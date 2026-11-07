"""Game-owned fixed-tick Mica execution and one durable repair transaction."""

import copy
import json
import math

from ..core import progress
from ..core.contracts import ContractError, canonical_digest, safe_json
from .mica_observation import MicaState, verify

TICK = 0.2


def saved_mica(world, fallback):
    stored = world.p.get("runtime_v1", {}).get("mica_by_world", {}).get(world.zone)
    if stored is None:
        return fallback
    return MicaState(tuple(stored["cell"]), stored["energy"], tuple(stored["abilities"]))


def replay(profile, event_id):
    for record in profile.get("program_library", {}).get("traces", []):
        if record.get("event_id") == event_id:
            return copy.deepcopy(record)
    return None


class MicaRunner:
    """Run bounded data only. Until completion, the profile is the last safe state."""

    def __init__(self, world, mica, pending, report, source):
        self.world = world
        self.mica = saved_mica(world, mica)
        self.pending = pending
        self.source = source
        self._report = safe_json(report)
        verified = verify(world, self.mica, pending, json.loads(self._report), source)
        self._verified = safe_json(verified)
        self._steps = verified["trace"]
        self._zone = world.zone
        self._target = pending.request()["observation"]["device_id"]
        self.event_id = (
            "mica-"
            + canonical_digest(
                [pending.snapshot_digest, pending.request()["source_hash"], verified]
            )[:59]
        )
        self.cursor = 0
        self.ticks = 0
        self._remaining = self._duration(self._steps[0]) if self._steps else 1
        self._elapsed = 0.0
        self.status = "running" if self._steps else "incomplete"
        self.message = "Mica is carrying out the verified plan."

    @staticmethod
    def _duration(step):
        return step["action"].get("ticks", 1)

    def cancel(self):
        if self.status == "running":
            self.status = "cancelled"
            self.message = "Mica recalled. The last safe checkpoint is unchanged."

    def advance(self, dt):
        if self.status != "running":
            return self.status
        if not math.isfinite(dt) or dt < 0:
            raise ValueError("Expected a finite nonnegative elapsed time")
        if self.world.zone != self._zone:
            self.cancel()
            return self.status
        self._elapsed += dt
        while self._elapsed + 1e-10 >= TICK and self.status == "running":
            self._elapsed = max(0.0, self._elapsed - TICK)
            self.ticks += 1
            self._remaining -= 1
            if self._remaining:
                continue
            self.cursor += 1
            if self.cursor == len(self._steps):
                self._commit()
            else:
                self._remaining = self._duration(self._steps[self.cursor])
        return self.status

    def visual(self):
        if self.status != "running":
            return None
        step = self._steps[self.cursor]
        fraction = min(1.0, self._elapsed / TICK) if step["action"]["type"] == "move" else 0.0
        a, b = step["from_cell"], step["to_cell"]
        return tuple(32 * (x + fraction * (y - x)) + 16 for x, y in zip(a, b))

    def _commit(self):
        profile = self.world.p
        old_runtime = profile.get("runtime_v1", {})
        if self.event_id in old_runtime.get("last_applied_event_ids", []):
            self.status = "duplicate"
            self.message = "This repair was already recorded."
            return
        try:
            # Verify again at the actual milestone: closed doors, device state and energy may have changed.
            verified = verify(
                self.world,
                saved_mica(self.world, self.mica),
                self.pending,
                json.loads(self._report),
                self.source,
            )
            if safe_json(verified) != self._verified:
                raise ContractError("STALE_SNAPSHOT", "The validated trace changed")
            if not any(
                intent["device_id"] == self._target and intent["operation"] == "activate"
                for intent in verified["proposed_intents"]
            ):
                self.status = "incomplete"
                self.message = "Mica finished the route without activating the target."
                return
            updated = progress.extensions(profile)
            runtime = updated["runtime_v1"]
            devices = runtime["device_state"]
            target_key = f"{self._zone}.{self._target}"
            if devices.get(target_key) == "online":
                self.status = "duplicate"
                self.message = "The target is already online."
                return
            devices[target_key] = "online"
            runtime.setdefault("mica_by_world", {})[self._zone] = dict(
                cell=verified["final_cell"],
                energy=verified["remaining_energy"],
                abilities=list(self.mica.abilities),
            )
            runtime["active_job"] = None
            runtime["last_applied_event_ids"] = (
                runtime["last_applied_event_ids"] + [self.event_id]
            )[-256:]
            event = dict(
                protocol_version=1,
                event_id=self.event_id,
                sequence=self.cursor,
                timestamp_tick=self.ticks,
                world_id=self._zone,
                event_type="device.state_changed",
                subject_id=self._target,
                payload={"state": "online"},
                idempotency_key=self.event_id,
            )
            record = dict(
                event_id=self.event_id,
                snapshot_digest=self.pending.snapshot_digest,
                source_hash=self.pending.request()["source_hash"],
                event=event,
                result=verified,
            )
            library = updated["program_library"]
            library["traces"] = (library["traces"] + [record])[-32:]
            # A failed disk write must leave both the real profile and in-memory world untouched.
            progress.save(updated)
        except (ValueError, OSError, progress.UnsupportedProfile) as exc:
            self.status = "rejected"
            self.message = str(exc)
            return
        profile.clear()
        profile.update(updated)
        self.status = "committed"
        self.message = f"Mica brought {self._target} online."

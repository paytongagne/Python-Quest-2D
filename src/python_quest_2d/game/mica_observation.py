"""Capture and verify immutable Mica observations without mutating the game."""

from dataclasses import dataclass
import hashlib
import json
import uuid

from ..core import protocol
from ..core.contracts import ContractError, canonical_digest, safe_json, source_digest


@dataclass(frozen=True)
class MicaState:
    cell: tuple[int, int]
    energy: int
    abilities: tuple[str, ...] = ("move", "scan", "interact")


@dataclass(frozen=True)
class Verification:
    request_json: bytes
    snapshot_digest: str

    def request(self):
        return json.loads(self.request_json)


def workshop_enabled(profile):
    return profile.get("settings", {}).get("mica_workshop") is True or protocol.enabled()


def device_state(world, identifier):
    runtime = world.p.get("runtime_v1", {})
    if not isinstance(runtime, dict) or not isinstance(runtime.get("device_state", {}), dict):
        return "offline"
    return runtime.get("device_state", {}).get(f"{world.zone}.{identifier}", "offline")


def device_locked(world, device):
    prerequisite = device.get("requires_device")
    return not set(device.get("requires", [])) <= set(world.p["completed"]) or (
        prerequisite is not None and device_state(world, prerequisite) != "online"
    )


def field_obstacles(world):
    cells = {tuple(cell) for cell in world.map.get("mica_barriers", [])}
    cells.update(
        tuple(gate["cell"])
        for gate in world.map.get("mica_gates", [])
        if device_state(world, gate["relay"]) != "online"
    )
    return cells


def observe(world, mica, target, seed=0):
    if not workshop_enabled(world.p):
        raise ContractError("UNSUPPORTED_CONTRACT", "Mica program verification is disabled")
    if world.p.get("deployment") or world.p.get("expedition_job"):
        raise ContractError("INVALID_INPUT", "Mica is already on a legacy delivery")
    if type(seed) is not int or seed < 0:
        raise ContractError("INVALID_INPUT", "Expected a nonnegative observation seed")
    walls = {(r.x // 32, r.y // 32) for r in world.walls}
    walls.update(
        (gate["x"] // 32, gate["y"] // 32)
        for gate in world.map["gates"]
        if gate["requires_challenge"] not in world.p["completed"]
    )
    walls.update((t["x"] // 32, t["y"] // 32) for t in world.map["interactables"])
    walls.update(field_obstacles(world))
    devices = []
    for device in sorted(world.map.get("mica_devices", []), key=lambda d: d["id"]):
        identifier = device["id"]
        locked = device_locked(world, device)
        state = "locked" if locked else device_state(world, identifier)
        capabilities = (
            [] if locked or identifier != target else sorted(set(device.get("capabilities", [])))
        )
        cell = tuple(device["cell"])
        walls.add(cell)
        devices.append(dict(id=identifier, cell=list(cell), state=state, capabilities=capabilities))
    if target not in {device["id"] for device in devices}:
        raise ContractError("INVALID_INPUT", "No registered Mica device at this destination")
    body = dict(
        schema=1,
        world_id=world.zone,
        device_id=target,
        seed=seed,
        robot=dict(
            id="mica",
            cell=list(mica.cell),
            energy=mica.energy,
            abilities=sorted(set(mica.abilities)),
        ),
        visible=dict(
            width=world.map["width"],
            height=world.map["height"],
            walls=[list(cell) for cell in sorted(walls)],
            devices=devices,
        ),
        objective=dict(target_id=target, required_state="online"),
        rules=dict(max_actions=64, step_energy=1, scan_energy=2, interact_energy=1),
    )
    body["snapshot_id"] = "snapshot-" + canonical_digest(body)[:55]
    return safe_json(body)


def prepare(world, mica, target, source, seed=0):
    snapshot = observe(world, mica, target, seed)
    req = protocol.validate_request(
        dict(
            kind="program_plan",
            protocol_version=1,
            request_id="request-" + uuid.uuid4().hex,
            mission_id=target,
            source=source,
            source_hash=source_digest(source),
            program_contract="mica.plan.v1",
            observation=json.loads(snapshot),
        )
    )
    return Verification(safe_json(req), hashlib.sha256(snapshot).hexdigest())


def verify(world, mica, verification, report, current_source):
    req = verification.request()
    obs = req["observation"]
    if (
        any(report.get(key) != req[key] for key in ("request_id", "mission_id", "protocol_version"))
        or report.get("passed") is not True
    ):
        raise ContractError("INVALID_EFFECT", "No passing worker response for this request")
    if world.zone != obs["world_id"]:
        raise ContractError("STALE_SNAPSHOT", "Destination changed; rescan before verification")
    current = json.loads(observe(world, mica, obs["device_id"], obs["seed"]))
    return protocol.validate_candidate(
        current,
        report.get("effect"),
        snapshot_digest=verification.snapshot_digest,
        source=current_source,
        source_hash=req["source_hash"],
    )

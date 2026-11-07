"""Persist immutable program revisions and bounded execution records."""

from datetime import datetime, timezone
import uuid

from . import progress
from .contracts import ContractError, source_digest


def _timestamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def change(profile, operation):
    updated = progress.extensions(profile)
    result = operation(updated["program_library"])
    progress.save(updated)
    profile.clear()
    profile.update(updated)
    return result


def save_revision(profile, source, parent=None):
    digest = source_digest(source)

    def insert(library):
        revisions = library["revisions"]
        if parent is not None and parent not in revisions:
            raise ContractError("INVALID_INPUT", "The parent revision is missing.")
        previous = revisions.get(parent, {})
        if previous.get("source") == source:
            return parent
        if (
            len(revisions) >= 128
            or sum(len(r["source"].encode("utf-8")) for r in revisions.values())
            + len(source.encode("utf-8"))
            > 524288
        ):
            raise ContractError(
                "INVALID_INPUT", "The library is full. Delete an unused revision first."
            )
        first = source.split("\n", 1)[0]
        name = first.removeprefix("# Name:").strip() if first.startswith("# Name:") else ""
        key = "program-" + uuid.uuid4().hex
        revisions[key] = dict(
            name=(name or previous.get("name") or "Mica program")[:48],
            source=source,
            contract="mica.plan.v1",
            verified=False,
            hash=digest,
            verified_worlds=[],
            created_at=_timestamp(),
            parent=parent,
            revision=previous.get("revision", 0) + 1,
        )
        return key

    return change(profile, insert)


def equip(profile, key):
    def assign(library):
        if key not in library["revisions"]:
            raise ContractError("INVALID_INPUT", "Select a saved revision to equip.")
        library["slots"]["mica"] = key

    change(profile, assign)


def delete_revision(profile, key):
    def remove(library):
        if key in library["slots"].values():
            raise ContractError(
                "INVALID_INPUT", "Equip a different revision before deleting this one."
            )
        del library["revisions"][key]

    change(profile, remove)


def record_verification(profile, key, world, digest, result, *, rehearsal):
    def record(library):
        revision = library["revisions"][key]
        revision["verified"] = True
        revision["verified_worlds"] = sorted(set(revision.get("verified_worlds", [])) | {world})
        revision["last_verified_at"] = _timestamp()
        if rehearsal:
            item = dict(
                event_id="rehearsal-" + uuid.uuid4().hex,
                mode="rehearsal",
                world_id=world,
                revision=key,
                snapshot_digest=digest,
                source_hash=revision["hash"],
                result=result,
            )
            library["traces"] = (library["traces"] + [item])[-32:]

    change(profile, record)

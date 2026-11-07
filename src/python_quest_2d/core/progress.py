import json
import os
import shutil
import copy
import tempfile
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from .challenges import LESSONS, ZONES, MAPS


class UnsupportedProfile(RuntimeError):
    """A newer profile must never be downgraded or overwritten."""


def extensions(profile):
    result = copy.deepcopy(profile)
    result.setdefault("program_library", dict(schema=1, slots={}, revisions={}, traces=[]))
    result.setdefault(
        "runtime_v1", dict(schema=1, device_state={}, active_job=None, last_applied_event_ids=[])
    )
    return result


def reject_future(profile):
    if (
        isinstance(profile, dict)
        and type(profile.get("schema_version")) is int
        and profile["schema_version"] > 4
    ):
        raise UnsupportedProfile(
            "This save needs a newer Python Quest version. Your progress has not been changed."
        )


def guard_write(profile):
    reject_future(profile)
    path = location()
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf8"))
        except (ValueError, UnicodeError):
            return
        reject_future(existing)


def fresh() -> dict:
    return {
        "schema_version": 4,
        "player": {"zone": "orientation", "x": 96, "y": 96, "xp": 0},
        "completed": [],
        "hinted": [],
        "drafts": {},
        "attempts": {},
        "world_flags": {},
        "review": {},
        "settings": {"sound": True},
    }


def location() -> Path:
    return Path(
        os.environ.get(
            "PYTHONQUEST_SAVE",
            Path(os.getenv("LOCALAPPDATA", Path.home())) / "PythonQuest2D" / "progress.json",
        )
    )


def save(p: dict) -> None:
    guard_write(p)
    if type(p.get("schema_version")) is not int or p["schema_version"] not in (2, 3, 4):
        raise ValueError("Only supported schema-2/3/4 progress can be saved")
    path = location()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf8",
            dir=path.parent,
            prefix="." + path.stem + "-",
            suffix=".tmp",
            delete=False,
        ) as stream:
            tmp = Path(stream.name)
            json.dump(p, stream, indent=2, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        # Check again in case another version wrote this path while encoding.
        guard_write(p)
        os.replace(tmp, path)
    finally:
        if tmp is not None and tmp.exists():
            tmp.unlink()


def load() -> dict:
    path = location()
    if path.exists():
        try:
            p = json.loads(path.read_text(encoding="utf-8"))
            reject_future(p)
            if not isinstance(p, dict):
                raise TypeError("profile")
            if type(p.get("schema_version")) is not int or p["schema_version"] not in (2, 3, 4):
                raise ValueError("Unsupported old or missing save schema")
            for k, v in fresh().items():
                if not isinstance(p.get(k), type(v)):
                    raise TypeError(k)
            p["settings"].setdefault("sound", True)
            if not all(isinstance(d, str) for d in p["drafts"].values()):
                raise TypeError("drafts")
            if p["player"]["zone"] not in MAPS or not all(
                isinstance(p["player"].get(k), (float, int)) for k in ("x", "y", "xp")
            ):
                raise ValueError("player")
            if p["schema_version"] == 2:
                backup = path.with_suffix(".pre-greenline.json")
                if not backup.exists():
                    shutil.copy2(path, backup)
                p["schema_version"] = 3
            if p["schema_version"] == 3:
                backup = path.with_suffix(".pre-expedition.json")
                if not backup.exists():
                    shutil.copy2(path, backup)
                p["schema_version"] = 4
            return extensions(p)
        except (KeyError, ValueError, TypeError, UnicodeError):
            shutil.copy2(
                path,
                path.with_suffix(
                    ".damaged-"
                    + datetime.now().strftime("%Y%m%d%H%M%S")
                    + "-"
                    + uuid.uuid4().hex[:8]
                    + ".json"
                ),
            )
    return extensions(fresh())


def award(p: dict, key: str) -> int:
    guard_write(p)
    now = datetime.now()
    p["review"][key] = (now + timedelta(days=1)).date().isoformat()
    if key in p["completed"]:
        save(p)
        return 0
    xp = 25 if key in p.get("revealed", []) else 75 if key in p["hinted"] else 100
    p["completed"].append(key)
    p["world_flags"][LESSONS[key]["world_effect"]] = True
    p["player"]["xp"] += xp
    save(p)
    return xp

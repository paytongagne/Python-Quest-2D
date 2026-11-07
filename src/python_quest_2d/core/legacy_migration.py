import json
import shutil

from .challenges import LESSONS, ROOT
from .progress import save


def migrate(path, p):
    old = json.loads(path.read_text(encoding="utf-8"))
    mapping = {
        str(r["legacy_index"]): r["challenge_id"]
        for r in json.loads((ROOT / "content/legacy_index_map.json").read_text())
    }
    for field in ("completed", "hinted", "revealed"):
        p[field] = list(
            dict.fromkeys(mapping[str(i)] for i in old.get(field, []) if str(i) in mapping)
        )
    p["drafts"] = {
        mapping[k]: v
        for k, v in old.get("drafts", {}).items()
        if k in mapping and isinstance(v, str)
    }
    p["player"]["xp"] = int(old.get("xp", 0))
    p["world_flags"] = {LESSONS[k]["world_effect"]: True for k in p["completed"]}
    backup = path.with_suffix(".pre-2d.bak")
    if not backup.exists():
        shutil.copy2(path, backup)
    save(p)

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
ZONES = ("orientation", "launch", "control", "sensor", "engine", "algorithm")
NAMES = (
    "Orientation Hangar",
    "Launch Pad",
    "Control Room",
    "Sensor Bay",
    "Engine Workshop",
    "Algorithm Arena",
)


def load_content(group):
    return {
        p.stem: json.loads(p.read_text(encoding="utf-8"))
        for p in (ROOT / "content" / group).glob("*.json")
    }


LESSONS = load_content("challenges")
LESSONS.update(load_content("expansion"))
LESSONS.update(load_content("expeditions"))
MAPS = load_content("maps") | load_content("sectors") | load_content("planets")
for zone in ZONES:
    for sequence in range(1, 5):
        key = f"{zone}_{sequence:02}"
        ch = LESSONS[key]
        if (
            ch["id"] != key
            or not ch["objective"]
            or not (ch.get("cases") or "expected_stdout" in ch)
        ):
            raise ValueError("Invalid mission " + key)

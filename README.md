# Python Quest 2D

An offline Pygame adventure with **76 playable Python missions** across Astra, Greenline, Workshop, Orion, Titan, Helix, and Aurora. The full campaign target is 152 missions.

Install Python 3.13 and run from the checkout:

```sh
python -m pip install -r requirements.txt
python play.py
```

Move with WASD or arrows, interact with E, run code with Ctrl+Enter, and open the flight log with J. The Workshop is accessible from the Astra hangar or J then 8. T opens world travel; D enables Expedition Preview. O inspects nearby equipment diagnostics; R opens program replay. Existing schema-4 profiles remain compatible.

```sh
python -m unittest discover -s tests -v
python tools/check_content.py
python tools/work_ticket.py next
```

The tests use disposable profiles. For a separate game profile, set `PYTHONQUEST_SAVE` before launching. The worker runs practice code locally in a separate Python process and is not a security sandbox.

[Current development state](docs/PROJECT_STATE.md) · [Live ticket ledger](handoff/12_TASK_STATE.json) · [Evidence](docs/evidence) · [Preproduction Bible](planning/PROGRESS_INDEX.md) · [Work handoff](planning/handoff/13_FINAL_WORK_READ_FIRST.md)

GitHub Actions runs tests on pushes and pull requests. Stable version tags (`vX.Y.Z`) also build a portable Windows ZIP and upload it as a workflow artifact. Generated builds and personal saves stay outside Git.

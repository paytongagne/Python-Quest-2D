# 10 — CI / host execution matrix

| Host | Gate | Command | Status during Stage10 |
|---|---|---|---|
| Any OS, Python3 stdlib | Stage 08 | `python -m unittest discover -s tests -p 'test_biomed_planning.py' -v` | runnable here |
| Any OS, Python3 stdlib, v1.4 source path | Stage 09 | `PYTHONQUEST_V14_ROOT=/path python -m unittest discover -s tests -p 'test_stage09_*.py' -v` | runnable here |
| Any OS, Python3 stdlib | Stage 10 | `python -m unittest discover -s tests -p 'test_stage10_*.py' -v` | runnable here |
| Any OS, archive | Windows ZIP static | `python tools/verify_windows_archive.py release.zip --json report.json` | runnable here |
| Windows + bundled runtime | full scripted | `runtime\python.exe -m pytest -q tests` if pytest available; otherwise each included `tests/test_*.py` | must run on real build |
| Windows native display | release | `runtime\python.exe tools\native_smoke.py` and `native_visual_revision.py`, run `.bat` | must run on real Windows |
| Windows real hardware | visual/perf | instrument `app.draw`, record frame distribution and capture three resolutions | must run on real Windows |
| Human test stations | usability | `qa/10_HUMAN_PLAYTEST_PROTOCOL.md` | not automated |

Never mark unavailable platform as PASS. Report BLOCKED and the missing prerequisite.

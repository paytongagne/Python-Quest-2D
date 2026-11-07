# Verification
Windows x64, bundled Python 3.13.9 and pygame-ce 2.5.8.

- Original campaign playthrough completed all 24 missions.
- Greenline playthrough completed all 16 missions and checked delivery resume, deck extensions, travel and boss state.
- Expedition playthrough completed all 28 new missions, visited all five destinations, resumed deliveries, preserved boss phases and verified no duplicate XP.
- Route contracts rejected malformed paths, out-of-bounds and blocked cells, non-cardinal movement, oversized outputs and incorrect costs.
- Syntax errors, runtime exceptions and infinite loops produced grading feedback.
- Save migration preserved XP, Greenline deployment, completion, flags and unknown fields in test fixtures. Pre-upgrade backups retained the original bytes. Live user saves were not edited.
- Native Windows smoke test exercised the actual SDL window, star map, Python input, lunar delivery, replay, 1280x720 resize, all five destinations, return travel and quit.
- Native update/render work averaged 7.14 ms over 210 frames, maximum 11.21 ms, on this machine.

Tests run with runtime/python.exe:
tests/test_flight.py, tests/test_controls.py, tests/test_greenline.py, tests/test_expeditions.py.
Native check: tools/native_expeditions.py.

These were scripted playthroughs and temporary profiles. Human playtesting of every lesson, a second physical Windows machine, alternate keyboard layouts and listening tests remain unverified. The Python worker is not a hardened security sandbox. Deliberately spawned descendant processes have no guaranteed cleanup.

The extracted Windows archive also passed expedition regression and the native five-world smoke test. START_PYTHON_QUEST_2D.bat opened the packaged game and saved successfully on close using a disposable profile.

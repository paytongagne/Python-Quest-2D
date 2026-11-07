# Greenline release verification

## Automated checks

- Original 24-mission campaign walked through its collision system, terminals, grading, bulkheads, lifts and finale.
- All 16 Hydroponics reference solutions executed through the subprocess grader. The chapter playthrough traversed all 16 repair locations in order, verified that the next repair was blocked before its prerequisite, and reached the canopy ending.
- Five rover programs produced routes that were validated and animated. Invalid commands, non-list results, excessive steps, wall collisions, out-of-bounds moves and incomplete routes were rejected.
- A learner attempt to mutate the goal fixture failed. The worker passes copies of inputs to learner functions.
- A delivery resumed from its saved step after restarting. Repeat delivery awarded zero additional XP.
- The tray controller persisted its selected beds. The final controller persisted its actual returned event sequence.
- Tested all six original deck extensions, archive interactions and return tram destinations.
- A schema 2 fixture containing 300 XP, three completed repairs, custom drafts, attempt history, settings and an unknown field upgraded without changing those values. Its original bytes were retained in a separate backup.
- Original editor, clipboard, history, indentation, mouse positioning, draft saving, syntax error, timeout, wrong output, crash, corruption and legacy import checks passed.

The gameplay tests use scripted input and disposable profiles. The user's live save was not edited during development. Screenshots come from the running game renderer.

## Native and packaged Windows checks

The extracted release passed its chapter, editor and original content checks. The native Windows display test entered Hydroponics through the tram, submitted Python, animated Mica's delivery, awarded XP, opened the survey, resized the window and quit. The update/render portion averaged 6.46 ms across 170 frames, with an 11.26 ms maximum on this machine. This measures frame work rather than end-to-end frame rate on other hardware.

The actual START_PYTHON_QUEST_2D.bat launcher opened the extracted game's window and saved on close. Both Windows checks used a disposable save path. The portable and source archives contain the same game source.

## Practical limits

A human playthrough of every mission, different keyboard layouts, listening tests and another physical Windows computer remain unverified. The worker runs trusted local practice code under the user's account. Its process boundary and timeout are not a hardened security sandbox. Subprocess descendants launched deliberately by learner code have no guaranteed process-tree termination.

Run the included tests from the project folder with the bundled interpreter:
```bat
runtime\python.exe tests\test_flight.py
runtime\python.exe tests\test_controls.py
runtime\python.exe tests\test_greenline.py
runtime\python.exe tools\check_content.py
```


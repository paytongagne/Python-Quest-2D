# Release 1.3 verification — 2026-11-06

## Passed
- 18 unittest methods: original 24-mission flight, 16 Greenline missions, 28 expedition missions, four Workshop missions, editor controls, physical collision, legacy/corrupt saves, migration, worker failures, rover delivery/replay and restart.
- Workshop reference classes and starter-code rejection; invalid boolean battery values and broken water conservation rejected. Constructor, independent-instance, property, invalid assignment, NaN/infinity, repeated transfer and capacity/supply cases checked.
- Physical walking through all four Workshop bays; unopened gates block later bays; previously completed mission, XP, draft and world flag survive restart. Repeat submissions grant no extra XP.
- All 72 mission titles fit bounded HUD rows. Resized mouse travel honors locks and preview. Reduced-motion rendering runs.
- Native Windows driver: four Workshop Python submissions, live machine rendering, five-world arrivals, resize, saved return and clean quit. Update/render mean 4.02 ms, maximum 8.69 ms in the measured 180-frame run (not an end-user hardware guarantee).
- Screenshots inspected for Workshop machines, arrival and HUD; machine footprints added after inspection to prevent walking over device readouts.

## Packaging verification
- Windows and source ZIP integrity checks passed; new modules, content, tests and runtime are present where intended.
- Extracted Windows package passed all three Workshop test methods with its bundled interpreter.
- The actual extracted START_PYTHON_QUEST_2D.bat opened a native game window, closed normally and wrote its disposable save.
- The original content validator independently passed all 24 original reference solutions and six map schemas.
- Final full regression: 18 methods passed in 14.67 seconds. Reproduction commands are in README.md.

## Limits
Scripted test input and reference solutions supplement visual inspection; this is not a full manual playthrough by a new learner. No clinical validation applies to synthetic biomedical lessons. The worker is timeout-isolated but is not a security sandbox. No older Windows versions or different GPU/display configurations were tested.

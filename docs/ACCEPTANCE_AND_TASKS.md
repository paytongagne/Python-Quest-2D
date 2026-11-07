# ACCEPTANCE CRITERIA, BUILD TASKS AND PRIORITY

This is an implementation checklist for Work mode, not a claim that items are already complete.

## Foundation (P0)
- [ ] Set up editable package installation, pygame-ce dependency, pytest.
- [ ] Validate all 24 challenge files; import and test 20 legacy solutions.
- [ ] Define GradeResult and subprocess protocol.
- [ ] Add grader timeout/crash/error tests.
- [ ] Implement schema-v2 save and atomic writes.
- [ ] Implement v1 save migration preserving XP/drafts/completions without overwriting old save.
- [ ] Implement state transitions and duplicate-XP prevention.

## First playable vertical slice (P1)
- [ ] Window starts with working frame rate, controllable player and 2D room.
- [ ] Player-wall/door collisions and nearby interaction prompts work.
- [ ] E opens terminal and pauses world movement.
- [ ] Editor supports multiline, indentation, cursor, selection, clipboard, undo, scroll.
- [ ] Ctrl+Enter grades typed code asynchronously with feedback.
- [ ] Failed solution shows intelligible output, edit-and-rerun works.
- [ ] Successful solution opens actual door and grants XP once.
- [ ] Exit/reopen restores progress, door state and editor draft.
- [ ] Demonstrate on-screen with screenshot or capture.

## Campaign (P2/P3)
- [ ] 4 orientation missions in first room cluster.
- [ ] 20 migrated missions across five zones.
- [ ] 6 map backgrounds with relevant interaction objects.
- [ ] One visually distinct end event for each zone.
- [ ] Algorithm boss gates on correct Two Sum indices.
- [ ] PIP hints, lesson explanations, journal, completion progress.
- [ ] Review mode and player-visible progress/milestones.

## Release (P4/P5)
- [ ] Cohesive original/licensed assets and music attribution.
- [ ] UI scaling and readable fonts at common resolutions.
- [ ] Accessibility basics and control descriptions.
- [ ] No internet use; low latency, no blocking render loop.
- [ ] Clean Windows launch instructions, no administrator permission needed.
- [ ] Clean install tested and files packaged.
- [ ] Final ZIP with application, docs, tests and changelog.

## Definition of done for the entire project
A player who has never used the app can install it, move through actual 2D rooms, type Python to solve a mission, diagnose a wrong answer, open a door with correct code, persist progress, continue through 24 unique challenges, and finish the Two Sum boss without online services.

## Out of scope unless all above are complete
Skill trees, complex combat, crafting, multiplayer, server leaderboards, user-created shared code packs, advanced graphics engine swaps, scripted cutscene editor, AI tutoring backend.

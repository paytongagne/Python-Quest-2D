# WORK MODE HANDOFF — PYTHON QUEST 2D

## Mission

Build and release a polished, functioning, offline-first 2D top-down Python learning adventure for Windows from the attached project blueprint. Do actual implementation, testing, packaging and playable verification. Do not stop after architecture, pseudocode, placeholder mockups, or a decorative UI.

## Mandatory inputs

1. Read `docs/MASTER_GAME_DESIGN.md` entirely.
2. Inspect `content/challenges/*.json` (20 migrated lessons plus orientation data) and authoring reference tests.
3. Follow `docs/TECHNICAL_HANDOFF.md` for structure and contracts.
4. Treat `docs/ACCEPTANCE_AND_TASKS.md` as checklist and source of truth for milestone completion.
5. Preserve and improve the earlier Python Quest v1 learning mechanics, not replace them with multiple choice.

## Product requirements

- Windows-first, offline, no accounts or server.
- Python 3.12 preferred, pygame-ce 2.5.8 initial dependency.
- Smooth WASD/arrow top-down movement, collisions, E-to-interact.
- Full Pygame window with a working in-game code editor, problem statements, progressive hints, visible test results.
- Grade learner code in a subprocess, not in Pygame frame thread. Strict timeouts and user-facing exception display. Do not claim the worker is a hardened security sandbox.
- Mission passes unlock actual doors/systems and persist. XP once per mission; no penalty for mistakes.
- Incorporate all 20 original challenges; add four beginner orientation challenges (further early `print`/variables lessons if stdout evaluation is implemented correctly).
- Six zones and a coherent throughline ending with Two Sum boss.
- Track completed missions, XP, draft code, help usage, flags, position, review state. Add importer for old `~/.python_quest_progress.json`, with consent and original backup.
- Responsive local code editing: multiline, auto-indent, undo/redo, clipboard, correct keyboard focus, line numbers/error display.
- Make visuals cohesive and playable, with placeholder assets acceptable early and final original or permissively licensed assets.

## Ordered implementation — do not skip gates

**P0 Foundation:** validate content schema, consolidate core grader, tests run without pygame, save system/migration.

**P1 Playable vertical slice:** one explorable map, player movement/collision, one terminal, working coding UI/test runner, animated gate unlock, real save/load. Demonstrate it is playable with screen capture/screenshot.

**P2 Game shell:** settings, HUD, NPC, zone transitions, mission log, audio interface.

**P3 Campaign:** six zones, all 24 missions, logic and map persistence, review terminals, final boss sequence.

**P4 Polish:** cohesive pixel art, sound, accessibility, polish to editor/feedback, bug fixes.

**P5 Distribution:** README and Windows startup flow, packaged release where feasible; clean environment smoke test; zip deliverable.

## Quality bar

- Use unit tests for challenge content, grader, timeouts, progress, map metadata, XP and gate transitions.
- Verify all reference solutions pass all challenge tests, including boundary cases.
- Manual playtest: walk to terminal, write incorrect code, see failure, fix code, see door unlock, exit game and resume with correct state.
- Keep game loop responsive on infinite user loops.
- Be explicit about anything untested or dependent on the target Windows environment.
- Do not use proprietary game assets, copyrighted music, or expose other user data.
- Prefer practical working features over beautiful mockups.

## Deliverables

1. Full repository with clean architecture, comments, test suite and content data.
2. A Windows-usable distribution/launcher with installation instructions.
3. A playable single-player campaign, actual Python editing and challenges.
4. Short changelog and test report listing passed/failed tests and unresolved issues.
5. A few screenshots or a short gameplay capture proving core interaction.

## Collaboration contract

Choose reasonable defaults without repeatedly asking for design approval. When scope threatens the build, prioritize gameplay + editor + grader + saving, then one complete zone, then remaining content, then polish. Report genuine blockers and never claim a feature was tested if it was not.

# 00 — Executive decisions and success definition

## Project identity (locked)
**Python Quest 2D is a top-down exploration adventure powered by real Python and persistent, simulated engineering systems.** Adventure first, programmable automation second, technical engineering challenges increasingly emphasized toward the finale. The player is a systems engineer restoring a damaged interplanetary research network with ION, PIP, MARA and Mica. Code *does* something in the world; it is not merely a gate-key trivia answer.

## Product pillars
1. **Explore before you program.** Discover a malfunction, see physical consequences, converse, and inspect a device before opening its editor.
2. **Real, reusable Python.** Correct code creates a saved capability. Repeat, inspect, refactor and optimize without redoing all scaffolding.
3. **Immediate, visible outcomes.** Robots move through actual tile collision; pipes fill, live graphs update, doors open and shortcuts remain open.
4. **Learn independently.** Clear requirements, optional progressive hints and robust diagnostics. No automatic answer-writing. Transfer problems prove retention.
5. **Each world is unmistakable.** Unique architecture, soundscape, activity and mode of reasoning. Not palette-swapped copies of terminal halls.
6. **Respect time and progress.** No XP farming, no lost saves, no unskippable cutscenes or harsh death while reading code.
7. **Engineering is observable.** The game reveals inputs, tests, state transitions, errors, time and expected effects.

## Scope and count
**Current baseline** 76 missions. **Planned goal** 152 total. **Remaining** 76: Workshop 09–16 (8), Algorithm Tower 01–16 (16), Titan 05–16 (12), Helix 05–16 (12), Aurora 05–16 (12), Mission Control 01–16 (16). Orion 01–16 are implemented and become the first flagship retrofit, not a source of duplicate mission content.

## Critical change in development measurement
The key release metric is **engaging, independently testable player capabilities**, not mission count. A release is valuable when it ships at least one durable capability (e.g. saved Mica program or a genuinely explorable level), coherent art, feedback, and regression-proof progress. Do not add sixteen shallow consoles merely to increase a counter.

## Decisions already made
- Keep Pygame-ce, Python 3.10+ source compatibility and Windows offline distribution. Existing release packages may use Python 3.13.9.
- Keep 32-pixel world-tile semantics for compatibility unless a specific authored sublayer is introduced.
- Maintain current content and v1.4 canonical mission IDs. Add a new `algorithm_tower` zone; existing `algorithm_01..04` are *not* renamed.
- Make Mica's persistent programmable action system the signature mechanic, with bounded action-plan outputs rather than executing learner code every frame.
- Keep independent validation of worker output in the game. Use data snapshots, no shared executable Python objects crossing the process boundary.
- Keep optional Expedition Preview; fix normal progression and clearly label preview as optional noncanonical travel.
- One high-quality, end-to-end Orion scenario serves as a visual, mechanical and pedagogical benchmark before other world-wide retrofits.
- Keep 100/75/25 first-pass/hint/reveal XP behavior for existing content; new optional mastery ranks are separate and nonfarmable.
- Synthetics only for Helix/Aurora. Do not claim a real medical device or expose any proprietary Affera internals.

## Explicitly *not* in first implementation cycle
Online multiplayer, generated AI NPC dialogue, a live MQTT broker, user-account cloud sync, high-speed combat, medical diagnosis, real-world device control, general Python plugin imports, unrestricted self-modifying game objects, infinite procedural map generation, premium art pipeline dependencies, and irreversible permadeath.

## Acceptance gate for 'fun, not more of the same'
Have an unfamiliar player begin in Orion with no instruction from the developer. They should be able to find their objective, interact with two distinct objects, program Mica, see an unambiguous result, find an optional discovery, and return to hub. A failure on any step triggers design iteration before scaling this gameplay pattern. Targets in `docs/10_TEST_AND_RELEASE_PLAN.md` are proposals, not currently measured outcomes.

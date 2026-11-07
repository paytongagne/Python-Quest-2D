# 01 — Complete game design bible

## High concept and fantasy
The Astra Research Facility survives a cascading relay malfunction. The player travels between a repair station, moon outposts, a cloud data grid, a biomedical research laboratory, and an orbital mapping observatory to reconnect the network. Each recovered subsystem grants a new engineering ability, and each location visibly changes. Programming is both a puzzle mechanic and the player's primary toolkit.

**Desired feelings:** curious during travel, capable while programming, proud when a simulated machine moves, relieved when a test finally passes, intrigued by environmental clues, and ambitious when optional optimization appears. Avoid frustration from UI opacity, aimless corridors and unhelpful error messages.

## Core loop: 6–15 minute mission arc (design target, not a timer)
1. Arrive at landmark or discover a fault via an animation, sound or short NPC exchange.
2. Gather constraints by reading a diagram, device status, damaged network route or testable sample.
3. Open an editor only after the need is contextualized. The learner may consult an in-world reference manual.
4. Submit real Python to a short-lived worker. Tests show failures with informative discrepancies; no automatic solution.
5. See validated action traces or data snapshots physically modify the game. Let the player inspect, pause, step, replay.
6. Store a reusable program, unlock a route, collect a blueprint or improve a machine. Offer a side objective or another mission.

### Player micro-activities between code sessions
Walk/observe, map and scan, talk to ION/MARA/PIP, discover artifacts, change device parameters, drag a cable into a port, inspect a circuit, ride a tram, launch a drone, revisit a previously repaired area, compare a previous algorithm and a new one. Each is a supported interaction, not just background scenery. A player should not face more than two consecutive missions that consist only of entering a terminal and leaving it.

## Player progression layers
- **Story progression:** repair physical systems and open named routes.
- **Tool progression:** Mica scanner → navigation → hauling → network probes → instrumentation → mapping sampler → orchestration.
- **Knowledge progression:** variables, functions, loops → OOP → graphs/algorithms → queues/async → synthetic time series/geometry → integration/testing.
- **Exploration progression:** world maps, secrets, warp points, optional archives and revisitable upgrade paths.
- **Mastery progression:** optional efficiency challenges. Finishing core lessons never requires optimized Big-O under severe pressure.

## Meta-upgrades and resources
Use **engineering parts** for optional blueprint upgrades, not consumable credit gates. Parts are earned from a fixed set of discoveries, quests and optional mastery, never from endless repetitive farming. Upgrades add *new actions* (scan radius, extra Mica action slots, stronger data scope, replay controls), not pay-to-skip knowledge. XP retains current reward policy and grants cosmetic achievement/badge recognition; no existing XP total is recalculated. Separate track records `mastery_badges` avoid disrupting XP.

## Game modes
- **Explore:** standard movement, collisions, interactive prompts, NPCs, maps, optional scanning.
- **Inspect:** device status, constraints and sample data; world simulation paused where needed.
- **Code:** full editor, test output, hints, accessible controls; world and hazards paused. Code is not run on the game loop.
- **Deploy:** replay validated bounded actions or update instruments in world; visible run/pause/step/rewind.
- **Review:** after mission success, show what function was used and why it passed; offer an optional transfer challenge.
- **Travel:** depart → flight or transit scene → named arrival; skip, reduced motion and restore checkpoint support.
- **Pause/Options:** rebindable controls, font scale, audio, motion, contrast, save and quit.

## Input scheme (proposal; reconcile existing bindings)
WASD/arrows move; E interact; T worlds; J journal; M local map; O inspect nearby device; R replay; Esc pause/back; Enter accept; Ctrl+Enter run code. New capability: **Q** quick companion command menu (when not editing); `Tab` cycles nearby targets; **F** scan (if not already used). Only bind after checking current v1.4 key handling and create `controls.json` keybinding map. Every action must also be operable through keyboard-first UI, with mouse optional. Don't break existing F1/F2/F3/F4 editor hint/scroll behaviors.

## Difficulty and scaffolding
Four pedagogical stages for every new mechanic: Observe (predict visible result), Guided (complete a short part), Independent (write API from scratch), Transfer (apply same API to unfamiliar map/input). New mechanics should be introduced without lethal/timed hazards. Optional optimization comes later with concrete traces and cost comparisons.

## Replayability without grinding
- User can revisit any accepted script and run it on a fresh safe synthetic fixture.
- Program slots save source and version history; submitted code is treated as local trusted practice code with warning.
- Replays award **zero repeat mission XP**.
- Exploration secrets and cosmetic upgrades can be earned once. Completion flags are idempotent.
- A chapter-clear environmental transformation persists after restart, visible from the hub and in local areas.

## Core reward cadence (design targets)
- Micro feedback within one second of immediate interaction (button push, hover, audio) *not* equivalent to guaranteeing worker completion within 1 second.
- After each successful run: a distinct machine event, concise test summary and tangible objective update.
- At least one optional side discovery per authored major sector; at least one revisitable shortcut per world.
- Every four missions: a new world capability, actor, landmark or machine state.
- Every world boss: ≥2 phases, independent save checkpoints and different visual states.

## Learning integrity
Do not let hints or AI write the student's solution by default. There must be a meaningful unaided path with tooltips and examples. `F2` confirm-reveal already exists and should remain, with reduced XP. The mastery system should show *why* a strategy works, but neither reward luck nor require unnecessary memorization of code golf.

## Success criteria
1. Can player discover and finish flagship Orion outpost without developer instructions?
2. Does at least one program remain reusable after its first completion?
3. Does incorrect Python produce informative feedback while leaving machine state unchanged?
4. Is the program-to-world effect visibly causal, replayable and persistent?
5. Do at least three worlds have genuinely different gameplay verbs instead of different colored screens?
6. Are all previously completed missions and live saves preserved?

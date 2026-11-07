# Visual correction & Workshop second wing — v1.4
2026-11-06

76 playable missions: Astra/Greenline 40, Workshop 8, Orion 16, Titan 4, Helix 4, Aurora 4. Developed in the existing v1.3 source. Save schema remains 4 and existing mission IDs are unchanged.

## World presentation
- Removed all large Orion route panels and the Titan/Helix/Aurora data panels from the world renderer. Detailed diagrams now belong to a dedicated nearby-console interface: O opens diagnostics, E opens code, Esc returns.
- Added reusable original pixel sprites for pilots, scientists, consoles, dishes, telescopes, tanks, racks, crates, rovers, beacons and shuttles. Characters and props share grounded shadows and are drawn in depth order. Pilot facing, walk frames and idle stance are distinct.
- Orion uses irregular shaded regolith, pebble texture, small impact craters, rocky boundaries, tracks, relay dishes and physical rover sprites. Crater placement rejects walls and console footprints.
- Titan gains conduit lanes and server racks; Helix gains cultivation windows and tank instruments; Aurora gains observation windows, telescopes and inlaid meridians. These worlds retain their existing playable maps; further architectural diversification remains planned.
- Workshop display slabs are replaced by grated assembly floors, equipment banks, physical instruments and service routes. Tested object state changes drones, needles, battery fill, tank fill, sensor lamps and service-log crates. Detailed numeric results remain available in diagnostics.
- Consoles, NPCs, racks and rover equipment animate. Existing repair particles and completion feedback remain. Expedition gates retain their opening animation.
- The compact mission HUD remains outside the world viewport. A gold diamond marks the next unfinished local-world mission, clamped to the viewport when offscreen.

## Navigation and travel
- A labeled WORKSHOP entrance is now present in Astra's Orientation Hangar. Approach and press E. The journal's J → 8 entry remains visible.
- Workshop camera framing favors the northern consoles while the player uses the southern service walkway.
- Travel stages show departure from the current environment, an animated flight, destination reveal and arrival. Any key skips; reduced motion omits the flight animation. Movement pauses during the staging sequence.
- Locked travel names the prerequisite. Expedition Preview is retained because some campaign prerequisites have not shipped.
- New solid props use collision footprints. A legacy save positioned inside a newly added prop can walk out without resetting progress or teleporting the player.

## Workshop 05–08
A second assembly wing extends the district from 64×24 to 128×24 tiles. New doors require preceding repairs.
- 05: Rover inheritance and polymorphic reports; subtype and independent-state tests.
- 06: composed Battery objects, actual delegated consumption, depleted/negative rejection and independent swappable cores.
- 07: a custom SensorFault exception with exact-type checks and inclusive configured limits.
- 08: read a supplied temporary UTF-8 service log with a context manager; empty/CRLF/Unicode/final-line and missing-file tests, observed handle closure and exact error-prefix counting.

Tests run real learner Python in the existing timed subprocess. First-pass XP, duplicate-XP prevention, drafts, old saves and machine snapshots persist.

## Remaining work — 76 missions
Workshop 09–16: 8. Algorithm Tower: 16. Mission Control Annex: 16. Titan: 12. Helix: 12. Aurora: 12.

Next: Workshop 09–12, then remaining Workshop and deeper Titan/Helix/Aurora batches. Larger bespoke planetary layouts, richer NPC stories, additional hazards, advanced synthetic biomedical pipelines and endgame bosses remain. This is a verified visual-system foundation and playable campaign increment, not a claim that every environment has reached final indie-game art quality. Astra's established deck art is largely preserved, with the new player and entrance.

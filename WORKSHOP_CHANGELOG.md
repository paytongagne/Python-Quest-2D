# Workshop & presentation release 1.3 — 2026-11-06

72 playable missions: Astra core/Greenline 40, Workshop 4, Orion 16, Titan 4, Helix 4, Aurora 4. Existing mission IDs, XP and schema-4 saves are retained.

## Presentation and travel
- A shared HUD separates progress, four local mission rows and field communications. All 72 mission titles are tested to fit their rows.
- Nearby interactables receive a focus ring and E prompt. Consoles scan, repairs show a completion card and particles, and restored expedition bulkheads retract.
- World arrivals show destination-specific staging with a short progress animation; any key dismisses the banner. Reduced-motion mode retains static cues.
- Star-map destinations support mouse clicks with letterbox-correct coordinates, visible locked-route feedback, and distinct planet markings.
- Lunar route boards have framed backgrounds. Titan, Helix and Aurora readouts now stay inside expanded device frames. Packet animations remain within their displays.

## Workshop District 01–04
Open J, then 8. Four interconnected assembly bays span a 64-by-24-tile district. Physical machines block movement; service walkways and three sequential bulkheads connect the bays. ION explains the repair order, M shows a survey, and J or the shuttle returns to travel.

1. Restore the Drone Blueprint: actual Rover classes, required arguments and independent instances; two drones awaken with returned IDs and power.
2. Calibrate the Probe: cumulative instance methods and isolation; instrument needles display the tested readings.
3. Protect the Battery: property setter, boundaries, invalid types, NaN/infinity and rejected assignments preserving state; charge displays show the validated objects.
4. Refill the Reservoir: stateful capacity/supply-constrained transfers, repeated calls and negative rejection; a hydraulic fill animation shows the resulting water and remaining supply.

Object fixtures run in the disposable Python worker. The game receives and validates a plain-data snapshot; it never executes learner classes in the render loop. Saved machine state survives restart. Repeating missions awards no extra XP.

## Save compatibility
No new schema migration. Existing schema-2/3 migration paths remain tested; schema-4 profiles load unchanged. Original completion IDs, drafts, XP and world flags are preserved. Tests use disposable profiles and do not alter the player's live save. The 68-mission v1.2 archives remain available as a rollback checkpoint.

## Remaining work — 80 missions
Workshop 05–16 (12); Algorithm Tower 01–16 (16); Mission Control Annex 01–16 (16); Titan 05–16 (12); Helix 05–16 (12); Aurora 05–16 (12).

The Workshop is an accessible chapter preview through the journal; full campaign prerequisite routing remains unfinished. The existing Expedition Preview option remains necessary for routes whose prerequisite chapters have not shipped. Workshop machines visualize tested fixtures, rather than accepting unrestricted real-time object commands. Later inheritance, file fixtures, async/concurrency, advanced synthetic signal processing, mapping pipelines and endgame bosses remain unimplemented. Presentation work is a first pass; environments still use generated geometry rather than a complete illustrated art set.

# 04 — World and level atlas

## Shared navigational architecture
Tiles remain 32 world pixels for v1.4 compatibility. Each destination has (a) visually distinct arrival point with world label, (b) a landmark or vista, (c) obvious primary objective clue, (d) at least one optional side path, (e) a named fast-travel return and (f) spatially integrated programmable device. Map coordinates below are **planning coordinates**; reconcile against existing collision maps, terminal IDs, NPCs and saved player positions before implementation.

### Canonical mission sequence: 152
`orientation → launch → control → sensor → engine → algorithm` (24 original) → `hydro_01..16` → `workshop_01..16` → `algorithm_tower_01..16` → `orion_moon_01..16` → `titan_cloud_01..16` → `helix_bio_01..16` → `aurora_ep_01..16` → `mission_control_01..16`.

For worlds already reached through Expedition Preview, maintain the saved world checkpoint. Existing completed missions remain accessible independent of new canonical unlock graph. The `Mission Control Annex` physical hub can appear earlier, but the final 16-mission sequence follows Aurora to keep the story logical. No self-referential world prerequisite. Each node must be graph-reachable under normal play without preview.

## World 1 — Astra Research Facility
**Identity:** familiar home hub, cold teal-lit corridors, multi-level tram, engineering workshops, buildable display area. **Intent:** teach basics and transform the station from fragile to productive. **Landmarks:** Orientation Hangar, Greenline hydroponics, Workshop Foundry, Algorithm Tower, Mission Control Annex (locked full finale). **Interaction loops:** repairs animate infrastructure, resource services activate and NPC work rhythms change. **Visual design:** warm repair sparks and orange machines contrast with cool control hall cyan. **Secrets:** three personnel logs and an unpowered observatory service lift. **Upgrade:** Mica's first programmable slot acquired near Workshop 09–12.

### Workshop extension, Missions 09–16
Existing 128×24 tile workshop with 8 missions. Extend as a **new connected annex**, not a third copy of four identical console bays. Plan two distinct wings: queue-and-conveyor hall (09–12) and supervisory foundry (13–16); moving conveyors, safe robot rails, overhead gantries, emergency stop and observably different machine states. Each wing houses four distinct programming encounters and one optional efficiency side challenge. Maintenance return shortcuts open after mission 12 and 16. The boss shows all four production lines, not a single green rectangle.

### Algorithm Tower, 16 missions
Design one tall research tower with 4 conceptual floors (four missions each): storage/search, network exploration, routing and scheduling, boss network core. Vertical movement should be legible: elevator animation, floor signage, sky view changes, saved elevator access. Each floor contains at least one *walkable* algorithm visualization. BFS reveals tiles, Dijkstra actually changes a drone route, topological ordering lights dependencies. Tower's final relay is the natural launch key for Orion. Map proposal: four linked `32×24` authored maps using existing world map contracts, or a single logically partitioned `64×64` with camera and elevator triggers; choose based on tests and performance.

## World 2 — Orion Relay Moon
**Identity:** lonely, atmospheric lunar expanse, irregular regolith, elevation bands, relay dishes, mineral seams, moving rover tracks, sky silhouettes. **Core verbs:** explore/scan, program routes, recover payloads, reroute around terrain hazards. **Landmarks:** shuttle pad, crater overlook, abandoned mining outpost, ice tunnel, radiation ridge, convoy bay. **World change:** dormant dishes rotate and transmit, mining lamps return, rover traffic grows, an alternate path opens. **Secrets:** one missing expedition manual page near a disguised crater wall, one research sample behind an efficient route (accessible without a strict optimization gate). **Music:** sparse windless low ambience and machine beeps; no constant loud percussion.

### Flagship detailed encounter: Relay Outpost Rescue (production benchmark)
**Goal:** implement one memorable 15–25 minute story episode *using existing Orion 01–16 without renumbering or retesting them as new missions*. Optional side contracts exist outside mission XP.

**Map planning:** 80×48 tiles is existing Orion size; reserve a north-west outpost vignette roughly x=5..28, y=4..19, connected by accessible track to current mission consoles. Include shuttle arrival, a visible damaged relay beyond locked hatch, a deploy station beside traversable route, two scanning nodes, optional archive under overhang, feedback beacon. Every interactable x/y must be checked for solidity and reachable via pathfinding from spawn.

**Episode beats:**
1. On entry, show a 2-second skippable arrival panorama ending on the remote relay; ION mentions disrupted transmissions once, not every visit.
2. Player walks across landmark path, hears intermittent ping near fault, sees Mica hovering by disabled relay.
3. `E` inspects broken console; `O` shows local diagram in a dedicated screen (never opaque rectangle overlaying terrain).
4. Guided `plan(observation)` returns bounded `scan`, `move`, `interact`. Render trace on nearby device before deployment; show walls and energy clearly.
5. Successful deployment lights first beacon; player physically follows newly opened corridor.
6. Add a new blocked tile / changed energy budget as a *transfer* variant. Player edits saved program, not restart from scratch.
7. Optional cave holds a discoverable engineering-manual page and spare cosmetic rover trail; main progression never requires hunting it.
8. Power restoration retracts a hatch, emits small particle burst + distinct sound and changes night-light silhouettes; optional replay can demonstrate alternate routes.

**Exit criteria:** From fresh preview save a player can find this encounter without pressing an undocumented hotkey; run genuine Python; watch Mica move with collision; find a log; return to shuttle; reload to retain states. Render/test at 1280×720,1600×900,1920×1080, at least 2 camera positions per area. Target reliable 60 FPS on baseline developer machine, measure rather than claim in advance. Full passage must be possible with keyboard alone.

## World 3 — Titan Cloudworks
**Identity:** industrial airborne platform, stacked antenna farms, pipework, moving cable-car, warm copper and deep cyan emissive packet trails. **Core verbs:** trace transmissions, route virtual packets, configure retries, synchronize message queues, recover failed network links. **Landmarks:** landing dock, ingress gate, broker hall, server spine, antenna deck, storm-control core. **Unique mechanic:** packets travel visibly across short conductor segments, with color-coding for delivered, buffered, dropped, invalid. **Secrets:** encrypted (fictional) maintenance note unlocked by a small string-matching program. **Boss:** recover a storm-failed broker grid with duplicate suppression and backpressure, phase-by-phase persistence.

## World 4 — Helix Biomedical Campus
**Identity:** bright lab corridors, translucent cultivation windows, instrument carts, sealed observation suites, synthetic signal monitors. **Core verbs:** acquire sample, inspect signal, code filtering/validation, diagnose faults, operate a synthetic live display. **Landmarks:** arrival atrium, sample clock room, filtering suite, multi-channel monitoring bay, acquisition control. **Unique mechanic:** interactive signal workstation supporting channel toggles, cursor measurements, play/pause, quality flags and controlled noise injection. **Secrets:** experiment notebook on calibration choices. **Boss:** restore an entirely fictional synthetic multi-channel acquisition system; no medical decisions.

## World 5 — Aurora Mapping Observatory
**Identity:** dark chamber dome, luminous vector grid, floating mesh displays, telescopes, white/pink accent lighting. **Core verbs:** inspect coordinate systems, move toy mapping probe, accept contact samples, create voltage/LAT fields, validate spatial pipeline. **Landmarks:** coordinate bridge, geometry lab, point collector, chamber renderer, observatory control core. **Unique mechanic:** rotatable simplified 3D chamber mesh *inside a dedicated workstation interface*, with point-picking, false-color toy fields and inspectable algorithm traces. Avoid claiming clinical accuracy. **Boss:** integrate deterministic toy map reconstruction, provenance audit and two data modes; player sees a complete map bloom across mesh.

## Final World — Mission Control Annex
**Identity:** the station's largest operations room, glass observation deck showing connections to restored worlds, emergency shutters, redundant command nodes, large but diegetic status displays. **Core verbs:** schedule systems, resolve dependencies, manage failures, replay event logs, run tests and watch the network come alive. **Landmarks:** integration bridge, scheduler rail, backup controller pod, event replay theater, central restore hub. **Boss:** four persistent phases: load/validate → coordinate → inject fault/recover → final transmission. Each phase uses an independently tested Python system; includes safe restart checkpoints and a skippable original finale.

## Multi-world travel design
From any approved travel terminal or `T`, open star map. Each destination card displays `visited / accessible / locked`, a brief environment description, unlock requirement and in-world feature. Selecting a world begins a fast 3–5 second optional departure animation: station door → ship silhouette → travel art motif → world-specific arrival; any key skips entire transition; reduced-motion instantly changes scene with static place card. Do not require a click on a tiny planet icon or advanced knowledge of `D` preview. Respect saved zone local checkpoint, and return to hub at known safe entry if previously saved tile is blocked. No enemy/hazard updates while travel overlay is active.

## Spatial design rules
- Never spawn behind a collider or on a prop with an interaction collision footprint.
- Visual props never obscure code entry points or mission prompts.
- Visible path to next critical objective, using gold marker on HUD and world-space waypoint only when helpful.
- Interactive status lights communicate inactive / ready / busy / restored, including non-color cue.
- Areas should have foreground/midground/background layer variety, varied negative space and a landmark at least every ~1–2 camera widths.
- Systems remain explorable after completion, with changed NPC behavior and visual state.

# 05 — Visual, audio, UX and accessibility production standard

## Goal
Move v1.4's improved procedural visuals into a **cohesive original pixel-art adventure** without smothering scenes in HUD. Design references are CrossCode (exploration clarity), Eastward (lived-in environments), and Opus Magnum (legible execution replay), but no art or layouts are copied. Visual upgrades must explain the world or affect play, not merely increase decoration density.

## Canvas and camera
The current native game draws into a 768×576 world viewport, with UI alongside, using 32-world-pixel tiles. Keep a stable logical canvas and scale the complete frame uniformly (integer scale when possible); letterbox intentionally instead of stretching. At native 1280×720, 1600×900 and 1920×1080 ensure no clipped labels, overlapping mission cards or unreadable text. Treat viewport, sidebar and popups as separate bounding boxes. World sprites are depth-sorted by foot position; foreground objects may mask actors only when still visually legible. Interaction focus lives on world object silhouette rather than giant rectangle.

## Visual language
- **Pixel proportion:** core 16×16 art grid enlarged to current 32px tile or matching sprite 2×; avoid inconsistent nearest-neighbor and antialiased edges. Some silhouettes span 2–3 tiles; grounded shadows maintain perspective.
- **Value hierarchy:** each world has one dark floor value, one mid surface, one brightest accent; animated signal points use accent sparingly.
- **Terrain:** 4–8 repeatable floor variants per biome, edge/corner tiles, collision silhouette, dirt/wear overlays, shadows and interactive landmarks. Generated noise must not become uniform static.
- **Props:** crates, panel banks, lamps, signs, pipes, screens, cables, walkable tracks, rubble, antennas; every prop has an unambiguous collision footprint and a clear role.
- **Lighting:** cheap deterministic radial masks or precomputed overlays on a separate transparent surface, limited to a few relevant emitters; no expensive per-pixel real-time shaders. Reduce intensity in accessible contrast mode.
- **World changes:** on successful program, persist the *art state* (repaired pipes, spinning dish, relit plant beds, signal arcs) rather than just the mission checklist. No restored terminal visually looking broken.
- **Animation:** player 4-direction 4–6 frame walk; 2-frame idle/breath; robot 2–4 frame motor/blink; door 4-frame retract; console 4-frame scan; relay dish ~8-frame cycle; environment indicator ~2-second calm loop. Reduced-motion offers static alternate states for all.

## Palette specification (original choices, adjustable after screenshots)
| World | Base dark | Mid | Accent primary | Accent secondary | Material motif |
|---|---|---|---|---|---|
| Astra | `#0B1D28` | `#28465A` | `#63D6C8` | `#F6B96C` | metal, service grates |
| Workshop | `#1A2330` | `#52626F` | `#F2B56D` | `#9CDDD1` | orange machinery, sparks |
| Orion | `#1A1A32` | `#515073` | `#C7B6FF` | `#F2C378` | lunar regolith, ion lamps |
| Titan | `#1D2630` | `#455A64` | `#FFB369` | `#47D5DE` | servers, copper wires |
| Helix | `#112A30` | `#467477` | `#85E0C9` | `#EFBF7E` | glass, instruments |
| Aurora | `#121B32` | `#48547C` | `#F09CC8` | `#89D3FA` | domes, holographic mesh |
| Mission Control | `#111F2E` | `#354E62` | `#E5CA8C` | `#74C4E2` | command glass, multiple networks |

Colors alone never encode critical information: use shapes, symbols, animation or text labels to denote validity/failure/accessibility.

## Interface architecture
### Explore HUD
- Left ~70–78%: unobstructed world. Right sidebar: 1 objective, 4 local missions maximum, XP, relevant tool status, one communications line. Longer mission descriptions open journal, never spill over HUD.
- Top: location breadcrumb + destination title. Bottom: controls shown only for available actions, context-first.
- Nearby interaction: short label `E Inspect Relay` near feet/target, only closest viable target, no screens of translucent text.
- Objective waypoint: offscreen gold diamond + distance; offscreen marker always clamped within viewport. Accessible `M` local map and readable unlocked destination labels.

### Code editor
- Split code and test area with adjustable divider. Keep input width sufficient for 88-character Python lines where practical; wrap long instructional prose, not code without explicit user preference.
- Header states exact function signature, tool context, time limit and examples.
- Error state: red line highlight and concise test diff, observed vs expected, next hint gated by player action. Avoid overwhelming learner with raw Python stack traces when they only need the culprit line.
- Ctrl+Enter to test, Ctrl+S to save, F1 hints, F2 twice confirmed reveal; existing interactions preserved.
- Program-library tab lists verified scripts and draft versions; source comparison plus 're-run tests' is accessible without traveling to original mission.

### Diagnostics / maps
- Dedicated screen/panel when `O` is pressed near a device; never a 400×400 opaque rectangle permanently over terrain.
- Generic diagnostics support device label, schematic, status, past trace and next action. Domain widgets add packet oscilloscope, numeric graph, 3D toy mesh or path overlay.
- Provide tooltips + keyboard selection for every diagram; animation and chart motion can be paused.

## Effects as feedback, not noise
- **Code accepted:** short audible chord, small local spark cluster near device, focus on changed world object, no full-screen confetti.
- **Code rejected:** gentle denial tone and terminal line highlight, not flashing red whole screen.
- **Unlocked path:** mechanical retract with a brief camera look if safe, skippable.
- **Major boss:** 2–4 state transitions, environment visible at each stage, distinct restore sound and cutscene skip.
- **Travel:** recognizable silhouette/motif, brief motion; can be bypassed.
- **Audio target:** two-channel mix for music/effects + volume controls; platform-independent generated short tones acceptable for first cut, optional composed loops later. No licensed music copied from existing games.

## UI/UX quality gates
- No obstruction of actors or core objects in normal exploration.
- No mission title, controls, scroll content, dynamic result or error text clipped in any supported resolution and font preset.
- Keyboard navigation complete; mouse coordinates correctly letterbox-transformed.
- Reduce-motion, screen-shake toggle, sound controls, high contrast, at least three text sizes.
- For color blindness, success = green + checkmark, failure = warning icon + text, locked = closed icon + explanatory label.
- 72 screenshots: baseline 6 representative world views × 3 resolutions × 2 camera/player positions; add run states like active Mica path, after-repair, editor and travel. Save screenshots with predictable filenames; compare before/after visually.
- Minimum animation performance measured on target baseline machine; cap particle counts/onscreen emitters and cache sprites/tile layers.

## Art production priority order
1. One polished Orion landmark scene, associated sprites, readable 2D camera and code effect.
2. Shared actor/robot sprite atlas and interactive prop states.
3. Consistent distinct world tile/edge libraries.
4. Boss/transit unique visual motifs.
5. Audio and optional portrait art.

`assets/ASSET_MANIFEST.csv` lists proposed reusable assets with locations, states and acceptance requirements. Generate original source art or commissioned/licensed assets only; document license/provenance.

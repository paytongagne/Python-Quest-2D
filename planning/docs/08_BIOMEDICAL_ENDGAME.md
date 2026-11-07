# 08 — Helix & Aurora: synthetic biomedical engineering endgame

**Stage:** Complete preproduction specification; **baseline:** Python Quest 2D v1.4 (76 playable missions); **scope:** Helix 05–16 and Aurora 05–16, 24 proposed missions; **date:** 2026-11-06. **Status:** design-only; not implemented in the game.

## 0. Purpose and strict scope

Helix and Aurora should feel like an original interactive engineering game, not a clinical training tool or a themed LeetCode list. They teach acquisition pipelines, deterministic simulation, quality control, coordinate transformations, spatial interpolation, and practical software integration. They use only synthetic, fictional observations and a toy chamber that cannot plausibly be treated as patient anatomy. No real devices, proprietary algorithms, patient files, diagnostic advice, medical decision support, or ablation simulation are in scope.

Public background informing **concept categories only**: Medtronic's product page describes ECG/intracardiac-electrogram displays, catheter visualization, and multiple mapping formats; its September 30, 2026 announcement describes Prism-2 mapping and beat matching. These do not describe implementation internals. Our simulator must not claim to reproduce Affera internals, performance, metrics, clinical accuracy, or intended use. See references at the end.

**Primary quality bar:** a user can collect a fake signal, diagnose a fake acquisition fault, manipulate a fake catheter on a toy 3D surface, write and debug Python transforms, then watch their verified computation produce a visible, explainable map. They understand how data travels through components and can reproduce the result after restarting the game.

### Relationship to v1.4 (preserve all)

Existing IDs remain exactly `helix_bio_01`–`helix_bio_04` and `aurora_ep_01`–`aurora_ep_04`; they are already included in the 76-mission baseline. The first four Helix exercises cover a repeating toy pulse, exact sample clocks, linear baseline estimation, and deterministic toy noise. Aurora 01–04 cover sample records, coordinate interpolation, 3×3 transformations, and contact/confidence filtering. **Do not replace these IDs, inputs, examples, effects, or XP.** Add missions 05–16 with compatible `kind=function`, `simulation=expedition`, `output=model` when feasible; only add new typed device-action outputs if the independent worker and parent validators support them. `world_effect` must be unique and present, because v1.4 `award()` expects it. Renderer and saved profiles stay compatible with schema 4 unless a separately tested additive migration is unavoidable.

## 1. Experience flow and narrative

### World identity: Helix Biomedical Campus

- **Mood:** low-light research lab where scientific instrumentation needs restoration, not a hospital. Background movement: moving cable gantries, blinking sample clocks, relay cooling vents, low-amplitude wave traces. Color: dark graphite, blue/cyan status, amber faults, mint recovery; always pair colors with labels/icons.
- **Exploration loop:** enter calibration foyer; look through a window at garbled instrument; inspect a damaged timing cabinet; consult ION's brief; adjust *physical* signal generator and probe settings; write short Python functions; observe traces on an in-world glass display; walk to quarantine bay to compare accepted and rejected samples; unlock research wing.
- **Interactables:** sample generator console, channel switcher, timestamp board, noise isolator, calibration rail, dual-clock bridge, gap detector, quality station, rolling buffer, diagnostic archive, acquisition core. Each named object has a world-space interaction prompt; only detailed traces live in an opened device view, never giant rectangles obscuring movement.
- **NPC:** CAL, a fictional lab technician with concise engineering dialogue. Dialogue focuses on sampling rates, reproducibility, data validity, not diagnoses. ION gives task-specific hypotheses and tests. No unskippable exposition.
- **World transformation:** noisy output and red/amber fault motifs at arrival; stable synchronized wave panels, revived corridor lighting, restored pumps after the boss; changes survive restart.

### World identity: Aurora Mapping Observatory

- **Mood:** precision geometry and data art. Exterior star observatory; interior 3D visualization dome, translucent guide rings, independently rotating toy mesh and light-field maps; dark navy and warm rose + teal accents, not a second Helix lab.
- **Exploration loop:** acquire a synthetic 3D point by positioning the game-owned probe; inspect surface/coordinate axes; write transform/quality/interpolation code; preview its scalar output; physically populate a simplified shell map; trace faulty points back to their recorded samples; complete a deterministic multi-stage map audit.
- **Interactables:** frame bridge, projection bay, neighbor locator, weight lab, activation clock, contact archive, topology editor, point-transfer station, beat-card gallery, cursor rig, packet intake, provenance desk, central dome.
- **NPC:** ECHO, observatory AI, acts as visual debugger: tells the player which source IDs fed the displayed vertex and how missing points change coverage. It does not invent medical interpretations.
- **World transformation:** wireframe-only shell to partially populated colored toy surface to dual-mode voltage/time complete display; saved after boss, optional replay toggle.

### Why the pair works

Helix answers **where do signal readings come from and how do we trust the transport?** Aurora answers **how do validated readings become spatial information?** Mission Control then asks whether the combined system remains correct under faults and restart. Establish the connection via a physical synthetic-data uplink after Helix 16; keep `Expedition Preview` optional during unfinished-chapter development.

## 2. Learning and interface boundaries

The signal chain is **SYNTHETIC GENERATOR → PACKET STREAM → VALIDATOR → CLOCK ALIGNER → QUALITY FILTER → FEATURE EXTRACTION → WINDOW DISPLAY**. The mapping chain is **SYNTHETIC POINTS → FRAME TRANSFORM → CONTACT VALIDATION → TIME/VALUE LAYERS → MESH INTERPOLATION → RENDERER → AUDIT**.

The learner authors an ordinary Python function against an immutable, plain-JSON fixture. `core/grade.py` runs the function in `core/worker.py` through the existing short-lived subprocess flow. For each test case, the worker compares outputs to canonical expectations or semantic validator; return a bounded JSON-safe result. **The Pygame process must never run learner-supplied Python in its event/render loop.** Independently validate the worker's serialized effect before state changes or XP. The current worker is not a hardened sandbox for malicious input; these exercises are local trusted practice and must not be exposed as a public execution service.

A device can be in `LOCKED`, `READY`, `TESTING`, `PREVIEW`, `DEPLOYING`, `RESTORED`, or `FAULT`. Wrong output causes `FAULT` in the preview UI but **does not damage persistent world state**. Only successful case tests **and** game-side postconditions advance the machine. Code source and failed attempts remain saved. Success generates a deterministic event trace and restores the interactable. Replay of saved result does not re-execute user code and never re-awards XP.

### Proposed interface shells (do not require Qt in the actual game)

The main release remains Pygame. Within the in-game instrument view, use a dedicated renderer for waveforms/geometry; no PySide6, network broker, external native math package, or clinical parser is needed to achieve these missions. However, teach the transferable Qt/QML architecture: a producer emits **plain data**, a queue/adaptor validates and applies changes, and the UI observes immutable snapshots. Qt's documented signals/slots and threaded delivery are comparison material in a lab manual, not a runtime dependency. A later optional standalone PySide6 extension can use this same `Frame` JSON contract if it is explicitly scoped and packaged separately.

## 3. Canonical fictional data model (version `toy-biomed-v1`)

These are **planning contracts**. Before implementation, content adapters and worker serializers must support them and acceptance tests must be checked in. All actual values are invented. Use `toy_units` instead of clinical units where possible; `ms` describes synthetic simulation time, not a clinical acquisition.

### 3.1 Common frame

```json
{
  "schema": "toy-biomed-v1", "source": "SYNTHETIC_ONLY",
  "channel": "SYN_A", "seq": 12, "time_ms": 48.0,
  "value": 0.25, "unit": "toy_u", "quality": "OK"
}
```

Required for accepted signal frames: `schema` exact, `source` exact, `channel` from a **fixture-declared allowlist**, `seq` nonnegative int (not bool), `time_ms` finite nonnegative number (not bool), `value` finite number, `unit` exact, `quality` one of `OK`, `ARTIFACT`, `MISSING`. A `MISSING` frame must use null `value`; use it as a gap marker rather than silently interpolating. Avoid adding real patient identifiers, geographic origin, device UIDs, or real date-of-birth. Unknown non-essential fields may be rejected in strict mission validation or discarded under a documented normalization policy; never accepted as executable instructions. Bound frame lists to ≤2,048 and result JSON to worker-defined size cap.

### 3.2 Mapping observation

```json
{
  "id":"MAP_004", "source":"SYNTHETIC_ONLY",
  "position":[0.0,0.5,1.0], "frame":"TOY_CHAMBER_V1",
  "voltage":1.5, "time_ms":112.0,
  "contact":true, "confidence":0.94, "channel":"SYN_A"
}
```

Geometry uses dimensionless **toy coordinates** and a consistent right-handed axis convention (`x` right, `y` up, `z` toward camera in the 3D view). Voltage is a **toy scalar**, not a real measured voltage. `time_ms` is fictional event time. Contact/confidence are explicitly game-defined booleans and numbers in [0,1], **not physiological validation**. Every observation references a unique ID and coordinate frame. Reject nonfinite coordinates/scalars and non-3D positions; deduplicate deterministically by ID when a mission specifies it. Do not infer a medical diagnosis from any scalar.

### 3.3 Toy mesh

```json
{
  "mesh_id":"CHAMBER_OCTAHEDRON_V1", "frame":"TOY_CHAMBER_V1",
  "vertices":[[0,0,1.5],[0,0,-1.3],[1.0,0,0],[-1.0,0,0],[0,0.9,0],[0,-0.9,0]],
  "faces":[[0,2,4],[0,4,3],[0,3,5],[0,5,2],[1,4,2],[1,3,4],[1,5,3],[1,2,5]]
}
```

This is an intentionally **non-anatomical octahedron-like closed toy surface**. Its topology is simple enough to audit manually. Vertex indices are zero-based. Every face has 3 distinct valid integer indices; reject degenerate triangles with near-zero area and out-of-range references. The first map pass uses this mesh; do not scope actual patient geometries, surgical anatomy or medical image reconstruction.

### 3.4 Numeric and deterministic rules

- Reject booleans where integers/floats are expected; Python's `bool` subclasses `int`.
- `math.isfinite` on every numeric input, coordinate, weight, timestamp and output.
- Distances in toy coordinate units; squared distances sufficient for sorting; no computationally expensive square root unless required by weighting.
- Floating equality: exact for integer/IDs/sequence and stable JSON structure; numeric tolerance `abs(actual-expected) ≤ 1e-8` for ordinary arithmetic, use explicit per-mission override for large summations. Do not compare image pixels as medical measurements.
- Deterministic canonical ordering: stable sort by `(time_ms, seq, original_index)` for frames, by `(distance_sq, id)` for nearest samples, by `vertex_index` for mesh outputs; document any exception.
- Reproducible samples use a fixed **local pseudorandom/integer deterministic** formula or seeded `random.Random(seed)`, never module-level randomness or wall clock. `i * (1000 / rate_hz)` avoids cumulative timing drift.
- Number formatting: preserve full finite values internally; round only at displayed UI boundaries unless a mission (e.g. existing Helix 04) explicitly requires rounded output.
- Missing observations are **missing**, not zeros. `None`/`null` is an explicit mask; invalid nonfinite values are rejected or quarantined, not silently drawn as NaN.

## 4. Synthetic signal generator and fault injection

Use the exact pre-existing v1.4 eight-sample template `[0, 0.1, -0.2, 1.0, -0.3, 0.2, 0.1, 0]` for continuity in beginner lessons. For advanced fixtures, use `SYN_A` as the template repeated at a fixed rate of 250 Hz; `SYN_B` is a time-shifted and attenuated copy with clearly documented coefficients. `baseline` is a deterministic, slowly changing additive trend. `noise` is a seeded bounded perturbation used to test filtering; do not claim a physiological distribution. For fault scenarios, inject `MISSING`, malformed values, repeated `seq`, out-of-order arrival, and paused devices. Store **event time** separately from **arrival order** so lessons can teach both.

**Required fixture suites:** `helix_clean.json` (two channels, 64 frames each, exact timestamps, no gaps); `helix_faults.json` (a shorter mixed arrival stream including duplicate, out-of-order, missing, and malformed examples); `aurora_toy_chamber.json` (six-vertex octahedral shell, valid and rejected observations, toy voltage/time scalars); `biomed_contracts.json` (schema, policies and limits). The provided generator under `reference/` is deterministic, pure Python stdlib, has a comment explaining *synthetic-only* usage, and is validated by `tests/test_biomed_planning.py`. Work should migrate fixtures into game content only after implementing worker/test adapters.

### Signal visualization

Draw clean and noisy traces as two or three *contained* viewports within the device UI. For a viewport with width `W`, height `H`, x pixel = `(sample_index / max(1, N-1)) * (W-1)`; y pixel = `center_y - clamp(value/display_scale, -1, 1) * (H/2 - padding)`. Render discontinuities as **gaps** on missing/invalid points; never connect across absent data. x ticks labeled synthetic `ms` when timestamp known, otherwise `sample index`. Cursor reads channel, index, event time, value, quality, not a diagnosis. Overlaid trace uses different line patterns or labels in addition to colors; avoid clutter and occlusion of game view. World-facing display uses mini waveform; detailed controls appear only upon interaction.

Controls: `Space` pause/resume; `Left/Right` scrub samples in dedicated view; `Tab` channel; `V` raw/processed visualization; `I` inspect sample; `Esc` close. Reconcile with existing game keys and editor before binding. Reduced motion disables animated sweep but keeps static trace and sample navigation. On deployment, animate the trace readout from synthetic event records, not a pre-authored fake success. Under 720p, all controls are visible without text collision.

## 5. Exact learning and grading policy: Helix 05–16

The function names below follow `missions/mission_blueprints.psv`. The corresponding `missions/biomed_24_contracts.csv` records the one-sentence objective and hidden-case areas. These refinements resolve ambiguities **before** Work begins coding. All errors use documented `ValueError` or typed failure output where runtime graders permit; avoid an ambiguous mixture of silent coercion and exception for the same input shape.

| ID | Signature / expected semantic contract | Main physical effect | Essential edge tests |
|---|---|---|---|
| HEL-05 | `normalize_trace(samples)`: min-max scale finite numbers to [0,1]. Empty `[]`; constant nonempty → all zeroes. Non-mutating. | Calibration rails stabilize and raw/normalized traces appear side by side. | negative values; constant; empty; nonfinite reject; immutable input. |
| HEL-06 | `moving_average(samples, window)`: trailing mean of last at most `window` values; prefix uses available count. `window>=1` integer. | Second filtered oscilloscope trace unrolls. | `[1,3,5],2 → [1,2,4]`; window larger than list; invalid window; no mutation. |
| HEL-07 | `find_peaks(samples, threshold, distance)`: interior strict maxima with amplitude ≥ threshold; plateau rejected; choose strongest within minimum index separation, ties choose lower index; return ascending indices. `distance>=1`. | Mechanical ruler moves to each detected **toy** peak. | endpoints; plateaus; equal heights within spacing; exact threshold; nonfinite. |
| HEL-08 | `repair_timestamps(samples, interval_ms)`: each item becomes `{index, time_ms, value}` with `time_ms = index * interval_ms`; input `None` denotes missing and stays null. | Sweep clock locks to a regular reference. | fractional interval, missing, empty, zero/negative interval, no iterative drift. |
| HEL-09 | `align_channels(a,b,tolerance_ms)`: validate finite timestamps; stable sort each by `(time_ms, original index)`. Greedily pair each A to closest **unused** B within inclusive tolerance; tie → earlier B timestamp, then original B index. Return tuples/JSON arrays with IDs or values as specified by in-game fixture. | Two channel traces align on twin monitors. | equal-distance ties; repeated timestamps; no pair; mismatched lengths; tolerance boundary. |
| HEL-10 | `missing_sequences(events)`: take nonnegative integer `seq`s, ignore duplicates, return sorted missing ints strictly between observed min/max. | Dashed trace gaps become visible; missing packet indicators update. | nonzero offset, duplicate, unsorted, empty, max gap cap, bad type. |
| HEL-11 | `quality_report(samples, flags)`: equal lengths; flags are booleans; report total/clean/artifact/missing and clean_mean (`null` if none). `None` sample is missing, not zero. Flagged nonmissing sample = artifact. | Instrument badges show quality with textual count. | all missing; length mismatch; nonfinite sample; empty; high/low range. |
| HEL-12 | `stream_windows(samples,size,step)`: only **complete** windows; positive int size and step; preserve original sequence and values; no partial tail. | Rolling oscilloscope updates one window per tick. | short input; overlapping; zero step; size>length; no mutation. |
| HEL-13 | `fault_timeline(events)`: events of `{device,type,time_ms,seq}` sorted by time then seq; each `OFFLINE` opens interval, `ONLINE` closes it, repeated status ignored, open-ended outage remains `{end_ms:null}`. | Fault light and timeline synchronize during replay. | duplicated state; equal-time events; unknown device; never recovered; unrelated devices. |
| HEL-14 | `validate_frame(frame)`: strictly normalize a synthetic signal frame (common schema above); reject missing/invalid values or strings masquerading as numbers; allow `MISSING` only with null `value`. | Invalid frames enter visible quarantine chute; valid frames continue. | bool-as-int, negative seq/time, unsupported channel, nonfinite, unknown schema. |
| HEL-15 | `monitor_pipeline(frames,capacity)`: deterministic simulation: group by integer `arrival_tick`; enqueue in given arrival order into capacity-bound FIFO; **drop newest** when full; process max one frame at the end of each tick and drain after arrivals finish. Validate before accepting; return processed/invalid/dropped/peak_queue counts and output seq list. | Live conveyor carries accepted packet icons; drops trigger readable alerts. | bursts; invalid frame; duplicate sequence policy; capacity=0 invalid; deterministic replay. |
| HEL-16 | `restore_acquisition(channels,events,policy)`: integrate validation, regular clocks, windowing, quality summaries, and fault report into a deterministic plain-data acquisition summary; explicit success predicate for calibrated channels. | Two-stage lab restoration; faulty instrument reboots; calibrated display persists. | mixed channel rates; missing frames; restart; no accepted frames; invalid policy; idempotent completion. |

**Critical semantic detail HEL-09:** Because blueprint signature does not specify frame field names for return, Work must freeze an exact contract in the mission JSON *before* authoring expected fixtures. Suggested return: list of `[a_id,b_id]` pairs; require input records to carry `id` and `time_ms`. No hand-wavy expected values.

**Critical semantic detail HEL-15:** A deterministic simulated tick must not depend on Pygame frame time. Buffer overflows should be possible through multiple arrivals at the same `arrival_tick`; one-per-tick arrival would never meaningfully exercise capacity.

## 6. Exact learning and grading policy: Aurora 05–16

| ID | Signature / expected semantic contract | Main physical effect | Essential edge tests |
|---|---|---|---|
| AUR-05 | `project_point(point,axes)`: axes = two unit, orthogonal 3-vectors; return dot(point, axis_x), dot(point, axis_y). Reject nonfinite/bad basis. | 3D toy probe projected onto a 2D grid. | rotated basis, origin, nonorthogonal axes, wrong dimensions. |
| AUR-06 | `nearest_samples(query,samples,k)`: consider samples satisfying explicit contact/quality gate; return IDs sorted by squared Euclidean distance, then ID. `k>=0`, `k=0 → []`. | Nearby sample halos illuminate in a deterministic order. | tied distance, no valid samples, k>count, duplicate ID, nonfinite coordinates. |
| AUR-07 | `interpolate_voltage(query,samples,power)`: inverse-distance weighting (IDW) over valid synthetic samples: `Σ(v_i / d_i**p) / Σ(1 / d_i**p)`. Exact location uses exact sample voltage; power>0. | Toy voltage field fills map, with provenance on click. | zero distance, zero/negative power, no eligible samples, extreme distances, finite output. |
| AUR-08 | `activation_map(samples,reference_ms)`: for each accepted sample, return `{id, lat_ms:time_ms - reference_ms}` in original order; negative LAT allowed and labeled. | Activation-time color layer becomes selectable. | before reference, duplicate ID, no samples, nonfinite time. |
| AUR-09 | `valid_contact_samples(samples,policy)`: preserve input order; gate `contact is True`, finite `confidence>=policy.min_confidence`, within [0,1], matching frame. | Rejected point glyphs fade, accepted ones lock onto mesh. | inclusive threshold, absent metadata, wrong frame, nonfinite, false boolean. |
| AUR-10 | `mesh_neighbors(faces,vertex_count)`: **revised signature** required; return dict of each vertex index including isolated vertices, with sorted adjacent vertex indices. Reject bad indices, duplicate degenerate vertices and near-zero-area triangles at mesh validation stage. | Edge network highlights around selected mesh point. | isolated vertex, invalid index, repeated triangle, empty mesh, degeneracy. |
| AUR-11 | `color_vertices(vertices,samples,radius)`: IDW from eligible samples **within** radius; exact point exact value; out-of-range vertex returns `None`. **Revised output type `list[float|null]`** required. | Surface coverage appears only where supported; unmeasured region remains hatch/shaded, never colored as zero. | no neighbors, exact hit, radius boundary, zero radius, bad contact. |
| AUR-12 | `group_beats(beats,tolerances)`: sort by `(time_ms,id)`; compare feature vector to first beat/anchor of each existing group; join first matching anchor (per-feature absolute difference ≤ tolerance); else new group. Groups returned as list of ID lists. **Toy pattern groups, not clinical beat classification.** | Similar synthetic beat cards cluster with trace previews. | nontransitive similarity, missing feature, equal values, zero tolerance, order. |
| AUR-13 | `update_cursor(state,events)`: apply bounded `MOVE` vector, `ROTATE` basis, `RESET` operations in sequence to toy probe; return canonical position, orientation and frame. | 3D probe animates along recorded trajectory. | reset after move, invalid rotation, out-of-range move, duplicate events. |
| AUR-14 | `map_stream(events,limit)`: stable event-time sort after validating arrival, drop duplicate observation IDs after first valid, bound queue to `limit`; emit accepted ordered IDs, rejected reasons and counts. | Samples bloom on mesh with event log synchronized. | out-of-order arrival, duplicate, overflow, malformed, restart. |
| AUR-15 | `audit_session(session)`: verify synthetic provenance, unique IDs, mesh references, timestamp monotonicity after sorting, coordinate-frame consistency and counts. Return `pass`, `problems`, `counts`. | Diagnostic overlay marks exact failing surface point or event. | empty session, wrong frame, duplicate IDs, mismatched mesh, gaps, invalid source. |
| AUR-16 | `rebuild_map(mesh,signals,samples,policy)`: validate; filter accepted points; compute toy voltage and LAT per mesh vertex; produce `{coverage, voltage_layer, lat_layer, provenance, audit}` in strict schema. No display mutation until audit success. | Four-step map boss: calibrate → collect → color → audit; map remains restored after restart. | out-of-order, sparse coverage, degenerate mesh, all filtered, replay deterministic. |

**Two necessary blueprint corrections:** Current `mission_blueprints.psv` proposes `mesh_neighbors(faces)` and `color_vertices(...)->list[float]`. The former cannot report isolated vertices without an explicit `vertex_count`; the latter cannot distinguish unmeasured territory from measured zero without a missing-value representation. This stage therefore records intentional revised design signatures for AUR-10 and AUR-11. Update future authored mission data consistently; **do not silently alter shipped content**, which does not include these IDs yet.

### Aurora interpolation policy (must be explicit in the player's lab manual)

For a sample at distance `d<=1e-9` of a query point, return the exact coincident sample value; duplicate coincident samples with conflicting values are an invalid fixture unless aggregation rule is explicitly specified. For other samples, IDW weight = `1 / max(d,1e-9)**power`. Define `power=2` in all default exercises; alternate values are tested within [1,4]. Use eligible samples only. No samples: `None` for vertex coloring, error for function expected to compute a point scalar in AUR-07. Missing values are displayed with a checkered neutral overlay, **not invented continuous data**. IDW is a simple educational technique and makes **no claim** about anatomical signal reconstruction.

### 3D workbench interaction specification

The 3D dome is a *dedicated UI mode* with mesh viewport left and a narrow inspector right, not a giant panel drawn across the walking world. Mouse drag rotates yaw/pitch; wheel zooms with bounded range; arrows rotate for keyboard-only; `1` voltage layer, `2` synthetic activation layer, `3` coverage mask; `Tab` cycles vertices/samples; `I` inspects provenance; `R` replay; `Esc` exit. Every control is shown in on-screen help and remappable when global controls are implemented. All transforms in **the view** affect camera only; learner-returned world coordinates remain in one canonical mesh frame. Store current display mode and camera defaults separately from puzzle success data. A map update is fed from a verified serialized layer object, not an arbitrary Python-drawn image.

### Toy 3D projection algorithm

No heavy renderer dependency is required. Project each vertex `p` after camera rotations R_yaw and R_pitch using `screen_x = cx + scale*x_rot`, `screen_y = cy - scale*y_rot`. Draw back-facing triangles or depth sort by average rotated z for a simple CPU implementation; assign triangle shade from face normal and one fixed display light direction. Keep vertex rings/points legible; use a translucent outline when selected. Clamp pitch and zoom; check for backface artifacts. For a more accurate later renderer, change only view-layer implementation, not the synthetic data schema. Avoid medical imagery that could be mistaken for a real patient map.

## 7. Curriculum pacing and encounter design

### Helix sequence (every four missions visibly changes a subsystem)

- **05–08: Calibration gallery**. Player sees unstable wave traces, normalizes values, implements a filter, detects toy peaks, and repairs event-time ticks. Reward: calibrated oscilloscope, inspectable cursor and a restored maintenance walkway.
- **09–12: Streaming wing**. Player aligns two channels, identifies sample loss, builds quality summaries, and feeds windows to a stable visualization. Reward: synchronized displays and telemetry archive access.
- **13–16: Incident room + boss**. Player correlates fault logs, validates each incoming frame, builds bounded producer/consumer pipeline, then restores acquisition in two stages. Reward: permanent uplink to Aurora, restored lab ambience and a new synthetic sample reference manual.

### Aurora sequence

- **05–08: Geometry/probe lab**. Project 3D points into views, identify nearby observations, interpolate a toy voltage scalar, compute reference-relative times. Reward: active point collector and two togglable scalar layers.
- **09–12: Quality/topology gallery**. Gate contact samples, construct adjacency, transfer values onto vertices, group synthetic signal cards. Reward: mesh inspection tool, hatched unknown regions and beat-card cabinet.
- **13–16: Map control core + boss**. Track synthetic cursor, consume and deduplicate point stream, audit provenance, then rebuild map through staged deterministic checks. Reward: completed fictional observatory visualization and route to Mission Control.

### Make lessons increasingly hard, not opaque

Each chapter starts with visible examples and optional first-principles explanations, then shifts to independent functions, unfamiliar transfer fixtures and multi-stage integration. The player should have to decide where to use `dict`, `set`, `deque`, sorting, state machines and immutable records. Avoid testing undocumented APIs or forcing one exact source-code pattern when multiple correct approaches exist. At least two late-game mission briefs ask for an optional first-person explanation of approach and expected Big-O, then let players inspect replay traces to verify their reasoning.

## 8. Visual and interactive device acceptance criteria

1. **World readability:** player can identify a current device, next landmark, restored region and return route without reading developer instructions. No giant permanent map overlay; nearby `E` prompt only when in reach.
2. **Meaningful cause/effect:** change in signal processing yields a changed trace, metric or explicit device state; change in point selection yields changed geometry coverage; if inputs differ but renders look identical, highlight which values were intentionally equivalent.
3. **Correct uncertainty:** gaps in sensor data and unmeasured mesh vertices remain visibly unmeasured; errors and warnings include a text label, not just red/yellow color.
4. **Durable progress:** validated synthetic lab restores are recorded as world effects; completed tests and phase state survive restart; no repeated XP from replay.
5. **Screens:** review 1280×720, 1600×900 and 1920×1080; ensure terminal text isn't obscured, signals have axes/legend and map controls are within the viewport. Dedicated code editor never loses focus to shortcuts bound for planet travel.
6. **Accessibility:** reduced-motion sweeps, scalable text, keyboard-only navigation, contrast checks, alternative text descriptions of waveform shape/peak count and 3D map extrema.
7. **Performance target:** steady ~60 FPS on typical Windows laptop for 64–256 displayed synthetic samples and a toy mesh of ≤512 vertices/1,024 faces; avoid unbounded per-frame geometry allocations. Cache static graph axes and background. These are *targets requiring measurement*, not verified metrics.
8. **Replay/step:** synthetic instrumentation has pause, step and replay. A replay's displayed trace hash and map data hash match the saved canonical result.
9. **No clinical affordances:** no treatment recommendation, no risk score, no patient UI fields, no operator instructions for real medical hardware. A visible `SYNTHETIC / EDUCATIONAL` label exists inside each advanced instrument view.
10. **Scenario truthfulness:** tests show observed vs expected output and one failing fixture; the UI does not mark a failed learner function as successful because a pre-authored animation plays.

## 9. Save, testing and crash strategy

Do not change schema 4 just to store a visual mode or cosmetic preferences. Add optional, namespaced keys, e.g. `biomed_lab_state` with validated `helix`/`aurora` sections and `schema_version:1`, plus world effect completion IDs. Never replace `completed`, `drafts`, `attempts`, `world_flags`, `programs`, `expedition_job` or unknown fields. Persist only canonical small results, hashes, view state and deterministic trace references, not megabytes of raw waveform frames. Regenerate synthetic fixtures from versioned seed and fixed algorithm when resuming. If any generator changes, bump its version and keep a compatibility fixture for old saves. Before changing migration logic, test legacy schema 2/3→4 and schema-4 roundtrips using disposable profile paths.

**Idempotent boss phases:** `CALIBRATE → COLLECT → VERIFY → RESTORE` in Aurora, each state saved after passing the real game-side check. A crash between stage save and visual animation restores the correct stage and replays visuals from deterministic snapshots. An invalid new run never unsets previously restored world flags unless the player explicitly enters a nonpersistent practice mode. No repeated XP.

**Test layers:** (a) fixture reproducibility and schema checks; (b) worker reference cases; (c) parent-side output validation, including maliciously malformed output; (d) mission/XP and save-compatibility tests; (e) headless simulated renderer state traces; (f) running-game screenshot geometry checks and keyboard walkthrough; (g) full campaign regression and Windows packaging.

**Explicit fault cases:** zero/negative sample rate or interval; nonfinite values; missing/duplicate/reordered packet; integer overflow-sized sequence gap; stale frame after an instrument reset; incompatible coordinate frames; exact/near-zero IDW distance; conflicting coincident observations; empty point set; invalid mesh reference; partial output JSON; user code timeout; game quit halfway through animation; rerun after completion; migration with unknown fields; 720p panel overflow; keyboard-only controls.

See `tests/biomed_acceptance.csv` for mission-by-mission acceptance scenarios and `reference/biomed_fixture_generator.py` for reproducible planning data.

## 10. Development handoff order and explicit gates

**Do not begin by implementing all 24 missions.** Their planned contracts support incremental sprints:

1. **Biome Foundation (no new missions):** build synthetic fixture loader/validator, viewport-contained signal renderer, toy mesh projector, canonical parent result guard, optional namespaced save state. Implement tests and screenshots. Do not change existing 8 missions.
2. **HEL-05–08:** implement calibration cluster and actual device-state changes. Gate: correct waveforms including gaps, all relevant unit/worker/parent tests.
3. **HEL-09–12:** implement channel alignment and streaming. Gate: deliberate packet drops and time skew visibly reproduce and diagnostics explain them.
4. **HEL-13–16:** implement deterministic pipeline and boss with saved phase checkpoints. Gate: crash/restart and bad input never reward success.
5. **AUR-05–08:** geometry, neighborhood and scalar fields. Gate: fixed mapping fixture renders equal canonical values across restart.
6. **AUR-09–12:** quality, topology, coverage/beat-card controls. Gate: unknown map regions remain unknown; two corrected blueprint signatures are adopted consistently.
7. **AUR-13–16:** interactive map stream and final boss. Gate: deterministic map layers, provenance readout, keyboard/reduced-motion, save restoration.
8. **Integration and release:** Mission Control cross-world contract consumers receive only validated toy snapshots; full mission regression and running Windows screenshots. Packaging is done at a stable milestone.

At every gate: save complete source, all fixture/version markers, user-visible changelog, and state summary with exact mission counts; do **not** count the 24 planned missions as implemented before they pass tests and are playable.

## 11. Interview and software-engineering transfer questions (optional in-game codex)

- **Why a sampling rate?** It defines the relationship between sample index and synthetic event time: `t_ms=i*1000/rate`. Explain why incremental `t += dt` can accumulate floating error.
- **Why distinguish missing from zero?** Zero is an observed scalar; missing means no valid observation. Treating both alike invents data and distorts display.
- **Why separate worker, game state and renderer?** Learner code may block or fail; parent-side validation and immutable data isolate it from UI responsiveness and prevent wrong world changes.
- **How do queues help?** Bounded FIFO decouples bursty producers from predictable consumers; make overflow policy explicit and test it deterministically.
- **How would a Qt UI fit?** A backend emits immutable validated snapshots; a queued signal/slot updates the GUI thread. Thread affinity and event-loop delivery need care; actual code stays in Pygame for this game. Source: official Qt for Python signals/slots docs.
- **Why use idempotency?** If a save/replay/restart repeats an event, a completion ledger and deterministic stage transition prevent duplicate XP and side effects.
- **Why choose IDW?** It's simple, transparent for teaching and easy to audit, but depends on distance and sample coverage and is not an accurate model of real tissue electrophysiology.
- **How to test visualization?** Unit test canonical layer arrays and hashes separately from screenshots, then verify rendered legend/gap markers/interaction manually and with image geometry checks.
- **What's a coordinate-frame bug?** Mixing positions from distinct origins/axes produces plausible-looking but wrong geometry. Require explicit frame IDs and transformations.
- **How do you test async without flakiness?** Make arrival schedules synthetic; process fixed logical ticks; assert event logs rather than wall-clock timing.

## 12. Source anchors and originality

- Medtronic Affera product overview (public feature categories only): https://www.medtronic.com/en-us/healthcare-professionals/products/surgical-energy/ablation/mapping-ablation-products/affera-mapping-system.html
- Medtronic Sept. 30, 2026 Affera Prism-2 public announcement: https://news.medtronic.com/2026-09-30-Medtronic-announces-regulatory-milestones-for-newest-cardiac-mapping-and-ablation-software
- Qt for Python signals/slots and threads: https://doc.qt.io/qtforpython-6/overviews/qtcore-signalsandslots.html and https://doc.qt.io/qtforpython-6/PySide6/QtCore/
- User-provided Python Quest v1.4 package (`content/expeditions/helix_bio_01..04.json`, `aurora_ep_01..04.json`, `core/worker.py`, `core/grade.py`, `game/expedition.py`, `core/progress.py`).

These sources motivate engineering *concepts*, not copying art, real patient waveforms, vendor UI designs, data formats, proprietary processing, or clinical workflows. The code, shapes, NPCs, labels and fixtures in this design are original. This is a fictional local programming game with **no medical use**.

## 13. Precise screen layout, coordinates and player walk-throughs

### Base-resolution layout contract

v1.4 currently renders to a **1088×690 logical canvas** and scales/letterboxes it into a resizable desktop window. The 3D/game-world viewport occupies approximately logical `(12,77,768,576)` with the right-side task HUD outside it. These numbers are actual source seams, not a proposal to resize the game.

| Component | Logical rect (x,y,w,h) | Constraints |
|---|---|---|
| World view, unchanged | (12,77,768,576) | Do not cover permanently with instrument graphs. |
| Right field sidebar, unchanged | x ≈ 796–1076 | Existing objective and status text must remain in normal exploration. |
| Detailed instrument overlay | (100,78,888,534) | Modal only upon interact; darkened world visible beneath. |
| Signal chart pane inside modal | (122,144,548,338) | Grid and axes cached; minimum two line patterns/labels; no text in data plot. |
| Signal details / channel selection | (690,144,270,338) | Quality, cursor, time, legend and fault context; scroll details, never clip. |
| Signal controls / error row | (122,499,838,90) | One active task hint, run status, pause/step/channel keys. |
| 3D mesh renderer inside modal | (122,139,548,357) | Clipped projection with mesh camera pan/zoom bounded to rect. |
| 3D inspector | (690,139,270,357) | Vertex/sample, units, source IDs, layer, contact quality. |
| 3D mode controls | (122,511,838,78) | Mode keys, legend, camera help, restore stage and exit. |

These are **initial layout targets**. Implement an anchored component geometry helper, not magic numbers in six different drawing functions. Use existing logical-scale-to-window mouse conversion; never mix untransformed physical-window coordinates with logical canvas coordinates. Run screenshots at 1280×720, 1600×900, 1920×1080, including the rightmost corners and scroll states. A modal must not overlap the code editor; opening an instrument from code mode is either disabled with text or deliberately replaces the view after draft persistence.

### Character-first playable scenario: Helix 05–08

1. Player enters a hallway where the oscilloscope trace jolts and the amber `CLOCK UNSYNCED` sign is visible. A wave generator makes an audible two-note synthetic chime, not a heartbeat recording.
2. CAL points to a calibration rail and offers two interactions: `inspect raw samples` and `restore normalization`; user sees exactly the values `[0,5,10]` in a tiny reference experiment, with a link to the longer hidden fixture.
3. User writes `normalize_trace`; wrong constant-case output receives a concise test failure. No electrical effect is awarded until all validation passes.
4. After success, rail lights turn mint, tracing line rescales within its viewport and the recovered rail physically opens a path to the next device. The status bar names the Python idea, rather than only showing XP.
5. User writes and tests `moving_average`; two traces are drawn together, and toggling `V` shows the raw/processed difference and a numeric cursor at selected index.
6. User finds a hidden maintenance note explaining why a peak detector should reject plateaus, then writes `find_peaks`. A 3D cursor is **not** introduced here; the physical oscilloscope ruler marks selected indices.
7. Timestamp repair re-aligns a synthetic sweep; CAL says why `i * dt` avoids accumulated drift. A shortcut corridor connects back to entrance.
8. Save/reload in the corridor, then revisit the normalization console: program, completed state and restored corridor remain; replay shows no new XP.

### Character-first playable scenario: Aurora 13–16

1. Player finds two sets of colored probe markers in different coordinate frames; ECHO highlights the chosen reference frame and refuses to mix the streams silently.
2. Player writes cursor update logic and physically drives the **toy** probe in the dome. Its path is a bounded synthetic trace, not a patient catheter.
3. Simulated sample packets arrive with deliberate reorder/duplicates. The player writes a deterministic intake function; rejected packets appear as labeled cards at the side, not invisible failures.
4. The player opens a provenance overlay and chooses a suspicious vertex. The UI enumerates source observation IDs, quality filters and interpolation weights that contributed to the toy scalar.
5. An audit fails because of a deliberately duplicated ID; the failing row and expected correction are shown. The world remains unchanged after the failed run.
6. Four boss phases each validate real learner output before saving. Between phases, the chamber visibly fills in; unknown regions remain hatched. Pausing mid-reconstruction and restarting restores the correct saved phase.
7. Success unlocks a *fully explorable* observation gallery with static dual-layer map review, an NPC interaction and optional replay/optimization side task. The mainline route advances to Mission Control without requiring clinical interpretations.

### Anti-boredom gate for each cluster

Before scaling 4-mission chunks, conduct an actual playthrough and answer: (1) Did the player do more than visit four identical code terminals? (2) Did two or more distinct world objects change visibly? (3) Did at least one task require inspecting the environment before coding? (4) Did the player have a discoverable return route? (5) Can the player explain a software concept rather than recite a memorized answer? A failing answer triggers a focused design correction before adding the next four.

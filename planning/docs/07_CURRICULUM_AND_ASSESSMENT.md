# 07 — Python learning curriculum and assessment design

## Audience and commitment
Begins at authentic Python fundamentals and eventually trains independent functions, OOP, data structures, algorithms, robust parsing, event-driven software, testing and numerical visualization. The existing 76 missions form the foundation. The next 76 should push the learner toward software engineering, without assuming every player wants heavy interview-style algorithms immediately.

## Campaign skill lattice
| Progress block | Missions | Main concepts | Demonstrated independent ability |
|---|---|---|---|
| Astra core | 24 shipped | prints, variables, types, branching, loops, strings, lists, dicts, simple algorithms, telemetry | complete short functions and scripts |
| Hydroponics | 16 shipped | rover plans, stateful repairs, simulation and validation | design bounded actions and understand result shape |
| Workshop | 8 shipped + 8 planned | classes, methods, properties, composition, exceptions, file IO, snapshots, tests | build reusable stateful components |
| Algorithm Tower | 16 planned | sets/maps/stacks/queues, binary search, BFS/DFS/Dijkstra/A*, topology, complexity | choose an algorithm, explain performance and validate routes |
| Orion | 16 shipped; retrofit optional transfer | navigation, graph routing, weighted paths, plan playback | adapt algorithms to changed maps, inspect action traces |
| Titan | 4 shipped + 12 planned | JSON, topic routing, queues, retries, event systems, async simulation, idempotency | make a robust network simulator under loss/duplicates |
| Helix | 4 shipped + 12 planned | synthetic sampling, timestamps, filtering, validation, windows, monitoring | process toy time-series streams correctly |
| Aurora | 4 shipped + 12 planned | geometry, coordinate transforms, toy interpolation, synthetic activation timing, mesh topology | assemble reproducible toy map layers |
| Mission Control | 16 planned | dependencies, event logs, concurrency models, fault injection, integration, regression | integrate and defend a multi-component software system |

## Standard lesson contract (one template for all 76 new missions)
1. **Discovery:** the player sees the problem physically before reading Python syntax.
2. **Brief:** plain-English input/output contract, exact signature, two small examples and at least one explicit constraint.
3. **Predict:** player predicts next state on a tiny fixture (optional for early missions, useful for debugging).
4. **Code:** genuine executable Python with optional starter stub. Advanced functions start with `pass`, not prefilled near-solution.
5. **Test:** deterministically check correctness on both visible and hidden edge fixtures. Never lie about a passed test.
6. **Diagnose:** show earliest failure, observed vs expected and which concept is relevant; preserve draft.
7. **Deploy:** a validated serialized result visibly changes a real device.
8. **Reflect:** optional 1-question `why did this work?` or complexity explanation; no essay required.
9. **Transfer:** an alternate fixture later requires the same idea with less guidance; no repeat mission XP.

## Hint ladder (three levels)
- Level 0: original objective + signature; no code supplied.
- Level 1: conceptual nudge ("Use a queue because neighbors must be explored in arrival order").
- Level 2: specific reasoning outline or pseudocode with omitted syntax; marks existing `hinted` completion XP at current 75 behavior.
- Level 3: intentional two-step confirmed solution reveal, retaining current 25 XP semantics. Store a review task encouraging an independent retry.

## Scoring and mastery
Keep original XP untouched. Optional `mastery` metadata tracks independent pass, hints, retries, new-scenario transfer and efficiency comparisons, but the story is not blocked by a lack of medals. Clear automated progress respects repeat-award=0. No leaderboard and no competitive pressure required.

## Assessment quality
- Visible examples illustrate, never exhaust constraints.
- Hidden cases cover empty, single element, duplicate IDs, missing fields, negative/zero, non-finite floats, boundaries, large-but-bounded and mismatched shapes where relevant.
- For graph problems, correctness means a legal, optimal result, not one exact path if ties are allowed. Define stable tie policy when exact canonical output is tested.
- For simulation, test both *model output* and *effect validation*. A return value that looks plausible but violates state rules must not unlock a system.
- For asynchronous/concurrency lessons, use deterministic simulated event order, not flaky real wall-clock races.
- For numeric toy models, publish units, rounding and tolerance. Avoid vague 'about equal' checks or pathological floating drift.
- For file tasks, fixtures are created under temporary directory and closed; never read arbitrary user files.
- Compare independent new variant without hint; if learner cannot transfer, offer scaffolded retry rather than harsh penalty.

## Personal learning outcomes and relevance to software engineering
- Explain code in natural first-person language before typing it: input, algorithm, expected result, time/space complexity when relevant.
- Debug by reproducing an issue with a small fixture, observing wrong data and reading an error trace.
- Recognize Python data model choices (list, dict, set, deque, heap), and choose based on access pattern.
- Understand object ownership and state isolation, especially in battery/robot tasks.
- Understand event-driven architecture, message ordering, bounded queues, synchronization, recoverability and tests.
- In the synthetic biomedical chapters, explain acquisition/processing/display boundaries and how to validate missing/corrupt samples without making clinical claims.

## Avoid superficial learning
Do not hand out XP for copying a displayed reference answer without confirmation and reduced award. Do not use enormous hints in first view. Do not teach `eval` or arbitrary `exec` as a normal student solution. Tests should check semantics, not whether a specific algorithm source substring appears, except for explicitly documented learning requirements such as use of a `with` statement for context management.

## Mission contract fields
`id`, `zone`, `sequence`, `kind`, `contract` if object/device, `title`, `story`, `objective`, `lesson`, `sample`, `function_name` (for functions), `starter_code`, `hint`, `cases`, `simulation`, `output`, `world_effect`, `difficulty`, `prerequisite`, `device_id`, `observed_result`, `additional_tests`. The first 14 mirror existing content patterns; new metadata may be loaded via optional accessors. Blueprints are *planning contracts*, not yet runtime-compatible JSON.

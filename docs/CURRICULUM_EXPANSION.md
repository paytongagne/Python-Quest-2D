# POST-LAUNCH CURRICULUM AND REAL-GAME MECHANICS

The first ship-repair campaign is 24 missions: four true beginner orientation scripts plus 20 migrated tasks. This document prevents the first release from becoming the full scope of the project. The extension mission set is a **planned backlog**, not implemented challenge files or completed tests.

## Four major learning tracks after the first campaign

### Track A — Python fluency (16 proposed missions)

1. Types and conversions: int/float/str and coercion pitfalls.
2. String slicing and indexing.
3. Truthiness and comparisons.
4. Nested conditionals.
5. While loop and sentinel values.
6. Loop break and continue.
7. List slicing and mutation.
8. List comprehensions.
9. Tuples and unpacking.
10. Sets and membership.
11. Dictionary traversal and nested maps.
12. Sorting with keys.
13. Function parameters and default values.
14. `*args`, `**kwargs` overview in controlled tasks.
15. Return versus print.
16. Multi-step independent Python mini-project.

**Zone concept:** The Hydroponics Station. The learner codes resource allocation, robot watering schedules, and sensor filtering while growing an animated indoor garden.

### Track B — Real Python software engineering (16 proposed missions)

1. Exceptions: try, except, else, finally.
2. Input validation and custom errors.
3. Module imports and organization.
4. Scope and mutable defaults.
5. Reading and writing safe text files.
6. JSON decoding and encoding.
7. CSV parsing.
8. Working with pathlib.
9. Dataclasses.
10. Classes, attributes, methods.
11. Encapsulation and composition.
12. Iterators and generators.
13. Type hints.
14. Unit testing with pytest.
15. Debugging and logging.
16. Multi-module repair project.

**Zone concept:** The Workshop District. The player assembles drones, maintains logs, manages inventory, and repairs a Python package across rooms.

### Track C — Interview algorithms (16 proposed missions)

1. FizzBuzz.
2. Valid Palindrome.
3. Best Time to Buy/Sell Stock.
4. First Unique Character.
5. Reverse String.
6. Valid Parentheses.
7. Merge Two Sorted Lists (intro data structures).
8. Binary Search.
9. Sliding Window maximum-sum fixed length.
10. Longest Substring Without Repeating Characters.
11. Prefix Sums.
12. Product of Array Except Self.
13. Frequency map matching.
14. Linked list traversal.
15. BFS on a tiny grid.
16. Algorithm boss: multiple approaches with time/space analysis.

**Zone concept:** The Algorithm Tower. The player supplies tested utility functions to unlock logic-based machines; explanation prompts ask for complexity without requiring memorized buzzwords.

### Track D — Telemetry and real applications (16 proposed missions)

1. Parse `TEL` packets safely.
2. Validate packet sequence order.
3. Detect missing readings.
4. Temperature threshold alerts.
5. BME-like sensor calibration arithmetic (synthetic data).
6. IMU magnitude calculation.
7. Rolling average.
8. Ring buffer.
9. Status transitions NORMAL/DEGRADED.
10. Convert bytes to integers.
11. Extract values from structured JSON.
12. Record synthetic rows to SQLite (non-Pygame isolated test mode).
13. Simulate producer/consumer queues.
14. Async event handling fundamentals.
15. Plotting data outside the core game.
16. Build a functioning virtual telemetry dashboard mini-project.

**Zone concept:** Mission Control Annex. The learner writes real data-handling logic that changes simulated live instruments in the game, with synthetic nonmedical readings only.

**Total roadmap:** 24 authored v1 missions + 64 proposed follow-on missions = 88 missions if all future content is built. Do not imply the 64 are already authored/tested or promised in the initial release.

## Evolving from terminal puzzles into programmable gameplay

A more distinctive game experience requires some player-authored code that *directly controls world objects*, not only switches on a lamp after a function passes tests.

**Programmable drone mode (after stable launch):** Player writes a function `plan_route(obstacles, target)` that returns a constrained list of actions (`"UP"`, `"DOWN"`, `"LEFT"`, `"RIGHT"`). The grader validates correctness and action limits in its isolated worker. The game then animates a drone following the returned plan in the world; user code never receives references to Pygame surfaces, files, or internal game objects.

**Factory conveyor mode:** Player writes `route_packet(packet)` returning which chute receives each telemetry packet; simulated packets visibly follow the selected path.

**Sensor sweep mode:** Player writes `filter_readings(readings)` and the returned values animate on the scanboard, with incorrect results visually missing detected objects.

**AI opponent challenge:** Player improves an O(n²) function to O(n), with gentle performance comparisons. Avoid infinite-loop risk by fixed input sizes and subprocess timeouts.

## Suggested session structure

- 5 minutes: freely write the previous day's skill from memory.
- 25–40 minutes: attempt new in-game coding terminals, debug all errors.
- 10 minutes: optional review terminal and paper notes.
- 5 minutes: independent write of one solved problem in a blank editor.

Do not require this schedule inside the game; provide an optional focus-mode timer only later. Maximize transfer to real coding instead of maximizing streak clicks.

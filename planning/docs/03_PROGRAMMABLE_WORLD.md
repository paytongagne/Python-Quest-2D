# 03 — Persistent programmable world: Mica, devices, replay

## Objective
**Convert successful Python submissions into reusable, player-owned capabilities.** The first flagship feature is a companion rover called Mica that executes safe, bounded plans against actual map geometry. A second feature allows a small catalog of world machines to accept validated data or command plans. Both retain genuinely written Python, but all world effects are validated and applied by the game, never by learner code acting directly on the renderer.

## Version 1 contract (proposed; not present in v1.4)
In a device's coding view, the player writes:
```python
def plan(observation):
    # observation is a JSON-like dict copied from the world
    # Return 0-64 action dictionaries; no mutation of global state
    return [
        {"type": "scan", "direction": "north"},
        {"type": "move", "direction": "east"},
        {"type": "interact", "target": "relay_a"},
    ]
```

**Observation v1** (world engine generated, frozen before invocation):
```json
{
  "schema": 1,
  "world_id": "orion_moon",
  "robot": {"id": "mica", "cell": [8, 12], "energy": 30, "abilities": ["move", "scan", "interact"]},
  "visible": {"width": 10, "height": 8, "walls": [[1, 1]], "devices": [{"id": "relay_a", "cell": [4, 2], "state": "offline"}]},
  "objective": {"target_id": "relay_a", "required_state": "online"},
  "rules": {"max_actions": 64, "step_energy": 1, "scan_energy": 2}
}
```
**Allowed actions**: `move(N/S/E/W)` one cardinal tile; `scan(direction|radius)` only with scanner ability; `interact(target)` adjacent to target and permitted by device capabilities; `wait(ticks)` bounded 1..5; `report(label)` optional, max 120 chars. Future skills add `pickup`, `drop`, `sample`, `send`, and `set` through versioned capability catalog.

### Validation pipeline
1. Game creates immutable observation with only game-owned JSON primitives and stores its hash + world snapshot ID.
2. Game sends the author's Python source, fixed `plan` function name, copied observation and designated tests to `core/grade.py` in a short-lived process.
3. Worker runs `plan(copy.deepcopy(observation))` on authored fixtures, requires exact `list[dict]` of allowed shapes, validates output length/time/serialization and captures structured trace. Never return executable functions/classes to renderer.
4. **Second independent game-side validator** checks each action against current map bounds, collision, device visibility, adjacency, unlocks, energy, action budget and immutable source snapshot. Validate entire transaction before changing mission progress. Failure returns a trace reason with the earliest invalid step, not a partially completed permanent repair.
5. If tests pass, game registers a `ProgramRevision` in a local library and offers **Deploy**.
6. Deployment re-validates on the actual current world. Advance one action at a time at a fixed simulation tick; render interpolation independently of logic tick. Maintain a bounded trace and cancel/pause/replay controls. Persist a checkpoint only on recognized atomic objective milestones, so quitting is safe.

### No invisible success
A successful program must produce: named action icon over robot; path highlight; robot movement or device animation; final state change; completion card; explicit reusable program slot. If output passes tests but the world state changed and cannot be replayed, the feature is not accepted.

## Program library
- **Saved draft**: unverified source; can be reopened; no live deployment.
- **Verified revision**: source text + sha256 digest + contract name/version + verification summary + fixture version + allowed world tags.
- **Equipped slot**: points to a verified revision; equipping cannot silently rewrite original source.
- **Replay record**: immutable bounded action trace, initial snapshot hash, final delta, step count, energy cost, deterministic seed.
- **Upgrade entitlement**: game-owned flag that adds abilities; never stored solely as a variable in learner code.

Proposed schema under new `progress["program_library"]`:
```json
{
  "schema": 1,
  "slots": {"mica.navigation": "p1"},
  "revisions": {
    "p1": {"name": "Lunar route", "source": "def plan(observation):\n    return []\n", "contract": "mica.plan.v1", "verified": false, "hash": null, "verified_worlds": [], "created_at": "2026-11-06T00:00:00Z"}
  },
  "traces": []
}
```
`verified` is never set merely because the field claims it: replay/deploy re-validates signed/hashed content against a current contract, then rechecks world constraints. Limit source length, histories and trace counts, with pruning that preserves equipped programs.

## Deterministic runtime
- Use fixed logical action ticks (e.g. 5 Hz for robot logical steps) and draw interpolation at independent FPS; frame rate never changes path legality.
- For an `interact` with machine state, send intent `{device_id, action, parameters}` through game-owned reducer; never let a Python-produced action assign `world_flags` directly.
- All randomness in scenarios uses a fixed seeded RNG passed in observation, never `random()` with hidden global state from gameplay.
- `scan` can reveal only tiles within allowed range; future tasks may include unknown cells and changing hazards.
- Robot cannot move outside map, through colliders, through locked gates, or overlap a protected NPC position.
- Abort / Esc / load / travel closes the running deployment cleanly. Persist last safe landmark and rollback incomplete multi-action world mutations.
- Path results are capped and documented; deep scripts do not rely on unbounded loops or untrusted object serialization.

## First flagship encounter: Mica and the Orion outpost
**World state:** power off, fog at north quarry, damaged relay, one maintenance hatch, two optional archives. The player sees a signal flash behind a locked maintenance gate. The companion scan highlights a fault; a terminal introduces an observation and four-action plan. A first guided plan reboots one beacon. Next puzzle supplies blocked tiles and forces the player to compute an actual route, then replay. Finally a transfer challenge asks them to re-run the *saved* script on a similar but not identical field map.

**Success:** the gate opens with sound, relay beacon animates, alternate map corridor becomes accessible and the old path remains replayable. No repeat mission XP. Completing optional optimization grants one cosmetic circuit trail and a mastery mark.

**Failure:** incorrect Python raises a precise line/test; invalid movement produces a step-indexed trace such as `Step 4: east target (12, 6) is a solid tile`, with world still unchanged. Resource exhaustion explains energy; player can reduce action count or choose another route.

## Device programming catalog
| Device type | Observations | Accepted output | Persistent change | Initially used in |
|---|---|---|---|---|
| Relay | link state, power budget, adjacent routes | action plan / activation intent | network path and gate | Orion |
| Cargo dock | crates, positions, battery | robot route + pickup/drop | available materials | Orion/Workshop |
| Press/Reservoir | capacity, machine health, sensors | validated config/snapshot | fill level or powered status | Workshop |
| Broker | queue length, device health, topic subscriptions | packet routing plan | network pulses, lights, delivery count | Titan |
| Oscilloscope | sample rate, toy trace and flags | validated array summary | waveform and quality UI | Helix |
| Mapping console | toy 3D points, mesh, timestamps | numeric field arrays, cursor trace | toy chamber overlays | Aurora |
| Control scheduler | DAG, budgets, live flags | validated repair protocol | station-wide state machine | Finale |

## Replay / debugger user experience
`R`: reopen last program action trace. `Space`: play/pause. `←`/`→`: previous/next step. `Home`: beginning. Optional inspector shows current observation, action, position, energy, device state before/after, and why an action is rejected. Add `Compare` to place two accepted runs side by side on *the same seeded fixture*. Optimization rankings prioritize correctness, then fewer actions/energy; no online leaderboards.

## Technical tests (must be authored before implementation is called complete)
- Actor obeys walls, bounds, adjacency, energy, abilities and max action count.
- Same code+snapshot yields same trace on repeated runs.
- A source change invalidates verification until retested.
- Mutating submitted observation does not mutate actual game observation.
- Invalid return types, nested huge structures, NaN/Inf and unknown actions rejected.
- Save, quit, reload mid-replay or mid-gate never doubles XP or partially destroys world.
- Disconnected world / legacy save retains the player and previously completed IDs.
- Worker timeout, crash, syntax error and log overflow present actionable diagnostics without freezing the frame loop.

## Security note (non-negotiable)
The shipped local `-I -S` worker with a timeout is useful for accidental runaway exercises but not safe containment against hostile Python. Do not run downloaded/untrusted scripts. For distribution beyond a trusted local learner, a real constrained process boundary with OS-level isolation and permissions would be required. No plugin system, network execution or unrestricted user-generated multiplayer sharing in this product phase.

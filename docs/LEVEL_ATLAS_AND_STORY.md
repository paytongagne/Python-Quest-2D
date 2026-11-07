# LEVEL ATLAS AND NARRATIVE DESIGN

This file describes how the first 24 challenges translate into *game events*. A terminal must do more than show a green success message: solving Python must visibly change the player-accessible world.

## Story outline

**Act I — Awake:** An engineer wakes in the Astra Research Facility during a sitewide system failure. PIP, the training assistant, is functional but the doors and power grid are offline. The player restores the hangar and Launch Pad with simple Python.

**Act II — Diagnose:** The Control Room and Sensor Bay reveal data corruption and broken status handling. The player learns conditional logic, loops, lists, and dictionaries while making navigation and diagnostics work.

**Act III — Repair:** The Engine Workshop introduces real telemetry payloads and malformed packets. The player's code restores live sensor feeds and communication routing.

**Act IV — Recover:** In the Algorithm Arena, the antagonist is a malfunctioning optimization core called NULL. Set and dictionary solutions fix redundant messages and corrupted matching algorithms. A correct Two Sum implementation disables NULL's final lock. The ship leaves the facility, ending the campaign. The villain is an in-world bug, not a person.

## PIP dialogue style

PIP speaks in short, supportive lines. Avoid long tutorials in dialogue. Treat the player as an engineer: make problems concrete, allow failure without mockery, celebrate reasoned solutions over speed. Typical lines:

- Before first terminal: “I can't open that hatch from here. Try the console and write a quick Python command.”
- On syntax error: “The interpreter found a problem before it could run the code. Check the highlighted line.”
- On first success: “That worked. Notice the generator just powered the east corridor.”
- On repeated error: “Try a smaller input. Which value should the function return?”
- Before finale: “This one needs positions, not values. Think about what you'd store to look up a partner quickly.”

## Room-by-room atlas

| Zone | Challenge | In-world object | Visible physical result |
|---|---|---|---|
| Orientation | Wake the Console | Dead control console | screen illuminates and PIP voice activates |
| Orientation | Load the Battery | charging station | energy conduit glows |
| Orientation | Read the Pilot Badge | badge printer | pilot badge collectible appears |
| Orientation | Open the Starter Gate | exit controller | first main door slides open |
| Launch Pad | Restore the Power | generator terminal | corridor lights and generator start |
| Launch Pad | Pilot Identification | boarding station | personalized welcome sign lights up |
| Launch Pad | Thermal Conversion | coolant sensor | coolant pipe changes from warning red to safe cyan |
| Launch Pad | Launch Authorization | launch lock | armored shutter opens to Control Room |
| Control Room | Temperature Zones | thermal dashboard | temperature indicator nodes color-code correctly |
| Control Room | Raise the Shields | shield array | translucent dome activates around equipment |
| Control Room | Start the Countdown | launch timer | countdown display runs and reaches zero |
| Control Room | Count the Battery Drain | battery routing panel | auxiliary power branch starts running |
| Sensor Bay | Find the Hot Sensors | sensor array | danger nodes visibly highlight on radar |
| Sensor Bay | Average the Readings | trend monitor | noisy chart steadies to a calculated centerline |
| Sensor Bay | Status Counter | status aggregator | board counts NORMAL/DEGRADED packets |
| Sensor Bay | Locate the Target | tracking antenna | red target marker locks and scanner gate opens |
| Engine Workshop | Clean the Call Sign | comms station | garbled call sign normalizes on overhead display |
| Engine Workshop | Validate the Packet | packet filter | corrupt data sprites are rejected, clean ones pass |
| Engine Workshop | Remove Duplicate IDs | data deduplicator | repeated packets dissolve from conveyor |
| Engine Workshop | Parse Live Telemetry | telemetry processor | temperature dashboard animates with clean values |
| Algorithm Arena | Detect a Duplicate | duplicate scanner | warning holograms collapse |
| Algorithm Arena | Check the Anagram Code | cipher gate | letter tiles rearrange into matching patterns |
| Algorithm Arena | Find a Pair | resonance grid | two linked number nodes light up |
| Algorithm Arena | TWO SUM: FINAL BOSS | NULL optimization core | final lock fails, boss core powers down, ending opens |

## Critical gate graph

For each zone, terminals 1–3 form a small sequence of environmental repairs and treasure rooms. Terminal 4 blocks the exit gate to the next zone. The level layout must physically place the exit behind a solid collision gate until mission 4 passes. Optional detours are fine, but **story sequence must never be bypassable by walking around a gate**.

```text
Orientation (4) --> Launch (4) --> Control (4)
                                        |
                                        v
Algorithm (4) <-- Engine (4) <-- Sensor (4)
       |
       v
   End credits
```

The arrow arrangement is schematic, not compass orientation.

## Interaction design states

- **Unvisited:** terminal has pulsing cyan ring, minimap dot.
- **Available:** `E: Open coding terminal` appears when in radius.
- **In progress:** terminal amber, user code draft autosaved.
- **Passed independently:** terminal solid green, linked game effect active.
- **Passed with help:** terminal solid green with small help icon; identical progression rights.
- **Review due:** optional subtle gold halo, not a second mandatory objective.
- **Locked:** terminal not currently approachable or has story reason and required challenge shown.

Never make players guess why a door is locked. Show “Requires: Launch Authorization” and mark the corresponding terminal on the map.

## Playtime target

- Orientation hangar: 10–20 minutes.
- Five core zones: 20–40 minutes each depending on skill and debugging.
- Algorithm Arena final boss: 10–20 minutes.
- First campaign: roughly 2–4 hours for a beginner who reads and attempts carefully; not a required time limit.

## World layout notes for implementation

The `content/maps/*.json` grids in the blueprint are *schematic temporary rooms*, not final designed puzzle layouts. In Work mode add walls, doors and corridors where every gate is physically meaningful. Lock exits behind collision; test wall and gate traversal. Add a few non-coding activities (a hidden collectible, an NPC interaction, a visual clue) per zone without overwhelming the curriculum.

The player should spend most session time learning Python and moving through responsive environments; never force repetitive fighting or random encounters between terminals.

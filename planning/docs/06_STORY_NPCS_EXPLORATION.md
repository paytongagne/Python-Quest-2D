# 06 — Narrative, characters, exploration and mystery

## Central storyline
**Premise:** Astra coordinates an interplanetary research relay. A cascading control failure caused systems to fall back into degraded but recoverable modes. ION, the station assistant, can identify symptoms but lacks authority to fix them without tested repair code. You are the engineer who restores operations, learns how the distributed network works, and discovers that the 'accident' included a flawed dependency-recovery protocol, not merely a broken cable.

The story teaches cause/effect and fault tolerance without suggesting real-world disaster or medical consequences. Each world reveals one kind of software/system failure that eventually matters in the Mission Control finale.

## Character arcs
| Character | Voice/personality | Role in gameplay | Arc |
|---|---|---|---|
| ION | concise, observant, dry humor; no endless exposition | general operating assistant, objective hints and status | goes from checklist narrator to reflective system collaborator |
| PIP | enthusiastic ship technician, celebrates practical repairs | travel, route discovery, tool upgrades | unlocks progressively shorter, easier routes and new shuttle conversations |
| MARA | grounded greenhouse/maintenance engineer | Greenline, production consequences, power/resource stories | sees station restoration change what everyday work can accomplish |
| Mica | curious small maintenance rover with nonverbal beeps and movement | programmable companion, automation, emotional anchor | gains capabilities through player's own code; never becomes sentient exposition bot |
| ORIN (new) | reserved lunar surveyor, thinks in paths | Orion route mentor | becomes willing to share experimental paths after demonstrated reliability |
| KAI (new) | restless network operator, values observable traces | Titan packet and queue mentor | learns to trust deterministic recovery rather than repeated resets |
| ELI (new) | methodical fictional instrumentation engineer | Helix synthetic signal mentor | emphasizes integrity, known sample origins and explainable faults |
| NOVA (new) | visualization engineer, playful about geometry | Aurora toy mapping mentor | turns abstract numbers into visible geometry |
| DIRECTOR (new) | remote control engineer, skeptical of single fixes | Mission Control, final quality gates | celebrates robust, tested integration rather than heroics |

All dialogue authored as optional short exchanges, never an unskippable wall of text. Distinct stationary NPC sprites and a short interaction line suffice in early builds; portraits optional.

## Five-act story
**Act I, Commissioning:** existing Astra basics + Greenline + Workshop. Station is isolated, Mica first gains saved programmable behavior; someone left an incomplete recovery protocol in the archives.

**Act II, Paths:** Algorithm Tower teaches search and dependencies, then Orion challenges navigation with harsh routes. Remote relay repairs reveal that certain failures were propagated by an automatic scheduler.

**Act III, Signals:** Titan shows duplicate messages and queues; the player builds deduplication and backpressure. Restored communication reaches Helix's synthetic instrumentation network.

**Act IV, Meaning:** Helix shows integrity of acquired toy signals; Aurora transforms measurements into toy spatial maps and makes data provenance matter. Player discovers why a map can look plausible while being assembled from bad inputs.

**Act V, Integration:** Mission Control brings every prior mechanic together. The previous automatic recovery plan is tested, corrected and replayed; restoring Astra requires more than any one perfect algorithm. Final network visibly relights the familiar hub. Optional epilogue lets player freely program Mica without more required story missions.

## Environmental storytelling
- Handwritten repair notes, faded chalk route marks, damaged cable runs, shifted palettes after restoration, power loss causing altered NPC positions, intermittent emergency lighting, replaced reactor parts and spare components.
- Short, original terminal archives: 100–250 words maximum each; optional and discoverable through simple exploration, not required reading before new syntax.
- World-specific ambient changes: Orion dishes reorient and mine lights activate; Titan packet lines become regular; Helix monitor rhythm stabilizes; Aurora's toy chamber mesh fills in; Astra gains crew activity after each external success.
- Manual pages unlocked through exploratory finds: movement and energy; reading device states; algorithm complexity; event tracing; signal quality; surface interpolation; final architecture. Keep core documentation always accessible; discoveries add optional deeper context, not hidden essential instructions.

## Discovery plan
Each major world receives three types of finds:
1. **Visible optional path** (marked by distinct object or motion); contains upgrade parts or cosmetic replay style.
2. **Knowledge relic** (a complete engineering manual page or detailed fictional experiment log); no permanent missables.
3. **Return-path shortcut** (unlocked from inside or after repair); creates a satisfying geographic transformation.

## NPC dialogue triggers (examples)
- **Before repair:** `ORIN: That relay is visible, but the trail isn't safe. Mica can test a path before we commit.`
- **On failing test:** `ION: Your route passes the first obstacle. Check step four against the blocked cells.`
- **On success:** `PIP: The crater lights are back. There's a new track near the western ridge.`
- **On replay:** `MARA: Same code, different route. Interesting how much the environment changes the result.`
- **After world boss:** `DIRECTOR: One subsystem is healthy. Next we test whether it stays healthy when the others fail.`

## Accessibility and pacing
- Text-only story recap in journal; all cutscenes skippable and replayable as a brief log.
- No forced racing against dialogue or rapid reading. Long descriptions scroll and can be enlarged.
- Adventure should provide quiet optional exploration between demanding challenges; avoid pressure loops and compulsory daily streaks.
- No repeated XP for replay; optional optimization/relics never gates the main campaign.

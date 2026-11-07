# UI DESIGN, IN-WORLD FEEDBACK AND ART DIRECTION

## Visual identity

**Working title:** Python Quest 2D: Code Runner  
**Palette:** space navy #101827, slate #26364B, cyan #44D9F4, amber #FFCC71, mint #65DBB1, red #EF7485, white #E8F4FF.  
**Render style:** clean 2D pixel art, 32-pixel tiles, low-noise surfaces, readable character silhouettes. Avoid excessively sharp glow effects and motion behind the code editor.

## Exploration wireframe

```text
+--------------------------------------------------------------------------+
| [Energy ████████]  [Level 3]   XP 260   Mission: Restore the Power [J]   |
|--------------------------------------------------------------------------|
|                                                                          |
|          #################################################               |
|          #          [terminal]        [locked door]       #               |
|          #            [◇]               [##]             #               |
|          #                                                 #               |
|          #  [player]      [PIP]         [generator]          #              |
|          #     @            !              O               #              |
|          #                                                 #               |
|          #################################################               |
|                                                                          |
|   [E] Open: Power Terminal                                [Esc] Pause     |
+--------------------------------------------------------------------------+
```

The visible scene must use real sprites and tile layouts, not literally print these symbols. Use one 2D camera; no 3D perspective.

## Terminal UI wireframe

```text
+-------------------------------------------------------------------------+
| TERMINAL: RESTORE THE POWER                          [Help] [Close X]   |
|-------------------------------------------------------------------------|
| LESSON                                  | CODE EDITOR                      |
| Add two values using + and return      | 1 def add_energy(current, pickup):|
| the result.                             | 2     pass                       |
|                                         | 3                                |
| OBJECTIVE                               |                                  |
| Return current + pickup.                |                                  |
|                                         |                                  |
| EXAMPLE                                 |                                  |
| add_energy(40, 15) -> 55                |                                  |
|                                         |                                  |
| [Hint 1] [Hint 2] [Show solution]       | [Run tests Ctrl+Enter] [Reset]   |
|-------------------------------------------------------------------------|
| RESULTS: 3/4 TESTS PASSED                                                |
| FAILED: add_energy(40,15) — expected 55, got 54                          |
+-------------------------------------------------------------------------+
```

### Important UX principles

1. Code editor always gets a large readable surface (at least 55% width).
2. Prioritize keyboard-first input with reliable focus and indentation.
3. Error messages always include one specific failing example when possible.
4. Preserve draft on close/quit and after attempts.
5. Make successful tests feel rewarding without blocking the next interaction.
6. Hint and reveal options must be clearly distinguishable from running tests.
7. Use proper horizontal/vertical scroll for code; never silently truncate source.
8. Keep actual Python syntax errors unaltered with optional explanatory note underneath.
9. Do not call a game success "correct" if the evaluator timed out or worker crashed.

## Feedback animation language

- **Submitted:** short pulse around terminal, progress spinner in editor, world paused.
- **Failed:** gentle shake of one results panel, red label and exact failed tests; no damage or loss of progress.
- **Passed:** terminal pulses mint, power beam animates to target object, player receives XP toast, linked door opens after a short nonblocking cue.
- **Zone complete:** optional 2–3 second transition with skip support and new region title.

## Art asset manifest for release

| Asset | Planned size | Variants |
|---|---|---|
| Player sprite sheet | 32×32/frame | 4 directions × 4 frames, idle |
| PIP assistant | 24–48 px portrait | neutral, hint, celebration |
| Floor tiles | 32×32 | six zone palettes, edge variants |
| Wall tiles | 32×32 | corners, edges, doors |
| Terminal sprite | 32×32 | off, active, pending, passed |
| Gate sprite | 32×64 | locked, opening, open |
| Drone enemy (future) | 32×32 | patrol, stunned, inactive |
| HUD icons | 16/24/32 px | XP, energy, journal, terminal |
| Effects | 32–128 px | sparks, power, shield, particles |
| UI panels | scalable | pause, mission, terminal, results |

Do not share or copy commercial game sprites or music without permission. Placeholder geometric assets suffice for MVP; do not choose final art before input/editor reliability.

## Audio notes

Sounds should communicate events, not distract from typing. Terminal panel opens quietly, background music drops in volume when code editor is active, and error feedback is subtle. Controls for volume and mute are mandatory by polish phase.

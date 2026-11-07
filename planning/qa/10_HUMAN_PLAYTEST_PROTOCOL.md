# 10 — Human playtest protocol (not yet performed)

## Recruiting and setup
Use at least 3 novices (little/no Python), 3 intermediate learners and 2 returning-player sessions, where feasible. Avoid telling first-time testers controls or mission locations beyond the in-game tutorial. Record platform, input mode, display resolution, font/reduced-motion settings, build digest and **only with consent** anonymized observations. No sensitive data. Offer skip/quit any time.

## Session A: first-time novice (20–30 min)
1. Launch from a clean install without guidance. Observe time to move, find current objective and reach a terminal.
2. Run an intentionally wrong program. Observe whether player understands error and knows how to retry.
3. Complete the first lesson and identify which game object changed.
4. Find the Workshop entrance via in-world cues, not `J → 8` verbal instruction.
5. Explore an optional log/secret and return to the main route.
6. Quit and reopen. Explain what should happen next.

## Session B: intermediate coder (30 min)
1. Solve a rover route with two different valid approaches.
2. Use replay/trace to explain a failure.
3. Save and reuse a device program (when implemented).
4. Check whether code genuinely changes machinery and whether player can predict the effect.
5. Try a more difficult algorithm and ask for hint only if necessary.

## Session C: returning player (15 min)
1. Resume an existing profile and find the current next objective without developer instructions.
2. Travel to a previously visited world and back.
3. Replay completed mission and confirm no duplicate XP.
4. Recover from a deliberate restart during a safe job checkpoint.

## Accessibility pass
Test keyboard-only, mouse-only where supported, at 1280×720/1600×900/1920×1080; at least two camera positions for each world. Evaluate focus indication, contrast, UI clipping, color-independent error cues, reduced motion, readable text, and slow input response. New text-size presets only after implemented.

## Observation sheet
Capture task ID, expected behavior, completed (yes/no), elapsed seconds, confusion pauses, hints used, failed attempts, UI overlap, exact repro step, severity P0/P1/P2, and tester comment. Avoid recording identities.

## Suggested research thresholds (aspirational, not pass claims)
- At least 80% of novice tasks find first objective without external help.
- At least 80% understand where to see and fix a failing Python attempt.
- 100% of critical paths accessible without relying on color alone.
- No P0 save/progression loss among sessions.
- Workshop discovery median <=3 minutes after it becomes relevant.
- Prefer qualitative issues over relying on small-sample percentages as proof of usability.

**Exit:** Aggregate observations, attach anonymized issue list, resolve all P0 and progression-related P1 issues, and explicitly state which claims still lack human verification.

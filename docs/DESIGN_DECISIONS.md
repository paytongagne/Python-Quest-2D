# DECISION LOG

These decisions are locked for the first Work mode implementation unless evidence requires a change.

1. **Genre:** top-down 2D sci-fi adventure with real movement and collision. If "plane" meant aircraft flight instead of a geometric 2D plane, replace only the movement/world layer, not the lesson/grader/progress architecture.
2. **Platform:** Windows desktop, offline-first, local data.
3. **Engine:** pygame-ce 2.5.8 and Python 3.12. No engine swap until vertical-slice results justify it.
4. **Content:** 4 new true beginner script challenges plus 20 imported function challenges.
5. **Learning:** write code, submit real Python, get explicit feedback, revise; no mandatory multiple-choice substitute.
6. **World progression:** mission completion physically unlocks doors and systems.
7. **Editor:** in-game multi-line editor with good keyboard support. A dedicated popup is temporary fallback only if keyboard input blocks the vertical slice.
8. **Safety:** separate time-limited local worker for *self-authored* code; not a hostile-code sandbox.
9. **Save:** versioned atomic local JSON, optional one-time legacy import.
10. **Milestones:** don't expand scope before successful vertical slice; 24-mission campaign is initial release, 64 more are a backlog.

**Deferred**: combat depth, voice acting, precise art asset pipeline, player avatar appearance, future programmable drones, packaged EXE versus launcher (choose based on clean-install test).

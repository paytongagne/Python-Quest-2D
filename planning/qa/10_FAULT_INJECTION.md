# 10 — Fault injection and recovery playbook (planned game tests)

All inputs must use **disposable profiles**, never the user's main save. New worker/device fault cases require implementation before these become executable gameplay tests. Each result captures before/after file hash, XP, completed set, world flags and event IDs.

| Fault | Injection technique | Required result | Repeat at |
|---|---|---|---|
| worker timeout | infinite loop in trusted self-authored test fixture (in isolated test session) | worker killed or reported timeout, draft preserved, no XP | script/function/program |
| crash/malformed worker JSON | stub worker returns non-JSON/invalid enum | parent returns `INVALID_OUTPUT`, no world effect | grade, device |
| stale snapshot | compute valid plan, change blocker/map digest | `STALE_SNAPSHOT`, no movement | robot, travel |
| energy exhausted | plan costs one more than capacity | explicit rejection, no partial route | robot |
| injected save-write error | mock `os.replace` / `Path.write_text` at safe boundary | last good save intact, visible error | save |
| truncated save | write truncated JSON in temporary profile | preserve corrupt bytes, recovery/quarantine | load |
| future schema | set `schema_version=999` in copied profile | reject writes, original bytes unchanged | load/save |
| pre-commit crash | interrupt before world-event atomic commit | last safe state, no repair or XP | device |
| post-commit restart | restart immediately after atomic replace | exactly one repair and XP | device |
| user cancel | cancel during simulated action phase | safe pause/cancel, no false success | robot |
| travel interruption | quit during departure/arrival on disposable profile | deterministic return checkpoint, no stuck map | travel |
| focus loss/minimize | toggle app focus during terminal submission | draft and input restored | UI |
| invalid synthetic sample | NaN/Inf/null confusion, out-of-order timestamps | reject or mask per Stage08 semantics; never show fabricated zero | Helix/Aurora |

**Execution policy:** Inject exceptions through mocks first. Any process-kill test must run in a dedicated subprocess with a temporary save path and a timeout/watchdog, never in the test runner's own process. Record the literal fault injection points and platform.

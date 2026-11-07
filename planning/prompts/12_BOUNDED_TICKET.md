# Work prompt — SELECTED TICKET (repeat)

Use Stage11 catalog and Stage10 release gates. Select the next dependency-eligible ticket with `python tools/work_ticket.py next --state handoff/12_TASK_STATE.json`, then generate its brief with `python tools/work_ticket.py brief <ID>`.

Implement only that ticket. Preserve all earlier IDs, saves and APIs. Read selected source anchors plus immediate interfaces, not the entire codebase. Add the ticket's targeted executable tests, run relevant regressions, create a recoverable source checkpoint, capture truthful test evidence, and update `handoff/12_TASK_STATE.json` only after evidence is recorded. If blocked, record reason and continue only with an independent eligible ticket that cannot risk data loss. Keep output <=180 words. No Windows binary rebuild for each four-mission batch unless required by that ticket's gate.

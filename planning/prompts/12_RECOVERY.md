# Work prompt — INTERRUPTED SESSION RECOVERY

Resume Python Quest from **actual saved artifacts**, not the last chat claim. Locate `checkpoints/CURRENT.json`, verify referenced source archive SHA256 and `handoff/12_TASK_STATE.json`. Compare to repository status, trace any uncommitted changes, list unfinished ticket and test failures.

If evidence differs, mark ticket IN_PROGRESS/TEST_FAILED rather than DONE. Continue from the latest valid source checkpoint, preserving newer files, legacy mission IDs and profile data. Do not reimplement tickets with verified source and tests. First priority: make a fresh recoverable source ZIP and update CURRENT. Then repair any failed current ticket; proceed to next eligible one when safe. Report source checksum, completed ticket IDs, mission count (verified or unknown), outstanding tests and next action. No background guarantee.

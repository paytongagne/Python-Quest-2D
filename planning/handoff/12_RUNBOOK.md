# Work operator runbook — bounded execution and handoff

## Start

1. Locate current working repository and unpacked **editable** source; compare to v1.4 ZIP. Identify whether Work already has newer improvements, and do **not** overwrite newer source.
2. Record SHA256, git status, 76 baseline mission IDs, save schema/version and installed dependencies. Use disposable `PYTHONQUEST_SAVE`; create `checkpoints/` and write initial immutable source archive.
3. Read `handoff/12_REPOSITORY_CONTEXT.md` then `python tools/work_ticket.py next --state handoff/12_TASK_STATE.json`; do not read all stage docs first.
4. Run `python tools/work_ticket.py brief PQ11-001 ...`, inspect exact source anchors, selected QA IDs, and required gates.

## Per ticket

- Create branch/working copy or backup; mark IN_PROGRESS with `python tools/work_ticket.py start <ID> --state ...`.
- Implement selected ticket, not adjacent speculative features. For mission batches, make four real, graded, playable, replayable IDs.
- Targeted tests => relevant regression => documentation and save compatibility => complete source checkpoint. Maintain native Windows status separately.
- Save `QA_EVIDENCE.json` (sample in `handoff/12_EVIDENCE_TEMPLATE.json`) listing commands, runtime environment, test counts, result paths, source hash, validated mission IDs. Use `python tools/work_ticket.py done <ID> --evidence path --state ...`; the tool rejects absent or failed evidence. This utility validates **evidence form and consistency**, not whether tests actually passed. Human reviews underlying artifacts.
- If the code/tests fail, mark `python tools/work_ticket.py fail <ID> --reason 'failed test...' --state ...` and preserve the log. Once corrected, use `python tools/work_ticket.py retry <ID> --state ...` to return to IN_PROGRESS; dependency checks are enforced.
- If blocked: `python tools/work_ticket.py block <ID> --reason '...' ...`. Preserve checkpoint and clear actionable next step.
- Continue to next eligible ticket if tools/allowance permit. On interruption use `prompts/12_RECOVERY.md`.

## Native release

- `python tools/verify_windows_archive.py <zip> --json <report>` is static only.
- Run bundled native smoke scripts and launcher **on actual Windows** using disposable saves; take screenshots and gameplay proof at three resolutions; report native/human gates as BLOCKED until evidence exists.
- Do not regenerate Windows ZIP every four missions; source and logs are sufficient at interim checkpoints. Major stable release needs Windows ZIP plus source ZIP/checksum/report.

## Recovery invariant

`CURRENT.json` checkpoint and task-state checksum must match current source or a documented patch-diff. A task is not done just because an assistant said it was. Recover incomplete ticket first. Preserve old save data. Stop on XP duplication, lost completion, corrupt save, unsafe action authorization or broken launch.

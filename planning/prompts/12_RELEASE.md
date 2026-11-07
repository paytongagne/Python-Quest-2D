# Work prompt — BUILD AND RELEASE CHECKPOINT

Freeze current verified source; record SHA256 and version. Run Stage08–12 applicable planning checks separately from runtime tests, then run current-source game regression and new ticket tests against disposable saves. Evaluate all hard gates from `release/10_RELEASE_GATES.json`, including v2/v3/v4 save compatibility, duplicate XP, worker boundaries, performance and screenshots. On actual Windows extract to a clean path and run native smoke scripts, launcher, save/reopen and display-size checks; perform human playtests or mark NOT RUN.

Produce source ZIP, Windows ZIP only if successfully built, SHA256SUMS, machine-readable QA status, changelog, known issues and rollback checkpoint. If native Windows or human tests cannot run, label it a development checkpoint and do not imply final release passed. Do not claim 152 missions merely because they appear in a plan.

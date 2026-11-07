# Stage 10 test run record — 2026-11-06

**Host:** Linux container, Python 3.13; `pygame-ce` unavailable; source located at `/mnt/data/pq_stage09_source`. Original v1.4 portable Windows archive supplied by user.

| Evidence | Command | Outcome | Important limitation |
|---|---|---|---|
| Stage08 design | `python -m unittest discover -s tests -p 'test_biomed_planning.py' -q` | 7 PASS | Design integrity only |
| Stage09 contract/source | `PYTHONQUEST_V14_ROOT=/mnt/data/pq_stage09_source python -m unittest discover -s tests -p 'test_stage09_*.py' -q` | 21 PASS | Selected v1.4 integration and schemas; no new game features |
| Stage10 release planning | `python -m unittest discover -s tests -p 'test_stage10_*.py' -v` | 12 PASS | Catalog/tools verification only |
| Original v1.4 Windows archive | `python tools/verify_windows_archive.py /mnt/data/Python-Quest-2D-v1.4-Windows-x64.zip --json release/10_V14_STATIC_AUDIT.json` | PASS, 427 entries, no errors, SHA256 7f845cec5b66ac5b6bc7fc9d07edc2b7e50adb45b9604b92caf46470a92da5e3 | ZIP structure and CRC only, **not Windows launch** |
| v1.4 Pygame headless suite | not run | BLOCKED | pygame-ce missing in this container |
| Native Windows launcher/smoke | not run | BLOCKED | no native Windows host |
| Human playtesting | not run | NOT RUN | requires actual user sessions |
| Performance measurements | not run | NOT RUN | budgets are proposed; no frame samples supplied |

**Scope and trust:** None of these tools execute unknown learner scripts. The zip auditor reads ZIP metadata/member CRCs without extracting or running executable content.

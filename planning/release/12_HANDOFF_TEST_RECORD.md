# Stage 12 independent verification record

**Date:** 2026-11-06. **Host:** Linux container, Python 3.13. **Baseline:** full v1.4 source content extracted from `Python-Quest-2D-v1.4-Windows-x64.zip`, excluding bundled Windows runtime. **Scope:** design integrity, Stage09 selected baseline worker/save cases, Stage11 source path checks, Stage12 ticket CLI.

Command (executed separately for each test pattern from Bible root):

```sh
export PYTHONQUEST_V14_ROOT='/mnt/data/pq_stage12_work/Python Quest 2D'
export PQ11_SOURCE_ROOT='/mnt/data/pq_stage12_work/Python Quest 2D'
python -m unittest discover -s tests -p 'test_biomed_planning.py' -q
python -m unittest discover -s tests -p 'test_stage09_*.py' -q
python -m unittest discover -s tests -p 'test_stage10_*.py' -q
python -m unittest discover -s tests -p 'test_stage11_*.py' -q
python -m unittest discover -s tests -p 'test_stage12_*.py' -q
python tools/work_ticket.py next
```

Results: **7 + 21 + 12 + 12 + 17 = 69 passed, zero failures** after restoring full source content. `next` => `PQ11-001`, no DONE tickets, no validated new missions. Earlier incomplete source extraction caused Stage09/11 source-linked failures; rerunning against complete source passed.

**Not run:** new 76 missions, newly designed runtime protocols, native Windows game launch, measured frame performance, human playtesting or a complete new 152-mission campaign. Static ZIP audit for prior v1.4 is documented in Stage10.

**Risk note:** `tools/work_ticket.py` checks evidence-file structure and consistency, but cannot attest to underlying log truth; independent code review and actual test commands are required.

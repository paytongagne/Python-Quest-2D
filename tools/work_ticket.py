"""Use the supplied ticket engine with the live project ledger, not its pristine template."""
from pathlib import Path
import runpy,sys
ROOT=Path(__file__).resolve().parents[1]
if '--state' not in sys.argv:sys.argv.extend(['--state',str(ROOT/'handoff/12_TASK_STATE.json')])
runpy.run_path(str(ROOT/'planning/tools/work_ticket.py'),run_name='__main__')

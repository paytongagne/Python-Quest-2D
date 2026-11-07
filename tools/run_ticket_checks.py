"""Run ticket regression with durable logs and a protected live-profile digest."""
from pathlib import Path
import hashlib,json,os,re,subprocess,sys,tempfile,platform
ROOT=Path(__file__).resolve().parents[1]
ticket=sys.argv[1]
target=ROOT/'checkpoints'/f'{int(ticket[-3:]):04d}_{ticket}'
target.mkdir(exist_ok=True,parents=True)
live=Path(os.environ.get('LOCALAPPDATA',Path.home()))/'PythonQuest2D/progress.json'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
before=digest(live)
with tempfile.TemporaryDirectory() as tmp:
    env=os.environ.copy();env.update(PYTHONQUEST_SAVE=str(Path(tmp)/'outer-profile.json'),TEMP=tmp,TMP=tmp)
    command=[sys.executable,'-m','unittest','discover','-s','tests','-p','test_*.py','-v']
    run=subprocess.run(command,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=target/'TEST_LOG.txt';log.write_text(run.stdout,encoding='utf8')
    count=re.search(r'Ran (\d+) tests?',run.stdout)
    evidence=dict(command='python -m unittest discover -s tests -p test_*.py -v',host=platform.platform()+' / Python '+platform.python_version()+' / SDL dummy',exit_code=run.returncode,passed=int(count.group(1)) if count and run.returncode==0 else 0,failed=0 if run.returncode==0 else 1,log_path=str(log.relative_to(ROOT)))
    (target/'RUN.json').write_text(json.dumps(evidence,indent=2))
    after=digest(live)
    (target/'PROFILE_ISOLATION.json').write_text(json.dumps(dict(live_save_before=before,live_save_after=after,unchanged=before==after,disposable_profile=True),indent=2))
    print(run.stdout[-3500:])
    if before!=after:raise RuntimeError('Live save changed during test run; stop and investigate')
    sys.exit(run.returncode)

"""Validate content, legacy solutions, and authored script tasks (no dependencies)."""
from __future__ import annotations
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
content=ROOT/'content'/'challenges'
authoring=ROOT/'content'/'authoring'

FUNC_RUNNER='''
import sys,json,contextlib,io,traceback
payload=json.loads(sys.stdin.read())
ns={}
try:
 with contextlib.redirect_stdout(io.StringIO()):
  exec(compile(payload['code'],'<author_solution>','exec'),ns,ns)
 fn=ns[payload['function_name']]
 results=[]
 for c in payload['cases']:
  actual=fn(*c['args'])
  expected=c['expected']
  if type(actual) in (int,float) and type(expected) in (int,float) and type(actual) is not bool and type(expected) is not bool:
   valid=abs(actual-expected)<1e-9
  else:
   valid=type(actual) is type(expected) and actual==expected
  results.append(valid)
 print(json.dumps({'ok':all(results),'results':results}))
except BaseException:
 print(json.dumps({'ok':False,'error':traceback.format_exc()}))
'''
SCRIPT_RUNNER='''
import sys,json,contextlib,io,traceback
payload=json.loads(sys.stdin.read())
ns={}
try:
 s=io.StringIO()
 with contextlib.redirect_stdout(s):
  exec(compile(payload['code'],'<author_solution>','exec'),ns,ns)
 ok=s.getvalue()==payload['expected_stdout']
 for k,v in payload.get('expected_variables',{}).items():
  ok=ok and k in ns and type(ns[k]) is type(v) and ns[k]==v
 print(json.dumps({'ok':bool(ok),'actual_stdout':s.getvalue()}))
except BaseException:
 print(json.dumps({'ok':False,'error':traceback.format_exc()}))
'''

def check_all():
    files=sorted(content.glob('*.json'))
    assert len(files)==24, f'Expected 24 challenges, got {len(files)}'
    ids=set()
    for f in files:
        ch=json.loads(f.read_text(encoding='utf-8'))
        assert f.stem==ch['id'],f
        assert ch['id'] not in ids,f
        ids.add(ch['id'])
        assert ch['zone'] and ch['sequence']>0 and ch['world_effect']
        solution_path=authoring/(ch['id']+'.py')
        assert solution_path.exists(),solution_path
        payload={'code':solution_path.read_text(encoding='utf-8'),**ch}
        runner=FUNC_RUNNER if ch['kind']=='function' else SCRIPT_RUNNER
        if ch['kind']=='function':
            assert len(ch['cases'])>=2
            assert ch['function_name'] in ch['starter_code']
        elif ch['kind']=='script':
            assert 'expected_stdout' in ch
        else:
            raise AssertionError(f'Bad challenge kind: {ch["kind"]}')
        r=subprocess.run([sys.executable,'-I','-S','-c',runner],input=json.dumps(payload),
                         text=True,capture_output=True,timeout=5,check=True)
        result=json.loads(r.stdout)
        assert result['ok'],f'{ch["id"]}: {result}'
        print('PASS',ch['id'],ch['title'])
    maps=sorted((ROOT/'content/maps').glob('*.json'))
    assert len(maps)==6
    for f in maps:
        m=json.loads(f.read_text(encoding='utf-8'))
        assert len(m['tiles'])==m['height']
        assert all(len(r)==m['width'] for r in m['tiles'])
        assert all(t['challenge_id'] in ids for t in m['interactables'])
        assert all(g['requires_challenge'] in ids for g in m['gates'])
    print(f'PASS: {len(files)} challenge solutions, {len(maps)} map schemas')

if __name__=='__main__':
    check_all()

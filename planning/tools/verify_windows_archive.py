"""Static release audit. Does NOT prove an extracted Windows game launches.

Usage: python verify_windows_archive.py archive.zip [--json output.json]
No third-party dependencies, and intentionally does not extract untrusted archive members.
"""
import argparse
import hashlib
import json
from pathlib import PurePosixPath, Path
import sys
import zipfile

REQUIRED = (
    'START_PYTHON_QUEST_2D.bat',
    'play.py',
    'runtime/python.exe',
    'src/python_quest_2d/game/app.py',
    'src/python_quest_2d/core/grade.py',
    'src/python_quest_2d/core/progress.py',
    'tests/test_flight.py',
    'tests/test_expeditions.py',
    'content/universe/destinations.json',
)
FORBIDDEN_SENSITIVE = ('.env', 'id_rsa', 'secrets.json', 'credentials.json')

def inspect(path: Path) -> dict:
    info = {'archive': str(path), 'scope':'STATIC_ONLY_NOT_NATIVE_WINDOWS_LAUNCH', 'passed':False,
            'issues':[], 'warnings':[], 'members':0, 'sha256':None, 'root':None}
    if not path.is_file():
        info['issues'].append('archive missing'); return info
    h=hashlib.sha256()
    with path.open('rb') as f:
        for piece in iter(lambda:f.read(1024*1024),b''):
            h.update(piece)
    info['sha256']=h.hexdigest()
    try:
        with zipfile.ZipFile(path) as z:
            members=z.infolist()
            info['members']=len(members)
            names=[i.filename.replace('\\','/') for i in members if not i.is_dir()]
            if len(names) != len(set(n.lower() for n in names)):
                info['issues'].append('case-insensitive duplicate paths')
            for i in members:
                raw=i.filename.replace('\\','/')
                parts=PurePosixPath(raw).parts
                if raw.startswith('/') or '..' in parts or ':' in raw.split('/')[0]:
                    info['issues'].append('unsafe archive member path: '+raw[:140])
                if ((i.external_attr >>16)&0o170000)==0o120000:
                    info['issues'].append('symbolic link in archive: '+raw[:140])
                lower=raw.lower()
                if any(lower.endswith('/'+p) or lower==p for p in FORBIDDEN_SENSITIVE):
                    info['issues'].append('possible sensitive file: '+raw[:140])
                if '__pycache__/' in lower or lower.endswith('.pyc'):
                    info['warnings'].append('build cache included: '+raw[:120])
            roots=sorted(set(n.split('/')[0] for n in names if '/' in n))
            # Release convention: all game paths live under one top folder.
            if len(roots)==1:
                info['root']=roots[0]
                rel={n[len(roots[0])+1:] for n in names if n.startswith(roots[0]+'/')}
            else:
                rel=set(names)
                info['warnings'].append('release archive has multiple or no top-level directories')
            for r in REQUIRED:
                if r not in rel: info['issues'].append('required file missing: '+r)
            # verify CRCs for all members without extraction; potentially expensive for huge archives
            bad=z.testzip()
            if bad: info['issues'].append('CRC failed: '+str(bad))
    except (zipfile.BadZipFile, OSError, RuntimeError) as e:
        info['issues'].append(type(e).__name__+': '+str(e))
    info['passed']=not info['issues']
    info['warnings_count']=len(info['warnings'])
    if len(info['warnings'])>20:
        info['warnings']=info['warnings'][:20]+['more warnings truncated']
    return info

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path)
    p.add_argument('--json',dest='output',type=Path)
    a=p.parse_args()
    result=inspect(a.archive)
    print(json.dumps(result,indent=2))
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
    return 0 if result['passed'] else 1

if __name__=='__main__':sys.exit(main())

#!/usr/bin/env python3
"""Stage 12 planning/Work utility. Evidence validation is structural, not an independent execution audit."""
import argparse, hashlib, json, pathlib, re, sys
BASE = pathlib.Path(__file__).resolve().parents[1]
CAT = BASE/'backlog/11_IMPLEMENTATION_TICKETS.json'
DEFAULT = BASE/'handoff/12_TASK_STATE.json'


def load(path):
    return json.loads(pathlib.Path(path).read_text(encoding='utf-8'))

def dump_atomic(path, obj):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    t=p.with_suffix(p.suffix+'.tmp')
    t.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    t.replace(p)

def ready(ticket, state):
    states=state['ticket_states']
    return states[ticket['ticket_id']]=='PLANNED' and all(states.get(d)=='DONE' for d in ticket['depends_on'])

def eligible(catalog, state):
    return [t for t in catalog['tickets'] if ready(t,state)]

def brief(t, base=BASE):
    c={'id':t['ticket_id'],'task':t['task'],'kind':t['kind'],'risk':t['risk'],'phase':t['phase'],'dependencies':t['depends_on'],'source_anchors':t['source_anchors'].split(';'),'mission_ids':t['mission_ids'],'expected_acceptance':t['acceptance'],'qa_cases':t['stage10_tests'].split(';'),'release_gates':t['release_gates'],'checkpoint':t['checkpoint'],'scope':'Selected ticket only; preserve baseline and schema-4 profile','quality':'Tests + durable source checkpoint + evidence needed before marking DONE'}
    return c

def evidence_ok(t, e):
    if e.get('ticket_id')!=t['ticket_id']: return 'ticket_id mismatch'
    if not re.fullmatch(r'[a-fA-F0-9]{64}',str(e.get('source_sha256',''))): return 'missing 64-hex source_sha256'
    if not e.get('checkpoint_path'): return 'missing checkpoint_path'
    runs=e.get('test_runs')
    if not isinstance(runs,list) or not runs: return 'no test runs'
    for r in runs:
        if not r.get('command') or not r.get('host') or not r.get('log_path'): return 'test record lacks command/host/log_path'
        if r.get('exit_code')!=0 or not isinstance(r.get('passed'),int) or r['passed']<1 or r.get('failed')!=0: return 'test run not passing'
    requested=set(t['stage10_tests'].split(';'))
    proven=set(e.get('applicable_stage10_cases',[]))
    if not requested.issubset(proven): return 'missing applicable Stage10 QA case IDs'
    mids=set(t.get('mission_ids',[]))
    if mids and not mids.issubset(set(e.get('mission_ids_validated',[]))): return 'mission batch has unvalidated mission IDs'
    return None

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('command',choices=['next','brief','start','block','fail','retry','done','status'])
    ap.add_argument('ticket',nargs='?')
    ap.add_argument('--state',type=pathlib.Path,default=DEFAULT)
    ap.add_argument('--evidence',type=pathlib.Path)
    ap.add_argument('--reason')
    args=ap.parse_args(argv)
    c=load(CAT); state=load(args.state); ids={t['ticket_id']:t for t in c['tickets']}
    if set(ids)!=set(state['ticket_states']): ap.error('ticket state keys do not match catalog')
    if args.command in ('next','status'):
        out={'eligible':[t['ticket_id'] for t in eligible(c,state)],'done':[i for i,s in state['ticket_states'].items() if s=='DONE'],'in_progress':[i for i,s in state['ticket_states'].items() if s=='IN_PROGRESS'],'blocked':[i for i,s in state['ticket_states'].items() if s=='BLOCKED'],'validated_new_missions':len(state.get('implemented_new_mission_ids',[]))}
        print(json.dumps(out,indent=2)); return 0
    if args.ticket not in ids: ap.error('select known ticket ID')
    t=ids[args.ticket]; old=state['ticket_states'][args.ticket]
    if args.command=='brief': print(json.dumps(brief(t),indent=2));return 0
    if args.command=='start':
        if not ready(t,state): ap.error('ticket must be PLANNED with all dependencies DONE')
        state['ticket_states'][args.ticket]='IN_PROGRESS';state['in_progress']=args.ticket
    elif args.command=='fail':
        if old!='IN_PROGRESS': ap.error('only in-progress tickets can fail')
        if not args.reason:ap.error('reason required')
        state['ticket_states'][args.ticket]='TEST_FAILED';state['blocked'][args.ticket]=args.reason
        if state.get('in_progress')==args.ticket: state['in_progress']=None
    elif args.command=='retry':
        if old not in ('TEST_FAILED','BLOCKED'):ap.error('only failed/blocked tickets may retry')
        if not all(state['ticket_states'].get(d)=='DONE' for d in t['depends_on']):ap.error('dependencies not complete')
        state['ticket_states'][args.ticket]='IN_PROGRESS';state['in_progress']=args.ticket
        state['blocked'].pop(args.ticket,None)
    elif args.command=='block':
        if old not in ('IN_PROGRESS','PLANNED','TEST_FAILED'): ap.error('only unfinished tickets can be blocked')
        if not args.reason:ap.error('reason required')
        state['ticket_states'][args.ticket]='BLOCKED';state['blocked'][args.ticket]=args.reason
        if state.get('in_progress')==args.ticket: state['in_progress']=None
    elif args.command=='done':
        if old!='IN_PROGRESS':ap.error('must start ticket first')
        if not args.evidence or not args.evidence.exists():ap.error('existing evidence JSON file required')
        e=load(args.evidence); issue=evidence_ok(t,e)
        if issue:ap.error(issue)
        state['ticket_states'][args.ticket]='DONE';state['completed_tickets'].append(args.ticket)
        state['evidence'][args.ticket]=str(args.evidence)
        if state.get('in_progress')==args.ticket: state['in_progress']=None
        known=set(state['implemented_new_mission_ids']); known.update(t.get('mission_ids',[]))
        state['implemented_new_mission_ids']=sorted(known)
    dump_atomic(args.state,state)
    print(json.dumps({'ticket_id':args.ticket,'old':old,'new':state['ticket_states'][args.ticket]},indent=2));return 0

if __name__=='__main__':
    sys.exit(main())

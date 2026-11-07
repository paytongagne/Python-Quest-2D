from __future__ import annotations
import json, csv
from pathlib import Path
P=Path('/mnt/data/Python_Quest_2D_Preproduction_Bible_v1')
E=P/'engineering'; S=E/'schemas'; EX=E/'examples'
S.mkdir(parents=True,exist_ok=True); EX.mkdir(parents=True,exist_ok=True)
def dump(path,data): path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def schema(name,props,req=(),extra=False,defs=None,desc=None):
  d={'$schema':'https://json-schema.org/draft/2020-12/schema','$id':f'https://pythonquest.local/contracts/v1/{name}.schema.json','title':name,'type':'object','additionalProperties':extra,'required':list(req),'properties':props}
  if defs:d['$defs']=defs
  if desc:d['description']=desc
  dump(S/f'{name}.schema.json',d);return d
string={'type':'string'}; nonempty={'type':'string','minLength':1,'maxLength':128}
identifier={'type':'string','pattern':'^[a-z][a-z0-9_.-]{0,63}$'}
nonneg={'type':'integer','minimum':0}; version={'const':1}
num={'type':'number'}; bounded_text={'type':'string','maxLength':65536}
cell={'type':'array','prefixItems':[{'type':'integer','minimum':0},{'type':'integer','minimum':0}],'minItems':2,'maxItems':2}
string_id_list={'type':'array','items':identifier,'uniqueItems':True,'maxItems':512}
json_value={}
error={'type':'object','additionalProperties':False,'required':['code','message'], 'properties':{
    'code':{'enum':['INVALID_INPUT','SCHEMA_MISMATCH','SYNTAX_ERROR','RUNTIME_ERROR','TEST_FAILED','TIMEOUT','WORKER_CRASH','INVALID_EFFECT','STALE_SNAPSHOT','INVALID_ACTION','COLLISION','ENERGY_EXHAUSTED','MISSING_CAPABILITY','DEVICE_NOT_ADJACENT','UNSUPPORTED_CONTRACT','SAVE_CONFLICT']},
    'message':{'type':'string','maxLength':480},'line':{'type':['integer','null'],'minimum':1},'step':{'type':['integer','null'],'minimum':0},'field':{'type':['string','null'],'maxLength':128},'case_id':{'type':['string','null'],'maxLength':128}}}
legacy_props={'id':identifier,'zone':nonempty,'sequence':{'type':'integer','minimum':1},'kind':{'enum':['script','function','object']},
              'title':{'type':'string','minLength':1,'maxLength':180},'story':bounded_text,'lesson':bounded_text,'objective':bounded_text,'sample':bounded_text,
              'starter_code':bounded_text,'hint':bounded_text,'world_effect':identifier,'cases':{'type':'array','items':{'type':'object'},'maxItems':128},'variants':{'type':'array','items':{'type':'object'},'maxItems':128},
              'expected_stdout':string,'expected_variables':{'type':'object'},'function_name':identifier,'class_name':identifier,'attributes':{'type':'array','items':string},
              'contract':identifier,'simulation':{'enum':['route','expedition','instrument']},'output':{'enum':['path','model']},'difficulty':string,
              'legacy_index':nonneg,'property':string,'pq_extension':{'type':'object','additionalProperties':False,'properties':{
                'extension_schema':version, 'program_contract':string,'device_id':identifier,'contract_ref':string,'fixture_ref':string,'ui_mode':string,'recommended_tier':{'type':'integer','minimum':1,'maximum':5}},'required':['extension_schema']}}
legacy=schema('mission_content',legacy_props,['id','zone','sequence','kind','title','story','lesson','objective','sample','starter_code','hint','world_effect'],True,
              desc='Stage09 additive content contract. Existing v1.4 mission keys remain legal; pq_extension is namespaced.')
legacy['allOf']=[{'if':{'properties':{'kind':{'const':'script'}}},'then':{'required':['expected_stdout']}},
 {'if':{'properties':{'kind':{'const':'function'}}},'then':{'required':['function_name','cases']}},
 {'if':{'properties':{'kind':{'const':'object'}}},'then':{'anyOf':[{'required':['class_name']},{'required':['contract']}]}}]
dump(S/'mission_content.schema.json',legacy)
script_envelope={'kind':{'enum':['legacy_mission','program_plan']},'protocol_version':version,'request_id':identifier,'mission_id':identifier,
 'source':bounded_text,'challenge':{'type':'object'},'observation':{'type':'object'},'program_contract':{'const':'mica.plan.v1'},'fixture_set_id':identifier,'source_hash':{'type':'string','pattern':'^[0-9a-f]{64}$'}}
req=schema('execution_request',script_envelope,['kind','protocol_version','request_id','mission_id','source'])
req['oneOf']=[{'properties':{'kind':{'const':'legacy_mission'}},'required':['challenge']},
              {'properties':{'kind':{'const':'program_plan'}},'required':['observation','program_contract','source_hash']}]
dump(S/'execution_request.schema.json',req)
schema('evaluation_result', {'protocol_version':version,'request_id':identifier,'mission_id':identifier,
 'status':{'enum':['finished','syntax_error','runtime_error','invalid_challenge','timeout','worker_crash','invalid_output','cancelled']},
 'passed':{'type':'boolean'},'passed_count':nonneg,'total_count':nonneg,'line':{'type':['integer','null'],'minimum':1},
 'rows':{'type':'array','items':{'type':'string','maxLength':1024},'maxItems':128},'errors':{'type':'array','items':error,'maxItems':128},
 'effect':json_value,'source_hash':{'type':'string','pattern':'^[0-9a-f]{64}$'},'snapshot_id':identifier},
 ['protocol_version','request_id','mission_id','status','passed','rows','errors','effect'])
observation=schema('observation',{'schema':version,'snapshot_id':identifier,'world_id':identifier,'device_id':identifier,'seed':nonneg,
 'robot':{'type':'object','additionalProperties':False,'required':['id','cell','energy','abilities'],
 'properties':{'id':identifier,'cell':cell,'energy':nonneg,'abilities':string_id_list}},
 'visible':{'type':'object','additionalProperties':False,'required':['width','height','walls','devices'],
 'properties':{'width':{'type':'integer','minimum':1,'maximum':256},'height':{'type':'integer','minimum':1,'maximum':256},
 'walls':{'type':'array','items':cell,'maxItems':8192},'devices':{'type':'array','maxItems':256,'items':{'type':'object','additionalProperties':False,
 'required':['id','cell','state'],'properties':{'id':identifier,'cell':cell,'state':identifier,'capabilities':string_id_list}}}}},
 'objective':{'type':'object','required':['target_id','required_state'],'properties':{'target_id':identifier,'required_state':identifier},'additionalProperties':True},
 'rules':{'type':'object','additionalProperties':False,'required':['max_actions','step_energy','scan_energy'],
 'properties':{'max_actions':{'type':'integer','minimum':1,'maximum':64},'step_energy':nonneg,'scan_energy':nonneg,'interact_energy':nonneg}}},
 ['schema','world_id','robot','visible','objective','rules'])
action_defs={
 'move':{'type':'object','additionalProperties':False,'required':['type','direction'],'properties':{'type':{'const':'move'},'direction':{'enum':['north','south','east','west']}}},
 'scan':{'type':'object','additionalProperties':False,'required':['type','direction'],'properties':{'type':{'const':'scan'},'direction':{'enum':['north','south','east','west']}}},
 'interact':{'type':'object','additionalProperties':False,'required':['type','target'],'properties':{'type':{'const':'interact'},'target':identifier}},
 'wait':{'type':'object','additionalProperties':False,'required':['type','ticks'],'properties':{'type':{'const':'wait'},'ticks':{'type':'integer','minimum':1,'maximum':5}}},
 'report':{'type':'object','additionalProperties':False,'required':['type','label'],'properties':{'type':{'const':'report'},'label':{'type':'string','minLength':1,'maxLength':120}}}}
actions=schema('action_plan',{'schema':version,'snapshot_id':identifier,'program_id':identifier,'actions':{
 'type':'array','maxItems':64,'items':{'oneOf':[{'$ref':'#/$defs/'+s} for s in action_defs]}}},['schema','snapshot_id','actions'],defs=action_defs)
schema('device_intent',{'protocol_version':version,'intent_id':identifier,'snapshot_id':identifier,'device_id':identifier,
 'operation':{'enum':['activate','configure','repair','sample','publish','reset']},'parameters':{'type':'object','maxProperties':64},
 'issued_by':{'enum':['game_reducer','validated_plan']},'expected_revision':nonneg},
 ['protocol_version','intent_id','snapshot_id','device_id','operation','parameters','issued_by','expected_revision'])
schema('world_event',{'protocol_version':version,'event_id':identifier,'sequence':nonneg,'timestamp_tick':nonneg,'world_id':identifier,
 'event_type':{'enum':['program.verified','program.rejected','robot.step','robot.docked','device.state_changed','world.unlock_applied','world.travel_started','world.travel_arrived','xp.awarded','diagnostic.updated','mission.completed','simulation.frame']},
 'subject_id':identifier,'payload':{'type':'object','maxProperties':64},'idempotency_key':identifier},
 ['protocol_version','event_id','sequence','timestamp_tick','world_id','event_type','subject_id','payload','idempotency_key'])
schema('render_snapshot',{'protocol_version':version,'frame_id':nonneg,'world_id':identifier,'logical_tick':nonneg,
 'camera':{'type':'object','additionalProperties':False,'required':['x','y','zoom'],
 'properties':{'x':num,'y':num,'zoom':{'type':'number','exclusiveMinimum':0,'maximum':8}}},
 'entities':{'type':'array','maxItems':1024,'items':{'type':'object','additionalProperties':False,
 'required':['id','sprite','x','y','state'],'properties':{'id':identifier,'sprite':identifier,'x':num,'y':num,'state':identifier,'layer':{'type':'integer','minimum':0,'maximum':100}}}},
 'instruments':{'type':'array','maxItems':32,'items':{'type':'object','additionalProperties':False,
 'required':['id','label','status'],'properties':{'id':identifier,'label':{'type':'string','maxLength':120},'status':identifier,'values':{'type':'array','maxItems':2048,'items':{'type':['number','null']}}}}},
 'effects':{'type':'array','maxItems':128,'items':{'type':'object','additionalProperties':False,'required':['kind','x','y'],
 'properties':{'kind':identifier,'x':num,'y':num,'duration_ticks':nonneg}}},
 'ui':{'type':'object','additionalProperties':False,'required':['objective','notice'],
 'properties':{'objective':{'type':'string','maxLength':180},'notice':{'type':'string','maxLength':320},'show_synthetic_banner':{'type':'boolean'}}}},
 ['protocol_version','frame_id','world_id','logical_tick','camera','entities','instruments','effects','ui'])
program_revision={'type':'object','additionalProperties':True, 'required':['name','source','contract','verified','created_at'],
 'properties':{'name':{'type':'string','maxLength':80},'source':bounded_text,'contract':{'const':'mica.plan.v1'},
 'verified':{'type':'boolean'},'hash':{'type':['string','null'],'pattern':'^[0-9a-f]{64}$'},
 'verified_worlds':{'type':'array','items':identifier,'maxItems':32},'fixture_version':string,
 'created_at':{'type':'string','maxLength':32},'last_verified_at':{'type':['string','null'],'maxLength':32}}}
schema('program_library',{'schema':version,'slots':{'type':'object','additionalProperties':identifier,'maxProperties':16},
 'revisions':{'type':'object','additionalProperties':program_revision,'maxProperties':128},
 'traces':{'type':'array','maxItems':32,'items':{'type':'object','maxProperties':32}}},['schema','slots','revisions','traces'])
schema('runtime_extension',{'schema':version,'device_state':{'type':'object','maxProperties':512},
 'active_job':{'anyOf':[{'type':'null'},{'type':'object','required':['job_id','world_id','snapshot_id','cursor','state'],
   'additionalProperties':True,'properties':{'job_id':identifier,'world_id':identifier,'snapshot_id':identifier,
   'cursor':nonneg,'state':{'enum':['paused','running','recovering']}}}]},
 'last_applied_event_ids':{'type':'array','items':identifier,'uniqueItems':True,'maxItems':1024}},
 ['schema','device_state','active_job','last_applied_event_ids'])
save=schema('save_v4',{
 'schema_version':{'const':4},'player':{'type':'object','required':['zone','x','y','xp'],'additionalProperties':True,
 'properties':{'zone':nonempty,'x':num,'y':num,'xp':{'type':'number','minimum':0}}},
 'completed':string_id_list,'hinted':string_id_list,'revealed':string_id_list,
 'drafts':{'type':'object','additionalProperties':bounded_text},'attempts':{'type':'object','additionalProperties':nonneg},
 'world_flags':{'type':'object'},'review':{'type':'object'},'settings':{'type':'object'},
 'program_library':{'$ref':'program_library.schema.json'},'runtime_v1':{'$ref':'runtime_extension.schema.json'},
 'programs':{'type':'object'},'last_replay':string,'expedition_job':{'type':'object'},'deployment':{'type':'object'},
 'checkpoints':{'type':'object'},'visited_worlds':{'type':'array','items':string}},
 ['schema_version','player','completed','hinted','drafts','attempts','world_flags','review','settings'],True,
 desc='Current v1.4 schema-4 plus additive stage-09 proposed keys; never erase unknown old fields.')
schema('travel_request',{'protocol_version':version,'request_id':identifier,'from_zone':identifier,'to_zone':identifier,
 'source':{'enum':['starmap','journal','physical_exit','quest_script']},
 'preview':{'type':'boolean'},'checkpoint_id':identifier},
 ['protocol_version','request_id','from_zone','to_zone','source','preview'])
schema('travel_result',{'protocol_version':version,'request_id':identifier,'status':{'enum':['allowed','rejected']},
 'reason':{'enum':['ok','busy','locked','unknown_world','unsafe_spawn','invalid_request']},
 'spawn':{'anyOf':[{'type':'null'},{'type':'object','additionalProperties':False,'required':['x','y'], 'properties':{'x':num,'y':num}}]},
 'requires_mission':{'type':['string','null']},'preview':{'type':'boolean'}},
 ['protocol_version','request_id','status','reason','spawn','requires_mission','preview'])
registry={
 'stage':9,'protocol_revision':'pq-architecture-v1','status':'DESIGN_ONLY','source_baseline':'Python Quest 2D v1.4 (76 shipped missions; profile schema 4)',
 'schemas':{p.stem:{'path':f'engineering/schemas/{p.name}','version':1,'wire_status':'PROPOSED' if p.stem not in ('mission_content.schema','save_v4.schema') else 'LEGACY_COMPATIBLE_SUPERSET'} for p in sorted(S.glob('*.json'))},
 'max_limits':{'source_bytes':65536,'worker_timeout_seconds':3,'worker_stdout_chars':8192,'worker_json_response_bytes_proposed':262144,'max_plan_actions':64,
 'max_render_entities':1024,'max_render_instruments':32,'max_active_traces':32,'max_program_revisions':128},
 'game_source_seams':{
 'legacy_entry':'src/python_quest_2d/core/grade.py:grade(ch, code, timeout_s=3)',
 'legacy_worker':'src/python_quest_2d/core/worker.py:evaluate(ch, code)',
 'legacy_result':'src/python_quest_2d/game/app.py:collect()',
 'expedition_result':'src/python_quest_2d/game/expedition.py:accept()',
 'legacy_save':'src/python_quest_2d/core/progress.py:load/save/award',
 'legacy_content':'src/python_quest_2d/core/challenges.py:LESSONS',
 'legacy_travel':'src/python_quest_2d/game/expedition.py:travel(index)',
 'legacy_render':'src/python_quest_2d/game/app.py:draw()'},
 'protected_legacy_fields':['completed','hinted','revealed','drafts','attempts','world_flags','review','settings','player','programs','last_replay','expedition_job','deployment','checkpoints','visited_worlds'],
 'new_optional_save_fields':['program_library','runtime_v1'],
 'references':['docs/02_SOURCE_AUDIT.md','docs/03_PROGRAMMABLE_WORLD.md','docs/07_CURRICULUM_AND_ASSESSMENT.md','docs/08_BIOMEDICAL_ENDGAME.md']}
dump(E/'09_CONTRACT_REGISTRY.json',registry)
state_machines={
 'stage':9,'design_status':'PROPOSED','machines':{
 'evaluation':{'initial':'idle','states':['idle','submitted','running','passed','failed','timeout','crashed','cancelled'],
  'transitions':[['idle','submit','submitted'],['submitted','spawn','running'],['running','valid_result_pass','passed'],['running','valid_result_fail','failed'],['running','deadline','timeout'],['running','exception','crashed'],['submitted','cancel','cancelled'],['running','cancel','cancelled']]},
 'deployment':{'initial':'draft','states':['draft','verified','ready','running','paused','committed','rejected','cancelled','recovery'],
  'transitions':[['draft','worker_verified','verified'],['verified','parent_revalidated','ready'],['verified','parent_rejected','rejected'],['ready','deploy','running'],['running','pause','paused'],['paused','resume','running'],['running','safe_milestone','committed'],['running','revalidate_failed','rejected'],['running','quit','recovery'],['recovery','resume_checkpoint','paused'],['ready','cancel','cancelled'],['paused','cancel','cancelled']]},
 'travel':{'initial':'idle','states':['idle','requested','allowed','rejected','departing','arriving','ready'],
  'transitions':[['idle','request','requested'],['requested','validated','allowed'],['requested','denied','rejected'],['allowed','start_departure','departing'],['departing','load_world','arriving'],['arriving','safe_spawn','ready'],['rejected','dismiss','idle'],['ready','acknowledge','idle']]},
 'device':{'initial':'offline','states':['offline','diagnosed','repairing','online','degraded'],
  'transitions':[['offline','inspect','diagnosed'],['diagnosed','begin_validated_repair','repairing'],['repairing','commit_success','online'],['repairing','repair_failed','degraded'],['degraded','retry','repairing'],['online','fault_event','degraded']]},
 'profile':{'initial':'unloaded','states':['unloaded','validated','migrating','ready','dirty','writing','committed','quarantined'],
  'transitions':[['unloaded','parse_valid','validated'],['unloaded','parse_invalid','quarantined'],['validated','schema_known','ready'],['validated','needs_migration','migrating'],['migrating','backup_and_upgrade','ready'],['ready','game_update','dirty'],['dirty','write_temp','writing'],['writing','atomic_replace','committed'],['committed','continue','ready']]}
 }}
dump(E/'09_STATE_MACHINES.json',state_machines)
adapters=[
 ('A01','core.challenges.LESSONS','content/expeditions/*.json','mission_content','Keep existing map/lesson keys. Add optional pq_extension (design-only).','Read-only wrapper; new optional fields; no relabeling IDs.'),
 ('A02','core.grade.grade','core/grade.py','execution_request','Wrap legacy ch+code only at new API boundary; pass unmodified ch to v1.4 grade().','No worker rewrite for legacy paths.'),
 ('A03','core.worker.evaluate','core/worker.py','evaluation_result','Normalize legacy status/rows/line/effect; reject malformed/NaN/over-budget outputs on parent.','Keep legacy status strings, do not assume worker isolating hostile code.'),
 ('A04','game.app.Game.collect','game/app.py','evaluation_result','Feature-gated new plan branch, independent parent validator before effects.','Maintain hydro route/instrument and expeditions.accept fallback.'),
 ('A05','game.expedition.Expeditions.accept','game/expedition.py','action_plan','Legacy expedition.validate first; feature-gated ProgramRuntime on new mission contracts.','Do not mutate p[programs]/p[last_replay].'),
 ('A06','game.world.World.nearest','game/world.py','device_intent','Device registry maps interacted hardware to canonical IDs and allowed intents.','Existing dictionaries remain valid.'),
 ('A07','game.app.Game.update_field','game/app.py','world_event','Drive proposed reducer from fixed logical ticks; emit bounded events.','Do not change existing rover flight timers without migration test.'),
 ('A08','game.expedition.Expeditions.travel','game/expedition.py','travel_request','Wrap current destination lookups + busy/locked/preview checks; safe spawn fallback.','Preserve checkpoint/astra_return/visited_worlds.'),
 ('A09','game.app.Game.draw','game/app.py','render_snapshot','Construct read-only draw snapshot from validated game-owned state; UI never calls learner functions.','Do not replace current renderer in one sprint.'),
 ('A10','core.progress.load/save/award','core/progress.py','save_v4','Add optional program_library/runtime_v1 defaults; preserve unknown fields; safe profile backups.','Do not bump schema until implemented migration.'),
 ('A11','game.diagnostics.draw','game/diagnostics.py','world_event','Read bounded event trace and replay timeline; no raw object repr in frame loop.','Keep 768x576 view unobstructed.'),
 ('A12','game.instruments + game.planet_art','game/instruments.py','render_snapshot','Use finite, nullable signal samples and toy mesh layers; label simulated status.','Synthetic fixtures only; do not import Qt.')
]
with (E/'09_SOURCE_ADAPTERS.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['adapter_id','source_entry','source_path','contract','transformation','compatibility_rule']);w.writerows(adapters)
matrix=[
 ('v2','v3 then v4','progress.py load()','backup .pre-greenline.json and .pre-expedition.json','migration unchanged','keep all legacy known/unknown fields','verify first-start restored old profiles'),
 ('v3','v4','progress.py load()','backup .pre-expedition.json','migration unchanged','keep all legacy known/unknown fields','verify rover replay and XP'),
 ('v4','v4 plus additive keys','stage09 design','no migration needed for optional namespaced fields','program_library/runtime_v1 absent -> default view only, not automatic overwrite','preserve programs, deployments, checkpoints, visited worlds','old v4 profile test + unknown field round-trip'),
 ('future v5','explicit v4->v5 only when needed','implementation deferred','backup .pre-architecture.json before write','never assume existing loader handles version safely','reject >supported schema for writes; preserve original bytes','forced corrupt/unsupported case must not replace original'),
 ('damaged JSON','quarantine + safe new profile','current progress.py load()','timestamp damaged backup','current behavior returns fresh','never award XP to corrupted body','copy of bad JSON preserved'),
 ('unknown keys','preserve','current progress.py save()','same serialized keys on roundtrip','merge defaults only; never rebuild profile with fresh()','retain extensions unrelated to architecture','sentinel nested unknown key survives'),
 ('idempotent XP','no re-award','current progress.py award()','none','check completed first','never rewrite completed IDs or unique world_effect','award same mission twice -> second returns 0'),
 ('mid-deployment','last safe point','planned runtime_v1','atomic commit on safe milestone only','recover as paused, revalidate before resume','legacy expedition_job/deployment unchanged','quit after each step + resume no duplicate effects'),
 ('source revision changed','invalidate verification','planned program_library','original draft retained','source sha256 and fixture version mismatch -> unverified','do not edit previous equipped revision in place','edited code cannot use prior verification'),
 ('unreachable legacy checkpoint','safe nearest accessible spawn','planned travel adapter','preserve old checkpoint values','feature-gated recovery only on entering world','never teleport on load silently without diagnostics','loading player trapped in new prop can move out')
]
with (E/'09_SAVE_COMPATIBILITY_MATRIX.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.writer(f);w.writerow(['input_state','proposed_state','source','backup','behavior','protected_data','test_gate']);w.writerows(matrix)
# Save design-positive examples anchored to the proposed schemas.
obs={'schema':1,'snapshot_id':'snap-orion-01','world_id':'orion_moon','device_id':'relay_a','seed':7,
 'robot':{'id':'mica','cell':[1,1],'energy':12,'abilities':['move','scan','interact']},
 'visible':{'width':6,'height':5,'walls':[[2,2],[3,2]],'devices':[{'id':'relay_a','cell':[3,1],'state':'offline','capabilities':['activate']}]},
 'objective':{'target_id':'relay_a','required_state':'online'},'rules':{'max_actions':64,'step_energy':1,'scan_energy':2,'interact_energy':1}}
examples={
 'observation':obs,
 'action_plan':{'schema':1,'snapshot_id':'snap-orion-01','program_id':'program-01','actions':[{'type':'move','direction':'east'},{'type':'interact','target':'relay_a'},{'type':'report','label':'relay restored'}]},
 'device_intent':{'protocol_version':1,'intent_id':'intent-01','snapshot_id':'snap-orion-01','device_id':'relay_a','operation':'activate','parameters':{},'issued_by':'validated_plan','expected_revision':0},
 'world_event':{'protocol_version':1,'event_id':'evt-01','sequence':1,'timestamp_tick':11,'world_id':'orion_moon','event_type':'device.state_changed','subject_id':'relay_a','payload':{'from':'offline','to':'online'},'idempotency_key':'relay_a-restore-01'},
 'render_snapshot':{'protocol_version':1,'frame_id':51,'world_id':'orion_moon','logical_tick':11,'camera':{'x':128,'y':64,'zoom':1},
 'entities':[{'id':'mica','sprite':'rover_mica','x':64,'y':32,'state':'idle','layer':10}],
 'instruments':[],'effects':[{'kind':'spark','x':96,'y':32,'duration_ticks':4}],
 'ui':{'objective':'Restore the relay','notice':'Mica docked','show_synthetic_banner':False}},
 'travel_request':{'protocol_version':1,'request_id':'travel-01','from_zone':'orientation','to_zone':'orion_moon','source':'starmap','preview':False},
 'travel_result':{'protocol_version':1,'request_id':'travel-01','status':'allowed','reason':'ok','spawn':{'x':96,'y':96},'requires_mission':None,'preview':False},
 'execution_request':{'kind':'legacy_mission','protocol_version':1,'request_id':'req-01','mission_id':'orientation_01','source':'print("System online")\n',
  'challenge':{'id':'orientation_01','kind':'script','expected_stdout':'System online\n'}},
 'evaluation_result':{'protocol_version':1,'request_id':'req-01','mission_id':'orientation_01','status':'finished','passed':True,'passed_count':1,'total_count':1,
  'line':None,'rows':['PASS  1  stdout expected'], 'errors':[],'effect':None},
 'program_library':{'schema':1,'slots':{},'revisions':{},'traces':[]},
 'runtime_extension':{'schema':1,'device_state':{},'active_job':None,'last_applied_event_ids':[]},
 'save_v4':{'schema_version':4,'player':{'zone':'orientation','x':96,'y':96,'xp':0},'completed':[],'hinted':[],
  'drafts':{},'attempts':{},'world_flags':{},'review':{},'settings':{'sound':True},'unknown_extension':{'keep':True}},
 'mission_content':{'id':'workshop_09','zone':'workshop','sequence':9,'kind':'function','title':'Repair the Assembly Queue',
 'story':'The conveyor needs a scheduling plan.','lesson':'Use a deque.','objective':'Return FIFO processed job IDs.',
 'sample':'[A,B] -> [A,B]','starter_code':'def process_jobs(jobs, capacity):\n    pass\n','hint':'Use collections.deque.',
 'function_name':'process_jobs','cases':[{'args':[['A','B'],1],'expected':['A','B']}], 'world_effect':'workshop_machine_9',
 'pq_extension':{'extension_schema':1,'program_contract':'workshop.queue.v1','device_id':'assembly_line'}}
}
for k,v in examples.items():dump(EX/(k+'.valid.json'),v)
# Explicitly invalid protocol examples used for negative tests; filename -> schema mapping
bad={
 'action_plan_unknown_action':('action_plan',{'schema':1,'snapshot_id':'snap-orion-01','actions':[{'type':'delete_world','target':'relay_a'}]}),
 'action_plan_extra_field':('action_plan',{'schema':1,'snapshot_id':'snap-orion-01','actions':[{'type':'move','direction':'east','world_flags':True}]}),
 'execution_request_missing_source':('execution_request',{'kind':'legacy_mission','protocol_version':1,'request_id':'req-01','mission_id':'orientation_01','challenge':{'id':'orientation_01'}}),
 'evaluation_result_unknown_status':('evaluation_result',{'protocol_version':1,'request_id':'req-01','mission_id':'orientation_01','status':'SUPER_PASS','passed':True,'rows':[],'errors':[],'effect':None}),
 'observation_negative_energy':('observation',dict(obs,robot={**obs['robot'],'energy':-1})),
 'world_event_unknown_type':('world_event',dict(examples['world_event'],event_type='filesystem.delete')),
 'render_snapshot_untrusted_code':('render_snapshot',dict(examples['render_snapshot'],code='exec(...)')),
 'program_library_missing_source':('program_library',{'schema':1,'slots':{},'revisions':{'p1':{'name':'fake','contract':'mica.plan.v1','verified':True,'created_at':'today'}},'traces':[]}),
 'save_v4_unsupported_version':('save_v4',dict(examples['save_v4'],schema_version=5)),
 'travel_result_bad_reason':('travel_result',dict(examples['travel_result'],reason='teleport_anywhere')),
 'device_intent_untrusted_actor':('device_intent',dict(examples['device_intent'],issued_by='learner_python')),
 'mission_content_script_missing_expected':('mission_content',dict(examples['mission_content'],kind='script')),
}
manifest=[]
for name,(target,data) in bad.items(): dump(EX/(name+'.invalid.json'),data);manifest.append({'file':f'{name}.invalid.json','schema':target})
dump(E/'09_NEGATIVE_EXAMPLES.json',manifest)
print('Generated',len(list(S.glob('*.schema.json'))),'schemas;',len(examples),'valid;',len(bad),'invalid examples')

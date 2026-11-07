"""Build stage-08 planning catalogs from existing frozen preproduction outline."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
psv=ROOT/'missions/mission_blueprints.psv'
base_cases={
 'helix_bio_05':('empty; constant; negative range; nonfinite rejection','[0,5,10] -> [0,.5,1]','calibration gallery'),
 'helix_bio_06':('prefix averages; window>length; invalid window; no mutation','[1,3,5],2 -> [1,2,4]','calibration gallery'),
 'helix_bio_07':('strict interior peaks; plateaus; minimum spacing; exact threshold','[0,3,0,4,0], threshold=3, distance=1 -> [1,3]','calibration gallery'),
 'helix_bio_08':('timestamp index multiplication; missing marker; fraction intervals','3 samples at interval 5ms -> [0,5,10]','calibration gallery'),
 'helix_bio_09':('one-to-one nearest; tie earlier timestamp; stable sort','A@100ms,B@101ms,tolerance2 -> pair','streaming wing'),
 'helix_bio_10':('unsorted/duplicate seq; large gaps bounded','[4,6,7] -> [5]','streaming wing'),
 'helix_bio_11':('empty clean_mean=null; missing not zero; flags mismatch','2 clean + 1 artifact -> total3/clean2/artifact1','streaming wing'),
 'helix_bio_12':('only full windows; overlap; positive size/step','[1,2,3,4],size3,step1 -> [[1,2,3],[2,3,4]]','streaming wing'),
 'helix_bio_13':('OFFLINE/ONLINE pair; duplicate state; open outage','A OFFLINE at 10, ONLINE at 20 -> one [10,20] outage','incident room'),
 'helix_bio_14':('valid frame canonical shape; invalid schema; bool-as-int; MISSING null','SYN_A seq0 0ms OK → valid, NaN/string → reject','incident room'),
 'helix_bio_15':('simulated arrivals; capacity; FIFO; drop newest; invalid quarantine','3 same-tick frames, capacity2 → 1 drop, 2 processed','incident room'),
 'helix_bio_16':('mixed channel rates; no frames; policy invalid; restart','clean dual channel → calibrated summary, corrupted → no restore','incident boss'),
 'aurora_ep_05':('basis orthonormal; rotated axes; invalid dimension','[1,2,3] projected to XY -> [1,2]','geometry lab'),
 'aurora_ep_06':('distance ties; contact filter; k zero; duplicate id','origin, A@(1,0,0), B@(2,0,0),k1 -> [A]','geometry lab'),
 'aurora_ep_07':('exact sample point; no sample; power positive; finite','equal-distance samples voltage1,3 -> 2','geometry lab'),
 'aurora_ep_08':('negative LAT; stable order; missing timestamp','time[100,125],reference100 -> LAT[0,25]','geometry lab'),
 'aurora_ep_09':('inclusive min confidence; bad contact; wrong frame','contact True confidence .8 threshold .8 -> accepted','topology gallery'),
 'aurora_ep_10':('revised vertex_count required; isolated vertex; bad face','triangle 0,1,2 vertex_count4 -> 3 connected + isolated 3','topology gallery'),
 'aurora_ep_11':('revised nullable uncovered vertices; exact hit; radius','vertex exactly matching voltage2 ->2; no neighbor -> null','topology gallery'),
 'aurora_ep_12':('anchor-group nontransitive; equal features; sorted','two identical toy features -> same group','topology gallery'),
 'aurora_ep_13':('MOVE/ROTATE/RESET sequence; bounds; transform validity','MOVE +1x from origin -> [1,0,0]','map control'),
 'aurora_ep_14':('time ordering; duplicate ID; buffer full; malformed','two valid unique events -> two accepted ids','map control'),
 'aurora_ep_15':('synthetic provenance; duplicate id; invalid mesh; gaps','clean toy session -> pass true and known counts','map control'),
 'aurora_ep_16':('coverage nullable; audit; dual layers; crash/replay','clean toy shell -> voltage + LAT + audit in result','mapping boss'),
}
assert len(base_cases)==24
rows=[]
with psv.open(encoding='utf8',newline='') as f:
 reader=csv.reader((line for line in f if line.strip() and not line.startswith('#')),delimiter='|')
 for v in reader:
  if len(v)<10:
   raise RuntimeError(f'Unexpected outline row {v}')
  zone,sequence,title,topic,api,action,effect,edges,example,tier=v[:10]
  if zone not in ('helix_bio','aurora_ep'):
   continue
  ident=f'{zone}_{int(sequence):02d}'
  fixture='helix_clean.json + helix_faults.json' if zone=='helix_bio' else 'aurora_toy_chamber.json'
  cases=base_cases[ident]
  if ident=='aurora_ep_10':
   api='mesh_neighbors(faces,vertex_count)->dict[int,list[int]]'
  if ident=='aurora_ep_11':
   api='color_vertices(vertices,samples,radius)->list[float|null]'
  rows.append(dict(mission_id=ident,world=zone,sequence=sequence,title=title,concept=topic,
   planned_signature=api,player_objective=action,visible_world_effect=effect,
   key_edge_tests=cases[0],golden_example=cases[1],encounter_area=cases[2],
   fixture=fixture,scaffold_level=tier,status='DESIGN_ONLY',
   worker_boundary='subprocess validated JSON',game_validation='verify canonical result before effect',
   save_policy='preserve prior IDs+XP; idempotent completion; retain draft'))
assert len(rows)==24
out=ROOT/'missions/biomed_24_contracts.csv'
with out.open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

scenario_rows=[]
for r in rows:
 m=r['mission_id']
 cases=[
  ('positive','Golden fixture output matches documented contract',f'Golden example: {r["golden_example"]}',
   'Validated real Python output; world event fires once; first completion only awards XP'),
  ('edge',r['key_edge_tests'],'Targeted boundary/invalid fixture returns documented value or clear error; draft preserved',
   'No false success, no irreversible world mutation, no crash'),
  ('integration',f'World device: {r["visible_world_effect"]}',
   'Renderer uses independently verified worker JSON snapshot; accessible inspect mode','Visible state change matches computed result and persists after restart'),
  ('save_regression','Quit or replay after prior completion',
   'Complete, save, restart, replay same program and compare canonical trace/result',
   'Same state, same hash, no extra XP, no existing completion/draft erased'),
 ]
 for label,description,input_case,expected in cases:
  scenario_rows.append(dict(mission_id=m,case_type=label,description=description,
   fixture=r['fixture'],test_input_or_procedure=input_case,expected_outcome=expected,
   automation_target='unit+worker+game regression' if label!='integration' else 'headless state test + manual screenshot',
   status='PLANNED_NOT_IMPLEMENTED'))
out=ROOT/'tests/biomed_acceptance.csv'
with out.open('w',newline='',encoding='utf8') as f:
 w=csv.DictWriter(f,fieldnames=list(scenario_rows[0]));w.writeheader();w.writerows(scenario_rows)
print('Generated',len(rows),'mission design contracts and',len(scenario_rows),'acceptance scenarios')

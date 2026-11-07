from pathlib import Path
import json
base=Path(__file__).resolve().parents[1]
def edit(file,old,new):
    p=base/file
    s=p.read_text(encoding="utf-8")
    assert old in s
    p.write_text(s.replace(old,new),encoding="utf-8")
worker="src/python_quest_2d/core/worker.py"
edit(worker,"import contextlib","import ast\nimport contextlib")
edit(worker,"    cases = ch.get(\"cases\", [{}])",'    cases = ch.get("cases", [{}]+ch.get("variants",[]))')
edit(worker,"                exec(compiled, ns)",'''                program=compiled
                if "override" in case:
                    name,value=next(iter(case["override"].items()))
                    tree=ast.parse(code)
                    for node in tree.body:
                        targets=node.targets if isinstance(node,ast.Assign) else [node.target] if isinstance(node,ast.AnnAssign) else []
                        if any(isinstance(t,ast.Name) and t.id==name for t in targets):
                            node.value=ast.copy_location(ast.Constant(value=value),node)
                            break
                    else:
                        raise ValueError("Assign "+name+" at the top level so alternate inputs can be tested.")
                    program=compile(tree,"terminal.py","exec")
                exec(program, ns)''')
edit(worker,'expected = ch["expected_stdout"]','expected = case.get("expected_stdout",ch["expected_stdout"])')
edit(worker,'for k,v in ch.get("expected_variables",{}).items():','for k,v in (ch.get("expected_variables",{}) | case.get("override",{})).items():')
edit(worker,'detail = f"stdout expected','detail = (f"{case[\'override\']}  " if "override" in case else "") + f"stdout expected')
for seq,name,value,out in [(3,"pilot","Sam","Pilot: Sam"),(4,"fuel",4,"WAIT"),(4,"fuel",10,"READY")]:
    p=base/f"content/challenges/orientation_0{seq}.json"
    ch=json.loads(p.read_text())
    ch.setdefault("variants",[]).append({"override":{name:value},"expected_stdout":out+"\n"})
    p.write_text(json.dumps(ch,indent=2)+"\n")
app="src/python_quest_2d/game/app.py"
edit(app,"from pathlib import Path","from pathlib import Path\nfrom datetime import date")
edit(app,'self.notice="PIP: Approach the glowing console in Bay 01."','self.notice="PIP: Astra lost power. Approach the Bay 01 console to start repairs." if not self.p["completed"] else "PIP: Welcome back, engineer. Check the deck systems for your next repair."')
edit(app,'        elif self.scene=="pause" and k==pg.K_q:', '''        elif self.scene=="pause" and k==pg.K_r:
            self.p["settings"]["reduced_motion"]=not self.p["settings"].get("reduced_motion",False)
            self.persist()
        elif self.scene=="pause" and k==pg.K_q:''')
edit(app,"self.accent,pg.time.get_ticks(),self.opening","self.accent,0 if self.p['settings'].get('reduced_motion') else pg.time.get_ticks(),{} if self.p['settings'].get('reduced_motion') else self.opening")
edit(app,r'''else 'off'}\nQ     Save''',r'''else 'off'}\nR     Reduced motion {'on' if self.p['settings'].get('reduced_motion') else 'off'}\nQ     Save''')
edit(app,'                    label(s,"Esc   Return to station",216,530,16,MUTED,True)','''                    due=[LESSONS[k]["title"] for k,d in self.p["review"].items() if k in LESSONS and d<=date.today().isoformat()]
                    if due:
                        wrapped(s,"Practice due: "+due[0],216,503,650,16,GOLD)
                    label(s,"Esc   Return to station",216,548,16,MUTED,True)''')
edit("pyproject.toml",'version = "0.0.1"','version = "1.0.0"')
edit("pyproject.toml","Build-ready scaffold for a local 2D Python learning adventure","Astra Research Facility: an offline Python learning adventure")
for p in (base/"src").rglob("__init__.py"):
    p.write_text('"""Python Quest 2D."""\n')


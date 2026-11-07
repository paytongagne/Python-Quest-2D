"""Detailed readouts are opt-in device interfaces, never world-sized scenery."""

import pygame as pg
from .art import INK, PANEL, WHITE, MINT, GOLD, MUTED, label, wrapped, rect
from ..core.challenges import LESSONS
from . import planet_art


def draw(s, g, key):
    s.fill(INK)
    ch = LESSONS[key]
    label(s, "DEVICE DIAGNOSTICS / " + key.upper(), 32, 25, 16, g.accent, True)
    label(s, ch["title"], 32, 60, 30)
    value = g.p.get("programs", {}).get(key)
    if g.world.zone == "orion_moon":
        panel = pg.Surface((620, 370))
        panel.fill(PANEL)
        job = g.p.get("expedition_job")
        step = (
            job["step"]
            if job and job["key"] == key
            else max(0, len(value) - 1)
            if isinstance(value, list)
            else 0
        )
        planet_art.board(panel, key, ch, value, pg.time.get_ticks(), step)
        s.blit(panel, (234, 140))
    elif g.world.zone == "workshop":
        rect(s, PANEL, 100, 140, 888, 370)
        if key=='workshop_08':
            label(s,'SERVICE LOG / active test fixture',130,166,18,g.accent,True)
            for row,line in enumerate(ch['cases'][0]['text'].splitlines()):
                label(s,f'{row+1:02}  {line.strip()}',130,214+row*34,19,GOLD if line.strip().startswith('ERROR:') else MUTED,True)
            label(s,'ERROR RECORDS FOUND',130,405,15,MINT,True)
            label(s,'Awaiting program' if value is None else str(value),130,435,28,WHITE)
        elif value is None:
            wrapped(s,'No tested object state yet. E opens the programming console.',130,170,824,20,WHITE)
        elif isinstance(value,dict) and 'state' in value:
            y=170
            for i,state in enumerate(value['state'],1):
                label(s,f'DEVICE {i:02}',130,y,15,g.accent,True)
                y=wrapped(s,'   '.join(f'{k.replace("_"," ")}: {v}' for k,v in state.items()),130,y+26,824,20,WHITE,True)+26
            if value.get('returns'):wrapped(s,'Method results: '+str(value['returns']),130,y,824,18,MINT,True)
        elif isinstance(value,list):
            label(s,'MACHINE RESPONSE',130,170,16,g.accent,True)
            for i,row in enumerate(value):
                text=' / '.join(f'{k}: {v}' for k,v in row.items()) if isinstance(row,dict) else str(row)
                label(s,f'{i+1:02}  {text}',130,215+i*43,20,GOLD if row=='fault' else WHITE,True)
        else:
            wrapped(s,'\n\n'.join(f'{k.title()}: {v}' for k,v in value.items()),130,170,824,20,WHITE,True)
    else:
        panel = pg.Surface((1088, 690))
        panel.fill(INK)
        planet_art.display(
            panel,
            g.world,
            g.p.get("programs", {}),
            0 if g.p["settings"].get("reduced_motion") else pg.time.get_ticks(),
        )
        s.blit(panel.subsurface((450, 260, 540, 290)), (274, 170))
    label(
        s,
        "Validated output" if value is not None else "Awaiting a verified program",
        32,
        552,
        18,
        MINT if value is not None else GOLD,
    )
    wrapped(
        s,
        "Your code changes the machine in the world. Detailed data stay here so the environment remains clear.",
        32,
        585,
        1000,
        17,
        MUTED,
    )
    label(s, "E Program     O / Esc Return to the world", 32, 647, 17, MINT, True)

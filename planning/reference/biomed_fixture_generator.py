"""Generate ORIGINAL, SYNTHETIC toy engineering fixtures for Python Quest.

Planning-only sample data. Not real medical signals, not anatomy, not diagnosis.
No patient records, no vendor implementation, no third-party dependencies.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / 'fixtures'
BASE = [0.0, 0.1, -0.2, 1.0, -0.3, 0.2, 0.1, 0.0]


def dump(name: str, obj: object) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(json.dumps(obj, indent=2, sort_keys=True, allow_nan=False) + '\n', encoding='utf8', newline='\n')


def build_clean() -> dict:
    channels = {}
    for channel, phase, scale in (('SYN_A', 0, 1.0), ('SYN_B', 2, 0.6)):
        frames = []
        for i in range(64):
            val = BASE[(i - phase) % len(BASE)] * scale
            # Explicit deterministic toy baseline, no random/clinical process.
            val = round(val + ((i % 16) - 8) * 0.003, 6)
            frames.append({
                'schema': 'toy-biomed-v1', 'source': 'SYNTHETIC_ONLY',
                'channel': channel, 'seq': i, 'time_ms': float(i * 4),
                'value': val, 'unit': 'toy_u', 'quality': 'OK',
            })
        channels[channel] = frames
    return {
        'fixture': 'HELIX_CLEAN_V1', 'description': 'Fictional two-channel test trace; 250 toy samples per second',
        'generator_version': 1, 'source': 'SYNTHETIC_ONLY',
        'sampling_hz': 250, 'channels': channels,
    }


def build_faults(clean: dict) -> dict:
    stream = []
    for frame in clean['channels']['SYN_A'][:20]:
        if frame['seq'] == 5:
            # Index is still represented by explicit data-loss record.
            lost = {**frame, 'value': None, 'quality': 'MISSING'}
            stream.append({'arrival_tick': 3, 'frame': lost})
            continue
        if frame['seq'] == 12:
            continue  # No sequence record, detect missing sequence 12.
        tick = frame['seq'] // 3
        stream.append({'arrival_tick': tick, 'frame': frame})
    duplicate = dict(clean['channels']['SYN_A'][6])
    stream.insert(11, {'arrival_tick': 3, 'frame': duplicate})
    # Arrival deliberately out of event-time order; event-time remains valid.
    stream.insert(9, {'arrival_tick': 2, 'frame': dict(clean['channels']['SYN_A'][16])})
    invalid = dict(clean['channels']['SYN_A'][10])
    invalid['value'] = 'not-a-number'
    stream.append({'arrival_tick': 7, 'frame': invalid})
    return {
        'fixture': 'HELIX_FAULTS_V1', 'source': 'SYNTHETIC_ONLY',
        'generator_version': 1, 'policy': 'validate, dedupe by channel+seq, drop newest on queue overflow',
        'events': stream,
        'expected_flags': {'explicit_missing_seq': 5, 'absent_seq': 12, 'duplicate_seq': 6,
                           'out_of_order_event_seq': 16, 'invalid_value_seq': 10},
    }


def build_chamber() -> dict:
    vertices = [[0.0, 0.0, 1.5], [0.0, 0.0, -1.3],
                [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
                [0.0, 0.9, 0.0], [0.0, -0.9, 0.0]]
    faces = [[0, 2, 4], [0, 4, 3], [0, 3, 5], [0, 5, 2],
             [1, 4, 2], [1, 3, 4], [1, 5, 3], [1, 2, 5]]
    specimens = [
        ('MAP_001', 0, 1.1, 100.0, True, 0.95),
        ('MAP_002', 1, 1.6, 130.0, True, 0.85),
        ('MAP_003', 2, 2.2, 90.0, True, 0.91),
        ('MAP_004', 3, 0.5, 150.0, True, 0.96),
        ('MAP_005', 4, 1.8, 110.0, True, 0.80),
        ('MAP_006', 5, 0.0, 175.0, True, 0.99),
        ('MAP_007', 2, 9.9, 200.0, False, 0.99),
        ('MAP_008', 1, 8.4, 225.0, True, 0.45),
    ]
    points = []
    for sid, vertex, voltage, time, contact, conf in specimens:
        points.append({
            'id': sid, 'source': 'SYNTHETIC_ONLY', 'position': vertices[vertex][:],
            'frame': 'TOY_CHAMBER_V1', 'voltage': voltage, 'time_ms': time,
            'contact': contact, 'confidence': conf, 'channel': 'SYN_A',
        })
    return {
        'fixture': 'AURORA_TOY_CHAMBER_V1', 'source': 'SYNTHETIC_ONLY',
        'generator_version': 1,
        'mesh': {'mesh_id': 'CHAMBER_OCTAHEDRON_V1', 'frame': 'TOY_CHAMBER_V1',
                 'vertices': vertices, 'faces': faces},
        'policy': {'min_confidence': 0.8, 'contact_required': True, 'idw_power': 2,
                   'lat_reference_ms': 100.0, 'uncovered_value': None},
        'observations': points,
    }


def generate() -> None:
    clean = build_clean()
    dump('helix_clean.json', clean)
    dump('helix_faults.json', build_faults(clean))
    dump('aurora_toy_chamber.json', build_chamber())


if __name__ == '__main__':
    generate()
    print(f'Generated three deterministic, synthetic fixtures in {OUT}')

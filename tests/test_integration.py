"""Offline integration check with synthetic data, not a model benchmark."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def test_stage1(tmp_path):
    raw = tmp_path / 'data' / 'raw' / 'fixture'
    raw.mkdir(parents=True)
    rows = []
    for pid in range(80):
        solutions = [f'def solve_{pid}_{i}(x):\n    return x + {pid * 10 + i}\n' for i in range(3)]
        if pid == 0:
            solutions.extend([solutions[0], 'def broken(:'])
        rows.append({'row': {'problem_id': pid, 'solutions': json.dumps(solutions),
                             'difficulty': 'introductory'}, 'truncated_cells': []})
    content = json.dumps({'rows': rows})
    (raw / 'page.json').write_text(content, encoding='utf-8')
    manifest = {'run_id': 'synthetic-fixture', 'split': 'train', 'problem_rows': 80,
                'pages': [{'file': 'page.json', 'rows': 80,
                           'sha256': hashlib.sha256(content.encode()).hexdigest()}]}
    (raw / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    (tmp_path / 'data' / 'active_snapshot.json').write_text(json.dumps({'folder': str(raw)}), encoding='utf-8')
    env = {**os.environ, 'CODE21_ROOT': str(tmp_path)}
    for day in range(3, 8):
        result = subprocess.run([sys.executable, str(ROOT / 'days' / f'day{day:02}.py')],
                                env=env, text=True, capture_output=True, timeout=120)
        assert result.returncode == 0, f'Day {day}: {result.stdout}\n{result.stderr}'
    quality = json.loads((tmp_path / 'reports' / 'quality.json').read_text())
    assert quality['accepted_solutions'] == 240
    assert quality['duplicates_removed'] == 1
    assert quality['rejected_solutions'] == 1
    assert json.loads((tmp_path / 'reports' / 'stage1_gate.json').read_text())['passed']
    assert (tmp_path / 'reports' / 'eda.png').exists()
    assert (tmp_path / 'reports' / 'eda.md').exists()

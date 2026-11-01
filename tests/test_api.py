"""API client checks with mocked responses; no real API token or network needed."""
import json
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import stage1


class ApiTests(unittest.TestCase):
    def test_authentication_pagination_and_no_secret_persistence(self):
        calls = []
        class Response:
            status_code = 200
            def __init__(self, payload):
                self.payload = payload
            def raise_for_status(self):
                pass
            def json(self):
                return self.payload
        class Session:
            def mount(self, *args):
                pass
            def get(self, url, params, headers, timeout):
                self_outer.assertEqual(headers['Authorization'], 'Bearer test-token-not-a-real-secret')
                calls.append((url, params.copy()))
                if url.endswith('/splits'):
                    return Response({'splits': [{'config': 'all', 'split': 'train'}]})
                return Response({'rows': [{'row_idx': i, 'row': {}} for i in
                                         range(params['offset'], params['offset'] + params['length'])]})
        self_outer = self
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            data = root / 'data'
            env = {'HF_TOKEN': 'test-token-not-a-real-secret', 'MAX_PROBLEMS': '150',
                   'HF_DATASET': 'codeparrot/apps', 'HF_CONFIG': 'all', 'HF_SPLIT': 'train'}
            dotenv = types.SimpleNamespace(load_dotenv=lambda path: None)
            with patch.dict(os.environ, env), patch.dict(sys.modules, {'dotenv': dotenv}), \
                 patch('requests.Session', Session), patch.object(stage1, 'ROOT', root), \
                 patch.object(stage1, 'DATA', data), \
                 patch.object(stage1, 'setup', lambda: (data / 'raw').mkdir(parents=True)):
                stage1.day02()
            active = json.loads((data / 'active_snapshot.json').read_text())
            manifest = json.loads((Path(active['folder']) / 'manifest.json').read_text())
            self.assertEqual(manifest['problem_rows'], 150)
            self.assertEqual([p['rows'] for p in manifest['pages']], [100, 50])
            self.assertEqual([p['offset'] for u, p in calls if u.endswith('/rows')], [0, 100])
            for path in root.rglob('*.json'):
                self.assertNotIn(env['HF_TOKEN'], path.read_text())

if __name__ == '__main__':
    unittest.main()

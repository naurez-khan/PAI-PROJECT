import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import FEATURES, analyze, pair_features

class StaticAnalysisTests(unittest.TestCase):
    def test_source_is_not_executed(self):
        result = analyze("raise RuntimeError('must never execute')")
        self.assertGreater(result['node_count'], 0)

    def test_identical_code_matches_all_channels(self):
        scores = pair_features('x = 1\nprint(x)', 'x = 1\nprint(x)')
        self.assertEqual(set(scores), set(FEATURES))
        self.assertTrue(all(abs(v - 1) < 1e-12 for v in scores.values()))

    def test_comments_and_formatting_share_fingerprint(self):
        self.assertEqual(analyze('x=1 # comment')['canonical_hash'],
                         analyze('x = 1\n')['canonical_hash'])

    def test_pair_features_are_symmetric_and_bounded(self):
        a, b = 'print(1)', 'for i in range(3):\n    print(i)'
        self.assertEqual(pair_features(a, b), pair_features(b, a))
        self.assertTrue(all(0 <= x <= 1 for x in pair_features(a, b).values()))

    def test_invalid_syntax_is_rejected(self):
        with self.assertRaises(SyntaxError):
            analyze('def bad(:')

if __name__ == '__main__':
    unittest.main()

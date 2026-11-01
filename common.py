"""Shared paths and static Python features for Stage 1."""
import ast
import hashlib
import io
import json
import os
import tokenize
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(os.environ.get("CODE21_ROOT", Path(__file__).resolve().parent))
DATA = ROOT / "data"
REPORTS = ROOT / "reports"
SEED = 42
FEATURES = ["token_jaccard", "shingle_jaccard", "ast_cosine", "line_ratio", "token_ratio", "node_ratio"]


def setup():
    for path in [DATA / "raw", REPORTS]:
        path.mkdir(parents=True, exist_ok=True)


def save_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False), encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@lru_cache(maxsize=10000)
def analyze(code):
    # Parse only: never import, eval, exec, or run submitted code.
    tree = ast.parse(code)
    ignored = {tokenize.COMMENT, tokenize.NL, tokenize.NEWLINE, tokenize.INDENT,
               tokenize.DEDENT, tokenize.ENDMARKER, tokenize.ENCODING}
    tokens = tuple(t.string for t in tokenize.generate_tokens(io.StringIO(code).readline)
                   if t.type not in ignored)
    nodes = Counter(type(node).__name__ for node in ast.walk(tree))
    # Ignore formatting/comments in the duplicate fingerprint, retain identifiers/literals.
    canonical_hash = digest(ast.dump(tree, include_attributes=False))
    return {"tokens": tokens, "nodes": nodes, "lines": len(code.splitlines()),
            "token_count": len(tokens), "node_count": sum(nodes.values()),
            "canonical_hash": canonical_hash}


def ratio(a, b):
    return min(a, b) / max(a, b) if max(a, b) else 1.0


def jaccard(a, b):
    a, b = set(a), set(b)
    return len(a & b) / len(a | b) if a | b else 1.0


def pair_features(code_a, code_b):
    a, b = analyze(code_a), analyze(code_b)
    def shingles(tokens):
        return [tokens[i:i + 3] for i in range(max(1, len(tokens) - 2))]
    keys = a["nodes"].keys() | b["nodes"].keys()
    dot = sum(a["nodes"][k] * b["nodes"][k] for k in keys)
    norm = (sum(v*v for v in a["nodes"].values()) * sum(v*v for v in b["nodes"].values())) ** 0.5
    return dict(zip(FEATURES, [
        jaccard(a["tokens"], b["tokens"]),
        jaccard(shingles(a["tokens"]), shingles(b["tokens"])),
        dot / norm if norm else 0.0,
        ratio(a["lines"], b["lines"]),
        ratio(a["token_count"], b["token_count"]),
        ratio(a["node_count"], b["node_count"]),
    ]))


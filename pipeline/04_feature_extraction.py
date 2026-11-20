"""Stage 4: Static code feature extraction (AST nodes, tokens, lines). See docs/04_feature_extraction.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import extract_features

if __name__ == "__main__":
    extract_features()

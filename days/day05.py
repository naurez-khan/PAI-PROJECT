"""Day 5: SQLite loading and reconciliation. See docs/day05.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import day05

if __name__ == "__main__":
    day05()

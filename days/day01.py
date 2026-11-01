"""Day 1: Environment and project contract. See docs/day01.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import day01

if __name__ == "__main__":
    day01()

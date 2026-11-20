"""Stage 1: Environment and contract verification. See docs/01_environment_setup.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import setup_environment

if __name__ == "__main__":
    setup_environment()

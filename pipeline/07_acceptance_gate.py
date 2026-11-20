"""Stage 7: Acceptance gate verification and readiness check. See docs/07_acceptance_gate.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import acceptance_gate

if __name__ == "__main__":
    acceptance_gate()

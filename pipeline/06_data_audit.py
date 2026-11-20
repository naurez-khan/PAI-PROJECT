"""Stage 6: Statistical data audit and complexity analysis. See docs/06_data_audit.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import data_audit

if __name__ == "__main__":
    data_audit()

"""Stage 5: Transactional ACID SQLite database loading. See docs/05_database_loading.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import load_database

if __name__ == "__main__":
    load_database()

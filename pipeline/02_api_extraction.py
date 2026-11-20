"""Stage 2: Authenticated Hugging Face API extraction. See docs/02_api_extraction.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import extract_data

if __name__ == "__main__":
    extract_data()

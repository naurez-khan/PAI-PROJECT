"""Stage 3: Data cleaning, Pydantic validation, and quarantine. See docs/03_data_cleaning_validation.md."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from stage1 import clean_and_validate

if __name__ == "__main__":
    clean_and_validate()

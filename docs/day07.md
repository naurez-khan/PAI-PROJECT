# Day 7: Stage 1 acceptance and demonstration

Stage 1, day 7/7. Allocate 3-4 focused hours.

## Objective

Run the quality gate and automated tests; demonstrate API-to-database-to-EDA flow.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day07`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day07.py
```

## Today's implementation

The executable source is `stage1.py`, function `day07`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day07():
    import pandas as pd
    with sqlite3.connect(DATA / "code_similarity.db") as conn:
        frame = pd.read_sql_query("SELECT * FROM solutions", conn)
    assert frame.solution_id.is_unique and frame.canonical_hash.is_unique
    assert not frame.isna().any().any()
    eligible = int((frame.groupby("problem_id").size() >= 2).sum())
    if eligible < 50:
        raise RuntimeError(f"Only {eligible} eligible problems. Increase MAX_PROBLEMS and rerun Days 2-6.")
    quality = read_json(REPORTS / "quality.json")
    assert len(frame) == quality["accepted_solutions"]
    save_json(REPORTS / "stage1_gate.json", {"passed": True, "eligible_problems": eligible,
                                             "rows": len(frame)})
    print("Stage 1 gate passed. Freeze this snapshot before Stage 2.")
```

## Documentation to write

docs/stage1_handoff.md: commands, actual counts, failure cases, screenshots, unresolved limitations.

Use this daily log template:

- Objective and design decision:
- Exact command and dependency versions:
- Input snapshot / split / run identifier:
- Actual output counts or metrics:
- Checks passed and failures investigated:
- Evidence files or screenshots:
- Interpretation and limitations:
- Next-day dependency:

## Acceptance check

At least 50 problems have two distinct valid solutions; integrity checks and tests pass.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

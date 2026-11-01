# Day 5: SQLite loading and reconciliation

Stage 1, day 5/7. Allocate 3-4 focused hours.

## Objective

Create constrained tables; load one active snapshot transactionally; retain historical run summaries.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day05`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day05.py
```

## Today's implementation

The executable source is `stage1.py`, function `day05`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day05():
    import pandas as pd
    frame = pd.read_json(DATA / "features.jsonl", lines=True)
    with sqlite3.connect(DATA / "code_similarity.db") as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS solutions (
          solution_id TEXT PRIMARY KEY, problem_id INTEGER NOT NULL, difficulty TEXT NOT NULL,
          code TEXT NOT NULL, code_hash TEXT NOT NULL, canonical_hash TEXT NOT NULL UNIQUE,
          lines INTEGER NOT NULL, token_count INTEGER NOT NULL, node_count INTEGER NOT NULL)""")
        # Canonical table reflects exactly one snapshot. Raw snapshots remain immutable.
        conn.execute("DELETE FROM solutions")
        columns = ["solution_id", "problem_id", "difficulty", "code", "code_hash", "canonical_hash",
                   "lines", "token_count", "node_count"]
        conn.executemany("INSERT INTO solutions VALUES (?,?,?,?,?,?,?,?,?)",
                         frame[columns].itertuples(index=False, name=None))
        conn.execute("CREATE TABLE IF NOT EXISTS pipeline_runs (run_id TEXT PRIMARY KEY, summary TEXT NOT NULL)")
        quality = read_json(REPORTS / "quality.json")
        conn.execute("INSERT OR REPLACE INTO pipeline_runs VALUES (?,?)",
                     (quality["run_id"], json.dumps(quality)))
        count = conn.execute("SELECT COUNT(*) FROM solutions").fetchone()[0]
        assert count == len(frame)
    print(f"Loaded and reconciled {count} rows in SQLite.")
```

## Documentation to write

docs/database.md: table schema, primary/unique keys, snapshot replacement policy, SQL count query.

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

SQL row count equals accepted rows; rerunning Day 5 produces the same canonical row count.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

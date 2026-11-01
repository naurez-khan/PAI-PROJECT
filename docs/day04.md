# Day 4: Static feature extraction

Stage 1, day 4/7. Allocate 3-4 focused hours.

## Objective

Extract lines, tokens, AST node counts and fingerprints; review common.py pair features.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day04`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day04.py
```

## Today's implementation

The executable source is `stage1.py`, function `day04`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day04():
    import pandas as pd
    frame = pd.read_json(DATA / "clean.jsonl", lines=True)
    for name in ["lines", "token_count", "node_count"]:
        frame[name] = frame.code.map(lambda code: analyze(code)[name])
    frame.to_json(DATA / "features.jsonl", orient="records", lines=True)
    print(frame[["lines", "token_count", "node_count"]].describe())
```

## Documentation to write

docs/feature_dictionary.md: formula, interpretation and limits of each static feature.

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

data/features.jsonl exists; submitted programs were only parsed, never executed.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

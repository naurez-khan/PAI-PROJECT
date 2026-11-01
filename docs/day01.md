# Day 1: Environment and project contract

Stage 1, day 1/7. Allocate 3-4 focused hours.

## Objective

Create a fresh virtual environment; install Stage 1/2 dependencies; configure a read token; run folder setup.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day01`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day01.py
```

## Today's implementation

The executable source is `stage1.py`, function `day01`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day01():
    setup()
    if sys.version_info < (3, 11):
        raise RuntimeError("Use Python 3.11 or later; Python 3.12 is recommended.")
    save_json(REPORTS / "environment.json", {"python": sys.version, "platform": platform.platform()})
    print("Folders ready. Create .env from .env.example and set HF_TOKEN privately.")
```

## Documentation to write

docs/project_brief.md: scope, users, target, inputs, outputs, exclusions, 21-day milestones.

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

reports/environment.json exists; .env is ignored; no token appears in source control.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

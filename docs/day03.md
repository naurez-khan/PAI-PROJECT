# Day 3: pandas cleaning and Pydantic validation

Stage 1, day 3/7. Allocate 3-4 focused hours.

## Objective

Validate API records; decode solution arrays; normalize line endings; parse Python; quarantine failures; globally deduplicate AST fingerprints.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day03`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day03.py
```

## Today's implementation

The executable source is `stage1.py`, function `day03`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day03():
    import pandas as pd
    from pydantic import BaseModel, ConfigDict, Field, ValidationError
    class Problem(BaseModel):
        model_config = ConfigDict(strict=True)
        problem_id: int = Field(ge=0)
        solutions: str
        difficulty: str
    setup()
    folder = ROOT / read_json(DATA / "active_snapshot.json")["folder"]
    manifest = read_json(folder / "manifest.json")
    records, rejected = [], []
    candidates = empty = capped = 0
    for page in manifest["pages"]:
        path = folder / page["file"]
        if digest(path.read_text(encoding="utf-8")) != page["sha256"]:
            raise RuntimeError("Raw snapshot checksum mismatch.")
        for entry in read_json(path)["rows"]:
            pid = entry.get("row", {}).get("problem_id")
            try:
                if entry.get("truncated_cells"):
                    raise ValueError("truncated_api_row")
                problem = Problem.model_validate(entry["row"])
                solutions = json.loads(problem.solutions)
                if not isinstance(solutions, list):
                    raise ValueError("solutions_not_list")
            except (ValidationError, ValueError, KeyError, TypeError):
                rejected.append({"problem_id": pid, "reason": "invalid_problem_contract"})
                continue
            if not solutions:
                empty += 1
            capped += max(0, len(solutions) - 5)
            for index, code in enumerate(solutions[:5]):
                candidates += 1
                try:
                    if not isinstance(code, str) or not code.strip() or len(code) > 50000:
                        raise ValueError("invalid_code_size_or_type")
                    code = code.replace("\r\n", "\n").strip() + "\n"
                    analysis = analyze(code)
                    records.append({"solution_id": f"{manifest['split']}:{problem.problem_id}:{index}",
                                    "problem_id": problem.problem_id, "difficulty": problem.difficulty,
                                    "code": code, "code_hash": digest(code),
                                    "canonical_hash": analysis["canonical_hash"]})
                except (SyntaxError, ValueError, TypeError, RecursionError):
                    rejected.append({"problem_id": pid, "solution_index": index,
                                     "reason": "invalid_python_solution"})
    if not records:
        raise RuntimeError("No valid solutions; inspect the API schema and snapshot.")
    frame = pd.DataFrame(records)
    before = len(frame)
    # Global deduplication prevents exact/AST-equivalent code appearing in separate splits.
    frame = frame.drop_duplicates("canonical_hash").reset_index(drop=True)
    frame.to_json(DATA / "clean.jsonl", orient="records", lines=True, force_ascii=False)
    with (DATA / "quarantine.jsonl").open("w", encoding="utf-8") as out:
        for item in rejected:
            out.write(json.dumps(item) + "\n")
    summary = {"run_id": manifest["run_id"], "problem_rows": manifest["problem_rows"],
               "candidate_solutions": candidates, "accepted_solutions": len(frame),
               "duplicates_removed": before - len(frame),
               "rejected_solutions": sum("solution_index" in r for r in rejected),
               "rejected_problem_rows": sum("solution_index" not in r for r in rejected),
               "empty_solution_lists": empty, "solutions_excluded_by_cap": capped}
    assert candidates == summary["accepted_solutions"] + summary["duplicates_removed"] + summary["rejected_solutions"]
    save_json(REPORTS / "quality.json", summary)
    print(summary)
```

## Documentation to write

docs/data_dictionary.md and docs/quality_rules.md: types, validation, rejected counts, cap, duplicate policy.

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

Accepted + duplicate + rejected solution counts reconcile with candidate solutions.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

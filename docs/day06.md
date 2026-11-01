# Day 6: Structured exploratory data analysis

Stage 1, day 6/7. Allocate 3-4 focused hours.

## Objective

Query SQLite; generate statistics, correlations, charts, and a question-driven report.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day06`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day06.py
```

## Today's implementation

The executable source is `stage1.py`, function `day06`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day06():
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    with sqlite3.connect(DATA / "code_similarity.db") as conn:
        frame = pd.read_sql_query("SELECT * FROM solutions", conn)
    counts = frame.groupby("problem_id").size()
    stats = frame[["lines", "token_count", "node_count"]].describe()
    stats.to_csv(REPORTS / "descriptive_statistics.csv")
    frame[["lines", "token_count", "node_count"]].corr().to_csv(REPORTS / "correlations.csv")
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    frame.lines.plot.hist(bins=30, ax=axes[0], title="Lines per solution")
    frame.difficulty.value_counts().plot.bar(ax=axes[1], title="Retained solutions by difficulty")
    counts.plot.hist(bins=10, ax=axes[2], title="Solutions per problem")
    fig.tight_layout()
    fig.savefig(REPORTS / "eda.png", dpi=160)
    plt.close(fig)
    quality = read_json(REPORTS / "quality.json")
    report = f"""# Stage 1 exploratory analysis

Data: the active API snapshot; at most five solutions per problem; invalid Python and AST duplicates removed.

1. How many records survived? {len(frame)} solutions from {frame.problem_id.nunique()} problems.
2. How many problems can supply positive pairs? {int((counts >= 2).sum())} have two or more distinct solutions.
3. How long are solutions? Median {frame.lines.median():.1f} lines; 95th percentile {frame.lines.quantile(.95):.1f}.
4. Which difficulties dominate? {frame.difficulty.value_counts().to_dict()}.
5. What quality issues occurred? See quality.json: {json.dumps(quality)}.
6. Which features move together? See correlations.csv; correlated size features may add little independent information.

Interpret eda.png and add three observations with evidence, two limitations, and one modeling decision.
Sampling the first API rows is a convenience sample, not a representative benchmark.
Same-problem labels are a proxy for task similarity, not verified plagiarism or semantic equivalence.
The final test partition is created on Day 8; no model decisions may use its outcomes.
"""
    (REPORTS / "eda.md").write_text(report, encoding="utf-8")
    print("EDA tables, chart, and report generated from SQLite.")
```

## Documentation to write

reports/eda.md: add three findings, supporting numbers, two limitations, and one modeling decision.

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

reports/eda.png, descriptive_statistics.csv, correlations.csv and eda.md exist.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

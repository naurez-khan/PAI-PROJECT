# Stage 1 — API, ETL, validation, SQLite and EDA

A self-contained seven-day project. Budget 3-4 hours per day. This package contains all Stage 1 source code, seven runnable day scripts, seven daily guides, technical documentation, API-token setup, tests, and a read-only Streamlit dashboard.

## Setup

Extract the ZIP and open PowerShell in the extracted `stage1_kit` directory. Use Python 3.12 or 3.13.

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` privately and set `HF_TOKEN` to your Hugging Face read token. Create a token at https://huggingface.co/settings/tokens. See [API key setup](docs/API_KEY_SETUP.md). The key is used by `stage1.py:day02` as an Authorization Bearer header. No real API key is included. Public API access can work anonymously, but this implementation requires a token to demonstrate authenticated extraction.

## Seven-day schedule

| Day | Implementation | Documentation/evidence |
|---|---|---|
| [1](docs/day01.md) | Environment, folders and scope | Project brief and environment report |
| [2](docs/day02.md) | Authenticated API extraction, pagination, retries and snapshots | API contract and checksummed manifest |
| [3](docs/day03.md) | pandas cleaning, Pydantic validation and quarantine | Data dictionary, quality rules and reconciliation |
| [4](docs/day04.md) | Static token/AST feature extraction | Feature definitions and feature data |
| [5](docs/day05.md) | Transactional SQLite loading | Schema, constraints and row-count checks |
| [6](docs/day06.md) | Structured EDA from SQLite | Statistics, chart, correlations and interpreted findings |
| [7](docs/day07.md) | Acceptance checks and demonstration | Test evidence and Stage 1 handoff report |

Each daily guide includes its actual implementation, command, documentation task and acceptance check. Read [technical design](docs/DESIGN.md) alongside the daily pages.

## Run each day in order

```powershell
.\.venv\Scripts\python.exe days/day01.py
.\.venv\Scripts\python.exe days/day02.py
.\.venv\Scripts\python.exe days/day03.py
.\.venv\Scripts\python.exe days/day04.py
.\.venv\Scripts\python.exe days/day05.py
.\.venv\Scripts\python.exe days/day06.py
.\.venv\Scripts\python.exe days/day07.py
```

The default download requests the first 500 problems from codeparrot/apps, config all, source split train. Day 2 checks available configs/splits. Cleaning keeps at most five solutions per problem. Increase MAX_PROBLEMS if Day 7 reports fewer than 50 eligible problems, then rerun Days 2-7.

## Tests and dashboard

The tests use mocked API responses and a temporary synthetic dataset, so they do not need a real token or a live download. They do not modify the real project dataset.

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m streamlit run app.py
.\.venv\Scripts\python.exe -m pip freeze > requirements-lock.txt
```

The dashboard reads your generated database and reports. Complete Days 1-6 to populate it. It shows stored counts, quality results, EDA and pipeline history. It does not execute submitted Python code.

## Files and generated outputs

- `stage1.py`: the seven implementation functions.
- `common.py`: paths, JSON/hash utilities and static code analysis.
- `days/day01.py` through `day07.py`: runnable daily entry points.
- `docs/day01.md` through `day07.md`: daily code and documentation instructions.
- `docs/DESIGN.md`: system design, data dictionary, schema, quality rules and EDA questions.
- `docs/API_KEY_SETUP.md`: token creation, storage and usage.
- `app.py`: read-only local dashboard.
- `tests/`: static-analysis, API-client and ETL/EDA integration checks.
- `data/raw/<run>/`: generated immutable snapshots and checksum manifests.
- `data/clean.jsonl`, `features.jsonl`, `quarantine.jsonl`: generated pipeline data.
- `data/code_similarity.db`: generated SQLite database.
- `reports/`: generated quality summary, EDA tables/chart/report and acceptance gate.

The source ZIP excludes credentials, virtual environments and generated datasets. Run the commands to create your own database and reports. The integration fixture is synthetic verification data, not valid evidence of real API extraction or benchmark performance.

## Documentation to finish with your actual results

Write a project brief, API contract, data dictionary/quality rules, feature dictionary, database description, interpreted EDA and Stage 1 handoff. Daily guides list the exact deliverables. The technical design provides the factual starting point. Add observed counts, three EDA findings, two limitations, one modeling decision, screenshots and command outputs. Never invent results.

## Troubleshooting

- 401/403: check token permissions and dataset access.
- 429: the client respects retry delays; retry later if the service remains limited.
- Missing config/split: use the combinations listed by Day 2.
- Truncated API rows, invalid fields or invalid Python: inspect quarantine counts.
- A checksum mismatch: investigate the snapshot rather than editing its manifest.
- Too few eligible problems: increase MAX_PROBLEMS, up to 5000.
- Rerunning Day 5 replaces only the active canonical table transactionally; raw snapshots remain available.

The first API rows are a convenience sample. Syntax filtering and the solution cap can bias results. Code is parsed/tokenized, never executed. This is a data-engineering and EDA stage; the data does not establish plagiarism.

## References

- https://huggingface.co/datasets/codeparrot/apps
- https://huggingface.co/docs/dataset-viewer/en/rows
- https://huggingface.co/docs/hub/security-tokens

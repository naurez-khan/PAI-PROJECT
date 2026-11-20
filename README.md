# Stage 1 — API, ETL, Validation, SQLite and Data Audit

A self-contained production-grade data engineering pipeline. This package contains all Stage 1 source code, seven modular pipeline stage scripts, comprehensive documentation, API token configuration, test suite, and a read-only Streamlit dashboard.

## Setup

Open PowerShell in the `stage1_kit` directory. Use Python 3.12 or 3.13.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` privately and set `HF_TOKEN` to your Hugging Face read token. Create a token at https://huggingface.co/settings/tokens. See [API key setup](docs/API_KEY_SETUP.md). The key is used by `stage1.py:extract_data` as an Authorization Bearer header.

## Pipeline Architecture & Execution Stages

| Stage | Step | Implementation | Documentation / Guide |
|---|---|---|---|
| **01** | **Environment Setup** | Environment verification, directory contracts & dependencies | [01_environment_setup.md](docs/01_environment_setup.md) |
| **02** | **API Extraction** | Authenticated Hugging Face ingestion, pagination & raw snapshots | [02_api_extraction.md](docs/02_api_extraction.md) |
| **03** | **Cleaning & Validation** | Pydantic schema validation, syntax check, quarantine & deduplication | [03_data_cleaning_validation.md](docs/03_data_cleaning_validation.md) |
| **04** | **Feature Extraction** | Static token, AST node count, and physical line metrics | [04_feature_extraction.md](docs/04_feature_extraction.md) |
| **05** | **Database Loading** | Transactional ACID loading into SQLite with constraint checks | [05_database_loading.md](docs/05_database_loading.md) |
| **06** | **Data Audit & EDA** | Statistical distributions, correlation analysis & findings | [06_data_audit.md](docs/06_data_audit.md) |
| **07** | **Acceptance Gate** | Quality gate verification and Stage 1 acceptance certification | [07_acceptance_gate.md](docs/07_acceptance_gate.md) |

Read [technical design](docs/DESIGN.md) alongside the stage documentation.

## Run the Pipeline in Order

```powershell
.\.venv\Scripts\python.exe pipeline/01_environment_setup.py
.\.venv\Scripts\python.exe pipeline/02_api_extraction.py
.\.venv\Scripts\python.exe pipeline/03_data_cleaning_validation.py
.\.venv\Scripts\python.exe pipeline/04_feature_extraction.py
.\.venv\Scripts\python.exe pipeline/05_database_loading.py
.\.venv\Scripts\python.exe pipeline/06_data_audit.py
.\.venv\Scripts\python.exe pipeline/07_acceptance_gate.py
```

The download requests the first 500 problems from the APPS benchmark. Cleaning keeps at most five solutions per problem.

## Tests and Dashboard

The tests use mocked API responses and a temporary synthetic dataset, so they do not require a live API download or token.

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m streamlit run app.py
```

The dashboard reads your generated database and reports. It shows stored counts, quality results, data audit statistics, and pipeline history.

## Files and Generated Outputs

- `stage1.py`: the core pipeline implementation functions.
- `common.py`: shared paths, JSON/hash utilities, and static code analysis.
- `pipeline/`: runnable pipeline stage entry points (`01_environment_setup.py` through `07_acceptance_gate.py`).
- `docs/`: stage specifications, technical design, and setup guides.
- `docs/DESIGN.md`: system design, data dictionary, schema, and quality rules.
- `docs/API_KEY_SETUP.md`: token creation, storage, and usage.
- `app.py`: read-only local and cloud-ready dashboard.
- `tests/`: unit and integration tests for API client, static analysis, and ETL flow.
- `data/raw/<run>/`: immutable snapshots and checksum manifests.
- `data/clean.jsonl`, `features.jsonl`, `quarantine.jsonl`: intermediate pipeline datasets.
- `data/code_similarity.db`: generated SQLite database.
- `reports/`: generated quality summary, audit tables, charts, report, and acceptance gate.

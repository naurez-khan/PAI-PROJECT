# Day 2: Authenticated API extraction

Stage 1, day 2/7. Allocate 3-4 focused hours.

## Objective

Use a Bearer token, discover config/split availability, paginate in batches of at most 100, retry transient failures, preserve checksummed snapshots.

## Prerequisites

Complete the earlier days in order. Read `common.py` and the helpers used by `stage1.py:day02`. On Day 1 follow the README setup first.

## Run

From the project root:

```powershell
.\.venv\Scripts\python.exe days/day02.py
```

## Today's implementation

The executable source is `stage1.py`, function `day02`. The function below relies on its module imports and shared helpers; use the supplied entry point rather than pasting it into an empty file.

```python
def day02():
    import requests
    from dotenv import load_dotenv
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    setup()
    load_dotenv(ROOT / ".env")
    token = os.environ.get("HF_TOKEN", "")
    if not token or token.startswith("replace_"):
        raise RuntimeError("Set HF_TOKEN in .env to your Hugging Face read token.")
    dataset = os.getenv("HF_DATASET", "codeparrot/apps")
    config = os.getenv("HF_CONFIG", "all")
    split = os.getenv("HF_SPLIT", "train")
    maximum = int(os.getenv("MAX_PROBLEMS", "500"))
    if not 50 <= maximum <= 5000:
        raise ValueError("MAX_PROBLEMS must be between 50 and 5000.")
    session = requests.Session()
    retry = Retry(total=4, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504],
                  allowed_methods=["GET"], respect_retry_after_header=True)
    session.mount("https://", HTTPAdapter(max_retries=retry))
    headers = {"Authorization": f"Bearer {token}"}  # The API key is used HERE only.
    def get(endpoint, params):
        response = session.get("https://datasets-server.huggingface.co/" + endpoint,
                               params=params, headers=headers, timeout=(10, 60))
        if response.status_code in (401, 403):
            raise RuntimeError("API access denied: check the token permissions and dataset access.")
        response.raise_for_status()
        return response.json()
    splits = get("splits", {"dataset": dataset}).get("splits", [])
    if not any(s["config"] == config and s["split"] == split for s in splits):
        raise RuntimeError("Requested config/split unavailable. Available: " +
                           str([(s["config"], s["split"]) for s in splits]))
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid.uuid4().hex[:8]
    folder = DATA / "raw" / run_id
    folder.mkdir(parents=True)
    pages, offset = [], 0
    while offset < maximum:
        params = {"dataset": dataset, "config": config, "split": split,
                  "offset": offset, "length": min(100, maximum - offset)}
        payload = get("rows", params)
        rows = payload.get("rows", [])
        if not rows:
            break
        filename = f"page_{offset:05}.json"
        save_json(folder / filename, payload)
        pages.append({"file": filename, "sha256": digest((folder / filename).read_text(encoding="utf-8")),
                      "rows": len(rows)})
        offset += len(rows)
        print(f"Downloaded {offset} problems")
    if not pages:
        raise RuntimeError("API returned no rows; no active snapshot was changed.")
    manifest = {"run_id": run_id, "dataset": dataset, "config": config, "split": split,
                "downloaded_at": datetime.now(timezone.utc).isoformat(), "pages": pages,
                "problem_rows": offset}
    save_json(folder / "manifest.json", manifest)
    save_json(DATA / "active_snapshot.json", {"folder": str(folder)})
    print("Snapshot saved. Token and authorization headers are never written to disk.")
```

## Documentation to write

docs/api_contract.md: endpoint, authentication, parameters, response shape, status handling, snapshot provenance.

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

data/raw/<run>/manifest.json records page checksums and downloaded problem count.

If this check fails, resolve it before the next day. Never insert invented output values into your report.

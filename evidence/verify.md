# Verification Evidence

**Last updated:** 2026-11-08

## Checks Run

| Component | Command | Result |
|---|---|---|
| API | `uv run --directory src/api pytest` | PASS — 16 tests passed |
| API | `uv run --directory src/api ruff check .` | PASS |
| API | `uv run --directory src/api ruff format --check .` | PASS |
| API | Live Uvicorn request to `POST /exp-digiServicing-transctiontraige/v1/message` | PASS — found shared `txn-001` for “Report $50 at Woolworths” |
| API | Live Uvicorn request to `POST /exp-digiServicing-transctiontraige/v1/submission` | PASS — confirmed Dispute returned `MOCK-DISPUTE-TXN-001` |
| Shared data | JSON parse, unique-ID, one-customer, and 50-record validation for `sample_data/transactions.json` | PASS |
| Agent | `uv run --directory src/agent pytest` | PASS — 16 tests passed |
| Agent | `uv run --directory src/agent ruff check .` | PASS |
| Agent | `uv run --directory src/agent ruff format --check .` | PASS |
| Agent | Agent lock and dependencies: `uv sync --directory src/agent --extra dev` | PASS |

## Local Verification

Run these commands from the repository root. The first command for each component requires the
Westpac Python package index and system certificates.

```bash
UV_DEFAULT_INDEX=https://artifactory.srv.westpac.com.au/artifactory/api/pypi/westpac-pypi/simple \
UV_SYSTEM_CERTS=true uv sync --directory src/api --extra dev
uv run --directory src/api pytest
uv run --directory src/api ruff check .
uv run --directory src/api ruff format --check .

UV_DEFAULT_INDEX=https://artifactory.srv.westpac.com.au/artifactory/api/pypi/westpac-pypi/simple \
UV_SYSTEM_CERTS=true uv sync --directory src/agent --extra dev
uv run --directory src/agent pytest
uv run --directory src/agent ruff check .
uv run --directory src/agent ruff format --check .
```

For a manual API check, start `uv run --directory src/api uvicorn api.app:app --host 127.0.0.1 --port 8765`
and call the two documented POST endpoints.

## PR / Pipeline Verification

No GitHub Actions, GitLab CI, or other pipeline configuration currently exists in this repository.
Therefore, none of the checks above run automatically on a pull request today.

When a pipeline is added, it should run the same isolated API and agent suites:

1. `uv sync --directory src/api --extra dev --locked`, followed by API pytest and Ruff checks.
2. `uv sync --directory src/agent --extra dev --locked`, followed by agent pytest and Ruff checks.
3. JSON validation for `sample_data/transactions.json` and a smoke test that imports both packages.
4. An API-to-agent integration test after the API is wired to call `process_interaction`.

## Known Gaps

- The API still uses `src/api/triage_service.py`; it does not yet invoke the agent's
  `transaction_agent.engine.process_interaction` function.
- The React chat UI feature is specified but not implemented or verified.
- The API and agent each have unit/integration tests, but there is no cross-component API-to-agent
  integration test until the wiring is implemented.
- FastAPI's `TestClient` currently emits a Starlette deprecation warning about its `httpx` integration.
  It does not fail the test suite.
- No automated PR/pipeline checks are configured.

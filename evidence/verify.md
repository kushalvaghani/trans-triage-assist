# Verification Evidence

**Last updated:** 2026-11-08

## Checks Run

| Component | Command | Result |
|---|---|---|
| API | `uv run --directory src/api pytest` | PASS — 19 tests passed, including API-to-agent message and submission delegation |
| API | `uv run --directory src/api ruff check .` | PASS |
| API | `uv run --directory src/api ruff format --check .` | PASS |
| API | Live Uvicorn request to `POST /exp-digiServicing-transctiontraige/v1/message` | PASS — delegated to the agent and found shared `txn-001` for “Report $50 at Woolworths” |
| API | Live Uvicorn request to `POST /exp-digiServicing-transctiontraige/v1/submission` | PASS — returned a nine-character alphanumeric case ID and logged the answers, outcome, user ID, and case ID |
| Shared data | JSON parse, unique-ID, one-customer, and 50-record validation for `sample_data/transactions.json` | PASS |
| Agent | `uv run --directory src/agent pytest` | PASS — 17 tests passed |
| Agent | `uv run --directory src/agent ruff check .` | PASS |
| Agent | `uv run --directory src/agent ruff format --check .` | PASS |
| Agent | Agent lock and dependencies: `uv sync --directory src/agent --extra dev` | PASS |
| UI | `npm test -- --run` from `src/ui` | PASS — 7 tests across API client, chat, transaction, triage, confirmation, and alternatives components |
| UI | `npm run lint` from `src/ui` | PASS |
| UI | `npm run build` from `src/ui` | PASS — TypeScript and Vite production build succeeded |
| UI | Live Vite-to-API proxy search for “Report $50 at Woolworths” | PASS — displayed shared transaction `txn-001` |
| UI | Headless Chrome visual checks | PASS — inspected default chat, matching transaction, triage-question, and disabled confirmed-case states |

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

For the UI, install dependencies with `npm install` in `src/ui`, start the API command above, then run
`npm run dev -- --host 127.0.0.1 --port 5173` in `src/ui`. Run `npm test -- --run`, `npm run lint`, and
`npm run build` from `src/ui` before review.

## PR / Pipeline Verification

No GitHub Actions, GitLab CI, or other pipeline configuration currently exists in this repository.
Therefore, none of the checks above run automatically on a pull request today.

When a pipeline is added, it should run the same isolated API and agent suites:

1. `uv sync --directory src/api --extra dev --locked`, followed by API pytest and Ruff checks.
2. `uv sync --directory src/agent --extra dev --locked`, followed by agent pytest and Ruff checks.
3. JSON validation for `sample_data/transactions.json` and a smoke test that imports both packages.
4. API-to-agent integration tests that exercise `process_interaction` through the API endpoints.
5. `npm ci --prefix src/ui`, then UI Vitest, ESLint, TypeScript/Vite build, and a browser smoke test.

## Known Gaps

- The UI calls only the documented API routes. Current API responses do not expose a session contract for
  transaction selection and one-question-at-a-time triage, so the UI renders that guided flow locally and
  calls `/submission` only after explicit confirmation. It does not access agent code or shared fixture
  data directly.
- The API-to-agent adapter is covered by an endpoint test, but the API does not yet expose the
  agent's per-question session state as an HTTP contract.
- FastAPI's `TestClient` currently emits a Starlette deprecation warning about its `httpx` integration.
  It does not fail the test suite.
- No automated PR/pipeline checks are configured.

## CI Command - Checks to run inside a CI pipeline

The CI runner must provide the approved Python package index and system certificates. 

These provide API/agent dependency check, Python tests and Ruff checks, UI install/test/lint/build.

From the
repository root, run:

```bash copy Copy CI Checks
set -euo pipefail

UV_DEFAULT_INDEX=https://artifactory.srv.westpac.com.au/artifactory/api/pypi/westpac-pypi/simple \
UV_SYSTEM_CERTS=true uv sync --directory src/api --extra dev --locked
UV_DEFAULT_INDEX=https://artifactory.srv.westpac.com.au/artifactory/api/pypi/westpac-pypi/simple \
UV_SYSTEM_CERTS=true uv sync --directory src/agent --extra dev --locked

uv run --directory src/api pytest
uv run --directory src/api ruff check .
uv run --directory src/api ruff format --check .
uv run --directory src/agent pytest
uv run --directory src/agent ruff check .
uv run --directory src/agent ruff format --check .

npm --prefix src/ui ci
npm --prefix src/ui test -- --run
npm --prefix src/ui run lint
npm --prefix src/ui run build

```

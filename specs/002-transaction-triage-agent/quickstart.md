# Quickstart: Transaction Triage Reasoning Agent

## Prerequisites

- Python 3.12+
- Shared mock data at `sample_data/transactions.json`
- The agent environment managed from `src/agent/`

## Install and test

From the repository root:

```bash
UV_DEFAULT_INDEX=https://artifactory.srv.westpac.com.au/artifactory/api/pypi/westpac-pypi/simple \
UV_SYSTEM_CERTS=true uv sync --directory src/agent --extra dev
uv run --directory src/agent pytest
uv run --directory src/agent ruff check .
```

## Validate the interaction flow

1. Process “I don’t recognise $50 at Woolworths”; expect the shared `txn-001` match.
2. Search a non-matching merchant or amount; expect exactly three ranked alternatives.
3. Select a transaction, answer merchant unknown; expect a Fraud/scam proposal without a case ID.
4. Confirm that proposal; expect one local mock case ID and next steps.
5. Follow the known/merchant-refund-agreed path; expect merchant guidance and no case ID.
6. Include an email address in a message; assert no output or session log contains it unmasked.

See the [library contract](contracts/transaction-agent.md) and [data model](data-model.md) for result
and state requirements.

# Implementation Plan: Transaction Triage Reasoning Agent

**Branch**: `002-transaction-triage-agent` | **Date**: 2026-11-08 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/002-transaction-triage-agent/spec.md`

## Summary

Build `agn-digiservcing-transactiontriage-v1`, a typed, deterministic Python library consumed by the
local API. It will mask customer text, infer message intent and transaction details, search the shared
JSON fixture, advance a three-question triage session, and return a confirmation-gated local mock
case. The implementation is under `src/agent`; shared transactions remain at the repository-level
`sample_data/transactions.json` for use by every component.

## Technical Context

**Language/Version**: Python 3.12+ (current local tooling: Python 3.15)

**Primary Dependencies**: Standard library for parsing and matching; Pydantic v2 for typed agent
contracts; pytest and Ruff for verification and style

**Storage**: Version-controlled `sample_data/transactions.json`; per-session masked JSON-lines logs
under `src/agent/logs/`

**Testing**: pytest unit and integration tests under `src/agent/tests/`

**Target Platform**: Local Python process, invoked by the local API

**Project Type**: Python library component

**Performance Goals**: Deterministic in-process processing of one local message and fixture search;
no network calls or external process dependencies

**Constraints**: No external LLM, database, banking API, cloud service, or automatic case creation;
mask PII before parsing, outputs, and logs

**Scale/Scope**: One mocked customer, 50 shared transactions, five baseline merchants, one active
triage session per correlation ID

## Constitution Check

**Pre-design gate: PASS.**

- Deterministic local functions and a static shared JSON fixture satisfy the mock-only architecture.
- The agent emits a proposal and never a case before explicit confirmation, satisfying immutable
  verdict and confirmation rules.
- Masking and correlation IDs are enforced within the agent, complementing the API boundary.
- The agent is API-consumed only; it does not create a customer-facing interface or bypass the API.
- Tests, strict type hints, Ruff, local logs, and removal of legacy fixture paths are planned.

**Post-design gate: PASS.** The data model and callable contract retain all of the above boundaries.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/agent/
├── pyproject.toml              # Agent-specific dependencies and quality settings
├── transaction_agent/
│   ├── __init__.py
│   ├── models.py               # Typed inputs, results, sessions, and proposals
│   ├── engine.py               # Message orchestration and triage state transitions
│   ├── parsing.py              # Masked keyword, merchant, and amount extraction
│   ├── repository.py           # Read-only shared JSON transaction loader/search
│   ├── pii.py                  # Regex masking helpers
│   ├── logging_service.py      # Correlation-linked masked local event logging
│   └── future_llm.py           # Inactive documented extension interface
├── logs/                       # Runtime local session logs; ignored by Git
└── tests/
    ├── test_parsing.py
    ├── test_transaction_search.py
    ├── test_triage_flow.py
    ├── test_confirmation.py
    └── test_safety_and_logging.py
sample_data/
└── transactions.json           # Shared mock fixture; owned at project level
```

**Structure Decision**: Keep the agent independently installable beneath `src/agent` while resolving
the shared fixture from the repository root. The API calls its explicit library contract; the UI never
reads the fixture or agent directly.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations require justification.

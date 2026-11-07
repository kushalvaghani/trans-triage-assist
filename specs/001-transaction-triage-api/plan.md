# Implementation Plan: Transaction Triage API

**Branch**: `001-transaction-triage-api` | **Date**: 2026-11-07 | **Spec**:
[spec.md](spec.md)

**Input**: Feature specification from `/specs/001-transaction-triage-api/spec.md`

## Summary

Build a local Python web service that accepts customer chat messages and confirmed transaction
submissions. It masks PII at the API boundary, delegates deterministic transaction triage to the
local reasoning component, returns customer-safe responses, and records correlation-linked local
session logs. The service exposes the two specified POST paths, uses only static JSON mock data, and
never accesses live banking, cloud, database, or external AI services.

## Technical Context

**Language/Version**: Python 3.12

**Primary Dependencies**: FastAPI, Pydantic v2, Uvicorn, pytest, httpx, Ruff

**Storage**: Version-controlled JSON mock transactions and local session log files; no database

**Testing**: pytest with FastAPI/httpx endpoint contract and integration tests

**Target Platform**: Local developer machine and CI on a supported Python 3.12 runtime

**Project Type**: Web service

**Performance Goals**: A local request completes within 1 second for the 50–100 transaction mock set

**Constraints**: Two fixed POST paths; all API code and tests under `src/api`; deterministic local
reasoning only; regex-based PII masking before reasoning or logging; explicit confirmation before a
mock case ID; no external services

**Scale/Scope**: One mocked customer, 50–100 static transactions, two public endpoints, and local
session logs

## Constitution Check

### Pre-Design Gate

| Principle | Plan Response | Status |
|---|---|---|
| Guided, contained chat experience | API returns customer-safe text and structured data that the chat UI renders; unrelated messages receive transaction-support redirection. | Pass |
| Deterministic search and triage | The API calls only local deterministic matching and the defined three-question decision flow. | Pass |
| Mock-only, component-scoped architecture | Static JSON and local utilities are the only data sources; this plan covers only the Python API component. | Pass |
| Financial safety and confirmation | Boundary masking, immutable proposals, and confirmation-gated case creation are endpoint contracts. | Pass |
| Quality and traceability | Strict type hints, Ruff, pytest, correlation IDs, and masked local session logs are mandatory. | Pass |

No constitutional exception or complexity justification is required.

### Post-Design Gate

The data model, endpoint contract, and validation guide below preserve the same five controls. No
design element introduces a live integration, external LLM, unmasked PII path, or automatic case
submission. **Pass.**

## Project Structure

### Documentation (this feature)

```text
specs/001-transaction-triage-api/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── transaction-triage-api.openapi.yaml
└── tasks.md                 # Created later by the tasks workflow
```

### Source Code (repository root)

```text
src/api/
├── app.py                   # Application assembly and routes
├── models.py                # Typed request and response models
├── routes.py                # Message and submission endpoint handlers
├── triage_service.py        # API orchestration and confirmation gate
├── pii.py                   # Boundary masking helpers
├── logging_service.py        # Correlation-aware masked session logging
├── sample_data/
│   └── transactions.json    # 50–100 mocked transactions for one customer
├── logs/                    # Runtime local session logs; ignored by Git
└── tests/
    ├── test_message_endpoint.py
    ├── test_submission_endpoint.py
    ├── test_pii_masking.py
    └── test_logging.py
```

**Structure Decision**: A single Python web-service component under `src/api` keeps the delivery
scope aligned with the feature specification. Route handlers remain thin; typed models, boundary
masking, orchestration, and session logging are isolated so each safety rule is directly testable.

## Complexity Tracking

No constitutional violations or unnecessary complexity require tracking.

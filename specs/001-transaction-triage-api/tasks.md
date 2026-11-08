# Tasks: Transaction Triage API

**Input**: Design documents from `/specs/001-transaction-triage-api/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, and
`contracts/transaction-triage-api.openapi.yaml`

**Tests**: Required by the feature specification. Write each test before its implementation and
confirm it fails for the intended missing behavior.

**Organization**: Tasks are grouped by user story so every increment is independently testable.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the Python API project, quality tooling, and planned package layout.

- [X] T001 Create the Python 3.12 dependency and tool configuration in `pyproject.toml` with FastAPI, Pydantic v2, Uvicorn, pytest, httpx, and Ruff.
- [X] T002 Create the API package and test package structure in `src/api/__init__.py` and `src/api/tests/__init__.py`.
- [X] T003 [P] Configure strict type-check-friendly Ruff linting and PEP 8 formatting rules in `pyproject.toml`.
- [X] T004 [P] Add local session-log ignore rules for `src/api/logs/` in `.gitignore`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Provide shared typed contracts, safety controls, fixtures, logging, and application
assembly that every user story needs.

**⚠️ CRITICAL**: Complete this phase before implementing any user story.

- [X] T005 Create typed request, response, transaction, and outcome models in `src/api/models.py`, including required non-blank `message`, positive decimal `amount`, UUID-form `correlation_id`, and `fraud_scam`, `dispute`, and `merchant_refund_guidance` outcomes.
- [X] T006 [P] Create regex-based PII masking helpers in `src/api/pii.py` for email addresses, phone numbers, card-like strings, and account-like number sequences before downstream processing.
- [X] T007 [P] Create correlation-aware masked JSON-lines session logging in `src/api/logging_service.py` that writes one local log file per correlation ID under `src/api/logs/`.
- [X] T008 Create 50–100 fictional transactions for one mocked customer in `sample_data/transactions.json`, including unique `transaction_id`, `customer_id`, `merchant`, positive two-decimal `amount`, ISO `transaction_date`, and customer-safe `description` fields.
- [X] T009 Create deterministic transaction loading, merchant/amount matching, closest-alternative selection, and three-question outcome helpers in `src/api/triage_service.py` using only `sample_data/transactions.json`.
- [X] T010 Assemble the FastAPI application, route registration, correlation-ID generation, and customer-safe validation/error responses in `src/api/app.py`.

**Checkpoint**: Shared models, local fixture, masking, logging, deterministic triage helpers, and app
assembly are ready for endpoint stories.

---

## Phase 3: User Story 1 - Process a Customer Message (Priority: P1) 🎯 MVP

**Goal**: Customers can send a chat message and receive transaction choices, safe redirection, or a
safe failure response from the message endpoint.

**Independent Test**: Send a valid transaction-reporting message to the message endpoint and verify a
correlation ID and transaction-processing response; independently verify unrelated and invalid-message
responses.

### Tests for User Story 1

- [X] T011 [US1] Write message endpoint contract tests in `src/api/tests/test_message_endpoint.py` for `POST /exp-digiServicing-transctiontraige/v1/message`, required non-blank `message`, and returned UUID-form `correlation_id`.
- [X] T012 [US1] Write message-processing integration tests in `src/api/tests/test_message_endpoint.py` for an exact mock transaction match, a not-found response with alternatives, unrelated-message redirection, and customer-safe failures.

### Implementation for User Story 1

- [X] T013 [US1] Implement message request handling in `src/api/routes.py` that masks input before invoking `src/api/triage_service.py` and logs only masked session events through `src/api/logging_service.py`.
- [X] T014 [US1] Add `POST /exp-digiServicing-transctiontraige/v1/message` in `src/api/routes.py` to return `transaction_matches`, `not_found`, `redirection`, or `error` responses defined by `specs/001-transaction-triage-api/contracts/transaction-triage-api.openapi.yaml`.
- [X] T015 [US1] Wire the message route into the application in `src/api/app.py` and ensure all successful and failure responses contain the active `correlation_id`.

**Checkpoint**: User Story 1 can process valid transaction-reporting messages independently and safely
redirect unsupported messages.

---

## Phase 4: User Story 2 - Submit a Confirmed Transaction for Triage (Priority: P2)

**Goal**: Customers can submit a selected, confirmed mock transaction and receive the correct
Fraud/scam, Dispute, or merchant-refund result.

**Independent Test**: Submit each branch of the decision table to the submission endpoint and verify
the specified outcome, confirmation gate, case-ID behavior, and next steps.

### Tests for User Story 2

- [X] T016 [US2] Write submission endpoint contract tests in `src/api/tests/test_submission_endpoint.py` for `POST /exp-digiServicing-transctiontraige/v1/submission`, required `transaction_id`, `merchant_known`, and `confirmed` fields.
- [X] T017 [US2] Write triage decision-table tests in `src/api/tests/test_submission_endpoint.py` for unknown merchant Fraud/scam, customer-did-not-make-purchase Fraud/scam, known merchant/no refund/customer-made-purchase Dispute, and merchant-refund guidance.
- [X] T018 [US2] Write confirmation-gate tests in `src/api/tests/test_submission_endpoint.py` proving `confirmed: false` returns no `case_id` and repeated or malformed submissions do not create duplicate case IDs.

### Implementation for User Story 2

- [X] T019 [US2] Add conditional submission validation in `src/api/models.py`: require `merchant_refund_agreed` only when `merchant_known` is true and require `customer_made_purchase` only when no refund was agreed.
- [X] T020 [US2] Implement immutable outcome proposal evaluation and local mock case-ID generation in `src/api/triage_service.py`, returning a case ID only for confirmed `fraud_scam` or `dispute` outcomes.
- [X] T021 [US2] Implement `POST /exp-digiServicing-transctiontraige/v1/submission` in `src/api/routes.py`, including selected-transaction lookup, explicit confirmation enforcement, masked logging, and customer-safe next steps.
- [X] T022 [US2] Register the submission route and its `400` and `404` customer-safe responses in `src/api/app.py` to match `specs/001-transaction-triage-api/contracts/transaction-triage-api.openapi.yaml`.

**Checkpoint**: User Stories 1 and 2 both work independently; unconfirmed submissions never return a
case ID.

---

## Phase 5: User Story 3 - Trace a Safe Triage Request (Priority: P3)

**Goal**: Support and development teams can trace an API interaction through masked, correlation-ID
linked local logs without exposing PII.

**Independent Test**: Submit a request containing maskable PII, then verify its response and local
session log share one correlation ID and contain no unmasked PII.

### Tests for User Story 3

- [X] T023 [P] [US3] Write PII boundary-masking tests in `src/api/tests/test_pii_masking.py` for email, phone, card-like, and account-like inputs used by both endpoints.
- [X] T024 [P] [US3] Write correlation and local-log tests in `src/api/tests/test_logging.py` proving one request produces one correlation-ID-named log file with masked session events.

### Implementation for User Story 3

- [X] T025 [US3] Apply `src/api/pii.py` masking to every message and submission logging path in `src/api/routes.py` before any call to `src/api/logging_service.py` or `src/api/triage_service.py`.
- [X] T026 [US3] Extend `src/api/logging_service.py` to record endpoint, response type, outcome, and error events with the active correlation ID while excluding raw customer content.
- [X] T027 [US3] Add correlation-ID propagation and safe error-path coverage to `src/api/app.py` so malformed payloads, lookup failures, and triage failures return a correlation ID without PII.

**Checkpoint**: All three user stories are independently functional, traceable, and compliant with
the PII and confirmation safeguards.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify the delivery against its public contract, quality standards, and runnable guide.

- [X] T028 [P] Validate the implemented endpoints against `specs/001-transaction-triage-api/contracts/transaction-triage-api.openapi.yaml` in `src/api/tests/test_contract.py`.
- [X] T029 [P] Run and correct Ruff findings for all Python files under `src/api/`.
- [X] T030 Run the end-to-end scenarios in `specs/001-transaction-triage-api/quickstart.md` and document any command updates in that file.
- [X] T031 Remove unused boilerplate and legacy mock-data paths from `src/api/` before declaring the feature complete.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: Starts immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1 and blocks every user story.
- **Phase 3 (US1)**: Depends on Phase 2; delivers the MVP message-processing path.
- **Phase 4 (US2)**: Depends on Phase 2 and reuses the transaction fixture and triage service from US1.
- **Phase 5 (US3)**: Depends on Phase 2 and can validate both endpoint paths after they exist.
- **Phase 6 (Polish)**: Depends on the desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Starts after foundational work and is the recommended MVP.
- **US2 (P2)**: Uses the shared mock transaction fixture and triage service; it can be built after US1
  to exercise the full customer journey.
- **US3 (P3)**: Applies cross-endpoint safety verification after US1 and US2 routes are available.

### Parallel Opportunities

- T003 and T004 can run after T001; T006–T008 can run after T005's model definitions are agreed.
- T011–T012 and T016–T018 share test files and must run sequentially; T023 and T024 can run together.
- T028 and T029 can run together after the three user-story phases finish.

## Parallel Example: User Story 3

```text
Task: "T023 PII masking tests in src/api/tests/test_pii_masking.py"
Task: "T024 local-log tests in src/api/tests/test_logging.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phases 1 and 2.
2. Complete Phase 3 and run the message endpoint tests.
3. Validate exact matches, alternatives, unsupported-message redirection, PII masking, and correlation
   IDs before proceeding.

### Incremental Delivery

1. Add US1 for message processing.
2. Add US2 for confirmation-gated triage submission.
3. Add US3 for full traceability verification.
4. Complete the Phase 6 contract, lint, quickstart, and cleanup checks.

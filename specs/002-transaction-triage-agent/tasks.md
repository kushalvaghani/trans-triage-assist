---

description: "Implementation tasks for the transaction triage reasoning agent"
---

# Tasks: Transaction Triage Reasoning Agent

**Input**: Design documents from `/specs/002-transaction-triage-agent/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`,
`contracts/transaction-agent.md`, and `quickstart.md`

**Tests**: Required by the specification's measurable success criteria. Write each test before the
behavior it covers and verify it fails on the preceding implementation state.

**Organization**: Tasks are grouped by user story so each increment is independently testable.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the standalone agent package and its local quality tooling.

- [X] T001 Create the agent package, test package, and package initializer in `src/agent/transaction_agent/__init__.py` and `src/agent/tests/__init__.py`.
- [X] T002 Create Python dependency, pytest, and Ruff configuration in `src/agent/pyproject.toml` for Pydantic v2, pytest, and Ruff.
- [X] T003 [P] Add ignored local agent session logs in `.gitignore` for `src/agent/logs/`.
- [X] T004 Generate the agent dependency lock file at `src/agent/uv.lock` using `uv sync --directory src/agent --extra dev`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create shared typed contracts, fixture access, masking, and logging before user-story
flows begin.

**⚠️ CRITICAL**: Complete this phase before any user-story work.

- [X] T005 Create typed transaction, interaction, result, session, proposal, outcome, and question models in `src/agent/transaction_agent/models.py`, including a required UUID `correlation_id` and positive two-decimal transaction `amount`.
- [X] T006 [P] Create regex PII masking helpers for email, phone, card-like, and account-like strings in `src/agent/transaction_agent/pii.py`.
- [X] T007 [P] Create correlation-ID-named JSON-lines session logging that accepts only masked event values in `src/agent/transaction_agent/logging_service.py`.
- [X] T008 Create a read-only shared-fixture loader in `src/agent/transaction_agent/repository.py` for `sample_data/transactions.json`, validating its 50–100 unique transaction IDs and one mocked customer.
- [X] T009 Create the inactive future LLM intent and transaction-tool interface, with comments proving it is never invoked, in `src/agent/transaction_agent/future_llm.py`.

**Checkpoint**: The agent has safe contracts and can read the global fixture without network access.

---

## Phase 3: User Story 1 - Find a Reported Transaction (Priority: P1) 🎯 MVP

**Goal**: Extract a supported merchant and valid dollar amount, return an exact shared transaction,
or exactly three deterministic alternatives.

**Independent Test**: Process “I don’t recognise $50 at Woolworths” and receive `txn-001`; process a
non-match and receive three alternatives; process a message without usable details and receive a safe
request for details.

### Tests for User Story 1

- [X] T010 [P] [US1] Write parser tests for baseline merchants, dollar amounts with and without cents, multiple candidates, and unsupported formats in `src/agent/tests/test_parsing.py`.
- [X] T011 [P] [US1] Write search tests for exact match, merchant-first then amount-difference ranking, and exactly three alternatives in `src/agent/tests/test_transaction_search.py`.
- [X] T012 [US1] Write interaction tests for reporting intent, request-details response, and masked result content in `src/agent/tests/test_message_flow.py`.

### Implementation for User Story 1

- [X] T013 [US1] Implement masked keyword intent, merchant, and dollar-amount extraction in `src/agent/transaction_agent/parsing.py`.
- [X] T014 [US1] Implement exact and three-alternative transaction searches over `sample_data/transactions.json` in `src/agent/transaction_agent/repository.py`.
- [X] T015 [US1] Implement report-message orchestration and customer-safe result kinds in `src/agent/transaction_agent/engine.py`.
- [X] T016 [US1] Record masked reporting interactions and search results with their correlation IDs in `src/agent/transaction_agent/logging_service.py`.

**Checkpoint**: Transaction search works independently, including safe missing-detail and not-found
outcomes.

---

## Phase 4: User Story 2 - Determine a Proposed Triage Outcome (Priority: P2)

**Goal**: Progress a selected transaction through the ordered questions and return the required
proposal or no-case merchant-refund guidance.

**Independent Test**: Start a triage session and verify the question order and outcomes for unknown
merchant, known/refund agreed, known/no refund/not made, and known/no refund/made paths.

### Tests for User Story 2

- [X] T017 [P] [US2] Write tests for transaction selection and the ordered three-question state transitions in `src/agent/tests/test_triage_flow.py`.
- [X] T018 [P] [US2] Write decision-table tests for Fraud/scam, Dispute, and merchant-refund guidance outcomes in `src/agent/tests/test_triage_flow.py`.

### Implementation for User Story 2

- [X] T019 [US2] Implement selected-transaction validation and immutable session state in `src/agent/transaction_agent/models.py`.
- [X] T020 [US2] Implement answer parsing and question progression—merchant known, refund agreed, then customer made purchase—in `src/agent/transaction_agent/engine.py`.
- [X] T021 [US2] Implement deterministic Fraud/scam, Dispute, and merchant-refund proposal construction with customer-safe next steps in `src/agent/transaction_agent/engine.py`.
- [X] T022 [US2] Log only masked triage question and proposal events in `src/agent/transaction_agent/logging_service.py`.

**Checkpoint**: A selected transaction reaches a deterministic outcome in no more than three
questions, with no case created.

---

## Phase 5: User Story 3 - Confirm a Proposed Case (Priority: P3)

**Goal**: Return a stable local mock case ID only after explicit confirmation of a Fraud/scam or
Dispute proposal.

**Independent Test**: Attempt early confirmation and receive no case; confirm each proposal and
receive one deterministic local mock case ID; confirm merchant-refund guidance and receive no case.

### Tests for User Story 3

- [X] T023 [P] [US3] Write confirmation-gate tests for early, unconfirmed, and repeated confirmations in `src/agent/tests/test_confirmation.py`.
- [X] T024 [P] [US3] Write outcome-specific case-ID and merchant-refund no-case tests in `src/agent/tests/test_confirmation.py`.

### Implementation for User Story 3

- [X] T025 [US3] Implement explicit-confirmation validation and stable local mock case-ID creation in `src/agent/transaction_agent/engine.py`.
- [X] T026 [US3] Enforce the immutable-proposal rule and return customer-safe errors for invalid confirmations in `src/agent/transaction_agent/models.py` and `src/agent/transaction_agent/engine.py`.
- [X] T027 [US3] Record masked confirmation attempts and outcomes with correlation IDs in `src/agent/transaction_agent/logging_service.py`.

**Checkpoint**: Confirmed proposals create only local mock cases; every other path returns no case.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Prove the component is safe, shared-data-compatible, and ready for API integration.

- [X] T028 [P] Add PII masking, correlation propagation, and log-content tests in `src/agent/tests/test_safety_and_logging.py`.
- [X] T029 [P] Add callable-contract tests against `specs/002-transaction-triage-agent/contracts/transaction-agent.md` in `src/agent/tests/test_contract.py`.
- [X] T030 Run and correct Ruff findings under `src/agent/` using `uv run --directory src/agent ruff check .` and `uv run --directory src/agent ruff format --check .`.
- [X] T031 Run the end-to-end scenarios in `specs/002-transaction-triage-agent/quickstart.md` and remove obsolete agent fixture paths or boilerplate from `src/agent/`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)** starts immediately.
- **Foundational (Phase 2)** depends on setup and blocks all stories.
- **US1 (Phase 3)** depends on foundational parsing, fixture access, and models.
- **US2 (Phase 4)** depends on US1 transaction selection.
- **US3 (Phase 5)** depends on US2 proposal construction.
- **Polish (Phase 6)** depends on all desired stories.

### User Story Dependencies

- **US1 (P1)** is the MVP and independently delivers safe transaction discovery.
- **US2 (P2)** consumes a selected transaction from US1 and adds deterministic triage proposals.
- **US3 (P3)** consumes immutable proposals from US2 and supplies confirmation-gated mock cases.

### Parallel Opportunities

- T003 can run alongside T001–T002; T006–T007 can run alongside T005.
- T010 and T011 can run in parallel; T017 and T018 can run in parallel; T023 and T024 can run in
  parallel.
- T028 and T029 can run in parallel after all user stories.

## Parallel Example: User Story 1

```text
Task: "T010 parser tests in src/agent/tests/test_parsing.py"
Task: "T011 transaction search tests in src/agent/tests/test_transaction_search.py"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete setup and foundational safety/fixture tasks.
2. Implement and verify deterministic transaction extraction and search.
3. Validate US1 independently before adding triage state.

### Incremental Delivery

1. Deliver US1 transaction search.
2. Add US2 ordered triage proposals.
3. Add US3 confirmation-gated mock cases.
4. Complete safety, contract, lint, and quickstart validation.

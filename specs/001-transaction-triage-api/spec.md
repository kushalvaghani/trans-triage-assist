# Feature Specification: Transaction Triage API

**Feature Branch**: `001-transaction-triage-api`

**Created**: 2026-11-07

**Status**: Draft

**Input**: User description: "Build a Python API with tests to process incoming customer chat
messages and submit transactions for triage. Provide POST
`/exp-digiServicing-transctiontraige/v1/message` and POST
`/exp-digiServicing-transctiontraige/v1/submission`; all code lives under `src/api`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Process a Customer Message (Priority: P1)

As a customer, I can submit a chat message about a transaction and receive a response that advances
my transaction-reporting journey.

**Why this priority**: Receiving and processing a customer message is the entry point for every
triage journey.

**Independent Test**: Send a valid customer message to the message endpoint and confirm that the
response identifies whether the message can be handled as a transaction-reporting request.

**Acceptance Scenarios**:

1. **Given** a customer submits a transaction-reporting message, **When** the message endpoint
   processes it, **Then** the customer receives a response for the next step in their journey.
2. **Given** a customer submits an unrelated message, **When** the message endpoint processes it,
   **Then** the response politely redirects the customer to transaction issues.
3. **Given** a message is invalid or cannot be processed, **When** the message endpoint receives it,
   **Then** the customer receives a clear, safe error response.

---

### User Story 2 - Submit a Confirmed Transaction for Triage (Priority: P2)

As a customer, I can submit a transaction I have reviewed and confirmed so that I receive a proposed
triage outcome, a mock case identifier when appropriate, and clear next steps.

**Why this priority**: Submission completes the reporting journey, but depends on a processed
message and a customer-confirmed transaction.

**Independent Test**: Submit a reviewed, confirmed transaction and verify that the returned outcome
is either a mock Fraud/scam case, a mock Dispute case, or merchant-refund guidance without a case.

**Acceptance Scenarios**:

1. **Given** a customer submits a selected and explicitly confirmed transaction, **When** the
   submission endpoint evaluates it, **Then** it returns the immutable proposed outcome and relevant
   next steps.
2. **Given** the triage outcome is Fraud/scam or Dispute, **When** the customer has confirmed the
   transaction, **Then** the response includes a local mock case identifier and next-step details.
3. **Given** a merchant has agreed to refund the transaction, **When** the submission endpoint
   evaluates it, **Then** the response tells the customer to contact the merchant and does not create
   a case identifier.
4. **Given** a customer has not explicitly confirmed the transaction, **When** they submit it for
   triage, **Then** the submission is rejected without creating a case identifier.

---

### User Story 3 - Trace a Safe Triage Request (Priority: P3)

As a support or development team member, I can trace a request across the service without exposing a
customer's personally identifiable information.

**Why this priority**: Safe traceability supports diagnosis and compliance after the customer-facing
journey is working.

**Independent Test**: Process a request containing maskable personal information and confirm that
the service returns a correlation identifier while the associated session log contains masked data.

**Acceptance Scenarios**:

1. **Given** either endpoint receives a request, **When** it is processed, **Then** all related
   service events share one correlation identifier.
2. **Given** a request contains personally identifiable information, **When** it crosses the service
   boundary, **Then** the information is masked before it is logged or used for reasoning.

### Edge Cases

- A customer message has no recognisable transaction amount or merchant.
- A message identifies a merchant outside the mock transaction set.
- A request omits required transaction-selection or confirmation details.
- A repeated or malformed submission must not yield multiple case identifiers.
- A failure in transaction lookup or triage must not disclose unmasked customer information.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The service MUST expose a POST endpoint at
  `/exp-digiServicing-transctiontraige/v1/message` that accepts an incoming customer chat message and
  returns a customer-safe processing response.
- **FR-002**: The service MUST expose a POST endpoint at
  `/exp-digiServicing-transctiontraige/v1/submission` that accepts a selected transaction and an
  explicit customer confirmation for triage.
- **FR-003**: The message-processing response MUST identify transaction-reporting messages and
  redirect unrelated messages to transaction support.
- **FR-004**: The service MUST use only local mock transaction data when processing and submitting
  transactions; it MUST NOT access live banking, cloud, database, or external AI services.
- **FR-005**: The service MUST apply deterministic triage using the defined three-question decision
  flow: merchant known, merchant refund agreed, and customer made purchase.
- **FR-006**: The service MUST propose Fraud/scam for an unknown merchant or a purchase the customer
  did not make, and MUST propose Dispute for a customer-made purchase when a known merchant has not
  agreed to refund.
- **FR-007**: The service MUST return merchant-refund guidance without creating a case when the
  merchant has agreed to refund.
- **FR-008**: The service MUST require explicit customer confirmation before creating a local mock
  case identifier; it MUST reject unconfirmed submissions.
- **FR-009**: The service MUST mask personally identifiable information at its boundary before
  reasoning, logging, or responding.
- **FR-010**: The service MUST associate all processing and logging for a request with a correlation
  identifier and record masked session events in a local log file.
- **FR-011**: The service MUST return clear, customer-safe failure responses for invalid messages,
  missing submission data, transaction lookup failures, and triage failures.
- **FR-012**: The service implementation and its automated tests MUST live under `src/api`.

### Key Entities *(include if feature involves data)*

- **Customer Message**: A customer's incoming chat text and its request correlation identifier.
- **Mock Transaction**: A transaction in the local mock set, identified by merchant, amount, and
  transaction reference.
- **Triage Submission**: A selected mock transaction, customer confirmation, and triage answers.
- **Triage Outcome**: The immutable proposed Fraud/scam, Dispute, or merchant-refund result and its
  next-step details.
- **Mock Case**: A local-only case identifier returned for confirmed Fraud/scam or Dispute outcomes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of valid transaction-reporting messages receive a customer-safe response from the
  message endpoint.
- **SC-002**: 100% of confirmed submissions following each branch of the three-question decision
  flow return the specified outcome and next-step details.
- **SC-003**: 100% of unconfirmed submissions are rejected without a case identifier.
- **SC-004**: 100% of requests produce a correlation identifier, and session logs contain no
  unmasked personally identifiable information in automated verification.
- **SC-005**: All automated tests for the two endpoint contracts and their stated failure paths pass.

## Assumptions

- The two endpoint paths are intentional as supplied, including the `transctiontraige` spelling.
- The API is the Python component specification; separate specifications will define the React chat
  UI and localized reasoning-agent components.
- Mock transaction data and local case identifiers are sufficient for this feature; authentication,
  authorization, and real banking integrations are out of scope.
- A submission contains the customer-selected transaction, explicit confirmation, and answers needed
  to apply the defined triage decision flow.

# Feature Specification: Transaction Triage Chat UI

**Feature Branch**: `003-transaction-triage-ui`

**Created**: 2026-11-07

**Status**: Draft


## User Scenarios & Testing *(mandatory)*

### User Story 1 - Start a Transaction Report (Priority: P1)

As a customer, I can start a transaction report from a clear chat interface and send my request for
processing.

**Why this priority**: Starting a report is the entry point for every customer journey.

**Independent Test**: Open a new chat, choose the preset label or enter a transaction-reporting
message, send it, and confirm that the message and processing response appear in the chat.

**Acceptance Scenarios**:

1. **Given** a customer opens a new chat, **When** the interface loads, **Then** it displays a
   welcome greeting, the Westpac logo, and the preset label “Report $50 at Woolworths”.
2. **Given** a customer chooses the preset label, **When** it is used, **Then** the corresponding
   transaction-reporting message is placed in the chat for submission.
3. **Given** a customer sends a transaction-reporting message, **When** the service responds, **Then**
   the customer message and service response appear in the chat transcript.
4. **Given** a customer sends an unrelated message, **When** the interface receives the response,
   **Then** it displays the transaction-support redirection supplied by the service.

---

### User Story 2 - Review Transaction and Triage Cards (Priority: P2)

As a customer, I can review transaction choices, triage questions, and a proposed outcome directly in
the chat before confirming it.

**Why this priority**: The customer must understand and review their transaction before it can be
submitted for triage.

**Independent Test**: Submit a transaction-reporting message that returns transaction choices, select
one, complete triage answers, and confirm that the transaction, question, and outcome content are
displayed as chat cards.

**Acceptance Scenarios**:

1. **Given** transaction choices are returned, **When** the interface displays them, **Then** each
   choice appears as a selectable card within the chat transcript.
2. **Given** the customer selects a transaction, **When** triage requires an answer, **Then** the
   applicable question is displayed in a chat card and the customer can provide an answer.
3. **Given** a Fraud/scam or Dispute proposal is returned, **When** the customer reviews it, **Then**
   the proposal and next steps are displayed in a confirmation card with an explicit confirm action.
4. **Given** the customer confirms the proposal, **When** the final response is returned, **Then** the
   mock case identifier and supporting details appear in the chat.

---

### User Story 3 - Recover from an Unmatched Merchant (Priority: P3)

As a customer, I receive clear guidance and available alternatives when the merchant or transaction I
search for cannot be found.

**Why this priority**: Helpful recovery prevents a failed search from ending the customer journey.

**Independent Test**: Send a message naming an unavailable merchant and confirm the prescribed
not-found message and exactly three merchant alternatives with available transactions are shown.

**Acceptance Scenarios**:

1. **Given** the service cannot find the requested merchant or transaction, **When** the interface
   renders the result, **Then** it displays “Could not find the merchant, please search for other
   transactions”.
2. **Given** the merchant is not found, **When** alternatives are available, **Then** the interface
   displays exactly three merchants for which the mocked customer has transactions.
3. **Given** the customer selects an alternative merchant, **When** the interface submits the new
   search, **Then** the resulting transaction choices are shown in the chat.

### Edge Cases

- The chat transcript exceeds the visible chat area.
- A transaction, triage, or confirmation response arrives after the customer restarts the chat.
- A customer attempts to confirm a proposal that is not displayed or is no longer current.
- The service response lacks the required three merchant alternatives.
- The service request fails while a transaction, merchant alternative, or confirmation card is shown.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The UI MUST consume the transaction-triage service for customer messages, transaction
  selections, triage answers, and confirmed submissions.
- **FR-002**: The UI MUST present a welcome greeting, Westpac logo, chat input, and a preset label
  reading “Report $50 at Woolworths” when a chat session starts.
- **FR-003**: The UI MUST render every customer message and service response in chronological chat
  order.
- **FR-004**: The UI MUST render transaction choices, triage questions, proposed outcomes,
  confirmations, and final case details as cards within the chat transcript where applicable.
- **FR-005**: The chat transcript MUST support scrolling by default and keep newly added content
  reachable without losing earlier conversation history.
- **FR-006**: When the service reports a missing transaction or merchant, the UI MUST display the
  exact customer message “Could not find the merchant, please search for other transactions”.
- **FR-007**: For a missing merchant or transaction, the UI MUST display exactly three alternative
  merchants that have transactions for the mocked customer and allow the customer to search one.
- **FR-008**: The UI MUST render the service-provided triage question sequence and submit only the
  customer's selected answer for the active question.
- **FR-009**: The UI MUST show Fraud/scam and Dispute results as proposals, require an explicit
  confirmation action, and MUST NOT submit a case automatically.
- **FR-010**: The UI MUST show merchant-refund guidance without offering a case-confirmation action.
- **FR-011**: The UI MUST display local mock case identifiers and next-step details only after the
  service confirms a customer-approved proposal.
- **FR-012**: The UI MUST provide a restart action at every stage that clears the current transcript
  and begins a new greeted chat session.
- **FR-013**: The UI MUST display clear, customer-safe error content when the service cannot process
  a request.
- **FR-014**: The UI implementation and automated tests MUST live under `src/ui`.

### Key Entities *(include if feature involves data)*

- **Chat Session**: A customer-visible ordered transcript and its correlation identifier.
- **Chat Message**: Customer or service content rendered in the transcript.
- **Chat Card**: Structured transcript content representing a transaction, question, proposal,
  confirmation, case details, or merchant alternative.
- **Transaction Selection**: The customer’s chosen mocked transaction sent for triage.
- **Merchant Alternative**: A supported merchant with mocked customer transactions shown after an
  unsuccessful search.
- **Confirmation State**: The explicit customer approval required before a proposed case is submitted.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of new chat sessions display the greeting, Westpac logo, and preset label before a
  customer sends a message.
- **SC-002**: 100% of transaction choices, triage questions, proposals, confirmations, and final case
  details are rendered in the chat transcript, with structured content shown as cards.
- **SC-003**: 100% of transcripts with content beyond the visible chat area remain scrollable and
  retain access to the complete conversation.
- **SC-004**: 100% of merchant-not-found responses display the required message and exactly three
  available merchant alternatives when the service supplies them.
- **SC-005**: 100% of Fraud/scam and Dispute case submissions require explicit customer confirmation,
  and 100% of restart actions create a cleared, greeted session.

## Assumptions

- The UI is the separate frontend component and consumes the API and reasoning-agent components
  defined in their own specifications.
- The service provides the three available merchant alternatives from mocked customer transaction
  data; the UI renders those alternatives rather than determining them itself.
- The UI has no access to live banking data, case systems, external cloud services, or external AI
  services.
- Mock data supplies at least three merchants with customer transactions so each merchant-not-found
  response can contain the required three alternatives.

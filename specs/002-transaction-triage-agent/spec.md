# Feature Specification: Transaction Triage Reasoning Agent

**Feature Branch**: `002-transaction-triage-agent`

**Created**: 2026-11-07

**Status**: Draft

**Input**: User description: "Build agent `agn-digiservcing-transactiontriage-v1` to analyse each
customer message, identify intent, merchant and amount, search mocked customer transactions, guide
triage, and return a mock case after customer confirmation. All code lives under `src/agent`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Find a Reported Transaction (Priority: P1)

As a customer, I can describe a transaction in natural language and receive the matching mock
transaction or useful alternatives to review.

**Why this priority**: Selecting the right transaction is required before the customer can begin
triage.

**Independent Test**: Analyse a message naming a supported merchant and amount, then verify that the
agent returns the matching mock transaction. Analyse a non-matching request and verify that exactly
three alternate transactions are returned as a hint.

**Acceptance Scenarios**:

1. **Given** a message such as “I don’t recognise $50 at Woolworths”, **When** the agent analyses
   it, **Then** it identifies a transaction-reporting intent, Woolworths as the merchant, and $50 as
   the amount.
2. **Given** a supported merchant and amount match a mock transaction, **When** the agent searches,
   **Then** it returns the matching transaction for customer selection.
3. **Given** a supported merchant or amount has no exact match, **When** the agent searches, **Then**
   it returns exactly three closest available transactions for the customer to review.
4. **Given** a message does not contain a supported merchant or usable amount, **When** the agent
   analyses it, **Then** it returns a customer-safe request for more transaction details.

---

### User Story 2 - Determine a Proposed Triage Outcome (Priority: P2)

As a customer, I can answer the required questions about my selected transaction and receive a clear
proposed outcome or merchant-refund guidance.

**Why this priority**: The triage decision is the primary customer value after a transaction is
selected.

**Independent Test**: Provide a selected transaction and each possible answer sequence, and verify
the required question order and resulting Fraud/scam, Dispute, or no-case merchant-refund guidance.

**Acceptance Scenarios**:

1. **Given** a customer selects a transaction, **When** the agent starts triage, **Then** it asks
   whether the merchant is known.
2. **Given** the merchant is unknown, **When** the customer answers the first question, **Then** the
   agent proposes Fraud/scam without asking another triage question.
3. **Given** the merchant is known and has not agreed to refund, **When** the customer says they made
   the purchase, **Then** the agent proposes Dispute after the third question.
4. **Given** the merchant is known and has agreed to refund, **When** the customer answers the second
   question, **Then** the agent gives merchant-refund guidance and does not propose a case.
5. **Given** the merchant is known, has not agreed to refund, and the customer did not make the
   purchase, **When** the customer answers the third question, **Then** the agent proposes Fraud/scam.

---

### User Story 3 - Confirm a Proposed Case (Priority: P3)

As a customer, I can review and explicitly confirm a proposed triage result before receiving a mock
case identifier and next steps.

**Why this priority**: Confirmation protects customers from an automatic or unintended submission.

**Independent Test**: Submit a confirmed proposed Fraud/scam or Dispute outcome and verify a mock
case identifier and supporting details; submit the same outcome without confirmation and verify that
no case identifier is returned.

**Acceptance Scenarios**:

1. **Given** the agent has proposed Fraud/scam or Dispute, **When** the customer has not confirmed
   it, **Then** the agent returns the proposal for preview without a case identifier.
2. **Given** the customer explicitly confirms a Fraud/scam or Dispute proposal, **When** the agent
   completes triage, **Then** it returns a local mock case identifier and supporting next-step details.
3. **Given** the merchant-refund outcome, **When** the customer reaches the outcome, **Then** the
   agent returns refund guidance without a case identifier.

### Edge Cases

- A message contains a named supported merchant but an amount in an unsupported format.
- A message contains multiple merchant names or multiple amounts.
- No mock transaction matches the extracted merchant and amount.
- A customer attempts to confirm before the agent has produced a triage proposal.
- A repeated confirmation must not produce duplicate mock case identifiers.
- Personal information appears in a customer message and must be masked before agent reasoning or
  logging.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The reasoning component MUST be named `agn-digiservcing-transactiontriage-v1`.
- **FR-002**: The agent MUST analyse every customer message and identify whether it is a
  transaction-reporting intent, an answer to an active triage question, a transaction selection, or
  a case-confirmation action.
- **FR-003**: For a transaction-reporting message, the agent MUST extract a merchant name and a
  monetary amount when they are present, including dollar amounts with or without cents.
- **FR-004**: The agent MUST support the baseline mock merchants Woolworths, Coles, Aldi, ZeroCoffee,
  and AlphaShop.
- **FR-005**: The agent MUST use a local JSON sample-data file containing 50 to 100 transactions for
  one mocked customer, including that customer's identifier.
- **FR-006**: The agent MUST return an exact transaction match when a supported merchant and amount
  match one mock transaction.
- **FR-007**: When no exact match exists, the agent MUST return exactly three alternatives, ranked by
  matching merchant first and then smallest monetary difference; if no merchant matches, it MUST rank
  all available transactions by smallest monetary difference.
- **FR-008**: The agent MUST ask no more than the constitution's three triage questions, in order:
  merchant known, merchant refund agreed when known, and customer made purchase when no refund is
  agreed.
- **FR-009**: The agent MUST propose Fraud/scam when the merchant is unknown or the customer did not
  make the purchase, and MUST propose Dispute when a known merchant did not agree to refund and the
  customer made the purchase.
- **FR-010**: The agent MUST return merchant-refund guidance and MUST NOT create a case when the
  merchant agreed to refund.
- **FR-011**: The agent MUST treat Fraud/scam and Dispute outcomes as immutable proposals until it
  receives explicit customer confirmation; it MUST return a local mock case identifier and supporting
  details only after confirmation.
- **FR-012**: The agent MUST mask personally identifiable information before reasoning, outputting,
  or logging customer content, and MUST attach a correlation identifier to each interaction.
- **FR-013**: The agent MUST provide a documented, inactive future extension point for language-model
  intent detection and transaction lookup tool calls; the current agent MUST continue to use only
  deterministic local matching and MUST NOT call any external AI service.
- **FR-014**: The agent implementation, sample data, automated tests, and future-extension
  documentation MUST live under `src/agent`.

### Key Entities *(include if feature involves data)*

- **Customer Message**: Incoming customer text, the derived intent, masked content, and correlation
  identifier.
- **Extracted Transaction Details**: The merchant and monetary amount detected in a customer message.
- **Mock Customer Transaction**: A local transaction record with the mock customer identifier,
  merchant, amount, and transaction reference.
- **Triage Session**: The selected transaction, answers to triage questions, and current proposed
  outcome.
- **Triage Proposal**: An immutable Fraud/scam or Dispute proposal awaiting explicit confirmation.
- **Mock Case**: A local-only case identifier and next-step details returned after confirmation.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of messages containing a baseline merchant and a valid dollar amount produce the
  expected extracted merchant and amount in automated verification.
- **SC-002**: 100% of exact-match searches return the matching mock transaction, while 100% of
  non-matching searches return exactly three alternatives.
- **SC-003**: 100% of automated decision-table scenarios produce the specified Fraud/scam, Dispute,
  or merchant-refund outcome with no more than three questions.
- **SC-004**: 100% of unconfirmed Fraud/scam and Dispute proposals return no case identifier, and
  100% of confirmed proposals return one local mock case identifier with next-step details.
- **SC-005**: Automated verification confirms that all interactions have a correlation identifier and
  that no unmasked personally identifiable information appears in agent outputs or logs.

## Assumptions

- The agent is a separate component consumed by the Python API specification and does not expose a
  customer-facing endpoint itself.
- The five named merchants are the initial baseline list; additional local merchants may be included
  in sample data without changing the required baseline behavior.
- When a message has multiple candidate amounts or merchants, the agent asks the customer to choose
  rather than guessing a transaction.
- Mock case identifiers are local-only and no real payment, banking, cloud, database, or external AI
  integration is in scope.

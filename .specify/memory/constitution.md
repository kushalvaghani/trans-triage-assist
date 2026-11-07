<!--
Sync Impact Report
- Version change: unversioned template → 1.0.0
- Modified principles: initial constitution replaces the unfilled scaffold
- Added sections: Core Principles, System Constraints, Delivery and Quality Workflow, Governance
- Removed sections: none
- Follow-up TODOs: none
-->

# Transaction Triage Assistant Constitution

## Core Principles

### I. Guided, Contained Chat Experience

**Rationale:** Customers need a simple path to report a transaction without the assistant
attempting unsupported banking services or leaving them uncertain about the next step.

**Rule:** The chat MUST greet a customer at the start of each session, support transaction-reporting
requests only, and respond to unrelated messages with a helpful redirection such as, “I am here to
help you with any issues with transactions.” Responses, transaction details, and confirmation MUST
be rendered in the chat; transaction and confirmation content MUST use chat cards. The UI MUST use
the Westpac logo, show the placeholder “Report $100 at ZeroCoffeeShop”, and provide a restart option
at every point in the session.

**How to Apply:** Build the React experience as a chat widget with explicit greeting, unsupported-
intent, searching, triage, preview, confirmation, completion, and restart states. Treat the cards as
part of the chat transcript rather than as a separate form or page.

### II. Deterministic Transaction Search and Triage

**Rationale:** A predictable local assistant is testable, auditable, and appropriate for a simulated
banking workflow.

**Rule:** The localized Python reasoning agent MUST use deterministic, local keyword and value-
matching functions; it MUST NOT call external LLMs. It MUST extract a known merchant and amount
from natural-language messages, including “I don’t recognise $50 spent at Woolworths.” It MUST
search mock transactions by merchant and amount, support mocked popular merchants including Coles
and Woolworths, and return a not-found result with hints about available transactions for merchants
outside the known scope. The triage sequence MUST ask no more than three questions: whether the
merchant is known; if known, whether the merchant agreed to refund; and, if no refund is agreed,
whether the customer made the purchase. An unknown merchant or a purchase the customer did not make
MUST produce a Fraud/scam proposal. A known merchant with no agreed refund and a customer-made
purchase MUST produce a Dispute proposal. If the merchant agreed to refund, the assistant MUST
direct the customer to contact the merchant and MUST NOT lodge a case.

**How to Apply:** Put intent parsing, transaction matching, and triage decisions in typed Python
functions with explicit inputs and outputs. Cover the three-question decision table and not-found
paths with tests; never hide decision logic in free-form prompts or remote services.

### III. Mock-Only and Component-Scoped Architecture

**Rationale:** The application is a safe demonstrator, not a connection to production banking
systems, and each layer needs a clear specification and contract.

**Rule:** The system MUST contain a React frontend, a Python API, and a localized Python reasoning
agent. Specifications MUST be generated separately for each component. The implementation MUST use
only static JSON data files and local mock utilities; it MUST NOT set up or configure live databases,
banking APIs, external cloud services, or external AI services. Mock data MUST include at least 50
customer transactions.

**How to Apply:** Keep mock transactions in version-controlled JSON inside a sample-data folder, expose them through the local
Python API, and route all frontend requests to that mock API. Produce component-level specifications
for the React UI, Python API, and reasoning agent before implementation begins.

### IV. Financial Safety and Customer Confirmation

**Rationale:** A misclassified or unintended transaction case can harm a customer; sensitive data
must not leak into responses or logs.

**Rule:** The Python API boundary MUST apply regex-based masking to PII before data enters agent
logic, responses, or logs. The agent’s final Fraud/scam or Dispute classification MUST be immutable
after it is proposed, but it MUST remain a proposal until the customer manually selects a confirm
button in the UI. A case ID and next-step details MUST be returned only after the customer previews
and confirms the selected transaction and proposed verdict. Failure paths MUST return a clear,
customer-safe chat message.

**How to Apply:** Define a preview payload that includes the selected transaction, masked details,
proposed case type, and next steps. The API must reject case creation without an explicit confirmation
signal, and the UI must never auto-submit or mutate the proposed verdict after it is shown.

### V. Quality, Traceability, and Maintainability

**Rationale:** The application must be dependable enough to demonstrate financial triage behavior
and straightforward enough for reviewers to trace a session across layers.

**Rule:** Python code MUST use strict type hints and comply with PEP 8 through Ruff. Frontend code
MUST comply with the project’s configured linting rules. Every session MUST have a correlation ID
carried through the React client, Python API, reasoning agent, and a session log file. Code comments
MUST explain non-obvious safety, triage, or masking decisions. Unused boilerplate and legacy mock-data
paths MUST be deleted, never retained as commented-out code.

**How to Apply:** Require linting and relevant automated tests before review. Log structured events
using the correlation ID without unmasked PII, and include the ID in safe failure diagnostics for
developers while keeping customer-facing failures understandable. Each session should have a log file with a correlation ID so its easier to trace across all the layers what was happening.

## System Constraints

- Case identifiers are local mock identifiers only and MUST NOT resemble real banking case records.
- The React UI, Python API, and local reasoning agent communicate only through documented local
  contracts.
- Any proposed integration with real customer, transaction, payment, cloud, or LLM data is outside
  scope and requires a constitutional amendment before implementation.
- A component may not bypass the API boundary to access mock data or agent logic directly.

## Delivery and Quality Workflow

1. Create component-scoped specifications for the React UI, Python API, and reasoning agent.
2. Define mock-data, API, and UI-state contracts before implementing dependent components.
3. Implement deterministic triage and API safety controls before wiring the confirmation experience.
4. Verify happy paths, all three triage outcomes, no-lodge refund guidance, unknown-merchant search,
   restart, PII masking, confirmation gating, correlation IDs, and customer-safe failures.
5. Run frontend linting, Ruff, type checks where configured, and relevant tests before review.

## Governance

This constitution supersedes conflicting project guidance. Every specification, plan, task list, code
review, and release check MUST verify compliance with its rules. Amendments require a written change
to this document, a rationale, an impact assessment for affected specifications and components, and a
semantic-version update: MAJOR for incompatible governance changes, MINOR for new or materially
expanded rules, and PATCH for clarifications. Compliance is reviewed during planning and before
implementation completion; unresolved violations block delivery.

**Version**: 1.0.0 | **Ratified**: 2026-11-07 | **Last Amended**: 2026-11-07

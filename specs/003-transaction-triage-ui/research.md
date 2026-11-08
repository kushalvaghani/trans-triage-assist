# Research: Transaction Triage Chat UI

## Decision: Use React, TypeScript, and Vite

**Rationale:** A small local Vite application provides a fast, independently runnable React widget
without adding server infrastructure.

**Alternatives considered:** A server-rendered UI adds an unneeded backend. A direct static HTML page
does not meet the React requirement.

## Decision: Keep all service calls in an API client adapter

**Rationale:** Components need to render chat state, not know endpoint details. One adapter sends the
correlation ID and maps customer-safe service responses into typed UI results.

**Alternatives considered:** Fetch calls inside cards would duplicate error handling and could let UI
code bypass the API boundary.

## Decision: Use append-only transcript entries and card variants

**Rationale:** An ordered transcript naturally preserves prior chat history, supports scrolling, and
lets transaction choices, questions, proposals, cases, and alternatives appear as cards in context.

**Alternatives considered:** Separate modal flows or a form wizard would violate the contained chat
experience.

## Decision: Maintain explicit confirmation state

**Rationale:** The confirmation card is enabled only when it represents the current proposal. Restart
invalidates pending work and a stale response cannot add a case to a new session.

**Alternatives considered:** Auto-submitting on classification conflicts with the constitution's
immutable-verdict rule.

## Decision: Treat API triage-session support as a dependency

**Rationale:** The current message/submission API does not expose a selected-transaction or
question-by-question session interaction contract. The UI can implement its state machine and adapter,
but integration requires the API to be wired to the agent or extended with compatible payloads.

**Alternatives considered:** Reading the global JSON fixture or importing the agent into the browser
would bypass the API and violate the constitution.

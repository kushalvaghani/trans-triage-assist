# Research: Transaction Triage API

## Decision: Use FastAPI with Pydantic v2

**Rationale**: FastAPI provides typed request validation, OpenAPI generation, and straightforward
local testing for the two fixed HTTP contracts. Pydantic v2 keeps boundary models explicit and
validates malformed input before it reaches triage logic.

**Alternatives considered**:

- Flask: viable, but requires more manual schema and OpenAPI work.
- A custom standard-library server: rejected because it adds avoidable validation and routing work.

## Decision: Keep the API deterministic and local

**Rationale**: The constitution prohibits external LLMs, live banking integrations, cloud services,
and databases. A local service can orchestrate deterministic matching and triage using static JSON
fixtures and local Python functions.

**Alternatives considered**:

- External LLM classification: rejected by the deterministic reasoning rule.
- External transaction provider: rejected by the mock-only rule.

## Decision: Generate a correlation ID at the API boundary

**Rationale**: Every request needs a traceable session identity across API, agent, UI, and local logs.
The API accepts a caller-supplied correlation ID when valid; otherwise it generates one and returns it
in every response.

**Alternatives considered**:

- Logging without a correlation ID: rejected because it cannot trace a customer journey.
- Using unmasked request bodies as log keys: rejected by the PII safety rule.

## Decision: Mask PII before service orchestration and logging

**Rationale**: Regex-based masking at the boundary ensures downstream deterministic reasoning,
responses, and log records do not receive raw email addresses, phone numbers, card-like strings, or
account-like number sequences.

**Alternatives considered**:

- Mask logs only: rejected because raw PII could still reach reasoning or response construction.
- Relying on callers to redact input: rejected because the API boundary owns the safety control.

## Decision: Enforce confirmation in the submission contract

**Rationale**: Fraud/scam and Dispute results are proposals. The API accepts a submission only when
the selected transaction and explicit confirmation are present, and only then returns a local mock
case identifier.

**Alternatives considered**:

- UI-only confirmation: rejected because direct endpoint callers could bypass it.
- Automatic case creation on a triage result: rejected by the immutable-verdict rule.

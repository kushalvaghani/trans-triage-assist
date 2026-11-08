# Research: Transaction Triage Reasoning Agent

## Decision: Use a typed, callable Python library contract

**Rationale:** The agent is consumed by the Python API and has no customer-facing transport. A
library method accepts an interaction and current session state, making its transitions directly
testable without HTTP or UI dependencies.

**Alternatives considered:** An internal HTTP endpoint would duplicate the API transport and weaken
the component boundary. A UI-owned state machine would violate the API-only access rule.

## Decision: Read global shared fixture through a repository adapter

**Rationale:** `sample_data/transactions.json` is shared by components. One read-only adapter gives
the agent deterministic validation, matching, and a single safe location to resolve the repository
root.

**Alternatives considered:** Copying transactions into `src/agent` would create divergent fixtures.
Adding a database conflicts with the mock-only constraint.

## Decision: Implement parsing and verdicts with standard-library heuristics

**Rationale:** Case-insensitive merchant matching, a dollar-amount regular expression, and explicit
intent/answer keywords are auditable and satisfy the no-external-LLM requirement.

**Alternatives considered:** OpenAI, Anthropic, or another remote model is prohibited. An inactive
typed extension interface will document future LLM intent/tool hooks without calling them.

## Decision: Carry immutable triage state in an explicit session model

**Rationale:** A session records the selected transaction, question position, answers, and proposal.
The engine can refuse early confirmation and preserve a proposal after it is made.

**Alternatives considered:** Recomputing state solely from each message risks reordered questions and
allows accidental case creation.

## Decision: Mask before agent parsing and retain only masked session events

**Rationale:** API masking remains required, but applying the same defensive boundary inside the
agent prevents accidental logging or output of raw PII when it is used independently in tests or a
future integration.

**Alternatives considered:** Trusting every caller to mask data is not sufficient for the financial
safety requirement.

# Decisions

## 1. Deterministic triage, not an external LLM

**Decision:** Use local keyword, amount, merchant, and yes/no parsing.  
**Trade-off:** Limited language coverage in return for reproducibility, safety, and zero external data
used. No LLM provider or prompt-based decisioning was built. Generated dummy transactions for 5 merchants.

## 2. Explicit confirmation is the case-creation gate

**Decision:** Require a manual confirmation after the proposal, then disable the button after success.
**Trade-off:** One extra customer action prevents accidental cases and duplicate local IDs. No
automatic submission was built.

## 3. Shared static fixtures and top-level local JSONL logs

**Decision:** Use `sample_data/transactions.json` and `logs/` for local traceability.
**Trade-off:** Simple and portable, but not durable, access-controlled, or appropriate for real
customer records. No database or cloud logging service was built.

## 4. UI speaks only to the API

**Decision:** Keep the UI behind the HTTP API boundary and prevent direct fixture/agent access.
**Trade-off:** Preserves component separation while the API invokes the deterministic agent for
message lookup and submission triage. A shared agent-session API contract remains future work.

## 5. Mock identity and case IDs

**Decision:** Emit mock `user_id: 599` and generate nine-character alphanumeric case IDs locally.
**Trade-off:** Supports demonstrable audit trails while avoiding real identity/case integration. The
uniqueness guarantee is process-local only; durable cross-instance idempotency was not built.

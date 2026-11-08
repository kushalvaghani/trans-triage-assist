# Transaction Agent Library Contract

## Component identity

`agn-digiservcing-transactiontriage-v1` is a local Python library invoked by the API. It exposes no
HTTP endpoint and performs no network calls.

## Callable interface

```text
process_interaction(interaction: AgentInteraction, session: TriageSession) -> AgentResult
```

The API supplies a correlation ID, customer input or explicit selection/confirmation action, and the
current session. The agent returns an updated session plus exactly one customer-safe result.

## Result kinds

| Kind | Required content | Case ID |
|---|---|---|
| `transaction_matches` | Exact match or three ranked alternatives | Never |
| `not_found` | Three ranked alternatives for an unavailable merchant | Never |
| `request_details` | Safe prompt for merchant or amount | Never |
| `triage_question` | Next ordered question and session state | Never |
| `proposal` | Immutable Fraud/scam or Dispute preview and next steps | Never |
| `merchant_refund_guidance` | Instruction to contact merchant | Never |
| `case_created` | Confirmed local mock case and next steps | Required |
| `error` | Safe message and correlation ID | Never |

## Invariants

- Every result contains the supplied correlation ID.
- Candidate search returns exactly three alternatives when no exact transaction exists.
- The agent ignores a confirmation before a proposal and returns a safe error.
- The agent masks PII in every string it returns or logs.
- `future_llm.py` defines only an interface and explanatory comments; no code invokes a remote model.

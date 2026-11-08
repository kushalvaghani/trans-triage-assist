# Transaction Triage UI API Contract

## Transport boundary

The React UI calls only the local Python API. It does not import the reasoning agent or read the
global transaction fixture.

## Existing paths

| UI action | Path | Required payload |
|---|---|---|
| Send customer message | `POST /exp-digiServicing-transctiontraige/v1/message` | `message`, `correlation_id` |
| Submit confirmed triage | `POST /exp-digiServicing-transctiontraige/v1/submission` | selected transaction, answers, `confirmed`, `correlation_id` |

## Required UI-facing response behaviors

- Every response includes `correlation_id` and customer-safe text.
- A transaction search result contains selectable transactions.
- A not-found result contains the exact required message and three alternative merchants.
- Triage interactions expose the active question, current session, and proposed outcome before a case
  can be submitted.
- A submitted case response contains the local case ID only after `confirmed: true`.

## Current integration gap

The existing API contract accepts a complete submission decision table rather than a transaction
selection and one answer at a time. Before final UI integration, update the API to use the agent's
`process_interaction` result or introduce equivalent API request/response fields. The UI must not
fill this gap by accessing internal API services, the agent, or `sample_data` directly.

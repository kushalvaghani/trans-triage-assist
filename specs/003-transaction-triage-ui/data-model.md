# Data Model: Transaction Triage Chat UI

## Chat Session

| Field | Type | Rule |
|---|---|---|
| `correlationId` | UUID | New for every restart; sent with all API calls |
| `entries` | `ChatEntry[]` | Append-only chronological transcript |
| `pendingProposal` | proposal/null | Enables confirmation only for the current proposal |
| `requestVersion` | number | Ignore responses from before a restart |

## Chat Entry

| Field | Type | Rule |
|---|---|---|
| `id` | string | Unique React list key |
| `role` | customer/assistant | Determines visual alignment |
| `content` | string | Customer-safe text |
| `card` | card/null | Structured transcript content |

## Chat Card Variants

| Variant | Content | Action rule |
|---|---|---|
| `transaction` | Mock transaction amount, merchant, date, description | Selection calls API adapter |
| `question` | Active triage question | Submit only a selected yes/no answer |
| `proposal` | Fraud/scam or Dispute plus next steps | Explicit confirm only |
| `merchantAlternatives` | Exactly three supplied merchants | Selecting one starts a new API search |
| `case` | Local mock case ID and next steps | Render only after confirmed service response |
| `error` | Customer-safe failure message | No automatic retry or submission |

## State transitions

```text
greeting → message submitted → transaction cards / redirection / not-found
transaction selected → triage question cards → proposal or refund guidance
proposal → explicit confirmation → case card
any state → restart → new greeting and correlation ID
```

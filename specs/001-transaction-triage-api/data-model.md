# Data Model: Transaction Triage API

## Customer Message

| Field | Type | Validation | Notes |
|---|---|---|---|
| `message` | string | Required, non-blank | Masked before downstream processing. |
| `correlation_id` | string | Optional UUID-form identifier | Generated when omitted; returned in every response. |

## Mock Transaction

| Field | Type | Validation | Notes |
|---|---|---|---|
| `transaction_id` | string | Required, unique | Local mock reference. |
| `customer_id` | string | Required | One mocked customer only. |
| `merchant` | string | Required | Used for deterministic matching. |
| `amount` | decimal string | Required, positive | Used for exact and closest matching. |
| `transaction_date` | ISO date | Required | Displayed in returned transaction details. |
| `description` | string | Required | Customer-safe mock description. |

The JSON fixture contains 50–100 records and no real customer data.

## Triage Submission

| Field | Type | Validation | Notes |
|---|---|---|---|
| `transaction_id` | string | Required, must exist in fixture | Selected transaction. |
| `merchant_known` | boolean | Required | First triage answer. |
| `merchant_refund_agreed` | boolean | Required only if merchant is known | Second triage answer. |
| `customer_made_purchase` | boolean | Required only if no refund was agreed | Third triage answer. |
| `confirmed` | boolean | Must be `true` to create a case | Customer confirmation gate. |
| `correlation_id` | string | Required or generated | Links request and logs. |

## Triage Outcome

| Field | Type | Notes |
|---|---|---|
| `outcome` | enum | `fraud_scam`, `dispute`, or `merchant_refund_guidance`. |
| `next_steps` | string array | Customer-safe actions. |
| `case_id` | string or null | Local mock ID only; present only after confirmed Fraud/scam or Dispute. |
| `correlation_id` | string | Present on all responses. |

## State Transitions

```text
message received
  → masked and classified
  → transaction choices or redirection
  → selected transaction
  → triage proposal or merchant-refund guidance
  → explicit confirmation
  → local mock case created
```

A Fraud/scam or Dispute proposal cannot transition to a created mock case unless `confirmed` is true.
Merchant-refund guidance is terminal and never creates a case.

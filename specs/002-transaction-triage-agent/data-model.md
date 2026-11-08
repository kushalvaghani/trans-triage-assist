# Data Model: Transaction Triage Reasoning Agent

## Shared Mock Transaction

Read-only record from `sample_data/transactions.json`.

| Field | Type | Rule |
|---|---|---|
| `transaction_id` | string | Unique fixture identifier |
| `customer_id` | string | Must be `mock-customer-001` in the current fixture |
| `merchant` | string | One of the baseline supported merchants |
| `amount` | decimal | Positive, two decimal places |
| `transaction_date` | date | ISO-8601 date |
| `description` | string | Customer-safe mock description |

## Agent Interaction

| Field | Type | Rule |
|---|---|---|
| `message` | string | Mask before parsing, output, or logging |
| `correlation_id` | UUID | Required for every interaction and event |
| `selected_transaction_id` | string/null | Must identify a fixture transaction before triage starts |
| `confirmed` | boolean | Can create a mock case only after a proposal exists |

## Triage Session

| Field | Type | Rule |
|---|---|---|
| `selected_transaction` | transaction/null | Set after explicit customer selection |
| `question` | enum/null | `merchant_known`, `merchant_refund_agreed`, or `customer_made_purchase` |
| `merchant_known` | boolean/null | First answer |
| `merchant_refund_agreed` | boolean/null | Required only when merchant is known |
| `customer_made_purchase` | boolean/null | Required only after no refund agreement |
| `proposal` | triage proposal/null | Immutable once set |

## Triage Proposal and Mock Case

| Field | Type | Rule |
|---|---|---|
| `outcome` | enum | `fraud_scam`, `dispute`, or `merchant_refund_guidance` |
| `next_steps` | list[string] | Customer-safe local instructions |
| `case_id` | string/null | Present only for confirmed Fraud/scam or Dispute outcomes |

### State transitions

```text
search → transaction selected → merchant known?
  unknown → Fraud/scam proposal → explicit confirmation → mock case
  known → refund agreed?
    yes → merchant-refund guidance → complete
    no → customer made purchase?
      no → Fraud/scam proposal → explicit confirmation → mock case
      yes → Dispute proposal → explicit confirmation → mock case
```

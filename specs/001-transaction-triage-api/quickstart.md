# Quickstart: Transaction Triage API Validation

## Prerequisites

- Python 3.12
- The project dependencies installed from the implementation's dependency manifest
- A local mock transaction fixture containing 50–100 records under `src/api/sample_data/`

## Run the Service

From the repository root, start the local API using the application's documented development command.
The service must expose the two paths in the [OpenAPI contract](contracts/transaction-triage-api.openapi.yaml).

## Validate Message Processing

Send a JSON POST request containing a transaction-reporting message to:

```text
/exp-digiServicing-transctiontraige/v1/message
```

Expected outcome:

- A successful, customer-safe response containing a correlation ID.
- A supported merchant and matching amount yield mock transaction choices.
- An unrelated message yields transaction-support redirection.
- A message containing PII yields no unmasked PII in the response or session log.

## Validate Triage Submission

Send a JSON POST request containing a selected mock transaction, triage answers, and `confirmed: true`
to:

```text
/exp-digiServicing-transctiontraige/v1/submission
```

Expected outcome:

- Unknown merchant or customer-did-not-make-purchase yields `fraud_scam` and a local mock case ID.
- Known merchant, no agreed refund, and customer-made purchase yields `dispute` and a local mock case
  ID.
- Agreed merchant refund yields `merchant_refund_guidance` without a case ID.
- `confirmed: false` is rejected without creating a case ID.

## Run Automated Checks

Run the implementation's pytest suite and Ruff checks. The suite must cover both endpoint contracts,
confirmation gating, the three triage outcomes, PII masking, correlation IDs, and masked session logs.

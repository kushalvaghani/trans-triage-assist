# Intent

## Problem and users

This exercise demonstates a simple workflow for a bank customer who wants to report a transaction against a merchant. The
customer searches for their transactions in natural language, answers at most three triage
questions, previews the proposed outcome, and explicitly confirms before receiving a case ID.
There is session evidence built in via logging.

## Assumptions and constraints

- The sole mocked customer has `user_id` 599 and at least 50 static transactions.
- The supported baseline merchants are Woolworths, Coles, Aldi, ZeroCoffee, and AlphaShop.
- The app is local-only: no real bank data, databases, cloud services, or external LLMs.
- Triage is deterministic: unknown merchant or customer-did-not-make-purchase proposes Fraud/scam;
  a known merchant with no agreed refund and customer-made purchase proposes Dispute; an agreed
  refund produces guidance without a case.
- A case ID is a nine-character local alphanumeric value, generated only after confirmation.

## Out of scope

Authentication, real customer identity, case-management integration, live
banking APIs, external AI/LLMs, case persistence, and production deployment.

## Success criteria

- Customers can complete the contained reporting journey and restart it at any point.
- No case is submitted without an explicit confirmation; a confirmed proposal cannot be submitted
  again from the same UI state.
- Logs carry the correlation ID, mock user ID, submitted answers, outcome, and generated case ID,
  without unmasked PII.
- API, agent, and UI checks pass locally.

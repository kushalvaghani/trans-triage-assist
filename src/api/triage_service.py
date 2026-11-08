"""Deterministic local transaction matching and triage decisions."""

from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from .models import MessageResponse, Outcome, ResponseType, SubmissionResponse, Transaction

DATA_PATH = Path(__file__).parents[2] / "sample_data" / "transactions.json"
MERCHANTS = ("Woolworths", "Coles", "Aldi", "ZeroCoffee", "AlphaShop")
REPORTING_KEYWORDS = ("report", "recognise", "recognize", "dispute", "fraud", "transaction")
AMOUNT_PATTERN = re.compile(r"(?:\$\s*(\d+(?:\.\d{1,2})?))|(?:(\d+(?:\.\d{1,2})?)\s*\$)")


class TransactionNotFoundError(ValueError):
    """Raised when a selected transaction does not exist in the local fixture."""


class ConfirmationRequiredError(ValueError):
    """Raised when a case-creating outcome lacks explicit customer confirmation."""


def load_transactions() -> list[Transaction]:
    """Load the version-controlled mock transaction fixture."""
    with DATA_PATH.open(encoding="utf-8") as data_file:
        return [Transaction.model_validate(item) for item in json.load(data_file)]


def _extract_merchant(message: str) -> str | None:
    lowered = message.lower()
    return next((merchant for merchant in MERCHANTS if merchant.lower() in lowered), None)


def _extract_amount(message: str) -> Decimal | None:
    match = AMOUNT_PATTERN.search(message)
    if not match:
        return None
    return Decimal(match.group(1) or match.group(2)).quantize(Decimal("0.01"))


def _closest_transactions(
    transactions: list[Transaction], merchant: str | None, amount: Decimal | None
) -> list[Transaction]:
    """Return three deterministic alternatives, preferring merchant then amount similarity."""
    comparison_amount = amount or Decimal("0")
    return sorted(
        transactions,
        key=lambda transaction: (
            merchant is None or transaction.merchant.lower() != merchant.lower(),
            abs(transaction.amount - comparison_amount),
            transaction.transaction_id,
        ),
    )[:3]


def process_message(message: str, correlation_id: UUID) -> MessageResponse:
    """Classify a masked message and return mock matches, alternatives, or safe redirection."""
    lowered = message.lower()
    merchant = _extract_merchant(message)
    amount = _extract_amount(message)
    has_reporting_intent = any(keyword in lowered for keyword in REPORTING_KEYWORDS)
    if not has_reporting_intent and (merchant is None or amount is None):
        return MessageResponse(
            correlation_id=correlation_id,
            response_type=ResponseType.REDIRECTION,
            message="I am here to help you with any issues with transactions.",
        )

    transactions = load_transactions()
    if merchant is not None and amount is not None:
        exact_matches = [
            transaction
            for transaction in transactions
            if transaction.merchant == merchant and transaction.amount == amount
        ]
        if exact_matches:
            return MessageResponse(
                correlation_id=correlation_id,
                response_type=ResponseType.TRANSACTION_MATCHES,
                message="We found a matching transaction for you to review.",
                transactions=exact_matches,
            )

    alternatives = _closest_transactions(transactions, merchant, amount)
    alternative_merchants = list(dict.fromkeys(item.merchant for item in alternatives))
    while len(alternative_merchants) < 3:
        alternative_merchants.append(MERCHANTS[len(alternative_merchants)])
    return MessageResponse(
        correlation_id=correlation_id,
        response_type=ResponseType.NOT_FOUND,
        message="Could not find the merchant, please search for other transactions.",
        transactions=alternatives,
        alternative_merchants=alternative_merchants[:3],
    )


def evaluate_submission(
    *,
    transaction_id: str,
    merchant_known: bool,
    merchant_refund_agreed: bool | None,
    customer_made_purchase: bool | None,
    confirmed: bool,
    correlation_id: UUID,
) -> SubmissionResponse:
    """Apply the constitution's fixed triage decision table to one selected transaction."""
    if not any(item.transaction_id == transaction_id for item in load_transactions()):
        raise TransactionNotFoundError("Selected transaction was not found.")

    if not merchant_known:
        outcome = Outcome.FRAUD_SCAM
        message = "We have proposed a Fraud/scam case based on the merchant being unknown."
        next_steps = ["Review the proposed Fraud/scam details.", "Confirm to create a case."]
    elif merchant_refund_agreed:
        return SubmissionResponse(
            correlation_id=correlation_id,
            outcome=Outcome.MERCHANT_REFUND_GUIDANCE,
            message="Please contact the merchant to complete the agreed refund.",
            next_steps=["Contact the merchant about the agreed refund."],
        )
    elif customer_made_purchase is False:
        outcome = Outcome.FRAUD_SCAM
        message = "We have proposed a Fraud/scam case because you did not make the purchase."
        next_steps = ["Review the proposed Fraud/scam details.", "Please get in touch if needed, and quote the case ID."]
    else:
        outcome = Outcome.DISPUTE
        message = "We have proposed a Dispute case for this transaction."
        next_steps = ["Review the proposed Dispute details.", "Please get in touch if needed, and quote the case ID."]

    if not confirmed:
        raise ConfirmationRequiredError(
            "Please confirm the proposed outcome before submitting a case."
        )

    return SubmissionResponse(
        correlation_id=correlation_id,
        outcome=outcome,
        message=message,
        next_steps=next_steps,
        case_id=f"{outcome.value.upper()}-{transaction_id.upper()}",
    )

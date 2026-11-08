"""Read-only access to the globally shared mock transaction fixture."""

from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from .models import Transaction

DATA_PATH = Path(__file__).parents[3] / "sample_data" / "transactions.json"


def load_transactions() -> list[Transaction]:
    """Load and validate the 50–100 record fixture for its one mocked customer."""
    with DATA_PATH.open(encoding="utf-8") as fixture:
        transactions = [Transaction.model_validate(item) for item in json.load(fixture)]
    if not 50 <= len(transactions) <= 100:
        raise ValueError("shared transaction fixture must contain 50 to 100 records")
    if len({item.transaction_id for item in transactions}) != len(transactions):
        raise ValueError("shared transaction fixture must have unique transaction IDs")
    if len({item.customer_id for item in transactions}) != 1:
        raise ValueError("shared transaction fixture must have one mocked customer")
    return transactions


def get_transaction(transaction_id: str) -> Transaction | None:
    """Return a selected fixture transaction if it exists."""
    return next(
        (item for item in load_transactions() if item.transaction_id == transaction_id), None
    )


def find_transactions(
    merchant: str, amount: Decimal
) -> tuple[list[Transaction], list[Transaction]]:
    """Find an exact match or three merchant-first, amount-nearest alternatives."""
    transactions = load_transactions()
    matches = [item for item in transactions if item.merchant == merchant and item.amount == amount]
    if matches:
        return matches, []
    alternatives = sorted(
        transactions,
        key=lambda item: (
            item.merchant.lower() != merchant.lower(),
            abs(item.amount - amount),
            item.transaction_id,
        ),
    )[:3]
    return [], alternatives

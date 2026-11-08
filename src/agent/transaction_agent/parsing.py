"""Local deterministic parsing for intent, merchants, amounts, and answers."""

from __future__ import annotations

import re
from decimal import Decimal

MERCHANTS = ("Woolworths", "Coles", "Aldi", "ZeroCoffee", "AlphaShop")
REPORTING_KEYWORDS = ("report", "recognise", "recognize", "dispute", "fraud", "transaction")
AMOUNT_PATTERN = re.compile(r"(?:\$\s*(\d+(?:\.\d{1,2})?))|(?:(\d+(?:\.\d{1,2})?)\s*\$)")
YES_PATTERN = re.compile(r"\b(?:yes|yeah|yep|correct|affirmative)\b", re.IGNORECASE)
NO_PATTERN = re.compile(r"\b(?:no|nope|nah)\b", re.IGNORECASE)


def extract_merchants(message: str) -> list[str]:
    """Return named baseline merchants in their order of appearance."""
    lowered = message.lower()
    return sorted(
        (merchant for merchant in MERCHANTS if merchant.lower() in lowered),
        key=lambda merchant: lowered.index(merchant.lower()),
    )


def extract_amounts(message: str) -> list[Decimal]:
    """Extract valid dollar values from a masked customer message."""
    return [
        Decimal(match.group(1) or match.group(2)).quantize(Decimal("0.01"))
        for match in AMOUNT_PATTERN.finditer(message)
    ]


def is_reporting_intent(message: str) -> bool:
    """Identify transaction reporting without an external language model."""
    lowered = message.lower()
    return any(keyword in lowered for keyword in REPORTING_KEYWORDS)


def parse_yes_no(message: str) -> bool | None:
    """Map an explicit customer response to a boolean without guessing."""
    if YES_PATTERN.search(message):
        return True
    if NO_PATTERN.search(message):
        return False
    return None

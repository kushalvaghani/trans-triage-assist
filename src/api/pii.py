"""Regex-based PII masking performed before triage or logging."""

from __future__ import annotations

import re

MASK = "[REDACTED]"

_EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
_PHONE = re.compile(r"\b(?:\+?61|0)4\d{8}\b")
_CARD = re.compile(r"\b(?:\d[ -]*?){13,16}\b")
_ACCOUNT = re.compile(r"\b\d{6,12}\b")


def mask_pii(value: str) -> str:
    """Mask common PII patterns while retaining transaction-search context."""
    masked = _EMAIL.sub(MASK, value)
    masked = _PHONE.sub(MASK, masked)
    masked = _CARD.sub(MASK, masked)
    return _ACCOUNT.sub(MASK, masked)

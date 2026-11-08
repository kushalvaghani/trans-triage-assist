"""Tests for deterministic message parsing."""

from decimal import Decimal

from transaction_agent.parsing import extract_amounts, extract_merchants, parse_yes_no


def test_extracts_baseline_merchant_and_amount_with_cents() -> None:
    assert extract_merchants("I don't recognise $50.00 at Woolworths") == ["Woolworths"]
    assert extract_amounts("I don't recognise $50.00 at Woolworths") == [Decimal("50.00")]


def test_extracts_amount_without_cents_and_multiple_candidates() -> None:
    assert extract_amounts("Report $50 at Coles and $90.01 at Aldi") == [
        Decimal("50.00"),
        Decimal("90.01"),
    ]
    assert extract_merchants("Report $50 at Coles and $90.01 at Aldi") == ["Coles", "Aldi"]


def test_rejects_unsupported_amount_and_recognises_answers() -> None:
    assert extract_amounts("Report fifty dollars at Woolworths") == []
    assert parse_yes_no("Yes, I know them") is True
    assert parse_yes_no("No") is False
    assert parse_yes_no("maybe") is None

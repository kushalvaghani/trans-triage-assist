"""Tests for shared fixture validation and deterministic search."""

from decimal import Decimal

from transaction_agent.repository import find_transactions, load_transactions


def test_shared_fixture_contains_one_customer_and_fifty_transactions() -> None:
    transactions = load_transactions()

    assert len(transactions) == 50
    assert {item.customer_id for item in transactions} == {"mock-customer-001"}


def test_finds_an_exact_shared_transaction() -> None:
    matches, alternatives = find_transactions("Woolworths", Decimal("50.00"))

    assert [item.transaction_id for item in matches] == ["txn-001"]
    assert alternatives == []


def test_returns_three_merchant_first_alternatives() -> None:
    matches, alternatives = find_transactions("Woolworths", Decimal("51.00"))

    assert matches == []
    assert len(alternatives) == 3
    assert {item.merchant for item in alternatives} == {"Woolworths"}

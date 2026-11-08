"""Tests for customer reporting-message processing."""

from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, ResultKind, TriageSession


def test_returns_exact_transaction_match_for_reporting_message() -> None:
    result = process_interaction(
        AgentInteraction(message="I don't recognise $50 at Woolworths"), TriageSession()
    )

    assert result.kind is ResultKind.TRANSACTION_MATCHES
    assert result.transactions[0].transaction_id == "txn-001"


def test_requests_details_when_no_supported_transaction_details_exist() -> None:
    result = process_interaction(AgentInteraction(message="I need help"), TriageSession())

    assert result.kind is ResultKind.REQUEST_DETAILS
    assert "merchant" in result.message.lower()


def test_returns_alternatives_for_an_unmatched_merchant() -> None:
    result = process_interaction(
        AgentInteraction(message="Report $99 at UnknownMart"), TriageSession()
    )

    assert result.kind is ResultKind.NOT_FOUND
    assert len(result.transactions) == 3

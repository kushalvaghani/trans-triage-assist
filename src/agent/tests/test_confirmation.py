"""Tests for the immutable proposal and confirmation gate."""

from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, ResultKind, TriageSession


def fraud_proposal_session() -> TriageSession:
    selected = process_interaction(
        AgentInteraction(selected_transaction_id="txn-001"), TriageSession()
    )
    return process_interaction(AgentInteraction(message="no"), selected.session).session


def test_confirmation_before_proposal_is_rejected() -> None:
    result = process_interaction(AgentInteraction(confirmed=True), TriageSession())

    assert result.kind is ResultKind.ERROR
    assert result.case_id is None


def test_confirmed_proposal_returns_a_stable_mock_case() -> None:
    session = fraud_proposal_session()
    first = process_interaction(AgentInteraction(confirmed=True), session)
    second = process_interaction(AgentInteraction(confirmed=True), first.session)

    assert first.kind is ResultKind.CASE_CREATED
    assert first.case_id == "MOCK-FRAUD_SCAM-TXN-001"
    assert second.case_id == first.case_id

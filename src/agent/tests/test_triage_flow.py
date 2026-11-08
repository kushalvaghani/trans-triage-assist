"""Decision-table tests for the ordered triage questions."""

from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, Outcome, Question, ResultKind, TriageSession


def select_transaction() -> TriageSession:
    return process_interaction(
        AgentInteraction(selected_transaction_id="txn-001"), TriageSession()
    ).session


def test_unknown_merchant_proposes_fraud_after_first_question() -> None:
    result = process_interaction(AgentInteraction(message="no"), select_transaction())

    assert result.kind is ResultKind.PROPOSAL
    assert result.proposal.outcome is Outcome.FRAUD_SCAM


def test_known_merchant_with_agreed_refund_returns_guidance() -> None:
    known = process_interaction(AgentInteraction(message="yes"), select_transaction())
    result = process_interaction(AgentInteraction(message="yes"), known.session)

    assert result.kind is ResultKind.MERCHANT_REFUND_GUIDANCE
    assert result.proposal.outcome is Outcome.MERCHANT_REFUND_GUIDANCE


def test_known_merchant_no_refund_and_made_purchase_proposes_dispute() -> None:
    known = process_interaction(AgentInteraction(message="yes"), select_transaction())
    no_refund = process_interaction(AgentInteraction(message="no"), known.session)
    result = process_interaction(AgentInteraction(message="yes"), no_refund.session)

    assert no_refund.question is Question.CUSTOMER_MADE_PURCHASE
    assert result.proposal.outcome is Outcome.DISPUTE


def test_known_merchant_no_refund_and_no_purchase_proposes_fraud() -> None:
    known = process_interaction(AgentInteraction(message="yes"), select_transaction())
    no_refund = process_interaction(AgentInteraction(message="no"), known.session)
    result = process_interaction(AgentInteraction(message="no"), no_refund.session)

    assert result.proposal.outcome is Outcome.FRAUD_SCAM

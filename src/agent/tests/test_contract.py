"""Tests for the documented library contract."""

from pathlib import Path

from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, TriageSession


def test_documented_callable_contract_returns_a_customer_safe_result() -> None:
    contract = (
        Path(__file__).parents[3]
        / "specs/002-transaction-triage-agent/contracts/transaction-agent.md"
    )
    result = process_interaction(
        AgentInteraction(message="Report $50 at Woolworths"), TriageSession()
    )

    assert "process_interaction" in contract.read_text(encoding="utf-8")
    assert result.correlation_id
    assert result.session is not None

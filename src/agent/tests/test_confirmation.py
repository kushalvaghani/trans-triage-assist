"""Tests for the immutable proposal and confirmation gate."""

import re
from pathlib import Path
from uuid import uuid4

from transaction_agent import logging_service
from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, ResultKind, TriageSession

CASE_ID_PATTERN = re.compile(r"^[A-Z0-9]{9}$")


def fraud_proposal_session() -> TriageSession:
    selected = process_interaction(
        AgentInteraction(selected_transaction_id="txn-001"), TriageSession()
    )
    return process_interaction(AgentInteraction(message="no"), selected.session).session


def test_confirmation_before_proposal_is_rejected() -> None:
    result = process_interaction(AgentInteraction(confirmed=True), TriageSession())

    assert result.kind is ResultKind.ERROR
    assert result.case_id is None


def test_confirmed_proposal_returns_a_stable_alphanumeric_case_id(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setattr(logging_service, "LOG_DIRECTORY", tmp_path)
    session = fraud_proposal_session()
    correlation_id = uuid4()
    first = process_interaction(
        AgentInteraction(confirmed=True, correlation_id=correlation_id), session
    )
    second = process_interaction(AgentInteraction(confirmed=True), first.session)

    assert first.kind is ResultKind.CASE_CREATED
    assert CASE_ID_PATTERN.fullmatch(first.case_id or "")
    assert second.case_id == first.case_id
    assert first.proposal is not None
    assert "Confirm to create a case." not in first.proposal.next_steps
    assert first.case_id in (tmp_path / f"{correlation_id}.jsonl").read_text(encoding="utf-8")

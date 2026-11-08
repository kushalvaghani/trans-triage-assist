"""Tests for agent-local masking and correlation-aware logs."""

from pathlib import Path
from uuid import uuid4

from transaction_agent import logging_service
from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, TriageSession


def test_masks_pii_before_returning_or_logging(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(logging_service, "LOG_DIRECTORY", tmp_path)
    correlation_id = uuid4()
    email = "customer@example.com"

    result = process_interaction(
        AgentInteraction(
            message=f"Report $50 at Woolworths for {email}", correlation_id=correlation_id
        ),
        TriageSession(),
    )

    content = (tmp_path / f"{correlation_id}.jsonl").read_text(encoding="utf-8")
    assert result.correlation_id == correlation_id
    assert email not in content
    assert "[REDACTED]" in content
    assert '"user_id": 599' in content

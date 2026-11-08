"""Tests for masked, correlation-aware local session logging."""

import json
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from api import logging_service
from api.app import app

MESSAGE_PATH = "/exp-digiServicing-transctiontraige/v1/message"


def test_message_log_uses_correlation_id_and_masks_pii(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(logging_service, "LOG_DIRECTORY", tmp_path)
    correlation_id = uuid4()
    raw_email = "customer@example.com"

    response = TestClient(app).post(
        MESSAGE_PATH,
        json={
            "message": f"Report $50 at Woolworths for {raw_email}",
            "correlation_id": str(correlation_id),
        },
    )

    assert response.status_code == 200
    log_file = tmp_path / f"{correlation_id}.jsonl"
    assert log_file.exists()
    events = [json.loads(line) for line in log_file.read_text(encoding="utf-8").splitlines()]
    assert raw_email not in log_file.read_text(encoding="utf-8")
    assert "[REDACTED]" in log_file.read_text(encoding="utf-8")
    assert all(event["user_id"] == 599 for event in events)


def test_submission_log_records_triage_answers(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(logging_service, "LOG_DIRECTORY", tmp_path)
    correlation_id = uuid4()

    response = TestClient(app).post(
        "/exp-digiServicing-transctiontraige/v1/submission",
        json={
            "transaction_id": "txn-001",
            "merchant_known": True,
            "merchant_refund_agreed": False,
            "customer_made_purchase": True,
            "confirmed": True,
            "correlation_id": str(correlation_id),
        },
    )

    assert response.status_code == 200
    events = [
        json.loads(line)
        for line in (tmp_path / f"{correlation_id}.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert events[0]["triage_answers"] == {
        "merchant_known": True,
        "merchant_refund_agreed": False,
        "customer_made_purchase": True,
    }
    assert events[0]["confirmed"] is True
    assert events[1]["case_id"] == response.json()["case_id"]
    assert all(event["user_id"] == 599 for event in events)

"""Contract and decision-table tests for triage submission."""

import re

from fastapi.testclient import TestClient

from api import triage_service
from api.app import app

client = TestClient(app)
SUBMISSION_PATH = "/exp-digiServicing-transctiontraige/v1/submission"
CASE_ID_PATTERN = re.compile(r"^[A-Z0-9]{9}$")


def submit(**overrides: object):
    payload: dict[str, object] = {
        "transaction_id": "txn-001",
        "merchant_known": True,
        "merchant_refund_agreed": False,
        "customer_made_purchase": True,
        "confirmed": True,
    }
    payload.update(overrides)
    return client.post(SUBMISSION_PATH, json=payload)


def test_submission_returns_dispute_case_after_confirmation() -> None:
    response = submit()

    assert response.status_code == 200
    body = response.json()
    assert body["outcome"] == "dispute"
    assert CASE_ID_PATTERN.fullmatch(body["case_id"])


def test_submission_reconstructs_triage_with_the_agent(monkeypatch) -> None:
    calls = []
    original = triage_service.process_interaction

    def tracked_process_interaction(*args, **kwargs):
        calls.append(args[0])
        return original(*args, **kwargs)

    monkeypatch.setattr(triage_service, "process_interaction", tracked_process_interaction)

    response = submit()

    assert response.status_code == 200
    assert calls[0].selected_transaction_id == "txn-001"
    assert calls[-1].confirmed is True


def test_unknown_merchant_returns_fraud_case() -> None:
    response = submit(
        merchant_known=False,
        merchant_refund_agreed=None,
        customer_made_purchase=None,
    )

    assert response.status_code == 200
    assert response.json()["outcome"] == "fraud_scam"
    assert CASE_ID_PATTERN.fullmatch(response.json()["case_id"])


def test_customer_did_not_make_purchase_returns_fraud_case() -> None:
    response = submit(customer_made_purchase=False)

    assert response.status_code == 200
    assert response.json()["outcome"] == "fraud_scam"


def test_agreed_refund_returns_guidance_without_case() -> None:
    response = submit(merchant_refund_agreed=True, customer_made_purchase=None)

    assert response.status_code == 200
    assert response.json()["outcome"] == "merchant_refund_guidance"
    assert response.json()["case_id"] is None


def test_unconfirmed_submission_creates_no_case() -> None:
    response = submit(confirmed=False)

    assert response.status_code == 400
    assert "case_id" not in response.json()


def test_repeated_confirmed_submissions_receive_unique_case_ids() -> None:
    first_response = submit()
    second_response = submit()

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert first_response.json()["case_id"] != second_response.json()["case_id"]


def test_missing_follow_up_answer_is_rejected() -> None:
    response = submit(customer_made_purchase=None)

    assert response.status_code == 422
    assert "correlation_id" in response.json()


def test_unknown_transaction_is_not_found() -> None:
    response = submit(transaction_id="missing-transaction")

    assert response.status_code == 404
    assert "Selected transaction" in response.json()["message"]

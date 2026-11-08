"""Contract and integration tests for customer-message processing."""

from uuid import UUID

from fastapi.testclient import TestClient

from api.app import app

client = TestClient(app)
MESSAGE_PATH = "/exp-digiServicing-transctiontraige/v1/message"


def test_message_endpoint_returns_exact_mock_transaction() -> None:
    response = client.post(MESSAGE_PATH, json={"message": "I don't recognise $50 at Woolworths"})

    assert response.status_code == 200
    body = response.json()
    UUID(body["correlation_id"])
    assert body["response_type"] == "transaction_matches"
    assert body["transactions"][0]["transaction_id"] == "txn-001"


def test_message_endpoint_accepts_a_merchant_and_amount_without_report_keyword() -> None:
    response = client.post(MESSAGE_PATH, json={"message": "$50 at Woolworths"})

    assert response.status_code == 200
    assert response.json()["response_type"] == "transaction_matches"


def test_message_endpoint_returns_closest_alternatives_when_not_found() -> None:
    response = client.post(MESSAGE_PATH, json={"message": "Report $99 at UnknownMart"})

    assert response.status_code == 200
    body = response.json()
    assert body["response_type"] == "not_found"
    assert len(body["transactions"]) == 3
    assert len(body["alternative_merchants"]) == 3


def test_message_endpoint_redirects_unrelated_messages() -> None:
    response = client.post(MESSAGE_PATH, json={"message": "What is the weather today?"})

    assert response.status_code == 200
    assert response.json()["response_type"] == "redirection"
    assert "transactions" in response.json()["message"]


def test_message_endpoint_returns_safe_error_for_blank_message() -> None:
    response = client.post(MESSAGE_PATH, json={"message": "   "})

    assert response.status_code == 422
    body = response.json()
    UUID(body["correlation_id"])
    assert "Please check the details" in body["message"]

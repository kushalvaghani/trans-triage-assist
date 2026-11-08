"""Typed models for the local transaction triage API."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field, field_validator, model_validator


class ResponseType(StrEnum):
    """Kinds of customer-safe message responses."""

    TRANSACTION_MATCHES = "transaction_matches"
    TRIAGE_QUESTION = "triage_question"
    REDIRECTION = "redirection"
    NOT_FOUND = "not_found"
    ERROR = "error"


class Outcome(StrEnum):
    """Allowed immutable triage outcomes."""

    FRAUD_SCAM = "fraud_scam"
    DISPUTE = "dispute"
    MERCHANT_REFUND_GUIDANCE = "merchant_refund_guidance"


class Transaction(BaseModel):
    """A fictional transaction belonging to the one mocked customer."""

    transaction_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    merchant: str = Field(min_length=1)
    amount: Decimal = Field(gt=Decimal("0"), max_digits=10, decimal_places=2)
    transaction_date: date
    description: str = Field(min_length=1)


class MessageRequest(BaseModel):
    """Payload accepted by the customer-message endpoint."""

    message: str = Field(min_length=1)
    correlation_id: UUID | None = None

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        """Reject whitespace-only customer messages."""
        if not value.strip():
            raise ValueError("message must not be blank")
        return value


class MessageResponse(BaseModel):
    """Response returned after processing a customer message."""

    correlation_id: UUID
    message: str
    response_type: ResponseType
    transactions: list[Transaction] = Field(default_factory=list)
    alternative_merchants: list[str] = Field(default_factory=list, max_length=3)


class SubmissionRequest(BaseModel):
    """A selected transaction and answers needed for deterministic triage."""

    transaction_id: str = Field(min_length=1)
    merchant_known: bool
    merchant_refund_agreed: bool | None = None
    customer_made_purchase: bool | None = None
    confirmed: bool
    correlation_id: UUID | None = None

    @model_validator(mode="after")
    def validate_triage_answers(self) -> SubmissionRequest:
        """Require only the follow-up answers that apply to the selected path."""
        if self.merchant_known and self.merchant_refund_agreed is None:
            raise ValueError("merchant_refund_agreed is required when merchant_known is true")
        if (
            self.merchant_known
            and self.merchant_refund_agreed is False
            and self.customer_made_purchase is None
        ):
            raise ValueError(
                "customer_made_purchase is required when no merchant refund was agreed"
            )
        return self


class SubmissionResponse(BaseModel):
    """Customer-safe result of a confirmed triage submission."""

    correlation_id: UUID
    outcome: Outcome
    message: str
    next_steps: list[str]
    case_id: str | None = None


class ErrorResponse(BaseModel):
    """Safe error response shared by all failure paths."""

    correlation_id: UUID
    message: str

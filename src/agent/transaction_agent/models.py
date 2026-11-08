"""Typed contracts for the deterministic transaction-triage agent."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class ResultKind(StrEnum):
    """Customer-safe results emitted by the agent."""

    TRANSACTION_MATCHES = "transaction_matches"
    REQUEST_DETAILS = "request_details"
    TRIAGE_QUESTION = "triage_question"
    PROPOSAL = "proposal"
    MERCHANT_REFUND_GUIDANCE = "merchant_refund_guidance"
    CASE_CREATED = "case_created"
    ERROR = "error"


class Outcome(StrEnum):
    """Deterministic triage outcomes."""

    FRAUD_SCAM = "fraud_scam"
    DISPUTE = "dispute"
    MERCHANT_REFUND_GUIDANCE = "merchant_refund_guidance"


class Question(StrEnum):
    """Ordered questions used to determine a triage outcome."""

    MERCHANT_KNOWN = "merchant_known"
    MERCHANT_REFUND_AGREED = "merchant_refund_agreed"
    CUSTOMER_MADE_PURCHASE = "customer_made_purchase"


class Transaction(BaseModel):
    """One fictional transaction from the globally shared fixture."""

    transaction_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    merchant: str = Field(min_length=1)
    amount: Decimal = Field(gt=Decimal("0"), max_digits=10, decimal_places=2)
    transaction_date: date
    description: str = Field(min_length=1)


class AgentInteraction(BaseModel):
    """One API-provided message, selection, or confirmation action."""

    message: str | None = None
    selected_transaction_id: str | None = None
    confirmed: bool = False
    correlation_id: UUID = Field(default_factory=uuid4)

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str | None) -> str | None:
        """Reject messages that would not be actionable after trimming."""
        if value is not None and not value.strip():
            raise ValueError("message must not be blank")
        return value


class TriageProposal(BaseModel):
    """An immutable proposed outcome that awaits customer confirmation."""

    model_config = {"frozen": True}

    outcome: Outcome
    message: str
    next_steps: list[str]


class TriageSession(BaseModel):
    """The caller-owned state for a single triage conversation."""

    selected_transaction: Transaction | None = None
    question: Question | None = None
    merchant_known: bool | None = None
    merchant_refund_agreed: bool | None = None
    customer_made_purchase: bool | None = None
    proposal: TriageProposal | None = None
    case_id: str | None = None


class AgentResult(BaseModel):
    """A single customer-safe result plus its next session state."""

    correlation_id: UUID
    kind: ResultKind
    message: str
    session: TriageSession
    transactions: list[Transaction] = Field(default_factory=list)
    question: Question | None = None
    proposal: TriageProposal | None = None
    case_id: str | None = None

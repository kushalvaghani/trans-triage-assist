"""Adapter that exposes the deterministic agent through the local HTTP API."""

from __future__ import annotations

from uuid import UUID

from transaction_agent.engine import process_interaction
from transaction_agent.models import AgentInteraction, ResultKind, TriageSession
from transaction_agent.models import Transaction as AgentTransaction
from transaction_agent.parsing import MERCHANTS

from .models import MessageResponse, Outcome, ResponseType, SubmissionResponse, Transaction


class TransactionNotFoundError(ValueError):
    """Raised when a selected transaction does not exist in the local fixture."""


class ConfirmationRequiredError(ValueError):
    """Raised when a case-creating outcome lacks explicit customer confirmation."""


def _transactions(result_transactions: list[AgentTransaction]) -> list[Transaction]:
    """Convert the agent's transaction models into the API response contract."""
    return [
        Transaction.model_validate(transaction.model_dump()) for transaction in result_transactions
    ]


def _alternative_merchants(transactions: list[Transaction]) -> list[str]:
    """Supply exactly three customer-visible alternatives from agent search results."""
    merchants = list(dict.fromkeys(transaction.merchant for transaction in transactions))
    for merchant in MERCHANTS:
        if merchant not in merchants:
            merchants.append(merchant)
        if len(merchants) == 3:
            break
    return merchants


def _answer(value: bool) -> str:
    """Use the agent's public yes/no interaction contract for a boolean API answer."""
    return "yes" if value else "no"


def process_message(message: str, correlation_id: UUID) -> MessageResponse:
    """Delegate message classification and transaction lookup to the agent."""
    result = process_interaction(
        AgentInteraction(message=message, correlation_id=correlation_id), TriageSession()
    )
    transactions = _transactions(result.transactions)

    if result.kind is ResultKind.TRANSACTION_MATCHES:
        return MessageResponse(
            correlation_id=correlation_id,
            response_type=ResponseType.TRANSACTION_MATCHES,
            message=result.message,
            transactions=transactions,
        )
    if result.kind is ResultKind.NOT_FOUND:
        return MessageResponse(
            correlation_id=correlation_id,
            response_type=ResponseType.NOT_FOUND,
            message=result.message,
            transactions=transactions,
            alternative_merchants=_alternative_merchants(transactions),
        )
    if result.kind is ResultKind.REQUEST_DETAILS:
        return MessageResponse(
            correlation_id=correlation_id,
            response_type=ResponseType.REDIRECTION,
            message="I am here to help you with any issues with transactions.",
        )
    return MessageResponse(
        correlation_id=correlation_id,
        response_type=ResponseType.ERROR,
        message="We could not process that request. Please try again.",
    )


def evaluate_submission(
    *,
    transaction_id: str,
    merchant_known: bool,
    merchant_refund_agreed: bool | None,
    customer_made_purchase: bool | None,
    confirmed: bool,
    correlation_id: UUID,
) -> SubmissionResponse:
    """Reconstruct the submitted triage path through the agent and map its final result."""
    result = process_interaction(
        AgentInteraction(selected_transaction_id=transaction_id, correlation_id=correlation_id),
        TriageSession(),
    )
    if result.kind is ResultKind.ERROR:
        raise TransactionNotFoundError("Selected transaction was not found.")

    result = process_interaction(
        AgentInteraction(message=_answer(merchant_known), correlation_id=correlation_id),
        result.session,
    )
    if merchant_known:
        result = process_interaction(
            AgentInteraction(
                message=_answer(merchant_refund_agreed is True), correlation_id=correlation_id
            ),
            result.session,
        )
        if merchant_refund_agreed is False:
            result = process_interaction(
                AgentInteraction(
                    message=_answer(customer_made_purchase is True), correlation_id=correlation_id
                ),
                result.session,
            )

    if result.kind is ResultKind.MERCHANT_REFUND_GUIDANCE:
        return SubmissionResponse(
            correlation_id=correlation_id,
            outcome=Outcome.MERCHANT_REFUND_GUIDANCE,
            message=result.message,
            next_steps=result.proposal.next_steps if result.proposal else [],
        )
    if result.kind is not ResultKind.PROPOSAL or result.proposal is None:
        raise TransactionNotFoundError("Selected transaction could not be triaged.")
    if not confirmed:
        raise ConfirmationRequiredError(
            "Please confirm the proposed outcome before submitting a case."
        )

    confirmed_result = process_interaction(
        AgentInteraction(confirmed=True, correlation_id=correlation_id), result.session
    )
    if confirmed_result.kind is not ResultKind.CASE_CREATED or confirmed_result.proposal is None:
        raise ConfirmationRequiredError("We could not create that case. Please try again.")
    return SubmissionResponse(
        correlation_id=correlation_id,
        outcome=Outcome(confirmed_result.proposal.outcome.value),
        message=confirmed_result.message,
        next_steps=confirmed_result.proposal.next_steps,
        case_id=confirmed_result.case_id,
    )

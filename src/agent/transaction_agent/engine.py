"""Deterministic message orchestration and triage state transitions."""

from __future__ import annotations

from secrets import choice
from string import ascii_uppercase, digits

from .logging_service import log_event
from .models import (
    AgentInteraction,
    AgentResult,
    Outcome,
    Question,
    ResultKind,
    TriageProposal,
    TriageSession,
)
from .parsing import extract_amounts, extract_merchants, is_reporting_intent, parse_yes_no
from .pii import mask_pii
from .repository import find_transactions, get_transaction

QUESTION_MESSAGES = {
    Question.MERCHANT_KNOWN: "Is the merchant known to you?",
    Question.MERCHANT_REFUND_AGREED: "Did you contact the merchant and did they agree to refund?",
    Question.CUSTOMER_MADE_PURCHASE: "Did you make the purchase?",
}
CASE_ID_ALPHABET = ascii_uppercase + digits
ISSUED_CASE_IDS: set[str] = set()


def _new_case_id() -> str:
    """Generate a unique nine-character alphanumeric identifier for this agent process."""
    while True:
        case_id = "".join(choice(CASE_ID_ALPHABET) for _ in range(9))
        if case_id not in ISSUED_CASE_IDS:
            ISSUED_CASE_IDS.add(case_id)
            return case_id


def _result(
    interaction: AgentInteraction,
    kind: ResultKind,
    message: str,
    session: TriageSession,
    **details: object,
) -> AgentResult:
    result = AgentResult(
        correlation_id=interaction.correlation_id,
        kind=kind,
        message=message,
        session=session,
        **details,
    )
    log_event(interaction.correlation_id, "agent_result", kind=kind.value)
    return result


def _ask_question(
    interaction: AgentInteraction, session: TriageSession, question: Question
) -> AgentResult:
    next_session = session.model_copy(update={"question": question})
    log_event(interaction.correlation_id, "triage_question", question=question.value)
    return _result(
        interaction,
        ResultKind.TRIAGE_QUESTION,
        QUESTION_MESSAGES[question],
        next_session,
        question=question,
    )


def _proposal(
    interaction: AgentInteraction, session: TriageSession, outcome: Outcome
) -> AgentResult:
    if outcome is Outcome.MERCHANT_REFUND_GUIDANCE:
        message = "Please contact the merchant to complete the agreed refund."
        next_steps = ["Contact the merchant about the agreed refund."]
        proposal = TriageProposal(outcome=outcome, message=message, next_steps=next_steps)
        next_session = session.model_copy(update={"proposal": proposal, "question": None})
        return _result(
            interaction,
            ResultKind.MERCHANT_REFUND_GUIDANCE,
            message,
            next_session,
            proposal=proposal,
        )

    label = "Fraud/scam" if outcome is Outcome.FRAUD_SCAM else "Dispute"
    proposal = TriageProposal(
        outcome=outcome,
        message=f"We have proposed a {label} case for this transaction.",
        next_steps=[f"Review the proposed {label} details.", "Confirm to create a mock case."],
    )
    next_session = session.model_copy(update={"proposal": proposal, "question": None})
    return _result(
        interaction,
        ResultKind.PROPOSAL,
        proposal.message,
        next_session,
        proposal=proposal,
    )


def _handle_answer(
    interaction: AgentInteraction, session: TriageSession, masked_message: str
) -> AgentResult:
    answer = parse_yes_no(masked_message)
    if answer is None:
        return _result(
            interaction,
            ResultKind.ERROR,
            "Please answer yes or no so I can continue your transaction triage.",
            session,
            question=session.question,
        )

    if session.question is Question.MERCHANT_KNOWN:
        updated = session.model_copy(update={"merchant_known": answer})
        if not answer:
            return _proposal(interaction, updated, Outcome.FRAUD_SCAM)
        return _ask_question(interaction, updated, Question.MERCHANT_REFUND_AGREED)
    if session.question is Question.MERCHANT_REFUND_AGREED:
        updated = session.model_copy(update={"merchant_refund_agreed": answer})
        if answer:
            return _proposal(interaction, updated, Outcome.MERCHANT_REFUND_GUIDANCE)
        return _ask_question(interaction, updated, Question.CUSTOMER_MADE_PURCHASE)

    updated = session.model_copy(update={"customer_made_purchase": answer})
    return _proposal(interaction, updated, Outcome.DISPUTE if answer else Outcome.FRAUD_SCAM)


def _handle_confirmation(interaction: AgentInteraction, session: TriageSession) -> AgentResult:
    if session.proposal is None:
        return _result(
            interaction,
            ResultKind.ERROR,
            "Please complete the transaction triage before confirming a case.",
            session,
        )
    if session.proposal.outcome is Outcome.MERCHANT_REFUND_GUIDANCE:
        return _result(
            interaction,
            ResultKind.MERCHANT_REFUND_GUIDANCE,
            session.proposal.message,
            session,
            proposal=session.proposal,
        )
    case_id = session.case_id or _new_case_id()
    next_session = session.model_copy(update={"case_id": case_id})
    return _result(
        interaction,
        ResultKind.CASE_CREATED,
        "Your mock case has been created. Follow the next steps provided.",
        next_session,
        proposal=next_session.proposal,
        case_id=case_id,
    )


def process_interaction(interaction: AgentInteraction, session: TriageSession) -> AgentResult:
    """Process a masked customer action without any external model or service call."""
    if interaction.confirmed:
        return _handle_confirmation(interaction, session)

    if interaction.selected_transaction_id is not None:
        transaction = get_transaction(interaction.selected_transaction_id)
        if transaction is None:
            return _result(
                interaction,
                ResultKind.ERROR,
                "The selected transaction was not found. Please choose another transaction.",
                session,
            )
        selected_session = session.model_copy(
            update={"selected_transaction": transaction, "question": Question.MERCHANT_KNOWN}
        )
        return _ask_question(interaction, selected_session, Question.MERCHANT_KNOWN)

    if interaction.message is None:
        return _result(
            interaction,
            ResultKind.ERROR,
            "Please provide a transaction report, select a transaction, or answer the "
            "triage question.",
            session,
        )

    masked_message = mask_pii(interaction.message)
    log_event(interaction.correlation_id, "message_received", message=masked_message)
    if session.question is not None:
        return _handle_answer(interaction, session, masked_message)

    merchants = extract_merchants(masked_message)
    amounts = extract_amounts(masked_message)
    if len(merchants) != 1 or len(amounts) != 1:
        return _result(
            interaction,
            ResultKind.REQUEST_DETAILS,
            "Please provide one supported merchant and one dollar amount for the transaction.",
            session,
        )
    if not is_reporting_intent(masked_message):
        return _result(
            interaction,
            ResultKind.REQUEST_DETAILS,
            "I am here to help with transaction issues. Please report the merchant and amount.",
            session,
        )

    matches, alternatives = find_transactions(merchants[0], amounts[0])
    if matches:
        return _result(
            interaction,
            ResultKind.TRANSACTION_MATCHES,
            "We found a matching transaction for you to review.",
            session,
            transactions=matches,
        )
    return _result(
        interaction,
        ResultKind.TRANSACTION_MATCHES,
        "We could not find an exact transaction. Please review these alternatives.",
        session,
        transactions=alternatives,
    )

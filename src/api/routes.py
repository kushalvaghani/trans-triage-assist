"""HTTP handlers for customer messages and triage submissions."""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .logging_service import log_session_event
from .models import (
    ErrorResponse,
    MessageRequest,
    MessageResponse,
    SubmissionRequest,
    SubmissionResponse,
)
from .pii import mask_pii
from .triage_service import (
    ConfirmationRequiredError,
    TransactionNotFoundError,
    evaluate_submission,
    process_message,
)

router = APIRouter(prefix="/exp-digiServicing-transctiontraige/v1")


def _correlation_id(value: UUID | None) -> UUID:
    return value or uuid4()


@router.post("/message", response_model=MessageResponse)
def post_message(payload: MessageRequest) -> MessageResponse:
    """Process only masked customer text and return a customer-safe response."""
    correlation_id = _correlation_id(payload.correlation_id)
    masked_message = mask_pii(payload.message)
    log_session_event(
        correlation_id,
        "message_received",
        endpoint="/message",
        message=masked_message,
    )
    response = process_message(masked_message, correlation_id)
    log_session_event(
        correlation_id,
        "message_responded",
        endpoint="/message",
        response_type=response.response_type,
    )
    return response


@router.post(
    "/submission",
    response_model=SubmissionResponse,
    responses={400: {"model": ErrorResponse}, 404: {"model": ErrorResponse}},
)
def post_submission(payload: SubmissionRequest) -> SubmissionResponse | JSONResponse:
    """Evaluate a selected mock transaction and enforce the confirmation gate."""
    correlation_id = _correlation_id(payload.correlation_id)
    masked_transaction_id = mask_pii(payload.transaction_id)
    log_session_event(
        correlation_id,
        "submission_received",
        endpoint="/submission",
        transaction_id=masked_transaction_id,
        triage_answers={
            "merchant_known": payload.merchant_known,
            "merchant_refund_agreed": payload.merchant_refund_agreed,
            "customer_made_purchase": payload.customer_made_purchase,
        },
        confirmed=payload.confirmed,
    )
    try:
        response = evaluate_submission(
            transaction_id=payload.transaction_id,
            merchant_known=payload.merchant_known,
            merchant_refund_agreed=payload.merchant_refund_agreed,
            customer_made_purchase=payload.customer_made_purchase,
            confirmed=payload.confirmed,
            correlation_id=correlation_id,
        )
    except (ConfirmationRequiredError, TransactionNotFoundError) as error:
        log_session_event(
            correlation_id,
            "submission_rejected",
            endpoint="/submission",
            reason=str(error),
        )
        status_code = 404 if isinstance(error, TransactionNotFoundError) else 400
        return JSONResponse(
            status_code=status_code,
            content=ErrorResponse(correlation_id=correlation_id, message=str(error)).model_dump(
                mode="json"
            ),
        )

    log_session_event(
        correlation_id,
        "submission_responded",
        endpoint="/submission",
        outcome=response.outcome,
        case_id=response.case_id,
    )
    return response

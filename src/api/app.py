"""FastAPI application for local mock transaction triage."""

from __future__ import annotations

from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .logging_service import log_session_event
from .routes import router

app = FastAPI(title="Transaction Triage Mock API", version="0.1.0")
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, _: RequestValidationError) -> JSONResponse:
    """Return a correlation-linked customer-safe response for invalid request payloads."""
    correlation_id = uuid4()
    log_session_event(correlation_id, "validation_rejected", endpoint=request.url.path)
    return JSONResponse(
        status_code=422,
        content={
            "correlation_id": str(correlation_id),
            "message": "We could not process that request. Please check the details and try again.",
        },
    )

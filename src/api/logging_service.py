"""Correlation-aware masked local session logging."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import UUID

LOG_DIRECTORY = Path(__file__).parent / "logs"


def log_session_event(correlation_id: UUID, event: str, **details: Any) -> None:
    """Append one already-masked JSON event to the session-specific local log file."""
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    payload = {"correlation_id": str(correlation_id), "event": event, **details}
    with (LOG_DIRECTORY / f"{correlation_id}.jsonl").open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + "\n")

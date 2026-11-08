"""Correlation-linked local logging for already-masked agent events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import UUID

LOG_DIRECTORY = Path(__file__).parents[3] / "logs"
MOCK_USER_ID = 599


def log_event(correlation_id: UUID, event: str, **details: Any) -> None:
    """Append an event supplied only after the agent has masked customer content."""
    LOG_DIRECTORY.mkdir(parents=True, exist_ok=True)
    payload = {
        "correlation_id": str(correlation_id),
        "user_id": MOCK_USER_ID,
        "event": event,
        **details,
    }
    with (LOG_DIRECTORY / f"{correlation_id}.jsonl").open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(payload, sort_keys=True) + "\n")

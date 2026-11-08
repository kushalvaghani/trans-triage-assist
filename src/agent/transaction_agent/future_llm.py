"""Inactive extension point for a future local intent or tool integration."""

from __future__ import annotations

from typing import Protocol


class FutureIntentTool(Protocol):
    """Potential future interface; no production agent code calls this protocol."""

    def analyse(self, message: str) -> str: ...


# This module deliberately defines no client, credentials, endpoint, or invocation.
# The current agent exclusively uses local functions from parsing.py and repository.py.

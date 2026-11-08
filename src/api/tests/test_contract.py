"""Tests for the documented OpenAPI endpoint paths."""

from api.app import app


def test_openapi_contains_the_documented_paths() -> None:
    paths = app.openapi()["paths"]

    assert "/exp-digiServicing-transctiontraige/v1/message" in paths
    assert "/exp-digiServicing-transctiontraige/v1/submission" in paths

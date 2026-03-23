"""Pytest configuration and fixtures."""

import pytest

from api.core.deps import _memory_store


@pytest.fixture(autouse=True)
def use_memory_store(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force in-memory store for all tests."""
    fake_settings = type("_", (), {"use_memory_store": True})()
    monkeypatch.setattr("api.core.config.settings", fake_settings)
    monkeypatch.setattr("api.core.deps.settings", fake_settings)


@pytest.fixture(autouse=True)
def clear_store() -> None:
    """Clear in-memory store before each test."""
    _memory_store._clear_for_tests()

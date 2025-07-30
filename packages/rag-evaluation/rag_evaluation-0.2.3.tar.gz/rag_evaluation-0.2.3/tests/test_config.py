import os
import pytest
from rag_evaluation.config import set_api_key, get_api_key


def test_set_and_get_in_memory():
    set_api_key("Test", "ABC123")
    assert get_api_key("test") == "ABC123"  # case‐insensitive lookup


def test_get_from_env(monkeypatch):
    monkeypatch.delenv("FOO_API_KEY", raising=False)
    monkeypatch.setenv("FOO_API_KEY", "ENV456")
    # no in-memory key, so should come from env
    assert get_api_key("foo") == "ENV456"


def test_get_default_fallback():
    assert get_api_key("bar", default_key="DEF789") == "DEF789"


def test_missing_key_raises(monkeypatch):
    monkeypatch.delenv("BAZ_API_KEY", raising=False)
    with pytest.raises(ValueError):
        get_api_key("baz")

"""Tests for AI client with error handling."""

import os
from unittest.mock import patch

import pytest

from projectmaker.core import ai_client


def test_create_client_missing_api_key():
    """Test that create_client raises helpful error when API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        # Remove ANTHROPIC_API_KEY if it exists
        os.environ.pop("ANTHROPIC_API_KEY", None)
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY environment variable is not set"):
            ai_client.create_client()


def test_create_client_with_api_key():
    """Test that create_client works with API key set."""
    with patch.dict(os.environ, {"ANTHROPIC_API_KEY": "test-key"}):
        client = ai_client.create_client()
        assert client is not None


def test_model_from_env():
    """Test that model can be overridden via environment variable."""
    with patch.dict(os.environ, {"ANTHROPIC_MODEL": "claude-3-opus-20240229"}):
        # Re-import to pick up the env var
        import importlib
        importlib.reload(ai_client)
        assert ai_client.MODEL == "claude-3-opus-20240229"
    
    # Reload again to restore default
    import importlib
    importlib.reload(ai_client)

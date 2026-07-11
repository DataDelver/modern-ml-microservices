import os
import pytest
from unittest.mock import patch
from shared.config.config_loader import load_config_settings


@pytest.fixture(autouse=True)
def clear_config_cache():
    """Clear the config loader cache before each test."""
    load_config_settings.cache_clear()
    yield


def test_config_default_values():
    """Test that configuration loads correctly from YAML with no environment variables set."""
    # GIVEN
    # Ensure MODEL_URL is not set
    with patch.dict(os.environ, {}, clear=True):
        # WHEN
        config = load_config_settings('default')

        # THEN
        assert config.pricing_model_url == 'http://housing-price-model:8080'


def test_config_with_env_var():
    """Test that configuration loads correctly from YAML with environment variables set."""
    # GIVEN
    with patch.dict(os.environ, {'MODEL_URL': 'http://custom-model:9000'}):
        # WHEN
        config = load_config_settings('default')

        # THEN
        assert config.pricing_model_url == 'http://custom-model:9000'


def test_config_environments():
    """Test that different environments (dev, qa, prod) load correctly."""
    # GIVEN
    with patch.dict(os.environ, {'MODEL_URL': 'http://custom-model:9000'}):
        # WHEN
        dev_config = load_config_settings('dev')
        qa_config = load_config_settings('qa')
        prod_config = load_config_settings('prod')

        # THEN
        assert dev_config.pricing_model_url == 'http://custom-model:9000'
        assert qa_config.pricing_model_url == 'http://custom-model:9000'
        assert prod_config.pricing_model_url == 'http://custom-model:9000'


def test_config_fallback_to_default():
    """Test that configuration falls back to the default value provided in the ${VAR:default} syntax."""
    # GIVEN
    # We want to verify that if MODEL_URL is missing, it uses the default.
    # In config.yaml, the default is http://housing-price-model:8080.
    # We can't easily change the YAML for one test, but we can check that
    # when MODEL_URL is NOT in env, it returns the YAML's default.
    with patch.dict(os.environ, {}, clear=True):
        # WHEN
        config = load_config_settings('default')

        # THEN
        assert config.pricing_model_url == 'http://housing-price-model:8080'

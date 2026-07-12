from pydantic_settings import BaseSettings


class UIConfigSettings(BaseSettings):
    """Configuration settings for the housing price UI application."""

    orchestrator_url: str = 'http://localhost:8000'
    """Base URL for the housing price orchestrator API."""

    model_config = {'env_prefix': ''}

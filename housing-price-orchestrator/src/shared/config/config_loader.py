from functools import lru_cache
import pathlib
import os
import re
from typing import Tuple, Type, Any
from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource


def resolve_env_vars(data: Any) -> Any:
    """Recursively resolves environment variable placeholders in the provided data.

    It identifies placeholders in the format ${VAR_NAME:default_value} or ${VAR_NAME}
    and replaces them with the corresponding environment variable value or the
    provided default value.

    Args:
        data: The data structure (dict, list, or string) containing potential
            placeholders to resolve.

    Returns:
        The data with all environment variable placeholders resolved.
    """
    if isinstance(data, dict):
        return {k: resolve_env_vars(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [resolve_env_vars(item) for item in data]
    elif isinstance(data, str):
        # Matches ${VAR_NAME} or ${VAR_NAME:default_value}
        pattern = r'\$\{([^:]+)(?::([^}]+))?\}'

        def replace_match(match: re.Match) -> str:
            var_name = match.group(1)
            default_value = match.group(2)

            if default_value is not None:
                return os.getenv(var_name, default_value)
            else:
                val = os.getenv(var_name)
                return val if val is not None else ''

        return re.sub(pattern, replace_match, data)
    return data


class Settings(BaseModel):
    pricing_model_url: str

    @model_validator(mode='before')
    @classmethod
    def resolve_env_vars_validator(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return resolve_env_vars(data)
        return data


class Config(BaseSettings):
    default: Settings
    dev: Settings
    qa: Settings
    prod: Settings
    model_config = SettingsConfigDict(yaml_file=pathlib.Path(__file__).parent.resolve() / 'config.yaml')

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )


@lru_cache
def load_config_settings(env: str) -> Settings:
    appconfig = Config()  # type: ignore
    return getattr(appconfig, env)

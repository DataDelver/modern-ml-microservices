from functools import lru_cache
import pathlib
from typing import Tuple, Type
from pydantic import BaseModel
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource


class Settings(BaseModel):
    met_api_url: str


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
            env_settings,
            dotenv_settings,
            file_secret_settings,
            YamlConfigSettingsSource(settings_cls),
        )


@lru_cache
def load_config_settings(env: str) -> Settings:
    appconfig = Config()  # type: ignore
    return getattr(appconfig, env)

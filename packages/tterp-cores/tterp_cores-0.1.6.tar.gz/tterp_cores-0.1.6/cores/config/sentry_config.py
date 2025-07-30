from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from cores.config.base_config import env_file_path


class SentryConfig(BaseSettings):
    SENTRY_ENABLE: bool = Field(default=False)
    SENTRY_DNS: str = Field(default="")
    model_config = SettingsConfigDict(env_file=env_file_path, extra="ignore")


sentry_config = SentryConfig()

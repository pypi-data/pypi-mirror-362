from pydantic_settings import BaseSettings, SettingsConfigDict

from cores.config.base_config import env_file_path


class MailConfig(BaseSettings):
    MAIL_DRIVER: str | None = None
    MAIL_HOST: str | None = None
    MAIL_PORT: int | None = None
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_ENCRYPTION: str | None = None
    MAIL_FROM_ADDRESS: str | None = None
    MAIL_FROM_NAME: str | None = None

    model_config = SettingsConfigDict(env_file=env_file_path, extra="ignore")


mail_config = MailConfig()

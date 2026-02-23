from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    dev_mode: bool
    token: str
    api_id: str
    api_hash: str
    postgres_dsn: str
    db_user: str
    db_name: str
    db_pass: str
    phone: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def logger_level(self) -> Literal["INFO", "DEBUG"]:
        if self.dev_mode:
            return "DEBUG"
        return "INFO"


settings = Settings()

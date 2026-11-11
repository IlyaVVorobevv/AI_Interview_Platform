from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    DB_URL: str

    @property
    def database_url(self) -> str:
        return self.DB_URL

    ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8"
    )

settings = Settings()
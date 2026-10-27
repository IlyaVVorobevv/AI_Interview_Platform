from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str

    @property
    def database_url(self) -> str:
        return self.DB_URL

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
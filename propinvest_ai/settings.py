from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    giga_token: str
    giga_scope: str


settings = Settings()  # type: ignore

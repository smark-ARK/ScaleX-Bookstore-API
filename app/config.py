from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    refresh_secret_key: str
    algorithm: str
    access_expire_minutes: int
    refresh_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings(_env_file=".env", extra="ignore")

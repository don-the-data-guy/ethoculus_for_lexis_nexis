from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    lexis_api_base_url: str = ""
    lexis_protege_ask_path: str = ""

    lexis_access_token: str = ""

    lexis_oauth_token_url: str = ""
    lexis_client_id: str = ""
    lexis_client_secret: str = ""
    lexis_oauth_scope: str = ""
    lexis_oauth_grant_type: str = ""

    lexis_prompt_field: str = ""
    lexis_response_text_path: str = ""

    lexis_timeout_seconds: int = 90

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()

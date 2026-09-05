from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str
    db_url: str
    api_host: str
    api_port: str
    embedding_model_name: str
    llm_model_name: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

"""Shared configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:0.5b"
    ollama_embed_model: str = "nomic-embed-text"

    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "articles"

    api_host: str = "0.0.0.0"
    api_port: int = 8000


settings = Settings()

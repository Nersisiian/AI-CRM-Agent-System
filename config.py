from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum
from typing import Optional

class LLMProvider(str, Enum):
    OPENAI = "openai"
    VLLM = "vllm"

class VectorStoreType(str, Enum):
    CHROMA = "chroma"
    QDRANT = "qdrant"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    LLM_PROVIDER: LLMProvider = LLMProvider.OPENAI
    VLLM_ENDPOINT: str = "http://localhost:8001/v1"
    VLLM_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.2"
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    EMBEDDING_PROVIDER: str = "openai"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    VECTOR_STORE: VectorStoreType = VectorStoreType.CHROMA
    QDRANT_URL: str = "http://localhost:6333"
    CHROMA_PERSIST_DIR: str = "./data/chroma"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "agent"
    POSTGRES_PASSWORD: str = "agentpass"
    POSTGRES_DB: str = "business_agent"
    DATABASE_URL: Optional[str] = None
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"
    CRM_BASE_URL: str = "https://example.kommo.com"
    CRM_API_KEY: str = ""
    AGENT_MAX_ITERATIONS: int = 8
    RATE_LIMIT_PER_SECOND: int = 10
    TRAINING_DATA_PATH: str = "./data/training/sales_conversations.jsonl"
    LORA_OUTPUT_DIR: str = "./models/lora-adapters"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DATABASE_URL:
            self.DATABASE_URL = (
                f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
            )
        if not self.REDIS_URL:
            self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"

settings = Settings()

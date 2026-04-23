from config import settings
from app.services.openai_service import OpenAIService

class EmbeddingService:
    def __init__(self):
        if settings.EMBEDDING_PROVIDER == "openai":
            self.provider = OpenAIService()
        else:
            # Можно добавить локальные эмбеддинги через sentence-transformers
            raise NotImplementedError

    async def embed(self, text: str):
        return await self.provider.get_embedding(text)
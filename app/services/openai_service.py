from typing import List, Dict, Any, Optional
import openai
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import settings
import structlog

logger = structlog.get_logger(__name__)

class OpenAIService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((openai.APIError, openai.APITimeoutError, openai.InternalServerError)),
        reraise=True,
    )
    async def acreate_chat_completion(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> Any:
        kwargs = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = "auto"
        response = await self.client.chat.completions.create(**kwargs)
        return response

    async def get_embedding(self, text: str) -> List[float]:
        response = await self.client.embeddings.create(
            input=text,
            model=settings.EMBEDDING_MODEL,
        )
        return response.data[0].embedding
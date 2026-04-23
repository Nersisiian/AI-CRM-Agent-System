from openai import AsyncOpenAI
from config import settings
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import openai

class VLLMService:
    def __init__(self):
        self.client = AsyncOpenAI(
            base_url=settings.VLLM_ENDPOINT,
            api_key="not-needed"
        )
        self.model = settings.VLLM_MODEL

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((openai.APIError, openai.APITimeoutError, openai.InternalServerError, ConnectionError)),
        reraise=True,
    )
    async def acreate_chat_completion(self, messages, tools=None, **kwargs):
        return await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            temperature=kwargs.get("temperature", 0.2),
        )

    async def get_embedding(self, text: str):
        # Можно использовать эмбеддинги через OpenAI или отдельный сервис
        return await OpenAIService().get_embedding(text)
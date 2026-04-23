from config import settings
from app.services.openai_service import OpenAIService
from app.services.vllm_service import VLLMService

_llm_service = None

def get_llm_service():
    global _llm_service
    if _llm_service is None:
        if settings.LLM_PROVIDER == "vllm":
            _llm_service = VLLMService()
        else:
            _llm_service = OpenAIService()
    return _llm_service
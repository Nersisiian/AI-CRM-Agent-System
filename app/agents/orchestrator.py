from typing import Dict, Any
import structlog
from app.agents.sales_agent import SalesAgent
from app.agents.support_agent import SupportAgent
from app.core.memory import MemoryManager
from app.services.llm_factory import get_llm_service

logger = structlog.get_logger(__name__)

INTENT_PROMPT = """Определи намерение одним словом: sales, support или general.
Пример:
Пользователь: Хочу купить тариф -> sales
Пользователь: У меня не работает интернет -> support
Пользователь: Привет! -> general
"""

class AgentOrchestrator:
    def __init__(self, sales_agent: SalesAgent, support_agent: SupportAgent, memory: MemoryManager):
        self.sales = sales_agent
        self.support = support_agent
        self.memory = memory
        self.llm = get_llm_service()

    async def route(self, message: str, session_id: str) -> Dict[str, Any]:
        resp = await self.llm.acreate_chat_completion(
            messages=[
                {"role": "system", "content": INTENT_PROMPT},
                {"role": "user", "content": message}
            ],
            temperature=0
        )
        intent = resp.choices[0].message.content.strip().lower()
        logger.info("routing", intent=intent)
        if intent == "sales":
            return await self.sales.process_message(message, session_id)
        elif intent == "support":
            return await self.support.process_message(message, session_id)
        else:
            return await self.sales.process_message(message, session_id, use_tools=False)

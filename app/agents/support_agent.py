from typing import Dict, Any
import structlog
from app.agents.tools.crm_tools import CRMTools
from app.rag.retrieval import RetrievalPipeline
from app.core.memory import MemoryManager
from app.services.llm_factory import get_llm_service
from config import settings

logger = structlog.get_logger(__name__)

SYSTEM_PROMPT_SUPPORT = """Ты — агент технической поддержки. Отвечай на вопросы пользователей, используй базу знаний и CRM инструменты для создания обращений. Будь дружелюбным и полезным."""

class SupportAgent:
    def __init__(self, memory: MemoryManager, db_session_factory, rag_pipeline: RetrievalPipeline):
        self.memory = memory
        self.db_factory = db_session_factory
        self.rag = rag_pipeline
        self.llm = get_llm_service()

    async def process_message(self, message: str, session_id: str) -> Dict[str, Any]:
        history = await self.memory.get_history(session_id)
        history.append({"role": "user", "content": message})
        context = await self.rag.retrieve_context(message)
        if context:
            history.insert(0, {"role": "system", "content": f"База знаний:\n{context}"})
        messages = [{"role": "system", "content": SYSTEM_PROMPT_SUPPORT}] + history

        for _ in range(settings.AGENT_MAX_ITERATIONS):
            response = await self.llm.acreate_chat_completion(messages=messages, tools=CRMTools.get_definitions())
            msg = response.choices[0].message
            if msg.tool_calls:
                async with self.db_factory() as db:
                    tools = CRMTools(db)
                    for tc in msg.tool_calls:
                        result = await tools.execute(tc.function.name, tc.function.arguments)
                        messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})
            else:
                final = msg.content
                await self.memory.add_message(session_id, "user", message)
                await self.memory.add_message(session_id, "assistant", final)
                return {"response": final, "sources": []}
        return {"response": "Извините, не удалось обработать запрос.", "sources": []}

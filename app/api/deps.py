from fastapi import Depends
from app.db.database import get_db_session
from app.rag.vector_store import VectorStore
from app.rag.retrieval import RetrievalPipeline
from app.core.memory import MemoryManager
from app.agents.orchestrator import AgentOrchestrator
from app.agents.sales_agent import SalesAgent
from app.agents.support_agent import SupportAgent
from app.integrations.crm_connector import CRMConnector
from config import settings
from sqlalchemy.ext.asyncio import AsyncSession

vector_store = VectorStore()
retrieval_pipeline = RetrievalPipeline(vector_store)
memory = MemoryManager()

async def get_sales_agent(db: AsyncSession = Depends(get_db_session)) -> SalesAgent:
    return SalesAgent(memory=memory, db_session_factory=get_db_session, rag_pipeline=retrieval_pipeline)

async def get_support_agent(db: AsyncSession = Depends(get_db_session)) -> SupportAgent:
    return SupportAgent(memory=memory, db_session_factory=get_db_session, rag_pipeline=retrieval_pipeline)

async def get_orchestrator(
    sales: SalesAgent = Depends(get_sales_agent),
    support: SupportAgent = Depends(get_support_agent),
) -> AgentOrchestrator:
    return AgentOrchestrator(sales_agent=sales, support_agent=support, memory=memory)

def get_crm_connector() -> CRMConnector:
    return CRMConnector(settings.CRM_BASE_URL, settings.CRM_API_KEY)
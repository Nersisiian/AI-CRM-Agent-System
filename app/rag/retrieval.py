import structlog
from app.rag.vector_store import VectorStore

logger = structlog.get_logger(__name__)

class RetrievalPipeline:
    def __init__(self, vector_store: VectorStore):
        self.store = vector_store

    async def retrieve_context(self, query: str, top_k: int = 3) -> str:
        try:
            results = await self.store.query(query, top_k=top_k)
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            contexts = [f"[{m.get('filename','')}] {d}" for d,m in zip(docs, metas)]
            return "\n\n".join(contexts)
        except Exception as e:
            logger.error("retrieval error", error=str(e))
            return ""
import uuid
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.models.ingest import IngestResponse
from app.agents.orchestrator import AgentOrchestrator
from app.rag.ingestion import IngestionPipeline
from app.api.deps import get_orchestrator, vector_store
from app.utils.metrics import metrics_collector
import structlog

logger = structlog.get_logger(__name__)
api_router = APIRouter()

@api_router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
):
    try:
        session_id = request.session_id or str(uuid.uuid4())
        result = await orchestrator.route(request.message, session_id)
        metrics_collector.increment("chat_requests")
        return ChatResponse(
            session_id=session_id,
            response=result.get("response", ""),
            sources=result.get("sources", []),
        )
    except Exception as e:
        logger.error("chat fail", error=str(e))
        metrics_collector.increment("chat_errors")
        raise HTTPException(500, "Agent processing error") from e

@api_router.post("/ingest", response_model=IngestResponse)
async def ingest(
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    content = await file.read()
    pipeline = IngestionPipeline(vector_store)
    count = await pipeline.ingest_pdf(content, file.filename)
    metrics_collector.increment("ingest_requests")
    return IngestResponse(status="success", chunks_stored=count, filename=file.filename)

@api_router.get("/health")
async def health():
    return {"status": "ok"}

@api_router.get("/metrics")
async def metrics():
    return {
        "chat_requests": metrics_collector.get("chat_requests", 0),
        "chat_errors": metrics_collector.get("chat_errors", 0),
        "ingest_requests": metrics_collector.get("ingest_requests", 0),
    }

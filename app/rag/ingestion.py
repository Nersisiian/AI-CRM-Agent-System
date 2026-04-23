import io
from PyPDF2 import PdfReader
from app.rag.vector_store import VectorStore
from app.utils.text_splitter import RecursiveCharacterTextSplitter
import structlog

logger = structlog.get_logger(__name__)

class IngestionPipeline:
    def __init__(self, vector_store: VectorStore):
        self.store = vector_store
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    async def ingest_pdf(self, file_bytes: bytes, filename: str) -> int:
        text = self._extract_text(file_bytes)
        if not text.strip():
            raise ValueError("No text in PDF")
        chunks = self.splitter.split_text(text)
        base_name = filename.rsplit(".", 1)[0]
        ids = [f"{base_name}-chunk{i}" for i in range(len(chunks))]
        metadatas = [{"filename": filename, "chunk_index": i} for i in range(len(chunks))]
        await self.store.add_documents(texts=chunks, metadatas=metadatas, ids=ids)
        logger.info("ingested", filename=filename, chunks=len(chunks))
        return len(chunks)

    def _extract_text(self, content: bytes) -> str:
        pdf = io.BytesIO(content)
        reader = PdfReader(pdf)
        text = ""
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
        return text
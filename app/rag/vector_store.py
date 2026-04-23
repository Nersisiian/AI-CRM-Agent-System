from config import settings
from chromadb.config import Settings as ChromaSettings
import chromadb
from chromadb.utils import embedding_functions
import qdrant_client
from qdrant_client.http import models as qdrant_models

class VectorStore:
    def __init__(self):
        if settings.VECTOR_STORE == "chroma":
            self.client = chromadb.PersistentClient(
                path=settings.CHROMA_PERSIST_DIR,
                settings=ChromaSettings(anonymized_telemetry=False),
            )
            self.embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY,
                model_name=settings.EMBEDDING_MODEL,
            )
            self.collection = self.client.get_or_create_collection(
                name="business_knowledge",
                embedding_function=self.embedding_fn,
            )
        elif settings.VECTOR_STORE == "qdrant":
            self.client = qdrant_client.QdrantClient(url=settings.QDRANT_URL)
            try:
                self.client.get_collection("business_knowledge")
            except Exception:
                self.client.create_collection(
                    collection_name="business_knowledge",
                    vectors_config=qdrant_models.VectorParams(
                        size=1536, distance=qdrant_models.Distance.COSINE
                    ),
                )
            self.collection = self.client

    async def add_documents(self, texts, metadatas=None, ids=None):
        # синхронный код обёрнут в asyncio.to_thread при использовании
        if settings.VECTOR_STORE == "chroma":
            self.collection.add(documents=texts, metadatas=metadatas, ids=ids)
        else:
            # Для Qdrant требуется конвертация в эмбеддинги
            from app.services.embedding_service import EmbeddingService
            emb_svc = EmbeddingService()
            vectors = [await emb_svc.embed(t) for t in texts]
            points = [
                qdrant_models.PointStruct(id=ids[i], vector=vectors[i], payload={
                    "text": texts[i], **metadatas[i]
                })
                for i in range(len(texts))
            ]
            self.client.upsert(collection_name="business_knowledge", points=points)

    async def query(self, query_text, top_k=3):
        if settings.VECTOR_STORE == "chroma":
            return self.collection.query(query_texts=[query_text], n_results=top_k)
        else:
            from app.services.embedding_service import EmbeddingService
            emb_svc = EmbeddingService()
            query_vector = await emb_svc.embed(query_text)
            results = self.client.search(
                collection_name="business_knowledge",
                query_vector=query_vector,
                limit=top_k
            )
            return {"documents": [[r.payload["text"] for r in results]], "metadatas": [[r.payload for r in results]]}
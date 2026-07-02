"""Embedding pipeline — vectorize articles and store in Qdrant."""

import httpx
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from collector.fetch_articles import Article
from config import settings

VECTOR_SIZE = 768  # nomic-embed-text dimension


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)


def ensure_collection(client: QdrantClient) -> None:
    collections = [c.name for c in client.get_collections().collections]
    if settings.qdrant_collection not in collections:
        client.create_collection(
            collection_name=settings.qdrant_collection,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
        )


def embed_text(text: str) -> list[float]:
    """Call Ollama embedding API. Requires `ollama pull nomic-embed-text`."""
    url = f"{settings.ollama_base_url}/api/embeddings"
    payload = {"model": settings.ollama_embed_model, "prompt": text}
    with httpx.Client(timeout=60) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()["embedding"]


def index_articles(articles: list[Article], start_id: int = 0) -> int:
    """Embed articles and upsert into Qdrant. Returns number of indexed items."""
    client = get_qdrant_client()
    ensure_collection(client)

    points: list[PointStruct] = []
    for i, article in enumerate(articles):
        text = f"{article.title}\n{article.content}"
        vector = embed_text(text)
        points.append(
            PointStruct(
                id=start_id + i,
                vector=vector,
                payload={
                    "title": article.title,
                    "url": article.url,
                    "source": article.source,
                },
            )
        )

    if points:
        client.upsert(collection_name=settings.qdrant_collection, points=points)
    return len(points)

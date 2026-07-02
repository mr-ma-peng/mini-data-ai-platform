from fastapi import FastAPI
from pydantic import BaseModel

from config import settings

app = FastAPI(
    title="Mini Data & AI Platform",
    description="Local DataOps + AI Platform — MVP RAG API",
    version="0.1.0",
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list[str]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/config")
def get_config():
    """Expose non-sensitive runtime config for debugging."""
    return {
        "ollama_model": settings.ollama_model,
        "qdrant_collection": settings.qdrant_collection,
    }


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    """RAG endpoint — placeholder until embedding pipeline is wired up."""
    return AskResponse(
        answer=f"[placeholder] Received: {req.question}",
        sources=[],
    )

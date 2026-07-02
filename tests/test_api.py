from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_ask_placeholder():
    resp = client.post("/ask", json={"question": "What is RAG?"})
    assert resp.status_code == 200
    body = resp.json()
    assert "answer" in body
    assert "sources" in body

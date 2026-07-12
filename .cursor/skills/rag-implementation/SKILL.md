---
name: rag-implementation
description: >-
  Phase 1 RAG 闭环实现 SOP：采集、切块、向量检索、/ask 接入 Ollama。
  在用户提到 RAG、/ask、embedding、chunk、检索、sources 引用时使用。
---

# RAG 实现 SOP（Phase 1）

## 目标

`/ask` 返回真实答案 + `sources` 引用列表。验收见 `docs/design.md` Phase 1。

## 数据流

```
RSS → collector.fetch_articles → Article[]
     → embedding.pipeline (chunk + embed)
     → Qdrant
     → api /ask (retrieve + prompt + Ollama generate)
     → AskResponse { answer, sources }
```

## 实现顺序

### 1. 采集层（collector）

- 扩充 RSS 源，支持分页
- `Article` 模型：`title, url, content, published_at, source`
- 去重：按 URL hash

### 2. 向量层（embedding）

- 文本切块（建议 512 token 级，overlap 50）
- `embed_text()` 已有，接 Ollama nomic-embed-text
- payload 含 `title, url, source, chunk_index`
- `scripts/ingest.py` 编排全流程

### 3. 检索 + 生成（建议新建 llm/ 或 api/rag.py）

```python
# 伪代码结构
def ask(question: str) -> AskResponse:
    query_vector = embed_text(question)
    hits = qdrant.search(collection, query_vector, limit=5)
    context = format_chunks(hits)
    prompt = build_rag_prompt(context, question)
    answer = ollama_generate(prompt)
    sources = [{title, url, score} for hit in hits]
    return AskResponse(answer=answer, sources=sources)
```

### 4. API 层

- `api/main.py` 的 `/ask` 调用 RAG 函数，去掉 placeholder
- `AskResponse.sources` 升级为结构化列表（与 design.md 对齐）

### 5. 测试

- 单元测试：mock Qdrant / Ollama 响应
- 集成测试：标记 `@pytest.mark.integration`，不放入默认 `make test`

## 约束

- 检索参数（top-k）走 config 或常量，便于 Phase 4 抽象 RAGChain
- Prompt 模板放独立文件（`llm/prompts/`），不在代码里写长字符串
- 最小可用优先，不做重排 / Agent 多步（留 Phase 4）

## 参考

- [docs/design.md](../../docs/design.md) §4.3 数据模型、§4.4 API 设计
- 现有实现：`embedding/pipeline.py`、`api/main.py`

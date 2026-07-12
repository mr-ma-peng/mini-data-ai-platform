# /ingest — 采集并入库

运行数据采集 + 向量化 + Qdrant 入库流水线。

## 前置

- `make up` 已启动 Qdrant 与 Ollama
- 已拉取 `nomic-embed-text` 模型

## 步骤

1. 确认 Ollama / Qdrant 可用（可参考 Skill `local-dev`）
2. 执行 `make ingest`（默认 `--limit 10`）
3. 检查输出：采集条数、入库条数、失败原因
4. 可选：`curl -X POST localhost:8000/ask -H 'Content-Type: application/json' -d '{"question":"..."}'` 验证检索

## 约束

- 不修改 `scripts/ingest.py` 的默认 limit 除非用户指定
- ingest 失败时先查 Ollama 模型与网络，不盲目重试
- 不读取 `.env` 内容

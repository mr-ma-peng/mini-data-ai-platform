---
name: local-dev
description: >-
  Mini Data & AI Platform 本地开发环境启动与排障。
  在用户提到 make dev、Ollama、Qdrant、ingest、本地跑不起来、mise 时使用。
---

# 本地开发 SOP

工作目录：项目根 `mini-data-ai-platform/`

## 前置检查

```bash
eval "$(mise activate zsh)"   # 若 mise 未激活
mise exec -- python --version # 应显示 3.12.x
docker compose ps             # Qdrant + Ollama 状态
```

## 标准启动顺序

```bash
cp .env.example .env          # 首次
make install
make up                       # Qdrant :6333, Ollama :11434
docker compose exec ollama ollama pull qwen2.5:0.5b
docker compose exec ollama ollama pull nomic-embed-text
make dev                      # API :8000
```

## 常用验证

| 检查 | 命令 |
|------|------|
| API 健康 | `curl localhost:8000/health` |
| OpenAPI | http://localhost:8000/docs |
| 入库 | `make ingest` |
| 测试 | `make test` |

## 排障

| 症状 | 处理 |
|------|------|
| `Connection refused :11434` | `make up`，确认 Ollama 容器运行 |
| embed 失败 | `ollama pull nomic-embed-text` |
| Qdrant 连接失败 | 检查 `QDRANT_HOST/PORT` 与 `docker compose ps` |
| mise 找不到 python | `mise install` 后重开 shell |
| ingest 超时 | Ollama 首次拉模型较慢，增大 httpx timeout |

## 约束

- 配置从 `config.py` / `.env.example` 读取，不硬编码端口
- 不读取 `.env` 实际内容

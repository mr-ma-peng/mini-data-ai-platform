# Mini Data & AI Platform

本地运行的 **DataOps + AI Platform**，用于学习数据工程、RAG 与 DevOps。

> 完整架构、分阶段路线、模块设计见 **[项目设计文档](./docs/design.md)**。

## 架构（MVP）

```
RSS → collector → embedding → Qdrant
                                 ↓
                     Ollama ← api (FastAPI) → frontend（待建）
```

## 目录结构

```
mini-data-ai-platform/
├── api/              # FastAPI 服务
├── collector/        # 数据采集（RSS）
├── embedding/        # 向量化 + Qdrant
├── scripts/          # ingest 等运维脚本
├── frontend/         # Web UI（占位）
├── tests/
├── docs/
│   └── design.md     # 项目设计文档
├── config.py
├── mise.toml         # Python 版本（mise 管理）
├── docker-compose.yml   # Qdrant + Ollama
└── requirements.txt
```

## 快速开始

### 0. 前置条件

- [mise](https://mise.jdx.dev/)（管理 Python 版本）
- Docker（运行 Qdrant / Ollama）

确保 shell 已激活 mise（写入 `~/.zshrc` 一次即可）：

```bash
eval "$(mise activate zsh)"
```

### 1. 环境准备

```bash
cp .env.example .env
make install          # 自动安装 Python 3.12 并创建 .venv
mise exec -- python --version
```

### 2. 启动基础服务

```bash
make up
```

启动 Qdrant（6333）和 Ollama（11434）。

拉取所需模型：

```bash
docker compose exec ollama ollama pull qwen2.5:3b
docker compose exec ollama ollama pull nomic-embed-text
```

### 3. 启动 API

```bash
make dev
```

访问 http://localhost:8000/docs 查看交互式 API 文档。

### 4. 导入数据（可选，需 Ollama 运行）

```bash
make ingest
```

### 5. 运行测试

```bash
make test
```

## 开发阶段

| 阶段 | 目标 | 状态 |
|------|------|------|
| Phase 0 骨架 | 目录、API、Compose、测试 | ✅ 完成 |
| Phase 1 MVP | RAG 闭环 + ~1000 篇文章 | 🚧 进行中 |
| Phase 2 数据工程 | Kafka + ClickHouse | 待开始 |
| Phase 3 DataOps | Airflow + 数据质量 | 待开始 |
| Phase 4 AI 工程 | Agent + Prompt 管理 | 待开始 |
| Phase 5 CI/CD | GitHub Actions | 待开始 |

详见 [docs/design.md](./docs/design.md)。

## License

MIT — 见 [LICENSE](./LICENSE)。

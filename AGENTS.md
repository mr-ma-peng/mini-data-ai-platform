# Mini Data & AI Platform

本地运行的 **DataOps + AI Platform**，用于学习数据工程、RAG 与 Agent 工程化。

> 详细架构与分阶段路线见 [docs/design.md](./docs/design.md)

## 当前阶段

**Phase 1 — MVP：RAG 闭环**（进行中）

目标：Ollama + Qdrant + 约 1000 篇技术文章 + 可问答 API。

验收：对技术问题返回有据可查的回答，并列出来源 URL。

## 目录

```text
api/           FastAPI 服务（/health, /config, /ask）
collector/     RSS 采集 → Article
embedding/     向量化 + Qdrant 入库
scripts/       离线任务（ingest.py）
tests/         pytest
docs/          设计文档
config.py      pydantic-settings 统一配置
```

规划模块（尚未创建，见 design.md）：`llm/`、`frontend/`、`kafka/`、`airflow/`

## 常用命令

```bash
make install    # mise + pip 依赖
make up         # 启动 Qdrant + Ollama（Docker）
make dev        # 启动 FastAPI（:8000）
make test       # pytest
make ingest     # 采集 + 入库（需 Ollama 运行）
```

Python 版本由 **mise** 管理，命令前缀 `mise exec --`。

## 架构约束

- 全项目 **Python 3.12 单体 + 模块化分包**，不引入 Java 等其他后端
- 配置统一走 `config.py`（pydantic-settings），禁止硬编码 URL / 端口
- MVP 阶段跳过 Kafka / Flink，用脚本直连「采集 → 向量 → 问答」
- 新模块按 `collector → embedding → api` 数据流方向扩展，不跨层调用

## Agent 配置层

完整导览见 [docs/agent-config.md](./docs/agent-config.md)。

```text
.cursor/
├── rules/
│   ├── project-core.mdc        # alwaysApply：阶段与模块边界
│   ├── python-conventions.mdc    # globs **/*.py
│   └── secrets-and-env.mdc       # alwaysApply：密钥保护
├── commands/
│   ├── test.md                   # /test
│   ├── phase-check.md            # /phase-check
│   └── ingest.md                 # /ingest
├── skills/
│   ├── local-dev/                # 本地启动与排障
│   └── rag-implementation/       # RAG 闭环 SOP
├── agents/
│   ├── code-reviewer.md
│   └── security-reviewer.md
└── hooks/
    ├── hooks.json
    ├── block-dangerous-git.sh    # 拦危险 Git
    ├── block-secret-read.sh      # 拦读 .env
    └── audit-mcp.sh              # MCP 调用审计
```

## 不要

- 不要提交 `.env` 或 API Key
- 不要改 `requirements.txt` 版本号除非 plan 明确要求
- 不要硬编码 `localhost:11434` 等地址，用 `settings.*`
- 不要提前引入 Phase 2+ 组件（Kafka、ClickHouse）到 MVP 代码路径
- 不要创建空壳模块目录，等对应 Phase 启动时再建

## 参考

- 设计文档：[docs/design.md](./docs/design.md)
- 远程仓库：https://github.com/mr-ma-peng/mini-data-ai-platform

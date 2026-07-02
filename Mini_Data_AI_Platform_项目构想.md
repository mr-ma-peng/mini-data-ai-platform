# Mini Data & AI Platform — 项目构想与设计

> 仓库：[github.com/mr-ma-peng/mini-data-ai-platform](https://github.com/mr-ma-peng/mini-data-ai-platform)

## 1. 项目定位

打造一个**运行在本地**的 Mini Data & AI Platform，用一条完整链路学习：

| 领域 | 学什么 |
|------|--------|
| 数据工程 | 采集、流处理、OLAP、数据建模 |
| DataOps | 调度、质量、血缘、可观测性 |
| AI 工程 | Embedding、RAG、Agent、Prompt |
| DevOps | 容器化、CI/CD、测试、部署 |
| 软件架构 | 分层、演进式架构、模块边界 |

**核心思想：**

> 不只是跑一个本地 LLM，而是搭建「数据平台 + AI 平台」的最小可行系统，再逐步演进到准生产形态。

**非目标（现阶段不做）：**

- 多租户 SaaS、高可用集群
- 替代 Databricks / Snowflake 级别产品
- 追求极致性能与成本优化

---

## 2. 技术选型（已定）

| 层次 | 技术 | 说明 |
|------|------|------|
| 语言 | **Python 3.9+** | 数据与 AI 生态成熟，MVP 快速迭代 |
| API | **FastAPI** | 异步友好、自动 OpenAPI 文档 |
| 本地 LLM | **Ollama** | Qwen / Llama 等，零云依赖 |
| 向量库 | **Qdrant** | MVP 首选；后续可抽象接口换 Milvus |
| 消息队列 | Kafka | 第二阶段引入 |
| OLAP | ClickHouse | 第二阶段引入 |
| 调度 | Airflow | 第三阶段引入 |
| 容器 | Docker Compose → K8s | MVP 用 Compose，后期可迁移 |
| CI | GitHub Actions | 第五阶段完善 |

**后端栈：** 全项目统一 **Python 单体 + 模块化分包**，不引入 Java 或其他语言后端。

---

## 3. 架构演进

### 3.1 目标架构（终态愿景）

```text
数据源（RSS / GitHub / API / 模拟订单）
        │
        ▼
   Python Collector
        │
        ▼
      Kafka                    ← 事件总线，解耦采集与消费
        │
 ┌──────┴──────────┐
 │                  │
 ▼                  ▼
Flink Job      Spark Job（可选）
 │                  │
 ▼                  ▼
Iceberg / ClickHouse          ← 明细 + 分析层
        │
        ▼
 Embedding Pipeline            ← 由 Airflow 调度
        │
        ▼
   Qdrant（向量库）
        │
        ▼
 Ollama（生成 + Embedding）
        │
        ▼
    FastAPI（RAG / Agent API）
        │
        ▼
   Web UI / Dashboard
```

### 3.2 MVP 架构（当前阶段）

MVP **刻意简化**：跳过 Kafka / Flink，用脚本直连完成「采集 → 向量 → 问答」闭环。

```text
RSS Feed
    │
    ▼
collector/          # fetch_articles.py
    │
    ▼
embedding/          # pipeline.py（Ollama embed → Qdrant）
    │
    ▼
Qdrant
    │
    ▼
api/                # FastAPI：检索 + Ollama 生成
    │
    ▼
frontend/（待建）
```

**MVP 与终态的差异是设计选择，不是遗漏。** 先验证 RAG 价值，再引入流式数据工程复杂度。

---

## 4. 模块设计

### 4.1 目录结构

**当前已实现（Phase 0 骨架）：**

```text
mini-data-ai-platform/
├── api/                 # HTTP 服务层
│   └── main.py
├── collector/           # 数据采集
│   └── fetch_articles.py
├── embedding/           # 向量化与入库
│   └── pipeline.py
├── scripts/             # 运维与一次性任务
│   └── ingest.py
├── frontend/            # Web UI（占位）
├── tests/
├── config.py            # 统一配置（pydantic-settings）
├── docker-compose.yml   # Qdrant + Ollama
├── requirements.txt
├── Makefile
└── .env.example
```

**随阶段扩展（尚未创建）：**

```text
├── simulator/           # 模拟订单 / 事件数据源（Phase 2）
├── kafka/               # Topic 定义、本地配置（Phase 2）
├── flink-job/           # 流处理作业（Phase 2+）
├── clickhouse/          # Schema、迁移脚本（Phase 2）
├── airflow/             # DAG：采集、质量、Embedding（Phase 3）
├── llm/                 # Prompt 模板、RAG 链、Agent（Phase 4）
├── dashboard/           # 数据看板（Phase 3+）
├── monitoring/          # Prometheus / Grafana 配置（Phase 5+）
└── .github/workflows/   # CI（Phase 5）
```

### 4.2 模块职责

| 模块 | 职责 | 输入 | 输出 |
|------|------|------|------|
| `collector` | 从 RSS / API / 文件拉取原始内容 | Feed URL、API Key | `Article` 结构化对象 |
| `embedding` | 文本切块、调用 Embedding、写入向量库 | `Article[]` | Qdrant Points |
| `api` | 对外 REST：健康检查、问答、检索 | HTTP 请求 | JSON 响应 |
| `scripts` | 编排离线任务（ingest、reindex） | CLI 参数 | 副作用（DB 写入） |
| `llm`（规划） | RAG 检索、Prompt 组装、调用 Ollama | 用户问题 | 答案 + 引用来源 |
| `frontend`（规划） | 聊天式 UI、引用展示 | 用户输入 | 渲染回答 |

### 4.3 核心数据模型

```python
# collector — 采集层
Article:
  title: str
  url: str
  content: str
  published_at: datetime | None
  source: str

# Qdrant payload — 向量层
Point payload:
  title, url, source, chunk_index（后续）

# api — 问答层
AskRequest:  { question: str }
AskResponse: { answer: str, sources: [{ title, url, score }] }
```

### 4.4 API 设计（规划）

| 方法 | 路径 | 状态 | 说明 |
|------|------|------|------|
| GET | `/health` | ✅ 已实现 | 存活探针 |
| GET | `/config` | ✅ 已实现 | 非敏感运行时配置 |
| POST | `/ask` | 🚧 占位 | RAG 问答（待接入检索 + LLM） |
| POST | `/ingest` | 规划 | 触发采集入库（或仅内部脚本） |
| GET | `/search` | 规划 | 纯向量检索，不生成 |

---

## 5. 分阶段路线图

每个阶段有**交付物**和**验收标准**，避免「学了很多但系统跑不起来」。

### Phase 0 — 工程骨架 ✅ 已完成

| 项 | 内容 |
|----|------|
| 交付 | 目录、FastAPI 空壳、docker-compose、测试、README |
| 验收 | `make test` 通过；`make dev` 可访问 `/docs` |

### Phase 1 — MVP：RAG 闭环 🚧 进行中

| 项 | 内容 |
|----|------|
| 目标 | 本地 Ollama + 约 1000 条技术文章 + 可问答 |
| 任务 | |
| | 1. 扩充 RSS 源，支持分页 / 增量采集 |
| | 2. 文本切块（chunk）与去重 |
| | 3. 完成 `/ask`：Qdrant 检索 → Prompt → Ollama 生成 |
| | 4. 返回 `sources` 引用列表 |
| | 5. 简单 Web UI 或 Streamlit 原型 |
| 学习 | Ollama、Embedding、向量检索、RAG、FastAPI |
| 验收 | 对技术问题能返回有据可查的回答，并列出来源 URL |

### Phase 2 — 数据工程

| 项 | 内容 |
|----|------|
| 目标 | 引入流式数据管道，分离采集与消费 |
| 增加 | Kafka、ClickHouse、`simulator/` 模拟订单流 |
| 任务 | |
| | 1. Collector 写 Kafka Topic，不再直连 Embedding |
| | 2. Consumer 落 ClickHouse（原始层 + 聚合层） |
| | 3. 可选：Flink 做实时窗口统计 |
| | 4. Embedding 从 ClickHouse 或 Kafka 触发 |
| 学习 | 消息队列、流处理、OLAP、ETL |
| 验收 | 模拟事件持续写入；ClickHouse 可 SQL 查询；向量库可定时增量更新 |

### Phase 3 — DataOps

| 项 | 内容 |
|----|------|
| 目标 | 可调度、可观测、可治理的数据作业 |
| 增加 | Airflow、数据质量检查、日志与告警 |
| 任务 | |
| | 1. DAG：日采集、Embedding 重建、质量报告 |
| | 2. 质量规则：空标题率、重复 URL、向量维度一致性 |
| | 3. 结构化日志 + 简单 Dashboard |
| 学习 | 调度、数据治理、数据质量 |
| 验收 | Airflow UI 可见任务历史；质量失败可告警（邮件 / Webhook 任选） |

### Phase 4 — AI 工程深化

| 项 | 内容 |
|----|------|
| 目标 | 从「能问答」到「好用、可扩展」的 AI 层 |
| 增加 | `llm/` 模块、Agent、Prompt 版本管理 |
| 任务 | |
| | 1. 抽象 `RAGChain`：检索策略可配置（top-k、重排） |
| | 2. 多步 Agent（查库 → 总结 → 追问） |
| | 3. Prompt 模板文件化 + 版本号 |
| | 4. 可选：对接 MCP 工具 |
| 学习 | LLMOps、Agent 编排、评估 |
| 验收 | 切换 Prompt / 检索参数无需改 API 代码；有基础评测脚本（命中率 / 幻觉抽查） |

### Phase 5 — DevOps / CI/CD

| 项 | 内容 |
|----|------|
| 目标 | 合并即测试、可重复部署 |
| 增加 | GitHub Actions、镜像构建、集成测试 |
| 任务 | |
| | 1. PR 触发：lint + pytest |
| | 2. 可选：docker compose 集成测试（起 Qdrant mock） |
| | 3. README 部署文档与版本标签 |
| 学习 | CI/CD、发布流程 |
| 验收 | 主干分支 CI 绿灯；文档描述可从零拉起环境 |

---

## 6. 基础设施与配置

### 6.1 Docker Compose 服务（MVP）

| 服务 | 端口 | 用途 |
|------|------|------|
| Qdrant | 6333 | 向量存储与检索 |
| Ollama | 11434 | Embedding + 文本生成 |

### 6.2 环境变量（`.env`）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama API |
| `OLLAMA_MODEL` | `qwen2.5:3b` | 生成模型 |
| `OLLAMA_EMBED_MODEL` | `nomic-embed-text` | Embedding 模型 |
| `QDRANT_HOST` | `localhost` | 向量库地址 |
| `QDRANT_PORT` | `6333` | |
| `QDRANT_COLLECTION` | `articles` | 集合名 |

### 6.3 本地开发命令

```bash
make install    # 创建 venv、安装依赖
make up         # 启动 Qdrant + Ollama
make dev        # 启动 FastAPI（热重载）
make ingest     # 采集并写入向量库
make test       # 运行 pytest
```

---

## 7. 数据流（MVP 详解）

```text
1. ingest 启动
      │
2. collector.fetch_all()
      │  解析 RSS → List[Article]
      │
3. embedding.index_articles()
      │  每条: title + content → Ollama /api/embeddings
      │  向量 + payload → Qdrant upsert
      │
4. 用户 POST /ask { question }
      │
5.（待实现）question → embed → Qdrant search top-k
      │
6.（待实现）context + question → Ollama /api/generate
      │
7.（待实现）返回答案 + sources
```

---

## 8. 质量与工程规范

| 规范 | 说明 |
|------|------|
| 测试 | 新 API 必须有 pytest；核心逻辑逐步补单元测试 |
| 配置 | 禁止硬编码密钥；统一走 `config.py` + `.env` |
| 提交 | 小步提交；message 说明「为什么」 |
| 分支 | `main` 保持稳定；功能用 `feat/xxx` 分支 |
| 文档 | 构想（本文）= 设计真理；README = 快速上手 |

---

## 9. 后续可扩展方向

在 Phase 5 之后，按兴趣择一深入：

- **Lakehouse**：Iceberg 表格式 + Spark
- **Kubernetes**：Helm Chart 部署全栈
- **可观测性**：Prometheus + Grafana + OpenTelemetry
- **元数据**：OpenMetadata / DataHub
- **协议**：MCP Server 暴露 RAG 为工具
- **多 Agent**：规划、检索、执行分工

---

## 10. 当前进度快照

| 模块 / 能力 | 状态 |
|-------------|------|
| Git + GitHub 远程 | ✅ |
| 工程骨架 | ✅ |
| RSS 采集 | ✅ 基础版 |
| Embedding → Qdrant | ✅ 骨架（依赖 Ollama 运行） |
| RAG `/ask` | ⏳ 占位，未接检索与生成 |
| Web UI | ⏳ 仅占位 |
| Kafka / ClickHouse | ⏳ 未开始 |
| Airflow | ⏳ 未开始 |
| CI/CD | ⏳ 未开始 |

**下一步建议（Phase 1）：** 实现完整 RAG 链路——`embedding` 增加 `search()`，`api` 组装 Prompt 调用 Ollama，补集成测试。

---

## 11. 最终愿景

构建一个**长期维护的个人开源项目** — **Mini Data & AI Platform**：

- 能从零说明白「数据怎么进来、怎么存、怎么变成 AI 可用的知识」
- 能在本地演示完整 DataOps + RAG 链路
- 能作为面试 / 博客 / 教学的具象案例
- 架构可演进，而不是一次性堆满所有组件

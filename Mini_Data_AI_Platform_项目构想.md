# Mini Data & AI Platform 项目构想

## 项目目标

打造一个运行在本地的 **Mini Data & AI Platform**，通过一个完整项目学习：

-   数据工程（Data Engineering）
-   DataOps
-   AI Engineering（RAG / Agent）
-   DevOps / CI/CD
-   软件架构设计

核心思想：

> 不只是运行一个本地 LLM，而是搭建一套完整的数据平台 + AI 平台。

------------------------------------------------------------------------

# 总体架构

``` text
数据源（GitHub、RSS、API、模拟订单）
        │
        ▼
 Python Collector
        │
        ▼
      Kafka
        │
 ┌──────┴────────┐
 │               │
 ▼               ▼
Flink         Spark（后续）
 │
 ▼
Iceberg / ClickHouse
 │
 ▼
Embedding Pipeline
 │
 ▼
Qdrant / Milvus
 │
 ▼
Ollama（Qwen / Llama）
 │
 ▼
FastAPI
 │
 ▼
Web UI
```

------------------------------------------------------------------------

# 开发阶段

## 第一阶段：MVP

目标：

-   本地运行 Ollama
-   导入约 1000 条技术文章
-   建立向量库
-   实现 RAG 问答

学习内容：

-   Ollama
-   Embedding
-   Vector Database
-   FastAPI

------------------------------------------------------------------------

## 第二阶段：数据工程

增加：

-   Kafka
-   ClickHouse
-   实时消费

学习：

-   消息队列
-   数据流
-   ETL

------------------------------------------------------------------------

## 第三阶段：DataOps

增加：

-   Airflow
-   数据质量检查
-   DAG 调度
-   日志
-   告警

学习：

-   数据调度
-   数据治理
-   数据质量

------------------------------------------------------------------------

## 第四阶段：AI 工程

增加：

-   Embedding Pipeline
-   RAG
-   Agent
-   Prompt 管理

学习：

-   AI 工程
-   LLMOps

------------------------------------------------------------------------

## 第五阶段：CI/CD

增加：

-   Docker Compose
-   GitHub Actions
-   自动测试
-   自动部署

学习：

-   DevOps
-   CI/CD

------------------------------------------------------------------------

# 建议目录结构

``` text
mini-ai-platform/
├── collector/
├── simulator/
├── kafka/
├── flink-job/
├── clickhouse/
├── airflow/
├── embedding/
├── vector-db/
├── llm-service/
├── api/
├── frontend/
├── dashboard/
├── monitoring/
├── docker-compose.yml
└── README.md
```

------------------------------------------------------------------------

# 后续可扩展

-   Lakehouse（Iceberg）
-   Kubernetes
-   Prometheus + Grafana
-   OpenTelemetry
-   OpenMetadata
-   DataHub
-   MCP
-   Multi-Agent

------------------------------------------------------------------------

# 最终目标

构建一个长期维护的个人开源项目：

**Mini Data & AI Platform**

它将完整覆盖：

-   Java 后端
-   数据工程
-   DataOps
-   AI 工程
-   DevOps
-   软件架构

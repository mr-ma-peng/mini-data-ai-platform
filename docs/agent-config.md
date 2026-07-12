# Agent 配置层导览

本仓库是 **Cursor Agent 配置的真实案例**：`AGENTS.md` + 三件套 + Subagent + Hooks，可直接 fork 后改内容。

## 分层一览

| 层级 | 位置 | 本仓库示例 | 作用 |
|------|------|------------|------|
| 项目说明书 | `AGENTS.md` | 根目录 | 5 分钟建立心智模型 |
| Rule | `.cursor/rules/*.mdc` | 3 条 | 自动约束 |
| Command | `.cursor/commands/*.md` | `/test` `/phase-check` `/ingest` | 你主动触发的起手式 |
| Skill | `.cursor/skills/*/SKILL.md` | `local-dev` `rag-implementation` | 多步骤 SOP |
| Subagent | `.cursor/agents/*.md` | `code-reviewer` `security-reviewer` | 专项审查，独立会话 |
| Hooks | `.cursor/hooks.json` | Git 拦截、敏感文件、MCP 审计 | 运行时硬闸门 |

**分工口诀**：AGENTS 管地图 → Rule 管底线 → Command/Skill 管流程 → Subagent 管分工 → Hooks 管能不能做。

## 目录树

```text
AGENTS.md
.cursor/
├── rules/
│   ├── project-core.mdc        # alwaysApply：阶段、模块边界
│   ├── python-conventions.mdc  # globs **/*.py：编码规范
│   └── secrets-and-env.mdc     # alwaysApply：密钥红线
├── commands/
│   ├── test.md                 # /test
│   ├── phase-check.md          # /phase-check
│   └── ingest.md               # /ingest
├── skills/
│   ├── local-dev/SKILL.md      # 本地启动与排障
│   └── rag-implementation/SKILL.md
├── agents/
│   ├── code-reviewer.md
│   └── security-reviewer.md
├── hooks.json
└── hooks/
    ├── block-dangerous-git.sh   # beforeShellExecution
    ├── block-secret-read.sh     # beforeReadFile
    └── audit-mcp.sh             # beforeMCPExecution
```

## 怎么用

### 1. 打开项目

用 Cursor 打开仓库根目录。`alwaysApply` 的 Rule 与 Hooks 自动生效。

### 2. 新人 / 新会话

先让 Agent 读 `AGENTS.md`，再按需 `@docs/design.md` 或具体模块。

### 3. Command 起手式

在 Agent 输入框输入：

- `/test` — 跑测试并修失败项
- `/phase-check` — 对照 Phase 1 验收标准列进度
- `/ingest` — 跑采集入库流水线

### 4. Skill 自动匹配

提到「Ollama 连不上」「RAG 怎么接」「/ask 没 sources」时，Agent 会加载对应 Skill。

### 5. Subagent 委派

交付前可说：

> 用 code-reviewer 审查本次 diff

涉及密钥 / 上线前可说：

> 用 security-reviewer 做安全检查

### 6. Hooks 行为

| 事件 | 脚本 | 行为 |
|------|------|------|
| `beforeShellExecution` | `block-dangerous-git.sh` | 拦截 `git push --force`、`git config` |
| `beforeReadFile` | `block-secret-read.sh` | 拦截读 `.env`、密钥文件 |
| `beforeMCPExecution` | `audit-mcp.sh` | 记入 `logs/mcp-audit.log`，不阻断 |

安全类 Hook 配置为 `failClosed: true`。

## 复制到自己的项目

1. 复制 `AGENTS.md` 骨架，改成你的技术栈与目录
2. 只保留 1 条 `alwaysApply` Rule（项目核心约束）
3. 按文件类型加 `globs` Rule（如 `**/*.py`）
4. 为最高频操作写 1 个 Command
5. 复杂流程再拆 Skill；交付审查再加 Subagent
6. 至少加一条 `beforeShellExecution` 安全 Hook

**反模式**：三处写同一段话 → 只留一处，其他地方写「见 `xxx.mdc`」。

## 相关

- 项目设计：[design.md](./design.md)
- 远程仓库：https://github.com/mr-ma-peng/mini-data-ai-platform

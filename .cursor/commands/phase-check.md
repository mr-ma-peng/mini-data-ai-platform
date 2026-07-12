# /phase-check — 对照当前 Phase 验收标准

对照 `docs/design.md` 检查 Phase 1 MVP 进度。

## 步骤

1. 阅读 `docs/design.md` 第 5 节 Phase 1 任务与验收标准
2. 检查代码现状：
   - `collector/` — RSS 源、分页/增量
   - `embedding/` — chunk、去重、入库
   - `api/main.py` — `/ask` 是否接入真实 RAG
   - `tests/` — 覆盖关键路径
3. 输出进度表：

| 任务 | 状态 | 证据（文件/函数） |
|------|------|-------------------|
| ... | ✅/🚧/❌ | ... |

4. 列出下一步 1–3 个最高优先级任务，附建议改动文件

## 约束

- 不提前规划 Phase 2+ 实现细节
- 建议保持 MVP 范围，避免过度设计

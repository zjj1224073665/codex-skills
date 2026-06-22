---
name: L3
description: "Emphasize Codex subagent usage. Use when the user invokes $L3 or asks Codex to prioritize subagents for complex, decomposable, review, planning, or implementation work."
---

# L3: Prefer Subagents For Complex Work

Codex 的 subagent（`~/.codex/agents/*.toml` 中定义，例如 architect / planner / requirement-implementer / security-reviewer / spec-fixer）核心优势是**每个子 agent 拥有全新的、干净的上下文窗口**。

## 为什么要用 subagent

1. **上下文隔离** — 主对话可能已经消耗了大量上下文（历史消息、文件内容、工具输出等），子 agent 从零开始，拥有完整的上下文容量，不会被无关信息干扰。
2. **专注度更高** — 子 agent 只看到分配给它的 prompt，不会被主对话中的其他任务、讨论、错误尝试等噪音分散注意力，输出质量更高。
3. **并行加速** — 多个子 agent 同时工作，互不干扰，总时间取决于最慢的那个子任务。
4. **失败隔离** — 某个子任务失败不会污染主对话的上下文，可以单独重试。
5. **上下文保护** — 子任务的大量中间输出（搜索结果、文件内容、长 diff、测试日志等）不会占用主对话的上下文窗口。
6. **沙箱隔离** — 像 architect / security-reviewer 这类 read-only sandbox 的 subagent，可以在不污染主会话写入语义的前提下做大规模分析。

**关键认知：当主对话上下文已经很长时，直接在主对话中做复杂操作，质量会下降。拉一个新的 subagent 来做，效果远好于在拥挤的上下文中继续。**

## 执行规则

- 遇到复杂、可拆、可并行的任务时，优先考虑把独立子任务派发给 subagent。
- 主对话负责把控目标、拆分任务、整合结果、处理关键路径；subagent 负责独立分析、实现、review 或验证。
- 不要把同一个问题重复派给多个 subagent，除非明确需要多视角 review。
- 不要把下一步立即依赖的阻塞任务丢给 subagent 后空等；关键路径工作应由主对话继续推进。
- 派发实现任务时，要明确文件/模块责任边界，并提醒 subagent 不要回滚其他人的改动。
- 派发 review/security/planning 任务时，要要求它给出具体文件、行号、风险等级和可执行建议。

结论：优先用 subagent 并行派发独立子任务执行；主对话保留协调权和最终判断权。

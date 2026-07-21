---
name: l3
description: "Emphasize Codex subagent usage. Use when the user invokes $L3 or asks Codex to prioritize subagents for complex, decomposable, review, planning, or implementation work."
---

**每个subagent 拥有全新的、干净的上下文窗口**：

1. **上下文隔离** — 主对话可能已经消耗了大量上下文（历史消息、文件内容等），subagent从零开始，拥有完整的上下文容量，不会被无关信息干扰
2. **专注度更高** — subagent只看到你给它的 prompt，不会被主对话中的其他任务、讨论、错误尝试等噪音分散注意力，输出质量更高
3. **并行加速** — 多个subagent同时工作，互不干扰，总时间取决于最慢的那个子任务
4. **失败隔离** — 某个subagent失败不会污染主对话的上下文，可以单独重试
5. **上下文保护** — subagent的大量中间输出（搜索结果、文件内容等）不会占用主对话的上下文窗口

**关键认知：当主对话上下文已经很长时，直接在主对话中做复杂操作，质量会下降。拉一个新的subagent来做，效果远好于在拥挤的上下文中继续。**

在执行复杂任务的时候，先主动拆分任务，然后每个子任务让一个subagent做，你只负责拆分任务和验收

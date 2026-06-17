---
name: luo-fengji-paper-writing
description: Luo-style 学术论文写作与 review 指南，适用于工程、应用 AI、能源预测、可解释预测、LLM/进化优化以及方法型 manuscript。用户要求 Luo Fengji / Luo teacher 风格论文写作、修改 introduction/abstract/contributions/method/experiments/conclusion、提升 reviewer-facing framing，或强化 application-driven academic clarity 时使用。也作为 paper-draft-orchestrator 和 paper-draft-worker run 内的 writing gate。
---

# Luo Fengji 论文写作

把这个 skill 当作 manuscript 写作和 review 的精简 gate。完整本地 Luo 写作指南在：

```text
/Users/junjiezhao/Library/CloudStorage/OneDrive-个人/AGENTS_/luo-paper-writing/SKILL.md
```

当任务需要细致 rewriting 或 reviewer-style diagnosis 时，先读取该文件并应用其中规则。轻量检查时，使用下面规则。

## 核心标准

为目标领域里负责任的 reviewer 写作。reviewer 应该能迅速理解：

1. 论文解决了什么真实工程或科学问题。
2. prior work 之后仍然留下什么 gap。
3. proposed method 改变了什么。
4. 这个改变为什么对 application 有意义。
5. 哪些 evidence 支持这些 claims。

如果一个段落不能回答以上任何一点，就修改、移动或删除它。

## Framing 规则

- 始终把 application 放在中心。不要让应用型论文读起来像一篇 generic computer-science technique note，最后才挂一个 application。
- 每个 contribution 都表达为：design choice + solved limitation + application benefit。
- 除非 citation evidence 支持，否则避免宽泛 novelty claims。
- 用具体 mechanism 替换模糊 benefits。
- 解释每个技术组件为什么对 target problem 有用。

可用句式：

```text
We develop [method/design] for [application]. Unlike [prior limitation], it [mechanism]. This helps [application need] by [benefit].
```

## 章节检查

### Abstract

包含 problem、gap、method、result 和 implication。不要写成 mini-method section。只有在数值已验证时才放入关键 numeric results。

### Introduction

按这个顺序组织：

1. application importance 和 operational need。
2. 按有意义的方法族归纳 literature status。
3. 精确 limitations。
4. proposed solution，以及它的 mechanism 为什么适配该 limitation。
5. 具体 contributions。

避免写 standard models、LLMs、optimization 或 metrics 的教程。

### Method

先讲 mechanism 和 component interaction，再讲 formulas、prompts、code restrictions、parsing details 或 edge cases。对于代表 design choice 的公式，要解释其 "why"。

### Experiments

使用叙事线：main performance、baselines、ablation、sensitivity、visualization 或 interpretation。每个 table 和 figure 都要连接到一个 claim。

### Conclusion

不要重复 abstract。说明本文开发了什么、关键已验证发现、application implications，以及真实 limitations 或 future work。

## Reviewer-Readability Checklist

返回 prose 前检查：

- target application 是否出现在 title、abstract、contribution list、method overview 和 experiments 中。
- 每个段落是否有明确角色：problem、gap、method、reason、evidence、implication，或应删除的细节。
- claims 是否有 evidence 和 citations 支持。
- 重复想法是否已压缩。
- terms 和 notation 是否一致。
- implementation details 是否干扰 core method。
- target-field reviewer 是否知道这一节为什么存在。

## 输出要求

修改或 review 文本时，提供：

1. 对主要写作问题的简短诊断。
2. 如果请求 revision，给出 polished academic English 版本。
3. 简短解释为什么修改后更强。
4. 未解决的事实检查，包括 missing citations、unsupported novelty 或 missing experiment numbers。

在 multi-agent paper run 内，把这些输出写到分配的 run 目录，而不是只在聊天中返回。

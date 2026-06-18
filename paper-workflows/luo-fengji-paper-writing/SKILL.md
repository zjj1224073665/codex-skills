---
name: luo-fengji-paper-writing
description: Luo-style 学术论文写作与 review 指南，适用于工程、应用 AI、能源预测、电价预测、可解释预测、LLM/进化优化、因子挖掘以及方法型 manuscript。用户要求 Luo Fengji / Luo teacher 风格论文写作、修改 introduction/abstract/contributions/method/experiments/conclusion、提升 reviewer-facing framing、强化 application-driven academic clarity，或参考 EPF/LLM 定稿与 revision 对话时使用。也作为 paper-draft-orchestrator 和 paper-draft-worker run 内的 writing gate。
---

# Luo Fengji 论文写作

把这个 skill 当作 manuscript 写作和 review 的精简 gate。目标不是把文章写得显得复杂，而是让负责任的 reviewer 快速看懂问题、gap、设计、证据和应用意义。

## 先读什么

轻量检查时，直接使用本文件规则。细致 rewriting 或 reviewer-style diagnosis 时，先读取完整本地 Luo 写作指南：

```text
/Users/junjiezhao/Library/CloudStorage/OneDrive-个人/AGENTS_/luo-paper-writing/SKILL.md
```

如果任务涉及 EPF、能源预测、LLM 生成预测模型、进化优化、可解释因子挖掘、贡献重写或 conclusion/future work，继续读取：

```text
references/luo-revision-principles.md
```

如果任务需要模仿这次修改后的成稿结构，查看定稿 PDF：

```text
references/final-manuscripts/electricity-price-forecasting-via-llm-revised-final.pdf
```

原始 revision 转写和经验文档已收在：

```text
references/source-index.md
references/revision-transcripts/
```

默认不要加载原始转写。只有在需要核对某条规则的来源、恢复具体讨论上下文，或用户明确要求参考对话记录时再读取。转写有 ASR 噪声，不要逐字模仿其中口语。

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
- 方法若具有通用性，把通用性作为 secondary implication。投能源、电力、工程应用期刊时，主线仍然是 target application。
- acronym、title、framework name 和核心术语要服务应用主线。不要让核心卖点看起来完全没有工程背景。

可用句式：

```text
We develop [method/design] for [application]. Unlike [prior limitation], it [mechanism]. This helps [application need] by [benefit].
```

## Luo Revision Gate

改稿前先问：

1. 这段是在解决 application problem，还是在科普通用 AI/optimization 概念。
2. 如果删掉 fancy words，核心意思是否仍然成立。
3. 这个 design choice 为什么对目标应用有帮助。
4. 术语、符号、图表标题和贡献点是否会让 reviewer 产生误解。
5. 引用是否支撑了明确论断，而不是为了显得有文献。

优先使用 plain academic English。避免用 big words 遮住逻辑，例如只说 transparency、robustness、semantic richness、pattern matching、decision support 而不解释具体机制。

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

Contribution list 必须实壮。每一点先说设计和好处，再必要时补技术名词。小技巧不要单独膨胀成一条贡献，除非它能解释清楚 application benefit 或可泛化价值。

### Method

先讲 mechanism 和 component interaction，再讲 formulas、prompts、code restrictions、parsing details 或 edge cases。对于代表 design choice 的公式，要解释其 "why"。

方法 overview 先给架构：关键模块是什么、每轮如何交互、最终产生什么。不要一进入 overview 就强调 metrics、实现语言、runtime 限制或 prompt 细节。实现约束只在它影响 method validity 或 reproducibility 时保留。

### Experiments

使用叙事线：main performance、baselines、ablation、sensitivity、visualization 或 interpretation。每个 table 和 figure 都要连接到一个 claim。

实验设置要回扣前文的 application motivation。dataset、features、regions、forecast horizons、hardware 和 implementation details 要放在读者需要的位置。图中文字必须能读，caption 要准确说明图中变量和 claim。

### Conclusion

不要重复 abstract。说明本文开发了什么、关键已验证发现、application implications，以及真实 limitations 或 future work。

Conclusion 应总结证据和观察，不要只写口水话。future work 要是能从本文打开的研究方向，不要只是换算法、换数据集、换更大模型这类小替换。

## Reviewer-Readability Checklist

返回 prose 前检查：

- target application 是否出现在 title、abstract、contribution list、method overview 和 experiments 中。
- 每个段落是否有明确角色：problem、gap、method、reason、evidence、implication，或应删除的细节。
- claims 是否有 evidence 和 citations 支持。
- 重复想法是否已压缩。
- terms 和 notation 是否一致。
- acronym 和变量是否会误导目标领域 reviewer。
- notation 是否避免把时间序列里的 time index 和优化里的 generation index 混淆。
- implementation details 是否干扰 core method。
- target-field reviewer 是否知道这一节为什么存在。

## 输出要求

修改或 review 文本时，提供：

1. 对主要写作问题的简短诊断。
2. 如果请求 revision，给出 polished academic English 版本。
3. 简短解释为什么修改后更强。
4. 未解决的事实检查，包括 missing citations、unsupported novelty 或 missing experiment numbers。

在 multi-agent paper run 内，把这些输出写到分配的 run 目录，而不是只在聊天中返回。

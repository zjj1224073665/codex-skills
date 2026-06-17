---
name: research-contribution-framing
description: 当用户想把一个技术方法、training trick、reward design、agent pipeline、evaluation protocol，或“这不就是 X 吗”的想法，转化成站得住的 research-paper positioning 时使用。适用于 contribution bullets、title/abstract/introduction framing、novelty claims、related-work defenses、reviewer-facing explanations，以及和 close prior work 的比较，尤其是 LLM、agent、RLHF、reward shaping、credit assignment 和 method-heavy papers。
---

# Research Contribution Framing

## 概览

使用这个 skill，把 implementation-level 的方法描述重新组织成 reviewer 能看懂、能接受的论文贡献。保持技术诚实：standard primitives 应该被明确命名，而 contribution 应放在真实的抽象层级上，例如 problem formulation、feedback construction、credit assignment、interaction protocol 或 evaluation design。

## 工作流

### 1. 区分 Primitive 和 Contribution

先从用户材料中抽取这些事实：

- target task、user scenario 或 scientific bottleneck。
- 现有 method family，以及它仍未解决的 limitation。
- 使用的 standard primitives，例如 PPO、DPO、REINFORCE、reward shaping、retrieval、prompting、search 或 simulation。
- proposed design choices，以及它们进入 pipeline 的位置。
- 已有 evidence：experiments、ablations、benchmark results、qualitative cases 或 failure analysis。
- closest prior work，以及 citations 是否需要验证。

明确写出这个区分：

```text
We use [standard primitive] as the optimization/mechanism layer. The contribution is [higher-level formulation/design], which changes [training signal / credit assignment target / interaction protocol / evaluation object].
```

如果用户要求针对某篇具体论文或缺失 citation 做 claim，先验证该论文，再做事实判断。未验证的相似性 claim 要标为 hypotheses。

### 2. 定位 Contribution

写作前先判断真实 contribution 位于哪里。常见位置：

- Problem formulation：命名一个 prior work 只隐式处理的 failure mode 或 task setting。
- Feedback construction：把 outcome、preference、critique 或 future trajectory information 转成可训练 signal。
- Credit assignment：决定哪个 action、response、query 或 module 接收 long-horizon feedback。
- Interaction protocol：改变谁行动、何时请求信息，或 multi-turn collaboration 如何展开。
- Optimization wrapper：围绕新的 signal、data source 或 rollout structure 使用 standard optimizer。
- Evaluation design：测量 single-turn metrics 或 final-task scores 看不到的 behavior。
- System integration：用 ablations 支持，将已知部件组合成一种新 capability。

使用这个句式：

```text
We propose [design/formulation] for [setting]. Unlike [prior family], which [limitation], it [mechanism]. This enables [benefit] because [causal reason].
```

### 3. 在正确层级命名 Idea

选择描述 design 作用的名称，而不是底层 commodity component 的名称。

好的名称指向：

- signal：future-aware feedback、trajectory-level preference、process-grounded reward。
- horizon：multi-turn credit assignment、long-horizon response valuation。
- behavior：active collaboration、query-aware refinement、uncertainty-driven intervention。
- training unit：response-level、query-level、dialogue-level、tool-call-level。

让命名可辩护：

- 标准 optimizers 和 algorithms 要朴素命名。
- 只有当 novelty 真正在 formulation、signal、protocol 或 evidence 上时，才为这些部分声称 novelty。
- 当 algorithmic core 是借来的，优先使用 "we instantiate"、"we construct"、"we operationalize" 或 "we formulate"。

### 4. 写 Contribution Bullets

每条 contribution bullet 都应包含 design、limitation 和 evidence。

使用这个模板：

```text
- We formulate [problem/object] as [new abstraction], addressing [limitation in prior work].
- We develop [method component] that [mechanism], allowing [capability] without [old assumption/cost].
- We provide [evaluation/analysis] showing [measured result], with ablations isolating [component].
```

避免只罗列 components。只有当一个 component 解决了明确 limitation，且论文能给出 evidence，它才构成 contribution。

### 5. 构建 Related-Work Defense

沿着能揭示真实差异的轴线比较 prior work：

- Training signal：labels、preferences、rewards、critiques、final outcome、future rollout、human feedback、environment feedback。
- Horizon：single-turn、step-level、episode-level、multi-turn、long-horizon。
- Credit target：token、response、query、action、tool call、dialogue state、policy。
- Supervision source：human、simulator、user model、external verifier、self-play、benchmark oracle。
- Optimizer：SFT、DPO、PPO、REINFORCE、search、filtering、reranking。
- Interaction role：passive responder、planner、active collaborator、tool user、question asker、controller。

防御性表述：

```text
Our method does not introduce a new policy-gradient optimizer. Instead, it introduces [signal/formulation/protocol], which can be optimized by [standard optimizers]. This distinction is important because prior work mainly changes [optimizer/model], whereas our bottleneck is [feedback/credit assignment/interaction].
```

如果某个 prior work 很接近，就引用它并收窄 claim。一篇强论文靠解释剩余差异站住，而不是隐藏最近邻。

### 6. 产出 Reviewer-Facing Output

让输出匹配用户请求：

- Brainstorming：给 2-4 个 framing options，每个包含 contribution locus、title phrase、risk 和 required evidence。
- Rewriting：给 polished title/abstract/introduction/contribution text，并附短 rationale。
- Novelty checking：列出 standard parts、genuine contribution candidates、close-prior-work risks 和 missing citations。
- Rebuttal 或 email：使用冷静、事实性的语言；区分 confirmed facts 和 inferred similarity。
- Paper draft：写 reviewer 能追溯到 experiments、ablations 或 citations 的 claims。

## Quality Gate

最终返回前检查：

- skeptical reviewer 会不会把它总结为 "just [standard primitive]"？如果会，补上 primitive/contribution split。
- 每个 novelty claim 是否绑定到具体 locus：problem、signal、credit assignment、protocol、evaluation 或 evidence。
- close prior works 是否已引用，或明确标记为 needing verification。
- contribution bullets 是否解释 design 为什么重要，而不只是列出实现内容。
- framing 是否在不过度声称 algorithmic originality 的前提下变强。

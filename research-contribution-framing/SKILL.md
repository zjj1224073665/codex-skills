---
name: research-contribution-framing
description: Use when the user wants to turn a technical method, training trick, reward design, agent pipeline, evaluation protocol, or "this is just X" idea into defensible research-paper positioning. Apply for contribution bullets, title/abstract/introduction framing, novelty claims, related-work defenses, reviewer-facing explanations, and comparisons against close prior work, especially in LLM, agent, RLHF, reward shaping, credit assignment, and method-heavy papers.
---

# Research Contribution Framing

## Overview

Use this skill to reframe a method from an implementation-level description into a reviewer-legible paper contribution. Preserve technical honesty: standard primitives should be named, while the contribution should be placed at the real abstraction level such as problem formulation, feedback construction, credit assignment, interaction protocol, or evaluation design.

## Workflow

### 1. Separate The Primitive From The Contribution

Start by extracting these facts from the user's material:

- Target task, user scenario, or scientific bottleneck.
- Existing method family and the limitation that remains.
- Standard primitives used, such as PPO, DPO, REINFORCE, reward shaping, retrieval, prompting, search, or simulation.
- Proposed design choices and where they enter the pipeline.
- Evidence already available: experiments, ablations, benchmark results, qualitative cases, or failure analysis.
- Closest prior work and whether citations need to be verified.

State the split explicitly:

```text
We use [standard primitive] as the optimization/mechanism layer. The contribution is [higher-level formulation/design], which changes [training signal / credit assignment target / interaction protocol / evaluation object].
```

If the user asks for claims against a specific paper or missing citation, verify the paper before making factual assertions. Mark unverified similarity claims as hypotheses.

### 2. Locate The Contribution

Classify the actual contribution before writing. Common loci:

- Problem formulation: naming a failure mode or task setting that prior work treats only implicitly.
- Feedback construction: turning outcome, preference, critique, or future trajectory information into a trainable signal.
- Credit assignment: deciding which action, response, query, or module receives long-horizon feedback.
- Interaction protocol: changing who acts, when information is requested, or how multi-turn collaboration unfolds.
- Optimization wrapper: using a standard optimizer around a new signal, data source, or rollout structure.
- Evaluation design: measuring behavior that single-turn metrics or final-task scores miss.
- System integration: combining known parts in a way that enables a new capability and is supported by ablations.

Use this sentence pattern:

```text
We propose [design/formulation] for [setting]. Unlike [prior family], which [limitation], it [mechanism]. This enables [benefit] because [causal reason].
```

### 3. Name The Idea At The Right Level

Choose names that describe the role of the design, not the commodity component underneath.

Good names point to:

- The signal: future-aware feedback, trajectory-level preference, process-grounded reward.
- The horizon: multi-turn credit assignment, long-horizon response valuation.
- The behavior: active collaboration, query-aware refinement, uncertainty-driven intervention.
- The unit of training: response-level, query-level, dialogue-level, tool-call-level.

Keep the naming defensible:

- Name standard optimizers and algorithms plainly.
- Claim novelty for the formulation, signal, protocol, or evidence only when that is where the novelty sits.
- Prefer "we instantiate", "we construct", "we operationalize", or "we formulate" when the algorithmic core is borrowed.

### 4. Write Contribution Bullets

Each contribution bullet should contain design, limitation, and evidence.

Use this template:

```text
- We formulate [problem/object] as [new abstraction], addressing [limitation in prior work].
- We develop [method component] that [mechanism], allowing [capability] without [old assumption/cost].
- We provide [evaluation/analysis] showing [measured result], with ablations isolating [component].
```

Avoid bullets that only list components. A component becomes a contribution only when it solves a named limitation and the paper can show evidence.

### 5. Build Related-Work Defense

Compare against prior work along axes that reveal the real distinction:

- Training signal: labels, preferences, rewards, critiques, final outcome, future rollout, human feedback, environment feedback.
- Horizon: single-turn, step-level, episode-level, multi-turn, long-horizon.
- Credit target: token, response, query, action, tool call, dialogue state, policy.
- Supervision source: human, simulator, user model, external verifier, self-play, benchmark oracle.
- Optimizer: SFT, DPO, PPO, REINFORCE, search, filtering, reranking.
- Interaction role: passive responder, planner, active collaborator, tool user, question asker, controller.

Defensive phrasing:

```text
Our method does not introduce a new policy-gradient optimizer. Instead, it introduces [signal/formulation/protocol], which can be optimized by [standard optimizers]. This distinction is important because prior work mainly changes [optimizer/model], whereas our bottleneck is [feedback/credit assignment/interaction].
```

If a prior work is close, cite it and narrow the claim. A strong paper survives by explaining the remaining difference, not by hiding the closest neighbor.

### 6. Produce Reviewer-Facing Output

Match the output to the user's request:

- For brainstorming: provide 2-4 framing options, each with contribution locus, title phrase, risk, and required evidence.
- For rewriting: provide polished title/abstract/introduction/contribution text plus a short rationale.
- For novelty checking: list standard parts, genuine contribution candidates, close-prior-work risks, and missing citations.
- For rebuttal or email: use calm, factual language; separate confirmed facts from inferred similarity.
- For a paper draft: write claims that a reviewer can trace to experiments, ablations, or citations.

## Quality Gate

Before finalizing, check:

- Would a skeptical reviewer summarize this as "just [standard primitive]"? If yes, add the primitive/contribution split.
- Is every novelty claim attached to a concrete locus: problem, signal, credit assignment, protocol, evaluation, or evidence?
- Are close prior works cited or explicitly marked as needing verification?
- Do the contribution bullets explain why the design matters, not only what was implemented?
- Is the framing stronger without overstating algorithmic originality?

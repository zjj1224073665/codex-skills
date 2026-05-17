---
name: luo-fengji-paper-writing
description: Luo-style academic paper writing and review guidance for engineering, applied AI, energy forecasting, interpretable forecasting, LLM/evolutionary optimization, and method-heavy manuscripts. Use when the user asks for Luo Fengji / Luo teacher style paper writing, revise introduction/abstract/contributions/method/experiments/conclusion, improve reviewer-facing framing, or enforce application-driven academic clarity. Also use as a writing gate inside paper-draft-orchestrator and paper-draft-worker runs.
---

# Luo Fengji Paper Writing

Use this skill as a concise gate for manuscript writing and review. The full local Luo writing guidance is stored at:

```text
/Users/junjiezhao/Library/CloudStorage/OneDrive-个人/AGENTS_/luo-paper-writing/SKILL.md
```

When a task requires detailed rewriting or reviewer-style diagnosis, read that file first and apply it. For lightweight checks, use the rules below.

## Core Standard

Write for a responsible reviewer in the target field. The reviewer should quickly understand:

1. What real engineering or scientific problem the paper solves.
2. What gap remains after prior work.
3. What the proposed method changes.
4. Why that change matters for the application.
5. What evidence supports the claim.

If a paragraph does not answer one of those points, revise, move, or delete it.

## Framing Rules

- Keep the application at the center. Do not make an applied paper read like a generic computer-science technique note with an application attached at the end.
- Express each contribution as: design choice + solved limitation + application benefit.
- Avoid broad novelty claims unless the citation evidence supports them.
- Replace vague benefits with concrete mechanisms.
- Explain why each technical component is useful for the target problem.

Useful pattern:

```text
We develop [method/design] for [application]. Unlike [prior limitation], it [mechanism]. This helps [application need] by [benefit].
```

## Section Checks

### Abstract

Include problem, gap, method, result, and implication. Do not write a mini-method section. Include key numeric results only when verified.

### Introduction

Use this order:

1. Application importance and operational need.
2. Literature status grouped by meaningful families.
3. Precise limitations.
4. Proposed solution and why its mechanism fits the limitation.
5. Concrete contributions.

Avoid tutorials on standard models, LLMs, optimization, or metrics.

### Method

Start with mechanism and component interaction before formulas, prompts, code restrictions, parsing details, or edge cases. Explain "why" around formulas that represent design choices.

### Experiments

Use a narrative: main performance, baselines, ablation, sensitivity, visualization or interpretation. Connect every table and figure to a claim.

### Conclusion

Do not repeat the abstract. State what was developed, the key verified findings, application implications, and real limitations or future work.

## Reviewer-Readability Checklist

Check before returning prose:

- Is the target application visible in the title, abstract, contribution list, method overview, and experiments?
- Does each paragraph have a clear role: problem, gap, method, reason, evidence, implication, or removable detail?
- Are claims supported by evidence and citations?
- Are repeated ideas compressed?
- Are terms and notation consistent?
- Are implementation details distracting from the core method?
- Would a target-field reviewer know why this section is in the paper?

## Output Expectations

When revising or reviewing text, provide:

1. A brief diagnosis of the main writing problem.
2. A revised version in polished academic English, if revision is requested.
3. A short explanation of why the revision is stronger.
4. Unresolved factual checks, including missing citations, unsupported novelty, or missing experiment numbers.

Inside a multi-agent paper run, write these outputs to the assigned run directory instead of only returning them in chat.

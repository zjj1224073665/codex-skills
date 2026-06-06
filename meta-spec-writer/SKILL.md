---
name: meta-spec-writer
description: Use when the user asks to write, review, improve, or turn requirements into a meta spec prompt for Codex to modify repository specs, architecture docs, AGENTS.md instructions, or implementation-task specs. This skill helps produce spec-first Codex prompts with clear scope, semantic contracts, constraints, examples, and stop-and-confirm rules.
---

# Meta Spec Writer

Use this skill to draft or review a **meta spec**: a prompt meant to instruct Codex how to update project specs. A meta spec is not just a feature request. It should freeze the intended semantics, edit scope, invalid shortcuts, and acceptance criteria so a later Codex run can safely modify the repo's specs.

## Workflow

1. Read the user's requested change, the target repo's `AGENTS.md`, and the relevant files under `specs/`, `meta_specs/`, or equivalent docs.
2. Identify whether the user wants spec-only work, code changes, tests, or a staged flow. If this is unclear and the answer changes what files may be edited, stop and ask.
3. Draft the meta spec in plain language. Prefer exact file names, concrete formulas, examples, defaults, legal values, and explicit illegal behavior over broad phrases like "optimize", "support", or "make robust".
4. Include examples only where they disambiguate behavior. Keep examples small enough that an implementer can manually check the expected result.
5. If the change touches public APIs, artifacts, metadata, backtest semantics, or compatibility rules, spell out both the new allowed path and the old path that must be removed or rejected.

## Recommended Shape

A strong meta spec usually has these sections:

- **Title**: one line naming the spec change.
- **Scope**: exact files to edit; say whether to edit only specs or also code/tests.
- **Goal**: the before/after semantic model, often as a short pipeline diagram.
- **Hard Constraints**: non-negotiable defaults, invariants, illegal shortcuts, and failure modes.
- **Definitions**: names and meanings of any new concepts, columns, config fields, APIs, or artifacts.
- **Allowed Values**: whitelists, fixed parameter levels, defaults, and where each config is declared.
- **Execution Semantics**: ordering, data alignment, missing-data behavior, batching semantics, CPU/GPU parity, or streaming parity if relevant.
- **Migration/Removal**: old APIs, fields, or docs that must be deleted or explicitly rejected.
- **Examples**: minimal code, tables, formulas, or timeline examples that make edge cases concrete.
- **Acceptance Checks**: what a reviewer can inspect in the resulting specs to know the prompt was followed.

Do not force every section if the task is small. Keep the shape proportional to the blast radius.

## Writing Rules

- Make the meta spec actionable for another Codex run: use imperatives like "modify", "delete", "treat as invalid", "must read from", and "do not silently fall back".
- Separate semantics from implementation. Freeze implementation details only when different implementations would otherwise produce different behavior.
- Pin source-of-truth boundaries: where config lives, who reads it, which artifacts may contain it, and what happens if it appears elsewhere.
- State defaults and missing-value behavior explicitly. If invalid input should fail, say where it should fail and that silent fallback is not allowed.
- Batch semantics matter. If one run evaluates many items, say what can be shared and what remains per-item.
- Prefer "plain language + one example" over abstract rules alone.
- Keep project-specific facts in the generated meta spec, not in this skill. Always re-read the repo's current docs before drafting.

## Stop And Confirm

Before writing or changing a meta spec, stop and ask the user when any of these are unclear:

- Which repo or spec files are in scope.
- Whether this turn should edit only docs/specs or also implementation and tests.
- Which behavior is the canonical truth when existing specs conflict.
- Whether old APIs/artifacts should remain backward compatible or become illegal.
- Whether a parameter should be freely tunable or constrained to a whitelist.
- Whether an example should be copied into the skill/output when it may be confidential or too project-specific.

If the uncertainty is only about local file permissions or sandbox approval, follow the normal tool approval flow instead of asking a product question.

## Mini Examples

Spec-only scope:

```markdown
请修改本 repo 的 spec 文档，先只改 spec，不改代码和测试。

重点修改：
- `specs/02_position_engine.md`
- `specs/07_pipeline.md`
```

Stable source-of-truth boundary:

```markdown
`normalization_config` 的声明入口固定为 `source.py` 顶层模块级静态字面量 dict。
`meta.json` / `FactorMeta` 不定义这个字段；出现就算非法 artifact，直接报错。
```

Invalid fallback:

```markdown
`cost_mode="full"` 必须提供并校验 spread。缺 spread 直接报错，不能静默退化成 fee-only。
```

Batch parity:

```markdown
批量路径中，每个因子的结果必须和“这个因子单独按自己的配置跑”一致；共享的只能是 features、prices、spread、target_index 等准备工作。
```

## Reference Example

For a complete high-quality example, read `references/normalization_config_meta_spec.md`. It shows a large spec-first prompt with exact target files, pipeline semantics, config ownership, whitelists, invalid artifact rules, examples, and batch/GPU parity requirements.

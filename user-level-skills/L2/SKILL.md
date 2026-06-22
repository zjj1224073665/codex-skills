---
name: L2
description: "Run the L2 workflow: implement the user's requirement, leave changes unstaged, then invoke Codex CLI to review the unstaged git diff for P0 completion blockers. Use when the user invokes $L2 or asks for the L2/codex-review workflow."
---

# L2: Implement, Then Codex Review

When the user invokes `$L2`, treat the rest of their request as the original requirement. Preserve that requirement byte-for-byte; quote it verbatim in the Codex review prompt.

## Workflow

### 1. Implement the requirement

- Understand the requirement and ask only genuinely blocking clarification questions.
- Implement the requested change using the repo's existing patterns.
- You may use subagents for independent implementation, planning, or review work when the task is complex and decomposable.
- Do not commit. Leave changes as working-tree edits so they appear in `git diff`.
- If a commit was already made during the task, warn that the default L2 review only sees unstaged changes and ask whether to soft-reset or review a specific commit range.

### 2. Check that unstaged changes exist

When implementation is done, run:

```bash
git diff --quiet && { echo "no unstaged changes detected"; exit 0; }
```

- Use `git diff --quiet` without `--staged` or `HEAD`; this checks only unstaged working-tree changes.
- If exit code is 0, tell the user `no unstaged changes detected` and stop.
- Do not write the diff to a patch file. Codex will read `git diff` itself.

### 3. Run Codex auto-review

Pass only the original requirement plus navigation instructions. Let Codex read the diff and related files itself with `git diff`, `cat`, and `rg`.

Use `printf '%s'` so shell metacharacters inside the requirement are not expanded:

```bash
{
  printf 'review 一下未提交的改动是否完成了下面的需求：\n\n"%s"\n\n你 CWD 就是项目根。请自己用：\n- git diff 看未提交改动\n- cat / rg 读相关文件做联动检查。\n\n## 严重度门槛（硬性要求）\n\n只输出 **P0** 问题。P0 的定义严格限定为以下三类：\n1. 需求里明确要求的功能没实现 / 实现错了\n2. 改动引入了功能性 bug（跑起来会报错、行为和需求矛盾、破坏了已有功能）\n3. 改动里有明显的安全漏洞（注入、鉴权绕过、密钥泄露这种，不是泛泛的"建议加校验"）\n\n**禁止输出以下内容**（哪怕你觉得很有道理）：\n- 代码风格、命名、格式\n- 重构建议、抽象层次、设计模式\n- "可以更健壮"、"建议加错误处理"、"可以加日志"、"可以加测试"\n- 性能优化（除非需求明确要求性能）\n- 未来可扩展性、边界情况补强\n- 文档 / 注释缺失\n- 任何 nice-to-have\n\n如果没有 P0 问题，**只输出一行**：`no blocking issues — 需求已完成`。不要补充"但是建议..."、"另外可以考虑..."。\n\n如果有 P0，按这个格式输出，每条都要给出"为什么这是 P0 而不是 nice-to-have"的一句话理由：\n```\n[P0] <一句话问题描述>\n  位置: <file:line>\n  为什么阻塞: <对照需求的哪一条 / 会导致什么功能性后果>\n```\n' "$ORIGINAL_REQUIREMENT"
} | codex exec \
  --skip-git-repo-check \
  --dangerously-bypass-approvals-and-sandbox \
  -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  2>/dev/null
```

Notes:

- `$ORIGINAL_REQUIREMENT` must be the user's exact text.
- `2>/dev/null` hides Codex stderr and leaves stdout for the user.
- `--dangerously-bypass-approvals-and-sandbox` avoids Codex's bwrap sandbox failures in environments where loopback setup is unavailable. The review prompt is read-oriented, but still inspect output carefully before acting on it.

### 4. Display Codex output verbatim

Show the complete Codex stdout to the user as-is. Do not summarize, filter, re-rank, apply fixes, commit, or decide next steps. Stop and wait for the user's instruction.

## Edge Cases

- **Empty diff after implementation**: tell the user the workflow produced no changes and stop.
- **Implementation requires commits**: Codex only sees unstaged changes by default. Add explicit review scope such as `git diff <base>..HEAD` plus `git diff`, after confirming the base with the user.
- **Codex CLI missing or errors**: surface the error verbatim; do not retry silently.
- **Requirement contains shell-special characters**: the `printf '%s' "$ORIGINAL_REQUIREMENT"` form handles this. If using a heredoc instead, use `<<'EOF'`.

---
name: paper-draft-orchestrator
description: 面向科研论文初稿生成的上下文安全 orchestrator。用于创建、继续或管理基于 subagent 的多智能体论文写作流程，尤其适合 orchestrator/subagent 写论文、manuscript first draft、逐节起草、从文献到论文的流水线，以及需要避免长任务污染上下文的场景。
---

# 论文初稿 Orchestrator

把这个 skill 当作长周期论文写作任务的主协调器。orchestrator 不应该亲自写完整论文章节，而应该创建并维护 run 目录，把边界清楚的任务分配给 subagent，在循环中只读取精简 handoff 文件，并用文件作为共享记忆来保护上下文。

## 必要配套 Skills

可用时，要求被 spawn 的 subagent 使用：

- `$paper-draft-worker`：处理有边界的 inventory、evidence、citation、outline、section writing、review、revision 和 assembly 任务。
- `$luo-fengji-paper-writing`：把关审稿人可读性、贡献表达、章节逻辑和应用工程类论文写作风格。
- `$research-contribution-framing`：处理 claim map、贡献点、novelty positioning、related-work defense 和 reviewer-facing framing。

如果这些 skills 不可用，就把关键要求内联进 subagent prompt：任务必须有边界、只能写 run 目录、claim 必须 evidence-first、citation 必须核验、要区分 contribution 和 primitive，并符合 Luo-style reviewer readability。

## Run 目录

创建或复用一个固定 run 目录：

```text
paper_runs/<run_id>/
  inputs/
    paper_brief.md
    target_venue.md
    raw_notes/
    figures/
    tables/
    bib/
  state/
    status.json
    recent_summary.md
    section_contracts.json
    evidence_ledger.jsonl
    citation_ledger.jsonl
    unresolved_questions.md
  rounds/
    round_00/
      task.md
      outputs/
        handoff_summary.md
        review.md
  draft/
    outline.md
    abstract.md
    introduction.md
    related_work.md
    method.md
    experiments.md
    conclusion.md
    full_draft.tex
  reviews/
```

如果用户没有提供 run id，就根据当前日期时间创建一个。所有 agent 只能写入 `ACTIVE_RUN_ID`。

## 调度规则

- 保持 orchestrator 上下文尽量小。常规轮次只读取 `state/status.json`、`state/recent_summary.md`、`state/unresolved_questions.md` 和各 subagent 的 `handoff_summary.md`。
- 不要查看完整章节草稿，除非正在做最终整合、排查已报告的问题，或用户明确要求。
- 为每个有边界的任务 spawn 一个短生命周期 subagent。不要让一个 subagent 写完整篇论文。
- 只有任务相互独立时才并行 spawn subagent，例如分别检查 citation、从不同材料集抽取 evidence。
- 要求每个 subagent 把输出写到自己负责的 `round_NN/outputs/`，只写被分配的 `draft/` 文件，只追加该任务允许追加的 ledger。
- 把 `evidence_ledger.jsonl` 和 `citation_ledger.jsonl` 当作 claim 和 citation 的事实依据。没有支持的 claim 必须保留标记。
- 绝不允许 agent 编造实验数字、数据集事实、论文标题、BibTeX key、reviewer comment 或 citation。

## 状态所有权

- orchestrator 拥有 `state/status.json`、`state/recent_summary.md` 和 `state/unresolved_questions.md`。
- worker 可以写自己负责的 `rounds/ROUND_ID/outputs/` 文件和被分配的 `draft/` 文件。
- worker 只有在任务明确要求时，才可以追加 `state/evidence_ledger.jsonl`、`state/citation_ledger.jsonl` 和任务相关 ledger。
- worker 不应该重写 `status.json` 或 `recent_summary.md`；需要改动全局状态时，在 `handoff_summary.md` 里提出。
- 每个 worker round 结束后，orchestrator 读取 handoff、验证 artifact，然后更新全局状态。

## 辅助脚本

只把内置脚本用于确定性的 housekeeping：

- `scripts/init_run.py` 创建 run scaffold。
- `scripts/validate_run.py` 检查 run 结构、JSON/JSONL ledger、section contract 引用、handoff 和未解决标记。

不要把调度判断交给脚本。主 agent 应该自己决定下一步任务，写出有边界的 worker prompt，spawn subagent，读取精简 handoff，并推进状态。

## 阶段循环

按顺序运行这些阶段；只有在所需 artifact 已存在且质量足够时才跳过。

1. `input_inventory`：盘点 brief、notes、papers、figures、tables、code outputs、experiment logs 和缺失输入。
2. `evidence_and_citation_build`：构建或更新 `evidence_ledger.jsonl` 和 `citation_ledger.jsonl`。
3. `claim_map_and_storyline`：生成一句话 sell point、gap、contribution map 和有 evidence 支持的 claims。
4. `outline`：创建 `draft/outline.md` 和 `state/section_contracts.json`。
5. `section_drafting`：根据 section contracts 和 ledgers，为每个章节分配一个 worker。
6. `internal_review`：分配 reviewer workers，检查逻辑、unsupported claims、venue fit、notation、重复内容和 Luo-style framing。
7. `revision`：根据 review findings 分配有目标的 revision 任务。
8. `final_assembly`：把各章节整合为 `full_draft.tex` 或用户要求的 manuscript 格式，不新增 claim。

每个阶段结束后，更新 `state/status.json`、`state/recent_summary.md` 和 `state/unresolved_questions.md`。

## Subagent Prompt 模板

spawn worker 时使用这个形状：

```text
Use $paper-draft-worker and $luo-fengji-paper-writing.
Use $research-contribution-framing when TASK_KIND is claim_map, outline, section_write for introduction/related_work, review, or revise.

ACTIVE_RUN_ID=<paper_runs/run_id>
ROUND_ID=round_NN
TASK_KIND=<inventory|evidence|citation|claim_map|outline|section_write|review|revise|assemble>
TARGET_SECTION=<optional>

You are not alone in this run. Other agents may update different files. Do not revert unrelated edits.
Write only inside ACTIVE_RUN_ID.
Read the relevant state files and the specific inputs needed for this task.
Do not write a whole paper unless TASK_KIND=assemble.
Every claim must be backed by evidence_ledger or marked [EVIDENCE_NEEDED].
Every citation must be backed by citation_ledger or marked [CITATION_NEEDED].
Do not rewrite state/status.json, state/recent_summary.md, or state/unresolved_questions.md; request state updates in handoff_summary.md.
End by writing rounds/ROUND_ID/outputs/handoff_summary.md.

Task:
<bounded task>
```

## Status 文件

维护 `state/status.json`，让它保持精简、机器可读：

```json
{
  "run_id": "paper_runs/example",
  "stage": "section_drafting",
  "round": 4,
  "target_venue": "unknown",
  "sections": {
    "introduction": "drafted",
    "method": "pending"
  },
  "open_blockers": [
    "Missing numeric results for Table 2"
  ],
  "last_updated": "YYYY-MM-DD"
}
```

## Handoff 纪律

每个 subagent handoff 必须回答：

- 完成了什么。
- 改了哪些文件。
- 新增或修改了哪些 claims。
- 使用了哪些 evidence 和 citations。
- 哪些 claims 仍然保留 `[EVIDENCE_NEEDED]` 或 `[CITATION_NEEDED]`。
- 下一个 agent 应该做什么。

保持 `recent_summary.md` 足够短，让新的 orchestrator 不读完整 run 也能继续。

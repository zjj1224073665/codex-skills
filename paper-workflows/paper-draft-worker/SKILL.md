---
name: paper-draft-worker
description: 多智能体科研论文写作中的有边界 worker skill。用于 paper-drafting run 内的单一子任务，例如 input inventory、evidence ledger 构建、citation checking、claim mapping、outline creation、section drafting、reviewer-style critique、targeted revision，或在 ACTIVE_RUN_ID 下做 final assembly。
---

# 论文初稿 Worker

当你作为短生命周期论文写作 subagent 工作时使用这个 skill。一次只完成一个有边界的任务，把持久 artifact 写入 run 目录，并用精简 handoff 交接。不要把一个有边界的任务扩展成整篇论文写作。

## 必要输入

预期 orchestrator 会提供：

```text
ACTIVE_RUN_ID=paper_runs/<run_id>
ROUND_ID=round_NN
TASK_KIND=<inventory|evidence|citation|claim_map|outline|section_write|review|revise|assemble>
TARGET_SECTION=<optional>
```

如果缺少 `ACTIVE_RUN_ID`，停止并要求补充。绝不要写到 `ACTIVE_RUN_ID` 之外。

## 首要动作

1. 读取相关 state 文件：
   - `state/status.json`
   - `state/recent_summary.md`
   - `state/unresolved_questions.md`
   - 起草、review 或 revision 章节时读取 `state/section_contracts.json`
   - 生成 claim 时读取 `state/evidence_ledger.jsonl` 和 `state/citation_ledger.jsonl`
2. 只读取当前任务需要的 input 文件。
3. 如果 `rounds/ROUND_ID/outputs/` 不存在，创建它。
4. 写作、review 或 revision prose 时使用 `$luo-fengji-paper-writing`。
5. `claim_map`、`outline`、novelty-sensitive `section_write`，以及涉及 contributions 或 related work 的 review 任务，使用 `$research-contribution-framing`。

## 硬规则

- 只写入 `ACTIVE_RUN_ID`。
- 不要编造 data、results、citations、datasets、related-work claims、reviewer feedback 或 novelty claims。
- 不受支持的 claim 标记为 `[EVIDENCE_NEEDED]`。
- 未核验的 citation 标记为 `[CITATION_NEEDED]`。
- 保留其他 agent 的工作。不要 revert 无关文件。
- 输出必须确定、基于文件。下一个 agent 应该能靠文件继续，而不是依赖聊天历史。
- 论文正文使用清晰的学术英语；notes 和 ledgers 保持简洁。
- 不要重写 `state/status.json`、`state/recent_summary.md` 或 `state/unresolved_questions.md`；需要这些改动时写进 `handoff_summary.md`。
- 只有当任务要求时才追加 ledger。除非 orchestrator 明确要求，不要重写 ledger 历史。

## 任务模式

### inventory

盘点可用材料。写 `rounds/ROUND_ID/outputs/inventory.md`，并在 `handoff_summary.md` 中给出建议的 `recent_summary.md` 更新。

记录：

- brief、target venue、page limit 和 intended field。
- 可用 notes、figures、tables、code、experiments 和 bibliography files。
- 缺失或有歧义的输入。
- 是否已经存在 manuscript draft。

### evidence

从 notes、tables、figures、logs 和已有 draft 中抽取 evidence。更新 `state/evidence_ledger.jsonl`。

每行使用一个 JSON object：

```json
{"claim_id":"E001","claim":"...","source_file":"...","figure_or_table":"...","experiment_id":"...","confidence":"high|medium|low","usable_in_section":["experiments"],"notes":"..."}
```

只记录 source 真正支持的内容。如果数值不确定，就记录不确定性，不要把它润色成确定结论。

### citation

构建或检查 `state/citation_ledger.jsonl`。只有在用户要求当前验证，或本地 bibliography 材料不足且 citation accuracy 很重要时，才使用浏览。

每行使用一个 JSON object：

```json
{"citation_id":"C001","key":"...","claim":"...","title":"...","source":"bib|pdf|web|notes","verified":true,"notes":"..."}
```

不要创建假的 BibTeX keys。如果 key 缺失，标记为 `[CITATION_KEY_NEEDED]`。

### claim_map

写这个任务前先使用 `$research-contribution-framing`。

写 `rounds/ROUND_ID/outputs/claim_map.md`，并在 `handoff_summary.md` 中给出建议的 `recent_summary.md` 更新。

包括：

- 一句话 sell point："This paper develops X for Y because Z remains difficult."
- target reviewer 和 venue framing。
- problem、gap、method mechanism、application benefit 和 evidence。
- contribution bullets，形式是：design choice + solved limitation + application benefit。
- 过强或尚未支持的 claims。

### outline

使用 `$research-contribution-framing`，确保 section contracts 绑定到站得住的 contribution claims。

写 `draft/outline.md` 并更新 `state/section_contracts.json`。

每个 section contract 应包含：

```json
{
  "section": "introduction",
  "purpose": "...",
  "must_make_claims": ["E001"],
  "must_use_citations": ["C001"],
  "avoid": ["generic LLM tutorial"],
  "open_questions": []
}
```

### section_write

只写 `TARGET_SECTION`，通常写到 `draft/<section>.md`，除非 run 指定使用 LaTeX。

写之前：

- 读取该 section 的 contract。
- 只读取相关 ledger entries 和 source materials。
- 保持 application framing 和 reviewer readability。

写作时：

- 从读者需要出发，不要从实现细节出发。
- 把每个技术选择和 application problem 联系起来。
- 只有 citation 已被 `citation_ledger` 支持时，才使用 citation placeholder。
- 用 `[EVIDENCE_NEEDED]` 或 `[CITATION_NEEDED]` 保留未解决缺口。

### review

写 `rounds/ROUND_ID/outputs/review.md`。优先列问题，不要写表扬。

检查：

- 不受支持或夸大的 claims。
- 缺失 citations 和薄弱 novelty statements。
- section logic 和 paragraph roles。
- application framing 是否被 generic method exposition 淹没。
- notation、terminology consistency 和重复内容。
- experiments 是否回答了 contributions。

### revise

根据 review file 做有目标的编辑。不要重写无关章节。除非存在支持性的 ledger entry，否则保留 claim markers。

### assemble

从已有章节整合用户要求的 manuscript 格式。不要新增 claims。解决 headings、terminology、labels、references 和重复文本问题。写 `draft/full_draft.tex` 或用户要求的输出文件。

## Handoff Summary

每个任务结束时写 `rounds/ROUND_ID/outputs/handoff_summary.md`：

```text
# Handoff Summary

Task:
Files changed:
Claims added or changed:
Evidence used:
Citations used:
Unresolved evidence gaps:
Unresolved citation gaps:
Next recommended task:
```

保持 handoff 简短。orchestrator 可能只读取这个文件。

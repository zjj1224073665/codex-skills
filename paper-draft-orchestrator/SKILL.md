---
name: paper-draft-orchestrator
description: Context-safe orchestrator for generating scientific paper drafts with short-lived subagents and a persistent run directory. Use when the user asks to create, continue, or manage a multi-agent research-paper drafting workflow, especially for "orchestrator/subagent" paper writing, manuscript first drafts, section-by-section drafting, literature-to-draft pipelines, or avoiding context corruption during long academic writing tasks.
---

# Paper Draft Orchestrator

Use this skill as the main coordinator for a long paper-writing run. The orchestrator should not write full manuscript sections. It should create and maintain the run directory, assign bounded tasks to subagents, read only compact handoff files during the loop, and preserve context by using files as the shared memory.

## Required Companion Skills

When available, instruct spawned subagents to use:

- `$paper-draft-worker` for bounded inventory, evidence, citation, outlining, section-writing, review, revision, and assembly tasks.
- `$luo-fengji-paper-writing` for reviewer-facing framing, contribution clarity, section logic, and applied-engineering writing style.

If those skills are unavailable, inline their key requirements in the subagent prompt: bounded task, run-directory-only writes, evidence-first claims, citation verification, and Luo-style reviewer readability.

## Run Directory

Create or reuse one fixed run directory:

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

If the user does not provide a run id, create one from the current date/time. All agents must write only inside `ACTIVE_RUN_ID`.

## Orchestration Rules

- Keep the orchestrator context small. During normal rounds, read only `state/status.json`, `state/recent_summary.md`, `state/unresolved_questions.md`, and each subagent's `handoff_summary.md`.
- Do not inspect full section drafts unless running final integration, checking a reported problem, or the user asks.
- Spawn short-lived subagents for one bounded task at a time. Do not ask one subagent to write the whole paper.
- Prefer parallel subagents only for independent tasks, such as citation checking and evidence extraction from separate material sets.
- Require each subagent to write all outputs under its assigned `round_NN/outputs/` directory and, when appropriate, update `state/` or `draft/`.
- Treat `evidence_ledger.jsonl` and `citation_ledger.jsonl` as the authority for claims and citations. Unsupported claims must remain marked.
- Never allow an agent to invent experimental numbers, dataset facts, paper titles, BibTeX keys, reviewer comments, or citations.

## Stage Loop

Run these stages in order, skipping only when the required artifacts already exist and are adequate.

1. `input_inventory`: catalog briefs, notes, papers, figures, tables, code outputs, experiment logs, and missing inputs.
2. `evidence_and_citation_build`: build or update `evidence_ledger.jsonl` and `citation_ledger.jsonl`.
3. `claim_map_and_storyline`: produce the one-sentence sell point, gap, contribution map, and evidence-backed claims.
4. `outline`: create `draft/outline.md` and `state/section_contracts.json`.
5. `section_drafting`: assign one section per worker, using section contracts and ledgers.
6. `internal_review`: assign reviewer workers to check logic, unsupported claims, venue fit, notation, repetition, and Luo-style framing.
7. `revision`: assign targeted revision tasks from review findings.
8. `final_assembly`: integrate sections into `full_draft.tex` or the requested manuscript format, without adding new claims.

After each stage, update `state/status.json`, `state/recent_summary.md`, and `state/unresolved_questions.md`.

## Subagent Prompt Template

Use this shape when spawning a worker:

```text
Use $paper-draft-worker and $luo-fengji-paper-writing.

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
End by writing rounds/ROUND_ID/outputs/handoff_summary.md.

Task:
<bounded task>
```

## Status File

Maintain `state/status.json` with compact machine-readable state:

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

## Handoff Discipline

Every subagent handoff must answer:

- What was completed.
- Which files were changed.
- Which claims were added or modified.
- Which evidence and citations were used.
- Which claims remain `[EVIDENCE_NEEDED]` or `[CITATION_NEEDED]`.
- What the next agent should do.

Keep `recent_summary.md` short enough for a fresh orchestrator to continue without reading the full run.

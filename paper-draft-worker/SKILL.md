---
name: paper-draft-worker
description: Bounded worker skill for multi-agent scientific manuscript drafting. Use inside a paper-drafting run when Codex is asked to perform exactly one subtask such as input inventory, evidence ledger construction, citation checking, claim mapping, outline creation, section drafting, reviewer-style critique, targeted revision, or final assembly under an ACTIVE_RUN_ID.
---

# Paper Draft Worker

Use this skill when acting as a short-lived paper-writing subagent. Complete one bounded task, write durable artifacts into the run directory, and hand off compactly. Do not turn a bounded task into whole-paper authorship.

## Required Inputs

Expect the orchestrator to provide:

```text
ACTIVE_RUN_ID=paper_runs/<run_id>
ROUND_ID=round_NN
TASK_KIND=<inventory|evidence|citation|claim_map|outline|section_write|review|revise|assemble>
TARGET_SECTION=<optional>
```

If `ACTIVE_RUN_ID` is missing, stop and ask for it. Never write outside `ACTIVE_RUN_ID`.

## First Actions

1. Read the relevant state files:
   - `state/status.json`
   - `state/recent_summary.md`
   - `state/unresolved_questions.md`
   - `state/section_contracts.json` when drafting, reviewing, or revising sections
   - `state/evidence_ledger.jsonl` and `state/citation_ledger.jsonl` when making claims
2. Read only the input files needed for the assigned task.
3. Create `rounds/ROUND_ID/outputs/` if it does not exist.
4. Use `$luo-fengji-paper-writing` when writing, reviewing, or revising prose.

## Hard Rules

- Write only inside `ACTIVE_RUN_ID`.
- Do not invent data, results, citations, datasets, related-work claims, reviewer feedback, or novelty claims.
- Mark unsupported claims as `[EVIDENCE_NEEDED]`.
- Mark unverified citations as `[CITATION_NEEDED]`.
- Preserve other agents' work. Do not revert unrelated files.
- Keep outputs deterministic and file-based. The next agent should be able to continue from files, not chat history.
- Use clear academic English for manuscript text, but keep notes and ledgers concise.

## Task Modes

### inventory

Catalog available material. Write `rounds/ROUND_ID/outputs/inventory.md` and update `state/recent_summary.md`.

Capture:

- Brief, target venue, page limit, and intended field.
- Available notes, figures, tables, code, experiments, and bibliography files.
- Missing or ambiguous inputs.
- Whether a manuscript draft already exists.

### evidence

Extract evidence from notes, tables, figures, logs, and existing drafts. Update `state/evidence_ledger.jsonl`.

Use one JSON object per line:

```json
{"claim_id":"E001","claim":"...","source_file":"...","figure_or_table":"...","experiment_id":"...","confidence":"high|medium|low","usable_in_section":["experiments"],"notes":"..."}
```

Only record what the source supports. If a numeric value is uncertain, record the uncertainty instead of smoothing it over.

### citation

Build or check `state/citation_ledger.jsonl`. Use browsing only when the user requested current verification or when local bibliographic material is insufficient and citation accuracy matters.

Use one JSON object per line:

```json
{"citation_id":"C001","key":"...","claim":"...","title":"...","source":"bib|pdf|web|notes","verified":true,"notes":"..."}
```

Do not create fake BibTeX keys. If the key is missing, mark it as `[CITATION_KEY_NEEDED]`.

### claim_map

Write `rounds/ROUND_ID/outputs/claim_map.md` and update `state/recent_summary.md`.

Include:

- One-sentence sell point: "This paper develops X for Y because Z remains difficult."
- Target reviewer and venue framing.
- Problem, gap, method mechanism, application benefit, and evidence.
- Contribution bullets in the form: design choice + solved limitation + application benefit.
- Claims that are too strong or not yet supported.

### outline

Write `draft/outline.md` and update `state/section_contracts.json`.

Each section contract should include:

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

Write only `TARGET_SECTION`, normally under `draft/<section>.md` unless the run specifies LaTeX.

Before writing:

- Read that section's contract.
- Read only the relevant ledger entries and source materials.
- Preserve application framing and reviewer readability.

During writing:

- Start with the reader's need, not implementation details.
- Tie each technical choice to the application problem.
- Use citation placeholders only when backed by `citation_ledger`.
- Keep unresolved gaps visible with `[EVIDENCE_NEEDED]` or `[CITATION_NEEDED]`.

### review

Write `rounds/ROUND_ID/outputs/review.md`. Prioritize issues, not praise.

Check:

- Unsupported or exaggerated claims.
- Missing citations and weak novelty statements.
- Section logic and paragraph roles.
- Application framing versus generic method exposition.
- Notation, terminology consistency, and repeated ideas.
- Whether experiments answer the contributions.

### revise

Make targeted edits based on a review file. Do not rewrite unrelated sections. Preserve claim markers unless the supporting ledger entry exists.

### assemble

Assemble the requested manuscript format from existing sections. Do not add new claims. Resolve headings, terminology, labels, references, and duplicated text. Write `draft/full_draft.tex` or the requested output file.

## Handoff Summary

End every task by writing `rounds/ROUND_ID/outputs/handoff_summary.md`:

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

Keep the handoff short. The orchestrator may read only this file.

---
name: luo-review-research-paper
description: Review research manuscripts with Professor Luo's reviewer-first approach and produce a prioritized diagnostic report without editing or rewriting the manuscript. Use when the requested deliverable must remain review-only, including pre-submission self-review and peer-review-style assessment of another manuscript, covering problem framing, application positioning, contribution claims, methods, experiments, abstract, conclusion, logic, terminology, notation, citations, figures, tables, and reviewer readability, especially in applied engineering and computing research.
---

# Review Research Papers with Luo's Approach

## Objective

Make the paper easy for a responsible reviewer to understand, evaluate, and trust. Build a defensible chain:

`domain problem -> literature gap -> contribution -> mechanism -> evidence -> implication`

Strengthen the visibility of real contributions without exaggerating novelty, inventing evidence, or hiding limitations.

## Use the principles reference

Read [references/luo-principles.md](references/luo-principles.md) completely for a full manuscript review. For a narrow review concerning one section or issue, read the matching section identified in its contents.

## Keep a review-only boundary

Use this skill only to diagnose and report. Do not modify the manuscript or turn the review into an editing task.

- Do not edit, overwrite, patch, or create a revised copy of any manuscript or source file.
- Do not rewrite sections, supply replacement paragraphs, or perform sentence-by-sentence polishing.
- Quote only the minimum text needed to locate or explain a finding.
- Recommend the goal and direction of a change, but leave the wording and implementation to the author.
- Create a separate review-report file only when the user explicitly requests one; otherwise report in the response.

If the user asks this skill to revise or edit a paper, state that this skill is review-only and provide diagnostic findings instead. Do not silently switch modes.

If another loaded skill or general workflow permits manuscript editing, this review-only boundary still governs work performed under this skill.

## Run the workflow

### 1. Inspect the available manuscript

Read the complete artifact when possible, including figures, tables, captions, references, comments, and tracked changes. Use an available format-specific skill for DOCX or PDF inputs. State extraction, rendering, or missing-material limitations rather than implying unavailable content was checked.

If no target venue is given, infer the likely audience from the manuscript and label the inference. Review incomplete drafts without blocking, but identify claims that cannot yet be evaluated.

### 2. Perform a cold read

Read the title, abstract, headings, contribution list, figure and table captions, and conclusion before line-by-line review. Record the apparent problem, audience, novelty, main result, and any term that blocks comprehension. Treat cold-reader confusion as a manuscript defect; do not silently fill logical gaps from author context.

### 3. Reconstruct the paper spine

State the domain problem, precise literature gap, consequence of the gap, author-created contribution, mechanism, supporting evidence, and bounded implication in one sentence each. Mark missing links and contradictions between sections.

### 4. Apply five publication gates

Evaluate before polishing language:

- **Comprehension**: Can a domain reviewer explain the work after one careful read?
- **Positioning**: Does an applied paper remain centered on its domain problem rather than a generic algorithm?
- **Contribution**: Are genuine author-created choices visible and separated from background or implementation detail?
- **Evidence**: Does every major claim have an appropriate experiment, analysis, comparison, citation, or qualification?
- **Coherence**: Do title, abstract, introduction, method, experiments, and conclusion tell the same story?

Treat a failure that prevents meaningful evaluation or invalidates the central claim as a submission blocker.

### 5. Review in dependency order

Review problem framing and domain motivation first, then novelty and contributions, method mechanism, claim-evidence coverage, introduction, abstract and title, conclusion, and finally sentence-level language and consistency. Diagnose structural issues before reporting surface-level language issues.

For every material unit, ask what job it performs, whether the reader has the required context, whether it explains the authors' work rather than standard background, whether its detail matches its importance, and whether it connects to adjacent units.

Run global audits for terminology, acronyms, notation, citations, repetition, figures, tables, and section titles. When one defect represents a pattern, report the pattern and representative locations rather than only its first occurrence.

### 6. Report actionable findings

Lead with the highest-impact issues. For each material finding, give:

- priority: submission blocker, major, moderate, or polish;
- location;
- what the reviewer encounters;
- why it matters;
- a concrete recommendation stated as an author action, without supplying replacement prose;
- confidence when missing context affects the diagnosis.

Avoid generic advice such as “improve clarity.” Let the requested task determine the report structure instead of forcing a fixed template.

## Review responsibly

While reviewing:

- evaluate claims only against available evidence;
- separate observed defects from uncertain concerns and stylistic preferences;
- do not invent citations, missing results, author intent, or technical meaning;
- distinguish general method claims from experimental implementation choices;
- flag unsupported novelty, unverifiable citations, missing baselines, and absent results rather than proposing fabricated repairs;
- state any extraction, rendering, venue, domain, or missing-material limitations.

## Default response

Unless the user requests another format, provide a concise reviewer verdict, reconstructed paper spine, prioritized findings, and a note on anything not inspected. Keep the review proportionate to the request and shorter than the manuscript.

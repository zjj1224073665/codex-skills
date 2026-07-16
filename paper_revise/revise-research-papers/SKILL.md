---
name: revise-research-papers
description: Revise research-paper prose and structure while preserving technical meaning. Use when Codex needs to diagnose or rewrite abstracts, introductions, related work, methods, results, discussions, conclusions, contribution statements, reviewer responses, or bilingual manuscript versions; compare a target section with reference papers; improve rhetorical flow, specificity, concision, terminology, or claim support; synchronize parallel language files; or rebuild and visually verify LaTeX, Markdown, DOCX, or PDF outputs after edits.
---

# Revise Research Papers

Revise academic writing at the level of rhetorical function, technical accuracy, sentence clarity, cross-language consistency, and rendered output. Treat reference papers as evidence about effective structure, not as text templates.

## Establish the task boundary

1. Determine whether the user requested diagnosis, a revision plan, an edit, or a complete verified artifact.
2. If the user requests a proposal before editing, inspect and explain without modifying files. Wait for explicit confirmation before applying changes.
3. Read repository instructions and identify the authoritative manuscript source, generated outputs, bibliography, and parallel language versions.
4. Preserve the paper's technical claims, notation, citations, limitations, and contribution scope unless the user explicitly asks to change them.
5. Flag any requested wording that would introduce an unsupported novelty, causal claim, empirical result, or generalization.

## Inspect before rewriting

Read enough context to identify the target passage's job:

- Read the complete target paragraph and its neighboring paragraphs.
- Read the section opening and closing when revising a transition.
- Search the abstract, contribution statement, methods, results, and conclusion for duplicated content.
- Locate definitions and formulas before simplifying technical language.
- Identify paired files such as source/translation, short/full version, or manuscript/supplement.

Represent each paragraph as one or more rhetorical moves:

- context or motivation;
- practical or scientific problem;
- prior-work summary;
- research gap;
- consequence of the gap;
- proposed response;
- concrete operating mechanism;
- study setting or evidence;
- contribution or implication;
- limitation or scope boundary.

Diagnose the move order before editing sentences. A grammatically correct paragraph can still feel wrong when it performs the wrong move for its position.

## Compare reference papers structurally

When a user supplies a reference paper:

1. Inspect the corresponding section and the same relative position within that section.
2. Map the reference's rhetorical sequence, paragraph functions, transition style, and level of technical detail.
3. Compare that map with the target passage.
4. Reuse the structural lesson, not the reference's wording, domain assumptions, or unsupported claims.
5. Prefer the target paper's own terminology and evidence.

For an introduction closing, commonly test this sequence:

1. Synthesize the relevant prior-work strands.
2. State the unresolved gap.
3. Explain why the gap matters.
4. Introduce the proposed method or strategy.
5. Explain concretely what the method observes, changes, or produces.
6. State the study setting or evaluation scope.
7. Present distinct contributions.

Adapt the sequence to the paper; do not force every move into every introduction.

## Diagnose prose that “feels strange”

Check for these common causes:

- **Wrong abstraction level:** Move implementation details out of motivation or contribution paragraphs when they belong in Methods.
- **Backward logic:** Avoid presenting the solution or case before stating the gap it addresses.
- **Abstract verb chains:** Replace sequences such as “formulate, construct, and achieve” with a clear method followed by concrete actions.
- **Missing actor or object:** Specify who coordinates, controls, predicts, compares, or updates what.
- **Vague achievement labels:** Demonstrate properties such as online, adaptive, robust, or real-time through the decision timing and behavior instead of merely naming them.
- **Repeated author labels:** Avoid several nearby sentences beginning with “this paper,” “this study,” “we,” or their translated equivalents.
- **Overloaded sentences:** Keep one main logical relationship per sentence when a sentence combines gap, formulation, method, mechanism, and goal.
- **Near-synonym stacking:** Do not cycle through framework, method, model, mechanism, and strategy unless each denotes a distinct object.
- **Redundant detail:** Do not repeat observation lists, cost formulas, or implementation rules in the introduction, contributions, and methods.
- **Questionable rationale:** Remove claims that are not logically necessary or could be defeated by a simple alternative design.
- **Unsupported gap claims:** Attach representative citations or qualify the scope when claiming that prior work does not address something.

## Design the revision

Draft a move-level outline before polishing wording. Prefer this pattern when introducing a technical method:

1. Name the method or strategy.
2. State the problem or setting it targets.
3. Explain what the model or data representation captures.
4. Name the decision-maker or analytical actor.
5. State its inputs, actions, and constraints concretely.
6. Add the case study or evaluation context.

Prefer actor-action-object constructions. Replace an abstract sentence such as “The framework enables effective coordination” with a sentence that identifies the actor, information used, decision made, and timing.

Use paragraph breaks to separate rhetorical moves, not merely to shorten text. Keep technical details only when they help the reader understand novelty, necessity, or scope at that point in the paper.

## Preserve section-specific roles

Use these patterns as diagnostics rather than rigid templates:

- **Abstract:** context → problem/gap → method → data or setting → principal results → implication.
- **Introduction:** motivation → focused problem → prior-work synthesis → gap → response → contributions.
- **Related work:** thematic synthesis → limitations relevant to the paper → precise positioning.
- **System modeling:** architecture → variables → dynamics → constraints. Keep case-specific data provenance out unless it changes how a model assumption must be interpreted.
- **Case study/experimental setup:** data provenance → public/derived/assumed classification → scenario parameters → experimental factors → evaluation protocol.
- **Results:** question → comparison → quantitative evidence → interpretation, without introducing new methods.
- **Discussion:** meaning → mechanisms or trade-offs → relation to prior work → limitations → external validity.
- **Conclusion:** answer the research question, summarize supported findings, and avoid new evidence or inflated claims.
- **Contributions:** separate novelty, reproducible artifact or formulation, and empirical evaluation; avoid turning the list into a methods recap.

## Synchronize bilingual or parallel versions

When parallel manuscript versions exist:

1. Identify the source of technical truth for the current edit.
2. Update all in-scope versions in the same task unless the user explicitly excludes one.
3. Preserve semantic alignment rather than sentence-by-sentence literal equivalence.
4. Keep terminology, symbols, line names, dataset names, citations, and scope qualifiers consistent.
5. Rewrite each language naturally. Avoid carrying source-language word order or repeated discourse markers into the translation.
6. Compare the rhetorical moves in both versions after editing.
7. Search for old wording that should have been removed from the paired version.

For Chinese academic prose, pay particular attention to repeated “本文/本研究/该框架,” long chains of nominalized actions, omitted coordination objects, and literal translations of vague English nouns. For English prose, check article use, compound modifiers, parallel structure, claim strength, and excessive nominalization.

## Edit safely

1. Inspect the current diff before editing and preserve unrelated user changes.
2. Apply the smallest coherent edit that fixes the rhetorical problem.
3. Keep citations attached to the claims they support.
4. Preserve LaTeX commands, labels, cross-references, equations, and bibliography keys.
5. Re-read the revised passage with its neighbors, not in isolation.
6. Search for newly duplicated phrases, inconsistent terminology, or stale translations.

## Build and verify

Never claim completion based only on source-text inspection.

1. Use the project's native build workflow.
2. For LaTeX, run the appropriate `latexmk` target and allow bibliography and cross-reference passes to finish.
3. Rebuild every synchronized output, including parallel language PDFs.
4. Distinguish new errors or warnings from pre-existing ones and report relevant residual issues.
5. Render the affected pages and visually inspect paragraph flow, column/page breaks, citations, headings, glyphs, clipping, and spacing.
6. For DOCX or other formatted artifacts, use the relevant render-and-verify workflow rather than checking text alone.
7. Inspect the final diff and status to confirm that only intended source and generated files changed.

## Report the result

Lead with the outcome. Include:

- the passages and language versions changed;
- the rhetorical improvement made;
- the build or validation commands that succeeded;
- any remaining warnings that matter;
- clickable paths to revised sources and outputs when available.

Do not describe an output as synchronized, compiled, or visually verified unless those checks were actually completed.

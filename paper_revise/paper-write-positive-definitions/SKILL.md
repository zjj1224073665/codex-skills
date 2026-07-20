---
name: paper-write-positive-definitions
description: Audit and revise academic-paper prose that defines a concept through defensive contrast, such as “X rather than Y,” “X, not Y,” “not X but Y,” “不是……而是……,” “而不是,” “而非,” or “并非.” Use when Codex needs to find or rewrite awkward reverse definitions, remove repetitive disclaimers, state technical concepts directly, rename misleading terms, preserve model boundaries while improving prose, synchronize bilingual manuscript versions, or respond to feedback that a paper should simply give the correct definition.
---

# Write Positive Definitions in Papers

Prefer a complete positive definition over explaining a concept by first invoking a nearby misconception. Preserve every technical boundary carried by the contrast; change the sentence structure, not the scientific meaning.

## Respect the task boundary

1. Determine whether the user requested an audit, an assessment, or an edit.
2. For an audit, report occurrences and classifications without modifying files.
3. For an assessment, explain which contrasts can be removed safely and which carry necessary meaning.
4. For an edit, update every in-scope source and parallel language version, then rebuild the generated artifacts.
5. Preserve unrelated user changes and leave staging or commit state unchanged unless explicitly requested.

## Audit the whole manuscript

Identify the authoritative manuscript source, generated outputs, and parallel versions. Search the full text for contrastive patterns, including:

- English: `rather than`, `instead of`, `not`, `not ... but`, `as opposed to`, `does not`, `need not`, and `neither ... nor`.
- Chinese: `不是……而是……`, `而不是`, `而非`, `并非`, `不……而是……`, `无需……而……`, and `不能……而应……`.

Treat these patterns as candidates, not automatic errors. Read the complete paragraph, neighboring paragraphs, first definition, formulas, tables, captions, experimental setup, and limitations before judging an occurrence. Search later uses to determine whether the contrast resolves a real ambiguity or merely repeats information.

## Classify before rewriting

Assign each occurrence to one of three classes.

### Direct-definition candidate

Rewrite when the positive clause already carries the full meaning and the negative clause only names an imagined misconception. Common cases include:

- units or time scale already made explicit;
- event-driven operation contrasted repeatedly with fixed time steps;
- a quantity defined positively and then contrasted with a different quantity;
- design coefficients contrasted with monetary prices;
- a fixed index mapping contrasted with arrival order;
- the same soft-constraint explanation repeated in several sections.

### Boundary-bearing contrast

Preserve the boundary semantically, but express it positively. Check especially:

- hard physical limit versus penalized planning target;
- power threshold versus energy allowance;
- measured or calibrated value versus explicit assumption;
- elapsed time versus event index;
- monetary price versus arbitrary objective unit;
- model input versus model output;
- online policy information versus a baseline's future information;
- local event cost versus nonnegative episode total;
- calibrated forecast versus scenario-based simulation;
- physical phenomenon versus modeling penalty.

If the positive rewrite cannot carry the distinction clearly, retain a concise contrast. Accuracy takes priority over stylistic uniformity.

### Necessary negative statement

Retain genuine negation when it performs an essential argumentative or logical role, including:

- establishing a supported research gap;
- stating that prior work lacks a feature;
- defining an infeasible or excluded condition;
- reporting missing data, unavailable measurements, or a method component that is genuinely absent;
- distinguishing mutually exclusive cases in a proof, formula, or algorithm;
- quoting reviewer language or source material.

Do not remove every occurrence of `not`, `rather than`, `不是`, or `而非` mechanically.

## Rewrite as a positive definition

Use actor--action--object constructions and state the operational meaning directly. Include the relevant unit, aggregation level, time scale, scope, source, or exceedance behavior in the positive sentence.

Apply these patterns:

- Replace “X is Y, not Z” with “X is Y,” expanding Y until it is unambiguous.
- Replace “the model does not impose A; instead B determines C” with “B determines C.”
- Replace “the mechanism uses A rather than B” with the event, rule, or input that directly defines A.
- Replace a negative provenance disclaimer with a positive source statement.
- Replace a negative limitation with a positive statement of the study's valid scope.
- Remove duplicated contrasts after preserving the definition once at its first formal use.
- Remove nonessential forward pointers such as “see a later section” or “as discussed below”; state the point directly. Keep precise figure and table references, and useful backward references.

Examples:

> The budget is a soft target rather than a hard physical limit.

Rewrite as:

> The budget is a penalized planning target, and temporary exceedance incurs a penalty.

> The exponent counts decision events rather than elapsed seconds.

Rewrite as:

> The exponent is the decision-event index.

> These coefficients are design weights, not monetary prices.

Rewrite as:

> These coefficients are fixed design weights expressed in arbitrary objective units.

> 该预算约束总功率，而不是整个时段的总能量。

Rewrite as:

> 总充电功率预算是运营商设定的总电网侧充电功率规划阈值，单位为 kW。

## Rename misleading terms

Prefer an accurate term over repeatedly denying the conventional meaning of an ambiguous term. Before renaming, search symbols, equations, tables, captions, figures, code-facing labels, and both language versions.

For example, if `overcharge` denotes a cumulative anti-cycling penalty, use `anti-cycling excess` or another technically accurate term throughout. Preserve existing mathematical symbols when changing them would create unnecessary implementation or notation churn, but update their prose labels consistently.

## Preserve scientific safeguards

After each rewrite, verify that a reader can still answer:

1. What exactly is being defined?
2. What are its unit, scope, and time scale?
3. Is it physical, contractual, economic, statistical, or model-imposed?
4. Can it be exceeded, and what happens then?
5. Is its value measured, derived, calibrated, selected, or assumed?
6. Which actor, rule, or data source determines it?
7. What conclusions does the definition permit?

Restore or recast any lost boundary before proceeding.

## Synchronize parallel versions

Update all in-scope language versions in the same task. Preserve semantic alignment instead of literal sentence structure. Search each version independently because a natural positive definition in one language may still appear as a defensive contrast in another.

Keep terminology, symbols, units, constraint behavior, calibration status, information assumptions, and limitation scope consistent. Search for stale terms after renaming.

## Verify the revision

1. Re-read every revised paragraph with its neighbors.
2. Search again for the targeted contrastive phrases and old terminology.
3. Confirm that remaining negative statements belong to the necessary-negative class.
4. Inspect the diff for lost qualifications, unsupported claims, and unintended edits.
5. Run the manuscript's native build workflow and complete bibliography and cross-reference passes.
6. Rebuild every synchronized output.
7. Inspect affected rendered pages when layout may have changed.
8. Report build errors, new warnings, or residual ambiguity honestly.

Lead the final response with the completed outcome, list the revised sources and outputs, and distinguish direct-definition rewrites from necessary negative statements that were intentionally retained.

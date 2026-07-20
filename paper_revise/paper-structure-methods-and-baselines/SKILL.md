---
name: paper-structure-methods-and-baselines
description: "Audit and revise research-paper section architecture so system modeling, proposed-method formulation, solution algorithms, comparison baselines, and experimental protocols have distinct roles and adequate technical depth. Use when method and solution sections are unnecessarily split, a solver subsection is too thin, baselines appear inside the proposed-method section, an algorithm is named without reproducible equations or update logic, numerical settings obscure the method, or a LaTeX, Markdown, or DOCX manuscript needs structural revision and verification."
---

# Structure Paper Methods and Baselines

Make the proposed method self-contained and place comparisons with the experiment that uses them. Preserve technical truth while improving section roles and methodological completeness.

## Respect the task boundary

1. Determine whether the user requested diagnosis, a revision plan, or direct edits.
2. For diagnosis, inspect and report without modifying files.
3. For direct edits, update every in-scope source and generated artifact.
4. Preserve unrelated changes, staging state, notation, citations, labels, and supported claims.
5. Do not invent implementation details to make a method look complete. Inspect code, configuration, appendices, or experiment logs when available; otherwise flag the missing fact.

## Map section roles before editing

Read the complete system-model, method, solution, experiment, and results sections rather than moving paragraphs from headings alone. Search for duplicated descriptions, hard-coded section numbers, and configuration tables.

Classify content by rhetorical function:

| Content | Default destination |
| --- | --- |
| Physical architecture, entities, dynamics, and feasibility | System modeling |
| Decision problem, observations, actions, constraints, and objective | Proposed method |
| Proposed solver parameterization, transformations, losses, targets, and update logic | Proposed method |
| Baseline identity, rationale, information access, and execution mechanism | Experimental setup: Compared Methods |
| Proposed and baseline numerical settings | Experimental setup: Algorithm Configuration |
| Seeds, matched budgets, evaluation counts, hardware, and statistical protocol | Evaluation protocol |
| Quantitative comparisons and interpretation | Results |

Treat these as defaults, not mechanical rules. Keep a comparator in the method section only when it is mathematically required to derive the proposed method or is an internal component of the proposed framework. Label that role explicitly. Do not present an external comparison algorithm as part of the paper's contribution.

## Decide whether to merge sections

Merge adjacent formulation and solution sections when they jointly describe one proposed method and the solution section is too small to carry an independent argument. A common coherent structure is:

```text
Proposed Method
  A. Decision Problem
  B. Observation/State and Action
  C. Constraints and Cost or Reward
  D. Optimization Objective
  E. Solution Algorithm
```

Use the following tests:

- Merge when the solver depends directly on the preceding state, action, and objective definitions.
- Merge when a section contains only one short generic algorithm paragraph.
- Merge when separating formulation and solver makes readers cross section boundaries to understand one method.
- Keep separate when the solver is itself a substantial contribution, contains several independent components, or solves multiple formulations.
- Keep system physics separate when it describes the environment rather than the learned or optimized decision rule.

After merging, rename the parent section so it covers both formulation and solution. Update hard-coded cross-references and verify all downstream section numbers.

## Strengthen an underspecified algorithm subsection

Make the proposed algorithm conceptually reproducible without turning the paper into a textbook. Include the parts that determine behavior or correctness:

1. Identify each trainable or optimized component and its inputs and outputs.
2. Define the policy, controller, search representation, or estimator mathematically when prose alone is ambiguous.
3. Show how raw outputs become feasible or bounded decisions, including projections, clipping, squashing, masks, or repair rules.
4. Include probability corrections when transformations change a density.
5. Define returns, residuals, advantages, targets, constraints, or surrogate objectives used for training.
6. Distinguish objectives that are maximized from losses that are minimized and use consistent update signs.
7. Define critic or estimator targets as cumulative-return targets when required; do not silently fit an immediate reward unless that is the actual method.
8. Explain rollout or data collection, minibatch reuse, update order, stopping behavior, and deterministic inference when they affect reproducibility.
9. Keep selected numerical values, network widths, learning rates, epochs, horizons, and schedules in the experimental configuration unless they are themselves methodological contributions.
10. Cite the original method and any separately introduced estimator, transformation, or correction.

For a standard algorithm, omit generic pseudocode that merely repeats its textbook loop unless the target implementation changes the loop. Spend space on problem-specific mechanics and non-obvious correctness details.

Before adding a formula, verify that it matches the implementation. If the policy standard deviation may be state-dependent or global, the entropy may be computed before or after squashing, or a feasibility layer changes the executed action, resolve that fact rather than choosing a convenient formula.

## Relocate and describe baselines

Create a `Compared Methods`, `Comparison Methods`, or equivalent subsection inside the case-study or experimental setup. Move external baselines there together with the information needed to understand the comparison.

For each baseline, report:

- why it represents a meaningful comparison class;
- what information and future knowledge it receives;
- whether it operates online, offline, open-loop, or receding-horizon;
- how its decisions are encoded and mapped to the simulator or dataset;
- which objective, action bounds, constraints, and evaluation budget it shares with the proposed method;
- any information or computational advantage that affects interpretation.

Explain custom MPC, heuristic, rule-based, or optimization baselines enough to reproduce their behavior. Avoid re-teaching standard GA, PSO, DE, or other textbook mechanics unless the implementation differs materially. Put their numerical settings in a shared configuration table.

Move comparison-specific fairness statements out of the proposed objective subsection. Keep the proposed objective focused on what the new method optimizes; explain matched objectives, seeds, evaluations, information, and budgets in the comparison or evaluation protocol.

## Keep proposed methods and experiments connected

End the method subsection with a concise forward reference to experimental configuration. In the setup:

1. Define data sources and assumptions.
2. Define scenarios and experimental factors.
3. Introduce compared methods.
4. Consolidate proposed and baseline settings.
5. State the fairness and evaluation protocol.
6. Define metrics, sensitivity tests, and ablations.

Avoid duplicating full method explanations in the setup. Use the setup to instantiate symbolic definitions with actual values.

## Verify the revision

1. Inspect the final source diff and repository status.
2. Search for baselines that remain in the proposed-method section without a justified role.
3. Search for hard-coded references to shifted sections.
4. Run the native build through all bibliography and cross-reference passes.
5. Check for undefined citations, undefined references, equation overflow, broken tables, missing glyphs, and new layout warnings.
6. Render and inspect affected pages when tools are available, especially section transitions and long equations.
7. Report verification accurately; do not claim visual inspection when only compilation was performed.

## Completion test

Finish only when a reader can answer:

1. What belongs to the system being modeled?
2. What is the paper's proposed method?
3. How does its solution algorithm actually train or optimize?
4. Which methods are external comparisons?
5. Where are all final numerical settings and evaluation rules?
6. Are comparisons fair, and are information advantages disclosed?
7. Are all added method details supported by the manuscript or implementation?
8. Are cross-references, citations, and rendered outputs consistent?

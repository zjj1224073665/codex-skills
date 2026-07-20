---
name: paper-separate-method-settings
description: Audit and revise research papers so method definitions, algorithm mechanics, and mathematical formulations remain in the methods section while case-specific hyperparameters, training schedules, baseline settings, seeds, hardware, and evaluation protocols move to the experimental setup, preferably in compact tables. Use when a methods subsection reads like a parameter dump, experimental details appear too early, a reference paper suggests better section placement, numerical settings need reorganizing across proposed and baseline methods, draft-only configuration language must be removed, or bilingual LaTeX manuscript versions must be synchronized and rebuilt.
---

# Separate Methods from Experimental Settings

Make the methods section explain how and why the method works. Make the experimental section report the exact configuration used to produce the results. Preserve both technical completeness and reproducibility.

## Respect the task boundary

1. Determine whether the user requested an assessment, a revision plan, or direct edits.
2. For an assessment, inspect and classify content without modifying files.
3. For an edit, update all in-scope manuscript versions and generated outputs.
4. Preserve unrelated user changes, notation, citations, labels, and staging state.

## Inspect the manuscript structure

Read the complete target subsection, its parent section, the experimental setup, and any parallel-language version. Search the manuscript for duplicated parameter values and later configuration tables.

When a reference paper is supplied, compare the rhetorical roles of corresponding sections:

- Identify where the reference defines the algorithm or model.
- Identify where it reports numerical settings and tuning choices.
- Reuse the organizational lesson, not the reference wording or parameter values.
- Do not follow the reference mechanically when the target method has a genuinely novel architectural component.

## Classify each detail by function

Use the following defaults, then apply the exceptions below.

| Content | Default destination |
| --- | --- |
| Method choice, purpose, inputs, outputs, and decision timing | Methods |
| State, observation, action, objective, constraints, and update equations | Methods |
| Algorithm mechanics such as clipping, advantage estimation, transformations, and probability corrections | Methods |
| Explanation of why a component is necessary | Methods |
| Numerical discount, clipping, GAE, or entropy coefficients | Experimental setup |
| Network depth, width, activation, optimizer, and learning rate | Experimental setup |
| Episodes, epochs, minibatch size, schedules, stopping rules, and tuning ranges | Experimental setup |
| Random seeds, evaluation mode, frozen normalizers, and hardware | Evaluation protocol |
| MPC horizon and numerical solver settings | Experimental setup |
| GA, PSO, DE, or other baseline rates and coefficients | Experimental setup |
| Fixed-baseline dwell times, powers, thresholds, or other values | Experimental setup |

Treat boundary cases carefully:

- Keep a network architecture in Methods when the architecture itself is a contribution; otherwise report its numerical shape in the setup table.
- Keep the existence and role of observation normalization in Methods when it affects the policy definition; place frozen statistics and evaluation behavior in the protocol.
- Keep a symbolic discount factor in the return equation; move its selected numerical value to the configuration table.
- Place physical or mathematical bounds in system modeling when they define general feasibility. Place case-specific bound values in the case study.
- Describe an MPC receding-horizon mechanism in Methods; report the chosen horizon length in Experimental Setup.

## Rewrite the methods section

Replace parameter-heavy prose with a technically complete account of the mechanism:

1. Name the method and the problem it solves.
2. State what the actor, optimizer, controller, or search procedure receives and produces.
3. Explain any transformations, objectives, constraints, or update logic needed for correctness.
4. Retain equations or citations that distinguish the implementation from a generic method.
5. End with a concise cross-reference to the experimental configuration.

Do not make the methods section shorter by making it vague. If removing numerical details exposes a missing explanation, add the relevant mechanism, formulation, or citation.

## Consolidate experimental configurations

Create a subsection such as `Algorithm Configuration and Evaluation Protocol` in the case-study or experimental section. Prefer one compact table with columns such as `Method`, `Parameter`, and `Value`.

Move settings for the proposed method and all comparison baselines consistently. A paper that moves PPO hyperparameters but leaves GA, PSO, DE, or MPC parameter lists in Methods still has the same structural problem.

Report exact final-run values. Keep method names, symbols, units, and terminology aligned with the methods section. Explain only protocol details that cannot be represented clearly in the table, such as deterministic action selection or frozen preprocessing statistics.

## Remove draft-only configuration language

Delete statements such as:

- “the current defaults are ...”;
- “if saved metadata differ, use the saved values”;
- “parameters may be updated in the final experiment”;
- internal paths, run-selection notes, or unresolved placeholders.

Replace them with the exact settings that generated the reported results. If those settings are not yet known, flag the manuscript as not ready for a final reproducibility claim rather than concealing the uncertainty.

## Synchronize and verify

1. Apply the same structural change to every in-scope language or manuscript version.
2. Preserve semantic alignment without forcing literal translation.
3. Search for stale numerical values, duplicated parameter prose, old subsection references, and unresolved drafting language.
4. Build each manuscript with its native workflow and complete bibliography and cross-reference passes.
5. Check logs for new errors, undefined references, and overfull boxes.
6. Render affected pages and visually inspect table width, line breaks, float placement, headings, glyphs, and readability.
7. Inspect the final diff and report the source files, generated outputs, and validation performed.

## Completion test

The revision is complete only when a reader can answer:

1. Does the methods section explain how the method works without relying on a parameter list?
2. Can every numerical setting used to generate the results be found in the experimental setup or protocol?
3. Are proposed and baseline methods treated consistently?
4. Are symbols retained in the formulation while selected values are reported separately?
5. Does the paper state final values rather than defaults or conditional metadata?
6. Are parallel versions and rendered outputs synchronized and visually sound?

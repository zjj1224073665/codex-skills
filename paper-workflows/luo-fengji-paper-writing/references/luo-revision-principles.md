# Luo Revision Principles From EPF Manuscript

Use this reference when revising engineering, energy forecasting, LLM-generated model, evolutionary optimization, interpretable forecasting, or factor-mining manuscripts in Luo-style.

These notes distill the 2026-06 EPF manuscript revision conversations and the revised final PDF. Treat them as operating rules, not as text to copy.

## Core Writing Position

Write for a serious target-field reviewer. The reviewer is not impressed by abstract technical labels. They accept the paper only if they can see what application problem is being solved, why prior work leaves a gap, why the proposed mechanism addresses the gap, and what evidence supports the claim.

For application journals, keep the application as the main story. A method may be generally useful, but the paper should read as a solution developed for the target problem, not as a computer-science technique later tested on the target problem.

For EPF or energy papers, the reviewer should constantly see electricity price forecasting, market behavior, operational decisions, accuracy, direction, interpretability, and forecast evidence. Do not let LLM, multi-objective optimization, symbolic regression, prompt engineering, parsing, or implementation details become the dominant story.

## Title, Acronyms, And Naming

If a framework name or acronym is used throughout the paper, make sure it does not erase the application. A generic acronym can make the paper look like a computing paper. Either choose an application-aware name or introduce the generic method through the application need.

Do:

- Make the title and key terms point to EPF, energy forecasting, interpretable forecasting, or the actual application.
- Explain a general method as the route used to solve an application gap.
- Keep generality as an implication: the same design may transfer to other time-series forecasting tasks.

Avoid:

- Selling only the generic framework name.
- Starting section headings with a technical acronym whose expansion has no engineering signal.
- Claiming a whole generic research direction as novel unless that is genuinely supported.

## Contribution Framing

Each contribution should follow this logic:

1. What design was introduced.
2. What limitation in existing work it addresses.
3. Why that matters for the application.
4. What evidence or experiment supports it.

Avoid contribution bullets that are only technical labels. Put the physical or operational meaning in the bullet. For EPF, point error and direction error are not just metrics. Point error concerns forecast magnitude. Direction error concerns whether the predicted movement supports downstream decisions.

Do not over-split small tricks. Merge secondary details into a larger contribution unless the detail has a clear application benefit or generalizable value.

Useful EPF contribution patterns from the revised manuscript:

- Code-level symbolic forecasting: generated EPF code can express multi-step and conditional forecasting logic more flexibly than a plain formula while remaining inspectable.
- Multi-objective forecasting design: jointly optimize point accuracy and directional accuracy because accurate direction can matter even when exact price magnitude is difficult.
- Signal-correlation based selection: replace generic distance-style diversity with behavior-level diversity among forecasting signals, reducing redundant forecasts and retaining varied EPF candidates. Present this as useful for price or time-series forecasting, not as an isolated optimization trick.

Only claim "first" when literature checking supports it. Otherwise use softer language such as "to our knowledge", "few studies", or "existing EPF studies rarely".

## Plain English And Fancy Words

Use plain academic English. Technical language is fine when it names a precise concept, but not when it hides a vague claim.

Replace vague or fancy wording with mechanism:

- Do not just say "improves transparency". Say what becomes visible, such as the forecasting calculation or decision logic.
- Do not just say "supports decision making". Say which decision-relevant property is improved, such as direction, confidence, or readable forecast logic.
- Do not just say "captures market patterns". Say which market logic can be represented, such as supply-demand imbalance, momentum, regional interaction, or price movement direction, and cite or test it when needed.

General background on LLMs, transformers, optimization, or standard metrics should be brief and cited. The paper is not a tutorial. Give only enough background to understand the proposed method, then return to the application.

## Related Work And Gap

State the scope precisely. If the limitation applies to interpretable EPF methods, do not write "common EPF methods" as if all EPF work has that limitation.

For explainability claims, distinguish between:

- post-hoc feature importance: explains which variables influenced a produced forecast;
- transparent forecasting logic: reveals how the forecast is computed before or during deployment.

Do not argue that post-hoc explanation is useless for decisions if the method still gives a forecast and explanation before the user acts. The stronger limitation is that feature attribution may not reveal the calculation or decision logic that generated the forecast.

For historical pattern matching or feature matching, explain why matching past patterns may be less satisfying than learning generalizable market logic. Use concrete examples only when they are supported: supply-demand imbalance, momentum, regional price interactions, or other domain mechanisms.

## Method Section

Open the method with the architecture and mechanism.

A strong method overview says:

- what the major modules are;
- how they interact in each generation or iteration;
- what a candidate solution is;
- how candidates are evaluated and selected;
- how the final forecast model or subset is obtained;
- why this design fits the application problem.

Do not open the overview by listing metrics or implementation details. Metrics belong where objectives are defined. Runtime, parsing prefixes, allowed libraries, response extraction, and code validation belong only where they affect reproducibility or method validity.

For LLM-generated forecasting code:

- Use one consistent term, such as "candidate EPF code", "candidate forecasting code", or "candidate solution".
- If the implementation is not tied to Python conceptually, do not bind the whole method to Python. Mention Python in implementation or experiment setup.
- If generated code is checked, explain the purpose plainly: the extracted candidate is checked to ensure it can produce valid forecasts under the evaluation protocol.
- Avoid long descriptions of prompt plumbing unless the prompt design is part of the contribution.

For multi-objective or evolutionary optimization:

- Do not over-explain standard Pareto concepts.
- Highlight what differs from a standard algorithm and why the difference helps forecasting.
- Explain why signal correlation or diversity matters for forecasts if it replaces a generic diversity measure.
- Keep formulas connected with text. Every displayed formula should have a reason.

## Notation And Terminology

Be strict with symbols. Sloppy notation makes reviewers doubt the whole paper.

Checklist:

- Define each abbreviation once, then reuse it consistently.
- Do not repeat full expansions every time.
- Use vector notation when a quantity is a vector.
- Avoid word-like variables when a mathematical symbol would be clearer.
- In time-series forecasting papers, avoid using `T` for optimization generations because readers associate `T` with time. Use `G` or another generation index.
- Keep "forecasting" and "prediction" usage consistent. Prefer "forecasting" for method-based time-series tasks.
- Use "generation" and "iteration" consistently. Do not switch terms casually.
- Use citations only when they support a claim, dataset, method, or standard definition.

## Experiments

Experiments should form a narrative, not a pile of tables.

A useful order is:

1. setup and dataset, tied back to the application motivation;
2. main performance against baselines;
3. ablation for design choices;
4. sensitivity or parameter analysis only after the reader knows the method works;
5. visualization or interpretability examples that support the claimed mechanism;
6. summary of observations.

Dataset description should echo the earlier motivation. If the introduction discusses regional interactions, market features, or specific operational needs, the experiment setup should show how the selected data and features test those claims.

Put hardware and implementation environment in experiment setup. Do not scatter these details in the method unless they are part of the method.

Figures must be readable at paper scale. Axis labels, legends, and captions should not be smaller than the surrounding text to the point of strain. Caption names must describe what is actually plotted, for example "Generation Index" if the x-axis is the generation index.

## Conclusion And Future Work

The conclusion is not a second abstract. Keep the method recap short, then summarize what the evidence shows.

Include concrete observations when available:

- which metrics improved;
- whether accuracy and direction were both maintained or improved;
- what visualization showed about readable forecasting logic;
- what ablations proved about the key design choices.

Limitations and future work should be real research directions. Avoid weak future work such as "try another optimizer", "test more datasets", or "use a larger model" unless it is tied to a deeper research question.

Good future-work directions are broader questions opened by the paper, such as multi-agent forecasting mechanisms, stronger confidence or uncertainty-aware forecasting, generalization to other markets, or principled ways to learn interpretable market logic.

## Final Revision Gate

Before returning revised prose, check:

- Does the target application appear in the title, abstract, contribution list, method overview, experiment setup, and conclusion.
- Can a target-field reviewer explain the method after reading the overview.
- Are all contribution bullets concrete enough to be defended in review.
- Are fancy words replaced by mechanism and evidence.
- Are implementation details kept in the right section.
- Are formulas and symbols clear, consistent, and necessary.
- Are repeated claims compressed.
- Are unsupported novelty claims softened or flagged.
- Are figure/table captions and section headings specific and helpful.

---
name: paper-explain-new-terms
description: Revise academic and technical writing so new terms, constraints, metrics, mechanisms, variables, and named concepts are motivated and defined before readers must rely on them. Use when a paper introduces jargon abruptly, assumes an unexplained budget or limit, leaves formula variables, indices, sets, or units unexplained, jumps from background to a formal model, leaves the origin of a research problem unclear, or receives feedback such as “Where did this come from?”, “Why is this needed?”, “What does this variable mean?”, or “This symbol appears out of nowhere.”
---

# Explain New Terms in Papers

Make each important new concept feel like the necessary conclusion of the preceding argument. Establish the real-world or technical cause, trace its consequences, explain the resulting need, and only then name and define the concept.

## Core Rule

Do not solve an abrupt-term problem with a dictionary definition alone. Use this causal order:

`starting condition -> mechanism -> system effect -> practical or research consequence -> need -> term and definition -> role in this paper`

The reader should understand why the concept must exist before being asked to remember its name.

Never treat an acronym expansion, parenthetical gloss, unit, formula, or sentence of the form “X is/means/refers to Y” as sufficient evidence that a term is explained. These forms establish what the term is; require the surrounding prose also to establish why it is introduced and what it affects in the paper.

## Workflow

### 1. Audit the first use

Locate the first substantive use of the questioned term and read enough surrounding material to answer:

- What does the paper later say the term means?
- Is it a physical limit, planning target, model assumption, decision variable, metric, algorithm, or label?
- What is its unit, scope, aggregation level, and time scale?
- Is it hard or soft, measured or assumed, local or system-wide?
- Which earlier fact should make the reader expect this concept?

Inspect equations, methods, tables, captions, and limitations before rewriting the introduction. Do not invent an introductory motivation that contradicts the formal model.

Treat the term's name as a search clue, not as evidence of its meaning. If the manuscript does not supply the facts needed to explain the concept accurately, identify the missing definition or mechanism and ask the author, or leave an explicit drafting placeholder. Do not complete the causal chain by guessing.

Build a notation ledger while auditing displayed equations. For each symbol, record its meaning, unit, and index or set. Define every symbol at or immediately before its first appearance; do not postpone the explanation until a later section.

Place a variable's prose name next to its symbol at first use---for example, ``next-platform arrival time $t_k^{\mathrm{next}}$'' or ``delay probability $p_{\mathrm d}$''. Repeat the name--symbol pair later whenever it improves readability. Apply this pattern to any symbol, not only those on the left-hand side of an equation.

### 2. Recover the root problem

Start from the earliest concrete fact, not from the paper's preferred solution. Ask “why?” repeatedly until reaching a condition the intended reader already understands.

For example, do not start with “the operator has a charging-power budget.” Recover the chain:

`high-power storage + short charging windows -> large individual charging demand -> overlapping vehicles add their demands -> aggregate peaks can exceed planned supply or contracted demand -> simultaneous power must be coordinated -> total charging-power budget`

The domain details will change, but the reasoning pattern should not.

### 3. Write the bridge before the label

Build the explanation in this order:

1. State the relevant system feature or observed condition.
2. Explain the mechanism by which it creates an effect.
3. State why the effect matters: risk, cost, infeasibility, uncertainty, poor service, or scientific ambiguity.
4. Explain what must therefore be limited, measured, compared, predicted, or controlled.
5. Introduce the term as the name for that requirement or quantity.
6. Define its operational meaning, including important boundaries and units.
7. Connect it directly to the paper's case, model, or research question.

Use explicit causal language where helpful: “because,” “when,” “as a result,” “therefore,” and “in this paper.” Prefer concrete actors and quantities over nominal abstractions.

### 4. Match the bridge to the concept type

- **Constraint or budget:** Identify the demand or risk that creates the need for a limit. Define what is capped, over what scope and time scale, in which unit, and whether exceedance is physically impossible or merely penalized.
- **Metric or index:** State the decision or comparison that cannot be made with raw observations. Explain what the metric captures, how to interpret high and low values, and its unit or normalization.
- **Method or mechanism:** State the failure of the existing process and the capability needed to address it. Then name the method and summarize the causal feature that supplies that capability.
- **Assumption or model abstraction:** State what is unknown, unavailable, or deliberately omitted. Explain why the assumption is needed and what conclusions it limits.
- **Variable or parameter:** Describe the physical or conceptual quantity before presenting its symbol. Give its unit, range, sign convention, and indexing when these matter.
- **Acronym or named system:** Give the full name and its role in the argument before relying on the shortened label.

### 5. Audit every equation

For every displayed equation, ensure the surrounding prose defines:

- the quantity on the left-hand side;
- every new symbol on the right-hand side;
- all indices, sets, and summation ranges;
- units and unit-conversion constants such as 60 or 3600;
- ranges, sign conventions, and stochastic distributions;
- whether a value is evaluated before or after an event or action.

Do not introduce a symbol in an equation and assume that its name or subscript makes the meaning obvious. If the explanation would interrupt the argument, add a concise ``where'' sentence immediately after the equation.

### 6. Preserve scientific accuracy

Do not exaggerate consequences to make the motivation sound dramatic. Distinguish among:

- a physical protection limit and an economic or planning target;
- possible stress or overload and inevitable system failure;
- a measured fact and a modeling assumption;
- a local infrastructure constraint and an operator-level accounting rule;
- a power limit and an energy allowance;
- correlation, mechanism, and causation.

Add or preserve citations for externally verifiable causal claims. If evidence only supports a narrower statement, use the narrower statement.

Do not infer a formula, mechanism, direction of improvement, unit, or causal effect from a term's wording alone. When the necessary evidence is unavailable, state what must be established before offering final prose.

### 7. Integrate rather than append

Rewrite the surrounding paragraph so the explanation forms one argument. Do not paste a long definition after the unexplained first use. Move the motivation earlier, remove duplicated later explanations, and make the next paragraph begin from the now-established concept.

Keep the bridge proportional. Explain every inferential step the reader needs, but avoid a textbook detour unrelated to the paper's contribution.

### 8. Check the whole manuscript

After revising the first use:

- Use one preferred term consistently across the abstract, introduction, model, results, and conclusion.
- Re-scan every displayed equation and confirm that no symbol depends on an unexplained later definition.
- Synchronize translated or parallel manuscript sources when present.
- Confirm that equations and prose use the same scope and units.
- Rebuild the document when editing LaTeX or another compiled format.
- Inspect the relevant rendered page for overflow or disrupted paragraph flow.

## Revision Test

The passage is ready only if a new reader can answer, in order:

1. What concrete condition starts the problem?
2. Through what mechanism does that condition produce the relevant effect?
3. Why does the effect matter?
4. Why is the new concept needed?
5. What exactly does the term mean here?
6. What does it include and exclude?
7. How does it lead to the paper's research problem or method?
8. Can every formula symbol, unit, index, and time reference be understood at first use?

If any answer depends on material that appears only later, repair the first-use explanation.

## Example

Abrupt:

> Two tram lines share a total charging-power budget.

Motivated:

> Vehicles with high-power onboard storage replenish energy during short station stops, so each charger can impose a large, short-duration load. When several vehicles charge simultaneously, these loads add and may exceed the capacity planned for supply equipment or the operator's contracted demand. The operator must therefore coordinate the aggregate grid-side power drawn at any instant. In this paper, the maximum planned aggregate charging power is called the total charging-power budget; it is a power limit in kW, not an energy allowance. When two lines share this budget, power used by one line reduces the amount available to the other.

Treat this as an illustration of the causal structure, not as wording or domain assumptions to copy into unrelated papers.

# Luo's reviewer-first principles

## Contents

1. Reviewer viewpoint
2. The application-centered story
3. Contributions and novelty
4. Logic and readability
5. Methods and technical detail
6. Abstract, introduction, and conclusion
7. Terminology, notation, and citations
8. Figures, tables, and final checks

## 1. Reviewer viewpoint

Write from the reader's mental state, not from the author's private model of the work. At every transition, ask what the reader currently knows, what they may infer incorrectly, and what must be stated next.

If a knowledgeable supervisor who has discussed the project cannot follow a passage, an external reviewer is even less likely to follow it. Treat “I can guess about 90%, but I am not certain” as a clarity failure, not as success.

Responsible reviewers need to understand the work before they can credit it. Obscurity does not make a contribution look sophisticated; it prevents evaluation. Maximize acceptance probability by making the work legible, coherent, and evidence-backed rather than relying on reviewer luck.

## 2. The application-centered story

For an engineering or applied-domain paper, sell the solution to the domain problem. The algorithm, model, or software mechanism is the means.

The preferred framing is:

1. the domain has an important unresolved problem;
2. existing approaches leave a specific limitation;
3. that limitation causes a concrete domain consequence;
4. the paper introduces a mechanism tailored to address it;
5. experiments test whether it does so.

Avoid making an energy, medical, manufacturing, transport, or other domain paper read like a generic computer-science technique followed by a token application. Align the title, acronym, method name, overview, figures, and terminology with the target venue's audience.

Generality can remain a secondary advantage. State first what the method accomplishes in the target task, then note how the mechanism may transfer to other tasks. Do not let a general acronym erase the application identity of the manuscript.

Connect method design choices to domain properties. For example, explain that a selection rule is useful because it preserves behaviorally different forecasts under volatile or regionally coupled market conditions; do not merely describe the selection rule in isolation.

## 3. Contributions and novelty

Inventory every author-created design choice before drafting the contribution list, including small changes. For each candidate contribution, determine:

- what is genuinely new;
- what prior component it changes or combines;
- what domain problem motivated the change;
- what benefit the mechanism should provide;
- what evidence verifies that benefit;
- how broadly the claim can safely generalize.

Distinguish three layers:

- **Background component**: established method requiring attribution, not contribution language.
- **Implementation choice**: needed for execution or reproducibility, but usually not a headline contribution.
- **Research contribution**: a defensible design, formulation, finding, or empirical demonstration that closes the stated gap.

Small modifications deserve visibility when they are purposeful and effective. Explain why the replacement is more appropriate for the task and what it enables. Do not hide it as a throwaway detail. Equally, do not inflate routine validation, library restrictions, error handling, or parameter wiring into novelty.

Contribution statements should name the physical or scientific meaning, not only the optimization operation. Prefer “jointly improves point accuracy and directional usefulness” over “minimizes objective 1 and objective 2.”

Verify every “first,” “novel,” “no prior work,” and “state-of-the-art” claim. If exhaustive verification is unavailable, narrow the wording.

## 4. Logic and readability

Use plain, professional language. Replace fancy words and abstract noun stacks with direct statements of actor, action, object, and consequence.

Before introducing a term, answer in ordinary language:

- What is it?
- What does it do?
- Why is it needed here?

Then supply the formal name, notation, or equation.

Ensure adjacent sentences and sections have explicit semantic links. A method step must state whether it initializes, solves, filters, updates, or evaluates the object introduced before it. Do not make readers reconstruct missing transitions.

Remove local repetition. State an important point once with force. Repeat it later only when the rhetorical job changes—for example, motivation in the introduction, evidence in the results, and implication in the conclusion.

Delete decorative or self-evident sentences that add no new information. Avoid preview paragraphs that merely repeat the upcoming subsection list unless they provide a useful conceptual map.

## 5. Methods and technical detail

Start a method section with an overview of the architecture or mechanism: major components, their roles, information flow, and final output. Do not lead with a metric, parameter, or code-level exception.

Use a simple overview figure when several modules interact. Keep it readable and visually economical.

Spend space on author-created mechanisms and non-obvious choices. Compress standard algorithms and textbook concepts, normally with a citation. Reviewers want to learn how the paper solves the problem, not receive a long tutorial on familiar machinery.

Maintain a clear detail hierarchy:

- main text: conceptual mechanism, research-relevant choices, and reasons;
- experimental setup: hardware, language, libraries, parameters, and implementation instantiation;
- appendix or supplement: code parsing, defensive checks, long prompts, edge-case handling, or reproducibility detail.

Every “instead of” needs a reason and an expected consequence. State what the new choice enables or improves.

Merge choppy runs of one sentence plus one equation when the relations are clearer as a single conceptual block. Split equations when displaying them together obscures their hierarchy.

## 6. Abstract, introduction, and conclusion

### Abstract

Review the abstract as a compact research argument, not as a compressed method section or experiment table. In most applied engineering papers, the reader should encounter the following sequence:

1. the broader domain background and why the problem matters;
2. the precise limitation of existing work and its practical consequence;
3. the paper's primary contribution, stated before secondary implementation details;
4. the proposed method at the level of its governing idea;
5. the case-study or evaluation setting; and
6. the headline outcome, comparison, and field-level implication.

The transition from background to gap must occur before the method is introduced. If the paper's central novelty is opening a previously unstudied system setting, such as moving from single-line to multi-line operation, make that contribution unmistakable and do not bury it behind state dimensions, simulator mechanics, or a list of algorithms.

Evidence in an abstract need not be numerical. A concise qualitative result is often more readable in an engineering abstract when exact values require substantial setup or are not themselves the paper's message. Recommend numbers only when they are central, interpretable without extra context, and supported by the final experiment set. Do not promote a preliminary baseline, accounting artifact, or merely available metric into the headline evidence just to make the abstract look empirical.

When experiments are complete, the abstract should state what the results show rather than say that the study “asks whether,” “will evaluate,” or “is designed to compare.” End with an evidence-bounded positive claim: name the operational benefits demonstrated, identify the comparison class when relevant, and explain why the method is useful. Promotional phrasing such as “an attractive solution” is acceptable when the preceding sentence establishes the tested benefits; unsupported claims of superiority are not.

Keep the method description conceptual. Remove unexplained acronyms, observation dimensions, detailed event-processing rules, parameter grids, and long baseline inventories unless one is essential to understanding the contribution or strength of evidence. A case-study identity and a short description of representative comparison methods are usually sufficient.

Do not weaken the abstract by advertising incidental omissions or limited interaction. Phrases such as “only connected through,” “weakly coordinated,” or “without modeling X” often make the problem look less important and draw attention to something the study does not claim to solve. State the actual coordination mechanism and intended scope positively. Reserve a boundary statement for the discussion unless omitting it would materially mislead the reader about the central claim.

Audit “first,” “novel,” and superiority claims against the literature and experiments. If the paper genuinely makes the first study of a new application setting, put that claim next to the contribution it qualifies; if verification is incomplete, narrow it with an appropriate knowledge boundary.

As a final cold-read test, a domain reviewer should be able to answer five questions from the abstract alone: Why does the problem matter? What exactly has prior work missed? What did the authors introduce? What did the evaluation show? Why should the field care?

### Introduction

Make the contribution paragraph exceptionally clear. Use ordinary but professional language so readers understand what was done, why it helps, and what evidence supports it. List contributions only when they are distinct and parallel.

Write the contribution list after the method and experiments are stable. Then check that the abstract and conclusion express the same contribution boundaries.

### Conclusion

Do not rewrite the abstract. Summarize the work briefly, then state what the study shows, using key quantitative results or observations where useful. A conclusion should answer: “After reading this study, what should the field now believe or know?”

Future work should contain two or three research directions that follow naturally from limitations or newly opened questions. Replacing an optimizer, testing one more dataset, or using a newer component is usually incremental rather than a substantive direction unless it tests a meaningful scientific question.

## 7. Terminology, notation, and citations

Use one name for one concept. Do not alternate between near-synonyms such as code, program, function, candidate, and solution unless each denotes a distinct object and the distinctions are defined.

Define acronyms once. Do not expand them repeatedly in nearby sections; re-expansion may be acceptable much later when readers reasonably need a reminder.

Choose notation for reader expectations, not author convenience. In a time-series paper, avoid using `T` for an evolutionary generation if readers will naturally interpret `T` as time. Prefer semantically suggestive symbols and reserve common symbols for their domain meanings.

Audit every symbol for:

- definition before use;
- scalar, vector, or matrix formatting;
- subscript and superscript meaning;
- index range;
- unit or dimension;
- collision with another concept;
- consistent use across text, equations, algorithms, and figures.

Use symbolic variables rather than literal English words inside formulas unless convention strongly favors the word. Make the notation easy to parse.

Every citation needs a job: support a claim or number, attribute a method, establish a gap, or enable comparison. Remove citations attached to self-evident implementation statements or generic facts when they support nothing identifiable. Add citations for borrowed technical explanations.

## 8. Figures, tables, and final checks

Figures and tables must remain readable at final publication size. Compare embedded font size with body text, enlarge dense plots, and avoid packing multiple time-series panels so tightly that labels and trends become illegible.

Check that captions explain the object, setting, and takeaway sufficiently for a reviewer scanning the paper. Ensure section titles and figure/table titles accurately summarize their content and use parallel grammar.

Before submission, inspect the compiled PDF rather than trusting the source editor. Check:

- title and acronym alignment with the domain;
- section hierarchy and headings;
- figure and table readability;
- caption accuracy;
- equation breaks and numbering;
- notation and term consistency;
- reference formatting and citation completeness;
- orphan headings, page breaks, and small fonts;
- any author notes, highlights, comments, or placeholders.

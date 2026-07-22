---
name: convergent-meta-spec-review
description: Review and revise meta-specs, agent task prompts, and implementation prompts without letting iterative audits expand indefinitely. Use when Codex must find real ambiguities, incorporate review feedback, separate downstream instructions from external review orchestration, or run multiple review rounds with explicit blocker and stopping criteria.
---

# Convergent Meta Spec Review

## Overview

Make prompt review converge on observable correctness. Separate the prompt delivered to the next agent from the orchestration used to review that prompt.

## Separate the Two Layers

- Put task scope, authoritative semantics, locked behavior, allowed files, acceptance contracts, and handoff requirements in the deliverable prompt.
- Keep review rounds, reviewer assignments, severity triage, and stopping policy in the calling agent's plan or a separate review rubric.
- Add review-process instructions to the deliverable only when the downstream agent is explicitly responsible for running that review process.
- Treat a meta-spec as a prompt sent to another agent: include only information that agent needs to execute its task.

Do not leak orchestration into the artifact merely because it helped the current team converge.

## Review Workflow

1. Identify the downstream executor, requested artifact, allowed mutations, locked behavior, and observable acceptance contracts.
2. Read the whole prompt and only the referenced source material needed to test its claims.
3. Run one open review pass. Classify every finding with the blocker gate below.
4. Apply the smallest revision that removes each blocker. Prefer one normative definition and references over duplicated rules.
5. Review the actual saved artifact and its diff, not only a proposed patch or summary.
6. Run a verification pass focused on resolved blockers and direct regressions. Allow genuinely new blockers, but apply the same gate.
7. After fixing a verification-pass blocker, continue using the verification gate; never reset to an unrestricted first pass.
8. Stop when no blocker remains. Keep optional hardening outside the current change.

## Blocker Gate

Treat a finding as blocking only when all conditions hold:

1. It is inside the original task scope.
2. It includes a concrete counterexample, event timeline, conflicting formula, or two reasonable conforming interpretations.
3. The ambiguity produces different observable behavior or violates a named invariant or acceptance contract.
4. Its minimal fix does not require inventing a new feature or expanding the authorized scope.

Record wording preferences, hypothetical future mechanisms, broader model redesigns, and extra defensive checks as non-blocking. Do not revise the current artifact for them unless the user expands scope.

## Check Normative Completeness

For each new state or term, verify only the information needed to implement it uniquely:

- isolation key;
- initial value or anchor;
- read and update times;
- ordering relative to other events;
- source of truth and profile precedence;
- effect on public outputs and locked interfaces.

Use a concrete timeline to test the model. Add an extra intervening event when necessary to expose stale-state overwrite bugs that a two-event example can hide.

## Preserve Scope and Existing Work

- State that unmodified behavior retains its existing authoritative semantics.
- Report out-of-scope conflicts by file, section, and reason; do not fix them implicitly.
- Snapshot dirty paths before editing and compare with the same commands afterward.
- Remember that `git diff --check` checks whitespace errors, not the set of modified files.
- Do not claim a clean worktree when unrelated user changes already existed.

## Avoid Review Loops

Do not repeatedly ask whether any ambiguity exists. That is an open-ended research question with no finite completion condition.

Avoid these failure modes:

- promoting style improvements to correctness blockers;
- adding a mechanism for every theoretical boundary;
- demanding that a narrow prompt axiomatize the entire system;
- inserting the team's review protocol into the downstream prompt;
- reopening an unrestricted audit after every wording change;
- reviewing only the intended patch instead of the saved artifact.

## Report Review Results

For every blocker, report:

- the exact location;
- the concrete counterexample or conflicting interpretations;
- the acceptance contract or invariant that fails;
- the smallest sufficient correction.

List non-blocking notes separately and keep them short. End with an explicit stop decision when no blocker remains.

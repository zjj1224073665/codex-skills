---
name: convergent-meta-spec-review
description: Review a meta-spec prompt before it is handed to another AI. Use when Codex must check whether a meta-spec defines a clear task, scope, authoritative semantics, edge cases, acceptance criteria, and final response without implementation-blocking ambiguity.
---

# Review a Meta Spec

## Goal

Determine whether the next AI can execute the meta spec correctly without making an important choice that the author should have made.

## Review

1. Read the complete meta spec.
2. Identify the requested outcome, allowed files or actions, prohibited changes, source-of-truth documents, acceptance criteria, and required final response.
3. Read referenced specifications or code only when needed to verify an interface, term, or claimed existing behavior.
4. Find contradictions, missing decisions, undefined terms, and edge cases that could produce different conforming implementations.
5. For each real problem, propose the smallest wording change that makes the instruction unique and executable.
6. After revision, reread the saved meta spec itself and confirm the blocker is gone.

## Checklist

- Is the downstream AI's role and deliverable explicit?
- Are allowed and forbidden mutations consistent?
- Is each source of truth and override priority clear?
- Do important states and terms have the necessary key, initial value, read time, and update time?
- Is event ordering or boundary behavior defined where outcomes depend on it?
- Does at least one concrete example exercise the main risky case?
- Can every acceptance item be observed or asserted?
- Does the final-answer instruction match the work the AI is allowed to perform?
- Does the meta spec contain only instructions needed by the downstream AI? Keep reviewer coordination and internal review rounds outside it unless that AI is explicitly asked to run them.

## Blocker Test

Treat a finding as blocking only if it is within scope and includes a concrete counterexample: two reasonable readings produce different required behavior, or one reading violates a stated invariant or acceptance item.

Treat style preferences, optional hardening, new features, and broader redesigns as non-blocking notes. Do not expand the meta spec for them.

## Report

List findings in severity order. For each blocker, include:

- location;
- conflicting readings or concrete example;
- implementation consequence;
- minimal correction.

If there are no blockers, say so and stop. Keep non-blocking notes short and separate.

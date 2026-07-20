# Self-review notes for AUPEC conference draft

## Scope decision

- The draft uses only `spec/`, current code, and case-data README content.
- `meta_spec/` is intentionally ignored because it targets the later journal-paper version.
- Experimental results remain TBD by request; result claims are therefore written as protocol/design claims, not performance claims.

## Reject-first risk summary

A critical AUPEC reviewer may reject the paper if it reads only as a simulator description without numerical evidence. The current mitigation is to sharpen the contribution around the event-driven two-line MDP, shared-vs-split budget accounting, and transparent engineering data construction. Once experiments are available, the paper must add at least one strong empirical message: e.g., whether shared accounting reduces total overload duration, whether THP1 yields charging windows to THZ1, and how PPO compares with MPC/search baselines under E1--E4.

## Claim audit

- Formulation claims are supported by `spec/01`, `spec/03`, `spec/07`, and `lrt_sim/plan2_env.py`.
- Data-source claims are supported by `data/case_haizhu/README.md` and `data/case_huangpu/README.md`.
- Algorithm claims are supported by `lrt_sim/ppo.py`, `lrt_sim/search_baselines.py`, `lrt_sim/mpc_baseline.py`, and `lrt_sim/baselines.py`.
- Performance claims are intentionally absent or marked TBD.

## Changes made during review

- Added a Related Work section to prevent the contribution from looking isolated.
- Softened result-language in the abstract from “is compared” to “evaluation protocol covers”.
- Added a pipeline-figure placeholder so the conference structure has a clear visual anchor.
- Explicitly stated novelty is in the event-driven two-line formulation, not a new RL algorithm.
- Removed Unicode-heavy Chinese URLs from BibTeX entries and pointed to case-data README records instead.

## Remaining before submission

- Replace all `\todo{}` / `[TBD]` markers with actual values or final author metadata.
- Replace the pipeline placeholder with a real figure.
- Fill Table I and Table II using the final `paper_outputs/plan2` summaries.
- Add one or two power-trace figures and one budget-pooling trade-off plot.
- If page limit is tight, compress Related Work and move detailed data-source discipline into a short paragraph.

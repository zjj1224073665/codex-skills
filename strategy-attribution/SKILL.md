---
name: strategy-attribution
description: "Use when analyzing quant trading strategy performance attribution, old vs new strategy variants, normalization or gate changes, in-sample vs out-of-sample failure, and HTML reports that need hypothesis-driven statistical validation plus plain-language factor logic."
---

# Strategy Attribution

## Overview

Use this skill to turn a quant strategy performance question into a falsifiable attribution report. The standard is: explain why the strategy changed or failed, not only how much Sharpe, net PnL, or drawdown changed.

Separate formal backtest metrics from diagnostic attribution. Counterfactual common-window tests are useful for marginal contribution, but they should be labeled as diagnostics unless they exactly match the official backtest engine.

## Workflow

### 1. Pin Down The Question

- Identify the strategy directories, artifacts, official backtest outputs, saved signals, and any modified versions.
- Define base vs new variants, in-sample vs out-of-sample splits, and the common time window used for fair comparison.
- State the user or mentor's real decision question, such as "should we switch normalization", "did the raw factor decay", or "which layer caused OOS loss".
- Preserve paths, assumptions, fee formula, timezone, and sampling frequency in the report.

### 2. Reconstruct The Signal Pipeline

Break the strategy into economic layers before looking at aggregate performance:

- Raw factor or raw momentum signal.
- Condition or gate layer: when the strategy is allowed to trade.
- Normalization and scaling: z-score, std-only scaling, clipping, ranks, smoothing.
- Position construction: sign, magnitude, lag, holding rule, leverage cap.
- Costs: turnover, fee rate, slippage assumptions.

For z-score or normalization changes, write the formula and the extra meaning it introduces. For example, subtracting a rolling mean can turn a raw momentum signal into a "relative to recent history" acceleration or cooling signal.

### 3. Generate Hypotheses First

Before testing, list falsifiable hypotheses. If subagent tools are available and the user wants deeper investigation, use separate agents for market structure, factor logic, and statistical validation, then synthesize their proposals.

Good hypotheses name a proxy variable and a falsification test:

- Raw factor decay: raw signal sign no longer predicts forward return.
- Gate failure: the condition selects the wrong regime or leaves exposure when it should be flat.
- Normalization artifact: z-score mean subtraction flips sign or creates residual exposure.
- Market structure shift: historical edge depended on rebound, volatility, liquidity, or autocorrelation patterns that changed OOS.
- Cost problem: turnover rose enough that gross edge survived but net edge died.
- Implementation bug: timestamp alignment, fillna, shifted masks, or saved signal mismatch changed behavior.

Do not accept a story because it sounds plausible. Require at least one statistic, event study, or historical analog that could have contradicted it.

### 4. Build Counterfactual Variants

Use counterfactuals to isolate marginal contribution. Typical variants:

- Old saved signal or official old output.
- Old signal with only the new gate applied after signal generation.
- New normalization with the same gate.
- Raw momentum sign with the same gate.
- Optional no-fee, fee-only, long-only, short-only, gate-on, and gate-off slices.

Run all variants on the same timestamps and with the same fee formula. Report gross PnL, fees, net PnL, Sharpe, max drawdown, average absolute position, and turnover. State clearly that this does not replace the official full backtest unless the engines match exactly.

### 5. Attribute By Components

Decompose PnL into interpretable buckets:

- Gate-on vs gate-off periods.
- Same sign vs sign-flip between old and new signals.
- Zero raw signal but nonzero normalized position.
- Long vs short exposure.
- High volatility vs low volatility.
- Downtrend, rebound, range, and trend continuation regimes.
- Specific condition families, such as extreme condition, middle bucket, or no-trade bucket.

Translate internal labels into plain language in the report. For example, "gate-off residual" means: the economic gate says do not trade, but the old normalization still leaves a leftover position because it subtracts historical mean.

### 6. Test Market And Factor Logic

If the key question is "why did this work in-sample but fail out-of-sample", do not stop at the normalization artifact. Test the market structure that made the artifact useful before and harmful now:

- Compare OOS with similar historical windows by cumulative return, drawdown, realized volatility, path persistence, and rebound after sharp drops.
- Test whether historical losses or gains came from rebound after selloffs, trend-following continuation, or mean-reversion after signal cooling.
- Check whether similar down markets existed in-sample. If they did, compare how much they rebounded and how the strategy behaved then.
- Verify whether the raw factor still has directional edge. If raw sign still works but z-score fails, the issue is likely the processing layer, not pure factor decay.
- Look for distribution shift in gate states, signal magnitude, sign flips, and turnover.

Use concrete phrases instead of vague regime labels. Prefer "low-rebound, persistent down move" to a custom term that readers have not agreed on.

### 7. Write The Report

Recommended HTML report structure:

- Executive conclusion: one paragraph that answers the decision question.
- Official performance comparison: old vs new, with IS and OOS separated.
- Counterfactual attribution: what changed because of gate, normalization, raw factor, and costs.
- Why section: the best causal explanation, supporting evidence, and rejected alternatives.
- Market analogs: similar historical windows and how they differ from OOS.
- Factor logic: what the signal is economically betting on.
- Next actions: targeted fixes or tests, not broad tuning advice.

Every table should have a short "how to read this" explanation. Avoid unexplained professional shorthand; define terms the first time they appear or rename them in plain language.

### 8. Quality Bar

- Align timestamps and lags explicitly; avoid lookahead.
- Use common windows for counterfactual comparison.
- Check that component PnL sums back to total PnL within tolerance.
- Cast shifted or filled gates to boolean before mask logic.
- Keep saved official signals separate from recomputed diagnostic signals.
- Show both gross and net results whenever turnover or fee changes.
- Mark unsupported causal claims as hypotheses, not conclusions.
- If a term confuses the user, remove it or replace it with measurable plain language.

## Reference

For full report work, load `references/attribution_checklist.md`.

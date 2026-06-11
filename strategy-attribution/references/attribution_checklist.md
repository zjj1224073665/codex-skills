# Strategy Attribution Checklist

Use this checklist when producing or reviewing a quant strategy attribution report.

## Minimum Inputs

- Strategy paths and variant names.
- Official backtest metrics and saved signals, if available.
- Price or return series used for PnL.
- Fee formula, turnover definition, sampling frequency, and timezone.
- In-sample and out-of-sample split dates.
- Code implementing raw factor, gate, normalization, clipping, and position generation.

## Core Tables

Create these tables when the data supports them:

- Official old vs new metrics: net return, Sharpe, max drawdown, turnover, average position.
- Common-window counterfactual metrics: old, old plus gate, new normalization, raw sign plus gate.
- IS vs OOS attribution: same metrics split by period.
- Component PnL: gate-on, gate-off residual, sign flip, same sign, long, short.
- Market analogs: similar historical windows with return, rebound, volatility, and strategy net PnL.
- Gate state distribution: share of time in each state and PnL by state.

## Useful Counterfactuals

- Keep raw factor fixed and change only normalization.
- Keep normalization fixed and change only gate.
- Set position to zero when gate is off.
- Use raw sign only to test whether direction survives without magnitude processing.
- Remove fees to separate gross edge from turnover drag.
- Clip or unclip positions to see whether tail sizing caused damage.

## Z-Score Failure Diagnostics

For a signal like:

```text
z = (raw_signal - rolling_mean(raw_signal)) / rolling_std(raw_signal)
```

test these effects:

- Mean-sticky residual: raw signal is zero or flat, but z-score is nonzero because the rolling mean is not zero.
- Sign flip: raw signal and z-score have opposite signs.
- Hidden reversal logic: a positive raw signal that is weaker than recent history becomes a short or flat signal.
- Hidden acceleration logic: the strategy trades whether momentum is stronger or weaker than its own recent average, not only whether momentum is positive or negative.
- Regime dependence: the hidden logic helps when selloffs rebound, but hurts when price keeps moving in one direction with weak rebound.

## Market Structure Tests

For OOS failure, compare with historical analogs instead of only saying "regime shift":

- Search for windows with similar cumulative return over the same horizon.
- Compare forward rebound after large down bars, for example next 24h or 48h return after sharp drops.
- Measure path persistence with simple metrics such as return autocorrelation, fraction of down bars, and drawdown duration.
- Compare realized volatility and turnover.
- Check whether similar in-sample windows were profitable or unprofitable for the same component.

Use simple names in the report, such as "low-rebound downtrend", only after defining the exact metrics used.

## Plain-Language Translations

- "Gate": the condition that decides whether the strategy is allowed to hold a position.
- "Gate-off residual": leftover position while the gate says no trade.
- "Normalization artifact": a position created by scaling or de-meaning rather than by the raw economic signal.
- "Sign flip": raw factor points one way, processed signal points the other way.
- "Common-window attribution": a diagnostic comparison where all variants are forced onto the same timestamps and fee assumptions.

## Report Guardrails

- Do not bury the conclusion after many plots.
- Do not present a counterfactual diagnostic as the official live/backtest result.
- Do not claim the raw factor is dead if raw sign still works.
- Do not claim the market structure changed without historical analog evidence.
- Do not use custom jargon if a reader has already said it is confusing.
- Keep the final explanation tied to a decision: keep old, switch new, add gate, change normalization, or run more tests.

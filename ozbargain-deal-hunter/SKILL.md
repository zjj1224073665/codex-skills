---
name: ozbargain-deal-hunter
description: Scan OzBargain public deal pages, extract current deal candidates, and use AI judgment plus reusable heuristics to surface genuinely strong bargains instead of noisy discounts. Use when the user asks to check OzBargain, find today's best Australian deals, rank real bargains, summarize daily OzBargain posts, or filter OzBargain deal noise.
---

# OzBargain Deal Hunter

## Overview

Use this skill to turn OzBargain's high-volume deal feed into a short, purchase-oriented shortlist. Combine the bundled scanner's structured candidate output with independent judgment about real value, hidden conditions, expiry, stock, cashback risk, seller risk, and whether the community evidence supports the deal.

## Daily Workflow

1. Run the scanner first:

```bash
python3 "$HOME/Documents/codex-skills/ozbargain-deal-hunter/scripts/scan_ozbargain.py" \
  --pages 2 \
  --max-age-hours 30 \
  --details 8 \
  --limit 15
```

2. Read `references/evaluation.md` when turning scanner output into final recommendations.
3. Do not simply repeat the scanner ranking. Use it as a candidate pool, then apply AI judgment.
4. For any expensive item, cashback-dependent offer, subscription-dependent offer, travel offer, grey-market seller, or unusually high score, verify the current merchant page and at least one comparison or historical-price source when available.
5. Output only the strongest deals plus a small "watch/verify" section. Avoid dumping all posts.

## Output Style

Produce a concise daily brief:

- **Buy / Seriously Consider**: 3-8 deals with the strongest evidence.
- **Watch / Verify**: deals that might be good but need stock, price, cashback, membership, or model/version verification.
- **Skip Signals**: short explanation of common noise found today, such as cashback-only posts, inflated RRP, delivery killing the discount, targeted deals, or low community confidence.

For each recommended deal include:

- deal title and OzBargain link
- merchant and category
- why it looks genuinely good
- main caveat or verification step
- urgency only when expiry, stock, or community comments justify it

## Scanner Notes

The scanner reads public OzBargain pages only. It extracts deal title, votes, comments, category, merchant domain, coupon code, expiry text, snippet, tags such as Affiliate/Marketing/Long Running, and optional comment signals from detail pages.

Useful scanner options:

- `--pages N`: fetch multiple `/deals` pages.
- `--details N`: fetch detail/comment pages for the top N heuristic candidates.
- `--max-age-hours N`: keep the daily scan focused.
- `--prefer TERM`: boost user-interest terms, repeatable.
- `--exclude TERM`: heavily penalize unwanted terms, repeatable.
- `--category NAME`: include categories containing this text, repeatable.
- `--json`: emit structured JSON for deeper processing.

If the same fetch or parse error occurs twice, research the current OzBargain page/feed behavior and identify 3-5 fixes before changing the scanner.

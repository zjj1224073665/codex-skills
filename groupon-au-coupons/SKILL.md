---
name: groupon-au-coupons
description: Find current Groupon Australia promo codes, voucher codes, coupon links, and deal-specific savings. Use when Codex is asked to search for Groupon AU discounts, OzBargain Groupon codes, Google-discovered Groupon Australia coupons, or to compare likely-working coupon options before a Groupon purchase.
---

# Groupon AU Coupons

## Overview

Find likely-working Groupon Australia coupon codes and deal links, verify freshness, and return a short ranked list the user can try before checkout.

## Quick Workflow

1. Clarify the target only if needed. If the user gives no product, city, category, or budget, run a broad Groupon Australia coupon search first.
2. Use live web search because coupon availability changes quickly. Prefer sources with current dates, active comments, or an official Groupon AU page.
3. Generate focused queries with `scripts/generate_queries.py` when the request includes a product, category, city, or general coupon hunt.
4. Read `references/source-checklist.md` when ranking unfamiliar coupon pages or deciding whether a code is worth presenting.
5. Test each candidate by checking source freshness and restrictions. If direct checkout validation is not possible, say that the code is unverified at checkout.
6. Return the best 3 to 5 options with code/link, estimated saving, restrictions, source, and confidence.

## Search Process

Use several query styles, not just one coupon site:

```bash
python3 scripts/generate_queries.py --term "massage Sydney" --category beauty
python3 scripts/generate_queries.py --city Melbourne
python3 scripts/generate_queries.py
```

Search priority:

1. Groupon Australia pages for official deals, sale banners, app-only offers, and checkout restrictions.
2. OzBargain threads for community-tested codes, expiry reports, and comments about exclusions.
3. Search results for coupon aggregators only when they show recent update dates and exact Groupon AU terms.
4. General Google-style searches for the user's category or city when no broad code is useful.

Useful manual query patterns:

```text
Groupon Australia promo code
Groupon AU coupon code today
site:ozbargain.com.au Groupon coupon
site:ozbargain.com.au Groupon promo code
site:groupon.com.au <city or category> deal
"Groupon Australia" "<term>" "promo code"
```

## Ranking Rules

Rank candidates by:

1. Verified or recently discussed on OzBargain, especially with successful user comments.
2. Official Groupon AU page, email-style promotion, app banner, or category sale.
3. Recent coupon aggregator page with a specific code, terms, and expiry date.
4. Broad or old coupon pages only if no better option exists.

Do not present a code as working unless a source shows recent use or checkout validation confirms it. Use labels such as `likely working`, `official sale`, `unverified at checkout`, or `low confidence`.

## Output Format

Keep the answer short and actionable:

```text
Best options I found:
1. CODE - 15% off selected local deals. Source: OzBargain, posted <date>. Confidence: likely working. Notes: excludes ...
2. Official Groupon AU sale link - up to 30% off beauty deals. Source: Groupon AU. Confidence: official sale. Notes: no code needed.

I would try CODE first, then the official sale link. I could not verify checkout success without logging in or starting a purchase.
```

Include direct source links. Mention exact dates when dates are visible. Never log in, purchase, or alter the user's Groupon account unless the user explicitly asks and confirms the action.

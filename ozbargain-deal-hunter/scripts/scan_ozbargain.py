#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import html
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - old Python fallback
    ZoneInfo = None


BASE_URL = "https://www.ozbargain.com.au"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (compatible; Codex OzBargain Deal Hunter; "
    "+https://www.ozbargain.com.au/)"
)
SYDNEY_TZ = ZoneInfo("Australia/Sydney") if ZoneInfo else dt.timezone(dt.timedelta(hours=10))


POSITIVE_PATTERNS = [
    ("all-time low", r"\b(all[- ]?time low|atl|lowest ever|record low|historical low)\b", 14),
    ("price match / beat", r"\b(price match|price beat|price check)\b", 7),
    ("stackable", r"\b(stack|stackable|combine|combined with|cashback on top)\b", 6),
    ("clearance", r"\b(clearance|runout|end of financial year|eofy)\b", 5),
    ("free delivery", r"\b(free delivery|delivered|free shipping|\$0 c&c|click and collect)\b", 4),
    ("local warranty", r"\b(australian warranty|local warranty|official store|authorised reseller)\b", 5),
]

RISK_PATTERNS = [
    ("cashback dependent", r"\b(cashback|shopback|cashrewards|topcashback)\b", -8),
    ("targeted/limited eligibility", r"\b(targeted|selected accounts|invitation only|new customers only|first order|student only)\b", -11),
    ("membership/subscription", r"\b(ebay plus|prime|onepass|kogan first|subscription|membership)\b", -5),
    ("minimum spend", r"\b(min(?:imum)? spend|spend over|spend \$|when you spend)\b|\$\d+(?:\.\d+)?\s+off\s+\$[0-9]", -7),
    ("shipping may hurt value", r"\b(\+ delivery|\+ shipping|postage|excluding delivery|shipping not included)\b", -6),
    ("refurbished/grey import", r"\b(refurb|refurbished|grey import|international version|import model)\b", -7),
    ("preorder/backorder", r"\b(pre[- ]?order|backorder|back order|ships in)\b", -5),
    ("out of stock / expired", r"\b(out of stock|oos|expired|sold out|no stock)\b", -25),
    ("inflated headline", r"\b(up to \d{1,3}% off|from \$|selected styles|selected items)\b", -4),
]

COMMENT_WARNING_PATTERNS = [
    r"\b(out of stock|oos|expired|sold out|no stock)\b",
    r"\b(cheaper|same price|not a deal|bad deal|overpriced)\b",
    r"\b(price jack|pricejacking|inflated rrp|wrong model)\b",
    r"\b(did not track|declined cashback|cashback excluded)\b",
    r"\b(postage kills|delivery kills|shipping kills)\b",
]

COMMENT_SUPPORT_PATTERNS = [
    r"\b(ordered|bought|worked|confirmed|price matched|tracked|delivered)\b",
    r"\b(good deal|great deal|bargain|excellent price|lowest)\b",
]

KNOWN_RETAILER_DOMAINS = {
    "amazon.com.au",
    "ebay.com.au",
    "thegoodguys.com.au",
    "jbhifi.com.au",
    "officeworks.com.au",
    "bunnings.com.au",
    "bigw.com.au",
    "kmart.com.au",
    "target.com.au",
    "woolworths.com.au",
    "coles.com.au",
    "chemistwarehouse.com.au",
    "harveynorman.com.au",
    "binglee.com.au",
    "davidjones.com",
    "myer.com.au",
    "rebel.com.au",
    "repco.com.au",
    "supercheapauto.com.au",
    "appliancesonline.com.au",
    "lenovo.com",
    "dell.com",
    "microsoft.com",
    "store.steampowered.com",
    "gog.com",
}


@dataclasses.dataclass
class Deal:
    deal_id: str
    title: str
    url: str
    external_domain: str = ""
    category: str = ""
    posted_at: str = ""
    posted_iso: str = ""
    age_hours: float | None = None
    votes_up: int = 0
    votes_down: int = 0
    comments: int = 0
    snippet: str = ""
    coupon: str = ""
    expiry: str = ""
    tags: list[str] = dataclasses.field(default_factory=list)
    score: float = 0.0
    rating: str = "skip"
    reasons: list[str] = dataclasses.field(default_factory=list)
    cautions: list[str] = dataclasses.field(default_factory=list)
    comment_support: list[str] = dataclasses.field(default_factory=list)
    comment_warnings: list[str] = dataclasses.field(default_factory=list)

    @property
    def net_votes(self) -> int:
        return self.votes_up - self.votes_down

    @property
    def vote_velocity(self) -> float | None:
        if self.age_hours is None:
            return None
        return self.net_votes / max(self.age_hours, 1.0)


def fetch_url(url: str, timeout: int = 25, user_agent: str = DEFAULT_USER_AGENT) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-AU,en;q=0.9",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def strip_tags(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style).*?</\1>", " ", raw)
    raw = re.sub(r"(?i)<br\s*/?>", "\n", raw)
    raw = re.sub(r"(?is)<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = raw.replace("\xa0", " ")
    return re.sub(r"\s+", " ", raw).strip()


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(value or "").replace("\xa0", " ")).strip()


def first_int(pattern: str, text: str, default: int = 0, flags: int = re.S) -> int:
    match = re.search(pattern, text, flags)
    if not match:
        return default
    try:
        return int(match.group(1).replace(",", ""))
    except ValueError:
        return default


def parse_posted(block: str, now: dt.datetime) -> tuple[str, str, float | None]:
    match = re.search(r"\bon\s+(\d{2}/\d{2}/\d{4})\s+-\s+(\d{2}:\d{2})", block)
    if not match:
        return "", "", None
    posted_at = f"{match.group(1)} - {match.group(2)}"
    try:
        naive = dt.datetime.strptime(f"{match.group(1)} {match.group(2)}", "%d/%m/%Y %H:%M")
        aware = naive.replace(tzinfo=SYDNEY_TZ)
        age = (now - aware).total_seconds() / 3600
        return posted_at, aware.isoformat(), max(age, 0.0)
    except ValueError:
        return posted_at, "", None


def extract_node_blocks(page_html: str) -> list[str]:
    parts = re.split(r"(?=<div class=\"node node-ozbdeal node-(?:teaser|full)\" id=\"node\d+\">)", page_html)
    return [part for part in parts if part.startswith('<div class="node node-ozbdeal')]


def parse_deal_block(block: str, now: dt.datetime) -> Deal | None:
    id_match = re.search(r'id="node(\d+)"', block)
    if not id_match:
        return None
    deal_id = id_match.group(1)

    title_match = re.search(r"<h2[^>]*\bdata-title=\"([^\"]+)\"", block, re.S)
    if title_match:
        title = clean_text(title_match.group(1))
    else:
        heading = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.S)
        title = strip_tags(heading.group(1)) if heading else f"OzBargain deal {deal_id}"

    posted_at, posted_iso, age_hours = parse_posted(block, now)

    vote_section = re.search(r'<div class="n-vote[^"]*"[^>]*>(.*?)</div>', block, re.S)
    vote_html = vote_section.group(1) if vote_section else block
    votes_up = first_int(r'class="nvb voteup"[^>]*>.*?<span>(-?\d+)</span>', vote_html)
    votes_down = first_int(r'class="nvb votedown"[^>]*>.*?<span>(-?\d+)</span>', vote_html)

    comments = first_int(r'<i class="fa fa-comment"></i>\s*([0-9,]+)', block)

    external_domain = ""
    via_match = re.search(r'<span class="via">.*?<a [^>]*>(.*?)</a>', block, re.S)
    if via_match:
        external_domain = strip_tags(via_match.group(1)).lower()

    category = ""
    category_match = re.search(r'<span class="tag">.*?<a href="/cat/[^"]+">(.*?)</a>', block, re.S)
    if category_match:
        category = strip_tags(category_match.group(1))

    content = ""
    content_match = re.search(r'<div class="content">\s*(.*?)(?=<div class="links"\s+id=)', block, re.S)
    if content_match:
        content = strip_tags(content_match.group(1))

    coupon = ""
    coupon_match = re.search(r'<div class="couponcode"[^>]*>.*?<strong>(.*?)</strong>', block, re.S)
    if coupon_match:
        coupon = strip_tags(coupon_match.group(1))

    expiry = ""
    expiry_match = re.search(r'<span class="nodeexpiry"[^>]*>(.*?)</span>\s*</li>', block, re.S)
    if expiry_match:
        expiry = strip_tags(expiry_match.group(1))

    tags: list[str] = []
    for tag_match in re.finditer(r'<(?:span|a)[^>]*class="[^"]*\btagger\b[^"]*"[^>]*>(.*?)</(?:span|a)>', block, re.S):
        tag = strip_tags(tag_match.group(1))
        if tag and tag not in tags:
            tags.append(tag)
    if "nodefreebie" in block and "Freebie" not in tags:
        tags.append("Freebie")

    return Deal(
        deal_id=deal_id,
        title=title,
        url=f"{BASE_URL}/node/{deal_id}",
        external_domain=external_domain,
        category=category,
        posted_at=posted_at,
        posted_iso=posted_iso,
        age_hours=age_hours,
        votes_up=votes_up,
        votes_down=votes_down,
        comments=comments,
        snippet=content,
        coupon=coupon,
        expiry=expiry,
        tags=tags,
    )


def parse_deals(page_html: str, now: dt.datetime) -> list[Deal]:
    deals: list[Deal] = []
    seen: set[str] = set()
    for block in extract_node_blocks(page_html):
        deal = parse_deal_block(block, now)
        if deal and deal.deal_id not in seen:
            deals.append(deal)
            seen.add(deal.deal_id)
    return deals


def price_numbers(text: str) -> list[float]:
    numbers = []
    for raw in re.findall(r"\$([0-9][0-9,]*(?:\.[0-9]{1,2})?)", text):
        try:
            numbers.append(float(raw.replace(",", "")))
        except ValueError:
            pass
    return numbers


def detect_discount_signal(text: str) -> tuple[float, str | None]:
    value_context = re.search(
        r"\b(rrp|was|normally|usually|original(?:ly)?|down from|reduced from|save[d]?)\b",
        text,
        re.I,
    )
    prices = price_numbers(text)
    if value_context and len(prices) >= 2:
        low = min(prices)
        high = max(prices)
        if high >= 10 and low < high:
            pct = (high - low) / high * 100
            if pct >= 30:
                return min(15.0, pct / 5.0), f"headline price implies about {pct:.0f}% off"

    pct_matches = [int(p) for p in re.findall(r"\b([1-9][0-9])\s*%\s*off\b", text.lower())]
    if pct_matches:
        pct = max(pct_matches)
        if pct >= 30:
            return min(12.0, pct / 6.0), f"headline claims {pct}% off"
    return 0.0, None


def add_unique(target: list[str], item: str) -> None:
    if item and item not in target:
        target.append(item)


def score_deal(deal: Deal, prefer_terms: list[str], exclude_terms: list[str]) -> Deal:
    score = 0.0
    reasons: list[str] = []
    cautions: list[str] = []
    searchable = " ".join(
        [deal.title, deal.snippet, deal.category, deal.external_domain, " ".join(deal.tags)]
    ).lower()

    net = deal.net_votes
    if net > 0:
        vote_score = min(35.0, net * 0.55)
        score += vote_score
        if net >= 30:
            add_unique(reasons, f"community support: +{deal.votes_up}/-{deal.votes_down} votes")
    if deal.votes_down:
        down_penalty = min(10.0, deal.votes_down * 1.5)
        score -= down_penalty
        add_unique(cautions, f"{deal.votes_down} downvotes")

    if deal.vote_velocity is not None:
        velocity = deal.vote_velocity
        score += min(22.0, max(0.0, velocity) * 4.0)
        if velocity >= 6:
            add_unique(reasons, f"fast vote velocity: {velocity:.1f} net votes/hour")
        elif velocity < 0.5 and (deal.age_hours or 0) >= 4:
            score -= 5
            add_unique(cautions, "weak vote velocity for its age")

    if deal.comments:
        score += min(10.0, deal.comments * 0.3)
        if deal.comments >= 20:
            add_unique(reasons, f"{deal.comments} comments to inspect")

    discount_score, discount_reason = detect_discount_signal(searchable)
    score += discount_score
    if discount_reason:
        add_unique(reasons, discount_reason)

    for label, pattern, points in POSITIVE_PATTERNS:
        if re.search(pattern, searchable, re.I):
            score += points
            add_unique(reasons, label)

    for label, pattern, points in RISK_PATTERNS:
        if re.search(pattern, searchable, re.I):
            score += points
            add_unique(cautions, label)

    tag_text = " ".join(deal.tags).lower()
    if "affiliate" in tag_text:
        score -= 4
        add_unique(cautions, "affiliate-tagged post")
    if "marketing" in tag_text or "employee" in tag_text:
        score -= 7
        add_unique(cautions, "seller/employee/marketing post")
    if "long running" in tag_text:
        score -= 3
        add_unique(cautions, "long-running deal; verify current value")
    if "freebie" in tag_text:
        score += 5
        add_unique(reasons, "freebie")

    if deal.external_domain in KNOWN_RETAILER_DOMAINS:
        score += 3
        add_unique(reasons, "known retailer domain")

    for term in prefer_terms:
        if term.lower() in searchable:
            score += 6
            add_unique(reasons, f"matches preference: {term}")
    for term in exclude_terms:
        if term.lower() in searchable:
            score -= 35
            add_unique(cautions, f"matches exclude term: {term}")

    if deal.comment_support:
        boost = min(10.0, 2.0 * len(deal.comment_support))
        score += boost
        add_unique(reasons, f"supportive comments: {len(deal.comment_support)}")
    if deal.comment_warnings:
        penalty = min(20.0, 4.0 * len(deal.comment_warnings))
        score -= penalty
        add_unique(cautions, f"warning comments: {len(deal.comment_warnings)}")

    deal.score = round(max(0.0, score), 1)
    deal.reasons = reasons[:7]
    deal.cautions = cautions[:7]
    if deal.score >= 70:
        deal.rating = "strong"
    elif deal.score >= 50:
        deal.rating = "worth checking"
    elif deal.score >= 35:
        deal.rating = "watch"
    else:
        deal.rating = "skip"
    return deal


def parse_comment_signals(detail_html: str, max_samples: int = 4) -> tuple[list[str], list[str]]:
    support: list[tuple[int, str]] = []
    warnings: list[tuple[int, str]] = []
    chunks = re.split(r'(?=<div class="comment-wrap" id="comment-\d+")', detail_html)
    for chunk in chunks:
        if not chunk.startswith('<div class="comment-wrap"'):
            continue
        score = first_int(r'<span class="cvc"[^>]*>(-?\d+)</span>', chunk, default=0)
        content_match = re.search(r'<div class="content[^"]*"[^>]*>(.*?)(?=</div>\s*<ul class="links">)', chunk, re.S)
        if not content_match:
            continue
        text = strip_tags(content_match.group(1))
        if not text:
            continue
        lower = text.lower()
        if any(re.search(pattern, lower, re.I) for pattern in COMMENT_WARNING_PATTERNS):
            warnings.append((score, shorten(text, 180)))
        elif any(re.search(pattern, lower, re.I) for pattern in COMMENT_SUPPORT_PATTERNS):
            support.append((score, shorten(text, 180)))

    support.sort(key=lambda item: item[0], reverse=True)
    warnings.sort(key=lambda item: item[0])
    return [text for _, text in support[:max_samples]], [text for _, text in warnings[:max_samples]]


def shorten(text: str, width: int = 160) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= width:
        return text
    return text[: max(0, width - 3)].rstrip() + "..."


def deal_to_dict(deal: Deal) -> dict:
    data = dataclasses.asdict(deal)
    data["net_votes"] = deal.net_votes
    data["vote_velocity"] = None if deal.vote_velocity is None else round(deal.vote_velocity, 2)
    return data


def build_source_urls(pages: int, source: str) -> list[str]:
    base_path = "/" if source == "frontpage" else "/deals"
    urls = []
    for page in range(max(1, pages)):
        if page == 0:
            urls.append(urllib.parse.urljoin(BASE_URL, base_path))
        else:
            urls.append(f"{urllib.parse.urljoin(BASE_URL, base_path)}?page={page}")
    return urls


def render_markdown(
    deals: list[Deal],
    *,
    generated_at: dt.datetime,
    source_urls: list[str],
    fetched_count: int,
    filtered_count: int,
    min_score: float,
    limit: int,
) -> str:
    lines: list[str] = []
    lines.append("# OzBargain deal scan")
    lines.append("")
    lines.append(f"Generated: {generated_at.isoformat(timespec='seconds')}")
    lines.append(f"Sources: {', '.join(source_urls)}")
    lines.append(f"Fetched {fetched_count} deals; filtered {filtered_count} by age/category/score.")
    lines.append(f"Showing up to {limit} deals with score >= {min_score:g}.")
    lines.append("")

    if not deals:
        lines.append("No new deals cleared the current threshold.")
        return "\n".join(lines)

    best = [deal for deal in deals if deal.rating in {"strong", "worth checking"}]
    watch = [deal for deal in deals if deal.rating == "watch"]

    if best:
        lines.append("## Buy / seriously consider")
        lines.append("")
        for index, deal in enumerate(best[:limit], 1):
            lines.extend(render_deal(index, deal))
    if watch:
        lines.append("## Watch / verify")
        lines.append("")
        start = 1
        for index, deal in enumerate(watch[: max(0, limit - len(best))], start):
            lines.extend(render_deal(index, deal))
    return "\n".join(lines).rstrip() + "\n"


def render_deal(index: int, deal: Deal) -> list[str]:
    velocity = "unknown"
    if deal.vote_velocity is not None:
        velocity = f"{deal.vote_velocity:.1f}/hour"
    meta = []
    if deal.external_domain:
        meta.append(deal.external_domain)
    if deal.category:
        meta.append(deal.category)
    if deal.posted_at:
        meta.append(deal.posted_at)
    if deal.expiry:
        meta.append(f"expiry: {deal.expiry}")

    lines = [
        f"### {index}. [{deal.rating}, score {deal.score:g}] {deal.title}",
        f"- Link: {deal.url}",
        f"- Meta: {' | '.join(meta) if meta else 'n/a'}",
        f"- Community: +{deal.votes_up}/-{deal.votes_down}, {deal.comments} comments, velocity {velocity}",
    ]
    if deal.coupon:
        lines.append(f"- Coupon: `{deal.coupon}`")
    if deal.tags:
        lines.append(f"- Tags: {', '.join(deal.tags)}")
    if deal.reasons:
        lines.append(f"- Why: {'; '.join(deal.reasons)}")
    if deal.cautions:
        lines.append(f"- Check: {'; '.join(deal.cautions)}")
    if deal.comment_support:
        lines.append(f"- Supportive comment signals: {' / '.join(deal.comment_support[:2])}")
    if deal.comment_warnings:
        lines.append(f"- Warning comment signals: {' / '.join(deal.comment_warnings[:2])}")
    if deal.snippet:
        lines.append(f"- Snippet: {shorten(deal.snippet, 220)}")
    lines.append("")
    return lines


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan OzBargain public deal pages and rank likely genuine bargains.")
    parser.add_argument("--pages", type=int, default=2, help="Number of listing pages to scan from /deals.")
    parser.add_argument("--source", choices=["deals", "frontpage"], default="deals", help="Listing source to scan.")
    parser.add_argument("--max-age-hours", type=float, default=36, help="Discard deals older than this many hours.")
    parser.add_argument("--min-score", type=float, default=35, help="Minimum heuristic score to output.")
    parser.add_argument("--limit", type=int, default=15, help="Maximum deals to output.")
    parser.add_argument("--details", type=int, default=0, help="Fetch detail/comment pages for the top N candidates.")
    parser.add_argument("--sleep", type=float, default=0.5, help="Delay between network requests.")
    parser.add_argument("--prefer", action="append", default=[], help="Boost deals containing this term. Repeatable.")
    parser.add_argument("--exclude", action="append", default=[], help="Penalize deals containing this term. Repeatable.")
    parser.add_argument("--category", action="append", default=[], help="Only include categories containing this term. Repeatable.")
    parser.add_argument("--exclude-category", action="append", default=[], help="Exclude categories containing this term. Repeatable.")
    parser.add_argument("--include-expired", action="store_true", help="Do not filter titles marked expired.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args(argv)


def category_allowed(deal: Deal, include_terms: list[str], exclude_terms: list[str]) -> bool:
    category = deal.category.lower()
    if include_terms and not any(term.lower() in category for term in include_terms):
        return False
    if exclude_terms and any(term.lower() in category for term in exclude_terms):
        return False
    return True


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    now = dt.datetime.now(tz=SYDNEY_TZ)
    source_urls = build_source_urls(args.pages, args.source)

    all_deals: list[Deal] = []
    fetch_errors: list[str] = []
    for index, url in enumerate(source_urls):
        try:
            page = fetch_url(url)
            all_deals.extend(parse_deals(page, now))
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            fetch_errors.append(f"{url}: {exc}")
        if index < len(source_urls) - 1:
            time.sleep(max(0.0, args.sleep))

    deduped: dict[str, Deal] = {}
    for deal in all_deals:
        deduped.setdefault(deal.deal_id, deal)
    fetched = list(deduped.values())

    candidates: list[Deal] = []
    filtered_count = 0
    for deal in fetched:
        if deal.age_hours is not None and deal.age_hours > args.max_age_hours:
            filtered_count += 1
            continue
        tag_text = " ".join(deal.tags)
        if not args.include_expired and re.search(r"\b(expired|out of stock|oos|sold out)\b", f"{deal.title} {tag_text}", re.I):
            filtered_count += 1
            continue
        if not category_allowed(deal, args.category, args.exclude_category):
            filtered_count += 1
            continue
        candidates.append(score_deal(deal, args.prefer, args.exclude))

    candidates.sort(key=lambda item: (item.score, item.net_votes, item.comments), reverse=True)

    detail_count = min(max(0, args.details), len(candidates))
    for index, deal in enumerate(candidates[:detail_count]):
        if index:
            time.sleep(max(0.0, args.sleep))
        try:
            detail_html = fetch_url(deal.url)
            support, warnings = parse_comment_signals(detail_html)
            deal.comment_support = support
            deal.comment_warnings = warnings
            score_deal(deal, args.prefer, args.exclude)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            add_unique(deal.cautions, f"could not fetch detail comments: {exc}")

    candidates.sort(key=lambda item: (item.score, item.net_votes, item.comments), reverse=True)
    output_deals = [deal for deal in candidates if deal.score >= args.min_score][: args.limit]
    filtered_count += max(0, len(candidates) - len(output_deals))

    if args.json:
        payload = {
            "generated_at": now.isoformat(),
            "sources": source_urls,
            "fetched_count": len(fetched),
            "filtered_count": filtered_count,
            "fetch_errors": fetch_errors,
            "deals": [deal_to_dict(deal) for deal in output_deals],
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        if fetch_errors:
            print("Fetch warnings:", file=sys.stderr)
            for error in fetch_errors:
                print(f"- {error}", file=sys.stderr)
        print(
            render_markdown(
                output_deals,
                generated_at=now,
                source_urls=source_urls,
                fetched_count=len(fetched),
                filtered_count=filtered_count,
                min_score=args.min_score,
                limit=args.limit,
            )
        )
    return 0 if fetched or not fetch_errors else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

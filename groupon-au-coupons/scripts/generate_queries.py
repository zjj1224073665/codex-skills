#!/usr/bin/env python3
"""Generate focused web search queries for Groupon Australia coupons."""

from __future__ import annotations

import argparse


def quoted(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    return f'"{value}"' if " " in value else value


def build_queries(term: str | None, city: str | None, category: str | None) -> list[str]:
    term_q = quoted(term or "")
    city_q = quoted(city or "")
    category_q = quoted(category or "")

    queries = [
        "Groupon Australia promo code",
        "Groupon AU coupon code today",
        "Groupon Australia voucher code",
        "site:ozbargain.com.au Groupon coupon",
        "site:ozbargain.com.au Groupon promo code",
        "site:groupon.com.au Groupon Australia sale",
    ]

    if term_q:
        queries.extend(
            [
                f'"Groupon Australia" {term_q} "promo code"',
                f'"Groupon" {term_q} Australia coupon',
                f"site:groupon.com.au {term_q} deal",
                f"site:ozbargain.com.au Groupon {term_q}",
            ]
        )

    if city_q:
        queries.extend(
            [
                f'"Groupon" {city_q} coupon',
                f"site:groupon.com.au {city_q} deal",
                f"site:ozbargain.com.au Groupon {city_q}",
            ]
        )

    if category_q:
        queries.extend(
            [
                f'"Groupon Australia" {category_q} coupon',
                f"site:groupon.com.au {category_q} sale",
                f"site:ozbargain.com.au Groupon {category_q}",
            ]
        )

    return list(dict.fromkeys(queries))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Print web search queries for finding Groupon Australia coupon codes."
    )
    parser.add_argument("--term", help="Product, merchant, service, or deal text.")
    parser.add_argument("--city", help="Australian city or suburb.")
    parser.add_argument("--category", help="Groupon category such as travel, dining, beauty, or activities.")
    args = parser.parse_args()

    for query in build_queries(args.term, args.city, args.category):
        print(query)


if __name__ == "__main__":
    main()

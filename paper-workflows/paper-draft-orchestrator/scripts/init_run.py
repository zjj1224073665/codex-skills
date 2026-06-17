#!/usr/bin/env python3
"""Initialize a paper drafting run directory."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path


SECTIONS = {
    "abstract": "pending",
    "introduction": "pending",
    "related_work": "pending",
    "method": "pending",
    "experiments": "pending",
    "conclusion": "pending",
}


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def copy_if_provided(src: str | None, dst: Path) -> None:
    if not src:
        return
    source = Path(src).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Input file does not exist: {source}")
    if not dst.exists():
        shutil.copy2(source, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a paper_runs/<run_id> scaffold.")
    parser.add_argument("--run-id", help="Run id. Defaults to timestamp.")
    parser.add_argument("--base-dir", default="paper_runs", help="Base directory for runs.")
    parser.add_argument("--brief", help="Optional paper brief file to copy into inputs/paper_brief.md.")
    parser.add_argument("--target-venue", help="Optional target venue file to copy into inputs/target_venue.md.")
    args = parser.parse_args()

    run_id = args.run_id or dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(args.base_dir).expanduser() / run_id

    dirs = [
        run_dir / "inputs" / "raw_notes",
        run_dir / "inputs" / "figures",
        run_dir / "inputs" / "tables",
        run_dir / "inputs" / "bib",
        run_dir / "state",
        run_dir / "rounds",
        run_dir / "draft",
        run_dir / "reviews",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    copy_if_provided(args.brief, run_dir / "inputs" / "paper_brief.md")
    copy_if_provided(args.target_venue, run_dir / "inputs" / "target_venue.md")

    write_if_missing(
        run_dir / "inputs" / "paper_brief.md",
        "# Paper Brief\n\nDescribe the problem, method, available evidence, target field, and desired output.\n",
    )
    write_if_missing(
        run_dir / "inputs" / "target_venue.md",
        "# Target Venue\n\nUnknown.\n",
    )

    status = {
        "run_id": str(run_dir),
        "stage": "input_inventory",
        "round": 0,
        "target_venue": "unknown",
        "sections": SECTIONS,
        "open_blockers": [],
        "last_updated": dt.date.today().isoformat(),
    }
    write_if_missing(run_dir / "state" / "status.json", json.dumps(status, indent=2) + "\n")
    write_if_missing(run_dir / "state" / "recent_summary.md", "# Recent Summary\n\nRun initialized.\n")
    write_if_missing(run_dir / "state" / "unresolved_questions.md", "# Unresolved Questions\n\n")
    write_if_missing(run_dir / "state" / "section_contracts.json", "{}\n")
    write_if_missing(run_dir / "state" / "evidence_ledger.jsonl", "")
    write_if_missing(run_dir / "state" / "citation_ledger.jsonl", "")

    print(run_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate a paper drafting run directory."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


EVIDENCE_FIELDS = {"claim_id", "claim", "source_file", "confidence", "usable_in_section"}
CITATION_FIELDS = {"citation_id", "key", "claim", "title", "source", "verified"}
UNRESOLVED_MARKERS = ("[EVIDENCE_NEEDED]", "[CITATION_NEEDED]", "[CITATION_KEY_NEEDED]")


def load_json(path: Path, errors: list[str]):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        errors.append(f"Missing JSON file: {path}")
    except json.JSONDecodeError as exc:
        errors.append(f"Invalid JSON in {path}: {exc}")
    return None


def load_jsonl(path: Path, required: set[str], id_field: str, errors: list[str]) -> tuple[list[dict], set[str]]:
    rows: list[dict] = []
    ids: set[str] = set()
    if not path.exists():
        errors.append(f"Missing JSONL file: {path}")
        return rows, ids

    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSONL in {path}:{line_no}: {exc}")
            continue
        missing = sorted(required - row.keys())
        if missing:
            errors.append(f"{path}:{line_no} missing fields: {', '.join(missing)}")
        row_id = row.get(id_field)
        if row_id:
            if row_id in ids:
                errors.append(f"Duplicate {id_field}={row_id} in {path}:{line_no}")
            ids.add(row_id)
        rows.append(row)
    return rows, ids


def validate_rounds(run_dir: Path, errors: list[str]) -> None:
    rounds_dir = run_dir / "rounds"
    if not rounds_dir.exists():
        errors.append(f"Missing rounds directory: {rounds_dir}")
        return
    for round_dir in sorted(p for p in rounds_dir.iterdir() if p.is_dir()):
        if not re.fullmatch(r"round_\d+", round_dir.name):
            continue
        if not (round_dir / "task.md").exists():
            errors.append(f"Missing task.md in {round_dir}")
        if not (round_dir / "outputs" / "handoff_summary.md").exists():
            errors.append(f"Missing outputs/handoff_summary.md in {round_dir}")


def validate_section_contracts(run_dir: Path, evidence_ids: set[str], citation_ids: set[str], errors: list[str]) -> None:
    contracts = load_json(run_dir / "state" / "section_contracts.json", errors)
    if contracts is None:
        return
    if not isinstance(contracts, dict):
        errors.append("section_contracts.json must contain an object")
        return
    for section, contract in contracts.items():
        if not isinstance(contract, dict):
            errors.append(f"Contract for {section} must be an object")
            continue
        for claim_id in contract.get("must_make_claims", []):
            if claim_id not in evidence_ids:
                errors.append(f"Contract {section} references missing evidence id: {claim_id}")
        for citation_id in contract.get("must_use_citations", []):
            if citation_id not in citation_ids:
                errors.append(f"Contract {section} references missing citation id: {citation_id}")


def validate_unresolved_markers(run_dir: Path, allow_unresolved: bool, errors: list[str]) -> None:
    if allow_unresolved:
        return
    for path in sorted((run_dir / "draft").glob("**/*")):
        if not path.is_file() or path.suffix not in {".md", ".tex"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for marker in UNRESOLVED_MARKERS:
            if marker in text:
                errors.append(f"Unresolved marker {marker} in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a paper drafting run.")
    parser.add_argument("run_dir", help="Path to paper run directory.")
    parser.add_argument("--allow-unresolved", action="store_true", help="Allow unresolved evidence/citation markers in drafts.")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    errors: list[str] = []

    for rel in ["inputs", "state", "rounds", "draft", "reviews"]:
        if not (run_dir / rel).exists():
            errors.append(f"Missing directory: {run_dir / rel}")

    status = load_json(run_dir / "state" / "status.json", errors)
    if isinstance(status, dict):
        for field in ["run_id", "stage", "round", "sections", "last_updated"]:
            if field not in status:
                errors.append(f"status.json missing field: {field}")

    _, evidence_ids = load_jsonl(run_dir / "state" / "evidence_ledger.jsonl", EVIDENCE_FIELDS, "claim_id", errors)
    _, citation_ids = load_jsonl(run_dir / "state" / "citation_ledger.jsonl", CITATION_FIELDS, "citation_id", errors)

    validate_section_contracts(run_dir, evidence_ids, citation_ids, errors)
    validate_rounds(run_dir, errors)
    validate_unresolved_markers(run_dir, args.allow_unresolved, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

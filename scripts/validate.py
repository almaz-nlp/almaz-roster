#!/usr/bin/env python3
"""
ALMAZ Resource Registry — validation script
Checks: duplicate IDs, missing fields, controlled values, ID format, link reachability
Usage: python scripts/validate.py [--check-links]
"""

import csv
import re
import sys
import argparse
from collections import Counter

REQUIRED_FIELDS = ["id", "name", "type", "layer", "source", "license", "link"]
VALID_TYPES = {"corpus", "dataset", "benchmark", "model", "tool"}
VALID_LAYERS = {"1", "2", "3", "4", "5"}
ID_PATTERN = re.compile(r"^AZ-(CORP|DATA|BENCH|MODEL|TOOL)-\d{3}$")

def load_registry(path="data/registry.csv"):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def check_duplicates(rows):
    ids = [r["id"] for r in rows]
    dupes = [id_ for id_, count in Counter(ids).items() if count > 1]
    return [f"Duplicate ID: {id_}" for id_ in dupes]

def check_required_fields(rows):
    errors = []
    for i, row in enumerate(rows, 2):
        for field in REQUIRED_FIELDS:
            if not row.get(field, "").strip():
                errors.append(f"Row {i} ({row.get('id','?')}): missing required field '{field}'")
    return errors

def check_controlled_values(rows):
    errors = []
    for i, row in enumerate(rows, 2):
        if row.get("type") not in VALID_TYPES:
            errors.append(f"Row {i} ({row['id']}): invalid type '{row.get('type')}' — must be one of {sorted(VALID_TYPES)}")
        if row.get("layer") not in VALID_LAYERS:
            errors.append(f"Row {i} ({row['id']}): invalid layer '{row.get('layer')}' — must be 1–5")
    return errors

def check_id_format(rows):
    errors = []
    for i, row in enumerate(rows, 2):
        if not ID_PATTERN.match(row.get("id", "")):
            errors.append(f"Row {i}: ID '{row.get('id')}' does not match AZ-TYPE-NNN format")
    return errors

def check_links(rows):
    import urllib.request
    import urllib.error
    errors = []
    for row in rows:
        url = row.get("link", "").strip()
        if not url or not url.startswith("http"):
            continue
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ALMAZ-Registry-Validator/1.0"})
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            errors.append(f"{row['id']}: link unreachable — {url} ({e})")
    return errors

def main():
    parser = argparse.ArgumentParser(description="Validate the ALMAZ registry")
    parser.add_argument("--check-links", action="store_true", help="Also check URL reachability (slow)")
    parser.add_argument("--path", default="data/registry.csv", help="Path to registry CSV")
    args = parser.parse_args()

    print(f"Loading registry from {args.path}...")
    rows = load_registry(args.path)
    print(f"  {len(rows)} artifacts loaded\n")

    all_errors = []
    all_errors += check_duplicates(rows)
    all_errors += check_required_fields(rows)
    all_errors += check_controlled_values(rows)
    all_errors += check_id_format(rows)

    if args.check_links:
        print("Checking links (this may take a moment)...")
        all_errors += check_links(rows)

    if all_errors:
        print(f"VALIDATION FAILED — {len(all_errors)} error(s):\n")
        for err in all_errors:
            print(f"  ERROR: {err}")
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED — {len(rows)} artifacts, 0 errors")
        type_counts = Counter(r["type"] for r in rows)
        for t, c in sorted(type_counts.items()):
            print(f"  {t}: {c}")
        sys.exit(0)

if __name__ == "__main__":
    main()

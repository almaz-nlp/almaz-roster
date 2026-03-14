#!/usr/bin/env python3
"""
ALMAZ Resource Registry — statistics script
Prints a coverage report by type, layer, domain, and license.
Usage: python scripts/stats.py
"""

import csv
from collections import Counter

def load_registry(path="data/registry.csv"):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def section(title):
    print(f"\n{'─' * 40}")
    print(f"  {title}")
    print(f"{'─' * 40}")

def table(counter, label_width=24):
    total = sum(counter.values())
    for key, count in sorted(counter.items(), key=lambda x: -x[1]):
        bar = "█" * count
        pct = count / total * 100
        print(f"  {key:<{label_width}} {count:>4}  {pct:5.1f}%  {bar}")

def main():
    rows = load_registry()
    print(f"\nALMAZ Resource Registry — coverage report")
    print(f"Total artifacts: {len(rows)}")

    section("By type")
    table(Counter(r["type"] for r in rows))

    section("By layer")
    layer_labels = {"1":"L1 raw sources","2":"L2 datasets & corpora",
                    "3":"L3 models","4":"L4 benchmarks","5":"L5 applications"}
    table(Counter(layer_labels.get(r["layer"], r["layer"]) for r in rows))

    section("By license (top 10)")
    table(Counter(r["license"] for r in rows))

    section("By domain tag (top 15)")
    domain_counts = Counter()
    for r in rows:
        for tag in r.get("domain","").split("·"):
            tag = tag.strip()
            if tag:
                domain_counts[tag] += 1
    table(Counter(dict(domain_counts.most_common(15))))

    section("Open vs restricted")
    OPEN = {"CC-BY-4.0","CC-BY-SA-4.0","CC0","MIT","Apache-2.0","CC-BY","CC-BY-SA","open"}
    open_c = sum(1 for r in rows if r["license"] in OPEN)
    restricted_c = sum(1 for r in rows if r["license"] in {"restricted","research"})
    unknown_c = len(rows) - open_c - restricted_c
    print(f"  {'open':<24} {open_c:>4}  {open_c/len(rows)*100:5.1f}%")
    print(f"  {'restricted / research':<24} {restricted_c:>4}  {restricted_c/len(rows)*100:5.1f}%")
    print(f"  {'unknown / other':<24} {unknown_c:>4}  {unknown_c/len(rows)*100:5.1f}%")

    section("Coverage gaps (missing domains)")
    present = set()
    for r in rows:
        for tag in r.get("domain","").split("·"):
            present.add(tag.strip())
    ALL_DOMAINS = {"speech","medical","government","translation","academic","legal",
                   "news","social media","books","blogs","instruction","school","mixed"}
    missing = ALL_DOMAINS - present
    if missing:
        print(f"  Domains with no artifacts: {', '.join(sorted(missing))}")
    else:
        print("  All expected domains covered.")
    print()

if __name__ == "__main__":
    main()

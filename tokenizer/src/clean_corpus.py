#!/usr/bin/env python3
"""
=== clean_corpus.py ===
Step 2: Clean and deduplicate the Azerbaijani corpus.
Input:  data/*.txt files
Output: corpus_clean.txt
"""

import os
import glob

input_dir   = "data"
output_file = "corpus_clean.txt"

seen = set()
total_lines = 0
kept_lines  = 0

with open(output_file, "w", encoding="utf-8") as out:
    for filepath in sorted(glob.glob(os.path.join(input_dir, "*.txt"))):
        print(f"Processing: {filepath}")
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                total_lines += 1
                line = line.strip()

                # Skip empty and very short lines
                if len(line) < 10:
                    continue

                # Skip exact duplicates
                if line in seen:
                    continue

                seen.add(line)
                out.write(line + "\n")
                kept_lines += 1

size_mb = os.path.getsize(output_file) / 1024 / 1024
print(f"\nTotal lines read:  {total_lines:,}")
print(f"Lines kept:        {kept_lines:,}")
print(f"Output:            {output_file} ({size_mb:.0f} MB)")

# Size check
if size_mb < 100:
    print(f"\n✗ WARNING: Output is only {size_mb:.0f} MB — expected 500+ MB.")
    print("  Check that your data/ folder contains the corpus .txt files.")
elif size_mb < 500:
    print(f"\n⚠ Output is {size_mb:.0f} MB — smaller than expected (1000+ MB).")
    print("  Training may produce fewer tokens. Consider adding more data.")
else:
    print(f"\n✓ Corpus size looks good ({size_mb:.0f} MB). Proceed to Step 3.")

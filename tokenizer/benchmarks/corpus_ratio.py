#!/usr/bin/env python3
"""
=== corpus_ratio.py ===
Step 8b: Measure fertility on the ENTIRE corpus (not just test phrases).
         This is the definitive measurement.
Run inside screen:  python corpus_ratio.py | tee corpus_results.txt
"""

from transformers import AutoTokenizer
import time

old_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
new_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_azerbaijani")

total_old = total_new = total_words = lines = 0

print("Measuring on full corpus_clean.txt...")
print("(30–60 min on 1.5 GB — progress every 100K lines)\n")
start = time.time()

with open("corpus_clean.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        words = line.split()
        total_words += len(words)
        total_old   += len(old_tok.tokenize(line))
        total_new   += len(new_tok.tokenize(line))
        lines += 1
        if lines >= 300000:
            break
        if lines % 100000 == 0:
            print(f"  {lines:>10,} lines | "
                  f"old={total_old/total_words:.3f}  "
                  f"new={total_new/total_words:.3f} | "
                  f"{time.time()-start:.0f}s")

old_r = total_old / total_words
new_r = total_new / total_words
delta = ((old_r - new_r) / old_r) * 100

print(f"\n{'='*55}")
print(f"Lines:            {lines:,}")
print(f"Words:            {total_words:,}")
print(f"Old fertility:    {old_r:.3f}")
print(f"New fertility:    {new_r:.3f}")
print(f"Improvement:      {delta:.1f}%")
print(f"Tokens saved:     {total_old - total_new:,}")
print(f"Time:             {(time.time()-start)/60:.1f} min")
print(f"{'='*55}")

# ─── CORPUS-LEVEL CHECKS ─────────────────────────────
print("\n── Corpus acceptance checks ──")

if delta >= 30:
    print(f"✓ Corpus improvement: {delta:.1f}% (target: ≥ 30%)")
else:
    print(f"✗ FAIL: Corpus improvement only {delta:.1f}% — need ≥ 30%.")
    print("  → ESCALATE: vocab extension did not help enough on real data.")

if new_r <= 3.0:
    print(f"✓ Corpus fertility: {new_r:.3f} (target: ≤ 3.0)")
elif new_r <= 3.5:
    print(f"⚠ Corpus fertility: {new_r:.3f} — close but above 3.0")
else:
    print(f"✗ FAIL: Corpus fertility {new_r:.3f} — still above 3.5!")
    print("  → ESCALATE.")

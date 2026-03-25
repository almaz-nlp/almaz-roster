#!/usr/bin/env python3
"""
=== filter_tokens.py ===
Step 6: Filter SentencePiece vocab — keep only tokens missing from Qwen
        that actually save tokens.
Input:  az_unigram.model, qwen3_tokenizer_original/
Output: new_tokens.tsv
"""

import sentencepiece as spm
from transformers import AutoTokenizer

print("Loading tokenizers...")
sp = spm.SentencePieceProcessor()
sp.load("az_unigram.model")

qwen_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
qwen_vocab = set(qwen_tok.get_vocab().keys())

print(f"SentencePiece vocab: {sp.get_piece_size():,}")
print(f"Qwen vocab:          {len(qwen_vocab):,}")
print()

new_tokens = []
skip_exists     = 0
skip_short      = 0
skip_no_savings = 0

for i in range(sp.get_piece_size()):
    piece = sp.id_to_piece(i)
    score = sp.get_score(i)

    # Skip special tokens
    if piece.startswith("<") and piece.endswith(">"):
        continue

    # Clean the piece (remove ▁ marker)
    clean = piece.replace("▁", "")
    if not clean:
        continue

    # Rule 1: not already in Qwen
    if piece in qwen_vocab or clean in qwen_vocab:
        skip_exists += 1
        continue

    # Rule 2: longer than 1 character
    if len(clean) <= 1:
        skip_short += 1
        continue

    # Rule 3: must save at least 1 Qwen token
    qwen_tokens = qwen_tok.tokenize(clean)
    savings = len(qwen_tokens) - 1
    if savings <= 0:
        skip_no_savings += 1
        continue

    # Passed all filters
    new_tokens.append({
        "piece": piece,
        "clean": clean,
        "score": score,
        "savings": savings,
        "qwen_tokens": qwen_tokens,
    })

# Sort by savings (most valuable first), then by score
new_tokens.sort(key=lambda x: (-x["savings"], x["score"]))

print(f"Skipped (already in Qwen):  {skip_exists:,}")
print(f"Skipped (too short):        {skip_short:,}")
print(f"Skipped (no savings):       {skip_no_savings:,}")
print(f"✓ NEW tokens with savings:  {len(new_tokens):,}")

# Show top 40
print(f"\n── Top 40 most valuable new tokens ──")
print(f"{'Token':25s} {'Saves':>5s}  {'Qwen currently produces':40s}")
print("-" * 75)
for t in new_tokens[:40]:
    print(f"{t['clean']:25s} {t['savings']:>4d}   {str(t['qwen_tokens']):40s}")

# Count ə-containing tokens
ə_count = sum(1 for t in new_tokens if "ə" in t["clean"])
print(f"\nTokens containing ə: {ə_count:,} / {len(new_tokens):,}")

# Save to TSV
out_file = "new_tokens.tsv"
with open(out_file, "w", encoding="utf-8") as f:
    f.write("token\tscore\tsavings\tqwen_tokens\n")
    for t in new_tokens:
        f.write(f"{t['clean']}\t{t['score']}\t{t['savings']}\t{' '.join(t['qwen_tokens'])}\n")

print(f"Saved {len(new_tokens):,} tokens → {out_file}")

# ─── AUTOMATED CHECKS ────────────────────────────────
print("\n── Automated checks ──")
count = len(new_tokens)
passed = 0
total_checks = 3

# Check 1: token count in range
if count < 5000:
    print(f"✗ FAIL: Only {count:,} tokens — expected at least 5,000.")
    print("  → Corpus may be too small or not Azerbaijani.")
    print("  → ESCALATE if this persists.")
elif count > 25000:
    print(f"✗ FAIL: {count:,} tokens — expected at most 25,000.")
    print("  → Filtering too loose. Change 'savings <= 0' to 'savings <= 1'.")
    print("  → ESCALATE if this persists.")
else:
    print(f"✓ Token count: {count:,} (expected 5,000–25,000)")
    passed += 1

# Check 2: ə tokens exist
if ə_count == 0:
    print("✗ FAIL: Zero ə-containing tokens found!")
    print("  → Corpus may not be UTF-8, or not Azerbaijani.")
    print("  → ESCALATE immediately.")
elif ə_count < count * 0.15:
    print(f"⚠ WARNING: Only {ə_count:,} ə-tokens ({ə_count*100//count}%).")
    print("  → Expected at least 15–20% to contain ə.")
    passed += 1  # warning, not failure
else:
    print(f"✓ ə-tokens: {ə_count:,} ({ə_count*100//count}% of total)")
    passed += 1

# Check 3: top tokens have good savings
top_savings = [t["savings"] for t in new_tokens[:10]]
if top_savings and max(top_savings) < 2:
    print("✗ FAIL: Top tokens only save 1 Qwen token each.")
    print("  → Check that corpus is actually Azerbaijani text.")
else:
    avg_top = sum(top_savings) / len(top_savings) if top_savings else 0
    print(f"✓ Top-10 tokens save avg {avg_top:.1f} Qwen tokens each")
    passed += 1

print(f"\nChecks passed: {passed}/{total_checks}")
if passed == total_checks:
    print("✓ ALL CHECKS PASSED — safe to proceed to Step 7.")
else:
    print("✗ SOME CHECKS FAILED — read messages above before proceeding.")

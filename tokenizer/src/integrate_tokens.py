#!/usr/bin/env python3
"""
=== integrate_tokens.py ===
Step 7: Add filtered tokens to Qwen tokenizer via add_tokens().
Input:  new_tokens.tsv, qwen3_tokenizer_original/
Output: qwen3_tokenizer_azerbaijani/
"""

from transformers import AutoTokenizer

# Load from backup — always start from clean original
tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
original_size = len(tok)
print(f"Original vocabulary: {original_size:,}")

# Read new tokens from TSV (skip header)
new_tokens = []
with open("new_tokens.tsv", "r", encoding="utf-8") as f:
    header = f.readline()
    for line in f:
        parts = line.strip().split("\t")
        if len(parts) >= 1 and parts[0]:
            new_tokens.append(parts[0])

print(f"Tokens to add:      {len(new_tokens):,}")

# Add them
num_added = tok.add_tokens(new_tokens)
print(f"Actually added:     {num_added:,}")
print(f"New vocab size:     {len(tok):,}")

# Save the extended tokenizer
output_dir = "./qwen3_tokenizer_azerbaijani"
tok.save_pretrained(output_dir)
print(f"Saved to {output_dir}/")

# Verify it loads back
print("\n── Verification ──")
tok2 = AutoTokenizer.from_pretrained(output_dir)
print(f"Reloaded vocab: {len(tok2):,}")

if len(tok2) == original_size + num_added:
    print("✓ Sizes match. Tokenizer is valid.")
else:
    print("✗ WARNING: size mismatch! Something went wrong.")

# Range check
print("\n── Range check ──")
if num_added < 5000:
    print(f"✗ FAIL: Only {num_added:,} tokens added — expected ≥ 5,000.")
    print("  → Go back to Step 5/6 and check corpus quality.")
    print("  → ESCALATE if issue persists.")
elif num_added > 25000:
    print(f"✗ FAIL: {num_added:,} tokens added — expected ≤ 25,000.")
    print("  → Go back to Step 6 and tighten the savings filter.")
    print("  → ESCALATE if issue persists.")
elif 8000 <= num_added <= 15000:
    print(f"✓ {num_added:,} tokens added — ideal range (8,000–15,000)")
else:
    print(f"⚠ {num_added:,} tokens added — acceptable but outside ideal 8K–15K")

print("\nDone. Proceed to Step 8 (final_check.py).")

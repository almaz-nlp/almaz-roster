#!/usr/bin/env python3
"""
=== download_tokenizer.py ===
Step 3: Download the Qwen3 tokenizer (~5 MB, not the full model).
Output: qwen3_tokenizer_original/
"""

from transformers import AutoTokenizer

model_name = "Qwen/Qwen3-32B"

print(f"Downloading tokenizer from {model_name}...")
tok = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

# Save a backup — NEVER modify this folder
tok.save_pretrained("./qwen3_tokenizer_original")

print(f"Vocabulary size: {len(tok):,}")
print("Saved to ./qwen3_tokenizer_original/")

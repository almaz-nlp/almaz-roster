#!/usr/bin/env python3
"""
=== train_unigram.py ===
Step 5: Train SentencePiece Unigram on Azerbaijani corpus.
Input:  corpus_clean.txt
Output: az_unigram.model, az_unigram.vocab
Run inside screen:  screen -S tokenizer
                    python train_unigram.py
"""

import sentencepiece as spm
import os
import time

# ─── Configuration ─────────────────────────────────────
CORPUS_FILE        = "corpus_clean.txt"
MODEL_PREFIX       = "az_unigram"
VOCAB_SIZE         = 50000    # Large pool — filters down in Step 6.
                              # 30K was too small: after filtering out
                              # tokens already in Qwen, only 5-8K survived.
                              # 50K gives enough headroom for 8-15K new tokens.
INPUT_SENTENCE_SIZE = 5000000  # Reduce to 2000000 if RAM issues
# ──────────────────────────────────────────────────────

# Verify corpus exists
if not os.path.exists(CORPUS_FILE):
    print(f"ERROR: {CORPUS_FILE} not found!")
    print("Make sure you ran clean_corpus.py first (Step 2).")
    exit(1)

size_mb = os.path.getsize(CORPUS_FILE) / 1024 / 1024
print(f"Corpus:              {CORPUS_FILE} ({size_mb:.0f} MB)")
print(f"Vocab size:          {VOCAB_SIZE:,}")
print(f"Input sentence size: {INPUT_SENTENCE_SIZE:,}")
print()
print("Training SentencePiece Unigram... (expect 10–30 minutes on CPU)")

start = time.time()

spm.SentencePieceTrainer.train(
    input=CORPUS_FILE,
    model_prefix=MODEL_PREFIX,
    vocab_size=VOCAB_SIZE,
    model_type="unigram",
    character_coverage=1.0,          # Cover ALL characters including ə
    byte_fallback=True,              # Fallback to bytes for OOV
    split_digits=True,               # Digits separate
    max_sentence_length=16384,       # Don't truncate long sentences
    input_sentence_size=INPUT_SENTENCE_SIZE,
    shuffle_input_sentence=True,
    seed_sentencepiece_size=1000000,
    num_threads=os.cpu_count(),
)

elapsed = time.time() - start
print(f"\nDone in {elapsed:.0f}s ({elapsed/60:.1f} min)")
print(f"Output files:")
print(f"  {MODEL_PREFIX}.model — trained tokenizer model")
print(f"  {MODEL_PREFIX}.vocab — vocabulary (for inspection)")

# Sanity check
print("\n── Sanity check ──")
sp = spm.SentencePieceProcessor()
sp.load(f"{MODEL_PREFIX}.model")
print(f"Vocabulary size: {sp.get_piece_size():,}")

for text in ["Azərbaycan Respublikasının Konstitusiyası",
             "müstəqilliyin bərpası haqqında",
             "dövlət büdcəsinin icrası",
             "kitablarımızdakılardan",
             "müasirləşdirilməsindən",
             "gələcəkdir"]:
    pieces = sp.encode(text, out_type=str)
    print(f"  {text}")
    print(f"    → {pieces}")
    print()

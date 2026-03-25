import torch
from transformers import AutoTokenizer
import time
import random
import os

def run_sample_check():
    # Use the 36k version for the final powerhouse check
    old_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
    new_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_azerbaijani")
    
    sample_size = 300000
    batch_size = 256
    
    print(f"Loading random {sample_size} lines from corpus...")
    # Get total lines roughly
    lines_pool = []
    with open("corpus_clean.txt", "r", encoding="utf-8") as f:
        # We can't load all 8M into memory safely if they are long
        # But we can reservoir sample or just pick the first 1M and shuffle
        counter = 0
        for line in f:
            lines_pool.append(line.strip())
            counter += 1
            if counter >= 1000000: break # Sample from the first 1M lines
            
    test_lines = random.sample(lines_pool, min(len(lines_pool), sample_size))
    del lines_pool
    
    total_old = total_new = total_words = 0
    start = time.time()
    
    print(f"Processing {len(test_lines)} lines in batches of {batch_size}...")
    
    for i in range(0, len(test_lines), batch_size):
        batch = test_lines[i : i + batch_size]
        batch = [l for l in batch if l]
        if not batch: continue
        
        # Count words
        for line in batch:
            total_words += len(line.split())
            
        # Count tokens (Batching is much faster)
        # We use 'is_fast=False' if needed, but default should work
        old_batch = old_tok(batch, add_special_tokens=False)["input_ids"]
        new_batch = new_tok(batch, add_special_tokens=False)["input_ids"]
        
        for ids in old_batch: total_old += len(ids)
        for ids in new_batch: total_new += len(ids)
        
        if (i // batch_size) % 100 == 0:
            elapsed = time.time() - start
            print(f"  Processed {i:,} lines... Current New Fertility: {total_new/total_words:.3f}")

    old_r = total_old / total_words
    new_r = total_new / total_words
    delta = ((old_r - new_r) / old_r) * 100
    
    print(f"\n--- FINAL 300K RANDOM SAMPLE RESULTS ---")
    print(f"Total Words:     {total_words:,}")
    print(f"Original Qwen:   {old_r:.3f} tokens/word")
    print(f"Azerbaijani Tok: {new_r:.3f} tokens/word")
    print(f"Improvement:     {delta:.1f}%")
    print(f"Time Taken:      {time.time()-start:.1f}s")
    print(f"------------------------------------------")

if __name__ == '__main__':
    run_sample_check()

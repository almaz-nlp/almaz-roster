from transformers import AutoTokenizer
import time
import random
import os

def run_deep_all():
    # Load all variants
    models = {
        "Original Qwen": "./qwen3_tokenizer_original",
        "14k Version": "./qwen3_tokenizer_az_14k",
        "20k Version": "./qwen3_tokenizer_az_20k",
        "36k Version": "./qwen3_tokenizer_azerbaijani"
    }
    
    tokenizers = {name: AutoTokenizer.from_pretrained(path) for name, path in models.items()}
    
    sample_size = 300000
    batch_size = 512
    
    print(f"Loading random {sample_size} lines...")
    with open("corpus_clean.txt", "r", encoding="utf-8") as f:
        # Use reservoir sampling to be efficient with memory
        test_lines = []
        for i, line in enumerate(f):
            if i < sample_size:
                test_lines.append(line.strip())
            else:
                r = random.randint(0, i)
                if r < sample_size:
                    test_lines[r] = line.strip()
            if i % 1000000 == 0: print(f"  Scanned {i:,} lines...")

    results = {name: 0 for name in models}
    total_words = 0
    start = time.time()
    
    print(f"Processing {len(test_lines)} lines in batches of {batch_size}...")
    for i in range(0, len(test_lines), batch_size):
        batch = [l for l in test_lines[i : i + batch_size] if l]
        if not batch: continue
        
        for line in batch:
            total_words += len(line.split())
            
        for name, tok in tokenizers.items():
            encoded = tok(batch, add_special_tokens=False)["input_ids"]
            for ids in encoded:
                results[name] += len(ids)
        
        if (i // batch_size) % 50 == 0:
            print(f"  Progress: {i:,} lines processed...")

    with open("deep_validation_report.txt", "w") as out:
        out.write("==== DEEP STATISTICAL VALIDATION (300,000 Random Sentences) ====\\n")
        out.write(f"Total Lines: {len(test_lines):,}\\n")
        out.write(f"Total Words: {total_words:,}\\n\\n")
        out.write(f"{'Version':<20} | {'Fertility':<10} | {'Improvement':<12}\\n")
        out.write("-" * 50 + "\\n")
        
        orig_r = results["Original Qwen"] / total_words
        for name, total_tokens in results.items():
            r = total_tokens / total_words
            imp = ((orig_r - r) / orig_r) * 100 if name != "Original Qwen" else 0
            out.write(f"{name:<20} | {r:<10.3f} | {imp:<11.1f}%\\n")
        
        out.write(f"\\nTime Taken: {(time.time()-start):.1f}s\\n")
    
    print("\\nValidation Report generated in deep_validation_report.txt")

if __name__ == '__main__':
    run_deep_all()

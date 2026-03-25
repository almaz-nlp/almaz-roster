from transformers import AutoTokenizer

old_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
new_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_azerbaijani")

total_old = total_new = total_words = lines = 0

with open("sample_test.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line: continue
        words = line.split()
        total_words += len(words)
        total_old   += len(old_tok.tokenize(line))
        total_new   += len(new_tok.tokenize(line))
        lines += 1

old_r = total_old / total_words
new_r = total_new / total_words
delta = ((old_r - new_r) / old_r) * 100

with open("micro_eval_results.txt", "w") as out:
    out.write(f"\\n--- FAST SAMPLE RESULTS ({lines} sentences) ---\\n")
    out.write(f"Lines Evaluated: {lines:,}\\n")
    out.write(f"Total Words:     {total_words:,}\\n")
    out.write(f"Original Qwen:   {old_r:.3f} tokens/word\\n")
    out.write(f"Azerbaijani Tok: {new_r:.3f} tokens/word\\n")
    out.write(f"Improvement:     {delta:.1f}%\\n")
    out.write("------------------------------------------\\n")

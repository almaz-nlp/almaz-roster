# Qwen3-Azerbaijani-Tokenizer

An optimized, highly mathematically compressed Azerbaijani Tokenizer extension for the **Qwen3 (Qwen2.5)** architecture. 

## 📌 Problem Statement
Native BPE-based tokenizers (like Qwen's) notoriously break when encountering the standard Azerbaijani `"ə"` character. Highly agglutinative words shatter into useless, tiny fragments (e.g., `müasirləşdirilməsindən` breaks into **12 fragments**!). This wastes token context, dramatically slows down inference speed, and severely bloats Embedding VRAM.

## 🚀 The Solution
This project uses **SentencePiece Unigram** to algorithmically extract pure linguistic roots from a massive DOLLMA corpus, filtering the absolute best custom tokens and surgically injecting them into the Qwen3 structural dictionary. 

The resulting tokenizers drop the tokenizer "fertility ratio" from **5.0 tokens/word** natively down to computationally brilliant **2.20 tokens/word**. 

---

## 📂 Repository Structure
- `/src/` - The core Tokenizer Generation pipeline scripts.
- `/outputs/` - The compiled, ready-to-use Tokenizer Configurations (`14k`, `20k`, and `36k` versions).
- `/benchmarks/` - The statistical testing scripts used to prove the fertility compression.
- `/docs/` - Comprehensive technical breakdown mapping the exact mathematical pros/cons of the different token variants.
- `/utils/` - Assorted helper scripts for headless SSH orchestration and data transfer.

---

## 🛠️ Step-by-Step Implementation Guide
To rebuild this project from scratch or modify the token pools, follow this pipeline natively in Python.

### Prerequisites
```bash
pip install sentencepiece transformers tokenizers
```

### Phase 1: Data Preparation
We utilized the massive 8.9-million line **DOLLMA Dataset** to guarantee linguistic accuracy.
1. Concatenate all your raw text data.
2. Run `src/clean_corpus.py` to aggressively deduplicate your dataset and strip empty spaces, ensuring the highest density text ratio.

### Phase 2: Unigram Modeling
Instead of BPE, we use Unigram generation. Unigram works top-down from vast strings to extract actual grammatical root components.
- Run `src/train_unigram.py`
*(Note: We trained a 50,000 parameter vocabulary on a 5-million sentence subset of the corpus).*

### Phase 3: Mathematical Filtering
The Unigram trainer will generate noisy candidate tokens. We must filter them strictly against Qwen's base matrix.
- Run `src/filter_tokens.py`
This script drops tokens that:
  - Are shorter than 3 characters.
  - Already exist precisely in Qwen's native dictionary.
  - Fail to save at least 1 character of space when tokenized.
*(You can adjust the sorting boundary in this file. We generated `14k`, `20k`, and `36k` variants).*

### Phase 4: Qwen Injection
We seamlessly wrap the isolated custom roots and inject them into the Hugging Face dictionary format.
- Run `src/integrate_tokens.py`
This will automatically generate a new `./qwen3_tokenizer_azerbaijani/` folder containing your `tokenizer.json` and config maps securely appended to Qwen.

### Phase 5: Verification
Proof of concept is empirically required for LLM training parameters to guarantee standard loss.
- Run `src/final_check.py` to analyze the fragmentation boundaries of the 20 most violently complex Azerbaijani words.
- *For Deep statistical profiling across massive datasets, run `/benchmarks/deep_validate_all.py`.*

---

## 📈 Performance Results
Based on a massive 12-million word randomized corpus string sample, extracting **20,000 custom tokens** represents the absolute "Goldilocks Zone" of stability vs. compression:

| Model | Average Fertility | Context Space Improvement |
| :------- | :--------: | :-------: |
| Original Qwen3 | 3.56 | - |
| **Qwen3 (20k Roots)** | **2.52** | **+29.0%** |

*Read the full internal benchmark evaluations inside the `/docs/` folder for deeper empirical parameters.*

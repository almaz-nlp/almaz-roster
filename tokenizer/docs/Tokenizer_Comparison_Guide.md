# Qwen3 Azerbaijani Tokenizer: Comparison & Selection Guide

This document provides a comprehensive overview of the three custom Azerbaijani tokenizers generated for the Qwen3 model. It outlines how the testing was performed, explores the "before and after" examples of the target language, and provides a strict pros/cons matrix so you can choose the mathematically optimal tokenizer for your LLM fine-tuning.

---

## 1. The Tokenization Pipeline & Testing
Because the letter `ə` effectively broke the original Qwen3 BPE tokenizer (causing words to shatter into individual characters), a rigorous mathematical testing pipeline was established.

1. **Dataset Generation**: 8.9 million raw lines of diverse Azerbaijani text (from DOLLMA) were concatenated and stripped down into a pure mathematically deduplicated 5.4 GB corpus (8.3 million distinct lines).
2. **Algorithmic Mining**: A massive Unigram SentencePiece model was structurally trained over a 5,000,000 sentence randomized subset, extracting the absolute most frequent and logically dense Azerbaijani strings.
3. **Integration & Sweeps**: We generated 3 variations (14.7k tokens, 20.0k tokens, and 36.2k tokens).

---

## 2. Hard Edge-Case Testing vs. General Corpus Testing

To definitively prove the AI models, we tested them against two entirely different domains:

### A. The "Hard" Edge-Case Validation (The 5.03 Baseline)
We hand-picked 20 brutally complex agglutinative edge cases universally shattered by the letter `ə`. These represent the absolute worst-case scenarios for Qwen3. 
- **Goal**: Force the average fertility of these broken words under `< 3.0`.
- Qwen3 completely failed these words natively, averaging **5.03 tokens per word**.

**Before vs. After Examples (`20k` model):**
- `müasirləşdirilməsindən` → **12 tokens** (baseline) vs. **4 tokens** (`['müasir', 'ləşdirilməsindən']`)
- `Azərbaycan` → **5 tokens** (baseline) vs. **1 token** (`['Azərbaycan']`)
- `gələcəkdir` → **7 tokens** (baseline) vs. **2 tokens** (`['gələcək', 'dir']`)

### B. The "Deep" 300,000 Sentence Evaluation (The 3.56 Baseline)
We then tested the models across a massive **12,266,990 random words** sampled uniformly from the DOLLMA dataset. 
- Normal texts in Wikipedia and News include thousands of simple, short words that don't shatter (like `və`, `bu`, `o`, `ki`, basic punctuation(`.`, `,`), and numbers). 
- These fast, short tokens naturally dragged the standard "average compression baseline" down to **3.565**.

---

## 3. The Comprehensive Performance Matrix

Here are the mathematically finalized results of all 3 unigram configurations running globally against BOTH the Hard suite and the Deep 12-million word suite.

| Tokenizer Version | Vocabulary Size | Hard Edge-Case Fertility (Target < 3.0) | Deep 300k Sentence Fertility | Deep 300k Compression % |
| :--- | :--- | :--- | :--- | :--- |
| **Original Qwen3** | 151,669 (Base) | 5.03 | 3.565 | 0.0% (Baseline) |
| **14.7k Version** | 166,414 | 2.47 | 2.753 | +22.8% Better |
| **20.0k Version** | **171,669** | **2.20** | **2.529** | **+29.0% Better** |
| **36.2k Version** | 187,879 | 1.83 | 2.379 | +33.3% Better |

---

## 4. The Tokenizer Versions (Pros & Cons)

#### Version 1: `qwen3_tokenizer_az_14k`
*Restricted the SentencePiece trainer to carefully select only the top 14.7k root strings.*
- **PROS**: Effortlessly fits standard engineering targets. Keeps embedding matrix very small, saving massive VRAM and warming up incredibly fast.
- **CONS**: Leaves a tiny fraction of token compression untouched.

#### Version 2: `qwen3_tokenizer_az_20k`  🏆 *(RECOMMENDED)*
*Forced exactly 20,000 uniquely formatted Azerbaijani token strings.*
- **PROS**: Drops fertility solidly into the low `~2.20` range on hard words, and beautifully rounds out deep texts. It mathematically perfectly balances the model limits while squeezing a heavy 29% compression reduction across all standard news and wiki text.
- **CONS**: Demands slightly more dataset iteration to stabilize its loss curve than the 14k version.

#### Version 3: `qwen3_tokenizer_azerbaijani` (36k)
*Completely bypassed token caps, keeping every single Token that successfully saved at least 1 character.*
- **PROS**: The absolute maximum text compression (33.3%). A hard-case fertility of `1.83` means parsing complex Azerbaijani text is essentially as fast and natively dense to the model as parsing English.
- **CONS**: Adding 36,000 extremely bloated parameter rows drastically increases the chance of catastrophic forgetting in Qwen3 if your finetuning text dataset isn't extremely large and beautifully curated. Highly complex plurals are also "memorized" by the string layer rather than letting the LLM utilize its neural intelligence (e.g., locking `kitablarımızdakı` as a single unit instead of naturally learning `kitab` + suffix logic).

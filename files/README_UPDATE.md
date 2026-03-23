# ALMAZ Registry Update v0.2.1

## New Datasets Added from omar07ibrahim

This update adds **6 new datasets** from the Hugging Face contributor [omar07ibrahim](https://huggingface.co/omar07ibrahim), bringing the total artifact count from **36 to 42**.

---

## New Entries (CSV rows to append)

```csv
AZ-DATA-011,660K-AZ-EN-Parallel,dataset,2,HuggingFace / omar07ibrahim,666K pairs,translation,unknown,https://huggingface.co/datasets/omar07ibrahim/660K_AZERBAIJAN-ENGLISH_PARALLEL,P2,Largest public Az-En parallel corpus; includes reliability scores and source tracking
AZ-DATA-012,Orca-AZ,dataset,2,HuggingFace / omar07ibrahim,500K samples,instruction,unknown,https://huggingface.co/datasets/omar07ibrahim/orca_firstpart_AZ,P2,Azerbaijani translation of Microsoft Orca instruction dataset
AZ-DATA-013,AzCon,dataset,2,HuggingFace / omar07ibrahim,237K samples,conversational,unknown,https://huggingface.co/datasets/omar07ibrahim/azcon,P2,Azerbaijani conversational QA dataset
AZ-DATA-014,UltraFeedback-AZ,dataset,2,HuggingFace / omar07ibrahim,61K pairs,preference,unknown,https://huggingface.co/datasets/omar07ibrahim/ultrafeedback_binarized-BIZIM,P2,First Azerbaijani preference dataset for RLHF/DPO alignment
AZ-DATA-015,Alpaca-AZ-Cleaned,dataset,2,HuggingFace / omar07ibrahim,52K samples,instruction,unknown,https://huggingface.co/datasets/omar07ibrahim/alpaca-cleaned_AZERBAIJANI,P2,Azerbaijani translation of Stanford Alpaca cleaned dataset
AZ-DATA-016,AZ-EN-Dataset,dataset,2,HuggingFace / omar07ibrahim,549K pairs,translation,unknown,https://huggingface.co/datasets/omar07ibrahim/AZERBAIJAN-ENGLISH-DATASET,P2,Az-En parallel translation dataset
```

---

## Dataset Details

### 1. 660K-AZ-EN-Parallel ⭐ (AZ-DATA-011)
- **Size:** 666,000 sentence pairs
- **URL:** https://huggingface.co/datasets/omar07ibrahim/660K_AZERBAIJAN-ENGLISH_PARALLEL
- **Format:** CSV with columns: sentence, id, source, reliability, sentence_en
- **Sources:** az_wiki + others
- **Features:** 
  - UUID tracking for deduplication
  - Reliability scores (3-5)
  - Source attribution
- **Significance:** Largest publicly available Azerbaijani-English parallel corpus

### 2. Orca-AZ (AZ-DATA-012)
- **Size:** 500,000 instruction-response pairs
- **URL:** https://huggingface.co/datasets/omar07ibrahim/orca_firstpart_AZ
- **Format:** JSON with question/response columns
- **Significance:** Large-scale Azerbaijani instruction dataset for LLM fine-tuning

### 3. AzCon (AZ-DATA-013)
- **Size:** 237,000 conversational QA pairs
- **URL:** https://huggingface.co/datasets/omar07ibrahim/azcon
- **Format:** JSON with question/answer columns
- **Significance:** Azerbaijani conversational/assistant-style QA dataset

### 4. UltraFeedback-AZ ⭐ (AZ-DATA-014)
- **Size:** 61,100 preference pairs
- **URL:** https://huggingface.co/datasets/omar07ibrahim/ultrafeedback_binarized-BIZIM
- **Format:** Binarized preference format
- **Significance:** **First public Azerbaijani preference dataset** for RLHF/DPO training

### 5. Alpaca-AZ-Cleaned (AZ-DATA-015)
- **Size:** 51,800 instruction pairs
- **URL:** https://huggingface.co/datasets/omar07ibrahim/alpaca-cleaned_AZERBAIJANI
- **Significance:** Azerbaijani translation of the popular Stanford Alpaca dataset

### 6. AZ-EN-Dataset (AZ-DATA-016)
- **Size:** 549,000 sentence pairs
- **URL:** https://huggingface.co/datasets/omar07ibrahim/AZERBAIJAN-ENGLISH-DATASET
- **Significance:** Additional large-scale parallel corpus

---

## Impact Summary

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Total artifacts | 36 | 42 | +6 |
| Dataset count | 10 | 16 | +6 |
| Translation pairs | ~60K | ~1.8M | +1.7M |
| Instruction samples | 0 | ~550K | +550K |
| Preference pairs | 0 | 61K | +61K |

### New Capabilities Enabled
1. **Machine Translation:** 1.7M+ new parallel sentence pairs
2. **Instruction Tuning:** 550K+ samples for fine-tuning LLMs
3. **RLHF/DPO Alignment:** First preference dataset enables human feedback alignment
4. **Conversational AI:** 237K QA pairs for chatbot training

---

## Contributor Attribution

**omar07ibrahim** (Omar)
- Profile: https://huggingface.co/omar07ibrahim
- Focus: NLP & Low resource languages
- Organizations: Data Is Better Together Contributor, Waifu Research Department
- Also maintains 4 models including NLLB_az fine-tune

---

## Files in This Update

1. `almaz_registry_v021.csv` - Complete updated registry
2. `CHANGELOG.md` - Version history
3. `README_UPDATE.md` - This file

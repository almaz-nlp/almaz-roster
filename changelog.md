# Changelog

All notable changes to the ALMAZ Resource Registry are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versioning follows [Semantic Versioning](https://semver.org/).
Each release is archived on Zenodo — use the DOI of the specific version you cite.

---

## [Unreleased]

---

## [0.2.0] — 2026-03-15

**Zenodo DOI:** `pending — tag v0.2.0 to mint`
**Cited by:** ALMAZ-Corpus (Paper 2)

### Added

- 8 new artifacts closing 3 of 4 coverage gaps identified in v0.1.0
- **Speech (4 artifacts):** Common Voice AZ · FLEURS-AZ · ISSAI Turkic ASR · ISSAI Turkic TTS · Whisper-large-v3 (AZ support)
- **Translation (3 artifacts):** ParaCrawl AZ-EN · OPUS AZ corpora · TIL-MT Azerbaijani
- **Government (1 artifact):** eQanun Legal Corpus (~55K legal documents from e-qanun.az)
- Total artifacts: **44** (up from 36)

### Still missing

- `medical` — no known open Azerbaijani medical text corpus; flagged as priority for v0.3.0

---

## [0.1.0] — 2026-03-14

**Zenodo DOI:** `10.5281/zenodo.19023843`
**Cited by:** ALMAZ-Survey (Paper 1)

### Added

- Initial seed registry with **36 artifacts** across five types
- 9 corpora: DOLLMA, azWaC, azcorpus_v0, AZ Wikipedia, C4-AZ, OSCAR-AZ, AZ Laws corpus, azerbaijani-blogs, Domrachev-Sudoplatova
- 10 datasets: AZ NER, AZ Sentiment (reviews), AZ Sentiment (social+news), AZ Twitter Sentiment, AZE-SCI, AZE-NSP, CB-MCQ, Aze-Instruct-2K, AZ-MRPC, UD Azerbaijani-TueCL
- 4 benchmarks: TUMLU-AZ, TUMLU-mini-AZ, aLLMA NLU Benchmark, BLEnD-AZ
- 10 models: aLLMA-SMALL, aLLMA-BASE, AzQ-1.7B, AtLLaMA, az-mistral, HPLT-BERT-AZ, mBERT-AZ, XLM-R-AZ, AZ Sentiment XLM-R, AzerBERT (Iranian AZ)
- 3 tools: Azmorph, MorAz, awesome-azerbaijani-nlp
- `data/registry.csv` — primary artifact table
- `data/registry.json` — same data in JSON format
- `data/registry.xlsx` — formatted spreadsheet with legend and stats sheets
- `docs/schema.md` — column definitions and type taxonomy
- `docs/contributing.md` — contributor guide
- `docs/changelog.md` — this file
- `scripts/validate.py` — link and schema validation
- `scripts/stats.py` — coverage statistics
- `CITATION.cff` — machine-readable citation metadata
- GitHub Actions: `validate.yml`, `zenodo-release.yml`

---

## Version roadmap

| Version | Target date | Trigger |
|---|---|---|
| v0.2.0 | With Paper 2 (ALMAZ-Corpus) | +speech datasets, translation corpora, CC data |
| v0.3.0 | With Paper 3 (ALMAZ-LM) | +new models, tokenizer resources |
| v0.4.0 | With Paper 4 (ALMAZ-Bench) | +AZ-GLUE components, leaderboard data |
| v0.5.0 | With Paper 5 (ALMAZ-Road) | +domain-specific resources, speech models |
| v1.0.0 | After Paper 5 published | Stable schema, full coverage audit |

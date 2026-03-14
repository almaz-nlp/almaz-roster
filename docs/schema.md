# Registry schema

This document defines every column in `data/registry.csv`.

---

## Column definitions

### `id`

A stable, unique identifier for the artifact. Never changes after assignment — even if the artifact is renamed or moved.

Format: `AZ-{TYPE}-{NUMBER}`

| Prefix | Type |
|---|---|
| `AZ-CORP` | Corpus |
| `AZ-DATA` | Dataset |
| `AZ-BENCH` | Benchmark |
| `AZ-MODEL` | Model |
| `AZ-TOOL` | Tool |

Numbers are zero-padded to three digits: `001`, `002`, etc. New artifacts receive the next available number in their type series.

---

### `name`

The artifact's canonical name as used in its primary publication or repository. Use the name the authors use — do not normalize or translate.

Examples: `DOLLMA`, `azWaC`, `TUMLU-mini-AZ`, `aLLMA-BASE`

---

### `type`

One of five controlled values:

| Value | Meaning |
|---|---|
| `corpus` | A collection of raw or lightly cleaned text used for language model pretraining |
| `dataset` | A labeled collection used for fine-tuning or task-specific evaluation |
| `benchmark` | A standardized evaluation suite with defined metrics and splits |
| `model` | A pretrained or fine-tuned language model |
| `tool` | Software for processing, analyzing, or generating Azerbaijani text |

If an artifact spans multiple types (e.g. a paper that releases both a dataset and a model), create one row per artifact — do not merge.

---

### `layer`

The ecosystem layer the artifact primarily belongs to, as defined by the ALMAZ hero diagram.

| Value | Layer name | Description |
|---|---|---|
| `1` | Raw sources | Unprocessed web, news, institutional text |
| `2` | Datasets & corpora | Cleaned, deduplicated, documented collections |
| `3` | Models | Pretrained encoders, decoders, LLMs |
| `4` | Benchmarks | Evaluation datasets and leaderboards |
| `5` | Applications | Deployed systems and downstream tools |

A benchmark dataset lives at layer 4 even if its raw source text came from layer 2. Assign the layer that reflects the artifact's *primary function*, not its origin.

---

### `source`

Where the artifact is hosted or published. Use the platform name followed by the organization or username.

Examples:
- `HuggingFace / allmalab`
- `GitHub / ceferisbarov`
- `SketchEngine`
- `ACL Anthology`
- `Zenodo`
- `Institutional` (for artifacts held by a university or government body with no public mirror)

---

### `size`

A human-readable size estimate. Use the unit most natural for the artifact type:

| Type | Preferred unit | Example |
|---|---|---|
| corpus | words or tokens | `651M words` |
| dataset | samples or sentences | `160K reviews` |
| benchmark | questions or pairs | `38,139 questions` |
| model | parameters | `1.7B params` |
| tool | — | leave blank |

If the size is unknown, write `unknown`. Do not leave blank.

---

### `domain`

A dot-separated list of domain tags describing the artifact's content. Use lowercase, and choose from the controlled vocabulary below where possible. Add new tags only if none of the existing ones fit.

**Controlled vocabulary:**

`general` · `news` · `legal` · `academic` · `books` · `social media` · `blogs` · `web-general` · `encyclopedic` · `instruction` · `reasoning` · `school` · `translation` · `speech` · `e-commerce` · `government` · `medical` · `mixed`

Example: `news · legal · blogs`

---

### `license`

The artifact's license as declared by its authors. Use SPDX identifiers where possible.

**Common values:**

| Value | Meaning |
|---|---|
| `CC-BY-4.0` | Creative Commons Attribution 4.0 |
| `CC-BY-SA-4.0` | Creative Commons Attribution-ShareAlike 4.0 |
| `CC-BY-NC-4.0` | Creative Commons Attribution-NonCommercial 4.0 |
| `CC-BY-NC-ND-4.0` | No derivatives, non-commercial |
| `CC0` | Public domain dedication |
| `MIT` | MIT License |
| `Apache-2.0` | Apache License 2.0 |
| `research` | Available for research use only; no formal license |
| `restricted` | Access controlled; requires agreement or application |
| `unknown` | License not stated by authors |

If a license is `restricted` or `unknown`, add a note in the `notes` column explaining what is known about access conditions.

---

### `link`

The canonical URL for the artifact. Prefer the primary hosting location over mirrors or aggregators.

Priority order:
1. HuggingFace dataset or model card page
2. GitHub repository
3. Paper page (arXiv, ACL Anthology, ACM DL)
4. Project homepage
5. Institutional page

Links are validated automatically by `scripts/validate.py` on every pull request. Broken links will block merging.

---

### `paper`

Which paper(s) in the ALMAZ series cover this artifact. Use dot-separated codes.

| Code | Paper |
|---|---|
| `P1` | ALMAZ-Survey |
| `P2` | ALMAZ-Corpus |
| `P3` | ALMAZ-LM |
| `P4` | ALMAZ-Bench |
| `P5` | ALMAZ-Road |

Example: `P2·P4` means the artifact appears in both the corpus paper and the benchmark paper.

---

### `notes`

Free text. Use this field for:
- Key caveats (e.g. "significant non-AZ content found on inspection")
- Access instructions for restricted artifacts
- Relationships to other artifacts (e.g. "fine-tuned on AZ-DATA-008")
- Version or date context

Keep notes to one or two sentences. Longer documentation belongs in a separate file in `docs/artifacts/`.

---

## Type taxonomy diagram

```
artifact
├── corpus          raw or cleaned text for pretraining
├── dataset         labeled data for a specific task
│   ├── NER
│   ├── sentiment
│   ├── classification
│   ├── STS / similarity
│   ├── QA
│   ├── translation pairs
│   └── instruction pairs
├── benchmark       standardized eval suite with splits + metrics
├── model
│   ├── encoder     BERT-style masked LM
│   ├── decoder     GPT-style causal LM
│   ├── seq2seq     encoder-decoder (e.g. T5, NLLB)
│   └── fine-tuned  task-specific fine-tune of any base
└── tool
    ├── morphological analyzer
    ├── tokenizer
    ├── POS tagger
    └── resource list / meta
```

---

## ID assignment rules

1. IDs are assigned sequentially within each type prefix.
2. Once assigned, an ID is permanent — even if the artifact is deprecated or removed.
3. Deprecated artifacts remain in the registry with a `deprecated: true` note.
4. If an artifact is superseded by a newer version, both get separate IDs and the older one's notes field points to the newer one.

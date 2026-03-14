# ALMAZ Resource Registry

**Advanced Language Model for AZerbaijan — Resource Registry**

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![Artifacts](https://img.shields.io/badge/artifacts-36-blue.svg)]()
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)]()

The ALMAZ Resource Registry is a curated, versioned catalog of Azerbaijani NLP artifacts. It is the shared reference dataset for the [ALMAZ paper series](#citing-the-almaz-paper-series) and is designed to support reproducible research in low-resource Azerbaijani language technology.

---

## What is ALMAZ?

**ALMAZ** (Advanced Language Model for **AZ**erbaijan) is a five-paper research program mapping the complete Azerbaijani AI ecosystem — from raw text sources to deployed applications. The name doubles as the Azerbaijani word for *diamond* (الماز · алмаз), reflecting the goal of making Azerbaijani NLP a precise and valuable resource for the research community.

---

## Registry contents

The registry currently covers **36 artifacts** across five types:

| Type | Count | Description |
|---|---|---|
| Corpus | 9 | Raw and cleaned text corpora for pretraining |
| Dataset | 10 | Labeled datasets for fine-tuning and evaluation |
| Benchmark | 4 | Standardized evaluation suites |
| Model | 10 | Pretrained and fine-tuned language models |
| Tool | 3 | Software tools, analyzers, and resource lists |

Each artifact is mapped to one of five ecosystem layers:

```
Layer 1 — Raw sources
Layer 2 — Datasets & corpora
Layer 3 — Models
Layer 4 — Benchmarks & evaluation
Layer 5 — Applications & frontier
```

---

## Files

```
almaz-registry/
├── data/
│   ├── registry.csv        ← primary artifact table (human-readable)
│   ├── registry.json       ← same data for programmatic use
│   └── registry.xlsx       ← formatted spreadsheet with legend and stats
├── docs/
│   ├── schema.md           ← column definitions and type taxonomy
│   ├── contributing.md     ← how to add or update an artifact
│   └── changelog.md        ← version history and Zenodo DOIs
├── scripts/
│   ├── validate.py         ← checks for broken links, missing fields, duplicates
│   └── stats.py            ← generates coverage statistics by type and layer
├── .github/workflows/
│   ├── validate.yml        ← runs validate.py on every pull request
│   └── zenodo-release.yml  ← mints a new DOI on every version tag
├── CITATION.cff            ← machine-readable citation metadata
├── LICENSE                 ← CC-BY 4.0
└── README.md               ← this file
```

---

## Registry schema

Each row in `registry.csv` describes one artifact:

| Column | Description | Example |
|---|---|---|
| `id` | Stable identifier | `AZ-CORP-001` |
| `name` | Human-readable name | `DOLLMA` |
| `type` | One of: corpus · dataset · benchmark · model · tool | `corpus` |
| `layer` | Ecosystem layer (1–5) | `2` |
| `source` | Where the artifact lives | `HuggingFace / allmalab` |
| `size` | Tokens, samples, or parameters | `651M words` |
| `domain` | Topic coverage | `general · news · legal` |
| `license` | License identifier | `CC-BY-SA` |
| `link` | Direct URL | `https://...` |
| `paper` | ALMAZ paper(s) that cover it | `P2` |
| `notes` | Key caveats or context | `Primary LLM pretraining corpus` |

Full column definitions are in [`docs/schema.md`](docs/schema.md).

---

## Quick start

```python
import pandas as pd

df = pd.read_csv("data/registry.csv")

# All corpora
corpora = df[df["type"] == "corpus"]

# Layer 4 benchmarks only
benchmarks = df[(df["type"] == "benchmark") & (df["layer"] == 4)]

# Open-licensed artifacts
open_artifacts = df[df["license"].isin(["CC-BY", "CC-BY-SA", "MIT", "Apache-2.0", "CC0"])]

print(df.groupby("type")["id"].count())
```

---

## How to cite

If you use this registry in your research, please cite:

```bibtex
@dataset{almaz_registry_2026,
  title     = {{ALMAZ} Resource Registry: A Curated Catalog of
               Azerbaijani {NLP} Artifacts},
  author    = {},
  year      = {2026},
  version   = {0.1.0},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.XXXXXXX},
  url       = {https://github.com/almaz-nlp/almaz-registry},
  note      = {Shared reference dataset for the ALMAZ paper series}
}
```

---

## Citing the ALMAZ paper series

Each paper in the series cites the registry version that existed at submission time.

| Paper | Short title | Registry version cited |
|---|---|---|
| Paper 1 — ALMAZ-Survey | Mapping the Azerbaijani AI ecosystem | v0.1.0 |
| Paper 2 — ALMAZ-Corpus | The Azerbaijani text data landscape for LLMs | v0.2.0 |
| Paper 3 — ALMAZ-LM | Large language models for Azerbaijani | v0.3.0 |
| Paper 4 — ALMAZ-Bench | Evaluating Azerbaijani language models | v0.4.0 |
| Paper 5 — ALMAZ-Road | Building the future of Azerbaijani AI | v0.5.0 |

---

## Contributing

We welcome additions and corrections. Before opening a pull request:

1. Read [`docs/contributing.md`](docs/contributing.md)
2. Add your artifact(s) to `data/registry.csv` following the schema
3. Run `python scripts/validate.py` to check for errors
4. Open a PR — the CI workflow will run validation automatically

Every merged PR that adds new artifacts triggers a minor version bump.

---

## Versioning and DOIs

Each release is archived on [Zenodo](https://zenodo.org) with a permanent DOI.

| Version | DOI | Notes |
|---|---|---|
| v0.1.0 | 10.5281/zenodo.XXXXXXX | Seed data — 36 artifacts |

Use the DOI of the specific version you used, not the concept DOI, to ensure reproducibility.

---

## License

The registry metadata is released under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/). Individual artifacts have their own licenses — see the `license` column in the registry.

---

## Acknowledgements

This registry builds on prior community work, in particular the [awesome-azerbaijani-nlp](https://github.com/alexeyev/awesome-azerbaijani-nlp) list by Alex Alekseyev, the [aLLMA Lab](https://huggingface.co/allmalab) DOLLMA corpus and benchmark suite, and the [TUMLU](https://github.com/ceferisbarov/TUMLU) benchmark by Jafar Isbarov and collaborators.

---

*الماز · алмаз · almaz — diamond of Azerbaijani NLP*

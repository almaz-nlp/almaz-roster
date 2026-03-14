# Contributing to the ALMAZ Resource Registry

Thank you for helping build the most comprehensive catalog of Azerbaijani NLP artifacts. This guide explains how to add new artifacts, correct existing entries, and participate in the review process.

---

## Before you start

- Read [`docs/schema.md`](schema.md) — every column has a controlled vocabulary and format rules.
- Search the existing registry before adding: `grep -i "your artifact name" data/registry.csv`
- Check that the artifact is genuinely related to Azerbaijani language technology (either North Azerbaijani ISO 639-1: `az`, or South Azerbaijani ISO 639-3: `azb`).

---

## What belongs in the registry

**Include:**
- Corpora, datasets, benchmarks, models, and tools that are publicly accessible or documented in a peer-reviewed publication
- Multilingual resources that include a meaningful Azerbaijani component (e.g. TUMLU, BLEnD)
- Restricted-access resources where the access process is documented

**Do not include:**
- Proprietary, undocumented internal datasets with no public reference
- Resources with no Azerbaijani content despite an Azerbaijani-language interface
- Duplicate entries for the same artifact (use the existing ID and update the row instead)

---

## How to add a new artifact

### Step 1 — Fork and clone

```bash
git clone https://github.com/almaz-nlp/almaz-registry.git
cd almaz-registry
git checkout -b add/your-artifact-name
```

### Step 2 — Assign an ID

Find the highest existing number in your artifact's type prefix:

```bash
grep "^AZ-CORP" data/registry.csv | tail -5
```

Assign the next sequential number. Example: if the last corpus is `AZ-CORP-009`, your new one is `AZ-CORP-010`.

### Step 3 — Add the row

Open `data/registry.csv` and append your row at the bottom of the appropriate type group. Keep the file sorted by type (`corpus` → `dataset` → `benchmark` → `model` → `tool`), then by ID within each group.

**Template:**
```
AZ-TYPE-NNN,Name,type,layer,source,size,domain,license,https://link,P?,Notes
```

### Step 4 — Validate

```bash
python scripts/validate.py
```

Fix any errors before opening a PR. The CI workflow runs the same validation — a failing check will block your PR from merging.

### Step 5 — Open a pull request

Use the PR title format: `add: AZ-TYPE-NNN — Artifact Name`

Example: `add: AZ-BENCH-005 — AZ-MMLU`

In the PR description, include:
- A one-sentence description of the artifact
- A link to the primary source (paper or repository)
- The license, if you had to look it up

---

## How to correct an existing entry

For small fixes (broken link, wrong license, typo):

```bash
git checkout -b fix/AZ-TYPE-NNN-description
# edit data/registry.csv
python scripts/validate.py
# open PR with title: fix: AZ-TYPE-NNN — brief description
```

For significant changes (reclassification, new size estimate from a published paper):

- Open an issue first describing the proposed change and your evidence
- Once discussed, submit the PR

---

## How to deprecate an artifact

If an artifact is no longer accessible and cannot be recovered:

1. Do not delete the row — IDs must remain stable
2. Change the `license` field to `deprecated`
3. Add a note: `deprecated YYYY-MM — reason. Superseded by AZ-TYPE-NNN.`
4. If a replacement exists, add the replacement as a new row

---

## Validation rules

`scripts/validate.py` enforces the following on every PR:

| Check | Rule |
|---|---|
| No duplicate IDs | Each `id` must be unique across the file |
| No empty required fields | `id`, `name`, `type`, `layer`, `source`, `license`, `link` must be non-empty |
| Controlled type values | `type` must be one of: corpus · dataset · benchmark · model · tool |
| Valid layer values | `layer` must be an integer between 1 and 5 |
| Link reachability | Every `link` must return HTTP 200 (checked on PR, not on every commit) |
| ID format | Must match `AZ-(CORP|DATA|BENCH|MODEL|TOOL)-\d{3}` |

---

## Review process

All PRs are reviewed by a registry maintainer within 7 days. Reviews check:

1. Schema compliance — does the row follow all rules in `schema.md`?
2. Accuracy — is the information correct and sourced?
3. Scope — does the artifact genuinely belong in an Azerbaijani NLP registry?

PRs that pass automated validation and review are merged into `main`. A new patch version is tagged monthly; minor versions are tagged when a ALMAZ paper is submitted.

---

## Versioning policy

| Change type | Version bump | Example |
|---|---|---|
| New artifacts added | patch | `v0.1.0` → `v0.1.1` |
| Corrections to existing rows | patch | `v0.1.1` → `v0.1.2` |
| New type or column added | minor | `v0.1.x` → `v0.2.0` |
| Schema breaking change | major | `v0.x.y` → `v1.0.0` |

Each tagged version is automatically archived on Zenodo with a new DOI. When citing the registry in a paper, always use the DOI of the version current at submission time.

---

## Questions

Open a [GitHub issue](https://github.com/almaz-nlp/almaz-registry/issues) with the label `question`. Do not email maintainers directly for registry questions — public issues build a searchable knowledge base for future contributors.

---

*الماز · алмаз · almaz*

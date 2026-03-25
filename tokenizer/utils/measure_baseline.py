#!/usr/bin/env python3
"""
=== measure_baseline.py ===
Step 4: Measure how badly Qwen tokenizes Azerbaijani before any changes.
Output: baseline_results.txt (via tee)
Run:    python measure_baseline.py | tee baseline_results.txt
"""

from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")

# Standard test phrases
test_texts = [
    "Azərbaycan Respublikasının Konstitusiyası",
    "müstəqilliyin bərpası haqqında",
    "ölkəmizin iqtisadi inkişafı",
    "dövlət büdcəsinin icrası",
    "təhsil sisteminin müasirləşdirilməsi",
    "Bakı şəhərinin gözəl mənzərələri",
    "Azərbaycan xalqının tarixi irsi",
    "müəllimlərin peşəkarlıq səviyyəsi",
    "kitablarımızdan oxuduqlarımız",
    "müasirləşdirilməsindən danışdıq",
]

total_words  = 0
total_tokens = 0

print("=" * 75)
print(f"{'Text':50s} Words  Toks  Ratio")
print("=" * 75)

for text in test_texts:
    tokens = tok.tokenize(text)
    words  = text.split()
    ratio  = len(tokens) / len(words)
    total_words  += len(words)
    total_tokens += len(tokens)
    print(f"{text:50s} {len(words):5d} {len(tokens):5d} {ratio:5.2f}")
    print(f"    → {tokens}")

avg = total_tokens / total_words
print("=" * 75)
print(f"AVERAGE FERTILITY: {avg:.2f}")
print(f"Target:            2.0 – 3.0")
print()

# ── Short ə-words (20 common roots) ──
print("── ə-word breakdown (short) ──")
ə_words_short = [
    "əsas", "dövlət", "təhsil", "həyat", "gözəl",
    "müstəqil", "xəstəxana", "kitabxanə", "ədəbiyyat", "hökumət",
    "əhali", "dərman", "əlaqə", "nəticə", "vətən",
    "məktəb", "müəllim", "nəzər", "dəyər", "əmək",
]
for w in ə_words_short:
    toks = tok.tokenize(w)
    print(f"  {w:25s} → {toks}")

# ── Long agglutinated words (where the real damage shows) ──
print()
print("── Long agglutinated words ──")
ə_words_long = [
    "kitablarımızdakılardan",
    "müasirləşdirilməsindən",
    "edəcəksiniz",
    "görüşəcəyiksə",
    "müstəqilləşdirilməsindən",
    "gələcəkdir",
    "istifadəçilərimizlə",
    "xəstəxanalarımızdakı",
    "dəyişdirilməməlidir",
    "razılaşdırılmışdır",
]
for w in ə_words_long:
    toks = tok.tokenize(w)
    print(f"  {w:35s} → {toks}  ({len(toks)} tokens)")

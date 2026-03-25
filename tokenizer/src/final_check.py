#!/usr/bin/env python3
"""
=== final_check.py ===
Step 8a: Compare fertility before/after on test phrases.
         Runs all acceptance criteria checks.
Run:     python final_check.py | tee final_results.txt
"""

from transformers import AutoTokenizer

old_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_original")
new_tok = AutoTokenizer.from_pretrained("./qwen3_tokenizer_azerbaijani")

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

print("=" * 85)
print(f"{'Text':45s} {'Before':>7s} {'After':>7s} {'Change':>8s}")
print("=" * 85)

total_old = total_new = total_words = 0

for text in test_texts:
    words      = text.split()
    old_tokens = old_tok.tokenize(text)
    new_tokens = new_tok.tokenize(text)
    old_r = len(old_tokens) / len(words)
    new_r = len(new_tokens) / len(words)
    delta = ((old_r - new_r) / old_r) * 100

    total_old   += len(old_tokens)
    total_new   += len(new_tokens)
    total_words += len(words)

    print(f"{text:45s} {old_r:7.2f} {new_r:7.2f} {delta:+7.0f}%")
    print(f"    old: {old_tokens}")
    print(f"    new: {new_tokens}")
    print()

avg_old = total_old / total_words
avg_new = total_new / total_words
delta   = ((avg_old - avg_new) / avg_old) * 100

print("=" * 85)
print(f"{'AVERAGE FERTILITY':45s} {avg_old:7.2f} {avg_new:7.2f} {delta:+7.0f}%")
print(f"\nOriginal vocab:  {len(old_tok):,}")
print(f"Extended vocab:  {len(new_tok):,}")
print(f"Added:           {len(new_tok) - len(old_tok):,}")

# ── Short ə-words (20 common roots) ──
print("\n── ə-word integrity (must NOT split at ə) ──")
ə_words_short = [
    "əsas", "dövlət", "təhsil", "həyat", "gözəl",
    "müstəqil", "xəstəxana", "ədəbiyyat", "hökumət", "əhali",
    "dərman", "əlaqə", "nəticə", "vətən", "məktəb",
    "müəllim", "nəzər", "dəyər", "əmək", "tərəf",
]

ok = 0
for w in ə_words_short:
    toks = new_tok.tokenize(w)
    broken = any(t.strip() in ("ə", "Ä", "Ļ") for t in toks)
    tag = "✗" if broken else "✓"
    if not broken:
        ok += 1
    print(f"  {tag}  {w:20s} → {toks}")

print(f"\nShort words passed: {ok}/20")

# ── Long agglutinated words (where morpheme boundaries matter) ──
print("\n── Long agglutinated words (morpheme boundary quality) ──")
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

ok_long = 0
for w in ə_words_long:
    old_toks = old_tok.tokenize(w)
    new_toks = new_tok.tokenize(w)
    improved = len(new_toks) < len(old_toks)
    broken   = any(t.strip() in ("ə", "Ä", "Ļ") for t in new_toks)
    if not broken:
        ok_long += 1
    tag = "✗" if broken else "✓"
    print(f"  {tag}  {w:35s}  {len(old_toks):2d} → {len(new_toks):2d} tokens  {new_toks}")

print(f"\nLong words passed (no ə split): {ok_long}/10")

# ─── ACCEPTANCE CRITERIA ──────────────────────────────
print("\n" + "=" * 85)
print("ACCEPTANCE CRITERIA")
print("=" * 85)

checks_passed = 0
total_checks = 5

# 1. Fertility target
if avg_new <= 3.0:
    print(f"✓ Fertility {avg_new:.2f} is within target (≤ 3.0)")
    checks_passed += 1
elif avg_new <= 3.5:
    print(f"⚠ Fertility {avg_new:.2f} is close but above target (≤ 3.0)")
else:
    print(f"✗ FAIL: Fertility {avg_new:.2f} — still above 3.5!")
    print("  → ESCALATE: ratio did not drop enough.")

# 2. Improvement percentage
if delta >= 30:
    print(f"✓ Improvement {delta:.0f}% (target: ≥ 30%)")
    checks_passed += 1
else:
    print(f"✗ FAIL: Improvement only {delta:.0f}% — need at least 30%.")

# 3. ə-word check (short words)
if ok >= 18:
    print(f"✓ ə-words: {ok}/20 passed (need ≥ 18)")
    checks_passed += 1
else:
    print(f"✗ FAIL: Only {ok}/20 ə-words passed (need ≥ 18)")

# 4. Token count
added = len(new_tok) - len(old_tok)
if 8000 <= added <= 15000:
    print(f"✓ Added tokens: {added:,} (target: 8,000–15,000)")
    checks_passed += 1
elif 5000 <= added <= 25000:
    print(f"⚠ Added tokens: {added:,} — outside ideal range but acceptable")
    checks_passed += 1
else:
    print(f"✗ FAIL: Added tokens: {added:,} — outside acceptable range!")
    print("  → ESCALATE.")

# 5. Tokenizer loads
print("✓ Extended tokenizer loads without errors")
checks_passed += 1

print(f"\n{'='*85}")
if checks_passed == total_checks:
    print(f"✓ ALL {total_checks} ACCEPTANCE CRITERIA PASSED")
    print("  Task complete. Deliver: qwen3_tokenizer_azerbaijani/, new_tokens.tsv,")
    print("  final_results.txt, and corpus_results.txt (from corpus_ratio.py).")
else:
    print(f"✗ {total_checks - checks_passed} CHECK(S) FAILED — review above.")
    print("  Do NOT deliver until all checks pass.")
print(f"{'='*85}")

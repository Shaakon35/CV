#!/usr/bin/env python3
"""Score a CV against a job offer for ATS keyword match and readability.

Estimates how an applicant tracking system would rank the CV by measuring how
many keywords from the job offer appear in the CV text, plus basic readability
and AI-filler signals. This is a heuristic aid, not a real ATS - use it to find
missing keywords before submitting.

Usage:
    python3 ats_score.py --cv path/to/cv.txt --offer path/to/job-offer.txt
    # CV may be plain text or extracted first with:  pdftotext cv.pdf cv.txt

Output: a human-readable report plus a machine-readable summary line
    SCORE=<0-100> COVERED=<n> MISSING=<n>
"""
import argparse
import re
import sys
from collections import Counter

# Words too generic to count as meaningful keywords.
STOPWORDS = set("""
a an the and or but if then else for to of in on at by with without from as is
are was were be been being this that these those it its their his her our your
you we they i he she will would can could should may might must shall do does
did have has had not no yes than into over under out up down more most less
least very much many few all any some such per via etc we're you'll role job
position candidate applicant company team work working experience years year
ability able strong good excellent required preferred responsibilities skills
skill including include includes about across also within using use used well
who whom which what when where why how our the a an
""".split())

# Words that make text read as AI-generated / generic. Flag for review.
AI_FILLER = [
    "leverage", "leveraging", "spearheaded", "passionate", "results-driven",
    "dynamic", "synergy", "seamless", "seamlessly", "cutting-edge",
    "fast-paced", "proven track record", "detail-oriented", "team player",
    "go-getter", "thought leader", "best-in-class", "world-class",
    "value-add", "deep dive", "move the needle", "hit the ground running",
]


def normalize(text: str) -> str:
    # Lowercase; keep tech chars (+ # / . -) and use other punctuation as
    # phrase boundaries so n-grams never cross commas/periods.
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#/.\- ]", " | ", text)  # boundary marker
    return text


def clean_token(t: str) -> str:
    return t.strip(".-/")


def tokens(text: str):
    # Keep tech tokens like c++, ci/cd, r, .net
    return [clean_token(t) for t in re.findall(r"[a-z0-9][a-z0-9+#/.\-]*",
                                               normalize(text)) if clean_token(t)]


def _segments(text: str):
    """Split normalized text into boundary-free token runs."""
    for seg in normalize(text).split("|"):
        toks = [clean_token(t) for t in re.findall(r"[a-z0-9][a-z0-9+#/.\-]*", seg)]
        toks = [t for t in toks if t]
        if toks:
            yield toks


def phrases(text: str, n_max=3):
    """Yield 1..n_max word phrases, never crossing a punctuation boundary."""
    for toks in _segments(text):
        for n in range(1, n_max + 1):
            for i in range(len(toks) - n + 1):
                yield toks[i:i + n]


def keyword_candidates(offer: str):
    """Rank candidate keywords/phrases from the offer.

    Includes both meaningful single tokens (tech terms) and specific multi-word
    phrases. A single keyword is kept even if it also appears inside a phrase,
    because an ATS matches either form.
    """
    single = Counter()
    multi = Counter()
    for parts in phrases(offer, 3):
        # strip leading/trailing stopwords from phrases
        while parts and parts[0] in STOPWORDS:
            parts = parts[1:]
        while parts and parts[-1] in STOPWORDS:
            parts = parts[:-1]
        if not parts:
            continue
        ph = " ".join(parts)
        if len(ph) < 2:
            continue
        if len(parts) == 1:
            if parts[0] not in STOPWORDS and len(parts[0]) >= 2:
                single[ph] += 1
        elif not any(p in STOPWORDS for p in parts):
            multi[ph] += len(parts)  # weight specific phrases higher

    top_single = [k for k, _ in single.most_common(25)]
    top_multi = [k for k, _ in multi.most_common(25)]

    # Merge: prefer specific multi-word phrases, then add single tech keywords
    # not already represented as their own concept.
    kept = []
    for kw in top_multi:
        if any(kw != o and kw in o for o in kept):
            continue
        kept.append(kw)
    for kw in top_single:
        kept.append(kw)
    # de-dup preserving order
    seen, out = set(), []
    for kw in kept:
        if kw not in seen:
            seen.add(kw)
            out.append(kw)
    return out[:40]


def contains(cv_text: str, kw: str) -> bool:
    return re.search(r"(?<![a-z0-9])" + re.escape(kw) + r"(?![a-z0-9])",
                     cv_text) is not None


def readability(cv_text: str):
    # Note: pdftotext splits a CV into many short lines, so sentence stats from
    # extracted PDF text are approximate. For accurate readability, run against
    # the prose sections rather than a bullet-heavy PDF dump.
    sents = [s for s in re.split(r"[.!?\n]", cv_text) if s.strip()]
    words = tokens(cv_text)
    avg = (len(words) / len(sents)) if sents else 0
    # crude sentence-length variation (human text varies more)
    lengths = [len(s.split()) for s in sents if s.split()]
    if len(lengths) > 1:
        mean = sum(lengths) / len(lengths)
        var = sum((x - mean) ** 2 for x in lengths) / len(lengths)
    else:
        var = 0
    return len(words), len(sents), avg, var ** 0.5


def find_filler(cv_text: str):
    found = []
    for w in AI_FILLER:
        if w in cv_text:
            found.append(w)
    return found


def main() -> int:
    ap = argparse.ArgumentParser(description="ATS keyword/readability scorer")
    ap.add_argument("--cv", required=True, help="CV text file (pdftotext output)")
    ap.add_argument("--offer", required=True, help="job offer text file")
    ap.add_argument("--top", type=int, default=40, help="max keywords to check")
    args = ap.parse_args()

    with open(args.cv, encoding="utf-8", errors="replace") as f:
        cv_raw = f.read()
    with open(args.offer, encoding="utf-8", errors="replace") as f:
        offer_raw = f.read()

    cv_norm = normalize(cv_raw)
    kws = keyword_candidates(offer_raw)[:args.top]

    covered, missing = [], []
    for kw in kws:
        (covered if contains(cv_norm, kw) else missing).append(kw)

    score = round(100 * len(covered) / len(kws)) if kws else 0
    words, sents, avg, sd = readability(cv_raw)
    filler = find_filler(cv_norm)

    print("=" * 60)
    print("ATS MATCH REPORT")
    print("=" * 60)
    print(f"Keyword match score : {score}/100  "
          f"({len(covered)}/{len(kws)} keywords)")
    print()
    print(f"COVERED ({len(covered)}):")
    print("  " + ", ".join(covered) if covered else "  (none)")
    print()
    print(f"MISSING - add if you legitimately have these ({len(missing)}):")
    print("  " + ", ".join(missing) if missing else "  (none)")
    print()
    print("Readability:")
    print(f"  words={words}  sentences={sents}  "
          f"avg sentence len={avg:.1f}  length variation(sd)={sd:.1f}")
    if avg > 28:
        print("  ! Sentences run long; tighten for scannability.")
    if sd < 4 and sents > 5:
        print("  ! Low sentence-length variation reads as AI-generated; vary it.")
    print()
    if filler:
        print(f"AI-filler words to remove ({len(filler)}):")
        print("  " + ", ".join(filler))
    else:
        print("AI-filler words: none found (good).")
    print()
    print(f"SCORE={score} COVERED={len(covered)} MISSING={len(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

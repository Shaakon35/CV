#!/usr/bin/env python3
"""ATS-safe character sanitizer for CV text and LaTeX source.

Workday and most ATS/resume-autofill parsers choke on "smart" typography and
non-ASCII symbols. They silently drop them, mangle field boundaries, or fail the
autofill entirely. This script rewrites problem characters to plain ASCII
equivalents so the parsed text is clean.

Usage:
    # Check a file, report offending characters, exit non-zero if any remain:
    python3 ats_sanitize.py --check path/to/cv.tex

    # Rewrite a file in place to ASCII-safe equivalents:
    python3 ats_sanitize.py --fix path/to/cv.tex

    # Pipe text through:
    echo "text" | python3 ats_sanitize.py

Exit codes:
    0  clean (or fixed successfully)
    1  --check found offending characters
"""
import argparse
import sys
import unicodedata

# Direct one-to-one replacements. Left = risky char, right = ASCII-safe.
REPLACEMENTS = {
    # Dashes and hyphens -> plain hyphen
    "\u2010": "-",   # hyphen
    "\u2011": "-",   # non-breaking hyphen
    "\u2012": "-",   # figure dash
    "\u2013": "-",   # en dash
    "\u2014": "-",   # em dash
    "\u2015": "-",   # horizontal bar
    "\u2212": "-",   # minus sign
    # Quotes -> straight quotes
    "\u2018": "'",   # left single quote
    "\u2019": "'",   # right single quote / apostrophe
    "\u201A": "'",   # single low quote
    "\u201B": "'",
    "\u201C": '"',   # left double quote
    "\u201D": '"',   # right double quote
    "\u201E": '"',   # double low quote
    "\u00AB": '"',   # <<
    "\u00BB": '"',   # >>
    # Spaces -> normal space
    "\u00A0": " ",   # non-breaking space
    "\u2007": " ",
    "\u2009": " ",   # thin space
    "\u200A": " ",
    "\u202F": " ",   # narrow no-break space
    "\u200B": "",    # zero-width space (delete)
    "\uFEFF": "",    # BOM / zero-width no-break (delete)
    "\u200C": "",    # zero-width non-joiner
    "\u200D": "",    # zero-width joiner
    # Bullets and list glyphs -> hyphen
    "\u2022": "-",   # bullet
    "\u2023": "-",
    "\u25E6": "-",
    "\u2043": "-",
    "\u2219": "-",
    "\u00B7": "-",   # middle dot
    # Ellipsis
    "\u2026": "...",
    # Symbols that break autofill / look "AI-generated"
    "\u2192": "->",  # right arrow
    "\u2190": "<-",
    "\u21D2": "=>",
    "\u2713": "",    # check mark (delete; ATS reads it as noise)
    "\u2714": "",
    "\u2717": "",
    "\u2718": "",
    "\u2605": "",    # star
    "\u2606": "",
    "\u25CF": "-",   # black circle
    "\u25AA": "-",   # black small square
    "\u2588": "",    # full block
    # Math-ish symbols spelled out (safer than < > + in parsed text)
    "\u2264": " or fewer",   # <=
    "\u2265": " or more",    # >=
    "\u00D7": "x",           # multiplication sign
    "\u00F7": "/",           # division sign
    "\u2260": "!=",
    "\u00B1": " plus or minus ",
    # Common typographic symbols
    "\u2122": "(TM)",
    "\u00AE": "(R)",
    "\u00A9": "(C)",
    "\u20AC": "EUR",
    "\u00A3": "GBP",
    "\u00A5": "JPY",
    "\u2153": "1/3", "\u00BC": "1/4", "\u00BD": "1/2", "\u00BE": "3/4",
    # Ligatures
    "\uFB01": "fi", "\uFB02": "fl",
}

# Characters that are risky in the *parsed plain text* of a resume even though
# they are valid ASCII. We only flag these in --check for prose lines; we do
# NOT auto-rewrite them because they are legitimate in LaTeX markup.
RISKY_ASCII_IN_PROSE = set("<>|^~`")


def sanitize(text: str) -> str:
    for bad, good in REPLACEMENTS.items():
        text = text.replace(bad, good)
    # Normalize accented letters to base ASCII where possible (e -> e, etc.)
    # Keep letters that have a clean decomposition; drop stray combining marks.
    normalized = unicodedata.normalize("NFKD", text)
    out = []
    for ch in normalized:
        if unicodedata.combining(ch):
            continue  # drop accents/diacritics
        if ord(ch) < 128:
            out.append(ch)
        else:
            # Last-resort: replace any remaining non-ASCII with a space so the
            # parser never sees an unknown glyph.
            out.append(" ")
    return "".join(out)


def find_offenders(text: str):
    offenders = {}
    for i, ch in enumerate(text):
        if ord(ch) > 127 or ch in {"\u00A0"}:
            offenders.setdefault(ch, 0)
            offenders[ch] += 1
    return offenders


def main() -> int:
    ap = argparse.ArgumentParser(description="ATS-safe character sanitizer")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--check", action="store_true",
                   help="report non-ASCII characters, exit 1 if any found")
    g.add_argument("--fix", action="store_true",
                   help="rewrite the file in place to ASCII-safe equivalents")
    ap.add_argument("path", nargs="?", help="file to process (else read stdin)")
    args = ap.parse_args()

    if args.path and args.path != "-":
        with open(args.path, encoding="utf-8") as f:
            text = f.read()
    else:
        args.path = None  # treat "-" as stdin, disable in-place write
        text = sys.stdin.read()

    if args.check:
        offenders = find_offenders(text)
        if offenders:
            print("Non-ASCII / risky characters found:", file=sys.stderr)
            for ch, n in sorted(offenders.items(), key=lambda x: -x[1]):
                name = unicodedata.name(ch, "UNKNOWN")
                print(f"  U+{ord(ch):04X} {name!s:<30} x{n}", file=sys.stderr)
            print("\nRun with --fix to rewrite them.", file=sys.stderr)
            return 1
        print("Clean: no non-ASCII characters.", file=sys.stderr)
        return 0

    result = sanitize(text)

    if args.fix and args.path:
        with open(args.path, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Sanitized {args.path}", file=sys.stderr)
        return 0

    sys.stdout.write(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

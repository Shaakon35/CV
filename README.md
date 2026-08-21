# CV

Master CV in LaTeX, with per-job tailored versions. Auto-built to PDF and
checked for ATS/Workday safety by GitHub Actions.

## Structure

```
cv_master.tex             # master CV - the source of truth
cover_letter_master.tex   # master cover letter (position + date are variables)
2026/ 2027/ 2028/         # tailored applications, one subfolder per job per year
  company-role/
    cv.tex                # tailored CV source
    cv.pdf                # built, ATS-safe CV
    cover_letter.tex      # tailored cover letter source
    cover_letter.pdf      # built, ATS-safe cover letter
    job-offer.txt         # the job description used for tailoring
    keywords.md           # ATS keyword coverage notes
.ona/skills/
  tailor-cv/              # tailors the CV to a job (ATS-safe + authentic)
  cover-letter/           # tailors the cover letter (auto position + date)
  ats-score/              # scores a CV/letter against a job offer
.github/workflows/        # CI: builds every .tex, verifies ATS-safe text layer
```

## How to tailor a CV

Ask Ona: "tailor my CV for this job" and paste the job description. Ona runs the
`tailor-cv` skill, which:

1. Saves the job offer and extracts ATS keywords.
2. Adapts `cv_master.tex` into `<year>/<company-role>/cv.tex`, matching the
   posting's keywords and job title using only real experience.
3. Sanitizes all characters to ASCII so Workday resume-autofill works.
4. Builds the PDF and verifies the PDF text layer is ATS-safe.
5. Reports keyword coverage.

## How to write a cover letter

Ask Ona: "cover letter for this job". The `cover-letter` skill copies
`cover_letter_master.tex`, then changes only two variables at the top of the
file:

```latex
\newcommand{\Position}{...}   % renders in BOTH body mentions automatically
\newcommand{\SignDate}{...}   % renders under the signature (DD/MM/YYYY)
```

You never hand-edit the two position sentences - changing `\Position` updates
both. Ona also proposes optional content improvements aligned to the job offer
(you approve before they are applied), then builds and ATS-verifies the PDF.

## How to score a CV against a job

Ask Ona: "score my CV against this job". The `ats-score` skill extracts the PDF
text, compares it to the job offer, and reports a keyword-match score out of 100,
covered vs missing keywords, readability, and AI-filler words to remove. Use it
before submitting, then feed the findings back to `tailor-cv` and re-score.

## Why "ATS-safe" matters

Workday and most applicant tracking systems parse the PDF's text layer, not the
visual layout. Smart quotes, em dashes, bullet glyphs, arrows, math symbols, and
icon fonts get dropped or mangled and break autofill. This repo enforces plain
ASCII in both the source and the rendered PDF:

- List markers render as a hyphen, not a bullet glyph.
- No icon fonts in contact details (plain text instead).
- Date ranges written as "2021 to Present".
- A sanitizer script rewrites any stray non-ASCII character.

Check any file yourself:

```bash
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check cv_master.tex
pdftotext cv_master.pdf - | \
  python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check -
```

## Building locally (optional)

```bash
tectonic cv_master.tex          # or any tailored cv.tex
```

CI does this automatically on every push and fails if a PDF's text layer
contains non-ASCII characters.

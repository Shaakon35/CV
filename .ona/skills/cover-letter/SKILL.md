---
name: cover-letter
description: Generate a tailored, ATS-safe cover letter for a specific job from cover_letter_master.tex. Automatically updates the position title (which appears twice in the body) and the signature date via the two variables at the top of the master, then proposes optional content improvements to better match the job offer. Use EVERY time the user asks for a cover letter, to redo/adapt/tailor a cover letter, or applies to a new position. Triggers on "cover letter", "motivation letter", "redo my cover letter", "cover letter for <company/role>", "tailor my cover letter", "letter for this job".
---

# Cover Letter

Produce a job-specific cover letter from `cover_letter_master.tex` (repo root),
saved next to the tailored CV under the correct year folder.

## The two variables that MUST change every time

`cover_letter_master.tex` defines exactly two per-application variables near the
top. Changing them updates every occurrence automatically:

```latex
\newcommand{\Position}{PKS Data Scientist \& Scientific Software Engineer}
\newcommand{\SignDate}{03/07/2026}
```

- `\Position` renders in BOTH places it is mentioned in the body. Never hand-edit
  the two sentences; only change this one command.
- `\SignDate` renders under the signature. Format DD/MM/YYYY.

When escaping the position for LaTeX: `&` becomes `\&`, `%` becomes `\%`,
`#` becomes `\#`. Keep it plain ASCII (the ATS sanitizer enforces this).

## Workflow (follow every time)

### 1. Get the target details
Ask for (or infer from the job offer): the exact position title and the
signature date. If a job offer is available, reuse the one saved by the
`tailor-cv` skill at `<year>/<company-role>/job-offer.txt`.

### 2. Copy the master into the application folder
```
cp cover_letter_master.tex <year>/<company-role>/cover_letter.tex
```
Use the SAME `<year>/<company-role>/` folder as the tailored CV so each
application is self-contained.

### 3. Set the two variables
Edit only `\Position` and `\SignDate` in the copied file. Do not touch the body
sentences - the position propagates automatically.

### 4. Propose improvements (do not apply silently)
Read the job offer and the letter, then PROPOSE targeted edits for the user to
approve before applying. Focus on:
- Aligning the opening and the four bullet themes (Leadership, Strategic Mindset,
  Technical & Product Ownership, AI) with the offer's priorities and wording.
- Weaving in 2-4 exact keywords from the offer where they fit naturally.
- Fixing any claim that does not match this specific role.
Keep the author's voice and real experience. Never fabricate. Present the
proposals as a short list and ask which to apply. Read
`../tailor-cv/references/ats-and-authenticity.md` for the keyword and
authenticity rules (same rules apply to letters).

### 5. Enforce ATS-safe characters
```
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --fix  <year>/<company-role>/cover_letter.tex
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check <year>/<company-role>/cover_letter.tex
```
`--check` MUST exit 0.

### 6. Build and verify the rendered text layer
```
tectonic <year>/<company-role>/cover_letter.tex
pdftotext <year>/<company-role>/cover_letter.pdf - | \
  python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check -
```
This MUST exit 0. The master's font setup (fontspec with `Mapping=` and
`Ligatures=NoCommon`) keeps quotes straight and removes fi/fl ligatures; preserve
it in the copy. Show an inline PDF preview.

## Definition of done
- `<year>/<company-role>/cover_letter.tex` and `.pdf` exist.
- `\Position` and `\SignDate` reflect this application; position appears correctly
  in both body mentions.
- Both `--check` runs (source and rendered PDF text) exit 0.
- Improvement proposals were shown; only approved edits applied.
- No fabricated content.

## Hard rules
- Change the position and date ONLY via `\Position` and `\SignDate`.
- Propose content changes; apply them only after the user approves.
- Keep the letter ATS-safe in both source and rendered PDF text layer.

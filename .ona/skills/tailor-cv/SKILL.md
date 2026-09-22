---
name: tailor-cv
description: Tailor the master CV and cover letter to a specific job offer, producing ATS-safe, human-sounding LaTeX sources and PDFs with the repository's canonical per-application artifact set. Enforces Workday-safe characters (no smart dashes, quotes, arrows, math symbols, or accents that break resume autofill) and maximizes ATS keyword match against the job description while keeping the writing authentic enough to pass AI-detection screens. Use EVERY time the user asks to redo, tailor, adapt, rewrite, or generate a CV or resume for a job. Triggers on "redo my CV", "tailor my CV", "adapt my resume", "make a CV for a job", "new CV", "CV for a company", "rewrite my resume".
---

# Tailor CV

Adapt `cv_master.tex` (repo root) into a job-specific CV saved under the correct
year folder. Always produce ATS-safe, authentic output.

## Repository layout (do not break)

```
cv_master.tex        # master CV - source of truth, edit rarely
cover_letter_master.tex # master cover letter - source of truth, edit rarely
2026/ 2027/ 2028/    # one subfolder per application, per year
.ona/skills/tailor-cv/
  scripts/ats_sanitize.py            # ASCII sanitizer (Workday-safe)
  references/ats-and-authenticity.md # ATS keyword + AI-detection guidance
```

## Workflow (follow in order every time)

### 1. Get the job offer
Ask the user to paste the job description (or a URL). If none is given, ask once.
Save it verbatim to `<year>/<company-role>/job-offer.txt`.

### 2. Read the guidance
Read `references/ats-and-authenticity.md` before writing. It defines the keyword
strategy, the banned character list, the AI-filler words to avoid, and the
honesty guardrail.

### 3. Extract keywords
From the job offer, list: exact job title, required hard skills, tools, methods,
certifications, and preferred items. Preserve the offer's exact wording. Write
them to `<year>/<company-role>/keywords.md`.

### 4. Create the complete application artifact set
Create all per-application deliverables in `<year>/<company-role>/`.

Use privacy-safe, role-specific filenames that never include the target
employer's name:
- CV source: `<year>/<company-role>/CV_ValentinLegras_<ROLE>.tex`
- CV PDF: `<year>/<company-role>/CV_ValentinLegras_<ROLE>.pdf`
- Cover letter source: `<year>/<company-role>/cover_letter.tex`
- Cover letter PDF: `<year>/<company-role>/cover_letter.pdf`
- Offer notes: `<year>/<company-role>/job-offer.txt`
- Keyword coverage: `<year>/<company-role>/keywords.md`

For `<ROLE>`, use a short ASCII role token such as `PKS`, `AIDD`,
`Clinical_Data_Science`, or `Pharmacometrics`. Do not leave the final CV only as
`cv.tex`, and do not use the target company name in the filename.

Copy `cv_master.tex` to the role-named CV source, copy
`cover_letter_master.tex` to `cover_letter.tex`, then adapt:
- Mirror the job title in the summary/target line if the user qualifies.
- Reorder and rephrase existing experience to surface the required keywords in
  the summary, skills, and most-recent-role bullets.
- Use both spelled-out terms and acronyms on first use.
- Only use experience already present in `cv_master.tex`. Never invent employers,
  dates, metrics, or skills. If a required skill is missing, tell the user.
- Write like a human: concrete metrics, specific tool/team names, varied
  sentence length. Avoid the AI-filler word list in the reference.
- Never name the TARGET company (the employer being applied to) in the tailored
  CV, the job title line, the file name, the folder name, or commit messages.
  The user may be applying discreetly and does not want colleagues to know.
  Refer to the target role generically (e.g. "PKS Data Scientist"), never
  "<Company> PKS Data Scientist". This applies ONLY to the target employer -
  the user's genuine PAST employers (including in `cv_master.tex`) must be kept
  by name as real work history.
- Tailor the cover letter to the same role using only factual content from the
  master CV. If the role has material gaps, state the fit honestly rather than
  pretending full qualification.

### 5. Enforce ATS-safe characters (mandatory)
Rewrite the tailored source to ASCII, then verify it is clean:
```
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --fix  <year>/<company-role>/CV_ValentinLegras_<ROLE>.tex
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --fix  <year>/<company-role>/cover_letter.tex
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check <year>/<company-role>/CV_ValentinLegras_<ROLE>.tex
python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check <year>/<company-role>/cover_letter.tex
```
The `--check` MUST exit 0 (report "Clean"). If it flags characters, fix them and
re-check. Do not deliver a CV or cover letter that fails this check.

Note: `--fix` strips accents and non-ASCII from the LaTeX source. Keep any
required LaTeX commands (e.g. `\href`) intact; if the CV legitimately needs an
accent for a name, add it via a LaTeX command (e.g. `\'e`) rather than a raw
accented byte, then re-run `--check`.

### 6. Build the PDF
```
tectonic <year>/<company-role>/CV_ValentinLegras_<ROLE>.tex
tectonic <year>/<company-role>/cover_letter.tex
```
If Tectonic is missing, install it (see repo README) or use an equivalent XeLaTeX
build path if Tectonic is unavailable. Then render a preview image of the CV
with `pdftoppm -png -r 130 CV_ValentinLegras_<ROLE>.pdf preview` and show it
inline.

### 6a. Enforce the 2-page limit (mandatory)
The CV must NEVER exceed 2 pages. After building, check the page count:
```
pdfinfo <year>/<company-role>/CV_ValentinLegras_<ROLE>.pdf | grep Pages
```
If it reports more than 2 pages, tighten until it fits 2, in this order (least
destructive first) and rebuild after each change:
1. Trim the least-relevant bullets (older/less-relevant roles first).
2. Tighten wording - shorter sentences, drop filler, merge overlapping bullets.
3. Reduce inter-role spacing (the `\vspace` in `\rolel`/`\role`) by 1-2pt.
4. Reduce `geometry` margin slightly (e.g. 1.2cm -> 1.1cm) as a last resort.
Never shrink the body font below 10pt or margins below 1.0cm. Re-run the ATS
checks (steps 5 and 7) after any edit. Do not deliver a CV over 2 pages.

### 7. Verify the text layer parses
Confirm the PDF's extracted text is ASCII and readable (the parser sees this,
not the layout):
```
pdftotext <year>/<company-role>/CV_ValentinLegras_<ROLE>.pdf - | python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check -
pdftotext <year>/<company-role>/cover_letter.pdf - | python3 .ona/skills/tailor-cv/scripts/ats_sanitize.py --check -
```

### 8. Report keyword coverage
Update `keywords.md` marking each required keyword as covered and where it
appears. Tell the user any required keyword you could NOT cover honestly.

## Definition of done
- Tailored `CV_ValentinLegras_<ROLE>.tex`,
  `CV_ValentinLegras_<ROLE>.pdf`, `cover_letter.tex`, `cover_letter.pdf`,
  `job-offer.txt`, and `keywords.md` exist in `<year>/<company-role>/`.
- The final CV filename does not include the target employer name.
- `ats_sanitize.py --check` on both tailored `.tex` files and both extracted PDF
  text layers exits 0.
- The built CV PDF is at most 2 pages (`pdfinfo ... | grep Pages` reports 1 or
  2). The cover letter should usually be 1 page unless the user asks otherwise.
- No fabricated content; every required keyword either covered or flagged.
- Inline PDF preview shown to the user.

## Template-level render rules (critical)
The sanitizer checks source bytes, but some risky characters are introduced by
LaTeX at RENDER time and only appear in the PDF text layer. `cv_master.tex`
already handles these; preserve them in every tailored copy:
- `\renewcommand{\labelitemi}{-}` so `itemize` markers render as a hyphen, not a
  U+2022 bullet.
- Plain-text header contact info. NO icon fonts (fontawesome): icon glyphs
  render as garbage codepoints in the text layer and break autofill.
- Date ranges as "2021 to Present", never `2021 -- 2024` (renders as en dash).
- Use `\%` for percent and spell out comparisons ("5 or more years").
Step 7 (pdftotext piped into `--check`) is what catches violations of these.
It MUST exit 0.

## Hard rules
- The CV must never be longer than 2 pages. Always verify with `pdfinfo` after
  building and trim/tighten until it fits (see step 6a).
- Never emit smart quotes, em/en dashes, arrows, checkmarks, bullets-as-glyphs,
  math comparison symbols, plus/minus, or accented bytes in the parsed text OR
  the rendered PDF text layer.
- Never fabricate experience to match keywords.
- Never keyword-stuff or use hidden text.
- Never mention the TARGET company's name anywhere in a tailored CV or its
  surrounding files (CV text, title line, file name, folder name, job-offer.txt
  header, keywords.md, or commit messages). Keep the user's real PAST employers
  named in `cv_master.tex` and in tailored CVs - the restriction is only on the
  employer being applied to.

# ATS keywords and authenticity guidance

Read this when tailoring a CV to a specific job offer. It covers two goals:
1. Maximize ATS keyword match against the job description.
2. Keep the writing human so it passes "AI-generated" screening and reads as
   authentic to a human reviewer.

## Table of contents
- [1. Character safety (Workday autofill)](#1-character-safety-workday-autofill)
- [2. ATS keyword matching](#2-ats-keyword-matching)
- [3. Passing AI-detection / authenticity screens](#3-passing-ai-detection--authenticity-screens)
- [4. Layout rules ATS parsers need](#4-layout-rules-ats-parsers-need)
- [5. Honesty guardrail](#5-honesty-guardrail)

## 1. Character safety (Workday autofill)

Workday and similar parsers read the PDF text layer, not the visual layout.
Non-ASCII glyphs get dropped or split fields incorrectly. Always run the
sanitizer before delivering:

```
python3 scripts/ats_sanitize.py --check 2026/company-role/cv.tex
```

Never use in the *parsed text* of the CV:
- Smart quotes, em/en dashes, non-breaking spaces
- Bullet glyphs, checkmarks, arrows, stars
- Math symbols: greater-than or less-than signs, plus/minus, multiplication
- Accented letters where an ASCII spelling exists (parsers vary)
- Emoji or icon fonts in body text (header contact icons are acceptable only
  if the same info is ALSO present as plain text)

Prefer instead:
- Plain hyphen for ranges and list markers
- The word "to" for ranges in dates ("2021 to Present")
- Spelled-out comparisons ("5 or more years", "reduced by 30 percent")

## 2. ATS keyword matching

ATS ranks a CV by how well its terms overlap the job description. Workflow:

1. **Extract keywords from the job offer.** Pull hard skills, tools, methods,
   certifications, and the exact job title. Note the precise wording (e.g. if
   the offer says "CI/CD" use "CI/CD", not just "pipelines").
2. **Capture variants.** Include both the spelled-out term and the acronym on
   first use: "Continuous Integration and Continuous Delivery (CI/CD)". ATS may
   search for either form.
3. **Match the job title.** If you qualify, mirror the posting's title in your
   summary or a target-role line. Exact-title match is a strong ranking signal.
4. **Place keywords where they count.** Highest weight: summary, skills section,
   and the most recent role's bullets. Distribute naturally; do not dump a list.
5. **Cover the "required" list first,** then "preferred". Aim to address every
   required item you legitimately have.
6. **Save coverage notes** to `keywords.md` in the application folder: list each
   required keyword and where it now appears in the CV.

Anti-patterns that get flagged or rejected:
- Keyword stuffing / hidden white text (instant reject at human review)
- Copying whole sentences from the job description verbatim
- Claiming skills you cannot back up in an interview

## 3. Passing AI-detection / authenticity screens

Recruiters increasingly run CVs through AI-text detectors. Generic LLM prose is
the main trigger. To read as human-written:

- **Cut AI-favored filler words.** Avoid: "leverage", "spearheaded",
  "passionate", "results-driven", "dynamic", "synergy", "seamless",
  "cutting-edge", "in today's fast-paced world", "proven track record",
  "detail-oriented team player". Detectors and recruiters both pattern-match
  these.
- **Lead with concrete, specific facts.** Real metrics, real tool names, real
  team sizes. Specificity is the strongest human signal ("cut nightly build
  from 22 to 6 minutes" beats "significantly improved build performance").
- **Vary sentence length and structure.** AI text is rhythmically uniform. Mix
  short fragments with longer bullets. Not every bullet needs to start with a
  past-tense verb.
- **Keep the candidate's real voice.** Reuse phrasing and terminology from the
  master CV rather than rewriting everything into generic prose.
- **Avoid perfectly parallel, templated bullets.** Slight natural variation
  reads as human.
- **No hallucinated detail.** Do not invent employers, dates, metrics, or
  certifications to sound impressive. Fabrication fails both detectors and
  background checks.

The best defense against AI-detection is real content: numbers, names, and the
candidate's own words. Do not try to "trick" detectors with invisible
characters or spacing hacks; the sanitizer strips those anyway and they get the
CV rejected.

## 4. Layout rules ATS parsers need

- Single-column body for the parsed sections (multi-column can scramble reading
  order in some parsers). A light sidebar is tolerable only if the text still
  extracts in order; when in doubt, single column.
- Standard section headings: "Summary", "Experience", "Education", "Skills".
  Parsers key off these exact words.
- Real text, never text-in-images. Never put contact details only in a logo or
  graphic.
- Dates in a consistent format, right-aligned or after the role.
- Standard fonts embedded in the PDF (the LaTeX build handles this).
- Save/export as PDF with a selectable text layer (Tectonic output is fine).

## 5. Honesty guardrail

Tailoring means emphasis and wording, not invention. Only surface, reorder, and
rephrase experience that already exists in `cv_master.tex`. If the job needs a
skill the candidate lacks, tell the user rather than fabricating it.

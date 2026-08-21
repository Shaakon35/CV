---
name: ats-score
description: Score a tailored CV (or cover letter) against a specific job offer before submitting. Reports a keyword-match score out of 100, which required keywords are covered vs missing, readability stats, and AI-filler words to remove. Use when the user asks to check, score, grade, or evaluate a CV/resume against a job, or asks how well their CV matches a posting, or before submitting an application. Triggers on "ATS score", "score my CV", "check my CV against this job", "how well does my CV match", "ATS check", "keyword match", "grade my resume", "is my CV good for this job".
---

# ATS Score

Estimate how an applicant tracking system would rank a CV against a job offer,
and surface concrete fixes before the user submits.

This is a heuristic aid, not a real ATS. Use it to catch missing keywords, AI
filler, and readability problems - then improve the CV and re-score.

## Inputs
- A CV or cover letter (PDF or `.tex`).
- The job offer text. Reuse `<year>/<company-role>/job-offer.txt` saved by the
  `tailor-cv` skill when available.

## Workflow

### 1. Get plain text of the CV
The scorer reads the same text an ATS parses. Extract it from the PDF:
```
pdftotext <year>/<company-role>/cv.pdf /tmp/cv.txt
```
(For a `.tex`, either build the PDF first or strip commands; PDF text is
preferred because it is exactly what the ATS sees.)

### 2. Run the scorer
```
python3 .ona/skills/ats-score/scripts/ats_score.py \
  --cv /tmp/cv.txt \
  --offer <year>/<company-role>/job-offer.txt
```

### 3. Read the report and act
The report gives:
- **Keyword match score / 100** and covered vs missing keywords.
- **Missing keywords** - add the ones the candidate legitimately has to the CV
  (summary, skills, most-recent role). Never fabricate to raise the score.
- **Readability** - flags overly long or uniform sentences (uniform length reads
  as AI-generated).
- **AI-filler words** - remove every one it lists.

### 4. Improve and re-score
Hand missing keywords and filler findings to the `tailor-cv` (or `cover-letter`)
skill to revise, then re-run the scorer. Aim for a keyword score of 70+ while
keeping the writing honest and human.

## Interpreting the score
- 70-100: strong keyword coverage.
- 40-69: several relevant keywords missing; revise before submitting.
- 0-39: weak match - either the CV needs tailoring or the role is a poor fit.

## Caveats
- `pdftotext` splits a CV into short lines, so sentence-length readability stats
  are approximate for bullet-heavy CVs. Treat them as directional.
- Keyword extraction is frequency-based; always sanity-check the missing list and
  ignore noise words (e.g. "looking", "focus").

## Definition of done
- Report generated against the correct job offer.
- Missing legitimate keywords and all AI-filler words were surfaced to the user.
- If revised, the CV was re-scored to confirm improvement.

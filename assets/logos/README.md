# Logos

Drop logo image files here. The CV references them by exact basename and shows a
plain-text fallback if a file is missing, so the CV always builds.

Prefer **PNG** (transparent background) or **PDF**. Recommended height ~40-80 px;
they are scaled down automatically.

## Required filenames

Header links (small, next to contact info):

| File          | Used for                    |
|---------------|-----------------------------|
| `gmail.png`   | email link                  |
| `linkedin.png`| LinkedIn link               |
| `github.png`  | GitHub link                 |

Company logos (next to role titles):

| File          | Used for                    |
|---------------|-----------------------------|
| `roche.png`   | F. Hoffmann-La Roche roles  |
| `anca.png`    | aNCA Product Owner role      |
| `novartis.png`| Novartis role               |
| `cofidis.png` | COFIDIS role                |
| `sanofi.png`  | Sanofi roles                |

## How to add them

Drag the image files into this folder in the VS Code editor, using the exact
names above, then rebuild:

```
tectonic cv_master.tex
```

Note: logos are images, so they are ATS-safe - they add nothing to the PDF text
layer that Workday parses.

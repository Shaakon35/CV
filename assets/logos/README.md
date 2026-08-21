# Logos

All logos below are already downloaded and committed (header icons from Simple
Icons; company wordmarks from Wikimedia Commons; aNCA hex from the pharmaverse
repo). The CV references them by exact basename and shows a plain-text fallback
if a file is ever missing, so the CV always builds.

## Portrait photo

The header shows a portrait if `assets/photo.jpg` (or `assets/photo.png`) exists.
Drop your photo there and rebuild; the header switches to a two-column layout
(text left, photo top-right). A photo never affects the ATS text layer because
it is an image.

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

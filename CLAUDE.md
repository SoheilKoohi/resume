# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single-source-of-truth resume. `Soheil_Koohi_CV.yaml` is the only hand-edited
content file; the PDF, HTML, Markdown, PNG and Typst outputs are all generated
from it by [RenderCV](https://rendercv.com) and are gitignored.

**Never edit anything in `rendercv_output/` or `site/`.** Those directories are
build artifacts and are overwritten on every build. Changes to resume content
always go into the YAML.

## Commands

```bash
make install   # one-time: uv tool install --python 3.12 "rendercv[full]==2.8"
make build     # render + assemble site/  (same script CI runs)
make open      # build, then open the PDF (macOS)
make watch     # re-render on every save of the YAML
make clean     # rm -rf rendercv_output site
```

`make build` just calls `./scripts/build.sh`, which is deliberately shared by
the Makefile and by GitHub Actions so local and CI output cannot drift. The
script picks `rendercv` off `PATH` if present, otherwise falls back to
`uvx --from "rendercv[full]==2.8"`.

There are no tests or linters. Verification is visual and mechanical — see below.

## Build pipeline

```
Soheil_Koohi_CV.yaml
  ├─ rendercv render      → rendercv_output/{pdf,html,md,typ,*.png}
  └─ scripts/build_site.py → site/index.html   (custom landing page)
       scripts/build.sh assembles site/:
         ├─ index.html          generated from the YAML, not RenderCV's HTML
         ├─ profile.jpg         copied from images/profile-square.jpg
         └─ Soheil_Koohi_CV.pdf, .md
```

`scripts/build_site.py` reads the same YAML the PDF is built from, so the page
and the PDF cannot drift. Every string on the page comes from the YAML; only
layout and the readout-strip labels live in the script. It needs **PyYAML** —
`build.sh` uses the system `python3` when it has it, otherwise falls back to
`uv run --with pyyaml`, and CI installs it alongside RenderCV.

The readout strip near the top of the page is curated, not scraped: the four
cells in `READOUTS` state scope (years, serving load, team size, roadmap areas)
because no single CV bullet says those things on its own. Each cell carries an
`evidence` regex naming the CV phrase it rests on, and the build prints a warning
to stderr when one stops matching — so edit the YAML freely, but read the build
output. Consecutive roles at the same employer are grouped into one block, so a
promotion reads as a promotion.

`.github/workflows/render.yml` runs on push to `main`: builds, uploads
`rendercv_output/` as a workflow artifact named `resume`, and deploys `site/`
to GitHub Pages. Pull requests build and upload but do not deploy.

## YAML structure notes

Section render order follows key order under `cv.sections`, currently
`summary → experience → education → skills`. Skills was tried above experience
(the tech-resume convention) and reverted: RenderCV never splits an entry
across a page boundary, so moving it left a quarter-page hole at the end of
page 1.

Non-obvious settings at the bottom of the file, each added to fix a real defect:

- `design.typography.alignment: justified-with-no-hyphenation` — the default
  justified text hyphenated words across line breaks, so `Identification` and
  `availability` did not exist in the extracted PDF text. Do not remove this.
- `design.page.show_top_note: false` — hides the "Last updated in <Month Year>" line.
- `design.header.connections.phone_number_format: international` — without it
  the phone renders as `0936 721 6152`, dropping the country code.
- `design.page.*_margin` — 1.2cm top/bottom, 1.6cm left/right. These are what
  hold the CV to two pages; widening them overflows to three.
- `locale.language: english` plus an explicit `month_abbreviations` list — the
  RenderCV default mixes 3- and 4-letter abbreviations (`Mar` next to `Sept`).
  Note the key is `english`, not `en`.

## Editing the resume

Content constraints that have been enforced so far, worth preserving:

- **Two pages, no mid-document white gap.** After any content change, rebuild
  and check `rendercv_output/Soheil_Koohi_CV_*.png`. Because entries never
  split across pages, removing a few lines can push a whole role onto the next
  page and leave a visible hole — check page bottoms, not just the page count.
- Bullets carry a metric wherever a defensible one exists. Do not invent
  numbers; ask.
- Filler words (`successfully`, `highly`, `utilizing`, `leveraging`) have been
  stripped; do not reintroduce them.
- Opening verbs are deliberately varied — check for repetition after edits.

## Auditing

`.claude/skills/` holds 23 vendored resume and job-search skills (see
`.claude/skills/README.md` for sources and MIT licenses). The ones used on this
repo are `resume-ats-optimizer`, `resume-bullet-writer`, `resume-quantifier`
and `resume-formatter`.

They all read resumes as **Markdown**, so feed them
`rendercv_output/Soheil_Koohi_CV.md` and apply accepted wording back into the
YAML.

Mechanical checks worth re-running after content changes (no tooling is
committed for these; they were run ad hoc with `uvx --from pypdf`):

- PDF text extraction — confirms sections and contact details parse, and that
  no word is split by an invented hyphen at a line break.
- Keyword coverage against a Staff/Principal ML keyword set.
- Filler-word and repeated-opening-verb counts.
- `uvx codespell` over the generated Markdown (`ALS` is a known false positive).

## Conventions

- The filename says `CV`, not `Resume`, which is correct for the UK/EU market
  being targeted. Rename only if switching to US applications.
- Dates are month-level (`2023-12`) and render as `Dec 2023`.

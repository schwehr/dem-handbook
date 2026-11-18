# The Digital Elevation Models Handbook

A comprehensive, practitioner-grade reference on elevation data on land and
under water (bathymetry), with a sustained emphasis on validation, correctness,
error, and uncertainty.

## Status (2026-11-14)

**Full edition drafted, audited, and fact-checked.** All 73 chapters and 9 appendices
(82 files) exist, match the chapter template in `STYLE_GUIDE.md`, and have passed
a three-model verification and Crossref DOI pass alongside structural, summary,
and cross-reference checks (`tools/check_book.py`: 82/82 files present, 0 hard
failures; `tools/check_summary.py`: 0 mismatches; `tools/check_xrefs.py`: 0
issues; `tools/check_facts.py`: 0 hard failures, 0 unresolved `(verify)` flags).
Figures are still placeholders.

| Item | Value |
|---|---|
| Chapters | 73 files, 581,439 words (`wc -w chapters/*.md`) |
| Appendices | 9 files (A–I), 45,837 words (`wc -w appendices/*.md`) |
| Total | 82 files, 627,276 words |
| Figure placeholders (`<!-- figure: … -->`) | 187 |
| Remaining `(verify)` flags | 0 across all 73 chapters and 9 appendices (`check_facts.py`) |
| Chapters over 8,500 words | 19 (see below) |

## How to navigate

- [`SUMMARY.md`](SUMMARY.md) — the reading order: every chapter and appendix
  with its title, grouped by Part (mdBook/Jupyter-Book style; titles match each
  file's H1).
- [`TABLE_OF_CONTENTS.md`](TABLE_OF_CONTENTS.md) — the detailed specification
  each chapter was written against: 16 parts, 73 chapters, 9 appendices. Each
  chapter block carries the same slots: Scope · Sections · Then & now · Math
  (where relevant) · Software (open / closed) · Standards & guides · Key
  references · Pitfalls · Key takeaways.
- [`STYLE_GUIDE.md`](STYLE_GUIDE.md) — chapter template, recurring boxes,
  honesty rules, and the fixed file manifest (the only valid cross-link targets).
- `chapters/chNN-slug.md` and `appendices/appendix-x-slug.md` — the text.
  Chapter numbers (1–73) are continuous and are the stable cross-reference keys.
- Start with Chapter 3 (fitness for use), Chapter 5 (error and uncertainty),
  and Chapter 53 (accuracy assessment) if you only read three chapters.

## Checking the book

```bash
python3 tools/check_book.py            # per-file table + summary; exit 1 on hard failure
python3 tools/check_book.py --quiet    # summary only
python3 tools/check_summary.py         # SUMMARY.md vs file H1s and TOC Part headings
python3 tools/check_xrefs.py           # [Chapter N](chNN-…) link-number agreement; title spot-check
python3 tools/check_facts.py --check-dois --check-history --quiet  # DOIs, (verify), and ⟨H⟩ years
```

`check_book.py` verifies that every manifest file exists, that the template
headings are present and in order, counts sections/boxes/figures/references,
flags chapters outside the 4,500–7,000-word target ("long" warns above
8,500), and resolves every relative Markdown link. Columns: P = numbered
sections, K = key takeaways, R = references, B = boxes, F = figure
placeholders. `check_xrefs.py` reports 0 issues across all 82 files.

### Chapters currently over 8,500 words

ch01, ch04, ch05, ch06, ch07, ch09, ch10, ch12, ch21, ch55, ch56, ch57, ch58,
ch59, ch60, ch63, ch65, ch66, ch67 (19 chapters; the longest is ch59 at 9,947 words).
They are complete and reviewed; trimming is an editorial choice, not a defect.

## Conventions

- ⟨H⟩ marks history items taken from <https://github.com/schwehr/gis-history>;
  ⟨+⟩ marks timeline entries added for this book (Appendix C).
- **"(verify)"** originally marked 106 citations, edition numbers, DOIs, or
  product figures requiring primary-source confirmation; all 106 flags across
  the 73 chapters and 9 appendices were resolved during the three-model
  bibliography, standards, and product verification pass (`0` remaining).
- Agreed values for recurring facts (harmonised across the handbook): Seabed 2030
  mapped fraction 26.1 % at GEBCO_2024 / 27.3 % at GEBCO_2025 / 28.7 % at
  GEBCO_2026 (Apr 2026; ≈ 6 % in 2017); IHO S-44 Ed. 6.1.0 (2022), S-100 Ed.
  5.2.0 (Jul 2024), S-102 Ed. 3.0.0 (Dec 2024; Ed. 3.1.0 in development),
  S-158:102 (Ed. 1.0.0, Dec 2025), S-4 Ed. 4.10.0, C-51, B-12 Ed. 3.0.0 (2023),
  and B-13 Ed. 1.0.0 (Mar 2024); NOAA HSSD 2024 and FPM (Apr 2014 PDF; 2020+
  online); USGS Lidar Base Specification 2024 rev. A (Jan 2024) / 2025 rev. A
  (Jun 2025); LAS 1.4 R14 (Mar 2019, classes 19–22) / R15 (Jul 2019, current); ASPRS Positional Accuracy Standards
  Ed. 2 (2023; v2 Jun 2024) report RMSE_V/RMSE_H with NVA/VVA kept as strata
  (1.96×RMSE and 95th-percentile VVA are Ed. 1 / pre-2024 LBS statistics); NGS
  modernized NSRS (NATRF2022/NAPGD2022/GEOID2022) Sept 2026 final public beta
  ahead of targeted 2027 FGCS adoption; Bielski et al. 2024 is *IEEE TGRS*
  62:4503922.

## Known limitations / next steps

1. **Figures.** All 187 figures are `<!-- figure: … -->` placeholders with
   captions; none has been drawn.
2. **Verification status.** The three-model Hydrogen/Argon/Carbon audit and
   Crossref DOI pass resolved all 106 original "(verify)" flags, confirmed DOIs,
   and checked editions in Appendix D against IHO/ASPRS/OGC/USGS/NOAA registries;
   keep a BibTeX export synchronized if generating print builds.
3. **Long chapters.** Nineteen chapters exceed 8,500 words (list above);
   decide whether to split, trim, or accept.
4. **Appendix J (learning pathways / certification)** was deferred — see the
   open decisions in Appendix I (gap review), which also lists the remaining
   coverage gaps and the slim-edition merge plan.
5. **Build.** Generate a book scaffold (mdBook `SUMMARY.md` is already in
   place; a Jupyter Book `_toc.yml` can be derived from it) and render the
   LaTeX and GFM tables to confirm they typeset.
6. **Currency.** Product tables (Appendix E) and standards (Appendix D) are
   verified as of 2026-11; re-check on each revision (e.g., GEBCO annual
   releases, S-102 3.1.0, official 2027 NSRS adoption).

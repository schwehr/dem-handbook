# The Digital Elevation Models Handbook

A comprehensive, practitioner-grade reference on elevation data on land and
under water (bathymetry), with a sustained emphasis on validation, correctness,
error, and uncertainty.

## Status (2026-10-03)

**Full edition drafted and reviewed.** All 73 chapters and 9 appendices
(82 files) exist, have been written to the chapter template in
`STYLE_GUIDE.md`, and have passed an independent review pass plus a final
consistency sweep (`tools/check_book.py`: 82/82 files present, 0 hard
failures, 0 broken cross-links). Figures are still placeholders.

| Item | Value |
|---|---|
| Chapters | 73 files, 571,805 words (`wc -w chapters/*.md`) |
| Appendices | 9 files (A–I), 44,944 words (`wc -w appendices/*.md`) |
| Total | 82 files, 616,749 words |
| Figure placeholders (`<!-- figure: … -->`) | 186 |
| Remaining `(verify)` flags | 106 (see below) |
| Chapters over 8,500 words | 17 (see below) |

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
```

`check_book.py` verifies that every manifest file exists, that the template
headings are present and in order, counts sections/boxes/figures/references,
flags chapters outside the 4,500–7,000-word target ("long" warns above
8,500), and resolves every relative Markdown link. Columns: P = numbered
sections, K = key takeaways, R = references, B = boxes, F = figure
placeholders. `check_xrefs.py` reports a handful of false positives where
prose follows "Chapter N —"; those have been inspected.

### Chapters currently over 8,500 words

ch01, ch04, ch05, ch06, ch07, ch10, ch12, ch21, ch55, ch56, ch57, ch58, ch59,
ch60, ch65, ch66, ch67 (17 chapters; the longest is ch59 at ≈ 9,900 words).
They are complete and reviewed; trimming is an editorial choice, not a defect.

## Conventions

- ⟨H⟩ marks history items taken from <https://github.com/schwehr/gis-history>;
  ⟨+⟩ marks timeline entries added for this book (Appendix C).
- **"(verify)"** flags a citation, edition number, DOI, or product figure that
  the author could not confirm against a primary source at writing time; the
  statement is believed correct but must be checked in the bibliography pass
  before publication. There are 106 flags, concentrated in Appendix D
  (standards index, 22), Appendix E (product tables, 18), and Appendix H
  (datasets, 10); 47 of the 73 chapters carry none.
- Agreed values for recurring facts (harmonised in the final sweep): Seabed 2030
  mapped fraction 26.1 % at GEBCO_2024 / 27.3 % at GEBCO_2025 (≈ 6 % in 2017);
  IHO S-44 Ed. 6.1.0 (2022); S-102 Ed. 3.0.0 (Dec 2024); NOAA HSSD 2024;
  LAS 1.4 R14 (Mar 2019, classes 19–22) / R15 (Jul 2019, current); ASPRS
  Positional Accuracy Standards Ed. 2 (2023; v2 2024) report RMSE_V/RMSE_H with
  NVA/VVA kept only as strata (1.96×RMSE and 95th-percentile VVA are Ed. 1 /
  pre-2024 LBS statistics); NAPGD2022 adoption pending (beta 2026); IHO B-12
  Ed. 3.0.0 (2023); IHO B-13 Ed. 1.0.0 (Mar 2024); Bielski et al. 2024 is
  *IEEE TGRS* 62:4503922.

## Known limitations / next steps

1. **Figures.** All 186 figures are `<!-- figure: … -->` placeholders with
   captions; none has been drawn.
2. **Bibliography pass.** Resolve the 106 "(verify)" flags; expand "References"
   into BibTeX with DOIs; confirm editions in Appendix D against the IHO/ASPRS/
   OGC registries.
3. **Long chapters.** Seventeen chapters exceed 8,500 words (list above);
   decide whether to split, trim, or accept.
4. **Appendix J (learning pathways / certification)** was deferred — see the
   open decisions in Appendix I (gap review), which also lists the remaining
   coverage gaps and the slim-edition merge plan.
5. **Build.** Generate a book scaffold (mdBook `SUMMARY.md` is already in
   place; a Jupyter Book `_toc.yml` can be derived from it) and render the
   LaTeX and GFM tables to confirm they typeset.
6. **Currency.** Product tables (Appendix E) and standards (Appendix D) are
   dated 2026-10; re-check on each revision (e.g., GEBCO annual releases,
   S-102 3.1.0, NSRS modernisation).

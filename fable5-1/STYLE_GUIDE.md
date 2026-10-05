# Style guide and file manifest — The Digital Elevation Models Handbook (full edition)

This document is the contract for every chapter and appendix file. Writers (human or
agent) must follow it so that the 73 chapters read as one book.

## 1. Files and naming

- Chapters live in `chapters/`, appendices in `appendices/`. Names are fixed (see §8);
  never rename a file — cross-links depend on them.
- One chapter per file, GitHub-flavored Markdown, UTF-8, LF line endings, no HTML
  except `<!-- figure: ... -->` placeholders.
- Target length: **4,500–7,000 words per chapter** (domain deep dives and sensor
  chapters toward the top; short chapters such as 28 or 37 toward the bottom).
  Appendices: as long as their content needs (glossary ≥ 250 terms; timeline ≥ 200
  entries; checklists complete).

## 2. Chapter template (use exactly these top-level headings, in this order)

```markdown
# Chapter N — Title

> **Part X — Part title.** One-sentence placement of the chapter in the book.

**In this chapter.** 120–180-word abstract: what the reader will be able to do.

## N.1 First section title
...numbered sections following the TOC block (you may split, merge, or add
subsections, but keep the TOC's substance; use `### N.1.1` for subsections)...

## Then & now
How the systems/processes in this chapter changed over time. Keep the ⟨H⟩ tag on
items that come from https://github.com/schwehr/gis-history.

## Mathematics            ← include only when the TOC block has a Math line
Derivations and formulas with notation defined; LaTeX ($...$ inline, $$...$$ display).

## Validation & uncertainty          ← MANDATORY in every chapter
How errors arise in this chapter's subject, how they propagate, how to test for them,
what to report. This is the book's spine; make it concrete (procedures, numbers,
statistics, worked example).

## Software
**Open source:** ... **Free but closed:** ... **Commercial:** ... (name, what it does
for this chapter, one caveat each where relevant).

## Standards & guides
Bulleted list with issuer, edition/year, and what it governs for this chapter.

## Pitfalls
8–15 bullets. Each bullet: the mistake → why it happens → how to detect/avoid it.

## Key takeaways
6–10 bullets; crisp, actionable.

## References
Full citations (authors, year, title, venue/publisher, volume(issue):pages). Add a
DOI **only if you are confident it is correct**; otherwise omit the DOI. Mark any
citation you could not confirm with "(verify)". Never invent papers.
```

## 3. Recurring boxes (blockquotes with a bold label)

Use these consistently; 2–6 boxes per chapter:

- `> **Uncertainty budget.** ...` — a table or list of error components with magnitudes.
- `> **Definitions that bite.** ...` — a term whose varying definitions cause errors.
- `> **Case file.** ...` — a short real incident (sourced) illustrating the point.
- `> **Try it.** ...` — a runnable snippet (PDAL/GDAL/GMT CLI, Python, or R) in a
  fenced code block, with the expected outcome stated. Prefer open-source tools.
- `> **Worked example.** ...` — numeric example with the arithmetic shown.
- `> **Rule of thumb.** ...` — a heuristic with its limits of validity.

## 4. Writing rules

- Audience: practitioners and graduate students across surveying, hydrography,
  remote sensing, GIS, geoscience, robotics, and software. Assume numeracy, not
  domain jargon; define terms on first use (and bold them).
- Voice: direct, concrete, second person acceptable ("check the vertical datum").
  No marketing language. Prefer numbers with units and sources over adjectives.
- **Honesty.** Do not fabricate statistics, dates, product specs, or citations. If a
  figure is approximate, say "approximately" and cite. If unsure, write "(verify)".
  It is better to omit a number than to invent one.
- Every chapter must explicitly connect to validation/uncertainty (the mandatory
  section) and must end with Pitfalls → Key takeaways → References.
- Cross-reference other chapters as Markdown links using the manifest in §8, e.g.
  `[Chapter 9](ch09-vertical-datums.md)` from within `chapters/`, or
  `[Appendix B](../appendices/appendix-b-math-reference.md)`. From `appendices/`,
  link chapters as `../chapters/chNN-....md`.
- Units: SI; give imperial in parentheses only where a standard uses it. Use
  "m", "cm", "mm", "km", "nmi" (nautical mile), "kn" (knot). Use "″" for arc seconds.
- Notation: σ for standard deviation, RMSE for root-mean-square error, 95 % with a
  space, LE95/CE95, "1σ". Use "DEM" as the generic term, "DSM"/"DTM" when specific.
  Height types: h (ellipsoidal), H (orthometric), N (geoid undulation): h = H + N.
- Dates: ISO style in tables (2000-02), prose style in text (February 2000).
- Figures: do not draw; insert `<!-- figure: Figure N.k — description of what the
  figure should show -->` where a figure belongs (2–6 per chapter).
- Tables: GFM pipe tables; keep ≤ 8 columns.
- Code: fenced blocks with language tags (`bash`, `python`, `r`, `json`).
- Avoid duplicating another chapter: summarize in one paragraph and link to it.
- Keep the ⟨H⟩ tag convention for gis-history items in "Then & now".
- Length control: write each chapter in 2–4 appends to avoid output truncation;
  after finishing, run `wc -w` and confirm the word count is within target.

## 5. Source constraints for agent writers

- You may read anything inside `dem-handbook/`
  and public web resources. **Do not read files anywhere else on this machine.**
- The authoritative specification for each chapter is its block in
  `TABLE_OF_CONTENTS.md` (`### Chapter N — ...`). Cover every bullet in that block's
  "Sections" list, and use its Then & now / Math / Software / Standards /
  References / Pitfalls / Key takeaways lines as the minimum content.
- Use the web to confirm facts, editions, and citations where practical.

## 6. Quality bar (self-check before reporting done)

- [ ] All template headings present and in order; "Validation & uncertainty" present.
- [ ] Every TOC "Sections" bullet is covered.
- [ ] ≥ 2 boxes, ≥ 1 worked example or Try-it, ≥ 2 figure placeholders.
- [ ] Pitfalls 8–15, Key takeaways 6–10, References ≥ 12 (≥ 20 for sensor/validation chapters).
- [ ] No invented numbers/citations; "(verify)" used where appropriate.
- [ ] Cross-links use manifest filenames.
- [ ] Word count within target (`wc -w`).

## 7. Part titles

I Why elevation? Uses and users · II Vocabulary and the foundations of correctness ·
III Where is "here"? Geodesy, datums, projections · IV Positioning and orientation ·
V Sensors and platforms · VI Planning and operating surveys · VII From sensor data to
products · VIII The dynamic Earth · IX Semantics, learning, and enhancement · X
Representing, storing, finding, and keeping elevation data · XI Validation, quality,
and judging data · XII Visualization and cartography · XIII Vectors, grids, and
location codes · XIV Domain deep dives · XV Law, policy, security, privacy, ethics ·
XVI Standards, software, and history

## 8. File manifest (fixed)

| # | File | Title |
|---|---|---|
| 1 | chapters/ch01-uses-on-land.md | The many uses of elevation data on land |
| 2 | chapters/ch02-uses-bathymetry.md | The many uses of bathymetry and topobathymetry |
| 3 | chapters/ch03-fitness-for-use.md | From use to requirement: fitness for use, constraints, and appropriate resolution |
| 4 | chapters/ch04-names-and-definitions.md | Names and definitions: DEM, DSM, DTM, and the words that bite |
| 5 | chapters/ch05-error-and-uncertainty.md | Error, uncertainty, accuracy, precision, resolution — the statistical toolkit |
| 6 | chapters/ch06-time-as-coordinate.md | Time as a coordinate: epochs, clocks, synchronization |
| 7 | chapters/ch07-shape-of-the-earth.md | The shape of the Earth: ellipsoid, geoid, gravity, heights |
| 8 | chapters/ch08-horizontal-datums.md | Horizontal datums and terrestrial reference frames |
| 9 | chapters/ch09-vertical-datums.md | Vertical datums: orthometric, ellipsoidal, tidal, and home-made |
| 10 | chapters/ch10-projections-and-resampling.md | Map projections, grids, and the resampling they force |
| 11 | chapters/ch11-history-of-positioning.md | A history of positioning: from plumb bobs to PPP |
| 12 | chapters/ch12-gnss.md | GNSS for elevation work |
| 13 | chapters/ch13-imu-ins.md | IMU/INS, motion sensing, and GNSS-aided navigation |
| 14 | chapters/ch14-positioning-beyond-gnss.md | Positioning without (or beyond) GNSS: acoustic, terrain-aided, radio, barometric |
| 15 | chapters/ch15-slam.md | SLAM: solving the map and the trajectory together (and mapping innerspace) |
| 16 | chapters/ch16-platforms.md | Platforms: feet, cars, boats, drones, kites, aircraft, satellites, fixed infrastructure |
| 17 | chapters/ch17-measurement-physics.md | Measurement physics: a unified view (ranging, parallax, interferometry, inversion) |
| 18 | chapters/ch18-topographic-lidar.md | Topographic lidar |
| 19 | chapters/ch19-bathymetric-lidar.md | Bathymetric lidar and the land–water transition |
| 20 | chapters/ch20-sonar.md | Sonar: the many types and how they make bathymetry |
| 21 | chapters/ch21-radar-sar-insar.md | Radar, SAR, InSAR, radar altimetry, and ice-penetrating radar |
| 22 | chapters/ch22-photogrammetry-sfm.md | Photogrammetry, stereo, and structure from motion |
| 23 | chapters/ch23-satellite-derived-bathymetry.md | Optical satellite-derived bathymetry, wave-kinematics bathymetry, altimetry-predicted bathymetry |
| 24 | chapters/ch24-gravity-magnetics-geophysics.md | Gravity, magnetics, and other geophysics as mapping aids |
| 25 | chapters/ch25-calibration-infrastructure.md | Calibration: targets, stations, networks, benchmarks, reference surfaces |
| 26 | chapters/ch26-survey-planning.md | Survey planning for calibration, error reduction, and error monitoring |
| 27 | chapters/ch27-moving-and-transient-objects.md | Moving and transient objects during collection (cars, ships, cranes, smoke, steam; AIS/ADS-B) |
| 28 | chapters/ch28-reducing-cost.md | Reducing cost across collection, processing, validation, and use |
| 29 | chapters/ch29-processing-pipelines.md | Processing pipelines: levels, lineage, and what gets lost |
| 30 | chapters/ch30-point-cloud-classification.md | Point-cloud cleaning, classification, and ground extraction |
| 31 | chapters/ch31-interpolation-and-gridding.md | Interpolation, gridding, and grid registration |
| 32 | chapters/ch32-dsm-to-dtm.md | DSM → DTM: removing objects, and the definitions problem (buildings, roads, bridges, pipes, panels) |
| 33 | chapters/ch33-wires-and-thin-structures.md | Wires, power lines, antennas, and other thin or moving structures |
| 34 | chapters/ch34-water-in-dems.md | Water in DEMs: surfaces, shorelines, hydro-flattening / -enforcement / -conditioning |
| 35 | chapters/ch35-voids-and-overhangs.md | Voids, occlusion, shadows, overhangs, and multi-valued surfaces |
| 36 | chapters/ch36-seasonal-variability.md | Seasonal and environmental variability (leaves, snow, groundwater, crops, steam, tides) |
| 37 | chapters/ch37-time-scales-of-change.md | Time scales of surface change |
| 38 | chapters/ch38-plate-motion-and-vlm.md | Plate motion, reference-frame dynamics, and vertical land motion |
| 39 | chapters/ch39-earthquakes-volcanoes-landslides.md | Earthquakes, volcanoes, landslides: sudden deformation and its datum consequences |
| 40 | chapters/ch40-erosion-and-geomorphic-change.md | Erosion, deposition, and geomorphic change |
| 41 | chapters/ch41-change-detection.md | Change detection methods and the minimum detectable change |
| 42 | chapters/ch42-object-detection-semantics.md | Object detection and semantic labelling of the surface |
| 43 | chapters/ch43-traditional-vs-ml.md | Traditional versus machine-learning methods: a cross-cutting assessment |
| 44 | chapters/ch44-resolution-and-sampling.md | Resolution, pixel size, sampling, and oversampling |
| 45 | chapters/ch45-super-resolution.md | Super-resolution and DEM enhancement |
| 46 | chapters/ch46-data-models.md | Data models: points, waveforms, grids, TINs, meshes, voxels, variable resolution, overviews, splats |
| 47 | chapters/ch47-file-formats.md | File formats: LAS/LAZ/COPC, GeoTIFF/COG, BAG/S-102, NetCDF/Zarr, DTED, and the rest |
| 48 | chapters/ch48-compositing.md | Compositing: merging many datasets into one product |
| 49 | chapters/ch49-metadata.md | Metadata |
| 50 | chapters/ch50-archiving-and-provenance.md | Archiving, versioning, and provenance |
| 51 | chapters/ch51-finding-data.md | Finding the right data: catalogs, STAC, and search |
| 52 | chapters/ch52-ground-truth.md | Ground truth and calibration/validation datasets |
| 53 | chapters/ch53-accuracy-assessment.md | Accuracy assessment and uncertainty quantification in practice |
| 54 | chapters/ch54-evaluating-others-data.md | Evaluating other people's data when you lack the full story |
| 55 | chapters/ch55-public-products.md | Public DEM and bathymetry products: catalog and comparison |
| 56 | chapters/ch56-case-files.md | Case files: failures, surprises, and lessons |
| 57 | chapters/ch57-visualizing-dems.md | Visualizing DEMs: shading, colormaps, filtering, rendering, point clouds, splats |
| 58 | chapters/ch58-making-maps.md | Making maps from elevation: topographic maps, charts, graticules, standard elements |
| 59 | chapters/ch59-vector-data.md | Vector data and DEMs: points, lines, polygons, breaklines, contours, topology |
| 60 | chapters/ch60-dggs-and-location-codes.md | Discrete global grids and location codes: S2, H3, geohash, plus codes, what3words, MGRS |
| 61 | chapters/ch61-hydrology.md | Hydrologic and hydraulic modeling constraints |
| 62 | chapters/ch62-navigation-and-charting.md | Navigation and charting from elevation: marine, aviation, drones, vehicles, robots |
| 63 | chapters/ch63-buildings-cities-innerspace.md | Buildings, cities, and innerspace |
| 64 | chapters/ch64-agriculture-forests-wetlands.md | Agriculture, forests, wetlands, and the living surface |
| 65 | chapters/ch65-mining-landfills-earthworks.md | Mining, landfills, construction, and engineered earthworks |
| 66 | chapters/ch66-coastal-marine-polar-lakes-rivers.md | Coastal, marine, polar, lakes and rivers |
| 67 | chapters/ch67-planetary-dems.md | Planetary DEMs: mapping without ground truth |
| 68 | chapters/ch68-legal-issues.md | Legal issues |
| 69 | chapters/ch69-security-sovereignty-privacy-ethics.md | National security, sovereignty, privacy, and ethics |
| 70 | chapters/ch70-specifications-guided-tour.md | Survey and product specifications: a guided tour (S-44, HSSD, FPM, LBS, ASPRS, ICAO, INSPIRE…) |
| 71 | chapters/ch71-software-landscape.md | Software landscape: open-source and closed-source by task |
| 72 | chapters/ch72-history.md | How we got here: a history of measuring the shape of the Earth |
| 73 | chapters/ch73-open-problems.md | Open problems and the next decade |
| A | appendices/appendix-a-glossary.md | Glossary |
| B | appendices/appendix-b-math-reference.md | Mathematical reference |
| C | appendices/appendix-c-timeline.md | Timeline (seeded from gis-history) |
| D | appendices/appendix-d-standards-index.md | Standards and guide documents index |
| E | appendices/appendix-e-public-products-tables.md | Public products comparison tables |
| F | appendices/appendix-f-software-index.md | Software index |
| G | appendices/appendix-g-checklists.md | Checklists |
| H | appendices/appendix-h-datasets.md | Datasets for exercises and benchmarks |
| I | appendices/appendix-i-gap-review.md | Gap review — what else should be included, and what could be trimmed |

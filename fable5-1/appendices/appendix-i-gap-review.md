# Appendix I — Gap review: what else should be included, and what could be trimmed

This appendix is the editorial audit the brief asked for. It compares the handbook as drafted against the original topic list, records what was added beyond that list and why, identifies chapters that run long and sections that duplicate one another, and lists decisions that a second edition should take deliberately rather than inherit. It was written against the draft state of the `chapters/` directory at the time of the appendix pass (all 73 chapter files present; Appendices A–D were being written concurrently), so section numbers cited here should be re-checked after final copy-editing.

The method was simple: read the TOC's final "Review" block and the user topic list it reflects; grep every `## N.k` heading in `chapters/`; sample the Validation & uncertainty sections and the boxes; count words. Where a topic is covered only in passing, the table says so rather than claiming coverage.

## I.1 Coverage of the original request

The original request enumerated roughly sixty topics. The table maps each to the chapters that carry it. "Primary" is where a reader should start; "also" lists substantive secondary treatment (a section or more, not a mention). Items marked ◐ are covered but thinner than their neighbours; items marked ● are covered at chapter depth.

| Requested topic | Primary chapter(s) | Also | Depth |
|---|---|---|---|
| Uses of elevation data on land | [1](../chapters/ch01-uses-on-land.md) | 3, 61, 63–65 | ● |
| Uses of bathymetry / topobathymetry | [2](../chapters/ch02-uses-bathymetry.md) | 62, 66 | ● |
| Resolution → appropriateness; fitness for use | [3](../chapters/ch03-fitness-for-use.md), [44](../chapters/ch44-resolution-and-sampling.md) | 53, 54 | ● |
| Naming and definitions (DEM/DSM/DTM) | [4](../chapters/ch04-names-and-definitions.md) | 32, App. A | ● |
| Resolution, precision, accuracy, error | [5](../chapters/ch05-error-and-uncertainty.md), [53](../chapters/ch53-accuracy-assessment.md) | 44, App. B | ● |
| Geodesy, projections, datums | [7](../chapters/ch07-shape-of-the-earth.md)–[10](../chapters/ch10-projections-and-resampling.md) | 38 | ● |
| Vertical datums incl. home-made | [9](../chapters/ch09-vertical-datums.md) | 34, 62, 66, 68.2 | ● |
| History of positioning | [11](../chapters/ch11-history-of-positioning.md) | 72, App. C | ● |
| GNSS | [12](../chapters/ch12-gnss.md) | 25, 52 | ● (long) |
| IMU / INS | [13](../chapters/ch13-imu-ins.md) | 15, 18, 20 | ● |
| Positioning without GNSS (acoustic, terrain-aided, radio, barometric) | [14](../chapters/ch14-positioning-beyond-gnss.md) | 62.6 | ● |
| SLAM; innerspace | [15](../chapters/ch15-slam.md) | 63.5 | ● |
| Platforms: feet, cars, boats, drones, kites, aircraft, satellites, fixed infrastructure | [16](../chapters/ch16-platforms.md) | 27, 28 | ● |
| Lidar (topographic) and bathymetric lidar, differences | [18](../chapters/ch18-topographic-lidar.md), [19](../chapters/ch19-bathymetric-lidar.md) | 17, 34.8 | ● |
| Sonar types | [20](../chapters/ch20-sonar.md) | 17, 26, 30.6 | ● |
| Radar / SAR / InSAR | [21](../chapters/ch21-radar-sar-insar.md) | 38, 39, 41.4 | ● (long) |
| Photogrammetry, stereo, SfM | [22](../chapters/ch22-photogrammetry-sfm.md) | 67 | ● |
| Satellite-derived bathymetry | [23](../chapters/ch23-satellite-derived-bathymetry.md) | 66 | ● |
| Gravity, magnetics | [24](../chapters/ch24-gravity-magnetics-geophysics.md) | 7, 23.4 | ● |
| Calibration targets, CORS, benchmarks | [25](../chapters/ch25-calibration-infrastructure.md) | 12, 52 | ● |
| Survey planning for calibration / error reduction | [26](../chapters/ch26-survey-planning.md) | App. G.1–G.2 | ● |
| Moving objects (cars, ships, cranes, dumps, fires, steam); AIS/ADS-B | [27](../chapters/ch27-moving-and-transient-objects.md) | 33, 36, 62.8 | ● |
| Reducing cost | [28](../chapters/ch28-reducing-cost.md) | 26.9 | ● |
| Processing | [29](../chapters/ch29-processing-pipelines.md)–[31](../chapters/ch31-interpolation-and-gridding.md) | 48 | ● |
| DSM → DTM; building/road definitions; bridges, pipes | [32](../chapters/ch32-dsm-to-dtm.md) | 4, 63.3–63.4 | ● |
| Wires, power lines, antennas; time scales | [33](../chapters/ch33-wires-and-thin-structures.md) | 27, 37 | ● |
| Variable water; shoreline definition | [34](../chapters/ch34-water-in-dems.md) | 66, 68.1 | ● |
| Data gaps, shadows, overhangs | [35](../chapters/ch35-voids-and-overhangs.md) | 48.5 | ● |
| Seasonal variability (leaves, snow, groundwater, crops, steam, tides) | [36](../chapters/ch36-seasonal-variability.md) | 64 | ● |
| Time scales of change; temporal variability | [37](../chapters/ch37-time-scales-of-change.md), [6](../chapters/ch06-time-as-coordinate.md) | 38–41 | ● |
| Plate motion | [38](../chapters/ch38-plate-motion-and-vlm.md) | 8 | ● |
| Earthquakes (and volcanoes, landslides) | [39](../chapters/ch39-earthquakes-volcanoes-landslides.md) | 56.4–56.5, 56.10 | ● |
| Erosion | [40](../chapters/ch40-erosion-and-geomorphic-change.md) | 66 | ● |
| Change detection | [41](../chapters/ch41-change-detection.md) | App. G (change items folded into G.8/G.9) | ● |
| Object detection / semantics | [42](../chapters/ch42-object-detection-semantics.md) | 63 | ● |
| Traditional vs ML | [43](../chapters/ch43-traditional-vs-ml.md) | 45 | ● |
| Oversampling; super-resolution | [44](../chapters/ch44-resolution-and-sampling.md), [45](../chapters/ch45-super-resolution.md) | — | ● |
| Point clouds, waveforms, grids, TINs, variable resolution, overviews | [46](../chapters/ch46-data-models.md) | 31.7 | ● |
| Formats: LAS, BAG, GeoTIFF | [47](../chapters/ch47-file-formats.md) | 46 | ● |
| Compositing (order, blend, crop, override) | [48](../chapters/ch48-compositing.md) | App. G.8 | ● |
| Metadata | [49](../chapters/ch49-metadata.md) | App. G.6 | ● |
| Archiving | [50](../chapters/ch50-archiving-and-provenance.md) | 29.4 | ● |
| STAC / search / finding data | [51](../chapters/ch51-finding-data.md) | App. H | ● |
| Ground-truth datasets | [52](../chapters/ch52-ground-truth.md) | App. H | ● |
| Evaluating others' data | [54](../chapters/ch54-evaluating-others-data.md) | App. G.7 | ● |
| Public products comparison | [55](../chapters/ch55-public-products.md) | App. E | ● (long) |
| Local vs integrated datasets | [3](../chapters/ch03-fitness-for-use.md), [48](../chapters/ch48-compositing.md) | 55.7 | ● |
| Visualization: colormaps, filtering, rendering, splats | [57](../chapters/ch57-visualizing-dems.md) | 22.10 | ● (long) |
| Map making, USGS topos, graticules | [58](../chapters/ch58-making-maps.md) | — | ● (long) |
| Vector data; GCPs | [59](../chapters/ch59-vector-data.md) | 25 | ● (long) |
| S2 / H3 / location codes | [60](../chapters/ch60-dggs-and-location-codes.md) | — | ● (long) |
| Use constraints: hydrology, shoalest point | [61](../chapters/ch61-hydrology.md), [62](../chapters/ch62-navigation-and-charting.md) | 48.3 | ● |
| Navigation and charting | [62](../chapters/ch62-navigation-and-charting.md) | 70 | ● |
| Roads under buildings; innerspace; solar panels/antennas | [63](../chapters/ch63-buildings-cities-innerspace.md) | 32.3, 33.4 | ● |
| Crops; agriculture | [64](../chapters/ch64-agriculture-forests-wetlands.md) | 36 | ● |
| Mining, landfills, dumps | [65](../chapters/ch65-mining-landfills-earthworks.md) | 27.6 | ● (long) |
| Legal issues; shoreline law | [68](../chapters/ch68-legal-issues.md) | 34.3, 69 | ● |
| Privacy; national security; sovereignty | [69](../chapters/ch69-security-sovereignty-privacy-ethics.md) | 63.8, 68.7–68.8 | ● |
| HSSD / FPM / standards and guides | [70](../chapters/ch70-specifications-guided-tour.md), App. D | every "Standards & guides" section | ● |
| Software per topic | [71](../chapters/ch71-software-landscape.md), App. F | every "Software" section | ● |
| Change of systems over time | every "Then & now"; [72](../chapters/ch72-history.md) | App. C | ● |
| Math per topic | every "Mathematics"; App. B | — | ● |
| References per topic | every "References" | — | ● |
| Pitfalls and takeaways per topic | every chapter | App. G | ● |
| Validation / uncertainty throughout | every "Validation & uncertainty" | 5, 53, 56 | ● |

Every requested topic has at least one chapter-depth home. Two requested items deserve a note because they were deliberately *distributed* rather than given a chapter: "time scales of change" is split between Chapter 6 (time as a coordinate), Chapter 37 (the log–log map), and the per-object treatments (33.3 for wires, 27.1 for transient objects, 63.6 for cities); and "AIS/ADS-B" lives in 27.3 with a navigation echo in 62.8, which is the right weight for a data source that is a mask rather than a sensor.

## I.2 Added beyond the request

The brief invited additions. The following forty items were added either as whole chapters or as sections. They are listed with the reason, because a second edition should keep only those whose reason still holds.

**Whole chapters added**

1. **Fitness-for-use framework (Ch. 3).** Without it, every later "which DEM?" question had no decision procedure.
2. **Error and uncertainty toolkit early (Ch. 5).** Gives every later chapter a shared vocabulary (bias, σ, RMSE, NMAD, LE95, correlation length) and the Gaussian-conversion caveats.
3. **Time as a coordinate (Ch. 6).** Epochs, clocks, and synchronization are the most under-documented error source in practice.
4. **Measurement physics unified (Ch. 17).** Ranging, parallax, interferometry, inversion share error structures; teaching them once reduces repetition in 18–24.
5. **Calibration infrastructure (Ch. 25).** CORS, benchmarks, targets, and reference surfaces as a system rather than a footnote per sensor.
6. **Pipelines and lineage (Ch. 29).** Where information is lost and why reproducibility is a validation issue.
7. **Voids, occlusion, overhangs (Ch. 35).** Multi-valued surfaces and completeness metrics had no home.
8. **Forensic evaluation of others' data (Ch. 54).** The brief asked for it; it became the book's capstone.
9. **Case files (Ch. 56).** Sourced incidents that justify the validation emphasis; 23 sections plus 45 Case-file boxes elsewhere.
10. **DGGS in depth (Ch. 60).** Requested S2/H3; expanded to a full treatment because elevation in DGGS is an unsolved representation issue.
11. **Planetary DEMs (Ch. 67).** The no-ground-truth stress test for every validation idea in the book.
12. **Specifications crosswalk (Ch. 70).** S-44, HSSD, FPM, LBS, ASPRS, ICAO, INSPIRE compared on test logic rather than listed.
13. **History narrative (Ch. 72) and timeline (App. C).** Requested as "how systems changed"; given one narrative chapter plus a ⟨H⟩-tagged timeline.
14. **Open problems (Ch. 73).** A research agenda rather than a summary.

**Sections or themes added within chapters**

15. **Effective resolution vs nominal post (44.3)** with an estimation recipe.
16. **Spatially correlated error and volume uncertainty (53.5, 41.8, 65.1)** — the formula most often omitted in practice.
17. **Nuth–Kääb and ICP co-registration as a prerequisite (41.1)** in every change and validation workflow.
18. **CUBE/CHRT as the hydrographic analogue of ground filtering (30.6).**
19. **Grid registration: pixel-is-point vs pixel-is-area and half-cell shifts (31.3).**
20. **Format-induced error catalog (47.6):** quantization, Terrain-RGB steps, lossy overviews.
21. **The land–water seam / white ribbon (34.8, 48.6).**
22. **Hydro-flattening vs enforcement vs conditioning as three distinct operations (34.1).**
23. **Snow, firn, and radar penetration as datum-like biases (21.3, 36.2).**
24. **Three times of a dataset: measured, referenced, valid (37.3).**
25. **Kinematic datums and time-dependent transforms (37.5, 38.3).**
26. **Chart and DEM invalidation policy after earthquakes (39.8)** → checklist G.9.
27. **Semantic vs geometric change (41.7).**
28. **Spatial cross-validation and area of applicability for ML DEMs (43.5).**
29. **"Sharper is not truer" — validation of super-resolution (45.6).**
30. **Attribute models for uncertainty in data models (46.9).**
31. **Metadata decay and forensic reading of metadata (49.7–49.8).**
32. **Rescue of historical data (50.9).**
33. **Search by quality in catalogs (51.4).**
34. **Validating the validators (52.5):** truth has uncertainty too.
35. **Decision-oriented uncertainty quantification (53.8)** and visualizing uncertainty (57.9).
36. **Vertical accuracy → horizontal inundation error (61.5).**
37. **Drones: "400 ft above what?" (62.3)** — regulatory altitude references.
38. **What is a building? (63.1)** and roads under buildings (63.4).
39. **Water as a moving reference (66.7)** and lake/river datums (66.5–66.6).
40. **Indigenous and community data rights (68.10)** and lidar deserts/equity (69.5).

Beyond these, the appendices add things the brief did not ask for by name: a software index of about 190 tools (App. F), nine operational checklists (App. G), a teaching-dataset catalog with a tested synthetic-terrain generator (App. H), and the comparison tables with explicit "(verify)" flags (App. E).

## I.3 Items from the TOC's own gap list: status after drafting

The TOC's review section listed forty candidate additions. A heading-level and keyword audit of the drafted chapters gives the following status (✓ present at section or box level; ◐ mentioned; ✗ not found).

| # | Candidate | Status | Where / note |
|---|---|---|---|
| 1 | Earth tides, loading, refraction as cm-level effects | ◐ | Mentioned in 7, 12, 36, 37; no dedicated section. Recommend a half-section in 25 or 7. |
| 2 | Barometric altimetry | ✓ | 14 (and 62.3 for drones) |
| 3 | GNSS-R/IR | ✓ | 14, 64 |
| 4 | Orthorectification and NWP orography as hidden DEM consumers | ◐ | Appears in 8 chapters by keyword; a dedicated paragraph in 1 or 29 would help |
| 5 | Radio/solar/wind engineering uses | ✓ | 1, 63.7 |
| 6 | Robotics elevation maps, latency | ✓ | 62.5 |
| 7 | Time synchronization as error source (PPS/PTP) | ✓ | 6, 13; G.2 |
| 8 | Quantization/compression/overviews as error | ✓ | 47.6, 31.7 |
| 9 | Reproducibility and computational provenance | ✓ | 29.4, 50 |
| 10 | Crowdsourced elevation and trust | ✓ | 51.5, 16 |
| 11 | Human factors in manual editing | ✓ | 30.7, 42.8 |
| 12 | Economics / value of information | ✓ | 28.6 |
| 13 | Licence NC/SA contamination | ✓ | 68.3, 43.8, H.7 |
| 14 | 2.5D vs 3D decision aid | ◐ | 46, 63.4; no one-page aid yet |
| 15 | Hazard-specific DEM requirements | ◐ | Keywords in 11 chapters; no consolidated section — candidate for 61 |
| 16 | UNCLOS Art. 121 worked case | ✓ | 68.1, 69 |
| 17 | Caves, karst, tunnels, subsurface voxels | ◐ | 63.5, 65.6 |
| 18 | Sea ice and icebergs as moving terrain | ✓ | 27.7, 66.4 |
| 19 | Lake/river datums (IGLD) | ✓ | 9, 34, 66 |
| 20 | Terrain indices (TWI, solar, cold-air pooling) | ✓ | 61.7, 1 |
| 21 | Vertical exaggeration honesty | ✓ | 57 |
| 22 | Generative/synthetic terrain leaking into catalogs | ✓ | 45.4, H.6 |
| 23 | Tile naming and indexing schemes | ◐ | 47, 51; no table |
| 24 | Elevation APIs and hidden provenance | ✓ | 51 |
| 25 | Consumer lidar validity | ✓ | 16 |
| 26 | Benchmarking culture (DEMIX, ISPRS, DFC, Shallow Survey) | ✓ | 52.7, 53; H.1 |
| 27 | Education/certification pathways | ◐ | Brief in 68.4; proposed Appendix J not written |
| 28 | Communicating uncertainty to decision makers | ✓ | 53.8, 57.9 |
| 29 | Equity and lidar deserts | ✓ | 69.5, 56.22 |
| 30 | Energy and carbon cost | ✓ | 28.8, 50.8 |
| 31 | Accessibility | ✓ | 57.11 |
| 32 | Artemis-era lunar south-pole requirements | ◐ | 67 covers polar DEMs; "Artemis" not named — update at revision |
| 33 | GPR and seismics | ✓ | 24.3–24.4, 21.8 |
| 34 | Areoid/selenoid | ✓ | 67.1 |
| 35 | Space weather on GNSS | ✓ | 12 (scintillation), 26 |
| 36 | Atmospheric correction in InSAR; DEM's role | ✓ | 21.4, 21.6 |
| 37 | Shadow/illumination in SDB and matching | ✓ | 22.8, 23.1 |
| 38 | Squat/heave/settlement | ✓ | 13, 20, 56.2 |
| 39 | Insurance and finance uses | ✓ | 1, 68 |
| 40 | Post-disaster SOP checklist | ✓ | 39.8 → App. G.9 |

Net: 31 of 40 are present at section depth, 9 are mentioned but thin. None is absent. The thin ones (1, 4, 14, 15, 17, 23, 27, 32) are the natural first additions for a second edition and are small — each is a half-section or a table, not a chapter.

## I.4 Length, duplication, and suggested trims

**The book overshoots its own target.** The style guide asks for 4,500–7,000 words per chapter. At the time of this audit — after a first trim pass on Chapters 12, 21, 55–60, and 65–67 — 65 of 73 chapter files still exceed 7,000 words and 9 exceed 9,000 (Chapters 5, 21, 55, 56, 57, 58, 59, 60, 65); Chapters 1, 6, 12, 66, and 67 sit just under 9,000. The total is approximately 573,000 words of chapters (≈ 620,000 with appendices) — roughly 1,450 printed pages at 400 words per page — against the TOC's estimate of 900–1,100 pages for the full edition. The first trim pass removed about 1,000–1,500 words from each of the longest chapters, which shows that cutting duplication rather than content is feasible; it did not bring any chapter under the ceiling. Some overshoot is content (the sensor and validation chapters earn their length), but much of it is structural: repeated definitions, parallel "Then & now" and "History" material, and Software sections that re-list the same tools. The trims below are ordered by expected savings per unit of editorial effort; word counts are post-trim-pass values and will drift as editing continues.

### I.4.1 Chapters that run long, and what to cut

| Chapter | Words (after first trim pass) | Diagnosis | Suggested trim | Target |
|---|---|---|---|---|
| 12 GNSS | ≈ 9,000 | Full receiver-level tutorial (signal structure, every error source, every correction service) duplicates Chapter 11 history and Chapter 25 CORS material | Keep error budget, height-specific issues (tropospheric zenith delay, antenna PCV, multipath, geometry), PPK/RTK/PPP comparison, and the Validation section; move signal/constellation background to a 600-word box and cite texts | 7,000 |
| 21 Radar, SAR, InSAR, altimetry, ice radar | ≈ 9,100 | Five sub-disciplines in one chapter; 10 numbered sections | Split altimetry (21.7) and ice/ground-penetrating radar (21.8–21.9) into a short Chapter 21b, or move radar altimetry to 23.4 (altimetry-predicted bathymetry already discusses it) and GPR to 24.4 | 7,000 + 3,500 |
| 55 Public products | ≈ 9,500 | Product-by-product prose repeats the tables now in Appendix E; errata section overlaps Case files 56.13–56.14 | Replace per-product paragraphs with the comparison framework (55.6), fitness by use (55.7), and errata; point to Appendix E for specifications | 6,000 |
| 56 Case files | ≈ 9,700 | 23 cases; some (56.6 units, 56.20 Everest) are history rather than validation lessons; several duplicate boxes in the subject chapters | Keep 14–16 cases with the strongest sourced lessons; move 56.20 to Chapter 72 and 56.6 to a box in Chapter 9; cross-reference instead of retelling where a chapter already has the Case-file box | 7,000 |
| 57 Visualizing DEMs | ≈ 9,400 | 11 sections; neural/splat rendering (57.8) overlaps 22.10; accessibility and time sections are long | Fold 57.8 into 22.10 with a pointer; compress 57.10–57.11 | 7,000 |
| 58 Making maps | ≈ 9,400 | Full cartography course; aeronautical and nautical chart sections duplicate 62.1–62.2 | Keep purpose/scale/accuracy, contours, graticule/three norths, marginalia, QA; refer to 62 for charts | 6,500 |
| 59 Vector data | ≈ 10,400 | Ten sections; geometry-type primer and generalization are textbook material | Cut 59.1 to a definitions box; compress 59.9–59.10; keep breaklines, contours-as-data, shorelines, GCPs, topology, operations | 6,500 |
| 60 DGGS and location codes | ≈ 10,400 | Each scheme gets a full section; the brief asked mainly for S2/H3 | Merge 60.4 (other DGGS) and 60.5 (human codes) into one comparative table-driven section; keep 60.6 elevation in DGGS and 60.8 issues | 6,500 |
| 65 Mining, landfills, earthworks | ≈ 9,300 | Nine sections; volume computation (65.1) is excellent and should stay; standards/legal (65.3) overlaps 68 | Compress 65.3, 65.8; merge 65.4–65.5 (landfills, construction) into "engineered fills" | 7,000 |
| 1 Uses on land; 5 Error toolkit; 6 Time | ≈ 8,900–9,100 each | Foundational; long because they are the book's vocabulary | Trim examples, not definitions; move extended worked examples to Appendix B (for 5) and Appendix H exercises (for 1, 6) | 7,500 |
| 66 Coastal, marine, polar, lakes, rivers | ≈ 8,700 | Six environments; some repeat 34 (water) and 40.4 (coastal change) | Pointer-ize overlaps with 34 and 40 | 7,000 |

### I.4.2 Cross-chapter duplication

- **History appears three times**: Chapter 11 (positioning), Chapter 72 (narrative), Appendix C (timeline), plus every "Then & now". Recommendation: keep "Then & now" short (≤ 300 words) and ⟨H⟩-tagged, let Appendix C carry dates, and let 72 carry only the narrative arc.
- **Co-registration (Nuth–Kääb/ICP)** is explained in 41.1, 53, 54.4, 55.6, and several domain chapters. Explain once in 41.1 (with the math in Appendix B) and link.
- **Geoid/ellipsoid confusion** is a recurring box in roughly a dozen chapters. That repetition is deliberate for a reference book read non-linearly, but the boxes should be identical in wording and point to 9.
- **Software sections** re-list GDAL/PDAL/QGIS in nearly every chapter. With Appendix F in place, chapter Software sections can shrink to the chapter-specific tools plus one line "general tools: see Appendix F".
- **Standards & guides** repeat ASPRS 2014/2023 and S-44 editions across chapters; Appendix D should become the single place for edition numbers, with chapters citing only what they use.
- **Water** is treated in 34 (operations), 36.3 (seasonal), 61.4 (bathymetry under models), 66 (environments). The split is defensible; the overlap between 34.4 "shorelines move" and 40.4 "coastal change" is not — merge toward 40.4.

### I.4.3 A slimmer edition (≈ 45 chapters)

The TOC's merge plan remains sound after drafting; the audit confirms the merges that cost least: 1+2 (uses), 7+8 (geodesy + horizontal datums), 13+14 (IMU + non-GNSS positioning), 23+24 (indirect bathymetry and geophysics), 28 into 26 (cost into planning), 33 into 32 (wires into DSM→DTM), 40+41 (geomorphic change + change detection), 44+45 (resolution + enhancement), 49+50 (metadata + archiving), 59+60 (vectors + DGGS), and Part XIV compressed to three chapters (water domains; built and engineered; living and planetary). Chapter 17 (measurement physics) should *not* be folded into the sensor chapters, contrary to the TOC's suggestion: in drafting it proved to be the chapter that lets 18–24 avoid repeating error derivations. Chapters 5, 53, 54, and 56 stay intact; they are the validation spine.

## I.5 Quality observations from the audit

- **The mandatory Validation & uncertainty section exists in every chapter**, and in the sensor chapters it is numerate (budgets with magnitudes). In some domain chapters (63, 64) it leans on references to 53 rather than giving domain-specific procedures; a second edition should add one worked example each.
- **Case-file boxes (45 across chapters) plus Chapter 56** give the book its evidential tone. A few boxes cite incidents that could not be fully verified during drafting and carry "(verify)"; these must be resolved or removed before publication — an unverifiable case file undermines the chapter that uses it.
- **"(verify)" flags** are concentrated in References, product specifications (Appendix E), and licence statements (Appendix F, H). A bibliography pass with DOIs would clear most of them; the remainder (product accuracy figures) should be re-checked against the current product handbooks on a fixed schedule because they change.
- **Regional balance.** Examples remain US/EU/NZ/JP-heavy. Appendix E lists programs from 17 countries, but worked examples from Africa, South America, South and Southeast Asia, and Pacific SIDS are few (56.22 and 69.5 are the exceptions). This is the most important content gap that is not a topic gap.
- **Figures** are placeholders throughout (2–6 per chapter as specified). The figure programme — roughly 300 figures — is a project in itself and should be planned with a consistent style for hillshades, residual maps, and uncertainty maps before any are drawn.
- **Notation** is consistent (σ, RMSE, LE95, h = H + N, TVU/THU, NVA/VVA, LoD) and defined in Appendix A/B. One residual inconsistency: some chapters write "LE90" for product specs quoted from producers (correctly, since that is what the producers report) and "LE95" for their own statistics; a sentence in Chapter 5 should state this convention explicitly.

## I.6 Open decisions for a second edition

1. **Length and format.** Publish the full edition (≈ 1,500 pages as drafted) as a reference with the slim edition (≈ 45 chapters, ≈ 500 pages) as the teaching text, or trim the full edition toward 1,000 pages first. The trims in I.4 reach roughly 1,100 pages without losing topics.
2. **Living appendices.** Appendices D, E, F, and H describe things that change yearly (editions, product versions, software licences, dataset URLs). Decide whether they are maintained as versioned web pages with the print edition carrying a snapshot date, and who owns updates.
3. **Bibliography infrastructure.** Maintain a BibTeX file with DOIs for every reference; decide whether chapters cite by author–year (current) or number. Resolve every "(verify)" or delete the citation.
4. **Exercises.** Decide whether each chapter gains a worked exercise using an Appendix H dataset, with solutions in a companion repository, which would turn the handbook into a usable course text.
5. **Code.** Decide the policy for "Try it" snippets: a tested companion repository with CI against pinned GDAL/PDAL/xdem versions (recommended — the synthetic-terrain script in H.6 was run before inclusion; most other snippets were not executed), or untested illustrative code clearly labelled as such.
6. **Units and conventions.** Keep SI with imperial in parentheses only where a standard uses it; decide whether to adopt "elevation positive-up" universally in the book's own tables, including bathymetry, with a standing note on chart convention.
7. **Regional examples.** Commission or solicit case material from under-represented regions (Caribbean lidar programs, African national mapping, Mekong and Ganges deltas, Pacific SIDS bathymetry) for Chapters 1, 2, 56, 61, 66, 69.
8. **Appendix J (learning pathways).** The TOC floated an appendix on education and certification (IHO Cat A/B, ASPRS CP, licensed surveyors, GISP). It was not written; decide whether it belongs in the book or on the companion site.
9. **Hazard constraints chapter.** Candidate 15 in I.3 (avalanche, rockfall, lava, tsunami, debris flow) is the one thin area large enough to justify a short new chapter (61b) rather than a section.
10. **Governance of "(verify)" in product tables.** Appendix E is the part of the book most likely to be wrong on the day it is printed. Decide a re-verification cadence (e.g. every GEBCO/Copernicus release) and whether to print accuracy figures at all or only point to the product handbooks with the handbook's own independent-test summaries.
11. **ML-era drift.** Chapters 43 and 45 describe tools and products (FABDEM, GEDTM30, foundation models for point clouds) whose state of the art turns over in 1–2 years. Decide whether these chapters are written to principles only, with the product specifics moved to the living appendices.
12. **Accessibility of the book itself.** The book preaches colour-blind-safe palettes and tactile maps (57.11); decide the production standard for its own figures and for an accessible digital edition.

<!-- figure: Figure I.1 — Word count per chapter (bar chart) with the 4,500–7,000 target band shaded, highlighting the thirteen chapters above 9,000 words. -->

## I.7 Summary

Against the original request, coverage is complete: every topic has a chapter-depth home, and the handbook adds a decision framework (fitness for use), a statistical spine (error toolkit, accuracy assessment, forensic evaluation, case files), and operational scaffolding (checklists, product tables, software index, datasets) that the request implied but did not name. The costs of that completeness are length — most chapters exceed the target — and maintenance exposure in the appendices that catalogue a moving landscape. The second edition's work is therefore less about new topics than about trimming duplication, verifying every flagged fact, balancing regional examples, and deciding which parts of the book live on paper and which live online.

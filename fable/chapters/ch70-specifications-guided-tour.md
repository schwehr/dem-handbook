# Chapter 70 — Survey and product specifications: a guided tour (S-44, HSSD, FPM, LBS, ASPRS, ICAO, INSPIRE…)

> **Part XVI — Standards, software, and history.** The documents that define what "good enough" means in each elevation domain — how they are built, how they differ, and how to read, apply, and crosswalk them without being misled by their tables.

**In this chapter.** A specification is a domain's written definition of fitness for use. This chapter takes the major ones apart: IHO S-44 and the national hydrographic specifications built on it (NOAA HSSD and Field Procedures Manual, USACE EM 1110-2-1003, LINZ, UKHO, CHS, Australia), the topographic lidar and photogrammetry family (USGS Lidar Base Specification, ASPRS Positional Accuracy Standards Ed. 2, FEMA, national specs), the aviation stack (ICAO Annex 15 and PANS-AIM eTOD, DO-276C, DO-200B, FAA AC 150/5300-18), geodetic control standards, and product specifications (INSPIRE Elevation, Copernicus DEM, DTED, S-102). You will learn the anatomy common to all of them — scope, definitions, accuracy classes, coverage and density, feature detection, calibration and QC, deliverables, metadata, acceptance tests — and then see them side by side in crosswalk tables that expose where their confidence levels, surfaces, and statistics do and do not line up. The chapter closes with how to read a spec critically, how to write a project-specific one that references rather than copies, and how compliance is audited. Appendix D holds the full citation index.

## 70.1 How specifications are built

Every mature specification has the same skeleton, and reading one is faster once you know where each part lives. **Scope** states what the document governs (a survey, a product, a process) and, as importantly, what it does not; S-44 governs hydrographic surveys for navigation safety and explicitly not, say, habitat mapping. **Definitions** are where the surface is defined — bare earth or first return, sounding or gridded node, "well-defined point" — and where a careless reader loses the most; [Chapter 4](ch04-names-and-definitions.md) is a long argument that this section matters more than the tables. **Accuracy classes or orders** then tabulate requirements: a confidence level (90 %, 95 %, RMSE), a horizontal and vertical allowance, and often a depth- or scale-dependent term. **Coverage and density** state how much of the surface must be measured (100 % ensonification, 2 points per square metre), and **feature detection** states the smallest object that must be found — a requirement distinct from accuracy that only hydrographic and aviation-obstacle specs make explicit. **Calibration and QC requirements** list the tests (patch test, boresight, crosslines, swath overlap analysis) and their frequency. **Deliverables** enumerate formats and contents; **metadata** requirements name the schema; and **acceptance tests** define how the buyer decides, with what sample, and what happens on failure.

Two design philosophies divide the field. **Prescriptive** specifications tell the contractor how to do the work — line spacing, flying height, pulse rate, software settings — which makes compliance easy to check and innovation hard; older national hydrographic specs and many engineering contracts are prescriptive. **Performance-based** specifications state the result required — uncertainty, coverage, detection — and leave the method to the surveyor, which is how S-44 is written since the 4th edition and how ASPRS and the LBS increasingly are. Performance specs demand better validation ([Chapter 53](ch53-accuracy-assessment.md)) because the method no longer guarantees the outcome. Finally, every spec has **versions**; the edition in force on the contract date is the one that binds ([Chapter 68](ch68-legal-issues.md)), and the change log between editions is the most informative document a newcomer can read, because it records what went wrong with the previous one.

> **Definitions that bite.** *Accuracy class* in ASPRS Ed. 2 is named by its RMSE — "10-cm vertical accuracy class" means RMSE$_z$ ≤ 0.10 m in non-vegetated terrain. *Quality Level* in the USGS LBS bundles an accuracy class with a density and a nominal pulse spacing — QL2 is RMSE$_z$ ≤ 0.10 m *and* ≥ 2 pulses/m². *Order* in S-44 bundles uncertainty, feature detection, and coverage and is *selected* by the hydrographic office for an area, not earned by the data. *Area* in ICAO eTOD is a geographic zone around an aerodrome with its own numerical requirements. A sentence like "the survey meets Order 1a / QL2 / Area 2" therefore asserts four different kinds of thing, and only one of them (the ASPRS class) is purely a statement about tested accuracy.

## 70.2 Hydrographic specifications

### 70.2.1 IHO S-44

The International Hydrographic Organization's *Standards for Hydrographic Surveys*, S-44, first published in 1968 ⟨H⟩ and now at Edition 6.1.0 (2022, a minor revision of 6.0.0, 2020), is the root document of the hydrographic family. It defines five **orders** — Exclusive, Special, 1a, 1b, and 2 — each with a maximum **total horizontal uncertainty** (THU) and **total vertical uncertainty** (TVU) at the 95 % confidence level, a **feature detection** requirement (the smallest cubic feature that must be detected), a **feature search** requirement, and a **bathymetric coverage** requirement. TVU is depth-dependent through the familiar formula

$$\mathrm{TVU}_{\max}(d) = \sqrt{a^2 + (b\,d)^2},$$

with $a$ the depth-independent term (metres) and $b$ the depth-dependent factor; THU for the lower orders also grows with depth. Table 70.1 gives the Ed. 6 values.

| Order | THU (95 %) | TVU: $a$, $b$ | Feature detection | Feature search | Bathymetric coverage |
|---|---|---|---|---|---|
| Exclusive | 1 m | 0.15 m, 0.0075 | 0.5 m cube | 200 % | 200 % |
| Special | 2 m | 0.25 m, 0.0075 | 1 m cube | 100 % | 100 % |
| 1a | 5 m + 5 % d | 0.5 m, 0.013 | 2 m cube to 40 m; 10 % of depth beyond | 100 % | ≤ 100 % |
| 1b | 5 m + 5 % d | 0.5 m, 0.013 | not specified | recommended, not required | 5 % |
| 2 | 20 m + 10 % d | 1.0 m, 0.023 | not specified | not required | 5 % |

Three features of Ed. 6 matter in practice. First, the orders are **minimum standards selected by the hydrographic office**, and Ed. 6 introduced the **survey matrix** — a template in which the office specifies each parameter independently (a tighter TVU with looser feature detection, for instance) when no order fits; a contract may cite an order or a matrix, and the two are not interchangeable. Second, "bathymetric coverage" is the fraction of the seafloor ensonified, distinct from "feature search," the fraction searched to the feature-detection standard; 200 % means every point seen from two independent passes. Third, uncertainty is **total propagated uncertainty** (TPU) at 95 %, meaning each sounding carries a modelled uncertainty from positioning, attitude, sound speed, tide, and sensor components ([Chapter 20](ch20-sonar.md), [Chapter 26](ch26-survey-planning.md)); the S-44 test is that the TPU of every accepted sounding be within the allowance, which is a per-sounding model check, not a comparison against ground truth. Companion IHO documents fill in the rest: **C-13** (*Manual on Hydrography*) is the textbook; **S-67** (*Mariners' Guide to Accuracy of Depth Information in ENCs*, 2020) explains the CATZOC quality indicators that S-44 orders feed; **B-11** (the GEBCO Cookbook) covers compilation of grids; **B-12** governs crowdsourced bathymetry; and the **S-100** product specifications — S-101 (ENC), S-102 (bathymetric surface, with mandatory uncertainty layer), S-104 (water level), S-111 (currents) — define how survey quality is carried into products ([Chapter 47](ch47-file-formats.md), [Chapter 62](ch62-navigation-and-charting.md)).

### 70.2.2 NOAA HSSD and the Field Procedures Manual

NOAA's Office of Coast Survey issues the *Hydrographic Surveys Specifications and Deliverables* (**HSSD**) annually; it is the document that binds NOAA field units and contractors. Where S-44 says what, HSSD says what *for NOAA*: it defines three coverage types — **object detection coverage** (a density sufficient to detect features of a stated size, with a minimum number of soundings per node), **complete coverage** (100 % ensonification without the object-detection density requirement), and **set line spacing** (single-beam or sparse lines at specified spacing) — and assigns them to survey areas by chart scale and use. It specifies TPU thresholds (aligned with S-44 orders, with NOAA-specific values for some products; the 2024 edition was a major restructuring), crossline requirements (typically a stated percentage of mainscheme line length, compared statistically), feature-attribution rules, and a long deliverables list: BAG grids at prescribed resolutions, an S-57 feature file, the **Descriptive Report** (DR) that narrates the survey and its problems, survey outlines, and metadata — now all feeding the **National Bathymetric Source** (NBS) compilation. Because HSSD changes every year (grid resolutions, required attributes, acceptance of new sensors), a contractor who reads the 2021 edition for a 2025 survey will fail deliverables checks on details that look cosmetic and are not.

The NOAA **Field Procedures Manual** (FPM; last issued as a dated PDF in 2014 and since maintained as a living online document) is the companion that says *how*: systems preparation and annual calibrations (patch tests, lead-line or bar checks, sound-speed sensor comparisons, GNSS and water-level system checks), reference-surface comparisons, data acquisition procedures, processing in NOAA's software stack, and documentation. The FPM is the document to read when a spec says "calibrated" and you want to know what that means operationally; it is also a good template for any organization writing its own procedures.

### 70.2.3 USACE EM 1110-2-1003 and other national specs

The US Army Corps of Engineers' Engineer Manual *Hydrographic Surveying* (EM 1110-2-1003, 30 November 2013) governs surveys for navigation-project design, maintenance, and — critically — **dredging payment**. It classifies surveys by purpose and bottom type (hard-bottom navigation and dredging support, soft-bottom navigation and dredging support, other general surveys), with vertical accuracy tolerances at 95 % of approximately ±0.15 m (0.5 ft), ±0.3 m (1.0 ft), and ±0.6 m (2.0 ft) respectively and horizontal tolerances of roughly 2–5 m (Table 3-1 of the manual gives the exact values by project class), and it prescribes performance tests, water-level correction procedures, and volume-computation methods because the surveys determine payment ([Chapter 65](ch65-mining-landfills-earthworks.md)). Its mixed units (feet in tables, metres in text) are themselves a lesson in reading specs.

Elsewhere: Land Information New Zealand's **HYSPEC** (*Contract Specifications for Hydrographic Surveys*) is a model of a tight performance spec built on S-44 with explicit deliverable schemas; the UK Hydrographic Office and the Maritime and Coastguard Agency's civil hydrography programme specifications and the **CHS Hydrographic Survey Management Guidelines** (Canada) are similar; Australia's **HydroScheme Industry Partnership Program** (HIPP) specifications added requirements for ancillary data (backscatter, water column) and S-100-ready deliverables. All inherit S-44's uncertainty framework and differ mainly in deliverables, metadata, and the operational detail they prescribe.

<!-- figure: Figure 70.2 — Anatomy of a specification: a one-page schematic showing the common skeleton (scope, definitions, classes, coverage/density, feature detection, calibration/QC, deliverables, metadata, acceptance) with callouts to where each element lives in S-44, HSSD, LBS, ASPRS Ed. 2, and PANS-AIM. -->

## 70.3 Topographic lidar and photogrammetry specifications

### 70.3.1 USGS Lidar Base Specification

The **Lidar Base Specification** (LBS) began as USGS Techniques and Methods 11-B4 in 2012 (v1.0), passed through v1.2 (2014), v1.3 (2018), v2.0–2.1 (2019–2020), and is now maintained online as "LBS 2024 rev. A." It is the de facto US national lidar spec through the 3D Elevation Program (3DEP) and the template for many state and county contracts. Its core is the **Quality Level** table (Table 70.2), which bundles vertical accuracy, aggregate nominal pulse spacing (ANPS), and density:

| QL | RMSE$_z$ (NVA) | ANPS | Density | Typical use |
|---|---|---|---|---|
| QL0 | ≤ 5 cm | ≤ 0.35 m | ≥ 8 pls/m² | engineering, urban |
| QL1 | ≤ 10 cm | ≤ 0.35 m | ≥ 8 pls/m² | 3DEP target (increasingly) |
| QL2 | ≤ 10 cm | ≤ 0.71 m | ≥ 2 pls/m² | 3DEP baseline |
| QL3 | ≤ 20 cm | ≤ 1.41 m | ≥ 0.5 pls/m² | legacy / coarse |

Beyond the table, the LBS specifies: swath overlap and **relative accuracy** (intra-swath and inter-swath differences on smooth surfaces, with numeric limits per QL); a mandatory **classification scheme** (ASPRS classes 1, 2, 7, 9, 17, 18, 20 and others, with definitions); **hydro-flattening** of water bodies above a size threshold using breaklines ([Chapter 34](ch34-water-in-dems.md)); a DEM deliverable at a stated cell size with void and tile rules; LAS 1.4 point data record formats; and detailed metadata. The **NVA** (non-vegetated vertical accuracy) and **VVA** (vegetated vertical accuracy) terms replaced the older FVA/SVA/CVA in v1.2 (2014), following ASPRS Ed. 1; the 2024 rev. A edition then aligned the testing framework with ASPRS Ed. 2 while keeping the NVA/VVA names (Ed. 2 itself speaks of RMSE$_V$ and RMSE$_H$): the minimum checkpoint count rose from 20 to 30 and scales with project area, checkpoint survey uncertainty must be included in the reported RMSE, and projects can no longer *fail* on VVA alone — VVA is reported, not thresholded. The "95 % confidence" framing was dropped in favour of RMSE-only reporting.

### 70.3.2 ASPRS Positional Accuracy Standards

The ASPRS *Positional Accuracy Standards for Digital Geospatial Data* (Edition 1, 2014; **Edition 2**, 2023, with a 2024 version 2 adding addenda) replaced the scale-based ASPRS 1990 standard and the FGDC NSSDA's 95 % language with RMSE-named accuracy classes. Edition 2 defines **horizontal** classes by RMSE$_H$ = $\sqrt{\mathrm{RMSE}_x^2 + \mathrm{RMSE}_y^2}$, **vertical** classes by RMSE$_V$ in non-vegetated terrain (Ed. 2 drops the NVA/VVA labels, which survive in the USGS LBS), and a new **3D accuracy** RMSE$_{3D}$ = $\sqrt{\mathrm{RMSE}_x^2 + \mathrm{RMSE}_y^2 + \mathrm{RMSE}_z^2}$; it requires at least 30 well-distributed checkpoints, requires that checkpoint survey accuracy be included in the product RMSE, removed the Edition 1 requirement that VVA (95th percentile of absolute errors in vegetated terrain) be no worse than three times the NVA class, and dropped 95 % confidence statements from the reporting language. Addenda give best practices for field surveying of control and checkpoints, photogrammetry, lidar, UAS, and oblique imagery. The historical lineage matters because contracts still cite the predecessors: the **FGDC NSSDA** (1998) with its Accuracy$_z$ = 1.96 RMSE$_z$ and 20-checkpoint rule, the **NDEP Guidelines for Digital Elevation Data** (2004) that invented FVA/SVA/CVA and the 95th-percentile treatment of vegetated terrain, and the **NMAS** of 1947 ⟨H⟩ with its 90 % of well-defined points within 1/30 inch at map scale and half a contour interval vertically.

### 70.3.3 Other national and sector specifications

FEMA's *Guidelines and Standards for Flood Risk Analysis and Mapping* require elevation data meeting USGS QL2 or better for new flood studies and specify how NVA/VVA are reported. **USACE EM 1110-1-1000** (*Photogrammetric and LiDAR Mapping*, 2015) is the Corps' topographic counterpart to EM 1110-2-1003. Australia's **ICSM LiDAR Acquisition Specifications and Tender Template** (v1.0, 2010) was influential in its explicit treatment of classification and metadata; Canada's **CanElevation** specifications under NRCan's National Elevation Data Strategy, the UK Environment Agency's survey specifications, the Netherlands' **AHN** specifications (now AHN5, with quality tiers and systematic validation), and the Nordic national programmes (Denmark's DHM, Finland's NLS, Sweden's Lantmäteriet, Norway's Nasjonal detaljert høydemodell) each define national QLs loosely comparable to the LBS. ISPRS and EuroSDR publish guidance and benchmarks rather than binding specs. For UAS mapping, the ASPRS Ed. 2 UAS addendum and national aviation rules supply the frame; there is no universally adopted UAS mapping spec, which is why UAS deliverables so often arrive with untested accuracy claims ([Chapter 22](ch22-photogrammetry-sfm.md)).

## 70.4 Aviation: terrain and obstacle data

Aviation is the one domain in which elevation-data requirements carry **integrity** classifications and a legal processing chain. **ICAO Annex 15** (*Aeronautical Information Services*) establishes the obligation on states to provide **electronic terrain and obstacle data** (eTOD); since Amendment 39 (2018) the numerical requirements live in **PANS-AIM, Doc 10066**, Appendix 1. Four **areas** are defined: Area 1 (the entire state territory), Area 2 (the terminal control area, subdivided into 2a–2d around the aerodrome), Area 3 (the aerodrome movement area), and Area 4 (the Category II/III precision-approach zone). Table 70.3 summarizes the terrain requirements (obstacle requirements are similar but with their own horizontal/vertical allowances).

| Area | Post spacing | Vertical accuracy | Horizontal accuracy | Confidence | Integrity |
|---|---|---|---|---|---|
| 1 | 3″ (≈ 90 m) | 30 m | 50 m | 90 % | routine (10⁻³) |
| 2 | 1″ (≈ 30 m) | 3 m | 5 m | 90 % | essential (10⁻⁵) |
| 3 | 0.6″ (≈ 18 m) | 0.5 m | 0.5 m | 90 % | essential (10⁻⁵) |
| 4 | 0.3″ (≈ 9 m) | 1 m | 2.5 m | 90 % | essential (10⁻⁵) |

(Values from PANS-AIM Appendix 1, which also specifies vertical resolution and the separate obstacle allowances; the amendment in force on the contract date governs.) Two things distinguish this from any topographic spec: the **90 % confidence level** rather than 95 % or RMSE, and the integrity levels, which are probabilities of undetected corruption per data element and are met by process assurance under **RTCA DO-200B / EUROCAE ED-76A** rather than by measurement. **RTCA DO-276C / EUROCAE ED-98C** (*User Requirements for Terrain and Obstacle Data*, 2015) is the detailed companion, specifying surface definitions (terrain is the bare earth *excluding* vegetation in principle, but the DSM may be accepted with stated treatment — a definitional point that matters for forest near runways), data attributes, and quality metadata; **ICAO Doc 9881** gives guidance; **EUROCONTROL's Terrain and Obstacle Data Manual** operationalizes it for Europe. In the United States, **FAA AC 150/5300-18** (*General Guidance and Specifications for Submission of Aeronautical Surveys to NGS*; 18B, 2009, with Change 1, 2011; the 18C revision was cancelled in 2016 and 18B reinstated) specifies, feature by feature, the horizontal and vertical accuracy of runway ends, navaids, obstacles, and terrain, with AC 150/5300-16 and -17 covering geodetic control and imagery. The practical consequence for a DEM producer is that aviation customers will ask for 90 % figures, DO-200B-compliant handling, and feature-level accuracy statements — none of which a standard lidar deliverable provides without translation ([Chapter 62](ch62-navigation-and-charting.md)).

## 70.5 Geodetic control standards

Every elevation spec rests on control, and control has its own specifications. The **FGCC 1984** *Standards and Specifications for Geodetic Control Networks* defined the classical orders and classes (first-order, second-order class I/II, third-order) by relative accuracy between adjacent points — e.g., first-order class I levelling requires the propagated standard deviation of an elevation difference, divided by the square root of the route distance in kilometres, not to exceed $b$ = 0.5 mm (0.7, 1.0, 1.3, and 2.0 mm for the lower classes) — still cited in legacy benchmark descriptions. **NGS-58** (1997) gave procedures for GPS-derived ellipsoid heights at the 2 cm and 5 cm levels (two or more occupations of ≥ 30 min on different days at different satellite geometries, fixed-height tripods), and **NGS-59** (2008) extended them to GPS-derived orthometric heights by combining with a hybrid geoid ([Chapter 12](ch12-gnss.md), [Chapter 25](ch25-calibration-infrastructure.md)). "Bluebooking" — submitting survey data to NGS in prescribed formats for inclusion in the NSRS — is the US procedural standard for control that will be published. **ISO 17123** (parts 1–9) standardizes field procedures for testing instruments (levels, total stations, GNSS RTK), giving a repeatable way to state an instrument's achieved precision; **IGS** standards and **CORS site guidelines** govern continuously operating reference stations. NGS's NSRS modernization documents (Blueprints Parts 1–3) describe how control will be defined, published, and time-tagged in the 2022 frames, which will change how every US spec references control.

## 70.6 Product and data specifications

Where survey specs govern collection, product specs govern what is delivered to the world. The **INSPIRE Data Specification on Elevation** (D2.8.II.1, v3.0, 2013) defines a conceptual model (grid coverage, TIN, vector elevation) with mandatory attributes — surface type (DTM/DSM), vertical CRS, property type — and maps quality reporting onto **ISO 19157** data-quality elements (completeness, logical consistency, positional accuracy, temporal quality) with recommended measures such as RMSE or LE90 of vertical position; it recommends a 1 m resolution class for national products but does not require it. The **Copernicus DEM Product Handbook** states the product's specifications (GLO-30/GLO-90 absolute vertical accuracy better than 4 m LE90 and horizontal better than 6 m CE90 as specified) and its editing rules. **3DEP product standards** define the 1 m, 1/3″, and 1″ DEM products and their seamless-mosaic rules. **DTED** (MIL-PRF-89020B, 2000) defines Levels 0–2 (30″, 3″, 1″) with Level 2 absolute vertical accuracy of 18 m LE90 and horizontal 23 m CE90 — the 90 % confidence convention of defence and aviation again; NGA's **HRE** (High Resolution Elevation) and HRTe specifications extend DTED to finer postings. **OGC CityGML** (3.0, 2021) and its relief/terrain module define how elevation is carried in 3D city models; **S-102** (Ed. 3.0.0, 2024) defines the gridded bathymetric surface with mandatory uncertainty and quality-of-coverage layers. A product spec answers "what does the user receive and how is quality described," which is why ISO 19157 and INSPIRE quality elements are the right vocabulary for metadata regardless of domain ([Chapter 49](ch49-metadata.md)).

## 70.7 Crosswalk tables

Crosswalks are useful and dangerous. Table 70.4 aligns the major specifications on the dimensions they share; the footnotes mark where the alignment is approximate or impossible.

| Dimension | S-44 Ed. 6 | NOAA HSSD | USACE EM 1110-2-1003 | ICAO eTOD | ASPRS Ed. 2 | USGS LBS 2024 | INSPIRE Elevation |
|---|---|---|---|---|---|---|---|
| Confidence convention | 95 % TPU | 95 % TPU | 95 % | 90 % | RMSE$_V$ / RMSE$_H$ (class name) | RMSE$_V$ (NVA and VVA, per ASPRS Ed. 2; VVA not pass/fail) | ISO 19157 measure (RMSE or LE90 recommended) |
| Vertical tiers | Excl/Special/1a/1b/2 | by coverage type and S-44 order | hard/soft/other | Area 1–4 | RMSE$_z$ classes (1, 2.5, 5, 10, 15, 20 cm …) | QL0–QL3 | none (reported) |
| Horizontal | THU by order | THU | ≈ 2–5 m by class | 0.5–50 m by area | RMSE$_H$ classes | not thresholded for lidar | reported |
| Surface | seafloor soundings | soundings/nodes | soundings | bare terrain (with DSM caveats) | per product | bare earth (class 2) | DTM or DSM, attributed |
| Density/coverage | coverage % | object detection / complete / set line | line spacing by class | post spacing by area | n/a | ANPS, pls/m², swath overlap | resolution attribute |
| Feature detection | cube size by order | object size by coverage type | implicit | obstacle allowances | n/a | n/a | n/a |
| Acceptance test | TPU model + crosslines | crosslines, junctions, DR | performance tests | DO-200B process | ≥ 30 checkpoints | ≥ 30 checkpoints, stratified | not specified |

Reading across, the first row is the trap: 95 % of a normal distribution is 1.960σ, 90 % is 1.645σ, and RMSE (for zero bias) is 1.0σ, so an S-44 Order 1a TVU of 0.5 m at 10 m depth (≈ 0.52 m at 95 %) corresponds to σ ≈ 0.27 m, which would be a 25-cm ASPRS class, while an ICAO Area 2 terrain accuracy of 3 m at 90 % is σ ≈ 1.8 m, roughly a 2-m RMSE class; the conversions in the Mathematics section make these explicit and the Validation section explains why they are only approximately right. The surface row is the second trap: hydrographic TVU applies to individual soundings before gridding; LBS NVA applies to a bare-earth DTM interpolated from classified ground points; eTOD terrain may be a DSM with trees; comparing them compares different things. The feature-detection row has no topographic analogue at all — no lidar spec requires that a 1 m boulder be found — and the density row is incommensurable because sonar coverage is a swath-geometry concept while lidar density is a sampling concept. Use crosswalks to translate *requirements* between domains when you must (a topobathy lidar survey serving both charting and floodplain mapping needs both columns), and state the assumptions in writing.

<!-- figure: Figure 70.1 — Vertical allowances of the major specifications plotted on a common σ axis after conversion from their native conventions (95 %, 90 %, RMSE), for a 10 m depth / flat terrain case, showing where S-44 Special, 1a, LBS QL1/QL2, ASPRS 10- and 20-cm classes, and ICAO Areas 2–4 fall. -->

> **Worked example.** *Translating a topobathy lidar requirement.* A coastal county wants one survey to serve FEMA flood mapping (requires USGS QL2: RMSE$_z$ ≤ 0.10 m on bare earth) and a nearshore charting update that the hydrographic office will accept at S-44 Order 1a. At 5 m depth, Order 1a TVU$_{\max}$ = $\sqrt{0.5^2 + (0.013 \times 5)^2}$ = 0.504 m at 95 %, i.e., σ ≈ 0.257 m — far looser than QL2 on land. But Order 1a also requires 100 % feature search for 2 m cubes and ≤ 100 % bathymetric coverage, and the lidar must therefore demonstrate *detection* (laser spot density and footprint on the bottom, water-column attenuation, bottom-return classification) that no topographic QL addresses. The project spec should therefore cite LBS QL2 for the subaerial DTM, S-44 Order 1a for uncertainty *and* feature search over the submerged portion, define the land–water transition surface explicitly ([Chapter 19](ch19-bathymetric-lidar.md)), and name the test for each: 30+ checkpoints on land, TPU modelling plus crosslines and an independent multibeam patch for feature detection in water.

## 70.8 Reading specifications critically

Specifications are written by committees solving last decade's problems, and they are silent on several things a careful user needs. **Effective resolution** ([Chapter 44](ch44-resolution-and-sampling.md)) is nowhere: a QL1 product with 8 pulses/m² may have an effective resolution of 1–2 m after ground classification under canopy, and no spec requires it to be measured. **Correlated error** is absent: checkpoint RMSE assumes independent errors, but lidar errors are correlated along swaths and photogrammetric errors across blocks, so 30 checkpoints may sample only a handful of independent error realizations ([Chapter 53](ch53-accuracy-assessment.md)). **Temporal validity** is rarely addressed: a spec says when data were acquired but not how long the product may be used before the surface has changed enough to invalidate it ([Chapter 37](ch37-time-scales-of-change.md)). **Vegetated accuracy** has moved from a requirement to a report, which is honest about measurement but silent about use. And specs **lag technology**: topobathy lidar straddles two spec families; ML-derived DTMs and super-resolved products have no accepted acceptance test; variable-resolution grids, meshes, and point-cloud-native deliverables fit poorly into tile-and-cell-size language; single-photon and Geiger-mode lidar have noise characteristics the LBS relative-accuracy tests were not designed for.

When you write a **project-specific specification**, reference rather than copy. Name the standard and edition ("USGS LBS 2024 rev. A, QL1; ASPRS Positional Accuracy Standards Ed. 2 v2 for accuracy testing"), then add only what the project needs and the standard lacks: the use case and its decision thresholds ([Chapter 3](ch03-fitness-for-use.md)); the surface definition where ambiguous (bridges, culverts, water, overhangs); acquisition windows (leaf-off, low water, tidal stage); the checkpoint plan (who, how many, where, stratified how, surveyed to what uncertainty); deliverables including raw data, trajectories, and processing logs; metadata schema; acceptance statistics and remedies; and a deviations procedure. Avoid inventing new accuracy classes, avoid "or better" without a test, and never cite two standards for the same quantity without saying which governs.

## 70.9 Compliance and audit

A specification without an audit is a wish. A **QA/QC plan** should be a contract deliverable before acquisition: it lists every requirement in the spec, the test that demonstrates it, who performs the test, the data used, and the pass criterion. **Independent verification** — by the agency, a third party, or an internal team walled off from production — is the only credible way to test performance-based requirements; vendor self-reports are inputs, not conclusions. **Deviations** should be documented as they occur (weather, sensor failure, access denied), with the agreed disposition, because an undocumented deviation discovered at acceptance becomes a dispute ([Chapter 68](ch68-legal-issues.md)). Acceptance or rejection should be recorded against each requirement, not as a single verdict, so that partial remedies can be targeted. Finally, close the loop: a **post-project review** that records what the spec failed to anticipate is the raw material from which the next edition — of the national standard or your own template — is written. The USGS and NOAA both maintain public change logs for exactly this reason, and the best thing a reader can do with a new spec edition is read its change log first.

## Then & now

The **US National Map Accuracy Standards** of 1947 ⟨H⟩ tested maps, not data: 90 % of well-defined points within 1/30 inch at publication scale, 90 % of elevations within half a contour interval. **IHO S-44** followed in 1968 ⟨H⟩ with depth-accuracy tables for lead-line and single-beam soundings; its 4th edition (1998) introduced the $\sqrt{a^2+(bd)^2}$ form and 95 % confidence, the 5th (2008) tightened orders for multibeam, and the 6th (2020/2022) added the Exclusive order, the survey matrix, and explicit coverage and feature-search definitions. The **FGDC NSSDA** (1998) moved US topographic testing from scale to RMSE × 1.96 with 20 checkpoints; **NDEP** (2004) added the land-cover stratification that lidar demanded; the **USGS LBS** (2012) tied accuracy to density and classification; **ASPRS 2014** named classes by RMSE; and **ASPRS Ed. 2 / LBS 2024** retreated from 95 % statements, raised checkpoint counts, made vegetated accuracy a report, and introduced 3D accuracy. Aviation moved its numbers out of Annex 15 into PANS-AIM (2018) and tied them to DO-200B process assurance. The arc runs from testing the drawn contour to testing the surface statistically, and now to specifying the uncertainty each measurement carries — a trajectory the hydrographers reached first with TPU and the topographers are still completing.

## Mathematics

**S-44 uncertainty allowances.** For order parameters $(a, b)$ and depth $d$,

$$\mathrm{TVU}_{\max}(d) = \sqrt{a^2 + (b\,d)^2}, \qquad \mathrm{THU}_{\max}(d) = c + e\,d,$$

with $c$ and $e$ the horizontal constants (e.g., 5 m and 0.05 for Order 1a). A sounding is compliant when its modelled TPU at 95 % satisfies $\mathrm{TVU} \le \mathrm{TVU}_{\max}(d)$, where the TPU combines independent components in quadrature: $\mathrm{TVU}^2 = 1.96^2\,(\sigma_{\text{range}}^2 + \sigma_{\text{ssp}}^2 + \sigma_{\text{tide}}^2 + \sigma_{\text{heave}}^2 + \sigma_{\text{roll}}^2 + \sigma_{\text{draft}}^2 + \dots)$. At 10 m, Order 1a allows 0.516 m; Special allows 0.261 m; Exclusive 0.168 m.

**ASPRS classes and 95 % conversions.** For $n$ checkpoints with errors $e_i$, $\mathrm{RMSE}_z = \sqrt{\frac{1}{n}\sum e_i^2}$, mean error $\bar e$, and $\sigma_z = \sqrt{\frac{1}{n-1}\sum(e_i - \bar e)^2}$, so $\mathrm{RMSE}_z^2 \approx \sigma_z^2 + \bar e^2$. Under normality with negligible bias, $\mathrm{LE95} = 1.9600\,\mathrm{RMSE}_z$ and $\mathrm{LE90} = 1.6449\,\mathrm{RMSE}_z$; Edition 1 and the NSSDA used the former as "NVA at 95 %." For horizontal error with $\mathrm{RMSE}_x = \mathrm{RMSE}_y$, $\mathrm{RMSE}_r = \sqrt{2}\,\mathrm{RMSE}_x$, $\mathrm{CE95} = 1.7308\,\mathrm{RMSE}_r = 2.4477\,\mathrm{RMSE}_x$, and $\mathrm{CE90} = 1.5175\,\mathrm{RMSE}_r = 2.1460\,\mathrm{RMSE}_x$. ASPRS Ed. 2 also requires the checkpoint survey uncertainty $\sigma_{cp}$ to be included: $\mathrm{RMSE}_{z,\text{reported}} = \sqrt{\mathrm{RMSE}_{z,\text{obs}}^2 + \sigma_{cp}^2}$ (Ed. 2 §7 gives the conditions under which checkpoint error is small enough to be neglected; read that clause before applying the formula).

**Converting between conventions.** Between 90 % and 95 % in one dimension, $\mathrm{LE95}/\mathrm{LE90} = 1.9600/1.6449 = 1.1916$; in two dimensions, $\mathrm{CE95}/\mathrm{CE90} = 2.4477/2.1460 = 1.1406$. So ICAO Area 4 terrain (1 m at 90 %) ≈ 1.19 m at 95 % ≈ 0.61 m RMSE; S-44 Special at 10 m (0.261 m at 95 %) ≈ 0.133 m RMSE ≈ 0.219 m at 90 %. These hold only for normal, unbiased, independent errors; with bias $\bar e$, the 95 % absolute error bound is not $1.96\,\mathrm{RMSE}$ but approximately $|\bar e| + 1.96\,\sigma$, and with heavy tails (vegetation, breaklines) the empirical 95th percentile should be reported instead of any multiplier — which is why NDEP and ASPRS treat vegetated terrain by percentile.

**LBS density and accuracy.** Aggregate nominal pulse spacing relates to density by $\mathrm{ANPS} = 1/\sqrt{\rho}$ for $\rho$ pulses per square metre (0.71 m ↔ 2 pls/m²; 0.35 m ↔ 8 pls/m²). Density controls the number of ground returns per cell under canopy and hence the interpolation error of the DTM, not the per-point ranging accuracy; the spec's NVA requirement is tested on open ground and the density requirement is what protects accuracy elsewhere.

## Validation & uncertainty

A specification tells you what to test and how to report; it does not make the test valid. Five issues recur when specs meet real data.

**The test statistic is a sample.** With $n$ = 30 checkpoints, the 95 % confidence interval on an estimated RMSE$_z$ is roughly ±25 % (from the χ² distribution with 29 degrees of freedom: $\sqrt{29/45.7}$ to $\sqrt{29/16.0}$, i.e., 0.80 to 1.35 times the estimate). A product with true RMSE$_z$ = 0.10 m will fail a 0.10 m class about half the time, and one with 0.085 m will fail noticeably often. Contracts should recognize this with tolerance bands or larger $n$; analysts should report the interval. [Chapter 53](ch53-accuracy-assessment.md) gives the full treatment.

**Checkpoints sample the easy places.** NVA checkpoints are on open, flat, hard ground by design; the product's error there is the sensor's best case. The spec's answer — VVA on vegetated land cover — now yields a report rather than a verdict, so the user must read the VVA value and decide for themselves. Report both, with $n$ per stratum and the spatial distribution.

**TPU is a model, not a measurement.** S-44 compliance is demonstrated by propagated uncertainty from manufacturer sensor specifications and operator-entered values (sound-speed variability, tide uncertainty). Optimistic inputs produce compliant surveys with real errors larger than claimed; crosslines, reference-surface comparisons, and junction analyses are the empirical check, and HSSD's crossline requirement exists because TPU alone was found insufficient. Report the TPU inputs with the survey.

**Confidence conversions assume normality.** The multipliers above fail with bias and heavy tails. Test normality (or at least plot the error histogram and Q–Q plot) before quoting any converted figure; where the tails are heavy, give the empirical 95th percentile and say so.

**Specs test the product once.** Acceptance is at delivery; the surface and the reference frame move afterwards ([Chapter 37](ch37-time-scales-of-change.md), [Chapter 38](ch38-plate-motion-and-vlm.md)). State the acquisition epoch and the control epoch in the compliance statement, so that later users can judge validity.

> **Try it.** Evaluate a delivered DTM against ASPRS Ed. 2 / LBS 2024 conventions and ICAO 90 % conventions from the same checkpoint file, so the two statements can be compared honestly. Expected output: per-stratum $n$, bias, σ, RMSE$_z$ (with checkpoint σ included), empirical 90th and 95th percentiles of |error|, and a χ²-based interval on RMSE$_z$.

```python
import numpy as np, pandas as pd
from scipy.stats import chi2, shapiro

cp = pd.read_csv("checkpoints_with_dtm.csv")   # cols: cover, z_cp, sigma_cp, z_dtm
cp["e"] = cp.z_dtm - cp.z_cp
for cover, g in cp.groupby("cover"):
    n = len(g); e = g.e.values
    rmse_obs = np.sqrt(np.mean(e**2))
    rmse_rep = np.sqrt(rmse_obs**2 + np.mean(g.sigma_cp**2))   # ASPRS Ed. 2
    lo = rmse_obs*np.sqrt((n-1)/chi2.ppf(0.975, n-1))
    hi = rmse_obs*np.sqrt((n-1)/chi2.ppf(0.025, n-1))
    p90, p95 = np.percentile(np.abs(e), [90, 95])
    W, p = shapiro(e) if n >= 3 else (np.nan, np.nan)
    print(f"{cover:10s} n={n:3d} bias={e.mean():+.3f} sd={e.std(ddof=1):.3f} "
          f"RMSEz={rmse_rep:.3f} [{lo:.3f},{hi:.3f}] "
          f"P90={p90:.3f} P95={p95:.3f} 1.96RMSE={1.96*rmse_rep:.3f} shapiro_p={p:.2f}")
```

If `P95` and `1.96RMSE` differ by more than ~15 %, the normal multiplier is misleading for that stratum and the percentile should be the reported figure.

> **Uncertainty budget.** Where the stated allowance goes in a QL2 lidar acceptance (illustrative 1σ magnitudes on open ground; the spec allows RMSE$_z$ ≤ 0.10 m):
>
> | Component | 1σ | Note |
> |---|---|---|
> | Checkpoint survey (RTK/levelling) | 0.02–0.03 m | included in reported RMSE under Ed. 2 |
> | Lidar ranging + boresight | 0.03–0.05 m | from calibration, flight height |
> | Trajectory (GNSS/INS) | 0.03–0.06 m | dominant; worse under interference |
> | Geoid/datum transformation | 0.01–0.03 m | systematic over the project |
> | Interpolation to DTM cell at checkpoint | 0.01–0.03 m | slope- and density-dependent |
> | **RSS** | **≈ 0.05–0.09 m** | little margin below 0.10 m |

## Software

**Open source / free:** NOAA **HydrOffice QC Tools** and **Pydro** (free, NOAA) implement HSSD checks — grid QA, feature scans, TPU flags, crossline statistics, deliverable validation — and are the reference for HSSD compliance; **PDAL** and **lidR** scripted to LBS checks (density, swath overlap, classification counts, void detection); **xdem** and **demcoreg** for checkpoint and DEM-to-DEM accuracy; **MB-System** for crossline and reference-surface comparisons; **GDAL** for product-format checks (COG, BAG, GeoTIFF tags); QGIS plugins for checkpoint reporting — caveat: none emits a complete compliance report; you assemble it. **Commercial:** CARIS HIPS and QPS Qimera compliance and TPU tools (S-44/HSSD order checking, CUBE hypothesis statistics); Teledyne/TerraSolid **TerraScan/TerraMatch** for strip adjustment and LBS relative-accuracy tests; **LP360** QA and **GeoCue** for LBS/ASPRS reports; Esri ArcGIS Pro lidar QA tools — caveat: vendor "compliance reports" encode the vendor's reading of the spec and edition; confirm the edition and statistic in the output header.

## Standards & guides

This chapter is itself the tour; [Appendix D](../appendices/appendix-d-standards-index.md) holds the full index with editions and URLs. The principal documents, by issuer: IHO S-44 Ed. 6.1.0 (2022), C-13, S-67, B-11, B-12, S-100/S-101/S-102/S-104/S-111; NOAA OCS HSSD (current year) and Field Procedures Manual (online, living document); USACE EM 1110-2-1003 (2013) and EM 1110-1-1000 (2015); LINZ HYSPEC; CHS Hydrographic Survey Management Guidelines; AHO HIPP specifications; USGS Lidar Base Specification 2024 rev. A; ASPRS Positional Accuracy Standards Ed. 2 (2023; v2 2024) and addenda; ASPRS LAS 1.4 R15; FGDC NSSDA (1998); NDEP (2004); FEMA Guidelines and Standards (current); ICSM LiDAR Acquisition Specifications; NRCan CanElevation specifications; UK Environment Agency survey specifications; AHN specifications; ICAO Annex 15 and PANS-AIM Doc 10066, Doc 9881; RTCA DO-276C/ED-98C (2015), DO-200B/ED-76A (2015); FAA AC 150/5300-16/17/18; EUROCONTROL TOD Manual; FGCC (1984); NGS-58 (1997), NGS-59 (2008); ISO 17123 series; IGS and CORS guidelines; INSPIRE D2.8.II.1 v3.0 (2013); ISO 19157:2023; Copernicus DEM Product Handbook; MIL-PRF-89020B (2000); OGC CityGML 3.0.

## Pitfalls

- **Quoting the spec's class as the product's accuracy.** "QL2 data" means the contract required RMSE$_z$ ≤ 0.10 m, not that this tile achieved it → read the project accuracy report; check $n$ and strata.
- **Mixing 95 %, 90 %, and RMSE across specs.** Each domain has its own convention → convert explicitly (×1.96, ×1.645) and only after checking normality; otherwise report percentiles.
- **Applying LBS classification or hydro-flattening rules to bathymetry, or S-44 feature detection to a DTM.** Specs are surface-specific → map requirements to surfaces before writing the project spec.
- **Treating HSSD annual changes as cosmetic.** Grid resolutions, attributes, and deliverable formats change → read the change log; cite the year.
- **Assuming an S-44 order is a property of the survey.** Orders are selected by the office; a "Special Order survey" is one *required* to meet Special → ask what was specified and what was demonstrated.
- **Accepting TPU compliance without empirical checks.** TPU inputs can be optimistic → require crosslines, reference surfaces, junction statistics.
- **Testing accuracy only where it is easy.** Open-ground checkpoints flatter the product → report VVA with $n$; map checkpoint locations.
- **Treating 30 checkpoints as decisive.** The RMSE interval is ±25 % → include tolerance or more points; report the interval.
- **Specifying "or better" without a test.** Unverifiable → name the statistic, sample, and threshold.
- **Citing two standards for the same quantity.** Conflicting conventions → say which governs.
- **Letting the spec define the surface for you.** Bridges, culverts, water, overhangs differ by spec → define the surface in the project spec ([Chapter 32](ch32-dsm-to-dtm.md)).
- **Forgetting the epoch.** Acceptance at delivery says nothing about validity in five years → record acquisition and control epochs in the compliance statement.

## Key takeaways

- A specification encodes a domain's definition of fitness; read its definitions and test procedures before its tables.
- S-44 bundles uncertainty, feature detection, and coverage into *selected* orders; the LBS bundles accuracy and density into Quality Levels; ASPRS classes are pure accuracy statements; ICAO areas are zones with 90 % requirements — these are different kinds of object.
- Hydrographic specs test a per-sounding uncertainty model; topographic specs test a gridded surface against checkpoints; aviation specs add integrity and process assurance. Translate between them only with stated assumptions.
- The 2023–2024 revisions (ASPRS Ed. 2, LBS 2024 rev. A) moved to RMSE-only reporting, 30+ checkpoints including checkpoint uncertainty, and VVA as a report — know which edition your contract cites.
- Confidence-level conversions (1.645σ, 1.960σ) are valid only for unbiased, normal, independent errors; otherwise report empirical percentiles.
- Specs are silent on effective resolution, correlated error, and temporal validity; add them to your project spec if the use case needs them.
- Write project specs by reference — standard, edition, class — and add only the surface definitions, acquisition windows, checkpoint plans, deliverables, and remedies the standard lacks.
- Compliance requires a QA/QC plan, independent verification, recorded deviations, requirement-by-requirement acceptance, and a post-project review that feeds the next edition.

## References

- ASPRS, 2015. ASPRS positional accuracy standards for digital geospatial data (Edition 1, 2014). *Photogrammetric Engineering & Remote Sensing*, 81(3):A1–A26.
- ASPRS, 2023. *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (August 2023); Version 2 with addenda, 2024. Baton Rouge: ASPRS.
- FGDC, 1998. *Geospatial Positioning Accuracy Standards, Part 3: National Standard for Spatial Data Accuracy*. FGDC-STD-007.3-1998.
- Heidemann, H. K., 2018. *Lidar Base Specification* (ver. 1.3). USGS Techniques and Methods 11-B4. (lineage of LBS 2024 rev. A, online)
- USGS, 2024. *Lidar Base Specification 2024 rev. A*. National Geospatial Program (online).
- IHO, 2022. *Standards for Hydrographic Surveys*, S-44 Edition 6.1.0. Monaco: International Hydrographic Organization. (Ed. 6.0.0, 2020)
- IHO, 2005 (with updates). *Manual on Hydrography*, C-13. Monaco: IHO.
- IHO, 2020. *Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts*, S-67 Ed. 1.0.0.
- NOAA Office of Coast Survey, current year. *Hydrographic Surveys Specifications and Deliverables*. Silver Spring: NOAA.
- NOAA Office of Coast Survey, 2020 (with updates). *Field Procedures Manual*. Silver Spring: NOAA.
- US Army Corps of Engineers, 2013. *Hydrographic Surveying*, EM 1110-2-1003. Washington: USACE.
- US Army Corps of Engineers, 2015. *Photogrammetric and LiDAR Mapping*, EM 1110-1-1000.
- ICAO, 2018 (and later amendments). *Procedures for Air Navigation Services — Aeronautical Information Management*, Doc 10066 (PANS-AIM); ICAO *Annex 15 — Aeronautical Information Services*, 16th ed. and amendments.
- ICAO, 2010. *Guidelines for Electronic Terrain, Obstacle and Aerodrome Mapping Information*, Doc 9881.
- RTCA, 2015. *User Requirements for Terrain and Obstacle Data*, DO-276C (EUROCAE ED-98C).
- RTCA, 2015. *Standards for Processing Aeronautical Data*, DO-200B (EUROCAE ED-76A).
- FAA, 2009. *General Guidance and Specifications for Submission of Aeronautical Surveys to NGS: Field Data Collection and Geographic Information System (GIS) Standards*, AC 150/5300-18B, with Change 1 (2011); remains the active edition.
- NDEP, 2004. *Guidelines for Digital Elevation Data*, Version 1.0. National Digital Elevation Program.
- Zilkoski, D. B., D'Onofrio, J. D., and Frakes, S. J., 1997. *Guidelines for Establishing GPS-Derived Ellipsoid Heights (Standards: 2 cm and 5 cm)*. NOAA Technical Memorandum NOS NGS-58.
- Zilkoski, D. B., Carlson, E. E., and Smith, C. L., 2008. *Guidelines for Establishing GPS-Derived Orthometric Heights*. NOAA Technical Memorandum NOS NGS-59.
- Federal Geodetic Control Committee, 1984. *Standards and Specifications for Geodetic Control Networks*. Rockville: NOAA.
- INSPIRE Thematic Working Group Elevation, 2013. *D2.8.II.1 Data Specification on Elevation — Technical Guidelines*, v3.0. European Commission Joint Research Centre.
- US Bureau of the Budget, 1947. *United States National Map Accuracy Standards*. Washington: GPO.
- Department of Defense, 2000. *Performance Specification: Digital Terrain Elevation Data (DTED)*, MIL-PRF-89020B.
- Airbus Defence and Space. *Copernicus DEM Product Handbook*, GEO1988-CopernicusDEM-SPE-002, Issue 5.0.

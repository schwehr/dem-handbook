# Chapter 3 — From use to requirement: fitness for use, constraints, and appropriate resolution

> **Part I — Why elevation? Uses and users.** Having catalogued the uses on land (Chapter 1) and under water (Chapter 2), this chapter shows how to turn a use into a requirement that can be written down, costed, and tested — and why no single dataset can satisfy them all.

**In this chapter.** "Is this DEM good?" is not a question; "is this DEM good *for this*?" is. This chapter gives you a formal framework for **fitness for use** built on the ISO 19157 data-quality elements, then decomposes a requirement into its dimensions — surface type, nominal and effective resolution, vertical and horizontal accuracy with its spatial structure, completeness, currency, datum, uncertainty metadata, licensing, and format. It contrasts the constraints imposed by eight very different uses to show that they genuinely conflict, so that a product optimised for one is wrong for another. It then treats two decisions that practitioners most often get backwards: whether a **local-only** dataset on a project datum is enough or **integration** with national and global frameworks is mandatory, and how **resolution** changes what a dataset is appropriate for, including the rule that a finer grid is not a finer survey. You will learn the difference between relative and absolute accuracy and between internal consistency and external truth, and finish with a template for writing a requirement with acceptance criteria, a sample design, and deliverables that a contractor can meet and an auditor can check.

## 3.1 Fitness for use, formally

The phrase **fitness for use** entered geographic information science through Chrisman (1991), who argued that there is no such thing as the accuracy of a dataset in the abstract: error has meaning only relative to a purpose, and the same data may be excellent for one decision and dangerous for another. Veregin (1999) organised the idea into the familiar data-quality parameters — accuracy, precision, resolution, consistency, completeness — each applicable to space, time, and attribute. The international standard that now operationalises this is **ISO 19157** (*Geographic information — Data quality*, 2013; revised as ISO 19157-1:2023), which defines a set of **data-quality elements**:

| ISO 19157 element | Sub-elements | What it means for a DEM |
|---|---|---|
| Completeness | commission, omission | voids, missing thin objects, spurious features; coverage gaps |
| Logical consistency | conceptual, domain, format, topological | nodata handling, value ranges, hydrologic connectivity, grid registration |
| Positional accuracy | absolute external, relative internal, gridded-data position | vertical/horizontal accuracy against truth; strip-to-strip agreement; cell alignment |
| Thematic accuracy | classification correctness, non-quantitative, quantitative attribute | land/water mask, point classification, surface-type labelling |
| Temporal quality | accuracy of measurement, temporal consistency, validity | acquisition date, epoch of the frame, currency against change |
| Usability | — | the explicit element for "fit for *this* use" |

Each element is reported as a **measure** (e.g. RMSE$_z$, percentage of voids), evaluated by a **procedure** (direct external, direct internal, or indirect) and given a **result** with a **scope** (the whole dataset, a tile, a land-cover class). ISO 19157's usability element is the formal hook: a conformance statement says that for a *specified* use, with *specified* thresholds on *specified* elements, the dataset does or does not conform. That is the structure this chapter uses.

The distinction between **"true"** and **"useful"** underlies everything that follows. A DEM is never true; it is a model with error. It is useful when the error it has does not change the decision it supports. A 30 m DSM with a 5 m RMSE$_z$ is useful for model orography at 10 km, useless for a floodplain, and actively misleading for sea-level-rise exposure (Gesch 2018). A 10 cm-accurate lidar DTM on a project datum is useful for a cut/fill quantity and useless for merging into a regional flood model until its datum is resolved. Fitness for use is the mapping from the error you have to the decision you are making; the rest of the chapter is about making that mapping explicit.

> **Definitions that bite.** *Accuracy* and *resolution* are independent axes, and *quality* is a third thing. A 1 m grid resampled from a 30 m DEM has 1 m resolution in name, 30 m (or worse) effective resolution, and exactly the accuracy of its source — plus interpolation error. A 1 m lidar DTM with a 2 m vertical datum blunder has excellent resolution and precision and is wrong by 2 m everywhere. "High-quality" in a catalogue entry tells you nothing until the element, measure, procedure, and scope are stated ([Chapter 4](ch04-names-and-definitions.md), [Chapter 5](ch05-error-and-uncertainty.md)).

## 3.2 Requirement dimensions

A complete requirement specifies a value, or a tolerance, for each of the following dimensions. Any dimension left unspecified will be decided by whoever produces the data — on cost grounds.

**Surface type.** DTM (bare earth), DSM (first reflective surface), both, nDSM/CHM (their difference), a *reflective surface* consistent with a particular sensor (for terrain-referenced navigation), a *conservative* surface (never shallower/lower than truth, for navigation and TAWS), or a *topobathymetric* seamless surface. The requirement must also say how **buildings, bridges, culverts, water bodies, and vegetation** are treated, because "bare earth" has at least four defensible definitions at a bridge ([Chapter 32](ch32-dsm-to-dtm.md), [Chapter 34](ch34-water-in-dems.md)).

**Nominal and effective resolution.** Nominal resolution is the cell size or post spacing; **effective resolution** is the smallest feature the data actually resolve, which depends on the measurement footprint, point density, filtering, and interpolation ([Chapter 44](ch44-resolution-and-sampling.md)). Specify the latter by the smallest feature that must be resolved and its minimum dimension, and derive the cell size from it (§3.5); specify the source **point density** (pulses/m²) or footprint rather than the grid alone. The USGS Lidar Base Specification does this with Quality Levels: QL1 ≥ 8 pulses/m², QL2 ≥ 2 pulses/m², QL3 ≥ 0.5 pulses/m², each paired with an accuracy class.

**Vertical and horizontal accuracy and its spatial structure.** State the statistic (RMSE$_z$, LE95, NVA/VVA, TVU/THU), the confidence level, the land-cover or depth stratification, the test procedure, and the minimum number of checkpoints. State separately the tolerances for **bias** (mean error) and for **spatially correlated error** (strip offsets, tilts, long-wavelength undulations), because the common statistics do not constrain them and because they dominate volumes, change detection, and hydrologic integrals. State horizontal accuracy, which lidar and bathymetric products often omit — yet on a 30° slope a 0.5 m horizontal error is a 0.29 m vertical error (§Mathematics).

**Completeness.** Maximum allowable void fraction and maximum void size; whether voids are filled and how the fill is flagged; whether thin tall objects (towers, wires) must be captured, which drives an obstacle database rather than a grid; feature-detection size for bathymetry; treatment of water surfaces. Completeness is the dimension most often left to default and most often the cause of failure in safety uses.

**Currency and epoch.** Acquisition window; maximum age at delivery; the reference-frame epoch (for ITRF-based coordinates in regions moving at centimetres per year); seasonal constraints (leaf-off, snow-free, low tide); and whether a change-detection baseline is needed ([Chapter 6](ch06-time-as-coordinate.md), [Chapter 37](ch37-time-scales-of-change.md)).

**Datum.** Horizontal datum and realization; vertical datum and geoid model (e.g. NAVD 88 via GEOID18; EGM2008; LAT with the named separation model; ellipsoidal with the frame and epoch); units; and the transformation path from the acquisition reference (always ellipsoidal for GNSS-based systems) to the delivery datum, with its uncertainty ([Chapter 9](ch09-vertical-datums.md)).

**Uncertainty metadata.** Whether a per-cell uncertainty layer is required (as BAG/S-102 do), or an accuracy report by stratum, or both; the error model used; the checkpoint data themselves as a deliverable.

**Licensing and cost.** Open licence (CC0, CC-BY, public domain), restricted, or proprietary; redistribution of derived products; and the budget, which is a real dimension because it caps all of the others ([Chapter 28](ch28-reducing-cost.md), [Chapter 68](ch68-legal-issues.md)).

**Format.** LAS/LAZ 1.4 with classification codes; COPC; Cloud-Optimized GeoTIFF with specified nodata, compression, overviews, and tiling; BAG with uncertainty; NetCDF/Zarr with CF conventions; and the metadata standard (ISO 19115, STAC) ([Chapter 47](ch47-file-formats.md), [Chapter 49](ch49-metadata.md)).

<!-- figure: Figure 3.1 — Radar/spider chart of the ten requirement dimensions, with overlaid polygons for four uses (flood modelling, ship navigation, mine volumetrics, web visualisation) showing where each is demanding and where it is indifferent. -->

## 3.3 Constraints from uses, contrasted

The requirement dimensions are not independent of the use; the use decides which one dominates. Eight uses, chosen for the way they conflict:

**Hydrologic modelling — connectivity over absolute accuracy.** A watershed model is insensitive to a uniform 1 m datum offset and extremely sensitive to a single 0.3 m error at a culvert that turns a channel into a dam. The dominant requirement is *logical consistency* (hydrologic connectivity after enforcement), followed by effective resolution adequate to channels and embankments, with absolute accuracy a distant third. A DTM that fails NVA by 5 cm but is hydro-enforced beats one that passes and is not ([Chapter 61](ch61-hydrology.md)).

**Ship navigation — shoalest point, no false deeps.** The requirement is asymmetric: an error toward shallow costs cargo capacity; an error toward deep costs a ship. Hence conservative surfaces, feature detection, 95 % TVU, and a datum (chart datum) chosen so that the real water is almost always deeper than charted. Unbiased statistics are the wrong statistics; the requirement is on the *tail* ([Chapter 62](ch62-navigation-and-charting.md)).

**Aviation obstacles — completeness of thin tall objects.** A 300 m guyed mast is a 2 m-wide object with 0.01 m-wide guy wires; no grid resolves it, and a DSM that captures the mast's top in one cell is worthless if a resampling step removes it. The requirement is *completeness of commission* in a vector obstacle database with stated vertical accuracy at the top of the object, and the DEM's role is to supply the ground height beneath it ([Chapter 33](ch33-wires-and-thin-structures.md)).

**Sea-level-rise exposure — decimetre vertical accuracy and the datum.** The flattest land on Earth is the land in question, and the signal (0.3–1 m of SLR over decades) is of the order of most DEMs' error. Gesch (2018) shows that the minimum SLR increment that a DEM can resolve is about twice its LE95, and that exposure counts are meaningless without an *orthometric-to-tidal* datum conversion whose error is included. The requirement is bias control, LE95 ≲ 0.2 m, and a documented tidal transformation.

**Volumetrics — bias dominates.** For a stockpile, pit, dredge reach, or landfill, the random error averages away over thousands of cells and the volume error is bias times area (worked examples in Chapters 1 and 2). The requirement is on *mean error between epochs* — centimetres — which is a requirement on control, datum consistency, and calibration, not on sensor noise ([Chapter 65](ch65-mining-landfills-earthworks.md)).

**Change detection — co-registration and precision.** Differencing two DEMs cancels common errors and amplifies independent ones. The requirement is sub-cell horizontal co-registration (a 0.5-cell shift on a 20° slope produces a spurious elevation change of $0.5\,d\tan 20°$), matched effective resolution (otherwise the difference map shows the resolution difference), and a stated **minimum detectable change** derived from the propagated uncertainty, including its spatial correlation ([Chapter 41](ch41-change-detection.md)).

**Visualisation — plausibility.** A hillshade must not show tile seams, spikes, striping, or terraces; it may be smoothed, super-resolved, or lightly invented, and the viewer will prefer the result. The requirement is the absence of visible artefacts, which is a *different* and sometimes *opposite* requirement from unbiased estimation ([Chapter 57](ch57-visualizing-dems.md)).

**Machine-learning training data — label consistency.** A model trained to predict a DTM from a DSM, or to classify points, learns whatever definition the labels embody. If half the training tiles define "ground" under bridges as the deck and half as the riverbed, the model learns to be uncertain at bridges; if the training lidar is leaf-off and the inference imagery leaf-on, the model learns a season. The requirement is *definitional consistency* and documented provenance across the training set, which is a thematic-accuracy and lineage requirement rather than a positional one ([Chapter 43](ch43-traditional-vs-ml.md)).

Table 3.1 summarises the dominant dimension for each.

| Use | Dominant dimension | Secondary | Nearly indifferent to |
|---|---|---|---|
| Hydrologic modelling | logical consistency (connectivity) | effective resolution at channels and embankments | absolute datum offset |
| Ship navigation | tail accuracy (95 % TVU), feature detection, conservative bias | chart datum fidelity | mean error being zero |
| Aviation obstacles | completeness (thin tall objects) | vertical accuracy at object top | DTM texture |
| SLR exposure | bias and LE95 ≲ 0.2 m; tidal↔orthometric datum | DTM (not DSM) | horizontal accuracy |
| Volumetrics | bias between epochs | project control | absolute datum |
| Change detection | co-registration; matched effective resolution; correlated error | precision | absolute accuracy |
| Visualisation | artefact-free plausibility | effective resolution | accuracy, datum |
| ML training | label/definition consistency; lineage | coverage diversity | absolute accuracy |

The table makes the chapter's central argument: these requirements are not points on a single axis of "quality" that more money moves you along. They pull in different directions. A conservative navigation surface fails the volumetrics requirement; a hydro-enforced DTM with burned-in culverts fails the ML-training requirement for "ground as measured"; a visually smoothed DEM fails change detection. One dataset cannot serve everyone, and the honest response is to derive *several products* from one measurement set, each labelled with the use it serves.

> **Case file.** When Kulp and Strauss (2019) replaced SRTM with a neural-network-corrected DTM (CoastalDEM) in a global coastal-flooding exposure analysis, the estimated population living on land below the projected 2050 annual flood level roughly tripled relative to SRTM-based estimates. The underlying data had not changed; what changed was that the surface type (DSM with canopy and building bias → approximate DTM) was now closer to what the use assumed. The same study illustrates the ML-training constraint: CoastalDEM was trained where lidar existed (largely the United States and Australia) and its residual errors elsewhere are themselves uncertain.

## 3.4 Local-only versus integrated datasets

Every elevation project chooses — usually without noticing — between two kinds of reference. A **local-only** dataset is referenced to a project datum: one or more benchmarks or a base station whose coordinates are *assumed*, with all measurements made relative to them. An **integrated** dataset is tied to the national or global framework — a national vertical datum through published benchmarks or a geoid model, a horizontal frame through CORS/RTK networks or PPP, with an epoch — so that it can be merged with other data and reused by strangers. The choice is a trade between cost and reach, and both directions of error are common: demanding global integration for a quarry's monthly stockpile survey, and delivering a local-only survey into a regional flood model.

**When a project datum and relative accuracy suffice.** Volumetrics between epochs on the same site; construction stake-out against a design on the same datum; deformation monitoring where only change matters; agricultural levelling; archaeological site recording; any product consumed only by people who also have the benchmarks. In all of these the quantity of interest is a *difference* or a *shape*, and a constant datum offset cancels. The requirements are then on **relative accuracy** (repeatability, internal consistency, §3.6) and on the *stability and documentation* of the local reference: the benchmark must not move, must be recoverable, and must be described well enough that a successor can re-occupy it. The silent cost is future integration: when the quarry closes and the land becomes a housing development, every survey it ever made is on a datum nobody can recover unless the benchmark was also tied to the national network at least once.

**When integration is mandatory.** Whenever the data will be merged with anyone else's: flood mapping (the model spans jurisdictions), coastal and topobathymetric work (land and sea datums must meet), charting, aviation, national mapping, any product that will be archived for reuse, anything that crosses a reference-frame boundary, any legal or regulatory submission where elevations are compared to a statutory datum (base flood elevation, zoning height, UNCLOS isobath), and change detection whose baseline was integrated. Integration is also mandatory when the *absolute* value matters: SLR exposure, reservoir stage, levee freeboard.

**What each costs.** Table 3.2 lists the elements and their typical magnitudes; the figures are indicative and depend heavily on country and site.

| Cost element | Local-only | Integrated |
|---|---|---|
| Control | one or two project benchmarks; a local base station | ties to published benchmarks and/or CORS network; GNSS static sessions of hours; or PPP with convergence; checkpoints on independent control |
| Transformations | none (or a single offset) | horizontal frame + epoch; geoid model; tidal separation model near water; unit conversions; each with documented uncertainty |
| Documentation | benchmark description; base coordinates | full lineage: frame, realization, epoch, geoid version, transformation grids, software versions |
| Accuracy achievable | relative: cm; absolute: unknown | absolute: typically 2–5 cm vertical with good geoid and control; worse where geoid models are poor |
| Typical cost share | a few per cent of the survey | 5–20 % of a small survey; negligible fraction of a large one |
| Failure mode | unrecoverable datum; cannot merge | wrong transformation applied; frame mismatch; "integrated" in name only |

The cheapest insurance is a **hybrid**: do the work on a project datum for day-to-day efficiency, but tie the project benchmarks to the national framework once, with a documented transformation, so that the dataset *can* be integrated later. A single static GNSS session on each benchmark and a published geoid model convert a local survey into an integrable one for a fraction of a day's effort. The reverse — trying to recover a datum years later from a lost benchmark — frequently costs more than the original survey.

> **Rule of thumb.** If the deliverable will ever be *added to* or *compared with* data you did not collect, integrate. If it will only ever be *subtracted from* data you did collect on the same control, a project datum suffices — but tie it to the framework once anyway. The rule fails when the "same control" moves (subsidence, earthquake, benchmark disturbance; [Chapter 38](ch38-plate-motion-and-vlm.md), [Chapter 39](ch39-earthquakes-volcanoes-landslides.md)) — then even differences need an external reference.

## 3.5 How product resolution changes what is appropriate

Resolution is the dimension users most often specify and least often justify. Three questions determine the appropriate cell size: what is the **smallest feature** that must be resolved; which **derivative** (slope, curvature, flow direction) will be computed; and what does each halving of cell size **cost** in acquisition, storage, and processing?

**Smallest feature.** Sampling theory gives the preview (full treatment in [Chapter 44](ch44-resolution-and-sampling.md)): to resolve a feature of width $w$ you need a cell size $d \le w/2$ (Nyquist), and in practice $d \le w/3$ to $w/5$ to resolve its *shape* rather than merely detect its presence, because real DEMs are sampled with a footprint, filtered, and interpolated, so the effective resolution is coarser than the cell. Hengl (2006) formalised the choice of pixel size from the data's inherent scale (point spacing, contour spacing, terrain complexity) and recommended a range rather than a single value, with the finest legitimate pixel set by the sampling density: for a point density of $\rho$ points per unit area, a cell size finer than about $1/\sqrt{\rho}$ to $0.5/\sqrt{\rho}$ is interpolation, not measurement.

**Derivatives.** Slope and curvature are differences of neighbouring cells divided by distance, so noise in them grows as cell size shrinks, while true terrain slope on a landscape tends to *increase* with finer resolution as short-wavelength relief is admitted (Zhang and Montgomery 1994 found that mean slope and derived hydrologic quantities changed systematically from 2 m to 90 m grids). There is therefore an optimum: coarse enough that the noise-induced slope is below the terrain slopes of interest, fine enough that the terrain's own features are resolved. Curvature, the second derivative, is more sensitive still, and third-order quantities (curvature change along flow paths) are often noise at any resolution finer than several times the point spacing.

**Cost.** Halving the cell size quadruples cells and storage; achieving genuinely finer *effective* resolution means quadrupling point density, which means roughly doubling or quadrupling flight time depending on sensor and overlap. For bathymetry it means working at a smaller fraction of water depth or using a vehicle nearer the bottom ([Chapter 20](ch20-sonar.md), [Chapter 28](ch28-reducing-cost.md)).

**"A finer grid is not a finer survey."** Resampling a 30 m DEM to 1 m produces a 1 m grid with a 30 m (or coarser) effective resolution, smooth interpolation surfaces between the original posts, slope values that are too low (interpolation smooths) except at the original post locations where they may be spuriously high, and an *appearance* of detail that misleads every downstream user. Super-resolution ([Chapter 45](ch45-super-resolution.md)) can produce plausible detail, but plausible detail is not measured detail; it is fit for visualisation and unfit for anything in Table 3.1's upper rows unless validated for that use.

Table 3.3 is a decision table. It assumes a well-made product whose effective resolution is close to its cell size; for resampled products, use the *source* resolution in the first column.

| Cell size (effective) | Resolves features ≥ | Typical source | Appropriate for | Inappropriate for |
|---|---|---|---|---|
| 0.1–0.25 m | 0.3–1 m (kerbs, walls, dune cusps, dredge ridges) | drone SfM/lidar, TLS, MLS, shallow multibeam, AUV | engineering as-built, archaeology, scour, UXO, rooftop solar | regional anything (cost, volume) |
| 0.5–1 m | 2–5 m (channels, levees, terraces, landslide scarps, buildings) | airborne lidar QL1/QL2, topobathy lidar, port multibeam | flood modelling, hydro-enforcement, forestry CHM, urban nDSM, landslide inventory, S-44 Special Order charting | ice-sheet mass balance (unnecessary), model orography |
| 2–5 m | 10–25 m (streams, roads, large buildings, bedforms) | lidar QL3, aerial stereo, shelf multibeam | catchment hydrology, slope-stability susceptibility, wind-resource flow models, habitat mapping | culvert-scale hydraulics, building-scale solar, obstacle completeness |
| 10–30 m | 50–150 m (valleys, ridges, large landslides, canyons) | national DTMs, Copernicus/SRTM/ALOS, FABDEM | regional geomorphology, $V_{S30}$ proxies, soil covariates, orthorectification of 10–30 m imagery, basin-scale SLR screening | floodplain inundation lines, levee crests, SLR exposure counts, anything needing a DTM where the product is a DSM |
| 90–450 m | 0.5–2 km | SRTM 3″, GEBCO, SRTM15+, MERIT | global hydrology routing, tsunami propagation (not inundation), continental orography, Article 76 at basin scale | coastal inundation, habitat patches, navigation |
| 1–100 km | 5–500 km | filtered DEMs | NWP/climate model orography, gravity-wave drag parameters | everything else |

<!-- figure: Figure 3.2 — Four-panel sequence of the same levee and floodplain at 0.5 m, 2 m, 10 m, and 30 m cell size, with the levee crest profile across each and the modelled flood extent, showing the crest height loss and the resulting spurious inundation at coarse resolution. -->

> **Worked example.** A levee crest is 4 m wide and stands 2.5 m above the floodplain. On a 1 m DTM (effective resolution ≈ 1.5 m) the crest is resolved; its maximum height in the grid is within a few centimetres of truth. Resampled to 10 m by averaging, with side slopes of 1:2 (each spanning 5 m horizontally): a cell centred on the crest contains 4 m of crest at 2.5 m and 3 m of each side slope descending from 2.5 m to 1.0 m (mean 1.75 m), so the cell mean is $(4 \times 2.5 + 6 \times 1.75)/10 = 2.05$ m; a cell whose edge coincides with the crest edge contains one full 5 m side slope (mean 1.25 m) and 5 m of floodplain, so its mean is $0.625$ m. The levee's grid height now depends on where the grid happened to fall, between about 0.6 and 2.05 m. At 30 m, the whole cross-section ($4 \times 2.5 + 2 \times \tfrac{1}{2} \times 5 \times 2.5 = 22.5$ m²) is spread over 30 m: a 0.75 m bump. A 2 m flood that the real levee holds is now modelled as overtopping. The remedy is not a finer *grid* but preserving the crest as a **breakline** or enforcing crest heights from the source points when coarsening ([Chapter 59](ch59-vector-data.md), [Chapter 31](ch31-interpolation-and-gridding.md)).

## 3.6 Relative vs absolute accuracy; internal consistency vs external truth

**Absolute accuracy** is the agreement of a dataset's coordinates with an external reference — the national datum, the ITRF, chart datum — measured by independent checkpoints of higher accuracy. **Relative accuracy** is the agreement of the dataset with itself: between adjacent strips, between overlapping swaths, between two points a known distance apart, between two epochs on the same control. ISO 19157 names these *absolute (external)* and *relative (internal)* positional accuracy. They are measured differently, fail differently, and matter to different uses.

Relative accuracy is usually much better than absolute. A lidar block may have strip-to-strip vertical agreement of 2–3 cm while its absolute accuracy, limited by the GNSS solution and the geoid model, is 5–10 cm. A multibeam survey may be internally consistent to a few centimetres and absolutely wrong by 0.3 m because the tide gauge was 20 km away. A drone SfM model can be internally beautiful and tilted by a metre across the site because the camera's lens model absorbed a systematic error — the "doming" that ground control points exist to detect ([Chapter 22](ch22-photogrammetry-sfm.md)).

**Internal consistency** is relative accuracy generalised to include logical consistency: do the strips agree, do the tiles align, do the water surfaces come out flat, do the rivers flow downhill, do the contours close, do the two epochs agree where nothing changed? Internal consistency can be checked exhaustively from the data alone and is cheap. **External truth** — checkpoints, benchmarks, higher-order surveys — is expensive, sparse, and the only thing that detects a common-mode error. A dataset can be perfectly internally consistent and uniformly wrong; conversely, checkpoints that pass at 30 locations say nothing about strip offsets 2 km from the nearest checkpoint. Both are needed, and a requirement must say which it is asking for. The common failure is to specify absolute accuracy only (because it is what the standards template contains), accept a product that passes at the checkpoints, and discover the strip offsets in the hillshade.

The relation between the two is also where many "accuracy" numbers are misread. If a product reports RMSE$_z$ = 0.10 m from checkpoints on open flat ground, that figure bounds the random-plus-bias error *at open flat ground near checkpoints*. It says nothing about the forest (VVA), the slopes (where horizontal error leaks into vertical), the void fills, or the strip 5 km from any checkpoint. A requirement that cares about those places must ask for them explicitly — stratified checkpoints, strip-overlap statistics, a void map — or accept not knowing.

## 3.7 Writing a requirement that can be tested

A requirement is testable when a third party, given the deliverables and the specification, can determine conformance without asking the producer what they meant. The template below produces one; [Appendix G](../appendices/appendix-g-checklists.md) carries a checklist version and [Chapter 70](ch70-specifications-guided-tour.md) shows how the major published specifications fill it in.

1. **Purpose statement.** One paragraph naming the use(s) in the vocabulary of Chapters 1–2, the decision the data support, and the consequence of error in each direction. This paragraph decides every threshold that follows and is the only place "fitness for use" is argued rather than measured.
2. **Surface definition.** DTM/DSM/both/conservative/seamless; explicit rules for buildings, bridges, culverts, water, vegetation, snow; the classification scheme (e.g. ASPRS LAS classes) and which classes form the surface.
3. **Spatial extent and resolution.** Area of interest with buffer; smallest feature to be resolved and its dimension; derived cell size; minimum point density or footprint; breaklines required and where; treatment of the land–water interface.
4. **Accuracy.** For each stratum (land cover, slope class, depth band): statistic, confidence level, threshold, and the test procedure (ASPRS 2023 for land; S-44 crosslines and target trials for water); separate thresholds for bias and for strip/swath relative agreement; horizontal accuracy and how it is tested.
5. **Completeness.** Maximum void fraction and size; flagging of filled areas; object-detection size (water) or obstacle capture policy (air); coverage/overlap requirement.
6. **Temporal.** Acquisition window and seasonal constraints; maximum age; epoch of the reference frame; whether a baseline for change detection is included.
7. **Datum and transformations.** Horizontal and vertical datums with realization/geoid/separation model and version; units; the required transformation documentation.
8. **Acceptance criteria.** The conformance rule: which tests, which thresholds, what happens on failure (re-fly, reprocess, reject, accept with documented deviation). State whether the thresholds apply to the whole dataset or per tile, and how outliers are treated (ASPRS Ed. 2 no longer removes them; earlier practice did).
9. **Sample design.** Number of checkpoints (ASPRS Ed. 2 gives minimums scaling with project area; roughly 30 per stratum is a floor for a meaningful RMSE), their spatial distribution (well distributed, including far from control), their land-cover stratification, their independence from the producer's control, and their required accuracy (at least three times better than the threshold being tested). For water: crossline spacing, target trials, independent water-level checks.
10. **Deliverables.** The product in the specified format; the uncertainty layer or accuracy report with checkpoint coordinates and residuals; the control and transformation documentation; the void/fill and water masks; the acquisition metadata (dates, sensor, trajectory quality); the processing lineage; the licence.

Two tests of whether the requirement is well written: (a) could it be met by a product that is useless for the stated purpose? If so, a dimension is missing (the classic case is "1 m DEM, 10 cm RMSE" met by a DSM). (b) Does it require anything you cannot verify with the sample design and budget you have? If so, the requirement is a wish; either fund the verification or lower the claim. Requiring 5 cm absolute accuracy with checkpoints of 5 cm accuracy, or requiring VVA with no checkpoints in vegetation, is the second failure.

> **Try it.** Compute the horizontal shift that explains a vertical mismatch on slopes — the cheapest co-registration diagnostic there is, and a test that a requirement for "horizontal accuracy" can be met on a DEM without planimetric features. With Python, numpy, and rasterio, following the principle of Nuth and Kääb (2011) as implemented in xdem:
>
> ```python
> import numpy as np, rasterio
> with rasterio.open("dem_new.tif") as a, rasterio.open("dem_ref.tif") as b:
>     z1, z2 = a.read(1).astype(float), b.read(1).astype(float)
>     d = a.res[0]
> dh = z1 - z2
> gy, gx = np.gradient(z2, d)                      # reference slope components
> slope = np.hypot(gx, gy)
> aspect = np.arctan2(-gx, gy)                      # radians, 0 = north
> ok = np.isfinite(dh) & (slope > 0.05) & (np.abs(dh) < 20)
> # Model: dh / tan(slope) = a*cos(aspect) + b*sin(aspect) + c
> A = np.c_[np.cos(aspect[ok]), np.sin(aspect[ok]), np.ones(ok.sum())]
> y = dh[ok] / slope[ok]
> a_, b_, c_ = np.linalg.lstsq(A, y, rcond=None)[0]
> print(f"shift north={a_:.2f} m, east={b_:.2f} m; dz bias={c_*np.mean(slope[ok]):.2f} m")
> ```
>
> Expected outcome: for two well co-registered DEMs the fitted shifts are below a fraction of a cell. A shift of 0.5–2 m with a sinusoidal dependence of $\Delta h/\tan\beta$ on aspect is the signature of a horizontal mis-registration that no checkpoint on flat ground would reveal — and a reason to include slope-stratified checks in the requirement. The `xdem` package (`xdem.coreg.NuthKaab`) does this robustly and iteratively.

## Then & now

Fitness for use was not always a question anyone could ask. When a national mapping agency produced one topographic series at one scale, "the map" was the only elevation product, and users adapted their questions to it: engineers knew that a 1:24,000 sheet with a 20 ft contour interval would not design a drainage ditch, and did their own levelling. Requirements were implicit in the product line.

- **Accuracy standards for maps (1940s–1990s).** The US National Map Accuracy Standards (1947) stated vertical accuracy as a fraction of the contour interval tested at 90 %; the equivalent national standards elsewhere were similar. Accuracy was a property of the sheet, tested once, and resolution was the scale. This is the regime in which Chrisman (1991) and Veregin (1999) wrote: they were arguing that this single number could not serve the new digital uses.
- **Digital standards (1998–2014).** The FGDC National Standard for Spatial Data Accuracy (1998) replaced the contour-interval rule with RMSE and 95 % statistics for digital data; ASPRS lidar guidelines (2004) added land-cover stratification (the "fundamental", "supplemental", and "consolidated" vertical accuracies that became NVA/VVA); IHO S-44 Ed. 4 (1998) introduced the $\sqrt{a^2 + (bd)^2}$ TVU formula and Ed. 5 (2008) the TPU philosophy. ISO 19113/19114/19138 (2002–2006) defined the data-quality elements later consolidated into ISO 19157 (2013). Requirements became explicit, but still mostly about absolute positional accuracy.
- **Quality levels and program specifications (2012–).** The USGS Lidar Base Specification (2012; v2.1 2020; 2024 online) tied point density, accuracy, classification, and hydro-flattening into named Quality Levels, so that a user could specify "QL2" and mean a bundle of dimensions; the National Enhanced Elevation Assessment (Dewberry 2012) had derived the QL needed by each of several hundred uses. ASPRS Positional Accuracy Standards (2014; Ed. 2, 2023) added horizontal accuracy for lidar, checkpoint minimums by project area, and removed the practice of discarding outliers.
- **Uncertainty as a deliverable (2000s–).** BAG (2006) and S-102 made per-node uncertainty part of the product; TanDEM-X shipped a height-error map; ICESat-2 ships per-photon confidence. The requirement conversation moved from "how accurate is it" to "how well does it know how accurate it is."
- **Fitness for use for machine learning (2020s).** Training-data consistency, provenance, and label definitions became requirement dimensions as ML products (FABDEM, CoastalDEM, learned ground filters) entered operational use; the data-quality elements of ISO 19157 are being stretched to cover them, and the open problem of how to validate a learned product for a use it was not trained for is where [Chapter 73](ch73-open-problems.md) picks up.

## Mathematics

Three results from later chapters are needed now to make the resolution and accuracy arguments quantitative. Notation: $d$ cell size, $w$ feature width, $\sigma_z$ standard deviation of vertical error (assumed independent between cells unless stated), $\beta$ terrain slope angle, $\Delta z$ vertical error, $\Delta x$ horizontal error.

**Nyquist preview.** A surface sampled at spacing $d$ can represent, without aliasing, only spatial wavelengths $\lambda \ge 2d$. A feature of width $w$ (half a wavelength for a ridge or channel) therefore needs

$$d \le \frac{w}{2}$$

to be *detected*, and practical experience with footprint, filtering, and interpolation suggests $d \le w/3$ to $w/5$ to represent its *height* with small bias. For a point cloud with density $\rho$ (points/m²) the mean spacing is $s \approx 1/\sqrt{\rho}$, and a grid finer than $s$ is interpolation; Hengl (2006) proposes selecting $d$ between about $0.5\,s$ (finest legitimate) and $2\,s$ (coarsest without loss). Full treatment: [Chapter 44](ch44-resolution-and-sampling.md).

**Slope error versus cell size.** For a central-difference slope estimate along one axis, $p = (z_{i+1} - z_{i-1})/(2d)$, with independent errors of standard deviation $\sigma_z$ at each cell,

$$\sigma_p = \frac{\sqrt{2}\,\sigma_z}{2d} = \frac{\sigma_z}{\sqrt{2}\,d}.$$

This is the per-component noise; the Horn 3 × 3 kernel used by `gdaldem` weights six cells (1, 2, 1 on each side, divided by $8d$), so for independent errors its variance is $12\sigma_z^2/(64 d^2)$ and $\sigma_p = \sqrt{12}\,\sigma_z/(8d) \approx 0.43\,\sigma_z/d$ — a factor $\sqrt{3/8} \approx 0.61$ smaller than the central difference ([Chapter 5](ch05-error-and-uncertainty.md) treats correlated errors). Numerically, $\sigma_z$ = 0.10 m on a 1 m grid gives $\sigma_{\tan\beta}$ ≈ 0.07 per component for the central difference, i.e. about 4° of slope noise; on a 10 m grid, 0.4°. For curvature (second differences divided by $d^2$) the noise scales as $\sigma_z/d^2$ — a hundredfold increase per decade of refinement — which is why curvature maps from fine lidar grids are smoothed first.

**Vertical ↔ horizontal error on slopes.** A horizontal displacement $\Delta x$ of a DEM relative to truth on terrain of slope $\beta$ produces an apparent vertical error

$$\Delta z = \Delta x \tan\beta,$$

and conversely a vertical error $\Delta z$ is indistinguishable from a horizontal error

$$\Delta x = \frac{\Delta z}{\tan\beta}.$$

The first form says that horizontal accuracy *is* vertical accuracy on slopes: 1 m horizontal error on a 30° slope is 0.58 m vertical; on a 5° slope, 0.09 m. It is why ASPRS Ed. 2 requires lidar horizontal accuracy to be stated and why checkpoints for vertical accuracy are placed on flat ground (to isolate $\sigma_z$). The second form says that vertical error becomes horizontal uncertainty of any *contour or boundary* drawn on the surface — a flood line, a shoreline, an isobath: 0.2 m on a 1:1,000 floodplain is 200 m. The two forms together explain why the same product can be "accurate to 10 cm" and place a flood boundary within only ±100 m.

**Combining them.** A vertical requirement $\sigma_z^{req}$ on a product used for slope on terrain where slopes of $\beta_{min}$ must be distinguished from flat implies a minimum cell size

$$d \ge \frac{\sigma_z}{\sqrt{2}\,\tan\beta_{min}} \cdot k,$$

where $k$ ≈ 2–3 is the signal-to-noise ratio you want. For $\sigma_z$ = 0.1 m and $\beta_{min}$ = 2° (tan = 0.035), $d \ge 0.1/(1.414 \times 0.035) \times 2 \approx 4$ m. The same data can be delivered at 1 m for feature visibility and at 4 m for slope analysis; both are legitimate, and the requirement should say which.

## Validation & uncertainty

Validating fitness for use means validating *against the requirement*, dimension by dimension, rather than computing one RMSE. The procedure is the ISO 19157 evaluation applied to the requirement written in §3.7.

**How requirement errors arise.** Most unfit products are not inaccurate; they are *mis-specified*. The commonest failures, in rough order of frequency observed in procurement reviews: surface type unspecified (DSM delivered, DTM needed, or hydro-treatment undefined); resolution specified as cell size without density or feature size (resampled product accepted); accuracy specified as a single RMSE without strata, bias limit, or relative-accuracy limit (strip offsets accepted); datum specified by name without realization or geoid model (0.1–0.5 m offsets in merging); currency unspecified (leaf-on lidar, or a survey predating the construction it was meant to capture); completeness unspecified (voids filled silently); and verification unfunded (requirement cannot be tested, so is not).

**How they propagate.** A mis-specified dimension propagates as a *systematic* error into every use that depends on it — a DSM-for-DTM error is a bias equal to canopy height, a datum error is a uniform offset, a resolution error is a low-pass filter on everything derived — and systematic errors do not shrink with sample size. The propagation rules in Chapter 1's Table 1.2 and the Mathematics above translate each into the use's output: datum offset $b$ → flood boundary shift $b/\tan\beta$; resampled resolution → slope bias and lost crest heights; missing uncertainty layer → inability to compute minimum detectable change.

**How to test — a conformance procedure.**

1. *Document review.* Compare the delivered metadata against each requirement dimension; a dimension absent from the metadata is non-conformant until shown otherwise.
2. *Surface-type audit.* Profiles across forest, buildings, bridges, water; difference against any trusted reference stratified by land cover; mean difference by canopy-height class.
3. *Resolution audit.* Measure effective resolution directly — e.g. the width of the narrowest resolved linear feature, or the spectral roll-off of the DEM compared with a finer reference ([Chapter 44](ch44-resolution-and-sampling.md)); confirm point density from the point cloud, not the grid.
4. *Accuracy test.* Independent checkpoints by stratum, with RMSE, mean error, and 95 % statistic per ASPRS Ed. 2 or S-44; strip/swath overlap statistics for relative accuracy; the slope-aspect co-registration test (§3.7 Try it) for horizontal error.
5. *Completeness test.* Void map and fill flags; object-detection trials; obstacle comparison against an independent list.
6. *Temporal test.* Acquisition dates against the window and against known change events; leaf/snow/tide state from imagery of the same dates.
7. *Datum test.* Occupy at least one benchmark of the target datum with the product's own positioning chain; compare the product at that point; verify the geoid/separation model version in the processing logs.
8. *Use-level test.* Where the budget allows, run the use: delineate the watershed and compare with the mapped network; model the design flood and compare with a recorded event; compute the dredge volume two ways. Nothing validates fitness for use like the use.

> **Uncertainty budget.** What a "10 cm RMSE$_z$" lidar DTM actually delivers to three uses on a 1:500 floodplain (slope 0.002), approximate 1σ magnitudes:
>
> | Error component | Magnitude (1σ) | Flood boundary (÷ tan β) | Slope at 1 m (× 1/(√2 d)) | 10 ha volume (× A) |
> |---|---|---|---|---|
> | Random noise | 0.07 m | averages out along boundary | 0.05 (≈ 3°) | 0.07 × 10⁵ / √10⁵ ≈ 22 m³ |
> | Strip offset (relative) | 0.04 m | 20 m | step artefact | up to 4,000 m³ if one strip |
> | Geoid / datum bias | 0.05 m | 25 m | none | 5,000 m³ |
> | Canopy/low-veg residual (VVA) | 0.15 m in vegetation | 75 m in vegetated reaches | spurious roughness | 15,000 m³ if vegetated |
> | **Combined (RSS)** | **≈ 0.10 m (open) / 0.18 m (veg)** | **≈ 50–90 m** | **≈ 3°** | **dominated by bias terms** |
>
> The same product is fit for a 1 m hillshade, marginal for the flood line (±50–90 m at 1σ), and fit for the volume only if the datum and strip biases are controlled — which is why the requirement must name the use.

**What to report.** A conformance statement per ISO 19157 for the stated use: each dimension, the measure, the procedure, the result, the threshold, pass/fail, and the scope. Attach the checkpoints and residuals, the strip-overlap statistics, the void and water masks, and the datum-transformation log. State what was *not* tested and therefore not claimed. [Chapter 53](ch53-accuracy-assessment.md) gives the statistical detail and [Chapter 54](ch54-evaluating-others-data.md) the procedure when you inherit data with none of this.

## Software

**Open source:** PDAL (`pdal info --stats`, `filters.hag_nn`, density rasters) to verify point density, classification, and returns; GDAL (`gdalinfo -stats`, `gdaldem`, `gdalcompare.py`, `gdal_calc.py`) for grid audits, differencing, and slope; xdem (Python) for co-registration (Nuth–Kääb, ICP), DEM differencing, and spatially correlated uncertainty estimation — the closest open tool to a fitness-for-use workbench for change detection; WhiteboxTools and SAGA for hydrologic-connectivity checks (fill, breach, flow accumulation); QGIS for profiling and visual audits; PROJ (with `projinfo` and the vertical transformation grids) for datum-path verification; MB-System for bathymetric crossline analysis; R packages `terra` and `gstat` for stratified accuracy statistics and variograms of error. **Free but closed:** NOAA VDatum for US tidal–orthometric–ellipsoidal transformation and its uncertainty; the ASPRS accuracy-assessment spreadsheets accompanying the 2023 standard. **Commercial:** Teledyne CARIS (TPU, CUBE, crosslines) for hydrographic conformance; Terrasolid TerraScan/TerraMatch for strip adjustment and lidar QC; GeoCue for lidar project QA; Esri ArcGIS Pro for stratified checkpoint tools. A caveat for all: a tool's default accuracy report is written to the standard the vendor had in mind, which may not be the dimension your use needs. See [Chapter 71](ch71-software-landscape.md).

## Standards & guides

- **ISO 19157:2013 / ISO 19157-1:2023, *Geographic information — Data quality*** — the elements, measures, and conformance structure used throughout this chapter.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)** — NVA/VVA, horizontal accuracy for lidar, checkpoint numbers and distribution, accuracy classes.
- **USGS Lidar Base Specification** (online edition, 2024; v2.1 2020) — Quality Levels QL0–QL3 as bundled requirements.
- **IHO S-44 Ed. 6.x (2020/2022)** — orders as bundled requirements for bathymetry (TVU, THU, feature detection, coverage).
- **ICAO Annex 15 and PANS-AIM (Doc 10066)** — terrain and obstacle data areas 1–4 with post spacing, accuracy, and confidence requirements.
- **FEMA Guidelines and Standards for Flood Risk Analysis and Mapping — Elevation Guidance** (November 2022 revision; continuously maintained) — the flood-study requirement expressed in QLs.
- **FGDC-STD-007.3-1998, National Standard for Spatial Data Accuracy** — historical RMSE/95 % basis.
- **ISO 19115-1:2014, Metadata** and **ISO 19131:2022, Data product specifications** — how to write the requirement down as a product specification.

## Pitfalls

- **Specifying "1 m DEM" without point density, surface type, and accuracy test.** The phrase is satisfied by a resampled DSM. Detect by reading the point density and surface definition in the metadata; avoid by specifying feature size, density, and surface explicitly.
- **Requiring accuracy you cannot verify.** A 3 cm vertical requirement with 5 cm checkpoints is untestable. Detect by comparing checkpoint accuracy to the threshold (need ≥ 3×); avoid by funding verification or relaxing the claim.
- **Demanding global integration for a purely local volume job.** Adds cost and introduces transformation error into a difference that would have cancelled. Detect by asking whether anything external will ever be compared; avoid with a project datum plus a one-time tie.
- **Delivering a local-only dataset into an integrated use.** The flood model, chart, or archive acquires an unknown offset. Detect at merge time by seam steps; avoid by requiring the datum path in the deliverables.
- **Confusing resolution with accuracy.** A 0.5 m grid is assumed better than a 2 m one regardless of source. Detect by checking source density and RMSE; avoid by treating the two as separate dimensions in the requirement.
- **Resampling to a finer grid and calling it higher resolution.** Effective resolution is unchanged, slope is biased, crests are lost. Detect by spectral or feature-width tests; avoid by stating effective resolution and source.
- **Specifying only absolute accuracy.** Strip offsets, tilts, and seams pass the checkpoints. Detect by overlap statistics and hillshade inspection; avoid by adding a relative-accuracy threshold.
- **Testing where it is convenient.** Checkpoints on roads near the office; none in forest, floodplain, or far from control. Detect from the checkpoint map; avoid by stratified, well-distributed sample design written into the requirement.
- **Leaving the bridge/culvert/water rule to the producer.** Each producer's default differs; the hydrology breaks. Detect by profiling at crossings; avoid by writing the rule.
- **Treating ISO 19157 conformance as a certificate rather than a statement about a use.** Conformance to one profile says nothing about another use. Detect by reading the scope; avoid by writing the usability element for your use.
- **Forgetting the epoch.** The frame moved, the ground moved, the leaves grew. Detect by checking dates against the use's currency need; avoid by specifying the window and the frame epoch.
- **Letting cost decide the unspecified dimensions.** Whatever is left blank is delivered at the cheapest defensible interpretation. Avoid by filling in all ten dimensions, even with "not required".

## Key takeaways

- Fitness for use is a mapping from the error you have to the decision you support; a dataset is never "accurate" in the abstract, only adequate or inadequate for a named purpose.
- A requirement has ten dimensions — surface, nominal resolution, effective resolution, accuracy with its spatial structure, completeness, currency/epoch, datum, uncertainty metadata, licence/cost, format — and any left blank will be decided on cost grounds by someone else.
- Uses genuinely conflict: conservative versus unbiased, connectivity versus accuracy, completeness versus resolution, plausibility versus truth. Derive multiple products from one measurement set and label each.
- Local-only versus integrated is a choice with consequences for control, transformations, documentation, and reuse; tie a local datum to the framework once even when you do not need to.
- Justify resolution by the smallest feature and the derivative you need, not by what is available; a finer grid is not a finer survey, and derivative noise grows as $\sigma_z/d$ (slope) and $\sigma_z/d^2$ (curvature).
- Vertical and horizontal error are interchangeable on slopes: $\Delta z = \Delta x \tan\beta$ and $\Delta x = \Delta z / \tan\beta$; the second turns centimetres of vertical error into tens of metres of boundary uncertainty on floodplains.
- Relative accuracy and internal consistency are cheap to test and cannot detect common-mode error; absolute accuracy is expensive and sparse and cannot detect strip-scale error; a requirement needs both.
- A requirement must be a testable statement: purpose, dimensions, acceptance criteria, sample design, deliverables — and it must not ask for anything the sample design cannot verify.

## References

- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0. American Society for Photogrammetry and Remote Sensing.
- Chrisman, N. R. (1991). The error component in spatial data. In: Maguire, D. J., Goodchild, M. F., Rhind, D. W. (eds.), *Geographical Information Systems: Principles and Applications*, Vol. 1, pp. 165–174. Harlow: Longman.
- Dewberry (2012). *National Enhanced Elevation Assessment — Final Report*. Prepared for the U.S. Geological Survey. Fairfax, VA: Dewberry.
- FGDC (1998). *Geospatial Positioning Accuracy Standards, Part 3: National Standard for Spatial Data Accuracy*. FGDC-STD-007.3-1998. Federal Geographic Data Committee.
- Fisher, P. F., Tate, N. J. (2006). Causes and consequences of error in digital elevation models. *Progress in Physical Geography* 30(4):467–489.
- Gesch, D. B. (2018). Best practices for elevation-based assessments of sea-level rise and coastal flooding exposure. *Frontiers in Earth Science* 6:230.
- Guth, P. L., Van Niekerk, A., Grohmann, C. H., Muller, J.-P., Hawker, L., Florinsky, I. V., Gesch, D., Reuter, H. I., Herrera-Cruz, V., Riazanoff, S., López-Vázquez, C., Carabajal, C. C., Albinet, C., Strobl, P. (2021). Digital elevation models: Terminology and definitions. *Remote Sensing* 13(18):3581.
- Heidemann, H. K. (2018). *Lidar Base Specification* (ver. 2.1). U.S. Geological Survey Techniques and Methods 11-B4. (Superseded by the online edition, 2024.)
- Hengl, T. (2006). Finding the right pixel size. *Computers & Geosciences* 32(9):1283–1298.
- IHO (2020, 2022). *S-44 Standards for Hydrographic Surveys*, Edition 6.0.0 / 6.1.0. Monaco: International Hydrographic Organization.
- ISO (2013). *ISO 19157:2013 Geographic information — Data quality*. Geneva: International Organization for Standardization. (Revised as ISO 19157-1:2023.)
- Kulp, S. A., Strauss, B. H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications* 10:4844.
- Mesa-Mingorance, J. L., Ariza-López, F. J. (2020). Accuracy assessment of digital elevation models (DEMs): A critical review of practices of the past three decades. *Remote Sensing* 12(16):2630.
- Nuth, C., Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere* 5(1):271–290.
- Polidori, L., El Hage, M. (2020). Digital elevation model quality assessment methods: A critical review. *Remote Sensing* 12(21):3522.
- Veregin, H. (1999). Data quality parameters. In: Longley, P. A., Goodchild, M. F., Maguire, D. J., Rhind, D. W. (eds.), *Geographical Information Systems: Principles and Technical Issues*, 2nd ed., Vol. 1, pp. 177–189. New York: Wiley.
- Wechsler, S. P. (2007). Uncertainties associated with digital elevation models for hydrologic applications: a review. *Hydrology and Earth System Sciences* 11:1481–1500.
- Zhang, W., Montgomery, D. R. (1994). Digital elevation model grid size, landscape representation, and hydrologic simulations. *Water Resources Research* 30(4):1019–1028.

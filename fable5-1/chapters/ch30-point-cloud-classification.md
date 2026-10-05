# Chapter 30 — Point-cloud cleaning, classification, and ground extraction

> **Part VII — From sensor data to products.** The second processing chapter: how georeferenced points become labelled points, and why "ground" is a decision that must be documented, tuned per terrain, and validated per class before any DTM is built.

**In this chapter.** A point cloud straight from georeferencing contains blunders, atmospheric returns, birds, multipath, and—under everything—the ground. You will be able to remove or flag noise without removing real features, read and apply the ASPRS LAS classification codes and the hydrographic accepted/rejected convention, and choose among the main families of ground filters: slope-based, morphological (PMF), progressive TIN densification (Axelsson), robust interpolation (Kraus & Pfeifer), multiscale curvature (MCC), simple morphological (SMRF), cloth simulation (CSF), and deep networks trained on OpenGF-scale benchmarks. You will understand what each filter's parameters mean geometrically, how they fail on steep slopes, levees, dunes, dense cities, and closed canopy, and how Type I (ground removed) and Type II (object kept) errors translate into DTM bias. You will be able to evaluate a classification with confusion-matrix metrics and with stratified manual QA, understand the hydrographic analog in CUBE/CHRT hypothesis review, audit manual edits, and write the deliverable statement that says what "ground" meant in this project.

## 30.1 Outlier and noise handling

Noise in an elevation point cloud comes in a few recognisable species, and the filter that removes one may remove or ignore another.

**High isolated points** are returns from birds, insects, aerosols, cloud wisps, and—in single-photon and Geiger-mode systems—solar background and detector dark counts; they sit metres to hundreds of metres above the surface with no neighbours. **Low isolated points** come from multipath (a pulse reflected off a wall and then the ground, arriving late and placed below the surface), from specular returns on water or glass, and from timing errors; they are more dangerous than high noise because a ground filter, by construction, trusts low points. **Multiple-time-around (MTA) returns** are mis-assigned real returns: at pulse rates where several pulses are in flight, a return attributed to the wrong outgoing pulse is displaced by one unambiguous-range interval (150 m at 1 MHz), producing coherent sheets of false surface at MTA-zone boundaries over steep terrain ([Chapter 18](ch18-topographic-lidar.md)). The multibeam equivalents are **fliers** (isolated soundings from bubble sweep-down, fish, or sidelobe detections) and **blunders** (structured errors from a bad sound-velocity profile, a motion-sensor dropout, or a mis-timed tide) ([Chapter 20](ch20-sonar.md)).

The standard tools are statistical and geometric. A **statistical outlier filter** computes, for each point, the mean distance to its $k$ nearest neighbours, fits a global mean $\mu$ and standard deviation $\sigma$ of those mean distances, and flags points whose value exceeds $\mu + m\sigma$ (PDAL `filters.outlier` with `method=statistical`; typical $k$ = 8–12, $m$ = 2–3). A **radius outlier filter** flags points with fewer than $n$ neighbours within radius $r$. An **extended local minimum (ELM)** filter (PDAL `filters.elm`) targets low noise specifically: it grids the cloud, finds the lowest point in each cell, and flags it as noise if it lies more than a threshold below the next-lowest point in the cell—a cheap guard against the single low outlier that would otherwise anchor a ground surface. Full-waveform and photon-counting data need density-based approaches (DBSCAN-style clustering along the vertical, as in the ICESat-2 ATL08 ground-finding algorithm) because the signal-to-noise ratio is too low for neighbour statistics on individual points.

Two rules of practice follow. First, run low-noise detection before ground filtering; a filter that has already adopted a low outlier as ground will build a pit around it. Second, **flag, do not delete**: ASPRS classes 7 (low noise) and 18 (high noise) exist so the decision can be reviewed, and the "withheld" flag marks points that all processing should ignore but the file should keep. A statistical filter on a sparse cloud will also remove the few ground returns under dense canopy—precisely the points that make the DTM there—so inspect what was removed by land cover before accepting it.

> **Try it.** Flag low and high noise in a LAZ tile, keeping the points. Expected outcome: noise points receive class 7 or 18; the point count of the output equals the input; `pdal info --stats` on the output shows the class histogram.
>
> ```json
> {
>   "pipeline": [
>     "tile.laz",
>     {"type": "filters.elm", "cell": 10.0, "threshold": 1.0, "class": 7},
>     {"type": "filters.outlier", "method": "statistical",
>      "mean_k": 10, "multiplier": 3.0, "class": 7},
>     {"type": "filters.assign",
>      "value": ["Classification = 18 WHERE Classification == 7 && HeightAboveGround > 2"]},
>     {"type": "writers.las", "filename": "tile_noise_flagged.laz",
>      "minor_version": 4, "dataformat_id": 6}
>   ]
> }
> ```
>
> The `HeightAboveGround` dimension requires a prior `filters.hag_nn` or `filters.hag_dem` stage against a provisional ground; in practice run noise flagging, a first ground pass, HAG, and then separate low from high noise. The point of the exercise is the histogram: if class 7 exceeds a few tenths of a percent of points, or is concentrated in forest, the filter is removing signal.

## 30.2 Classification schemes and flags

The ASPRS LAS specification defines the classification codes that nearly all topographic point clouds use. LAS 1.4 (R15, 2019) point data record formats 6–10 use an 8-bit class field (0–255, with 0–63 reserved for the standard), separate from the flag bits; legacy formats 0–5 have only a 5-bit field (0–31) sharing a byte with the flags. The standard classes that matter for DEMs:

| Code | Class | DEM relevance |
|---|---|---|
| 0 | Created, never classified | Should not appear in a deliverable |
| 1 | Unclassified | Everything not otherwise assigned; may include low vegetation, cars, walls |
| 2 | Ground | The DTM source; its meaning is project-defined (Section 30.8) |
| 3, 4, 5 | Low, medium, high vegetation | Height tiers (commonly 0–0.5 m, 0.5–2 m, > 2 m, but the breaks are project-defined) |
| 6 | Building | Roofs and walls; DSM source, DTM exclusion |
| 7 | Low point (noise) | Must be excluded from gridding |
| 9 | Water | Returns from water surfaces; usually excluded from the DTM and replaced by hydro-flattening |
| 10 | Rail | |
| 11 | Road surface | Ground-like; some specs keep roads in class 2 |
| 13, 14, 15, 16 | Wire – guard (shield), wire – conductor, transmission tower, wire – structure connector | [Chapter 33](ch33-wires-and-thin-structures.md) |
| 17 | Bridge deck | Excluded from DTM, included in DSM ([Chapter 32](ch32-dsm-to-dtm.md)) |
| 18 | High noise | Must be excluded from gridding |
| 20 | Ignored ground (breakline proximity) | USGS LBS uses this for ground points near hydro breaklines |
| 19, 21, 22 | Overhead structure, snow, temporal exclusion | LAS 1.4 R14 (2019) additions for points that are real but not terrain of record |
| 40–45 | Bathymetric classes (LAS Domain Profile for Topo-Bathy Lidar) | Bathymetric point, water surface, derived water surface, submerged object, IHO S-57 object, no-bottom-found-at |

The four **flag bits** carry decisions orthogonal to class. **Synthetic** marks points created rather than measured (e.g. points on a hydro-flattening breakline). **Key-point** marks a point a thinning algorithm should retain. **Withheld** marks a point all processing should ignore but the file should keep—the correct destination for noise. **Overlap** (LAS 1.4) marks points in swath overlap; it is a hint, not a deletion order, and tools differ in whether they honour it. Confusing "overlap" with "withheld" has removed a great many good points from a great many DTMs.

> **Definitions that bite.** Class 1 "Unclassified" is not "unprocessed." In most deliverables it means "not ground, building, water, or any other class we were asked to label"—so it holds cars, low vegetation, fences, walls, and construction. A DSM built from "all points except noise" includes them; one built from classes 2–6 and 9 does not; the two differ by a car's height on every street. Vendor-specific reuses of codes (class 8 "model key-point" and class 12 "overlap" in LAS 1.1–1.3; user-defined 64–255) make it worse; read the project's classification report, not just the code table.

Hydrography uses a different and simpler convention: every sounding is **accepted** or **rejected**, with rejection reasons recorded (manual, filter, outside survey area, etc.) in formats such as the Generic Sensor Format (GSF) and in CARIS/Qimera project databases. A rejected sounding stays in the file. Because the chart is shoal-biased, the asymmetry is reversed from topographic lidar: a falsely rejected shoal sounding is a navigational hazard, while a falsely accepted deep sounding is merely conservative. Topo-bathy lidar straddles the conventions, using LAS classes 40–45 for the bathymetric part and the topographic classes above water.

## 30.3 Ground filtering algorithms

Every ground filter rests on an assumption about how terrain differs from objects. The assumptions differ, and so do the failure modes. Reviews by Sithole & Vosselman (2004) and Meng, Currit & Zhao (2010) organise the field; the summary below follows the lineage from geometric rules to simulated physics to learned models.

### 30.3.1 Slope-based filters (Vosselman 2000)

Vosselman's filter formalises the intuition that terrain slopes are bounded: a point $p$ is not ground if some nearby point $q$ lies lower by more than a maximum allowed difference $\Delta h_{\max}(d)$ for their horizontal separation $d$. The function $\Delta h_{\max}(d)$ is a morphological structuring element—a cone for a constant slope limit, or a kernel estimated from training data—and the filter is a grey-scale erosion with that element. It fails where terrain is steeper than the kernel allows: cliffs, terraces, levee sides, and quarry faces are eroded as if they were buildings.

### 30.3.2 Morphological filters: PMF (Zhang et al. 2003)

The **progressive morphological filter** applies a grey-scale opening (erosion then dilation; see Mathematics) to a minimum-binned surface with a window that grows geometrically, $w_k = 2 b^k + 1$ cells, flagging points whose elevation drops by more than a scale-dependent threshold $dh_k = s\,(w_k - w_{k-1})\,c + dh_0$, where $s$ is a terrain slope parameter, $c$ the cell size, and $dh_0$ an initial threshold. Small windows remove cars and shrubs; large windows remove buildings; the growing threshold lets terrain whose relief exceeds that of small objects survive. The key parameters are the maximum window (which must exceed the largest building's smallest dimension—50–100 m in industrial areas), $s$, and $dh_0$. PMF's weakness is that one slope parameter governs an entire tile; hilly terrain with large flat-roofed buildings forces an impossible compromise.

### 30.3.3 Progressive TIN densification (Axelsson 2000)

Axelsson's algorithm, the engine of TerraScan's ground routine, starts from seed points—the lowest point in each large cell, with the cell larger than the largest building—builds a Delaunay TIN, and iteratively adds candidates that satisfy two criteria relative to the triangle containing them: the **angle** between the triangle plane and the line from each vertex to the candidate below a threshold (typically 6–10°), and the **distance** from candidate to plane below a threshold (typically 0.5–1.5 m). Each iteration densifies the TIN and evaluates the criteria against smaller triangles. It handles discontinuities better than slope filters because the angle is measured against the local facet. Its failures are at seed selection (a large building with no ground in its cell yields a roof seed) and in steep terrain where the angle criterion rejects legitimate ground; operational implementations add heuristics such as an edge-length rule that relaxes the angle for small triangles and terrain mirroring across breaks.

### 30.3.4 Robust interpolation (Kraus & Pfeifer 1998)

Kraus and Pfeifer's filter fits a surface by linear prediction to all points, computes residuals, and re-weights points asymmetrically—points far above the surface get low weight, points below keep high weight—then refits; the iteration converges toward the lower envelope of the data. A hierarchical version (Pfeifer et al. 2001) runs coarse to fine so that large buildings are removed at coarse scales. It produces a DTM and a classification together, with the fit residual as a quality indicator; it needs ground returns everywhere at the coarsest scale and is sensitive to the weight-function parameters.

### 30.3.5 Multiscale curvature (MCC; Evans & Hudak 2007)

MCC, designed for forested terrain, interpolates a thin-plate spline through the current ground candidates, removes points more than a curvature tolerance $t$ (default 0.3 m) above it, and repeats across three scales ($\lambda$, $1.5\lambda$, $2\lambda$, with $\lambda$ near the point spacing) until convergence. It performs well under canopy but, like all curvature filters, shaves sharp convex features: levee crests, dune crests, road embankments.

### 30.3.6 Simple morphological filter (SMRF; Pingel, Clarke & McBride 2013)

SMRF reworked PMF with a smaller parameter set and a different final step. It builds a minimum surface, applies a progressive opening with a linearly growing window and a slope-based threshold (as in PMF), then—unlike PMF—uses the resulting provisional surface to interpolate a DTM and classifies the original points by their elevation difference from it with a threshold that increases with local slope: $\text{thr} = t_0 + s\cdot\text{slope}$. The published defaults (cell 1 m, slope 0.15, window 18 m, elevation threshold 0.5 m, scalar 1.25) performed competitively on the ISPRS test and the method's five parameters map directly to terrain intuition: `slope` is the steepest terrain you believe in, `window` is the largest object you want removed, `threshold` is the height of a thing that is not ground. PDAL's `filters.smrf` is a faithful implementation and the usual open-source starting point.

### 30.3.7 Cloth simulation filtering (CSF; Zhang et al. 2016)

CSF inverts the point cloud and drops a simulated cloth onto it: a grid of particles connected by springs, each pulled by gravity and stopped when it hits an (inverted) point. The cloth drapes over inverted buildings and canopy—now below it—and settles onto the inverted ground. Points within a distance threshold of the final cloth are ground. The parameters are the cloth resolution (grid spacing, typically 0.5–2 m), the **rigidness** (1, 2, or 3: how resistant the cloth is to bending, with higher values for flat terrain and lower for steep), the number of iterations, the classification threshold (0.5 m default), and a "slope post-processing" switch that relaxes the cloth near steep edges. CSF's virtue is that its parameters are few and intuitive and it runs fast; its weakness is the same as all lower-envelope methods—low noise anchors the cloth, and under dense canopy the cloth drapes on the lowest vegetation returns where no ground returns exist. It is implemented in CloudCompare, PDAL (`filters.csf`), and lidR.

### 30.3.8 Deep learning (KPConv, RandLA-Net, OpenGF)

Point-based deep networks learn the features that rule-based filters encode by hand. **KPConv** (Thomas et al. 2019) defines convolution kernels on points in continuous space; **RandLA-Net** (Hu et al. 2020) uses random sampling with local feature aggregation to process millions of points efficiently. Trained on the **OpenGF** benchmark (Qin et al. 2021; Section 30.5), such networks reach overall accuracies above 97 % and ground IoU in the mid-90s on in-distribution test tiles, with errors more uniformly distributed across terrain types than any single parameter set of a rule-based filter achieves. Two cautions govern their use. They are trained on a particular sensor density, land cover, and labelling policy, and degrade when any of these change—a network trained where "ground" includes levees will reproduce that choice elsewhere, whether or not the new project specifies it. And their decisions are not explainable by a parameter a reviewer can defend; the audit trail is the training set and the validation statistics, which must be delivered with the product ([Chapter 43](ch43-traditional-vs-ml.md)).

<!-- figure: Figure 30.1 — Cross-section through a levee with closed canopy on one side, a building on the other, and a car on the crest road, showing the ground surface estimated by PMF, SMRF, Axelsson TIN densification, and CSF; annotations mark where each filter shaves the crest, keeps low vegetation, or anchors on a low outlier. -->

## 30.4 Parameter sensitivity by terrain and density; Type I/II trade-off

Every filter has a knob that trades **Type I errors** (true ground points rejected as objects) against **Type II errors** (object points accepted as ground), in Sithole and Vosselman's convention. The two have different geometric consequences. Type I errors remove data: the DTM is interpolated over a longer distance, and on convex features (crests, embankments) the interpolation is biased low. Type II errors add false surface: the DTM is biased high by roughly the height of the accepted object. The cost asymmetry depends on use—a flood model would rather lose a few crest points than gain a hedge as a dyke; a canopy-height model prefers the opposite—so the knob should be set per application and the setting recorded.

Terrain type changes which error dominates and which parameter matters:

| Terrain | Typical failure | Governing parameter | Direction of DTM bias |
|---|---|---|---|
| Steep natural slopes (> 30°) | Ground rejected as object (Type I) on upslope side | Slope limit / TIN angle / cloth rigidness | Low on ridges, high in gullies after interpolation |
| Dense urban with large buildings | Roofs retained as ground (Type II) where the window is smaller than the building; courtyards lost | Max window / seed cell size | High under retained roofs |
| Forest, closed canopy | Low vegetation accepted as ground (Type II); true ground sparse | Elevation threshold; ground-return density | High, 10–50 cm or more |
| Dunes and sharp crests | Crest shaved (Type I) by curvature or slope rules | Curvature tolerance / threshold | Low on crests |
| Levees, berms, embankments | Crest shaved; toe smeared | Slope and window interaction | Low on crest, high at toe |
| Terraces, retaining walls | Upper terrace rejected near the step | Discontinuity handling | Low on upper terrace edge |
| Flat with low noise | Pits around low outliers | Noise filter first | Local low |

Point density changes the picture again. At 2 pt/m² a 0.5 m threshold spans several points' worth of vertical noise and cars survive; at 30 pt/m² the same threshold over-removes on rough natural ground. A rule that works in practice is to express thresholds in multiples of the per-point vertical noise and windows in multiples of point spacing, and to retune when either changes by a factor of two. No single parameter set works for a county; production practice is to stratify the area by land cover and terrain (using an existing DEM and land-cover map) and apply different parameter sets per stratum, blending at boundaries, or to run a learned classifier that has been validated per stratum.

> **Worked example.** A SMRF-style classifier runs on a 1 km² tile of mixed farmland and woodland at 8 pt/m² with threshold 0.5 m. Manual QA on 2,000 sampled points finds 60 of 1,400 true ground points labelled non-ground (Type I = 4.3 %) and 45 of 600 object points labelled ground (Type II = 7.5 %). Overall accuracy is $(1340 + 555)/2000 = 94.8\,\%$. The Type II points are low shrubs in hedgerows at a mean height of 0.42 m above true ground; because hedgerows cover 3 % of the tile, the DTM carries a +0.42 m bias over 3 % of its area, undetectable by a global RMSE on open-ground checkpoints but fatal for a drainage model that routes flow across the field boundaries. Lowering the threshold to 0.3 m removes the hedges but raises Type I in a ploughed field to 12 %, where rejected furrows are then interpolated flat—a 10 cm loss of real micro-relief. The right answer depends on the deliverable, and the report must say which was chosen and why.

<!-- figure: Figure 30.2 — Type I and Type II error rates as functions of the elevation threshold for one filter on three terrain strata (open farmland, hedgerows, closed-canopy forest), showing that the error-minimising threshold differs by stratum. -->

## 30.5 Evaluation: benchmarks, per-class accuracy, manual QA sampling

The ISPRS Commission III filter test (Sithole & Vosselman 2004) remains the reference experiment: eight filters on fifteen samples from the Vaihingen and Stuttgart datasets (0.67–1.5 m spacing), each sample chosen for a known difficulty—steep slopes, discontinuities, bridges, ramps, low vegetation, large buildings, data gaps. Three conclusions have survived two decades: surface-based filters (Axelsson's TIN, Kraus & Pfeifer's interpolation) outperformed slope and morphology overall; all filters struggled with the same scenes (discontinuities, low vegetation on slopes, bridge approaches, courtyards); and the manually produced reference itself contained ambiguous regions, so reported errors near 1–2 % are at the limit of what the truth can resolve.

Later benchmarks scaled up. **OpenGF** (Qin et al. 2021) provides approximately 47 km² of labelled airborne lidar across metropolis, small-city, village, and mountain scenes, with a held-out test set large enough to train and evaluate deep networks. **DALES** (Varney, Asari & Graham 2020) covers 10 km² of Surrey, British Columbia, at ~50 pt/m² with eight classes. The ISPRS **Vaihingen 3D** and **Hessigheim 3D** (Kölle et al. 2021) datasets provide dense multi-class urban scenes. Each benchmark encodes a labelling policy—OpenGF's documentation specifies how bridges and low walls are labelled—and a filter's score measures agreement with that policy, not with your project's.

Metrics derive from the confusion matrix (see Mathematics): overall accuracy, per-class precision and recall, F1, IoU, and Cohen's κ. For ground extraction, report Type I and Type II separately and by stratum, because an overall accuracy of 97 % can hide a 15 % Type I rate on the 10 % of the tile that is steep; and report the geometric consequence—mean and RMSE of the DTM difference against a reference DTM, by stratum—which is what the end user experiences.

Production QA samples. A defensible design draws a stratified random sample of points or small patches by land cover and terrain, has an analyst label each against imagery, cross-sections, and a hillshade, and estimates per-stratum error rates with binomial confidence intervals. With $n = 200$ sampled points and $e = 10$ errors, the Wilson 95 % interval on a 5 % estimate is approximately 2.7–9.0 %; a few hundred points per stratum is the minimum for rates near 5 %, and detecting a 1 % rate with useful precision needs thousands. Visual QA—hillshades, cross-sections, and the ground-only nDSM that should be near zero over bare ground—remains indispensable because it finds structured errors (a whole terrace shaved, a whole bridge kept) that random sampling misses.

## 30.6 The hydrographic analog: CUBE/CHRT hypothesis selection and operator review

Multibeam cleaning solved the same problem with a different philosophy. Before CUBE, hydrographers rejected fliers by eye in swath editors—slow, inconsistent, and liable to "over-cleaning," the removal of real small features (boulders, wreck masts, pipeline spans) that looked like noise. **CUBE** (Calder & Mayer 2003) replaced sounding-editing with surface estimation: each sounding, carrying a propagated uncertainty from the Hare–Godin–Mayer error model, contributes to nearby grid nodes with a distance-dependent weight; at each node a set of Kalman-style estimators maintains one or more **hypotheses** of depth, spawning a new one when a sounding is inconsistent with all existing hypotheses; and a **disambiguation** rule (by supporting count, neighbourhood consistency, or both) selects the reported value. The operator reviews nodes where disambiguation was uncertain—the "hypothesis strength" and "hypothesis count" layers are the map of where to look—and overrides the selection where the alternative is a real feature. **CHRT** (Calder & Rice 2017) adds variable resolution driven by local data density, the hydrographic version of the cell-size-versus-point-spacing question of [Chapter 31](ch31-interpolation-and-gridding.md).

The lesson that transfers is the maxim "do not over-clean a shoal": the cost of removing a real hazard is unbounded, so the process keeps evidence and makes rejection reviewable. The same asymmetry applies, with a different sign, to levee crests in flood modelling. A ground-filtering pipeline that keeps rejected points flagged, records which filter and parameters applied per stratum, delivers a per-cell count of accepted ground points, and routes ambiguous regions to review has adopted the CUBE philosophy.

## 30.7 Cost and consistency of manual editing; audit trails

Manual classification review is the most expensive processing stage of a lidar project, commonly cited as a quarter to a half of processing labour for QL1/QL2 deliverables in urban and vegetated areas (figures vary by vendor and are rarely published; treat any specific number as approximate). It buys the correction of structured errors that automated filters cannot resolve: bridge decks reclassified to class 17, levee crests restored, hedgerows demoted, water bodies cleaned, hydro-flattening breaklines digitised.

Consistency is the problem. Two analysts given the same ambiguous region—a rubble slope, a terraced vineyard, a construction site, a marsh—produce different ground surfaces, and the differences are systematic by analyst. Mitigations are editorial: a written classification policy with worked pictures for each ambiguous case; calibration sessions in which analysts classify the same tile and reconcile; double-blind review of a fixed fraction of tiles; and per-analyst metrics tracked over the project.

The audit trail must capture edits as operations: tool or polygon, source and target class, analyst, timestamp, reason code. TerraScan and the hydrographic suites can log edits; PDAL pipelines can express them as `filters.assign` or `filters.overlay` steps with a polygon layer; the point is that a reprocessing run can replay them ([Chapter 29](ch29-processing-pipelines.md)). A deliverable that includes the edit log is worth more than one that includes only the edited points.

## 30.8 Deliverable semantics: what "ground" includes in this project

The class 2 label asserts that a point lies on the surface the project calls ground, and that surface is a definition, not an observation. Projects differ on whether ground includes paved roads (USGS LBS: yes), bridge decks (no, class 17), dams and levees (yes), culverts (the road over the culvert is ground unless hydro-enforcement is specified), stockpiles and landfills (usually yes, as of acquisition), retaining walls (the ground on each side yes, the wall face ambiguous), piers (no), rock outcrops and boulders (yes), snow (no, class 21), tall grass and crops (no, but the filter cannot always tell), marsh platforms (yes, biased), and water surfaces (no, class 9). [Chapter 32](ch32-dsm-to-dtm.md) treats the definitions in detail; the point here is that the classification report must state the policy adopted, deviation by deviation, in a form the next user can parse. A sentence like "ground classification follows USGS LBS 2024 except that stockpiles in the active quarry (polygon supplied) were classified as class 1" is worth more than a page of generic method description, because it tells a flood modeller, a volume estimator, and a canopy-height analyst exactly what they are getting.

## Then & now

- **Late 1990s.** First-generation airborne lidar at 0.1–1 pt/m² and the first filters: Kraus & Pfeifer's robust interpolation (1998), Vosselman's slope-based morphology (2000), and Axelsson's progressive TIN densification (2000), which became the TerraScan ground routine and has shaped commercial practice since.
- **2003–2004.** The progressive morphological filter (Zhang et al. 2003) and the ISPRS filter comparison (Sithole & Vosselman 2004) established the Type I/Type II vocabulary and the benchmark habit; CUBE (Calder & Mayer 2003) moved hydrography from sounding-editing to hypothesis-based surface estimation.
- **2007–2013.** MCC (2007) for forestry; LAS 1.4 (2011) standardised the modern class list and flag bits; SMRF (2013) and its PDAL implementation made a competitive open-source filter a one-line pipeline stage.
- **2016–2017.** CSF (2016) brought physical simulation to ground filtering and, through CloudCompare, to a wide user base; CHRT (2017) brought variable resolution to CUBE.
- **2017–2021.** Deep point-cloud networks (PointNet++, KPConv 2019, RandLA-Net 2020) and the benchmarks that made them trainable for ground extraction (DALES 2020, OpenGF 2021); LAS 1.4 R14 (2019) added classes 19–22.
- **Now.** Production pipelines mix a learned classifier for the bulk with rule-based filters and manual review for the structured cases; the open question is how to make the residual few percent reviewable, auditable, and documented per stratum ([Chapter 43](ch43-traditional-vs-ml.md)).

## Mathematics

**Grey-scale morphology.** Let $Z(x)$ be a minimum-binned surface and $B$ a flat structuring element (window) of half-width $w$. Erosion and dilation are
$$ (Z \ominus B)(x) = \min_{u \in B} Z(x+u), \qquad (Z \oplus B)(x) = \max_{u \in B} Z(x+u). $$
The **opening** $Z \circ B = (Z \ominus B) \oplus B$ removes bright (high) features narrower than $B$ and leaves wider ones; the **closing** $Z \bullet B = (Z \oplus B) \ominus B$ fills dark (low) features narrower than $B$. PMF flags a point as non-ground at scale $k$ if $Z_{k-1}(x) - (Z_{k-1} \circ B_k)(x) > dh_k$, with
$$ dh_k = \begin{cases} dh_0, & k = 1 \\ s\,(w_k - w_{k-1})\,c + dh_0, & k > 1 \end{cases}, \qquad dh_k \le dh_{\max}, $$
where $s$ is the slope parameter, $c$ the cell size, and $w_k$ the window half-width in cells. The term $s\,(w_k - w_{k-1})\,c$ is the elevation change that terrain of slope $s$ could legitimately exhibit across the window growth, which is why the threshold grows with scale. Vosselman's slope filter is the same operation with a non-flat (conical) structuring element $B(u) = s\,\|u\|$: $p$ is ground iff $Z(p) \le \min_{q}\,[Z(q) + s\,d(p,q)]$.

**Progressive TIN densification criteria.** For a candidate point $p$ and the triangle $T = (v_1, v_2, v_3)$ containing it, with plane normal $\mathbf{n}$, define the orthogonal distance $d = |\mathbf{n}\cdot(p - v_1)|$ and the angles $\theta_i = \angle(\,p - v_i,\; T\,)$ between the line from each vertex to $p$ and the plane. Accept $p$ as ground if $d < d_{\max}$ and $\max_i \theta_i < \theta_{\max}$. Because $\tan\theta_i = d / \|\pi(p) - v_i\|$ where $\pi(p)$ is the projection of $p$ onto the plane, the angle criterion tightens as triangles shrink; a fixed $d_{\max}$ alone would admit low vegetation in small triangles, while a fixed $\theta_{\max}$ alone would admit large buildings in large triangles. The two together form a scale-adaptive acceptance region.

**CSF physics.** The cloth is a grid of particles whose horizontal positions are fixed and whose heights $z_i$ are updated by Verlet integration under gravity, $z_i^{t+1} = 2 z_i^t - z_i^{t-1} + g\,\Delta t^2$, each particle stopping when it reaches the inverted point surface. Spring forces are applied as positional constraints: for movable neighbours $i, j$, each moves by $\tfrac{1}{2}(z_j - z_i)\,b$ toward the other, where $b$ is set by the rigidness parameter; if one neighbour has landed, the other moves the full difference. Higher rigidness bridges small depressions (flat terrain with buildings); lower rigidness follows steep ground. After convergence a point is ground if its distance to the cloth is below the threshold $h_{cc}$.

**Confusion-matrix metrics.** With $TP$ = ground labelled ground, $FN$ = ground labelled object, $FP$ = object labelled ground, $TN$ = object labelled object:
$$ \text{Type I} = \frac{FN}{TP + FN}, \qquad \text{Type II} = \frac{FP}{FP + TN}, \qquad \text{OA} = \frac{TP + TN}{N}, $$
$$ \text{Precision} = \frac{TP}{TP+FP}, \quad \text{Recall} = 1 - \text{Type I}, \quad F_1 = \frac{2\,TP}{2\,TP + FP + FN}, \quad \text{IoU}_{\text{ground}} = \frac{TP}{TP + FP + FN}, $$
and Cohen's $\kappa = (p_o - p_e)/(1 - p_e)$ with $p_o$ the observed agreement and $p_e$ the agreement expected by chance from the marginals. The geometric translation: if Type II errors have mean height $\bar{h}_{II}$ above true ground and cover a fraction $a_{II}$ of the area, the DTM carries an area-weighted bias of approximately $a_{II}\,\bar{h}_{II}$ plus whatever interpolation bias the Type I gaps induce; report both the label metrics and the DTM difference statistics.

## Validation & uncertainty

Classification error is the component of a DTM's uncertainty budget that is least Gaussian, most spatially structured, and least visible in a standard checkpoint test. A checkpoint survey on open, hard ground—the NVA of the ASPRS standard—tests the trajectory, calibration, and gridding and tells you almost nothing about classification, because the filter had nothing to decide at those points. The VVA, measured at vegetated checkpoints, does test classification, and ASPRS Edition 1 (2014) and the pre-2024 USGS LBS reported it as the 95th percentile of absolute errors rather than as an RMSE precisely because the error distribution there is skewed and heavy-tailed (ASPRS Edition 2, 2023, reports VVA as RMSE$_V$ "as found", not pass/fail; the skew has not gone away, so report the percentile alongside). The validation plan for classification must therefore go beyond checkpoints.

**How the errors arise.** Type II errors (objects accepted) bias the DTM upward by the object height, over the object's footprint. Type I errors (ground rejected) create gaps that the interpolator fills; on convex terrain the fill is low, on concave terrain high, and the magnitude scales with the gap's width and the terrain's curvature ([Chapter 31](ch31-interpolation-and-gridding.md)). Low-noise points accepted as ground create pits whose depth is the outlier's offset. Systematic policy differences—roads in or out, levees shaved or kept—produce errors that are constant across a project and invisible to any within-project test.

**How to test.** The procedure that works in practice is layered:

1. *Stratified label QA* (Section 30.5): Type I and Type II with binomial confidence intervals per stratum.
2. *Reference-DTM comparison*: on tiles with an independent ground surface (field survey, TLS, or a hand-edited reference), DTM differences by stratum—mean, σ, RMSE, 95th percentile of $|\Delta z|$, fraction of cells beyond tolerance.
3. *Feature-specific checks*: profiles across every mapped levee, dam, and embankment crest against surveyed crest heights; a bridge inventory against class 17 extents; a water-body inventory against class 9.
4. *Internal consistency*: the nDSM over ground cells should be near zero; ground above the first-return surface indicates accepted low noise; ground-point density maps show where the DTM is interpolation rather than measurement.
5. *Reproducibility*: rerun with the recorded parameters (and, for learned classifiers, the same weights and seed) and confirm identical labels.

> **Uncertainty budget.** Classification-related contributions to DTM error for an 8 pt/m² leaf-off airborne lidar project with SMRF-class filtering and manual review; magnitudes are typical of values reported in the filter literature and in USGS LBS QA experience, not guarantees.
>
> | Stratum | Dominant error | Typical bias | Typical σ | Detectable by |
> |---|---|---|---|---|
> | Open hard ground | None from classification | ~0 | 0.02–0.05 m | NVA checkpoints |
> | Short grass, crops < 0.3 m | Vegetation top as ground | +0.03 to +0.15 m | 0.05–0.10 m | VVA checkpoints; seasonal comparison |
> | Shrubs, hedgerows | Type II | +0.2 to +1.0 m | large | Stratified QA; nDSM inspection |
> | Closed canopy (leaf-off) | Sparse ground + Type II | +0.05 to +0.3 m | 0.1–0.3 m | VVA; TLS plots |
> | Closed canopy (leaf-on, conifer) | Very sparse ground | +0.3 to > 1 m | large | Field transects |
> | Levee/dune crests | Type I + interpolation | −0.1 to −0.5 m | — | Crest profiles vs. survey |
> | Terraces, walls | Type I at step | −0.1 to −0.3 m locally | — | Profiles |
> | Urban courtyards | Type I (roof seed) | variable | — | Visual QA; footprint overlay |
> | Marsh platform | Vegetation + water | +0.1 to +0.5 m | 0.1–0.2 m | RTK transects ([Chapter 32](ch32-dsm-to-dtm.md)) |

**What to report.** Filters and software versions with every parameter per stratum; the stratification layer; the manual-edit policy and edit-log summary; per-stratum Type I/II with confidence intervals and sample sizes; per-stratum DTM difference statistics where a reference exists; a ground-point density raster and an interpolated-cell mask; and the statement of what ground includes (Section 30.8). This is what lets the accuracy assessment of [Chapter 53](ch53-accuracy-assessment.md) and the reviewer of [Chapter 54](ch54-evaluating-others-data.md) do their jobs.

## Software

**Open source:** PDAL (`filters.outlier`, `filters.elm`, `filters.pmf`, `filters.smrf`, `filters.csf`, `filters.hag_nn`, `filters.assign`, `filters.overlay`; caveat: defaults have changed across versions—pin and record). CloudCompare (CSF plugin and manual segmentation; caveat: edits are not logged unless scripted). lidR (R; `classify_ground()` with `pmf()`, `csf()`, `mcc()`; strong for forestry QA). Open3D-ML and PyTorch-Points3D (KPConv, RandLA-Net; caveat: training on OpenGF or project data is required). MCC-LIDAR (reference MCC). WhiteboxTools (`LidarGroundPointFilter`). MB-System (`mbclean`, `mbedit`, `mbgrid`). Kluster (open multibeam processing with CUBE-style gridding). QGIS with PDAL integration for visual review.

**Free but closed:** LAStools `lasground`/`lasground_new` (free within licence limits; TIN-densification variant with terrain presets `-wilderness` … `-metro` that are effectively step-size parameters—record which was used).

**Commercial:** TerraSolid TerraScan (Axelsson-based ground routine; macro files record parameters); Global Mapper (lidar module); CARIS HIPS & SIPS and QPS Qimera (CUBE/CHRT surfaces, hypothesis review, logged editing); Esri ArcGIS Pro (`Classify LAS Ground` with conservative/standard/aggressive presets); Trimble, RIEGL, and Leica sensor suites (preprocessing and noise handling before LAS export).

## Standards & guides

- **ASPRS LAS Specification 1.4 – R15 (2019)** — classification codes 0–63, flag bits (synthetic, key-point, withheld, overlap), point data record formats 6–10; the **LAS Domain Profile for Topo-Bathy Lidar (2013)** defines classes 40–45.
- **USGS Lidar Base Specification** (online edition, 2024 revision) — required classes for deliverables, the classification accuracy requirement (a maximum fraction of demonstrably misclassified non-withheld points per 1 km × 1 km area; 2 % in recent editions (verify)), the definition of "ground" including roads, dams, and bridge handling, and class 20 use near hydro breaklines.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)** — NVA/VVA strata (both reported as RMSE$_V$ in Edition 2; the 95th-percentile VVA is the Edition 1 / pre-2024 LBS convention) and the land-cover stratification of checkpoints.
- **IHO S-44 Edition 6.1.0 (2022)** — survey orders, TVU/THU, and feature-detection requirements that constrain how aggressively soundings may be cleaned.
- **NOAA Hydrographic Surveys Specifications and Deliverables** (annual) — CUBE/CHRT surface requirements, hypothesis review, the obligation to flag rather than delete soundings.
- **ISPRS Commission III filter test (2003–2004)** — not a standard but the de facto evaluation protocol, with its Type I/Type II definitions.
- **OpenGF benchmark documentation (2021)** — the labelling policy that defines "ground" for the largest public training set; read it before using a model trained on it.

## Pitfalls

- **One parameter set for a whole county.** Filters tuned on flat suburbs shave hills and keep sheds in villages. Detect with per-stratum Type I/II; avoid by stratifying parameters by terrain and land cover.
- **Filters that shave levees, berms, and dune crests.** Curvature and slope rules treat sharp convex terrain as objects; the DTM crest is interpolated low. Detect with crest profiles against survey; avoid with larger thresholds in a levee buffer, breakline-constrained interpolation, or manual restoration.
- **Low vegetation kept as ground.** Thresholds above the vegetation height admit hedges and crops. Detect with nDSM inspection and VVA; avoid with lower thresholds in vegetated strata and seasonal (leaf-off) acquisition.
- **Deleting rather than flagging; confusing overlap with withheld.** Points removed as noise or overlap cannot be reviewed, and tools that drop overlap points thin the cloud by a third. Detect by comparing point counts and density maps across stages; avoid by using class 7/18 and the withheld flag and filtering explicitly.
- **Cleaning that deletes real seafloor features.** Over-aggressive sonar filtering removes boulders, wrecks, and pipeline spans. Detect by reviewing CUBE hypothesis-count layers and by comparing with side-scan or backscatter; avoid by reviewing, not deleting.
- **Low outliers anchoring the ground surface.** A single multipath return becomes a pit. Detect with the ELM filter and pit maps; avoid by running low-noise detection before ground filtering.
- **Class codes reused with vendor-specific meanings.** Class 8, 12, and user classes mean different things in different projects. Detect by reading the classification report; avoid by documenting every code used.
- **Trusting overall accuracy.** 97 % overall can hide 15 % Type I on steep ground. Detect by stratified metrics; avoid by reporting Type I and Type II per stratum.
- **Learned classifier applied out of distribution.** A model trained on temperate suburbs fails on tropical forest or desert. Detect by stratified QA on the new area before production; avoid by fine-tuning with local labels and documenting the training policy.
- **Roof seeds in TIN densification.** Large buildings with no ground in the seed cell become ground. Detect with building-footprint overlays and nDSM; avoid by enlarging the seed cell or seeding from an existing coarse DTM.
- **Classification policy unstated.** The next user cannot know whether roads, dams, or stockpiles are ground. Avoid by writing the Section 30.8 statement into the metadata.

## Key takeaways

- Ground is a classification decision made under a documented policy; record the policy, the filter, the parameters per stratum, and the edits.
- Flag noise and rejected points; never delete them. Low noise must be handled before ground filtering because every ground filter trusts low points.
- Each filter family encodes a terrain assumption (bounded slope, bounded object size, lower envelope, learned features) and fails where the assumption fails—steep slopes, large buildings, sharp crests, dense canopy.
- Type I and Type II errors have opposite DTM consequences (low on crests, high under objects); set the trade-off per use and report both rates per stratum with confidence intervals.
- Validate against reference surfaces and feature-specific checks (crest profiles, bridge inventories), not only against open-ground checkpoints.
- Learned classifiers raise bulk accuracy but transfer a training policy; deliver the training description and per-stratum validation with the product.
- CUBE's lesson transfers: estimate with uncertainty, keep hypotheses, route ambiguity to review, and make rejection auditable.
- Deliver ground-point density and interpolated-cell masks alongside the DTM so users can see where the surface is measured and where it is inferred.

## References

- Axelsson, P. (2000). DEM generation from laser scanner data using adaptive TIN models. *International Archives of Photogrammetry and Remote Sensing*, 33(B4/1), 110–117.
- Calder, B. R., & Mayer, L. A. (2003). Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems*, 4(6), 1048.
- Calder, B. R., & Rice, G. (2017). Computationally efficient variable resolution depth estimation. *Computers & Geosciences*, 106, 49–59.
- Calder, B. R., & Wells, D. E. (2007). *CUBE User's Manual*, Version 1.13. Center for Coastal and Ocean Mapping / Joint Hydrographic Center, University of New Hampshire.
- Evans, J. S., & Hudak, A. T. (2007). A multiscale curvature algorithm for classifying discrete return LiDAR in forested environments. *IEEE Transactions on Geoscience and Remote Sensing*, 45(4), 1029–1038.
- Hare, R., Godin, A., & Mayer, L. A. (1995). *Accuracy estimation of Canadian swath (multibeam) and sweep (multi-transducer) sounding systems*. Canadian Hydrographic Service Technical Report.
- Hu, Q., Yang, B., Xie, L., Rosa, S., Guo, Y., Wang, Z., Trigoni, N., & Markham, A. (2020). RandLA-Net: Efficient semantic segmentation of large-scale point clouds. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*, 11108–11117.
- Kölle, M., Laupheimer, D., Schmohl, S., Haala, N., Rottensteiner, F., Wegner, J. D., & Ledoux, H. (2021). The Hessigheim 3D (H3D) benchmark on semantic segmentation of high-resolution 3D point clouds and textured meshes from UAV LiDAR and multi-view-stereo. *ISPRS Open Journal of Photogrammetry and Remote Sensing*, 1, 100001.
- Kraus, K., & Pfeifer, N. (1998). Determination of terrain models in wooded areas with airborne laser scanner data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 53(4), 193–203.
- Meng, X., Currit, N., & Zhao, K. (2010). Ground filtering algorithms for airborne LiDAR data: A review of critical issues. *Remote Sensing*, 2(3), 833–860.
- Neuenschwander, A., & Pitts, K. (2019). The ATL08 land and vegetation product for the ICESat-2 mission. *Remote Sensing of Environment*, 221, 247–259.
- Pfeifer, N., Stadler, P., & Briese, C. (2001). Derivation of digital terrain models in the SCOP++ environment. *Proceedings of OEEPE Workshop on Airborne Laserscanning and Interferometric SAR for Detailed Digital Terrain Models*, Stockholm.
- Pingel, T. J., Clarke, K. C., & McBride, W. A. (2013). An improved simple morphological filter for the terrain classification of airborne LIDAR data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 77, 21–30.
- Qin, N., Tan, W., Ma, L., Zhang, D., & Li, J. (2021). OpenGF: An ultra-large-scale ground filtering dataset built upon open ALS point clouds around the world. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, 1082–1091.
- Sithole, G., & Vosselman, G. (2004). Experimental comparison of filter algorithms for bare-Earth extraction from airborne laser scanning point clouds. *ISPRS Journal of Photogrammetry and Remote Sensing*, 59(1–2), 85–101.
- Thomas, H., Qi, C. R., Deschaud, J.-E., Marcotegui, B., Goulette, F., & Guibas, L. J. (2019). KPConv: Flexible and deformable convolution for point clouds. *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*, 6411–6420.
- Varney, N., Asari, V. K., & Graham, Q. (2020). DALES: A large-scale aerial LiDAR data set for semantic segmentation. *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW)*, 186–187.
- Vosselman, G. (2000). Slope based filtering of laser altimetry data. *International Archives of Photogrammetry and Remote Sensing*, 33(B3/2), 935–942.
- Zhang, K., Chen, S.-C., Whitman, D., Shyu, M.-L., Yan, J., & Zhang, C. (2003). A progressive morphological filter for removing nonground measurements from airborne LIDAR data. *IEEE Transactions on Geoscience and Remote Sensing*, 41(4), 872–882.
- Zhang, W., Qi, J., Wan, P., Wang, H., Xie, D., Wang, X., & Yan, G. (2016). An easy-to-use airborne LiDAR data filtering method based on cloth simulation. *Remote Sensing*, 8(6), 501.
- ASPRS (2019). *LAS Specification 1.4 – R15*. American Society for Photogrammetry and Remote Sensing.
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2. American Society for Photogrammetry and Remote Sensing.
- U.S. Geological Survey (2024). *Lidar Base Specification*, online edition. USGS National Geospatial Program.

# Chapter 52 — Ground truth and calibration/validation datasets

> **Part XI — Validation, quality, and judging data.** This chapter opens the validation part of the book by asking what we compare elevation products *against*, how that reference material is made, and how good it actually is.

**In this chapter.** Every accuracy statement in this book rests on a comparison with something believed to be better. This chapter is about that "something." You will learn the hierarchy of reference measurements—levelled benchmarks and CORS, GNSS checkpoints, total-station profiles, terrestrial laser scans, dense lidar, and spaceborne laser altimetry—with the error budget of each; how to design a checkpoint campaign that survives scrutiny under ASPRS Edition 2, the USGS Lidar Base Specification, and IHO S-44; which reference surfaces and test sites exist for lidar, photogrammetry, and multibeam; how to use ICESat-2, GEDI, benchmark databases, and open lidar as near-global quasi-truth without being fooled by their biases; how to budget the checkpoints themselves; why ground under canopy, marsh, and soft seafloor have no single "true" height; and how algorithm benchmarks differ from product validation datasets. You will finish able to specify, collect, document, and critique a validation dataset, and to recognize when the "truth" is worse than the product it is judging.

## 52.1 Hierarchy of truth: nothing is true, some things are better measured

There is no ground truth. There are only measurements with smaller and better-characterized uncertainty than the measurement under test. That is not philosophy; it is the operational rule that decides whether a validation means anything. [Chapter 5](ch05-error-and-uncertainty.md) gave the statistical toolkit and [Chapter 25](ch25-calibration-infrastructure.md) the physical infrastructure of calibration. Here we arrange the available reference measurements by what they can resolve, so that the reference matches the claim being tested.

A reference is useful when its uncertainty is small compared with the error you are trying to detect (the conventional target is a factor of three, so the reference contributes about 10 % of observed variance); it measures the same quantity (same surface, datum, and compatible epoch); and it is independent of the product. Table 52.1 arranges the common references by typical vertical uncertainty; the numbers are indicative, and your own checkpoints must carry their own budget (§52.5).

| Reference type | Typical vertical uncertainty (1σ) | Footprint | Appropriate for validating |
|---|---|---|---|
| First-order levelled benchmark | 1–5 mm relative; datum realization dominates | Monument top; H in a specific adjustment | GNSS heights, geoid models, local lidar bias |
| CORS station | 2–5 mm (daily solution) | Antenna reference point; h in ITRF/national frame | Vertical land motion, campaign checks |
| Static GNSS checkpoint (NGS-58 style) | 1–2 cm h, plus geoid error for H | Point on hard surface | Lidar NVA, photogrammetric DTMs, UAS |
| RTK/RTN checkpoint (180 s, redundant) | 2–5 cm h; 3–6 cm H | Point | Lidar NVA, UAS, mobile mapping |
| Total station / level profile from control | 2–10 mm relative | Line or grid of points | TLS, UAS SfM, local relative accuracy |
| TLS registered to control | 5–20 mm | Surface at mm–cm spacing | Airborne lidar, SfM, change detection |
| Dense airborne lidar (QL1, ≥ 8 pls/m²) | 5–10 cm NVA | Surface at dm spacing | 1″–3″ global DEMs, satellite stereo, SDB |
| ICESat-2 ATL03/06/08 | ~0.1–0.3 m on flat open ground; metres on steep or forested terrain | ~11–17 m footprint; 20 m (ATL06) or 100 m (ATL08) segments | Regional/global DEMs, open-terrain bias |
| GEDI L2A ground elevation | ~1–3 m; worse on slopes | 25 m footprint, sparse | Coarse DEMs; canopy structure |
| MBES reference surface (Special Order) | 0.1–0.3 m TVU at shelf depths | Gridded surface, few km² | Crosslines, other MBES, lidar bathymetry, SDB |
| Lead line, pole, diver tape | 0.05–0.3 m; bottom definition dominates | Point | Very shallow water, soft bottoms, history |

*Table 52.1 — A hierarchy of reference measurements under good conditions. A badly executed benchmark tie is worse than a well-executed ICESat-2 comparison.*

Three remarks. First, at the top of the hierarchy the **datum realization** matters more than the instrument: a benchmark published to the millimetre in NAVD88 from the 1991 adjustment and lidar whose NAVD88 heights come through GNSS and GEOID18 can disagree by several centimetres through no fault of either, and in subsiding or rebounding regions published heights are decades out of date ([Chapter 9](ch09-vertical-datums.md), [Chapter 38](ch38-plate-motion-and-vlm.md)). Second, **footprint** is a quantity—a rod tip, a 1 m DEM cell, and a 100 m ATL08 segment sample different things—so comparisons are meaningful only where the surface is smooth at the larger scale, which is why standards insist on flat, open, hard ground for the primary vertical test. Third, the right-hand column is a matter of ratios: dense lidar at 7 cm RMSE is excellent truth for a 30 m global DSM with metre-level errors and useless as truth for another lidar survey of the same class.

<!-- figure: Figure 52.1 — Pyramid of reference measurements labelled with vertical uncertainty (mm for levelled benchmarks and CORS, cm for GNSS checkpoints and TLS, dm for dense lidar and ICESat-2, m for GEDI and lead lines), with arrows showing which level validates which product class. -->

> **Definitions that bite.** *Control point*, *checkpoint*, and *validation point* are not synonyms. A **control point** constrains or adjusts the product (ground control for aerotriangulation, boresight targets, a benchmark used to level a tide staff). A **checkpoint** is withheld from all adjustment and used only to test. A point that touched the processing in any way—including by being used to choose between parameter sets or to decide a block had "passed"—is no longer independent and must not appear in the accuracy statement. When a report says "the data were checked against 45 control points," ask which were used in the adjustment. The answer is usually "all of them."

## 52.2 Designing a checkpoint campaign

A checkpoint campaign is a survey in its own right, with a specification, a plan, a field protocol, a processing workflow, and a report. Sending whoever is free with an RTK rover on the last day produces the failures in the Pitfalls section.

### 52.2.1 How many

ASPRS Positional Accuracy Standards Edition 2 (2023; Version 2, 2024) set a minimum of 30 checkpoints per project, scaling with area to a cap of 120, with vertical results reported separately for non-vegetated (NVA) and vegetated (VVA) land cover; Edition 1 (2014) had started at 20 plus 5 for projects up to 500 km². The USGS Lidar Base Specification 2024 incorporates Edition 2 by reference. Thirty is roughly the smallest sample for which an RMSE has a tolerable confidence interval: the Mathematics section shows a 95 % interval of about 0.80–1.34 times the sample value at $n = 30$ and 0.68–1.92 at $n = 8$. "RMSE 9 cm from 8 checkpoints" is an anecdote, not a result.

The better question is "how many do I need to detect the failure I care about?" Distinguishing a 10 cm product from a 13 cm one at useful power pushes the open-terrain count toward 60–100, and every stratum you report needs its own 30: a campaign with 25 points on roads and 5 in forest has tested the roads.

### 52.2.2 Where

**Spatial spread** across the project so that strip- or block-dependent biases are sampled rather than averaged (a coarse grid with at least one point per accessible cell). **Stratification by land cover**, because the error mechanisms differ: pavement tests sensor, trajectory, and calibration; grass and crops test the ground filter; forest tests penetration and classification; urban tests edges and building removal. **Stratification by slope**, because a horizontal error $\sigma_{xy}$ on a slope of angle $\theta$ appears as a vertical error $\sigma_{xy}\tan\theta$—0.3 m horizontal on a 20° slope is 0.11 m of apparent vertical error—and because interpolation error grows with slope and curvature. Confine the NVA stratum to flat (preferably well under 10 %) hard, open surfaces so that it measures the product rather than the test geometry, and report sloped and vegetated strata separately.

Within each stratum choose sites that are stable between epochs (no construction, tillage, or snow), accessible without trespass, uniform for at least 3–5 m around for a 1 m DEM, and away from curbs, ditches, footprints, and treelines; a checkpoint one metre from a curb tests horizontal registration, not vertical accuracy.

### 52.2.3 Independence

Checkpoints must be independent of the product in instrument, crew, processing, and ideally epoch and method. A vendor who surveys their own checkpoints with the same base station, antenna heights, and geoid model cannot detect an error in any of those shared elements: a 4 cm error in the base height propagates identically into the lidar trajectory and the checkpoints, and the "validation" reports a 1 cm mean error over a product that is 4 cm wrong relative to the national datum. Independence means a different control tie (OPUS, CORS, published benchmarks), a different receiver and antenna, and where possible a different method.

### 52.2.4 How: occupation protocols

For static GNSS the templates are NOAA Technical Memoranda NOS NGS-58 (Zilkoski, D'Onofrio & Frakes 1997) for ellipsoidal heights at the 2 cm and 5 cm standards and NGS-59 (Zilkoski, Carlson & Smith 2008) for orthometric heights; NGS 92 (2024) supersedes their procedures but their logic remains the practical guide. NGS-58's core requirements for the 2 cm standard: dual-frequency receivers, fixed-height tripods, sessions of at least 30 minutes, each baseline observed at least twice on different days at different times of day, and VDOP below 6 for most of the session. NGS-59 adds the tie to published benchmarks so that GNSS-derived orthometric heights agree with the local datum realization.

For RTK/RTN, which is how most lidar validation is actually done, the NGS single-base real-time guidelines (Henning 2011) recommend observations of about 180 seconds with a fixed solution, redundant occupations several hours apart, a bipod rather than a hand-held rod, and short base-to-rover distances (commonly under 10–15 km). Record antenna model and height, base coordinates and source, fixed status and precision per occupation, and time. Two occupations agreeing within 2 cm are worth five single ones.

Convert to orthometric height with a named geoid model and record it. If the product is in NAVD88 via GEOID18 and the checkpoints via GEOID12B, the comparison has a regionally varying bias of several centimetres built in before anyone looks at the lidar. The cleaner practice is to compare in ellipsoidal heights where available and treat the geoid conversion as a separate documented step.

### 52.2.5 What to measure

An NVA checkpoint is a marked, photographed point on hard, flat, open ground—pavement, packed gravel, bare soil, short grass—where lidar returns are unambiguous and the DEM represents the same surface the rod tip touches. VVA checkpoints are collected in tall grass, crops, brush, or forest with the rod on mineral soil, not litter; because GNSS under canopy degrades sharply (§52.6), many campaigns measure VVA points by total station from a GNSS pair in the nearest opening, which is slower and better. Horizontal checkpoints, where required, use intensity imagery on road markings or targets ([Chapter 53](ch53-accuracy-assessment.md)).

### 52.2.6 Documentation

The deliverable is a **checkpoint table** plus a **checkpoint report**. Per point: identifier; easting, northing, h and H with CRS, geoid model, and epoch named; stratum and slope class; date and time; method, receiver, antenna, antenna height, base or network; reported precision; photographs. The report describes the control tie, the independence from the product, the processing, and the checkpoints' own uncertainty (§52.5), which under Edition 2 enters the product accuracy computation and is therefore mandatory. §52.8 returns to the table as a deliverable.

> **Rule of thumb.** Thirty checkpoints per reported stratum; three times more accurate than the product class (or well enough budgeted to combine); zero shared with control or calibration; two independent occupations each. Where any of these cannot be met, say so. The 3× factor is a convenience; what matters is a documented checkpoint uncertainty.

## 52.3 Reference surfaces and sites

Scattered points answer "how high is the product here?"; a reference *surface* answers "what are its shape, noise, relative accuracy, and calibration state?"

**Runways, aprons, and large parking lots** are the workhorse surfaces for airborne lidar and photogrammetry: flat to engineering tolerance (runway grades are typically limited to about 1–2 %, so a kilometre of runway fits a low-order polynomial to a few centimetres), hard, bright in the near-infrared, and often resurveyed for obstruction and eTOD purposes ([Chapter 62](ch62-navigation-and-charting.md)). A runway crossed by several flight lines yields swath-to-swath differences, roll and pitch boresight residuals (roll appears as a cross-track tilt, pitch as an along-track offset), and the intra-swath noise the LBS calls "smooth surface precision." When airport access is impractical, freshly paved roads, commercial parking lots, and sports fields serve.

**Lidar calibration ranges** are purpose-built: a few square kilometres with gabled roofs of varied orientation (to separate roll, pitch, and heading), flat open areas, and surveyed hard targets. [Chapter 25](ch25-calibration-infrastructure.md) describes the targets and geometry.

**Photogrammetric and geodetic test fields** have a longer history. The ISPRS test fields (Vaihingen/Enz, Enschede, Dortmund, Zurich/Hönggerberg) were established with dense signalized points for camera calibration and aerotriangulation studies and later served lidar filtering and urban classification benchmarks ([Chapter 42](ch42-object-detection-semantics.md)). The EuroSDR/ISPRS DTM quality project used such fields to compare producers' DTMs and established the robust statistics that became standard (Höhle & Höhle 2009).

**Hydrographic reference surfaces** are the multibeam counterpart. The NOAA Field Procedures Manual requires each platform to run a **reference surface** check: a small area of flat, featureless, stable seafloor at representative depth is surveyed with multiple passes in multiple directions, gridded, and compared with a previously accepted surface to test depth agreement, noise, and sound-speed sensitivity. A **patch test** site, by contrast, needs features—a distinct slope and a point target—so that roll, pitch, heading, and latency can be solved from reciprocal and parallel lines ([Chapter 20](ch20-sonar.md), [Chapter 26](ch26-survey-planning.md)). The Shallow Survey common datasets (§52.7) were collected over documented sites for exactly this reason.

**Instrumented slopes and catchments**—resurveyed repeatedly by TLS, UAS SfM, and GNSS—are the geomorphologists' reference sites ([Chapter 40](ch40-erosion-and-geomorphic-change.md)); their "truth" includes a change signal, so a method is tested on detecting known change, not merely reproducing a static surface.

<!-- figure: Figure 52.2 — A lidar calibration range and an MBES reference-surface/patch-test site side by side: a runway with crossing flight lines and gabled roofs annotated with the boresight angle each resolves; a flat reference area with reciprocal lines and a nearby slope plus point feature for pitch, roll, heading, and latency. -->

## 52.4 Global and semi-global validation datasets

For a product you did not make, or for a regional or global DEM, you will not survey checkpoints; you will use what exists. Four families of reference data are now in routine use, each with a characteristic bias.

### 52.4.1 Spaceborne laser altimetry

**ICESat GLAS** (2003–2009), with a roughly 65 m footprint at 172 m spacing, was the first near-global laser reference and was used to assess SRTM by tree cover and relief (Carabajal & Harding 2006); its archive remains useful for pre-2010 epochs.

**ICESat-2** (launched September 2018; Markus et al. 2017) carries ATLAS, a 532 nm photon-counting lidar with six beams in three strong/weak pairs, footprints of roughly 11–17 m, and 0.7 m along-track photon spacing. For DEM validation the relevant products are **ATL03** (geolocated photons, from which you can build your own ground estimate), **ATL06** (40 m overlapping segments at 20 m posting, designed for ice but excellent over any smooth open surface), and **ATL08** (100 m land segments with a terrain estimate, canopy height, and photon classification). Over flat open ground ATL06/ATL08 terrain heights agree with airborne lidar and GNSS at the decimetre level or better—biases of a few centimetres and precision near 9 cm over the Antarctic 88°S traverse (Brunt et al. 2019); ATL08 terrain means near zero and RMSE of a few decimetres in open boreal and temperate terrain, degrading under dense canopy and on slopes (Neuenschwander et al. 2020; Liu et al. 2021). Weak beams and daytime data carry far more background photons; under dense canopy the terrain fit drifts upward; on slopes the 100 m fit smooths real topography. Keep strong-beam, night-time, high-confidence segments with low slope, clear cloud flags, a minimum terrain-photon count, and limited canopy cover, and compare the DEM interpolated along the segment rather than at its centroid. ICESat-2 heights are ellipsoidal (ITRF2014); convert with the same geoid model used for any other comparison.

**GEDI** (Dubayah et al. 2020), on the International Space Station since 2019, is a 1064 nm full-waveform lidar with 25 m footprints along eight tracks between about 51.6°S and 51.6°N. Its **L2A** ground elevation is the last waveform mode under one of several algorithm settings; assessments in temperate forest report ground RMSE of the order of 1–3 m, strongly dependent on slope, cover, and algorithm group (Adam et al. 2020; Liu et al. 2021). GEDI is a reasonable reference for 30 m DEMs in gentle terrain and a poor one for anything finer or steeper; its strength is canopy structure.

### 52.4.2 National benchmark and GNSS databases

The NGS Integrated Database publishes orthometric and, for many marks, GNSS-derived ellipsoidal heights for hundreds of thousands of monuments; **OPUS Shared Solutions** add user-submitted static solutions with photographs. These were used to assess the National Elevation Dataset and 3DEP (Gesch, Oimoen & Evans 2014; Stoker & Miller 2022), and most countries have equivalents. The caveats: heights are in a specific adjustment and epoch; many marks are disturbed, destroyed, or in subsiding ground; a disc on a post or headwall is not at ground height; and marks were sited along roads and railways, the easiest stratum. Filter to marks with recent GNSS observations, good stability codes, and a flush setting on natural ground.

### 52.4.3 Open high-resolution lidar

The most powerful reference for 1″–3″ global DEMs is dense airborne lidar, now openly available through OpenTopography, USGS 3DEP, and national programmes ([Chapter 51](ch51-finding-data.md), [Chapter 55](ch55-public-products.md)). Lidar DTMs with 5–15 cm NVA are an order of magnitude better than any global DEM and, unlike ICESat-2, test the product under canopy and in cities. The **DEMIX** initiative (Guth et al. 2021; Bielski et al. 2024) formalized this into 10 km × 10 km tiles spanning terrain types, each with reference lidar DTM and DSM, and criteria ranked with a Wilcoxon-based test that avoids over-interpreting small differences. Two lessons: compare each global DEM to a reference of the *same surface type*—GLO-30 and AW3D30 are DSMs and belong against a lidar DSM—and report the land-cover and slope distribution of your reference points, because when the same products were ranked with ICESat-2 instead of lidar (Guth & Geoffroy 2021) the magnitudes were systematically more favourable: usable ICESat-2 segments concentrate on open, low-slope terrain where every DEM does well.

Aggregation needs care: averaging a 1 m DTM to 30 m suits a DEM whose cells are area means; sampling at cell centres suits a point-sampled product. Resolve the pixel-is-point/area convention first ([Chapter 44](ch44-resolution-and-sampling.md), [Chapter 54](ch54-evaluating-others-data.md)): a half-cell shift on a 30 m product in 10° terrain is 2.6 m of apparent vertical error that is entirely an artefact of the comparison.

### 52.4.4 Bathymetric references

At sea the hierarchy is shorter. A modern MBES survey to IHO Special or Exclusive Order with documented TPU (Hare, Eakins & Amante 2011) is the usual reference for older single-beam surveys, bathymetric lidar, satellite-derived bathymetry, and compiled grids; hydrographic archives (NCEI, UKHO, EMODnet) provide them with Descriptive Reports and quality metadata ([Chapter 49](ch49-metadata.md)). SDB is validated against MBES or lidar bathymetry reduced to the same datum and compared at SDB cell scale ([Chapter 23](ch23-satellite-derived-bathymetry.md)), and only where the reference postdates morphologic change—on sandy coasts, a season. Compiled grids such as GEBCO can be validated honestly only against surveys *not* included in the compilation, which is why the Type Identifier grid matters ([Chapter 48](ch48-compositing.md)).

## 52.5 Validating the validators

Every checkpoint has an error budget, and under ASPRS Edition 2 it enters the product's accuracy computation. The budget has five parts.

**GNSS height.** A well-executed RTN occupation on an open site gives 2–3 cm (1σ) in ellipsoidal height; the receiver's reported precision is optimistic by a factor of two or more. Two occupations hours apart agreeing within 2–3 cm justify a claim near 2 cm; static NGS-58 work achieves 1–2 cm. A local base's coordinate error is common to all points and invisible to repeatability statistics; estimate it from the OPUS report.

**Geoid model.** Converting h to H adds a spatially correlated error—1–2 cm for hybrid geoids in densely levelled regions, 5–10 cm or worse in mountains or with gravimetric-only models—that acts as a regional bias. If product and checkpoints use the same model, it cancels in the comparison; if not, apply the published difference grid.

**Antenna height and rod.** The antenna-to-tip distance is the largest blunder source; a fixed-height pole, a documented phase-centre model, and a setup photograph are the defences. A hand-held rod wanders 1–2 cm from plumb; a tip pushed into soft ground measures 2–5 cm below the surface the lidar saw.

**Epoch and surface change.** A regraded lot, a ploughed field, or a marsh in another season is a different surface. Where vertical land motion approaches 1 cm/yr (parts of the Gulf Coast, Fennoscandia) a decades-old benchmark discrepancy is real motion, not product error.

**Datum realization.** A 1991-adjustment NAVD88 height and a GNSS/GEOID18 NAVD88 height differ by the local levelling–geoid discrepancy, usually centimetres, occasionally a decimetre. State which realization each side uses.

> **Uncertainty budget.** A typical RTN checkpoint for lidar validation: hard open surface, two 180 s occupations four hours apart, network solution, GEOID18 on both sides.
>
> | Component | 1σ (cm) | Notes |
> |---|---|---|
> | RTN ellipsoidal height, per occupation | 2.5 | Two occupations averaged → 1.8 |
> | Network realization relative to NSRS | 1.0 | Common to all points (bias) |
> | Antenna height / rod plumb | 0.7 | Fixed-height pole, bipod |
> | Rod tip / surface roughness | 0.5 | Pavement |
> | Geoid model | 0 | Cancels; same model both sides |
> | Surface change | 0 | Pavement, 3 months |
> | **Combined (RSS)** | **≈ 2.1** | Random ≈ 1.9; bias ≈ 1.0 |
>
> Against a QL2 product (10 cm RMSE_v class) the checkpoint contributes $(2.1/10)^2 \approx 4\%$ of observed variance—negligible. Against a QL0 product (5 cm) about 18 %, and against a UAS SfM survey claiming 2 cm it dominates: that claim cannot be tested with these checkpoints at all.

**When truth is worse than the product.** Modern lidar and GNSS routinely exceed the accuracy of the infrastructure they are compared to. The pre-lidar National Elevation Dataset had RMSE around 1.5–2.5 m against GNSS benchmarks depending on source (Gesch et al. 2014), so "validating" a 30 m product against it mostly measures the NED. When you must use a reference of comparable quality, call it a *consistency check*, decompose $\sigma^2_{\text{obs}} = \sigma^2_{\text{product}} + \sigma^2_{\text{ref}}$ with your best estimate of $\sigma_{\text{ref}}$, and refuse to quote a product RMSE smaller than the reference's own uncertainty.

## 52.6 Vegetated and bathymetric truth problems

The hierarchy assumes "the surface" exists and every instrument sees the same one. In three environments it does not.

**Ground under canopy.** Four instruments return four heights. A rod reaches mineral soil only if the operator clears the litter (2–10 cm in temperate forest, more in boreal moss). GNSS under canopy suffers attenuation and multipath; float or degraded-fixed solutions can be decimetres wrong while reporting centimetres. Hodgson & Bresnahan (2004) found checkpoint survey error itself a noticeable part of observed lidar error in vegetated classes, with land cover dominating over slope. Lidar last returns come from whatever the pulse reaches—soil, litter, shrubs, logs—and the ground filter then decides which are "ground"; Reutebuch et al. (2003) found DTM errors under conifer canopy of about 0.2–0.3 m mean, larger in dense stands. ATL08 under dense canopy drifts toward the canopy. Consequences: measure VVA points by total station from a clearing or by long static GNSS with skeptical QC; state the "ground" convention (mineral soil versus litter top) because it is worth centimetres; and understand that VVA tests the filter as much as the sensor—which is why Edition 2 keeps it as a required report but not a pass/fail criterion.

**Marsh.** Coastal marsh is a saturated, spongy surface under dense *Spartina* or *Juncus* that lidar rarely penetrates fully; lidar DEMs in salt marsh are biased high by typically 0.1–0.3 m, from about 7 cm in short sparse vegetation to over 0.5 m in tall dense stands (Schmid et al. 2011; Medeiros et al. 2015). The rod sinks several centimetres, so the reference depends on how hard the surveyor pushes; tide, season, and wrack change both the lidar return and the accessible surface. For inundation modelling with a relevant vertical range of a few decimetres this bias is the dominant uncertainty (Gesch 2018), and the reference protocol must specify a plate of stated area under the rod tip, measurement at low tide, vegetation height, and a documented correction by species ([Chapter 64](ch64-agriculture-forests-wetlands.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).

**Soft seafloor.** A lead line stops where the lead stops sinking, which in fluid mud can be well below the reflector a 200 kHz multibeam detects and well above the consolidated bottom a 12 kHz single-beam sees; differences of 0.3–1 m between frequencies are routine in estuaries, and the nautical-depth concept (a density threshold, often 1,200 kg/m³) exists because no acoustic answer is unique ([Chapter 20](ch20-sonar.md)). A reference survey must match the product's frequency class and detection method; otherwise a comparison is a definition test, not an accuracy test.

**Temporal mismatch.** Snow adds decimetres to metres and both lidar and GNSS measure its surface; a summer checkpoint survey against a winter DEM has a "bias" equal to the snowpack. Tides shift intertidal comparisons unless both sides are reduced identically. Crops grow 1–2 m between May and August. Beaches move decimetres per storm. The reference epoch must lie inside the window over which the surface is stable at the level claimed, and that window must be stated ([Chapter 36](ch36-seasonal-variability.md), [Chapter 37](ch37-time-scales-of-change.md)).

<!-- figure: Figure 52.3 — Cross-sections under forest canopy and across a salt marsh showing the different "ground" surfaces returned by a rod on mineral soil, a rod on litter, lidar last returns, a filtered DTM, and an ATL08 terrain estimate, annotated with typical offsets in centimetres. -->

## 52.7 Benchmarks for algorithms versus datasets for products

An **algorithm benchmark** is a fixed input with a fixed reference labelling used to compare methods under identical conditions; a **product validation dataset** is a reference measurement used to judge a specific delivered dataset. Confusing them yields claims like "our classifier scores 97 % on DALES, therefore the DTM is accurate," which does not follow.

Algorithm benchmarks for ground extraction and classification include the ISPRS filter test (Sithole & Vosselman 2004), which established the Type I/Type II error protocol; the ISPRS Vaihingen and Toronto urban benchmarks; **DALES** (Varney, Asari & Graehling 2020); and **OpenGF** (Qin et al. 2021), built from open national lidar to test ground filtering across terrain types ([Chapter 30](ch30-point-cloud-classification.md), [Chapter 42](ch42-object-detection-semantics.md)). For photogrammetry and SfM there are the ISPRS/EuroSDR multi-platform benchmark and UAS test fields with surveyed targets ([Chapter 22](ch22-photogrammetry-sfm.md)). For multibeam processing, the **Shallow Survey common datasets**—collected over documented sites for the conference series beginning in Sydney in 1999 and continuing at Portsmouth, Plymouth, Wellington, and St John's—offer raw multibeam, lidar, and ancillary data for comparing processing chains and uncertainty models. **DEMIX** is a product intercomparison framework, not an algorithm benchmark. Use benchmarks to choose methods and validation datasets to accept products ([Appendix H](../appendices/appendix-h-datasets.md) lists both).

## 52.8 Sharing and licensing truth data

Checkpoint tables are small, expensive, and durable, yet they are routinely delivered as a PDF table or not at all. Three practices fix this. **Make the checkpoint table a mandatory deliverable** as a machine-readable file (CSV or GeoPackage) with the columns of §52.2.6 and the per-point residuals, cited in the metadata ([Chapter 49](ch49-metadata.md)) and archived with the product ([Chapter 50](ch50-archiving-and-provenance.md)); the LBS requires the checkpoint report and coordinates, and Edition 2's reporting guidance includes the residual table. **License truth data openly** (CC0, CC BY, or the national open-data licence), because its value is reuse, and publish reference surfaces with persistent identifiers (OpenTopography assigns DOIs). **Treat privacy and security as questions to assess, not assume**: a checkpoint is a coordinate on a public road, visible in any aerial image; the rare exceptions (private land under non-disclosure, secure facilities) are handled by generalizing the public location ([Chapter 69](ch69-security-sovereignty-privacy-ethics.md)). Benchmark databases have been public for a century.

## Then & now

- **Levelled benchmarks and triangulation stations ⟨H⟩.** Into the 1980s, truth was a monument: a brass disc with a levelled height in a national adjustment (Sea Level Datum of 1929, later NGVD29; Ordnance Datum Newlyn) and a triangulated position. The US National Map Accuracy Standards of 1947 ⟨H⟩ tested "90 % of elevations interpolated from contours within half a contour interval," assuming the tester had better heights than the map.
- **GPS campaigns (1990s).** Dual-frequency static GPS delivered centimetre ellipsoidal heights in hours; NGS-58 (1997) codified the procedures and the geoid model became the limiting factor for orthometric heights. NSSDA (1998) replaced the contour test with an RMSE statistic and asked for checkpoints three times more accurate than the data tested.
- **CORS, OPUS, and real-time networks (2000s).** Online processing (NGS OPUS from 2001) and real-time networks made independent 3 cm checkpoints a matter of minutes; counts and stratification grew accordingly.
- **Spaceborne laser altimetry as near-global reference.** ICESat (2003) assessed SRTM within three years; ICESat-2 (2018), GEDI (2019), and open national lidar changed the default from "the agency says it meets spec" to "we checked."
- **Standards.** NMAS 1947 ⟨H⟩ → NSSDA 1998 → ASPRS 2014 (NVA/VVA, quality classes) → Edition 2 (2023/2024: 30-point minimum, checkpoint error in the budget, VVA reported but not pass/fail, 3D accuracy). S-44 moved from fixed depth-accuracy tables to the TVU formula in Edition 4 (1998) and added feature-detection language through Editions 5 and 6. The arc is from trusting the reference to budgeting it.

## Mathematics

**Confidence interval on an RMSE.** If $n$ residuals are independent, normal, zero-mean with variance $\sigma^2$, then $n\,\widehat{\mathrm{RMSE}}^2/\sigma^2 \sim \chi^2_n$, and

$$
\widehat{\mathrm{RMSE}}\sqrt{\frac{n}{\chi^2_{n,\,1-\alpha/2}}} \;\le\; \sigma \;\le\; \widehat{\mathrm{RMSE}}\sqrt{\frac{n}{\chi^2_{n,\,\alpha/2}}} .
$$

For $n = 30$, $\alpha = 0.05$: $\chi^2_{30,0.975} = 46.98$, $\chi^2_{30,0.025} = 16.79$, multipliers 0.80 and 1.34. For $n = 8$: 0.68 and 1.92. For $n = 100$: 0.88 and 1.16. The large-sample approximation $\sigma_{\widehat{\mathrm{RMSE}}} \approx \widehat{\mathrm{RMSE}}/\sqrt{2n}$ gives the $n$ needed for a half-width of fraction $r$: $n \approx (1.96/r)^2/2$, so $r = 0.10$ needs about 192 points and $r = 0.20$ about 48. Non-normal residuals widen them; bootstrap.

**Allowing for checkpoint error.** With independent errors, $\sigma^2_{\text{obs}} = \sigma^2_{\text{product}} + \sigma^2_{\text{check}}$, so $\widehat\sigma_{\text{product}} = \sqrt{\sigma^2_{\text{obs}} - \sigma^2_{\text{check}}}$. With $\sigma_{\text{obs}} = 9.0$ cm and $\sigma_{\text{check}} = 2.1$ cm, $\widehat\sigma_{\text{product}} = \sqrt{81 - 4.4} = 8.75$ cm, a 3 % correction; with $\sigma_{\text{obs}} = 4.0$ cm, $\sqrt{16 - 4.4} = 3.4$ cm, a 15 % correction that depends sensitively on the checkpoint estimate. The 3:1 rule follows from requiring the correction to be under about 5 %. ASPRS Edition 2 takes the opposite, conservative convention for *reporting*: the checkpoint RMSE is added in quadrature, $\mathrm{RMSE}_{\text{reported}} = \sqrt{\mathrm{RMSE}_{\text{test}}^2 + \mathrm{RMSE}_{\text{check}}^2}$, so that relaxed checkpoint accuracy can never flatter the product. Use subtraction to *estimate* the product's own error and addition to *report* under Edition 2. If checkpoint and product errors are *correlated* (shared base, shared geoid) the formula understates product error and the shared component must be estimated separately.

**Stratified estimation.** With strata of area weights $w_k$ and per-stratum $\mathrm{RMSE}_k$, the area-weighted figure is $\mathrm{MSE}_{\text{area}} = \sum_k w_k\,\mathrm{RMSE}_k^2$; report the per-stratum values too, since the weighted number hides the stratum that fails. Neyman allocation $n_k \propto w_k\sigma_k$ minimizes the pooled variance for a fixed total, which puts more points where error is larger (forest) rather than where surveying is easiest (roads).

**Outlier policy.** A 3σ rule is circular when outliers inflate $\hat\sigma$ and it discards real product failures. Compute the median $m$ and $\mathrm{NMAD} = 1.4826\,\mathrm{median}(|\varepsilon_i - m|)$, flag $|\varepsilon_i - m| > 3\,\mathrm{NMAD}$, investigate each flagged point, and report statistics with and without them and the reason for each exclusion (Höhle & Höhle 2009). A checkpoint removed because the site was regraded is a bad checkpoint; one removed because the product is 1.2 m wrong there is a product failure.

## Validation & uncertainty

This chapter's subject is validation, so this section concentrates on the question the chapter raises: how do you know your reference is good enough, and how do you show it?

**Qualifying a checkpoint set.** (1) Recompute every height from the raw observations or processing report. (2) Verify the control tie: base or network coordinates, source, epoch, OPUS report. (3) Confirm the geoid model and datum realization match the product's, or apply the documented difference. (4) Check repeatability: the spread between redundant occupations bounds the random error from below—an RMS first-versus-second difference of 1.5 cm supports about 1.1 cm per occupation ($1.5/\sqrt2$), not better. (5) Check each site: photographs, slope, edges, surface type, dates. (6) Assign strata and confirm each has enough points. (7) Write the budget of §52.5 and report the combined checkpoint uncertainty as a number.

> **Worked example.** A county lidar project (QL2: NVA ≤ 10 cm RMSE_v) is tested with 42 NVA checkpoints on pavement, each occupied twice by RTN, and 31 VVA points in forest by total station from GNSS pairs in clearings.
>
> *Checkpoint qualification.* RMS difference between first and second RTN occupations is 2.4 cm → per-occupation random error ≈ 1.7 cm, two-occupation mean ≈ 1.2 cm. Adding 1.0 cm network realization and 0.8 cm rod/setup: $\sigma_{\text{check,NVA}} = \sqrt{1.2^2 + 1.0^2 + 0.8^2} \approx 1.8$ cm. VVA points carry the clearing pair's 2.5 cm, a 1 cm traverse, and a 3 cm litter/soil definition allowance: $\sigma_{\text{check,VVA}} \approx 4.0$ cm.
>
> *Observed residuals (product minus checkpoint).* NVA mean +1.3 cm, RMSE 7.9 cm. VVA median +6 cm, NMAD 14 cm, RMSE 16 cm, 95th percentile of $|\varepsilon|$ 31 cm.
>
> *Product NVA.* The statistical estimate of the product's own error is $\sqrt{7.9^2 - 1.8^2} = 7.7$ cm; the Edition 2 reported value adds the checkpoint error instead, $\sqrt{7.9^2 + 1.8^2} = 8.1$ cm. With $n = 42$ ($\chi^2_{42,0.975} = 61.8$, $\chi^2_{42,0.025} = 26.0$) the multipliers are 0.82 and 1.27, so the 95 % interval on the reported value is about 6.6–10.3 cm: the point estimate meets the 10 cm class, but the upper bound does not, and the honest statement is "consistent with, but not demonstrably within, specification"—roughly 60 points would have been needed to close the interval. The VVA is reported as found—as RMSE$_v$ (16 cm) under Edition 2, with the 95th percentile alongside for LBS-era comparability—together with its definition uncertainty, not as a pass/fail.

**What to report about the reference.** Instrument and method; control tie and datum realization; geoid model; points per stratum; site criteria; epoch and interval to the product; the checkpoint budget; the independence statement; and the per-point residual table. For external references (ICESat-2, GEDI, benchmarks, reference lidar): product version, filters and survivor counts, datum conversion, and the land-cover/slope distribution of survivors relative to the project. For spaceborne altimetry, qualify the filtered set against local high-accuracy data *before* using it on the product of interest: if ICESat-2 disagrees with your airborne lidar by 0.4 m RMSE on open flat ground, the filtering or datum handling is wrong and the global DEM comparison will inherit it. [Chapter 53](ch53-accuracy-assessment.md) gives the full template.

## Software

**Open source.** *NGS OPUS* (free service) — static GNSS tied to CORS; the solution report is the control-tie document (peak-to-peak values are not 1σ). *RTKLIB* — PPK/PPP; demands care with antenna models and ambiguity validation. *PDAL* — checkpoint residuals against a TIN from classified ground points. *xdem* — DEM differencing, Nuth–Kääb co-registration, robust statistics. *CloudCompare* — M3C2 distances for TLS and SfM references. *icepyx*, *SlideRule* — ICESat-2 subsetting and on-demand ATL03 processing. *rGEDI* — L2A extraction. *QGIS*, *GMT* (`grdtrack`) — sampling and review.

**Free but closed.** *NOAA HydrOffice QC Tools* — hydrographic QA; *CSRS-PPP*, *AUSPOS* — national static processing.

**Commercial.** *Trimble Business Center*, *Leica Infinity* — checkpoint processing, adjustment, and the reports reviewers expect. *TerraMatch/TerraScan* — strip adjustment and known-point reports (points used in adjustment are not checkpoints). *CARIS HIPS and SIPS*, *QPS Qimera* — reference-surface and crossline tools with TPU. *Global Mapper*, *ArcGIS* — simple comparisons.

## Standards & guides

- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2** (2023; Version 2, 2024) — checkpoint minimums (30 to 120), NVA/VVA strata, inclusion of checkpoint uncertainty, independence from control, per-point reporting.
- **NSSDA** (FGDC-STD-007.3-1998) — RMSE × 1.96 vertical statistic, "tested to meet" language, checkpoint accuracy and distribution guidance.
- **NOAA TM NOS NGS-58** (1997) and **NGS-59** (2008) — GPS-derived ellipsoid and orthometric heights; **NOAA TM NOS NGS 92** (2024), *Classifications, Standards, and Specifications for GNSS Geodetic Control Surveys Using OPUS Projects* — replaces NGS-58/59 for surveys submitted through OPUS Projects.
- **NGS User Guidelines for Single Base Real Time GNSS Positioning** (Henning 2011) — RTK/RTN checkpoint protocols.
- **USGS Lidar Base Specification 2024 rev. A** — checkpoint survey, TIN-based NVA/VVA assessment, deliverables.
- **IHO S-44 Edition 6.1.0** (2022) — orders, TVU/THU, feature detection, crosslines and reference checks.
- **NOAA Field Procedures Manual** and **Hydrographic Surveys Specifications and Deliverables** (current editions) — reference-surface and patch-test procedures, crossline requirements.
- **ISO 19157-1:2023** — quality elements, direct external evaluation against reference data, reporting.

## Pitfalls

- **Checkpoints by the same crew, instrument, base, and epoch as the survey** → convenient; shared errors cancel and a biased product passes → read the control-tie section; require an independent tie.
- **All checkpoints on roads, then claiming vegetated accuracy** → roads are fast → plot checkpoints over land cover; plan strata before fieldwork.
- **An RMSE from 8–15 points** → small budgets → the confidence interval spans nearly a factor of three; publish the chi-square interval and refuse pass/fail below 30.
- **ICESat-2/GEDI as truth under dense canopy or on slopes without filtering** → the segments exist → plot residuals against canopy and slope; filter on beam, background, confidence, slope, cover, and photon count.
- **Lidar in NAVD88 (GEOID18) against benchmarks from the 1991 adjustment or GEOID12B** → both are "NAVD88" → a smooth regional residual pattern betrays it; compare in ellipsoidal heights or apply the model-difference grid.
- **Rod tip in litter, soft ground, or marsh without a stated convention** → the surveyor pushes until it stops → centimetres to decimetres of definition error; specify a plate or convention.
- **A legacy DEM or SRTM as "truth" for a new product** → nothing better at hand → the comparison measures the reference; call it a consistency check.
- **3σ outlier removal with only survivors reported** → flattering → demand the full residual table and exclusion reasons; use NMAD flags and report both.

## Key takeaways

- There is no ground truth, only references with error budgets; write the budget and never quote a product uncertainty smaller than the reference's own.
- Independence and stratification matter more than count; thirty points per reported stratum is the floor.
- Follow a written protocol (NGS-58/59/92 for static, NGS real-time guidelines for RTK/RTN) with redundant occupations, fixed-height poles, photographs, and a named geoid model.
- Reference surfaces test shape, noise, and calibration state in ways scattered points cannot.
- ICESat-2 is excellent quasi-truth over open flat terrain after filtering and poor under canopy or on slopes; GEDI is metre-level; open dense lidar is the best reference for coarse DEMs when aggregated, registered, and matched by surface type.
- Under canopy, in marsh, and on soft seafloor the surface is a convention; state it and treat cross-convention comparisons as definition tests.
- Include checkpoint uncertainty in the accuracy statement and give confidence intervals.
- Benchmarks choose methods; validation datasets accept products.
- Deliver the checkpoint table with residuals as an open, machine-readable file; its metadata must be as rigorous as the product's.

## References

- Adam, M., Urbazaev, M., Dubois, C., & Schmullius, C. (2020). Accuracy assessment of GEDI terrain elevation and canopy height estimates in European temperate forests. *Remote Sensing*, 12(23):3948.
- ASPRS (2015). ASPRS Positional Accuracy Standards for Digital Geospatial Data (Edition 1, Version 1.0, November 2014). *Photogrammetric Engineering & Remote Sensing*, 81(3):A1–A26.
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2* (Version 1.0.0, August 2023; Version 2, 2024). American Society for Photogrammetry and Remote Sensing.
- Bielski, C., López-Vázquez, C., Grohmann, C. H., Guth, P. L., Hawker, L., Gesch, D., Trevisani, S., Herrera-Cruz, V., Riazanoff, S., Corseaux, A., Reuter, H. I., & Strobl, P. (2024). Novel approach for ranking DEMs: Copernicus DEM improves one arc second open global topography. *IEEE Transactions on Geoscience and Remote Sensing*, 62:4503922. doi:10.1109/TGRS.2024.3368015.
- Brunt, K. M., Neumann, T. A., & Smith, B. E. (2019). Assessment of ICESat-2 ice sheet surface heights, based on comparisons over the interior of the Antarctic ice sheet. *Geophysical Research Letters*, 46(22):13072–13078.
- Carabajal, C. C., & Harding, D. J. (2006). SRTM C-band and ICESat laser altimetry elevation comparisons as a function of tree cover and relief. *Photogrammetric Engineering & Remote Sensing*, 72(3):287–298.
- Dubayah, R., Blair, J. B., Goetz, S., et al. (2020). The Global Ecosystem Dynamics Investigation: High-resolution laser ranging of the Earth's forests and topography. *Science of Remote Sensing*, 1:100002.
- FGDC (1998). *Geospatial Positioning Accuracy Standards, Part 3: National Standard for Spatial Data Accuracy*. FGDC-STD-007.3-1998.
- Gesch, D. B. (2018). Best practices for elevation-based assessments of sea-level rise and coastal flooding exposure. *Frontiers in Earth Science*, 6:230.
- Gesch, D. B., Oimoen, M. J., & Evans, G. A. (2014). *Accuracy assessment of the U.S. Geological Survey National Elevation Dataset, and comparison with other large-area elevation datasets—SRTM and ASTER*. USGS Open-File Report 2014-1008.
- Guth, P. L., & Geoffroy, T. M. (2021). LiDAR point cloud and ICESat-2 evaluation of 1 second global digital elevation models: Copernicus wins. *Transactions in GIS*, 25(5):2245–2261.
- Guth, P. L., Van Niekerk, A., Grohmann, C. H., et al. (2021). Digital Elevation Models: Terminology and definitions. *Remote Sensing*, 13(18):3581.
- Hare, R., Eakins, B., & Amante, C. (2011). Modelling bathymetric uncertainty. *International Hydrographic Review*, No. 6:31–42.
- Henning, W. (2011). *User Guidelines for Single Base Real Time GNSS Positioning*, Version 2.1. NOAA National Geodetic Survey (a Version 3.1 followed in 2014).
- Hodgson, M. E., & Bresnahan, P. (2004). Accuracy of airborne lidar-derived elevation: Empirical assessment and error budget. *Photogrammetric Engineering & Remote Sensing*, 70(3):331–339.
- Höhle, J., & Höhle, M. (2009). Accuracy assessment of digital elevation models by means of robust statistical methods. *ISPRS Journal of Photogrammetry and Remote Sensing*, 64(4):398–406.
- IHO (2022). *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. International Hydrographic Organization.
- Liu, A., Cheng, X., & Chen, Z. (2021). Performance evaluation of GEDI and ICESat-2 laser altimeter data for terrain and canopy height retrievals. *Remote Sensing of Environment*, 264:112571.
- Markus, T., Neumann, T., Martino, A., et al. (2017). The Ice, Cloud, and land Elevation Satellite-2 (ICESat-2): Science requirements, concept, and implementation. *Remote Sensing of Environment*, 190:260–273.
- Medeiros, S., Hagen, S., Weishampel, J., & Angelo, J. (2015). Adjusting lidar-derived digital terrain models in coastal marshes based on estimated aboveground biomass density. *Remote Sensing*, 7(4):3507–3525.
- Neuenschwander, A. L., Guenther, E., White, J. C., Duncanson, L., & Montesano, P. (2020). Validation of ICESat-2 terrain and canopy heights in boreal forests. *Remote Sensing of Environment*, 251:112110.
- Qin, N., Tan, W., Ma, L., Zhang, D., & Li, J. (2021). OpenGF: An ultra-large-scale ground filtering dataset built upon open ALS point clouds around the world. *CVPR Workshops*, 1082–1091.
- Reutebuch, S. E., McGaughey, R. J., Andersen, H.-E., & Carson, W. W. (2003). Accuracy of a high-resolution lidar terrain model under a conifer forest canopy. *Canadian Journal of Remote Sensing*, 29(5):527–535.
- Schmid, K. A., Hadley, B. C., & Wijekoon, N. (2011). Vertical accuracy and use of topographic LIDAR data in coastal marshes. *Journal of Coastal Research*, 27(6A):116–132.
- Sithole, G., & Vosselman, G. (2004). Experimental comparison of filter algorithms for bare-Earth extraction from airborne laser scanning point clouds. *ISPRS Journal of Photogrammetry and Remote Sensing*, 59(1–2):85–101.
- Stoker, J., & Miller, B. (2022). The accuracy and consistency of 3D Elevation Program data: A systematic analysis. *Remote Sensing*, 14(4):940.
- U.S. Geological Survey (2024). *Lidar Base Specification 2024 rev. A*. National Geospatial Program.
- Varney, N., Asari, V. K., & Graehling, Q. (2020). DALES: A large-scale aerial LiDAR data set for semantic segmentation. *CVPR Workshops*, 186–187.
- Zilkoski, D. B., D'Onofrio, J. D., & Frakes, S. J. (1997). *Guidelines for Establishing GPS-Derived Ellipsoid Heights (Standards: 2 cm and 5 cm), Version 4.3*. NOAA Technical Memorandum NOS NGS-58.
- Zilkoski, D. B., Carlson, E. E., & Smith, C. L. (2008). *Guidelines for Establishing GPS-Derived Orthometric Heights*. NOAA Technical Memorandum NOS NGS-59.

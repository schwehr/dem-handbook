# Chapter 53 — Accuracy assessment and uncertainty quantification in practice

> **Part XI — Validation, quality, and judging data.** Having established in [Chapter 52](ch52-ground-truth.md) what we compare against, this chapter sets out how the comparison is done, which statistics and standards define the words, and how the result becomes a defensible decision.

**In this chapter.** This is the procedural core of the book's validation argument. You will learn the vocabulary precisely (accuracy, precision, uncertainty; absolute and relative; RMSE, bias, σ, MAE, NMAD, percentiles, LE95/CE90/CE95; "tested" versus "compiled to meet"); the test logic of the standards that use those words—NMAS 1947, NSSDA 1998, ASPRS 2014 and Edition 2 (2023), USGS Lidar Base Specification quality levels, IHO S-44 orders with TVU/THU, ICAO Annex 15, INSPIRE; the procedures for checkpoint comparison, relative and swath-to-swath accuracy, crosslines, and systematic-error detection; how to build an uncertainty budget for lidar, multibeam (TPU), SfM, and InSAR and propagate it to slope, viewshed, and floodplain; why error is spatially structured and why a single RMSE understates local error; what a report must contain; how to assess horizontal, temporal, thematic, completeness, and logical-consistency quality; and how to turn σ into a probability for a threshold decision such as keel clearance or levee freeboard. A runnable Python snippet computes the standard statistics with confidence intervals from a checkpoint table.

## 53.1 Vocabulary

[Chapter 5](ch05-error-and-uncertainty.md) built the statistical toolkit; here the terms are fixed as they will be used in reports. **Accuracy** is closeness to the (reference) truth and includes systematic error; **precision** is repeatability and excludes it; **uncertainty** is a parameter characterizing the dispersion of values that could reasonably be attributed to the measurand (JCGM 100), usually reported as a standard uncertainty (1σ) or an expanded uncertainty at a stated coverage (95 %). **Absolute accuracy** is with respect to the datum; **relative accuracy** is the consistency of the product with itself (point-to-point, swath-to-swath). **Horizontal** and **vertical** accuracy are reported separately; **3D accuracy** combines them.

Let $\varepsilon_i = z_{\text{product},i} - z_{\text{reference},i}$ for $n$ checkpoints. The working statistics are

$$
\mathrm{RMSE} = \sqrt{\tfrac{1}{n}\sum \varepsilon_i^2},\qquad
\bar\varepsilon = \tfrac{1}{n}\sum \varepsilon_i,\qquad
\sigma = \sqrt{\tfrac{1}{n-1}\sum(\varepsilon_i - \bar\varepsilon)^2},\qquad
\mathrm{RMSE}^2 \approx \bar\varepsilon^{\,2} + \sigma^2 ,
$$

plus the **mean absolute error** $\mathrm{MAE} = \frac{1}{n}\sum|\varepsilon_i|$, the **normalized median absolute deviation** $\mathrm{NMAD} = 1.4826\cdot\mathrm{median}(|\varepsilon_i - \mathrm{median}(\varepsilon)|)$ (equal to σ for a normal distribution, robust otherwise; Höhle & Höhle 2009), and the empirical **95th percentile of $|\varepsilon|$**. **LE95** is the linear error at 95 % (vertical); **CE90/CE95** the circular error at 90 %/95 % (horizontal). For normal, zero-mean errors, $\mathrm{LE95} = 1.96\,\mathrm{RMSE}_z$; for circular normal horizontal error with $\mathrm{RMSE}_x = \mathrm{RMSE}_y$, $\mathrm{RMSE}_r = \sqrt{\mathrm{RMSE}_x^2 + \mathrm{RMSE}_y^2}$ and $\mathrm{CE95} = 1.7308\,\mathrm{RMSE}_r$, $\mathrm{CE90} = 1.5175\,\mathrm{RMSE}_r$. These multipliers *assume* normality and zero bias; the 95th percentile does not.

> **Definitions that bite.** NMAS and NSSDA distinguish three claims. **"Tested to meet"** (NSSDA: "Tested ___ (meters) vertical accuracy at 95 % confidence level") means an independent checkpoint test was performed and the statistic computed. **"Compiled to meet"** means the producer followed procedures expected to achieve the class but did not test (NSSDA allows "Compiled to meet ___"). **"Produced to meet"** (ASPRS) is the same idea for the production specification. Only the first is evidence. A metadata record that says "meets NSSDA 95 % vertical accuracy of 18.5 cm" without the word *tested* is a statement of intent.

## 53.2 Standards and their test logic

Each standard encodes a test: which statistic, which threshold, which checkpoints, and what the words mean. Table 53.1 compares them; the paragraphs explain the logic.

| Standard | Vertical statistic | Threshold logic | Strata / checkpoint rule |
|---|---|---|---|
| NMAS 1947 ⟨H⟩ | Fraction of tested points in error by more than ½ contour interval | ≤ 10 % may exceed | Unspecified; "well-defined points" |
| NSSDA 1998 | Accuracy$_z$ = 1.96 × RMSE$_z$ | Report, not pass/fail | ≥ 20 points, spread over quadrants |
| ASPRS 2014 (Ed. 1) | NVA = 1.96 × RMSE$_z$; VVA = 95th percentile | Class by RMSE$_z$; VVA = 3 × RMSE$_z$ pass/fail | 20 NVA + 5 VVA at ≤ 500 km², rising with area |
| ASPRS Ed. 2 (2023/2024) | NVA and VVA both as RMSE$_v$ (VVA reported as found, not pass/fail); 3D = √(RMSE$_x^2$+RMSE$_y^2$+RMSE$_z^2$) | Class by RMSE; checkpoint RMSE added in quadrature | ≥ 30, scaling to 120; per-land-cover reporting |
| USGS LBS 2024 | RMSE$_v$ NVA by QL; VVA reported | QL0 5 cm; QL1/QL2 10 cm; QL3 20 cm | Edition 2 by reference; TIN from ground points |
| IHO S-44 Ed. 6.1.0 | TVU$_{\max}$ = √(a² + (b·d)²) at 95 % | Order: Exclusive a=0.15, b=0.0075; Special 0.25/0.0075; 1a/1b 0.5/0.013; 2 1.0/0.023 | THU: 1 m; 2 m; 5 m + 5 % d; 20 m + 10 % d; feature detection by order |
| ICAO Annex 15 / Doc 10066 | Accuracy and confidence per terrain/obstacle area | Area 1: 30 m / 90 %; Area 2: 3 m / 90 %; Area 3: 0.5 m / 90 %; Area 4: 1 m / 90 % (terrain, vertical) | Integrity classification (routine/essential/critical) |
| INSPIRE Elevation | ISO 19157 positional accuracy elements | Report; no fixed threshold | Data quality metadata mandatory |

*Table 53.1 — Test logic of the principal standards. S-44 and ICAO values are from the respective current editions; always cite the edition used.*

**NMAS 1947 ⟨H⟩** was written for printed maps: horizontally, no more than 10 % of well-defined points may be in error by more than 1/30 inch at publication scale (1/50 inch for scales of 1:20,000 and smaller); vertically, no more than 10 % of interpolated elevations may exceed half the contour interval. It is a percentile test (the 90th percentile ≤ ½ CI), scale-dependent, and silent on sample size. Its legacy is the habit of stating accuracy as "meets NMAS for 2 ft contours," which carries over into "2-foot-contour-equivalent lidar."

**NSSDA 1998** replaced the percentile with an RMSE and a multiplier: $\mathrm{Accuracy}_z = 1.9600\,\mathrm{RMSE}_z$ and $\mathrm{Accuracy}_r = 1.7308\,\mathrm{RMSE}_r$. It prescribes at least 20 checkpoints distributed so that at least 20 % fall in each quadrant and points are at least a tenth of the diagonal apart, requires checkpoints "of the highest accuracy feasible and practicable" (conventionally three times better), and provides the "Tested/Compiled to meet" language. Its weakness is that the 1.96 multiplier is a normality assumption; in vegetated terrain the residuals are skewed and heavy-tailed and the multiplier understates the 95th percentile (Zandbergen 2008).

**ASPRS 2014 (Edition 1)** introduced accuracy *classes* named by RMSE (a "10-cm class" product), split vertical testing into **NVA** (non-vegetated: open terrain and urban, tested at 1.96 × RMSE$_z$) and **VVA** (vegetated: tested at the 95th percentile, with a pass/fail threshold of 3 × RMSE$_z$ of the class), set checkpoint counts by project area, and tied horizontal classes to RMSE$_x$ = RMSE$_y$. **Edition 2 (2023; Version 2, 2024)** made four substantive changes: accuracy is stated by RMSE alone (the 95 % multipliers are dropped from class definitions); VVA is computed as RMSE$_v$ like NVA (the Edition 1 95th-percentile VVA is gone) and is reported as found, no longer pass/fail, in recognition that its distribution and its reference are both ill-behaved; the checkpoint survey's own RMSE is combined with the test RMSE in quadrature, $\mathrm{RMSE}_{\text{reported}} = \sqrt{\mathrm{RMSE}_{\text{test}}^2 + \mathrm{RMSE}_{\text{check}}^2}$, in exchange for relaxing the old 3× requirement; and a **3D accuracy** $\mathrm{RMSE}_{3D}$ is defined. Minimum checkpoints rose to 30 with a cap of 120, and horizontal testing of lidar (via intensity-visible features or targets) is expected rather than waived.

**USGS Lidar Base Specification 2024** maps the ASPRS classes onto **quality levels**: QL0 (RMSE$_v$ ≤ 5 cm, ≥ 8 pls/m²), QL1 (≤ 10 cm, ≥ 8 pls/m²), QL2 (≤ 10 cm, ≥ 2 pls/m²), QL3 (≤ 20 cm, ≥ 0.5 pls/m²), with VVA reported, NVA assessed against a TIN of ground-classified points, and relative-accuracy limits for smooth-surface precision and swath-overlap difference by QL ([Chapter 18](ch18-topographic-lidar.md)).

**IHO S-44 Edition 6.1.0 (2022)** specifies a maximum allowable **Total Vertical Uncertainty** at 95 % as a function of depth $d$, $\mathrm{TVU}_{\max}(d) = \sqrt{a^2 + (b\,d)^2}$, where $a$ collects depth-independent terms (tide, draft, heave, datum) and $b\,d$ depth-proportional terms (sound speed, refraction). For Special Order ($a = 0.25$ m, $b = 0.0075$) at 20 m depth, $\mathrm{TVU}_{\max} = \sqrt{0.0625 + 0.0225} = 0.29$ m; for Order 1a ($a = 0.5$, $b = 0.013$) at 20 m, 0.56 m. **Total Horizontal Uncertainty** is likewise 95 %: 1 m (Exclusive), 2 m (Special), 5 m + 5 % of depth (1a/1b), 20 m + 10 % of depth (2). The crucial difference from the land standards is that S-44 is a *requirement on the uncertainty model* of every sounding—demonstrated by TPU computation, crosslines, and reference surfaces—rather than a post-hoc checkpoint test, and that it adds **feature detection** (cubic features of 0.5 m for Exclusive, 1 m for Special, 2 m to 40 m depth then 10 % of depth for 1a) and **feature search** coverage (200 %, 100 %, 100 %, 5 %, 5 %). Edition 6 also introduced a *matrix* approach that lets an authority specify each parameter independently of the orders ([Chapter 20](ch20-sonar.md), [Chapter 70](ch70-specifications-guided-tour.md)).

**ICAO Annex 15 and PANS-AIM (Doc 10066)** define terrain and obstacle data requirements by **area**: Area 1 (whole state), Area 2 (terminal control area), Area 3 (aerodrome movement area), Area 4 (Category II/III approach). Each has a vertical accuracy, a confidence level (typically 90 %), an integrity classification, and a post spacing; the accuracy statement is thus a confidence-at-threshold claim, not an RMSE ([Chapter 62](ch62-navigation-and-charting.md)). **INSPIRE** Elevation requires data-quality reporting using the ISO 19157 elements (absolute/relative positional accuracy, completeness, logical consistency) without fixing thresholds.

<!-- figure: Figure 53.1 — Timeline and logic diagram of accuracy standards: NMAS percentile test → NSSDA RMSE × 1.96 → ASPRS classes with NVA/VVA → Edition 2 RMSE-only with checkpoint error in quadrature; parallel track for S-44 Editions 4–6 with the TVU curve plotted against depth for each order. -->

## 53.3 Procedures

### 53.3.1 Checkpoint comparison: point to surface

The product value at a checkpoint must be *interpolated*, not read from the nearest cell or nearest point. For a gridded DEM, bilinear interpolation of the four surrounding cell values is the minimum; for a point cloud or classified ground points, the USGS LBS prescribes a TIN of ground points and the elevation of the facet containing the checkpoint. Nearest-cell sampling adds an error of up to half a cell times the slope: on a 1 m grid in 10° terrain that is 9 cm, comparable to the specification being tested. The checkpoint must also fall where the surface is defined—not in a void, not on a hydro-flattened water body, not inside a building footprint—and the product's surface type (DSM, DTM) must match what the rod measured. Interpolate in the product's native grid before any reprojection, because resampling blurs.

### 53.3.2 Relative accuracy and internal consistency

Relative accuracy is tested without external truth. For lidar, **intra-swath** (smooth-surface) precision is the standard deviation of elevations on a planar hard surface within one swath (LBS limits by QL), and **inter-swath** (swath-to-swath) accuracy is the RMS of differences between overlapping swaths on hard surfaces; Latypov (2002) formalized estimating relative accuracy from overlaps. Both are computed on flat, open surfaces to exclude slope-induced apparent differences and reported as RMS and as a map of signed differences, because a map reveals roll (a cross-track gradient), pitch (along-track offsets of features), heading (rotation at swath edges), and range scale (differences growing with range) as distinct patterns ([Chapter 18](ch18-topographic-lidar.md), [Chapter 25](ch25-calibration-infrastructure.md)). For multibeam, **crosslines** run perpendicular to the mainscheme lines at a prescribed fraction of line-kilometres (NOAA HSSD: at least 4 % of mainscheme multibeam line-nautical-miles) and their soundings are compared with the mainscheme surface, binned by beam angle and depth; a difference growing with beam angle is refraction, a constant offset is tide or draft, a periodic difference is heave or motion latency ([Chapter 20](ch20-sonar.md)). For photogrammetry, overlap statistics of independent strips and the residuals of tie points in the bundle adjustment play the same role ([Chapter 22](ch22-photogrammetry-sfm.md)).

### 53.3.3 Systematic error detection

Compute the residuals by strip, by flight day, by scan angle, by range, by beam angle, by time of day, and by land-cover and slope class, and test each grouping for a non-zero mean (a t-test or, robustly, a sign test). A strip mean that differs from the project mean by more than about twice its standard error is a strip bias—usually a trajectory or boresight issue—and must be fixed, not averaged away. A residual trend with scan angle indicates range or angular calibration; with time, a GNSS or atmospheric effect; with slope and aspect, a horizontal shift (Nuth & Kääb 2011 give the closed form: $\Delta z = a\cos(b - \psi)\tan\theta + c$, where $\psi$ is aspect, $\theta$ slope, and $a, b, c$ encode the shift magnitude, direction, and vertical offset).

### 53.3.4 Outliers and strata

Flag $|\varepsilon_i - \mathrm{median}| > 3\,\mathrm{NMAD}$, investigate each flagged point against the point cloud, imagery, and the checkpoint record, classify it as *checkpoint blunder*, *surface change*, or *product error*, and report statistics with and without exclusions and the classification of every excluded point ([Chapter 52](ch52-ground-truth.md)). Report by stratum: at minimum NVA and VVA, better land-cover classes and slope classes, each with $n$, mean, σ, RMSE, NMAD, 95th percentile, and the confidence interval on RMSE.

## 53.4 Uncertainty budgets

A checkpoint test tells you how wrong a product *was* where you tested it. An uncertainty budget tells you how wrong it *should be* everywhere, from the physics of its construction, and is the only option where no checkpoints exist (the deep sea, the past, another planet). Both are needed: the budget predicts, the test confirms or exposes the term you forgot.

### 53.4.1 Component propagation

For a measurement $z = f(x_1, \dots, x_m)$ with input uncertainties collected in a covariance matrix $\Sigma_x$, first-order propagation gives $\sigma_z^2 = J\,\Sigma_x\,J^{\mathsf T}$ with $J = \partial f/\partial x$ (JCGM 100). For airborne lidar the inputs are the GNSS position, the IMU attitude, the boresight angles, the lever arm, the scanner angle, and the range; Baltsavias (1999) gives the basic relations and Glennie (2007) the rigorous 3D treatment. The structure is instructive: a roll error $\delta\omega$ at range $R$ produces a vertical error that grows with scan angle $\beta$ as roughly $R\,\delta\omega\sin\beta$ and a horizontal error $R\,\delta\omega\cos\beta$—so at 1,500 m range, 0.005° (0.09 mrad) of roll is 13 cm horizontally at nadir and 5 cm vertically at 20° off-nadir—while a range error maps directly into the vertical at nadir. This is why vertical accuracy at nadir on flat ground is the easy case and why slope and scan angle must be reported with it.

> **Uncertainty budget.** Representative 1σ vertical components for a modern airborne topographic lidar at 1,500 m AGL over flat hard ground (values indicative; derive your own from the manufacturer's specifications and your trajectory report):
>
> | Component | 1σ vertical (cm) | Scales with |
> |---|---|---|
> | GNSS kinematic position (PPK, short baseline) | 3–5 | Baseline length, geometry |
> | IMU attitude (0.005° roll/pitch) at 20° off-nadir | 2–5 | Range × sin(scan angle) |
> | Boresight residual after calibration | 1–3 | Range, scan angle |
> | Range (timing, waveform detection) | 1–2 | Target reflectance, incidence |
> | Lever arm | < 1 | Attitude |
> | Geoid model (if orthometric) | 1–3 | Region; cancels vs. same-model checkpoints |
> | Ground-point classification / interpolation on hard flat ground | 1–2 | Surface roughness, density |
> | **Combined (RSS)** | **≈ 5–8** | — |
>
> The combined figure is consistent with the 5–10 cm NVA actually achieved by QL1/QL2 programmes. On a 20° slope, add $\sigma_{xy}\tan 20° \approx 0.36\,\sigma_{xy}$—with $\sigma_{xy} \approx 15$ cm that is another 5 cm. Under canopy the classification term dominates and the budget is no longer Gaussian.

### 53.4.2 Hydrographic TPU

For multibeam the equivalent is the **Total Propagated Uncertainty** model (Hare 1995; Hare, Godin & Mayer 1995), which propagates, per beam, the uncertainties in sounder range and beam angle, sound-speed profile and surface sound speed (refraction grows with beam angle), roll, pitch, heading, heave, latency, draft, squat, loading, tide or ellipsoid-to-datum separation, and horizontal position, into a vertical and horizontal uncertainty for every sounding. These TPU values are the inputs that CUBE (Calder & Mayer 2003) uses to weight soundings into a gridded surface with an uncertainty layer, which is what BAG and S-102 carry ([Chapter 47](ch47-file-formats.md)). S-44 compliance is demonstrated by showing that the TPU at 95 % is below $\mathrm{TVU}_{\max}(d)$ for the order, and crosslines then test whether the model is honest. The water-level term is often the largest shallow-water component: a 10 cm tidal zoning error is 10 cm of TVU before any sonar error is counted ([Chapter 9](ch09-vertical-datums.md), [Chapter 20](ch20-sonar.md)).

### 53.4.3 SfM, InSAR, and gridded error surfaces

For structure-from-motion, the bundle adjustment's covariance can be propagated to each sparse point and interpolated into a **precision map** (James, Robson & Smith 2017), which reveals the doming and edge degradation characteristic of weakly constrained self-calibrating networks; precision maps are the right denominator for change detection with SfM ([Chapter 22](ch22-photogrammetry-sfm.md), [Chapter 41](ch41-change-detection.md)). For InSAR DEMs the height error follows from the phase error through the **height of ambiguity** $h_a$: $\sigma_h = \frac{h_a}{2\pi}\,\sigma_\phi$, with $\sigma_\phi$ set by coherence and the number of looks; TanDEM-X delivers this as a per-pixel Height Error Map (Rizzoli et al. 2017), and low coherence (vegetation, water, layover) is where the HEM is large ([Chapter 21](ch21-radar-sar-insar.md)). For legacy or composite DEMs with no propagation available, an **error surface** is modelled empirically from residuals against reference data as a function of slope, roughness, land cover, and source (Wechsler 2007; Fisher & Tate 2006), and that surface, not a scalar, is what should be delivered.

### 53.4.4 Propagation to derivatives

Slope, aspect, curvature, viewsheds, watersheds, and inundation extents are nonlinear functions of neighbourhoods of cells, and their uncertainty depends on the *spatial correlation* of the DEM error as much as on its magnitude (§53.5). Analytical propagation is possible for slope (Hunter & Goodchild 1997; Oksanen & Sarjakoski 2005): for a central-difference gradient $(z_{i+1} - z_{i-1})/(2\Delta)$ on a grid of spacing $\Delta$ with uncorrelated cell errors σ, the per-axis gradient standard deviation is $\sigma\sqrt{2}/(2\Delta) = \sigma/(\sqrt{2}\,\Delta)$—so a 30 m DEM with σ = 3 m has gradient uncertainty about 0.07 (4°) per axis even on flat ground, and finer grids make it *worse*, not better, for the same σ. For everything else, **Monte Carlo** simulation is the practical route: generate many realizations of the error field with the fitted variogram (sequential Gaussian simulation; Heuvelink 1998; Temme et al. 2009), add each to the DEM, recompute the derivative, and summarize the ensemble as a mean, a standard deviation, and probability maps (probability a cell is inundated; probability a cell is visible). The xdem library implements this chain for DEM differences (Hugonnet et al. 2022).

## 53.5 Spatial structure of error

DEM error is not white noise. It is correlated over distances set by the acquisition geometry (swath width, strip length, image footprint, InSAR baseline), by the terrain (steep slopes and forests cluster), and by processing (interpolation smooths, tile-based processing introduces edges). Shortridge & Messina (2011) showed SRTM error correlated with slope, aspect, and land cover with coherent spatial patterns; Holmes, Chadwick & Kyriakidis (2000) found USGS 30 m DEM error autocorrelated over hundreds of metres and showed its consequences for hydrologic derivatives; Rolstad, Haug & Denby (2009) derived how the uncertainty of a *mean* elevation change over an area depends on the correlation length, and Hugonnet et al. (2022) generalized this to multi-range variograms estimated from stable terrain.

The practical consequences are three. First, the uncertainty of a spatial average does not fall as $1/\sqrt{N}$ cells but as $1/\sqrt{N_{\text{eff}}}$, where $N_{\text{eff}} \approx A/(\pi L^2)$ for area $A$ and correlation length $L$—a 1 km² area with σ = 0.5 m and $L$ = 200 m has $N_{\text{eff}} \approx 8$, so the mean is uncertain by about 0.18 m, not the 0.0005 m that counting 10⁶ one-metre cells would suggest. Second, derivatives that difference neighbouring cells (slope, curvature) are *insensitive* to long-wavelength error and *hypersensitive* to short-wavelength error, the reverse of volumes and means. Third, a global RMSE averages over strata with very different errors and hides the local 1–2 m errors under forest inside a 0.3 m project figure; error must be mapped, and the **variogram of residuals** (empirical semivariance $\gamma(h) = \frac{1}{2N(h)}\sum(\varepsilon_i - \varepsilon_j)^2$ for pairs at lag $h$, fitted with a spherical or exponential model) is the standard instrument for characterizing it. Resolution interacts with all of this: coarsening a grid averages short-wavelength error (reducing per-cell σ) while leaving long-wavelength error untouched and adding representation error on slopes ([Chapter 44](ch44-resolution-and-sampling.md)).

<!-- figure: Figure 53.2 — Empirical variogram of DEM residuals against reference lidar with a fitted two-range model (short range ≈ 50 m from interpolation noise, long range ≈ 2 km from strip/tile effects), beside a map of the residuals showing both scales. -->

## 53.6 Reporting

An accuracy report is evidence, and evidence must be reproducible. The ASPRS Edition 2 reporting guidance and the LBS deliverables converge on the following content; use it as a template.

1. **Product tested**: identifier, version, surface type (DSM/DTM/bathymetric surface), CRS with geoid model and epoch, resolution, extent, acquisition dates.
2. **Reference data**: source, method, instrument, control tie, datum realization, epoch, checkpoint RMSE and how it was estimated, independence statement ([Chapter 52](ch52-ground-truth.md)).
3. **Procedure**: interpolation method (bilinear / TIN), stratification rules, outlier policy, software and version.
4. **Per-stratum table**: $n$, mean, σ, RMSE, NMAD, MAE, 95th percentile, min/max, 95 % confidence interval on RMSE; for Edition 2, the test RMSE, the checkpoint RMSE, and the combined reported RMSE.
5. **Standard statement**, verbatim in the standard's form: for example "Tested 0.081 m RMSE$_v$ (NVA, 42 checkpoints) in accordance with ASPRS Positional Accuracy Standards Edition 2; VVA 0.16 m RMSE$_v$ (31 checkpoints), reported as found," or "Soundings meet IHO S-44 Ed. 6.1.0 Order 1a TVU and THU at 95 % confidence; TPU computed per sounding; crossline comparison RMS 0.18 m (n = 41,220 soundings)."
6. **Relative accuracy**: intra-swath σ, inter-swath RMS and map; crossline statistics by beam sector and depth.
7. **Residual maps and plots**: residuals over land cover, histogram per stratum, residual versus slope/scan angle/time, variogram.
8. **Uncertainty layer**: where a per-cell uncertainty raster or TPU grid exists, deliver it as a band or companion file (BAG/S-102 uncertainty layer; TanDEM-X HEM; a σ raster for lidar DEMs built from the error model), with its definition (1σ, 95 %, which components).
9. **Exclusions**: every excluded checkpoint with reason.
10. **Failure handling**: if the product fails, say which stratum, by how much, the likely cause, and what was done (re-adjustment, reflight, rejection, acceptance with a documented deviation). A failed test is a finding, not an embarrassment to be reworded.

Confidence statements must match the test. Where a 95th percentile is also reported (the USGS LBS still asks for it in vegetated classes), remember that from 31 points it has a standard error of roughly the spread of the top three values, so "VVA 0.31 m" should read "VVA 0.31 m (95th percentile; 31 points; bootstrap 90 % interval 0.24–0.46 m)."

## 53.7 Beyond vertical

**Horizontal accuracy** of a DEM is hard to test because bare earth has few well-defined points. The methods are: targets or painted features visible in lidar intensity or orthoimagery, compared with surveyed positions; edge-based methods that match breaklines (roof edges in a DSM, road crowns, channel banks) between product and reference and solve for a shift; and co-registration against a reference DEM over stable sloped terrain (Nuth & Kääb 2011), which yields a horizontal shift vector and its uncertainty from the aspect-dependence of residuals. A typical lidar project achieves RMSE$_r$ of a few decimetres; it is rarely tested unless the contract requires it, which Edition 2 now encourages.

**Temporal accuracy** is the uncertainty in *when* the surface was as described—acquisition date ranges, per-cell date layers in composites, and the change expected between acquisition and use ([Chapter 37](ch37-time-scales-of-change.md)). **Thematic accuracy** of classification labels (ground, building, vegetation, water, bridge) is a confusion matrix against a labelled reference sample with producer's and user's accuracy per class; ASPRS lidar guidelines call for a classification accuracy check, and the choice of classes and the reference labelling protocol dominate the result ([Chapter 42](ch42-object-detection-semantics.md)). **Completeness** is the fraction of the area with valid measurements (voids, masked water, low-density holes), reported as a percentage and a mask ([Chapter 35](ch35-voids-and-overhangs.md)). **Logical consistency** covers topological and semantic rules: hydro-flattened water bodies are level, hydro-enforced drainage is monotonic, no cells are below the sounding datum where the survey says dry land, bridges are treated as declared, tile edges match ([Chapter 34](ch34-water-in-dems.md), [Chapter 61](ch61-hydrology.md)). ISO 19157-1 names all of these as data-quality elements and INSPIRE requires them to be reported.

## 53.8 Decision-oriented uncertainty quantification

A number in a report is not the purpose of uncertainty quantification; a defensible decision is. The translation is a probability statement about a threshold.

If the quantity of interest $z$ (a depth, a levee crest height, a ground elevation) is estimated as $\hat z$ with standard uncertainty $\sigma$ and approximately normal error, the probability that the true value is on the wrong side of a threshold $T$ is

$$
P(z < T) = \Phi\!\left(\frac{T - \hat z}{\sigma}\right),
$$

where $\Phi$ is the standard normal CDF. The same formula, with $\sigma$ replaced by the combined uncertainty of the *difference* between two uncertain quantities, answers "will the keel clear?" and "is the levee higher than the design flood?" (compare the level-of-detection threshold in [Chapter 41](ch41-change-detection.md)).

> **Worked example.** *Keel clearance.* A charted depth over a shoal is 12.0 m at chart datum from a survey meeting Order 1a (TVU at 95 % of 0.52 m at 12 m, so σ ≈ 0.52/1.96 = 0.27 m). A ship with 10.5 m draught transits at a predicted tide of +0.6 m with tidal prediction uncertainty σ ≈ 0.15 m and squat of 0.5 m (σ ≈ 0.1 m); the port requires a net under-keel clearance of at least 0.5 m. Available water: $12.0 + 0.6 - 0.5 = 12.1$ m; required: $10.5 + 0.5 = 11.0$ m; margin $\hat m = 1.1$ m; combined $\sigma_m = \sqrt{0.27^2 + 0.15^2 + 0.10^2} = 0.32$ m. Probability the margin is negative: $\Phi(-1.1/0.32) = \Phi(-3.4) \approx 3\times10^{-4}$. Under an Order 2 survey (σ ≈ 0.53 m at 12 m) $\sigma_m = 0.56$ m and $P = \Phi(-1.96) \approx 0.025$—one transit in forty violates the clearance rule. That is the value of the better survey, and it is computable before the survey is bought. If the seabed is mobile and the survey is five years old, add a morphologic-change term; if the error distribution has a shoal-biased tail (missed features), the normal model understates the risk and feature-detection compliance matters more than TVU.
>
> *Levee freeboard.* A levee crest is measured by lidar at 7.40 m NAVD88 (σ = 0.08 m, including checkpoint error and a 0.03 m geoid term) against a design water surface of 6.80 m (σ = 0.25 m from the hydraulic model). Freeboard $\hat f = 0.60$ m; $\sigma_f = \sqrt{0.08^2 + 0.25^2} = 0.26$ m; $P(f < 0) = \Phi(-2.3) \approx 0.011$. The DEM contributes 9 % of the variance; the hydraulic model, 91 %. Spending on better lidar would barely move this probability; spending on the hydraulic model would. The expected-loss framing—probability × consequence—then tells you whether 1 % is acceptable for the asset at risk, and the **value of information** of a new survey is the expected reduction in loss it buys, which here is small for lidar and large for better hydrology.

For a parcel-in-floodplain question the same logic applies cell by cell: with a base flood elevation $B$ and a DEM cell $\hat z$ with σ, $P(\text{inundated}) = \Phi((B - \hat z)/\sigma)$, and a map of that probability is more useful to a property owner, and more honest, than a line. FEMA's elevation guidance accepts lidar meeting specified accuracy for floodplain mapping, but the probability framing is what connects that accuracy to the decision ([Chapter 61](ch61-hydrology.md)).

<!-- figure: Figure 53.3 — Decision diagram for a threshold question: estimated value with its σ, the threshold, the shaded tail probability, and the same for two survey orders; inset shows a probability-of-inundation map replacing a binary floodplain boundary. -->

## Then & now

- **Contour-interval tests ⟨H⟩.** NMAS (1947) tested paper maps by percentile against half a contour interval; accuracy was a property of a map sheet and sample size went unmentioned.
- **NSSDA RMSE (1998).** Digital data brought RMSE × 1.96, the 20-point minimum, and "tested/compiled to meet." Hydrography moved in parallel from S-44 Edition 3's fixed tables to Edition 4's (1998) depth-dependent TVU formula.
- **Quality-level frameworks and stratified tests (2010s).** ASPRS 2014 introduced RMSE-named classes and the NVA/VVA split; the USGS LBS tied them to quality levels and pulse densities; S-44 Edition 5 (2008) added feature detection.
- **Delivered uncertainty (2010s–).** BAG (2006 onward) and S-102 carry an uncertainty layer per cell; TanDEM-X ships a height error map; CUBE made uncertainty an input to gridding rather than an afterthought.
- **RMSE-only classes and budgeted checkpoints (2023–).** ASPRS Edition 2 dropped the 95 % multipliers from class definitions, made VVA report-only, folded checkpoint error into the statement, and added 3D accuracy. Spaceborne altimetry and open lidar made independent testing routine ([Chapter 52](ch52-ground-truth.md)).
- **Probabilistic products and decision analytics.** Monte Carlo propagation, probability-of-inundation maps, and uncertainty-aware under-keel-clearance systems turn σ into decisions; the open problem ([Chapter 73](ch73-open-problems.md)) is delivering spatially correlated uncertainty, not just per-cell σ.

## Mathematics

**Decomposition.** $\mathrm{RMSE}^2 = \bar\varepsilon^{\,2} + \frac{n-1}{n}\sigma^2 \approx \bar\varepsilon^{\,2} + \sigma^2$. Report both terms: a 10 cm RMSE made of 8 cm bias and 6 cm σ is a datum problem; one made of 1 cm bias and 10 cm σ is noise.

**Chi-square test for an RMSE claim.** To test $H_0: \sigma \le \sigma_0$ (the class limit) against the sample RMSE $s$ from $n$ normal zero-mean residuals, compute $\chi^2 = n s^2/\sigma_0^2$ and reject if it exceeds $\chi^2_{n,\,1-\alpha}$. With $n = 30$, $\alpha = 0.05$, $\chi^2_{30,0.95} = 43.77$, so rejection requires $s > \sigma_0\sqrt{43.77/30} = 1.21\,\sigma_0$: a 30-point test cannot distinguish a 10 cm product from a 12 cm one. The confidence interval on RMSE in [Chapter 52](ch52-ground-truth.md) is the dual statement.

**Percentile confidence intervals.** For the $p$-th sample percentile from $n$ observations, the order statistics $x_{(l)}$ and $x_{(u)}$ with $l, u = np \pm z_{\alpha/2}\sqrt{np(1-p)}$ bracket the true percentile with approximate confidence $1-\alpha$. For $p = 0.95$, $n = 31$: $np = 29.45$, $\sqrt{np(1-p)} = 1.21$, so the 90 % interval runs from roughly the 27th to the 31st order statistic—essentially the top five residuals. A bootstrap gives the same answer with less algebra.

**Variance propagation and Monte Carlo.** $\Sigma_z = J\,\Sigma_x\,J^{\mathsf T}$ for linearizable functions (JCGM 100); for nonlinear derivatives, JCGM 101 prescribes Monte Carlo. To honour spatial correlation, simulate error fields with the fitted variogram $\gamma(h)$ by sequential Gaussian simulation or spectral methods, so that each realization has the right covariance $C(h) = \sigma^2 - \gamma(h)$; the ensemble of recomputed derivatives then has correct, not merely plausible, spread.

**Variogram fitting.** Fit $\gamma(h) = c_0 + c_1\,g_1(h/a_1) + c_2\,g_2(h/a_2)$ (nugget plus nested spherical or exponential structures) to the empirical semivariance of residuals on stable terrain by weighted least squares; the ranges $a_1, a_2$ are the correlation lengths that enter $N_{\text{eff}}$ (§53.5; Hugonnet et al. 2022).

**S-44 TVU.** $\mathrm{TVU}_{\max}(d) = \sqrt{a^2 + (b\,d)^2}$ at 95 %; the sounding's own TPU is $\sigma_{\text{TPU}} \cdot 1.96$ and compliance is $1.96\,\sigma_{\text{TPU}} \le \mathrm{TVU}_{\max}(d)$ for every sounding.

## Validation & uncertainty

This chapter is about validating products; this section is about validating the *assessment*. Three failure modes recur.

**The assessment measures the wrong thing.** Nearest-cell sampling, mismatched surface types (rod on ground versus DSM), mismatched datums (ellipsoidal checkpoints against an orthometric DEM: a 20–40 m "bias" that is simply the geoid), mismatched epochs, and checkpoints inside voids or hydro-flattened polygons all produce statistics that describe the test, not the product. The defence is the procedure of §53.3 and a residual map: artefacts of the test have spatial patterns that product errors do not (a constant offset equal to the local geoid height; a residual proportional to slope).

**The assessment is underpowered or overstated.** Thirty points cannot certify a 10 cm product against a 12 cm alternative (Mathematics); a 95th percentile from 31 points has a wide interval; a single project-wide RMSE averages a passing stratum with a failing one. State the interval, state $n$ per stratum, and let the confidence statement be no stronger than the test.

**The budget omits a term.** Budgets built only from random components (GNSS noise, ranging noise) and compared with a test that passed produce false confidence; the terms that bite are systematic—datum realization, geoid model, boresight drift, tidal zoning, sound-speed structure, canopy classification—and they appear in the test as bias by stratum, by strip, or by region. When test and budget disagree, the test is usually right about the magnitude and the budget about the cause; reconcile them rather than reporting whichever looks better.

> **Try it.** Compute the standard statistics with confidence intervals from a checkpoint CSV (`id, x, y, z_ref, z_dem, stratum`). Expected output: a per-stratum table with $n$, mean, σ, RMSE with its 95 % chi-square interval, NMAD, 95th percentile with a bootstrap interval, and a flag list. For the example numbers of §53.6 the NVA row should show RMSE ≈ 0.079 m with an interval of roughly 0.065–0.100 m.
>
> ```python
> import numpy as np, pandas as pd
> from scipy import stats
>
> df = pd.read_csv("checkpoints.csv")
> df["eps"] = df["z_dem"] - df["z_ref"]            # product minus reference
> rng = np.random.default_rng(0)
>
> def summarize(e, sigma_check=0.0, alpha=0.05, nboot=5000):
>     e = np.asarray(e, float); n = e.size
>     rmse = np.sqrt(np.mean(e**2))
>     lo = rmse * np.sqrt(n / stats.chi2.ppf(1 - alpha/2, n))
>     hi = rmse * np.sqrt(n / stats.chi2.ppf(alpha/2, n))
>     med = np.median(e); nmad = 1.4826 * np.median(np.abs(e - med))
>     p95 = np.percentile(np.abs(e), 95)
>     boot = [np.percentile(np.abs(rng.choice(e, n)), 95) for _ in range(nboot)]
>     flags = np.flatnonzero(np.abs(e - med) > 3 * nmad)
>     return dict(n=n, mean=e.mean(), sd=e.std(ddof=1), rmse=rmse, rmse_lo=lo, rmse_hi=hi,
>                 rmse_ed2=np.sqrt(rmse**2 + sigma_check**2),      # ASPRS Ed. 2 reported value
>                 nmad=nmad, p95=p95, p95_lo=np.percentile(boot, 5), p95_hi=np.percentile(boot, 95),
>                 n_flagged=flags.size)
>
> rows = {s: summarize(g["eps"], sigma_check=0.018 if s == "NVA" else 0.040)
>         for s, g in df.groupby("stratum")}
> print(pd.DataFrame(rows).T.round(3).to_string())
> ```

## Software

**Open source.** *xdem* — DEM differencing, co-registration, variogram estimation on stable terrain, spatially correlated error propagation (Hugonnet et al. 2022); the reference implementation of §53.5. *demcoreg* — Nuth–Kääb and ICP co-registration for DEM pairs. *PDAL* and *lidR* — swath-overlap and checkpoint-versus-TIN QC for point clouds. *CloudCompare* — M3C2 distances with per-point uncertainty. *R gstat / geoR* — variograms and sequential Gaussian simulation. *QGIS* — residual mapping and point sampling. *MB-System* — crossline and reference-surface comparison for multibeam (`mbgrid`, `mbnavadjust`). *GMT* — `grdtrack`, `blockmedian`, and profile statistics.

**Free but closed.** *NOAA HydrOffice QC Tools* — grid QA, flier finder, and S-44/HSSD checks on BAGs.

**Commercial.** *TerraMatch/TerraScan* — strip adjustment and control reports. *LP360* — ASPRS Edition 2 accuracy reports with checkpoint-error combination. *CARIS HIPS and SIPS* — TPU computation, CUBE, crossline QC. *QPS Qimera* — CUBE surfaces with uncertainty layers. *ArcGIS*, *Global Mapper*, *GeoCue* — checkpoint tools and QA workflows; verify which interpolation they use at checkpoints.

## Standards & guides

- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2** (2023; Version 2, 2024) — RMSE classes, NVA/VVA, 3D accuracy, checkpoint error combination, reporting template.
- **NSSDA** (FGDC-STD-007.3-1998) — RMSE × 1.96 and × 1.7308, tested/compiled language.
- **U.S. Bureau of the Budget, National Map Accuracy Standards** (1947) — percentile contour test ⟨H⟩.
- **USGS Lidar Base Specification 2024 rev. A** — QL0–QL3, NVA/VVA, relative accuracy limits, deliverables.
- **IHO S-44 Edition 6.1.0** (2022) — TVU/THU, orders, feature detection and search, matrix; **IHO S-67 Edition 1.0.0** (2020) — mariners' guide to accuracy of depth information in ENCs (CATZOC).
- **NOAA Hydrographic Surveys Specifications and Deliverables** (current edition) — TPU, crossline, and reporting requirements for NOAA surveys.
- **ICAO Annex 15** (16th edition, 2018) and **PANS-AIM Doc 10066** — terrain/obstacle accuracy, confidence, and integrity by area.
- **ISO 19157-1:2023** — data-quality elements (positional, thematic, temporal accuracy; completeness; logical consistency) and evaluation reporting.
- **JCGM 100:2008 (GUM)** and **JCGM 101:2008** — uncertainty propagation and Monte Carlo.
- **FEMA Guidelines and Standards for Flood Risk Analysis and Mapping — Elevation Guidance** (current edition) (verify) — accepted elevation accuracy for floodplain mapping.
- **INSPIRE Data Specification on Elevation** (D2.8.II.1, v3.0, 2013) — quality reporting requirements.

## Pitfalls

- **Treating RMSE as the 95 % error** → the two are conflated in metadata → a 10 cm RMSE product has 95 % errors near 20 cm if normal and larger if not; always state the statistic and multiplier.
- **Declaring VVA pass/fail, or reporting it as a 95th percentile under Edition 2** → Edition 1 habit → Edition 2 and LBS 2024 report VVA as RMSE$_v$ as found; test it, map it, explain it.
- **Nearest-cell checkpoint sampling** → it is one line of code → inflates error on slopes by up to ½ cell × slope; interpolate bilinearly or against a TIN.
- **Ellipsoidal checkpoints against an orthometric DEM (or vice versa)** → the geoid field was not read → a smooth 20–40 m "bias"; check the datum before the first statistic.
- **Propagating only random terms** → they are the ones in the spec sheet → budget predicts 5 cm, test finds a 12 cm strip bias; include datum, geoid, boresight, tide, sound speed, classification.
- **One number for a continent (or a county)** → the standard asks for "the" RMSE → report per stratum and deliver an uncertainty raster; a global RMSE hides forest and slope.
- **Thirty points declaring a 10 cm product "within specification" at 9.5 cm** → the interval was not computed → the 95 % interval reaches 12.7 cm; say "consistent with."
- **Crosslines evaluated only as a global RMS** → convenient → refraction, tide, and latency each have signatures by beam angle, time, and depth; bin the differences.
- **Uncorrelated Monte Carlo error fields** → simpler to generate → derivative uncertainties are wrong by factors (too large for slope, too small for volumes); use the fitted variogram.
- **Rewording a failed test** → contractual pressure → a failure is a finding; report it with cause and remedy.

## Key takeaways

- Say which statistic, which standard and edition, which checkpoints, which strata, and with what confidence interval; a bare RMSE is not a result.
- Interpolate the product at the checkpoint; match surface type, datum, and epoch before computing anything.
- Standards differ in logic—percentile (NMAS, Edition 1 VVA, ICAO), RMSE (NSSDA, ASPRS, LBS), uncertainty-model compliance (S-44 TVU/THU)—and the words "tested," "compiled," and "produced to meet" mean different things.
- Under ASPRS Edition 2, NVA is RMSE$_v$ with checkpoint error added in quadrature, VVA is RMSE$_v$ reported as found rather than pass/fail, and 3D accuracy exists.
- Budgets predict and tests confirm; when they disagree, find the missing systematic term.
- Error is spatially correlated; $N_{\text{eff}}$, not $N$, governs the uncertainty of averages, and variograms of residuals belong in the report.
- Deliver uncertainty spatially (σ rasters, TPU layers, HEM) and propagate it to derivatives by Monte Carlo with correlated fields.
- The point of UQ is a defensible decision: convert σ to a probability at the threshold, compute expected loss, and buy more survey only where the value of information justifies it.

## References

- ASPRS (2015). ASPRS Positional Accuracy Standards for Digital Geospatial Data (Edition 1, Version 1.0, November 2014). *Photogrammetric Engineering & Remote Sensing*, 81(3):A1–A26.
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2* (Version 1.0.0, 2023; Version 2, 2024). American Society for Photogrammetry and Remote Sensing.
- Baltsavias, E. P. (1999). Airborne laser scanning: Basic relations and formulas. *ISPRS Journal of Photogrammetry and Remote Sensing*, 54(2–3):199–214.
- Calder, B. R., & Mayer, L. A. (2003). Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems*, 4(6):1048.
- FGDC (1998). *Geospatial Positioning Accuracy Standards, Part 3: National Standard for Spatial Data Accuracy*. FGDC-STD-007.3-1998.
- Fisher, P. F., & Tate, N. J. (2006). Causes and consequences of error in digital elevation models. *Progress in Physical Geography*, 30(4):467–489.
- Glennie, C. (2007). Rigorous 3D error analysis of kinematic scanning LIDAR systems. *Journal of Applied Geodesy*, 1(3):147–157.
- Hare, R. (1995). Depth and position error budgets for multibeam echosounding. *International Hydrographic Review*, 72(2):37–69.
- Hare, R., Godin, A., & Mayer, L. A. (1995). *Accuracy Estimation of Canadian Swath (Multibeam) and Sweep (Multitransducer) Sounding Systems*. Canadian Hydrographic Service / Geomatics Canada technical report, Ottawa.
- Heuvelink, G. B. M. (1998). *Error Propagation in Environmental Modelling with GIS*. Taylor & Francis, London.
- Hodgson, M. E., & Bresnahan, P. (2004). Accuracy of airborne lidar-derived elevation: Empirical assessment and error budget. *Photogrammetric Engineering & Remote Sensing*, 70(3):331–339.
- Höhle, J., & Höhle, M. (2009). Accuracy assessment of digital elevation models by means of robust statistical methods. *ISPRS Journal of Photogrammetry and Remote Sensing*, 64(4):398–406.
- Holmes, K. W., Chadwick, O. A., & Kyriakidis, P. C. (2000). Error in a USGS 30-meter digital elevation model and its impact on terrain modeling. *Journal of Hydrology*, 233(1–4):154–173.
- Hugonnet, R., Brun, F., Berthier, E., Dehecq, A., Mannerfelt, E. S., Eckert, N., & Farinotti, D. (2022). Uncertainty analysis of digital elevation models by spatial inference from stable terrain. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*, 15:6456–6472.
- Hunter, G. J., & Goodchild, M. F. (1997). Modeling the uncertainty of slope and aspect estimates derived from spatial databases. *Geographical Analysis*, 29(1):35–49.
- IHO (2020). *S-67 Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts*, Edition 1.0.0. International Hydrographic Organization.
- IHO (2022). *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. International Hydrographic Organization.
- James, M. R., Robson, S., & Smith, M. W. (2017). 3-D uncertainty-based topographic change detection with structure-from-motion photogrammetry: Precision maps for ground control and directly georeferenced surveys. *Earth Surface Processes and Landforms*, 42(12):1769–1788.
- JCGM (2008). *Evaluation of Measurement Data — Guide to the Expression of Uncertainty in Measurement* (JCGM 100:2008) and *Supplement 1: Propagation of Distributions Using a Monte Carlo Method* (JCGM 101:2008). Joint Committee for Guides in Metrology.
- Latypov, D. (2002). Estimating relative lidar accuracy information from overlapping flight lines. *ISPRS Journal of Photogrammetry and Remote Sensing*, 56(4):236–245.
- Nuth, C., & Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5(1):271–290.
- Oksanen, J., & Sarjakoski, T. (2005). Error propagation of DEM-based surface derivatives. *Computers & Geosciences*, 31(8):1015–1027.
- Rizzoli, P., Martone, M., Gonzalez, C., Wecklich, C., Borla Tridon, D., Bräutigam, B., Bachmann, M., Schulze, D., Fritz, T., Huber, M., Wessel, B., Krieger, G., Zink, M., & Moreira, A. (2017). Generation and performance assessment of the global TanDEM-X digital elevation model. *ISPRS Journal of Photogrammetry and Remote Sensing*, 132:119–139.
- Rolstad, C., Haug, T., & Denby, B. (2009). Spatially integrated geodetic glacier mass balance and its uncertainty based on geostatistical analysis: Application to the western Svartisen ice cap, Norway. *Journal of Glaciology*, 55(192):666–680.
- Shortridge, A., & Messina, J. (2011). Spatial structure and landscape associations of SRTM error. *Remote Sensing of Environment*, 115(6):1576–1586.
- Temme, A. J. A. M., Heuvelink, G. B. M., Schoorl, J. M., & Claessens, L. (2009). Geostatistical simulation and error propagation in geomorphometry. In Hengl, T., & Reuter, H. I. (eds.), *Geomorphometry: Concepts, Software, Applications*, Developments in Soil Science 33:121–140. Elsevier.
- U.S. Bureau of the Budget (1947). *United States National Map Accuracy Standards*. Washington, D.C.
- U.S. Geological Survey (2024). *Lidar Base Specification 2024 rev. A*. National Geospatial Program.
- Wechsler, S. P. (2007). Uncertainties associated with digital elevation models for hydrologic applications: A review. *Hydrology and Earth System Sciences*, 11(4):1481–1500.
- Zandbergen, P. A. (2008). Positional accuracy of spatial data: Non-normal distributions and a critique of the National Standard for Spatial Data Accuracy. *Transactions in GIS*, 12(1):103–130.

# Chapter 43 — Traditional versus machine-learning methods: a cross-cutting assessment

> **Part IX — Semantics, learning, and enhancement.** A cross-cutting chapter: where learned methods genuinely help across the handbook's tasks, where physics, geometry, and geostatistics still win, and how to validate each so that the claim matches the evidence.

**In this chapter.** Machine learning (ML) now touches almost every stage of elevation work, from ground filtering to global DEM correction to satellite-derived bathymetry, and the literature reports large gains. Many of those gains are real; some are artefacts of how they were measured. You will be able to place each task on a scorecard that states what ML adds over the best classical method and at what cost; explain what "traditional" means (physics, geometry, geostatistics, robust estimation) and why its error propagation is an asset; read the validation of ML-corrected global DEMs—CoastalDEM, FABDEM, DeltaDTM, DiluviumDEM—and say what their published numbers do and do not show; design a validation that respects spatial autocorrelation (block cross-validation, area of applicability); obtain and *test* calibrated uncertainty from ensembles, quantile regression, and conformal prediction; prefer hybrid designs that keep physics in the loop; document models with model cards and track licence contamination; and decide, with a short guide, when a 20-year-old algorithm is the right answer.

## 43.1 Task-by-task scorecard

"Best classical" is the method a careful practitioner would have used in about 2010; "ML gain" is the typical in-domain improvement reported in the literature; "transfer risk" is how badly the learned method degrades when geography, sensor, or density changes. The entries are assessments, not measurements; each is justified in the referenced chapter.

| Task | Best classical method | ML gain (in-domain) | Transfer risk | Recommendation |
|---|---|---|---|---|
| Ground filtering ([Ch. 30](ch30-point-cloud-classification.md)) | PTD/SMRF/CSF with tuned parameters | Moderate (+2–5 % points of accuracy on OpenGF-type benchmarks; large on complex urban) | High across density and terrain | Learned filter with classical fallback; always DTM-level validation |
| Building extraction ([Ch. 42](ch42-object-detection-semantics.md)) | nDSM + planarity rules; RANSAC roofs | Large (IoU gains of 5–15 points) | Moderate–high across regions and roof styles | ML, with boundary metrics and local fine-tuning |
| Void filling ([Ch. 35](ch35-voids-and-overhangs.md)) | Delta-surface fill, kriging, spline | Small for small voids; visually large, geometrically unproven for large voids | High (hallucination) | Classical with uncertainty; ML only with flags |
| Global DEM error correction (§43.4) | Land-cover-stratified bias removal; vegetation-height subtraction | Large in trained strata (MAE halved in forests) | High outside training strata | ML with per-stratum, spatially independent validation |
| Satellite-derived bathymetry ([Ch. 23](ch23-satellite-derived-bathymetry.md)) | Log-ratio (Stumpf) and physics-based inversion | Moderate; strongest for turbidity/bottom-type variability | High across water types and seasons | Hybrid: physics forward model with learned corrections |
| Bathymetric outlier cleaning ([Ch. 20](ch20-sonar.md)) | CUBE, surface-based robust filters | Small–moderate; useful as a flagging prior | Moderate | Classical with ML flagging, human review |
| Super-resolution ([Ch. 45](ch45-super-resolution.md)) | Bicubic/spline/kriging | Large on PSNR; unproven on independent truth | Very high | Not for measurement products |
| Feature matching in SfM ([Ch. 22](ch22-photogrammetry-sfm.md)) | SIFT/SURF + RANSAC | Large in low-texture and wide-baseline cases (SuperPoint/LightGlue) | Low–moderate | ML matchers inside classical bundle adjustment |
| GNSS multipath mitigation ([Ch. 12](ch12-gnss.md)) | Antenna design, sidereal filtering, elevation masks | Moderate in static/known environments | High across sites and antennas | Classical, ML as site-specific add-on |
| Sound-speed estimation ([Ch. 20](ch20-sonar.md)) | Measured profiles, ray tracing, refraction solvers | Small; ML useful for gap-filling profiles from climatology | Moderate | Classical; ML for prediction between casts with inflated uncertainty |
| Change detection ([Ch. 41](ch41-change-detection.md)) | DoD with LoD, M3C2, PS/SBAS InSAR | Moderate for semantic change; small for geometric | Moderate | Classical geometry; ML for classification of change type |

The pattern is consistent. ML wins where the task is *recognition*—telling a roof from a tree, a building from a terrace, a matching corner in two images—and where large labelled datasets exist. Classical methods win where the task is *measurement* with a known physical model and where the honest output is a number with an uncertainty rather than a label with a confidence. The middle ground—correction of systematic error, gap filling, denoising—is where the largest claims and the largest validation failures both live.

## 43.2 What "traditional" means

The word is used loosely and often pejoratively; it deserves a definition. Traditional methods in elevation work fall into four families, and what unites them is that their assumptions are explicit and their errors propagate.

**Physics-based models** describe the measurement: the lidar range equation, the sonar ray path through a sound-speed profile, the radar phase as a function of baseline and height, the radiative-transfer model of light through water. Their parameters have physical meaning and physical bounds; a sound speed of 1,700 m/s in seawater is wrong before any data are seen. **Geometric algorithms** operate on shape: TIN densification, morphological filters, plane fitting, Delaunay triangulation, ICP registration. Their parameters (window size, slope tolerance, inlier threshold) are terrain assumptions a user can inspect and adjust per site. **Geostatistics**—variograms, kriging, Gaussian processes—models the spatial structure of the field and of its error and returns, with every prediction, a variance derived from that structure; it is the only family of methods in this book that *by construction* delivers a spatially varying uncertainty map, and it has done so since Matheron (1963). **Robust estimation**—M-estimators, RANSAC, least median of squares, CUBE's hypothesis tracking—accepts that data contain blunders and bounds their influence with a stated breakdown point.

The shared virtue is **error propagation**: because the model is explicit, the uncertainty of the output can be derived from the uncertainty of the inputs by the law of propagation of variances ([Chapter 5](ch05-error-and-uncertainty.md)), and the result is a total propagated uncertainty (TPU/TVU) that a hydrographic standard can audit. The shared vice is **rigidity**: when the model is wrong—the terrain is not smooth, the water is not optically simple, the roof is not planar—the method fails in ways that are predictable but not self-correcting. A random forest has no idea what a roof is; a RANSAC plane fitter has exactly one idea.

> **Definitions that bite.** "Traditional" and "machine learning" are not disjoint. Kriging is a Gaussian-process regression, which is textbook ML; a random forest on hand-crafted features is "traditional" in the deep-learning literature and "ML" in a surveying office; CUBE is a Bayesian estimator; ANUDEM is an iterative optimisation with a drainage prior. The useful distinction is not the age of the method but whether its assumptions are explicit and its uncertainty is derived rather than asserted.

## 43.3 What ML adds, and what it costs

What ML adds is a **nonlinear prior learned from data**. Where a physical or geometric model cannot be written down—what does a roof look like in a point cloud at 8 pts/m², how does the SRTM vegetation bias depend on canopy structure, texture, and latitude—a model with $10^6$–$10^9$ parameters fit to $10^7$–$10^{10}$ examples can approximate the relationship well enough to be useful. The gains are real where the training data represent the deployment, and they are large where the classical alternative was a hand-tuned rule.

The costs are four, and each is a validation problem.

**Hidden assumptions.** The learned prior is the training distribution. A model that corrected SRTM against US and Australian lidar has learned the relationship between SRTM error and NDVI, population density, and slope *in those landscapes*; it has not learned the relationship in Bangladeshi mangroves, and it cannot tell you so. The assumption is as strong as "the terrain is smooth" but invisible.

**Dataset shift.** Deployment data differ from training data in covariate distribution (new terrain, new sensor), in the conditional relationship (a different forest structure gives a different bias for the same NDVI), or in label definition. Performance degrades silently; the model produces plausible outputs with the same confidence it produced correct ones.

**Lack of calibrated uncertainty.** A softmax probability or a regression output has no built-in relationship to the frequency with which the model is right. Networks trained with cross-entropy are systematically overconfident (Guo et al. 2017); regression networks output a point estimate with no variance at all unless designed otherwise. §43.6 treats the remedies and their limits.

**Hallucination of plausible terrain.** A model trained to produce realistic-looking surfaces learns to produce realistic-looking surfaces. In void filling and super-resolution this means gullies, ridges, and buildings that are consistent with the training statistics and absent from the Earth. In DEM correction it means terraces removed because they resembled buildings and mangrove platforms lowered because the model had learned that vegetation bias is always positive. The output is wrong in a way no residual plot of the training data reveals.

The least-discussed cost is the **asymmetry of effort**: a classical method's failure modes are known when it is published; a learned method's are discovered by its users, one landscape at a time.

## 43.4 ML-corrected global DEMs

The clearest test case for the chapter's argument is the family of global DEMs produced by applying ML corrections to SRTM or Copernicus GLO-30 to remove the vegetation and building bias that makes a radar DSM a poor DTM. They are widely used in flood and sea-level studies, their validation is public, and their failure modes are instructive.

**CoastalDEM** (Kulp & Strauss 2018; version 2.1 in 2021, version 3.0 in 2024) corrected SRTM 1″ (later also NASADEM/Copernicus inputs) with an artificial neural network using inputs including SRTM elevation, vegetation indices, population density, slope, and canopy height, trained against US and Australian lidar. In its validation regions it roughly halved RMSE relative to SRTM and reduced vertical bias from metres to decimetres; the follow-up global exposure paper (Kulp & Strauss 2019) tripled estimates of population on land below projected high-tide lines. Coverage is restricted to elevations below about 20 m. The training data are from two high-income countries with particular building densities and vegetation types; the authors tested transfer with held-out regions within those countries, which is not the same as transfer to the deltas where most of the exposed population lives.

**FABDEM** (Hawker et al. 2022; "Forest And Buildings removed DEM") corrected Copernicus GLO-30 with random forests, trained against reference lidar DTMs from 12 countries with separate models for forest and built-up areas and predictors including canopy height, tree cover, building footprint density, and slope. The published validation reports mean absolute error reduced from 5.15 m to 2.88 m in forests and from 1.61 m to 1.12 m in built-up areas, with testing on held-out countries. Later independent assessments (e.g., the DEMIX intercomparison; Guth et al. 2024) found FABDEM to be the best or near-best global DTM candidate in many terrain types but also found cases where the correction *degraded* geomorphometric measures relative to the uncorrected Copernicus DSM in low-relief areas, because removing a smooth bias from a smooth surface leaves artefacts at the boundaries of the correction strata.

**DeltaDTM** (Pronk et al. 2024) targets low-lying coastal zones (below about 10 m) with a different design: Copernicus GLO-30 is corrected using spaceborne lidar (ICESat-2 ATL08 and GEDI terrain estimates) as the reference, with a filtering and local bias-correction approach rather than a global regressor, and reports a mean absolute error of about 0.45 m against independent airborne lidar. The use of globally distributed satellite lidar as training and reference reduces the geographic bias of the airborne-lidar-trained products, at the price of inheriting the ICESat-2/GEDI terrain errors under dense canopy ([Chapter 18](ch18-topographic-lidar.md)).

**DiluviumDEM** (Dusseau, Zobel & Schwalm 2023) corrects Copernicus GLO-30 up to 80 m elevation with a LightGBM gradient-boosting model trained on lidar from several countries and ICESat-2, reporting accuracy comparable to or better than FABDEM and CoastalDEM in its coastal test areas. Products of the "forest-removed DTM" type continue to appear—FathomDEM (Uhe et al. 2025) uses a vision-transformer correction of Copernicus—and the pattern of claims is similar.

What the validations show and do not show deserves care. They show that, *in the strata and regions represented by the training data*, systematic vegetation and building bias is substantially reduced—and this is a real achievement; an SRTM-based flood map in a forested floodplain is wrong by metres, and a FABDEM-based one is wrong by one or two. They do not show accuracy in regions with no training data (most of Africa, South America, and Asia for the lidar-trained products), in low-relief forests where the correction is largest and the reference sparsest, in dense informal settlements where building-height predictors fail, or in landscapes whose terrain features resemble the objects being removed—agricultural terraces, levees, dykes, and raised roads are all at risk of being "corrected" away. A spatially global RMSE averages the well-validated with the unvalidated. The products are large improvements for screening and relative comparison, and they are not substitutes for measured terrain in any single place where a decision has consequences ([Chapter 55](ch55-public-products.md) compares them with other public products).

> **Case file.** When Pronk et al. (2024) validated DeltaDTM against independent airborne lidar in low-lying coastal zones, they also scored the earlier ML-corrected products on the same checkpoints. Under tree cover—the stratum where the correction is largest and where deltaic populations concentrate—only about 42 % of FABDEM and 49 % of CoastalDEM elevations fell within 1 m of the reference (60 % for DiluviumDEM, 87 % for DeltaDTM), while on open cropland all products were within a few decimetres. The products' own papers had not claimed sub-metre accuracy under tropical canopy; users assumed it from the global summary statistics. The failure is in the reading, and the remedy is to publish and read per-stratum, per-region error with an explicit statement of where the model had no training data (§43.5).

<!-- figure: Figure 43.1 — Side-by-side profiles across a forested floodplain and an agricultural terrace: Copernicus GLO-30 DSM, FABDEM, DeltaDTM, and airborne lidar DTM; the forested section shows the correction working, the terrace section shows terraces smoothed away by the correction. -->


## 43.5 Validation for ML: spatial cross-validation and area of applicability

The validation habit imported from general ML—hold out a random subset of samples and report error on it—is wrong for spatial data, and the size of the error it makes is large enough to reverse conclusions.

### 43.5.1 Why random cross-validation is optimistic

Elevation errors, land cover, and terrain are spatially autocorrelated: two checkpoints 30 m apart share the same canopy, the same soil, the same SRTM look geometry, and nearly the same residual. When training and test points are interleaved at random, every test point has a near-twin in the training set, and the model is rewarded for interpolating rather than for predicting. Roberts et al. (2017) showed the effect across ecological models; Ploton et al. (2020) showed that a tropical forest biomass model with a random-CV $R^2$ of 0.5–0.7 had a spatially blocked $R^2$ near zero—that is, it had learned nothing that transferred beyond the sampled plots. Meyer et al. (2019) demonstrated the same optimism in land-cover and soil mapping and traced part of it to the use of latitude, longitude, and other spatial-proxy predictors that let the model memorise location.

### 43.5.2 Block, buffered, and target-oriented cross-validation

The remedy is to hold out *regions*, not points. **Spatial block CV** divides the area into blocks (squares, watersheds, administrative units, or clusters of training locations) larger than the autocorrelation range of the residuals and leaves out whole blocks in turn (Roberts et al. 2017; Valavi et al. 2019 for the `blockCV` package). **Buffered leave-one-out** excludes all training points within a radius of each test point. **Leave-location-out** and **leave-time-out** CV hold out entire sites or entire epochs, matching the intended use: if a DEM correction will be applied to countries it was not trained on, validate by leaving countries out, as FABDEM did. The block size should be chosen from a variogram of the residuals (block edge ≥ the range), not by convenience. **Nearest-neighbour distance matching** (Milà et al. 2022) goes further: it chooses the CV design so that the distribution of distances from test points to their nearest training point matches the distribution of distances from *prediction* locations to their nearest training point, which is the quantity that actually determines how hard the prediction task is.

A counterpoint deserves airing. Wadoux et al. (2021) argued that when a *probability sample* of independent reference data exists, design-based estimation from that sample gives an unbiased map accuracy and spatial CV is unnecessary—and can be pessimistic if blocks are larger than needed. Both positions are right in their domains: use design-based inference on an independent probability sample when you have one ([Chapter 53](ch53-accuracy-assessment.md)); use spatial CV when the only reference data are the training data's clustered relatives, which is the normal situation for ML-corrected products.

### 43.5.3 Area of applicability

Cross-validation estimates error *where reference data exist*. Meyer & Pebesma (2021) proposed the **area of applicability** (AOA) to say where a model's CV error estimate can be trusted at all. The method computes, for each prediction location, a **dissimilarity index** (DI): the distance in (importance-weighted) predictor space to the nearest training sample, normalised by the mean distance among training samples. Locations whose DI exceeds the threshold observed in cross-validation—i.e., that are further from any training sample than the CV folds were from each other—are outside the AOA, and the model's error there is unknown rather than merely larger. Applied to global ML maps (Meyer & Pebesma 2022), the AOA frequently excluded large fractions of the Earth's land surface: predictions existed everywhere, but applicability did not. For an ML-corrected DEM, the AOA map is the single most useful piece of metadata a user can be given, and none of the products in §43.4 shipped one at first release.

### 43.5.4 Reporting per-stratum error

A global RMSE is a weighted average over strata with different error magnitudes and different user populations. Report error separately by slope class (0–2°, 2–10°, 10–30°, > 30°), land cover (forest by canopy density, cropland, built-up by building density, wetland, bare), latitude band or climate zone, elevation band (for coastal products: 0–2 m, 2–5 m, 5–10 m), and distance to the nearest training sample. Report $n$, bias, RMSE, MAE, NMAD, and LE95 per stratum ([Chapter 5](ch05-error-and-uncertainty.md)); where $n$ is small, say so instead of reporting a number to two decimals. The NVA/VVA split of the first-edition ASPRS positional accuracy standards (retained in the USGS Lidar Base Specification) is the minimal version of this discipline; ML products need the fuller version because their error structure follows their training strata, not the terrain.

> **Try it.** Compare random and spatial block cross-validation for a DEM bias-correction model with scikit-learn. Expected outcome: random K-fold RMSE is noticeably lower than block RMSE; the gap is your optimism estimate. Replace the synthetic data with a table of checkpoint residuals and covariates.
>
> ```python
> import numpy as np
> from sklearn.ensemble import RandomForestRegressor
> from sklearn.model_selection import KFold, GroupKFold, cross_val_score
>
> rng = np.random.default_rng(0)
> n = 4000
> x, y = rng.uniform(0, 10_000, n), rng.uniform(0, 10_000, n)       # metres
> canopy = np.clip(rng.normal(12, 6, n), 0, None)                     # m
> # spatially correlated "true" DEM error: smooth field + canopy bias + noise
> field = 3 * np.sin(x / 900) * np.cos(y / 1300)
> err = 0.6 * canopy + field + rng.normal(0, 0.8, n)
> X = np.c_[canopy, x, y]                                             # x, y as predictors: a common mistake
>
> rf = RandomForestRegressor(300, min_samples_leaf=5, n_jobs=-1, random_state=0)
> kf = KFold(5, shuffle=True, random_state=0)
> blocks = (x // 2000).astype(int) * 10 + (y // 2000).astype(int)     # 2 km blocks
> gkf = GroupKFold(5)
> for name, cv, groups in [("random", kf, None), ("block", gkf, blocks)]:
>     s = cross_val_score(rf, X, err, cv=cv, groups=groups,
>                         scoring="neg_root_mean_squared_error")
>     print(f"{name:7s} RMSE = {-s.mean():.2f} m")
> ```
>
> Then drop `x, y` from `X` and repeat: the gap shrinks because the model can no longer memorise location; the residual gap is the genuine cost of predicting into unsampled space.

## 43.6 Uncertainty from ML

A measurement without an uncertainty is not a measurement, and an ML prediction without a *calibrated* uncertainty is not a usable estimate. The methods below produce uncertainty; only the calibration tests tell you whether to believe it.

**Deep ensembles** (Lakshminarayanan et al. 2017) train $M$ networks from different initialisations (and ideally different bootstrap samples) and take the spread of their predictions as the epistemic uncertainty; they are simple, strong, and cost $M$ times the training. **Monte Carlo dropout** (Gal & Ghahramani 2016) keeps dropout active at inference and samples; it is cheap and tends to underestimate uncertainty far from training data. **Quantile regression** trains the model with the pinball loss to output chosen quantiles (e.g., 5th, 50th, 95th) directly, giving a heteroscedastic interval that captures aleatoric variation; random forests have a quantile variant. **Gaussian processes** and kriging deliver a predictive variance from the covariance structure; they are the gold standard for interpolation uncertainty at the scales their covariance models hold. **Conformal prediction** (Vovk, Gammerman & Shafer 2005; Angelopoulos & Bates 2023) wraps any point predictor: on a held-out calibration set it computes the nonconformity scores (e.g., absolute residuals, or residuals scaled by a predicted spread) and takes their $(1-\alpha)$ quantile as the interval half-width, guaranteeing marginal coverage of $1-\alpha$ on exchangeable data. The guarantee is distribution-free and finite-sample; the catch is exchangeability, which spatial data violate across regions exactly as §43.5 described. Spatially blocked calibration sets restore an honest, if looser, guarantee.

**Calibration tests.** For prediction intervals, compute the empirical coverage: the fraction of independent test residuals within the stated interval, per stratum; a 90 % interval that covers 70 % of forest residuals is miscalibrated there regardless of its global coverage. Plot a **reliability diagram** (predicted probability or nominal coverage vs observed frequency) and report the **expected calibration error**. For full predictive distributions, use **proper scoring rules**—the continuous ranked probability score (CRPS) and the logarithmic score (Gneiting & Raftery 2007)—which reward both calibration and sharpness and cannot be gamed by hedging. A model with a lower CRPS on spatially independent test data is better in the sense that matters.

**Why a confidence map is not an accuracy map.** A network's softmax or an ensemble's spread measures the model's *internal* disagreement; it says nothing about errors the whole ensemble shares, which is what dataset shift produces. All members of an ensemble trained on temperate lidar will agree, confidently, on a wrong correction in a mangrove. A confidence map answers "where is the model unsure?"; an accuracy map answers "where is the model wrong?"; the first is a lower bound on the second, and only independent reference data close the gap. Publishing a confidence layer as an "uncertainty" layer without a coverage test is the ML equivalent of reporting a surveying instrument's display precision as its accuracy.

> **Worked example.** A DEM-correction model is wrapped with split conformal prediction. On a calibration set of $n = 2{,}000$ spatially blocked checkpoints, the absolute residuals $|y_i - \hat{y}_i|$ have an empirical 90th percentile of 1.42 m (the conformal quantile uses the $\lceil (n+1)(1-\alpha) \rceil / n$ = 1,801st ordered value, 1.43 m). The model therefore reports $\hat{y} \pm 1.43$ m as a 90 % interval everywhere. On an independent test region the interval covers 91 % of open-ground residuals but 74 % of residuals under dense forest and 62 % in built-up areas with building footprint density > 30 %. Marginal coverage holds (88 % overall); conditional coverage fails exactly where the correction is largest. The remedy is a *locally weighted* or stratified conformal procedure—calibrate separate quantiles per land-cover stratum (forest: 2.6 m; built-up: 3.1 m; open: 0.9 m)—and report all three. The uncertainty map now varies by a factor of three across the landscape, which is the truth the single number hid.

## 43.7 Hybrid designs

The most durable successes in this field keep the physics or geometry in the loop and let learning do the part that cannot be written down.

**Physics-guided learning** constrains the model with known structure: a bathymetric inversion whose network predicts the parameters of a radiative-transfer forward model (bottom albedo, water-column attenuation) rather than depth directly, so that outputs obey the physics and extrapolate sensibly; a DEM correction that predicts *canopy height* and subtracts a physically bounded fraction of it, rather than predicting elevation error from arbitrary covariates. Reichstein et al. (2019) set out the general case for Earth system science.

**Learned priors in Bayesian inversion** treat the ML output as a prior with its own variance and combine it with measurements by the usual Bayesian update. In satellite-derived bathymetry, a learned depth prior from imagery with a 2 m standard deviation combined with sparse soundings of 0.3 m standard deviation yields a surface that is sounding-controlled near the data and prior-controlled away from it, with a posterior variance that says which is which ([Chapter 23](ch23-satellite-derived-bathymetry.md)). The same architecture underlies gravity-guided bathymetric prediction (Smith & Sandwell 1997) with a physical rather than learned prior, and GEBCO's type-identifier grid records the distinction cell by cell ([Chapter 45](ch45-super-resolution.md)).

**ML for QC flagging with human review** uses the classifier where it is strongest—recognising anomalies—and the human where the model is weakest—deciding what they mean. Multibeam outlier detection, DTM spike detection, and labelling review (§42.8) all fit this pattern; the design requirement is that the flagging recall on known error types be measured and the review rate budgeted.

**Classical algorithms with learned parameters** keep an interpretable algorithm and let a model choose its settings: SMRF window and slope per tile predicted from terrain roughness; kriging variogram parameters fit by a network from local structure; CUBE capture radius chosen by a learned function of density and slope. The output inherits the classical method's error propagation while losing its one-size-fits-all parameterisation.

The common thread is that the learned component is **bounded**: by physics, by a prior variance, by a human decision, or by the algorithm it parameterises. An unbounded learned component is the one that hallucinates.

<!-- figure: Figure 43.2 — Block diagram of four hybrid architectures (physics-guided network, learned prior in Bayesian inversion, ML flagging with human review, classical algorithm with learned parameters), each annotated with where uncertainty enters and how it propagates to the output. -->

## 43.8 Reproducibility, versioning, model cards, and licence contamination

A classical algorithm is reproducible from its description and parameters; a learned model is reproducible only from its weights, its training data, its preprocessing, and often its random seed and library versions. Treat each as a versioned artefact. Pin training data by content hash and release date (the Copernicus DEM has had several releases with different void handling and edits; a model trained on release 2021_1 is a different model from one trained on 2023_1). Record the preprocessing (tiling, normalisation, resampling kernel), the split design (which blocks were held out), the hyperparameters, and the evaluation code; archive weights with the product ([Chapter 50](ch50-archiving-and-provenance.md)).

**Model cards** (Mitchell et al. 2019) are the minimum documentation: intended use and out-of-scope uses; training data (sources, geography, sensors, epochs, licences); evaluation data and their independence from training; per-stratum metrics; known failure modes; and the area of applicability. For a geospatial product, add the input product versions, the AOA map as a raster, and the calibration results of the uncertainty layer. OGC's **TrainingDML-AI** standard (Part 1, 2023) provides an encoding for describing training datasets—their labels, provenance, quality, and licences—so that the "training data" field of a model card can be machine-readable.

**Licence contamination** is an unsolved legal problem with a practical surveying consequence. Many of the best reference DTMs are released under non-commercial or share-alike licences (CC BY-NC, ODbL); a model trained on them and sold commercially, or a DEM product derived from such a model, may breach the licence, and the derived product's own licence may be unenforceable or misleading. FABDEM is released under CC BY-NC-SA 4.0 in part because of its training data; downstream users who build commercial products on it inherit the restriction. The second-order problem is **training on a product that was itself ML-corrected**: a model trained with FABDEM as "truth" learns FABDEM's errors as signal and inherits its licence, and the resulting error correlation between products defeats any later attempt to validate one against the other. Keep a licence inventory for training data alongside the content hashes, and never use an ML-corrected product as reference without stating it ([Chapter 68](ch68-legal-issues.md)).

## 43.9 Decision guide: when a 20-year-old algorithm is the right answer

Use the classical method when any of the following holds:

1. **The output is a measurement with a liability attached.** Navigation depths, legal boundaries, flood-defence crest heights, engineering volumes: the method must have a derivable uncertainty and an audit trail. CUBE, kriging, and least squares qualify; a network does not, unless wrapped in a calibrated, stratified, independently tested uncertainty and accepted by the authority concerned.
2. **The physics is known and the data are sufficient.** Refraction correction, geoid modelling, InSAR phase-to-height, lidar range processing: learning would only re-derive an equation you already have, with less precision.
3. **There is no training data from the deployment domain and no way to get it.** A model outside its area of applicability is a guess; a geometric algorithm with terrain-appropriate parameters is a method.
4. **The smallest features matter.** Classical interpolation and filtering have predictable smoothing; learned methods have unpredictable hallucination. For levee crests, culverts, and narrow channels the first can be corrected for and the second cannot.
5. **You cannot afford the validation.** A learned method whose spatial CV, AOA, calibration, and per-stratum reporting you will not perform should not be deployed; the classical method's known weaknesses are cheaper to live with than the learned method's unknown ones.

Use the learned method when the task is recognition, the training data represent the deployment (checked with an AOA), the §43.5–43.6 validation has been done, and the output is a prior, a flag, or a screening product rather than the measurement of record. Use a hybrid whenever you can.

> **Rule of thumb.** If you cannot write down what the model would have to get wrong for the output to be wrong, you cannot validate it, and you should not ship it as a measurement. This applies to classical methods too; it just tends to be easier to answer for them.


## Then & now

- **Hand rules (to the 1990s).** Classification and editing by operators with explicit rules; error propagation by least squares (Gauss, Helmert) for geodetic quantities; kriging in mining and soil science from the 1960s (Matheron 1963).
- **Statistical learning (2000s).** Random forests (Breiman 2001) and SVMs on hand-crafted features entered remote sensing and lidar classification; Breiman's "two cultures" essay (2001) framed the data-modelling vs algorithmic-modelling divide this chapter still lives in.
- **Deep learning (2015–).** CNNs on imagery, then point-cloud networks (2017), then DEM correction with networks and boosted trees (CoastalDEM 2018, FABDEM 2022, DiluviumDEM 2023, DeltaDTM 2024).
- **Validation caught up late (2017–2022).** Spatial CV (Roberts et al. 2017), the exposure of random-CV optimism (Ploton et al. 2020), and the area of applicability (Meyer & Pebesma 2021, 2022) arrived after the first global ML products, which is why their first releases lacked applicability maps.
- **Foundation models and conformal guarantees (2023–).** Earth-observation foundation models promise transfer; conformal prediction promises distribution-free intervals; both guarantees are conditional on exchangeability that spatial deployment violates.
- **Meanwhile**, geostatistics, robust estimation, and least squares never stopped being correct.

## Mathematics

**Bias–variance decomposition.** For a predictor $\hat{f}$ trained on random samples and a target $y = f(\mathbf{x}) + \varepsilon$ with $\mathrm{Var}(\varepsilon) = \sigma^2$, the expected squared error at $\mathbf{x}$ is
$$\mathbb{E}\big[(y - \hat{f}(\mathbf{x}))^2\big] = \underbrace{\big(f(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})]\big)^2}_{\text{bias}^2} + \underbrace{\mathbb{E}\big[(\hat{f}(\mathbf{x}) - \mathbb{E}[\hat{f}(\mathbf{x})])^2\big]}_{\text{variance}} + \sigma^2 .$$
Flexible learners trade bias for variance; under dataset shift the bias term grows where the training density is low, which is what the AOA tries to map.

**Optimism of random CV under autocorrelation.** If residuals have a covariance $C(d)$ with range $a$, and test points lie at distance $d \ll a$ from training points, the model's effective test error is closer to the interpolation error $\sigma^2(1 - \rho(d))$ than to the extrapolation error $\sigma^2$, where $\rho(d) = C(d)/C(0)$. Block CV with block edge $\ge a$ restores $d \gtrsim a$, hence $\rho \approx 0$. The practical consequence is that the random-CV RMSE understates the deployment RMSE by a factor approaching $\sqrt{1 - \rho(d)}$ for pure interpolation.

**Dissimilarity index and AOA (Meyer & Pebesma 2021).** With predictors scaled and weighted by importance $w_k$, the distance between locations $i$ and $j$ is $d_{ij} = \sqrt{\sum_k w_k^2 (x_{ik} - x_{jk})^2}$. For a prediction location $p$, $\mathrm{DI}_p = \min_j d_{pj} / \bar{d}$, where $\bar{d}$ is the mean pairwise distance among training samples. The AOA threshold is the upper whisker (or a chosen quantile) of the DI values obtained for training samples with respect to samples *in other CV folds*; locations with $\mathrm{DI}_p$ above it are outside the AOA.

**Proper scoring rules.** For a predictive CDF $F$ and observation $y$, the continuous ranked probability score is
$$\mathrm{CRPS}(F, y) = \int_{-\infty}^{\infty} \big(F(z) - \mathbf{1}[z \ge y]\big)^2 \, dz,$$
which reduces to the absolute error for a point forecast and has the units of $y$. The logarithmic score is $-\ln f(y)$. Both are strictly proper: their expectation is minimised only by the true distribution (Gneiting & Raftery 2007).

**Split conformal intervals.** With calibration residuals $s_i = |y_i - \hat{y}_i|$, $i = 1 \ldots n$, and $\hat{q} = $ the $\lceil (n+1)(1-\alpha) \rceil$-th smallest $s_i$, the interval $\hat{y}(\mathbf{x}) \pm \hat{q}$ satisfies $P(y \in \text{interval}) \ge 1 - \alpha$ for exchangeable $(\mathbf{x}, y)$. With a scaled score $s_i = |y_i - \hat{y}_i| / \hat{\sigma}(\mathbf{x}_i)$ the interval becomes $\hat{y} \pm \hat{q}\,\hat{\sigma}(\mathbf{x})$, adapting its width to a predicted spread.

**Calibration curve.** For nominal coverage levels $\alpha_k$, plot observed coverage $\hat{c}_k = \frac{1}{n}\sum_i \mathbf{1}[y_i \in I_{\alpha_k}(\mathbf{x}_i)]$ against $1 - \alpha_k$; the expected calibration error is $\sum_k w_k |\hat{c}_k - (1-\alpha_k)|$.

## Validation & uncertainty

For any ML component in an elevation pipeline, the validation has five parts, and omitting any one is how the failures in this chapter happened.

1. **Independence of reference data.** Reference checkpoints or DTMs must come from a different source than the training data, a different epoch where change is plausible, and ideally a different sensor. Never validate an ML-corrected DEM against another ML-corrected DEM, or against the lidar it was trained on.
2. **Spatial design.** Use block, leave-location-out, or NNDM cross-validation with block size set from the residual variogram; or, where an independent probability sample exists, design-based estimation from it. Report both the random-CV and spatial-CV numbers so readers can see the optimism.
3. **Applicability.** Compute and publish the AOA (or an equivalent dissimilarity map) as a raster at product resolution. State the fraction of the product outside it.
4. **Stratified error.** Report bias, RMSE, MAE, NMAD, LE95, and $n$ by slope, land cover, elevation band, and region; flag strata with $n < 30$ as unassessed rather than averaging them in.
5. **Calibration of the uncertainty layer.** Test empirical coverage per stratum on independent data; report CRPS or log score where a predictive distribution is claimed; label the layer "model confidence" rather than "uncertainty" if it has not been tested.

How errors propagate downstream: a corrected DEM's residual error enters flood models as water-depth error one-for-one in low-relief terrain, enters slope as $\partial z$ differences amplified by $1/h$ ([Chapter 44](ch44-resolution-and-sampling.md)), and enters change detection as a false change wherever two products of different correction lineage are differenced ([Chapter 41](ch41-change-detection.md)). The last is insidious: FABDEM minus Copernicus is a map of the correction, not of change, and FABDEM minus CoastalDEM is a map of the difference between two models' training data.

> **Uncertainty budget.** Where the error in an ML-corrected global DTM comes from, for a low-relief coastal cell (indicative; derive your own per stratum from the five-part validation):
>
> | Component | Typical magnitude | How to bound it |
> |---|---|---|
> | Input DSM random error (Copernicus/SRTM) | 1–3 m (1σ) in flat open terrain; more under canopy | Published validations; local checkpoints |
> | Residual vegetation/building bias after correction | 0.5–3 m, land-cover dependent, sign can reverse | Per-stratum independent checkpoints |
> | Correction applied to real terrain features (terraces, levees) | 1–10 m local, rare but severe | Profile checks across known features |
> | Reference (training) DTM error and datum mismatch | 0.1–0.5 m; whole-product bias if the geoid differs | Datum audit ([Ch. 9](ch09-vertical-datums.md)) |
> | Outside-AOA extrapolation | Unknown; not bounded by any of the above | AOA map; treat as missing data |
>
> The last row is the one no RMSE captures and the one the AOA exists to expose.

## Software

**Open source:** scikit-learn (forests, boosting, CV framework), XGBoost and LightGBM (gradient boosting; DiluviumDEM's engine), PyTorch and TensorFlow (deep learning), TorchGeo (geospatial samplers and datasets for PyTorch; caveat: random geo-samplers reproduce the random-CV problem unless you block them), CAST (R; spatial CV, AOA, NNDM; the reference implementation of Meyer & Pebesma), blockCV (R; spatial and environmental blocking), MAPIE (Python; conformal prediction for regression and classification), quantile-forest / `quantregForest`, GSTools and PyKrige (variograms and kriging for the geostatistical baseline), xdem (DEM error analysis and uncertainty; caveat: not an ML framework but the right place to test ML outputs).

**Free but closed:** cloud AutoML platforms that fit tabular models to checkpoint residuals with no spatial awareness; convenient and dangerous for the reasons in §43.5.

**Commercial:** Esri ArcGIS deep-learning toolsets (pretrained models for point clouds and imagery; caveat: training domains rarely documented), Trimble eCognition (rule-based plus ML object analysis), proprietary DEM-correction services (several vendors sell corrected global DEMs; apply the §43.5 questions before purchase).

## Standards & guides

- **ISO/IEC 23053:2022, Framework for Artificial Intelligence (AI) Systems Using Machine Learning (ML).** Terminology and lifecycle framework; useful for procurement language.
- **OGC Training Data Markup Language for AI (TrainingDML-AI) Part 1: Conceptual Model Standard, v1.0 (2023).** Encoding of training-dataset metadata, labels, provenance, quality, and licences.
- **Mitchell et al. (2019), Model Cards for Model Reporting.** De facto standard for model documentation; adopt with geospatial extensions (AOA, input versions, calibration results).
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Ed. 2 (2023).** Applies unchanged to ML outputs: independent checkpoints, RMSE_V/RMSE_H reporting (the NVA/VVA split of Ed. 1 survives in the USGS Lidar Base Specification); nothing in the standard exempts a learned product.
- **IHO S-44 Ed. 6.1.0 (2022) and S-100 data quality.** TVU/THU requirements that an ML-derived depth must meet by demonstration, not by assertion.
- **Meyer & Pebesma (2021, 2022) and Roberts et al. (2017)** as method guides for spatial validation; not standards, but the references any reviewer will expect.

## Pitfalls

- **Random train/test splits across autocorrelated terrain** → every test point has a near-twin in training → use block/leave-location-out CV sized by the residual variogram, and report the random-vs-block gap.
- **"RMSE 1.2 m globally" hiding 8 m errors in mangroves** → global averages weight the well-sampled temperate strata → stratify by land cover, slope, and region; publish $n$ per stratum.
- **A corrected DEM that removed real terraces, levees, or raised roads as "buildings"** → the model learned that step-like features are objects → profile checks across known engineered features; keep classical fallbacks where the AOA is marginal.
- **Training on a product that was itself ML-corrected** → it looked like a good reference and was easy to get → check lineage; never use an ML product as truth; record licences.
- **An "uncertainty" layer nobody calibrated** → ensemble spread or softmax exported as-is → test empirical coverage per stratum on independent data; rename the layer if untested.
- **Latitude, longitude, or tile ID as predictors** → they let the model memorise location and inflate random-CV scores → drop them or validate with leave-location-out CV.
- **Assuming conformal coverage holds across regions** → exchangeability fails under spatial shift → calibrate on spatially blocked sets and per stratum.
- **Differencing two products of different correction lineage and calling it change** → the difference is the correction → difference only like-lineage products; see [Chapter 41](ch41-change-detection.md).
- **Buying ML because the classical method needed tuning** → tuning is visible work; dataset shift is invisible → budget the §43.5–43.6 validation; if you will not, keep the classical method.

## Key takeaways

- ML is a powerful prior learned from data, not a measurement; it wins at recognition and loses at measurement with liability.
- "Traditional" means explicit assumptions and derivable uncertainty; that property, not age, is what matters.
- ML-corrected global DEMs are large improvements *within their training strata* and unvalidated outside them; read per-stratum error and demand an area-of-applicability map.
- Random cross-validation on spatial data is optimistic; use spatial blocks, leave-location-out, or an independent probability sample.
- Uncertainty from ensembles, quantile regression, or conformal prediction is a hypothesis until its coverage is tested per stratum on independent data.
- A confidence map is a lower bound on error, not an accuracy map.
- Prefer hybrids that bound the learned component with physics, a prior variance, a human decision, or a classical algorithm.
- Version models and training data, publish model cards, and track licence contamination.
- When the output carries liability, the physics is known, or the validation cannot be afforded, the 20-year-old algorithm is the right answer.

## References

- Angelopoulos, A. N. & Bates, S. (2023). Conformal prediction: A gentle introduction. *Foundations and Trends in Machine Learning* 16(4):494–591.
- Breiman, L. (2001). Random forests. *Machine Learning* 45(1):5–32.
- Breiman, L. (2001). Statistical modeling: The two cultures. *Statistical Science* 16(3):199–231.
- Dusseau, D., Zobel, Z. & Schwalm, C. R. (2023). DiluviumDEM: Enhanced accuracy in global coastal digital elevation models. *Remote Sensing of Environment* 298:113812.
- Gal, Y. & Ghahramani, Z. (2016). Dropout as a Bayesian approximation: Representing model uncertainty in deep learning. *Proceedings of the 33rd International Conference on Machine Learning (ICML)*, PMLR 48:1050–1059.
- Gneiting, T. & Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *Journal of the American Statistical Association* 102(477):359–378.
- Guo, C., Pleiss, G., Sun, Y. & Weinberger, K. Q. (2017). On calibration of modern neural networks. *Proceedings of the 34th ICML*, PMLR 70:1321–1330.
- Guth, P. L., Trevisani, S., Grohmann, C. H., Lindsay, J., Gesch, D., Hawker, L. & Bielski, C. (2024). Ranking of 10 global one-arc-second DEMs reveals limitations in terrain morphology representation. *Remote Sensing* 16(17):3273.
- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C. & Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters* 17(2):024016.
- Kulp, S. A. & Strauss, B. H. (2018). CoastalDEM: A global coastal digital elevation model improved from SRTM using a neural network. *Remote Sensing of Environment* 206:231–239.
- Kulp, S. A. & Strauss, B. H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications* 10:4844.
- Lakshminarayanan, B., Pritzel, A. & Blundell, C. (2017). Simple and scalable predictive uncertainty estimation using deep ensembles. *Advances in Neural Information Processing Systems* 30.
- Matheron, G. (1963). Principles of geostatistics. *Economic Geology* 58(8):1246–1266.
- Meyer, H., Reudenbach, C., Wöllauer, S. & Nauss, T. (2019). Importance of spatial predictor variable selection in machine learning applications – Moving from data reproduction to spatial prediction. *Ecological Modelling* 411:108815.
- Meyer, H. & Pebesma, E. (2021). Predicting into unknown space? Estimating the area of applicability of spatial prediction models. *Methods in Ecology and Evolution* 12(9):1620–1633.
- Meyer, H. & Pebesma, E. (2022). Machine learning-based global maps of ecological variables and the challenge of assessing them. *Nature Communications* 13:2208.
- Milà, C., Mateu, J., Pebesma, E. & Meyer, H. (2022). Nearest neighbour distance matching leave-one-out cross-validation for map validation. *Methods in Ecology and Evolution* 13(6):1304–1316.
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D. & Gebru, T. (2019). Model cards for model reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAT\*)*, 220–229.
- Ploton, P., Mortier, F., Réjou-Méchain, M., Barbier, N., Picard, N., Rossi, V., Dormann, C., Cornu, G., Viennois, G., Bayol, N., Lyapustin, A., Gourlet-Fleury, S. & Pélissier, R. (2020). Spatial validation reveals poor predictive performance of large-scale ecological mapping models. *Nature Communications* 11:4540.
- Pronk, M., Hooijer, A., Eilander, D., Haag, A., de Jong, T., Vousdoukas, M., Vernimmen, R., Ledoux, H. & Eleveld, M. (2024). DeltaDTM: A global coastal digital terrain model. *Scientific Data* 11:273.
- Reichstein, M., Camps-Valls, G., Stevens, B., Jung, M., Denzler, J., Carvalhais, N. & Prabhat (2019). Deep learning and process understanding for data-driven Earth system science. *Nature* 566:195–204.
- Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F. & Dormann, C. F. (2017). Cross-validation strategies for data of temporal, spatial, hierarchical, or phylogenetic structure. *Ecography* 40(8):913–929.
- Smith, W. H. F. & Sandwell, D. T. (1997). Global sea floor topography from satellite altimetry and ship depth soundings. *Science* 277(5334):1956–1962.
- Uhe, P., Lucas, C., Hawker, L., Brine, M., Wilkinson, H., Cooper, A., Saoulis, A. A., Savage, J., Sampson, C. & Neal, J. (2025). FathomDEM: an improved global terrain map using a hybrid vision transformer model. *Environmental Research Letters* 20(3):034002.
- Valavi, R., Elith, J., Lahoz-Monfort, J. J. & Guillera-Arroita, G. (2019). blockCV: An R package for generating spatially or environmentally separated folds for k-fold cross-validation of species distribution models. *Methods in Ecology and Evolution* 10(2):225–232.
- Vovk, V., Gammerman, A. & Shafer, G. (2005). *Algorithmic Learning in a Random World*. Springer, New York.
- Wadoux, A. M. J.-C., Heuvelink, G. B. M., de Bruin, S. & Brus, D. J. (2021). Spatial cross-validation is not the right way to evaluate map accuracy. *Ecological Modelling* 457:109692.

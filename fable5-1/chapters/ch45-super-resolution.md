# Chapter 45 — Super-resolution and DEM enhancement

> **Part IX — Semantics, learning, and enhancement.** The closing chapter of the semantics part: methods that produce finer, cleaner, or more complete elevation surfaces than their inputs, what they actually add (assumptions, not measurements), and the epistemics of trusting them.

**In this chapter.** Every DEM user has wanted a finer, smoother, or gap-free surface than the data provide, and there is now a method for each wish. You will be able to classify enhancement methods—interpolation upsampling, single-image super-resolution, multi-source fusion, multi-epoch stacking, physics-driven shape-from-shading—by what information each draws on; remove stripes, speckle, terraces, and pits with feature-preserving filters and know what each filter costs; treat void filling as a special case with its own hallucination risk; distinguish terrain *synthesis* for graphics from terrain *estimation* for science; apply the same reasoning to bathymetry, where gravity-guided and learned seafloor prediction fill most of the ocean; validate an enhanced DEM against independent truth with per-feature, spectral, and hallucination tests rather than peak signal-to-noise ratio; and write the metadata and usage constraints that keep an enhanced surface out of the legal, navigational, and engineering decisions it was never fit for. The thesis in one line: sharper is not truer.

## 45.1 A taxonomy of enhancement

Enhancement methods differ in the *source of the added information*, and that source determines what can go wrong.

**Interpolation upsampling** (bilinear, bicubic, thin-plate spline, kriging) adds no information: it produces a smooth surface through or near the existing samples at a finer grid. It is honest—nothing appears that was not implied by the data—and uninformative—nothing appears that was not implied by the data. Kriging adds a variance surface that is largest between samples, which is the correct statement of what upsampling knows ([Chapter 31](ch31-interpolation-and-gridding.md)).

**Single-image super-resolution (SISR)** learns, from pairs of low- and high-resolution DEMs, a mapping that predicts the fine detail plausibly associated with a coarse pattern. Xu et al. (2015) applied non-local similarity; Chen et al. (2016) adapted SRCNN (Dong et al. 2016) to DEMs; D-SRGAN (Demiray, Sit & Demir 2021) applied an adversarial loss; later work added attention and feedback (Kubade et al. 2021), terrain-feature losses, and diffusion-style generative models. The added information is a **prior learned from the training terrain**: the model has seen what gullies look like at 1 m in the training region and draws them where the 30 m input has a valley. When the deployment terrain resembles the training terrain this works, in the sense that the output is statistically similar to real 1 m terrain; whether the drawn gully is in the right place is a separate question that PSNR does not answer.

**Multi-source fusion SR** combines the coarse DEM with an independent fine-resolution observation that is correlated with elevation: optical texture and shading (Argudo, Chica & Andújar 2018 trained a fully convolutional network on DEM + orthophoto pairs), SAR backscatter and coherence, a photogrammetric DSM with a lidar DTM, or a sparse but accurate dataset with a dense but biased one (Yue et al. 2015 posed multi-scale DEM fusion as regularised SR). The added information is real—a 0.5 m orthophoto genuinely constrains where the gully is—but it is indirect, and the model must learn or be told the mapping from image to height, which fails on uniform texture, shadows, and vegetation.

**Multi-epoch stacking** exploits sub-pixel offsets between repeated acquisitions: if the same terrain is sampled $N$ times with different grid phases, the aliased high frequencies can be partially unfolded (classical multi-frame SR), and independent noise averages down as $1/\sqrt{N}$. TanDEM-X's global DEM combined multiple acquisitions per site, and the ASTER GDEM stacked tens of scenes; the gain is real for noise and modest for resolution, and it requires accurate co-registration of the stack ([Chapter 41](ch41-change-detection.md)) and a stationary surface.

**Physics-driven enhancement** uses an imaging model to extract height from an independent physical signal at the image's resolution: **shape-from-shading** and **photoclinometry** recover surface slope from the brightness of a scene under known illumination and reflectance, integrate it to height, and use the coarse DEM to fix the long wavelengths that shading cannot constrain. This is the standard method for planetary surfaces where stereo is sparse (Kirk et al. 2003; [Chapter 67](ch67-planetary-dems.md)) and works on Earth where albedo is uniform and vegetation absent—deserts, ice, bare rock. Its errors are physical (albedo variation misread as slope, atmospheric scattering) rather than statistical, which makes them diagnosable.

| Method | Information added | Fails when | Typical honest use |
|---|---|---|---|
| Interpolation upsampling | None | Never (it never claims anything) | Grid matching, display |
| Single-image SR | Learned terrain prior | Terrain unlike training; small features; built structures | Visualisation; priors for matching |
| Multi-source fusion | Correlated fine observation | Texture–height mapping breaks (shadow, canopy, water) | Mosaics with flagged cells |
| Multi-epoch stacking | Sub-pixel sampling diversity, noise averaging | Surface changes; misregistration | Noise reduction; modest SR |
| Shape-from-shading | Radiometric slope signal | Albedo variation; atmosphere; vegetation | Planetary, desert, ice surfaces |

<!-- figure: Figure 45.1 — The same 30 m DEM tile enhanced to 5 m by bicubic interpolation, single-image SR, DEM + orthophoto fusion, and shape-from-shading, each shown as a hillshade beside the 5 m lidar truth and a difference map; the SR panel shows a sharp but displaced gully network. -->

## 45.2 Noise reduction and artefact removal

Denoising is enhancement that claims to remove what is not terrain. Each artefact has a characteristic signature; each removal method has a characteristic cost.

**Stripes.** SRTM carries along-track and across-track striping from residual phase and baseline errors; ASTER GDEM carries stacking artefacts; airborne lidar DEMs show strip-wise steps where adjacent flight lines were mis-calibrated by a few centimetres; photogrammetric DSMs show seam lines at image boundaries. Stripe removal works in the frequency domain (notch filtering of the stripe wavenumber, directional filtering) or by modelling the stripe as a slowly varying additive field estimated along the stripe direction and subtracted. Gallant & Read (2009, 2016) removed SRTM stripes by this route in producing the Australian DEM-S and a near-global bare-earth product; Yamazaki et al. (2017) removed stripe noise, speckle, absolute bias, and tree-height bias in sequence to produce MERIT DEM from SRTM and AW3D30. The cost: a real linear feature aligned with the stripe direction (a levee, a road cut) is attenuated with the stripe. The test: difference the before and after and look for anything that is not a stripe.

**Speckle and isolated outliers.** Radar and photogrammetric DEMs carry spiky pixel-scale noise; lidar DTMs carry pits (low noise) and spikes (high noise or residual vegetation). Median filters remove isolated outliers while preserving edges better than mean filters; the **adaptive median** applies a median only where a pixel departs from its neighbourhood by more than a threshold, which spares legitimate small features. Pit-and-peak filters (e.g., a local-minimum test against the median of a ring) are the DEM equivalent of the point-cloud noise filters of [Chapter 30](ch30-point-cloud-classification.md). The cost: a median of width $w$ removes any feature narrower than $w/2$—including the culvert inlet and the boulder.

**Terraces (stair-steps) from contour-derived DEMs.** DEMs interpolated from digitised contours (most national 1:25k–1:50k-era products, and many hydrographic grids from chart contours) show flat treads along the contour lines and steep risers between them, with a histogram spiked at the contour values. Removal methods fit a smooth surface constrained to pass between (not through) the contours, or apply a drainage-aware smoother such as ANUDEM's (Hutchinson 1989) iterative finite-difference solution with a roughness penalty and stream enforcement; the GRASS `r.surf.contour` and ArcGIS Topo to Raster implement variants. The cost: the terraces encode the true vertical uncertainty of the source (±half the contour interval), and a smooth output hides it. The honest product keeps the contour interval in the metadata and the uncertainty at ±CI/2.

**Feature-preserving smoothing.** Gaussian and mean filters blur edges; **bilateral filtering** weights neighbours by both spatial distance and elevation difference, so smoothing stops at breaks of slope; **anisotropic diffusion** (Perona & Malik 1990) diffuses along but not across gradients; **normal-vector smoothing** (Sun et al. 2007, adopted for DEMs in Lindsay, Francioni & Cockburn 2019 and implemented as WhiteboxTools `FeaturePreservingSmoothing`) smooths the surface normals and then re-integrates heights, preserving ridges and channels while removing speckle. These are the methods of choice for lidar DTMs before slope and curvature analysis. The cost: parameters (range σ, number of iterations) that, set too strongly, turn rolling terrain into facets; and a tendency to sharpen soft edges into hard ones, which is the sharper-not-truer problem in miniature.

**Learned denoisers.** Networks trained on noisy/clean DEM pairs (often with synthetic noise added to lidar) outperform classical filters on the noise they were trained on and can remove real terrain that resembles the noise model. A denoiser trained on Gaussian noise applied to SRTM removes the speckle and also every karst doline of pixel scale.

> **Try it.** Remove striping from a DEM tile with a directional frequency-domain filter and check what else was removed. Expected outcome: the stripe wavenumber disappears from the spectrum; the before–after difference should contain only stripes—if it contains ridges or roads, the filter is too wide.
>
> ```bash
> # 1. Inspect the spectrum (GMT 6): look for a peak at the stripe wavelength and azimuth
> gmt grdfft dem.tif -Er+n -Gspectrum.txt      # radial power spectrum (text)
> gmt grdfft dem.tif -Er+wk -Gspec2d.nc        # 2-D power grid in wavenumber space
>
> # 2. Remove the stripe band: low-pass in the across-stripe direction with grdfilter
> #    (stripe wavelength ~ 400 m across-track, azimuth 15°; here approximate with an
> #    anisotropic Gaussian: wide along the stripes, narrow across)
> gmt grdfilter dem.tif -Fg600/150 -D0 -Gdem_destriped.nc    # 600 m x 150 m Gaussian, rotate as needed
>
> # 3. What was removed?
> gmt grdmath dem.tif dem_destriped.nc SUB = removed.nc
> gmt grdimage removed.nc -Cpolar -JX15c -Baf -png removed
> ```
>
> Inspect `removed.png`: a clean result shows stripes only. For lidar flight-line steps use `pdal`'s per-flight-line statistics instead and fix the calibration ([Chapter 18](ch18-topographic-lidar.md)); filtering the DEM treats a symptom of a boresight error.

## 45.3 Void filling and inpainting as enhancement

Void filling is the enhancement everyone performs and few validate. [Chapter 35](ch35-voids-and-overhangs.md) covers the classical methods—interpolation (spline, kriging, IDW), delta-surface fill from an auxiliary DEM, and the SRTM-era combination of fill sources; here the question is what changes when the filler is generative.

A classical fill is bounded by its inputs: a spline through the void rim produces a smooth surface whose maximum deviation from the rim is predictable; a delta-surface fill from a coarser DEM reproduces that DEM's terrain within the void, offset to match the rim, and inherits that DEM's known accuracy. A **generative inpainter**—a network trained to complete masked DEMs, including diffusion models—produces terrain inside the void that is *statistically consistent* with the surroundings: if the rim shows a valley entering and leaving, the fill contains a channel; if the surroundings are dissected, the fill is dissected. The result looks right, and its error relative to the true terrain is unbounded by anything in the input. Published comparisons report lower RMSE for learned inpainting than for spline fills on held-out voids *in the training region*; they rarely report the maximum error, the error on voids larger than those in training, or the error where a real feature (a dam, a quarry, a cliff) lies inside the void.

The practical rules follow. For voids smaller than a few cells, any method is fine and the fill is interpolation. For voids of tens of cells, a classical fill with an auxiliary DEM where available, and a per-cell uncertainty that grows with distance from the rim. For large voids, classical fill with uncertainty, *or* a generative fill labelled as synthetic with no uncertainty claim at all—never a generative fill labelled as a measurement. In every case the void mask must survive into the product as a flag layer: the user who models a flood through a filled void needs to know it was filled, and the next producer who composites the product needs to know not to use the filled cells as a source.


## 45.4 Terrain synthesis versus terrain estimation

The computer-graphics community has built excellent tools for producing terrain that looks real. Guérin et al. (2017) trained conditional generative adversarial networks to synthesise terrain from sketches and from coarse inputs, with an "amplification" mode that adds plausible detail to a low-resolution heightfield; Argudo et al. (2018) and a line of subsequent work (including diffusion-based terrain generators) produce landscapes with realistic drainage, ridges, and erosion textures at interactive rates. These are achievements, and they are not estimation.

The distinction is the objective. **Synthesis** optimises for plausibility: the output should be indistinguishable from real terrain by a human or a discriminator network, and any of many outputs is acceptable. **Estimation** optimises for fidelity: the output should be as close as possible to the one true terrain, and the acceptable outputs are those within a stated tolerance of it. Adversarial and perceptual losses, by design, push toward the first; they sharpen edges and add texture that minimises the discriminator's ability to tell fake from real, and in doing so they move the output *away* from the conditional mean that minimises RMSE. Blau & Michaeli (2018) proved the general perception–distortion trade-off: beyond a point, improving perceptual quality necessarily worsens distortion. A super-resolved DEM optimised to look like lidar is therefore, provably, a worse estimate of the lidar than a blurrier one would be.

Geoscience needs estimation. A hydrologist wants the valley where the valley is; a geomorphologist wants the real gully density, not a plausible one; an engineer wants a height with an uncertainty. Synthesis has legitimate uses adjacent to these—generating training data for classifiers, filling background terrain in a visualisation beyond the survey boundary, stress-testing a flood model with plausible terrains—and each is a use in which the output is *not mistaken for a measurement*. The failure mode is the transfer of a synthesis tool to an estimation task because its outputs look better: "plausible" and "true" are different properties, and the eye cannot tell them apart.

> **Definitions that bite.** "Super-resolution" in the imaging literature means recovering frequencies above the sampling limit of the input—genuinely new information from priors or from multiple frames. In much of the DEM-SR literature it means producing a finer grid with sharper features from one input, scored by PSNR against a reference downsampled from the same source. The second is closer to "learned interpolation with texture synthesis", and its scores say how well the model reproduces the downsampling operator, not how well it recovers terrain. When reading an SR paper, find how the low-resolution inputs were made: if by downsampling the truth, the task is easier than any real one.

## 45.5 Bathymetric enhancement

Most of the ocean floor has never been measured directly; the global grids that depict it are enhancements, and the hydrographic community has been unusually disciplined about saying so.

**Gravity-guided prediction.** Smith & Sandwell (1997) combined satellite-altimetry-derived marine gravity with sparse ship soundings: in the band of wavelengths (~15–160 km) where seafloor topography and gravity are coherent, gravity predicts topography through a transfer function calibrated against the soundings; outside that band the soundings alone (long wavelengths) or nothing (short wavelengths) constrain the surface. The method produced the first global seafloor map with consistent ~10–20 km resolution and remains the basis of SRTM15+ (Tozer et al. 2019) and of the GEBCO grid in unsurveyed areas. Its honesty is structural: the predicted depth has a known spectral band, a known transfer-function uncertainty, and a published **type identifier (TID)** grid in GEBCO that labels each cell as measured (by sounding type) or predicted. The TID grid is the model for every enhanced product in this chapter.

**Machine-learned seafloor prediction.** Networks and boosted trees trained on measured bathymetry with predictors including gravity, vertical gravity gradient, sediment thickness, age, and distance to ridges and coasts can reduce prediction error relative to the linear transfer-function approach, particularly where the gravity–topography relationship varies (thick sediments, flexural compensation). The validation issues of [Chapter 43](ch43-traditional-vs-ml.md) apply in full: measured bathymetry is clustered along ship tracks, random cross-validation is optimistic, and the area of applicability is a function of distance from track. Several such products exist; treat each as the GEBCO TID discipline would—predicted cells labelled predicted.

**SDB fused with sparse soundings.** In shallow water, satellite-derived bathymetry gives dense but biased and smooth depths, and soundings give sparse but accurate ones. Fusion by regression (soundings calibrate the SDB model), by Bayesian update (SDB as prior, soundings as data, posterior variance per cell), or by kriging of the SDB residuals at the soundings produces a surface that is sounding-controlled near tracks and SDB-controlled away from them. The posterior variance is the enhancement's honest output; the fused depth without it is a chart that looks surveyed and is not ([Chapter 23](ch23-satellite-derived-bathymetry.md)).

**Chart generalisation as the inverse problem.** A nautical chart deliberately *coarsens* the seafloor: soundings are selected shoal-biased, contours are smoothed seaward, and features are exaggerated for safety. Enhancing a chart-derived grid—removing terraces, interpolating between selected soundings—is the inverse of generalisation, and it is ill-posed in the dangerous direction: the generalisation removed the deep values and kept the shoal ones, so a smooth surface through chart soundings is biased shoal in a way that is safe for navigation and wrong for volume, habitat, and hydrodynamic modelling, and it can be biased *deep* between shoal soundings where a real shoal was omitted at that chart scale. Chart-derived bathymetry should carry the chart scale as its effective resolution and the chart's safety bias as a known, one-sided error ([Chapter 62](ch62-navigation-and-charting.md)).

> **Case file.** The GEBCO_2014 to GEBCO_2024 grids added the TID layer and reported the fraction of the ocean floor constrained by direct measurement, which rose from about 6 % at the project's 2017 launch to roughly a quarter (26.1 % at the GEBCO_2024 release) of the seafloor at the 400 m grid resolution. The reported number matters less than the practice: a global product that states, cell by cell, what is measured and what is predicted, and whose users can mask either. No global land DEM enhanced by ML yet does this at the cell level, and the land community should adopt it.

## 45.6 Validation: sharper is not truer

Validation of an enhanced DEM has one rule above all: the reference must be **independent and finer** than the output. A reference downsampled from the same source as the input shares its errors; a reference at the output resolution cannot reveal hallucinated detail below it. Airborne lidar DTMs validate 5–10 m SR products; UAV or terrestrial scanning validates 1 m products. With that reference in hand, test the following.

**Fidelity statistics by stratum.** RMSE, MAE, NMAD, LE95, and bias of the enhanced DEM against the reference, stratified by slope, land cover, and relief class, and *compared with the same statistics for the plain interpolation baseline*. An SR method that does not beat bicubic interpolation on independent truth by a margin larger than the reference uncertainty has added texture and nothing else. Report the maximum error and the 99th percentile; hallucination lives in the tails.

**Per-feature metrics.** Extract features that matter—channel networks (by flow accumulation), ridgelines, slope breaks, building edges—from the enhanced DEM and from the reference, and measure *position error* (mean and 95th-percentile distance between matched features), *completeness* (fraction of reference features found), and *correctness* (fraction of enhanced features that exist in the reference). Edge sharpness in the enhanced DEM is not a metric; the position error of the edge is. A gully drawn 8 m from the real gully with a crisp edge is worse than a blurred gully in the right place.

**Spectral checks.** Compute the power spectrum of the enhanced DEM, of the reference, and of the interpolation baseline (Try it in [Chapter 44](ch44-resolution-and-sampling.md)). An honest enhancement moves the spectrum toward the reference across the band it claims to recover; over-sharpening shows as power *exceeding* the reference at short wavelengths (a spectral slope flatter than the terrain's), which is texture synthesis. The ratio of enhanced to reference power as a function of wavelength is a direct, scalar-per-band statement of what was recovered and what was invented.

**Hallucination detection.** Difference the enhanced DEM and the reference; threshold at a multiple of the reference uncertainty; extract connected regions of exceedance; and classify them: features present in the enhanced DEM and absent in the reference (invented), present in the reference and absent in the enhanced DEM (missed), and displaced. Report counts per square kilometre by feature type. The method is the change-detection procedure of [Chapter 41](ch41-change-detection.md) applied between an estimate and the truth rather than between epochs.

**Domain independence.** Test on terrain types and regions outside the training set—different lithology, relief, land use, and latitude—and report results per domain. A model trained on alpine lidar and tested on alpine lidar tells you about alpine lidar. The training–testing-on-the-same-terrain problem is identical to the spatial-leakage problem of [Chapter 43](ch43-traditional-vs-ml.md), and the remedy is the same: leave whole regions and whole terrain types out.

**Uncertainty inflation.** Where enhanced cells are mixed with measured cells, the enhanced cells' uncertainty must be at least the validated RMSE of the enhancement in that stratum, and the product's reported accuracy must be computed over all cells, not only the measured ones. A mosaic that reports lidar accuracy while 40 % of its cells are SR-filled misstates its quality by construction.

> **Worked example.** A 30 m DEM over 100 km² of dissected farmland is super-resolved to 5 m. Validation against an independent 1 m lidar DTM (aggregated to 5 m; σ ≈ 0.15 m) gives, on 10 km² of held-out terrain of the same type: bicubic baseline RMSE 2.41 m, SR RMSE 2.08 m, 99th-percentile |error| 7.9 m (baseline 6.2 m). Channel networks extracted above a 1 ha accumulation threshold: 184 km in the reference, 171 km matched within 10 m in the SR product (completeness 0.93), 212 km total in the SR product (correctness 0.81), mean position error 6.4 m. Spectral ratio SR/reference: 0.95 at 100 m wavelength, 1.02 at 40 m, 1.38 at 15 m, 1.9 at 10 m. Reading: the SR product improved RMSE by 14 % and worsened the tails; it found most real channels and invented one kilometre of channel for every five real ones; and at wavelengths below ~20 m it contains more power than the Earth, i.e., synthesised texture. Fit for visualisation and as a matching prior; not fit for a drainage design, and its metadata must say so. On the independent domain (a karst plateau, 5 km²), SR RMSE 3.6 m vs baseline 2.9 m—worse than interpolation—and the area of applicability excludes it.

<!-- figure: Figure 45.2 — Validation dashboard for an SR DEM: stratified error table, channel-network overlay (reference, matched, invented, missed), spectral ratio curve crossing 1.0 near 40 m wavelength and rising to 1.9 at 10 m, and a map of hallucinated features per km². -->

## 45.7 Communicating enhancement

An enhanced DEM is dangerous in proportion to how little its users know about it. The communication requirements are therefore not optional.

**Mandatory metadata.** The enhancement method (name, version, reference); the training data (sources, regions, resolutions, epochs, licences) for learned methods; the input product and its resolution and accuracy; the output cell size *and* the estimated effective resolution after enhancement (which is not the output cell size); the validation (reference, independence, strata, statistics, spectral ratio, hallucination counts); the area of applicability for learned methods; and the intended and prohibited uses. ISO 19115 lineage (`LI_Lineage` with `LI_ProcessStep` and `LI_Source`) carries all of this if the producer writes it ([Chapter 49](ch49-metadata.md)).

**Layer flags.** A per-cell raster distinguishing *measured*, *interpolated*, *enhanced* (with method code), and *filled void*, modelled on GEBCO's TID; the flag survives compositing only if every downstream tool is told to carry it, so the product's documentation should instruct exactly that. A BAG-style per-cell uncertainty layer with the enhancement's validated stratum RMSE in the enhanced cells is the second layer ([Chapter 47](ch47-file-formats.md)).

**Naming.** Never name or catalogue an enhanced product by its output cell size alone. "5 m SR DEM from 30 m Copernicus" is honest; "5 m DEM" is not. STAC and catalogue entries should carry both resolutions and the enhancement flag as searchable properties ([Chapter 51](ch51-finding-data.md)).

**Downstream constraints.** State them explicitly: not for navigation or charting; not for legal boundaries, floodplain designation, or regulatory flood mapping; not for engineering design or volumetrics; not as a source for further enhancement or as training or reference data; not for change detection against measured DEMs. The reason is not that enhanced DEMs are always wrong; it is that in each of these uses a hallucinated or displaced feature has consequences, the product's uncertainty cannot be bounded per feature, and the user cannot tell measured from invented by looking.

## 45.8 When enhancement is appropriate

Enhancement is a legitimate tool when its output is used as what it is. **Visualisation**: a super-resolved or smoothed DEM makes a better hillshade, and if the map says "enhanced for display" no one is misled ([Chapter 57](ch57-visualizing-dems.md)). **Priors for matching and registration**: a sharper DEM improves the initialisation of stereo matching, SAR geocoding, terrain-aided navigation, and co-registration, where the subsequent measurement step corrects the prior's errors ([Chapter 14](ch14-positioning-beyond-gnss.md), [Chapter 22](ch22-photogrammetry-sfm.md)). **Hypothesis generation**: an enhanced DEM that suggests a lineament, a palaeochannel, or an archaeological earthwork is a reason to look, not a finding. **Consistent-resolution mosaics**: where a product must have one cell size and sources differ, enhancing the coarse sources to the fine grid with flagged cells and inflated uncertainty is better than degrading the fine sources—provided the flags and the uncertainty are real and carried ([Chapter 48](ch48-compositing.md)). **Denoising before derivatives**: feature-preserving smoothing of a lidar DTM before slope and curvature analysis removes measurement noise that would otherwise dominate the second derivative, and is appropriate when its parameters are reported and its effect on the features of interest has been checked.

In each case the test is the same: would a user who understood exactly what was done still make the same decision with the enhanced product as with the raw one plus an honest statement of its limits? If yes, enhance and label. If the enhancement changes the decision because it looks more certain than the data are, do not.

> **Rule of thumb.** Treat every enhanced cell as having uncertainty no smaller than the input product's, and as having *unknown* uncertainty for features smaller than the input's effective resolution. The rule is conservative for noise reduction (which genuinely lowers uncertainty when validated) and exactly right for super-resolution and generative fills.


## Then & now

- **Contour-to-grid smoothing (1980s).** Hutchinson's ANUDEM (1989) turned digitised contours and spot heights into drainage-consistent grids with an iterative finite-difference solver and a roughness penalty; it was the first widely used "enhancement" that added a prior (connected drainage) to sparse data, and it still underlies ArcGIS Topo to Raster.
- **Signal-processing SR (1990s–2000s).** Multi-frame reconstruction from sub-pixel-shifted images, non-local means, and sparse-coding SR entered image processing; the first DEM applications (Xu et al. 2015) adapted non-local similarity to terrain.
- **Deep SR (2015–).** SRCNN (Dong et al. 2016) and its successors moved to DEMs within a year (Chen et al. 2016); GAN-based D-SRGAN (2021) and attention/feedback networks followed, with PSNR gains and the perception–distortion trade-off arriving together.
- **Diffusion and generative models (2022–).** Terrain synthesis and inpainting with diffusion models produce the most realistic outputs yet, and the widest gap between plausibility and fidelity.
- **Bathymetry: hand contouring → gravity-predicted depth (1997) → ML prediction.** Smith & Sandwell's 1997 global map replaced hand-contoured charts of the deep ocean; SRTM15+ and GEBCO institutionalised the measured/predicted distinction with the TID grid; ML predictors now compete with the transfer-function method and must adopt the same labelling discipline.

## Mathematics

**SR as an ill-posed inverse problem.** Model the observed coarse DEM $\mathbf{y}$ (vector of $m$ cells) as a degraded version of the fine terrain $\mathbf{x}$ ($n$ cells, $n > m$):
$$\mathbf{y} = \mathbf{D}\mathbf{H}\mathbf{x} + \mathbf{n},$$
where $\mathbf{H}$ is the sensor/aggregation blur (footprint and smoothing), $\mathbf{D}$ the decimation to the coarse grid, and $\mathbf{n}$ noise. Because $\mathbf{DH}$ has a null space of dimension at least $n - m$, infinitely many $\mathbf{x}$ reproduce $\mathbf{y}$ exactly; the estimate is chosen by a prior through regularised least squares,
$$\hat{\mathbf{x}} = \arg\min_{\mathbf{x}} \|\mathbf{y} - \mathbf{D}\mathbf{H}\mathbf{x}\|^2 + \lambda\,R(\mathbf{x}),$$
with $R$ a smoothness penalty (Tikhonov $\|\nabla\mathbf{x}\|^2$, total variation $\|\nabla\mathbf{x}\|_1$, a slope-based Markov random field as in Yue et al. 2015), or implicitly by a learned mapping $\hat{\mathbf{x}} = f_\theta(\mathbf{y})$ whose "prior" is the training distribution. Everything the output contains in the null space of $\mathbf{DH}$ comes from $R$ or $\theta$, not from $\mathbf{y}$.

**Fidelity versus perceptual losses.** Training $f_\theta$ with an $\ell_2$ loss $\mathbb{E}\|\mathbf{x} - f_\theta(\mathbf{y})\|^2$ yields the conditional mean $\mathbb{E}[\mathbf{x} \mid \mathbf{y}]$, which is blurred because it averages over all terrains consistent with $\mathbf{y}$. Adding a perceptual or adversarial term $\mathcal{L} = \ell_2 + \gamma\,\mathcal{L}_{\text{adv}}$ selects a sharp sample from the conditional distribution instead of its mean; by the perception–distortion trade-off (Blau & Michaeli 2018), for any fixed distortion measure $\Delta$ and divergence $d$ between output and real distributions, the attainable $(\Delta, d)$ pairs are bounded by a convex, decreasing frontier—lower $d$ (more realistic) implies higher $\Delta$ (less accurate) once on the frontier.

**Uncertainty inflation when mixing measured and predicted cells.** If a product combines measured cells with variance $\sigma_m^2$ and enhanced cells with validated stratum error variance $\sigma_e^2$ (from independent truth), the product's reported variance must be computed over all cells; with a fraction $p$ of enhanced cells, the pooled mean-square error is $(1-p)\sigma_m^2 + p\,\sigma_e^2$, and the per-cell uncertainty layer should carry $\sigma_m$ or $\sigma_e$ by flag rather than the pooled value. Where an enhanced cell is a Bayesian combination of a prior (variance $\sigma_p^2$) and a measurement (variance $\sigma_d^2$), the posterior variance is $(1/\sigma_p^2 + 1/\sigma_d^2)^{-1}$—smaller than either, *only if* the prior's variance is honest.

**Spectral slope check.** With radially averaged power spectra $P_{\text{enh}}(f)$, $P_{\text{ref}}(f)$, and $P_{\text{int}}(f)$ (interpolation baseline), define the recovery ratio $\rho(f) = P_{\text{enh}}(f)/P_{\text{ref}}(f)$. Over the band the method claims to recover, $\rho \to 1$ indicates success; $\rho \ll 1$ (as for interpolation) indicates nothing recovered; $\rho > 1$ indicates over-sharpening. Fitting $P(f) \propto f^{-\beta}$ over the claimed band, $\beta_{\text{enh}} < \beta_{\text{ref}}$ is the signature of synthesised texture.

## Validation & uncertainty

Enhanced DEMs fail in three ways, and the validation must be designed to catch each: they are *wrong in the tails* (hallucinated or displaced features with errors far larger than the RMSE), *wrong by stratum* (good on training-like terrain, worse than interpolation elsewhere), and *wrong about their own uncertainty* (reported at the output resolution's apparent precision rather than at the enhancement's validated error).

**Procedure.** (1) Obtain independent reference data finer than the output over several terrain types including at least one outside the training domain. (2) Compute the interpolation baseline at the same output grid. (3) Report stratified RMSE, MAE, NMAD, LE95, maximum, and 99th percentile for enhanced and baseline, with the reference uncertainty stated. (4) Extract and match features; report completeness, correctness, and position error per feature type. (5) Compute the spectral recovery ratio per wavelength band. (6) Count hallucinated, missed, and displaced features per km². (7) Compute the area of applicability for learned methods and report the fraction of the product outside it. (8) Set the per-cell uncertainty layer from the stratum RMSE and the flag layer from the method, and recompute the product-wide accuracy over all cells.

**Propagation.** Enhanced cells entering slope and curvature contribute invented short-wavelength power that inflates both; entering flow routing they create or sever channels; entering change detection against a measured DEM they appear as change; entering a composite they lower the product's true accuracy while raising its apparent resolution. Each downstream use needs the flag layer to mask or down-weight enhanced cells, which is why the flag must be a raster, not a sentence in the abstract.

> **Uncertainty budget.** Error sources in a learned SR DEM (30 m → 5 m) relative to independent lidar, indicative of the structure rather than the values, which are product-specific:
>
> | Component | Nature | Where it dominates | How to bound |
> |---|---|---|---|
> | Input DEM error (passes through) | Random + systematic, 1–5 m | Everywhere; largest under canopy and on steep slopes | Input product validation |
> | Conditional-mean blur (what the data cannot know) | Systematic smoothing of features < input effective resolution | Dissected terrain, edges | Spectral ratio ≪ 1 in the unrecoverable band |
> | Prior/hallucination error | Features invented or displaced; heavy-tailed | Terrain unlike training; small built features | Feature matching; 99th percentile; AOA |
> | Over-sharpening | Short-wavelength power above truth | Everywhere, when adversarial losses are used | Spectral ratio > 1; β comparison |
> | Reference error in validation | 0.1–0.3 m lidar DTM; more under canopy | Caps the demonstrable improvement | State reference σ; do not claim below it |
>
> The second and third rows are in tension by the perception–distortion trade-off: reducing one increases the other. A product cannot be both sharp and safe below the input's effective resolution; it can only be labelled.

## Software

**Open source:** GRASS GIS (`r.surf.contour` for contour-to-grid, `r.fill.stats` and `r.fillnulls` for voids, `r.resamp.rst` and `r.resamp.bspline` for spline upsampling, `r.denoise` for Sun et al. normal smoothing; caveat: parameters need per-terrain tuning). WhiteboxTools (`FeaturePreservingSmoothing`, `FillMissingData`, `RemoveOffTerrainObjects`, `FillDepressions`; the reference implementation of Lindsay et al. 2019). GDAL (`gdal_fillnodata`, `gdalwarp` resampling; honest baselines). GMT (`surface` with tension for spline gridding, `grdfill` for voids, `grdfft`/`grdfilter` for spectra and destriping). xdem (DEM differencing, co-registration, and variogram-based uncertainty for validating enhanced vs reference). PyTorch SR codebases (BasicSR; several public DEM-SR repositories accompanying Demiray et al. 2021 and later papers; caveat: pretrained weights carry their training terrain). Scikit-image and OpenCV (bilateral and anisotropic-diffusion filters).

**Free but closed:** none of consequence; some agency viewers apply display-time smoothing that should not be mistaken for a product.

**Commercial:** ArcGIS Topo to Raster (ANUDEM) and Spatial Analyst filters; Global Mapper (void fill, smoothing, resampling); ENVI (image SR and pan-sharpening tools that some users apply to DEMs—do not without the §45.6 validation); various "AI upscaling" services aimed at imagery (caveat: trained on photographs, not terrain; no uncertainty; unsuitable for DEMs as measurements).

## Standards & guides

- **No formal specification for enhanced or super-resolved DEMs exists** (as of this writing). In its absence, this handbook recommends the following combination.
- **ISO 19115-1:2014 / 19115-2:2019 lineage.** `LI_ProcessStep` and `LI_Source` entries for the enhancement method, training data, and inputs; `MD_Resolution` for both output cell size and effective resolution.
- **ASPRS Positional Accuracy Standards, Ed. 2 (2023).** Accuracy reporting on independent checkpoints applies unchanged; enhanced products must be tested as products, over all cells.
- **GEBCO Type Identifier (TID) grid conventions** (GEBCO Compilation Group, current release documentation). The model for a per-cell measured/predicted flag layer; adopt an equivalent coding for land products.
- **OGC BAG / IHO S-102 uncertainty layers.** Per-cell uncertainty carried with the surface; the natural home for stratum-based uncertainty of enhanced cells.
- **OGC TrainingDML-AI (2023) and model cards (Mitchell et al. 2019).** Documentation of training data and model for learned enhancement ([Chapter 43](ch43-traditional-vs-ml.md)).
- **IHO S-44 Ed. 6.1.0 and national charting authorities' policies.** Exclude predicted or enhanced depths from navigational products unless carried as such with appropriate CATZOC/quality attribution ([Chapter 62](ch62-navigation-and-charting.md)).

## Pitfalls

- **Presenting SR output at 1 m with the metadata of the 30 m input** → the resampling tool wrote the new cell size and nothing else → write lineage, both resolutions, and the enhancement flag; name the product by its source.
- **Hallucinated gullies and buildings** → generative and adversarial losses reward plausible texture → feature matching against independent truth; spectral ratio; AOA; label as synthetic where no truth exists.
- **Validating with PSNR on the training domain** → the standard practice in the SR literature → independent, finer reference; held-out terrain types; stratified tails; feature metrics.
- **Using SR or predicted bathymetry in a navigation product** → the grid looks surveyed → TID-style flags; exclude predicted cells from safety surfaces; S-44 compliance by demonstration.
- **Losing the measured/predicted distinction in a mosaic** → compositing tools drop auxiliary layers by default → carry flag and uncertainty rasters through every step; test the output for their presence.
- **Smoothing away the features the analysis targets** → median and Gaussian widths chosen for appearance → set filter widths from the smallest feature of interest; diff before and after and inspect.
- **Removing terraces from contour-derived DEMs and reporting the smooth product's apparent precision** → the terraces were the uncertainty made visible → retain ±CI/2 as the vertical uncertainty.
- **Filling large voids generatively and labelling them as data** → the fill looks like terrain → classical fill with distance-dependent uncertainty, or synthetic label with no uncertainty claim; keep the void mask.
- **Training an SR model on lidar downsampled to make the inputs** → the learned task is "invert my downsampler" → train and test on real coarse products paired with independent fine truth.
- **Comparing an enhanced DEM against a measured DEM and calling the difference change** → the difference is the enhancement → never difference across enhancement lineage ([Chapter 41](ch41-change-detection.md)).
- **Denoising with a learned model trained on synthetic noise** → it removes real pixel-scale terrain resembling the noise model → validate on terrain with known small features (dolines, pits, mounds).

## Key takeaways

- Enhancement adds assumptions, not measurements; the information in the output beyond the input's effective resolution comes from a prior, and the prior can be wrong.
- Classify by information source—none, learned prior, correlated observation, sampling diversity, physics—and expect failures where that source fails.
- Denoising and artefact removal are valuable and must be checked by differencing before and after; what was removed should be only the artefact.
- Void filling is enhancement; generative fills are synthesis and must be labelled, with the void mask preserved.
- Plausible is not true: adversarial and perceptual objectives provably trade fidelity for realism.
- Validate against independent, finer truth with stratified tails, feature position metrics, spectral recovery ratios, hallucination counts, and out-of-domain tests; beat the interpolation baseline or stop.
- Bathymetry's TID discipline—every cell labelled measured or predicted—is the model for all enhanced products.
- Mandatory metadata: method, training data, input resolution and accuracy, effective output resolution, validation, applicability, permitted and prohibited uses; a per-cell flag and uncertainty layer.
- Keep enhanced surfaces out of navigational, legal, regulatory, and engineering decisions unless the uncertainty is explicitly inflated, carried per cell, and accepted by the authority concerned.

## References

- Argudo, O., Chica, A. & Andújar, C. (2018). Terrain super-resolution through aerial imagery and fully convolutional networks. *Computer Graphics Forum* 37(2):101–110.
- Blau, Y. & Michaeli, T. (2018). The perception-distortion tradeoff. *IEEE/CVF CVPR*, 6228–6237.
- Chen, Z., Wang, X., Xu, Z. & Hou, W. (2016). Convolutional neural network based DEM super resolution. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences* XLI-B3:247–250.
- Demiray, B. Z., Sit, M. & Demir, I. (2021). D-SRGAN: DEM super-resolution with generative adversarial networks. *SN Computer Science* 2:48.
- Dong, C., Loy, C. C., He, K. & Tang, X. (2016). Image super-resolution using deep convolutional networks. *IEEE Transactions on Pattern Analysis and Machine Intelligence* 38(2):295–307.
- Gallant, J. C. & Read, A. (2009). Enhancing the SRTM data for Australia. *Proceedings of Geomorphometry 2009*, Zurich, 149–154.
- Gallant, J. C. & Read, A. M. (2016). A near-global bare-Earth DEM from SRTM. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences* XLI-B4:137–141.
- GEBCO Compilation Group (2024). *GEBCO 2024 Grid* and Type Identifier (TID) grid documentation. British Oceanographic Data Centre / IHO–IOC. doi:10.5285/1c44ce99-0a0d-5f4f-e063-7086abc0ea0f
- Guérin, É., Digne, J., Galin, É., Peytavie, A., Wolf, C., Benes, B. & Martinez, B. (2017). Interactive example-based terrain authoring with conditional generative adversarial networks. *ACM Transactions on Graphics* 36(6):228.
- Hutchinson, M. F. (1989). A new procedure for gridding elevation and stream line data with automatic removal of spurious pits. *Journal of Hydrology* 106(3–4):211–232.
- Kirk, R. L., Barrett, J. M. & Soderblom, L. A. (2003). Photoclinometry made simple…? *ISPRS Working Group IV/9 Workshop "Advances in Planetary Mapping"*, Houston, March 2003.
- Kubade, A., Patel, D., Sharma, A. & Rajan, K. S. (2021). AFN: Attentional feedback network based 3D terrain super-resolution. *Computer Vision – ACCV 2020*, LNCS 12622:192–208.
- Lin, X., Zhang, Q., Wang, H., Yao, C., Chen, C., Cheng, L. & Li, Z. (2022). A DEM super-resolution reconstruction network combining internal and external learning. *Remote Sensing* 14(9):2181.
- Lindsay, J. B., Francioni, A. & Cockburn, J. M. H. (2019). LiDAR DEM smoothing and the preservation of drainage features. *Remote Sensing* 11(16):1926.
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D. & Gebru, T. (2019). Model cards for model reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency*, 220–229.
- Perona, P. & Malik, J. (1990). Scale-space and edge detection using anisotropic diffusion. *IEEE Transactions on Pattern Analysis and Machine Intelligence* 12(7):629–639.
- Smith, W. H. F. & Sandwell, D. T. (1997). Global sea floor topography from satellite altimetry and ship depth soundings. *Science* 277(5334):1956–1962.
- Sun, X., Rosin, P. L., Martin, R. R. & Langbein, F. C. (2007). Fast and effective feature-preserving mesh denoising. *IEEE Transactions on Visualization and Computer Graphics* 13(5):925–938.
- Tozer, B., Sandwell, D. T., Smith, W. H. F., Olson, C., Beale, J. R. & Wessel, P. (2019). Global bathymetry and topography at 15 arc sec: SRTM15+. *Earth and Space Science* 6(10):1847–1864.
- Xu, Z., Wang, X., Chen, Z., Xiong, D., Ding, M. & Hou, W. (2015). Nonlocal similarity based DEM super resolution. *ISPRS Journal of Photogrammetry and Remote Sensing* 110:48–54.
- Yamazaki, D., Ikeshima, D., Tawatari, R., Yamaguchi, T., O'Loughlin, F., Neal, J. C., Sampson, C. C., Kanae, S. & Bates, P. D. (2017). A high-accuracy map of global terrain elevations. *Geophysical Research Letters* 44(11):5844–5853.
- Yue, L., Shen, H., Yuan, Q. & Zhang, L. (2015). Fusion of multi-scale DEMs using a regularized super-resolution method. *International Journal of Geographical Information Science* 29(12):2095–2120.

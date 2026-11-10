# Chapter 5 — Error, uncertainty, accuracy, precision, resolution — the statistical toolkit

> **Part II — Vocabulary and the foundations of correctness.** This chapter supplies the quantitative language — error models, summary statistics, uncertainty propagation, spatial statistics, and least squares — that every later chapter uses when it says how good an elevation is.

**In this chapter.** You will be able to classify an elevation error (blunder, systematic, random, spatially correlated, artefact) and choose statistics that describe it honestly: mean error, σ, RMSE, MAE, median, NMAD, percentiles, LE90/LE95, CE90/CE95, and when the Gaussian multipliers 1.6449, 1.96, and 2.4477 are legitimate. You will distinguish error from uncertainty in the GUM sense, read "95 % uncertainty" in a BAG or S-102 file correctly, and relate TPU/TVU/THU to standard uncertainties. You will propagate uncertainty three ways — Jacobian ($\Sigma_y = J\Sigma_x J^{\mathsf T}$), Monte Carlo, and sequential Gaussian simulation for correlated fields — and compute the effective sample size that spatial correlation leaves you. You will see why reference data must be 3–10× better and independent, how quantization (int16 SRTM, Terrain-RGB) adds $q/\sqrt{12}$ of noise, and why least squares and the Kalman filter are one engine under GNSS, INS, bundle adjustment, strip adjustment, and SLAM. A worked example, a runnable Python box, and an accuracy-statement template close the chapter.

## 5.1 Error types

An **error** is the difference between a measured or modeled value and the true value: $e = \hat z - z$. The true value is never known, so in practice we observe $e$ only against a reference of higher accuracy, and the "error" we report is a difference containing both datasets' errors (§5.6). It is still useful to classify errors by *behavior*, because each class calls for a different remedy and a different statistic.

**Blunders (outliers)** are gross errors from a failed process rather than from the noise of a working one: a misidentified checkpoint, a multipath-corrupted GNSS fix, a lidar return from a bird, a sonar bubble sweep, a photogrammetric mismatch on water, a mis-typed benchmark elevation, a transposed sign. Their distribution is not Gaussian and not even unimodal; it is whatever the failure mode produces. Blunders must be *detected and removed* (or their influence bounded by robust statistics), not averaged in. A single 50 m blunder among 100 checkpoints with 0.1 m true RMSE raises the computed RMSE to 5 m; the mean error is shifted by 0.5 m.

**Systematic errors** affect many observations in a consistent, structured way. The three canonical forms are a **bias** (constant offset: a wrong antenna height, a datum mismatch, a range bias), a **drift** (a slowly varying offset in time or space: INS error growth between GNSS updates, a tide-model error over a survey day, thermal change in a laser), and a **scale** error (proportional to the quantity: sound speed scales depth; focal length scales photogrammetric heights; a wrong foot definition scales coordinates by 2 ppm). Systematic errors do not shrink with more observations; averaging a million biased points gives a precise estimate of the wrong number. They are reduced by calibration, modeling, and independent checks, and they are the dominant risk in volumes, change detection, and datum work.

**Random errors** are the residual scatter after blunders are removed and systematics are modeled — the sum of many small, independent influences, which the central limit theorem pushes toward a Gaussian. Random error *does* average down, by $1/\sqrt{n}$ when observations are independent. The "when independent" is the catch.

**Spatially correlated error** is unpredictable from first principles but structured: neighboring errors are similar. Geoid model errors are correlated over tens to hundreds of kilometers; a lidar strip's residual roll error along the strip; a photogrammetric block's "bowl" or "dome" over the whole block; InSAR atmospheric phase screens over kilometers; interpolation error over the interpolation neighborhood. Spatial correlation is what makes DEM uncertainty hard: the error in a volume computed over 10 000 cells is *not* the per-cell σ divided by 100 (§5.4–5.5).

**Artefacts** are errors with recognizable geometric signatures produced by processing: striping along flight lines or satellite tracks, terracing from integer quantization or contour-to-grid interpolation, pits and spikes from classification, "ghosting" and double surfaces from unsynchronized strips, phase-unwrapping jumps in InSAR, pixel-locking in dense matching, ringing from resampling, seams between tiles. They are systematic at small scales, usually visually obvious in a hillshade or a slope map, and often invisible in checkpoint statistics because checkpoints are sparse and placed on flat open ground where artefacts are mild ([Chapter 56](ch56-case-files.md), [Chapter 57](ch57-visualizing-dems.md)).

<!-- figure: Figure 5.1 — Five small DEM difference maps (same scene) illustrating a blunder, a constant bias, a tilt/drift, pure random noise, and spatially correlated error, each with its histogram beneath; and a sixth panel showing flight-line striping as an artefact. -->

## 5.2 Describing error

Given $n$ error values $e_i = \hat z_i - z_i$ (DEM minus reference, so positive means the DEM is too high), the standard descriptors are:

| Statistic | Formula | Measures | Robust to outliers? |
|---|---|---|---|
| Mean error (bias) | $\bar e = \frac{1}{n}\sum e_i$ | Trueness; systematic offset | No |
| Standard deviation | $\sigma = \sqrt{\frac{1}{n-1}\sum (e_i - \bar e)^2}$ | Precision; scatter about the mean | No |
| RMSE | $\text{RMSE} = \sqrt{\frac{1}{n}\sum e_i^2}$ | Combined bias and scatter | No |
| MAE | $\frac{1}{n}\sum \lvert e_i \rvert$ | Typical absolute error | Partially |
| Median | $\tilde e$ | Robust bias | Yes |
| MAD | $\operatorname{median}\lvert e_i - \tilde e\rvert$ | Robust scatter (unscaled) | Yes |
| NMAD | $1.4826 \cdot \text{MAD}$ | Robust σ-equivalent | Yes |
| Percentiles | $Q_{0.68}, Q_{0.90}, Q_{0.95}$ of $\lvert e_i \rvert$ | Empirical LE68/LE90/LE95 | Yes |

The three non-robust quantities are related exactly (for the population; approximately for samples with $n-1$) by

$$\text{RMSE}^2 = \bar e^{\,2} + \sigma^2,$$

which is why RMSE alone is ambiguous: an RMSE of 0.20 m could be a bias of 0.20 m with no scatter or a scatter of 0.20 m with no bias, and the remedies are opposite. Report both $\bar e$ and $\sigma$ (or both median and NMAD) alongside RMSE.

The factor 1.4826 in NMAD is $1/\Phi^{-1}(0.75)$, chosen so that NMAD equals σ when the errors are Gaussian; for heavy-tailed DEM errors, NMAD estimates the scatter of the *core* of the distribution and ignores the tails. Höhle and Höhle (2009) showed with airborne lidar and photogrammetric DEMs that DEM error distributions are typically non-Gaussian — leptokurtic, often skewed in vegetation — and that median, NMAD, and empirical percentiles should be reported in preference to or alongside mean, σ, and 1.96·RMSE. ASPRS Edition 1 (2014) adopted this split: non-vegetated vertical accuracy (NVA) as $1.96 \cdot \text{RMSE}_z$, vegetated vertical accuracy (VVA) as the empirical 95th percentile of absolute error, because the Gaussian multiplier is not trusted there. Edition 2 (2023) simplified to RMSE-only reporting for both and made VVA report-only rather than pass/fail; the percentile remains the honest statistic for vegetated error and this book continues to recommend it.

### 5.2.1 Linear, circular, and spherical error

**LE$p$** (linear error at probability $p$) is the half-width of the interval containing a fraction $p$ of vertical errors. If errors are Gaussian with zero bias and standard deviation σ,

$$\text{LE68} = 1.0000\,\sigma, \qquad \text{LE90} = 1.6449\,\sigma, \qquad \text{LE95} = 1.9600\,\sigma, \qquad \text{LE99} = 2.5758\,\sigma .$$

The NSSDA (FGDC 1998) uses $\text{LE95} = 1.9600 \cdot \text{RMSE}_z$, which silently assumes **both** zero bias (so that RMSE = σ) and normality. If there is a bias $b$, neither multiplier gives exactly 95 %: for $b = \sigma$ the fraction of errors within ±1.96·RMSE (= ±2.77σ about zero) is about 0.96, and the fraction within ±1.96σ about zero is only about 0.83. The ASPRS standard handles this by requiring that the bias be small relative to RMSE (and investigated if not); the honest approach is to report the bias separately and the 95 % percentile empirically.

**CE$p$** (circular error) describes horizontal error. For a bivariate Gaussian with equal, uncorrelated components $\sigma_x = \sigma_y = \sigma$, the radial error follows a Rayleigh distribution and

$$\text{CE50} = 1.1774\,\sigma, \qquad \text{CE90} = 2.1460\,\sigma, \qquad \text{CE95} = 2.4477\,\sigma .$$

The NSSDA writes $\text{CE95} = 2.4477 \cdot \text{RMSE}_r/\sqrt 2$ where $\text{RMSE}_r = \sqrt{\text{RMSE}_x^2 + \text{RMSE}_y^2}$, equivalently $\text{CE95} = 1.7308\,\text{RMSE}_r$, valid when $\sigma_x \approx \sigma_y$ (within a ratio of about 0.6–1.0; outside that range the standard gives an interpolation formula). **SE$p$** (spherical error) extends this to 3D: $\text{SE90} \approx 2.50\,\sigma$ and $\text{SE95} \approx 2.80\,\sigma$ for equal components — rarely used for DEMs, where vertical and horizontal errors differ in both magnitude and mechanism, but it appears in military mapping specifications.

**3D accuracy** for point clouds is now specified by ASPRS Edition 2 as $\text{RMSE}_{3D} = \sqrt{\text{RMSE}_x^2 + \text{RMSE}_y^2 + \text{RMSE}_z^2}$, acknowledging that horizontal accuracy of a lidar point cloud cannot be tested the way an orthoimage can.

### 5.2.2 When the multipliers are valid

The Gaussian multipliers are valid when the error distribution is (i) approximately Gaussian, (ii) unbiased, and (iii) the sample is large enough that σ is well estimated (§5.6). All three fail routinely for DEMs:

- **Vegetation and urban areas** produce skewed, heavy-tailed errors because ground-filtering failures are one-sided (the DEM sits *above* ground). Use percentiles.
- **Steep terrain** mixes horizontal error into vertical error through the slope, $\sigma_z^2 = \sigma_{z,0}^2 + \sigma_{xy}^2 \tan^2\beta$ (Chapter 3), so the error distribution across a sample of mixed slopes is a *mixture* of Gaussians with different widths — leptokurtic even if each component is Gaussian.
- **Composite products** (merged sources) have piecewise-different error distributions; a single σ describes none of the pieces.
- **Small samples**: the NSSDA minimum of 20 checkpoints gives a 95 % confidence interval on σ of roughly $[0.76\sigma,\ 1.46\sigma]$ (§5.6); the 1.96 multiplier is then precision theater.

Test normality before using the multipliers: a Q–Q plot is more informative than a p-value; the Shapiro–Wilk or Anderson–Darling tests reject normality for almost any large real DEM sample, which is itself the message. A practical check is to compare $1.96\cdot\sigma$ with the empirical 95th percentile of $|e|$: if they differ by more than ~20 %, report the empirical value.

> **Worked example.** Fifty checkpoints on open ground give DEM-minus-GNSS differences with $\bar e = +0.062$ m, $\sigma = 0.118$ m. Then $\text{RMSE} = \sqrt{0.062^2 + 0.118^2} = \sqrt{0.003844 + 0.013924} = \sqrt{0.017768} = 0.1333$ m. The NSSDA-style statement is $\text{LE95} = 1.96 \times 0.1333 = 0.261$ m. But the bias is half the scatter; if we removed it (by applying a −0.062 m correction after confirming it in an independent subset), the product would have $\text{RMSE} = \sigma = 0.118$ m and $\text{LE95} = 0.231$ m. The empirical 95th percentile of $|e|$ for this sample is 0.247 m — between the two, as expected for a modestly biased, roughly Gaussian sample. Now add one blunder of +3.0 m (a checkpoint under a culvert): $\bar e$ becomes $+0.120$ m, σ becomes 0.428 m, RMSE 0.440 m, and $1.96\cdot\text{RMSE} = 0.863$ m; the median moves from +0.058 to +0.060 m and the NMAD from 0.112 to 0.114 m. The robust statistics barely notice; the classical ones quadruple.

## 5.3 Uncertainty versus error: the GUM

The GUM (JCGM 100:2008) makes a distinction that elevation practice often blurs. An **error** is a specific, unknowable quantity attached to a specific measurement. An **uncertainty** is a parameter describing the dispersion of values that could reasonably be attributed to the measurand, given everything we know — a property of our *knowledge*, expressed as a probability distribution. We cannot report the error of a DEM cell; we can report its uncertainty.

The GUM classifies uncertainty evaluation by *method*, not by nature:

- **Type A** evaluation uses statistics of repeated observations: the standard deviation of the mean of $n$ repeat GNSS occupations, the scatter of overlapping lidar strips, the NMAD of checkpoints. It yields a standard uncertainty $u = s/\sqrt n$ for a mean, or $s$ for a single future observation.
- **Type B** evaluation uses other knowledge: manufacturer specifications, calibration certificates, published model accuracies (a geoid model's stated 2 cm σ), physical limits (a rectangular distribution of half-width $a$ has $u = a/\sqrt 3$; a triangular one $a/\sqrt 6$), expert judgment. Type B is not inferior; it is how one accounts for systematic effects that repetition cannot reveal.

The **combined standard uncertainty** $u_c$ is obtained by propagation (§5.4). The **expanded uncertainty** $U = k\,u_c$ uses a **coverage factor** $k$; $k = 2$ gives approximately 95 % coverage for a Gaussian, $k=1.96$ exactly. The GUM Supplement 1 (JCGM 101:2008) describes Monte Carlo propagation for cases where linearization or normality fails.

Two semantic traps. First, **confidence versus tolerance**: a 95 % *confidence interval* on the mean bias narrows with $\sqrt n$ and says where the *bias* is; a 95 % *tolerance* or *coverage* interval says where *individual errors* lie and does not narrow with $n$. Accuracy standards want the latter; many reports compute the former and call it accuracy. Second, **uncertainty ≠ accuracy class**: a product may have an expanded uncertainty of 0.3 m and still meet a 0.5 m specification, or carry a 0.1 m uncertainty estimate that is simply wrong because a systematic effect was omitted. Validation ([Chapter 53](ch53-accuracy-assessment.md)) exists to test whether the uncertainty estimate is itself credible.

### 5.3.1 TPU, TVU, THU, and "95 % uncertainty" in BAG and S-102

Hydrography adopted the GUM framework early (Hare 1995) under the name **total propagated uncertainty (TPU)**: the 1σ uncertainty of each sounding's depth and position, propagated from the uncertainties of every input — GNSS position, heading, roll, pitch, heave, latency, lever arms, sound-speed profile, tide, draft, and the sonar's own range and angle resolution — through the geometry of the sounding ([Chapter 20](ch20-sonar.md)). The expanded, 95 %-coverage versions are the **total vertical uncertainty (TVU)** and **total horizontal uncertainty (THU)** against which S-44 Orders are specified; S-44 (6.1.0) uses $k = 1.96$ for vertical and $k = 2.45$ for horizontal, consistent with the linear and circular Gaussian factors above.

The Open Navigation Surface **BAG** format and the IHO **S-102** bathymetric surface product carry an `uncertainty` layer alongside `elevation` (BAG) or `depth` (S-102). BAG defines several uncertainty-type codes — commonly "Raw std dev," "CUBE std dev," "Product uncertainty" (the TPU-derived value at 95 %), and "Historical std dev" — so a reader must consult the metadata to know whether a value is 1σ or 95 %. In CUBE (Calder and Mayer 2003; Calder 2006) the node uncertainty is the posterior standard deviation of the depth hypothesis, scaled to 95 % on output when "Product uncertainty" is selected. **S-102** Edition 2.x/3.0 specifies the uncertainty attribute as the vertical uncertainty at the 95 % confidence level, positive, in meters. The practical rule: never assume a bathymetric uncertainty layer is 1σ or 95 % without reading the metadata — a factor of 1.96 is the difference between passing and failing an Order.

> **Definitions that bite.** "95 %" appears in three roles in this book: a *coverage* probability on an individual error (LE95, TVU), a *confidence* level on an estimated parameter (the 95 % CI on RMSE), and a *proportion* of a sample (the empirical 95th percentile used for VVA). All three are legitimate; a report must say which it means. A checkpoint sample whose 95th percentile of $|e|$ is 0.25 m does not imply that 95 % of *all* DEM cells err by less than 0.25 m — that would require the checkpoints to be a representative sample of the cells, which open-ground checkpoints never are.

## 5.4 Propagation of uncertainty

Almost no elevation is measured directly. A lidar height is a function of GNSS position, INS attitude, lever arms, boresight angles, scan angle, and range; a sounding is a function of position, attitude, heave, sound speed, tide, and draft; a photogrammetric height is a function of orientation parameters and image measurements; a volume is a function of thousands of DEM cells. **Propagation** is how input uncertainties become output uncertainties, and three methods cover practice.

### 5.4.1 First-order (Jacobian) propagation

If $\mathbf y = f(\mathbf x)$ with input covariance $\Sigma_x$, linearizing about the working point gives

$$\Sigma_y = J\,\Sigma_x\,J^{\mathsf T}, \qquad J_{ij} = \frac{\partial f_i}{\partial x_j}.$$

For a scalar output and uncorrelated inputs this is the familiar $\sigma_y^2 = \sum_j (\partial f/\partial x_j)^2 \sigma_{x_j}^2$; the full matrix form keeps the input correlations (off-diagonal $\Sigma_x$) and produces output correlations, which are what downstream users need. The method is exact for linear $f$ and good for mildly nonlinear $f$ when input uncertainties are small relative to the curvature scale. It underlies TPU engines, the covariance output of every least-squares adjustment (§5.9), and the ASPRS/USGS lidar error-budget spreadsheets.

> **Worked example.** A lidar point at range $R = 1200$ m, scan angle $\theta = 15°$ off nadir, with range uncertainty $\sigma_R = 0.02$ m, combined attitude (roll + boresight) uncertainty $\sigma_\theta = 0.005° = 8.73\times10^{-5}$ rad, and GNSS/INS vertical position uncertainty $\sigma_{z_0} = 0.05$ m. Ignoring terrain slope, the height is $z = z_0 - R\cos\theta$, so $\partial z/\partial R = -\cos\theta = -0.966$, $\partial z/\partial\theta = R\sin\theta = 310.6$ m/rad, $\partial z/\partial z_0 = 1$. Then
> $$\sigma_z^2 = (0.966 \times 0.02)^2 + (310.6 \times 8.73\times10^{-5})^2 + 0.05^2 = 0.000373 + 0.000735 + 0.0025 = 0.003608 \ \text{m}^2,$$
> so $\sigma_z = 0.060$ m. The horizontal position uncertainty from the same attitude error is $R\cos\theta\,\sigma_\theta = 1159 \times 8.73\times10^{-5} = 0.101$ m, which on a 20 % slope adds $0.101 \times 0.2 = 0.020$ m to the vertical, giving $\sigma_z = \sqrt{0.003608 + 0.0004} = 0.063$ m. The GNSS/INS term dominates; halving range noise would change nothing visible, while halving the attitude uncertainty would help on slopes.

### 5.4.2 Monte Carlo

When $f$ is strongly nonlinear, when inputs are non-Gaussian, or when $f$ is an algorithm rather than a formula (a ground filter, a hydrologic flow routing, a flood-depth model), draw $M$ samples of the inputs from their joint distribution, run $f$ on each, and summarize the outputs. JCGM 101:2008 is the formal guide. The cost is $M$ evaluations ($M$ of 100–10 000 is common); the payoff is distribution shape, not just variance, and correct treatment of hard nonlinearities such as thresholds. Monte Carlo on a DEM requires simulating *error fields*, which brings us to spatial structure.

### 5.4.3 Sequential Gaussian simulation for correlated error fields

A DEM error field is not white noise. Simulating one realistically requires a model of its spatial covariance — a **variogram** (§5.5) — and a generator that honors it. **Sequential Gaussian simulation (SGS)** visits cells in random order, krigs each from already-simulated neighbors and any conditioning data (e.g., known checkpoint errors), draws from the conditional Gaussian, and proceeds; the result is one equiprobable realization of the error field. Repeating $M$ times and adding each realization to the DEM produces $M$ plausible DEMs; running the application (slope, watershed, volume, viewshed, flood extent) on each yields an empirical distribution of the result. Heuvelink (1998) established this as the standard for GIS error propagation; Wechsler (2007) reviewed its application to DEM hydrology and found that flow accumulation and wetness index are far more sensitive to *correlated* error than to uncorrelated error of the same σ. Unconditional simulation via FFT or spectral methods is faster for large grids with stationary covariance (gstools and scikit-gstat implement both).

### 5.4.4 Effective sample size

Spatial correlation reduces the information in $n$ samples to that of $n_{\text{eff}} < n$ independent ones. For the mean of $n$ equally weighted values with correlation matrix $\mathbf R$,

$$n_{\text{eff}} = \frac{n^2}{\mathbf 1^{\mathsf T}\mathbf R\,\mathbf 1} = \frac{n}{1 + \frac{1}{n}\sum_{i\neq j}\rho_{ij}}.$$

Two useful special cases. For a one-dimensional AR(1) sequence with lag-one correlation $\rho$ (a profile, a time series), $n_{\text{eff}} \approx n\,(1-\rho)/(1+\rho)$: at $\rho = 0.9$, 1000 samples are worth 53. For a two-dimensional area $A$ with a spherical variogram of range $L$ (correlation area $A_c = \pi L^2$), Rolstad et al. (2009) derived for $A \gg A_c$

$$\sigma_{\bar e}^2 \approx \sigma^2\,\frac{A_c}{5A},$$

i.e., $n_{\text{eff}} \approx 5A/A_c$. Hugonnet et al. (2022) generalized this to multi-range variograms (short-range noise plus long-range systematic components), showing with ASTER, ArcticDEM, and Pléiades DEMs that neglecting the long-range component underestimates the uncertainty of mean elevation change over glacier-sized areas by factors of 10 to 100. The xdem library implements the full procedure (variogram estimation on stable terrain, multi-range fitting, $n_{\text{eff}}$ by area).

> **Worked example.** A DEM has per-cell σ = 0.30 m and a spherical correlation range $L = 200$ m, so $A_c = \pi(200)^2 = 125\,664$ m². A volume is computed over a 1 km² quarry ($A = 10^6$ m², 10 m cells, $n = 10\,000$). Treating cells as independent: $\sigma_{\bar e} = 0.30/\sqrt{10\,000} = 0.003$ m, volume uncertainty $0.003 \times 10^6 = 3\,000$ m³. With correlation: $n_{\text{eff}} = 5 \times 10^6 / 125\,664 = 39.8$, $\sigma_{\bar e} = 0.30/\sqrt{39.8} = 0.048$ m, volume uncertainty $48\,000$ m³ — sixteen times larger. If an additional long-range component (a 0.10 m tilt/bowl with 2 km range) is present, it barely averages at all over 1 km² and adds $\approx 0.10 \times 10^6 = 100\,000$ m³ in quadrature: total $\approx \sqrt{48^2 + 100^2}\times 10^3 \approx 111\,000$ m³, 37× the naive figure. This is the arithmetic behind the TOC's "100× too small."

## 5.5 Spatial structure of DEM error

The **semivariogram** $\gamma(h) = \tfrac12\,\mathrm{E}\big[(e(\mathbf s) - e(\mathbf s + \mathbf h))^2\big]$ describes how dissimilar errors become with separation $h$. Its three parameters — **nugget** (variance at zero lag: measurement noise plus sub-cell variability), **sill** (total variance), and **range** or **correlation length** (separation beyond which errors are uncorrelated) — are estimated from DEM differences over **stable terrain** (bedrock, roads, non-glaciated ground unchanged between DEM and reference) using scikit-gstat, gstools, R's gstat, or xdem. Real DEMs usually need two or three nested structures: a short-range one (tens to a few hundred meters: sensor noise, interpolation, matching) and one or more long-range ones (kilometers to tens of kilometers: orbit/attitude errors, atmospheric phase, geoid, strip-adjustment residuals).

<!-- figure: Figure 5.2 — Empirical semivariogram of DEM error on stable terrain with a fitted two-range (short + long) spherical model, annotated with nugget, partial sills, and ranges; inset shows the error map used. -->

Consequences by application:

- **Volumes and mean change** over an area: uncertainty is governed by $n_{\text{eff}}$, i.e., by how the area compares with the correlation areas (§5.4.4). Short-range noise averages out; long-range error does not.
- **Slopes and curvature**: these are differences of neighboring cells, so *positively correlated* error partially cancels. For slope from cells a distance $d$ apart, $\sigma_{\Delta z}^2 = 2\sigma^2(1 - \rho(d))$; with $\rho(d) = 0.9$ at one cell lag, the slope noise is $\sqrt{0.2}\,\sigma \approx 0.45\sigma$ rather than $\sqrt 2\,\sigma$. Conversely, *uncorrelated* noise (e.g., quantization) is amplified by differencing; a 1 m int16 DEM at 30 m spacing has slope noise of $\sqrt{2}\times 0.29/30 \approx 1.4 \%$ — which is why SRTM slopes below ~2 % are mostly noise ([Chapter 44](ch44-resolution-and-sampling.md)).
- **Change detection**: the error of a DEM-of-difference includes both DEMs' errors plus co-registration error; the per-cell **limit of detection** is $\text{LoD} = t\sqrt{\sigma_1^2 + \sigma_2^2}$ with $t = 1.96$ for 95 %, and for areal sums the spatially correlated component sets the floor ([Chapter 41](ch41-change-detection.md)).
- **Kriging variance**: when a DEM is produced by kriging, the kriging variance $\sigma_K^2(\mathbf s_0)$ gives a per-cell uncertainty that depends on the data configuration (distance to neighbors) and the variogram, but not on the data values — it is a measure of sampling geometry, not of local roughness, and it is an honest uncertainty only if the variogram is right ([Chapter 31](ch31-interpolation-and-gridding.md)).

## 5.6 Reference data are uncertain too

Every reported "error" is a difference between two uncertain quantities: $d_i = \hat z_i - z_i^{\text{ref}}$, with $\sigma_d^2 = \sigma_{\text{DEM}}^2 + \sigma_{\text{ref}}^2$ if independent. The reference contributes negligibly only when $\sigma_{\text{ref}} \ll \sigma_{\text{DEM}}$; the usual rule — the **hierarchy of accuracy** — is that reference data should be at least 3× better (ASPRS Edition 1 required checkpoints 3× better than the target RMSE; Edition 2 relaxed the fixed ratio but requires the checkpoint uncertainty to be included in the product's accuracy; metrology practice prefers 4× to 10×). At 3×, the reference inflates the observed RMSE by $\sqrt{1 + 1/9} = 1.054$, about 5 %; at 1×, by 41 %, and the DEM is being blamed for the reference's errors.

**Independence** is the second requirement. Checkpoints must not have been used as control in the adjustment, must not have been used to shift or "calibrate" the product, and ideally come from a different instrument, crew, and epoch than the production survey ([Chapter 52](ch52-ground-truth.md)). Points that were control are, by construction, fit by the model; residuals at them measure fit, not accuracy, and are optimistic by an amount that depends on the model's degrees of freedom.

**Sample size** determines how well the statistics are known. For Gaussian errors the sample standard deviation $s$ from $n$ values has a $(1-\alpha)$ confidence interval

$$\sqrt{\frac{(n-1)}{\chi^2_{\alpha/2,\,n-1}}}\; s \;\le\; \sigma \;\le\; \sqrt{\frac{(n-1)}{\chi^2_{1-\alpha/2,\,n-1}}}\; s,$$

which for $n = 20$ gives $[0.76\,s,\ 1.46\,s]$ and for $n = 100$ gives $[0.88\,s,\ 1.16\,s]$ at 95 %. An RMSE of 0.100 m from 20 points means "somewhere between 0.08 and 0.15 m"; an accuracy class boundary cannot be resolved by such a sample. The same interval applies approximately to RMSE when bias is small. For percentiles the picture is worse: the 95th percentile from 20 points is essentially the maximum, and its sampling variability is enormous. ASPRS Edition 2 requires a minimum of 30 checkpoints per land-cover type and scales the count with project area; the NSSDA's 20 was a floor set in 1998 for a different era.

**Stratification** addresses the fact that DEM error depends on land cover, slope, and sensor geometry. Report statistics per stratum (open ground, forest, urban, steep), and resist aggregating strata whose distributions differ — a pooled RMSE of open and vegetated checkpoints is a weighted mixture that describes neither. Checkpoint *placement* is itself a design problem: points placed only on flat, open, paved surfaces (because that is where GNSS works best) measure the DEM at its best and are not a random sample of the product ([Chapter 26](ch26-survey-planning.md), [Chapter 53](ch53-accuracy-assessment.md)).

## 5.7 Relative versus absolute accuracy; internal versus external checks

**Absolute accuracy** is agreement with the reference frame — with truth as realized by external control. **Relative accuracy** is agreement of the dataset with itself: strip-to-strip in lidar, crossline-to-mainline in hydrography, tile-to-tile in a mosaic, point-to-point over short distances. A dataset can have excellent relative and poor absolute accuracy (one bad base-station coordinate shifts everything together), or the reverse is nearly impossible (poor relative accuracy usually implies poor absolute accuracy except by cancellation).

**Internal checks** use the data's own redundancy: overlap differences, crossline residuals, loop closures, bundle-adjustment σ₀ and residuals. They are cheap, dense, and available wherever data overlap, and they catch boresight, timing, lever-arm, and drift errors well. They cannot catch anything common to all passes: datum errors, geoid model errors, a constant range bias, a sound-speed bias affecting every line equally. **External checks** against independent reference data catch those, at the cost of sparsity. Both are required; neither substitutes for the other. Relative-accuracy statistics (e.g., USGS LBS intraswath and interswath RMSD) should be reported alongside absolute ones; a report offering only one is incomplete ([Chapter 18](ch18-topographic-lidar.md), [Chapter 20](ch20-sonar.md)).

## 5.8 Resolution, precision, and quantization

The numeric **precision** of a stored elevation is a floor on its uncertainty, not a statement of its accuracy. Storing an elevation as an integer meter (SRTM, ASTER GDEM, DTED, the original USGS DEM format) **quantizes** it with step $q = 1$ m; if the true values are spread uniformly within each bin, the quantization error has a uniform distribution on $[-q/2, q/2]$ with

$$\sigma_q = \frac{q}{\sqrt{12}} = 0.289\,q .$$

For $q = 1$ m this is 0.29 m of added, spatially *uncorrelated* noise — negligible against SRTM's several-meter absolute error, but decisive for slope (§5.5) and for the "terracing" visible in flat terrain. Float32 has 24 bits of significand, so at elevations around 1000 m the step is $2^{-14} \approx 6\times10^{-5}$ m; at 8000 m it is still 0.5 mm. Float32 is adequate for any DEM; float64 buys nothing except for geopotential or ECEF coordinates (where $6.4\times 10^6$ m in float32 would quantize at 0.5 m). Scaled integers are a good compromise: LAS stores int32 coordinates with a 0.01 m or 0.001 m scale, and GeoTIFF may store int16 with a 0.1 m scale (σ_q = 0.029 m).

**Terrain-RGB** encodings (Mapbox: $z = -10\,000 + 0.1\,(256^2 R + 256 G + B)$; Mapzen Terrarium: $z = 256 R + G + B/256 - 32\,768$) pack elevation into image channels with 0.1 m or 1/256 m steps, so their quantization noise (0.029 m or 0.0011 m) is fine — but they are commonly produced from lower-precision sources and served through lossy or resampled tile pyramids, so apparent precision far exceeds source accuracy. A visualization DEM reporting millimeters from a 10 m source with 2 m RMSE is not lying about its encoding, but a user who reads precision as accuracy will be misled ([Chapter 47](ch47-file-formats.md), [Chapter 57](ch57-visualizing-dems.md)).

> **Rule of thumb.** Store with at least 10× finer steps than the smallest uncertainty you want to represent: 0.01 m steps for 0.1 m lidar, 0.1 m for 1 m photogrammetry, 1 m for 10 m global DSMs. Finer than that wastes bits; coarser adds noise you cannot remove.

## 5.9 Least squares as the unifying engine

Nearly every estimation in this book — a GNSS position from pseudoranges, a bundle adjustment, a lidar strip adjustment, a sonar patch test, a geodetic network, a datum transformation, a SLAM pose graph, a Kalman-filtered trajectory — is an instance of **weighted least squares**: find the parameters $\mathbf x$ that minimize the weighted sum of squared residuals between observations $\boldsymbol\ell$ and their model $A\mathbf x$,

$$\min_{\mathbf x}\ (\boldsymbol\ell - A\mathbf x)^{\mathsf T} P\,(\boldsymbol\ell - A\mathbf x), \qquad P = \sigma_0^2\,\Sigma_\ell^{-1},$$

whose solution is given by the **normal equations**

$$\hat{\mathbf x} = (A^{\mathsf T} P A)^{-1} A^{\mathsf T} P\,\boldsymbol\ell, \qquad \Sigma_{\hat x} = \hat\sigma_0^2\,(A^{\mathsf T} P A)^{-1}, \qquad \hat\sigma_0^2 = \frac{\hat{\mathbf v}^{\mathsf T} P \hat{\mathbf v}}{n - u},$$

with residuals $\hat{\mathbf v} = \boldsymbol\ell - A\hat{\mathbf x}$, $n$ observations, $u$ unknowns, and **redundancy** $r = n - u$. The *a posteriori* variance factor $\hat\sigma_0^2$ should be near 1 if the weights were right; a value of 4 means the observations are twice as noisy as claimed (or the model is wrong). Nonlinear models are linearized and iterated. The output covariance $\Sigma_{\hat x}$ is the Jacobian propagation of §5.4.1 applied to the estimator, and it is the honest *precision* of the solution — honest about random error, silent about unmodeled systematics (Mikhail and Ackermann 1976; Ghilani 2017).

**Redundancy numbers** $r_i$ (the diagonal of $I - A(A^{\mathsf T}PA)^{-1}A^{\mathsf T}P$, summing to $r$) tell how much each observation is controlled by the others: $r_i \approx 0$ means an observation is uncheckable (a blunder in it passes straight into the solution); $r_i \approx 1$ means it is almost fully checked. **Data snooping** (Baarda 1968) tests each standardized residual $w_i = \hat v_i / \sigma_{\hat v_i}$ against a critical value (often 3.29 for α = 0.001), rejects the largest significant one, re-adjusts, and repeats; its companion **reliability** theory gives the smallest detectable blunder in each observation (internal reliability) and its effect on the parameters if undetected (external reliability). Their logic — detect, remove, re-estimate, and report what *could not* have been detected — is the correct outlier policy for checkpoint analysis too: remove blunders for *documented physical reasons*, report how many were removed and why, and never iterate removals until the statistics look good.

The **Kalman filter** (Kalman 1960 ⟨H⟩) is recursive weighted least squares for a state that evolves in time. With state $\mathbf x_k$, transition $F$, process noise $Q$, observation $H$, and observation noise $R$:

$$\text{predict:}\quad \mathbf x_k^- = F\mathbf x_{k-1}, \quad P_k^- = F P_{k-1} F^{\mathsf T} + Q;$$
$$\text{update:}\quad K = P_k^- H^{\mathsf T}(H P_k^- H^{\mathsf T} + R)^{-1}, \quad \mathbf x_k = \mathbf x_k^- + K(\mathbf z_k - H\mathbf x_k^-), \quad P_k = (I - KH)P_k^- .$$

The update step is exactly a weighted least-squares combination of the prediction (weight $P^{-1}$) and the observation (weight $R^{-1}$); the covariance $P$ is the running $\Sigma_{\hat x}$. GNSS/INS integration ([Chapter 13](ch13-imu-ins.md)) is a Kalman filter whose state includes position, velocity, attitude, and sensor biases; forward–backward smoothing (as in an SBET) is the batch least-squares solution of the same problem. SLAM pose graphs ([Chapter 15](ch15-slam.md)), lidar strip adjustment ([Chapter 18](ch18-topographic-lidar.md)), and multibeam patch tests ([Chapter 20](ch20-sonar.md)) are least-squares problems with different parameterizations. Knowing this lets you read any of their reports: look for σ₀, redundancy, residual histograms, and rejected observations.

## 5.10 Reporting

An accuracy statement that cannot be reproduced or compared is noise. The minimum content:

> **Accuracy-statement template.**
> 1. **Product**: name, version, surface type (DSM/DTM), post spacing, vertical datum and realization/epoch, horizontal CRS, sign convention, acquisition dates.
> 2. **Reference**: source, instrument/method, stated accuracy (σ or 95 %), datum and epoch (and the transformation applied if different), acquisition dates, independence from production (explicitly: "not used as control").
> 3. **Sample**: number of checkpoints per stratum; stratification variables (land cover, slope class); placement method; map of locations.
> 4. **Preprocessing**: how DEM values were extracted at checkpoints (nearest cell, bilinear, TIN); outlier policy (criterion, number removed, reason for each).
> 5. **Statistics per stratum**: $n$, mean (bias), median, σ, NMAD, RMSE, MAE, empirical 68/90/95th percentiles of $|e|$, min/max; normality diagnostic (Q–Q plot or skew/kurtosis).
> 6. **Derived 95 % values**: with method stated (1.96·RMSE vs empirical percentile) and confidence interval on RMSE from $n$.
> 7. **Relative accuracy**: overlap/crossline statistics where available.
> 8. **Spatial structure**: variogram parameters on stable terrain, or at least a map of residuals; $n_{\text{eff}}$ for the project area.
> 9. **Uncertainty raster** (if delivered): what it represents (1σ, 95 %; which components), how produced.

Never report: a bare RMSE without $n$, stratum, reference, and date; a 95 % value without saying how it was computed; "accuracy: sub-meter"; a precision (float, Terrain-RGB, decimal places) as an accuracy; a fit to control as an accuracy; a pooled statistic across strata with different distributions. An **uncertainty raster** — per-cell σ or 95 % — is increasingly expected (BAG and S-102 require it; xdem and CUBE produce it; ASPRS Ed. 2 encourages it) and should be built from propagation and spatial modeling, not from a constant.

> **Try it.** The script below computes the full set of statistics for a checkpoint comparison, flags outliers by a documented rule (|e − median| > 3·NMAD) *without* silently removing them, and bootstraps a confidence interval on RMSE. Replace the synthetic data with a CSV of DEM-minus-reference differences.
>
> ```python
> import numpy as np
> from scipy import stats
>
> rng = np.random.default_rng(7)
> # Synthetic: 48 open-ground points, biased +0.06 m, sigma 0.12 m, plus 2 blunders
> e = np.concatenate([rng.normal(0.06, 0.12, 48), [1.9, -0.8]])
>
> def summarize(e):
>     n = e.size
>     med = np.median(e)
>     nmad = 1.4826 * np.median(np.abs(e - med))
>     out = dict(n=n, mean=e.mean(), median=med, sd=e.std(ddof=1),
>                rmse=np.sqrt(np.mean(e**2)), mae=np.mean(np.abs(e)),
>                nmad=nmad,
>                p68=np.percentile(np.abs(e), 68), p95=np.percentile(np.abs(e), 95),
>                skew=stats.skew(e), kurt=stats.kurtosis(e))
>     # 95 % CI on RMSE assuming ~Gaussian: chi-square on n dof
>     lo, hi = stats.chi2.ppf([0.975, 0.025], n)
>     out['rmse_ci95'] = (out['rmse']*np.sqrt(n/lo), out['rmse']*np.sqrt(n/hi))
>     # Bootstrap CI (distribution-free)
>     boots = [np.sqrt(np.mean(rng.choice(e, n)**2)) for _ in range(5000)]
>     out['rmse_boot95'] = tuple(np.percentile(boots, [2.5, 97.5]))
>     return out
>
> full = summarize(e)
> flag = np.abs(e - full['median']) > 3 * full['nmad']
> clean = summarize(e[~flag])
> for k in ('n','mean','median','sd','rmse','nmad','p95','rmse_ci95','rmse_boot95'):
>     print(f"{k:12s} all={full[k]}  clean={clean[k]}")
> print("flagged as blunders:", np.flatnonzero(flag), e[flag])
> print("1.96*RMSE (clean) =", 1.96*clean['rmse'], " vs empirical p95 =", clean['p95'])
> ```
>
> Expected outcome (seed 7): with all 50 points, RMSE ≈ 0.31 m and σ ≈ 0.31 m, while median ≈ 0.03 m and NMAD ≈ 0.10 m; the two injected points are flagged; after their removal RMSE ≈ 0.10 m, the chi-square CI on RMSE is about [0.086, 0.128] m (≈ ±20 %), the bootstrap CI is similar, and 1.96·RMSE (0.201 m) and the empirical 95th percentile (0.209 m) agree within a centimeter — confirming the Gaussian core. Note that the bootstrap CI on the *uncleaned* RMSE is [0.09, 0.50] m: with blunders present, the RMSE is barely estimable at all. The report should list *both* rows, the rule, and the two flagged points.

## Then & now

The statistical toolkit is older than the data it now serves. Legendre (1805) and Gauss (1809) introduced least squares for orbit determination; Gauss's 1821–1826 *Theoria combinationis* gave the weighted form and the minimum-variance justification that geodesists still cite, and national triangulation networks were the first large-scale application. The error ellipse, the propagation law, and the a posteriori variance factor were all nineteenth-century geodesy. Hydrographers inherited a more qualitative tradition — lead-line soundings were "reliable" or not — until echo sounders (1920s) and multibeam (1970s–1980s) produced enough redundant data to treat statistically.

Three developments made the twentieth century's toolkit. Kalman (1960) ⟨H⟩ recast sequential least squares as a recursive filter in time; within a few years it was in the Apollo guidance computer, then in inertial navigation, and by the 1990s in GNSS/INS trajectory determination for every mapping sensor. Baarda (1968) formalized blunder detection and reliability for geodetic networks, a disciplined alternative to "throw out the points that look bad." Matheron's regionalized-variable theory (1960s, from mining), codified by Journel and Huijbregts (1978) and Cressie (1993), supplied the variogram and kriging, which the GIS community adopted for DEM error propagation through Heuvelink (1998) and for hydrologic sensitivity through Wechsler (2007).

Accuracy *standards* lagged. The US National Map Accuracy Standards (1947) required 90 % of elevations within half a contour interval; the NSSDA (FGDC 1998) replaced the map-scale basis with RMSE and the 95 % multipliers used here; ASPRS Edition 1 (2014) decoupled accuracy from map scale and introduced the NVA/VVA split; Edition 2 (2023) added 3D point-cloud accuracy, raised the checkpoint minimum, moved to RMSE-only reporting, and relaxed the fixed 3× checkpoint rule. Hydrography's S-44 moved from fixed depth tolerances to the TPU-based $\sqrt{a^2 + (bd)^2}$ formulation in the 4th edition (1998), following Hare (1995); CUBE (Calder and Mayer 2003) made per-node uncertainty routine, and BAG (2006) and S-102 (2012–) made it a *required* layer. The 2010s and 2020s brought the spatial-correlation reckoning: Rolstad et al. (2009) and Hugonnet et al. (2022) showed that glacier mass-balance uncertainties had been understated by an order of magnitude, and xdem made the corrected procedure accessible.

## Mathematics

Notation: $e_i$ error of the $i$-th sample; $n$ sample size; $\sigma$ population standard deviation; $s$ sample standard deviation; $\Phi^{-1}$ the standard normal quantile function.

**Descriptive statistics.**
$$\bar e = \tfrac1n\sum e_i,\qquad s^2 = \tfrac{1}{n-1}\sum(e_i-\bar e)^2,\qquad \text{RMSE} = \sqrt{\tfrac1n\sum e_i^2},\qquad \text{RMSE}^2 \approx \bar e^2 + s^2 .$$
$$\text{MAD} = \operatorname{median}_i\,\lvert e_i - \operatorname{median}(e)\rvert,\qquad \text{NMAD} = \frac{\text{MAD}}{\Phi^{-1}(0.75)} = 1.4826\,\text{MAD}.$$

**Gaussian coverage factors.** For $e \sim N(0,\sigma^2)$: $P(|e| \le k\sigma) = 2\Phi(k) - 1$, giving $k = 0.6745$ (50 %), $1.0000$ (68.27 %), $1.6449$ (90 %), $1.9600$ (95 %), $2.5758$ (99 %). For the radial error $r = \sqrt{e_x^2 + e_y^2}$ with $e_x, e_y \sim N(0,\sigma^2)$ independent, $r$ is Rayleigh: $P(r \le k\sigma) = 1 - \exp(-k^2/2)$, giving $k = \sqrt{-2\ln(1-p)}$: $1.1774$ (50 %), $2.1460$ (90 %), $2.4477$ (95 %). Since $\text{RMSE}_r = \sigma\sqrt2$ for equal components, $\text{CE95} = 2.4477\,\text{RMSE}_r/\sqrt 2 = 1.7308\,\text{RMSE}_r$. For 3D with equal components, $r$ is Maxwell-distributed; $k \approx 2.50$ (90 %) and $2.80$ (95 %).

**Bias and coverage.** For $e \sim N(b, \sigma^2)$, $P(|e| \le c) = \Phi\!\left(\frac{c-b}{\sigma}\right) - \Phi\!\left(\frac{-c-b}{\sigma}\right)$; the 95 % half-width $c_{95}$ solving this equals $1.96\sigma$ only at $b = 0$.

**Confidence interval on σ (and approximately RMSE).**
$$\sqrt{\frac{n-1}{\chi^2_{1-\alpha/2,\,n-1}}}\,s \le \sigma \le \sqrt{\frac{n-1}{\chi^2_{\alpha/2,\,n-1}}}\,s .$$

**Propagation.** $\Sigma_y = J\Sigma_x J^{\mathsf T}$; scalar, uncorrelated: $\sigma_y^2 = \sum_j (\partial f/\partial x_j)^2\sigma_j^2$. Difference of two correlated quantities: $\sigma^2_{z_1 - z_2} = \sigma_1^2 + \sigma_2^2 - 2\rho\sigma_1\sigma_2$.

**Limit of detection** for change between two DEMs: $\text{LoD}_{95} = 1.96\sqrt{\sigma_1^2 + \sigma_2^2}$ per cell (independent errors); for an areal mean, replace σ by $\sigma/\sqrt{n_{\text{eff}}}$ for each DEM.

**Quantization noise.** Uniform error on $[-q/2, q/2]$: $\sigma_q^2 = \frac{1}{q}\int_{-q/2}^{q/2} x^2\,dx = q^2/12$.

**Semivariogram and effective samples.** $\gamma(h) = \tfrac12\mathrm{E}[(e(\mathbf s) - e(\mathbf s+\mathbf h))^2] = \sigma^2(1 - \rho(h))$ for a stationary field. Spherical model with range $L$ and sill $\sigma^2$: $\gamma(h) = \sigma^2\left[\tfrac32\tfrac hL - \tfrac12\left(\tfrac hL\right)^3\right]$ for $h \le L$, $\sigma^2$ beyond. Variance of the areal mean over $A \gg A_c = \pi L^2$: $\sigma_{\bar e}^2 \approx \sigma^2 A_c/(5A)$; multi-range: $\sigma_{\bar e}^2 \approx \sum_k \sigma_k^2 A_{c,k}/(5A)$ for each nested component (components with $A_{c,k} \gtrsim A$ contribute $\approx \sigma_k^2$ in full). General: $n_{\text{eff}} = n^2/\sum_{i,j}\rho_{ij}$.

**Kriging variance** (ordinary kriging at $\mathbf s_0$ with weights $\lambda_i$ and Lagrange multiplier $\mu$): $\sigma_K^2(\mathbf s_0) = \sum_i \lambda_i\gamma(\mathbf s_i - \mathbf s_0) + \mu$.

**Weighted least squares.** Normal equations $N\hat{\mathbf x} = \mathbf t$ with $N = A^{\mathsf T}PA$, $\mathbf t = A^{\mathsf T}P\boldsymbol\ell$; $\Sigma_{\hat x} = \hat\sigma_0^2 N^{-1}$; $\hat\sigma_0^2 = \hat{\mathbf v}^{\mathsf T}P\hat{\mathbf v}/(n-u)$; redundancy matrix $\mathbf R = I - AN^{-1}A^{\mathsf T}P$, $r_i = R_{ii}$, $\sum r_i = n - u$; standardized residual $w_i = \hat v_i/(\sigma_0\sqrt{(\Sigma_\ell R)_{ii}})$ (Baarda's w-test).

**Kalman filter.** Predict $\mathbf x^- = F\mathbf x,\ P^- = FPF^{\mathsf T} + Q$; gain $K = P^-H^{\mathsf T}(HP^-H^{\mathsf T} + R)^{-1}$; update $\mathbf x = \mathbf x^- + K(\mathbf z - H\mathbf x^-),\ P = (I - KH)P^-$. The update is the WLS solution of $\begin{bmatrix}\mathbf x^- \\ \mathbf z\end{bmatrix} = \begin{bmatrix} I \\ H\end{bmatrix}\mathbf x$ with weights $\operatorname{blockdiag}((P^-)^{-1}, R^{-1})$.

## Validation & uncertainty

This chapter *is* the validation toolkit, so this section turns inward: how do the statistics themselves go wrong, and how do you validate an uncertainty estimate?

**How the statistics mislead.** (1) RMSE and σ are dominated by the few largest errors; a sample's RMSE can be set by 2 % of its points. (2) The 1.96 multiplier presumes symmetry; vegetated errors are one-sided, so $1.96\cdot\text{RMSE}$ may *under*-cover the positive tail while over-covering the negative. (3) Small-sample percentiles are nearly meaningless: the 95th percentile of 20 points is between the 19th and 20th ordered value. (4) The reference's own error adds in quadrature and its *bias* adds linearly — a reference survey in the wrong epoch or geoid model shifts every "error" by the same amount, and no statistic will reveal it. (5) Spatial correlation makes $n$ a fiction for areal quantities.

**Validating an uncertainty estimate.** An uncertainty layer or a propagated σ is a *prediction* about the distribution of errors; it can be tested. Compute standardized residuals $e_i/\sigma_i$ at independent checkpoints: their standard deviation should be ≈ 1 (0.5 means the uncertainties are twice too pessimistic; 2 means twice too optimistic), their distribution approximately standard normal, and $|e_i| \le 1.96\sigma_i$ should hold for ≈ 95 % of points. Binning by predicted σ and plotting observed RMSE per bin against predicted σ (a "reliability diagram") shows whether the model discriminates good from bad cells or merely gets the average right. Hugonnet et al. (2022) applied exactly this test to their heteroscedastic (slope- and curvature-dependent) DEM uncertainty model; it applies equally to CUBE uncertainties against crosslines ([Chapter 53](ch53-accuracy-assessment.md)).

**Outlier policy, stated once.** (a) Define the rule *before* looking at results (e.g., $|e - \tilde e| > 3\cdot\text{NMAD}$, or a physical criterion such as "checkpoint within 2 m of a breakline"). (b) Investigate every flagged point and record a reason; a point with no identifiable cause is *not* a blunder but a tail sample and should be retained in the robust statistics. (c) Report statistics with and without the flagged points. (d) Never remove points iteratively until a specification is met.

> **Uncertainty budget.** Typical contributions to a *reported* vertical RMSE of 0.15 m for a lidar DTM on open ground, decomposed by source (illustrative magnitudes consistent with QL2 practice; a real budget must be built from the project's own data).
>
> | Component | Type (GUM) | 1σ (m) | Correlated over | Notes |
> |---|---|---|---|---|
> | GNSS/INS vertical position | B (manufacturer, PPK report) | 0.05 | Minutes / km along track | Dominant; drift-like |
> | Attitude + boresight at edge of swath | B/A (calibration) | 0.03 | Whole strip | Roll error → cross-track tilt |
> | Range noise and pulse detection | A (overlap stats) | 0.02 | None (white) | Averages in gridding |
> | Geoid model (GEOID18) | B (NGS stated) | 0.02–0.03 | 10–100 km | Converts h → H; a tilt, not noise |
> | Ground classification + interpolation | A (checkpoint residuals by cover) | 0.03 (open) – 0.3 (forest) | Tens of m | One-sided in vegetation |
> | Checkpoint reference (RTK GNSS) | A/B | 0.02–0.03 | None | Adds to observed RMSE |
> | Checkpoint–DEM extraction (bilinear on 1 m grid, 5 % slope) | B | 0.01 | None | Scales with slope × cell |
> | **Root-sum-square (open ground)** | | **≈ 0.075–0.085** | | Observed 0.15 m implies an unbudgeted systematic term — investigate |

The last row is the point: when the budget and the observed statistics disagree, one of them is wrong, and the disagreement is the most valuable diagnostic in the report.

## Software

**Open source:** **xdem** (Python) — DEM co-registration, stable-terrain variograms, multi-range $n_{\text{eff}}$, heteroscedastic uncertainty maps; the reference implementation of Hugonnet et al. 2022. **demcoreg** — Nuth–Kääb co-registration and stable-terrain masking. **scikit-gstat** and **gstools** — variogram fitting, kriging, and conditional/unconditional Gaussian simulation. **NumPy/SciPy** — everything in the Try-it box; `scipy.stats` for χ², normality tests, bootstrap. **R gstat / sp / terra** — the classical geostatistics stack; `gstat::krige` with `nsim` for sequential Gaussian simulation. **PDAL** `filters.stats`, `filters.hag_*`, `filters.outlier` — point-cloud statistics and documented outlier flagging; **GDAL** `gdalinfo -stats`, `gdal_calc.py` for difference maps; **GMT** `grdmath`, `blockmedian` for robust gridding. **RTKLIB** and **GNSSTk** expose least-squares and Kalman internals for GNSS. Shared caveat: variogram and $n_{\text{eff}}$ results are only as good as the stable-terrain mask. **Free but closed:** NOAA/NGS OPUS reports (peak-to-peak and RMS of solutions as a Type A input); Leica/Trimble office exports of adjustment statistics. **Commercial:** CARIS HIPS and QPS Qimera — Hare-style TPU engines with vendor sensor libraries and CUBE surfaces with uncertainty layers (caveat: the TPU is only as good as the entered sensor uncertainties, often left at defaults); Terrasolid TerraMatch/TerraScan — strip adjustment with residual and tie-line reports; Agisoft Metashape and Pix4D — bundle-adjustment reports with reprojection error, GCP/checkpoint residuals, and (Metashape) parameter covariances; Esri Geostatistical Analyst — kriging and simulation with a GUI.

## Standards & guides

- **JCGM 100:2008** (GUM) and **JCGM 101:2008** (Supplement 1: Monte Carlo) — uncertainty vocabulary, Type A/B, coverage factors, propagation.
- **JCGM 200:2012** (VIM 3rd ed.) — definitions of accuracy, trueness, precision, uncertainty.
- **ISO 19157-1:2023** — data-quality elements and measures for geographic information, including positional accuracy measures (RMSE, LE90, CE90 are catalogued as standard measures).
- **ISO 5725 (parts 1–6)** — trueness and precision; repeatability and reproducibility experiments.
- **FGDC-STD-007.3-1998**, *Geospatial Positioning Accuracy Standards Part 3: National Standard for Spatial Data Accuracy (NSSDA)* — RMSE-based reporting; 1.96 and 2.4477 multipliers; minimum 20 checkpoints.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (Version 1.0, 2023; Version 2, June 2024)** — NVA/VVA, checkpoint counts, 3D accuracy, checkpoint accuracy requirements.
- **USGS Lidar Base Specification 2024** — absolute (NVA/VVA) and relative (intraswath/interswath) accuracy requirements and test methods.
- **IHO S-44 Edition 6.1.0 (2022)** — TVU/THU formulation and coverage factors; and **IHO S-102 Edition 3.0.0 (December 2024)** — bathymetric surface with 95 % uncertainty layer.
- **NOAA Hydrographic Surveys Specifications and Deliverables (HSSD, 2024)** — TPU model requirements, CUBE parameters, crossline analysis.
- **Open Navigation Surface BAG Format Specification v2.0** — uncertainty layer types and semantics.

## Pitfalls

- **RMSE from a sample containing blunders** → RMSE weights large errors quadratically → always report median and NMAD beside it; flag outliers by a pre-declared rule and show both rows.
- **95 % = 1.96 × RMSE on vegetated or urban errors** → the formula assumes an unbiased Gaussian → test with a Q–Q plot and compare against the empirical 95th percentile; use percentiles for VVA.
- **Ignoring spatial correlation in volume or mean-change uncertainty** → each cell is treated as an independent sample → estimate the variogram on stable terrain, compute $n_{\text{eff}}$; expect uncertainties 10–100× larger than $\sigma/\sqrt n$.
- **Reusing control points as checkpoints** → one field campaign, no points withheld → residuals at control measure fit; require an independent set, ideally a different method or epoch.
- **Checkpoints in a different datum, geoid model, or epoch than the DEM** → metadata was incomplete or the transformation was skipped → a constant offset in the residuals equal to a datum or geoid difference is the signature; transform explicitly and record it.
- **Reporting precision as accuracy** → σ from overlaps, σ₀ from a bundle adjustment, or a float32 encoding is quoted as "accuracy" → label internal statistics as relative/precision; accuracy requires external, independent reference.
- **Treating the a priori TPU as validated uncertainty** → default sensor values in the TPU engine → compare standardized residuals at crosslines; adjust the model until their σ ≈ 1.
- **Confidence interval on the mean quoted as the accuracy** → $s/\sqrt n$ is small and looks good → coverage of individual errors is $s$, not $s/\sqrt n$.
- **Small-sample percentiles** → 20 checkpoints and a "95th percentile" → report the sample size and the CI; with $n < 50$ do not report percentiles above the 90th.
- **Pooling strata** → a single RMSE across open, forested, and urban points → the mixture describes none; stratify and report per class.
- **Iterative outlier removal until the spec passes** → the specification is a target, not a measurement → fix the rule before looking; report everything removed and why.
- **Trusting $\Sigma_{\hat x}$ from an adjustment as total uncertainty** → the covariance matrix contains only random error under the assumed model → add Type B terms for unmodeled systematics (datum, geoid, lever arms); check $\hat\sigma_0^2 \approx 1$.
- **Quantization treated as negligible everywhere** → 0.29 m is small against 5 m RMSE → it dominates slope and curvature noise on coarse integer DEMs; compute the derivative's noise explicitly.

## Key takeaways

- There is no accuracy without a reference, a sample design, and a date; an RMSE without $n$, stratum, reference accuracy, and datum/epoch is not a result.
- Decompose: report bias (mean/median) and scatter (σ/NMAD) separately; RMSE alone hides which you have.
- Use robust statistics (median, NMAD, empirical percentiles) alongside classical ones; use Gaussian multipliers only after testing normality and bias.
- Uncertainty is a distribution about our knowledge; error is one unknown number. Combine Type A and Type B evaluations; state coverage factors; know whether a "95 %" is coverage, confidence, or a sample percentile.
- Propagate with $J\Sigma J^{\mathsf T}$ when the model is smooth, Monte Carlo when it is not, and spatially correlated simulation when the output integrates over area.
- Model the spatial structure of error or downstream uncertainty is fiction: $n_{\text{eff}} \approx 5A/(\pi L^2)$, and long-range components do not average out.
- Reference data must be independent and ≥ 3× (preferably 5–10×) more accurate; sample size sets the confidence interval on your statistics — 20 points give ±35 % on σ.
- Least squares and the Kalman filter are one engine behind GNSS, INS, bundle adjustment, strip adjustment, network adjustment, and SLAM; read their reports for σ₀, redundancy, and rejected observations.
- Validate uncertainty estimates with standardized residuals at independent points; when budget and observation disagree, that disagreement is the finding.

## References

- ASPRS. 2015. ASPRS Positional Accuracy Standards for Digital Geospatial Data (Edition 1, v1.0, 2014). *Photogrammetric Engineering & Remote Sensing* 81(3):A1–A26.
- ASPRS. 2023. *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (Version 2 adopted June 2024). Bethesda, MD: ASPRS.
- Baarda, W. 1968. *A Testing Procedure for Use in Geodetic Networks*. Publications on Geodesy, New Series 2(5). Delft: Netherlands Geodetic Commission.
- Calder, B. R. 2006. On the uncertainty of archive hydrographic data sets. *IEEE Journal of Oceanic Engineering* 31(2):249–265. doi:10.1109/JOE.2006.872215
- Calder, B. R., and L. A. Mayer. 2003. Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems* 4(6):1048. doi:10.1029/2002GC000486
- Chilès, J.-P., and P. Delfiner. 2012. *Geostatistics: Modeling Spatial Uncertainty*, 2nd ed. Hoboken, NJ: Wiley.
- Cressie, N. A. C. 1993. *Statistics for Spatial Data*, rev. ed. New York: Wiley.
- FGDC. 1998. *Geospatial Positioning Accuracy Standards, Part 3: National Standard for Spatial Data Accuracy*. FGDC-STD-007.3-1998. Reston, VA: Federal Geographic Data Committee.
- Fisher, P. F., and N. J. Tate. 2006. Causes and consequences of error in digital elevation models. *Progress in Physical Geography* 30(4):467–489. doi:10.1191/0309133306pp492ra
- Ghilani, C. D. 2017. *Adjustment Computations: Spatial Data Analysis*, 6th ed. Hoboken, NJ: Wiley.
- Hare, R. 1995. Depth and position error budgets for multibeam echosounding. *International Hydrographic Review* 72(2):37–69.
- Heuvelink, G. B. M. 1998. *Error Propagation in Environmental Modelling with GIS*. London: Taylor & Francis.
- Höhle, J., and M. Höhle. 2009. Accuracy assessment of digital elevation models by means of robust statistical methods. *ISPRS Journal of Photogrammetry and Remote Sensing* 64(4):398–406. doi:10.1016/j.isprsjprs.2009.02.003
- Hugonnet, R., F. Brun, E. Berthier, R. Dehecq, E. S. Mannerfelt, N. Eckert, and D. Farinotti. 2022. Uncertainty analysis of digital elevation models by spatial inference from stable terrain. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing* 15:6456–6472. doi:10.1109/JSTARS.2022.3188922
- International Hydrographic Organization. 2022. *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. Monaco: IHO.
- JCGM. 2008. *JCGM 100:2008 Evaluation of measurement data — Guide to the expression of uncertainty in measurement*. Sèvres: BIPM.
- JCGM. 2008. *JCGM 101:2008 Supplement 1 — Propagation of distributions using a Monte Carlo method*. Sèvres: BIPM.
- Journel, A. G., and C. J. Huijbregts. 1978. *Mining Geostatistics*. London: Academic Press.
- Kalman, R. E. 1960. A new approach to linear filtering and prediction problems. *Journal of Basic Engineering* 82(1):35–45. doi:10.1115/1.3662552
- Mikhail, E. M., and F. Ackermann. 1976. *Observations and Least Squares*. New York: IEP–Dun-Donnelley.
- Nuth, C., and A. Kääb. 2011. Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere* 5(1):271–290. doi:10.5194/tc-5-271-2011
- Rolstad, C., T. Haug, and B. Denby. 2009. Spatially integrated geodetic glacier mass balance and its uncertainty based on geostatistical analysis: application to the western Svartisen ice cap, Norway. *Journal of Glaciology* 55(192):666–680. doi:10.3189/002214309789470950
- Teunissen, P. J. G. 2000. *Testing Theory: An Introduction*. Delft: Delft University Press.
- Wechsler, S. P. 2007. Uncertainties associated with digital elevation models for hydrologic applications: a review. *Hydrology and Earth System Sciences* 11(4):1481–1500. doi:10.5194/hess-11-1481-2007
- Wechsler, S. P., and C. N. Kroll. 2006. Quantifying DEM uncertainty and its effect on topographic parameters. *Photogrammetric Engineering & Remote Sensing* 72(9):1081–1090.

# Appendix B — Mathematical reference

Formulas collected from the "Math" lines of the chapters, with notation defined and a short worked numeric example in each section. Cross-references point to the chapter where the derivation and the caveats live. Notation: $h$ ellipsoidal height, $H$ orthometric height, $N$ geoid undulation ($h = H + N$); $\sigma$ standard deviation; $\Sigma$ covariance matrix; $a, b, f, e^2$ ellipsoid semi-axes, flattening, first eccentricity squared; $\varphi, \lambda$ geodetic latitude and longitude; $c$ speed of light or sound as context requires.

| Symbol | Meaning | Symbol | Meaning |
|---|---|---|---|
| $e_i$ | error of sample $i$, $\hat z_i - z_i$ | $n$ | number of samples |
| $\bar e$ | mean error (bias) | $J$ | Jacobian matrix |
| $\mathrm{MAD}$ | median absolute deviation | $\ell$ | correlation length |
| $R$ | mean Earth radius ≈ 6,371 km | $k$ | refraction coefficient |
| $\Delta$ | grid spacing | $B_\perp$ | perpendicular baseline (InSAR) |

## B.1 Statistics of error

For errors $e_i = \hat z_i - z_i$ against an independent reference ([Chapter 5](../chapters/ch05-error-and-uncertainty.md), [Chapter 53](../chapters/ch53-accuracy-assessment.md)):

$$ \bar e = \frac{1}{n}\sum e_i, \qquad \sigma = \sqrt{\frac{1}{n-1}\sum (e_i - \bar e)^2}, \qquad \mathrm{RMSE} = \sqrt{\frac{1}{n}\sum e_i^2}, \qquad \mathrm{MAE} = \frac{1}{n}\sum |e_i| $$

$$ \mathrm{RMSE}^2 = \bar e^{\,2} + \frac{n-1}{n}\sigma^2 \approx \bar e^{\,2} + \sigma^2 $$

**Robust estimators.** $\mathrm{NMAD} = 1.4826 \cdot \mathrm{median}(|e_i - \mathrm{median}(e)|)$ estimates $\sigma$ under normality and is insensitive to outliers; report the median as the robust bias and the 68.3 % and 95 % absolute-error percentiles as robust spread.

**95 % conversions (normal assumption only).** Vertical: $\mathrm{LE95} = 1.9600\,\sigma$ (zero bias) or, per NSSDA, $1.9600 \cdot \mathrm{RMSE}_z$. Horizontal, circular normal with $\sigma_x = \sigma_y$: $\mathrm{CE95} = 2.4477\,\sigma$; in terms of the radial RMSE $\mathrm{RMSE}_r = \sqrt{\mathrm{RMSE}_x^2 + \mathrm{RMSE}_y^2}$, $\mathrm{CE95} = 1.7308\,\mathrm{RMSE}_r$. LE90 $= 1.6449\,\sigma$; CE90 $= 2.1460\,\sigma$. ASPRS Positional Accuracy Standards Ed. 1 (2014) and the USGS Lidar Base Specification define NVA $= 1.96 \cdot \mathrm{RMSE}_z$ and VVA as the 95th percentile of $|e|$ because vegetated errors are not normal; ASPRS Ed. 2 (2023) keeps NVA/VVA only as checkpoint strata and reports both as $\mathrm{RMSE}_V$ (and $\mathrm{RMSE}_H$ horizontally), dropping the 1.96× and 95th-percentile statistics, with the 95 % value still derived as $1.96 \cdot \mathrm{RMSE}$ where normality holds.

**Confidence interval for RMSE** (normal errors, zero bias): $(n-1)s^2/\sigma^2 \sim \chi^2_{n-1}$, so

$$ \mathrm{RMSE}\sqrt{\frac{n-1}{\chi^2_{n-1,\,1-\alpha/2}}} \;\le\; \sigma \;\le\; \mathrm{RMSE}\sqrt{\frac{n-1}{\chi^2_{n-1,\,\alpha/2}}} . $$

**Outlier tests.** Flag $|e_i - \mathrm{median}| > 3\,\mathrm{NMAD}$ (robust 3σ) or use Chauvenet/Grubbs for small normal samples; report how many were removed and why.

> **Worked example (B.13e).** Thirty checkpoints give $\mathrm{RMSE}_z = 0.092$ m with negligible bias. With $\chi^2_{29,\,0.975} = 45.72$ and $\chi^2_{29,\,0.025} = 16.05$: lower $= 0.092\sqrt{29/45.72} = 0.073$ m, upper $= 0.092\sqrt{29/16.05} = 0.124$ m. The 95 % CI on σ is 7.3–12.4 cm, so a 10 cm specification is neither clearly met nor clearly failed with 30 points; NVA $= 1.96 \times 0.092 = 0.18$ m with CI 0.14–0.24 m.

## B.2 Error propagation

**Linear (first-order).** For $\mathbf{y} = f(\mathbf{x})$ with Jacobian $J = \partial f/\partial \mathbf{x}$:

$$ \Sigma_y = J\,\Sigma_x\,J^{\mathsf T}. $$

For a scalar function of independent inputs this reduces to $\sigma_y^2 = \sum_i (\partial f/\partial x_i)^2 \sigma_i^2$.

**Monte Carlo.** Draw $\mathbf{x}^{(k)} \sim \mathcal N(\hat{\mathbf x}, \Sigma_x)$ for $k = 1..K$, evaluate $\mathbf{y}^{(k)}$, and summarize; required when $f$ is nonlinear or non-Gaussian. $K = 10^3$–$10^4$ gives percentiles to a few percent.

**Spatially correlated fields.** Model the error covariance $C(d) = \sigma^2 \rho(d)$ with a variogram $\gamma(d) = \sigma^2 - C(d)$ (exponential: $\rho = e^{-d/\ell}$; spherical with range $a$; nugget for white noise). Sequential Gaussian simulation (SGS) generates realizations honouring $C(d)$ for Monte Carlo propagation through nonlinear operations (slope, flow routing).

**Effective sample size.** For a mean over $n$ cells of spacing $\Delta$ with exponential correlation length $\ell$, approximately

$$ n_{\mathrm{eff}} \approx \frac{n}{1 + 2\sum_{k\ge 1} \rho(k\Delta)} \quad \text{(1-D)}, \qquad n_{\mathrm{eff}} \approx \frac{A}{\int \rho\,\mathrm{d}A} = \frac{A}{2\pi \ell^2} \quad \text{(2-D exponential, } A \gg \ell^2\text{)}. $$

The constant depends on the correlation model: $\int\rho\,\mathrm{d}A = 2\pi\ell^2$ for the exponential model, $\pi\ell^2$ for a Gaussian model $\rho = e^{-d^2/\ell^2}$. Treat $n_{\mathrm{eff}}$ as an order-of-magnitude quantity unless the variogram has actually been fitted.

**Volume uncertainty with correlation.** For a volume $V = \Delta^2 \sum_i \delta z_i$ over $n$ cells with per-cell σ and correlation $\rho_{ij}$:

$$ \sigma_V^2 = \Delta^4 \sum_i \sum_j \sigma_i \sigma_j \rho_{ij} \;\approx\; \Delta^4\, n\, \sigma^2 \left(1 + \frac{2\pi \ell^2}{\Delta^2}\right) \;\approx\; A\,\sigma^2\, 2\pi\ell^2 \quad (\ell \gg \Delta). $$

> **Worked example (B.13f).** A stockpile DoD covers $A = 10{,}000$ m² at $\Delta = 0.5$ m ($n = 40{,}000$ cells), per-cell $\sigma = 0.05$ m, correlation length $\ell = 20$ m. Uncorrelated: $\sigma_V = \Delta^2 \sigma\sqrt{n} = 0.25 \times 0.05 \times 200 = 2.5$ m³. Correlated: $\sigma_V \approx \sqrt{A \sigma^2 2\pi \ell^2} = \sqrt{10^4 \times 0.0025 \times 2513} = 251$ m³ — a hundred times larger, and $n_{\mathrm{eff}} \approx A/(2\pi\ell^2) \approx 4$. Ignoring correlation is the commonest error in volume reporting ([Chapter 65](../chapters/ch65-mining-landfills-earthworks.md)).

## B.3 Geodesy

**Ellipsoid.** $f = (a-b)/a$, $e^2 = 2f - f^2$. GRS80: $a = 6\,378\,137$ m, $1/f = 298.257\,222\,101$; WGS 84: same $a$, $1/f = 298.257\,223\,563$ (difference ≈ 0.1 mm in $b$). Radii of curvature:

$$ N_\varphi = \frac{a}{\sqrt{1 - e^2\sin^2\varphi}} \ (\text{prime vertical}), \qquad M = \frac{a(1-e^2)}{(1 - e^2\sin^2\varphi)^{3/2}} \ (\text{meridional}). $$

**Geodetic → ECEF.**

$$ X = (N_\varphi + h)\cos\varphi\cos\lambda, \quad Y = (N_\varphi + h)\cos\varphi\sin\lambda, \quad Z = \big(N_\varphi(1-e^2) + h\big)\sin\varphi . $$

The inverse is iterative in $\varphi$ (or closed-form via Bowring/Vermeille); $h = p/\cos\varphi - N_\varphi$ with $p = \sqrt{X^2+Y^2}$.

**Helmert 7-parameter (similarity) transformation**, small-angle form:

$$ \begin{bmatrix} X \\ Y \\ Z \end{bmatrix}_B = \begin{bmatrix} t_X \\ t_Y \\ t_Z \end{bmatrix} + (1 + s) \begin{bmatrix} 1 & -r_Z & r_Y \\ r_Z & 1 & -r_X \\ -r_Y & r_X & 1 \end{bmatrix} \begin{bmatrix} X \\ Y \\ Z \end{bmatrix}_A $$

with $s$ the scale difference (quoted in ppm, i.e. $s = 10^{-6}\times$ the tabulated value) and rotations in radians (⚠ sign convention differs between "position vector" and "coordinate frame" conventions; EPSG method codes 1033 vs 1032). The **14-parameter** form adds rates $\dot t, \dot r, \dot s$ applied as $p(t) = p(t_0) + \dot p\,(t - t_0)$.

**Heights.** Geopotential number $C = W_0 - W_P = \int_0^P g\,\mathrm{d}n$. Orthometric $H = C/\bar g$ (Helmert: $\bar g = g_P + 0.0424\,H$ mGal); normal $H^* = C/\bar\gamma$; dynamic $H_{\mathrm{dyn}} = C/\gamma_{45}$. $N = h - H$; the quasi-geoid height (height anomaly) $\zeta = h - H^*$.

**Plate velocity.** $\mathbf{v} = \boldsymbol\omega \times \mathbf{r}$ with $\boldsymbol\omega$ the Euler vector (rad/yr) and $\mathbf{r}$ the ECEF position; $|\mathbf v| = |\boldsymbol\omega|\,R\sin\theta$ with $\theta$ the angular distance from the pole.

> **Worked example.** At $\varphi = 45°$ on GRS80: $\sin^2\varphi = 0.5$, $e^2 = 0.006\,694\,380$, $N_\varphi = 6\,378\,137/\sqrt{1 - 0.003\,347} = 6\,388\,838$ m, $M = 6\,378\,137 \times 0.993\,306/(0.996\,653)^{3/2} = 6\,367\,382$ m. One arc second of latitude is $M \cdot 4.848\times10^{-6} = 30.87$ m; of longitude, $N_\varphi\cos\varphi \cdot 4.848\times10^{-6} = 21.90$ m — so a 1″ SRTM cell at 45° is 30.9 m × 21.9 m, not square ([Chapter 10](../chapters/ch10-projections-and-resampling.md)).

## B.4 Projections

**Scale factor** $k$ is the ratio of grid distance to ellipsoidal distance. Transverse Mercator (Snyder 1987 ⟨H⟩), to second order in the distance from the central meridian:

$$ k \approx k_0\left(1 + \frac{\Delta\lambda^2\cos^2\varphi}{2}\right) \approx k_0\left(1 + \frac{E'^2}{2R^2}\right), $$

where $E' = E - E_0$ is the easting from the central meridian. UTM: $k_0 = 0.9996$, so $k = 1$ at $E' \approx \pm 180$ km and $k \approx 1.00097$ at the zone edge ($E' = 334$ km at the equator).

**Grid convergence** $\gamma \approx \Delta\lambda \sin\varphi$ (angle between grid north and true north).

**Combined (grid-to-ground) factor.** Elevation factor $k_h = R/(R + h)$ (strictly, with the ellipsoidal height); combined $k_c = k \cdot k_h$. Ground distance $= $ grid distance $/ k_c$.

**Tissot.** Principal scale factors $a_T, b_T$ along the indicatrix axes: conformal if $a_T = b_T$ everywhere, equal-area if $a_T b_T = 1$; maximum angular distortion $2\arcsin\frac{a_T - b_T}{a_T + b_T}$.

> **Worked example.** A site at $h = 1{,}500$ m, 150 km from the UTM central meridian: $k \approx 0.9996(1 + 150^2/(2 \times 6371^2)) = 0.9996 \times 1.000277 = 0.99988$; $k_h = 6371/6372.5 = 0.99976$; $k_c = 0.99964$. A 1,000.000 m ground distance measures 999.64 m on the grid — a 36 cm discrepancy that will appear as a "scale error" if a design on ground coordinates is overlaid on a UTM DEM.

## B.5 Positioning

**GNSS observation equations.** Pseudorange $P$ and carrier phase $\Phi$ (metres) from satellite $s$ to receiver $r$:

$$ P_r^s = \rho_r^s + c(\mathrm{d}t_r - \mathrm{d}t^s) + I_r^s + T_r^s + \varepsilon_P, \qquad \Phi_r^s = \rho_r^s + c(\mathrm{d}t_r - \mathrm{d}t^s) - I_r^s + T_r^s + \lambda N_r^s + \varepsilon_\Phi , $$

with geometric range $\rho$, clock errors $\mathrm{d}t$, ionospheric and tropospheric delays $I, T$, wavelength $\lambda$, and integer ambiguity $N$. **Double differences** between two receivers and two satellites cancel both clocks and, over short baselines, most of $I$ and $T$, leaving $\nabla\Delta\rho + \lambda\nabla\Delta N$; fixing $\nabla\Delta N$ to integers (LAMBDA method) gives centimetre solutions. **DOP:** with design matrix $A$ of unit vectors and clock column, $Q = (A^{\mathsf T}A)^{-1}$; $\mathrm{PDOP} = \sqrt{Q_{11}+Q_{22}+Q_{33}}$, $\mathrm{VDOP} = \sqrt{Q_{33}}$; $\sigma_{\mathrm{pos}} = \mathrm{DOP} \times \sigma_{\mathrm{range}}$. VDOP typically exceeds HDOP by 1.5–2× because all satellites are above the horizon.

**Kalman filter** ⟨H⟩ (state $\mathbf x$, covariance $P$, transition $F$, process noise $Q$, measurement $\mathbf z = H\mathbf x + \mathbf v$, $R$):

$$ \mathbf{x}^- = F\mathbf{x}, \quad P^- = FPF^{\mathsf T} + Q, \quad K = P^-H^{\mathsf T}(HP^-H^{\mathsf T}+R)^{-1}, \quad \mathbf{x} = \mathbf{x}^- + K(\mathbf{z} - H\mathbf{x}^-), \quad P = (I-KH)P^- . $$

**Strapdown mechanization** (navigation frame $n$, body frame $b$): attitude $\dot C_b^n = C_b^n[\boldsymbol\omega_{ib}^b \times] - [(\boldsymbol\omega_{ie}^n + \boldsymbol\omega_{en}^n)\times]C_b^n$; velocity $\dot{\mathbf v}^n = C_b^n \mathbf f^b - (2\boldsymbol\omega_{ie}^n + \boldsymbol\omega_{en}^n)\times\mathbf v^n + \mathbf g^n$; position $\dot{\mathbf r} = \mathbf v^n$. Unaided position error grows as $\tfrac{1}{2}\delta a\,t^2$ for an accelerometer bias $\delta a$ and as $\tfrac{1}{6} g\,\delta\omega\, t^3$ for a gyro bias $\delta\omega$ over short intervals.

**Lever arm and boresight.** Ground point from a lidar range vector $\mathbf r^s$ in the sensor frame:

$$ \mathbf X^{m} = \mathbf X^{m}_{\mathrm{GNSS}} + C_b^m\left(\mathbf l^b_{\mathrm{sensor}} - \mathbf l^b_{\mathrm{GNSS}} + C_s^b\,\mathbf r^s\right), $$

where $C_b^m$ is the INS attitude, $C_s^b$ the boresight rotation, and $\mathbf l^b$ lever arms in the body frame. A boresight error $\delta\theta$ produces a ground error $\approx \rho\,\delta\theta$: at 1,000 m range, 0.01° (175 µrad) gives 17.5 cm ([Chapter 25](../chapters/ch25-calibration-infrastructure.md)).

> **Worked example.** A gyro bias of 0.01°/h ($4.85\times10^{-8}$ rad/s) unaided for 60 s: tilt error $\delta\omega t = 2.9\times10^{-6}$ rad; position error $\tfrac16 g\,\delta\omega\,t^3 = \tfrac16 \times 9.81 \times 4.85\times10^{-8} \times 216{,}000 = 0.017$ m. The same bias over 600 s gives 17 m — the reason GNSS outages of minutes, not seconds, are the planning constraint ([Chapter 13](../chapters/ch13-imu-ins.md)).

## B.6 Sensors

**Lidar range and footprint.** Range $\rho = c\,\Delta t/2$ ($c = 299\,792\,458$ m/s; 1 ns of timing error = 15 cm of range). Footprint diameter $D \approx \rho\,\gamma$ for beam divergence $\gamma$ (full angle, rad): 0.25 mrad at 1,500 m gives 0.375 m. Along-track spacing $= v/f_{\mathrm{scan}}$; across-track $\approx 2\rho\tan(\theta_{\max})/n_{\mathrm{pulses}}$. Range error from a timing jitter $\sigma_t$: $\sigma_\rho = c\,\sigma_t/2$. Pulse geometry on a slope $s$: the footprint's elevation spread is $D\tan s$, which smears the return ([Chapter 18](../chapters/ch18-topographic-lidar.md)).

**Refraction (Snell).** $n_1\sin\theta_1 = n_2\sin\theta_2$. Bathymetric lidar: air–water with $n_w \approx 1.33$–1.34 (532 nm), so a 20° incidence refracts to 14.9°; the in-water slant range must also be divided by $n_w$ because light is slower. Depth from slant range $r_w$ at in-water angle $\theta_2$: $d = r_w\cos\theta_2/n_w$ (with $r_w$ measured as if in air). An error of 0.01 in $n_w$ gives ~0.75 % depth error ([Chapter 19](../chapters/ch19-bathymetric-lidar.md)).

**Sonar.** Depth from two-way travel time $t$ at nadir: $d = \bar c\,t/2$ with harmonic-mean sound speed $\bar c$. Beam footprint across track $\approx d\,\theta_b/\cos^2\theta$ for beamwidth $\theta_b$ and steering angle $\theta$. **Ray tracing** through layers of constant gradient $g_i$ ($c = c_i + g_i z$): the ray is a circular arc with radius $R_i = c_i/(g_i\sin\theta_i)$ and Snell's constant $p = \sin\theta/c$ preserved across layers. Depth-at-angle sensitivity to a surface sound-speed error $\delta c_s$ in a flat-launched MBES: the launch angle error $\delta\theta \approx \tan\theta\,\delta c_s/c_s$ produces a depth error $\delta d \approx d\tan\theta\,\delta\theta$ — i.e., $\delta d/d \approx \tan^2\theta\,\delta c_s/c_s$ — the "smile/frown" ([Chapter 20](../chapters/ch20-sonar.md)).

> **Worked example (B.13c).** Depth 50 m, beam at 60°, surface sound speed assumed 1,500 m/s but actually 1,510 m/s ($\delta c_s/c_s = 0.67\%$). Angular error $\delta\theta \approx \tan 60° \times 0.0067 = 0.0115$ rad (0.66°); depth error $\approx 50 \times \tan 60° \times 0.0115 = 1.0$ m, i.e. 2 % of depth, versus 0.33 m (0.67 %) at nadir from the mean-speed error alone. IHO Order 1a TVU at 50 m is $\sqrt{0.5^2 + (0.013 \times 50)^2} = 0.82$ m at 95 %; the outer beam alone violates it ([Chapter 70](../chapters/ch70-specifications-guided-tour.md)).

**SAR geometry.** Ground range $= $ slant range $/\sin\theta_i$. Foreshortening when the terrain slope $\alpha < \theta_i$ (toward sensor); **layover** when $\alpha > \theta_i$; **shadow** on back slopes steeper than $90° - \theta_i$.

**InSAR phase to height.** Interferometric phase $\phi = \phi_{\mathrm{flat}} + \phi_{\mathrm{topo}} + \phi_{\mathrm{defo}} + \phi_{\mathrm{atm}} + \phi_{\mathrm{noise}}$. Topographic sensitivity:

$$ \frac{\partial \phi}{\partial h} = \frac{4\pi B_\perp}{\lambda\,\rho\,\sin\theta_i} \quad (\text{repeat-pass}), \qquad h_{\mathrm{amb}} = \frac{2\pi}{\partial\phi/\partial h} = \frac{\lambda\,\rho\,\sin\theta_i}{2 B_\perp}, $$

(single-pass bistatic systems such as TanDEM-X have a factor 2 smaller phase, hence $h_{\mathrm{amb}} = \lambda\rho\sin\theta_i/B_\perp$). Height error from phase noise $\sigma_\phi$: $\sigma_h = h_{\mathrm{amb}}\,\sigma_\phi/(2\pi)$. Coherence $|\gamma| = \gamma_{\mathrm{geom}}\gamma_{\mathrm{temp}}\gamma_{\mathrm{vol}}\gamma_{\mathrm{SNR}}$; phase standard deviation for $L$ looks $\sigma_\phi \approx \sqrt{(1-|\gamma|^2)/(2L|\gamma|^2)}$ ([Chapter 21](../chapters/ch21-radar-sar-insar.md)).

> **Worked example.** TanDEM-X: $\lambda = 3.1$ cm, $\rho = 600$ km, $\theta_i = 35°$, $B_\perp = 200$ m (bistatic): $h_{\mathrm{amb}} = 0.031 \times 6\times10^5 \times 0.574/200 = 53$ m. With coherence 0.8 and 10 looks, $\sigma_\phi = \sqrt{0.36/(2\times10\times0.64)} = 0.168$ rad, so $\sigma_h = 53 \times 0.168/6.283 = 1.4$ m — consistent with the mission's ~2 m relative accuracy at 90 %.

**Stereo parallax.** For vertical aerial photographs with base $B$, flying height $H_f$ above ground, focal length $f$: parallax $p = fB/(H_f - h)$, and height difference $\Delta h = \frac{H_f\,\Delta p}{p + \Delta p} \approx \frac{H_f^2}{fB}\Delta p$. Height precision $\sigma_h \approx \frac{H_f}{f}\cdot\frac{H_f}{B}\,\sigma_p = \mathrm{GSD}\cdot\frac{H_f}{B}\cdot\sigma_{p,\mathrm{px}}$: a base-to-height ratio of 0.6 and 0.3 px matching precision give $\sigma_h \approx 0.5\,\mathrm{GSD}$. Satellite stereo with convergence angle $\psi$: $\sigma_h \approx \sigma_{xy}/(2\tan(\psi/2))$.

**Collinearity.** $x - x_0 = -f\frac{r_{11}(X-X_c) + r_{12}(Y-Y_c) + r_{13}(Z-Z_c)}{r_{31}(X-X_c) + r_{32}(Y-Y_c) + r_{33}(Z-Z_c)}$ and similarly for $y$ with row 2; **coplanarity** $\mathbf b\cdot(\mathbf a_1\times\mathbf a_2) = 0$ for relative orientation. **Bundle adjustment** linearizes collinearity for all images and points: normal equations $(A^{\mathsf T}PA)\,\delta = A^{\mathsf T}P\mathbf l$ with a sparse block structure (camera block, point block) solved by Schur complement. **SfM scale ambiguity:** without control or known baseline, the reconstruction is determined up to a 7-parameter similarity; GCPs or GNSS camera positions fix it ([Chapter 22](../chapters/ch22-photogrammetry-sfm.md)).

**Satellite-derived bathymetry.** Stumpf log-ratio: $z = m_1\frac{\ln(nR_{\mathrm{blue}})}{\ln(nR_{\mathrm{green}})} - m_0$, with $m_0, m_1$ fitted to soundings and $n$ a constant keeping the logs positive. Lyzenga: $L_i = L_{\infty,i} + (L_{b,i} - L_{\infty,i})\,e^{-2K_i z}$ so that $\ln(L_i - L_{\infty,i})$ is linear in $z$ with slope $-2K_i$; the multi-band form solves for $z$ independent of bottom albedo given two bands ([Chapter 23](../chapters/ch23-satellite-derived-bathymetry.md)).

**Gravity–bathymetry admittance.** In the wavenumber domain, gravity anomaly $\Delta g(k) = 2\pi G\,\Delta\rho\, e^{-kd}\, h(k)\, \Phi(k)$ for topography $h$ at mean depth $d$, density contrast $\Delta\rho$, and isostatic filter $\Phi$; the inverse is band-limited to roughly 15–160 km wavelength, which is why altimetric bathymetry resolves nothing shorter than ~10–15 km (Smith & Sandwell 1997).

## B.7 Surfaces

**Delaunay / TIN.** The Delaunay triangulation maximizes the minimum angle and is unique for points in general position; the surface is piecewise planar, $C^0$. Linear interpolation inside triangle $(p_1,p_2,p_3)$ uses barycentric weights $z = \sum w_i z_i$, $\sum w_i = 1$.

**IDW.** $\hat z(\mathbf x) = \sum_i w_i z_i/\sum_i w_i$, $w_i = d_i^{-p}$ (usually $p = 2$); exact at data points, bounded by the data range (no extrapolation), produces "bull's-eyes" around isolated points.

**Thin-plate spline.** Minimizes $\iint (z_{xx}^2 + 2z_{xy}^2 + z_{yy}^2)\,\mathrm{d}x\,\mathrm{d}y$ subject to fitting the data; solution $z(\mathbf x) = a_0 + a_1 x + a_2 y + \sum_i \lambda_i\, r_i^2 \ln r_i$. Splines in tension (GMT `surface`) add a first-derivative term to suppress overshoot.

**Ordinary kriging.** Given variogram $\gamma(d)$, weights solve

$$ \begin{bmatrix} \Gamma & \mathbf 1 \\ \mathbf 1^{\mathsf T} & 0 \end{bmatrix} \begin{bmatrix} \mathbf w \\ \mu \end{bmatrix} = \begin{bmatrix} \boldsymbol\gamma_0 \\ 1 \end{bmatrix}, \qquad \sigma^2_{\mathrm{OK}} = \mathbf w^{\mathsf T}\boldsymbol\gamma_0 + \mu, $$

where $\Gamma_{ij} = \gamma(d_{ij})$ and $\gamma_{0,i} = \gamma(d_{0i})$. The kriging variance depends on data geometry, not on the values — it measures sampling density, not local fit ([Chapter 31](../chapters/ch31-interpolation-and-gridding.md)).

**ANUDEM sketch.** Iterative finite-difference thin-plate spline with a roughness penalty that is relaxed near drainage lines; a drainage-enforcement step removes spurious sinks by locating the lowest saddle and lowering the surface along a path to it.

**CUBE hypothesis updating.** Each node keeps one or more Kalman-like hypotheses $(\hat d, \sigma^2)$; a new sounding $(d_i, \sigma_i^2)$, propagated to the node with distance-weighted inflation, updates the nearest consistent hypothesis by $\hat d \leftarrow \frac{\sigma_i^2\hat d + \sigma^2 d_i}{\sigma^2 + \sigma_i^2}$, $\sigma^2 \leftarrow \frac{\sigma^2\sigma_i^2}{\sigma^2 + \sigma_i^2}$, or spawns a new hypothesis if the innovation exceeds a threshold; disambiguation picks by sounding count, neighbourhood consistency, or prior ([Chapter 20](../chapters/ch20-sonar.md)).

**Slope and aspect.** With the 3×3 neighbourhood $z_1..z_9$ (row-major, $z_5$ centre) and spacing $\Delta$, the **Horn** (1981) operator:

$$ \frac{\partial z}{\partial x} = \frac{(z_3 + 2z_6 + z_9) - (z_1 + 2z_4 + z_7)}{8\Delta}, \qquad \frac{\partial z}{\partial y} = \frac{(z_7 + 2z_8 + z_9) - (z_1 + 2z_2 + z_3)}{8\Delta}, $$

$$ \text{slope} = \arctan\sqrt{z_x^2 + z_y^2}, \qquad \text{aspect} = \mathrm{atan2}(z_y, -z_x)\ (\text{then rotated to compass convention}). $$

**Zevenbergen–Thorne** (1987) uses only the four edge neighbours: $z_x = (z_6 - z_4)/(2\Delta)$, $z_y = (z_8 - z_2)/(2\Delta)$, and curvatures from the second differences $z_{xx} = (z_4 - 2z_5 + z_6)/\Delta^2$, $z_{yy} = (z_2 - 2z_5 + z_8)/\Delta^2$, $z_{xy} = (-z_1 + z_3 + z_7 - z_9)/(4\Delta^2)$. Profile curvature $k_p = -\frac{z_{xx}z_x^2 + 2z_{xy}z_xz_y + z_{yy}z_y^2}{(z_x^2+z_y^2)(1+z_x^2+z_y^2)^{3/2}}$; plan curvature $k_c = -\frac{z_{xx}z_y^2 - 2z_{xy}z_xz_y + z_{yy}z_x^2}{(z_x^2+z_y^2)^{3/2}}$. Horn is less noise-sensitive; Zevenbergen–Thorne is more faithful on smooth surfaces ([Chapter 57](../chapters/ch57-visualizing-dems.md)).

**Hillshade.** With solar azimuth $\phi_s$ and altitude $\alpha_s$, the Lambertian intensity is $I = \cos\theta_z\cos s + \sin\theta_z\sin s\cos(\phi_s - \text{aspect})$ with zenith angle $\theta_z = 90° - \alpha_s$, clipped to $[0,1]$ and scaled to 0–255. A vertical exaggeration $Z$ multiplies $z_x, z_y$ before computing $s$.

**Openness / SVF.** Positive openness $= \frac{1}{8}\sum_{\text{8 azimuths}} (90° - \max\text{ elevation angle within radius } L)$; sky-view factor $\approx \frac{1}{n}\sum_{i=1}^n \left(1 - \sin\gamma_i\right)$ with $\gamma_i$ the horizon elevation angle in direction $i$.

**Flow routing.** D8 assigns all flow to the steepest of 8 neighbours (slope $= \Delta z/\Delta$ for cardinals, $\Delta z/(\sqrt2\Delta)$ for diagonals); D∞ (Tarboton) splits flow between the two facets adjacent to the steepest triangular facet direction. **Priority-flood** (Barnes et al. 2014) fills depressions in $O(n\log n)$ by processing cells from the edges inward with a priority queue. **TWI** $= \ln\frac{a}{\tan\beta}$ with specific catchment area $a$ and slope $\beta$ ([Chapter 61](../chapters/ch61-hydrology.md)).

> **Worked example (B.13b).** A 1 m DEM is misregistered by a half cell (pixel-is-point treated as pixel-is-area). On a uniform 10 % slope the height error is $0.5 \times 0.10 = 5$ cm everywhere — invisible in a DoD of two products with the same error, but a 5 cm bias against checkpoints. On a 30° slope, $0.5\tan 30° = 29$ cm. Slope itself is unaffected on a plane, but at a ridge line of 1 m width the computed slope on the far side flips sign across the half cell, producing a one-cell-wide artefact in curvature and hillshade ([Chapter 10](../chapters/ch10-projections-and-resampling.md)).

## B.8 Sampling and resolution

**Nyquist–Shannon** ⟨H⟩: a band-limited surface with no power above spatial frequency $f_c$ is exactly recoverable from samples at spacing $\Delta \le 1/(2f_c)$; equivalently, the shortest representable wavelength is $2\Delta$ and the smallest resolvable feature is in practice 3–5 cells wide. **Aliasing:** power above the Nyquist frequency $f_N = 1/(2\Delta)$ folds to $|f - 2kf_N|$, appearing as spurious low-frequency structure (moiré from regular canopy, striping from flight-line spacing).

**MTF of a footprint.** A circular footprint of diameter $D$ acts as a low-pass filter with MTF $= 2J_1(\pi D f)/(\pi D f)$ (Airy), first zero at $f = 1.22/D$; a square cell of side $\Delta$ has $\mathrm{MTF} = |\mathrm{sinc}(\Delta f)|$. Successive stages multiply: footprint × sampling × interpolation × resampling.

**Effective resolution from spectra.** Compute the radially averaged power spectrum $P(f)$ of the DEM; terrain typically follows $P \propto f^{-\beta}$ with $\beta \approx 2$–3. The frequency at which $P(f)$ departs from the power law (flattens to a noise floor or rolls off from smoothing) marks the effective resolution $r_{\mathrm{eff}} = 1/(2 f_{\mathrm{break}})$; alternatively, difference against a finer reference and find the smallest feature size with > 50 % amplitude recovery ([Chapter 44](../chapters/ch44-resolution-and-sampling.md)).

**Quantization noise.** Rounding to step $q$ adds uniform error with $\sigma_q = q/\sqrt{12}$: 1 m integers → 0.29 m; 0.1 m (Terrain-RGB) → 2.9 cm; 1 cm → 0.29 cm.

**Float precision.** IEEE float32 has 24 significant bits (≈ 7.2 decimal digits); the spacing between representable values near magnitude $x$ is $\mathrm{ulp}(x) = 2^{\lfloor\log_2 x\rfloor - 23}$.

> **Worked example (B.13a).** A UTM northing of 4,500,000 m stored as float32: $2^{22} = 4{,}194{,}304 \le x < 2^{23}$, so $\mathrm{ulp} = 2^{22-23} = 0.5$ m. Coordinates are quantized to half a metre and rounding adds $\sigma = 0.5/\sqrt{12} = 14$ cm. Heights near 4,000 m have ulp $= 2^{11-23} = 2.4\times10^{-4}$ m, which is fine. Store coordinates as float64 or as scaled integers (LAS); store heights as float32 only if $|z| \lesssim 10^4$ ([Chapter 47](../chapters/ch47-file-formats.md)).

## B.9 Change

**DoD and LoD.** $\Delta z = z_2 - z_1$; with independent per-cell uncertainties, $\sigma_{\Delta} = \sqrt{\sigma_1^2 + \sigma_2^2}$ and the level of detection at 95 % is $\mathrm{LoD}_{95} = 1.96\,\sigma_\Delta$; cells with $|\Delta z| < \mathrm{LoD}_{95}$ are not significant. Area-averaged change over $n_{\mathrm{eff}}$ independent cells has $\mathrm{LoD}_{95} = 1.96\,\sigma_\Delta/\sqrt{n_{\mathrm{eff}}}$ (B.2) ([Chapter 41](../chapters/ch41-change-detection.md)).

**Nuth & Kääb (2011) co-registration.** A horizontal shift $(\Delta x, \Delta y)$ between two DEMs produces elevation differences on slopes that vary with aspect $\psi$:

$$ \frac{\Delta z}{\tan(\text{slope})} = a\cos(b - \psi) + c, \qquad \Delta x = a\sin b,\ \Delta y = a\cos b,\ c = \frac{\overline{\Delta z}}{\overline{\tan(\text{slope})}}, $$

fitted on stable terrain and iterated until the shift is below a tolerance (typically < 0.5 cell). Follow with a vertical bias and, if needed, a tilt (first-order polynomial) correction.

**M3C2** (Lague et al. 2013). For each core point, estimate the local normal at scale $D$, project both clouds onto a cylinder of diameter $d$ along the normal, compute mean positions $\bar p_1, \bar p_2$ and standard deviations $\sigma_1, \sigma_2$ with $n_1, n_2$ points; distance $= (\bar p_2 - \bar p_1)\cdot\mathbf n$ and

$$ \mathrm{LoD}_{95} = 1.96\left(\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}} + \mathrm{reg}\right), $$

where $\mathrm{reg}$ is the registration uncertainty.

**ICP.** Iterate: match each point to its nearest neighbour (or point-to-plane), solve the rigid transform minimizing $\sum\|R\mathbf p_i + \mathbf t - \mathbf q_i\|^2$ (closed form via SVD of the cross-covariance), apply, repeat until convergence. Converges to a local minimum; needs a good initial alignment and stable-area masking.

**Okada (1985) dislocation (summary).** Surface displacement $\mathbf u(\mathbf x)$ from a rectangular fault of length $L$, width $W$, depth $d$, dip $\delta$, and slip $(U_1, U_2, U_3)$ in an elastic half-space is given by closed-form expressions in terms of the Chinnery notation $f(\xi,\eta)\| = f(x,p) - f(x,p-W) - f(x-L,p) + f(x-L,p-W)$; the vertical component for pure dip-slip scales as $U_2/(2\pi)$ times a geometric factor. Used to predict the coseismic height change a DEM epoch must absorb ([Chapter 39](../chapters/ch39-earthquakes-volcanoes-landslides.md)).

**Time-series regression with correlated noise.** For heights $z(t_i) = a + b\,t_i + \varepsilon_i$ with covariance $\Sigma_\varepsilon$ (white + flicker/power-law + seasonal), the generalized least-squares rate is $\hat b$ from $(A^{\mathsf T}\Sigma_\varepsilon^{-1}A)^{-1}A^{\mathsf T}\Sigma_\varepsilon^{-1}\mathbf z$ and its uncertainty is typically 2–5× the white-noise value; for GNSS vertical series a white + flicker model is standard (Hector, MIDAS).

> **Worked example.** Two lidar DTMs with NVA 10 cm each ($\sigma \approx 5.1$ cm) over a 1 ha landslide toe: per-cell $\mathrm{LoD}_{95} = 1.96\sqrt{2}\times0.051 = 0.14$ m. Mean change over the hectare with exponential correlation length $\ell = 15$ m: $n_{\mathrm{eff}} \approx 10^4/(2\pi\times225) \approx 7$, so $\mathrm{LoD}_{95,\mathrm{mean}} = 0.14/\sqrt{7} = 5.3$ cm — not the 0.14/√10,000 = 1.4 mm a naive count of 1 m cells would give.

## B.10 Catenary, under-keel clearance, tidal datums

**Catenary.** A conductor of weight per unit length $w$ under horizontal tension $T_H$ hangs as $y(x) = \frac{T_H}{w}\left(\cosh\frac{wx}{T_H} - 1\right)$; for span $S$ the mid-span sag is $D = \frac{T_H}{w}\left(\cosh\frac{wS}{2T_H} - 1\right) \approx \frac{wS^2}{8T_H}$ (parabolic approximation, valid when $D \ll S$). Conductor length $L \approx S + \frac{8D^2}{3S}$.

**Thermal sag.** Length change $\Delta L = \alpha L\,\Delta T$ (aluminium–steel conductors $\alpha \approx 1.9\times10^{-5}$/°C); from $L \approx S + 8D^2/(3S)$, $D_2 = \sqrt{D_1^2 + \tfrac{3}{8}S\,\Delta L}$ (ignoring the tension change, which reduces the effect somewhat — IEEE 738 and the ruling-span method give the full solution).

**Wind sway.** Blow-out angle $\theta = \arctan(F_w/w)$ with wind force per unit length $F_w = \tfrac12\rho_a v^2 C_d\, d_c$ for conductor diameter $d_c$; horizontal displacement at mid-span $\approx D\sin\theta$ ([Chapter 33](../chapters/ch33-wires-and-thin-structures.md)).

**Under-keel clearance.** $\mathrm{UKC} = (d_{\mathrm{chart}} + \eta_{\mathrm{tide}} + \eta_{\mathrm{surge}}) - (T_{\mathrm{static}} + \text{squat} + \text{heel/roll} + \text{wave response}) - \text{uncertainty allowance}$, with squat $\approx C_b\,\frac{v^2}{100}\,\frac{S_b}{1 - S_b}$-type empirical forms (Barrass) where $S_b$ is the blockage factor and $v$ in knots. The uncertainty allowance should be the combined 95 % uncertainty of the charted depth (CATZOC-dependent) and the water-level prediction ([Chapter 62](../chapters/ch62-navigation-and-charting.md)).

**Tidal datums.** From hourly water levels over a National Tidal Datum Epoch (US: 19 years, currently 1983–2001; a modified 5-year epoch is used where sea-level trends are large): MSL = mean of hourly heights; MLLW = mean of the lower low water of each tidal day; MHW, MHHW analogously. For short series, datums are transferred from a control station by the modified-range-ratio or tide-by-tide method: $\mathrm{MLLW}_{\mathrm{sub}} = \mathrm{MSL}_{\mathrm{sub}} - (\mathrm{MSL} - \mathrm{MLLW})_{\mathrm{ctl}}\cdot\frac{\mathrm{range}_{\mathrm{sub}}}{\mathrm{range}_{\mathrm{ctl}}}$ ([Chapter 9](../chapters/ch09-vertical-datums.md), [Chapter 66](../chapters/ch66-coastal-marine-polar-lakes-rivers.md)).

> **Worked example (B.13d).** A 300 m span with 8 m sag at 15 °C: $L_1 = 300 + 8\times64/900 = 300.569$ m. A 100 °C rise gives $\Delta L = 1.9\times10^{-5}\times300.569\times100 = 0.571$ m. $D_2 = \sqrt{64 + 0.375\times300\times0.571} = \sqrt{64 + 64.2} = 11.3$ m — about 3.3 m more sag, a lower bound on the clearance change (tension relief reduces it to perhaps 2.5–3 m). A lidar DTM-to-wire clearance measured on a cool morning overstates the hot-afternoon clearance by that amount.

## B.11 Indexing

**Morton (Z-order) curve** ⟨H⟩: interleave the bits of integer $(i, j)$ — $M = \sum_k \left(i_k 2^{2k} + j_k 2^{2k+1}\right)$ — so that nearby cells are usually nearby in the 1-D key; quadtree node addresses are Morton prefixes. **Hilbert curve** ⟨H⟩ preserves locality better (no large jumps) at the cost of a rotation-state machine per level.

**Quadtree / octree addressing** ⟨H⟩: a cell at level $L$ has key length $2L$ (quad) or $3L$ (oct) bits; the parent is the key shifted right by 2 (3); siblings share all but the last 2 (3) bits. COPC stores an octree of LAZ chunks keyed by (level, x, y, z).

**S2.** Project the sphere onto the six faces of a cube, apply a quadratic transform to equalize cell areas (ratio of largest to smallest ≈ 2.1), and index each face with a Hilbert curve; a 64-bit cell ID encodes face (3 bits), Hilbert position, and level (0–30). Level-$L$ cells have average area $\approx 85{,}011{,}000\ \mathrm{km^2}/4^L$ (one sixth of the Earth's surface) (level 10 ≈ 81 km², level 20 ≈ 77 m²).

**H3.** Aperture-7 hexagonal hierarchy on an icosahedron: each resolution $r$ cell has $\approx 7$ children; average hexagon area $A_r = A_0/7^r$ with $A_0 \approx 4.36\times10^6$ km², so $A_9 \approx 0.105$ km² and $A_{15} \approx 0.9$ m²; 12 pentagons per resolution; children are not exactly nested (≈ 1/7 area mismatch at boundaries).

**Web Mercator area distortion.** Scale factor $k = \sec\varphi$ (isotropic), area factor $k^2 = \sec^2\varphi$: 1.0 at the equator, 2.0 at 45°, 4.0 at 60°, 14.9 at 75°. A "1 m" zoom-level tile size at the equator is 0.5 m at 60° — relevant when a DEM is served through XYZ tiles ([Chapter 60](../chapters/ch60-dggs-and-location-codes.md)).

> **Worked example.** Cell $(i, j) = (5, 3) = (101_2, 011_2)$: $i$-bits occupy even positions and $j$-bits odd positions, so with $i_0=1, j_0=1, i_1=0, j_1=1, i_2=1, j_2=0$ the key bits (LSB first) are $1,1,0,1,1,0$ and $M = 1 + 2 + 8 + 16 = 27$. Its parent at the next coarser level is $27 \gg 2 = 6$, i.e. cell $(2, 1)$.

## B.12 ML evaluation

**Confusion-matrix metrics** for class $c$ with true positives TP, false positives FP, false negatives FN, true negatives TN: precision $= \mathrm{TP}/(\mathrm{TP}+\mathrm{FP})$, recall $= \mathrm{TP}/(\mathrm{TP}+\mathrm{FN})$, $F_1 = 2PR/(P+R)$, IoU $= \mathrm{TP}/(\mathrm{TP}+\mathrm{FP}+\mathrm{FN})$, overall accuracy $= \sum_c \mathrm{TP}_c/n$. **Cohen's κ** $= (p_o - p_e)/(1 - p_e)$ with observed agreement $p_o$ and chance agreement $p_e = \sum_c p_{c\cdot}p_{\cdot c}$. Report per-class metrics; overall accuracy is dominated by the majority class (ground).

**Spatial cross-validation.** Random point-wise splits leak spatially autocorrelated information; use spatial blocks (tiles, regions) or buffered leave-one-out with buffer ≥ the correlation length, and report the gap between random and spatial CV as a measure of over-optimism.

**Proper scoring rules** for probabilistic predictions: Brier score $\frac{1}{n}\sum(p_i - o_i)^2$; log score $-\frac{1}{n}\sum\ln p_i(o_i)$; for continuous predictions, the **CRPS** $= \int (F(x) - \mathbb 1[x \ge y])^2\,\mathrm{d}x$, which reduces to MAE for a point forecast and rewards sharpness subject to calibration (Gneiting & Raftery 2007).

**Calibration curves (reliability diagrams).** Bin predictions by stated probability or interval; plot observed frequency against stated. For regression intervals, the **PIT** $u_i = F_i(y_i)$ should be uniform; the coverage of a stated 95 % interval should be 0.95 ± $1.96\sqrt{0.95\times0.05/n}$.

**Conformal intervals.** With calibration residuals $r_i = |y_i - \hat y_i|$ (or scaled $r_i/\hat\sigma_i$), take $\hat q$ as the $\lceil (n+1)(1-\alpha)\rceil/n$ empirical quantile; the interval $\hat y \pm \hat q\,(\hat\sigma)$ has marginal coverage $\ge 1-\alpha$ on exchangeable data — but *not* under distribution shift to a new region, which is the usual case for global DEM products ([Chapter 43](../chapters/ch43-traditional-vs-ml.md)).

> **Worked example.** A ground classifier reports 98.5 % overall accuracy on a tile that is 94 % ground. Per class: ground recall 0.995, non-ground recall 0.83; non-ground IoU 0.78. κ: $p_o = 0.985$, $p_e = 0.94\times0.945 + 0.06\times0.055 = 0.892$, $\kappa = (0.985 - 0.892)/(1 - 0.892) = 0.86$. The 17 % of non-ground returns labelled ground are low vegetation — the headline accuracy hides a +10–30 cm DTM bias in shrubland.

## B.13 Numeric worked examples (index)

The six examples required by the chapter plan are embedded above; this table locates them and restates the results.

| Example | Section | Result |
|---|---|---|
| (a) float32 northing precision | B.8 | ulp = 0.5 m at 4.5 × 10⁶ m; σ_q = 14 cm; use float64 or scaled integers |
| (b) half-cell shift effect | B.7 | 5 cm bias on 10 % slope, 29 cm on 30°; one-cell curvature/hillshade artefacts at ridges |
| (c) sound-speed error → depth at 60° | B.6 | 10 m/s surface error → ≈ 1.0 m (2 %) at 50 m depth vs 0.33 m at nadir; exceeds Order 1a TVU |
| (d) 100 °C conductor temperature rise | B.10 | 300 m span, 8 m sag → ≈ 11.3 m (upper bound; ≈ 2.5–3 m with tension relief) |
| (e) RMSE from 30 checkpoints, 95 % CI | B.1 | RMSE 9.2 cm → σ ∈ [7.3, 12.4] cm; NVA 18 cm ∈ [14, 24] cm |
| (f) volume ± uncertainty, ℓ = 20 m | B.2 | 1 ha at σ = 5 cm: ±2.5 m³ uncorrelated vs ±251 m³ correlated; n_eff ≈ 4 |

**Further reading.** Snyder (1987) for projections; Torge & Müller (2012) for geodesy; Hofmann-Wellenhof et al. (2008) for GNSS; Groves (2013) for INS; Hanssen (2001) for InSAR; Lurton (2010) for sonar; Hengl & Reuter (2009) for terrain analysis; Wackernagel (2003) for geostatistics; Gneiting & Raftery (2007) and Angelopoulos & Bates (2023) for probabilistic evaluation. Full citations appear in the chapters referenced.

# Shared Template 0.3 — Pre-Survey *A Priori* vs. Post-Survey *A Posteriori* Error Budget

> **Purpose:** Enforce quantitative continuity between **pre-survey prediction** (worst-case analytical TPU / RSS budget) and **post-survey validation** (independent stratified checkpoints, $\chi^2$ confidence intervals, robust estimators, variogram correlation lengths, and anomaly root-cause reconciliation). Grounded in [Chapter 53](../../fable/chapters/ch53-accuracy-assessment.md), [Chapter 70](../../fable/chapters/ch70-specifications-guided-tour.md), [Chapter 52](../../fable/chapters/ch52-ground-truth.md), and [Gemini4 Ch. 14](../../gemini4/book/ch-14/sec-14-02.md).

---

## 1. Governing Statistical & Reporting Rules

| Standard & Edition | Primary Metric & Test Logic | Checkpoint / Sample Rules | Mandatory Disclosure Rules |
|---|---|---|---|
| **ASPRS *PAS* Ed. 2 (2023; v2 2024; Addenda I–VI)** & **USGS LBS 2024/2025 rev. A** | Classed by $\text{RMSE}_V$ (NVA pass/fail without $1.96\times$; VVA tested & reported *as found*, no pass/fail) and $\text{RMSE}_H$; 3D $\text{RMSE}_{3D} = \sqrt{\text{RMSE}_x^2+\text{RMSE}_y^2+\text{RMSE}_z^2}$. | $\ge 30$ independent withheld checkpoints (scaling to $120$); **compliance reporting adds checkpoint error in quadrature**: $\text{RMSE}_{\text{rep}} = \sqrt{\text{RMSE}_{\text{test}}^2 + \sigma_{\text{cp}}^2}$ (whereas inferring *true underlying product error* subtracts $\widehat{\sigma}_{\text{prod}} = \sqrt{\sigma_{\text{obs}}^2 - \sigma_{\text{cp}}^2}$). | Quote exact ASPRS Ed. 2 statement (*"Tested to meet..."* vs. *"Produced to meet"*); report NVA/VVA separately; note if $n < 30$. |
| **Legacy ASPRS Ed. 1 (2014) / NSSDA (1998)** | $\text{NVA}_{95\%} = 1.9600\,\text{RMSE}_z$; $\text{VVA} = P_{95}(\|\varepsilon\|) \le 3\times\text{RMSE}_z$ class limit. | $\ge 20$ NVA + $\ge 5$ VVA ($\le 500\text{ km}^2$); $\sigma_{\text{cp}} \le \frac{1}{3}\sigma_{\text{product}}$. | Verify normality before applying $1.96$; report empirical $P_{95}$ whenever heavy-tailed. |
| **IHO S-44 Ed. 6.2.0 (Oct 2024)** | Sounding-level TPU at $95\%$ confidence: $\text{TVU}_{\max}(d) = \sqrt{a^2 + (b\,d)^2}$; $\text{THU}_{\max}(d) = c + e\,d$. | Exclusive ($a=0.15\text{ m}, b=0.0075$), Special ($0.25, 0.0075$), Order 1a/1b ($0.50, 0.013$), Order 2 ($1.00, 0.023$). | Maintenance update retaining Ed. 6.1.0 Table 1 TVU/THU $a/b$ parameters while adding §3.8 seabed characteristics and *a priori*/*a posteriori* glossary clarifications (`fable/` cites Ed. 6.1.0 baseline). TPU is a *model*, not empirical truth; crosslines and reference surfaces must empirically validate it. |
| **ICAO Annex 15 / PANS-AIM Doc 10066** | $90\%$ confidence level: Area 1 ($30\text{ m}$ V / $50\text{ m}$ H), Area 2 ($3/5\text{ m}$), Area 3 ($0.5/0.5\text{ m}$), Area 4 ($1/2.5\text{ m}$). | Process integrity via RTCA DO-200B (`10^-3` Area 1 routine / `10^-5` Areas 2–4 essential terrain; `10^-8` critical obstacle/runway data). | Explicit conversion for Gaussian zero-bias: $\text{LE90} = 1.6449\,\sigma_z$, $\text{LE95}/\text{LE90} = 1.1916$. |

**Gaussian Conversion Reference (Valid Only When Normal & Zero-Bias; Test with Histogram / Shapiro–Wilk):**
$$\text{LE95} = 1.9600\,\sigma_z, \qquad \text{LE90} = 1.6449\,\sigma_z, \qquad \text{CE95} = 1.7308\,\text{RMSE}_r = 2.4477\,\sigma_H, \qquad \text{CE90} = 1.5175\,\text{RMSE}_r = 2.1460\,\sigma_H$$

---

## 2. *A Priori* Worst-Case Quadrature (RSS / TPU) Budget

Evaluate ALL terms at the **worst-case operating envelope** (outer swath edge $\theta_{\max}$, deepest water $d_{\max}$ or highest $H_{\text{AGL}}$, longest GNSS baseline, steepest target slope $\alpha$, densest canopy). Under first-order covariance propagation $\boldsymbol{\Sigma}_{xyz} = \mathbf{J}\,\boldsymbol{\Sigma}_l\,\mathbf{J}^\top$:

- **Airborne / UAS Lidar:** $\sigma_z^2 = \sigma_{z,\text{GNSS/INS}}^2 + \sigma_{l_z}^2 + (\sigma_r\cos\theta_{\text{scan}})^2 + (H_{\text{AGL}}\tan\theta_{\text{scan}}\,\sigma_{\phi,\text{cross}})^2 + \sigma_{\text{bore/att}}^2 + \sigma_{\text{geoid}}^2 + (\sigma_H\tan\alpha)^2 + \sigma_{\text{class/interp}}^2$, where $\theta_{\text{scan}}$ is off-nadir scan angle, $\sigma_{\phi,\text{cross}}^2 = \sigma_\phi^2 + \sigma_{\delta\phi}^2 + \sigma_{\theta_{\text{scan}}}^2$ combines roll/boresight/encoder (pitch $\sigma_{\theta_{\text{pitch}}}$ drives along-track horizontal shift $H_{\text{AGL}}\sigma_{\theta_{\text{pitch}}}$ into slope), and **1D single-axis** $\sigma_H = \mathrm{RMSE}_r/\sqrt{2} = \mathrm{THU}_{95\%}/2.4477$ avoids the $2\times$ radial slope variance error ([Notation & Symbols](../../gemini4/book/00-front-matter/notation-and-symbols.md) §6.2).
- **Bathymetric Lidar:** Bottom **elevation $z_b$** incurs wave-surface sensitivity $\big((1 - \frac{n_a\cos\theta_w}{n_g\cos\theta_a})\,\delta z_s\big)^2 \approx \big((1 - 1/n_g)\delta z_s\big)^2 \approx (0.27\,\delta z_s)^2$ ($\approx 0.25\,\delta z_s$ at Palmer $\theta_a = 20^\circ$), whereas **instantaneous-surface depth** $d = z_s - z_b$ incurs $\frac{n_a\cos\theta_w}{n_g\cos\theta_a}\delta z_s \approx (1/n_g)\delta z_s \approx 0.73\,\delta z_s$ ($\approx 0.75\,\delta z_s$ at $20^\circ$; [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md)); separate the **systematic $+1.6\text{–}1.8\%$ seawater depth bias** ($n_p \approx 1.341$ vs. $n_g \approx 1.364$ at $532\text{ nm}$; $+0.5\text{–}0.6\%$ shallow bias if seawater $n_g$ is applied in freshwater) from random index TPU $(\frac{\sigma_n}{n_g}d)^2 \approx (0.0015\,d)^2$, pulse stretching $(b_{\text{det}} d)^2$, wave-slope horizontal shift $d(1-1/n_p)\delta\alpha_{\text{wave}}$, and footprint slope $(D\tan\alpha/2)^2$.
- **Sonar / AUV / USV:** Hare–Godin–Mayer TVU: separate **surface SVS beam-steering** $(-d\tan^2\theta\,\frac{\delta c_0}{c_0})^2$ from **column harmonic-mean SVP** $\big(d(1-\tan^2\theta)\frac{\delta c_p}{c}\big)^2$ (non-zero at $\theta=0$), roll $(d\tan\theta\,\delta\phi)^2$, heave, dynamic draft/squat, and water level/SEP. For **AUVs**, acoustic roll, refraction, and swath footprint scale with **altitude $h_{\text{alt}}$ ($5\text{–}70\text{ m}$)** rather than depth $d$, vertical reference uses **TEOS-10 pressure integration** $+ P_{\text{atm}}(t) + \eta(t)$, and DVL–INS drift ($0.05\text{–}0.2\%$ distance) + USBL ($0.05\text{–}0.3\%$ slant range) are **THU** terms coupling into TVU via $\tan\alpha\,\sigma_H$.
- **Optical Stereo / SfM:** $\sigma_z = \frac{H}{B}\,\text{GSD}\,\sigma_{p,\text{px}}$ combined in quadrature with trajectory/GCP, self-calibration doming, and rolling-shutter skew.
- **InSAR:** $\sigma_z = \frac{h_{\text{amb}}}{2\pi}\sigma_\phi(\gamma, N_L)$ with $h_a \equiv h_{\text{amb}} = \frac{\lambda R\sin\theta_i}{p\,B_\perp}$ ($p=1$ bistatic single-TX, $p=2$ repeat-pass/ping-pong; $\theta_i$ incidence angle) plus $k\,h_{\text{amb}}$ integer unwrapping blunders, atmospheric phase screen (APS), and canopy/firn penetration bias.
- **Slope-Coupled Total Vertical Uncertainty:** $\text{TVU}_{95\%,\text{eff}} = \sqrt{\text{TVU}_{95\%,0}^2 + \big(\frac{1.9600}{2.4477}\tan\alpha \cdot \text{THU}_{95\%}\big)^2}$ ([Sec. 13.3](../../gemini4/book/ch-13/sec-13-03.md)).

| Error Component | Worst-Case Operating Parameter | Budgeted $1\sigma_z$ (m) | Unmodeled Bias $b_z$ (m) | Variance Share ($\sigma_k^2 / \sigma_{\text{tot}}^2$) | Planning Lever / Mitigation |
|---|---|---|---|---|---|
| 1. Positioning / GNSS Trajectory (PPK/PPP/USBL) | Max baseline / depth / $K_p$ | `______` | `______` | `____ %` | Shorten baseline $\le 15\text{–}20\text{ km}$; second base |
| 2. Attitude $\times$ Standoff / Refraction ($\phi,\theta,\psi$, SVP) | $\theta_{\max} = \text{___}^\circ$, $H\text{ or }d = \text{___ m}$ | `______` | `______` | `____ %` | Clip outer swath; increase SVP cadence |
| 3. Range / Latency / Wave Surface / Timing | $\Delta t_{\text{sync}}$, sea state, $B/H$, $\gamma$ | `______` | `______` | `____ %` | 1PPS/PTP verify; figure-8; calm window |
| 4. Lever Arm & Boresight / Patch-Test Residual | Post-cal residual | `______` | `______` | `____ %` | Pre/post calibration over slope + flat |
| 5. Datum / Geoid / Tide / SEP Model ($\sigma_{\text{SEP}}$) | VDatum / gauge / geoid region | `______` | `______` | `____ %` | Site tide gauge or ERS + local tie |
| 6. Surface Definition / Ground Filter / Gridding | Slope $\alpha = \text{___}^\circ$, canopy/mud | `______` | `______` | `____ %` | Leaf-off window; higher ANPD; manual QC |
| 7. Checkpoint Survey Uncertainty ($\sigma_{\text{cp}}$) | ASPRS Ed. 2 quadrature inclusion | `______` | `0.000` | `____ %` | Project target $\sigma_{\text{cp}} \le \frac{1}{3}\sigma_{\text{spec}}$ (Ed. 2 permits relaxed ratios via quadrature) |
| **TOTAL *A Priori* RSS ($\sigma_{\text{total}}$)** | $\sigma_{\text{RSS}} = \sqrt{\sum \sigma_k^2}$ | **`______`** | **`______`** | **100 %** | **Conservative 95 % Bound:** $\|b\| + 1.96\,\sigma_{\text{RSS}} = \text{______ m}$ |
| **Governing Spec Limit & Pre-Mob Margin** | Spec limit: `______ m` | Margin: `______ m` (`____ %`) | Status: | `[ ] GREEN (<70%)` `[ ] YELLOW (70–90%)` `[ ] RED (>90%)` | **RED or $<10\%$ margin = NO-GO until re-planned.** |

---

## 3. *A Posteriori* Empirical Residuals & $\chi^2$ Confidence Intervals

Compute residuals as $\varepsilon_i = z_{\text{product},i} - z_{\text{reference},i}$ after verifying identical CRS, epoch, datum, and surface ontology (bilinear/TIN interpolation at checkpoints, never nearest-cell):

$$\bar\varepsilon = \frac{1}{n}\sum_{i=1}^n \varepsilon_i, \qquad \sigma = \sqrt{\frac{1}{n-1}\sum_{i=1}^n(\varepsilon_i - \bar\varepsilon)^2}, \qquad \mathrm{RMSE}_{\text{obs}} = \sqrt{\frac{1}{n}\sum_{i=1}^n \varepsilon_i^2}, \qquad \mathrm{NMAD} = 1.4826\cdot\mathrm{median}\big(|\varepsilon_i - \mathrm{median}(\varepsilon)|\big)$$

**$\chi^2$ 95 % Confidence Interval on True $\sigma$ / Zero-Mean RMSE** (valid for $n$ independent normal errors; use $\nu = n$ for zero-mean $\mathrm{RMSE}_{\text{obs}}$ and $\nu = n - 1$ for sample $\sigma$, e.g., $[0.796, 1.344]$ at $n=30$; one-sided compliance rejection checks $\chi^2_{n,0.95}$):
$$\mathrm{CI}_{95\%}(\mathrm{RMSE}) = \left[\widehat{\mathrm{RMSE}}\sqrt{\frac{n}{\chi^2_{n,\,0.975}}},\;\; \widehat{\mathrm{RMSE}}\sqrt{\frac{n}{\chi^2_{n,\,0.025}}}\right], \qquad \mathrm{RMSE}_{\text{Ed.2,bounds}} = \sqrt{\mathrm{RMSE}_{\text{obs}}^2 \cdot \frac{n}{\chi^2_{n,\text{crit}}} + \sigma_{\text{cp}}^2}$$

| Sample Size $n$ | $\chi^2_{n,\,0.025}$ | $\chi^2_{n,\,0.975}$ | Lower Multiplier | Upper Multiplier | Interpretation for Spec Acceptance |
|---|---|---|---|---|---|
| $n = 20$ | $9.59$ | $34.17$ | $0.765\times$ ($-23.5\%$) | $1.444\times$ ($+44.4\%$) | Underpowered; high false-fail / false-pass risk |
| $n = 30$ (ASPRS Ed. 2 min) | $16.79$ | $46.98$ | $0.799\times$ ($-20.1\%$) | $1.337\times$ ($+33.7\%$) | Sample RMSE $= 0.095\text{ m}$ spans $0.076\text{–}0.127\text{ m}$ |
| $n = 50$ | $32.36$ | $71.42$ | $0.837\times$ ($-16.3\%$) | $1.243\times$ ($+24.3\%$) | Minimum recommended for borderline strata |
| $n = 100$ | $74.22$ | $129.56$ | $0.879\times$ ($-12.1\%$) | $1.161\times$ ($+16.1\%$) | Tight $\chi^2$ bounds; spatial $N_{\text{eff}}$ check still required |

| Stratum / Test Group | $n$ | Mean Bias $\bar\varepsilon$ (m) | SD $\sigma$ (m) | $\mathrm{RMSE}_{\text{obs}}$ (m) | $\mathrm{RMSE}_{\text{Ed.2}}$ (m) | 95 % $\chi^2$ CI `[lo, hi]` (m) | NMAD (m) | Empirical $P_{95}(|\varepsilon|)$ (m) | $1.96\,\mathrm{RMSE}$ vs. $P_{95}$ Ratio | Pass / Report Status |
|---|---|---|---|---|---|---|---|---|---|---|
| NVA (Open / Hard Flat) | `__` | `_____` | `_____` | `_____` | `_____` | `[_____, _____]` | `_____` | `_____` | `____` | `[ ] PASS` `[ ] FAIL` |
| VVA (Vegetated / Canopy) | `__` | `_____` | `_____` | `_____` | `_____` | `[_____, _____]` | `_____` | `_____` | `____` | `Reported as found` |
| Steep Slope ($\alpha > 15^\circ$) | `__` | `_____` | `_____` | `_____` | `_____` | `[_____, _____]` | `_____` | `_____` | `____` | `[ ] PASS` `[ ] INFO` |
| Submerged / Crosslines / Junctions | `__` | `_____` | `_____` | `_____` | `—` | `[_____, _____]` | `_____` | `_____` | `____` | `[ ] PASS` `[ ] FAIL` |
| Horizontal Check ($\text{RMSE}_H$) | `__` | $\Delta E:\_\_,\Delta N:\_\_$ | `_____` | `_____` | `—` | `CE95: _____` | `—` | `_____` | `—` | `[ ] PASS` `[ ] FAIL` |

**Flagged Outliers (`|eps - median| > 3 * NMAD`):** Count: `____` · Excluded count (only documented blunders/change): `____` · Attach full CSV residual table (`id, x, y, z_ref, sigma_cp, z_dem, eps, stratum, disposition`).

---

## 4. Spatial Error Autocorrelation & Variogram Fields

DEM error is never spatially uncorrelated white noise ([Gemini4 Sec. 14.1](../../gemini4/book/ch-14/sec-14-01.md), [Sec. 14.5](../../gemini4/book/ch-14/sec-14-05.md), [Sec. 33.1](../../gemini4/book/ch-33/sec-33-01.md), [Chapter 53](../../fable/chapters/ch53-accuracy-assessment.md) §53.5). Estimate the empirical semivariogram $\gamma(h) = \frac{1}{2N(h)}\sum (e_i - e_j)^2$ on stable terrain overlaps (e.g., via `xdem`) before quoting areal mean or volumetric uncertainty:

| Variogram Component | Physical Origin | Fitted Model (`Spherical`/`Exponential`) | Partial Sill $c_k$ ($\text{m}^2$) | Correlation Length $a_k$ (m) | Volumetric Impact over Domain $A = \text{____ m}^2$ |
|---|---|---|---|---|---|
| **Nugget ($c_0$)** | Shot noise, phase noise, micro-roughness | `Uncorrelated` | `________` | $0\text{ m}$ | $\sigma_{\bar z,0}^2 = c_0 / M_{\text{cells}}$ |
| **Short-Range ($c_1, a_1$)** | Footprint, scan pattern, local interpolation | `____________` | `________` | `________ m` | Spherical range $a_1$: $N_{\text{eff},1} \approx \frac{5A}{\pi a_1^2}$ (Rolstad et al. 2009 Eq. 12; equiv. $\frac{A}{\pi L_c^2}$ at $L_c = a_1/\sqrt{5} \approx 0.45\,a_1$) |
| **Long-Range ($c_2, a_2$)** | Swath tilt, trajectory ramp, tidal/geoid drift | `____________` | `________` | `________ m` | $N_{\text{eff},2}$ dominates $\sigma_V = A\,\sigma_{\bar z,\text{total}}$ |
| **Effective Sample Summary** | Combined mean elevation error $\sigma_{\bar z} = \text{_____ m}$ | Effective $N_{\text{eff}} = \sigma_z^2 / \sigma_{\bar z}^2 = \text{_____}$ | **Volumetric $1\sigma_V$:** | **`_______ m³`** | Never report naive $\sigma_z / \sqrt{M_{\text{cells}}}$ for cut/fill or flood budgets. |

---

## 5. Field-Interpretable Triggers & Anomaly Reconciliation Matrix

Trigger immediate investigation whenever **actual $\mathrm{RMSE}$ or $|\bar\varepsilon|$ exceeds budgeted $1\sigma$ by $>25\%$**, **$P_{95} > 1.15 \times (1.96\,\mathrm{RMSE})$**, or a **sub-stratum fails**:

| Diagnostic Signature Observed | Suspect Root Cause | Confirmatory Check / Script | Required Corrective Disposition |
|---|---|---|---|
| Constant vertical offset across entire site | Datum/geoid/SEP mismatch, antenna height blunder, draft error | Check sea-level zero (`0 m`?) & base OPUS; compare $h$ vs. $H$ | Re-apply single verified transformation; audit raw antenna photos |
| Residual scales with $\tan\alpha \cos(b - \psi)$ | Horizontal shift, boresight pitch/yaw, epoch/tectonic offset | Run Nuth–Kääb 3D co-registration (`xdem` / `demcoreg`) | Solve horizontal shift + latency/boresight; re-run strip/bundle adj. |
| Cross-track parabola ("smile" / "frown") | Stale SVP vs. surface sound speed; wrong $n_p/n_g$ | Bin crossline–mainscheme residuals vs. beam/scan angle | Re-raytrace with updated casts; verify $n_g \approx 1.364$ vs. $n_p \approx 1.341$ |
| Radial concentric bowl / dome | SfM self-calibration coupling ($k_1, f$) on nadir-only grid | Compare interior vs. edge withheld checkpoints | Add $15^\circ\text{–}20^\circ$ oblique cross-lines or lock camera IO |
| Step between adjacent days / flights | Tide zoning jump, thermal IMU drift, base outage, GNSS spoof | Stratify $\bar\varepsilon$ and $\sigma$ by flight/dive/day and distance to base | Inspect $C/N_0$ & AGC logs; split lift calibration; re-run affected lines |
| Positive bias concentrated under canopy / marsh | Leaf-on attenuation, aggressive filter, soft-substrate sink | Compare NVA vs. VVA; inspect DSM–DTM ($n\text{DSM}$) & slopes | Tune ground filter per terrain; declare low-confidence polygon & bias |

# On-Land Drone (UAS) LiDAR + Imagery — Mission & Flight Planning

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `land-drone-lidar-imagery` | **Platform / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

---

## 1. Terrain-Following & `122 m` (`400 ft`) / `120 m` AGL Regulatory Trap Gates

- [ ] **[GATE]** **Replace Coarse SRTM/Copernicus Terrain-Following Grids & Buffer Barometric Drift:** Prohibit planning `100–120 m` AGL terrain-following flights solely on `30 m` SRTM/GLO-30 without local bare-earth DTM + canopy/obstacle verification. Two coupled mechanisms defeat barometric terrain followers:
  1. **Barometric ISA pressure drift:** By the hypsometric equation:
     $$\frac{\Delta z}{\Delta P} = -\frac{R_d\,T}{g\,P} = -8.32\text{ m/hPa} \quad \left(\text{at } 15\,^\circ\text{C}, 1013.25\text{ hPa}\right)$$
     A **synoptic pressure drop** ($\Delta P < 0$) causes raw baro altitude to read artificially *high*, driving an uncompensated baro-hold drone to **descend into terrain/canopy** (`-25 to -50 m` across `3–6 hPa`); conversely, a **pressure rise** ($\Delta P > 0$) drives the drone to **climb toward/above the `122 m` (`400 ft AGL` FAA `§ 107.51(b)`) / `120 m` (EASA Open) ceiling**. Re-zero home altitude on every battery swap and verify RTK/PPK ellipsoid-height telemetry.
  2. **Coarse `30 m` SRTM DSM canopy/ridge error:** SRTM encodes tall canopy (`+10–30 m` above bare ground) while smoothing sharp hogbacks and narrow valleys (`-15–30 m` low). Load local `3DEP 1 m` DTM where available, capping planned ceiling `<= 110–115 m` above bare earth (`<= 120 m` satisfies both FAA & EASA) and verifying `>= 25–30 m` clearance above maximum obstacle/canopy height.
  — *Evidence:* Flight-plan elevation profile verified over local DTM + obstacle layer & battery re-zero SOP. | *Ref:* [Ch. 16](../../fable/chapters/ch16-platforms.md), [Ch. 26](../../fable/chapters/ch26-survey-planning.md), [`gemini4` §7.3](../../gemini4/book/ch-07/sec-07-03.md).
- [ ] **[REC]** **3D Terrain-Profile & Obstacle-Buffer Check:** Inspect every terrain-following waypoint profile in 3D against local DTM + surveyed powerline/tower heights, ensuring `<= 120 m` AGL everywhere and `>= 30 m` horizontal standoff from wires, guy cables, and turbines. — *Evidence:* Screenshot/export of 3D terrain clearance profile signed by PIC & Verifier. | *Ref:* [Ch. 26](../../fable/chapters/ch26-survey-planning.md).
- [ ] **[COND]** **High-Relief Stepped-Altitude Block Splitting (`\Delta H / H >= 20–30 %`):** *Trigger:* Canyon, quarry, or bluff vertical relief exceeds `20–30 %` of planned flying height. Partition blocks into stair-stepped AGL terraces to hold GSD/ANPD within `±15 % (tolerance)` while maintaining legal ceiling clearance. — *Evidence:* Multi-block flight-plan KML showing stepped AGL altitudes. | *Ref:* [Ch. 26](../../fable/chapters/ch26-survey-planning.md).

---

## 2. Photogrammetric (SfM) Flight Grid & Radial Doming Mitigation

- [ ] **[GATE]** **SfM Overlap & Sun-Elevation Window:** Program forward overlap **`>= 80 %`** and side overlap **`>= 70 %`** over crisp bare ground (`>= 85 % / 80 %` over vegetation, steep slopes, or low-texture sand/soil). Schedule imagery only at **solar elevation `> 30°`** (`30–45°` along water margins or bright beaches to limit specular sun glint). — *Evidence:* Mission grid geometry summary & solar-ephemeris UTC window table. | *Ref:* [Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md), [Ch. 26](../../fable/chapters/ch26-survey-planning.md), [`gemini4` §13.1](../../gemini4/book/ch-13/sec-13-01.md).
- [ ] **[GATE]** **Oblique Cross-Grids (`10–20°`) for James & Robson Radial Doming Mitigation:** Prohibit nadir-only single-altitude grids for self-calibrating blocks. Nadir-only bundles couple focal length ($\delta f \leftrightarrow \delta H$) and radial distortion ($\delta k_1$), inducing parabolic vertical doming:
  $$\Delta z_{\text{dome}}(R_{\max}) \approx -\eta_{\text{net}}\,\frac{\delta k_1}{H}\,R_{\max}^2$$
  producing **`0.50–1.00 m` bow across a `1 × 1 km` block at `100 m` AGL despite `0.28 px` reprojection error**. Mandate **orthogonal cross-grid passes tilted `10–20°` (`15–25°` effective) off-nadir** (or perimeter convergent oblique rings + `\Delta H / H >= 20–30 %` multi-altitude pass where permitted), suppressing radial doming by **`15–40×`**. — *Evidence:* Mission plan showing dual-grid orthogonal lines + `10–20°` gimbal pitch settings. | *Ref:* [Ch. 22 §22.3.1](../../fable/chapters/ch22-photogrammetry-sfm.md), [`gemini4` §8.2.2](../../gemini4/book/ch-08/sec-08-02.md).
- [ ] **[REC]** **GSD, Exposure Speed & Shutter Blur Cap:** Select altitude $H_{\text{AGL}} = \text{GSD} \cdot f / p_{\text{pix}}$ for target `1–3 cm` GSD, lock manual ISO (`<= 400–800`), aperture (`f/4–f/5.6`), and shutter speed (`<= 1/1000–1/2000 s`) holding ground smear **`<= 0.5 GSD`**:
  $$v_g\,t_{\text{exp}} \le 0.5\,\text{GSD}$$
  (`10 m/s` at `1/1000 s` = `1.0 cm`; slow to `<= 5–8 m/s` for sub-cm GSD or overcast skies). — *Evidence:* Camera exposure matrix & blur-budget calculation (`cm` vs `GSD`). | *Ref:* [Ch. 16](../../fable/chapters/ch16-platforms.md).
- [ ] **[REC]** **Perimeter Convergent Oblique Ring & Cross-Line Placement:** On narrow linear corridors or irregular quarries where full orthogonal cross-grids are impractical, add perimeter convergent `10–20°` oblique rings (`>= 2` passes) tying edges cleanly to interior GCPs. — *Evidence:* Corridor mission file showing perimeter convergent passes. | *Ref:* [`gemini4` §8.2](../../gemini4/book/ch-08/sec-08-02.md).

---

## 3. UAS LiDAR Swath Geometry & Dynamic IMU Alignment

- [ ] **[GATE]** **LiDAR Sidelap (`30–50 %`), Scan FOV & Cross-Strips:** Space lines for **`30–50 %` sidelap** ($W = 2H_{\text{AGL}}\tan(\text{FOV}/2)$, $S = W(1 - f_{\text{side}})$; use `40–50 %` over forest canopy or `8–10 m/s` crosswinds), capping usable scan angle at **`<= 30–35°` off-nadir** to limit outer-beam canopy extinction and roll lever amplification ($\delta z = R\sin\theta\,\delta\theta_{\text{roll}}$). Include **`5–10 %` orthogonal cross-strips** (`>= 2` crosslines) for strip adjustment. — *Evidence:* Swath-spacing worksheet (`W, S, ANPD`) + cross-strip KML overlay. | *Ref:* [Ch. 18](../../fable/chapters/ch18-topographic-lidar.md), [Ch. 26](../../fable/chapters/ch26-survey-planning.md), [`gemini4` §13.1](../../gemini4/book/ch-13/sec-13-01.md).
- [ ] **[GATE]** **Pre/Post Figure-8 IMU Alignment & Hover-Between-Lines Prohibition:** Program **`60–120 s` static leveling**, pre-mission and post-mission **dynamic figure-8 maneuvers** (plus straight `2–3 m/s²` accel/decel legs), and **prohibit hovering between flight lines**. Hovering starves industrial/MEMS IMUs (`0.5–10 °/h`) of horizontal acceleration observability, allowing `0.1–0.3°` yaw drift (`15–40 cm` strip offsets). Execute banked turns (`15–20°`) beyond AOI margins with triggers paused/flagged. — *Evidence:* Mission script explicitly containing pre/post figure-8 waypoints & non-stop line transitions. | *Ref:* [Ch. 13](../../fable/chapters/ch13-imu-ins.md), [Ch. 18 §18.7](../../fable/chapters/ch18-topographic-lidar.md), [`gemini4` §7.3](../../gemini4/book/ch-07/sec-07-03.md).
- [ ] **[REC]** **GNSS DOP, Space Weather, Wind & VLOS Line Sequencing:** Plan flight UTC blocks with **`PDOP <= 2.5–3.0`** (`>= 10–12` SVs above `15°` mask), **`Kp < 5`**, and forecasted wind **`< 8–10 m/s`** (`gusts < 12 m/s`), flying upwind on final approaches and reserving `>= 25–30 %` landing SoC (`>= 20 %` hard RTH). — *Evidence:* GNSS almanac skyplot & wind/Kp window printout in flight binder. | *Ref:* [Ch. 12](../../fable/chapters/ch12-gnss.md), [Ch. 16](../../fable/chapters/ch16-platforms.md).
- [ ] **[REC]** **Battery-Swap Sortie Overlap & Mid-Block Stitching Buffer:** Place battery-swap breaks between consecutive sorties with **`>= 2` full overlapping flight lines** inside the AOI so trajectory breaks never land unbridged over bare control targets. — *Evidence:* Sortie boundary polygons confirming `>= 2`-strip overlap. | *Ref:* [Ch. 26](../../fable/chapters/ch26-survey-planning.md).
- [ ] **[COND]** **Multi-Modal White-Ribbon Tide & Solar Alignment Window:** *Trigger:* Survey ties intertidal beaches or riverbanks to concurrent ASV/bathylidar mapping. Lock UAS flight windows `within 1.5 hr` of predicted spring low water while holding solar elevation `30–45°` to ensure `100–500 m` wet-dry overlap. — *Evidence:* Co-timed marine/UAS window schedule. | *Ref:* [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md).

---

## 4. Worked *A Priori* UAS LiDAR & SfM Error Budgets (Gate Before Mobilization)

Populate [the shared error budget template](../_shared/template-error-budget.md) prior to Gate **G-04**. Note that **ASPRS PAS Ed. 2 (v2, 2024)** reports `1σ` `RMSE_V`/`RMSE_H`/`RMSE_3D` directly with checkpoint survey uncertainty ($\sigma_{\text{cp}}$) folded in quadrature; `95 %` metrics below are explicitly labeled **Legacy Ed. 1 / NSSDA (informational)**.

### Baseline Budget A — `80 m` AGL Survey-Grade MEMS UAS LiDAR ($\theta = 20^\circ$ Scan, $\alpha = 15^\circ$ Slope)

Reference derivation from [`gemini4` §7.3.4](../../gemini4/book/ch-07/sec-07-03.md), [`fable` Ch. 16](../../fable/chapters/ch16-platforms.md), and [`ch53`](../../fable/chapters/ch53-accuracy-assessment.md):

| Error Component (`1σ`) | Magnitude / Formula | Vertical (`1σ_z`) | Horizontal (`1σ_xy`) |
| :--- | :--- | :--- | :--- |
| PPK GNSS/INS Trajectory | `2.00 cm` H, `2.50 cm` V (`1σ`) | `2.50 cm` | `2.00 cm` |
| MEMS Roll/Pitch + Boresight (`0.015°`) | $H\tan(20^\circ)\sigma_{\phi,\theta}$; conservative passive bound $H\sec^2(20^\circ)\sigma_{\phi,\theta}$ (active LiDAR cross-track roll shift is $H\sigma_{\phi,\theta} = 2.09\text{ cm}$) | `0.76 cm` | `2.37 cm` |
| MEMS Yaw / Heading (`0.040°`) | $H\tan(20^\circ)\sigma_{\psi}$ | `0.00 cm` | `2.03 cm` |
| Laser Rangefinder ($\sigma_r = 1.50\text{ cm}$) | $\sigma_r\cos(20^\circ)$ | `1.41 cm` | `—` |
| Slope-Coupled Horizontal ($\alpha = 15^\circ$) | Worst-case $\tan(15^\circ)\,\mathrm{THU}$ (`THU = 3.71 cm` DRMS; `0.70 cm` if isotropic 1D $\mathrm{THU}/\sqrt{2} = 2.62\text{ cm}$) | `0.99 cm` | `—` |
| **Combined Model Bare-Earth RSS (`1σ`)** | Quadrature sum ($\sqrt{\sum \sigma_i^2}$) | **`TVU = 3.13 cm` (`1σ`)** | **`THU = 3.71 cm` (`1σ` DRMS)** |
| **ASPRS Ed. 2 Reported ($\sigma_{\text{cp}} = 2.1\text{ cm}$)** | $\text{RMSE}_{\text{rep}} = \sqrt{\text{TVU}^2 + \sigma_{\text{cp}}^2}$ | **`RMSE_V,rep = 3.77 cm`** | **`RMSE_H,rep` includes $\sigma_{\text{cp},H}$** |
| *Legacy Ed. 1 / NSSDA (Informational)* | `1.96 × TVU`; leaf-off canopy bias `+3–10 cm`; `CE95 = 1.7308 × DRMS = 2.4477 × sigma_1D` | *`95 % NVA = 6.1 cm` (bare); `8–15 cm` VVA* | *`CE95 = 6.4 cm`* |

### Baseline Budget B — `100 m` AGL Optical RTK/PPK SfM (`2.5 cm` GSD, `B/H = 0.5`, Oblique Cross-Grid)

Reference derivation from [`fable` Ch. 22 §22.8](../../fable/chapters/ch22-photogrammetry-sfm.md) and [`ch53`](../../fable/chapters/ch53-accuracy-assessment.md):

| Error Component (`1σ`) | Formula / Magnitude | Contribution (`cm`) | Mitigation Dependence |
| :--- | :--- | :--- | :--- |
| Image-Matching Parallax | $\sigma_Z = (H/B)\,\text{GSD}\,\sigma_p = 2.0 \times 2.5 \times 0.4$ | `2.00 cm` | Texture contrast; `<= 0.5 GSD` blur |
| RTK/PPK Camera Centers & GCP Control | `1.5–2.0 cm` V (`1σ`), `>= 5–8` distributed GCPs | `2.00 cm` | Base `<= 15 km`, OPUS tied |
| Residual Dome + Geoid + IO | `1.5–2.5 cm` (`1σ`) **only with `10–20°` obliques** | `2.50 cm` | Collapses to **`50–100 cm` fail** without obliques |
| **Combined Model `RMSE_V`** | Quadrature RSS ($\sqrt{2.0^2 + 2.0^2 + 2.5^2} = 3.77\text{ cm}$) | **`RMSE_V,model = 3.8 cm`** | DSM only; fails closed canopy |
| **ASPRS Ed. 2 Reported ($\sigma_{\text{cp}} = 2.1\text{ cm}$)** | $\sqrt{3.77^2 + 2.1^2}$; *Legacy `1.96×` Ed. 1 `LE95 = 7.4 cm`* | **`RMSE_V,rep = 4.32 cm`** | Tested against `>= 30` bare CPs |

- [ ] **[GATE]** **Site-Specific Error Budget Sign-Off & Flight Plan Freeze:** Populate site $H_{\text{AGL}}$, `B/H`, wind speed, sensor specs, and $\sigma_{\text{cp}}$ into [the error budget template](../_shared/template-error-budget.md), confirm `>= 25 %` margin below contract `RMSE_V`/`RMSE_H` targets, export verified mission KMLs, and record Gate **G-04** in [00-README-and-signoff.md](00-README-and-signoff.md). — *Evidence:* Completed site error-budget sheet + frozen mission `.kml`/`.mission` archive + G-04 dual sign-off. | *Ref:* [Error Budget](../_shared/template-error-budget.md), [Ch. 53](../../fable/chapters/ch53-accuracy-assessment.md).

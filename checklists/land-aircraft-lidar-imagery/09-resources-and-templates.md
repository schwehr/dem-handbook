# Land Aircraft LiDAR & Imagery — Resources, Critique & Operational Templates

This reference pairs an annotated critique of governing standards and processing software with an external regulatory/insurance register and copy-ready flight, geodetic base-station, and airworthiness/oxygen/boresight templates for `land-aircraft-lidar-imagery` campaigns. Return to [00-README-and-signoff.md](00-README-and-signoff.md) for the master sign-off sheet, or open shared governance templates: [template-project-header](../_shared/template-project-header.md), [template-error-budget](../_shared/template-error-budget.md), [template-cost-ledger](../_shared/template-cost-ledger.md), [template-insurance-coi](../_shared/template-insurance-coi.md), [template-accident-card](../_shared/template-accident-card.md), and [template-aar-retrospective](../_shared/template-aar-retrospective.md).

---

## 1. Critical Resource Inventory & Methodological Critique

### 1.1 Standards, Regulatory Guidance & Textbooks

| Resource | Authoritative Scope | Critical Strengths & Operational Pitfalls to Watch | Handbook Link |
| :--- | :--- | :--- | :--- |
| **USGS 3DEP Lidar Base Specification (`LBS 2024 / 2025 rev. A`)** | Federal US standard for `QL0–QL3` airborne LiDAR density, `RMSD_z`, `LAS 1.4` (`Class 20/21`), and hydro-flattening | **Strength:** Strict open-terrain spatial-distribution (`2×ANPS` cells), inter-swath `RMSD_z`, and standardized class codes. **Pitfall:** Passing open-terrain `ANPD` and flat `RMSE_V` does *not* guarantee bare-earth resolution under dense leaf-on canopy or steep canyon walls; always pair with $\mathrm{ANPS}_{\text{ground}}$ and under-canopy `VVA` reporting. | [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md), [ch-24/sec-24-01](../../gemini4/book/ch-24/sec-24-01.md) |
| **ASPRS Positional Accuracy Standards Ed. 2, v2 (June 2024)** | Horizontal, vertical & 3D (`RMSE_V`, `RMSE_H`, `RMSE_3D`) accuracy testing, `≥ 30`–`120` checkpoints, and quadrature error folding | **Strength:** Replaces legacy fixed-contour / `95 %` NSSDA pass-fail confusion with unified `RMSE` classes, **adds checkpoint uncertainty in quadrature**, and drops rigid pass/fail thresholds on vegetated terrain (`VVA` reported as observed). **Pitfall:** Small `n = 30` checkpoint sets yield wide `χ²` `95 %` confidence bands (`[0.80, 1.34] × RMSE`); clustered checkpoints further shrink `N_eff`. Always design `a priori` `σ_Z <= 0.75 ×` spec. | [ch53-accuracy-assessment](../../fable/chapters/ch53-accuracy-assessment.md), [ch70-specifications-guided-tour](../../fable/chapters/ch70-specifications-guided-tour.md) |
| **FEMA Elevation Guidance (Nov 2022) / *Guidelines & Standards* & USACE `EM 1110-1-1000` (2015)** | Flood-hazard elevation accuracy, hydraulic breaklines, and federal civil-works topographic mapping | **Strength:** Enforces hydraulic continuity (culvert flow paths vs. Class 17 bridge decks). **Pitfall:** Automated ground filters routinely bridge narrow streams or erase levee crests; mandate manual breakline/hydro QC before delivery. | [ch32-dsm-to-dtm](../../fable/chapters/ch32-dsm-to-dtm.md), [ch70-specifications-guided-tour](../../fable/chapters/ch70-specifications-guided-tour.md) |
| **ICAO Annex 15 / Doc 10066 eTOD & `RTCA DO-200B` / `ED-76A`** | Airport/obstacle terrain Areas 1–4 (`90 %` confidence) and aeronautical terrain integrity (`10⁻³`–`10⁻⁵`) | **Strength:** Explicit numerical integrity lineage across every software handoff (`DO-200B`). **Pitfall:** Aeronautical products often require `EGM96`/`EGM2008` orthometric heights while avionics display `WGS 84 (G2296)` ellipsoidal heights (`ch62`) — mixing them creates tens of meters of vertical blunder. | [ch62-navigation-and-charting](../../fable/chapters/ch62-navigation-and-charting.md) |
| **ASPRS *Manual of Airborne Topographic LiDAR* & *Manual of Photogrammetry*** | Sensor physics, strip adjustment (`Skáloud–Lichti`), and digital metric camera calibration | **Strength:** Authoritative physical/mathematical treatment of scan geometry and boresight coupling. **Pitfall:** Classical derivations often treat optical windows as zero-thickness flat planes; explicitly apply pressurized meniscus/Snell corrections (`ch-07/sec-07-03`). | [ch22-photogrammetry-sfm](../../fable/chapters/ch22-photogrammetry-sfm.md), [ch25-calibration-infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md) |

### 1.2 Processing, Trajectory & QA Software Tools

| Software / Library | Primary Role | Honest Technical Assessment & Common Trap | Handbook Link |
| :--- | :--- | :--- | :--- |
| **`Applanix POSPac MMS` / `NovAtel Inertial Explorer`** | Tightly coupled `PPK/RTS` GNSS+IMU `SBET` & `SMRMSG` covariance | **Assessment:** Industry-standard dual-pass Kalman smoothers with `IGS`/`ANTEX` support. **Trap:** Default base-station single-point `RINEX` positions or mismatched radome codes bias entire sorties silently; `SMRMSG` covariance can be overly optimistic during GNSS spoofing unless raw `AGC`/`C/N0` is audited. | [ch12-gnss](../../fable/chapters/ch12-gnss.md), [ch13-imu-ins](../../fable/chapters/ch13-imu-ins.md) |
| **`TerraScan` / `TerraMatch` / `OPALS` / `BayesStripAlign`** | Rigorous Skáloud–Lichti boresight, strip adjustment, and manual/macro classification | **Assessment:** Proven strip-adjustment engines capable of solving static boresight and dynamic mirror/trajectory residuals. **Trap:** Unconstrained time-varying trajectory correction in `TerraMatch` without flat/sloped constraints can "adjust" true gentle terrain slopes into adjacent swaths; always check against independent CPs. | [ch25-calibration-infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md), [ch30-point-cloud-classification](../../fable/chapters/ch30-point-cloud-classification.md) |
| **`RiPROCESS` / `Leica HxMap` / `Vexcel UltraMap`** | Vendor raw waveform/MTA decoding, `SPL` noise pruning, and large-format frame SGM/ortho | **Assessment:** Essential for proprietary pulse-coding (`MTA`), `SPL` solar pruning, and sub-pixel camera radiometry. **Trap:** `SPL` aggressive solar-noise filters can strip sparse canopy or dark asphalt roads if thresholded too tight; inspect raw intensity before purging noise classes. | [ch-09/sec-09-01](../../gemini4/book/ch-09/sec-09-01.md), [ch-09/sec-09-06](../../gemini4/book/ch-09/sec-09-06.md), [ch-08/sec-08-01](../../gemini4/book/ch-08/sec-08-01.md) |
| **`PDAL` / `laspy` / `lidR` / `GDAL` / `xdem`** | Open-source reproducible QC pipelines, `COG`/`COPC` generation, `Nuth–Kääb`, `FFT` forensics | **Assessment:** Deterministic, scriptable, zero license lock-in for field QA and independent audits (`Nuth–Kääb` co-registration and `2D FFT`). **Trap:** Older `GDAL`/`PDAL` builds or custom `rasterio` scripts can silently drop `AREA_OR_POINT=Area` or write `RasterPixelIsPoint`, shifting steep slopes by half a cell; always assert tag presence post-write. | [ch31-interpolation-and-gridding](../../fable/chapters/ch31-interpolation-and-gridding.md), [ch-15/sec-15-03](../../gemini4/book/ch-15/sec-15-03.md), [ch-14/sec-14-05](../../gemini4/book/ch-14/sec-14-05.md) |
| **`PLS-CADD`** | Helicopter utility corridor catenary modeling & `IEEE Std 738` thermal wire sag | **Assessment:** Standard for transmission-line clearance, blow-out, and vegetation encroachment. **Trap:** Wire elevation without concurrent SCADA ampacity and ambient wind/temp is snapshot geometry only — never extrapolate max-sag clearances without logged weather/load inputs. | [ch33-wires-and-thin-structures](../../fable/chapters/ch33-wires-and-thin-structures.md), [ch56-case-files](../../fable/chapters/ch56-case-files.md) |

### 1.3 External Statutory, Safety, Hazmat & Insurance Register

*Note: Federal aviation, workplace-safety, hazmat, laser, privacy/export, and commercial-insurance mandates listed below are external regulatory authorities outside `fable/` and `gemini4/`; verify active statutory text prior to launch.*

| Authority & Citation / Standard | Edition / As-Of | Governing Scope for Airborne Surveys | Verified Operational Trigger / Threshold |
| :--- | :--- | :--- | :--- |
| **FAA `14 CFR § 91.211`** | Current eCFR (as of 2026) | Supplemental oxygen requirements (cabin pressure altitude basis) | Crew O₂ `> 30 min` above `3,810 m` (`12,500 ft MSL`), continuous crew `> 4,267 m` (`14,000 ft MSL`), all occupants `> 4,572 m` (`15,000 ft MSL`) |
| **FAA `14 CFR §§ 91.119, 91.137, 91.509, 99.7, 119.1(e)(4)(iii), Part 375`** | Current eCFR (as of 2026) | Minimum safe altitudes, TFRs (wildfire/stadium), turbine over-water floor, aerial-survey Part 135 exemption, foreign-aircraft permits | Congested `305 m` (`1,000 ft`) / `610 m` (`2,000 ft`); `91.509` floor adopted beyond `§ 91.205(b)(12)`; `§ 119.1(e)(4)(iii)` restricts flights to survey ops; `Part 375` before foreign-tail entry |
| **FAA `14 CFR Part 43` (`Form 337` / `STC`) & `AC 70-1B`** | `AC 70-1B` (14 Feb 2022) / Current eCFR | Airframe belly-port / helicopter hardpoint airworthiness and outdoor laser notification (`Form 7140-1` + DoD `LCH`) | Signed STC/Form 337 W&B prior to flight; `Form 7140-1` + LCH approval before energizing `532`/`1064 nm` lasers aloft |
| **NOAA `15 CFR Part 922` (National Marine Sanctuaries) & `FAA AC 91-36D` (Noise-Sensitive Overflights)** | Current eCFR / FAA Advisory Circular | **Mandatory** sanctuary minimum overflight zones (`15 CFR Part 922`) vs. **voluntary** quiet-flight advisory (`AC 91-36D`) over parks/refuges | Comply strictly with `15 CFR Part 922` regulatory overflight floors/permits in designated Marine Sanctuary zones; maintain `>= 610 m` (`2,000 ft`) AGL where feasible over parks/refuges (`AC 91-36D`), seasonal nesting buffers, & advance community notices |
| **ANSI `Z136.1` & `Z136.6`** | `Z136.1-2022` / `Z136.6-2015` | Laser eye/skin MPE, `NOHD`, and binocular `ENOHD` | Enforce project floor `>= 1.2 × NOHD` (`532 nm` SPL `~5×` tighter retinal MPE than `1,064 nm`) |
| **NTSB `49 CFR Part 830` (`§§ 830.2, 830.5, 830.10, 830.15`)** | Amended 2022 / Current eCFR | Civil aircraft accident reporting, recorder preservation, and `Form 6120.1/2` | **Immediate** verbal notice (`+1-844-373-9922`) for fatal/serious injury, substantial damage, collision, fire, or `> $25,000` non-aircraft property damage; **written `Form 6120.1/2` within `10 days`** |
| **OSHA `29 CFR § 1904.39`, USCG/NRC (`33 CFR § 153.203`, `46 CFR § 4.05-10`) & `MUTCD`** | Current eCFR / `MUTCD` 11th Ed. (2023) | Severe workplace injury, fuel/spill/ditching notification, and roadside crew PPE | OSHA `8 h` fatality / `24 h` hospitalization or eye loss; **NRC immediate (`+1-800-424-8802`)** / **USCG `CG-2692` `5 d`**; `ANSI/ISEA 107` Class 2/3 vests for ground GNSS/CP crews |
| **IATA DGR & DOT Hazmat (`49 CFR 171–180`, `UN 3480/3481`, `UN 3090/3091`)** | IATA DGR 67th Ed. (eff. Jan 1, 2026) | Air/ground lithium battery & primary-cell transport and fire containment | **`<= 30 % SoC`** air-freight mandatory for `UN 3480 PI 965 (CAO)` & `UN 3481 PI 966`; `UN 3090 CAO`; `UN 38.3` + `SDS`; Halon/water-AVD for Li-ion vs. `Class D` strictly for `UN 3090` |
| **Export (`ITAR 22 CFR 120–130` / `EAR 15 CFR 730–774`), Privacy & Culture (`GDPR`, `NHPA § 106`, `ARPA`, `CARE/OCAP®`)** | Current eCFR / `(EU) 2016/679` | Dual-use IMU/laser export (`7A003/7A005/6A005/6A008`), foreign permits, PII/tribal/heritage protection | Screening before cross-border transit or foreign-national crew access; `ATA Carnet`; **`GDPR Art. 33 <= 72 h`** personal/medical PII breach reporting; tribal/archaeological data masking |
| **Aviation, Payload, Auto, Workers' Comp, `E&O` & Cyber COIs** | Active Policy Year / `ISO CG 00 01` | Bridging standard CGL aviation exclusion, hull/liability/ocular risk, ground-crew auto, and telemetry/PII breaches | Aviation Hull + Third-Party Liability (w/ laser ocular check) + Non-Owned + Over-Water + `C&V` Payload Floater + Auto/WC/FVWC + `E&O` + **Cyber Liability / Data Breach** (`>= 60 d` buffer past planned completion) |

---

## 2. Copy-Ready Field & Flight Operational Templates

### Template A — Airborne Flight-Line & Sortie Log

```text
AIRBORNE SORTIE & FLIGHT-LINE LOG
Project / AOI: ______________________   Sortie ID: ______________   Date (UTC): ____-__-__
Aircraft Tail: __________  Platform: [ ] Unpressurized  [ ] Pressurized  [ ] Helicopter
PIC: ___________________  Sensor Op: ___________________  Engine Start/Stop (UTC): ____ / ____
Active Base IDs (<= 20 km): __________________  Local Kp / PDOP Max: ____ / ____
Sensor Config: PRF _____ kHz | Scan Freq _____ Hz | Half-FOV ____ deg | Port ΔP ____ kPa
Target AGL: ______ m (Backup Low-Ceiling Plan Used? [ ] Yes [ ] No) | MTA Zone: ____ (R_unamb = ____ m)

Line ID | Plan AGL (m) | Speed (m/s) | Start UTC | End UTC | Sky/Cloud/Smoke | Camera Exp/Sun>30° | QC Status (PASS/REFLY)
--------|--------------|-------------|-----------|---------|-----------------|--------------------|-----------------------
L-001   |              |             |           |         |                 |                    |
L-002   |              |             |           |         |                 |                    |
X-001   |              |             |           |         |                 |                    |

Same-Day Field QC Gate:
- Raw Offload SHA-256 Verified & 3-2-1 Replicated: [ ] Yes  Manifest ID: ______________
- PPK Fwd-Rev Max Sep: _____ m (<= 0.10 m) | 2xANPS Cells Populated: ___% (>= 90 %)
- Inter-Swath RMSD_z: _____ m (<= 0.08 m) | Low-Sun Corduroy Hillshade Check: [ ] Clean [ ] Refly Issued
```

### Template B — GNSS Base-Station Datasheet & Dual Antenna-Height Photo Log

```text
GNSS BASE-STATION DATASHEET & ANTENNA-HEIGHT PHOTO LOG
Project ID: _______________________   Base ID / Name: ______________   Date (UTC): ____-__-__
Operator: _________________________   Monument Type / Stability Class (A–D): ______________
Right-of-Entry / Permit Ref: ______________   Lat/Lon (approx): _________________________

Hardware & IGS ANTEX Identity (MUST match physical serial labels):
- Receiver Model & Serial: _____________________  Firmware: __________  Rate: ____ Hz (Elev Mask: __ deg)
- Antenna + Radome 20-Char IGS Code (igs20.atx): [____________________]  Serial: ______________

Dual Independent ARP Antenna-Height Verification (Measure TWICE in meters + Photograph):
- Measurement 1 (Meters, Slant / Vertical ARP [circle one]): ________ m  By: _________
- Measurement 2 (Meters, Independent Tape/Conversion):         ________ m  By: _________
- Mean True Vertical ARP above Monument Mark:                  ________ m  (Diff <= 0.002 m)
- Timestamped Collar / Tape Close-Up Photo Filename:           _________________________
- Horizon Obstruction Photo Filename (N/E/S/W):                _________________________

Session & OPUS / NGS 92 Tie Record:
- Logging Start (UTC): ____-__-__ __:__   End (UTC): ____-__-__ __:__  Total Duration: ____ h (>= 4 h)
- OPUS / Network Solution ID: _________________  CRS/Epoch: ______________  Vert RMS: _____ m (<= 0.015 m)
```

### Template C — Aircraft Weight & Balance, `14 CFR § 91.211` Oxygen & Boresight Tracking Log

```text
AIRCRAFT W&B, 14 CFR § 91.211 OXYGEN & BORESIGHT TRACKING LOG
Aircraft Tail: __________  STC / FAA Form 337 Doc ID: ___________________  Return-to-Service Date: ____-__-__
Optical Port Glass: Material ______  t_win ____ mm  n_win ______  AR Dual-Band Check: [ ] PASS  Cert: ________
IMU Body Frame: [ ] FRD (NED-aligned: +x fwd, +y stbd, +z down)  [ ] RFU (ENU-aligned: +x right, +y fwd, +z up)
Lever Arms (<= 0.010 m Total-Station Survey; state signed direction clearly):
- IMU -> GNSS ARP (dx, dy, dz m):       (________, ________, ________)  Survey Ref: __________________
- IMU -> Sensor Origin (dx, dy, dz m):  (________, ________, ________)

Sortie Weight & Balance Check:
- Empty Wt (kg): ______  Sensor + Rack (kg): ______  Crew + Gear (kg): ______  Takeoff Fuel (kg): ______
- Takeoff Total Mass (kg): ______ (Max MTOW: ______)  Takeoff CG: ______ (Limits: ____ to ____)
- Zero-Fuel / Landing CG: ______ (Limits: ____ to ____)  W&B Signed by PIC: __________________

14 CFR § 91.211 Supplemental Oxygen Check (Cabin Pressure Altitude Basis):
- Max Planned Geometric / Cabin Pressure Altitude: ______ m MSL (______ ft) / ______ m MSL (______ ft)
- Applicable Rule: [ ] <= 3,810 m (12,500 ft) [ ] > 3,810 m (>30 min crew O2) [ ] > 4,267 m (cont. crew) [ ] > 4,572 m (all occupants)
- Pre-Flight Cylinder Pressure: ______ kPa (______ psi)  Duration Margin >= Flight + 60 min: [ ] YES  Mask Leak Test: [ ] PASS

Pre-Project vs. Post-Project Boresight Closure Tracking (Gable-Roof + Flat Range, Rank 4):
- Pre-Survey Boresight (UTC ____-__-__): dRoll _____ deg | dPitch _____ deg | dYaw _____ deg | dT ____ ms
- Post-Survey Closure  (UTC ____-__-__): dRoll _____ deg | dPitch _____ deg | dYaw _____ deg | dT ____ ms
- Closure Delta (|Post - Pre|): dRoll _____ | dPitch _____ | dYaw _____  (Gate <= 0.003 deg: [ ] PASS [ ] FAIL)
```

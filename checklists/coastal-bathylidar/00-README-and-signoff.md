# Coastal Bathymetric & Topo-Bathy LiDAR — Overview & Master Sign-Off

This operational checklist binder governs **Airborne Laser Bathymetry (ALB)** and **coastal topo-bathymetric LiDAR** campaigns designed to bridge the nearshore land–water **"white ribbon"** from subaerial dunes, beaches, and marshes down through the shallow seabed ($d \approx 0.2\text{–}70\text{ m}$, water-clarity limited). Dual-wavelength systems pair a **532 nm green** (frequency-doubled Nd:YAG) pulse that penetrates the Jerlov coastal optical window ($a_w \approx 0.045\text{ m}^{-1}$) with a co-aligned **1,064 nm near-infrared (NIR)** pulse ($a_w \approx 36.3\text{ m}^{-1}$, absorbed within centimeters of the water surface) and, on hydrographic platforms, a **647 nm water Raman** backscatter receiver or cross-polarized green channel to lock onto the true air–water interface across both mirror-calm and wave-roughened seas.

> **Offline Field-Binder Rule:** This directory (`checklists/coastal-bathylidar/`) is self-contained for airport FBOs, survey aircraft, and coastal support boats operating without internet access. Print or cache the companion templates in [`../_shared/`](../_shared/template-project-header.md) alongside files `01`–`09` prior to mobilization.

---

## 1. Platform & Dual-Wavelength Sensor Envelope

Crewed fixed-wing aircraft (unpressurized Cessna 206/208 Caravan, Partenavia P.68, Twin Otter; pressurized King Air B200/350, Twin Commander 690) carry full-energy ALB suites ($60\text{–}150\text{ kg}$, $800\text{–}2{,}000\text{ W}$), while helicopters and heavy-lift UAS deploy compact topobathy green scanners over rivers, lagoons, and short coastal reaches.

| System (Manufacturer) | Wavelength Channels | Bathy PRF & Scan Geometry | Nominal Depth Envelope | Typical AGL & Footprint | Operational Role & Notes |
|---|---|---|---|---|---|
| **CZMIL SuperNova** (Teledyne Optech) | 532 nm (deep + 7-segment shallow), 1,064 nm NIR, RGB/HSI | 10 kHz (deep) / higher shallow segments; 20° circular Palmer | $\approx 3\,Z_{\text{SD}}$ (deep); $\approx 1.5\text{–}2\,Z_{\text{SD}}$ (shallow) | 400–600 m AGL; ~300 m swath; ~2 m deep footprint | USACE NCMP / JALBTCX coastal charting workhorse; mJ-class pulse energy |
| **HawkEye-5 / 4X** (Leica Geosystems) | 532 nm deep + Chiroptera shallow, 1,064 nm topo, RGB | 10 kHz deep + ~140 kHz shallow; 15°–20° elliptical Palmer | $\approx 3\,Z_{\text{SD}}$ (deep); $\approx 1.5\,Z_{\text{SD}}$ (shallow) | 400–600 m AGL; wide divergence (~4.75–7.5 mrad deep) | Dual-mode coastal charting + dense beach/intertidal mapping |
| **Chiroptera-5 / 4X** (Leica Geosystems) | 532 nm shallow bathy, 1,064 nm topo, medium-format RGB | ~140 kHz bathy; ~500 kHz topo; elliptical Palmer | $\approx 1.5\,Z_{\text{SD}}$ (typically 10–25 m clear coast) | 400–600 m AGL; high density ($5\text{–}20\text{ pts m}^{-2}$) | Topobathy shoreline, reef flat, and intertidal mapping |
| **VQ-880-G / VQ-880-G II** (RIEGL) | 532 nm full-waveform + optional 1,064 nm NIR/RGB | 200–700 kHz; 20° circular Palmer (forward/aft looks) | $\approx 1.5\,Z_{\text{SD}}$ | 400–600 m AGL; ~0.7–2.0 mrad divergence | High-density shallow coast, tidal inlets, and clear rivers |
| **VQ-840-G / -GL** (RIEGL) | 532 nm compact full-waveform | 50–200 kHz; elliptical/circular scan | $\approx 1.7\text{–}2.0\,Z_{\text{SD}}$ (rate-dependent) | 50–150 m (UAS/heli) to 600 m AGL | Compact riverine, marsh, and pocket-beach topobathy |
| **RAMMS** (Fugro) | 532 nm multi-beam pushbroom | Fan-beam pushbroom geometry (proprietary PRF) | $\approx 3\,Z_{\text{SD}}$ (vendor-stated) | ~400 m AGL; ~2 mrad configurable divergence | Compact coastal bathymetry; requires vendor processing pipeline |

> **Physics Warning — Water Clarity Controls Range:** Bottom-return power falls as $\exp(-2\,k_{\text{sys}}\,z)$; doubling pulse energy adds less than $2\text{ m}$ of depth at $k_{\text{sys}} = 0.2\text{ m}^{-1}$, whereas halving attenuation $K_d$ doubles achievable depth. Quoted Secchi multiples ($1.5\text{–}3\,Z_{\text{SD}}$ or $(3\text{–}4.5)/K_d$) drop by roughly one Secchi depth over dark mud, basalt, or seagrass (5 % albedo vs. 40–60 % coral sand). See [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md) and [Section 9.2](../../gemini4/book/ch-09/sec-09-02.md).

---

## 2. Governing Specifications Crosswalk

Coastal ALB projects routinely serve two masters simultaneously—hydrographic charting/dredging and terrestrial floodplain/shoreline modeling—whose statistics, confidence levels, and surface definitions differ:

| Standard & Edition | Scope in ALB | Statistical Metric & Confidence | Typical Coastal Thresholds | Reference |
|---|---|---|---|---|
| **NOAA HSSD** (2024 edition, restructured; annual updates) & **FPM** | US charting acceptance, crosslines, TPU, BAG/S-102, Descriptive Report | 95 % TVU & THU (Eren et al. 2019 / S-44 aligned) | Crosslines $\ge 4\%$ ($\ge 100\%$ coverage) or $\ge 8\%$ ($<100\%$ coverage); DTON alert $\le 24\text{ h}$; BAG/S-102 uncertainty | [Chapter 70](../../fable/chapters/ch70-specifications-guided-tour.md) |
| **IHO S-44 Ed. 6.2.0** (Oct 2024; core Table 1 TVU/THU $a/b$ values unchanged from Ed. 6.1.0 baseline in handbook, adding §3.8 seabed characteristics) & **S-102 Ed. 3.0.0** (2024) | Bathymetric orders (Special, Order 1a, 1b, Survey Matrix, §3.8 seabed characterization) | $\text{TVU}_{95\%}(d) = \sqrt{a^2 + (bd)^2}$ | Order 1a: $a=0.5\text{ m}, b=0.013$ ($\text{TVU}_{95\%}=0.56\text{ m}$ at $20\text{ m}$); Special: $a=0.25\text{ m}, b=0.0075$ | [Section 24.1](../../gemini4/book/ch-24/sec-24-01.md) |
| **USGS LBS** (2024 rev. A / 2025 rev. A) | Subaerial topography, QL0–QL2 density, overlap, LAS 1.4 classes 40–45 | $\text{RMSE}_V$ (NVA pass/fail; VVA reported) | QL1/QL2 NVA $\text{RMSE}_V \le 0.10\text{ m}$; inter-swath $\text{RMSD}_z \le 0.08\text{ m}$; ANPD $\ge 8\text{ or }2\text{ pls m}^{-2}$ | [Chapter 70](../../fable/chapters/ch70-specifications-guided-tour.md) |
| **ASPRS PAS Ed. 2 v2** (2023/2024) & **Topo-Bathy Profile** (2013/2019) | Checkpoint design ($\ge 30$/stratum), quadrature checkpoint variance, LAS 40–45 (incl. Class 45 extinction) | $\text{RMSE}_V$, $\text{RMSE}_H$, $\text{RMSE}_{3D}$ | Reported $\text{RMSE}_{\text{rep}} = \sqrt{\text{RMSE}_{\text{obs}}^2 + \sigma_{\text{cp}}^2}$; conservative project target $\sigma_{\text{cp}} \le \sigma_{\text{prod}}/3$ (`2x` Ed. 2 floor) | [Chapter 53](../../fable/chapters/ch53-accuracy-assessment.md) |
| **USACE EM 1110-2-1003** (2013) & **JALBTCX NCMP** | Navigation dredging payment & recurring national coastal mapping | 95 % vertical tolerance (0.15 / 0.30 / 0.60 m tiers) | ~1.6 km (1 US mi) coastal swath (~1,000 m onshore to optical extinction offshore); strict datum ties | [Chapter 66](../../fable/chapters/ch66-coastal-marine-polar-lakes-rivers.md) |
| **FAA AC 70-1B / ANSI Z136.6 / 14 CFR § 91.509 / Part 43** | Outdoor laser notice (Form 7140-1), NOHD eye safety, overwater gear, STC port glass | MPE / NOHD ($1\times$ ocular margin), statutory equipment | NOHD $\le$ planned AGL floor; Form 337/STC signed; PFDs + 406 MHz ELT + raft per rule | [09 External Register](09-resources-and-templates.md), [Chapter 68](../../fable/chapters/ch68-legal-issues.md) |

---

## 3. Mandatory Coordinate, Sign & Refraction Rules

1. **Single Unified Vertical Datum & Coastal Triad Across the Shoreline:** Never deliver subaerial points in NAVD88 and submerged points in MLLW inside one unflagged LAS or DEM—doing so creates a $0.3\text{–}1.5\text{ m}$ cliff at the waterline ([Chapter 9](../../fable/chapters/ch09-vertical-datums.md)). Enforce the coastal vertical datum triad **$h = H + N = z_{\text{CD}} + \mathrm{SEP} = \mathrm{SEP} - d_{\text{CD}}$**, process and archive in a **single working ellipsoidal height ($h$)** with explicit frame, realization, and epoch (e.g., ITRF2020 or NAD83(2011) epoch 2010.0), and apply one documented separation grid (VDatum/VORF/GEOID) to produce the deliverable vertical datum.
2. **Explicit Sign Convention & Axis Frames:** State `+z ↑` (elevation positive upward, metres) vs. `+d ↓` (hydrographic depth positive downward, metres; note **BAG FSD 2.0.1** uses `+z ↑`, whereas **IHO S-102 Ed. 3.0.0** enforces `+d ↓` with **`verticalCS = 6498`** — verify depth-vs-elevation sign explicitly via GDAL/HDF5 metadata). Document aircraft lever arms in explicitly labeled **RFU / ENU** vs. **FRD / NED** body coordinates.
3. **Phase ($n_p$) vs. Group ($n_g$) Refractive Index Separation:** Apply the **phase index** $n_p \approx 1.3411\text{–}1.3420$ ($532\text{ nm}$ seawater; $1.3350$ freshwater) in 3D Snell vector ray bending and the **group index** $n_g = n_p - \lambda\,\mathrm{d}n_p/\mathrm{d}\lambda \approx 1.3638\text{–}1.3651$ (seawater; $1.3566$ freshwater) for two-way slant range $s_w = c_0 \Delta t_w / (2 n_g)$. Substituting $n_p$ for $n_g$ biases depths deep by $+1.6\text{–}1.8\%$ ($+33\text{ to }+36\text{ cm}$ at $20\text{ m}$ depth).
4. **SI Primary Units:** Report all distances, elevations, depths, uncertainties, and flight altitudes in SI units (`m`, `km`, `m/s`), citing statutory US aviation values in parentheses only where required by regulation (e.g., `3,810 m (12,500 ft MSL per 14 CFR § 91.211)`).

---

## 4. Checklist Suite Index & Master Gate Sign-Off

| Phase | Checklist File | Primary Owner | Key Go/No-Go `[GATE]` Decisions | Companion Shared Template |
|---|---|---|---|---|
| **01** | [01-requirements-and-preplanning.md](01-requirements-and-preplanning.md) | PI / Lead Hydrographer | Spec crosswalk, single CRS/datum lock, ICESat-2/MODIS $K_d$ recon, turbidity abort gate | [`template-project-header.md`](../_shared/template-project-header.md) |
| **02** | [02-permits-safety-insurance-cost.md](02-permits-safety-insurance-cost.md) | Aviation Ops / LSO / PM | FAA 7140-1 + LCH, ANSI Z136.6 NOHD/shutter, STC/Form 337, § 91.509 raft/ELT, Hull+Overwater+E&O COIs, standby budget | [`template-insurance-coi.md`](../_shared/template-insurance-coi.md), [`template-cost-ledger.md`](../_shared/template-cost-ledger.md) |
| **03** | [03-platform-sensor-prep-and-support.md](03-platform-sensor-prep-and-support.md) | Sensor Eng / Field Lead | Belly glass bowing check, 532/1064/647 nm co-alignment, chiller, lever arms/1PPS, CORS $\le 20\text{ km}$, VDatum/gauges, Secchi teams, dry+submerged ref surfaces & $\ge 30$/stratum CPs | [`template-project-header.md`](../_shared/template-project-header.md) |
| **04** | [04-mission-or-flight-planning.md](04-mission-or-flight-planning.md) | Flight Planner / Hydrographer | 15–20° Palmer geometry, strict $30^\circ\text{–}45^\circ$ sun window, low-tide ALB + high-tide vessel sync (100–500 m overlap), NOHD AGL floor, 5–10 % cross-strips, *a priori* TPU budget | [`multimodal-white-ribbon.md`](../_shared/multimodal-white-ribbon.md), [`template-error-budget.md`](../_shared/template-error-budget.md) |
| **05** | [05-underway-qc-and-field-processing.md](05-underway-qc-and-field-processing.md) | Airborne Operator / Field QC | Live waveform SNR vs. Secchi, Class 45 voids, NIR surface health, daily PPK $\le 5\text{–}10\text{ cm}$, dry+wet overlap, SHA-256 3-2-1 ingest | [`multimodal-white-ribbon.md`](../_shared/multimodal-white-ribbon.md) |
| **06** | [06-accidents-and-emergencies.md](06-accidents-and-emergencies.md) | PIC / LSO / Safety Officer | Ditching/ELT, **532 nm ocular exposure** shutter-kill + ophthalmology, hard-landing boresight freeze, NTSB 49 CFR 830 immediate, FAA/LSO/insurer clocks | [`template-accident-card.md`](../_shared/template-accident-card.md) |
| **07** | [07-demob-processing-and-validation.md](07-demob-processing-and-validation.md) | Processing Lead / QA Lead | Post-campaign boresight & flat-seabed closure BEFORE release, raw custody gate, deconvolution $<1\text{ m}$, $n_p/n_g$ refraction, LAS 40–45/BAG/COG/TBDEM, MBES/ICESat-2 cross-check | [`template-error-budget.md`](../_shared/template-error-budget.md) |
| **08** | [08-error-budget-and-retrospective.md](08-error-budget-and-retrospective.md) | PI / QA Lead | Reconciled wave/refraction/pulse-stretch/seagrass/VDatum budget ($\chi^2$ 95 % CI, variogram), 14–30 day AAR, checklist Git diff | [`template-aar-retrospective.md`](../_shared/template-aar-retrospective.md) |
| **09** | [09-resources-and-templates.md](09-resources-and-templates.md) | Field & Processing Teams | Critique of JALBTCX, HSSD, LBS, ASPRS, ANSI Z136.6, AC 70-1B; copy-ready Secchi, laser-shutter, and sortie logs | — |

### Master Project Gate Sign-Off Sheet

| Gate Stage | Responsible Role | Independent Verifier | Printed Name & Credentials (PLS / CH / LSO / ATP) | Verification Artifact / Hash | Status (`PASS` / `HOLD`) | UTC Timestamp & Signatures |
|---|---|---|---|---|---|---|
| **G1: Requirements & Clarity Recon (`01`)** | Principal Investigator / Lead Hydrographer | Geodesist / Co-PI | `______________________` | Project Instructions + $K_d$/ICESat-2 Memo | `[ ] PASS  [ ] HOLD` | `__________________` |
| **G2: Permits, Laser NOHD, Safety & COIs (`02`)** | Laser Safety Officer / Aviation Ops Mgr | PIC / Risk Lead | `______________________` | FAA 7140-1 + Form 337 + LSHA + COIs | `[ ] PASS  [ ] HOLD` | `__________________` |
| **G3: Aircraft/Sensor Prep & Control (`03`)** | Chief Sensor Engineer / Geodesist | Second Engineer / PLS | `______________________` | Lever-Arm Survey + 1PPS + CP/Gauge Report | `[ ] PASS  [ ] HOLD` | `__________________` |
| **G4: Flight Plan, Sun/Tide Sync & TPU (`04`)** | Flight Planning Lead | Lead Hydrographer | `______________________` | GIS Line Plan + White-Ribbon Schedule + TPU | `[ ] PASS  [ ] HOLD` | `__________________` |
| **G5: Final Acquisition & Custody Before Demob (`05`/`07`)** | Airborne Field Lead / QC Lead | Data Manager | `______________________` | Closure Lines + SHA-256 3-2-1 Manifest | `[ ] PASS  [ ] HOLD` | `__________________` |
| **G6: Final TBDEM Validation & AAR Release (`07`/`08`)** | Lead Processor / PI | Independent QA Reviewer | `______________________` | S-44/ASPRS Ed. 2 Report + Reconciled AAR | `[ ] PASS  [ ] HOLD` | `__________________` |

*Core References:* [Chapter 19 — Bathymetric Lidar](../../fable/chapters/ch19-bathymetric-lidar.md) · [Chapter 26 — Survey Planning](../../fable/chapters/ch26-survey-planning.md) · [Chapter 70 — Specifications Guided Tour](../../fable/chapters/ch70-specifications-guided-tour.md) · [Appendix G — Checklists](../../fable/appendices/appendix-g-checklists.md) · [Section 9.2 — Bathymetric LiDAR](../../gemini4/book/ch-09/sec-09-02.md) · [Section 13.2 — Environmental & Tidal Scheduling](../../gemini4/book/ch-13/sec-13-02.md).

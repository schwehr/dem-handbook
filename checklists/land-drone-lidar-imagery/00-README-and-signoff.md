# On-Land Drone (UAS) LiDAR + Imagery — Modality Overview & Master Sign-Off

> **Modality ID:** `land-drone-lidar-imagery` | **Governing Standards:** ASPRS Positional Accuracy Standards Edition 2 (v2, 2024) + Addendum V (UAS), USGS LiDAR Base Specification (2025 rev. A), FAA 14 CFR Part 107 / `49 U.S.C. § 44807` / EASA `(EU) 2019/947` SORA  
> **Primary Handbook References:** [`fable` Ch. 16](../../fable/chapters/ch16-platforms.md), [Ch. 18](../../fable/chapters/ch18-topographic-lidar.md), [Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md), [Appendix G](../../fable/appendices/appendix-g-checklists.md); [`gemini4` §7.3](../../gemini4/book/ch-07/sec-07-03.md), [§8.2](../../gemini4/book/ch-08/sec-08-02.md)  
> **Shared Templates:** [Project Header](../_shared/template-project-header.md) | [Error Budget](../_shared/template-error-budget.md) | [Cost Ledger](../_shared/template-cost-ledger.md) | [Insurance COI](../_shared/template-insurance-coi.md) | [Accident Card](../_shared/template-accident-card.md) | [AAR Retrospective](../_shared/template-aar-retrospective.md) | [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md)

> **Offline Field-Binder Rule:** Print or cache the full field bundle (`checklists/land-drone-lidar-imagery/00–09.md` plus `../_shared/template-accident-card.md` and `template-insurance-coi.md`) offline before mobilization. Every `[GATE]` threshold, formula, and statutory clock in `01`–`08` is self-contained inline so crews never require internet lookups to execute go/no-go decisions; laminate `06-accidents-and-emergencies.md` + `template-accident-card.md` inside each GCS case and field truck.

---

## 1. Modality Scope & Operating Envelope

This directory defines the end-to-end field, regulatory, calibration, processing, and accuracy-assurance checklists for **on-land uncrewed aircraft system (UAS) topographic LiDAR and RTK/PPK Structure-from-Motion (SfM) photogrammetry** generating Digital Surface Models (DSMs), bare-earth Digital Terrain Models (DTMs), and georeferenced orthomosaics/point clouds.

This modality applies to small UAS under `25 kg` (`55 lb` per FAA 14 CFR Part 107 / EASA Open & Specific categories; `122 m` / `400 ft AGL` FAA cap vs. `120 m` EASA Open cap — planning `<= 120 m` satisfies both) and approved heavy-lift multirotors or VTOL aircraft operating under `49 U.S.C. § 44807` exemptions + COAs or EASA Specific SORA authorizations. Use these checklists whenever centimeter-to-decimeter terrain mapping covers compact corridors, coastal bluffs, quarries, floodplains, landslides, coastal marshes, forests, or repeat geomorphic monitoring below crewed airborne break-even scales (`< 1–20 km²/day` planning envelope; [01-requirements-and-preplanning.md](01-requirements-and-preplanning.md)).

### Platform & Sensor Class Envelope (Planning Estimates)

| Platform / Payload Class | Endurance, Speed & Daily Area | Typical Payload | Effective Canopy Penetration | Realistic Vertical Accuracy (`RMSE_V`) | Primary Failure Modes & References |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Multirotor + Optical SfM (RTK/PPK, Global Shutter)** | `20–45 min`, `5–15 m/s`, `< 1–2.5 km²/day` | `0.5–3 kg` (up to `10 kg` heavy-lift) | **None** under closed canopy (DSM only; grass/shrub bias `+0.10–0.50 m`) | `2.0–5.0 cm` (`1–2× GSD` with obliques + control; `3–5× GSD` without) | Radial doming without obliques/fixed IO; water glint spikes; rolling-shutter blur ([Ch. 16](../../fable/chapters/ch16-platforms.md), [Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md), [`gemini4` §8.2](../../gemini4/book/ch-08/sec-08-02.md)) |
| **Fixed-Wing / VTOL + Optical SfM (PPK)** | `60–180 min`, `15–25 m/s`, `1–20 km²/day` | `0.5–3 kg` | **None** under closed canopy | `2.5–6.0 cm` (`1–2× GSD` on hard bare surfaces) | Landing terrain impact; high wind crab/crab-pitch blur; weak side-lap over relief ([Ch. 16](../../fable/chapters/ch16-platforms.md), [`gemini4` §7.3](../../gemini4/book/ch-07/sec-07-03.md)) |
| **Multirotor / Heavy-Lift + Survey-Grade UAS LiDAR** (`miniVUX` / `CL-360` + Industrial/Tactical IMU) | `20–35 min` (electric) or `60–120 min` (hybrid/VTOL), `5–10 m/s` | `1.5–10 kg` | Multi-return (`3–7` returns); `30–60 %` leaf-off deciduous, `5–20 %` leaf-on, `1–5 %` dense conifer | `2.5–4.0 cm` (`RMSE_V` @ `60–100 m` AGL, bare earth) | Cold MEMS yaw drift (`0.05–0.15°`) without figure-8; isolator flutter; hover saturation ([Ch. 18](../../fable/chapters/ch18-topographic-lidar.md), [`gemini4` §7.3](../../gemini4/book/ch-07/sec-07-03.md)) |
| **Multirotor + Mid-Grade Solid-State UAS LiDAR** (`Livox Avia` / `DJI L1`/`L2`) | `25–40 min`, `5–10 m/s` | `0.9–1.5 kg` | Multi-return (`2–5` returns); reduced foliage penetration past `80–100 m` AGL | `5.0–10.0 cm` (warm IMU, calm wind); degrades to `10–30 cm` if cold/fast turns | Thermal/yaw heading drift during straight lines; `0.2–0.5°` beam divergence smear ([Ch. 18](../../fable/chapters/ch18-topographic-lidar.md)) |

---

## 2. Coordinate Frames, Sign Conventions, Accuracy Metrics & Units

All UAS deliverables and trajectory files enforce explicit frame declarations ([`gemini4` Notation & Symbols §1](../../gemini4/book/00-front-matter/notation-and-symbols.md), [`fable` Ch. 8](../../fable/chapters/ch08-horizontal-datums.md)):

- **Body Axes (`FRD` / `RFU`) vs. Local-Level Frames (`NED` vs. `ENU`):** Inertial/GNSS post-processed trajectories (`SBET`) typically define aircraft body axes as **Forward–Right–Down (`FRD`)** (`+x_b` nose forward, `+y_b` starboard, `+z_b` nadir down; vs. **`RFU`** `+x` starboard, `+y` nose, `+z` up) referenced to local-level **North–East–Down (`NED`)**. Photogrammetric and GIS grids express coordinates in right-handed **East–North–Up (`ENU`)** (`+X` East, `+Y` North, `+Z` up). Mixing `NED` boresight angles (`rx, ry, rz`) or lever-arm signs with `ENU` axes flips vertical and lateral corrections by `2×` ([Notation & Symbols §1](../../gemini4/book/00-front-matter/notation-and-symbols.md)).
- **Vertical Sign Convention & Realization:** Topographic UAS products deliver **Elevation (`+z ↑`, meters)** referenced to a named vertical datum (e.g., `NAVD88` via `GEOID18`, `EGM2008`, or explicit ellipsoidal `ITRF2020 / WGS 84 (G2296)` with epoch; [Ch. 8](../../fable/chapters/ch08-horizontal-datums.md)). Never mix ellipsoidal (`h`) and orthometric (`H = h - N`) heights or deprecated US Survey Foot units (retired `2022-12-31`).
- **ASPRS Ed. 2 Metrics & Units:** **ASPRS PAS Edition 2 (v2, 2024)** drops legacy Ed. 1 `1.96 ×` NVA multipliers and VVA pass/fail thresholds, reporting `1σ` **`RMSE_V`**, **`RMSE_H`**, and **`RMSE_3D`** with checkpoint uncertainty ($\sigma_{\text{cp}}$) folded in quadrature ($\sqrt{\text{RMSE}_{\text{test}}^2 + \sigma_{\text{cp}}^2}$); any `LE95`/`CE95` figures cited in planning are legacy ASPRS Ed. 1 / NSSDA informational equivalents. SI meters (`m`, `cm`, `m/s`, `Hz`, `hPa`, `kg`) are primary everywhere; statutory imperial equivalents appear only in parentheses (`122 m` / `400 ft AGL`).

---

## 3. Master Checklist Index (`01`–`09`)

| Phase File | Lifecycle Stage | Primary Owner | Blocking Gate Focus |
| :--- | :--- | :--- | :--- |
| [01-requirements-and-preplanning.md](01-requirements-and-preplanning.md) | Requirements, Recon & Feasibility | Survey Lead / PM | Platform vs crewed ALS break-even, DSM vs DTM under canopy, ASPRS Ed. 2 target class, wind/season climatology |
| [02-permits-safety-insurance-cost.md](02-permits-safety-insurance-cost.md) | Permits, Airspace, Legal, Insurance & Cost | Remote PIC & Legal/PM | Part A (Part 107 / `§ 44807` / SORA, ROE, CARE-OCAP® / *Ritter* PLS, UN 3480/3481, Aviation COI vs CGL exclusion) & Part B (Daily Safety/Burn-Rate) |
| [03-platform-sensor-prep-and-support.md](03-platform-sensor-prep-and-support.md) | Airframe, Payload, Base & Control Prep | Flight Engineer & Survey Lead | Isolator resonance ($f_n$), rolling shutter / hot-shoe $\Delta t_{\text{sync}}$, lever arms, OPUS static base, strict GCP vs `>= 30` withheld CP wall |
| [04-mission-or-flight-planning.md](04-mission-or-flight-planning.md) | Mission Design & *A Priori* Error Budget | Remote PIC & Geodesist | `122/120 m` AGL SRTM/barometer trap (`-8.32 m/hPa`), `80/70` + `10–20°` obliques vs `30–50 %` sidelap + figure-8, worked TPU budgets |
| [05-underway-qc-and-field-processing.md](05-underway-qc-and-field-processing.md) | Field Ops, Per-Battery & Pre-Departure QC | Remote PIC & Field Processor | Per-battery RTK/blur check, pre-departure `RTKLIB` (`$10`) PPK fix `>= 95 %` & coarse tie/strip check, dual-SSD `sha256sum` custody |
| [06-accidents-and-emergencies.md](06-accidents-and-emergencies.md) | Incidents, Emergency & Boresight Recovery | Remote PIC & Safety Officer | Printable laminated card (`911`/FSDO/ROC contacts), flyaway/wire/water/LiPo deluge, FAA `14 CFR § 107.9` & NTSB `49 CFR 830` clocks, post-impact IMU + IO recal |
| [07-demob-processing-and-validation.md](07-demob-processing-and-validation.md) | Demob, Processing, Strip Adj. & ASPRS QA | Lead Geodesist / Processor | LiPo `3.8 V/cell` (`<= 30 %` air), RTS PPK + strip adj (`Withheld=1`) / rolling-shutter + NDWI glint mask, `>= 30` CP quadrature + Nuth–Kääb QA, COG/COPC/STAC |
| [08-error-budget-and-retrospective.md](08-error-budget-and-retrospective.md) | Reconciled Error Budget & 30-Day AAR | Survey Lead & QA Reviewer | `[SfM]` vs `[LiDAR]` variance reconciliation, $\chi^2$/`NMAD`/variogram $L_{\text{corr}}$ forensics, cost/schedule AAR & checklist PR loop |
| [09-resources-and-templates.md](09-resources-and-templates.md) | Tools, Critiques, External Register & Logs | All Roles | ASPRS Ed. 2 / LBS / Part 107 / SORA / ODM / COLMAP / PDAL critiques, External Statutory Register, LiPo, Part 107 & split `gcps`/`cps_withheld` templates |

---

## 4. Phase Gate Master Sign-Off Register (Two-Person Verification)

Every phase gate requires verification by both the **Responsible Phase Lead** and an **Independent Verifier**, holding UTC date/time, signatures, and archive link to passing evidence before advancing or delivering products.

| Gate ID | Milestone / Gate Condition | Required Verification Evidence | Phase Lead Sign-Off & UTC Date | Independent Verifier Sign-Off & UTC Date | Status (`PASS` / `HOLD`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **G-01** | Feasibility, canopy DSM/DTM choice & ASPRS Ed. 2 specs locked ([Phase 01](01-requirements-and-preplanning.md)) | Signed Project Instructions, 3DEP/NDVI recon snapshot, break-even check | `__________________` | `__________________` | `[ ]` |
| **G-02** | Airspace (LAANC/`§ 44807`/SORA), ROE, PLS/privacy, UN 3480/3481 & Aviation COI active ([Phase 02](02-permits-safety-insurance-cost.md)) | Approved LAANC/SORA PDF, signed ROE, COI explicitly confirming Aviation/Payload/E&O | `__________________` | `__________________` | `[ ]` |
| **G-03** | Isolators, hot-shoe sync, lever arms (`FRD/NED` vs `ENU`), PPK base `<= 15 km` (OPUS), & GCP vs `>= 30`/stratum CP wall ([Phase 03](03-platform-sensor-prep-and-support.md)) | Lever-arm photo/cal report, OPUS datasheet, split `gcps.csv` / `cps_withheld.csv` | `__________________` | `__________________` | `[ ]` |
| **G-04** | Terrain-following DSM cleared for `122/120 m` AGL + baro drift; *a priori* TPU `<` spec ([Phase 04](04-mission-or-flight-planning.md)) | Flight plan KML over local DTM, overlap/cross-strip check, error-budget table | `__________________` | `__________________` | `[ ]` |
| **G-05** | Pre-departure PPK fix `>= 95 %`, coarse tie/doming & swath overlap pass, dual-SSD `sha256sum` complete ([Phase 05](05-underway-qc-and-field-processing.md)) | Field PPK summary plot, overlap diff map, `sha256sum` manifests (`copy_A`, `copy_B`) | `__________________` | `__________________` | `[ ]` |
| **G-06** | Incident clearance (zero unresolved § 107.9 / Part 830 / OSHA clocks; post-impact IMU + IO recal if triggered) ([Phase 06](06-accidents-and-emergencies.md)) | Incident log (or "None"), post-impact patch/boresight + camera IO diff if struck | `__________________` | `__________________` | `[ ]` |
| **G-07** | Final PPK + strip/BA + NDWI water mask + ASPRS Ed. 2 (`>= 30` CP quadrature + Nuth–Kääb) pass; COG/COPC/STAC valid ([Phase 07](07-demob-processing-and-validation.md)) | ASPRS Ed. 2 accuracy report, `gdalinfo`/COPC check, STAC metadata JSON | `__________________` | `__________________` | `[ ]` |
| **G-08** | Reconciled error budget, cost ledger variance, 30-day AAR & checklist improvement PR closed ([Phase 08](08-error-budget-and-retrospective.md)) | Reconciled TPU vs empirical report, final cost sheet, Git PR link | `__________________` | `__________________` | `[ ]` |

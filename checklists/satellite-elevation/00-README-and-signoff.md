# Satellite-Built Elevations — Overview & Phase Sign-Off

Spaceborne elevation products span five distinct physical measurement regimes—agile optical stereo/tri-stereo, declassified historical film-return stereo, single-pass and repeat-pass interferometric SAR (InSAR/KaRIn), spaceborne photon-counting/waveform altimetry, and multispectral Satellite-Derived Bathymetry (SDB). Unlike airborne or shipborne campaigns where the survey crew operates the vehicle, satellite missions separate **orbital tasking and raw Level-1 collection** (governed by commercial/agency Service-Level Agreements and tight quick-look rejection windows) from **ground calibration/check-point surveying, geophysical processing, and independent validation**.

This directory operationalizes Phases `01`–`08` plus tools/templates (`09`) for satellite-built topography and nearshore bathymetry under [Appendix G](../../fable/appendices/appendix-g-checklists.md) and [Chapter 7.5](../../gemini4/book/ch-07/sec-07-05.md).

> **Offline Field-Binder Rule (`PRD` §2.3):** Every operational phase checklist (`01`–`08`) inlines its executable thresholds, equations, and statutory notification clocks so ground-control teams and orbital QC desks operate fully offline. Bundle `checklists/satellite-elevation/00`–`09` together with `../_shared/` ([Accident Card](../_shared/template-accident-card.md), [Insurance COI](../_shared/template-insurance-coi.md), [Project Header](../_shared/template-project-header.md)); laminate `06-accidents-and-emergencies.md` + `template-accident-card.md` inside every field-crew vehicle binder.

---

## 1. Modality Scope & Sensor Matrix

| Sub-Track | Representative Platforms / Archives | Primary Measurement Physics | Typical Posting & Nominal Vertical Regime | Primary Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Agile Optical Stereo & Tri-Stereo** | WorldView-1/2/3/Legion (`0.31–0.50 m`), Pléiades-1A/1B (`0.50 m`), Pléiades Neo (`0.30 m`), SkySat/Pelican (`0.30–0.50 m`), SPOT-6/7 (`1.5 m`), ASTER/ALOS PRISM | Along-track multi-angle RPC/line-scanner disparity matching (First Visible Surface **DSM**) | `0.5–4.0 m` GSD DEM; `0.5–1.5 m` `LE90` (with GCPs/bundle adjust) | [ch22](../../fable/chapters/ch22-photogrammetry-sfm.md), [sec-07-05](../../gemini4/book/ch-07/sec-07-05.md) |
| **Historical Film-Return Stereo** | CORONA KH-1–KH-4B (`1960–1972`), HEXAGON KH-9 mapping frame (`1,081` reseau crosses, `1971–1986`) & panoramic | Scanned analog film, panoramic / frame collinearity after reseau dewarp & fiducial calibration | `2–15 m` GSD DEM; `5–15 m` `RMSE_V` (epoch baseline) | [ch22](../../fable/chapters/ch22-photogrammetry-sfm.md), [sec-07-05](../../gemini4/book/ch-07/sec-07-05.md) |
| **Single-Pass & Repeat-Pass InSAR / KaRIn** | SRTM/NASADEM (`C`-band), TanDEM-X / Copernicus `GLO-30` & `EEA-10` / WorldDEM Neo (`X`-band), Sentinel-1 (`C`-band), NISAR (`L`/`S`-band), ESA Biomass (`P`-band), SWOT (`Ka`-band WSE) | Interferometric phase difference (`p=1` bistatic, `p=2` repeat-pass) + scattering phase center | `10–30 m` posting (commercial `WorldDEM Neo` `5 m`, `<1.4 m LE90`); canopy/firn penetration dependent | [ch21](../../fable/chapters/ch21-radar-sar-insar.md), [appendix-e](../../fable/appendices/appendix-e-public-products-tables.md), [sec-11-01](../../gemini4/book/ch-11/sec-11-01.md) |
| **Spaceborne Altimetry Control** | ICESat-2 ATLAS (`ATL03`, `ATL06`, `ATL08`, `ATL11`, `ATL14`, `ATL24`), ISS GEDI (`L2A`), SWOT nadir | `532 nm` photon-counting lidar (`~11–14 m` footprint, `0.7 m` along-track) & `1064 nm` full-waveform lidar (`25 m` footprint) | Along-track spot control (`<0.10–0.50 m` `RMSE_V` over flat/bare terrain) | [ch25](../../fable/chapters/ch25-calibration-infrastructure.md), [ch52](../../fable/chapters/ch52-ground-truth.md), [sec-11-02](../../gemini4/book/ch-11/sec-11-02.md) |
| **Satellite-Derived Bathymetry (SDB) & Wave Kinematics** | Sentinel-2, Landsat-8/9, SuperDove, WorldView-2/3, Pléiades Neo + `ATL24` calibration | Empirical log-ratio (`Stumpf`/`Lyzenga`), radiative transfer (`HOPE`/`ACOLITE`), or Airy wave dispersion ($\omega^2 = g k \tanh(kh)$) | `2–10 m` (optical SDB to $2\text{–}3/K_d$, max `~20–30 m` clear); `100–500 m` wave inversion; `IHO B-13` / `CATZOC C–D` | [ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md), [sec-11-03](../../gemini4/book/ch-11/sec-11-03.md) |

---

## 2. Governing Standards & Reference Documents

- **Photogrammetry & General Elevation Accuracy:** [ASPRS Positional Accuracy Standards Ed. 2 (2024; v2 Addenda I–VI)](../../fable/chapters/ch70-specifications-guided-tour.md) (reports `1σ` `RMSE_V`, `RMSE_H`, `RMSE_3D` with unconditional checkpoint quadrature; `CE90`/`LE90` belong to legacy NSSDA, NGA [MIL-PRF-89020B](../../fable/appendices/appendix-d-standards-index.md), and Copernicus/commercial vendor specs), and [USGS Lidar Base Specification](../../fable/chapters/ch70-specifications-guided-tour.md) (vertical/horizontal validation & metadata conventions).
- **SAR & Analysis-Ready Data:** [CEOS ARD (`CARD4L` NRB/POL/GSLC)](../../fable/chapters/ch21-radar-sar-insar.md), Copernicus DEM Product Handbook (Issue 5.0/6.1) & TanDEM-X `TD-GS-PS-0021`, and ASF Modified Copernicus DEM (`NISAR DEM V1.2`, WGS 84 ellipsoid reference).
- **Hydrography & SDB:** [IHO B-13 Ed. 1.0.0 (Guidance to SDB, March 2024)](../../fable/chapters/ch23-satellite-derived-bathymetry.md) and **IHO S-44 Ed. 6.2.0 (Oct 2024; core Table 1 TVU/THU a/b values unchanged from Ed. 6.1.0 baseline cited in `fable/`, adding §3.8 seabed characteristics)** (`CATZOC` / `TVU_95%` / `THU_95%`).
- **Regulatory, Licensing & Legal:** NOAA CRSRA **15 CFR Part 960** (Tier 1–3 licensing & shutter control), **India DST 2021** sensitivity thresholds, **China Surveying and Mapping Law** (`GCJ-02`/`BD-09` prohibitions), **GDPR / CARE / OCAP®**, and commercial imagery **EULA derivative-DEM** rules ([ch68](../../fable/chapters/ch68-legal-issues.md), [ch69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md), [sec-27-01](../../gemini4/book/ch-27/sec-27-01.md), [sec-27-02](../../gemini4/book/ch-27/sec-27-02.md), [sec-27-03](../../gemini4/book/ch-27/sec-27-03.md)).
- **Archiving, Interoperability & Mathematical Conventions:** [Notation & Symbols](../../gemini4/book/00-front-matter/notation-and-symbols.md), **OGC Cloud-Optimized GeoTIFF (COG)**, **STAC**, **BagIt SHA-256**, and **`PROJ` / `EPSG`** vertical datum transformations ([ch08](../../fable/chapters/ch08-horizontal-datums.md), [ch09](../../fable/chapters/ch09-vertical-datums.md), [ch50](../../fable/chapters/ch50-archiving-and-provenance.md)).

---

## 3. Phase Navigation & Shared Templates

| Phase | Checklist File | Primary Focus | Linked Shared Template |
| :--- | :--- | :--- | :--- |
| `01` | [01-requirements-and-preplanning.md](./01-requirements-and-preplanning.md) | Surface ontology (DSM vs scattering phase vs SDB), CE90/LE90 contracts, archive-first audit, climatology, vendor rejection & de-scope triggers | [Project Header](../_shared/template-project-header.md) |
| `02` | [02-permits-safety-insurance-cost.md](./02-permits-safety-insurance-cost.md) | 15 CFR Part 960, commercial EULA derivative vs raw rules, India/China/GDPR/CARE, ground-crew safety & PPE, E&O/CGL/Auto insurance, pricing & cloud egress ledger | [Cost Ledger](../_shared/template-cost-ledger.md), [Insurance COI](../_shared/template-insurance-coi.md) |
| `03` | [03-platform-sensor-prep-and-support.md](./03-platform-sensor-prep-and-support.md) | RPC00B vs SPICE/POD ephemeris tiers, Siemens-star/checkerboard GCPs + withheld CPs, trihedral SAR corner reflectors, SDB water-level gauges & `ATL24` calibration | [Error Budget](../_shared/template-error-budget.md) |
| `04` | [04-mission-or-flight-planning.md](./04-mission-or-flight-planning.md) | LTAN/LTDN sun-angle windows, convergence (`15–25°` urban vs `30–45°` open), InSAR $B_{\perp,\mathrm{crit}}$ & $h_{\mathrm{amb}}$, asc/desc pairs, *a priori* stereo/InSAR/SDB error budgets | [Error Budget](../_shared/template-error-budget.md), [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md) |
| `05` | [05-underway-qc-and-field-processing.md](./05-underway-qc-and-field-processing.md) | Collection tracking, quick-look acceptance/rejection within vendor SLA window, B/H & coherence verification, immutable Level-1/RPC/SLC SHA-256 ingest | [Project Header](../_shared/template-project-header.md) |
| `06` | [06-accidents-and-emergencies.md](./06-accidents-and-emergencies.md) | Cloud-out escalation, vendor refund/re-tasking triggers, corrupted orbital telemetry fallback, ground-crew roadside/cliff/medical emergencies, EULA/ITAR spill, cyber recovery | [Accident Card](../_shared/template-accident-card.md) |
| `07` | [07-demob-processing-and-validation.md](./07-demob-processing-and-validation.md) | Field target recovery, ASP (`jitter_solve`)/SETSM/CARS/KH-9 reseau, ISCE3/GMTSAR/SNAP+SNAPHU geocoding check, ACOLITE/Stumpf+tide, Nuth–Kääb `xdem` + ICESat-2/FFT forensics, COG/STAC | [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md) |
| `08` | [08-error-budget-and-retrospective.md](./08-error-budget-and-retrospective.md) | Reconciled *a priori* vs *a posteriori* budget (jitter, $B/H$, APS, unwrapping, penetration, SDB), ML/super-resolution disclosure, AAR & Git improvement diff | [AAR Retrospective](../_shared/template-aar-retrospective.md) |
| `09` | [09-resources-and-templates.md](./09-resources-and-templates.md) | Critiques of ASP, SETSM, CEOS ARD, SNAP, ISCE2/3, SlideRule/`icepyx`, ACOLITE, IHO B-13, Copernicus/NISAR/SWOT; copy-ready Tasking, Quick-Look & Ground-Crew Cards | All `../_shared/` templates |

---

## 4. Program Gate & Role-Split Sign-Off Table

No downstream phase starts until the preceding phase `[GATE]` items are checked off and signed by an independent role where specified (`Tasking Lead` = commercial/agency collection specification & quick-look disposition; `Ground-Control Lead` = GNSS monuments, corner reflectors, tide stations, field safety; `QA / Geodetic Reviewer` = independent bundle/InSAR/SDB verification, held-back checkpoints, and EULA/security audit).

| Sign-Off Gate | Required Evidence & Artifact | Tasking Lead | Ground-Control Lead | QA / Geodetic Reviewer | Program Manager / Client | Date (UTC) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **G1. Requirements & Archive Audit (`01`)** | Signed surface ontology, statistical SLA, archive search log, climatology & abandon triggers | `[ ] Sign` | `[ ] Concur` | `[ ] Verify` | `[ ] Approve` | `____-__-__` | `[ ] Open` |
| **G2. Permits, EULA, Safety & Budget (`02`)** | Part 960 / national clearances, EULA derivative memo, ground safety ERP, COIs, cost ledger | `[ ] Sign` | `[ ] Safety` | `[ ] Legal/QA` | `[ ] Fund` | `____-__-__` | `[ ] Open` |
| **G3. Ephemeris, GCP & Reflector Prep (`03`)** | POD/RPC verification, independent GCP vs CP inventory, corner-reflector RCS & tie survey, `eta(t)` gauges | `[ ] Ephem` | `[ ] Field Tie` | `[ ] Check` | `[ ] Noted` | `____-__-__` | `[ ] Open` |
| **G4. Orbit Geometry & Error Budget (`04`)** | Approved AOI polygon, LTAN/convergence/$B/H$ or $B_\perp$/$h_{\mathrm{amb}}$/asc-desc plan, *a priori* budget | `[ ] Task` | `[ ] Window` | `[ ] Audit` | `[ ] Release` | `____-__-__` | `[ ] Open` |
| **G5. SLA Quick-Look & Raw Ingest (`05`)** | Within-window acceptance/rejection log, cloud/B/H/coherence pass, SHA-256 BagIt Level-1 archive | `[ ] Accept` | `[ ] Field Sync` | `[ ] Hash/QC` | `[ ] Milestone` | `____-__-__` | `[ ] Open` |
| **G6. Contingency & Incident Readiness (`06`)** | Verified vendor re-tasking/refund trigger, field SOS drill, EULA spill & cyber playbook signed | `[ ] Escal` | `[ ] Drill` | `[ ] Cyber` | `[ ] Endorse` | `____-__-__` | `[ ] Open` |
| **G7. Processing, Forensics & Release (`07`)** | Nuth–Kääb co-reg report, withheld-CP/ICESat-2 validation, FFT/histogram audit, COG/STAC/DOI | `[ ] Close` | `[ ] Decom` | `[ ] Certify` | `[ ] Accept` | `____-__-__` | `[ ] Open` |
| **G8. Reconciled Budget & AAR (`08`)** | Reconciled error ledger, ML/fill pixel provenance mask, AAR metrics & checklist PR | `[ ] Input` | `[ ] Input` | `[ ] Sign` | `[ ] Close` | `____-__-__` | `[ ] Open` |

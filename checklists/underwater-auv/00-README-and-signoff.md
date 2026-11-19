# Underwater AUV Bathymetric & Subsea Mapping — Overview & Master Sign-Off

**Modality Code:** `underwater-auv`  
**Applicable Platforms:** Untethered Autonomous Underwater Vehicles (AUVs) — hovering, cruising torpedo-hull, and long-range seabed-mapping classes (e.g., Kongsberg HUGIN 3000/6000/Endurance, WHOI *Sentry* & *REMUS 6000*, NOC *Autosub Long Range*, Exail A18-D)  
**Primary Payloads:** Deep-rated Multibeam Echosounders (MBES, 200–400 kHz), Synthetic Aperture Sonar / Interferometric SAS (SAS/InSAS, e.g., Kongsberg HISAS 1032, Kraken AquaPix), Sidescan Sonar (SSS), Sub-Bottom Profilers (SBP, chirp/parametric), Optical/Laser Line-Scan Imaging  
**Minimum Depth / Endurance Envelope:** Shallow shelf to full ocean depth (`10 m` to `6,000 m`), typical sortie endurance `12 h` to `72 h` at `1.5–2.3 m/s` (`3.0–4.5 kn`), survey altitude `5–70 m` above bottom  

---

## 1. Purpose & Modality Envelope

Shipboard deep-water multibeam echosounders (`12–30 kHz`) resolve seafloor features on the scale of `50–250 m` at `4,500 m` depth because acoustic beam footprints scale linearly with range (`D_fp ≈ 2 d tan(θ/2)`). By flying `5–70 m` above the seabed, an AUV shrinks the footprint of a `0.5° × 1.0°` MBES beam to `0.44 m` at `50 m` altitude — more than two orders of magnitude finer — while SAS/InSAS reaches `2–5 cm` across-track/along-track resolution across `150–400 m` swaths.

That spatial gain is paid for in **positioning, pressure, logistics, and recovery risk**. At `50 m` altitude, a `0.5° × 1.0°` MBES projects a **`0.44 m` along-track × `0.87 m` across-track** elliptical nadir footprint — yet radio-frequency GNSS signals attenuate within `6.3–13 mm` of seawater at L-band, isolating the AUV beneath a moving ocean water column where sound speed varies by `+4.0 m/s` per `°C`, `+1.3 m/s` per `PSU`, and `+1.7 m/s` per `100 m` depth. Operational success hinges on:

1. Pre-dive density-specific ballasting, vacuum/O-ring sealing, and dual emergency drop-weight readiness.
2. Tightly coupled **INS + 4-beam phased-array DVL + Paroscientific Digiquartz pressure + USBL/iUSBL or LBL** navigation, upgraded post-dive via Rauch–Tung–Striebel (RTS) smoothing and bathymetric SLAM (`mbnavadjust`).
3. Strict deck, Li-ion battery (UN 3480 / UN 3481), Launch and Recovery System (LARS), and non-surfacing recovery protocols.
4. Immediate post-recovery station-hold QC **before** the support ship releases station.

| Regime / Mission Class | Typical Altitude (`m`) | Primary Payload | Nominal Resolution (`m`) | Target Standard / Envelope |
| :--- | :--- | :--- | :--- | :--- |
| Deep-ocean tectonic / habitat / cable route | `40–70` | 200–400 kHz MBES + SBP | `0.5–1.5` grid | IHO S-44 Ed. 6.2.0 (Oct 2024; Table 1 TVU/THU unchanged from Ed. 6.1.0, adding §3.8 seabed characteristics) Order 1b / 2; NOAA HSSD `4–8 m` depth-bracketed |
| Pipeline / UXO / wreck / high-res archaeology | `5–30` | 400 kHz MBES + InSAS + camera | `0.02–0.25` | IHO S-44 Special / Exclusive Order relative; GEBCO TID `11` |
| Deep mineral / hydrothermal vent / cliff terrain | `20–50` | Dual-mode MBES / Isobaric pass | `0.25–1.0` | Crossline-tied SLAM (`mbnavadjust`) |
| Polar / under-ice shelf cavity | `25–60` (inverted + seabed) | Up/down MBES + DVL + INS | `0.5–2.0` | IHO S-44 Order 1b / 2 + acoustic homing / emergency abort logic |

---

## 2. Coordinate Frames, Sign Conventions & Datum Contract

Every deliverable, intermediate grid, and navigation trajectory in `underwater-auv` **must declare both** frame orientation and vertical sign explicitly:

- **World Frame (`ENU` vs `NED`):** Geodetic map grids (`BAG`, `GeoTIFF`/`COG`) use right-handed **East–North–Up (`ENU`)** unless otherwise noted; AUV kinematic INS/DVL/sonar body frames use right-handed **Forward–Starboard–Down (`NED`-aligned body frame)** (`+x_b` nose forward, `+y_b` starboard, `+z_b` keel down; roll `φ` right-wing down, pitch `θ` nose up, yaw/heading `ψ` clockwise from North). Transformations between `ENU` and `NED` must apply the proper permutation (`det = +1`), never an improper reflection (`det = -1`).
- **Grid Convergence (`γ`):** Projected CRS heading satisfies `α_grid = ψ_true - γ`; applying true gyro heading directly in UTM without convergence correction induces swath-edge azimuth tilt (`1°` error `≈ 1.75 m` lateral shift per `100 m` off-nadir).
- **Vertical Sign (`+z ↑` vs `+d ↓`) & Datum Sign Relation:**
  - **Bathymetric Attributed Grid (`BAG`, FSD 2.0.1):** `/BAG_root/elevation` stores **Elevation `+z ↑`** (`m`, positive up, seabed negative).
  - **IHO S-102 Ed. 3.0.0 & S-44 Ed. 6.2.0 Equations:** Native S-102 HDF5 `BathymetryCoverage` stores **Depth `+d ↓`** (`m`, positive down, `verticalCS = 6498`, `d = -z`; note GDAL's S-102 driver can expose `+z ↑` elevation unless `DEPTH_OR_ELEVATION=DEPTH` / `verticalCS` is explicitly verified). `S-44 Ed. 6.2.0 (Oct 2024)` preserves core Table 1 `TVU/THU` `a/b` values from `Ed. 6.1.0` cited in `fable/`, adding `§3.8` seabed characteristics.
  - **Vertical Transformation & Sign Equation:** `h = H + N` (ellipsoidal height `h` = orthometric `H` + geoid `N`), Separation Model `S = N + (MSL - geoid) + (CD - MSL)` (note `CD - MSL < 0` when MLLW/LAT lies below MSL), and **`h = z_CD + S = S - d_CD` (so `z_CD = h - S` and `d_CD = S - h`)**. Never confuse a raw geoid model with a Chart Datum `SEP` without verifying sign.

---

## 3. Master Phase Navigation, Offline Binder & Sign-Off Summary

**Offline Field-Binder Bundle:** Print or sync `checklists/underwater-auv/00`–`09` plus `../_shared/template-accident-card.md` and `../_shared/template-insurance-coi.md` (with `06-accidents-and-emergencies.md` laminated as a standalone ship-bridge/LARS quick-action card); every `[GATE]` in `01`–`08` carries inline numeric thresholds so field execution never requires internet access.

Complete each phase file in order (`01` through `08`). A phase is **OPEN** until every `**[GATE]**` item in that phase passes with verifiable evidence and the Phase Lead records UTC completion below.

| Phase | Checklist File | Scope Summary | Minimum Gates | Phase Lead & UTC Sign-Off | Status |
| :--- | :--- | :--- | :---: | :--- | :--- |
| **01** | [01-requirements-and-preplanning.md](./01-requirements-and-preplanning.md) | S-44 Order, CRS/SEP, prior audit, break-even, Project Instructions, spares, abandonment rules | `7` | `__________________` | `[ ] PASS` |
| **02** | [02-permits-safety-insurance-cost.md](./02-permits-safety-insurance-cost.md) | UNCLOS MSR, ITAR/EAR, MMPA/JNCC, UN 3480/3090, RVSS/LARS safety, COI insurance, cost ledger | `8` | `__________________` | `[ ] PASS` |
| **03** | [03-platform-sensor-prep-and-support.md](./03-platform-sensor-prep-and-support.md) | Density ballasting, O-ring vacuum test, drop-weights, RVSS rigging, Digiquartz/CTD cal, USBL/LBL box-in | `9` | `__________________` | `[ ] PASS` |
| **04** | [04-mission-or-flight-planning.md](./04-mission-or-flight-planning.md) | Terrain-follow vs isobaric, 100–200 %+ overlap, SLAM crosslines, patch test, descent drift, TPU budget | `7` | `__________________` | `[ ] PASS` |
| **05** | [05-underway-qc-and-field-processing.md](./05-underway-qc-and-field-processing.md) | Surface wet check, USBL residuals, abort gates, thruster lockout, IR hull check, station-hold quick-grid, 3-2-1 | `9` | `__________________` | `[ ] PASS` |
| **06** | [06-accidents-and-emergencies.md](./06-accidents-and-emergencies.md) | Non-surfacing/entanglement/under-ice/LARS/Li-ion runaway response, beacons, USCG/UNOLS/OSHA/insurer clocks | `6` | `__________________` | `[ ] PASS` |
| **07** | [07-demob-processing-and-validation.md](./07-demob-processing-and-validation.md) | Custody lock, washdown, UN 3480/3481/3090 `<= 30 %` SoC, Carnet, TEOS-10, `mbnavadjust`/CUBE/S-102, Nuth–Kääb | `8` | `__________________` | `[ ] PASS` |
| **08** | [08-error-budget-and-retrospective.md](./08-error-budget-and-retrospective.md) | *A priori* vs *a posteriori* error reconciliation, stratified stats, 14–30 day AAR, checklist PR diff | `6` | `__________________` | `[ ] PASS` |
| **09** | [09-resources-and-templates.md](./09-resources-and-templates.md) | Resource inventory & critique, External Regulatory Register, Dive Plan, Ballasting & O-Ring/Vacuum forms | Ref | `__________________` | `[ ] ACTIVE` |

---

## 4. Shared Templates & Cross-Modality Links

- **Shared Workbook Templates:**
  - [Project Header Block](../_shared/template-project-header.md)
  - [A Priori & A Posteriori Error Budget](../_shared/template-error-budget.md)
  - [Mission Cost & Standby Ledger](../_shared/template-cost-ledger.md)
  - [Insurance Certificate of Insurance (COI) Audit](../_shared/template-insurance-coi.md)
  - [Emergency & Casualty Quick-Action Card](../_shared/template-accident-card.md)
  - [14–30 Day After-Action Review (AAR)](../_shared/template-aar-retrospective.md)
  - [White-Ribbon Multi-Modal Synchronization](../_shared/multimodal-white-ribbon.md) (AUV-to-ship MBES, USV, LiDAR, and photogrammetry overlap)

---

## 5. Primary Handbook & Specification References

- **Fable Handbook:** [Ch. 13 IMU/INS](../../fable/chapters/ch13-imu-ins.md), [Ch. 14 Positioning Beyond GNSS](../../fable/chapters/ch14-positioning-beyond-gnss.md), [Ch. 15 SLAM](../../fable/chapters/ch15-slam.md), [Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md), [Ch. 20 Sonar](../../fable/chapters/ch20-sonar.md), [Ch. 25 Calibration Infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md), [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md), [Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md), [Ch. 68 Legal Issues](../../fable/chapters/ch68-legal-issues.md), [Ch. 69 Security & Ethics](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md), [Ch. 70 Specifications](../../fable/chapters/ch70-specifications-guided-tour.md), [Appendix D Standards Index](../../fable/appendices/appendix-d-standards-index.md), [Appendix G Checklists](../../fable/appendices/appendix-g-checklists.md)
- **Gemini4 Companion:** [Notation & Symbols](../../gemini4/book/00-front-matter/notation-and-symbols.md), [Sec. 5.4 Underwater AUV Positioning](../../gemini4/book/ch-05/sec-05-04.md), [Sec. 7.4 Marine Platforms & AUVs](../../gemini4/book/ch-07/sec-07-04.md), [Sec. 10.2–10.6 Sonar & Acoustic Processing](../../gemini4/book/ch-10/sec-10-02.md), [Sec. 13.1–13.5 Marine Survey Planning, QC & Observability](../../gemini4/book/ch-13/sec-13-01.md), [Sec. 24.1–24.2 Hydrographic Standards & GEBCO](../../gemini4/book/ch-24/sec-24-01.md)

---

## 6. Final Campaign Release Certification

> **Chief Hydrographer / Lead Engineer (IHO Cat A/B or Equivalent):** `__________________` | **Signature / UTC:** `__________________`  
> **AUV Lead Engineer / Vehicle Custodian:** `__________________` | **Signature / UTC:** `__________________`  
> **Vessel Master / Safety Officer (LARS & Deck Custody):** `__________________` | **Signature / UTC:** `__________________`  
> **Cruise Principal Investigator / Operations Manager:** `__________________` | **Signature / UTC:** `__________________`  
> **Release Scope Approved:** `[ ] Raw Archive (NCEI/DCDB)` `[ ] Working Grids Only` `[ ] Final Charting (S-102 / BAG)` `[ ] Public Tiered Release`

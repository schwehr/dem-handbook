# On-Land Drone (UAS) LiDAR + Imagery — Resources, Critiques & Field Templates

> **Modality ID:** `land-drone-lidar-imagery` | **Handbook Portal:** [00-README-and-signoff.md](00-README-and-signoff.md)  
> **Shared Operational Templates:** [Project Header](../_shared/template-project-header.md) | [Error Budget](../_shared/template-error-budget.md) | [Cost Ledger](../_shared/template-cost-ledger.md) | [Insurance COI](../_shared/template-insurance-coi.md) | [Accident Card](../_shared/template-accident-card.md) | [AAR Retrospective](../_shared/template-aar-retrospective.md) | [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md)

---

## 1. Authoritative Standards & Software Critique

Every standard and software tool used in UAS topographic mapping carries strengths and real-world failure traps. Treat this critique matrix as an operational audit guide ([`fable` Appendix D](../../fable/appendices/appendix-d-standards-index.md), [Ch. 70](../../fable/chapters/ch70-specifications-guided-tour.md); [`gemini4` §8.2](../../gemini4/book/ch-08/sec-08-02.md), [§9.6](../../gemini4/book/ch-09/sec-09-06.md), [§19.1](../../gemini4/book/ch-19/sec-19-01.md)).

| Resource / Tool | Operational Role | Key Strengths | Known Weaknesses, Blind Spots & Traps |
| :--- | :--- | :--- | :--- |
| **ASPRS Positional Accuracy Standards Ed. 2 (v2, 2024) + Addendum V & Addendum II** | Governing UAS accuracy & control-survey standard | Eliminates legacy `1.96×` NVA multiplier & VVA pass/fail gates; folds checkpoint uncertainty ($\sigma_{\text{cp}}$) in quadrature; adds UAS Addendum V and control/checkpoint surveying Addendum II | Minimum `n = 30` checkpoints still leaves wide `[0.80, 1.34]×` `95 %` $\chi^2$ RMSE confidence bounds; omits explicit spatial correlation length ($L_{\text{corr}}$) adjustment unless added via [Ch. 53](../../fable/chapters/ch53-accuracy-assessment.md) |
| **USGS LiDAR Base Specification (2025 rev. A)** | Federal LAS 1.4 & QL0–QL3 benchmark | Rigorous class taxonomy (`Class 7/17/18/20/21`), quantitative smooth-surface **intra-swath `<= 6 cm`** and **inter-swath `<= 8 cm` `RMSDz`**, hydro-flattening (`>= 0.81 ha` / `2 acres`) | Tailored to high-altitude crewed aircraft; under-specifies UAS MEMS yaw drift during hovering, figure-8 alignment, and solid-state `905 nm` shrub merging ([Ch. 18](../../fable/chapters/ch18-topographic-lidar.md)) |
| **FAA `14 CFR Part 107` / LAANC / B4UFLY / `49 U.S.C. § 44807`** | U.S. airspace, Remote ID & heavy-lift governance | LAANC automates sub-minute controlled-airspace grid approvals; clear Part 89 Remote ID and `§ 107.9` clocks | `122 m` (`400 ft`) AGL limit clashes with `30 m` SRTM terrain-following DSM biases and synoptic barometric drift (`-8.32 m/hPa`); `>= 25 kg` (`55 lb`) `§ 44807` exemptions carry long lead times; B4UFLY omits landowner ROE and NPS/USFS land bans |
| **EASA `(EU) 2019/947` & SORA** | European Open (`120 m`) & Specific risk framework | Unified quantitative ground/air risk (`SAIL I–VI`) methodology portable across EASA member states | Heavy paperwork burden for BVLOS/urban Specific ops; national GEO-zones and `GDPR` privacy interpretations vary across borders |
| **`OpenDroneMap` (`ODM` / `WebODM`)** | Open-source PPK SfM & COG/DSM/DTM engine | Zero per-seat license fee, scriptable Docker CLI, `--rolling-shutter` compensation, direct COG export | `--dem-resolution` expects `cm/pixel` (trap for meter inputs); default auto-cal without `10–20°` obliques suffers radial doming; passing `--use-fixed-camera-params` turns self-cal off |
| **`COLMAP` / `GLOMAP` + `MicMac`** | Research-grade SfM & geometric photogrammetry | Transparent camera-parameter locking (`--refine_focal_length 0`), deterministic calibration workflows, `GLOMAP` global BA scaling | Minimal built-in vertical geoid/datum handling or hydro-flattening; requires external CRS wrapper scripts ([Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md)) |
| **`PDAL` + `lidR` + `xdem`** | Scriptable point-cloud & DEM forensics stack | Reproducible JSON pipelines (`ELM`/`SOR`/`SMRF`), native `COPC 1.0`, `xdem` Nuth & Kääb 3D co-registration & variogram tools | Steep CLI curve; automated `SMRF`/`CSF` thresholds misclassify walls, bridges (`Class 17`), and cliffs without tuned slope/window passes |
| **`RTKLIB` (`2.4.3` / `demo5`)** | Open-source multi-GNSS PPK solver & QA | Exposes cycle slips, `Q = 1..5` fix percentages, and F/B separation openly in `.pos` (check col `$10 = sdu`) | Does not perform tightly-coupled MEMS IMU RTS smoothing (`SBET`), requiring manual `igs20.atx` ANTEX setup and careful antenna HI entry |
| **`Agisoft Metashape Pro` & `Pix4Dmatic`** | Commercial GUI SfM + rolling-shutter suites | Fast GPU dense matching, intuitive marker/GCP marking, solid rolling-shutter & oblique optimization when properly constrained | Single-click self-calibration defaults tempt operators into nadir-only radial doming (`0.5–1.0 m` bow) and accidentally leaving checkpoints checked as control ([Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md), [Ch. 52](../../fable/chapters/ch52-ground-truth.md)) |
| **`CloudCompare`** | Interactive 3D point-cloud inspection & M3C2 | Rapid cross-sections across overlapping LiDAR swaths, strip-step checks, M3C2 surface diffing | GUI state is non-reproducible; must accept 64-bit Global Shift on UTM imports or `float32` truncation corrupts cm precision ([Ch. 47](../../fable/chapters/ch47-file-formats.md)) |

---

## 2. External Regulatory & Non-Handbook Source Register

All regulatory clocks, hazmat limits, workplace reporting thresholds, and insurance clauses used across `01`–`08` trace to the authoritative external issuers below (`fable/` and `gemini4/` do not prescribe local aviation/hazmat clocks).

| Issuer | Standard / Statute / Rule | Edition / Effective As-Of | Scope & Operational Threshold |
| :--- | :--- | :--- | :--- |
| **FAA (U.S. DOT)** | `14 CFR Part 107` (`§§ 107.9, 107.29, 107.31, 107.35, 107.39, 107.51`) & `Part 89` | Current as of `2026` | `< 25 kg` (`< 55 lb`), `122 m` (`400 ft AGL`), `>= 152 m (500 ft)` below / `>= 610 m (2,000 ft)` horiz clouds, `4.8 km (3 SM)` vis, Remote ID, `10`-day accident report (`AIS >= 3`, `LOC`, or `> $500` lesser repair/FMV) |
| **U.S. Congress / FAA** | `49 U.S.C. § 44807` & `14 CFR Part 47`; `FAA AC 70-1B` / `Form 7140-1` | Current as of `2026`; `AC 70-1B (2022)` | Heavy-lift UAS `>= 25 kg` (`55 lb`) exemptions + COA + registration; outdoor Class 3B/4 laser airspace evaluation |
| **FAA PackSafe / DOT PHMSA** | `FAA PackSafe` Li-ion rules; `49 CFR Parts 171–180` | Current as of `2026` | Passenger carry-on spare packs (`<= 100 Wh` OK; `100–160 Wh` max `2` packs, carry-on only); U.S. ground Class 9 rules for `> 300 Wh` heavy-lift packs |
| **NTSB** | `49 CFR Part 830` (`§§ 830.2, 830.5(a)(6), 830.10, 830.15`) | Amended `Aug 15, 2022` final rule | Immediate ROC call (`+1-844-373-9922`) on death, serious injury, substantial damage to airworthiness-certificated UAS, or `> $25,000` non-aircraft damage (lesser repair/FMV); `10`-day written Form `6120.1/2`; wreckage preservation |
| **EASA / EU** | `Reg. (EU) 2019/947` (`SORA`) & `Reg. (EU) 376/2014`; `GDPR (EU) 2016/679` | Current as of `2026` | Open (`120 m` cap) & Specific SORA (`SAIL I–VI`); `<= 72 hr` NAA occurrence report; `GDPR Art. 4(1)` PII scrubbing & `Art. 33` `72 hr` breach notice |
| **IATA** | Dangerous Goods Regulations (`DGR`), `PI 965 / 966 / 967`, `UN 3480/3481/3090/3091`, `UN 38.3` | **67th Ed. (eff. Jan 1, 2026)** | `UN 3480 PI 965` (`CAO <= 30 %` SoC); `UN 3481 PI 966` (`<= 30 %` SoC mandatory Jan 2026+); `PI 967` (`<= 30 %` rec.); printed `UN 38.3` & `SDS` |
| **OSHA (U.S. DOL)** | `29 CFR § 1904.39` | Current as of `2026` | Workplace fatality `<= 8 hr`; in-patient hospitalization, amputation, or **loss of an eye** `<= 24 hr` |
| **US NPS / USFS / FHWA** | `36 CFR § 1.5` (NPS), `36 CFR § 261.18` (USFS Wilderness); `ANSI Z136.1/Z136.6`; `ANSI/ISEA 107` / `MUTCD` | Current as of `2026` | Restricted park/wilderness UAS bans without SUP; Class 3B/4 NOHD/MPE eye safety; roadside GCP crew high-vis PPE & lane cones |
| **State Law / 4th Cir. / ISO** | *360 Virtual Drone v. Ritter* (`102 F.4th 263`, cert denied `Apr 2026`); `TX Ch. 423`, `FL § 934.50`; `ISO CG 00 01` Exclusion `(g)` | Verified `2024–2026` | PLS licensure enforcement on measurable aerial mapping; state drone privacy statutes; CGL aircraft/UAS exclusion requiring Aviation Hull/Liability/Floater/E&O |

---

## 3. Handbook Reference Cross-Walk (`fable/` & `gemini4/`)

| Checklist Topic | `fable/` Reference | `gemini4/` Reference |
| :--- | :--- | :--- |
| Horizontal datums, WGS 84 (`G2296`), GNSS, OPUS, `Kp` | [Ch. 8 Datums](../../fable/chapters/ch08-horizontal-datums.md), [Ch. 12 GNSS](../../fable/chapters/ch12-gnss.md) | [§3.2 Geoids](../../gemini4/book/ch-03/sec-03-02.md), [§5.2 GNSS Errors](../../gemini4/book/ch-05/sec-05-02.md) |
| MEMS IMU drift, figure-8, latency, `FRD/NED` vs `ENU` | [Ch. 13 IMU/INS](../../fable/chapters/ch13-imu-ins.md) | [Notation & Symbols §1](../../gemini4/book/00-front-matter/notation-and-symbols.md), [§5.3 INS](../../gemini4/book/ch-05/sec-05-03.md) |
| UAS airframes, wind tilt, isolators, hover power | [Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md) | [§7.3 UAS Platforms & Error Budget](../../gemini4/book/ch-07/sec-07-03.md) |
| UAS LiDAR returns, canopy penetration, marsh pitfalls | [Ch. 18 Topographic LiDAR](../../fable/chapters/ch18-topographic-lidar.md) | [§9.1 Range Physics](../../gemini4/book/ch-09/sec-09-01.md), [§9.6 LiDAR Error](../../gemini4/book/ch-09/sec-09-06.md), [§9.7 Canopy & Marsh](../../gemini4/book/ch-09/sec-09-07.md) |
| SfM doming, rolling shutter, NDWI water-glint | [Ch. 22 Photogrammetry/SfM](../../fable/chapters/ch22-photogrammetry-sfm.md) | [§8.2 SfM Doming & Mitigation](../../gemini4/book/ch-08/sec-08-02.md) |
| Benchmarks, targets (`5–10 GSD`), 4-question wall | [Ch. 25 Calibration](../../fable/chapters/ch25-calibration-infrastructure.md), [Ch. 52 Ground Truth](../../fable/chapters/ch52-ground-truth.md) | [§12.3 GCP vs. CP](../../gemini4/book/ch-12/sec-12-03.md) |
| Survey overlap, sun angle, transient masks, cost | [Ch. 26 Planning](../../fable/chapters/ch26-survey-planning.md), [Ch. 27 Transients](../../fable/chapters/ch27-moving-and-transient-objects.md), [Ch. 28 Cost](../../fable/chapters/ch28-reducing-cost.md) | [§13.1 Survey Design](../../gemini4/book/ch-13/sec-13-01.md), [§27.4 Cost](../../gemini4/book/ch-27/sec-27-04.md) |
| Noise flagging, DTM bridges, water, formats & archiving | [Ch. 30 Classification](../../fable/chapters/ch30-point-cloud-classification.md), [Ch. 32 DTM](../../fable/chapters/ch32-dsm-to-dtm.md), [Ch. 34 Water](../../fable/chapters/ch34-water-in-dems.md), [Ch. 47 Formats](../../fable/chapters/ch47-file-formats.md), [Ch. 50 Archiving & Provenance](../../fable/chapters/ch50-archiving-and-provenance.md) | [§19.1 Formats](../../gemini4/book/ch-19/sec-19-01.md), [§32.2 Time Sync](../../gemini4/book/ch-32/sec-32-02.md) |
| ASPRS Ed. 2 stats, Nuth–Kääb, forensics, variograms | [Ch. 53 Accuracy](../../fable/chapters/ch53-accuracy-assessment.md), [Ch. 54 Evaluating Data](../../fable/chapters/ch54-evaluating-others-data.md), [Ch. 56 Case Files](../../fable/chapters/ch56-case-files.md) | [§14.2 TPU](../../gemini4/book/ch-14/sec-14-02.md), [§14.3 FFT Forensics](../../gemini4/book/ch-14/sec-14-03.md), [§14.5 Nuth–Kääb & NMAD](../../gemini4/book/ch-14/sec-14-05.md), [§33.1 Variograms](../../gemini4/book/ch-33/sec-33-01.md) |
| Legal (*Ritter*), CARE-OCAP®, privacy, export/cyber | [Ch. 68 Legal](../../fable/chapters/ch68-legal-issues.md), [Ch. 69 Security/Privacy](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md) | [§27.1 Legal](../../gemini4/book/ch-27/sec-27-01.md), [§27.2 Privacy](../../gemini4/book/ch-27/sec-27-02.md), [§27.3 Export & Security](../../gemini4/book/ch-27/sec-27-03.md) |

---

## 4. Copy-Ready Field Templates (Printable / Offline Bundle)

### Template A — LiPo Battery Cycle, SoC & `UN 3480/3481` Shipping Log

```markdown
# UAS LiPo Battery Cycle & Hazmat Transport Ledger (IATA DGR 67th Ed. Jan 2026)
Airframe / Battery Series: ______________________  Nominal Cell Count / Wh: ____ S / _____ Wh
UN Classification: [ ] UN 3480 PI 965 (Cargo-Only <=30% SoC)  [ ] UN 3481 PI 966 (<=30% SoC Jan 2026+)  [ ] UN 3481 PI 967
UN 38.3 Test Summary & SDS on File: [ ] Yes  Quarantine Rule: Discard if >0.05 V cell delta, puffing, or >150-200 cycles

| Pack ID | Date (UTC) | Pre-Flight V/cell | Sortie ID | Min Land V/cell | Max Temp (deg C) | Internal Res (mOhm) | Storage/Ship State (~3.8V / <=30% SoC) | Initials |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| BAT-01A | YYYY-MM-DD | 4.20 V | S-01 | 3.71 V | 42 C | 3.2 mOhm | [ ] 3.82 V storage  [ ] <=30% air | _____ |
| BAT-01B | YYYY-MM-DD | 4.20 V | S-01 | 3.70 V | 41 C | 3.4 mOhm | [ ] 3.82 V storage  [ ] <=30% air | _____ |
```

### Template B — Part 107 / `§ 44807` / SORA Pre-Flight Safety & Density-Altitude Card

```markdown
# Pre-Flight Safety, Airspace & Density-Altitude Check Card
Sortie ID: ____________ Date/UTC: ____________ Tail/Reg #: ____________ Remote PIC: ____________ VO(s): ____________
1. Airspace & Clearances: [ ] LAANC/DroneZone/COA Active  [ ] B4UFLY/NOTAM/TFR Clear  [ ] Remote ID RF Verified  [ ] ROE Signed
2. Statutory Ops Mode: [ ] Part 107 (<25 kg, 122 m / 400 ft) [ ] Sec 44807 (>=25 kg) [ ] EASA SORA (120 m) [ ] Waivers: _______
3. Terrain-Following & Ceiling Check (<=120 m Plan Clears Both FAA 122 m & EASA 120 m):
   - Baro QNH / Temp: ______ hPa / _____ deg C -> Density Alt: ______ m | Max Plan AGL: _____ m (local DTM verified)
   - RTH Alt Set: _____ m (>=20 m above tallest tree/tower AND <=120 m AGL) | Wind / Gust (anemometer): ____ / ____ m/s (<8-10 m/s)
   - Sun Elev: ____ deg (>30 deg) | GNSS SVs / PDOP: ____ / ____ (<=3.0) | Kp Index: ___ (<5) | Wildlife Buffer Clear: [ ] Yes
4. Payload & Hardware: [ ] Isolators Intact (no GNSS on soft mount)  [ ] Lever Arms / Hot-Shoe Checked  [ ] Figure-8 Planned
5. Field Crew Briefed: LZ Exclusion >=20 m [ ] | Lost-Link Action Briefed [ ] | Laminated 06 Card & Water/AVD Staged [ ]
PIC Sign-Off: ____________________  VO Sign-Off: ____________________  Verifier: ____________________
```

### Template C — Strictly Split Control (`base_and_gcps.csv`) vs. Withheld Checkpoints (`cps_withheld.csv`)

Maintain these as **two separate files on disk** — NEVER feed `cps_withheld.csv` into SfM optimization, LiDAR strip adjustment, or vertical shift calibration (`03` Gate). Note `07` reads `cps_withheld.csv` named headers directly.

```csv
# File 1: base_and_gcps.csv (Base Stations + Optimization Control Only)
Point_ID,Role,Stratum,Method,Target_Type_Size_cm,Vertical_HI_m,Slant_HI_m,Easting_m,Northing_m,Ortho_Elev_m,Geoid_Model,Sigma_V_m,Photo_Start_ID,Photo_End_ID,Observer_Verifier
BASE-01,BASE,Open,OPUS_4h_Static,Tripod_Fixed,1.800,1.834,542110.214,4812090.551,142.318,GEOID18,0.008,IMG_001,IMG_002,JS/KL
GCP-01,GCP,Bare_Edge,RTN_180s_Dual,Checker_30cm_Matte,2.000,N/A,541850.112,4812405.882,168.412,GEOID18,0.018,IMG_003,IMG_004,JS/KL
GCP-02,GCP,Bare_Ridge,RTN_180s_Dual,Checker_30cm_Matte,2.000,N/A,542810.440,4812690.120,214.905,GEOID18,0.018,IMG_005,IMG_006,JS/KL
```

```csv
# File 2: cps_withheld.csv (Strictly Withheld Validation Checkpoints — Schema Matched to 07 QC Script)
Point_ID,Stratum,Method,Target_Type_Size_cm,Easting_m,Northing_m,Ortho_Elev_m,Geoid_Model,Sigma_V_m,Photo_Start_ID,Photo_End_ID,Observer_Verifier
CP-01,NVA_Asphalt,RTN_180s_IndepBase,50pct_Diff_LiDAR_120cm,542390.440,4811920.110,139.004,GEOID18,0.021,IMG_007,IMG_008,MR/KL
CP-31,VVA_Forest,Closed_Total_Station,Bare_Ground_Prism,542612.885,4812288.419,155.782,GEOID18,0.008,IMG_067,IMG_068,MR/KL
```

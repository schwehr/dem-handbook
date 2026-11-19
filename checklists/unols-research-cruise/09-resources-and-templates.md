# UNOLS Research Cruise — Authoritative Resources Critique & Field Templates

Operational reference guide and copy-ready shipboard forms supporting the `unols-research-cruise` checklist suite (`00` through `08`). All templates in Section 4 are formatted for direct printing into the Main-Lab Watch Binder so bridge and watchstanders remain self-sufficient with zero internet connectivity.

---

## 1. Critical Evaluation of Authoritative External Resources

Use the matrix below to pair external manuals and software suites with the exact technical cross-references required to eliminate silent sign, uncertainty, or governance blind spots.

| Authoritative Resource | Scope & Operational Role | Primary Strengths | Critical Blind Spots & Failure Modes | Companion Handbook Reference |
| :--- | :--- | :--- | :--- | :--- |
| **UNOLS `RVSS` (11th Ed., Nov 2021 rev. 2023) & `MFP`** | Fleetwide safety standards, hoisting/wire SWL, `SME` scheduling, hazmat, medical & `PCAR` | Binding vessel/deck safety design factor (`5.0` App. A default wire/rope SWL; reduced `2.5/2.0/1.5` under tension monitoring, `OHDD` shock loads), unified `MFP` scheduling, formal `Master` authority & `PCAR` loop | Silent on acoustic `TPU` budgets, sound-speed ray bending, coordinate sign polarity, `ERS` geoids, and post-cruise demob data cleaning | [ch16-platforms.md](../../fable/chapters/ch16-platforms.md) |
| **UNOLS Multibeam Advisory Committee (`MAC`) Wiki & `SAT`/`QAT` Tools** | Vessel-specific multibeam calibration, self-noise, extinction & offset verification | Empirically grounded `VSR` offset checks, cavitation/RPM curves, `4-step` patch-test SOPs, and `SVS` validation routines across UNOLS fleet | Shipboard-hardware focused (`SIS`/`Qimera`); limited coverage of `PPK`/`PPP-AR` `ERS` reduction, `VDatum` `TSS` sign traps, `IHO S-102` encryption, or `UNCLOS Art. 76` | [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md) |
| **Rolling Deck to Repository (`R2R`)** | Post-cruise shipboard operator breakout, metadata QA, DOI minting & `NCEI` archival ingestion | Standardizes vessel-level instrument stream separation, assigns permanent cruise DOIs, and automates NCEI/DCDB ingest after the operator transmits raw distributions (paired with Phase `07` custody gate before gangway exit!) | Archives *raw* shipboard streams and environmental logs—does **not** perform `CUBE` cleaning, delayed-heave `SBET`, `ERS` datum reduction, or `HydrOffice` QC | [ch50-archiving-and-provenance.md](../../fable/chapters/ch50-archiving-and-provenance.md) |
| **NOAA Ocean Exploration (`OE`) *Deepwater Exploration Mapping Procedures Manual*** | Blue-water (`> 200 m`) continuous mapping, `XBT`/`SVP` cadence & `Seabed 2030` transit SOPs | Highly practical `24/7` watchstander workflows, `Qimera`/`SIS` step-by-step operations, clean `NCEI`/`DCDB` delivery templates | Blue-water U.S.-centric scope; under-specifies shallow shelf `S-44 Order 1a` object detection, `Tuck/Barrass` squat, pole `VIV` Strouhal locks, and `White-Ribbon` coastal ties | [sec-24-01.md](../../gemini4/book/ch-24/sec-24-01.md) |
| **`MB-System` / `Kluster` / `HydrOffice QC Tools` vs. Commercial (`Qimera`, `CARIS HIPS`, `SIS`)** | Open-source CLI bathymetry processing & QC vs vendor real-time/GUI suites | `MB-System`/`Kluster` offer transparent math (`mbgrid`, `mbnavadjust`), scriptable `Git`/`SHA-256` provenance, and zero license lock; `HydrOffice` automates `S-44`/`HSSD` QA | Commercial GUIs enable fast `.kmall`/`WCI` visualization but hide default CUBE/heave settings; open tools require deeper CLI expertise for vendor dual-swath edge datagrams | [appendix-f-software-index.md](../../fable/appendices/appendix-f-software-index.md) |
| **IHO `S-44 Ed. 6.2.0` (Oct 2024; core Table 1 `a`/`b` unchanged from `Ed. 6.1.0`, adding `§3.8`), `C-13`, `S-102 Ed. 3.0.0`, `S-158:102` & NOAA `HSSD` (2024 restructured ed.) / `FPM`** | Governing hydrographic uncertainty orders, manuals, and machine-validated HDF5 schemas | Rigorous mathematical `TVU`/`THU` limits, feature detection matrices, seabed characteristics (`§3.8`), and automated schema checks (`S-158:102`) across modern S-100 products | Fragmented across sign conventions (`BAG FSD 2.0.1` `+z` up vs `S-102` `+d` down), `float32` UTM quantization traps, and complex datum `SEP` notation without unified practitioner guides | [appendix-d-standards-index.md](../../fable/appendices/appendix-d-standards-index.md) |

---

## 2. External Statutory, Safety & Operational Source Register

Statutory clocks, safety design factors, environmental rules, and UNOLS fleet procedures are curated from active primary authorities outside the handbook text (**edition and status as of 2026**; confirm operator/flag-state updates prior to sailing):

| Standard / Regulation / Program | Issuing Authority, Edition & As-Of Status | Governing Scope & Jurisdictional Applicability | Where Enforced |
| :--- | :--- | :--- | :--- |
| **UNOLS `RVSS` (App. A & B)** | UNOLS *Research Vessel Safety Standards*, **11th Ed. (Nov 2021, rev. 2023)** | Fleet safety standard (not statute); Master authority, App. A rope/wire safety factor `5.0` (reduced `2.5/2.0/1.5` under monitoring), App. B `OHDD` shock loads | Phases `02`, `03`, `06`, `07` |
| **UNOLS `MFP`, `PCAR` & Medical Clearance** | UNOLS Marine Facilities Planning (`mfp.us`, active fleet scheduling portal, 2026) | Indicative `SME` submission & annual scheduling windows, `MFP` Medical History / Fit-for-Duty clearance (`>= 30–60 d` pre-sail), hazmat, independent `PCAR`s | Phases `01`, `02`, `07` |
| **NSF Data & Custody Policy / `R2R`** | National Science Foundation (`NSF 24-1` Data Management / Division of Ocean Sciences) & `R2R` (2026) | `DMP` enforcement, raw stream post-cruise ingestion to `NCEI`/`DCDB` via `R2R` breakout (paired with Phase `07` pre-disembark custody gate) | Phases `01`, `07`, `08` |
| **Marine Casualty & Pollution (`CG-2692`, `SMI`, `NRC`)** | U.S. Coast Guard (`46 CFR §§ 4.05-1`, `4.05-10`, `Subpart 4.06`; `33 CFR § 153.203`, active 2026) | **U.S.-flag / U.S. waters** (use flag/coastal MRCC abroad): immediate verbal + `5 d` `CG-2692` (`> $75k` damage, beyond first aid), `2 h`/`32 h` SMI testing, immediate `NRC` | Phases `02`, `06` |
| **STCW Watchkeeping Rest** | USCG / IMO STCW (`46 CFR § 15.1111`, active 2026) | `>= 10 h` rest per `24 h` (`>= 6 h` block, `<= 14 h` gap) & `>= 77 h` per `7 d` for bridge/engineering crew; science watch fatigue cap | Phases `02`, `06`, `08` |
| **OSHA Injury Reporting** | U.S. Dept. of Labor (`29 CFR § 1904.39`, active 2026) | **U.S. contractor / non-seafarer science staff:** `8 h` fatality / `24 h` inpatient hospitalization, amputation, or eye loss | Phases `02`, `06` |
| **`MMPA`/`ESA` (`NMFS 2018`) & `JNCC (2017)`** | NOAA NMFS *Technical Guidance* (2018 rev. 2024) & UK JNCC *Seismic/Acoustic Guidelines* (2017) | `IHA`/`LOA`/`BiOp` permit zones, `JNCC` `60 min` visual pre-watch (`> 200 m` depth) vs `30 min` (`<= 200 m`), `20–40 min` soft-start, `90 d` MMO closeout | Phases `02`, `07`, `08` |
| **Lithium Batteries (`IATA DGR`, `IMDG`, `49 CFR`)** | IATA **DGR 67th Ed. (eff. Jan 1, 2026)**, **IMO IMDG Code**, PHMSA **`49 CFR Parts 171–180`** | Mandatory `<= 30 % SoC` air-freight (`UN 3480 PI965 CAO` & `UN 3481 PI966 > 2.7 Wh`), `UN 3090 CAO / 3091`, `UN 38.3` & `SDS` | Phases `02`, `07` |
| **Export Controls (`ITAR` / `EAR`) & `ATA Carnet`** | U.S. Dept. of State (`22 CFR 120–130`), Commerce BIS (`15 CFR 730–774`), ICC `ATA Carnet` (2026) | `ECCN 6A001/7A003/7A005/8A001` screening, foreign-national Deemed Export clearance, temporary customs Carnet stamping | Phases `02`, `07` |
| **UNCLOS Part XIII/76, `UNESCO 2001` & `CARE/OCAP®`** | UN `1982 UNCLOS` (`Art. 18(2), 76, 245–249`), `RATS`, `UNESCO 2001` UCH, GIDA `CARE` / FNIGC `OCAP®` | `>= 7 mo` `RATS` MSR filing, `Art. 249` preliminary report (`<= 30 d`), wreck/cultural protection, Indigenous data sovereignty & escrow | Phases `01`, `02`, `06`, `07` |
| **Marine Insurance & Liability Standards** | Institutional Risk Mgmt / Marine Underwriting (`H&M`, `P&I`, `Jones Act/MEL`, `MLC 2006`, `USL&H`, `FVWC`, `C&V`) | Vessel `H&M`/`P&I` + `Jones Act`/`MLC 2006` + `USL&H` + `FVWC` + `IWL` vs PI Scheduled Subsea Floater (`C&V` appraisal) + `E&O` | Phases `02`, `06`, `08` |
| **Hydrographic & Continental-Shelf Standards (`IHO S-44`, `S-102`, `TALOS C-51`)** | International Hydrographic Organization (`IHO S-44 Ed. 6.2.0` Oct 2024 [core `a`/`b` unchanged from `Ed. 6.1.0` + `§3.8`]; `S-102 Ed. 3.0.0` Dec 2024; `C-51 Ed. 6.0.0` 2020) | Mandatory `TVU`/`THU` order compliance, seabed characteristics (`§3.8`), `+d` S-102 schema validation (`S-158:102`), & Art. 76 CLCS legal traceability | Phases `01`, `04`, `07`, `08` |

---

## 3. Handbook & Cross-Modality Reference Crosswalk

- **Standards, Public Grids & Software Indexes:** [appendix-d-standards-index.md](../../fable/appendices/appendix-d-standards-index.md) | [appendix-e-public-products-tables.md](../../fable/appendices/appendix-e-public-products-tables.md) | [appendix-f-software-index.md](../../fable/appendices/appendix-f-software-index.md)
- **Geodesy, Ray-Tracing, Vessels & QA Chapters:** [ch08-horizontal-datums.md](../../fable/chapters/ch08-horizontal-datums.md) | [ch09-vertical-datums.md](../../fable/chapters/ch09-vertical-datums.md) | [ch47-file-formats.md](../../fable/chapters/ch47-file-formats.md) | [ch49-metadata.md](../../fable/chapters/ch49-metadata.md) | [ch52-ground-truth.md](../../fable/chapters/ch52-ground-truth.md) | [ch62-navigation-and-charting.md](../../fable/chapters/ch62-navigation-and-charting.md)
- **Technical Manual Deep-Dives:** [TOC.md](../../gemini4/TOC.md) | [sec-03-02.md](../../gemini4/book/ch-03/sec-03-02.md) | [sec-05-03.md](../../gemini4/book/ch-05/sec-05-03.md) | [sec-10-04.md](../../gemini4/book/ch-10/sec-10-04.md) | [sec-13-01.md](../../gemini4/book/ch-13/sec-13-01.md) | [sec-13-03.md](../../gemini4/book/ch-13/sec-13-03.md) | [sec-13-05.md](../../gemini4/book/ch-13/sec-13-05.md) | [sec-14-05.md](../../gemini4/book/ch-14/sec-14-05.md) | [sec-19-01.md](../../gemini4/book/ch-19/sec-19-01.md) | [sec-24-01.md](../../gemini4/book/ch-24/sec-24-01.md) | [sec-28-01.md](../../gemini4/book/ch-28/sec-28-01.md) | [sec-33-01.md](../../gemini4/book/ch-33/sec-33-01.md)
- **Cross-Modality Shared Templates:** [template-project-header.md](../_shared/template-project-header.md) | [template-error-budget.md](../_shared/template-error-budget.md) | [template-cost-ledger.md](../_shared/template-cost-ledger.md) | [template-insurance-coi.md](../_shared/template-insurance-coi.md) | [template-accident-card.md](../_shared/template-accident-card.md) | [template-aar-retrospective.md](../_shared/template-aar-retrospective.md) | [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md)

---

## 4. Copy-Ready Shipboard Field Logs

### Template 4A — UNOLS 24/7 Watchstander & Bridge/Lab Shift Log

```markdown
# UNOLS Watchstander Shift Log (Print & Keep at Main-Lab MBES Console)
Cruise ID: ______________________   Vessel: ______________________   UTC Date: YYYY-MM-DD
Shift Window (UTC): [ ] 00:00-08:00   [ ] 08:00-16:00   [ ] 16:00-24:00   (or 4/8 Watch: ________)
Incoming Watch Lead / Tech: _______________________   Outgoing Initials & Turnover Time (UTC): ________

1. Pre-Relief 15-Min Handover Check:
   [ ] Bridge advised of relief & upcoming line/turn changes (Officer of the Watch: ______________)
   [ ] POS MV / Seapath: GAMS = [READY/DROP]  1PPS = [LOCKED/FAULT]  .000 Raw Recording = [ON]
   [ ] K-Sync / Sensors Active: [ ] MBES  [ ] SBP  [ ] WCI  [ ] ADCP  [ ] MVP  [ ] MMO Watch (Daylight)
   [ ] Disk Free Space: Acq PC ______ %   Ship NAS RAID ______ %   NVMe Copy 2 ______ %   LTO-9 ______

2. Underway Watch Event Table (Log every line start/end, SVP cast, bubble intervention, DTON, or GNSS alert):
| UTC Time | Line / Box ID | Speed m/s (kn) / RPM | Depth (m) | SVS - Cast(0) (m/s) | Live TPU / Swath State | Actions / Bubble / WCI / EW Notes | Init |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| ____:____ | ____________ | ____ (____) / ____ | ________ | ________ (Trigger >1.5) | [G / Y / R] Dropout ___% | ______________________________ | ____ |
| ____:____ | ____________ | ____ (____) / ____ | ________ | ________ (Trigger >1.5) | [G / Y / R] Dropout ___% | ______________________________ | ____ |
| ____:____ | ____________ | ____ (____) / ____ | ________ | ________ (Trigger >1.5) | [G / Y / R] Dropout ___% | ______________________________ | ____ |
| ____:____ | ____________ | ____ (____) / ____ | ________ | ________ (Trigger >1.5) | [G / Y / R] Dropout ___% | ______________________________ | ____ |

3. Watch End & Backup Gate:
   [ ] Nightly 24h MB-System / Qimera Crossline QA run?  Result: median bias ______ m, NMAD ______ m, P95 ______ m
   [ ] Any Shelf Shoal / DTON Observed? [ ] NO  [ ] YES -> Transmitted to Master / Hydro Office / NAVAREA at UTC ________
   [ ] 3-2-1 SHA-256 Backup Verified (Copy 1 NAS + Copy 2 SSD + Copy 3 LTO/Vault): Pass [ ]  SHA mismatches = ___
```

### Template 4B — MVP / CTD / XBT Sound-Velocity & SVS Cross-Check Log

```markdown
# UNOLS Sound-Velocity Profile (SVP) & Surface SVS Cross-Check Log
Cruise ID: ______________________   Vessel: ______________________   Surface SVS Model/SN: __________________
Trigger Rule: Deploy MVP or XBT immediately if |c_SVS - c_cast(0)| > 1.5 m/s OR outer-beam curl > 0.25% depth.

| Cast # | UTC Date/Time | Lat / Lon (DD) | Sensor (MVP/CTD/XBT) & SN | Speed m/s (kn) | Water Depth (m) | Max Cast Depth (m) | WOA Splice Used? | c_SVS vs c_Cast(0) (m/s) | Outer-Beam Curl Pre/Post (% d) | Applied Filename (.asvp/.svp) & Operator |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 001 | ________ | ________ / ________ | ________________ | ____ (____) | ______ | ______ | [Y/N] _____ m | ____ vs ____ (d=____) | ____% -> ____% | ______________________ (____) |
| 002 | ________ | ________ / ________ | ________________ | ____ (____) | ______ | ______ | [Y/N] _____ m | ____ vs ____ (d=____) | ____% -> ____% | ______________________ (____) |
| 003 | ________ | ________ / ________ | ________________ | ____ (____) | ______ | ______ | [Y/N] _____ m | ____ vs ____ (d=____) | ____% -> ____% | ______________________ (____) |
| 004 | ________ | ________ / ________ | ________________ | ____ (____) | ______ | ______ | [Y/N] _____ m | ____ vs ____ (d=____) | ____% -> ____% | ______________________ (____) |

Sound Speed Equation Match Check: [ ] TEOS-10 / UNESCO Chen-Millero / Del Grosso verified identical across MVP/CTD/SIS.
Deck Pressure Tare Confirmed (0.0 dbar at deck prior to MVP/CTD launch): Operator Initials ______   Date ______
```

### Template 4C — Static Draft, Fuel/Water Burn & Dynamic Squat Ledger

```markdown
# UNOLS Vessel Static Draft, Density, Fuel/Water Burn & Squat Ledger
Cruise ID: ______________________   Vessel: ______________________   Waterplane Area A_WP (m^2): __________
Immersion Rate TPC (tonnes/cm): ________   Offset-Survey Datum-to-Draft-Mark Z_offset (m): ______________

Waterline Sign Convention (MANDATORY):
  z_waterline(t) = z_static(t_0) - dz_fuel + dz_rho + S_squat  [+d POSITIVE DOWNWARD draft, m, per Gemini4 Sec. 7.8]
  Software Entry Warning: Kongsberg SIS "WL" uses Vessel NED (+Z downward from origin); Qimera/CARIS track vessel
  waterline sign explicitly—verify positive rise/sinkage sign on first day-to-day overlap check!
  Sign Reminders: Fuel/water burn REDUCES draft (dz_fuel > 0 rise -> depth reads artificially deep unless updated!).
                  Dynamic squat INCREASES draft underway (S_squat > 0 sink -> unmodeled squat injects shoal bias!).

PART 1: PIER STATIC DRAFT & TANK CLOSURE (Measure at Departure t_0 AND Demobilization t_end)
| State | UTC Date/Time | Port/Stbd Fwd (m) | Port/Stbd Mid (m) | Port/Stbd Aft (m) | Water Density (kg/m^3) | Salinity Shift dz_rho (m) | Fuel + FW + Ballast Total (t) | Net z_waterline Draft (m) | Chief Mate & Lead Initials |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Sail t_0 | ____________ | ____ / ____ | ____ / ____ | ____ / ____ | ________ | ________ | __________ t | ________ m | ________ / ________ |
| Mid-Leg | ____________ | ____ / ____ | ____ / ____ | ____ / ____ | ________ | ________ | __________ t | ________ m | ________ / ________ |
| Demob t_end | ____________ | ____ / ____ | ____ / ____ | ____ / ____ | ________ | ________ | __________ t | ________ m | ________ / ________ |

PART 2: DAILY FUEL BURN & TUCK / BARRASS DYNAMIC SQUAT TABLE
| Day / UTC | Daily Fuel+FW Delta dm (t) | Cumulative Buoyancy Rise dz_fuel (m) | Speed m/s (kn) | Min Water Depth h (m) | Tuck / Barrass Squat S_squat (m) | Net Draft z_waterline(t) (m) | Software WL Entry & Init |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Day __ | __________ t | -________ m (rise) | ____ (____) | ______ m | +________ m (sink) | ________ m | [Y/N] ________ (____) |
| Day __ | __________ t | -________ m (rise) | ____ (____) | ______ m | +________ m (sink) | ________ m | [Y/N] ________ (____) |
| Day __ | __________ t | -________ m (rise) | ____ (____) | ______ m | +________ m (sink) | ________ m | [Y/N] ________ (____) |
```

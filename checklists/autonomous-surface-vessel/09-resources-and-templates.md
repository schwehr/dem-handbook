# Autonomous Surface Vessel (ASV / USV) — Phase 09: Authoritative Resources & Copy-Ready Templates

> **Modality:** `autonomous-surface-vessel` | **Role:** Critical literature review + printable field/ROC blank logs  
> **Companion Docs:** [Phase 00 Overview](./00-README-and-signoff.md) · [`_shared/` Templates](../_shared/template-project-header.md)

This file pairs an unvarnished practitioner critique (**"How Good Are They?"**) of the primary regulatory, hydrographic, and software standards governing autonomous surface vessels with **copy-ready blank operational templates** for offline ROC watch desks and chase boats.

---

## 1. Critical Resource Evaluation ("How Good Are They?")

### A. Maritime Autonomy & Regulatory Governance (CONOPS, COLREGS, USCG)

1. **USV Operational CONOPS Doctrine (Project / Industry Practice Modeled on NOAA Uncrewed Surface Ops)**
   - *Strengths:* Separates **Attended**, **Monitored**, and **Over-The-Horizon (OTH)** supervision tiers, enforces single-point helm authority between mothership/ROC/chase boat, adopts 4-hour bridge/ROC watch rotations, and aligns DTON triage workflows with crewed hydrographic ships. (Tiers and shift durations here are operational rules adopted in project CONOPS rather than a single numbered federal statute.)
   - *Gaps & Operational Friction:* Agency uncrewed-vessel doctrine centers on larger Saildrone, DriX, and research-ship force-multiplier deployments; commercial crews launching **1–4 m micro-catamarans** off beaches/ramps still must define explicit dockside e-stop distances and Sector-specific COTP agreements locally.
   - *How to Use Here:* Enforce the **3-tier supervision polygon** and **4-hour watch handoff rigor** in Phases 01–05, paired with hardware e-stop + chase-boat interception gates for small craft.

2. **International COLREGS (1972 / 33 CFR Part 81), IMO MASS Code & USCG Work Instruction 5P-WI-002(1)**
   - *Strengths:* Binding legal baseline on navigable waters. Rule 5 (*Look-Out*), Rule 6 (*Safe Speed*), Rule 7 (*Risk of Collision*), Rule 8 (*Action to Avoid Collision*), Rule 23 (*Lights*), and **Rule 27(b)/(c)/(d)** (*Restricted in Ability to Maneuver* / *Towing* / *Dredging & Underwater Ops*) keep autonomy engineers grounded in seamanship rather than software optimism. **USCG 5P-WI-002(1)** (*Oversight of Unmanned, Autonomous, and Remote-Control Operations*) gives Sector Inspectors and COTPs a structured framework for reviewing USV navigation safety, LNM wording, and loss-of-control mitigation.
   - *Gaps & Operational Friction:* COLREGS assumes a human lookout and sound watch on deck; the non-mandatory **IMO MASS (Maritime Autonomous Surface Ships) Code** adopted at **MSC 111 (May 2026)** targets mandatory adoption around **2032** specifically for SOLAS cargo ships $\ge 500\text{ GT}$ and does not automatically govern small uncrewed survey craft. Small USVs remain vulnerable to **un-AIS'd kayaks, recreational fishers, and drifting crab buoys** in Rule 5/7 compliance. Never claim Rule 27(b) RAM as an excuse to force large ships to maneuver late—enforce Rule 8/17 early avoidance in ROC SOPs.
   - *Crosswalk:* [Ch. 68 Legal Issues](../../fable/chapters/ch68-legal-issues.md) · [Sec. 27.1 Legal Issues](../../gemini4/book/ch-27/sec-27-01.md)

### B. Hydrographic Standards, Datums & File Specifications

3. **IHO S-44 Ed. 6.2.0 (Oct 2024; core Table 1 TVU/THU $a/b$ values unchanged from Ed. 6.1.0, adding §3.8 seabed characteristics), C-13 *Manual on Hydrography*, S-102 Ed. 3.0.0 & S-158:102**
   - *Strengths:* S-44 Ed. 6.2.0 (`fable/` cites the Ed. 6.1.0 baseline) is the authoritative international baseline for bathymetric uncertainty ($TVU_{95\%}$, $THU_{95\%}$), feature detection, seabed characteristics (§3.8), and bathymetric coverage orders (`Exclusive` through `Order 2`). **S-102 Ed. 3.0.0** (Dec 2024, with **S-158:102** validation checks) unifies gridded bathymetry, uncertainty coverage, and S-100 encryption/portrayal alongside S-101 ENCs and S-104 water levels.
   - *Implementation Pitfalls:* S-44 leaves crossline percentages and separation-model validation up to the hydrographic authority; if a processor omits $\sigma_{\text{SEP}}$ from total TVU, an `Order 1a` compliance check becomes artificially optimistic. Furthermore, S-102 stores **positive-down depth ($+d \downarrow$, `verticalCS = 6498`)** whereas BAG 2.0.1 and coastal topobathy DEMs store **positive-up elevation ($+z \uparrow$)**—making explicit sign checks mandatory in automated pipelines.
   - *Crosswalk:* [Appendix D Standards Index](../../fable/appendices/appendix-d-standards-index.md) · [Ch. 47 File Formats](../../fable/chapters/ch47-file-formats.md) · [Ch. 70 Specifications](../../fable/chapters/ch70-specifications-guided-tour.md)

4. **NOAA Hydrographic Surveys Specifications and Deliverables (HSSD, 2024 edition, restructured; annual updates) & Field Procedures Manual (FPM)**
   - *Strengths:* Unmatched operational detail—codifies 200 % Object Detection vs. 100 % Complete coverage, crossline proportions ($\ge 4\%$), Variable-Resolution (VR) BAG brackets, CUBE + **Designated Soundings** rules, immediate / 24-hour **DTON** S-57 `.000` deliverables, and strict vessel/sensor patch-test procedures.
   - *Gaps & Operational Friction:* Heavy NOAA/CARIS institutional heritage occasionally lags open-source cloud-native workflows (`Kluster`, `Zarr`, `COPC`, `COG`), and strict Object Detection density can be slow or impossible in steep surf with lightweight micro-USVs unless paired with high-tide/low-tide multi-modal lidar.
   - *Crosswalk:* [Sec. 24.1 Survey Guide Documents (HSSD / FPM)](../../gemini4/book/ch-24/sec-24-01.md)

5. **USACE EM 1110-2-1003 (*Hydrographic Surveying*)**
   - *Strengths:* Essential for U.S. dredging payment volumes, channel condition surveys, tight navigation tolerances (**$\pm 0.15\text{ m}$ hard-bottom / $\pm 0.30\text{ m}$ soft-bottom at 95 %**; **$2\text{–}5\text{ m}$ horizontal tolerance**), bar-check / lead-line verification, and levee/channel cross-section conventions.
   - *Gaps & Operational Friction:* Legacy edition still mixes **U.S. Survey Feet** (`1200/3937 m`) with SI meters, pre-dates modern USV endurance/ERS workflows in several chapters, and can under-specify multi-beam outer-beam refraction checks relative to HSSD. Always normalize internal processing to SI meters (`float64`) and verify State Plane Survey Foot vs. International Foot explicitly on USACE contracts.
   - *Crosswalk:* [Ch. 66 Coastal, Rivers & Dredging](../../fable/chapters/ch66-coastal-marine-polar-lakes-rivers.md) · [Ch. 56 Units Case Files](../../fable/chapters/ch56-case-files.md)

### C. Open & Commercial Hydrographic Software Stack

6. **Open-Source Processing & QC (`HSTB Kluster`, `HydrOffice QC Tools / Sound Speed Manager`, `MB-System`)**
   - *Strengths:* `Kluster` provides transparent, Python-scriptable `.kmall`/`.all`/`.s7k` multibeam direct georeferencing, SBET/TrueHeave integration, TPU computation, and VR BAG export with zero license seats (critical for distributed ROCs). `HydrOffice QC Tools` (Grid QA, Flier Finder, Holiday Finder, S-102/BAG validators) and `Sound Speed Manager` are industry-standard independent auditors. `MB-System` remains unrivaled for CLI batch processing, side-scan/backscatter mosaics, deep ocean (`EM 304`) grids, and reproducible shell scripts.
   - *Gaps & Operational Friction:* `Kluster` focuses on Kongsberg/Reson multibeam workflows and requires disciplined Python/conda environment pinning; `MB-System` demands command-line fluency and careful parameter review (`-A1` depth vs. `-A2` elevation; format `261` for `.kmall`); commercial suites (`QPS Qimera`, `Teledyne CARIS HIPS`) retain advantages in real-time turnkey operator GUIs, automated wobble diagnostics, and integrated S-57/S-102 cartographic chart production—though dongle/seat licensing breaks elastic cloud scaling ([Ch. 28](../../fable/chapters/ch28-reducing-cost.md)).
   - *Crosswalk:* [Sec. 10.5 Hydrographic Software](../../gemini4/book/ch-10/sec-10-05.md) · [Sec. 13.6 Software Ecosystem](../../gemini4/book/ch-13/sec-13-06.md) · [Ch. 71 Software Landscape](../../fable/chapters/ch71-software-landscape.md)

### D. Handbook Chapter Crosswalk (`fable/` & `gemini4/`)

- **Platform Physics, Timing & Positioning:** [Ch. 12 GNSS](../../fable/chapters/ch12-gnss.md) · [Ch. 13 IMU & INS](../../fable/chapters/ch13-imu-ins.md) · [Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md) · [Sec. 7.4 Marine Platforms & USVs](../../gemini4/book/ch-07/sec-07-04.md) · [Sec. 7.8 Vessel Squat & Dynamic Draft](../../gemini4/book/ch-07/sec-07-08.md) · [Sec. 32.2 Hardware Time Sync](../../gemini4/book/ch-32/sec-32-02.md) · [Notation](../../gemini4/book/00-front-matter/notation-and-symbols.md)
- **Sonar Calibration, Datums, Planning & QC:** [Ch. 9 Vertical Datums](../../fable/chapters/ch09-vertical-datums.md) · [Ch. 20 Sonar](../../fable/chapters/ch20-sonar.md) · [Ch. 25 Calibration](../../fable/chapters/ch25-calibration-infrastructure.md) · [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md) · [Ch. 34 Water in DEMs](../../fable/chapters/ch34-water-in-dems.md) · [Sec. 10.4 Refraction & TVU](../../gemini4/book/ch-10/sec-10-04.md) · [Sec. 13.1 Design & Boresight](../../gemini4/book/ch-13/sec-13-01.md) · [Sec. 13.2 Environmental & White-Ribbon Scheduling](../../gemini4/book/ch-13/sec-13-02.md) · [Sec. 13.3 Real-Time QA](../../gemini4/book/ch-13/sec-13-03.md) · [Sec. 13.5 Boresight Calibration Math](../../gemini4/book/ch-13/sec-13-05.md)
- **Validation, Archiving, Economics & Law:** [Ch. 28 Reducing Cost](../../fable/chapters/ch28-reducing-cost.md) · [Ch. 29 Pipelines](../../fable/chapters/ch29-processing-pipelines.md) · [Ch. 50 Archiving](../../fable/chapters/ch50-archiving-and-provenance.md) · [Ch. 53 Accuracy](../../fable/chapters/ch53-accuracy-assessment.md) · [Ch. 56 Case Files](../../fable/chapters/ch56-case-files.md) · [Ch. 62 Charting & UKC](../../fable/chapters/ch62-navigation-and-charting.md) · [Ch. 69 Security & Sovereignty](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md) · [Sec. 14.5 Co-Registration](../../gemini4/book/ch-14/sec-14-05.md) · [Sec. 19.1 Formats & Telemetry](../../gemini4/book/ch-19/sec-19-01.md) · [Sec. 24.2 Public DEMs & TID](../../gemini4/book/ch-24/sec-24-02.md) · [Sec. 27.2 Privacy](../../gemini4/book/ch-27/sec-27-02.md) · [Sec. 27.3 National Security & Spoofing](../../gemini4/book/ch-27/sec-27-03.md) · [Sec. 27.4 Reducing Cost](../../gemini4/book/ch-27/sec-27-04.md) · [Sec. 33.1 Spatial Autocorrelation](../../gemini4/book/ch-33/sec-33-01.md) · [Sec. 34.5 Cloud-Native Python](../../gemini4/book/ch-34/sec-34-05.md)

### E. External Regulatory & Operational Basis Register (Non-Handbook Sources)

Statutory clocks, hazmat shipping thresholds, RF licensing, and marine insurance endorsements cited in `01`–`08` derive from external regulatory/industry authorities outside the `fable/` and `gemini4/` handbooks. U.S. CFR citations apply in U.S. navigable waters / to U.S.-flag vessels; verify host flag-state/MRCC equivalents abroad before mobilization:

| Citation / Standard | Issuing Authority | Edition / As-Of | Scope & Key Thresholds Enforced in This Modality |
| :--- | :--- | :--- | :--- |
| **COLREGS (1972) / 33 CFR Parts 81 & 83** | IMO / USCG | 1972 (current CFR) | Rules 5–8 (Look-out, Safe Speed, Plotting, Early Avoidance), Rule 23 (Lights), Rule 27(b)/(c)/(d) (RAM / Towing / Dredging) |
| **IHO S-44** | International Hydrographic Org. | Ed. 6.2.0 (Oct 2024) | Core Table 1 $TVU_{95\%}/THU_{95\%}$ $a/b$ parameters unchanged from Ed. 6.1.0 (`fable/` baseline); adds §3.8 seabed characteristics |
| **IMO MASS Code** | IMO Maritime Safety Comm. | MSC 111 (May 2026) | Non-mandatory autonomous ship code (targeting mandatory ~2032 for SOLAS cargo ships $\ge 500\text{ GT}$; informs small USV best practice) |
| **USCG Work Instruction 5P-WI-002(1)** | U.S. Coast Guard | Rev. 1 (current) | *Oversight of Unmanned, Autonomous, and Remote-Control Operations*; COTP CONOPS review & LNM coordination |
| **33 CFR Part 64 & 33 CFR § 153.203** | USCG / EPA (NRC) | Current CFR (U.S.) | Marking sunken hazards/wrecks in navigable channels; **immediate** NRC notice (`1-800-424-8802`) for any visible oil sheen |
| **46 CFR §§ 4.03-2, 4.05-1, 4.05-10 & 4.06** | U.S. Coast Guard | Current CFR (U.S.) | **Immediate** verbal casualty notice; **5-day** CG-2692 (`>$75,000` or grounding/allision/propulsion loss); **2 h** alcohol / **32 h** drug SMI tests |
| **29 CFR § 1904.39** | OSHA | Current CFR (U.S.) | Work-related fatality (**8 h**); hospitalization, amputation, or eye loss (**24 h**; shore/ROC/uninspected craft where not USCG-preempted) |
| **14 CFR § 107.9 & 49 CFR §§ 830.2 / 830.5** | FAA / NTSB | 2022 § 830 amend. | Shipboard support UAS only: FAA **10 d** (`>$500` lower repair/FMV); NTSB **immediate** (`>$25,000` 3rd-party or airworthiness UA) |
| **49 CFR 171–180, IMDG Code, IATA DGR** | PHMSA / IMO / IATA | 67th Ed. (Jan 2026) | Class 9 **UN 3480 `PI965` & UN 3481 `PI966`** ($\le 30\%$ SoC mandatory Jan 2026; `CAO` rules, `UN 38.3`, SDS) + **UN 3090/3091** beacons |
| **47 CFR Parts 80 / 90 & MMSI** | FCC (or local telecom) | Current CFR | Maritime VHF, marine radar, AIS Class A/B, and RF telemetry spectrum licensing |
| **EAR 15 CFR 730–774 & ITAR 22 CFR 120–130** | U.S. BIS / DDTC | Current CFR | Dual-use ECCNs (`6A001` sonar, `7A003` IMU, `7A005` GNSS, `8A001` marine) & defense-article export controls |
| **UNCLOS Part XIII (Arts. 248–249)** | United Nations | 1982 (in force 1994) | Coastal-state MSR consent ($\ge 6\text{ mo}$ Art. 248 lead; plan $\ge 7\text{ mo}$), participation rights, and Art. 249 cruise data sharing |
| **MMPA / ESA & JNCC Seismic Guidelines** | NOAA NMFS / JNCC | JNCC 2017 / current | **30 min** visual pre-watch (**60 min** in $>200\text{ m}$ water) prior to $\ge 20\text{ min}$ soft-start for low-freq acoustic / SBP systems |
| **IOC Manuals & Guides No. 14 / NOAA CO-OPS** | UNESCO IOC / NOAA | Vol. V (2016) / current | Subordinate $\ge 30\text{ d}$ tide gauge installation, $\ge 5$ leveled benchmarks ($6\text{ mm}\sqrt{K}$), and `GNSS@TG` tie |
| **Federal Rules of Evidence 901/902 & 702** | U.S. Courts | Current FRE | Authentication of electronic/SHA-256 digital evidence (`FRE 901/902(13)–(14)`) and expert methodology (`FRE 702 / Daubert`) |
| **GDPR Art. 33 / Art. 34** | European Union | Reg. (EU) 2016/679 | Personal/EO-IR/VHF/medical PII breach notification to supervisory authority within **$\le 72\text{ h}$** (`Art. 33`) |
| **Maritime Coverages (H&M, P&I, MEL, USL&H, IWL)** | Marine Underwriters | Policy-specific | Uncrewed vessel hull endorsement, P&I compulsory wreck removal, Jones Act/MEL & USL&H chase/LARS crew cover, IWL zones |

---

## 2. Copy-Ready Field & ROC Templates

### Template A — ROC / Bridge 4-Hour Watch-Handoff Sheet

```markdown
## ROC / Bridge Watch Handoff Log (4-Hour Max Continuous Helm Watch)
- **Project / Sortie ID:** ______________________ | **Vessel / MMSI:** ______________________
- **Watch Period (UTC):** Start `YYYY-MM-DDTHH:MMZ` -> End `YYYY-MM-DDTHH:MMZ`
- **Single-Point Helm Authority Confirmed At Handoff:** `[ ] ROC Primary` `[ ] Mothership` `[ ] Chase Boat (RF LOS)`
- **Current CONOPS Tier & Polygon:** `[ ] Tier 1 (Attended)` `[ ] Tier 2 (Monitored)` `[ ] Tier 3 (OTH)` | Zone: ________
- **C2 Link Health:** Primary Link (RF/LTE/Starlink/Iridium): ________ | Latency: ____ ms | Packet Loss: ____ %
- **GNSS / INS Status:** Fix Mode (`RTK` / `PPP` / `Float`): ________ | PDOP: ____ | Min C/N0: ____ dB-Hz | Max Rate (deg/s): ____
- **Endurance & Mechanical:** Battery SoC: ____ % OR Fuel Remaining: ____ % | Bilge Alarm: `[ ] DRY` | Cooling Temp: ____ C
- **Weather & Sea State:** Wind: ____ m/s @ ____ deg | Hs / Tp: ____ m / ____ s | Forecast Next 4 h: ________________
- **Active COLREGS / Traffic / Gear Risks:** Closest AIS CPA: ____ m | EO/IR Vis: ____ km (____ nmi) | Active LNM: `[ ] Verified`
- **Acoustic / QC Status:** Active Line: ________ | Last SVP UTC: ________ | SVS Delta: ____ m/s | Open Holidays/DTONs: ________
- **Outgoing Watchstander (Name / Signature / UTC):** ________________________ (Max 4 h continuous helm verified: `[ ]`)
- **Incoming Watchstander (Name / Signature / UTC):** ________________________ (All panels & hazards briefed: `[ ]`)
```

### Template B — COLREGS Traffic, CPA Alert & Incident / Near-Miss Log

```markdown
## COLREGS Traffic, CPA Override & Near-Miss Log
- **UTC Date/Time:** `YYYY-MM-DDTHH:MM:SSZ` | **USV Lat/Lon:** `________, ________` | **CONOPS Tier:** ________
- **Event Category:** `[ ] Routine Give-Way` `[ ] Operator Helm Override` `[ ] CPA < 500/1000 m Alert` `[ ] Near-Miss / Allision`
- **Target Vessel Details:** Name / MMSI / Type: ______________________ | AIS Present? `[ ] Yes` `[ ] No (EO/IR/Radar Only)`
- **Encounter Geometry:** Initial Bearing/Range: ____ deg / ____ m | Predicted Min CPA: ____ m | TCPA: ____ min
- **COLREGS Rule Applied:** `[ ] R8 Early Action` `[ ] R13 Overtaking` `[ ] R14 Head-On` `[ ] R15 Crossing` `[ ] R17 Stand-On Action`
- **Action Taken:** Auto-Avoidance / Manual Course Change (deg): ________ | Speed Reduction (m/s): ________ | VHF Hail Ch: ____
- **Evidence Saved:** `[ ] EO/IR Video Clip` `[ ] Radar Screen` `[ ] AIS Replay` `[ ] C2 Log` | **USCG / Harbor Notice Req'd?** `[ ] Y  [ ] N`
- **Watch Officer Initials:** ________ | **24 h PM Review Initials:** ________
```

### Template C — Autonomous Winched-SVT / SVP Cast, SVS Delta & Draft Log

```markdown
## Sound-Speed Profile (SVP / SVT), SVS Comparison & Static/Dynamic Draft Log
- **Project / Vessel:** ______________________ | **Date (UTC):** `YYYY-MM-DD`
- **Static Waterline Check (Calm Water):** Port Bow: ____ m | Stbd Bow: ____ m | Port Stern: ____ m | Stbd Stern: ____ m | Mean Draft: ____ m
- **Fuel / Ballast Mass & Salinity:** Fuel Load: ____ % | Water Surface Temp / Salinity / Density: ____ C / ____ PSU / ____ kg/m3

| Cast # | UTC Time | Lat / Lon | Method (Winched SVT / MVP / Manual CTD) | Bottom Depth (m) | Max Cast Depth (m) | Hull SVS c_SVS (m/s) | Cast Top c_0 (m/s) | Delta |c_SVS - c_0| (m/s) | Outer Curl Check (+smile / -frown in +d down, % d) | Accepted File Name & SHA-256 Prefix |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 01 | `____Z` | `____, ____` | `____________` | `____` | `____` | `______` | `______` | `____` | `____` | `________________` |
| 02 | `____Z` | `____, ____` | `____________` | `____` | `____` | `______` | `______` | `____` | `____` | `________________` |
| 03 | `____Z` | `____, ____` | `____________` | `____` | `____` | `______` | `______` | `____` | `____` | `________________` |

- **Reminder:** Immediate cast trigger fires whenever `|c_SVS - c_0| > 1.5-2.0 m/s` OR outer-beam refraction smile/frown exceeds `0.5 %` of water depth. Confirm `>= 3-5 m` seabed clearance before paying out autonomous winched SVT.
```

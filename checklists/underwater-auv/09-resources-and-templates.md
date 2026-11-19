# Underwater AUV Bathymetric & Subsea Mapping — Phase 9: Resource Inventory, Critique & Copy-Ready Templates

> **Modality:** `underwater-auv` | **Scope:** Authoritative external guides, open-source tools, handbook links, and field-ready operational worksheets  
> **Companion Reference:** [00-README-and-signoff.md](./00-README-and-signoff.md) | [Fable Appendix G Checklists](../../fable/appendices/appendix-g-checklists.md)

---

## 1. Modality Resource Inventory & Honest Critique

No single external manual spans the entire underwater AUV bathymetric lifecycle — from UNCLOS/ITAR/UN 3480 permitting and Archimedes salinity ballasting through acoustic USBL box-in, TEOS-10 pressure reduction, bathymetric SLAM, and S-102/BAG delivery. Use this table to understand what each authoritative source covers well and where it has operational blind spots.

| Source / Standard / Tool | Coverage Strengths | Critical Gaps & Operational Blind Spots | Primary Phase Fit |
| :--- | :--- | :--- | :--- |
| **WHOI NDSF** (*Sentry* / *REMUS 6000* User Guides & Ops SOPs) | Battle-tested deep-ocean AUV LARS, dual burn-wire / galvanic drop-weight safety, ship-board dive-turnaround cadence, and non-surfacing search discipline | Heavily tailored to UNOLS vessels and WHOI telemetry; sparse on commercial `IHO S-44`/`S-102` certification, coastal tidal SEP transforms, and international `UN 3480` freight brokerage | Phases `03`, `05`, `06` |
| **MBARI** (`MB-System`, `mbnavadjust`, Seafloor Mapping AUV Workflows) | Unmatched open-source AUV swath processing, ray-tracing, and bathymetric SLAM (`mbnavadjust`) crossline inversion; proven to `4,000+ m` | Steep CLI learning curve; requires explicit user discipline on INS/body-frame sign conventions, grid convergence, and `TEOS-10` vs naive depth checks; sparse `CUBE`/`S-102` GUI tooling | Phases `04`, `05`, `07`, `08` |
| **NOC** (*Autosub* / *Autosub Long Range* Field & Under-Ice Guides) | Premier engineering treatment of endurance modeling (`P ~ v^3`), high-latitude salinity ballasting, fault-tree autonomy, and under-ice acoustic homing | Centered on UK research infrastructure (`NERC`); does not cover US `NOAA HSSD`, `USCG CG-2692`, or `ITAR/EAR` export-control mechanics | Phases `02`, `03`, `04`, `06` |
| **Kongsberg Maritime** (HUGIN / HiSAS / HiPAP / `SIS` / `NavLab` Manuals) | Integrated hardware manuals for `.kmall` logging, `HiPAP` USBL box-in, `HiSAS 1032` SAS beamforming, and `NavLab` RTS Kalman smoothing | Vendor-locked formats and closed customer portals; treats environmental permits, Li-ion air transport, insurance COIs, and white-ribbon compositing as out of scope | Phases `03`, `04`, `05`, `07` |
| **UNOLS / Multibeam Advisory Committee (`MAC` Wiki)** | Outstanding shipboard MBES patch tests, BIST noise diagnostics, SVP hysteresis checks, and USBL/MRU alignment best practices | Strong on surface hull-mounted sonar, **thin on AUV salinity ballasting, O-ring vacuum tests, descent water-column drift, battery reserve abort gates, and AUV SLAM loops** | Phases `03`, `04`, `05` |
| **IHO (`S-44 Ed. 6.2.0`, `C-13`, `S-102 Ed. 3.0.0`, `S-158:102`)** | Authoritative uncertainty definitions (`TVU`/`THU`), feature detection matrices, seabed characteristics (`S-44 Ed. 6.2.0`, Oct 2024; core Table 1 `a/b` values unchanged from Ed. 6.1.0), and unambiguous `+d ↓` bathymetric coverage schemas | Normative standards only; give zero guidance on how to calibrate a Paroscientific sensor, ballast an AUV, mitigate DVL dropout, or manage `UN 3480` hazmat | Phases `01`, `07`, `08` |
| **NOAA OCS (`HSSD 2024`, `FPM`, `Kluster`, `HydrOffice`)** | Concrete grid-resolution brackets (`0–320 m`), `24 h` DTON escalation, holiday rules, and reproducible open-source Python (`Kluster`) uncertainty pipelines | Designed primarily for surface ships and launches `< 320 m` deep; omits abyssal `TEOS-10` conversion (`-45.4 m` pressure bias at `3,000 m`), SAS nadir fill, and LARS safety | Phases `01`, `05`, `07` |
| **IMCA (`IMCA S 017 / M 244`)** | Clear commercial offshore guidance on **USBL/LBL positioning calibration geometry, box-in residual targets, and subsea positioning redundancy** | Positioning-only offshore guidance (does not cover LARS crane rigging SWL — use `UNOLS RVSS App. A & B` / `API RP 2D`); omits `NCEI/DCDB` archiving, `GEBCO TID` provenance, and scientific MSR permitting | Phases `03`, `04` |

---

## 2. Handbook Chapter Crosswalk (`fable` & `gemini4`)

- **Navigation, INS, USBL/LBL & SLAM:** [fable Ch. 13 IMU/INS](../../fable/chapters/ch13-imu-ins.md), [fable Ch. 14 Positioning Beyond GNSS](../../fable/chapters/ch14-positioning-beyond-gnss.md), [fable Ch. 15 SLAM](../../fable/chapters/ch15-slam.md), [gemini4 Sec. 5.4 Underwater Positioning & Worked 3,000 m TPU Budget](../../gemini4/book/ch-05/sec-05-04.md), [gemini4 Sec. 6.1 SLAM Foundations](../../gemini4/book/ch-06/sec-06-01.md)
- **AUV Platforms, Sonar & Calibration Infrastructure:** [fable Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md), [fable Ch. 20 Sonar](../../fable/chapters/ch20-sonar.md), [fable Ch. 25 Calibration Infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md), [gemini4 Sec. 7.4 Marine Platforms & AUVs](../../gemini4/book/ch-07/sec-07-04.md), [gemini4 Sec. 10.2–10.6 Acoustic Ray Tracing & Pitfalls](../../gemini4/book/ch-10/sec-10-02.md)
- **Planning, QC, Uncertainty, Formats & Archiving:** [fable Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md), [fable Ch. 47 File Formats](../../fable/chapters/ch47-file-formats.md), [fable Ch. 49 Metadata](../../fable/chapters/ch49-metadata.md), [fable Ch. 50 Archiving & Provenance](../../fable/chapters/ch50-archiving-and-provenance.md), [fable Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md), [gemini4 Sec. 13.1–13.5 Marine QC, TPU Audits & Observability](../../gemini4/book/ch-13/sec-13-01.md), [gemini4 Sec. 14.2–14.5 Error Propagation, Nuth–Kääb & DEM Forensics](../../gemini4/book/ch-14/sec-14-02.md), [gemini4 Sec. 33.1 Spatial Autocorrelation & N_eff](../../gemini4/book/ch-33/sec-33-01.md)
- **Legal, Security, Cost, Standards & Shared Workbooks:** [fable Ch. 28 Reducing Cost](../../fable/chapters/ch28-reducing-cost.md), [fable Ch. 68 Legal Issues](../../fable/chapters/ch68-legal-issues.md), [fable Ch. 69 Security & Ethics](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md), [fable Ch. 70 Specifications](../../fable/chapters/ch70-specifications-guided-tour.md), [Appendix D Standards Index](../../fable/appendices/appendix-d-standards-index.md), [gemini4 Sec. 24.1–24.2 Hydrographic Standards](../../gemini4/book/ch-24/sec-24-01.md), [gemini4 Sec. 27.1–27.4 Legal, Export Controls & Cost Tiering](../../gemini4/book/ch-27/sec-27-01.md)
- **Shared Cross-Modality Templates:** [Project Header](../_shared/template-project-header.md), [Error Budget](../_shared/template-error-budget.md), [Cost Ledger](../_shared/template-cost-ledger.md), [Insurance COI](../_shared/template-insurance-coi.md), [Accident Card](../_shared/template-accident-card.md), [AAR Retrospective](../_shared/template-aar-retrospective.md), [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md)

### External Regulatory & Standards Basis Register (Non-Handbook Authorities)

*Scope note:* These external operational, hazmat, rigging, and maritime casualty authorities sit outside `fable/` and `gemini4/`; verify current edition status prior to international mobilization (register baseline verified as of `2026`).

| Regulation / Standard | Issuer & Exact Edition / Citation | Modality Scope & Verification Basis |
| :--- | :--- | :--- |
| **UN 3480 / 3481 / 3090 / 3091** | `IATA DGR 67th Ed. (2026)` (`PI965–970`), `IMO IMDG Code`, `49 CFR 171–180` | `UN 3480 PI965` (`<= 30 %` SoC, `CAO`), `UN 3481 PI966` (`<= 30 %` SoC eff. 1 Jan 2026), primary lithium-metal `UN 3090` (`CAO`) / `UN 3091`, `UN 38.3` & `SDS` |
| **UNOLS `RVSS` Safety Standards** | `UNOLS` *Research Vessel Safety Standards* (`App. A & B`, `RVOC`) | Rope/wire rope safety factors (`>= 2.0x` LARS SWL), crane/A-frame overboard-handling hardware, and vessel deck incident reporting |
| **USCG Casualty & `SMI` Rules** | `46 CFR § 4.05-1 / § 4.05-10`, `46 CFR § 4.06`, `33 CFR § 153.203` | US-flag/US-waters immediate verbal + `5-day` `Form CG-2692` (`> USD 75,000`), `2 h / 32 h` `SMI` testing, immediate `NRC` oil/hazmat notice |
| **OSHA Recordkeeping** | `29 CFR § 1904.39` | `8 h` fatality / `24 h` hospitalization, amputation, or loss of eye (where OSHA holds jurisdiction; exempt for USCG-inspected seamen) |
| **Export Control (`ITAR` / `EAR`)** | `22 CFR Parts 120–130` (`DSP-5/DSP-73`), `15 CFR Parts 730–774` (`ECCNs 8A001, 7A003, 7A005, 6A001`; `§ 740.9 TMP`) | Submersible hulls, nav-grade INS, SAS/InSAS, and foreign-national deemed-export Technology Control Plans |
| **Seafloor Positioning & Tides** | `IMCA S 017 / M 244 (Rev. 2023)`, `IOC Manuals & Guides No. 14` | USBL/LBL box-in calibration geometry & tidal benchmark leveling practices (`>= 3` minimum per `fable §26.3`, `5+` recommended) |
| **IHO Hydrographic Surveys** | `IHO S-44 Ed. 6.2.0 (Oct 2024)` (baseline `Ed. 6.1.0` cited in `fable/`) | Core Table 1 `TVU/THU` `a/b` values unchanged from `Ed. 6.1.0`; adds `§3.8` seabed characteristics (`Exclusive`, `Special`, `1a/1b`, `2`) |
| **Subsea Acoustics & Wildlife** | `UNCLOS Part XIII (1982, Art. 245–249)`, `MMPA/ESA`, `JNCC (2017)` | `>= 6 mo` diplomatic MSR consent (`+ routing lead`), `30 min` (`60 min` in `> 200 m`) MMO pre-watch & `>= 20 min` soft-start |
| **Cultural Heritage, Localization & Customs** | `UNESCO (2001)`, `India MoST (2021)`, `ICC/WCO ATA Carnet (1990)`, `IMO STCW (2010 Manila)` | Underwater wreck protection, `< 10 m / < 100 m` bathymetric localization, customs equipment carnet, and `>= 10 h / 24 h` crew rest |
| **Marine Insurance Clauses** | `Institute Time Clauses` (`IWL`, `P&I`, `C&V` Survey, `FVWC`, `E&O`) | Submerged equipment floater valuation (`C&V`), `IWL` polar/ice boundaries, Waiver of Subrogation, and `>= 30 d` expiry standby buffer |

---

## 3. Copy-Ready Field Worksheets & Logs

### A. AUV Dive Plan & Go/No-Go Card

```text
========================================================================
AUV DIVE PLAN & GO/NO-GO CARD (COPY FOR BRIDGE, LAB & LARS DECK)
========================================================================
Cruise / Project ID:   ____________________   Dive No.: ______________
AUV Vehicle / Hull ID: ____________________   Date (UTC): ____________
Launch Coord (Lat/Lon):____________________   Target Max Depth (m): __
Descent Waypoint (Offset up-current): _________________________________
Predicted Descent Drift (m / deg):   _________________________________
Altitude Mode:  [ ] Terrain-Follow (h_alt = ____ m)  [ ] Isobaric (Z = ____ m)
OAS Min Clearance (m): _____   Max Depth Floor (m) / Min Alt Ceiling (m): ___
Swath / Overlap (%):   _____   SLAM Tie / Crosslines Included? [Y / N]
Planned Duration (h):  _____   Battery Start SoC (%): ________________
HARD ABORT SoC (%):    25 %    Max Elapsed Dive Timeout (UTC): _______
Surface Wet-Check Pass (UTC): ______  Rally / Abort Waypoint: ________

RECOVERY & TELEMETRY CHANNELS:
- USBL Beacon Address / Freq: ______________   Max Slant Range (m): __
- LBL Array IDs / Active? [Y / N]             Iridium IMEI: __________
- Argos PTT ID: ___________________________   VHF DF Freq (MHz): _____
- Emergency Pinger Freq (kHz): ____________   Corrodible Link (h): ___

MANDATORY GO / NO-GO GATES (ALL MUST BE SIGNED YES PRIOR TO CRANE LIFT):
[ ] UNCLOS / MMPA / PSO Watch Cleared        [ ] Ballast & Trim Log Signed
[ ] Vacuum Leak Test Passed & Logged         [ ] Drop-Weights & Burn-Wire Armed
[ ] Fresh SVP Loaded (< 4 h)                 [ ] LARS RVSS Rigging & Hs Verified
[ ] Deck BIT, INS & Strobes Verified         [ ] Drop-Weight Safety Pin Pulled @ Rail

Chief Scientist / Hydrographer: _____________  AUV Lead Eng.: __________
Ship Master / Bridge OOD: ___________________  Launch UTC: _____________
========================================================================
```

### B. Salinity Ballasting & Trim Calculation Worksheet

```text
========================================================================
SALINITY BALLASTING & HYDROSTATIC TRIM WORKSHEET (TEOS-10 DENSITY)
========================================================================
Dive No.: _______________  Location: _________________  Date (UTC): ____
Vehicle Baseline Dry Config Mass M_base (kg):     ____________________
Baseline Displaced Volume V_disp (m^3):           ____________________

1. MEASURED WATER DENSITY (rho_w = TEOS-10 rho(S, T, p)):
   - Launch Surface Water:  T_surf = _____ C  | S_surf = _____ PSU | rho_surf = _______ kg/m^3
   - Target Seabed Water:   T_bot  = _____ C  | S_bot  = _____ PSU | rho_bot  = _______ kg/m^3
   - Note: 1 m^3 displaced across 1000 -> 1026 kg/m^3 shifts buoyancy by +26.0 kg!

2. BUOYANCY & MASS-BALANCE SIGN EQUATION:
   - Delta M_add = (V_disp + Delta V_hull(P, T)) * rho_site - M_base - B_net_positive
     (+ = add ballast weight to maintain target positive surfacing reserve B_net_positive; - = remove weight)
   - Gross Buoyancy at Surface:  B_surf = V_disp * rho_surf = _________ kg
   - Gross Buoyancy at Seabed:   B_bot  = (V_disp + Delta V_hull) * rho_bot = _________ kg
   - Target Net Positive Buoyancy B_net_positive (typ. +0.5% to +1.5%): _________ kg
   - Required Trim/Ballast Adjustment Delta M_add (+ add / - remove):    _________ kg

3. WET TANK / HARBOR TRIM & MAGNETOMETER VERIFICATION:
   - Nose-Up / Down Pitch Angle (within [-1.5, +1.5] deg static tank trim tolerance): _________ deg
   - Static Roll Angle (within [-0.5, +0.5] deg static tank trim tolerance):           _________ deg
   - Compass / Magnetometer Hard- & Soft-Iron Swing Check Passed After Ballast Shift? [ ] Yes
   - Drop-Weight Mass (exceeds max negative buoyancy margin): _________ kg
   - Weight Placement Logged (Bow: ___ kg | Mid: ___ kg | Aft: ___ kg)

Prepared By: _____________________   Independent Verifier: _____________
========================================================================
```

### C. Pressure Housing O-Ring & Vacuum Leak-Test Log

```text
========================================================================
PRESSURE HOUSING O-RING, CONNECTOR & VACUUM LEAK-TEST LOG
========================================================================
AUV Hull ID: _______________   Dive / Cycle No.: __________  Date (UTC): ___
Ambient Deck Temp (C): _____   Deck RH (%): _____   Barometer (hPa): ______

1. SEAL & CONNECTOR INSPECTION (CHECK EVERY OPENED HATCH / BULKHEAD):
   Housing / Section         | O-Ring S/N | Groove Clean? | Grease OK? | Tech Initials
   --------------------------|------------|---------------|------------|--------------
   Main Electronics Hull     | __________ | [ ] Pass      | [ ] Pass   | _____________
   Battery Module Bay A      | __________ | [ ] Pass      | [ ] Pass   | _____________
   Battery Module Bay B      | __________ | [ ] Pass      | [ ] Pass   | _____________
   Payload / Sonar Nose      | __________ | [ ] Pass      | [ ] Pass   | _____________
   Vacuum Port & Relief Valve| __________ | [ ] Pass      | [ ] Pass   | _____________
   Wet-Mateable Whips Cleaned| N/A        | [ ] Inspected | [ ] Silicone | ___________

2. VACUUM LEAK-TEST RECORD (BEFORE EVERY DEPLOYMENT AFTER ANY SEAL OPENING):
   Housing / Bay   | Target Pull (kPa) | Start (kPa / UTC) | End (kPa / UTC) | Drift (kPa) | Result
   ----------------|-------------------|-------------------|-----------------|-------------|-------
   Main Hull       | -65 kPa (min 30m) | _____ / _________ | _____ / _______ | _________   | [ ] PASS
   Battery Bay A   | -65 kPa (min 30m) | _____ / _________ | _____ / _______ | _________   | [ ] PASS
   Battery Bay B   | -65 kPa (min 30m) | _____ / _________ | _____ / _______ | _________   | [ ] PASS
   Payload Section | -65 kPa (min 30m) | _____ / _________ | _____ / _______ | _________   | [ ] PASS

3. INTERNAL HEALTH & DESICCANT GATE:
   - Internal Bay Humidity at Closeout: ______ % RH (must be <= 25 % RH)
   - Fresh Silica Gel Packs Installed? [ ] Yes (Count: ____)
   - Ground-Fault Insulation Resistance: ______ MOhm (must be >= 10 MOhm)
   - BMS Cell Group Spread: ______ mV (must be <= 20 mV)
   - Pressure-Compensated Oil Junction Boxes Bled Bubble-Free? [ ] Yes

Seal Lead Technician: _______________  Second-Eyes Verifier: _______________
========================================================================
```

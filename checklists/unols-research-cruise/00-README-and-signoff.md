# UNOLS Research Cruise DEM & Bathymetric Mapping Checklists

Operational end-to-end checklist suite for crewed **University-National Oceanographic Laboratory System (UNOLS)** academic research vessels conducting multibeam echosounder (`MBES`), sub-bottom profiler (`SBP`), water-column imaging (`WCI`), and Moving Vessel Profiler (`MVP`) bathymetric surveys. This modality spans long-lead scheduling in Marine Facilities Planning (`MFP`) through foreign Marine Scientific Research (`MSR`) clearance, pier mobilization, 24/7 watchstanding, operator-to-`R2R` raw custody verification before disembarkation, ellipsoidally referenced reprocessing (`ERS`), and error-budget reconciliation.

> **Master Project Header:** Complete [template-project-header.md](../_shared/template-project-header.md) once at project kickoff and propagate the locked fields identically into phases `01` through `08`. Do **not** alter datum, epoch, or sign convention mid-cruise without an audited Chief Scientist + Mapping Lead change order.

---

## 1. UNOLS Vessel Class, Payload & Indicative Cost Envelopes

Select and verify the vessel envelope against science mission endurance, water depth, swath acoustic frequency, and transit distance.

| UNOLS Vessel Class | Typical LOA & Endurance | Indicative Daily Charter Tier (USD) | Primary Acoustic & Water-Column Suite | Typical Swath & Mapping Throughput | Primary Mount & Motion Architecture |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Global Class** | `70–90+ m` LOA, `30+` science berths, `45–60+ d` endurance, worldwide blue-water / high-latitude | `$40,000–$60,000+/day` | `12 kHz` deepwater MBES (`0.5° × 1°` or `1° × 1°`), `3.5 kHz` / parametric SBP, `18/38/120 kHz` EK80 WCI, `38/75 kHz` ADCP, winch-deployed MVP + 24-bottle CTD + XBT | `200–11,000 m` water depth; `2–3x d` swath (`110°–125°` total); `1,000–5,000 km²/day` at `5.1–6.2 m/s (10–12 kn)` | `1.0–2.0 m` below-keel ice/bubble gondola or deep hull blister; high-grade FOG INS (`POS MV OceanMaster` / `Seapath 380` + `GAMS`) |
| **Ocean / Intermediate Class** | `50–70 m` LOA, `18–26` science berths, `25–40 d` endurance, ocean-basin & continental margin | `$25,000–$40,000/day` | `12/30 kHz` or dual `30/70 kHz` MBES, `3.5 kHz` SBP, `75/150 kHz` ADCP, MVP / underway CTD, XBT launcher | `50–7,000 m` water depth; `2.5–3.5x d` swath; `400–2,500 km²/day` at `4.1–5.7 m/s (8–11 kn)` | Flush hull blister or shallow gondola; dual-antenna GNSS-aided INS + `1PPS` / `PTP` synchronization |
| **Regional / Coastal Class (incl. RCRV)** | `25–50 m` LOA, `10–18` science berths, `7–21 d` endurance, continental shelf & coastal margin | `$15,000–$25,000/day` | `70–100 kHz` or `200–400 kHz` shallow/shelf MBES, Chirp SBP, `300 kHz` ADCP, portable `SVS`/`MVP`/`CTD`, optional portable over-side pole | `5–1,500 m` water depth; `3–4x d` swath (`130°–145°` total); `50–400 km²/day` at `3.1–5.1 m/s (6–10 kn)` | Hull fairing, moonpool deployment carriage, or rigid over-the-side pole (`VIV` and speed-deflection rated) |

> **Cost & Offline Field-Binder Basis:** Daily charter tiers above are **indicative planning ranges** (actual cost is quote-dependent by operator, fuel burn, and port-agent surcharges; [sec-07-04.md](../../gemini4/book/ch-07/sec-07-04.md) notes `$30,000–$80,000/day` blue-water research-vessel benchmarks—verify current UNOLS/operator schedule in `MFP`). Print and bind `00`–`09` plus [template-accident-card.md](../_shared/template-accident-card.md) and [template-insurance-coi.md](../_shared/template-insurance-coi.md) in physical Bridge and Main-Lab binders for 100 % offline execution at sea.

---

## 2. Coordinate Frames, Sign Conventions & Time Scales (Hard Lock)

Misaligned coordinate signs and uncompensated baud/lever delays cause systematic bathymetric artifacts that survive naive automated cleaning. Lock all values across [notation-and-symbols.md](../../gemini4/book/00-front-matter/notation-and-symbols.md), [sec-03-02.md](../../gemini4/book/ch-03/sec-03-02.md), and [ch06-time-as-coordinate.md](../../fable/chapters/ch06-time-as-coordinate.md):

1. **Vessel & Motion Reference Frame (NED vs ENU):** Reconcile the ship's pier/dry-dock total-station vessel offset survey (e.g., **Westlake Consultants Vessel Survey Report [VSR]**) right-handed **NED** vessel frame (`+X` forward/bow, `+Y` starboard, `+Z` downward into water, positive roll = starboard down, positive pitch = bow up, positive yaw = clockwise viewed from above) explicitly against **ENU** IMU outputs (`+X` East, `+Y` North, `+Z` Up) before typing signs into `POS MV`, `Seapath`, `SIS`, or `Qinsy`.
2. **Vertical Datum Triad & Sign Convention (`h = H + N = z_CD + SEP = SEP - d_CD`):** Explicitly separate **Elevation (`+z` positive upward)** used by `GeoTIFF`/`COG`, `BAG FSD 2.0.1` (`BAG 2.0.1`), and ellipsoidal/orthometric heights (`h`, `H`) from **Depth (`+d` positive downward)** used by raw `.kmall`/`.all` water depths and `IHO S-102 Ed. 3.0.0` (verify GDAL's `S-102` `verticalCS = 6498` depth-vs-elevation open option on export!). Clarify datum scope: **`EPSG:5866` (`NOAA MLLW depth`)** governs U.S. coastal/shelf hydrographic charting, whereas open-ocean UNOLS cruises typically archive ellipsoidal height `h` (`ITRF2020`) or `EGM2008` orthometric height (`EPSG:3855`) / `MSL`. Never mix signs inside `VDatum` (`TSS_VDatum = -TSS`).
3. **Time Scales & Latency:** Acquire all raw streams in **UTC** (or **GPST**, explicitly recording leap-second offset `GPST = UTC + 18 s` since 2017-01-01). Verify hardware **`1PPS`** (`< 1 us` jitter) paired with serial `$GPZDA` at `>= 115,200 baud` (or **IEEE 1588v2 PTP**), eliminating the classic `1.000 s` NMEA message-lag blunder.

---

## 3. Two-Person Independent Verification Protocol

Single-operator configuration errors (`SVP` vs `SVS`, double-applied induced heave, wrong `ant_height` sign, unlogged fuel burn) frequently escape detection until final shore processing weeks later:

- Every **`[GATE]`** item in phases `01` through `08` requires **both** a **Phase Lead** (Chief Scientist, Lead Marine Tech, or Mapping Lead) **and** an **Independent Verifier** (separate watchstander, MAC representative, or onshore QA lead) who independently reads the instrument screen, script output, or signed document rather than relying on verbal confirmation.
- On peer-to-peer watch handovers and shore transfers, no vessel departs pier (`03 -> 04`) or releases science party at disembarkation (`07`) until the **Independent Verifier** initials the gate row below.

---

## 4. Phase Checklists & Gate Summary

| Phase | Checklist File | Operational Scope | Mandatory Exit Gate Summary | Target Sign-Off Timing |
| :--- | :--- | :--- | :--- | :--- |
| **01** | [01-requirements-and-preplanning.md](01-requirements-and-preplanning.md) | MFP/SSC scheduling, S-44 Ed. 6.2.0/NOAA OE/Seabed 2030/UNCLOS specs, R2R/GEBCO screening, transit & standby plan | Cruise Planning Manual, spec-derived TPU target, Archive/TID screen, DMP, Medical init & spares signed | `12–18+ mo` prior to `60 d` pre-cruise |
| **02** | [02-permits-safety-insurance-cost.md](02-permits-safety-insurance-cost.md) | Part A (Pre-Mob) & Part B (Daily): UNCLOS Part XIII, MMPA/JNCC, RVSS A/B, STCW, Medical, ITAR/hazmat, COI & rate ledger | RATS MSR (`>= 7 mo`), IHA/LOA, hazmat/SDS/RSO, Floater COI + C&V, RVSS wire/crane, Medical, STCW & MOB drill locked | `>= 7 mo` (MSR) to `Day 0` clearing sea buoy |
| **03** | [03-platform-sensor-prep-and-support.md](03-platform-sensor-prep-and-support.md) | MAC QAT/SAT, offset survey (e.g., Westlake VSR), pole VIV, static draft/density, GAMS/1PPS, single induced heave, MVP/SVS cal | Exact lever arms & signs verified by 2 people; `GAMS` & `1PPS` active; `|SVS - CTD| <= 0.5 m/s`; 30-min soak clean | Pier-side mobilization prior to transit |
| **04** | [04-mission-or-flight-planning.md](04-mission-or-flight-planning.md) | Swath `2–4x d`, ping speed ceiling, `>= 4–5 %` crosslines, 4-step patch test, `2–3 Tc` turn run-in, Tuck/Barrass squat, TPU budget | Worked *a priori* deep/shelf TPU budget passes S-44 Ed. 6.2.0; line plan includes crosslines, `2–3 Tc` run-in, & SVP cadence | Before start of first survey line |
| **05** | [05-underway-qc-and-field-processing.md](05-underway-qc-and-field-processing.md) | 24/7 watchstanding, live TPU, bubble/WCI SNR, `|SVS - cast(0)| > 1.5–2.0 m/s` trigger, nightly MB-System/Qimera QA, 3-2-1 SHA-256 | Zero red TPU zones; crosslines within budget; 24 h DTON cleared; Seabed 2030 transit active; 3-2-1 SHA-256 verified daily | Continuous underway (every `12–24 h`) |
| **06** | [06-accidents-and-emergencies.md](06-accidents-and-emergencies.md) | Laminated Bridge/Lab ERP: MOB, wire failure, grounding, hazmat, medevac, Li-ion deluge/RAID/GNSS-EW freeze, USCG/SMI/NRC/OSHA clocks | Printed copies at Bridge & Main Lab; crew drilled; statutory/policy notification & SHA-256/FRE 901/902 freeze armed | Active `24/7` from boarding to demob |
| **07** | [07-demob-processing-and-validation.md](07-demob-processing-and-validation.md) | End-of-cruise draft closure, **100 % raw custody BEFORE disembark**, PCAR, delayed heave vs PPK ERS, CUBE, NCEI/DCDB deposit | Dual-signed project custody receipt BEFORE gangway exit; off-hire inspection clear; PPK/ERS + CUBE + HydrOffice QC + DOI accepted | Day of arrival (`custody`) to `90–180 d` post-cruise |
| **08** | [08-error-budget-and-retrospective.md](08-error-budget-and-retrospective.md) | *A priori* vs *a posteriori* error decomposition, `chi^2` CIs (`N_eff`), NMAD, 14–30 d AAR, MAC/R2R feedback, casualty case trigger | Empirical `95 %` TVU/THU within target & `|bias| <= 0.1 * TVU_max`; AAR cost/safety diff closed; fleet lessons transmitted | `14–30 d` post-demob (`AAR`) / final archive |
| **09** | [09-resources-and-templates.md](09-resources-and-templates.md) | Authoritative UNOLS/MAC/R2R/NOAA OE/IHO/software critique, External Statutory Register & copy-ready watch/SVP/draft field logs | Printed watch binder stocked with physical copies of all three field logs & emergency quick-card | Pre-departure binder assembly |

---

## 5. Cruise Sign-Off & Custody Sheet (Shipboard & Shoreside Gate Record)

Complete every physical and digital signature row below before clearing the departure sea buoy (`Pre-Sail`) and before the science party departs the vessel (`Raw Custody & Off-Hire`).

| Role | Printed Name & Affiliation | Pre-Sail Briefing & Safety Gate (`02–04`) | Signature / Date (UTC) | Disembarkation Raw Custody / Off-Hire Gate (`07`) | Signature / Date (UTC) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Chief Scientist** | `______________________________` | `[ ]` Permits, Science Plan, DMP & Cost/Standby rules locked | `________________` | `[ ]` 100 % raw custody receipt signed, PCAR queued, off-hire clear | `________________` |
| **Ship Master** | `______________________________` | `[ ]` RVSS App. A/B, Stability, STCW Rest & MOB drill approved | `________________` | `[ ]` Crane offload, deck restoration & hazardous cargo clear | `________________` |
| **Lead Marine Technician** | `______________________________` | `[ ]` Offset survey, 1PPS, SVS/CTD cal, K-Sync & vans verified | `________________` | `[ ]` R2R shipboard raw copy & MAC calibration logs confirmed | `________________` |
| **Lead Multibeam / Mapping Lead** | `______________________________` | `[ ]` Patch test, line plan, TPU budget & 3-2-1 backup live | `________________` | `[ ]` Final draft/fuel closure, cal reports & daily QC packaged | `________________` |
| **Independent QA Verifier** | `______________________________` | `[ ]` Two-person check of sign conventions, lever arms & heave | `________________` | `[ ]` SHA-256 BagIt manifests match 100 % of raw streams | `________________` |
| **Data Custodian / R2R Contact** | `______________________________` | `[ ]` Cruise ID registered & metadata skeleton active | `________________` | `[ ]` Operator distribution verified for R2R ingestion & DOI | `________________` |

---

## 6. Foundational Cross-References

- **Handbook Foundations:** [STYLE_GUIDE.md](../../fable/STYLE_GUIDE.md) | [appendix-g-checklists.md](../../fable/appendices/appendix-g-checklists.md) | [ch16-platforms.md](../../fable/chapters/ch16-platforms.md) | [ch20-sonar.md](../../fable/chapters/ch20-sonar.md) | [ch70-specifications-guided-tour.md](../../fable/chapters/ch70-specifications-guided-tour.md)
- **Technical Reference Manual:** [TOC.md](../../gemini4/TOC.md) | [notation-and-symbols.md](../../gemini4/book/00-front-matter/notation-and-symbols.md) | [sec-03-02.md](../../gemini4/book/ch-03/sec-03-02.md) | [sec-07-04.md](../../gemini4/book/ch-07/sec-07-04.md) | [sec-07-08.md](../../gemini4/book/ch-07/sec-07-08.md)
- **Shared Cross-Modality Templates:** [template-project-header.md](../_shared/template-project-header.md) | [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md) | [template-error-budget.md](../_shared/template-error-budget.md) | [template-cost-ledger.md](../_shared/template-cost-ledger.md) | [template-insurance-coi.md](../_shared/template-insurance-coi.md) | [template-accident-card.md](../_shared/template-accident-card.md) | [template-aar-retrospective.md](../_shared/template-aar-retrospective.md)

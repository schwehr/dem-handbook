# Land Aircraft LiDAR & Imagery — Master Overview & Phase-Gate Sign-Off

> **Offline Field-Binder Rule:** Print or archive offline `00`–`09` plus `../_shared/` templates (`template-project-header.md`, `template-error-budget.md`, `template-cost-ledger.md`, `template-insurance-coi.md`, `template-accident-card.md`, `template-aar-retrospective.md`, `multimodal-white-ribbon.md`). Every `[GATE]` threshold, formula, and statutory clock in `01`–`08` is inlined so cockpit, FBO, and ramp checks execute without internet connectivity.

## 1. Modality Scope & Operational Envelope

This checklist suite governs manned airborne topographic LiDAR and large-format digital photogrammetric surveys collected across terrestrial, coastal-upland, utility-corridor, and alpine environments. All quantitative specifications use SI units as primary values (with statutory US aviation altitudes or legacy imperial program references noted alongside SI equivalents). Horizontal realizations require an explicit datum and epoch (e.g., `NAD83(2011) epoch 2010.00`, `ITRF2020`, or `WGS 84 (G2296)` — never bare `"WGS 84"`).

| Dimension | Covered Configurations & Operational Parameters | Governing Reference |
| :--- | :--- | :--- |
| **Unpressurized Fixed-Wing** | Single/twin piston and turboprop platforms (Cessna 206/208, Partenavia P.68, Diamond DA42/DA62 MPP, DHC-6 Twin Otter); open or optical-port belly hatches; typical survey ceiling `300–3,810 m AGL` (`12,500 ft MSL` oxygen threshold), airspeed `45–75 m s⁻¹`, endurance `4–7 h` | [ch-07/sec-07-03](../../gemini4/book/ch-07/sec-07-03.md), [ch16-platforms](../../fable/chapters/ch16-platforms.md) |
| **Pressurized Fixed-Wing & Jet** | Pressurized twin turboprop and light/mid-size jets (Beechcraft King Air B200/350, Twin Commander 690, Learjet 35/60); optical port glass windows requiring cabin `ΔP` & thermal meniscus correction; operating envelope `500–11,000 m AGL`, airspeed `75–150 m s⁻¹`, daily coverage `500–1,500+ km²` | [ch-07/sec-07-03](../../gemini4/book/ch-07/sec-07-03.md) |
| **Rotorcraft (Hardpoints & Slung Pods)** | Single/twin helicopters (Airbus AS350/H125, Bell 206L/407) with FAA-approved nose, belly, or landing-gear step hardpoints (`f_1R ≈ 5–7 Hz`, blade harmonics `18–28 Hz`) or cable-slung EM/LiDAR pods; oblique `35°–60°` alpine cliff mounts; corridor/wire hover-to-`45 m s⁻¹` sweeps | [ch-07/sec-07-03](../../gemini4/book/ch-07/sec-07-03.md), [ch33-wires-and-thin-structures](../../fable/chapters/ch33-wires-and-thin-structures.md) |
| **LiDAR Sensors** | Linear-mode discrete-return & full-waveform (`1064 nm` / `1550 nm`), Single-Photon LiDAR (`SPL`, `532 nm`, 100 beamlets, `1.6–3.2 ns` dead time), and Geiger-mode APD (`GmAPD`, `1064 nm`, `45–50 ns` dead time); note **SPL/GmAPD first-photon range-walk bias (`+0.05 to +0.25 m` upward step across dark-to-bright albedo boundaries unless dead-time `fpb` correction is applied)** | [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md), [ch-09/sec-09-01](../../gemini4/book/ch-09/sec-09-01.md), [ch-09/sec-09-07](../../gemini4/book/ch-09/sec-09-07.md) |
| **Metric Cameras** | Large-format digital frame cameras (Vexcel UltraCam Eagle/Osprey, Leica DMC-III) and three-line pushbroom scanners (Leica ADS100); excludes non-metric rolling-shutter consumer cameras | [ch22-photogrammetry-sfm](../../fable/chapters/ch22-photogrammetry-sfm.md), [ch-08/sec-08-01](../../gemini4/book/ch-08/sec-08-01.md) |

---

## 2. Governing Standards & Compliance Matrix

1. **USGS 3DEP Lidar Base Specification (`LBS 2024 / 2025 rev. A`):** Defines Quality Levels **QL0–QL3** (`ANPD ≥ 0.5–8 pls m⁻²`, open-terrain non-vegetated vertical accuracy `RMSE_V ≤ 0.05–0.20 m` — aligned with ASPRS Ed. 2 to report `RMSE_V` directly without `95 %` pass/fail multipliers and report `VVA` without fail threshold), inter-swath overlap consistency (`RMSD_z ≤ 0.08 m` for QL1/QL2, `≤ 0.04 m` for QL0), ASPRS LAS 1.4 R15 classifications including **Class 20** (ignored ground within hydro breakline buffers) and **Class 21** (perennial snowpack), and hydro-flattening rules (`≥ 0.81 ha` [`2 acres` / `~8,094 m²`] impoundments; `≥ 30 m` nominal river widths). See [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md) and [ch-24/sec-24-01](../../gemini4/book/ch-24/sec-24-01.md).
2. **ASPRS Positional Accuracy Standards Edition 2, v2 (June 2024):** Establishes **Tested to Meet** vs. **Produced to Meet** disclosures, direct **`RMSE_V`**, **`RMSE_H`**, and **`RMSE_3D`** accuracy classes (dropping Edition 1 / NSSDA `1.96 ×` `95 %` multipliers and dropping fixed `VVA` thresholds while retaining empirical `VVA` reporting), **quadrature addition** of checkpoint survey uncertainty ($\mathrm{RMSE}_{\text{rep}} = \sqrt{\mathrm{RMSE}_{\text{test}}^2 + \sigma_{\text{cp}}^2}$), minimum `≥ 30` withheld checkpoints per stratum (scaling up for large blocks), and `χ²` sample confidence reporting. Legacy contracts explicitly invoking pre-2024 Ed. 1 / NSSDA keep `1.96 × RMSE_z` and `95th` percentile `VVA` limits solely as labeled legacy equivalents. See [ch53-accuracy-assessment](../../fable/chapters/ch53-accuracy-assessment.md) and [ch70-specifications-guided-tour](../../fable/chapters/ch70-specifications-guided-tour.md).
3. **FEMA Elevation Guidance (Nov 2022) / *Guidelines and Standards for Flood Risk Analysis and Mapping* & USACE `EM 1110-1-1000` (2015):** Requires bare-earth hydraulic continuity (Class 17 bridge decks distinct from open culverts), `NAD83` / `NAVD88` (or modernized `NSRS` `NATRF2022`/`NAPGD2022` upon NGS operational adoption) consistency, and explicit flood-plain uncertainty reporting. See [ch53-accuracy-assessment](../../fable/chapters/ch53-accuracy-assessment.md) and [ch70-specifications-guided-tour](../../fable/chapters/ch70-specifications-guided-tour.md).
4. **ICAO Annex 15 / PANS-AIM (`Doc 10066`) eTOD & RTCA `DO-200B` / `ED-76A`:** Governs Electronic Terrain and Obstacle Data Areas 1–4 (`90 %` vertical/horizontal confidence, terrain integrity `10⁻³` [Area 1 routine] to `10⁻⁵` [Areas 2–4 essential], `EGM96`/`EGM2008` orthometric vs. `WGS 84 (G2296)` ellipsoidal height audit) and aeronautical data-chain traceability. See [ch62-navigation-and-charting](../../fable/chapters/ch62-navigation-and-charting.md) and [ch70-specifications-guided-tour](../../fable/chapters/ch70-specifications-guided-tour.md).
5. **Aviation Airworthiness, Oxygen & Laser Safety (`14 CFR`, `STC`/`Form 337`, `AC 70-1B`, `ANSI Z136.1`/`Z136.6`):** Enforces fuselage port/hardpoint structural approval, commercial survey Part 135 exemption (`§ 119.1(e)(4)(iii)`), cabin supplemental oxygen (`§ 91.211`), safe altitudes (`§ 91.119`), and `NOHD` laser safety gates cataloged in the [External Statutory Register](09-resources-and-templates.md#13-external-statutory-safety-hazmat--insurance-register).

---

## 3. Master Project Identity & Phase-Gate Sign-Off Sheet

Complete the authoritative project datum header using [template-project-header](../_shared/template-project-header.md) before authorizing Phase 01, then sign each phase gate in sequence. No flight operations, aircraft release, or client delivery may proceed across an unsigned `[GATE]`.

| Phase | Checklist File | Accountable Role | Mandatory Hard-Gate Deliverable | Signer Name & License / Cert | Timestamp (UTC) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **01** | [01-requirements-and-preplanning](01-requirements-and-preplanning.md) | Lead PLS / Survey Lead | Locked QL/ASPRS SOW, CRS/Geoid epoch, leaf-off/snow-free NDVI gate, DMP | `__________________` | `__________________` | `OPEN` |
| **02** | [02-permits-safety-insurance-cost](02-permits-safety-insurance-cost.md) | Flight-Ops Safety Officer / PM | STC/337, ATC LOAs, AC 70-1B/LCH, `91.211` O₂ plan, Aviation COI, Cost Ledger | `__________________` | `__________________` | `OPEN` |
| **03** | [03-platform-sensor-prep-and-support](03-platform-sensor-prep-and-support.md) | Calibration Lead / Geodesist | Port window `Δr_win(θ)` check, IMU Allan/lever-arm survey, 1PPS sync, ≥2 bases ≤20 km, ≥30 CPs/stratum | `__________________` | `__________________` | `OPEN` |
| **04** | [04-mission-or-flight-planning](04-mission-or-flight-planning.md) | Mission Planner / PIC | Verified sidelap/cross-strips, low-ceiling backup lines, MTA zone check, *a priori* TPU ≤ spec | `__________________` | `__________________` | `OPEN` |
| **05** | [05-underway-qc-and-field-processing](05-underway-qc-and-field-processing.md) | Sensor Operator / Field QA | Same-day fwd–rev SBET `≤ 0.10 m`, ANPD map, `RMSD_z ≤ 0.08 m`, zero corduroy, SHA-256 3-2-1 | `__________________` | `__________________` | `OPEN` |
| **06** | [06-accidents-and-emergencies](06-accidents-and-emergencies.md) | PIC / Flight-Ops Safety Officer | Briefed emergency card, ELT test, spoofing forensics protocol, NTSB `49 CFR 830` / LSO standby | `__________________` | `__________________` | `ACTIVE` |
| **07** | [07-demob-processing-and-validation](07-demob-processing-and-validation.md) | Processing/QA Lead & PLS | Post-project boresight flight + raw custody BEFORE demob, strip-adj, LAS/COG/STAC QA, ASPRS validation | `__________________` | `__________________` | `OPEN` |
| **08** | [08-error-budget-and-retrospective](08-error-budget-and-retrospective.md) | Survey Lead / PM | Reconciled error budget (`χ²` CIs, `N_eff`), AAR completed 14–30 days post-demob, Git diff | `__________________` | `__________________` | `OPEN` |

**Final Delivery Certification (Two-Person Sign-Off — Licensed Surveyor / Certified Mapping Scientist & Independent Verifier):**  
*I certify that every `[GATE]` item in Phases 01–08 was verified from recorded evidence without undisclosed waiver, that all positional accuracy claims disclose Tested-to-Meet vs. Produced-to-Meet status under ASPRS Edition 2 (with checkpoint uncertainty folded in quadrature), and that raw trajectories, calibration files, and deliverables are archived with verified SHA-256 checksums.*

- **PIC (Pilot in Command):** `____________________________` **Cert #:** `______________` **Date (UTC):** `______________`
- **Sensor Operator Lead:** `____________________________` **Cert #:** `______________` **Date (UTC):** `______________`
- **Survey / Geodesy Lead (PLS / CP):** `__________________` **License #:** `____________` **Date (UTC):** `______________`
- **Independent Verifier / QA Lead:** `_____________________` **Date (UTC):** `______________` **Project Manager:** `____________________________`

---

## 4. Directory Index & Cross-Modality Handoffs

### Phase Checklists & Reference Templates (Local)
- [01-requirements-and-preplanning.md](01-requirements-and-preplanning.md) — Standards selection, leaf-off/snow-free gating, 3DEP/CORS/airspace recon, BAA & multi-sensor window conflicts, DMP skeleton.
- [02-permits-safety-insurance-cost.md](02-permits-safety-insurance-cost.md) — STC/Form 337, Class B/C/D LOAs, AC 70-1B/ANSI Z136 NOHD, `14 CFR § 91.211` oxygen, ITAR/EAR/PLS/IATA DGR, Aviation COIs, 3DEP cost ledger.
- [03-platform-sensor-prep-and-support.md](03-platform-sensor-prep-and-support.md) — Pressurized optical window bowing, IO calibration, FOG/RLG Allan variance & lever arms, ANTEX radome, 1PPS sync, base stations, gable boresight & CPs.
- [04-mission-or-flight-planning.md](04-mission-or-flight-planning.md) — Swath/ANPD math, sidelap & cross-strips, block step-downs & low-ceiling backup, MTA `c_0/(2·n_g·PRF)`, helicopter wire/alpine oblique, `Kp`/`PDOP`, *a priori* TPU.
- [05-underway-qc-and-field-processing.md](05-underway-qc-and-field-processing.md) — In-flight INS/MTA/cloud monitoring, same-day fwd–rev SBET, spatial ANPD, `RMSD_z` & corduroy hillshades, first-sortie CP spot check, PDAL/Python scripts.
- [06-accidents-and-emergencies.md](06-accidents-and-emergencies.md) — Standalone laminated emergency card, forced landing, CFIT, bird/wire strike, hypoxia, 532/1064 nm eye exposure, GNSS spoofing (`C/N0`, `AGC`, OSNMA), NTSB 49 CFR 830/830.15, black-box freeze.
- [07-demob-processing-and-validation.md](07-demob-processing-and-validation.md) — Pre-demob closure boresight & SHA-256 raw custody gate, W&B restoration, Skáloud–Lichti strip adjustment, classification (`2/7/17/18/20/21`), COG/COPC/LAZ/STAC, ASPRS/ICESat-2/Nuth–Kääb/FFT validation.
- [08-error-budget-and-retrospective.md](08-error-budget-and-retrospective.md) — Reconciled error table, `χ²` `95 %` CIs, spatial variogram (`L_corr`, `N_eff`), anomaly diagnosis, 14–30 day AAR & checklist versioning.
- [09-resources-and-templates.md](09-resources-and-templates.md) — Critical resource & software critique, External Statutory/Hazmat/Insurance Register, and copy-ready Flight-Line, Base-Station + Photo Log, and W&B/Oxygen/Boresight Log templates.

### Shared Governance & Cross-Modality Templates
- [template-project-header.md](../_shared/template-project-header.md) — Authoritative CRS, epoch, vertical datum/geoid, and `+z ↑` sign-convention lock.
- [template-error-budget.md](../_shared/template-error-budget.md) — Standardized `1σ` quadrature & `95 %` confidence worksheet.
- [template-cost-ledger.md](../_shared/template-cost-ledger.md) — Airborne mobilization, hourly wet rate, weather standby, processing, and cloud egress ledger.
- [template-insurance-coi.md](../_shared/template-insurance-coi.md) — Aviation Hull/Liability, Non-Owned Aircraft, Over-Water, Payload Floater, and E&O coverage verification.
- [template-accident-card.md](../_shared/template-accident-card.md) — Cockpit/ground-crew quick-reference emergency notification & evidence freeze card.
- [template-aar-retrospective.md](../_shared/template-aar-retrospective.md) — Post-project retrospective and quantitative estimation-accuracy scoring template.
- [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md) — Coastal/riparian upland tie-in protocol when airborne topographic LiDAR merges with airborne topobathymetric LiDAR or vessel multibeam sonar across the land–water seam.

### Handbook Foundations
- [ch18-topographic-lidar.md](../../fable/chapters/ch18-topographic-lidar.md) | [ch22-photogrammetry-sfm.md](../../fable/chapters/ch22-photogrammetry-sfm.md) | [ch26-survey-planning.md](../../fable/chapters/ch26-survey-planning.md) | [ch70-specifications-guided-tour.md](../../fable/chapters/ch70-specifications-guided-tour.md) | [notation-and-symbols.md](../../gemini4/book/00-front-matter/notation-and-symbols.md)

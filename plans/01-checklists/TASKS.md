# TASKS.md — Execution Tracker for DEM Survey Planning & Execution Checklists

This document tracks the authoring, domain grounding, cross-referencing, automated validation, and **three-model independent peer review** (`Fable 5.2`, `Gemini 4 Carbon`, and `Gemini 4 Neon`) for all planning artifacts, shared templates, tooling, and seven DEM collection checklist suites defined in [PRD.md](PRD.md) and architected in [PLAN.md](PLAN.md).

---

## 1. Mandatory Authoring & Three-Model Independent Review Protocol

Every deliverable task (`X.Y`) follows a strict two-phase execution loop modeled on [gemini4/TASKS.md](../../gemini4/TASKS.md) and the multi-model audit discipline documented in [fable/README.md](../../fable/README.md):

### Phase A: Author Deliverable (`Write X.Y` / `Task X.Y`)
1. Draft the target file following the header block and tiered checkbox schema (`[GATE]`, `[REC]`, `[COND]`) defined in [PLAN.md](PLAN.md).
2. Ground every quantitative threshold, equation, and workflow in verified sources from `fable/`, `gemini4/`, and confirmed external standards/regulations (no invented dates, editions, rates, or citations).
3. Include concrete pass/fail thresholds, required verification evidence/artifacts, and relative links to `../../fable/...`, `../../gemini4/...`, and `../_shared/...`.
4. Ensure full coverage of all prompt questions assigned to that file plus the missed cross-cutting domains in [PRD.md](PRD.md) §4.20.

### Phase B: Three-Model Independent Verification & Fix Loop (`Review X.Y` × 3)
Immediately after completing Phase A for any task `X.Y`, invoke **three separate, independent review subagents**—each pinned to a distinct model family (**Fable 5.2**, **Gemini 4 Carbon**, and **Gemini 4 Neon**)—to audit the artifact blindly against the **10-Point Checklist Verification Rubric** before reconciliation:

| Reviewer Model | Primary Audit Lens (in addition to full 10-Point Rubric pass) |
|---|---|
| **Fable 5.2** | Standards/edition currency (S-44 Ed. 6.2.0, HSSD/FPM, LBS 2024/2025, ASPRS Ed. 2, ICAO, B-13), legal/EULA/privacy/CARE-OCAP®, cross-links to `fable/`, editorial precision, zero fabricated citations. |
| **Gemini 4 Carbon** | Mathematical physics, coordinate/sign conventions (ENU vs. NED, $+z\uparrow$ vs. $+d\downarrow$, $n_p$ vs. $n_g$, ray tracing), TPU/RSS propagation, statistical estimators ($\chi^2$, NMAD, Nuth–Kääb), runnable scripts, cross-links to `gemini4/`. |
| **Gemini 4 Neon** | Platform/field operations, physical prep (ballasting, crane SWL, STC/Form 337, isolators), permits & hazmat (UNCLOS, Part 107/91, AC 70-1B, UN 3480, ITAR/EAR), safety (RVSS, ANSI Z136 NOHD, 91.211, COLREGS), insurance/cost realism, underway QC & statutory accident clocks. |

#### 10-Point Checklist Verification Rubric
1. **Physics, Geodesy & Sign Hygiene:** Are CRS, realization, epoch, vertical datum/geoid/SEP, sign conventions ($+z\uparrow$ vs. $+d\downarrow$; ENU vs. NED), and SI units explicit and error-free?
2. **Uncertainty & Statistical Rigor:** Are accuracy requirements tied to named statistics (`RMSE_V`, `TVU_95%`, `LE95`, `NMAD`, `P95`), editions (ASPRS Ed. 2 / LBS 2024–2025 / S-44 Ed. 6.2.0), independent withheld checkpoints ($\ge 30$/stratum), and pre/post error budgets?
3. **Platform & Sensor Prep Completeness:** Are lever-arm surveys, time-sync (1PPS/PTP), calibration currency, and platform-specific mechanics (AUV ballasting/O-rings, USV dual-GNSS/COLREGS, UNOLS RVSS crane SWL/VIV, aircraft STC/Form 337/port glass, drone isolators/shutter) thoroughly covered?
4. **Permits, Export Control, Licensing & Governance Accuracy:** Are FAA (`Part 107` / `§ 107.29` / `§ 107.51(b)` / `§ 44807` heavy UAS / `§ 91.119` / `§ 119.1(e)(4)(iii)` / `AC 70-1B` / `Form 337`), `FCC Part 90`, EASA (`2019/947` SORA), UNCLOS Part XIII (`Art. 248`), NMFS MMPA/JNCC, **EAR ECCNs vs. ITAR USML**, **`UN 3480/3481` (`PI965`/`PI966` $\le 30\%$ SoC) & `UN 3090/3091` (`UN 38.3`, SDS)**, localization laws, CARE/OCAP®/GDPR, **commercial EULAs, DMP/DOI archival**, and all **9 missed domains (`PRD.md` §4.20)** accurately covered?
5. **Safety & Emergency Rigor:** Are UNOLS RVSS, ANSI Z136.1/Z136.6 NOHD, 14 CFR 91.211 oxygen, overwater ditching, **chemistry-specific Li-ion (water/AVD) vs. Li-metal (Class D) fire rules**, COLREGS, lone-worker/MUTCD safety, and statutory reporting clocks (**FAA § 107.9 10-day, NTSB 49 CFR 830 `§ 830.2`/`§ 830.5`, USCG immediate + 5-day CG-2692 + `46 CFR 4.06` `2 h/32 h` SMI + NRC immediate `33 CFR 153.203`, OSHA `29 CFR 1904.39` `8 h/24 h`**) actionable?
6. **Insurance & Cost Realism:** Are all required coverages (H&M, P&I, Jones Act/MEL, USL&H, Charterer's, **IWL, FVWC/Medevac, Waiver of Subrogation/Primary**, C&V Marine Floater, Aviation Hull+Liab+Overwater+**Class 3B/4 Ocular**, E&O, **COI expiry $\ge \text{demob}+30\text{ d}$**) and realistic cost structures (mob, Carnet/MMO/hazmat/bunker lines, standby climatology, validation 5–10 %, storage/egress, day/km² ranges with **basis & as-of date caveats**) verified?
7. **Mission/Flight Geometry & Underway QC:** Are limiting-case swath/spacing, 4–10 % crosslines, boresight/patch-test/oblique-SfM geometry, and hard underway re-fly/re-run triggers concrete and testable?
8. **De-Mob, Processing & Cross-Validation:** Are raw-custody gates (SHA-256, 3-2-1 backup before vessel/aircraft release), pinned pipelines, **runnable QC / Nuth–Kääb co-registration checks**, ICESat-2/adjacent-survey checks, **"tested vs. compiled to meet" accuracy disclosure**, and AAR learning loops complete?
9. **Format Contract, Link Integrity & Q21 Honesty:** Do files satisfy `PLAN.md` §2 (compact header block, `[GATE]`/`[REC]`/`[COND]` tags, `02` Part A/B split, Offline Binder self-containment), resolve all relative links & external register citations with zero `(verify)` placeholders, and keep `Q21` resource critiques fair?
10. **Execution Protocol — Three-Model Reconciliation & Fix Loop:** Apply all valid findings raised by `Fable 5.2`, `Gemini 4 Carbon`, and `Gemini 4 Neon` directly to the file, verify the diff, and check each model's review box `[x]` only after its findings are resolved.

---

## 2. Phase 0: Requirements, Scaffolding, Shared Templates & QA Harness

### 2.1 Planning & Specification (Current Directory)
- [x] **Task 0.0.1:** Write [PRD.md](PRD.md) containing the verbatim user prompt, 7-modality architecture, 19 substantive prompt questions + 9 missed domains (`Q20`) + `Q21` resource critique, modality matrix, and External Standards/Regulatory Register.
  - [x] **Review 0.0.1 (Fable 5.2):** Audit `PRD.md` verbatim prompt preservation, standards/edition index, resource evaluation fairness, and `fable/` cross-links.
  - [x] **Review 0.0.1 (Gemini 4 Carbon):** Audit `PRD.md` error-budget formulas, datum/sign consistency, modality matrix metrics, and `gemini4/` alignment.
  - [x] **Review 0.0.1 (Gemini 4 Neon):** Audit `PRD.md` operational/safety/permit/insurance/cost completeness across all 7 platforms and Section 4.20 missed domains.
- [x] **Task 0.0.2:** Write [PLAN.md](PLAN.md) specifying the 10-file modular layout per modality, 9-domain mapping table, Markdown checklist & Offline Binder contracts, cross-reference map, shared templates, and automated QA harness.
  - [x] **Review 0.0.2 (Fable 5.2):** Audit `PLAN.md` 10-file taxonomy coverage against `PRD.md` requirements, editorial conventions, and verified handbook links.
  - [x] **Review 0.0.2 (Gemini 4 Carbon):** Audit `PLAN.md` sign/datum header block, uncertainty/equation guardrails, and `check_checklists.py` validation specs.
  - [x] **Review 0.0.2 (Gemini 4 Neon):** Audit `PLAN.md` offline field-binder usability, shared operational templates, and cross-modal phase sequencing.
- [x] **Task 0.0.3:** Write [TASKS.md](TASKS.md) establishing the authoring/three-model review protocol and complete Phase 0–8 task list.
  - [x] **Review 0.0.3 (Fable 5.2):** Audit `TASKS.md` coverage of all 78 checklist Markdown files + 1 validator (`79` deliverables under `checklists/`), standards references, and review rubric completeness.
  - [x] **Review 0.0.3 (Gemini 4 Carbon):** Audit `TASKS.md` mathematical/validation task granularity and parameter accuracy across phases.
  - [x] **Review 0.0.3 (Gemini 4 Neon):** Audit `TASKS.md` operational/safety/insurance/emergency task assignments across all 7 modalities.

### 2.2 Portal & Shared Templates (`checklists/` & `checklists/_shared/`)
- [x] **Write 0.1:** `checklists/README.md` — Master portal, platform-selection guide, directory index, and offline field-binder instructions.
  - [x] **Review 0.1 (Fable 5.2):** Audit `checklists/README.md` for modality routing accuracy, standard references, and link integrity.
  - [x] **Review 0.1 (Gemini 4 Carbon):** Audit `checklists/README.md` platform selection thresholds (resolution, depth, area break-evens).
  - [x] **Review 0.1 (Gemini 4 Neon):** Audit `checklists/README.md` offline field-binder usage instructions and operational entry points.
- [x] **Write 0.2:** `checklists/_shared/template-project-header.md` — Standard sign-off header block (CRS/realization, epoch, vertical datum/SEP, sign convention, spec edition, optional `Platform/Tail #`, `Governing Spec` & `Independent Verifier`, RACI).
  - [x] **Review 0.2 (Fable 5.2):** Audit `template-project-header.md` against ISO 19111/19115 and `fable/chapters/ch08-horizontal-datums.md`, `ch09-vertical-datums.md`, and `ch49-metadata.md`.
  - [x] **Review 0.2 (Gemini 4 Carbon):** Audit `template-project-header.md` ENU/NED and $+z\uparrow$/$+d\downarrow$ sign/epoch fields.
  - [x] **Review 0.2 (Gemini 4 Neon):** Audit `template-project-header.md` RACI sign-off roles and field usability.
- [x] **Write 0.3:** `checklists/_shared/template-error-budget.md` — Pre-survey *a priori* vs. post-survey *a posteriori* error-budget reconciliation sheet ($\sigma$, RMSE, $\chi^2$ 95 % CI $[\hat{\sigma}\sqrt{\nu/\chi^2_{\nu,1-\alpha/2}},\,\hat{\sigma}\sqrt{\nu/\chi^2_{\nu,\alpha/2}}]$ for $\nu=n$ vs. $\nu=n-1$, one-sided $\chi^2_{n,0.95}$ test, quadrature $\sqrt{\sigma_{\text{obs}}^2-\sigma_{\text{cp}}^2}$ vs. ASPRS Ed. 2 $\sqrt{\text{RMSE}_{\text{test}}^2+\sigma_{\text{cp}}^2}$, NMAD, P95, correlation length).
  - [x] **Review 0.3 (Fable 5.2):** Audit `template-error-budget.md` compliance with ASPRS Ed. 2 (Addenda I–VI), LBS 2024/2025, and IHO S-44 Ed. 6.2.0 reporting rules.
  - [x] **Review 0.3 (Gemini 4 Carbon):** Audit `template-error-budget.md` quadrature math (sign/axis physics, $0.27\delta z_s$ vs. $0.73\delta z_s$, AUV $h_{\text{alt}}$), $\chi^2$ interval formulas ($\nu=n$ vs. $\nu=n-1$), and variogram fields.
  - [x] **Review 0.3 (Gemini 4 Neon):** Audit `template-error-budget.md` field-interpretable margin triggers and anomaly reconciliation prompts.
- [x] **Write 0.4:** `checklists/_shared/template-cost-ledger.md` — Lifecycle cost estimate and daily underway burn-rate tracker (mob/demob, permits/Carnet/MMO/hazmat/bunker lines, productive vs. weather standby, labor, 5–10 % validation, compute/egress, licensing, abandon triggers).
  - [x] **Review 0.4 (Fable 5.2):** Audit `template-cost-ledger.md` alignment with `fable/chapters/ch28-reducing-cost.md`, cost-basis caveats, and EULA/licensing lines.
  - [x] **Review 0.4 (Gemini 4 Carbon):** Audit `template-cost-ledger.md` weather-distribution modeling, cloud storage/egress math, and validation % formulas.
  - [x] **Review 0.4 (Gemini 4 Neon):** Audit `template-cost-ledger.md` daily burn-rate tracking, standby vs. productive splits, and abort-gate fields.
- [x] **Write 0.5:** `checklists/_shared/template-insurance-coi.md` — Pre-mobilization Certificate of Insurance (COI) verification matrix across Marine, Subsea, Aviation/UAS, and Professional E&O lines (`demob + >= 30 d` expiry buffer, IWL, FVWC/Medevac, Waiver of Subrogation, Class 3B/4 ocular).
  - [x] **Review 0.5 (Fable 5.2):** Audit `template-insurance-coi.md` contractual/liability alignment with `fable/chapters/ch68-legal-issues.md`.
  - [x] **Review 0.5 (Gemini 4 Carbon):** Audit `template-insurance-coi.md` technical envelope parameters (depth, altitude, payload value thresholds).
  - [x] **Review 0.5 (Gemini 4 Neon):** Audit `template-insurance-coi.md` coverage completeness (H&M, P&I, Jones Act/MEL, Aviation Hull+Liab+Ocular, Overwater, IWL, FVWC, Waiver of Subrogation, E&O, Floaters, exclusions).
- [x] **Write 0.6:** `checklists/_shared/template-accident-card.md` — Printable Emergency Response Plan (ERP) quick card, beacon registry, radio/ROC block, evidence freeze, chemistry-specific battery fire rules, and statutory reporting clocks.
  - [x] **Review 0.6 (Fable 5.2):** Audit `template-accident-card.md` legal/chain-of-custody and privacy/PII incident procedures.
  - [x] **Review 0.6 (Gemini 4 Carbon):** Audit `template-accident-card.md` raw-telemetry/black-box preservation and GNSS-spoofing log freeze steps.
  - [x] **Review 0.6 (Gemini 4 Neon):** Audit `template-accident-card.md` statutory timelines (FAA § 107.9 10-day, NTSB 49 CFR 830 `§ 830.2`/`830.5`/`830.15`, USCG immediate + 5-day CG-2692 + `46 CFR 4.06` `2h/32h` SMI + NRC immediate, UNOLS, OSHA `8h/24h`) and ICS actions.
- [x] **Write 0.7:** `checklists/_shared/template-aar-retrospective.md` — Post-survey After-Action Review (AAR) and checklist-improvement Git PR template.
  - [x] **Review 0.7 (Fable 5.2):** Audit `template-aar-retrospective.md` alignment with `fable/chapters/ch56-case-files.md` case-file structure and provenance archiving.
  - [x] **Review 0.7 (Gemini 4 Carbon):** Audit `template-aar-retrospective.md` quantitative planned-vs.-realized error and drift trend capture.
  - [x] **Review 0.7 (Gemini 4 Neon):** Audit `template-aar-retrospective.md` operational safety/near-miss, spare-parts, and cost-delta feedback loop.
- [x] **Write 0.8:** `checklists/_shared/multimodal-white-ribbon.md` — Cross-platform coastal synchronization guide (high-tide ASV/launch + low-tide bathylidar/drone + ICESat-2/SDB).
  - [x] **Review 0.8 (Fable 5.2):** Audit `multimodal-white-ribbon.md` against `fable/chapters/ch19-bathymetric-lidar.md`, `ch34-water-in-dems.md`, and `ch48-compositing.md` compositing and datum-seam rules.
  - [x] **Review 0.8 (Gemini 4 Carbon):** Audit `multimodal-white-ribbon.md` intertidal overlap geometry and VDatum/SEP uncertainty propagation against `gemini4/book/ch-13/sec-13-02.md`.
  - [x] **Review 0.8 (Gemini 4 Neon):** Audit `multimodal-white-ribbon.md` multi-asset field scheduling, tide/solar window conflicts, and safety deconfliction (NOHD/airspace/marine).

### 2.3 Automated Checklist Validator (`checklists/tools/`)
- [x] **Write 0.9:** `checklists/tools/check_checklists.py` — Automated verification script (`--phase0-only`, `--dir`, `--quiet`, `--self-test`, word floors, `01`–`08` header, `[GATE]`/`[REC]`/`[COND]` & escaped-checkbox checks, code-stripped `os.path.isfile`, `/` & escape-root guard + GitHub `#anchor` resolver to `_shared/`, `fable/`, and `gemini4/`, placeholder/`(verify)` detector, `±`/`\pm`/`+/-` & `ft`/`mi²` linter).
  - [x] **Review 0.9 (Fable 5.2):** Audit `check_checklists.py` checks against `PRD.md` §7 non-functional requirements and `fable/tools/check_book.py` conventions.
  - [x] **Review 0.9 (Gemini 4 Carbon):** Audit `check_checklists.py` regexes, statistic/unit lint rules, link normalization, and edge cases.
  - [x] **Review 0.9 (Gemini 4 Neon):** Execute and audit `check_checklists.py` CLI UX, exit codes, and diagnostics on the Phase 0 scaffold.

---

## 3. Phase 1: Underwater AUV Checklist (`checklists/underwater-auv/`)

- [x] **Write 1.0:** `checklists/underwater-auv/00-README-and-signoff.md` (AUV envelope: MBES/SAS/SSS/SBP/optical, S-44/HSSD targets, master gate sign-off).
  - [x] **Review 1.0 (Fable 5.2):** Audit standards/spec framing and link integrity in `00-README-and-signoff.md`.
  - [x] **Review 1.0 (Gemini 4 Carbon):** Audit AUV sensor resolution/footprint and sign/datum conventions in `00-README-and-signoff.md`.
  - [x] **Review 1.0 (Gemini 4 Neon):** Audit operational scope, gate summary, and roles in `00-README-and-signoff.md`.
- [x] **Write 1.1:** `checklists/underwater-auv/01-requirements-and-preplanning.md` (survey requirements, prior GEBCO TID / charts / currents / seafloor slope analysis, project instructions, spares, abort/abandon rules).
  - [x] **Review 1.1 (Fable 5.2):** Audit S-44/HSSD requirement definitions, GEBCO TID usage, and DMP/metadata skeleton.
  - [x] **Review 1.1 (Gemini 4 Carbon):** Audit depth/footprint/navigation drift requirements and pre-survey current/terrain hazard analysis.
  - [x] **Review 1.1 (Gemini 4 Neon):** Audit spares sizing, shipboard integration pre-planning, and weather/abort decision gates.
- [x] **Write 1.2:** `checklists/underwater-auv/02-permits-safety-insurance-cost.md` (UNCLOS Part XIII MSR, LNM, MMPA/sanctuary, **EAR ECCN 8A001/7A003/6A001 [ITAR USML where applicable]**, **UN 3480/3481 PI965/PI966** $\le 30\%$ SoC & **UN 3090/3091** [`UN 38.3`, SDS], O-ring/vacuum/H2/thermal runaway/LARS safety, H&M/P&I/Jones Act/subsea floater + C&V survey, vessel+AUV day-rate & weather-standby cost ledger).
  - [x] **Review 1.2 (Fable 5.2):** Audit UNCLOS Part XIII, EAR/ITAR export controls, and subsea contracting/liability clauses.
  - [x] **Review 1.2 (Gemini 4 Carbon):** Audit pressure-housing, battery energy/depth ratings, and weather-contingency distribution math.
  - [x] **Review 1.2 (Gemini 4 Neon):** Audit UN 3480/3090/3091 (`UN 38.3`, SDS) hazmat, H2/Li-ion/LARS safety gates, H&M/P&I/Jones Act/floater insurance, and charter cost ledger.
- [x] **Write 1.3:** `checklists/underwater-auv/03-platform-sensor-prep-and-support.md` (salinity ballasting & trim, pressure housing vacuum & deck overpressure/vent-valve safety, recovery-beacon bench test, compass/DVL/INS alignment, Paroscientific calibration, drop-weight corrodible link/burn-wire, USBL/iUSBL/LBL seabed transponder deployment & box-in calibration, shipboard CTD/SVP & tide gauge).
  - [x] **Review 1.3 (Fable 5.2):** Audit calibration traceability (ISO 17025, pressure/CTD/ANTEX) and USBL/LBL box-in documentation.
  - [x] **Review 1.3 (Gemini 4 Carbon):** Audit salinity/density ballasting math, lever-arm ENU/NED sign conventions, and USBL/DVL/INS alignment physics.
  - [x] **Review 1.3 (Gemini 4 Neon):** Audit O-ring/vacuum/vent-valve/beacon/drop-weight prep, LARS rigging, and transponder/tide-gauge field deployment checks.
- [x] **Write 1.4:** `checklists/underwater-auv/04-mission-or-flight-planning.md` (terrain-following altitude $h_{\text{alt}}=5\text{–}70\text{ m}$ vs. isobaric mode [scaling AUV acoustic footprint & TPU with $h_{\text{alt}}$, NOT ocean depth $d$], 100–200 %+ overlap, crosslines for bathymetric SLAM `mbnavadjust`, turn radii, descent current-drift compensation, battery 20–30 % reserve abort, *a priori* USBL + DVL-INS + TEOS-10 pressure TPU budget).
  - [x] **Review 1.4 (Fable 5.2):** Audit coverage/feature-detection conformance and observability rules in mission geometry.
  - [x] **Review 1.4 (Gemini 4 Carbon):** Audit terrain-following $h_{\text{alt}}$ vs. isobaric geometry, SAS/MBES swath math scaling with $h_{\text{alt}}$ (not $d$), and *a priori* USBL+DVL+TEOS-10 TPU budget.
  - [x] **Review 1.4 (Gemini 4 Neon):** Audit descent drift buffers, turn radii, obstacle clearance, and battery reserve abort waypoints.
- [x] **Write 1.5:** `checklists/underwater-auv/05-underway-qc-and-field-processing.md` (tethered surface wet-checks, continuous USBL innovation monitoring, abort triggers, thruster lockout before recovery, **post-recovery quick-grid & DVL/USBL loop check before leaving station**, SHA-256 + 3-2-1 backup).
  - [x] **Review 1.5 (Fable 5.2):** Audit data-custody/checksum rules, field logging, and HSSD/R2R anomaly escalation rules.
  - [x] **Review 1.5 (Gemini 4 Carbon):** Audit USBL innovation residuals, DVL bottom-lock/SLAM loop closure quick-check, and refraction checks.
  - [x] **Review 1.5 (Gemini 4 Neon):** Audit surface wet-check, live abort triggers, thruster-lockout recovery safety, and pre-departure station hold gate.
- [x] **Write 1.6:** `checklists/underwater-auv/06-accidents-and-emergencies.md` (non-surfacing/subsea entanglement/under-ice loss, Iridium/Argos/VHF/strobe/acoustic pinger homing, LARS crush/wire snap, Li-ion deck thermal runaway vs. Li-metal Class D, **NRC immediate spill + USCG immediate / 5-day CG-2692 + 46 CFR 4.06 SMI**, UNOLS / insurer clocks).
  - [x] **Review 1.6 (Fable 5.2):** Audit incident documentation, chain-of-custody preservation, and liability/insurance notice compliance.
  - [x] **Review 1.6 (Gemini 4 Carbon):** Audit acoustic beacon/pinger frequency/range parameters and black-box log recovery procedures.
  - [x] **Review 1.6 (Gemini 4 Neon):** Audit non-surfacing search/recovery flow, deck thermal-runaway response, LARS casualty, and USCG CG-2692/NRC/SMI/UNOLS clocks.
- [x] **Write 1.7:** `checklists/underwater-auv/07-demob-processing-and-validation.md` (post-mission reference check, freshwater washdown, O-ring/zinc inspection, UN 3480 PI965/PI966 discharge $\le 30\%$ SoC, **LBL transponder recovery/abandonment closeout**, ATA Carnet, TEOS-10 pressure + tide reduction, `mbnavadjust`/SLAM/CUBE/S-102/BAG processing, cross-check vs. surface MBES/prior charts).
  - [x] **Review 1.7 (Fable 5.2):** Audit S-102/BAG/ISO 19115 metadata deliverables, release review, and independent cross-validation standards.
  - [x] **Review 1.7 (Gemini 4 Carbon):** Audit TEOS-10 Saunders–Fofonoff/density integration, `mbnavadjust` SLAM tie, CUBE parameters, and Nuth–Kääb checks.
  - [x] **Review 1.7 (Gemini 4 Neon):** Audit physical de-mob sequence (washdown, O-rings, UN 3480 $\le 30\%$ discharge, ATA Carnet, raw custody before vessel release).
- [x] **Write 1.8:** `checklists/underwater-auv/08-error-budget-and-retrospective.md` (reconciled descent/DVL-scale/USBL-range/SVP/tide error table, AAR, checklist diff).
  - [x] **Review 1.8 (Fable 5.2):** Audit case-file/lessons-learned capture and archive provenance requirements.
  - [x] **Review 1.8 (Gemini 4 Carbon):** Audit *a priori* vs. *a posteriori* error-component reconciliation and spatial correlation reporting.
  - [x] **Review 1.8 (Gemini 4 Neon):** Audit AAR operational metrics (dive turnaround, battery performance, LARS near-misses, cost/day variance).
- [x] **Write 1.9:** `checklists/underwater-auv/09-resources-and-templates.md` (WHOI/MBARI/NOC/Kongsberg/MAC/NDSF/IHO/NOAA references + quality critique + AUV dive/ballast log forms).
  - [x] **Review 1.9 (Fable 5.2):** Audit bibliography accuracy, edition numbers, critique fairness, and `fable/` cross-links.
  - [x] **Review 1.9 (Gemini 4 Carbon):** Audit software workflows (`MB-System`, `Kluster`, `CARIS`, `NavLab`) and `gemini4/` cross-links.
  - [x] **Review 1.9 (Gemini 4 Neon):** Audit practical completeness of copy-ready AUV ballast, O-ring, and dive-log field forms.

---

## 4. Phase 2: Autonomous Surface Vessel Checklist (`checklists/autonomous-surface-vessel/`)

- [x] **Write 2.0:** `checklists/autonomous-surface-vessel/00-README-and-signoff.md` (micro-catamaran 1–4 m vs. semi-submersible DriX vs. 22 m Saildrone Surveyor scope, master gate sign-off).
  - [x] **Review 2.0 (Fable 5.2):** Audit IHO S-44 / NOAA HSSD / USACE scope alignment and sign-off integrity.
  - [x] **Review 2.0 (Gemini 4 Carbon):** Audit hull-class kinematic profiles, CRS/datum/sign fields, and sensor matrix accuracy.
  - [x] **Review 2.0 (Gemini 4 Neon):** Audit CONOPS supervision tiers and platform-specific gate summaries.
- [x] **Write 2.1:** `checklists/autonomous-surface-vessel/01-requirements-and-preplanning.md` (S-44 / HSSD / USACE EM 1110-2-1003, ERS vs. tide, prior charts/tide/currents/traffic AIS/surf climatology, CONOPS & supervision tier: attended vs. monitored vs. over-the-horizon).
  - [x] **Review 2.1 (Fable 5.2):** Audit standard crosswalks (S-44 vs. USACE EM 1110-2-1003 units) and archival DMP planning.
  - [x] **Review 2.1 (Gemini 4 Carbon):** Audit ERS vs. tidal reduction decision tree and current/surf environmental bounding.
  - [x] **Review 2.1 (Gemini 4 Neon):** Audit CONOPS supervision tiers (attended/monitored/OTH), AIS traffic recon, and standby/abort governance.
- [x] **Write 2.2:** `checklists/autonomous-surface-vessel/02-permits-safety-insurance-cost.md` (COLREGS Rules 5–8 lookout/radar/AIS/EO-IR/day shapes, USCG LNM & Port Authority, UNCLOS Part XIII, **FCC Part 90 / RF licensing**, **diesel & Li-ion SDS hazmat + fishery/mariner outreach**, remote e-stop/kill-switch, lost-link/lost-GNSS failsafe, cybersecurity/link encryption, **H&M/P&I/Jones Act-MEL & USL&H (chase-boat/LARS crew)/Charterer's/Equipment Floater/E&O**, USV vs. crewed ship cost ledger).
  - [x] **Review 2.2 (Fable 5.2):** Audit COLREGS legal obligations, UNCLOS Part XIII, and cybersecurity/privacy obligations.
  - [x] **Review 2.2 (Gemini 4 Carbon):** Audit lost-GNSS/link failsafe state logic and USV vs. crewed vessel cost-scaling model.
  - [x] **Review 2.2 (Gemini 4 Neon):** Audit remote e-stop hardware checks, USCG LNM/Harbor Master/FCC RF permits, fishery outreach, H&M/P&I/Jones Act-MEL/USL&H/Charterer/Floater/E&O insurance, and ROC staffing.
- [x] **Write 2.3:** `checklists/autonomous-surface-vessel/03-platform-sensor-prep-and-support.md` (hull/thruster/rudder/**watertight hatch/bilge-pump & lifting-bridle SWL** checks, dual-antenna GNSS heading baseline $\ge 0.8\text{–}1.5\text{ m}$, rigid transducer/pole alignment, 1PPS/PTP time-sync, SVS/winched SVT/CTD calibration, shore CORS/RTK base, temporary tide gauge + $\ge 3$ [`fable` §26.3; 5–10 recommended] benchmarks, patch-test & reference-surface prep).
  - [x] **Review 2.3 (Fable 5.2):** Audit IOC Manual 14 tide-gauge leveling, GNSS baseline limits, and calibration traceability.
  - [x] **Review 2.3 (Gemini 4 Carbon):** Audit dual-antenna baseline heading precision ($\sigma_\psi$), 1PPS latency math, and rigid-pole deflection checks.
  - [x] **Review 2.3 (Gemini 4 Neon):** Audit hull/propulsion/thruster bench checks, winched SVT mechanics, and shore base/tide-gauge deployment.
- [x] **Write 2.4:** `checklists/autonomous-surface-vessel/04-mission-or-flight-planning.md` (shallowest-depth swath spacing, 100–200 % overlap, $\ge 4\text{–}8\%$ crosslines, 4-step patch test, swell-heading alignment & high angular-rate $\dot{\phi}>30^\circ/\text{s}$ limits, tidal-current crabbing margin, high-tide intertidal sync, *a priori* TPU budget).
  - [x] **Review 2.4 (Fable 5.2):** Audit S-44/HSSD feature-detection coverage and crossline compliance logic.
  - [x] **Review 2.4 (Gemini 4 Carbon):** Audit shallow-edge line spacing, 4-step patch-test observability, short-chop angular-rate TPU, and crabbing math.
  - [x] **Review 2.4 (Gemini 4 Neon):** Audit sea-state limits, surf/keel clearance buffers, and high-tide intertidal operational scheduling.
- [x] **Write 2.5:** `checklists/autonomous-surface-vessel/05-underway-qc-and-field-processing.md` (ROC watch handoff, live link/AIS/COLREGS traffic monitoring, low-bandwidth swath/holiday/refraction smile telemetry, SVS divergence $>1.5\text{–}2.0\text{ m/s}$ cast trigger, raw onboard logging + SHA-256 sync).
  - [x] **Review 2.5 (Fable 5.2):** Audit raw-data immutability, DTON 24-hour (`gemini4` §24.1 / HSSD) alert rules, and metadata/environmental logging.
  - [x] **Review 2.5 (Gemini 4 Carbon):** Audit outer-beam refraction smile detection, SVS $>1.5\text{–}2.0\text{ m/s}$ trigger, and live holiday/TPU thresholds.
  - [x] **Review 2.5 (Gemini 4 Neon):** Audit ROC shift handoff checklists, COLREGS traffic intervention, and low-bandwidth SATCOM/mesh triage.
- [x] **Write 2.6:** `checklists/autonomous-surface-vessel/06-accidents-and-emergencies.md` (COLREGS collision/near-miss, capsize/surf grounding, runaway/lost-link chase-boat intercept, LiFePO4/Li-ion or diesel fire, **NRC immediate spill + USCG immediate / 5-day CG-2692 + 46 CFR 4.06 SMI**, wreck removal, insurer notice).
  - [x] **Review 2.6 (Fable 5.2):** Audit maritime liability preservation, wreck-removal legal triggers, and telemetry evidence freeze.
  - [x] **Review 2.6 (Gemini 4 Carbon):** Audit inertial/GNSS failure diagnostics and safe-towing sensor protection steps.
  - [x] **Review 2.6 (Gemini 4 Neon):** Audit chase-boat runaway intercept, capsize/fire suppression, USCG CG-2692/NRC/SMI, and P&I/H&M claims clocks.
- [x] **Write 2.7:** `checklists/autonomous-surface-vessel/07-demob-processing-and-validation.md` (post-survey reference surface & waterline check, raw drive custody BEFORE release, desalination/biofouling washdown, battery storage SoC, SBET/delayed-heave/ERS VDatum reduction, CUBE/designated soundings/BAG/S-102, crossline & white-ribbon intertidal check).
  - [x] **Review 2.7 (Fable 5.2):** Audit BAG/S-102/S-158 conformance, designated soundings, and VDatum/white-ribbon compositing rules.
  - [x] **Review 2.7 (Gemini 4 Carbon):** Audit delayed-heave/ERS separation reduction, CUBE disambiguation, **Nuth–Kääb (`xdem`)/ICP 3D co-registration & runnable QC scripts**, and crossline/intertidal overlap statistics.
  - [x] **Review 2.7 (Gemini 4 Neon):** Audit invasive-species washdown, fuel/battery de-mob safety, raw drive extraction, and gauge recovery.
- [x] **Write 2.8:** `checklists/autonomous-surface-vessel/08-error-budget-and-retrospective.md` (reconciled angular-rate/crabbing-heading/SVP/heave/datum error budget, AAR, ROC/autonomy checklist diff).
  - [x] **Review 2.8 (Fable 5.2):** Audit uncertainty disclosure and provenance archiving completeness.
  - [x] **Review 2.8 (Gemini 4 Carbon):** Audit achieved vs. budgeted TPU components (angular rates, crabbing, heel, SVP, datum).
  - [x] **Review 2.8 (Gemini 4 Neon):** Audit ROC fatigue, comms dropouts, COLREGS near-misses, and autonomy threshold updates.
- [x] **Write 2.9:** `checklists/autonomous-surface-vessel/09-resources-and-templates.md` (NOAA OMAO/OCS USV CONOPS, COLREGS/IHO/HSSD/FPM/Kluster/HydrOffice critique + USV watch-handoff & SVT log templates).
  - [x] **Review 2.9 (Fable 5.2):** Audit citations, edition dates, resource critique accuracy, and `fable/` links.
  - [x] **Review 2.9 (Gemini 4 Carbon):** Audit `Kluster`/`HydrOffice`/`MB-System`/`Qimera` workflow pointers and `gemini4/` links.
  - [x] **Review 2.9 (Gemini 4 Neon):** Audit usability of ROC watch-handoff, COLREGS incident, and winched-SVT log sheets.

---

## 5. Phase 3: UNOLS Research Cruise Checklist (`checklists/unols-research-cruise/`)

- [x] **Write 3.0:** `checklists/unols-research-cruise/00-README-and-signoff.md` (Global/Ocean/Regional UNOLS vessel classes, shipboard MBES/SBP/WCI/MVP scope, Chief Scientist / Marine Tech / Master sign-off).
  - [x] **Review 3.0 (Fable 5.2):** Audit Seabed 2030/IHO/NOAA/R2R framing and sign-off structure.
  - [x] **Review 3.0 (Gemini 4 Carbon):** Audit deep/shelf vessel acoustic frequency/footprint envelopes and datum/sign conventions.
  - [x] **Review 3.0 (Gemini 4 Neon):** Audit UNOLS command/science party sign-off authority (Master, Chief Scientist, Marine Tech).
- [x] **Write 3.1:** `checklists/unols-research-cruise/01-requirements-and-preplanning.md` (12–18+ mo UNOLS SME request via MFP, IHO S-44 / NOAA OE / Seabed 2030 / CLCS Art. 76 specs, GEBCO TID & prior cruise R2R archive review, transit-mapping plan, ship-specific Cruise Planning Manual).
  - [x] **Review 3.1 (Fable 5.2):** Audit UNCLOS Art. 76 / CLCS/11 / Seabed 2030 / GEBCO TID requirements and R2R DMP planning.
  - [x] **Review 3.1 (Gemini 4 Carbon):** Audit deepwater MBES/SBP resolution vs. depth expectations and transit-mapping geometry.
  - [x] **Review 3.1 (Gemini 4 Neon):** Audit 12–18 month UNOLS MFP/SME submission timeline, annual Ship Scheduling Committee (SSC, typ. autumn) scheduling, and Cruise Planning Manual steps.
- [x] **Write 3.2:** `checklists/unols-research-cruise/02-permits-safety-insurance-cost.md` (UNCLOS Part XIII Art. 248 statutory $\ge 6$ mo [plan $\ge 7$ mo State processing], MMPA/ESA IHA/LOA + MMOs + soft-start for 12 kHz/SBP, RVSS & App. A/B crane/winch/wire SWL, hazmat/RSO/UN 3480-3091 declarations & **ATA Carnet foreign-port customs** in MFP, **immersion-suit/medical boarding gate**, MOB/STCW watch limits, UNOLS vessel daily tiers $\$15\text{k–}\$60\text{k+/day}$ [2025–2026 basis] & NSF/institution property-at-sea insurance).
  - [x] **Review 3.2 (Fable 5.2):** Audit UNCLOS Part XIII Art. 245–249, MMPA/JNCC acoustic mitigation, and IWC whale-stranding lessons (`ch69`).
  - [x] **Review 3.2 (Gemini 4 Carbon):** Audit sonar source-level/frequency acoustic zones and weather-day Monte Carlo budgeting.
  - [x] **Review 3.2 (Gemini 4 Neon):** Audit UNOLS RVSS App. A/B, immersion-suit/medical boarding gate, MFP hazmat/RSO & ATA Carnet clearances, STCW watch limits, UNOLS daily tiers, and NSF/P&I/Jones Act coverage.
- [x] **Write 3.3:** `checklists/unols-research-cruise/03-platform-sensor-prep-and-support.md` (MAC QAT/SAT baseline report review, Westlake-style total-station hull/gondola/IMU offset survey, pole VIV & $\propto v^2$ deflection check, fuel/ballast/salinity static draft marks, POS MV GAMS/1PPS, MVP/CTD/XBT/SVS cross-cal, science van tie-downs).
  - [x] **Review 3.3 (Fable 5.2):** Audit MAC QAT/SAT documentation and dimensional offset traceability.
  - [x] **Review 3.3 (Gemini 4 Carbon):** Audit VIV Strouhal frequency ($f_s$), pole deflection $\propto v_{\text{ship}}^2$, fuel/salinity draft math, and POS MV GAMS baseline checks.
  - [x] **Review 3.3 (Gemini 4 Neon):** Audit shipyard/pier load-testing, science van deck tie-downs, and MVP/CTD/XBT shipboard readiness.
- [x] **Write 3.4:** `checklists/unols-research-cruise/04-mission-or-flight-planning.md` (depth-band swath & usable sector planning, $2\text{–}3\times d$ deep vs. $3\text{–}4\times d$ shelf line spacing, $\ge 4\text{–}5\%$ crosslines, 4-step patch test site selection, dynamic squat & turn lead-in $2\text{–}3\,T_c$ for heave settling, MVP/XBT cast cadence, *a priori* TPU budget).
  - [x] **Review 3.4 (Fable 5.2):** Audit NOAA OE / HSSD / MAC patch-test and crossline design rules.
  - [x] **Review 3.4 (Gemini 4 Carbon):** Audit Barrass/Tuck squat, turn heave-filter settling ($2\text{–}3\,T_c$), outer-beam flat-bed footprint ($D_{\text{fp,across}}(\theta)=d\beta_x/\cos^2\theta$, i.e. $4d\beta_x$ at $60^\circ$), and deepwater TPU math.
  - [x] **Review 3.4 (Gemini 4 Neon):** Audit 24/7 science watch line ordering, MVP cast speed windows, and transit-mapping integration.
- [x] **Write 3.5:** `checklists/unols-research-cruise/05-underway-qc-and-field-processing.md` (24/7 watchstanding Sis/Qinsy live TPU & bubble-sweepdown/water-column checks, SVS $>1.5\text{–}2.0\text{ m/s}$ cast trigger, nightly MB-System/CARIS/Qimera gridding & crossline junction QA, Seabed 2030 transit logging, RAID/LTO/SSD 3-2-1 SHA-256 backups).
  - [x] **Review 3.5 (Fable 5.2):** Audit R2R/NCEI logging standards, DTON/backscatter/water-column retention, and metadata logging.
  - [x] **Review 3.5 (Gemini 4 Carbon):** Audit nightly crossline junction statistics, bubble-sweepdown SNR diagnostics, and SVS divergence triggers.
  - [x] **Review 3.5 (Gemini 4 Neon):** Audit 24/7 watchstander rotation, bridge-to-lab communication, and shipboard 3-2-1 RAID/LTO/SSD backups.
- [x] **Write 3.6:** `checklists/unols-research-cruise/06-accidents-and-emergencies.md` (MOB, winch/A-frame/MVP snag or wire failure, vessel grounding/collision, hazmat spill, medevac, shipboard data loss, **NRC immediate spill + USCG immediate / 5-day CG-2692 + 46 CFR 4.06 `2h/32h` SMI**, UNOLS/NSF incident reporting & P&I notification).
  - [x] **Review 3.6 (Fable 5.2):** Audit grounding/chart liability preservation (*USS Guardian* / *USS San Francisco* lessons) and UNOLS/NSF records.
  - [x] **Review 3.6 (Gemini 4 Carbon):** Audit emergency sensor/sonar shutdown and data-corruption quarantine steps.
  - [x] **Review 3.6 (Gemini 4 Neon):** Audit RVSS MOB, crane/winch wire failure, hazmat/medevac response, USCG CG-2692/NRC/SMI, and P&I/NSF clocks.
- [x] **Write 3.7:** `checklists/unols-research-cruise/07-demob-processing-and-validation.md` (end-of-cruise draft check & calibration closure, **R2R raw/metadata/SVP/calibration handoff BEFORE disembarking**, science gear crane off-load & **off-hire deck-condition closeout**, Post-Cruise Assessment Report [PCAR], delayed heave/TrueHeave or ERS PPP reduction, CUBE/MB-System/HydrOffice QC, NCEI/DCDB submission).
  - [x] **Review 3.7 (Fable 5.2):** Audit R2R/NCEI/Seabed 2030 submission requirements, GSF/BAG/S-102 formats, and ISO 19115 provenance.
  - [x] **Review 3.7 (Gemini 4 Carbon):** Audit delayed heave (non-causal zero-phase) vs. PPK/PPP ERS reduction, ray-tracing, **Nuth–Kääb (`xdem`)/ICP 3D co-registration & runnable QC scripts**, and CUBE/crossline validation.
  - [x] **Review 3.7 (Gemini 4 Neon):** Audit pre-disembark R2R data custody gate, port crane offload & off-hire deck-condition closeout, fuel-draft log closure, and MFP PCAR completion.
- [x] **Write 3.8:** `checklists/unols-research-cruise/08-error-budget-and-retrospective.md` (reconciled outer-beam refraction/roll/heave-hook/bubble/fuel-draft error budget, cruise AAR, MAC/R2R feedback loop).
  - [x] **Review 3.8 (Fable 5.2):** Audit cruise-report transparency and MAC/R2R archival feedback.
  - [x] **Review 3.8 (Gemini 4 Carbon):** Audit reconciled outer-beam SVP, roll, heave-hook, and dynamic draft/squat residual breakdown.
  - [x] **Review 3.8 (Gemini 4 Neon):** Audit watchstanding, port-mob/demob, crane/winch readiness, and ship-day cost variance review.
- [x] **Write 3.9:** `checklists/unols-research-cruise/09-resources-and-templates.md` (UNOLS RVSS/MFP, MAC Wiki, R2R, NOAA OE Manual, MB-System, IHO S-44/C-13 critique + watchstander log & SVP/squat sheet).
  - [x] **Review 3.9 (Fable 5.2):** Audit UNOLS/MAC/R2R/NOAA OE citations, honest critique, and `fable/` cross-links.
  - [x] **Review 3.9 (Gemini 4 Carbon):** Audit `MB-System`/`Qimera`/`CARIS`/`HydrOffice` recipes and `gemini4/` cross-links.
  - [x] **Review 3.9 (Gemini 4 Neon):** Audit copy-ready watchstander log, MVP/XBT cast sheet, and fuel/draft tracking forms.

---

## 6. Phase 4: Coastal Bathylidar Checklist (`checklists/coastal-bathylidar/`)

- [x] **Write 4.0:** `checklists/coastal-bathylidar/00-README-and-signoff.md` (dual 532 nm + 1064 nm ALB systems [CZMIL, HawkEye, Chiroptera, VQ-880/840-G, RAMMS], NOAA HSSD + LBS + S-44 crosswalk sign-off).
  - [x] **Review 4.0 (Fable 5.2):** Audit topobathy system specs (`ch19`) and dual-spec crosswalk sign-off (`ch70`).
  - [x] **Review 4.0 (Gemini 4 Carbon):** Audit 532/1064 nm wavelength physics, $K_d$/Secchi envelope, and unified vertical sign convention.
  - [x] **Review 4.0 (Gemini 4 Neon):** Audit flight/safety/coastal-coordination gate summary.
- [x] **Write 4.1:** `checklists/coastal-bathylidar/01-requirements-and-preplanning.md` (Order 1a/Special vs. LBS QL1/QL2 crosswalk, single unified vertical CRS vs. land-NAVD88/sea-MLLW split guard, LAS 1.4 classes 40–45, prior MODIS/VIIRS $K_d$/Secchi & ICESat-2 water-clarity recon, tide/weather climatology, abort/deferral gates).
  - [x] **Review 4.1 (Fable 5.2):** Audit HSSD/S-44/LBS crosswalk logic, LAS 1.4 Topo-Bathy Classes 40–45, and single-datum rule.
  - [x] **Review 4.1 (Gemini 4 Carbon):** Audit ICESat-2 bathymetric clarity recon lower bound ($\sim 1\,Z_{sd}$) vs. topobathy ($1.5\text{–}2\,Z_{sd}$) / deep ALB ($2.5\text{–}3\,Z_{sd}$; $Z_{sd} \approx 1.44/K_d$) and VDatum separation uncertainties.
  - [x] **Review 4.1 (Gemini 4 Neon):** Audit turbidity/bloom/runoff window planning and seasonal deferral/abandonment rules.
- [x] **Write 4.2:** `checklists/coastal-bathylidar/02-permits-safety-insurance-cost.md` (**FAA AC 70-1B Form 7140-1** + Laser Clearinghouse, **14 CFR §§ 91.119 / 119.1(e)(4)(iii) / pilot duty limits**, **heavy-lift UAS `§ 44807 + COA` & helicopter pod STC paths**, **ANSI Z136.1/Z136.6 NOHD** ocular safety & shutter geofences, STC/Form 337 dual-band belly glass, coastal airspace/TFRs, marine/shore wildlife, overwater ditching PFD/raft/ELT, **aviation hull+liab+overwater+Class 3B/4 ocular+E&O**, ALB cost/weather-standby budget).
  - [x] **Review 4.2 (Fable 5.2):** Audit coastal wildlife/privacy/national-security bathymetry release constraints (`ch69`).
  - [x] **Review 4.2 (Gemini 4 Carbon):** Audit ANSI Z136.1/Z136.6 NOHD/MPE calculation links and water-surface specular reflection safety.
  - [x] **Review 4.2 (Gemini 4 Neon):** Audit FAA Form 7140-1/LCH, §§ 91.119/119.1/44807/pilot duty limits, STC/Form 337, overwater ditching gear (§ 91.509 Subpart F floor/PFDs/raft/ELT), aviation+overwater+ocular+E&O insurance, and ALB unit cost ranges.
- [x] **Write 4.3:** `checklists/coastal-bathylidar/03-platform-sensor-prep-and-support.md` (dual-band 532/1064 nm co-alignment & Raman channel check, **chiller & alternator/electrical bus load margin**, pressure-window thermal bowing check, lever arms & 1PPS sync, coastal CORS/base stations $\le 20\text{ km}$, project tide gauges/VDatum verification, boat/shore Secchi & turbidity/CTD logging, dry beach & submerged flat reference surface + withheld NVA/VVA/bathymetric checkpoints).
  - [x] **Review 4.3 (Fable 5.2):** Audit independent checkpoint independence rules (dry + submerged) and VDatum/tide-gauge benchmark ties.
  - [x] **Review 4.3 (Gemini 4 Carbon):** Audit 532/1064/647 nm co-alignment, pressurized optical glass refraction $\Delta r_{\text{win}}(\theta)$, and lever-arm/1PPS accuracy.
  - [x] **Review 4.3 (Gemini 4 Neon):** Audit aircraft chiller/alternator bus load integration, ground/boat Secchi team deployment, and base-station security.
- [x] **Write 4.4:** `checklists/coastal-bathylidar/04-mission-or-flight-planning.md` (15–20° constant-incidence Palmer/circular scan geometry, **strict $30^\circ\text{–}45^\circ$ sun elevation window**, **low-water flight + high-water vessel white-ribbon sync** for 100–500 m overlap, NOHD altitude floor, cross-strips 5–10 %, *a priori* ALB TPU budget incl. wave term $(1-\frac{n_a\cos\theta_w}{n_g\cos\theta_a})\delta z_s \approx (1-1/n_g)\delta z_s \approx 0.27\,\delta z_s$ on $z_b$ vs. $\approx 0.73\,\delta z_s$ on depth $d$, $n_p/n_g$, turbidity stretching).
  - [x] **Review 4.4 (Fable 5.2):** Audit JALBTCX/HSSD coverage rules and white-ribbon overlap planning.
  - [x] **Review 4.4 (Gemini 4 Carbon):** Audit Palmer constant-incidence geometry, sun-glint/shadow window ($30^\circ\text{–}45^\circ$), and ALB TPU budget ($\approx 0.27\,\delta z_s$ / $0.25\,\delta z_s$ at $20^\circ$ for $z_b$ vs. $0.73\,\delta z_s$ for $d$, $n_p$ vs. $n_g$, slope).
  - [x] **Review 4.4 (Gemini 4 Neon):** Audit NOHD minimum AGL floor, shutter geofencing, and low-tide flight vs. high-tide boat dispatch coordination.
- [x] **Write 4.5:** `checklists/coastal-bathylidar/05-underway-qc-and-field-processing.md` (live waveform SNR & bottom-extinction vs. Secchi checks, surf-zone foam/turbidity plume void tagging, NIR water-surface detection health, daily PPK forward/reverse separation, swath overlap on beach + flat seabed, SHA-256 3-2-1 ingest).
  - [x] **Review 4.5 (Fable 5.2):** Audit LAS Class 45 ("no bottom found at") logging rules, environmental metadata, and raw backup integrity.
  - [x] **Review 4.5 (Gemini 4 Carbon):** Audit waveform surface/column/bottom separation, daily PPK separation, and beach/seabed overlap checks.
  - [x] **Review 4.5 (Gemini 4 Neon):** Audit in-flight turbidity abort/re-tasking decisions and ground-team Secchi synchronization.
- [x] **Write 4.6:** `checklists/coastal-bathylidar/06-accidents-and-emergencies.md` (coastal aircraft ditching/forced landing, mid-air near-miss, **unintended 532 nm laser eye exposure / cockpit illumination**, hard landing/window strike, NTSB 49 CFR 830 immediate, FAA FSDO/LSO/**OSHA `29 CFR § 1904.39` `24 h` eye-loss & `8 h` fatality**/insurance reporting).
  - [x] **Review 4.6 (Fable 5.2):** Audit incident chain-of-custody and regulatory report documentation.
  - [x] **Review 4.6 (Gemini 4 Carbon):** Audit laser ocular exposure reconstruction parameters and hard-landing boresight invalidation triggers.
  - [x] **Review 4.6 (Gemini 4 Neon):** Audit ditching egress/PLB/USCG rescue, 532 nm eye-injury medical protocol, NTSB 49 CFR 830, **OSHA `24 h` eye-loss / `8 h` fatality**, FAA/LSO, and insurer clocks.
- [x] **Write 4.7:** `checklists/coastal-bathylidar/07-demob-processing-and-validation.md` (post-campaign boresight & flat-seabed range closure, raw waveform/SBET custody gate, **FAA Form 7140-1 / LCH / NOTAM closeout & aircraft W&B restoration**, sensor purge/window cover, waveform decomposition/deconvolution <1 m, **group index $n_g$ vs. phase index $n_p$ refraction audit** & freshwater $1.335/1.357$ vs. seawater $1.341/1.364$ salinity check, LAS 1.4 Class 40–45 + BAG/COG/TBDEM, cross-check vs. concurrent MBES/USV/ICESat-2).
  - [x] **Review 4.7 (Fable 5.2):** Audit LAS 1.4 Topo-Bathy Profile, BAG/TBDEM deliverables, and non-interpolation of surf gaps.
  - [x] **Review 4.7 (Gemini 4 Carbon):** Audit $n_p \approx 1.341$ vs. $n_g \approx 1.364$ (and freshwater $0.5\%$ salinity bias) vector Snell refraction math, deconvolution <1 m, **Nuth–Kääb (`xdem`)/ICP 3D co-registration & runnable QC scripts**, and MBES/ICESat-2 cross-checks.
  - [x] **Review 4.7 (Gemini 4 Neon):** Audit post-flight boresight closure before aircraft release, FAA 7140-1/LCH/NOTAM closeout, W&B restoration, optical port care, and custody verification.
- [x] **Write 4.8:** `checklists/coastal-bathylidar/08-error-budget-and-retrospective.md` (reconciled wave-model/refraction/pulse-stretch/seagrass/VDatum uncertainty budget, AAR, white-ribbon checklist diff).
  - [x] **Review 4.8 (Fable 5.2):** Audit stratified reporting across dry land, intertidal, clear seabed, and vegetated/turbid zones.
  - [x] **Review 4.8 (Gemini 4 Carbon):** Audit empirical wave-residual, footprint-slope, and false-bottom seagrass bias reconciliation.
  - [x] **Review 4.8 (Gemini 4 Neon):** Audit weather/clarity standby utilization, tide-window efficiency, and white-ribbon lessons learned.
- [x] **Write 4.9:** `checklists/coastal-bathylidar/09-resources-and-templates.md` (JALBTCX/NCMP, NOAA HSSD, USGS LBS, ASPRS Topo-Bathy Profile, ANSI Z136.6, FAA AC 70-1B critique + Secchi/flight-sortie/laser-safety log sheets).
  - [x] **Review 4.9 (Fable 5.2):** Audit JALBTCX/NOAA/USGS/ASPRS references, honest gap critique, and `fable/` links.
  - [x] **Review 4.9 (Gemini 4 Carbon):** Audit waveform/refraction tooling (`RiHYDRO`, `CZMIL HydroFusion`, `PDAL`, `VDatum`) and `gemini4/` links.
  - [x] **Review 4.9 (Gemini 4 Neon):** Audit Secchi/turbidity, laser-shutter, and sortie-log field sheet usability.

---

## 7. Phase 5: On-Land Drone Lidar + Imagery Checklist (`checklists/land-drone-lidar-imagery/`)

- [x] **Write 5.0:** `checklists/land-drone-lidar-imagery/00-README-and-signoff.md` (multirotor/fixed-wing/VTOL UAS lidar + RTK/PPK SfM scope, ASPRS Ed. 2 + Addendum V + Part 107/SORA gate sign-off).
  - [x] **Review 5.0 (Fable 5.2):** Audit ASPRS Ed. 2 / Addendum V / LBS framing and sign-off fields.
  - [x] **Review 5.0 (Gemini 4 Carbon):** Audit multirotor/fixed-wing/VTOL payload envelopes and SfM vs. lidar error regimes.
  - [x] **Review 5.0 (Gemini 4 Neon):** Audit PIC/VO/Survey Lead sign-off authority and pre-flight go/no-go summary.
- [x] **Write 5.1:** `checklists/land-drone-lidar-imagery/01-requirements-and-preplanning.md` (site break-even vs. crewed ALS, DSM vs. canopy-penetrating DTM choice, ASPRS Ed. 2 accuracy class + GSD/density, prior 3DEP/NDVI leaf-off/snow/obstacles/airspace/utility recon, battery/sortie logistics, weather go/no-go).
  - [x] **Review 5.1 (Fable 5.2):** Audit ASPRS Ed. 2 RMSE_V/RMSE_H classes, canopy SfM warning, and break-even cost logic (`ch28`).
  - [x] **Review 5.1 (Gemini 4 Carbon):** Audit GSD/altitude/density scaling and vegetation/snow/water phenology constraints.
  - [x] **Review 5.1 (Gemini 4 Neon):** Audit site obstacle/powerline recon, battery logistics sizing, and wind/gust abort rules.
- [x] **Write 5.2:** `checklists/land-drone-lidar-imagery/02-permits-safety-insurance-cost.md` (FAA 14 CFR Part 107 / LAANC / Remote ID / **`§ 107.29` standard night compliance & `§ 107.31 / .35 / .39 / .51(b)` waivers** / **`49 U.S.C. § 44807 + COA` heavy-lift UAS $\ge 25\text{ kg}$ [$55\text{ lb}$]** / EASA 2019/947 SORA, landowner ROE, NPS/USFS/Tribal/privacy/PLS licensure [*360 Virtual Drone*], LiPo UN 3480/3481 & SDS, pre-flight battery/prop/RTH/lost-link/wildlife/`[COND]` Class 3B-4 NOHD safety, Aviation Hull+Liab+Payload+`[COND]` Overwater/Ocular+E&O [CGL exclusion], site/GCP/processing cost sheet).
  - [x] **Review 5.2 (Fable 5.2):** Audit state surveying licensure (*360 Virtual Drone v. Ritter*), privacy/GDPR/CARE-OCAP®, and wildlife rules (`ch68`–`ch69`).
  - [x] **Review 5.2 (Gemini 4 Carbon):** Audit hover power scaling at altitude ($\rho_{\text{air}}^{-1/2}$) and wildlife buffer/noise metrics.
  - [x] **Review 5.2 (Gemini 4 Neon):** Audit FAA Part 107 (`§ 107.29`/`.51(b)`)/LAANC/Remote ID/`§ 44807 + COA`/EASA SORA, `[COND]` Class 3B/4 NOHD & overwater endorsement, LiPo UN 3480/3481 & thermal checks, RTH/lost-link safety, and Aviation Hull+Liab+E&O (CGL exclusion).
- [x] **Write 5.3:** `checklists/land-drone-lidar-imagery/03-platform-sensor-prep-and-support.md` (vibration-isolator health $f_n \ll f_{\text{blade}}/\sqrt{2}$, global vs. rolling-shutter readout check, flash hot-shoe mid-exposure sync $\Delta t_{\text{sync}}$, rigid IMU-lidar-antenna lever-arm check, local RTK/PPK base $\le 10\text{–}15\text{ km}$ on verified mark + dual 4+ hr OPUS static, **separate GCPs [edges+interior+relief] and $\ge 30$/stratum withheld CPs**, high-contrast matte 5–10 GSD targets).
  - [x] **Review 5.3 (Fable 5.2):** Audit strict GCP vs. withheld CP separation (`ch25`, `ch52`), target sizing/matte finish, and base-station mark verification.
  - [x] **Review 5.3 (Gemini 4 Carbon):** Audit isolator cutoff ($f_n \ll f_{\text{blade}}/\sqrt{2}$), rolling-shutter shear $\Delta x(r)$, hot-shoe $\Delta t_{\text{sync}}$, and lever-arm rules.
  - [x] **Review 5.3 (Gemini 4 Neon):** Audit field antenna-height double measurement (slant + vertical + photo), OPUS occupation timing, and pre-arming hardware checks.
- [x] **Write 5.4:** `checklists/land-drone-lidar-imagery/04-mission-or-flight-planning.md` (**$122\text{ m}$ [`400 ft`; $120\text{ m}$ EASA] AGL DEM terrain-following vs. canopy/barometer drift trap**, SfM 80/70 overlap + **10–20° oblique cross-grids** to break radial doming, lidar 30–50 % sidelap + cross-strip + pre/post figure-8 IMU yaw alignment, sun angle $>30^\circ$, wind $<8\text{–}10\text{ m/s}$, *a priori* UAS lidar/SfM error budget).
  - [x] **Review 5.4 (Fable 5.2):** Audit James & Robson doming mitigation, ASPRS Ed. 2 checkpoint placement (edges/corners), and sun-angle limits.
  - [x] **Review 5.4 (Gemini 4 Carbon):** Audit barometer ISA drift ($8.3\text{ m/hPa}$) vs. SRTM canopy offset in terrain following, figure-8 yaw observability, and UAS error budgets.
  - [x] **Review 5.4 (Gemini 4 Neon):** Audit VLOS/observer sightlines, battery-swap staging waypoints, and $122\text{ m}$ (`400 ft`) AGL regulatory ceiling enforcement.
- [x] **Write 5.5:** `checklists/land-drone-lidar-imagery/05-underway-qc-and-field-processing.md` (per-battery telemetry/RTK-fix/exposure-blur/gimbal check, **in-field PPK fix-ratio & quick coarse tie/strip-overlap check before leaving site**, wind/cloud/moving-object log, dual-copy SD->SSD SHA-256 verification).
  - [x] **Review 5.5 (Fable 5.2):** Audit daily log metadata, moving-object documentation, and raw-file immutability.
  - [x] **Review 5.5 (Gemini 4 Carbon):** Audit image motion-blur vs. GSD check, PPK fix-ratio, and quick coarse tie/strip-overlap residual verification.
  - [x] **Review 5.5 (Gemini 4 Neon):** Audit per-battery voltage/temp turnaround, field SD-to-dual-SSD SHA-256 workflow, and pre-packup re-fly gate.
- [x] **Write 5.6:** `checklists/land-drone-lidar-imagery/06-accidents-and-emergencies.md` (flyaway, tree/wire/water crash, bystander/property strike, LiPo thermal runaway in field/vehicle, **FAA 14 CFR § 107.9 10-day reporting [>$500 lower of repair/FMV or serious injury]**, **amended 2022 NTSB 49 CFR § 830.2 airworthiness-certificated UAS / § 830.5(a)(6) & OSHA `8h/24h`**, log/SD preservation).
  - [x] **Review 5.6 (Fable 5.2):** Audit post-crash evidence/flight-log preservation and insurance/legal disclosure protocols.
  - [x] **Review 5.6 (Gemini 4 Carbon):** Audit flyaway trajectory/last-known-coordinate telemetry recovery and damaged-IMU boresight invalidation.
  - [x] **Review 5.6 (Gemini 4 Neon):** Audit bystander/fire/powerline immediate actions, **FAA § 107.9** (10 calendar days, >$500 lower of repair/FMV or serious injury), and amended 2022 NTSB 49 CFR § 830.2 / § 830.5(a)(6) & OSHA clocks.
- [x] **Write 5.7:** `checklists/land-drone-lidar-imagery/07-demob-processing-and-validation.md` (target retrieval, LiPo storage discharge $\sim 3.8\text{ V/cell}$ + **`[COND]` UN 3480 $\le 30\%$ air-freight SoC**, post-flight log custody, PPK trajectory/figure-8 yaw solution, lidar strip adjustment & ground classification vs. SfM rolling-shutter/fixed-IO BA + water NDWI mask, withheld edge/interior CP NVA/VVA validation, COG/COPC/STAC).
  - [x] **Review 5.7 (Fable 5.2):** Audit water masking (preventing reservoir-glint volume errors `ch22`), ASPRS Ed. 2 CP reporting, and COG/COPC/STAC deliverables.
  - [x] **Review 5.7 (Gemini 4 Carbon):** Audit rolling-shutter BA model, fixed-IO vs. self-cal check, lidar strip adjustment, **Nuth–Kääb (`xdem`)/ICP 3D co-registration & runnable QC scripts**, and edge-CP doming verification.
  - [x] **Review 5.7 (Gemini 4 Neon):** Audit target/base recovery, LiPo storage discharge ($\sim 3.8\text{ V/cell}$ & `[COND]` UN 3480 $\le 30\%$ SoC), and custody sign-off before site departure.
- [x] **Write 5.8:** `checklists/land-drone-lidar-imagery/08-error-budget-and-retrospective.md` (reconciled doming/rolling-shutter/IMU-drift/geoid/canopy error table, AAR, mission-template updates).
  - [x] **Review 5.8 (Fable 5.2):** Audit honest accuracy reporting by stratum (`NVA` vs. `VVA` vs. edge CPs).
  - [x] **Review 5.8 (Gemini 4 Carbon):** Audit reconciled doming, rolling-shutter, PPK, IMU, and geoid budget magnitudes.
  - [x] **Review 5.8 (Gemini 4 Neon):** Audit battery endurance, wind-hold, and GCP-survey labor lessons learned.
- [x] **Write 5.9:** `checklists/land-drone-lidar-imagery/09-resources-and-templates.md` (ASPRS PAS Ed. 2 + Addendum V, FAA Part 107 / LAANC / B4UFLY, EASA SORA, ODM/COLMAP/PDAL critique + battery/flight/GCP log sheets).
  - [x] **Review 5.9 (Fable 5.2):** Audit ASPRS Addendum V / EASA / FAA citations, resource critique, and `fable/` cross-links.
  - [x] **Review 5.9 (Gemini 4 Carbon):** Audit `OpenDroneMap`, `COLMAP`, `PDAL`, `RTKLIB`, `Metashape`, `Pix4D` workflows and `gemini4/` cross-links.
  - [x] **Review 5.9 (Gemini 4 Neon):** Audit copy-ready LiPo battery cycle, Part 107 pre-flight, and GCP photo-log templates.

---

## 8. Phase 6: On-Land Crewed Aircraft Lidar + Imagery Checklist (`checklists/land-aircraft-lidar-imagery/`)

- [x] **Write 6.0:** `checklists/land-aircraft-lidar-imagery/00-README-and-signoff.md` (unpressurized/pressurized fixed-wing & helicopter hardpoint/pod systems, linear/SPL/GmL lidar + metric cameras, USGS LBS/3DEP & ASPRS sign-off).
  - [x] **Review 6.0 (Fable 5.2):** Audit USGS LBS 2024/2025 rev. A / ASPRS Ed. 2 / ICAO eTOD scope and sign-off integrity.
  - [x] **Review 6.0 (Gemini 4 Carbon):** Audit linear vs. SPL/GmL vs. metric camera error regimes and datum/epoch headers.
  - [x] **Review 6.0 (Gemini 4 Neon):** Audit pilot-in-command, sensor operator, and project-manager sign-off structure.
- [x] **Write 6.1:** `checklists/land-aircraft-lidar-imagery/01-requirements-and-preplanning.md` (USGS LBS 2024/2025 rev. A QL0–QL3 / FEMA / USACE EM 1110-1-1000 / ICAO eTOD DO-200B specs, leaf-off NDVI & snow-free verification, prior 3DEP/CORS/airport/TFR recon, BAA pooled acquisition & multi-sensor trade-offs, weather-climatology contingency).
  - [x] **Review 6.1 (Fable 5.2):** Audit LBS 2025 rev. A Class 20/21 rules, DO-200B integrity levels, and 3DEP BAA pooled-acquisition governance.
  - [x] **Review 6.1 (Gemini 4 Carbon):** Audit ANPD/ANPS vs. effective resolution, leaf-off penetration ratios, and climatology weather modeling.
  - [x] **Review 6.1 (Gemini 4 Neon):** Audit FBO staging, multi-sensor conflicting optimal windows (lidar leaf-off vs. imagery sun), and partial-delivery abort rules.
- [x] **Write 6.2:** `checklists/land-aircraft-lidar-imagery/02-permits-safety-insurance-cost.md` (ATC/Class B-C-D coordination, NOTAMs, TFRs, foreign overflight, **14 CFR § 119.1(e)(4)(iii) survey exemption & § 91.119**, **ATA Carnet / EAR-ITAR temporary export**, **STC / FAA Form 337 camera/lidar port**, FAA AC 70-1B / ANSI Z136.1/Z136.6 NOHD for high-power/SPL lasers, **14 CFR § 91.211 oxygen** [$>3{,}810/4{,}267/4{,}572\text{ m}$ (`12.5k/14k/15k ft`)], weight & balance, pilot duty limits, **Aviation Hull+Liab+Non-Owned Aircraft+Payload+Ocular+E&O**, aircraft hourly/mob/standby/3DEP cost tracking).
  - [x] **Review 6.2 (Fable 5.2):** Audit foreign overflight/survey licensure, EAR/ITAR dual-use temporary export (`ATA Carnet`), and privacy/sensitive-site release checks.
  - [x] **Review 6.2 (Gemini 4 Carbon):** Audit high-altitude SPL/1064 nm NOHD bounds and cabin pressure/oxygen altitude thresholds.
  - [x] **Review 6.2 (Gemini 4 Neon):** Audit STC/Form 337 airworthiness, `§ 119.1(e)(4)(iii)` / `§ 91.119`, **14 CFR § 91.211 oxygen**, W&B, pilot duty limits, Aviation Hull+Liab+Non-Owned+Ocular+E&O, ATA Carnet, and hourly/standby cost ledger.
- [x] **Write 6.3:** `checklists/land-aircraft-lidar-imagery/03-platform-sensor-prep-and-support.md` (pressurized optical port glass cleaning/AR/bowing calibration, metric camera USGS/lab IO certificate, nav-grade FOG/RLG IMU + lever-arm total-station survey, ANTEX radome check, 1PPS sync, multi-CORS/local base network $\le 20\text{ km}$, gable-roof boresight site, $\ge 30$/stratum independent NVA/VVA CPs [total station under canopy]).
  - [x] **Review 6.3 (Fable 5.2):** Audit ASPRS Ed. 2 $\ge 30$/stratum CP independence, total-station under-canopy VVA procedure, and ANTEX/NGS-58/59 rules.
  - [x] **Review 6.3 (Gemini 4 Carbon):** Audit pressurized glass meniscus bowing & $\Delta r_{\text{win}}(\theta)$, FOG/RLG Allan variance, and boresight observability planes.
  - [x] **Review 6.3 (Gemini 4 Neon):** Audit optical port inspection, multi-base deployment/redundancy, and helicopter hardpoint/pod vibration mount checks.
- [x] **Write 6.4:** `checklists/land-aircraft-lidar-imagery/04-mission-or-flight-planning.md` (AGL/speed/PRF/FOV swath & ANPS math, 20–30 % sidelap + 5–10 % cross-strips, terrain-following block step-downs & backup low-ceiling plan, **MTA zone ambiguity checks**, helicopter wire/alpine oblique tilt, sun $>30^\circ$, Kp/PDOP windows, *a priori* Hodgson–Bresnahan/LBS budget).
  - [x] **Review 6.4 (Fable 5.2):** Audit LBS spatial distribution, cross-strip norms, and Hodgson–Bresnahan/Chapter 26 budget consistency.
  - [x] **Review 6.4 (Gemini 4 Carbon):** Audit MTA range-zone folding ($c/(2\,\text{PRF})$), swath-edge roll amplification, and backup lower-AGL flight plans.
  - [x] **Review 6.4 (Gemini 4 Neon):** Audit ATC block routing, fuel-reserve/endurance legs, low-ceiling contingency, and Kp/PDOP operational windows.
- [x] **Write 6.5:** `checklists/land-aircraft-lidar-imagery/05-underway-qc-and-field-processing.md` (in-flight sensor/INS/MTA/cloud monitoring, **same-day PPK/SBET forward-reverse separation $\le 5\text{–}10\text{ cm}$**, density/spatial-distribution map, inter-swath $\text{RMSD}_z$ & corduroy hillshade check, first-sortie partial checkpoint check, SHA-256 3-2-1 backup, re-fly trigger enforcement).
  - [x] **Review 6.5 (Fable 5.2):** Audit LBS inter-swath ($\le 8\text{ cm}$ QL2) & intra-swath thresholds, corduroy case-file checks, and raw immutability.
  - [x] **Review 6.5 (Gemini 4 Carbon):** Audit forward/reverse SBET separation, overlap residual signatures (roll vs. pitch vs. height), and first-sortie CP check.
  - [x] **Review 6.5 (Gemini 4 Neon):** Audit in-flight operator triage, overnight processing turnaround before next sortie, and re-fly enforcement gates.
- [x] **Write 6.6:** `checklists/land-aircraft-lidar-imagery/06-accidents-and-emergencies.md` (forced landing/CFIT/bird strike/wire strike [helicopter]/hypoxia/laser exposure/GNSS spoofing in interference zones, ELT/flight-following SAR, **NTSB 49 CFR 830 immediate notification**, FAA FSDO, **OSHA `29 CFR § 1904.39` `8h/24h`**, insurer, black-box/flight-data freeze).
  - [x] **Review 6.6 (Fable 5.2):** Audit GNSS spoofing forensics (`ch56.19`, raw observable logging) and legal/investigative evidence retention.
  - [x] **Review 6.6 (Gemini 4 Carbon):** Audit GNSS interference C/N0 & AGC checks and post-incident sensor/boresight recalibration gates.
  - [x] **Review 6.6 (Gemini 4 Neon):** Audit CFIT/wire-strike/hypoxia/forced-landing SAR response, **NTSB 49 CFR 830 immediate** clock, **OSHA `8h/24h`**, FAA FSDO, and insurer notice.
- [x] **Write 6.7:** `checklists/land-aircraft-lidar-imagery/07-demob-processing-and-validation.md` (post-project boresight closure flight BEFORE aircraft demob, raw data/SBET custody gate, sensor removal/W&B restoration, RTS SBET + rigorous strip adjustment + noise/Class 2/7/17/18/20/21 classification QA + hydro-flattening + Pixel-is-Area COG/COPC/LAZ 1.4, NVA/VVA/ICESat-2/adjacent-tile validation).
  - [x] **Review 6.7 (Fable 5.2):** Audit LBS 2025 rev. A classification (Class 20/21, bridges, hydro-flattening), COPC/COG/LAZ 1.4, and ISO 19115/STAC.
  - [x] **Review 6.7 (Gemini 4 Carbon):** Audit RTS SBET, Skaloud–Lichti strip adjustment, `Pixel-is-Area` convention, Type I/II confusion matrix, **Nuth–Kääb (`xdem`)/ICP 3D co-registration & runnable QC scripts**, and ICESat-2 checks.
  - [x] **Review 6.7 (Gemini 4 Neon):** Audit post-project boresight flight before aircraft departure, aircraft W&B restoration, and final raw custody gate.
- [x] **Write 6.8:** `checklists/land-aircraft-lidar-imagery/08-error-budget-and-retrospective.md` (reconciled trajectory/attitude-edge/boresight/MTA/geoid/canopy error table, $\chi^2$ CIs, AAR, aircraft/weather contingency diff).
  - [x] **Review 6.8 (Fable 5.2):** Audit ASPRS Ed. 2 quadrature checkpoint inclusion ($\sqrt{\text{RMSE}_{\text{test}}^2+\sigma_{\text{cp}}^2}$ vs. true-error $\sqrt{\sigma_{\text{obs}}^2-\sigma_{\text{cp}}^2}$) and stratified NVA/VVA disclosure.
  - [x] **Review 6.8 (Gemini 4 Carbon):** Audit $\chi^2$ RMSE confidence bounds ($\nu=n$ zero-mean RMSE vs. $\nu=n-1$ sample $\sigma$), variogram correlation length, and error-table balance.
  - [x] **Review 6.8 (Gemini 4 Neon):** Audit mobilization/ferry efficiency, weather-standby forecasting accuracy, and crew/aircraft AAR actions.
- [x] **Write 6.9:** `checklists/land-aircraft-lidar-imagery/09-resources-and-templates.md` (USGS LBS 2024/2025, ASPRS Ed. 2 + LiDAR Manual, USACE EM 1110-1-1000, FEMA G&S, FAA 91.211/337/AC 70-1B critique + flight/base-station/boresight log forms).
  - [x] **Review 6.9 (Fable 5.2):** Audit LBS/ASPRS/USACE/FEMA/FAA citations, critical gap analysis, and `fable/` links.
  - [x] **Review 6.9 (Gemini 4 Carbon):** Audit `PDAL`/`laspy`/`lidR`/`TerraMatch`/`POSPac`/`xdem` tooling and `gemini4/` links.
  - [x] **Review 6.9 (Gemini 4 Neon):** Audit flight-line log, base-station datasheet, and aircraft W&B/oxygen log templates.

---

## 9. Phase 7: Satellite-Built Elevations Checklist (`checklists/satellite-elevation/`)

- [x] **Write 7.0:** `checklists/satellite-elevation/00-README-and-signoff.md` (optical stereo/tri-stereo, CORONA/KH-9 historical, single/repeat InSAR, SWOT/ICESat-2/GEDI control, SDB under IHO B-13; tasking/processing/QA sign-off).
  - [x] **Review 7.0 (Fable 5.2):** Audit multi-architecture satellite taxonomy (optical, film, InSAR, altimetry, SDB) and IHO B-13 framing.
  - [x] **Review 7.0 (Gemini 4 Carbon):** Audit orbital error regimes (pointing jitter, $B/H$, $h_{\text{amb}}$, penetration bias) and sign/datum headers.
  - [x] **Review 7.0 (Gemini 4 Neon):** Audit tasking buyer, ground-truth lead, and QA acceptance sign-off structure.
- [x] **Write 7.1:** `checklists/satellite-elevation/01-requirements-and-preplanning.md` (DSM vs. radar scattering-center vs. SDB-depth ontology, CE90/LE90 vs. RMSE/SDB depth-bin metrics, **archive vs. new tasking audit** [Copernicus GLO-30, ArcticDEM/REMA/EarthDEM, NASADEM, NISAR, SWOT, ICESat-2], cloud/seasonal/snow/tide climatology, delivery-rejection criteria).
  - [x] **Review 7.1 (Fable 5.2):** Audit public-product license/accuracy comparison (`ch55`/App. E), LE90/CE90 conversions (`ch70`), and ontology honesty.
  - [x] **Review 7.1 (Gemini 4 Carbon):** Audit radar penetration bias (X/C/L/P-band canopy & firn), SDB $K_d$ depth limit, and archive screening math.
  - [x] **Review 7.1 (Gemini 4 Neon):** Audit archive-first vs. commercial tasking go/no-go gate and explicit vendor SLA rejection criteria.
- [x] **Write 7.2:** `checklists/satellite-elevation/02-permits-safety-insurance-cost.md` (NOAA CRSRA / shutter control, **commercial EULA derivative-DEM vs. raw-imagery redistribution clauses**, national restriction/localization laws [India 2021, China GCJ-02], GDPR/sensitive-site release review, **ground-truth/corner-reflector ROE/DOT roadside permits & crew field safety** [MUTCD Class 2/3 PPE, heat/cold, remote lone-worker inReach], E&O + **Inland Marine Floater + FVWC/Medevac** + ground CGL/auto insurance, commercial tasking per-km² pricing [as-of basis], min AOI $\ge 25\text{ km}^2$, cloud/priority uplifts, HPC/cloud egress ledger).
  - [x] **Review 7.2 (Fable 5.2):** Audit commercial EULA derivative-DEM terms (`gemini4` §27.1.3 / `fable` §68.3), Kyl–Bingaman/CRSRA, India/China laws, and GDPR/mosaic release review.
  - [x] **Review 7.2 (Gemini 4 Carbon):** Audit HPC compute/storage/egress sizing and corner-reflector placement constraints.
  - [x] **Review 7.2 (Gemini 4 Neon):** Audit commercial tasking pricing structures (e.g., Pléiades Neo stereo/tri-stereo per-km², min AOI, cloud uplifts), ROE/DOT permits, E&O/Inland Marine Floater/FVWC/CGL/Auto insurance, and lone-worker/MUTCD ground-crew safety.
- [x] **Write 7.3:** `checklists/satellite-elevation/03-platform-sensor-prep-and-support.md` (sensor selection & RPC/POD ephemeris tier, **ground deployment where required**: GNSS-surveyed photo-identifiable GCPs/checkerboards/Siemens stars [5–10 GSD], **triangular** trihedral SAR corner reflectors [$\sigma_{\max}=4\pi a^4/3\lambda^2$, inner orthogonal leg $a$], independent withheld checkpoints, tide/water-level model $\eta(t)$ for SDB, SDB sonar/ICESat-2 calibration depths).
  - [x] **Review 7.3 (Fable 5.2):** Audit CEOS PICS/test-site guidance (`ch25`), GCP vs. withheld CP rules, and SDB calibration-source hierarchy (`ch23`).
  - [x] **Review 7.3 (Gemini 4 Carbon):** Audit triangular trihedral RCS formula ($\sigma_{\max}=4\pi a^4/3\lambda^2$, inner leg $a$), optical target sizing, RPC error vs. POD accuracy, and SDB $\eta(t)$ tide datum math.
  - [x] **Review 7.3 (Gemini 4 Neon):** Audit field deployment/anchoring of targets & reflectors, land-access safety, and target visibility checks prior to overpass.
- [x] **Write 7.4:** `checklists/satellite-elevation/04-mission-or-flight-planning.md` (tasking window & LTAN/LTDN sun-angle selection, stereo/tri-stereo convergence angles [$15^\circ\text{–}25^\circ$ urban vs. $30^\circ\text{–}45^\circ$ open, $B/H$], off-nadir & cloud-cover SLA thresholds, InSAR $B_\perp < B_{\perp,\text{crit}}$ & $h_{\text{amb}}$ + ascending/descending pairs to cover layover/shadow, temporal decorrelation limits, *a priori* stereo/InSAR/SDB error budget).
  - [x] **Review 7.4 (Fable 5.2):** Audit tri-stereo occlusion vs. $B/H$ trade-offs (`ch22`) and IHO B-13 SDB geometry/glint bounds (`ch23`).
  - [x] **Review 7.4 (Gemini 4 Carbon):** Audit stereo $\sigma_z = \frac{H}{B}\,\text{GSD}\,\sigma_{p,\text{px}}$ (pixels), InSAR $h_{\text{amb}} = \frac{\lambda R \sin\theta_i}{p B_\perp}$ ($p \in \{1,2\}$, incidence $\theta_i$), layover/shadow slopes, and SDB sensitivity.
  - [x] **Review 7.4 (Gemini 4 Neon):** Audit tasking-portal order configuration (commercial vendor minimum AOI/corridor-width gates, cloud %, priority tier, pass deadline) and go/no-go order gates.
- [x] **Write 7.5:** `checklists/satellite-elevation/05-underway-qc-and-field-processing.md` (tasking monitor & **vendor delivery acceptance/rejection gate within contract window**: quick-look cloud/haze/glint screening, actual convergence/$B/H$ & off-nadir audit, stereo overlap/saturation check, InSAR coherence/burst alignment check, immediate raw Level-1/RPC/SLC checksum & immutable archive).
  - [x] **Review 7.5 (Fable 5.2):** Audit metadata preservation, EULA tagging, and raw Level-1/RPC/SLC immutability rules.
  - [x] **Review 7.5 (Gemini 4 Carbon):** Audit actual $B/H$, sun-glint geometry, snow/sand saturation, and InSAR coherence/APS quick-screen thresholds.
  - [x] **Review 7.5 (Gemini 4 Neon):** Audit contract rejection-window SLA clock, vendor re-tasking trigger, and archive/checksum verification.
- [x] **Write 7.6:** `checklists/satellite-elevation/06-accidents-and-emergencies.md` (tasking window missed/cloud-out escalation, vendor failed-collection re-tasking/refund trigger, orbital anomaly/corrupted telemetry, **ground-truth field crew accident** [road strike, cliff fall, heat/cold, detention + OSHA `8h/24h` & consular escalation], EULA/classified/restricted data spill, cyber/HPC data corruption).
  - [x] **Review 7.6 (Fable 5.2):** Audit EULA/ITAR/restricted-country data-spill containment and legal notification.
  - [x] **Review 7.6 (Gemini 4 Carbon):** Audit corrupted RPC/SLC/telemetry detection and unrecoverable-scene fallback fusion strategies.
  - [x] **Review 7.6 (Gemini 4 Neon):** Audit ground-crew trauma/roadside/remote-SOS response, OSHA `29 CFR § 1904.39` `8h/24h` & consular/legal detention clocks, vendor SLA dispute/refund escalation, and cyber/HPC recovery.
- [x] **Write 7.7:** `checklists/satellite-elevation/07-demob-processing-and-validation.md` (ground crew target/reflector recovery & site closeout, tasking order closeout, **rigorous processing**: ASP/SETSM/CARS/MicMac RPC bias + `jitter_solve` + SGM/MGM + water/cloud/snow mask; KH-9 1081-reseau dewarp; ISCE/GMTSAR/SNAP APS + SNAPHU unwrap + geocoding DEM circularity check; ACOLITE/glint + Stumpf/physics SDB + tide reduction; **Nuth–Kääb 3D co-registration + ICESat-2/GEDI/lidar/GCP validation** + 2D FFT/histogram forensics + COG/STAC).
  - [x] **Review 7.7 (Fable 5.2):** Audit geocoding-DEM circularity disclosure (`ch21.6`), KH-9/CORONA provenance, water/cloud masks, and COG/STAC release review.
  - [x] **Review 7.7 (Gemini 4 Carbon):** Audit `jitter_solve` wavelength $\Lambda_k=v_{\text{ground}}/f_k$ (pushbroom ground-scan velocity $v_{\text{ground}}=\text{GSD}_y/\Delta t_{\text{line}}$, distinct from optical $v_g=c_0/n_g$), SNAPHU phase-unwrapping jump detection, SDB Stumpf/refraction math, and runnable Nuth–Kääb/2D-FFT forensics.
  - [x] **Review 7.7 (Gemini 4 Neon):** Audit ground-crew demob/target recovery, HPC cost/egress cleanup, and vendor SLA sign-off.
- [x] **Write 7.8:** `checklists/satellite-elevation/08-error-budget-and-retrospective.md` (reconciled pointing-jitter/B-H/APS/unwrapping/firn-or-canopy penetration/SDB glint-albedo error table, AAR, tasking/SLA checklist diff).
  - [x] **Review 7.8 (Fable 5.2):** Audit honest disclosure of ML/super-resolution vs. measured cells and regional bias caveats.
  - [x] **Review 7.8 (Gemini 4 Carbon):** Audit reconciled stereo/InSAR/SDB error magnitudes against ICESat-2/3DEP/lidar benchmarks.
  - [x] **Review 7.8 (Gemini 4 Neon):** Audit tasking wait-time, cloud-rejection rate, per-$\text{km}^2$ realized cost, and SLA negotiation lessons.
- [x] **Write 7.9:** `checklists/satellite-elevation/09-resources-and-templates.md` (NASA ASP, PGC SETSM, CEOS Cal/Val & ARD, ESA SNAP, ISCE2/3, SlideRule/`icepyx`, IHO B-13, Copernicus/TanDEM-X handbooks critique + tasking spec & scene acceptance cards).
  - [x] **Review 7.9 (Fable 5.2):** Audit ASP/SETSM/CEOS/IHO B-13/Copernicus/NISAR/SWOT citations, critique depth, and `fable/` links.
  - [x] **Review 7.9 (Gemini 4 Carbon):** Audit `ASP`, `SETSM`, `CARS`, `ISCE3`, `GMTSAR`, `ACOLITE`, `SlideRule`, `xdem` workflows and `gemini4/` links.
  - [x] **Review 7.9 (Gemini 4 Neon):** Audit copy-ready satellite tasking order spec and quick-look acceptance/rejection cards.

---

## 10. Phase 8: Cross-Modality Audit, Automated Validation & Integration

- [x] **Task 8.1:** Run `python3 checklists/tools/check_checklists.py` across all **78 checklist Markdown files** (`README.md`, `7` `_shared/`, `7 × 10` modality files) plus planning docs (`plans/01-checklists/`) and achieve **0 hard failures, 0 warnings, 0 broken links, 0 unresolved `(verify)` flags**.
  - [x] **Review 8.1 (Fable 5.2):** Audit `check_checklists.py` full-corpus report for zero unresolved `(verify)` flags and 100 % link integrity.
  - [x] **Review 8.1 (Gemini 4 Carbon):** Audit `check_checklists.py` unit/sign/statistic warnings (`±`/`\pm`/`+/-`, `ft`/`mi²`) across all 78 checklist Markdown files.
  - [x] **Review 8.1 (Gemini 4 Neon):** Verify reproducible execution of `check_checklists.py` from clean workspace state with exit code 0.
- [x] **Task 8.2:** Perform cross-modality consistency review (`fable/` Ch. 26/70/App. G alignment, datum/epoch/sign harmonization across `coastal-bathylidar/` ↔ `autonomous-surface-vessel/` ↔ `unols-research-cruise/`, **9-domain coverage matrix across all 7 modalities**, **Phase 0 `_shared/` & `README.md` back-sync** after Phases 1–7, and consistent insurance/statutory clock tables).
  - [x] **Review 8.2 (Fable 5.2):** Audit cross-modality consistency against `fable/` App. G, Ch. 26, Ch. 68–70, and the **§4.20 9-domain × 7-modality coverage matrix**.
  - [x] **Review 8.2 (Gemini 4 Carbon):** Audit cross-modality datum/epoch, ENU/NED, white-ribbon overlap formulas, and Phase 0 `_shared/` back-sync consistency across all 7 suites.
  - [x] **Review 8.2 (Gemini 4 Neon):** Audit cross-modality consistency of insurance lines, statutory accident clocks, UN 3480/3090/3091 safety gates, and Phase 0 back-sync updates.
- [x] **Task 8.3:** Verify root [README.md](../../README.md) / TeachBook integration options, verify **offline field-binder usability** (`01`–`08` `[GATE]`s self-contained offline & `06` standalone printable), and confirm `git status` contains only intended deliverables with clean formatting.
  - [x] **Review 8.3 (Fable 5.2):** Audit final repository cleanliness, licensing/attribution alignment, and documentation accuracy.
  - [x] **Review 8.3 (Gemini 4 Carbon):** Audit final file manifest counts (`78` checklist Markdown files + `1` validator = `79` deliverables under `checklists/`, plus `3` planning docs in `plans/01-checklists/`).
  - [x] **Review 8.3 (Gemini 4 Neon):** Audit final readiness for offline field-binder deployment (`01`–`08` standalone gates & `06` quick-cards) and clean `git status` / diff inspection.

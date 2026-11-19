# Architecture & Implementation Plan (`PLAN.md`): Multi-Modality DEM Survey Checklists

This document defines the file architecture, checklist engineering standards, knowledge-integration mapping, shared templates, automated verification harness, and phased execution plan to fulfill [PRD.md](PRD.md).

---

## 1. Repository & Directory Architecture

All deliverables live under `checklists/` at the repository root, organized into shared cross-cutting scaffolding, automated validation tooling, and **seven self-contained modality subdirectories**:

```text
dem-handbook-checklists/
├── plans/01-checklists/
│   ├── PRD.md                              # Product requirements (includes verbatim user request)
│   ├── PLAN.md                             # This architecture and implementation plan
│   └── TASKS.md                            # Granular authoring and verification tracker
└── checklists/
    ├── README.md                           # Master portal: modality selector, white-ribbon sync guide, usage SOP
    ├── _shared/                            # Reusable templates, ledgers, and reference cards (copied/adapted per project)
    │   ├── template-project-header.md      # Sign-off header: Datum, Realization, Epoch, Sign Convention, Roles
    │   ├── template-error-budget.md        # A priori vs. a posteriori RSS/TPU reconciliation sheet
    │   ├── template-cost-ledger.md         # Mob/platform/weather-standby/labor/validation/egress burn-rate sheet
    │   ├── template-insurance-coi.md       # Marine (H&M/P&I/Jones Act), Aviation/UAS Hull+Liab, E&O verification matrix
    │   ├── template-accident-card.md       # ICS quick-action card & statutory clocks (FAA 107.9, NTSB 830, USCG CG-2692)
    │   ├── template-aar-retrospective.md   # Post-survey After-Action Review & checklist-diff template
    │   └── multimodal-white-ribbon.md      # Cross-platform sync guide (High-Tide ASV/Vessel + Low-Tide Lidar + SDB)
    ├── tools/
    │   └── check_checklists.py             # Automated structure, GATE tag, link, unit, and citation linter
    ├── underwater-auv/                     # Modality 1: Underwater AUV bathymetric/SAS/optical surveys
    ├── autonomous-surface-vessel/          # Modality 2: ASV / USV shallow-to-ocean hydrographic surveys
    ├── unols-research-cruise/              # Modality 3: UNOLS crewed oceanographic multibeam cruises
    ├── coastal-bathylidar/                 # Modality 4: Airborne (and heavy-UAS) 532nm/1064nm coastal bathylidar
    ├── land-drone-lidar-imagery/           # Modality 5: On-land UAS (drone) LiDAR + SfM photogrammetry
    ├── land-aircraft-lidar-imagery/        # Modality 6: On-land crewed fixed-wing & helicopter LiDAR + imagery
    └── satellite-elevation/                # Modality 7: Satellite stereo/tri-stereo, InSAR, altimetry & SDB DEMs
```

### 1.1 Standardized 10-File Layout Inside Each Modality Subdirectory

To guarantee uniform navigation, printable field-binder modularity, and clean review diffs, every one of the 7 modality subdirectories implements the exact same 10-file structure:

| File | Lifecycle Stage & Required Prompt Topics Covered |
|---|---|
| `00-README-and-signoff.md` | Modality overview, sensor/platform envelope, governing specs summary, project sign-off cover sheet, go/no-go gate summary, and cross-link index to all files `01`–`09`. |
| `01-requirements-and-preplanning.md` | **Q1** Survey requirements (use/loss function, DSM/DTM/TBDEM ontology, CRS/datum/epoch/units, accuracy metrics); **Q3** Pre-existing documents & data collection/analysis (GEBCO TID, ICESat-2, charts/sectionals, NGS marks, climatology, Kp, HTDP); **Q4** Pre-planning (break-even audit, project instructions, metadata skeleton, naming/3-2-1 backup, spares, abandonment criteria). |
| `02-permits-safety-insurance-cost.md` | Organized into **Part A: Pre-Mob Admin (Permits, COIs, Budget)** and **Part B: Daily Pre-Sortie Safety & Burn-Rate Gates**. **Q7** Permits, clearances, export control (EAR/ITAR), localization laws, UN `3480/3481` & `3090/3091` hazmat (`UN 38.3`, SDS), `49 U.S.C. § 44807` heavy UAS, `§ 119.1(e)(4)(iii)` / `§ 91.119`, FCC Part 90, CARE/OCAP® Indigenous & MMPA/fishery liaison; **Q8** Platform/crew/laser/marine/aviation safety checks; **Q12** Insurance (H&M, P&I, Jones Act, Aviation Hull+Liab+Overwater+Ocular, IWL, FVWC, C&V floaters, E&O); **Q9** Cost estimation & burn-rate tracking; **Q20** Crew fatigue/watch limits & cybersecurity. |
| `03-platform-sensor-prep-and-support.md` | **Q2** Platform & sensor prep (lever-arm survey, axis diagrams, 1PPS/PTP time-sync, calibration certificates, ballasting/O-rings/vent-valves/COLREGS/RVSS crane SWL/STC belly glass & alternator load/helicopter hardpoint/vibration isolation); **Q5** Field support deployments (GNSS bases/CORS, tide gauges + $\ge 3$ [`fable` §26.3] / `5–10` recommended benchmarks, USBL/LBL box-in, CTD/MVP/SVS, Secchi, targets, triangular corner reflectors, independent withheld checkpoints $\ge 30$/stratum). |
| `04-mission-or-flight-planning.md` | **Q6** Mission/flight/dive/orbital planning (limiting-case swath & line spacing, overlap/sidelap, 4–10 % orthogonal crosslines, 4-step patch test / boresight / oblique SfM cross-grids, figure-8 yaw alignment, sun-elevation $30^\circ\text{–}45^\circ$, tidal white-ribbon sync, 400 ft AGL DEM trap, satellite $B/H$ & $h_{\text{amb}}$); **Q10** Pre-survey analytical TPU/RSS error budget & observability rank verification. |
| `05-underway-qc-and-field-processing.md` | **Q13** Underway validation while operating (trajectory forward/reverse separation, live TPU green/yellow/red maps, holiday accumulators, crossline junction alerts, SVS cast triggers, AUV post-dive quick-grid, bathylidar waveform/Secchi gate, satellite quick-look acceptance); **Q14** In-field non-destructive ingest, SHA-256 checksums, 3-2-1 backup, field triage vs. irreversible editing, daily environmental/moving-object logs. |
| `06-accidents-and-emergencies.md` | **Q11** Modality-specific accident taxonomy (loss/flooding/entanglement/collision/flyaway/ditching/laser exposure/MOB/data loss), immediate preserve-life & beacon-recovery actions, evidence/log freeze, and statutory reporting clocks (FAA § 107.9 10-day, NTSB 49 CFR 830 immediate, USCG CG-2692, UNOLS/NSF, OSHA/LSO, insurance underwriter notice). |
| `07-demob-processing-and-validation.md` | **Q15** Demobilization (post-survey closure lines, draft/benchmark tie checks, checksummed custody handoff BEFORE releasing vessel/aircraft, washdown/desalination, UN 3480 $\le 30\%$ discharge, ATA Carnet, PCAR); **Q16** End-to-end processing pipeline (pinned env/geoids, SBET/BA/refraction/CUBE/classification/gridding/Pixel-is-Area/COG/COPC/BAG/S-102/STAC/release review); **Q17** Cross-check with prior/contemporaneous data (Nuth–Kääb co-registration, withheld checkpoints, ICESat-2/GEDI/SWOT, intertidal overlap, 2D FFT/hillshade forensics). |
| `08-error-budget-and-retrospective.md` | **Q18** Reconciled *a priori* vs. *a posteriori* error-source & magnitude budget (stratified by cover/slope/depth/angle/day, variogram correlation length, anomaly root-cause table); **Q19** Post-survey After-Action Review (AAR) / continuous learning loop (planned vs. actual cost/schedule/safety/accuracy, Git checklist diff, calibration drift logs). |
| `09-resources-and-templates.md` | **Q21** Modality-specific resource bibliography & quality critique (handbooks, manuals, software, public portals, External Standards/Regulatory Authority Register), copy-ready field log forms, and explicit relative links into `../../fable/` and `../../gemini4/`. |

### 1.2 Nine Cross-Cutting Missed Domains (`PRD.md` §4.20) Mapping
Every modality suite distributes the 9 cross-cutting planning domains from `PRD.md` §4.20 across standardized lifecycle files so nothing falls between phases:

| §4.20 Missed Domain | Primary File Home(s) | Supporting `_shared/` & Secondary Files |
|---|---|---|
| **1. Data Security, Export Control (EAR/ITAR), Sovereignty, Privacy, CARE/OCAP®** | `02` (Part A), `07` (release review) | `01`, `06` (spill/breach), `template-project-header.md` |
| **2. Environmental, Wildlife, Biofouling & Local Fishery / Community Liaison** | `02` (MMPA/JNCC/fishery/beach outreach), `07` (washdown) | `01`, `05` (MMO logs) |
| **3. Supply Chain, Customs, ATA Carnet, Hazmat (`UN 3480/3090/3091`) & Spares** | `01` (spares sizing), `02` (Carnet/hazmat freight) | `03` (bench), `07` (export closure), `template-cost-ledger.md` |
| **4. Human Factors, Crew Fatigue, STCW/FAA Duty Limits & Watch Handoffs** | `02` (Part B daily gates), `05` (watch handoff) | `00`, `03` (fatigue-proof offset double-check) |
| **5. Cybersecurity, RF Spectrum (`FCC Part 90`) & GNSS Interference Resilience** | `02` (comms/cyber), `05` (`C/N_0`/AGC logs) | `03` (RF test), `06` (GNSS-spoof/cyber freeze) |
| **6. Contractual Governance, SOW Acceptance, Licensure (PLS/Cat A) & EULAs** | `01` (SOW/EULA), `02` (licensure/COI) | `07` (acceptance), `08` (remedies), `template-cost-ledger.md` |
| **7. Data Management Plan (DMP), Raw Immutability, Repository Archival & DOIs** | `01` (DMP/naming), `05` (3-2-1 SHA-256), `07` (R2R/NCEI/BagIt) | `08` (drift logs), `template-project-header.md` |
| **8. Multi-Modal Synchronization Across the Land–Water "White Ribbon"** | `04` (tide/solar window), `05` (quick-overlap), `07` (Nuth–Kääb tie) | `multimodal-white-ribbon.md`, `01` |
| **9. Abandonment, Weather-Standby & De-Scope Decision Governance** | `01` (pre-auth gates), `02` (Part B CPI/burn), `04`/`05` (holds) | `08` (AAR), `template-cost-ledger.md` §4 |

---

## 2. Checklist Formatting & Content Contract

Every module under `checklists/<modality>/` MUST follow this uniform Markdown specification so both humans and `check_checklists.py` can validate compliance:

### 2.1 Mandatory File Header Block
Each checklist file (`01`–`08`) opens with the five mandatory tokens validated by `check_checklists.py` (extending lines 1–3 with `Platform / Vessel / Tail #`, `Governing Spec`, and `Independent Verifier & Date (UTC)` per `template-project-header.md` §1):
```markdown
# <Modality Title> — <Phase Title>

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `<slug>` | **Platform / Vessel / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier & Date (UTC):** `__________________`
```
- **Realization & Frame Completeness:** `Horizontal CRS / Epoch` MUST record exact realization (e.g., `NAD83(2011)` or `ITRF2020`, never bare ensemble `WGS 84`). Files `00` and `03` MUST declare explicit **ENU ($+E, +N, +U\uparrow$) vs. NED ($+N, +E, +D\downarrow$)** body/mapping frames, while seamless TBDEM headers note the dual elevation/depth sign rule. Keeping the header compact on `01`–`08`, paired with the master RACI sign-off table in `00` and copy-ready field logs in `09`, preserves two-person `Lead / Verifier` traceability (`PRD.md` §7.2).

### 2.2 Tiered Checkbox Syntax
Every actionable checklist bullet MUST use one of three explicit priority tags:
- `- [ ] **[GATE]** <Actionable check with numeric threshold or pass criterion>.` — Hard stop; failure blocks the next operational phase (analogous to `fable` Appendix G **(must)** items).
- `- [ ] **[REC]** <Strongly recommended practice>.` — Required unless a documented project deviation explains why not.
- `- [ ] **[COND]** <Conditional check> (*Trigger:* ...).` — Mandatory whenever the stated operational trigger applies (e.g., foreign EEZ, Class B airspace, $>12{,}500\text{ ft}$ cabin altitude, turbidity $> K_d$ limit, GNSS interference zone).

Each item includes compact inline metadata where applicable:
`— *Threshold:* ... — *Evidence:* ... — *Ref:* [Chapter N](../../fable/chapters/chNN-....md)`

### 2.3 Quantitative Rigor & Domain Guardrails
1. **No ambiguous accuracies & proper $1\sigma$ vs. $95\%$ scaling:** Every accuracy requirement specifies statistic (`RMSE_V`, `RMSE_H`, `TVU_95%`, `LE95`, `CE90`, `NMAD`, `P95`), confidence level, land-cover/depth stratum, and edition year. Before variance propagation (RSS), convert $\text{TVU}_{95\%}/1.9600$ and circular $\text{THU}_{95\%}/2.4477$ to $1\sigma$, and use **1D single-axis** $\sigma_H = \text{RMSE}_r/\sqrt{2} = \text{THU}_{95\%}/2.4477$ in slope coupling $\tan^2\alpha\,\sigma_H^2$ (never 2D radial $\text{RMSE}_r$).
2. **Physics, datum triad, registration & sign consistency:**
   - Axis diagrams explicitly declare **ENU** ($+E, +N, +U\uparrow$) vs. **NED** ($+N, +E, +D\downarrow$) and lever-arm direction conventions.
   - Vertical datum reductions preserve $h = H + N = z_{\text{CD}} + \text{SEP} = \text{SEP} - d_{\text{CD}}$, keeping trajectories ellipsoidal until a single checksummed VDatum/SEP grid is applied.
   - Bathymetric lidar explicitly distinguishes phase refractive index $n_p$ (Snell bending) from group refractive index $n_g$ (pulse travel speed, avoiding $+1.6\%$ bias) and applies $(1 - 1/n_g)\delta z_s \approx 0.27\,\delta z_s$ to bottom elevation $z_b$ vs. $(1/n_g)\delta z_s \approx 0.73\,\delta z_s$ to instantaneous depth $d$.
   - Sonar/AUV checklists separate surface sound speed ($-d\tan^2\theta\,\delta c_0/c_0$ at flat arrays) from full water-column harmonic-mean SVP ($d(1 - \tan^2\theta)\delta c_p/c$) and scale AUV acoustic terms with altitude $h_{\text{alt}}$ rather than ocean depth $d$.
   - Drone/aircraft checklists treat "$122\text{ m}$ (`400 ft`) AGL" relative to true ground/canopy beneath the aircraft, never barometer QFE alone or coarse SRTM without canopy allowance.
   - InSAR & SAR RCS formulas explicitly state $h_a \equiv h_{\text{amb}} = \frac{\lambda R\sin\theta_i}{p\,B_\perp}$ ($p \in \{1,2\}$), distinguish incidence $\theta_i$ from grazing angle $\theta_g$, and measure **triangular** trihedral corner reflectors by inner orthogonal leg $a$ ($\sigma_{\max} = \frac{4\pi a^4}{3\lambda^2}$).
   - Gridding steps explicitly verify **`Pixel-is-Area`** vs. **`Pixel-is-Point`** registration metadata to prevent half-cell (`0.5 px`) offset errors.
3. **Zero fabricated figures or citations:** Cost benchmarks, regulatory numbers, and standards editions come strictly from verified `fable/`/`gemini4/` chapters or verified external authorities with explicit as-of dates/cost-basis caveats; uncertain specifics prompt local verification rather than guessing.

### 2.4 Offline Field-Binder Contract
To satisfy `PRD.md` §2.3 offline self-containment:
1. **Inline Actionable Gates:** Every `[GATE]` in `01`–`08` MUST carry its numeric threshold, equation, or statutory clock inline so crews execute offline without resolving external links.
2. **Printable Field Bundle:** Crews deploy `checklists/<modality>/` + `checklists/_shared/` + `checklists/tools/check_checklists.py`, printing `06-accidents-and-emergencies.md` and `template-accident-card.md` as a single-page laminated bridge/cockpit/dash emergency card (plus blank logs in `09`).
3. **Two-Part `02` Structure:** `02-permits-safety-insurance-cost.md` separates **Part A: Pre-Mob Admin (Permits, COIs, Budget)** from **Part B: Daily Pre-Sortie Safety & Burn-Rate Gates** for rapid daily field reference.

---

## 3. Cross-Reference Knowledge Integration Map

Every checklist module draws directly from verified chapters in `fable/` and `gemini4/`, augmented with external operational/safety/insurance/regulatory protocols. **Path convention:** All `gemini4/` file links resolve under `gemini4/book/ch-XX/sec-XX-YY.md` from repo root (i.e., `../../gemini4/book/ch-XX/sec-XX-YY.md` from `checklists/<modality>/`):

| Checklist Phase / Domain | Primary `fable/` Sources | Primary `gemini4/` Sources (under `gemini4/book/`) | External Operational Supplements |
|---|---|---|---|
| **Requirements, Standards & Surface Ontology** (`01`) | `ch01`–`ch04`, `ch32`, `ch34`, `ch44`, `ch70`, `appendix-d-standards-index.md`, `appendix-g-checklists.md` | `ch-01/`, `ch-20/`, `ch-24/sec-24-01.md` | Current annual NOAA HSSD (2024 restructured ed.); IHO S-102 Ed. 3.0.0 / S-158:102; USGS LBS 2024/2025 rev. A; ASPRS Ed. 2 v2 Addenda I–VI (incl. V UAS, VI Oblique) |
| **Geodesy, Datums, Time & Crustal Motion** (`01`, `03`, `07`) | `ch06`–`ch10`, `ch38`–`ch39`, `ch66`, `ch68.2` | `00-front-matter/notation-and-symbols.md`, `ch-02/`–`ch-04/` | NGS Modernized NSRS (Sept 2026 beta / ~2027 adoption caveat); VDatum/VORF; ITRF2020 / HTDP |
| **Pre-Existing Data & Public Products** (`01`, `07`) | `ch51`, `ch54`, `ch55`, `appendix-e-public-products-tables.md` | `ch-14/sec-14-01.md`–`sec-14-04.md`, `ch-19/`, `ch-24/` | GEBCO TID grids; SlideRule / `icepyx` ICESat-2; Sentinel-2 $K_d$/NDVI; MARAD/EASA interference advisories |
| **Permits, Licensure, Security & Ethics** (`02`) | `ch68`, `ch69`, `ch26.8` | `ch-27/sec-27-01.md`–`sec-27-03.md` | UNCLOS Part XIII (`>= 6` mo Art. 248 / `>= 7` mo plan); FAA Part 107 / `§ 44807` / `§ 119.1(e)(4)(iii)` / `§ 91.119` / AC 70-1B; FCC Part 90; EASA SORA; NMFS MMPA/JNCC 2017; EAR/ITAR; UN 3480/3090/3091 (`UN 38.3`, SDS); CARE/OCAP®; Fishery liaison |
| **Safety Checks & Emergency / Accidents** (`02`, `06`) | `ch56` (Case files), `appendix-g-checklists.md` §G.9 | `ch-07/sec-07-03.md`, `sec-07-04.md`, `sec-07-05.md`, `ch-27/sec-27-02.md` | UNOLS RVSS App. A/B; ANSI Z136.1/Z136.6 NOHD; 14 CFR 91.211 & 91.509; FAA § 107.9; NTSB 49 CFR 830 (`§ 830.2`/`830.5`); USCG 46 CFR 4.05/4.06 + NRC 33 CFR 153.203; OSHA 29 CFR 1904.39; COLREGS Rules 5–8 |
| **Insurance Coverage & Contracting** (`02`) | `ch68.4`–`ch68.5` | `ch-27/sec-27-01.md` | Marine H&M, P&I, Jones Act/MEL, USL&H, Charterer's Liab, IWL, C&V floaters; Aviation Hull+Liab+Overwater+Ocular; E&O; FVWC/Medevac; Waiver of Subrogation; UNOLS/NSF rules |
| **Cost Estimation & Reduction** (`02`, `08`) | `ch26.9`, `ch28` | `ch-27/sec-27-04.md` | UNOLS daily tiers ($15k–$60k+/day; commercial up to $80k/day); commercial stereo pricing & min AOI (2025–2026 list); 3DEP ALS/ALB `$/km²` ranges; site-month weather climatology; Carnet/MMO/hazmat/bunker lines |
| **Platform/Sensor Prep & Support Deployments** (`03`) | `ch12`–`ch16`, `ch18`–`ch25` | `ch-05/`–`ch-12/` (incl. `sec-12-06.md` RCS), `ch-07/sec-07-03.md`–`05.md` | MAC SAT/QAT & Westlake offset surveys; IOC Manual 14 tide gauges; NOAA OE Deepwater Mapping Manual; AUV ballasting/O-ring/vent SOPs |
| **Mission / Flight Planning & Pre-Survey TPU** (`04`) | `ch17`–`ch23`, `ch26.1`–`ch26.4`, `ch26.7`, `ch53` | `ch-07/`, `ch-08/`–`ch-12/`, `ch-13/sec-13-01.md`–`sec-13-02.md` | NOAA FPM patch test & ERS; Skáloud & Lichti boresight; James et al. oblique SfM; orbital $B/H$ & $h_{\text{amb}}$ calculators |
| **Underway QC, In-Field Processing & De-Mob** (`05`, `07`) | `ch26.5`–`ch26.6`, `ch27`, `ch29`–`ch36`, `ch47`–`ch50` | `ch-10/sec-10-06.md`, `ch-13/sec-13-03.md`, `ch-15/`, `ch-19/`, `ch-21/`–`ch-23/`, `ch-32/`–`ch-34/` | HydrOffice QC Tools / Kluster; POSPac SBET; PDAL/GDAL/MB-System scripts; UNOLS PCAR; 3-2-1 SHA-256 custody gates; off-hire & NOTAM/LNM closeout |
| **Cross-Validation, Error Budgets & Learning** (`07`, `08`, `09`) | `ch41`, `ch52`–`ch56`, `appendix-b`, `appendix-f`, `appendix-i` | `ch-14/sec-14-01.md`–`sec-14-04.md`, `ch-24/`, `ch-25/` | Nuth–Kääb (`xdem`), ICESat-2 ATL03/06/08, SWOT, ASPRS Ed. 2 $\chi^2$ CIs, AAR continuous checklist improvement |

---

## 4. Shared Scaffolding & Automated QA Tooling

### 4.1 `checklists/_shared/` Deliverables
- **`template-project-header.md`**: Standardized ISO 19111/19115/WKT2 table capturing realization, epoch, vertical datum + geoid/SEP model, ENU/NED & $+z\uparrow/+d\downarrow$ signs, governing spec/edition, RACI roles, plus compact header guidance (`Platform/Tail #` and `Independent Verifier`).
- **`template-error-budget.md`**: Side-by-side table pairing *a priori* budgeted 1σ/95 % components against *a posteriori* realized residuals (bias, σ, RMSE, $\chi^2$ 95 % CI with $\nu=n$ vs. $\nu=n-1$, NMAD, P95, spatial correlation length, ASPRS Ed. 2 quadrature reporting vs. true-sigma subtraction).
- **`template-cost-ledger.md`**: Multi-section Markdown ledger tracking Mobilization (incl. Permits/Carnet/Hazmat freight), Platform Hours/Days (fuel-bunker/FX clauses), Weather Standby climatology, Personnel/MMO/PSO, `5–10 %` Validation, Cloud Storage/Egress, EULAs/Insurance, Earned Value (`CPI`/`EV`), and §4 Abandon-Window Trigger Box.
- **`template-insurance-coi.md`**: Pre-mobilization COI audit sheet verifying H&M, P&I (wreck removal), Jones Act/MEL, USL&H, Charterer's, Subsea/Marine Floater (`C&V`), Aviation Hull+Liab+Overwater+Ocular endorsement, E&O, CGL, Auto, Cyber, FVWC/Medevac, **COI expiry vs. demob + $\ge 30$ d weather-extension buffer**, Waiver of Subrogation / Primary, **IWL** polar/restricted zones, and exclusion limits.
- **`template-accident-card.md`**: Field-printable emergency card with emergency radio/agency numbers (VHF Ch 16, `121.5 MHz`, NTSB ROC, NRC, FSDO/USCG), ICS escalation chain, chemistry-specific battery fire rules (water/AVD vs. Class D), beacon/pinger registry, black-box/GNSS-spoof log freeze, and statutory clocks (FAA § 107.9 10-day, NTSB 49 CFR 830 `§ 830.2`/`830.5`, USCG immediate + 5-day CG-2692 + 2h/32h SMI + immediate NRC, OSHA 8h/24h, UNOLS/NSF, LSO, insurer).
- **`template-aar-retrospective.md`**: Post-survey After-Action Review capturing schedule/cost/safety/accuracy deltas, near-misses, calibration drift trends, and mandatory PR/diff items to update the checklist.
- **`multimodal-white-ribbon.md`**: Synchronization checklist for combined coastal campaigns (e.g., high-tide ASV/UNOLS launch + low-tide bathylidar/drone + SDB/ICESat-2) ensuring seamless vertical datum ties, 100–500 m intertidal overlap, and **multi-asset safety deconfliction** (`532 nm` NOHD exclusion over chase boats/USVs; UAS vs. crewed airspace/altitude separation).

### 4.2 Automated Validation Harness (`checklists/tools/check_checklists.py`)
Modeled after [check_book.py](../../fable/tools/check_book.py), `check_checklists.py` validates up to **78 checklist Markdown files under `checklists/` plus `plans/01-checklists/{PRD,PLAN,TASKS}.md`** (supporting default full-corpus run, `--phase0-only`, `--dir checklists/<modality>`, `--quiet`, and `--self-test`), exiting `1` on any hard failure:
1. **Manifest & Word-Floor Check:** Verify target files exist (`os.path.isfile`) and meet minimum word floors (`>= 350` words for `checklists/README.md` and `checklists/_shared/*.md`; `>= 600` words for modality `00`–`09.md`).
2. **Header Block Check (`01`–`08`):** Confirm every modality file `01`–`08` opens with `# ` H1 and a `> ` blockquote containing `Project / Cruise / Sortie ID`, `Modality`, `Horizontal CRS / Epoch`, `Vertical Datum`, `Sign Convention`, `Elevation (+z`, and `Depth (+d`.
3. **Checklist Item & Escaped-Checkbox Hygiene (`01`–`08`):** Outside fenced code blocks, require every checkbox (`- [ ]` / `- [x]`) in `01`–`08` to carry `**[GATE]**`, `**[REC]**`, or `**[COND]**`, with `>= 5` `[GATE]` items and `>= 12` tagged items per file; reject backtick-escaped list checkboxes (`- \`[ ]\``) as hard failures in `01`–`08` (and warn in `README`/`_shared`/`00`/`09`).
4. **Link Integrity, `#anchor` & Cross-Reference Check:** After stripping fenced code blocks (`` ``` ``/`~~~`) and inline backtick spans (`` `...` ``), check all relative Markdown links via `os.path.isfile`, reject `/` absolute links and repo-escaping paths, verify GitHub-slug `#anchor` fragments (both intra-file and cross-file), allow links into the planned 70-file manifest only under `--phase0-only`, and require `>= 1` valid `fable/` and `>= 1` valid `gemini4/` link in every `_shared/*.md` and `00`–`09` file plus `>= 1` valid `../_shared/` link per modality.
5. **Unresolved Flag & Placeholder Check:** Fail on `TODO`, `TBD`, `lorem ipsum`, `to be written`, or unresolved `(verify)` markers outside fenced/inline code.
6. **Sign & Unit Discipline Warnings:** Flag unqualified `±`/`\pm`/`+/-` before numbers (including `\pm\,`, `±$`, and inline-backtick numbers) lacking a statistic/confidence/tolerance label, or bare `feet`/`ft`/`mi²`/`mi^2` without SI primary values (outside exempted statutory/USACE contexts).

---

## 5. Phased Execution Plan & TeachBook Considerations

1. **Phase 0 — Scaffolding & QA Harness:** Create `checklists/README.md`, all 7 files in `checklists/_shared/`, and `checklists/tools/check_checklists.py`. Verify `--phase0-only` passes cleanly.
2. **Phases 1–3 — Marine & Subsea Modalities:** Draft and 3-model review `underwater-auv/`, `autonomous-surface-vessel/`, and `unols-research-cruise/` (marine domain coherence across IHO S-44 Ed. 6.2.0 [retaining Ed. 6.1.0 Table 1 TVU/THU $a/b$ parameters], S-102/S-158, NOAA HSSD/FPM, UNOLS RVSS/MFP, MAC, COLREGS, UNCLOS, H&M/P&I/Jones Act).
3. **Phases 4–6 — Coastal & Terrestrial Airborne Modalities:** Draft and 3-model review `coastal-bathylidar/`, `land-drone-lidar-imagery/`, and `land-aircraft-lidar-imagery/` (FAA Part 107/44807/91/119/STC/AC 70-1B, ANSI Z136 NOHD, EASA SORA, USGS LBS 2024/2025, ASPRS Ed. 2 Addenda I–VI, aviation hull/overwater/ocular/E&O insurance).
4. **Phase 7 — Spaceborne Modality:** Draft and 3-model review `satellite-elevation/` (optical stereo/tri-stereo tasking, CORONA/KH-9 historical, InSAR/TanDEM-X/NISAR/Biomass, SWOT/ICESat-2/GEDI control, SDB under IHO B-13, EULAs, ground-crew safety).
5. **Phase 8 — Cross-Modality Audit, Phase 0 Back-Sync, Validator Run & Repo Integration:** Run `python3 checklists/tools/check_checklists.py` across all **78 checklist Markdown files + 3 planning docs** (target: 0 hard failures, 0 warnings, 0 broken links, 0 unresolved `(verify)` flags), execute a **Phase 0 back-sync pass** (`_shared/*` & `checklists/README.md`), audit the **9-domain coverage matrix** and **offline field-binder usability**, run cross-modality consistency checks (especially white-ribbon overlap and datum harmonization), and check whether root `README.md` or `book/_toc.yml` should remain untouched or receive an optional pointer (leaving existing TeachBook/Fable/Gemini4 sources intact unless explicitly requested; confirmed intentionally untouched in Phase 8 isolation check and documented in [checklists/README.md](../../checklists/README.md) §6).

### 5.1 Quality & Review Workflow
Borrowing and extending the multi-model workflow from [gemini4/TASKS.md](../../gemini4/TASKS.md), **every checklist deliverable is authored and then independently audited by three separate review passes (`Fable 5.2`, `Gemini 4 Carbon`, `Gemini 4 Neon`)** against the **10-Point Checklist Verification Rubric** detailed in [TASKS.md](TASKS.md) §1 (covering actionable thresholds, physics/math accuracy, regulatory/permit accuracy, safety/emergency completeness, insurance/cost realism, underway QC triggers, de-mob/custody gates, error-budget/cross-validation rigor, format contract & 9-domain coverage, link/register integrity, Q21 critique fairness, and zero hallucinated facts or unsupported cost numbers).

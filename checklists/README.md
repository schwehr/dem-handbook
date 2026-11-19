# DEM Survey Planning & Execution Checklists — Master Portal

> **Scope:** Operational, field-ready, signable checklists covering the full survey lifecycle across **seven DEM and bathymetric collection modalities**, synthesizing the physical, geodetic, and statistical foundations of [fable/](../fable/README.md) and [gemini4/](../gemini4/TOC.md) with regulatory, safety, insurance, hazmat, permitting, emergency, and cost-tracking realities. See [PRD.md](../plans/01-checklists/PRD.md), [PLAN.md](../plans/01-checklists/PLAN.md), and [TASKS.md](../plans/01-checklists/TASKS.md).

---

## 1. Platform-Selection Matrix & Economic Break-Evens

Choose the platform tier from the **decision risk, required accuracy/ontology, depth/canopy environment, and project area**—never solely from whatever hardware is in the garage ([Chapter 3](../fable/chapters/ch03-fitness-for-use.md), [Chapter 16](../fable/chapters/ch16-platforms.md) §16.11, [Chapter 28](../fable/chapters/ch28-reducing-cost.md) §28.2.4, [Gemini4 Sec. 27.4.2](../gemini4/book/ch-27/sec-27-04.md)).

| Modality Directory | Platform & Sensor Envelope | Depth / Canopy Regime | Typical Area Rate & Break-Even | Nominal Resolution / Density | Typical Vertical Uncertainty (Open / Clear) | Key Operational & Regulatory Gates |
|---|---|---|---|---|---|---|
| **[underwater-auv/](underwater-auv/00-README-and-signoff.md)** | Deep/shallow AUVs (MBES `200–400 kHz`, SAS, SSS, SBP, DVL, FOG INS, quartz pressure) | Shelf to abyssal (`5–6,000 m+`), `5–70 m` bottom-follow alt; under-ice | `10–50 km²/day`; wins when surface ship footprint (`50–150 m`) is too coarse | `0.5–2 m` footprint at any ocean depth | `dm` relative; absolute limited by USBL (`0.05–0.3 %` range) & DVL (`0.05–0.2 %` dist) | UNCLOS Part XIII MSR; EAR `8A001` / ITAR; `UN 3480/3481` (`PI965`/`PI966` `<=30%` SoC, IATA DGR 67th Ed. 2026), `UN 3090/3091`, `UN 38.3`, SDS; O-ring/ballast; LARS SWL |
| **[autonomous-surface-vessel/](autonomous-surface-vessel/00-README-and-signoff.md)** | Nearshore USVs (`1–4 m`), semi-submersibles (`DriX`), ocean USVs (`Saildrone Surveyor`) | `0.2–200 m` nearshore/turbid (up to `7,000 m` ocean USV); handles turbid rivers/estuaries | `5–50 km²/day` shallow; Tier 2 (`~$50–$250/km²`), ~75 % lower daily burn vs. crewed ship | `0.05–2 m` shallow footprint (`~0.5–2 %` depth) | `10–30 cm` (`95 % TVU`, S-44 Ed. 6.2.0 Special / Order 1a shallow) | COLREGS Rules 5–8 (AIS/radar/EO-IR); USCG LNM; RF e-stop; H&M/P&I/Floater; high-tide flats |
| **[unols-research-cruise/](unols-research-cruise/00-README-and-signoff.md)** | UNOLS Global / Ocean / Regional ships (hull/gondola/moonpool/pole MBES `12–400 kHz`, SBP, MVP/CTD) | `10–11,000 m`; shelf, canyon, deep ocean; heavy shipboard ops | `1,000–5,000 km²/day` deep; `$15k–$60k+/day` (commercial/deep up to `$80k/day`; Tier 3 `$1k–$5k/km²`) | `1–2 %` of depth (`50–150 m` at `4,000 m`) | `0.2–0.5 %` of depth deep; S-44 Ed. 6.2.0 Order 1a/Special shallow | 12–18 mo UNOLS MFP/SME lead; RVSS App. A/B crane SWL; MMPA/JNCC soft-start; R2R custody |
| **[coastal-bathylidar/](coastal-bathylidar/00-README-and-signoff.md)** | Crewed aircraft (or heavy UAS) `532 nm` green + `1064 nm` NIR ALB (`CZMIL`, `HawkEye`, `VQ-880-G`, `RAMMS`) | Dry beach + clear shallow water `0.5–50 m` (`~1.5–3 Secchi` / `(3–4.5)/Kd`) | `100–300 km²/day`; `~$385+/km²` (`~$1,000+/mi²` historical program range); fails if $Z_{sd} < 1\text{ m}$ or surf | `1–8 pts/m²` in water; `0.5–3 m` footprint | `10–20 cm` $1\sigma_z$ / `20–40 cm` `95 % TVU`, depth-dependent (S-44 Ed. 6.2.0 Order 1b/1a); NIR/land `5–10 cm` | FAA AC 70-1B Form 7140-1 + LCH; `14 CFR §§ 91.119/119.1(e)(4)(iii)/91.509`; ANSI Z136 NOHD & ocular COI; `30°–45°` sun; STC/337 |
| **[land-drone-lidar-imagery/](land-drone-lidar-imagery/00-README-and-signoff.md)** | Multirotor, fixed-wing, VTOL UAS (`<25 kg` & heavy-lift) with lidar & RTK/PPK global/rolling-shutter RGB | Open sites (`SfM`) or light-to-moderate canopy (`lidar`); DSM fails bare earth in forest | `0.2–2 km²/day` (SfM multirotor); `1–10 km²/day` (lidar); wins `< 10–20 km²` & repeat sites | `1–3 cm` GSD (SfM); `50–500 pts/m²` (lidar) | `2–5 cm` (SfM hard open); `3–8 cm` (lidar) `RMSE_V` | `<= 120 m` EASA Open / `<= 122 m (400 ft)` FAA Part 107 / `§ 107.29` / `§ 107.51(b)` / `§ 44807`; `UN 3480/3481` (`PI965`/`PI966` `<=30%` SoC, 2026); Aviation Hull+Liab+Ocular (CGL excl.) |
| **[land-aircraft-lidar-imagery/](land-aircraft-lidar-imagery/00-README-and-signoff.md)** | Fixed-wing & helicopter linear/SPL/GmL lidar (`1064/1550 nm`) + metric cameras (`USGS 3DEP`) | Regional blocks, forest DTMs (leaf-off), alpine/utility corridors | `200–1,000 km²/day`; breaks even `> ~20–100 km²` (`~$115–$385+/km²`, `~$300–$1,000+/mi²`; 3DEP pooling) | `2–30+ pts/m²` (QL0/QL1 `>=8`, QL2 `>=2 pls/m²`) | `5–10 cm` (`RMSE_V` NVA; LBS QL0 `<=5 cm`, QL1/2 `<=10 cm`) | STC/Form 337 port; `14 CFR §§ 91.119/119.1(e)(4)(iii)/91.211` O2 (`>3,810 / 4,267 / 4,572 m` [`12,500 / 14,000 / 15,000 ft`] PA); NOHD; Aviation Hull+Liab+Ocular+E&O |
| **[satellite-elevation/](satellite-elevation/00-README-and-signoff.md)** | Agile optical stereo/tri-stereo, CORONA/KH-9, InSAR (`TanDEM-X`, `NISAR`, `Sentinel-1`), `ICESat-2`/`GEDI`/`SWOT`, SDB | Global/regional/remote/denied airspace ($10^3\text{–}10^6\text{ km}^2$); SDB clear reefs (`0–25 m`) | Archive free (`$0–$5/km²` SDB); commercial stereo `~$64–$85/km²` (2025–2026 list range, $\ge 25\text{ km}^2$ min AOI) | `0.3–2 m` GSD (`1–4 m` DSM); InSAR `5–30 m`; GLO-30 `30 m` | Optical `1–4 m` (`<1 m` w/ GCP); InSAR `2–10 m`; GLO-30 `<=4 m LE90` | EULA derivative-DEM rights; CRSRA / India / China GCJ-02; ground-crew PPE; rejection SLA |

**Terrestrial Reference Tier (All Land/Coastal Campaigns):** GNSS RTK/PPK rovers (`100–300 pts/day`, `1–3 cm` vertical `1σ`), total stations/leveling (`mm–cm`), and `ICESat-2 ATL06/08` (`~0.1–0.3 m` flat open) validate the tiers above—never treat a platform tier as self-validating ([Chapter 52](../fable/chapters/ch52-ground-truth.md)).

---

## 2. Multi-Modal "White Ribbon" & Cross-Cutting Shared Templates

When a coastal campaign spans dry land, intertidal flats, and nearshore channels, single sensors leave a coverage gap or a vertical datum step. Use **[Shared Guide 0.8 — Multi-Modal White Ribbon Synchronization](_shared/multimodal-white-ribbon.md)** to pair high-tide ASV/launch MBES with low-tide bathylidar/UAS across a **100–500 m validation overlap belt** under one unified VDatum/SEP vertical frame.

| Shared Template / Guide | Operational Function | When to Copy / Fill |
|---|---|---|
| **[0.2 Project Geodetic & RACI Header](_shared/template-project-header.md)** | ISO 19111/19115 CRS/epoch, vertical datum/SEP, ENU/NED & `+z↑/+d↓` signs, RACI sign-off | Before writing line plans (`01`–`08`) |
| **[0.3 *A Priori* vs. *A Posteriori* Error Budget](_shared/template-error-budget.md)** | Quadrature RSS/TPU, ASPRS Ed. 2 / LBS / S-44 Ed. 6.2.0 (retaining Ed. 6.1.0 Table 1 $a/b$ values) rules, $\chi^2$ 95 % CIs, variogram & anomaly matrix | `04` (pre-mob) & `08` (post-demob) |
| **[0.4 Lifecycle Cost & Burn-Rate Ledger](_shared/template-cost-ledger.md)** | 7-category `ch28` budget, climatology standby math, cloud egress, `5–10 %` validation, abort gates | `02` (pre-mob) & `05` (daily underway) |
| **[0.5 Insurance & COI Audit Matrix](_shared/template-insurance-coi.md)** | H&M, P&I (wreck removal), Jones Act/MEL, USL&H, Floater (`C&V`), Aviation+Overwater+Ocular, IWL/FVWC, E&O | `02` (hard gate before mob) |
| **[0.6 Emergency & Accident Quick-Card](_shared/template-accident-card.md)** | Preserve-life ICS, beacon registry, black-box/GNSS-spoof log freeze, FAA §107.9 / NTSB 830 / USCG CG-2692 / OSHA | Print/laminate before first sortie (`02`, `06`) |
| **[0.7 After-Action Review & Checklist Diff](_shared/template-aar-retrospective.md)** | `ch56` case-file block, 14–30 day 4-axis reconciliation, calibration drift log, mandatory Git PR diff | `08` (within 14–30 days post-demob) |
| **[0.8 Multi-Modal White-Ribbon Guide](_shared/multimodal-white-ribbon.md)** | High-tide ASV + low-tide ALB/drone + SDB/ICESat-2 sync, `30°–45°` sun, VDatum/SEP, safety deconfliction | `04`, `05`, `07` on coastal projects |

---

## 3. Standardized 10-File Modality Layout & Tiered Gate Taxonomy

The corpus under `checklists/` comprises **78 checklist Markdown files** (`README.md`, `7` `_shared/` templates/guides, and `7 × 10` modality files) plus **`1` automated validator (`checklists/tools/check_checklists.py`)** = **79 deliverables under `checklists/`** (alongside `plans/01-checklists/{PRD,PLAN,TASKS}.md`). Every modality directory follows an identical `00`–`09` lifecycle layout so crews moving between platforms find every gate in the same place ([PLAN.md](../plans/01-checklists/PLAN.md) §1.1):
- `00-README-and-signoff.md` (Envelope, spec crosswalk, master sign-off) → `01-requirements-and-preplanning.md` → `02-permits-safety-insurance-cost.md` (**Part A:** Pre-Mob Admin/Permits/COIs/Budget; **Part B:** Daily Pre-Sortie Safety & Burn-Rate Gates) → `03-platform-sensor-prep-and-support.md` → `04-mission-or-flight-planning.md` → `05-underway-qc-and-field-processing.md` → `06-accidents-and-emergencies.md` → `07-demob-processing-and-validation.md` → `08-error-budget-and-retrospective.md` → `09-resources-and-templates.md`.

All actionable items in `01`–`08` enforce three strict checkbox tags:
- **`[GATE]`** — Hard stop; failure blocks the next phase (analogous to `(must)` in [Appendix G](../fable/appendices/appendix-g-checklists.md)).
- **`[REC]`** — Strongly recommended baseline practice; deviations require written rationale.
- **`[COND]`** — Mandatory whenever the stated operational trigger applies (foreign EEZ, $> 3{,}810\text{ m}$ [`12,500 ft`] under `14 CFR § 91.211`, $> 120\text{ m}$ EASA / $> 122\text{ m}$ [`400 ft`] FAA AGL, GNSS interference, turbid water, under-ice).

---

## 4. Offline Field-Binder Standard Operating Procedure (SOP)

Vessels at sea, field trucks in canyons, and remote charter bases lose internet connectivity. Prepare a verified **Offline Field Binder** **before departure**:

1. **Bundle the Self-Contained Directory (Offline Binder Rule):** Copy the active modality folder (`checklists/<modality>/`), all templates (`checklists/_shared/`), the verification tool (`checklists/tools/check_checklists.py`), and an offline checkout/PDF of [fable/](../fable/README.md) and [gemini4/](../gemini4/TOC.md) onto two independent ruggedized field drives/tablets. Every `[GATE]` in `01`–`08` inlines actionable thresholds and statutory clocks so crews can execute without live links.
2. **Stage Offline Geodetic & Environmental Caches:** Pre-cache local geoid grids (`GEOID18`, `GEOID2022`, `EGM2008`), `VDatum` / `PROJ-data` regional grids, `HTDP` parameters, predicted tide/harmonic tables, local CORS/NGS datasheets, and FAA Sectionals / USCG LNMs / ENC chart tiles for offline use.
3. **Print Hard-Copy Safety & Sign-Off Packets:** Print and laminate [_shared/template-accident-card.md](_shared/template-accident-card.md) (populated with platform beacon/pinger IDs and local SAR/underwriter numbers), print `00-README-and-signoff.md` and `06-accidents-and-emergencies.md` for cockpit/bridge binders, and stage blank weather/SVP/antenna-height photo logs (`09-resources-and-templates.md`).
4. **Enforce Raw Custody & Checksums Offline:** Run `sha256sum` / `bagit` manifests daily onto dual physical media (`3-2-1` rule; hold third copy at shore office/cloud as soon as link allows) **before** releasing any vessel, aircraft, or field crew.
5. **Post-Demob Git Sync & AAR:** Within `14–30` days of return, merge ticked field checklists, completed error/cost ledgers, and [AAR checklist diffs](_shared/template-aar-retrospective.md) back into the project repository.

---

## 5. Automated Checklist Validation (`checklists/tools/check_checklists.py`)

Run the automated linter modeled on [check_book.py](../fable/tools/check_book.py) before finalizing any campaign binder or repository edit:

```bash
# Validate the entire corpus (81 files: planning docs in plans/01-checklists/, README, _shared/, 7 modalities x 10 files)
python3 checklists/tools/check_checklists.py

# Run built-in linter regression unit tests (--self-test can combine with --phase0-only or default)
python3 checklists/tools/check_checklists.py --self-test

# Validate Phase 0 scaffolding only
python3 checklists/tools/check_checklists.py --phase0-only

# Validate a single modality directory during drafting or field binder export
python3 checklists/tools/check_checklists.py --dir checklists/underwater-auv --quiet
```

`check_checklists.py` fails (exit `1`) on missing/stub files, missing `01..08` geodetic header blocks, untagged checkboxes, backtick-escaped list checkboxes (`- \`[ ]\`` in `01..08`), `<5 [GATE]` or `<12` tagged items, broken relative links/paths (including `/` absolute or repo-escaping paths, invalid GitHub-style `#anchor` targets, and missing `fable/` / `gemini4/` / `../_shared/` coverage), and unresolved placeholders outside code blocks; and warns on escaped checkboxes in overview/template files, unqualified `±`/`\pm`/`+/-` values, or bare non-SI `feet`/`ft`/`mi²` units.

---

## 6. Upstream Repository Isolation, License & Operational Disclaimer

Per [`plans/01-checklists/PLAN.md`](../plans/01-checklists/PLAN.md) §5, the `checklists/` module (`README.md`, `_shared/*`, `tools/check_checklists.py`, and the 7 modality directories) together with `plans/01-checklists/` (`PRD.md`, `PLAN.md`, and `TASKS.md`) are **intentionally isolated as net-new files**: stock upstream files ([`../README.md`](../README.md), [`../book/_toc.yml`](../book/_toc.yml), `fable/`, `gemini4/`, `research/`, and `conductor/`) remain **unmodified** (`git diff --stat` empty). Because `book/_toc.yml` builds the handbook prose separately, checklists should be consulted via [`checklists/README.md`](README.md) or standalone offline field binders; if a downstream fork wishes to include these checklists in a Jupyter Book / TeachBook build later, add an optional `caption: Operational Checklists` section pointing to `checklists/README.md` in `book/_toc.yml` without modifying upstream handbook chapters.

- **License & Attribution:** All content under `checklists/` is released under the repository's **Creative Commons Attribution 4.0 International (`CC BY 4.0`)** license ([`LICENSE`](../LICENSE); preserve upstream attribution to the repository handbook sources `fable/` and `gemini4/`).
- **Operational & Legal Disclaimer:** Operational planning reference only — not legal, aviation, maritime, or insurance advice; verify current statutes, NOTAMs/LNMs, and binding COI policies before mobilization.

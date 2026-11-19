# Autonomous Surface Vessel (ASV / USV) — Survey Checklists Overview & Master Gate Sign-Off

> **Modality:** `autonomous-surface-vessel` | **Scope:** Uncrewed & autonomous surface hydrographic survey platforms (micro-catamarans, semi-submersible USVs, endurance ocean USVs)  
> **Companion Templates:** [`_shared/`](../_shared/template-project-header.md) | **Theory Backstops:** [`fable/`](../../fable/appendices/appendix-g-checklists.md) & [`gemini4/`](../../gemini4/book/ch-13/sec-13-01.md)

This folder is a **self-contained, offline-usable field binder** for planning, permitting, calibrating, operating, recovering, processing, and auditing autonomous surface vessel (ASV) and uncrewed surface vehicle (USV) bathymetric surveys. Every `[GATE]` in phases `01`–`08` carries its numeric pass/fail criterion, statutory clock, formula, and verification artifact inline so a Remote Operations Center (ROC) watchstander, launch vessel crew, or shore hydrographer can make defensible Go/No-Go decisions with zero network access.

---

## 1. Platform Envelope Crosswalk (Three ASV / USV Regimes)

An ASV behaves physically like a surface ship scaled down to extreme hydrodynamic, acoustic, and communications limits: smaller hulls experience dramatically higher pitch/roll rates in identical sea states, shorter GNSS antenna baselines limit heading precision, and uncrewed bridges shift Collision Regulations (COLREGS) watchkeeping from human eyes on deck to electro-optical/infrared (EO/IR), AIS, marine radar, and low-latency command links.

| Parameter | Regime A: Micro-Catamaran / Kayak (1–4 m) | Regime B: Semi-Submersible / Coastal Force-Multiplier (6–16 m) | Regime C: Endurance Ocean-Going USV (18–24 m) |
| :--- | :--- | :--- | :--- |
| **Representative Platforms** | Seafloor EchoBoat / HyDrone, Teledyne Z-Boat, Maritime Robotics Otter | Exail DriX (H-8: 7.71 m; H-9: 9.0 m; O-16: 15.75 m), Fugro Blue Essence, XOCEAN | Saildrone Surveyor (22 m LOA, wing sail + diesel-electric) |
| **Displacement & Draft** | 15–150 kg; 0.10–0.25 m hull draft; man-portable or davit | 1.4–22 t; 1.5–2.55 m submerged sonar gondola below wave-piercing strut | ~14 t; ~3.0 m keel/gondola draft; deep-ocean tow/ship-escort free |
| **Typical Sonar Suite** | 200–700 kHz SBES / compact MBES; optional side-scan | Kongsberg EM 2040 (200–400 kHz) + EM 712 (40–100 kHz), ADCP, sub-bottom | Kongsberg EM 304 MKII (26–34 kHz to ~7,000 m) + EM 2040 + Simrad EK80 |
| **Operating Depth Envelope** | 0.2–50 m (surf edge, marinas, rivers, tailings, glacier fronts) | 3–800 m (shelf, harbor approaches, pipeline/cable corridors) | 20–7,000 m (shelf edge, EEZ mapping, deep abyssal basins) |
| **Speed & Endurance** | 1.0–2.5 m/s (2–5 kn); 4–12 h battery (LiFePO₄ / Li-ion) | 3.1–7.2 m/s (6–14 kn); 3–10 days diesel / diesel-electric | 1.5–4.1 m/s (3–8 kn); 30–180+ days multi-month endurance |
| **Motion & Hydrodynamic Hazards** | High angular rates ($\dot{\phi}, \dot{\theta} > 30\text{–}50^\circ/\text{s}$) in 0.5–1.5 m chop; thruster aeration; over-the-side pole deflection | Minimal bubble sweepdown in gondola; strut-wake drag; tight LARS cradle/launch shock loads | Static wind-sail heel bias ($5^\circ\text{–}15^\circ$); sparse temporal SVP updates mitigated via winched SVT |
| **GNSS Baseline & Positioning** | Dual-antenna $B \ge 0.8\text{–}1.5\text{ m}$ ($\sigma_\psi \approx 0.07^\circ\text{–}0.13^\circ$); shore RTK or PPK | Rigid mast baseline $B \ge 1.5\text{–}2.5\text{ m}$ ($\sigma_\psi \approx 0.04^\circ\text{–}0.07^\circ$); PPP / RTK / inertial | Dual-antenna + high-grade FOG INS; global PPP-AR + Iridium/Starlink SATCOM |
| **Primary CONOPS Tier** | Tier 1 (Attended LOS) or Tier 2 (Monitored) | Tier 2 (Monitored from mothership/shore) or Tier 3 (OTH) | Tier 3 (Over-The-Horizon ROC supervisory autonomy) |

*Refs:* [Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md) · [Sec. 7.4 Marine Platforms & USVs](../../gemini4/book/ch-07/sec-07-04.md) · [Sec. 7.8 Vessel Squat & Dynamic Draft](../../gemini4/book/ch-07/sec-07-08.md)

---

## 2. Governing Standards & Accuracy Crosswalk

Before signing Phase 01, verify which specification controls depth uncertainty, feature detection, sounding density, coordinate frame (`ENU` vs. `NED`, $\det = +1$ permutation), and final grid sign convention. Note that **IHO S-44 Ed. 6.2.0 (Oct 2024)** preserves the core Table 1 TVU/THU $a/b$ values unchanged from the Ed. 6.1.0 baseline cited in `fable/` while adding §3.8 seabed characteristics. Depth-oriented survey standards use positive-down depth ($+d \downarrow$, meters; GDAL / IHO S-102 `verticalCS = 6498`), whereas Bathymetric Attributed Grid (BAG) elevation layers and topo-bathy merged DEMs use positive-up elevation ($+z \uparrow$, meters), linked via the vertical datum triad $h = H + N = z_{\text{CD}} + \text{SEP} = \text{SEP} - d_{\text{CD}}$.

| Governing Standard & Edition | Order / Class | Max Allowable TVU (95 %, $d$ in m) | Max Allowable THU (95 %) | Feature Detection / Spacing | Crosslines & Deliverable Sign |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **IHO S-44 Ed. 6.2.0 (Oct 2024; Table 1 $a/b$ unchanged from Ed. 6.1.0)** | Exclusive Order | $\sqrt{0.15^2 + (0.0075\,d)^2}$ | $1.0\text{ m}$ | Cubic feature $>0.5\text{ m}$; 200 % bathy coverage | Per authority (S-44 sets no fixed %); $+d \downarrow$ soundings / S-102 |
| **IHO S-44 Ed. 6.2.0 (Oct 2024)** | Special Order | $\sqrt{0.25^2 + (0.0075\,d)^2}$ | $2.0\text{ m}$ | Cubic feature $>1.0\text{ m}$; 100 % bathy coverage | Per authority (NOAA HSSD $\ge 4\%$); $+d \downarrow$ |
| **IHO S-44 Ed. 6.2.0 (Oct 2024)** | Order 1a | $\sqrt{0.50^2 + (0.013\,d)^2}$ | $5.0\text{ m} + 0.05\,d$ | Cubic $>2.0\text{ m}$ ($\le 40\text{ m}$ depth) or $>0.10\,d$ ($>40\text{ m}$) | Per authority (NOAA HSSD $\ge 4\%$ full / $\sim 8\%$ partial); $+d \downarrow$ |
| **IHO S-44 Ed. 6.2.0 (Oct 2024)** | Order 2 | $\sqrt{1.00^2 + (0.023\,d)^2}$ | $20\text{ m} + 0.10\,d$ | Not required (deep ocean / endurance USV; §3.8 seabed chars) | Per authority (typically $\ge 4\%$ check lines); $+d \downarrow$ |
| **NOAA HSSD (2024 edition, restructured; annual updates)** | Object Detection / Complete | IHO Special (shallow critical) or Order 1a | Same as S-44 Special / Order 1a | 200 % Object Detection or 100 % Complete (CUBE / VR BAG) | $\ge 4\%$ MBES crosslines ($\sim 8\%$ partial); BAG $+z \uparrow$, S-102 $+d \downarrow$ |
| **USACE EM 1110-2-1003 (2013)** | Navigation / Dredging Class 1 | Hard-bottom: $\pm 0.15\text{ m}$ (`0.5 ft`, 95 %); Soft-bottom: $\pm 0.30\text{ m}$ (`1.0 ft`, 95 %); General: $\pm 0.60\text{ m}$ (95 %) | $2.0\text{–}5.0\text{ m}$ (95 %; by survey class) | Check-bar / reference checks; $1\text{–}3\text{ m}$ grid; dredge-prism volume | Watch US Survey Foot vs. International Foot on legacy contracts; convert to SI primary |

*Refs:* [Ch. 70 Specifications Guided Tour](../../fable/chapters/ch70-specifications-guided-tour.md) · [Appendix D Standards Index](../../fable/appendices/appendix-d-standards-index.md) · [Sec. 24.1 IHO S-44 & NOAA HSSD](../../gemini4/book/ch-24/sec-24-01.md)

---

## 3. Supervision Tiers (NOAA OMAO / OCS & USCG CONOPS Alignment)

Define the CONOPS tier per operational zone before mobilization; a single sortie may step down from Tier 1 (harbor egress) to Tier 2 or Tier 3 (open transit/survey) only at documented waypoints after passing link, AIS, and EO/IR gates.

| CONOPS Tier | Operator Role & Line-of-Sight | Communications & Latency | Maximum Safe Density / Proximity | Mandatory Failsafe Behavior |
| :--- | :--- | :--- | :--- | :--- |
| **Tier 1: Attended / Direct Remote Control** | Dedicated helmsman visually observing vessel or via zero-latency FPV; chase boat within $200\text{–}500\text{ m}$ | Dedicated RF LOS link ($\le 100\text{ ms}$ latency) + physical RF e-stop fob ($\le 1\text{ s}$ trip) | Harbors, piers, marinas, busy channels, LARS launch/recovery, surf edge | Hardware RF e-stop cuts propulsion to neutral/all-stop immediately on trigger or link loss $>3\text{–}5\text{ s}$ |
| **Tier 2: Monitored / Supervised Autonomous** | Watchstander on mothership bridge or onshore ROC continuously watching radar + AIS + EO/IR + helm state (4 h max shift) | Dual-path RF mesh / LTE / coastal Starlink ($\le 1.5\text{ s}$ telemetry loop) | Coastal approaches, shipping fairways, anchorages, multi-vessel survey ops | Auto-COLREGS CPA maneuver with operator override; lost-link loiter/safe-circle for $60\text{–}180\text{ s}$, then station-keep or abort |
| **Tier 3: Over-The-Horizon (OTH) Supervisory** | ROC watch team monitoring multiple assets by exception (alarm-driven + 15–30 min status check-ins) | Redundant LEO/GEO SATCOM (Starlink + Iridium Certus/SBD) | Open shelf, offshore corridors, high seas / EEZ (>12 NM offshore) | Autonomous COLREGS Rule 8/13–17 avoidance; dead-man heartbeat ($15\text{–}30\text{ min}$) forces safe heave-to or return-to-muster if SATCOM drops |

---

## 4. Phase Directory & Offline Field-Binder Map

| File | Phase Scope | Primary Owner | Print / Field Role |
| :--- | :--- | :--- | :--- |
| [01-requirements-and-preplanning.md](./01-requirements-and-preplanning.md) | S-44/HSSD/EM spec, ERS vs. tide tree, climatology, CONOPS tier, spares, DMP | Lead Hydrographer | Pre-mob design gate |
| [02-permits-safety-insurance-cost.md](./02-permits-safety-insurance-cost.md) | Part A: COLREGS, USCG 5P-WI-002(1)/LNM, UNCLOS/ITAR, Hazmat, COIs, Cost · Part B: Daily Pre-Sortie & Burn-Rate | Project Manager / Legal / ROC Lead | Office gate + daily sortie clip |
| [03-platform-sensor-prep-and-support.md](./03-platform-sensor-prep-and-support.md) | Hull/gondola/sail, GNSS baseline, pole VIV/deflection, 1PPS/PTP, SVS/SVT, CORS, 5-BM tide station | Field Engineer / Hydrographer | Dockside mob & cal binder |
| [04-mission-or-flight-planning.md](./04-mission-or-flight-planning.md) | Swath spacing, 100–200 % overlap, 4–8 % crosslines, 4-step patch test, swell/angular-rate, crabbing, white-ribbon, *a priori* TPU | Mission Planner / Cat A/B | Pre-deployment mission pack |
| [05-underway-qc-and-field-processing.md](./05-underway-qc-and-field-processing.md) | ROC 4 h watch handoff, live SATCOM QC, SVS $>1.5\text{–}2.0\text{ m/s}$ cast trigger, 24 h DTON, SHA-256 custody, Kluster/MB-System | ROC Watch / Data Processor | Live ROC desk reference |
| [06-accidents-and-emergencies.md](./06-accidents-and-emergencies.md) | Collision, capsize, surf grounding, runaway intercept/tow, LiFePO₄/diesel fire, spoofing, CG-2692 / NRC / OSHA clocks | Watch Officer / Chase Coxswain | **Bridge/ROC emergency reference (print §0 card on 1 sheet)** |
| [07-demob-processing-and-validation.md](./07-demob-processing-and-validation.md) | Closure pass, raw custody BEFORE vessel release, washdown, UN 3480 SoC, Carnet, LNM closeout, ERS/SBET/CUBE/BAG/S-102 | Lead Processor / Field Lead | Demob gate + final QA |
| [08-error-budget-and-retrospective.md](./08-error-budget-and-retrospective.md) | Reconciled *a priori* vs. *a posteriori* TPU (angular rate, crabbing, heel, SVP, datum), AAR, checklist diffs | Lead Hydrographer / PM | Post-project 14–30 d closeout |
| [09-resources-and-templates.md](./09-resources-and-templates.md) | Authoritative critique of CONOPS/COLREGS/IHO/HSSD/Kluster + copy-ready ROC Handoff, COLREGS & SVT logs | Entire Survey Team | Reference & blank logs |

**Cross-Modality Shared Templates (print with this folder when building an offline binder):** [`template-project-header.md`](../_shared/template-project-header.md) · [`template-error-budget.md`](../_shared/template-error-budget.md) · [`template-cost-ledger.md`](../_shared/template-cost-ledger.md) · [`template-insurance-coi.md`](../_shared/template-insurance-coi.md) · [`template-accident-card.md`](../_shared/template-accident-card.md) · [`template-aar-retrospective.md`](../_shared/template-aar-retrospective.md) · [`multimodal-white-ribbon.md`](../_shared/multimodal-white-ribbon.md)

---

## 5. Master Phase-Gate Sign-Off Sheet

No survey transitions across a major operational boundary until both the **Phase Lead** and **Independent Verifier** sign off every `[GATE]` in that phase.

| Gate Boundary | Controlling Document | Key Non-Negotiable Release Criteria | Phase Lead (Name / Date UTC) | Independent Verifier (Name / Date UTC) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **G0 -> G1: Requirements Freeze** | [Phase 01](./01-requirements-and-preplanning.md) | Order, CRS/epoch, ERS/tide tree, CONOPS tier, *a priori* TPU margin, DMP locked | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G1 -> G2: Legal, Safety & Funds** | [Phase 02](./02-permits-safety-insurance-cost.md) | USCG 5P-WI-002(1)/COTP & LNM active, RF e-stop bench-tested, H&M/P&I/MEL COIs verified, weather contingency funded | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G2 -> G3: Vessel & Sensor Ready** | [Phase 03](./03-platform-sensor-prep-and-support.md) | Total-station lever arms + dual-antenna baseline signed, 1PPS/PTP locked, CORS/tide benchmarks leveled | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G3 -> G4: Mission & Patch Plan** | [Phase 04](./04-mission-or-flight-planning.md) | Shallow-edge spacing, 4–8 % crosslines, 4-step patch test site, crab/rate limits, white-ribbon window locked | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G4 -> G5: Field Production Ops** | [Phase 05](./05-underway-qc-and-field-processing.md) | Watch handoffs clean, SVS cast triggers honored, zero unassessed DTONs, daily SHA-256 backups verified | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G5 -> G6: Incident Free / Closed** | [Phase 06](./06-accidents-and-emergencies.md) | Zero open CG-2692 / NRC / OSHA / P&I notifications or full evidence freeze completed | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G6 -> G7: Custody & Vessel Release** | [Phase 07](./07-demob-processing-and-validation.md) | Reference closure pass clean, 100 % raw custody SHA-256 verified BEFORE demob release, LNMs closed | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |
| **G7 -> G8: Final Delivery & AAR** | [Phase 08](./08-error-budget-and-retrospective.md) | *A posteriori* TPU within spec, BAG/S-102/S-158 valid, AAR filed within 14–30 days | `__________________` | `__________________` | `[ ] GO  [ ] HOLD` |

# Autonomous Surface Vessel (ASV / USV) — Phase 05: Underway QC & Field Processing

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `autonomous-surface-vessel`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________`  
> **Vessel / Hull Class & Governing Spec:** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

This checklist governs live vessel operations in the Remote Operations Center (ROC) and chase boat, real-time acoustic/telemetry quality control, DTON triage, and raw custody synchronization. Every code snippet below is **strictly read-only or non-destructive triage** on a working copy—never overwrite raw files.

---

## 1. Watch Handoff, COLREGS Supervision & Override Discipline

- [ ] **[GATE]** **Execute formal ROC / Bridge 4-Hour Watch Handoff before relieving watch.** Outgoing and incoming watchstanders physically review active vessel track, COLREGS radar/AIS targets, live EO/IR video visibility, C2 link SNR/latency, battery/fuel endurance, weather trend, open SVP triggers, and unresolved holidays. — *Threshold:* Zero unbriefed helm transfers; incoming operator signs Watch-Handoff Sheet ([Template 09](./09-resources-and-templates.md)) only after verifying single-point helm command authority and confirming active LNM/AIS broadcast. — *Evidence:* Signed 4-hour Watch-Handoff Sheet logged every shift change. — *Ref:* [Phase 09 External Regulatory Register](./09-resources-and-templates.md#e-external-regulatory--operational-basis-register-non-handbook-sources) · [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md)

- [ ] **[GATE]** **Enforce live COLREGS Closest Point of Approach (CPA) and automated-override triggers.** Monitor radar + AIS + EO/IR continuously; never let autonomous collision-avoidance (COLREGS Rule 8/13–17) wait until close-quarters crossing, and verify early, unmistakable course alterations ($\ge 20^\circ\text{–}30^\circ$). — *Threshold:* Mandatory human review/override trigger whenever predicted **CPA $< 500\text{ m}$ ($0.27\text{ nmi}$)** in coastal/harbor Tier 1–2 waters or **$< 1,000\text{ m}$ ($0.54\text{ nmi}$)** in Tier 3 OTH ops, TCPA $< 5\text{ min}$, or whenever an un-AIS'd small craft/kayak/fishing buoy appears on EO/IR/radar; switch to manual slow-stop if EO/IR fog/glare cuts visual range **$< 1.85\text{ km}$ ($1.0\text{ nmi}$)**. — *Evidence:* Timestamped AIS/CPA alert log and override notes. — *Ref:* [Ch. 68 Legal Issues](../../fable/chapters/ch68-legal-issues.md) · [Ch. 62 Navigation & Charting](../../fable/chapters/ch62-navigation-and-charting.md)

---

## 2. Live Low-Bandwidth Telemetry, Swath QC & Sound-Speed Cast Triggers

- [ ] **[GATE]** **Inspect live SATCOM/mesh swath-coverage grid, outer-beam refraction smiles/frowns, and backscatter continuity.** Stream decimated real-time depth grids (tile deltas, nadir-vs-outer profile snippets, uncertainty grid) across Starlink/Iridium/mesh links without saturating C2 helm bandwidth. — *Threshold:* Coverage gaps (**holidays**) $> 3\times 3$ grid nodes (or violating HSSD $1\text{ m} / 2\text{ m}$ cube detection) are queued for immediate infill pass before vessel departs local block; outer-beam (`-60° to +60°`) refraction curl exceeding **$0.5\%$ of water depth** ($0.05\text{ m}$ at $10\text{ m}$; $1.0\text{ m}$ at $200\text{ m}$) or slope-coupled TVU exceeding $80\%$ of S-44 allowance halts line continuation for an immediate SVP cast. — *Evidence:* Hourly swath coverage waterfall + outer-beam cross-profile snapshot archived in QC log. — *Ref:* [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md) · [Sec. 10.4 Refraction & Ray Tracing](../../gemini4/book/ch-10/sec-10-04.md)

- [ ] **[GATE]** **Enforce the SVS vs. Cast-Surface $>1.5\text{–}2.0\text{ m/s}$ Sound-Speed Cast Trigger.** Continuously compare hull-mounted SVS reading ($c_{\text{SVS}}$) against top-of-cast sound speed from the active SVP profile ($c_{\text{cast},0}$) AND watch outer-beam afternoon thermocline curl:
  $$\frac{\delta z}{z} \approx \frac{\delta \bar{c}}{\bar{c}} - \tan^2\theta\left(\frac{\delta \bar{c}}{\bar{c}} - \frac{\delta c_0}{c_0}\right)$$
  Because $\tan^2(65^\circ) \approx 4.6$, even a $2\text{ m/s}$ surface mismatch ($\approx 0.13\%$) tilts outer beams sharply upward/downward! — *Threshold:* Trigger an autonomous **winched SVT/CTD cast** (or manual MVP/SVP drop from chase boat) **immediately** whenever $|c_{\text{SVS}} - c_{\text{cast},0}| > \mathbf{1.5\text{–}2.0\text{ m/s}}$, every **2–4 hours** in coastal/estuarine plumes, or whenever entering a visible turbidity/salinity front ($>0.5\text{ PSU}$ / $>0.5^\circ\text{C}$ jump); note Saildrone/DriX autonomous winched casts must confirm safe bottom clearance ($\ge 3\text{–}5\text{ m}$ margin above seabed) before payout. — *Evidence:* Timestamped `.asvp`/`.svp` cast files paired with continuous SVS delta strip chart. — *Ref:* [Ch. 20 Sonar](../../fable/chapters/ch20-sonar.md) · [Sec. 13.2 Environmental Scheduling](../../gemini4/book/ch-13/sec-13-02.md) · [Sec. 13.3 Real-Time QA](../../gemini4/book/ch-13/sec-13-03.md)

- [ ] **[GATE]** **Monitor angular rates ($\dot\phi, \dot\theta$), GNSS fix quality, and SBET health gaps in real time.** Track RTK/PPP fix mode (`Fixed` vs. `Float`), satellite count, PDOP, $C/N_0$, and micro-USV instantaneous roll/pitch rates while underway. — *Threshold:* Flag and schedule infill if: (1) RTK fix drops to `Float`/`Autonomous` for $> 30\text{ s}$ where ERS is primary; (2) `PDOP > 3.0` or sudden $C/N_0$ drop $> 5\text{ dB}$ indicating jamming/spoofing; or (3) sustained angular rate $\dot{\phi}, \dot{\theta} > \mathbf{30^\circ/\text{s}}$ persists over $> 30\text{ s}$ of mainscheme swath. — *Evidence:* Real-time navigation-status health summary archived per watch. — *Ref:* [Ch. 12 GNSS](../../fable/chapters/ch12-gnss.md) · [Sec. 7.4 Marine Platforms & USVs](../../gemini4/book/ch-07/sec-07-04.md)

- [ ] **[GATE]** **Verify daily ERS vs. Tide-Gauge vertical consistency and track dynamic draft / fuel-burn shift.** Compare ERS-reduced waterline heights against nearest verified tide gauge (if active) and confirm fuel-burn/salinity draft evolution matches pre-computed lookup curves (tracking uncertainty in [`template-error-budget.md`](../_shared/template-error-budget.md)). — *Threshold:* Instantaneous tide-vs-ERS discrepancy **$\le 0.08\text{ m}$ ($1\sigma$ coastal)** or investigate VDatum/datum epoch mismatch before proceeding; verify static/dynamic draft log on every refueling/battery swap. — *Evidence:* Daily vertical-datum residual log entry. — *Ref:* [Ch. 9 Vertical Datums](../../fable/chapters/ch09-vertical-datums.md) · [Sec. 7.8 Vessel Squat & Dynamic Draft](../../gemini4/book/ch-07/sec-07-08.md)

- [ ] **[GATE]** **Monitor propulsion amp-draw spikes, coolant temperature, sail heel, and autonomous winch payout limits.** Watch continuous motor current (detecting weed/line prop entanglement early), diesel coolant/exhaust temps on DriX/ocean USVs, steady wind-sail heel on Saildrone, and winch slip/clearance alarms during SVP casts (updating downtime/burn tracking in [`template-cost-ledger.md`](../_shared/template-cost-ledger.md)). — *Threshold:* Abort line if motor current rises **$>25\%$** at constant RPM (fouled prop risk) or steady sail heel exceeds **$15^\circ$** without dynamic compensation verification. — *Evidence:* Watch engineering telemetry screenshot & anomaly log. — *Ref:* [Sec. 7.8 Vessel Squat & Dynamic Draft](../../gemini4/book/ch-07/sec-07-08.md) · [Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md)

- [ ] **[GATE]** **Compute daily Crossline-vs-Mainscheme difference check before departing each operational sector.** Evaluate preliminary gridded crosslines against mainscheme tiles daily while vessel remains on-station so any systematic patch shift, refraction curl, or tide lag costs zero re-mobilization. — *Threshold:* Crossline-vs-mainscheme **$\ge 95\%$ nodes within S-44 $TVU_{95\%}$** and **$| \text{mean bias} | \le 0.05\text{ m}$ (shallow)** / $\le 0.3\%$ depth (deep) before releasing USV to distant block. — *Evidence:* Daily crossline diff check table in QC report. — *Ref:* [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md) · [Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md)

- [ ] **[COND]** **Execute real-time Protected-Species Soft-Start & Exclusion Pause** (*Trigger:* low-frequency $12\text{–}34\text{ kHz}$ deep sonar / SBP operations OR visual marine-mammal sighting inside mitigation zone via EO/IR or chase boat). — *Threshold:* Enforce **$\ge 30\text{ min}$ visual pre-watch** (**$60\text{ min}$** in water depths $>200\text{ m}$ per JNCC 2017) prior to ramping transmit power gradually over **$20\text{–}30\text{ min}$** at initial start-up where permit requires, and immediately secure low-frequency acoustics whenever a protected mammal/turtle enters the **100–500 m** mitigation radius until 30 min post-sighting clear. — *Evidence:* Timestamped acoustic soft-start & PSO mitigation log. — *Ref:* [Ch. 69 Security, Sovereignty & Ethics](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md)

- [ ] **[REC]** **Screen live Water-Column Imagery (WCI) for kelp canopies, gas seeps, and bait-fish schools.** Inspect nadir/outer water-column echoes whenever abrupt shoaling appears in smooth channels before dispatching chase boats or logging false DTONs. — *Threshold:* Distinguish suspended fish/kelp echoes from solid seabed returns using multi-pass repeatability and backscatter texture. — *Evidence:* Annotated WCI screenshot archived alongside shoal triage decision. — *Ref:* [Ch. 20 Sonar](../../fable/chapters/ch20-sonar.md)

---

## 3. Danger to Navigation (DTON) Escalation & Raw Custody Synchronization

- [ ] **[GATE]** **Assess potential Dangers to Navigation (DTONs) immediately and enforce the 24-Hour Escalation SLA.** Screen every un-charted shoal, submerged wreck, piling, pipeline span, or debris posing a surface/under-keel clearance hazard per NOAA HSSD least-depth criteria (with $>10\%$ shoaler than surrounding charted depth serving as an immediate project triage flag). — *Threshold:* Run cross-check verification pass over the shoal (2+ perpendicular/reciprocal passes + SVP check) immediately while USV is on scene; notify Hydrographic Project Lead **immediately upon discovery** and transmit formal DTON package (least-depth sounding, uncertainty, seabed imagery/backscatter, S-57 `.000` feature with `sftype=DTON`, and chartlet) to client / NOAA MCD / USCG District within **$\le 24\text{ hours}$** of initial detection. — *Evidence:* Submitted DTON `.000` + PDF chartlet + USCG/MCD delivery confirmation receipt. — *Ref:* [Ch. 62 Navigation & Charting](../../fable/chapters/ch62-navigation-and-charting.md) · [Sec. 24.1 Survey Guide Documents & HSSD](../../gemini4/book/ch-24/sec-24-01.md)

- [ ] **[GATE]** **Execute Daily Raw Custody Sync with SHA-256 Verification (`3-2-1` Backup Discipline).** Upon vessel recovery (or daily satellite/burst sync for multi-day DriX/Saildrone missions), ingest raw sonar datagrams (`.kmall`/`.all`/`.s7k`/`.xtf`), raw GNSS RINEX/`.t04`/`.pos`, raw IMU, raw SVS/SVP, AIS/EO-IR event logs, and mission helm logs to redundant storage with cryptographic manifests. — *Threshold:* **Zero unbacked raw bytes overnight:** maintain **3 copies** across **2 distinct media** (onboard NVMe + ruggedized shore NAS/RAID + isolated air-gapped SSD or encrypted cloud bucket) with **100 % verified SHA-256 checksum parity** matching onboard source files; **never** wipe or re-format onboard USV acquisition drives until verification completes. — *Evidence:* Daily `sha256sum -c` verification pass log stored alongside immutable raw folder. — *Ref:* [Ch. 50 Archiving & Provenance](../../fable/chapters/ch50-archiving-and-provenance.md)

---

## 4. Runnable Non-Destructive Field QC Snippets (`Kluster`, `MB-System`, Python)

All snippets below operate strictly on **read-only or working-copy paths** (`raw_copy/`, `qc_scratch/`).

### A. Quick `MB-System` Swath Inspection, Density & SVS/Tide Quick-Grid

```bash
# Non-destructive line inventory, ping/beam counts, and bounds check on working copy
# Kongsberg .kmall uses MB-System format ID 261 (MBF_EMKMALL); or use mbdatalist -F-1
ls qc_scratch/*.kmall | awk '{print $1, 261}' > qc_scratch/datalist.mb-1
mbdatalist -Z -Iqc_scratch/datalist.mb-1
mbinfo -Iqc_scratch/datalist.mb-1 -G -N -Oqc_scratch/mbinfo_summary.txt

# Quick ERS/processed working grid (+z up = -A2, -F5 shoal/min filter; use -F1 for Gaussian mean)
mbgrid -Iqc_scratch/datalist.mb-1 -A2 -E1.0/1.0/meters! -F5 -G3 -N \
  -Oqc_scratch/quick_utm_elev_1m
```

### B. Python `HSTB.kluster` Underway Processing & Variable-Resolution Surface (Working Copy)

```python
from HSTB.kluster.fqpr_convenience import perform_all_processing, generate_new_surface

# Process raw working copies into Kluster FQPR store under NAD83 / Ellipsoid (ERS)
fqpr = perform_all_processing(
    filname=["qc_scratch/0001_20260714_120000_ASV.kmall"],  # 'filname' is exact HSTB.kluster spelling
    navfiles=["qc_scratch/20260714_sbet.out"],
    errorfiles=["qc_scratch/20260714_smrmsg.out"],
    svfiles=["qc_scratch/20260714_1205Z.svp"],
    outfold="qc_scratch/kluster_fqpr",
    coord_system="NAD83",
    vert_ref="ellipse",
)
# Generate variable-resolution CUBE surface; inspect output in HydrOffice QC Tools
surf = generate_new_surface(
    fqpr_inst=fqpr,
    grid_type="variable_resolution_tile",
    output_path="qc_scratch/vr_surface_20260714",
)
```

### C. Python Live Trigger: SVS Delta & Outer-Beam Refraction Smile Monitor

```python
import numpy as np

def check_refraction_and_svs_trigger(c_svs: float, c_cast_surface: float,
                                     angles_deg: np.ndarray,
                                     depth_resid_m: np.ndarray,
                                     mean_depth_m: float) -> dict:
    """Flag SVS >1.5-2.0 m/s divergence or outer-beam curl >0.5% depth."""
    svs_delta = abs(c_svs - c_cast_surface)
    valid = np.isfinite(angles_deg) & np.isfinite(depth_resid_m)
    ang = angles_deg[valid]
    res = depth_resid_m[valid]
    outer = np.abs(ang) >= 50.0
    nadir = np.abs(ang) <= 10.0
    if not (np.any(outer) and np.any(nadir)):
        raise ValueError("Need finite nadir (<=10 deg) and outer (>=50 deg) beams.")
    curl_m = float(np.median(res[outer]) - np.median(res[nadir]))
    curl_pct = 100.0 * abs(curl_m) / max(mean_depth_m, 0.1)
    return {
        "svs_delta_mps": round(svs_delta, 3),
        "outer_curl_m": round(curl_m, 4),
        "outer_curl_pct_depth": round(curl_pct, 3),
        "cast_now": (svs_delta > 1.5) or (curl_pct > 0.5),
    }
```

- [ ] **[REC]** **Run `HydrOffice QC Tools` (Grid QA, Flier Finder, Holiday Finder) on daily working surfaces.** Check daily grid density ($\ge 5$ soundings/node), flag isolated fliers $>3\sigma$ prior to manual review, and export GeoJSON holiday polygons directly back to the USV mission queue for same-deployment infill. — *Threshold:* Zero uninspected fliers above S-44 TVU limit and zero unresolved holidays exceeding local line-spacing plan at block sign-off. — *Evidence:* Saved HydrOffice QC Tools PDF/JSON report for each production block. — *Ref:* [Sec. 13.6 Kluster & HydrOffice Processing](../../gemini4/book/ch-13/sec-13-06.md) · [Sec. 10.5 Hydrographic Software](../../gemini4/book/ch-10/sec-10-05.md)

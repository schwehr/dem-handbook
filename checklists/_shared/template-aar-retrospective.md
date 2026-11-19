# Shared Template 0.7 — Post-Survey After-Action Review (AAR) & Checklist Diff

> **Purpose:** Convert operational friction, calibration drift, cost variance, and near-misses into permanent improvements within **14–30 days after demobilization** while raw logs and crew memory are fresh. Structured after [Chapter 56](../../fable/chapters/ch56-case-files.md) case files, [Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md) provenance standards, [Chapter 28](../../fable/chapters/ch28-reducing-cost.md) economics, and [Gemini4 Sec. 14.1](../../gemini4/book/ch-14/sec-14-01.md) / [Sec. 14.5](../../gemini4/book/ch-14/sec-14-05.md) (for Axis D error forensics).

---

## 1. AAR Timeline & Provenance Gate

- **Completion Window (Project Default):** Convene AAR within **14 days** of demobilization; finalize signed AAR, archive manifest, and checklist Git PR within **30 days** (*funder/agency deadlines—e.g., UNOLS Post-Cruise Assessment Report [PCAR], NOAA Descriptive Report, or USGS LBS QA schedule—govern where shorter*).
- **Project / Cruise / Sortie ID:** `____________________` · **Modality:** `____________________`
- **AAR Chair (PI / PM):** `____________________` · **Attendees (Survey, Platform, Processing, QA/QC):** `____________________`

---

## 2. Structured Incident & Finding Case-File Block (`ch56` Format)

For every significant anomaly, near-miss, QC failure, or unexpected success, log one structured case entry using the handbook failure taxonomy (`datum/epoch`, `surface definition`, `metadata/units`, `measurement physics`, `missing data`, `decision process`). **Blameless culture & PII rule:** AARs exist to **assign root cause, never personal blame** ([Chapter 56](../../fable/chapters/ch56-case-files.md)); redact all personal names, medical notes, and crew PII before committing to shared Git repositories.

- **Finding Title & Date (UTC):** `________________________________________`
- **What Happened (Facts Only):** `__________________________________________________________________`
- **Root Cause (Handbook Taxonomy):** `____________________________________________________________`
- **Check That Caught It (or Would Have Caught It Earlier):** `______________________________________`
- **Archive & Provenance Disposition (`ch50`):**
  - Raw sensor logs, GNSS/IMU (`RINEX`/`SBET`), SVP/tide logs, and calibration certificates archived? `[ ] Yes` (Repo & DOI: `________________`)
  - `BagIt` (`RFC 8493`) `manifest-sha256.txt` verified in 2+ geographic locations ([Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md) geo-redundancy; project `3-2-1` rule)? `[ ] Yes` (Root Hash: `________________`)
  - Software container digest / lockfile + geoid/VDatum grid files archived with product? `[ ] Yes`

---

## 3. Four-Axis Planned-vs.-Actual Reconciliation

### 3.1 Axis A — Schedule & Environmental Window Reconciliation
| Metric | Planned ($P_{50}$ / $P_{80}$) | Actual Realized | Delta ($\text{Actual} - \text{Planned}$) | Root Cause & Climatology Database Update |
|---|---|---|---|---|
| Productive Acquisition Days / Hours | `________` | `________` | `________` | `________________________________` |
| Mobilization / Transit / Calibration Days | `________` | `________` | `________` | `________________________________` |
| Weather / Environmental Standby Days | `________` | `________` | `________` | Update site-month $f_{\text{workable}}$ record |
| Equipment Downtime / Re-Fly / Infill Days | `________` | `________` | `________` | `________________________________` |
| Permit / UNCLOS / Airspace Lead Time (Days) | `________` | `________` | `________` | Update lead-time floor in `02` |

### 3.2 Axis B — Lifecycle Cost & Burn-Rate Reconciliation (`template-cost-ledger.md`)
| Cost Category (`ch28` §28.1) | Planned (USD) | Actual (USD) | Delta (USD & %) | Notes / False-Economy Check |
|---|---|---|---|---|
| 1. Mobilization & Demobilization | `$________` | `$________` | `$________` | `________________________` |
| 2. Platform Operating Time | `$________` | `$________` | `$________` | Actual online %: `____ %` |
| 3. Weather & Standby Holding | `$________` | `$________` | `$________` | `________________________` |
| 4. Field & Processing Labor | `$________` | `$________` | `$________` | Editing hrs vs. CUBE/auto: `____` |
| 5. Independent Validation (`5–10 %` target; `>= 3 %` hard floor) | `$________` | `$________` | `$________` | Realized share: `____ %` |
| 6. Cloud Storage, Compute & Egress | `$________` | `$________` | `$________` | `________________________` |
| 7. Software, EULAs & Re-Survey Costs | `$________` | `$________` | `$________` | `________________________` |
| **TOTAL COST & REALIZED UNIT RATE** | **`$________`** | **`$________`** | **`$________`** | **Realized Cost / $\text{km}^2$ (or line-km):** `$____` |

### 3.3 Axis C — Safety, Human Factors & Spares Logistics
- **Accidents / Statutory Reports Filed (`template-accident-card.md`):** Count: `____` · Summary: `____________________`
- **Near-Misses / Fatigue / Watch-Handoff Issues:** `____________________________________________________`
- **Spares Consumed & Stockout Bottlenecks (item + replacement lead time):** `____________________________________`

### 3.4 Axis D — Error Budget & Longitudinal Calibration Drift (`template-error-budget.md`)
- **Summary Uncertainty Delta:** Budgeted $1\sigma_z$: `____ m` vs. Achieved $\text{RMSE}_{\text{test}}$ / ASPRS $\text{RMSE}_{\text{rep}}$ / $\text{NMAD}$: `____ m` (Per-stratum NMAD; long-range variogram range $a_2$ / correlation length $L_c$: `____ m`). Link completed [Error Budget Sheet](template-error-budget.md).

| Parameter / Sensor Pair | Pre-Project Cal Value | Mid-Project Check | Post-Project Closure Value | Total Drift ($\text{Post} - \text{Pre}$) | Mechanical / Thermal / Impact Explanation |
|---|---|---|---|---|---|
| Roll Boresight / Patch ($\delta\phi$) | `________` | `________` | `________` | `________` | `________________________________` |
| Pitch Boresight / Patch ($\delta\theta$) | `________` | `________` | `________` | `________` | `________________________________` |
| Yaw / Heading Alignment ($\delta\psi$) | `________` | `________` | `________` | `________` | `________________________________` |
| Time Latency ($\delta t_{\text{lat}}$) / Camera IO | `________` | `________` | `________` | `________` | `________________________________` |
| Lever Arm / Static Draft / Waterline | `________` | `________` | `________` | `________` | `________________________________` |
| SVS / Pressure-Depth Zero / RTK Base Monument Tie | `________` | `________` | `________` | `________` | `________________________________` |

### 3.5 Axis E — Regulatory, Permit, Cultural & EULA Obligations Closeout
| Obligation Category | Action Closed | Closure Date & Proof Ref |
|---|---|---|
| **Airspace / Maritime Notices & Permits** | NOTAMs, USCG LNMs, FAA `AC 70-1B` Form `7140-1` / LCH advisories canceled; MMPA monitoring report filed | `____________________` |
| **UNCLOS Part XIII & Sovereignty / Security** | UNCLOS Art. 249 preliminary cruise report / coastal-state data return sent; `CARE/OCAP®` data-governance terms fulfilled | `____________________` |
| **Customs & Commercial Data Licensing** | ATA Carnet temporary export stamped closed; commercial satellite/DEM **EULA derivative & redistribution limits** logged in metadata | `____________________` |

---

## 4. Mandatory Git PR / Checklist Diff Template

Every AAR **MUST** produce at least one concrete proposed modification to the team's operational checklists, threshold tables, or spares manifests (or an explicit justification why zero edits are needed). Paste and open as a Pull Request:

```diff
--- a/checklists/<modality>/<file>.md
+++ b/checklists/<modality>/<file>.md
@@ -<line>,<count> +<line>,<count> @@
# Evidence / Incident Ref: <Project ID> AAR §2–§3 (<YYYY-MM-DD>)
- [ ] **[GATE]** <Previous threshold, spare count, or timing rule>
+ [ ] **[GATE]** <Updated threshold, mandatory check, lead time, or abort trigger>
```

| PR / Issue ID | Target Checklist File & Item | Change Summary (Threshold / Lead Time / Spare / Trigger) | Owner | Target Merge Date |
|---|---|---|---|---|
| `PR #____` | `checklists/<mod>/0__-....md` | `________________________________________________` | `________` | `____-__-__` |
| `PR #____` | `checklists/_shared/....md` | `________________________________________________` | `________` | `____-__-__` |

**AAR Closure Sign-Off:** PI / PM: `____________________` · Survey Lead: `____________________` · Date (UTC): `____-__-__`

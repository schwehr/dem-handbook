# Shared Template 0.4 — Lifecycle Cost Estimate & Underway Burn-Rate Ledger

> **Purpose:** Replace optimistic day-rate guesses with a full 7-category lifecycle cost ledger, site-month weather climatology distributions, cloud storage/egress math, protected validation budgets, and explicit underway standby/abort triggers. Grounded in [Chapter 28](../../fable/chapters/ch28-reducing-cost.md), [Chapter 26](../../fable/chapters/ch26-survey-planning.md) §26.9, [Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md) §50.8, [Chapter 68](../../fable/chapters/ch68-legal-issues.md), and [Gemini4 Sec. 27.4](../../gemini4/book/ch-27/sec-27-04.md).

---

## 1. Seven-Category Pre-Survey Cost Decomposition

Never cut control, crosslines, calibration events, raw-data retention, lossless archiving, metadata/lineage, or EULA legal review—every one reappears later as failed acceptance, re-survey cost, or liability ([Chapter 28](../../fable/chapters/ch28-reducing-cost.md) §28.6 & Pitfalls).

| Cost Category | Key Cost Drivers & Reference Benchmarks (Author-Compiled Indicative 2025–2026 Ranges; Quote-Dependent) | Planned Qty & Unit Rate | Planned Cost (USD) | Contingency / Uncertainty Basis |
|---|---|---|---|---|
| **1. Mobilization & Demobilization** | Ferry flights, vessel transit days, port calls, permits, ATA Carnet/customs brokerage, `UN 3480/3481` (`PI965`/`PI966` $\le 30\%$ SoC, IATA DGR 67th Ed. Jan 2026), `UN 3090/3091` (`UN 38.3`, SDS), `49 CFR 171–180` (`>300 Wh`) hazmat freight surcharges, boresight/patch test, tide-gauge/CORS setup (>50 % of small airborne or remote marine jobs). | `____` units @ `$____` | `$________` | Permit delay & transit weather risk |
| **2. Platform Operating Time** | **UNOLS/Research Ships (indicative, quote-dependent):** `~$15k–$25k/day` (regional/coastal), `$25k–$40k/day` (ocean/intermed.), `$40k–$60k+/day` (global; commercial/deep-ocean vessels up to `~$30k–$80k/day` per [Gemini4 Sec. 7.4](../../gemini4/book/ch-07/sec-07-04.md)). **Tiered funnel:** Tier 1 SDB/ICESat-2 `$0–$5/km²`; Tier 2 USV/ALB `$50–$250/km²`; Tier 3 crewed ship `$1,000–$5,000/km²`. **Indicative ALS/ALB:** `~$115–$385+/km²` (`~$300–$1,000+/mi²` historical 3DEP-scale) vs. **ALB:** `~$385+/km²` (`~$1,000+/mi²`). **Satellite stereo (public reseller list, quote-dependent):** e.g., Pléiades Neo 30 cm `~$64–$65/km²` stereo / `~$82–$85/km²` tri-stereo ($\ge 25\text{ km}^2$ min AOI + cloud/priority uplifts). Include fuel-bunker & FX escalation clauses. | Productive: `____` h/d<br>Transit/Cal: `____` h/d | `$________` | Account for `50–70 %` airborne online fraction (lower for small boats in chop) |
| **3. Weather & Environmental Standby** | **Derived from site-month climatology distribution** (see §2 below), NOT a flat guess: `~10 %` arid spring lidar up to `40–50 %` winter coastal MBES/ALB. | $P_{50}$ / $P_{80}$ days:<br>`____ / ____ d` @ `$____/d` | `$________` | Budget at $P_{80}$ climatology; hold $P_{90}-P_{80}$ in reserve |
| **4. Personnel, MMO/PSO & Processing Labor** | Field watch/flight crew rotation (STCW/FAA duty limits), **Marine Mammal Observers (MMO/PSO)** where MMPA/JNCC applies, analyst ground-editing/classification/breaklines (CUBE/CHRT cuts manual hydro editing; still budget ~5 % manual QC review). | Field/MMO: `____` h<br>Proc: `____` h | `$________` | Terrain complexity & canopy multiplier |
| **5. Independent Validation Budget** | **Target `5–10 %` of acquisition cost (hard floor `>= 3 %`).** Crosslines (`4–10 %` line-km), $\ge 30$/stratum independent checkpoints, reference surfaces, third-party QA audit. | `____ %` of Acq (`$____`) | `$________` | **PROTECTED LINE ITEM — DO NOT CUT** |
| **6. Storage, Compute & Cloud Egress** | Raw lidar `1–3 GB/km²` (LAZ, excl. waveforms; `~10x` with waveforms); raw MBES + WCI `10–80+ GB/day`. Object storage `~$0.02/GB-month` standard/hot (`~$0.023` hot; `~$0.001–$0.004/GB-mo` deep archive, plus retrieval/min-duration fees); egress `~$0.05–$0.09/GB` (2024 major cloud list prices). GPU/HPC burst compute. | Raw+Int: `____ TB`<br>Compute: `____ h` | `$________` | Mitigate egress `>99 %` via COG/COPC/Zarr + STAC HTTP Range requests |
| **7. Insurance, Software, Data EULAs & Re-Survey Risk** | Marine/Aviation/Payload/E&O policy riders & C&V survey fees; commercial seats (`CARIS`, `Qimera`, `TerraSolid`, `POSPac`, `Metashape`) vs. OSGeo (`PDAL`, `GDAL`, `MB-System`, `Kluster`, `ASP`); EULA derivative/redistribution fees; post-demob re-mob exposure. | Seats/COI: `____`<br>EULA: `____` | `$________` | Confirm EULA permits derivative DEM distribution **before** tasking |
| **TOTAL PROJECT BUDGET** | **Planned Baseline (`P50` / Target)** vs. **Authorized Ceiling (`P80`)** | Validation Share: `___ %` | **`$________`** | Re-survey cost if error caught post-demob: `$________` |

---

## 2. Site-Month Weather Climatology & Cloud Egress Modeling

### 2.1 Climatology Standby Distribution (`ch26` §26.9, `ch28` §28.1)
Do not apply a generic "20 % weather contingency." Query historical site-month reanalysis/met-buoy/METAR records (cloud ceiling, wind $> 8\text{–}10\text{ m/s}$ UAS limit, sea state $H_s > 1.5\text{–}2.0\text{ m}$, river turbidity/Secchi, leaf-off/snow-free dates) and compute:

$$N_{\text{standby}}(p) = N_{\text{prod}} \cdot \left(\frac{1}{f_{\text{workable}}(p)} - 1\right), \qquad C_{\text{prod/day}} = C_{\text{daily}} + C_{\text{standby}} \cdot \mathbb{E}\!\left[\frac{N_{\text{standby}}}{N_{\text{prod}}}\right], \qquad C_{\text{eff/on-line hr}} = \frac{C_{\text{prod/day}}}{H_{\text{online/day}}}$$

*(Keep **total campaign cost** $= N_{\text{prod}}\cdot C_{\text{prod/day}}$ distinct from **unit on-line collection cost** $C_{\text{eff/on-line hr}}$, where $H_{\text{online/day}} = f_{\text{online}} \cdot H_{\text{paid/day}}$, so $f_{\text{online}}$ is never double-applied.)*

- **Site & Target Month(s):** `________________` · **Data Source (NDBC/METAR/ERA5/MODIS):** `________________`
- **Workability Fraction $f_{\text{workable}}$:** Median ($P_{50}$): `____` · Conservative ($P_{80}$): `____` · Severe ($P_{90}$): `____`
- **Planned Productive Days ($N_{\text{prod}}$):** `____ d` · **Budgeted Standby Days ($N_{\text{standby}}(P_{80})$):** `____ d`

### 2.2 Cloud Storage & Egress Sensitivity Check (`ch28` §28.3, `ch50` §50.8)
Evaluate 5-year storage plus user-egress exposure before selecting distribution format:
- **Hot vs. Deep Archive Storage:** $C_{\text{store}} = V_{\text{hot}} \cdot \$0.02/\text{GB-mo} \cdot M_{\text{months}} + V_{\text{cold}} \cdot (\$0.001\text{–}\$0.004/\text{GB-mo}) \cdot M_{\text{months}}$. Keep raw waveforms/datagrams/RINEX in deep archive (`~$0.001–$0.004/GB-mo`, accounting for retrieval & minimum-duration fees) and deliverables in cloud-native `COG`/`COPC`/`Zarr` (`~$0.02/GB-mo`).
- **Egress Exposure (Full Download vs. Cloud-Native Range Requests):**
  $$C_{\text{full}} = N_{\text{users}} \cdot V_{\text{archive,GB}} \cdot r_{\text{egress}}, \qquad C_{\text{COG/COPC}} = N_{\text{users}} \cdot V_{\text{archive,GB}} \cdot \left(\frac{A_{\text{AOI}}}{A_{\text{total}}}\right) \cdot 1.5 \cdot r_{\text{egress}}$$
  where $r_{\text{egress}} \approx \$0.05\text{–}\$0.09/\text{GB}$ and $1.5\times$ accounts for tile/index overfetch. Planned 5-yr Storage: `$______` · Planned Egress: `$______` · Requester-Pays Bucket Enabled: `[ ] Yes [ ] No`.

---

## 3. Underway Daily Burn-Rate & Earned Value Tracker

Update daily during mobilization, acquisition, and demobilization. **Earned Value ($\text{EV}$) counts only QC-accepted productive units (free of un-infilled holidays and exceeding daily TPU/overlap triggers).**

| Date (UTC) | Productive Hours | Transit / Cal Hours | Weather Standby Hours | Equip. Downtime Hours | Productive Units ($\text{km}^2$ or line-km) | Daily Burn (USD) | Cumulative Spend (`AC`, USD) | Cumulative Earned Value (`EV`, USD) | Remaining Standby Budget (Days / USD) | Status / Action |
|---|---|---|---|---|---|---|---|---|---|---|
| `____-__-__` | `____` | `____` | `____` | `____` | `____` | `$____` | `$____` | `$____` | `___ d / $____` | `[ ] Nominal` |
| `____-__-__` | `____` | `____` | `____` | `____` | `____` | `$____` | `$____` | `$____` | `___ d / $____` | `[ ] Standby` |
| `____-__-__` | `____` | `____` | `____` | `____` | `____` | `$____` | `$____` | `$____` | `___ d / $____` | `[ ] Re-fly/Infill` |

**Daily Efficiency Metrics:** Online Utilization $= \frac{\text{Productive Hours}}{\text{Total Paid Hours}} = \text{____ \%}$ · Cost Performance Index $\text{CPI} = \text{EV}/\text{AC} = \text{____}$ · Cost/Unit $= \text{AC}/\text{Cumulative Units} = \$ \text{____}$.

---

## 4. Explicit Standby, De-Scope & Abort Decision Gates

Pre-authorize objective financial and environmental thresholds **before** mobilization so decisions are not improvised under daily burn-rate pressure:

| Trigger Condition | Threshold | Decision Authority | Required Action (Stand-Down / De-Scope / Abort) |
|---|---|---|---|
| **Weather Standby Depletion** | Remaining standby reserve $< 20\%$ OR consecutive weather holds $> \text{___ days}$ | PM / PI + Client | Switch to priority sub-blocks (Priority 1 channels/floodplains first); authorize de-scope or window deferral. |
| **Environmental Window Closure** | Leaf-on NDVI threshold exceeded, snow onset, Secchi $< \text{___ m}$, or $K_p \ge 5$ persistence | Survey Lead + QA/QC | **HARD HOLD** on affected blocks; prohibit leaf-on/turbid data blending into spec deliverables; document partial delivery. |
| **Burn-Rate / CPI Excursion** | $\text{CPI} = \text{EV}/\text{AC} < 0.80$ for $\ge 3$ consecutive operational days | PM / Contracting Officer | Audit platform downtime, line ordering, or swath clipping; renegotiate infill or trigger partial-delivery gate. |
| **Unresolved Systematic QC Failure** | Crosslines/overlaps fail spec after recalibration OR sensor hardware fault unresolvable with spares | Survey Lead + Platform Lead | **ABORT PRODUCTION** immediately; do not burn charter days collecting invalid data; recover/repair or demobilize. |
| **Pre-Demob Custody & Closure Gate** | 100 % raw checksum verification + closure lines incomplete | PM + Data Processor | **DO NOT RELEASE** chartered vessel/aircraft/crew until raw custody and post-survey calibration closure pass. |

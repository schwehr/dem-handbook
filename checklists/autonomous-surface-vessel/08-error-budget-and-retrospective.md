# Autonomous Surface Vessel (ASV / USV) — Phase 08: Reconciled Error Budget & Retrospective

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `autonomous-surface-vessel`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________`  
> **Vessel / Hull Class & Governing Spec:** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

Complete this phase **14–30 days after demobilization / initial processing closeout** (updating acceptance notes once final client review clears) while operational memory, raw logs, and cost invoices remain fresh. The goal is to convert empirical residuals into tighter *a priori* uncertainty budgets, realistic weather/cost models, and version-controlled checklist improvements.

---

## 1. Reconciled *A Priori* vs. *A Posteriori* Uncertainty Audit

- [ ] **[GATE]** **Populate the Reconciled ASV Error-Budget Table against [`template-error-budget.md`](../_shared/template-error-budget.md).** Distinguish clearly between pre-survey modeled uncertainty (**"compiled to meet"** IHO S-44 / HSSD via *a priori* TPU) and empirical post-survey residuals (**"tested to meet"** via crosslines, reference closure, and check points) across every error driver below:

| Error Mechanism (ASV-Specific Physics) | Phase 04 *A Priori* ($1\sigma$, or $95\%$ noted) | Phase 07 Measured ($1\sigma$ / NMAD, or $95\%$ noted) | Ratio ($\text{Meas}/\text{Pred}$) | Dominant Root Driver & Corrective Action |
| :--- | :--- | :--- | :--- | :--- |
| **Angular-Rate Latency Coupling** ($\dot{\phi}, \dot{\theta} > 30^\circ/\text{s}$) | `______ m` | `______ m` | `____` | Timing residual $\delta\phi = \dot{\phi}\,\delta t$ in chop; verify 1PPS/PTP |
| **GNSS Baseline Heading & Crabbing** ($B_{\text{GNSS}}, \beta$) | `______ m` | `______ m` | `____` | Cross-current crabbing + dual-antenna $0.1^\circ\cdot\text{m}/B_{\text{GNSS}}$ outer-beam yaw |
| **Static Sail Heel & Tack Bias** (Ocean USV) | `______ m` | `______ m` | `____` | Asymmetric sail loading port vs. starboard tack; check roll offset |
| **Rigid Pole Deflection / VIV** ($\delta\theta \propto v^2$) | `______ m` | `______ m` | `____` | Strut bending or brace slip vs. speed; weld/keyway or fair pole |
| **Surface SVS vs. Thermocline SVP Curl** ($\tan^2\theta$) | `______ m` | `______ m` | `____` | Missed $>1.5\text{ m/s}$ trigger or afternoon stratification frown |
| **ERS VDatum/VORF SEP + Dynamic Draft/Squat** | `______ m` | `______ m` | `____` | Coast-vs-estuary SEP error, fuel burn $\Delta z$, or salinity $\Delta\rho$ |
| **Reference Surface Closure Shift** (Pre vs. Post) | `______ m` | `______ m` | `____` | Pole shift, unrecorded waterline change, or patch drift |
| **Combined $1\sigma$ & $95\%$ $TVU_{95\%}=1.96\,\sigma_z$ / $THU_{95\%}=2.4477\,\sigma_{1\text{D},H}$** | `1s: ___ m / 95%: ___ m` | `1s: ___ m / 95%: ___ m` | `____` | Compare $TVU_{95\%}$ & $THU_{95\%}$ against S-44 / HSSD / USACE ceiling |

- *Threshold:* Explain any component whose **Measured / Predicted ratio exceeds $1.25\times$** or whose empirical standard deviation $\hat{\sigma}$ over $\nu$ effective degrees of freedom falls outside its two-sided $\chi^2$ 95 % confidence interval $\left[\hat{\sigma}\sqrt{\nu/\chi^2_{\nu,\,0.975}},\;\hat{\sigma}\sqrt{\nu/\chi^2_{\nu,\,0.025}}\right]$; zero unexplained mean vertical bias $>0.03\text{ m}$ ($1\sigma$ coastal) or $>0.08\text{ m}$ (unmodeled estuary). — *Evidence:* Signed Reconciled Error Budget table attached to final Survey Report. — *Ref:* [Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md) · [Sec. 14.2 TPU & Metrics](../../gemini4/book/ch-14/sec-14-02.md)

- [ ] **[GATE]** **Diagnose Spatial Correlation Length ($L$) and Effective Sample Size ($N_{\text{eff}}$) in Crosslines.** Model crossline error residuals with an empirical semivariogram rather than assuming uncorrelated random noise ($\sigma/\sqrt{N}$). — *Threshold:* Compute $N_{\text{eff}} \approx A / (\pi L^2)$ over survey block area $A$; never claim millimeter-level mean confidence using $N = 10^6$ pings when refraction, SEP, or tide-zoning errors correlate over $L \approx 200\text{–}2,000\text{ m}$ ($N_{\text{eff}}$ can be $100\text{–}10,000\times$ smaller than raw ping count). — *Evidence:* Semivariogram range plot and corrected uncertainty confidence interval of the mean bias. — *Ref:* [Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md) · [Sec. 33.1 Modeling Spatial Autocorrelation](../../gemini4/book/ch-33/sec-33-01.md)

- [ ] **[GATE]** **Recompute Under-Keel Clearance (UKC) Exceedance Risk on Navigation-Critical Deliverables.** For harbor channels, shoals, or DTONs, evaluate the probability that true shoal depth is shallower than published depth plus safety margin $m$ via $\Phi(-m/\sigma_m)$ using empirical $\sigma_m$. — *Threshold:* Document exceedance probability explicitly whenever published chart/channel clearance margin $m < 2.0\,\sigma_m$ ($>2.3\%$ risk) or verify shoal-biased selection / designated soundings protect critical corridors. — *Evidence:* UKC sensitivity note included in Descriptive Report / client brief. — *Ref:* [Ch. 62 Navigation & Charting](../../fable/chapters/ch62-navigation-and-charting.md)

- [ ] **[GATE]** **Classify All Survey Anomalies Against the Root-Cause Attribution Matrix.** Tag every operational re-run, infill holiday, or residual artifact using the deterministic diagnostic mapping below:

| Observed Surface Symptom | Root Physical Cause | Missed Checklist Gate | Preventive Update for Next Cruise |
| :--- | :--- | :--- | :--- |
| Symmetric outer-beam **smile / frown** growing late afternoon | Surface sound-speed lag or missed thermocline SVP | Phase 05 $>1.5\text{ m/s}$ cast trigger | Tighten SVP cast cadence / autonomous winched SVT depth trigger |
| Alternating **sawtooth / roll ripple** between reciprocal lines | Roll boresight error or 1PPS timing jitter under $\dot{\phi} > 30^\circ/\text{s}$ | Phase 03 1PPS lock / Phase 04 flat-bottom roll pass | Lock PTP/1PPS + add steep-chop rate pause ceiling |
| **Step offset between adjacent blocks / surveys** ($0.3\text{–}2.0\text{ m}$) | `PROJ +proj=vgridshift` sign flip, geoid version mismatch, or `AREA_OR_POINT` shift | Phase 01 CRS freeze / Phase 07 `GNSS@TG` sign check | Enforce blind monument + tide-gauge residual assertion in pipeline |
| **One-sided wing droop** across entire sail USV track | Steady wind-sail heel bias unmodeled by flat patch test | Phase 04 opposite-tack heel check | Require port-vs-starboard tack calibration run before mainscheme |
| **Intertidal step** along USV / lidar white-ribbon boundary | Storm erosion between passes or mismatched vertical epoch/datum | Phase 01 high/low tide $\le 3\text{–}7\text{ d}$ window | Tighten tidal-sync gap and require Nuth–Kääb 3D co-registration check |

- *Threshold:* Every documented field anomaly maps to a named root cause and specific phase-gate improvement. — *Evidence:* Completed Anomaly Root-Cause Table in After-Action Report. — *Ref:* [Ch. 56 Case Files](../../fable/chapters/ch56-case-files.md) · [Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md)

---

## 2. Operational, Cost, Autonomy & Safety Retrospective (14–30 Day PCAR / AAR)

- [ ] **[GATE]** **Reconcile Actual Cost Ledger, Weather Standby Days & True `$/km²` Efficiency.** Close out [`template-cost-ledger.md`](../_shared/template-cost-ledger.md) using verified contractor invoices, chase-boat charter hours, SATCOM airtime, cloud storage/egress bills, validation labor, and weather standby days. — *Threshold:* Compare actual **weather-standby percentage**, **re-survey / infill line-km percentage**, and **validation labor %** against Phase 02 estimates; flag any category exceeding budget by **$>15\%$** with explanation for future bidding baselines. — *Evidence:* Closed final cost ledger signed by PM. — *Ref:* [Ch. 28 Reducing Cost](../../fable/chapters/ch28-reducing-cost.md) · [Sec. 27.4 Reducing Cost](../../gemini4/book/ch-27/sec-27-04.md)

- [ ] **[GATE]** **Audit ROC Watch-Fatigue, Autonomy Overrides, Link Uptime & COLREGS CPA Events.** Tabulate total autonomous hours vs. manual/override hours, link dropout durations, hardware/software e-stop activations, number of CPA $<500\text{ m}$ / $<1,000\text{ m}$ alerts, and any shift $>4\text{ h}$ fatigue deviations. — *Threshold:* **100 % of near-misses, unexpected e-stops, or link dropouts $>180\text{ s}$** investigated with software firmware version, RF noise floor, or COLREGS planner patch actions recorded. — *Evidence:* Autonomy & COLREGS Safety Metrics Summary table. — *Ref:* [Phase 09 External Regulatory Register](./09-resources-and-templates.md#e-external-regulatory--operational-basis-register-non-handbook-sources) · [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md)

- [ ] **[GATE]** **Review Critical-Spares Consumption, Hull/Sensor MTBF & LARS Wear.** Log every part replaced (thruster seals, propellers, wet-mate whips, O-rings, SVS sensors, winch slip-rings, battery cells) and mean time between failures. — *Threshold:* Update minimum spare-kit manifest for any component that exhausted stock or triggered $>4\text{ hours}$ downtime on site. — *Evidence:* Updated Master Spares BOM stored with vessel maintenance record. — *Ref:* [Ch. 16 Platforms](../../fable/chapters/ch16-platforms.md)

- [ ] **[REC]** **Audit Processing Reproducibility & Archive Accession Completeness.** Test pulling raw files + container digest + `VDatum`/`GGXF` transformation grid from long-term archive onto a clean workstation and regenerating one tile verbatim. — *Threshold:* Independent rebuild matches archived product to **$\le 10^{-4}\text{ m}$ ($0.1\text{ mm}$ floating-point determinism)** with intact ISO 19115 / STAC / BagIt checksums. — *Evidence:* Clean-room reproducibility test pass log. — *Ref:* [Ch. 29 Processing Pipelines](../../fable/chapters/ch29-processing-pipelines.md) · [Ch. 50 Archiving & Provenance](../../fable/chapters/ch50-archiving-and-provenance.md)

- [ ] **[GATE]** **Conduct 14–30 Day After-Action Review (AAR) and Commit Checklist Improvements to Git.** Convene Lead Hydrographer, Independent Verifier, ROC Lead, Chase-Boat Coxswain, and PM using [`template-aar-retrospective.md`](../_shared/template-aar-retrospective.md) to convert findings into **exact version-controlled checklist edits** (never just unactioned "lessons learned" bullets). — *Threshold:* Open and review concrete pull request / diff against `checklists/autonomous-surface-vessel/00..09.md` (and `../_shared/` templates if cross-modal) within **$\le 30\text{ days}$** of demob. — *Evidence:* Signed AAR PDF + merged commit/PR hash referencing checklist threshold or procedure improvements. — *Ref:* [Appendix G Checklists](../../fable/appendices/appendix-g-checklists.md) · [Ch. 26 Survey Planning](../../fable/chapters/ch26-survey-planning.md)

---

## 3. Additional Post-Survey Verification Checks

- [ ] **[REC]** **Evaluate Realized Sound-Speed Savings & Winched-SVT Duty Cycle.** Compare total cast hours / mechanical winch wear against outer-beam curl stability to refine future cast intervals (e.g., relaxing 2 h coastal cadence to 3 h offshore or tightening to 60 min across river fronts). — *Threshold:* Target **$<5\%$ of total survey lines** needing post-hoc SVP re-cast or outer-beam trimming. — *Evidence:* Cast-interval vs. refraction residual regression plot. — *Ref:* [Sec. 13.2 Environmental & Temporal Scheduling](../../gemini4/book/ch-13/sec-13-02.md) · [Sec. 10.4 Refraction & Ray Tracing](../../gemini4/book/ch-10/sec-10-04.md)

- [ ] **[COND]** **Verify Client / Agency Acceptance & Unresolved CARIS / NOAA Review Comments** (*Trigger:* third-party government/client hydrographic review branch audit). — *Threshold:* Zero unaddressed critical review comments or unresolved designated soundings at contract closeout; archive formal client acceptance sign-off letter alongside [`00-README-and-signoff.md`](./00-README-and-signoff.md). — *Evidence:* Signed Client Acceptance Letter and closed comment-resolution matrix. — *Ref:* [Ch. 70 Specifications Guided Tour](../../fable/chapters/ch70-specifications-guided-tour.md)

- [ ] **[COND]** **Deliver UNCLOS Art. 249 Cruise Report & Public Seabed 2030 / DCDB Contribution** (*Trigger:* foreign MSR consent or publicly funded survey). — *Threshold:* Submit final processed grids + metadata + requested raw subsets to participating coastal state within UNCLOS Art. 249 negotiated schedule (and release approved non-sensitive bathymetry with explicit GEBCO `TID 10–17` metadata to NCEI/DCDB/Seabed 2030). — *Evidence:* Transmittal receipt / DOI landing page. — *Ref:* [Ch. 69 Security & UNCLOS](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md) · [Sec. 24.2 Key Public DEM Products & TID](../../gemini4/book/ch-24/sec-24-02.md)

- [ ] **[REC]** **Evaluate Multi-Sensor Tiered Funnel ROI (USV vs. Ship / Airborne Lidar).** Quantify cost-per-square-kilometer savings and CO₂ reduction achieved by deploying the USV vs. a crewed ship or mothership force-multiplier, documenting optimal depth crossover points (`0–3 m` micro-USV vs. lidar; `3–200 m` semi-submersible; `200–7,000 m` ocean USV). — *Threshold:* Update organizational estimating rates for next bid cycle. — *Evidence:* Fleet ROI summary paragraph in AAR. — *Ref:* [Sec. 27.4 Reducing Cost](../../gemini4/book/ch-27/sec-27-04.md) · [Ch. 28 Reducing Cost](../../fable/chapters/ch28-reducing-cost.md)

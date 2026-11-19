# Coastal Bathymetric LiDAR — Resources, Standards Critique, and Copy-Ready Templates

Critical evaluation of primary coastal topo-bathymetric LiDAR standards, public programs, safety regulations, and processing tools, followed by an external statutory/standards register and three field-ready operational log templates. For cross-modality standards details and shared templates, see [appendix-d-standards-index.md](../../fable/appendices/appendix-d-standards-index.md), [ch19-bathymetric-lidar.md](../../fable/chapters/ch19-bathymetric-lidar.md), [ch70-specifications-guided-tour.md](../../fable/chapters/ch70-specifications-guided-tour.md), [ch28-reducing-cost.md](../../fable/chapters/ch28-reducing-cost.md), [sec-03-02.md](../../gemini4/book/ch-03/sec-03-02.md), [sec-09-02.md](../../gemini4/book/ch-09/sec-09-02.md), [sec-09-05.md](../../gemini4/book/ch-09/sec-09-05.md), [sec-09-06.md](../../gemini4/book/ch-09/sec-09-06.md), [sec-09-07.md](../../gemini4/book/ch-09/sec-09-07.md), [sec-24-01.md](../../gemini4/book/ch-24/sec-24-01.md), [sec-24-02.md](../../gemini4/book/ch-24/sec-24-02.md), [template-project-header.md](../_shared/template-project-header.md), [template-error-budget.md](../_shared/template-error-budget.md), [template-cost-ledger.md](../_shared/template-cost-ledger.md), [template-accident-card.md](../_shared/template-accident-card.md), [template-aar-retrospective.md](../_shared/template-aar-retrospective.md), and [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md).

---

## 1. Resource Quality Critique & Applicability Limits

| Resource / Authority / Tool | Primary Scope | Honest Strengths | Key Gaps, Traps, & Operational Watchouts |
| :--- | :--- | :--- | :--- |
| **USACE JALBTCX / National Coastal Mapping Program (NCMP)** | High-power dual-wavelength ALB + hyperspectral + RGB coastal corridor mapping (`~1,000 m` onshore to extinction). | Benchmark multi-decadal operational discipline, integrated white-ribbon workflows, and coastal corridor cost benchmarks (`~$1,780–$2,700+/km²` [`$4,600–$7,000+/mi²`] for full multi-sensor corridors vs. `~$385+/km²` [`$1,000+/mi²`] large-block baseline; *author/industry historical contracting estimates, 2020–2025 USD, mobilization- and quote-dependent; not a fixed handbook rate*). | Heavily tailored to specialized CZMIL/HawkEye aircraft on federal shoreline corridors; smaller river/harbor projects cannot directly replicate JALBTCX unit rates or aircraft readiness without substantial mobilization amortization. |
| **NOAA OCS Hydrographic Surveys Specifications and Deliverables (HSSD) & FPM** | Charting-grade hydrography (`2024 edition, restructured; annual updates`), BAG `FSD 2.0.1` (`+z ↑`), S-44 alignment, crosslines, holiday rules, and ALB turbidity workflows. | Authoritative operational checklist language for crosslines (`>= 4 %` at `>= 100 %` coverage; `>= 8 %` when `< 100 %`), `<= 24 h` DTON alerts, object detection (`S-57`), project/FPM optical clarity documentation (`>= 2` Secchi/turbidity checks per window as common project practice), and **BAG** uncertainty layers. | Written primarily around acoustic multibeam; ALB users must enforce HSSD's shallow-water optical extinction caveats, breaking-wave holiday exclusions, and strict sign conventions (`BAG +z ↑` vs. `S-102 +d ↓`). |
| **USGS Lidar Base Specification (2024 rev. A / 2025 rev. A)** | Topographic Quality Levels (`QL0–QL2`), `NVA/VVA`, LAS 1.4, swath overlap, and 3DEP ingest compliance. | Unmatched clarity for dry-beach / coastal-upland `1,064 nm` performance (`<= 0.10 m` `NVA` `RMSE_V` at QL1/QL2), **smooth-surface intra-swath precision (`RMSD_z <= 0.06 m`)**, **inter-swath overlap (`RMSD_z <= 0.08 m`)**, and `COPC` / `LAZ` delivery rules. | Does **not** natively define green-laser depth extinction, `n_p / n_g` two-index refraction, wave-surface `0.27 delta z_s` TPU growth, fixed cross-strip percentage, or benthic `Class 40–45` accuracy; combining LBS on land with HSSD/S-44 underwater requires an explicit Phase 1 crosswalk. |
| **ASPRS Positional Accuracy Standards Ed. 2 (v2) & LAS 1.4 Topo-Bathy Profile** | Statistical accuracy (`>= 30` checkpoints/stratum, quadrature `sqrt(RMSE_obs^2 + sigma_cp^2)`, no `RMSE`-only bluffing) and **Classes 40–45** (`Class 45` extinction logging). | Standardizes realistic `NVA` (`RMSE_V`) / `VVA` (reported) rules, enforces checkpoint uncertainty quadrature addition, and defines `40` (Bathy), `41` (Water Surface), `42` (Derived Water Surface), `43` (Submerged Object), `44` (S-57 Object), and `45` (No Bottom Found At). | Real-world vendor deliverables routinely misclassify breaking foam or kelp as `Class 40` or strip `Class 45` extinction records entirely, silently erasing turbidity blind spots unless audited in Phase 5 and Phase 7. |
| **IHO S-44 Ed. 6.2.0 & S-102 Ed. 3.0.0** | Depth-dependent Total Vertical/Horizontal Uncertainty (`Oct 2024`; core Table 1 TVU/THU $a/b$ values unchanged from Ed. 6.1.0 baseline in `fable/`, adding §3.8 seabed characteristics) and HDF5 bathymetric surface (`+d ↓`, `verticalCS = 6498`). | Platform-agnostic, depth-scaled `TVU/THU` formulas (`Order 1a`: `a=0.50 m, b=0.013`; `Special`: `a=0.25 m, b=0.0075`) and future-proof ECDIS surface interoperability (`S-102`). | **Sign-flip trap:** S-102 enforces positive **depth** (`+d ↓`, `verticalCS = 6498`) whereas BAG and LAS/COG TBDEMs enforce positive **elevation** (`+z ↑`); unverified sign handling at export corrupts chart depths fatally. |
| **ANSI Z136.1 / Z136.6 & FAA AC 70-1B / Form 7140-1 / STC Form 337 / § 91.509** | Outdoor eye safety (`NOHD`, `ENOHD`, `MPE`), NAS deconfliction, DoD LCH, airframe optical-port certification, and overwater life safety. | Concrete quantitative engineering framework for `532 nm` ocular risk (`0.40 mrad` to `7.5 mrad` divergence trade-offs), legal airspace clearance, and ditching readiness. | Frequently underestimated during bidding: **FAA Form 7140-1** reviews, belly-glass **STC/Form 337** approvals, and DoD LCH windows have multi-week lead times that cannot be compressed on site. |
| **NOAA VDatum, `vyperdatum`, & CUDEM** | Vertical datum transforms across ellipsoid (`NAD83`/`ITRF`), orthometric (`NAVD88`), and tidal (`MLLW`/`MHW`) surfaces. | Essential glue for single-CRS land–sea stitching across the white ribbon ([ch48-compositing.md](../../fable/chapters/ch48-compositing.md), [ch66-coastal-marine-polar-lakes-rivers.md](../../fable/chapters/ch66-coastal-marine-polar-lakes-rivers.md)). | `SEP` uncertainty is `5–10 cm` on open coasts and worsens to `10–20 cm` (`1σ`) inside complex estuaries and marsh channels ([ch09-vertical-datums.md](../../fable/chapters/ch09-vertical-datums.md)); blindly chaining incompatible epoch/geoid realizations produces `0.2–1.2 m` seam cliffs. |
| **ALB Software (`HydroFusion`, `RiHYDRO`, `LSS`, `PDAL`, `SlideRule atl24x`, `HydrOffice QC Tools`)** | Full-waveform deconvolution, two-index refraction, trajectory integration, ICESat-2 recon, and S-44/BAG QC. | `RiHYDRO` / `HydroFusion` / `LSS` handle vendor-specific dual-digitizer deconvolution and two-index refraction; `PDAL` (`filters.python` two-index refraction, `filters.smrf`, `filters.stats`, `COPC`, [sec-09-06.md](../../gemini4/book/ch-09/sec-09-06.md)) and `HydrOffice QC Tools` make independent open-source audits reproducible. | Official PDAL has no native `filters.refract` stage (`filters.python` is required), and proprietary packages sometimes obscure whether `n_p` vs. `n_g` and wave-surface smoothing were applied consistently; always cross-check deep overlap vs. MBES using independent Python/PDAL code (`07` § 5). |

### External Regulatory & Non-Handbook Source Register

Because aviation, ocular laser safety, overwater survival, marine casualty, hazmat, wildlife, cultural heritage, export, and insurance rules originate outside the two DEM handbooks, verify current statutory text prior to every mobilization (noting U.S. federal maritime/OSHA rules apply strictly in U.S. jurisdiction; international deployments follow flag-state, host-state CAA/MRCC, and **ICAO Annex 13** equivalents):

| Issuer / Regime | Regulation / Standard | Edition / As-Of Checked | Coastal ALB Scope |
| :--- | :--- | :--- | :--- |
| **ANSI / Laser Institute of America** | `ANSI Z136.1` & `ANSI Z136.6` | `2022` / `2015` (pre-mob check) | Outdoor laser MPE, `NOHD`, `ENOHD` (`Class 1` vs. `Class 1M` optical-aid hazard) |
| **FAA** | `AC 70-1B` + `Form 7140-1`; `Form 337` / `14 CFR Part 43` | Issued `14 Feb 2022` / `14 CFR` | Outdoor laser NAS deconfliction (`50 nW / 5 uW / 100 uW cm^-2`); belly-glass STC / AFMS (`337`) |
| **FAA / U.S. Code** | `14 CFR § 91.119`, `§ 91.211`, `§ 91.509`, `§ 119.1(e)(4)(iii)`, `§ 107.9`; `49 U.S.C. § 44807` | `14 CFR` current | Minimum altitudes, oxygen, overwater ditching gear (Subpart F adopted as floor), Part 135 survey exemption, UAS (`10 d` `§ 107.9`; `>= 25 kg` `§ 44807` COA) |
| **DoD / USSPACECOM** | Laser Clearinghouse (**LCH**) Predictive Avoidance | Current range/contract SOP | Blackout windows & predictive avoidance for millijoule `532 nm` lasers near restricted ranges |
| **IATA / PHMSA** | `IATA DGR 67th Ed.` (`PI 965 / PI 966`) & `49 CFR 171–180` | Eff. `1 Jan 2026` / `49 CFR` | `UN 3480 / 3481 <= 30 % SoC` air-freight limit; `UN 3090 / 3091` primary lithium beacons; `UN 38.3` & `SDS` |
| **NTSB** | `49 CFR Part 830` (`§ 830.2`, `§ 830.5`, `§ 830.15`) | Amended `2022` UAS rule | Immediate aircraft/certificated-UAS accident & `> $25k` non-aircraft damage reporting; 10-day Form 6120.1/2 |
| **USCG / OSHA / EPA** | `46 CFR § 4.05` (`CG-2692`), `§ 4.06`; `33 CFR § 153.203`; `29 CFR § 1904.39` | Current `CFR` (U.S. jurisdiction) | Boat/ditching marine casualty (`5 d`), `2 h / 32 h` SMI testing, NRC spill notice, `8 h / 24 h` OSHA eye loss (USCG-inspected vessel preemption noted) |
| **USFWS / NMFS / DOI** | `ESA`, `MMPA`, `MBTA`; `NHPA § 106` & `ARPA`; **CARE / OCAP®** | Current statutes & tribal agreements | Seabird/pinniped/marine-mammal altitude buffers, shipwreck/cultural redaction, indigenous data sovereignty |
| **Commerce / State / Privacy / Underwriters** | **EAR** (`15 CFR 730–774`), **ITAR** (`22 CFR 120–130`), **GDPR Art. 33** (`EU 2016/679`); Aviation/Marine/E&O COIs | Current `CFR` / EU Reg / Policy terms | `ECCN 7A003/6A005/6A008` export controls; `<= 72 h` PII/medical breach notice; Hull, Liability (no ocular exclusion), Overwater/IWL, `C&V` Payload Floater, E&O, Waiver of Subrogation |

---

## 2. Copy-Ready Operational Templates

### Template A — Secchi Disk, $K_d$, and CTD / Optical Clarity Field Log

````markdown
# ALB Water-Clarity, Secchi & CTD Field Log
- **Project / Sortie ID:** ____________________  | **Date (UTC):** YYYY-MM-DD
- **Vessel / Shore Team:** ____________________  | **Lead Observer:** ____________________
- **System / Nominal `d_max` Spec (`Z_SD` multiplier):** ____________________ (`1.5–3.0 Z_SD`; ICESat-2 recon floor `~1.0 Z_SD`)

| Station ID | UTC Time | Lat / Lon (WGS84 G2296 / NAD83(2011)) | Secchi Down `Z_down` (m) | Secchi Up `Z_up` (m) | Mean `Z_SD` (m) | Est. `K_d` (`~(1.44–1.70)/Z_SD`, `m^-1`) | Water Depth (m) | Temp (`deg C`) / Salinity (`PSU`) | `n_p` / `n_g` Applied | Sea State (`Beaufort / H_s m`) & Sun Glint | Status (`GO / DEFER / ABORT`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `STN-01` | | | | | | | | | | | |
| `STN-02` | | | | | | | | | | | |
| `STN-03` | | | | | | | | | | | |

- **Boat Safety & Notes (`VHF Ch 16` + CTAF check, PFDs worn, ZERO `7x50` binocs under `532 nm`, plume / foam / lutocline / CTD SHA-256):**
  ____________________________________________________________________________________
````

### Template B — Laser Safety, ANSI Z136.6 NOHD, & Geofenced Shutter Interlock Log

````markdown
# ALB Laser Safety, NOHD & Geofenced Shutter Verification Log
- **Aircraft Tail / Pod S/N:** ____________________ | **Sortie / Flight ID:** ____________________
- **Wavelengths (`nm`):** `532 nm` + `1,064 nm`     | **Laser Safety Officer (LSO):** ____________________
- **Max Pulse Energy (`mJ`) / Width (`ns`) / PRF (`kHz`) / Exit Dia (`mm`) / Div (`mrad`):** ____ mJ / ____ ns / ____ kHz / ____ mm / ____ mrad
- **Computed ANSI Z136.6 `NOHD` (m) & `ENOHD` (`7x50` binocs, m) + Class (`1` vs `1M`):** ______ m / ______ m / Class ____
- **Minimum Survey AGL Floor (`m` [statutory `ft`]):** ______ m (______ ft)
- **FAA AC 70-1B / Form 7140-1 Determination ID & Expiry:** ____________________
- **DoD Laser Clearinghouse (LCH) Window ID (if applicable):** ____________________

| Pre-Flight / In-Flight Check | Verified Value / State | Pass / Fail | Verifier Initials & UTC |
| :--- | :--- | :--- | :--- |
| Physical master-kill switch & operator abort accessible | | `[ ] PASS [ ] FAIL` | |
| Hardware AGL / altitude lockout floor armed (`>= NOHD` margin) | `______ m AGL` | `[ ] PASS [ ] FAIL` | |
| Geofenced no-fire polygons loaded (airports, beaches, vessels, wildlife) | `Filename / SHA256:` | `[ ] PASS [ ] FAIL` | |
| Bench test of automatic shutter trip across test polygon | `Trip latency: ___ ms` | `[ ] PASS [ ] FAIL` | |
| In-flight unplanned shutter trips or illumination alerts (`count / UTC`) | `Count: ___` | `[ ] NONE [ ] LOGGED` | |

- **Incident / Unintended Illumination Trigger Action:** Hit physical laser master-kill switch immediately, record UTC/lat/lon/AGL/speed/$E_p$/$\tau_p$/PRF/$D_0$/$\beta_t$/$f_{\text{scan}}$/attitude/viewing mode, notify LSO (`< 1 h`), refer exposed person for `< 24 h` retinal OCT exam, and open `06-accidents-and-emergencies.md` + `../_shared/template-accident-card.md`.
````

### Template C — ALB Sortie, Solar Elevation (`30–45°`), & White-Ribbon Tide-Sync Log

````markdown
# ALB Sortie, Solar Window & White-Ribbon Tide-Sync Log
- **Project / Block ID:** ____________________  | **Sortie #:** ____ | **Date (UTC):** YYYY-MM-DD
- **PIC / LiDAR Operator:** ____________________ / ____________________ | **Base Airfield:** ____________________
- **Planned Survey AGL / Speed / Scan Angle:** `______ m` / `______ m/s (______ kn)` / `______ deg (Palmer 15-20 deg)`
- **Target Tide Window (MLLW / MHW):** Low water `____ m` at `____ UTC` | High-water MBES/USV window: `____ UTC`
- **Solar Elevation Window (`30–45 deg` strict):** Window Open `____ UTC` | Window Close `____ UTC`
- **CORS (`<= 20 km`) / Project Base Station(s) Running:** ____________________ (Verified: `[ ]`)

| Line ID | Line Type (`Main / Cross / Boresight / Gap`) | Start UTC | End UTC | Solar Elev (`deg`) | Tide Stage (`m`, MLLW) | Mean `532 nm` SNR / Max Achieved Depth (`m`) | `1,064 nm` Surface Lock (`%`) | GNSS PDOP / Sat Count | Surf Foam / Cloud / Class 45 Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `L001` | | | | | | | | | |
| `L002` | | | | | | | | | |
| `XL01` | | | | | | | | | |

- **Post-Sortie Ingest & Preliminary QC Sign-Off:**
  - `[ ]` Raw digitizer waveforms + SBET raw + RGB/NIR + shutter logs copied to dual drives (`3-2-1`) & SHA-256 verified.
  - `[ ]` Daily PPK forward-backward separation `<= 0.05 m H / <= 0.10 m V (95 %)` verified.
  - `[ ]` Dry-beach `532/1,064 nm` residual `<= 0.03–0.05 m RMSE` (`|mean bias| <= 0.02–0.03 m`); Class 45 extinction polygons logged for MBES fill / repeat sortie.
````

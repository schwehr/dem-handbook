# Satellite-Built Elevations — Reference Software Critique & Operational Card Templates

This reference sheet pairs an operational, defect-focused critique of open-source software, satellite portals, and governing standards (`PRD.md` §6; [Appendix F](../../fable/appendices/appendix-f-software-index.md)) with copy-ready field and tasking cards covering the satellite workflow (`01`–`08`). Shared cross-modality forms live in `../_shared/` ([Project Header](../_shared/template-project-header.md), [Error Budget](../_shared/template-error-budget.md), [Cost Ledger](../_shared/template-cost-ledger.md), [Insurance COI](../_shared/template-insurance-coi.md), [Accident Card](../_shared/template-accident-card.md), [AAR Retrospective](../_shared/template-aar-retrospective.md), [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md)).

---

## 1. Critical Audit of Satellite Elevation Tools, Portals & Standards

| Tool / Standard / Portal | Primary Role & License | Proven Operational Strengths | Known Failure Modes & Guardrails | Key References |
| :--- | :--- | :--- | :--- | :--- |
| **NASA Ames Stereo Pipeline (`ASP`)** | Stereo/tri-stereo, `KH-9`/`KH-4B`, `bundle_adjust`, `jitter_solve` (`Apache-2.0`) | Rigorous CSM/pushbroom + RPC models; `asp_mgm` dense matching; native `jitter_solve` removes $\Lambda_k = v_{\mathrm{ground}} / f_k$ attitude ripples **strictly on rigorous CSM/linescan `.xml`/`.json` camera models** (never static `.rpb` RPCs); planetary/Earth parity | Fails silently if `mapproject` seed DEM has large datum offset or voids; default MGM settings blur thin urban edges unless `B/H` and kernel sizes are tuned; non-trivial RAM footprint on large mosaics | [ch22](../../fable/chapters/ch22-photogrammetry-sfm.md), [sec-08-05](../../gemini4/book/ch-08/sec-08-05.md), [sec-08-06](../../gemini4/book/ch-08/sec-08-06.md) |
| **PGC `SETSM` / CNES `CARS` / `s2p` / `MicMac`** | High-res optical satellite DSM engines (`GPL` / `Apache-2.0` / `CeCILL-B`) | `SETSM` powers `ArcticDEM`/`REMA`/`EarthDEM` with rock-solid `2 m` strip alignment; `CARS` scales cleanly via Dask/Docker on `Pléiades Neo`; `MicMac` excels on custom film frames | `SETSM` is tuned for open/polar bare terrain and struggles in narrow tropical urban street canyons without pre-configured `B/H` bounds; `s2p` uses tiled epipolar assumptions that drop edge tiles if `RPC` bias exceeds ~20 px | [ch22](../../fable/chapters/ch22-photogrammetry-sfm.md), [appendix-f](../../fable/appendices/appendix-f-software-index.md) |
| **`ISCE2` / `ISCE3` + `GMTSAR` + `SNAPHU`** | `Sentinel-1`, `NISAR`, `ALOS-2`, `TanDEM-X` InSAR processing (`Apache-2.0` / `GPL` / Stanford) | `ISCE3` is official `NISAR` production core (`GPU` accelerated); `GMTSAR` is lightweight and scriptable; `SNAPHU` delivers robust minimum-cost-flow phase unwrapping | Default `SNAPHU` tile cuts cause discrete `h_amb` (`2*pi`) jumps across low-coherence rivers/steep scarps; feeding an outdated/EGM-mismatched geocoding DEM creates circular horizontal shifts (`delta h / tan theta_i`) unless audited ([ch21](../../fable/chapters/ch21-radar-sar-insar.md)) | [ch21](../../fable/chapters/ch21-radar-sar-insar.md), [sec-11-07](../../gemini4/book/ch-11/sec-11-07.md), [appendix-f](../../fable/appendices/appendix-f-software-index.md) |
| **ESA `SNAP`** | GUI & `gpt` CLI InSAR / S1/S2 preprocessing (`GPL-3.0`) | Accessible visual quick-look burst/coherence inspection; broad Copernicus `S1`/`S2`/`S3` reader support | GUI batch runs silently drop Java heap memory or apply default bilinear interpolation + un-flagged `EGM96` transforms; strictly pin XML graphs in headless `gpt` and verify `POEORB` fetch | [ch21](../../fable/chapters/ch21-radar-sar-insar.md), [sec-11-07](../../gemini4/book/ch-11/sec-11-07.md) |
| **`SlideRule` & `icepyx` (`ICESat-2`)** | Cloud photon-level `ATL03`/`ATL06`/`ATL08`/`ATL24` extraction (`BSD-3`) | Eliminates multi-terabyte `NSIDC` HDF5 downloads via server-side photon classification & custom windowing | Default `ATL08` canopy/terrain classification degrades on slopes `> 20°` or cloudy low-SNR passes; for `ATL03` bathymetry, verify `ATL24` or apply explicit angle-dependent Snell refraction correction ([ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md)) | [ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md), [sec-09-06](../../gemini4/book/ch-09/sec-09-06.md), [ch51](../../fable/chapters/ch51-finding-data.md) |
| **`ACOLITE`** | Coastal atmospheric correction & SDB preprocessing (`GPL-3.0`) | Purpose-built Dark Spectrum Fitting (`DSF`) + `Hedley` deglinting for `Sentinel-2`, `Landsat`, `WorldView`, `Pléiades`, `SuperDove` over turbid waters | Assumes optically homogeneous dark targets exist within scene tiles; can over-subtract over shallow bright carbonate reefs or fail under heavy coastal cirrus (`<= 10 %` haze degrades `Stumpf` log-ratio drastically) | [ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md), [sec-11-03](../../gemini4/book/ch-11/sec-11-03.md), [appendix-f](../../fable/appendices/appendix-f-software-index.md) |
| **`xdem` & `demcoreg`** | 3D DEM co-registration (`Nuth–Kääb`), `NMAD` & variogram stats (`Apache-2.0`) | Standardizes `NuthKaab()`, `Deramp()`, `NMAD`, slope/aspect stratification, and geodetic uncertainty propagation | Misaligned `PixelIsArea` vs `PixelIsPoint` headers ([ch41](../../fable/chapters/ch41-change-detection.md)) corrupt shift vectors if metadata tags differ; always mask changing water/snow/forest before calling `.fit()` | [ch41](../../fable/chapters/ch41-change-detection.md), [sec-14-05](../../gemini4/book/ch-14/sec-14-05.md), [sec-33-01](../../gemini4/book/ch-33/sec-33-01.md) |
| **CEOS `ARD` (`CARD4L`) & `IHO B-13`** | Operational product specs (`NRB`/`POL`/`GSLC` & SDB Guidance Ed. 1.0.0) | `CARD4L` mandates explicit geocoding-DEM disclosure ([ch21](../../fable/chapters/ch21-radar-sar-insar.md)); `IHO B-13` (Mar 2024) sets honest uncertainty bins (`CATZOC C/D`) and independent holdout validation | Passing `CARD4L` radiometric formatting does **not** certify bare-earth accuracy or `InSAR` phase-unwrapping completeness; `IHO B-13` SDB cannot substitute for `S-44 Order 1a` port clearance | [ch21](../../fable/chapters/ch21-radar-sar-insar.md), [ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md), [sec-11-03](../../gemini4/book/ch-11/sec-11-03.md) |
| **Copernicus / `TanDEM-X` / `NISAR` / `SWOT` / `Biomass` Portals** | ASF DAAC, Copernicus Data Space, DLR EOWEB, Earthdata (`Open / Research`) | Free global/regional baselines (`GLO-30` `<4 m LE90`, `ArcticDEM` `2 m`, `NISAR DEM V1.2` ellipsoid-referenced at ASF, `SWOT` KaRIn water levels, `Biomass` P-band open access) | Mixing `Copernicus GLO-30` (`EGM2008`), `SRTM`/`AW3D30` (`EGM96`), and `TanDEM-X` / `NISAR DEM V1.2` (`WGS 84` ellipsoid) introduces `10–100 m` vertical step disasters if datum conversions are skipped | [appendix-e](../../fable/appendices/appendix-e-public-products-tables.md), [ch09](../../fable/chapters/ch09-vertical-datums.md) |

---

## 2. Copy-Ready Template A — Satellite Tasking Specification Card (`Phase 04`)

```markdown
### SATELLITE TASKING SPECIFICATION CARD
- **Project ID / AOI Polygon SHA-256:** ________________________ | **Track:** [ ] Optical Stereo [ ] Tri-Stereo [ ] InSAR [ ] SDB
- **Constellation / Sensor Mode:** ________________________ (e.g., Pleiades Neo 30 cm / WorldView Legion / TanDEM-X / NISAR / Sentinel-2)
- **AOI Area & Corridor Width Check:** _______ km^2 (Min >= 25 km^2 Neo/SkySat, >= 50 km^2 Legion) | Min Width: _____ km (>= 5 km narrow-corridor rule)
- **Tasking Window (UTC):** ____-__-__ to ____-__-__ | **Hard Abandon / Pivot Trigger Date:** ____-__-__
- **Solar & Orbit Constraints:** LTAN/LTDN _____ (verify per satellite; e.g., 10:00–10:30 Neo/S2, ~13:30 WV-3, 06:00/18:00 SAR) | Min Sun Elev: ___ deg (>=30 open / >=40 urban)
- **Optical Geometry SLA:** Off-Nadir <= ___ deg (<=25 urban / <=30 open) | Convergence alpha: ___ to ___ deg (15-25 urban / 30-45 open)
- **B/H & Same-Pass Continuity:** Target B/H ____ to ____ (0.26–0.83) | Max intra-triplet interval <= ____ s (<90 s) | Min AOI overlap >= 95%
- **Weather / Water SLA Ceiling:** Max AOI Cloud + Shadow <= ___ % (0 % over GCPs) | SDB Glint >= 20 deg off-spec | Wind <= ___ m/s (<7 m/s)
- **SAR / InSAR Geometry SLA:** Band ___ (X/C/L/P) | Pol ____ | B_perp range ___ to ___ m (< 0.35 B_perp,crit) | h_amb ___ to ___ m | Asc + Desc: [ ] Yes
- **Ephemeris / Sidecars Required:** [ ] RPC00B (.RPB) [ ] Rigorous CSM/ATT/EPH (.XML) [ ] POEORB (<5 cm) [ ] KH-9 1,081 Reseau Scan (7 um)
- **Vendor Acceptance / Rejection Clock:** ___ business days from delivery notice (verify PO; typ. 5–10 days) | Penalty-free cure/refund if SLA fails
- **EULA Derivative Clause Verified:** Non-reversible COG DEM client/public release permitted: [ ] YES (Counsel Sign: __________)
```

---

## 3. Copy-Ready Template B — Quick-Look Scene Acceptance / Rejection Gate Card (`Phase 05`)

```markdown
### QUICK-LOOK VENDOR ACCEPTANCE / REJECTION CARD (INSPECT WITHIN SLA CLOCK)
- **Task Order ID / Scene Strip ID:** ________________________ | **Delivery UTC:** ____-__-__T__:__Z | **SLA Expiry UTC:** ____-__-__T__:__Z
- **AOI Cloud + Cast Shadow (%):** _____% (Limit <= ____%) | **Primary GCPs Cloud-Free?** [ ] PASS [ ] FAIL (Blocked IDs: _________)
- **Realized Geometry:** ONA ___ deg | Convergence ___ deg | Realized B/H ____ | Stereo AOI Overlap _____% (>=95%) | Delta-t ___ s
- **Optical Radiometry:** Max Pan Clipped Saturation _____% (<0.5%) | Line Drops / Haze: [ ] NONE [ ] FAIL | Complete .RPB/.XML: [ ] YES
- **Target Visibility (if GCP/CR deployed):** Checkerboard/Siemens star centroid pickable (<=0.25 px)? [ ] YES [ ] N/A
- **SAR / InSAR Check (if radar):** Burst Sync (<15 ms): [ ] PASS | RFI Stripes: [ ] NONE | Realized B_perp ___ m | Bare gamma ____ (>=0.45)
- **SDB Check (if coastal optical):** Un-deglintable Sunglint _____% (<10%) | Whitecaps/Sediment Plume obscuring cal lines: [ ] NONE [ ] FAIL
- **IMMUTABLE INGEST (if ACCEPTED):** BagIt SHA-256 verified: [ ] YES (`manifest-sha256.txt`) | Stored 3-2-1 w/ EULA tag: [ ] YES
- **DISPOSITION:** [ ] **ACCEPT** (Proceed to Phase 07) | [ ] **REJECT — ISSUE VENDOR SLA NOTICE BEFORE EXPIRY** (Signed QA: _________)
```

---

## 4. Copy-Ready Template C — Ground-Crew GCP / Corner-Reflector & Safety Card (`Phases 02, 03, 06`)

```markdown
### FIELD GCP / SAR CORNER-REFLECTOR DEPLOYMENT & SAFETY LOG
- **Site ID / Role:** ___________ [ ] Bundle GCP [ ] WITHHELD CP (Vault Only) [ ] Trihedral CR [ ] Tide/Water Gauge
- **ROE / DOT Encroachment Permit #:** _________________ | **Wildlife / Biosecurity Buffer Cleared:** [ ] YES | **ATA Carnet / UN3480-3481:** [ ] N/A [ ] OK
- **Safety & Lone-Worker Gates:** ANSI Class 2/3 PPE + Cones: [ ] YES | Max Shift <=10 h Driving: [ ] YES | Garmin inReach Check-In Every: ___ h
- **GNSS Occupation QC:** Receiver S/N _______ | ANTEX (`igs20.atx`) _______ | PDOP <=3.0: ___ | C/N0 & AGC Spoofing Nominal: [ ] YES
- **Antenna Height (HI) Double-Check:** Read 1 (Crew A): ______ m | Read 2 (Crew B): ______ m | Photo Taken: [ ] YES | Delta <= 0.003 m
- **Optical Target Spec (if GCP/CP):** [ ] Siemens Star [ ] Checkerboard [ ] Crisp Corner | Diameter _____ m (5-10 x GSD) | Photo ID: _______
- **SAR Triangular Trihedral CR Spec (if CR):** Leg a = _____ m (sigma_max = _____ dBsm >= 20 dB SCR) | Drain holes clear: [ ] YES | Track: [ ] Asc [ ] Desc
- **CR Boresight Alignment:** Target Azimuth _____ deg | Boresight Elev _____ deg (35.26 deg base + tilt) | Within -3 dB (-18° to +18°) beam: [ ] YES
- **Apex / Monument Final Tie (ITRF2020@____.__):** E _________ m | N _________ m | Ellip h _________ m | Ortho H _________ m (Geoid: _________)
- **Post-Campaign Leave-No-Trace Removal & Site Sign-Off:** Date Removed ____-__-__ | Before/After Photos Logged: [ ] YES (Lead: ________)
```

---

## 5. External Regulatory & Technical Standards Register (`PRD.md` §7.4)

Because operational satellite workflows integrate statutory safety, transport, licensing, privacy, and charting frameworks published outside [Appendix D](../../fable/appendices/appendix-d-standards-index.md) and [Chapter 70](../../fable/chapters/ch70-specifications-guided-tour.md), verify current edition status at contract kickoff:

| Standard / Regulation | Issuing Body | Edition / Citation (As-Of 2026) | Scope in `satellite-elevation` Checklists |
| :--- | :--- | :--- | :--- |
| **15 CFR Part 960 & Kyl–Bingaman** | NOAA CRSRA (U.S. Dept. of Commerce) | 2020 Revision (Tier 1–3); KBA `0.40 m` (Jul 2020) | U.S. private space remote-sensing licensing, shutter-control tiers & Israel resolution cap (`02`, `09`) |
| **EAR (`15 CFR 730–774`) & ITAR (`22 CFR 120–130`)** | U.S. BIS / DDTC | Current Federal Rules | Dual-use POD/IMU/tactical GNSS export control & USML applicability (`02`, `06`) |
| **GDPR (`(EU) 2016/679`)** | European Union | In force (2018; Art. 33 `72 h` clock) | Privacy masking for `<= 0.5 m` imagery, field-crew PII/medical records & `<= 72 h` breach reporting (`02`, `06`) |
| **India DST Guidelines & China Surveying Law** | Govt. of India DST / PRC SAMR | India DST (Feb 2021); PRC Surveying Law | India `<1 m` H / `<3 m` V / `<10 m` bathy (`<= 500 m` / `100 m`) restrictions; China `GCJ-02`/`BD-09` obfuscation (`02`, `07`) |
| **NHPA §106, ARPA & CARE / OCAP®** | U.S. ACHP / Tribal / FNIGC | Statutory / CARE & OCAP® Governance | Cultural/archaeological site redaction & Indigenous data sovereignty consent (`00`, `02`, `07`) |
| **29 CFR § 1904.39 (OSHA) & 46 CFR § 4.05–4.06 / NRC** | U.S. OSHA / USCG (`33 CFR § 153.203`) | Current Federal Rules | Ground-crew `8 h` fatality / `24 h` hospital/eye clocks (`06`); SDB vessel `CG-2692` (`5 d`), SMI (`2 h`/`32 h`), `NRC` spill (`06`) |
| **IATA DGR (`UN 3480`/`3481`, `UN 3090`/`3091`, `UN 38.3`) & `49 CFR 171–180`** | IATA / UNECE / U.S. DOT & FAA PackSafe | **IATA DGR 67th Ed. (eff. Jan 1, 2026)** | **`<= 30 %` SoC mandatory for `UN 3480 PI 965 (CAO)` AND `UN 3481 PI 966`**, `100–160 Wh` passenger rules, `> 300 Wh` ground, `SDS` water/AVD vs Class D (`02`, `07`) |
| **ASPRS Positional Accuracy Standards** | ASPRS | Edition 2, v2 (2024; Addenda I–VI) | Reports `1σ` `RMSE_V`/`RMSE_H`/`RMSE_3D` with unconditional `sigma_cp` quadrature & `>= 30`/stratum CPs (`00`, `01`, `03`, `07`, `08`) |
| **IHO `B-13`, `S-44` & `MIL-PRF-89020B`** | IHO / U.S. NGA | `B-13` Ed. 1.0.0 (Mar 2024); `S-44` Ed. 6.2.0 (Oct 2024; core Table 1 TVU/THU a/b unchanged from Ed. 6.1.0, adding §3.8 seabed characteristics) | `SDB` `2 m` bin holdout validation & `CATZOC C/D`; legacy `CE90`/`LE90` benchmarks (`00`, `01`, `07`) |
| **CEOS `ARD` (`CARD4L`), Copernicus DEM & TanDEM-X Specs** | CEOS / ESA / DLR | `CARD4L` v5.5 (2022); Copernicus Iss. 5.0/6.1; `TD-GS-PS-0021` | Geocoding-DEM circularity disclosure ([ch21 §21.6](../../fable/chapters/ch21-radar-sar-insar.md)) & Copernicus/TanDEM-X accuracy specs (`00`, `07`) |
| **ANSI/ISEA 107 & `MUTCD`** | ISEA / U.S. FHWA | ANSI 107-2020; MUTCD 11th Ed. (2023) | Ground-truth roadside Class 2/3 PPE & work-zone traffic control (`02`) |
| **Commercial & Field Insurance COIs** | ACORD / Industry Underwriting | Active Policy Term (`>= 30 d` buffer) | `E&O`, `CGL`, `Commercial Auto`, `Inland Marine + C&V`, `Workers' Comp`, `FVWC`/Medevac, `Waiver of Subrogation` (`02`) |
| **ISO 19111 / 19115 / WKT2:2019 & OGC COG / STAC** | ISO / OGC | ISO 19162:2019; OGC COG 1.0; STAC 1.1.0 | Compound CRS + pinned geoid/SEP ([ch08](../../fable/chapters/ch08-horizontal-datums.md)–[ch09](../../fable/chapters/ch09-vertical-datums.md)) & cloud-native packaging (`07`) |

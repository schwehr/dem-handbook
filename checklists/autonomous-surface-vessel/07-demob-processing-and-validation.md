# Autonomous Surface Vessel (ASV / USV) — Phase 07: Demobilization, Final Processing & Validation

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `autonomous-surface-vessel`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________`  
> **Vessel / Hull Class & Governing Spec:** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

**HARD STOP RULE:** Never release the USV, rented sonar/INS hardware, charter chase boat, or shore GNSS base before verifying **100 % SHA-256 raw data custody** and completing the pre-teardown reference-surface closure pass.

---

## 1. Pre-Teardown Closure & Non-Negotiable Raw Custody Gates

- [ ] **[GATE]** **Run Post-Survey Reference Surface Closure Pass & Final Static Waterline / Draft Check.** Prior to hoisting the USV onto trailer/cradle or removing any sonar mount, acquire reciprocal lines over the Phase 03 hard-bottom Reference Surface + fresh SVP cast, then measure static draft marks in calm water and close out, physically recover, and post-calibrate any temporary subordinate tide gauge & shore GNSS base. — *Threshold:* Pre- vs. post-survey Reference Surface mean vertical shift **$\le 0.03\text{–}0.05\text{ m}$** (check $95\%$ difference inside IHO S-44 Special/Order 1a TVU); shore RTK base tripod height closing check agrees to **$\le 0.002\text{ m}$** with closing photograph; subordinate tide-gauge closing staff-to-benchmark level loop closes within **$\le 6\text{ mm}\sqrt{K}$** ($K$ in km) with post-recovery pressure/zero-drift check verified. — *Evidence:* Pre-vs-post reference surface diff raster + closing draft/base/leveling log sheets + recovered gauge calibration sheet. — *Ref:* [Ch. 25 Calibration Infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md) · [Ch. 20 Sonar](../../fable/chapters/ch20-sonar.md)

- [ ] **[GATE]** **Verify Post-Survey Patch-Test Boresight Repeatability & Pole Witness Marks.** Compare pre-survey vs. post-survey patch-test solutions (and inspect witness paint on all strut/pole clamps) before unbolting transducers to prove zero mechanical slip occurred during deployment. — *Threshold:* Pre- vs. post-survey roll drift **$\le 0.05^\circ$**, pitch drift **$\le 0.10^\circ$**, yaw drift **$\le 0.15^\circ$**; unbroken torque-witness paint on all fasteners (any slip triggers retrospective line-segment boresight partitioning). — *Evidence:* Pre- vs. post-patch comparison table + fastener witness-paint photos. — *Ref:* [Sec. 13.1 Geometric Survey Design & Boresight](../../gemini4/book/ch-13/sec-13-01.md) · [Sec. 13.5 Boresight Calibration Math](../../gemini4/book/ch-13/sec-13-05.md) · [Sec. 7.4 Marine Platforms & Pole Flexure](../../gemini4/book/ch-07/sec-07-04.md)

- [ ] **[GATE]** **Verify 100 % Raw Custody & SHA-256 BagIt Manifests BEFORE Vessel, Sensor, or Rental Release.** Copy and hash-verify every `.kmall`/`.all`/`.s7k`/`.xtf` sonar file, GNSS RINEX/`.t04`/`.pos`, raw IMU, SVS/SVP casts, total-station lever-arm sheets, AIS/EO-IR event logs, watch sheets, and helm logs across all **3-2-1 backup tiers**. — *Threshold:* **100 % bit-exact SHA-256 match** across primary archive NAS, off-site ruggedized shuttle SSD, and cold/cloud bucket (`bagit --sha256` per **RFC 8493**); **zero onboard media wiped** until independent read-back succeeds in the processing office. — *Evidence:* Signed Raw Custody Release Certificate + `sha256sum -c` / BagIt `valid` stdout log. — *Ref:* [Ch. 50 Archiving & Provenance](../../fable/chapters/ch50-archiving-and-provenance.md)

---

## 2. Physical Demob: Washdown, Battery SoC, Customs & Maritime Closeout

- [ ] **[GATE]** **Perform Invasive-Species Freshwater Desalination Washdown & Sensor O-Ring Care.** Thoroughly flush hull, gondola/strut joints, jet/thruster seals, engine cooling heat-exchangers, winched SVT housings, and wet-mate connectors with clean freshwater, scrub biofouling per aquatic invasive-species rules before crossing watershed/state lines, inspect sacrificial anodes, and lubricate wet-mate pins with silicone dielectric per OEM manual. — *Threshold:* Zero standing salt crust, barnacles, or aquatic weeds on hull/trailer; wet-mate pins dry and capped with protective dust boots before crating. — *Evidence:* Invasive-species washdown checklist & equipment closeout photos. — *Ref:* [Phase 09 External Regulatory Register](./09-resources-and-templates.md#e-external-regulatory--operational-basis-register-non-handbook-sources)

- [ ] **[GATE]** **Prepare Batteries for Storage / UN 3480 & UN 3481 Transport & Remove UN 3090 Primary Cells.** Discharge/balance LiFePO₄ or Li-ion packs to regulatory transport/storage State of Charge (SoC), pack terminal-protected UN-certified Class 9 boxes with UN 38.3 summary + SDS, and remove/isolate any UN 3090/3091 lithium-metal primary cells in PLBs/EPIRBs/transponders. — *Threshold:* **$\le 30\%$ SoC** for air transport under **IATA DGR (67th Ed., Jan 2026) UN 3480 `PI965` (standalone, Cargo Aircraft Only [`CAO`] > limit) and UN 3481 `PI966` (packed with equipment, $\le 30\%$ mandatory Jan 2026) / `PI967`**; for extended shelf storage hold **$30\text{–}50\%$ SoC ($\approx 3.3\text{ V/cell}$ nominal for LiFePO₄ vs. $\approx 3.8\text{ V/cell}$ for NMC Li-ion)**; terminals insulated against short circuit; hazmat Shipper's Declaration signed for packs $>300\text{ Wh}$ (49 CFR 171–180 / IMDG). — *Evidence:* Cell-voltage log, hazard labels photo, and dangerous-goods waybill. — *Ref:* [Phase 09 External Regulatory Register](./09-resources-and-templates.md#e-external-regulatory--operational-basis-register-non-handbook-sources)

- [ ] **[GATE]** **Complete Joint On-Hire / Off-Hire Vessel Inspection, ATA Carnet Closeout & Close USCG LNM / Harbor Advisories.** Conduct joint walk-around with chase-boat/mothership master or pier manager to sign off hull/deck restoration, clear ATA Carnet re-export customs stamps where international, and explicitly cancel active USCG Local Notices to Mariners (LNMs), Harbor Master safety zones, and marine-fishery advisories. — *Threshold:* Zero unclosed maritime notices left active after USV departs operational waters; Carnet export/re-import sheets countersigned by Customs prior to departure. — *Evidence:* Signed Off-Hire Condition Receipt, LNM cancellation email/confirmation, and stamped Carnet. — *Ref:* [Ch. 68 Legal Issues](../../fable/chapters/ch68-legal-issues.md) · [Phase 09 External Regulatory Register](./09-resources-and-templates.md#e-external-regulatory--operational-basis-register-non-handbook-sources)

---

## 3. Reproducible Post-Processing, Vertical Reduction & Surface Generation

- [ ] **[GATE]** **Process RTS-Smoothed SBET Trajectory, Delayed TrueHeave / ERS Reduction & Verify Sign Polarity.** Solve post-processed PPK/PPP-AR + FOG/MEMS INS trajectory with **Rauch–Tung–Striebel (RTS)** forward-backward smoothing (halving GNSS outage spikes), verify forward-backward separation residuals, and apply pinned vertical datum transformation (`VDatum` [pinned release, e.g., v4.5+] / `VORF` / `AusCoastVDT` / `GGXF` SEP grid or final verified CO-OPS water levels). — *Threshold:* Forward-backward SBET trajectory separation **$<0.02\text{–}0.03\text{ m}$ ($1\sigma$)** throughout nominal lines (flag and inspect any spike **$>0.05\text{–}0.10\text{ m}$**); explicitly test PROJ `+proj=vgridshift` sign convention (`z_CD = h - SEP`, `d_CD = SEP - h`) against 1+ verified Tide Gauge / `GNSS@TG` benchmark so SEP shifts are **applied with zero sign inversion** (`Ch. 9` / `Ch. 56` trap); run full circular-arc Snell ray tracing across all accepted `.svp`/winched-SVT casts. — *Evidence:* SBET separation QC plot, pinned PROJ/VDatum pipeline version + grid SHA-256, and zero-sign-error monument check. — *Ref:* [Ch. 13 IMU & INS](../../fable/chapters/ch13-imu-ins.md) · [Ch. 9 Vertical Datums](../../fable/chapters/ch09-vertical-datums.md) · [Sec. 10.4 Refraction & Ray Tracing](../../gemini4/book/ch-10/sec-10-04.md)

- [ ] **[GATE]** **Run Pinned Processing Pipeline (CUBE / CHRT + Designated Soundings + Shoal-Biased Cleaning).** Record exact container digest / `Kluster` / `Qimera` / `CARIS` / `MB-System` version, apply verified 4-step patch test boresights + angular-rate/aeration filters, build Variable-Resolution (VR) or fixed-resolution CUBE surfaces, and enforce **Designated Soundings** for wrecks, pilings, boulders, and DTONs so surface smoothing never suppresses least depths. — *Threshold:* Reproducible environment lockfile/container hash archived; CUBE hypotheses verified on all shoal features (`0` critical DTONs clipped by statistical gridding); flag/remove micro-USV motion spikes where instantaneous angular rates exceeded $\dot\phi,\dot\theta > 30^\circ/\text{s}$ and failed outer-beam TVU. — *Evidence:* Processing provenance JSON (`W3C PROV` / `ISO LI_Lineage`), designated-sounding table, and cleaning audit trail. — *Ref:* [Ch. 29 Processing Pipelines](../../fable/chapters/ch29-processing-pipelines.md) · [Ch. 62 Shoal-Biased Selection](../../fable/chapters/ch62-navigation-and-charting.md)

---

## 4. Independent Statistical & Multi-Modal Validation

- [ ] **[GATE]** **Audit Crossline vs. Mainscheme Agreement Across Depth Bins & Swath Angles.** Difference validated crosslines against mainscheme surface, record residuals in [`template-error-budget.md`](../_shared/template-error-budget.md), and evaluate performance binned by depth bracket and outer beam angle ($\theta \in [0^\circ, 65^\circ]$) using parametric and robust metrics. — *Threshold:* **$\ge 95\%$ of crossline soundings/cells** fall inside governing **IHO S-44 Ed. 6.2.0 (Oct 2024; core Table 1 TVU/THU $a/b$ values unchanged from Ed. 6.1.0, adding §3.8 seabed characteristics)** / HSSD / USACE allowable $TVU_{95\%}$; inspect both mean bias (should be **$\approx 0.00\text{–}0.03\text{ m}$**) and robust dispersion **$\text{NMAD} = 1.4826\cdot\text{median}(|e - \text{median}(e)|)$** + **P95**; flat/zero overall bias must NOT mask opposing outer-beam refraction curls ($+\text{smile}$ vs. $-\text{frown}$) when binned by angle! — *Evidence:* Angle-binned crossline difference histogram and S-44 compliance pass/fail table. — *Ref:* [Ch. 53 Accuracy Assessment](../../fable/chapters/ch53-accuracy-assessment.md) · [Sec. 14.2 Error Metrics & S-44 Compliance](../../gemini4/book/ch-14/sec-14-02.md)

- [ ] **[GATE]** **Verify Spatial Grid Resolution, Sounding Density ($\ge 5$/Node) & Holiday Compliance.** Run automated `HydrOffice QC Tools` / `s102` density and gap audits across every HSSD VR-BAG depth bracket ($0.5\text{–}16\text{ m}$) or fixed grid resolution. — *Threshold:* **$\ge 95\%$ of populated grid cells contain $\ge 5$ soundings**, zero unexplained coverage holidays larger than $3\times 3$ cells, and zero least-depth shoals suppressed by smoothing. — *Evidence:* `HydrOffice` Grid QA + Holiday Finder PDF/JSON reports attached to Descriptive Report. — *Ref:* [Sec. 24.1 Survey Guide Documents & HSSD](../../gemini4/book/ch-24/sec-24-01.md) · [Sec. 13.6 Software Ecosystem](../../gemini4/book/ch-13/sec-13-06.md)

- [ ] **[REC]** **Archive Exact Container Digest, Lockfiles & Vertical Transformation Grids (`VDatum` / `GGXF`).** Bundle the pinned processing environment manifest alongside the exact `VDatum`/`VORF`/geoid grid file hashes so future audits reproduce grids deterministically. — *Threshold:* Complete reproducibility manifest verified alongside BagIt RFC 8493 archive package. — *Evidence:* `environment.lock` / OCI digest + `vdatum_grid.sha256` inside archive `lineage/` folder. — *Ref:* [Ch. 29 Processing Pipelines](../../fable/chapters/ch29-processing-pipelines.md) · [Ch. 50 Archiving & Provenance](../../fable/chapters/ch50-archiving-and-provenance.md)

- [ ] **[COND]** **Enforce CARE / OCAP® / Sovereign Data Embargoes & UNCLOS Art. 249 Cruise Delivery** (*Trigger:* tribal waters, defense security zones, or foreign EEZ MSR clearance). — *Threshold:* Strip/quarantine restricted high-resolution grids per security classification or Indigenous governance agreement prior to public NCEI/DCDB ingest, and submit negotiated UNCLOS Art. 249 coastal-state data package within diplomatic timeline. — *Evidence:* Redaction/embargo clearance sign-off or Art. 249 transmittal receipt. — *Ref:* [Ch. 69 Security & UNCLOS Art. 249](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md) · [Ch. 68 Legal Issues](../../fable/chapters/ch68-legal-issues.md)

- [ ] **[COND]** **Validate Multi-Modal White-Ribbon Intertidal Seam & Co-Registration** (*Trigger:* project stitches USV MBES with coastal/topobathy lidar or beach RTK). — *Threshold:* Extract overlapping 100–500 m intertidal zone ($+z \uparrow$ common epoch/datum), quantify vertical bias, NMAD, P95, and **Nuth & Kääb (2011)** horizontal shift vector ($\Delta x, \Delta y, \Delta z$) vs. slope/aspect; verify shoreline discontinuity **$\le 0.15\text{–}0.25\text{ m}$ ($95\%$)** before blending seamlines ([`multimodal-white-ribbon.md`](../_shared/multimodal-white-ribbon.md)). — *Evidence:* Co-registration scatter/aspect plot and blended transition QC hillshade. — *Ref:* [Ch. 34 Water in DEMs](../../fable/chapters/ch34-water-in-dems.md) · [Sec. 14.5 Nuth & Kääb Co-Registration](../../gemini4/book/ch-14/sec-14-05.md)

- [ ] **[GATE]** **Validate Final BAG 2.0.1 / IHO S-102 Ed. 3.0.0 / COG Deliverables & Archive Submission.** Verify HDF5 structural integrity, sign conventions (`BAG` elevation `+z ↑`, `S-102` depth `+d ↓` / `verticalCS == 6498`), uncertainty layers (`productUncert` 95 % vs. `1σ`), VR-BAG refinement grids (`/BAG_root/varres_refinements`), `float64` spatial transforms (zero `float32` coordinate ulp rounding), metadata (`ISO 19115`, `S-158:102`, `STAC`), and final ingestion receipt from Client / NOAA NCEI / DCDB / Seabed 2030. — *Threshold:* **Zero validation errors** in `S-158:102` / `HydrOffice` / `gdalinfo` / `rio cogeo validate`; explicit `AREA_OR_POINT=Area` vs. `Point` tag audit passed. — *Evidence:* Schema validator outputs (`PASS`), archive DOI/accession ticket, and metadata XML/JSON. — *Ref:* [Ch. 47 File Formats](../../fable/chapters/ch47-file-formats.md) · [Sec. 24.1 Survey & Product Guide Documents](../../gemini4/book/ch-24/sec-24-01.md) · [Sec. 19.1 Key File Formats](../../gemini4/book/ch-19/sec-19-01.md)

---

## 5. Runnable Post-Processing Validation Snippets (Working Copy)

```python
import h5py
import numpy as np

def audit_bag_v2_and_s44(bag_path: str, a_const: float = 0.50, b_factor: float = 0.013,
                          uncert_is_1sigma: bool = False) -> dict:
    """Verify BAG v2.0.1 elevation (+z up), 95% IHO S-44 Ed. 6.2.0 TVU scaling, and VR-BAG presence.

    Inspect /BAG_root/metadata XML 'uncertaintyType' ('productUncert' vs 'rawStdDev'/'cubeStdDev')
    to set uncert_is_1sigma; for IHO S-102 Ed. 3.0.0 (+d down), verify verticalCS == 6498.
    """
    with h5py.File(bag_path, "r") as f:
        elev = f["/BAG_root/elevation"][:]
        uncert = f["/BAG_root/uncertainty"][:]
        has_vr = "varres_refinements" in f["/BAG_root"]
        fill = float(f["/BAG_root/elevation"].attrs.get("Fill Value", 1e6))
        valid = (elev != fill) & (uncert != fill) & np.isfinite(elev) & np.isfinite(uncert)
        if not np.any(valid):
            raise ValueError(f"No valid BAG grid nodes found in {bag_path}.")
        depth_m = np.maximum(-elev[valid], 0.0)  # BAG elevation (+z up) -> positive depth
        tvu_95 = 1.96 * uncert[valid] if uncert_is_1sigma else uncert[valid]
        allowable_tvu = np.sqrt(a_const**2 + (b_factor * depth_m)**2)
        pass_pct = 100.0 * np.mean(tvu_95 <= allowable_tvu)
        return {
            "valid_nodes": int(np.sum(valid)),
            "has_vr_refinements": has_vr,
            "dtype_elev": str(elev.dtype),
            "median_tvu95_m": round(float(np.median(tvu_95)), 4),
            "p95_tvu95_m": round(float(np.percentile(tvu_95, 95)), 4),
            "s44_pass_pct": round(float(pass_pct), 2),
        }

def nuth_kaab_coreg_shift(z_usv: np.ndarray, z_lidar: np.ndarray,
                          pixel_size_m: float, north_up: bool = True,
                          min_slope_deg: float = 3.0) -> dict:
    """Estimate horizontal (dx_east, dy_north) and vertical bias on +z up overlap."""
    dz = z_lidar - z_usv
    gy_row, gx = np.gradient(z_usv, pixel_size_m)
    gy_north = -gy_row if north_up else gy_row
    slope = np.arctan(np.hypot(gx, gy_north))
    aspect = np.arctan2(-gx, -gy_north)  # downslope azimuth clockwise from North
    valid = np.isfinite(dz) & np.isfinite(slope) & (slope > np.deg2rad(min_slope_deg))
    if np.sum(valid) < 25:
        raise ValueError("Insufficient sloped intertidal overlap pixels for co-registration.")
    y = dz[valid] / np.tan(slope[valid])
    med = np.median(y)
    nmad = 1.4826 * np.median(np.abs(y - med))
    keep = np.abs(y - med) <= 3.0 * max(nmad, 1e-6)
    ang, slp = aspect[valid][keep], slope[valid][keep]
    # dz/tan(alpha) = dx_east*sin(psi) + dy_north*cos(psi) + dz_bias*cot(alpha)
    design = np.column_stack([np.sin(ang), np.cos(ang), 1.0 / np.tan(slp)])
    dx_east, dy_north, dz_bias = np.linalg.lstsq(design, y[keep], rcond=None)[0]
    return {"dx_east_m": round(float(dx_east), 3), "dy_north_m": round(float(dy_north), 3),
            "dz_bias_m": round(float(dz_bias), 3), "n_used": int(np.sum(keep))}
```

```bash
# MB-System final tide/SVP lock & crossline diff grid check on working copy
mbset -Iqc_scratch/datalist.mb-1 -PSVPFILE:qc_scratch/master_svp_catalog.svp
mbprocess -Iqc_scratch/datalist.mb-1
# Compare crosslines vs. mainscheme grid via GMT grdmath
gmt grdmath qc_scratch/crosslines.grd qc_scratch/mainscheme.grd SUB = qc_scratch/xline_diff.grd
gmt grdinfo -L2 qc_scratch/xline_diff.grd
```

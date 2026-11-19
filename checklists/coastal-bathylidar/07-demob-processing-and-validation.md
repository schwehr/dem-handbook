# Coastal Bathymetric LiDAR — Demobilization, Processing, and Validation

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `coastal-bathylidar` | **Platform / Vessel / Tail #:** `__________________` | **Governing Spec:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

Aircraft/field-team demobilization gates, deterministic dual-band waveform processing (deconvolution, two-index $n_p$ vs. $n_g$ vector Snell refraction, Class 40–45 topo-bathy classification, and BAG/S-102/COG packaging), and independent MBES/USV, checkpoint, and ICESat-2 accuracy validation. See [ch19-bathymetric-lidar.md](../../fable/chapters/ch19-bathymetric-lidar.md), [ch29-processing-pipelines.md](../../fable/chapters/ch29-processing-pipelines.md), [ch48-compositing.md](../../fable/chapters/ch48-compositing.md), [ch53-accuracy-assessment.md](../../fable/chapters/ch53-accuracy-assessment.md), [sec-09-05.md](../../gemini4/book/ch-09/sec-09-05.md), and [sec-14-02.md](../../gemini4/book/ch-14/sec-14-02.md).

---

## 1. Demobilization Gates (Before Aircraft & Team Release)

- [ ] **[GATE]** **Post-Campaign Boresight & Flat-Surface Range Closure BEFORE Aircraft Release:** Fly a closing boresight cross-line/reciprocal pass over the calibrated dry runway/flat surface AND a calm overlapping flat-seabed line **before releasing the aircraft or pod from project mobilization**; verify boresight drift (`< 0.005°` angular / `< 0.05 m` vertical step `95 %` across opposite headings) and dry-beach `532 nm` vs. `1,064 nm` residual (`<= 0.03–0.05 m` `RMSE`, `|mean bias| <= 0.02–0.03 m`) to confirm zero window bowing or mechanical shock over the campaign (`[ ] Passed` `[ ] Re-fly Required`). — *Threshold:* Closing boresight and flat-seabed residuals within pre-mob tolerance; any step drift `> 0.05 m` isolates affected sorties prior to ferry. — *Evidence:* Signed Closing Boresight & Green–NIR Beach Closure Report. — *Ref:* [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md) §19.3, [Chapter 25](../../fable/chapters/ch25-calibration-infrastructure.md) §25.5–25.6, [Section 13.5](../../gemini4/book/ch-13/sec-13-05.md).
- [ ] **[GATE]** **100 % Raw Custody & SHA-256 Verification Prior to Aircraft/Crew Release:** Confirm that all raw digitizer waveforms, scanner angles, raw IMU/GNSS (`T04`/RINEX), camera frames, laser geofence/shutter audit logs, and field Secchi/CTD/tide files exist on **at least two independent checksummed archives (`3-2-1` rule)** with zero missing flight lines or un-indexed sorties before authorizing ferry departure. — *Threshold:* `100 %` expected flight lines and sensor files matched against verified `SHA256SUMS.txt` across dual physical archives + off-site sync. — *Evidence:* Verified Raw Custody Manifest & Dual-Archive Checksum Report. — *Ref:* [Chapter 29](../../fable/chapters/ch29-processing-pipelines.md), [Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md).
- [ ] **[REC]** **Belly-Glass Preservation, Laser Purge, Return Hazmat Packing, & Lever-Arm Spot Check:** Inspect dual-band belly glass after salt-spray wipe-down (`DI water + lens tissue`), install protective transit cover, purge chiller/desiccant per OEM transit spec, spot-check IMU-to-GNSS-to-window lever arms if fasteners were disturbed, pack `UN 3480 / UN 3481` Li-ion spares at **`<= 30 % SoC`** (`IATA DGR 67th Ed., Jan 2026`) + `UN 3090/3091` cells with SDS/`UN 38.3`, and execute Secchi/CTD vessel washdown & aquatic biofouling inspection. — *Threshold:* Zero uninspected optical residue, non-compliant lithium air-freight packs, or invasive-species transfer on launches/CTDs. — *Evidence:* Signed Equipment Preservation, Lithium Return Packing & Biofouling Log. — *Ref:* [09 External Register](09-resources-and-templates.md), [Section 7.3](../../gemini4/book/ch-07/sec-07-03.md) §7.3.3.
- [ ] **[GATE]** **Project GNSS Base & Temporary Tide Gauge Closing Ties:** Perform closing static GNSS checks and third-order/level-loop ties (`<= 3–5 mm` closure tolerance) between any temporary project water-level gauge and **>= 3 primary local tidal benchmarks (`5` recommended in subsiding/estuarine reaches per IOC Manual 14)** prior to sensor retrieval. — *Threshold:* Closing benchmark loop misclosure `<= 3–5 mm` and closing static GNSS base delta `<= 0.02 m` (`h`); zero datum shift over deployment. — *Evidence:* Closing Level-Loop Sheet & OPUS/Static Base Comparison. — *Ref:* [Chapter 9](../../fable/chapters/ch09-vertical-datums.md) §9.3, [Chapter 25](../../fable/chapters/ch25-calibration-infrastructure.md) §25.2–25.3.
- [ ] **[REC]** **Permit, Airspace Closeout & Off-Hire Aircraft W&B Restoration:** Cancel active low-altitude coastal **NOTAMs** and **LNMs**, close **FAA Form 7140-1 / DoD LCH** laser windows, sign **joint off-hire aircraft condition and Weight & Balance / STC restoration** records when un-installing the ALB rack/belly port, remove temporary ground targets/marsh plates, and return signed landowner/tribal access logs. — *Threshold:* Zero orphaned NOTAMs, open LCH windows, unrecovered coastal targets, or unsigned W&B restoration entries. — *Evidence:* NOTAM/7140-1 Closeout Confirmation & Signed Off-Hire W&B Sheet. — *Ref:* [09 External Register](09-resources-and-templates.md), [Chapter 16](../../fable/chapters/ch16-platforms.md).

---

## 2. Deterministic Processing, Waveform Deconvolution, & Two-Index Refraction

- [ ] **[GATE]** **Pinned Software, CRS, & VDatum/Geoid Environment:** Lock exact versions of trajectory/LiDAR tools (e.g., POSPac MMS, RiHYDRO, HydroFusion, Leica Survey Studio, PDAL, PROJ/VDatum, `vyperdatum`) and exact geoid/SEP grids from [template-project-header.md](../_shared/template-project-header.md) into a single reproducible configuration manifest; reject mixed vertical CRSs across adjacent land and seabed tiles (preventing NAVD88/MLLW step discontinuities). — *Threshold:* Exact software container/version hashes and VDatum/geoid grid SHA-256 recorded; `allow_ballpark=False` transformation audit passes on every CRS step. — *Evidence:* Pinned Processing Environment Manifest & Non-Ballpark PROJ Check Log. — *Ref:* [template-project-header.md](../_shared/template-project-header.md), [Chapter 29](../../fable/chapters/ch29-processing-pipelines.md), [Section 9.6](../../gemini4/book/ch-09/sec-09-06.md).
- [ ] **[GATE]** **Tightly Coupled RTS Trajectory (SBET) Verification:** Process dual-frequency PPK trajectories against coastal CORS ($\le 20\text{ km}$) / project base stations using exact `igs20.atx` ANTEX phase centers; confirm forward–backward separation `<= 0.05 m` horizontal and `<= 0.10 m` vertical (`95 %`), and publish `SMRMSG` covariance (`1σ`) alongside SBET before point generation. — *Threshold:* Fixed ambiguity `>= 95–99 %`, forward–backward delta `<= 0.05 m` H / `<= 0.10 m` V (`95 %`), and `igs20.atx` codes verified against field antenna photos. — *Evidence:* Final Trajectory Processing Report (`SMRMSG` & Separation Plots). — *Ref:* [Chapter 12](../../fable/chapters/ch12-gnss.md) §12.6, [Chapter 13](../../fable/chapters/ch13-imu-ins.md) §13.8.
- [ ] **[GATE]** **Shallow-Water Waveform Deconvolution (`d < 1.0 m`):** Apply Gaussian, exponentially modified Gaussian (EMG), or Richardson–Lucy waveform deconvolution constrained by `1,064 nm` NIR (and/or `647 nm` Raman) water-surface timing to resolve overlapping surface and bottom returns down to `0.2–0.5 m` depth across the white-ribbon transition. — *Threshold:* Deconvolved shallow depths (`0.2–1.0 m`) match wading RTK / submerged patch control within `< 0.15 m` `RMSE` with zero unexplained bimodal drop-out collar at the `1.0 m` transition. — *Evidence:* Shallow-Water Deconvolution Validation Histogram & Waveform Fit Plots. — *Ref:* [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md) §19.4, [Section 9.5](../../gemini4/book/ch-09/sec-09-05.md) §9.5.3.
- [ ] **[GATE]** **Wave-Surface Modeling (`0.27 delta z_s`) & Two-Index Vector Snell Refraction (`n_p` vs. `n_g`):** Derive instantaneous water-surface elevation $z_s(x,y,t)$ from `1,064 nm` / `647 nm` / `532 nm` surface returns (keeping residual depth error bounded by $\delta z_b \approx (1 - \frac{n_a\cos\theta_w}{n_g\cos\theta_a})\,\delta z_s \approx 0.27\,\delta z_s$); enforce **3D vector Snell ray bending using the phase refractive index $n_p \approx 1.3411\text{–}1.3420$** ($532\text{ nm}$ seawater; $1.3350$ freshwater) **AND compute submerged optical range using the group refractive index $n_g \approx 1.3638\text{–}1.3651$** ($1.3566$ freshwater) from campaign CTD $T/S$ profiles, explicitly verifying that $n_p$ is NOT reused for range (`+1.6–1.8 %` deep depth bias) and seawater $n_g$ is NOT misapplied to freshwater inflows (`-0.5 to -0.6 %` shallow depth bias, $\sim 10\text{–}12\text{ cm}$ at $20\text{ m}$). — *Threshold:* Verified linear regression slope between `(z_ALB - z_MBES)` and depth $d$ within `|slope| < 0.005 m/m`; CTD salinity-zone refractive-index table applied across estuaries. — *Evidence:* Refraction Physics Parameter Audit & Depth-Residual Slope Check. — *Ref:* [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md) §19.3–19.4, [Section 9.2](../../gemini4/book/ch-09/sec-09-02.md) §9.2.3, [Section 9.7](../../gemini4/book/ch-09/sec-09-07.md).
- [ ] **[REC]** **Turbidity Pulse-Stretch & Slope Footprint Correction:** Document and apply empirical or radiative-transfer correction for multiple-scattering path-length stretching in turbid waters ($K_d > 0.35\text{ m}^{-1}$) and steep-slope leading-edge shoal bias where the broadened benthic beam footprint ($D_{\text{benthic}} \approx 0.5\text{–}1.0\,d$) intersects canyon walls or dredge cuts. — *Threshold:* Residual deep-turbidity stretch bias bounded below `<= 0.05–0.10 m` where optical backscatter/Secchi calibration exists; uncorrected zones flagged in companion uncertainty grid. — *Evidence:* Turbidity/Slope Correction Note & Sensitivity Test Plot. — *Ref:* [Section 9.5](../../gemini4/book/ch-09/sec-09-05.md) §9.5.4–9.5.5, [Section 9.7](../../gemini4/book/ch-09/sec-09-07.md).

---

## 3. Classification, Compositing, Packaging & Release Gate

- [ ] **[GATE]** **LAS 1.4 Topo-Bathy Classification (Classes 40–45) & Void Integrity:** Classify point clouds strictly in **LAS 1.4 PDRF 6–10** using standard topographic codes (`2` Ground, `3–5` Veg, `7/18` Noise flagged `Withheld`, `17` Bridge Deck, `20` Ignored Ground) and ASPRS Topo-Bathy codes (`40` Bathymetric Point, `41` Water Surface, `42` Derived Water Surface, `43` Submerged Object, `44` IHO S-57 Object, `45` No Bottom Found At); strip pelagic fish, kelp canopies, and lutocline false shoals into noise/vegetation, **preserve Class 45 extinction shots**, and **never interpolate across surf-zone breaking-wave voids or optical extinction gaps**. — *Threshold:* Zero `Class 26` reserved bridge labels (`17` only); Class 45 retained verbatim; `0` synthetic TIN triangles spanning surf/extinction void polygons. — *Evidence:* LAS 1.4 Class Histogram (`pdal info` / `filters.stats`) & Void Boundary Polygon Mask. — *Ref:* [Chapter 30](../../fable/chapters/ch30-point-cloud-classification.md) §30.2, [Chapter 34](../../fable/chapters/ch34-water-in-dems.md) §34.8, [Chapter 35](../../fable/chapters/ch35-voids-and-overhangs.md).
- [ ] **[GATE]** **Cross-Modality White-Ribbon Land–Water Seam Stitching:** Stitch dry `1,064 nm` topo, ALB `532 nm` nearshore bathy, and concurrent MBES/USV bathymetry into a unified TBDEM across the [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md) overlap zone (`100–500 m`) using consistent VDatum/geoid grids and explicit Type Identifier (**TID**) / provenance source masks. — *Threshold:* Inter-modality seam step across stable sand `<= 0.05–0.10 m` `RMSE`; 100 % pixel coverage mapped in companion provenance/TID raster. — *Evidence:* Seam Difference Raster & Multimodal Provenance Mask. — *Ref:* [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md), [Chapter 48](../../fable/chapters/ch48-compositing.md) §48.6, [Section 24.1](../../gemini4/book/ch-24/sec-24-01.md).
- [ ] **[GATE]** **Deliverable Formats (`BAG`, `S-102`, `COG`), Sign Integrity, & Metadata:** Export **BAG FSD 2.0.1** (`+z ↑` elevation + uncertainty layer), **IHO S-102 Ed. 3.0.0** (`+d ↓` depth, verifying HDF5/GDAL `verticalCS = 6498` sign flip cleanly), and/or **PixelIsArea Cloud-Optimized GeoTIFF (COG)** TBDEM (ZSTD or controlled LERC compression) plus companion uncertainty, point-density, and void masks; populate **ISO 19115 / 19157** & **FGDC CSDGM Shoreline Profile** / **STAC** metadata. — *Threshold:* `gdalinfo` / `hdf5` inspection confirms `AREA_OR_POINT=Area`, declared WKT2 compound CRS, valid `verticalCS`, and zero NaN/nodata leakage (`-9999` / `1e6` unmasked); metadata schemas validate without error. — *Evidence:* Format Inspection Report (`gdalinfo` + `S-102`/`BAG` schema validator) & ISO/STAC XML/JSON Bundle. — *Ref:* [Chapter 47](../../fable/chapters/ch47-file-formats.md), [Chapter 49](../../fable/chapters/ch49-metadata.md), [Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md).
- [ ] **[COND]** **Security, Sanitization, & Privacy Release Screening:** (*Trigger:* ports/naval zones, indigenous/cultural sites, or residential shorelines) execute release review before public dissemination: verify critical coastal defense/port-infrastructure exemptions, indigenous **CARE/OCAP®** data sovereignty agreements, coastal residential curtilage optical masking, and `100 m` / coarse gridding rules where required by permit or defense authority. — *Threshold:* Signed release authorization confirming zero restricted port hydrography, unmasked curtilage PII, or embargoed cultural coordinates in public packages. — *Evidence:* Signed Security & CARE/OCAP® Release Clearance Memo. — *Ref:* [Chapter 69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md) §69.1, §69.5, [Section 27.2](../../gemini4/book/ch-27/sec-27-02.md).

---

## 4. Independent Accuracy Validation & Visual Forensics

- [ ] **[GATE]** **Inter-Swath, Cross-Line, and 3D Co-Registration Audit:** Verify cross-line vs. main-line differences across dry beach (`<= 0.05 m` `RMSE`) and flat seabed (`<= 0.10–0.15 m` `RMSE`), confirm zero residual 3D translation via **Nuth & Kääb (2011)** analytical co-registration ($\frac{\Delta z}{\tan\alpha} = a\cos\psi + b\sin\psi + c\cot\alpha$, `+z ↑` elevation with downslope clockwise-from-North aspect $\psi = \operatorname{atan2}(-\partial z/\partial x, -\partial z/\partial y)$), and enforce zero systematic swath-edge step (`[Chapter 56](../../fable/chapters/ch56-case-files.md) §56.23`). — *Threshold:* Estimated `(dx_east, dy_north)` horizontal shift `<= 0.10–0.15 m` over sloped terrain/beach bluffs; dry inter-swath `RMSD_z <= 0.08 m` (`<= 0.06 m` intra-swath). — *Evidence:* StripAlign / Nuth–Kääb Shift Diagnostic & Swath-Overlap Summary. — *Ref:* [Section 14.5](../../gemini4/book/ch-14/sec-14-05.md), [Chapter 56](../../fable/chapters/ch56-case-files.md) §56.23, [Section 14.3](../../gemini4/book/ch-14/sec-14-03.md).
- [ ] **[GATE]** **Stratified Withheld Checkpoints (`>= 30/stratum`) & Concurrent MBES / USV Cross-Check:** Validate against independent withheld checkpoints (`>= 30` per stratum: dry NVA, coastal marsh/vegetated VVA, shallow clear seabed `< 3 m`, deep/turbid seabed, and seagrass/rock hardground) AND against **concurrent MBES/USV** overlap (`100–500 m` white ribbon); report **mean bias, `1σ`, `RMSE` (including ASPRS Ed. 2 `RMSE_rep = hypot(RMSE_obs, sigma_cp)`), `95 % CI` ($\chi^2$), `NMAD`, `P95`**, variogram spatial correlation length $L$ ($N_{\text{eff}} \approx A / (\pi L^2)$), and pass rate against **IHO S-44 Order 1a / Special Order TVU & THU** and **USGS LBS QL1/QL2** thresholds in [template-error-budget.md](../_shared/template-error-budget.md). — *Threshold:* Stratified `n >= 30`; dry NVA `RMSE_V <= 0.10 m`; bathymetric `>= 95 %` points inside contract S-44 `TVU_max(d)` (confirming Order 1a closure and flagging any Special Order exceedance cleanly). — *Evidence:* Signed Stratified Accuracy & Concurrent MBES Reconciliation Report (`template-error-budget.md`). — *Ref:* [template-error-budget.md](../_shared/template-error-budget.md), [Chapter 52](../../fable/chapters/ch52-ground-truth.md), [Chapter 53](../../fable/chapters/ch53-accuracy-assessment.md).
- [ ] **[REC]** **ICESat-2 ATL03 / ATL24 Macro-Bias Check & Multi-Azimuth Hillshade Forensics:** Cross-check regional shallow-water bias against calm-sea **ICESat-2 ATL03/ATL24** profiles (recognizing `0.43–0.60 m` `RMSE` spaceborne photon noise), inspect **4+ azimuth multi-azimuth hillshades** and **2D FFT** spectra to trap scan-angle smiles, wave-aliasing corrugations, or VDatum discontinuities before client delivery. — *Threshold:* Zero unflagged directional scan-angle banding or periodic wave striping in `2D FFT` / 4-azimuth hillshades; regional macro-bias vs. ATL24 explained within photon noise. — *Evidence:* 4-Azimuth Hillshade Inspection Mosaic, 2D FFT Plot, & ATL24 Comparison Sheet. — *Ref:* [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md) §19.5, [Chapter 57](../../fable/chapters/ch57-visualizing-dems.md), [Section 14.3](../../gemini4/book/ch-14/sec-14-03.md).

---

## 5. Runnable Verification Snippets (PDAL + Python + VDatum/PROJ)

```bash
# 1. Valid two-index Snell refraction (filters.python) + Class 40-45 audit in PDAL,
#    plus explicit non-ballpark VDatum PROJ grid pipeline check (never bare ballpark cs2cs).
WORKDIR="$(mktemp -d)"

cat <<'PYEOF' > "${WORKDIR}/refract_two_index.py"
import numpy as np
N_A, N_P, N_G = 1.00028, 1.3415, 1.3645  # 532 nm seawater: air, phase (Snell), group (range)

def refract(ins, outs):
    cls = ins["Classification"]
    sa = np.deg2rad(np.abs(ins["ScanAngleRank"].astype(float)))
    z = ins["Z"].astype(float)
    zs = ins["WaterSurface"].astype(float)
    mask = (cls == 40) & (z < zs)
    s_air = (zs[mask] - z[mask]) / np.cos(sa[mask])
    th_w = np.arcsin((N_A / N_P) * np.sin(sa[mask]))   # Snell direction uses n_p
    s_w = s_air * (N_A / N_G)                          # Submerged range uses n_g
    z[mask] = zs[mask] - s_w * np.cos(th_w)
    dh = s_air * np.sin(sa[mask]) - s_w * np.sin(th_w)
    y = ins["Y"].astype(float)
    y[mask] -= np.sign(ins["ScanAngleRank"][mask]) * dh
    outs["Z"] = z
    outs["Y"] = y
    return True
PYEOF

cat <<EOF > "${WORKDIR}/alb_qa_pipeline.json"
{
  "pipeline": [
    "raw_unrefracted_submerged.laz",
    {
      "type": "filters.python",
      "script": "${WORKDIR}/refract_two_index.py",
      "module": "refract_two_index",
      "function": "refract"
    },
    {
      "type": "filters.stats",
      "dimensions": "Z,Classification",
      "enumerate": "Classification"
    },
    {
      "type": "writers.copc",
      "filename": "${WORKDIR}/qa_refracted_check.copc.laz",
      "forward": "all"
    }
  ]
}
EOF
pdal pipeline "${WORKDIR}/alb_qa_pipeline.json" --metadata "${WORKDIR}/alb_stats.json"

# Explicit non-ballpark NAVD88 -> MLLW depth (+d down) shift using a named NOAA VDatum grid (example grid name):
# (Or use NOAA vyperdatum; never accept silent ballpark transforms.)
# cct +proj=pipeline +step +proj=vgridshift +grids=us_noaa_g2018u0.tif \
#     +step +proj=vgridshift +grids=us_noaa_vdatum_navd88_to_mllw.tif +step +proj=axisswap +order=1,2,-3
```

```python
# 2. Hardened Python QA suite: two-index + freshwater check, pyproj ballpark guard,
#    S-44 TVU + ASPRS Ed. 2 quadrature + chi2 CI, and Nuth & Kaab (2011) co-registration.
import json, math
import numpy as np
from pyproj import Transformer
from scipy.stats import chi2

S44_LIMITS = {
    "Exclusive": (0.15, 0.0075),
    "Special": (0.25, 0.0075),
    "Order1a": (0.50, 0.013),
    "Order1b": (0.50, 0.013),
}

def assert_non_ballpark_crs(src_crs: str, dst_crs: str) -> None:
    """Reject silent ballpark fallbacks (e.g., missing VDatum SEP grid) before transforming."""
    tf = Transformer.from_crs(src_crs, dst_crs, always_xy=True, allow_ballpark=False)
    if tf.has_ballpark:
        raise ValueError(f"Ballpark vertical/horizontal transform detected: {src_crs} -> {dst_crs}")

def audit_n_p_vs_n_g(depths_m: np.ndarray, theta_a_deg: float = 20.0,
                     n_a: float = 1.00028, n_p: float = 1.3415,
                     n_g: float = 1.3645, n_g_fresh: float = 1.3566) -> dict:
    """Quantify +1.6-1.8 % single-index bias and -0.58 % seawater-in-freshwater bias."""
    theta_a = math.radians(theta_a_deg)
    sin_w = (n_a / n_p) * math.sin(theta_a)
    cos_w = math.sqrt(1.0 - sin_w ** 2)
    single_idx_bias_m = depths_m * ((n_g / n_p) - 1.0)
    freshwater_bias_m = depths_m * ((n_g_fresh / n_g) - 1.0)
    return {
        "cos_theta_w": round(cos_w, 5),
        "wave_factor_1_minus_na_cosw_over_ng_cosa": round(
            1.0 - (n_a * cos_w) / (n_g * math.cos(theta_a)), 4
        ),
        "max_single_index_deep_bias_m": round(float(np.max(single_idx_bias_m)), 4),
        "single_index_pct": round(((n_g / n_p) - 1.0) * 100.0, 3),
        "max_seawater_in_freshwater_bias_m": round(float(np.min(freshwater_bias_m)), 4),
        "freshwater_pct": round(((n_g_fresh / n_g) - 1.0) * 100.0, 3),
    }

def validate_bathy_residuals(dz_m: np.ndarray, depths_m: np.ndarray,
                             order: str = "Order1a", sigma_cp_m: float = 0.03) -> dict:
    """dz_m = z_alb - z_ref (+z up). Reports S-44 TVU pass rate, ASPRS Ed. 2 RMSE_rep, & chi2 95% CIs."""
    if order not in S44_LIMITS:
        raise ValueError(f"Unknown S-44 order '{order}'; expected one of {list(S44_LIMITS)}")
    mask = np.isfinite(dz_m) & np.isfinite(depths_m)
    dz, dp = dz_m[mask], depths_m[mask]
    n = int(dz.size)
    if n < 2:
        raise ValueError(f"Need >= 2 finite residuals after NaN filtering, got {n}")
    a, b = S44_LIMITS[order]
    tvu_95 = np.sqrt(a ** 2 + (b * dp) ** 2)
    pass_rate = float(np.mean(np.abs(dz) <= tvu_95)) * 100.0
    rmse = float(np.sqrt(np.mean(dz ** 2)))
    rmse_reported = math.hypot(rmse, sigma_cp_m)
    sigma = float(np.std(dz, ddof=1))
    nmad = float(1.4826 * np.median(np.abs(dz - np.median(dz))))
    p95 = float(np.percentile(np.abs(dz), 95))
    sigma_ci = (sigma * math.sqrt((n - 1) / chi2.ppf(0.975, n - 1)),
                sigma * math.sqrt((n - 1) / chi2.ppf(0.025, n - 1)))
    rmse_ci = (rmse * math.sqrt(n / chi2.ppf(0.975, n)),
               rmse * math.sqrt(n / chi2.ppf(0.025, n)))
    return {
        "n": n, "bias_m": round(float(np.mean(dz)), 4),
        "sigma_m": round(sigma, 4), "rmse_obs_m": round(rmse, 4),
        "rmse_reported_asprs_m": round(rmse_reported, 4),
        "sigma_95ci_df_n1_m": tuple(round(x, 4) for x in sigma_ci),
        "rmse_95ci_df_n_m": tuple(round(x, 4) for x in rmse_ci),
        "nmad_m": round(nmad, 4), "p95_m": round(p95, 4),
        f"s44_{order}_pass_pct": round(pass_rate, 2),
    }

def nuth_kaab_shift(dz_m: np.ndarray, slope_rad: np.ndarray,
                    aspect_cw_north_rad: np.ndarray) -> tuple[float, float, float]:
    """Solve Nuth & Kaab (2011): dz / tan(alpha) = a*cos(psi) + b*sin(psi) + c*cot(alpha) (+z up)."""
    mask = np.isfinite(dz_m) & np.isfinite(slope_rad) & (slope_rad > math.radians(3.0))
    tana = np.tan(slope_rad[mask])
    y = dz_m[mask] / tana
    A = np.column_stack([np.cos(aspect_cw_north_rad[mask]),
                         np.sin(aspect_cw_north_rad[mask]),
                         1.0 / tana])
    c_north, c_east, c_vert = np.linalg.lstsq(A, y, rcond=None)[0]
    return float(c_east), float(c_north), float(c_vert)

if __name__ == "__main__":
    rng = np.random.default_rng(42)
    d = np.linspace(1.0, 20.0, 60)
    dz = rng.normal(loc=0.015, scale=0.11, size=60)
    print("Two-index check:", json.dumps(audit_n_p_vs_n_g(d)))
    print("Residual audit:", json.dumps(validate_bathy_residuals(dz, d, "Order1a", 0.03)))
    asp = rng.uniform(0, 2 * math.pi, 200)
    slp = rng.uniform(0.10, 0.35, 200)
    syn_dz = (0.12 * np.sin(asp) + 0.08 * np.cos(asp)) * np.tan(slp) - 0.02
    print("Nuth-Kaab shift (dE, dN, dZ):", [round(v, 4) for v in nuth_kaab_shift(syn_dz, slp, asp)])
```

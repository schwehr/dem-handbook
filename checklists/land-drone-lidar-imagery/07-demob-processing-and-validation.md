# On-Land Drone (UAS) LiDAR + Imagery — Demob, Processing & Validation

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `land-drone-lidar-imagery` | **Platform / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

---

## 1. Field Demobilization, Battery Storage & Custody Gate

- [ ] **[GATE]** **Control Retrieval, Post-Occupation Base Check & Site Sweep:** Measure and photograph closing vertical + slant base antenna heights, log `>= 10 min` post-flight static overlap before shutting down base RINEX, recover `100 %` of targets/stakes/flagging, and secure landowner checkout sign-off. — *Evidence:* Closing ARP photo, complete target-recovery count, and signed landowner checkout. | *Ref:* [Ch. 25](../../fable/chapters/ch25-calibration-infrastructure.md).
- [ ] **[GATE]** **LiPo Battery Storage Discharge & Air-Freight SoC Prep:** Within `24–48 hr` of final flight, discharge all packs to **`~3.80–3.85 V/cell`** (`~35–45 %` SoC) for dry `< 25 °C` cabinet storage. Before **any** air shipment (`UN 3480` PI 965 / `UN 3481` PI 966, IATA DGR 67th Ed. eff. Jan 1, 2026), strictly discharge to **`<= 30 %` SoC** (`~3.72–3.78 V/cell`) and record cycle counts in [09 Template A](09-resources-and-templates.md). — *Evidence:* Final pack storage/shipping SoC log signed by Flight Lead. | *Ref:* [02-permits-safety-insurance-cost.md](02-permits-safety-insurance-cost.md), [09 Template A](09-resources-and-templates.md).
- [ ] **[GATE]** **Final Raw Data Custody Gate BEFORE Departing Site:** Confirm zero missing files across `SSD_A` and `SSD_B` via `sha256sum -c manifest.sha256`, verify strict separation of `gcps.csv` vs. `cps_withheld.csv`, close active LAANC/COA advisories, and confirm offsite upload hash. — *Evidence:* Passing dual-SSD `sha256sum` receipt initialed by Field Lead & Verifier. | *Ref:* [Appendix G §G.3–G.5](../../fable/appendices/appendix-g-checklists.md), [Ch. 47](../../fable/chapters/ch47-file-formats.md).
- [ ] **[GATE]** **Reproducible Software & Geodetic Grid Lock:** Pin exact `PDAL`/`OpenDroneMap`/`COLMAP`/`RTKLIB`/`PROJ` container digests, `igs20.atx` ANTEX file, and vertical geoid (`GEOID18` / `EGM2008` / VDatum) SHA-256 checksums before generating client deliverables. — *Evidence:* Pinned `environment.lock` + `geoid_hashes.txt` stored alongside deliverables. | *Ref:* [Ch. 47](../../fable/chapters/ch47-file-formats.md).

---

## 2. Trajectory, LiDAR Strip Adjustment & SfM Processing

- [ ] **[GATE]** **Bidirectional PPK + IMU Figure-8 RTS Solution:** Solve final base position (`NGS OPUS Static` / `CSRS-PPP` verified `<= 1–2 cm` against published control) and run tightly-coupled forward/backward RTS smoother (`POSPac` / `Inertial Explorer` / `RTKLIB`) using pre/post figure-8 yaw alignment and verified `FRD/NED -> ENU` lever arms. Require `>= 98 %` fixed ambiguities on lines and forward-backward separation `< 2–3 cm` (`1σ`). — *Evidence:* Trajectory RMS & F/B separation summary plot archived with solution files. | *Ref:* [Ch. 12](../../fable/chapters/ch12-gnss.md), [Ch. 13](../../fable/chapters/ch13-imu-ins.md).
- [ ] **[GATE]** **UAS LiDAR Strip Adjustment, ELM/SOR (`Withheld = 1`) & DTM Classification:** Run orthogonal cross-strip adjustment (`TerraMatch` / `StripAlign` / `PDAL ICP`) until open flat inter-swath residuals fall **`<= 3–5 cm` `RMSDz`** (`<= 8 cm` USGS LBS ceiling). Apply `filters.elm` + `filters.outlier` (`SOR`), setting **LAS Class 7/18 AND `Withheld = 1`** (preserving raw returns); tune `SMRF`/`CSF`/PTIN ground slopes so bridge decks stay **Class 17** (never Class 2), mask transients (`withheld`), and export `interp_mask.tif`. — *Evidence:* Strip-residual table (`RMSDz`), PDAL pipeline JSON, and `interp_mask.tif` void overlay. | *Ref:* [Ch. 18](../../fable/chapters/ch18-topographic-lidar.md), [Ch. 27](../../fable/chapters/ch27-moving-and-transient-objects.md), [Ch. 30](../../fable/chapters/ch30-point-cloud-classification.md), [Ch. 32](../../fable/chapters/ch32-dsm-to-dtm.md).
- [ ] **[GATE]** **SfM Bundle Adjustment, Rolling Shutter (`--rolling-shutter`) & NDWI Water-Glint Masking:** Anchor SfM (`OpenDroneMap` / `COLMAP` / `Metashape` / `Pix4D`) with PPK camera centers (`2–3 cm` `1σ` weights), `10–20°` oblique cross-grids (or locked pre-calibrated IO via `--use-fixed-camera-params`), convex-hull `gcps.csv`, and **`--rolling-shutter` linear optimization `[COND]`** (*Trigger:* rolling-shutter sensor flown). Apply **NDWI (`(Green - NIR)/(Green + NIR) > 0.1–0.3`)** or water masks prior to dense MVS matching so wave glint does not fabricate `+0.5–1.5 m` false bars, and hydro-flatten lakes (`>= 0.81 ha` / `2 acres`) and rivers (`>= 30.5 m` / `100 ft`). — *Evidence:* SfM calibration residual report + applied water/transient mask polygons. | *Ref:* [Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md), [Ch. 34](../../fable/chapters/ch34-water-in-dems.md), [`gemini4` §8.2](../../gemini4/book/ch-08/sec-08-02.md).

### Runnable Processing Snippets (`PDAL` + `OpenDroneMap` + `COLMAP`)

```bash
# A. PDAL pipeline: Merge strips -> ELM + SOR -> Class 7/18 + Withheld=1 -> SMRF Ground -> COPC
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT
pdal merge raw_adjusted_*.laz "$WORKDIR/merged_adjusted.laz"
cat << EOF > "$WORKDIR/uas_lidar_clean.json"
[
  "$WORKDIR/merged_adjusted.laz",
  { "type": "filters.elm", "cell": 5.0, "threshold": 1.0, "class": 7 },
  { "type": "filters.outlier", "method": "statistical", "mean_k": 12, "multiplier": 2.2, "class": 18,
    "where": "Classification != 7" },
  { "type": "filters.assign", "value": "Withheld = 1 WHERE Classification == 7 || Classification == 18" },
  { "type": "filters.smrf", "slope": 0.25, "window": 16.0, "threshold": 0.45, "scalar": 1.25,
    "ignore": "Classification[7:7],Classification[18:18]" },
  { "type": "writers.copc", "filename": "deliverable_cloud.copc.laz",
    "scale_x": 0.001, "scale_y": 0.001, "scale_z": 0.001,
    "offset_x": "auto", "offset_y": "auto", "offset_z": "auto" }
]
EOF
pdal pipeline "$WORKDIR/uas_lidar_clean.json"

# B1. OpenDroneMap (CLI) — PPK SfM with oblique cross-grid self-calibration (--dem-resolution in cm/px!)
docker run --rm -v "$PWD":/datasets opendronemap/odm --project-path /datasets uas_project \
  --gcp /datasets/uas_project/gcps_only.txt --rolling-shutter --dtm --dsm --cog \
  --dem-resolution 5 --pc-quality high

# B2. OpenDroneMap (CLI) — Pre-calibrated locked IO variant (disables self-calibration!)
# docker run --rm -v "$PWD":/datasets opendronemap/odm --project-path /datasets uas_project \
#   --gcp /datasets/uas_project/gcps_only.txt --cameras /datasets/uas_project/cameras_precal.json \
#   --use-fixed-camera-params --rolling-shutter --dtm --dsm --cog --dem-resolution 5

# C. COLMAP headless check — lock pre-calibrated intrinsics before dense stereo
colmap bundle_adjuster --input_path sparse/0 --output_path sparse/ba \
  --BundleAdjustment.refine_focal_length 0 --BundleAdjustment.refine_extra_params 0
```

---

## 3. ASPRS Ed. 2 Withheld Checkpoint Validation & Delivery Packaging

- [ ] **[GATE]** **ASPRS Ed. 2 Quadrature Validation + Nuth & Kääb (2011) 3D Check:** Interpolate the final DEM at all `>= 30` NVA + `>= 30` VVA withheld checkpoints (`cps_withheld.csv`) via **bilinear or TIN interpolation** honoring `AREA_OR_POINT` (`0.5 px` corner offset for `PixelIsArea`), never nearest-cell lookup. Propagate checkpoint survey uncertainty ($\sigma_{\text{cp}}$) in quadrature and verify zero lateral co-registration bias via **Nuth & Kääb (2011)** ($\frac{\Delta z}{\tan\alpha} = a\cos(b - \psi) + \frac{c}{\tan\alpha}$, `+z ↑`, downslope aspect $\psi$):
  $$\text{RMSE}_{\text{rep}} = \sqrt{\text{RMSE}_{\text{test}}^2 + \text{RMSE}_{\text{cp}}^2}, \qquad \text{NMAD} = 1.4826 \cdot \text{median}\left|\varepsilon_i - \text{median}(\varepsilon)\right|$$
  Report `RMSE_V`, `RMSE_H`, `RMSE_3D`, mean bias, `s`, `NMAD`, `P95`, edge vs. interior dome `R²`, and `|ε_i| > 3 × NMAD` outliers transparently. — *Evidence:* Printed Python QC report + Nuth–Kääb shift vector (`dx, dy, dz`). | *Ref:* [Ch. 53](../../fable/chapters/ch53-accuracy-assessment.md), [`gemini4` §14.2](../../gemini4/book/ch-14/sec-14-02.md), [`gemini4` §14.5](../../gemini4/book/ch-14/sec-14-05.md).
- [ ] **[COND]** **White-Ribbon Intertidal / Multi-Modal Edge Sync:** *Trigger:* Coastal/riparian AOI abuts concurrent ASV, bathylidar, or UNOLS bathymetry. Cross-check `100–500 m` shoreline overlap bands over shared VDatum/SEP (`<= 10–15 cm` mean offset). — *Evidence:* Intertidal seam overlap histogram & mean offset check. | *Ref:* [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md).
- [ ] **[REC]** **2D FFT Strip-Frequency & Fractional Elevation Histogram Forensics:** Run `2D FFT/PSD` spectral diagnostics on shaded relief to rule out flight-line striping and inspect fractional elevation histograms ($z \bmod 1\text{ m}$) for integer/float32 rounding defects. — *Evidence:* Spectral PSD plot & fractional-z histogram PNG. | *Ref:* [Ch. 54](../../fable/chapters/ch54-evaluating-others-data.md), [`gemini4` §14.3](../../gemini4/book/ch-14/sec-14-03.md).
- [ ] **[REC]** **`Tested to Meet` vs. `Produced to Meet` ASPRS Ed. 2 Honest Disclosure:** State **`"Tested to meet"`** strictly for strata holding `>= 30`–`120` independent withheld CPs meeting `RMSE_rep`; label unverified closed-canopy gaps or interpolated zones honestly as **`"Produced to meet"`**. — *Evidence:* Statement verbatim in accuracy report & STAC metadata. | *Ref:* [Ch. 53](../../fable/chapters/ch53-accuracy-assessment.md), [Ch. 70](../../fable/chapters/ch70-specifications-guided-tour.md).
- [ ] **[COND]** **Privacy PII & Protected Cultural Redaction Before Release:** *Trigger:* Public or third-party distribution of orthomosaics/point clouds. Blur faces/license plates (`GDPR`) and mask/withhold protected archaeological features (`NHPA § 106` / `ARPA` / `CARE-OCAP®`). — *Evidence:* Redaction QA log verifying masked areas before archive push. | *Ref:* [Ch. 68](../../fable/chapters/ch68-legal-issues.md), [Ch. 69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md), [`gemini4` §27.2](../../gemini4/book/ch-27/sec-27-02.md).
- [ ] **[REC]** **Airspace / Landowner Final Closeout Notice:** Cancel remaining LAANC/COA advisories, confirm NOTAM closure, and send written completion notice to landowner contacts. — *Evidence:* Cancellation confirmations & landowner closeout email archived. | *Ref:* [Appendix G §G.9](../../fable/appendices/appendix-g-checklists.md).
- [ ] **[GATE]** **COG / COPC / LAS 1.4 / STAC Format & Metadata Audit:** Deliver **LAS 1.4 / COPC 1.0 (`PDRF 6–10`, adjusted GPS time)** and **COG 1.0 (`ZSTD`, `PREDICTOR=3`, `GTRasterTypeGeoKey = PixelIsArea`)** using `float64` or millimeter-scaled coordinates (avoiding `float32` UTM northing `0.5 m` rounding traps), paired with `interp_mask.tif`, **STAC 1.1.0**, and ISO 19115/19157 lineage; sign Gate **G-07** in [00-README-and-signoff.md](00-README-and-signoff.md). — *Evidence:* Passing `gdalinfo` / `copc` validation logs & signed G-07 row. | *Ref:* [Ch. 47](../../fable/chapters/ch47-file-formats.md), [`gemini4` §19.1](../../gemini4/book/ch-19/sec-19-01.md).

### Runnable Python QC Snippet (ASPRS Ed. 2 Quadrature + Edge Dome + Nuth & Kääb Check)

```python
import numpy as np, rasterio
from scipy import ndimage, stats

# 1. Withheld CP validation using 09 Template C2 named CSV headers
cps = np.atleast_1d(
    np.genfromtxt("cps_withheld.csv", delimiter=",", names=True, dtype=None, encoding="utf-8")
)
xs, ys = cps["Easting_m"].astype(float), cps["Northing_m"].astype(float)
zs_cp, sig_v = cps["Ortho_Elev_m"].astype(float), cps["Sigma_V_m"].astype(float)

with rasterio.open("deliverable_dtm_cog.tif") as src:
    dem = src.read(1, masked=True).filled(np.nan)
    px_shift = 0.5 if src.tags().get("AREA_OR_POINT", "Area") == "Area" else 0.0
    col_f, row_f = ~src.transform * (xs, ys)
    zs_dem = ndimage.map_coordinates(
        dem, [row_f - px_shift, col_f - px_shift], order=1, mode="constant", cval=np.nan
    )

err_raw = zs_dem - zs_cp
valid = np.isfinite(err_raw) & np.isfinite(sig_v)
if valid.sum() < 3:
    raise ValueError(f"Only {valid.sum()} finite checkpoints inside DEM coverage (< 3)")
err = err_raw[valid]
rmse_test = float(np.sqrt(np.mean(err**2)))
rmse_cp = float(np.sqrt(np.mean(sig_v[valid]**2)))
rmse_rep = float(np.hypot(rmse_test, rmse_cp))  # ASPRS Ed. 2 quadrature inclusion
nmad = float(1.4826 * np.median(np.abs(err - np.median(err))))
r2 = (xs[valid] - xs[valid].mean())**2 + (ys[valid] - ys[valid].mean())**2
_, _, r_val, p_val, _ = stats.linregress(r2, err)
print(f"n={valid.sum()}, bias={err.mean():+.4f}m, RMSE_test={rmse_test:.4f}m, "
      f"RMSE_rep={rmse_rep:.4f}m, NMAD={nmad:.4f}m, Dome_R2={r_val**2:.3f} (p={p_val:.3g})")

# 2. Closed-form Nuth & Kaab (2011) vs. reference DEM (north-up grid; or use xdem.coreg.NuthKaab)
def nuth_kaab_shift(z_uas: np.ndarray, z_ref: np.ndarray, dx_m: float, dy_m: float, min_slope_deg: float = 5.0):
    dz_dy_down, dz_dx = np.gradient(z_ref, dy_m, dx_m)  # row increases southward -> dz/dy = -dz_dy_down
    dz_dy = -dz_dy_down
    tan_a = np.hypot(dz_dx, dz_dy)
    psi = np.arctan2(-dz_dx, -dz_dy)  # downslope aspect clockwise from North (+z up)
    dh = z_uas - z_ref
    m = np.isfinite(dh) & np.isfinite(tan_a) & (tan_a > np.tan(np.deg2rad(min_slope_deg)))
    if m.sum() < 10:
        raise ValueError("Insufficient sloped pixels (>= 10 required) for Nuth-Kaab fit")
    med = np.median(dh[m])
    nmad_nk = 1.4826 * np.median(np.abs(dh[m] - med))
    m &= np.abs(dh - med) <= 3.0 * max(nmad_nk, 1e-4)
    A = np.column_stack([np.sin(psi[m]), np.cos(psi[m]), 1.0 / tan_a[m]])
    dx_hat, dy_hat, dz_hat = np.linalg.lstsq(A, dh[m] / tan_a[m], rcond=None)[0]
    return float(dx_hat), float(dy_hat), float(dz_hat)
```

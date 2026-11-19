# Land Aircraft LiDAR & Imagery — Demobilization, Processing & Validation

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `land-aircraft-lidar-imagery` | **Platform / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[x] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

---

## 1. Pre-Demobilization Closure, Custody & Airframe Closeout

- [ ] **[GATE]** Fly a **post-project boresight closure flight** over the gable-roof + flat calibration range **BEFORE aircraft demobilization or sensor unmounting**, confirming angular stability (`|Δω|, |Δφ|, |Δκ| <= 0.002°–0.003°` vs. pre-survey calibration) and checking optical port glass for zero coating/thermal shift. *Evidence:* Signed pre- vs. post-project boresight closure table. *Refs:* [ch25-calibration-infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md), [ch-13/sec-13-01](../../gemini4/book/ch-13/sec-13-01.md), [ch-13/sec-13-05](../../gemini4/book/ch-13/sec-13-05.md).
- [ ] **[GATE]** Clear the **100 % Raw Data & Calibration Custody Gate BEFORE releasing aircraft or field crews**: verify complete `SHA-256`-hashed `3-2-1` archival of all raw LiDAR/waveform files, metric imagery, `IMU` + `GNSS` + `AGC`/`C/N0` telemetry, base `RINEX` + `ANTEX` + dual antenna-height sheets + collar photos, port glass certs, and pre/post boresight reports. *Evidence:* Signed `SHA-256` custody receipt verifying `0` missing sorties or base sessions. *Refs:* [ch50-archiving-and-provenance](../../fable/chapters/ch50-archiving-and-provenance.md), [ch-19/sec-19-01](../../gemini4/book/ch-19/sec-19-01.md).
- [ ] **[GATE]** Complete **sensor de-integration, joint off-hire condition sign-off, and airframe `W&B` restoration**: reinstall original hatch/blanking plate per **STC / Form 337**, update Aircraft Equipment List & `W&B`, inspect helicopter hardpoints/isolators, and sign airframe logbook return-to-service. *Evidence:* Joint off-hire inspection log, A&P logbook photo, and restored W&B sheet. *Refs:* [ch-07/sec-07-03](../../gemini4/book/ch-07/sec-07-03.md), [ch16-platforms](../../fable/chapters/ch16-platforms.md).
- [ ] **[GATE]** Formally **cancel and close out project `NOTAM`s, `FAA Form 7140-1` / `LCH` laser clearances, temporary base-station ground permits, and ATA Carnet filings**, **retrieve all temporary GNSS base tripods, survey targets, and temporary marks**, and package spare Li-ion/Li-metal cells strictly under **`IATA DGR 67th Ed. (Jan 2026) <= 30 % SoC` (`UN 3480 PI 965`, `UN 3481 PI 966`) and `UN 3090/3091`** return shipping rules. *Evidence:* Timestamped NOTAM/LCH closeout receipts, base-retrieval checklist, and hazmat return manifest. *Refs:* [ch68-legal-issues](../../fable/chapters/ch68-legal-issues.md), [09 External Register](09-resources-and-templates.md#13-external-statutory-safety-hazmat--insurance-register).

---

## 2. Deterministic Processing, Strip Adjustment & Classification

- [ ] **[GATE]** Execute processing inside a **version-pinned reproducible environment** (manifest pinning binaries, `PROJ` `GEOID18`/`SGEOID2022` grids, `GPST - UTC = 18 s` offset, atmospheric `n_g`, and optical-window `Δr_win(θ)`): compute tightly coupled **RTS forward–backward `SBET` + `SMRMSG`**, run rigorous **Skáloud–Lichti / Glira strip adjustment**, report pre- vs. post-adjustment `RMSD_z` (`<= 0.08 m` QL1/QL2, `<= 0.04 m` QL0), and verify unconstrained trajectory splines did not absorb real terrain slope. *Evidence:* Pinned environment manifest + strip-adjustment residual diagnostics. *Refs:* [ch13-imu-ins](../../fable/chapters/ch13-imu-ins.md), [ch25-calibration-infrastructure](../../fable/chapters/ch25-calibration-infrastructure.md), [ch29-processing-pipelines](../../fable/chapters/ch29-processing-pipelines.md).
- [ ] **[GATE]** Perform **ASPRS LAS 1.4 R15 / USGS LBS 2024/2025 rev. A classification**: flag low/high noise (`Class 7`/`Class 18` + **`withheld` bit**; **never delete returns**; keep **`overlap` bit separate from `withheld`**), ensure `0` `Class 0` unclassified points remain, separate **Class 2** bare earth, **Class 17** bridges (distinct from open culverts), **Class 20** ignored ground within hydro breakline buffers (`LBS 2025 rev. A`), **Class 21** perennial snowpack, and **Class 13–16** wires/towers if scoped; evaluate **stratified Type I/II confusion matrices** against project SOW limits with an immutable manual-edit log. *Evidence:* Tile classification summary + confusion matrix + manual edit-log file. *Refs:* [ch30-point-cloud-classification](../../fable/chapters/ch30-point-cloud-classification.md), [ch32-dsm-to-dtm](../../fable/chapters/ch32-dsm-to-dtm.md), [ch33-wires-and-thin-structures](../../fable/chapters/ch33-wires-and-thin-structures.md).
- [ ] **[GATE]** Execute **hydro-flattening and standards-compliant DEM packaging**: flatten lakes `>= 0.81 ha` (`2 acres`, `~8,094 m²`) and rivers `>= 30 m` nominal width monotonically downstream (`USGS LBS`); enforce **`RasterPixelIsArea` (`AREA_OR_POINT=Area`)** to eliminate `0.5 Δx` shift traps; write **`Float32` `COG` (`ZSTD`, `PREDICTOR=3`, never `Int16` quantized meters)** and **`LAZ 1.4` (`PDRF 6–10`, `0.001 m` scale, `Float64` coordinates) / `COPC 1.0`**. *Evidence:* `gdalinfo` / `pdal info` validation proving `AREA_OR_POINT=Area`, `Float32`, `ZSTD`, and monotonic stream profiles. *Refs:* [ch31-interpolation-and-gridding](../../fable/chapters/ch31-interpolation-and-gridding.md), [ch-15/sec-15-03](../../gemini4/book/ch-15/sec-15-03.md), [ch-24/sec-24-01](../../gemini4/book/ch-24/sec-24-01.md).
- [ ] **[GATE]** Package **`STAC` catalog + `ISO 19115`/`19157` lineage metadata** (embedding data license & embargo terms) and execute final **privacy / critical-infrastructure / archaeological (`NHPA § 106` / `ARPA` / `CARE & OCAP®`) release screening** prior to publishing public cloud buckets. *Evidence:* Passed `STAC` schema validation log and signed release-review clearance. *Refs:* [ch49-metadata](../../fable/chapters/ch49-metadata.md), [ch69-security-sovereignty-privacy-ethics](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md).

---

## 3. Independent Accuracy Validation & Forensic Audit

- [ ] **[GATE]** Execute **ASPRS Edition 2 v2 (June 2024) / USGS LBS 2024+ rev. A** validation on strictly withheld `>= 30` checkpoints per stratum using **`PixelIsArea` bilinear / TIN interpolation** (never nearest pixel): **add checkpoint survey uncertainty `σ_cp` in quadrature** ($\mathrm{RMSE}_{\text{rep}} = \sqrt{\mathrm{RMSE}_{\text{test}}^2 + \sigma_{\text{cp}}^2}$; never subtract `σ_cp` from reported compliance accuracy), test non-vegetated **`RMSE_V` (`NVA`)** against QL limits (`<= 0.05/0.10/0.20 m`), report **`RMSE_H` / `RMSE_3D`** where scoped, report vegetated **`VVA` (`RMSE_V` + empirical `95th` percentile absolute error as observed — not pass/fail)**, disclose **Tested-to-Meet vs. Produced-to-Meet**, and log every `3 × NMAD` outlier inspection without silent deletion. *Evidence:* PLS/CP-signed Accuracy Report conforming to [ch53-accuracy-assessment](../../fable/chapters/ch53-accuracy-assessment.md) 10-item checklist. *Refs:* [ch52-ground-truth](../../fable/chapters/ch52-ground-truth.md), [ch53-accuracy-assessment](../../fable/chapters/ch53-accuracy-assessment.md), [ch70-specifications-guided-tour](../../fable/chapters/ch70-specifications-guided-tour.md).
- [ ] **[GATE]** Run **2D FFT PSD, multi-azimuth hillshade, and `nDSM` structural sanity checks** (`ch-14/sec-14-03`, `ch32-dsm-to-dtm`) across delivered rasters to verify zero residual flight-line striping, zero `corduroy` mirror lag, zero void-fill over-smoothing, and zero `nDSM < -0.10 m` ground classification blunders. *Evidence:* Archived FFT spectrum plot, hillshade gallery, and `nDSM` negative-pixel histogram. *Refs:* [ch-14/sec-14-03](../../gemini4/book/ch-14/sec-14-03.md), [ch32-dsm-to-dtm](../../fable/chapters/ch32-dsm-to-dtm.md).
- [ ] **[GATE]** Cross-validate regional elevation integrity using **filtered `ICESat-2 ATL08`/`ATL06`** (flat bare terrain `< 5°`, strong beams), **Nuth & Kääb (2011) 3D co-registration** ($\Delta z/\tan\alpha = a\cos\psi + b\sin\psi + c\cot\alpha$, downslope $\psi$ in `+z ↑`), and **adjacent-tile / [multimodal-white-ribbon](../_shared/multimodal-white-ribbon.md) seam continuity (`<= 0.05–0.10 m` step)** to catch undetected regional lifts (`11–14 cm` western step, Case `56.23`). *Evidence:* `ICESat-2` bias summary, Nuth–Kääb vector fit, and inter-tile/coastal seam difference raster. *Refs:* [ch-14/sec-14-05](../../gemini4/book/ch-14/sec-14-05.md), [ch56-case-files](../../fable/chapters/ch56-case-files.md), [ch54-evaluating-others-data](../../fable/chapters/ch54-evaluating-others-data.md).
- [ ] **[COND]** For bundled metric imagery / `SGM` deliveries, verify `GCP`/`CP` independence (`sigma_0 <= 0.5 px`), test `SGM` vs. LiDAR ground surfaces across flat zones for **zero quadratic doming** (`<= 0.05 m`), and check true-ortho building lean and seamline radiometric feathering. *Trigger:* Any project delivering metric orthoimagery or `SGM` photogrammetric surfaces. *Evidence:* Quadratic dome-test residual output and ortho seamline QA check. *Refs:* [ch22-photogrammetry-sfm](../../fable/chapters/ch22-photogrammetry-sfm.md), [ch-08/sec-08-01](../../gemini4/book/ch-08/sec-08-01.md).
- [ ] **[REC]** Verify `COG` and `COPC` cloud streaming compliance (`rio cogeo validate`, `gdalinfo -stats`, `pdal info --metadata`) and verify immutable object-lock retention before archival sign-off. *Evidence:* Zero-error validation stdout log. *Refs:* [ch47-file-formats](../../fable/chapters/ch47-file-formats.md), [ch-19/sec-19-01](../../gemini4/book/ch-19/sec-19-01.md).

### Runnable Deliverable Verification, CP Validation & Nuth–Kääb Check (`Python`)

```python
import numpy as np
from scipy.ndimage import map_coordinates

def fft_striping_ratio(arr: np.ndarray) -> float:
    """Centered 2D Hann-windowed FFT peak/median PSD ratio with dynamic DC masking."""
    h, w = arr.shape
    m = min(512, h, w)
    if m < 16:
        raise ValueError(f"Raster shape {arr.shape} too small for 2D FFT audit")
    r0, c0 = (h - m) // 2, (w - m) // 2
    patch = arr[r0:r0 + m, c0:c0 + m]
    if not np.isfinite(patch).all():
        raise ValueError("Centered patch contains nodata/NaN; supply interior valid tile")
    win = np.outer(np.hanning(m), np.hanning(m))
    psd = np.abs(np.fft.fftshift(np.fft.fft2((patch - np.mean(patch)) * win))) ** 2
    cy, cx = m // 2, m // 2
    psd[max(0, cy - 4):cy + 5, max(0, cx - 4):cx + 5] = 0.0
    pos = psd[psd > 0]
    if pos.size == 0:
        raise ValueError("Zero positive spectral power after DC masking")
    return float(np.max(psd) / np.median(pos))

def validate_cps_pixel_is_area(dem, x0, y0, res, xs, ys, zs_cp, sigma_cp):
    """Bilinear CP validation in RasterPixelIsArea (+z up) with ASPRS Ed. 2 quadrature sum."""
    cols_c = (np.asarray(xs) - x0) / res - 0.5
    rows_c = (y0 - np.asarray(ys)) / res - 0.5
    z_dem = map_coordinates(dem, [rows_c, cols_c], order=1, mode="constant", cval=np.nan)
    valid = np.isfinite(z_dem) & np.isfinite(zs_cp)
    if int(valid.sum()) < 2:
        raise ValueError("Fewer than 2 valid checkpoints inside raster bounds")
    err = z_dem[valid] - np.asarray(zs_cp)[valid]
    med = float(np.median(err))
    nmad = float(1.4826 * np.median(np.abs(err - med)))
    rmse_test = float(np.sqrt(np.mean(err**2)))
    rmse_rep = float(np.hypot(rmse_test, sigma_cp))  # ASPRS Ed. 2 adds sigma_cp in quadrature
    outliers = np.where(np.abs(err - med) > 3.0 * nmad)[0] if nmad > 0 else np.array([], dtype=int)
    return float(np.mean(err)), rmse_test, rmse_rep, nmad, outliers

def nuth_kaab_shift(z_test: np.ndarray, z_ref: np.ndarray, res_m: float, north_up: bool = True):
    """Estimate (dx_east, dy_north, dz_bias) of z_test vs. z_ref in +z up coordinates."""
    dy_idx, dx_idx = np.gradient(z_ref, res_m)
    gx, gy = dx_idx, (-dy_idx if north_up else dy_idx)
    tan_a = np.hypot(gx, gy)
    alpha = np.arctan(tan_a)
    psi = np.arctan2(-gx, -gy)  # downslope azimuth clockwise from North
    dh = z_test - z_ref
    mask = np.isfinite(dh) & np.isfinite(tan_a) & (alpha > np.deg2rad(5.0)) & (alpha < np.deg2rad(45.0))
    for _ in range(3):
        if int(mask.sum()) < 10:
            raise ValueError("Insufficient sloped pixels (< 10) for Nuth-Kaab fit")
        y = dh[mask] / tan_a[mask]
        A = np.column_stack([np.cos(psi[mask]), np.sin(psi[mask]), 1.0 / tan_a[mask]])
        params, *_ = np.linalg.lstsq(A, y, rcond=None)
        res = y - A @ params
        nmad = float(1.4826 * np.median(np.abs(res - np.median(res))))
        if nmad > 0:
            keep = np.abs(res - np.median(res)) <= 3.0 * nmad
            idx = np.flatnonzero(mask)
            mask = mask.copy()
            mask.flat[idx[~keep]] = False
    dy_north, dx_east, dz_bias = params
    return float(dx_east), float(dy_north), float(dz_bias)
```

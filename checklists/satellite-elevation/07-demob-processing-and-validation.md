# Satellite-Built Elevations — Demobilization, Processing, Forensics & Release

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `satellite-elevation` | **Constellation / Platform:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

Processing raw satellite strips into an engineering-grade elevation deliverable requires turning uncalibrated sensor disparities, wrapped interferometric phases, or multispectral water reflectances into a strictly co-registered, datum-clean, artifact-audited raster without contaminating validation independence or leaking restricted vendor assets. Complete physical ground demobilization, sensor-specific pipelines, `Nuth–Kääb` 3D alignment, withheld-checkpoint statistics, `2D FFT`/quantization forensics, and interoperable `COG`/`STAC` packaging below ([Chapter 29](../../fable/chapters/ch29-processing-pipelines.md), [Chapter 53](../../fable/chapters/ch53-accuracy-assessment.md), [Section 7.5](../../gemini4/book/ch-07/sec-07-05.md)).

---

## 1. Ground Target Recovery, Customs & Tasking Closeout (`§4.20.2`, `§4.20.3`, `§4.20.6`)

- [ ] **[GATE]** **Remove temporary ground targets, SAR corner reflectors & pressure gauges with Leave-No-Trace sign-off.** Once raw Level-1 target visibility is verified in Phase `05`, recover all staked vinyl Siemens stars/checkerboards, collapsible trihedral corner reflectors, anchor stakes, road warning signs, and temporary coastal pressure loggers; capture geo-tagged restoration photographs matching Right-of-Entry (`ROE`) and `DOT` encroachment closeout terms ([ch26](../../fable/chapters/ch26-survey-planning.md)). *Evidence:* Signed site-restoration photo log + ROE closeout receipts.
- [ ] **[COND]** **Reconcile international ATA Carnet, IATA DGR 67th Ed. (2026) lithium return & customs manifests (*Trigger:* cross-border equipment mobilization returning home).** Inspect returning GNSS base/rovers, antennas, UHF radios, and reflector panels for transit damage, discharge lithium-ion batteries to **`<= 30 %` state-of-charge** per **IATA DGR 67th Ed. (eff. Jan 1, 2026)** for both **`UN 3480 PI 965 (CAO)`** and **`UN 3481 PI 966` (packed with equipment)** alongside `UN 3090/3091` primary cells and **`49 CFR 171–180`** U.S. ground documentation (`SDS` + `UN 38.3`), and stamp re-export `ATA Carnet` vouchers at customs departure ([ch26](../../fable/chapters/ch26-survey-planning.md), [09 External Register](./09-resources-and-templates.md#5-external-regulatory--technical-standards-register-prdmd-74)). *Evidence:* Stamped return Carnet + hazmat shipping papers.
- [ ] **[GATE]** **Close vendor tasking orders and cancel residual orbital collection queues.** Formally close fulfilled commercial and agency tasking IDs immediately after AOI coverage reaches `>= 98 %` SLA pass, ensuring zero runaway multi-pass charges or overlapping renewal windows, and reconcile any SLA re-tasking credits or cloud-out refunds in [Cost Ledger](../_shared/template-cost-ledger.md) ([ch68](../../fable/chapters/ch68-legal-issues.md)). *Evidence:* Vendor tasking-order closure confirmation + final invoice reconciliation.

---

## 2. Primary Elevation Processing Pipelines (`Stereo`, `KH-9`, `InSAR`, `SDB`)

- [ ] **[GATE]** **Run bias-compensated optical stereo/tri-stereo photogrammetry (`ASP` / `SETSM` / `CARS` / `MicMac`) with separated RPC vs. CSM jitter workflows.** Execute multi-view bundle adjustment against `>= 5` verified `GCPs` (`bundle_adjust -t rpc --robust-threshold 2.0`), orthoproject **all three** views onto a coarse ellipsoid seed DEM (`mapproject` using `Copernicus GLO-30` converted to ellipsoid or `ArcticDEM`) to suppress perspective shear, correlate multi-view tri-stereo (`parallel_stereo --stereo-algorithm asp_mgm` passing `ortho/fwd.tif ortho/nad.tif ortho/bwd.tif`), and grid at `>= 2–3 x GSD` (`point2dem`, producing `*-DEM.tif`). Whenever along-track pushbroom attitude ripples appear ($\Lambda_k = v_{\mathrm{ground}} / f_k$, where $v_{\mathrm{ground}} = \mathrm{GSD}_y / \Delta t_{\mathrm{line}}$ is effective ground-scan speed under slow-scan pitch compensation vs. `~6.7–7.1 km/s` orbital sub-point), run **`jitter_solve` strictly on rigorous CSM / linescan `.xml`/`.json` camera models** (never static `.rpb` RPCs; [ch22](../../fable/chapters/ch22-photogrammetry-sfm.md), [sec-08-05](../../gemini4/book/ch-08/sec-08-05.md), [sec-08-06](../../gemini4/book/ch-08/sec-08-06.md)):

```bash
# Track A: Commercial RPC tri-stereo (ASP bundle_adjust -> mapproject -> parallel_stereo -> point2dem)
bundle_adjust img_fwd.tif img_nad.tif img_bwd.tif \
  img_fwd.rpb img_nad.rpb img_bwd.rpb gcps_control.gcp \
  -t rpc --robust-threshold 2.0 \
  --heights-from-dem copernicus_glo30_ellip.tif --heights-from-dem-uncertainty 10.0 \
  -o ba/run

mapproject --tr 0.50 copernicus_glo30_ellip.tif img_fwd.tif img_fwd.rpb ortho/fwd.tif --bundle-adjust-prefix ba/run
mapproject --tr 0.50 copernicus_glo30_ellip.tif img_nad.tif img_nad.rpb ortho/nad.tif --bundle-adjust-prefix ba/run
mapproject --tr 0.50 copernicus_glo30_ellip.tif img_bwd.tif img_bwd.rpb ortho/bwd.tif --bundle-adjust-prefix ba/run

parallel_stereo ortho/fwd.tif ortho/nad.tif ortho/bwd.tif \
  img_fwd.rpb img_nad.rpb img_bwd.rpb stereo/out copernicus_glo30_ellip.tif \
  --bundle-adjust-prefix ba/run --stereo-algorithm asp_mgm --subpixel-mode 9

point2dem --dem-spacing 1.0 --nodata-value -9999.0 --remove-outliers-params 75.0 3.0 \
  stereo/out-PC.tif -o products/optical_dsm_ellip   # Writes products/optical_dsm_ellip-DEM.tif

# Track B (Rigorous CSM/linescan .xml/.json only -- required for attitude jitter unmixing):
# jitter_solve img_fwd.ntf img_nad.ntf img_bwd.ntf img_fwd.xml img_nad.xml img_bwd.xml \
#   -t dg --heights-from-dem copernicus_glo30_ellip.tif -o ba_jitter/run
```

  *Evidence:* Bundle-adjustment residual report (`<= 0.5 px` GCP RMS) + stereo percentage-good-pixel map (`>= 90 %` bare ground).
- [ ] **[COND]** **Apply 1,081-reseau film dewarp & stable-bedrock control for historical `CORONA KH-4B` / `HEXAGON KH-9` (*Trigger:* declassified historical film track processed).** On `KH-9` mapping frames, extract all `23 x 47 = 1,081` reseau crosses to remove non-linear film shrinkage/warp via bicubic/TPS resampling prior to frame triangulation, or solve time-dependent panoramic scan curves on `KH-4B`, anchoring adjustment solely onto verified unchanging bedrock surrounding glaciers or active landscapes ([ch22](../../fable/chapters/ch22-photogrammetry-sfm.md), [sec-07-05](../../gemini4/book/ch-07/sec-07-05.md)). *Evidence:* Sub-pixel reseau-residual RMS plot (`<= 1.0 px`) + bedrock control footprint.
- [ ] **[GATE]** **Run SAR/InSAR processing (`ISCE3` / `GMTSAR` / `SNAP` + `SNAPHU`) and break Geocoding-DEM Circularity ([ch21 §21.6](../../fable/chapters/ch21-radar-sar-insar.md)).** Enforce `POEORB` orbit precision (`<= 5 cm`), Enhanced Spectral Diversity (`ESD`) coregistration (`< 0.001 px` azimuth residual), topographic phase removal, Goldstein filtering, and `SNAPHU` unwrapping masked below coherence `gamma < 0.35`. Explicitly verify and fix **`2*pi` / integer `h_amb` phase-unwrapping jumps** across steep ridges/islands, merge complementary **Ascending + Descending** DEMs to fill layover/shadow masks, and verify **Geocoding-DEM Circularity**: any vertical bias $\delta h_{\mathrm{ref}}$ in the external DEM used for geocoding injects horizontal shift $\delta h_{\mathrm{ref}} / \tan\theta_i$ into radar products, so update iteratively and record exact geocoding DEM ID/version in `CEOS CARD4L` metadata ([ch21](../../fable/chapters/ch21-radar-sar-insar.md), [ch35](../../fable/chapters/ch35-voids-and-overhangs.md)). *Evidence:* Unwrapped phase continuity check + `CARD4L` geocoding-DEM provenance record.
- [ ] **[GATE]** **Execute coastal SDB atmospheric/glint correction (`ACOLITE`), `Stumpf`/`HOPE` inversion & $\eta(t)$ tide reduction (*Trigger:* coastal SDB deliverable track).** Run `ACOLITE` dark-spectrum atmospheric correction + `Hedley` SWIR/NIR sunglint subtraction (`R_w`), calibrate empirical `Stumpf` ($d_{\mathrm{image}}(t) = m_1 \frac{\ln(n R_w(\lambda_1))}{\ln(n R_w(\lambda_2))} - m_0$) or semi-analytical `HOPE` inversion strictly on the `<= 70 %` calibration split, convert instantaneous depth (`+d ↓`) to Chart Datum via **`d_CD = d_image(t) - eta(t)`** (`z_CD = -d_CD` if emitting `+z ↑` elevation) using synchronized tide-gauge $\eta(t)$ + `VDatum`/`EGM2008` SEP, and mask pixels exceeding the `2–3 / K_d` optical extinction ceiling or land/whitecap masks as `NoData` ([ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md), [sec-11-03](../../gemini4/book/ch-11/sec-11-03.md)). *Evidence:* Tide-reduction log + `K_d` extinction mask + regression calibration residual plot.
- [ ] **[REC]** **Mask hydrological flats, clouds, and stereo water anomalies cleanly before releasing DEM rasters.** Apply synchronized NIR/NDWI water masks and `Copernicus WBM`/`FLM` lake footprints to stereo/InSAR grids—never ship unconstrained optical stereo correlation spikes over flat ocean or specular rivers ([ch34](../../fable/chapters/ch34-water-in-dems.md), [ch35](../../fable/chapters/ch35-voids-and-overhangs.md)). *Evidence:* Clean water-body mask polygon + void percentage summary.

---

## 3. 3D Co-Registration, Withheld Validation & Forensic Screening

- [ ] **[GATE]** **Perform `Nuth–Kääb` 3D co-registration + first-order deramp (`xdem`) across verified static bedrock before validation.** Mask unstable terrain (forests, snow/ice, construction, water, slopes `< 2°` or `> 45°`), solve Nuth & Kääb (2011) ($\frac{\Delta z}{\tan\alpha} = a\cos\psi + b\sin\psi + c\cot\alpha$, `+z ↑`, downslope azimuth $\psi$) + first-order planar deramp (`NuthKaab() + Deramp(poly_order=1)`) against the authoritative local `ICESat-2` / lidar reference (`ref_icesat2_lidar_ellip.tif`), and verify horizontal shift residual `< 0.5 px` and mean vertical offset `< 0.05–0.15 m` ([ch41](../../fable/chapters/ch41-change-detection.md), [sec-14-05](../../gemini4/book/ch-14/sec-14-05.md)):

```python
import xdem, geoutils as gu

ref_dem = xdem.DEM("ref_icesat2_lidar_ellip.tif")
src_dem = xdem.DEM("products/optical_dsm_ellip-DEM.tif").reproject(ref_dem)
stable_mask = gu.Vector("static_bedrock_bare.gpkg").create_mask(ref_dem)

coreg = xdem.coreg.NuthKaab() + xdem.coreg.Deramp(poly_order=1)
aligned_dem = coreg.fit_and_apply(ref_dem, src_dem, inlier_mask=stable_mask)
aligned_dem.save("products/optical_dsm_ellip-DEM_aligned.tif")
diff = aligned_dem - ref_dem
print(f"NMAD={xdem.spatialstats.nmad(diff[stable_mask]):.3f} m | "
      f"med={float(diff[stable_mask].median()):.3f} m")
```

  *Evidence:* Shift vector `(dx, dy, dz)` + pre/post `NMAD` reduction table referencing [ch41](../../fable/chapters/ch41-change-detection.md) and [sec-14-05](../../gemini4/book/ch-14/sec-14-05.md).
- [ ] **[GATE]** **Grade final positional accuracy strictly on locked withheld Check Points + independent `ICESat-2` / `GEDI` / holdout depths.** Evaluate `checkpoints_withheld.csv` (`>= 30` points per stratum; `NVA` & `VVA` separated per **ASPRS Ed. 2 (2024)**). Always propagate known checkpoint survey error unconditionally in quadrature ($\mathrm{RMSE}_{\mathrm{total}} = \sqrt{\mathrm{RMSE}_{\mathrm{DEM}}^2 + \mathrm{RMSE}_{\mathrm{cp}}^2}$—never subtract $\mathrm{RMSE}_{\mathrm{cp}}$ from reported accuracy, keeping $\mathrm{RMSE}_{\mathrm{cp}} \le \tfrac{1}{3}\mathrm{RMSE}_{\mathrm{DEM}}$ as the field survey target). Report `RMSE_V` / `RMSE_H` / `NMAD` with exact **`chi^2` 95 % confidence intervals** ($\widehat{\mathrm{RMSE}}\sqrt{\nu/\chi^2_{0.975,\nu}}$ to $\widehat{\mathrm{RMSE}}\sqrt{\nu/\chi^2_{0.025,\nu}}$, $\nu = n$ for zero-mean RMSE vs $\nu = n-1$ for sample $\sigma$; at $n = 30$, $[0.80, 1.34] \times \widehat{\mathrm{RMSE}}$), spatial autocorrelation (`variogram n_eff`), and labeled legacy `LE90 = 1.6449 * sigma_V` / `CE90` where contracted by NSSDA/Copernicus SLAs. Cross-check regional tilt against **`ICESat-2 ATL06/ATL08`** (`SlideRule`/`icepyx`) and **`GEDI L2A`**, and for SDB evaluate strictly on **`>= 30 %` holdout depths in `2 m` bins** (`RMSE`, bias, `TVU_95%` vs `IHO B-13`). *Evidence:* Signed Validation Certificate + `chi^2` CI table referencing [ch23](../../fable/chapters/ch23-satellite-derived-bathymetry.md) and [ch53](../../fable/chapters/ch53-accuracy-assessment.md).
- [ ] **[GATE]** **Run a quantitative 5-stage Forensic, Spectral (`2D FFT`) & Registration Audit prior to client delivery ([sec-14-03](../../gemini4/book/ch-14/sec-14-03.md), [ch45](../../fable/chapters/ch45-super-resolution.md), [ch54](../../fable/chapters/ch54-evaluating-others-data.md)).** Screen every finished DEM for silent processing bugs (`PixelIsArea` vs `PixelIsPoint` half-pixel shift, integer-meter `int16` rounding, pushbroom jitter striping, un-flagged Poisson void fill, or ML super-resolution hallucination spectral cutoff $\rho(f) = P_{\mathrm{enh}}/P_{\mathrm{ref}} > 1$):

```python
import numpy as np, rasterio
from scipy.ndimage import binary_erosion, laplace

with rasterio.open("products/optical_dsm_ellip-DEM_aligned.tif") as ds:
    z = ds.read(1, masked=True)
    res_m = abs(ds.transform.a)
    area_or_point = ds.tags().get("AREA_OR_POINT", "UNSET")

zv = np.where(np.asarray(z.mask), np.nan, np.asarray(z.data, dtype=np.float64))
valid = np.isfinite(zv)
if int(valid.sum()) < 16:
    raise ValueError("Insufficient finite DEM pixels (< 16) for forensic audit.")

vals = zv[valid]
frac_hist, _ = np.histogram(np.mod(vals, 1.0), bins=20, range=(0.0, 1.0))
quant_spike = float(frac_hist.max() / frac_hist.sum())

# Erode 1 px before Laplacian check so nodata borders do not trigger false void-fill flags
interior = binary_erosion(valid, border_value=0)
lap = np.abs(laplace(np.nan_to_num(zv, nan=float(np.mean(vals)))))
flat_lap_frac = float(np.mean(lap[interior] < 1e-4)) if np.any(interior) else 0.0

# Extract actual centered m x m crop over finite terrain, linear detrend + 2D Hann window
H, W = zv.shape
rows, cols = np.where(valid)
m = min(512, H, W)
r0 = int(np.clip((rows.min() + rows.max()) // 2 - m // 2, 0, H - m))
c0 = int(np.clip((cols.min() + cols.max()) // 2 - m // 2, 0, W - m))
patch = zv[r0 : r0 + m, c0 : c0 + m].copy()
p_valid = np.isfinite(patch)
patch[~p_valid] = float(np.nanmean(patch))

yy, xx = np.mgrid[0:m, 0:m]
A = np.column_stack([xx.ravel(), yy.ravel(), np.ones(m * m)])
coef, *_ = np.linalg.lstsq(A[p_valid.ravel()], patch.ravel()[p_valid.ravel()], rcond=None)
detrended = patch - (coef[0] * xx + coef[1] * yy + coef[2])
if float(np.std(detrended)) < 1e-8:
    psd_ratio = 0.0
else:
    psd = np.abs(np.fft.fftshift(np.fft.fft2(detrended * np.outer(np.hanning(m), np.hanning(m))))) ** 2
    cy, cx = m // 2, m // 2
    rad = max(4, m // 64)
    psd[max(0, cy - rad) : min(m, cy + rad + 1), max(0, cx - rad) : min(m, cx + rad + 1)] = 0.0
    pos = psd[psd > 0.0]
    med = float(np.median(pos)) if pos.size > 0 else 0.0
    psd_ratio = float(pos.max() / med) if (pos.size > 0 and med > 0.0) else 0.0

print(f"AREA_OR_POINT={area_or_point} | res={res_m} m | max_frac_bin={quant_spike:.3f} | "
      f"flat_lap={flat_lap_frac:.3f} | PSD_peak/med={psd_ratio:.1f}")
```

  *Evidence:* Saved Python forensic stdout + 2D PSD radial plot + visual multi-azimuth hillshade sign-off referencing [ch45](../../fable/chapters/ch45-super-resolution.md), [ch54](../../fable/chapters/ch54-evaluating-others-data.md), and [sec-14-03](../../gemini4/book/ch-14/sec-14-03.md).

---

## 4. Interoperable Packaging (`COG`/`STAC`), Security & Archive Handoff (`§4.20.1`, `§4.20.7`)

- [ ] **[GATE]** **Deliver strictly as Cloud-Optimized GeoTIFFs (`COG`) with embedded WKT2:2019, `AREA_OR_POINT` tag, and pixel provenance raster.** Package primary elevation grids using floating-point `ZSTD` (`PREDICTOR=3`) or `LERC` (`MAX_Z_ERROR=0.01`–`0.05 m`, `<= 0.1 x sigma_V`) compression inside `COG`, explicitly verify `AREA_OR_POINT=Area` (pixel-center vs corner agreement within `< 0.5 px`; [ch41](../../fable/chapters/ch41-change-detection.md)), embed full **ISO 19111 WKT2:2019** CRS + geoid SHA-256, and pair every DEM with a **pixel-level source/provenance mask** (`1 = measured optical stereo`, `2 = bistatic/multi-pass InSAR`, `3 = SDB optical`, `4 = interpolated/void-filled`, `5 = ML-bias-corrected/super-resolved`; [ch45](../../fable/chapters/ch45-super-resolution.md), [ch47](../../fable/chapters/ch47-file-formats.md)). *Evidence:* Passing `rio cogeo validate` + `gdalinfo` output citing [ch47](../../fable/chapters/ch47-file-formats.md) and [ch49](../../fable/chapters/ch49-metadata.md).
- [ ] **[GATE]** **Complete Final EULA Compliance, Security Redaction & White-Ribbon Integration Audit prior to public/client release.** Confirm zero commercial raw Level-1 pan/MS strips, `.RPB` files, or proprietary telemetry leak into client/public folders ([sec-27-01](../../gemini4/book/ch-27/sec-27-01.md)); verify all sensitive national-security buffers (`India`/`China`/bases), `GDPR` masks, and `CARE`/`OCAP®`/`NHPA §106` site redactions ([ch69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md)); verify seamless datum blending across the coastal [White-Ribbon Sync](../_shared/multimodal-white-ribbon.md); and deposit versioned **STAC Items + BagIt SHA-256 + Container lockfiles** to a persistent repository (`OpenTopography`, `NSIDC`, or institutional OAIS) with minted **DOI** ([ch50](../../fable/chapters/ch50-archiving-and-provenance.md)). *Evidence:* Release Clearance Certificate + DOI link + BagIt checksum pass log.
- [ ] **[REC]** **Publish reproducible container lockfiles (`conda-lock.yml` / `Docker` digest) and CLI scripts alongside the DOI.** Archive exact `ASP`/`ISCE3`/`SNAP`/`ACOLITE`/`xdem` version pins and command invocations inside the provenance package so any future epoch re-analysis avoids software-drift bias ([ch50](../../fable/chapters/ch50-archiving-and-provenance.md), [ch71](../../fable/chapters/ch71-software-landscape.md)). *Evidence:* Version-controlled `repro/` directory in archive bundle.

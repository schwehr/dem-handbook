# Underwater AUV Bathymetric & Subsea Mapping — Phase 7: Demobilization, Processing & Cross-Validation

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `underwater-auv` | **Platform / Vessel / Hull #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

---

## 1. Custody Lock, Physical Demobilization & UN 3480 Freight Preparation

- [ ] **[GATE]** Complete a final **post-campaign Reference Surface Closure Pass** (where operationally feasible) AND enforce the **100 % Raw Data, Calibration & Custody Gate BEFORE releasing the support vessel or wiping vehicle drives**. *Threshold:* Reconcile every dive number (`100 %` accounting for raw MBES/SAS/SBP datagrams, INS/DVL/Digiquartz logs, USBL/LBL files, CTD/SVP casts, barometric `P_atm` logs, and final lever-arm/patch-test configs) across all `3-2-1` archive copies with matching **`SHA-256` manifests** (`0` missing segments or unverified checksums). *Evidence:* Signed Vessel-Release Data Custody Certificate + Master `SHA256SUMS` file. *Ref:* [ch50-archiving-and-provenance.md](../../fable/chapters/ch50-archiving-and-provenance.md), [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md).
- [ ] **[COND]** Execute **post-impact dimensional lever-arm & boresight re-verification** (*Trigger:* Any hard deck contact, LARS knock, crane snag, or seabed collision occurred during the cruise). *Threshold:* Re-survey affected transducer/IMU/hull mounts or run a closure patch test before demobilizing so mechanical shock shifts cannot corrupt final bathymetry (`<= 0.02–0.05°` residual alignment). *Evidence:* Post-Impact Re-Survey / Boresight Closure Report. *Ref:* [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md) (§25.9 shock trigger).
- [ ] **[GATE]** Execute full **freshwater desalination washdown, corrosion/anode/seal preservation, and desiccant transit packing** within `12 h` of final recovery: flush thrusters, DVL transducer faces, optical windows, SVS/CTD flow ducts, and syntactic seams with clean fresh water and blow dry with oil-free air; inspect **sacrificial zinc anodes** (replace any anode `> 50 %` consumed), clean/re-grease O-rings and SubConn bulkheads for crevice corrosion, and seal dry electronics bays with fresh desiccant. *Evidence:* Signed Hardware Washdown & Preservation Log. *Ref:* Vehicle OEM maintenance manual.
- [ ] **[GATE]** Complete **UN 3480 PI965 / UN 3481 / UN 3090 mandatory battery discharge, `UN 38.3` verification, and hazmat crating**: discharge every standalone air-freight Li-ion module (**`UN 3480 PI965`, `Cargo Aircraft Only (CAO)`** for Section IA/IB) AND **`UN 3481 PI966`** packed-with-equipment Li-ion batteries down to **`<= 30 %` `SoC`** per **IATA DGR 67th Ed. (effective 1 Jan 2026)**; verify **`UN 3481 PI967`** power-isolation lockouts for installed cells (`<= 30 %` recommended when > 100 Wh); package primary lithium-metal transponder/beacon cells (**`UN 3090 CAO` / `UN 3091`**) in UN-certified Class 9 drums; verify undamaged casings (`0` swollen cells) and attach current `UN 38.3` test summaries + `SDS` + `IATA/IMDG` (`49 CFR 171–180` US ground) declarations. *Evidence:* Pre-Shipping Module Voltage/`SoC` Table (`<= 30 %` SoC verified) + Signed DGD. *Ref:* IATA DGR 67th Ed. (2026) / IMDG / 49 CFR via [External Regulatory Basis Register](./09-resources-and-templates.md#external-regulatory--standards-basis-register-non-handbook-authorities).
- [ ] **[COND]** Reconcile **ATA Carnet / temporary import export vouchers**, complete **joint off-hire LARS/deck vessel condition sign-off**, **recover all seabed LBL transponders & project tide gauges**, and perform a **post-survey benchmark leveling closure check** (*Trigger:* International port demob, chartered vessel off-hire, LBL array deployment, or local project tide gauge installation). *Threshold:* Re-level tide gauge staff/sensor to `>= 3` coastal tidal benchmarks (`fable §26.3`; `5+` recommended per `IOC Manuals & Guides 14` reference in `ch25`/`ch26`, `<= 1–2 cm` post-minus-pre closure error); reconcile `100 %` serialized hardware against Carnet counterfoils (`0` left-behind transponders unless explicitly permitted permanent moorings); cancel active `LNM` advisories; submit **UNOLS Post-Cruise Assessment Report (`PCAR`)** if sailing on UNOLS vessels. *Evidence:* Customs-Stamped Carnet Discharge, Off-Hire Sign-Off, LBL Recovery Log & Benchmark Closure Sheet. *Ref:* [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md), [ch26-survey-planning.md](../../fable/chapters/ch26-survey-planning.md); ATA Carnet Convention via [External Regulatory Basis Register](./09-resources-and-templates.md#external-regulatory--standards-basis-register-non-handbook-authorities).

---

## 2. Reproducible Processing Pipeline: TEOS-10, RTS, `mbnavadjust`, CUBE & S-102/BAG

- [ ] **[GATE]** Execute **TEOS-10 / Saunders–Fofonoff Pressure-to-Depth & Vertical Datum Reduction** inside a pinned, reproducible environment (`gsw`, `PROJ`, container hash logged in `W3C PROV`): apply bridge barometric gauge tare **`p_sea_dbar = (p_abs_hpa - p_atm_hpa) * 0.01`** to Paroscientific Digiquartz logs, convert sea pressure to geometric depth using integrated full-depth CTD steric density anomaly (`gsw.z_from_p(..., geo_strf_dyn_height=...)`) and latitude-dependent gravity `g(lat)` (removing the `-45.4 m` raw bias at `3,000 dbar, lat = 45°` and `13.8 m` latitude shift across `0°–70°`), then apply verified tide/inverse-barometer/`SEP` offsets (`h = H + N = z_CD + SEP`). *Evidence:* Reproducible TEOS-10 Depth Reduction Script & Spot-Check Log. *Ref:* [sec-05-04.md](../../gemini4/book/ch-05/sec-05-04.md), [ch09-vertical-datums.md](../../fable/chapters/ch09-vertical-datums.md).
- [ ] **[GATE]** Run **Rauch–Tung–Striebel (`RTS`) Navigation Smoothing, Bathymetric SLAM (`mbnavadjust`), and Layered SVP Ray-Tracing**: smooth INS + DVL (`s_DVL`, `delta_psi_DVL`) + sparse-LBL/USBL trajectories forward-backward (pruning `> 3 sigma` USBL outliers); solve crossline and overlap tie-lines in `mbnavadjust` confirming smooth loop convergence (`<= 0.1–0.3 m` residual vertical scatter, zero unphysical jumps or false flat-mud closures); and re-ray-trace full swaths (`mbprocess` / `Kluster`) with fresh SVP casts. *Evidence:* Navigation Covariance Convergence Plot & `mbnavadjust` Residual Summary. *Ref:* [ch15-slam.md](../../fable/chapters/ch15-slam.md), [ch20-sonar.md](../../fable/chapters/ch20-sonar.md), [sec-10-06.md](../../gemini4/book/ch-10/sec-10-06.md).
- [ ] **[GATE]** Build **CUBE / CHRT Uncertainty Surfaces & Validated `VR-BAG` / `IHO S-102` Deliverables**: generate uncertainty-weighted `CUBE` grids (`Kluster` / `CARIS HIPS` / `Qimera`; `mbgrid` produces Gaussian weighted means rather than CUBE) with sounding count and total uncertainty (`TVU` / `THU`) bands; export **VR-BAG (`FSD 2.0.1`, strictly `+z ↑` elevation)** AND **IHO S-102 (`Ed. 3.0.0`, strictly `+d ↓` depth)** using `float64` horizontal coordinate transforms (preventing `float32` UTM precision jitter) alongside `COG` (`ZSTD`/`LERC`) derivatives. *Threshold:* Zero schema errors under **`S-158:102` format validation**, S-102 HDF5 root attribute **`verticalCS == 6498` (`+d ↓`)** and `/BAG_root/metadata` **`uncertaintyType`** verified, and separately `<= 5 %` nodes failing S-44 `TVU_95%` compliance. *Evidence:* Containerized Processing Script + `S-158:102` Pass + S-44 `TVU_95%` Audit Summary. *Ref:* [ch47-file-formats.md](../../fable/chapters/ch47-file-formats.md), [ch70-specifications-guided-tour.md](../../fable/chapters/ch70-specifications-guided-tour.md), [sec-10-05.md](../../gemini4/book/ch-10/sec-10-05.md).

```bash
# Minimal Reproducible MB-System + TEOS-10 / Python Validation Workflow
# 1. Inspect raw datalist, apply updated SVP + lever-arm/patch offsets, & run SLAM tie-line adjustment
mbdatalist -F-1 -I survey.datalist -O -V
mbnavadjust -I survey.datalist -T -V    # Crossline & overlap tie inversion
mbprocess -I survey.datalist -V          # Write calibrated swath files (.mbXX)
mbgrid -I survey.datalist -A2 -E0.50/0.50/meters! -G3 -N -O auv_final_0p5m_wmean  # Gaussian weighted mean (+z up); use Kluster/Qimera for CUBE

# 2. Verify barometric tare & TEOS-10 depth at 3,000 dbar, lat=45.0 deg
python3 - <<'PY'
import gsw

p_abs_hpa, p_atm_hpa = 301013.25, 1013.25
p_sea_dbar = (p_abs_hpa - p_atm_hpa) * 0.01  # 3000.00 dbar gauge sea pressure
# Standard ocean at lat=45.0 deg (pass geo_strf_dyn_height from full CTD cast for exact steric term)
depth_teos10 = -float(gsw.z_from_p(p_sea_dbar, 45.0))  # +d down (m)
print(f"TEOS-10 depth at {p_sea_dbar:.2f} dbar (45N): {depth_teos10:.3f} m (vs naive 1 dbar=1 m: {depth_teos10 - p_sea_dbar:+.3f} m)")
PY
```

- [ ] **[GATE]** Bundle complete archival package (`ISO 19115-1/-2/-3` + `STAC 1.1.0` + `Descriptive Report A–E` + `GEBCO TID 11–17` tags + **explicit Licence (`CC0`/`CC BY`/contractual) & persistent `DOI`** + `BagIt RFC 8493` `SHA-256` manifest) for `NOAA NCEI/DCDB` or client repository ingestion, applying any authorized security/host-nation **tier-down sanitization** (`e.g., 100 m / 400 m` public release grid vs restricted full-res escrow) prior to external distribution. *Evidence:* BagIt Verification (`bagit.py --validate` exit `0`), `DOI` Registration Receipt & Metadata Schema Pass. *Ref:* [ch49-metadata.md](../../fable/chapters/ch49-metadata.md), [ch50-archiving-and-provenance.md](../../fable/chapters/ch50-archiving-and-provenance.md), [ch69-security-sovereignty-privacy-ethics.md](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md).

---

## 3. Multi-Sensor Cross-Validation, Nuth–Kääb & Forensics Gates

- [ ] **[GATE]** Cross-validate the final AUV bathymetric DEM against **independent reference data** before client sign-off:
  - Compare overlapping **crosslines (`>= 5–10 %` of survey)** and overlapping **ship/USV MBES or prior verified surveys** over stable rocky/consolidated seabed (excluding mobile sandwaves or fluid mud).
  - Run **Nuth & Kääb (2011) 3D terrain co-registration** (`Delta z approx delta * tan(alpha) * cos(psi - psi_0) + c`) across stable sloped seabed patches (`slope 5°–60°`) in consistent **positive-up `+z ↑` elevation** using **downslope geographic aspect clockwise from North** (`atan2(-dz/dx, -dz/dy)`) and iterative `3 * NMAD` outlier rejection to isolate subtle residual `XY` navigation shifts versus true vertical datum bias (`c`).
  - *Threshold:* Residual post-SLAM horizontal shift `<= 0.5–1.5 m` (within `THU_95%`) and vertical crossline/overlap `TVU_95%` (`1.96 * RMSE` and `P95(|Delta z|)`) strictly inside contracted `IHO S-44 Ed. 6.2.0 (Oct 2024; core Table 1 TVU/THU a/b unchanged from Ed. 6.1.0, adding §3.8 seabed characteristics)` / `NOAA HSSD` limits across `>= 95 %` of soundings (note `fable/` cites Ed. 6.1.0 baseline).
  - *Evidence:* Nuth–Kääb Cosinusoid Fit Plot & Crossline Agreement Report. *Ref:* [ch41-change-detection.md](../../fable/chapters/ch41-change-detection.md), [ch53-accuracy-assessment.md](../../fable/chapters/ch53-accuracy-assessment.md), [sec-14-03.md](../../gemini4/book/ch-14/sec-14-03.md), [sec-14-05.md](../../gemini4/book/ch-14/sec-14-05.md).

```python
# Post-Processing Cross-Check: Iterative 3D Nuth-Kaab Co-Registration (+z up grids)
import numpy as np
from scipy.interpolate import RegularGridInterpolator


def fit_nuth_kaab_seabed(
    z_auv_up: np.ndarray, z_ref_up: np.ndarray, grid_res_m: float, north_up: bool = True, max_iter: int = 3
) -> dict:
  """Solve 3D shift (dx_east, dy_north, dz_bias) of positive-up AUV grid vs reference grid."""
  auv = z_auv_up[::-1, :].copy() if north_up else z_auv_up.copy()
  ref = z_ref_up[::-1, :].copy() if north_up else z_ref_up.copy()
  ny, nx = ref.shape
  zy0, zx0 = np.gradient(ref, grid_res_m, grid_res_m)  # row y=North (+), col x=East (+)
  slope0 = np.arctan(np.hypot(zx0, zy0))
  geom_ok = np.isfinite(auv) & np.isfinite(ref) & (slope0 >= np.deg2rad(5.0)) & (slope0 <= np.deg2rad(60.0))
  if int(geom_ok.sum()) < 10:
    return {"n_cells": int(geom_ok.sum()), "converged": False}
  xs, ys = np.arange(nx) * grid_res_m, np.arange(ny) * grid_res_m
  interp_ref = RegularGridInterpolator((ys, xs), ref, bounds_error=False, fill_value=np.nan)
  YY, XX = np.meshgrid(ys, xs, indexing="ij")
  dx_tot, dy_tot, dz_tot = 0.0, 0.0, 0.0
  for _ in range(max_iter):
    pts = np.column_stack([(YY - dy_tot).ravel(), (XX - dx_tot).ravel()])
    ref_s = interp_ref(pts).reshape(ref.shape)
    dz = (auv - dz_tot) - ref_s
    ok = geom_ok & np.isfinite(dz)
    if int(ok.sum()) < 10:
      break
    r = dz[ok]
    nmad = 1.4826 * np.median(np.abs(r - np.median(r)))
    inliers = ok & (np.abs(dz - np.median(r)) <= max(3.0 * nmad, 1e-6))
    if int(inliers.sum()) < 10:
      break
    zy_s, zx_s = np.gradient(ref_s, grid_res_m, grid_res_m)
    sl = np.arctan(np.hypot(zx_s[inliers], zy_s[inliers]))
    asp = np.arctan2(-zx_s[inliers], -zy_s[inliers])  # downslope clockwise from North
    y = dz[inliers] / np.tan(sl)
    X = np.column_stack([np.cos(asp), np.sin(asp), 1.0 / np.tan(sl)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    dx_tot += float(beta[1])
    dy_tot += float(beta[0])
    dz_tot += float(beta[2])
  return {
      "n_cells": int(geom_ok.sum()),
      "dx_east_m": round(dx_tot, 3),
      "dy_north_m": round(dy_tot, 3),
      "horiz_shift_m": round(float(np.hypot(dx_tot, dy_tot)), 3),
      "vertical_bias_m": round(dz_tot, 3),
      "converged": True,
  }
```

- [ ] **[REC]** Inspect **4-azimuth hillshades (`45°, 135°, 225°, 315°` illumination), `z mod 1 m` quantization scans, and 2D FFT Power Spectral Density (`PSD`)** on the final grid to rule out residual roll oscillation, outer-beam SVP smiles, pitch-latency saw-tooth steps, or cross-track motion striping. *Evidence:* 4-Azimuth Hillshade Mosaic & 2D FFT Artifact Check. *Ref:* [sec-14-03.md](../../gemini4/book/ch-14/sec-14-03.md), [ch53-accuracy-assessment.md](../../fable/chapters/ch53-accuracy-assessment.md).
- [ ] **[REC]** Verify **companion sensor parity (`Backscatter`, `SAS Imagery`, `WCI`, `SBP` horizons)** confirming all auxiliary grids and sub-bottom segy horizons share the final `RTS + mbnavadjust` navigation solution and matching CRS/epoch definitions. *Evidence:* Companion Layer Alignment & CRS Manifest. *Ref:* [ch20-sonar.md](../../fable/chapters/ch20-sonar.md), [ch47-file-formats.md](../../fable/chapters/ch47-file-formats.md).
- [ ] **[REC]** Run an automated **`h5py` / `pyproj` precision and schema check** confirming `float64` horizontal coordinate origins (`0` single-precision `float32` UTM staircase jitter), S-102 `verticalCS == 6498` (`+d ↓`), `/BAG_root/metadata` `uncertaintyType` consistency (`1 sigma` vs `95 %`), zero `NaN` vs `nodata = 1e6` mismatches, and clean CRS WKT2 tags. *Evidence:* Automated Python Schema & Precision Check Output. *Ref:* [ch47-file-formats.md](../../fable/chapters/ch47-file-formats.md), [sec-10-05.md](../../gemini4/book/ch-10/sec-10-05.md).
- [ ] **[COND]** Document **white-ribbon multi-modal blend diagnostics** across shallow AUV-to-ship/USV/LiDAR seams per [multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md) (*Trigger:* Survey merges AUV bathymetry with overlapping vessel or airborne/coastal DEMs). *Threshold:* Seam jump `<= 0.15 m` mean bias and zero double-counted shoal cliffs or datum step discontinuities. *Evidence:* Seam Difference Profile Plot. *Ref:* [ch48-compositing.md](../../fable/chapters/ch48-compositing.md), [ch66-coastal-marine-polar-lakes-rivers.md](../../fable/chapters/ch66-coastal-marine-polar-lakes-rivers.md).

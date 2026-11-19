# Land Aircraft LiDAR & Imagery — Underway QC & Field Processing

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `land-aircraft-lidar-imagery` | **Platform / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[x] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier & Date (UTC):** `__________________`

---

## 1. In-Flight Operator Monitoring & Telemetry Checks

- [ ] **[GATE]** Monitor real-time **GNSS/INS health, `C/N0`/`AGC` interference levels, and `MTA` zone stability** continuously during every strip: confirm `>= 7` tracked SVs, `PDOP <= 3.0`, steady `C/N0` and receiver `AGC` (alert immediately on suspected jamming/spoofing transients), green Kalman alignment/innovation metrics, and zero unflagged `MTA` zone jumps over steep ridges. *Evidence:* Operator in-flight log with timestamped telemetry status per line. *Refs:* [ch12-gnss](../../fable/chapters/ch12-gnss.md), [ch-13/sec-13-03](../../gemini4/book/ch-13/sec-13-03.md).
- [ ] **[GATE]** Log exact `UTC` time spans of **low cumulus clouds, valley fog, wildfire smoke, or industrial steam plumes** intersecting the swath so obscured sub-swaths enter immediate re-fly queueing rather than escaping into late bare-earth interpolation. *Evidence:* Timestamped atmospheric dropout log cross-referenced to FMS strip IDs. *Refs:* [ch36-seasonal-variability](../../fable/chapters/ch36-seasonal-variability.md), [ch26-survey-planning](../../fable/chapters/ch26-survey-planning.md).
- [ ] **[GATE]** Confirm real-time **swath edge coverage, ground speed vs. `ANPS`, and camera radiometry** after each line: check crosswind crab angle against swath width $W$ to confirm `>= 20 %` overlap without gaps, ensure tailwind ground speed $v$ stayed inside density limits, and inspect metric RGB/NIR histograms for zero clipped snow/roof highlights. *Evidence:* In-flight FMS coverage polygon overlay and camera exposure histogram log. *Refs:* [ch26-survey-planning](../../fable/chapters/ch26-survey-planning.md), [ch22-photogrammetry-sfm](../../fable/chapters/ch22-photogrammetry-sfm.md).
- [ ] **[REC]** Record **pressurized cabin differential (`ΔP`), optical-port heater status, and flight-level pressure/temperature** per altitude block so post-processing verifies `n_g,air` and optical-window meniscus stability. *Evidence:* Sortie environment table recorded in flight log. *Refs:* [ch-07/sec-07-03](../../gemini4/book/ch-07/sec-07-03.md), [ch-09/sec-09-01](../../gemini4/book/ch-09/sec-09-01.md).

---

## 2. Same-Day Trajectory, Density, Overlap & Corduroy QC

- [ ] **[GATE]** Compute **same-day `PPK/RTS` forward–reverse `SBET` trajectories** (`POSPac` / `Inertial Explorer`) within `<= 12 h` of engine shutdown: confirm `>= 95 %` fixed integer ambiguities on production strips, verify base coordinates match `OPUS`/`NGS` control within `<= 0.015 m`, and enforce **`<= 0.02–0.03 m` nominal forward–reverse separation** with a hard **`<= 0.05–0.10 m` alert/re-fly cutoff** (inspecting long baselines for unmodeled IERS 2010 solid-Earth tide bias). *Evidence:* Same-day `SBET` QC report (`dN, dE, dD` separation, `PDOP`, ambiguity ratio). *Refs:* [ch12-gnss](../../fable/chapters/ch12-gnss.md), [ch26-survey-planning](../../fable/chapters/ch26-survey-planning.md), [ch36-seasonal-variability](../../fable/chapters/ch36-seasonal-variability.md).
- [ ] **[GATE]** Produce a **daily open-terrain spatial point-density (`ANPD`) and holiday-void raster** (`2 × ANPS` grid cells per USGS LBS spatial-distribution test — e.g., `0.71 m` for QL0/QL1, `1.41 m` for QL2 — alongside `1.0 m` open-terrain `ANPD`): verify **`>= 90 %` of `2 × ANPS` cells contain `>= 1` first return**, verify open-terrain aggregate `ANPD >= QL threshold` (`>= 2.0 pls m⁻²` QL2; `>= 8.0 pls m⁻²` QL0/QL1), and detect any unflagged holiday voids `>= (4 × ANPS)²`. *Evidence:* Daily `ANPD` `GeoTIFF` and pass/fail cell percentage report. *Refs:* [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md), [ch-13/sec-13-03](../../gemini4/book/ch-13/sec-13-03.md).
- [ ] **[GATE]** Quantify **daily inter-swath vertical consistency (`RMSD_z`)** and **intra-swath repeatability** on open hard surfaces (`slope < 5°` and cross-tie intersections): enforce **`RMSD_z <= 0.08 m` for QL1/QL2 (`<= 0.04 m` QL0; internal field trigger `<= 0.05 m`, max excursion `<= 0.16 m`)** and intra-swath smoothness `<= 0.06 m`. *Evidence:* Daily overlap `dz` raster and `RMSD_z` summary table. *Refs:* [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md), [ch56-case-files](../../fable/chapters/ch56-case-files.md).
- [ ] **[GATE]** Inspect **multi-azimuth low-sun hillshades (`315°` and `45°` azimuths at `15°–25°` solar altitude)** over smooth airport runways, highways, and aprons nightly specifically to catch **"corduroy" cross-track mirror lag / encoder hysteresis** (`> 0.05 m` peak-to-trough) and outer-edge roll curling before subsequent sorties. *Evidence:* Annotated low-sun runway/road hillshade screenshots archived in daily QC folder. *Refs:* [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md), [ch-14/sec-14-03](../../gemini4/book/ch-14/sec-14-03.md).
- [ ] **[GATE]** Perform a **Sortie 1 ground-truth spot check** within `24 h` against the `>= 5–10` un-withheld airport/field verification targets (preserving full blinding on the sealed ASPRS independent `CP` set) to expose `18 s` `GPST–UTC` shifts (`1,080 m`), geoid sign flips, `US Survey Foot` scaling (`2 ppm`), or base `ARP` collar errors immediately. *Evidence:* Sortie 1 verification bias summary (`|mean Δz| <= 0.05 m`, `RMSE_z <= 0.08 m`). *Refs:* [ch52-ground-truth](../../fable/chapters/ch52-ground-truth.md), [ch-32/sec-32-01](../../gemini4/book/ch-32/sec-32-01.md).

---

## 3. Immutable Ingest, Custody & Automated Re-Fly Triggers

- [ ] **[GATE]** Generate **`SHA-256` checksums on raw offload** (`RINEX`, `IMU`, raw `.rxp`/`.csd`/PulseWaves, raw camera imagery, flight/operator logs) and replicate across a **`3-2-1` backup topology** (`3` copies, `2` distinct media types, `1` off-site/cloud archive) **prior to reformatting aircraft SSDs**. *Evidence:* Signed `SHA-256` verification log with zero hash mismatches. *Refs:* [ch50-archiving-and-provenance](../../fable/chapters/ch50-archiving-and-provenance.md), [ch-19/sec-19-01](../../gemini4/book/ch-19/sec-19-01.md).
- [ ] **[COND]** Issue an immediate **Field Re-Fly Order** mapped to exact strip IDs and log re-fly hours/standby burn in [template-cost-ledger](../_shared/template-cost-ledger.md) before leaving the staging airport whenever any trigger trips: (1) `SBET` fwd–rev `> 0.10 m`; (2) holiday void or cloud/smoke dropout `> (4 × ANPS)²`; (3) `< 90 %` of `2×ANPS` cells populated; (4) `RMSD_z > 0.08 m` (`> 0.04 m` QL0); or (5) unresolved corduroy striping `> 0.05 m` on paved surfaces. *Trigger:* Any daily QC check breaching threshold. *Evidence:* Exported `.kml`/`.gpkg` re-fly line package queued in FMS + cost-ledger entry. *Refs:* [ch26-survey-planning](../../fable/chapters/ch26-survey-planning.md), [ch56-case-files](../../fable/chapters/ch56-case-files.md).
- [ ] **[COND]** Run preliminary **photogrammetric tie-point bundle adjustment (`sigma_0 <= 0.5–1.0 px`)** and compare Sortie 1 `SGM` elevations over flat open ground against coincident LiDAR ground points to rule out `1 %` focal-length shift or pressurized optical-port doming. *Trigger:* Any sortie collecting metric frame or pushbroom imagery. *Evidence:* Preliminary bundle report and `SGM-vs-LiDAR` flat-field difference plot. *Refs:* [ch22-photogrammetry-sfm](../../fable/chapters/ch22-photogrammetry-sfm.md), [ch-07/sec-07-03](../../gemini4/book/ch-07/sec-07-03.md).
- [ ] **[REC]** Execute the automated **`PDAL` + `GDAL` + `Python` nightly QC pipeline** (below) on calibrated swath exports to verify `ANPD`, swath `RMSD_z`, and low-sun hillshades reproducibly. *Evidence:* Archived terminal stdout and generated `dz_AB.tif` / `hs_315.tif` rasters. *Refs:* [ch18-topographic-lidar](../../fable/chapters/ch18-topographic-lidar.md), [ch-14/sec-14-03](../../gemini4/book/ch-14/sec-14-03.md).

### Runnable Field QC Pipeline (`PDAL` + `GDAL` + `Python`)

```bash
# 1. Open-terrain single-return ANPD grid (use range filter + inferred GTiff writer from .tif)
pdal translate strip_A.laz strip_A_anpd.tif range \
  --filters.range.limits="ReturnNumber[1:1]" \
  --writers.gdal.resolution=1.0 \
  --writers.gdal.output_type="count" \
  --writers.gdal.nodata=-9999

# 2. Overlapping swath min-Z rasters on shared aligned origin/bounds & intersected difference
BOUNDS="([500000,502000],[4500000,4502000])"
for s in strip_A strip_B; do
  pdal translate "${s}.laz" "${s}_z.tif" \
    --writers.gdal.resolution=0.5 --writers.gdal.output_type="min" \
    --writers.gdal.bounds="$BOUNDS" --writers.gdal.nodata=-9999
done
gdal_calc.py --extent=intersect -A strip_A_z.tif -B strip_B_z.tif --outfile=dz_AB.tif \
  --calc="(A-B)*((A!=-9999)&(B!=-9999)) + (-9999)*((A==-9999)|(B==-9999))" \
  --NoDataValue=-9999

# 3. Low-sun orthogonal hillshades (18 deg altitude) for corduroy mirror-lag inspection
gdaldem hillshade strip_A_z.tif hs_315.tif -az 315 -alt 18
gdaldem hillshade strip_A_z.tif hs_045.tif -az 45  -alt 18
```

```python
import numpy as np
import rasterio

with rasterio.open("dz_AB.tif") as src:
    dz = src.read(1, masked=True).compressed()
    dz = dz[np.isfinite(dz)]
    if dz.size == 0:
        raise ValueError("Empty overlap mask between strip_A_z.tif and strip_B_z.tif")
    med = float(np.median(dz))
    nmad = float(1.4826 * np.median(np.abs(dz - med)))
    core = dz if nmad == 0.0 else dz[np.abs(dz - med) <= 3.0 * nmad]
    if core.size == 0:
        raise ValueError("No valid overlap pixels remaining after 3*NMAD filter")
    rmsd_z = float(np.sqrt(np.mean(core**2)))
    print(f"Overlap N={core.size}, Bias={med:+.4f} m, NMAD={nmad:.4f} m, RMSD_z={rmsd_z:.4f} m")
    assert rmsd_z <= 0.080, f"FAIL: RMSD_z {rmsd_z:.4f} m exceeds 0.080 m QL1/QL2 gate"
```

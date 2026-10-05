# Appendix H — Datasets for exercises and benchmarks

This appendix lists open datasets that are suitable for teaching, for testing algorithms, and for the exercises implied throughout the handbook. It is organized by what the dataset is *for*: algorithm benchmarks with labels (H.1), validation references (H.2), teaching scenes keyed to chapters (H.3), bathymetric and hydrographic samples (H.4), planetary samples (H.5), and synthetic data with known truth (H.6). Each row names the licence as published; licences change, and several "research-only" datasets forbid commercial use or redistribution, so read the terms before copying data into a course repository.

Sizes are approximate and given to help plan downloads; "(verify)" marks values not confirmed against the current landing page. URLs point to the canonical host; many datasets are mirrored on OpenTopography, AWS Open Data, Zenodo, or Hugging Face.

> **Rule of thumb.** For an algorithm benchmark, choose a dataset with *labels and a published evaluation protocol* (H.1). For validating a *product*, choose a reference with *better accuracy and independent lineage* (H.2). Confusing the two — scoring a global DEM against a dataset derived from the same lidar it was trained on, for example — is the most common error in published comparisons ([Chapter 52](../chapters/ch52-ground-truth.md) §52.7, [Chapter 43](../chapters/ch43-traditional-vs-ml.md) §43.5).

## H.1 Algorithm benchmarks (labelled point clouds, DSM/DTM pairs)

| Dataset | Content | Size (approx.) | Labels / truth | Licence | Good for | Chapters |
|---|---|---|---|---|---|---|
| ISPRS Vaihingen (2D + 3D semantic labelling) | ALS (≈ 4 pts/m²) and orthoimagery, Vaihingen, Germany, 2008 | ≈ 1 GB | 9 classes (3D), 6 classes (2D) | Research use; registration required (ISPRS/DGPF) | Ground filtering, urban semantics | 30, 42 |
| ISPRS Toronto | ALS + imagery, downtown Toronto | ≈ 1 GB | Buildings, trees | Research use | Building extraction in dense urban | 42, 63 |
| ISPRS Filter Test (Sithole & Vosselman 2004) | 15 reference sites, ALS, manual ground labels | small (tens of MB) | Ground / non-ground | Free for research | Classic ground-filter evaluation (Type I/II) | 30 |
| OpenGF (Qin et al. 2021) | ≈ 47 km² ALS from 4 countries, 9 terrain scenes | ≈ 10 GB | Ground / non-ground | Derived from open ALS; CC BY (verify) | Learning-based ground filtering | 30, 43 |
| DALES / DALES Objects | ≈ 10 km² ALS, Dayton, Ohio, 505 M points | ≈ 20 GB | 8 classes; instances (Objects) | CC BY-NC-SA 4.0 (verify) | Semantic segmentation at ALS density | 42 |
| Hessigheim 3D (H3D) | UAV lidar (≈ 800 pts/m²) + mesh, 4 epochs, Hessigheim, Germany | ≈ 10 GB per epoch | 11 classes; mesh labels | Research use (registration) | High-density semantics; multi-epoch | 42, 41 |
| SensatUrban | Photogrammetric point clouds, Birmingham/Cambridge/York, ≈ 7.6 km² | ≈ 30 GB | 13 classes | Code MIT; dataset terms on project page (verify) | City-scale photogrammetric semantics | 42, 63 |
| Toronto-3D | Mobile lidar, ≈ 1 km of road | ≈ 2 GB | 8 classes | MIT / CC BY (verify) | Mobile-mapping semantics | 16, 42 |
| Semantic3D / Paris-Lille-3D | TLS and MLS urban scenes | 10–30 GB | 8–9 classes | CC BY-NC-SA / research | Terrestrial semantics | 42 |
| US3D / IEEE GRSS DFC 2019 | Multi-view WorldView-3 + ALS, Jacksonville and Omaha | ≈ 100 GB | DSM truth from lidar; semantic labels | DFC terms (research) | Satellite stereo DSM accuracy; 3D reconstruction | 22, 43 |
| IEEE GRSS DFC 2018 (Houston) | Hyperspectral + ALS + VHR | ≈ 10 GB | 20 classes | DFC terms | Fusion for land cover | 42 |
| ETH3D / Tanks & Temples / DTU | Close-range MVS benchmarks with laser-scan truth | 10–100 GB | Dense truth geometry | CC BY-NC-SA / research | Photogrammetric dense-matching evaluation | 22 |
| Middlebury stereo | Classic stereo pairs with truth | small | Disparity truth | Research | Teaching stereo matching | 22 |
| TLSpecies / ForInstance / FOR-species20K | Forest TLS/ULS with tree instances | 10–50 GB | Tree instances/species | CC BY 4.0 (verify) | Canopy and ground under forest | 64 |
| NEON AOP | Airborne lidar + hyperspectral + camera at ≈ 80 US sites, repeated annually | TB (site subsets GB) | Field plots (vegetation structure) | CC0 / public domain | Forest canopy vs. ground; multi-year change | 36, 64 |
| Hyytiälä / EuroSDR benchmarks | Forest ALS/ULS benchmarks | GB | Field trees | Research | — | 64 |
| 3D BAG | LoD1.2/1.3/2.2 building models of the Netherlands from AHN + BAG footprints | GB per tile set | Building models with quality attributes | CC BY 4.0 | Urban LoD2 exercises; DSM→DTM in cities | 63 |
| DEMIX tiles (Guth et al. 2024) | 10 km × 10 km tiles with reference DTM/DSM (lidar-derived) and all 1″ global DEMs | GB | Reference DEMs | Open (tile list and criteria on GitHub; reference DEMs under their national licences) | Global DEM ranking; intercomparison | 53, 55 |

## H.2 Validation references (truth, quasi-truth, benchmarks)

| Dataset | Content | Access | Accuracy of reference | Licence | Use | Chapters |
|---|---|---|---|---|---|---|
| ICESat-2 ATL03 / ATL06 / ATL08 | Photon heights; land-ice segments (20 m); land/vegetation (100 m segments with terrain and canopy) | NSIDC, icepyx, SlideRule, OpenAltimetry | ≈ 0.1–0.5 m vertical on flat open ground (strong beams); worse on slopes; geolocation ≈ 5 m | Free (NASA) | Global DEM validation; co-registration reference | 52.4, 53 |
| GEDI L2A / L2B | Footprint (≈ 25 m) elevation and canopy metrics, 51.6°N–51.6°S, 2019– | LP DAAC, ORNL | Ground elevation ≈ 1–3 m typical; geolocation ≈ 10 m | Free | Forest-height checks; terrain under canopy (with care) | 52, 64 |
| ICESat GLAS (2003–2009) | Historical footprint altimetry (≈ 70 m) | NSIDC | ≈ 0.1–0.5 m on flat ice/ground | Free | Reference epoch for change | 41 |
| NGS datasheets / OPUS Shared | US passive marks with NAVD88/NAD83 coordinates and orders | NGS web/API | cm-level (order-dependent); many marks disturbed | Public domain | Checkpoints; datum sanity | 25, 52 |
| National benchmark databases (e.g. OS, IGN, swisstopo, LINZ) | Levelling benchmarks and GNSS stations | Agency portals | mm–cm | Varies (mostly open) | Checkpoints | 25 |
| USGS 3DEP point clouds (AWS EPT/COPC) | QL2/QL1 lidar, CONUS and territories | `s3://usgs-lidar-public/` (EPT); The National Map (LAZ) | ≈ 5–10 cm RMSE_z NVA | Public domain | High-quality reference for coarser products | 52, 55 |
| OpenTopography lidar collections | Hundreds of ALS/TLS datasets incl. repeat surveys | OpenTopography portal/API | Dataset-specific reports | Mostly CC BY / public domain | Reference surfaces; repeat-survey change | 41, 52 |
| AHN4/5, EA National LIDAR, swissSURFACE3D, DHM, NLS, NDH, LiDAR HD | National lidar (Appendix E.5) | National portals | 5–20 cm | Open (see App. E) | Reference DTMs for DEMIX-style tests | 55 |
| CORS / IGS station coordinates and time series | Continuous GNSS positions and velocities | NGS, IGS, UNAVCO/EarthScope, EUREF | mm–cm | Free | Reference frame epochs; VLM | 8, 38 |
| Tide gauges (PSMSL, NOAA CO-OPS, GLOSS) | Water-level records and datums | Portals/API | cm | Free | Datum checks; VLM | 9, 38 |
| GNSS campaign checkpoints shared in papers (e.g. Guth 2021 lidar/ICESat-2 test sets) | Checkpoint tables | Supplementary data | Reported | Varies | Reproducing published assessments | 53 |

## H.3 Teaching scenes keyed to chapters

Each scene is chosen so that the phenomenon in the chapter is visible with free tools (QGIS, PDAL, GDAL, xdem). Suggested exercise and expected outcome are given so an instructor can check results.

| Scene | Datasets | Chapter(s) | Exercise | Expected outcome |
|---|---|---|---|---|
| Global DEM intercomparison tile | One DEMIX tile: Copernicus GLO-30, NASADEM, AW3D30, FABDEM, GEDTM30 + national lidar DTM + ICESat-2 ATL08 | 53, 55 | Co-register each DEM to the lidar (xdem Nuth–Kääb), compute stratified residuals by slope and land cover; rank | Copernicus lowest σ in open terrain; FABDEM/GEDTM30 lower bias in forest; AW3D30 and NASADEM show shifts of ~0.3–1 pixel; all show forest bias of several m |
| Geoid mix-up demonstration | Any Copernicus tile + the EGM2008 undulation grid (PROJ `egm08_25.gtx`) + TanDEM-X 90 m (ellipsoidal) | 7, 9 | Difference Copernicus (EGM2008) from TanDEM-X 90 (ellipsoid) with and without applying N | Without N: smooth offset equal to local undulation (tens of m); with N: residual σ ≈ 1–2 m |
| Coastal lidar + MBES seam | One CUDEM 1/9″ tile and its source lidar (NOAA Digital Coast) and BlueTopo tiles | 34, 48, 66 | Profile across the shoreline; identify the datum variant; find the white ribbon | Visible step or smoothing at the land–water seam; MLLW–NAVD88 separation of 0.5–2 m if datums mixed |
| Urban LoD2 city block | 3D BAG tile + AHN4 point cloud (Rotterdam or Amsterdam) | 32, 63 | Build DSM and DTM from AHN; compare DTM under buildings with 3D BAG ground heights; test bridge inclusion rules | Interpolated ground under buildings differs from 3D BAG by 0.1–0.5 m; bridges present/absent changes flow routing |
| Forested slope, leaf-on vs leaf-off | 3DEP project pairs where a state program re-flew (e.g. Pennsylvania 2006–08 vs PAMAP 2017–19; verify availability) or NEON site repeated flights | 36, 64 | Compute ground-point density and DTM difference by canopy class | Leaf-on ground density drops 2–10×; DTM differences of 0.1–0.5 m under canopy with positive bias leaf-on |
| River with hydro-flattening | 3DEP 1 m DTM + source LAZ + NHDPlus HR flowlines | 34, 61 | Compare the hydro-flattened DTM with a raw TIN DTM; route flow with WhiteboxTools | Raw DTM shows triangulation across water and bridge decks damming flow; flattened DTM routes but hides bathymetry |
| Landslide pre/post pair | Oso, Washington 2014: pre-event lidar (2013 PSLC; verify) and post-event lidar (2014) via OpenTopography / WA DNR | 39, 41 | Co-register on stable terrain; difference; threshold with LoD; compute volume with correlated-error interval | Deposit and scarp volumes of order 10⁷ m³ (verify against published value ≈ 7.6 × 10⁶ m³ (verify)); LoD ≈ 0.2–0.4 m |
| Glacier DEM time series | ArcticDEM strips over a Svalbard or Alaska glacier + ICESat-2 ATL06 | 40, 41, 66 | Register strips to ATL06 off-ice; compute elevation change per year | Thinning of metres per year at the terminus; off-ice residual σ ≈ 1 m after registration |
| Power-line corridor | Any open ALS with class 14 (wire conductor) e.g. AHN4 tiles over high-voltage lines, or a utility sample on OpenTopography | 33 | Extract class 14; fit catenaries; compute clearance to class 2/5 | Catenary sag of several m; clearance violations detectable only at ≥ 8 pts/m² (verify) |
| Earthquake coseismic pair | Kaikōura 2016 (LINZ pre/post lidar) or El Mayor–Cucapah 2010 (INEGI/B4-style lidar via OpenTopography) | 38, 39 | Horizontal offsets by image correlation (COSI-Corr or xdem) and vertical by DoD after local co-registration | Metre-scale horizontal and vertical offsets; naive co-registration erases the signal — a teaching point |
| Planetary HiRISE DTM | HiRISE DTM over a candidate landing site + CTX DEM + MOLA PEDR | 67 | Compare DTM with MOLA shots; estimate alignment residuals | Residuals of a few m with a planar tilt; MOLA shot spacing shows interpolation limits |
| Port MBES with crosslines | Shallow Survey common dataset (e.g. Plymouth 2015/2018; verify availability) or a NOAA survey (H-number) with BAG from NCEI | 20, 26, 53 | Crossline analysis; compute TVU vs S-44 Order; inspect CUBE hypotheses | Crossline differences within Order 1a in the channel; outliers at quay walls (multipath) |
| SDB scene | Sentinel-2 L2A scene + reference MBES/lidar bathy (e.g. NOAA NCMP topobathy in Florida Keys; verify) | 23 | Fit Stumpf log-ratio model; validate by depth bin | Good to ≈ 10–15 m in clear water; bias and σ grow with depth and turbidity |
| Flood-map sensitivity | FABDEM vs Copernicus vs national lidar over a floodplain; LISFLOOD-FP or HEC-RAS 2D | 61 | Run the same event on three DEMs | Inundated area differs by tens of percent between DSM and DTM; lidar vs FABDEM differ in detail but less in extent |
| Datum/epoch shift exercise | A 1980s USGS DEM (NGVD29, NAD27), a 2010s 3DEP DTM, and HTDP/VDatum | 8, 9, 56.21 | Transform the old DEM; difference | Systematic offsets of 0.3–1.5 m vertical (NGVD29→NAVD88 + VLM) and tens of m horizontal if NAD27 is ignored |

<!-- figure: Figure H.1 — Map of the teaching scenes (global), with icons for the sensor type and the chapter numbers, plus thumbnails of three of them (DEMIX tile, Oso, Kaikōura). -->

## H.4 Bathymetric and hydrographic samples

| Dataset | Content | Access | Licence | Use | Chapters |
|---|---|---|---|---|---|
| NOAA NCEI hydrographic surveys (BAG, XYZ, DR) | Every NOAA survey since the 1800s (smooth sheets) and modern BAGs with uncertainty | NCEI Bathymetric Data Viewer | Public domain | BAG inspection; CUBE QC; historical change | 20, 47 |
| NOAA BlueTopo tiles | Elevation/uncertainty/contributor; US waters | AWS `noaa-ocs-nationalbathymetry-pds` | Public domain | Compositing with supersession; uncertainty layers | 48, 55 |
| MB-System test data and tutorials | Sample multibeam files for every supported format | MB-System site / GitHub | GPL-3.0 (software); data public | Patch test; editing; gridding | 20 |
| Shallow Survey common datasets | Multibeam/lidar over the same area for the Shallow Survey conference series (2001–) | Conference archives (verify hosting) | Research use | Cross-system comparison | 20, 26 |
| EMODnet Bathymetry DTM tiles + CDI | DTM and per-cell source references | EMODnet portal | CC BY 4.0 | Source-layer-based QC | 48, 55 |
| GEBCO grid + TID | 15″ grid with type identifier | GEBCO | Free | Measured vs predicted mapping | 23, 55 |
| USACE eHydro channel surveys | Frequent SBES/MBES of federal channels | eHydro portal | Public domain | Dredging change detection | 41, 65 |
| Multibeam archives: MGDS / R2R / GMRT cruises | Raw and processed MBES from research vessels | MGDS, R2R | Free (varies) | Deep-water processing exercises | 20 |
| JALBTCX / NOAA NCMP topobathy lidar | Coastal topobathy lidar (CZMIL) | NOAA Digital Coast | Public domain | Land–water transition; turbidity limits | 19, 34 |
| IHO S-102 sample datasets | S-102 HDF5 bathymetric surfaces | IHO / NOAA (verify) | Free | Format validation | 47 |
| Lake and river bathymetry (USGS, Great Lakes NCEI) | Reservoir and river bathy, IGLD datums | USGS ScienceBase, NCEI | Public domain | Inland datum exercises | 66 |

## H.5 Planetary samples

| Dataset | Body | Access | Licence | Use | Chapters |
|---|---|---|---|---|---|
| HiRISE DTMs (e.g. Jezero, Gale, candidate landing sites) | Mars | UA HiRISE DTM page; PDS | Public domain | Stereo DTM QA without ground truth | 67 |
| CTX stereo pairs + ASP tutorials | Mars | PDS; ASP documentation examples | Public domain / Apache-2.0 | Build a DEM with ASP; align to MOLA | 22, 67 |
| MOLA PEDR (shot data) and MEGDR | Mars | PDS Geosciences Node | Public domain | Interpolation across track gaps | 67, 31 |
| LOLA RDR shots, LDEM, SLDEM2015 | Moon | PDS | Public domain | Polar DEMs; shadowed regions | 67 |
| LRO NAC DTMs (ASU) | Moon | LROC RDR | Public domain | Landing-site slope statistics | 67 |
| Bennu / Ryugu shape models | Asteroids | PDS SBN; JAXA DARTS | Public domain / JAXA terms | Meshes vs grids; non-convex bodies | 46, 67 |
| Titan / Europa radar topography (Cassini, Galileo) | Outer planets | PDS | Public domain | Sparse-data mapping | 67 |

## H.6 Synthetic data with known truth

Synthetic terrain lets you test an algorithm against a truth you control: you know the bias, the noise, the correlation length, the stripes, the blunders, and the mis-registration, because you injected them. It is the only way to verify that an accuracy-assessment script computes what it claims ([Chapter 5](../chapters/ch05-error-and-uncertainty.md), [Chapter 53](../chapters/ch53-accuracy-assessment.md)), that a co-registration routine recovers a known shift ([Chapter 41](../chapters/ch41-change-detection.md)), or that an interpolator's error grows with gap size the way theory says ([Chapter 31](../chapters/ch31-interpolation-and-gridding.md)).

The script below depends only on NumPy (rasterio is optional for GeoTIFF export). The truth is a sum of a regional tilt, a spectrally synthesized fractal surface (Hurst exponent 0.8, typical of real terrain), two Gaussian hills, a sinuous channel, and a sharp terrace. The error field has six labelled components so students can reason about which statistic detects which component: a constant bias (datum offset), a planar tilt (boresight-like), periodic stripes (strip adjustment residuals), white noise, spatially correlated noise, and sparse blunders. The "observed" grid is additionally shifted horizontally by a sub-cell amount, so the apparent vertical error includes the slope-dependent term that co-registration should remove.

> **Try it.** Save as `synthetic_terrain.py` and run `python synthetic_terrain.py --size 512 --out demo`. Console output for seed 42, size 512 (verified at writing): component σ of bias 0 (constant), tilt 0.165 m, stripes 0.200 m, noise 0.120 m, correlated 0.250 m, blunders ≈ 0.20 m; overall mean +0.350 m (the injected bias), σ ≈ 0.60 m (inflated above the ≈ 0.43 m error-field σ by the slope × shift term), RMSE ≈ 0.70 m, NMAD ≈ 0.45 m (smaller than σ because of blunders and the shift), LE95 ≈ 1.08 m. Then: (1) estimate and remove the shift with `xdem.coreg.NuthKaab` and confirm σ drops toward ≈ 0.43 m (= √(0.165² + 0.20² + 0.12² + 0.25²) plus blunders); (2) regress the residual on x and y to recover the tilt coefficients (1.0 × 10⁻³ and −0.5 × 10⁻³); (3) compute a variogram and recover the correlation length; (4) remove the voids by interpolation and measure error vs distance to the nearest valid cell.

```python
"""synthetic_terrain.py — synthetic DEM with known truth plus an injected error
field, for testing interpolation, co-registration, change detection and
accuracy-assessment code.  Requires numpy; rasterio optional for GeoTIFF.

Usage: python synthetic_terrain.py [--size 512] [--cell 1.0] [--seed 42]
                                   [--shift 0.6 -0.4] [--out prefix]
Outputs: <prefix>_truth.npy, _observed.npy, _error.npy, _mask.npy
         (+ _truth.tif, _observed.tif if rasterio is installed)
"""
import argparse
import numpy as np


def fractal_surface(n, hurst=0.8, rng=None):
    """fBm-like surface by spectral synthesis: PSD ~ k^-(2H+2)."""
    rng = rng or np.random.default_rng()
    kx = np.fft.fftfreq(n)[:, None]
    ky = np.fft.fftfreq(n)[None, :]
    k = np.sqrt(kx**2 + ky**2)
    k[0, 0] = 1.0
    amp = k ** (-(2 * hurst + 2) / 2.0)
    amp[0, 0] = 0.0
    phase = np.exp(2j * np.pi * rng.random((n, n)))
    z = np.real(np.fft.ifft2(amp * phase))
    return (z - z.mean()) / z.std()


def gaussian_hill(n, cell, x0, y0, sx, sy, h):
    y, x = np.mgrid[0:n, 0:n] * cell
    return h * np.exp(-(((x - x0) ** 2) / (2 * sx**2) + ((y - y0) ** 2) / (2 * sy**2)))


def make_truth(n, cell, rng):
    """Regional tilt + fractal roughness + two hills + sinuous channel + terrace."""
    y, x = np.mgrid[0:n, 0:n] * cell
    L = n * cell
    z = 100.0 + 0.02 * x + 0.005 * y                       # 2 % east, 0.5 % north
    z += 8.0 * fractal_surface(n, hurst=0.8, rng=rng)      # roughness, σ = 8 m
    z += gaussian_hill(n, cell, 0.30 * L, 0.35 * L, 0.08 * L, 0.06 * L, 40.0)
    z += gaussian_hill(n, cell, 0.70 * L, 0.65 * L, 0.05 * L, 0.10 * L, 25.0)
    cx = 0.5 * L + 0.15 * L * np.sin(2 * np.pi * y / L)    # channel centreline
    z += -6.0 * np.exp(-((x - cx) ** 2) / (2 * (0.01 * L) ** 2))
    z += np.where(x > 0.8 * L, 3.0, 0.0)                   # 3 m terrace step
    return z


def make_error(n, cell, rng):
    """Injected error with six labelled components (metres)."""
    y, x = np.mgrid[0:n, 0:n] * cell
    L = n * cell
    e = {}
    e["bias"] = np.full((n, n), 0.35)                                  # datum offset
    e["tilt"] = 1.0e-3 * (x - L / 2) - 0.5e-3 * (y - L / 2)            # boresight-like ramp
    e["stripes"] = 0.20 * np.sign(np.sin(2 * np.pi * x / (0.1 * L)))   # strip steps
    e["noise"] = rng.normal(0.0, 0.12, (n, n))                         # white, σ = 12 cm
    e["correlated"] = 0.25 * fractal_surface(n, hurst=0.5, rng=rng)    # correlated, σ = 25 cm
    blund = np.zeros((n, n))                                           # 0.05 % blunders
    nb = max(1, int(0.0005 * n * n))
    idx = rng.choice(n * n, nb, replace=False)
    blund.flat[idx] = rng.choice([-1, 1], nb) * rng.uniform(2, 15, nb)
    e["blunders"] = blund
    return sum(e.values()), e


def inject_voids(n, rng, frac=0.01, patches=6):
    """Rectangular voids (water, occlusion) covering ~frac of the area."""
    mask = np.zeros((n, n), dtype=bool)
    side = int(np.sqrt(frac * n * n / patches))
    for _ in range(patches):
        r, c = rng.integers(0, n - side, 2)
        mask[r:r + side, c:c + side] = True
    return mask


def horizontal_shift(z, dx_cells, dy_cells):
    """Sub-cell shift via Fourier phase ramp (periodic edges)."""
    n = z.shape[0]
    kx = np.fft.fftfreq(n)[None, :]
    ky = np.fft.fftfreq(n)[:, None]
    Z = np.fft.fft2(z) * np.exp(-2j * np.pi * (kx * dx_cells + ky * dy_cells))
    return np.real(np.fft.ifft2(Z))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=512)
    ap.add_argument("--cell", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--shift", type=float, nargs=2, default=(0.6, -0.4),
                    help="mis-registration of the observed grid, in cells (dx dy)")
    ap.add_argument("--out", default="synthetic")
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)

    truth = make_truth(a.size, a.cell, rng)
    err_total, parts = make_error(a.size, a.cell, rng)
    observed = horizontal_shift(truth, *a.shift) + err_total
    mask = inject_voids(a.size, rng)
    observed[mask] = np.nan

    np.save(f"{a.out}_truth.npy", truth)
    np.save(f"{a.out}_observed.npy", observed)
    np.save(f"{a.out}_error.npy", observed - truth)
    np.save(f"{a.out}_mask.npy", mask)

    d = (observed - truth)[~mask]
    nmad = 1.4826 * np.median(np.abs(d - np.median(d)))
    print(f"cells={a.size}x{a.size} cell={a.cell} m voids={mask.mean()*100:.2f} %")
    print("component σ (m): " + ", ".join(f"{k}={v.std():.3f}" for k, v in parts.items()))
    print(f"observed-truth: mean={d.mean():+.3f} σ={d.std():.3f} "
          f"RMSE={np.sqrt(np.mean(d**2)):.3f} NMAD={nmad:.3f} "
          f"LE95={np.percentile(np.abs(d), 95):.3f}")

    try:
        import rasterio
        from rasterio.transform import from_origin
        tr = from_origin(500000.0, 4000000.0 + a.size * a.cell, a.cell, a.cell)
        prof = dict(driver="GTiff", height=a.size, width=a.size, count=1,
                    dtype="float32", crs="EPSG:32610", transform=tr,
                    nodata=-9999.0, tiled=True, compress="deflate")
        for name, arr in (("truth", truth), ("observed", observed)):
            with rasterio.open(f"{a.out}_{name}.tif", "w", **prof) as dst:
                dst.write(np.where(np.isnan(arr), -9999.0, arr).astype("float32"), 1)
        print("GeoTIFFs written (EPSG:32610, synthetic origin).")
    except ImportError:
        print("rasterio not installed: wrote .npy only.")


if __name__ == "__main__":
    main()
```

Extensions that make useful assignments:

- **Simulated lidar strips with boresight error.** Sample the truth along parallel flight lines with a scan pattern, apply a small roll error (e.g. 0.01°) to alternate strips, and ask students to detect it from strip-overlap height differences as a function of across-track distance (expected: a linear ramp of 0.01° × range ≈ 17 cm at 1,000 m) and to estimate the roll angle by least squares ([Chapter 18](../chapters/ch18-topographic-lidar.md), [Chapter 25](../chapters/ch25-calibration-infrastructure.md)).
- **Simulated MBES with sound-speed error.** Ray-trace beams through a two-layer water column with a 2 m/s error in the surface sound speed; show the "smile/frown" of the outer beams (depth error growing with beam angle, ≈ 0.1–0.3 % of depth at 60° for a few m/s error) and test whether crosslines catch it ([Chapter 20](../chapters/ch20-sonar.md)).
- **Resolution experiments.** Aggregate the truth to 2, 5, 10, 30 m by averaging and by point sampling; compute slope and curvature at each; plot the resolution dependence ([Chapter 44](../chapters/ch44-resolution-and-sampling.md)).
- **Interpolation across voids.** Enlarge the void patches; compare TIN linear, IDW, spline, and kriging reconstructions against truth as a function of distance to the nearest valid cell ([Chapter 31](../chapters/ch31-interpolation-and-gridding.md), [Chapter 35](../chapters/ch35-voids-and-overhangs.md)).
- **Change detection with LoD.** Generate a second epoch by adding a localized "landslide" (negative Gaussian on a slope and matching positive deposit below) and independent error fields; recover the volume with and without co-registration; compute the uncertainty interval using the correlated-error formula ([Chapter 41](../chapters/ch41-change-detection.md) §41.8).
- **Datum mistakes.** Add a smooth "geoid" surface (e.g. 30 m + 0.002 x) to one epoch only and show that the hillshade looks identical while every difference is wrong ([Chapter 9](../chapters/ch09-vertical-datums.md)).

Other synthetic-terrain tools: Landlab (process-based landscapes), `noise`/`opensimplex` Python packages (Perlin/simplex fractals), the diamond–square algorithm (simple but with known grid artefacts — themselves a teaching point), and GMT's `grdmath` with `RAND`/`NRAND` and `grdfilter` for correlated fields. Synthetic terrain should never be mixed with real data in a catalog without an explicit "synthetic" flag ([Chapter 45](../chapters/ch45-super-resolution.md) §45.4, [Chapter 73](../chapters/ch73-open-problems.md)).

## H.7 Licensing notes and practical advice

- Datasets labelled "research use" (ISPRS, DFC, several deep-learning benchmarks) typically forbid commercial use and redistribution; do not bundle them in public course repositories — link instead.
- CC BY-NC-SA datasets (DALES, SensatUrban, FABDEM) contaminate derivatives: a model trained on them is arguably NC-SA too ([Chapter 68](../chapters/ch68-legal-issues.md) §68.3).
- Public-domain US federal data (3DEP, NOAA, USGS, NASA) can be redistributed freely; cite anyway, and keep the acquisition metadata with your copy.
- Large downloads: use cloud-native access (EPT/COPC via PDAL `readers.ept`/`readers.copc`, COG via `/vsicurl/`, STAC search) rather than bulk tile downloads ([Chapter 51](../chapters/ch51-finding-data.md)).
- Record the version and download date of every dataset used in an exercise: ICESat-2 products are reissued (ATL06 v006 vs v005 differ), global DEMs are re-released, and national lidar composites are refreshed yearly.

## H.8 References

- Guth, P. L., et al. (2024). Ranking of 1 arc-second global DEMs with the DEMIX wine contest. *Transactions in GIS* (verify volume/pages) and related DEMIX documentation on GitHub.
- Hu, Q., et al. (2021). Towards semantic segmentation of urban-scale 3D point clouds: A dataset, benchmarks and challenges (SensatUrban). *CVPR 2021*.
- Kölle, M., et al. (2021). The Hessigheim 3D (H3D) benchmark on semantic segmentation of high-resolution 3D point clouds and textured meshes from UAV LiDAR and multi-view-stereo. *ISPRS Open Journal of Photogrammetry and Remote Sensing*, 1:100001.
- Le Saux, B., et al. (2019). 2019 Data Fusion Contest (US3D). *IEEE GRSS*. (verify)
- Neuenschwander, A., & Pitts, K. (2019). The ATL08 land and vegetation product for the ICESat-2 mission. *Remote Sensing of Environment*, 221:247–259.
- Peters, R., et al. (2022). Automated 3D reconstruction of LoD2 and LoD1 models for all 10 million buildings of the Netherlands (3D BAG). *Photogrammetric Engineering & Remote Sensing*, 88(3):165–170.
- Qin, N., et al. (2021). OpenGF: An ultra-large-scale ground filtering dataset built upon open ALS point clouds around the world. *CVPRW 2021*.
- Rottensteiner, F., et al. (2014). Results of the ISPRS benchmark on urban object detection and 3D building reconstruction. *ISPRS Journal of Photogrammetry and Remote Sensing*, 93:256–271.
- Sithole, G., & Vosselman, G. (2004). Experimental comparison of filter algorithms for bare-Earth extraction from airborne laser scanning point clouds. *ISPRS Journal of Photogrammetry and Remote Sensing*, 59(1–2):85–101.
- Tan, W., et al. (2020). Toronto-3D: A large-scale mobile LiDAR dataset for semantic segmentation of urban roadways. *CVPRW 2020*.
- Varney, N., Asari, V. K., & Graehling, Q. (2020). DALES: A large-scale aerial LiDAR data set for semantic segmentation. *CVPRW 2020*.
- Saupe, D. (1988). Algorithms for random fractals. In Peitgen & Saupe (eds.), *The Science of Fractal Images*. Springer. (spectral synthesis of fBm)
- Wheaton, J. M., et al. (2010). Accounting for uncertainty in DEMs from repeat topographic surveys: improved sediment budgets. *Earth Surface Processes and Landforms*, 35(2):136–156.

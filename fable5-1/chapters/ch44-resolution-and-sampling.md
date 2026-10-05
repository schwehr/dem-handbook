# Chapter 44 — Resolution, pixel size, sampling, and oversampling

> **Part IX — Semantics, learning, and enhancement.** The chapter that defines what "resolution" can honestly mean for points and grids, why the number in the filename and the information in the file differ, and how every derivative—slope, curvature, flow, viewshed—inherits that difference; it sets up the enhancement claims of [Chapter 45](ch45-super-resolution.md).

**In this chapter.** "30 m DEM" is a statement about a grid, not about the terrain it resolves. You will be able to distinguish ground sample distance, post spacing, point density and spacing, footprint, and effective resolution, and compute the nominal pulse spacing and density that the USGS Lidar Base Specification uses; apply the Nyquist–Shannon theorem to terrain and recognise aliasing and footprint anti-aliasing in real products; estimate effective resolution from power spectra and from product lineage (Copernicus from TanDEM-X, ASTER GDEM's ~70–100 m, SRTM's smoothing); recognise oversampling and say when it is legitimate; predict how slope, curvature, roughness, wetness index, viewshed, and flow accumulation change with cell size, with a worked example you can reproduce; choose a resolution for a purpose from hydrologic, navigational, and feature-detection requirements; and report resolution correctly, including the pixel-is-area/pixel-is-point convention whose half-cell shift still misregisters products.

## 44.1 Definitions

Five quantities are routinely called "resolution", and they are different things.

**Ground sample distance (GSD)** is the distance on the ground between adjacent sample centres of a sensor—the pixel pitch projected to the surface for a camera, the range-bin or azimuth spacing for a radar. It is a property of the acquisition. **Post spacing** (or **grid spacing**, **cell size**) is the distance between adjacent nodes of a gridded product; it is a property of the file and can be set to anything by resampling. **Point density** (points per square metre) and **point spacing** (metres between points) describe a point cloud; for a roughly uniform distribution, spacing ≈ $1/\sqrt{\text{density}}$, so 2 pts/m² ≈ 0.71 m spacing and 8 pts/m² ≈ 0.35 m. **Footprint** is the area on the ground over which a single measurement integrates: the laser beam diameter (divergence × range; 0.25 mrad at 1,500 m gives ~0.4 m), the sonar beam footprint (beamwidth × depth; a 1° beam at 100 m depth gives ~1.7 m across-track at nadir and wider off-nadir), the radar resolution cell, the stereo-matching window. **Effective resolution** (also "true", "intrinsic", or "actual" resolution) is the smallest feature the data can actually distinguish; it is a property of the information, and it is never finer than the post spacing and usually coarser.

The USGS Lidar Base Specification formalises the point-cloud quantities as **nominal pulse spacing (NPS)** and **nominal pulse density (NPD)**—computed from first returns in single-swath, non-overlap areas, so that overlap and multiple returns do not inflate the number—and sets per-quality-level requirements: QL0 and QL1 ≥ 8 pulses/m² (NPS ≤ 0.35 m), QL2 ≥ 2 pulses/m² (NPS ≤ 0.71 m), QL3 ≥ 0.5 pulses/m² (NPS ≤ 1.41 m), with the DEM cell size for each level set so that it is supported by the data (1 m for QL2 is the common 3DEP product; check the current LBS revision for exact values). Density must also be *spatially uniform*: the specification tests the fraction of 2 m × 2 m (or similar) cells meeting the required count, because a mean density of 2 pts/m² produced by 6 pts/m² in overlap and 0.5 pts/m² between lines does not support a 1 m DEM.

For sonar, the relevant comparison is **beam footprint versus grid size**. A multibeam system with 1° × 1° beams in 50 m of water has a nadir footprint of ~0.9 m and an outer-swath footprint (at 60° from nadir) of several metres across-track; gridding the swath at 0.5 m claims detail the outer beams cannot support. CUBE and variable-resolution surfaces ([Chapter 20](ch20-sonar.md), §44.7) exist to make the grid follow the footprint and density rather than the other way round.

> **Definitions that bite.** "1 m lidar DEM" can mean (a) a grid with 1 m posts built from ≥ 8 pts/m² data, in which 1–2 m features are resolved; (b) a grid with 1 m posts built from 2 pts/m² data, in which features smaller than ~2–3 m are interpolation; or (c) a grid with 1 m posts resampled from a 5 m product, in which nothing smaller than ~10 m is real. All three have the same cell size in the GeoTIFF header. Only (a) is a 1 m DEM in the sense a user means.

## 44.2 Sampling theory and terrain

### 44.2.1 Nyquist–Shannon

The sampling theorem (Nyquist 1928; Shannon 1949 ⟨H⟩) states that a signal containing no frequencies above $f_{\max}$ is completely determined by samples spaced $\Delta \le 1/(2 f_{\max})$; equivalently, a grid with spacing $\Delta$ can represent terrain wavelengths no shorter than $\lambda_{\min} = 2\Delta$. For a 30 m grid, the shortest representable wavelength is 60 m; a feature is "resolved" in the weak sense if at least two samples fall across it, and in a practical sense (recognisable shape, measurable height) only if four or more do. This is why effective resolution is often quoted as 2–3 times the post spacing even for perfectly sampled data: the Nyquist limit is a bound on representability, not a guarantee of fidelity.

### 44.2.2 Aliasing in terrain

Terrain is not band-limited. Slope breaks, cliffs, channel banks, buildings, and furrows contain power at all wavelengths, so any sampling aliases: energy at wavelengths shorter than $2\Delta$ folds back into longer wavelengths and appears as spurious terrain. Point sampling of a ploughed field at 2 m spacing with 0.75 m furrow spacing produces a beat pattern of several metres wavelength that is not in the field; sampling a stepped urban DSM at 10 m produces blocky artefacts whose positions depend on where the grid happened to fall. In bathymetry, sand waves of 20 m wavelength sampled by survey lines 50 m apart alias into apparent bedforms of 33 m wavelength (the difference frequency), an effect that has produced spurious "migration" in repeat surveys ([Chapter 41](ch41-change-detection.md)).

### 44.2.3 Anti-aliasing by footprint

Real sensors do not point-sample; they integrate over a footprint, which acts as a low-pass filter before sampling. A footprint of width $w$ (modelled as a box) multiplies the terrain spectrum by $\mathrm{sinc}(\pi w f)$, suppressing wavelengths shorter than about $w$; a Gaussian footprint suppresses more gently. The **footprint–spacing ratio** $w/\Delta$ therefore controls aliasing: when $w \approx \Delta$ (a lidar with beam diameter equal to point spacing, a radar with resolution cell equal to post spacing) aliasing is modest; when $w \ll \Delta$ (a narrow-beam laser at sparse spacing, single-beam echo-sounder lines far apart) aliasing is severe; when $w \gg \Delta$ (oversampled grids, §44.4) there is no aliasing and no additional information either. SRTM's processing, which applied averaging to the interferometric data before posting, is a deliberate example of the first case and the reason its effective resolution is coarser than its 1″ posts (§44.3).

### 44.2.4 Point-to-grid aggregation as a filter

Converting points to a grid is itself a low-pass filter whose cut-off depends on the method ([Chapter 31](ch31-interpolation-and-gridding.md)). **Binning by mean** averages all points in a cell and is a box filter of width $\Delta$. **Binning by minimum** (common for bare-earth DTMs) or **maximum** (for DSMs and canopy) is nonlinear, biased by roughly one standard deviation of the within-cell variation in the chosen direction, and preserves extremes at the cost of a systematic offset. **Inverse-distance weighting** with a search radius $r$ smooths over ~$2r$. **TIN-linear** interpolation reproduces the points exactly and interpolates linearly between them; its effective resolution is the point spacing, and it aliases if the points are sparser than the terrain. **Kriging and splines** have an explicit smoothing parameter and, for kriging, a nugget that controls how much of the short-wavelength variance is treated as noise. A 1 m grid built from 2 pts/m² data by mean binning has empty cells; built by TIN it has a facet structure at 0.7 m scale that is interpolation, not terrain. The grid's resolution is the point spacing in either case; the file says 1 m.

<!-- figure: Figure 44.1 — A 100 m terrain profile with a 5 m sinusoid, sampled at 2, 10, 30, and 50 m spacing with and without footprint averaging, showing faithful reproduction, amplitude loss, aliasing to a longer wavelength, and total loss at the Nyquist limit. -->

## 44.3 Nominal versus effective resolution

The following products are widely used, and in each the effective resolution differs from the post spacing for a reason that can be traced in the lineage.

**Copernicus DEM (GLO-30 and GLO-90).** Derived from the TanDEM-X global DEM, which was produced at 12 m (0.4″) posting from bistatic X-band interferometry with an independent-pixel resolution close to its posting in most terrain. GLO-30 is produced by resampling to 1″ (~30 m) and GLO-90 to 3″. Because the source has finer independent resolution than the product, GLO-30's effective resolution is close to its nominal 30 m—this is why it outperforms other 1″ global DEMs in the DEMIX intercomparisons (Bielski et al. 2024; Guth et al. 2024). The caveat is that it is a DSM with editing, not a DTM, and its vertical error structure is set by X-band penetration and the edits, not by the sampling.

**ASTER GDEM (v2, v3).** Posted at 1″ but built by stacking many 15 m stereo pairs with a correlation window of several pixels and then averaging; validation found an effective horizontal resolution of roughly 70–100 m (the GDEM v2 validation report, Tachikawa et al. 2011, estimated ~72 m), and residual stacking artefacts ("mole runs") at the scale of the correlation window. A 30 m grid with 70–100 m information: roughly a 3× oversampled product.

**SRTM (1″ and 3″).** C-band interferometry at ~30 m ground-range resolution, with multi-look averaging and a final boxcar smoothing stage; Smith & Sandwell (2003) found SRTM coherent with the US National Elevation Dataset at wavelengths longer than ~200 m and poorer than NED below ~350 m wavelength, attributing the difference to the boxcar filter. The 1″ release (2014–15, "SRTM-GL1") carries the same information as the processed data posted at 3″ did in terms of short-wavelength content; the finer posting did not restore what the smoothing removed. Effective resolution is reasonably quoted as roughly 2–3 posts, i.e., 60–90 m at 1″.

**Satellite-derived bathymetry at "10 m".** An SDB product from Sentinel-2 inherits 10 m pixels, but the depth information in each pixel comes from a regression against sparse soundings and a water-column model whose spatial support is the atmospheric and water-column correction, often hundreds of metres to kilometres. Depth varies smoothly in the product not because the seafloor is smooth but because the information is ([Chapter 23](ch23-satellite-derived-bathymetry.md)). Gridding SDB at 10 m to match lidar and treating the two as equal is the pitfall this chapter is named for.

**"1 m lidar DEM" from 2 pts/m².** The 3DEP QL2 standard product: 0.71 m nominal spacing, ground returns sparser still under canopy (often < 1 pt/m² and sometimes < 0.1 pt/m²), gridded at 1 m. In the open, effective resolution is 1–2 m; under dense forest, the DTM is a smooth interpolation with effective resolution of 5–20 m and the 1 m posts are cosmetic. The product is honest about this in its metadata only if ground-point density is published alongside the DEM (§44.4).

### 44.3.1 Estimating effective resolution

Three methods are in use. **Spectral analysis** computes the power spectrum of the DEM (or of its difference from a finer reference) and finds the wavelength at which the spectrum departs from the terrain's characteristic power law and flattens into a noise floor, or at which coherence with the reference drops below 0.5 (Smith & Sandwell 2003); Grohmann (2015) used spectral and slope-based comparisons to show that products posted at the same spacing differ in information content. **Feature-based tests** measure the smallest features (gullies, roads, buildings, bedforms) detectable against a finer reference, which is how the GDEM team estimated ~72 m. **Geomorphometric intercomparison** (DEMIX; Guth et al. 2021, 2024; Bielski et al. 2024) scores DEMs on a battery of criteria—elevation, slope, roughness, and derived channel networks against lidar reference—over hundreds of tiles with a ranked block design, giving a statistical ranking rather than a single resolution number; its practical output is that Copernicus DEM is the best 1″ global product and that none of them resolves what their post spacing suggests in low-relief terrain.

> **Try it.** Estimate the effective resolution of a DEM by its radially averaged power spectrum. Expected outcome: a log–log spectrum that follows an approximate $1/f^{\beta}$ law at long wavelengths (β typically 2–3 for terrain) and flattens or rolls off at short wavelengths; the roll-off wavelength is a lower bound on effective resolution. Run on a lidar DTM and on SRTM over the same area and compare roll-offs.
>
> ```python
> import numpy as np, rasterio
> from numpy.fft import fft2, fftshift, fftfreq
>
> with rasterio.open("dem.tif") as src:
>     z = src.read(1, masked=True).filled(np.nan)
>     dx = src.res[0]                        # cell size in map units (m)
> z = z[:1024, :1024]; z = z - np.nanmean(z); z = np.nan_to_num(z)
> win = np.outer(np.hanning(z.shape[0]), np.hanning(z.shape[1]))
> P = np.abs(fftshift(fft2(z * win)))**2
> fy = fftshift(fftfreq(z.shape[0], dx)); fx = fftshift(fftfreq(z.shape[1], dx))
> FX, FY = np.meshgrid(fx, fy); fr = np.hypot(FX, FY)
> bins = np.logspace(np.log10(1/(z.shape[0]*dx)), np.log10(0.5/dx), 40)
> idx = np.digitize(fr, bins)
> Pr = np.array([P[idx == i].mean() if np.any(idx == i) else np.nan for i in range(1, len(bins))])
> fc = np.sqrt(bins[1:] * bins[:-1])
> for f, p in zip(fc, Pr):
>     print(f"wavelength {1/f:8.1f} m   power {p:10.3e}")
> ```
>
> Fit a line to log(power) vs log(frequency) over the long-wavelength half; where the measured spectrum first falls more than ~3 dB below (roll-off) or rises above (noise floor) that line, read the wavelength. For SRTM 1″ expect a roll-off near 100–200 m; for a QL2 lidar DTM in open terrain, near 2–4 m.


## 44.4 Oversampling

**Oversampling** is gridding finer than the information supports: a 1 m grid from 5 m data, a 10 m SDB grid from kilometre-scale information, a 0.25 m orthophoto DSM from 1 m stereo matching. The result is smooth, visually continuous, and contains no detail finer than the source; every added cell is an interpolation whose value is determined by its neighbours.

Oversampling has legitimate uses. **Visual continuity**: a hillshade of a 30 m DEM resampled bicubically to 10 m looks less blocky and is easier to read, provided the legend says what was done ([Chapter 57](ch57-visualizing-dems.md)). **Matching another grid**: differencing, compositing, and mosaicking require common grids, and resampling the coarser product to the finer grid is often preferable to degrading the finer one—as long as the uncertainty of the resampled product is carried along and the difference is interpreted at the coarser resolution ([Chapter 48](ch48-compositing.md)). **Numerical stability**: some hydraulic and geotechnical models need cell sizes smaller than the data resolution for the scheme to converge, and interpolating the terrain is the correct way to supply them, with the understanding that the terrain is still known only at the coarser scale.

The illegitimate use is **implying detail**: distributing a resampled product with the cell size of the output and the metadata of nothing, so that the next user reads 1 m and assumes 1 m. The failure is common because resampling is one command and because finer grids look better. The remedies are procedural. Store the **source density or source resolution** as a companion layer or metadata field: for lidar DEMs, a ground-point-density raster at the DEM cell size (or at a coarser aggregation) tells a user where the 1 m posts are supported and where they are not; for composite products, a source-ID raster (GEBCO's type-identifier grid, the 3DEP project-boundary layer) does the same by lineage. Write the effective resolution, not only the cell size, in the ISO 19115 resolution fields (§44.8). And when oversampling for one of the legitimate reasons, inflate the stated uncertainty of the output to that of the source and say in the lineage that the grid was resampled, from what, with which kernel.

> **Rule of thumb.** A gridded product's effective resolution is at least the larger of (a) twice the mean spacing of the measurements that fed it, (b) the measurement footprint, and (c) the aggregation or smoothing window used to build it. Report the largest of the three, not the cell size. The rule breaks down where density is non-uniform—use the local (e.g., per-100 m-cell) spacing, not the mean—and where the gridding method is nonlinear (min/max binning), which preserves extremes at finer scales than the rule implies while biasing them.

## 44.5 Resolution dependence of derivatives

Every quantity derived from a DEM by differencing or neighbourhood analysis is a function of the cell size as much as of the terrain. This is not an error; it is the definition of a scale-dependent quantity. It becomes an error when results computed at different resolutions are compared, or when a resolution is chosen without regard to the process being modelled.

**Slope** decreases as cell size increases, because finite differences across a longer baseline average the gradient over more terrain and because short-wavelength relief is smoothed away. Zhang & Montgomery (1994) showed, for two catchments in California and Oregon with 2 m to 90 m grids, that mean slope decreased and the slope distribution narrowed systematically as cell size grew, and that hydrologic model outputs sensitive to slope (topographic index, saturation extent) changed accordingly; they argued that a 10 m grid was a reasonable compromise for hillslope hydrology, finer than the then-standard 30 m and coarser than the data could support in most places. Grohmann (2015) extended the analysis to regional scales with SRTM, ASTER, and lidar resampled over 10 m to 1 km and found steep slopes most affected—a 30° slope at 10 m may be 20° at 90 m and 10° at 500 m—with the loss largest in dissected terrain. Kienzle (2004) and Florinsky & Kuryakova (2000) reported the same monotonic behaviour and proposed methods to choose cell size from the terrain's own characteristic lengths.

**Curvature** (profile, plan, total) is a second derivative and is more sensitive still: it scales roughly as $1/h^2$ in its noise response and converges to zero for all terrain as $h$ grows. Curvature maps at 1 m from lidar show micro-topography (furrows, tyre tracks, vegetation residuals); at 30 m they show hillslope convexity; the two are different quantities that share a name. **Roughness** (standard deviation of elevation or of residuals from a plane within a window) depends on both cell size and window size and must be reported with both. The **topographic wetness index** $\mathrm{TWI} = \ln(a / \tan\beta)$ combines specific catchment area $a$ (which increases with cell size because the unit contour length is the cell width) and slope $\tan\beta$ (which decreases), so TWI increases systematically with coarser grids and its distribution shifts; Zhang & Montgomery's results showed exactly this. **Flow accumulation** and the derived channel network depend on cell size through the flow-routing algorithm (D8 routes to one of eight neighbours, so flow paths are quantised to 45°) and through what the DEM resolves: a 10 m grid cannot represent a 3 m levee or a 1.5 m culvert, so the modelled water flows over the levee and is blocked by the road embankment, producing a flood that cannot happen or one that cannot be stopped ([Chapter 61](ch61-hydrology.md)). Hydro-enforcement ([Chapter 34](ch34-water-in-dems.md)) exists to restore the connectivity the resolution removed. **Viewshed** depends on resolution through the terrain horizon: coarser cells smooth the ridgelines that define the horizon, generally increasing the visible area, and the observer height relative to the cell introduces its own artefacts.

**Feature detectability** follows directly: a feature of width $w$ and height $\Delta z$ is detectable when at least 2–4 cells span $w$ and $\Delta z$ exceeds the local noise. A 1 m-wide, 0.5 m-high drainage ditch is visible at 0.5 m, marginal at 1 m, and absent at 2 m regardless of vertical accuracy.

> **Worked example.** Take terrain $z(x) = A \sin(2\pi x / L)$ with amplitude $A = 5$ m and wavelength $L = 100$ m—a train of low ridges. The true maximum slope is $2\pi A / L = 0.314$ (17.4°). A central-difference slope estimate at spacing $h$ has maximum $\frac{A \sin(2\pi h / L)}{h} = \frac{2\pi A}{L} \cdot \frac{\sin(2\pi h/L)}{2\pi h/L}$. Evaluating the bracketed factor:
>
> | Cell size $h$ | Sampling factor $\frac{\sin(2\pi h/L)}{2\pi h/L}$ | Max slope | With box footprint of width $h$ (× $\frac{\sin(\pi h/L)}{\pi h/L}$) |
> |---|---|---|---|
> | 1 m | 0.999 | 0.314 (17.4°) | 0.314 (17.4°) |
> | 5 m | 0.984 | 0.309 (17.2°) | 0.304 (16.9°) |
> | 10 m | 0.935 | 0.294 (16.4°) | 0.289 (16.1°) |
> | 30 m | 0.505 | 0.159 (9.0°) | 0.136 (7.8°) |
> | 50 m | 0.000 | 0.000 (0°) | 0.000 (0°) |
>
> At 30 m—the nominal spacing of SRTM and Copernicus—the slope of a 100 m-wavelength ridge is halved by sampling alone and reduced to 43 % when the sensor footprint also averages; at 50 m, the Nyquist limit, the ridges vanish. Real terrain superposes many wavelengths, so the slope loss is a weighted average of these factors over the terrain spectrum; steep, finely dissected terrain (power at short wavelengths) loses most, which is Grohmann's result. The arithmetic also shows why a slope map from a 30 m DEM must not be compared with one from a 1 m DTM without stating the scale.

## 44.6 Choosing resolution for a purpose

Resolution is bought per unit area, roughly as $1/\Delta^2$ in storage and processing and more steeply in acquisition (a QL1 lidar survey at 8 pts/m² costs several times a QL2 survey at 2 pts/m² over the same area; sonar coverage time scales with the inverse of swath width, which is set by depth, not by the grid). The question is therefore what the use requires, and [Chapter 3](ch03-fitness-for-use.md) gives the general method; the resolution-specific points are these.

**Hydrology and hydraulics** require that the features controlling flow be resolved: channel width (≥ 3–4 cells across the channel), levee and road-embankment crests (cells narrower than the crest), culverts and bridges (which cannot be resolved by any practical grid and must be enforced as breaklines or structures). For urban pluvial flooding this means 1–2 m; for rural floodplain inundation 5–10 m with enforced structures; for continental-scale routing 30–90 m with the understanding that local connectivity is parameterised rather than resolved.

**Navigation and charting** specify not resolution but **feature detection**: IHO S-44 Ed. 6.1.0 requires that cubic features of 0.5 m (Exclusive Order), 1 m (Special Order), or 2 m (Order 1a, in depths to 40 m; 10 % of depth beyond) be detected, which translates into a sounding density and beam footprint requirement per depth ([Chapter 20](ch20-sonar.md)). For aviation, ICAO Annex 15 and PANS-AIM define electronic terrain and obstacle data (eTOD) areas with post spacings of 3″ (Area 1), 1″ (Area 2), 0.6″ (Area 3), and 0.3″ (Area 4), with obstacle data collected to stated height thresholds rather than grid sizes ([Chapter 62](ch62-navigation-and-charting.md)).

**Geomorphology and geology** need the process scale: landslide scarps and gullies at 1–2 m, hillslope form at 5–10 m, drainage-basin morphometry at 30 m, tectonic geomorphology at 30–90 m. Tarolli (2014) reviews what high-resolution topography made newly visible and where it adds noise rather than information.

**Change detection** needs the finer of the two epochs' effective resolutions to be degraded to the coarser before differencing, and the minimum detectable change computed at that scale ([Chapter 41](ch41-change-detection.md)).

The practical procedure is: list the features that must be represented and their widths; divide the smallest width by three to four for the required cell size; check that the acquisition footprint and density support it (§44.1); confirm that the vertical accuracy at that cell size still resolves the heights that matter; and cost it. Where the answer is unaffordable, choose a coarser product and enforce the critical features as vectors rather than pretending the grid contains them.

## 44.7 Multi-resolution representation

A single grid at a single resolution is the simplest representation and often the wrong one for data whose information content varies in space. **Overviews or pyramids** (GeoTIFF/COG internal overviews, `gdaladdo`) store successively coarser versions of a grid for display and fast access; they are a performance structure, not a resolution statement, and the choice of downsampling kernel (nearest, average, Gaussian) matters for what the coarser levels mean—`average` is a box filter; `nearest` aliases ([Chapter 46](ch46-data-models.md)). **Variable-resolution grids** store different cell sizes in different regions according to data support: the BAG variable-resolution extension (VR BAG) and CUBE-based "supergrid" surfaces in hydrographic software let the cell size follow depth and density so that shallow, dense areas are gridded at 0.5 m and deep, sparse areas at 8 m within one surface, each cell carrying its own uncertainty ([Chapter 47](ch47-file-formats.md)). **Adaptive TINs** place vertices where the terrain demands them, so that resolution is implicitly variable; they are the natural representation of lidar ground points before gridding and of breakline-constrained surfaces.

**Honest resampling when mixing** is the rule that makes multi-resolution work in practice. When a 1 m lidar DTM and a 30 m SRTM tile are composited, the output is either a 30 m product (lidar degraded by averaging, with its finer information discarded but its accuracy retained) or a 1 m product in which the SRTM region is oversampled and must be flagged as such with uncertainty appropriate to 30 m data. The seam between them is a change in effective resolution as well as in accuracy, and derivative maps (slope, curvature) will show it as a texture boundary. [Chapter 48](ch48-compositing.md) gives the compositing procedures; the resolution-specific requirement is that the output carry a source-resolution layer.

## 44.8 Reporting resolution

**ISO 19115-1** provides `MD_Resolution` with alternatives: `equivalentScale` (a representative fraction, e.g., 1:24,000—meaningful for maps, nearly meaningless for grids), `distance` (a ground distance with units, the right field for post spacing), `vertical` (vertical resolution, usually the quantisation step), `angularDistance` (for geographic grids: 1″), and `levelOfDetail` (free text). The `distance` field should carry the post spacing; the effective resolution, if different, belongs in the lineage statement and in a `DQ_` quality element, because ISO has no dedicated field for it ([Chapter 49](ch49-metadata.md)). STAC's `raster:spatial_resolution` and `gsd` fields carry only the nominal value; a product's effective resolution must be stated in the description and in a custom property if it is to survive a catalogue search ([Chapter 51](ch51-finding-data.md)).

**Pixel-is-area versus pixel-is-point.** GeoTIFF (OGC GeoTIFF 1.1, `GTRasterTypeGeoKey`) distinguishes `RasterPixelIsArea` (code 1; the pixel is a cell whose georeferenced coordinate refers to its upper-left corner, and the elevation value represents the cell) from `RasterPixelIsPoint` (code 2; the value is a point sample located at the georeferenced coordinate, which is the cell centre). SRTM, ASTER GDEM, and many geographic-grid products are pixel-is-point: the 1″ posts sit on the integer-second graticule, and the cell "covers" ±0.5″ around each post. Most projected lidar DEMs are pixel-is-area. The difference is exactly half a cell in each axis. Software that reads a pixel-is-point file as pixel-is-area (or the reverse) shifts the data by half a cell—15 m for 1″ products—and the shift appears as a systematic slope-correlated elevation error when the product is differenced against another: on a 10° slope, 15 m of horizontal shift is 2.6 m of vertical error, larger than the stated accuracy of every global DEM. GDAL honours the key and reports it in `gdalinfo` as `AREA_OR_POINT=Area|Point`; some tools ignore it, and some products have had it set wrong. [Chapter 31](ch31-interpolation-and-gridding.md) treats the resulting registration problem and [Chapter 41](ch41-change-detection.md) its consequences for differencing.

What to report with any gridded elevation product, then: cell size and its units; the pixel-is-area/point convention and the grid origin; the source measurement density or footprint; the gridding method and any smoothing window; the estimated effective resolution and how it was estimated; and, where density varies, a density or source raster.

<!-- figure: Figure 44.2 — Slope maps of the same hillslope from a 1 m lidar DTM and from the same DTM aggregated to 5, 10, 30, and 90 m, with the slope histogram for each; and an inset showing the half-cell shift between a pixel-is-point and a pixel-is-area reading of a 1″ tile. -->


## Then & now

- **Contour interval as the resolution surrogate ⟨H⟩.** On paper maps the vertical interval and the map scale together implied what terrain could be shown: a 1:24,000 sheet with a 20-ft (6.1 m) interval resolved features of roughly that height and of widths near the plotting limit (~0.2 mm at scale, 5 m on the ground). "Resolution" was a cartographic property, and users read it from the legend.
- **Raster post spacing ⟨H⟩.** DTED (US Defense Mapping Agency, 1970s onward) fixed the vocabulary of posts: Level 0 at 30″ (~1 km), Level 1 at 3″ (~90 m), Level 2 at 1″ (~30 m); the USGS DEM series followed with 30 m and later 10 m products. Post spacing became the number everyone quoted, and the distinction from information content was lost for a generation.
- **Shannon's theorem ⟨H⟩ (1949)** gave the formal limit—two samples per shortest wavelength—and the signal-processing community applied it to images; its application to terrain grids came later and is still not routine in metadata.
- **Point density specifications (2000s–).** Airborne lidar made density the primary specification: the USGS LBS (2012; current 2024 rev. A) defined NPS/NPD and the QL0–QL3 ladder; IHO S-44 defined bathymetric coverage and feature detection by order rather than by grid.
- **Effective-resolution metrics (2003–).** Smith & Sandwell's spectral coherence analysis of SRTM (2003), the GDEM validation team's ~72 m estimate (2011), Grohmann's slope-based comparison (2015), and the DEMIX intercomparison (2021–2024) made effective resolution a measured quantity—one that still rarely appears in product metadata.

## Mathematics

**Sampling theorem.** A signal $z(x)$ with Fourier transform $Z(f) = 0$ for $|f| > f_{\max}$ is exactly recoverable from samples $z(n\Delta)$ if $\Delta \le 1/(2 f_{\max})$:
$$z(x) = \sum_{n} z(n\Delta)\,\mathrm{sinc}\!\left(\frac{x - n\Delta}{\Delta}\right), \qquad \mathrm{sinc}(u) = \frac{\sin \pi u}{\pi u}.$$
For frequencies above the Nyquist frequency $f_N = 1/(2\Delta)$, a component at $f$ aliases to $|f - k/\Delta|$ for the integer $k$ that brings it into $[0, f_N]$; two bedform fields with wavelengths $\lambda_1$ and sampling $\Delta$ produce an alias at wavelength $1/|1/\lambda_1 - 1/\Delta|$.

**Footprint as modulation transfer function.** A measurement that averages uniformly over a footprint of width $w$ has impulse response $\Pi(x/w)/w$ and MTF $|\mathrm{sinc}(w f)|$; a Gaussian footprint of standard deviation $\sigma_w$ has MTF $\exp(-2\pi^2 \sigma_w^2 f^2)$. The product of the footprint MTF, the aggregation MTF (a box of width $\Delta$ for mean binning), and any smoothing MTF is the system MTF; the effective resolution is conventionally the wavelength at which it falls to 0.5 (or to $1/e$ or 0.1 by other conventions—state which).

**Slope from finite differences.** Horn's (1981) operator estimates the gradient at cell $(i,j)$ from the 3 × 3 neighbourhood with cell size $h$:
$$\frac{\partial z}{\partial x} \approx \frac{(z_{i+1,j+1} + 2 z_{i+1,j} + z_{i+1,j-1}) - (z_{i-1,j+1} + 2 z_{i-1,j} + z_{i-1,j-1})}{8h},$$
and similarly for $y$; slope is $\arctan\sqrt{z_x^2 + z_y^2}$. For a sinusoid of wavelength $L$ the estimate's amplitude is the true amplitude times $\frac{\sin(2\pi h/L)}{2\pi h/L}$ (central difference) with an additional cross-row averaging factor for Horn's weights when the terrain varies in $y$. For white vertical noise of variance $\sigma_z^2$, the variance of the central-difference gradient is $\sigma_z^2 / (2h^2)$, so slope noise grows as $1/h$ while slope signal falls with $h$: there is an optimal cell size for slope that depends on the terrain spectrum and the noise ([Chapter 5](ch05-error-and-uncertainty.md)).

**Terrain power spectra.** Terrain power spectral density is approximately a power law, $P(f) \propto f^{-\beta}$ with $\beta$ typically between 2 and 3 (β = 2 corresponds to a Brownian surface; higher β is smoother). Measurement noise with variance $\sigma_n^2$ contributes a flat floor $P_n = \sigma_n^2 \Delta^2$ (two-dimensional, per unit frequency area). The frequency at which $P(f) = P_n$ is the scale below which the grid contains more noise than terrain; the corresponding wavelength is a defensible estimate of effective resolution for noisy products.

**Effective resolution from slope comparison (Grohmann 2015).** For a DEM $D$ and a reference $R$ at common cell size $h$, compute mean slope $\bar{s}_D(h)$ and $\bar{s}_R(h)$ while aggregating both over increasing $h$; the finest $h$ at which $\bar{s}_D(h) \approx \bar{s}_R(h)$ within tolerance is the scale at which $D$ carries the reference's information. DEMIX's criteria (Guth et al. 2024) generalise this to a ranked comparison over elevation, slope, roughness, and derived networks.

## Validation & uncertainty

Resolution errors are errors of *claim*: the product is correct about the values it holds and wrong about what those values represent. They propagate into every derivative and into every comparison between products.

**How they arise.** (1) Resampling finer than the data (oversampling) with the output cell size recorded as the resolution. (2) Non-uniform density (overlap vs between-line, open vs canopy) reported as a mean. (3) Smoothing in processing (SRTM's boxcar, GDEM's stacking, stereo-correlation windows) not reflected in metadata. (4) Pixel-is-area/point confusion, shifting the grid by half a cell. (5) Derivatives computed at one scale and compared with derivatives at another.

**How they propagate.** A half-cell shift $\delta = \Delta/2$ on a slope $\beta$ yields a vertical error $\delta \tan\beta$, correlated with aspect, that masquerades as a datum or tilt error. Slope loss at coarse resolution biases every slope-dependent model (TWI, erosion, stability, viewshed) in a direction that depends on the terrain spectrum. Oversampled products entering a composite inherit the fine grid's apparent precision; their 30 m uncertainty must be carried as 30 m uncertainty in 1 m cells.

**How to test.** Compute the radial power spectrum and identify the roll-off (Try it, §44.3). Compare slope and roughness distributions against a finer reference while aggregating both (Grohmann's test). Check `AREA_OR_POINT` in the header, then difference the product against a reference and regress the residual on $\tan\beta \cos(\text{aspect})$ and $\tan\beta \sin(\text{aspect})$: a half-cell shift appears as significant coefficients equal to the shift components (the Nuth & Kääb method of [Chapter 41](ch41-change-detection.md) in its registration role). For lidar DEMs, compute the ground-point-density raster and the fraction of cells with zero or one supporting point; publish it. For composites, compute the effective resolution per source and attach it as a raster.

**What to report.** Cell size; convention (area/point) and origin; source density, footprint, and smoothing; effective resolution with its estimation method; density or source-resolution raster; and, for derivatives, the cell size and neighbourhood at which they were computed.

> **Uncertainty budget.** Resolution-related contributions to error in a composite 1″ (~30 m) DEM compared against lidar on a 10° hillslope (indicative; compute your own by the tests above):
>
> | Component | Mechanism | Typical magnitude |
> |---|---|---|
> | Half-cell convention error | Point read as area or vice versa | 15 m horizontal → ~2.6 m vertical on 10° slope, aspect-correlated |
> | Slope under-estimation | 100 m-wavelength relief sampled at 30 m | Slope factor 0.5 (worked example); 17° → 9° |
> | Smoothing in source (SRTM boxcar) | Short-wavelength relief removed | Effective resolution 60–90 m; valley floors raised, ridges lowered by metres in dissected terrain |
> | Oversampled SDB or GDEM cells in composite | 70–1,000 m information in 30 m cells | Apparent precision; true uncertainty that of the source |
> | Aggregation method bias | Min/max binning | ±(0.5–1) σ of within-cell relief, systematic in sign |
>
> The first row is the only one that is an outright blunder; the others are properties of the data that become errors when the metadata do not disclose them.

## Software

**Open source:** GDAL (`gdalwarp` with `-r` kernels—nearest, bilinear, cubic, cubicspline, lanczos, average, mode, rms—for resampling; `gdaladdo` for overviews; `gdalinfo` reports `AREA_OR_POINT`; caveat: default `-r nearest` aliases when downsampling). PDAL (`filters.info`, `filters.hexbin` density and boundary; `writers.gdal` with `output_type=count` gives a per-cell point-count raster for the density layer). lidR (`grid_density`, `rasterize_density`; density and spacing per cell). WhiteboxTools (slope, curvature, roughness with explicit window sizes; `Resample`, `Aggregate`). GRASS GIS (`r.resamp.stats`, `r.resamp.filter`, `r.resamp.interp`, `r.resamp.rst`; honest aggregation and interpolation with documented kernels). xdem (DEM comparison, co-registration, and variogram-based uncertainty across resolutions). GMT (`grdfft` for power spectra and coherence between grids; `grdfilter` for defined-wavelength filtering).

**Free but closed:** NASA's and USGS's product-specific viewers report cell size only; verify convention in the header.

**Commercial:** Global Mapper (resampling and density grids), ArcGIS Pro (Resample, Aggregate, Focal Statistics; caveat: raster functions default to nearest-neighbour), QPS Qimera (CUBE resolution estimation and variable-resolution surfaces), CARIS HIPS/BASE Editor (VR surfaces, density-driven resolution).

## Standards & guides

- **USGS Lidar Base Specification, 2024 rev. A (or current revision).** NPS/NPD definitions, QL0–QL3 density table, spatial-uniformity test, DEM cell size per QL.
- **IHO S-44 Ed. 6.1.0 (2022).** Feature-detection sizes (0.5 / 1 / 2 m cubes) and coverage by order; resolution expressed as detection, not grid.
- **ICAO Annex 15 and PANS-AIM (Doc 10066).** eTOD Areas 1–4 post spacings (3″, 1″, 0.6″, 0.3″) and accuracy/integrity requirements.
- **ASPRS Positional Accuracy Standards, Ed. 2 (2023).** Relationships between accuracy class, recommended cell size, and point density for lidar and photogrammetric products.
- **OGC GeoTIFF 1.1 (OGC 19-008r4).** `GTRasterTypeGeoKey` (RasterPixelIsArea = 1, RasterPixelIsPoint = 2) and raster-space definitions.
- **ISO 19115-1:2014.** `MD_Resolution` (`equivalentScale`, `distance`, `vertical`, `angularDistance`, `levelOfDetail`) and lineage.
- **MIL-PRF-89020B (DTED).** Levels 0/1/2 post spacings and the latitude-dependent longitude spacing.
- **DEMIX / CEOS terminology (Guth et al. 2021).** Recommended definitions of DEM, DSM, DTM, resolution, and related terms.

## Pitfalls

- **Reading "30 m" as "features of 30 m are resolved"** → cell size is mistaken for information content → check lineage and spectrum; assume effective resolution of 2–3 posts unless demonstrated otherwise.
- **Comparing slopes (or curvature, TWI, roughness) across resolutions** → each is scale-dependent by construction → aggregate to a common cell size before comparing, and state the scale.
- **Oversampling SDB to the lidar grid and treating them as equal** → common grids are needed for compositing → carry source resolution and uncertainty per cell; difference at the coarser scale.
- **Losing a 3 m levee in a 10 m grid** → the crest is narrower than the cell and is averaged away → enforce crests as breaklines or structures; test connectivity of modelled flow against known features.
- **Ignoring the pixel-is-area/point convention** → tools and products disagree silently → read `AREA_OR_POINT`; test for a half-cell shift by aspect regression against a reference.
- **Reporting mean density** → overlap and open ground inflate the mean while canopy and gaps go unsupported → publish a density raster and the fraction of cells below threshold.
- **Downsampling with nearest-neighbour** → aliasing of fine relief into the coarse grid → use average or Gaussian kernels for aggregation; nearest only for categorical rasters.
- **Choosing resolution by what is available rather than by what the process needs** → the finest data look best → list the controlling features, divide by 3–4, and check the footprint; enforce what the grid cannot hold.
- **Treating overview levels as resolution statements** → pyramids are for display → compute analyses on the base level or on an explicitly aggregated grid.
- **Assuming a global DEM's finer release has finer information** → SRTM 1″ carries the same smoothing as the 3″ processing → check effective resolution, not posting.

## Key takeaways

- Resolution is a property of the information, not of the file; cell size is the easiest number to change and the least informative.
- Nyquist gives a bound (two samples per wavelength); practical fidelity needs three to four, and terrain always aliases to some degree.
- Footprint, spacing, and aggregation each act as low-pass filters; the system's effective resolution is set by the coarsest.
- Copernicus GLO-30 is close to its nominal 30 m; ASTER GDEM is ~70–100 m; SRTM is ~2–3 posts; SDB "10 m" is often kilometre-scale; a "1 m" QL2 lidar DTM is 1–2 m in the open and much coarser under canopy.
- Slope, curvature, roughness, TWI, flow paths, and viewsheds all change systematically with cell size; never compare them across scales without saying so.
- Oversampling is legitimate for display and grid matching when disclosed with source density and inflated uncertainty; it is illegitimate when it implies detail.
- Half a cell matters: check the pixel-is-area/point convention, and test for the shift.
- Publish source density, footprint, smoothing, and estimated effective resolution alongside cell size.

## References

- Bielski, C., López-Vázquez, C., Grohmann, C. H., Guth, P. L., Hawker, L., Gesch, D., Trevisani, S., Herrera-Cruz, V., Riazanoff, S., Corseaux, A., Reuter, H. & Strobl, P. (2024). Novel approach for ranking DEMs: Copernicus DEM improves one arc second open global topography. *IEEE Transactions on Geoscience and Remote Sensing* 62:4503922. doi:10.1109/TGRS.2024.3368015
- Florinsky, I. V. & Kuryakova, G. A. (2000). Determination of grid size for digital terrain modelling in landscape investigations—exemplified by soil moisture distribution at a micro-scale. *International Journal of Geographical Information Science* 14(8):815–832.
- Grohmann, C. H. (2015). Effects of spatial resolution on slope and aspect derivation for regional-scale analysis. *Computers & Geosciences* 77:111–117.
- Guth, P. L., Van Niekerk, A., Grohmann, C. H., Muller, J.-P., Hawker, L., Florinsky, I. V., Gesch, D., Reuter, H. I., Herrera-Cruz, V., Riazanoff, S., López-Vázquez, C., Carabajal, C. C., Albinet, C. & Strobl, P. (2021). Digital elevation models: Terminology and definitions. *Remote Sensing* 13(18):3581.
- Guth, P. L., Trevisani, S., Grohmann, C. H., Lindsay, J., Gesch, D., Hawker, L. & Bielski, C. (2024). Ranking of 10 global one-arc-second DEMs reveals limitations in terrain morphology representation. *Remote Sensing* 16(17):3273.
- Hengl, T. (2006). Finding the right pixel size. *Computers & Geosciences* 32(9):1283–1298.
- Horn, B. K. P. (1981). Hill shading and the reflectance map. *Proceedings of the IEEE* 69(1):14–47.
- International Hydrographic Organization (2022). *IHO Standards for Hydrographic Surveys*, Special Publication S-44, Edition 6.1.0. IHO, Monaco.
- Kienzle, S. (2004). The effect of DEM raster resolution on first order, second order and compound terrain derivatives. *Transactions in GIS* 8(1):83–111.
- Nyquist, H. (1928). Certain topics in telegraph transmission theory. *Transactions of the American Institute of Electrical Engineers* 47(2):617–644.
- Open Geospatial Consortium (2019). *OGC GeoTIFF Standard*, version 1.1. OGC 19-008r4.
- Polidori, L. & El Hage, M. (2020). Digital elevation model quality assessment methods: A critical review. *Remote Sensing* 12(21):3522.
- Shannon, C. E. (1949). Communication in the presence of noise. *Proceedings of the IRE* 37(1):10–21.
- Smith, B. & Sandwell, D. (2003). Accuracy and resolution of shuttle radar topography mission data. *Geophysical Research Letters* 30(9):1467.
- Tachikawa, T., Kaku, M., Iwasaki, A., Gesch, D., Oimoen, M., Zhang, Z., Danielson, J., Krieger, T., Curtis, B., Haase, J., Abrams, M., Crippen, R. & Carabajal, C. (2011). *ASTER Global Digital Elevation Model Version 2 – Summary of Validation Results*. NASA/METI/USGS.
- Tarolli, P. (2014). High-resolution topography for understanding Earth surface processes: Opportunities and challenges. *Geomorphology* 216:295–312.
- U.S. Geological Survey (2024). *Lidar Base Specification 2024 rev. A*. USGS National Geospatial Program.
- Zhang, W. & Montgomery, D. R. (1994). Digital elevation model grid size, landscape representation, and hydrologic simulations. *Water Resources Research* 30(4):1019–1028.

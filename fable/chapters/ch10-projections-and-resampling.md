# Chapter 10 — Map projections, grids, and the resampling they force

> **Part III — Where is "here"? Geodesy, datums, projections.** The last chapter of Part III moves from the datum to the grid: how a curved surface is flattened into rows and columns, what that costs, and why every change of projection is also a change of the elevations themselves.

**In this chapter.** A DEM is a sample of a surface on a lattice, and the lattice has to live in a map projection or in geographic coordinates; neither choice is free. After this chapter you will be able to compute the ground size and shape of a cell in any projection, choose a projection by what you will compute from it (slope, area, volume, flow), explain grid versus ground distance and the combined scale factor, and — the practical core — understand that reprojecting a DEM is a resampling that changes elevations slightly and derivatives a lot, with a worked example showing how much. You will also meet the tiling schemes you will encounter (USGS quads, SRTM 1° tiles, Copernicus, XYZ/WMTS), the ways zone boundaries and the poles break naive workflows, how to encode CRS and pixel registration in a file, and the half-pixel shift that silently misaligns products whose authors disagreed about whether a pixel is an area or a point.

## 10.1 Geographic grids and anisotropic cells

Most global and many national DEMs are distributed on a **geographic grid**: rows at constant latitude, columns at constant longitude, with a cell size in arc seconds. SRTM, ASTER GDEM, Copernicus DEM, NASADEM, the USGS 3DEP 1/3″ and 1″ products, and MERIT are all geographic. The reason is practical — one lattice covers the planet without zones, and the lattice coincides with the degree-based tiling — but the consequence is that cells are not square on the ground. One arc second of latitude is about 30.9 m everywhere (slightly more near the poles, since the meridian radius of curvature grows with latitude: 30.7 m at the equator, 31.0 m at 60°). One arc second of longitude is about $30.9\cos\varphi$ m: 30.9 m at the equator, 21.8 m at 45°, 15.5 m at 60°, 5.4 m at 80°. A "30 m" global DEM is therefore 30 × 22 m in the Alps and 30 × 15 m in Fairbanks, and the ground area of a 1″ cell varies from about 950 m² at the equator to about 480 m² at 60°.

This anisotropy has three consequences that are routinely ignored:

- **Slope and aspect** computed by a finite-difference operator that assumes square cells of one unit (degrees) or of a nominal 30 m are wrong. Treating a 1″ × 1″ cell as 30 × 30 m at 45° N understates east–west gradients by 27 % and biases aspect toward north–south (Mathematics section, worked example in §10.4).
- **Area and volume** per cell vary with latitude; summing cells without weighting by $\cos\varphi$ (or by the exact ellipsoidal cell area) biases any area statistic poleward.
- **Effective resolution** differs by axis. Near 60° the east–west sampling is finer than the north–south; the information content of the data (which was typically acquired by a sensor with isotropic footprints) does not improve just because the lattice is denser, so the east–west axis is oversampled ([Chapter 44](ch44-resolution-and-sampling.md)).

When should you *stay* in latitude/longitude? When the product is global or spans many projection zones; when the downstream users will reproject anyway (reprojecting twice is worse than once; §10.4); when the computation is cell-wise (classification, thresholding, change detection on co-registered grids) and does not involve distances; and when the data are an authoritative archive that should be kept in native form. Compute derivatives in geographic coordinates only with software that scales the two axes separately (GDAL's `gdaldem slope -s 111120` with a scale that is correct only for the N–S axis is *not* enough; use a tool that applies $\cos\varphi$ per row — WhiteboxTools does; check your GDAL version's `gdaldem` documentation before assuming it does — or reproject to an equal-area or conformal CRS first).

<!-- figure: Figure 10.1 — Ground footprints of a 1″ × 1″ cell at 0°, 30°, 45°, 60°, and 75° latitude drawn to scale, next to the fixed 30 m × 30 m footprint of a UTM cell; annotation of the area ratio. -->

## 10.2 Properties, distortion, and projection choice

No map of a curved surface onto a plane preserves all distances (Gauss); a projection chooses what to preserve. **Conformal** projections (Mercator, Transverse Mercator, Lambert Conformal Conic, stereographic) preserve angles and therefore local shape, at the price of a scale factor $k$ that varies with position; areas are distorted by $k^2$. **Equal-area** projections (Albers, Lambert Azimuthal Equal-Area, sinusoidal, Mollweide) preserve area, at the price of shape distortion that grows away from the standard lines. **Equidistant** projections preserve distance along one family of lines only (meridians in the equidistant conic; from the centre in the azimuthal equidistant). **Tissot's indicatrix** visualizes all of this: an infinitesimal circle on the ellipsoid maps to an ellipse with semi-axes $a_T$ and $b_T$ equal to the principal scale factors; a conformal projection has $a_T = b_T$ everywhere (circles stay circles but change size), an equal-area projection has $a_T b_T = 1$ (ellipses of constant area), and the maximum angular distortion is $2\arcsin\frac{a_T - b_T}{a_T + b_T}$.

For DEMs, the relevant question is what will be computed:

| Computation | Needs | Preferred class | Typical choice |
|---|---|---|---|
| Slope, aspect, curvature, hillshade | local isotropy of scale | conformal | UTM, TM/LCC national grid, polar stereographic |
| Area, volume, hypsometry, catchment area | true area | equal-area | Albers (continents), LAEA (Europe, ETRS89-LAEA), equal-area cylindrical for global |
| Flow routing, hydrologic distance | isotropic scale and modest distortion | conformal or low-distortion | UTM or LDP |
| Visualization / web | any; speed and tiling | — | Web Mercator (with caveats below) |
| Archive, global analysis | no reprojection | geographic | 1″/3″ lat-lon |

The common choices: **UTM** ⟨H⟩ (Transverse Mercator in 6° zones with $k_0 = 0.9996$, adopted by the US Army in the 1940s — the gis-history record places it in 1942 ⟨H⟩ — and now the default for everything from lidar deliveries to Landsat) keeps scale distortion within about ±400 ppm at the zone's design limits, i.e. 0.4 m per kilometre; areas within $k^2 \approx \pm 800$ ppm. **Polar stereographic** (EPSG:3031 for Antarctica with true scale at 71° S; EPSG:3413 for the Arctic with true scale at 70° N) is the ice-sheet standard because it is conformal, has no zone seams, and its scale error is modest over the polar caps (for EPSG:3031, $k = (1+\sin 71°)/(1+\sin\varphi)$, so $k \approx 0.973$ at the pole — distances shrunk by about 2.7 % and areas by $k^2 \approx 0.946$; worth remembering when computing ice volume: apply the area-scaling factor $k^{-2}$ per cell, which REMA and BedMachine documentation provide). **LAEA** on ETRS89 (EPSG:3035, centred 52° N 10° E) is the European standard for pan-European statistics and the Copernicus land products, chosen because area is what those products count. **National grids** (OSGB36/British National Grid, a TM with $k_0 = 0.9996012717$; Lambert-93 for France, an LCC; RD New for the Netherlands, an oblique stereographic; Swiss LV95, an oblique Mercator) were designed to keep distortion within ~±200–500 ppm over their country and are the right choice within it.

**Web Mercator** (EPSG:3857) deserves a specific warning. It is a spherical Mercator applied to ellipsoidal coordinates, so it is *not conformal* (the north–south and east–west scale factors differ by up to about 0.67 %, and the position of a point differs from true ellipsoidal Mercator by up to about 20–40 km in northing at mid-latitudes if you tried to treat it as the same projection); its linear scale is $\sec\varphi$ (2 at 60°, 3.9 at 75°) and its area scale is $\sec^2\varphi$ (4 at 60°); it cannot represent the poles. It is a fine tile addressing scheme and a poor coordinate system for computation: slope computed on a Web Mercator DEM without per-row scaling is wrong by a factor of $\sec\varphi$, and areas by $\sec^2\varphi$. Battersby et al. (2014) document the perceptual and analytical consequences.

> **Definitions that bite.** "Metres" in a projected CRS are **grid metres**, not ground metres. A 1 000.000 m distance between two UTM coordinates near a zone edge is about 1 000.4 m on the ellipsoid and, at 1 500 m elevation, about 1 000.6 m on the ground. For a DEM this means that a "30 m" UTM cell has a ground size that varies by about ±0.4 % across the zone and that cell *areas* in UTM are in error by up to ±0.08 %; not much — until you compute a reservoir volume to 0.1 % or stake out a pipeline from grid coordinates.

## 10.3 Grid versus ground distance; combined scale factor; low-distortion projections

A distance measured on the ground at elevation $h$ relates to the distance on the map grid through two factors. The **elevation factor** (or sea-level factor) reduces the ground distance to the ellipsoid: $EF = R/(R + h)$ with $R$ the local radius of curvature (6 371 km is adequate for most purposes; the geometric mean radius $\sqrt{MN}$ at the latitude for precision), so at $h = 1\,600$ m, $EF = 0.999\,749$. The **grid scale factor** $k$ then maps ellipsoid distance to grid distance; in UTM it is 0.9996 on the central meridian and about 1.000\,98 at 3° from it at the equator (less at higher latitude, since the zone narrows). The **combined scale factor** is $CSF = k \times EF$, and $D_{grid} = CSF \times D_{ground}$. In Denver (UTM zone 13, roughly 1.3° west of the central meridian at 105° W, $h \approx 1\,600$ m): $k \approx 0.9996 + \tfrac{1}{2}(\Delta\lambda \cos\varphi)^2 \cdot 0.9996 \approx 0.99976$, $EF = 0.99975$, $CSF \approx 0.99951$. A 1 000 m ground distance is 999.51 m on the grid; a kilometre of surveyed pipeline comes out half a metre short on the map, and a square kilometre of surveyed area comes out about 980 m² short.

Engineers resolve this in one of three ways. The crude one is a **"modified" or "ground" grid**: multiply project coordinates by $1/CSF$ about some origin, producing coordinates that look like State Plane or UTM but are not — and that will be mistaken for the real thing by the next person ([Chapter 9](ch09-vertical-datums.md), §9.5, on project datums). The second is to carry $CSF$ explicitly in every computation. The third, now preferred, is a **low-distortion projection (LDP)**: a conformal projection (usually TM or LCC, sometimes oblique Mercator) designed for the project area with its developable surface raised to the project's mean elevation, so that $CSF \approx 1$ within a few ppm across the area. The **State Plane Coordinate System of 2022** (SPCS2022; defined by the NGS *SPCS2022 Policy* and *Procedures* documents, with Dennis 2018 giving the history and design rationale) institutionalizes this: each state can define a statewide zone (distortion up to a few hundred ppm), multiple zones, and a layer of **special-purpose LDPs** with distortion designed to within about ±20 ppm — meaning a 1 km ground distance differs from its grid distance by ≤ 2 cm. For DEM producers, LDPs are a mixed blessing: they are excellent for engineering deliverables and terrible for regional mosaicking, because every project has its own CRS, often not in EPSG; an LDP DEM must ship with its full WKT2 definition, not a name.

## 10.4 Reprojection is resampling

A projected DEM is a lattice of samples in projected space. Changing the projection moves every lattice point to a non-lattice position in the new space, and the only way to get values back on a lattice is to **resample** — to estimate elevation at new positions from the old samples with an interpolation kernel. This is the most underappreciated fact about DEMs: `gdalwarp` does not "convert" a DEM, it *creates a new one* by interpolation, and the new one has different elevations, different derivatives, different noise properties, and different nodata boundaries.

### 10.4.1 Kernels

| Kernel (`gdalwarp -r`) | Support | What it does | Elevation effect | Slope/curvature effect |
|---|---|---|---|---|
| `near` (nearest neighbour) | 1 cell | copies the closest sample | no new values; positional error up to ½ cell | blocky; introduces spurious steps of up to one cell's relief; preserves nodata exactly |
| `bilinear` | 2 × 2 | linear in x then y | smooths; peaks lowered and pits raised by up to ~¼ of local curvature × cell²; never overshoots | slopes reduced (low-pass); curvature strongly attenuated |
| `cubic` (Keys, $a = -0.5$) | 4 × 4 | piecewise cubic convolution | sharper than bilinear; **overshoots** by up to ~7 % of a step in 1D, ~15 % at a 2D corner | retains more slope; creates ringing (false pits/peaks) at cliffs, building edges, nodata edges |
| `cubicspline` (B-spline) | 4 × 4 | smoothing cubic B-spline | smoother than bilinear, no overshoot | strong attenuation of slope and curvature |
| `lanczos` ($a = 3$) | 6 × 6 | windowed sinc | sharpest; overshoot comparable to or larger than cubic | best frequency preservation; worst ringing at edges |
| `average`, `rms`, `med`, `min`, `max`, `mode`, `q1`, `q3`, `sum` | all source cells in target footprint | aggregation | correct for coarsening (downsampling); `average` is the right default for DSM→coarser DTM-like products; `max`/`min` for DSM/DTM envelopes | `average` is an area low-pass; `sum` for counts |

Two further points. **Nodata**: `near` preserves it; interpolating kernels either propagate it (one nodata in the support → nodata out, eroding valid data by the kernel radius — 1 cell bilinear, 2 cubic, 3 Lanczos) or ignore it with renormalized weights, which biases values near holes toward the valid side (GDAL's default; check its behaviour at lake polygons and void edges). **Downsampling with an interpolating kernel is wrong**: bilinear at a 10× coarser grid samples a 2 × 2 neighbourhood out of 100 cells and aliases the rest; coarsen with `average` (or a proper anti-aliased filter) and keep interpolating kernels for same-scale or finer-scale reprojection.

### 10.4.2 How much does it change?

For a smooth surface sampled at spacing $\Delta$, bilinear interpolation at a point midway between samples has an error of about $\tfrac{1}{8}\Delta^2 |f''|$ in 1D; for a ridge with radius of curvature 100 m sampled at 10 m, that is $\tfrac{1}{8}\times100/100 = 0.125$ m of peak lowering. Over real terrain the elevation RMS difference between a DEM and its reprojected copy is typically a few percent of the cell-to-cell relief: 0.05–0.2 m for 1 m lidar DTMs in rolling terrain, 1–3 m for 30 m DEMs in mountains. Slope is affected far more: bilinear resampling reduces the standard deviation of slope by 5–15 % at the same nominal resolution, and the maximum slope by more; cubic preserves slope statistics better but adds spurious extremes at edges. Grohmann (2015) quantifies these effects across resolutions for SRTM-class data.

> **Worked example.** *Slope on a geographic grid, and what bilinear resampling does to it.* A 1″ DEM at 45° N has an east–west ramp rising 7.9 m per column. The correct E–W gradient is $7.9 / 21.8 = 0.362$, a slope of 19.9°. Three ways to get it wrong:
>
> 1. Treat the cell as 30 m square (nominal resolution): gradient $7.9/30 = 0.263$, slope 14.8° — understated by 5.1°.
> 2. Treat the cell as 1 unit (degrees) with `gdaldem slope` and no `-s`: gradient $7.9 / (1/3600)$ = 28 440 → slope 89.998°, flagged by any user, hence harmless.
> 3. Use `-s 111120` (metres per degree for latitude): correct for the N–S axis, but the E–W axis is still treated as 30.87 m, so the result is case 1 with a slightly different divisor: 14.4°.
>
> Now reproject the same DEM to UTM at 30 m with bilinear resampling. The UTM grid is rotated relative to the geographic one by the convergence (about 1° near the zone centre at this latitude; more at the edges) and its 30 m cells each straddle about 1.4 E–W source columns. A cell midway between two source columns receives the average of neighbours; on a straight ramp bilinear interpolation is exact, so the slope is preserved at 19.9°. On a *crest* with the same 7.9 m/column flanks, a new cell centre that falls a fraction $t$ of a column away from the crest sample receives $P - 7.9\,t$ (the linear interpolant cannot see the peak between samples), so the crest cell value drops by up to 3.9 m when $t = 0.5$ — and the slope on either side, computed over 30 m instead of 21.8 m from values that were themselves interpolated along the ramp, is still 19.9° on the flanks but with the summit 3.9 m lower. A hypsometric maximum, a peak-to-saddle relief, or a line-of-sight from the crest now differ by that amount. Reproject with `cubic` instead and the crest is preserved to within ~0.5 m but the toe of a 10 m road cut nearby acquires a 0.7 m ($7.4 \%$) false depression on its downhill side.

### 10.4.3 Reproject once, late

The practical doctrine follows: (1) keep the archive DEM in its native grid and projection; (2) do computations that do not need distances (classification, masking, differencing against a co-registered product) in the native grid; (3) when a projected grid is required, reproject *once*, directly from the native grid to the final one, with the kernel chosen for the quantity of interest (bilinear or cubic for elevation and for slope at the same scale; `average` for coarsening; `near` only for categorical layers and for preserving exact nodata); (4) compute derivatives *after* the single reprojection; and (5) record the resampling (source grid, target grid, kernel, nodata handling, software version) in the metadata and lineage ([Chapter 29](ch29-processing-pipelines.md), [Chapter 49](ch49-metadata.md)). Two reprojections — geographic → UTM → State Plane, or UTM zone 10 → geographic → UTM zone 11 — compound the smoothing and shift the surface by up to a cell; the second step should always be replaced by a direct transform from the original.

> **Try it.** Measure the resampling effect on your own DEM. The script reprojects a geographic DEM to UTM with three kernels, reprojects each back, and compares with the original over the valid area.
>
> ```bash
> SRC=n45_w122_1arc_v3.tif       # any 1" DEM tile (pixel-is-point!)
> for R in near bilinear cubic; do
>   gdalwarp -q -overwrite -t_srs EPSG:32610 -tr 30 30 -r $R -tap $SRC utm_$R.tif
>   gdalwarp -q -overwrite -t_srs EPSG:4326 -tr 0.000277777777778 0.000277777777778 \
>            -te $(gdalinfo $SRC | python3 -c "
> import sys,re; t=sys.stdin.read()
> ul=re.search(r'Upper Left\s+\(\s*([-\d.]+),\s*([-\d.]+)',t).groups()
> lr=re.search(r'Lower Right\s+\(\s*([-\d.]+),\s*([-\d.]+)',t).groups()
> print(ul[0],lr[1],lr[0],ul[1])") -r $R utm_$R.tif back_$R.tif
>   gdal_calc.py -q --overwrite -A $SRC -B back_$R.tif --outfile=diff_$R.tif \
>                --calc="A-B" --NoDataValue=-9999
>   echo "$R:"; gdalinfo -stats diff_$R.tif | grep -E "MINIMUM|MAXIMUM|MEAN|STDDEV"
>   gdaldem slope utm_$R.tif slope_$R.tif -q
>   gdalinfo -stats slope_$R.tif | grep -E "MEAN|STDDEV" | sed 's/^/  slope /'
> done
> ```
>
> Expected outcome on a 1″ mountain tile: round-trip STDDEV of roughly 1–3 m for `near`, 0.5–1.5 m for `bilinear` and `cubic`, with `cubic` showing larger MIN/MAX extremes (overshoot at cliffs); slope STDDEV lowest for `bilinear`, highest for `near` (spurious steps), with `cubic` in between. The round trip doubles the damage; the single forward reprojection is about half.

<!-- figure: Figure 10.2 — Four-panel comparison of a ridge-and-road-cut profile in the source DEM and after nearest, bilinear, and cubic resampling to a rotated grid; cubic panel shows the overshoot at the cut, bilinear the lowered crest, nearest the staircase. -->

## 10.5 Tiling

No one distributes a continent as one file. Tiling schemes are the second lattice — a lattice of files on top of the lattice of cells — and their conventions are a recurring source of one-cell errors.

**USGS quadrangles.** The 7.5′ quad tiled the United States for a century and the original 30 m USGS DEMs inherited it (quad-based, in UTM, with neat lines clipped at an angle to the grid — hence the stair-stepped edges of legacy DEMs). 3DEP now distributes 1″ and 1/3″ products in 1° × 1° tiles and lidar-derived 1 m DEMs in 10 km UTM tiles.

**SRTM 1° × 1° tiles.** The SRTM convention — followed by ASTER GDEM, NASADEM, and ALOS AW3D30 — names a tile by the latitude and longitude of its *south-west corner* (`N45W122`) and gives it 3 601 × 3 601 cells at 1″ (1 201 × 1 201 at 3″). The extra row and column exist because the cells are **pixel-is-point** samples at integer multiples of 1″ *inclusive of both edges*: the eastern column of `N45W122` and the western column of `N45W121` are the same samples. Mosaicking such tiles without recognizing the overlap produces either duplicated edge columns or, after a naive "shift by one," a one-cell offset that propagates across the mosaic. GDAL handles this when the files carry `RasterPixelIsPoint` keys and the merge honours them; many derived products do not.

**Copernicus DEM tiles.** Also 1° × 1°, but with a latitude-dependent column count to keep ground sampling roughly isotropic: 3 600 columns at |φ| < 50°, 2 400 at 50–60°, 1 800 at 60–70°, 1 200 at 70–80°, 720 at 80–85°, 360 at 85–90° (Airbus product handbook). A mosaic across 50° N has a change of cell size along a parallel; use each tile's own geotransform.

**XYZ / TMS / WMTS and quadkeys.** Web tiles are 256 × 256 (or 512 × 512) cells in Web Mercator at zoom $z$, $2^z$ tiles per axis. **XYZ** ("slippy map") numbers rows from the north, **TMS** from the south ($y_{TMS} = 2^z - 1 - y_{XYZ}$) — a schism that has misplaced many tiles by a hemisphere. **WMTS** generalizes to arbitrary tile matrix sets, standardized in the **OGC Two-Dimensional Tile Matrix Set** (17-083r2 v1.0, 2019; 17-083r4 v2.0, 2022). **Quadkeys** (Bing) interleave the bits of $x$ and $y$ into a base-4 string — a Z-order curve, as in S2 and geohash ([Chapter 60](ch60-dggs-and-location-codes.md)). Terrain served this way (Terrain-RGB, quantized meshes) has been resampled to Web Mercator at the tile's zoom resolution: a visualization product, not a measurement product.

**DGGS preview.** Discrete global grid systems (H3, S2, rHEALPix, ISEA) replace rectangular tiles with cells of nearly equal area on the sphere, resolving anisotropy and the pole problem at the cost of hexagonal or triangular cells; gridding a DEM to one is yet another resampling ([Chapter 60](ch60-dggs-and-location-codes.md)).

## 10.6 Zone boundaries, seams, and the poles

Any zoned projection has seams. UTM zones are 6° wide; a project that straddles a boundary must choose one zone and accept distortion beyond the design limit in the other half (UTM remains usable to about 1.5–2 zones' width with distortion rising to ~1 000–1 500 ppm at 4.5° from the central meridian, which is acceptable for a DEM used for slope but not for engineering), or use a different projection (an LCC or a custom TM centred on the project). The classic mistake is mosaicking tiles delivered in two different zones as if they were one grid: the result is a shear of several hundred metres and a rotation of a few degrees at the seam. Detect it by looking for a straight discontinuity along a meridian; prevent it by reprojecting every tile to one target CRS before mosaicking and by refusing files whose CRS differs from the project's.

**UTM overlap.** Many lidar specifications (and the 3DEP 1 m product) deliver tiles in the zone where most of the tile lies, with a buffer of a few kilometres into the adjacent zone computed in the delivery zone, so that a user needing a seamless surface can reproject the other side's tiles once, from original data, rather than resampling an already-resampled edge.

**Polar regions.** UTM stops at 84° N and 80° S; UPS covers the caps; a 1″ geographic cell at 89° is 31 m × 0.54 m; Web Mercator cannot reach the poles. Ice-sheet products use polar stereographic (EPSG:3413, 3031), and merging them with sub-Arctic UTM or geographic data must happen in one CRS with a single resampling. Convergence is extreme near the poles — grid north and true north differ by the longitude difference from the central meridian — so aspect from a polar-stereographic DEM must be rotated by the convergence before it means anything geographic.

**Antimeridian.** Geographic grids split at ±180°: tiles `N65E179` and `N65W180` are adjacent but numerically 359° apart, and a bounding box from 179° to −179° is 2° or 358° wide depending on the software. Work in a projected CRS centred on the region or in antimeridian-aware software.

## 10.7 CRS metadata in grids and the half-pixel problem

### 10.7.1 Encoding

A raster's georeferencing is a **geotransform** (origin, cell sizes, rarely rotation terms) plus a CRS. In **GeoTIFF** the geotransform lives in `ModelTiepointTag` with `ModelPixelScaleTag` (or `ModelTransformationTag`) and the CRS in the GeoKey directory; GeoTIFF 1.1 (OGC 19-008r4, 2019) allows a full WKT2 string and compound CRSs with a vertical component. **COG** adds tiling and overviews — and overviews are *resampled* copies whose kernel (`gdaladdo -r`) matters to anyone who reads them as data ([Chapter 47](ch47-file-formats.md)). **NetCDF/CF** and **Zarr** carry coordinates as explicit variables (cell centres by convention, with optional `bounds`) and a `grid_mapping` or `crs_wkt`. A raster with only a `.prj` and a world file has WKT1 and a geotransform referring to the *centre* of the upper-left pixel — opposite to GeoTIFF's default, and the first of the half-pixel traps.

### 10.7.2 Pixel-is-area versus pixel-is-point

A raster cell can be understood as an **area** (the value represents the cell's extent; the georeferenced corner is the outer corner of the cell) or as a **point** (the value is a sample at a location; the georeferenced coordinate is the sample location, i.e. the cell *centre*). GeoTIFF records this in `GTRasterTypeGeoKey` as `RasterPixelIsArea` (the default) or `RasterPixelIsPoint`. The two interpretations place the same array of numbers half a cell apart on the ground. Elevation data are, in origin, point samples (SRTM, 3DEP seamless, Copernicus, most global products declare `PixelIsPoint`); imagery is area. Software disagrees about what to do with `PixelIsPoint`: GDAL internally treats every raster as pixel-is-area and *shifts the geotransform by half a pixel* when reading a `PixelIsPoint` file so that the cell extents are centred on the sample locations (and writes the key back on output); other software ignores the key, or applies the shift in the opposite direction. World files always refer to the centre of the upper-left pixel, so a world file written from GDAL's internal (area) geotransform is correct, but a world file written by software that took the GeoTIFF tiepoint literally from a `PixelIsPoint` file is half a cell off. ESRI ASCII grids use `xllcorner`/`yllcorner` (area) or `xllcenter`/`yllcenter` (point) and the two keywords are frequently used interchangeably by hand-edited headers.

The consequence is a horizontal offset of half a cell between products that should be coincident — 15 m for a 30 m DEM, 0.5 m for a 1 m lidar DEM — in a diagonal direction (half a cell in x and y). By §8.7's rule, on a 20° slope that is 5.5 m of apparent vertical error for the 30 m product, and it is systematic. It is also invisible in casual overlay and appears in a DEM of difference as an aspect-dependent pattern that looks exactly like a datum or co-registration error — because it *is* one.

> **Case file.** The SRTM 1″ tiles are `PixelIsPoint` with sample locations at exact integer arc seconds and 3 601 samples per degree. Early in the product's life, several widely used derived datasets re-gridded SRTM onto 3 600-cell tiles under a pixel-is-area reading, which both shifted the data by half a cell (15 m) and resampled it; a decade of papers comparing "SRTM" to lidar then reported horizontal offsets of 10–20 m, some of which were the product's genuine geolocation error (~9 m CE90; Rodríguez et al. 2006) and some of which were the half-pixel reinterpretation. The lesson that USGS, NASA LP DAAC, and the Copernicus programme all state in their documentation — that the tile edges overlap and that the registration is point — is still routinely missed; the test is simple: check `GTRasterTypeGeoKey` with `gdalinfo` (or `listgeo`) and compare the reported origin against the tile name. If the origin is `-122.000138889` for a tile named `W122`, GDAL has applied the half-cell shift and the extents are right; if it is `-122.0` for a `PixelIsPoint` file, the software did not.

### 10.7.3 Registration conventions when converting

Converting between conventions is a bookkeeping shift, not a resampling: the array is unchanged, and the origin moves by half a cell. The error is to resample when a shift was needed (introducing smoothing) or to shift when the data were already correct (introducing the offset). Grid *alignment* (`gdalwarp -tap`, "target aligned pixels") snaps the output grid to multiples of the cell size, which is what you want for mosaicking consistency, but if the source was point-registered at integer arc seconds and you align area cells to integer arc seconds, you have moved the samples by half a cell; align to half-integers instead, or let GDAL's internal convention handle it and confirm with `gdalinfo`. [Chapter 31](ch31-interpolation-and-gridding.md) covers the related **grid registration** issue in gridding (GMT's gridline- versus pixel-registered grids, `-r`), which is the same distinction under another name.

<!-- figure: Figure 10.3 — Two overlaid 3×3 grids with the same cell values, one interpreted as pixel-is-area and one as pixel-is-point, showing the half-cell diagonal displacement; inset: SRTM tile edges N45W122 and N45W121 sharing their boundary column. -->

## Then & now

- **Projections from tables to series to nanometres.** Mercator (1569) and Lambert (1772) by construction; Gauss and Krüger (1912) gave the TM its series; UTM ⟨H⟩ (gis-history dates it 1942) standardized zones and $k_0$; Snyder's *Working Manual* (USGS PP 1395, 1987 ⟨H⟩) became the implementer's bible; Evenden's PROJ (1990 ⟨H⟩) made it software; Karney (2011) took the TM to nanometres, the algorithm in PROJ since 4.8.
- **Resampling from an afterthought to a documented step.** Early raster GIS resampled with nearest neighbour by default; bilinear and cubic became standard in the 1980s image-processing literature (Keys 1981); GDAL's `gdalwarp` (2002 onward) exposed the kernel choice; `average`/`mode`/`rms` aggregation kernels arrived in GDAL 1.10–3.x; provenance standards (ISO 19115 lineage, STAC processing extension) now expect the kernel to be recorded.
- **Tiling from quads to tile matrix sets.** Paper quads → SRTM's 1° point-registered tiles (2000–2003) → Web Mercator XYZ tiles (2005) with the TMS/XYZ row-order schism → WMTS (2010) → OGC 2D-TMS (2019/2022) → COG with internal tiles replacing external tile pyramids for analysis (2016 onward).
- **Metadata from sidecars to self-description.** World files and `.prj` (1990s) → GeoTIFF 1.0 with EPSG codes → GeoTIFF 1.1 (2019) with WKT2 and compound CRSs → PROJJSON in STAC and PROJ.

## Mathematics

**Area and dimensions of a geographic cell.** The ellipsoidal area of a cell $\Delta\varphi \times \Delta\lambda$ (radians) centred at latitude $\varphi$ is, to excellent approximation,

$$A \approx M(\varphi)\,N(\varphi)\,\cos\varphi\;\Delta\varphi\,\Delta\lambda ,$$

with $M$ and $N$ the radii of curvature of [Chapter 7](ch07-shape-of-the-earth.md) (an exact expression integrates the authalic latitude; the approximation errs by < 10⁻⁵ for arc-second cells). The N–S side is $M\,\Delta\varphi$ and the E–W side $N\cos\varphi\,\Delta\lambda$. For $\Delta\varphi = \Delta\lambda = 1″ = 4.848\times10^{-6}$ rad at $\varphi = 45°$: $M = 6\,367\,382$ m, $N = 6\,388\,838$ m, so the sides are 30.87 m and 21.90 m and $A = 676$ m². At the equator, $M = 6\,335\,439$ m and $N = a$, giving 30.71 m × 30.92 m = 950 m². At 60°: 30.97 m × 15.50 m = 480 m².

**Scale factor and convergence.** A projection's local behaviour at a point is its Jacobian. For a conformal projection, $k$ is the ratio of a map distance to the corresponding ellipsoidal distance, independent of direction. For the Transverse Mercator on the sphere the closed form is $k = 1/\sqrt{1 - \cos^2\varphi\sin^2\Delta\lambda}$; on the ellipsoid, to second order in $\Delta\lambda$,

$$k \approx k_0\left[1 + \frac{(\Delta\lambda\cos\varphi)^2}{2}(1 + \eta^2)\right], \qquad \eta^2 = e'^2\cos^2\varphi ,$$

which gives, for UTM at the equator and $\Delta\lambda = 3°$ ($0.05236$ rad): $k \approx 0.9996\,[1 + 0.00137\times1.0067] = 1.00098$. The **grid convergence** $\gamma$ — the angle from grid north to true north — is $\gamma \approx \Delta\lambda\sin\varphi$ to first order (positive east of the central meridian in the northern hemisphere), so at $\varphi = 45°$, $\Delta\lambda = 3°$: $\gamma \approx 2.12°$. Aspect from a UTM DEM is relative to grid north and should be corrected by $\gamma$ when compared to compass or solar azimuths; the error is up to 3° at a UTM zone edge and up to 180° in polar stereographic.

**Transverse Mercator (Krüger–Karney series).** With conformal latitude $\chi$ (the latitude on the conformal sphere, computed from $\varphi$ via $\tan\chi = \sinh(\operatorname{artanh}\sin\varphi - e\operatorname{artanh}(e\sin\varphi))$), define $\xi' = \arctan\left(\tan\chi / \cos\Delta\lambda\right)$ and $\eta' = \operatorname{artanh}\left(\sin\Delta\lambda / \sqrt{\tan^2\chi + \cos^2\Delta\lambda}\right)$ — the spherical TM — then

$$\xi = \xi' + \sum_{j=1}^{J}\alpha_j\sin(2j\xi')\cosh(2j\eta'), \qquad \eta = \eta' + \sum_{j=1}^{J}\alpha_j\cos(2j\xi')\sinh(2j\eta'),$$

$$x = k_0 A\,\eta + FE, \qquad y = k_0 A\,\xi + FN, \qquad A = \frac{a}{1+n}\left(1 + \frac{n^2}{4} + \frac{n^4}{64} + \cdots\right), \quad n = \frac{f}{2-f},$$

where the $\alpha_j$ are polynomials in the third flattening $n$ ($\alpha_1 = \tfrac{1}{2}n - \tfrac{2}{3}n^2 + \tfrac{5}{16}n^3 + \cdots$, etc.; Karney 2011 gives them to $n^6$, and $J = 6$ yields nanometre accuracy within 3 900 km of the central meridian). The scale factor and convergence follow from the derivatives of the same series. This is the algorithm in PROJ (`+proj=tmerc`, default since 4.8 is the extended Krüger; `+approx` selects the older Snyder/Evenden series, which is accurate to ~1 mm within the zone but degrades badly beyond ~5°).

**Combined scale factor.** $CSF = k \cdot EF$, $EF = \dfrac{R_\alpha}{R_\alpha + h}$, where $R_\alpha = \dfrac{MN}{M\sin^2\alpha + N\cos^2\alpha}$ is the radius of curvature in the azimuth $\alpha$ of the line (Euler's formula) and $h$ the ellipsoidal height; with $R = 6\,371\,000$ m and $h$ in metres, $EF \approx 1 - h/6\,371\,000 = 1 - 0.157\,h$ ppm. Ground distance $D_{ground} = D_{grid}/CSF$; ground area $A_{ground} = A_{grid}/CSF^2$. Note that $h$ here should be the *ellipsoidal* height; using $H$ introduces an error of $N/R \approx 5$ ppm for $N = 30$ m, which is below the design tolerance of most LDPs but not negligible for the tightest.

**Tissot indicatrix.** With map metric $ds^2 = E\,d\varphi^2 + 2F\,d\varphi\,d\lambda + G\,d\lambda^2$, the scale along the meridian is $h_T = \sqrt{E}/M$ and along the parallel $k_T = \sqrt{G}/(N\cos\varphi)$; the principal scale factors $a_T \ge b_T$ satisfy $a_T^2 + b_T^2 = h_T^2 + k_T^2$ and $a_T b_T = h_T k_T\sin\theta'$, with $\theta'$ the angle between the meridian and parallel images. Conformal: $a_T = b_T = k$; equal-area: $a_T b_T = 1$.

**Interpolation kernels.** In one dimension with samples $f_i$ at integer positions and a target at $i + t$, $0 \le t < 1$:

- Nearest: $\hat f = f_{i + \lfloor t + 0.5\rfloor}$.
- Bilinear (linear in 1D): $\hat f = (1-t)f_i + t f_{i+1}$; error $\le \tfrac{1}{8}\max|f''|$ per unit spacing squared; the kernel's frequency response is $\operatorname{sinc}^2$, a low-pass that attenuates the Nyquist frequency to 40 %.
- Keys cubic convolution ($a = -0.5$): weights $w(x) = (a+2)|x|^3 - (a+3)|x|^2 + 1$ for $|x| \le 1$ and $w(x) = a|x|^3 - 5a|x|^2 + 8a|x| - 4a$ for $1 < |x| \le 2$; $\hat f = \sum_{j=-1}^{2} w(j - t)\,f_{i+j}$. At $t = 0.5$ the weights are $(-0.0625, 0.5625, 0.5625, -0.0625)$. On a unit step the maximum overshoot is $-\min_{1<x<2} w(x) = 0.0741$ at $x = 4/3$, i.e. 7.4 % of the step in 1D and up to $(1.074)^2 - 1 \approx 15\ \%$ at a 2D corner. Third-order accurate for smooth functions.
- Lanczos-$a$: $w(x) = \operatorname{sinc}(x)\operatorname{sinc}(x/a)$ for $|x| < a$; sharper passband and larger ringing than Keys for $a = 3$.
- Average (box) over the target footprint: exact for coarsening in the sense that the output is the area mean of the input cells; the frequency response is $\operatorname{sinc}$ with the first null at the new Nyquist frequency.

In 2D all of these are applied separably (rows then columns), so the 2D kernel is the outer product and the 2D overshoot compounds as stated.

**Slope on an anisotropic grid.** With Horn's (1981) 3 × 3 operator and cell sizes $\Delta x = N\cos\varphi\,\Delta\lambda$, $\Delta y = M\,\Delta\varphi$,

$$\frac{\partial z}{\partial x} = \frac{(z_{3} + 2z_{6} + z_{9}) - (z_{1} + 2z_{4} + z_{7})}{8\,\Delta x}, \qquad \frac{\partial z}{\partial y} = \frac{(z_{1} + 2z_{2} + z_{3}) - (z_{7} + 2z_{8} + z_{9})}{8\,\Delta y},$$

$\tan\beta = \sqrt{z_x^2 + z_y^2}$, aspect $= \operatorname{atan2}(z_y, -z_x)$ (conventions vary). Using a single $\Delta$ for both axes scales $z_x$ by $\Delta x/\Delta$, which at 45° with $\Delta = 30$ m is a factor 0.73 — the 27 % understatement of §10.1 — and rotates aspect toward the meridian by up to $\arctan(0.73) - 45° \approx -8.9°$ for a surface sloping at 45° azimuth.

## Validation & uncertainty

Projection and resampling errors are **deterministic given the inputs** — the same source, target, and kernel always produce the same result — but they are not recorded anywhere unless you record them, and they accumulate with every step. Their signature is spatial structure correlated with the terrain (resampling) or with position in the zone (projection), never white noise.

### How errors arise

1. **Projection distortion treated as zero.** Grid distances and areas reported as ground quantities: ±400 ppm (UTM), up to ±1 500 ppm (overextended UTM), $\sec\varphi$ and $\sec^2\varphi$ (Web Mercator), about 2.7 % in distance and 5.4 % in area at the pole for EPSG:3031. **Anisotropic cells treated as square**: E–W slope understated by $1-\cos\varphi$, aspect biased toward N–S.
2. **Resampling smoothing and overshoot.** Elevation changes of a few percent of local relief (bilinear) and ringing of up to ~7–15 % of a step (cubic, Lanczos); slope variance reduced 5–15 % per bilinear pass; pits and peaks created at edges and nodata boundaries.
3. **Repeated resampling.** Each pass compounds smoothing and may shift the surface; three passes (e.g., native → geographic → UTM → State Plane) can move a feature by a cell and reduce slope variance by a third.
4. **Registration errors.** Half-cell shifts from pixel-is-point/area confusion; one-cell shifts from tile edge-overlap handling; `-tap` alignment applied to point-registered data.
5. **Tile and zone seams.** Shears of hundreds of metres from mixed UTM zones; one-cell duplication or gap at SRTM-style tile edges; cell-size discontinuities at Copernicus latitude bands.
6. **Nodata handling.** Kernels that propagate nodata erode valid areas by 1–3 cells; renormalizing kernels bias values near holes; undeclared nodata (0, −32768) gets interpolated into real values, producing −16 000 m cliffs along coastlines.

### How they propagate

Elevation changes from resampling are small in absolute terms (centimetres to a few metres) but structured — concentrated at crests, channels, and edges, exactly where hydrological and geomorphological analyses look. Slope and curvature inherit them amplified by the differencing ([Chapter 44](ch44-resolution-and-sampling.md)). Co-registration offsets of half a cell convert to vertical error at $\tan\beta$ and appear as aspect-correlated change in DEM differencing ([Chapter 41](ch41-change-detection.md)). Projection distortion is a multiplicative error in every distance, area, and volume; at UTM magnitudes it is usually below the measurement uncertainty, but it is a *bias*, and biases do not average out over a basin.

### How to test

- **Round-trip test** (Try it, §10.4): reproject and reproject back; the difference map's statistics bound the one-way damage at about half the round-trip values, and its spatial pattern shows where (edges, crests).
- **Registration check**: overlay a hillshade of the DEM on an independent, well-georeferenced layer (orthoimage, lidar intensity, surveyed road centrelines) and look at linear features; a half-cell diagonal offset is visible at 1:2 000 on a 1 m DEM. Quantitatively, run a Nuth–Kääb co-registration ([Chapter 8](ch08-horizontal-datums.md), §8.7) against a trusted DEM — a recovered shift of exactly $(\pm\tfrac{1}{2}\Delta, \pm\tfrac{1}{2}\Delta)$ is the smoking gun.
- **Metadata check**: `gdalinfo` for `AREA_OR_POINT`, origin versus tile name, WKT2 with vertical CRS, and the lineage of resampling steps.
- **Area/volume cross-check**: compute a large polygon's area in the DEM's CRS and on the ellipsoid (GeographicLib `Planimeter`); the ratio is the area distortion factor to apply to any volume from the grid.

> **Uncertainty budget.** One reprojection of a 1″ geographic DEM (mountain terrain, 500 m local relief per km) to 30 m UTM, bilinear kernel. Indicative values; measure them for your data with the round-trip test.
>
> | Component | Effect on elevation | Effect on slope (σ of slope) | Character |
> |---|---|---|---|
> | Bilinear interpolation (one pass) | 0.5–1.5 m RMS; crests −1 to −4 m, channels +1 to +3 m | −5 to −15 % | terrain-correlated |
> | Grid rotation (convergence ≤ 3°) | none directly | aspect rotated by $\gamma$ unless corrected | position-correlated |
> | Cell-size change 21.8 × 30.9 m → 30 × 30 m | none directly | E–W derivative now over 30 m instead of 21.8 m: additional smoothing | axis-dependent |
> | UTM scale factor (0.9996–1.0010) | none | slope × (1/k): ±0.1 % | position-correlated |
> | Half-cell registration error (if made) | ±$\tfrac{1}{2}\Delta\tan\beta$: ±5.5 m on 20° slopes for 30 m | none on slope; large on DoD | systematic, aspect-correlated |
> | Nodata erosion (bilinear) | 1 cell lost at every void/coast edge | — | boundary |
>
> The lesson in the table is the asymmetry: elevation is barely affected, derivatives are substantially affected, and one bookkeeping mistake (registration) outweighs everything else.

### What to report

The native CRS and grid (origin, cell size, registration convention); each reprojection or resampling with source grid, target grid, kernel, nodata handling, and software version; the convergence correction applied to aspect, if any; the scale/area factor used for any distance, area, or volume; and the round-trip statistics if the product has been resampled from a measurement-grade source.

## Software

**Open source.**
- **PROJ**: the projection and transformation engine behind nearly everything else; `proj -V` reports scale factors, convergence, and Tissot parameters at a point (`echo -105 40 | proj +proj=utm +zone=13 -V`); `+proj=tmerc` uses the Krüger–Karney algorithm. Caveat: Web Mercator is `+proj=webmerc`, not `+proj=merc +R=6378137`; mixing them yields metre-level differences.
- **GDAL**: `gdalwarp -r <kernel> -tap -tr -te -ct`, `gdal_translate -a_srs/-a_ullr` for fixing metadata without resampling, `gdaldem` for derivatives (with `-s`; check whether your version scales geographic grids per row before relying on it), `gdalinfo` for `AREA_OR_POINT`. Caveat: the `GTIFF_POINT_GEO_IGNORE` config option disables the half-pixel shift on read; know whether it is set in your environment.
- **GMT**: `grdproject` (reprojection with its own interpolators), `grdsample`, `grdgradient`, and the gridline/pixel registration flag `-r`; `mapproject` for scale and convergence. Caveat: GMT's registration vocabulary (gridline = point, pixel = area) and GDAL's differ in name but not meaning; `grdconvert` handles the exchange.
- **rasterio / rioxarray** (Python): `rasterio.warp.reproject` with `Resampling.*` enumerations, `transform` objects that make the half-pixel arithmetic explicit (`transform * (col + 0.5, row + 0.5)` is a cell centre), `rioxarray.reproject_match` for aligning grids. Caveat: `xarray` coordinates are cell centres by convention; writing them to NetCDF without `bounds` loses the area semantics.
- **GeographicLib**: `TransverseMercatorExact`, `TransverseMercator` (Karney series), `PolarStereographic`, `Planimeter`, `GeoConvert` — the reference implementation to check PROJ against. **QGIS**: GDAL-based reprojection and on-the-fly display reprojection (caveat: the processing toolbox defaults to nearest neighbour, and canvas exports are resampled). **xdem / demcoreg**: for detecting registration offsets empirically.


**Free but closed.** NGS SPCS2022 zone definitions and distortion maps.

**Commercial.** ArcGIS Pro (Project Raster; caveat: defaults to nearest neighbour for continuous rasters, and "snap raster" is the equivalent of `-tap`); Global Mapper (caveat: on-the-fly reprojection hides the resampling that occurs on export); ERDAS IMAGINE; Blue Marble tools for LDP design.

## Standards & guides

- **EPSG Geodetic Parameter Dataset** (IOGP) — projection definitions and parameters by code; the authority for UTM zones, national grids, and the ensemble/axis-order semantics.
- **ISO 19111:2019** and **IOGP Guidance Note 7-2** — the CRS model and the formulas for every EPSG projection method (TM, LCC, polar stereographic, oblique Mercator, LAEA, Web Mercator).
- **OGC GeoTIFF 1.1** (OGC 19-008r4, 2019) — `GTRasterTypeGeoKey` (PixelIsArea/PixelIsPoint), model tiepoints and pixel scale, WKT2 in GeoKeys.
- **OGC Two-Dimensional Tile Matrix Set and Tile Set Metadata** (17-083r2 v1.0, 2019; 17-083r4 v2.0, 2022) — definitions of WebMercatorQuad, WorldCRS84Quad, and the tile addressing conventions.
- **NGS SPCS2022 Policy and SPCS2022 Procedures** (National Geodetic Survey, 2019, with later updates) — SPCS2022 design policy, LDP guidance, distortion tolerances; **NOAA Special Publication NOS NGS 13** (Dennis 2018) gives the history and policy background.

## Pitfalls

- **Computing slope on a lat/lon grid with one cell size.** It happens because the tool defaults to grid units. Detect by slopes near 90° (degrees treated as metres) or by an aspect histogram with excess N–S; avoid by scaling each axis by $M\Delta\varphi$ and $N\cos\varphi\,\Delta\lambda$ or by reprojecting to a conformal CRS first.
- **Cubic or Lanczos resampling creating new pits and peaks.** Overshoot of up to 7–15 % of a step at cliffs, building edges, and nodata boundaries. Detect by comparing min/max of source and target and by sink-filling statistics (new sinks appear along edges); avoid with bilinear for elevation, or cubic only where the surface is smooth and edges are masked.
- **Web Mercator in area, volume, or slope computations.** Area scale $\sec^2\varphi$: a factor of 4 at 60°. Detect by latitude-dependent bias; avoid by using an equal-area or conformal CRS and treating Web Mercator as a display/tiling scheme only.
- **UTM zone mismatch at seams.** Tiles from adjacent zones mosaicked as one grid: hundreds of metres of shear. Detect by a straight discontinuity along a meridian and a rotation of linear features; avoid by reprojecting every input to a single CRS before mosaicking.
- **Forgetting the half-cell shift when converting registration conventions.** Pixel-is-point data read as area, or vice versa: $\tfrac{1}{2}\Delta$ diagonal offset. Detect by comparing the file's origin with its nominal tile boundary and by Nuth–Kääb shifts of exactly half a cell; avoid by reading `AREA_OR_POINT` and verifying with `gdalinfo` after any conversion.
- **Reprojecting the same DEM repeatedly.** Each pass smooths and shifts. Detect by the lineage (if any) and by slope-variance loss; avoid by reprojecting once from the native product directly to the final grid.
- **Nodata smeared into real values.** Nodata stored as 0 or −32768 without a declared nodata value gets interpolated into coastlines and void edges. Detect by implausible cliffs (−16 000 m) or a thin band of near-zero elevations along coasts; avoid by declaring nodata before warping and checking the kernel's nodata policy.
- **Treating a "ground" or modified grid as the real State Plane/UTM.** Coordinates scaled by $1/CSF$ look like the official grid and are off by hundreds of ppm (tens of metres across a project). Detect by comparing a control point's coordinates in both; avoid by publishing the LDP or scale factor and origin in the WKT2 (as a custom projection), never as a bare name.
- **Aspect without convergence correction; overviews and web tiles treated as data.** Grid north differs from true north by up to 3° in UTM and by the longitude difference in polar stereographic; COG overviews and Terrain-RGB tiles are resampled copies in Web Mercator. Add $\gamma$ where geographic azimuth matters; analyse the full-resolution base, not the pyramid.

## Key takeaways

- Every projection distorts; choose by what you will compute: conformal for slope and shape, equal-area for area and volume, geographic only for archive and cell-wise work, Web Mercator only for tiles.
- A 1″ cell is ~30.9 m × 30.9 cos φ m; geographic-grid derivatives must scale the two axes separately or they are wrong by $1 - \cos\varphi$ on the E–W axis.
- Grid distance ≠ ground distance: the combined scale factor (grid scale × elevation factor) is ±400 ppm in UTM and matters for engineering; low-distortion projections (SPCS2022 LDPs) are designed to make it ≈ 1, and must ship with full WKT2.
- Reprojection *is* resampling: elevations change by a few percent of local relief, slopes by 5–15 % per bilinear pass, and cubic/Lanczos overshoot creates false pits and peaks at edges; downsample with `average`, never with an interpolator.
- Reproject once, late, directly from the native grid, with the kernel chosen for the quantity of interest, and compute derivatives after; record source grid, target grid, kernel, and nodata handling in the lineage.
- Pixel-is-point and pixel-is-area readings of the same array differ by half a cell; SRTM-family tiles are point-registered with shared edge columns; check `AREA_OR_POINT` and the origin against the tile name before merging anything.
- Zone and tile seams are where mosaics fail: one CRS before mosaicking, the overlap buffer used for a single reprojection, and a seam audit afterwards.

## References

- Airbus Defence and Space (2020 and later revisions). *Copernicus DEM — Copernicus Digital Elevation Model Product Handbook*, GEO.2018-1988-2.
- Battersby, S. E., Finn, M. P., Usery, E. L., & Yamamoto, K. H. (2014). Implications of Web Mercator and its use in online mapping. *Cartographica*, 49(2):85–101. doi:10.3138/carto.49.2.2313
- Dennis, M. L. (2018). *The State Plane Coordinate System: History, Policy, and Future Directions*. NOAA Special Publication NOS NGS 13. National Geodetic Survey, Silver Spring.
- National Geodetic Survey (2019, updated). *SPCS2022 Policy* and *SPCS2022 Procedures*. NOAA/NGS, Silver Spring.
- Duchon, C. E. (1979). Lanczos filtering in one and two dimensions. *Journal of Applied Meteorology*, 18(8):1016–1022.
- Evenden, G. I. (1990). *Cartographic Projection Procedures for the UNIX Environment — A User's Manual*. USGS Open-File Report 90-284. ⟨H⟩
- Grohmann, C. H. (2015). Effects of spatial resolution on slope and aspect derivation for regional-scale analysis. *Computers & Geosciences*, 77:111–117. doi:10.1016/j.cageo.2015.02.003
- Horn, B. K. P. (1981). Hill shading and the reflectance map. *Proceedings of the IEEE*, 69(1):14–47.
- Iliffe, J., & Lott, R. (2008). *Datums and Map Projections for Remote Sensing, GIS and Surveying* (2nd ed.). Whittles Publishing, Dunbeath.
- IOGP (current revision). *Coordinate Conversions and Transformations including Formulas*. Geomatics Guidance Note 7, part 2.
- Karney, C. F. F. (2011). Transverse Mercator with an accuracy of a few nanometers. *Journal of Geodesy*, 85(8):475–485. doi:10.1007/s00190-011-0445-3
- Keys, R. G. (1981). Cubic convolution interpolation for digital image processing. *IEEE Transactions on Acoustics, Speech, and Signal Processing*, 29(6):1153–1160. doi:10.1109/TASSP.1981.1163711
- Krüger, L. (1912). *Konforme Abbildung des Erdellipsoids in der Ebene*. Veröffentlichung des Königlich Preuszischen Geodätischen Instituts, Neue Folge 52. Potsdam.
- OGC (2019). *OGC GeoTIFF Standard*, version 1.1, OGC 19-008r4. Open Geospatial Consortium.
- OGC (2022). *OGC Two Dimensional Tile Matrix Set and Tile Set Metadata*, version 2.0, OGC 17-083r4. Open Geospatial Consortium.
- Rodríguez, E., Morris, C. S., & Belz, J. E. (2006). A global assessment of the SRTM performance. *Photogrammetric Engineering & Remote Sensing*, 72(3):249–260.
- Snyder, J. P. (1987). *Map Projections — A Working Manual*. USGS Professional Paper 1395. US Government Printing Office, Washington. ⟨H⟩
- Snyder, J. P. (1993). *Flattening the Earth: Two Thousand Years of Map Projections*. University of Chicago Press, Chicago.
- Zevenbergen, L. W., & Thorne, C. R. (1987). Quantitative analysis of land surface topography. *Earth Surface Processes and Landforms*, 12(1):47–56.

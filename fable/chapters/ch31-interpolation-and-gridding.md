# Chapter 31 — Interpolation, gridding, and grid registration

> **Part VII — From sensor data to products.** The third processing chapter: how labelled points become a continuous surface, what a cell value actually means, and why two correct grids of the same terrain can disagree by half a cell and a whole hillside.

**In this chapter.** A grid is the most common elevation product and the least self-describing. You will be able to choose among the standard interpolators—nearest neighbour, inverse distance weighting, TIN-linear, natural neighbour, thin-plate and regularized splines, ordinary and universal kriging, ANUDEM's drainage-enforced spline, binning statistics, CUBE node estimation, moving least squares, and Poisson reconstruction—on the basis of point density, terrain, and purpose rather than habit. You will understand the undocumented decision that breaks more comparisons than any other: whether a cell value is a point sample at the cell centre or a statistic over the cell's area, and whether the grid is pixel-is-area or pixel-is-point registered. You will handle breaklines, voids, and edges; set cell size from point spacing; build overviews that do not lie; and quantify interpolation uncertainty with kriging variance, cross-validation, and distance-to-observation layers. A worked experiment compares six methods on one lidar tile and shows how large the differences are, where they occur, and how to report them.

## 31.1 Methods

Interpolation estimates the value of a field at a location where it was not measured from values where it was. Every method encodes an assumption about how the field behaves between samples, and the error of the method is the mismatch between that assumption and the terrain. The methods below are ordered roughly from local and assumption-light to global and model-heavy.

**Nearest neighbour** assigns each cell the value of the closest point. It is exact at the data, piecewise constant between them (Voronoi cells), introduces no new values, and produces a stair-stepped surface with slope artefacts at every Voronoi boundary. It is appropriate for categorical data and for resampling a grid without inventing values; it is a poor DEM interpolator except as a baseline.

**Inverse distance weighting (IDW)** (Shepard 1968) estimates $\hat z(x) = \sum_i w_i z_i / \sum_i w_i$ with $w_i = d_i^{-p}$ over the $n$ nearest points or all points within a radius. The power $p$ (commonly 2) controls locality; higher $p$ approaches nearest neighbour, lower $p$ approaches a moving average. IDW is exact at the data, bounded by the data range (no overshoot), and simple, but it produces "bull's-eyes" around isolated points, flattens peaks and pits between samples (the estimate can never exceed the samples), and its smoothness depends on sample configuration rather than on terrain. Within a dense lidar cloud at cell sizes near the point spacing, IDW with a small radius behaves like a local mean and is the pragmatic default in PDAL's `writers.gdal`.

**TIN-linear** builds a Delaunay triangulation of the points (Delaunay 1934; the TIN as a terrain model is due to Peucker et al. 1978 ⟨H⟩) and interpolates linearly within each triangle. It is exact, local, bounded, and honours breaklines when they are enforced as triangle edges (constrained Delaunay). Its surface is $C^0$ (continuous but with slope discontinuities at every edge), so slope and curvature derived from it show triangle facets; in sparse data, long thin triangles across valleys create the characteristic "flat-triangle" artefacts of early contour-derived DEMs. For dense lidar it is the most honest interpolator: no smoothing, no invention, and errors confined to within-triangle linearity.

**Natural neighbour** (Sibson 1981) inserts the query point into the Voronoi diagram and weights each neighbour by the area its Voronoi cell loses to the new point (see Mathematics). It is exact, local, bounded, $C^1$ everywhere except at the data points, adapts automatically to anisotropic sampling, and has no parameters—which is why it is a reliable default for irregular data of moderate density. It cannot extrapolate beyond the convex hull.

**Splines** minimise a roughness functional subject to fitting the data. The **thin-plate spline (TPS)** minimises the integrated squared second derivatives (bending energy) and passes exactly through the points; **regularized** or **smoothing** splines add a penalty weight so that the surface passes near rather than through the points, trading fidelity for smoothness and suppressing noise. The **regularized spline with tension** (Mitášová & Mitáš 1993; Mitas & Mitasova 1999; GRASS `v.surf.rst`) adds a tension parameter that controls the transition from membrane (tension high, surface stiff and local) to thin plate (tension low, surface smooth and global). Splines are $C^2$, differentiate cleanly, and are excellent for smooth terrain; they **overshoot** at breaklines and in steep terrain (the surface rings like a struck plate around a cliff), and they extrapolate aggressively across voids.

**Kriging** (Matheron's formalisation of Krige's method; Cressie 1993; Chilès & Delfiner 2012) treats the field as a realisation of a random process with a covariance structure estimated from the data through the **variogram** $\gamma(h) = \tfrac{1}{2}\,\mathrm{E}[(z(x) - z(x+h))^2]$, and computes the best linear unbiased predictor given that structure. **Ordinary kriging** assumes an unknown constant mean; **universal kriging** (kriging with a trend) allows a polynomial or external drift. Its distinctive output is the **kriging variance**, a prediction uncertainty at every cell that depends on the sample configuration and the variogram but not on the sample values. Kriging is optimal when the model is right and the data are stationary, computationally heavy at lidar densities (local neighbourhoods are mandatory), and only as good as the variogram; terrain is rarely stationary, so universal kriging or kriging of residuals from a trend is usual. For dense lidar it offers little over natural neighbour; for sparse bathymetry, scattered spot heights, or borehole surfaces it is the right tool.

**ANUDEM / Topo to Raster** (Hutchinson 1989) is a discretised thin-plate spline with a roughness penalty tuned for terrain and, critically, a **drainage-enforcement** step that iteratively removes spurious sinks and, where stream lines are supplied, forces the surface to descend monotonically along them. It was designed for contour and spot-height inputs and remains the standard for building hydrologically sound DEMs from such data; for lidar it is used when a hydro-conditioned product is the goal. Its enforcement is a modelling assumption—real terrain has closed depressions—and must be reported as such ([Chapter 34](ch34-water-in-dems.md), [Chapter 61](ch61-hydrology.md)).

**Binning** assigns each cell a statistic of the points that fall inside it: mean, median, minimum, maximum, count, standard deviation, or a percentile. It is not interpolation (empty cells stay empty) but at lidar densities it is the dominant way grids are made: GMT's `blockmean`/`blockmedian`/`blockmode`, GDAL's `gdal_grid` with `average`/`minimum`/`maximum`/`count` and the `-a` data-metrics algorithms, PDAL's `writers.gdal` with `output_type` of `min`, `max`, `mean`, `idw`, `count`, `stdev`. The statistic chosen defines the product (Section 31.2).

**CUBE node estimation** (Calder & Mayer 2003) is a bathymetric gridding method that weights each sounding's contribution to a node by its propagated uncertainty and distance, maintains competing hypotheses, and reports the selected hypothesis's depth and uncertainty; it is binning with a Bayesian update, uncertainty propagation, and outlier resistance ([Chapter 30](ch30-point-cloud-classification.md)).

**Moving least squares (MLS)** fits a low-order polynomial to the weighted neighbourhood of each query point; it smooths noise and differentiates well, and rounds sharp features. **Poisson surface reconstruction** (Kazhdan, Bolitho & Hoppe 2006) solves for an indicator function whose gradient matches oriented point normals and extracts a watertight mesh; it is a true-3D method (overhangs, caves; [Chapter 35](ch35-voids-and-overhangs.md)), not a 2.5D gridder, and it hallucinates surface across holes by construction.

<!-- figure: Figure 31.1 — One cross-section of lidar ground points through a terrace and a small gully, with the surfaces produced by nearest, IDW (p=2), TIN-linear, natural neighbour, TPS, and ordinary kriging overlaid; annotations mark IDW's flattening of the gully, the spline's overshoot at the terrace edge, and the TIN facets. -->

> **Rule of thumb.** At cell sizes near or above the mean point spacing (dense lidar), the choice among exact local interpolators—TIN-linear, natural neighbour, small-radius IDW, or mean binning—changes the surface by less than the per-point noise over smooth ground; what matters there is the cell semantics and the breaklines. At cell sizes well below the spacing (sparse soundings, spot heights, contours), the interpolator's model dominates and kriging, splines with tension, or ANUDEM must be chosen deliberately and reported. The transition is at a cell size of roughly one to two times the spacing; see Section 31.6.

## 31.2 Choosing by data density and purpose; what a cell value represents

Two decisions must be made for every grid, and most metadata records neither.

The first is the **statistic**. A cell that contains thirty lidar ground points can report their mean (a smooth, low-noise estimate of the average surface), their minimum (the lowest return—closest to bare earth under grass, but also the most sensitive to low noise), their maximum (the highest—a DSM of obstacles), their median (robust to a few outliers), or the value of an interpolator evaluated at the cell centre. These are different products. A hydrographic chart grid is **shoal-biased**: the cell carries the minimum depth (shallowest sounding), because a navigator who grounds on an unreported shoal is not consoled by an accurate average. A scientific bathymetric compilation for volume or morphology uses the mean or a CUBE estimate. A DSM for airport obstacle analysis or wind modelling uses the maximum. A hydrologic DTM uses an interpolated or mean value, because minimum binning creates artificial pits (every low-noise point becomes a sink) and maximum binning creates dams. Using a min-binned surface for flow routing, or a mean-binned surface for a chart, is a product-definition error, not an accuracy error, and no RMSE will reveal it.

The second is the **support**: does the value represent the field at a point (the cell centre) or an average over the cell's area? Interpolators evaluated at the centre give point support; binning gives area support (the statistic of everything inside the cell). The distinction matters whenever two grids are compared or a grid is resampled. Differencing a point-support grid against an area-support grid of the same terrain yields a systematic difference that depends on terrain curvature: over a convex ridge the area mean is lower than the centre value; over a concave valley it is higher. At 1 m cells the effect is centimetres; at 30 m cells in mountains it can reach metres. Change-detection studies that difference products with different supports see "change" that is curvature ([Chapter 41](ch41-change-detection.md)).

> **Definitions that bite.** "Resolution" in a grid's metadata is the cell spacing. It says nothing about the support (point or area), the statistic, the interpolator, the effective resolution (the smallest feature actually resolvable, which for a smoothed or oversampled grid is several cells), or the registration (Section 31.3). A "1 m DEM" can be a point-sampled TIN at cell centres, a mean of eight returns per cell, or a 5 m product resampled bicubically to 1 m. Only the lineage tells you which ([Chapter 29](ch29-processing-pipelines.md), [Chapter 44](ch44-resolution-and-sampling.md)).

Density guides the method. With many points per cell, binning statistics or an exact local interpolator are appropriate, the interpolator's assumptions are almost irrelevant, and the choice of statistic is the whole decision. With about one point per cell, TIN-linear or natural neighbour is the honest choice, and the cell count layer should be delivered so the user can see which cells were measured. With fewer than one point per cell—sparse soundings, spot heights, contours, GEDI or ICESat-2 footprints—the surface between samples is a model; kriging gives the most defensible estimate with an uncertainty, splines give the smoothest, ANUDEM the most hydrologically plausible, and the interpolation mask (Section 31.5) is as important as the elevation.

## 31.3 Grid registration: pixel-is-area, pixel-is-point, half-cell shifts

A grid's **registration** defines where its sample locations are relative to its stated extent. Under **pixel-is-area** (GeoTIFF `RasterPixelIsArea`, GMT "pixel registration"), each cell is a rectangle; the value is attributed to the whole rectangle (or, for point-support data, to its centre), and the grid's extent runs from the outer edge of the first cell to the outer edge of the last. A 1° tile at 1″ has 3,600 × 3,600 cells whose centres lie at half-arc-second offsets from the integer degree lines. Under **pixel-is-point** (GeoTIFF `RasterPixelIsPoint`, GMT "gridline registration"), each value is a sample at a node, the nodes lie on the grid lines including the boundary, and a 1° tile at 1″ has 3,601 × 3,601 nodes whose outermost rows and columns lie exactly on the integer degree lines and are shared with the neighbouring tiles.

The two conventions describe the same sample locations with origins that differ by half a cell. If software reads a pixel-is-point grid as pixel-is-area (or the metadata tag is missing and a default applies), every value is displaced by half a cell diagonally—15 m at 1″, 0.5 m at 1 m. On flat ground this is invisible. On a slope of gradient $s$ it appears as a vertical error of $\Delta z \approx s \cdot \Delta x$: on a 30 % slope a 15 m shift produces a 4.5 m apparent elevation error, aligned with the aspect, that looks exactly like a systematic bias in a DEM comparison and is in fact a registration mismatch. The ASTER GDEM, SRTM, and the original Copernicus DEM tiles are all distributed as 3,601-sample tiles with the outermost rows and columns shared between neighbours—node-registered data—while the cloud-optimised redistribution of Copernicus DEM drops the shared east and south edges to give 3,600 × 3,600 tiles whose values still refer to pixel centres; and the GeoTIFF tags of various redistributions have not always said so consistently. Checking the registration of each product against a known feature before any comparison is the single highest-value validation step in [Chapter 55](ch55-public-products.md)'s product comparisons.

GMT makes the distinction explicit with the `-r` flag (pixel registration on; gridline registration by default) and `grdedit -T` toggles between them without resampling (it changes the extent by half a cell, not the values). GDAL exposes `AREA_OR_POINT` metadata and, since GDAL 1.x, applies a half-pixel shift to the geotransform when reading `RasterPixelIsPoint` GeoTIFFs so that its internal model is always pixel-is-area with the stated geotransform; the configuration option `GTIFF_POINT_GEO_IGNORE` disables this. The practical consequence is that the same file read by two libraries with different conventions can place the data half a cell apart—and that re-saving a file through a tool that writes `AREA_OR_POINT=Area` while keeping the point geotransform silently moves the grid.

> **Worked example.** Two 1″ DEMs of the same mountainous area are differenced and show a mean difference of +0.1 m but an RMSE of 6.2 m, with the difference map strongly correlated with aspect (positive on east-facing slopes, negative on west-facing). Fitting the difference $\Delta z$ against the slope components, $\Delta z \approx a\,\partial z/\partial x + b\,\partial z/\partial y$, gives $a = +14.8$ m, $b = -15.1$ m: a horizontal offset of about 21 m along the NW–SE diagonal, i.e. half a cell in each axis (at this site's latitude of about 20°, half of 1″ is 14.5 m in x and 15.4 m in y) within noise. Shifting one grid by half a cell and re-differencing reduces the RMSE to 1.9 m. The "6 m RMSE" was never an elevation error; it was a registration mismatch, and it would have been reported as a product accuracy in a less careful study. The slope-regression test (Nuth & Kääb 2011 give the aspect-based form) belongs in every DEM comparison ([Chapter 41](ch41-change-detection.md)).

The edge-overlap convention has a corollary for mosaics. Node-registered tiles share their boundary rows and columns; mosaicking them with a tool that assumes pixel-is-area and non-overlapping extents either duplicates or drops those rows, producing a one-cell seam every degree that shows as a hairline in a hillshade and as a one-cell shift in everything east or south of it. GDAL's `gdalwarp` handles overlapping node-registered inputs correctly when the tags are right; `gdal_merge.py` and naive array concatenation do not.

<!-- figure: Figure 31.2 — Pixel-is-area and pixel-is-point registration drawn for the corner of a 1° tile: cell rectangles and their centres versus nodes on the grid lines, the half-cell offset between the two origins, and the shared boundary row between adjacent node-registered tiles. -->

## 31.4 Breaklines, hydro-flattening inputs, and anisotropy

Terrain has discontinuities—cliff edges, retaining walls, levee crests, road shoulders, stream banks—and a smooth interpolator crosses them as if they were not there, rounding the crest and smearing the toe. A **breakline** is a 3D polyline that tells the interpolator where the surface bends or breaks. A **hard breakline** forces a slope discontinuity: the surface is $C^0$ across it but its gradient may jump (a kerb, a wall top, a water's edge). A **soft breakline** marks a line the surface must pass through without a slope discontinuity (a ridge line or drainage line that should be honoured as a feature but is smooth). In TIN construction both are enforced as constrained edges, with hard breaklines additionally preventing the smoothing of slope across them in any subsequent surface fitting. In grid interpolation they are enforced by densifying the breakline into points with higher weight, by treating them as barriers in the neighbourhood search, or by ANUDEM's stream and cliff-line inputs.

Hydro-flattening ([Chapter 34](ch34-water-in-dems.md)) is a breakline application: lake shorelines are hard breaklines at a constant elevation and river banks are paired breaklines with monotonic downstream elevations, and the interpolator is forced to a flat (lake) or planar-monotonic (river) surface between them. The USGS Lidar Base Specification requires the breaklines as a deliverable so that the DTM can be regenerated; a DTM delivered without them cannot be rebuilt consistently.

**Anisotropy** is directional dependence in the terrain's spatial correlation: dunes, drumlins, ploughed fields, and terraced hillsides vary more rapidly across their grain than along it. Isotropic interpolators smear across the grain. Kriging handles anisotropy through a directional variogram (different ranges along the major and minor axes); IDW and splines can be given an anisotropy ratio and angle that rescale coordinates before the distance computation; TIN-linear and natural neighbour inherit whatever anisotropy the sample layout provides. Sample geometry also matters: lidar scan lines and multibeam swaths are denser along track than across, so a neighbourhood search that selects the $n$ nearest points may draw them all from one scan line—a quadrant or octant search (GDAL `gdal_grid` `min_points_per_quadrant`, GMT `nearneighbor -N`) prevents this.

## 31.5 Interpolation across voids and edge effects; flagging interpolated cells

Every interpolator will fill a hole if asked, and the fill is a model, not a measurement. The three regimes are: **within-support interpolation** between points at normal density, where the error is the within-cell terrain variability; **void filling** across gaps larger than a few cells (water bodies, building footprints, shadows, dropouts, lidar swath gaps), where the error grows with the gap width and the terrain's roughness; and **extrapolation** beyond the convex hull of the data at the grid's edges, where splines and kriging with trends diverge and even bounded interpolators simply continue the last values. [Chapter 35](ch35-voids-and-overhangs.md) treats voids in depth; the gridding rules are these.

Measure the void, do not guess: a **distance-to-nearest-observation** raster (GDAL `gdal_proximity.py` on the observation mask) and a per-cell **count** raster cost nothing and tell the user where the surface is measured, where it bridges a short gap, and where it is invented. Set a maximum search radius for interpolation and leave cells beyond it as nodata rather than let a spline bridge a lake; fill large voids deliberately with a documented method (`gdal_fillnodata.py`, which uses inverse-distance weighting from the void edge with optional smoothing; delta-surface fill from an auxiliary DEM, as used for SRTM void filling; or a hydrologically constrained fill), and write the void mask into the product. Clip the final grid to a buffer inside the data hull, since the outermost cells of any gridded product are extrapolations. The Copernicus DEM's Edit Data Mask, Filling Mask, and Height Error Mask ([Chapter 32](ch32-dsm-to-dtm.md)) are the model: a product that ships with an interpolation mask has told the truth about itself; one that does not has asked to be trusted.

## 31.6 Cell size relative to point spacing

Cell size is a resolution choice and a lie detector. If the mean point spacing is $\bar d = \sqrt{A/N}$ for $N$ points over area $A$, then a cell size $c \gg \bar d$ averages many points per cell (smooth, low noise, features smaller than $c$ lost), $c \approx \bar d$ puts roughly one point per cell (honest, noisy, some cells empty), and $c \ll \bar d$ is **oversampling**: most cells contain no point and are interpolated, and the grid's apparent resolution is fiction. Hengl (2006) gives a systematic treatment with several rules relating cell size to sampling density, the variogram range, and the intended map scale; the recurring conclusion is that the cell size should be chosen from the data's information content and that halving the cell size without more data adds smoothness, not detail. The Nyquist view says the same thing: a surface sampled at spacing $\bar d$ carries no information about wavelengths shorter than $2\bar d$, and resampling to a finer grid cannot recover them.

Oversampling is seductive because the hillshade of a finely interpolated grid looks sharper. Its consequences are concrete: slope and curvature are those of the interpolator, not the terrain; volumes gain false precision; the "resolution" field misleads every future user; and storage grows as $c^{-2}$ for nothing. The USGS LBS ties DEM cell size to lidar quality level (QL1/QL2: 0.5 m or 1 m DEMs from ≥ 8 and ≥ 2 pt/m², i.e. spacings of ≤ 0.35 m and ≤ 0.71 m; QL3: 2 m from ≥ 0.5 pt/m²—check the current edition for the exact table), which keeps cell size at or above point spacing. Report effective resolution alongside cell size ([Chapter 44](ch44-resolution-and-sampling.md)).

## 31.7 Overviews, pyramids, and level of detail

Overviews (pyramids) are reduced-resolution copies of a grid stored alongside it so that a viewer or an analysis at coarse scale need not read every cell. Each level aggregates a 2 × 2 (or larger) block of the level below into one cell, and the aggregation rule defines what the overview means. **Average** gives a smooth, visually pleasing overview whose cells are area means—and whose maxima and minima are gone: a ridge crest, a tower, a channel thalweg, or a shoal disappears from the overview even though it is in the base level. **Nearest** keeps one of the four values arbitrarily (fast; preserves categorical data; makes elevation overviews noisy and position-dependent). **Minimum** and **maximum** preserve the shoal-biased or obstacle-biased semantics that charts and obstacle analyses require. **Bilinear**, **cubic**, **Lanczos**, and **Gauss** are smoothing kernels with different frequency responses; cubic and Lanczos can overshoot. GDAL's `gdaladdo -r {nearest,average,rms,bilinear,gauss,cubic,cubicspline,lanczos,average_magphase,mode}` exposes the choice; the COG driver's `OVERVIEW_RESAMPLING` creation option does the same.

Overviews lie in two ways. Semantic drift: a chart grid with min-binned base cells and average-resampled overviews shows deeper water when zoomed out—exactly the wrong direction. Silent use: tiled viewers and cloud platforms choose the overview level from the display scale, so a computation at a coarse output scale may run on an overview without the user knowing (Earth Engine's per-asset pyramid policy—mean, sample, min, max, or mode—is the documented example; [Chapter 29](ch29-processing-pipelines.md)). The rule is to choose the overview resampling to match the product semantics (min for charts, max for obstacles, average for scientific DEMs), to record it in metadata, and to perform quantitative work at the base level or on an overview whose aggregation is known ([Chapter 46](ch46-data-models.md), [Chapter 57](ch57-visualizing-dems.md)).

## 31.8 Interpolation uncertainty

An interpolated value without an uncertainty is a guess with a decimal point. Four tools give the uncertainty, with increasing cost and realism.

**Kriging variance** $\sigma_K^2(x)$ is the prediction variance under the fitted variogram model; it is zero at the data points (for exact kriging), grows with distance from them, and depends only on the sample geometry and the variogram, not on the local terrain roughness—so it understates uncertainty in rough areas and overstates it in smooth ones unless the variogram is estimated locally. It is nonetheless the only widely available analytic uncertainty surface and is the basis of the uncertainty layers in many bathymetric compilations.

**Cross-validation** withholds data and predicts it. *Leave-one-out* removes each point in turn, predicts it from the rest, and summarises the residuals (mean, RMSE, 95th percentile, by stratum); it is cheap, model-agnostic, and tests the interpolator at the data density, not in the voids. *k-fold* or *block* cross-validation withholds spatial blocks or whole swaths to emulate void filling, and is the correct test when the question is how the interpolator behaves across gaps of a given size (Amante & Eakins 2016 did exactly this for coastal DEMs, withholding soundings and measuring interpolation error as a function of distance to the nearest remaining sounding and of terrain slope). The result is an empirical error model, $\sigma(d, s)$, as a function of distance to data and slope, that can be applied cell by cell to produce an uncertainty raster.

**Bootstrap and Monte Carlo** resample the input points (with replacement, or with perturbations drawn from their stated uncertainties) and re-grid many times; the per-cell spread of the ensemble is the interpolation plus input uncertainty. Jakobsson, Calder & Mayer (2002) applied this to gridded bathymetric compilations and showed that the random error of a compilation grid depends strongly on the sounding density and the gridding method, and that the error surface must accompany the grid. For compilations assembled from heterogeneous sources it is the only method that captures the real structure.

**Distance and density layers** are the minimum: distance to nearest observation, count per cell, and within-cell standard deviation. They are not uncertainties in themselves, but with an empirical cross-validation model they become one, and even alone they tell the user where to be careful.

> **Try it.** A worked experiment comparing six gridding methods on one lidar tile. Expected outcome: six 1 m DTMs from the same ground points, a table of leave-out residuals (mean, RMSE, 95th percentile) per method, and a difference map between the two most different methods showing where they disagree (breaklines and gaps, not open ground). The withheld 10 % of ground points serve as independent checkpoints.
>
> ```bash
> # 1. Split ground points 90/10 (deterministic: every 10th point is a checkpoint).
> for s in "train 1" "check 0"; do set -- $s
>   pdal translate tile_ground.laz $1.csv \
>     -f filters.range --filters.range.limits="Classification[2:2]" \
>     -f filters.decimation --filters.decimation.step=10 --filters.decimation.offset=$2 \
>     --writers.text.order="X,Y,Z" --writers.text.keep_unspecified=false
> done
> ogr2ogr -f GPKG train.gpkg train.csv -oo X_POSSIBLE_NAMES=X -oo Y_POSSIBLE_NAMES=Y \
>   -oo Z_POSSIBLE_NAMES=Z -a_srs EPSG:6339
> read XMIN XMAX YMIN YMAX < <(gmt info train.csv -C -I1 | awk '{print $1,$2,$3,$4}')
> R="-R$XMIN/$XMAX/$YMIN/$YMAX"                       # common extent, 1 m cells
> C="-txe $XMIN $XMAX -tye $YMIN $YMAX -tr 1 1 -ot Float32 -a_srs EPSG:6339 -zfield Z"
>
> # 2. Six surfaces on the same grid.
> gdal_grid -a nearest:radius=3 $C train.gpkg dtm_nearest.tif
> gdal_grid -a invdist:power=2:radius=3:min_points=3 $C train.gpkg dtm_idw.tif
> gdal_grid -a average:radius=1.0:min_points=1 $C train.gpkg dtm_mean.tif
> gdal_grid -a linear:radius=5 $C train.gpkg dtm_tin.tif
> gmt surface train.csv $R -I1 -T0.35 -r -Gdtm_spline.tif=gd:GTiff
> gmt nearneighbor train.csv $R -I1 -S3 -N4 -r -Gdtm_nn.tif=gd:GTiff
>
> # 3. Residuals at the withheld points, per method.
> python3 - <<'EOF'
> import numpy as np, rasterio
> pts = np.loadtxt("check.csv", delimiter=",", skiprows=1)
> for name in ["nearest","idw","mean","tin","spline","nn"]:
>     with rasterio.open(f"dtm_{name}.tif") as ds:
>         z = np.array([v[0] for v in ds.sample(pts[:,:2])], float); nod = ds.nodata
>     ok = np.isfinite(z) & ((z != nod) if nod is not None else True)
>     r = z[ok] - pts[ok,2]
>     print(f"{name:8s} n={ok.sum():6d} mean={r.mean():+.3f} "
>           f"rmse={np.sqrt((r**2).mean()):.3f} p95={np.percentile(abs(r),95):.3f}")
> EOF
> gdal_calc.py -A dtm_spline.tif -B dtm_tin.tif --outfile=diff_spline_tin.tif --calc="A-B"
> ```
>
> On a typical 8 pt/m² tile of rolling farmland with hedgerows and a stream, expect RMSE values of a few centimetres for TIN, natural neighbour, and mean, slightly larger for IDW and nearest, and a comparable RMSE but a larger 95th percentile for the spline, with its tail concentrated along the stream banks and hedgerow bases where it overshoots. The difference map is the deliverable insight: the methods agree over open ground to within noise and disagree at breaklines and in the gaps under the hedgerows, which is where the user should be warned and where breaklines or a void mask are needed.

## Then & now

- **1930s–1960s.** Delaunay's triangulation (1934) and Voronoi's tessellation (1908) preceded their use in terrain by decades. Early DEMs were digitised from contours and gridded by hand-tuned local polynomial fits; the "flat triangle" and "contour ghost" artefacts of those products are still visible in some national DEMs.
- **1968–1981.** Shepard's IDW (1968) for computer mapping; Matheron's geostatistics (1960s) and its DEM applications in the 1970s; the TIN as a terrain model (Peucker et al. 1978 ⟨H⟩) and Sibson's natural neighbour (1981) gave the field its exact local interpolators.
- **1989–1990s.** Hutchinson's ANUDEM (1989) introduced drainage enforcement and became ArcInfo's TOPOGRID, then Topo to Raster; GMT's `surface` (Smith & Wessel 1990) brought tensioned minimum-curvature gridding to open-source geoscience; the SRTM mission (2000) fixed 3,601 × 3,601 node-registered 1° tiles as a de facto global convention.
- **2002–2003.** Jakobsson, Calder & Mayer (2002) quantified random error in gridded bathymetric compilations; CUBE (2003) made the uncertainty layer a first-class output of hydrographic gridding, which the BAG format (2006) then standardised.
- **2006.** Hengl's "Finding the right pixel size" gave practitioners defensible rules for cell size; Poisson surface reconstruction (Kazhdan et al. 2006) opened true-3D surface recovery for point clouds.
- **2011–present.** Lidar densities made binning the dominant gridding method and shifted the hard questions from interpolator choice to cell semantics, registration, and masks; Cloud-optimized GeoTIFF (2016 onward) made overview resampling a published, inspectable property of every product; Amante & Eakins (2016) and successors turned cross-validation into per-cell uncertainty rasters for coastal DEMs.

## Mathematics

**IDW.** For query location $x$ and samples $z_i$ at $x_i$ with distances $d_i = \|x - x_i\|$,
$$ \hat z(x) = \frac{\sum_{i=1}^{n} d_i^{-p}\, z_i}{\sum_{i=1}^{n} d_i^{-p}}, \qquad \hat z(x_i) = z_i, $$
with the second property holding in the limit $d_i \to 0$. Because the weights are positive and sum to one, $\min_i z_i \le \hat z \le \max_i z_i$: IDW cannot overshoot, and cannot represent a peak or pit between samples.

**Thin-plate spline.** The TPS $f$ minimises the bending energy
$$ J(f) = \iint \left[ \left(\frac{\partial^2 f}{\partial x^2}\right)^2 + 2\left(\frac{\partial^2 f}{\partial x\,\partial y}\right)^2 + \left(\frac{\partial^2 f}{\partial y^2}\right)^2 \right] dx\,dy $$
subject to $f(x_i) = z_i$ (exact) or minimising $\sum_i (f(x_i) - z_i)^2 + \lambda J(f)$ (smoothing, with $\lambda$ the regularisation weight). The solution is $f(x) = a_0 + a_1 x + a_2 y + \sum_i w_i\, \phi(\|x - x_i\|)$ with radial basis $\phi(r) = r^2 \ln r$, the coefficients found from a linear system with the side conditions $\sum_i w_i = \sum_i w_i x_i = \sum_i w_i y_i = 0$. Tension adds a first-derivative term to $J$ weighted by $\tau$, stiffening the surface toward a membrane.

**Variogram and ordinary kriging.** The empirical semivariogram for lag $h$ is
$$ \hat\gamma(h) = \frac{1}{2\,|N(h)|} \sum_{(i,j) \in N(h)} \left(z_i - z_j\right)^2, $$
fitted with a licit model (spherical, exponential, Gaussian, Matérn) with nugget $c_0$, partial sill $c$, and range $a$; e.g. spherical $\gamma(h) = c_0 + c\,[\,1.5\,h/a - 0.5\,(h/a)^3\,]$ for $h \le a$, $c_0 + c$ beyond. Ordinary kriging predicts $\hat z(x_0) = \sum_i \lambda_i z_i$ with weights from
$$ \begin{bmatrix} \Gamma & \mathbf{1} \\ \mathbf{1}^\top & 0 \end{bmatrix} \begin{bmatrix} \boldsymbol\lambda \\ \mu \end{bmatrix} = \begin{bmatrix} \boldsymbol\gamma_0 \\ 1 \end{bmatrix}, $$
where $\Gamma_{ij} = \gamma(x_i - x_j)$, $(\boldsymbol\gamma_0)_i = \gamma(x_i - x_0)$, and $\mu$ is the Lagrange multiplier enforcing $\sum_i \lambda_i = 1$. The kriging variance is $\sigma_K^2(x_0) = \boldsymbol\lambda^\top \boldsymbol\gamma_0 + \mu$.

**Natural neighbour (Sibson) weights.** Insert $x_0$ into the Voronoi diagram of the samples. Let $A_i$ be the area of the intersection of the new cell of $x_0$ with the original cell of sample $i$, and $A = \sum_i A_i$ the new cell's area. Then $\hat z(x_0) = \sum_i (A_i / A)\, z_i$. The weights are positive, sum to one, are continuous in $x_0$, and are nonzero only for the natural neighbours (samples whose cells the new cell overlaps), which adapts the neighbourhood to the local sampling pattern.

**Delaunay criterion.** A triangulation of a point set is Delaunay if no sample lies strictly inside the circumcircle of any triangle. Among all triangulations it maximises the minimum angle, which minimises the long thin triangles across which linear interpolation is least reliable; it is unique when no four points are cocircular, and it is the dual of the Voronoi diagram, which is why TIN-linear and natural neighbour are built on the same structure.

**Registration shift as vertical error.** For a DEM with gradient $\nabla z = (\partial z/\partial x,\ \partial z/\partial y)$ and a horizontal displacement $(\delta_x, \delta_y)$ between two grids, the first-order apparent elevation difference is $\Delta z \approx \delta_x\,\partial z/\partial x + \delta_y\,\partial z/\partial y$, which is the regression used in the worked example of Section 31.3 and the basis of the Nuth & Kääb (2011) co-registration.

## Validation & uncertainty

Gridding error has three sources, and a validation plan must separate them because they have different remedies. **Sampling error** is the terrain variability the samples did not capture—the within-cell relief at high density, the between-sample relief at low density; it is reduced only by more data. **Model error** is the interpolator's mismatch with the terrain—IDW flattening, spline overshoot, kriging with the wrong variogram, ANUDEM enforcing drainage through a real closed basin; it is reduced by choosing and tuning the method per terrain. **Definition error** is the mismatch between the product's cell semantics and registration and what the user assumed—min versus mean, point versus area, area versus point registration; it is not reduced by any amount of data and is eliminated only by documentation and by checking.

> **Uncertainty budget.** Gridding-stage contributions to a 1 m lidar DTM at 8 pt/m² (mean spacing ≈ 0.35 m), and to a 10 m bathymetric compilation from soundings at 50–500 m spacing. Magnitudes are indicative, drawn from the cross-validation literature (Amante & Eakins 2016; Jakobsson et al. 2002) and routine lidar QA; measure your own.
>
> | Component | 1 m lidar DTM | 10 m sparse bathymetry | Test |
> |---|---|---|---|
> | Within-cell/between-sample relief (smooth terrain) | 1–3 cm | 0.1–0.5 m | Leave-one-out residuals, open ground |
> | Same, at breaklines / steep slopes | 10–50 cm locally | 1–10 m | Residuals stratified by slope and curvature |
> | Interpolator model error (spline overshoot, IDW flattening) | 0–20 cm at breaks | 0.5–5 m in channels | Compare methods; difference maps |
> | Void fill (gap of $k$ cells) | grows ≈ linearly with gap for rough terrain | depends on slope × distance | Block cross-validation vs. distance |
> | Statistic choice (min vs mean) | 5–15 cm on grass; larger under low noise | shoal bias vs. mean: metres on rough seabed | Compute both; report which |
> | Registration mismatch (half cell) | 0.5 m × slope: 15 cm at 30 % | 5 m × slope | Aspect-regression test |
> | Overview aggregation (average) | loses features < 2 cells per level | hides shoals | Compare overview extrema with base |

**Procedures.** (1) Withhold a random 5–10 % of points before gridding and report residual statistics by stratum (slope class, land cover, distance to nearest retained point); this is the leave-out test of the Try-it box and is cheap enough to be routine. (2) Run block cross-validation with blocks sized to the voids you expect to fill, and fit $\sigma(d, s)$ to produce an uncertainty raster. (3) Difference the grid against the same points gridded by a second method; where the two agree, the interpolator is not the problem, and where they disagree you have found the breaklines and voids. (4) Verify registration against a feature with a known location (a surveyed building corner in a DSM, a benchmark, a crossing of surveyed roads) or against a second product with the aspect-regression test; do this for every public DEM before using it. (5) Check overviews: compute the minimum and maximum of the base level and of each overview level over a region with a known shoal or peak; if the overview's extremum is not the base's, the aggregation is average and the overview must not be used for navigation or obstacle work. (6) Compute the cell-count and distance-to-observation rasters and look at them; empty-cell fractions above a few percent mean the cell size is too small for the data.

**What to report.** The interpolator and its parameters (power, radius, tension, variogram model and parameters, enforcement options); the binning statistic if any; the support (point or area) and the registration (pixel-is-area or -point, with the tag set correctly in the file); the cell size and the mean point spacing; the breaklines used (delivered as a layer); the void-fill method and the void mask; the overview resampling; and the uncertainty raster or, at minimum, the count and distance rasters. The BAG format carries depth and uncertainty together; for GeoTIFF products, deliver them as a multi-band COG or as sibling files with the same grid, and say in the metadata what the uncertainty layer is (kriging σ, cross-validation model, ensemble spread) and at what confidence level.

## Software

**Open source:** GDAL (`gdal_grid` nearest/invdist/average/linear and data metrics; `gdal_fillnodata.py`; `gdaladdo` and COG overview options; `gdal_proximity.py`; caveat: `gdal_grid` is slow on millions of points unless radius and max points are set). GMT (`surface`, `nearneighbor`, `triangulate`, `greenspline`, `blockmean`/`blockmedian`, `grdblend`, `grdedit -T`; caveat: gridline registration is the default, opposite to GeoTIFF practice). PDAL `writers.gdal` (min/max/mean/idw/count/stdev binning; caveat: binning with IDW fallback, not a TIN). GRASS GIS (`v.surf.rst` with cross-validation, `v.surf.idw`, `r.surf.nnbathy`, `r.fill.stats`). SAGA GIS (ordinary and universal kriging among many). PyKrige, scikit-gstat, gstools (variograms and kriging with variance). MB-System `mbgrid` (swath gridding with per-cell count and σ). xdem (co-registration and Nuth & Kääb shift estimation). WhiteboxTools (TIN, IDW, natural neighbour with breaklines).

**Free but closed:** LAStools `las2dem`/`blast2dem` (fast TIN rasterisation; licence limits). ANUDEM (licensed from ANU; algorithm published).

**Commercial:** ArcGIS Pro (Topo to Raster; Geostatistical Analyst kriging with cross-validation; caveat: default cell size and binning rules are easy to accept unexamined); Golden Software Surfer; CARIS HIPS & SIPS and QPS Qimera (CUBE/CHRT surfaces with uncertainty); Global Mapper; TerraSolid TerraModeler.

## Standards & guides

- **OGC GeoTIFF 1.1 (2019)** — `GTRasterTypeGeoKey` values `RasterPixelIsArea` and `RasterPixelIsPoint`; the normative definition of grid registration for GeoTIFF products.
- **OGC Cloud Optimized GeoTIFF (2023)** — internal overview requirements; resampling is a producer choice to be documented.
- **USGS Lidar Base Specification** (online edition, 2024 revision) — DEM cell size by quality level, hydro-flattening breakline deliverables, the requirement that DEMs be derived from the classified point cloud, and nodata/void handling.
- **IHO S-44 Edition 6.1.0 (2022)** and **IHO S-102 Bathymetric Surface Product Specification, Edition 3.0.0 (December 2024; in force from 2026-01-01)** — the depth-plus-uncertainty grid model, shoal-biased sounding selection, and gridding resolution guidance tied to feature detection.
- **Open Navigation Surface BAG Format Specification (current edition)** — elevation and uncertainty layers, with the uncertainty type declared in metadata.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)** — accuracy testing of the gridded DEM (interpolated at checkpoints), NVA/VVA, and the statement that accuracy is assessed on the product, not the points.
- **GMT documentation, "Grid registration"** — the clearest short treatment of gridline versus pixel registration and the half-cell relationship; not a standard but a de facto reference.
- **NOAA NCEI coastal DEM development guidance (Amante & Eakins 2009; subsequent technical memoranda)** — gridding, void filling, and uncertainty practice for integrated topobathymetric DEMs.

## Pitfalls

- **Cubic or spline overshoot in steep terrain.** Smooth interpolators ring around cliffs and terraces, producing values outside the data range. Detect by comparing with TIN-linear and by checking min/max against the input points; avoid by using tension, bounded interpolators at breaklines, or breakline constraints.
- **Min-binning used for a hydrologic DEM.** Every low outlier becomes a pit; flow routing fragments. Detect with sink counts versus a mean-binned surface; avoid by using mean or interpolated values for hydrology and reserving min for charts.
- **Mean-binning used for a chart.** Shoals are averaged away. Detect by comparing with the shallowest sounding per cell; avoid by shoal-biased selection or CUBE with appropriate disambiguation.
- **Unknown registration producing half-cell offsets.** Looks like slope-correlated vertical error. Detect with the aspect-regression test or a known feature; avoid by checking and setting `AREA_OR_POINT` and by verifying every public DEM before use.
- **Overviews computed with average hiding what a navigator or pilot needs.** Zoomed-out views show deeper water or lower obstacles. Detect by comparing extrema across levels; avoid by matching overview resampling to product semantics and recording it.
- **Oversampling.** A fine cell size from sparse data invents smoothness and false precision. Detect with the empty-cell fraction and the point spacing; avoid by setting cell size at or above the spacing and reporting effective resolution.
- **Spline bridging a lake or a building footprint.** Large voids are filled with a plausible-looking fiction. Detect with the distance-to-observation raster; avoid by setting a maximum search radius, filling voids deliberately, and delivering the mask.
- **Breaklines missing from the deliverable.** The DTM cannot be regenerated and hydro-flattening cannot be audited. Avoid by delivering breaklines as a layer with the DTM.
- **Comparing point-support and area-support grids.** Curvature appears as change. Detect by correlating the difference with curvature; avoid by resampling to common support before differencing.
- **Uncertainty omitted because "it's just interpolation."** The user cannot tell measured from invented cells. Avoid by delivering at least count and distance rasters, preferably a cross-validated uncertainty layer.

## Key takeaways

- The interpolator, the binning statistic, the support, and the registration are part of the product definition; record all four in the metadata and the file tags.
- At lidar density the choice among exact local interpolators barely matters over smooth ground; the statistic (min/mean/max) and the breaklines matter a great deal.
- At sparse density the interpolator is a model; choose kriging, tensioned splines, or ANUDEM deliberately and deliver an uncertainty layer.
- Shoal-biased minimum for charts, mean or interpolated for hydrology and science, maximum for obstacles—and never mix them silently through overviews.
- A half-cell registration mismatch masquerades as slope-correlated vertical error; test for it with the aspect regression before trusting any DEM comparison.
- Set cell size from point spacing; oversampling adds smoothness, not detail, and misleads every downstream user about resolution.
- Deliver count, distance-to-observation, and void masks with every grid; they cost nothing and distinguish measurement from invention.
- Validate gridding by withholding points, by block cross-validation sized to the voids, and by differencing against a second method; report residuals by stratum.

## References

- Amante, C. J., & Eakins, B. W. (2016). Accuracy of interpolated bathymetry in digital elevation models. *Journal of Coastal Research*, SI 76, 123–133.
- Amante, C., & Eakins, B. W. (2009). *ETOPO1 1 Arc-Minute Global Relief Model: Procedures, Data Sources and Analysis*. NOAA Technical Memorandum NESDIS NGDC-24.
- Calder, B. R., & Mayer, L. A. (2003). Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems*, 4(6), 1048.
- Chilès, J.-P., & Delfiner, P. (2012). *Geostatistics: Modeling Spatial Uncertainty*, 2nd ed. Wiley.
- Cressie, N. A. C. (1993). *Statistics for Spatial Data*, revised ed. Wiley.
- Delaunay, B. (1934). Sur la sphère vide. *Bulletin de l'Académie des Sciences de l'URSS, Classe des sciences mathématiques et naturelles*, 6, 793–800.
- Hengl, T. (2006). Finding the right pixel size. *Computers & Geosciences*, 32(9), 1283–1298.
- Hutchinson, M. F. (1989). A new procedure for gridding elevation and stream line data with automatic removal of spurious pits. *Journal of Hydrology*, 106(3–4), 211–232.
- Jakobsson, M., Calder, B., & Mayer, L. (2002). On the effect of random errors in gridded bathymetric compilations. *Journal of Geophysical Research: Solid Earth*, 107(B12), 2358.
- Kazhdan, M., Bolitho, M., & Hoppe, H. (2006). Poisson surface reconstruction. *Proceedings of the Fourth Eurographics Symposium on Geometry Processing*, 61–70.
- Mitas, L., & Mitasova, H. (1999). Spatial interpolation. In P. A. Longley, M. F. Goodchild, D. J. Maguire, & D. W. Rhind (Eds.), *Geographical Information Systems: Principles, Techniques, Management and Applications*, 2nd ed., Vol. 1, 481–492. Wiley.
- Mitášová, H., & Mitáš, L. (1993). Interpolation by regularized spline with tension: I. Theory and implementation. *Mathematical Geology*, 25(6), 641–655.
- Nuth, C., & Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5(1), 271–290.
- Peucker, T. K., Fowler, R. J., Little, J. J., & Mark, D. M. (1978). The triangulated irregular network. *Proceedings of the Digital Terrain Models (DTM) Symposium*, American Society of Photogrammetry, St. Louis, 516–540.
- Shepard, D. (1968). A two-dimensional interpolation function for irregularly-spaced data. *Proceedings of the 1968 23rd ACM National Conference*, 517–524.
- Sibson, R. (1981). A brief description of natural neighbour interpolation. In V. Barnett (Ed.), *Interpreting Multivariate Data*, 21–36. Wiley.
- Smith, W. H. F., & Wessel, P. (1990). Gridding with continuous curvature splines in tension. *Geophysics*, 55(3), 293–305.
- OGC (2019). *OGC GeoTIFF Standard*, Version 1.1. Open Geospatial Consortium, OGC 19-008r4.
- U.S. Geological Survey (2024). *Lidar Base Specification*, online edition. USGS National Geospatial Program.

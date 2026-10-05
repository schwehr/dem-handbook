# Chapter 46 — Data models: points, waveforms, grids, TINs, meshes, voxels, variable resolution, overviews, splats

> **Part X — Representing, storing, finding, and keeping elevation data.** The chapter about the abstract containers elevation lives in—before any file format—and about what each container can hold, what it silently discards, and what the conversions between them cost.

**In this chapter.** A DEM is not the terrain; it is one of several *models* of a set of measurements, and every model commits to what can be represented. You will be able to describe the expressive power of each major data model—unorganized and organized point clouds, full waveforms and photon clouds, 2.5D rasters with their cell semantics and overviews, triangulated irregular networks with breaklines, true-3D meshes with level of detail, voxel and signed-distance volumes, Gaussian splats, and variable-resolution hydrographic surfaces—and state what each cannot express (overhangs in a raster, density in a TIN, uncertainty in a mesh). You will read the conversion matrix between them and name the information lost at each arrow, explain why a raster overview built with the wrong kernel removes ridges and shoals, construct Morton and Hilbert indices and relate octree level to resolution, compute a Hausdorff distance for a simplified mesh, and follow how CUBE and CHRT turn per-sounding uncertainty into per-node hypotheses. The lesson is simple to state and hard to live by: keep the richest representation you have, and treat every conversion as a documented decision.

## 46.1 Point clouds

The **point cloud** is the closest thing elevation work has to raw measurement, and for lidar, multibeam, and dense image matching it is the first product a non-specialist can open. Each point is a tuple of three coordinates and some attributes; the attributes are where the information later products will need—and usually lose—lives.

### 46.1.1 Attributes

A lidar return typically carries **intensity** (an uncalibrated backscatter amplitude), **return number** and **number of returns**, a **classification** code (ASPRS classes: 2 ground, 6 building, 9 water; see [Chapter 30](ch30-point-cloud-classification.md)), **GPS time** (which joins the point to the trajectory and is essential for strip adjustment and for diagnosing time-dependent errors; [Chapter 6](ch06-time-as-coordinate.md)), **scan angle** (which governs the geometric error budget and lets you filter swath edges), **point source ID** (flight line), **RGB/NIR** colour, and sometimes a **scanner channel**. Multibeam soundings carry analogues: beam number, ping time, backscatter, detection method (amplitude or phase), and a rejection flag.

Two attributes deserve to be first-class and rarely are. **Per-point uncertainty**: for multibeam, total propagated uncertainty (**TPU**; [Chapter 20](ch20-sonar.md)) gives each sounding a vertical and horizontal 1σ from the sensor, motion, sound-speed, and tide budgets; for lidar the equivalent is computable from range, scan angle, trajectory covariance, and boresight uncertainty but is rarely written to the file. **Time**: a cloud without timestamps cannot be split by strip, checked against a trajectory, or reasoned about as an epoch-stamped observation ([Chapter 37](ch37-time-scales-of-change.md)); it has been reduced to geometry.

### 46.1.2 Unorganized versus organized clouds

An **unorganized** cloud is a bag of points with no implied neighbourhood; finding neighbours requires an index (§46.8). An **organized** cloud retains acquisition structure—a terrestrial scanner's azimuth-by-elevation array, an airborne scanner's scanlines, a multibeam's pings of beams. Organization is information: you know which points were adjacent in time, which lets you detect dropouts, estimate local footprint spacing, and compute normals and occlusion without a search structure. Most delivery formats discard it; formats that preserve structure (E57 structured scans, organized PCD, vendor raw sonar) are worth keeping for exactly this reason ([Chapter 47](ch47-file-formats.md)).

### 46.1.3 Density as a property of the data

Point density is not one number. It varies with range, scan angle, platform speed, overlap, reflectivity, and incidence angle; it is zero in shadows and voids ([Chapter 35](ch35-voids-and-overhangs.md)); it doubles in sidelap; and in forest the *ground* density is a small fraction of the total. The USGS Lidar Base Specification distinguishes aggregate nominal pulse density from per-swath density and requires density to be assessed on a grid, not quoted as a mean, because the mean hides the holes. The effective resolution of any grid made from the cloud ([Chapter 44](ch44-resolution-and-sampling.md)) is bounded by the local density, and a density raster—ground returns per cell—is the first companion layer a point-derived DEM should carry. Only the point cloud can produce it.

> **Definitions that bite.** *Point density* vs *pulse density* vs *ground-point density*. A multi-return lidar over forest at 8 pulses/m² might yield 20 points/m² total and 1 ground point/m². A specification written as "8 points per square metre" is ambiguous by a factor of 20. Read the definition in your contract before measuring compliance.

<!-- figure: Figure 46.1 — A forested slope as (a) all-return point cloud coloured by return number, (b) ground-classified points only, (c) ground-point density raster at 2 m cells with zeros under dense canopy, showing that nominal and DEM-supporting density differ by an order of magnitude. -->

## 46.2 Full waveforms and photon-counting data

Below the point is the signal it was extracted from. For a linear-mode lidar it is the **full waveform**: received power digitized at about 1 ns (15 cm range) intervals. For a photon-counting lidar there is no waveform—only time-tagged detection events, most of them noise. For multibeam it is the per-beam **water-column** time series and the **snippet** of samples around the bottom detection.

### 46.2.1 Why waveforms matter

A discrete-return lidar applies a hardware detector and reports where it fired; the waveform lets you choose the detector afterwards, with knowledge of the target. In vegetation, weak late ground returns below the hardware threshold can be recovered by fitting. In bathymetric lidar the waveform *is* the measurement: surface, water-column, and bottom returns overlap, and depth is the separation of two fitted peaks after modelling the column's exponential decay ([Chapter 19](ch19-bathymetric-lidar.md)). And the waveform carries the echo width and the fitted peak's standard error—a per-return range uncertainty that no discrete product can recover. Mallet and Bretar (2009) review the field; their message is that waveforms encode within-footprint target geometry (slope, roughness, vertical extent) that points cannot.

### 46.2.2 Gaussian decomposition

The standard model represents the received waveform as a sum of $K$ Gaussian echoes on a background $b$:

$$w(t) = b + \sum_{k=1}^{K} A_k \exp\!\left(-\frac{(t-\mu_k)^2}{2\sigma_k^2}\right) + \varepsilon(t),$$

with amplitude $A_k$, echo time $\mu_k$ (range $c\,\mu_k/2$), and width $\sigma_k$. Initial guesses come from the smoothed second derivative; nonlinear least squares refines them, and $K$ is chosen by an information criterion or an amplitude threshold. The width is diagnostic: $\sigma_k$ larger than the emitted pulse width indicates slope or vertical extent within the footprint—a 4 ns pulse broadened to 6 ns implies roughly 0.7 m of vertical spread. The standard error of $\mu_k$ from the fit covariance is the per-echo ranging precision and scales inversely with signal-to-noise ratio.

### 46.2.3 Photon-counting statistics: ATL03 to ATL08

Photon-counting systems trade signal strength for sensitivity, so the raw product is dominated by solar background and dark counts. ICESat-2's geolocated photon product **ATL03** contains every detection with a coarse confidence flag; the land and vegetation product **ATL08** (Neuenschwander and Pitts 2019) applies a density-based noise filter (DRAGANN), then iterative surface finding, to classify photons as ground, canopy, or top-of-canopy and to aggregate statistics in 100 m segments. Noise is a Poisson process whose rate depends on solar elevation and reflectance; signal photons per shot are few; per-photon vertical precision is of order 0.1–0.2 m 1σ; and the *segment* terrain height uncertainty depends on how many ground photons survived the filter and on terrain variation within 100 m. A photon cloud is a data model whose unit is not a surface point but a detection event with a probability of being signal, and products derived from it should carry both photon count and classification confidence.

### 46.2.4 Sonar water column and snippets

Multibeam bottom detection is likewise an algorithm applied to a time series. The water-column record enables re-detection (a wreck's mast, a kelp canopy) and least-depth verification; it is large and often discarded, which is why NOAA's hydrographic specifications now require its retention in defined circumstances. Snippets and per-beam backscatter are the acoustic analogue of intensity, and equally uncalibrated unless a calibration campaign says otherwise.

## 46.3 Grids and rasters

The regular grid dominates because it is simple, compact, and usable by every raster tool. Its simplicity is bought with commitments, each a source of error if forgotten.

### 46.3.1 2.5D and single-valuedness

A raster assigns one elevation per cell: a function $z = f(x,y)$, a **2.5D** surface. It cannot represent a vertical face, an overhang, a bridge deck with water beneath, a cave, or a building interior. Every raster made from measurements that include such features embeds a **collapse rule**—highest, lowest, last return, mean, or class-dependent—and the rule is almost never stated in metadata. [Chapter 35](ch35-voids-and-overhangs.md) treats multi-valued surfaces; the point here is that the model forces the choice and the grid cannot record it.

### 46.3.2 Cell semantics: area versus point

A grid value can mean the elevation *at* a node (**PixelIsPoint**) or a representative elevation *of* the cell's area (**PixelIsArea**). The difference is half a cell: 0.5 m at 1 m resolution, which on a 30° slope is 0.29 m of elevation; 15 m for SRTM's 30 m PixelIsPoint cells, or 8.7 m on the same slope. GeoTIFF encodes the convention; GDAL honours it; many tools and hand-written readers ignore it ([Chapter 31](ch31-interpolation-and-gridding.md), [Chapter 47](ch47-file-formats.md)). What the area value *means* is a second question: mean, minimum (shoal-biased), or centre sample differ systematically on rough terrain—with a within-cell σ of 0.5 m and 20 points per cell, the expected gap between minimum and mean is roughly $1.9\sigma \approx 0.9$ m—and a grid that does not state its aggregation has an unknown bias of that order against any checkpoint.

### 46.3.3 Nodata

Conventions proliferate: −9999, −32767, −32768, float max, NaN, 0 (catastrophic, since 0 is a valid elevation), and format defaults (DTED −32767; BAG 1 000 000). The raster model does not distinguish "not measured" from "rejected," "outside footprint," or "water, deliberately flattened"; a single value collapses them, and preserving the distinction needs a mask band. The subtle failure is nodata that survives resampling as a legitimate value interpolated between −9999 and 300 m.

### 46.3.4 Multi-band grids

A multi-band raster is a surface with attributes: **uncertainty** (with its definition), **source identifier**, **acquisition date**, **method** (GEBCO's TID, a sensor class), and **count** or density. [Chapter 48](ch48-compositing.md) makes these mandatory for composites; the model supports them natively and most products do not use the capacity. BAG was designed around elevation and uncertainty as paired layers and remains the clearest example of a format treating uncertainty as a co-equal measurement.

### 46.3.5 Tiling and chunking

Large grids are stored as internal blocks or independently fetchable chunks. Storage leaks into the model: operations whose support crosses a tile edge (slope, flow routing, focal statistics) must read neighbours, or artefacts appear one kernel radius wide; delivered tiles may overlap by one row and column (SRTM) or not at all and may disagree along shared edges; and a chunk shape chosen for map display is pathological for time-series access.

### 46.3.6 Pyramids and overviews — and why an overview can lie

An **overview** is a reduced-resolution copy stored alongside the grid so a viewer can draw a continent without reading every cell. Each overview cell summarizes an $n\times n$ block with a kernel, and the kernel determines what the overview *means*:

| Kernel | Overview value | Preserves | Destroys |
|---|---|---|---|
| Nearest | One arbitrary cell of the block | Original values exist in data | Features narrower than the block; ridges dash or vanish |
| Average / bilinear / cubic | Block mean (weighted) | Volume; smooth terrain | Peaks lowered, pits raised; shoals disappear |
| Min | Block minimum | Channels; shoalest value when z is depth-positive | Ridges; shoals when z is elevation-negative |
| Max | Block maximum | Ridges, peaks; shoalest elevation | Channels |
| Mode | Most frequent value | Categorical bands (source, class) | Meaningless for continuous elevation |

A nearest overview of a lidar DTM at 16× shows a levee as a dashed line because the crest is sampled only when the chosen cell lands on it. An average overview of a nautical surface raises every narrow shoal toward the surrounding depth—the opposite of the safety bias the product exists to provide—so hydrographic viewers must build shoal-biased overviews, and GDAL's `-r min`/`-r max` must be chosen with the sign convention in mind. A categorical band must use `mode` or `nearest`, because the average of source IDs 3 and 7 is not source 5. The honest formulation: an overview is a *new product with its own aggregation rule*, and a viewer that lets a user read a value from it is displaying a model the user did not ask for. GDAL records the kernel in overview metadata; most viewers do not show it.

> **Try it.** Build overviews two ways and compare the ridge.
> ```bash
> gdaladdo -r average -ro dtm.tif 2 4 8 16
> gdal_translate -outsize 6.25% 6.25% -r nearest dtm.tif ovr16_avg.tif
> cp dtm.tif dtm_max.tif && gdaladdo -r max dtm_max.tif 2 4 8 16
> gdal_translate -outsize 6.25% 6.25% -r nearest dtm_max.tif ovr16_max.tif
> gdal_calc.py -A ovr16_avg.tif -B ovr16_max.tif --calc="B-A" --outfile=ovr_diff.tif
> gdalinfo -stats ovr_diff.tif | grep -E "MINIMUM|MAXIMUM|MEAN"
> ```
> Expected outcome: near zero over flat ground; along narrow ridges and levees the max-minus-average difference approaches the feature's full height. Whichever you ship, write the kernel into the product metadata.

<!-- figure: Figure 46.2 — A 1 m DTM of a levee and ditch at native resolution and at 16× overview under nearest, average, min, and max resampling: the levee dashed, lowered by ~60 %, gone, and preserved respectively. -->

## 46.4 TINs and breaklines

A **triangulated irregular network** (TIN) represents a surface as non-overlapping triangles whose vertices are measured points. Introduced to terrain modelling by Peucker, Fowler, Little, and Mark (1978), it was the first data model to make adaptive density explicit: triangle size is a visible statement of local information content.

### 46.4.1 Delaunay and constrained Delaunay

The **Delaunay** triangulation is the one in which no point lies inside any triangle's circumcircle; it maximizes the minimum angle (avoiding slivers), is unique in general position, is the dual of the Voronoi diagram, and is built in $O(n\log n)$. Its drawback for terrain is that it is defined on horizontal coordinates alone: it will connect two points on opposite banks of a stream with an edge that dams the channel. The **constrained Delaunay triangulation** (CDT) forces specified segments—**breaklines**—to be edges. A **hard breakline** marks a slope discontinuity (road edge, top of cut, stream centreline); a **soft breakline** forces an edge without a gradient break (a shoreline at a given elevation); **mass points** are unconstrained vertices. CDT edges lose the circumcircle guarantee locally but the surface respects the hydrography ([Chapter 59](ch59-vector-data.md)).

### 46.4.2 What a TIN expresses

A TIN is piecewise planar, so slope is constant within a triangle and curvature undefined except across edges. It is still 2.5D—triangles cannot fold over. It represents breaklines exactly, which a grid never can, and vertical faces as triangles of near-zero horizontal extent. Its triangle-area distribution *is* the density, and it preserves exactly which measurements made the surface. What it loses relative to the cloud is everything but the ground-classified vertices: canopy, intensity, and time are gone unless carried as vertex attributes, which few tools support.

### 46.4.3 Flat triangles and contour-derived TINs

Where three vertices on the same contour are mutually nearest—ridge noses, valley heads, hilltops—Delaunay connects them into a horizontal **flat triangle** at the contour elevation. Ridges become terraces, summits are truncated to the highest contour, valley heads become benches. Symptoms: histogram spikes at the contour interval, zero-slope polygons along ridgelines, drainage that ponds on benches. Remedies: ridge and drainage breaklines, spot heights, or contour-aware interpolators (ANUDEM; [Chapter 31](ch31-interpolation-and-gridding.md)). Legacy national DEMs digitized from contours carry this as the "contour ghost" stair-step ([Chapter 47](ch47-file-formats.md)).

### 46.4.4 TIN ↔ grid losses

TIN → grid samples the planar surface at cell centres and loses exact breakline positions, vertex positions, and adaptive density—every cell costs the same whether the triangle was 1 m or 100 m across. Grid → TIN selects vertices by a tolerance $\tau$ (very-important-points, greedy insertion) until the TIN is within $\tau$ of the grid everywhere—a bound the grid never had against the measurements. Repeated round-trips are a low-pass filter whose cutoff nobody chose.

## 46.5 Meshes

A **mesh** is a set of 3D vertices connected into faces with no requirement that the surface be a function of $(x,y)$. It is the native model of photogrammetric reconstruction, terrestrial scanning, and the 3D city, and it can represent overhangs, bridges with water visible beneath, façades, cave interiors, and the undersides of piers, with a **texture** mapped onto the faces.

### 46.5.1 What a mesh expresses and what it does not

A mesh expresses geometry and topology (whether the surface is closed, manifold, oriented). It does not natively express density, uncertainty, time, or source: a vertex is a vertex whether measured by a return or hallucinated by hole filling. Photogrammetric meshes are especially opaque, because meshing (Poisson reconstruction, Delaunay carving) interpolates freely across unobserved regions and texture paints the interpolation with pixels that look like measurement. If per-vertex confidence exists (number of observing cameras), keep it as a vertex attribute; glTF and PLY allow it and almost nobody does.

### 46.5.2 Level of detail

Streaming meshes are organized as **level-of-detail** (LoD) hierarchies with a **geometric error** per tile—the maximum deviation of the tile from the full-resolution surface—so a renderer can pick the coarsest level whose screen-space error is acceptable. Cesium's **quantized-mesh** stores terrain TINs with 16-bit quantized vertices (vertical precision = tile height range / 32 767) in a quadtree; OGC **3D Tiles 1.1** generalizes to arbitrary tilesets with explicit or implicit quadtree/octree subdivision and glTF content; Esri's **I3S** is a comparable OGC community standard. These are *rendering* models: geometric error is a visual bound, not a measurement uncertainty, and an elevation read from a coarse tile deviates from the source by up to that tile's declared error—often metres ([Chapter 57](ch57-visualizing-dems.md)).

### 46.5.3 Simplification and the Hausdorff metric

The quadric error metric (Garland and Heckbert 1997) collapses edges in the order that minimizes squared distance to the original face planes; it is fast but its error is a quadratic form, not a geometric distance. The standard geometric measure is the **Hausdorff distance**

$$d_H(A,B) = \max\!\left\{\sup_{a\in A}\inf_{b\in B}\|a-b\|,\ \sup_{b\in B}\inf_{a\in A}\|a-b\|\right\},$$

the largest distance from any point on either surface to the nearest point on the other. Symmetry matters: the one-sided distance from $B$ to $A$ can be small while $A$ has a spire that $B$ removed. It is estimated by sampling (Metro, MeshLab, CGAL) and should be reported with mean and RMS. For terrain the worst case is exactly the summit, the shoal, and the wire.

### 46.5.4 Solids and semantics

A **solid** is a closed shell with an inside; CityGML 3.0/CityJSON attach semantics (wall, roof, ground) and LoDs 0–3 that are modelling levels, not error bounds, and IFC describes BIM elements in local, often ungeoreferenced coordinates ([Chapter 63](ch63-buildings-cities-innerspace.md)). A solid rasterizes to a DSM by its highest face, to a DTM by its ground surface, or not at all—another decision the raster cannot record.

## 46.6 Voxels, implicit surfaces, and splats

**Voxels** divide space into cubes storing **occupancy** (free, occupied, unknown) or a signed distance. OctoMap (Hornung et al. 2013) keeps log-odds occupancy in an octree so that large free and unknown regions cost one node each; it is the robotics standard for innerspace, mines, and forests where overhangs are the rule ([Chapter 15](ch15-slam.md)). The **truncated signed distance function** (TSDF) stores signed distance to the nearest surface within a band and extracts surfaces by marching cubes. Voxel models express the third dimension fully, carry an explicit "unknown" state that no raster nodata distinguishes from "measured empty," and support probabilistic fusion. They do not scale: a 10 km × 10 km × 100 m volume at 0.1 m is 10¹² voxels.

**Implicit surfaces** are zero level sets of a function $f(x,y,z)$—an SDF, or a neural network fitted to one—and **neural radiance fields** (NeRF) store volumetric density and colour as network weights fitted to images. They smooth over gaps elegantly, which is the problem: the surface is a learned prior conditioned on observations, and its uncertainty is not something the model exposes. They belong to visualization and to the enhancement methods of [Chapter 45](ch45-super-resolution.md), not the measurement chain.

**3D Gaussian splatting** (Kerbl et al. 2023) represents a scene as anisotropic 3D Gaussians—position, covariance, opacity, spherical-harmonic colour—optimized so that rasterizing them reproduces the input photographs. Rendering is fast and photographic. But a splat is not a surface: Gaussians overlap, float, and interpenetrate; their centres are not on any surface; their covariances are fitted to appearance; and there is no principled way to ask "what is the elevation at $(x,y)$?" Surface-extraction attempts produce geometry whose relationship to the measurements is mediated by a photometric loss and a regularizer, not by a ranging equation. Splats are a textured mesh's successor for *display*; the "splats → nothing measurable (yet)" entry in §46.10 is a statement of design intent, not a dismissal ([Chapter 57](ch57-visualizing-dems.md)).

## 46.7 Variable-resolution surfaces

A single-resolution grid fits bathymetry poorly because sounding density falls with depth: a multibeam swath delivering 50 soundings/m² in 10 m of water delivers fewer than 1/m² at 500 m. A grid fine enough for the shallows is empty in the deep; one coarse enough for the deep discards the shallows.

### 46.7.1 CUBE and CHRT

**CUBE** (Calder and Mayer 2003) estimates depth at grid nodes from nearby soundings weighted by their propagated uncertainty, keeping multiple **hypotheses** per node when soundings disagree beyond what their uncertainties allow (§46.9 and Mathematics). It is fixed-resolution. **CHRT** (Calder and Rice 2017) makes resolution data-adaptive: a first pass estimates, from density and uncertainty in each coarse super-cell, the finest resolution the data can support—**resolution-by-uncertainty**—and a second pass runs the estimator at that local resolution. The output is a tiling by patches of different resolution, each with depth, uncertainty, hypothesis count, and hypothesis strength.

### 46.7.2 BAG VR and S-102 tiling

BAG's **variable-resolution extension** stores a coarse base grid in which each cell holds either a value or a pointer to a **refinement grid** of its own resolution, with elevation and uncertainty at every refinement node. IHO S-102 instead fixes one resolution per dataset and achieves multi-resolution by **tiling**—separate datasets of different resolutions—which is simpler for navigation displays and loses per-cell adaptivity. VR surfaces are faithful and efficient, but most raster tools cannot read them (GDAL exposes VR BAG via resampling or per-refinement sub-datasets), QC must handle resolution seams, and flattening to a fixed grid either invents detail in coarse zones or destroys it in fine ones. Ship the VR surface and a fixed-resolution derivative with a resolution-source band.

### 46.7.3 Quadtree and octree tilings ⟨H⟩

The structure beneath VR surfaces, LoD meshes, and map tiles is the **quadtree** (Finkel and Bentley 1974; Samet 1984): recursively subdivide a square into four until a criterion—homogeneity, point count, uncertainty—is met; the **octree** is its 3D analogue. A cell at level $\ell$ of a root of side $S$ has side $S/2^\ell$, so an octree on a 10 km cube reaches 0.6 m at level 14. Web tiles are a quadtree on a fixed Web Mercator root; quantized-mesh and implicit 3D Tiles use quadtrees and octrees explicitly; COPC is an octree over the cloud's bounding cube. The cost of adaptivity is that neighbours at different levels have mismatched edges—T-junctions in meshes, resolution seams in VR grids—which every consumer must handle.

<!-- figure: Figure 46.3 — A CHRT/VR BAG surface across a shelf-to-slope transect: 1 m refinements in 10–30 m water, 4 m at 100 m, 16 m at 500 m, with super-cell boundaries drawn and an inset of hypothesis count at a wreck where two hypotheses coexist. -->

## 46.8 Hierarchical and spatial indexing

A data model determines what can be stored; an index determines what can be found. A **k-d tree** splits points by alternating coordinate medians and is the default for nearest-neighbour search in clouds (PDAL, Open3D, scipy), but it is static. An **R-tree** nests bounding rectangles and indexes extents, not just points (GeoPackage, PostGIS). **Quadtrees** and **octrees** subdivide space rather than data and are stable under insertion and natural for LoD.

**Space-filling curves** ⟨H⟩ linearize space so that a one-dimensional sort gives spatial locality. The **Morton** (Z-order) code interleaves the bits of integer cell coordinates; its prefixes are quadtree node addresses, which is why it underlies S2 cells, database spatial keys, and EPT/COPC addressing. The **Hilbert curve** (Hilbert 1891) preserves locality better—consecutive codes are always adjacent cells, whereas Morton order jumps at quadrant boundaries—at the cost of a state-machine computation; PMTiles and GeoParquet writers use it for ordering. [Chapter 60](ch60-dggs-and-location-codes.md) covers discrete global grids.

**COPC and EPT** apply the octree to point clouds for cloud access. Entwine Point Tiles writes each node as a separate LAZ file with a JSON hierarchy; **Cloud Optimized Point Cloud** (COPC, 2021) folds the same octree into a single LAZ 1.4 file, each node an independently decodable chunk and the node→byte-range hierarchy in a VLR, so an HTTP client fetches only the nodes intersecting its view at the LoD it needs. Both store a subsample at each coarse node, so—like raster overviews—the coarse levels are a *selection* whose statistics differ from the full cloud; a density computed from a shallow traversal is wrong by the subsampling factor.

## 46.9 Attribute models for uncertainty

Where does uncertainty live in the model, and what does the number mean?

**Per-point.** A sounding with a TPU, a lidar return with a propagated covariance, a photon with a confidence class: uncertainty attaches to the observation and travels through filtering, which is ideal. LAS 1.4 extra bytes permit per-point uncertainty; the ASPRS topo-bathy domain profile defines fields; few producers populate them. Vendor sonar formats carry what TPU needs but not TPU itself; processing software computes and stores it in its own project model.

**Per-cell.** BAG stores an **uncertainty** layer co-registered with elevation and an **uncertainty type** declaring its meaning. The ONS specification enumerates several (names vary by edition; check the edition you are reading): unknown; raw standard deviation of contributing soundings; CUBE standard deviation of the chosen hypothesis; product uncertainty (a propagated 95 % total vertical uncertainty for chart compilation); historical standard deviation. These are not interchangeable (a raw σ of 0.1 m from 200 soundings implies a standard error of 0.007 m; a product uncertainty of 0.1 m is a 95 % bound including systematic terms), and exporting the layer to a GeoTIFF band named "uncertainty" discards the type ([Chapter 47](ch47-file-formats.md)). BAG also carries a **tracking list** of manually edited nodes with original and new values—a provenance structure no other common elevation format has.

**Per-tile or per-source.** Many composites carry uncertainty only as one number per source rasterized into source zones. It is a prior, not a measurement, and says nothing about local degradation at swath edges, under canopy, or on slopes. S-102's QualityOfBathymetryCoverage attribute table is a per-region model of this kind, with survey dates, horizontal and vertical uncertainty, and feature-detection parameters.

**Covariance versus scalar.** Horizontal and vertical uncertainty are coupled on slopes: horizontal error $\sigma_h$ on gradient $s$ induces vertical error $s\,\sigma_h$ ([Chapter 5](ch05-error-and-uncertainty.md)). A scalar vertical uncertainty computed on the flat understates the error on a 20° slope by $0.36\,\sigma_h$—0.18 m for $\sigma_h = 0.5$ m. The compromise is to store THU and TVU separately and let the consumer combine them with local slope, which is what S-44 and BAG are designed to permit.

**Propagation into grids: CUBE hypotheses.** Each sounding is propagated to nearby nodes with its uncertainty inflated by distance, and each node runs a sequential Kalman-style update: a sounding consistent with the current hypothesis refines it; one that is not opens a new hypothesis. A **disambiguation** rule then picks one hypothesis per node, and the node reports depth, that hypothesis's σ, the hypothesis count, and a **hypothesis strength**. The node's σ is therefore the σ *of the chosen hypothesis*, not of the seafloor: a node with three hypotheses and weak strength can have a small σ and a large chance of being wrong. Hypothesis count and strength are part of the uncertainty, not optional extras.

> **Uncertainty budget.** What an "uncertainty" band might mean for the same cell.
>
> | Reported quantity | Meaning | Example value |
> |---|---|---|
> | Raw σ of soundings | Spread of contributing measurements (includes roughness) | 0.30 m |
> | Standard error of mean (n = 100) | Raw σ / √n | 0.03 m |
> | CUBE hypothesis σ | Posterior σ of chosen hypothesis | 0.05 m |
> | Propagated TVU, 1σ | Sensor + motion + SSP + tide budget | 0.15 m |
> | Product uncertainty, 95 % | ≈ 1.96 × TVU plus allowances | 0.30 m |
> | Source-declared accuracy | S-44 Order 1a at 20 m depth, 95 % | 0.52 m |
>
> One cell legitimately carries values from 0.03 m to 0.52 m depending on which quantity is meant. A band named "uncertainty" without a type is a number with no units of meaning.

## 46.10 The conversion matrix

Every arrow between data models is lossy in some direction, and the loss is rarely reversible.

| From → To | Decision the converter makes | Information lost | Typical artefact |
|---|---|---|---|
| Points → grid (binning) | Aggregation (mean/min/max), cell size, nodata threshold | Sub-cell geometry, point attributes, density unless banded | Aliased narrow features; empty cells where density < 1/cell |
| Points → grid (interpolation) | Interpolator, search radius, breaklines | Same, plus measured-vs-invented distinction | Smoothed peaks; invented terrain in voids |
| Points → TIN | Which classes, breaklines, thinning tolerance | Non-vertex points, non-ground classes, attributes | Flat triangles; stream-damming edges |
| Waveform → points | Detector/decomposition, thresholds | Echo widths, weak returns, fit uncertainty | Missing ground under canopy; biased bathy bottom |
| Grid → contours | Interval, smoothing | Everything between contours | Stair-stepped contours |
| Contours → TIN/grid | Interpolator, breaklines, spot heights | Shape between contours | Flat triangles; contour-ghost terraces |
| TIN → grid | Cell size, sampling point, convention | Exact breaklines, vertex positions, adaptive density | Breakline smearing |
| Grid → TIN | Tolerance τ, heuristic | Cells within τ of a plane | Faceted slopes |
| Mesh → DSM | Collapse rule (highest/lowest/first hit) | Overhangs, undersides, texture | Bridges become dams; balconies become walls |
| Mesh → DTM | Classification of faces as ground | Everything else | Buildings become craters if footprints mis-classified |
| Fine grid → overview | Resampling kernel | Extremes or means | Ridges/shoals vanish (average) or dash (nearest) |
| VR surface → fixed grid | Target resolution, up/down policy | Resolution-by-uncertainty | Invented detail in coarse zones or lost detail in fine |
| Splats → anything measurable | Surface-extraction heuristic | Any direct link to a ranging measurement | Geometry fitted to appearance; no error model |

> **Rule of thumb.** Convert *down* the richness ladder (waveform → points → TIN/grid → overview/contour) only for a stated purpose, and archive the level above. Never convert *up* (contours → grid, overview → analysis grid, splat → surface) and present the result as measurement. Where the richer level was never recorded—legacy contour maps *are* the data—the lineage must say so.

## Then & now

The history of elevation data models is a history of storing more of the measurement and deferring more of the decisions. **Contours and spot heights** ⟨H⟩ were the topographic map's model for two centuries—compact, legible, and silent about everything between the lines; digitized contours fed the first national DEMs. **Regular grids** came with computers: DTED (US Defense Mapping Agency, 1970s) and the USGS DEM series gridded contours and photogrammetric profiles because array arithmetic was what machines did. **TINs** (Peucker et al. 1978) made adaptive density and breaklines first-class and remain native to design software. **Dense point clouds** became lidar's primary deliverable in the 2000s, with LAS (2003) ⟨H⟩ as the shared container; multibeam had produced dense soundings since the 1980s but gridded them early. **Waveforms and photons** moved the archive toward the signal (full-waveform airborne systems mid-2000s; LAS 1.3/1.4 waveform packets; ICESat-2 from 2018). **Meshes and 3D tiles** (quantized-mesh; 3D Tiles 1.0 as an OGC community standard in 2019, 1.1 in 2023; I3S) made true 3D a web commodity. **Variable resolution**: CUBE (2003) made uncertainty-weighted gridding standard in hydrography; CHRT (2017) and BAG VR made resolution data-driven. **Cloud-native indexing**: EPT (2018) and COPC (2021) put octrees inside the files. **Neural and splat representations** (NeRF 2020; 3D Gaussian splatting 2023) opened a branch whose relation to measurement is still being worked out. Each generation's products were made from a richer representation that was often not kept; the change that most improves future correctness is that points, and increasingly waveforms, are now routinely archived ([Chapter 50](ch50-archiving-and-provenance.md)).

## Mathematics

**Delaunay properties.** Stated in §46.4.1: empty circumcircles, maximal minimum angle, Voronoi duality, $O(n\log n)$ construction; the constrained version relaxes the empty-circle test to points visible from the triangle. **Gaussian decomposition.** The fit covariance $\hat\sigma^2 (J^\top J)^{-1}$ gives the range uncertainty of echo $k$ as $\tfrac{c}{2}\sqrt{[\mathrm{Cov}]_{\mu_k\mu_k}}$, improving with amplitude and degrading with width.

**Morton and Hilbert indices.** For cell coordinates $i=\sum_b i_b 2^b$, $j=\sum_b j_b 2^b$ at depth $L$, the Morton code is $M(i,j)=\sum_{b=0}^{L-1}(i_b 2^{2b} + j_b 2^{2b+1})$; its top $2\ell$ bits are the code of the level-$\ell$ ancestor, so a quadtree node is a contiguous Morton range. The Hilbert index is computed coarsest-to-finest with a four-state machine tracking curve orientation; consecutive indices share an edge. Both cost $O(L)$ per point.

**Octree level and resolution.** A root cube of side $S$ has cells of side $S/2^\ell$ at level $\ell$. COPC's root spacing is $S/n_0$ for a target of about $n_0$ points per axis and halves per level, so spacing $d$ is reached at $\ell = \lceil \log_2 (S/(n_0 d)) \rceil$: a 20 km cube with root spacing ≈ 156 m reaches 0.6 m at $\ell = 8$.

**CUBE hypothesis statistics** (Calder and Mayer 2003). A sounding $z_i$ with vertical variance $\sigma_{v,i}^2$ and horizontal variance $\sigma_{h,i}^2$ at distance $r$ from a node is propagated with a variance inflated by a distance term of the form $\left((r+\sigma_{h,i})/d\right)^{\alpha}$ (node spacing $d$, tunable exponent $\alpha$). Each hypothesis $j$ holds $(\hat z_j, P_j)$ updated as a scalar Kalman filter: $K = P_j/(P_j+\sigma_{p,i}^2)$, $\hat z_j \leftarrow \hat z_j + K(z_i-\hat z_j)$, $P_j \leftarrow (1-K)P_j$. Assignment uses the normalized innovation $(z_i-\hat z_j)/\sqrt{P_j+\sigma_{p,i}^2}$ with a sequential Bayes-factor test; a rejected sounding starts a new hypothesis. Disambiguation selects by sounding count, posterior variance, proximity to a guide surface, or a combined score; strength compares the chosen hypothesis's support to its nearest competitor's.

## Validation & uncertainty

The data model is itself an error source: every structure imposes a **representation error**—the gap between what was measured and what the structure can hold—on top of measurement error, and a plan that checks only the latter misses the former.

**Representation error by model.** For a grid the dominant term is within-cell aggregation; for a plane of slope $s$ sampled over a cell of size $\Delta$, the within-cell spread is $\sigma_c \approx s\,\Delta/\sqrt{12}$—0.29 m for a 1 m cell at 45°, 2.5 m for a 30 m cell at 16°—and any point check differs from the cell value by up to several $\sigma_c$ depending on the aggregation rule. For a TIN it is the facet error, bounded by the thinning tolerance $\tau$ or by curvature times squared edge length. For an LoD tile it is the declared geometric error. For an overview it is the kernel bias, which scales with block size and terrain curvature.

**Test conversion loss by round trip.** Grid the points, sample the grid at the point locations, and tabulate residuals by class and slope; their slope dependence tells you whether the cell size is appropriate. Build an overview, upsample it back with nearest resampling, and difference against the original; the 99th-percentile absolute difference is the overview's worst-case lie. Simplify a mesh and compute the two-sided Hausdorff distance against the use tolerance. Each test is cheap and produces a number that belongs in the metadata.

> **Worked example.** *Does an average overview misrepresent a navigation shoal?* A 2 m bathymetric grid has a pinnacle with least depth 4.1 m over a 3×3-cell patch in 12 m water. An 8× overview averages 64 cells: $(9\times4.1 + 55\times12.0)/64 = 10.9$ m. The overview reports 10.9 m where the chart must say 4.1 m—6.8 m in the unsafe direction, at the one place the product exists to protect. A shoal-biased overview reports 4.1 m. The test: downsample with the viewer's kernel, upsample back, and report the maximum depth *increase*; for a navigation product it must be zero.

**Validate the uncertainty definition, not just the value.** (1) *Type*: σ, 95 % bound, raw spread, or declared accuracy (§46.9)? Compare against the format's type field (BAG) or the metadata text. (2) *Calibration*: at independent checkpoints compute the standardized residual $(z_{\text{check}}-z_{\text{product}})/\sigma_{\text{product}}$; an honest 1σ band gives a standard deviation near 1 (0.5 means pessimistic by 2×; 3 means optimistic by 3×). Do this per source zone and slope class, because bands calibrated on the flat are routinely optimistic on slopes. (3) *Spatial behaviour*: a band constant within a source polygon is a declaration, not a propagation, and should be labelled as such.

**CUBE products.** Nodes with hypothesis count > 1 and low strength can be wrong by the hypothesis separation—often metres—regardless of the reported σ. Report the fraction and spatial distribution of multi-hypothesis nodes; a rising fraction across a survey usually signals a sound-speed or tide problem producing inter-line offsets, not real multi-valued seafloor.

**What to report.** The data model and its parameters (cell size and registration; aggregation rule; TIN tolerance and breaklines; LoD scheme; VR criteria), the overview kernel, the uncertainty type with its calibration statistics, and the conversion lineage from the richest representation that exists.

## Software

**Open source:** PDAL (pipelines, binning via `writers.gdal`, k-d neighbourhoods, COPC read/write); laspy (LAS/LAZ/COPC in Python, extra bytes); Entwine (EPT/COPC builders; caveat—per-node subsampling is fixed by the builder); Open3D and PyVista/VTK (meshes, voxels, marching cubes); CGAL and MeshLab (robust CDT, quadric simplification, Hausdorff/Metro); GDAL (overviews with explicit `-r`, BAG and VR BAG reading; caveat—the kernel is recorded in metadata but not shown by most viewers); GRASS GIS, SAGA, QGIS (TINs, binning with count/min/max/mean); OctoMap; MB-System (`mbgrid`, TPU; caveat—no CUBE).

**Free but closed:** NOAA HydrOffice/Pydro utilities for VR BAG and CUBE QC; Esri's I3S specification is open but reference tooling is proprietary.

**Commercial:** TerraSolid (classification, TIN modelling with breaklines); CARIS HIPS and SIPS/BASE Editor (CUBE/CHRT, VR BAG, hypothesis review; caveat—proprietary CSAR model); QPS Qimera and Fledermaus (CUBE, dynamic surfaces, water column); ArcGIS (terrain, LAS, and mosaic datasets; caveat—default pyramid kernel depends on data type); Bentley ContextCapture/iTwin (photogrammetric meshes, 3D Tiles/I3S export).

## Standards & guides

- ASPRS, *LAS Specification 1.4 – R15* (2019): PDRFs 0–10, extra bytes, waveform packets.
- ASPRS Lidar Division, *LAS Domain Profile Description: Topo-Bathy Lidar* (version 1.0, August 2013): per-point uncertainty, water-column depth, and figure-of-merit extra bytes; bathymetric classification codes.
- Open Navigation Surface WG, *BAG Format Specification Document* 2.0.x (2.0.1 released 2022; current documentation at bag.readthedocs.io): uncertainty-type enumeration, tracking list, VR extension.
- IHO, *S-102* Ed. 3.0.0 (December 2024): single-resolution tiled surfaces with QualityOfBathymetryCoverage; Ed. 3.1.0 in development at the time of writing.
- IHO, *S-44* Ed. 6.1.0 (2022): TVU/THU definitions per-node uncertainty is compared against.
- OGC, *3D Tiles* 1.1 (2023, OGC 22-025r4): tilesets, geometric error, implicit quadtree/octree tiling.
- OGC, *I3S and Scene Layer Package* community standard 1.3 (OGC 17-014r9, 2023); Cesium *quantized-mesh-1.0*; OGC *CityGML 3.0* (2021, OGC 20-010) and *CityJSON* 2.0 (2023).
- NASA ICESat-2 ATBDs for ATL03 and ATL08 (current releases, NSIDC).
- USGS, *Lidar Base Specification* 2024 rev. A (or current revision): density definitions assessed on a grid.
- Hobu Inc., *COPC Specification* 1.0 (2021).

## Pitfalls

- **Treating the DSM raster as "the data" when points exist** → the raster is what opens in a GIS → check lineage; do density, void, and aggregation checks on the cloud and regrid with a stated rule when the use needs a different surface.
- **Nearest overviews that dash every ridge and levee** → `nearest` is the fast default → difference an upsampled overview against the original; use `max`/`min` for safety-critical products and record the kernel.
- **Average overviews raising navigation shoals** → pyramids built for appearance → test for any depth increase under downsample/upsample; build shoal-biased overviews.
- **Flat triangles on ridges from contour sources** → Delaunay ignores elevation → look for zero-slope polygons on ridgelines and histogram spikes at the contour interval; add breaklines or use a contour-aware interpolator.
- **Uncertainty as an afterthought band with no definition** → the format allowed a band → declare the type; validate with standardized residuals.
- **Meshes rasterized to the highest surface by default** → first ray hit from above → bridges become dams; use face semantics, state the collapse rule, map multi-valued cells with a lowest-hit raster.
- **Assuming PixelIsArea on a PixelIsPoint product** → the georeferencing numbers look alike → read the raster-type key; the half-cell shift becomes a slope-proportional vertical bias.
- **CUBE σ taken as depth uncertainty at multi-hypothesis nodes** → only the σ layer was exported → inspect hypothesis count and strength; treat multi-hypothesis nodes as unresolved.

## Key takeaways

- A data model is a set of commitments; choose the structure that preserves what the use needs and name what it cannot hold.
- Points carry attributes (time, class, scan angle, uncertainty, density) no derived surface can recover; waveforms and photons carry the detector's uncertainty beneath the points. Archive the richest level you have.
- Grids are single-valued and area- or point-registered and hide density and multi-valuedness behind a collapse rule; write the rule and the registration into the metadata.
- Overviews are new products with their own kernel: average lowers peaks and raises shoals, nearest dashes ridges. Test the lie, choose the kernel by use, record it.
- TINs expose density and breaklines but inherit flat triangles from contours; meshes hold overhangs but not uncertainty; voxels carry "unknown" explicitly; splats render and do not measure.
- Variable-resolution surfaces let the data set the resolution; flattening them to one grid loses in one direction or invents in the other.
- Uncertainty attributes need a declared type and a calibration check; CUBE's σ is the σ of a chosen hypothesis, and count and strength are part of the uncertainty.
- Every arrow in the conversion matrix is a documented decision. Convert down for a purpose; never convert up and call it measurement.

## References

- American Society for Photogrammetry and Remote Sensing (2019). *LAS Specification 1.4 – R15*. ASPRS, Bethesda, MD.
- Calder, B. R., and Mayer, L. A. (2003). Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems*, 4(6), 1048. doi:10.1029/2002GC000486
- Calder, B. R., and Rice, G. (2017). Computationally efficient variable resolution depth estimation. *Computers & Geosciences*, 106, 49–59. doi:10.1016/j.cageo.2017.05.013
- Garland, M., and Heckbert, P. S. (1997). Surface simplification using quadric error metrics. *Proceedings of SIGGRAPH '97*, 209–216.
- Hobu Inc. (2021). *Cloud Optimized Point Cloud (COPC) Specification 1.0*. https://copc.io
- Hornung, A., Wurm, K. M., Bennewitz, M., Stachniss, C., and Burgard, W. (2013). OctoMap: An efficient probabilistic 3D mapping framework based on octrees. *Autonomous Robots*, 34(3), 189–206.
- International Hydrographic Organization (2024). *S-102 Bathymetric Surface Product Specification*, Edition 3.0.0. IHO, Monaco.
- Kerbl, B., Kopanas, G., Leimkühler, T., and Drettakis, G. (2023). 3D Gaussian splatting for real-time radiance field rendering. *ACM Transactions on Graphics*, 42(4), Article 139.
- Mallet, C., and Bretar, F. (2009). Full-waveform topographic lidar: State-of-the-art. *ISPRS Journal of Photogrammetry and Remote Sensing*, 64(1), 1–16.
- Neuenschwander, A., and Pitts, K. (2019). The ATL08 land and vegetation product for the ICESat-2 mission. *Remote Sensing of Environment*, 221, 247–259.
- Neumann, T. A., et al. (2019). The Ice, Cloud, and Land Elevation Satellite-2 mission: A global geolocated photon product derived from the Advanced Topographic Laser Altimeter System. *Remote Sensing of Environment*, 233, 111325.
- Open Geospatial Consortium (2023). *3D Tiles Specification 1.1*, OGC 22-025r4.
- Open Navigation Surface Working Group (2024). *Bathymetric Attributed Grid (BAG) Format Specification Document*, version 2.0.x. https://bag.readthedocs.io (code: https://github.com/OpenNavigationSurface/BAG)
- Peucker, T. K., Fowler, R. J., Little, J. J., and Mark, D. M. (1978). The triangulated irregular network. *Proceedings of the ASP Digital Terrain Models (DTM) Symposium*, St. Louis, 516–540.
- Samet, H. (1984). The quadtree and related hierarchical data structures. *ACM Computing Surveys*, 16(2), 187–260.
- Wagner, W., Ullrich, A., Ducic, V., Melzer, T., and Studnicka, N. (2006). Gaussian decomposition and calibration of a novel small-footprint full-waveform digitising airborne laser scanner. *ISPRS Journal of Photogrammetry and Remote Sensing*, 60(2), 100–112.

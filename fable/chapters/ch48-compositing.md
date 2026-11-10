# Chapter 48 — Compositing: merging many datasets into one product

> **Part X — Representing, storing, finding, and keeping elevation data.** The chapter about seamless products: how surveys of different dates, sensors, datums, and quality are ordered, blended, cropped, and overridden into one grid, and what that grid's cells then mean.

**In this chapter.** Almost every DEM a user downloads is a composite—a decision about which of several measurements to show at each cell, made by someone else, usually undocumented. You will be able to prepare heterogeneous sources for merging (common horizontal and vertical datum, harmonized surface type, aligned resolution, co-registration and bias removal over overlaps, per-source artefact screening); choose and declare a prioritization rule (best, newest, finest, shoal-biased) and recognize how NOAA's National Bathymetric Source, GEBCO, EMODnet, and USGS 3DEP make that choice; blend across overlaps with distance-weighted or gradient-domain methods and know when a hard seam is more honest than a feather; handle the land–water transition where topographic lidar, bathymetric lidar, sonar, and satellite-derived bathymetry meet across different datums; produce the companion rasters—source, date, uncertainty, method—without which a composite cannot be validated or used for change; run seam, connectivity, and checkpoint QC by source zone; and version the build so that a bad source can be retracted and "what changed since v2.1" can be answered with a raster.

## 48.1 Why composite, and what it costs

No single survey covers a watershed, a coast, or a nation at the resolution and currency its users want. Compositing buys **coverage** (filling gaps between surveys with coarser data), **currency** (replacing old cells with new ones where resurveys exist), **resolution** (showing the finest available data where it exists), and **cost** (reusing what was already paid for). National products—USGS 3DEP's seamless DEMs, NOAA's BlueTopo, GEBCO, EMODnet Bathymetry, Copernicus DEM, national lidar mosaics—are composites by construction, and so is nearly every project DEM that combines a new lidar survey with an older fill.

The price has three parts. **Inhomogeneous error**: a composite cell drawn from a 2023 lidar survey has an uncertainty of centimetres; its neighbour, from a 1960s lead-line survey or a satellite-gravity prediction, has an uncertainty of metres to hundreds of metres; nothing in the elevation value tells the user which is which. **Hidden seams**: where sources meet, the composite contains steps, slope changes, and texture changes that are artefacts of the merge, indistinguishable from terraces, scarps, and channels unless the seam locations are published. **Ambiguous provenance**: a cell's date, sensor, datum conversion path, and processing history are properties of its source, and a composite that does not carry per-cell source identifiers has thrown them away. A composite therefore is not a measurement; it is a *decision* about measurements, and the chapter's thesis is that the decision must be published alongside the surface ([Chapter 49](ch49-metadata.md)).

## 48.2 Preparation

Most composite failures are preparation failures. Each source must be brought onto a common footing before any priority or blend rule is applied.

### 48.2.1 Common horizontal and vertical datum

Sources arrive in different horizontal datums and realizations (NAD83(2011) epoch 2010.0, NAD83(NSRS2007), WGS 84 (G1762), ITRF2014 at various epochs; [Chapter 8](ch08-horizontal-datums.md)) and, more consequentially, different vertical datums: orthometric heights on different geoid models (NAVD88 via GEOID12B versus GEOID18; EGM96 versus EGM2008), ellipsoidal heights, and tidal datums (MLLW, MSL, LAT, chart datum) whose relationship to the orthometric surface varies spatially by decimetres to metres ([Chapter 9](ch09-vertical-datums.md)). The conversion chain for a hydrographic source going into a topographic composite is tidal → ellipsoidal → orthometric, each step with its own uncertainty: NOAA's **VDatum** publishes a per-region uncertainty for each transformation (of order 5–20 cm for tidal-to-orthometric in US waters, varying by region), and NOAA's open **vyperdatum** wraps VDatum grids in a PROJ pipeline so that the transformation, its version, and its uncertainty are logged. Land sources need the geoid-model step made explicit: two NAVD88 lidar DEMs on different geoid models differ by the geoid-model difference, which can be several centimetres and spatially smooth—an unnoticed tilt. The output datum should be chosen for the use (ellipsoidal for exchange and change detection, orthometric for hydrology and engineering, tidal for navigation) and every source's path to it recorded in the lineage table (§48.7).

### 48.2.2 Surface-type harmonization

A DSM, a DTM, a hydro-flattened DTM, a bathymetric "seafloor," a topobathymetric lidar bare-earth, and a photogrammetric mesh rasterized to its highest surface are different surfaces ([Chapter 4](ch04-names-and-definitions.md), [Chapter 32](ch32-dsm-to-dtm.md)). Merging a DSM source into a DTM composite plants a forest at the seam; merging a hydro-flattened DTM beside a non-flattened one creates a step at every river bank; merging a bathymetric surface that represents the seabed under vegetation (kelp, seagrass) beside a bathy-lidar surface that stopped at the canopy top produces a false ledge. Decide the composite's surface type, inspect each source's definition (what was removed, what was flattened, how water is treated), and either convert (DSM→DTM with the methods of [Chapter 32](ch32-dsm-to-dtm.md), at a documented accuracy cost) or exclude.

### 48.2.3 Resolution alignment

The composite grid has one cell size (or a VR scheme; [Chapter 46](ch46-data-models.md)). Finer sources must be aggregated to it with a stated kernel—mean for a general-purpose DEM, minimum depth for a navigation surface—and coarser sources must be resampled *up* with a stated interpolator, producing cells whose effective resolution ([Chapter 44](ch44-resolution-and-sampling.md)) is the source's, not the grid's. Record the source's native resolution per cell (§48.7) so that users can tell a 1 m cell measured at 1 m from a 1 m cell interpolated from 90 m. Align grids by resampling onto the composite lattice once, with the pixel convention checked ([Chapter 47](ch47-file-formats.md)); do not let each tool resample on the fly with its own default.

### 48.2.4 Co-registration and bias removal over overlaps

Where sources overlap, difference them. A systematic offset in the overlap is a datum, geoid, tide, or calibration error in one source (or both) and must be resolved *before* merging, or the merge will carry it into the seam as a step. [Chapter 41](ch41-change-detection.md) gives the methods: a robust vertical bias (median of differences over stable, flat, open ground or seafloor), a horizontal shift estimated from the slope–aspect dependence of the differences (Nuth and Kääb 2011), and, if justified, a planar tilt. Apply the correction to the less trustworthy source, record the correction and its estimation statistics in the lineage, and re-difference to confirm the residual is zero-mean. Over water–land overlaps, the overlap may be a thin strip in the intertidal zone where neither source is at its best; use the widest stable overlap available and accept larger uncertainty.

### 48.2.5 Outlier and artefact screening

Each source brings its own defects: lidar DEMs with bridge decks left in or removed inconsistently, building fragments under trees, swath-edge steps; sonar grids with refraction smiles, nadir stripes, and unflagged fliers; SDB with cloud-edge artefacts and turbidity-induced shoaling; legacy grids with contour terraces and interpolation ridges across voids ([Chapter 35](ch35-voids-and-overhangs.md), [Chapter 54](ch54-evaluating-others-data.md)). Screen each source before merging with a low-sun hillshade sweep, a slope histogram, a spike filter, and a difference against any overlapping neighbour, and mask the defects as nodata so that the priority rule falls through to the next source instead of promoting the defect.

> **Case file.** Eakins and Grothe (2014) catalogue the challenges in building NOAA's coastal DEMs from heterogeneous bathymetry and topography and report that the dominant failures were not in the gridding but in the inputs: vertical datum mismatches between neighbouring surveys of 0.3–1 m read as seafloor steps; shoreline inconsistencies between the topographic and bathymetric sources producing false cliffs and trenches at the coast; and undocumented surface types (vegetation left in lidar, dredged channels in old charts) that no blend could fix. Their recommendation—resolve datum and shoreline before gridding, and publish source and uncertainty layers—became the practice in NCEI's CUDEM program.

## 48.3 Prioritization rules

At every cell where more than one prepared source exists, something must decide. The rule is the heart of the composite and must be explicit.

**By uncertainty ("best wins").** Each source carries a vertical uncertainty, propagated or assigned, and the lowest-uncertainty source takes the cell. This is the engineering default and is what inverse-variance weighting (Mathematics) formalizes when sources are blended rather than switched. Its failure mode is bias: a precise but biased source wins over an accurate but noisy one.

**By date ("newest wins").** The most recent source takes the cell, on the argument that the surface changes and the latest observation is most representative. This is right for dynamic environments (dredged channels, migrating sandbars, post-event landscapes; [Chapter 37](ch37-time-scales-of-change.md)) and wrong where the newest source is a coarse reconnaissance over an older high-quality survey of stable ground.

**By resolution ("finest wins").** The finest native resolution takes the cell. Correlated with quality but not identical to it; a 1 m SDB grid is finer and worse than a 5 m multibeam grid.

**By surface type.** In a topobathymetric composite the bathymetric source wins below a shoreline and the topographic above it; in a DTM composite a bare-earth source wins over a DSM regardless of other properties.

**By source tier.** Agencies publish hierarchies. **NOAA's National Bathymetric Source** (NBS), which produces **BlueTopo**, scores each survey on quality, age, and resolution and applies **supersession** rules so that a newer, adequate survey replaces an older one but a coarse or low-quality survey does not displace a better older one; the resulting per-cell *contributor* is published as a band with a raster attribute table listing the survey, date, and uncertainty (the scoring and supersession details are in the current NBS documentation and have evolved between releases). **GEBCO** builds from regional compilations (the Seabed 2030 regional centres and IHO DCDB holdings), prefers direct measurements over predictions, and publishes the per-cell **Type Identifier** (TID) so users can see the method (§48.7). **EMODnet Bathymetry** merges contributed DTMs by a priority order and publishes a source-reference layer per cell. **USGS 3DEP** seamless products are assembled from project DEMs by a "best available" rule in which newer, higher-quality-level lidar supersedes older sources, with the project boundaries available as a separate layer.

**Use-dependent overrides.** The rule depends on what the composite is for. A navigation surface is **shoal-biased**: where sources disagree, the shoalest credible depth wins, and the newest survey of a dredged channel wins over an older deeper one, but an older shoal sounding is retained unless a newer survey *disproves* it with adequate feature detection (IHO S-44 and NOAA HSSD practice). A change-detection baseline is **most-recent**, with the date layer mandatory. An engineering design surface is **most-accurate**, with a stated date. One source set can legitimately produce three different composites; what is not legitimate is one composite presented for all three uses.

> **Definitions that bite.** *Best available.* Every national program says it; none means the same thing. For 3DEP "best" is quality level then date; for NBS it is a weighted score with supersession; for GEBCO it is direct-over-indirect then regional-centre judgement; for a project it is often "whatever was on the drive." Write the ordering as a sorted list of criteria with tie-breakers, and store the rule's version with the product.

## 48.4 Blending and feathering

Switching sources at a line produces a seam; blending them across an overlap zone hides it. Hiding is not always honest.

**Distance-weighted feathering.** In the overlap zone, weight each source by its distance from its own edge so that weights go from 1 to 0 smoothly across the zone (Mathematics). GMT's `grdblend` implements this with per-grid inner regions and weights; GDAL has no direct feathering but `gdalwarp` with cutlines and `-cblend` blends a cutline's edge over a specified pixel distance. Feathering across a 100 m zone turns a 0.5 m step into a 0.5 % slope—invisible in a hillshade and wrong everywhere in the zone, because the blended cell is a value no instrument measured.

**Gradient-domain blending.** Rather than blending values, blend gradients and solve a Poisson equation for the surface that best matches them (Pérez et al. 2003, developed for images). This removes low-frequency offsets while preserving each source's texture, and is attractive when one source has a smooth bias; it also moves the error into a global adjustment that is hard to attribute to a cell.

**Breakline-aware merges.** Where a real discontinuity exists in the overlap zone—a sea wall, a channel bank, a cliff—a feather smears it. Introduce the discontinuity as a breakline or hard mask boundary and blend only within each side.

**No blend, hard edge, documented seam.** Switch at a line, leave the step, and publish the seam line and the step statistics. Users who need a smooth surface can smooth it; users who need the truth can see it. For products that carry an uncertainty layer, the step at the seam is itself a measurement of the two sources' combined error and belongs in the QC report (§48.8).

Two named dangers recur. The **blended cliff**: an offset between a lidar DTM and a coarser fill feathered across a zone that happens to contain a real scarp produces a smoothed ramp whose position and height match neither the scarp nor the offset. The **feathered channel**: a navigation channel surveyed by multibeam, feathered into an older surrounding grid that predates dredging, acquires sloped walls and a shoaled centreline that would ground a vessel designed to the dredged depth; navigation composites must switch, not feather, at channel limits.

> **Rule of thumb.** Blend only after bias removal has made the overlap difference zero-mean, blend over a zone no wider than a few times the coarser source's resolution, never blend across a known discontinuity, and never blend a navigation surface. If the residual step after bias removal exceeds the combined uncertainty of the two sources, do not blend—investigate.

<!-- figure: Figure 48.1 — Cross-sections through a lidar/legacy-DEM overlap under four merge rules: hard switch (visible 0.4 m step), 100 m feather (ramp), gradient-domain blend (texture preserved, offset absorbed), and feather across a real scarp (the blended cliff), with the per-cell uncertainty traced beneath each. -->

## 48.5 Cropping and masks

A source should contribute only where it is valid, and validity is a polygon, not a bounding box. **Footprints** must be the actual data extent—the hull of the measured cells, eroded by a margin equal to the gridding search radius so that edge extrapolation does not enter the composite—rather than the tile rectangle, which includes nodata and interpolated fringe. **Water masks** decide which source speaks in rivers, lakes, and the sea (§48.6) and which cells are flattened or set to a water-surface elevation ([Chapter 34](ch34-water-in-dems.md)). **Void masks** record where a source had no measurement and was filled, so that the composite's fill cells can be attributed to the fill method rather than to the source ([Chapter 35](ch35-voids-and-overhangs.md)). **Quality masks** exclude parts of a source that failed screening (§48.2.5) or that fall below a declared quality threshold—outer multibeam beams beyond a grazing-angle limit, lidar swath edges, SDB deeper than its validated range.

**Copernicus DEM** is the exemplar of publishing masks with the product: alongside the elevation it distributes an **editing mask** (EDM, which cells were edited and how—water flattened, void filled, airports levelled), a **filling mask** (FLM, which auxiliary DEM filled a void), a **height error mask** (HEM, the per-cell height error estimate from the TanDEM-X interferometric coherence), and a **water body mask** (WBM), each a co-registered raster. A user can therefore remove the edited cells, treat filled cells with the fill source's uncertainty, and reason about the HEM as a per-cell σ. Any composite can do the same, and the masks cost little compared to the surface.

## 48.6 The land–water seam

The coast is where compositing is hardest, because the sources differ in every respect at once: sensor (topographic lidar, bathymetric lidar, multibeam and single-beam sonar, SDB, charted soundings), vertical datum (orthometric on land, tidal at sea), surface definition (bare earth, canopy top, seabed, chart safety surface), and date (the intertidal zone changes seasonally). Four practices make it tractable.

**One vertical datum, converted with a published model.** NOAA NCEI's **CUDEM** (Continuously Updated DEM) tiles are built on NAVD88, with bathymetric sources converted from MLLW through VDatum and the conversion uncertainty carried into the cell uncertainty (Amante and Eakins 2016; Amante 2018). USGS **CoNED** topobathymetric models (Danielson et al. 2016) follow the same principle with per-source datum conversions documented in a source table. Outside the US the equivalent is the national separation model (e.g., the UKHO's VORF in the UK, AusCoastVDT in Australia).

**A consistent shoreline.** The shoreline in the composite must be a single line derived from, or at least consistent with, the chosen sources at the chosen datum; using the lidar's water edge (at whatever tide was flying) as the bathymetry's landward limit produces a gap or an overlap of tens of metres on flat coasts. Derive the shoreline from the composite's own datum (the zero contour of the merged surface at MHW or MLLW as the use requires), and let the source-switch line sit seaward of the lowest tide the topographic lidar observed so that the intertidal zone is taken from whichever source actually measured it.

**Tidal datum surfaces for the transition.** Where topographic lidar flown at low tide and bathymetric lidar or sonar overlap in the intertidal zone, the overlap is the only place the two datum chains can be checked against each other; use it (§48.2.4). Where they do not overlap—a dry beach above the sonar's shallowest line—the gap must be interpolated, and the interpolation across an intertidal flat is the single largest uncertainty in many coastal DEMs (Amante and Eakins 2016 quantify interpolation error as a function of distance from measurements, reaching metres in sparse legacy soundings).

**Cross-border seams.** National DEMs meet at borders with different vertical datums: the Dutch NAP and the Belgian TAW differ by about 2.33 m (the TAW zero lies below NAP, so TAW heights are the larger), and the pre-EVRS national datums of Europe differed by decimetres among neighbours. A composite that crosses such a border without conversion contains a terrace along the frontier; the EVRS realizations and national transformation grids exist to remove it ([Chapter 9](ch09-vertical-datums.md)).

The common failure here is the **invented beach**: a topographic source ending at the wet/dry line, a sonar source starting 200 m offshore, and a feather or an interpolator joining them with a smooth slope that no one measured and that sits a metre above or below the true intertidal profile. Mark such cells in the method layer as interpolated, with an uncertainty that grows with distance from the nearest measurement.

<!-- figure: Figure 48.2 — Coastal profile across the land–water seam showing topographic lidar (NAVD88), bathymetric lidar and multibeam (MLLW → NAVD88 via VDatum with uncertainty band), the un-surveyed intertidal gap, the interpolated segment flagged in the method layer, and the shoreline derived from the merged surface at MHW. -->

## 48.7 Mandatory companion layers

A composite without companion layers is unverifiable and unusable for change. The minimum set, each co-registered with the surface:

| Layer | Content | Type | Why |
|---|---|---|---|
| Source ID | Integer key into the lineage table | Categorical (mode/nearest overviews) | Attribution, retraction, per-zone validation |
| Acquisition date | Decimal year or days since epoch; start and end if a source spans years | Continuous or categorical | Change detection; currency; dynamic areas |
| Uncertainty | Vertical 1σ (or 95 %, declared) per cell, propagated or assigned per source, inflated for datum conversion and interpolation | Continuous | Fitness for use; weighting in later merges |
| Method / TID | Sensor and method class (direct multibeam, lidar, SDB, interpolated, predicted…) | Categorical | Separates measured from modelled cells |
| Native resolution | Source cell size or point spacing at this cell | Continuous | Effective resolution; distinguishes measured 1 m from upsampled 90 m |
| Masks | Void/fill, water, edited, quality | Bit flags | Same roles as Copernicus EDM/FLM/WBM |

The **lineage table** is keyed by source ID and holds the source's name and identifier, custodian, sensor, dates, native resolution, horizontal and vertical datum as received, the transformation path and model versions applied, the bias correction applied over overlaps and its statistics, the surface type, the declared or assessed accuracy, the priority rank, and the masks applied. It travels as a CSV/GeoPackage table and as a raster attribute table on the source-ID band (BlueTopo's pattern). **Mosaic-level metadata** states the priority rule and its version, the blend method and zone width, the output datum and geoid or tidal model, the build date, the software versions, and the known issues.

GEBCO's **Type Identifier** grid is the model for the method layer. A subset of codes (see the GEBCO documentation for the full list): 0 land; 10 single-beam; 11 multibeam; 12 seismic; 13 isolated sounding; 14 ENC sounding; 15 lidar; 16 optical; 17 combination of direct methods; 40 predicted from satellite gravity; 41 interpolated; 42 and 43 digitized contours from charts and ENCs; 70 pre-generated grid; 71 unknown source. The practical consequence of publishing the TID is that users can mask GEBCO to directly measured cells—26.1 % of the ocean floor at the GEBCO_2024 release, by Seabed 2030's accounting—and treat the rest as a model.

## 48.8 QC of composites

Composite QC adds seam and consistency tests to the per-source accuracy assessment of [Chapter 53](ch53-accuracy-assessment.md).

**Seam statistics.** Along every source boundary (derived from the source-ID layer), sample the elevation step across the boundary and the slope on either side. Report the median and 95th-percentile step by boundary pair, and compare each pair's step distribution against the combined uncertainty of the two sources; a step larger than $2\sqrt{\sigma_1^2 + \sigma_2^2}$ is a datum or bias failure, not noise. Map the steps; clusters along a particular source's boundary indicate that source's bias.

**Gradient and texture sweeps.** Compute slope and aspect; a seam appears in the slope raster as a line of anomalous values and in the aspect raster as a line where aspect flips. Compute a local roughness (standard deviation of elevation in a moving window); texture changes across boundaries reveal resolution and smoothing differences that the elevation step does not. **Slope and aspect histograms** computed per source zone should be similar for similar terrain; a zone whose slope histogram is shifted toward zero is over-smoothed, and one with spikes at particular azimuths has gridding artefacts.

**Hillshade sweeps.** Render multi-azimuth, low-angle hillshades and look. Seams, feathers, contour terraces, tile edges, and interpolation ridges are visible to a trained eye at a glance and invisible to statistics that average over the product; a systematic visual sweep at two scales is part of every composite's QC ([Chapter 57](ch57-visualizing-dems.md)).

**Hydro-connectivity.** Run a flow-direction and sink-fill analysis; count the sinks and the fill volume per source zone and along boundaries. A seam step that dams a valley produces a sink on the uphill side; a feathered channel produces a spurious divide. For bathymetric composites, trace navigation channels for shoaling at source boundaries.

**Independent checkpoints per source zone.** Checkpoints assessed against the composite must be stratified by source zone and by method class, because a pooled RMSE averages a 5 cm lidar zone with a 2 m legacy zone into a number that describes neither. Report accuracy per zone with checkpoint counts, and compare each zone's residuals against its uncertainty layer (standardized residuals should have σ ≈ 1; [Chapter 46](ch46-data-models.md)).

> **Try it.** Priority-ordered mosaic with GDAL VRTs, then a feathered blend with GMT, with seam statistics.
> ```bash
> # 1. Priority mosaic: later files override earlier ones in a VRT.
> #    Order: coarse fill first, legacy survey, then lidar (highest priority last).
> gdalbuildvrt -resolution user -tr 2 2 -tap -srcnodata -9999 -vrtnodata -9999 \
>   mosaic.vrt fill_30m.tif legacy_5m.tif lidar_1m.tif
> gdal_translate -co COMPRESS=ZSTD -co TILED=YES mosaic.vrt composite_switch.tif
> # 2. Source-ID raster from the same ordering (constant rasters per source).
> for i in 1 2 3; do f=$(sed -n "${i}p" <<< $'fill_30m.tif\nlegacy_5m.tif\nlidar_1m.tif');
>   gdal_calc.py -A "$f" --calc="where(A!=-9999,$i,0)" --NoDataValue=0 --type=Byte --outfile=src_$i.tif; done
> gdalbuildvrt -srcnodata 0 -vrtnodata 0 srcid.vrt src_1.tif src_2.tif src_3.tif
> # 3. Feathered alternative with GMT grdblend (weights taper to 0 at each grid's edge).
> printf "fill_30m.tif -R-123.2/-122.8/37.6/37.9 1\nlegacy_5m.tif -R-123.1/-122.9/37.65/37.85 2\nlidar_1m.tif -R-123.05/-122.95/37.7/37.8 4\n" > blend.txt
> gmt grdblend blend.txt -R-123.2/-122.8/37.6/37.9 -I2e -Gcomposite_blend.nc -V
> # 4. Seam visibility: slope rasters of both products.
> gdaldem slope composite_switch.tif slope_switch.tif
> gdaldem slope composite_blend.nc slope_blend.tif
> ```
> Expected outcome: `slope_switch.tif` shows the source boundaries as lines of high slope whose magnitude equals the inter-source step divided by the cell size; `slope_blend.tif` hides them. Extract the step distribution by sampling `composite_switch.tif` on either side of the boundary polygons derived from `srcid.vrt` (`gdal_polygonize.py srcid.vrt`), and compare its 95th percentile to the combined source uncertainty before deciding whether blending is permissible.

## 48.9 Versioning composites

A composite is rebuilt whenever a source is added, corrected, or withdrawn, and users need to know what changed. **Reproducible builds**: the build is a script (GDAL/GMT/Python pipeline, or a CARIS/ArcGIS mosaic-dataset definition exported as text) with pinned software versions and a manifest of input source identifiers and checksums; given the manifest, the product can be regenerated. **Supersession logs**: each build records which sources entered, which were superseded in which cells, and why (new survey, bias correction revised, source retracted). **"What changed since" rasters**: for each release, publish the difference raster against the previous release and a change-reason raster (source changed, datum model updated, edit applied), so that a user who built a flood model on v2.1 can see that the 0.3 m change in their reach is a geoid-model update and not erosion. **Retraction**: when a source is found defective, the build must be able to remove it and let the priority rule fall through; this is only possible if the composite kept the per-cell source ID and the sources themselves. NOAA's NBS republishes BlueTopo tiles as sources change, with per-tile version metadata; USGS 3DEP marks project DEM replacements in its product index; GEBCO issues annual grids with a changelog. Icechunk-style versioned stores ([Chapter 47](ch47-file-formats.md)) and persistent identifiers per release ([Chapter 50](ch50-archiving-and-provenance.md)) are the infrastructure; the discipline is to never overwrite a release in place.

## Then & now

Compilation is older than digital data: hydrographic offices have always compiled charts from surveys of different dates and qualities, applying shoal-biased selection by hand and recording the sources in a **source diagram** on the chart—the ancestor of the source-ID layer. Early digital DEMs were "best available" mosaics with no provenance: **GTOPO30** (USGS, 1996) ⟨H⟩ combined DTED, the Digital Chart of the World contours, and other sources into a 30″ global grid and published a source map as a separate layer, which was advanced for its time. SRTM mosaics (2000s) and ASTER GDEM used void-fill from other DEMs with limited per-cell flagging; GMTED2010 (Danielson and Gesch 2011) improved the source bookkeeping. **GEBCO** moved from contour-based grids to gridded compilations with the per-cell TID in its 2014 release and has published source type ever since. **EMODnet Bathymetry** (2009–) built the European DTM from contributed grids with a source-reference layer. **NOAA's National Bathymetric Source** (program from the late 2010s; BlueTopo public releases from the early 2020s) made per-cell source, date, and uncertainty with explicit supersession the standard for a national navigation compilation. On land, **USGS 3DEP** replaced the NED's opaque mosaic with a seamless product whose project boundaries and quality levels are published, and the 1 m DEM program made lidar-derived cells the norm. **Copernicus DEM** (2019–) set the standard for publishing masks with a global product. The trajectory is from hidden decisions to published ones: source diagrams in the margin became source rasters in the file.

## Mathematics

**Inverse-variance combination.** If $n$ sources give unbiased, independent estimates $z_i$ of the same cell with variances $\sigma_i^2$, the minimum-variance unbiased combination is

$$\hat z = \frac{\sum_i w_i z_i}{\sum_i w_i}, \qquad w_i = \frac{1}{\sigma_i^2}, \qquad \mathrm{Var}[\hat z] = \frac{1}{\sum_i 1/\sigma_i^2}.$$

With $\sigma_1 = 0.1$ m and $\sigma_2 = 1.0$ m, $w_1 : w_2 = 100 : 1$ and $\sigma_{\hat z} = 0.0995$ m—the poor source contributes almost nothing, which is why "best wins" and inverse-variance blending give nearly the same surface when uncertainties differ by an order of magnitude. The formula is invalid under **bias**: if source 2 has a systematic offset $b$, the combined estimate has bias $b\,w_2/(w_1+w_2)$ and the stated variance is wrong; with equal weights the bias halves rather than vanishing. Bias must be removed (§48.2.4) before weights mean anything, and the residual bias uncertainty $\sigma_b^2$ should be added to $\sigma_i^2$.

**Distance-based feather weights.** For two sources overlapping in a zone, let $d_1(x)$ be the distance from cell $x$ to the edge of source 1's footprint (measured inward) and $d_2(x)$ likewise. A linear feather uses $w_1 = d_1/(d_1 + d_2)$, $w_2 = 1 - w_1$; GMT `grdblend` tapers each grid's weight linearly from its full value inside a user-set inner region to zero at the grid's outer edge and normalizes. A cosine taper $w_1 = \tfrac12\left(1 - \cos(\pi d_1/(d_1+d_2))\right)$ avoids slope discontinuities at the zone edges. Feather weights are geometric, not statistical; combining them with inverse-variance weights ($w_i \propto f_i(x)/\sigma_i^2$) is common and reasonable only if the sources are unbiased.

**Uncertainty of a composite cell under source switching.** When the cell takes one source outright, its uncertainty is that source's $\sigma_i$ plus the datum-conversion and resampling terms in quadrature. When the cell is a blend with weights $w_i$ (normalized), the variance of the blended value is $\sum_i w_i^2 \sigma_i^2$ if the sources are independent and unbiased—but the *relevant* uncertainty for a user is the mixture variance

$$\sigma_{\text{mix}}^2 = \sum_i w_i \sigma_i^2 + \sum_i w_i\,(z_i - \hat z)^2,$$

which includes the disagreement between sources. In a feather zone where the sources differ by a step $\Delta$, the second term is up to $\Delta^2/4$ at the midpoint; a composite that reports only the first term understates the uncertainty exactly where the sources disagree.

**Seam detection via gradient statistics.** Along a boundary $B$ between zones $i$ and $j$, sample pairs of cells $(x_i, x_j)$ straddling $B$ at spacing $\Delta$ and compute $s_k = z(x_i) - z(x_j) - \Delta\,\bar{g}_k$, where $\bar g_k$ is the mean along-normal gradient estimated from cells one or more steps away on each side (so that true slope is removed). The seam step is the median of $s_k$; its significance is tested against $\sqrt{\sigma_i^2 + \sigma_j^2 + 2\sigma_g^2\Delta^2}$ with $\sigma_g$ the gradient estimation noise. Equivalently, a seam is a line along which the second derivative normal to the line has a persistent sign; a Laplacian filtered along the source-ID boundary isolates it.

## Validation & uncertainty

A composite's error field is piecewise: within a source zone it is the source's error after transformation; at the seams it is the sources' disagreement; in interpolated gaps it is the interpolation error. Validation must address each piece and must produce a per-cell uncertainty layer that is honest about all three.

**Per-source uncertainty, transformed.** Start from each source's assessed accuracy (checkpoint-based where it exists, declared otherwise; [Chapter 53](ch53-accuracy-assessment.md) and [Chapter 54](ch54-evaluating-others-data.md)). Add in quadrature the datum transformation uncertainty (VDatum's published values or the geoid-model difference), the resampling error ($s\,\Delta/\sqrt{12}$ for slope $s$ and the larger of source and target cell sizes), and the residual bias uncertainty after co-registration. For a legacy survey converted from MLLW with a 0.15 m VDatum uncertainty and a 0.5 m declared accuracy, the transformed σ is $\sqrt{0.5^2 + 0.15^2} = 0.52$ m; for a lidar DTM with 0.05 m assessed σ and a 0.03 m geoid-model term it is 0.058 m. These become the uncertainty layer within each zone.

**Interpolated and filled cells.** Where the composite interpolates across gaps between sources (the intertidal flat, the void in a legacy grid), uncertainty must grow with distance from the nearest measurement. Amante and Eakins (2016) fitted empirical functions of interpolation error against distance and terrain for coastal DEMs and found errors reaching metres over kilometre-scale gaps in sparse sounding fields; a practical approach is to withhold a sample of measurements, interpolate without them, and fit the residual's standard deviation as a function of distance, then apply that function to the method layer's interpolated cells.

**Seams.** The seam statistics of §48.8 are validation data. For each source pair, the median step is a bias that should have been removed; the spread of the step about its median, divided by $\sqrt{2}$ if the sources are comparable, is an independent estimate of the sources' combined random error and should agree with the uncertainty layer. Where it does not, the uncertainty layer is wrong.

**Checkpoints by stratum.** Pool nothing. Report, per source zone and per method class, the checkpoint count, mean error (bias), RMSE or NMAD, and the 95th-percentile absolute error, and compare each to the uncertainty layer's values at the checkpoint locations with standardized residuals. A composite's single headline accuracy number is meaningful only as the areal-weighted summary of these strata and should be presented as such.

> **Worked example.** *Is the terrace a seam?* A coastal composite shows a 0.6 m step along a straight line. The source-ID layer shows a 2019 topobathy lidar (assessed σ = 0.10 m, NAVD88 via GEOID18) on one side and a 2004 single-beam survey (declared 0.3 m at 95 % ≈ 0.15 m σ, MLLW, converted with VDatum at 0.12 m σ) on the other. Combined σ: $\sqrt{0.10^2 + 0.15^2 + 0.12^2} = 0.22$ m; the step is 2.7σ, so it is not noise. Seam sampling along 400 straddling pairs gives median step 0.58 m, spread (NMAD) 0.19 m. The spread agrees with the combined σ (0.19 ≈ 0.22), so the random errors are as stated and the step is a bias. The 2004 survey's metadata lists "MLLW" but the survey report shows soundings reduced to a local tide staff set to the 1983–2001 epoch MLW, 0.5 m above the modern MLLW in this estuary. Correcting the datum removes 0.5 m of the step; the remaining 0.08 m is within uncertainty. The terrace was a datum error, caught because the composite kept the source ID and the seam was measured rather than feathered.

**Hydro-connectivity as validation.** Sinks and spurious divides created at seams are errors with a direct consequence for hydrologic users ([Chapter 61](ch61-hydrology.md)); count them, attribute them to boundaries, and fix the cause (bias, feather) rather than filling the symptom.

**What to report.** The priority rule and its version; the blend method and zone width; per-source transformed uncertainty and how it was obtained; seam statistics per source pair; per-stratum checkpoint results with standardized residuals; the fraction of cells by method class (measured, interpolated, predicted); hydro-connectivity counts; the build manifest; and the difference raster against the previous release.

## Software

**Open source:** GDAL (`gdalbuildvrt` for priority mosaics with nodata fall-through, `gdalwarp` with `-cutline`/`-cblend` for masked and edge-blended merges, `gdal_merge.py`, VRT mask bands and per-source `<ComplexSource>` scaling; caveat—no statistical weighting, and later-wins ordering is easy to get backwards); GMT `grdblend` (weighted feathering with per-grid inner regions; `grdfill`, `grdmath`); MB-System `mbgrid` (gridding many surveys with weights by data type and footprint); WhiteboxTools (mosaic with feathering, sink analysis); NOAA NCEI **cudem** (`waffles` gridding modules with source ranking, per-source datum conversion, uncertainty estimation; the CUDEM production toolkit); xarray/dask pipelines for large stacks; QGIS (visual QC, raster calculator); **vyperdatum** (NOAA, free, open; PROJ pipelines over VDatum grids); PDAL for point-level merges; Icechunk/Zarr for versioned stores.

**Free but closed:** NOAA **VDatum** (Java; the transformation grids and uncertainty tables are public).

**Commercial:** CARIS BASE Editor and Bathy DataBASE (hydrographic compilation with per-cell contributor, supersession, and uncertainty; the NBS toolchain lineage); QPS Fledermaus/Qimera (surface combination, difference, visualization); Global Mapper (mosaic with feathering; caveat—defaults hide the blend width and resampling); ArcGIS mosaic datasets (priority by attribute, seamline generation, blend; caveat—on-the-fly mosaicking means the "product" can change with the query); Hypack (survey compilation).

## Standards & guides

- NOAA Office of Coast Survey, *National Bathymetric Source / BlueTopo* product documentation and tile specification (current edition): contributor band, RAT, supersession.
- IHO, *B-11 GEBCO Cookbook* (current edition): gridding and compilation practice, TID assignment.
- GEBCO Compilation Group, *GEBCO Grid* documentation (annual): TID definitions and source hierarchy.
- EMODnet Bathymetry Consortium, *EMODnet Digital Bathymetry (DTM) methodology* (current release): source priority and source-reference layer.
- USGS, *3DEP Seamless DEM product specification* and *Lidar Base Specification* 2024 rev. A (or current revision): best-available assembly and quality levels.
- Copernicus DEM *Product Handbook* (Airbus/ESA, current issue): EDM, FLM, HEM, WBM mask definitions.
- NOAA NCEI, *CUDEM* technical documentation and Amante and Eakins (2016) methodology report.
- IHO, *S-44* Ed. 6.1.0 (2022) and *S-102* Ed. 3.0.0 (2024): shoal-biased compilation for navigation; tiling.
- ASPRS, *Positional Accuracy Standards for Digital Geospatial Data* Ed. 2 (2023): accuracy reporting by stratum, applicable to mosaics by source zone.
- ISO 19157-1:2023: data quality elements for lineage and completeness.

## Pitfalls

- **Newest source overriding a better older one (or vice versa) with no stated rule** → "best available" was never defined → write the ordering as explicit criteria with tie-breakers and store its version with the product.
- **Blending a DSM into a DTM at the seam** → surface types were not harmonized → inspect each source's definition; convert or exclude before merging.
- **A feathered bathy–topo transition that invents a beach slope** → the interpolator or feather bridged an unsurveyed intertidal gap → flag interpolated cells in the method layer with distance-dependent uncertainty; never present them as measured.
- **Losing per-source uncertainty** → the composite carries one elevation band → propagate a per-cell uncertainty layer, inflated for datum conversion and interpolation.
- **Vertical datum mismatch of 0.3–1 m between neighbours read as a terrace** → tidal, geoid-model, or local-datum differences unresolved → difference overlaps before merging; measure seams; check survey reports, not just metadata fields.
- **A composite with no date layer used for change detection** → dates were a property of sources, not cells → publish an acquisition-date raster; refuse change analyses without one.
- **Feathering a navigation channel into an older grid** → the blend shoals the dredged depth → switch, do not blend, at channel limits; shoal-biased rules for navigation.
- **Footprints taken as tile rectangles** → nodata fringe and edge extrapolation enter the composite → derive footprints from valid cells, eroded by the gridding search radius.
- **Pooled accuracy statistics** → one RMSE across lidar and legacy zones → stratify by source zone and method class; report areal-weighted summaries only alongside strata.
- **Overwriting a release in place** → users cannot tell what changed → version every build, publish difference and change-reason rasters, keep the manifest.
- **Blending before bias removal** → the feather spreads the offset over the zone → make overlap differences zero-mean first; if the residual step exceeds combined uncertainty, investigate instead of blending.

## Key takeaways

- A composite is a decision, not a measurement; publish the decision—source, date, uncertainty, method rasters and the lineage table—with the surface.
- Prepare before merging: one datum with recorded transformation paths, one surface type, aligned resolution, bias removed over overlaps, defects masked per source.
- Choose the priority rule by use—shoal-biased for navigation, most-recent for change, most-accurate for engineering—and declare it with its version.
- Blend only unbiased, comparable sources across narrow zones away from discontinuities; otherwise switch at a hard, documented seam. Never feather a navigation surface.
- The land–water seam needs one datum via a published model, one shoreline derived from the composite, and honest flagging of interpolated intertidal cells.
- Measure seams: the step is a bias to fix, the spread is an independent check on the uncertainty layer.
- Validate by stratum, never pooled; compare residuals to the per-cell uncertainty.
- Version every build reproducibly and publish what changed since the last release.

## References

- Amante, C. J. (2018). Estimating coastal digital elevation model uncertainty. *Journal of Coastal Research*, 34(6), 1382–1397.
- Amante, C. J., and Eakins, B. W. (2016). Accuracy of interpolated bathymetry in digital elevation models. *Journal of Coastal Research*, Special Issue 76, 123–133.
- Danielson, J. J., and Gesch, D. B. (2011). *Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010)*. U.S. Geological Survey Open-File Report 2011-1073.
- Danielson, J. J., Poppenga, S. K., Brock, J. C., Evans, G. A., Tyler, D. J., Gesch, D. B., Thatcher, C. A., and Barras, J. A. (2016). Topobathymetric elevation model development using a new methodology: Coastal National Elevation Database. *Journal of Coastal Research*, Special Issue 76, 75–89.
- Eakins, B. W., and Grothe, P. R. (2014). Challenges in building coastal digital elevation models. *Journal of Coastal Research*, 30(5), 942–953.
- Gesch, D. B., Verdin, K. L., and Greenlee, S. K. (1999). New land surface digital elevation model covers the Earth. *Eos, Transactions AGU*, 80(6), 69–70. (GTOPO30)
- Marks, K. M., and Smith, W. H. F. (2006). An evaluation of publicly available global bathymetry grids. *Marine Geophysical Researches*, 27(1), 19–34.
- Nuth, C., and Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5(1), 271–290.
- Pe'eri, S., Parrish, C., Azuike, C., Alexander, L., and Armstrong, A. (2014). Satellite remote sensing as a reconnaissance tool for assessing nautical chart adequacy and completeness. *Marine Geodesy*, 37(3), 293–314.
- Pérez, P., Gangnet, M., and Blake, A. (2003). Poisson image editing. *ACM Transactions on Graphics*, 22(3), 313–318.
- Weatherall, P., Marks, K. M., Jakobsson, M., Schmitt, T., Tani, S., Arndt, J. E., Rovere, M., Chayes, D., Ferrini, V., and Wigley, R. (2015). A new digital bathymetric model of the world's oceans. *Earth and Space Science*, 2(8), 331–345.
- Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., and Tian, D. (2019). The Generic Mapping Tools version 6. *Geochemistry, Geophysics, Geosystems*, 20(11), 5556–5564.
- NOAA Office of Coast Survey. *BlueTopo* and *National Bathymetric Source* product documentation (current edition). NOAA, Silver Spring, MD. https://nauticalcharts.noaa.gov/data/bluetopo.html
- Airbus Defence and Space. *Copernicus DEM Product Handbook*, GEO1988-CopernicusDEM-SPE-002, issue 5.0 (current issue). ESA/Airbus.
- EMODnet Bathymetry Consortium (2022). *EMODnet Digital Bathymetry (DTM 2022)*. doi:10.12770/ff3aff8a-cff1-44a3-a2c8-1910bf109f85
- Stoker, J. M., and Miller, B. (2022). The accuracy and consistency of 3D Elevation Program data: A systematic analysis. *Remote Sensing*, 14(4), 940.
- Thatcher, C. A., Brock, J. C., Danielson, J. J., Poppenga, S. K., Gesch, D. B., Palaseanu-Lovejoy, M. E., Barras, J. A., Evans, G. A., and Gibbs, A. E. (2016). Creating a Coastal National Elevation Database (CoNED) for science and conservation applications. *Journal of Coastal Research*, Special Issue 76, 64–74.

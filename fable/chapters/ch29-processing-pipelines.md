# Chapter 29 — Processing pipelines: levels, lineage, and what gets lost

> **Part VII — From sensor data to products.** The opening chapter of the processing part: the generic chain from raw observations to a published surface, what each step throws away, and how to record the chain so that the product can be trusted, reprocessed, and challenged.

**In this chapter.** Every elevation product is the end of a pipeline, and most of its errors were introduced—or made invisible—somewhere along that pipeline rather than at the sensor. You will be able to describe the generic processing levels (raw → trajectory → georeferenced observations → cleaned → classified → surface → derived product → QA → metadata → archive) and map them onto the specific chains used for lidar, multibeam, structure from motion, InSAR, satellite stereo, and satellite-derived bathymetry. You will be able to say what information is irreversibly lost at each step, decide which intermediates to keep, and write a lineage record that a machine can parse (ISO 19115 `LI_Lineage`, W3C PROV). You will know why the same software with the same data gives different grids a year later, how to pin versions, parameters, and seeds, where human editing enters and how large inter-operator variability is, how to build QA gates and regression tests on reference datasets, and what changes when the pipeline runs on a cluster or in the cloud. A complete PDAL/GDAL pipeline with a provenance sidecar is given as a template.

## 29.1 Processing levels: from raw observations to an archived product

NASA's Earth Observing System introduced a vocabulary of **processing levels** that has proven more useful than its original purpose. **Level 0** is reconstructed, unprocessed instrument data at full resolution; **Level 1A** is Level 0 with radiometric and geometric calibration coefficients appended but not applied; **Level 1B** has the calibrations applied; **Level 2** is a derived geophysical variable at the sensor's native sampling; **Level 3** is that variable mapped to a uniform space–time grid; and **Level 4** is a model output or a result of analysis of lower-level data (NASA ESDIS data processing levels; the definitions are published on the Earthdata site and have been stable since the 1990s). The scheme matters because each level boundary is a decision boundary: a place where somebody chose a calibration, a sampling, a filter, or a model, and where the user downstream inherits that choice whether they know it or not.

For elevation data the analogy maps naturally onto a ten-stage chain that this book will use as its reference pipeline:

| Stage | Elevation-data equivalent | Typical artefact |
|---|---|---|
| 0 Raw | Range/time records, waveforms, beam amplitudes, image frames, radar echoes, GNSS/IMU logs | Vendor binary (e.g. `.sdf`, `.all`/`.kmall`, `.rxp`, raw images, L0 SLC) |
| 1 Trajectory | Tightly or loosely coupled GNSS/INS solution; camera poses; satellite ephemeris | SBET, `.pos`, bundle-adjusted cameras, precise orbits |
| 2 Georeferenced observations | Points, soundings, or pixels with coordinates in a named frame and epoch | LAS/LAZ, GSF, per-ping soundings, SLC with geolocation grid |
| 3 Cleaned | Blunders, noise, multiple-time-around returns, sonar fliers removed or flagged | LAS with noise classes / withheld flags; rejected soundings |
| 4 Classified | Semantic labels (ground, building, water, accepted sounding) | LAS classification field; hydrographic feature flags |
| 5 Surface | A continuous model: TIN, grid, CUBE/CHRT node set, mesh | GeoTIFF/COG, BAG, TIN, OBJ |
| 6 Derived product | DTM/DSM/nDSM, slope, contours, hydro-conditioned DEM, chart soundings | Derived rasters and vectors |
| 7 QA | Checkpoints, crosslines, crossover statistics, visual review | Accuracy report, QA log |
| 8 Metadata | Lineage, parameters, CRS, epoch, accuracy statements | ISO 19115/19157 XML, STAC JSON, README |
| 9 Archive | Fixity, versioning, persistent identifiers, access | Repository record, DOI, checksums |

<!-- figure: Figure 29.1 — Ten-stage reference pipeline drawn as a left-to-right flow with, under each stage, the information discarded (e.g. waveform shape, pulse timing, per-point density) and the decisions introduced (e.g. filter thresholds, class rules, interpolator). -->

Three properties of this chain recur throughout the book. First, it is **lossy**: every arrow from left to right discards information that cannot be recovered from the right-hand side (Section 29.3). Second, it is **not linear in practice**: QA at stage 7 routinely sends the project back to stage 1 (a trajectory re-solve after a bad crossover) or stage 4 (a reclassification after a checkpoint fails), and a product with a published lineage shows those loops rather than hiding them. Third, the chain is **rerun more often than it is run**: a national lidar program will reclassify, regrid, and re-datum the same acquisition several times over its life as specifications, geoids, and algorithms change. The design question is therefore not "how do I get from raw to grid once" but "how do I make the trip repeatable and auditable."

> **Definitions that bite.** "Level 2" and "Level 3" mean different things in different communities. In NASA usage Level 3 is gridded; in hydrography, "Level 2" often refers to a NOAA Office of Coast Survey data-quality level, and in the Copernicus and ESA worlds Level 2 commonly means a geophysical product that may already be gridded (Sentinel-2 L2A is an orthorectified bottom-of-atmosphere grid). When a dataset description says "Level 2 point cloud," ask which scheme is meant before assuming anything about what has been done to it.

## 29.2 Sensor-specific pipelines

The reference chain is generic; the stages in which errors are most often introduced are sensor-specific. This section walks each major sensor through the chain, pointing to the deep-dive chapters for the physics.

### 29.2.1 Airborne and mobile lidar

A topographic lidar pipeline ([Chapter 18](ch18-topographic-lidar.md)) begins with three raw streams—laser ranges with scan angles and timestamps, GNSS observables, and IMU increments—plus a mission-specific calibration file. The **trajectory** stage solves a tightly coupled GNSS/INS filter and smoother (forward–backward, so that the solution at any epoch uses future data too), typically against a base station or a network solution, and produces a smoothed best-estimate trajectory (SBET) at 200 Hz or more with a position and attitude covariance. The **georeferencing** stage applies the lidar equation (lever arm, boresight, scanner geometry, range corrections) to produce points in an ellipsoidal frame at the trajectory epoch. **Calibration and strip adjustment** then estimate residual boresight, lever-arm, and per-strip trajectory corrections by minimising surface mismatches in overlaps; strip adjustment moves points, so a point cloud delivered before and after adjustment is not the same dataset. **Cleaning** flags noise and withheld points; **classification** labels ground, vegetation tiers, buildings, water, and bridge decks ([Chapter 30](ch30-point-cloud-classification.md)); **surface** generation interpolates ground points to a DTM and all first returns (or highest returns) to a DSM ([Chapter 31](ch31-interpolation-and-gridding.md), [Chapter 32](ch32-dsm-to-dtm.md)); and the **derived** products—hydro-flattened DEMs, contours, intensity images, building footprints—follow. The datum transformation from ellipsoidal to orthometric height ($H = h - N$) is a stage in its own right, usually applied between georeferencing and classification; which geoid model and which epoch were used is among the most frequently missing items in lidar lineage ([Chapter 9](ch09-vertical-datums.md)).

The places where information silently dies in this pipeline are: full-waveform digitisation reduced to discrete returns (if the system recorded waveforms at all), per-pulse intensity normalised or rescaled without a record of the formula, overlap points flagged and then dropped by a downstream tool that treats the overlap bit as "delete," and the swath-edge cut that removes points with large scan angles without noting the threshold.

### 29.2.2 Multibeam echosounder bathymetry

A multibeam pipeline ([Chapter 20](ch20-sonar.md)) starts from raw datagrams containing per-beam two-way travel times and beam angles, attitude and heave at the motion sensor's rate, position, and, critically, the **sound-velocity profile (SVP)** casts taken during the survey. The ray-tracing step converts travel time and angle into a depth and across-track distance by integrating through the SVP; an error of 1 m/s in the profile or a profile applied at the wrong time produces the characteristic "smile" or "frown" across the swath that grows with beam angle. The reduction to a vertical datum applies tides (from gauges, zoned predictions, or a model) or **ellipsoidally referenced surveying (ERS)**, in which GNSS heights replace tide observations and a separation model (e.g. NOAA VDatum) relates the ellipsoid to chart datum. Cleaning rejects fliers and blunders—manually in swath editors or automatically by statistical filtering—and the surface is estimated by **CUBE** (Combined Uncertainty and Bathymetry Estimator; Calder & Mayer 2003) or its variable-resolution successor **CHRT** (Calder & Rice 2017), which maintain multiple depth hypotheses at each node weighted by the propagated uncertainty of each sounding. The output is normally a BAG file carrying depth and uncertainty layers ([Chapter 47](ch47-file-formats.md)), from which charted soundings are selected shoal-biased. NOAA's Hydrographic Surveys Specifications and Deliverables (HSSD) and the Field Procedures Manual prescribe which intermediates must be delivered: raw data, processed data with all corrections applied, the SVP casts, tide files or ERS separation surfaces, the CUBE surfaces, and the Descriptive Report that narrates the processing (NOAA OCS 2024 editions; check the current year's edition for exact deliverable lists).

Loss points: the backscatter and water-column data, often not retained; the record of which SVP applied to which ping; the rejected soundings (a hydrographer who deletes rather than flags has made the dataset unauditable); and the hypothesis set at each CUBE node, which is discarded when the surface is finalised.

### 29.2.3 Structure from motion and photogrammetry

Image-based pipelines ([Chapter 22](ch22-photogrammetry-sfm.md)) begin with image frames and, optionally, camera positions from GNSS and ground control points. **Alignment** detects and matches features, estimates relative camera poses, and produces a sparse cloud; **bundle adjustment (BA)** refines poses, interior orientation (focal length, principal point, distortion), and tie-point coordinates together, with control points or precise camera positions providing the datum. **Dense matching** produces the dense cloud; a **mesh** or a direct DSM follows; an **orthomosaic** is projected onto the DSM. The stages that most often damage the product are BA with self-calibrated interior orientation and weak geometry (the "doming" systematic error of parallel-strip nadir surveys, with magnitudes of decimetres over hundreds of metres in the literature) and the dense-matching confidence filter, whose threshold determines whether vegetation and water appear as surface or as holes. SfM software typically does not export the covariance of the adjusted parameters; the user gets a reprojection error in pixels and must infer object-space uncertainty from checkpoints.

### 29.2.4 InSAR and satellite stereo

An InSAR DEM pipeline ([Chapter 21](ch21-radar-sar-insar.md)) coregisters two single-look-complex (SLC) images to sub-pixel precision, forms the interferogram, removes the flat-Earth and (optionally) a reference-topography phase, filters, **unwraps** the phase from modulo-$2\pi$ to continuous, converts unwrapped phase to height through the baseline geometry, and geocodes from radar to map coordinates. Unwrapping is the single step at which a DEM can acquire whole-ambiguity errors (one height-of-ambiguity per cycle, tens of metres for TanDEM-X depending on baseline); the resulting "phase-unwrapping errors" are flagged in TanDEM-X and Copernicus DEM auxiliary layers but cannot be repaired from the final grid. Satellite stereo (ASTER, SPOT, Pléiades, WorldView; [Chapter 22](ch22-photogrammetry-sfm.md)) follows the photogrammetric chain with rational polynomial coefficient (RPC) sensor models, bias-corrected against control or against an existing DEM, and with a stereo-matching step whose correlation window sets the effective resolution of the result.

### 29.2.5 Satellite-derived bathymetry

Optical SDB ([Chapter 23](ch23-satellite-derived-bathymetry.md)) adds atmospheric correction, sun-glint and water-column handling, and an empirical or physics-based inversion calibrated against soundings. Its pipeline is unusual in that the dominant uncertainty is in the **model** stage rather than in geolocation: the same imagery with a different training set of soundings yields a different depth surface, and the lineage must record the training soundings, their datum, and their date.

## 29.3 Information lost at each step, and when to keep intermediates

Processing is compression with a purpose. The useful question is not whether information is lost—it always is—but whether what is lost could be needed later and whether it can be reconstructed. Consider a lidar pipeline from the most information-rich artefact to the least:

**Full waveform → discrete returns.** A digitised waveform at 1 GHz holds the shape of every echo: its width (a proxy for footprint-scale roughness or slope), its amplitude, and weak late returns from the ground under dense canopy that a real-time discriminator would miss. Reduction to discrete returns keeps three to five ranges and intensities per pulse. Re-detecting returns with a better algorithm—or a lower threshold under canopy—is only possible if the waveforms were kept. Waveform storage is 10–50 times the volume of discrete points, which is why most programs discard it, and why re-detection studies are rare.

**Discrete returns → classified points.** Classification adds information (labels) but a downstream step often removes points: noise-class points are dropped, overlap points removed, "withheld" points stripped. Each removal destroys the ability to re-run classification with different rules. The USGS Lidar Base Specification requires delivery of the all-return classified point cloud precisely so that the ground decision can be revisited ([Chapter 30](ch30-point-cloud-classification.md)).

**Classified points → grid.** Gridding is the largest single loss. A 1 m DTM from an 8 pt/m² cloud discards the positions of seven of every eight points and all the vertical scatter within a cell; it fixes an interpolator, a cell semantics (centre sample or area mean), a registration, and a nodata policy ([Chapter 31](ch31-interpolation-and-gridding.md)). Nothing in the grid records how many points supported each cell or how far the nearest ground point was—unless the pipeline writes count and distance layers alongside.

**Grid → overviews and derived products.** Pyramids computed by averaging remove local maxima; slope rasters lose the elevation offset; contours lose everything between the contour interval; and a hillshade loses almost everything quantitative.

> **Rule of thumb.** Keep any intermediate whose regeneration costs more than its storage, and any intermediate that embodies a human decision. Trajectories (small), calibration reports (small), classified point clouds (large but irreplaceable), and rejected-sounding flags (small) always qualify. Dense SfM clouds and intermediate grids usually do not, provided the parameters that produced them are recorded and the software is pinned. Full waveforms are the hard case: expensive to keep, impossible to recreate.

Bathymetry has its own version of the ladder. The CUBE surface is a sufficient statistic for the chart only if the hypothesis strengths and the per-node sounding counts are retained; a BAG with depth and uncertainty layers but without the underlying soundings cannot be re-cleaned when a shoal is questioned. NOAA's practice of archiving raw and processed soundings at NCEI alongside the surfaces exists precisely for this reason.

The decision of what to keep should be made explicitly at the project outset, written in the data-management plan, and reflected in the lineage: a record that says "waveforms discarded at stage 0→2, overlap points retained, noise points retained with class 7" tells a future user what reprocessing is possible.

## 29.4 Reproducibility: versions, parameters, containers, seeds, and lineage records

A pipeline is reproducible when a second party, given the raw data and the lineage record, obtains the same product to within a stated tolerance. That is a stricter standard than most elevation projects meet, and the failures are rarely exotic. The common ones are:

- **Software version drift.** The default parameters of a filter change between releases. PDAL's `filters.smrf` and `filters.pmf`, LAStools' `lasground`, and TerraScan's ground routine have all had defaults or internal behaviour change over their lifetimes; GDAL's resampling kernels and nodata handling have changed in minor releases. A lineage record that says "classified with PDAL" without a version number does not allow a rerun.
- **Unrecorded parameters.** A strip adjustment's weighting scheme, a CUBE configuration (capture distance, hypothesis-selection method), a geoid model name and version, a sound-velocity application mode. Each of these changes the product by more than its stated accuracy.
- **Hidden state.** Environment variables (`GDAL_NUM_THREADS`, `PROJ_NETWORK`, the PROJ grid directory contents), the availability of a geoid grid or a time-dependent transformation file, the locale that controls decimal parsing.
- **Nondeterminism.** Multi-threaded reductions that sum in different orders, random subsampling in SfM alignment or in machine-learning classifiers, cloth simulation with random initialisation, and Monte Carlo uncertainty estimates. A seed is a parameter and must be recorded; where the library does not expose a seed, the lineage must say so and the tolerance must absorb the spread.

The practical remedies are now well established. **Pin everything**: software versions (conda `environment.yml` or lockfile, `pip freeze`, `R sessionInfo()`), the PROJ and GDAL data directories with their checksums, and the geoid/transformation grids by name and version. **Containerise** the pipeline (Docker, Apptainer) so that the operating system libraries travel with it; a container image digest is a single string that identifies the whole execution environment. **Externalise parameters** into a configuration file that is committed alongside the pipeline and copied into the product's metadata. **Make the pipeline a program**, not a sequence of GUI clicks—PDAL JSON pipelines, GMT and GDAL shell scripts, MB-System `mbprocess` parameter files, and Python notebooks with pinned kernels are all acceptable; a screen recording is not. **Record run metadata** automatically: start and end times, host, container digest, input checksums, output checksums.

Two formal vocabularies exist for recording lineage. **ISO 19115-1** (2014, with amendments) defines `LI_Lineage` with a free-text `statement` and a list of `LI_ProcessStep` elements, each with a description, a date, a processor, and references to `LI_Source` inputs; ISO 19115-2 extends it with `LE_Processing` for algorithm and software identification and `LE_ProcessStepReport`. **W3C PROV** (PROV-O, PROV-DM, 2013) is a general-purpose provenance model built around three classes—*Entity* (a dataset or file), *Activity* (a process step), and *Agent* (a person, organisation, or software)—and a small set of relations (`wasGeneratedBy`, `used`, `wasAttributedTo`, `wasDerivedFrom`, `wasAssociatedWith`). PROV can be serialised as JSON-LD or Turtle, queried with SPARQL, and nested, which makes it a better fit for machine processing than the ISO structure; many projects now write PROV and generate an ISO lineage summary from it. The STAC `processing` extension carries lightweight equivalents (`processing:software`, `processing:lineage`, `processing:level`) for catalogue items ([Chapter 51](ch51-finding-data.md)). What matters more than the choice of vocabulary is that the record is **generated by the pipeline**, not typed by a person afterward, and that it is **retrievable alongside the product** ([Chapter 49](ch49-metadata.md), [Chapter 50](ch50-archiving-and-provenance.md)).

> **Try it.** A PDAL pipeline that takes a LAZ tile from georeferenced points to a ground-classified cloud and a 1 m DTM, with the pipeline file itself and the software versions written into a provenance sidecar. Expected outcome: `tile_dtm.tif` (1 m, `float32`, nodata −9999), `tile_ground.laz`, and `tile_dtm.prov.json` recording PDAL and GDAL versions, the pipeline, and input/output checksums.
>
> ```json
> {
>   "pipeline": [
>     {"type": "readers.las", "filename": "tile.laz",
>      "override_srs": "EPSG:6339+5703"},
>     {"type": "filters.assign", "value": "Classification = 0"},
>     {"type": "filters.elm", "cell": 10.0, "threshold": 1.0},
>     {"type": "filters.outlier", "method": "statistical",
>      "mean_k": 8, "multiplier": 2.5},
>     {"type": "filters.smrf", "ignore": "Classification[7:7]",
>      "cell": 1.0, "slope": 0.15, "window": 18.0,
>      "threshold": 0.5, "scalar": 1.25},
>     {"type": "writers.las", "filename": "tile_ground.laz",
>      "minor_version": 4, "dataformat_id": 6, "forward": "all"},
>     {"type": "filters.range", "limits": "Classification[2:2]"},
>     {"type": "writers.gdal", "filename": "tile_dtm.tif",
>      "resolution": 1.0, "output_type": "idw", "radius": 1.5,
>      "window_size": 3, "nodata": -9999, "data_type": "float32",
>      "gdalopts": "COMPRESS=DEFLATE,PREDICTOR=3,TILED=YES"}
>   ]
> }
> ```
>
> ```bash
> #!/usr/bin/env bash
> set -euo pipefail
> P=dtm_pipeline.json
> pdal pipeline "$P" --metadata tile_dtm.pdal-metadata.json
> python3 - <<'EOF'
> import json, hashlib, subprocess, datetime, platform
> def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
> prov = {
>   "@context": "https://www.w3.org/ns/prov",
>   "activity": {"id": "urn:dtm:tile:run:" + datetime.datetime.utcnow().isoformat(),
>                "type": "prov:Activity",
>                "pdal_version": subprocess.check_output(["pdal","--version"]).decode().strip(),
>                "gdal_version": subprocess.check_output(["gdalinfo","--version"]).decode().strip(),
>                "host": platform.platform(),
>                "pipeline": json.load(open("dtm_pipeline.json"))},
>   "used": [{"id": "tile.laz", "sha256": sha("tile.laz")}],
>   "generated": [{"id": f, "sha256": sha(f)} for f in ("tile_ground.laz","tile_dtm.tif")]
> }
> json.dump(prov, open("tile_dtm.prov.json","w"), indent=1)
> EOF
> gdal_edit.py -mo "LINEAGE=see tile_dtm.prov.json" tile_dtm.tif
> ```
>
> The `--metadata` flag makes PDAL emit the effective parameters of every stage, including defaults the pipeline did not set—this is the record that catches silent default changes between versions. The SMRF parameters shown are starting points for gentle, mixed terrain; see [Chapter 30](ch30-point-cloud-classification.md) for tuning.

## 29.5 Human-in-the-loop steps

No production elevation pipeline is fully automatic. Hydrographers review CUBE surfaces and override hypotheses; lidar technicians reclassify bridge decks, correct false ground on levees, and digitise hydro-flattening breaklines; photogrammetrists mask water and edit meshes. These steps are where expertise enters and also where reproducibility and consistency leave.

The size of the effect has been measured in a few places. In the ISPRS ground-filter comparison (Sithole & Vosselman 2004) the reference classification itself was produced by manual editing and the authors note residual ambiguity in the reference; subsequent studies that had several operators classify the same tile report disagreement rates of a few percent of points overall and much higher in low vegetation, at building edges, and on terraces—regions where "ground" is a judgement rather than a measurement. In hydrography, "over-cleaning" (removing real seafloor features as noise) is a recognised failure mode, serious enough that NOAA's guidance and the CUBE design philosophy explicitly favour flagging over deletion and require the surface, not the cleaned soundings, to be the product of record (Calder & Mayer 2003). Multi-analyst studies of volcanic and geomorphic change mapping report that operator choice of masking and co-registration parameters changes volume estimates by amounts comparable to the stated uncertainty.

The practical consequences for pipeline design are three. Manual edits should be stored as **operations** (a polygon plus a rule: "reclassify class 2 to class 17 inside this polygon"), not as modified copies of the data, so that they can be replayed on reprocessed inputs. Each operation should carry the operator, the timestamp, and the reason. And QA sampling should be designed to measure inter-operator variability—two operators on the same 1 % of tiles—so that the human component of the uncertainty budget is a number rather than an assumption ([Chapter 53](ch53-accuracy-assessment.md)).

> **Case file.** The classic illustration of unrecorded human editing is the SRTM "finished" product. NGA's editing of the research-grade SRTM data flattened water bodies, set shorelines to constant elevations, and removed spikes and wells by rules that were documented in general terms (Slater et al. 2006) but not point by point; the result was that users comparing SRTM versions (SRTMGL1 v3 vs. the unedited v2.1, or NASADEM) found differences concentrated along coastlines and lakes that were decisions, not measurement changes. The lesson is not that the editing was wrong—it was needed—but that a product whose edits are not expressed as a replayable layer cannot be compared with its own earlier versions.

## 29.6 Automation and QA gates; regression tests on reference datasets

Treat the pipeline as software, and its quality control as testing. Three kinds of tests matter.

**Unit tests on stages.** Each stage has invariants that can be asserted automatically: the point count after noise filtering falls within an expected fraction of the input; the trajectory covariance never exceeds a threshold; every output grid has a CRS with a vertical component and an epoch tag; nodata is identical in the raster header and the metadata; the geoid model named in the lineage is the one whose checksum was loaded. These are cheap and catch the configuration errors that account for most datum disasters.

**QA gates between stages.** A gate is a quantitative acceptance criterion that must pass before the pipeline continues. The USGS Lidar Base Specification supplies several that are easy to encode: intra-swath and inter-swath relative accuracy (RMSDz of overlap differences on hard surfaces), aggregate nominal pulse spacing, spatial distribution (percentage of 2 × NPS cells that contain at least one point), and the non-vegetated vertical accuracy (NVA) at checkpoints after classification ([Chapter 18](ch18-topographic-lidar.md), [Chapter 53](ch53-accuracy-assessment.md)). For multibeam, crossline comparisons against main-scheme lines and the IHO S-44 order's total vertical uncertainty (TVU) at 95 % act as gates ([Chapter 20](ch20-sonar.md)). The gate records its own result in the lineage, so a product carries the evidence that it passed.

**Regression tests on reference datasets.** Keep a small, fixed set of reference tiles with known answers—an ISPRS or OpenGF ground-truth tile, a multibeam patch over a flat, well-surveyed area, a tile with a bridge, one with a levee, one with closed canopy—and run the full pipeline on them with every software or parameter change. Compare the outputs against the previous run: per-class confusion matrices, DTM difference statistics, the elevation at a dozen named checkpoints. A change that moves the levee crest by 20 cm or converts a bridge deck to ground should fail the build, exactly as a unit-test failure fails a software build. Appendix H lists suitable public datasets ([Appendix H](../appendices/appendix-h-datasets.md)).

> **Worked example.** A regression gate for a DTM pipeline. The reference tile has 11,520 surveyed checkpoints on non-vegetated ground. The previous pipeline version gave RMSE$_z$ = 0.072 m, mean error = +0.011 m. A new SMRF version is proposed. Running it on the reference tile gives RMSE$_z$ = 0.075 m, mean = +0.009 m: within the gate's tolerance (RMSE change < 10 %, mean change < 0.02 m). But the per-land-cover breakdown shows that on the levee sub-sample (n = 410) the mean error went from −0.04 m to −0.19 m, because the new window parameter removed the crest. The aggregate passed; the stratified test failed. The gate must be stratified by terrain and land-cover class or it will pass changes that break the product for the users who care most.

## 29.7 Cloud-native and distributed processing

Elevation data volumes—a state-wide QL1 lidar collection is tens of terabytes of LAZ; a global 30 m DEM is a few hundred gigabytes; a decade of ICESat-2 ATL03 photons is petabytes—have pushed processing toward systems that move computation to data rather than data to computation.

**Google Earth Engine** ⟨H⟩ (Gorelick et al. 2017) made planetary-scale raster analysis available to non-specialists by holding public catalogues (SRTM, ALOS, Copernicus DEM, GEDI rasters) in a tiled, pyramided store and executing lazily evaluated expressions server-side; its model of on-the-fly reprojection and pyramid-level selection is powerful and also a lineage trap, because the pyramid level at which a computation ran depends on the output scale the user asked for, and the resampling is not always what the user assumed (Section 31.7). **Pangeo** and **Dask** bring the same lazy, chunked model to open Python: xarray over Zarr or COG stores, with Dask scheduling chunked computations across a cluster; `rioxarray`, `xdem`, and `odc-geo` handle georeferencing. **PDAL pipelines** parallelise naturally over tiles, and the COPC and Entwine formats ([Chapter 47](ch47-file-formats.md)) allow spatially indexed partial reads of point clouds from object storage, so that a classification or a DTM can be computed for a bounding box without downloading the collection. **Apache Spark** with **Sedona** (formerly GeoSpark) or **RasterFrames** serves organisations already running Spark; **GeoTrellis** and **Kubernetes-orchestrated PDAL** are used by several national mapping agencies.

Distributed execution adds its own reproducibility hazards. Tile edges require buffered reads and consistent handling so that filters do not create seams; floating-point reductions across partitions can be non-associative; the versions of libraries on worker nodes may differ from the driver; and dynamically chosen chunk sizes change the behaviour of neighbourhood operations. The remedy is the same as in Section 29.4—pin, containerise, record—plus explicit tests that a tile processed alone matches the same tile processed within a mosaic to within floating-point noise.

<!-- figure: Figure 29.2 — Distributed PDAL/GDAL workflow: COPC point clouds in object storage, a tile index, parallel workers each running the same pinned container, buffered tile processing with seam checks, and a provenance record emitted per tile and aggregated per product. -->

## Then & now

- **1970s–1980s.** Processing chains were bespoke, batch, and poorly recorded; stereo-plotter DEMs and early echosounder soundings were reduced by hand, and the "pipeline" existed in an operator's notebook. The NASA EOS processing-level vocabulary (defined for the EOS Data and Information System in the late 1980s and early 1990s) gave data producers a shared language for how processed a product was.
- **1990s.** GPS/INS direct georeferencing turned lidar and digital photogrammetry into trajectory-first pipelines; the SBET became the central intermediate. SRTM (2000) was processed centrally at JPL and edited at NGA, with the editing rules documented only in summary.
- **2003.** CUBE (Calder & Mayer 2003) changed hydrographic processing from "clean the soundings, then grid" to "estimate the surface with uncertainty, then review the hypotheses"—a shift from editing data to editing a model.
- **2007–2012.** ⟨H⟩ Google Earth Engine was developed from 2008 and publicly introduced in December 2010; it demonstrated server-side processing of global archives and became a standard platform for DEM-based analysis (Gorelick et al. 2017).
- **2011–2016.** PDAL (first releases around 2011, 1.0 in 2015; Butler et al. 2021) and the JSON pipeline model made point-cloud processing scriptable and reproducible in open source; LAS 1.4 (2011) formalised the classification and flag fields that pipelines depend on.
- **2016.** The FAIR principles (Wilkinson et al. 2016) gave data managers a vocabulary—findable, accessible, interoperable, reusable—that explicitly includes provenance (R1.2).
- **2019–present.** Cloud-optimized GeoTIFF, COPC (2021), STAC (1.0 in 2021), and Zarr made cloud-native elevation stores common; national programs (USGS 3DEP, Environment Agency, AHN, swisstopo) now publish point clouds and grids in these forms, and lineage increasingly travels as STAC JSON rather than as a PDF.

## Validation & uncertainty

The pipeline view changes what "validation" means. A checkpoint comparison at the end tells you the total error of the product at the checkpoints; it does not tell you which stage introduced it, whether it is representative away from the checkpoints, or whether a rerun would reproduce it. A validation plan for a pipeline therefore has three layers.

**Stage-wise error budgets.** Each stage contributes an error with a characteristic spatial structure, and the structures differ enough that they can often be separated. Trajectory errors are smooth along track and correlated over hundreds of metres to kilometres; boresight errors grow with scan angle and change sign between opposing flight lines; SVP errors in multibeam curve the swath; classification errors are local and land-cover dependent; interpolation errors scale with point spacing and curvature; datum errors are constant or long-wavelength. A validation plan that only computes a global RMSE throws this structure away.

> **Uncertainty budget.** Representative 1σ vertical contributions for an airborne lidar DTM pipeline over mixed terrain at 1,000–1,500 m AGL, with the stage that controls each and the test that isolates it. Magnitudes are typical ranges from the sources cited in [Chapter 18](ch18-topographic-lidar.md) and the USGS LBS; a specific project must measure its own.
>
> | Stage | Component | Typical 1σ | Isolating test |
> |---|---|---|---|
> | 1 Trajectory | GNSS/INS height, post-processed | 3–8 cm | Base-station baseline length, PDOP time series, forward/backward separation |
> | 1–2 Calibration | Boresight/lever arm residual | 2–5 cm at swath edge | Inter-swath RMSDz on hard flat surfaces vs. scan angle |
> | 2 Range | Range noise, hard target | 1–3 cm | Intra-swath roughness on flat pavement |
> | 2 Datum | Geoid model (h → H) | 2–5 cm (regional geoids), larger in mountains | Independent levelled benchmarks |
> | 3–4 Classification | Ground misclassification in low vegetation | 5–30 cm, biased positive | VVA at vegetated checkpoints vs. NVA |
> | 5 Gridding | Interpolation at 1 m from ~8 pt/m² | 1–5 cm on smooth ground; 10–50 cm at breaklines | Leave-one-out against withheld ground points |
> | 7 QA | Checkpoint survey itself | 1–3 cm (RTK) or < 1 cm (levelled) | Independent re-survey of a subset |
>
> Combined in quadrature the non-vegetated budget is roughly 5–12 cm 1σ, which is why QL1/QL2 NVA requirements of 10 cm RMSE$_z$ (19.6 cm at 95 %) are achievable but not trivially so, and why the vegetated budget is dominated by a single stage—classification—whose error is not Gaussian and must be reported separately.

**Propagation across stages.** Where errors are independent and approximately Gaussian, variances add: $\sigma_{\text{total}}^2 = \sum_i \sigma_i^2$. Two qualifications matter in practice. First, stages are not independent: a trajectory error moves the whole strip, so it correlates every point's error within the strip, and the effective sample size of a checkpoint set drawn from one strip is far smaller than its count. Second, several stages introduce **biases**, not scatter—vegetation-induced positive bias in a DTM, the shoal bias of minimum binning, the smoothing bias of a spline in concave terrain—and biases add linearly, not in quadrature. Report the mean error and the RMSE separately at every stage where a bias is plausible ([Chapter 5](ch05-error-and-uncertainty.md)).

**Reproducibility tests.** The third layer validates the pipeline rather than the product: rerun the same inputs under the recorded lineage and difference the outputs. A deterministic pipeline should reproduce to floating-point precision (differences of order $10^{-6}$ m on `float32` grids); a stochastic one should reproduce within a documented tolerance, and that tolerance belongs in the uncertainty statement. Record the result of the reproducibility test as a QA item in the lineage. Where the pipeline cannot be rerun—closed software whose version is no longer available, a geoid grid that has been withdrawn—say so in the metadata; a product whose pipeline cannot be rerun is less trustworthy than one whose pipeline can, even when their checkpoint statistics are identical.

What to report, at minimum, in the product's validation statement: the lineage record (or a pointer to it), the stage at which the vertical datum was applied and with which model, the QA gates passed with their values, the checkpoint statistics stratified by land cover and terrain, the human-editing operations applied and their extent, and the reproducibility result.

## Software

**Open source:** PDAL (JSON pipelines, `--metadata` for effective parameters; the de facto open standard for point-cloud processing chains; caveat: filter defaults have changed across versions, so pin the version); GDAL (gridding, warping, overviews, metadata editing; caveat: resampling defaults—nearest for `gdalwarp`—are easy to leave unexamined); MB-System (`mbpreprocess`, `mbprocess`, `mbgrid` with per-file parameter files that act as lineage; caveat: parameter files must be archived with the data); Kluster (open Python multibeam processing with Dask, by NOAA developers; caveat: still maturing); OpenDroneMap (end-to-end SfM pipeline with stored settings; caveat: GPU and version variability affect results); NASA Ames Stereo Pipeline (satellite and planetary stereo, deterministic and scriptable); ISCE2/ISCE3 (InSAR processing from SLC to geocoded unwrapped phase); xarray/Dask/Pangeo stack and xdem (grid analysis with reproducible Python environments).

**Free but closed:** Google Earth Engine (planetary-scale raster processing; caveat: pyramid-level and reprojection behaviour must be understood for quantitative work, and processing cannot be exported as a standalone container); POSPac trial/academic licences; vendor "lite" tools shipped with sensors.

**Commercial:** Applanix POSPac and NovAtel Inertial Explorer (GNSS/INS trajectory processing; the trajectory report is a key lineage document); TerraSolid TerraScan/TerraMatch (lidar classification and strip adjustment; macros are a form of pipeline record); CARIS HIPS & SIPS and QPS Qimera (hydrographic processing with CUBE/CHRT; both maintain processing logs that should be exported with the deliverable); Agisoft Metashape (SfM; the project file and report record parameters, but not the random seeds); Hexagon/Leica HxMap, RIEGL RiPROCESS (sensor-specific chains). The caveat shared by all closed suites is that the pipeline cannot be rerun without a licence for the exact version; the lineage record should therefore be rich enough that an open-source approximation can be built if needed.

## Standards & guides

- **ISO 19115-1:2014** (with Amd 1:2018, Amd 2:2020) — Geographic information — Metadata — Fundamentals; defines `LI_Lineage`, `LI_ProcessStep`, `LI_Source`. **ISO 19115-2:2019** adds `LE_Processing` and `LE_Algorithm` for imagery and gridded data.
- **ISO 19157-1:2023** — Data quality; the structure for reporting positional accuracy and completeness that a pipeline's QA gates feed.
- **W3C PROV** (PROV-DM, PROV-O, PROV-N; Recommendations of April 2013) — general provenance model; recommended serialisation for machine-readable lineage.
- **FAIR Guiding Principles** (Wilkinson et al. 2016) — Findable, Accessible, Interoperable, Reusable; R1.2 requires detailed provenance.
- **NOAA Office of Coast Survey, Hydrographic Surveys Specifications and Deliverables (HSSD)**, annual editions — lists required processing deliverables (raw and processed data, SVP, tides/ERS, surfaces, Descriptive Report). **NOAA Field Procedures Manual (FPM)** — processing chapter describes the operational chain.
- **USGS Lidar Base Specification** (current online edition; 2024 revision) — deliverables (classified point cloud, DEM, breaklines, metadata, QA reports) and the required metadata content including processing description.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)** — defines NVA/VVA and the accuracy reporting that pipeline QA gates target.
- **OGC/STAC processing extension** (community extension) — `processing:lineage`, `processing:software`, `processing:level` fields for catalogue items.
- **IHO S-44 Edition 6.1.0 (2022)** — TVU/THU requirements that function as hydrographic QA gates.

## Pitfalls

- **Overwriting raw data with "corrected" data.** It happens because storage is finite and the corrected file "is better"; it destroys the ability to reprocess. Detect by checking whether the archive holds anything the current software cannot regenerate; avoid by making raw storage a budgeted deliverable.
- **Parameter defaults silently different between software versions.** Filters evolve; a pipeline that relies on defaults reproduces differently. Detect by emitting effective parameters (`pdal pipeline --metadata`) and diffing them between runs; avoid by setting every parameter explicitly.
- **Lineage recorded as a PDF nobody can parse.** Human-readable reports satisfy a contract and defeat automation. Detect by asking whether a script can find the geoid model name; avoid by generating ISO/PROV/STAC records from the pipeline and attaching the PDF as a supplement.
- **Publishing only the final grid.** The grid cannot be reclassified, re-datumed, or re-gridded. Detect by checking whether the classified point cloud or the soundings are archived; avoid by making intermediates part of the deliverable.
- **The vertical datum applied twice or not at all.** A geoid correction applied in the trajectory software and again in the gridding tool, or assumed applied and never run. Detect with a benchmark comparison; avoid by recording the datum stage explicitly in the lineage and checking a benchmark at every gate.
- **Treating the overlap or withheld flag as "delete."** Downstream tools differ; points vanish. Detect by comparing point counts across stages; avoid by filtering explicitly with `filters.range` and recording the rule.
- **Trusting aggregate QA.** A tile-level RMSE passes while levees, bridges, or marshes fail. Detect by stratifying QA by land cover and feature type; avoid by designing stratified gates.
- **Nondeterministic steps without recorded seeds.** SfM alignment, ML classifiers, Monte Carlo uncertainty. Detect by rerunning and differencing; avoid by seeding where possible and documenting tolerance where not.
- **Tile-edge seams in distributed runs.** Neighbourhood filters without buffered reads produce discontinuities at tile boundaries. Detect with a hillshade of the mosaic and a seam-difference test; avoid with buffers of at least the largest filter window.
- **Pyramid-level computation in server-side platforms.** A quantitative statistic computed at an output scale coarser than the native grid silently uses an aggregated pyramid level. Detect by comparing with a native-resolution computation; avoid by setting the scale explicitly and understanding the aggregation.
- **Manual edits as modified copies.** Edited files cannot be replayed on reprocessed inputs, and the edits cannot be audited. Avoid by storing edits as operations with operator, time, and reason.
- **Assuming the pipeline is the same as last year's.** Staff change, software updates, and configuration drift. Detect with regression tests on fixed reference tiles; avoid by running them on every change.

## Key takeaways

- Keep the raw data. Everything downstream can be regenerated from it; nothing upstream can be regenerated from a grid.
- Record every step in a machine-readable lineage generated by the pipeline itself: software versions, effective parameters, input and output checksums, datum stage, seeds.
- Expose intermediates—trajectories, classified point clouds, rejected-sounding flags, CUBE hypotheses—as deliverables; reprocessing is the normal lifecycle of elevation data, not an exception.
- Understand what each stage discards; the largest losses (waveform → returns, points → grid) are the ones users most often wish they could undo.
- Treat human edits as replayable operations with authorship, and measure inter-operator variability as part of the uncertainty budget.
- Build stratified QA gates and regression tests on reference tiles; aggregate statistics pass changes that break the product for specific users.
- Pin and containerise; a container digest plus a configuration file is the shortest complete description of an execution environment.
- Distributed and cloud-native processing changes the engineering, not the obligations: buffered tiles, seam tests, and per-tile provenance.

## References

- Butler, H., Chambers, B., Hartzell, P., & Glennie, C. (2021). PDAL: An open source library for the processing and analysis of point clouds. *Computers & Geosciences*, 148, 104680.
- Calder, B. R., & Mayer, L. A. (2003). Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems*, 4(6), 1048.
- Calder, B. R., & Rice, G. (2017). Computationally efficient variable resolution depth estimation. *Computers & Geosciences*, 106, 49–59.
- Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., & Moore, R. (2017). Google Earth Engine: Planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202, 18–27.
- Wilkinson, M. D., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*, 3, 160018.
- Slater, J. A., Garvey, G., Johnston, C., Haase, J., Heady, B., Kroenung, G., & Little, J. (2006). The SRTM data "finishing" process and products. *Photogrammetric Engineering & Remote Sensing*, 72(3), 237–247.
- Sithole, G., & Vosselman, G. (2004). Experimental comparison of filter algorithms for bare-Earth extraction from airborne laser scanning point clouds. *ISPRS Journal of Photogrammetry and Remote Sensing*, 59(1–2), 85–101.
- Moreau, L., & Groth, P. (2013). *Provenance: An Introduction to PROV*. Morgan & Claypool.
- W3C (2013). PROV-DM: The PROV Data Model. W3C Recommendation, 30 April 2013.
- ISO (2014). ISO 19115-1:2014 Geographic information — Metadata — Part 1: Fundamentals. International Organization for Standardization.
- ISO (2019). ISO 19115-2:2019 Geographic information — Metadata — Part 2: Extensions for acquisition and processing. International Organization for Standardization.
- NOAA Office of Coast Survey (2024). *Hydrographic Surveys Specifications and Deliverables*. National Oceanic and Atmospheric Administration.
- NOAA Office of Coast Survey (current edition). *Field Procedures Manual*. National Oceanic and Atmospheric Administration. (verify)
- U.S. Geological Survey (2024). *Lidar Base Specification*, online edition. USGS National Geospatial Program.
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2. American Society for Photogrammetry and Remote Sensing.
- Hare, R., Eakins, B., & Amante, C. (2011). Modelling bathymetric uncertainty. *International Hydrographic Review*, No. 6 (November 2011), 31–42.
- NASA Earth Science Data Systems. *Data Processing Levels*. NASA Earthdata (web page; definitions of Levels 0–4).
- Rocklin, M. (2015). Dask: Parallel computation with blocked algorithms and task scheduling. *Proceedings of the 14th Python in Science Conference*, 126–132.
- Abernathey, R. P., et al. (2021). Cloud-native repositories for big scientific data. *Computing in Science & Engineering*, 23(2), 26–35.
- Yu, J., Zhang, Z., & Sarwat, M. (2019). Spatial data management in Apache Spark: the GeoSpark perspective and beyond. *GeoInformatica*, 23, 37–78.
- Shean, D. E., Alexandrov, O., Moratto, Z. M., Smith, B. E., Joughin, I. R., Porter, C., & Morin, P. (2016). An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very-high-resolution commercial stereo satellite imagery. *ISPRS Journal of Photogrammetry and Remote Sensing*, 116, 101–117.
- Rosen, P. A., Gurrola, E., Sacco, G. F., & Zebker, H. (2012). The InSAR Scientific Computing Environment. *Proceedings of EUSAR 2012*, 730–733.

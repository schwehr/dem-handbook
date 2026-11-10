# Chapter 49 — Metadata

> **Part X — Representing, storing, finding, and keeping elevation data.** This chapter sits between the formats that carry elevation data ([Chapter 47](ch47-file-formats.md)) and the archives and catalogs that keep and expose it ([Chapter 50](ch50-archiving-and-provenance.md), [Chapter 51](ch51-finding-data.md)); it specifies what must travel with the numbers for them to be used correctly.

**In this chapter.** Metadata is the only defence a downstream user has against misusing your elevation data, and the only evidence you will have, years later, of what you actually did. This chapter defines a minimum metadata set for DEMs, point clouds, and bathymetric surfaces—CRS with geoid and epoch, surface type with inclusions and exclusions, acquisition dates, sensor and method, lineage, resolution, accuracy with its evidence, voids and masks, licence, identifier, version—and maps that set onto the standards you will meet: ISO 19115/19157, FGDC CSDGM, INSPIRE, STAC and its extensions, DataCite, and the internal metadata of GeoTIFF, LAS, and BAG. It walks through the hydrographic record (S-44 reports, NOAA Descriptive Reports, BAG and S-102 quality layers, CATZOC, GEBCO TID) and the lidar record (USGS LBS project reports, ASPRS accuracy language, calibration and trajectory files). You will learn which quality metadata actually changes decisions, how to generate structured metadata automatically with pystac and pygeometa, how metadata decays, and how to read a record forensically so that what is missing tells you what was never done.

## 49.1 The minimum set

Ask what a competent stranger needs in order to use an elevation dataset without calling you—not what a standard permits, what the stranger needs. The answer is a short list, and nearly every failure catalogued in [Chapter 56](ch56-case-files.md) traces to one of its items being absent, ambiguous, or wrong.

| Element | Minimum content | Chapter explaining the risk |
|---|---|---|
| Horizontal CRS | Datum, realization and epoch, projection, units, authority code | [Ch. 8](ch08-horizontal-datums.md) |
| Vertical CRS | Datum, geoid or tidal model and version, units, height-vs-depth sign, epoch | [Ch. 9](ch09-vertical-datums.md) |
| Surface type | DSM / DTM / bathymetric surface; what is included and excluded (buildings, bridges, piers, wires, vegetation, water surface) | [Ch. 4](ch04-names-and-definitions.md), [Ch. 32](ch32-dsm-to-dtm.md) |
| Acquisition dates | Start and end; per-cell date layer where sources are mixed | [Ch. 37](ch37-time-scales-of-change.md) |
| Sensor, platform, method | Instrument model, platform, measurement principle, nominal parameters | [Ch. 17](ch17-measurement-physics.md) |
| Lineage | Processing steps, software and versions, parameters | [Ch. 29](ch29-processing-pipelines.md) |
| Resolution | Grid spacing; source density; effective resolution if estimated | [Ch. 44](ch44-resolution-and-sampling.md) |
| Accuracy and uncertainty | Statistic, test method, reference, checkpoint count, per stratum; uncertainty layer if present | [Ch. 5](ch05-error-and-uncertainty.md), [Ch. 53](ch53-accuracy-assessment.md) |
| Voids, fills, masks | Where data are absent, interpolated, or borrowed | [Ch. 35](ch35-voids-and-overhangs.md) |
| Licence and constraints | SPDX identifier or licence text; attribution; caveats | [Ch. 68](ch68-legal-issues.md) |
| Contact, identifier, version | Responsible party; DOI or equivalent; version and what changed | [Ch. 50](ch50-archiving-and-provenance.md) |

*Table 49.1 — The minimum metadata set. Everything else is desirable; these are necessary.*

### 49.1.1 Coordinate reference systems, fully specified

A CRS statement is complete when a second person can reproduce the transformation you would apply. "WGS 84" is not complete: it names an ensemble of realizations whose members differ by up to about a metre horizontally over the decades, and it says nothing about the vertical. "NAVD88" is not complete either, because NAVD88 heights on modern surveys are realized through GNSS and a hybrid geoid model, and GEOID12B, GEOID18, and their predecessors differ by centimetres to a decimetre or more depending on region (NGS publishes the difference grids). The complete statement is an authority code where one exists (EPSG:6350 for NAD83(2011) Conus Albers; EPSG:5703 for NAVD88 height), plus the geoid model used, plus the epoch, plus the unit. The epoch matters for any plate-fixed frame on a moving plate and for all tidal datums, whose national epoch is itself a 19-year window. For bathymetry add the sounding datum (MLLW, LAT, chart datum) and the model or zoning used to reduce to it, and state whether values are depths positive-down or heights positive-up; a sign error is the most expensive one-bit mistake in the field.

Well-Known Text 2 (ISO 19162:2019) can carry all of this, including a compound CRS with a named geoid and an epoch in a `COORDINATEMETADATA` wrapper, and GeoTIFF 1.1 and LAS 1.4 both store WKT. Store it there *and* repeat the human-readable statement in the discovery metadata; the WKT is for software, the sentence is for the person who opens the record first.

### 49.1.2 Surface type with inclusions and exclusions

"DTM" and "DSM" are not sufficient. State whether bridges, culverts, and overpasses were removed or retained; whether building footprints were flattened or interpolated; how water bodies were treated (hydro-flattened to a constant, hydro-enforced, left as measured); whether piers and docks remain over water; whether bare earth under vegetation was estimated or interpolated across; and—for bathymetry—whether wrecks and obstructions were retained, and whether the surface is shoal-biased, mean, or median. [Chapter 32](ch32-dsm-to-dtm.md) and [Chapter 34](ch34-water-in-dems.md) show that each choice moves the surface by metres locally; the choice is recoverable only from the metadata.

### 49.1.3 Dates and accuracy

Record acquisition start and end dates to the day, and for mixed-source products a per-cell or per-tile date layer; record also the dates of ancillary measurements that determine the surface (tide observations, snow and leaf state). Publication and processing dates are not substitutes: a DEM whose only date is "2021" might contain 2009 photogrammetry; a GEBCO cell might rest on a 1930s lead-line sounding.

An accuracy statement is meaningful only with its derivation: the statistic (RMSE$_z$, 95 % confidence, LE95, TVU), the test method (independent checkpoints, crosslines, reference surface, propagation), the reference and its own uncertainty, the number and distribution of checkpoints, and the strata. "Vertical accuracy 10 cm" fails on every count; "NVA = 7.8 cm RMSE$_z$ (15.3 cm at 95 %), 42 GNSS checkpoints on open hard surfaces, reference σ ≈ 2 cm, NAVD88 via GEOID18; VVA = 24 cm at the 95th percentile, 31 forest checkpoints" passes.

> **Definitions that bite.** *Resolution.* In metadata the word is used for grid spacing, source point or pulse spacing, image ground sample distance, and effective resolution—the smallest feature actually resolved, usually two to five times the spacing ([Chapter 44](ch44-resolution-and-sampling.md)). ISO 19115 has one `spatialResolution` element, which almost everyone fills with the cell size. If you resampled a 10 m source to 1 m cells, say so in the same sentence; that is the most common way a "1 m DEM" misleads.

<!-- figure: Figure 49.1 — The minimum metadata set drawn as a one-page "label" for an elevation dataset, each field annotated with the chapter of this book that explains the error you risk by omitting it. -->

## 49.2 Standards

Metadata standards make the minimum set findable in a predictable place and parseable by software. None forces you to fill it in well.

### 49.2.1 ISO 19115 and ISO 19157

**ISO 19115-1:2014** (*Metadata — Part 1: Fundamentals*, amended 2018 and 2020) is the conceptual model most national catalogs use: identification, distribution, reference system, content, lineage, maintenance, and quality. **ISO 19115-2:2019** adds acquisition information—platform, instrument, operation, processing environment—where sensor metadata for lidar and sonar belongs. **ISO 19115-3** (a technical specification in 2016, a full standard in 2023) is the XML encoding that replaced ISO 19139; many catalogs still accept both.

**ISO 19157-1:2023** defines the data quality elements—completeness, logical consistency, positional accuracy (absolute and relative), thematic accuracy, temporal quality, usability—and a register of standardized measures. For a DEM, absolute vertical accuracy as RMSE or as a 95 % value, with the evaluation method and the sample count, goes in a `DQ_QuantitativeResult`. The structure is verbose, but it is the only widely implemented way to state "RMSE$_z$ 0.078 m from 42 checkpoints, direct external evaluation" in a machine-readable element rather than free text.

### 49.2.2 FGDC CSDGM ⟨H⟩

The US Federal Geographic Data Committee's **Content Standard for Digital Geospatial Metadata** appeared in 1994 and was revised as FGDC-STD-001-1998 ⟨H⟩. Mandated for US federal data by Executive Order 12906 (1994), it became the template ISO 19115 generalized. Its Data Quality section was ahead of its time in requiring positional accuracy *with a report of the test* and lineage with process steps and source citations. Two profiles matter here: the **Shoreline Metadata Profile** (FGDC-STD-001.2-2001), adding tidal datum and tide-coordination elements, and the **Extensions for Remote Sensing Metadata** (FGDC-STD-012-2002), adding platform, sensor, and processing-level elements. CSDGM records remain dominant for US lidar in The National Map and for NOAA bathymetric archives, and are often richer than the ISO records later generated by translation. Read them.

### 49.2.3 INSPIRE

The European INSPIRE **Data Specification on Elevation** (D2.8.II.1, Technical Guidelines v3.0, 2013) defines grid, vector, and TIN models and requires each dataset to state its vertical CRS, its surface type (DTM or DSM as a coverage property), and ISO 19157 quality elements including a positional accuracy report. It is a useful checklist outside Europe because it makes the DTM/DSM distinction and the vertical datum mandatory elements rather than free text.

### 49.2.4 STAC and its extensions

The **SpatioTemporal Asset Catalog** (STAC)—version 1.0.0 in May 2021 ⟨H⟩, 1.1.0 in September 2024—is a JSON specification for describing spatiotemporal assets so they can be crawled and searched. An **Item** is a GeoJSON Feature with a `datetime` (or `start_datetime`/`end_datetime`), `properties`, and `assets`; a **Collection** groups Items with extents, licence, providers, and summaries; a **Catalog** links Collections. The core is deliberately small; domain content lives in **extensions**, several of which are exactly what elevation needs: **projection** (`proj:code`, `proj:wkt2`, `proj:shape`, `proj:transform`—the full CRS including a vertical component); **raster** (`raster:bands` with `data_type`, `nodata`, `unit`, `spatial_resolution`, `statistics`); **pointcloud** (`pc:count`, `pc:type`, `pc:encoding`, `pc:density`, `pc:schemas`); **processing** (`processing:level`, `processing:lineage`, `processing:software` as a name→version map); **scientific** (`sci:doi`, `sci:citation`); **file** (`file:checksum` as a multihash, `file:size`); **version** (`version`, `deprecated`, `predecessor-version`/`successor-version` links); **eo** and **sat** for the imagery behind photogrammetric and InSAR DEMs; and **classification** for the meaning of mask values.

STAC has no accuracy extension. Practitioners put RMSE$_z$ and checkpoint counts in project-specific properties and link the checkpoint table from `links`; [Chapter 51](ch51-finding-data.md) argues that a shared accuracy extension is the single most useful missing piece for quality-first search.

### 49.2.5 DataCite, schema.org, OGC API – Records

**DataCite Metadata Schema 4** is what you fill in when minting a DOI—creators, title, publisher, year, plus recommended geolocation, version, and related identifiers such as `IsNewVersionOf`; it is citation metadata and should link to the ISO or STAC record. **schema.org/Dataset** JSON-LD on a landing page makes a dataset visible to general dataset search engines. **OGC API – Records** is the web-API successor to CSW and has converged with STAC API so that a STAC Collection is a valid Records record with minor additions.

### 49.2.6 Internal metadata versus sidecars

Formats carry their own metadata. A **GeoTIFF** stores CRS (GeoKeys; WKT in 1.1), affine transform, nodata, band statistics, and free-form tags; GDAL adds `.aux.xml` sidecars for the rest. A **LAS 1.4** file stores CRS as WKT in a Variable Length Record, point counts by return, bounding box, `system_id`, `software_id`, creation day and year, and a `global_encoding` flag stating whether GPS time is adjusted standard time; COPC adds a hierarchy VLR. A **BAG** embeds an ISO 19115/19139 XML document in HDF5 with BAG-specific elements for uncertainty type and a tracking list of overridden nodes. **S-102** carries S-100 Part 4a metadata in HDF5 attributes plus an exchange-set catalogue. NetCDF and Zarr carry CF attributes for units, standard names, and grid mapping ([Chapter 47](ch47-file-formats.md)).

Internal metadata travels with the bytes; sidecars and catalog records get separated on every copy. Put everything *software* needs (CRS, nodata, units, time, checksum) inside the file and everything a *person* needs (surface definition, dates, lineage, accuracy evidence, limitations, licence) in a record linked from the file's description tag; then verify the two agree. A GeoTIFF whose GeoKey says EPSG:4326 while its STAC Item says EPSG:32610 is a question with no answer.

> **Try it.** Read what a file says about itself before believing any external record.
>
> ```bash
> # GeoTIFF: CRS, nodata, tags
> gdalinfo -json dem.tif | jq '{wkt: .coordinateSystem.wkt[0:160], nodata: [.bands[].noDataValue], tags: .metadata}'
> # LAS/LAZ/COPC: header fields that identify sensor, software, and acquisition epoch
> pdal info --metadata cloud.copc.laz | jq '.metadata | {creation_year, creation_doy, system_id, software_id, count, global_encoding, srs: .srs.wkt[0:120]}'
> ```
>
> Expected outcome: a CRS string (or an empty one—itself a finding), a nodata value (or none), and for LAS a `system_id` and `software_id` that often identify the sensor and processing software even when the external record does not. If `creation_year` is the processing year, note that it is not the acquisition year.

## 49.3 Hydrographic metadata

Hydrography has the longest tradition of structured survey records, because charts carry liability. The record has three layers: the survey report, the quality attributes attached to the product, and the contribution metadata for international compilations.

### 49.3.1 The S-44 survey report and the NOAA Descriptive Report

**IHO S-44** (*Standards for Hydrographic Surveys*, Edition 6.1.0, 2022) specifies survey orders—Exclusive, Special, 1a, 1b, 2—by maximum allowable **total vertical uncertainty** (TVU) and **total horizontal uncertainty** (THU) at 95 %, feature detection, and coverage. TVU is parameterized as $\mathrm{TVU} = \sqrt{a^2 + (b\,d)^2}$ for depth $d$: Special Order $a = 0.25$ m, $b = 0.0075$; Order 1a/1b $a = 0.5$ m, $b = 0.013$; Order 2 $a = 1.0$ m, $b = 0.023$. S-44 requires a report stating the order achieved, positioning and sounding systems, datums and their realization, sound-speed and water-level reduction, calibrations, crossline results, and any areas where the order was not met. Edition 6 adds a specification *Matrix* so that a survey can declare uncertainty and coverage per area rather than one order per sheet.

The **NOAA Hydrographic Surveys Specifications and Deliverables** (HSSD, revised annually) make this concrete. The core document is the **Descriptive Report** (DR): A, Area Surveyed; B, Data Acquisition and Processing (vessels, sonars, positioning, sound speed, uncertainty-model parameters, software versions); C, Vertical and Horizontal Control (tide stations, zoning or VDatum method, GNSS control); D, Results and Recommendations (chart comparison, dangers to navigation, junctions); E, Approval. It is accompanied by a Survey Outline, BAG surfaces with uncertainty layers at prescribed resolutions, a feature file, the processed soundings, and the tide and sound-speed records. The HSSD's virtue is that it specifies the uncertainty *model inputs*—offsets, latency, patch-test values, zoning error—so that the TPU of every sounding is traceable to a number in section B.

### 49.3.2 BAG metadata and S-102 quality layers

A **Bathymetric Attributed Grid** (BAG, Open Navigation Surface Working Group, version 2.0) embeds an ISO 19115/19139 document that must state the horizontal and vertical reference systems, the vertical uncertainty type (a controlled vocabulary: raw standard deviation, computed from a product specification, historical, etc.), the depth correction type, the surface type (mean, shoal-biased, CUBE), process steps, and constraints. Every BAG also carries the **uncertainty layer** itself, so the metadata describes what kind of number the layer holds rather than asserting one survey-wide value. The **tracking list** records nodes manually overridden, with the original value and a reason code—cell-level provenance, and a model for what land DEM producers rarely offer.

**IHO S-102** (*Bathymetric Surface Product Specification*, Edition 3.0.0, December 2024) carries depth and uncertainty coverages and, since the Edition 2.x series, a per-cell quality feature—`QualityOfSurvey` in Edition 2.x, renamed `QualityOfBathymetryCoverage` in 3.0—that points each cell to a record of survey date range, source identifier, feature-detection and coverage attributes, and a CATZOC-equivalent category. It is the hydrographic answer to the "which source and when" question that [Chapter 48](ch48-compositing.md) raises for composites: the answer travels with the product in a queryable raster, not a PDF.

### 49.3.3 CATZOC

On electronic navigational charts the **Category of Zone of Confidence** (CATZOC) attribute classifies areas by positional and depth accuracy and seafloor coverage of their source surveys (Table 49.2). It is coarse, assigned by the compiler rather than measured per cell, and a large share of charted waters remains U (unassessed) or D. But it is the only quality statement most mariners see, and ECDIS uses it in safety logic. When you ingest ENC soundings into a DEM, carry CATZOC through as a per-source attribute.

| CATZOC | Horizontal (95 %) | Depth (95 %) | Seafloor coverage |
|---|---|---|---|
| A1 | ±5 m + 5 % depth | 0.5 m + 1 % depth | Full area search; all significant features detected |
| A2 | ±20 m | 1.0 m + 2 % depth | Full area search; all significant features detected |
| B | ±50 m | 1.0 m + 2 % depth | Full search not achieved; hazardous uncharted features not expected |
| C | ±500 m | 2.0 m + 5 % depth | Full search not achieved; depth anomalies may be expected |
| D | Worse than C | Worse than C | Large depth anomalies may be expected |
| U | Not assessed | Not assessed | — |

*Table 49.2 — CATZOC categories (IHO S-57 Appendix A; retained in S-101 as a quality-of-bathymetric-data attribute).*

### 49.3.4 GEBCO TID and DCDB contribution metadata

The **GEBCO Type Identifier** (TID) grid, released with every GEBCO grid since GEBCO_2014, gives each cell an integer for the kind of source that determined it: 0 land; 10 single-beam; 11 multibeam; 12 seismic; 13 isolated sounding; 14 ENC sounding; 15 lidar; 16 optical; 17 combination of direct methods; 40 predicted from satellite-derived gravity; 41 interpolated by algorithm; 42 digitized contours from charts; 43 digitized contours from ENCs; 44 soundings in a gridded dataset with gravity-guided interpolation; 70 pre-generated mixed grid; 71 unknown; 72 steering points. The TID is not an uncertainty, but it separates measured from inferred cells, and in most of the deep ocean the inferred cells dominate; mask by TID before any analysis that treats GEBCO as a seafloor.

The **IHO Data Centre for Digital Bathymetry** (DCDB, hosted by NOAA NCEI) accepts formal surveys and **crowdsourced bathymetry** (CSB) under IHO **B-12** (*Guidance on Crowdsourced Bathymetry*, Edition 3.0.0, 2023). CSB contribution metadata is deliberately light—provider, platform identifier (optionally anonymized), sensor type, draft and offsets if known, position source, corrections applied—because the point is to get data in; the DCDB exposes that metadata so users can decide how much to trust it.

> **Case file.** Before 2014 GEBCO grids were distributed without a source-type layer, and users regularly treated the global surface as measured bathymetry: ship-track artefacts and gravity-predicted texture were interpreted as geology, and interpolated depths were used for cable routing and habitat models. GEBCO_2014 introduced the TID grid so that the majority of ocean cells constrained only indirectly could be identified cell by cell (Weatherall et al., 2015); Seabed 2030 now reports progress as the fraction of cells with direct-measurement TIDs—the metadata layer became the progress metric.

<!-- figure: Figure 49.2 — A GEBCO tile rendered as hillshade beside its TID grid, showing that the apparent seafloor texture lies almost entirely in cells with TID 40/41 and that measured cells form narrow ship-track ribbons. -->

## 49.4 Lidar and photogrammetric metadata

The **USGS Lidar Base Specification** (LBS, 2024 edition) defines deliverables for 3DEP lidar and has become the de facto template for North American lidar metadata. Required project-level deliverables include a **collection report** (sensor, platform, flight dates and times, flight-line map, nominal pulse spacing and density, scan angle, overlap, snow and leaf state), a **survey/control report** (base stations with datum realization; checkpoint coordinates, method, and photographs), a **processing report** (software versions, calibration and boresight procedure, classification methods, breakline and hydro-flattening rules), and a **QA/QC report** with a table of every checkpoint—surveyed coordinates, lidar elevation, residual, land-cover stratum—plus NVA and VVA, intraswath and interswath statistics, and a gridded density assessment. The LBS also requires FGDC or ISO metadata per tile and per project, and delivery of swath point clouds, classified tiles, DEM, breaklines, and flight trajectories.

The trajectory—commonly an Applanix **SBET** (*Smoothed Best Estimate of Trajectory*) or an equivalent record of position, attitude, and covariances at 100–200 Hz—is metadata in the most literal sense: data about where the sensor was when each point was measured. Without it there is no strip re-adjustment, no boresight re-check, and no recomputed per-point uncertainty ([Chapter 13](ch13-imu-ins.md), [Chapter 18](ch18-topographic-lidar.md)). Archive it with the points.

The **ASPRS Positional Accuracy Standards** (Edition 2, 2023) prescribe not only statistics but sentences, distinguishing data *produced to meet* a class from data *tested to meet* it: "This dataset was tested to meet ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023) for a __ (cm) RMSE$_V$ Vertical Accuracy Class. NVA accuracy was found to be RMSE$_V$ = __ (cm). VVA accuracy was found to be RMSE$_V$ = __ (cm)." Note the change from Edition 1, which reported NVA as RMSE$_z$ × 1.96 and VVA at the 95th percentile; Edition 2 reports both strata as RMSE$_V$, and the Edition 1 vocabulary survives in the USGS LBS. Use the template verbatim; its value is that a reader can tell in one sentence whether anyone measured anything, and with fewer than 30 checkpoints the standard requires you to say so in the same sentence.

Calibration records complete the set: boresight and lever-arm values with the calibration flight's date, site, and residuals; for photogrammetry the camera calibration certificate, the interior orientation actually used, and the bundle-adjustment report with control and tie-point residuals ([Chapter 22](ch22-photogrammetry-sfm.md)); for multibeam the patch-test values and vessel offset survey ([Chapter 20](ch20-sonar.md)). Systematic errors live in these documents; an undocumented calibration cannot be audited, only re-measured.

## 49.5 Quality metadata that actually helps

A long ISO record whose quality section says "data meet specification" changes no decision. The quality metadata users act on is spatial, numeric, and specific.

**Uncertainty rasters.** A per-cell 1σ or 95 % layer—propagated TPU for sonar and bathymetric lidar, a sensor-model or density-and-slope estimate for topographic lidar, matching confidence for photogrammetry, a height-error map for InSAR DEMs (TanDEM-X and Copernicus DEM ship one). It lets a user compute minimum detectable change ([Chapter 41](ch41-change-detection.md)) and weight a composite ([Chapter 48](ch48-compositing.md)).

**Checkpoint tables with coordinates.** Not the summary RMSE: the points, with land cover, surveyed and modelled heights, and residuals. A user can then re-test for their own area and strata and can see whether the checkpoints were clustered on one road. The LBS requires this table; most non-US deliveries omit it.

**Density and coverage maps.** Ground-return density per cell, soundings per node, image or match count per cell. They show where effective resolution collapses and where the DTM is interpolation.

**Swath and crossline statistics.** Interswath RMSD$_z$ in overlaps and crossline-versus-mainline differences are the only relative-accuracy evidence independent of ground control; mapped, they expose strips with calibration or trajectory problems.

**Known-issue lists.** A plain list—"tiles 0412–0418 flown after snowfall; bridge decks retained east of the river; Lake X set to 231.4 m from one gauge reading; channel 2 intensity unreliable"—is the most-read part of any record and the least often written. It belongs in the abstract or a *Limitations* element.

## 49.6 Generating metadata without heroics

Metadata is written badly when it is written last by hand. It is written well when the structured parts are generated by the pipeline that made the data and the unstructured parts are written by the person who understands the limitations.

Every value in Table 49.1 except surface definition, limitations, and licence can be read from files or logs: CRS, extent, nodata, and statistics from `gdalinfo` or rasterio; point count, density, classification histogram, and GPS-time range from `pdal info`; software versions from the environment; parameters from the pipeline manifest ([Chapter 29](ch29-processing-pipelines.md)); accuracy statistics from the checkpoint script; checksums from the archival step. Write a script that assembles these into a STAC Item (for catalogs and machines) and a **pygeometa** Metadata Control File (a YAML document rendered to ISO 19139 or 19115-3 XML for national catalogs). Run it as the last pipeline step and fail the build if a mandatory field is empty.

> **Try it.** Generate a STAC Item for a DEM tile from the file itself plus a small dictionary of human-supplied facts; render ISO XML from the same facts with pygeometa.
>
> ```python
> import json, hashlib, subprocess, rasterio, rasterio.warp, pystac
> from pystac.extensions.projection import ProjectionExtension
> from pystac.extensions.raster import RasterExtension, RasterBand
> from pystac.extensions.file import FileExtension
> from shapely.geometry import box, mapping
>
> path = "dem_tile_0412.tif"
> human = {   # the parts a pipeline cannot know
>   "surface": "DTM; buildings and bridge decks removed; water hydro-flattened",
>   "vertical": "NAVD88 height (EPSG:5703) via GEOID18; epoch 2023.6",
>   "start": "2023-07-11T00:00:00Z", "end": "2023-08-02T23:59:59Z",
>   "nva_rmse_m": 0.078, "nva_n": 42, "vva_95th_m": 0.24, "vva_n": 31,
>   "licence": "CC0-1.0",
>   "limitations": "Tiles 0412-0418 flown after a 2023-07-30 snowfall above 2,400 m.",
> }
> with rasterio.open(path) as src:
>     crs, shape, tr, nodata = src.crs, src.shape, src.transform, src.nodata
>     bbox = list(rasterio.warp.transform_bounds(crs, "EPSG:4326", *src.bounds))
>     arr = src.read(1, masked=True)
> item = pystac.Item(id="dem_tile_0412", geometry=mapping(box(*bbox)), bbox=bbox,
>     datetime=None, properties={
>       "start_datetime": human["start"], "end_datetime": human["end"],
>       "description": f'{human["surface"]}. {human["vertical"]}.',
>       "dem:surface_type": "DTM", "dem:limitations": human["limitations"],
>       "dem:nva_rmse_m": human["nva_rmse_m"], "dem:nva_checkpoints": human["nva_n"],
>       "dem:vva_95th_m": human["vva_95th_m"], "dem:vva_checkpoints": human["vva_n"],
>       "processing:software": {"pdal": subprocess.run(["pdal", "--version"],
>                                capture_output=True, text=True).stdout.strip()},
>       "license": human["licence"]})
> proj = ProjectionExtension.ext(item, add_if_missing=True)
> proj.epsg, proj.wkt2 = crs.to_epsg(), crs.to_wkt()
> proj.shape, proj.transform = list(shape), list(tr)[:6]
> asset = pystac.Asset(href=path, media_type=pystac.MediaType.COG, roles=["data"])
> item.add_asset("dem", asset)
> RasterExtension.ext(asset, add_if_missing=True).bands = [RasterBand.create(
>     data_type="float32", nodata=nodata, unit="metre", spatial_resolution=abs(tr.a),
>     statistics={"minimum": float(arr.min()), "maximum": float(arr.max())})]
> sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
> FileExtension.ext(asset, add_if_missing=True).checksum = "1220" + sha  # multihash sha2-256
> item.validate()
> json.dump(item.to_dict(), open("dem_tile_0412.json", "w"), indent=2)
> ```
>
> ```bash
> stac-validator dem_tile_0412.json
> # pygeometa: a YAML MCF holding the same facts (title, abstract = surface + vertical +
> # limitations, temporal extent, licence, contact, distribution URL) renders to ISO:
> pygeometa metadata generate dem_tile_0412.yml --schema iso19139 > dem_tile_0412.xml
> ```
>
> Expected outcome: a STAC Item valid against core plus the projection, raster, and file extensions, and an ISO 19139 document that GeoNetwork or pycsw will ingest. The `dem:` properties are project-local; replace them with a community accuracy extension when one exists. Only the `human` dictionary required a person.

Validate structure with `stac-validator` or `pystac`'s `validate()`, and ISO XML against the 19139/19115-3 schemas (and in Europe the INSPIRE validator). Then validate *content* with a project-specific checker: vertical CRS present and compound; geoid named; acquisition dates not equal to the processing date; accuracy fields populated with a count of at least the ASPRS minimum of 30 per stratum ([Chapter 53](ch53-accuracy-assessment.md)); checksum present; licence an SPDX identifier. Schema validity is necessary and nearly meaningless; a schema-valid record can say the vertical datum is "metres."

The *Limitations* element should be written by the person who processed the data, in the week they finished, answering: what did we not do; where is the data worse than the headline accuracy; what will surprise someone who assumes bare earth everywhere; what changed in the real world during acquisition. It is the only part of the record that cannot be generated and the only part most users read in full.

## 49.7 Metadata decay and currency

A record is correct on the day it is written and becomes less correct every year after, even if the data never change. Three mechanisms drive the decay.

**The world around the dataset changes.** The vertical datum is re-realized—NGS's replacement of NAVD88 by the North American–Pacific Geopotential Datum of 2022 (adoption still pending; beta products expected 2026) will shift heights by decimetres to over a metre in parts of the continent ([Chapter 9](ch09-vertical-datums.md)); a new geoid model is published; the frame is updated; a tidal epoch rolls over. "NAVD88 via GEOID12B" remains a true statement of what was done, but a user in 2030 who treats it as interchangeable with current heights will be wrong by the model difference and then by the datum transition. State realizations precisely enough that the published transformation can be applied, and keep the transformation grids ([Chapter 50](ch50-archiving-and-provenance.md)).

**The dataset is superseded.** A newer survey covers the area; a reprocessing corrects a bias; a composite retracts a source. Unless the old record gains a successor link (STAC `successor-version`, DataCite `IsPreviousVersionOf`, ISO maintenance information), copies of the old product circulate as current. NOAA's National Bathymetric Source models the discipline: every tile carries a supersession record naming what replaced what and why.

**Links break.** Records point to licences, checkpoint tables, project reports, and the data; servers are renamed, FTP is turned off, a contractor's domain lapses. Remedies: persistent identifiers for datasets and their reports; critical documents stored *inside* the archive package; periodic link audits. A landing page whose files silently changed is worse than a dead link—version the files and let the DOI resolve to a version list.


## 49.8 Reading metadata forensically

A record is evidence not only of what was done but of what was not. Those who evaluate other people's data ([Chapter 54](ch54-evaluating-others-data.md)) learn to read absences:

- **No vertical CRS, or "WGS 84" alone** → the producer never confronted the geoid question; heights are whatever the software defaulted to. Test against a known point before use.
- **Orthometric datum without a geoid model** → the transformation was done once and forgotten; the difference from a current realization is unknown at the decimetre level.
- **Accuracy as a bare number** → no test, or the sensor's nominal specification. Treat as "produced to meet."
- **Accuracy without checkpoint count or distribution** → possibly a handful of points on roads; vegetated and sloped areas untested.
- **Acquisition date equal to publication year, or year only** → acquisition untracked; mixed epochs likely.
- **Cell size finer than source density supports** → oversampled; effective resolution coarser ([Chapter 44](ch44-resolution-and-sampling.md)).
- **No void or fill description for a seamless product** → fills unmarked; expect interpolated terrain in shadows and over water.
- **Metadata only as a PDF or an image of a title block** → unsearchable, unvalidatable, and likely a copied template.

Copied templates are the most common metadata failure in practice: the elements nobody looked at—geoid model, sensor serial, checkpoint count, limitations—carry over from the previous project unchanged. Compare records across projects from the same producer; identical quality sections for different surveys are a finding.

> **Worked example.** Two national DEMs are to be joined at a border. Record A: "Vertical datum: EGM96; source: SRTM-derived, void-filled." Record B: "Vertical datum: EGM2008; source: TanDEM-X-derived, edited." Reading the two geoid models over the region gives an EGM96→EGM2008 difference ranging from $-0.42$ to $+0.61$ m. A naive mosaic would therefore carry a step of up to about 1 m at the seam, which a geomorphologist would read as a scarp and a hydrologic model would treat as a dam ([Chapter 61](ch61-hydrology.md)). The fix is to convert both to ellipsoidal heights, $h = H + N$, with the named geoids and then to one target; the metadata that made this possible was two words per record—the geoid name. Had either said only "mean sea level," the step would have been undiagnosable.

<!-- figure: Figure 49.3 — A real (anonymized) metadata record annotated with forensic marks: present fields in green, absent mandatory fields in red with the inferred consequence in the margin ("no geoid → vertical uncertain ±0.3 m"; "accuracy 'meets spec' → untested"). -->

## Then & now

Metadata began as marginalia. A nineteenth-century hydrographic **smooth sheet** carried in its title block the vessel, the officers, the dates, the sounding method, the datum of reduction, and the scale—a complete lineage record by the standards of Table 49.1, lacking only an accuracy test. The information was authoritative and un-queryable.

The transition to digital data in the 1970s–1980s lost most of it: DTED and early USGS DEMs carried fixed-width headers with datum and spacing and little else. The **FGDC CSDGM** (1994; revised 1998) ⟨H⟩ restored the full record in parseable form under the US National Spatial Data Infrastructure, and **ISO 19115** (2003; revised 2014) generalized its pattern internationally.

**STAC** (development from 2017; 1.0 in 2021 ⟨H⟩; 1.1 in 2024) inverted the priorities: a small JSON core any web developer could emit and crawl, extensions for domain content, and a search API. Built for satellite imagery on object storage, it was adopted for elevation because the same questions apply; its cost is that quality metadata has no standard home yet. Hydrography moved in parallel from the paper Descriptive Report to BAG's embedded ISO record (2006) to S-102's per-cell quality coverage, and GEBCO's TID (2014) showed that a quality layer can be a raster. The arc runs from documents, to records, to API-queryable catalogs, to quality inside the data; the content required has not changed since the smooth sheet.

## Validation & uncertainty

Metadata is itself a claim and can be wrong. Its errors arise from four sources, each with a test.

**Transcription and template errors.** The record states a value that is not the value in the data. Test by cross-checking record against bytes: parse the file's internal CRS, extent, nodata, point count, and GPS-time range and compare field by field. For point clouds, convert the GPS-time range to calendar dates (respecting the adjusted-standard-time flag and its 10⁹ s offset) and compare with the stated acquisition window; mismatches of months are not rare. A build-breaking script for this takes an hour to write.

**Vertical-reference ambiguity.** The record names a datum without its realization. Quantify by computing the difference between plausible realizations over the extent—GEOID12B vs GEOID18, EGM96 vs EGM2008, MLLW by zoning vs by VDatum. If the range exceeds the stated accuracy, as it usually does over large extents, the ambiguity dominates the error budget until resolved by testing against known points ([Chapter 52](ch52-ground-truth.md)).

**Unsupported accuracy claims.** Test by re-measuring: 20–30 GNSS points on open ground, a crossline, or a comparison with a better overlapping dataset. State your test's own uncertainty: with checkpoint σ of 2–3 cm and 30 points, the 95 % confidence interval on an RMSE of 10 cm is roughly 8–13 cm ([Chapter 53](ch53-accuracy-assessment.md)); you cannot refute a 10 cm claim with 12 cm, but you can with 30 cm.

**Decay.** Check realizations, links, and supersession status against current registries (EPSG, NGS geoid pages, DataCite, the producer's catalog).

> **Uncertainty budget.** Vertical error introduced by metadata ambiguity alone, for a product whose measured accuracy is 10 cm RMSE$_z$ (approximate, region-dependent magnitudes):
>
> | Ambiguity in the record | Typical magnitude | Dominates a 10 cm product? |
> |---|---|---|
> | Orthometric datum named, geoid model not | 0.02–0.15 m | Often |
> | "WGS 84" vertical, ellipsoidal vs orthometric unstated | 10–60 m | Always (gross) |
> | EGM96 vs EGM2008 unstated | 0.1–1 m, locally more | Always |
> | Tidal datum unstated (MLLW vs MSL vs LAT) | 0.3–3 m | Always |
> | Depth vs height sign unstated | 2 × depth | Always (gross) |
> | Acquisition date unstated in changing terrain | 0 to several m | Site-dependent |
> | DSM vs DTM unstated in built or forested terrain | 0–30 m | Wherever objects exist |
>
> Each row is gross relative to the measurement error, which is why the minimum set is a correctness requirement, not documentation polish.

Report, when you publish: every row of Table 49.1 with its evidence; the result of the record-versus-file cross-check; the date the record was last verified; and, for inherited data, what you assumed and what test justified it.

## Software

**Open source:** **pystac** (build, read, validate STAC with extension classes); **stac-validator** / **stac-check** (schema and best-practice validation); **pygeometa** (YAML MCF to ISO 19139/19115-3, DCAT, STAC—the fastest route from pipeline to national catalog); **GeoNetwork** (ISO editors, validators, CSW and OGC API – Records); **pycsw** (CSW/Records server ingesting ISO, FGDC, STAC); **CKAN** with the spatial extension (DCAT-flavoured; shallow for elevation specifics); **mdEditor**/**mdTranslator** (browser editor and translator for ISO 19115-2/-3 and FGDC); **GDAL** and **PDAL** (internal metadata readers; GDAL's BAG and S-102 drivers expose embedded ISO and quality groups); **NOAA s100py** (S-102/S-104/S-111 HDF5 with S-100 metadata); **laspy** (LAS VLRs and WKT); the ISO 19139/19115-3 XSDs and INSPIRE Reference Validator. Caveat common to all: they validate structure, not truth.

**Free but closed:** NOAA **Pydro** (HSSD deliverables and DR assembly).

**Commercial:** **ArcGIS Pro** metadata editor (ISO and FGDC styles; synchronizes some properties from data—convenient, and a source of stale values when sync is off); **CARIS HIPS/SIPS** and **BASE Editor** (BAG metadata, DR content, survey statistics); **QPS Qimera** (BAG export with uncertainty typing); **FME** (metadata transformation at scale); commercial geoportals (record-store lock-in is the caveat).

## Standards & guides

- **ISO 19115-1:2014** (Amd 1:2018, Amd 2:2020); **ISO 19115-2:2019**; **ISO 19115-3:2023** — metadata model, acquisition extensions, XML encoding.
- **ISO 19157-1:2023** — data quality elements, measures, evaluation, reporting.
- **ISO 19162:2019** — WKT2 for complete CRS statements including vertical and epoch.
- **FGDC-STD-001-1998** ⟨H⟩; **FGDC-STD-001.2-2001** (Shoreline Profile); **FGDC-STD-012-2002** (Remote Sensing Extensions) — US federal metadata content.
- **STAC 1.0.0 (2021) / 1.1.0 (2024)** with projection, raster, pointcloud, processing, scientific, file, version, eo, sat, classification extensions; **STAC API 1.0.0 (2023)**.
- **OGC API – Records – Part 1: Core** — web-API catalog records, convergent with STAC.
- **INSPIRE D2.8.II.1 Elevation Technical Guidelines v3.0 (2013)** — mandatory elevation metadata in Europe.
- **USGS Lidar Base Specification 2024** — project reports, metadata, QA/QC deliverables.
- **ASPRS Positional Accuracy Standards, Edition 2 (2023)** — accuracy classes and reporting language.
- **NOAA HSSD** (current annual edition) — Descriptive Report and metadata deliverables.
- **IHO S-44 Ed. 6.1.0 (2022)**; **S-100 Ed. 5.2.0 Part 4a**; **S-102 Ed. 3.0.0 (2024)**; **S-57 App. A / S-101** (CATZOC); **B-12 Ed. 3.0.0 (2023)**; **B-11 GEBCO Cookbook** — hydrographic survey reporting, product metadata, zones of confidence, CSB, TID practice.
- **ONSWG BAG Format Specification 2.0** — embedded ISO metadata and uncertainty typing.
- **DataCite Metadata Schema 4.5/4.6** — DOI registration including versions and related identifiers.

## Pitfalls

- **"Vertical datum: NAVD88" with no geoid model** → the software dialog offered only the datum name → grep the record for "GEOID"; make the model a mandatory template field.
- **"Accuracy: 0.1 m" with no statistic, count, or method** → the record echoes the contract → look for the ASPRS "tested to meet" sentence and a checkpoint table; deliver the table.
- **Dates set to publication or processing year** → the tool defaulted to "now" → compare with LAS GPS-time ranges; generate dates from the data.
- **Metadata only in a PDF, an image, or an unstructured README** → faster to produce → generate STAC plus ISO from the pipeline so the structured record costs nothing.
- **Previous project's record copied and retitled** → deadline → diff quality sections across projects from one producer; require a freshly written limitations paragraph.
- **File metadata disagreeing with the external record** → files reprojected or re-tiled after the record was written → automated cross-check as the last pipeline step.
- **"Resolution: 1 m" for a resampled coarser source** → cell size is the only resolution field → compare source density to cell size; state density and effective resolution alongside spacing.
- **"DEM" with no inclusions/exclusions** → producer thinks it obvious → inspect bridges and buildings in a hillshade; mandate a surface-definition sentence.
- **Void fills unmarked in a seamless product** → it looks finished → compare with a density or source raster; publish the mask.
- **DOI pointing to a landing page whose files were replaced** → a fix uploaded over the original → checksum mismatch against earlier downloads; version files and DOI.

## Key takeaways

- Metadata is the user's only defence against misusing the data and your only defence against misremembering what you did; treat it as part of the measurement, with its own uncertainty.
- The minimum set—full CRS with geoid and epoch, surface definition, acquisition dates, sensor and method, lineage with versions, resolution in its several senses, accuracy with evidence, voids and masks, licence, identifier, version—is a correctness requirement.
- Automate the structured parts from the pipeline (STAC for machines, ISO via pygeometa for catalogs), hand-write the limitations, and fail the build on empty mandatory fields or file–record disagreement.
- Quality metadata that changes decisions is spatial and numeric: uncertainty rasters, checkpoint tables with coordinates, density maps, swath and crossline statistics, per-cell source and date layers, and a known-issues list.
- Hydrography shows mature practice—S-44 reports, Descriptive Reports with uncertainty-model inputs, BAG's embedded record and tracking list, S-102 per-cell quality, CATZOC, GEBCO TID—and land DEM producers should copy it.
- Metadata decays: realizations change, products are superseded, links break. State realizations precisely, link supersession explicitly, use persistent identifiers, audit.
- Read metadata forensically: what is missing tells you what was never done. If it is not in the metadata, assume it was not measured.

## References

- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2. American Society for Photogrammetry and Remote Sensing.
- Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., et al. (2020). The CARE Principles for Indigenous Data Governance. *Data Science Journal* 19(1):43. doi:10.5334/dsj-2020-043.
- Devillers, R., Stein, A., Bédard, Y., Chrisman, N., Fisher, P., and Shi, W. (2010). Thirty years of research on spatial data quality: achievements, failures, and opportunities. *Transactions in GIS* 14(4):387–400.
- Federal Geographic Data Committee (1998). *Content Standard for Digital Geospatial Metadata*, FGDC-STD-001-1998. Washington, DC: FGDC.
- Federal Geographic Data Committee (2001). *Shoreline Metadata Profile*, FGDC-STD-001.2-2001; and (2002) *Extensions for Remote Sensing Metadata*, FGDC-STD-012-2002.
- Goodchild, M. F. (2007). Citizens as sensors: the world of volunteered geography. *GeoJournal* 69(4):211–221.
- STAC Contributors (2021). *SpatioTemporal Asset Catalog (STAC) Specification*, version 1.0.0 (community-authored; Radiant Earth Foundation). stacspec.org.
- International Hydrographic Organization (2022). *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. Monaco: IHO.
- International Hydrographic Organization (2024). *S-102 Bathymetric Surface Product Specification*, Edition 3.0.0. Monaco: IHO.
- ISO (2014). *ISO 19115-1:2014 Geographic information — Metadata — Part 1: Fundamentals*. Geneva: ISO.
- ISO (2023). *ISO 19157-1:2023 Geographic information — Data quality — Part 1: General requirements*. Geneva: ISO.
- Joint Research Centre (2013). *D2.8.II.1 INSPIRE Data Specification on Elevation — Technical Guidelines*, v3.0. European Commission.
- NOAA Office of Coast Survey (current edition). *Hydrographic Surveys Specifications and Deliverables*. Silver Spring, MD: NOAA.
- Open Navigation Surface Working Group (2022). *Bathymetric Attributed Grid (BAG) Format Specification Document*, Version 2.0.1 (also an OGC Community Standard).
- Tsou, M.-H. (2002). An operational metadata framework for searching, indexing, and retrieving distributed geographic information services on the Internet. In Egenhofer, M. J. and Mark, D. M. (eds.), *GIScience 2002*, LNCS 2478, pp. 313–332. Berlin: Springer.
- US Geological Survey (2024). *Lidar Base Specification 2024*. National Geospatial Program. Reston, VA: USGS.
- Weatherall, P., Marks, K. M., Jakobsson, M., et al. (2015). A new digital bathymetric model of the world's oceans. *Earth and Space Science* 2(8):331–345. doi:10.1002/2015EA000107.
- Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data* 3:160018. doi:10.1038/sdata.2016.18.

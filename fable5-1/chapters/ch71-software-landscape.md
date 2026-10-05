# Chapter 71 — Software landscape: open-source and closed-source by task

> **Part XVI — Standards, software, and history.** Who does what in elevation-data work, organized by task rather than vendor, with licences, lineage, strengths, and the risks of lock-in — the catalogue behind every "Software" section in this book.

**In this chapter.** Every chapter so far has ended with a Software section; this one is the map those sections point into. It explains how to read a software landscape — open source under OSI licences, free-but-closed, and commercial; maturity, community, format fidelity, scripting, and provenance features; the foundations (OSGeo, NumFOCUS, OGC, Linux Foundation) that keep projects alive — and then tours the tools by task: foundations and libraries, GNSS/INS processing, lidar, photogrammetry and SfM, sonar and hydrography, radar and InSAR, geodesy and datums, DEM analysis and hydrology, change detection and validation, machine learning, visualization and cartography, data management and catalogs, planetary, and cloud platforms. Each task area has a compact table. The chapter closes with how to choose and govern software — validating it like data with benchmarks and round trips, pinning versions, reproducible environments, licence compliance, bus-factor risk, and when to buy. [Appendix F](../appendices/appendix-f-software-index.md) holds the sortable index.

## 71.1 How to read this chapter

Three licensing categories structure everything that follows. **Open source** means a licence approved by the Open Source Initiative — permissive (MIT, BSD, Apache 2.0) or copyleft (GPL, LGPL, AGPL, MPL, CeCILL) — under which anyone may read, modify, and redistribute the code; it is the only category in which you can audit an algorithm, fix a bug yourself, and be sure of running the software in twenty years. **Free but closed** ("freeware") costs nothing but withholds the source: HEC-RAS, NOAA's VDatum and Pydro, FUSION, many vendor viewers, and most "community editions" sit here, and the category is where the most dangerous confusion lives — *freeware is not open source*; its future depends entirely on its owner. **Commercial** software is licensed for money under proprietary terms, perpetual or subscription, node-locked or floating, often with maintenance contracts and, increasingly, cloud-only delivery.

Beyond licence, evaluate: **maturity** (age, release cadence, test suite, issue backlog); **community** (contributors beyond one employer, a foundation home, documentation and answers that exist); **format fidelity** (does it read and write LAS 1.4 PDRF 6–10 with all extra bytes, COG with overviews, BAG with the uncertainty layer, and preserve CRS and vertical-datum metadata? — [Chapter 47](ch47-file-formats.md)); **scripting and APIs** (a GUI-only tool cannot be put in a pipeline or a provenance log); and **provenance features** (does it record parameters, versions, and lineage in outputs? — [Chapter 50](ch50-archiving-and-provenance.md)). Sustainability matters more than features for anything you will depend on for a decade: the **Open Source Geospatial Foundation** (OSGeo, founded 2006) ⟨H⟩ hosts GDAL, PROJ, GEOS, GRASS, QGIS, PDAL, and others through an incubation process that requires open governance; **NumFOCUS** (2012) sponsors the scientific Python stack (NumPy, SciPy, xarray, pandas, Project Jupyter); the **Linux Foundation** hosts the Overture Maps Foundation and OpenJS; and the **Open Geospatial Consortium** (1994) standardizes the interfaces and formats these projects implement. A project with a foundation home, several employers among its maintainers, and a public roadmap has a low **bus factor** risk; a brilliant single-maintainer tool — and the field has many — does not, however good it is today.

> **Rule of thumb.** For every step in a pipeline that produces a deliverable, keep an open-source path that can reproduce the step to within its stated uncertainty, even if production runs on commercial software. It need not be as fast or as pretty; it must exist and be tested once a year. The rule fails for steps whose algorithms are genuinely proprietary (some sensor-specific waveform processing, vendor trajectory solutions), where the mitigation is to archive the raw inputs and the vendor's intermediate products rather than an alternative tool.

## 71.2 Foundations and libraries

The elevation world runs on a small set of libraries that almost every tool, open or closed, links against. **GDAL/OGR** (begun by Frank Warmerdam in 1998, first release 2000; MIT licence; OSGeo) ⟨H⟩ reads and writes some 200 raster and vector formats and is the de facto definition of how a GeoTIFF, COG, or BAG is interpreted — ArcGIS, Global Mapper, QGIS, and most commercial hydrographic suites all ship it. **PROJ** (lineage from Gerald Evenden's USGS PROJ of the 1980s; MIT) ⟨H⟩ performs coordinate operations, including, since PROJ 6–7 (2019–2020), full ISO 19111 pipelines, time-dependent transformations, and grid-based vertical transformations distributed through PROJ-data and the CDN ([Chapter 8](ch08-horizontal-datums.md), [Chapter 9](ch09-vertical-datums.md)). **GEOS** (LGPL) supplies planar geometry; **PDAL** (BSD; 2011–, Hobu) is the point-cloud counterpart of GDAL — readers, writers, and a filter pipeline for LAS/LAZ/COPC/EPT/E57 and more ([Chapter 29](ch29-processing-pipelines.md), [Chapter 30](ch30-point-cloud-classification.md)); **laspy** (BSD) reads LAS/LAZ in Python; **rasterio** (BSD) wraps GDAL for Python, and **xarray/rioxarray/dask** (Apache 2.0) provide labelled, lazy, chunked arrays for grids that do not fit in memory ([Chapter 46](ch46-data-models.md)). **GMT** (Wessel and Smith, 1991; LGPL; GMT 6 in 2019) ⟨H⟩ remains the standard for gridding (`surface`, `nearneighbor`), grid algebra, and publication maps in marine geophysics; **PyGMT** exposes it to Python. The **NumPy/SciPy** stack supplies the numerics; **R** has **terra** (rasters, successor to raster), **sf** (vectors), **lidR** (airborne lidar; GPL-3), and **gstat** (geostatistics); **Julia** has GeoStats.jl; **Rust** and **Go** host fast new tooling (the `geo` crate, tile servers, `pdal`-adjacent point-cloud crates) that often ends up wrapped for Python.

| Library | Licence | Role | Caveat |
|---|---|---|---|
| GDAL/OGR | MIT | raster/vector I/O, warping, DEM tools | default resampling is nearest; set `-r` deliberately |
| PROJ | MIT | CRS operations, grids | grid availability decides accuracy; check `projinfo` pipelines |
| PDAL | BSD | point-cloud I/O and filters | pipelines are JSON; no GUI |
| GMT/PyGMT | LGPL | gridding, grid math, maps | `surface` tension and registration must be stated |
| rasterio/xarray | BSD/Apache | Python grids | chunking and NoData handling are the user's job |
| terra/sf/lidR | GPL | R raster, vector, lidar | lidR memory use scales with catalog design |

## 71.3 GNSS/INS processing

Trajectory quality bounds everything downstream ([Chapter 12](ch12-gnss.md), [Chapter 13](ch13-imu-ins.md)). Open-source GNSS processing is strong at the receiver level and weak at the tightly coupled GNSS/INS level. **RTKLIB** (BSD-2; Takasu) does RTK, PPK, and PPP for multi-constellation data and is the reference open implementation, with active forks (rtklibexplorer's demo5) improving ambiguity resolution. **PRIDE PPP-AR** (GPL; Wuhan University) delivers ambiguity-fixed PPP; **gnssrefl** (GPL; Larson) handles GNSS reflectometry for water and snow heights. **GAMIT/GLOBK** (from MIT the institution, not under the MIT licence; free for academic and government use, source provided) and **Bernese** (University of Bern, licensed) are the geodetic network packages; **GipsyX** (JPL, licensed through Caltech, free for research) is the PPP engine behind many reference solutions. Commercial trajectory software is where loosely and tightly coupled GNSS/INS with lidar-grade smoothing lives: **Applanix POSPac MMS** (Trimble), **NovAtel Inertial Explorer** (Hexagon), **Trimble Business Center**, and **Leica Infinity**; most airborne lidar and mobile-mapping systems are processed in one of the first two, and their trajectories are an input you will rarely be able to reproduce independently — so archive them. Free online services — NGS **OPUS**, NRCan **CSRS-PPP**, Geoscience Australia **AUSPOS** — provide authoritative static positions for control and checkpoints.

| Tool | Licence | Task | Caveat |
|---|---|---|---|
| RTKLIB (+demo5) | BSD-2 | RTK/PPK/PPP | tune ambiguity settings; no tight INS coupling |
| PRIDE PPP-AR | GPL | PPP-AR | needs products from Wuhan/IGS |
| GAMIT/GLOBK | free academic | networks, velocities | Fortran/C, Unix; learning curve |
| POSPac / Inertial Explorer | commercial | GNSS/INS for lidar/MMS | opaque; archive trajectory and SBET |
| OPUS / CSRS-PPP / AUSPOS | free service | static control | returns depend on observation length; read the report |

## 71.4 Lidar

**PDAL** is the open backbone: readers and writers, ground filters (SMRF, PMF, CSF), HAG, outlier removal, reprojection, COPC/EPT output, and a pipeline format that doubles as a provenance record. **LAStools** (rapidlasso; Isenburg) is *mixed*: `laszip`, `las2las`, `lasinfo`, and a few others are LGPL, while the processing tools (`lasground`, `lasclassify`, `lasheight`, `blast2dem`) are closed and licensed — and unlicensed use adds deliberate noise to outputs, which has bitten more than one unwary user. **lidR** (GPL-3; Roussel et al. 2020) is the research standard for forestry and ALS analysis in R; **CloudCompare** (GPL; Girardeau-Montaut) is the universal viewer/editor with M3C2, ICP registration, and subsampling; **Open3D** (MIT) supplies registration and geometry primitives in Python/C++; **WhiteboxTools** (MIT; Lindsay) has fast lidar tools alongside its terrain analysis; **FUSION** (US Forest Service; free, closed) remains common in forestry; **OpenTopography** runs open pipelines (PDAL, GDAL, points2grid) as a service over public data. On the commercial side, **TerraSolid** (TerraScan, TerraMatch, TerraModeler; MicroStation/Spatix-hosted) is the production standard for strip adjustment and classification; **LP360** (GeoCue) and GeoCue's pipelines are common in US production; **Trimble RealWorks** and **Leica Cyclone** serve terrestrial scanning; **Riegl RiPROCESS/RiPRECISION** and **Teledyne Optech LMS** are the sensor vendors' required first stages; **Global Mapper** with the Lidar Module is the affordable generalist. Bathymetric lidar is vendor-locked at the waveform stage — **Leica (formerly AHAB) Chiroptera/HawkEye** LSS, **Riegl VQ-880-G** processing in RiHYDRO — before data reach generic tools ([Chapter 19](ch19-bathymetric-lidar.md)).

| Tool | Licence | Strength | Caveat |
|---|---|---|---|
| PDAL | BSD | scriptable, format-complete, provenance | no interactive editing |
| LAStools | mixed (LGPL/closed) | fast, battle-tested | closed tools degrade output without licence |
| lidR | GPL-3 | forestry, research, catalogs | R memory model |
| CloudCompare | GPL | inspection, M3C2, registration | GUI-first; CLI limited |
| WhiteboxTools | MIT | fast lidar + terrain tools | single-maintainer lineage; check status |
| TerraSolid | commercial | strip adjustment, production classification | MicroStation/Spatix dependency; opaque |
| LP360 / GeoCue | commercial | US production QA | Windows; project-file lock-in |

## 71.5 Photogrammetry and SfM

Open photogrammetry became production-grade in the 2010s. **MicMac** (IGN France; CeCILL-B; Rupnik et al. 2017) is the most rigorous — full bundle adjustment with camera models, GCP uncertainty handling, and dense matching — and the hardest to learn. **COLMAP** (BSD; Schönberger and Frahm 2016) is the computer-vision reference for SfM and multi-view stereo and underlies many pipelines; **OpenMVS** (AGPL) densifies; **Meshroom/AliceVision** (MPL-2) is the node-graph GUI; **OpenDroneMap/WebODM** (AGPL) packages the stack for drone mapping with GCPs and georeferenced outputs. For satellite stereo, NASA's **Ames Stereo Pipeline** (Apache 2.0; Beyer et al. 2018) ⟨H⟩ handles pushbroom sensors with RPCs and rigorous models, bundle adjustment, and DEM alignment, and is the open engine behind much planetary and polar work; **SETSM** (Noh and Howat) produced ArcticDEM and REMA ([Chapter 55](ch55-public-products.md)). Commercially, **Agisoft Metashape** dominates small- and medium-project SfM for its price and usability; **Pix4D** (Pix4Dmapper, Pix4Dmatic) competes in drone mapping; **Bentley iTwin Capture Modeler** (formerly ContextCapture) and **RealityCapture** (Epic; free below a revenue threshold since 2024) lead large urban mesh production; **DJI Terra** is tied to DJI hardware; **Trimble Inpho**, **SimActive Correlator3D**, **BAE SOCET GXP**, and **Hexagon ERDAS IMAGINE** are the traditional aerial-photogrammetry production systems ([Chapter 22](ch22-photogrammetry-sfm.md)).

| Tool | Licence | Strength | Caveat |
|---|---|---|---|
| MicMac | CeCILL-B | rigorous adjustment, uncertainty | steep learning curve |
| COLMAP + OpenMVS | BSD / AGPL | reference SfM/MVS | georeferencing is on you |
| OpenDroneMap | AGPL | end-to-end drone mapping | dense matching quality lags commercial |
| Ames Stereo Pipeline | Apache 2.0 | satellite/planetary stereo | command-line; many parameters |
| Metashape | commercial | usability, price, scripting API | reports accuracy on GCPs unless told to use checkpoints |
| Pix4D / iTwin Capture / RealityCapture | commercial | drone workflows / large meshes | subscription; cloud-tied features |

<!-- figure: Figure 71.2 — Dependency diagram: PROJ → GDAL/OGR and GEOS → PDAL, rasterio, QGIS, GRASS, and (embedded) ArcGIS, Global Mapper, CARIS, Qimera; showing the open core beneath open and closed applications. -->

## 71.6 Sonar and hydrography

**MB-System** (GPL; Caress and Chayes, 1993–; MBARI/LDEO) ⟨H⟩ is the open reference for multibeam and sidescan processing — format conversion for dozens of sonar formats, navigation and attitude editing, sound-speed and tide correction, the `mbeditviz` 3D editor, and gridding with `mbgrid`/`mbmosaic` — and it remains the only fully open path from raw multibeam to a validated grid ([Chapter 20](ch20-sonar.md)). NOAA's **HydrOffice** suite (QC Tools, Sound Speed Manager; LGPL) and **Pydro** (free) implement HSSD checks and NOAA field workflows; NOAA's **Kluster** (open) is a newer Python multibeam processor built on xarray/dask; **OpenSidescan** (open) handles sidescan mosaics; **OpenCPN** (GPL) is the open chart plotter. The commercial market is concentrated: **CARIS HIPS and SIPS** (Teledyne) with **BASE Editor** and **HPD** for the survey-to-chart chain; **QPS Qinsy** (acquisition), **Qimera** (processing, with CUBE and TPU), and **Fledermaus** (4D visualization); **Hypack/Hysweep** (Xylem) for single-beam and small-boat multibeam; **EIVA NaviSuite** and **Teledyne PDS** for offshore and dredging; **BeamworX** for acquisition and processing; **SonarWiz** (Chesapeake Technology) for sidescan and sub-bottom; and **Kongsberg SIS** as the acquisition front-end tied to Kongsberg sonars. Hydrographic offices and most contractors process in CARIS or Qimera, which means that reproducing an official survey independently almost always means MB-System on the raw files.

| Tool | Licence | Strength | Caveat |
|---|---|---|---|
| MB-System | GPL | full open multibeam chain; many formats | command-line; GUI editors dated |
| HydrOffice / Pydro / Kluster | LGPL / free / open | HSSD QC, NOAA workflows | NOAA-centric conventions |
| CARIS HIPS/SIPS | commercial | production standard, charting chain | project formats closed; costly |
| QPS Qimera / Fledermaus | commercial | usable processing, CUBE, 4D viz | subscription; hardware keys |
| Hypack / EIVA / PDS | commercial | acquisition, dredging, offshore | acquisition-tied; mixed export fidelity |

## 71.7 Radar and InSAR

**ISCE2** (Apache 2.0; NASA/JPL) is the reference open InSAR processor for Sentinel-1, ALOS, and others, with stripmap and TOPS workflows; **GMTSAR** (GPL; Sandwell et al.) builds on GMT; ESA's **SNAP** with the Sentinel-1 Toolbox (GPL) is the accessible GUI/graph-processing route and the standard for Sentinel-1 preprocessing; **MintPy** (GPL; Yunjun et al. 2019) and **LiCSBAS** (GPL) do time-series (SBAS) analysis on stacks from ISCE/GAMMA/LiCSAR; **pyroSAR** (MIT) and **Doris** (GPL; TU Delft, historic) round out the open set ([Chapter 21](ch21-radar-sar-insar.md), [Chapter 38](ch38-plate-motion-and-vlm.md)). **GAMMA** (GAMMA Remote Sensing) is the commercial standard in research and service provision for its rigor and sensor coverage; **SARscape** (L3Harris, within ENVI) serves GIS-oriented users; **TRE Altamira** (CLS) and similar firms sell processed PSI/SBAS products rather than software. DEM generation from InSAR (TanDEM-X-style bistatic) is mostly agency-internal; what the practitioner gets is ground motion.

| Tool | Licence | Strength | Caveat |
|---|---|---|---|
| ISCE2 | Apache 2.0 | reference processor; TOPS | build complexity; many compiled dependencies |
| SNAP S1TBX | GPL | accessible; standard preprocessing | memory-hungry; graph reproducibility needs care |
| GMTSAR | GPL | GMT integration; simple stacks | fewer sensors |
| MintPy / LiCSBAS | GPL | time series | quality depends on input stack |
| GAMMA | commercial | rigor, sensor breadth | licence cost; scripts not portable |

## 71.8 Geodesy and datums

The datum problem is a software-availability problem as much as a geodetic one ([Chapter 9](ch09-vertical-datums.md)). **PROJ** with **PROJ-data** performs grid-based horizontal and vertical transformations wherever the grids are published under open terms — and many national geoid and datum grids were not, until the PROJ-data effort and the EU high-value-datasets regulation ([Chapter 68](ch68-legal-issues.md)) pushed agencies to release them; where a grid is missing, PROJ silently falls back to a less accurate operation unless you check `projinfo` and `PROJ_NETWORK`. NOAA's **VDatum** (free, closed; Java) transforms among tidal, orthometric, and ellipsoidal datums in US coastal waters with published uncertainties; **vyperdatum** (NOAA; open) wraps VDatum grids through PROJ for pipelines; NGS's **HTDP** (free; Fortran source available) handles time-dependent horizontal positions and will be superseded by the NSRS modernization tools; NGS **GEOID18/xGEOID** models and **NCAT** convert heights and coordinates; **GeographicLib**'s GeoidEval (MIT) evaluates EGM96/EGM2008. Commercial systems ship their own transformation libraries (Esri's projection engine, Blue Marble's GeoCalc, Trimble's), which sometimes implement national grids earlier than PROJ and sometimes implement them differently — a source of centimetre-to-decimetre discrepancies between tools that is invisible until you test a round trip.

## 71.9 DEM analysis and hydrology

**GRASS GIS** (US Army CERL, developed from 1982 and released 1984; GPL; OSGeo) ⟨H⟩ has the deepest terrain toolbox — `r.watershed`, `r.terraflow`, `r.sim.water`, `r.geomorphon`, `r.param.scale` — and a stable, scriptable, topologically careful design; **SAGA GIS** (GPL) is the morphometry specialist (dozens of terrain indices, TPI, MRVBF, wetness); **WhiteboxTools** (MIT) is fast and broad with excellent hydrological conditioning (breaching, depression filling) and lidar tools; **TauDEM** (GPL; Tarboton) is the parallel flow-routing standard (D∞); **RichDEM** (GPL; Barnes) provides fast depression-filling and flow algorithms as a library; **LSDTopoTools** (GPL; Edinburgh) and **TopoToolbox** (MATLAB, with a Python successor) serve geomorphology (channel steepness, chi analysis); **Landlab** (MIT) is the landscape-evolution modelling framework; **xdem** (Apache 2.0; GlacioHack) focuses on DEM coregistration, bias correction, and uncertainty ([Chapter 41](ch41-change-detection.md), [Chapter 53](ch53-accuracy-assessment.md)); **QGIS** (2002–; GPL; OSGeo) ⟨H⟩ fronts GRASS, SAGA, WhiteboxTools, and GDAL through its Processing framework and is the universal desktop ([Chapter 61](ch61-hydrology.md)). Commercially, **ArcGIS Pro** with **Spatial Analyst** and **Arc Hydro** is the institutional standard in US agencies; **Global Mapper** is the affordable generalist with surprising depth in terrain and volume tools; **Surfer** (Golden Software) remains popular for gridding and contouring in geoscience; **RiverTools** (Rivix) is a hydrology specialist.

| Tool | Licence | Strength | Caveat |
|---|---|---|---|
| GRASS GIS | GPL | depth, stability, scripting | location/mapset model confuses newcomers |
| SAGA | GPL | morphometric indices | GUI-centric; CLI verbose |
| WhiteboxTools | MIT | speed; hydro-conditioning | check maintenance status; some tools in paid extension |
| TauDEM / RichDEM | GPL | flow routing at scale | TauDEM needs MPI |
| xdem | Apache 2.0 | coregistration, uncertainty | young API; moving fast |
| QGIS | GPL | integration, cartography | plugin quality varies |
| ArcGIS Pro / Spatial Analyst | commercial | institutional, Arc Hydro | licence tiers; default resampling and NoData handling differ from GDAL |

## 71.10 Change detection and validation

Validation tooling has consolidated around a few open packages. **xdem** implements Nuth–Kääb and ICP coregistration, deramping, terrain-bias correction, and spatial-statistics-based uncertainty (variograms, effective sample size); **demcoreg** (MIT; Shean) is the lighter predecessor used for ArcticDEM/REMA alignment; **py4dgeo** (MIT; Heidelberg) and **CloudCompare's M3C2** implement point-cloud distance with per-point uncertainty and significance; the **Geomorphic Change Detection** (GCD) software (Riverscapes; free/open) implements DoD with spatially variable error and thresholding; **MICRODEM** (Guth; free) and the **DEMIX** tools provide standardized DEM intercomparison; PDAL and GDAL handle the plumbing. Commercial counterparts are **TerraMatch** (strip adjustment and calibration), **Leica Cyclone 3DR**, and **Trimble RealWorks** for scan-to-scan comparison ([Chapter 41](ch41-change-detection.md), [Chapter 53](ch53-accuracy-assessment.md)).

## 71.11 Machine learning

ML for elevation sits on general frameworks: **PyTorch** (BSD) and **TensorFlow** (Apache 2.0) with **scikit-learn** (BSD) for classical methods. Geospatial layers above them: **TorchGeo** (MIT; Microsoft) for datasets, samplers, and pretrained models aware of CRS and tiles; **Raster Vision** (Apache 2.0; Azavea/Element 84) for end-to-end raster pipelines; **segment-geospatial** (MIT) wrapping SAM for imagery; **Open3D-ML** and **Pointcept** (MIT) for point-cloud semantic segmentation (RandLA-Net, KPConv, PointTransformer). Closed alternatives are Esri's deep-learning toolset in ArcGIS Pro (pretrained models for building footprints, ground classification), Trimble **eCognition** (object-based image analysis), and the cloud vendors' managed ML. The reproducibility and validation problems of [Chapter 43](ch43-traditional-vs-ml.md) apply with force: pin framework versions and random seeds, archive weights and training-data manifests with licences ([Chapter 68](ch68-legal-issues.md)), and validate against held-out *geographies*, not held-out tiles.

## 71.12 Visualization and cartography

**QGIS** and **GMT** cover most published maps; **Blender** (GPL) has become a serious terrain renderer (BlenderGIS, displacement shading) for hillshade-quality work; the **Relief Visualization Toolbox** (RVT; Apache 2.0; ZRC SAZU) implements sky-view factor, openness, local dominance, and multi-directional hillshade for archaeology and geomorphology ([Chapter 57](ch57-visualizing-dems.md)). For the web and point clouds: **Potree** (BSD-2) and its successors render billions of points in the browser; **CesiumJS** (Apache 2.0) with 3D Tiles and quantized-mesh terrain; **deck.gl** (MIT) and **MapLibre GL** (BSD-3) for terrain and raster-DEM tiles; **three.js** (MIT) underneath many of them. For colour, **cmcrameri** (MIT; Crameri's scientific colour maps) should replace rainbow palettes in every elevation figure ([Chapter 58](ch58-making-maps.md)). Closed tools: **Eduard** (Jenny; macOS) for shaded relief of exceptional quality; **ArcGIS Pro** and **Global Mapper** for production cartography; **Fledermaus** for bathymetric 4D scenes; **Surfer** for contour maps; **Terragen** for photorealistic rendering.

## 71.13 Data management and catalogs

The cloud-native stack is open end to end ([Chapter 51](ch51-finding-data.md), [Chapter 47](ch47-file-formats.md)): **pystac** and **stac-fastapi** (Apache 2.0) for STAC catalogs and APIs; **Entwine** (LGPL) and **COPC** for cloud-optimized point clouds; **TiTiler** (MIT) for dynamic COG tiling; **GeoServer** (GPL) and **MapServer** (MIT) for OGC services; **PostGIS** (GPL) with its raster and point-cloud extensions; **DuckDB spatial** (MIT) for analytical queries over GeoParquet; **GeoNetwork** (GPL) and **pycsw** (MIT) for ISO 19115 metadata catalogs; **CKAN** (AGPL) for open-data portals. Closed: **ArcGIS Enterprise/Portal** and **Image Server**, commercial digital-asset-management systems, and vendor data lakes — where the lock-in is the metadata model rather than the file format.

## 71.14 Planetary

**ISIS** (USGS Astrogeology; public domain/CC0) handles mission sensor models, calibration, and control for planetary imagery; **Ames Stereo Pipeline** produces DEMs from it; NAIF's **SPICE** toolkit (public) supplies geometry; **JMARS** (ASU; free) is the planetary GIS viewer; the **Community Sensor Model** (CSM) standard and USGS's **ALE/Knoten** make sensor models portable. Closed: **BAE SOCET GXP/SET** with planetary sensor models, long the production system for lunar and Martian DTMs ([Chapter 67](ch67-planetary-dems.md)).

## 71.15 Cloud platforms

**Google Earth Engine** (started 2009, public 2010; Gorelick et al. 2017) ⟨H⟩ hosts petabytes of public imagery and DEMs with a server-side array API; it is free for non-commercial research and education and licensed commercially since 2022, and it is *closed*: your code runs on Google's engine and cannot run anywhere else. **Microsoft Planetary Computer** provides STAC catalogs of open data on Azure (its hosted Hub was retired in 2024; the catalog remains); **AWS Open Data** hosts 3DEP, Copernicus DEM, ArcticDEM, and others as COGs and COPC, queryable with any open tool; **Copernicus Data Space Ecosystem** (2023–) serves Sentinel data with openEO and STAC APIs. The reproducibility calculus differs by platform: on open-data buckets with open tools, a pipeline is portable; on Earth Engine, the *results* are reproducible only while the platform exists and the API is unchanged, and the *method* is reproducible elsewhere only if you re-implement it. Record the platform, asset IDs, and dates in every provenance log, and export intermediate products you cannot regenerate.

## 71.16 Choosing and governing software

**Validate software like data.** For each critical operation, maintain a benchmark: a small dataset with a known answer (a synthetic DEM with analytic slopes; a point cloud with surveyed checkpoints; a grid in one CRS and its transformed twin computed by an independent tool) and a test that runs on every version change. **Round trips** are the cheapest tests: read–write–read a LAS 1.4 file and diff the headers and extra bytes; project a grid and back and measure the residual; export a BAG and check that the uncertainty layer survived. Half-cell shifts from pixel-is-area versus pixel-is-point conventions, silent resampling defaults (nearest in GDAL, bilinear in some GUIs), NoData promotion, and differing geoid grids are the usual discoveries ([Chapter 10](ch10-projections-and-resampling.md), [Chapter 31](ch31-interpolation-and-gridding.md)).

**Pin and reproduce.** Record exact versions (`gdalinfo --version`, `pdal --version`, `pip freeze`, `conda list --explicit`); build environments with conda/mamba, pixi, or containers from lock files; archive the container image with the project. Unpinned environments change results — PROJ grid updates alone shift heights by centimetres.

**Comply with licences.** Copyleft (GPL/AGPL) matters if you redistribute or offer the software as a service; permissive licences require attribution; commercial EULAs restrict seats, sites, and sometimes *export* (some vendor tools cannot legally be used in embargoed countries or by foreign nationals). Keep a software bill of materials (SPDX) beside the data BOM of [Chapter 68](ch68-legal-issues.md).

**Plan for longevity.** Ask: who maintains it, who pays them, what happens if the company is acquired or the maintainer retires, can I read my project files without the software, and is there an export to an open format for every object type? A tool that has answered these badly in the past — the field has watched formats orphaned by acquisitions — should hold raw data only in open formats.

**When to buy.** Buy when the commercial tool delivers a validated capability you cannot reproduce (tightly coupled trajectory processing, sensor-specific waveform processing, production strip adjustment at scale), when support with a service-level agreement is worth the price, or when your institution's auditors require a vendor to hold accountable. Do not buy to avoid learning; do not buy a GUI for a step that belongs in a pipeline; and never buy without an exit: raw data in open formats, products in open formats, and the open path of the rule of thumb above tested at least once.

> **Try it.** A round-trip test that catches half-cell registration shifts and resampling surprises between two tools. Expected outcome: a residual grid whose mean is ≈ 0 and whose 95th-percentile |residual| is ≪ the DEM's stated accuracy; a mean offset of half a cell times the local slope indicates a pixel-is-point/area mismatch.

```bash
# Reproject with GDAL (bilinear) and back, then compare to the original.
gdalwarp -t_srs EPSG:32610 -r bilinear -tr 1 1 dem_utm11.tif tmp_utm10.tif
gdalwarp -t_srs EPSG:32611 -r bilinear -tr 1 1 -te $(gdalinfo -json dem_utm11.tif \
   | python3 -c "import json,sys;b=json.load(sys.stdin)['cornerCoordinates'];print(*b['lowerLeft'],*b['upperRight'])") \
   tmp_utm10.tif roundtrip.tif
gdal_calc.py -A dem_utm11.tif -B roundtrip.tif --calc="A-B" --outfile=resid.tif --NoDataValue=-9999
gdalinfo -stats resid.tif | grep -E "MEAN|STDDEV"
gdalinfo dem_utm11.tif | grep -i AREA_OR_POINT     # must match the other tool's assumption
```

Repeat with the second tool (QGIS GUI export, ArcGIS Project Raster, Global Mapper) producing `roundtrip.tif`, and compare the statistics. A systematic difference between tools that disappears when `AREA_OR_POINT` is forced consistent is the half-cell bug.

<!-- figure: Figure 71.1 — Task-by-licence matrix: rows are task areas (71.2–71.15), columns are open / free-closed / commercial, cells name the leading tools; shading indicates where an open path is complete, partial, or missing (tightly coupled GNSS/INS, bathymetric-lidar waveform processing). -->

## Then & now

The first terrain software was institutional and mainframe-bound: Harvard's **SYMAP** (1960s) printed choropleths and surfaces on line printers; **GRASS** (1984) ⟨H⟩ gave the US Army a raster GIS that became the first widely used open one; **ARC/INFO** (1982) ⟨H⟩ made Esri the institutional default. The 1990s brought desktop GIS and the vendor suites that still dominate production — CARIS, TerraSolid, SOCET SET, ERDAS — each with its own project formats. The decisive change was the emergence of **open libraries as shared substrate**: PROJ's lineage from the 1980s, **GDAL in 2000** ⟨H⟩, GEOS (2001), and **PDAL (2011–)**, which every commercial package now embeds, so that "open versus closed" became a question about the application layer over a common open core. The 2010s added **cloud-native** formats and notebook workflows (COG, COPC, STAC, Zarr; Jupyter; Earth Engine in 2010 ⟨H⟩), and the 2020s added ML frameworks and foundation models. The open/closed boundary keeps moving in both directions: HEC-RAS and VDatum are free and closed; LAStools is half and half; RealityCapture became free for small users; Earth Engine went commercial; SNAP and ISCE opened agency code; and the EU's high-value-datasets regulation is opening the geoid and datum grids that PROJ needs. The tendency is toward an open core with closed, specialized, sensor-tied edges — exactly where the validation risk now concentrates.

## Validation & uncertainty

Software is a source of error like any sensor, and it should be characterized like one. Five mechanisms account for most tool-induced discrepancies in elevation work.

**Registration conventions.** Pixel-is-area versus pixel-is-point (`AREA_OR_POINT` in GeoTIFF; gridline versus pixel registration in GMT and NetCDF) shift a grid by half a cell when tools disagree — 0.5 m at 1 m posting, which on a 10° slope is a 9 cm height error, systematically. Test: round-trip a grid between the two tools and regress the residual against slope components; a non-zero coefficient is the shift.

**Resampling and interpolation defaults.** GDAL defaults to nearest neighbour; many GUIs default to bilinear or cubic; gridding tools differ in kernel, search radius, and tension. Resampling a 1 m DEM to 5 m by averaging versus by nearest neighbour changes slope statistics by tens of percent and volumes by amounts proportional to curvature. Test: resample a synthetic surface with known analytic properties and compare; require that the method be recorded in metadata.

**Coordinate operations.** Tools pick different transformation paths for the same CRS pair — a Helmert versus a grid, one grid version versus another, a hybrid geoid versus a gravimetric one — and differ by centimetres to decimetres vertically. `projinfo -s EPSG:A -t EPSG:B --spatial-test intersects` lists the candidates and their accuracies; compare a sample of points through both tools and treat the difference as a tool uncertainty component until resolved.

**Numerical and version drift.** New versions change algorithms (PDAL's SMRF parameters, GDAL's warping kernel handling of NoData, PROJ's grid updates), so results drift without any change in your code. Test: a frozen benchmark run on each upgrade, with a tolerance tied to the product's accuracy.

**Silent degradation and silent success.** Unlicensed LAStools adds noise; some tools silently drop extra bytes, waveform packets, or the BAG uncertainty layer; GUI exports silently change NoData values or data type. Test: byte-level and header-level round trips; count attributes before and after.

> **Worked example.** *Two tools, one DEM, a 7 cm argument.* Two offices computed the mean height of 40 checkpoints against the same 1 m DTM and disagreed by 7.1 cm. Office A used GDAL (`gdallocationinfo`, pixel-is-area, nearest cell); Office B used a GUI that bilinearly interpolated and treated the file as pixel-is-point. Regressing B−A residuals against the DTM's east–west slope gave a coefficient of 0.49 m (≈ half a cell) with $R^2$ = 0.83; mean slope at the checkpoints was 8 % east-facing, so $0.49 \times 0.08 \approx 0.04$ m, with the remaining ~3 cm attributable to bilinear versus nearest sampling on the same slopes. Neither tool was wrong; the convention was undocumented. The fix was to state `AREA_OR_POINT=Area`, use bilinear sampling in both, and add "sampling method and registration" to the acceptance report template.

> **Uncertainty budget.** Tool-induced vertical discrepancy components observed in round-trip tests on a 1 m DTM (illustrative magnitudes from practice; measure your own):
>
> | Component | Typical magnitude | How detected |
> |---|---|---|
> | Half-cell registration mismatch | 0.5 cell × slope (≈ 0.04 m at 8 %) | slope regression of residuals |
> | Nearest vs bilinear sampling | 0.01–0.05 m on slopes | repeat with both methods |
> | Geoid/grid version difference | 0.01–0.10 m, systematic | `projinfo`; point sample through both |
> | Datum path (Helmert vs grid) | 0.05–1 m horizontal → height via slope | list operations; force grid |
> | NoData/data-type coercion | gross (−9999 → 0) or ±0.5 unit rounding | histogram of residuals; header diff |

## Software

This chapter is the catalogue; [Appendix F](../appendices/appendix-f-software-index.md) gives the sortable table (name, task, licence, language, formats, maintainer, last release, notes). For the environment itself: **conda-forge/mamba** and **pixi** provide reproducible installs of GDAL, PDAL, PROJ, and the Python stack with lock files; **Docker/Podman** images (OSGeo's `gdal` images, `pdal/pdal`) freeze complete toolchains; **Nix** offers bit-reproducible builds for the determined. **Free but closed:** vendor viewers and format SDKs (Riegl RiVLib, Kongsberg KMALL libraries) that are sometimes the only readers for proprietary raw formats — archive the SDK version with the data. **Commercial:** environment and pipeline managers from vendors (Esri ArcGIS Pro conda environments, Safe FME for format translation at scale) — caveat: FME and similar translators are excellent and widely used, and their translations should still be round-trip tested like any other.

## Standards & guides

- Open Source Initiative, *The Open Source Definition* and approved licence list — what "open source" means.
- OSGeo, *Project Incubation Criteria* and *Project Graduation Checklist* — governance signals for sustainability.
- OGC Compliance Program — certified implementations of OGC standards (WMS, WCS, GeoTIFF, GeoPackage, API Features, 3D Tiles).
- SPDX Specification (ISO/IEC 5962:2021) — software bill of materials and licence identifiers.
- Chue Hong, N. P., et al., 2022. *FAIR Principles for Research Software (FAIR4RS Principles)*, Research Data Alliance.
- Smith, A. M., Katz, D. S., and Niemeyer, K. E., 2016. Software citation principles. *PeerJ Computer Science*, 2:e86 — how to cite the tools you used.
- ASPRS LAS Specification 1.4 R15 (2019) and COPC 1.0 (2021); OGC GeoTIFF 1.1 (2019); OGC Cloud Optimized GeoTIFF (2023); ONSWG BAG Format Specification (current) — format conformance targets for round-trip tests.
- Conda-forge and pixi documentation on lock files; OCI image specification — reproducible environments.

## Pitfalls

- **Trusting output because the vendor is reputable.** Reputation is not validation → benchmark every critical step against a known answer.
- **Confusing freeware with open source.** Free tools can vanish or change terms → classify by licence; keep an open path.
- **Silently different resampling/registration defaults across tools.** Half-cell shifts and kernel differences → round-trip tests; record `AREA_OR_POINT` and the method.
- **Unpinned versions.** PROJ grids, PDAL filters, and GDAL kernels change → lock files, archived containers, benchmark on upgrade.
- **Using unlicensed LAStools processing tools.** Outputs are deliberately degraded → license them or use PDAL/lidR.
- **GUI-only workflows with no provenance.** Parameters live in nobody's memory → script it, or export the tool's processing log into the project record.
- **Losing data access when a licence lapses.** Project files in closed formats → export every object to open formats at milestones.
- **Assuming a "free" tool has no export or use restrictions.** Some vendor freeware and some government tools do → read the EULA; check export-control clauses.
- **Running a critical transformation in one tool only.** Grid and path choices differ → cross-check a point sample in a second implementation.
- **Treating Earth Engine or other closed platforms as archives.** Results are reproducible only while the platform and API persist → export intermediates; record asset IDs and dates.
- **Picking tools by feature list instead of by format fidelity.** Lost extra bytes, uncertainty layers, or CRS metadata → test the specific formats and attributes you need.
- **Ignoring bus factor.** Single-maintainer tools stall → check commit history, funding, and foundation status before depending on one.

## Key takeaways

- Organize software by task, and for every task know the open path, the free-but-closed options, and the commercial standard — and which of the three your deliverables actually depend on.
- Open libraries (GDAL, PROJ, GEOS, PDAL) are the shared substrate under nearly every tool; the open/closed boundary is at the application layer and keeps moving.
- Freeware is not open source; licence, governance, and foundation status predict longevity better than features do.
- Validate software like data: benchmarks with known answers, round-trip tests, version-pinned environments, and a tolerance tied to the product's accuracy.
- The usual tool-induced errors — half-cell registration, resampling defaults, transformation-path differences, NoData coercion — are systematic, detectable, and avoidable once you test for them.
- Keep provenance machine-readable: versions, parameters, lock files, container images, and asset IDs belong with the data.
- Buy when a validated capability cannot be reproduced or support is worth paying for — never to avoid learning, and never without an exit to open formats.
- Contribute back: bug reports, tests, and documentation to the open tools you depend on are the cheapest insurance against their disappearance.

## References

- Beyer, R. A., Alexandrov, O., and McMichael, S., 2018. The Ames Stereo Pipeline: NASA's open source software for deriving and processing terrain data. *Earth and Space Science*, 5(9):537–548.
- Butler, H., Chambers, B., Hartzell, P., and Glennie, C., 2021. PDAL: An open source library for the processing and analysis of point clouds. *Computers & Geosciences*, 148:104680.
- Caress, D. W. and Chayes, D. N., 1996. Improved processing of Hydrosweep DS multibeam data on the R/V Maurice Ewing. *Marine Geophysical Researches*, 18:631–650.
- Coetzee, S., Ivánová, I., Mitasova, H., and Brovelli, M. A., 2020. Open geospatial software and data: a review of the current state and a perspective into the future. *ISPRS International Journal of Geo-Information*, 9(2):90.
- Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., and Moore, R., 2017. Google Earth Engine: planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment*, 202:18–27.
- Lindsay, J. B., 2016. Whitebox GAT: a case study in geomorphometric analysis. *Computers & Geosciences*, 95:75–84.
- Neteler, M., Bowman, M. H., Landa, M., and Metz, M., 2012. GRASS GIS: a multi-purpose open source GIS. *Environmental Modelling & Software*, 31:124–130.
- Noh, M.-J. and Howat, I. M., 2015. Automated stereo-photogrammetric DEM generation at high latitudes: Surface Extraction with TIN-based Search-space Minimization (SETSM) validation and demonstration over glaciated regions. *GIScience & Remote Sensing*, 52(2):198–217.
- Rosen, P. A., Gurrola, E., Sacco, G. F., and Zebker, H., 2012. The InSAR Scientific Computing Environment. *Proceedings of EUSAR 2012*, 730–733.
- Roussel, J.-R., Auty, D., Coops, N. C., et al., 2020. lidR: an R package for analysis of airborne laser scanning (ALS) data. *Remote Sensing of Environment*, 251:112061.
- Rupnik, E., Daakir, M., and Pierrot-Deseilligny, M., 2017. MicMac — a free, open-source solution for photogrammetry. *Open Geospatial Data, Software and Standards*, 2:14.
- Sandwell, D., Mellors, R., Tong, X., Wei, M., and Wessel, P., 2011. Open radar interferometry software for mapping surface deformation. *Eos, Transactions AGU*, 92(28):234.
- Schönberger, J. L. and Frahm, J.-M., 2016. Structure-from-motion revisited. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 4104–4113.
- Shean, D. E., Alexandrov, O., Moratto, Z. M., Smith, B. E., Joughin, I. R., Porter, C., and Morin, P., 2016. An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very-high-resolution commercial stereo satellite imagery. *ISPRS Journal of Photogrammetry and Remote Sensing*, 116:101–117.
- Smith, A. M., Katz, D. S., and Niemeyer, K. E., 2016. Software citation principles. *PeerJ Computer Science*, 2:e86.
- Steiniger, S. and Hunter, A. J. S., 2013. The 2012 free and open source GIS software map — a guide to facilitate research, development, and adoption. *Computers, Environment and Urban Systems*, 39:136–150.
- Takasu, T. and Yasuda, A., 2009. Development of the low-cost RTK-GPS receiver with an open source program package RTKLIB. *Proceedings of the International Symposium on GPS/GNSS*, Jeju, Korea.
- Warmerdam, F., 2008. The Geospatial Data Abstraction Library. In: Hall, G. B. and Leahy, M. G. (eds.), *Open Source Approaches in Spatial Data Handling*. Berlin: Springer, 87–104.
- Wessel, P., Luis, J. F., Uieda, L., Scharroo, R., Wobbe, F., Smith, W. H. F., and Tian, D., 2019. The Generic Mapping Tools version 6. *Geochemistry, Geophysics, Geosystems*, 20(11):5556–5564.
- Yunjun, Z., Fattahi, H., and Amelung, F., 2019. Small baseline InSAR time series analysis: unwrapping error correction and noise reduction. *Computers & Geosciences*, 133:104331.
- Zahs, V., Winiwarter, L., Anders, K., et al., 2022. Correspondence-driven plane-based M3C2 for lower uncertainty in 3D topographic change quantification. *ISPRS Journal of Photogrammetry and Remote Sensing*, 183:541–559. (the method behind py4dgeo)
- xdem contributors (GlacioHack), 2024. *xdem: Analysis of digital elevation models (DEMs)*. Software, versioned releases archived on Zenodo; documentation at xdem.readthedocs.io.

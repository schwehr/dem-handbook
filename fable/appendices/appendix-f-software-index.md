# Appendix F — Software index

This index lists software referred to throughout the handbook, grouped by the task it is most often used for. It complements the prose survey in [Chapter 71](../chapters/ch71-software-landscape.md), which discusses *how to choose*; this appendix only answers *what exists*. Rows are alphabetical within each group. The "Chapters" column points to where the tool is used or discussed.

**Reading the Licence column.** OSI identifiers are used for open source (MIT, BSD-3, Apache-2.0, GPL-2.0/3.0, LGPL-2.1/3.0, MPL-2.0). "Freeware" means gratis but closed. "Commercial" means paid, closed; "Commercial (free tier)" where a limited free edition exists. Licences change — LAStools, for example, is a mixture of LGPL tools and closed tools — so check the current licence file before redistributing or embedding. "(verify)" marks entries whose licence or status could not be confirmed at the time of writing.

**Reading the Platform column.** "CLI" means command line; "GUI" a desktop application; "lib" a library; "web" browser-based. Language indicates the implementation language and, where relevant, the primary binding (e.g. "C++ / Python").

## F.1 Foundations: geospatial libraries and coordinate operations

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| GDAL/OGR | Raster and vector I/O, warping, DEM utilities (`gdaldem`, `gdalwarp`, `gdal_translate`, `gdalbuildvrt`) | MIT (X/MIT) | C++ / CLI, Python, R, Java bindings | The substrate under almost every open and many commercial tools; vertical-CRS transforms depend on PROJ grids | 10, 31, 47, 48 |
| PROJ | Coordinate transformations incl. vertical (geoid grids via PROJ-data / CDN) | MIT | C++ / lib, CLI (`cs2cs`, `projinfo`) | Transformation pipelines; time-dependent transforms (`+t_epoch`); grid download on demand | 8, 9, 10, 38 |
| GEOS | 2D geometry engine (predicates, overlays) | LGPL-2.1 | C++ / lib | Underlies PostGIS, Shapely, QGIS geometry | 59 |
| Shapely / pyproj / rasterio / fiona | Pythonic wrappers for GEOS/PROJ/GDAL | BSD-3 | Python | The usual Python stack for scripted DEM QA | 31, 53, 59 |
| GeoPandas / xarray / rioxarray | DataFrame and labelled-array geospatial analysis | BSD-3 | Python | rioxarray handles CRS/transform on DEM stacks; dask for scale | 48, 53 |
| terra / sf / stars (R) | Raster, vector, data cubes in R | GPL-3.0 (terra, stars), GPL-2.0/MIT (sf) | R | terra replaced raster; `terrain()` for slope/aspect | 44, 53 |
| HTDP | Time-dependent horizontal/vertical coordinate transformation (NAD83 epochs, ITRF) | Public domain (US NGS) | Fortran / CLI, web | Models plate motion and coseismic deformation in the US | 8, 38, 39 |
| VDatum | Vertical datum transformation (US tidal, orthometric, ellipsoidal) | Public domain (NOAA) | Java / GUI, CLI | Includes separation-model uncertainty; US coastal waters only | 9, 34, 62 |
| vyperdatum | Pythonic VDatum-grid application for hydrographic pipelines | CC0-1.0 (NOAA) | Python | Used by NOAA NBS workflows | 9, 62 |
| NGS GEOID tools (GEOID18, xGEOID, GEOCON) | Geoid undulation / datum conversion in the US | Public domain | Fortran / web | NAPGD2022 will replace GEOID18 | 7, 9 |
| GeographicLib | Geodesics, geoid, magnetic and gravity models | MIT | C++ / Python, JS | `GeoidEval` for EGM96/2008 undulations | 7, 9 |
| ICGEM calculation service | Gravity field / geoid heights from global models | Free (web service) | web | Compute N for any model (EGM2008, XGM2019e…) | 7 |

## F.2 Point-cloud processing (lidar, photogrammetric, sonar)

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| PDAL | Point-cloud pipelines: filters, classification (SMRF, PMF, CSF), gridding (`writers.gdal`), COPC/EPT | BSD-3 | C++ / CLI, Python | JSON pipelines; the open equivalent of a lidar workbench | 29, 30, 31, 47 |
| LAStools | Lidar processing suite (`lasground`, `lasheight`, `lasclassify`, `blast2dem`) | Mixed: some LGPL-2.1 (LASlib, `las2las`, `laszip`), most tools commercial | C++ / CLI, Windows (Wine on Linux) | Very fast; licence restrictions on unlicensed use (added noise) | 30, 31 |
| LASzip / laz-perf | LAZ compression | LGPL-2.1 / Apache-2.0 | C++ / lib, JS | LAZ 1.4 is the de facto archive format | 47 |
| laspy | LAS/LAZ reading and writing | BSD-2 | Python | With `lazrs` backend | 47 |
| lidR | ALS analysis for forestry and terrain (ground classification, CHM, segmentation) | GPL-3.0 | R | Catalog processing for large areas; `rasterize_terrain()` | 30, 64 |
| CloudCompare | Point-cloud/mesh viewer and editor: registration, M3C2, CSF, subsampling | GPL-2.0 | C++ / GUI, CLI | M3C2 plugin is the reference implementation | 30, 41, 57 |
| Open3D | 3D data processing: ICP, meshing, visualization | MIT | C++ / Python | Includes Open3D-ML for segmentation | 15, 41, 46 |
| PCL (Point Cloud Library) | Point-cloud algorithms (filters, features, registration) | BSD-3 | C++ | Robotics heritage; ROS integration | 15, 46 |
| py4dgeo | 4D point-cloud change analysis (M3C2, M3C2-EP, time series) | MIT | C++ / Python | From the 3DGeo group, Heidelberg | 41 |
| Entwine | Builds EPT point-cloud indexes for streaming | LGPL-2.1 | C++ / CLI | Used for the USGS 3DEP AWS point-cloud archive | 46, 47, 51 |
| Untwine / COPC tools | COPC conversion | BSD-3 / Apache-2.0 | C++ | COPC is single-file cloud-optimized LAZ | 47 |
| Potree / PotreeConverter | Web point-cloud rendering and octree conversion | BSD-2 | JS / C++ | Common for publishing lidar | 57 |
| OPALS | Orientation and processing of airborne laser scanning | Commercial (free for academic/small) | C++ / CLI, Python | TU Wien; strip adjustment, robust interpolation | 18, 30, 31 |
| TerraSolid (TerraScan, TerraMatch, TerraModeler) | Production lidar classification, strip adjustment, modelling | Commercial | MicroStation / Spatix | Industry standard in many production shops | 18, 30, 33 |
| LP360 / GeoCue | Lidar QA/QC, classification, drone-lidar production | Commercial | Windows (ArcGIS or standalone) | Strong on accuracy-assessment reporting | 30, 53 |
| Global Mapper (with Lidar Module) | General GIS with lidar classification and gridding | Commercial | Windows | Popular low-cost production tool | 30, 31, 57 |
| Trimble RealWorks / Business Center | Terrestrial and mobile scan registration; survey processing | Commercial | Windows | TBC handles GNSS/total-station adjustment too | 12, 15, 25 |
| Leica Cyclone (REGISTER 360, 3DR) / Infinity | Scan registration and survey adjustment | Commercial | Windows | Cyclone for TLS; Infinity for GNSS/level networks | 12, 15, 25 |
| Riegl RiPROCESS / RiPRECISION / RiSCAN PRO | Riegl sensor processing, strip adjustment, waveform | Commercial (bundled) | Windows | Full-waveform export; RiPRECISION for automated strip adjustment | 18, 29 |
| Applanix POSPac MMS | GNSS/IMU post-processing (SmartBase, PP-RTX) | Commercial | Windows | Trajectory uncertainty exports (SBET + RMS) | 12, 13 |
| NovAtel Inertial Explorer | GNSS/INS tightly coupled post-processing | Commercial | Windows | Alternative to POSPac for many lidar/sonar systems | 12, 13 |
| Pointcept | Deep-learning point-cloud perception codebase (Point Transformer v3 etc.) | MIT | Python / PyTorch | Research-grade; benchmarks on DALES, SensatUrban | 42, 43 |
| Open3D-ML / torch-points3d / KPConv | Point-cloud deep learning | MIT / BSD | Python | Reference implementations for semantic segmentation | 42 |
| TorchGeo | Geospatial deep learning datasets and models (rasters, DEMs) | MIT | Python / PyTorch | Handles CRS-aware sampling | 42, 43, 45 |
| segment-geospatial (samgeo) | Segment Anything applied to geospatial rasters | MIT | Python | For quick object masks from orthoimagery/DSMs | 42 |

## F.3 Photogrammetry, SfM, and stereo

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| MicMac | Photogrammetry suite (aerial, close-range, satellite) with rigorous bundle adjustment | CeCILL-B (BSD-like) | C++ / CLI | IGN France; strong on accuracy reporting | 22 |
| OpenDroneMap (ODM, WebODM, NodeODM) | Drone image → orthophoto, DSM, DTM, point cloud | AGPL-3.0 | Python/C++ / CLI, web | Ground classification via PDAL SMRF | 22, 30 |
| COLMAP | SfM and multi-view stereo | BSD-3 | C++ / CLI, GUI | Research standard; GLOMAP for global SfM | 22 |
| Meshroom / AliceVision | Node-based photogrammetry | MPL-2.0 | C++ / GUI | GPU required for dense steps | 22 |
| NASA Ames Stereo Pipeline (ASP) | Stereo DEMs from satellite and planetary images; `pc_align`, `dem_mosaic`, bundle adjust | Apache-2.0 | C++ / CLI | Supports DigitalGlobe/Maxar, Pléiades, ASTER, HiRISE, CTX, LRO NAC | 22, 41, 67 |
| SETSM | Surface extraction from TIN-based search-space minimization | Apache-2.0 | C / CLI | Produces ArcticDEM/REMA/EarthDEM strips | 22, 55 |
| CARS (CNES) | Satellite stereo 3D reconstruction pipeline | Apache-2.0 | Python | CO3D mission ground segment heritage | 22 |
| S2P (Satellite Stereo Pipeline) | Pushbroom stereo to DSM | AGPL-3.0 | Python | Research pipeline (CMLA/ENS) | 22 |
| Agisoft Metashape | SfM/MVS production | Commercial | Windows/macOS/Linux; Python API | Exports camera uncertainty, GCP residuals | 22 |
| Pix4Dmapper / Pix4Dmatic / Pix4Dsurvey | Drone and large-project photogrammetry | Commercial | Windows/macOS | Pix4Dsurvey for vectorization and ground point extraction | 22 |
| Bentley ContextCapture / iTwin Capture | Reality meshes at city scale | Commercial | Windows | Mesh outputs; LoD tiles (3D Tiles) | 22, 63 |
| DJI Terra | Drone photogrammetry and lidar (L1/L2) processing | Commercial | Windows | Tied to DJI hardware | 22, 18 |
| Trimble Inpho (Match-AT, Match-T DSM) | Aerial triangulation and DSM matching | Commercial | Windows | Classic aerial-survey production | 22 |
| SOCET GXP (BAE Systems) | Photogrammetric workstation; stereo DEM extraction (NGATE) | Commercial | Windows | Used for planetary DTMs (HiRISE, LRO) at USGS/UA | 22, 67 |
| Correlator3D (SimActive) | Aerial/drone DSM, orthophoto, DTM | Commercial | Windows | GPU dense matching | 22 |
| OpenMVS / OpenMVG | Multi-view stereo / SfM libraries | AGPL-3.0 / MPL-2.0 | C++ | Building blocks for custom pipelines | 22 |
| Nerfstudio / gsplat | NeRF and 3D Gaussian Splatting training and rendering | Apache-2.0 | Python / CUDA | Not metric by default; needs georeferencing | 22, 57 |

## F.4 Radar, SAR, and InSAR

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| ISCE2 / ISCE3 | InSAR processing (stripmap, TOPS, ALOS, NISAR) | Apache-2.0 (ISCE2 export-controlled historically; verify) | C/C++/Python | NASA JPL; NISAR ground segment basis | 21 |
| GMTSAR | InSAR processing built on GMT | GPL-3.0 | C / CLI | Scripps; simple batch processing | 21 |
| SNAP (Sentinel Application Platform) with S1TBX | Sentinel-1 interferometry, terrain correction | GPL-3.0 | Java / GUI, CLI (gpt) | ESA; terrain correction requires an external DEM | 21 |
| MintPy | Small-baseline InSAR time series | GPL-3.0 | Python | Works on ISCE/GAMMA/SNAP stacks | 21, 41 |
| LiCSBAS | Time-series from LiCSAR products | GPL-3.0 | Python | COMET; semi-automatic | 21, 41 |
| HyP3 (ASF) | On-demand Sentinel-1 InSAR and RTC | Free service (BSD-3 SDK) | web / Python SDK | No local processing needed | 21 |
| snaphu | Statistical-cost phase unwrapping | Stanford licence (free, redistributable with restrictions; verify) | C / CLI | Used by most open InSAR stacks | 21 |
| GAMMA Remote Sensing software | InSAR, SAR processing, geocoding | Commercial | C / CLI | Reference commercial toolkit in research | 21 |
| SARscape (ENVI) | SAR/InSAR processing in ENVI | Commercial | IDL / GUI | DEM generation from stereo/InSAR | 21 |
| ENVI | Image analysis incl. DEM extraction module | Commercial | IDL / GUI | Photogrammetric DEM extraction from stereo pairs | 21, 22 |
| PyRate | Rate and time-series estimation from InSAR | Apache-2.0 | Python | Geoscience Australia | 21, 38 |
| CReSIS Toolbox | Ice-penetrating radar processing | Free (academic) (verify) | MATLAB | Radar depth sounder processing for ice thickness | 21, 66 |

## F.5 Sonar and hydrography

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| MB-System | Multibeam/sidescan processing, editing, gridding, patch test | GPL-3.0 | C / CLI, Tk GUIs | The open reference for MBES; reads > 70 formats | 20, 26, 31 |
| HydrOffice (Sound Speed Manager, QC Tools, BAG Explorer) | Hydrographic QA tools, sound-speed profiles, BAG inspection | LGPL-2.1 (Sound Speed Manager) / LGPL-3.0 (QC Tools); check per tool | Python | Jointly CCOM/JHC and NOAA | 20, 47, 70 |
| Pydro | NOAA hydrographic Python distribution and tools | Public domain (NOAA) | Python / Windows | Bundles HydrOffice and NOAA field tools | 20, 70 |
| Kluster | Open multibeam processing (Kongsberg .all/.kmall) with TPU | CC0-1.0 (NOAA) | Python / Dask | Georeferencing and uncertainty in xarray | 20, 53 |
| CARIS HIPS and SIPS / BASE Editor / Onboard | Full hydrographic production (CUBE, TPU, BAG) | Commercial | Windows | Dominant in national hydrographic offices | 20, 30, 47 |
| QPS Qimera / Qinsy / Fledermaus | Processing (Qimera), acquisition (Qinsy), 4D visualization (Fledermaus) | Commercial | Windows | Fledermaus common for scientific visualization | 20, 57 |
| Hypack / Hysweep | Survey acquisition and processing | Commercial | Windows | Widespread in coastal/engineering surveys | 20, 26 |
| EIVA NaviSuite (NaviScan, NaviModel) | Acquisition and processing | Commercial | Windows | Offshore industry | 20 |
| Teledyne PDS | Acquisition/processing for Teledyne sonars and dredging | Commercial | Windows | Dredge monitoring | 20, 65 |
| BeamworX AutoClean / NavAQ | Automated cleaning and acquisition | Commercial | Windows | Fast CUBE-like cleaning | 20, 30 |
| SonarWiz (Chesapeake Technology) | Sidescan, sub-bottom, and bathymetry processing | Commercial | Windows | Strong sidescan mosaicking | 20 |
| Kongsberg SIS / Reson Sonar UI | Sonar control and acquisition | Bundled with hardware | Windows | Real-time QA displays | 20 |
| CUBE / CHRT (reference implementations) | Hypothesis-based bathymetric gridding | Licensed via CCOM/JHC to vendors (CUBE); CHRT research | C/C++ | Appears in CARIS, Qimera, Hypack; see MB-System's `mbgrid` for alternatives | 30, 31 |
| BAG library (libBAG) | Read/write Bathymetric Attributed Grid | BSD-3 | C++ / Python | ONS (Open Navigation Surface) | 47 |
| S-100/S-102 tools (IHO S-100 toolkit, NOAA s100py) | Produce S-102 bathymetric surfaces | Various; s100py public domain | Python | HDF5-based | 47, 62, 70 |
| GEBCO Cookbook tools / `gmt grdblend` | Compiling bathymetric grids | GPL-3.0 (GMT) | CLI | GEBCO Cookbook documents the workflow | 48 |
| OpenCPN | Chart display (ENC/raster) | GPL-2.0 | C++ / GUI | For checking chart datums and features | 62 |

## F.6 Terrain analysis, geomorphometry, and hydrology

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| GMT (Generic Mapping Tools) | Gridding (`surface`, `greenspline`), filtering, blending, mapping | LGPL-3.0 | C / CLI, Python (PyGMT), Julia | Minimum-curvature gridding with tension; `grdblend` for compositing | 31, 48, 57, 58 |
| GRASS GIS | Full GIS: `r.terraflow`, `r.watershed`, `r.geomorphon`, `v.surf.rst`, `r.in.pdal` | GPL-2.0 | C/Python / GUI, CLI | Regularized-spline interpolation with error estimates | 31, 44, 61 |
| SAGA GIS | Terrain analysis and hydrology modules (hundreds) | GPL-2.0 (library LGPL) | C++ / GUI, CLI | Sink filling (Wang & Liu), TWI, multi-scale TPI | 44, 61 |
| WhiteboxTools | > 500 geospatial tools incl. lidar, hydrology, geomorphometry | MIT | Rust / CLI, Python, QGIS plugin | Breaching, hydro-conditioning, lidar ground filtering | 30, 34, 61 |
| TauDEM | Parallel hydrologic terrain analysis (D∞ flow) | GPL-3.0 | C++/MPI / CLI | Scales to continental grids | 61 |
| RichDEM | Depression filling/breaching, flow accumulation | GPL-3.0 | C++ / Python | Priority-flood algorithms (Barnes) | 61 |
| LSDTopoTools | Geomorphic analysis (channel steepness, hillslope metrics) | GPL-3.0 | C++ | Edinburgh; research-grade | 40, 44 |
| TopoToolbox | Terrain and river-network analysis | GPL-3.0 (MATLAB and Python) | MATLAB / Python | Classic in geomorphology | 40, 61 |
| Landlab | Component-based landscape evolution and surface process modelling | MIT | Python | For synthetic terrain and process tests | 40, Appendix H |
| xdem | DEM co-registration (Nuth–Kääb, ICP), bias correction, uncertainty (variograms), differencing | Apache-2.0 | Python | GlacioHack; integrates with geoutils | 41, 53 |
| demcoreg / pygeotools | DEM co-registration to reference points (ICESat) and tools | MIT | Python | David Shean; ArcticDEM/REMA workflows | 41, 53 |
| GCD (Geomorphic Change Detection) | DoD with spatially variable uncertainty and thresholding | GPL-3.0 | ArcGIS add-in / standalone | Riverscapes consortium | 40, 41 |
| DSAS (Digital Shoreline Analysis System) | Shoreline change rates | Public domain (USGS) | ArcGIS add-in | Transect-based statistics | 34, 40 |
| MICRODEM | DEM analysis, DEMIX tools, visualization | Freeware (Peter Guth) | Windows | DEMIX criteria implemented here first | 53, 55 |
| Relief Visualization Toolbox (RVT) | Hillshade, sky-view factor, openness, local relief | Apache-2.0 | Python / QGIS plugin | ZRC SAZU | 57 |
| gdaldem (GDAL) | Hillshade, slope, aspect, TRI, TPI, roughness, color-relief | MIT | CLI | First-pass derivatives | 44, 57 |
| ArcGIS Pro (Spatial Analyst, 3D Analyst) | Raster/terrain analysis, lidar (LAS datasets), hydrology, geostatistics | Commercial | Windows; ArcPy | Arc Hydro for hydro-conditioning | 31, 61 |
| QGIS | Desktop GIS with Processing (GDAL, GRASS, SAGA, Whitebox) | GPL-2.0 | C++/Python / GUI | Point-cloud support via PDAL since 3.18+ | throughout |
| Surfer (Golden Software) | Gridding (kriging, min. curvature) and contouring | Commercial | Windows | Legacy in mining/geoscience | 31 |
| gstat / scikit-gstat / PyKrige / GSTools | Variography and kriging | GPL (gstat), MIT (scikit-gstat, PyKrige), LGPL-3.0 (GSTools) | R / Python | Interpolation uncertainty; variograms of DEM error | 31, 53 |
| DEMIX tools (Guth et al.) | Tile-based DEM intercomparison, ranking | Open (GitHub) (verify licence) | Python / MICRODEM | Wine-contest ranking statistics | 53, 55 |

## F.7 GNSS, navigation, and positioning

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| RTKLIB (and rtklibexplorer fork) | GNSS RTK/PPK/PPP post-processing and real time | BSD-2 | C / CLI, Windows GUI | Open reference; fork adds low-cost receiver tuning | 12 |
| PRIDE PPP-AR | PPP with ambiguity resolution | GPL-3.0 | Fortran/C / CLI | Wuhan University; cm-level static | 12 |
| GAMIT/GLOBK | Scientific GNSS network processing | Free for academic (licence agreement) | Fortran / CLI | MIT; reference-frame work, velocities | 8, 12, 38 |
| Bernese GNSS Software | Scientific GNSS processing | Commercial (academic pricing) | Fortran / CLI | AIUB; used by many IGS analysis centres | 8, 12 |
| GipsyX / RTGx | PPP and orbit determination | Free for non-commercial via JPL licence (verify) | C++/Python | JPL; PPP with JPL products | 12 |
| OPUS (NGS) | Online static GNSS positioning in the US (NAD83/ITRF) | Free service | web | OPUS-Projects for networks; OPUS Share for benchmarks | 12, 25 |
| AUSPOS / CSRS-PPP / TrimbleRTX / Apps from IGS ACs | Online PPP/static services | Free services | web | Different frames/epochs — read the report header | 12 |
| gnssrefl | GNSS interferometric reflectometry (snow depth, water level, soil moisture) | GPL-3.0 | Python | Kristine Larson's group | 14, 36 |
| georinex / gnss-py / Hatanaka tools | RINEX parsing and compression | MIT / BSD | Python / C | Utility layer | 12 |
| Teqc (legacy) / gfzrnx / BNC | RINEX QC, editing, streaming | Freeware (teqc discontinued) / free (gfzrnx) / GPL (BNC) | CLI | Multipath and cycle-slip QC | 12 |
| Trimble Business Center / Leica Infinity / Topcon Magnet | Commercial GNSS/total-station network adjustment | Commercial | Windows | Least-squares adjustment reports with σ | 12, 25 |
| STAR*NET (MicroSurvey) | Least-squares survey network adjustment | Commercial | Windows | Widely used by land surveyors | 25 |
| ROS 2 (robot_localization, nav2) / GTSAM / Ceres Solver | State estimation and factor-graph optimization | Apache-2.0 / BSD-3 / BSD-3 | C++ / Python | Backbone for SLAM and GNSS/INS fusion research | 13, 15 |
| Kalibr / OpenCalib | Multi-sensor calibration (camera–IMU–lidar) | BSD-3 / Apache-2.0 | C++/Python | Boresight and lever-arm estimation | 13, 25 |
| LIO-SAM / FAST-LIO2 / KISS-ICP / Cartographer | Lidar(-inertial) odometry and SLAM | BSD-3 / GPL-2.0 / MIT / Apache-2.0 | C++ / ROS | Mapping innerspace and GNSS-denied sites | 15 |
| OctoMap / GridMap / Elevation Mapping (ETH/ANYbotics) | Robot occupancy and elevation maps | BSD-3 | C++ / ROS | Elevation map as a control input | 15, 62 |
| OpenSfM / Mapillary tools | Street-level SfM | BSD-2 | Python | Crowd imagery to geometry | 16, 22 |

## F.8 Data models, formats, catalogs, and infrastructure

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| PostGIS (with pointcloud and raster extensions) | Spatial database; 3D geometry; raster storage | GPL-2.0 | C / SQL | `pgpointcloud` for LAS in Postgres | 46, 59 |
| DuckDB spatial | Analytical SQL with spatial types, GeoParquet | MIT | C++ / SQL, Python | Fast local analytics on checkpoint tables and STAC exports | 51, 53 |
| GeoParquet / Apache Arrow / GeoArrow | Columnar vector and point storage | Apache-2.0 | lib | Emerging exchange for billions of points | 46, 47 |
| Zarr / NetCDF (netCDF-C, h5netcdf) / HDF5 | Chunked n-dimensional arrays (DEM time series, BAG uses HDF5) | MIT / BSD / BSD-style | C / Python | Zarr v3 for cloud-native cubes | 47, 50 |
| COG tooling: `rio cogeo`, `gdal_translate -of COG`, cogger | Cloud-optimized GeoTIFF creation and validation | BSD-3 / MIT | Python / CLI / Go | Validate overviews and tiling | 47 |
| pystac / pystac-client / stac-fastapi / stactools | STAC catalog creation, search, and serving | Apache-2.0 | Python | STAC extensions for point clouds and raster bands | 51 |
| STAC Browser / Radiant Earth tools | Browsing STAC catalogs | Apache-2.0 | JS / web | — | 51 |
| GeoNetwork / pycsw / CKAN | Metadata catalogs (ISO 19115, CSW, DCAT) | GPL-2.0 / MIT / AGPL-3.0 | Java / Python | National SDI backbones | 49, 51 |
| ISO 19115 / FGDC tools (mdEditor, USGS Metadata Wizard, `mp`) | Metadata authoring and validation | Open (various) | web / Python | FGDC CSDGM still required by some US programs | 49 |
| TiTiler / rio-tiler / terracotta | Dynamic raster tiling from COGs | MIT | Python | Serve DEMs and hillshades without pre-tiling | 51, 57 |
| GeoServer / MapServer / pg_tileserv | OGC services (WMS/WCS/WFS/OGC API) | GPL-2.0 / MIT / Apache-2.0 | Java / C / Go | WCS for DEM delivery | 51 |
| Cesium (CesiumJS, Cesium ion, 3D Tiles tools) | 3D globe rendering; quantized-mesh terrain; 3D Tiles | Apache-2.0 (CesiumJS); ion commercial | JS / web | 3D Tiles is an OGC community standard | 46, 57, 63 |
| deck.gl / loaders.gl | GPU web visualization; LAS/3D Tiles loaders | MIT | JS | TerrainLayer from elevation tiles | 57 |
| MapLibre GL JS / Native | Vector and raster-DEM map rendering (terrain, hillshade) | BSD-3 | JS / C++ | Terrarium/Mapbox RGB terrain encodings | 57, 58 |
| Terrain-RGB tools (rio-rgbify, `gdal2tiles`, MapTiler Engine) | Encode DEMs for web terrain | MIT / MIT / commercial | Python / CLI | Quantization (0.1 m steps) is a format error | 47, 57 |
| GeoTIFF/COG validators (`validate_cloud_optimized_geotiff.py`), `lasinfo`/`pdal info`, BAG validator | File validation | MIT / LGPL / BSD | CLI | Appendix G.6 uses these | 47 |
| Git LFS / DVC / DataLad / Quilt | Data versioning | MIT / Apache-2.0 / MIT / Apache-2.0 | CLI | Provenance of processed DEMs | 50 |
| Docker / Apptainer / conda-lock / Nix | Reproducible environments | Apache-2.0 / BSD-3 / MIT / MIT | CLI | Pin GDAL/PROJ versions — results change with grids | 29, 50 |
| Apache Spark / Dask / Ray with GeoTrellis, RasterFrames, Xarray | Distributed raster/point processing | Apache-2.0 | Scala / Python | Continental-scale compositing | 29, 48 |
| Google Earth Engine | Planetary-scale raster analysis (hosts SRTM, Copernicus, ALOS, ArcticDEM…) | Free for non-commercial; commercial tiers | JS / Python API | Check each asset's licence and version | 51, 55 |
| Microsoft Planetary Computer / AWS Open Data / NOAA NODD | Hosted open datasets (3DEP, Copernicus DEM, BlueTopo…) | Free (dataset licences apply) | STAC / S3 | Mirrors may lag source versions | 51 |
| OpenTopography | Lidar and global DEM discovery, on-demand processing | Free (academic focus; OT+ tiers) | web / API | Hosts DEMIX-relevant data; `pc2dem` pipelines | 51, Appendix H |
| FME (Safe Software) | ETL for spatial data, point-cloud transformation | Commercial | Windows/Linux | Format conversion at scale | 29, 47 |

## F.9 Visualization, cartography, and communication

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| Blender (with BlenderGIS) | Physically based relief rendering, 3D printing exports | GPL-2.0 (Blender), GPL-3.0 (BlenderGIS) | Python / GUI | Realistic shaded relief; vertical exaggeration must be documented | 57 |
| Eduard | Shaded relief with neural-network generalization (Jenny et al.) | Commercial (macOS) | macOS | Cartographic relief shading | 57 |
| QGIS (hillshade, relief, 3D map view, Qgis2threejs) | Map production | GPL-2.0 | GUI | Print layouts with graticules, scale bars, north arrows | 57, 58 |
| ArcGIS Pro (Maps, Layouts, Scene) | Map production, multidirectional hillshade, 3D scenes | Commercial | Windows | Standard in US agencies for topo map production | 58 |
| matplotlib / cmcrameri / cmocean / colorcet | Plotting and perceptually uniform colormaps | PSF / MIT / MIT / CC-BY | Python | Use `batlow`, `topo`, `oleron` (land–sea) — avoid rainbow | 57 |
| Terrain Sculptor / Pyramid Shader / Scree Painter | Generalized relief, scree, and rock drawing (Jenny) | Open (various) (verify) | Java | Cartographic generalization | 57, 58 |
| MapSCII / Mapnik / Maperitive | Tile rendering | GPL / LGPL-2.1 / freeware | C++ / CLI | — | 58 |
| ParaView / VisIt | Scientific 3D visualization of meshes, voxels | BSD-3 | C++ / GUI, Python | Large time-varying datasets | 46, 57 |
| Potree / Cesium / three.js | Web 3D (see F.2, F.8) | BSD-2 / Apache-2.0 / MIT | JS | — | 57 |
| PlotJuggler / GNSS Viewer tools | Time-series inspection of trajectories | MPL-2.0 | C++ | For spotting timing errors | 6, 13 |
| Inkscape / Scribus | Vector map finishing | GPL-2.0 / GPL-2.0 | GUI | Marginalia and legends | 58 |
| Touch Mapper / OpenSCAD / PrusaSlicer | Tactile and 3D-printed terrain | Open (various) | web / CLI | Accessibility | 57 |

## F.10 Hydraulic, hazard, and domain models that consume DEMs

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| HEC-RAS (1D/2D) | River hydraulics and floodplain mapping | Freeware (US Army Corps; closed source) | Windows | 2D mesh from DTM; RAS Mapper terrain tiles | 61 |
| HEC-HMS | Hydrologic modelling | Freeware (USACE) | Windows/Linux | — | 61 |
| LISFLOOD-FP | Raster-based 2D flood inundation | GPL-3.0 (v8) | C++ / CLI | Subgrid channels; used with FABDEM in global studies | 61 |
| SFINCS (Deltares) | Compound flooding (surge, rain, river) at reduced complexity | GPL-3.0 | Fortran / Python (HydroMT) | Needs topobathy seams correct | 61, 66 |
| ANUGA | Shallow-water finite-volume inundation (tsunami, flood) | Apache-2.0 (verify; earlier GPL) | Python/C | Unstructured mesh from DEM | 61 |
| Delft3D FM / D-Flow | Hydrodynamics, morphology, waves | AGPL-3.0 (source) / commercial support | Fortran/C++ | Morphological change needs bathy time series | 40, 66 |
| TUFLOW / MIKE+ / Infoworks ICM / XPSWMM | Commercial urban/river flood modelling | Commercial | Windows | Urban drainage with 1D–2D coupling | 61 |
| SWMM (EPA) / PCSWMM | Stormwater modelling | Public domain (SWMM) / commercial (PCSWMM) | C / Windows | Subcatchment slopes from DTM | 61 |
| RAMMS / Flow-R / r.avaflow / Titan2D | Avalanche, debris-flow, rockfall, lava and mass-flow runout | Commercial / free / GPL-3.0 / open (verify) | Windows / GRASS / Python | Runout is very sensitive to DEM smoothing | 39, 61 |
| GeoClaw / ComMIT-MOST / Tsunami-HySEA | Tsunami propagation and inundation | BSD / NOAA free / academic licence | Fortran/Python / GPU | Nearshore bathymetry resolution governs results | 39, 61 |
| SAGA / GRASS solar modules, `r.sun`, PVGIS | Solar radiation on terrain | GPL | — | Horizon from DSM vs DTM matters | 1, 63 |
| WindNinja / WAsP / OpenFOAM | Wind flow over terrain | Public domain / commercial / GPL-3.0 | — | DSM roughness vs DTM shape | 1, 63 |
| PLS-CADD | Power-line design and clearance analysis from lidar | Commercial | Windows | Wire catenary modelling | 33 |
| Maptek PointStudio / Vulcan; Leapfrog; Datamine; Surpac | Mining survey and geological modelling | Commercial | Windows | Volumes by surface difference; underground scanning | 65 |
| Propeller / Trimble Stratus / Carlson / Kespry (legacy) | Earthworks volume platforms (drone photogrammetry to stockpile volumes) | Commercial (SaaS) | web | Report their own accuracy — check against GCPs | 65 |
| Trimble SiteVision / Earthworks; Topcon; Leica iCON | Machine control and site survey | Commercial | — | Design-surface vs as-built | 65 |
| eCognition (Trimble) | Object-based image analysis incl. nDSM features | Commercial | Windows | Classic OBIA for buildings/trees | 42, 63 |
| 3dcitydb / citygml-tools / CityJSON tools (cjio) | City model storage, validation, conversion | Apache-2.0 / Apache-2.0 / MIT | Java / Python | val3dity for geometric validation | 63 |
| Open3D-ML, PointNet++, RandLA-Net implementations | Urban point-cloud semantics | MIT / various | Python | See F.2 | 42, 63 |

## F.11 Planetary and space geodesy

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| ISIS (USGS Astrogeology) | Planetary image processing: ingestion, camera models, control networks (`jigsaw`), map projection | CC0 / public domain (verify; formerly custom) | C++ / CLI | Core for HiRISE/CTX/LRO DTM pipelines with SOCET or ASP | 67 |
| SPICE (NAIF) toolkit, SpiceyPy | Spacecraft geometry, ephemerides, pointing, body frames | Public domain (NASA) | C/Fortran/IDL/MATLAB; Python | Needed to geolocate any planetary observation | 67 |
| Ames Stereo Pipeline | See F.3 | Apache-2.0 | C++ | `bundle_adjust`, `pc_align` to altimetry | 67 |
| JMARS / JMoon | Planetary GIS and data browsing | Free (ASU) | Java | Visual QA of DTM coverage and layers | 67 |
| QGIS with planetary CRS (PROJ IAU codes) | Planetary GIS | GPL-2.0 | GUI | IAU_2015 CRS codes in PROJ ≥ 8 | 67 |
| OpenPlanetary tools / PDS4 tools / pds4_tools | PDS archive access | Open | Python | Label parsing | 67 |
| GMT (planetary ellipsoids) | Mapping other bodies | LGPL-3.0 | CLI | `-Je`/custom ellipsoids | 67 |
| ICESat-2 tools: `icepyx`, `SlideRule`, `pyGEDI` / `gedipy` | Spaceborne lidar access and subsetting for validation | BSD-3 / BSD-3 / various | Python | ATL03/06/08 photon-level access | 52, 53 |
| Nuth–Kääb implementations (xdem, demcoreg) | Co-registration (see F.6) | — | — | — | 41 |

## F.12 Checklists, QA, and reporting helpers

| Name | Task area | Licence | Language / platform | Notes | Chapters |
|---|---|---|---|---|---|
| `pdal info --stats`, `pdal density`, `lasinfo`, `lasvalidate` | Point-cloud statistics and validity | BSD-3 / LGPL / ASPRS free | CLI | lasvalidate checks LAS spec compliance | 47, 53 |
| `gdalinfo -stats -checksum`, `gdalcompare.py` | Raster inspection and regression tests | MIT | CLI | Pixel-is-point vs area flag is in the metadata | 47, 54 |
| ASPRS positional-accuracy spreadsheet / `aspras` tools | ASPRS 2014/2023 statistics (NVA/VVA) | Free (ASPRS) / open (verify) | Excel / Python | Compute RMSE, 95 % with the right formula | 53 |
| NOAA/USGS lidar QA tools (e.g. `lidar_qc`, GeoCue QC) | Density, overlap, classification QA | Public domain / commercial | — | — | 53 |
| Great Expectations / pandera / pytest | Data validation and test harnesses for pipelines | Apache-2.0 / MIT / MIT | Python | Regression tests on reference tiles | 29 |
| Jupyter / Quarto / R Markdown | Reproducible reports (accuracy assessment, fitness memos) | BSD-3 / MIT / GPL | — | Deliver the notebook with the DEM | 53, 54 |
| Zenodo / Dryad / Pangaea / NCEI archive submission tools | Archival with DOIs | Free services | web / API | Trusted repositories (CoreTrustSeal) | 50 |
| ReadTheDocs / mkdocs / Sphinx | Documentation of processing chains | MIT / BSD | Python | Processing reports as living documents | 29, 49 |

## F.13 Counting and caveats

This index contains roughly 190 named tools in 12 groups (counting combined cells as one row). It is not exhaustive: national hydrographic offices and survey agencies run bespoke pipelines; many research groups publish one-off repositories; vendors rename products yearly. Three durable observations from [Chapter 71](../chapters/ch71-software-landscape.md) apply to every row: (1) the open-source foundation layer (GDAL, PROJ, PDAL, GMT) is shared by commercial products too, so a bug or grid version there affects everyone; (2) the differences that matter for validation are rarely algorithmic — they are defaults, hidden resampling, and datum handling; (3) the licence of the *data* usually constrains you more than the licence of the *software*.

<!-- figure: Figure F.1 — Dependency diagram: PROJ → GDAL → (PDAL, rasterio, QGIS, GRASS, ArcGIS Pro, Global Mapper, FME, …) with the open libraries as a shared trunk and commercial and open applications as branches. -->

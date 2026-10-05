# Appendix A — Glossary

Terms used across the handbook, in alphabetical order (acronyms sorted as spelled). Each entry gives a one-line working definition, flags common confusions with ⚠, and points to the chapter(s) where the term is treated. Height notation throughout: $h$ ellipsoidal, $H$ orthometric, $N$ geoid undulation, $h = H + N$.

## A

- **Absolute accuracy** — closeness of a coordinate or height to its true value in the stated reference frame, as opposed to relative accuracy between nearby points — *Ch. 5, 53*
- **Accuracy** — closeness of a measurement to the truth; distinct from precision (repeatability) and uncertainty (quantified doubt) — ⚠ RMSE is not a 95 % bound — *Ch. 5*
- **ADS-B** — Automatic Dependent Surveillance–Broadcast; aircraft position broadcasts used to flag transient objects and verify airborne trajectories — *Ch. 27*
- **AGL** — above ground level; height relative to the local terrain surface rather than a datum — *Ch. 62*
- **AHN** — Actueel Hoogtebestand Nederland; the Dutch national lidar elevation programme (AHN1–AHN5) — *Ch. 55*
- **AIS** — Automatic Identification System; ship position broadcasts, also a source of crowdsourced bathymetry context — *Ch. 27*
- **Aliasing** — appearance of spurious low-frequency content when a surface is sampled below the Nyquist rate — *Ch. 44*
- **Altimetry (radar/laser)** — nadir ranging from a satellite or aircraft to a surface, giving height profiles along track — *Ch. 21, 23*
- **AMSL** — above mean sea level; loosely, an orthometric height — ⚠ "sea level" differs by datum and epoch — *Ch. 9*
- **ANUDEM** — Hutchinson's drainage-enforcing thin-plate-spline gridding algorithm (ArcGIS *Topo to Raster*) — *Ch. 31*
- **Aspect** — compass direction of the steepest downslope gradient at a cell — *Ch. 57, App. B*
- **ASPRS** — American Society for Photogrammetry and Remote Sensing; issuer of the LAS format and positional accuracy standards — *Ch. 70*
- **ATL03 / ATL06 / ATL08** — ICESat-2 photon, land-ice height, and land/vegetation height products — *Ch. 52*
- **AUV** — autonomous underwater vehicle; untethered robotic platform for near-bottom sonar mapping — *Ch. 16*

## B

- **BAG** — Bathymetric Attributed Grid; Open Navigation Surface format carrying elevation, uncertainty, and metadata in HDF5 — *Ch. 47*
- **Bare earth** — the terrain surface with vegetation and structures removed according to a stated rule — ⚠ the rule varies by producer — *Ch. 32*
- **Bathymetry** — measurement and representation of water depth / submerged terrain — *Ch. 2, 20*
- **Beam angle (sonar)** — angle of a multibeam beam from nadir; drives footprint size and refraction sensitivity — *Ch. 20*
- **Beam footprint** — area of the seabed (or ground) ensonified or illuminated by one beam or pulse — *Ch. 17, 20*
- **Bias (systematic error)** — the mean of the error distribution; removable if known — *Ch. 5*
- **Bilinear / bicubic resampling** — interpolation kernels used when regridding rasters; smooth values, shift extremes — *Ch. 10*
- **BIM** — building information model; engineered 3D model of a structure, often on a local vertical datum — *Ch. 63*
- **BlueTopo** — NOAA's public best-available bathymetric compilation derived from the National Bathymetric Source — *Ch. 48, 55*
- **Boresight** — angular misalignment between a sensor's axes and the IMU body frame, estimated by calibration — *Ch. 13, 25*
- **Breakline** — vector line (hard or soft) constraining surface interpolation along edges such as curbs and banks — *Ch. 59*
- **Bundle adjustment** — simultaneous least-squares estimation of camera poses, calibration, and 3D points from image observations — *Ch. 22*

## C

- **Canopy height model (CHM)** — DSM minus DTM over vegetation; the height of the canopy top above ground — *Ch. 64*
- **CARE principles** — Collective benefit, Authority to control, Responsibility, Ethics for Indigenous data governance — *Ch. 69*
- **CATZOC / ZOC** — Category of Zone of Confidence on nautical charts (A1, A2, B, C, D, U); encodes survey quality — *Ch. 62, 70*
- **CE90 / CE95** — circular error radius containing 90 % / 95 % of horizontal errors — *Ch. 5, 53*
- **Chart datum** — the low-water reference surface for charted depths (LAT, MLLW, etc.) — ⚠ differs from the land datum by metres — *Ch. 9*
- **Checkpoint** — independent surveyed point used only to test a product, never in its adjustment — ⚠ never also a control point — *Ch. 52, 53*
- **CityGML / CityJSON** — OGC XML and compact JSON encodings of semantic 3D city models with levels of detail — *Ch. 47, 63*
- **COG** — Cloud-Optimized GeoTIFF; internally tiled GeoTIFF with overviews, readable by HTTP range requests — *Ch. 47*
- **Collinearity equations** — photogrammetric relation between image, perspective centre, and ground point — *Ch. 22, App. B*
- **Compositing** — merging multiple elevation datasets into one product with source selection and feathering — *Ch. 48*
- **Conformal prediction** — distribution-free method for producing prediction intervals with guaranteed coverage — *Ch. 43, App. B*
- **Contour** — isoline of equal elevation; the historical primitive of topographic mapping — *Ch. 58, 59*
- **Control point (GCP)** — surveyed point used to constrain an adjustment or georeferencing — *Ch. 25*
- **COPC** — Cloud-Optimized Point Cloud; LAZ 1.4 with an embedded octree for HTTP range access — *Ch. 47*
- **Co-registration** — alignment of two DEMs or point clouds (shift, tilt, scale) before differencing — *Ch. 41*
- **CORS** — continuously operating reference station; permanent GNSS station providing reference observations — *Ch. 12, 25*
- **Crowdsourced bathymetry (CSB)** — depths logged by volunteer vessels under IHO B-12 — *Ch. 20, 70*
- **CRS** — coordinate reference system; datum plus coordinate system (and, when kinematic, epoch) — *Ch. 8*
- **CSDGM** — FGDC Content Standard for Digital Geospatial Metadata (1994/1998) — *Ch. 49*
- **CUBE** — Combined Uncertainty and Bathymetry Estimator; hypothesis-based sounding-to-grid estimator with per-node uncertainty — *Ch. 20, 31*
- **Curvature (profile/plan)** — second derivative of the surface along and across the slope direction — *Ch. 57, App. B*

## D

- **D8 / D∞** — single- and multiple-direction flow-routing algorithms on grids — *Ch. 61*
- **Datum (geodetic)** — reference frame definition plus its realization (and epoch) from which coordinates are reckoned — ⚠ "WGS 84" has multiple realizations — *Ch. 8, 9*
- **DBM** — digital bathymetric model; a DEM of the seabed — *Ch. 4*
- **DCAT / GeoDCAT-AP** — W3C and EU catalog vocabularies for dataset metadata — *Ch. 51*
- **Deflection of the vertical** — angle between the plumb line and the ellipsoidal normal — *Ch. 7*
- **DEM** — digital elevation model; generic term for a gridded (or other) elevation surface — ⚠ used for both DSM and DTM — *Ch. 4*
- **DEMIX** — Digital Elevation Model Intercomparison eXercise; community method for ranking global DEMs — *Ch. 55*
- **Density (point)** — points per unit area; nominal pulse density (NPD) versus achieved — *Ch. 44*
- **DGGS** — discrete global grid system; hierarchical cell tessellation of the globe (S2, H3, ISEA) — *Ch. 60*
- **DHM** — digital height model; term used in some countries for DSM or nDSM — ⚠ ambiguous — *Ch. 4*
- **DoD** — DEM of difference; cell-wise subtraction of two DEMs — *Ch. 41*
- **Doming** — bowl- or dome-shaped systematic error in SfM DSMs from unmodelled radial distortion — *Ch. 22*
- **DOP** — dilution of precision; geometry factor scaling GNSS position uncertainty — *Ch. 12*
- **Draft (vessel)** — depth of the transducer below the water surface; a sonar depth offset — *Ch. 20*
- **DSM** — digital surface model; the first-reflective surface including vegetation and structures — *Ch. 4*
- **DTED** — Digital Terrain Elevation Data; US military raster format (Levels 0–2) — *Ch. 47*
- **DTM** — digital terrain model; the bare-earth surface — *Ch. 4*
- **Dynamic height** — geopotential number divided by a constant normal gravity; used for lake levels — *Ch. 7*

## E

- **ECEF** — Earth-centred, Earth-fixed Cartesian coordinates (X, Y, Z) — *Ch. 8, App. B*
- **Echo sounder (SBES)** — single-beam sonar measuring depth from two-way travel time — *Ch. 20*
- **Effective resolution** — smallest feature a DEM actually resolves; generally coarser than its pixel size — *Ch. 44*
- **Effective sample size** — number of independent samples equivalent to a set of spatially correlated ones — *Ch. 5*
- **EGM96 / EGM2008** — NGA global geopotential (geoid) models — *Ch. 7*
- **Ellipsoid (reference)** — oblate spheroid approximating the Earth (GRS80, WGS 84, Clarke 1866, …) — *Ch. 7*
- **Ellipsoidal height (h / HAE)** — height above the reference ellipsoid along its normal; what GNSS measures — ⚠ not an elevation above sea level — *Ch. 7, 9*
- **Epoch** — the instant to which coordinates refer in a time-dependent frame — *Ch. 6, 38*
- **EPSG** — IOGP Geodetic Parameter Dataset; registry of CRS and transformation codes — *Ch. 8*
- **EPT** — Entwine Point Tiles; octree-organized, cloud-native point-cloud layout, predecessor of COPC — *Ch. 47*
- **Error** — difference between a measured/modelled value and the truth; realized, not knowable exactly — *Ch. 5*
- **ETRS89** — European Terrestrial Reference System 1989, fixed to the Eurasian plate — *Ch. 8*
- **eTOD** — electronic terrain and obstacle data (ICAO Annex 15) — *Ch. 62, 70*

## F

- **FABDEM** — Forest And Buildings removed Copernicus DEM; ML-corrected 30 m global DTM — *Ch. 43, 55*
- **FAIR principles** — Findable, Accessible, Interoperable, Reusable data — *Ch. 50*
- **Feathering** — gradual blending across the overlap between composited datasets — *Ch. 48*
- **FGDC** — US Federal Geographic Data Committee — *Ch. 70*
- **First return / last return** — earliest and latest echo of a lidar pulse; top of surface vs nearest ground — *Ch. 18*
- **Flattening (f)** — $(a-b)/a$ of the reference ellipsoid; GRS80 $1/f = 298.257222101$ — *Ch. 7*
- **Footprint (laser)** — ground area illuminated by one pulse; beam divergence × range — *Ch. 18*
- **Full waveform** — digitized return intensity vs time for a lidar pulse, rather than discrete returns — *Ch. 18*

## G

- **Gaussian process (kriging)** — probabilistic interpolation yielding mean and variance from a covariance model — *Ch. 31*
- **GCP** — ground control point; see *control point* — *Ch. 25*
- **GEBCO** — General Bathymetric Chart of the Oceans; global bathymetric compilation (1903–) — *Ch. 55*
- **GEDI** — Global Ecosystem Dynamics Investigation; full-waveform lidar on the ISS — *Ch. 52, 64*
- **Geiger-mode lidar** — photon-detecting array lidar with very high sensitivity and distinct noise behaviour — *Ch. 18*
- **Geoid** — equipotential surface of Earth's gravity field approximating mean sea level; zero for orthometric heights — *Ch. 7*
- **Geoid model** — numerical realization of the geoid (EGM2008, GEOID18, GEOID2022, …) — *Ch. 7, 9*
- **Geoid undulation (N)** — separation between geoid and ellipsoid; $N = h - H$ — *Ch. 7*
- **GeoPackage** — OGC SQLite-based container for vector and raster data — *Ch. 47*
- **GeoParquet** — columnar vector (and STAC) encoding on Apache Parquet — *Ch. 47, 51*
- **Geopotential number (C)** — $W_0 - W_P$; the physical quantity underlying orthometric, normal, and dynamic heights — *Ch. 7*
- **Georeferencing (direct)** — computing ground coordinates from sensor pose (GNSS/INS) without ground control — *Ch. 13, 18*
- **GeoTIFF** — TIFF with georeferencing tags (OGC GeoTIFF 1.1) — *Ch. 47*
- **GeoZarr** — draft OGC convention for geospatial Zarr stores — *Ch. 47*
- **GNSS** — Global Navigation Satellite Systems (GPS, GLONASS, Galileo, BeiDou) — *Ch. 12*
- **GRAV-D** — NGS airborne gravity programme underpinning GEOID2022 — *Ch. 7, 73*
- **Grid registration (pixel-is-area / pixel-is-point)** — whether a cell value refers to the cell centre or the cell area; GeoTIFF RasterPixelIs — ⚠ half-cell shift — *Ch. 10, 47*
- **Ground filtering** — classification of point-cloud returns as ground vs non-ground — *Ch. 30*
- **GSD** — ground sample distance; pixel size of imagery on the ground — *Ch. 22, 44*
- **GSF** — Generic Sensor Format; sonar data exchange format — *Ch. 47*
- **GUM** — ISO/JCGM *Guide to the Expression of Uncertainty in Measurement* — *Ch. 5*

## H

- **H3** — Uber's hexagonal hierarchical DGGS — *Ch. 60*
- **HAE** — height above ellipsoid; see *ellipsoidal height* — *Ch. 7*
- **Height of ambiguity** — InSAR height change corresponding to one fringe (2π) of phase — *Ch. 21, App. B*
- **Helmert transformation** — 7-parameter (or 14 with rates) similarity transformation between frames — *Ch. 8, App. B*
- **Hillshade** — rendering of a DEM by simulated illumination (Horn 1981) — *Ch. 57*
- **Horn operator** — 3×3 finite-difference gradient estimator for slope and aspect — *Ch. 57, App. B*
- **HSSD** — NOAA Hydrographic Surveys Specifications and Deliverables — *Ch. 70*
- **HTDP** — NGS Horizontal Time-Dependent Positioning tool for epoch transformations — *Ch. 38*
- **Hydro-conditioning** — modifying a DEM so water flows correctly (pit filling, breaching) — *Ch. 34, 61*
- **Hydro-enforcement** — cutting through barriers (culverts, bridges) so modelled flow passes — *Ch. 34*
- **Hydro-flattening** — forcing water bodies to a flat (or monotonic) surface in a DTM — *Ch. 34*

## I

- **ICESat / ICESat-2** — NASA spaceborne laser altimeters (2003–2009; 2018–) — *Ch. 52*
- **ICP** — iterative closest point; point-cloud registration algorithm — *Ch. 41*
- **IDW** — inverse-distance weighting interpolation — *Ch. 31*
- **IGS** — International GNSS Service; precise orbits, clocks, and station network — *Ch. 12*
- **IHO** — International Hydrographic Organization — *Ch. 70*
- **IHRS / IHRF** — International Height Reference System / Frame; geopotential-based global height system — *Ch. 73*
- **IMU** — inertial measurement unit (gyroscopes and accelerometers) — *Ch. 13*
- **IndoorGML** — OGC standard for indoor spatial models — *Ch. 63*
- **INS** — inertial navigation system; IMU plus mechanization to position, velocity, attitude — *Ch. 13*
- **InSAR** — interferometric SAR; phase differences between acquisitions giving topography or deformation — *Ch. 21*
- **INSPIRE** — EU Directive 2007/2/EC on spatial data infrastructure; Elevation theme specification — *Ch. 70*
- **Intensity (lidar)** — return signal strength; useful for classification, not calibrated reflectance unless corrected — *Ch. 18*
- **Interpolation** — estimating values between samples (IDW, splines, kriging, TIN) — *Ch. 31*
- **IoU** — intersection over union; segmentation accuracy metric — *Ch. 42, App. B*
- **ISO 19115 / 19157** — geographic metadata / data-quality standards — *Ch. 49*
- **Isostasy** — compensation of topographic loads by density or thickness variations at depth — *Ch. 7, 72*
- **ITRF** — International Terrestrial Reference Frame (ITRF88 … ITRF2020) — *Ch. 8, 38*

## J–K

- **JCGM** — Joint Committee for Guides in Metrology; publisher of the GUM and VIM — *Ch. 5*
- **Kalman filter** — recursive least-squares estimator for dynamic systems; core of GNSS/INS — *Ch. 13, App. B*
- **Kriging** — see *Gaussian process* — *Ch. 31*

## L

- **LAS / LAZ** — ASPRS point-cloud format / its lossless compression — *Ch. 47*
- **LAT** — lowest astronomical tide; common chart datum — *Ch. 9*
- **Layover** — SAR geometric distortion where steep foreslopes map to the same range — *Ch. 21*
- **LE90 / LE95** — linear (vertical) error containing 90 % / 95 % of errors — *Ch. 5, 53*
- **Least squares** — estimation minimizing the weighted sum of squared residuals — *Ch. 5, App. B*
- **LEO-PNT** — positioning, navigation, and timing from low-Earth-orbit satellites — *Ch. 73*
- **Level of detail (LoD, 3D models)** — CityGML generalization level (LoD0–LoD3) — ⚠ not level of detection — *Ch. 63*
- **Level of detection (LoD)** — minimum change distinguishable from noise in a DoD at a stated confidence — ⚠ not level of detail — *Ch. 41*
- **Levelling (spirit/geodetic)** — measuring height differences with a horizontal line of sight — *Ch. 9, 72*
- **Lever arm** — offset vector between sensor, IMU, and GNSS antenna reference points — *Ch. 13, 25*
- **Lidar** — light detection and ranging; laser pulse ranging — *Ch. 18, 19*
- **Lidar Base Specification (LBS)** — USGS requirements for lidar deliverables (QL0–QL3) — *Ch. 70*
- **Lineage** — documented history of a dataset's sources and processing — *Ch. 49, 50*

## M

- **M3C2** — Multiscale Model-to-Model Cloud Comparison; point-cloud change detection with local LoD₉₅ — *Ch. 41*
- **MAE** — mean absolute error — *Ch. 5*
- **Map projection** — mathematical mapping from ellipsoid to plane (UTM, Lambert, Mercator, …) — *Ch. 10*
- **MBES** — multibeam echo sounder; swath sonar producing many depths per ping — *Ch. 20*
- **Mean sea level (MSL)** — average sea level at a gauge over a tidal datum epoch (19 years in the US) — *Ch. 9*
- **Mesh** — surface represented by connected polygons (usually triangles), possibly multi-valued — *Ch. 46*
- **MGRS** — Military Grid Reference System; alphanumeric grid on UTM/UPS — *Ch. 60*
- **MHW / MHHW** — mean high water / mean higher high water; shoreline datums — *Ch. 9, 34*
- **MLLW** — mean lower low water; US chart datum — *Ch. 9*
- **Model card** — standardized documentation of an ML model's intended use, data, and evaluation — *Ch. 43*
- **Monte Carlo propagation** — uncertainty propagation by repeated sampling of input errors — *Ch. 5, App. B*
- **Morton / Hilbert curve** — space-filling curves used for spatial indexing — *Ch. 46, 60*
- **Motion compensation** — correcting sonar or lidar observations for platform roll, pitch, heave, yaw — *Ch. 13, 20*
- **MTF** — modulation transfer function; frequency response of a sensor or process — *Ch. 44*
- **Multi-valued surface** — a location with more than one legitimate elevation (bridges, overhangs) — *Ch. 35*

## N

- **NAD27 / NAD83** — North American Datums of 1927 and 1983 (with realizations) — *Ch. 8*
- **NADCON / VERTCON** — NGS grid transformations between US horizontal / vertical datums — *Ch. 8, 9*
- **NAPGD2022** — North American-Pacific Geopotential Datum of 2022; geoid-based vertical datum replacing NAVD88 — *Ch. 9, 73*
- **NASADEM** — reprocessed SRTM with improved void filling and ICESat control — *Ch. 55*
- **NATRF2022** — North American Terrestrial Reference Frame of 2022; plate-fixed frame replacing NAD83 — *Ch. 8, 73*
- **NAVD88** — North American Vertical Datum of 1988; levelling-based, tied to Father Point/Rimouski — *Ch. 9*
- **NBS** — NOAA National Bathymetric Source; living compilation with supersession — *Ch. 48*
- **nDSM** — normalized DSM; DSM minus DTM (object heights above ground) — *Ch. 4, 32*
- **NGVD29** — National Geodetic Vertical Datum of 1929 (Sea Level Datum of 1929) — *Ch. 9, 72*
- **NMAD** — normalized median absolute deviation; robust estimate of σ, $1.4826 \times \mathrm{MAD}$ — *Ch. 5, 53*
- **NMAS** — US National Map Accuracy Standards (1947) — *Ch. 53, 58*
- **Nodata** — sentinel value marking absent cells — ⚠ distinguish from zero and from filled — *Ch. 35*
- **Normal height** — height above the quasi-geoid (Molodensky); used in many European systems — *Ch. 7*
- **NPS / NPD** — nominal pulse spacing / density of a lidar survey — *Ch. 44*
- **NSRS** — US National Spatial Reference System — *Ch. 8*
- **NSSDA** — FGDC National Standard for Spatial Data Accuracy (1998) — *Ch. 53*
- **Nuth–Kääb co-registration** — DEM shift estimation from the aspect-dependence of elevation differences on slopes — *Ch. 41, App. B*
- **NVA / VVA** — non-vegetated / vegetated vertical accuracy (ASPRS Positional Accuracy Standards Ed. 1, 2014, and USGS Lidar Base Specification); NVA = 1.96 × RMSE$_z$, VVA = 95th percentile of absolute errors — ⚠ ASPRS Ed. 2 (2023) keeps NVA/VVA only as checkpoint strata and reports both as RMSE$_V$ (with RMSE$_H$ horizontally), dropping the 1.96× and 95th-percentile statistics and the VVA pass/fail — *Ch. 53, 70*
- **Nyquist frequency** — half the sampling rate; the highest representable spatial frequency — *Ch. 44*

## O

- **OAIS** — Open Archival Information System reference model (ISO 14721) — *Ch. 50*
- **Occlusion** — region not visible to a sensor because of intervening objects or terrain — *Ch. 35*
- **OGC** — Open Geospatial Consortium — *Ch. 70*
- **Open Location Code (plus codes)** — Google's short-code location encoding — *Ch. 60*
- **Openness (topographic)** — angular measure of terrain enclosure/exposure (Yokoyama) — *Ch. 57*
- **Orthometric height (H)** — height above the geoid along the plumb line; "elevation above sea level" — *Ch. 7*
- **Orthophoto / orthomosaic** — imagery rectified to a DEM so scale is uniform — *Ch. 22*
- **Outlier (blunder)** — gross error not described by the random error model — *Ch. 5*
- **Overhang** — surface element whose projection overlaps another at the same (x, y) — *Ch. 35*
- **Overviews (pyramids)** — reduced-resolution copies stored for fast display — *Ch. 46, 47*

## P

- **Patch test** — procedure for estimating MBES or lidar boresight angles from overlapping lines — *Ch. 25, 26*
- **PDAL** — Point Data Abstraction Library — *Ch. 71*
- **Photogrammetry** — measuring geometry from photographs — *Ch. 22*
- **Pixel-is-area / pixel-is-point** — see *grid registration* — *Ch. 10, 47*
- **Plate motion** — horizontal (and vertical) movement of tectonic plates, cm/yr — *Ch. 38*
- **Point cloud** — set of 3D points with attributes from lidar, sonar, or photogrammetry — *Ch. 46*
- **PPK / RTK** — post-processed / real-time kinematic GNSS using carrier phase — *Ch. 12*
- **PPP (-AR)** — precise point positioning (with ambiguity resolution) — *Ch. 12*
- **Precision** — repeatability of measurements; spread, not closeness to truth — *Ch. 5*
- **Priority-flood** — efficient depression-filling algorithm for DEMs — *Ch. 61*
- **PROJ** — open-source coordinate transformation library — *Ch. 10, 71*
- **PROV (W3C)** — provenance data model — *Ch. 50*
- **Provenance** — record of origin and derivation of data — *Ch. 50*
- **Pulse (lidar)** — one emitted laser shot; may yield several returns — *Ch. 18*

## Q

- **QL0–QL3** — USGS lidar quality levels by density and vertical accuracy (e.g., QL1: ≥ 8 pls/m², 10 cm RMSE$_z$ NVA) — *Ch. 70*
- **Quadtree / octree** — hierarchical 2D / 3D spatial subdivision — *Ch. 46*
- **Quantization noise** — error from rounding to a step $q$; σ = $q/\sqrt{12}$ — *Ch. 5, App. B*
- **Quasi-geoid** — reference surface for normal heights; coincides with the geoid at sea — *Ch. 7*

## R

- **Radar altimetry** — nadir radar ranging to sea, ice, or land surfaces — *Ch. 21*
- **RANSAC** — random sample consensus; robust model fitting — *Ch. 42*
- **Raw data** — unprocessed sensor observations (waveforms, pings, images, trajectories) — *Ch. 29, 50*
- **Ray tracing (sound)** — computing acoustic path through a sound-speed profile — *Ch. 20, App. B*
- **Refraction** — bending of light or sound at density/speed gradients; a range-dependent error — *Ch. 17, 19, 20*
- **Relative accuracy** — consistency of positions/heights between nearby points — *Ch. 53*
- **Resampling** — recomputing raster values on a new grid — *Ch. 10*
- **Resolution** — ambiguous: pixel size, point spacing, or smallest resolvable feature — ⚠ specify which — *Ch. 44*
- **RINEX** — Receiver Independent Exchange Format for GNSS observations — *Ch. 12*
- **RMSE** — root-mean-square error; $\sqrt{\text{bias}^2 + \sigma^2}$ — *Ch. 5*
- **Roughness** — local surface variability (e.g., σ of residuals from a plane) — *Ch. 57*
- **ROV** — remotely operated (tethered) underwater vehicle — *Ch. 16*

## S

- **S-44** — IHO Standards for Hydrographic Surveys (Ed. 6.1.0, 2022) — *Ch. 70*
- **S-57 / S-100 / S-101 / S-102** — IHO ENC transfer standard / universal hydrographic data model / next-generation ENC / bathymetric surface product — *Ch. 47, 70*
- **S2** — Google's spherical-cube hierarchical DGGS — *Ch. 60*
- **SAR** — synthetic aperture radar — *Ch. 21*
- **SBES** — single-beam echo sounder — *Ch. 20*
- **SBET** — smoothed best estimate of trajectory (GNSS/INS post-processing output) — *Ch. 13*
- **SDB** — satellite-derived bathymetry from optical imagery — *Ch. 23*
- **Seabed 2030** — Nippon Foundation–GEBCO project to map the ocean floor by 2030 — *Ch. 66, 73*
- **Selective Availability** — intentional GPS degradation, ended 2000-05-02 — *Ch. 12*
- **SfM** — structure from motion; photogrammetry from unordered images — *Ch. 22*
- **Shadow (radar/lidar)** — region unobserved because the terrain blocks the line of sight — *Ch. 21, 35*
- **Shoal-biased** — gridding or generalization that keeps the shallowest depth per cell — *Ch. 20, 62*
- **Shoreline** — legally or tidally defined land–water line (MHW, MLLW, LAT) — ⚠ not the visible water edge — *Ch. 34, 68*
- **Single-photon lidar** — lidar detecting individual photons for high-altitude, high-density collection — *Ch. 18*
- **Sky-view factor (SVF)** — fraction of the sky hemisphere visible from a point — *Ch. 57*
- **SLAM** — simultaneous localization and mapping — *Ch. 15*
- **Slope** — magnitude of the surface gradient, in degrees or percent — *Ch. 57, App. B*
- **Sound speed profile (SSP)** — sound speed vs depth, from CTD or SVP casts — *Ch. 20*
- **Spatial autocorrelation** — correlation of errors or values as a function of separation — *Ch. 5*
- **Splat (Gaussian splatting)** — rendering primitive for point-based radiance fields — *Ch. 46, 57*
- **Spline (thin-plate, tension)** — smooth interpolation minimizing curvature energy — *Ch. 31*
- **SRTM** — Shuttle Radar Topography Mission (2000) — *Ch. 21, 55*
- **STAC** — SpatioTemporal Asset Catalog specification — *Ch. 51*
- **Strip adjustment** — least-squares alignment of overlapping lidar strips — *Ch. 18, 29*
- **Stumpf ratio / Lyzenga model** — empirical log-ratio / radiative-transfer SDB algorithms — *Ch. 23*
- **Super-resolution** — inferring finer-resolution elevation from coarser input — ⚠ inference, not measurement — *Ch. 45*
- **Supersession** — rule by which newer or better data replace older in a compilation — *Ch. 48*
- **SWOT** — Surface Water and Ocean Topography mission (2022–) — *Ch. 66, 73*
- **Systematic error** — see *bias* — *Ch. 5*

## T

- **TanDEM-X** — DLR formation-flying X-band InSAR mission; source of the 12 m global DEM and Copernicus DEM — *Ch. 21, 55*
- **Terrain-aided navigation** — positioning by matching sensed terrain to a stored DEM — *Ch. 14*
- **THU** — total horizontal uncertainty (IHO, 95 %) — *Ch. 53, 70*
- **TID** — GEBCO Type Identifier; per-cell source-type code — *Ch. 48, 55*
- **Tidal datum** — vertical reference defined from tide observations over an epoch — *Ch. 9*
- **Tide correction** — reduction of soundings from instantaneous water level to chart datum — *Ch. 20*
- **TIN** — triangulated irregular network — *Ch. 46*
- **Topobathymetric DEM** — seamless land–seabed elevation model on one vertical datum — *Ch. 19, 66*
- **TPU** — total propagated uncertainty of a sounding (horizontal and vertical components) — *Ch. 20, 53*
- **Transverse Mercator / UTM** — conformal cylindrical projection / its 6° zone system — *Ch. 10*
- **TVU** — total vertical uncertainty (IHO, 95 %): $\sqrt{a^2 + (b d)^2}$ — *Ch. 53, 70*
- **TWI** — topographic wetness index — *Ch. 61*

## U

- **UAS / UAV** — uncrewed aircraft system / vehicle — *Ch. 16*
- **UKC** — under-keel clearance — *Ch. 62*
- **Uncertainty** — quantified doubt about a value (GUM); a property of knowledge, not a realized error — *Ch. 5*
- **Uncertainty raster** — per-cell σ or 95 % interval shipped with a DEM — *Ch. 47, 73*
- **UNCLOS** — UN Convention on the Law of the Sea (1982) — *Ch. 68*
- **USBL / LBL** — ultra-short / long baseline acoustic positioning — *Ch. 14*
- **US survey foot** — 1200/3937 m; deprecated 2022-12-31 — ⚠ 2 ppm from the international foot — *Ch. 68*
- **USV** — uncrewed surface vessel — *Ch. 16*

## V

- **Variogram** — plot of semivariance vs separation distance; models spatial correlation — *Ch. 5, 31*
- **VDatum** — NOAA tool for transforming among tidal, orthometric, and ellipsoidal datums — *Ch. 9*
- **Vertical datum** — reference surface for heights (ellipsoid, geoid-based, tidal, local) — *Ch. 9*
- **VLM** — vertical land motion — *Ch. 38*
- **Void** — region of a DEM with no valid data — *Ch. 35*
- **Void fill** — replacement of voids by interpolation or another source — ⚠ should be flagged — *Ch. 35, 48*
- **Voxel** — volumetric cell; 3D raster element — *Ch. 46*

## W

- **Water column (sonar)** — acoustic returns between transducer and seabed; used for feature and gas detection — *Ch. 20*
- **Wave-kinematics bathymetry** — depth inferred from wave celerity/dispersion in imagery — *Ch. 23*
- **Waveform** — see *full waveform* — *Ch. 18*
- **WGS 84** — World Geodetic System 1984; ellipsoid and frame with realizations G730–G2296 — *Ch. 8*
- **what3words** — proprietary 3 m-square word-triplet addressing — *Ch. 60*
- **White ribbon** — the nearshore gap between topographic and bathymetric coverage — *Ch. 19, 66*
- **WKT / WKT2** — well-known text for geometry / for CRS (ISO 19162) — *Ch. 8*

## X–Z

- **xDEM** — open-source Python library for DEM co-registration and uncertainty — *Ch. 41, 71*
- **XGEOID** — NGS experimental gravimetric geoid model series leading to GEOID2022 — *Ch. 7, 9*
- **Zarr** — chunked, compressed N-dimensional array storage format — *Ch. 47*
- **Zevenbergen–Thorne** — 4-neighbour finite-difference operator for slope and curvature — *Ch. 57, App. B*
- **Zone of confidence** — see *CATZOC* — *Ch. 62*

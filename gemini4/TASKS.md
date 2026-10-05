# TASKS.md — Execution Plan for Writing *The Digital Elevation Models Handbook*

This document tracks the end-to-end authoring, mathematical verification, historical fact-checking, and subagent peer review for every chapter and subsection of ***The Digital Elevation Models Handbook: From Physics and Sensors to Uncertainty, Semantics, and Applications*** (defined in [TOC.md](TOC.md)).

---

## 1. Mandatory Per-Subsection Authoring & Subagent Review Protocol

For **every subsection (`X.Y`)** in this handbook, the authoring workflow requires two explicit, sequential phases:

### Phase A: Draft Subsection (`Write X.Y`)
1. Draft the complete subsection in its corresponding chapter/subsection file (e.g., `book/part-01/ch-01/sec-01-01.md` or within `book/ch-XX.md`).
2. Ensure full technical depth covering:
   * Both **terrestrial (land)** and **marine/estuarine/lacustrine (bathymetry)** domains.
   * **Validation, correctness, error budgets, and uncertainty propagation** (THU, TVU, spatial autocorrelation, and downstream impact).
   * Explicit **mathematical equations** with every variable, coordinate frame, sign convention (elevation positive-up vs. depth positive-down), and SI unit defined.
   * Historical context anchored to [`schwehr/gis-history`](https://github.com/schwehr/gis-history).
   * Concrete **open-source** and **commercial/closed-source** software workflows.
   * **Common Pitfalls** and **Key Takeaways**.
   * **Curated, verifiable references** (real DOIs, USGS/NOAA/IHO/ASPRS report numbers, and seminal papers).

### Phase B: Subagent Review & Issue Correction (`Subagent Review & Fix X.Y`)
Immediately after drafting subsection `X.Y` (or when auditing the subsection specification), invoke a dedicated review subagent (`invoke_subagent`) to audit the subsection against the **10-Point Subsection Verification Rubric**:
1. **Physics & Mathematical Correctness:** Are all equations dimensionally consistent, free of sign/transpose/factor-of-2 errors, and properly derived?
2. **Uncertainty & Validation Rigor:** Does the subsection quantify error sources, bias vs. variance, and validation procedures rather than speaking in vague generalities?
3. **Land & Bathymetry Integration:** Are both land and underwater/coastal perspectives accurately represented?
4. **`gis-history` Alignment:** Are historical dates, inventions, satellites, file formats, and software milestones consistent with `https://github.com/schwehr/gis-history`?
5. **Standards & Manuals Compliance:** Are NOAA HSSD, NOAA FPM (1997/2020), IHO S-44/S-100/S-102, USGS 3DEP LBS, and ASPRS Positional Accuracy Standards cited and applied accurately?
6. **Software Ecosystem Accuracy:** Are tool names, CLI flags, library APIs (GDAL, PROJ, PDAL, MB-System, GMT, `xdem`, CARIS, Qimera, etc.), and open vs. closed licenses accurate?
7. **Edge Cases & Real-World Pathologies:** Are degenerate cases (overhangs, bridges/tunnels, moving ships/cars, steam plumes, fluid mud, leap seconds, custom datums, antimeridian seams) thoroughly addressed?
8. **Pitfalls & Key Takeaways Quality:** Are the pitfalls concrete failure modes encountered by practitioners, and are the takeaways actionable?
9. **Bibliographic Integrity:** Are all citations real, accurately attributed, and free of hallucinated titles or authors?
10. **Correction Loop:** Apply all fixes identified by the subagent directly to the file, verify the diff, and only then mark the review task `[x]`.

---

## 2. Phase 0: Repository & Book Infrastructure Setup

- [x] **Task 0.1:** Create comprehensive Table of Contents in [TOC.md](TOC.md) covering all land and bathymetric applications, sensors, geodesy, error/uncertainty, formats, semantics, visualization, cartography, legal/cost topics, and gap-review chapters.
- [x] **Task 0.2:** Create master task tracker in [TASKS.md](TASKS.md) with per-subsection authoring and subagent review tasks.
- [x] **Task 0.3:** Create shared Front Matter & Reference files:
  - [x] **Write 0.3.1:** `book/00-front-matter/notation-and-symbols.md` (Master mathematical notation table: coordinate frames, matrices, geodesy, acoustics, radiometry, uncertainty metrics).
  - [x] **Subagent Review & Fix 0.3.1:** Subagent review of `notation-and-symbols.md` for mathematical consistency across all 35 chapters.
  - [x] **Write 0.3.2:** `book/00-front-matter/acronyms-and-glossary.md` (Comprehensive glossary of terrestrial, photogrammetric, LiDAR, SAR, geodetic, and hydrographic terms).
  - [x] **Subagent Review & Fix 0.3.2:** Subagent review of `acronyms-and-glossary.md` for ontological precision and standard compliance (ISO/OGC/IHO/ASPRS/NOAA).
  - [x] **Write 0.3.3:** `book/00-front-matter/gis-history-timeline.md` (Curated chronological timeline of DEM, geodesy, positioning, and hydrography milestones from `schwehr/gis-history`).
  - [x] **Subagent Review & Fix 0.3.3:** Subagent review of `gis-history-timeline.md` against `https://github.com/schwehr/gis-history`.

---

## 3. Part-by-Part & Subsection-by-Subsection Book Authoring and Subagent Review Tasks

### PART I: Applications, Use Cases, and Operational Constraints

#### Chapter 1: The Landscape and Seascape of DEM Applications
- [x] **Write 1.1:** Terrestrial (Land) Applications (hydrology, geomorphology/hazards, civil engineering/transportation, forestry/ecology/agriculture, urban/telecom/energy, defense/autonomy).
- [x] **Subagent Review & Fix 1.1:** Subagent review of Subsection 1.1 and correction of any issues.
- [x] **Write 1.2:** Marine, Estuarine, and Lacustrine (Bathymetry) Applications (safety of navigation/UKC/charting, submarine/AUV navigation, tsunami/storm surge, offshore engineering/cables/wind, marine geology/oceanography, benthic ecology/oil spills, UNCLOS maritime law).
- [x] **Subagent Review & Fix 1.2:** Subagent review of Subsection 1.2 and correction of any issues.
- [x] **Write 1.3:** Cross-Domain Constraints: How End-Use Dictates Product Design (shoal-biased navigation vs. tallest-point aviation vs. hydro-enforced connectivity vs. unbiased volumetric mean; resolution vs. application matrix).
- [x] **Subagent Review & Fix 1.3:** Subagent review of Subsection 1.3 and correction of any issues.
- [x] **Write 1.4:** Historical Evolution (`gis-history` Context: plumb bob, 1807 US Coast Survey, 1854 John Snow, 1879 USGS, 1903 GEBCO, 1912 *Titanic* & 1914 SOLAS, 1929 Grand Banks turbidity current, 1952/1957/1977 Marie Tharp, 1963 CGIS, 1969 McHarg, 2005 *USS San Francisco* grounding, 2006 NOAA ERMA).
- [x] **Subagent Review & Fix 1.4:** Subagent review of Subsection 1.4 and correction of any issues.
- [x] **Write 1.5:** Mathematical Foundations (volumetric error covariance double integral, extreme-value shoal/obstacle statistics, shallow-water wave celerity sensitivity to depth error).
- [x] **Subagent Review & Fix 1.5:** Subagent review of Subsection 1.5 and correction of any issues.
- [x] **Write 1.6:** Software Ecosystem (GRASS, QGIS, WhiteboxTools, HEC-RAS, ANUGA, Delft3D, GDAL vs. ArcGIS Pro, CARIS, Qimera/Fledermaus, Civil 3D, OpenRoads, MIKE 21).
- [x] **Subagent Review & Fix 1.6:** Subagent review of Subsection 1.6 and correction of any issues.
- [x] **Write 1.7:** Common Pitfalls & Key Takeaways for Chapter 1.
- [x] **Subagent Review & Fix 1.7:** Subagent review of Subsection 1.7 and correction of any issues.
- [x] **Write 1.8:** Curated Key References for Chapter 1.
- [x] **Subagent Review & Fix 1.8:** Subagent review of Subsection 1.8 and correction of any issues.

---

### PART II: Mathematical, Geodetic, and Spatiotemporal Reference Foundations

#### Chapter 2: Geodesy, Horizontal Datums, Projections, and Coordinate Reference Systems
- [x] **Write 2.1:** The Shape of the Earth: Sphere, Ellipsoid, and Geoid (historical ellipsoids to GRS80/WGS84; ECEF vs. Geodetic vs. Local Tangent Plane; NAD27 to ITRF2020/NAD83/NATRF2022).
- [x] **Subagent Review & Fix 2.1:** Subagent review of Subsection 2.1 and correction of any issues.
- [x] **Write 2.2:** Map Projections and Distortion Impacts on DEMs (Conformal, Equal-Area, Equidistant; scale factor $k$ and grid convergence $\gamma$ impacts on slope/aspect/area; Web Mercator pitfalls; reprojection resampling artifacts).
- [x] **Subagent Review & Fix 2.2:** Subagent review of Subsection 2.2 and correction of any issues.
- [x] **Write 2.3:** Custom, Local, and Assumed Datums: What Happens When People Create Their Own Datums? (mine/plant grids, ground-to-grid combined scale factor, US Survey Foot vs. International Foot, reconciling local grids).
- [x] **Subagent Review & Fix 2.3:** Subagent review of Subsection 2.3 and correction of any issues.
- [x] **Write 2.4:** Historical Evolution (`gis-history` Context: Hipparchus, 1569 Mercator, 1791 GB Triangulation, 1830 Airy, 1855 Gall, 1861 Clarke, 1884 Meridian Conf., 1927 NAD27, 1942 UTM, 1980 GRS80/GCTP, 1983 Evenden PROJ, 1984 WGS84, 1985/1993 EPSG, 1987 Snyder PP 1395, 1994 PROJ4, 1999 WKT, 2018 PROJ RFC 1, 2019 GDAL RFC 73 / WKT2).
- [x] **Subagent Review & Fix 2.4:** Subagent review of Subsection 2.4 and correction of any issues.
- [x] **Write 2.5:** Mathematical Foundations (ECEF-Geodetic transformations, 7/14-parameter Helmert transformations, Tissot's indicatrix, metric tensor on projected surfaces, geodesic vs. planar slope).
- [x] **Subagent Review & Fix 2.5:** Subagent review of Subsection 2.5 and correction of any issues.
- [x] **Write 2.6:** Software Ecosystem (PROJ, GDAL, GeographicLib, PyPROJ vs. Esri Projection Engine, Blue Marble Geographic Calculator, FME, TBC).
- [x] **Subagent Review & Fix 2.6:** Subagent review of Subsection 2.6 and correction of any issues.
- [x] **Write 2.7:** Common Pitfalls & Key Takeaways for Chapter 2.
- [x] **Subagent Review & Fix 2.7:** Subagent review of Subsection 2.7 and correction of any issues.
- [x] **Write 2.8:** Curated Key References for Chapter 2.
- [x] **Subagent Review & Fix 2.8:** Subagent review of Subsection 2.8 and correction of any issues.

#### Chapter 3: Vertical Datums, the Geoid, Tides, and the Shoreline
- [x] **Write 3.1:** What Are Vertical Datums? (Ellipsoidal $h$, Geopotential $C$, Orthometric $H$, Normal $H^*$, Dynamic heights; EGM84/96/2008, GEOID18/2022; NGVD29, NAVD88, NAPGD2022, IGLD85; Tidal datums NTDE, LAT, MLLW, MLW, LMSL, MTL, MHW, MHHW, HAT).
- [x] **Subagent Review & Fix 3.1:** Subagent review of Subsection 3.1 and correction of any issues.
- [x] **Write 3.2:** Bridging the Land-Sea Interface: Vertical Datum Transformations ($h = H + N$, VDatum/VORF/CVDCW separation models, uncertainty propagation across estuaries and barrier islands).
- [x] **Subagent Review & Fix 3.2:** Subagent review of Subsection 3.2 and correction of any issues.
- [x] **Write 3.3:** What Is a Shoreline? (Physical/instantaneous swash line vs. tidal datum MHW/MLLW vs. ecological/mangrove/marsh fringe vs. legal ambulatory boundary; extracting shorelines from TBDEMs and bridging the intertidal white ribbon).
- [x] **Subagent Review & Fix 3.3:** Subagent review of Subsection 3.3 and correction of any issues.
- [x] **Write 3.4:** Historical Evolution (`gis-history` Context: 1833 Buttermilk mark, 1928 Hawley Manual, 1984 EGM84, 1985 GEOSAT, 1992 TOPEX/Poseidon, 1994 UNCLOS, 1996 EGM96, 2008 EGM2008).
- [x] **Subagent Review & Fix 3.4:** Subagent review of Subsection 3.4 and correction of any issues.
- [x] **Write 3.5:** Mathematical Foundations (Stokes' integral, spherical harmonic geoid expansion, Bruns' formula, harmonic tidal constituent analysis, vertical datum transformation variance propagation).
- [x] **Subagent Review & Fix 3.5:** Subagent review of Subsection 3.5 and correction of any issues.
- [x] **Write 3.6:** Software Ecosystem (NOAA VDatum, PROJ GTG grids, PyTMD, UTide, GMT vs. CARIS ERS, QPS Qimera, Hypack).
- [x] **Subagent Review & Fix 3.6:** Subagent review of Subsection 3.6 and correction of any issues.
- [x] **Write 3.7:** Common Pitfalls & Key Takeaways for Chapter 3.
- [x] **Subagent Review & Fix 3.7:** Subagent review of Subsection 3.7 and correction of any issues.
- [x] **Write 3.8:** Curated Key References for Chapter 3.
- [x] **Subagent Review & Fix 3.8:** Subagent review of Subsection 3.8 and correction of any issues.

#### Chapter 4: Plate Motion Models, Crustal Deformation, and Dynamic Datums
- [x] **Write 4.1:** Plate Motion Models and Secular Crustal Velocity (Euler poles, NNR-MORVEL56, ITRF2020 PMM, NOAA HTDP, Glacial Isostatic Adjustment ICE-6G/7G).
- [x] **Subagent Review & Fix 4.1:** Subagent review of Subsection 4.1 and correction of any issues.
- [x] **Write 4.2:** Dealing with Earthquake Deformation and Transient Crustal Motion (interseismic strain, coseismic slip steps—1960 Valdivia, 2004 Indian Ocean, 2011 Tōhoku—postseismic viscoelastic relaxation, deformation patching in DEMs, groundwater/oil subsidence).
- [x] **Subagent Review & Fix 4.2:** Subagent review of Subsection 4.2 and correction of any issues.
- [x] **Write 4.3:** Historical Evolution (`gis-history` Context: 1912 Wegener, 1960 Valdivia, 1960/62 Plate tectonics & Vine-Matthews-Morley, 1977 Parsons & Sclater, 1992 Cande & Kent, 1992 NOAA HTDP 1.0, 2004 Sumatra, 2011 Tōhoku).
- [x] **Subagent Review & Fix 4.3:** Subagent review of Subsection 4.3 and correction of any issues.
- [x] **Write 4.4:** Mathematical Foundations (Euler vector cross product, time-dependent coordinate trajectory with Heaviside coseismic steps and logarithmic postseismic decay, Okada 1985 elastic half-space dislocation equations).
- [x] **Subagent Review & Fix 4.4:** Subagent review of Subsection 4.4 and correction of any issues.
- [x] **Write 4.5:** Software Ecosystem (NOAA HTDP, PROJ `+proj=deformation`, GMT `backtracker`/`grdpmodeler`, MintPy, PySolid vs. Trimble RTX, Esri HTDP).
- [x] **Subagent Review & Fix 4.5:** Subagent review of Subsection 4.5 and correction of any issues.
- [x] **Write 4.6:** Common Pitfalls & Key Takeaways for Chapter 4.
- [x] **Subagent Review & Fix 4.6:** Subagent review of Subsection 4.6 and correction of any issues.
- [x] **Write 4.7:** Curated Key References for Chapter 4.
- [x] **Subagent Review & Fix 4.7:** Subagent review of Subsection 4.7 and correction of any issues.

---

### PART III: Positioning, Attitude, and Trajectory Estimation

#### Chapter 5: Positioning, GNSS, IMU/INS, and the History of Positioning
- [x] **Write 5.1:** The History of Positioning and Navigation (`gis-history` Deep Dive: plumb bob, compass, plane table, theodolite, Gunter's chain, pendulum clock, Rømer, quadrant/sextant, Harrison H4, Brunton compass, Gee, Project 3, Decca, LORAN/CHAYKA, 1942 INS, atomic clocks, Tellurometer, Kalman filter, Sputnik, GPS, GLONASS, NMEA 0183, Etak, RINEX, DGPS, BeiDou, SA off, WAAS, Galileo, 2024 smartphone ionosphere mapping).
- [x] **Subagent Review & Fix 5.1:** Subagent review of Subsection 5.1 and correction of any issues.
- [x] **Write 5.2:** Global Navigation Satellite Systems (GNSS) for Elevation Mapping (code vs. carrier phase, ionosphere/troposphere/multipath/PCV errors, why VDOP > HDOP, SBAS, RTK, PPK, Network RTK, PPP-AR).
- [x] **Subagent Review & Fix 5.2:** Subagent review of Subsection 5.2 and correction of any issues.
- [x] **Write 5.3:** Inertial Measurement Units (IMU), INS, and Sensor Fusion (RLG/FOG/MEMS, Allan variance, strapdown mechanization, loosely vs. tightly coupled EKF & RTS backward smoothing SBET, lever arms and boresight angles).
- [x] **Subagent Review & Fix 5.3:** Subagent review of Subsection 5.3 and correction of any issues.
- [x] **Write 5.4:** Underwater Positioning (LBL, SBL, USBL/SSBL, DVL bottom-lock, Paroscientific pressure depth Saunders-Fofonoff conversion, acoustic ray bending).
- [x] **Subagent Review & Fix 5.4:** Subagent review of Subsection 5.4 and correction of any issues.
- [x] **Write 5.5:** Mathematical Foundations (carrier-phase observation equation, full 3D direct georeferencing rigid-body transformation equation, RTS smoother).
- [x] **Subagent Review & Fix 5.5:** Subagent review of Subsection 5.5 and correction of any issues.
- [x] **Write 5.6:** Software Ecosystem (RTKLIB, PRIDE PPP-AR, Ginan, GNSS-SDR, Kalibr, GPSBabel vs. Applanix POSPac, NovAtel Inertial Explorer, TerraMatch, Delph INS, Sonardyne Fusion).
- [x] **Subagent Review & Fix 5.6:** Subagent review of Subsection 5.6 and correction of any issues.
- [x] **Write 5.7:** Common Pitfalls & Key Takeaways for Chapter 5.
- [x] **Subagent Review & Fix 5.7:** Subagent review of Subsection 5.7 and correction of any issues.
- [x] **Write 5.8:** Curated Key References for Chapter 5.
- [x] **Subagent Review & Fix 5.8:** Subagent review of Subsection 5.8 and correction of any issues.

#### Chapter 6: Simultaneous Localization and Mapping (SLAM)
- [x] **Write 6.1:** Foundations and Evolution of SLAM (Smith & Cheeseman 1986, EKF-SLAM, FastSLAM, Factor Graphs, LiDAR-Inertial LIO, Visual-Inertial VIO, Bathymetric SLAM).
- [x] **Subagent Review & Fix 6.1:** Subagent review of Subsection 6.1 and correction of any issues.
- [x] **Write 6.2:** Loop Closure, Drift, and Georeferencing SLAM Maps ($z$-drift in planar/corridor environments, place recognition, degenerate geometries, tying SLAM to GCPs/GNSS/prior DEMs).
- [x] **Subagent Review & Fix 6.2:** Subagent review of Subsection 6.2 and correction of any issues.
- [x] **Write 6.3:** Historical Evolution (`gis-history` Context: 1958 Kalman filter, 1981 RANSAC, 1986 Smith & Cheeseman, 1993 VEVI, 1994 CMU Dante II in Mt. Spurr, 2000 OpenCV).
- [x] **Subagent Review & Fix 6.3:** Subagent review of Subsection 6.3 and correction of any issues.
- [x] **Write 6.4:** Mathematical Foundations (MAP factor-graph non-linear least squares on $\text{SE}(3)$, point-to-plane ICP, observability eigenvalue analysis of $\mathbf{J}^T\mathbf{J}$).
- [x] **Subagent Review & Fix 6.4:** Subagent review of Subsection 6.4 and correction of any issues.
- [x] **Write 6.5:** Software Ecosystem (GTSAM, Ceres, g2o, Cartographer, LIO-SAM, Fast-LIO2, Kiss-ICP, RTAB-Map, Open3D vs. GeoSLAM/Faro, Emesent Hovermap, NavVis, Leica BLK2GO).
- [x] **Subagent Review & Fix 6.5:** Subagent review of Subsection 6.5 and correction of any issues.
- [x] **Write 6.6:** Common Pitfalls & Key Takeaways for Chapter 6.
- [x] **Subagent Review & Fix 6.6:** Subagent review of Subsection 6.6 and correction of any issues.
- [x] **Write 6.7:** Curated Key References for Chapter 6.
- [x] **Subagent Review & Fix 6.7:** Subagent review of Subsection 6.7 and correction of any issues.

---

### PART IV: Sensors, Platforms, and Physical Measurement Principles

#### Chapter 7: Platforms for Collecting Elevation Data
- [x] **Write 7.1:** Humans on Foot (spirit leveling, total stations, TLS, RTK poles, backpack/handheld SLAM, phone LiDAR, ODK/Ground/FieldKit/Rockd, surf-zone wading).
- [x] **Subagent Review & Fix 7.1:** Subagent review of Subsection 7.1 and correction of any issues.
- [x] **Write 7.2:** Car-Based and Rail-Based Surveying (Mobile Mapping Systems—MMS, Street View, autonomous vehicle fleets, DMI wheel odometry, urban canyon challenges).
- [x] **Subagent Review & Fix 7.2:** Subagent review of Subsection 7.2 and correction of any issues.
- [x] **Write 7.3:** Airborne Platforms: Balloons, Kites, Drones (UAS), and Crewed Aircraft (Nadar 1858 balloon, kite KAP, multi-rotor/VTOL/fixed-wing drones, crewed fixed-wing & helicopter pods).
- [x] **Subagent Review & Fix 7.3:** Subagent review of Subsection 7.3 and correction of any issues.
- [x] **Write 7.4:** Marine Platforms: Ships, USVs, Towed Bodies, ROVs, AUVs, and Submarines (hull/gondola/pole mounts, bubble sweepdown, dynamic squat/settlement, USVs, deep-tow layback, ROVs, AUVs, submarines).
- [x] **Subagent Review & Fix 7.4:** Subagent review of Subsection 7.4 and correction of any issues.
- [x] **Write 7.5:** Spaceborne Platforms (CORONA/Keyhole film return, optical stereo constellations, radar & lidar spacecraft from GEOSAT/SRTM/ICESat to SWOT/NISAR/Biomass).
- [x] **Subagent Review & Fix 7.5:** Subagent review of Subsection 7.5 and correction of any issues.
- [x] **Write 7.6:** Using Fixed Infrastructure to Detect the World (Argus coastal video stations, webcams, traffic cameras, GNSS-R reflectometry at CORS, DAS telecom fiber, bridge/dam/radar gauges).
- [x] **Subagent Review & Fix 7.6:** Subagent review of Subsection 7.6 and correction of any issues.
- [x] **Write 7.7:** Historical Evolution (`gis-history` Context: 1562 submarine, 1858 Nadar balloon, 1957 Sputnik, 1959 CORONA, 1964 Ranger 7, 1972 Landsat 1 & Apollo 17, 1984 Landsat 5, 1986 archival fish tags, 1999 Ikonos, 2000 SRTM & Wardriving, 2006 DJI, 2008 Street View, 2010 Planet Labs, 2011 OpenROV, 2017 FieldKit, 2018 Google Ground).
- [x] **Subagent Review & Fix 7.7:** Subagent review of Subsection 7.7 and correction of any issues.
- [x] **Write 7.8:** Mathematical Foundations (vessel dynamic squat & fuel draft equation, linear surface gravity wave dispersion inversion for depth).
- [x] **Subagent Review & Fix 7.8:** Subagent review of Subsection 7.8 and correction of any issues.
- [x] **Write 7.9:** Software Ecosystem (OpenDroneMap, ArduPilot/PX4, MB-System, cBathy, `gnssrefl` vs. Applanix, RiPROCESS, Kongsberg SIS, UgCS, Pix4Dcapture).
- [x] **Subagent Review & Fix 7.9:** Subagent review of Subsection 7.9 and correction of any issues.
- [x] **Write 7.10:** Common Pitfalls & Key Takeaways for Chapter 7.
- [x] **Subagent Review & Fix 7.10:** Subagent review of Subsection 7.10 and correction of any issues.
- [x] **Write 7.11:** Curated Key References for Chapter 7.
- [x] **Subagent Review & Fix 7.11:** Subagent review of Subsection 7.11 and correction of any issues.

#### Chapter 8: Photogrammetry, Stereo Cameras, and Structure from Motion (SfM)
- [x] **Write 8.1:** Classical Photogrammetry and Stereo Cameras (interior/exterior orientation, Brown-Conrady distortion, frame vs. pushbroom, RPCs, $B/H$ trade-offs, epipolar geometry, SGM/MGM/deep stereo matching).
- [x] **Subagent Review & Fix 8.1:** Subagent review of Subsection 8.1 and correction of any issues.
- [x] **Write 8.2:** Structure from Motion (SfM) and Multi-View Stereo (MVS) (SIFT/SuperPoint, RANSAC fundamental matrix, bundle adjustment, self-calibration radial doming error, underwater flat/dome port & two-media refractive photogrammetry).
- [x] **Subagent Review & Fix 8.2:** Subagent review of Subsection 8.2 and correction of any issues.
- [x] **Write 8.3:** Historical Evolution (`gis-history` Context: 1776 photogrammetry, 1826 photograph, 1858 Nadar, 1934 ASPRS, 1964 Ranger 7, 1966 VICAR, 1969 CCD, 1981 RANSAC, 1992 Tomasi & Kanade SfM, 1995 Exif, 1996 NASA Ames Stereo Pipeline, 2000 OpenCV, 2006 VisionWorkbench).
- [x] **Subagent Review & Fix 8.3:** Subagent review of Subsection 8.3 and correction of any issues.
- [x] **Write 8.4:** Mathematical Foundations (collinearity equations, robust bundle adjustment cost function, vertical parallax error propagation).
- [x] **Subagent Review & Fix 8.4:** Subagent review of Subsection 8.4 and correction of any issues.
- [x] **Write 8.5:** Software Ecosystem (NASA ASP, COLMAP, MicMac, OpenDroneMap, Meshroom, OpenCV, VisionWorkbench vs. Agisoft Metashape, Pix4D, SOCET GXP, ContextCapture, Inpho).
- [x] **Subagent Review & Fix 8.5:** Subagent review of Subsection 8.5 and correction of any issues.
- [x] **Write 8.6:** Common Pitfalls & Key Takeaways for Chapter 8.
- [x] **Subagent Review & Fix 8.6:** Subagent review of Subsection 8.6 and correction of any issues.
- [x] **Write 8.7:** Curated Key References for Chapter 8.
- [x] **Subagent Review & Fix 8.7:** Subagent review of Subsection 8.7 and correction of any issues.

#### Chapter 9: Topographic and Bathymetric LiDAR
- [x] **Write 9.1:** Topographic LiDAR Principles and Architectures (ToF/CW/FMCW, mirror/polygon/Palmer/Risley scanners, discrete return vs. full-waveform Gaussian decomposition, Geiger-mode & single-photon LiDAR SPL).
- [x] **Subagent Review & Fix 9.1:** Subagent review of Subsection 9.1 and correction of any issues.
- [x] **Write 9.2:** Bathymetric LiDAR (Bathylidar) vs. Topographic LiDAR (532 nm green vs. 1064/1550 nm NIR physics, Raman channel, air-water Snell refraction & speed slowdown, $K_d$/Secchi depth limits, shallow "white ribbon" ambiguity, forward-scattering shoal bias).
- [x] **Subagent Review & Fix 9.2:** Subagent review of Subsection 9.2 and correction of any issues.
- [x] **Write 9.3:** Spaceborne LiDAR Missions (ICESat GLAS, ICESat-2 ATLAS photon-counting topo/bathy, ISS GEDI full-waveform).
- [x] **Subagent Review & Fix 9.3:** Subagent review of Subsection 9.3 and correction of any issues.
- [x] **Write 9.4:** Historical Evolution (`gis-history` Context: 1676 Rømer, 1960 Laser, 1961 LiDAR, 2003 ICESat & LAS 1.0, 2011 PDAL, 2018 ICESat-2 & GEDI, 2021 COPC).
- [x] **Subagent Review & Fix 9.4:** Subagent review of Subsection 9.4 and correction of any issues.
- [x] **Write 9.5:** Mathematical Foundations (LiDAR range & waveform convolution integral, 3D vector Snell's Law refraction across tilted wave facets).
- [x] **Subagent Review & Fix 9.5:** Subagent review of Subsection 9.5 and correction of any issues.
- [x] **Write 9.6:** Software Ecosystem (PDAL, LAStools, PulseWaves, PhoREAL, SlideRule, pyGEDI, CloudCompare vs. TerraScan/TerraMatch, RiPROCESS/RiHYDRO, Leica Chiroptera, CZMIL HydroFusion, StripAlign).
- [x] **Subagent Review & Fix 9.6:** Subagent review of Subsection 9.6 and correction of any issues.
- [x] **Write 9.7:** Common Pitfalls & Key Takeaways for Chapter 9.
- [x] **Subagent Review & Fix 9.7:** Subagent review of Subsection 9.7 and correction of any issues.
- [x] **Write 9.8:** Curated Key References for Chapter 9.
- [x] **Subagent Review & Fix 9.8:** Subagent review of Subsection 9.8 and correction of any issues.

#### Chapter 10: Sonar Systems and Underwater Acoustics
- [x] **Write 10.1:** Underwater Acoustic Physics and Sound Speed Refraction (frequency vs. attenuation vs. beamwidth, Chen-Millero/Del Grosso sound speed equations, SVP thermoclines/haloclines, ray-tracing smile/frown errors).
- [x] **Subagent Review & Fix 10.1:** Subagent review of Subsection 10.1 and correction of any issues.
- [x] **Write 10.2:** The Many Types of Sonar (Single-Beam SBES, Multibeam MBES Mills Cross amplitude/phase detection, Interferometric/Phase-Differencing PDBS, Side-Scan SSS & Synthetic Aperture Sonar SAS/InSAS, Sub-Bottom Profilers SBP, Split-Beam & ADCP bottom-track).
- [x] **Subagent Review & Fix 10.2:** Subagent review of Subsection 10.2 and correction of any issues.
- [x] **Write 10.3:** Historical Evolution (`gis-history` Context: 1490 da Vinci, 1902 Atlas Elektronik, 1912 *Titanic*, 1913 sonar patent, 1931 Simrad/Kongsberg, 1962 US3144631A multibeam patent, 1977 SeaBeam 1st gen, 1979 CARIS, 1989 Hydrosweep DS 2nd gen, 1993 MB-System, 1994 `pfmabe`, 1998 GSF).
- [x] **Subagent Review & Fix 10.3:** Subagent review of Subsection 10.3 and correction of any issues.
- [x] **Write 10.4:** Mathematical Foundations (constant-gradient circular-arc acoustic ray-tracing, outer-beam depth error sensitivity to surface vs. profile sound velocity errors).
- [x] **Subagent Review & Fix 10.4:** Subagent review of Subsection 10.4 and correction of any issues.
- [x] **Write 10.5:** Software Ecosystem (MB-System, HydrOffice Sound Speed Manager & QC Tools, Kluster, `pfmabe` vs. CARIS HIPS & SIPS, QPS Qimera, Kongsberg SIS, Hypack, SonarWiz, NaviSuite).
- [x] **Subagent Review & Fix 10.5:** Subagent review of Subsection 10.5 and correction of any issues.
- [x] **Write 10.6:** Common Pitfalls & Key Takeaways for Chapter 10.
- [x] **Subagent Review & Fix 10.6:** Subagent review of Subsection 10.6 and correction of any issues.
- [x] **Write 10.7:** Curated Key References for Chapter 10.
- [x] **Subagent Review & Fix 10.7:** Subagent review of Subsection 10.7 and correction of any issues.

#### Chapter 11: Radar, SAR, Satellite Altimetry, Satellite-Derived Bathymetry (SDB), and Auxiliary Geophysics
- [x] **Write 11.1:** Synthetic Aperture Radar (SAR) and Interferometric SAR (InSAR) (layover/foreshortening/shadow, X/C/L/P-band canopy penetration & PolInSAR, bistatic single-pass vs. repeat-pass InSAR, phase unwrapping, radargrammetry).
- [x] **Subagent Review & Fix 11.1:** Subagent review of Subsection 11.1 and correction of any issues.
- [x] **Write 11.2:** Satellite Radar Altimetry and Swath Interferometric Altimetry (pulse-limited & delay-Doppler altimetry from GEOSAT/TOPEX to CryoSat-2/Sentinel-6, SWOT KaRIn wide-swath interferometry).
- [x] **Subagent Review & Fix 11.2:** Subagent review of Subsection 11.2 and correction of any issues.
- [x] **Write 11.3:** Satellite-Derived Bathymetry (SDB) from Optical Imagery (blue/green radiative transfer, Lyzenga & Stumpf log-ratio models, physics-based hyperspectral inversion with PACE/EMIT/Sentinel-2, wave-kinematics SDB, ICESat-2 + SDB fusion, albedo/turbidity failure modes).
- [x] **Subagent Review & Fix 11.3:** Subagent review of Subsection 11.3 and correction of any issues.
- [x] **Write 11.4:** Using Other Data to Help Mapping: Gravity, Magnetics, and Seismic (Smith & Sandwell satellite altimetry gravity-predicted bathymetry & flexural isostasy limits, airborne gravimetry GRAV-D, aeromagnetics/paleomagnetism, GPR & AEM).
- [x] **Subagent Review & Fix 11.4:** Subagent review of Subsection 11.4 and correction of any issues.
- [x] **Write 11.5:** Historical Evolution (`gis-history` Context: seafloor ages & magnetic reversals, 1797 Humboldt, 1904 Radar, 1951 SAR, 1956 Blackett magnetometer, 1960/62 Vine-Matthews-Morley, 1972 Landsat 1, 1985 GEOSAT, 1988 GMT, 1992 TOPEX/Poseidon, 1997 Smith & Sandwell, 2000 SRTM & EO-1 Hyperion, 2014 Sentinel-1, 2015 Sentinel-2, 2022 EMIT, 2024 PACE, 2025 Biomass).
- [x] **Subagent Review & Fix 11.5:** Subagent review of Subsection 11.5 and correction of any issues.
- [x] **Write 11.6:** Mathematical Foundations (InSAR phase-to-height equation, Stumpf log-ratio SDB equation, Parker-Oldenburg Fourier gravity-to-bathymetry upward continuation relation).
- [x] **Subagent Review & Fix 11.6:** Subagent review of Subsection 11.6 and correction of any issues.
- [x] **Write 11.7:** Software Ecosystem (ISCE2/3, SNAP, GMTSAR, MintPy, GMT, ACOLITE, Polymer vs. ENVI SARscape, GAMMA, EOMAP, TCarta).
- [x] **Subagent Review & Fix 11.7:** Subagent review of Subsection 11.7 and correction of any issues.
- [x] **Write 11.8:** Common Pitfalls & Key Takeaways for Chapter 11.
- [x] **Subagent Review & Fix 11.8:** Subagent review of Subsection 11.8 and correction of any issues.
- [x] **Write 11.9:** Curated Key References for Chapter 11.
- [x] **Subagent Review & Fix 11.9:** Subagent review of Subsection 11.9 and correction of any issues.

---

### PART V: Calibration, Survey Planning, Ground Truth, and Uncertainty

#### Chapter 12: Calibration Targets, Reference Stations, and Ground Control Points (GCPs)
- [x] **Write 12.1:** Active Calibration and Reference Infrastructure (CORS & IGS networks, ANTEX antenna calibrations, active SAR transponders/PARCs, NWLON tide gauges & benchmark ties).
- [x] **Subagent Review & Fix 12.1:** Subagent review of Subsection 12.1 and correction of any issues.
- [x] **Write 12.2:** Static Calibration Locations and Monuments on the Planet (1833 Buttermilk mark, 3D deep-rod marks, 1930s Siemens star & 2010 Google Mountain View rooftop Siemens star, 2015 NPS King Hall rooftop QR code, 2007 USGS/CEOS Cal/Val Test Sites Catalog, LiDAR calibration runways/roofs, sonar patch-test beds).
- [x] **Subagent Review & Fix 12.2:** Subagent review of Subsection 12.2 and correction of any issues.
- [x] **Write 12.3:** Ground Control Points (GCPs) vs. Independent Check Points (CPs) (strict separation of calibration vs. validation points, multi-modal target design, spatial & elevation network geometry).
- [x] **Subagent Review & Fix 12.3:** Subagent review of Subsection 12.3 and correction of any issues.
- [x] **Write 12.4:** Ground Truth and Calibration Datasets: Creation, Validation, and Use ($3\times$ accuracy rule, land-cover/benthic stratification, preventing ML spatial data leakage).
- [x] **Subagent Review & Fix 12.4:** Subagent review of Subsection 12.4 and correction of any issues.
- [x] **Write 12.5:** Historical Evolution (`gis-history` Context: 1807 Hassler, 1833 Buttermilk mark, 1930s Siemens star, 1996 DGPS, 2007 USGS/CEOS Test Sites Catalog, 2010 Google Siemens Star, 2015 NPS rooftop QR code).
- [x] **Subagent Review & Fix 12.5:** Subagent review of Subsection 12.5 and correction of any issues.
- [x] **Write 12.6:** Mathematical Foundations (trihedral corner reflector RCS equation, ESF $\to$ LSF $\to$ MTF Fourier chain for effective resolution).
- [x] **Subagent Review & Fix 12.6:** Subagent review of Subsection 12.6 and correction of any issues.
- [x] **Write 12.7:** Software Ecosystem (OpenCV AprilTag/ChArUco, PDAL, QGIS vs. TerraMatch, Metashape, Pix4D, Leica Cyclone).
- [x] **Subagent Review & Fix 12.7:** Subagent review of Subsection 12.7 and correction of any issues.
- [x] **Write 12.8:** Common Pitfalls & Key Takeaways for Chapter 12.
- [x] **Subagent Review & Fix 12.8:** Subagent review of Subsection 12.8 and correction of any issues.
- [x] **Write 12.9:** Curated Key References for Chapter 12.
- [x] **Subagent Review & Fix 12.9:** Subagent review of Subsection 12.9 and correction of any issues.

#### Chapter 13: Survey Planning for Calibration, Error Reduction, and Monitoring
- [x] **Write 13.1:** Geometric Survey Design: Overlap, Cross-Lines, and Boresight Patterns (swath overlap rules, orthogonal cross-lines/tie-lines, hydrographic patch test & LiDAR boresight flight geometry for roll/pitch/yaw/latency).
- [x] **Subagent Review & Fix 13.1:** Subagent review of Subsection 13.1 and correction of any issues.
- [x] **Write 13.2:** Environmental and Temporal Survey Scheduling (PDOP/ionosphere windows, high-tide boat + low-tide LiDAR intertidal overlap, SVP cast triggers, sun angle & sea-state limits).
- [x] **Subagent Review & Fix 13.2:** Subagent review of Subsection 13.2 and correction of any issues.
- [x] **Write 13.3:** Real-Time Quality Assurance (QA) During Acquisition (live TPU heatmaps, holiday/gap detection, cross-line discrepancy alerts prior to demobilization).
- [x] **Subagent Review & Fix 13.3:** Subagent review of Subsection 13.3 and correction of any issues.
- [x] **Write 13.4:** Historical Evolution (`gis-history` Context: 1928 Hawley Manual, 1976 Hydrographic Manual 4th ed., 1997/2020 NOAA Field Procedures Manual, 2000 NOAA HSSD).
- [x] **Subagent Review & Fix 13.4:** Subagent review of Subsection 13.4 and correction of any issues.
- [x] **Write 13.5:** Mathematical Foundations (boresight observability matrix & Jacobian rank analysis showing why flat vs. sloped terrain is required for each angle).
- [x] **Subagent Review & Fix 13.5:** Subagent review of Subsection 13.5 and correction of any issues.
- [x] **Write 13.6:** Software Ecosystem (HydrOffice QC Tools, Kluster, QGIS, ODM vs. Hypack, Qinsy, Kongsberg SIS, Leica FlightPro, RiPARAMETER).
- [x] **Subagent Review & Fix 13.6:** Subagent review of Subsection 13.6 and correction of any issues.
- [x] **Write 13.7:** Common Pitfalls & Key Takeaways for Chapter 13.
- [x] **Subagent Review & Fix 13.7:** Subagent review of Subsection 13.7 and correction of any issues.
- [x] **Write 13.8:** Curated Key References for Chapter 13.
- [x] **Subagent Review & Fix 13.8:** Subagent review of Subsection 13.8 and correction of any issues.

#### Chapter 14: Error Theory, Total Propagated Uncertainty (TPU), and Forensic Evaluation of Third-Party DEMs
- [x] **Write 14.1:** Taxonomy of DEM Errors (gross blunders, systematic biases, random noise, and spatially autocorrelated multi-scale errors).
- [x] **Subagent Review & Fix 14.1:** Subagent review of Subsection 14.1 and correction of any issues.
- [x] **Write 14.2:** Total Propagated Uncertainty (TPU): Horizontal (THU) and Vertical (TVU) (Jacobian covariance propagation, RMSE vs. LE95 vs. NVA/VVA quantiles vs. robust NMAD, derivative noise amplification).
- [x] **Subagent Review & Fix 14.2:** Subagent review of Subsection 14.2 and correction of any issues.
- [x] **Write 14.3:** Forensic Evaluation: How to Evaluate Others' Data Products When You Don't Have All the Info (multi-azimuth hillshade & high-pass filters, 2D FFT spectral striping/aliasing detection, fractional-elevation & slope histograms for quantization/terracing, Nuth & Kääb 3D co-registration against ICESat-2/GEDI, detecting undocumented void fills).
- [x] **Subagent Review & Fix 14.3:** Subagent review of Subsection 14.3 and correction of any issues.
- [x] **Write 14.4:** Historical Evolution (`gis-history` Context: 1948 Shannon, 1958 Kalman, 1998 FGDC NSSDA, 2000 NOAA HSSD, 2003 ISO 19115, 2006 CUBE/BAG, 2018 ICESat-2).
- [x] **Subagent Review & Fix 14.4:** Subagent review of Subsection 14.4 and correction of any issues.
- [x] **Write 14.5:** Mathematical Foundations (Nuth & Kääb 3D shift regression, Höhle & Höhle robust NMAD estimator, autocorrelated slope error variance).
- [x] **Subagent Review & Fix 14.5:** Subagent review of Subsection 14.5 and correction of any issues.
- [x] **Write 14.6:** Software Ecosystem (`xdem`, PDAL, CloudCompare, HydrOffice QC Tools, SciPy/`scikit-gstat` vs. QPS CrossCheck, CARIS QC, Global Mapper, ArcGIS Geostatistical Analyst).
- [x] **Subagent Review & Fix 14.6:** Subagent review of Subsection 14.6 and correction of any issues.
- [x] **Write 14.7:** Common Pitfalls & Key Takeaways for Chapter 14.
- [x] **Subagent Review & Fix 14.7:** Subagent review of Subsection 14.7 and correction of any issues.
- [x] **Write 14.8:** Curated Key References for Chapter 14.
- [x] **Subagent Review & Fix 14.8:** Subagent review of Subsection 14.8 and correction of any issues.

---

### PART VI: Data Representations, Geometry, Resolution, and File Formats

#### Chapter 15: Point Clouds, Full Waveforms, Grids, TINs, Variable-Resolution Systems, and Overviews
- [x] **Write 15.1:** From Raw Sensor Telemetry to Structured Products (end-to-end processing pipeline architecture).
- [x] **Subagent Review & Fix 15.1:** Subagent review of Subsection 15.1 and correction of any issues.
- [x] **Write 15.2:** Point Clouds and Full Waveforms (discrete returns vs. digitized waveforms, attributes, octrees/kd-trees/space-filling curves).
- [x] **Subagent Review & Fix 15.2:** Subagent review of Subsection 15.2 and correction of any issues.
- [x] **Write 15.3:** Regular Grids (Rasters) vs. Triangulated Irregular Networks (TINs) (Pixel-is-Area vs. Pixel-is-Point half-pixel shift, IDW/Spline/Kriging/CUBE gridding, Constrained Delaunay TINs with breaklines).
- [x] **Subagent Review & Fix 15.3:** Subagent review of Subsection 15.3 and correction of any issues.
- [x] **Write 15.4:** Variable-Resolution Systems and Multi-Resolution Hierarchies (Quadtrees, ROAM, AMR, Variable-Resolution BAGs / CHRT).
- [x] **Subagent Review & Fix 15.4:** Subagent review of Subsection 15.4 and correction of any issues.
- [x] **Write 15.5:** Overviews (Pyramids) and Multi-Scale Decimation (why mean/bilinear overviews fail in navigation; shoal-biased min-depth and max-obstacle overview pyramids).
- [x] **Subagent Review & Fix 15.5:** Subagent review of Subsection 15.5 and correction of any issues.
- [x] **Write 15.6:** Historical Evolution (`gis-history` Context: 1965 Billingsley "pixel", 1974 Quadtree, 1978 Peucker et al. TIN, 1988 GMT `surface`, 2003 CUBE & LAS, 2006 BAG, 2011 PDAL, 2021 COPC).
- [x] **Subagent Review & Fix 15.6:** Subagent review of Subsection 15.6 and correction of any issues.
- [x] **Write 15.7:** Mathematical Foundations (Smith & Wessel biharmonic spline-in-tension PDE, CUBE Bayesian Kalman depth hypothesis updating).
- [x] **Subagent Review & Fix 15.7:** Subagent review of Subsection 15.7 and correction of any issues.
- [x] **Write 15.8:** Software Ecosystem (PDAL, GDAL, GMT, CGAL, WhiteboxTools, Entwine, Potree vs. CARIS, Qimera, LAStools, Esri).
- [x] **Subagent Review & Fix 15.8:** Subagent review of Subsection 15.8 and correction of any issues.
- [x] **Write 15.9:** Common Pitfalls & Key Takeaways for Chapter 15.
- [x] **Subagent Review & Fix 15.9:** Subagent review of Subsection 15.9 and correction of any issues.
- [x] **Write 15.10:** Curated Key References for Chapter 15.
- [x] **Subagent Review & Fix 15.10:** Subagent review of Subsection 15.10 and correction of any issues.

#### Chapter 16: Discrete Global Grid Systems (S2, H3) and Special Location Coding Schemes
- [x] **Write 16.1:** Space-Filling Curves and Discrete Global Grid Systems (Peano 1890, Hilbert 1891, Morton Z-order, Google S2 cube-Hilbert, Uber H3 icosahedral hexagons, rHEALPix/ISEA).
- [x] **Subagent Review & Fix 16.1:** Subagent review of Subsection 16.1 and correction of any issues.
- [x] **Write 16.2:** Storing and Analyzing Elevation on S2 and H3 Cells (isotropic 6-neighbor gradients on H3 vs. non-exact parent-child containment, spherical vs. ellipsoidal latitude discrepancies).
- [x] **Subagent Review & Fix 16.2:** Subagent review of Subsection 16.2 and correction of any issues.
- [x] **Write 16.3:** Issues with Special Location Coding Schemes (Geohash seam/aspect distortion, Open Location Code / Plus Codes 2014, What3Words 2013 proprietary/homophone/non-hierarchical safety hazards, MGRS, FIPS, ISO 3166).
- [x] **Subagent Review & Fix 16.3:** Subagent review of Subsection 16.3 and correction of any issues.
- [x] **Write 16.4:** Historical Evolution (`gis-history` Context: 1890 Peano, 1891 Hilbert, 1970 ISO 3166, 1974 Quadtree & FIPS, 2011 S2, 2013 What3Words, 2014 Open Location Code, 2018 H3).
- [x] **Subagent Review & Fix 16.4:** Subagent review of Subsection 16.4 and correction of any issues.
- [x] **Write 16.5:** Mathematical Foundations (Hilbert curve locality bound, discrete Laplacian and gradient operators on hexagonal H3 grids).
- [x] **Subagent Review & Fix 16.5:** Subagent review of Subsection 16.5 and correction of any issues.
- [x] **Write 16.6:** Software Ecosystem (`s2geometry`, `h3`/`h3-py`, `dggridR`, DuckDB/PostGIS H3, OLC vs. What3Words API, BigQuery GIS, Snowflake).
- [x] **Subagent Review & Fix 16.6:** Subagent review of Subsection 16.6 and correction of any issues.
- [x] **Write 16.7:** Common Pitfalls & Key Takeaways for Chapter 16.
- [x] **Subagent Review & Fix 16.7:** Subagent review of Subsection 16.7 and correction of any issues.
- [x] **Write 16.8:** Curated Key References for Chapter 16.
- [x] **Subagent Review & Fix 16.8:** Subagent review of Subsection 16.8 and correction of any issues.

#### Chapter 17: Vector Data Issues in Elevation Modeling
- [x] **Write 17.1:** Vector Primitives and Dimensionality: 2D, 2.5D, and True 3D (OGC Simple Features `Z`/`M`, breakdown of $z = f(x,y)$ on vertical walls, `PolyhedralSurfaceZ`, `TINZ`, CityGML, IFC).
- [x] **Subagent Review & Fix 17.1:** Subagent review of Subsection 17.1 and correction of any issues.
- [x] **Write 17.2:** Topological Integrity and Vector Pathologies (Corbett 1979 topology, winding order, self-intersections, slivers, floating-point robustness, antimeridian/pole wrapping).
- [x] **Subagent Review & Fix 17.2:** Subagent review of Subsection 17.2 and correction of any issues.
- [x] **Write 17.3:** Breaklines, Contours, and Hydro-Enforcement Vectors (hard vs. soft breaklines, hydro-flattening vs. culvert breaching, contour flat-triangle wedding-cake artifacts).
- [x] **Subagent Review & Fix 17.3:** Subagent review of Subsection 17.3 and correction of any issues.
- [x] **Write 17.4:** What Happens When Roads Cross or a Road Goes Under Buildings? (multi-level highway interchanges, tunnels, underpasses, skybridges, multi-surface elevation stacks vs. 3D topological graphs).
- [x] **Subagent Review & Fix 17.4:** Subagent review of Subsection 17.4 and correction of any issues.
- [x] **Write 17.5:** Historical Evolution (`gis-history` Context: 1959 Bézier, 1973 GIRAS, 1979 Corbett Topology & MOSS, 1982 Arc/Info, 1996 CGAL & FME, 1997 Simple Features & WKT, 1998 Shapefile, 2000 JTS & GML, 2001 PostGIS, 2002 GEOS, 2004 OSM, 2008 GeoJSON & SpatiaLite, 2013 GeoPandas, 2021 GeoParquet, 2023 Overture Maps).
- [x] **Subagent Review & Fix 17.5:** Subagent review of Subsection 17.5 and correction of any issues.
- [x] **Write 17.6:** Mathematical Foundations (Shewchuk adaptive-precision `Orient2D`/`Orient3D`/`InCircle` predicates, Hutchinson ANUDEM drainage-enforced spline).
- [x] **Subagent Review & Fix 17.6:** Subagent review of Subsection 17.6 and correction of any issues.
- [x] **Write 17.7:** Software Ecosystem (GEOS, JTS, CGAL, PostGIS/SFCGAL, Shapely, GeoPandas, GDAL/OGR, WhiteboxTools, GRASS vs. ArcGIS, FME, MicroStation).
- [x] **Subagent Review & Fix 17.7:** Subagent review of Subsection 17.7 and correction of any issues.
- [x] **Write 17.8:** Common Pitfalls & Key Takeaways for Chapter 17.
- [x] **Subagent Review & Fix 17.8:** Subagent review of Subsection 17.8 and correction of any issues.
- [x] **Write 17.9:** Curated Key References for Chapter 17.
- [x] **Subagent Review & Fix 17.9:** Subagent review of Subsection 17.9 and correction of any issues.

#### Chapter 18: Resolution, Pixel Size, Oversampling, Precision, and Super-Resolution
- [x] **Write 18.1:** Resolution vs. Pixel Size vs. Effective Resolution (GSD vs. beam footprint vs. Nyquist-Shannon & MTF effective resolution; the oversampling fallacy).
- [x] **Subagent Review & Fix 18.1:** Subagent review of Subsection 18.1 and correction of any issues.
- [x] **Write 18.2:** Resolution vs. Numerical Precision vs. Accuracy (`Int16` terracing steps, scale/offset, `Float32`/`Float64`, false ASCII precision vs. LERC/ZSTD bit-plane compression).
- [x] **Subagent Review & Fix 18.2:** Subagent review of Subsection 18.2 and correction of any issues.
- [x] **Write 18.3:** How the Resolution of the Resulting Product Changes What Is Appropriate (scale-dependent hydraulic roughness, sub-grid channels vs. resolved street curbs/boulders).
- [x] **Subagent Review & Fix 18.3:** Subagent review of Subsection 18.3 and correction of any issues.
- [x] **Write 18.4:** Super-Resolution of DEMs: Classical Physics vs. Machine Learning (Shape-from-Shading / sensor fusion vs. CNN/GAN/Diffusion super-resolution; hallucinated geomorphology, conservation of mass, uncertainty inflation).
- [x] **Subagent Review & Fix 18.4:** Subagent review of Subsection 18.4 and correction of any issues.
- [x] **Write 18.5:** Historical Evolution (`gis-history` Context: 1732 bits, 1930s Siemens star, 1948 Shannon sampling theorem, 1965 pixel, 2010 Google Siemens star, 2015 TensorFlow, 2021 TorchGeo).
- [x] **Subagent Review & Fix 18.5:** Subagent review of Subsection 18.5 and correction of any issues.
- [x] **Write 18.6:** Mathematical Foundations (PSF + decimation forward model, Shape-from-Shading variational PDE anchored to low-resolution altimetry).
- [x] **Subagent Review & Fix 18.6:** Subagent review of Subsection 18.6 and correction of any issues.
- [x] **Write 18.7:** Software Ecosystem (GDAL, OTB, NASA ASP `sfs`, TorchGeo, PyTorch, `xdem` vs. Esri Deep Learning, ENVI).
- [x] **Subagent Review & Fix 18.7:** Subagent review of Subsection 18.7 and correction of any issues.
- [x] **Write 18.8:** Common Pitfalls & Key Takeaways for Chapter 18.
- [x] **Subagent Review & Fix 18.8:** Subagent review of Subsection 18.8 and correction of any issues.
- [x] **Write 18.9:** Curated Key References for Chapter 18.
- [x] **Subagent Review & Fix 18.9:** Subagent review of Subsection 18.9 and correction of any issues.

#### Chapter 19: Key File Formats, Metadata, Archiving, and Data Discovery (STAC & Beyond)
- [x] **Write 19.1:** Key File Formats for Sensors and Products (RINEX, NMEA, GSF, `.all`/`.kmall`, `.s7k`, PulseWaves; LAS/LAZ, COPC, E57, GeoParquet/GeoArrow; TIFF/GeoTIFF/COG, BAG/VR-BAG, S-102, NetCDF, HDF5, Zarr, IceChunk, FITS, VICAR, PFM, GeoPackage).
- [x] **Subagent Review & Fix 19.1:** Subagent review of Subsection 19.1 and correction of any issues.
- [x] **Write 19.2:** Metadata: Making a DEM Usable and Auditable (7 mandatory metadata pillars, FGDC CSDGM, ISO 19115/19157, NASA GCMD Keywords, INSPIRE, WKT2).
- [x] **Subagent Review & Fix 19.2:** Subagent review of Subsection 19.2 and correction of any issues.
- [x] **Write 19.3:** Searching for the Right Data and Data Type: STAC and Modern Catalogs (STAC 1.0/1.1, `proj`/`pointcloud`/`raster` extensions, STAC GeoParquet + DuckDB, Earth Engine Catalog, Planetary Computer, Digital Coast, OpenTopography, IHO DCDB).
- [x] **Subagent Review & Fix 19.3:** Subagent review of Subsection 19.3 and correction of any issues.
- [x] **Write 19.4:** Archiving and Long-Term Data Preservation (raw sensor + trajectory retention vs. products, bit rot, format obsolescence lessons from Flash EOL / SGI demise, checksums, DOIs).
- [x] **Subagent Review & Fix 19.4:** Subagent review of Subsection 19.4 and correction of any issues.
- [x] **Write 19.5:** Historical Evolution (`gis-history` Context: 1966 VICAR, 1974 FIPS, 1981 FITS, 1984 NMEA, 1987 GCMD, 1988 NetCDF, 1989 RINEX, 1990 HDF & FGDC, 1991 `libtiff`, 1994 `pfmabe` & OGC & FGDC metadata, 1995 GeoTIFF, 1998 Shapefile & GSF, 1999 `libgeotiff` & WKT, 2000 SQLite & GDAL, 2003 LAS & ISO 19115, 2008 GeoJSON, 2014 GeoPackage, 2015 Zarr, 2017–2024 STAC & STAC GeoParquet & COPC & IceChunk).
- [x] **Subagent Review & Fix 19.5:** Subagent review of Subsection 19.5 and correction of any issues.
- [x] **Write 19.6:** Mathematical Foundations (LERC max-error bound, LAZ arithmetic coding entropy bound).
- [x] **Subagent Review & Fix 19.6:** Subagent review of Subsection 19.6 and correction of any issues.
- [x] **Write 19.7:** Software Ecosystem (GDAL, `libtiff`, `libgeotiff`, PDAL, `laszip`, ONS `bag`, `xarray`, `zarr`, `icechunk`, `pystac`, DuckDB vs. FME, ArcGIS Portal, CARIS Bathy DataBASE).
- [x] **Subagent Review & Fix 19.7:** Subagent review of Subsection 19.7 and correction of any issues.
- [x] **Write 19.8:** Common Pitfalls & Key Takeaways for Chapter 19.
- [x] **Subagent Review & Fix 19.8:** Subagent review of Subsection 19.8 and correction of any issues.
- [x] **Write 19.9:** Curated Key References for Chapter 19.
- [x] **Subagent Review & Fix 19.9:** Subagent review of Subsection 19.9 and correction of any issues.

---

### PART VII: Surface Semantics, Feature Extraction, and the Dynamic Earth

#### Chapter 20: Naming, Ontologies, and the Confusing Definitions of Surface Objects
- [x] **Write 20.1:** Naming and Definitions: The Alphabet Soup of Elevation Models (DEM, DSM, DTM, nDSM/CHM, DBM, TBDEM/CUDEM).
- [x] **Subagent Review & Fix 20.1:** Subagent review of Subsection 20.1 and correction of any issues.
- [x] **Write 20.2:** The Confusing Definitions of Buildings, Roads, Bridges, and Other Objects (what counts as a building/road; when bridges, culverts, elevated pipes, piers, levees, and breakwaters are kept vs. removed across DSM, DTM, Hydro-DEM, and True Ortho surfaces).
- [x] **Subagent Review & Fix 20.2:** Subagent review of Subsection 20.2 and correction of any issues.
- [x] **Write 20.3:** Dealing with Wires, Powerlines, Solar Panels, and Antennas (thin-wire dropout, wind sway and thermal/load catenary sag across timescales; solar panel specular dropouts/multipath; antenna/guy-wire preservation against outlier filters).
- [x] **Subagent Review & Fix 20.3:** Subagent review of Subsection 20.3 and correction of any issues.
- [x] **Write 20.4:** Dealing with Innerspace: Inside-Building and Subterranean Issues (indoor SLAM, parking decks, tunnels, caves, mines, glass skylight laser penetration, BIM/IFC-to-GIS integration).
- [x] **Subagent Review & Fix 20.4:** Subagent review of Subsection 20.4 and correction of any issues.
- [x] **Write 20.5:** Historical Evolution (`gis-history` Context: 1973 GIRAS, 1985 Intergraph, 1997 VRML/X3D, 2003 ASPRS LAS point classes, 2004 OSM ontology).
- [x] **Subagent Review & Fix 20.5:** Subagent review of Subsection 20.5 and correction of any issues.
- [x] **Write 20.6:** Mathematical Foundations (catenary sag and thermal elongation equations for overhead conductors).
- [x] **Subagent Review & Fix 20.6:** Subagent review of Subsection 20.6 and correction of any issues.
- [x] **Write 20.7:** Software Ecosystem (PDAL, CloudCompare, `3dcitydb`, IfcOpenShell, OSM2World vs. TerraScan, PLS-CADD, ArcGIS GeoBIM, Bentley iTwin).
- [x] **Subagent Review & Fix 20.7:** Subagent review of Subsection 20.7 and correction of any issues.
- [x] **Write 20.8:** Common Pitfalls & Key Takeaways for Chapter 20.
- [x] **Subagent Review & Fix 20.8:** Subagent review of Subsection 20.8 and correction of any issues.
- [x] **Write 20.9:** Curated Key References for Chapter 20.
- [x] **Subagent Review & Fix 20.9:** Subagent review of Subsection 20.9 and correction of any issues.

#### Chapter 21: Bare-Earth Extraction (DSM to DTM), Data Gaps, Shadows, and Overhangs
- [x] **Write 21.1:** Removing Objects from a DSM or Point Cloud to Create a DTM (Progressive Morphological Filter, Axelsson Progressive TIN Densification, Cloth Simulation Filter CSF, raster DSM-to-DTM inpainting like FABDEM, deep learning point cloud segmentation).
- [x] **Subagent Review & Fix 21.1:** Subagent review of Subsection 21.1 and correction of any issues.
- [x] **Write 21.2:** Errors and Unknowns When Removing Objects (Type I ridge-clipping vs. Type II large-roof/shrub commission errors; unquantified interpolation uncertainty voids underneath large buildings and dense forests).
- [x] **Subagent Review & Fix 21.2:** Subagent review of Subsection 21.2 and correction of any issues.
- [x] **Write 21.3:** Data Gaps, Shadows, Overlapping, and Overhanging Situations (optical/SAR/LiDAR/sonar shadows & voids; sea cliffs, arches, undercut riverbanks, and 3D Poisson / SDF representations).
- [x] **Subagent Review & Fix 21.3:** Subagent review of Subsection 21.3 and correction of any issues.
- [x] **Write 21.4:** Historical Evolution (`gis-history` Context: 1996 CGAL, 2000 SRTM void filling & Axelsson TIN densification, 2011 PDAL ground filters, 2022 FABDEM).
- [x] **Subagent Review & Fix 21.4:** Subagent review of Subsection 21.4 and correction of any issues.
- [x] **Write 21.5:** Mathematical Foundations (morphological opening operator, slope-dependent threshold, Kriging variance inflation across occluded footprints).
- [x] **Subagent Review & Fix 21.5:** Subagent review of Subsection 21.5 and correction of any issues.
- [x] **Write 21.6:** Software Ecosystem (PDAL `smrf`/`csf`/`pmf`, WhiteboxTools, CloudCompare, GDAL, `PoissonRecon` vs. TerraScan, LAStools, Global Mapper, BayesMap).
- [x] **Subagent Review & Fix 21.6:** Subagent review of Subsection 21.6 and correction of any issues.
- [x] **Write 21.7:** Common Pitfalls & Key Takeaways for Chapter 21.
- [x] **Subagent Review & Fix 21.7:** Subagent review of Subsection 21.7 and correction of any issues.
- [x] **Write 21.8:** Curated Key References for Chapter 21.
- [x] **Subagent Review & Fix 21.8:** Subagent review of Subsection 21.8 and correction of any issues.

#### Chapter 22: The Dynamic Earth: Temporal Changes, Moving Objects, AIS/ADS-B, Seasonality, and Change Detection
- [x] **Write 22.1:** Geomorphic and Anthropogenic Surface Evolution; Erosion and Deposition (fluvial/coastal erosion, migrating submarine sand waves, turbidity currents, landslides, construction/demolition, dumps/landfills/trash piles, wildfires & post-fire debris flows).
- [x] **Subagent Review & Fix 22.1:** Subagent review of Subsection 22.1 and correction of any issues.
- [x] **Write 22.2:** Dealing with Moving Objects and Timescale Impacts (cars, trains, ships, wakes, aircraft; epipolar motion-to-height parallax distortion; using AIS and ADS-B/ATCRBS trajectories to automatically mask ship, wake, and aircraft artifacts).
- [x] **Subagent Review & Fix 22.2:** Subagent review of Subsection 22.2 and correction of any issues.
- [x] **Write 22.3:** Seasonal, Vegetative, Agricultural, Hydrological, and Atmospheric Transients (leaf-on vs. leaf-off, snow/ice/permafrost/aquifer breathing, farm crops & tillage cycles, variable water stage in streams and reservoirs, industrial steam plumes/cooling towers/fumaroles).
- [x] **Subagent Review & Fix 22.3:** Subagent review of Subsection 22.3 and correction of any issues.
- [x] **Write 22.4:** Change Detection & Object Detection: Traditional vs. Machine Learning Methods (DoD with LoD thresholding, 3D M3C2 normal change, RANSAC/BPI/shoal detection vs. 3D deep learning & geospatial foundation models).
- [x] **Subagent Review & Fix 22.4:** Subagent review of Subsection 22.4 and correction of any issues.
- [x] **Write 22.5:** Historical Evolution (`gis-history` Context: 1929 turbidity current, 1973 ATCRBS, 1981 RANSAC, 1998 AIS M.1371, 2002 AIS mandate, 2010 DWH & `libais`, 2012 WhaleAlert, 2013 *All the Ships* & Earth Engine Timelapse, 2015 TensorFlow, 2016 TPU & Global Fishing Watch, 2018 MovingPandas, 2021 TorchGeo, 2022 Dynamic World, 2024 Clay 1.0).
- [x] **Subagent Review & Fix 22.5:** Subagent review of Subsection 22.5 and correction of any issues.
- [x] **Write 22.6:** Mathematical Foundations (along-track stereo velocity-to-elevation error formula, M3C2 3D confidence interval & Level of Detection).
- [x] **Subagent Review & Fix 22.6:** Subagent review of Subsection 22.6 and correction of any issues.
- [x] **Write 22.7:** Software Ecosystem (GCD, CloudCompare M3C2, `xdem`, `libais`, MovingPandas, TorchGeo, MMDetection3D, PDAL vs. QPS, CARIS, ArcGIS Image Analyst).
- [x] **Subagent Review & Fix 22.7:** Subagent review of Subsection 22.7 and correction of any issues.
- [x] **Write 22.8:** Common Pitfalls & Key Takeaways for Chapter 22.
- [x] **Subagent Review & Fix 22.8:** Subagent review of Subsection 22.8 and correction of any issues.
- [x] **Write 22.9:** Curated Key References for Chapter 22.
- [x] **Subagent Review & Fix 22.9:** Subagent review of Subsection 22.9 and correction of any issues.

---

### PART VIII: Composite Products, Standards, Visualization, Cartography, and Governance

#### Chapter 23: Local vs. Integrated Surveys and Building Composite DEM Products
- [x] **Write 23.1:** Comparing Local-Only Datasets vs. Surveys Integrated with Regional/Global Data (internal relative precision vs. absolute geodetic/tidal seam consistency).
- [x] **Subagent Review & Fix 23.1:** Subagent review of Subsection 23.1 and correction of any issues.
- [x] **Write 23.2:** Building Composite Data Products: Ordering, Cropping, Blending, and Overrides (source prioritization/supercession, outer-beam cropping, RCR/Poisson gradient blending, wavelet blending, spline-in-tension stitching, shoal-preservation & hydro-enforcement hard overrides, per-pixel provenance masks).
- [x] **Subagent Review & Fix 23.2:** Subagent review of Subsection 23.2 and correction of any issues.
- [x] **Write 23.3:** Historical Evolution (`gis-history` Context: 1903 GEBCO, 1988 GMT, 1993 MB-System `mbgrid`, 1994 `pfmabe`, 2006 BAG tracking list, 2014 NOAA CUDEM).
- [x] **Subagent Review & Fix 23.3:** Subagent review of Subsection 23.3 and correction of any issues.
- [x] **Write 23.4:** Mathematical Foundations (Poisson surface editing PDE with Dirichlet boundary conditions, temporal sediment-mobility uncertainty inflation).
- [x] **Subagent Review & Fix 23.4:** Subagent review of Subsection 23.4 and correction of any issues.
- [x] **Write 23.5:** Software Ecosystem (NOAA CUDEM `waffles`/`fetches`, MB-System, GMT `grdblend`, GDAL, GRASS, WhiteboxTools vs. CARIS Bathy DataBASE, Qimera, Esri Mosaic Dataset).
- [x] **Subagent Review & Fix 23.5:** Subagent review of Subsection 23.5 and correction of any issues.
- [x] **Write 23.6:** Common Pitfalls & Key Takeaways for Chapter 23.
- [x] **Subagent Review & Fix 23.6:** Subagent review of Subsection 23.6 and correction of any issues.
- [x] **Write 23.7:** Curated Key References for Chapter 23.
- [x] **Subagent Review & Fix 23.7:** Subagent review of Subsection 23.7 and correction of any issues.

#### Chapter 24: Survey Standards, Guide Documents, and Key Public DEM Products
- [x] **Write 24.1:** Survey and Product Guide Documents (NOAA HSSD 2000–present, NOAA Field Procedures Manual 1997/2020, Hawley 1928 & Umbach 1976 Hydrographic Manuals, IHO S-44/S-100/S-102, USGS 3DEP Lidar Base Specification, ASPRS Positional Accuracy Standards).
- [x] **Subagent Review & Fix 24.1:** Subagent review of Subsection 24.1 and correction of any issues.
- [x] **Write 24.2:** Key Public DEM Products and How They Compare (SRTM, NASADEM, ASTER GDEM, AW3D30, Copernicus GLO-30/90, FABDEM, ArcticDEM, REMA, USGS 3DEP, European national LiDAR, GEBCO + TID grid, SRTM15+, NOAA CUDEM/CRM, EMODnet).
- [x] **Subagent Review & Fix 24.2:** Subagent review of Subsection 24.2 and correction of any issues.
- [x] **Write 24.3:** Historical Evolution (`gis-history` Context: 1879 USGS, 1903 GEBCO, 1928 Hawley, 1970 NOAA, 1976 Hydrographic Manual, 1997 NOAA FPM & Smith and Sandwell, 2000 SRTM & NOAA HSSD, 2003 ICESat, 2018 ICESat-2 & GEDI).
- [x] **Subagent Review & Fix 24.3:** Subagent review of Subsection 24.3 and correction of any issues.
- [x] **Write 24.4:** Mathematical Foundations (IHO S-44 / NOAA HSSD depth-dependent $\text{TVU}_{\max}(d)$ and $\text{THU}_{\max}(d)$ equations across all survey orders).
- [x] **Subagent Review & Fix 24.4:** Subagent review of Subsection 24.4 and correction of any issues.
- [x] **Write 24.5:** Software Ecosystem (`bmi-topography`, `py3dep`, `cudem`, Earth Engine, HydrOffice QC Tools vs. CARIS IHO QC, Esri Living Atlas).
- [x] **Subagent Review & Fix 24.5:** Subagent review of Subsection 24.5 and correction of any issues.
- [x] **Write 24.6:** Common Pitfalls & Key Takeaways for Chapter 24.
- [x] **Subagent Review & Fix 24.6:** Subagent review of Subsection 24.6 and correction of any issues.
- [x] **Write 24.7:** Curated Key References for Chapter 24.
- [x] **Subagent Review & Fix 24.7:** Subagent review of Subsection 24.7 and correction of any issues.

#### Chapter 25: Deep Dive into Visualization of DEMs
- [x] **Write 25.1:** Visual Perception Science for Terrain (Colin Ware luminance vs. chrominance principles, relief inversion illusion, Mach bands).
- [x] **Subagent Review & Fix 25.1:** Subagent review of Subsection 25.1 and correction of any issues.
- [x] **Write 25.2:** Colormaps for Elevation, Bathymetry, and Derivatives (why rainbow/jet fails; perceptually uniform `viridis`/`cividis`/`batlow`/`cmocean`; Haxby & Imhof hypsometric/bathymetric palettes; bivariate elevation + uncertainty colormaps).
- [x] **Subagent Review & Fix 25.2:** Subagent review of Subsection 25.2 and correction of any issues.
- [x] **Write 25.3:** Filtering, Shading, and Terrain Enhancement Techniques (analytical vs. multi-directional vs. Swiss shading, Sky-View Factor SVF, Openness, Ambient Occlusion, RRIM, Local Relief Models, multi-scale TPI).
- [x] **Subagent Review & Fix 25.3:** Subagent review of Subsection 25.3 and correction of any issues.
- [x] **Write 25.4:** Rendering Types: From 2D Slippy Tiles to 3D Meshes, Point Clouds, and Gaussian Splats (Terrain-RGB/Terrarium, Quantized-Mesh, OGC 3D Tiles, RTIN/MARTINI, Potree Eye-Dome Lighting, NeRFs, and 3D/2D Gaussian Splatting for terrain & overhangs).
- [x] **Subagent Review & Fix 25.4:** Subagent review of Subsection 25.4 and correction of any issues.
- [x] **Write 25.5:** Historical Evolution (`gis-history` Context: 1965 Harvard Lab, 1967 ECU, 1981 SGI, 1988 GMT, 1989 OpenInventor, 1990 Fisher VR, 1992 OpenGL, 1993 VEVI, 1997 VRML/X3D/Ames Viz, 1999 Keyhole, 2000 Colin Ware & Coin3D, 2002 Blender, 2003 WorldWind, 2004 GeoMapApp, 2005 Google Maps, 2006 Virtual Globes & OpenLayers, 2007 Google Earth, 2009 Google Ocean, 2010 Three.js & Leaflet, 2011 CesiumJS, 2013 MapLibre, 2016 deck.gl & d3-geo, 2018 kepler.gl, 2023 3DGS).
- [x] **Subagent Review & Fix 25.5:** Subagent review of Subsection 25.5 and correction of any issues.
- [x] **Write 25.6:** Mathematical Foundations (Lambertian reflectance, Sky-View Factor horizon integral, 3D Gaussian Splatting anisotropic covariance projection $\boldsymbol{\Sigma}' = \mathbf{J}\mathbf{W}\boldsymbol{\Sigma}\mathbf{W}^T\mathbf{J}^T$).
- [x] **Subagent Review & Fix 25.6:** Subagent review of Subsection 25.6 and correction of any issues.
- [x] **Write 25.7:** Software Ecosystem (RVT, GMT, BlenderGIS, QGIS 3D, Potree, CesiumJS, deck.gl, MapLibre, Three.js, Nerfstudio/`gsplat`/2DGS vs. Fledermaus, ArcGIS Scene, Eduard, Surfer).
- [x] **Subagent Review & Fix 25.7:** Subagent review of Subsection 25.7 and correction of any issues.
- [x] **Write 25.8:** Common Pitfalls & Key Takeaways for Chapter 25.
- [x] **Subagent Review & Fix 25.8:** Subagent review of Subsection 25.8 and correction of any issues.
- [x] **Write 25.9:** Curated Key References for Chapter 25.
- [x] **Subagent Review & Fix 25.9:** Subagent review of Subsection 25.9 and correction of any issues.

#### Chapter 26: Navigating, Charting, Topographic Maps, and Cartographic Production
- [x] **Write 26.1:** Navigating and Charting Based on DEMs (Terrain-Relative Navigation TRN/TERCOM/BAN particle filters, aviation TAWS/EGPWS, nautical chart shoal-biased sounding selection and seaward-only contour generalization, S-102 ECDIS).
- [x] **Subagent Review & Fix 26.1:** Subagent review of Subsection 26.1 and correction of any issues.
- [x] **Write 26.2:** USGS Topos and Topographic Maps in General (history from 1879 plane tables to US Topo GeoPDFs & TopoView, Swisstopo/OS/IGN traditions, contour interval rule $\text{CI} \ge 3.3 \cdot \text{RMSE}_z$, index/supplementary/depression contours).
- [x] **Subagent Review & Fix 26.2:** Subagent review of Subsection 26.2 and correction of any issues.
- [x] **Write 26.3:** Creating Maps with DEM Products: Graticules, Labels, and Marginalia (geographic graticules vs. projected planar grids, True/Grid/Magnetic north diagram, variable-latitude scale bars, uphill-reading contour labels, mandatory datum & accuracy collar statements).
- [x] **Subagent Review & Fix 26.3:** Subagent review of Subsection 26.3 and correction of any issues.
- [x] **Write 26.4:** Historical Evolution (`gis-history` Context: 1551 plane table, 1569 Mercator, 1807 US Coast Survey, 1879 USGS, 1884 Meridian Conf., 1903 GEBCO, 1942 UTM, 1952/1957/1977 Marie Tharp, 1982 PostScript, 1988 GMT, 1991 Alacarte, 1993 PDF, 2005 *USS San Francisco*, 2011 CalTopo).
- [x] **Subagent Review & Fix 26.4:** Subagent review of Subsection 26.4 and correction of any issues.
- [x] **Write 26.5:** Mathematical Foundations (shoal-safe one-sided bathymetric contour generalization inequality, TRN Bayesian particle filter measurement likelihood).
- [x] **Subagent Review & Fix 26.5:** Subagent review of Subsection 26.5 and correction of any issues.
- [x] **Write 26.6:** Software Ecosystem (GMT, QGIS Print Layout, GRASS, Mapnik, GDAL, CalTopo vs. ArcGIS Aviation/Maritime Charting, CARIS Paper Chart/Composer, MAPublisher).
- [x] **Subagent Review & Fix 26.6:** Subagent review of Subsection 26.6 and correction of any issues.
- [x] **Write 26.7:** Common Pitfalls & Key Takeaways for Chapter 26.
- [x] **Subagent Review & Fix 26.7:** Subagent review of Subsection 26.7 and correction of any issues.
- [x] **Write 26.8:** Curated Key References for Chapter 26.
- [x] **Subagent Review & Fix 26.8:** Subagent review of Subsection 26.8 and correction of any issues.

#### Chapter 27: Legal, Privacy, Sovereignty, National Security, and Cost Optimization
- [x] **Write 27.1:** Legal Issues in Elevation and Bathymetric Mapping (chart/flood map liability, professional surveyor licensure, ambulatory property boundaries, FEMA LOMA/LOMR, software/data licenses MIT/GPL/BSD/Apache/CC0/ODbL/commercial EULAs, UNCLOS Article 76 ECS claims & MSR permits).
- [x] **Subagent Review & Fix 27.1:** Subagent review of Subsection 27.1 and correction of any issues.
- [x] **Write 27.2:** Privacy Issues (high-res LiDAR/drone/3DGS residential privacy, GDPR PII anonymization in mobile mapping, Indigenous CARE data sovereignty, archeological/shipwreck site protection).
- [x] **Subagent Review & Fix 27.2:** Subagent review of Subsection 27.2 and correction of any issues.
- [x] **Write 27.3:** Country, National Security, and Sovereignty Issues (classified territorial-sea bathymetry & sanitization, 1997 Kyl-Bingaman Amendment, 2003 US Commercial Remote Sensing Space Policy, GCJ-02 coordinate obfuscation laws, ITAR/EAR export controls, GNSS jamming/spoofing).
- [x] **Subagent Review & Fix 27.3:** Subagent review of Subsection 27.3 and correction of any issues.
- [x] **Write 27.4:** How to Reduce the Cost of Collecting, Processing, Validating, and Using DEM Data ("map once, use many times" coalitions, tiered SDB + ICESat-2 $\to$ bathylidar/USV screening, Crowdsourced Bathymetry IHO B-12, automated cloud CUBE/QC, COG/COPC/Zarr range-request streaming).
- [x] **Subagent Review & Fix 27.4:** Subagent review of Subsection 27.4 and correction of any issues.
- [x] **Write 27.5:** Historical Evolution (`gis-history` Context: 1914 SOLAS, 1982/1994 UNCLOS, 1986 Swedish Land Data Bank, 1987 MIT, 1989 GPL, 1990 BSD, 1991 LGPL, 1996 NSDI, 1997 Kyl-Bingaman, 2001 CC, 2003 US Commercial Remote Sensing Policy, 2004 Apache 2.0 & OSM & AWS & MapReduce, 2006 OSGeo, 2007 INSPIRE, 2009 CC0).
- [x] **Subagent Review & Fix 27.5:** Subagent review of Subsection 27.5 and correction of any issues.
- [x] **Write 27.6:** Mathematical Foundations (Value of Information VoI expected-loss minimization for optimal survey resolution and sensor budgeting).
- [x] **Subagent Review & Fix 27.6:** Subagent review of Subsection 27.6 and correction of any issues.
- [x] **Write 27.7:** Software Ecosystem (OSGeo stack, IHO DCDB CSB tools, ODM vs. Google Earth Engine, AWS/GCP/Azure geospatial cloud, ArcGIS Online).
- [x] **Subagent Review & Fix 27.7:** Subagent review of Subsection 27.7 and correction of any issues.
- [x] **Write 27.8:** Common Pitfalls & Key Takeaways for Chapter 27.
- [x] **Subagent Review & Fix 27.8:** Subagent review of Subsection 27.8 and correction of any issues.
- [x] **Write 27.9:** Curated Key References for Chapter 27.
- [x] **Subagent Review & Fix 27.9:** Subagent review of Subsection 27.9 and correction of any issues.

---

### PART IX: Advanced and Specialized Frontiers (Added from Gap Review)

#### Chapter 28: Acoustic Backscatter, LiDAR Intensity, and Substrate/Benthic Co-Products
- [x] **Write 28.1:** Physical Principles of Return Amplitude and Backscatter (acoustic $S_b(\theta)$, LiDAR reflectance, SAR $\sigma^0$; surface vs. volume scattering).
- [x] **Subagent Review & Fix 28.1:** Subagent review of Subsection 28.1 and correction of any issues.
- [x] **Write 28.2:** Radiometric and Geometric Correction Using the DEM (TVG, true 3D DEM slope footprint area & grazing angle correction, Angular Range Analysis ARA).
- [x] **Subagent Review & Fix 28.2:** Subagent review of Subsection 28.2 and correction of any issues.
- [x] **Write 28.3:** Disambiguating DEM Anomalies with Backscatter and Intensity (rock shoal vs. kelp/fish/gas seep; road pavement vs. bare soil).
- [x] **Subagent Review & Fix 28.3:** Subagent review of Subsection 28.3 and correction of any issues.
- [x] **Write 28.4:** Historical Evolution (`gis-history` Context: 1962 multibeam patent, 1977 SeaBeam, 1993 MB-System, 2003 LAS intensity, 2018 GeoHab guidelines).
- [x] **Subagent Review & Fix 28.4:** Subagent review of Subsection 28.4 and correction of any issues.
- [x] **Write 28.5:** Mathematical Foundations (sonar equation for bottom backscatter strength with 3D DEM normal grazing angle).
- [x] **Subagent Review & Fix 28.5:** Subagent review of Subsection 28.5 and correction of any issues.
- [x] **Write 28.6:** Software Ecosystem (MB-System, OpenBST, PDAL vs. QPS FMGT, CARIS SIPS, SonarWiz).
- [x] **Subagent Review & Fix 28.6:** Subagent review of Subsection 28.6 and correction of any issues.
- [x] **Write 28.7:** Common Pitfalls & Key Takeaways for Chapter 28.
- [x] **Subagent Review & Fix 28.7:** Subagent review of Subsection 28.7 and correction of any issues.
- [x] **Write 28.8:** Curated Key References for Chapter 28.
- [x] **Subagent Review & Fix 28.8:** Subagent review of Subsection 28.8 and correction of any issues.

#### Chapter 29: Fluid Mud, "Nautical Depth," and Multi-Horizon Subsurface DEMs
- [x] **Write 29.1:** The Fluid Mud Problem and Dual-Frequency Echosounding ($200\text{ kHz}$ lutocline vs. $15\text{–}33\text{ kHz}$ consolidated bed reflections).
- [x] **Subagent Review & Fix 29.1:** Subagent review of Subsection 29.1 and correction of any issues.
- [x] **Write 29.2:** PIANC "Nautical Depth" and Rheological Surveying ($\rho = 1200\text{ kg/m}^3$ / yield stress thresholds, densitometer probes + parametric sub-bottom profilers).
- [x] **Subagent Review & Fix 29.2:** Subagent review of Subsection 29.2 and correction of any issues.
- [x] **Write 29.3:** Multi-Horizon DEMs (Stacked Stratigraphic Surfaces on land and sea with non-crossing topological constraints).
- [x] **Subagent Review & Fix 29.3:** Subagent review of Subsection 29.3 and correction of any issues.
- [x] **Write 29.4:** Historical Evolution (`gis-history` Context: 1913 sonar, 1929 turbidity current, 1976 Hydrographic Manual, 2014 PIANC Report 121).
- [x] **Subagent Review & Fix 29.4:** Subagent review of Subsection 29.4 and correction of any issues.
- [x] **Write 29.5:** Mathematical Foundations (inequality-constrained multi-horizon Kriging/splines, viscoelastic acoustic impedance reflection).
- [x] **Subagent Review & Fix 29.5:** Subagent review of Subsection 29.5 and correction of any issues.
- [x] **Write 29.6:** Software Ecosystem (SegyIO, OpendTect, GMT, GemPy vs. SonarWiz Sub-Bottom, Innomar, Kingdom Suite, Petrel).
- [x] **Subagent Review & Fix 29.6:** Subagent review of Subsection 29.6 and correction of any issues.
- [x] **Write 29.7:** Common Pitfalls & Key Takeaways for Chapter 29.
- [x] **Subagent Review & Fix 29.7:** Subagent review of Subsection 29.7 and correction of any issues.
- [x] **Write 29.8:** Curated Key References for Chapter 29.
- [x] **Subagent Review & Fix 29.8:** Subagent review of Subsection 29.8 and correction of any issues.

#### Chapter 30: Cryospheric and Subglacial / Sub-Ice-Shelf Bed Topography
- [x] **Write 30.1:** Surface DEMs of Ice Sheets, Glaciers, and Sea Ice (radar firn penetration bias vs. optical/laser surface, hydrostatic ice-shelf/sea-ice freeboard conversion).
- [x] **Subagent Review & Fix 30.1:** Subagent review of Subsection 30.1 and correction of any issues.
- [x] **Write 30.2:** Mapping Subglacial Bed Topography (*BedMachine* mass-conservation inversion, ice-penetrating radar RES, gravity/seismic/AUV mapping of sub-ice-shelf cavities).
- [x] **Subagent Review & Fix 30.2:** Subagent review of Subsection 30.2 and correction of any issues.
- [x] **Write 30.3:** Historical Evolution (`gis-history` Context: 1957 IGY, 1985 GEOSAT, 2003 ICESat, 2016 ArcticDEM, 2017 BedMachine, 2018 ICESat-2 & REMA).
- [x] **Subagent Review & Fix 30.3:** Subagent review of Subsection 30.3 and correction of any issues.
- [x] **Write 30.4:** Mathematical Foundations (ice mass-conservation PDE $\nabla \cdot (H\bar{\mathbf{v}}) = \dot{b} - \dot{m}_b - \partial H/\partial t$, hydrostatic freeboard equation).
- [x] **Subagent Review & Fix 30.4:** Subagent review of Subsection 30.4 and correction of any issues.
- [x] **Write 30.5:** Software Ecosystem (ISSM/BedMachine, `xdem`, CReSIS, SlideRule vs. GAMMA, Oasis montaj).
- [x] **Subagent Review & Fix 30.5:** Subagent review of Subsection 30.5 and correction of any issues.
- [x] **Write 30.6:** Common Pitfalls & Key Takeaways for Chapter 30.
- [x] **Subagent Review & Fix 30.6:** Subagent review of Subsection 30.6 and correction of any issues.
- [x] **Write 30.7:** Curated Key References for Chapter 30.
- [x] **Subagent Review & Fix 30.7:** Subagent review of Subsection 30.7 and correction of any issues.

#### Chapter 31: Planetary and Extraterrestrial DEMs (Moon, Mars, Asteroids, and Ocean Worlds)
- [x] **Write 31.1:** Planetary Geodesy and Vertical Datums Without Oceans (areoid/selenoid equipotential surfaces, planetocentric vs. planetographic coordinates, JPL SPICE kernels).
- [x] **Subagent Review & Fix 31.1:** Subagent review of Subsection 31.1 and correction of any issues.
- [x] **Write 31.2:** Planetary Laser Altimetry, Stereo Photogrammetry, and Photoclinometry (MOLA/LOLA orbit crossover adjustment, pushbroom jitter correction in NASA ASP, multi-view Shape-from-Shading, Cassini Titan hydrocarbon-sea radar bathymetry).
- [x] **Subagent Review & Fix 31.2:** Subagent review of Subsection 31.2 and correction of any issues.
- [x] **Write 31.3:** Non-Spherical Small Bodies: Asteroids and Comets (3D polyhedral shape models, stereophotoclinometry SPC, Roche geopotential dynamic height on rotating irregular bodies).
- [x] **Subagent Review & Fix 31.3:** Subagent review of Subsection 31.3 and correction of any issues.
- [x] **Write 31.4:** Historical Evolution (`gis-history` Context: 1785/1918 Galactic coordinates, 1962 JPL IPL, 1964 Ranger 7, 1966 VICAR, 1972 Apollo 17, 1981 FITS, 1982 JPL SPICE, 1996 NASA ASP, 1997 Ames Viz).
- [x] **Subagent Review & Fix 31.4:** Subagent review of Subsection 31.4 and correction of any issues.
- [x] **Write 31.5:** Mathematical Foundations (polyhedral gravitational + centrifugal Roche potential and dynamic elevation).
- [x] **Subagent Review & Fix 31.5:** Subagent review of Subsection 31.5 and correction of any issues.
- [x] **Write 31.6:** Software Ecosystem (USGS ISIS3, NASA ASP, SpiceyPy/SPICE, ALE vs. BAE SOCET GXP, Gaskell SPC).
- [x] **Subagent Review & Fix 31.6:** Subagent review of Subsection 31.6 and correction of any issues.
- [x] **Write 31.7:** Common Pitfalls & Key Takeaways for Chapter 31.
- [x] **Subagent Review & Fix 31.7:** Subagent review of Subsection 31.7 and correction of any issues.
- [x] **Write 31.8:** Curated Key References for Chapter 31.
- [x] **Subagent Review & Fix 31.8:** Subagent review of Subsection 31.8 and correction of any issues.

#### Chapter 32: Hardware Timing, Synchronization, Leap Seconds, and Relativistic/Atmospheric Physics
- [x] **Write 32.1:** Time Scales in Geodesy and Surveying (TAI, UTC, GPS Time, GLONASS Time, Unix Time, and the 18-second leap-second trajectory offset bug).
- [x] **Subagent Review & Fix 32.1:** Subagent review of Subsection 32.1 and correction of any issues.
- [x] **Write 32.2:** Hardware Time Synchronization Architectures (PPS + NMEA `$GPZDA` baud-delay pitfalls, NTP vs. IEEE 1588 PTP hardware timestamping).
- [x] **Subagent Review & Fix 32.2:** Subagent review of Subsection 32.2 and correction of any issues.
- [x] **Write 32.3:** Relativistic and Atmospheric Propagation Physics (special/general relativistic GNSS clock corrections, Sagnac effect, Ciddor/Marini-Murray atmospheric laser group refractivity delay & ray bending).
- [x] **Subagent Review & Fix 32.3:** Subagent review of Subsection 32.3 and correction of any issues.
- [x] **Write 32.4:** Historical Evolution (`gis-history` Context: 1656 pendulum clock, 1676 Rømer, 1761 Harrison H4, 1915 General Relativity, 1917 nautical time, 1928 UT, 1949/1955 atomic clocks, 1960 UTC, 1970 Unix time, 1979 NTP, 1984 NMEA 0183).
- [x] **Subagent Review & Fix 32.4:** Subagent review of Subsection 32.4 and correction of any issues.
- [x] **Write 32.5:** Mathematical Foundations (relativistic eccentricity & Sagnac range equations, Ciddor group delay integral).
- [x] **Subagent Review & Fix 32.5:** Subagent review of Subsection 32.5 and correction of any issues.
- [x] **Write 32.6:** Software Ecosystem (`linuxptp`, `chrony`, AstroPy/SOFA, `gpsd` vs. Meinberg grandmasters, Applanix POS).
- [x] **Subagent Review & Fix 32.6:** Subagent review of Subsection 32.6 and correction of any issues.
- [x] **Write 32.7:** Common Pitfalls & Key Takeaways for Chapter 32.
- [x] **Subagent Review & Fix 32.7:** Subagent review of Subsection 32.7 and correction of any issues.
- [x] **Write 32.8:** Curated Key References for Chapter 32.
- [x] **Subagent Review & Fix 32.8:** Subagent review of Subsection 32.8 and correction of any issues.

#### Chapter 33: Geostatistical Error Simulation and Downstream Uncertainty Propagation
- [x] **Write 33.1:** Modeling Spatial Autocorrelation of DEM Errors (why i.i.d. white noise fails, empirical/theoretical semivariograms, anisotropic flight/ship-line correlation, heteroscedastic $\sigma_z(x,y)$).
- [x] **Subagent Review & Fix 33.1:** Subagent review of Subsection 33.1 and correction of any issues.
- [x] **Write 33.2:** Conditional Geostatistical Simulation of Equiprobable DEMs (Sequential Gaussian Simulation SGS, Turning Bands, FFT moving-average ensembles).
- [x] **Subagent Review & Fix 33.2:** Subagent review of Subsection 33.2 and correction of any issues.
- [x] **Write 33.3:** Propagating DEM Ensembles Through Non-Linear Downstream Models (probabilistic flood inundation maps, fuzzy viewsheds, watershed avulsion probability, landslide factor-of-safety distributions).
- [x] **Subagent Review & Fix 33.3:** Subagent review of Subsection 33.3 and correction of any issues.
- [x] **Write 33.4:** Historical Evolution (`gis-history` Context: 1951 Krige, 1988 GMT, 2000 R `gstat`, 2006 BAG uncertainty, 2022 `xdem`).
- [x] **Subagent Review & Fix 33.4:** Subagent review of Subsection 33.4 and correction of any issues.
- [x] **Write 33.5:** Mathematical Foundations (2D FFT spectral covariance synthesis with heteroscedastic variance scaling, coupled THU-TVU slope variance formula).
- [x] **Subagent Review & Fix 33.5:** Subagent review of Subsection 33.5 and correction of any issues.
- [x] **Write 33.6:** Software Ecosystem (`xdem`, `gstools`, R `gstat`, SGeMS, GRASS `r.random.surface` vs. ArcGIS Geostatistical Analyst, Isatis.neo).
- [x] **Subagent Review & Fix 33.6:** Subagent review of Subsection 33.6 and correction of any issues.
- [x] **Write 33.7:** Common Pitfalls & Key Takeaways for Chapter 33.
- [x] **Subagent Review & Fix 33.7:** Subagent review of Subsection 33.7 and correction of any issues.
- [x] **Write 33.8:** Curated Key References for Chapter 33.
- [x] **Subagent Review & Fix 33.8:** Subagent review of Subsection 33.8 and correction of any issues.

#### Chapter 34: Cloud-Native Petabyte Pipelines, GPU Acceleration, and Automated Testing for DEMs
- [x] **Write 34.1:** Evolution of Geospatial Computing Architectures (`gis-history` Arc from Z3/ENIAC/Fortran/VICAR/Unix/C/Cray-1 to Python/NumPy/GDAL to MapReduce/Earth Engine/Dask/Zarr/IceChunk/TPUs).
- [x] **Subagent Review & Fix 34.1:** Subagent review of Subsection 34.1 and correction of any issues.
- [x] **Write 34.2:** Out-of-Core Tiled Processing and Halo/Apron Management (`map_overlap` halo sizing for filters/splines, distributed Priority-Flood depression filling, CUDA/WebGPU compute kernels).
- [x] **Subagent Review & Fix 34.2:** Subagent review of Subsection 34.2 and correction of any issues.
- [x] **Write 34.3:** Automated Testing, CI/CD, and Verification for DEM Software & Data Pipelines (analytical paraboloid/Gaussian test surfaces, volumetric conservation invariants, datum round-trip tests, STAC schema checkers, guardrails for AI/LLM coding agents against PROJ4/axis-order/half-pixel bugs).
- [x] **Subagent Review & Fix 34.3:** Subagent review of Subsection 34.3 and correction of any issues.
- [x] **Write 34.4:** Mathematical Foundations (Priority-Flood $O(N\log N)$ graph reduction across tile boundaries, discrete Green's theorem volume invariance).
- [x] **Subagent Review & Fix 34.4:** Subagent review of Subsection 34.4 and correction of any issues.
- [x] **Write 34.5:** Software Ecosystem (`xarray`, `Dask`, `rioxarray`, `odc-geo`, Earth Engine API v1.0, Apache Sedona, RichDEM, `pytest` + `hypothesis` vs. Earth Engine Commercial, Databricks Mosaic, TileDB).
- [x] **Subagent Review & Fix 34.5:** Subagent review of Subsection 34.5 and correction of any issues.
- [x] **Write 34.6:** Common Pitfalls & Key Takeaways for Chapter 34.
- [x] **Subagent Review & Fix 34.6:** Subagent review of Subsection 34.6 and correction of any issues.
- [x] **Write 34.7:** Curated Key References for Chapter 34.
- [x] **Subagent Review & Fix 34.7:** Subagent review of Subsection 34.7 and correction of any issues.

#### Chapter 35: Accessibility, Physical/Tactile Terrain Models, and Field Augmented Reality (AR)
- [x] **Write 35.1:** Accessible and Colorblind-Safe Elevation Design (CVD simulation for deuteranopia/protanopia/tritanopia, high-contrast tactile/hachure modes, screen-reader terrain summaries).
- [x] **Subagent Review & Fix 35.1:** Subagent review of Subsection 35.1 and correction of any issues.
- [x] **Write 35.2:** Physical and Tactile Terrain Models (watertight 3D printable `.stl`/`.3mf` manifold extrusion, Braille/tactile cartography standards, multi-material resin bathy models, CNC routing).
- [x] **Subagent Review & Fix 35.2:** Subagent review of Subsection 35.2 and correction of any issues.
- [x] **Write 35.3:** Field Augmented Reality (AR) and Virtual Globes (mobile AR visualization of DEMs, flood stages, and buried/submerged utilities; Visual Positioning System VPS registration against 3D terrain meshes).
- [x] **Subagent Review & Fix 35.3:** Subagent review of Subsection 35.3 and correction of any issues.
- [x] **Write 35.4:** Historical Evolution (`gis-history` Context: 1957 Marie Tharp, 1990 Fisher VR, 1993 VEVI, 1997 VRML/X3D, 2002 Blender, 2006 Virtual Globes, 2012 Niantic Field Trip, 2016 Pokémon Go).
- [x] **Subagent Review & Fix 35.4:** Subagent review of Subsection 35.4 and correction of any issues.
- [x] **Write 35.5:** Mathematical Foundations (Euler-Poincaré characteristic $V - E + F = 2$ and closed surface normal integral $\oint \hat{\mathbf{n}}\,dA = \mathbf{0}$ for watertight 3D printing).
- [x] **Subagent Review & Fix 35.5:** Subagent review of Subsection 35.5 and correction of any issues.
- [x] **Write 35.6:** Software Ecosystem (`TouchTerrain`, QGIS `DEMto3D`, Blender, MeshLab, PrusaSlicer, Cesium for Unreal/Unity vs. ArcGIS Maps SDK, Trimble SiteVision).
- [x] **Subagent Review & Fix 35.6:** Subagent review of Subsection 35.6 and correction of any issues.
- [x] **Write 35.7:** Common Pitfalls & Key Takeaways for Chapter 35.
- [x] **Subagent Review & Fix 35.7:** Subagent review of Subsection 35.7 and correction of any issues.
- [x] **Write 35.8:** Curated Key References for Chapter 35.
- [x] **Subagent Review & Fix 35.8:** Subagent review of Subsection 35.8 and correction of any issues.

---

## 4. Final Book Synthesis, Cross-Chapter Verification, and Publication Tasks

- [x] **Task 4.1:** Cross-chapter mathematical symbol & equation audit (verify zero conflicting symbols between geodesy, acoustics, photogrammetry, SAR, and statistics).
- [x] **Task 4.2:** Master bibliography deduplication and DOI/URL verification across all 35 chapters.
- [x] **Task 4.3:** End-to-end build and lint of the complete handbook (`TOC.md`, front matter, Chapters 1–35, index).

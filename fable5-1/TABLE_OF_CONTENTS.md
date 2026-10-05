# The Digital Elevation Models Handbook — Detailed Table of Contents (draft 0.1)

*From sensor physics to trustworthy elevation products, on land and under water.*

## How to read this document

- The book is organized in 16 parts, 73 chapters, and 9 appendices. Chapters are
  numbered continuously so cross-references are stable.
- **Ordering rationale.** Uses first (what people need) → vocabulary and the
  statistics of error (so every later chapter can speak precisely) → geodesy and
  datums (where "here" is) → positioning (every sensor needs it) → sensors and
  platforms → planning and operations → processing → the dynamic Earth →
  semantics/ML/resolution → storage, metadata, discovery → validation and judging
  data (the capstone) → visualization and cartography → vectors and grids → domain
  deep dives → law/security/privacy → standards, software, history → appendices.
- **Every chapter block below has the same slots**: *Scope*, *Sections*,
  *Then & now* (how the system/process changed over time; entries tagged ⟨H⟩ come
  from [schwehr/gis-history](https://github.com/schwehr/gis-history)), *Math*
  (only where the chapter is mathematical), *Software* (open / closed),
  *Standards & guides*, *Key references* (seed bibliography, short form; DOIs to be
  added in the bibliography pass), *Pitfalls*, and *Key takeaways*. In the finished
  book every chapter ends with "Pitfalls" and "Key takeaways" boxes and contains a
  mandatory "Validation & uncertainty" section.
- **Recurring boxes** throughout the book: *Uncertainty budget*, *Then & now*,
  *Definitions that bite*, *Try it* (runnable code), *Case file*.
- **Reading paths.** Validator: 1→3→4→5→9→52→53→54→55→56. Hydrographer:
  2→9→13→20→25→26→34→48→62→70. Lidar/photogrammetry: 12→13→18→22→30→31→32→53.
  Data engineer: 4→44→46→47→48→49→50→51. Decision maker: 1→2→3→54→55→68→69.
- **Conventions.** Items marked "(verify)" are citations or edition numbers to be
  confirmed in the bibliography pass. In Appendix C, ⟨H⟩ marks entries taken from
  gis-history and ⟨+⟩ marks entries added for this handbook. Product accuracy
  figures in Appendix E are indicative seeds, to be re-checked against the current
  product handbooks when the chapters are written.

## Skeleton

**Part I — Why elevation? Uses and users**
1. The many uses of elevation data on land
2. The many uses of bathymetry and topobathymetry
3. From use to requirement: fitness for use, constraints, and appropriate resolution

**Part II — Vocabulary and the foundations of correctness**
4. Names and definitions: DEM, DSM, DTM, and the words that bite
5. Error, uncertainty, accuracy, precision, resolution — the statistical toolkit
6. Time as a coordinate: epochs, clocks, synchronization

**Part III — Where is "here"? Geodesy, datums, projections**
7. The shape of the Earth: ellipsoid, geoid, gravity, heights
8. Horizontal datums and terrestrial reference frames
9. Vertical datums: orthometric, ellipsoidal, tidal, and home-made
10. Map projections, grids, and the resampling they force

**Part IV — Positioning and orientation**
11. A history of positioning: from plumb bobs to PPP
12. GNSS for elevation work
13. IMU/INS, motion sensing, and GNSS-aided navigation
14. Positioning without (or beyond) GNSS: acoustic, terrain-aided, radio, barometric
15. SLAM: solving the map and the trajectory together (and mapping innerspace)

**Part V — Sensors and platforms**
16. Platforms: feet, cars, boats, drones, kites, aircraft, satellites, fixed infrastructure
17. Measurement physics: a unified view (ranging, parallax, interferometry, inversion)
18. Topographic lidar
19. Bathymetric lidar and the land–water transition
20. Sonar: the many types and how they make bathymetry
21. Radar, SAR, InSAR, radar altimetry, and ice-penetrating radar
22. Photogrammetry, stereo, and structure from motion
23. Optical satellite-derived bathymetry, wave-kinematics bathymetry, altimetry-predicted bathymetry
24. Gravity, magnetics, and other geophysics as mapping aids
25. Calibration: targets, stations, networks, benchmarks, reference surfaces

**Part VI — Planning and operating surveys**
26. Survey planning for calibration, error reduction, and error monitoring
27. Moving and transient objects during collection (cars, ships, cranes, smoke, steam; AIS/ADS-B)
28. Reducing cost across collection, processing, validation, and use

**Part VII — From sensor data to products**
29. Processing pipelines: levels, lineage, and what gets lost
30. Point-cloud cleaning, classification, and ground extraction
31. Interpolation, gridding, and grid registration
32. DSM → DTM: removing objects, and the definitions problem (buildings, roads, bridges, pipes, panels)
33. Wires, power lines, antennas, and other thin or moving structures
34. Water in DEMs: surfaces, shorelines, hydro-flattening / -enforcement / -conditioning
35. Voids, occlusion, shadows, overhangs, and multi-valued surfaces
36. Seasonal and environmental variability (leaves, snow, groundwater, crops, steam, tides)

**Part VIII — The dynamic Earth**
37. Time scales of surface change
38. Plate motion, reference-frame dynamics, and vertical land motion
39. Earthquakes, volcanoes, landslides: sudden deformation and its datum consequences
40. Erosion, deposition, and geomorphic change
41. Change detection methods and the minimum detectable change

**Part IX — Semantics, learning, and enhancement**
42. Object detection and semantic labelling of the surface
43. Traditional versus machine-learning methods: a cross-cutting assessment
44. Resolution, pixel size, sampling, and oversampling
45. Super-resolution and DEM enhancement

**Part X — Representing, storing, finding, and keeping elevation data**
46. Data models: points, waveforms, grids, TINs, meshes, voxels, variable resolution, overviews, splats
47. File formats: LAS/LAZ/COPC, GeoTIFF/COG, BAG/S-102, NetCDF/Zarr, DTED, and the rest
48. Compositing: merging many datasets into one product
49. Metadata
50. Archiving, versioning, and provenance
51. Finding the right data: catalogs, STAC, and search

**Part XI — Validation, quality, and judging data**
52. Ground truth and calibration/validation datasets
53. Accuracy assessment and uncertainty quantification in practice
54. Evaluating other people's data when you lack the full story
55. Public DEM and bathymetry products: catalog and comparison
56. Case files: failures, surprises, and lessons

**Part XII — Visualization and cartography**
57. Visualizing DEMs: shading, colormaps, filtering, rendering, point clouds, splats
58. Making maps from elevation: topographic maps, charts, graticules, standard elements

**Part XIII — Vectors, grids, and location codes**
59. Vector data and DEMs: points, lines, polygons, breaklines, contours, topology
60. Discrete global grids and location codes: S2, H3, geohash, plus codes, what3words, MGRS

**Part XIV — Domain deep dives**
61. Hydrologic and hydraulic modeling constraints
62. Navigation and charting from elevation: marine, aviation, drones, vehicles, robots
63. Buildings, cities, and innerspace
64. Agriculture, forests, wetlands, and the living surface
65. Mining, landfills, construction, and engineered earthworks
66. Coastal, marine, polar, lakes and rivers
67. Planetary DEMs: mapping without ground truth

**Part XV — Law, policy, security, privacy, ethics**
68. Legal issues
69. National security, sovereignty, privacy, and ethics

**Part XVI — Standards, software, and history**
70. Survey and product specifications: a guided tour (S-44, HSSD, FPM, LBS, ASPRS, ICAO, INSPIRE…)
71. Software landscape: open-source and closed-source by task
72. How we got here: a history of measuring the shape of the Earth
73. Open problems and the next decade

**Appendices**
A. Glossary · B. Mathematical reference · C. Timeline (seeded from gis-history) ·
D. Standards and guide documents index · E. Public products comparison tables ·
F. Software index · G. Checklists · H. Datasets for exercises and benchmarks ·
I. Gap review — what else should be included, and what could be trimmed

---

# Detailed chapter blocks

## Part I — Why elevation? Uses and users

### Chapter 1 — The many uses of elevation data on land
**Scope.** Catalog what people do with DEM/DSM/DTM products and what each use silently assumes (surface type, resolution, vertical datum, currency, uncertainty).
**Sections.**
- 1.1 Topographic mapping and cartography (contours, relief, spot heights; national mapping)
- 1.2 Imagery production: orthorectification, SAR geocoding, radiometric terrain correction — the largest hidden consumer of DEMs
- 1.3 Hydrology and hydraulics: watersheds, flow routing, flood inundation and insurance (FEMA/NFIP), stormwater, dam-break
- 1.4 Coastal risk: sea-level rise exposure, storm surge, tsunami run-up (requires seamless topobathy)
- 1.5 Geomorphology and Earth-surface processes: landslides, erosion, rivers, glaciers, permafrost, volcanoes, active tectonics
- 1.6 Geology and geophysics: gravity terrain corrections, structural mapping, seismic site effects, exploration
- 1.7 Forestry and ecology: canopy height models, biomass/carbon (GEDI), habitat, wildfire behavior, snow depth by lidar differencing
- 1.8 Agriculture: drainage and tile design, land leveling, erosion (RUSLE LS factor), precision agriculture
- 1.9 Urban planning and engineering: cut/fill, site design, viewshed and line of sight, rooftop solar, shadows, wind/CFD, noise, RF propagation (ITU-R P.1812/P.452), utility corridors, road/rail design, building-height regulation, digital twins and BIM
- 1.10 Infrastructure monitoring: subsidence, dams and levees, mines (stockpiles, pits, tailings), landfills (airspace), construction progress
- 1.11 Disaster response and risk: earthquake deformation, landslide hazard, post-fire debris flow, floods, lava-flow paths, avalanche terrain, damage assessment
- 1.12 Climate and cryosphere: ice-sheet and glacier elevation change, snow water equivalent, sea-level budget
- 1.13 Weather, climate, and environmental modeling: model orography, downscaling, cold-air pooling, soil-mapping covariates, species distribution
- 1.14 Defense, intelligence, aerospace: line of sight, mission planning, terrain-referenced navigation, obstacle databases (DTED, DVOF)
- 1.15 Navigation and mobility: aviation terrain awareness (TAWS), drone AGL, autonomous vehicles and robots, hiking/cycling apps
- 1.16 Energy and communications: wind/solar/hydro siting, reservoir capacity curves, transmission routing, telecom planning
- 1.17 Archaeology and cultural heritage: lidar under canopy, local relief models
- 1.18 Legal and cadastral: boundaries, airspace, zoning height, flood zones
- 1.19 Consumer, media, entertainment: 3D maps, games, flight simulators, AR, fitness, 3D printing, tactile maps
- 1.20 Beyond Earth: planetary DEMs (pointer to Ch. 67)
- 1.21 What each use assumes — a matrix (surface type, resolution, vertical accuracy, datum, currency, completeness, uncertainty layer)
**Then & now.** Contour maps (USGS founded 1879 ⟨H⟩; 7.5′ quads) → digitized contours (USGS DEMs 1970s–90s) → SRTM 2000 ⟨H⟩ → national lidar (3DEP 2012–) → ML-corrected global DTMs (2020s): from "a map you read" to "a model you compute with."
**Standards & guides.** USGS 3DEP program documents; National Enhanced Elevation Assessment (Dewberry 2012); 3D Nation Elevation Requirements and Benefits Study (Dewberry/NOAA/USGS 2022) — the authoritative use/benefit inventories.
**Key references.** Maune & Nayegandhi (eds.) 2018, *DEM Users Manual* 3rd ed. (ASPRS); Wilson & Gallant 2000; Hengl & Reuter 2009; Sugarbaker et al. 2014 USGS Circ. 1399; Tarolli 2014 *Geomorphology*; Passalacqua et al. 2015 *Earth-Sci. Rev.*; Dewberry 2012; Dewberry 2022.
**Pitfalls.** Using a DSM where a DTM is required (flood water flowing over tree canopy); mixing vertical datums across inputs; assuming a "30 m" product resolves 30 m features; treating an elevation value as timeless; skipping the uncertainty layer because "this use doesn't need it."
**Key takeaways.** Name the use before choosing data; every use implies a surface definition, resolution, datum, accuracy, and currency; the biggest DEM consumers are often invisible (orthorectification, model orography).

### Chapter 2 — The many uses of bathymetry and topobathymetry
**Scope.** Water-side uses from harbor to hadal, fresh and salt; what "depth" means to each.
**Sections.**
- 2.1 Safety of navigation: nautical charts (ENC S-57/S-101; S-102 surfaces), under-keel clearance, routes, anchorages, grounding risk, "never-deeper-than" surfaces
- 2.2 Ports, dredging, coastal engineering: pre/post volumes, channel maintenance, scour, breakwaters, berth pockets
- 2.3 Offshore energy and infrastructure: wind farms, cables and pipelines (routes, burial depth, free spans), platforms, UXO, geohazards
- 2.4 Coastal management: shoreline change, nourishment volumes, sediment budgets, storm response, inlets, marsh platforms
- 2.5 Hydrodynamic and hazard modeling: tides, currents, surge (ADCIRC), waves (SWAN), tsunami (MOST/GeoClaw) — the seamless-topobathy requirement
- 2.6 Inland waters: river bathymetry for hydraulics, reservoir capacity and sedimentation surveys, lakes (IGLD), inland navigation (USACE eHydro), glacial lakes
- 2.7 Habitat, fisheries, marine spatial planning: benthic habitat (CMECS), coral reefs, seagrass, essential fish habitat, MPAs, aquaculture siting
- 2.8 Geoscience: plate tectonics and ridges (Tharp ⟨H⟩), seamounts, canyons, submarine landslides as tsunami sources (Grand Banks 1929 ⟨H⟩), hydrates, sediment transport, paleo-shorelines
- 2.9 Deep-sea resources and policy: nodules, vents, UNCLOS Article 76 continental-shelf claims
- 2.10 Cryosphere: sub-ice-shelf cavities, grounding lines, fjords, sub-ice bed topography
- 2.11 Defense and security: submarine navigation (USS *San Francisco* 2005 ⟨H⟩), ASW acoustics (propagation needs bathymetry), mine countermeasures
- 2.12 Search, rescue, salvage, archaeology: MH370 search, wrecks
- 2.13 Exploration and the unmapped majority: GEBCO (1903 ⟨H⟩), Seabed 2030, crowdsourced bathymetry (IHO B-12)
- 2.14 Use → requirement matrix for bathymetry (depth-dependent resolution, object detection, TVU/THU, datum, currency)
**Then & now.** Lead lines (*Challenger* 1872–76) → wire drag → echo sounder (1913 patent ⟨H⟩; *Meteor* 1925–27) → multibeam (1962 patent, SeaBeam 1977, Hydrosweep 1989 ⟨H⟩) → satellite-predicted (Smith & Sandwell 1997 ⟨H⟩) → topobathy lidar and SDB → Seabed 2030 (2017).
**Standards & guides.** IHO S-44 Ed. 6; NOAA HSSD and FPM; USACE EM 1110-2-1003; IHO C-13; IHO S-100 family; GEBCO Cook Book (IHO-IOC B-11).
**Key references.** Mayer 2006 *Mar. Geophys. Res.*; Mayer et al. 2018 *Geosciences* (Seabed 2030); Wölfl et al. 2019 *Front. Mar. Sci.*; Weatherall et al. 2015; Tozer et al. 2019 (SRTM15+); Eakins & Grothe 2014 *J. Coastal Res.*; Danielson et al. 2016 (CoNED); Picard et al. 2018 *Mar. Geol.* (MH370); Doel, Levin & Marker 2006 (Heezen–Tharp); Wright 2002 *Undersea with GIS* ⟨H⟩.
**Pitfalls.** Averaging soundings for a navigation product (buries shoals); mixing chart datum with orthometric land data at the coast; assuming altimetry-predicted bathymetry resolves features under ~10 km; reading an old chart as current (soundings may be 19th-century lead line).
**Key takeaways.** Bathymetric resolution is inherently depth-dependent; navigation products are conservative by design and science products unbiased by design — different products from the same data; the land–water seam is where most datum errors live.

### Chapter 3 — From use to requirement: fitness for use, constraints, and appropriate resolution
**Scope.** Translate a use into testable requirements; why one dataset cannot serve everyone; preview of resolution/accuracy trade-offs.
**Sections.**
- 3.1 Fitness for use, formally (ISO 19157 quality elements; "true" vs "useful")
- 3.2 Requirement dimensions: surface type, nominal and effective resolution, vertical/horizontal accuracy and its spatial structure, completeness (voids, object detection), currency/epoch, datum, uncertainty metadata, licensing/cost, format
- 3.3 Constraints from uses, contrasted: hydrologic modeling (connectivity over absolute accuracy); ship navigation (shoalest point, no false deeps); aviation obstacles (completeness of thin tall objects); SLR exposure (decimeter vertical accuracy, datum); volumetrics (bias dominates); change detection (co-registration and precision); visualization (plausibility); ML training (label consistency)
- 3.4 Local-only versus integrated datasets: when a project datum and relative accuracy suffice, when integration with national/global frameworks is mandatory, and what each costs (control, transformations, documentation)
- 3.5 How product resolution changes what is appropriate: decision table (smallest feature vs cell size; slope/curvature vs resolution; cost vs resolution; "a finer grid is not a finer survey")
- 3.6 Relative vs absolute accuracy; internal consistency vs external truth
- 3.7 Writing a requirement that can be tested: acceptance criteria, sample design, deliverables
**Math.** Nyquist preview (cell ≤ ½ smallest feature); slope error vs cell size; vertical→horizontal error on slopes Δx = Δz / tan β.
**Standards & guides.** ISO 19157; ASPRS Positional Accuracy Standards Ed. 2; USGS Lidar Base Specification quality levels; IHO S-44 orders; ICAO Annex 15 terrain areas; FEMA elevation guidance.
**Key references.** Chrisman 1991 (fitness for use, in Maguire et al.); Veregin 1999 (in Longley et al.); Hengl 2006 *Comput. Geosci.* (right pixel size); Zhang & Montgomery 1994 *WRR*; Guth et al. 2021 *Remote Sens.* (terminology); Gesch 2018 *Front. Earth Sci.*
**Pitfalls.** Specifying "1 m DEM" without point density, surface type, and accuracy test; requiring accuracy you cannot verify; demanding global integration for a purely local volume job (or the reverse); confusing resolution with accuracy.
**Key takeaways.** Requirements must be testable statements; local vs integrated is a choice with consequences for datum, control, and cost; justify resolution by the smallest feature and the derivative you need.

## Part II — Vocabulary and the foundations of correctness

### Chapter 4 — Names and definitions: DEM, DSM, DTM, and the words that bite
**Scope.** Make the vocabulary explicit, including terms whose meaning differs across communities.
**Sections.**
- 4.1 DEM as umbrella; DSM, DTM, DHM/nDSM, CHM, DBM (bathymetric), topobathymetric model; "bare earth," "first/last return," "reflective surface"
- 4.2 Elevation, height, altitude, depth, sounding, reduced sounding, draft; orthometric, normal, dynamic, ellipsoidal heights; geopotential number; geoid undulation N
- 4.3 Grid, raster, cell, pixel, post, node; pixel-is-area vs pixel-is-point; gridline vs pixel registration (GMT)
- 4.4 Resolution vs GSD vs post spacing vs point density vs footprint vs effective resolution
- 4.5 Accuracy, precision, trueness, uncertainty, repeatability, reproducibility (ISO 5725, GUM)
- 4.6 Datum, reference frame, CRS, epoch, realization; "WGS84" as at least six different things
- 4.7 Hydrographic vocabulary: chart datum, sounding datum, TVU/THU/TPU, Order, feature detection, CATZOC
- 4.8 Lidar vocabulary: NPS/NPD/ANPD, swath/strip, QL0–QL3, ASPRS classification codes, withheld/synthetic/key-point/overlap flags
- 4.9 Photogrammetry/CV vocabulary: GSD, base-to-height, GCP vs checkpoint, bundle adjustment, dense matching, tie points
- 4.10 Radar vocabulary: slant/ground range, layover, foreshortening, shadow, coherence, height of ambiguity, penetration depth
- 4.11 Community collisions: "resolution," "accuracy," "control," "calibration," "validation," "verification," "ground truth," "model"
- 4.12 Style guide for this handbook; a plea for metadata that uses these words precisely
**Then & now.** "Digital terrain model" coined at MIT (Miller & Laflamme 1958); "pixel" (Billingsley 1965 ⟨H⟩); DEM as a USGS product name (1970s); DSM/DTM split popularized by lidar (1990s); Guth et al. 2021 standardization attempt.
**Standards & guides.** Guth et al. 2021; ISO 19157; ISO 5725; JCGM 100 (GUM); IHO S-32 Hydrographic Dictionary; ASPRS LAS 1.4 R15; USGS LBS glossary; IHO S-44 definitions.
**Key references.** Miller & Laflamme 1958 *Photogramm. Eng.*; Doyle 1978 *PE&RS*; Guth et al. 2021; Maune & Nayegandhi 2018 ch. 1; Pike 2000 *Prog. Phys. Geog.*
**Pitfalls.** Catalog "DEM" that is a DSM; "WGS84" without realization/epoch; "MSL" used to mean geoid; feet vs meters (the US survey foot was retired at the end of 2022); "resolution" meaning cell size of a resampled product.
**Key takeaways.** Every elevation number needs five qualifiers — which surface, which datum (and epoch), which cell semantics, which resolution (nominal and effective), which uncertainty.

### Chapter 5 — Error, uncertainty, accuracy, precision, resolution — the statistical toolkit
**Scope.** The quantitative language used by every later chapter.
**Sections.**
- 5.1 Error types: blunders/outliers, systematic (bias, drift, scale), random; spatially correlated error; artefacts
- 5.2 Describing error: mean error, RMSE, σ, MAE, median, NMAD, percentiles, LE68/LE90/LE95, CE90/CE95, 3D accuracy; when Gaussian multipliers (1.6449, 1.96, 2.4477) are valid and when they are not
- 5.3 Uncertainty vs error: GUM Type A/B, coverage factors, confidence vs tolerance; TPU/TVU/THU; "95 % uncertainty" semantics in BAG/S-102
- 5.4 Propagation: first-order (Jacobian) variance propagation; Monte Carlo; sequential Gaussian simulation for correlated error fields; effective sample size
- 5.5 Spatial structure of DEM error: variograms, correlation length; consequences for volumes, slopes, change detection
- 5.6 Reference data are uncertain too: hierarchy of accuracy (3–10× rule), independence, sample size and stratification, checkpoint vs control
- 5.7 Relative vs absolute accuracy; internal (overlap/crossline) vs external checks
- 5.8 Resolution, precision, quantization: int16 meters (SRTM), float32, Terrain-RGB; quantization noise σ = q/√12
- 5.9 Least squares as the unifying engine: observations, weights, residuals, redundancy, data snooping (Baarda), network adjustment; the Kalman filter as recursive least squares
- 5.10 Reporting: accuracy-statement template; uncertainty rasters; what never to report (a bare RMSE without n, land cover, date, reference)
**Math.** Σ_y = J Σ_x Jᵀ; RMSE, NMAD = 1.4826·MAD; LE95 = 1.96·RMSE only if unbiased and Gaussian; CE95 ≈ 2.4477·σ (circular); kriging variance; limit of detection LoD = t·√(σ₁² + σ₂²); quantization noise; weighted normal equations; Kalman predict/update.
**Software.** Open: xdem, demcoreg, scikit-gstat/gstools, NumPy/SciPy, R gstat, PDAL `filters.stats`, GDAL. Closed: CARIS/Qimera TPU engines, TerraScan/TerraMatch reports.
**Standards & guides.** JCGM 100/101; ISO 19157; ASPRS Ed. 2; FGDC NSSDA; IHO S-44; NOAA HSSD TPU section.
**Key references.** Mikhail & Ackermann 1976 *Observations and Least Squares*; Ghilani 2017 *Adjustment Computations*; JCGM 100:2008; Höhle & Höhle 2009 *ISPRS J.*; Fisher & Tate 2006; Wechsler 2007 *HESS*; Heuvelink 1998; Hugonnet et al. 2022 *IEEE JSTARS*; Rolstad et al. 2009 *J. Glaciol.*; Cressie 1993; Chilès & Delfiner 2012; Baarda 1968; Kalman 1960 ⟨H⟩; Hare 1995 *IHR*; Calder 2006 *IEEE JOE*.
**Pitfalls.** RMSE with outliers (use robust statistics); 95 % from 1.96×RMSE on skewed vegetated errors; ignoring spatial correlation (volume uncertainty looks 100× too small); reusing control points as checkpoints; checkpoints in a different datum/epoch; reporting precision as accuracy.
**Key takeaways.** No accuracy without a reference, a sample design, and a date; model the spatial structure of error or downstream uncertainty is fiction; least squares/Kalman is the shared engine of GNSS, INS, bundle adjustment, SLAM, strip adjustment, and network adjustment.

### Chapter 6 — Time as a coordinate: epochs, clocks, synchronization
**Scope.** Everything that makes "when" part of "where."
**Sections.**
- 6.1 Time scales: TAI, UTC and leap seconds (to be discontinued by 2035), GPS/GLONASS/Galileo/BeiDou time, Unix time (1970 ⟨H⟩), GPS week rollover; nautical time (1917 ⟨H⟩); Julian/Gregorian calendars in historical surveys (1582 ⟨H⟩)
- 6.2 Clocks: pendulum 1656 → chronometer 1761 → quartz → cesium 1955 ⟨H⟩ → optical; relativity in GNSS
- 6.3 Synchronization on moving platforms: PPS, NMEA ZDA, PTP/IEEE 1588, NTP (1979 ⟨H⟩); latency → position error v·Δt; event marks (mid-exposure, laser shot, ping)
- 6.4 Epochs of coordinates and datums: NAD83(2011) epoch 2010.00, ITRF2020 at epoch t, GDA2020, dynamic datums; "coordinate + epoch + velocity"
- 6.5 Temporal metadata for elevation: acquisition start/end, per-pixel dates, composite dates, validity windows
- 6.6 Time in formats: LAS GPS time (week vs adjusted standard), GSF, SBET, EXIF, NetCDF time units
**Math.** v·Δt; relativistic clock offset (~38 μs/day); Allan variance.
**Software.** chrony/ntpd/ptp4l; gpsd; NASA SPICE time utilities ⟨H⟩; Astropy `time`; RTKLIB.
**Standards.** BIPM; IEEE 1588-2019; RFC 5905; CGPM 2022 Resolution 4; ISO 8601; IERS Conventions 2010.
**Key references.** Ashby 2003 *Living Rev. Relativ.*; Allan 1966; Levine 2008 *Metrologia*; Sobel 1995 *Longitude*; Petit & Luzum 2010.
**Pitfalls.** LAS week time mistaken for adjusted standard time (10⁹ s offset); unsynchronized camera/IMU clocks → position error proportional to speed; leap-second mishandling at year boundaries; comparing coordinates from different epochs on fast plates (Australia ~7 cm/yr).
**Key takeaways.** A position is a position at a time in a frame; synchronization errors are geometric errors in disguise.

## Part III — Where is "here"? Geodesy, datums, projections

### Chapter 7 — The shape of the Earth: ellipsoid, geoid, gravity, heights
**Scope.** The physical and geometric geodesy needed to interpret any elevation.
**Sections.**
- 7.1 Sphere → ellipsoid: Eratosthenes, arc measurements (Lapland/Peru 1735–44), Airy 1830 ⟨H⟩, Clarke 1861/1866 ⟨H⟩, Bessel 1841, Hayford 1909, GRS80 1980 ⟨H⟩, WGS84 1984 ⟨H⟩
- 7.2 Gravity and the geoid: Stokes 1849, free-air/Bouguer anomalies, Molodensky and the quasigeoid, normal gravity, deflection of the vertical
- 7.3 Height systems: ellipsoidal h, orthometric H, normal, dynamic; geopotential numbers; h = H + N (and why it is not exact)
- 7.4 Geoid models: EGM84/96/2008 ⟨H⟩, XGM2019e, hybrid national geoids (GEOID18, CGG2013a, AUSGeoid2020, OSGM15), xGEOID → GEOID2022/NAPGD2022; accuracies and how they are validated (Geoid Slope Validation Surveys 2011/2014/2017)
- 7.5 Measuring gravity: pendulums, relative/absolute gravimeters, airborne (GRAV-D), satellite (GRACE 2002, GOCE 2009, GRACE-FO 2018), quantum gravimeters
- 7.6 Levelling: spirit, trigonometric, GNSS-levelling; loop closures; systematic errors
- 7.7 Mean sea level is not the geoid: mean dynamic topography (±1–2 m)
- 7.8 Earth tides, ocean and atmospheric loading — the cm-level breathing of the surface
**Math.** Ellipsoid (a, f, e²); normal gravity; spherical-harmonic expansion of the potential; Stokes' integral (sketch); h = H + N; dynamic height C/γ₄₅.
**Software.** PROJ + PROJ-data geoid grids; GeographicLib (GeoidEval, Gravity); NGS GEOID tools; ICGEM service; pyshtools.
**Standards & guides.** IERS Conventions 2010; NGS Blueprint Parts 1–3 (NOAA TR NOS NGS 62/64/67); ISO 19111.
**Key references.** Torge & Müller 2012 *Geodesy*; Hofmann-Wellenhof & Moritz 2006 *Physical Geodesy*; Heiskanen & Moritz 1967; Meyer 2010; Vaníček & Krakiwsky 1986; Pavlis et al. 2012 *JGR* (EGM2008); Smith et al. 2013 *J. Geod.* (GSVS11); Tapley et al. 2004 *GRL*; Hirt et al. 2013 *GRL* (GGMplus); Jekeli 2016 lecture notes.
**Pitfalls.** Subtracting a geoid model from GNSS heights without checking which datum the model realizes ("NAVD88 ≠ EGM2008 orthometric"); treating MSL as zero everywhere; ignoring dynamic heights on large lakes; forgetting geoid errors are spatially correlated (tilts, not noise).
**Key takeaways.** GNSS gives ellipsoidal heights; nearly every user wants gravity-related heights; the geoid model is the bridge and has its own spatially structured uncertainty.

### Chapter 8 — Horizontal datums and terrestrial reference frames
**Scope.** Frames, realizations, epochs, and transformations.
**Sections.**
- 8.1 Classical datums (NAD27 1927 ⟨H⟩, ED50, Tokyo) → geocentric (NAD83, WGS84, ITRF); why NAD27→NAD83 shifts exceed 100 m
- 8.2 ITRS/ITRF realizations (ITRF88…2014, 2020), IGS frames, WGS84 realizations (G730…G2296), ETRS89, GDA94→GDA2020, NAD83(CSRS), JGD2011, SIRGAS; plate-fixed vs Earth-fixed
- 8.3 Epochs and velocities: ITRF2014 plate-motion model, HTDP (1992 ⟨H⟩), modernized NSRS (NATRF2022 and sister frames), dynamic datums (NZGD2000), semi-dynamic corrections (Japan)
- 8.4 Transformations: Helmert 7/14-parameter, Molodensky–Badekas, grid shifts (NTv2, NADCON5), time-dependent; concatenation errors; "WGS84 to WGS84" is not identity
- 8.5 Encoding CRSs: EPSG (1985/1993 ⟨H⟩), WKT1 → WKT2 (ISO 19162:2019), PROJJSON, axis-order wars (EPSG:4326 is lat/lon), bound and compound CRSs (with vertical)
- 8.6 Horizontal control: triangulation (GB 1791–1853 ⟨H⟩, GTS India), traverses, GNSS networks, CORS (1994)
- 8.7 Horizontal accuracy of DEMs: why it matters on slopes, how it is tested (feature-based, ICP, cross-correlation), typical values (SRTM ~9 m CE90; Copernicus DEM < 6 m; lidar < 0.3 m)
**Math.** x′ = T + (1+s)·R·x; time-dependent parameters; grid-shift interpolation.
**Software.** Open: PROJ/pyproj, GeographicLib, NGS NCAT/HTDP, GEOTRANS. Closed: Blue Marble Geographic Calculator, Trimble Coordinate System Manager; transformation pickers in ArcGIS/QGIS.
**Standards.** ISO 19111:2019; ISO 19162; IOGP Guidance Note 373-7-2; EPSG Geodetic Parameter Dataset; IERS Conventions.
**Key references.** Altamimi et al. 2016 *JGR* (ITRF2014), 2017 *GJI* (plate model), 2023 *J. Geod.* (ITRF2020); Snay 1999; Pearson & Snay 2013 *GPS Solut.*; Soler & Hothem 1988; Iliffe & Lott 2008; ICSM GDA2020 Technical Manual; Snay & Soler 2008 *J. Surv. Eng.*
**Pitfalls.** Ignoring epoch (meters in Australia; decimeters in California per decade); default null WGS84↔NAD83 transformations (~1–2 m); 2D transformations applied to 3D data; shapefile `.prj` files that cannot express realization; EPSG codes copied without axis order.
**Key takeaways.** A horizontal datum is frame + realization + epoch; sub-meter work needs all three; the plate beneath you moves about as fast as your fingernails grow — and decade-old control shows it.

### Chapter 9 — Vertical datums: orthometric, ellipsoidal, tidal, and home-made
**Scope.** The most common source of gross error in merged elevation products.
**Sections.**
- 9.1 National orthometric datums: NGVD29 → NAVD88 → NAPGD2022; CGVD28 → CGVD2013; ODN, NAP, DHHN2016, EVRF2019, AHD, NZVD2016; how realized (levelling vs geoid-based) and their known tilts/biases (AHD ≈ 0.5 m north–south; NAVD88 ≈ 0.5 m tilt across CONUS)
- 9.2 Ellipsoidal heights as a working datum (ellipsoidally referenced surveys, ERS)
- 9.3 Tidal datums: MSL, MLW, MLLW, MHW, MHHW, LAT/HAT, MLWS; National Tidal Datum Epoch (1983–2001; 2002–2020), modified epochs where relative SLR is fast; computation at gauges (19-year averaging, simultaneous comparison); zoning across a survey (TCARI)
- 9.4 Chart and sounding datums: national conventions (MLLW US; LAT for most IHO states); reduction of soundings; dynamic draft/squat; predicted vs observed vs ERS water-level corrections
- 9.5 Lake, river, and project datums: IGLD 1985 (dynamic heights), river-gauge datums and "stage," "assumed elevation 100.00," construction and mine grids, RTK "site calibration/localization," island and legacy datums, "sea level" as a datum
- 9.6 What happens when people create their own datums: why (speed, isolation, legal/engineering habit); costs (merging, change detection, liability, staff turnover); doing it safely (tie to national control at ≥ 2 marks, publish the transformation, keep ellipsoidal heights in parallel)
- 9.7 Vertical transformations: VDatum (US), geoid grids, separation (SEP) models, AusCoastVDT, VORF (UK), European BLAST/EMODnet; transformation uncertainty (cm offshore → dm in estuaries)
- 9.8 The land–water seam: NAVD88 vs MLLW zero differs by meters at the coast; NAP vs TAW ≈ 2.3 m across the Dutch–Belgian border; NGVD29–NAVD88 up to ~1.5 m
- 9.9 Vertical datums on ice and other planets (areoid; lunar sphere)
**Math.** H = h − N; tidal-datum computation; TVU contribution of water-level reduction; S = N + (MSL − geoid) + (CD − MSL).
**Software.** NOAA VDatum; NGS VERTCON/GEOID; PROJ vertical grids; CARIS/Qimera SEP models; AusCoastVDT; VORF.
**Standards & guides.** NOAA CO-OPS *Tidal Datums and Their Applications* (2000) and *Computational Techniques for Tidal Datums Handbook* (2003); IOC Manuals and Guides 14; FIG Publication 62 (Dodd & Mills 2012); NOAA HSSD water-levels chapter; NGS-58/59; IHO S-44.
**Key references.** Zilkoski, Richards & Young 1992 (NAVD88); Parker et al. 2003 *Sea Technology* (VDatum); Hess 2003 *Cont. Shelf Res.* (TCARI); Dodd & Mills 2011 *IHR*; Pugh & Woodworth 2014 *Sea-Level Science*; Véronneau & Huang 2016 (CGVD2013); NGS Blueprint Part 2; Eakins & Grothe 2014; Shalowitz 1962/1964 *Shore and Sea Boundaries*; Coordinating Committee 1992 (IGLD 1985).
**Pitfalls.** "MSL" of unknown epoch; applying a land geoid offshore; predicted tides when observed differ by decimeters (surge); mixing LAT and MLLW; feet vs meters on legacy benchmarks; undocumented local datums; forgetting that tidal datums (and legal shorelines) move with every epoch update.
**Key takeaways.** Document the vertical datum, its epoch, and the transformation used, or the product cannot be merged or trusted; survey to the ellipsoid and reduce to whatever the user needs; the coast is where three height systems meet.

### Chapter 10 — Map projections, grids, and the resampling they force
**Scope.** Projections as necessary distortion; grids as a sampling decision.
**Sections.**
- 10.1 Geographic grids and anisotropic cells (1″ cells are ~30 m × cos φ); when to stay in lat/lon
- 10.2 Properties and distortion (conformal, equal-area, equidistant; Tissot); projection choice for DEMs (UTM 1942 ⟨H⟩, polar stereographic for ice sheets, LAEA for Europe, national grids; Web Mercator's sins)
- 10.3 Grid vs ground distance; combined scale factor; low-distortion projections for engineering (SPCS2022)
- 10.4 Reprojection = resampling: nearest/bilinear/cubic/Lanczos/average; effects on elevation, slope, nodata; resampling uncertainty; "reproject once, late"
- 10.5 Tiling: USGS quads, SRTM 1°×1° (3601², overlapping edges), Copernicus tiles, XYZ/TMS/WMTS, quadkeys; DGGS preview (Ch. 60)
- 10.6 Zone boundaries and seams; UTM overlap; polar regions
- 10.7 CRS metadata in grids: GeoTIFF keys, WKT2, PROJJSON; the half-pixel shift (pixel-is-area vs pixel-is-point)
**Math.** Scale factor k; Transverse Mercator (Krüger/Karney series); Tissot indicatrix; bilinear/cubic kernels; area of a geographic cell.
**Software.** PROJ; GDAL (`gdalwarp -r`); GMT; rasterio; QGIS/ArcGIS; GeographicLib.
**Standards.** EPSG; ISO 19111; OGC Two-Dimensional Tile Matrix Set; Snyder 1987 as de-facto reference.
**Key references.** Snyder 1987 USGS PP 1395 ⟨H⟩; Snyder 1993 *Flattening the Earth*; Karney 2011 *J. Geod.* (TM to nanometers); Evenden 1990 (PROJ) ⟨H⟩; Dennis 2023 NOAA Manual NOS NGS 13 (SPCS2022); Iliffe & Lott 2008.
**Pitfalls.** Slope on a lat/lon grid without separate x/y scaling; cubic resampling overshoot creating new pits/peaks and smearing nodata; Web Mercator in area/volume computations; UTM zone mismatch at seams; forgetting the half-cell shift when converting registration conventions.
**Key takeaways.** Every projection and resampling changes elevations slightly and derivatives a lot; stay in the native grid as long as possible and record each resampling in metadata.

## Part IV — Positioning and orientation

### Chapter 11 — A history of positioning: from plumb bobs to PPP
**Scope.** Narrative chapter anchored in the gis-history timeline; explains why today's methods look the way they do.
**Sections.**
- 11.1 Antiquity to the Renaissance: plumb bob (Egypt ⟨H⟩), gnomon, Eratosthenes, Hipparchus and trigonometry (~140 BC ⟨H⟩), compass (206 BC; navigation 11th c. ⟨H⟩), Antikythera ⟨H⟩, portolans, Mercator 1569 ⟨H⟩
- 11.2 Instruments: plane table 1551, theodolite 1576, Gunter's chain 1620, octant 1699, sextant 1731, Brunton compass 1894, tellurometer 1957 ⟨H⟩, total station
- 11.3 Longitude and time: pendulum clock 1656, Rømer 1676, Harrison H4 1761, Meridian Conference 1884 ⟨H⟩, UT 1928/UTC 1960 ⟨H⟩
- 11.4 National surveys: Cassini, Principal Triangulation of GB 1791–1853 ⟨H⟩, US Coast Survey 1807 ⟨H⟩, Great Trigonometrical Survey of India, Gauss and least squares, Buttermilk mark 1833 ⟨H⟩, USGS 1879 ⟨H⟩
- 11.5 Radio navigation: Gee 1940, LORAN 1942, Decca 1942, CHAYKA 1969, LORAN-C civil 1974 ⟨H⟩, Omega, eLoran revival
- 11.6 Inertial: first INS 1942 ⟨H⟩, Kalman 1960 ⟨H⟩, strapdown, MEMS
- 11.7 Satellites: Sputnik 1957 ⟨H⟩, Transit/NNSS 1964, GPS 1978 ⟨H⟩, GLONASS 1982 ⟨H⟩, RINEX 1989 ⟨H⟩, NMEA 0183 1984 ⟨H⟩, CORS/IGS 1994, DGPS 1996 ⟨H⟩, SA off 2000 ⟨H⟩, WAAS 2003 ⟨H⟩, BeiDou 2000 ⟨H⟩, Galileo 2011/2016 ⟨H⟩, PPP 1997, RTK 1990s
- 11.8 Underwater: lead line → acoustic transponders (LBL/USBL) → INS + DVL
- 11.9 The mobile age: cell/WiFi positioning, wardriving 2000 ⟨H⟩, phones mapping the ionosphere 2024 ⟨H⟩
- 11.10 What history teaches about error: each generation's "accurate" became the next generation's "biased"
**Key references.** Sobel 1995; Hofmann-Wellenhof, Lichtenegger & Wasle 2008 (history chapter); Kaplan & Hegarty 2017 ch. 1; Snay & Soler 2008; NOAA history (Theberge); gis-history timeline.
**Pitfalls.** Legacy positions fixed by LORAN/celestial still on modern charts; reading historical accuracy claims with today's definitions.
**Key takeaways.** Positioning accuracy improved roughly tenfold per generation; datums and products inherit the positioning technology of their era — know the vintage of what you merge.

### Chapter 12 — GNSS for elevation work
**Scope.** How GNSS positions are obtained and why the vertical component is the weak one.
**Sections.**
- 12.1 Constellations and signals (GPS L1/L2/L5, GLONASS, Galileo, BeiDou, QZSS, NavIC); observables: code, carrier phase, Doppler
- 12.2 Error sources: orbits/clocks, ionosphere (TEC; dual-frequency), troposphere (wet delay → height error), multipath, antenna phase-center variations (ANTEX), cycle slips, geometry (DOP); why vertical ≈ 2–3× horizontal
- 12.3 Modes: SPP, DGNSS/SBAS (WAAS/EGNOS), RTK and network RTK (VRS/MAC), PPK, PPP, PPP-AR/PPP-RTK; convergence; ambiguity resolution
- 12.4 Infrastructure and services: CORS, IGS, NRTK providers, OPUS/CSRS-PPP/AUSPOS; RTCM, NTRIP, RINEX/BINEX
- 12.5 Field practice for control and checkpoints: occupation time, antenna height (the classic blunder), monumentation, redundancy, NGS-58/59, ASPRS Ed. 2 Addendum II
- 12.6 GNSS on moving platforms: PPK trajectories for lidar/MBES/SfM, baseline length, base-station ties, trajectory quality metrics
- 12.7 Heights from GNSS are ellipsoidal — bridge to Ch. 7 and 9
- 12.8 Threats and hard environments: jamming/spoofing, ionospheric storms at solar maximum, urban canyons (shadow matching), under canopy
- 12.9 Consumer vs survey receivers; smartphone dual-frequency; low-cost RTK (u-blox F9P class) — what to expect and how to verify
**Math.** Pseudorange and carrier-phase observation equations; single/double differences; DOP from the geometry matrix; tropospheric mapping functions (sketch).
**Software.** Open: RTKLIB, PRIDE PPP-AR, gLAB, GNSS-SDR, GAMIT/GLOBK (academic license). Services: OPUS, CSRS-PPP, AUSPOS. Closed: Trimble Business Center, Leica Infinity, NovAtel Inertial Explorer, Bernese.
**Standards & guides.** RINEX 3/4; RTCM 10403.x; NMEA 0183/2000; NGS-58/59; NGS RTN guidelines; ASPRS Ed. 2 Addendum II; IGS conventions.
**Key references.** Teunissen & Montenbruck (eds.) 2017 *Springer Handbook of GNSS*; Misra & Enge 2011; Kaplan & Hegarty 2017; Hofmann-Wellenhof et al. 2008; Zumberge et al. 1997 *JGR* (PPP); Dow, Neilan & Rizos 2009 (IGS); Soler et al. 2006 (OPUS); Takasu & Yasuda 2009 (RTKLIB); Geng et al. 2019 (PRIDE); Williams et al. 2024 *Nature* ⟨H⟩; Leick, Rapoport & Tatarnikov 2015.
**Pitfalls.** Antenna height to the wrong reference (ARP vs phase center; slant vs vertical); ellipsoidal and orthometric heights mixed in one checkpoint file; short occupations under canopy; RTK fixed to a base with wrong coordinates (whole-survey offset); NRTK datum differing from the project datum; ignoring the CORS coordinate epoch.
**Key takeaways.** GNSS vertical accuracy is bounded by troposphere, geometry, and multipath, not receiver price; every GNSS survey needs documented base coordinates, datum/epoch, antenna model, and redundancy.

### Chapter 13 — IMU/INS, motion sensing, and GNSS-aided navigation
**Scope.** Orientation and short-term motion that every scanning sensor needs.
**Sections.**
- 13.1 Sensors: gyroscopes (MEMS, FOG, RLG), accelerometers; grades; bias, drift, scale factor, noise (Allan variance)
- 13.2 Strapdown mechanization; Euler/DCM/quaternion attitude; heading (gyrocompass, dual-antenna GNSS, magnetometer + declination from WMM/IGRF)
- 13.3 Integration: Kalman filter; loosely/tightly/deeply coupled GNSS/INS; RTS smoothing → SBET; error-state formulation
- 13.4 Marine motion: roll, pitch, heave and induced heave, yaw; MRUs (POS MV, Octans, SBG); lever arms and the reference point ("what is it we are really aligning?")
- 13.5 Airborne: boresight (IMU–sensor misalignment), lever arms, timing; calibration flights; feedback from strip adjustment
- 13.6 Cars and GNSS outages: urban canyons, tunnels, odometer aiding, zero-velocity updates; drift growth laws
- 13.7 Underwater: INS + DVL + USBL; dead-reckoning error growth
- 13.8 Judging a trajectory: SBET RMS, forward/backward separation, overlap statistics in the mapped data
**Math.** INS error growth (t², t³ terms); lever arm r_sensor = r_ref + R·l; small-angle boresight rotation; Kalman predict/update; Allan deviation.
**Software.** Open: ROS 2 `robot_localization`, OpenVINS, Kalibr, GTSAM. Closed: Applanix POSPac MMS, NovAtel Inertial Explorer, SBG Qinertia, iXblue Delph INS.
**Standards & guides.** IEEE Std 952/1554; NOAA FPM (vessel offsets, patch test); USGS LBS trajectory requirements.
**Key references.** Groves 2013 *Principles of GNSS, Inertial, and Multisensor Integrated Navigation*; Titterton & Weston 2004; Farrell 2008; Kalman 1960; El-Sheimy, Hou & Niu 2008 (Allan variance); Hughes Clarke 2003 (vessel coordinate systems, US Hydro); Skaloud & Lichti 2006 *ISPRS J.* (boresight); Glennie 2007 *J. Appl. Geod.*
**Pitfalls.** Vendor-specific lever-arm sign conventions; heave-filter settling after turns (artefacts at line starts); magnetometer heading near steel; induced heave applied at the wrong point; trajectory and base station in different frames/epochs.
**Key takeaways.** Attitude error scales with range — 0.01° of roll is 17 cm at 1 km; the trajectory, not the sensor, usually limits DEM accuracy from moving platforms.

### Chapter 14 — Positioning without (or beyond) GNSS
**Scope.** Methods that complement GNSS or replace it where it fails.
**Sections.**
- 14.1 Acoustic positioning: LBL, SBL, USBL, inverted USBL; sound-speed dependence; calibration (box-in)
- 14.2 Terrain-aided/terrain-relative navigation: TERCOM, submarine bathymetric navigation, Mars 2020 Lander Vision System, AUVs over mapped seafloor — the DEM becomes the positioning system and its errors become yours
- 14.3 Visual odometry and visual-inertial navigation; map matching
- 14.4 Radio and indoor: eLoran, UWB, WiFi/BLE/cellular, 5G positioning
- 14.5 Total stations, laser trackers, traverses, levelling
- 14.6 Celestial navigation as backup
- 14.7 Barometric altimetry: drones' "AGL," phones, aircraft QNH — and its weather-driven errors
- 14.8 Signals of opportunity and GNSS reflectometry (CYGNSS; altimetry)
**Math.** USBL range/bearing error propagation; barometric formula and its sensitivity; terrain-matching likelihood.
**Software.** PX4/ArduPilot EKF (open); ROS packages; Sonardyne/iXblue/Kongsberg HiPAP suites (closed).
**Key references.** Golden 1980 (TERCOM); Johnson & Montgomery 2008 (TRN); Milne 1983 *Underwater Acoustic Positioning Systems*; Groves 2013; Mars 2020 LVS flight-performance papers (2022).
**Pitfalls.** Drone missions flown at "400 ft AGL" on SRTM in mountainous terrain; USBL without a sound-speed profile; barometric drift over a long survey day.
**Key takeaways.** Without GNSS, position error grows with time or inherits map quality — plan for it explicitly.

### Chapter 15 — SLAM: solving the map and the trajectory together
**Scope.** Simultaneous localization and mapping as the unifying modern formulation; indoor, underground, and "innerspace" mapping.
**Sections.**
- 15.1 Origins (Smith & Cheeseman 1986 ⟨H⟩) → EKF-SLAM → particle filters → graph SLAM and factor graphs (g2o, GTSAM, Ceres)
- 15.2 Lidar SLAM (LOAM, LIO-SAM, FAST-LIO2, Cartographer, KISS-ICP), visual and visual-inertial SLAM (ORB-SLAM3), RGB-D; loop closure and place recognition
- 15.3 Relationship to bundle adjustment and survey network adjustment (same least squares, different priors)
- 15.4 Handheld and backpack scanners (GeoSLAM, Leica BLK2GO, NavVis, Hovermap); mines, caves, tunnels, ship interiors, buildings — innerspace
- 15.5 Georeferencing SLAM maps: control, GNSS where available, drift correction; evaluation (APE/RPE; KITTI, EuRoC, TUM, Hilti)
- 15.6 Where SLAM-derived terrain fits (construction, under-canopy DTMs, urban canyons) and where it fails (featureless corridors, long loops, crowds)
- 15.7 Uncertainty in SLAM outputs (covariances are often optimistic)
**Math.** Pose-graph optimization; ICP/GICP objectives; factor-graph MAP estimate; trajectory error metrics.
**Software.** Open: ROS 2, Cartographer, LIO-SAM, FAST-LIO2, ORB-SLAM3, GTSAM, g2o, Ceres, Open3D, KISS-ICP. Closed: GeoSLAM Connect, Leica Cyclone, NavVis IVION, Emesent.
**Key references.** Smith & Cheeseman 1986 *IJRR*; Durrant-Whyte & Bailey 2006 *IEEE RAM*; Cadena et al. 2016 *IEEE T-RO*; Thrun, Burgard & Fox 2005 *Probabilistic Robotics*; Besl & McKay 1992 (ICP); Zhang & Singh 2014 (LOAM); Xu et al. 2022 (FAST-LIO2); Campos et al. 2021 (ORB-SLAM3); Grisetti et al. 2010 (graph SLAM tutorial); Dellaert & Kaess 2017; Zhang & Scaramuzza 2018 (trajectory evaluation).
**Pitfalls.** Treating SLAM output as surveyed (1–2 % drift without loop closure; scale drift in monocular); comparing SLAM DTMs to lidar DTMs without co-registration; indoor "elevations" with no vertical-datum tie.
**Key takeaways.** SLAM is least squares with a map prior; its accuracy is relative unless tied to control; it is the only practical option in GNSS-denied innerspace.

## Part V — Sensors and platforms

### Chapter 16 — Platforms
**Scope.** Where sensors sit and what each vantage point implies for coverage, resolution, accuracy, cost, and regulation.
**Sections.**
- 16.1 Humans on foot: GNSS rovers, total stations, levelling, backpack lidar/SLAM, handheld photogrammetry, phone lidar
- 16.2 Cars and rail: mobile mapping systems (Street View 2007/2008 ⟨H⟩), survey vans, urban-canyon GNSS, rail clearance scanners
- 16.3 Boats, ships, USVs, AUVs, ROVs (OpenROV 2011 ⟨H⟩), submarines, divers; ships of opportunity and crowdsourced bathymetry
- 16.4 Drones: multirotor, fixed-wing, VTOL; payload classes; RTK/PPK; regulations (FAA Part 107, EASA); drone lidar vs drone SfM; DJI 2006 ⟨H⟩
- 16.5 Kites, balloons, blimps, poles (Nadar's balloon 1858 ⟨H⟩; kite aerial photography)
- 16.6 Crewed aircraft and helicopters: altitude/speed/swath trade-offs; regional programs (USGS 3DEP, JALBTCX NCMP)
- 16.7 High-altitude platforms and pseudo-satellites
- 16.8 Satellites: orbits and revisit, swath vs resolution, agility and stereo; optical (Ikonos 1999, QuickBird, WorldView, Pléiades, Legion ⟨H⟩), SAR (Seasat 1978, ERS, Sentinel-1 2014 ⟨H⟩, TanDEM-X, ALOS-2, NISAR, Biomass 2025 ⟨H⟩), lidar (ICESat 2003, ICESat-2 and GEDI 2018 ⟨H⟩), altimetry (Geosat 1985, TOPEX 1992 ⟨H⟩ … SWOT 2022), gravity (GRACE/GOCE); Shuttle (SRTM) and ISS (GEDI)
- 16.9 Fixed infrastructure that senses the world: CORS and tide gauges; permanent terrestrial laser scanners (cliffs, snow, glaciers); ground-based radar interferometers (mine slopes); coastal video (Argus, CoastSnap), traffic/security webcams; seismometers; weather radars; harbor sonars; river gauges
- 16.10 The crowd as platform: phones (GNSS, barometer, cameras, ionosphere mapping ⟨H⟩), vehicle fleets, fishing-vessel sounders (IHO B-12), OSM mappers; trust and privacy preview
- 16.11 Platform-selection matrix: area, resolution, accuracy, environment (water, canopy, urban), cadence, cost, permits
**Then & now.** Balloon 1858 → aircraft 1910s → Corona 1959 ⟨H⟩ → Landsat 1972 ⟨H⟩ → Shuttle 2000 → consumer drones 2010s → smallsat constellations → USV/AUV fleets 2020s.
**Standards & guides.** FAA Part 107 / EASA; IHO B-12; USGS LBS; NOAA FPM vessel configuration; UNCLOS Part XIII (consent for marine scientific research in foreign EEZs).
**Key references.** Colomina & Molina 2014 *ISPRS J.* (UAS review); Nex & Remondino 2014; Holman & Stanley 2007 (Argus); Harley et al. 2019 (CoastSnap); Mayer et al. 2018; IHO B-12.
**Pitfalls.** Platform chosen by availability rather than requirement; drones in wind (blur, IMU noise); satellite revisit ≠ cloud-free revisit; hull-mounted sonars blinded by aeration; crowd data without provenance.
**Key takeaways.** The platform sets the error envelope before the sensor is switched on; fixed infrastructure and the crowd are under-used, cheap, and continuous — but need trust models.

### Chapter 17 — Measurement physics: a unified view
**Scope.** The handful of physical principles behind every elevation sensor, and what "the surface" means to each.
**Sections.**
- 17.1 Ranging: pulsed time-of-flight, phase, FMCW; range = c·t/2; speed of light vs sound; refraction
- 17.2 Parallax and triangulation: stereo, structured light, laser triangulation
- 17.3 Interferometry: InSAR, phase-differencing sonar; height of ambiguity
- 17.4 Radiometric inversion: satellite-derived bathymetry, shape-from-shading/photoclinometry, shadow-length heights
- 17.5 Potential-field inversion: gravity → predicted bathymetry/sub-ice beds
- 17.6 Footprint, beamwidth, divergence, and the sensor as a low-pass filter; footprint = R·θ
- 17.7 Which surface did we measure? First/last return, phase/scattering center, canopy and snow/ice penetration by wavelength (X/C/L/P band), water penetration (green vs NIR), bottom detection in sonar
- 17.8 The sensor–material interaction matrix (rock, vegetation, clear/turbid water, snow/ice, clouds, smoke/steam)
- 17.9 Noise, detection thresholds, and false alarms as the origin of outliers
**Math.** Two-way travel time; Snell's law (air–water n ≈ 1.33–1.34; sound-speed gradients); beam footprint; InSAR height of ambiguity; Nyquist preview.
**Key references.** Lurton 2010 *Introduction to Underwater Acoustics*; Shan & Toth 2018; Hanssen 2001; Jensen 2007 *Remote Sensing of the Environment*; Elachi & van Zyl 2006 *Introduction to the Physics and Techniques of Remote Sensing*.
**Pitfalls.** Assuming the measured surface is the ground (X-band DEMs sit meters above snow-covered ice); comparing sensors whose "surface" definitions differ and calling the difference "error"; ignoring refraction in bathy lidar.
**Key takeaways.** Each sensor measures a physically defined surface at a physically defined resolution; DEM comparison across sensors is a comparison of definitions first and errors second.

### Chapter 18 — Topographic lidar
**Scope.** Airborne, UAV, terrestrial, and mobile laser scanning for DSMs/DTMs.
**Sections.**
- 18.1 System types: discrete-return, full-waveform, single-photon/Geiger-mode, photon-counting (ICESat-2); multi-return; intensity; scan patterns; divergence and footprint; MTA ambiguity
- 18.2 The lidar georeferencing equation and its error budget (trajectory, boresight, lever arm, range, scan angle, timing, atmosphere)
- 18.3 Calibration and strip adjustment (boresight sites, overlap residuals, ICP-based strip adjustment)
- 18.4 Point density, NPS/ANPD, swath overlap, relative (intra/inter-swath) accuracy; USGS quality levels QL0–QL3
- 18.5 Vegetation penetration, leaf-off preference, ground-return statistics; water absorption at 1064 nm → voids
- 18.6 Terrestrial and mobile laser scanning: registration, targets, E57, urban canyons
- 18.7 UAV lidar: payload grades, flight planning, PPK, typical accuracies
- 18.8 Spaceborne lidar as sparse truth: ICESat/GLAS, ICESat-2 ATL03/06/08, GEDI L2A/L3
- 18.9 Deliverables and QA: classified LAS/LAZ, DTM/DSM, intensity, breaklines, project reports; LBS checks (voids, density, accuracy)
**Then & now.** Laser 1960 → first lidar 1961 ⟨H⟩ → airborne laser profiling 1960s–80s (Krabill et al. 1984) → commercial ALS mid-1990s → LAS 2003 ⟨H⟩ → national programs (3DEP 2012; AHN, EA, swissSURFACE3D) → single-photon lidar 2017+ → drone lidar everywhere 2020s.
**Math.** p = p_GNSS + R_nav·(l + R_boresight·r_scanner); range precision; footprint; error propagation of attitude × range.
**Software.** Open: PDAL, CloudCompare, lidR, laspy, PCL, Open3D, Potree, Entwine/untwine, OPALS (academic). Mixed: LAStools (partly open). Closed: TerraSolid (TerraScan/TerraMatch), Riegl RiPROCESS, Leica HxMap/Cyclone, Optech LMS, Global Mapper, ArcGIS, LP360.
**Standards & guides.** USGS Lidar Base Specification (2024 rev. A and successors); ASPRS Positional Accuracy Standards Ed. 2 (Addendum on lidar); ASPRS LAS 1.4 R15; NRCan Federal Airborne LiDAR Guideline; ICSM LiDAR Acquisition Specifications; LINZ base specification.
**Key references.** Shan & Toth 2018 *Topographic Laser Ranging and Scanning*; Vosselman & Maas 2010; Renslow (ed.) 2012 *Manual of Airborne Topographic Lidar*; Baltsavias 1999 *ISPRS J.*; Wehr & Lohr 1999; Glennie 2007; Schenk 2001; Glira et al. 2015 (strip adjustment); Hodgson & Bresnahan 2004 *PE&RS*; Mallet & Bretar 2009 (full waveform); Degnan 2016 and Stoker et al. 2016 (single-photon/Geiger); Neumann et al. 2019 (ICESat-2); Dubayah et al. 2020 (GEDI); Isenburg 2013 (LASzip); Butler et al. 2021 (PDAL); Roussel et al. 2020 (lidR).
**Pitfalls.** Point density mistaken for resolution; swath-edge and turn artefacts; "corduroy" from residual roll/timing; vegetated accuracy reported with Gaussian statistics; leaf-on acquisition sold as DTM-grade; GPS-time convention errors; classification codes reinterpreted between vendors.
**Key takeaways.** Lidar accuracy is a trajectory-and-calibration problem more than a laser problem; the ground is a classification decision; overlap statistics are your cheapest independent check.

### Chapter 19 — Bathymetric lidar and the land–water transition
**Scope.** Green-laser lidar, topobathy systems, spaceborne photon-counting bathymetry, and the "white ribbon."
**Sections.**
- 19.1 Physics: 532 nm propagation, water-surface detection, refraction correction (range and angle), Secchi depth and diffuse attenuation Kd, maximum depth ≈ 1.5–3× Secchi, bottom-return detection, turbidity, sea state, bottom albedo
- 19.2 Systems: CZMIL, Leica Chiroptera/HawkEye, Riegl VQ-880-G/-GII, Fugro RAMMS, ASTRALiTe, EAARL; topobathy vs bathy-only; UAV bathy lidar
- 19.3 Total propagated uncertainty for bathy lidar (refraction model, surface model, sea state, bottom type, trajectory)
- 19.4 Processing: waveform decomposition, surface/bottom classification, refraction correction, TPU, cleaning; deliverables (LAS with bathy classes, BAG, DEM)
- 19.5 Spaceborne photon-counting bathymetry: ICESat-2 ATL03 (≈ 40 m in clear water), refraction correction, use as SDB calibration
- 19.6 Bathy lidar vs topo lidar vs sonar: depth range, coverage rate, cost per km², environments (surf zone, reefs, rivers), the white ribbon between topo and hydro surveys
- 19.7 Program context: JALBTCX National Coastal Mapping Program, NOAA NGS, Litto3D, national programs
**Then & now.** First airborne laser bathymetry experiments late 1960s–70s → SHOALS 1990s → CZMIL/Chiroptera 2010s → UAV bathy lidar and ICESat-2 2018+.
**Math.** Snell refraction correction; depth-dependent TVU model; Kd attenuation.
**Software.** Open: PDAL (refraction scripts), CloudCompare, SlideRule (ICESat-2), OpenAltimetry, `icepyx`. Closed: Leica LSS, Teledyne Optech HydroFusion, Riegl RiHYDRO, Fugro proprietary, CARIS/Qimera for products.
**Standards & guides.** IHO S-44 Ed. 6; NOAA HSSD (lidar bathymetry annex); USACE EM 1110-2-1003; USGS LBS (topobathy addendum).
**Key references.** Guenther 1985 NOAA Prof. Paper 1; Guenther et al. 2000 (accuracy challenge); Philpot (ed.) 2019 *Airborne Laser Hydrography II*; Mandlburger 2022 *IHR* review; Fernandez-Diaz et al. 2014 (Titan); Nayegandhi et al. 2009 (EAARL); Parrish et al. 2019 *Remote Sens.* (ICESat-2 bathymetry); Quadros et al. 2008 (topo–bathy integration).
**Pitfalls.** Surface model errors doubling as depth errors; data gaps in the surf zone sold as "no features"; turbidity-limited depth presented as the seabed; mixing tidal and orthometric datums within one topobathy LAS.
**Key takeaways.** Bathy lidar fills the white ribbon but only where water is clear; its uncertainty is dominated by the water surface and refraction model, so publish those models with the data.

### Chapter 20 — Sonar: the many types and how they make bathymetry
**Scope.** From lead lines to multi-sector multibeam and synthetic aperture sonar.
**Sections.**
- 20.1 Underwater acoustics: sound speed (~1500 m/s) and profiles, ray bending, absorption vs frequency, beam patterns, the sonar equation, bottom detection (amplitude vs phase)
- 20.2 The family tree: lead line and wire drag; single-beam (incl. dual-frequency); multibeam (Mills cross, beamforming, sectors, dual-swath, dual-head, FM chirp, water column); interferometric/phase-differencing bathymetric sonar; side-scan; synthetic aperture sonar; sub-bottom profilers and seismic (chirp, boomer, sparker) — the sub-seafloor "DEMs"; parametric; forward-looking and imaging sonars (ARIS/Oculus); scanning sonars; fisheries split-beam (calibration spheres); ADCP/DVL (positioning, not mapping)
- 20.3 Multibeam geometry: footprint growth with depth and angle, outer-beam degradation, swath width vs depth, nadir gap in side-scan, sounding density vs grid resolution
- 20.4 Integration: motion (roll/pitch/heave/yaw), latency, lever arms, waterline and draft, squat/settlement, sound-speed casts, tides/ERS; the patch test; refraction artefacts ("smiles/frowns")
- 20.5 Uncertainty: Hare–Godin–Mayer TPU; S-44 TVU = √(a² + (b·d)²) and THU; CUBE/CHRT as uncertainty-weighted estimators; crossline statistics; reference surfaces
- 20.6 Backscatter and multispectral MBES; seabed classification; water-column imaging (plumes, wrecks, gas seeps)
- 20.7 Platforms: ships, launches, USVs, AUVs (deep-water resolution via proximity), ROVs
- 20.8 Processing chain and deliverables: raw (.all/.kmall/.s7k/.xtf/GSF) → cleaned soundings → surfaces (BAG/S-102) → charts; Descriptive Reports
**Then & now.** da Vinci 1490 ⟨H⟩ → Titanic 1912 / Fessenden → echo sounder patent 1913 ⟨H⟩ → Simrad 1931, Atlas 1902 ⟨H⟩ → Hawley's Hydrographic Manual 1928 ⟨H⟩ → multibeam patent 1962, SeaBeam 1977, Hydrosweep 1989 ⟨H⟩ → MB-System 1993, pfmabe 1994, GSF 1998 ⟨H⟩ → CUBE 2003, BAG 2006 → HSSD 2000 ⟨H⟩ and annual updates → USV/AUV mapping 2020s.
**Math.** Sonar equation; Snell ray tracing through an SVP; footprint = 2d·tan(θ/2); TVU/THU; CUBE hypothesis weighting; patch-test geometry.
**Software.** Open: MB-System, Kluster (NOAA), HydrOffice Sound Speed Manager/QC Tools, Pydro (partly), GMT, pfmabe (legacy). Closed: Teledyne CARIS HIPS & SIPS/BASE Editor, QPS Qimera/Fledermaus/FMGT, HYPACK/HYSWEEP, EIVA NaviSuite, BeamworX, Teledyne PDS, Kongsberg SIS, Chesapeake SonarWiz, NaviModel.
**Standards & guides.** IHO S-44 Ed. 6; NOAA HSSD (annual) and FPM; USACE EM 1110-2-1003; IHO C-13; Multibeam Advisory Committee calibration guidance; GeoHab backscatter guidelines (Lurton & Lamarche 2015); IHO S-102/BAG specs.
**Key references.** Lurton 2010; Urick 1983; Medwin & Clay 1998; de Moustier 1988 *IHR*; Hughes Clarke, Mayer & Wells 1996 *MGR*; Hughes Clarke 2018 (*Submarine Geomorphology* chapter; *Geosciences* imaging-geometry paper); Godin 1998 (patch test); Hare, Godin & Mayer 1995; Hare 1995/2001 (error budgets); Calder & Mayer 2003 *G³* (CUBE); Calder & Rice 2017 (CHRT); Lurton & Augustin 2010 *IEEE JOE*; Beaudoin, Hughes Clarke & Bartlett 2004 (sound speed); Dinn, Loncarevic & Costello 1995; Colbo et al. 2014 (water column); Hansen 2011 and Hayes & Gough 2009 (SAS); Demer et al. 2015 ICES CRR 326 (calibration spheres); Caress & Chayes 1996 (MB-System); Hawley 1928 and Umbach 1976 *Hydrographic Manual* ⟨H⟩.
**Pitfalls.** Grid resolution finer than the depth-dependent footprint; sound-speed casts too infrequent in stratified water; mis-set waterline/draft as a constant vertical bias; squat ignored at survey speed; over-cleaning that removes real shoals; averaging surfaces used for charting; bubble sweep-down on the transducer.
**Key takeaways.** Sonar resolution degrades with depth by physics, so products are inherently variable-resolution; the vertical budget is dominated by water level, sound speed, and vessel geometry; navigation surfaces must be shoal-biased and must carry uncertainty.

### Chapter 21 — Radar, SAR, InSAR, radar altimetry, ice-penetrating radar
**Scope.** Microwave methods for elevation: imaging geometry, interferometry, altimetry, sub-ice beds.
**Sections.**
- 21.1 Radar basics and SAR imaging geometry: slant range, foreshortening, layover, shadow; speckle
- 21.2 InSAR DEM generation: baselines, phase unwrapping (Goldstein, MCF, SNAPHU), coherence and decorrelation, atmospheric phase screen; single-pass (SRTM, TanDEM-X bistatic) vs repeat-pass
- 21.3 Penetration and the measured surface: X/C/L/P band in vegetation, snow, ice, dry sand (TanDEM-X over ice sheets; Biomass P-band)
- 21.4 Differential InSAR and time series (PSI, SBAS): subsidence, earthquakes, volcanoes, slopes — bridge to Part VIII
- 21.5 Radargrammetry and SAR stereo; SAR offset tracking
- 21.6 SAR geocoding and radiometric terrain correction need a DEM (circularity and error inheritance)
- 21.7 Radar altimetry: TOPEX/Jason, CryoSat-2 SARIn, Sentinel-3/6, SWOT KaRIn; sea surface height → marine gravity → predicted bathymetry; ice sheets; inland water
- 21.8 Ice-penetrating and ground-penetrating radar: radio-echo sounding, Bedmap/BedMachine bed DEMs, snow depth, GPR for shallow subsurface
- 21.9 Ground-based radar interferometers for slopes and dams
- 21.10 Products and missions: SRTM (2000 ⟨H⟩), TanDEM-X DEM (12/30/90 m), Copernicus DEM, NISAR, Sentinel-1C/D
**Math.** Height of ambiguity h_amb = λ·R·sin θ / (2·B⊥) (×2 for bistatic convention); phase-to-height sensitivity; coherence; layover geometry.
**Software.** Open: ISCE2/3, GMTSAR, ESA SNAP, MintPy, LiCSBAS, StaMPS, PyRate, SNAPHU, HyP3 (ASF service). Closed: GAMMA, SARscape, SARPROZ.
**Standards & guides.** TanDEM-X DEM Product Specification; Copernicus DEM Product Handbook; SRTM User Guide; CEOS ARD for SAR (CARD4L).
**Key references.** Hanssen 2001 *Radar Interferometry*; Rosen et al. 2000 *Proc. IEEE*; Bamler & Hartl 1998; Massonnet & Feigl 1998 *Rev. Geophys.*; Zebker & Villasenor 1992; Ferretti, Prati & Rocca 2001 (PS); Berardino et al. 2002 (SBAS); Hooper et al. 2004 (StaMPS); Goldstein, Zebker & Werner 1988; Chen & Zebker 2001 (SNAPHU); Farr et al. 2007 *Rev. Geophys.* (SRTM); Rodríguez, Morris & Belz 2006 (SRTM assessment); Krieger et al. 2007; Rizzoli et al. 2017 and Wessel et al. 2018 (TanDEM-X DEM); Cumming & Wong 2005; Moreira et al. 2013 tutorial; Fu & Cazenave 2001; Sandwell et al. 2014 *Science*; Fu et al. 2024 (SWOT); Fretwell et al. 2013 (Bedmap2); Morlighem et al. 2017/2020 (BedMachine); Quegan et al. 2019 (Biomass).
**Pitfalls.** InSAR DEM heights over forest/snow interpreted as ground; layover/shadow voids filled silently; unwrapping errors as 2π jumps presented as terraces; tropospheric artefacts read as deformation; using a DEM for RTC that was itself made from the same SAR.
**Key takeaways.** Radar sees through clouds and some media but measures a wavelength-dependent surface; InSAR products need coherence, void, and height-error layers to be interpretable.

### Chapter 22 — Photogrammetry, stereo, and structure from motion
**Scope.** Image-based 3D from film cameras to drones and satellites, plus NeRF/3DGS as reconstruction (not metrology).
**Sections.**
- 22.1 Camera model and calibration: pinhole, Brown distortion, rolling shutter; interior/exterior orientation; collinearity
- 22.2 Classical aerial photogrammetry: stereo pairs, parallax, aerial triangulation, GSD, base-to-height; ASPRS lineage (1934 ⟨H⟩; photogrammetry's start 1776 ⟨H⟩)
- 22.3 Structure from motion: features (SIFT 2004), RANSAC (1981 ⟨H⟩), factorization (Tomasi & Kanade 1992 ⟨H⟩), incremental/global SfM, bundle adjustment, self-calibration and the doming problem
- 22.4 Dense matching: SGM, PatchMatch, MVS, deep stereo; DSM vs mesh vs point cloud outputs
- 22.5 Georeferencing: GCPs vs checkpoints (number, distribution, independence), RTK/PPK direct georeferencing, precision maps
- 22.6 Satellite stereo and tri-stereo: RPC models and bias compensation; ASTER, SPOT, ALOS PRISM, WorldView, Pléiades, Cartosat; pipelines (ASP ⟨H⟩ 1996, SETSM, s2p, CARS, MicMac); ArcticDEM/REMA/EarthDEM
- 22.7 Historical imagery: declassified Corona/Hexagon ⟨H⟩, archival aerial photographs, "structure from history"
- 22.8 Failure modes: water, snow, shadow, repetitive texture, moving objects, thin objects, occlusion; what an image DSM is (first visible surface)
- 22.9 Shape-from-shading and photoclinometry (planetary); shadow-length heights
- 22.10 NeRF and 3D Gaussian Splatting: strengths for visualization, caveats for measurement
**Math.** Collinearity equations; σ_Z ≈ (Z²/(f·B))·σ_px; bundle-adjustment normal equations; essential/fundamental matrices; SGM cost aggregation.
**Software.** Open: COLMAP, OpenMVG/OpenMVS, Meshroom (AliceVision), MicMac, OpenDroneMap/WebODM, Ames Stereo Pipeline, SETSM, s2p, CARS, OpenCV (2000 ⟨H⟩). Closed: Agisoft Metashape, Pix4D, RealityCapture, Bentley ContextCapture/iTwin, Trimble Inpho, SOCET GXP, DJI Terra, SimActive Correlator3D.
**Standards & guides.** ASPRS Ed. 2 (photogrammetry and UAS addenda); USGS/NGS camera calibration practices; EuroSDR/ISPRS benchmark protocols.
**Key references.** Hartley & Zisserman 2004 *Multiple View Geometry*; Szeliski 2022; Förstner & Wrobel 2016; Kraus 2007; McGlone (ed.) 2013 *Manual of Photogrammetry*; Luhmann et al. 2019; Triggs et al. 2000 (bundle adjustment); Lowe 2004; Fischler & Bolles 1981; Schönberger & Frahm 2016 (COLMAP); Hirschmüller 2008 (SGM); Westoby et al. 2012; James & Robson 2014 (doming); James et al. 2017 *Geomorphology* (GCP design); Eltner et al. 2016; Grodecki & Dial 2003 (RPC); Beyer et al. 2018 (ASP); Shean et al. 2016; Noh & Howat 2015 (SETSM); de Franchis et al. 2014 (s2p); Dehecq et al. 2020 (KH-9); Mildenhall et al. 2020 (NeRF); Kerbl et al. 2023 (3DGS).
**Pitfalls.** Doming from self-calibration with nadir-only, GCP-poor blocks; checkpoints that were also GCPs; DSM sold as DTM; smooth "water" surfaces that are matching noise; RPC products with meters of bias uncorrected; NeRF/3DGS outputs quoted with centimeter "accuracy."
**Key takeaways.** Image-based DEMs are only as good as the camera model, the network geometry, and the control; they measure the first visible surface, and they fail predictably on water, snow, and thin objects.

### Chapter 23 — Optical SDB, wave-kinematics bathymetry, altimetry-predicted bathymetry
**Scope.** Three distinct families often lumped together as "satellite bathymetry."
**Sections.**
- 23.1 Optical SDB physics: attenuation, Kd, bottom albedo, optically shallow water; empirical (Lyzenga, Stumpf band ratio), physics-based (radiative transfer), and ML approaches; multi-temporal compositing; sun glint, waves, turbidity, tide stage at acquisition (datum of the result!)
- 23.2 Calibration and validation of SDB: sonar, lidar, ICESat-2; typical uncertainty (≈ 10–20 % of depth); depth limits (~20–30 m)
- 23.3 Wave-kinematics bathymetry: linear dispersion relation; video (cBathy), Sentinel-2 band time lag, SAR, Pléiades video
- 23.4 Altimetry-predicted bathymetry: Smith & Sandwell inversion of marine gravity (gravity ↔ topography admittance), resolution ≈ 6–12 km, local errors of hundreds of meters, seamount detection; SRTM15+/GEBCO's type identifier (TID) grid
- 23.5 Products and providers: EOMAP, TCarta, Allen Coral Atlas, national SDB programs; GEBCO/SRTM15+/ETOPO
- 23.6 Fitness: reconnaissance and charting support vs safety-of-navigation (CATZOC implications)
**Math.** Stumpf ratio model z = m₁·ln(nπR(λ₁))/ln(nπR(λ₂)) − m₀; dispersion ω² = g·k·tanh(k·h); gravity–topography transfer function (Parker 1973).
**Software.** Open: Google Earth Engine scripts, ACOLITE (atmospheric correction), `sdb` notebooks, GMT `gravfft`. Closed: EOMAP, TCarta, ENVI.
**Standards & guides.** IHO B-13 Guidance on Satellite-Derived Bathymetry (verify current edition); IHO S-44 note on SDB; GEBCO Cook Book chapters.
**Key references.** Lyzenga 1978 *Appl. Opt.*; Stumpf, Holderied & Sinclair 2003 *L&O*; Lee et al. 1999; Dekker et al. 2011; Caballero & Stumpf 2019/2020; Hedley et al. 2018; Babbel, Parrish & Magruder 2021 *GRL*; Thomas et al. 2021; Sagawa et al. 2019; Ashphaq et al. 2021 review; Holman, Plant & Holland 2013 (cBathy); Bergsma, Almar & Maisongrande 2019; Almar et al. 2019; Smith & Sandwell 1994/1997 ⟨H⟩; Sandwell et al. 2014; Tozer et al. 2019; Parsons & Sclater 1977 ⟨H⟩ (depth–age prior); Marks & Smith 2006.
**Pitfalls.** SDB depth referenced to the water level at image time, not chart datum; extrapolating empirical models beyond calibration depths/bottom types; using altimetry-predicted bathymetry for anything local; treating ML-SDB confidence as accuracy.
**Key takeaways.** Three different physics, three different error structures; all three need in-situ calibration and all three should be flagged by source in any compilation.

### Chapter 24 — Gravity, magnetics, and other geophysics as mapping aids
**Scope.** Potential fields and other geophysics that constrain, correct, or extend elevation models.
**Sections.**
- 24.1 Gravity: geoid → orthometric heights; terrain corrections need DEMs (Hammer, Nagy prisms; the circularity); airborne gravity (GRAV-D) and satellite missions; gravity inversion for sub-ice bathymetry and seamounts; isostasy and flexure
- 24.2 Magnetics: declination for headings (WMM/IGRF); marine magnetic anomalies → seafloor age (Vine–Matthews–Morley 1963, Cande & Kent 1992 ⟨H⟩) → depth–age priors; magnetometer surveys for pipelines, UXO, wrecks; EMAG2
- 24.3 Seismics: refraction/reflection, sub-bottom horizons as buried "DEMs"; Moho topography (receiver functions)
- 24.4 Electrical, electromagnetic, GPR: depth to bedrock, water table, permafrost; "Earth layers as DEMs"
- 24.5 Fusing geophysics with topography: joint inversion, constraints in void filling (predicted bathymetry), plausibility checks
**Math.** Bouguer and terrain corrections; Parker's forward formula; admittance/coherence; Nagy prism formula.
**Software.** Open: GMT (`grdfft`, `gravfft`), Fatiando a Terra/Harmonica, pyshtools, Geosoft-free alternatives (Oasis montaj is closed), GeographicLib `MagneticField`. Closed: Seequent Oasis montaj, Petrel, Kingdom.
**Key references.** Watts 2001 *Isostasy and Flexure of the Lithosphere*; Parker 1973 *GJRAS*; Nagy 1966; Hammer 1939; Forsberg 1984 (RTM); Hirt et al. 2013 (GGMplus); Müller et al. 2008/2019 (seafloor age grids); Meyer et al. 2017 (EMAG2v3); Alken et al. 2021 (IGRF-13); Morlighem et al. 2017/2020.
**Pitfalls.** Using a DEM to correct gravity and the resulting geoid to correct the same DEM without tracking the loop; assuming seafloor age–depth relations hold near hotspots and margins; magnetic declination from the wrong epoch.
**Key takeaways.** Gravity ties elevation to physics (the geoid) and fills where sensors cannot see; magnetics and seismics add priors and context but never replace direct measurement.

### Chapter 25 — Calibration: targets, stations, networks, benchmarks, reference surfaces
**Scope.** Active and passive infrastructure that makes measurements traceable and comparable.
**Sections.**
- 25.1 Definitions: calibration vs validation vs verification; traceability to SI (metre via c, second via Cs); calibration certificates and intervals
- 25.2 Active stations: CORS/IGS, GNSS at tide gauges (SONEL/GLOSS), tide gauges (NWLON), NTRIP casters; VLBI/SLR/DORIS core sites (GGOS)
- 25.3 Passive marks: benchmarks and levelling networks (NSRS; "Buttermilk" 1833 ⟨H⟩; NGS datasheets), horizontal marks, tidal benchmarks, OPUS-Share
- 25.4 Calibration ranges and targets: USGS/CEOS test-site catalog (2007 ⟨H⟩), Siemens stars and spoke targets (1930s; Google roof 2010 ⟨H⟩), QR-code roofs (NPS 2015 ⟨H⟩), aerial camera ranges (Sioux Falls), lidar boresight sites, Sjökulla/Vaihingen permanent test fields, corner reflectors for SAR (Surat Basin array), radiometric sites (Railroad Valley), altimeter cal/val (Harvest, Corsica, Bass Strait, Salar de Uyuni, Lake Issykkul)
- 25.5 Hydrographic calibration: patch test, bar check (SBES), lead-line check, calibration spheres (fisheries), MBES reference surfaces and calibration areas, sound-speed sensor checks, waterline/draft/squat trials
- 25.6 Sensor-level calibration: GNSS antenna (ANTEX), IMU (Allan variance, six-position), camera (checkerboards, Zhang 2000, self-calibration), laser scanner (range/intensity), TLS targets
- 25.7 Global quasi-truth: ICESat-2 and GEDI as checkpoints for DEMs; "stable terrain" co-registration (Nuth & Kääb); Geoid Slope Validation Surveys
- 25.8 Redundancy as self-calibration: loop closures, crosslines, strip overlap, tie points
- 25.9 Designing and maintaining a calibration program; documentation and recalibration triggers
**Software.** NGS tools (OPUS, datasheets), Kalibr, OpenCV calibration, TerraMatch (closed), CARIS/Qimera patch-test tools (closed), MB-System `mbeditviz` offsets, SlideRule/icepyx.
**Standards & guides.** ISO/IEC 17025 (lab competence); NGS geodetic control standards; FGDC-STD-007.2 (geodetic networks); IHO S-44; NOAA FPM (system calibrations); Multibeam Advisory Committee procedures; CEOS WGCV.
**Key references.** Godin 1998; Hughes Clarke 2003; Demer et al. 2015; Smith et al. 2013 (GSVS); Zhang 2000 (camera calibration); Skaloud & Lichti 2006; Nuth & Kääb 2011; Snay & Soler 2008 (CORS); IOC Manuals 14 (tide gauges); Honkavaara et al. 2008 (permanent test fields).
**Pitfalls.** Calibration done once and never re-verified after a sensor swap; patch tests on flat, featureless seabed (unobservable yaw/latency); checkpoints surveyed to a different datum than the product; targets whose own coordinates are undocumented.
**Key takeaways.** Calibration infrastructure is what makes a measurement a measurement; plan calibration observations into every survey and publish them with the data.

## Part VI — Planning and operating surveys

### Chapter 26 — Survey planning for calibration, error reduction, and error monitoring
**Scope.** Design surveys so that errors are small, observable, and provable.
**Sections.**
- 26.1 From requirement to specification: choosing the governing standard (HSSD/S-44, LBS, ASPRS, ICAO, client spec); deliverables and acceptance tests up front
- 26.2 Geometry: line spacing vs swath/footprint, overlap and sidelap (lidar 20–30 %; SfM 80/70), crosslines (≈ 5–10 % of line km), flying height vs density, sun angle and shadow, tide windows, bathy coverage vs object detection
- 26.3 Control design: base-station siting and baseline limits, GCP/checkpoint count and distribution (≥ 30 per land-cover class; independence), benchmarks and tide gauges, calibration lines and patch tests per mobilization, reference surfaces
- 26.4 Environmental windows: leaf-off, snow-free, low turbidity, calm sea state, PDOP, ionospheric activity, weather; seasonality (Ch. 36)
- 26.5 Operational QC: daily checks (overlap residuals, crossline differences, sound-speed stability, trajectory metrics), field logs, re-flight/re-run triggers
- 26.6 Design for validation: reserve independent checks before collecting; plan what you will later remove (water surface, vessel draft, canopy)
- 26.7 Surveying to the ellipsoid and reducing later (ERS) as a planning decision
- 26.8 Permits and constraints: airspace (Part 107, NOTAMs), marine scientific research consent in foreign EEZs, protected areas, privacy
- 26.9 Risk and cost planning: mobilization dominates; weather contingency; re-survey economics
- 26.10 Documentation that starts before the first line: project instructions, metadata skeleton, naming conventions
**Standards & guides.** NOAA HSSD and FPM (project instructions, Descriptive Report); USGS LBS (swath overlap, voids, density, accuracy); ASPRS Ed. 2 Addendum II (control surveys); IHO S-44; USACE EM 1110-2-1003 and EM 1110-1-1000; ICSM lidar tender template.
**Key references.** James et al. 2017 (GCP design); Hodgson & Bresnahan 2004 (error budget planning); Hughes Clarke 2018 (imaging geometry); NOAA FPM; Maune & Nayegandhi 2018 (project planning chapters).
**Pitfalls.** No crosslines ("we had no time"); checkpoints clustered near the office; base station on an unknown mark; patch test skipped after a transducer change; survey season chosen by budget year rather than leaf-off/low-flow.
**Key takeaways.** Observability of error is designed in, not discovered later; redundancy (overlap, crosslines, control) is the cheapest insurance in the whole lifecycle.

### Chapter 27 — Moving and transient objects during collection
**Scope.** Things that are not terrain but get measured: vehicles, vessels, people, animals, cranes, construction, demolition, debris, fire, smoke, steam, spray — and how AIS/ADS-B can help.
**Sections.**
- 27.1 Taxonomy by time scale: seconds (vehicles, waves, birds), hours (parked cars, moored ships, cranes), days–months (construction, demolition, stockpiles, dumps and trash piles, fire scars), with the 2.5D consequence (a car is a 1.5 m "hill")
- 27.2 Detection and removal: classification (LAS low/high noise, unclassified), multi-pass/median temporal filtering, dynamic masks in SfM, motion cues in lidar (scan-line discontinuities), ML object detection
- 27.3 Ships and aircraft as artefacts: hulls in MBES/lidar (false shoals, shadows), aircraft in satellite stereo; using AIS (ITU-R M.1371 1998; mandate 2002 ⟨H⟩; libais 2010 ⟨H⟩) and ADS-B (OpenSky) as spatio-temporal masks and priors — feasibility, timing/position accuracy, antenna offsets, non-broadcasting targets, latency, spoofing; verdict: useful for masking and QC, not sufficient alone
- 27.4 Fires, smoke, steam, dust, spray, fog: obscuration and false returns in lidar/photogrammetry; industrial plumes and cooling towers; thermal refraction; radar immunity
- 27.5 Construction and destruction: cranes (move between passes), scaffolding, excavations, demolition, war damage; dating the surface
- 27.6 Dumps, landfills, stockpiles, snow piles: legitimately changing surfaces — decide whether they are "terrain" for your product
- 27.7 Water surface motion: waves, wakes, boat traffic in bathy lidar; ice
- 27.8 Documenting what was removed (masks as deliverables)
**Software.** PDAL filters (noise, temporal), CloudCompare, lidR, Metashape/Pix4D masking, OpenSky/ADS-B Exchange APIs, AIS decoders (libais, pyais), Global Fishing Watch data ⟨H⟩.
**Key references.** Schwehr & McGillivary 2007 (AIS applications); Schäfer et al. 2014 (OpenSky); Kroodsma et al. 2018 *Science* (GFW); USGS LBS noise classes; Matikainen et al. 2016 (corridor objects); Pelich et al. 2019 (SAR ship–AIS matching).
**Pitfalls.** Moored hulls charted as shoals or leaving unflagged gaps; cars baked into "bare-earth" DTMs in parking lots; steam plumes creating floating points that survive filtering; AIS positions trusted to the second when reports arrive every 2–10 s with antenna offsets of tens of meters.
**Key takeaways.** Transient objects are a classification problem with a time dimension; external tracking data (AIS/ADS-B) make good masks and QC evidence; always deliver the masks.

### Chapter 28 — Reducing cost across collection, processing, validation, and use
**Scope.** Economics of elevation data and where savings are real versus false.
**Sections.**
- 28.1 Cost structure: mobilization, platform hours, personnel, processing labor (manual editing dominates hydrography), validation surveys, storage/egress, licensing
- 28.2 Collection: right-sizing resolution to requirement; multi-sensor single missions; shared/pooled acquisitions (3DEP partnerships); satellite vs airborne vs ground break-evens; opportunistic data (fleets, phones, CSB); open data reuse
- 28.3 Processing: automation (CUBE/CHRT, ML classification), cloud-native formats (COG/COPC/Zarr), reproducible pipelines, open-source tooling vs seat licenses, GPU costs
- 28.4 Validation: reuse national control, ICESat-2/GEDI as free checkpoints, stable-terrain methods, crosslines designed in, shared benchmark datasets
- 28.5 Use: overviews, tiling, caching, APIs, "good-enough" derived products; avoiding re-processing by publishing intermediate products and metadata
- 28.6 The cost of errors: groundings, flood-map lawsuits, failed acceptance, re-surveys; benefit–cost evidence (NEEA ~4–5:1; 3D Nation)
- 28.7 Data lifetimes, refresh cycles, and when not to re-survey (change detection triggers)
- 28.8 Energy and environmental cost of surveys and compute
**Key references.** Dewberry 2012 (NEEA); Dewberry 2022 (3D Nation); Sugarbaker et al. 2014; Mayer et al. 2018 (Seabed 2030 economics); IHO B-12.
**Pitfalls.** Saving on control and crosslines (the costs reappear in validation and liability); "free" global DEMs with hidden fitness costs; lossy compression of elevation to save bytes; license terms that forbid the intended derivative.
**Key takeaways.** Collect once at the right specification and publish well; the cheapest validation is the one designed into acquisition; errors are the most expensive line item.

## Part VII — From sensor data to products

### Chapter 29 — Processing pipelines: levels, lineage, and what gets lost
**Scope.** The generic chain from raw observations to products, per sensor, with provenance.
**Sections.**
- 29.1 Processing levels (NASA L0–L4 analogy): raw → trajectory → georeferenced observations → cleaned → classified → surface → derived product → QA → metadata → archive
- 29.2 Sensor-specific pipelines: lidar (trajectory, calibration, strip adjustment, classification, DTM/DSM), MBES (SVP, motion, tides/ERS, cleaning, CUBE, BAG), SfM (alignment, BA, dense cloud, mesh, DSM, ortho), InSAR (coregistration, interferogram, unwrapping, geocoding), SDB, satellite stereo
- 29.3 Information lost at each step (full waveform → discrete returns → classified points → grid → overview); when to keep intermediates
- 29.4 Reproducibility: software versions, parameters, containers, random seeds; lineage records (ISO 19115 LI_Lineage, W3C PROV)
- 29.5 Human-in-the-loop steps: manual editing, subjectivity, inter-operator variability studies
- 29.6 Automation and QA gates; regression tests on reference datasets
- 29.7 Cloud-native and distributed processing (Earth Engine ⟨H⟩, Dask, Pangeo, PDAL pipelines, Spark/Sedona)
**Software.** PDAL pipelines, MB-System scripts, Kluster, OpenDroneMap, ASP, ISCE; closed suites (CARIS, Qimera, TerraSolid, Metashape, POSPac).
**Standards & guides.** ISO 19115 lineage; W3C PROV; FAIR principles; NOAA HSSD processing deliverables; USGS LBS deliverables.
**Key references.** Wilkinson et al. 2016 (FAIR); Butler et al. 2021 (PDAL); Gorelick et al. 2017 (Earth Engine) ⟨H⟩; Calder & Mayer 2003; NOAA FPM processing chapter.
**Pitfalls.** Overwriting raw data with "corrected" data; parameter defaults silently different between software versions; lineage recorded as a PDF nobody can parse; publishing only the final grid.
**Key takeaways.** Keep raw, record every step machine-readably, and expose intermediate products — reprocessing is the normal lifecycle of elevation data.

### Chapter 30 — Point-cloud cleaning, classification, and ground extraction
**Scope.** Turning observations into labeled points; the ground as a decision.
**Sections.**
- 30.1 Outlier and noise handling: statistical/radius filters, low/high noise classes, isolated points, multiple-time-around returns, sonar "fliers" and blunders
- 30.2 Classification schemes: ASPRS LAS classes (ground, vegetation tiers, building, water, rail, road, bridge deck, wire classes, noise), hydrographic rejected/accepted soundings, flags (withheld, synthetic, key-point, overlap)
- 30.3 Ground filtering algorithms: slope-based (Vosselman), morphological (PMF), progressive TIN (Axelsson/TerraScan), robust interpolation (Kraus & Pfeifer), MCC, SMRF, cloth simulation (CSF), deep learning (KPConv/RandLA-Net, OpenGF)
- 30.4 Parameter sensitivity by terrain type (steep, urban, forest, dunes, levees) and point density; Type I/II error trade-off
- 30.5 Evaluation: ISPRS filter test (Sithole & Vosselman), OpenGF, DALES/Vaihingen/Hessigheim; per-class accuracy; manual QA sampling
- 30.6 Hydrographic analog: CUBE/CHRT hypothesis selection, operator review, "do not over-clean a shoal"
- 30.7 Cost and consistency of manual editing; audit trails
- 30.8 Deliverable semantics: what "ground" includes in this project (ties to Ch. 32)
**Math.** Morphological opening/closing; progressive TIN densification criteria; CSF physics model; confusion-matrix metrics.
**Software.** Open: PDAL (`filters.pmf`, `filters.smrf`, `filters.csf`, `filters.outlier`), CloudCompare (CSF), lidR, Open3D-ML, MB-System, Kluster. Closed: TerraScan, LAStools (`lasground`), Global Mapper, CARIS/Qimera cleaning tools.
**Key references.** Sithole & Vosselman 2004 *ISPRS J.*; Axelsson 2000; Kraus & Pfeifer 1998; Vosselman 2000; Zhang et al. 2003 (PMF); Evans & Hudak 2007 (MCC); Pingel, Clarke & McBride 2013 (SMRF); Zhang et al. 2016 (CSF); Meng, Currit & Zhao 2010 review; Qin et al. 2021 (OpenGF); Thomas et al. 2019 (KPConv); Hu et al. 2020 (RandLA-Net); Calder & Mayer 2003; Calder & Rice 2017.
**Pitfalls.** One parameter set for a whole county; filters that shave levees and berms or keep low vegetation as ground; cleaning that deletes real seafloor features; class codes reused with vendor-specific meanings.
**Key takeaways.** Ground is a classification decision with documented rules; validate per land-cover and terrain class; never discard rejected points — flag them.

### Chapter 31 — Interpolation, gridding, and grid registration
**Scope.** From points to surfaces, and the semantics of a cell value.
**Sections.**
- 31.1 Methods: nearest, IDW, natural neighbour, TIN-linear, splines (TPS, regularized), kriging (ordinary/universal; variogram; kriging variance), ANUDEM/Topo-to-Raster (drainage enforcement), binning (mean/min/max/median), CUBE node estimation, moving least squares, Poisson reconstruction
- 31.2 Choosing by data density and purpose: shoal-biased (min) for navigation, mean for science, max for obstacles; what a cell value represents (sample at center? mean over area?) — the undocumented choice that breaks comparisons
- 31.3 Grid registration: pixel-is-area vs pixel-is-point, half-cell shifts, GMT gridline vs pixel registration, SRTM edge-overlap tiles
- 31.4 Breaklines (hard/soft), hydro-flattening inputs, anisotropy
- 31.5 Interpolation across voids and edge effects (ties to Ch. 35); flagging interpolated cells
- 31.6 Cell size relative to point spacing (Nyquist; Hengl 2006); oversampling consequences (smoothness not detail)
- 31.7 Overviews/pyramids and level-of-detail: aggregation choice (average vs nearest vs min/max) and how overviews can lie
- 31.8 Interpolation uncertainty: kriging variance, cross-validation, bootstrap, distance-to-nearest-observation layers
**Math.** IDW weights; TPS energy; variogram models and ordinary kriging system; natural-neighbour Sibson weights; Delaunay criterion.
**Software.** Open: GDAL (`gdal_grid`, `gdal_fillnodata`, `gdaladdo`), GMT (`surface`, `nearneighbor`, `blockmedian`, `grdblend`), PDAL writers.gdal, GRASS (`v.surf.rst`, `r.surf.idw`), SAGA, scikit-gstat/gstools, PyKrige, MB-System `mbgrid`. Closed: ArcGIS (Topo to Raster, Geostatistical Analyst), Surfer, CARIS/Qimera surfaces, Global Mapper.
**Key references.** Hutchinson 1989 *J. Hydrol.* (ANUDEM); Mitas & Mitasova 1999; Sibson 1981; Shepard 1968; Cressie 1993; Chilès & Delfiner 2012; Hengl 2006; Calder & Mayer 2003; Jakobsson, Calder & Mayer 2002 *JGR* (random errors in gridded bathymetry); Amante & Eakins 2016 (interpolated bathymetry accuracy); Peucker et al. 1978 (TIN) ⟨H⟩; Delaunay 1934.
**Pitfalls.** Cubic/spline overshoot in steep terrain; min-binning used for a hydrologic DEM (creates artificial pits) or mean-binning used for a chart; unknown registration → half-cell horizontal offsets that look like vertical error on slopes; overviews computed with "average" hiding peaks a navigator needs.
**Key takeaways.** The interpolator and the cell semantics are part of the product definition; store them in metadata and provide an interpolation/distance mask.

### Chapter 32 — DSM → DTM: removing objects, and the definitions problem
**Scope.** What counts as terrain, how objects are removed, and what is unknowable afterwards.
**Sections.**
- 32.1 Definitions that bite: building (sheds, carports, greenhouses, tents, stadium roofs, ruins, under construction), road (surface vs corridor), bridge vs culvert vs causeway, dam, pier/dock, retaining wall, tank, elevated pipeline, conveyor, aqueduct, solar array, antenna/mast, wind turbine, vehicles, vegetation and crops, stockpiles and landfills, snow and ice
- 32.2 Specification examples: USGS LBS bare-earth rules (bridges removed, dams kept, buildings/tanks removed, culverts not cut unless hydro-enforced), Copernicus DEM editing (EDM/FLM/HEM/WBM layers), national lidar DTM specs, CityGML LoD semantics; "DTM" products that are modeled, not measured (FABDEM, MERIT, DeltaDTM)
- 32.3 Roads crossing roads and roads under buildings: the single-valued 2.5D limit; what the DTM shows under overpasses, arcades, tunnels; multi-layer and true-3D alternatives (voxels, meshes, CityGML)
- 32.4 Removal methods: classification then interpolation under footprints (what was under the building is unknowable → interpolated mask), morphological approaches, ML DSM→DTM
- 32.5 Errors and unknowns after removal: interpolation bias under large footprints, retained basements/foundations, smoothing of terraces, false ground under dense canopy; how to express it in an uncertainty layer
- 32.6 Vegetation and "ground": tall grass, crops, marsh platform bias (10–50 cm), forest floor under closed canopy, hedges; correction models (LEAN)
- 32.7 What each public dataset includes or excludes (SRTM, ASTER, AW3D, TanDEM-X, Copernicus, NASADEM, MERIT, FABDEM, national lidar DTMs, GEDI/ICESat-2) — a comparison table with "surface definition" column
- 32.8 nDSM = DSM − DTM and the propagation of both definitions into building/canopy heights
**Math.** nDSM; morphological operators; interpolation bias estimates; error propagation for differences.
**Software.** PDAL/lidR/CloudCompare (classification), WhiteboxTools (`RemoveOffTerrainObjects`), SAGA, GRASS, 3dfier; closed: TerraScan, Global Mapper, ArcGIS.
**Standards & guides.** USGS LBS (definitions and bare-earth rules); Copernicus DEM Product Handbook (mask layers); CityGML 3.0; INSPIRE Elevation specification; ASPRS LAS classes.
**Key references.** Guth et al. 2021; Hawker et al. 2022 (FABDEM); Yamazaki et al. 2017 (MERIT); Pronk et al. 2024 (DeltaDTM); Gevaert et al. 2018 (DL DTM extraction); Hladik & Alber 2012; Buffington et al. 2016 (LEAN); Rogers et al. 2018; Medeiros et al. 2015; Biljecki, Ledoux & Stoter 2016 (LoD specification); Weidner & Förstner 1995 (nDSM).
**Pitfalls.** Calling a modeled bare earth "DTM" without a model-uncertainty layer; bridges removed in the DTM but present in the DSM used for the same flood model; landfill or stockpile treated as noise; marsh "ground" biased by vegetation and then used for SLR exposure.
**Key takeaways.** A DTM is a DSM plus a set of decisions; publish the decisions, the masks, and the interpolation footprint; 2.5D cannot represent stacked infrastructure — know when you need 3D.

### Chapter 33 — Wires, power lines, antennas, and other thin or moving structures
**Scope.** Objects that are small in cross-section, important for safety, and never still.
**Sections.**
- 33.1 Why they are missed: cross-section vs footprint and point density, specularity, photogrammetric non-reconstruction, radar cross-section
- 33.2 Detection and modeling: Hough/RANSAC line extraction, PCA linearity, catenary fitting, LAS wire classes (13–16), tower detection; corridor mapping programs
- 33.3 Motion and time scales: catenary sag with conductor temperature (IEEE 738; decimeters to meters), wind sway and galloping (seconds), ice loading, creep (years); implications for clearance surveys and for comparing epochs
- 33.4 Antennas, masts, guyed towers, cranes, wind turbines (blades), cable cars, ski lifts, fences, railings: obstacle databases (FAA DOF/AGIS, ICAO eTOD, NGA DVOF) vs DSM products
- 33.5 Should a DSM include wires? Decision by use (aviation obstacles yes; hydrology no; urban wind yes); separate obstacle layers
- 33.6 Wires as artefacts: false ground, floating points, SfM ghosts
- 33.7 Vegetation encroachment and clearance analysis (NERC FAC-003; PLS-CADD)
**Math.** Catenary y = a·cosh(x/a); sag ≈ wL²/(8T); thermal elongation ΔL = αLΔT; wind-induced displacement order-of-magnitude.
**Software.** Open: PDAL/CloudCompare/lidR custom pipelines, Open3D; Closed: PLS-CADD, TerraScan powerline tools, Global Mapper, LP360.
**Standards & guides.** FAA AC 150/5300-18; ICAO Annex 15 and PANS-AIM; RTCA DO-276/EUROCAE ED-98; IEEE 738; NERC FAC-003; ASPRS LAS 1.4 (wire classes).
**Key references.** McLaughlin 2006 *IEEE GRSL*; Jwa & Sohn 2012 *PE&RS* (catenary growing); Matikainen et al. 2016 *ISPRS J.* review; Guo et al. 2016; IEEE 738-2012.
**Pitfalls.** A clearance survey flown on a cold day used to judge summer sag; antennas absent from a DSM used for obstacle analysis; wires removed as noise in a lidar dataset later used for drone route planning.
**Key takeaways.** Thin structures need their own layer, their own acquisition parameters, and a time stamp with ambient conditions; their absence from a DSM is not evidence of absence.

### Chapter 34 — Water in DEMs: surfaces, shorelines, and hydro-conditioning
**Scope.** Representing water in a terrain model and the definition of a shoreline.
**Sections.**
- 34.1 Water in topographic lidar: absorption and specular loss, voids, low returns; hydro-flattening (flat lakes, monotonic rivers via breaklines), USGS definitions of hydro-flattening vs hydro-enforcement vs hydro-conditioning
- 34.2 Variable water: reservoir drawdown, ephemeral streams, tidal flats (survey at low tide), braided and migrating rivers, floods at acquisition; the water surface as "ground" of the day; JRC Global Surface Water for deciding what is water
- 34.3 What is a shoreline? Instantaneous waterline, wet/dry line, vegetation line, tide-coordinated lines (MHW, MLLW, LAT), legal definitions (Borax 1935; UNCLOS Art. 5 normal baseline on charts), NOAA shoreline practice (Shalowitz; CUSP), tide-coordinated extraction from DEM + VDatum, imagery-derived (NDWI) vs DEM-derived, slope amplification Δx = Δz/tan β, the coastline paradox (Mandelbrot 1967)
- 34.4 Shorelines move: erosion/accretion, seasonal profiles, storms, SLR and datum-epoch updates (the shoreline moves with no sand moving), subsidence
- 34.5 Rivers: water-surface slope, bathymetry gap in flood models, burned-in channels, thalweg as boundary, ice-covered rivers
- 34.6 Lakes and reservoirs: level datums (IGLD 85), capacity curves, seasonal variability; wetlands and marsh platforms
- 34.7 Hydro-conditioning for flow routing: fill vs breach (Priority-Flood; Lindsay), culverts and bridges as hydrologic connections, D8/D∞, HAND; artefact depressions vs real sinks (karst, prairie potholes)
- 34.8 Topobathy stitching and the white ribbon (ties to Ch. 19, 48)
**Math.** Δx = Δz / tan β; D8/D∞ flow direction; priority-flood complexity; fractal length scaling.
**Software.** Open: WhiteboxTools, TauDEM, RichDEM, GRASS `r.watershed`/`r.fill.dir`, SAGA, pysheds, GDAL, Google Earth Engine (GSW); Closed: ArcGIS Hydrology/Arc Hydro, Global Mapper.
**Standards & guides.** USGS LBS hydro-flattening requirements; NOAA shoreline standards; FEMA Guidelines and Standards (hydraulic DEMs); IHO S-57/S-101 coastline features; UNCLOS Art. 5/7/13.
**Key references.** Shalowitz 1962/1964; Graham, Sault & Bailey 2003; Boak & Turner 2005; Li, Ma & Di 2002 (tide-coordinated shoreline); Gesch 2009/2018; Mandelbrot 1967; Pekel et al. 2016 *Nature*; Poppenga et al. 2010 USGS SIR; Lindsay 2016 *Hydrol. Process.*; Barnes, Lehman & Mulla 2014; Jenson & Domingue 1988; O'Callaghan & Mark 1984; Tarboton 1997; Nobre et al. 2011 (HAND); Eakins & Grothe 2014.
**Pitfalls.** Flattening a river to a horizontal plane; filling sinks that are real; "shoreline" extracted from a DSM with riparian trees; treating a reservoir at drawdown as the terrain; comparing shorelines from different tidal epochs as change.
**Key takeaways.** Water is a surface with its own datum and date; the shoreline is a legal and tidal construct, not a visible line; hydro-conditioning changes elevations — keep the unconditioned DEM too.

### Chapter 35 — Voids, occlusion, shadows, overhangs, and multi-valued surfaces
**Scope.** Where the data are not, why, and what to do about it.
**Sections.**
- 35.1 Void sources per sensor: lidar shadows behind buildings/cliffs, water absorption, dropouts; SAR layover/shadow and decorrelation; optical clouds/shadow/matching failure; MBES nadir gaps, outer-beam rejection, acoustic shadows behind wrecks; bathy lidar turbidity and surf zone
- 35.2 Overhangs and multi-valued surfaces: cliffs, caves, bridges, piers, tree canopy, balconies — 2.5D collapse rules (highest? lowest? last return?) and 3D alternatives
- 35.3 Void filling: interpolation (Ch. 31), delta surface fill, auxiliary DEM fill (SRTM v3, Copernicus FLM), ML inpainting; always flag filled cells
- 35.4 Voids as information (water, ice, moving objects) vs voids as failure
- 35.5 Completeness metrics (ISO 19157), void statistics in specs (LBS), feature-detection coverage (S-44)
- 35.6 Overlap handling: strip/swath overlap, duplicate points, crossline soundings, keeping overlap for QC vs thinning for products
**Key references.** Reuter, Nelson & Jarvis 2007 (void filling); Grohman, Kroenung & Strebeck 2006 (delta surface fill); Dowding, Kuuskivi & Li 2004; Farr et al. 2007; Copernicus DEM Product Handbook; USGS LBS.
**Pitfalls.** Filled voids indistinguishable from measured cells; collapsing a bridge deck onto the river; cloud-filled DSM patches from a different year; "100 % coverage" claims that exclude the surf zone.
**Key takeaways.** Every DEM needs a source/void/fill mask; multi-valued geometry cannot be stored in a grid — decide and document the collapse rule.

### Chapter 36 — Seasonal and environmental variability
**Scope.** The surface measured depends on the season and the weather of the day.
**Sections.**
- 36.1 Vegetation: leaf-on/leaf-off penetration, crop growth and harvest, tillage microtopography (10–30 cm), grass and marsh height, forest regrowth and clear-cuts
- 36.2 Snow and ice: snow surface vs ground (winter lidar = snow DEM; the basis of ASO snow depth), glaciers, river/lake ice, frost heave, permafrost thaw subsidence, sea ice is not terrain
- 36.3 Water: groundwater and soil moisture (seasonal subsidence/uplift, swelling clays), reservoirs and rivers (Ch. 34), tides and surge at acquisition, Earth tides and loading (cm)
- 36.4 Atmosphere: refraction (laser/EDM/levelling), tropospheric delay (GNSS/InSAR), fog/cloud/dust/smoke, industrial steam (Ch. 27)
- 36.5 Aeolian and volcanic deposition; dune migration; ash
- 36.6 Scheduling and metadata: acquisition windows, per-pixel dates in mosaics (SRTM Feb 2000; Copernicus 2011–2015), seasonal confounds in change detection
**Key references.** Painter et al. 2016 (ASO); Nuth & Kääb 2011; Hugonnet et al. 2021; USGS LBS leaf-off guidance; IERS Conventions (tides, loading); Petit & Luzum 2010.
**Pitfalls.** Comparing a leaf-on DSM to a leaf-off DTM and reporting "growth"; using a snow-season DEM as terrain; ignoring Earth tides in cm-level GNSS control; a mosaic with hidden multi-year dates.
**Key takeaways.** Elevation has a season; record and publish acquisition conditions; design change studies to compare like with like.

## Part VIII — The dynamic Earth

### Chapter 37 — Time scales of surface change
**Scope.** A unifying frame for every "the ground moved" problem: what changes, how fast, how far, and whether a survey can see it.
**Sections.**
- 37.1 A log–log map of change: amplitude (mm → km) vs period (seconds → Myr) for tides, loading, wires, vehicles, crops, snow, subsidence, landslides, earthquakes, volcanism, plate motion, erosion, sea-level rise
- 37.2 Reversible vs irreversible, periodic vs secular vs episodic; what a single-epoch DEM freezes
- 37.3 Epochs, reference epochs, and the difference between "when measured" and "when valid for"
- 37.4 Matching survey cadence to process rate: Nyquist in time; aliasing seasonal signals into trends
- 37.5 Kinematic datums and time-dependent coordinates (preview of Ch. 38)
- 37.6 Expressing time in metadata: acquisition start/end, per-pixel date rasters, reference epoch of coordinates, tidal epoch (NTDE)
- 37.7 Decision rule: when is a DEM "out of date" for a given use?
**Then & now.** Static maps assumed a static Earth; GNSS made plate motion a routine datum problem (NAD83 vs ITRF drift of ~1–2 cm/yr); repeat lidar and InSAR made change the product, not the nuisance.
**Math.** Signal-in-time sampling: f_s ≥ 2·f_max; detectability when change Δz ≪ σ per epoch (averaging N epochs reduces random error ∝ 1/√N but not systematic bias); regression of elevation vs time with correlated errors.
**Software.** Open: xdem, py4dgeo, GMT, pyproj (time-dependent transforms); Closed: Trimble HTDP-based tools, Esri change tools.
**Standards & guides.** ISO 19111 (dynamic CRS, 2019); IERS Conventions 2010; NOAA tidal datum epoch policy.
**Key references.** Petit & Luzum 2010 (IERS 2010); Altamimi et al. 2016 *JGR* (ITRF2014); Eitel et al. 2016 *RSE* (lidar for ecosystem change, time-scale framing); Anders et al. 2020 *ISPRS J.* (4D point clouds); Gesch 2018 (DEM currency for coastal use).
**Pitfalls.** Treating a 1979 benchmark elevation as current in a subsiding delta; comparing DEMs across a tidal-epoch change; trend analysis on two epochs; mixing coordinates referenced to different epochs within one survey.
**Key takeaways.** Every elevation has a time; every datum has an epoch; choose survey cadence from the process you need to see, not from budget cycles alone.

### Chapter 38 — Plate motion, reference-frame dynamics, and vertical land motion
**Scope.** Slow, steady, large-scale motion that makes coordinates functions of time.
**Sections.**
- 38.1 Plate tectonics as a coordinate problem: ITRF velocities, plate motion models (NNR-MORVEL56, ITRF2014/2020 plate models), Euler poles
- 38.2 Plate-fixed datums (NAD83, ETRS89, GDA2020, NZGD2000) vs global dynamic frames (ITRF, WGS 84 realizations); the 1.8 m GDA94→GDA2020 shift; the ETRS89 ~2.5 cm/yr drift from ITRF
- 38.3 Deformation models and time-dependent transforms: HTDP, NZGD2000 deformation model, Japan's semi-dynamic correction, Australia's ATRF, NGS IFVM for NSRS modernization; PROJ deformation-model grids (GGXF)
- 38.4 Vertical land motion: glacial isostatic adjustment (ICE-6G, Peltier), tectonic uplift, groundwater/oil/gas extraction subsidence (Jakarta, Mexico City, Central Valley, Houston–Galveston, Tokyo, Bangkok), sediment compaction (deltas, New Orleans), permafrost thaw, mining subsidence
- 38.5 Measuring VLM: CORS/GNSS time series, InSAR (Sentinel-1, NISAR), repeat levelling, tide gauge–altimetry differences, absolute gravity
- 38.6 Consequences for DEMs: relative vs absolute sea-level rise, benchmark decay, control that moved between campaigns, "stable" ground that isn't
- 38.7 Katrina lesson: subsided benchmarks and levee heights (Dixon et al. 2006); re-levelling and vertical control programs
**Then & now.** Fixed terrestrial datums (NAD27 ⟨H⟩, ED50) → satellite global frames (WGS 84 1984 ⟨H⟩, ITRF series) → plate-fixed plus deformation models → fully kinematic NSRS modernization (NATRF2022 family).
**Math.** Rigid-plate velocity v = ω × r; Helmert 14-parameter (7 + rates) transformation; propagating position to epoch t: x(t) = x(t₀) + v·(t − t₀) + Σ episodic displacements; interpolating velocity grids.
**Software.** Open: PROJ (deformation models, point-motion operations), HTDP (NGS), GMT, MIDAS/Hector (GNSS time series), MintPy/ISCE2/LiCSBAS (InSAR time series); Closed: Trimble/Leica office suites with HTDP plug-ins, GAMMA, SARscape.
**Standards & guides.** ISO 19111:2019 (dynamic datums); IOGP Guidance Note 373-25 (time-dependent transformations); NGS NSRS modernization blueprints (NOAA TR NOS NGS 62/64/67); Geoscience Australia GDA2020 Technical Manual; LINZ NZGD2000 deformation model documentation.
**Key references.** Argus, Gordon & DeMets 2011 (NNR-MORVEL56); Altamimi et al. 2023 (ITRF2020); Peltier, Argus & Drummond 2015 (ICE-6G_C); Dixon et al. 2006 *Nature* (New Orleans subsidence); Galloway & Burbey 2011 *Hydrogeol. J.*; Shirzaei et al. 2021 *Nat. Rev. Earth Env.* (coastal subsidence); Pearson & Snay 2013 (HTDP); Stanaway, Roberts & Blick 2014 (dynamic datums).
**Pitfalls.** Mixing ITRF-realized GNSS heights with a plate-fixed national datum without epoch propagation; assuming "WGS 84" is one thing; using a benchmark published decades ago without a VLM check; attributing subsidence to sea-level rise or vice versa.
**Key takeaways.** Coordinates have velocities; a datum is a frame plus an epoch plus a deformation model; vertical land motion is often the largest term in coastal elevation change — measure it, don't assume it away.

### Chapter 39 — Earthquakes, volcanoes, landslides: sudden deformation and its datum consequences
**Scope.** Episodic motion that invalidates control, DEMs, and charts in minutes.
**Sections.**
- 39.1 Coseismic displacement: magnitude vs offsets (Tōhoku 2011: >5 m horizontal, ~1 m subsidence; Kaikōura 2016: up to ~6 m uplift; Maule 2010; Sumatra 2004); far-field reach of displacement
- 39.2 Post-seismic relaxation and afterslip: motion that continues for years; the "patch" problem for deformation models
- 39.3 What a national agency does after an earthquake: GSI Japan's coordinate revision after Tōhoku; LINZ's deformation model patches; re-survey of benchmarks and CORS; chart and port re-survey (Kaikōura harbour uplift)
- 39.4 Measuring it: GNSS, InSAR (coseismic interferograms), optical image correlation (COSI-Corr, MicMac), lidar differencing (El Mayor–Cucapah 2010; Nissen et al. 2012 ICP method), MBES repeat surveys (Tōhoku seafloor displacement ~50 m, Fujiwara et al. 2011)
- 39.5 Volcanic deformation and new terrain: inflation/deflation, lava flows (Kīlauea 2018, La Palma 2021 — new land, DEMs obsolete in days), dome growth, ash, caldera collapse
- 39.6 Landslides and mass movements: pre/post DEM differencing, volume estimation and its uncertainty, Oso 2014 (lidar showed prior slides), rock avalanches, submarine landslides and cable breaks (Grand Banks 1929 ⟨H⟩)
- 39.7 Tsunami and surge erosion/deposition as instantaneous terrain change; post-event survey priorities and perishable data
- 39.8 Chart and DEM invalidation policy: when to withdraw products; notices to mariners; rapid-response DEMs (ArcticDEM/REMA strips, Pléiades, drone)
**Then & now.** 1906 San Francisco triangulation revealed elastic rebound (Reid 1910); 1964 Alaska uplift mapped with barnacle lines; now coseismic fields are in InSAR within days and in deformation models within months.
**Math.** Okada 1985 elastic dislocation (displacement field from a rectangular fault); ICP for 3D displacement from point clouds; volume difference with spatially correlated error (preview Ch. 41).
**Software.** Open: ISCE2, GMTSAR, LiCSAR products, COSI-Corr (free), MicMac, py4dgeo, CloudCompare, xdem, Okada implementations (okada_wrapper, Coulomb — free); Closed: GAMMA, SARscape, ENVI, Trimble/Leica survey office for control re-adjustment.
**Standards & guides.** GSI Japan post-earthquake coordinate revision notices; LINZ deformation-model patch policy; IHO S-44 (survey after events); USGS post-event lidar acquisition protocols (3DEP); NOAA NRT survey procedures (Navigation Response Teams).
**Key references.** Reid 1910 (elastic rebound); Okada 1985 *BSSA*; Nissen et al. 2012 *GRL*; Oskin et al. 2012 *Science* (El Mayor lidar); Fujiwara et al. 2011 *Science*; Hamling et al. 2017 *Science* (Kaikōura); Clark et al. 2017 (Kaikōura coastal uplift); Iverson et al. 2015 *EPSL* (Oso); Leprince et al. 2007 *IEEE TGRS* (COSI-Corr); Heezen & Ewing 1952 (Grand Banks turbidity current).
**Pitfalls.** Using pre-event control after a M7+ event; comparing post-event DEM to pre-event DEM referenced to now-displaced control and "finding" uniform offsets; ignoring post-seismic drift years later; volume estimates without error bars; forgetting that the seafloor moved too.
**Key takeaways.** After a large event, control is a hypothesis to be re-tested; coseismic deformation is a datum event, not just a hazard; rapid-response DEMs are valuable but must be labelled provisional.

### Chapter 40 — Erosion, deposition, and geomorphic change
**Scope.** The slow (and sometimes fast) reshaping of the surface by water, wind, ice, gravity, and people.
**Sections.**
- 40.1 Processes and rates: hillslope diffusion, fluvial incision and aggradation, bank erosion, coastal cliff retreat, beach/dune dynamics, glacial scour, aeolian transport, gullying, soil creep, bioturbation, anthropogenic earth moving (humans now move more sediment than rivers)
- 40.2 Geomorphic change detection (GCD): DEM of Difference (DoD), thresholding by level of detection (LoD), spatially variable error, probabilistic thresholding, volumetric budgets with uncertainty
- 40.3 Sediment budgets and the "net vs gross" problem; compensating errors; erosion masked by deposition within a cell
- 40.4 Coastal: shoreline change (DSAS), beach volume, storm response, cliff retreat, sea-level feedback; bathymetric change at inlets and nearshore bars
- 40.5 Rivers: bedform migration, braided river dynamics, dam effects (sediment starvation, reservoir infilling, bathymetric surveys for capacity), post-fire debris flows
- 40.6 Glaciers and ice: geodetic mass balance (Hugonnet 2021), penetration bias in radar DEMs over firn, ice-sheet change (ICESat/ICESat-2, CryoSat-2), glacial lake outburst floods
- 40.7 Using DEM-derived morphometrics to infer process: slope–area, hypsometry, roughness, drainage density, knickpoints — and the resolution dependence of all of them
- 40.8 Anthropogenic change: terraces, levelled fields, quarries, landfills, land reclamation, dredging and dumping (Ch. 65)
**Then & now.** Repeat cross-sections and erosion pins → repeat total station/GNSS surveys → repeat lidar/SfM/MBES; from "did it change?" to "where, how much, with what confidence?"
**Math.** DoD: ΔZ = Z₂ − Z₁; σ_ΔZ = √(σ₁² + σ₂²) (independent errors); LoD = t·σ_ΔZ; volume V = Σ ΔZ_i·A with error propagation including spatial correlation (effective number of independent cells); fuzzy-inference error surfaces (Wheaton 2010).
**Software.** Open: GCD (Riverscapes), xdem, py4dgeo, CloudCompare M3C2, DSAS (USGS, free ArcGIS add-in), LSDTopoTools, TopoToolbox, Landlab, WhiteboxTools; Closed: ArcGIS Pro, Global Mapper, Trimble Business Center earthwork tools.
**Standards & guides.** USGS DSAS user guide; USACE EM 1110-2-4000 (sedimentation); Riverscapes GCD documentation; FGDC shoreline metadata profile.
**Key references.** Wheaton et al. 2010 *ESPL* (GCD/LoD); Brasington, Langham & Rumsby 2003; Lane, Westaway & Hicks 2003; James, Hodgson, Ghoshal & Latiolais 2012 *Geomorphology* (DEM differencing review); Passalacqua et al. 2015 *Earth-Sci. Rev.*; Hugonnet et al. 2021 *Nature*; Himmelstoss et al. 2021 (DSAS v5); Hooke 2000 *Geology* (humans as geomorphic agents); Wilkinson & McElroy 2007 *GSA Bull.*
**Pitfalls.** Reporting change below the LoD; summing volumes without correlated error; comparing DEMs from different sensors with different ground definitions (grass height, canopy, water); mistaking co-registration shift for erosion on slopes (aspect-dependent bias — Nuth & Kääb); morphometrics compared across resolutions.
**Key takeaways.** Change is a difference of two uncertain surfaces; co-register first, threshold by LoD, report volumes with intervals; many "erosion" signals are datum or registration artefacts until proven otherwise.

### Chapter 41 — Change detection methods and the minimum detectable change
**Scope.** The methods toolbox for comparing elevation data across time (and across sources), and the statistics of what can honestly be claimed.
**Sections.**
- 41.1 Co-registration before comparison: Nuth & Kääb 2011 (aspect/slope cosine fit), ICP variants, feature-based matching, bias correction over stable terrain; the half-pixel registration problem (Ch. 31)
- 41.2 Grid-based: DoD, LoD, spatially variable uncertainty, slope-dependent error, curvature effects; vertical vs normal-direction change
- 41.3 Point-cloud-based: C2C, C2M, M3C2 (Lague 2013), M3C2-EP (error propagation; Winiwarter 2021), multi-scale normals, 4D time-series methods (Anders 2020 4D-OBC), permanent laser scanning
- 41.4 InSAR time series (PS/SBAS) as mm-scale change detection; limits: decorrelation, atmosphere, unwrapping errors, LOS geometry
- 41.5 Image-based: optical correlation (COSI-Corr, MicMac, autoRIFT), feature tracking on ice and dunes
- 41.6 Bathymetric change: MBES repeat surveys, uncertainty from tides/sound speed/vessel; dredge monitoring; bedform tracking; sandwave migration for cable and pipeline risk
- 41.7 Semantic change vs geometric change: building appeared, tree removed, pile grew — classification-aware differencing (links Ch. 42)
- 41.8 Minimum detectable change: formal definitions, power analysis, confidence maps; how sensors/survey design trade MDC vs coverage vs cost
- 41.9 Separating signal from confounds: season (Ch. 36), moving objects (Ch. 27), datum changes (Ch. 38–39), processing-version changes, "comparing DSM to DTM = trees"
**Then & now.** Visual comparison of maps → DoD in GIS (1990s) → statistically thresholded GCD (2000s) → point-cloud and 4D methods with per-point uncertainty (2010s–) → continuous monitoring (permanent TLS, InSAR, UAV repeat).
**Math.** Nuth & Kääb: dh/tan(α) = a·cos(b − ψ) + c; M3C2 distance and its LoD₉₅ ≈ 1.96·√(σ₁²/n₁ + σ₂²/n₂) + reg; power of a test for Δz given σ and N; variogram-based effective sample size; hypothesis testing framing (Type I vs II errors in change maps).
**Software.** Open: xdem, py4dgeo, CloudCompare (M3C2), GCD, demcoreg, autoRIFT, MintPy, LiCSBAS, OpenTopography differencing service; Closed: TerraScan, Trimble RealWorks, Leica Cyclone 3DR, Global Mapper, Esri change-detection tools.
**Standards & guides.** USGS 3DEP guidance on repeat-collection comparison; IHO S-44 (repeat survey for change); ASPRS positional accuracy standards (for epoch comparability).
**Key references.** Nuth & Kääb 2011 *The Cryosphere*; Lague, Brodu & Leroux 2013 *ISPRS J.*; Winiwarter, Anders & Höfle 2021 *ISPRS J.*; Anders et al. 2020/2021; Qin, Tian & Reinartz 2016 *ISPRS J.* (3D change detection review); Okyay et al. 2019 *Earth-Sci. Rev.* (airborne lidar change detection); Hugonnet et al. 2022 *IEEE JSTARS* (uncertainty of DEM differencing); Ferretti, Prati & Rocca 2001; Berardino et al. 2002 (SBAS).
**Pitfalls.** Skipping co-registration; using global σ for slope-dependent errors; detecting "change" that is a reprocessed baseline; mixing surface definitions; declaring MDC after seeing the data; publishing change maps without a confidence layer.
**Key takeaways.** Register, estimate uncertainty spatially, threshold, then interpret; report what you cannot detect as clearly as what you can; the best change detector is a survey designed for change.

---

## Part IX — Semantics, learning, and enhancement

### Chapter 42 — Object detection and semantic labelling of the surface
**Scope.** Assigning meaning (ground, building, tree, wire, water, car, ship, pile) to points, pixels, and cells — a prerequisite for DTMs, obstacle data, and change interpretation.
**Sections.**
- 42.1 Label schemes: ASPRS LAS classes (0–255; standard 0–22, wires 13–16, bridge deck 17, overlap flag), CityGML/LoD classes, OSM tags, land cover vs object classes, hydro feature classes, S-57/S-101 object classes for charts; why schemes disagree (Ch. 32)
- 42.2 Features from geometry: height above ground, normals, eigenvalue features (linearity, planarity, sphericity), roughness, intensity/return number, multi-scale neighbourhoods; from imagery: spectral, texture, NDVI/NDWI
- 42.3 Classical pipelines: rule-based (height + planarity), region growing, RANSAC planes, morphological filters, random forests/gradient boosting on hand-crafted features
- 42.4 Deep learning on point clouds (PointNet/PointNet++, KPConv, RandLA-Net, Point Transformer, sparse voxel CNNs), on rasters (U-Net family, SegFormer), fused 2D–3D; foundation-model era (SAM on orthos/DSMs, Prithvi, Clay) and their failure modes on elevation data
- 42.5 Object detection and instance segmentation: buildings (footprints, roof planes; Open Buildings, Microsoft footprints), trees (ITC delineation), vehicles, ships (SAR ship detection; AIS fusion), power infrastructure, solar panels, antennas, piles and stockpiles, caves/sinkholes
- 42.6 Benchmarks and datasets: ISPRS Vaihingen/Toronto, DALES, OpenGF (ground filtering), Semantic3D, SensatUrban, Toronto-3D, H3D, US3D/DFC2019, Hessigheim, STPLS3D; bathymetric object detection sets (wrecks, boulders; MBES backscatter)
- 42.7 Evaluation: per-class IoU/F1, boundary metrics, geometric effect of label error on the DTM (a mislabelled roof point = a 10 m bump), transfer across regions/sensors/densities
- 42.8 Human-in-the-loop editing, QA/QC sampling, and labelling cost
**Then & now.** Manual stereoplotter compilation ⟨H⟩ → morphological/TIN filters (Axelsson 2000) → random forests on eigenfeatures → point-cloud deep learning (PointNet 2017) → foundation models; LAS class list grew to express wires, bridges, and overlap.
**Math.** Covariance eigenfeatures (λ₁ ≥ λ₂ ≥ λ₃; linearity (λ₁−λ₂)/λ₁ etc.); confusion matrix → IoU, κ; graph/CRF smoothing; sampling-based accuracy estimates with confidence intervals.
**Software.** Open: PDAL (filters.smrf/pmf/csf), lidR, CloudCompare (CANUPO, CSF), Open3D-ML, torch-points3d, Pointcept, segment-geospatial, Raster Vision, scikit-learn; Closed: TerraScan (macro + ML), LP360 AI, Esri 3D Basemaps/deep learning packages, Trimble eCognition, Bentley/Orbit, Global Mapper Pro.
**Standards & guides.** ASPRS LAS 1.4 R15 classification table; USGS LBS classification requirements and accuracy thresholds; OGC CityGML 3.0; IHO S-101 feature catalogue; ISPRS benchmark protocols.
**Key references.** Axelsson 2000; Weinmann, Jutzi, Hinz & Mallet 2015 *ISPRS J.*; Qi et al. 2017 (PointNet/PointNet++); Thomas et al. 2019 (KPConv); Hu et al. 2020 (RandLA-Net); Qin et al. 2021 (OpenGF); Varney, Asari & Graehling 2020 (DALES); Sirko et al. 2021 (Open Buildings); Niemeyer, Rottensteiner & Soergel 2014; Kirillov et al. 2023 (SAM).
**Pitfalls.** Models trained on one density/sensor silently degrade on another; benchmarks dominated by European/North American cities; labelling "bridge" differently from the DTM spec; evaluating labels but never the resulting DTM; data leakage between train/test tiles that share a scene.
**Key takeaways.** Labels are hypotheses with error rates; a DTM is only as good as its ground label; validate semantics with geometric consequences in mind, and across domains, not just on a held-out tile from the same city.

### Chapter 43 — Traditional versus machine-learning methods: a cross-cutting assessment
**Scope.** Where learned methods help, where physics and statistics still win, and how to validate each honestly — applied across the handbook's tasks.
**Sections.**
- 43.1 Task-by-task scorecard: ground filtering, building extraction, void filling, DEM error correction, SDB, bathymetric outlier cleaning, super-resolution, feature matching in SfM, GNSS multipath mitigation, sound-speed estimation, change detection
- 43.2 What "traditional" means: physics-based models, geometric algorithms, geostatistics (kriging, variograms), robust estimation, rule systems — interpretable, with error propagation
- 43.3 What ML adds: nonlinear priors from large data; what it costs: hidden assumptions, dataset shift, lack of calibrated uncertainty, hallucination of plausible but false terrain
- 43.4 ML-corrected global DEMs: CoastalDEM (Kulp & Strauss 2018), FABDEM (Hawker 2022), DeltaDTM (Pronk 2024), DiluviumDEM, ForestDTM-type products — how they were trained, what the validation does and does not show, where they fail (low-relief forests, built-up areas, regions with no training data)
- 43.5 Validation for ML: spatial cross-validation and area of applicability (Meyer & Pebesma), block CV, independent-source checkpoints, temporal holdouts, reporting per-stratum error (slope, land cover, latitude)
- 43.6 Uncertainty from ML: ensembles, MC dropout, quantile regression, conformal prediction; calibration tests; why a confidence map from a network is not an accuracy map
- 43.7 Hybrid designs: physics-guided learning, learned priors in Bayesian inversion (SDB), ML for QC flagging with human review, classical algorithms with learned parameters
- 43.8 Reproducibility, versioning of models and training data, model cards for geospatial products, licence contamination (training on NC data)
- 43.9 Decision guide: when a 20-year-old algorithm is the right answer
**Then & now.** Hand rules → statistical learning (RF/SVM 2000s) → deep learning (2015–) → foundation models; meanwhile geostatistics and robust estimation never stopped being correct.
**Math.** Bias–variance decomposition; spatial autocorrelation and the optimism of random CV; proper scoring rules (CRPS, log score) for probabilistic predictions; conformal prediction intervals; calibration curves.
**Software.** Open: scikit-learn, PyTorch/TensorFlow, TorchGeo, CAST (R, spatial CV/AOA), blockCV, MAPIE (conformal), xgboost/LightGBM, GSTools/PyKrige (geostatistics); Closed: Esri deep learning toolsets, eCognition, cloud AutoML platforms.
**Standards & guides.** ISO/IEC 23053 (ML framework); OGC Training Data Markup Language for AI (TrainingDML-AI); model cards (Mitchell 2019); ASPRS positional accuracy standards still apply to ML outputs.
**Key references.** Meyer & Pebesma 2021 *MEE* / 2022 *Nat. Commun.* (AOA, spatial CV); Ploton et al. 2020 *Nat. Commun.*; Roberts et al. 2017 *Ecography*; Kulp & Strauss 2018 *RSE*; Hawker et al. 2022 *ERL*; Pronk et al. 2024 *ESSD*; Breiman 2001 (two cultures); Reichstein et al. 2019 *Nature*; Mitchell et al. 2019 (model cards).
**Pitfalls.** Random train/test splits across autocorrelated terrain; "RMSE 1.2 m globally" hiding 8 m errors in mangroves; a corrected DEM that removed real terraces as "buildings"; training on a product that itself was ML-corrected; uncertainty maps nobody calibrated.
**Key takeaways.** ML is a powerful prior, not a measurement; validate with spatially independent truth and report where the model has no applicability; prefer hybrid methods that keep physics and error propagation in the loop.

### Chapter 44 — Resolution, pixel size, sampling, and oversampling
**Scope.** What resolution means for points and grids, why nominal and effective resolution differ, and how resolution governs every derived quantity.
**Sections.**
- 44.1 Definitions: ground sample distance, post spacing, point density/spacing, footprint, effective/true resolution (smallest resolvable feature), nominal pulse spacing (NPS) and density (NPD) in LBS; sonar beam footprint vs grid size
- 44.2 Sampling theory: Nyquist–Shannon ⟨H⟩, aliasing in terrain, anti-aliasing by footprint averaging, the footprint–spacing ratio; point-to-grid aggregation choices (mean, min, max, IDW, TIN-linear) as low-pass filters
- 44.3 Nominal vs effective: Copernicus 30 m from 12 m TanDEM-X; ASTER GDEM effective ~70–100 m; SRTM 1″ from ~45 m along-track averaging; SDB "10 m" products with km-scale information content; "1 m lidar DEM" from 2 pts/m² — spectral analysis to estimate true resolution
- 44.4 Oversampling: gridding finer than the data (smooth but not informative), legitimate uses (visual continuity, matching another grid) and illegitimate uses (implying detail); storing resolution and source density together
- 44.5 Resolution dependence of derivatives: slope decreases with coarser cells (Zhang & Montgomery 1994; Grohmann 2015), curvature, roughness, TWI, viewshed, flow accumulation; feature detectability vs cell size; hydrological connectivity (culverts, levees) lost at coarse resolution
- 44.6 Choosing resolution for a purpose: cost/area trade-offs; hydrologic vs navigational vs geological needs; mandatory feature detection sizes (S-44 cubic features 1 m/2 m; aviation obstacle sizes)
- 44.7 Multi-resolution representation: overviews/pyramids (Ch. 46), variable-resolution grids (BAG VR, CUBE), adaptive TINs; honest resampling when mixing (Ch. 48)
- 44.8 Reporting: ISO 19115 spatial resolution fields, "distance" vs "equivalent scale", pixel-is-area vs pixel-is-point (GeoTIFF RasterPixelIsArea/Point) and the half-cell shift
**Then & now.** Contour interval as the resolution surrogate ⟨H⟩ → raster post spacing (DTED levels 0/1/2 at 30″/3″/1″ ⟨H⟩) → point density specs (LBS QL0–QL3) → effective-resolution metrics (DEMIX, spectral).
**Math.** Sampling theorem and aliasing; modulation transfer function of footprint convolution; slope from finite differences and its dependence on cell size h (Horn's operator); power spectra of terrain (roughly 1/f^β) and the resolution at which noise exceeds signal; effective resolution estimation (Grohmann 2015; Guth 2024 DEMIX).
**Software.** Open: GDAL (gdalwarp resampling kernels, gdaladdo), PDAL (density/overlap metrics), lidR (density), WhiteboxTools, GRASS r.resamp.*, xdem; Closed: Global Mapper, ArcGIS Pro, QPS Qimera (CUBE resolution estimation), CARIS (VR surfaces).
**Standards & guides.** USGS LBS 2024 (NPS/NPD, QL table); IHO S-44 Ed. 6.1.0 (feature detection and search); ICAO Annex 15 eTOD post spacing; ASPRS Ed. 2 (resolution–accuracy relationships); OGC GeoTIFF 1.1 raster space definitions.
**Key references.** Shannon 1949 ⟨H⟩; Zhang & Montgomery 1994 *WRR*; Hengl 2006 *Comput. Geosci.* (finding the right pixel size); Grohmann 2015 *Comput. Geosci.*; Florinsky & Kuryakova 2000; Guth et al. 2021 *Remote Sens.* (DEM terminology/effective resolution); Polidori & El Hage 2020 *Remote Sens.* (DEM quality review); Kienzle 2004; Tarolli 2014 *Geomorphology* (high-resolution topography).
**Pitfalls.** Reading "30 m" as "features of 30 m are resolved"; comparing slopes across resolutions; oversampling SDB to match lidar and treating it as equal; losing a 3 m levee in a 10 m grid and modelling a flood that can't happen (or one that can't be stopped); ignoring the half-pixel convention shift.
**Key takeaways.** Resolution is a property of the information, not the file; derivatives inherit resolution dependence; store and publish source density, footprint, and effective resolution alongside pixel size.

### Chapter 45 — Super-resolution and DEM enhancement
**Scope.** Methods that produce finer, cleaner, or more complete elevation surfaces than the input — and the epistemics of trusting them.
**Sections.**
- 45.1 Taxonomy: interpolation upsampling (bicubic, spline, kriging) vs single-image SR (SRCNN/ESRGAN/diffusion-style for DEMs) vs multi-source fusion SR (DSM + optical texture, DEM + SAR, lidar + SfM) vs multi-epoch stacking (aliasing-based SR; TanDEM-X multi-acquisition) vs physics-driven enhancement (shape-from-shading, photoclinometry)
- 45.2 Noise reduction and artefact removal: stripe removal (SRTM/ASTER), speckle/outlier filtering, terrace/stair-step removal from contour-derived DEMs, "pit and peak" filters, feature-preserving smoothing (bilateral, anisotropic diffusion), ML denoisers
- 45.3 Void filling and inpainting (Ch. 35) as a special case of enhancement; generative inpainting risks
- 45.4 Terrain synthesis and example-based amplification (graphics community: Guérin 2017, Argudo 2018) vs geoscience needs — plausible ≠ true
- 45.5 Bathymetric enhancement: gravity-guided interpolation (Smith & Sandwell), machine-learned seafloor prediction, SDB fused with sparse soundings; chart "generalization" as the inverse problem
- 45.6 Validation: against independent high-resolution truth, per-feature metrics (edge sharpness vs position error), hallucination detection, spectral checks, "sharper ≠ truer"; the danger of training and testing on the same terrain types
- 45.7 Communicating enhancement: mandatory metadata (method, training data, input resolution, intended use), "enhanced" vs "measured" layer flags, downstream constraints (never use SR DEMs for legal or navigational decisions)
- 45.8 When enhancement is appropriate: visualization, priors for matching, hypothesis generation, consistent-resolution mosaics with explicit uncertainty inflation
**Then & now.** Contour-to-grid smoothing (ANUDEM 1989) → signal-processing SR → deep SR (2015–) → diffusion/generative models (2022–); bathymetry: hand contouring → gravity-predicted depth (1997) → ML seafloor prediction.
**Math.** SR as ill-posed inverse problem: y = D·H·x + n; regularization and priors; perceptual vs fidelity losses; uncertainty inflation when combining measured and predicted cells; spectral slope checks for over-sharpening.
**Software.** Open: GDAL/ANUDEM-style tools (GRASS r.surf.contour, r.fill.stats), xdem, WhiteboxTools (feature-preserving smoothing), PyTorch SR codebases (DEM-SR repos), GMT surface/grdfill; Closed: ArcGIS Topo to Raster (ANUDEM), Global Mapper, ENVI, commercial "AI upscaling" tools.
**Standards & guides.** No formal spec exists for SR DEMs — recommend ISO 19115 lineage statements, ASPRS accuracy reporting on independent checkpoints, and a required "derived/enhanced" flag; GEBCO TID codes as a model for distinguishing measured from predicted.
**Key references.** Hutchinson 1989 (ANUDEM); Smith & Sandwell 1997 *Science*; Xu et al. 2015 (DEM SR); Chen et al. 2016; Argudo, Chica & Andújar 2018 *Comput. Graph. Forum*; Guérin et al. 2017 *ACM TOG*; Demiray, Sit & Demir 2021 *SN Comput. Sci.* (D-SRGAN); Yue et al. 2015 *ISPRS J.* (fusion); Lin et al. 2023 *IEEE TGRS*; Kubade et al. 2021; Dong, Loy, He & Tang 2016 (SRCNN); Tozer et al. 2019 (SRTM15+ predicted bathymetry).
**Pitfalls.** Presenting SR output at 1 m with the metadata of the 30 m input; hallucinated gullies and buildings; validating with PSNR on the training domain; using SR bathymetry for a navigation product; losing the measured/predicted distinction in a mosaic.
**Key takeaways.** Enhancement adds assumptions, not measurements; label it, bound it, validate it independently, and keep it out of safety-critical decisions unless the uncertainty is explicitly inflated and accepted.

---

## Part X — Representing, storing, finding, and keeping elevation data

### Chapter 46 — Data models: points, waveforms, grids, TINs, meshes, voxels, variable resolution, overviews, splats
**Scope.** The abstract structures elevation data live in, what each can and cannot express, and the information lost at each conversion.
**Sections.**
- 46.1 Point clouds: attributes (XYZ, intensity, returns, class, GPS time, scan angle, RGB/NIR, uncertainty), unorganized vs organized (scanline/swath), density as a first-class property
- 46.2 Full waveforms and photon-counting: waveform decomposition (Gaussian), Geiger-mode/single-photon noise statistics (ICESat-2 ATL03→ATL08), sonar water-column data and snippets/backscatter; why waveforms matter for canopy, bathymetry, and uncertainty
- 46.3 Grids/rasters: 2.5D single-valued surfaces, cell semantics (area vs point), nodata, multi-band (elevation, uncertainty, source, date, count), tiling and chunking, pyramids/overviews — and why an overview can lie (min/max/mean/nearest choice changes the "terrain")
- 46.4 TINs and breaklines: Delaunay, constrained Delaunay, hard/soft breaklines, mass points; adaptive density; TIN→grid and grid→TIN losses; contour-derived TINs and flat triangles
- 46.5 Meshes (3D surfaces, textured; multi-valued, overhangs, buildings), level-of-detail meshes (quantized-mesh, 3D Tiles, I3S), BIM/CityGML solids; mesh simplification error metrics (Hausdorff)
- 46.6 Voxels and occupancy (OctoMap, TSDF), implicit surfaces (SDFs, NeRF density), Gaussian splats as a rendering representation vs a measurement representation
- 46.7 Variable-resolution surfaces: CUBE/CHRT, BAG VR, quadtree/octree tilings ⟨H⟩, resolution-by-uncertainty; multi-resolution hydrographic surfaces
- 46.8 Hierarchical and spatial indexing: quadtrees, octrees, k-d trees, R-trees, Hilbert/Morton ordering ⟨H⟩, COPC/EPT octrees, DGGS (Ch. 60)
- 46.9 Attribute models for uncertainty: per-point vs per-cell vs per-tile; uncertainty bands in BAG; covariance vs scalar; TPU propagation into grids (CUBE hypotheses)
- 46.10 Conversion matrix: points→grid (binning, interpolation), grid→contours, TIN↔grid, mesh→DSM (rasterizing multi-valued surfaces), splats→nothing measurable (yet)
**Then & now.** Contours and spot heights ⟨H⟩ → regular grids (DTED 1970s; USGS DEM) → TINs (Peucker et al. 1978) → dense point clouds (2000s) → waveforms/photons → meshes and 3D tiles → neural/splat representations (2020s).
**Math.** Delaunay properties and constrained triangulations; Gaussian waveform decomposition; Morton/Hilbert curve index construction; octree level ↔ resolution; Hausdorff distance for mesh simplification; CUBE hypothesis statistics (Calder & Mayer 2003).
**Software.** Open: PDAL, laspy, Entwine/COPC, Potree, Open3D, PyVista/VTK, CGAL, GDAL (overviews), TINs in GRASS/SAGA/QGIS, OctoMap, MBSystem; Closed: TerraSolid, CARIS HIPS/BASE, QPS Qimera/Fledermaus, ArcGIS (terrain datasets, LAS datasets), Global Mapper, Bentley ContextCapture/iTwin.
**Standards & guides.** OGC 3D Tiles 1.1; Esri I3S (OGC community standard); Cesium quantized-mesh; ONS BAG VR extension; ASPRS LAS 1.4 (waveform packets); ICESat-2 ATBDs; CityGML 3.0.
**Key references.** Peucker, Fowler, Little & Mark 1978 (TIN); Calder & Mayer 2003 *G³* (CUBE); Calder & Rice 2017 (CHRT); Mallet & Bretar 2009 *ISPRS J.* (full-waveform review); Neuenschwander & Pitts 2019 (ATL08); Hornung et al. 2013 (OctoMap); Kerbl et al. 2023 (3D Gaussian splatting); Samet 1984 (quadtrees); Garland & Heckbert 1997 (mesh simplification).
**Pitfalls.** Treating a DSM raster as "the data" when the points exist; nearest-neighbour overviews that drop every narrow ridge; TIN flat triangles on ridgelines from contour sources; storing uncertainty as an afterthought band with no definition; meshes with overhangs rasterized to the highest surface by default.
**Key takeaways.** Pick the structure that preserves what the use needs; every conversion is a lossy model decision — document it; keep the richest representation (points/waveforms) archived.

### Chapter 47 — File formats: LAS/LAZ/COPC, GeoTIFF/COG, BAG/S-102, NetCDF/Zarr, DTED, and the rest
**Scope.** The practical encodings, their semantic gaps, and the format-induced errors that recur in real projects.
**Sections.**
- 47.1 Point formats: ASPRS LAS 1.0–1.4 (PDRFs 0–10, extra bytes, OGC WKT CRS, classification flags, overlap, scanner channel), LAZ compression, COPC (cloud-optimized octree in LAZ) and EPT, E57 (terrestrial), PLY/PCD/PTX, ASCII XYZ and its CRS-less peril; zLAS (closed); scale/offset precision traps
- 47.2 Raster formats: GeoTIFF 1.1 (OGC), COG (OGC 21-026), GeoKeys and vertical CRS keys (EPSG compound), RasterPixelIsArea/Point, nodata conventions, compression (DEFLATE/ZSTD/LERC with max error); Terrain-RGB/Terrarium quantization; Esri ASCII/.flt/.hdr; SRTM .hgt (edge-overlapping 3601×3601 ⟨H⟩); USGS DEM/SDTS legacy and contour-ghost stair-steps; DTED (MIL-PRF-89020B, levels 0–2, latitude-dependent spacing, MSL/EGM96); NITF; JPEG2000 (lossy use warnings); IMG (Erdas); GRIB for model orography
- 47.3 Hydrographic: BAG (ONS; elevation + uncertainty + metadata + tracking list; VR extension; uncertainty-type semantics), S-102 (HDF5, S-100 framework, Ed. 3.0 and 3.1, QualityOfSurvey/uncertainty, tiling, encryption S-100 Part 15), S-57/S-101 soundings and depth areas, GSF, vendor raw (.all/.kmall Kongsberg, .s7k Reson/Teledyne, .xtf, .jsf, .r2sonic), SBET/POSPac trajectories, Hypack/Qinsy project formats, GEBCO/ETOPO NetCDF, CSAR (CARIS, closed)
- 47.4 Multidimensional and cloud-native: NetCDF-4/HDF5 with CF conventions, Zarr v2/v3, GeoZarr, Icechunk ⟨H⟩, Kerchunk; chunking strategies for DEMs; tiled web formats (XYZ tiles, quantized-mesh, 3D Tiles, PMTiles)
- 47.5 Vector and 3D exchange: CityGML/CityJSON, IFC/BIM, LandXML, DXF/DWG (no CRS; local grid-vs-ground), OBJ/glTF/USD, GeoPackage (rasters and vectors), GeoParquet; contours and breaklines in GPKG/shapefile (.prj limitations)
- 47.6 Format-induced error catalog: integer quantization (LAS scale factors; DTED integer meters; Terrain-RGB 0.1 m steps), float32 precision at large coordinates, lossy LERC/JP2, nodata collisions (−9999 vs −32768 vs NaN), vertical CRS lost on export, half-cell shifts between pixel conventions, tile seam artefacts, big-endian legacies
- 47.7 Choosing a format by role: acquisition raw (keep forever), working, delivery (spec-mandated), archive, web
- 47.8 Validation tools for files: lasinfo/lasvalidate, pdal info, gdalinfo + cogger validators, BAG validation, S-100 validation checks
**Then & now.** Vendor binaries and ASCII → USGS DEM/SDTS (1990s) → LAS 1.0 (2003) ⟨H⟩ → GeoTIFF spec (1995) → BAG 1.0 (2006) → LAZ (2011) → COG (2016–) → COPC (2021), Zarr/GeoZarr (2020s), S-102 Ed. 3 (2024).
**Math.** Quantization error (uniform: σ = q/√12); float32 precision limits (24-bit significand: ulp ≈ 0.8 cm at 10⁵ m, 6 cm at 10⁶ m, 0.5 m at 5×10⁶ m — projected northings must not be stored as float32 without an offset); LERC max-error semantics; Hilbert-ordered octree addressing in COPC.
**Software.** Open: PDAL, LAStools (partly open), laspy, GDAL/rasterio, libLAS (legacy), MB-System, HDF5/h5py, xarray/rioxarray, Zarr-Python, cogger/rio-cogeo, pybag/OpenNS BAG library, s100py (NOAA), GeoPandas; Closed: LAStools (licensed tools), CARIS, QPS, Hypack, Global Mapper, FME, ArcGIS, TerraSolid.
**Standards & guides.** ASPRS LAS 1.4 R15 (2019) and the LAS 1.4 domain profile for topo-bathy; OGC GeoTIFF 1.1 (19-008r4); OGC COG 1.0 (21-026); ONS BAG Format Specification 2.0 (verify edition/date); IHO S-100 Ed. 5, S-102 Ed. 3.0 (3.1 — verify); MIL-PRF-89020B (DTED); CF Conventions 1.11; Zarr v3 spec; OGC GeoPackage 1.4; OGC CityGML 3.0/CityJSON 2.0.
**Key references.** ASPRS LAS 1.4 R15 specification; Isenburg 2013 *PE&RS* (LAZ); Hobu Inc./USGS COPC spec 1.0; OGC COG; ONS 2024 BAG 2.0; IHO S-102 PS 3.0 (2024); Ritter & Ruth 1997 (GeoTIFF); Eaton et al. (CF conventions); Cesium quantized-mesh and OGC 3D Tiles specifications (web terrain delivery).
**Pitfalls.** LAS files with no CRS VLR and "it's probably State Plane feet"; GeoTIFF with horizontal CRS but no vertical CRS (orthometric or ellipsoidal? which geoid?); exporting BAG uncertainty into a GeoTIFF and losing its meaning; Terrain-RGB decoded with the wrong base/interval; DTED edges and integer meters taken as 1 m accuracy; a JP2 DEM with 0.5 m "lossless-looking" errors.
**Key takeaways.** The format is part of the measurement chain; always carry horizontal and vertical CRS, nodata, uncertainty, and lineage inside the file; validate files automatically on receipt and before delivery.

### Chapter 48 — Compositing: merging many datasets into one product
**Scope.** Building seamless DEMs/bathymetry from heterogeneous sources — the order, blend, crop, override, and bookkeeping rules that decide what the final cell means.
**Sections.**
- 48.1 Why composite: coverage, currency, resolution, cost; the price: inhomogeneous error, hidden seams, ambiguous provenance
- 48.2 Preparation: common horizontal and vertical datum (incl. tidal→orthometric→ellipsoidal conversions with VDatum/vyperdatum), surface-type harmonization (DSM vs DTM vs bathy "seafloor"), resolution alignment, co-registration and bias removal over overlaps (Ch. 41), outlier and artefact screening per source
- 48.3 Prioritization rules: by accuracy/uncertainty, by date (newest wins vs best wins), by resolution, by surface type, by source quality tier (NOAA NBS supersession rules; GEBCO/EMODnet source hierarchies; USGS 3DEP seamless rules); use-dependent overrides (shoal-biased for navigation; most-recent for change; most-accurate for engineering)
- 48.4 Blending and feathering: distance-weighted blends across overlap zones (GMT grdblend), gradient-domain blending, breakline-aware merges, no-blend hard edges with documented seams; avoiding the "blended cliff" and "feathered channel"
- 48.5 Cropping and masks: footprints, water masks, void masks, quality masks; Copernicus DEM editing/mask layers as an exemplar of publishing masks with the product
- 48.6 The land–water seam: topo lidar vs bathy lidar vs sonar vs SDB; shoreline consistency; tidal datum surfaces for the transition; CUDEM/CoNED practice; NAP–TAW cross-border seams
- 48.7 Mandatory companion layers: source ID raster, acquisition date raster, uncertainty raster (propagated or assigned per source), method/TID (GEBCO Type Identifier), lineage table; mosaic-level metadata
- 48.8 QC of composites: seam statistics, hydro-connectivity checks, visual hillshade sweeps, independent checkpoints per source zone, slope/aspect histograms at seams
- 48.9 Versioning composites: reproducible builds, supersession logs, "what changed since v2.1" rasters, retraction of bad sources
**Then & now.** Hand-drawn chart compilations and "best available" DEM mosaics → GTOPO30 (1996) ⟨H⟩, SRTM mosaics → GEBCO gridded compilations with TID (2014–) → NOAA National Bathymetric Source/BlueTopo (2020–) with per-cell source/uncertainty; USGS 3DEP seamless and 1 m DEM program.
**Math.** Weighted combination z = Σ w_i z_i / Σ w_i with w_i = 1/σ_i² (inverse-variance) and its invalidity under bias; distance-based feather weights; uncertainty of a composite cell under source switching; seam detection via gradient statistics.
**Software.** Open: GDAL (gdalwarp/gdalbuildvrt/gdal_merge, VRT masks), GMT grdblend, WhiteboxTools, CUDEM tools (NOAA NCEI "cudem" Python), MB-System mbgrid, QGIS, Vyperdatum/VDatum (free), xarray/dask pipelines; Closed: CARIS BASE Editor/BDB, QPS Fledermaus/Qimera, Global Mapper, ArcGIS mosaic datasets, Hypack.
**Standards & guides.** NOAA NBS/BlueTopo specification and supersession rules; GEBCO Cookbook (IHO B-11); EMODnet Bathymetry DTM methodology; USGS 3DEP seamless product spec; Copernicus DEM Product Handbook (mask layers); IHO S-102 tiling; ASPRS accuracy reporting for mosaics (by source zone).
**Key references.** Eakins & Grothe 2014 *Mar. Geod.* (challenges in building coastal DEMs); Amante & Eakins 2016 (CUDEM/NCEI methodology); Amante 2018 (uncertainty of coastal DEMs); Danielson et al. 2016 (CoNED); Weatherall et al. 2015/2020 (GEBCO); Wessel et al. 2019 (GMT 6); Marks & Smith 2006 (seamless bathy); Danielson & Gesch 2011 (GMTED2010); NOAA 2023 (BlueTopo); Pe'eri et al. 2014 (SDB in compilations).
**Pitfalls.** Newest source overriding a better older one (or vice versa) without a stated rule; blending a DSM into a DTM at the seam; a feathered bathy–topo transition that invents a beach slope; losing the per-source uncertainty; vertical datum mismatch of 0.3–1 m between neighbors read as a terrace; a composite with no date layer used for change detection.
**Key takeaways.** A composite is a decision, not a measurement; publish the decision (source, date, uncertainty, method rasters) with the surface; choose priority rules by use and declare them.

### Chapter 49 — Metadata
**Scope.** What must travel with elevation data for it to be used correctly — and how to produce it without heroics.
**Sections.**
- 49.1 The minimum set: horizontal and vertical CRS (with geoid model and epoch), surface type (DSM/DTM/bathy; what is included/excluded — bridges, piers, wires, vegetation), acquisition dates (start/end; per-cell where mixed), sensor/platform/method, processing lineage and software versions, resolution (nominal, source density, effective if known), accuracy/uncertainty (how assessed, against what, per stratum), voids/fills/masks, licence, contact, identifier/DOI, version
- 49.2 Standards: ISO 19115-1/-2/-3 (XML), ISO 19157 (data quality elements and measures), FGDC CSDGM ⟨H⟩ and its lidar/shoreline profiles, INSPIRE elevation specification metadata, STAC Item/Collection with extensions (pointcloud, raster, projection, eo, sat, scientific, processing, file), DataCite, schema.org/Dataset, OGC API – Records; GeoTIFF/LAS internal metadata vs sidecars
- 49.3 Hydrographic metadata: S-44 survey report elements, HSSD Descriptive Report (DR) and deliverables, BAG metadata (ISO 19115 inside), S-102 QualityOfSurvey, CATZOC/ZOC, GEBCO TID, IHO DCDB contribution metadata
- 49.4 Lidar/photogrammetric: USGS LBS metadata and project reports (acquisition, calibration, swath-to-swath, checkpoint tables), ASPRS accuracy reporting language, boresight/calibration reports, trajectory metadata (SBET), camera calibration certificates
- 49.5 Quality metadata that actually helps: uncertainty rasters, checkpoint tables with coordinates, strata, and residuals; swath overlap statistics; density maps; crossline statistics; known-issue lists
- 49.6 Generating metadata: templates, automation from processing logs, PDAL/GDAL/pystac pipelines, validation (ISO schema validators, stac-validator), human-written "limitations" sections (the most-read, least-written part)
- 49.7 Metadata decay and currency: superseded datasets, datum changes after publication, broken links; persistent identifiers
- 49.8 Reading metadata forensically: what is missing tells you what wasn't done (no vertical CRS → probably never checked; no checkpoints → accuracy is a guess) (links Ch. 54)
**Then & now.** Map marginalia and survey sheets' title blocks → FGDC CSDGM (1994/1998) ⟨H⟩ → ISO 19115 (2003/2014) → machine-first STAC (2017–; 1.0 in 2021 ⟨H⟩); from documents to records to API-queryable catalogs.
**Software.** Open: pystac/stac-validator, pygeometa, GeoNetwork, CKAN, pycsw, mdEditor, GDAL/PDAL metadata readers, ISO 19139 validators, NOAA s100py; Closed: ArcGIS metadata editor, CARIS, QPS, FME, commercial catalog portals.
**Standards & guides.** ISO 19115-1:2014/-2:2019/-3; ISO 19157-1:2023; FGDC-STD-001-1998 and shoreline/lidar extensions; STAC 1.0/1.1 and extensions; INSPIRE D2.8.II.1 (Elevation); USGS LBS 2024 metadata section; NOAA HSSD (DR, survey outline, metadata deliverables); IHO S-100 Part 4a (metadata); DataCite schema 4.
**Key references.** FGDC 1998; ISO 19115-1; Hanson & Holmes (STAC spec) 2021; Wilkinson et al. 2016 *Sci. Data* (FAIR); Carroll et al. 2020 (CARE); Goodchild 2007 (fitness-for-use, VGI metadata); Devillers et al. 2010 *IJGIS* (spatial data quality in practice); Tsou 2002 (metadata and interoperability).
**Pitfalls.** "Vertical datum: NAVD88" without geoid model; "accuracy: 0.1 m" without stating RMSE/95 %/CE/LE or checkpoint count; dates as the publication year not the acquisition year; metadata in a PDF nobody can query; copying a template's values into a new project.
**Key takeaways.** Metadata is the user's only defence against misuse; automate the structured parts, hand-write the limitations; if it's not in the metadata, assume it wasn't measured.

### Chapter 50 — Archiving, versioning, and provenance
**Scope.** Keeping elevation data usable, trustworthy, and traceable for decades — raw to product.
**Sections.**
- 50.1 What to keep: raw sensor data (waveforms, raw sonar, images, GNSS/IMU observables, trajectories), calibration records, intermediate products, final products, software/versions, scripts and parameters; why raw matters (reprocessing with better geoids, filters, ML; forensic reanalysis after disasters)
- 50.2 Formats for the long term: open, documented, self-describing (LAS/LAZ, GeoTIFF/COG, NetCDF/HDF5, BAG); migration plans for vendor raw; checksums and fixity (SHA-256), PREMIS, bagit
- 50.3 OAIS reference model; trusted repositories (CoreTrustSeal); national archives (NOAA NCEI, USGS EROS, NASA DAACs, LINZ, EA, PDS); community repositories (OpenTopography, Zenodo, Pangaea, DCDB for crowdsourced bathymetry)
- 50.4 Versioning: semantic versioning for products, per-tile change logs, supersession records (NBS), reproducible builds, content-addressed storage (Icechunk ⟨H⟩, LakeFS, DVC); dataset DOIs with versions (DataCite)
- 50.5 Provenance: W3C PROV, lineage in ISO 19115, STAC processing extension, pipeline manifests (PDAL JSON, Snakemake/Nextflow), container images, environment locks; audit trails for chart products (S-100 exchange sets)
- 50.6 Coordinate reference frames over time: archiving the geoid/transformation grids used; epochs; re-reduction of historical soundings (lead-line to modern datum; Ch. 72)
- 50.7 Legal/holding periods and retention schedules; hydrographic survey records as legal evidence; data sovereignty and where bits may live (Ch. 69)
- 50.8 Cost: storage classes (hot/cold/glacier), compression choices (lossless LAZ ~5–10×; LERC with declared error), what to downsample vs never; energy footprint
- 50.9 Rescue of historical data: smooth sheets, lead-line soundings, aerial film scans, SRTM tapes, early lidar — georeferencing and uncertainty assignment for legacy data
**Then & now.** Paper smooth sheets and field books (NOS archives) → magnetic tape (Landsat, SRTM) → NCEI/EROS digital archives → cloud object stores with versioned, content-addressed formats; the pattern of data lost at every transition.
**Software.** Open: BagIt tools, DVC, LakeFS, Icechunk, Git LFS, Zenodo/Pangaea workflows, Entwine/COPC for archive-friendly point clouds, ESIP/EarthCube tools; Closed: commercial DAM systems, cloud archive tiers, CARIS Bathy DataBASE.
**Standards & guides.** ISO 14721 (OAIS); ISO 16363 (trusted repositories); W3C PROV-O; DataCite metadata schema; FAIR principles; NOAA data management directives; NARA records schedules; IHO C-55 and DCDB contribution guidance; LAS/BAG as archival formats (Library of Congress sustainability pages).
**Key references.** CCSDS 650.0 (OAIS); Moreau & Groth 2013 (PROV); Wilkinson et al. 2016; Crosby, Arrowsmith & Nandigam 2020 (OpenTopography); Hare, Eakins & Amante 2011 (uncertainty of legacy soundings); Jakobsson et al. 2012 (IBCAO compilation provenance); Icechunk/Zarr v3 specifications (versioned cloud arrays).
**Pitfalls.** Keeping only the "final DEM"; vendor raw formats that no software reads in 10 years; DOIs that point to a landing page whose files changed; silent reprocessing under the same name; lost geoid grids making heights irreproducible.
**Key takeaways.** Archive the rawest data you can, in open formats, with fixity and provenance; version products explicitly; the cheapest storage is the one that avoids re-surveying.

### Chapter 51 — Finding the right data: catalogs, STAC, and search
**Scope.** How to discover what exists for an area, judge it quickly, and get it in a usable form.
**Sections.**
- 51.1 The discovery questions: where, when, what surface, what resolution/accuracy, what datum, what licence, what format, what cost; "best" is use-dependent (Ch. 3)
- 51.2 Catalogs and portals: USGS The National Map/3DEP and LidarExplorer; NOAA Digital Coast Data Access Viewer, NCEI bathymetry viewer, Bathymetric Data Viewer, NBS/BlueTopo; OpenTopography; NASA Earthdata (ICESat-2, GEDI, SRTM, NASADEM); ESA/Copernicus Data Space (Copernicus DEM); JAXA (AW3D30); DLR (TanDEM-X); national portals (UK EA/DEFRA survey, Netherlands AHN, swisstopo, LINZ Data Service, Geoscience Australia ELVIS, NRCan HRDEM, Spain PNOA, France RGE ALTI/LiDAR HD, Denmark, Finland, Norway Høydedata, Japan GSI); marine: EMODnet, GEBCO/DCDB, IHO DCDB, GMRT, Seabed 2030; cloud: AWS Open Data, Microsoft Planetary Computer, Google Earth Engine catalog ⟨H⟩, Source Cooperative
- 51.3 STAC: Items/Collections/Catalogs, STAC API (search by bbox/datetime/properties), extensions relevant to elevation (pointcloud, raster, projection, processing, file, scientific), static vs dynamic catalogs; the GCMD/CMR lineage ⟨H⟩; OGC API – Records/Features; CSW legacy
- 51.4 Search by quality: filtering by checkpoint accuracy, density, date, vertical datum — rarely possible today; proposals for quality-first catalogs; DEMIX-style tile rankings
- 51.5 Crowd and commercial: OpenStreetMap elevation-adjacent data, crowdsourced bathymetry (DCDB CSB), commercial DEMs (Maxar/Vricon, Airbus WorldDEM, Intermap NEXTMap, Fugro, NV5, Hexagon HxGN Content), elevation APIs (Google, Mapbox, Open-Elevation) and their hidden provenance
- 51.6 Access patterns: bulk download vs cloud-native range reads (COG/COPC/Zarr) vs tiles vs APIs; authentication, egress costs; keeping a local manifest of what you fetched (version, checksum, date)
- 51.7 Evaluating before downloading: previews, hillshade quicklooks, metadata forensics (Ch. 54), coverage/void maps
- 51.8 When nothing fits: commissioning a survey (Ch. 26) vs enhancing (Ch. 45) vs living with uncertainty
**Then & now.** Map libraries and agency indexes → FTP sites and clearinghouses (NSDI 1994 ⟨H⟩; GCMD ⟨H⟩) → web portals → API-first catalogs (STAC 2017–2021 ⟨H⟩, Earth Engine catalog ⟨H⟩) → cloud-native direct access.
**Software.** Open: pystac-client, stac-browser, STAC FastAPI, odc-stac, stackstac, GDAL /vsicurl, rasterio, PDAL (EPT/COPC readers), QGIS STAC plugin, OpenTopography API, Earth Engine Python API (free tier), wget/aria2; Closed: commercial portals, Esri Living Atlas, Planet/Maxar discovery APIs.
**Standards & guides.** STAC 1.0.0/1.1.0; OGC API – Records; OGC CSW 2.0.2 (legacy); ISO 19115; DCAT/GeoDCAT-AP; INSPIRE discovery services.
**Key references.** Hanson & Holmes (STAC spec); Gorelick et al. 2017 *RSE* (Earth Engine); Crosby et al. 2020 (OpenTopography); Nebert 2004 (SDI Cookbook); Goodchild, Fu & Rich 2007 (geoportals); Guth 2024 (DEMIX tile ranking as discovery aid).
**Pitfalls.** Using an elevation API without knowing which DEM answered; downloading a "1 m DEM" that is a resampled 10 m; mixing tiles from two 3DEP projects of different years without noticing; assuming the portal's "accuracy" field was independently tested; licence surprises (NC, share-alike) found after delivery.
**Key takeaways.** Search by use requirements, not by resolution alone; read the metadata and look at a hillshade before committing; record exactly what you obtained and from where.

---

## Part XI — Validation, quality, and judging data

### Chapter 52 — Ground truth and calibration/validation datasets
**Scope.** What counts as truth, how it is made, how it is validated, and how to use it to judge other data.
**Sections.**
- 52.1 Hierarchy of truth: nothing is true, some things are better measured — benchmarks and CORS (mm–cm), GNSS checkpoints (cm), total-station/levelled profiles, TLS reference surfaces, high-density lidar as reference for coarser DEMs, ICESat-2 ATL08/ATL03 and GEDI as global quasi-truth (with their own biases), MBES reference surfaces and patch-test sites, lead-line/diver measurements
- 52.2 Designing a checkpoint campaign: number (ASPRS Ed. 2: ≥30 per land-cover stratum; scaling by area), distribution (spatial spread, strata by slope/land cover), independence (different instrument, crew, epoch), occupation time and PPK/RTK protocols (NGS-58/59 heights), what to measure (hard flat open surfaces for NVA; vegetated for VVA), documentation
- 52.3 Reference surfaces and sites: airport runways, parking lots, calibration ranges (lidar boresight sites), hydrographic reference surfaces (NOAA FPM), Hydrographic Patch Test sites, geodetic test fields (ISPRS), Ohio State/other permanent sites, instrumented slopes/catchments
- 52.4 Global/semi-global validation datasets: ICESat-2 (ATL03/06/08), GEDI L2A, ICESat GLAS (historic), national GNSS benchmark databases (NGS OPUS shared solutions), DEMIX tile set and reference DEMs, OpenTopography high-res lidar as truth for global DEMs; bathymetry: IHO/NOAA reference surveys, MBES over SDB
- 52.5 Validating the validators: checkpoint uncertainty budgets (GNSS height σ 2–5 cm typical), datum/geoid consistency, antenna heights, time/epoch; when "truth" is worse than the product (modern lidar vs old benchmarks)
- 52.6 Vegetated and bathymetric truth problems: ground under canopy (probe vs lidar vs GNSS under trees), marsh surfaces, soft seafloor (what depth is "the bottom" for lead-line vs acoustic vs lidar); temporal mismatch (snow, tide, growth)
- 52.7 Benchmarks for algorithms vs datasets for products: ISPRS, DALES/OpenGF (Ch. 42), DEMIX (Ch. 55), SfM benchmark sets, MBES processing test data (Shallow Survey series)
- 52.8 Sharing and licensing truth data; checkpoint tables as mandatory deliverables; privacy of control locations (usually none)
**Then & now.** Levelled benchmarks and triangulation stations ⟨H⟩ → GPS campaigns (1990s) → CORS/OPUS (2000s) → spaceborne laser altimetry as near-global reference (ICESat 2003; ICESat-2 2018; GEDI 2019); ASPRS standards moved from NMAS 1947 ⟨H⟩ to NSSDA 1998 to ASPRS 2014/2023.
**Math.** Required N for a confidence interval on RMSE (chi-square); allowing for checkpoint error: σ²_obs = σ²_product + σ²_check; stratified estimation; outlier policy (3σ rule vs robust).
**Software.** Open: NGS OPUS (free service), RTKLIB, PDAL/xdem/CloudCompare for point-vs-surface checks, icepyx/SlideRule (ICESat-2), GEDI tools, QGIS; Closed: Trimble Business Center, Leica Infinity, TerraMatch/TerraScan control reports, CARIS/QPS reference-surface tools.
**Standards & guides.** ASPRS Positional Accuracy Standards Ed. 2 (2023) incl. checkpoint guidance; NSSDA (FGDC-STD-007.3-1998); NGS-58 (1997) and NGS-59 (2008); USGS LBS 2024 (checkpoint requirements); IHO S-44 Ed. 6.1.0 (reference surfaces, crosslines); NOAA FPM 2020/2023 (reference surface, patch test); ISO 19157 quality evaluation procedures.
**Key references.** Zilkoski, D'Onofrio & Frakes 1997 (NGS-58); Hodgson & Bresnahan 2004 *PE&RS* (lidar accuracy and checkpoint error); Höhle & Höhle 2009 *ISPRS J.* (robust accuracy measures); Neuenschwander et al. 2020 (ATL08 validation); Liu et al. 2021 (ICESat-2 for DEM validation); Guth et al. 2021; Bielski et al. 2024 (DEMIX); Hare, Eakins & Amante 2011; Dewberry 2012 (NEEA).
**Pitfalls.** Checkpoints collected by the same crew/instrument/epoch as the survey; all checkpoints on roads (then claiming vegetated accuracy); ICESat-2 used as truth under dense canopy without filtering; comparing lidar to benchmarks in NAVD88 realized with a different geoid; reporting RMSE from 8 points.
**Key takeaways.** Truth has an error budget — state it; independence and stratification matter more than count; a validation dataset's metadata must be as rigorous as the product's.

### Chapter 53 — Accuracy assessment and uncertainty quantification in practice
**Scope.** The procedures, statistics, and reporting language for saying how good an elevation product is — with the standards that define the words.
**Sections.**
- 53.1 Vocabulary (back to Ch. 5): accuracy vs precision vs uncertainty; absolute vs relative; horizontal vs vertical; RMSE, mean error (bias), standard deviation, MAE, NMAD, 95th percentile, LE95/CE90/CE95; "tested" vs "produced to meet" vs "compiled to meet" (NMAS/NSSDA language)
- 53.2 Standards and their test logic: NMAS 1947 ⟨H⟩ (90 % within ½ contour interval), NSSDA 1998 (RMSE × 1.96), ASPRS 2014 → Ed. 2 2023 (RMSE_v classes; NVA vs VVA, VVA at 95th percentile and not pass/fail; horizontal from RMSE_r; 3D accuracy), USGS LBS QLs, IHO S-44 Ed. 6 (TVU = √(a² + (b·d)²), THU, orders; feature detection), ICAO Annex 15 (eTOD accuracy/confidence per area), INSPIRE elevation quality
- 53.3 Procedures: checkpoint comparison (point-to-surface via TIN/bilinear), relative accuracy (swath-to-swath, intra-swath, crossline analysis), internal consistency (overlap statistics), systematic error detection (bias by strip, by scan angle, by time), outlier handling and reporting, strata by land cover/slope
- 53.4 Uncertainty budgets: component propagation (GNSS, IMU, ranging, boresight, lever arms, sound speed, tide, refraction, interpolation), TPU for hydrography (Hare 1995; CUBE inputs), lidar error models (Baltsavias 1999; Glennie 2007), SfM (James et al. 2017 precision maps), InSAR height error (HoA, coherence), DEM error surfaces (Wechsler 2007), Monte Carlo propagation to derivatives (slope, viewshed, floodplain)
- 53.5 Spatial structure of error: autocorrelation, variograms of residuals, slope/aspect dependence, resolution effects; why global RMSE understates local error
- 53.6 Reporting: ASPRS report template; per-stratum tables; maps of residuals; uncertainty rasters delivered as bands; confidence statements consistent with the test; what to do when the dataset fails
- 53.7 Beyond vertical: horizontal accuracy of DEMs (hard to test; edge-based methods), temporal accuracy, thematic accuracy of labels (Ch. 42), completeness (voids), logical consistency (hydro-connectivity)
- 53.8 Decision-oriented UQ: translating σ into probabilities for a threshold decision (will the keel clear? is the levee high enough? is the parcel in the floodplain?), expected loss, value of information for additional survey
**Then & now.** Contour-interval tests ⟨H⟩ → NSSDA RMSE → quality-level frameworks and stratified vegetated tests → delivered uncertainty rasters (BAG, S-102, TanDEM-X HEM) → probabilistic products and decision analytics.
**Math.** RMSE, bias, σ decomposition RMSE² = bias² + σ²; NMAD = 1.4826·median|ε − median ε|; percentile confidence intervals; S-44 TVU formula; variance propagation J Σ Jᵀ; Monte Carlo with spatially correlated fields (sequential Gaussian simulation); variogram fitting; chi-square test for RMSE claims.
**Software.** Open: xdem (error modelling, variograms, Monte Carlo), demcoreg, PDAL/lidR QC, CloudCompare, R gstat/geoR, QGIS, NOAA HydrOffice (QC Tools, free), MB-System crossline tools; Closed: TerraMatch/TerraScan reports, LP360 QA/QC, CARIS (TPU, crosslines), QPS Qimera (CUBE), ArcGIS, Global Mapper, GeoCue.
**Standards & guides.** ASPRS Positional Accuracy Standards for Digital Geospatial Data Ed. 2 (2023); NSSDA; USGS LBS 2024; IHO S-44 Ed. 6.1.0 and S-67 (mariners' guide to uncertainty); NOAA HSSD (current edition); ICAO Annex 15/Doc 10066; ISO 19157-1; JCGM 100 (GUM) and JCGM 101 (Monte Carlo); FEMA elevation guidelines (G&S).
**Key references.** Höhle & Höhle 2009; Hodgson & Bresnahan 2004; Wechsler 2007 *HESS*; Hare 1995 *Int. Hydrogr. Rev.* (TPU); Calder & Mayer 2003; Baltsavias 1999 *ISPRS J.*; Glennie 2007 *J. Appl. Geod.*; James, Robson & Smith 2017 *ESPL*; Fisher & Tate 2006 *Prog. Phys. Geogr.*; Hugonnet et al. 2022; Rolstad, Haug & Denby 2009 (spatially correlated error); ASPRS 2023.
**Pitfalls.** Treating RMSE as 95 % error; declaring VVA pass/fail; checkpoint-to-raster comparison with nearest-cell instead of interpolation (inflating error on slopes); mixing ellipsoidal checkpoints with orthometric DEM; propagating only random error; reporting a single number for a continent.
**Key takeaways.** Say which statistic, which standard, which checkpoints, which strata; deliver uncertainty spatially; the point of UQ is a defensible decision, not a number in a report.

### Chapter 54 — Evaluating other people's data when you lack the full story
**Scope.** Forensic assessment of DEMs, point clouds, and bathymetry delivered with thin or suspect metadata.
**Sections.**
- 54.1 Triage from the file alone: CRS and vertical reference sanity (values over the sea near 0? ±geoid offset ⇒ ellipsoidal heights; units feet vs meters; integer quantization; nodata values), pixel-is-area/point, tiling seams, compression artefacts, date clues in headers, software signatures
- 54.2 Hillshade and derivative sweeps: multi-azimuth hillshades, slope and curvature maps reveal interpolation ghosts, contour terraces, stripes, tile edges, ML "smearing", resampling blur, surface type (buildings present?), swath boresight errors (sawtooth), sonar refraction "smiles/frowns", heave artefacts, motion residuals
- 54.3 Internal consistency: flat-surface tests (lakes, runways, parking lots, reservoirs — slope and noise), lake-level consistency across tiles, road crown continuity, bridge treatment, water edge consistency, histogram of elevations for quantization, spectral analysis for effective resolution
- 54.4 External cross-checks: ICESat-2/GEDI, benchmarks (NGS datasheets), other DEMs over stable terrain (differencing with Nuth–Kääb co-registration), OSM features (roads/buildings), imagery for date and change, tide gauge/water-level for bathy
- 54.5 Inferring provenance: resolution and texture signatures of SRTM/ASTER/ALOS/TanDEM-X/lidar/SfM; chart-derived bathymetry (contour terraces, sounding density), SDB signatures; ML-corrected DEM artefacts
- 54.6 Judging claims: "accuracy 10 cm" without a test; vendor QC vs independent; sample size; extrapolation from checkpoints on roads; reading between the lines of a survey report; red flags list
- 54.7 Legal/contractual lens: specification compliance checklists (LBS, HSSD, S-44 orders), acceptance testing, independent QA/QC roles, rejecting deliverables
- 54.8 Writing a fitness-for-use memo: what it is, what it isn't, what you tested, what you'd need to trust it for use X; uncertainty inflation when unknown
**Then & now.** Trusting the agency stamp → NSSDA-era "tested to meet" → routine independent verification with spaceborne altimetry and open reference lidar; the rise of third-party DEM intercomparisons (DEMIX, 2020s).
**Math.** Quick statistics for flat-surface tests (σ, slope); spectral slope for effective resolution; registration shift estimation; sample-size reasoning for how much a small check can tell you.
**Software.** Open: GDAL/QGIS (hillshade, histograms), xdem, demcoreg, CloudCompare, PDAL, SlideRule/icepyx (ICESat-2 pulls), NOAA QC Tools, lasvalidate/pdal info, GMT; Closed: Global Mapper, ArcGIS, CARIS, QPS, TerraScan.
**Standards & guides.** ASPRS Ed. 2 (independent testing); USGS LBS acceptance criteria; NOAA HSSD/FPM (QC roles, crossline requirements); IHO S-44/S-67/CATZOC; ISO 19157 evaluation methods; ISO/IEC 17025 mindset (traceability).
**Key references.** Guth 2006 *PE&RS* (SRTM geomorphometric assessment); Hirt 2018 *Remote Sens.* (artefacts in DEMs); Polidori & El Hage 2020; Mesa-Mingorance & Ariza-López 2020 *Remote Sens.* (DEM accuracy assessment review); Guth et al. 2021; Bielski et al. 2024 (DEMIX); Hawker et al. 2019 *Front. Earth Sci.* (global DEM intercomparison); Hare et al. 2011; Oksanen & Sarjakoski 2005 (error propagation).
**Pitfalls.** Accepting a DEM because it "looks fine" at full extent; judging a DTM by a DSM's standards (or vice versa); testing only where it's easy; assuming newer = better; dismissing a good dataset because the metadata template was sloppy.
**Key takeaways.** Treat every delivered dataset as a hypothesis; a few well-chosen internal tests and one independent external source expose most problems; write down what you found and what you couldn't test.

### Chapter 55 — Public DEM and bathymetry products: catalog and comparison
**Scope.** The major freely available (and some commercial) elevation products: what they are, how they were made, how they compare, and when to use which.
**Sections.**
- 55.1 Global/near-global land DEMs: SRTM (v3/NASADEM; Feb 2000; C-band DSM; voids; 60°N–56°S), ASTER GDEM v3 (optical stereo; noisy; 83°), ALOS World 3D AW3D30 (v3/v4; PRISM stereo DSM), TanDEM-X 90 m/30 m and 12 m (X-band DSM; penetration; commercial for 12 m), Copernicus DEM GLO-30/GLO-90 (from TanDEM-X; edited; masks; best general-purpose DSM today; 2011–2015 dates), MERIT DEM (error-removed SRTM/AW3D), MERIT Hydro, FABDEM/FABDEM v1-2 (ML-removed forest/buildings; NC licence), DeltaDTM (coastal DTM), CoastalDEM (NC; ML), DiluviumDEM, GEDTM30 (2025), GMTED2010, GTOPO30 ⟨H⟩, ETOPO1/2022, GLO-30 vs NASADEM vs AW3D30 behaviour by land cover
- 55.2 Regional/national high-resolution: USGS 3DEP (lidar; QL1/QL2; 1 m DEMs; CoNED/CUDEM topobathy), Canada HRDEM, Mexico INEGI, UK EA 1 m/2 m composite and national lidar programme, Netherlands AHN1–AHN5 (the longest national lidar time series), Denmark DHM, Finland NLS, Norway Høydedata, Sweden, Switzerland swissALTI3D/swissSURFACE3D, Austria, Spain PNOA-LiDAR, France LiDAR HD/RGE ALTI, Italy, Poland ISOK, Estonia, Japan GSI 5 m/1 m, Australia ELVIS/Geoscience Australia 5 m & lidar, New Zealand LINZ lidar, Slovenia, Brazil, Argentina; ArcticDEM and REMA (2 m SfM strips/mosaics; time stamps; ellipsoidal heights)
- 55.3 Global bathymetry: GEBCO_2024 (15″; with TID), SRTM15+ V2 (gravity + soundings), ETOPO 2022, GMRT (MBES synthesis), EMODnet Bathymetry DTM (1/16′), IBCAO v5/IBCSO v2, Seabed 2030 progress metrics, BedMachine/Bedmap3 (sub-ice), NOAA NBS/BlueTopo (US; per-cell source/uncertainty), NCEI CUDEM tiles, national bathymetric portals (UKHO ADMIRALTY Marine Data Portal, Australia AusSeabed, NZ, Canada CHS NONNA, Japan), crowdsourced CSB (DCDB)
- 55.4 Spaceborne altimetry as products: ICESat-2 ATL06/08/13, GEDI L2/L3/L4, CryoSat-2, SWOT L2 (rivers/lakes), Sentinel-3/6 (inland water)
- 55.5 Commercial: Maxar Precision3D/Vricon (50 cm/3 m DSM/DTM), Airbus WorldDEM Neo (5 m), Intermap NEXTMap (IfSAR), Fugro/NV5/Hexagon lidar programs, Planet/Blackshark 3D, elevation-as-a-service APIs
- 55.6 Comparison framework (DEMIX-style): surface type (DSM/DTM/hybrid), nominal vs effective resolution, acquisition dates, vertical/horizontal datum (EGM96 vs EGM2008 vs ellipsoid; WGS 84 realizations), reported vs independent accuracy by land cover and slope, voids and fills, artefacts (stripes, terraces, penetration), licence (CC-BY, CC-BY-NC, public domain, custom), formats/tiling, uncertainty layers, update cadence; standardized tables in Appendix E
- 55.7 Fitness by use: flood modelling (DTM! FABDEM/DeltaDTM/national lidar), geomorphology (resolution and effective resolution), aviation (certified eTOD only), hydrography (never a global grid), telecommunications (DSM), coastal SLR (vertical accuracy & datum dominate), glaciology (time-stamped; penetration bias)
- 55.8 Known errata and quirks: SRTM edge overlap and EGM96; Copernicus DEM editing and water flattening; AW3D30 cloud/stripe masks; ASTER GDEM "mole runs"; TanDEM-X urban/forest penetration and HEM; MERIT's residual stripes; FABDEM over terraces/cliffs; GEBCO TID interpretation; ArcticDEM blunders and ellipsoidal heights
**Then & now.** GTOPO30 (1996) ⟨H⟩ → SRTM (2000, released 1″ globally 2014–15) → ASTER GDEM (2009) → TanDEM-X (2010–) → AW3D30 (2016) → Copernicus DEM (2019–2021) → ML-corrected DTMs (2018–2024) → GEBCO TID era (2019–) and Seabed 2030; from one global DEM to a crowded field where choice requires evaluation.
**Software.** Open: DEMIX tools (Guth MICRODEM, free), xdem, OpenTopography API, GEE, Planetary Computer; Closed: commercial product viewers.
**Standards & guides.** Product handbooks: Copernicus DEM Product Handbook; NASADEM/SRTM user guides; AW3D30 product description; TanDEM-X DEM product specification; GEBCO Cookbook (B-11) and TID definitions; NBS/BlueTopo spec; 3DEP product standards; ArcticDEM/REMA release notes; ICESat-2/GEDI ATBDs.
**Key references.** Farr et al. 2007 (SRTM); Crippen et al. 2016 (NASADEM); Abrams, Crippen & Fujisada 2020 (ASTER GDEM v3); Tadono et al. 2014/Takaku et al. 2020 (AW3D30); Rizzoli et al. 2017 (TanDEM-X DEM); Airbus/ESA Copernicus DEM handbook; Yamazaki et al. 2017 (MERIT); Hawker et al. 2022 (FABDEM); Pronk et al. 2024 (DeltaDTM); Kulp & Strauss 2018 (CoastalDEM); Porter et al. 2018/Howat et al. 2019 (ArcticDEM/REMA); GEBCO Compilation Group 2024; Tozer et al. 2019 (SRTM15+); Jakobsson et al. 2020/Dorschel et al. 2022 (IBCAO/IBCSO); Morlighem et al. 2017/2020 (BedMachine); Guth & Geoffroy 2021 *Trans. GIS*; Bielski et al. 2024; Hawker et al. 2019; Uuemaa et al. 2020 *Remote Sens.*; Purinton & Bookhagen 2021 *ESurf*.
**Pitfalls.** Calling Copernicus DEM a DTM; using FABDEM commercially; mixing EGM96 and EGM2008 products; using SRTM's 2000 date as "current"; GEBCO for anything navigational; ArcticDEM strips with unresolved vertical bias; believing "30 m" is comparable across products.
**Key takeaways.** No product is best everywhere — compare by land cover, slope, datum, date, and licence; read the handbook; test against ICESat-2 or lidar locally before trusting; the metadata/mask layers are part of the product.

### Chapter 56 — Case files: failures, surprises, and lessons
**Scope.** Short, sourced narratives where elevation/positioning data went wrong (or saved the day), each tied back to handbook chapters.
**Sections (each ≈ 1–2 pages: what happened, root cause, what would have caught it, chapters).**
- 56.1 USS *San Francisco* (2005) — grounding on an uncharted seamount; chart source data age and CATZOC-like confidence ⟨H⟩ (Ch. 20, 62, 70)
- 56.2 *Queen Elizabeth 2* (1992) — squat and charted depth at Vineyard Sound; vertical datum, uncertainty, and vessel dynamics (Ch. 9, 62)
- 56.3 Hurricane Katrina (2005) — subsided benchmarks and levee design heights (Ch. 38, 61)
- 56.4 Tōhoku (2011) — >5 m coordinate shift, national datum revision, harbour re-surveys (Ch. 39)
- 56.5 Kaikōura (2016) — coastal uplift of several metres, chart withdrawals, deformation-model patch (Ch. 39)
- 56.6 Mars Climate Orbiter (1999) — units; and terrestrial unit disasters (US survey foot vs international foot, 2022 deprecation) (Ch. 4, 47)
- 56.7 Grand Banks (1929) — cable breaks timing a turbidity current ⟨H⟩; seafloor processes as hazards (Ch. 39, 66)
- 56.8 Strava heatmap (2018) — fitness traces exposing bases; privacy and derived data (Ch. 69)
- 56.9 Border lines that move: Italy–Switzerland (Matterhorn glacier ridge), Italy–Austria; a boundary defined by a watershed on a melting glacier (Ch. 68, 40)
- 56.10 Oso landslide (2014) — lidar showed the history; who reads the DEM? (Ch. 39, 57)
- 56.11 Brumadinho (2019) — InSAR signals before dam failure; detection vs decision (Ch. 41, 65)
- 56.12 MH370 search — bathymetry gaps and the cost of mapping the unknown; Seabed 2030 (Ch. 2, 66)
- 56.13 SRTM/EGM96 vs ellipsoid mix-ups in flood maps; CoastalDEM vs SRTM sea-level exposure estimates (Kulp & Strauss 2019) (Ch. 9, 43, 61)
- 56.14 The 2 m FABDEM "terraces" and other ML artefacts in published analyses (Ch. 43, 45)
- 56.15 Bridge decks in DTMs blocking flood models; culverts missing (Ch. 32, 61)
- 56.16 Powerline clearance survey flown cold (Ch. 33)
- 56.17 Seasonal snow DEM used as bare earth; leaf-on vs leaf-off "growth" (Ch. 36)
- 56.18 Sonar sound-speed error producing "smiles" accepted into a chart (Ch. 20, 53)
- 56.19 GNSS jamming/spoofing in survey operations (Baltic/Black Sea reports) (Ch. 12, 69)
- 56.20 Historical: the Great Trigonometrical Survey's Everest height and refraction; Cassini vs Newton Earth shape debate (Ch. 72)
- 56.21 Half-pixel shifts, grid-vs-ground, and feet/meters in a single engineering project (Ch. 10, 31, 47)
- 56.22 Lidar deserts and equity: hazards unmapped where lidar isn't (Ch. 69, 73)
- 56.23 A successful catch: independent QC rejecting a lidar delivery with strip bias; what the process looked like (Ch. 53, 54)
**Key references.** Per case: US Navy JAGMAN investigation (2005); NTSB MAR-93/01 (QE2); Dixon et al. 2006; GSI 2011 notices; Hamling et al. 2017; Stephenson 1999 (MCO MIB); Heezen & Ewing 1952; Hern 2018 (Strava); Iverson et al. 2015; Gama et al. 2020 (Brumadinho InSAR); Picard et al. 2018 (MH370 bathymetry); Kulp & Strauss 2019 *Nat. Commun.*; Keay 2000 (Great Arc).
**Pitfalls.** Reading case files as "they were careless" rather than "the system allowed it"; forgetting that most failures combine a datum/metadata gap with a human assumption.
**Key takeaways.** Almost every disaster in this list had a data-quality signal available in advance; validation is cheap compared to the alternative; teach with cases.

---

## Part XII — Visualization and cartography

### Chapter 57 — Visualizing DEMs: shading, colormaps, filtering, rendering, point clouds, splats
**Scope.** Making terrain visible honestly — for analysis, QC, and communication — from hillshade to Gaussian splats.
**Sections.**
- 57.1 Purposes: exploration/QC (reveal artefacts), analysis (perceive form), communication (tell the truth attractively); each wants different choices
- 57.2 Relief shading: Lambertian hillshade (Horn 1981 gradients; azimuth/altitude conventions and the "inverted relief" illusion), multidirectional hillshade (Mark 1992; USGS/Esri MDOW), shadows, ambient occlusion, sky-view factor, openness (Yokoyama 2002), local relief model, slope/curvature shading, Red Relief Image Map (Chiba 2008), Swiss-style manual shading (Imhof) and learned shading (Eduard/Jenny 2021), aerial perspective, vertical exaggeration (declare it!)
- 57.3 Colormaps: perceptual uniformity (viridis, cividis, Crameri's batlow/oleron, cmocean topo/deep), hypsometric tints (Patterson & Jenny cross-blended), bathymetric conventions (chart blue tints; depth-area colouring; shoal-biased color breaks), rainbow/jet harm (false boundaries, colorblind failure), diverging maps for change (zero-centred), discrete vs continuous, lightness for luminance channels, dual encoding with hillshade (multiply vs HSV blends)
- 57.4 Filtering for display vs for analysis: Gaussian/median smoothing, feature-preserving filters, high-pass "detail" layers, de-striping, exaggeration of micro-topography (archaeology: RVT, LRM, SVF, openness blends), how display filters can hide or invent features
- 57.5 Contours and labels: interval choice by slope/resolution, smoothing, index contours, depression ticks (hachures), label placement; isobaths and generalization rules (shoal-biased)
- 57.6 3D rendering: perspective views, oblique flyovers, exaggeration, texture draping, LOD streaming (Cesium 3D Tiles, deck.gl TerrainLayer, MapLibre terrain), WebGL/WebGPU, lighting that lies (specular water)
- 57.7 Point clouds: EDL (eye-dome lighting), point size by density, colour by class/intensity/height/return/time/uncertainty, cross-sections and profiles as the main QC tool, Potree/COPC viewers, VR
- 57.8 Neural and splat rendering: NeRF/3D Gaussian splatting for visualization of SfM scenes — stunning, non-metric by default, no uncertainty; when to use (public engagement) and when not (measurement)
- 57.9 Visualizing uncertainty: transparency/fog, noise texture, side-by-side ensembles, hop/animated realizations, contour "bands", bivariate maps (elevation × uncertainty), confidence hatching on change maps (MacEachren 2005/2012)
- 57.10 Visualizing time: before/after swipes, DoD maps, 4D point clouds, animation; the tyranny of two-epoch stills
- 57.11 Accessibility and reproducibility: colorblind-safe palettes, tactile/3D-printed terrain, screen readers for charts, scripted figures
**Then & now.** Hachures (Lehmann 1799) ⟨H⟩ → hand-painted Swiss relief (Imhof) → analytical hillshade (Yoëli 1965) → GIS hillshade default → multi-technique archaeological visualizations (RVT 2011) → web 3D terrain → neural rendering (2020–).
**Math.** Gradient estimation (Horn 3×3), illumination I = cos θ with normal n and light vector l; sky-view factor and openness integrals; multiscale relief filters; perceptual colour spaces (CIELAB, CAM16) and lightness monotonicity.
**Software.** Open: GDAL (gdaldem), QGIS (hillshade, blending), Relief Visualization Toolbox (RVT), WhiteboxTools, SAGA, GRASS, Blender (GIS add-on; raytraced relief), Eduard (closed-source, paid), Potree, CloudCompare, Cesium (open core), deck.gl, MapLibre, three.js, matplotlib/cmcrameri/cmocean, gsplat/nerfstudio; Closed: ArcGIS Pro (multidirectional hillshade), Global Mapper, Surfer, Fledermaus, Terragen, Natural Scene Designer, Adobe Photoshop workflows.
**Standards & guides.** ISO 7154/charting conventions for depth tints (IHO S-4, S-52 presentation library); USGS topographic map symbol standards; cartographic colour guidance (ColorBrewer; Crameri 2020 misuse paper); WCAG for web maps.
**Key references.** Horn 1981 *Proc. IEEE*; Imhof 1982 *Cartographic Relief Presentation*; Yoëli 1965; Mark 1992 (multidirectional); Yokoyama, Shirasawa & Pike 2002 (openness); Zakšek, Oštir & Kokalj 2011 (SVF); Kokalj & Hesse 2017 (RVT/airborne laser scanning raster visualization); Chiba, Kaneta & Suzuki 2008 (RRIM); Patterson & Jenny 2011 *Cartogr. Perspect.* (hypsometric tints); Crameri, Shephard & Heron 2020 *Nat. Commun.*; Kovesi 2015; Thyng et al. 2016 (cmocean); Borland & Taylor 2007 (rainbow); MacEachren et al. 2005/2012; Jenny 2021 (Eduard/neural shading); Boucheny 2009 (EDL); Kerbl et al. 2023 (3DGS); Schütz 2016 (Potree).
**Pitfalls.** Hillshade from the south causing relief inversion; rainbow colormaps creating false terraces; forgetting to state vertical exaggeration; smoothing for display then analysing the smoothed grid; splat renderings mistaken for survey data; QC done only in 2D plan view (profiles catch what maps hide).
**Key takeaways.** Visualization is an analysis step with its own parameters — record them; use multiple techniques, perceptual colormaps, and cross-sections; show uncertainty and time, not just elevation.

### Chapter 58 — Making maps from elevation: topographic maps, charts, graticules, standard elements
**Scope.** From DEM to a finished topographic map or nautical chart: generalization, symbology, marginalia, and the standards that define them.
**Sections.**
- 58.1 Map purpose and scale: topographic (general), nautical (safety of navigation), aeronautical (obstacles, terrain), thematic (hazard, slope); scale → generalization → contour interval; "map accuracy" standards (NMAS 1947 ⟨H⟩: 90 % of contours within ½ interval; horizontal 1/30″ or 1/50″)
- 58.2 USGS topographic maps: the 7.5′ quadrangle series (1947–1992; HTMC scans), US Topo (2009–; GeoPDF from national datasets), what changed (field-checked vs database-derived; loss of some features), reading legacy sheets (datum NAD27 ⟨H⟩, NGVD29, declination), other national series (OS, IGN, swisstopo, GSI, LINZ Topo50)
- 58.3 Contours from DEMs: interval selection, smoothing/generalization, supplementary contours, depression contours, consistency with spot heights and hydrography, avoiding contour crossings and "staircase" artefacts; contour accuracy inherits DEM accuracy plus generalization
- 58.4 Nautical charts from bathymetry: soundings selection (shoal-biased, legibility), depth contours/areas, depth tints, generalization rules (IHO S-4), CATZOC/ZOC diagram, chart datum (LAT/MLLW), scale and compilation scale, ENC (S-57 → S-101) vs paper, overscale warnings; S-102 bathymetric surface overlays; source diagrams
- 58.5 Aeronautical: terrain and obstacle depiction (sectional charts; maximum elevation figures; MEF rounding rules), eTOD datasets and their accuracy areas, ICAO Annex 4
- 58.6 Graticule vs grid: latitude/longitude graticules, projected grids (UTM, MGRS, State Plane, national grids), grid-north/true-north/magnetic-north and the declination diagram (and its date), neatlines, corner coordinates, tick conventions; scale bars (projection-dependent), representative fraction, north arrows
- 58.7 Standard marginalia: title, series/sheet, edition/date, datum (horizontal and vertical!), projection, contour interval, sources and currency diagram, reliability/accuracy diagram, legend, adjoining sheets index, producer/licence; what modern web maps drop (and why that matters)
- 58.8 Layout and generalization: label placement, hydrography–contour consistency, road/building generalization at scale, spot heights selection, hypsometric tints and relief shading integration, marine/land seam on coastal maps
- 58.9 Web and dynamic maps: zoom-dependent generalization, vector tiles with terrain, legends that vanish, datum and date metadata hidden; printable outputs from web maps
- 58.10 Map QA: topological checks (contours don't cross), consistency checks (rivers flow downhill), accuracy statements, independent review
**Then & now.** Cassini/Ordnance Survey national surveys ⟨H⟩ → USGS quadrangles (1879–) ⟨H⟩ → photogrammetric compilation → DEM-derived US Topo and ENCs → continuous, database-driven cartography (S-101, vector tiles).
**Math.** Contour generation (marching squares); line generalization (Douglas–Peucker, Visvalingam) and positional error; scale factor and convergence angle for grid north; MEF computation rules; sounding selection as a constrained optimization.
**Software.** Open: QGIS (print layouts, graticules, contours), GDAL (gdal_contour), GRASS/SAGA, GMT (publication maps, graticules), Mapnik/MapServer, OpenCPN (chart display), S-57/S-101 tools (GDAL S57 driver, NOAA s100py); Closed: ArcGIS Pro (production mapping, maritime charting), CARIS S-57 Composer/HPD, dKart, SevenCs, Global Mapper, Avenza MAPublisher, Adobe Illustrator.
**Standards & guides.** USGS Standards for US Topo and historical map standards; NMAS 1947; IHO S-4 (chart specifications), S-52 (ECDIS presentation), S-57/S-101, S-102, S-67; ICAO Annex 4 (aeronautical charts) and Annex 15; FAA aeronautical chart users' guide; OS and IGN cartographic specifications; FGDC Digital Cartographic Standard for Geologic Map Symbolization (for relief/hypsometry conventions).
**Key references.** Imhof 1982; Robinson et al. 1995 *Elements of Cartography*; Monmonier 1996 *How to Lie with Maps*; Moore 2011 (US Topo); USGS US Topo product standards; Kraak & Ormeling 2020; Brewer 2015 *Designing Better Maps*; IHO S-4; Zoraster & Bayer 1993 (sounding selection); USGS 2015 *Topographic Mapping* history booklet; Snyder 1987 (projections for mapping) ⟨H⟩.
**Pitfalls.** Omitting vertical datum from a map that shows elevations; stale declination; grid north treated as true north; contour interval smaller than DEM accuracy justifies; chart generalization that is not shoal-biased; web maps with no edition date or source currency; mixing feet contours with metric spot heights.
**Key takeaways.** A map is a claim with marginalia as its evidence; generalize deliberately and safely (shoal-biased at sea); the graticule, grid, datum, and date are not decoration.

---

## Part XIII — Vectors, grids, and location codes

### Chapter 59 — Vector data and DEMs: points, lines, polygons, breaklines, contours, topology
**Scope.** How vector geometry interacts with continuous elevation — as input (breaklines, GCPs, shorelines), as output (contours, footprints), and as a source of error.
**Sections.**
- 59.1 Geometry types and their 3D semantics: points, multipoints, linestrings/polylines, polygons/multipolygons, rings and holes, Z and M values, 2.5D vs 3D vs solids; OGC Simple Features; GeoJSON (RFC 7946: WGS 84 only, third coordinate "undefined" vertical reference), shapefile limits (.prj without vertical CRS, 2 GB, field names), GeoPackage/GeoParquet/FlatGeobuf; CAD (DXF/LandXML: no CRS, local grids)
- 59.2 Breaklines and mass points: hard vs soft breaklines, hydro-flattening and hydro-enforcement breaklines (LBS), ridge/drain lines, roads and curbs, their collection cost and their effect on TINs/grids; breaklines from imagery vs lidar
- 59.3 Contours as data: digitized historical contours → DEMs (ANUDEM; stair-step artefacts), contour accuracy vs DEM accuracy, contours as a legal product (some jurisdictions), round-trip losses (DEM → contours → DEM)
- 59.4 Shorelines and water polygons: NOAA CUSP, NHD/NHDPlus HR, OSM coastlines, GSHHG; tidal reference of each; polygon vs raster water masks; shoreline as a vector contract for DEM products (Ch. 34)
- 59.5 Footprints and obstacles: building footprints (Microsoft/Google/OSM) and roof heights, obstacle points (FAA DOF), wires as polylines with sag; "which point of the footprint has the height?"
- 59.6 Ground control points and checkpoints as vectors: schemas (ID, XYZ, σ, datum, epoch, description, photos), exchange formats (CSV with CRS!, GeoPackage), GCP marking in SfM, target design and visibility
- 59.7 Topology and consistency: contours that cross, polygons that self-intersect, rivers flowing uphill, roads under buildings (Ch. 63), overlapping footprints, bridges as lines over polygons; topological checks as DEM QC
- 59.8 Operations: draping vectors on DEMs (sampling method matters), profile extraction, 3D length and surface area (Jenness 2004), slope-aware buffering, vector-to-raster rasterization rules (all-touched, centre, area-weighted), raster-to-vector artefacts
- 59.9 Generalization: Douglas–Peucker, Visvalingam–Whyatt, topology-preserving simplification; implications for areas, lengths, and derived elevations
- 59.10 Vector tiles and 3D vector formats (3D Tiles vector, CityJSON, glTF); vertical CRS loss in web delivery
**Then & now.** Coverage/topological models (ARC/INFO 1982 ⟨H⟩) → shapefile (1998) ⟨H⟩ → OGC Simple Features (1999) → GeoJSON (2008/2016 RFC) → GeoPackage (2014) → cloud-native GeoParquet (2022–); Z handling remained an afterthought throughout.
**Math.** Point-in-polygon, line simplification tolerance → positional error; Delaunay with constraints; 3D length/area from DEM; rasterization sampling bias.
**Software.** Open: GDAL/OGR, GEOS/Shapely, PostGIS, QGIS, GeoPandas, JTS, tippecanoe, pyproj, PDAL (breakline tools), WhiteboxTools, GRASS v.* modules; Closed: ArcGIS (topology, Terrain datasets), FME, Global Mapper, Bentley, AutoCAD Civil 3D, TerraModeler.
**Standards & guides.** OGC Simple Features (ISO 19125); RFC 7946 (GeoJSON); OGC GeoPackage 1.4; GeoParquet 1.1; Esri Shapefile technical description (1998); USGS LBS (breakline and hydro-flattening requirements); FGDC shoreline metadata profile; LandXML 1.2.
**Key references.** Douglas & Peucker 1973; Visvalingam & Whyatt 1993; Jenness 2004 *Wildl. Soc. Bull.* (surface area); Hutchinson 1989; Butler et al. 2016 (RFC 7946); Egenhofer & Franzosa 1991 (topological relations); Goodchild & Hunter 1997 (positional accuracy of lines); Li, Ma & Di 2002 (shoreline).
**Pitfalls.** GeoJSON Z values assumed orthometric; shapefile with no vertical datum; breaklines from a different epoch than the lidar; contour intervals finer than the data; draping a 2D road onto a DSM and reporting a bridge as a hill; rasterization rule changing a footprint's area by 20 %.
**Key takeaways.** Vectors carry elevation semantics too — define Z's datum and meaning; breaklines and shorelines are inputs that shape the DEM, so version them; topology checks are DEM checks.

### Chapter 60 — Discrete global grids and location codes: S2, H3, geohash, plus codes, what3words, MGRS
**Scope.** Cell-based and code-based ways to name places, how they interact with elevation data, and the traps in each scheme.
**Sections.**
- 60.1 Why DGGS: equal-area/consistent-area analysis, hierarchical aggregation, indexing/joins at scale, tiling for cloud-native data; OGC Abstract Specification Topic 21 (DGGS)
- 60.2 S2 (Google): cube-face projection, Hilbert-curve cell IDs ⟨H⟩, levels 0–30 (~85 km² face to <1 cm²), exact hierarchy (parent contains children), cell shapes vary in area (~2× ) across a face, coverings for regions; use in indexing point clouds and DEM tiles
- 60.3 H3 (Uber): icosahedron, aperture-7 hexagons, resolutions 0–15, 12 pentagons per resolution, approximate hierarchy (a child is not fully contained in its parent — small boundary leakage), cell area varies with position (roughly up to ~2× between smallest and largest hexagons at a given resolution), neighbour uniformity benefits for flow/raster-like analysis; pitfalls for aggregation across resolutions
- 60.4 Other DGGS: rHEALPix, ISEA3H/ISEA4T (DGGRID), HEALPix (astronomy; equal area), OpenEAGGR, Geohash (Z-order on lat/lon rectangles; boundary and pole distortions), quadkeys/XYZ tiles (Web Mercator; area distortion toward poles; no pole coverage), GeoSOT, A5; equal-area vs equal-shape trade-offs
- 60.5 Location codes for humans: MGRS/USNG (UTM-based; zone boundaries; precision by digits), plus codes/Open Location Code (open, offline, grid-based) ⟨H⟩, what3words (closed, proprietary, homophone collisions, no hierarchy), Maidenhead, Natural Area Coding; emergency-services considerations
- 60.6 Elevation in DGGS: cell-aggregated elevation statistics (mean/min/max/σ), resolution matching DEM to cell size (no false precision), slope/aspect in hex grids, hydrology on hex grids, 3D DGGS (voxel extensions), time in DGGS
- 60.7 Converting between systems: lossy nature of raster→DGGS→raster; area-weighted reprojection; cell-boundary artefacts; H3 non-containment causing double counting in hierarchical sums
- 60.8 Issues with special coding schemes: ambiguity (letter/digit confusions in MGRS/plus codes), truncation semantics, datum assumptions (all assume WGS 84 — which realization?), vertical absent in nearly all schemes, legal/ownership status, longevity risk of proprietary schemes
- 60.9 Choosing: indexing (S2/H3/geohash), analysis (equal-area DGGS; H3 with caveats), human communication (MGRS/plus codes), tiling for distribution (XYZ/COG tiling vs DGGS)
**Then & now.** Military grid systems (UTM/MGRS 1940s–) → quadtree indexing ⟨H⟩ → Geohash (2008) → S2 (open-sourced 2017) ⟨H⟩ → H3 (2018) → OGC DGGS standardization (2017; API 2020s); plus codes 2014 ⟨H⟩.
**Math.** Hilbert/Morton curve mapping; S2 cell geometry (cube face quadratic projection); H3 aperture-7 rotation and non-containment; equal-area projections underlying ISEA; area distortion of Web Mercator ∝ sec²φ; precision per code length.
**Software.** Open: s2geometry (and bindings), h3 (and bindings; h3-pandas), DGGRID, rHEALPix, geohash libs, open-location-code, mgrs libs, pyproj, DuckDB spatial (H3/S2 extensions), BigQuery/PostGIS extensions; Closed: what3words API, commercial DGGS platforms.
**Standards & guides.** OGC Topic 21 (DGGS) and OGC API – DGGS (draft); NGA MGRS/USNG standard (FGDC-STD-011-2001); Open Location Code spec; H3 documentation; S2 documentation.
**Key references.** Sahr, White & Kimerling 2003 *Cartogr. Geogr. Inf. Sci.* (DGGS); Purss et al. 2016/2019 (OGC DGGS); Veach et al. (S2 docs); Brodsky 2018 (H3); Open Location Code technical overview (Google, 2014; verify author); Bondaruk, Roberts & Robertson 2020 (DGGS review); Kmoch et al. 2022 *Big Earth Data*; Gibb 2016 (rHEALPix); Mahdavi-Amiri, Alderson & Samavati 2015 (survey).
**Pitfalls.** Summing H3 children and comparing to parents; Web Mercator tiles used for area statistics; MGRS zone-boundary mistakes; a DEM resampled to hexagons then differentiated; emergency responders handed a what3words address with a transposed word; assuming a code encodes a datum/epoch.
**Key takeaways.** DGGS and codes are indexes, not measurements; match cell size to data resolution; know each scheme's geometry quirks before aggregating or differencing elevation on it.

---

## Part XIV — Domain deep dives

### Chapter 61 — Hydrologic and hydraulic modeling constraints
**Scope.** What flood, drainage, and watershed models demand from elevation data — and the artefacts that ruin them.
**Sections.**
- 61.1 Model families: 1D/2D/coupled hydraulics (HEC-RAS, LISFLOOD-FP, TUFLOW, MIKE, Delft3D, SFINCS), hydrology (SWAT, HEC-HMS, WRF-Hydro), terrain-only proxies (HAND, geomorphic floodplains); each has a DEM resolution/accuracy sweet spot
- 61.2 DTM, not DSM: vegetation and buildings as false barriers; building representation choices (block-out, porosity, roughness); bridge decks and culverts (hydro-enforcement), levees and walls (thin features lost at coarse resolution; breaklines), roads as dams
- 61.3 Hydro-conditioning vs hydro-flattening vs hydro-enforcement (Ch. 34): sink filling vs breaching, stream burning, priority-flood, flow direction algorithms (D8, D∞, MFD) and their resolution sensitivity; flow accumulation thresholds for channel initiation
- 61.4 Bathymetry under the water: channel geometry missing from lidar (hydro-flattened), synthetic channels (conveyance-based), green lidar/ADCP/sonar river bathymetry, reservoir bathymetry for storage curves
- 61.5 Vertical accuracy → inundation error: sensitivity (σ_z of 0.5 m can move a flood edge 100s of m on flat terrain), uncertainty propagation (Monte Carlo DEM realizations), global flood maps built on SRTM vs FABDEM vs lidar (Hawker 2018; Sampson 2015), coastal SLR exposure and DEM choice (Kulp & Strauss 2019; Gesch 2018 "minimum threshold")
- 61.6 Regulatory uses: FEMA NFIP flood insurance rate maps (Guidelines & Standards, elevation requirements, BFE), EU Floods Directive, levee certification (USACE), dam safety; what accuracy the rules require and how they're tested
- 61.7 Terrain indices and their resolution dependence: TWI, stream power, HAND, slope length; catchment delineation differences across DEMs
- 61.8 Urban drainage: curbs, inlets, underpasses (true 3D), sub-grid representation, 1D sewer–2D surface coupling; data needs beyond a DTM
- 61.9 Data gaps that matter most: culverts and bridges, levee crests, channel bathymetry, tidal boundary datums, floodplain vegetation roughness (from the same lidar)
**Then & now.** Contour-derived DEMs and 1D cross-sections (1980s–90s) → SRTM-based global models (2010s) → lidar DTMs with hydro-enforcement, FABDEM-class corrected DTMs, and probabilistic flood maps.
**Math.** Shallow-water equations (brief) and their dependence on bed elevation; D8/D∞ flow routing; priority-flood algorithm; TWI = ln(a / tan β); error propagation of inundation extent with correlated DEM error.
**Software.** Open: HEC-RAS (free, closed-source), LISFLOOD-FP, SFINCS, TauDEM, WhiteboxTools, RichDEM, pysheds, GRASS r.watershed/r.stream.*, SAGA, HAND tools (GeoFlood), ANUGA; Closed: TUFLOW, MIKE+, InfoWorks ICM, Delft3D FM (open core), Flood Modeller, ArcHydro.
**Standards & guides.** FEMA Guidelines and Standards for Flood Risk Analysis and Mapping (elevation guidance); USACE EM 1110-2-1619 and levee guidance; USGS LBS (hydro-flattening/breaklines); EU Floods Directive technical guidance; EA (UK) LiDAR for flood modelling guidance; ASFPM recommendations.
**Key references.** Horritt & Bates 2001/2002; Bates & De Roo 2000; Sampson et al. 2015 *WRR*; Hawker et al. 2018 *Front. Earth Sci.*; Hawker et al. 2022; Nobre et al. 2011 (HAND); Barnes, Lehman & Mulla 2014 (priority-flood); Tarboton 1997 (D∞); Lindsay 2016 (breaching); Wechsler 2007; Gesch 2018 *Front. Earth Sci.*; Kulp & Strauss 2019; Schumann & Bates 2018 (the need for a high-accuracy open DEM); Poppenga & Worstell 2016 (hydro-enforcement).
**Pitfalls.** Running a flood model on a DSM (or on Copernicus DEM assuming DTM); filled sinks that were real detention basins; a bridge deck blocking a river; levee lost at 10 m; tidal boundary in the wrong datum; reporting a deterministic flood edge from a DEM with 1 m σ.
**Key takeaways.** Hydraulics needs a bare-earth, hydro-enforced, thin-feature-preserving DTM with known uncertainty; propagate elevation error to inundation; the smallest features (culverts, levees) control the biggest outcomes.

### Chapter 62 — Navigation and charting from elevation: marine, aviation, drones, vehicles, robots
**Scope.** Safety-critical uses where the shoalest point, the highest obstacle, or the nearest wall matters more than the mean.
**Sections.**
- 62.1 Marine: nautical charts and ENCs (S-57/S-101), chart datum (LAT/MLLW), under-keel clearance and squat, dynamic UKC with S-102/S-104 (water level)/S-111 (currents), CATZOC and S-67 uncertainty for mariners, shoal-biased gridding and sounding selection, feature detection requirements (S-44 orders; 1 m/2 m cubic features), survey currency and notices to mariners, port surveys and dredging, autonomous surface vessels and the "chart as sensor"
- 62.2 Aviation: terrain and obstacle data (ICAO Annex 15 eTOD areas 1–4 and their accuracy/resolution/confidence; DO-276/ED-98 and DO-200B data quality), TAWS/EGPWS terrain databases, minimum safe altitudes, obstacle surveys (FAA AC 150/5300-18; Part 77 imaginary surfaces), helicopter and low-level routes, vertical datum (MSL/EGM96 vs ellipsoid), currency and change notification
- 62.3 Drones/UAS: AGL rules (Part 107 400 ft AGL — relative to what surface?), terrain-following, geofencing with DSM vs DTM, UTM/U-space terrain services, obstacle detection vs stored obstacles, BVLOS risk models needing DSM + wires (Ch. 33)
- 62.4 Ground vehicles: HD maps (lane-level, slope/bank for ADAS), road grade for energy/efficiency, localization against lidar maps (SLAM; Ch. 15), tunnels/underpasses (multi-level roads; Ch. 63), construction change
- 62.5 Robots and off-road: elevation maps/2.5D traversability (GridMap, OctoMap), Mars rovers (TRN on Mars 2020 using orbital DEMs; Ch. 67), legged robots, planetary landers; latency, uncertainty-aware planning
- 62.6 Terrain-referenced navigation (TERCOM/TRN) and bathymetric navigation for AUVs — DEM quality as a navigation sensor's error budget
- 62.7 Liability and certification: who certifies the data (hydrographic offices, AIS/AIP providers), chain of custody, DO-200B processing standards, safety cases, and the role of uncertainty in go/no-go decisions
- 62.8 Object/transient handling in navigation products: wrecks, obstructions, moored structures, offshore wind farms, construction cranes; update cycles
**Then & now.** Lead-line charts and visual pilotage ⟨H⟩ → MBES and ENC (1990s–) ⟨H⟩ → S-100 dynamic products (2020s); aviation: paper sectionals → EGPWS databases (1996) → eTOD; robotics: Mars TRN 2021.
**Math.** UKC budget: available depth = charted depth + tide − (draft + squat + heel + uncertainty allowance); S-44 TVU as the uncertainty term; obstacle clearance surfaces geometry; probability of grounding given depth uncertainty; terrain-referenced navigation as a matching problem.
**Software.** Open: OpenCPN, GDAL S-57, NOAA s100py, OctoMap/GridMap/elevation_mapping (ROS), ArduPilot/PX4 terrain following; Closed: ECDIS systems, CARIS, QPS, Jeppesen/Honeywell terrain DBs, Lufthansa Systems, HERE/TomTom HD maps, Trimble/Topcon machine control.
**Standards & guides.** IHO S-44 Ed. 6.1.0, S-57, S-101, S-102 Ed. 3, S-104, S-111, S-67, S-4, S-52; NOAA HSSD (current) and FPM; ICAO Annex 15, Annex 4, Doc 10066 (PANS-AIM), Doc 9881 (eTOD guidelines); RTCA DO-276C/EUROCAE ED-98D, DO-200B/ED-76A; FAA AC 150/5300-18; 14 CFR Part 77 and Part 107; ISO 26262/UL 4600 (automotive safety, map data).
**Key references.** IHO S-44 (2020/2022); Calder & Wells 2007 (CUBE for charts); PIANC WG 121 (2014) harbour approach channels design guidelines (UKC); ICAO Doc 9881; Johnson et al. 2022 (Mars 2020 TRN); Fankhauser & Hutter 2016 (GridMap); Hornung et al. 2013; Thrun, Burgard & Fox 2005 (probabilistic robotics); Golden 1980 (TERCOM); NTSB/JAGMAN case reports (Ch. 56).
**Pitfalls.** Mean-gridded bathymetry in a chart product; DTM-based AGL geofence over a forest; obstacle databases missing new cranes/turbines; EGM96-referenced aviation data vs ellipsoidal GPS altitude; HD maps not updated for construction; UKC computed with charted depth but no uncertainty.
**Key takeaways.** Navigation products encode a worst-case philosophy (shoalest/highest) and an explicit uncertainty — never substitute a general-purpose DEM; currency and certified lineage are part of safety.

### Chapter 63 — Buildings, cities, and innerspace
**Scope.** The built environment: how buildings and infrastructure are defined, modelled, and removed; multi-level and indoor spaces that break the 2.5D assumption.
**Sections.**
- 63.1 What is a building? Footprint definitions (roof outline vs wall base vs cadastral), minimum sizes, attached structures, carports, greenhouses, ruins, under construction; height references (Biljecki et al. 2016: eave, ridge, mean roof, percentile heights; LoD0–LoD3 CityGML and LoD1.x/2.x refinements), roof shapes
- 63.2 City models: CityGML/CityJSON, 3D BAG (Netherlands), swissBUILDINGS3D, LoD2 national programs (Germany), Google/Apple photogrammetric meshes, OSM building:levels; generating LoD1/2 from lidar + footprints (3dfier, City3D); mesh vs semantic models
- 63.3 DSM→DTM in cities (Ch. 32): courtyard interpolation, terraces and retaining walls, sunken roads, elevated roads/rail, podiums; "ground" under a building (slab vs natural ground vs basement) — spec definitions vs practice
- 63.4 Roads crossing and under buildings: multi-level intersections, tunnels, covered roads, buildings over roads (air rights), parking structures — multi-valued surfaces; representing with network Z-levels (OSM layer/level tags), 3D road models, and separate DTM/DSM/"navigable surface" layers
- 63.5 Innerspace: indoor mapping (SLAM, mobile mappers; Ch. 15), IndoorGML and IFC/BIM, floor/level semantics, indoor–outdoor registration (door thresholds, GNSS-denied), underground utilities and ASCE 38-22 quality levels, mines and caves (Ch. 65/66), subsurface voxel models
- 63.6 Urban dynamics: construction/demolition detection, crane and scaffold transients (Ch. 27), temporary structures (markets, stadium stands), solar panels and rooftop equipment (count as building height?), green roofs, antennas (Ch. 33)
- 63.7 Urban applications and their surface requirements: solar potential (DSM with panels/trees), wind/CFD (DSM + roughness), noise (DTM + buildings as barriers), 5G/RF planning (DSM; clutter classes), shadow/sunlight rights, flood (DTM + building blocks), viewsheds/skylines, population/volume estimation, urban heat
- 63.8 Privacy and security in city models (Ch. 69): façade detail, interiors, sensitive sites; licensing of national 3D models
- 63.9 Validation of city models: height accuracy per building, footprint completeness/commission, LoD compliance (val3dity), temporal currency
**Then & now.** Fire-insurance maps and building outlines (Sanborn) → photogrammetric city models (1990s) → lidar LoD1/2 at national scale (2010s) → photogrammetric meshes and digital twins (2020s); indoor mapping from CAD plans to SLAM.
**Math.** Roof-plane fitting (RANSAC), height percentiles, volume from LoD1 blocks and its sensitivity to height reference; 3D topological validity (val3dity rules); multi-valued surface representation via layered grids.
**Software.** Open: 3dfier, City3D, CityJSON tools (cjio), val3dity, 3D BAG pipeline, PDAL/lidR building tools, QGIS 3D, Blender-GIS, IndoorGML tools, OSM tooling; Closed: Esri 3D Basemaps/City Engine, Bentley ContextCapture/OpenCities, Trimble SketchUp/eCognition, virtualcitySYSTEMS, Cyclomedia, Google/Apple 3D.
**Standards & guides.** OGC CityGML 3.0 / CityJSON 2.0; OGC IndoorGML 2.0; ISO 16739 (IFC); ASCE 38-22 (utility quality levels); national LoD2 specifications (AdV Germany, Kadaster NL); USGS LBS (building classification); ISO 19152 (LADM) for 3D cadastre.
**Key references.** Biljecki, Ledoux & Stoter 2016 *Comput. Environ. Urban Syst.* (height references/LoD); Biljecki et al. 2015 (applications of 3D city models); Ledoux et al. 2021 (3D BAG); Haala & Kada 2010 *ISPRS J.* (building reconstruction review); Gröger & Plümer 2012 (CityGML); Peters et al. 2022 (3D BAG automation); Zlatanova et al. 2013 (indoor); Kang & Li 2017 (IndoorGML).
**Pitfalls.** Comparing building heights with different reference points; a "DTM" that keeps podium levels; roads under buildings vanishing from both DTM and DSM; indoor maps with no vertical datum tie; counting rooftop PV as height change; LoD1 volumes used for energy models with ±30 % error.
**Key takeaways.** Define "building" and "ground" per product; cities are inherently 3D/multi-level — keep separate layers rather than forcing one surface; validate heights per object against the stated reference.

### Chapter 64 — Agriculture, forests, wetlands, and the living surface
**Scope.** Surfaces that grow, flood, and breathe: what elevation means there and how to measure it.
**Sections.**
- 64.1 Forests: canopy height models (DSM − DTM), penetration by sensor (lidar best; X/C-band SAR partial; optical none), ground under canopy and the leaf-off requirement, understory, biomass and structure (GEDI, ICESat-2, Biomass P-band), forest DTM errors by density and slope, ML "forest removal" products (FABDEM) vs measured DTMs
- 64.2 Croplands: seasonal canopy (0–3 m), tillage and furrows (10–30 cm micro-relief), land levelling and terraces, drainage tiles, irrigation furrow design (cm-level RTK), precision agriculture DEM needs, "bare earth" definition during crop season; UAV SfM for crop height; soil erosion by DoD
- 64.3 Grasslands, shrub, tundra: grass height bias in lidar DTMs (5–30 cm), seasonal thaw/heave, permafrost thermokarst
- 64.4 Wetlands and marshes: lidar positive bias in dense marsh vegetation (decimeters; Hladik & Alber 2012), correction methods, tidal datum conversions, marsh elevation capital and SLR vulnerability, mangroves (SRTM bias of meters), peatlands and "bog breathing" (seasonal cm surface oscillation), GNSS-RTK transects as truth, SET tables
- 64.5 Floodplain vegetation roughness from lidar; riparian canopy and shoreline extraction (Ch. 34)
- 64.6 Snow/ice as a seasonal surface (Ch. 36) and ASO-style snow depth from repeat lidar
- 64.7 Temporal design: phenology calendars, multi-season acquisitions, consistent definitions across epochs; separating growth from ground change
- 64.8 Products and benchmarks: GEDI L2A/L4, ICESat-2 ATL08, GLAD canopy height, Meta/WRI 1 m canopy height (ML; validation caveats), national forest inventories with lidar, marsh elevation datasets (USGS), NEON
**Then & now.** Field plots and clinometers → airborne lidar forestry (1990s–) → spaceborne lidar (GLAS 2003; GEDI/ICESat-2 2018–) → ML canopy height maps (2020s) whose validation is the open question.
**Math.** CHM = DSM − DTM and its error (both terms uncertain); percentile metrics (p95, cover); penetration models; marsh bias correction regressions; seasonal signal decomposition.
**Software.** Open: lidR, PDAL, FUSION (free), CloudCompare, GEDI/ICESat-2 toolkits (rGEDI, icepyx, SlideRule), WhiteboxTools, QGIS; Closed: TerraScan, LP360, ArcGIS, Trimble eCognition, agricultural RTK design suites (Trimble/Topcon land levelling).
**Standards & guides.** USGS LBS (leaf-off, vegetated accuracy VVA); ASPRS Ed. 2 (VVA); NEON AOP protocols; FAO/IPCC guidance using canopy height; USDA NRCS land-levelling specs; Ramsar wetland mapping guidance.
**Key references.** Hodgson & Bresnahan 2004; Hladik & Alber 2012 *RSE*; Rogers et al. 2018 (marsh lidar correction); Simard et al. 2019 (mangrove height); Dubayah et al. 2020 (GEDI); Potapov et al. 2021 (GLAD canopy height); Tolan et al. 2024 (1 m canopy height; and its critiques); Lang et al. 2023 (global canopy height); Painter et al. 2016 (ASO); Alshammari et al. 2020 (peat bog breathing); Næsset 2002 (area-based lidar forestry).
**Pitfalls.** Leaf-on lidar DTMs under dense canopy; using FABDEM over mangroves/marsh; crop-season "bare earth"; comparing canopy heights from different percentile definitions; believing 1 m ML canopy height has 1 m accuracy; forgetting grass height bias in cm-level change studies.
**Key takeaways.** The living surface has a season and a bias; design acquisitions by phenology; report bias by vegetation class; treat ML vegetation products as priors, not measurements.

### Chapter 65 — Mining, landfills, construction, and engineered earthworks
**Scope.** Volumes, cut/fill, stockpiles, pits, dumps, and the legal/economic weight of a cubic metre.
**Sections.**
- 65.1 Volume computation: grid/TIN prism methods, cut/fill between surfaces, base-surface definition (the biggest uncertainty), toe lines, stockpile delineation, correlated error and volume uncertainty (Ch. 40 math), density/tonnage conversion
- 65.2 Survey methods and cadence: UAV SfM (daily/weekly; GCPs vs RTK/PPK; doming), terrestrial scanners, mobile mapping, machine-control GNSS "as-built" surfaces, satellite stereo for remote sites, InSAR for subsidence and tailings dams (Brumadinho; Ch. 56)
- 65.3 Standards and legal: surveyor licensure and stamped volumes, JORC/NI 43-101 reporting, landfill airspace and regulatory capacity reports, mine reclamation bonds, construction pay quantities (grid-vs-ground, units, rounding), dispute resolution with independent surveys
- 65.4 Landfills and dumps: continuous change, settlement and gas, cover vs waste, scavenging activity, illegal dumping detection via DoD, fires (Ch. 27), trash piles as transient objects in DSMs
- 65.5 Construction sites: daily change, cranes/scaffolds/equipment as transients, design surface vs as-built, BIM-to-field (IFC alignment), tolerance checks, machine-control models (LandXML/TIN), earthwork balancing
- 65.6 Open pits, quarries, underground: pit wall monitoring (slope radar, TLS), highwall change, dewatering subsidence, underground SLAM/cavity scanners, stope volumes, cave surveys
- 65.7 Tailings and dams: freeboard, crest elevation monitoring, deformation (InSAR, GNSS), GISTM requirements; dam safety surveys
- 65.8 Reclamation and post-mining landscapes: geomorphic reclamation design (GeoFluv), long-term erosion monitoring, "approximate original contour"
- 65.9 Pitfalls particular to engineered surfaces: vertical walls and overhangs in 2.5D, vehicles on stockpiles, wet vs dry material heights, dust/steam, dynamic water in pits
**Then & now.** Chain-and-level cross-sections and planimeter areas → total stations and GNSS → UAV photogrammetry revolution (2013–) → continuous monitoring (fixed scanners, InSAR, machine control).
**Math.** Volume by prisms V = Σ A_i·(z_top − z_base); end-area method; propagation with spatial correlation; sensitivity to base surface; tonnage uncertainty; doming error models in SfM (James & Robson 2014).
**Software.** Open: CloudCompare (volume), QGIS/GRASS r.volume, WhiteboxTools, OpenDroneMap/WebODM, MicMac, PDAL; Closed: Propeller, Pix4D, Agisoft Metashape, Trimble Business Center/SiteVision, Carlson, Maptek PointStudio/Vulcan, Leica Cyclone, Bentley, DJI Terra, Kespry.
**Standards & guides.** JORC Code (2012); CIM/NI 43-101; US EPA landfill (40 CFR 258) reporting; ASPRS UAS guidelines; state surveyor licensing rules; GISTM (2020); ISO 17123 (instrument testing); ASTM standards for earthwork; FGDC/USACE EM 1110-1-1000 (photogrammetric mapping), EM 1110-2-1003 (hydrographic surveying for dredging).
**Key references.** James & Robson 2014 *ESPL* (doming); James et al. 2017 (precision maps); Carrivick, Smith & Quincey 2016 (SfM in geosciences); Tucci et al. 2019 (landfill volumes); Esposito et al. 2017 (mine UAV); Gama et al. 2020 (Brumadinho InSAR); Wheaton et al. 2010 (volumetric uncertainty); Hugenholtz et al. 2015 (UAV earthwork accuracy); Bemis et al. 2014 (ground-based SfM).
**Pitfalls.** Volume without base-surface uncertainty; grid-vs-ground scale confusion changing quantities by 0.01–0.1 %; counting a loader as stockpile; SfM dome inflating a 50,000 m³ pile by several percent; comparing surfaces in different vertical datums; wet-day survey of hygroscopic material.
**Key takeaways.** Engineered volumes are legal numbers — document datum, method, control, base surface, and uncertainty; use repeat-survey consistency checks and independent control; monitor continuously where failure is catastrophic.

### Chapter 66 — Coastal, marine, polar, lakes and rivers
**Scope.** Where land meets water and where water or ice is the surface: special datums, special sensors, special failure modes.
**Sections.**
- 66.1 The coastal zone: topo-bathy integration (Ch. 48), the white ribbon (surf zone, turbidity; Ch. 19), tidal datums and VDatum-type transformations (Ch. 9), shoreline definitions (Ch. 34), beach/dune/cliff change (Ch. 40), coastal structures (seawalls, jetties, groins), marsh and mangrove (Ch. 64), SLR exposure mapping and DEM requirements (Gesch 2018)
- 66.2 Ports, harbours, estuaries: dredging surveys and payment volumes (USACE EM 1110-2-1003), fluid mud and nautical bottom (density-based depth), siltation rates, bridge clearances (air gap, S-104/S-111), berth pockets, turbidity and SDB limits
- 66.3 Continental shelf and deep ocean: MBES systematics (Ch. 20), sound-speed structure, deep-water footprints (100s of m), gravity-predicted bathymetry (Ch. 23/24), Seabed 2030 resolution targets by depth (100 m–800 m cells), GEBCO TID reading, seamounts and hazards (USS *San Francisco*), submarine cables and pipelines (sandwaves, scour), offshore wind site surveys (geophysics + MBES + backscatter), habitat mapping from bathy + backscatter
- 66.4 Polar: ice-sheet surface DEMs (REMA/ArcticDEM; ICESat-2; CryoSat-2 swath), bed topography (BedMachine/Bedmap3 via radar sounding + mass conservation), penetration bias (X/C/Ku band into firn), sea ice is not terrain (freeboard → thickness), ice shelves (floating; tidal flexure), grounding lines, ice-free Antarctic bathymetry gaps, Arctic charting gaps and IBCAO/IBCSO
- 66.5 Lakes: lake datums (IGLD 1985/2020 for the Great Lakes; lake-specific chart datums), bathymetry campaigns (small boats, USVs, SDB for clear lakes), water-level time series (altimetry, SWOT, gauges), reservoir sedimentation surveys, lake ice season
- 66.6 Rivers: channel bathymetry (green lidar, ADCP, sonar; gaps in topo lidar), water surface slope from lidar/SWOT, stage–discharge, braided river dynamics, river datums and flood stages, sediment transport, bridge scour surveys, navigation channels (USACE eHydro), riverbed classification
- 66.7 Water as a moving reference: tides, surge, seiches, river stage, wind setup, SWOT and altimetry products, GNSS buoys and ellipsoidally referenced surveys (ERS) removing tidal reduction error
- 66.8 Validation in aquatic settings: reference surfaces, crosslines, uncertainty (TPU), diver/lead-line checks, repeatability of soft bottoms, SDB vs MBES checks, bias from bedforms moving between lines
**Then & now.** Lead lines and tide staffs ⟨H⟩ → singlebeam echo sounders (1920s) → SeaBeam MBES (1977) ⟨H⟩ → GNSS-referenced bathy lidar and ERS → satellite-derived and crowdsourced bathymetry; polar: radio-echo sounding (1960s) → BedMachine.
**Math.** Tidal datum computation (19-year NTDE, equivalence methods); sound-speed refraction (Snell) and depth error; freeboard→thickness hydrostatics; mass-conservation bed inversion (brief); air-gap and UKC budgets.
**Software.** Open: MB-System, VDatum/vyperdatum, NOAA HydrOffice tools, GMT, pyTMD (tides), SWOT toolkits, QGIS; Closed: CARIS HIPS/SIPS/BASE, QPS Qimera/Qinsy/Fledermaus, Hypack/Hysweep, EIVA NaviSuite, Teledyne PDS, BeamworX.
**Standards & guides.** IHO S-44, S-67, B-11 (GEBCO Cookbook); NOAA HSSD, FPM, Tidal Datums handbook, NOS Hydrographic Manual (1976 historic); USACE EM 1110-2-1003; IGLD 2020 documentation; UKHO/LINZ/CHS survey specs; SCAR/IBCSO guidance; Seabed 2030 roadmap.
**Key references.** Mayer et al. 2018 *Geosciences* (Seabed 2030); Weatherall et al. 2020; Wölfl et al. 2019; Jakobsson et al. 2020; Morlighem et al. 2017/2020 (BedMachine); Fretwell et al. 2013/Pritchard et al. 2025 (Bedmap); Howat et al. 2019; Porter et al. 2018; Gesch 2018; Parker et al. 2003 (VDatum); Dodd & Mills 2012 (ERS); Legleiter et al. 2009 (river bathymetry); Biancamaria, Lettenmaier & Pavelsky 2016 (SWOT); Eakins & Grothe 2014; Pe'eri et al. 2014 (SDB).
**Pitfalls.** Mixing LAT-based and MLLW-based grids; land DEM in orthometric meters merged with bathy in chart datum feet; a reservoir surveyed at drawdown presented as full-pool bathymetry; penetration bias in ice DEMs read as mass loss; sea ice in a "coastal DEM"; bedform migration aliasing as survey error.
**Key takeaways.** Water bodies introduce their own datums, surfaces, and time scales; ellipsoidally referenced surveys and explicit datum transformations remove the biggest seams; the deep ocean and polar beds remain mostly predicted, not measured — read the TID.

### Chapter 67 — Planetary DEMs: mapping without ground truth
**Scope.** Elevation on other worlds as the stress test for every method in this book — no benchmarks, no GNSS, few repeat passes.
**Sections.**
- 67.1 Reference systems off Earth: IAU body-fixed frames, reference radii and triaxial ellipsoids, planetocentric vs planetographic latitude, "sea level" surrogates (Mars areoid from MOLA/MGS gravity; lunar reference sphere 1737.4 km), the equivalent of vertical datum choices and their consequences
- 67.2 Sensors: laser altimetry (MOLA, LOLA, MLA, LLRI, GLAS-like), stereo photogrammetry (HRSC, HiRISE, CTX, LROC NAC, Cassini), radar (Magellan on Venus, Cassini on Titan, MARSIS/SHARAD subsurface), photoclinometry/shape-from-shading, radio science gravity; rover/lander stereo and lidar; sample-return context
- 67.3 Control: altimetry as the control network (MOLA as "truth" at ~m vertical, 100 m horizontal), bundle adjustment to altimetry, crossover analysis, control networks (USGS/RAND lunar networks), the absence of independent checkpoints and what replaces them (crossovers, overlap, self-consistency, lander positions)
- 67.4 Products: MOLA MEGDR (463 m), HRSC DTMs (50–100 m), CTX stereo DEMs (~20 m), HiRISE DTMs (1–2 m; Ames Stereo Pipeline/SOCET SET), LOLA/SLDEM2015 (60 m), LROC NAC DTMs (2–5 m), Mercury (MESSENGER), Venus (Magellan 1–3 km), asteroids/comets (shape models: SPC, SPG; Bennu/Ryugu/67P), Titan, icy moons; GMM gravity-derived "geoids"
- 67.5 Quality without ground truth: precision vs accuracy claims, inter-method comparisons (HiRISE vs CTX vs MOLA), illumination-induced artefacts (SfS), jitter, CCD seams, radar penetration into regolith/ice, time variability (dust devils, dunes, polar CO₂ frost, Titan lakes, Io volcanism), landing-site certification (Mars 2020 TRN map requirements; Hazard maps), slope statistics for engineering
- 67.6 Lessons back to Earth: self-consistency metrics, crossover adjustment, honest uncertainty in the absence of truth, archival discipline (PDS4), open pipelines (ISIS, ASP)
- 67.7 Formats and archives: PDS3/PDS4, ISIS cubes, GeoTIFF with planetary CRS (IAU codes in PROJ/GDAL), SPICE kernels for geometry; interoperability gaps
**Then & now.** Telescopic shadow heights (Galileo's lunar mountains) → Apollo metric camera and laser altimeter (1971) → Viking/Mariner photogrammetry → MOLA (1997–2001) → HiRISE DTMs (2008–) → LOLA/LROC → rover TRN (2021) and sample return.
**Math.** Planetocentric↔planetographic latitude; areoid from spherical-harmonic gravity; photoclinometry (reflectance → slope integration) and its ill-posedness; crossover adjustment formulation; bundle adjustment constrained to altimetry.
**Software.** Open: USGS ISIS, NASA Ames Stereo Pipeline (ASP) ⟨H⟩, SPICE/SpiceyPy, GDAL/PROJ planetary CRS, JMARS (free), QGIS planetary plugins, Cosmographia; Closed: BAE SOCET SET/GXP (HiRISE DTM production), ERDAS.
**Standards & guides.** IAU WGCCRE reports on cartographic coordinates and rotational elements; PDS4 standards; USGS Astrogeology DTM production guidelines; NASA PDS Cartography and Imaging Sciences Node guidance; IAU/USGS planetary CRS codes (PROJ).
**Key references.** Smith et al. 2001 *JGR* (MOLA); Kirk et al. 2008 *JGR* (HiRISE DTMs); Beyer, Alexandrov & McMichael 2018 *ESS* (ASP); Barker et al. 2016 (SLDEM2015); Archinal et al. 2018 (IAU WGCCRE); Gwinner et al. 2016 (HRSC); Henriksen et al. 2017 (LROC NAC DTMs); Ford & Pettengill 1992 (Magellan); Johnson et al. 2022 (Mars 2020 TRN); Laura et al. 2017 (planetary control networks); Barnouin et al. 2019/2020 (Bennu shape).
**Pitfalls.** Mixing areoid and ellipsoid-referenced Martian heights; HiRISE DTM "1 m posts" with meter-scale correlated error; shape-from-shading hallucinating relief under oblique light; planetographic vs planetocentric latitude confusions (Mars especially); PDS products without modern CRS metadata.
**Key takeaways.** Planetary mapping shows how far self-consistency and altimetry-anchored control can go — and how much honesty about accuracy is required when there is no ground truth; its open pipelines and archives are a model for Earth.

---

## Part XV — Law, policy, security, privacy, ethics

### Chapter 68 — Legal issues
**Scope.** Where elevation data meets law: boundaries, liability, licensing, regulation, and evidence.
**Sections.**
- 68.1 Boundaries defined by elevation and water: UNCLOS baselines (Art. 5 normal baseline = low-water line on official charts; Art. 7 straight baselines; Art. 13 low-tide elevations; Art. 76 continental shelf — 2,500 m isobath + 100 nmi and foot-of-slope rules; Art. 121 rocks vs islands), TALOS (IHO S-51) manual, the "ambulatory" shoreline and sea-level rise (ILC/ILA debates; Pacific states' baseline-freezing declarations), riparian/littoral property boundaries (mean high water; *Borax Consolidated v. Los Angeles* 1935 defining MHW by 18.6-year tidal epoch), watershed and ridgeline borders that move (Alps glaciers), thalweg boundaries (rivers), state boundaries in lakes
- 68.2 Vertical datum and units in law: statutory datums (NAVD88, NGVD29 in old deeds, local tidal datums), US survey foot deprecation (2022) and its legal transition, grid vs ground in plats, floodplain regulatory elevations (BFE) and insurance (NFIP; Elevation Certificates), building height limits (which reference?), FAA Part 77 obstruction surfaces and notice (Form 7460), easements by elevation (air rights, solar access, view ordinances), mineral rights by depth
- 68.3 Licensing and IP: public domain (US federal), Crown copyright and open licences (OGL), CC-BY/CC-BY-NC/CC-BY-SA products (FABDEM NC; CoastalDEM NC; Copernicus DEM licence terms; AW3D30 terms; TanDEM-X 12 m commercial), database rights (EU sui generis), derivative-work questions (is a DTM derived from NC data NC?), attribution requirements, open data mandates (EU High-Value Datasets Regulation 2023 includes elevation; INSPIRE; US OPEN Government Data Act), ML training data licensing and model outputs
- 68.4 Liability and professional practice: licensed surveyor requirements for boundary and (in some jurisdictions) topographic/hydrographic surveys, "practice of surveying" definitions vs GIS/photogrammetry (state board disputes; ASPRS/NSPS model law), standard of care and negligence (charts, flood maps, obstacle data), product liability for data, disclaimers and their limits, duty to warn (known errors), professional certification (ASPRS CP, IHO Cat A/B, PLS/RPLS, chartered status)
- 68.5 Contracts and specifications as law: procurement specs (LBS, HSSD, S-44 order) as contractual accuracy, acceptance testing and remedies, data ownership clauses, delivery format requirements, warranty of fitness, dispute resolution with independent verification
- 68.6 Evidence: DEMs and surveys in litigation (boundary, flood damage, mining disputes, landslide causation, construction claims), admissibility (Daubert/Frye in US; expert evidence rules elsewhere), chain of custody and provenance (Ch. 50), expert-witness duties, drone data as evidence
- 68.7 Privacy and data-protection law touching elevation (Ch. 69): GDPR and 3D city/façade data, aerial imagery regulations, Street View-type blurring, drone privacy laws, trespass by survey (airspace and property), lidar scanning people
- 68.8 Export control and secrecy law: ITAR/EAR and Wassenaar (high-grade IMUs, certain lidar/sonar, GNSS), national mapping restrictions (India 2021 Geospatial Guidelines; China Surveying and Mapping Law and GCJ-02 offsets; Russia; South Korea export restrictions on maps), Kyl–Bingaman Amendment on Israel imagery resolution (relaxed 2020) ⟨H⟩, classification of bathymetry
- 68.9 Regulatory requirements for data use: aviation (DO-200B processing, certified providers), maritime (SOLAS carriage of ENCs; official vs unofficial charts), floodplain management, environmental permitting (wetland delineation elevations), mining and dam safety (Ch. 65)
- 68.10 Indigenous and community data rights: CARE principles, OCAP (Canada), consultation on surveys over traditional lands, sacred-site locations in elevation products
**Then & now.** Boundaries by monument and witness tree ⟨H⟩ → coordinates in law (Public Land Survey System; state plane) → tidal boundaries by datum (Borax 1935) → UNCLOS 1982 (in force 1994) → open-data mandates (2010s–2020s) and ML-licence questions (2020s).
**Software.** Open: GDAL/QGIS for boundary analysis; UNCLOS/TALOS tools (CARIS LOTS is closed; Geocap closed; open scripts exist); licence checkers (SPDX); Closed: CARIS LOTS, Geocap, Trimble/Carlson survey legal description tools.
**Standards & guides.** UNCLOS (1982); IHO S-51 TALOS Manual (Ed. 5); ILA Sea Level Rise Committee reports; US ALTA/NSPS Land Title Survey standards; NSPS model law; ASPRS/MAPPS guidance on licensing; FEMA G&S and Elevation Certificate instructions; FAA AC 70/7460; EU Regulation 2023/138 (High-Value Datasets); INSPIRE Directive 2007/2/EC; Creative Commons licences; OGL v3; India Geospatial Guidelines 2021; US OPEN Government Data Act 2018.
**Key references.** *Borax Consolidated v. City of Los Angeles*, 296 U.S. 10 (1935); Shalowitz 1962/1964 *Shore and Sea Boundaries*; Reed 2000 (vol. 3); Schofield et al. 2014 (sea-level rise and baselines); Prescott & Schofield 2005 *Maritime Political Boundaries*; Onsrud 2010 (legal issues in geospatial data); Cho 2005 *Geographic Information Science: Mastering the Legal Issues*; Scassa 2013 (legal issues with VGI); NGS 2019/2020 (survey foot deprecation notices); Carroll et al. 2020 (CARE).
**Pitfalls.** Treating MHW from a single tide gauge as the boundary everywhere; building a commercial product on NC-licensed DEMs; "topographic survey" delivered by an unlicensed firm in a state that requires a PLS; obstacle filings in the wrong vertical datum; assuming public-domain status for non-US agency data; discovery of a known DEM error after harm with no record of disclosure.
**Key takeaways.** Elevation numbers have legal meaning only with their datum, epoch, method, and licence attached; know which activities require licensure or certification; keep provenance as if it will be evidence — someday it will be.

### Chapter 69 — National security, sovereignty, privacy, and ethics
**Scope.** Who may map what, who may see it, who is harmed or helped — and how the field should behave.
**Sections.**
- 69.1 Security history and present: wartime map secrecy, Cold War deliberate map distortion (Soviet maps), GPS Selective Availability (off 2000) ⟨H⟩, SRTM 1″ release restrictions (2000 → global 2014–15), Kyl–Bingaman ⟨H⟩, bathymetry classification (submarine operations) vs Seabed 2030 openness, NGA TREx (TanDEM-X-based 12 m, restricted), national high-resolution lidar release policies, DEM resolution caps in some countries, GNSS jamming/spoofing effects on surveys (Baltic, Eastern Mediterranean, Black Sea), anti-drone restrictions
- 69.2 Sovereignty and national mapping control: licensing of surveys by foreigners (India, China, Russia, Gulf states), mandatory data localization, offset coordinate systems (GCJ-02/BD-09), control over foreign satellite imagery of territory, marine scientific research consent in EEZs (UNCLOS Part XIII) for bathymetric surveys, the politics of names and boundaries in elevation products (disputed territories; Google Maps border practices), who "owns" the seafloor map of an EEZ
- 69.3 Dual use: elevation data for defence (TERCOM, line-of-sight, trafficability), civilian benefit vs adversary use, the resolution/security trade-off debate; disaster response needing open data quickly (Charter, Copernicus EMS)
- 69.4 Privacy: individuals in point clouds and imagery (faces, licence plates, backyards from oblique/3D), fitness traces (Strava 2018), mobile-mapping blurring norms (Street View), drones over private property, indoor scans, elevated-view "peeking" (3D city models revealing courtyards, pools, extensions), inference risks (unpermitted construction detected from DSM change — civic good or surveillance?), legal frameworks (GDPR, CCPA, Canadian PIPEDA; "reasonable expectation of privacy" case law), de-identification techniques for point clouds (blur/remove people/vehicles; aggregate), data minimization and retention
- 69.5 Equity and access: "lidar deserts" — hazard mapping gaps in the Global South (Schumann & Bates 2018), Seabed 2030 and the unmapped 75 %, cost barriers and open-data benefits, capacity building (IHO CBSC, Nippon Foundation–GEBCO training), Indigenous data sovereignty (CARE, OCAP), benefit sharing from surveys of community lands/waters
- 69.6 Ethics of representation and inference: ML products as de facto truth, bias in training geographies, overstated accuracy and its downstream harms (flood maps, insurance redlining), transparency obligations, publishing uncertainty as an ethical duty, dual-use review of methods papers (e.g., building-level exposure)
- 69.7 Environmental and animal welfare ethics of surveying: sonar and marine mammals (mitigation, permits), drone disturbance of wildlife, energy/carbon of large campaigns and ML training
- 69.8 Governance proposals: tiered access with declassification schedules, independent audits of restricted DEM quality, open metadata even when data are closed, responsible-use statements for products, community review in survey planning
**Then & now.** Secret national surveys ⟨H⟩ → civilian GPS and SA removal (2000) ⟨H⟩ → open global DEMs (SRTM) → a mixed present of openness (Copernicus, 3DEP, Seabed 2030) and new restrictions (data localization, drone rules, spoofing); privacy moved from imagery to 3D and inference.
**Software.** Open: anonymization tools for point clouds/imagery (e.g., open face/plate blurring models), differential-privacy libraries (for aggregate products), OSM-style community governance tooling; Closed: commercial blurring pipelines (Cyclomedia, Google), restricted government distribution systems.
**Standards & guides.** UNCLOS Part XIII (marine scientific research); IHO CBSC guidance; GDPR (2016/679) and EDPB guidance on video/imagery; CARE/OCAP; US NSG/NGA release policies (public summaries); India Geospatial Guidelines 2021; EU Data Governance Act; FAIR + CARE joint guidance; ethical guidelines for remote sensing (ASPRS Code of Ethics; GEO data sharing principles); JNCC/NOAA sonar mitigation guidance.
**Key references.** Monmonier 2002 *Spying with Maps*; Crampton 2010 *Mapping: A Critical Introduction to Cartography and GIS*; Hern 2018 (Strava); Schumann & Bates 2018 *Front. Earth Sci.*; Mayer et al. 2018 (Seabed 2030 openness); Carroll et al. 2020 (CARE); Kitchin & Dodge 2011 *Code/Space*; Kitchin 2014 *The Data Revolution*; Postnikov (Soviet maps) 2002; Zook & Graham 2007 (geoweb and borders); Pickles 1995 *Ground Truth*.
**Pitfalls.** Collecting high-resolution 3D data in a jurisdiction that requires permits (and losing the data and the project); publishing a DSM change product that outs private construction without considering harm; assuming export-controlled IMUs can travel; surveys in an EEZ without consent; treating restricted-data quality claims as verified; ignoring community consent.
**Key takeaways.** Elevation data are powerful and political; know the legal regime before you fly, sail, or publish; default to open data with open uncertainty while designing for privacy and consent; openness and security are a negotiated, documented trade-off — not an accident.

---

## Part XVI — Standards, software, and history

### Chapter 70 — Survey and product specifications: a guided tour (S-44, HSSD, FPM, LBS, ASPRS, ICAO, INSPIRE…)
**Scope.** The documents that define what "good enough" means — how they're structured, how they differ, and how to read, apply, and crosswalk them.
**Sections.**
- 70.1 How specs are built: scope, definitions, accuracy classes/orders, coverage/density, feature detection, calibration/QC requirements, deliverables, metadata, acceptance tests; prescriptive vs performance-based; versions and change logs
- 70.2 Hydrographic: IHO S-44 Ed. 6.1.0 (orders Exclusive/Special/1a/1b/2; TVU/THU formulas; feature detection/search; bathymetric coverage; survey-matrix flexibility), NOAA HSSD (annual editions; object detection coverage, complete coverage, set-line spacing; crosslines; TPU; deliverables — BAG, S-57 features, DR, metadata; NBS integration), NOAA Field Procedures Manual (2020; later editions) — systems preparation, calibrations, reference surfaces, data acquisition and processing procedures, USACE EM 1110-2-1003 (Hydrographic Surveying; dredging payment surveys), LINZ HYSPEC, UKHO/Admiralty specs, CHS Hydrographic Survey Management Guidelines, Australian HIPP specs, IHO C-13 (Manual on Hydrography), S-67, B-11 (GEBCO Cookbook), IHO S-100 product specs (S-101/S-102/S-104/S-111) and their quality attributes; crowdsourced bathymetry guidance (B-12)
- 70.3 Topographic lidar/photogrammetry: USGS Lidar Base Specification (2024 rev A; QL0–QL3; NPS/NPD, NVA/VVA, classification, hydro-flattening, swath overlap, deliverables), ASPRS Positional Accuracy Standards Ed. 2 (2023), ASPRS LAS 1.4, FEMA G&S elevation guidance, USACE EM 1110-1-1000 (photogrammetric and lidar mapping), FGDC NSSDA, NDEP guidelines (2004 — historical), ICSM LiDAR Acquisition Specifications (Australia), NRCan/CanElevation specs, UK EA survey specs, Netherlands AHN specs, Nordic national specs, ISPRS/EuroSDR guidance, UAV mapping guidelines (ASPRS UAS; national aviation authorities)
- 70.4 Aviation: ICAO Annex 15 and PANS-AIM Doc 10066 (eTOD areas 1–4, numerical requirements), Doc 9881, RTCA DO-276C/EUROCAE ED-98D (terrain/obstacle data user requirements), DO-200B/ED-76A (processing standards), FAA AC 150/5300-18 (airport surveys; vertical/horizontal accuracy by feature), AC 150/5300-16/17, EUROCONTROL TOD manual
- 70.5 Geodetic control: NGS-58/59 (GPS heights), NGS Bluebooking, FGCC 1984 standards (orders/classes), ISO 17123 (instrument field procedures), CORS site guidelines, NOAA NGS NSRS modernization documents, IGS standards
- 70.6 Product/data specs: INSPIRE Data Specification on Elevation (D2.8.II.1), Copernicus DEM product handbook, 3DEP product standards, DTED MIL-PRF-89020B, NGA HRE/HRTe, OGC CityGML, S-102; INSPIRE/ISO 19157 quality element mapping
- 70.7 Crosswalk tables: S-44 orders ↔ HSSD coverage/accuracy ↔ USACE classes ↔ ICAO eTOD areas ↔ ASPRS vertical classes ↔ LBS QLs ↔ INSPIRE quality — units, confidence levels (95 % vs RMSE vs 90 %), surface definitions, feature detection; where they are incommensurable
- 70.8 Reading specs critically: what they don't say (effective resolution, correlated error, temporal validity), when specs lag technology (topo-bathy lidar, ML, VR grids), how to write a project-specific spec that references standards without copying them
- 70.9 Compliance and audit: QA/QC plans, independent verification, documentation of deviations, acceptance/rejection, continuous improvement loops (post-project reviews)
**Then & now.** NMAS 1947 ⟨H⟩ → IHO S-44 1st ed. 1968 ⟨H⟩ … 6th ed. 2020/2022 → NSSDA 1998 → USGS LBS v1.0 2012 → 2024; from contour tests to statistical, surface-type-aware, uncertainty-bearing specifications.
**Math.** S-44 TVU/THU; ASPRS RMSE classes and 95 % conversion; LBS density/accuracy relationships; ICAO confidence levels (90 %/95 %); conversions between 90 %, 95 %, RMSE assuming normality (and when not to assume it).
**Software.** Open: NOAA HydrOffice QC Tools (free), Pydro (free), PDAL/lidR checks scripted to LBS, xdem; Closed: CARIS/QPS compliance tools, TerraScan, LP360 QA, GeoCue.
**Standards & guides.** (This chapter *is* the index — see Appendix D for the full citation list with editions and URLs.)
**Key references.** IHO 2020/2022 S-44 Ed. 6.0.0/6.1.0; NOAA OCS HSSD (current edition) and FPM (2020; 2023 update); USGS 2024 LBS rev A (Techniques and Methods 11-B4 lineage); ASPRS 2023 *PE&RS*; ICAO Annex 15 (Amendment 40+) and Doc 10066; RTCA 2021 DO-276C; FAA 2009/2024 AC 150/5300-18; FGDC 1998 NSSDA; NDEP 2004; INSPIRE TWG 2013; Zilkoski et al. 1997/2008.
**Pitfalls.** Quoting a spec's accuracy class as the product's tested accuracy; mixing 95 % and RMSE across specs; applying LBS classification rules to a bathymetric dataset; treating HSSD annual changes as cosmetic; forgetting that S-44 "orders" are minimums chosen by the hydrographic office, not automatic properties of a survey.
**Key takeaways.** Specs encode a domain's definition of fitness; read the definitions and test procedures, not just the tables; crosswalks are approximate — document assumptions; a project spec should reference, not reinvent.

### Chapter 71 — Software landscape: open-source and closed-source by task
**Scope.** Who does what in elevation data processing, with licences, lineage, strengths, and the risk of lock-in; organized by task, not vendor.
**Sections.**
- 71.1 How to read this chapter: open source (OSI licences), free-but-closed (freeware, academic licences), commercial; maturity, community, file-format support, scripting/APIs, provenance features; "freeware ≠ open source"; sustainability (foundations: OSGeo, NumFOCUS, Linux Foundation/OGC) ⟨H⟩
- 71.2 Foundations and libraries: GDAL/OGR ⟨H⟩, PROJ ⟨H⟩, GEOS, PDAL, laspy, rasterio/xarray/rioxarray/dask, GMT ⟨H⟩, NumPy/SciPy stack, R (terra, sf, lidR, gstat), Julia (GeoStats.jl), Rust/Go ecosystems (geo, tile tools)
- 71.3 GNSS/INS processing: open RTKLIB, GAMIT/GLOBK (free academic), Bernese (licensed), GipsyX (licensed), PRIDE-PPP-AR, gnssrefl; closed Applanix POSPac, NovAtel Inertial Explorer, Trimble Business Center, Leica Infinity; services OPUS, CSRS-PPP, AUSPOS
- 71.4 Lidar: open PDAL, LAStools (mixed), lidR, CloudCompare, Open3D, whitebox, FUSION (free), OpenTopography pipelines; closed TerraSolid, LP360, GeoCue, Trimble RealWorks, Leica Cyclone, Riegl RiPROCESS, Optech LMS, Global Mapper; bathy lidar vendor suites (Teledyne/Leica Chiroptera/HawkEye; Riegl VQ-880)
- 71.5 Photogrammetry/SfM: open MicMac, OpenDroneMap, COLMAP, Meshroom/AliceVision, OpenMVS, Ames Stereo Pipeline ⟨H⟩, SETSM, MicMac; closed Agisoft Metashape, Pix4D, Bentley ContextCapture/iTwin Capture, DJI Terra, Trimble Inpho, SimActive, BAE SOCET GXP, Hexagon/ERDAS, RealityCapture
- 71.6 Sonar/hydrography: open MB-System ⟨H⟩, HydrOffice (free), Pydro (free), Kluster (NOAA, open), OpenSidescan, OpenCPN; closed CARIS HIPS/SIPS/BASE/HPD, QPS Qinsy/Qimera/Fledermaus, Hypack/Hysweep, EIVA NaviSuite, Teledyne PDS, BeamworX, SonarWiz, Kongsberg SIS
- 71.7 Radar/InSAR: open ISCE2, GMTSAR, SNAP (ESA; free), MintPy, LiCSBAS, pyroSAR, Doris; closed GAMMA, SARscape, TRE Altamira services
- 71.8 Geodesy/datums: PROJ + PROJ-data grids, VDatum (free), vyperdatum, HTDP, NGS tools (GEOID18/xGEOID, OPUS), GeoidEval; closed vendor transformation libraries; the problem of grid availability and licensing (national geoid models)
- 71.9 DEM analysis and hydrology: GRASS GIS ⟨H⟩, SAGA, WhiteboxTools, TauDEM, RichDEM, LSDTopoTools, TopoToolbox, Landlab, xdem, QGIS ⟨H⟩; closed ArcGIS Pro/Spatial Analyst/ArcHydro, Global Mapper, Surfer, RiverTools
- 71.10 Change detection and validation: xdem, demcoreg, py4dgeo, CloudCompare M3C2, GCD, MICRODEM/DEMIX (free); closed TerraMatch, Cyclone 3DR, Trimble RealWorks
- 71.11 ML: PyTorch/TensorFlow, TorchGeo, Open3D-ML, Pointcept, segment-geospatial, Raster Vision, scikit-learn; closed Esri deep learning, eCognition, cloud vendor ML
- 71.12 Visualization/cartography: QGIS, GMT, Blender, RVT, Potree, Cesium, deck.gl, MapLibre, three.js, matplotlib/cmcrameri, Eduard (closed), ArcGIS Pro, Global Mapper, Fledermaus, Surfer, Terragen
- 71.13 Data management/catalogs: pystac, STAC tooling, GeoNetwork, CKAN, pycsw, Entwine, TiTiler, GeoServer/MapServer, PostGIS, DuckDB spatial; closed ArcGIS Enterprise, Esri Portal, commercial DAMs
- 71.14 Planetary: ISIS, ASP, SPICE, JMARS; closed SOCET GXP
- 71.15 Cloud platforms: Google Earth Engine ⟨H⟩ (free for research; closed service), Microsoft Planetary Computer, AWS Open Data, Copernicus Data Space; vendor lock-in and reproducibility
- 71.16 Choosing and governing software: validation of software (benchmarks, round-trip tests), version pinning, reproducible environments (conda/pixi/docker), license compliance, long-term support, contributing back; when to buy
**Then & now.** SYMAP/GRASS/ARC-INFO era ⟨H⟩ → desktop GIS and vendor suites → open libraries as the shared substrate (GDAL 1998 ⟨H⟩, PROJ, PDAL 2011–) → cloud-native and notebook workflows → ML frameworks; the open/closed boundary keeps moving (e.g., HEC-RAS free-closed; LAStools mixed).
**Software.** (This chapter is the catalogue; Appendix F gives a sortable table: name, task, licence, language, formats, maintainer, last release, notes.)
**Standards & guides.** OSI licence definitions; OGC compliance program; OSGeo project incubation criteria; FAIR for research software (FAIR4RS); software citation principles (Smith et al. 2016).
**Key references.** Warmerdam 2008 (GDAL); Butler et al. (PDAL docs); Caress & Chayes 1996 (MB-System); Neteler et al. 2012 (GRASS); Wessel et al. 2019 (GMT 6); Roussel et al. 2020 (lidR); Lindsay 2016 (Whitebox); Beyer et al. 2018 (ASP); Rupnik, Daakir & Pierrot-Deseilligny 2017 (MicMac); Schönberger & Frahm 2016 (COLMAP); Gorelick et al. 2017 (GEE); Steiniger & Hunter 2013 (open-source GIS landscape); Coetzee et al. 2020 (open geospatial software, data, standards).
**Pitfalls.** Treating software output as validated because the vendor is reputable; silently different interpolation/resampling defaults across tools (half-cell shifts, kernel choice); unpinned versions changing results; "free" tools with export restrictions; losing data access when a licence lapses; GUI-only workflows with no provenance.
**Key takeaways.** Pick tools by task, format fidelity, provenance, and sustainability; keep an open-source path for every critical step; validate software like data — with benchmarks and round trips.

### Chapter 72 — How we got here: a history of measuring the shape of the Earth
**Scope.** A narrative history tying the handbook together — ideas, instruments, institutions, and mistakes — anchored to the timeline in Appendix C.
**Sections.**
- 72.1 Antiquity to the Enlightenment: Eratosthenes' circumference; Ptolemy; Islamic geodesy (al-Biruni); Snellius triangulation (1615); Picard; Cassini vs Newton on the Earth's shape and the French geodesic missions to Lapland and Peru (1735–44); the metre defined from the meridian ⟨H⟩
- 72.2 National surveys and the figure of the Earth: Ordnance Survey (1791) ⟨H⟩; Great Trigonometrical Survey of India and Everest (1802–1870s); Gauss and least squares (1809) ⟨H⟩; Bessel/Clarke/Hayford ellipsoids ⟨H⟩; US Coast Survey (1807) ⟨H⟩; levelling networks and NGVD29 (1929) ⟨H⟩; Helmert and the geoid; isostasy (Pratt/Airy)
- 72.3 Depth: lead lines and Maury's bathymetric chart (1853) ⟨H⟩; HMS *Challenger* (1872–76) ⟨H⟩; echo sounding (Fessenden 1914; Meteor expedition 1925) ⟨H⟩; Heezen–Tharp physiographic maps (1950s–70s) ⟨H⟩; SeaBeam multibeam (1977) ⟨H⟩; satellite altimetry bathymetry (Seasat 1978; Smith & Sandwell 1997) ⟨H⟩; GEBCO (1903–) and Seabed 2030 (2017) ⟨H⟩
- 72.4 Air and light: photogrammetry (Laussedat; stereoplotters 1900s–1930s) ⟨H⟩; aerial survey in WWI/WWII; radar (1930s–40s); laser (1960) and airborne laser profiling (1960s–70s); GPS launch (1978) ⟨H⟩ and full operational capability (1995); airborne lidar with GPS/IMU (1990s) ⟨H⟩; SRTM (2000) ⟨H⟩; ICESat (2003); TanDEM-X (2010); ICESat-2/GEDI (2018–19); UAV SfM (2010s)
- 72.5 Computation and data: Fourier/Shannon ⟨H⟩; Kalman (1960) ⟨H⟩; digital terrain models (Miller & Laflamme 1958) ⟨H⟩; SYMAP/Harvard Lab (1960s) ⟨H⟩; CGIS (1960s) ⟨H⟩; DTED (1970s) ⟨H⟩; quadtrees ⟨H⟩; ARC/INFO (1982) ⟨H⟩; GRASS (1982) ⟨H⟩; TIN (1978); CUBE (2003); LAS (2003) ⟨H⟩; BAG (2006); GDAL (1998) ⟨H⟩; PDAL; cloud-native formats (2016–) ⟨H⟩; STAC (2017–) ⟨H⟩; Earth Engine (2010) ⟨H⟩; ML era (2012–)
- 72.6 Datums and frames: NAD27 (1927) ⟨H⟩ → NAD83 (1986) → ITRF (1988–) → WGS 84 realizations ⟨H⟩ → NAVD88 (1991) → GEOID models → NSRS modernization (2020s); international: ED50 → ETRS89; GDA94 → GDA2020; the move to time-dependent coordinates (Ch. 38)
- 72.7 Standards and institutions: IHO (1921) ⟨H⟩ and S-44 (1968) ⟨H⟩; ISPRS (1910); FIG (1878); IAG/IUGG; ASPRS (1934); FGDC (1990) ⟨H⟩; OGC (1994) ⟨H⟩; ISO/TC 211 (1994) ⟨H⟩; OSGeo (2006) ⟨H⟩; the open-data turn (SRTM, Landsat 2008, Copernicus, 3DEP)
- 72.8 Recurring patterns: every new sensor was first over-trusted; every datum change created a decade of mixed data; the archive was always under-funded; the error budget was understood by few and documented by fewer; standards followed disasters
- 72.9 Then-vs-now table: for each capability (horizontal position, height, depth, point density, coverage, latency, cost, uncertainty reporting) — 1900 / 1950 / 1980 / 2000 / 2025
**Math.** Eratosthenes' geometry; least squares (Gauss/Legendre); ellipsoid flattening from arc measurements; the geoid as an equipotential surface (brief); Kalman filter origins.
**Software.** (Historical: SYMAP, GRASS 1.0, ARC/INFO, ERDAS, early MB-System; emulators and archives where available.)
**Standards & guides.** Historical editions: NMAS 1947; S-44 1st ed. 1968; FGDC CSDGM 1994; NSSDA 1998 — read alongside current editions to see what changed and why.
**Key references.** Keay 2000 *The Great Arc*; Alder 2002 *The Measure of All Things*; Smith 1997 (history of geodesy/surveying); Torge & Müller 2012 *Geodesy* (historical chapters); Dickinson 1979 *Maps and Air Photographs*; Collier 2002 (history of photogrammetry); Deacon 1971 *Scientists and the Sea*; Dierssen & Theberge 2014 (bathymetry history); Parkinson & Spilker 1996 *GPS: Theory and Applications* (history chapter); Konecny 2014 *Geoinformation*; Chrisman 2006 *Charting the Unknown* (Harvard Lab); Foresman 1998 *The History of GIS*; Coppock & Rhind 1991; Theberge 1989 (NOAA Coast Survey history); gis-history repository (schwehr) as the timeline source.
**Pitfalls.** Whiggish history ("we finally got it right"); forgetting that legacy data in archives were produced under those old assumptions and still carry them; assuming today's defaults will not look naive in 2050.
**Key takeaways.** Most present-day confusions (datums, units, surface definitions, over-trust of new sensors) have historical roots; knowing the history is a validation skill — it tells you what a dataset from a given era could and could not know.

### Chapter 73 — Open problems and the next decade
**Scope.** Where the field is heading, what remains unsolved, and what practitioners should prepare for.
**Sections.**
- 73.1 Reference frames: NSRS modernization (NATRF2022/NAPGD2022 geopotential datum), fully kinematic global frames, GNSS-only heights via geoid models at cm level — and the decade of mixed-datum data that will follow
- 73.2 Sensors: SWOT (water surfaces), NISAR (L/S-band InSAR), Biomass (P-band), ICESat-2/GEDI continuity, single-photon and Geiger-mode lidar at scale, topo-bathy lidar from satellites?, hyperspectral-aided SDB, quantum gravimetry/accelerometers for navigation, chip-scale atomic clocks, LEO-PNT and GNSS resilience, swarm USVs/AUVs for Seabed 2030, commercial smallsat stereo constellations, consumer lidar (phones, cars) as crowdsourced sources
- 73.3 Products: uncertainty rasters by default; per-pixel time stamps; multi-surface products (DTM/DSM/canopy/water/building layers shipped together); continuous national updates instead of decadal campaigns; ML-corrected global DTMs with calibrated uncertainty and open training data; "living" bathymetric compilations with supersession (NBS as model)
- 73.4 Methods: foundation models for point clouds and terrain (promise and risk), physics-informed ML, probabilistic terrain modelling (Gaussian processes at scale), 4D change as the native product, automatic QA/QC with human audit, standardized intercomparison (DEMIX-like) as a community habit, formal verification of pipelines
- 73.5 Semantics: agreed cross-domain definitions of ground/building/water surfaces (a "surface ontology"), machine-readable inclusion/exclusion rules, multi-valued surface standards (bridges, overhangs), 3D/indoor integration with outdoor DEMs
- 73.6 Data infrastructure: cloud-native everything (COPC/COG/Zarr), quality-first catalogs (search by tested accuracy), persistent provenance (content-addressed), long-term raw archives funded as infrastructure, energy footprint accounting
- 73.7 Policy: openness vs security equilibria, privacy in 3D, ML licence contamination resolution, international bathymetric data sharing (EEZ consent), capacity building and closing lidar deserts, data sovereignty tooling
- 73.8 Education and workforce: curricula that teach error budgets and datums before deep learning; certification updates (IHO Cat A/B, ASPRS CP) for ML and autonomy; interdisciplinary literacy (geodesy ↔ hydrology ↔ ML)
- 73.9 Grand challenges list: a global 1 m DTM with 0.5 m 95 % vertical accuracy and uncertainty layers; full-ocean MBES coverage; routine daily change monitoring of hazards; universal, machine-readable datum/epoch metadata; validated uncertainty for ML elevation products; privacy-preserving 3D city data
- 73.10 What to do now: adopt uncertainty-bearing formats, publish checkpoints, archive raw data, participate in intercomparisons, write limitations sections, keep an open-source path
**Then & now.** From "a DEM" to "the elevation of this place at this time with this uncertainty for this purpose" — the next decade should make that sentence routine.
**Key references.** NGS 2021 *Blueprint for the Modernized NSRS* (TR 62/64/67); Mayer et al. 2018 (Seabed 2030); Schumann & Bates 2018; Hawker et al. 2022; Guth et al. 2021; Bielski et al. 2024; Reichstein et al. 2019; Tuia et al. 2024 (AI for Earth observation perspective); SWOT/NISAR mission papers; GEO/OGC/IHO strategic plans; NASEM 2018 *Thriving on Our Changing Planet* (Decadal Survey; topography and vegetation structure observables).
**Pitfalls.** Betting on a single sensor or model; assuming new frames will be adopted quickly; shipping ML products without truth; neglecting archives while chasing novelty.
**Key takeaways.** The next decade's gains will come as much from metadata, uncertainty, and openness as from sensors; the handbook's validation discipline is the part least likely to be automated away.

---

## Appendices

### Appendix A — Glossary (selected entries; full glossary ≈ 400 terms)
Format: **term** — definition — *see chapter*. Entries flag common confusions with ⚠.
- **Accuracy / precision / uncertainty** — closeness to truth / repeatability / quantified doubt (GUM) — ⚠ RMSE is not a 95 % bound — *Ch. 5, 53*
- **AGL / AMSL / HAE** — above ground level / above mean sea level (orthometric) / height above ellipsoid — ⚠ GPS "altitude" is HAE unless converted — *Ch. 7, 9, 62*
- **BAG** — Bathymetric Attributed Grid; elevation + uncertainty + metadata (ONS) — *Ch. 47*
- **Bare earth** — surface with vegetation and structures removed per a stated rule — ⚠ rule varies by producer — *Ch. 32*
- **Breakline** — vector line constraining surface interpolation (hard/soft) — *Ch. 59*
- **CATZOC / ZOC** — chart category of zone of confidence (A1–D, U) — *Ch. 62, 70*
- **Chart datum** — low-water reference for depths (LAT, MLLW, …) — ⚠ differs from land datum by metres — *Ch. 9*
- **Checkpoint vs control point** — independent test point vs point used in adjustment — ⚠ never both — *Ch. 25, 52*
- **CHM** — canopy height model = DSM − DTM — *Ch. 64*
- **COG / COPC / Zarr** — cloud-optimized GeoTIFF / point cloud / chunked arrays — *Ch. 47*
- **CORS** — continuously operating reference station — *Ch. 25*
- **CUBE / CHRT** — Combined Uncertainty and Bathymetry Estimator; its variable-resolution successor — *Ch. 20, 46*
- **Datum (geodetic, vertical, tidal)** — reference frame/surface + realization + epoch — ⚠ "WGS 84" has multiple realizations — *Ch. 7–9, 38*
- **DEM / DSM / DTM / DBM** — generic elevation model / surface incl. objects / terrain (bare earth) / bathymetric model — ⚠ "DEM" used for both DSM and DTM — *Ch. 4*
- **DGGS** — discrete global grid system (S2, H3, ISEA…) — *Ch. 60*
- **DoD / LoD** — DEM of difference / level of detection (also level of detail in 3D models ⚠) — *Ch. 40, 41, 63*
- **Effective resolution** — smallest feature actually resolved; ≠ pixel size — *Ch. 44*
- **Epoch** — the time to which coordinates refer — *Ch. 37, 38*
- **eTOD** — electronic terrain and obstacle data (ICAO) — *Ch. 62, 70*
- **Geoid / quasi-geoid / geoid model** — equipotential surface ≈ MSL / Molodensky variant / its numerical realization (EGM2008, GEOID18…) — *Ch. 7*
- **GCP** — ground control point — *Ch. 25, 59*
- **Hydro-flattening / -enforcement / -conditioning** — flat water bodies / cut barriers for flow / general flow fixes — *Ch. 34, 61*
- **Last return / first return** — lidar returns nearest ground / top of surface — *Ch. 18*
- **Lever arm / boresight** — sensor offset vector / angular misalignment — *Ch. 13, 25*
- **M3C2** — multiscale model-to-model cloud comparison — *Ch. 41*
- **NMAD** — normalized median absolute deviation (robust σ) — *Ch. 53*
- **NPS / NPD** — nominal pulse spacing / density — *Ch. 44*
- **NVA / VVA** — non-vegetated / vegetated vertical accuracy (ASPRS) — *Ch. 53*
- **Orthometric / dynamic / normal height** — height types over a geoid/quasigeoid — *Ch. 7*
- **Patch test** — MBES/lidar boresight calibration procedure — *Ch. 25, 26*
- **Pixel-is-area / pixel-is-point** — GeoTIFF raster-space conventions — ⚠ half-cell shift — *Ch. 10, 47*
- **Shoal-biased** — gridding/generalization choosing the shallowest value — *Ch. 20, 62*
- **Shoreline (MHW, MLLW, LAT, "instantaneous")** — legally/tidally defined lines — ⚠ not the visible water edge — *Ch. 34, 68*
- **STAC** — SpatioTemporal Asset Catalog — *Ch. 51*
- **TPU / TVU / THU** — total propagated / vertical / horizontal uncertainty (IHO) — *Ch. 53, 70*
- **TID** — GEBCO Type Identifier (measured vs predicted source) — *Ch. 48, 55*
- **VLM** — vertical land motion — *Ch. 38*
- **Void / nodata / fill** — missing cell / sentinel value / interpolated replacement — *Ch. 35*
- **White ribbon** — the nearshore gap between topographic and bathymetric coverage — *Ch. 19, 66*

### Appendix B — Mathematical reference
Short derivations and formulas collected from the "Math" lines, with notation table and worked numeric examples.
- B.1 Statistics of error: mean, bias, σ, RMSE, MAE, NMAD, percentiles; RMSE² = bias² + σ²; CI for RMSE (χ²); 95 % conversions (1.96σ; 1.7308·RMSE_r for CE95 under circular normal); robust estimators; outlier tests
- B.2 Error propagation: linear J Σ Jᵀ; Monte Carlo; spatially correlated fields (variograms, SGS); effective sample size; volume uncertainty with correlation
- B.3 Geodesy: ellipsoid geometry (a, f, e²; N, M radii), geodetic↔ECEF, Helmert 7/14-parameter, orthometric/normal/dynamic heights, geoid undulation h = H + N, gravity and geopotential numbers, plate velocity v = ω × r
- B.4 Projections: scale factor, convergence, grid-vs-ground combined factor, Tissot indicatrix (brief), UTM/TM series (Snyder) ⟨H⟩
- B.5 Positioning: GNSS pseudorange/carrier-phase observation equations, DOP, double differences, ambiguity resolution sketch; Kalman filter equations ⟨H⟩; IMU strapdown mechanization; lever-arm and boresight transforms
- B.6 Sensors: lidar range/footprint/pulse geometry; refraction (Snell) for bathy lidar and sonar; sonar range/beamwidth/footprint; MBES depth from beam angle with ray tracing; SAR geometry (layover/shadow), InSAR phase→height (height of ambiguity), decorrelation; stereo parallax→height; collinearity/coplanarity; bundle adjustment normal equations; SfM scale ambiguity; SDB log-ratio (Stumpf) and radiative-transfer (Lyzenga) models; gravity–bathymetry admittance (Smith & Sandwell)
- B.7 Surfaces: Delaunay/TIN properties; interpolation (IDW, splines, kriging equations), ANUDEM sketch; CUBE hypothesis updating; Horn gradient operator; slope/aspect/curvature; openness/SVF; flow routing (D8/D∞); priority-flood; TWI
- B.8 Sampling and resolution: Nyquist–Shannon ⟨H⟩; aliasing; MTF of footprint; power spectra of terrain and effective resolution estimation; quantization noise q/√12; float precision
- B.9 Change: DoD/LoD; Nuth & Kääb cosine fit; M3C2 and LoD₉₅; ICP; Okada dislocation (summary); time-series regression with correlated noise
- B.10 Catenary, thermal sag, wind sway (Ch. 33); UKC budget (Ch. 62); tidal datum computation (Ch. 9/66)
- B.11 Indexing: Morton/Hilbert curves ⟨H⟩; quadtree/octree addressing ⟨H⟩; S2 cell geometry; H3 aperture-7 relations; Web Mercator area distortion
- B.12 ML evaluation: confusion matrix metrics, IoU, κ; spatial CV; proper scoring rules; conformal intervals; calibration curves
- B.13 Numeric worked examples: (a) float32 northing precision; (b) half-cell shift effect on slope; (c) sound-speed error → depth error at 60° beam; (d) sag change for 100 °C conductor temperature rise; (e) RMSE from 30 checkpoints with 95 % CI; (f) volume ±uncertainty with correlation length 20 m

### Appendix C — Timeline (seeded from gis-history; ⟨H⟩ = from the repository, ⟨+⟩ = added for this handbook)
*Format: year — event — chapter(s). A ~250-entry version is planned; the seed below shows coverage.*
- c. 240 BC — Eratosthenes measures Earth's circumference ⟨+⟩ — 72
- 1569 — Mercator projection ⟨H⟩ — 10
- 1576 — Theodolite first built ⟨H⟩ — 11
- 1615 — Snellius triangulation ⟨+⟩ — 72
- 1620 — Gunter's chain ⟨H⟩ — 11
- 1735–44 — French geodesic missions settle Earth's flattening ⟨+⟩ — 72
- 1761 — Harrison H4 chronometer ⟨H⟩ — 11
- 1776 — Photogrammetry's beginnings (Lambert) ⟨H⟩ — 22
- 1791 — Principal Triangulation of Great Britain / Ordnance Survey ⟨H⟩ — 72
- 1795 — Metre defined from the meridian ⟨+⟩ — 4
- 1799 — Lehmann hachures ⟨+⟩ — 57
- 1807 — US Coast Survey funded ⟨H⟩ — 72
- 1809 — Gauss, least squares ⟨+⟩ — 5
- 1830 / 1861 — Airy / Clarke ellipsoids ⟨H⟩ — 7
- 1833 — Buttermilk, oldest surviving US survey mark ⟨H⟩ — 25
- 1853 — Maury's bathymetric chart of the North Atlantic ⟨+⟩ — 20
- 1858 — Nadar's balloon aerial photograph ⟨H⟩ — 22
- 1872–76 — HMS *Challenger* soundings ⟨+⟩ — 20
- 1879 — USGS formed ⟨H⟩ — 58
- 1884 — International Meridian Conference ⟨H⟩ — 8
- 1890 / 1891 — Peano / Hilbert space-filling curves ⟨H⟩ — 46, 60
- 1903 — GEBCO started ⟨H⟩ — 55
- 1904 — Radar beginnings ⟨H⟩ — 21
- 1913 — First echo-sounder patent ⟨H⟩ — 20
- 1914 — SOLAS convention ⟨H⟩ — 62
- 1921 — IHO founded ⟨+⟩ — 70
- 1927 — NAD27 ⟨H⟩ — 8
- 1928 — Hawley's *Hydrographic Manual* ⟨H⟩ — 70
- 1929 — Grand Banks turbidity current breaks cables ⟨H⟩ — 39, 56
- 1929 — NGVD29 (Sea Level Datum of 1929) ⟨+⟩ — 9
- 1934 — ASPRS founded ⟨H⟩ — 70
- 1942 — UTM first appears; LORAN; first INS ⟨H⟩ — 10, 11, 13
- 1947 — US National Map Accuracy Standards ⟨+⟩ — 53, 58
- 1948 — Shannon, *A Mathematical Theory of Communication* ⟨H⟩ — 44
- 1951 — Synthetic-aperture radar concept ⟨H⟩ — 21
- 1952 / 1957 / 1977 — Tharp–Heezen seafloor maps; first physiographic ocean map; first whole-ocean-floor map ⟨H⟩ — 20, 72
- 1957 — Tellurometer; Sputnik 1 ⟨H⟩ — 11
- 1958 — Kalman filter ⟨H⟩ — 13
- 1958 — Miller & Laflamme coin "digital terrain model" ⟨+⟩ — 4
- 1960 — Laser; UTC; Valdivia M9.5 ⟨H⟩ — 17, 39
- 1961 — First lidar system ⟨H⟩ — 18
- 1962 — Multibeam sonar patent filed ⟨H⟩ — 20
- 1963 — CGIS, first GIS ⟨H⟩ — 72
- 1964 — Transit satellite navigation operational ⟨+⟩ — 11
- 1965 — Harvard Lab for Computer Graphics; "pixel" coined ⟨H⟩ — 72
- 1968 — IHO S-44 first edition ⟨+⟩ — 70
- 1969 — ESRI founded; CCD invented ⟨H⟩ — 71, 22
- 1970 — NOAA formed ⟨H⟩ — 70
- 1972 — Landsat 1 ⟨H⟩ — 23
- 1974 — Quadtree ⟨H⟩ — 46
- 1976 — NOS *Hydrographic Manual*, 4th ed. ⟨H⟩ — 70
- 1977 — SeaBeam, first commercial multibeam ⟨H⟩ — 20
- 1978 — GPS first launch; TIN paper (Peucker et al.); Seasat altimetry ⟨H⟩⟨+⟩ — 12, 46, 23
- 1979 — CARIS formed ⟨H⟩ — 71
- 1980 — GRS80; GCTP (Snyder) ⟨H⟩ — 7, 10
- 1981 — RANSAC; Horn hillshade ⟨H⟩⟨+⟩ — 42, 57
- 1982 — Arc/Info; GLONASS first launch; SPICE; UNCLOS signed ⟨H⟩ — 71, 12, 67, 68
- 1983 — Evenden's projection procedures → PROJ ⟨H⟩ — 10
- 1984 — GRASS released; WGS 84 / EGM84; NMEA 0183 ⟨H⟩ — 71, 7, 12
- 1985 — GEOSAT ⟨H⟩ — 23
- 1986 — SLAM begins (Smith & Cheeseman); NAD83 (1986) ⟨H⟩⟨+⟩ — 15, 8
- 1987 — Snyder, *Map Projections: A Working Manual*; GCMD keywords ⟨H⟩ — 10, 49
- 1988 — GMT; NetCDF; ITRF88 ⟨H⟩⟨+⟩ — 71, 47, 38
- 1989 — RINEX; ANUDEM ⟨H⟩⟨+⟩ — 12, 31
- 1990 — HDF ⟨H⟩ — 47
- 1991 — NAVD88 ⟨+⟩ — 9
- 1992 — TOPEX/Poseidon; HTDP 1.0; Tomasi–Kanade factorization ⟨H⟩ — 23, 38, 22
- 1993 — MB-System first commit; EPSG dataset public ⟨H⟩ — 71, 8
- 1994 — OGC founded; PROJ4; FGDC metadata standard; UNCLOS in force; NSDI ⟨H⟩ — 70, 10, 49, 68, 51
- 1995 — GeoTIFF published; GPS full operational capability ⟨H⟩⟨+⟩ — 47, 12
- 1996 — Ames Stereo Pipeline starts; EGM96; GTOPO30 ⟨H⟩⟨+⟩ — 67, 7, 55
- 1997 — Smith & Sandwell global seafloor topography; NOAA FPM first edition; Kyl–Bingaman ⟨H⟩ — 23, 70, 69
- 1998 — Shapefile spec; AIS first spec; GSF baseline; NSSDA ⟨H⟩⟨+⟩ — 59, 27, 47, 53
- 1999 — libgeotiff; Ikonos; WKT CRS ⟨H⟩ — 47, 22, 8
- 2000 — SRTM flown; SA disabled; GDAL first release; HSSD first released; GML ⟨H⟩ — 21, 12, 71, 70
- 2001 — PostGIS; QuickBird ⟨H⟩ — 71, 22
- 2002 — QGIS; AIS mandated; GEOS ⟨H⟩ — 71, 27
- 2003 — LAS 1.0; ICESat launched; ISO 19115:2003; WAAS; CUBE published ⟨H⟩⟨+⟩ — 47, 52, 49, 12, 20
- 2004 — Indian Ocean earthquake/tsunami; OSM; AWS ⟨H⟩ — 39, 59, 51
- 2005 — USS *San Francisco* grounding; Google Maps ⟨H⟩ — 56
- 2006 — OSGeo founded; BAG 1.0; DJI formed ⟨H⟩⟨+⟩ — 71, 47, 16
- 2007 — INSPIRE directive; Google Earth; Farr et al. SRTM paper ⟨H⟩⟨+⟩ — 70, 57, 55
- 2008 — GeoJSON; EGM2008; Street View ⟨H⟩ — 59, 7, 69
- 2009 — ASTER GDEM v1; Earth Engine begins; US Topo ⟨H⟩⟨+⟩ — 55, 51, 58
- 2010 — TanDEM-X launched; GeoEye/WorldView era; Deepwater Horizon ⟨+⟩⟨H⟩ — 21, 22, 27
- 2011 — Tōhoku earthquake; PDAL; CesiumJS; LAZ; Galileo first launch ⟨H⟩⟨+⟩ — 39, 71, 57, 47, 12
- 2012 — USGS Lidar Base Specification v1.0; 3DEP concept ⟨+⟩ — 70
- 2013 — what3words; geopandas; xarray ⟨H⟩ — 60, 71
- 2014 — GeoPackage; Sentinel-1; plus codes; SRTM 1″ global release begins; ASPRS 2014 accuracy standards ⟨H⟩⟨+⟩ — 47, 21, 60, 55, 53
- 2015 — Sentinel-2; Zarr-python; AW3D30 ⟨H⟩⟨+⟩ — 23, 47, 55
- 2016 — Kaikōura earthquake; COG emerges; deck.gl ⟨+⟩⟨H⟩ — 39, 47, 57
- 2017 — STAC first commit; S2 geometry open-sourced; Seabed 2030 launched; PointNet; Earth Engine paper ⟨H⟩⟨+⟩ — 51, 60, 66, 42
- 2018 — ICESat-2; GEDI; Earth Engine public catalog; H3; Strava heatmap; CoastalDEM ⟨H⟩⟨+⟩ — 52, 60, 69, 43
- 2019 — Copernicus DEM first release; GEBCO TID grids; Zarr spec ⟨+⟩⟨H⟩ — 55, 48, 47
- 2020 — IHO S-44 Ed. 6; NOAA FPM 2020; Kyl–Bingaman relaxed; Planetary Computer; NBS/BlueTopo ⟨+⟩⟨H⟩ — 70, 69, 51, 48
- 2021 — STAC 1.0; COPC 1.0; GeoParquet; Mars 2020 TRN landing; Hugonnet glacier mass balance ⟨H⟩⟨+⟩ — 51, 47, 62, 40
- 2022 — FABDEM; ETOPO 2022; US survey foot deprecated; SWOT launched ⟨+⟩ — 43, 55, 68, 66
- 2023 — ASPRS Positional Accuracy Standards Ed. 2; SAM; EU High-Value Datasets in force ⟨+⟩ — 53, 42, 68
- 2024 — USGS LBS 2024; S-102 Ed. 3; DEMIX papers; STAC 1.1; Icechunk; DeltaDTM; BAG 2.0 ⟨H⟩⟨+⟩ — 70, 47, 55, 51
- 2025 — Biomass P-band launched; NISAR launch; GEDTM30; Bedmap3 ⟨H⟩⟨+⟩ — 64, 21, 55, 66
- 2026+ — NSRS modernization rollout (NATRF2022/NAPGD2022) ⟨+⟩ — 73

### Appendix D — Standards and guide documents index
Grouped by domain; each entry in the full appendix carries: issuer, current edition/date, scope one-liner, what it defines about accuracy/uncertainty, URL, chapters.
- **Hydrographic:** IHO S-44 Ed. 6.1.0 (2022); S-57 Ed. 3.1; S-100 Ed. 5.x; S-101; S-102 Ed. 3.0/3.1; S-104; S-111; S-67; S-4; S-51 (TALOS); S-32 (dictionary); C-13; B-11 (GEBCO Cookbook); B-12 (CSB); NOAA HSSD (annual; current ed.); NOAA Field Procedures Manual (2020; subsequent updates); NOAA NOS Hydrographic Manual 4th ed. (1976, historical); NOAA Tidal Datums and Their Applications (SP CO-OPS 1); USACE EM 1110-2-1003; LINZ HYSPEC; CHS Standards for Hydrographic Surveys; UKHO/ADMIRALTY survey specs; AusSeabed/HIPP specs; NOAA NBS/BlueTopo specification
- **Topographic lidar/photogrammetry/UAS:** USGS Lidar Base Specification 2024 rev A; ASPRS Positional Accuracy Standards Ed. 2 (2023); ASPRS LAS 1.4 R15 (2019) and topo-bathy domain profile; FGDC NSSDA (1998); NMAS (1947); NDEP Guidelines (2004); FEMA Guidelines & Standards for Flood Risk Analysis and Mapping (elevation guidance); USACE EM 1110-1-1000; ICSM LiDAR Acquisition Specifications (AU); NRCan HRDEM product spec; UK EA National LiDAR Programme spec; AHN product specs (NL); ASPRS UAS guidelines; ISPRS/EuroSDR benchmarks
- **Geodesy and datums:** ISO 19111:2019; IOGP EPSG Guidance Notes 7-2 and 373-25; NGS-58 (1997), NGS-59 (2008); FGCC Standards and Specifications for Geodetic Control Networks (1984); NGS NSRS modernization Blueprints (NOAA TR NOS NGS 62, 64, 67); IERS Conventions (2010) and updates; ITRF2020 documentation; GDA2020 Technical Manual; LINZ NZGD2000 deformation model; VDatum documentation; IHO/IOC tidal datum guidance
- **Aviation:** ICAO Annex 15; Annex 4; Doc 10066 (PANS-AIM); Doc 9881 (eTOD guidelines); RTCA DO-276C / EUROCAE ED-98D; DO-200B / ED-76A; FAA AC 150/5300-18; AC 150/5300-16, -17; 14 CFR Parts 77 and 107; EUROCONTROL TOD manual
- **Formats:** OGC GeoTIFF 1.1 (19-008r4); OGC COG 1.0 (21-026); COPC 1.0; ASPRS LAS 1.4 R15; ONS BAG 2.0; MIL-PRF-89020B (DTED); CF Conventions 1.11; Zarr v3; GeoZarr (draft); OGC GeoPackage 1.4; GeoParquet 1.1; RFC 7946 (GeoJSON); OGC Simple Features (ISO 19125); OGC CityGML 3.0, CityJSON 2.0; OGC IndoorGML 2.0; OGC 3D Tiles 1.1; I3S; Cesium quantized-mesh; LandXML 1.2; E57 (ASTM E2807); GSF; S-100 Part 10c (HDF5)
- **Metadata, quality, catalogs, archives:** ISO 19115-1/-2/-3; ISO 19157-1:2023; ISO 19131 (product specs); FGDC CSDGM (1998) and shoreline/lidar profiles; STAC 1.0/1.1 + extensions; OGC API – Records; DCAT/GeoDCAT-AP; INSPIRE D2.8.II.1 Elevation; ISO 14721 (OAIS); ISO 16363; W3C PROV; DataCite 4; FAIR; CARE; CoreTrustSeal
- **DGGS and codes:** OGC Topic 21 (DGGS); OGC API – DGGS (draft); FGDC-STD-011-2001 (USNG); Open Location Code spec; H3/S2 documentation
- **ML and software governance:** OGC TrainingDML-AI; model cards; ISO/IEC 23053; OSGeo incubation; FAIR4RS
- **Legal/policy:** UNCLOS (1982); EU Regulation 2023/138 (HVD); INSPIRE 2007/2/EC; GDPR; India Geospatial Guidelines (2021); US OPEN Government Data Act (2018); Creative Commons licence suite; OGL v3; ITAR/EAR and Wassenaar lists (relevant categories); NFIP regulations (44 CFR)
- **Engineering/other:** ASCE 38-22; JORC (2012); NI 43-101; GISTM (2020); IEEE 738; NERC FAC-003; ISO 17123; ALTA/NSPS 2021; IAU WGCCRE reports; PDS4

### Appendix E — Public products comparison tables
Two master tables (land; bathymetry/ice) plus regional-program table. Columns: **Product · Producer · Type (DSM/DTM/hybrid/model) · Nominal post · Effective resolution (est.) · Acquisition dates · Horizontal/vertical datum (geoid) · Reported accuracy · Independent accuracy (by land cover/slope; source) · Voids/fills & masks · Known artefacts · Uncertainty layer? · Licence · Formats/tiling · Cadence/version · Best for / avoid for · Handbook refs.**
Seed rows (values to be verified against product handbooks at writing time):

| Product | Type | Post | Dates | Vert. datum | Reported acc. | Licence | Notes |
|---|---|---|---|---|---|---|---|
| SRTM v3 / NASADEM | DSM (C-band) | 1″ | Feb 2000 | EGM96 | ~16 m LE90 spec; ~5–9 m RMSE typical | Public domain | Voids filled; penetration; 60°N–56°S |
| ASTER GDEM v3 | DSM (optical) | 1″ | 2000–2013 stack | EGM96 | ~8–17 m RMSE | Free (terms) | Noisy, artefacts; high lat. coverage |
| ALOS AW3D30 v3/v4 | DSM (optical) | 1″ | 2006–2011 | EGM96 | ~5 m RMSE | Free (terms) | Cloud masks; v4 improvements |
| TanDEM-X DEM | DSM (X-band) | 12/30/90 m | 2010–2015 | WGS 84 ellipsoid | <2 m rel. (90 %); ~10 m abs. | 90 m free; 12/30 m restricted | HEM layer; penetration in forest/snow |
| Copernicus DEM GLO-30/90 | DSM (edited TanDEM-X) | 1″/3″ | 2011–2015 | EGM2008 | <4 m LE90 abs. (90 %) | Free (Copernicus licence) | Edited water/shore; masks; best general DSM |
| MERIT DEM / MERIT Hydro | DTM-ish (error-removed) | 3″ | SRTM/AW3D base | EGM96 | improved low-relief | CC-BY-NC-4.0 / mixed | Stripe/speckle removed; hydro layers |
| FABDEM v1-2 | DTM (ML-removed) | 1″ | Copernicus base | EGM2008 | ~1.1–2.9 m RMSE reported | CC-BY-NC-SA-4.0 | Forest/building removal; artefacts on terraces |
| DeltaDTM | Coastal DTM | 1″ | Copernicus + ICESat-2 | EGM2008 | ~0.45 m MAE reported | CC-BY-4.0 | Coastal lowlands only |
| CoastalDEM v2 | Coastal DTM (ML) | 1″ | SRTM base | EGM96 | ~1–2 m RMSE reported | Non-commercial/licensed | Used in SLR exposure papers |
| GEDTM30 | DTM (ML global) | 1″ | multi | EGM2008 | per paper | CC-BY | 2025; validate locally |
| ArcticDEM / REMA | DSM strips & mosaics | 2 m | 2009– (time-stamped) | WGS 84 ellipsoid | ~m-level abs. (ICESat-2 registered) | Public | Blunders; use strips for change |
| USGS 3DEP | DTM (lidar) + point clouds | 1 m (QL2/QL1) | 2010s– | NAVD88 (GEOID12B/18) | ≤10 cm RMSE_z NVA (QL2) | Public domain | Project-based dates; seamless 1 m/1/3″ |
| National lidar (AHN, EA, swisstopo, LINZ, …) | DTM/DSM | 0.5–2 m | varies | national | ~5–15 cm | mostly open | See Ch. 55.2 |
| GEBCO_2024 | Bathy/topo model | 15″ | compilation | MSL (nominal) | n/a (TID-based) | Free | Mostly predicted in deep ocean |
| SRTM15+ V2 | Bathy/topo | 15″ | compilation | MSL | n/a | Free | Gravity-predicted + soundings |
| ETOPO 2022 | Bathy/topo (bed/ice) | 15″/30″ | compilation | EGM2008 | n/a | Public domain | Ice surface & bedrock versions |
| GMRT | MBES synthesis | ~100 m (multi) | continuous | MSL | n/a | Free | Measured where MBES exists |
| EMODnet Bathymetry | Bathy DTM | 1/16′ | compilation | LAT→MSL | source-dependent | Free | Europe; source references layer |
| IBCAO v5 / IBCSO v2 | Bathy | 200 m / 500 m | compilation | MSL | n/a | Free | Polar; TID-like source grids |
| NOAA BlueTopo (NBS) | Bathy (US) | 2–16 m VR | continuous | MLLW (ellipsoid-ready) | per-cell uncertainty | Public domain | Source & uncertainty rasters; supersession |
| NCEI CUDEM | Topo-bathy tiles | 1/9″, 1/3″ | compilation | NAVD88 / MHW variants | per-tile | Public domain | Coastal US; check datum variant |
| BedMachine / Bedmap3 | Sub-ice bed | 150–500 m | compilation | ellipsoid/geoid | error grid | Free | Mass-conservation inversion |

### Appendix F — Software index
Sortable table: **Name · Primary tasks · Licence (OSI id / freeware / commercial) · Language/API · Key formats · Maintainer/foundation · First release · Status · Chapters.** Seed: GDAL, PROJ, GEOS, PDAL, LAStools (mixed), laspy, lidR, CloudCompare, Open3D, PotreeConverter/Potree, Entwine, MicMac, OpenDroneMap, COLMAP, Meshroom, Ames Stereo Pipeline, SETSM, MB-System, HydrOffice, Pydro, Kluster, ISCE2, GMTSAR, SNAP, MintPy, LiCSBAS, RTKLIB, gnssrefl, HTDP, VDatum, vyperdatum, GMT, GRASS, SAGA, WhiteboxTools, TauDEM, RichDEM, LSDTopoTools, TopoToolbox, Landlab, xdem, demcoreg, py4dgeo, GCD, DSAS, MICRODEM, QGIS, PostGIS, DuckDB spatial, pystac, STAC tooling, GeoNetwork, TiTiler, Cesium, deck.gl, MapLibre, RVT, Blender, matplotlib/cmcrameri/cmocean, TorchGeo, Pointcept, Open3D-ML, segment-geospatial, ISIS, SPICE, JMARS, HEC-RAS (free/closed), LISFLOOD-FP, SFINCS, ANUGA, OctoMap, GridMap; commercial: ArcGIS Pro, Global Mapper, TerraSolid, LP360, GeoCue, Trimble Business Center/RealWorks/Inpho, Leica Cyclone/Infinity, Riegl RiPROCESS, Agisoft Metashape, Pix4D, Bentley ContextCapture/iTwin, DJI Terra, CARIS, QPS, Hypack, EIVA, Teledyne PDS, BeamworX, SonarWiz, Applanix POSPac, NovAtel Inertial Explorer, GAMMA, SARscape, ENVI, Surfer, Fledermaus, Eduard, Propeller, Maptek, PLS-CADD, eCognition, FME, SOCET GXP.

### Appendix G — Checklists
- **G.1 Before commissioning or planning a survey (Ch. 26):** use and decision defined → required surface type, resolution, accuracy, currency → datum/epoch/geoid specified → control plan (CORS, benchmarks, GCPs, checkpoints independent) → calibration plan (patch test/boresight; reference surface; crosslines ≥ 5 % or spec) → environmental windows (tide, leaf-off, snow, turbidity, wind) → moving-object strategy (AIS/ADS-B logs, time-of-day) → deliverables and formats with uncertainty layers → QA/QC roles and acceptance tests → archive and licence terms
- **G.2 Evaluating a DEM you did not make (Ch. 54):** CRS horizontal + vertical + geoid + epoch confirmed → units → pixel convention → surface type and inclusion rules → acquisition dates (per-cell?) → hillshade sweep (multi-azimuth) → flat-surface noise test → tile/strip seam check → voids/fill mask → independent check (ICESat-2/benchmarks/other DEM over stable terrain, with co-registration) → stratified residual stats → licence → write fitness-for-use memo
- **G.3 Metadata minimum for publication (Ch. 49):** identifier/DOI & version → CRS (H+V, geoid, epoch) → surface type & inclusion/exclusion rules → dates → sensor/platform/method → processing lineage & software versions → resolution (post, source density, effective) → accuracy (statistic, standard, checkpoint table, strata) → voids/fills/masks → uncertainty layer definition → licence → contact → limitations paragraph
- **G.4 Compositing (Ch. 48):** harmonize datums → harmonize surface types → co-register & bias-correct on overlaps → declare priority rule (by use) → blend policy and seam documentation → produce source/date/uncertainty/method rasters → seam QC → hydro-connectivity QC → version & supersession log
- **G.5 Change detection (Ch. 41):** same surface definition both epochs → co-registration (Nuth–Kääb/ICP) on stable terrain → per-epoch uncertainty, spatially variable → LoD threshold stated a priori → confounds screened (season, water, moving objects, datum/epoch changes, processing version) → volumes with correlated-error intervals → confidence map published
- **G.6 Publishing an ML-derived or enhanced elevation product (Ch. 43, 45):** training data and licences listed → spatial CV/AOA reported → independent checkpoints by stratum → calibrated uncertainty tested → "derived/enhanced" flag in metadata and filename → intended/forbidden uses stated → model card
- **G.7 Hydrographic deliverable (Ch. 62, 70):** S-44 order / HSSD edition cited → TPU per sounding → crosslines analysed → feature detection demonstrated → datum (chart datum via ellipsoid separation model) → BAG/S-102 with uncertainty → DR/metadata complete → supersession info for NBS
- **G.8 Archiving (Ch. 50):** raw retained (waveforms/raw sonar/images/GNSS-IMU) → open formats → checksums → provenance manifest → geoid/transformation grids archived → DOI → retention schedule → repository with trust certification

### Appendix H — Datasets for exercises and benchmarks
- **Validation/benchmark:** DEMIX tiles and reference DEMs; ISPRS Vaihingen/Toronto; DALES; OpenGF; Hessigheim H3D; US3D/DFC2019; SensatUrban; Toronto-3D; ICESat-2 ATL08 samples; GEDI L2A samples; NGS benchmark datasheets (OPUS shared); OpenTopography lidar (e.g., repeat surveys for change exercises); Shallow Survey common datasets (MBES); NOAA sample BAGs; EMODnet sample tiles
- **Teaching scenes (one per chapter where possible):** a coastal lidar + MBES seam (CUDEM tile); an urban LoD2 city block (3D BAG); a forested slope leaf-on/leaf-off pair (3DEP + state lidar); a river with hydro-flattening (3DEP + NHDPlus HR); a landslide pre/post pair (Oso lidar); a glacier DEM time series (ArcticDEM strips); a powerline corridor (open utility lidar sample); an earthquake coseismic pair (El Mayor–Cucapah/Kaikōura); a planetary HiRISE DTM; a port MBES survey with crosslines; an SDB scene (Sentinel-2 + reference MBES); a global-DEM intercomparison tile (Copernicus/NASADEM/AW3D30/FABDEM + ICESat-2)
- **Synthetic data:** generated terrain with known truth for error-propagation and interpolation exercises; simulated lidar strips with boresight errors; simulated MBES with sound-speed errors
- **Licensing notes per dataset; download sizes; suggested exercises and expected outcomes.**

### Appendix I — Gap review: what else should be included, and what could be trimmed
*The requested review of the outline against the brief, plus items surfaced while drafting.*

**I.1 Topics added beyond the original list (already placed in the skeleton)**
Fitness-for-use framework (Ch. 3); the error/uncertainty toolkit as an early chapter (Ch. 5); time as a first-class axis (Ch. 6, 37); non-GNSS positioning and the GNSS-denied world (Ch. 14); measurement physics across sensors (Ch. 17); calibration infrastructure as its own chapter (Ch. 25); cost reduction (Ch. 28); pipelines and lineage (Ch. 29); voids/occlusion/multi-valued surfaces (Ch. 35); traditional-vs-ML as a cross-cutting assessment with validation rules (Ch. 43); archiving/versioning/provenance (Ch. 50); forensic evaluation (Ch. 54); case files (Ch. 56); DGGS in depth (Ch. 60); planetary DEMs as the no-ground-truth stress test (Ch. 67); specifications crosswalk (Ch. 70); history narrative (Ch. 72); open problems (Ch. 73).

**I.2 Candidates still missing or thin — recommended additions**
1. **Earth tides, ocean/atmospheric loading, and refraction** as cm-level systematic effects — give a dedicated section in Ch. 7 or 25 (currently scattered in 36.3/36.4).
2. **Barometric altimetry and pressure-based heights** (drones, phones, aviation QNH/QFE) — add to Ch. 14.
3. **GNSS reflectometry (GNSS-R/IR)** for water level, snow depth, soil moisture — add to Ch. 14/23.
4. **Orthorectification and model orography as hidden consumers of DEMs** (satellite image geolocation errors inherit DEM errors; NWP terrain) — add to Ch. 1 and 29.
5. **Radio/viewshed/solar/wind engineering uses** (RF planning clutter, PV yield, wind resource) — currently in 63.7; promote to a section in Ch. 1 with surface requirements.
6. **Robotics elevation maps and HD maps** — present in Ch. 62; add latency/update-rate requirements and map-as-sensor error budgets.
7. **Time synchronization as an error source** (GNSS/IMU/lidar/sonar timing, PPS, PTP; 1 ms at 50 m/s = 5 cm) — add to Ch. 13/17.
8. **Quantization, lossy compression, and overview generation as error sources** — present in Ch. 46/47; add a worked-example box.
9. **Reproducibility and computational provenance** (containers, pinned versions, notebooks) — present in Ch. 50/71; consider a short dedicated section in Ch. 29.
10. **Crowdsourced elevation and trust models** (CSB, OSM elevation tags, phone barometers, consumer lidar/iPhone scans; validity and bias) — add to Ch. 16/51.
11. **Human factors in manual editing and QC** (fatigue, inter-operator variability, editing logs as data) — add to Ch. 30/53.
12. **Economics**: cost–benefit and value-of-information for elevation programs (3DEP benefit study; Seabed 2030 economics) — add to Ch. 28.
13. **Licence nuances**: NC/SA contamination through derivatives and ML training — present in Ch. 68.3; add decision tree.
14. **2.5D vs true 3D decision guidance** across domains — present in 46/63; add a one-page decision aid in Ch. 46.
15. **Hazard-specific DEM requirements** (avalanche, rockfall, lava flow, tsunami inundation, debris flow, pyroclastic) — add a section in Ch. 61 or a short Ch. 61b "Hazard modelling constraints".
16. **UNCLOS Art. 121 and low-tide elevations** in detail with DEM/bathy evidence needs — present in Ch. 68.1; expand with a worked case (South China Sea arbitration 2016).
17. **Caves, karst, mines, tunnels, and subsurface voxel models** — mention in 63/65; consider a short section "Below the surface" in Ch. 63.
18. **Sea ice and icebergs** as moving "terrain" — present in 66.4; add to Ch. 27 (moving objects) too.
19. **Lake and river datums** (IGLD, river stage datums) — present in 66.5/66.6; cross-link Ch. 9.
20. **Terrain for noise, microclimate, and ecological indices (TWI, solar radiation, cold-air pooling)** — add to Ch. 1 uses with resolution guidance.
21. **Vertical exaggeration honesty and perceptual effects** — in 57; add guidance table.
22. **Generative/synthetic terrain** (games, simulation, training data) and the risk of synthetic data leaking into "real" catalogs — add to Ch. 45/73.
23. **Tile naming and indexing schemes** (SRTM N37W122, 3DEP project tiles, Copernicus tile IDs, S-102 tiling) — add to Ch. 47/51.
24. **Elevation APIs and hidden provenance** — present in Ch. 51; add testing recipe.
25. **Consumer lidar (phones, cars) validity** — add to Ch. 16.
26. **Benchmarking culture** (DEMIX, ISPRS, GRSS DFC, Shallow Survey) — scattered; a sidebar in Ch. 53.
27. **Education/certification pathways** (IHO Cat A/B, ASPRS CP, licensed surveyors, GISP) — brief in 68/73; consider a short Appendix J "Learning pathways".
28. **Communicating uncertainty to decision makers** (risk framing, probabilistic maps, legal thresholds) — present in 53.8/57.9; consider a short standalone chapter in Part XI.
29. **Equity and "lidar deserts"** — present in 69.5; strengthen with program case studies (Caribbean, Africa, Pacific SIDS).
30. **Energy and carbon cost** of acquisition, processing, ML, and storage — mentioned in 50.8/69.7; add numbers.
31. **Accessibility** (colorblind-safe palettes, tactile/3D-printed terrain, screen-reader charts) — present in 57.11; keep.
32. **Planetary analog fieldwork and lunar south-pole DEMs for landing** — in Ch. 67; add Artemis-era requirements.
33. **Subsurface geophysics beyond gravity/magnetics** (seismic refraction, GPR for near-surface) — Ch. 24 could mention GPR for ice/snow/soil interfaces.
34. **Areoid/selenoid definitions** — present in 67.1; keep.
35. **Weather/space-weather effects on GNSS** (ionospheric storms, scintillation) — add to Ch. 12.
36. **Atmospheric correction for InSAR and the role of DEMs in it** — add to Ch. 21.
37. **Shadow/illumination in optical SDB and DSM matching (sun angle, seasons)** — add to Ch. 22/23.
38. **Vessel/aircraft dynamics and squat/heave/settlement** as elevation error sources — in 20/62; add to Ch. 13 lever-arm/motion section.
39. **Insurance and finance uses** (cat models, parametric insurance, mortgage flood risk) — add to Ch. 1 and 68.
40. **Standard operating procedures for post-disaster rapid DEMs** (who flies, what to publish, provisional labelling) — present in 39.8; expand into a checklist (Appendix G.9).

**I.3 Items from the brief — coverage check (all present)**
Uses land/bathy (1–3); positioning history/GNSS/IMU (11–14); sensors & platforms incl. car/foot/drone/kite/aircraft/fixed infrastructure (16); bathylidar vs lidar (18–19); sonar types (20); SDB (23); geodesy/projections/datums (7–10); SfM/stereo (22); SLAM (15); radar/SAR (21); calibration targets/CORS/benchmarks (25); survey planning (26); temporal change (6, 37–41); moving objects incl. cars/ships/construction/dumps/fires/steam & AIS/ADS-B (27); formats LAS/BAG/GeoTIFF (47); resolution/oversampling (44); super-resolution (45); point clouds/waveforms/grids/TINs/VR/overviews (46); references per topic (every block); traditional vs ML (43); change detection (41); object detection (42); privacy (69); gravity/magnetics (24); processing (29–31); resolution & precision (44, 53); change over time of systems (Then & now lines; 72); software per topic (Software lines; 71); visualization incl. colormaps/filtering/rendering/splats (57); math (Math lines; App. B); building/road definitions and DSM→DTM errors (32); bridges/pipes inclusion rules (32); wires/powerlines & time scales (33); seasonal (36); variable water (34, 66); steam (27, 36); ground truth datasets (52); metadata (49); archiving (50); STAC/search (51); pitfalls & takeaways (every block); resolution→appropriateness (3, 44); cost reduction (28); naming/definitions (4); compositing order/blend/crop/override (48); shoreline (34, 68); vertical datums (9); legal (68); HSSD/FPM and other guides (70; App. D); evaluating others' data (54); public products comparison (55; App. E); AIS/ADS-B (27); plate motion (38); erosion (40); earthquakes (39); local vs integrated datasets (3, 48); use constraints hydrology/shoalest point (61, 62); roads under buildings (63); home-made datums (9); vector data (59); GCPs (25, 59); S2/H3 (60); location codes (60); innerspace (15, 63); solar panels/antennas (33, 63); crops (64); national security/sovereignty (69); navigation/charting (62); USGS topos/map making/graticules (58); data gaps/shadows/overhangs (35).

**I.4 Suggested trims or merges for a slimmer edition (~45 chapters)**
Merge 1+2 (uses) into one chapter with land/water halves; merge 7+8 (geodesy + horizontal datums); merge 13+14 (IMU + non-GNSS positioning); fold 17 (measurement physics) into sensor chapters; merge 23+24 (SDB + geophysics) as "indirect bathymetry"; merge 28 (cost) into 26 (planning); merge 33 (wires) into 32 (DSM→DTM); merge 40+41 (erosion + change detection); merge 44+45 (resolution + SR); merge 49+50 (metadata + archiving); merge 59+60 (vectors + DGGS); compress Part XIV to three chapters (water domains; built/engineered; living/planetary); fold 72 (history) into Appendix C with a short essay; keep 5, 53, 54, 56 intact — they carry the validation emphasis.

**I.5 Open editorial decisions**
Target length (full ≈ 900–1,100 pages vs slim ≈ 450); whether to maintain BibTeX with DOIs for every "Key references" line; whether to publish the checklists and comparison tables as living web pages; whether each chapter should include a worked exercise with datasets from Appendix H; notation conventions (σ vs RMSE symbols; "DEM" as the generic term); regional balance of examples (currently US/EU/NZ/JP-heavy; add Africa, South America, South/Southeast Asia, Pacific).

---
*End of table of contents.*

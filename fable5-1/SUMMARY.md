# Summary — The Digital Elevation Models Handbook (full edition)

[Front matter](README.md)
[Style guide](STYLE_GUIDE.md)
[Detailed table of contents](TABLE_OF_CONTENTS.md)


## Part I — Why elevation? Uses and users

- [Chapter 1 — The many uses of elevation data on land](chapters/ch01-uses-on-land.md)
- [Chapter 2 — The many uses of bathymetry and topobathymetry](chapters/ch02-uses-bathymetry.md)
- [Chapter 3 — From use to requirement: fitness for use, constraints, and appropriate resolution](chapters/ch03-fitness-for-use.md)

## Part II — Vocabulary and the foundations of correctness

- [Chapter 4 — Names and definitions: DEM, DSM, DTM, and the words that bite](chapters/ch04-names-and-definitions.md)
- [Chapter 5 — Error, uncertainty, accuracy, precision, resolution — the statistical toolkit](chapters/ch05-error-and-uncertainty.md)
- [Chapter 6 — Time as a coordinate: epochs, clocks, synchronization](chapters/ch06-time-as-coordinate.md)

## Part III — Where is "here"? Geodesy, datums, projections

- [Chapter 7 — The shape of the Earth: ellipsoid, geoid, gravity, heights](chapters/ch07-shape-of-the-earth.md)
- [Chapter 8 — Horizontal datums and terrestrial reference frames](chapters/ch08-horizontal-datums.md)
- [Chapter 9 — Vertical datums: orthometric, ellipsoidal, tidal, and home-made](chapters/ch09-vertical-datums.md)
- [Chapter 10 — Map projections, grids, and the resampling they force](chapters/ch10-projections-and-resampling.md)

## Part IV — Positioning and orientation

- [Chapter 11 — A history of positioning: from plumb bobs to PPP](chapters/ch11-history-of-positioning.md)
- [Chapter 12 — GNSS for elevation work](chapters/ch12-gnss.md)
- [Chapter 13 — IMU/INS, motion sensing, and GNSS-aided navigation](chapters/ch13-imu-ins.md)
- [Chapter 14 — Positioning without (or beyond) GNSS: acoustic, terrain-aided, radio, barometric](chapters/ch14-positioning-beyond-gnss.md)
- [Chapter 15 — SLAM: solving the map and the trajectory together (and mapping innerspace)](chapters/ch15-slam.md)

## Part V — Sensors and platforms

- [Chapter 16 — Platforms: feet, cars, boats, drones, kites, aircraft, satellites, fixed infrastructure](chapters/ch16-platforms.md)
- [Chapter 17 — Measurement physics: a unified view (ranging, parallax, interferometry, inversion)](chapters/ch17-measurement-physics.md)
- [Chapter 18 — Topographic lidar](chapters/ch18-topographic-lidar.md)
- [Chapter 19 — Bathymetric lidar and the land–water transition](chapters/ch19-bathymetric-lidar.md)
- [Chapter 20 — Sonar: the many types and how they make bathymetry](chapters/ch20-sonar.md)
- [Chapter 21 — Radar, SAR, InSAR, radar altimetry, and ice-penetrating radar](chapters/ch21-radar-sar-insar.md)
- [Chapter 22 — Photogrammetry, stereo, and structure from motion](chapters/ch22-photogrammetry-sfm.md)
- [Chapter 23 — Optical satellite-derived bathymetry, wave-kinematics bathymetry, and altimetry-predicted bathymetry](chapters/ch23-satellite-derived-bathymetry.md)
- [Chapter 24 — Gravity, magnetics, and other geophysics as mapping aids](chapters/ch24-gravity-magnetics-geophysics.md)
- [Chapter 25 — Calibration: targets, stations, networks, benchmarks, reference surfaces](chapters/ch25-calibration-infrastructure.md)

## Part VI — Planning and operating surveys

- [Chapter 26 — Survey planning for calibration, error reduction, and error monitoring](chapters/ch26-survey-planning.md)
- [Chapter 27 — Moving and transient objects during collection](chapters/ch27-moving-and-transient-objects.md)
- [Chapter 28 — Reducing cost across collection, processing, validation, and use](chapters/ch28-reducing-cost.md)

## Part VII — From sensor data to products

- [Chapter 29 — Processing pipelines: levels, lineage, and what gets lost](chapters/ch29-processing-pipelines.md)
- [Chapter 30 — Point-cloud cleaning, classification, and ground extraction](chapters/ch30-point-cloud-classification.md)
- [Chapter 31 — Interpolation, gridding, and grid registration](chapters/ch31-interpolation-and-gridding.md)
- [Chapter 32 — DSM → DTM: removing objects, and the definitions problem](chapters/ch32-dsm-to-dtm.md)
- [Chapter 33 — Wires, power lines, antennas, and other thin or moving structures](chapters/ch33-wires-and-thin-structures.md)
- [Chapter 34 — Water in DEMs: surfaces, shorelines, hydro-flattening / -enforcement / -conditioning](chapters/ch34-water-in-dems.md)
- [Chapter 35 — Voids, occlusion, shadows, overhangs, and multi-valued surfaces](chapters/ch35-voids-and-overhangs.md)
- [Chapter 36 — Seasonal and environmental variability (leaves, snow, groundwater, crops, steam, tides)](chapters/ch36-seasonal-variability.md)

## Part VIII — The dynamic Earth

- [Chapter 37 — Time scales of surface change](chapters/ch37-time-scales-of-change.md)
- [Chapter 38 — Plate motion, reference-frame dynamics, and vertical land motion](chapters/ch38-plate-motion-and-vlm.md)
- [Chapter 39 — Earthquakes, volcanoes, landslides: sudden deformation and its datum consequences](chapters/ch39-earthquakes-volcanoes-landslides.md)
- [Chapter 40 — Erosion, deposition, and geomorphic change](chapters/ch40-erosion-and-geomorphic-change.md)
- [Chapter 41 — Change detection methods and the minimum detectable change](chapters/ch41-change-detection.md)

## Part IX — Semantics, learning, and enhancement

- [Chapter 42 — Object detection and semantic labelling of the surface](chapters/ch42-object-detection-semantics.md)
- [Chapter 43 — Traditional versus machine-learning methods: a cross-cutting assessment](chapters/ch43-traditional-vs-ml.md)
- [Chapter 44 — Resolution, pixel size, sampling, and oversampling](chapters/ch44-resolution-and-sampling.md)
- [Chapter 45 — Super-resolution and DEM enhancement](chapters/ch45-super-resolution.md)

## Part X — Representing, storing, finding, and keeping elevation data

- [Chapter 46 — Data models: points, waveforms, grids, TINs, meshes, voxels, variable resolution, overviews, splats](chapters/ch46-data-models.md)
- [Chapter 47 — File formats: LAS/LAZ/COPC, GeoTIFF/COG, BAG/S-102, NetCDF/Zarr, DTED, and the rest](chapters/ch47-file-formats.md)
- [Chapter 48 — Compositing: merging many datasets into one product](chapters/ch48-compositing.md)
- [Chapter 49 — Metadata](chapters/ch49-metadata.md)
- [Chapter 50 — Archiving, versioning, and provenance](chapters/ch50-archiving-and-provenance.md)
- [Chapter 51 — Finding the right data: catalogs, STAC, and search](chapters/ch51-finding-data.md)

## Part XI — Validation, quality, and judging data

- [Chapter 52 — Ground truth and calibration/validation datasets](chapters/ch52-ground-truth.md)
- [Chapter 53 — Accuracy assessment and uncertainty quantification in practice](chapters/ch53-accuracy-assessment.md)
- [Chapter 54 — Evaluating other people's data when you lack the full story](chapters/ch54-evaluating-others-data.md)
- [Chapter 55 — Public DEM and bathymetry products: catalog and comparison](chapters/ch55-public-products.md)
- [Chapter 56 — Case files: failures, surprises, and lessons](chapters/ch56-case-files.md)

## Part XII — Visualization and cartography

- [Chapter 57 — Visualizing DEMs: shading, colormaps, filtering, rendering, point clouds, splats](chapters/ch57-visualizing-dems.md)
- [Chapter 58 — Making maps from elevation: topographic maps, charts, graticules, standard elements](chapters/ch58-making-maps.md)

## Part XIII — Vectors, grids, and location codes

- [Chapter 59 — Vector data and DEMs: points, lines, polygons, breaklines, contours, topology](chapters/ch59-vector-data.md)
- [Chapter 60 — Discrete global grids and location codes: S2, H3, geohash, plus codes, what3words, MGRS](chapters/ch60-dggs-and-location-codes.md)

## Part XIV — Domain deep dives

- [Chapter 61 — Hydrologic and hydraulic modeling constraints](chapters/ch61-hydrology.md)
- [Chapter 62 — Navigation and charting from elevation: marine, aviation, drones, vehicles, robots](chapters/ch62-navigation-and-charting.md)
- [Chapter 63 — Buildings, cities, and innerspace](chapters/ch63-buildings-cities-innerspace.md)
- [Chapter 64 — Agriculture, forests, wetlands, and the living surface](chapters/ch64-agriculture-forests-wetlands.md)
- [Chapter 65 — Mining, landfills, construction, and engineered earthworks](chapters/ch65-mining-landfills-earthworks.md)
- [Chapter 66 — Coastal, marine, polar, lakes and rivers](chapters/ch66-coastal-marine-polar-lakes-rivers.md)
- [Chapter 67 — Planetary DEMs: mapping without ground truth](chapters/ch67-planetary-dems.md)

## Part XV — Law, policy, security, privacy, ethics

- [Chapter 68 — Legal issues](chapters/ch68-legal-issues.md)
- [Chapter 69 — National security, sovereignty, privacy, and ethics](chapters/ch69-security-sovereignty-privacy-ethics.md)

## Part XVI — Standards, software, and history

- [Chapter 70 — Survey and product specifications: a guided tour (S-44, HSSD, FPM, LBS, ASPRS, ICAO, INSPIRE…)](chapters/ch70-specifications-guided-tour.md)
- [Chapter 71 — Software landscape: open-source and closed-source by task](chapters/ch71-software-landscape.md)
- [Chapter 72 — How we got here: a history of measuring the shape of the Earth](chapters/ch72-history.md)
- [Chapter 73 — Open problems and the next decade](chapters/ch73-open-problems.md)

## Appendices

- [Appendix A — Glossary](appendices/appendix-a-glossary.md)
- [Appendix B — Mathematical reference](appendices/appendix-b-math-reference.md)
- [Appendix C — Timeline](appendices/appendix-c-timeline.md)
- [Appendix D — Standards and guide documents index](appendices/appendix-d-standards-index.md)
- [Appendix E — Public products comparison tables](appendices/appendix-e-public-products-tables.md)
- [Appendix F — Software index](appendices/appendix-f-software-index.md)
- [Appendix G — Checklists](appendices/appendix-g-checklists.md)
- [Appendix H — Datasets for exercises and benchmarks](appendices/appendix-h-datasets.md)
- [Appendix I — Gap review: what else should be included, and what could be trimmed](appendices/appendix-i-gap-review.md)

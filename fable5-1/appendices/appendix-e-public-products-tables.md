# Appendix E — Public products comparison tables

This appendix condenses the catalog of [Chapter 55](../chapters/ch55-public-products.md) into reference tables. It is deliberately terse: the prose explanations of *why* a given product behaves the way it does live in Chapter 55, the fitness-by-use arguments in [Chapter 3](../chapters/ch03-fitness-for-use.md), and the methods for checking any of these numbers yourself in [Chapters 53](../chapters/ch53-accuracy-assessment.md) and [54](../chapters/ch54-evaluating-others-data.md).

## E.0 How to read these tables

Every table in this appendix is a snapshot taken while the handbook was being written (2025–2026). Public products are re-issued, re-licensed, and occasionally withdrawn, so treat each row as a pointer to the current product handbook, not as a substitute for it.

Column conventions:

- **Type** uses the handbook's vocabulary from [Chapter 4](../chapters/ch04-names-and-definitions.md): **DSM** (first surface the sensor saw), **DTM** (bare earth after removal), **hybrid** (DSM in which only some objects were removed or edited, e.g. water flattened), **model** (interpolated or predicted surface, e.g. gravity-predicted bathymetry). A radar DSM is not a DSM in the optical sense: C-band and X-band penetrate partway into canopy and dry snow, so "DSM (C-band)" means "somewhere between canopy top and ground, depending on cover" ([Chapter 21](../chapters/ch21-radar-sar-insar.md)).
- **Post** is the nominal grid spacing. Arc seconds are written with ″; 1″ ≈ 30.9 m north–south everywhere and 30.9 m × cos(latitude) east–west. Effective resolution is almost always coarser than the post ([Chapter 44](../chapters/ch44-resolution-and-sampling.md)); where a credible estimate exists it is given in the notes.
- **Vertical reference** names the surface heights are counted from. "EGM96" and "EGM2008" are geoid models (heights approximate orthometric H); "WGS 84" means ellipsoidal h. Converting between them changes values by the geoid undulation N, which exceeds 100 m in places (h = H + N; [Chapter 9](../chapters/ch09-vertical-datums.md)). Mixing rows from this table without that conversion is the single most common error in global-DEM work.
- **Reported accuracy** is the producer's figure, in the producer's own statistic. LE90, RMSE, MAE, and "95 %" are not interchangeable: for Gaussian errors LE90 ≈ 1.645 σ, LE95 ≈ 1.96 σ, and MAE ≈ 0.80 σ ([Chapter 5](../chapters/ch05-error-and-uncertainty.md)). Producer figures are typically derived over open, flat, low-slope terrain and are optimistic for forest, cities, and steep slopes. Figures marked "(verify)" could not be confirmed against a primary document at the time of writing.
- **Licence** is summarized. "Public domain" means works of a government that places no restriction (e.g. US federal works). "Free (terms)" means no fee but conditions apply (attribution, no redistribution, registration). NC and SA clauses propagate into derivatives, including machine-learning training sets ([Chapter 68](../chapters/ch68-legal-issues.md)).
- **Dates** are acquisition epochs, not release dates, unless stated. For compilations the epoch varies cell by cell and only a source/date layer tells you which ([Chapter 48](../chapters/ch48-compositing.md)).
- **URL** points at the producer's landing page or the canonical archive. Mirrors (cloud buckets, OpenTopography, Google Earth Engine) are convenient but may lag versions.

General caveats, in order of how often they cause trouble:

1. Void fill is silent. SRTM-family and ASTER products fill voids from other sources; the fill mask is a separate file that most users never download.
2. Water is edited differently everywhere. Copernicus DEM flattens and sets water to an editing-derived value; TanDEM-X raw DEM leaves radar noise; GEBCO land cells come from a land DEM at a different epoch and datum.
3. A "global" product usually stops at some latitude (SRTM at 60°N/56°S) and may have restricted tiles (Copernicus GLO-30 historically omitted a handful of countries at 30 m).
4. Versions matter at the metre level. NASADEM differs from SRTM v3 by several metres in places because of re-unwrapping and ICESat control; FABDEM V1-0 and V1-2 differ where the building/forest masks changed.
5. Accuracy figures are not spatially uniform. Where an independent stratified assessment exists it is cited in the notes; otherwise assume the producer figure degrades by a factor of 2–5 in forest and on slopes above 20°.

## E.1 Global and near-global land DEMs — identity and coverage

| Product | Producer | Type | Post | Acquisition | Coverage | Vertical ref. | URL |
|---|---|---|---|---|---|---|---|
| SRTM v3 (SRTMGL1) | NASA JPL / USGS | DSM (C-band InSAR) | 1″ (3″ also) | 2000-02 (11 days) | 60°N–56°S | EGM96 | https://lpdaac.usgs.gov/products/srtmgl1v003/ |
| NASADEM | NASA JPL | DSM (C-band, reprocessed) | 1″ | 2000-02 (reprocessed 2020) | 60°N–56°S | EGM96 | https://lpdaac.usgs.gov/products/nasadem_hgtv001/ |
| ASTER GDEM v3 | NASA / METI | DSM (optical stereo stack) | 1″ | 2000–2013 (scene stack) | 83°N–83°S | EGM96 | https://lpdaac.usgs.gov/products/astgtmv003/ |
| ALOS AW3D30 v3.2 / v4.1 | JAXA | DSM (optical tri-stereo) | 1″ | 2006–2011 (PRISM) | 82°N–82°S | EGM96 | https://www.eorc.jaxa.jp/ALOS/en/dataset/aw3d30/aw3d30_e.htm |
| TanDEM-X DEM | DLR / Airbus | DSM (X-band InSAR) | 0.4″ (12 m); 1″; 3″ | 2010–2015 (global); Change DEM 2017–2020 | Global incl. poles | WGS 84 ellipsoid | https://geoservice.dlr.de/web/dataguide/tdm90/ |
| TanDEM-X 30 m EDEM | DLR | DSM (X-band, edited) | 1″ | 2010–2015 base | Global | WGS 84 ellipsoid | https://geoservice.dlr.de/web/dataguide/tdm30edem/ |
| Copernicus DEM GLO-30 | ESA / Airbus (EU Copernicus) | DSM (X-band, edited: water, shore, artefacts) | 1″ | 2011–2015 (WorldDEM base) | Global; a few tiles restricted in early releases | EGM2008 | https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model |
| Copernicus DEM GLO-90 | ESA / Airbus | DSM (as GLO-30, resampled) | 3″ | 2011–2015 | Global | EGM2008 | as above |
| Copernicus DEM EEA-10 | ESA / Airbus | DSM | 10 m | 2011–2015 | EEA-39 countries; restricted access | EGM2008 | as above |
| GTOPO30 / GMTED2010 | USGS | DSM/hybrid compilation | 30″ / 7.5″, 15″, 30″ | pre-2010 sources (SRTM-dominated) | Global | EGM96 (nominal) | https://www.usgs.gov/coastal-changes-and-impacts/gmted2010 |
| WorldDEM / WorldDEM Neo | Airbus | DSM (X-band) | 12 m / 5 m | 2011–2015 / 2017– | Global (commercial) | EGM2008 (ellipsoid on request) | https://www.intelligence-airbusds.com/ |

## E.2 Global and near-global land DEMs — accuracy, licence, artefacts

| Product | Reported accuracy (producer) | Independent findings (examples) | Voids / fills | Known artefacts | Uncertainty layer | Licence |
|---|---|---|---|---|---|---|
| SRTM v3 | Spec: 16 m LE90 abs. vertical, 20 m CE90 horizontal (mission spec); Rodríguez et al. 2006: ~6–9 m LE90 by continent | ~3–5 m RMSE open flat; 10–20 m in forest/steep terrain (many studies) | Voids filled from ASTER GDEM2, GMTED2010, NED; fill mask (NUM) provided | Canopy penetration bias (+ several m in forest); speckle; striping (~1–2 m) along-track; phase-unwrapping errors on steep slopes | No | Public domain |
| NASADEM | Improved over SRTM v3 (ICESat/GLAS control; re-unwrapped); no single global figure | Reduced blunders and voids vs. SRTM; residual forest bias unchanged (verify) | Fewer voids; remaining fills from external sources, flagged | As SRTM, reduced striping | No (NUM layer gives source) | Public domain |
| ASTER GDEM v3 | ~8.5 m RMSE vertical vs. GPS benchmarks (CONUS) (verify); horizontal ~ 1 pixel | Noisy at pixel scale ("mole runs", pits/bumps); worse where few scenes stacked | Residual voids filled with SRTM/other; NUM layer gives stack count | Cloud residuals, stacking artefacts, steps between scene stacks | Stack-count layer only | Free (terms; attribution) |
| AW3D30 | ~5 m RMSE vertical (JAXA, from the 5 m parent product; verify for v4.1) | ~3–5 m RMSE open; forest bias (optical DSM = canopy top) | Cloud/snow voids filled from other DEMs in v3+; mask file provided | Matching failures in low-texture areas (snow, sand); seams between strips | No (mask/stack layers) | Free (JAXA terms; attribution; verify redistribution clause) |
| TanDEM-X DEM | Spec: <10 m LE90 abs.; <2 m rel. (slope ≤ 20 %), <4 m rel. (slope > 20 %) per 1°×1° cell | Wessel et al. 2018 and DLR mission summaries: absolute error ≈ 1 m (90 %) on open terrain vs. ICESat/GNSS; much worse in forest and ice | Few voids; no fill in raw DEM; invalid pixels flagged | Penetration into forest, dry snow, ice (metres to tens of m); water noise; residual phase-unwrapping errors in mountains | **Yes** — HEM (height error map) per pixel | 90 m free (DLR terms); 12/30 m by proposal/commercial |
| TanDEM-X 30 m EDEM | As TanDEM-X; water and some artefacts edited | — | Edited voids/water | Residual penetration | HEM | Free (DLR terms) |
| Copernicus GLO-30/90 | Spec: < 4 m LE90 absolute vertical, < 6 m CE90 horizontal (Copernicus DEM Product Handbook, Issue 5.0) | Guth & Geoffroy 2021 and DEMIX: best general global DSM; ~2–3 m RMSE open terrain; forest bias remains (X-band DSM) | Voids filled from other DEMs; editing/fill masks (EDM, FLM, WBM, HEM) distributed | Hydro-edits flatten lakes/rivers; shoreline set to edited value; some terrace-like steps from editing; strip seams rare | HEM inherited from TanDEM-X | Free and open (Copernicus licence; attribution) |
| GMTED2010 | ~26–30 m RMSE at 30″ (source-dependent) | — | Compilation; source layer | Steps between sources | No | Public domain |
| WorldDEM Neo | Spec: ~2.5 m LE90 abs. (Airbus) (verify) | — | — | — | Yes (quality layers) | Commercial |

> **Rule of thumb.** For a global 1″ DSM assume ≈ 3 m RMSE on open terrain with slope < 10°, ≈ 2× that on slopes 10–30°, and a positive bias of 30–70 % of canopy height under closed forest (X/C-band) or ≈ full canopy height (optical). Validate locally before using any smaller number.

## E.3 Derived and corrected global DTMs

These products start from one of the DSMs above and remove or correct something (vegetation, buildings, striping, speckle). Their accuracy inherits the base product's and adds model error; their licences are often more restrictive than their base.

| Product | Base | Correction | Post | Reported accuracy | Licence | URL / reference |
|---|---|---|---|---|---|---|
| MERIT DEM (2017) | SRTM v2.1 + AW3D30 (+ Viewfinder Panoramas at high lat.) | Absolute bias, stripe noise, speckle, tree-height bias removed | 3″ | Fraction of land within ±2 m error improved from ~39 % to ~58 % (Yamazaki et al. 2017) | CC BY-NC 4.0 **or** ODbL 1.0 (dual) | http://hydro.iis.u-tokyo.ac.jp/~yamadai/MERIT_DEM/ |
| MERIT Hydro (2019) | MERIT DEM | Hydrography layers (flow direction, upstream area, HAND) | 3″ | — | CC BY-NC 4.0 / ODbL 1.0 | Yamazaki et al. 2019 |
| FABDEM V1-2 (2023) | Copernicus GLO-30 | Forest and building removal by random forest | 1″ | Hawker et al. 2022: MAE reduced from 1.61 to 1.12 m (built-up) and 5.15 to 2.88 m (forest) vs. lidar at test sites | CC BY-NC-SA 4.0 (commercial licence from Fathom) | https://data.bris.ac.uk/ (search FABDEM) |
| CoastalDEM v2.1 | NASADEM (v2.1) | Neural-network bias correction in coastal lowlands | 1″ | Climate Central reports RMSE ≈ 1–2 m vs. lidar in the US/Australia test regions (verify per version) | Free for non-commercial research; licensed otherwise | https://go.climatecentral.org/coastaldem/ |
| DeltaDTM (2024) | Copernicus GLO-30 + ICESat-2 + GEDI | Coastal lowland (≤ 10 m) DTM by filtering/correction | 1″ | MAE 0.45 m vs. lidar (Pronk et al. 2024) | CC BY 4.0 | https://doi.org/10.4121/21997565 (verify) |
| GEDTM30 (2025) | Multi-source (Copernicus, AW3D30, etc.) + ICESat-2/GEDI | ML ensemble DTM | 1″ | Per Ho et al. 2025; validate locally | CC BY 4.0 | https://github.com/openlandmap/GEDTM30 |
| DiluviumDEM (2023) | Copernicus GLO-30 | ML correction, coastal zones | 1″ | Dusseau et al. 2023 report ~0.7 m RMSE at test sites (verify) | CC BY 4.0 (verify) | Dusseau et al. 2023 |
| GLO-30-derived hydro DEMs (e.g. HydroSHEDS v2) | Copernicus / TanDEM-X | Hydro-conditioned | 3″ | — | Free (terms) | https://www.hydrosheds.org/ |

<!-- figure: Figure E.1 — Lineage diagram: SRTM → NASADEM → CoastalDEM; SRTM+AW3D30 → MERIT → MERIT Hydro; TanDEM-X → Copernicus DEM → FABDEM / DeltaDTM / GEDTM30. Arrows annotated with what was changed. -->

Caveat specific to this table: when two "independent" global DEMs share a parent (e.g. FABDEM and Copernicus), differencing them measures only the correction, not the error. Use ICESat-2 ATL08/ATL06 terrain photons or airborne lidar as the third party ([Chapter 52](../chapters/ch52-ground-truth.md)).

## E.4 Polar and high-latitude DEMs

| Product | Producer | Type | Post | Acquisition | Vertical ref. | Accuracy / registration | Licence & URL |
|---|---|---|---|---|---|---|---|
| ArcticDEM strips (v4) | PGC (U. Minnesota) with NGA/NSF | DSM (optical stereo, SETSM) | 2 m | 2007– (time-stamped strips, ongoing) | WGS 84 ellipsoid | Strips registered to ICESat-2 (ATL06) where possible; residual blunders in clouds/water/low texture | CC BY 4.0 (most data; some post-2022 Alaska strips restricted by EOCL licensing); https://www.pgc.umn.edu/data/arcticdem/ |
| ArcticDEM mosaic v4.1 | PGC | DSM composite | 2 m, 10 m, 32 m | strips 2007–2022 (verify end) | WGS 84 ellipsoid | Mosaic cells from different years; use strips for change | as above |
| REMA strips / mosaic v2 | PGC | DSM | 2 m (strips); 2, 10, 32 m (mosaic) | 2009– | WGS 84 ellipsoid | ICESat-2 registered; ~m-level absolute on stable terrain | https://www.pgc.umn.edu/data/rema/ |
| EarthDEM | PGC | DSM | 2 m | 2010s– | WGS 84 ellipsoid | Non-polar extension; partial coverage | Access varies by region (verify) |
| Copernicus / TanDEM-X at high latitude | ESA / DLR | DSM (X-band) | 1″ | 2011–2015 | EGM2008 / ellipsoid | Dry-snow and firn penetration (several m to > 10 m on ice sheets) | as E.1 |
| Greenland GIMP DEM | NSIDC / Howat et al. | DSM | 30 m (90 m) | ~2007 nominal | WGS 84 ellipsoid | ~±10 m typical; better on bare rock | Free; https://nsidc.org/data/nsidc-0645 |
| Antarctic ice surface (Bedmap/REMA-based) | BAS / NSIDC | DSM | 500 m–1 km | compilation | WGS 84 ellipsoid | — | Free |

Polar caveats: (1) ellipsoidal heights throughout — do not compare with EGM-referenced DEMs without conversion (N ranges roughly −60 m to +60 m over Antarctica and Greenland); (2) the surface is moving — ice-sheet surface elevation changes by up to several metres per year near outlet glaciers, so the strip date is part of the coordinate ([Chapter 37](../chapters/ch37-time-scales-of-change.md), [Chapter 66](../chapters/ch66-coastal-marine-polar-lakes-rivers.md)); (3) ArcticDEM/REMA mosaics mix years; the accompanying date raster is mandatory for any change study.

## E.5 National and regional high-resolution programs (lidar and photogrammetric DTMs)

National programs are where sub-decimetre vertical accuracy exists. Their specifications differ in statistic (RMSE vs. 1σ vs. 95 %), in land-cover stratification (NVA/VVA in the United States; "Class I/II" in Finland), and in what "ground" includes ([Chapter 32](../chapters/ch32-dsm-to-dtm.md)). Figures below are the program specifications unless stated; actual delivered accuracy is usually better in open terrain and documented per project.

| Program (country) | Producer | Products | Post | Vertical ref. | Spec / reported accuracy | Licence | URL |
|---|---|---|---|---|---|---|---|
| 3DEP (USA) | USGS with partners | Lidar point clouds (LAZ), 1 m DTM, 1/3″ & 1″ seamless; some topobathy | 1 m (QL2/QL1); 1/3″; 1″ | NAVD88 via GEOID12B/18 (project-specific); Alaska/territories vary | QL2: NVA ≤ 10 cm RMSE_z (19.6 cm at 95 %), VVA ≤ 30 cm at 95th percentile; NPS ≤ 0.71 m (≥ 2 pts/m²); QL1 ≥ 8 pts/m² | Public domain | https://www.usgs.gov/3d-elevation-program |
| National LIDAR Programme (England) | Environment Agency | 1 m DTM/DSM composites, time-stamped tiles, point clouds | 1 m (older 25 cm–2 m) | ODN (Newlyn) via OSGM15 | ±15 cm RMSE specification; EA reports typically better (verify current spec) | Open Government Licence v3 | https://environment.data.gov.uk/ |
| Scotland / Wales lidar | Scottish Government / NRW | DTM/DSM | 0.5–2 m | ODN | project-specific | OGL | https://remotesensingdata.gov.scot/ ; https://datamap.gov.wales/ |
| AHN (Netherlands) | Het Waterschapshuis / Rijkswaterstaat / provinces | AHN1–AHN5 point clouds, 0.5 m DTM/DSM | 0.5 m (5 m also) | NAP | AHN3/4 spec: systematic ≤ 5 cm, stochastic ≤ 5 cm (1σ) on hard surfaces; ≥ 10–20 pts/m² (AHN4 higher) (verify AHN5 spec) | CC0 1.0 | https://www.ahn.nl/ ; https://www.pdok.nl/ |
| swissALTI3D (Switzerland) | swisstopo | DTM (and swissSURFACE3D DSM / point cloud) | 0.5 m, 2 m | LN02 / LHN95 (Swiss) | 1σ: ≈ 0.3 m (new lidar); 0.5 m (older lidar < 2,000 m); 1–3 m (stereo > 2,000 m, being replaced) | Open Government Data (free, attribution) | https://www.swisstopo.admin.ch/en/height-model-swissalti3d |
| DHM (Denmark) | SDFI / Klimadatastyrelsen (agency names change; verify) | DTM/DSM, point cloud, derived (hydro-adjusted) | 0.4 m (also 1, 5, 20 m) | DVR90 | Vertical accuracy ≈ 5 cm (stated for the 0.4 m grid); ≥ 4–5 pts/m² | Open (Danish open data terms) | https://dataforsyningen.dk/ |
| NLS elevation model (Finland) | Maanmittauslaitos (NLS) | 2 m DTM (KM2), 10 m; point clouds (5 pts/m² newer) | 2 m | N2000 | Class I: ≈ 0.3 m mean elevation accuracy; Class II: 0.3–1 m (older data) | CC BY 4.0 | https://www.maanmittauslaitos.fi/en/maps-and-spatial-data/datasets-and-interfaces |
| NDH (Norway) | Kartverket | DTM1 / DOM1, point clouds | 1 m (10 m, 50 m) | NN2000 | ≥ 2 pts/m² (5 in places); vertical accuracy project-specific (≈ 10–20 cm typical) (verify) | NLOD / CC BY 4.0 | https://hoydedata.no/ |
| GSI DEM (Japan) | Geospatial Information Authority of Japan | 5 m mesh (DEM5A lidar, 5B photogrammetric, 5C), 10 m mesh, 1 m mesh for selected areas | 5 m; 10 m; 1 m | Tokyo Peil (T.P.) via Japanese geoid | DEM5A: 0.3 m (1σ); DEM5B: 0.7 m; DEM5C: 1.4 m; 10 m: 5 m | Free (GSI terms; attribution; verify commercial clause) | https://fgd.gsi.go.jp/download/ |
| ELVIS / national 5 m DEM (Australia) | Geoscience Australia with states | Lidar tiles (1 m, state programs), 5 m DEM (lidar compilation), 1″ SRTM-derived DEM-S/DEM-H | 1 m; 5 m; 1″ | AHD (AUSGeoid2020) | ICSM lidar spec: ≤ 0.30 m vertical, ≤ 0.80 m horizontal (95 %); better in practice (≈ 10–15 cm RMSE for 1 m products) | CC BY 4.0 (most) | https://elevation.fsdf.org.au/ |
| LINZ lidar (New Zealand) | LINZ with regional councils | Point clouds, 1 m DEM/DSM | 1 m | NZVD2016 | Vertical ≤ 0.2 m at 95 % (spec), horizontal ≤ 1 m (verify) | CC BY 4.0 | https://data.linz.govt.nz/ |
| RGE ALTI / LiDAR HD (France) | IGN | RGE ALTI 1 m/5 m; LiDAR HD point clouds and DTM/DSM | 1 m (0.5 m LiDAR HD) | NGF-IGN69 (RAF geoid) | LiDAR HD: ≥ 10 pts/m²; vertical ≈ 10 cm (spec) (verify) | Licence Ouverte (Etalab) 2.0 | https://geoservices.ign.fr/lidarhd |
| Germany (Länder) | 16 state surveying agencies (e.g. Bavaria, NRW) | DGM1 / DOM1, point clouds | 1 m (some 0.5 m) | DHHN2016 via GCG2016 | ≈ 10–20 cm (state-specific) | Varies: many now DL-DE/BY-2.0 or CC BY 4.0 | state portals (e.g. https://www.opengeodata.nrw.de/) |
| Spain PNOA-LiDAR | IGN España (CNIG) | Point clouds (1st & 2nd coverage), MDT02/05/25 | 2 m, 5 m | REDNAP (EGM08-REDNAP) | 1st coverage 0.5 pts/m², 2nd ≥ 1–2 pts/m²; vertical ≈ 20 cm RMSE (verify) | CC BY 4.0 | https://centrodedescargas.cnig.es/ |
| Italy, Austria, Poland, Estonia, Latvia, Slovenia, Czechia | national/regional agencies | Lidar DTM/DSM | 0.5–5 m | national | varies | mostly open (verify per country) | national geoportals |
| Canada HRDEM / CanElevation | NRCan | HRDEM (lidar/stereo), MRDEM 30 m | 1–2 m; 30 m | CGVD2013 | lidar projects ≤ 10–20 cm (verify) | Open Government Licence – Canada | https://open.canada.ca/ (search HRDEM) |

<!-- figure: Figure E.2 — World map of national lidar coverage status (complete / in progress / none), with insets for Europe and a bar chart of the fraction of each country mapped at ≤ 1 m post. -->

Caveats specific to national programs: (1) national vertical datums (NAVD88, ODN, NAP, LN02, DVR90, N2000, NN2000, T.P., AHD, NZVD2016, NGF, DHHN2016, CGVD2013) differ from one another and from EGM2008 by decimetres to a metre or more; the geoid model used to realize each differs by version ([Chapter 9](../chapters/ch09-vertical-datums.md)); (2) programs mix epochs — a 1 m "national" DTM may span 10–15 years of flights; (3) hydro-flattening and breakline rules differ (3DEP requires hydro-flattening of water bodies ≥ 2 acres (≈ 0.8 ha); many European programs do not flatten); (4) the US 3DEP spec quotes RMSE_z and 95 % figures that assume Gaussian errors in non-vegetated terrain; the VVA is a 95th percentile and is not an RMSE.

## E.6 Global and regional bathymetry

| Product | Producer | Type | Post | Vertical ref. | What is measured vs. predicted | Licence | URL |
|---|---|---|---|---|---|---|---|
| GEBCO_2025 Grid | GEBCO / Nippon Foundation–GEBCO Seabed 2030 | Bathy + topo compilation | 15″ | MSL (nominal; sources mixed) | ≈ 27.3 % of the ocean floor mapped by direct measurement at grid resolution (Seabed 2030, June 2025; later figures: verify against seabed2030.org); rest from altimetry-predicted base (SRTM15+). TID grid gives per-cell source type | Free (public domain-like GEBCO terms; attribution) | https://www.gebco.net/ |
| SRTM15+ V2.x | SIO (Scripps) / Tozer et al. 2019 | Bathy + topo | 15″ | MSL | Gravity (altimetry)-predicted bathymetry constrained by soundings; the base of GEBCO | Free | https://topex.ucsd.edu/WWW_html/srtm15_plus.html |
| ETOPO 2022 | NOAA NCEI | Bathy + topo (ice surface and bedrock versions) | 15″; 30″; 60″ | EGM2008 (geoid version) and WGS 84 ellipsoid version | Compilation (GEBCO, regional DEMs, BedMachine, CopDEM on land) | Public domain | https://www.ncei.noaa.gov/products/etopo-global-relief-model |
| GMRT | Lamont-Doherty (LDEO) | MBES synthesis + background | ~100 m where MBES; multi-res tiles | MSL | Measured only where ship MBES exists (curated cruises); elsewhere GEBCO/SRTM15+ background | Free (attribution) | https://www.gmrt.org/ |
| EMODnet Bathymetry DTM 2024 | EMODnet (EU) | Bathy DTM compilation | 1/16′ (≈ 115 m) | LAT (with MSL conversion layer) | Compiled from ≈ 22,000 survey/CDI references; source-reference layer per cell; gaps filled with GEBCO | Free (CC BY 4.0 for DTM; source data vary) | https://emodnet.ec.europa.eu/en/bathymetry |
| IBCAO v5 | IBCAO / GEBCO | Arctic bathy | 100 m (v5; earlier 200 m) | MSL | Source/TID grid; large predicted areas under permanent ice | Free | https://www.gebco.net/data-products/gridded-bathymetry-data/arctic-ocean |
| IBCSO v2 | AWI / SCAR | Southern Ocean bathy (south of 50°S) | 500 m | MSL | TID grid; annual releases since 2022 | Free (CC BY 4.0) | https://ibcso.org/ |
| NOAA BlueTopo (NBS) | NOAA OCS | US bathy compilation, continuously updated | 2–16 m, varies by region (tile-based) | MLLW (ellipsoid separation via VDatum) | Per-cell **Elevation**, **Uncertainty**, **Contributor** layers; supersession rules; "not for navigation" | Public domain | https://nauticalcharts.noaa.gov/data/bluetopo.html |
| NCEI CUDEM | NOAA NCEI / OCM | Topobathy tiles (coastal US) | 1/9″ (≈ 3 m), 1/3″, some 1/27″ | NAVD88 (CONUS) or MHW variants — check per tile set | Compilation of lidar, MBES, charts; per-tile source documentation | Public domain | https://www.ncei.noaa.gov/products/coastal-elevation-models |
| NCEI Coastal Relief Model (CRM) | NOAA NCEI | Topobathy | 1″ (2023+; older 3″) | MHW / NAVD88 (verify by volume) | Compilation | Public domain | as above |
| USACE eHydro / NCMP (JALBTCX) | USACE | Channel surveys; coastal topobathy lidar | survey-specific; 1 m | MLLW / NAVD88 | Measured (SBES/MBES; bathy lidar) | Public domain | https://navigation.usace.army.mil/Survey/Hydro ; https://coast.noaa.gov/dataviewer/ |
| AusSeabed / Australian Bathymetry and Topography Grid | Geoscience Australia | Compilation + MBES grids | 250 m national; survey grids finer | MSL (national); LAT for some | Source layer | CC BY 4.0 | https://www.ausseabed.gov.au/ |
| Japan JHOD J-EGG500 / M7000 | Japan Coast Guard / JHA | Compilation | 500 m; chart-based | MSL / chart datum | — | Free / licensed (verify) | https://www1.kaiho.mlit.go.jp/ |
| Great Lakes bathymetry | NOAA NCEI | Lake bathy | 3″ (≈ 90 m); newer finer | IGLD 1985 | Compilation | Public domain | https://www.ncei.noaa.gov/ |

> **Definitions that bite.** "Depth" in a bathymetric grid is positive-down in charts and most hydrographic software, but negative-up (elevation) in GEBCO, ETOPO, BlueTopo, and CUDEM. Check the sign convention and the datum (MSL vs. LAT vs. MLLW) before merging with land data; the LAT–MSL separation alone is 1–6 m in macrotidal seas ([Chapter 34](../chapters/ch34-water-in-dems.md), [Chapter 62](../chapters/ch62-navigation-and-charting.md)).

Bathymetric caveats: (1) a cell-by-cell **source/TID layer** is the only honest accuracy statement for a compilation — a 15″ GEBCO cell may be a modern MBES average or a gravity prediction with ±100–200 m uncertainty in the deep ocean ([Chapter 23](../chapters/ch23-satellite-derived-bathymetry.md)); (2) grids are not charts: none of these products is authorized for navigation, and shoalest-point preservation is not guaranteed by mean-value gridding ([Chapter 61](../chapters/ch61-hydrology.md), [Chapter 62](../chapters/ch62-navigation-and-charting.md)); (3) compilations inherit sounding datums and sound-speed corrections of their sources, which are often undocumented for pre-1990 data.

## E.7 Sub-ice bed, ice thickness, and ice-surface products

| Product | Producer | Content | Post | Vertical ref. | Method | Uncertainty | Licence & URL |
|---|---|---|---|---|---|---|---|
| BedMachine Greenland v5 | NASA / UC Irvine (Morlighem et al.) | Bed, surface, thickness, mask, error | 150 m | WGS 84 ellipsoid (geoid offset layer supplied) | Mass conservation + radar sounding + bathymetry | Per-cell error grid | Free (NSIDC, NASA data policy); https://nsidc.org/data/idbmg4 |
| BedMachine Antarctica v3 | NASA / UC Irvine | Bed, surface, thickness, firn, error | 500 m | WGS 84 ellipsoid (geoid offset layer) | Mass conservation + radar + gravity inversion under shelves | Per-cell error grid | Free; https://nsidc.org/data/nsidc-0756 |
| Bedmap3 (2025) | BAS / SCAR | Bed, surface, thickness; point data | 500 m | geoid (EIGEN-6C4-based; verify) | Interpolation of ≈ 82 million survey points (Pritchard et al. 2025) | Uncertainty grid | Free (CC BY 4.0); https://www.bas.ac.uk/project/bedmap/ |
| ArcticDEM / REMA (ice surface) | PGC | DSM | 2 m | WGS 84 ellipsoid | Optical stereo | strip-dependent | see E.4 |
| ICESat-2 ATL06 / ATL11 / ATL14-15 | NASA | Land-ice height, time series, gridded height & change | along-track 20 m / 100 m grid (ATL14) | WGS 84 ellipsoid (ITRF2014) | Photon-counting lidar | Per-segment σ | Free; https://nsidc.org/data/icesat-2 |
| CryoSat-2 / CryoTEMPO | ESA | Ice-sheet, sea-ice, polar ocean elevations | along-track; gridded products 1–2 km | WGS 84 ellipsoid | Radar altimetry (SARIn) | Per-product | Free (ESA terms) |

## E.8 Planetary DEMs (selected)

Planetary DEMs are referenced to body-specific shapes (Mars areoid; lunar sphere of radius 1,737.4 km) and lack ground control; see [Chapter 67](../chapters/ch67-planetary-dems.md) for how their quality is established.

| Product | Body | Producer | Post | Vertical ref. | Reported accuracy | Licence | URL |
|---|---|---|---|---|---|---|---|
| MOLA MEGDR | Mars | NASA GSFC (MGS) | 128 ppd (≈ 463 m/px at equator); 463 m polar | Areoid (MOLA/GMM-3 based) | Radial ≈ 1 m (profile points); horizontal ≈ 100 m; grid interpolated between tracks | Public domain (NASA PDS) | https://pds-geosciences.wustl.edu/missions/mgs/megdr.html |
| HRSC MOLA blended DEM (Fergason et al. 2018) | Mars | USGS Astrogeology | 200 m | Areoid | Blends HRSC DTMs with MOLA | Public domain | https://astrogeology.usgs.gov/ |
| HRSC single-strip DTMs / MC-quadrangle DTMs (e.g. MC-11) | Mars | DLR / FU Berlin | 50–100 m | Areoid | Vertical ≈ 10–20 m typical (strip-dependent) (verify) | ESA/DLR terms (free) | https://hrscteam.dlr.de/ |
| CTX stereo DEMs (e.g. Murray Lab global mosaic for images; ASP-derived DEMs) | Mars | Various; Caltech Murray Lab (mosaic) | 18–24 m | Areoid, tied to MOLA | Tied to MOLA by alignment; relative precision few m | Public domain | https://murray-lab.caltech.edu/CTX/ |
| HiRISE DTMs | Mars | UA / USGS | 1–2 m | Areoid, tied to MOLA | Vertical precision ≈ 0.1–0.5 m relative (verify); absolute inherits MOLA tie | Public domain | https://www.uahirise.org/dtm/ |
| LOLA LDEM | Moon | NASA GSFC (LRO) | 256 ppd (≈ 118 m) global; up to 5 m/px polar | Sphere r = 1,737.4 km | Vertical ≈ 1 m (accuracy), 0.1 m precision; gaps between tracks at low latitudes | Public domain | https://pds-geosciences.wustl.edu/missions/lro/lola.htm |
| SLDEM2015 | Moon | GSFC / JAXA (LOLA + Kaguya TC) | 512 ppd (≈ 60 m) | Sphere r = 1,737.4 km | ≈ 3–4 m vertical (Barker et al. 2016) | Public domain | as LOLA |
| LRO NAC DTMs | Moon | ASU / USGS | 2–5 m | Sphere | Tied to LOLA; sub-m relative (verify) | Public domain | https://wms.lroc.asu.edu/lroc/rdr_product_select |
| MESSENGER MLA / USGS Mercury DEM | Mercury | NASA / USGS | 665 m (global) | Sphere r = 2,439.4 km | ~ km-scale gaps in south; stereo-derived | Public domain | https://astrogeology.usgs.gov/ |
| Magellan GTDR | Venus | NASA | ≈ 4.6 km (4,641 m/px) | Sphere r = 6,051.0 km | Radar altimetry; coarse | Public domain | NASA PDS |
| OSIRIS-REx Bennu / Hayabusa2 Ryugu shape models | Asteroids | NASA / JAXA | cm–m facets | Body-centred | — | Public domain / JAXA terms | PDS / DARTS |

Planetary caveats: (1) altimeter grids are interpolated between tracks — the MOLA grid at 463 m has true information content of only a few hundred metres along-track and kilometres across-track at low latitude; (2) stereo DEMs are tied to altimetry by bulk alignment, so absolute error is the altimeter's plus alignment residuals; (3) longitude conventions differ (planetocentric east-positive vs. planetographic west-positive) and have caused errors of the same class as datum mistakes on Earth ([Chapter 67](../chapters/ch67-planetary-dems.md)).

## E.9 Quick chooser

| Need | First choice | Also consider | Avoid |
|---|---|---|---|
| Global 30 m DSM, general | Copernicus GLO-30 | TanDEM-X 30 m EDEM; AW3D30 | ASTER GDEM alone |
| Global 30 m "bare earth" for flood/lowland | FABDEM (if NC acceptable), DeltaDTM (coastal), GEDTM30 | MERIT (90 m) | Raw SRTM in forest |
| Global 30 m with ellipsoidal heights | TanDEM-X (native ellipsoid) | Copernicus + EGM2008 undulation | Mixing EGM96/EGM2008 rows |
| Change detection, polar | ArcticDEM / REMA strips (dated) | ICESat-2 ATL06 | Mosaics (mixed epochs) |
| Sub-decimetre terrain, any country with a program | National lidar (E.5) | — | Any global product |
| Deep-ocean context | GEBCO (with TID) | SRTM15+; GMRT (where MBES) | Treating predicted cells as measured |
| US coastal topobathy | CUDEM (check datum variant); BlueTopo for bathy | USACE NCMP | Products with undocumented datum |
| European shelf | EMODnet (with source layer) | national hydrographic offices | — |
| Teaching the limits of DEMs | A DEMIX tile with all of the above | Appendix H | — |

## E.10 References for this appendix

- Barker, M. K., et al. (2016). A new lunar digital elevation model from the Lunar Orbiter Laser Altimeter and SELENE Terrain Camera. *Icarus*, 273:346–355.
- Dusseau, D., Zobel, Z., & Schwalm, C. R. (2023). DiluviumDEM: Enhanced accuracy in global coastal digital elevation models. *Remote Sensing of Environment*, 298:113812.
- Fergason, R. L., Hare, T. M., & Laura, J. (2018). HRSC and MOLA blended digital elevation model at 200m v2. USGS Astrogeology. (verify)
- Frémand, A. C., et al. (2023). Antarctic Bedmap data: Findable, Accessible, Interoperable, and Reusable (FAIR) sharing of 60 years of ice bed, surface, and thickness data. *Earth System Science Data*, 15:2695–2710.
- Guth, P. L., & Geoffroy, T. M. (2021). LiDAR point cloud and ICESat-2 evaluation of 1 second global digital elevation models: Copernicus wins. *Transactions in GIS*, 25(5):2245–2261.
- Hawker, L., et al. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters*, 17(2):024016.
- Ho, Y.-F., Grohmann, C. H., Lindsay, J., Reuter, H. I., Parente, L., Witjes, M., & Hengl, T. (2025). Global ensemble digital terrain modeling and parametrization at 30 m resolution (GEDTM30): a data fusion approach based on ICESat-2, GEDI and multisource data. *PeerJ*, 13:e19673.
- Jakobsson, M., et al. (2020). The International Bathymetric Chart of the Arctic Ocean Version 4.0. *Scientific Data*, 7:176.
- Jakobsson, M., Mohammad, R., Karlsson, M., et al. (2024). The International Bathymetric Chart of the Arctic Ocean Version 5.0. *Scientific Data*, 11:1420.
- Pritchard, H. D., et al. (2025). Bedmap3 updated ice bed, surface and thickness gridded datasets for Antarctica. *Scientific Data*, 12:414. (verify pages)
- Kulp, S. A., & Strauss, B. H. (2018). CoastalDEM: A global coastal digital elevation model improved from SRTM using a neural network. *Remote Sensing of Environment*, 206:231–239.
- Morlighem, M., et al. (2017). BedMachine v3: Complete bed topography and ocean bathymetry mapping of Greenland from multibeam echo sounding combined with mass conservation. *Geophysical Research Letters*, 44:11,051–11,061.
- Morlighem, M., et al. (2020). Deep glacial troughs and stabilizing ridges unveiled beneath the margins of the Antarctic ice sheet. *Nature Geoscience*, 13:132–137.
- NASA JPL (2020). NASADEM Merged DEM Global 1 arc second V001. LP DAAC.
- Pronk, M., et al. (2024). DeltaDTM: A global coastal digital terrain model. *Scientific Data*, 11:273.
- Rizzoli, P., et al. (2017). Generation and performance assessment of the global TanDEM-X digital elevation model. *ISPRS Journal of Photogrammetry and Remote Sensing*, 132:119–139.
- Rodríguez, E., Morris, C. S., & Belz, J. E. (2006). A global assessment of the SRTM performance. *Photogrammetric Engineering & Remote Sensing*, 72(3):249–260.
- Smith, D. E., et al. (2001). Mars Orbiter Laser Altimeter: Experiment summary after the first year of global mapping of Mars. *Journal of Geophysical Research*, 106(E10):23689–23722.
- Tadono, T., et al. (2014). Precise global DEM generation by ALOS PRISM. *ISPRS Annals*, II-4:71–76.
- Tozer, B., et al. (2019). Global bathymetry and topography at 15 arc sec: SRTM15+. *Earth and Space Science*, 6(10):1847–1864.
- Wessel, B., et al. (2018). Accuracy assessment of the global TanDEM-X Digital Elevation Model with GPS data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 139:171–182.
- Yamazaki, D., et al. (2017). A high-accuracy map of global terrain elevations. *Geophysical Research Letters*, 44:5844–5853.
- Yamazaki, D., et al. (2019). MERIT Hydro: A high-resolution global hydrography map based on latest topography dataset. *Water Resources Research*, 55:5053–5073.
- Abrams, M., Crippen, R., & Fujisada, H. (2020). ASTER Global Digital Elevation Model (GDEM) and ASTER Global Water Body Dataset (ASTWBD). *Remote Sensing*, 12(7):1156.
- Airbus Defence and Space. Copernicus DEM — Copernicus Digital Elevation Model Product Handbook, GEO1988-CopernicusDEM-SPE-002, Issue 5.0 (current issue at time of writing).
- Heidemann, H. K. (2018). Lidar Base Specification, v2.1 (USGS Techniques and Methods 11-B4); superseded by the online Lidar Base Specification, current revision 2024 rev. A.

# Appendix G — Checklists

These checklists condense the handbook into things you can tick off. Each item has a one-line rationale and a pointer to the chapter that explains it. They are written for the person who has to sign something: a survey plan, an acceptance report, a fitness-for-use memo, a data release. Use them as a floor, not a ceiling; project specifications ([Chapter 70](../chapters/ch70-specifications-guided-tour.md)) override them where stricter.

Conventions: **(must)** marks items whose omission has caused documented failures ([Chapter 56](../chapters/ch56-case-files.md)); other items are strongly recommended. Copy the Markdown into your project repository and keep the ticked version with the deliverable — the completed checklist is itself provenance ([Chapter 50](../chapters/ch50-archiving-and-provenance.md)).

## G.1 Survey planning (before commissioning or bidding)

Reference: [Chapter 26](../chapters/ch26-survey-planning.md), [Chapter 3](../chapters/ch03-fitness-for-use.md), [Chapter 25](../chapters/ch25-calibration-infrastructure.md).

- [ ] **Use and decision defined (must).** Write down who will use the data, for what decision, and what a wrong answer costs. Every later number (resolution, accuracy, currency) derives from this. — Ch. 3
- [ ] **Surface type specified.** DSM, DTM, or both; inclusion rules for bridges, culverts, buildings, piers, vegetation; water treatment (flattened? enforced? measured?). — Ch. 4, 32, 34
- [ ] **Resolution and point density derived from use, not from the sensor brochure.** State nominal post, required effective resolution, and minimum pulse/sounding density, with the smallest feature that must be resolved. — Ch. 44
- [ ] **Accuracy requirement in a named statistic and standard.** E.g. "NVA ≤ 10 cm RMSE_z, VVA ≤ 30 cm 95th percentile per USGS LBS 2020" or "RMSE_V ≤ 10 cm per ASPRS Ed. 2 (2023)" or "IHO S-44 Ed. 6 Order 1a TVU". Avoid "±10 cm" with no statistic. — Ch. 5, 53, 70
- [ ] **Currency requirement.** How old may the data be at delivery, and how long will it remain valid for the use? Decide re-survey triggers. — Ch. 37
- [ ] **Datums, geoid, epoch written in full (must).** Horizontal frame and epoch (e.g. ITRF2020 at 2025.5 or NAD83(2011) epoch 2010.0); vertical datum and realization (NAVD88 via GEOID18; LAT via a named separation model); units (m; never "feet" without specifying which foot). — Ch. 8, 9, 56.6
- [ ] **Control plan.** CORS/base stations with baseline lengths; passive marks to be occupied; GCPs for photogrammetry; **independent** checkpoints (different crew, instrument, or at least not used in adjustment) stratified by land cover and slope, with the sample size justified (ASPRS: ≥ 30 per stratum as a minimum, more for large areas). — Ch. 25, 52, 53
- [ ] **Calibration plan.** Boresight/lever-arm procedure and dates; patch test or calibration range; reference surfaces (flat, hard, open) inside the project area; sound-speed profile cadence for sonar; camera calibration currency. — Ch. 13, 18, 20, 25
- [ ] **Redundancy for self-checking.** Swath overlap (≥ 20–30 % lidar sidelap typical; 100 % + for MBES feature detection), crosslines (≥ 5 % of line-km or per spec), repeat lines over the calibration surface at start and end of each sortie. — Ch. 25.8, 26.2
- [ ] **Environmental windows.** Leaf-off/leaf-on, snow-free, tide windows (bathy lidar at low water; shoreline at a defined stage), turbidity, wind/sea state, sun angle for imagery, groundwater/soil-moisture season for radar. — Ch. 36, 26.4
- [ ] **Moving-object strategy.** Time of day/week for traffic; AIS/ADS-B logging to mask ships and aircraft; construction schedules; smoke/steam sources mapped. — Ch. 27
- [ ] **Tide/water-level plan (bathy).** Gauges or GNSS-ellipsoid reduction; separation model and its uncertainty; zoning. — Ch. 9, 20, 62
- [ ] **Deliverables list with formats and companion layers.** Point clouds (LAZ 1.4, classification scheme), DTM/DSM (COG, pixel convention stated), uncertainty raster, source/date raster, void mask, breaklines, control report, metadata (ISO 19115 / FGDC), processing report. — Ch. 47, 48.7, 49
- [ ] **Acceptance tests and who runs them.** Independent QC (not the producer) with pass/fail thresholds, sample design, and a re-fly clause. — Ch. 53, 56.23
- [ ] **Permits, airspace, access, privacy.** UAS authorizations, marine notices, landowner access, data-protection assessment for imagery over dwellings. — Ch. 26.8, 68, 69
- [ ] **Licence and archiving terms (must).** Who owns the raw data, may the public reuse it, which repository receives raw + processed, retention period. — Ch. 50, 68
- [ ] **Risk register and contingency.** Weather days, GNSS outages/jamming, sensor failure, re-survey budget. — Ch. 26.9, 56.19

## G.2 Field and acquisition (during the survey)

Reference: [Chapter 26](../chapters/ch26-survey-planning.md) §26.5, [Chapter 12](../chapters/ch12-gnss.md), [Chapter 13](../chapters/ch13-imu-ins.md), [Chapter 18](../chapters/ch18-topographic-lidar.md)–[20](../chapters/ch20-sonar.md).

- [ ] **Time synchronization verified (must).** All sensors on GNSS time (PPS + NMEA or PTP); logged offsets; a 1 ms timing error at 50 m/s is 5 cm along-track. — Ch. 6, 13
- [ ] **Base station / CORS health.** Base coordinates in the project frame and epoch; antenna height measured twice (slant and vertical); logging rate ≥ rover rate; baseline length within spec; PDOP and satellite count logged. — Ch. 12
- [ ] **IMU alignment and dynamics.** Static alignment time observed; figure-eights/S-turns before and after lines (airborne) or before survey (marine); no long straight-and-level periods beyond the IMU drift budget. — Ch. 13
- [ ] **Lever arms and offsets re-measured if anything was moved.** Record with photos; sign conventions written on the sheet. — Ch. 13, 25
- [ ] **Calibration lines flown/sailed** at start and end (and daily on long projects); patch test on a slope and a flat area with a feature. — Ch. 25
- [ ] **Sound-speed profiles (sonar)** at the interval dictated by observed variability; surface sound speed continuous; compare profile to surface sensor. — Ch. 20
- [ ] **Water-level/tide logging** running with time stamps in UTC; gauge datum tie checked against a benchmark. — Ch. 9, 20
- [ ] **Real-time coverage and density monitoring.** Gaps, dropouts, and low-density areas flagged for re-fly before leaving site; swath coverage ≥ spec. — Ch. 26.5, 35
- [ ] **Environmental log.** Wind, sea state, visibility, cloud, snow cover, water level, leaf state, turbidity (Secchi/Kd) — the things the metadata will need. — Ch. 36, 49
- [ ] **Moving-object log.** Note trains, ships, cranes, traffic jams, fires, steam plumes seen during lines; keep AIS/ADS-B logs with the raw data. — Ch. 27
- [ ] **Checkpoint survey executed independently.** RTK/PPK with a different base or network solution than the airborne/marine trajectory; occupation times and fix quality recorded; hard, flat, open surfaces for NVA; stratified vegetation for VVA. — Ch. 52, 53
- [ ] **Raw data integrity.** Checksums on raw logs daily; two copies in two places before leaving site; file naming with UTC date/time. — Ch. 29, 50
- [ ] **Daily QC report.** Trajectory separation (forward/reverse), line-to-line height differences on overlaps, intensity/backscatter sanity, GNSS outages, anomalies. — Ch. 26.5
- [ ] **Anomalies escalated, not fixed silently.** Jamming/spoofing, sensor errors, timing jumps logged with times; decision recorded. — Ch. 56.19

## G.3 Processing (from raw data to a gridded product)

Reference: [Chapter 29](../chapters/ch29-processing-pipelines.md), [Chapter 30](../chapters/ch30-point-cloud-classification.md), [Chapter 31](../chapters/ch31-interpolation-and-gridding.md).

- [ ] **Software versions, parameters, and grids pinned (must).** GDAL/PROJ/PDAL versions, geoid grid file names and versions, filter parameters, random seeds; container or lockfile archived. — Ch. 29.4, 50
- [ ] **Trajectory QC passed.** Forward/reverse separation, ambiguity-fixed fraction, estimated position/attitude σ within budget; segments failing QC flagged in the deliverable, not just discarded. — Ch. 12, 13
- [ ] **Boresight/strip adjustment done and reported.** Residual strip-to-strip height differences (mean and σ) on overlaps before and after; remaining systematic patterns examined (roll ramps, pitch offsets, range scale). — Ch. 18, 25
- [ ] **Datum transformation applied once and documented.** Ellipsoid → orthometric with a named geoid; horizontal frame and epoch transformations; no double application, no mixed geoids within a project. — Ch. 9, 10
- [ ] **Noise and outlier removal with logged thresholds.** Low/high noise classified, not deleted; birds, water-column returns, multipath, "smile/frown" MBES artefacts checked. — Ch. 30.1, 56.18
- [ ] **Ground classification validated against manual samples.** Type I/II error rates by land cover; parameters tuned per terrain class; vegetation/buildings/bridges per inclusion rules. — Ch. 30.3–30.5, 32
- [ ] **Breaklines and hydro features captured per spec.** Water-body flattening (monotonic rivers), coastline at defined stage, culverts/bridges per rule. — Ch. 34, 59
- [ ] **Gridding method and cell convention chosen deliberately.** Method (TIN linear, IDW, kriging, binning), cell size relative to point spacing (≥ 1–2× NPS), pixel-is-point vs pixel-is-area recorded in the file, NoData value declared. — Ch. 31
- [ ] **Voids identified and handled per spec.** Interpolated vs filled vs left as NoData; void mask delivered; maximum interpolation distance stated. — Ch. 35
- [ ] **Overviews and tiles generated without smearing.** Averaging vs nearest for overviews; tile seams checked. — Ch. 31.7, 47
- [ ] **Uncertainty layer produced.** Per-cell σ from TPU/propagation or at minimum per-stratum constants; method documented. — Ch. 46.9, 53.4
- [ ] **Lineage recorded end to end.** What each step removed or changed; intermediate products retained where re-processing is likely. — Ch. 29.3, 50.5
- [ ] **Regression test on a reference tile.** Re-run the pipeline on a known tile; differences vs. last release explained. — Ch. 29.6

## G.4 DSM → DTM and classification QA

Reference: [Chapter 32](../chapters/ch32-dsm-to-dtm.md), [Chapter 30](../chapters/ch30-point-cloud-classification.md), [Chapter 33](../chapters/ch33-wires-and-thin-structures.md), [Chapter 63](../chapters/ch63-buildings-cities-innerspace.md).

- [ ] **Definition of "ground" written and attached (must).** Bridges (in or out), culverts, retaining walls, piers, stockpiles, solar panels, greenhouses, dense low vegetation, snow. — Ch. 32.1, 32.2
- [ ] **Multi-azimuth hillshade sweep** of the DTM at ≥ 4 azimuths and low sun angle; look for building stubs, tree "pimples", terrace steps, strip edges, flattened hilltops (over-filtering). — Ch. 54.2, 57.2
- [ ] **nDSM = DSM − DTM inspected.** Negative values (DTM above DSM) are errors; large positive on open ground means missed objects. — Ch. 32.8
- [ ] **Ridge and cut-bank preservation.** Compare slope histograms of DTM vs raw ground points; over-aggressive filters shave crests and terraces. — Ch. 30.4
- [ ] **Steep-slope check.** Classification error climbs with slope; sample manually on slopes > 30°. — Ch. 30.4
- [ ] **Buildings removed cleanly.** No footprint "craters" or "plateaus"; ground interpolated under buildings per spec (declared as interpolated). — Ch. 32.4, 63.3
- [ ] **Bridges and overpasses per rule;** multi-valued surfaces flagged rather than averaged. — Ch. 32.3, 63.4
- [ ] **Vegetation residuals by stratum.** VVA checkpoints under canopy; check seasonal state matches spec. — Ch. 32.6, 36.1, 53
- [ ] **Wires, towers, cranes** not left in DTM and, if required, present in DSM as a separate class. — Ch. 33
- [ ] **Water bodies.** Flattened at a plausible, monotonic level; no "waterfalls" at tile boundaries; shoreline consistent with stage/date. — Ch. 34
- [ ] **Classification confusion matrix** from an independent manual sample (per class precision/recall; ground Type I/II). — Ch. 30.5, 42.7
- [ ] **Edit log retained.** Who edited what, when, with which tool; manual edits are data. — Ch. 30.7

## G.5 Accuracy assessment and reporting

Reference: [Chapter 53](../chapters/ch53-accuracy-assessment.md), [Chapter 5](../chapters/ch05-error-and-uncertainty.md), [Chapter 52](../chapters/ch52-ground-truth.md).

- [ ] **Checkpoints independent of production (must).** Not used in adjustment, calibration, or training; different observation method where possible. — Ch. 52.2
- [ ] **Checkpoint accuracy ≥ 3× better than the product requirement,** documented with its own σ. — Ch. 52.1
- [ ] **Stratification.** Separate statistics for open/hard, vegetated classes, urban, slope classes; sample sizes stated. — Ch. 53.3
- [ ] **Co-registration tested before computing statistics.** Horizontal shift estimated (e.g. Nuth–Kääb on slopes); if shift > 1/4 pixel, report both raw and co-registered results and explain. — Ch. 41.1, 53
- [ ] **Statistics computed with the right formulas:** mean error (bias), σ, RMSE, MAE, median, NMAD, LE95 (empirical 95th percentile of |error| for non-normal; 1.96 × RMSE only when normality is shown). Report *n*. — Ch. 5, 53.1
- [ ] **Normality and outliers examined.** Histogram, Q–Q plot; outliers reported, not silently removed; thresholds documented if removed. — Ch. 5
- [ ] **Spatial structure of error.** Error map or variogram; strip/tile pattern test; correlation length reported for volume/area users. — Ch. 53.5
- [ ] **Horizontal accuracy assessed** where features permit (building corners, targets, lidar intensity targets). — Ch. 53.7
- [ ] **Comparison against the specification's test logic** (ASPRS NVA/VVA; S-44 TVU/THU per sounding; INSPIRE; national) with pass/fail stated explicitly. — Ch. 53.2, 70
- [ ] **Independent cross-check against another source** (ICESat-2 ATL06/08, prior lidar on stable ground, national benchmarks) and its agreement reported. — Ch. 52.4, 54.4
- [ ] **Uncertainty budget table** listing components (positioning, attitude, range, geoid, interpolation, temporal) with magnitudes and how combined. — Ch. 53.4
- [ ] **Report contains:** method, checkpoint table (coordinates may be withheld; residuals must not), statistics by stratum, maps of checkpoints and residuals, limitations paragraph, software versions, date of assessment, name of assessor. — Ch. 53.6
- [ ] **Decision-relevant statement.** What the numbers mean for the intended use (e.g. inundation extent uncertainty at the design stage). — Ch. 53.8, 61.5

## G.6 Metadata and delivery

Reference: [Chapter 49](../chapters/ch49-metadata.md), [Chapter 47](../chapters/ch47-file-formats.md), [Chapter 50](../chapters/ch50-archiving-and-provenance.md).

- [ ] **Identifier and version** (DOI or persistent URI; semantic version; supersession statement). — Ch. 49, 50.4
- [ ] **CRS complete (must):** horizontal datum + frame realization + epoch; vertical datum + geoid model/version; EPSG codes (compound CRS) *and* WKT2 embedded in files; units. — Ch. 8, 9, 49
- [ ] **Surface type and inclusion/exclusion rules** stated in plain language. — Ch. 4, 32
- [ ] **Acquisition dates** (start/end; per-tile or per-cell date raster for composites); time of day where tide/traffic matter. — Ch. 37.6, 48.7
- [ ] **Sensor, platform, method,** nominal density, flying height/speed, swath overlap, sound-speed cadence. — Ch. 49
- [ ] **Processing lineage** with software versions, parameters, geoid grid names; link to processing report. — Ch. 29, 50.5
- [ ] **Resolution**: nominal post, source density, estimated effective resolution. — Ch. 44.8
- [ ] **Accuracy**: statistic, standard, per-stratum values, *n*, date of test, link to full assessment. — Ch. 53.6
- [ ] **Voids, fills, masks, water treatment** documented with raster layers. — Ch. 35, 34
- [ ] **Uncertainty layer definition** (what the values mean: 1σ? 95 %? vertical only?). — Ch. 46.9
- [ ] **File-format checks passed**: COG validator; LAS header (version, point format, CRS VLR/WKT, point count); BAG/S-102 validator; NoData set; pixel-is-point/area flag; overviews present; checksums. — Ch. 47.8
- [ ] **Tiling/index** documented (naming scheme, tile size, overlap); index shapefile/GeoJSON delivered. — Ch. 47, 51
- [ ] **Licence** (SPDX identifier where possible), attribution text, and any NC/SA/ND clauses; third-party data licences inherited. — Ch. 68.3
- [ ] **Contact, limitations paragraph, and "not for navigation"/"not for design" statements** where applicable. — Ch. 49, 62.7
- [ ] **Archive package**: raw data, intermediate products as agreed, metadata, checklists, reports, in a trusted repository with retention schedule. — Ch. 50

## G.7 Evaluating someone else's DEM

Reference: [Chapter 54](../chapters/ch54-evaluating-others-data.md), [Chapter 55](../chapters/ch55-public-products.md), [Appendix E](appendix-e-public-products-tables.md).

- [ ] **Read the file before the website.** `gdalinfo`/`pdal info`: CRS (horizontal, vertical, geoid?), units, pixel convention, NoData, data type and scale (integers? 0.1 m quantization?), overviews, creation software. — Ch. 54.1, 47
- [ ] **Confirm what surface it is** (DSM/DTM/hybrid; radar vs optical vs lidar) and what was removed or filled. — Ch. 4, 32.7
- [ ] **Confirm the epoch(s).** Acquisition dates; for composites, is a date layer available? Does the epoch suit the use (post-earthquake? post-construction?). — Ch. 37, 39
- [ ] **Vertical datum sanity test.** Compare a few cells with known heights (benchmarks, tide gauge zero, airport elevation) — an offset near a local geoid undulation value means a geoid/ellipsoid mix-up. — Ch. 9, 56.13
- [ ] **Visual artefact sweep** (hillshade at ≥ 4 azimuths plus a slope map): striping, tile seams, terraces, pits/spikes, "mole runs", smoothed ridges, flattened water with steps. — Ch. 54.2
- [ ] **Flat-surface noise test.** σ of heights over a known flat area (lake, runway, parking lot); compare with claimed accuracy. — Ch. 54.3
- [ ] **Seam/strip test.** Height differences across tile and strip boundaries; periodicity in a Fourier/autocorrelation plot. — Ch. 54.3
- [ ] **Void and fill map** retrieved or derived; are fills from a coarser/older product? — Ch. 35
- [ ] **Independent check** against ICESat-2 (ATL06/ATL08 terrain), national benchmarks, or a better DEM over stable terrain, after co-registration; stratify by land cover/slope. — Ch. 52.4, 53
- [ ] **Compare with a second product** of different lineage (e.g. Copernicus vs AW3D30, not FABDEM vs Copernicus) to localize gross errors. — Ch. 55.6, App. E.3
- [ ] **Texture-based provenance inference.** Does the noise texture match the claimed sensor (radar speckle, photogrammetric matching blobs, lidar strip edges)? — Ch. 54.5
- [ ] **Claims vs evidence.** Does the accuracy claim cite an independent test with *n* and strata? Does it apply to this terrain? — Ch. 54.6
- [ ] **Licence permits your use and your derivative** (NC/SA/ND; redistribution; ML training). — Ch. 68.3
- [ ] **Write the fitness-for-use memo:** source, tests performed, numbers found, decision (use / use with caveats / reject), and what would change the decision. — Ch. 54.8

## G.8 Compositing and merging products

Reference: [Chapter 48](../chapters/ch48-compositing.md), [Chapter 34](../chapters/ch34-water-in-dems.md) §34.8, [Chapter 41](../chapters/ch41-change-detection.md) §41.1.

- [ ] **Inventory every input** with CRS (H+V+geoid+epoch), surface type, resolution, date, accuracy, licence, sign convention (depth vs elevation). — Ch. 48.2
- [ ] **Harmonize datums first (must)**, with named transformation grids; record the uncertainty of each transformation (separation models can be 10–30 cm uncertain at the coast). — Ch. 9, 48.2
- [ ] **Harmonize surface types**; do not blend a DSM into a DTM without declaring the result a hybrid and mapping where each applies. — Ch. 4, 48.2
- [ ] **Harmonize sign and units** (positive-up elevation; metres; same foot definition if feet were ever involved). — Ch. 56.6
- [ ] **Co-register and bias-correct on overlaps** (Nuth–Kääb/ICP); report the shifts applied per input. — Ch. 41.1, 48.2
- [ ] **Priority rule declared and justified by use** (newest? most accurate? highest resolution? shoalest for navigation?). — Ch. 48.3, 62
- [ ] **Blending/feathering policy stated** with widths; seams documented in a seam-line vector layer. — Ch. 48.4
- [ ] **Cropping and masks** for invalid zones (clouds, water, snow, ships) applied before blending. — Ch. 48.5, 27
- [ ] **Land–water seam handled explicitly**: the "white ribbon" treatment, intertidal datum, shoreline date; no step at the waterline. — Ch. 34.8, 48.6
- [ ] **Companion rasters produced (must):** source ID, acquisition date, uncertainty, method/flag; plus a lineage table keyed to source ID. — Ch. 48.7
- [ ] **Seam QC**: profiles across every seam type; hillshade sweep; hydro-connectivity test (flow routing does not pond at seams). — Ch. 48.8, 61.3
- [ ] **Resolution honesty**: output post no finer than the best input where it dominates; effective resolution map if inputs differ widely. — Ch. 44, 48
- [ ] **Licence compatibility** of the composite (most restrictive input governs; NC/SA propagate). — Ch. 68.3
- [ ] **Versioning and supersession**: changelog per release; tiles that changed; how users are notified. — Ch. 48.9, 50.4

## G.9 Post-disaster rapid mapping

Reference: [Chapter 39](../chapters/ch39-earthquakes-volcanoes-landslides.md) §39.8, [Chapter 41](../chapters/ch41-change-detection.md), [Chapter 62](../chapters/ch62-navigation-and-charting.md), [Chapter 69](../chapters/ch69-security-sovereignty-privacy-ethics.md).

- [ ] **Decide what question the first product answers** (where did the ground move; where is debris; is the channel open; which roads are passable) and label it as such; do not promise a general DEM. — Ch. 3, 39.8
- [ ] **Freeze and label the pre-event reference**: dataset, version, epoch, datum; archive a copy. — Ch. 41, 50
- [ ] **Datum consequences evaluated (must).** After large earthquakes, coordinates of control points, CORS, and the pre-event DEM have moved (metres horizontally, decimetres to metres vertically); decide whether to work in a post-event local frame or apply a coseismic deformation model. State which. — Ch. 38, 39, 56.4, 56.5
- [ ] **GNSS infrastructure checked.** Which CORS/benchmarks survived and moved; use independent sources (PPP in ITRF) rather than local RTK networks until re-adjusted. — Ch. 12, 25, 56.3
- [ ] **Acquisition priorities by risk**, not by convenience: dams, levees, landslide dams, lifelines, ports/channels, hospitals. — Ch. 39.8, 65.7
- [ ] **Sensor choice by conditions**: SAR for cloud/night and displacement; optical/photogrammetry for rapid DSMs; lidar where available; MBES/SBES for channels; crowd/UAS imagery with care. — Ch. 16–22
- [ ] **Quick co-registration on stable terrain** before any differencing; report residual σ and the LoD used. — Ch. 41.1, 41.8
- [ ] **Confounds screened**: season, water level, debris, vegetation loss, tents and vehicles, and processing differences between pre and post. — Ch. 41.9, 27
- [ ] **Provisional labelling (must).** Every product stamped "PROVISIONAL — rapid assessment, not for design/navigation", with date, version, and known limitations; superseded versions withdrawn but archived. — Ch. 39.8, 62.7
- [ ] **Uncertainty communicated simply**: LoD map or confidence classes, not raw differences; vertical exaggeration and colour scale chosen to avoid false alarm. — Ch. 53.8, 57.9
- [ ] **Navigation products**: notices to mariners/airmen issued; chart or obstacle data flagged; shoalest-point rule maintained; no silent updates. — Ch. 62
- [ ] **Privacy, dignity, and security**: imagery over casualties and homes handled per policy; sensitive sites redacted; sharing agreements with authorities and humanitarian clusters. — Ch. 69
- [ ] **Hand-off plan**: who converts provisional products into validated ones, when, and how users are notified; raw data archived with time stamps for later science and litigation. — Ch. 50, 68.6
- [ ] **After-action review** recorded: what worked, what failed, checklist updated. — Ch. 56

<!-- figure: Figure G.1 — Flow diagram linking the nine checklists along a project life cycle (plan → acquire → process → classify → assess → deliver), with G.7 and G.8 as entry points for data consumers and G.9 as an emergency branch. -->

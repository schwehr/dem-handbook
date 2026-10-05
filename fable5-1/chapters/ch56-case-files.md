# Chapter 56 — Case files: failures, surprises, and lessons

> **Part XI — Validation, quality, and judging data.** This chapter closes the validation part of the book with evidence: twenty-three documented incidents in which elevation, depth, or positioning data went wrong — or, in a few cases, were caught in time — each traced to the chapters that explain the mechanism.

**In this chapter.** Standards and statistics are abstractions until a submarine hits a seamount the chart did not show, a levee is built half a metre low because the benchmark had sunk, or a flood map triples a country's exposure because someone finally subtracted the trees. Each file here is short and sourced: what happened, the root cause in this book's vocabulary (datum, epoch, surface definition, uncertainty, metadata, human assumption), the check that would have caught it, and the chapters that apply. The cases span naval groundings, earthquakes that moved national datums, unit confusions on Mars and in state plane coordinates, a fitness app that mapped military bases, borders that migrate with glaciers, landslides and dam failures whose precursors were in the data, the cost of mapping the unknown seafloor, machine-learning artefacts in published analyses, bridges that dam flood models, sonar errors that reached charts, GNSS jamming, nineteenth-century refraction, and one independent QC process that worked. Read them as a practitioner reads accident reports: not to assign blame, but to recognize the system conditions that let a known failure mode through and to design the check that closes it.

## 56.1 USS *San Francisco* (2005): the seamount that was not on the chart ⟨H⟩

**What happened.** On 8 January 2005 the nuclear attack submarine USS *San Francisco* (SSN-711), at flank speed and 525 ft (160 m) depth about 360 nmi southeast of Guam, struck a seamount. One sailor, Machinist's Mate Second Class Joseph Ashley, died and 98 of 137 crew were injured; the bow was crushed but the pressure hull held (US Navy 2005). The chart in use — a Defense Mapping Agency chart with source data from 1989 and earlier — showed thousands of metres of water along the track.

**Root cause.** The seamount existed in the data system but not on the chart in use. The command investigation found that other charts in the boat's inventory depicted a hazard near the track and that a "discoloured water" notation lay within about 2.5–2.8 nmi of the grounding position; 1999 Landsat imagery shows a colour anomaly consistent with the feature. The deep-ocean chart was compiled from sparse soundings and satellite-gravity prediction — in the vocabulary of [Chapter 55](ch55-public-products.md), nearly every cell near the track would carry a GEBCO TID of "predicted" — and the chart gave the navigator no way to see that. Voyage planning did not cross-check all available charts as required.

**What would have caught it.** A source-confidence overlay — what ENCs encode as CATZOC and what S-101/S-102 carry as quality-of-bathymetric-data attributes ([Chapter 62](ch62-navigation-and-charting.md), [Chapter 70](ch70-specifications-guided-tour.md)) — would have shown the route crossing unsurveyed water; the required cross-check of every chart in the inventory would have transferred the hazard; modern practice adds a speed–depth policy keyed to survey confidence ([Chapter 20](ch20-sonar.md)).

## 56.2 *Queen Elizabeth 2* (1992): squat, tide, and the number on the chart

**What happened.** On 7 August 1992 the liner *Queen Elizabeth 2*, outbound through Vineyard Sound at 24–25 kn, struck uncharted rocks and opened her hull over tens of metres; no one was hurt but repairs cost tens of millions of dollars (NTSB 1993). The chart showed about 39 ft (11.9 m) at mean low water; static draft was about 32 ft (9.8 m).

**Root cause.** Three vertical quantities were misjudged together. The bridge estimated **squat** — dynamic sinkage of a fast hull in shallow water — at 1–1.5 ft; the NTSB put bow sinkage at not less than 2.7 ft. The master assumed about 2 ft of tide against about 0.5 ft actual. And the rocks struck lay at about 34–35 ft, shallower than the charted depth — a sounding-density problem in a rocky area last surveyed with widely spaced lines. Each error alone was within what a cautious navigator might accept; summed, they consumed a nominal clearance of about 7 ft. The datum (MLW) and tide reduction were correct; the chart depth was a sample on a surface whose minima had not been sampled, and the vessel's instantaneous draft was not.

**What would have caught it.** An under-keel clearance budget treating each term as a quantity with uncertainty — charted depth minus a sounding-density allowance, tide minus its prediction error, static draft, speed-dependent squat — would have shown negative clearance at planned speed (worked example below; [Chapter 9](ch09-vertical-datums.md), [Chapter 62](ch62-navigation-and-charting.md)). NOAA's full-coverage multibeam resurvey found the rocks; S-44's "full seafloor search" exists for this reason ([Chapter 70](ch70-specifications-guided-tour.md)).

## 56.3 Hurricane Katrina (2005): benchmarks that sank with the city

**What happened.** When Katrina's surge reached New Orleans on 29 August 2005, floodwalls and levees were overtopped and breached, flooding about 80 % of the city and killing more than a thousand people. Investigations (IPET 2007; Seed et al. 2006) found several levee reaches 0.3–0.6 m (1–2 ft) below design crest height — not built wrong, but built to a vertical reference that had moved.

**Root cause.** Design heights were specified relative to older benchmarks and datum realizations (NGVD 29 and early NAVD 88 adjustments) whose published heights were decades out of date in a region subsiding at 1–2 cm/yr and locally more (Dixon et al. 2006). When NGS re-levelled and re-adjusted (NAVD 88 epoch 2004.65), many benchmarks had sunk by tens of centimetres relative to their published values; some projects had also mixed NGVD 29 and NAVD 88 or assumed an unstated "mean sea level." The structure was built to the datasheet, and the datasheet was a historical record.

**What would have caught it.** Treating vertical control as time-dependent: re-observing benchmarks with GNSS before design, using CORS and a geoid model to detect subsidence ([Chapter 38](ch38-plate-motion-and-vlm.md)), and specifying heights in a named realization with an epoch. The Corps' adoption of time-tagged NAVD 88 (2004.65) heights with periodic re-levelling, and NGS's move to a GNSS-based vertical datum (NAPGD2022; adoption still pending, beta products expected in 2026) are the institutional fixes ([Chapter 9](ch09-vertical-datums.md), [Chapter 61](ch61-hydrology.md)).

## 56.4 Tōhoku (2011): when the country moved more than five metres

**What happened.** The M9.0 Tōhoku-oki earthquake of 11 March 2011 displaced the Oshika Peninsula about 5.3 m east-southeast and lowered it about 1.2 m; GEONET stations across northeastern Honshu moved by metres horizontally and subsided by decimetres (GSI 2011). Harbours, coastal DEMs, flood maps, and property boundaries were suddenly in the wrong place relative to the national datum.

**Root cause.** Nothing failed; the Earth moved and the coordinates did not. JGD2000 was a static frame, so every control point in the region carried a coordinate that no longer described its position, and co-seismic subsidence shifted tidal datums, chart datums, and land heights relative to one another. Inundation mapping and harbour re-surveys had to proceed against a reference being redefined.

**What would have caught it.** Preparedness rather than catching: GSI suspended survey results, published revised coordinates (JGD2011 with a semi-dynamic correction) and new heights within months, and the Japan Coast Guard re-surveyed ports with multibeam before reopening them. For DEM users ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md), [Chapter 6](ch06-time-as-coordinate.md)): record the epoch of every coordinate; expect any DEM in a seismically active region to become obsolete overnight; and treat a post-event DEM difference as deformation plus datum change plus surface change until separated.

## 56.5 Kaikōura (2016): the coast rose and the charts were withdrawn

**What happened.** The M7.8 Kaikōura earthquake of 14 November 2016 ruptured more than twenty faults in the northeastern South Island. Coastal uplift ranged from decimetres to about 6 m, locally about 8 m across the Papatea fault, lifting rocky seabed, kelp beds, and Kaikōura harbour out of the water (Hamling et al. 2017; Clark et al. 2017); horizontal displacements of several metres were measured by GNSS and InSAR.

**Root cause.** As at Tōhoku, the ground left the datum — but Kaikōura shows the full cascade for elevation products. Charted harbour depths were suddenly 1–2 m too deep in places, so Land Information New Zealand withdrew or amended charts pending resurvey; pre- and post-event lidar showed the uplift directly; and NZGD2000, a semi-dynamic datum with a published deformation model, received a **patch** — a localized displacement model (deformation model version 20171201, refined in 20180701) — so that pre- and post-event coordinates could be related without renaming the datum.

**What would have caught it.** Readiness: pre-event lidar and GNSS baselines existed, so change was quantified within days; the datum had a mechanism for absorbing co-seismic steps; and the hydrographic office treated the charts as falsified until re-observed. Users near any active fault should ask whether their datum has such a mechanism and whether their DEM's epoch precedes the last large event ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md), [Chapter 8](ch08-horizontal-datums.md), [Chapter 62](ch62-navigation-and-charting.md)).

## 56.6 Mars Climate Orbiter (1999) and the US survey foot: units

**What happened.** On 23 September 1999 NASA's Mars Climate Orbiter entered the Martian atmosphere at about 57 km instead of the planned 150–226 km and was lost. The Mishap Investigation Board found that a ground-software file supplied thruster impulse in pound-force seconds where the navigation software expected newton-seconds — a factor of 4.45 — so small trajectory corrections were under-modelled for months (Stephenson et al. 1999). A growing inconsistency between navigation solutions was noticed but not resolved.

**Root cause.** The interface specification said SI; one supplier delivered imperial; no automated check compared units; and the process discounted residuals that were telling the truth. Elevation work has the same failure at every scale. The **US survey foot** (1200/3937 m) and the **international foot** (0.3048 m) differ by 2 ppm — negligible for a height, but 2 ppm of a 2,000,000 ft state plane coordinate is about 4 ft (1.2 m), enough to misregister a DEM. NIST and NOAA deprecated the US survey foot effective 31 December 2022 (NIST/NOAA 2019), but legacy files, CRS definitions, and software defaults still carry both, and feet-versus-metres confusion in vertical units remains common in lidar deliveries — usually revealed by sea-level cells that read 3.28 instead of 1.00.

**What would have caught it.** Units carried in the data model and checked by software (CRS linear units; LAS scale factors; GeoTIFF vertical-unit keys — [Chapter 47](ch47-file-formats.md)); the "values over the sea near 0?" triage of [Chapter 54](ch54-evaluating-others-data.md); and attention to residuals that will not go away ([Chapter 4](ch04-names-and-definitions.md), [Chapter 10](ch10-projections-and-resampling.md)).

## 56.7 Grand Banks (1929): the cables that timed a turbidity current ⟨H⟩

**What happened.** On 18 November 1929 an M7.2 earthquake on the continental slope south of Newfoundland triggered a submarine slump and a turbidity current that broke twelve transatlantic telegraph cables in sequence over about thirteen hours, the farthest some 600 km from the epicentre; the tsunami killed 28 people on the Burin Peninsula. Heezen and Ewing (1952) used the recorded break times and cable positions to infer the current's speed — roughly 60–100 km/h on the upper slope, slowing with distance — and so established turbidity currents as a real seafloor process.

**Root cause.** Infrastructure designed on the assumption of a static seafloor. The lesson is twofold: seafloor topography changes by events — post-event bathymetry differed from pre-event by tens of metres in channels (Piper et al. 1988), so every seafloor DEM has an epoch that matters on slopes with sediment supply — and the event was reconstructed from time stamps in cable-company logs, the earliest example in this book of time as a coordinate making a geomorphic measurement possible ([Chapter 6](ch06-time-as-coordinate.md)).

**What would have caught it.** Nothing in 1929; today, slope-stability mapping from multibeam and sub-bottom profiling, repeat bathymetry of canyon systems, and geohazard-informed cable routing are standard ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md), [Chapter 40](ch40-erosion-and-geomorphic-change.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).

## 56.8 Strava heatmap (2018): derived data that revealed what the DEM did not

**What happened.** In November 2017 Strava published a global heatmap of about a billion activities. In January 2018 an Australian student, Nathan Ruser, showed that it traced running routes and perimeter patrols at military bases in Syria, Afghanistan, Niger, and elsewhere, including sites whose existence was not public (Hern 2018), at a resolution commercial imagery of those places was not permitted to show.

**Root cause.** Aggregation was assumed to anonymize. Individual traces were opt-out-able but public by default, and the aggregate carried information none of its constituents was thought to carry. DEMs behave the same way: a 1 m DTM reveals a facility's layout through earthworks and berms even where the DSM has been sanitized; a canopy-height model reveals clearings; a DEM time series reveals construction. Governments that restrict imagery resolution rarely restrict lidar-derived products ([Chapter 69](ch69-security-sovereignty-privacy-ethics.md)).

**What would have caught it.** A disclosure-risk review of the aggregate product rather than of individual records, a default of private, and the question "what does this reveal when combined with other public data?" — the review public lidar programmes now perform, inconsistently, before releasing data over sensitive sites ([Chapter 68](ch68-legal-issues.md)).

## 56.9 Borders that move: the Matterhorn ridge and the melting watershed

**What happened.** The Italy–Switzerland border across the Alps follows, by treaty, the watershed. On the Theodul Glacier below the Matterhorn the crest is ice, and as the glacier has thinned by tens of metres since the boundary was surveyed in the 1920s–1940s the divide has migrated by tens of metres or more. In 2008–2009 the two countries agreed to treat glaciated sections as a **mobile border** following the measured divide, and Italy concluded a similar agreement with Austria (Italian Law 72/2009 (verify)). By 2023–2024 the retreat had moved the line enough that the Rifugio Guide del Cervino at Testa Grigia straddled it; a redrawing was approved by Switzerland's Federal Council in 2024 pending Italian ratification. Ski-lift stations, a customs post, and which rescue service responds all depend on where the surveyed crest is this year.

**Root cause.** The boundary references a geomorphic feature that is itself an elevation product with an epoch. A watershed computed from a DEM moves whenever the DEM is updated — on bedrock by measurement noise, on ice by real change. The treaty assumed a stable surface.

**What would have caught it.** The drafters could not foresee twentieth-century retreat, but the lesson generalizes: any boundary or jurisdiction defined on terrain (watersheds, ridgelines, mean high water, thalwegs, "top of bank") inherits the epoch and uncertainty of the DEM used to locate it ([Chapter 68](ch68-legal-issues.md)). Record the DEM source and date in the boundary survey and compare the minimum detectable change ([Chapter 41](ch41-change-detection.md)) with the expected rate of change ([Chapter 40](ch40-erosion-and-geomorphic-change.md), [Chapter 37](ch37-time-scales-of-change.md)).

## 56.10 Oso (2014): the lidar showed the history; who reads the DEM?

**What happened.** On 22 March 2014, after weeks of heavy rain, a hillslope above the North Fork Stillaguamish River near Oso, Washington, failed catastrophically, mobilizing about 8 million m³ of glacial sediment, crossing the river and valley floor, burying the Steelhead Haven neighbourhood, and killing 43 people (Iverson et al. 2015; Keaton et al. 2014). The slope had a documented history of failures in 1949, 1951, 1967, and 2006.

**Root cause.** The hazard was legible in the data and illegible in the decision process. Public lidar flown in 2003 and 2013 showed hummocky deposits of prehistoric and historical landslides across the valley floor — some reaching farther than the 2014 runout — and USGS geologist Ralph Haugerud published an interpretation within weeks (Haugerud 2014) using nothing but a bare-earth hillshade that had been available for a decade. A 1999 consultant's report had warned of catastrophic-failure potential. Zoning, home-buying, and river-restoration decisions were made by people who did not look at the DTM or could not read a hummocky surface as an old landslide.

**What would have caught it.** Lidar landslide inventories as routine input to land-use planning — which Washington State subsequently funded — and treating a bare-earth hillshade as a public document decision-makers are expected to read. Multi-directional hillshade and slope maps make old landslides obvious; a single-azimuth hillshade or a contour map may not ([Chapter 57](ch57-visualizing-dems.md), [Chapter 39](ch39-earthquakes-volcanoes-landslides.md), [Chapter 1](ch01-uses-on-land.md)). On the morphologic evidence the 2014 slide was not a surprise; it was a repeat.

## 56.11 Brumadinho (2019): InSAR signals before the dam failed

**What happened.** On 25 January 2019 the Córrego do Feijão Dam I, an upstream-raised iron-ore tailings dam near Brumadinho, Brazil, liquefied and collapsed with no warning its monitoring recognized, releasing about 10 million m³ of tailings and killing 270 people. The dam, inactive since 2016, was monitored with piezometers, inclinometers, ground-based radar, and — from 2018 — satellite InSAR.

**Root cause.** The expert panel (Robertson et al. 2019) attributed the failure to static liquefaction of loose, saturated tailings under internal creep and seasonal rainfall, with no significant deformation detectable by conventional instruments in the days before. Retrospective InSAR studies disagree on what was detectable: Gama et al. (2020) with Sentinel-1 SBAS/PSI and Grebby et al. (2021) with ISBAS report accelerating millimetre-per-month deformation on parts of the dam in the preceding months; the panel's review found settlement rates up to about 30 mm/yr it considered normal; others argue the signals were within noise or ambiguous without hindsight (Holden et al. 2020 (verify)). The case separates **detection** — is there a signal above the minimum detectable change ([Chapter 41](ch41-change-detection.md))? — from **decision** — who must act on a signal of what size, at what false-alarm rate?

**What would have caught it.** Possibly nothing with confidence; that is the honest answer. But the case made explicit what a monitoring design must specify: the deformation rate that constitutes an alarm, each instrument's detection threshold including InSAR's line-of-sight geometry and atmospheric noise, and the decision authority. The Global Industry Standard on Tailings Management (ICMM/UNEP/PRI 2020) now requires it ([Chapter 65](ch65-mining-landfills-earthworks.md), [Chapter 21](ch21-radar-sar-insar.md)).

## 56.12 MH370: the cost of mapping the unknown

**What happened.** Malaysia Airlines Flight 370 disappeared on 8 March 2014. Satellite-communication analysis placed its end point along an arc in the southern Indian Ocean in 1,500–6,000 m of water. Before any sonar search for wreckage could run, the seafloor had to be mapped: existing bathymetry there was almost entirely altimetry prediction at kilometre-scale resolution, inadequate for planning towed-sonar and AUV operations near seamounts, scarps, and canyons. Phase 1 surveyed about 279,000 km² with shipboard multibeam in 2014–2016 (Picard et al. 2018; Picard, Brooke & Coffin 2017); the underwater search then covered 120,000 km² and found nothing. The released data revealed volcanoes, fault scarps, landslides, and canyons invisible in the altimetry model and improved local resolution by at least a factor of fifteen.

**Root cause.** The ocean floor was, and mostly still is, unmapped: roughly 6 % measured at modern resolution in 2014, 27.3 % by mid-2025 ([Chapter 55](ch55-public-products.md)). The search had to pay for mapping as a precondition, and the mapping took longer than the search. Every deep-water use of a global grid inherits this: the cells are predictions with 100–200 m vertical error and kilometres of horizontal error in feature position.

**What would have caught it.** A cost to recognize rather than a failure to catch. The case became an argument for the Nippon Foundation–GEBCO Seabed 2030 project (2017), for routine data release from transits, and for crowdsourced bathymetry under IHO B-12 ([Chapter 2](ch02-uses-bathymetry.md), [Chapter 23](ch23-satellite-derived-bathymetry.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).

## 56.13 Flood maps and the subtracted trees: SRTM, geoids, and CoastalDEM

**What happened.** Two classes of error have shaped global coastal-flood analyses. The first is a datum error: SRTM (EGM96 orthometric) or TanDEM-X (WGS 84 ellipsoidal) heights are loaded into a model that assumes "0 = sea level" without conversion to a tidal datum or even the right geoid, producing a smooth bias of tens of metres (ellipsoid) or decimetres to metres (geoid difference, sea-surface topography) that shifts the mapped inundation line by hundreds of metres on flat coasts. The second is a surface-definition error quantified by Kulp and Strauss (2019): SRTM is a DSM whose canopy and building bias in populated coastal lowlands averages about 2 m in the United States and more in dense Asian cities. Replacing SRTM with CoastalDEM — SRTM corrected by a neural network trained on US lidar — raised the estimated global population below projected 2100 high-tide lines from about 80 million to about 190 million (110 to 340 million under high emissions). The "triples estimates" headline was accurate; the uncertainty around the new numbers was itself large, as the authors stated.

**Root cause.** The DSM-as-DTM confusion of [Chapter 4](ch04-names-and-definitions.md), compounded by geoid-versus-tidal-datum mismatches ([Chapter 9](ch09-vertical-datums.md)), in the one place where a 2 m error has the largest horizontal and human consequences. The ML correction reduced bias but added its own uncertainty structure — trained on US lidar, applied to deltas in Bangladesh and Vietnam ([Chapter 43](ch43-traditional-vs-ml.md)).

**What would have caught it.** The sea-level and flat-surface tests of [Chapter 54](ch54-evaluating-others-data.md) (do cells over the sea read near zero? does a tide gauge's land elevation match?) catch the datum errors; land-cover-stratified comparison against ICESat-2 reveals the canopy bias; and exposure reported as a range with the DEM's uncertainty propagated ([Chapter 61](ch61-hydrology.md)) is the honest form. Purpose-built products — DeltaDTM, national lidar — now exist ([Chapter 55](ch55-public-products.md)).

## 56.14 The FABDEM terraces: machine-learning artefacts in published analyses

**What happened.** FABDEM (Hawker et al. 2022) removed forests and buildings from Copernicus GLO-30 with random forests and within a year became the default terrain for global flood modelling. Users then noticed **terraces** in slope and hillshade maps over flat forested terrain — steps of 1–2 m along land-cover class boundaries where the correction changes discontinuously — plus "trenches" where canopy correction was applied to bare cliffs and rounded mounds where large buildings survived. Similar artefacts occur in CoastalDEM and in super-resolved DEMs ([Chapter 45](ch45-super-resolution.md)) and have propagated into published hazard analyses whose drainage networks route around steps that do not exist. DEMIX (Bielski et al. 2024) and Guth & Geoffroy (2021) documented that FABDEM's slope and roughness statistics depart from reference lidar more than its elevations do; version 1-2 (2023) reduced the worst cases.

**Root cause.** A per-pixel correction predicted from categorical covariates inherits the covariates' boundaries; a model trained where lidar exists extrapolates to where it does not; and validation by elevation RMSE at points is blind to artefacts that live in the derivatives. The authors documented the limitations; hurried users measured only what the paper measured.

**What would have caught it.** Looking at slope and curvature ([Chapter 54](ch54-evaluating-others-data.md), §54.2), comparing derivative distributions as DEMIX does, inspecting any flow-routing DEM for spurious barriers, and running the model on both the corrected DTM and its parent DSM with the difference as a sensitivity bound ([Chapter 43](ch43-traditional-vs-ml.md), [Chapter 55](ch55-public-products.md)).

## 56.15 Bridge decks that dam rivers and culverts that are not there

**What happened.** A DTM is bare earth, but "earth" at a bridge is a choice. Leave the deck in and the river is dammed, so a 2-D flood model fills the valley until it overtops; remove the deck but not the abutments and embankment and the model routes water through a notch narrower than the real opening. Culverts are the inverse: the road embankment is correctly in the DTM, the pipe through it is not, and a watershed delineation puts a lake behind every road. Both errors recur in practitioner reports and the hydro-conditioning literature (Poppenga & Worstell 2016; Lindsay 2016); USGS Elevation-Derived Hydrography work found that unmodified 3DEP DEMs could not yield usable drainage without breaching thousands of road and bridge barriers.

**Root cause.** Surface definition ([Chapter 32](ch32-dsm-to-dtm.md)): bridges are LAS class 17, but whether they leave the DEM depends on the specification — the USGS Lidar Base Specification requires removal in hydro-flattened DEMs; many national products do not — and culverts are invisible to every airborne sensor. The surface was correct; the model needed connectivity a surface cannot carry.

**What would have caught it.** Reading the specification for bridge treatment; an automated check flagging cells where a road polygon crosses a stream line and the DTM has no low point; and a hydro-enforced DEM with a culvert inventory, with the enforcement delivered as a separate layer rather than burned into the terrain ([Chapter 34](ch34-water-in-dems.md), [Chapter 61](ch61-hydrology.md)).

## 56.16 The power-line clearance survey flown cold

**What happened.** After the 2003 Northeast blackout, initiated by sagging conductors contacting trees, and a 2010 NERC alert on facility ratings, North American utilities flew tens of thousands of kilometres of transmission line with lidar to verify clearances. Several found that a survey flown on a cool, low-load morning showed clearances within limits while the same spans at maximum operating temperature would sag a metre or more into violation (NERC 2010); lines were derated or re-rated once the as-flown geometry was corrected to design temperature.

**Root cause.** Conductor sag depends on temperature, which depends on load, ambient temperature, wind, and sun (IEEE Std 738). Lidar measures the catenary at the instant of acquisition, which is useless for clearance unless the conductor temperature then is known and the catenary re-computed to the rated temperature. The lidar was accurate; the state of the object was not recorded ([Chapter 33](ch33-wires-and-thin-structures.md), [Chapter 27](ch27-moving-and-transient-objects.md)).

**What would have caught it.** Logging load and weather during acquisition (now standard in PLS-CADD workflows), modelling the catenary rather than measuring points, and contracts that require clearances at maximum operating temperature with the thermal assumptions stated ([Chapter 6](ch06-time-as-coordinate.md)).

## 56.17 Snow as bare earth, and the forest that "grew" between flights

**What happened.** Two recurring seasonal errors documented across the change-detection and glaciology literature. First, a DEM acquired with snow on the ground — spring-dated ArcticDEM strips, winter lidar flown for leaf-off, radar DSMs — is used as bare earth; 0.5–3 m of snow in open terrain, more in drifts, becomes terrain, and a later summer DEM shows "erosion" of exactly that amount. Deems, Painter & Finnegan (2013) review lidar snow-depth measurement by exploiting this: snow-on minus snow-off is a measurement when intended and an error when not. Second, DEMs from different seasons are differenced and show forest "growth" of metres or bare-earth change of decimetres in fields and wetlands that are leaf-on versus leaf-off, crop stage, and penetration differences ([Chapter 36](ch36-seasonal-variability.md)); ArcticDEM time series over tundra and national programmes whose repeats were flown in different seasons both show it.

**Root cause.** The epoch was recorded as a date but not as a **surface state** — snow depth, phenology, soil moisture, water level. Specifications constrain the state (leaf-off, snow-free, below bankfull), but the constraint is not always met, not always verifiable from the data, and rarely propagated into the derived DEM's metadata ([Chapter 29](ch29-processing-pipelines.md)).

**What would have caught it.** Checking flight days against snow-cover and NDVI records (MODIS, Sentinel-2); flat-surface tests on ploughed roads versus adjacent open ground; and treating any spatially coherent decimetre-to-metre offset over vegetated or open terrain as seasonal until proven otherwise ([Chapter 41](ch41-change-detection.md)).

## 56.18 The sonar "smile" that reached the chart

**What happened.** A composite case drawn from hydrographic QC practice and the error budgets of Hare, Godin & Mayer (1995) and the IHO *Manual on Hydrography* (C-13). A harbour-approach multibeam survey was processed with a sound-speed profile cast at the start of the day in a stratified estuary. As the tide turned and fresher water moved in, actual surface sound speed diverged from the profile by several metres per second; outer beams refracted more than assumed, so each swath curved upward at its edges — the **"smile"**. Across overlapping lines the smiles partly cancelled, the grid averaged to a plausible bottom with a 0.2–0.4 m ripple at swath edges, and the crossline check — a single line down the channel centre, where the error is smallest — passed. A later survey with proper casts found the charted channel edges shoaler by 0.3 m over several hundred metres.

**Root cause.** Refraction has a known signature (error growing with beam angle and depth, symmetric across the swath), and the crossline test was insensitive to it because it compared nadir with nadir. The QC answered a different question from the one that mattered, and gridding smoothed the rest away ([Chapter 20](ch20-sonar.md), [Chapter 53](ch53-accuracy-assessment.md)).

**What would have caught it.** Continuous surface sound speed at the transducer with an alarm on divergence; more frequent casts in stratified water; crosslines perpendicular to the main lines so outer beams meet nadir beams; per-beam-angle residual analysis in overlaps (the "wobble" and refraction tests of NOAA QC Tools and CARIS/QPS equivalents); and a TVU-aware grid (CUBE, BAG uncertainty) in which the swath edges would have shown elevated uncertainty ([Chapter 26](ch26-survey-planning.md), [Chapter 47](ch47-file-formats.md)).

## 56.19 GNSS jamming and spoofing in survey operations

**What happened.** From about 2016, GNSS interference reports accumulated around the Black Sea, eastern Mediterranean, and later the Baltic. C4ADS (2019) documented nearly 10,000 spoofing events affecting more than 1,300 vessels in Russian and Syrian waters in 2016–2018, including receivers reporting positions at inland airports. In 2022–2024 EASA and national authorities issued jamming bulletins; in April 2024 Finnair suspended flights to Tartu after GNSS-dependent approaches became unreliable; the US Maritime Administration issued repeated advisories. Survey vessels in these waters reported RTK fixes jumping by metres to kilometres, PPP failing to converge, and INS-aided systems drifting when GNSS was silently corrupted rather than lost.

**Root cause.** Positioning systems were designed for a benign signal environment. **Jamming** removes the signal, which most receivers detect; **spoofing** replaces it with a plausible false one, which most do not. A survey under spoofing yields internally consistent data with a wrong absolute position, unfixable afterwards if the offset drifted ([Chapter 12](ch12-gnss.md)); fix type, PDOP, and residuals can all look normal.

**What would have caught it.** Receiver-level spoofing detection (cross-constellation and cross-frequency consistency, signal-power monitoring, Galileo OSNMA); independent cross-checks — INS drift, terrain-aided navigation against prior bathymetry, radar or visual fixes ([Chapter 14](ch14-positioning-beyond-gnss.md)); raw-observable logging for forensics; and, where interference is reported, flagging absolute position as unverified in the metadata ([Chapter 69](ch69-security-sovereignty-privacy-ethics.md)).

## 56.20 Historical: Everest's height and the shape of the Earth

**What happened.** Two episodes from [Chapter 72](ch72-history.md) whose failure modes recur. In the 1730s the French Academy sent expeditions to Lapland (Maupertuis, 1736–1737) and Peru (Bouguer, La Condamine, Godin, 1735–1744) to measure a degree of latitude near the pole and the equator and settle whether the Earth was flattened at the poles (Newton) or elongated (as the Cassinis' French arcs suggested); the Lapland degree came out longer, confirming oblateness, and the Cassini result proved an artefact of accumulated small errors in a short arc. In 1852 Radhanath Sikdar, chief computer of the Great Trigonometrical Survey of India, reduced observations of "Peak XV" from six stations 175–190 km away to a mean of 29,002 ft (8,840 m); Andrew Waugh announced it in 1856 and named the peak for George Everest (Keay 2000). The modern value of 8,848.86 m, agreed by Nepal and China in 2020, differs by about 9 m, mostly **atmospheric refraction** over very long lines and the difference between the 1850s local geoid and modern definitions.

**Root cause.** In both cases the measurement was precise and the systematic error was in the model — short-arc extrapolation and instrument bias for the Cassinis; refraction coefficients, deflection of the vertical, and geoid definition for Everest. Sikdar's team knew refraction dominated and said so; the story that they "added two feet so it would not look rounded" is folklore.

**What would have caught it.** Longer baselines and independent methods (the eighteenth-century answer); shorter lines, reciprocal observations, and GNSS on the summit (the modern ones). Disagreement between independent measurements is information about the model, not noise to average ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 7](ch07-shape-of-the-earth.md), [Chapter 11](ch11-history-of-positioning.md)).

## 56.21 One engineering project, three invisible shifts

**What happened.** A composite assembled from engineering-review experience; each error is documented in the chapters cited. A highway design combined a county lidar DTM (state plane, US survey feet, NAVD 88, GeoTIFF pixel-is-point), a consultant's drone DSM (UTM metres, ellipsoidal heights, pixel-is-area), and CAD coordinates in a **ground-distance** local system scaled from state plane by a combined factor of about 1.00012. The DTM was reprojected by an analyst who missed the AREA_OR_POINT flag (a half-pixel, 0.5 m shift); the DSM was converted with GEOID12A instead of GEOID18 (3–6 cm there); the CAD system read state plane as grid rather than ground, a 120 ppm difference worth about 1.8 m at 15 km from the project origin; and one file was in international rather than US survey feet, 2 ppm that moved northings by about 0.4 m. Earthwork quantities were off by several percent and a culvert invert was staked 0.3 m high before a field check caught the accumulation.

**Root cause.** Each system was internally correct and each conversion individually small; none was visible at project scale, and the file formats carried the information to prevent three of them (CRS units, AREA_OR_POINT, vertical CRS) in metadata nobody read ([Chapter 10](ch10-projections-and-resampling.md), [Chapter 31](ch31-interpolation-and-gridding.md), [Chapter 47](ch47-file-formats.md)).

**What would have caught it.** A single project control statement (datums with realization and epoch, projection, linear unit, grid-to-ground policy, pixel registration) enforced at ingest; a check of each dataset against the same three physical control points before merging; and a rule that any difference between two surfaces of the same terrain be inspected for a planar trend before being accepted as real.

## 56.22 Lidar deserts: hazards unmapped where lidar is not

**What happened.** 3DEP brought the conterminous United States to near-complete QL2 coverage in the 2020s; the Netherlands has five national lidar epochs; England, Denmark, Finland, Switzerland, and Spain have national metre-scale terrain. Across most of Africa, South and Southeast Asia, and Latin America — home to the majority of people exposed to floods, landslides, and coastal inundation — the best public terrain remains a 30 m DSM from 2000 or 2011–2015 ([Chapter 55](ch55-public-products.md)). Schumann and Bates (2018) and Hawker et al. (2018) made the case explicitly: the absence of a high-accuracy open global DTM is the largest controllable error in global flood-risk estimates, concentrated where the risk is. ML-corrected products respond to the gap, but their training data come from lidar-rich countries, so their accuracy is lowest where most needed ([Chapter 43](ch43-traditional-vs-ml.md)); within rich countries the pattern recurs, with tribal lands, rural counties, and some floodplains mapped last.

**Root cause.** Elevation data are collected where someone pays, and hazard exposure is not correlated with ability to pay; the uncertainty in a flood map is a function of national income ([Chapter 69](ch69-security-sovereignty-privacy-ethics.md)).

**What would have caught it.** A gap to name rather than an error to catch: report the terrain source and its stratified uncertainty with every exposure estimate; fund open national lidar in low- and middle-income countries ([Chapter 28](ch28-reducing-cost.md)). [Chapter 73](ch73-open-problems.md) lists a global open DTM at 1–5 m among the field's unmet needs.

## 56.23 A successful catch: independent QC rejects a lidar delivery

**What happened.** A composite describing a process that works, assembled from USGS and state-programme practice under the Lidar Base Specification. A vendor delivered a 1,200 km² QL2 block — classified LAZ, 1 m hydro-flattened DTM, swath-separation report, and an accuracy report showing NVA of 6.8 cm RMSE$_z$ against 32 checkpoints (specification ≤ 10 cm). The independent QC contractor found the vendor's checkpoints clustered on paved roads in the eastern third. The QC team surveyed 48 more checkpoints across all land-cover classes and the full extent, computed per-swath difference rasters in the overlaps, and ran flat-surface tests on 11 parking lots and two runways. The overlap rasters showed a systematic 11–14 cm step between adjacent flight lines across the western half — a roll-boresight or trajectory error on one lift — and western checkpoints showed a +9 cm mean bias with 13 cm RMSE$_z$. The delivery was rejected under the LBS relative-accuracy requirement (≤ 8 cm RMSD$_z$ in swath overlap for QL2); the vendor reprocessed the lift with corrected boresight values, and the redelivery passed with NVA 5.9 cm and overlap RMSD$_z$ 4 cm.

**Root cause (of the near-miss).** The vendor's QC asked "does the product meet NVA at our checkpoints?" and the answer was yes. The independent QC asked "is there any region or component where it fails?" and designed tests — checkpoint distribution, swath-overlap difference, flat-surface noise — that reveal a localized systematic error a global RMSE hides ([Chapter 53](ch53-accuracy-assessment.md), [Chapter 54](ch54-evaluating-others-data.md)).

**What made it work.** A specification with testable relative-accuracy criteria; a QC role contractually independent of the producer with budget for its own checkpoints; and tests chosen for the known failure modes of the sensor and workflow rather than to confirm the headline statistic ([Chapter 18](ch18-topographic-lidar.md)). The independent QC cost a small fraction of the acquisition; a 12 cm step through a floodplain DTM would have been paid for by people who never saw the data.

<!-- figure: Figure 56.1 — Matrix of the 23 cases (rows) against failure-mode categories (columns: datum/epoch, surface definition, metadata/units, measurement physics, missing data, decision process), with cells marked where a category contributed; most rows have two or more marks -->

<!-- figure: Figure 56.2 — Bare-earth lidar hillshade of the Oso valley (2013 data) with the outlines of pre-2014 landslide deposits and the 2014 runout, after Haugerud (2014), illustrating how legible the hazard was in the DTM -->

## Then & now

The cases span three centuries, and what fails has shifted less than the technology. In the eighteenth and nineteenth centuries (56.20) the failures were in the physical model — refraction, the figure of the Earth — and were resolved by independent measurement over longer baselines. In the twentieth century (56.2, 56.3, 56.6, 56.7) they were in the reference: soundings decades old, benchmarks that had sunk, units crossing an interface unchecked, a seafloor assumed static. ⟨H⟩ The USS *San Francisco* grounding (56.1) and the Grand Banks cables (56.7) are both in the gis-history timeline because each changed how a community thought about seafloor data — charted confidence and seafloor dynamics respectively. In the twenty-first century the measurements are rarely at fault; the failures are in **surface definition** (56.13–56.15, 56.17), **epoch and state** (56.4, 56.5, 56.9, 56.16), **derived-data disclosure** (56.8), **signal environment** (56.19), and above all the **decision process** that had the data and did not use it (56.10, 56.11). The successful catch (56.23) is modern too, resting on testable relative criteria and an independent QC role, both products of the 2010s. What has not changed is that in almost every case the information needed to prevent the failure existed beforehand, somewhere, in a form the decision-maker did not see.

## Validation & uncertainty

The cases are an argument for the validation chapters, and they can be read as a checklist of the failure modes those chapters' tests are designed to catch. Table 56.1 maps each case to the test that would have exposed it and to the chapter where that test is described.

| Case | Dominant failure mode | Test that exposes it | Where described |
|---|---|---|---|
| 56.1 San Francisco | Unmeasured cells presented as data | Source/confidence layer (CATZOC, TID) along the route | [Ch. 55](ch55-public-products.md), [Ch. 62](ch62-navigation-and-charting.md) |
| 56.2 QE2 | Uncertainty terms summed without budget | Under-keel clearance as a propagated budget | [Ch. 5](ch05-error-and-uncertainty.md), [Ch. 62](ch62-navigation-and-charting.md) |
| 56.3 Katrina | Vertical control out of date | Re-observe benchmarks; CORS/InSAR subsidence rates | [Ch. 38](ch38-plate-motion-and-vlm.md), [Ch. 25](ch25-calibration-infrastructure.md) |
| 56.4 / 56.5 Tōhoku, Kaikōura | Coordinates without epoch | Epoch on every coordinate; deformation model | [Ch. 39](ch39-earthquakes-volcanoes-landslides.md), [Ch. 6](ch06-time-as-coordinate.md) |
| 56.6 Units | Interface without unit check | Sea-level and benchmark sanity checks; CRS unit audit | [Ch. 54](ch54-evaluating-others-data.md), [Ch. 47](ch47-file-formats.md) |
| 56.7 Grand Banks | Static-seafloor assumption | Repeat bathymetry; geohazard mapping | [Ch. 66](ch66-coastal-marine-polar-lakes-rivers.md) |
| 56.8 Strava | Disclosure through aggregation | Derived-product disclosure review | [Ch. 69](ch69-security-sovereignty-privacy-ethics.md) |
| 56.9 Borders | Boundary on a moving surface | DEM epoch vs rate of change; MDC | [Ch. 41](ch41-change-detection.md), [Ch. 68](ch68-legal-issues.md) |
| 56.10 Oso | Data not read | Lidar landslide inventory; hillshade literacy | [Ch. 57](ch57-visualizing-dems.md) |
| 56.11 Brumadinho | Detection vs decision | Specified alarm threshold vs MDC with false-alarm rate | [Ch. 41](ch41-change-detection.md) |
| 56.12 MH370 | Unmapped seafloor | TID fraction; survey before operations | [Ch. 2](ch02-uses-bathymetry.md) |
| 56.13 Flood maps | DSM as DTM; datum mismatch | Stratified ICESat-2 comparison; sea-level test | [Ch. 54](ch54-evaluating-others-data.md), [Ch. 9](ch09-vertical-datums.md) |
| 56.14 FABDEM terraces | Artefacts in derivatives | Slope/curvature inspection; DEMIX criteria | [Ch. 54](ch54-evaluating-others-data.md), [Ch. 43](ch43-traditional-vs-ml.md) |
| 56.15 Bridges, culverts | Surface vs connectivity | Stream-crossing audit; hydro-enforcement layer | [Ch. 34](ch34-water-in-dems.md), [Ch. 61](ch61-hydrology.md) |
| 56.16 Power lines | Object state at epoch | Record load/temperature; model to rated state | [Ch. 33](ch33-wires-and-thin-structures.md) |
| 56.17 Snow, leaves | Surface state at epoch | Flight-day snow/NDVI check; flat-surface test | [Ch. 36](ch36-seasonal-variability.md) |
| 56.18 Sonar smile | Insensitive QC test | Perpendicular crosslines; per-angle residuals; TVU grid | [Ch. 20](ch20-sonar.md), [Ch. 53](ch53-accuracy-assessment.md) |
| 56.19 Jamming | Corrupted reference signal | Multi-source position consistency; raw logging | [Ch. 12](ch12-gnss.md), [Ch. 14](ch14-positioning-beyond-gnss.md) |
| 56.20 Everest, Cassini | Model error mistaken for noise | Independent method; longer baseline | [Ch. 5](ch05-error-and-uncertainty.md), [Ch. 72](ch72-history.md) |
| 56.21 Three shifts | Accumulated small conversions | Common control points; planar-trend test on differences | [Ch. 10](ch10-projections-and-resampling.md) |
| 56.22 Lidar deserts | Uncertainty correlated with need | Report terrain source and stratified uncertainty | [Ch. 69](ch69-security-sovereignty-privacy-ethics.md), [Ch. 73](ch73-open-problems.md) |
| 56.23 QC catch | — (success) | Spatially distributed checkpoints; swath-overlap difference | [Ch. 53](ch53-accuracy-assessment.md) |

*Table 56.1 — Each case mapped to the failure mode and the test that exposes it.*

Three properties of the table deserve comment. The tests are cheap: the flat-surface test, the sea-level sanity check, the ICESat-2 comparison, the planar-trend test on a difference map, and the stream-crossing audit each take an hour or a day, against failures that cost lives, ships, and cities. Most cases pair a data gap with a human assumption that filled it, which is why the Pitfalls warn against reading the cases as carelessness. And several (56.11, 56.12, 56.22) are limits of knowledge rather than failures of validation, where the honest response is to state the limit — a detection threshold, an unmapped fraction, a stratified uncertainty.

> **Rule of thumb.** When a DEM, chart, or difference map shows something surprising, the order of hypotheses is: (1) datum, units, or registration; (2) epoch, surface state, or surface definition; (3) sensor artefact or processing error; (4) real change. In the cases above, hypothesis (4) was the right one less than half the time, and it was never safe to assume it first. The rule fails when the surprise is a sudden, spatially coherent step that coincides with a known event — an earthquake, a landslide — where (4) jumps to the top; even then, (1) and (2) must still be excluded for the magnitude to be trusted.

> **Worked example.** The under-keel clearance budget that would have described the *QE2* case (56.2), using the NTSB's figures in feet because the chart and the inquiry used them. Charted depth at MLW: 39 ft, but the chart's sounding density in a rocky area implies an unsampled-minimum allowance; the rocks actually struck were at about 34–35 ft, so take the shoalest plausible depth as 34.5 ft. Predicted tide: assumed +2.0 ft, actual about +0.5 ft; a prudent plan uses the prediction minus its uncertainty, say +0.3 ft. Static draft forward: 32.3 ft. Squat at 24–25 kn in about 40 ft of water: the bridge assumed 1–1.5 ft; a Barrass-type estimate for a block coefficient around 0.6 at 25 kn in open shallow water gives several feet, and the NTSB's analysis put the bow sinkage at not less than 2.7 ft and the total squat plausibly in the 4.5–8 ft range. Clearance with the bridge's assumptions: $39 + 2.0 - 32.3 - 1.5 = 7.2$ ft. Clearance with the budgeted values: $34.5 + 0.3 - 32.3 - 4.5 = -2.0$ ft at the low end of squat, and $-5.5$ ft at the high end. The sign of the answer changed because three terms were each taken at their optimistic value. The arithmetic is trivial; the discipline of writing it down with uncertainties is the lesson, and it is the same discipline as a lidar NVA budget or a GEBCO TID tabulation.

> **Try it.** Reproduce the first step of the Oso analysis (56.10) with open data: download the Washington DNR lidar DTM for the Oso quadrangle (or any valley with a landslide history), and make a multi-directional hillshade and a slope map. Expected outcome: the hummocky deposits of old landslides across the valley floor are obvious in the multi-directional hillshade and the slope map, and barely visible in a single-azimuth hillshade with the default 315° sun.
>
> ```bash
> # DTM in a projected CRS with metre units (reproject first if not)
> gdaldem hillshade -multidirectional -z 1.0 oso_dtm.tif oso_hs_multi.tif
> gdaldem hillshade -az 315 -alt 45 oso_dtm.tif oso_hs_315.tif
> gdaldem slope -p oso_dtm.tif oso_slope_pct.tif
> gdaldem color-relief oso_slope_pct.tif slope_ramp.txt oso_slope_rgb.tif
> # slope_ramp.txt: "0 255 255 255" / "15 200 200 255" / "30 100 100 255" / "60 0 0 128"
> ```

## Software

**Open source:** The tools that would have caught the cases are the ones catalogued in [Chapter 53](ch53-accuracy-assessment.md) and [Chapter 54](ch54-evaluating-others-data.md): **GDAL** (`gdaldem`, `gdalinfo` for AREA_OR_POINT and units, `gdalwarp` with vertical CRS), **PDAL** (swath-overlap difference and classification audits), **xdem** and **demcoreg** (co-registration and planar-trend detection in difference maps), **MB-System** (multibeam refraction and crossline analysis), **SlideRule/icepyx** (ICESat-2 comparisons), **QGIS** (hillshade literacy), **GMT** (bathymetric compilations and TID maps), and **PROJ** (deformation models and epoch transformations). Caveat: every one of these produces a plausible-looking output from wrong inputs; the tool does not know the datum.

**Free but closed:** NOAA's **QC Tools** for hydrographic surfaces (flier finder, grid QA, crossline analysis), the **NGS OPUS** and **NCAT/VDatum** services for coordinate and datum checks, and the **GSI/LINZ/NGS** deformation-model calculators.

**Commercial:** **CARIS HIPS and SIPS**, **QPS Qimera** (refraction and wobble analysis), **TerraSolid TerraMatch** (strip adjustment that would have fixed 56.23's lift), **PLS-CADD** (conductor thermal modelling for 56.16), and **Global Mapper**/**ArcGIS Pro** for general inspection.

## Standards & guides

- **IHO S-44**, ed. 6.1.0 (2022) and **S-57/S-101 CATZOC / quality of bathymetric data** — survey confidence attributes behind 56.1 and 56.2.
- **NOAA Hydrographic Surveys Specifications and Deliverables (HSSD)** and **Field Procedures Manual** — sound-speed, crossline, and QC requirements behind 56.18.
- **USGS Lidar Base Specification**, 2024 revision — relative accuracy, swath-overlap, bridge and hydro-flattening rules behind 56.15 and 56.23.
- **ASPRS Positional Accuracy Standards**, Edition 2 (2023) — checkpoint distribution and NVA/VVA reporting behind 56.23.
- **NGS Blueprint for the Modernized NSRS** (NOAA Technical Reports 62, 64, 67) and **NGS 58/59** — time-dependent vertical control behind 56.3.
- **NIST/NOAA Federal Register Notice on deprecation of the US survey foot** (2019, effective 2022-12-31) — 56.6 and 56.21.
- **IEEE Std 738** (conductor temperature) and **NERC Alert on Facility Ratings** (2010) — 56.16.
- **Global Industry Standard on Tailings Management** (ICMM/UNEP/PRI 2020) — monitoring and decision requirements behind 56.11.
- **IHO B-12 Crowdsourced Bathymetry Guidance** and **Seabed 2030 Roadmap** — 56.12.
- **ISO 19157** (data quality) and **ISO 19115** (metadata) — the fields whose absence recurs in nearly every case.

## Pitfalls

- **Reading case files as "they were careless"** → hindsight makes the missed signal look obvious → ask instead what system condition let a known failure mode through; the fix is procedural, not personal.
- **Forgetting that most failures pair a data gap with a human assumption** → each alone is survivable → design checks that test the assumption (is this surface bare earth? is this coordinate current?) rather than only the data.
- **Testing only the headline statistic** → NVA passed in 56.23's first delivery, crossline passed in 56.18 → add tests for the known failure modes of the sensor and workflow: spatial distribution, swath overlap, per-angle residuals, derivative inspection.
- **Treating a chart, benchmark, or DEM as present-tense** → it is a record of a past measurement → attach an epoch and a rate of change to every reference (56.1, 56.3, 56.4, 56.5, 56.9).
- **Assuming aggregate or derived products are harmless** → the derivation adds information → run a disclosure review on derived terrain and activity products (56.8).
- **Mistaking a detection problem for a decision problem, or vice versa** → InSAR could see Brumadinho moving; no one had specified what movement meant → write the alarm threshold and the authority to act into the monitoring design (56.11).
- **Letting unit and registration metadata ride along unread** → three invisible shifts in 56.21 and a Mars orbiter in 56.6 → enforce CRS, unit, and AREA_OR_POINT checks at ingest, automatically.
- **Using a DSM as a DTM in the one place it matters most** → low coasts and forests (56.13) → stratify any accuracy test by land cover; never report coastal exposure without the DEM's surface type stated.
- **Trusting corrected or learned surfaces by their elevation RMSE alone** → terraces live in slope (56.14) → inspect derivatives and run the analysis on the parent DSM as a sensitivity case.
- **Running a QC test that cannot detect the error you fear** → nadir-to-nadir crosslines are blind to refraction (56.18) → match the test geometry to the error geometry.
- **Confusing surface state with surface** → snow, leaves, conductor temperature (56.16, 56.17) → record state variables with the acquisition and constrain them in the specification.
- **Assuming the signal environment is benign** → spoofed positions look like good positions (56.19) → cross-check against an independent positioning source and log raw observables.
- **Equating "no data" with "nothing there"** → the seamount (56.1) and the MH370 seafloor (56.12) → carry a source or confidence layer with every bathymetric product and look at it before planning.

## Key takeaways

- Almost every disaster in this chapter had a data-quality signal available in advance — an old survey date, a sunk benchmark, a hummocky hillshade, a mismatched unit — that no one was positioned to see or obliged to act on.
- Validation is cheap compared with the alternative: an hour of flat-surface tests, a day of checkpoint surveying, or a glance at a TID layer, against lives, ships, and cities.
- Failures combine a datum, epoch, surface-definition, or metadata gap with a human assumption that filled it; fix the system so the assumption is tested, not the person who made it.
- Epoch is part of every coordinate and every surface: the ground moves (56.3–56.5), the ice melts (56.9), the conductor sags (56.16), and the snow falls (56.17).
- Surface definition — DSM, DTM, bridge deck in or out, snow on or off — decides fitness for use more often than resolution or accuracy does.
- Tests must match the error geometry: global RMSE does not see a swath step; nadir crosslines do not see refraction; elevation RMSE does not see terraces.
- Absence of measurement is information; carry it as a source or confidence layer and look at it before every decision (56.1, 56.12, 56.22).
- Teach with cases: a practitioner who has worked through the *QE2* budget or the Oso hillshade will run the test next time without being told.

## References

- Bielski, C., López-Vázquez, C., Grohmann, C. H., Guth, P. L., Hawker, L., et al. (2024). Novel approach for ranking DEMs: Copernicus DEM improves one arc second open global topography. *IEEE Transactions on Geoscience and Remote Sensing*, 62:4503922.
- C4ADS (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Center for Advanced Defense Studies, Washington, DC.
- Clark, K. J., Nissen, E. K., Howarth, J. D., Hamling, I. J., Mountjoy, J. J., Ries, W. F., Jones, K., Goldstien, S., Cochran, U. A., Villamor, P., Hreinsdóttir, S., Litchfield, N. J., Mueller, C., Berryman, K. R., & Strong, D. T. (2017). Highly variable coastal deformation in the 2016 Mw7.8 Kaikōura earthquake reflects rupture complexity along a transpressional plate boundary. *Earth and Planetary Science Letters*, 474:334–344.
- Deems, J. S., Painter, T. H., & Finnegan, D. C. (2013). Lidar measurement of snow depth: a review. *Journal of Glaciology*, 59(215):467–479.
- Dixon, T. H., Amelung, F., Ferretti, A., Novali, F., Rocca, F., Dokka, R., Sella, G., Kim, S.-W., Wdowinski, S., & Whitman, D. (2006). Subsidence and flooding in New Orleans. *Nature*, 441:587–588.
- Gama, F. F., Mura, J. C., Paradella, W. R., & de Oliveira, C. G. (2020). Deformations prior to the Brumadinho dam collapse revealed by Sentinel-1 InSAR data using SBAS and PSI techniques. *Remote Sensing*, 12(21):3664.
- Geospatial Information Authority of Japan (GSI) (2011). *Crustal deformation and revision of survey results associated with the 2011 off the Pacific coast of Tohoku Earthquake* (notices and press releases, March–October 2011). (verify exact titles)
- Grebby, S., Sowter, A., Gluyas, J., Toll, D., Gee, D., Athab, A., & Girindran, R. (2021). Advanced analysis of satellite data reveals ground deformation precursors to the Brumadinho Tailings Dam collapse. *Communications Earth & Environment*, 2:2.
- Guth, P. L., & Geoffroy, T. M. (2021). LiDAR point cloud and ICESat-2 evaluation of 1 second global digital elevation models: Copernicus wins. *Transactions in GIS*, 25(5):2245–2261.
- Hamling, I. J., Hreinsdóttir, S., Clark, K., et al. (2017). Complex multifault rupture during the 2016 Mw 7.8 Kaikōura earthquake, New Zealand. *Science*, 356(6334):eaam7194.
- Hare, R., Godin, A., & Mayer, L. A. (1995). *Accuracy Estimation of Canadian Swath (Multibeam) and Sweep (Multitransducer) Sounding Systems*. Canadian Hydrographic Service / University of New Brunswick technical report.
- Haugerud, R. A. (2014). *Preliminary Interpretation of Pre-2014 Landslide Deposits in the Vicinity of Oso, Washington*. USGS Open-File Report 2014-1065.
- Hawker, L., Bates, P., Neal, J., & Rougier, J. (2018). Perspectives on digital elevation model (DEM) simulation for flood modeling in the absence of a high-accuracy open access global DEM. *Frontiers in Earth Science*, 6:233.
- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., & Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters*, 17(2):024016.
- Heezen, B. C., & Ewing, M. (1952). Turbidity currents and submarine slumps, and the 1929 Grand Banks earthquake. *American Journal of Science*, 250(12):849–873.
- Hern, A. (2018). Fitness tracking app Strava gives away location of secret US army bases. *The Guardian*, 28 January 2018.
- Holden, D., Donegan, S., & Pon, A. (2020). Brumadinho Dam InSAR study: analysis of TerraSAR-X, COSMO-SkyMed and Sentinel-1 images preceding the collapse. In *Proceedings of the 2020 International Symposium on Slope Stability in Open Pit Mining and Civil Engineering*, Australian Centre for Geomechanics. (verify)
- ICMM, UNEP, & PRI (2020). *Global Industry Standard on Tailings Management*.
- Interagency Performance Evaluation Task Force (IPET) (2007). *Performance Evaluation of the New Orleans and Southeast Louisiana Hurricane Protection System*, Final Report, Vol. I–IX. US Army Corps of Engineers.
- Iverson, R. M., George, D. L., Allstadt, K., Reid, M. E., Collins, B. D., Vallance, J. W., Schilling, S. P., Godt, J. W., Cannon, C. M., Magirl, C. S., Baum, R. L., Coe, J. A., Schulz, W. H., & Bower, J. B. (2015). Landslide mobility and hazards: implications of the 2014 Oso disaster. *Earth and Planetary Science Letters*, 412:197–208.
- Keaton, J. R., Wartman, J., Anderson, S., Benoît, J., deLaChapelle, J., Gilbert, R., & Montgomery, D. R. (2014). *The 22 March 2014 Oso Landslide, Snohomish County, Washington*. GEER Association Report GEER-036.
- Keay, J. (2000). *The Great Arc: The Dramatic Tale of How India Was Mapped and Everest Was Named*. HarperCollins, London.
- Kulp, S. A., & Strauss, B. H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications*, 10:4844.
- Lindsay, J. B. (2016). The practice of DEM stream burning revisited. *Earth Surface Processes and Landforms*, 41(5):658–668.
- National Transportation Safety Board (1993). *Grounding of the United Kingdom Passenger Vessel RMS Queen Elizabeth 2 near Cuttyhunk Island, Vineyard Sound, Massachusetts, August 7, 1992*. Marine Accident Report NTSB/MAR-93/01.
- NERC (2010). *Recommendation to Industry: Consideration of Actual Field Conditions in Determination of Facility Ratings*. North American Electric Reliability Corporation Alert, 7 October 2010.
- NIST & NOAA (2019). Deprecation of the United States (U.S.) survey foot. *Federal Register*, 84(197):54562–54566 (notice), with final decision effective 31 December 2022. (verify page numbers)
- Picard, K., Brooke, B. P., Harris, P. T., Siwabessy, P. J. W., Coffin, M. F., Tran, M., Spinoccia, M., Weales, J., Macmillan-Lawler, M., & Sullivan, J. (2018). Malaysia Airlines flight MH370 search data reveal geomorphology and seafloor processes in the remote southeast Indian Ocean. *Marine Geology*, 395:301–319.
- Picard, K., Brooke, B., & Coffin, M. F. (2017). Geological insights from Malaysia Airlines flight MH370 search. *Eos*, 98.
- Piper, D. J. W., Shor, A. N., & Hughes Clarke, J. E. (1988). The 1929 "Grand Banks" earthquake, slump, and turbidity current. *Geological Society of America Special Paper*, 229:77–92.
- Poppenga, S. K., & Worstell, B. B. (2016). Hydrologic connectivity: quantitative assessments of hydrologic-enforced drainage structures in an elevation model. *Journal of Coastal Research*, SI 76:90–106.
- Robertson, P. K., de Melo, L., Williams, D. J., & Wilson, G. W. (2019). *Report of the Expert Panel on the Technical Causes of the Failure of Feijão Dam I*. Commissioned by Vale S.A.
- Schumann, G. J.-P., & Bates, P. D. (2018). The need for a high-accuracy, open-access global DEM. *Frontiers in Earth Science*, 6:225.
- Seed, R. B., Bea, R. G., Abdelmalak, R. I., et al. (2006). *Investigation of the Performance of the New Orleans Flood Protection Systems in Hurricane Katrina on August 29, 2005*. Independent Levee Investigation Team Final Report, University of California, Berkeley.
- Stephenson, A. G., LaPiana, L. S., Mulville, D. R., Rutledge, P. J., Bauer, F. H., Folta, D., Dukeman, G. A., Sackheim, R., & Norvig, P. (1999). *Mars Climate Orbiter Mishap Investigation Board Phase I Report*. NASA, 10 November 1999.
- US Navy (2005). *Command Investigation into the Grounding of USS San Francisco (SSN 711) on 8 January 2005* (JAGMAN investigation, Commander Submarine Force US Pacific Fleet; released in redacted form). (verify title)

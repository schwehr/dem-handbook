# Chapter 62 — Navigation and charting from elevation: marine, aviation, drones, vehicles, robots

> **Part XIV — Domain deep dives.** The safety-critical uses of elevation data, where the shoalest sounding, the highest obstacle, or the nearest wall matters more than the mean, and where a DEM becomes a certified navigation product or a sensor in a control loop.

**In this chapter.** A general-purpose DEM describes a surface on average; a navigation product must bound it in the dangerous direction and say how sure it is. You will be able to read a nautical chart's depths as shoal-biased, datum-referenced, uncertainty-tagged values rather than elevations; compute an under-keel clearance budget with the IHO S-44 total vertical uncertainty as an explicit term; explain what S-102, S-104, and S-111 add to a static chart; state the ICAO terrain and obstacle data requirements for Areas 1–4 and why DO-200B treats data processing as a safety function; decide which surface a drone's 400 ft AGL limit is measured from; see how HD maps, robot elevation maps, and planetary terrain-relative navigation all turn a DEM into a sensor whose error budget feeds a controller; and understand who certifies these products, how currency is maintained, and why uncertainty belongs in every go/no-go decision.

## 62.1 Marine: charts, datums, clearance, and the dynamic chart

A nautical chart is an elevation model with the sign flipped and the philosophy changed. Where a DTM reports its best estimate of the ground, a chart reports the **shoalest** (shallowest) depth a mariner might encounter in each area, referenced to a **chart datum** chosen so that the actual water is almost never lower than the datum implies. The two conventions in use are **Lowest Astronomical Tide (LAT)**, the lowest level predictable from tidal harmonics over a nodal cycle (18.6 years), adopted by the IHO and most of the world, and **Mean Lower Low Water (MLLW)**, the average of the lower of the two daily low waters over the US National Tidal Datum Epoch (currently 1983–2001), used by NOAA. Both are *local* surfaces that vary by meters along a coast and are tied to the ellipsoid and orthometric datums through models such as NOAA's VDatum or the UK's VORF ([Chapter 9](ch09-vertical-datums.md)). Charted depth is therefore depth below chart datum, and the water actually available is charted depth plus the tide height above datum at that time.

**Electronic Navigational Charts (ENCs)** encode this in the IHO **S-57** data model (object classes such as DEPARE depth areas, SOUNDG soundings, OBSTRN obstructions, WRECKS), displayed under the **S-52** presentation library on type-approved ECDIS; the successor **S-101** product specification, built on the **S-100** framework, is being introduced in the 2020s with dual-fuel ECDIS able to read both. ENC soundings are a selection, not a grid: from millions of multibeam soundings the hydrographic office selects a sparse set that preserves the shoalest values and the navigationally significant pattern (**shoal-biased sounding selection**), draws depth contours that enclose everything shallower than their value, and encloses hazards in polygons. A chart that reported the mean depth of each cell would, on a rough bottom, systematically overstate the available water by half the local relief.

**Gridded bathymetry for navigation** follows the same principle. The **BAG** format ([Chapter 47](ch47-file-formats.md)) and the **S-102** bathymetric surface product carry a depth and an uncertainty per node; when a navigation-grade grid is generated from CUBE or similar estimators ([Chapter 20](ch20-sonar.md); Calder and Wells 2007), the node value in a product destined for mariners is chosen by **shoal-biased** rules—the shoalest hypothesis or the shoalest sounding within the node footprint—rather than the mean, and the uncertainty layer propagates the S-44 total vertical uncertainty rather than a sampling standard error. S-102 Edition 3.0.0 (2024) adds a quality-of-bathymetric-coverage feature and is designed to be overlaid in ECDIS with **S-104** (water level information for surface navigation: predicted and forecast tide and surge as time-varying grids) and **S-111** (surface currents), so that the ECDIS can compute, for a given time, the actual water depth at every node and a time-varying no-go area for the vessel's draft. This is the **dynamic chart**: static depth plus forecast water level plus the vessel's own draft and motion. Its uncertainty is the sum of the parts, and S-102's uncertainty layer is the first of them to be delivered to the bridge.

The mariner's view of uncertainty has historically been the **CATZOC** (Category of Zone of Confidence) attribute of each depth area in an ENC: A1 (position ± 5 m + 5 % of depth, depth ± 0.5 m + 1 % of depth, full-seafloor search), A2 (± 20 m; ± 1.0 m + 2 %), B (± 50 m; ± 1.0 m + 2 %, no full search), C (± 500 m; ± 2.0 m + 5 %), D (worse than C), and U (unassessed). The IHO's **S-67** *Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts* (Edition 1.0.0, 2020) explains these to navigators and shows how to convert a CATZOC into a depth allowance; S-101 replaces CATZOC with a **Quality of Bathymetric Data** feature carrying survey date, technique, and uncertainties explicitly. In practice large fractions of the world's charted waters remain CATZOC C, D, or U, and the depth allowance for a CATZOC B area in 20 m of water (1.0 + 0.02 × 20 = 1.4 m) exceeds the keel clearance many ports plan for.

The **IHO S-44** standard (Edition 6.1.0, 2022) specifies survey orders whose vertical uncertainty is expressed at 95 % as

$$\mathrm{TVU}_{\max}(d) = \sqrt{a^2 + (b \cdot d)^2},$$

with $(a, b)$ = (0.15 m, 0.0075) for Exclusive Order, (0.25 m, 0.0075) for Special Order, (0.5 m, 0.013) for Orders 1a and 1b, and (1.0 m, 0.023) for Order 2, and whose **feature detection** requirements are cubic features of 0.5 m (Exclusive), 1 m (Special), and 2 m to 40 m depth, 10 % of depth beyond (Order 1a); Order 1b and Order 2 do not require full-seafloor search ([Chapter 70](ch70-specifications-guided-tour.md) walks through the whole standard). The feature-detection requirement, not the TVU, is what distinguishes a chart-grade survey from a scientific one: a survey can have excellent TVU on the soundings it collected and still miss a 1 m boulder between lines.

**Survey currency** is part of the product. Sandy approaches and dredged channels change on time scales of months; a sounding's date is a chart attribute (SORDAT, and the source diagram) and the hydrographic office issues **Notices to Mariners** for changes between editions. Ports and channel authorities run **condition surveys** (often monthly in active dredging) under NOAA's Hydrographic Surveys Specifications and Deliverables (HSSD) or USACE EM 1110-2-1003, reporting shoalest depth per channel reach and controlling depth, which is the depth a vessel can rely on through the full channel width—another worst-case statistic. **Autonomous surface vessels** invert the relation: the chart becomes a sensor input to the vessel's path planner, and the uncertainty tags (CATZOC, S-102 uncertainty) become constraints on allowable routes rather than advisory information for a human.

<!-- figure: Figure 62.1 — Cross-section of a harbor channel showing chart datum (LAT/MLLW), charted depth, tide height, vessel draft, squat, heel, and the S-44 TVU allowance that together make up the under-keel clearance budget. -->

> **Worked example.** *Under-keel clearance with S-44 uncertainty.* A bulk carrier with static draft 14.0 m plans to transit a dredged channel charted at 15.5 m below MLLW. The channel was surveyed to S-44 Special Order ($a$ = 0.25 m, $b$ = 0.0075) three months ago. Predicted tide at transit is +1.2 m above MLLW; the S-104 forecast carries a stated uncertainty of 0.15 m (95 %). Transit speed 10 kn through the water gives a predicted squat of 0.9 m (from the port's squat tables); heel allowance 0.2 m; wave-induced motion allowance 0.3 m.
>
> Available depth at transit = 15.5 + 1.2 = 16.7 m. Required depth = 14.0 + 0.9 + 0.2 + 0.3 = 15.4 m. Nominal clearance = 1.3 m.
>
> Depth uncertainty terms (95 %): survey TVU at $d$ = 15.5 m is $\sqrt{0.25^2 + (0.0075 \times 15.5)^2} = \sqrt{0.0625 + 0.0135} = 0.276$ m; tide forecast 0.15 m; squat prediction (say) ± 0.3 m; draft reading ± 0.1 m. Combined in quadrature: $\sqrt{0.276^2 + 0.15^2 + 0.3^2 + 0.1^2} = 0.45$ m at 95 %. Net clearance after uncertainty = 1.3 − 0.45 = 0.85 m, which exceeds the port's 0.5 m minimum, so the transit is acceptable—*if* the channel has not shoaled since the survey. If the same channel had been charted from a CATZOC B survey instead (allowance 1.0 + 0.02 × 15.5 = 1.31 m), the net clearance would be negative and the transit would require a fresh survey or less draft. The arithmetic is simple; the discipline is to include the survey uncertainty at all, which many UKC calculations still do not.

## 62.2 Aviation: terrain, obstacles, and the integrity of a database

Aviation's elevation needs are the mirror image of hydrography's: the highest point in an area, not the lowest, and the certainty that nothing above a stated height has been left out. ICAO's **Annex 15** (Aeronautical Information Services) and, since Amendment 40 in 2018, the **PANS-AIM (Doc 10066)** specify **electronic Terrain and Obstacle Data (eTOD)** in four coverage areas with numerical requirements that are among the few DEM specifications written directly into an international treaty instrument:

| Area | Coverage | Terrain post spacing | Terrain vertical accuracy (90 %) | Obstacle vertical accuracy | Obstacle horizontal accuracy |
|---|---|---|---|---|---|
| 1 | Entire State territory | 3″ (≈ 90 m) | 30 m | 30 m | 50 m |
| 2 | Terminal control area (≈ 45 km radius of the ARP) | 1″ (≈ 30 m) | 3 m | 3 m | 5 m |
| 3 | Aerodrome movement area | 0.6″ (≈ 20 m) | 0.5 m | 0.5 m | 0.5 m |
| 4 | CAT II/III precision approach area | 0.3″ (≈ 9 m) | 1 m | 1 m | 2.5 m |

(values per ICAO Annex 15 / PANS-AIM Doc 10066 Appendix 1; confirm against the current amendment before use). Each dataset also carries a **confidence level** (90 % for the accuracies above), an **integrity classification**—*routine* (10⁻³ probability of undetected corruption), *essential* (10⁻⁵), *critical* (10⁻⁸)—and a vertical reference of mean sea level, in practice **EGM96**, while GNSS altitude on board is ellipsoidal; the geoid undulation (up to ± 100 m globally) must be applied consistently, and the common error is to compare a WGS 84 ellipsoidal GPS altitude against an EGM96-referenced terrain cell. ICAO **Doc 9881** (*Guidelines for Electronic Terrain, Obstacle and Aerodrome Mapping Information*) gives the implementation guidance; **Annex 4** governs the aeronautical charts that present the same data.

The user requirements and processing standards come from RTCA and EUROCAE. **DO-276 / ED-98** (*User Requirements for Terrain and Obstacle Data*; DO-276C / ED-98C, 2015) define the terrain and obstacle data attributes, accuracies, and resolutions that databases must provide; **DO-200B / ED-76A** (*Standards for Processing Aeronautical Data*) treat every step of the data chain—origination, transmission, transformation, formatting, distribution—as a process that must preserve accuracy, resolution, integrity, traceability, timeliness, and completeness, with documented procedures and a Letter of Acceptance from the authority. The philosophy is that the data product's quality is a property of the *process*, not only of the end file, which is exactly the provenance argument of [Chapter 50](ch50-archiving-and-provenance.md) made mandatory.

**TAWS/EGPWS.** Terrain Awareness and Warning Systems compare the aircraft's GNSS/baro position with an onboard terrain database and alert on predicted collision; Honeywell's Enhanced Ground Proximity Warning System (1996) was the first widely fitted system with a terrain database and look-ahead logic, and TAWS became mandatory on turbine aircraft with six or more passenger seats in the US from March 2005 (14 CFR 91.223). The database is a coarse DEM (post spacings from 30″ to 15″ over most of the globe, finer near airports) in which each cell stores the *maximum* elevation within it plus a buffer, again the worst-case convention; it is updated on a cycle (typically each 28-day AIRAC cycle for obstacles, less often for terrain) and its quality is assessed against DO-200B rather than ASPRS statistics. **Minimum safe altitudes** (MSA, MORA, grid MORA) are published numbers derived from the highest terrain or obstacle in an area plus 1,000 ft (2,000 ft in mountainous terrain) rounded up; a DEM that misses a ridge by 50 m is irrelevant for MORA, while one that misses a 150 m tower is not.

**Obstacle surveys.** In the US, FAA **AC 150/5300-18** (*General Guidance and Specifications for Submission of Aeronautical Surveys to NGS*) specifies airport obstruction surveys—accuracy classes for runway ends, navigational aids, and obstacles penetrating defined surfaces—and **14 CFR Part 77** defines the **imaginary surfaces** (primary, approach, transitional at 7:1, horizontal at 150 ft above airport elevation, conical at 20:1) whose penetration by any object constitutes an obstruction requiring notice and evaluation. Part 77.9 also requires notice to the FAA for any construction over 200 ft AGL anywhere, or lower near airports (a 100:1 slope from the nearest runway within 20,000 ft for the longest runways). Obstacle data therefore come from a mix of surveyed points (lidar and photogrammetry around airports, with ground survey of critical obstacles), developer filings, and change detection; the data gap is always the new object—crane, turbine, mast—between survey and use, which is why **currency and change notification** are part of the specification and why obstacles have a mandatory **NOTAM** path for temporary structures.

Helicopter and low-level routes (HEMS, power-line patrol, military low-flying) are where this matters most, because the margin above wires and masts is tens of meters and wires are invisible to most DEM sources ([Chapter 33](ch33-wires-and-thin-structures.md)); DO-276 treats wires as obstacles only when their supporting structures are, and the practical defence is a dedicated wire-and-obstacle database plus onboard sensing.

## 62.3 Drones and UAS: 400 ft above what?

Small-UAS rules set altitude ceilings relative to the ground. US **14 CFR Part 107.51** limits operations to 400 ft (≈ 122 m) **above ground level (AGL)**, or within a 400 ft radius of a structure up to 400 ft above the structure's immediate uppermost limit; EASA's open category uses 120 m above the closest point of the Earth's surface, with similar structure exemptions. The rules do not say which surface "ground" is, and the answer changes the legality of a flight. A flight controller that estimates AGL from a barometric altitude relative to the take-off point assumes flat terrain; one that uses a stored DEM assumes the DEM's definition. Over a forest, a DTM-based geofence allows the aircraft to climb to 400 ft above the ground, 300 ft above the canopy—legal under a literal reading, but a DSM-based geofence would hold it to 400 ft above the trees, which is both safer and closer to what a manned pilot would judge. Over a ridge, a 30 m SRTM DSM with 10 m vertical error and 30 m posts under-reports a sharp crest by tens of meters, and a terrain-following mission flown at 100 m AGL from that DEM may be 70 m AGL at the crest—or, with a stale DEM, in the new transmission tower.

**Terrain following** in ArduPilot and PX4 uses SRTM-derived tiles by default (ArduPilot's terrain database at 100 m or 30 m spacing, PX4 similar) unless a rangefinder is fitted; mission planners offer DSM/DTM options with varying clarity about which is loaded. **Geofencing** and **UTM / U-space** services (the FAA's LAANC authorizations, EU U-space terrain services) express ceilings in AGL and depend on the service's own DEM, so a drone whose onboard DEM differs from the authority's can be compliant by one and in violation by the other; the only robust practice is to state the reference surface and its source in the operation's documentation. **BVLOS** (beyond visual line of sight) risk assessments under the JARUS SORA framework need a DSM with wires, masts, and tall structures to compute air-risk and ground-risk buffers—exactly the thin features a DEM product is least likely to contain—and operators increasingly fly their own corridor survey to produce them. **Obstacle detection** on board (stereo, lidar, radar) handles the unexpected object; stored obstacles handle the known one; neither alone is sufficient, and the stored data's epoch is the first question in an incident investigation.

> **Definitions that bite.** *AGL* has at least four operational meanings: (1) height above the take-off point (barometric, no terrain model), (2) height above a DTM (bare earth), (3) height above a DSM (top of canopy and buildings), (4) height above the nearest obstacle or structure (Part 107's structure exemption). A single flight plan can be compliant under one, non-compliant under another, and physically unsafe under a third. Document which one the flight controller, the mission planner, and the authorization service each use, and the DEM source and epoch behind each.

## 62.4 Ground vehicles: HD maps, grade, and localization

Road vehicles use elevation in three distinct ways. **HD maps** for driver assistance and automated driving (HERE HD Live Map, TomTom, Mobileye REM, and OEM-internal maps) store lane geometry as 3D polylines with centimeter-to-decimeter relative accuracy, plus **slope** (longitudinal grade) and **bank** (cross-slope, superelevation) per lane segment, because a controller that does not know the road is banked 6 % misreads lateral acceleration and a powertrain that does not know the grade mis-plans torque. These are not DEM rasters; they are vector attributes measured by survey vehicles with lidar and GNSS/INS and maintained by fleet-sourced change detection. Absolute accuracy matters less than relative accuracy along and across the lane, and the maps are specified under functional-safety frameworks (**ISO 26262** for the vehicle systems; **UL 4600** for autonomous-product safety cases, which explicitly treats map data as a safety-relevant input with required validation and update processes).

**Road grade for energy** is the simplest use and the one where public DEMs are good enough: eco-routing and predictive cruise control for heavy trucks use grade profiles from 10–30 m DEMs sampled along the road centerline, and a 1 m vertical error over a 100 m baseline is a 1 % grade error—tolerable for energy estimation, not for control. Grade from a DSM is wrong in tunnels, under tree canopy, and on bridges; from a DTM it is wrong wherever the road is on structure. [Chapter 63](ch63-buildings-cities-innerspace.md) treats multi-level roads; for vehicle maps the practical representation is the road network's own Z-profile, not a surface.

**Localization against lidar maps** ([Chapter 15](ch15-slam.md)) uses a prior point-cloud or feature map and matches live lidar scans to it (NDT, ICP, or learned descriptors) to obtain decimeter positioning when GNSS is blocked; elevation enters as the ground-plane and the vertical structure of curbs, walls, and poles. Maps go stale with **construction**—a lane shift, a new barrier, a resurfaced road 5 cm higher—and the system must detect disagreement between map and sensor and degrade gracefully, which is the same problem as obstacle-database currency in aviation with a faster clock.

## 62.5 Robots and off-road: the elevation map as a control input

Mobile robots on rough terrain plan over a **2.5D elevation map**: a robot-centric grid, typically 0.02–0.2 m cells over a few meters, each cell holding an elevation estimate and its variance, updated from depth cameras or lidar as the robot moves. The **GridMap** library (Fankhauser and Hutter 2016) and the `elevation_mapping` package in ROS are the common implementations; they fuse range measurements with the robot's pose uncertainty so that cells far from the robot, seen from a drifting pose, carry larger variance, and they derive **traversability** layers (slope, step height, roughness) that the planner thresholds. Where overhangs and multi-level structure matter, **OctoMap** (Hornung et al. 2013) stores occupancy in an octree so that a table top and the floor beneath it are both represented; the 2.5D assumption breaks exactly where it does for cities ([Chapter 35](ch35-voids-and-overhangs.md)). The probabilistic framing throughout is Thrun, Burgard, and Fox's (2005): every map cell is a belief, every plan is evaluated against that belief, and a cell's variance is as much an input as its mean. **Legged robots** add a footstep-planning layer that needs the elevation map to be accurate to a few centimeters within a stride, which drives mapping latency requirements of tens of milliseconds; a map that is accurate but 200 ms old is a map of where the ground *was* relative to a body that has since moved.

Off-planet, the elevation map is built in advance from orbit and the robot localizes against it. **Mars 2020's Terrain-Relative Navigation** used the Lander Vision System to match descent images against an onboard orthomosaic and DEM made from HiRISE stereo (Johnson et al. 2022; [Chapter 67](ch67-planetary-dems.md)), with hazard maps pre-computed from the DEM at ~1 m posting; the requirement was a map-relative position within 40 m, and the flight result was a few meters, which allowed Perseverance to land in Jezero Crater's hazardous terrain by diverting from mapped hazards. The DEM's role here is entirely as a navigation sensor: its horizontal registration to the orthomosaic, its vertical accuracy relative to the hazard scale (rocks and slopes of a meter or two), and the absence of unmapped hazards were the requirements, and were verified by comparison with independent HiRISE products and by Monte Carlo landing simulations. Rover traverse planning uses the same orbital DEMs at 1 m with the known vertical uncertainty (meters absolute, decimeters relative) and relies on onboard stereo for the last few meters.

## 62.6 Terrain-referenced navigation: the DEM as a sensor

**Terrain-referenced navigation (TRN)** estimates position by matching a measured terrain profile against a stored DEM. **TERCOM** (Terrain Contour Matching; Golden 1980) correlated a radar-altimeter-minus-barometric-altitude profile along a cruise missile's track against DEM strips to fix position when inertial drift had accumulated; modern formulations (SITAN, and particle-filter TRN) run the match continuously inside a Bayesian filter. The same idea underlies **bathymetric navigation for AUVs**, which match multibeam or single-beam depth profiles against a prior bathymetric grid to bound INS drift during long dives without surfacing for GNSS ([Chapter 14](ch14-positioning-beyond-gnss.md)).

In all of these the DEM is a sensor with an error budget: the match's horizontal accuracy is bounded by the DEM's horizontal registration and by the terrain's information content—flat or self-similar terrain gives ambiguous matches regardless of DEM quality—and its vertical noise and bias enter the likelihood directly. A TRN system flying over a 30 m DEM with 10 m vertical error in rough terrain can fix position to a few tens of meters; over a plain it cannot fix position at all, and over a DEM with an unmodeled datum offset it converges confidently to the wrong place. The design questions are the DEM's resolution relative to terrain correlation length, its vertical error model (bias, noise, correlation), its epoch (sand dunes and glaciers move), and the availability of a **terrain-informativeness map** so the navigator knows where fixes are trustworthy.

## 62.7 Liability and certification: who stands behind the data

Navigation products are certified. **Hydrographic offices** are the national authorities responsible for charts under SOLAS Chapter V, which obliges ships to carry up-to-date official charts; the office's survey specifications (S-44, national HSSD-like documents), its validation procedures, and its Notices to Mariners form the chain of custody, and a grounding on an uncharted shoal within a recently surveyed CATZOC A1 area is a different legal matter from one in a CATZOC D area. **Aeronautical Information Services (AIS/AIP providers)** certify terrain and obstacle data under Annex 15 and DO-200B; database suppliers (Jeppesen, Lufthansa Systems, Honeywell, Garmin) hold Letters of Acceptance from their authorities, and each 28-day AIRAC cycle is an audited release. HD-map and robot-map suppliers operate under product-safety frameworks (ISO 26262, UL 4600, and sector-specific regulation) rather than public certification, and the **safety case** must argue that map errors are bounded, detected, and tolerated.

Three principles recur. First, **lineage must be unbroken**: each transformation (datum, resampling, selection) is a documented process with its own quality check, which is DO-200B's core and what a general-purpose DEM pipeline almost never provides. Second, **uncertainty must be delivered to the decision**: CATZOC on the chart, confidence level in eTOD, the variance layer in the robot's map; a product whose uncertainty stays in a metadata file the user never opens has not communicated it. Third, **go/no-go decisions are probabilistic**: the under-keel budget of §62.1, the obstacle-clearance surface, and the landing-hazard map all ask for a probability of harm given the data's uncertainty, and a decision made on nominal values alone transfers risk silently to whoever is aboard.

## 62.8 Transient and new objects in navigation products

The objects that cause accidents are disproportionately the ones that were not there at the last survey. Charts carry **wrecks**, **obstructions**, **moored structures**, and, increasingly, **offshore wind farms**—each turbine a charted obstruction with a safety zone, each inter-array cable a seabed feature, each foundation a scour pit that changes local bathymetry—and the update cycle for these is driven by notifications from developers and port authorities rather than resurvey. Aviation obstacle databases carry **construction cranes** as temporary obstacles via NOTAM, permanent **masts and turbines** via developer filings and surveys, and depend on the filing being made. Drone and vehicle maps face the same classes at a faster clock. [Chapter 27](ch27-moving-and-transient-objects.md) treats transients at acquisition; for navigation products the questions are the update latency between the object's appearance and its presence in the product, the mechanism (regulatory filing, resurvey, crowd-sourced detection), and the product's explicit statement of currency, which for charts is the edition and the last Notice to Mariners applied, for aviation the AIRAC cycle, and for HD maps a version and a last-verified date per segment.

<!-- figure: Figure 62.2 — Timeline of currency mechanisms across domains: chart edition + Notices to Mariners, AIRAC 28-day cycle + NOTAM, HD-map segment versioning, robot map live update; annotated with typical latency from object appearance to product. -->

## Then & now

Charts began as **lead-line soundings and visual pilotage** ⟨H⟩, with depths measured one at a time and positions by bearings; the sparse soundings and the convention of charting the shoalest value date from this era and survive in ENC sounding selection. Echo sounders (1920s) and then **multibeam sonar** (commercial systems from the late 1970s; routine hydrographic use from the 1990s) ⟨H⟩ produced full-coverage bathymetry, and the **ENC/ECDIS** combination (S-57 Edition 3 in 1996; ECDIS performance standards from IMO in 1995 and carriage requirements phased in 2012–2018) ⟨H⟩ replaced paper as the legal chart. The **S-100** framework (2010) and its product specifications—S-101 ENC, S-102 bathymetric surface, S-104 water levels, S-111 currents—make the chart a layered, time-varying product in the 2020s, with S-102 Edition 3 (2024) the first gridded bathymetry with per-node uncertainty intended for the bridge.

Aviation went from **paper sectionals** and pilot judgment to the first **ground-proximity warning systems** (1970s, radar-altimeter-based, no database) and then to Honeywell's **EGPWS** (1996) with a worldwide terrain database and look-ahead alerting, which cut controlled-flight-into-terrain accidents sharply; ICAO's **eTOD** provisions (Annex 15 Amendment 33, 2004, with applicability dates through 2015) made terrain and obstacle datasets a State obligation with numerical requirements. Robotics moved from flat-world occupancy grids (1980s) to probabilistic 2.5D and 3D maps (OctoMap 2013; GridMap 2016), and planetary landing from ballistic targeting ellipses of hundreds of kilometers to **Mars 2020's TRN** (February 2021), the first use of an orbital DEM as a real-time landing sensor on another planet.

## Mathematics

**Under-keel clearance budget.** With charted depth $D_c$ (below chart datum), tide height $T$ above datum, static draft $d_s$, squat $s(v)$, heel allowance $h$, wave-motion allowance $w$, and a 95 % uncertainty allowance $U$,

$$\mathrm{UKC}_{\text{net}} = (D_c + T) - (d_s + s(v) + h + w) - U, \qquad U = k\sqrt{\sigma_D^2 + \sigma_T^2 + \sigma_s^2 + \sigma_d^2},$$

where $\sigma_D$ is the survey TVU at 1σ (S-44's TVU is at 95 %, so $\sigma_D = \mathrm{TVU}/1.96$ if Gaussian) and $k$ = 1.96 for 95 %. PIANC's WG 121 report (2014) recommends this probabilistic structure for channel design, with the alternative of a direct **probability of grounding**: if depth error is $\mathcal{N}(0, \sigma^2)$ and the nominal clearance is $c$, $P(\text{touch}) = \Phi(-c/\sigma)$; for $c$ = 0.85 m and $\sigma$ = 0.23 m (0.45 m at 95 %), $P \approx \Phi(-3.7) \approx 1 \times 10^{-4}$ per transit, before the probability that the bottom has changed since survey.

**Obstacle clearance surfaces.** Part 77's surfaces are planes and cones defined from the runway: an approach surface rising at slope $1{:}m$ (e.g., 50:1 for precision approaches) from the runway end over a trapezoid; transitional surfaces at 7:1 from the primary and approach surfaces up to the horizontal surface at 150 ft above airport elevation; a conical surface at 20:1 outward from the horizontal surface for 4,000 ft. An object at $(x, y, z)$ penetrates if $z > z_{\text{surf}}(x,y)$; with object height uncertainty $\sigma_z$ the penetration decision has a probability $\Phi((z - z_{\text{surf}})/\sigma_z)$, which is why obstacle surveys specify vertical accuracies (0.5–3 m) small compared with the surfaces' margins.

**Terrain-referenced navigation as matching.** Given a measured profile $m_i$ at along-track positions $t_i$ and a DEM $z(\cdot)$, TERCOM chooses the offset $\boldsymbol{\delta}$ minimizing $\sum_i \left(m_i - z(\mathbf{p}_i + \boldsymbol{\delta})\right)^2$ (mean-removed to cancel altimeter bias); a Bayesian TRN maintains $p(\mathbf{x}_k \mid m_{1:k}) \propto p(m_k \mid \mathbf{x}_k)\, p(\mathbf{x}_k \mid m_{1:k-1})$ with likelihood $p(m_k \mid \mathbf{x}_k) = \mathcal{N}(m_k; z(\mathbf{x}_k), \sigma_z^2 + \sigma_m^2)$, where $\sigma_z$ is the DEM's error and $\sigma_m$ the altimeter's. The posterior's horizontal spread is governed by the terrain's gradient: in the linearized case $\sigma_{xy} \approx \sqrt{\sigma_z^2 + \sigma_m^2} / |\nabla z|$, so a 10 m DEM error on a 10 % slope gives 100 m position uncertainty per measurement, reduced by $\sqrt{N}$ over $N$ independent samples along the track. DEM *bias* does not average out and must be estimated or removed.

## Validation & uncertainty

Navigation products are validated against a different question from general DEMs: not "how close is the surface to truth on average" but "what is the probability that the product under-reports a hazard." The statistics follow.

**Marine.** The hydrographic office's acceptance tests check TVU and THU against S-44 by crossline comparison and reference-surface analysis ([Chapter 20](ch20-sonar.md), [Chapter 53](ch53-accuracy-assessment.md)), but the chart-specific tests are (1) **feature detection**: did the survey's coverage and resolution meet the order's cubic-feature requirement everywhere, verified from sounding density and swath overlap, and was every detected feature carried into the product; (2) **shoal bias preservation**: for every node of a gridded product and every selected sounding, confirm the product value is no deeper than the shoalest source sounding in its footprint—an automated check that should fail on zero nodes; (3) **datum**: confirm the chart datum realization (tide gauge, zoning, or ellipsoid-to-datum separation model) and its uncertainty, which in zoned tidal reductions reaches 0.1–0.3 m and dominates TVU in shallow water; (4) **currency**: compare against the most recent condition survey and the shoaling rate. Report CATZOC (or S-101 quality of bathymetric data) per area with the survey date.

**Aviation.** Terrain datasets are tested against independent check points for the 90 % vertical accuracy per area, obstacle datasets against field survey for position and height, and both for **completeness** (every obstacle above the area's height threshold present) by comparing against a DSM or imagery of newer date; integrity is tested as a *process* (CRC on every transfer, documented transformation steps, DO-200B audit). Vertical reference checks—EGM96 versus ellipsoid versus local MSL—are mandatory and are where cross-border datasets most often fail.

**Drones, vehicles, robots.** Validate the reference surface against an independent DSM/DTM and report which surface the AGL is referenced to; test HD-map grade and bank against GNSS/INS drive-throughs; for robot elevation maps, compare mapped step heights and slopes with a ground-truth scan and track the variance layer's calibration (is the 1σ band actually containing 68 % of errors?). For TRN, validate the DEM's horizontal registration against orthoimagery, estimate the vertical bias and noise by profile comparison, and produce the terrain-informativeness map that bounds achievable fixes.

> **Try it.** Check shoal-bias preservation in an S-102/BAG grid against the source soundings with Python.
>
> ```python
> import h5py, numpy as np, laspy
> from scipy.stats import binned_statistic_2d
>
> # Source soundings (depth positive down, same datum as the product)
> src = laspy.read("soundings_mllw.laz")
> x, y, d = src.x, src.y, -src.z
>
> with h5py.File("channel_s102.h5") as f:
>     g = f["BathymetryCoverage/BathymetryCoverage.01/Group_001"]
>     depth = g["values"]["depth"][:]            # S-102: depth positive down
>     unc   = g["values"]["uncertainty"][:]
>     attrs = f["BathymetryCoverage/BathymetryCoverage.01"].attrs
>     x0, y0 = attrs["gridOriginLongitude"], attrs["gridOriginLatitude"]
>     dx, dy = attrs["gridSpacingLongitudinal"], attrs["gridSpacingLatitudinal"]
>
> ny, nx = depth.shape
> shoalest, *_ = binned_statistic_2d(x, y, d, statistic="min",
>                                    bins=[nx, ny],
>                                    range=[[x0, x0+nx*dx], [y0, y0+ny*dy]])
> shoalest = shoalest.T
> deeper_than_source = (depth - shoalest) > 0.0     # product deeper than shoalest sounding
> print("nodes violating shoal bias:", np.nansum(deeper_than_source),
>       "of", np.isfinite(shoalest).sum())
> print("median product uncertainty (m):", np.nanmedian(unc))
> ```
>
> Expected outcome: zero violating nodes for a navigation-grade product (check the group/attribute names against the S-102 edition in your file; the layout above follows Edition 2/3 conventions and the `s100py` library can read it directly). Any violations mark nodes where mean or smoothed gridding leaked into a product that should be shoal-biased.

> **Uncertainty budget.** Illustrative vertical terms for a harbor-approach UKC decision (95 % values).
>
> | Term | Magnitude | Source |
> |---|---|---|
> | Survey TVU, Special Order, 15 m | 0.28 m | S-44 formula |
> | Chart datum realization (tidal zoning) | 0.10–0.30 m | Gauge network, VDatum/VORF |
> | Water-level forecast (S-104) | 0.10–0.25 m | Model skill, surge |
> | Squat prediction | 0.2–0.4 m | Empirical formula vs hull |
> | Draft reading, density | 0.05–0.15 m | Loading survey |
> | Shoaling since survey | 0 → unbounded | Survey age × sedimentation rate |
>
> The last term is why currency, not TVU, is usually the controlling uncertainty in an active channel.

## Software

**Open source:** **OpenCPN** (chart plotter; reads S-57 ENCs and raster charts, useful for inspecting ENC content and CATZOC). **GDAL/OGR S-57 driver** (reads ENC objects and attributes into any GIS; `ogrinfo` lists DEPARE, SOUNDG, M_QUAL/CATZOC). **NOAA `s100py`** (Python; read/write S-102, S-104, S-111 HDF5 products). **OctoMap**, **GridMap**, **elevation_mapping** (ROS; robot 3D/2.5D mapping with uncertainty). **ArduPilot** and **PX4** (terrain-following and geofence code; inspect which terrain tiles are loaded). **MB-System** and **PDAL** for bathymetric and lidar processing upstream of products.

**Free but closed:** **NOAA ENC viewer / Chart Display Service**; **FAA Obstacle Data (DOF)** downloads; **ArduPilot Mission Planner** (terrain tile download).

**Commercial:** **ECDIS** systems (type-approved under IEC 61174; Kongsberg, Wärtsilä, Furuno, and others). **CARIS HIPS/SIPS and BASE Editor**, **QPS Qimera/Fledermaus** (survey-to-chart bathymetry, CUBE, shoal-biased gridding, BAG/S-102 export). **Jeppesen**, **Honeywell**, **Lufthansa Systems**, **Garmin** (certified terrain/obstacle databases). **HERE**, **TomTom**, **Mobileye** (HD maps). **Trimble/Topcon** machine-control terrain models for earthmoving (grade control; [Chapter 65](ch65-mining-landfills-earthworks.md)).

## Standards & guides

- **IHO S-44 Ed. 6.1.0 (2022)** *Standards for Hydrographic Surveys* — survey orders, TVU/THU, feature detection and search.
- **IHO S-57 Ed. 3.1** and **S-101** (ENC product specifications); **S-52** (presentation); **S-4** (chart specifications); **S-67 Ed. 1.0.0 (2020)** *Mariners' Guide to Accuracy of Depth Information in ENCs*.
- **IHO S-102 Ed. 3.0.0 (2024)** bathymetric surface; **S-104** water level information for surface navigation; **S-111** surface currents.
- **NOAA Hydrographic Surveys Specifications and Deliverables (HSSD, current edition)** and **Field Procedures Manual**; **USACE EM 1110-2-1003** *Hydrographic Surveying* (2013).
- **PIANC WG 121 (2014)** *Harbour Approach Channels Design Guidelines* — UKC methodology.
- **ICAO Annex 15** (AIS), **Annex 4** (charts), **Doc 10066 PANS-AIM** (eTOD areas and data quality), **Doc 9881** (eTOD guidelines).
- **RTCA DO-276C / EUROCAE ED-98C (2015)** (terrain and obstacle data user requirements); **DO-200B / ED-76A** (processing aeronautical data).
- **FAA AC 150/5300-18** (aeronautical surveys); **14 CFR Part 77** (obstruction standards); **14 CFR Part 107** (small UAS; §107.51 altitude).
- **ISO 26262** (road vehicle functional safety) and **UL 4600** (safety for autonomous products; map data as a safety input).

## Pitfalls

- **Mean-gridded bathymetry in a chart product** → general-purpose gridding averages across relief → enforce shoal-biased node selection and test every node against the shoalest source sounding.
- **UKC computed with charted depth but no uncertainty** → the chart looks exact → add the S-44 TVU or CATZOC allowance, the datum realization, and the forecast error; compute net clearance and probability of touch.
- **Chart datum confused with MSL or NAVD 88** → datums differ by 0.5–2 m in most ports → confirm the datum on the chart title block and transform with VDatum/VORF; never mix a topographic DEM and a chart without a separation model.
- **DTM-based AGL geofence over forest or city** → "ground" literally means bare earth → use a DSM (or DSM + obstacle buffer) for geofencing and terrain following; document which surface.
- **SRTM terrain tiles as the only terrain-following source** → 30–90 m posts and ~10 m errors miss ridgelines and towers → add a rangefinder, fly higher margins, or load a lidar DSM for the corridor.
- **Obstacle database missing new cranes, turbines, masts** → the object post-dates the survey and no filing was made → check NOTAMs, developer filings, and recent imagery; treat the database epoch as a hazard.
- **EGM96-referenced terrain compared with ellipsoidal GNSS altitude** → mixing $h$ and $H$ by up to ± 100 m → apply $h = H + N$ consistently; test with a known airport elevation.
- **HD map or lidar localization map not updated for construction** → lane shifts and barriers invalidate the prior → run map–sensor disagreement detection and degrade to safe behavior.
- **TRN over flat or self-similar terrain** → the match is ambiguous regardless of DEM quality → compute terrain informativeness in advance and do not accept fixes where it is low.
- **DEM datum offset in TRN or landing hazard maps** → bias does not average out → estimate and remove bias against independent data before flight.
- **Robot elevation-map variance that is not calibrated** → the planner trusts cells it should not → check the empirical coverage of the 1σ band against ground truth and inflate accordingly.
- **Treating survey TVU as the whole depth uncertainty in an active channel** → shoaling since survey can exceed TVU within weeks → require a survey-age limit in the UKC policy.

## Key takeaways

- Navigation products encode a worst-case philosophy—shoalest depth, highest obstacle, maximum cell elevation—and an explicit uncertainty; never substitute a general-purpose DEM.
- Chart depths are below a tidal datum (LAT/MLLW), not an orthometric or ellipsoidal one; every topographic–bathymetric comparison needs a separation model with its own uncertainty.
- Put the S-44 TVU (or CATZOC allowance) and the water-level forecast error into the UKC budget and compute a net clearance or a probability of touch; in active channels, survey age usually dominates.
- ICAO eTOD areas specify post spacing, 90 % vertical accuracy, and integrity class per area; DO-200B makes the processing chain, not only the file, the object of certification.
- "AGL" means different things to a barometer, a DTM, a DSM, and a structure rule; state the reference surface and its epoch in every drone operation.
- A DEM used for localization (HD map, robot map, TRN, planetary landing) is a sensor whose bias, noise, registration, and epoch form an error budget that the controller must know.
- Currency mechanisms—Notices to Mariners, AIRAC/NOTAM, map versioning, live robot updates—are part of the product's safety, and the new object is the usual cause of the accident.
- Uncertainty belongs in the go/no-go decision, not in a metadata file; deliver it to the bridge, the cockpit, or the planner.

## References

- Calder, B. R., and Wells, D. (2007). *CUBE User's Manual*, Version 1.13. Center for Coastal and Ocean Mapping, University of New Hampshire.
- Fankhauser, P., and Hutter, M. (2016). A universal grid map library: Implementation and use case for rough terrain navigation. In A. Koubaa (ed.), *Robot Operating System (ROS): The Complete Reference (Volume 1)*, Studies in Computational Intelligence 625, Springer, pp. 99–120.
- Golden, J. P. (1980). Terrain contour matching (TERCOM): A cruise missile guidance aid. *Proceedings of SPIE*, 238 (Image Processing for Missile Guidance):10–18.
- Hornung, A., Wurm, K. M., Bennewitz, M., Stachniss, C., and Burgard, W. (2013). OctoMap: An efficient probabilistic 3D mapping framework based on octrees. *Autonomous Robots*, 34(3):189–206.
- International Hydrographic Organization (2022). *IHO Standards for Hydrographic Surveys*, S-44 Edition 6.1.0. IHO, Monaco.
- International Hydrographic Organization (2020). *Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts (ENC)*, S-67 Edition 1.0.0. IHO, Monaco.
- International Hydrographic Organization (2024). *S-102 Bathymetric Surface Product Specification*, Edition 3.0.0. IHO, Monaco.
- International Civil Aviation Organization (2018). *Procedures for Air Navigation Services — Aeronautical Information Management (PANS-AIM)*, Doc 10066, First Edition. ICAO, Montréal.
- International Civil Aviation Organization (2010). *Guidelines for Electronic Terrain, Obstacle and Aerodrome Mapping Information*, Doc 9881, First Edition. ICAO, Montréal.
- Johnson, A. E., Aaron, S. B., Ansari, H., Bergh, C., Bourdu, H., Butler, J., Chang, J., Cheng, R., Cheng, Y., Clark, K., et al. (2022). Mars 2020 Lander Vision System flight performance. *AIAA SciTech 2022 Forum*, AIAA 2022-1214.
- PIANC (2014). *Harbour Approach Channels Design Guidelines*, MarCom Working Group 121 report. PIANC, Brussels.
- RTCA (2015). *Standards for Processing Aeronautical Data*, DO-200B. RTCA, Washington, DC.
- RTCA (2015). *User Requirements for Terrain and Obstacle Data*, DO-276C. RTCA, Washington, DC.
- Thrun, S., Burgard, W., and Fox, D. (2005). *Probabilistic Robotics*. MIT Press, Cambridge, MA.
- US Federal Aviation Administration (2009). *General Guidance and Specifications for Submission of Aeronautical Surveys to NGS: Field Data Collection and Geographic Information System (GIS) Standards*, AC 150/5300-18B, with Change 1 (2011); 18C was cancelled in 2016 and 18B remains in force.
- US Army Corps of Engineers (2013). *Hydrographic Surveying*, EM 1110-2-1003. USACE, Washington, DC.
- Bergman, N. (1999). *Recursive Bayesian Estimation: Navigation and Tracking Applications*. PhD thesis, Linköping Studies in Science and Technology, Dissertation No. 579, Linköping University.
- International Maritime Organization (2006). *Revised Performance Standards for Electronic Chart Display and Information Systems (ECDIS)*, Resolution MSC.232(82). IMO, London.
- US Code of Federal Regulations. 14 CFR Part 77, *Safe, Efficient Use, and Preservation of the Navigable Airspace*; 14 CFR Part 107, *Small Unmanned Aircraft Systems* (§107.51).

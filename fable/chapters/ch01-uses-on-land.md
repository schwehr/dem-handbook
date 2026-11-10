# Chapter 1 — The many uses of elevation data on land

> **Part I — Why elevation? Uses and users.** This chapter opens the book by cataloguing what people actually do with elevation data on land, and what each of those uses quietly assumes about the data.

**In this chapter.** Elevation data are consumed by far more people than ever look at a hillshade. After reading this chapter you will be able to recognise the two dozen or so families of land-side uses — from national topographic mapping and orthorectification through flood modelling, forestry, engineering, defence, navigation, and consumer apps — and, for each, name the five things the use silently assumes: which **surface** is represented (bare earth, canopy top, built roof, or "whatever reflected"), what **resolution** (nominal and effective) is needed, which **vertical datum** the numbers must be referenced to, how **current** the surface must be, and what **uncertainty** the use can tolerate and whether it needs an explicit uncertainty layer. The chapter closes with a use-versus-requirements matrix that later chapters refine into testable specifications ([Chapter 3](ch03-fitness-for-use.md)). Throughout, the emphasis is on the uses that break when one of those assumptions is wrong — and on the largest consumers of elevation data, which are often invisible.

## 1.1 Topographic mapping and cartography

The oldest and still the most visible use of elevation data is the topographic map: contours, spot heights, hill shading, and hypsometric tints that let a reader see a landscape in their head. A national mapping agency's elevation layer is also the skeleton on which everything else hangs — hydrography must flow downhill through it, roads must sit on it, orthoimagery (§1.2) must be draped over it. In the United States the US Geological Survey (USGS) has produced topographic quadrangles since its founding in 1879 and converted that heritage into the 7.5-minute series, the digitised-contour DEMs of the 1970s–1990s, and finally the lidar-based 3D Elevation Program (3DEP) that began after the 2012 National Enhanced Elevation Assessment (Dewberry 2012; Sugarbaker et al. 2014). Most other countries followed a similar arc — Ordnance Survey, IGN, swisstopo, Geoscience Australia, GSI Japan — and the modern pattern is a national **digital terrain model (DTM)** at 0.5–5 m, with contours now *derived* from it rather than the other way round.

What cartography silently assumes is instructive, because it differs from most other uses:

- **Surface type.** Contours represent **bare earth** — ground with vegetation and buildings removed — but a map also wants buildings, bridges, and dams drawn where they stand, so the cartographer needs *both* a DTM and knowledge of what was removed. A contour that dips to the river bed under a bridge deck is "correct" for a DTM and wrong for a road map.
- **Resolution.** Contour interval drives it. A 10 m interval on a 1:24,000 map needs vertical accuracy of about half the interval (the historical National Map Accuracy Standard required 90 % of tested points within one-half contour interval) and an effective resolution fine enough that contour crenulations are real terrain, not interpolation noise.
- **Datum.** National orthometric datum (NAVD 88 in the US today, with NAPGD2022 coming; see [Chapter 9](ch09-vertical-datums.md)). Contours labelled in feet on older sheets and metres on newer ones have cost more than one user a factor of 3.28.
- **Currency.** Maps age gracefully for mountains and badly for suburbs, open-pit mines, and river deltas.
- **Uncertainty.** Traditionally expressed once for the whole sheet, if at all. Modern practice — and this book — asks for it per cell or per tile.

<!-- figure: Figure 1.1 — Same 2 km × 2 km area shown four ways: 1950s contour quadrangle, 1990s 30 m DEM hillshade, 2015 lidar DTM hillshade at 1 m, and the DSM of the same lidar; annotate what each surface includes and omits. -->

## 1.2 Imagery production: the largest hidden consumer of DEMs

Ask most people who the biggest users of elevation data are and they will say hydrologists or civil engineers. By volume of DEM cells touched per day, the answer is almost certainly the pipelines that turn raw images into map-registered products. Every orthophoto, every Sentinel-2 or Landsat Level-2 scene, every Sentinel-1 radiometrically terrain-corrected (RTC) backscatter image, and every commercial ortho mosaic was made by projecting pixels onto an elevation model — once per output pixel, billions of times a day — and almost no end user of the imagery ever learns which DEM was used.

**Orthorectification** removes relief displacement: a feature at height $\Delta z$ above the reference surface is imaged at a horizontal offset of roughly $\Delta x \approx \Delta z \tan\theta$ from its true planimetric position, where $\theta$ is the viewing angle from nadir. For a 30° off-nadir satellite image and a 10 m DEM error, the horizontal error is about 5.8 m, which is larger than the pixel of most modern sensors. For aerial frame imagery the relevant quantity is the radial distance from the principal point divided by the flying height, and it is why "true orthophotos" need a **DSM** (so that building roofs land where they are) while classical orthophotos use a DTM (so that the ground is correct and buildings lean).

**SAR geocoding** uses the DEM to convert slant range and Doppler to ground coordinates and to identify layover and shadow; **radiometric terrain correction** goes further and uses local incidence angle and illuminated area derived from the DEM to normalise backscatter (Small 2011). Here the DEM's *derivatives* matter more than its absolute heights: a noisy DEM produces a speckled "terrain-corrected" image with striping that follows DEM artefacts. The Copernicus DEM, SRTM, and national lidar DTMs have each been used as the elevation reference for global products, and their differences show up as geolocation shifts of metres when products from different providers are overlaid.

The hidden assumptions:

- The DEM must be a **DTM for ground-level accuracy** and a DSM for rooftop-level accuracy; most global products are neither cleanly, being radar- or optical-stereo DSMs with partial canopy penetration ([Chapter 4](ch04-names-and-definitions.md), [Chapter 55](ch55-public-products.md)).
- Heights must be converted to **ellipsoidal** heights ($h = H + N$) before use with satellite sensor models that work in Earth-centred Cartesian coordinates; forgetting the geoid undulation $N$ (−100 m to +85 m globally) is a classical source of systematic ortho offsets on slopes.
- The DEM **epoch** should match the imagery in areas of change; a pre-eruption DEM under post-eruption imagery misplaces the new crater rim by $\Delta z \tan\theta$.
- Resolution should be comparable to or finer than the imagery's ground sample distance; using a 30 m DEM for 30 cm imagery leaves residual relief displacement at every break of slope.

> **Rule of thumb.** Horizontal error induced by DEM error in an orthoimage is $\Delta x \approx \Delta z \tan\theta$ (satellite, $\theta$ = off-nadir angle) or $\Delta x \approx \Delta z \cdot r / H_f$ (frame camera, $r$ = radial distance in the image plane projected to ground, $H_f$ = flying height above ground). Valid for small angles and single-valued terrain; it does not describe building lean in a classical ortho, which is a surface-definition issue, not a DEM-error issue.

## 1.3 Hydrology and hydraulics

Water is the use that most severely punishes a wrong surface. **Watershed delineation** and **flow routing** (D8, D∞, multiple-flow-direction algorithms; [Chapter 61](ch61-hydrology.md)) assume water flows across a *bare-earth, hydrologically connected* surface. A DSM routes the flood over the forest canopy and dams every stream at every bridge; even a good DTM must be **hydro-enforced** or **hydro-conditioned** so that culverts and bridges do not act as walls ([Chapter 34](ch34-water-in-dems.md)). The requirement that dominates hydrology is therefore not absolute vertical accuracy but **connectivity**: a 0.5 m error at a random hillslope cell changes nothing, at a drainage divide it moves a catchment boundary, and at a road crossing it creates a 100-ha phantom lake.

**Flood inundation** mapping and insurance rating depend on the DTM in two ways: as the geometry of the hydraulic model (channel and floodplain cross-sections or 2D mesh elevations) and as the surface against which the computed water-surface elevation is compared to draw the inundation polygon. In the United States, Federal Emergency Management Agency (FEMA) Flood Insurance Rate Maps under the National Flood Insurance Program (NFIP) set the Base Flood Elevation and therefore premiums and building requirements; FEMA's elevation guidance ties the required DEM quality to USGS Lidar Base Specification quality levels and to ASPRS accuracy classes (FEMA 2022). The sensitivity is simple to state: on a floodplain with slope 1:1,000, a 0.1 m vertical error moves the mapped flood boundary by 100 m. **Stormwater** design and **dam-break** analysis follow the same logic at street and valley scale, with the added need for currency — new fill, culverts, and subdivisions change the answer.

Hydrology's silent assumptions are a DTM (never a DSM) with known hydro-treatment, an effective resolution fine enough to resolve channels, levees, and road embankments (usually 1–5 m), a consistent orthometric datum (water flows according to geopotential, not ellipsoidal height), currency relative to the most recent earthworks, and an uncertainty layer that can be propagated through the model (Wechsler 2007). The datum point matters more than it looks: the ellipsoid–geoid separation varies by tens of centimetres over tens of kilometres in mountainous areas, so a river modelled on ellipsoidal heights can appear to flow uphill.

> **Worked example.** A floodplain has a mean ground slope of $\beta$ = 0.0008 (0.8 m per km). The DTM's vertical uncertainty is RMSE$_z$ = 0.10 m (95 % ≈ 0.196 m under a normal assumption). The horizontal uncertainty of the inundation boundary caused by the DTM alone is
> $$\Delta x_{95} = \frac{\Delta z_{95}}{\tan\beta} = \frac{0.196}{0.0008} \approx 245\ \text{m}.$$
> That is the width of the band within which the "100-year" line cannot be placed from the terrain alone, before any model or hydrologic uncertainty is added. Doubling point density does not help; halving RMSE$_z$ does.

## 1.4 Coastal risk: sea-level rise, surge, and tsunami

Coastal risk assessment is the use that most insistently requires **seamless topobathymetry** — a single surface across the shoreline with land and seabed on one datum ([Chapter 2](ch02-uses-bathymetry.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)). Sea-level-rise (SLR) exposure maps, in their simplest "bathtub" form, count the land cells below a chosen water level that are hydrologically connected to the sea. Their output is exquisitely sensitive to DEM vertical error because coastal plains are flat: Gesch (2018) showed that with SRTM-class data (RMSE$_z$ of several metres) the population exposed to 1 m of SLR is uncertain by factors, and that the minimum SLR increment a DEM can *resolve* is about twice its 95 % linear error (LE95) — roughly 0.3–0.4 m for lidar DEMs, several metres for SRTM. Kulp and Strauss (2019) found that correcting SRTM's canopy and building bias roughly tripled global estimates of population on land below projected high-tide lines — an entire policy conversation that hinged on the difference between a DSM and a DTM.

**Storm-surge** (e.g. ADCIRC) and **tsunami** (e.g. MOST, GeoClaw) models need the same seamless surface as their computational domain, with resolution of tens of metres offshore grading to metres at the coast, and they need the vertical datum to be *tidal* for the forcing and *orthometric or ellipsoidal* for the land — reconciled through a datum-transformation model such as NOAA's VDatum in the United States ([Chapter 9](ch09-vertical-datums.md)). The surface must be current with respect to dunes, nourishment, and seawalls, and must preserve the crest heights of thin features (levees, dune ridges) that a coarse grid erases ([Chapter 44](ch44-resolution-and-sampling.md)).

Assumptions: DTM on land (levee crests preserved as breaklines) merged with a bathymetric surface; decimetre vertical accuracy; a tidal-to-orthometric transformation with its own uncertainty; currency against the last storm; explicit uncertainty so that exposure can be mapped as a probability rather than a line.

## 1.5 Geomorphology and Earth-surface processes

For the Earth-surface scientist the DEM *is* the data. Slope, aspect, curvature, drainage area, channel steepness, local relief, and roughness are computed directly from the grid and interpreted as records of tectonics, climate, and erosion (Wilson and Gallant 2000; Hengl and Reuter 2009). High-resolution topography transformed the field: at 1 m, landslide scarps, fluvial terraces, fault scarps, and periglacial patterned ground become visible that were invisible at 30 m (Tarolli 2014; Passalacqua et al. 2015). Glaciologists difference DEMs across years for mass balance; permafrost scientists watch thermokarst subsidence; volcanologists compute erupted volumes and lava-flow paths; tectonic geomorphologists measure fault-scarp offsets of a few decimetres.

Each sub-use has its own dominant requirement. Landslide inventories need **effective resolution** fine enough to show the hummocky texture of deposits (a few metres), and a DTM clean of vegetation — which is why lidar, not photogrammetry, revolutionised landslide mapping in forested terrain. Erosion and glacier studies difference two epochs, so **co-registration** and the *precision* of the difference matter more than absolute accuracy ([Chapter 41](ch41-change-detection.md)): a 1 m absolute bias common to both epochs cancels, while a 0.3 m relative tilt does not. River science needs channel bathymetry that topographic lidar does not provide (water absorbs near-infrared), so the "DTM" has a flat, false surface at the water level unless bathymetric lidar or sonar fills it ([Chapter 19](ch19-bathymetric-lidar.md)). Derivatives amplify noise: each gradient component from a central difference has error $\sigma_z \sqrt{2}/(2d)$ for cell size $d$, so a 0.15 m noise level on a 1 m grid gives a slope noise of order 5–10° on flat ground (depending on the kernel) — and curvature is worse ([Chapter 3](ch03-fitness-for-use.md) §Mathematics).

Silent assumptions: DTM; resolution set by the smallest landform of interest; relative accuracy and co-registration for change; epoch known to the day for fast processes; an uncertainty model that includes spatial correlation, because terrain derivatives depend on neighbouring cells' errors jointly, not independently.

## 1.6 Geology and geophysics

Geologists use DEMs to map structure (bedding traces intersecting topography give strike and dip — the "V-rule"), to compute **gravity terrain corrections**, to characterise **seismic site effects**, and to plan exploration. The gravimetric terrain correction removes the attraction of topography above and below the station; it requires a DEM extending to a radius of about 167 km (Hayford zone O) and is highly sensitive to the DEM within a few hundred metres of the station, where a 1 m error on a steep slope changes the correction by of order 0.1 mGal (approximate; depends on density and geometry). Topographic slope is also a widely used proxy for the shear-wave velocity $V_{S30}$ in seismic-hazard mapping (Wald and Allen 2007), and here the DEM's *resolution* is part of the method: the calibration was done at 30″ (about 900 m) and does not transfer to finer grids without recalibration.

Assumptions: DTM (gravity cares about buildings only at the microgal level); resolution matched to the calibration; orthometric heights (gravity corrections are referenced to the geoid); staleness tolerable except in mining districts.

## 1.7 Forestry and ecology

Forestry is the use that needs *two* surfaces. The **canopy height model (CHM)** is the difference between a DSM of the canopy top and a DTM of the ground beneath it: CHM = DSM − DTM. Every error in either propagates into tree height and, through allometric equations, into **above-ground biomass and carbon**. NASA's GEDI lidar on the International Space Station (launched December 2018) measures waveform-derived canopy height and relative-height metrics in ~25 m footprints for gridded biomass products (Dubayah et al. 2020); its ground-finding depends on the waveform's last mode, and its validation on airborne lidar DTMs and field plots ([Chapter 52](ch52-ground-truth.md)). Wildfire behaviour models (e.g. FARSITE/FlamMap) take slope and aspect from a DTM and fuel heights from a CHM; **snow depth** is measured operationally by differencing a snow-on lidar DSM against a snow-off DTM, as pioneered by the Airborne Snow Observatory with a reported depth uncertainty of about 8 cm at 3 m resolution (Painter et al. 2016). Habitat and species-distribution models consume elevation, slope, aspect, and topographic wetness as covariates, typically at 30–90 m.

Assumptions: *both* DSM and DTM from the same epoch and sensor so that their errors are correlated and cancel in the difference; resolution finer than crown size (≤ 1 m) for individual-tree work and 10–30 m for stand-level work; leaf-on versus leaf-off acquisition stated ([Chapter 36](ch36-seasonal-variability.md)); a datum only loosely needed for CHM (differences are datum-free) but essential for snow-water-equivalent volumes integrated over a basin.

<!-- figure: Figure 1.2 — Cross-section through a forested slope showing DSM, DTM, and CHM, with the lidar return distribution, GEDI footprint waveform, and the location where a DTM error becomes a biomass error. -->

## 1.8 Agriculture

Agricultural uses of elevation are low-relief and high-precision. **Subsurface drainage (tile) design** needs grades of 0.1–0.5 % held over hundreds of metres; **land levelling** for surface irrigation targets residual relief of a few centimetres over a whole field; both are routinely done today with RTK-GNSS on the machine rather than from a DEM, but the planning and the earthwork estimates use one. **Erosion** modelling with RUSLE uses the slope-length and steepness factor $LS$, which is computed from slope and upslope contributing area; it is notoriously sensitive to resolution because flow-path length and slope both change with cell size (Zhang and Montgomery 1994). Precision agriculture consumes topographic wetness and relative elevation as management-zone covariates and uses them to explain yield-map variability.

Assumptions: DTM at a resolution of 1–5 m with *relative* vertical accuracy of a few centimetres within a field (absolute datum almost irrelevant); leaf-off or bare-soil acquisition (a lidar return from a maize canopy in August is 2–3 m above the ground); currency relative to tillage and levelling; a slope algorithm stated alongside the result, because RUSLE's $LS$ values depend on it.

## 1.9 Urban planning and engineering

Engineering is where the use list gets long, and where the DSM/DTM distinction is renegotiated case by case:

- **Cut-and-fill and site design** need a DTM of the existing ground with centimetre-to-decimetre accuracy over the site, usually on a *project* datum tied to one or two benchmarks ([Chapter 3](ch03-fitness-for-use.md) §3.4). Volume error is dominated by *bias*, not noise: a 2 cm systematic offset over a 10 ha site is 2,000 m³.
- **Viewshed and line of sight** need a DSM — the viewer cannot see through buildings or trees — with *transient* obstructions (parked trucks, cranes) removed ([Chapter 27](ch27-moving-and-transient-objects.md)). Long-distance visibility also needs Earth curvature and refraction corrections ($\approx 0.87\, d^2 / (2R)$ for distance $d$ and Earth radius $R$), which a planar GIS forgets.
- **Rooftop solar**, **shadow**, and **daylight** studies need a DSM fine enough to resolve roof planes, dormers, and chimneys (≤ 0.5 m) plus tree shadows across the day and year.
- **Wind and CFD** modelling of urban canyons needs building-resolving DSMs (1 m or better); mesoscale wind-resource work needs a DTM at 10–100 m plus a roughness-length layer derived from the DSM.
- **Noise** mapping under the EU Environmental Noise Directive and **RF propagation** planning under ITU-R P.1812 (point-to-area, 30 MHz–6 GHz) and P.452 (interference) take terrain profiles from a DTM and clutter heights from a DSM-minus-DTM layer; P.1812 allows clutter heights per terrain-profile point.
- **Utility corridors, road and rail design** need DTMs with breaklines along crests and toes so that profiles and cross-sections are faithful; design practice specifies accuracy on hard surfaces separately from vegetated areas, which is why ASPRS reports **non-vegetated vertical accuracy (NVA)** and **vegetated vertical accuracy (VVA)** separately.
- **Building-height regulation** needs the height of the building above *ground* at a defined point — a DSM − DTM question with legal consequences.
- **Digital twins and BIM** integrate DTM, DSM, point cloud, and building models and expose every datum and epoch inconsistency between them ([Chapter 63](ch63-buildings-cities-innerspace.md)).

Assumptions vary, but one is constant: engineering wants to know the *height of things above the ground* (nDSM = DSM − DTM), which means that both surfaces must be defined consistently and that the definition of "ground" at building footprints — where lidar sees roof, not floor — must be stated ([Chapter 32](ch32-dsm-to-dtm.md)).

## 1.10 Infrastructure monitoring

Monitoring reverses the question: not *what is the elevation* but *how has it changed*. **Subsidence** from groundwater withdrawal, mining, or hydrocarbon extraction is measured by InSAR at millimetres per year over hundreds of kilometres ([Chapter 21](ch21-radar-sar-insar.md)), by repeat levelling and GNSS at points, and by repeat lidar where the signal is decimetres. **Dams and levees** need crest elevations to centimetres (freeboard is a regulated quantity) and repeat surveys to detect settlement. **Mines** survey stockpiles, pits, and tailings facilities weekly or monthly with drone photogrammetry or lidar, reconciling volumes against production records ([Chapter 65](ch65-mining-landfills-earthworks.md)); **landfills** are paid by airspace consumed, measured by differencing against permitted final contours; **construction progress** is tracked by comparing as-built to design surfaces.

The controlling requirement is **repeatability** and **co-registration** between epochs: a 3 cm precision survey whose absolute datum is off by 20 cm is far more useful than the reverse, provided the datum error is constant. The trap is that it is not always constant — a new GNSS base station, geoid model, or processing version introduces a step that masquerades as a settlement event ([Chapter 50](ch50-archiving-and-provenance.md)).

## 1.11 Disaster response and risk

In the hours after an earthquake, landslide, flood, eruption, or wildfire, elevation data are used in three ways. **Pre-event** DEMs feed hazard models (landslide susceptibility from slope and lithology; lava-flow paths from steepest descent; avalanche terrain from slope and aspect; post-fire debris-flow probability from burned-area slope and rainfall). **Co-event** measurements — InSAR interferograms, pixel-offset tracking, repeat lidar — quantify the deformation itself: the 2016 Kaikōura earthquake slipped up to roughly 10 m on individual ruptures and uplifted stretches of coast by several metres (Clark et al. 2017), and repeat lidar and photogrammetric differencing resolved fault-zone deformation at the metre scale. **Post-event** DSMs from satellites or drones support damage assessment by comparing building heights before and after.

The silent assumption that bites hardest is **currency and the datum's own stability**: a large earthquake moves the ground, and therefore the control network, by metres; the pre-event DEM and the post-event survey are in different physical frames even if both say "NAD83(2011)" ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md)). Response work also tolerates and must *communicate* much higher uncertainty than mapping work — a rough DSM within hours beats a precise DTM in weeks — but the rough product must carry its uncertainty so that it is retired when the better one arrives.

> **Case file.** After the 2014 Oso landslide in Washington State, pre-event lidar (2003 and 2013) and post-event lidar were differenced to compute the mobilised volume (about 8 million m³, approximate) and the runout surface (Iverson et al. 2015). Earlier lidar had revealed the long history of prehistoric landslides on the same slope — visible under the forest canopy only in a lidar DTM — which became central to the post-event review of what was knowable beforehand. The lesson for this chapter: the DTM existed; the use case (hazard communication) had not been connected to it.

## 1.12 Climate and cryosphere

The cryosphere is measured in elevation change. Ice-sheet mass balance in Greenland and Antarctica is derived from repeat satellite altimetry (ICESat, ICESat-2, CryoSat-2), from DEM differencing (ASTER, WorldView stereo, TanDEM-X), and from gravimetry (GRACE/GRACE-FO), with the altimetric and DEM methods converting volume to mass via assumptions about firn density ([Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)). Hugonnet et al. (2021) quantified global mountain-glacier mass balance from two decades of ASTER DEMs — possible only because systematic errors can be modelled and random errors averaged over many scenes. **Snow water equivalent** from lidar snow depth (§1.7) and modelled density feeds water-supply forecasts. The **sea-level budget** closes only if land-ice volume change, thermal expansion, and land-water storage are each known to a fraction of a millimetre per year of sea-level equivalent.

Assumptions: the surface is the *snow or ice surface* — a DSM in lidar terms, and a radar-penetrated surface in Ku- or X-band altimetry (penetration of metres into dry firn is a known bias); tens of metres suffice for ice sheets but glacier tongues need better; the datum must be ellipsoidal with frame and epoch specified, because vertical land motion (glacial isostatic adjustment of millimetres per year) is the same order as the signal; and — above all — uncertainty must be reported with its spatial correlation structure, because an elevation-change map integrated over a million square kilometres has an uncertainty that depends almost entirely on the correlated, not the random, component ([Chapter 41](ch41-change-detection.md), [Chapter 53](ch53-accuracy-assessment.md)).

## 1.13 Weather, climate, and environmental modelling

Numerical weather and climate models need **model orography**: the DEM averaged and filtered to the model grid of 1–100 km, plus sub-grid statistics (standard deviation of elevation, ridge orientation and anisotropy) that parameterise gravity-wave and orographic form drag. The averaging is deliberately lossy; the hidden assumption is a void-free, artefact-free DTM, because a 1 km cell that averages in a 3,000 m void-fill spike acquires a spurious mountain. **Statistical downscaling** uses lapse rates against elevation; **cold-air pooling** and frost-risk studies need valley shape at 10–100 m. **Digital soil mapping** and **species-distribution models** use elevation derivatives (slope, curvature, wetness index, multi-resolution valley-bottom flatness) as covariates in machine-learning models. These covariate uses are forgiving of absolute accuracy but unforgiving of artefacts — a striping pattern in a DEM becomes a striping pattern in the soil map, which the model will happily "learn".

## 1.14 Defence, intelligence, and aerospace

Military mapping produced many of the elevation formats and standards still in use. **DTED** (Digital Terrain Elevation Data) is the NGA/NATO format with Level 0 (30″ ≈ 900 m), Level 1 (3″ ≈ 90 m), and Level 2 (1″ ≈ 30 m) post spacings; SRTM was flown in 2000 to produce DTED-2 globally between 60° N and 56° S (Farr et al. 2007). Uses include **line of sight** for weapons, sensors, and communications; **mission planning** and route finding; **terrain-referenced navigation** (TERCOM, TERPROM), in which an aircraft or missile correlates its radar-altimeter profile against a stored DEM ([Chapter 14](ch14-positioning-beyond-gnss.md)); **obstacle databases** such as NGA's **Digital Vertical Obstruction File (DVOF)**, which catalogues towers, masts, and wires that no gridded DEM resolves ([Chapter 33](ch33-wires-and-thin-structures.md)); and DSM-based 3D site models and built-area change detection.

Assumptions: for terrain-referenced navigation, a *reflective-surface* DEM consistent with what the radar altimeter sees (neither purely DTM nor DSM); for obstacle work, **completeness** of thin tall objects is the controlling metric, addressed by a vector database rather than a grid; datum WGS 84 (G-realization stated) with EGM96 or EGM2008 orthometric heights and the DTED specification's accuracy classes; and classification restrictions that mean the best data are often not the data a civilian user can obtain ([Chapter 69](ch69-security-sovereignty-privacy-ethics.md)).

## 1.15 Navigation and mobility

**Terrain awareness and warning systems (TAWS)** in aircraft compare GNSS position and altitude against an onboard terrain and obstacle database and alert when the projected flight path intersects it; ICAO Annex 15 and PANS-AIM define terrain and obstacle data areas whose resolution and accuracy requirements tighten from en-route (Area 1) to aerodrome (Areas 2–4) ([Chapter 62](ch62-navigation-and-charting.md)). The database must be *conservative* — no terrain modelled lower than it is — the opposite of the unbiased estimate a scientist wants. **Drone operations** need height above ground level (AGL) for regulatory ceilings (120 m in many jurisdictions) and terrain-following flight; most consumer drones compute AGL from barometric altitude relative to take-off plus, increasingly, an onboard DEM. **Autonomous vehicles and robots** use elevation in high-definition maps for road grade, traversability, and localisation against a prior terrain map ([Chapter 15](ch15-slam.md)). **Hiking and cycling apps** compute elevation gain by sampling a DEM along a GNSS track; the result depends on the DEM's resolution and noise far more than users suspect, with cumulative gain inflating as noise is summed along the track.

Assumptions: conservative (never-below-truth) surfaces for safety uses versus unbiased surfaces for everything else; a surface definition that includes obstacles for aviation but excludes them for ground robotics; currency, because cranes and new towers appear; and, for consumer apps, a tolerance for error that is wide but should be made visible.

## 1.16 Energy and communications

Wind-resource assessment uses DTMs for flow modelling and DSMs for roughness; a 10 m error in a ridge-top elevation changes modelled wind speed by a few per cent and energy yield by about three times that, since power scales with speed cubed. Solar siting uses slope, aspect, and horizon shading from a DSM. **Hydropower** and **reservoir capacity curves** (stage–area–volume) integrate a DEM — and a bathymetric survey of the inundated part ([Chapter 2](ch02-uses-bathymetry.md) §2.6) — over elevation bands, so a DEM bias becomes a stored-volume bias at every stage. **Transmission routing** needs DTMs for tower spotting and conductor sag and DSMs for vegetation clearance (the 2003 North American blackout began with conductors sagging into trees, which is why vegetation-management lidar is now routine). **Telecom planning** was covered in §1.9; 5G millimetre-wave planning pushes the clutter requirement to building-resolving DSMs.

## 1.17 Archaeology and cultural heritage

Lidar's ability to map the ground beneath forest canopy made archaeology one of the most visible beneficiaries of high-resolution DTMs. The 2009 lidar survey of Caracol, Belize, revealed causeways, terraces, and settlement extent across 200 km² of rainforest in days of flying (Chase et al. 2011), and subsequent surveys in the Maya lowlands, Angkor, and Amazonia reshaped population estimates. The analytical tools are DTM visualisations — **local relief models** (DTM minus its low-pass-filtered version), sky-view factor, openness, and multi-directional hillshades — that reveal decimetre-scale earthworks ([Chapter 57](ch57-visualizing-dems.md)). Heritage documentation also uses terrestrial lidar and photogrammetry at millimetre resolution.

Assumptions: a DTM produced with a ground filter tuned to *keep* subtle anthropogenic relief (standard filters remove low walls as "vegetation" or smooth terraces as noise; [Chapter 30](ch30-point-cloud-classification.md)); point density sufficient for ground returns under dense canopy (≥ 10–20 pulses/m²); leaf-off season where it exists; no particular datum or absolute accuracy, but strong internal consistency.

## 1.18 Legal and cadastral

Elevation enters law through **flood zones** (§1.3) that set insurance obligations; through **zoning height limits** and view-protection ordinances; through **airspace** (obstacle limitation surfaces around airports, drone ceilings); through **boundaries** defined by watersheds, ridgelines, or the mean high-water line; and through mineral and property volumes in royalty disputes ([Chapter 68](ch68-legal-issues.md)). Each of these makes a DEM a piece of evidence, which means its surface definition, datum, epoch, and uncertainty become matters for cross-examination. A particularly treacherous area is the shoreline boundary, where the legal line is defined on a tidal datum (mean high water, mean higher high water) and the DEM is on an orthometric one ([Chapter 9](ch09-vertical-datums.md)).

## 1.19 Consumer, media, and entertainment

The largest audiences for elevation data never see a number. Web maps shade terrain from global DEMs; flight simulators and games stream real-world DEMs with photogrammetric DSMs over cities; augmented-reality apps label peaks; fitness watches report elevation gain; makers 3D-print terrain and tactile maps. These uses need **plausibility** — no spikes, no steps at tile boundaries, no flat-topped mountains from void-fill — more than accuracy, tolerate a mixed DSM/DTM surface, and are the uses for which smoothing, super-resolution, and ML enhancement are most appropriate ([Chapter 45](ch45-super-resolution.md)) — with the caveat that an enhanced DEM that looks real can leak back into analytical uses that need it to *be* real.

## 1.20 Beyond Earth

Planetary DEMs of the Moon, Mars, Mercury, Venus, asteroids, and comets are made by laser altimetry (MOLA, LOLA), stereo photogrammetry (HRSC, HiRISE, LROC), and radar (Magellan), and are used for landing-site selection, rover traverse planning, geological mapping, and gravity modelling. The distinguishing feature is the near-total absence of ground truth and the need to define the datum (an areoid or selenoid, a reference sphere or ellipsoid) from the same mission data; [Chapter 67](ch67-planetary-dems.md) treats this in full.

## 1.21 What each use assumes — a matrix

Table 1.1 condenses the chapter. The columns are the five silent assumptions plus two more that distinguish professional from casual use: *completeness* (are voids, thin objects, or water surfaces acceptable?) and *uncertainty layer* (does the use need a per-cell or per-region uncertainty estimate to do its job honestly?). Entries are typical, not universal; [Chapter 3](ch03-fitness-for-use.md) shows how to turn a row into a testable requirement.

| Use | Surface | Resolution (typical) | Vertical accuracy (typical) | Datum | Currency | Completeness / uncertainty layer |
|---|---|---|---|---|---|---|
| Topographic mapping (§1.1) | DTM + knowledge of removed objects | 1–10 m | ½ contour interval (90–95 %) | national orthometric | years–decades | no voids; sheet-level accuracy statement |
| Orthorectification / SAR RTC (§1.2) | DTM (ground) or DSM (true ortho) | ≤ image GSD | $\Delta z \tan\theta$ < pixel | ellipsoidal for sensor models | match imagery in changing areas | voids filled; artefacts matter via derivatives |
| Hydrology / flood (§1.3) | hydro-enforced DTM | 1–5 m | RMSE$_z$ ≤ 0.1–0.2 m; connectivity dominant | orthometric | since last earthworks | culverts/bridges treated; uncertainty propagated |
| Coastal risk / SLR (§1.4) | seamless topobathy DTM | 1–10 m | LE95 ≤ 0.2–0.3 m | tidal↔orthometric transformation | since last storm/nourishment | levee/dune crests preserved; probabilistic exposure |
| Geomorphology (§1.5) | DTM | 0.5–5 m | relative; co-registration for change | any, stated | epoch to the day for change | spatially correlated error model |
| Geology / geophysics (§1.6) | DTM | method-calibrated (30″ for $V_{S30}$) | metres | orthometric | decades OK | voids fatal in gravity corrections |
| Forestry / ecology (§1.7) | DSM *and* DTM, same epoch | ≤ 1 m (trees), 10–30 m (stands) | CHM error ≈ √(σ²$_{DSM}$+σ²$_{DTM}$) when uncorrelated | not needed for CHM | leaf-on/off stated | ground returns under canopy |
| Agriculture (§1.8) | bare-soil DTM | 1–5 m | relative cm within field | project | since tillage | slope algorithm stated |
| Urban / engineering (§1.9) | DTM + DSM (nDSM) | 0.25–1 m | cm–dm; bias controls volumes | project or national | months | transient objects removed |
| Infrastructure monitoring (§1.10) | DTM/DSM as appropriate | 0.1–1 m | repeatability cm; InSAR mm/yr | stable, consistent across epochs | per survey | datum-change log |
| Disaster response (§1.11) | whatever is fastest, labelled | 1–30 m | known, communicated | pre/post frames may differ | hours | uncertainty travels with product |
| Cryosphere (§1.12) | snow/ice surface (penetration stated) | 10–100 m | correlated-error budget | ellipsoidal, frame + epoch | per season | firn/penetration corrections |
| Weather / soil covariates (§1.13) | DTM, filtered | 10 m–100 km | artefact-free more than accurate | any | decades | no voids or stripes |
| Defence / aerospace (§1.14) | reflective surface; obstacles as vectors | DTED-0/1/2 | class-specified | WGS 84 / EGM | obstacle currency critical | completeness of thin tall objects |
| Navigation (§1.15) | conservative (TAWS) or unbiased | ICAO areas 1–4 | never-below-truth for safety | ellipsoidal (GNSS) | obstacles: continuous | obstacle completeness |
| Energy / comms (§1.16) | DTM + clutter (DSM−DTM) | 1–30 m | metres (wind), dm (hydro volumes) | orthometric | years | reservoir bathymetry included |
| Archaeology (§1.17) | DTM with gentle filter | ≤ 0.5 m | relative dm | any | leaf-off | ground density under canopy |
| Legal / cadastral (§1.18) | as defined in statute | per statute | defensible, documented | statutory (often tidal) | date-stamped | chain of custody |
| Consumer / media (§1.19) | mixed OK | 1–30 m | plausibility | any | years | no visual artefacts |

<!-- figure: Figure 1.3 — Two-axis diagram placing the uses of Table 1.1 by required resolution (x, log scale 0.1 m–100 km) and required vertical accuracy (y, log scale 1 mm–10 m), with symbols for DTM/DSM/both and shading for "conservative" vs "unbiased" surfaces. -->

> **Definitions that bite.** "Elevation" in a use specification may mean any of: orthometric height $H$ above a geoid model, ellipsoidal height $h$, height above a tidal datum, height above local ground (AGL, nDSM), or height above a project benchmark. A requirement that says "1 m DEM, 15 cm accuracy" without naming the surface and the datum is not a requirement; it is a hope. [Chapter 4](ch04-names-and-definitions.md) makes the vocabulary precise.

## Then & now

The uses in this chapter did not appear with the data; the data appeared and the uses followed, each generation of product unlocking consumers the previous one could not serve.

- **Contour maps as the elevation product (1879–1970s).** ⟨H⟩ The USGS was founded in 1879 and its topographic quadrangles — ultimately the 7.5-minute series at 1:24,000 — were the elevation database of the United States for a century. Elevation was something a human *read* from a sheet; the uses were cartographic, engineering-by-hand, and military.
- **Digitised contours and the first grids (1970s–1990s).** USGS DEMs at 30 m (later 10 m) were interpolated from those same sheets, inheriting their contour-interval accuracy and "terracing" artefacts. Hydrology, geomorphometry, and viewshed analysis became *computations*; DTED levels defined the military equivalent.
- **SRTM (2000).** ⟨H⟩ The Shuttle Radar Topography Mission flew in February 2000 and produced the first near-global, consistent DEM at 1″ (released at 3″ outside the US until 2014–2015). Overnight every country had a 30–90 m DSM, and global hydrology, SLR exposure, orthorectification, and model orography were rebuilt on it (Farr et al. 2007). Its C-band surface — part canopy, part ground, with voids on steep slopes and water — made the DSM/DTM distinction a global problem.
- **National lidar (2000s–present).** Lidar DTMs at 1 m with decimetre accuracy — first in the Netherlands (AHN), Denmark, Switzerland, and England, then the US 3DEP program from 2012 — moved flood mapping, archaeology, landslide inventory, and engineering from "possible" to "routine". The National Enhanced Elevation Assessment estimated benefits of at least US$690 million per year for Quality Level 2 national coverage (Dewberry 2012); the 3D Nation study extended the inventory to topobathymetry (Dewberry 2022).
- **Global DSMs and ML-corrected global DTMs (2010s–2020s).** TanDEM-X (12–90 m), ALOS World 3D (30 m), and the Copernicus DEM (30/90 m) improved on SRTM; FABDEM (Hawker et al. 2022) and similar products use machine learning to remove forest and building heights from the Copernicus DEM, producing a global pseudo-DTM whose residual errors are themselves a research topic ([Chapter 43](ch43-traditional-vs-ml.md), [Chapter 55](ch55-public-products.md)).

The shift in a sentence: from *a map you read* to *a model you compute with* — and therefore from accuracy stated once per sheet to uncertainty that must travel with every cell.

## Validation & uncertainty

Each use in this chapter fails in its own way when the data are wrong, so validation has to be use-specific. Three questions organise it: *which error matters* for this use, *how it propagates* into the use's output, and *how to test* for it before the output is trusted.

**Which error matters.** Random per-cell noise ($\sigma_z$) controls derivatives (slope, curvature) and local features; **bias** controls volumes, flood extents on flat terrain, and SLR exposure; **spatially correlated error** (tilts, strip offsets, long-wavelength undulations from geoid or trajectory errors) controls catchment-scale integrals and change detection; **surface-definition error** (DSM used as DTM, canopy or building height left in) is the largest error of all for hydrology, SLR, and CHM uses and is not captured by any RMSE computed at open-ground checkpoints; and **completeness error** (voids, missing thin objects, flattened water) controls aviation safety, gravity corrections, and orography. The usual checkpoint-based accuracy statement (NVA/VVA per ASPRS 2023, [Chapter 53](ch53-accuracy-assessment.md)) measures only the first two of these, at points chosen to be easy to measure.

**How it propagates.** Table 1.2 gives first-order propagation rules; [Chapter 5](ch05-error-and-uncertainty.md) derives them and [Appendix B](../appendices/appendix-b-math-reference.md) collects them.

| Use output | Driving error | First-order propagation |
|---|---|---|
| Ortho position on slope / off-nadir | $\Delta z$ | $\Delta x = \Delta z \tan\theta$ |
| Flood or SLR boundary position | $\Delta z$ (incl. bias) | $\Delta x = \Delta z / \tan\beta$ |
| Slope from finite differences | $\sigma_z$, cell size $d$ | $\sigma_{\tan\beta} \approx \sigma_z \sqrt{2}/(2d)$ for central differences, uncorrelated noise |
| Volume over area $A$ | bias $b$, noise $\sigma_z$, $n$ cells | $\sigma_V \approx \sqrt{(bA)^2 + A^2\sigma_z^2/n}$; bias term dominates for large $n$ |
| CHM = DSM − DTM | $\sigma_{DSM}, \sigma_{DTM}$, correlation $\rho$ | $\sigma_{CHM}^2 = \sigma_{DSM}^2 + \sigma_{DTM}^2 - 2\rho\,\sigma_{DSM}\sigma_{DTM}$ |
| Elevation change between epochs | co-registration, correlated error | $\sigma_{\Delta z}^2 = \sigma_1^2 + \sigma_2^2 + \sigma_{reg}^2$; minimum detectable change ≈ 1.96 $\sigma_{\Delta z}$ |

**How to test.** For a given use, validate the quantity the use consumes, not just the elevation:

1. *Surface definition.* Overlay the DEM on recent imagery and profile across forests, buildings, bridges, and water. A DTM should pass under tree crowns and bridge decks; a DSM should not. Compute the DEM minus a trusted DTM in forested and built areas separately; a mean difference that scales with canopy height tells you the "DTM" is not one.
2. *Checkpoints by land cover.* Survey or acquire independent checkpoints (GNSS, higher-accuracy lidar) stratified by the land-cover classes the use cares about; report NVA and VVA separately with sample sizes, and report mean error (bias) alongside RMSE. For flood and SLR uses, insist on checkpoints on the floodplain itself, not only on roads.
3. *Hydrologic connectivity.* Compute flow accumulation on the DTM and look for spurious ponding at roads and spurious channels along strip boundaries; compare delineated watersheds with mapped stream networks.
4. *Derivative sanity.* Compute slope on areas known to be flat (airfields, water); the standard deviation of slope there is a direct estimate of the noise-induced slope error.
5. *Epoch and datum audit.* Confirm the vertical datum, geoid model, and reference-frame realization in the metadata, and *test* them against a benchmark; confirm the acquisition dates against the dates of known changes (construction, storms, eruptions).
6. *Uncertainty layer.* If the product provides one (e.g. per-cell height-error map for TanDEM-X, or a lidar density/intensity raster that proxies it), check it against the checkpoint residuals; if it does not, build one from density, slope, and land cover ([Chapter 53](ch53-accuracy-assessment.md)).

> **Try it.** Measure the noise-induced slope error of any DTM by sampling slope on a surface you know is flat. With GDAL and Python:
>
> ```bash
> # Compute slope in degrees from a 1 m DTM (metres, projected CRS)
> gdaldem slope dtm_1m.tif slope_deg.tif -compute_edges
> # Crop to a polygon of a known-flat airfield apron and get statistics
> gdalwarp -cutline apron.gpkg -crop_to_cutline slope_deg.tif slope_apron.tif
> gdalinfo -stats slope_apron.tif | grep -E "MEAN|STDDEV"
> ```
>
> Expected outcome: for a lidar DTM with $\sigma_z$ ≈ 0.05 m on a 1 m grid, the mean slope on the apron is of order 1–3° and the standard deviation similar — not the ~0° a naïve user expects. Repeat after resampling to 5 m (`gdalwarp -tr 5 5 -r average`) and the slope noise drops sharply (by up to a factor of ~25 for uncorrelated noise: √25 from averaging and 5 from the longer baseline), which is the resolution/derivative trade-off of [Chapter 3](ch03-fitness-for-use.md) in one experiment.

**What to report.** For any product you hand to a user of one of these use families: the surface definition in words, the nominal and effective resolution, the vertical datum (geoid model and frame realization with epoch), the acquisition date range, accuracy by land-cover class with bias and RMSE and sample size, treatment of water and voids, and either an uncertainty layer or an honest statement of why there is none.

## Software

**Open source:** GDAL (`gdaldem`, `gdalwarp`) for slope/aspect/hillshade, reprojection, and resampling — caveat: `gdaldem slope` uses a Horn kernel and reports noise as slope on fine grids. PDAL for point-cloud filtering and DTM/DSM rasterisation. WhiteboxTools and SAGA GIS for hydrological conditioning, flow routing, and geomorphometric derivatives; TauDEM for parallel D∞ routing on large DTMs; GRASS GIS (`r.watershed`, `r.sun`, `r.viewshed`) for watersheds, solar, and visibility; QGIS as the desktop front end. xdem (Python) for DEM differencing, co-registration, and spatially correlated uncertainty. HEC-RAS (free, US Army Corps of Engineers; source not open) for hydraulics; GeoClaw and ADCIRC for tsunami and surge (ADCIRC requires registration); Relief Visualization Toolbox (RVT) for archaeological visualisations. **Free but closed:** Google Earth Engine (hosted DEMs and terrain functions; terms restrict commercial use). **Commercial:** Esri ArcGIS Pro (Spatial Analyst, 3D Analyst); Hexagon ERDAS IMAGINE and Trimble Inpho for orthorectification; Bentley OpenRoads for engineering design; WindSim and Meteodyn for CFD wind; Forsk Atoll and Siradel for RF planning. Each commercial tool embeds default DEM handling (resampling method, nodata treatment, datum assumptions) that you should inspect rather than trust. See [Chapter 71](ch71-software-landscape.md) and [Appendix F](../appendices/appendix-f-software-index.md).

## Standards & guides

- **USGS 3D Elevation Program (3DEP)** program documents and the **USGS Lidar Base Specification** (current online edition, 2024 revision; earlier v2.1 2020) — quality levels QL0–QL3, point density, NVA/VVA, hydro-flattening, deliverables.
- **National Enhanced Elevation Assessment** (Dewberry 2012, for USGS) — the use/benefit inventory (602 mission-critical activities across 34 federal agencies, all 50 states; approximate counts) that justified 3DEP.
- **3D Nation Elevation Requirements and Benefits Study** (Dewberry for NOAA and USGS, 2022) — extends the inventory to topobathymetry and inland bathymetry.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)** — NVA, VVA, checkpoint design, accuracy classes.
- **FEMA Guidelines and Standards for Flood Risk Analysis and Mapping — Elevation Guidance** (November 2022 revision; continuously maintained) — ties flood-study DEM quality to USGS QLs.
- **ITU-R P.1812** (point-to-area terrestrial propagation, 30 MHz–6 GHz) and **ITU-R P.452** (interference evaluation) — terrain-profile and clutter inputs.
- **ICAO Annex 15 / PANS-AIM (Doc 10066)** — terrain and obstacle data areas 1–4 (detail in [Chapter 62](ch62-navigation-and-charting.md)).
- **MIL-PRF-89020B** — DTED performance specification (levels, accuracies, datum).
- **ISO 19157** — data-quality elements used to express any of the above ([Chapter 3](ch03-fitness-for-use.md)).

## Pitfalls

- **Using a DSM where a DTM is required.** Happens because the catalog said "DEM" and the hillshade looked fine. Flood water flows over canopy; SLR exposure is underestimated by factors. Detect by profiling across forests and bridges; avoid by naming the surface in the requirement.
- **Mixing vertical datums across inputs.** A lidar DTM on NAVD 88, a bathymetric grid on MLLW, and a design surface on an old local datum, merged without transformation. Steps of 0.5–2 m appear at the seams. Detect with cross-profiles at every dataset boundary; avoid with a datum-transformation log.
- **Assuming a "30 m" product resolves 30 m features.** Post spacing is not effective resolution; SRTM's effective resolution is closer to 60–90 m, and resampled products are coarser still. Detect by looking for features of known size; avoid by using the smallest-feature rule of [Chapter 3](ch03-fitness-for-use.md).
- **Treating an elevation value as timeless.** The ground moved (earthquake, subsidence), the surface changed (mining, construction), or the datum was redefined. Detect by checking acquisition dates against event and construction records; avoid by storing epoch with every product.
- **Skipping the uncertainty layer because "this use doesn't need it."** Consumer and visualisation uses genuinely do not; everything else does, and the product will be reused. Avoid by shipping at least a land-cover-stratified accuracy table.
- **Validating only where it is easy.** NVA on roads is reported; the floodplain, the forest, and the levee crest are never checked. Detect by reading the checkpoint map; avoid by stratifying checkpoints by the land cover the use cares about.
- **Computing derivatives on a grid finer than the data support.** Slope noise of 10°+ on flat ground, curvature that is pure noise. Detect with the flat-area test above; avoid by matching cell size to point density and noise.
- **Forgetting the geoid in orthorectification.** Sensor models need $h$; the DEM gives $H$; the 20–50 m difference in many regions produces systematic horizontal offsets on slopes. Detect with checkpoints on slopes facing opposite directions; avoid by converting explicitly.
- **Letting hydro-flattened or void-filled areas pose as measured terrain.** Flat lakes and interpolated voids are the right answer for a map and the wrong one for a gravity correction or a reservoir volume. Detect from the void/flatten masks (if shipped); avoid by demanding them.
- **Treating a safety-of-life conservative surface as a scientific estimate, or vice versa.** TAWS and chart surfaces are biased on purpose. Detect by reading the specification; avoid by matching the surface's bias philosophy to the use.
- **Summing noisy elevation differences along a track.** Hiking-app "elevation gain" inflates with DEM noise; the same effect inflates channel-length and $LS$-factor computations. Detect by varying the DEM; avoid by smoothing with a stated filter.
- **Believing that a global ML-corrected DTM is a lidar DTM.** Residual errors of metres remain under dense canopy and in cities, and they are spatially structured. Detect by comparing with any available lidar; avoid by using the product's own uncertainty estimates.

## Key takeaways

- Name the use before choosing data; the same landscape needs different surfaces, resolutions, datums, and currencies for different consumers.
- Every use implies a surface definition (DTM, DSM, both, reflective, or conservative), a nominal and effective resolution, a vertical datum, a required currency, and a tolerable uncertainty — make all five explicit.
- The biggest consumers of DEMs are invisible: orthorectification, SAR geocoding, and model orography touch more cells per day than all human analysts combined, and their errors propagate into products that never mention a DEM.
- Water-related uses (hydrology, flood, SLR) are the least tolerant of surface-definition and datum errors because flat terrain converts small vertical errors into large horizontal ones: $\Delta x = \Delta z / \tan\beta$.
- Derivative uses (slope, curvature, CHM, change) are controlled by noise, co-registration, and spatial correlation of error rather than by absolute accuracy.
- Volume and exposure uses are controlled by bias, which no amount of point density reduces and which standard checkpoint statistics may not reveal.
- Safety-of-life uses want conservative surfaces; science wants unbiased ones — different products from the same measurements.
- The use-versus-requirements matrix (Table 1.1) is a starting point; [Chapter 3](ch03-fitness-for-use.md) turns a row into a testable requirement.

## References

- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0. American Society for Photogrammetry and Remote Sensing.
- Chase, A. F., Chase, D. Z., Weishampel, J. F., Drake, J. B., Shrestha, R. L., Slatton, K. C., Awe, J. J., Carter, W. E. (2011). Airborne LiDAR, archaeology, and the ancient Maya landscape at Caracol, Belize. *Journal of Archaeological Science* 38(2):387–398.
- Clark, K. J., Nissen, E. K., Howarth, J. D., et al. (2017). Highly variable coastal deformation in the 2016 Mw 7.8 Kaikōura earthquake reflects rupture complexity along a transpressional plate boundary. *Earth and Planetary Science Letters* 474:334–344.
- Dewberry (2012). *National Enhanced Elevation Assessment — Final Report*. Prepared for the U.S. Geological Survey. Fairfax, VA: Dewberry.
- Dewberry (2022). *3D Nation Elevation Requirements and Benefits Study — Final Report*. Prepared for NOAA and USGS. Fairfax, VA: Dewberry.
- Dubayah, R., Blair, J. B., Goetz, S., et al. (2020). The Global Ecosystem Dynamics Investigation: High-resolution laser ranging of the Earth's forests and topography. *Science of Remote Sensing* 1:100002.
- Farr, T. G., Rosen, P. A., Caro, E., et al. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics* 45(2):RG2004.
- FEMA (2022). *Guidelines and Standards for Flood Risk Analysis and Mapping: Elevation Guidance* (November 2022). Federal Emergency Management Agency.
- Gesch, D. B. (2018). Best practices for elevation-based assessments of sea-level rise and coastal flooding exposure. *Frontiers in Earth Science* 6:230.
- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters* 17(2):024016.
- Hengl, T., Reuter, H. I. (eds.) (2009). *Geomorphometry: Concepts, Software, Applications*. Developments in Soil Science 33. Amsterdam: Elsevier.
- Hugonnet, R., McNabb, R., Berthier, E., et al. (2021). Accelerated global glacier mass loss in the early twenty-first century. *Nature* 592:726–731.
- Iverson, R. M., George, D. L., Allstadt, K., et al. (2015). Landslide mobility and hazards: implications of the 2014 Oso disaster. *Earth and Planetary Science Letters* 412:197–208. doi:10.1016/j.epsl.2014.12.020
- Kulp, S. A., Strauss, B. H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications* 10:4844.
- Maune, D. F., Nayegandhi, A. (eds.) (2018). *Digital Elevation Model Technologies and Applications: The DEM Users Manual*, 3rd ed. Bethesda, MD: ASPRS.
- Painter, T. H., Berisford, D. F., Boardman, J. W., et al. (2016). The Airborne Snow Observatory: Fusion of scanning lidar, imaging spectrometer, and physically-based modeling for mapping snow water equivalent and snow albedo. *Remote Sensing of Environment* 184:139–152.
- Passalacqua, P., Belmont, P., Staley, D. M., et al. (2015). Analyzing high resolution topography for advancing the understanding of mass and energy transfer through landscapes: A review. *Earth-Science Reviews* 148:174–193.
- Small, D. (2011). Flattening gamma: Radiometric terrain correction for SAR imagery. *IEEE Transactions on Geoscience and Remote Sensing* 49(8):3081–3093.
- Sugarbaker, L. J., Constance, E. W., Heidemann, H. K., Jason, A. L., Lukas, V., Saghy, D. L., Stoker, J. M. (2014). *The 3D Elevation Program initiative — A call for action*. U.S. Geological Survey Circular 1399.
- Tarolli, P. (2014). High-resolution topography for understanding Earth surface processes: Opportunities and challenges. *Geomorphology* 216:295–312.
- Wald, D. J., Allen, T. I. (2007). Topographic slope as a proxy for seismic site conditions and amplification. *Bulletin of the Seismological Society of America* 97(5):1379–1395.
- Wechsler, S. P. (2007). Uncertainties associated with digital elevation models for hydrologic applications: a review. *Hydrology and Earth System Sciences* 11:1481–1500.
- Wilson, J. P., Gallant, J. C. (eds.) (2000). *Terrain Analysis: Principles and Applications*. New York: Wiley.
- Zhang, W., Montgomery, D. R. (1994). Digital elevation model grid size, landscape representation, and hydrologic simulations. *Water Resources Research* 30(4):1019–1028.

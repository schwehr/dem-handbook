# Chapter 34 — Water in DEMs: surfaces, shorelines, hydro-flattening / -enforcement / -conditioning

> **Part VII — From sensor data to products.** The chapter on the one surface a terrain model cannot measure well, cannot leave out, and cannot represent without a datum and a date: water, and the line where it meets the land.

**In this chapter.** Water defeats topographic sensors, moves between surveys, and has legal definitions that no sensor observes directly. You will be able to explain why lidar returns from water are sparse and biased; what the USGS means by hydro-flattening, hydro-enforcement, and hydro-conditioning and why they are three different operations; how to decide what is water when the level changes daily; and what "shoreline" means in the instantaneous, tidal, and legal senses—MHW, MLLW, LAT, *Borax* (1935), UNCLOS Article 5, NOAA practice from Shalowitz to CUSP—including the slope amplification $\Delta x = \Delta z / \tan\beta$ that turns a 10 cm datum error into a 20 m shoreline shift on a flat beach. You will apply priority-flood filling, breaching, D8 and D∞ routing, and HAND to a lidar DTM, distinguish real sinks from artefacts, stitch topography to bathymetry across the white ribbon, and report what every step did to the elevations.

## 34.1 Water in topographic lidar, and three operations that are not the same

A near-infrared laser pulse that reaches a water surface mostly leaves the survey. Water absorbs strongly at 1064 nm and 1550 nm; what is not absorbed is reflected specularly, and a specular reflection returns to the receiver only when the surface is perpendicular to the beam—at nadir on a calm surface. Off-nadir, over calm water, the pulse glances away and the receiver records nothing; over rippled water, the random facets send occasional returns from near-nadir; over turbid water a weak diffuse return from suspended sediment is sometimes detected. The practical outcome is a point cloud with **voids** over most water bodies, a thin strip of returns under the flight line, and a scatter of low points from sub-surface backscatter or from the trough of waves. Where returns do exist they are biased: the few off-nadir returns come from wave facets, typically slightly below the mean surface, and sub-surface returns are below it by the uncorrected slant range through water. Photogrammetric DSMs fail differently—water has no stable texture, so matching produces noise or nothing—and InSAR decorrelates over water within the time between passes ([Chapter 35](ch35-voids-and-overhangs.md) treats voids generically).

A gridded DTM made from such data without intervention shows lakes as pitted, tilted, or spiky surfaces and rivers as chains of pits separated by ridges of interpolated bank. Since the 2000s the US lidar community has standardised both the remedy and the vocabulary, because three different interventions were being called by one name.

**Hydro-flattening** is a cartographic operation on the DEM only. Lakes and ponds above an area threshold are made flat at a single elevation at or just below the surrounding ground; wide rivers are made flat across their width and **monotonic** along their length (never flowing uphill); the results are enforced by 3D **breaklines** digitised along banks, with the water-side elevations set by the lowest reliable ground returns adjacent to the shore. The USGS Lidar Base Specification (LBS) requires hydro-flattening of water bodies of 2 acres (about 0.8 ha) or more and of rivers 100 ft (about 30 m) or wider in nominal width, and specifies that the water surface shall not be above the adjacent ground. The purpose is a clean DEM for display and for most analysis; no claim is made that the flat surface is the water elevation on a particular date, and the point cloud is not changed. Hydro-flattening does nothing about culverts, bridges, or flow connectivity; a hydro-flattened lake remains a sink.

**Hydro-enforcement** modifies elevations to make water flow where it does in reality: cutting a DEM through a road embankment where a culvert or bridge carries the stream underneath, lowering a channel bed so that the stream path is continuous downhill, removing a dam from the DEM where the analysis needs the pre-dam flow path. It is an edit to the terrain, made with knowledge of structures that the sensor could not see through, and it produces a DEM that is deliberately *not* the measured surface at those locations. The LBS describes hydro-enforcement as an optional, buyer-specified product distinct from the base bare-earth DEM. The edited cells should be recorded in a mask.

**Hydro-conditioning** is the algorithmic preparation of a DEM for flow routing: filling depressions, breaching barriers, resolving flat areas so that every cell has a downslope neighbour. It is what GIS "fill sinks" tools do (§34.7). It is applied by the analyst, not the data producer, and its result is a modelling surface that should never replace the DEM in the archive.

The distinctions matter because each operation changes elevations in a different place for a different purpose, and because a user who receives a "hydro-corrected" DEM without knowing which was done cannot judge it. A flood model needs enforcement at culverts; a volume calculation needs none of the three; a watershed delineation needs conditioning; a hillshade needs flattening. Flattening a river to a *horizontal* plane instead of a monotonic sloped surface is a classic mistake: a 50 km reach with 0.2 m km⁻¹ of water-surface slope falls 10 m, and a horizontal plane will stand 10 m above the water at the downstream end or 10 m below it at the upstream end.

> **Definitions that bite.** *Hydro-flattening*, *hydro-enforcement*, and *hydro-conditioning* were used interchangeably in vendor specifications before the USGS LBS (first edition 2012) fixed the meanings above. Non-US specifications and older papers still vary. A deliverable described as "hydrologically corrected" may mean any of the three, and only the first leaves the elevations of the land untouched. Ask which cells were changed, by how much, and whether the unmodified DEM is available.

<!-- figure: Figure 34.1 — A river reach shown in four panels: raw gridded lidar (pits and ridges over water), hydro-flattened (flat across, monotonic along, breaklines drawn), hydro-enforced (road embankment cut at the culvert), hydro-conditioned (depressions filled; the change raster shown). -->

## 34.2 Variable water: what is water, and when?

A DEM assigns one elevation to a cell, but water bodies have levels that vary by hours (tides), days (floods), seasons (reservoirs, snowmelt), and years (drought, regulation). The water surface captured at acquisition is the "ground" of that day; its elevation is a real measurement of nothing permanent.

**Reservoirs** are the clearest case. A storage reservoir may be drawn down tens of metres between full pool and the end of the dry season. A lidar survey flown at drawdown captures the exposed bed—valuable bathymetry, in effect—but a DEM that hydro-flattens at that level and labels the result "terrain" misrepresents the reservoir to any user who expects full pool, and a DEM that flattens to full pool from a photogrammetric survey discards real measurements of the bed. The honest product records the water-surface elevation and date at which flattening was applied, flattens at that elevation, and carries the exposed-bed measurements in the point cloud. Capacity analysis then uses the exposed bed together with bathymetry of the still-submerged part.

**Ephemeral and intermittent streams** are dry at acquisition in arid climates; they are terrain, and the channel geometry is a legitimate and valuable part of the DTM. **Floods at acquisition** are the opposite problem: a survey flown after a storm captures a water surface metres above the floodplain, and the DEM over the inundated area is the flood, not the ground. **Tidal flats** cycle between exposed and submerged twice daily; coastal lidar programs specify acquisition within a window around low tide (NOAA coastal mapping typically requires flights within a tolerance of predicted low water) and record the predicted and observed tide for each flight line, because the "shoreline" captured is wherever the water was at that minute. **Braided and migrating rivers** change their channel pattern between floods; a DEM of a braidplain is a snapshot of one configuration, and the thalweg position in next year's survey will differ by channel widths.

Deciding which cells are water, and what kind, is a classification problem that lidar alone solves poorly. Intensity (water is dark at 1064 nm), return density (voids), and local flatness help, and the LBS requires the producer to digitise water-body breaklines from the data and imagery. For the temporal regime of a water body, the **JRC Global Surface Water** dataset (Pekel et al., 2016) is the standard reference: from the Landsat archive since 1984 it provides, at 30 m, the occurrence (fraction of observations in which a pixel was water), seasonality, recurrence, and change class of every pixel. A pixel with 100 % occurrence is a permanent lake; one with 30 % is a seasonal floodplain, a reservoir margin, or a tidal flat. Using GSW to decide whether a lidar void is permanent water (flatten), seasonal water (flatten at the acquisition-date level and say so), or a flood (do not flatten; flag) is a defensible, reproducible procedure where the water body spans more than a few Landsat pixels.

> **Try it.** Summarise Global Surface Water occurrence over a lidar project footprint to decide which voids are permanent water. Expected outcome: an occurrence histogram; voids above ~90 % occurrence are flattening candidates, 10–90 % seasonal, < 10 % floods or non-water voids to investigate.
>
> ```python
> import ee
> ee.Initialize()
> aoi = ee.Geometry.Rectangle([-122.60, 38.00, -122.40, 38.15])
> gsw = ee.Image("JRC/GSW1_4/GlobalSurfaceWater").select("occurrence")
> hist = gsw.reduceRegion(ee.Reducer.fixedHistogram(0, 101, 10),
>                         aoi, scale=30, maxPixels=1e9)
> print(hist.get("occurrence").getInfo())
> # Export a mask of >=90 % occurrence for use as a flattening candidate layer
> task = ee.batch.Export.image.toDrive(gsw.gte(90).clip(aoi),
>        description="gsw_permanent", scale=30, region=aoi)
> task.start()
> ```
>
> Replace the dataset ID with the current GSW version if a newer one is published.

## 34.3 What is a shoreline?

Ask three people for the shoreline of a beach and you will receive three lines tens of metres apart, all correct. The difficulty is not measurement but definition, and the definitions are physical, statistical, and legal in turn.

### 34.3.1 Lines you can see

The **instantaneous waterline** is where the water meets the land at the moment of observation. It is what an image or a lidar strip records; it moves with the tide, with wave run-up, and with the wind, and on a beach of 1:50 slope it migrates 50 m horizontally for every metre of water level. The **wet/dry line** is the boundary between sand darkened by the last high water and dry sand above it; it approximates the previous high-tide run-up limit and is the line most often digitised from aerial photographs as a "high-water line" proxy. The **vegetation line**, **dune toe**, **berm crest**, and **cliff base** are morphological proxies that move more slowly and are used in erosion studies precisely because they are less sensitive to the tide at the moment of the photograph. Boak and Turner (2005) catalogue more than a dozen such indicators and the disagreements among them; the largest systematic differences are between water-based indicators (which depend on the tide at acquisition) and morphology-based indicators (which do not).

### 34.3.2 Lines defined by tidal datums

A **tidal datum** is a vertical reference defined as the average of a phase of the tide over a **National Tidal Datum Epoch** (NTDE), the 19-year period that averages out the 18.6-year lunar nodal cycle; the NTDE in current US use is 1983–2001, with a modernised epoch in preparation ([Chapter 9](ch09-vertical-datums.md)). **Mean high water (MHW)** is the average of all high waters over the epoch; **mean higher high water (MHHW)** the average of the higher of the two daily highs; **mean lower low water (MLLW)** the average of the lower of the two daily lows; **mean sea level (MSL)** the average of hourly heights; **lowest astronomical tide (LAT)** the lowest level predictable under average meteorological conditions over the nodal cycle, used as chart datum by most hydrographic offices outside the United States. A **tide-coordinated shoreline** is the intersection of the land surface with one of these datums. It cannot be photographed, because the water is at MHW only for an instant twice a day on average and never exactly; it must be constructed either by timing the observation to the datum (tide-coordinated photography, the historical NOAA method) or by intersecting a DEM with a model of the datum's elevation. The second method, demonstrated by Li, Ma, and Di (2002) and routine now, is where DEMs enter the shoreline business: a lidar DTM of the beach, a model of the MHW surface in the DTM's vertical datum (in the United States, NOAA's **VDatum** supplies the transformation from NAVD88 to MHW, MLLW, and the others as a spatially varying field), and a contour operation produce the MHW line.

### 34.3.3 Lines defined by law

The legal shoreline is a tidal line chosen by statute or case law. In the United States the seaward boundary of private upland against state-owned tidelands is, in most states, the **mean high water line**, and the controlling definition comes from *Borax Consolidated, Ltd. v. Los Angeles*, 296 U.S. 10 (1935), in which the Supreme Court held that the line is to be determined from the average of all high tides over the full 18.6-year lunar cycle, as determined by the Coast and Geodetic Survey—explicitly a scientific tidal datum, not the visible high-water mark or the vegetation line. Some states (Massachusetts, Maine, and others under colonial ordinance) use mean low water; Texas uses mean higher high water on the Gulf coast; Louisiana uses the civil-law shoreline. For the baseline of a nation's maritime zones, the **United Nations Convention on the Law of the Sea** Article 5 defines the **normal baseline** as "the low-water line along the coast as marked on large-scale charts officially recognized by the coastal State"; Article 7 permits **straight baselines** across deeply indented coasts and fringing islands, and Article 13 defines **low-tide elevations** (features above water at low tide but submerged at high tide) and their effect on the baseline. The low-water line in Article 5 is whatever datum the state's charts use—MLLW for the United States, LAT for most others—so that the legal baseline moves if the chart datum changes, with no sand moving at all.

NOAA's practice descends from Aaron Shalowitz's *Shore and Sea Boundaries* (two volumes, 1962 and 1964, with a third by Reed in 2000), which remains the authoritative treatment of how tidal datums, the *Borax* rule, and chart conventions combine. The National Ocean Service's shoreline—compiled historically from tide-coordinated aerial photography interpreted to the MHW line and the MLLW line, as reviewed by Graham, Sault, and Bailey (2003)—is now maintained as the **Continually Updated Shoreline Product (CUSP)**, which draws on lidar-derived tide-coordinated shorelines, imagery, and the charted shoreline, with source and date attributes per segment. On nautical charts, S-57 and S-101 encode the coastline (COALNE) and the land area boundary with attributes for the datum and the nature of the feature, and the charted low-water line is the one that carries legal weight under UNCLOS.

### 34.3.4 Extracting a shoreline from a DEM

The DEM method is a contour at the datum elevation, and its accuracy follows from the DEM's vertical accuracy and the beach slope. If the DEM (or the datum model) has a vertical error $\Delta z$ and the foreshore has slope angle $\beta$, the contour is displaced horizontally by

$$ \Delta x = \frac{\Delta z}{\tan \beta}. $$

On a steep gravel beach with $\tan\beta$ = 0.1, a 10 cm error moves the line 1 m. On a dissipative sand beach or a tidal flat with $\tan\beta$ = 0.005, the same 10 cm moves it 20 m, and a 30 cm error—the sum of a lidar RMSE, a VDatum uncertainty, and a geoid-model uncertainty is easily that—moves it 60 m. The uncertainty of a DEM-derived shoreline is therefore a map, not a number, and it is largest where the shoreline is most consequential for inundation.

The alternative, an **imagery-derived** shoreline from a water index such as NDWI or from classification, yields the instantaneous waterline at image time and must be corrected to a datum using the tide stage at acquisition and the local slope—which requires a DEM anyway. Where imagery and DEM shorelines disagree, the cause is usually the tide at image time, run-up, or a DSM used in place of a DTM (riparian trees or marsh vegetation lifting the surface and pushing the contour seaward).

Finally, the length of a shoreline has no definite value. Mandelbrot (1967), building on Richardson's measurements, showed that the measured length $L$ of a coastline grows as the measuring step $\epsilon$ shrinks, $L(\epsilon) \propto \epsilon^{1-D}$ with a fractal dimension $D$ between 1 and about 1.3 for real coasts, so that a shoreline digitised from a 1 m DEM is longer than one from a 30 m DEM, not because either is wrong but because length at this scale is not an intrinsic property. Comparing shoreline lengths across sources without matching the resolution is meaningless; comparing positions is meaningful only after matching the datum.

> **Worked example.** A coastal lidar DTM has a tested vertical accuracy (NVA) of 10 cm RMSE in NAVD88; the VDatum NAVD88→MHW transformation in the area has a stated uncertainty of about 8 cm (1σ); the MHW surface is therefore known to $\sqrt{0.10^2 + 0.08^2} \approx 0.13$ m (1σ). On a beach segment with foreshore slope 1:40 ($\tan\beta$ = 0.025), the MHW line's horizontal uncertainty is $0.13/0.025 \approx 5$ m (1σ), about 10 m at 95 %. On an adjacent mudflat at 1:400, it is 52 m (1σ). A change study that compares this MHW line with one from a 2005 photogrammetric DEM with 30 cm RMSE must carry $\sqrt{0.13^2 + 0.30^2}/0.025 \approx 13$ m (1σ) of positional noise on the beach and must not report changes smaller than roughly 30 m there as detected.

<!-- figure: Figure 34.2 — Cross-shore profile with the instantaneous waterline, wet/dry line, vegetation line, and the MHW, MLLW, and LAT datum intersections marked; inset showing Δx = Δz / tan β for two slopes. -->

## 34.4 Shorelines move

A shoreline position has a date for three independent reasons, and change analysis must separate them.

The sand moves. **Erosion and accretion** shift beaches by metres per year on average and tens of metres in a storm; a **seasonal profile** cycle moves the waterline tens of metres between summer berm and winter bar with no net change; deltas prograde and retreat with sediment supply. These are the signals shoreline-change studies seek, quantified by transect-based rates with per-epoch positional uncertainty ([Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).

The water moves. **Sea-level rise** of around 3–4 mm yr⁻¹ globally, more where land subsides, raises every tidal datum; on a 1:100 foreshore, a decade of 3.5 mm yr⁻¹ moves the MHW line landward by $0.035/0.01$ = 3.5 m with no sand moving. **Subsidence**—of groundwater-extraction basins, deltas, and reclaimed land, at rates from millimetres to several centimetres per year—does the same by lowering the land relative to the datum. Storm surge moves the instantaneous line far inland for hours.

The datum moves. When NOAA adopts a new **tidal datum epoch**, every tidal datum elevation is recomputed from a more recent 19 years; because sea level rose during the interval, MHW rises by several centimetres relative to the land, and the MHW shoreline shifts landward—again with no physical change. The same happens when a geoid model or vertical datum is replaced (NAVD88 → NAPGD2022) and the DEM is retransformed, if the datum transformation is not applied consistently to both epochs. Comparing a shoreline referenced to the 1960–1978 epoch with one referenced to 1983–2001 as if the difference were erosion is one of the recurring errors in coastal change literature; the fix is to express both in the same epoch (NOAA publishes the offsets between epochs at each station) before differencing.

## 34.5 Rivers

A river in a DEM is three surfaces that are routinely confused: the water surface at acquisition, the bed beneath it, and the banks that bound it. Topographic lidar sees only the third and fragments of the first.

The **water-surface slope** is the first thing to get right. Rivers fall; hydro-flattening makes them fall monotonically, but the slope assigned is interpolated between bank elevations and the actual water surface on the day is rarely known except at gauges. For hydraulic modelling the water surface at acquisition is a useful calibration observation—its elevation along the reach, together with the gauge discharge that day, is a free stage–discharge data point—so recording the date and the gauge reading with the DEM is worth doing.

The **bathymetry gap** is the larger problem. A flood model built on a lidar DTM has a channel that stops at the water surface on the survey day; the volume below is missing and conveyance at low flows is wrong by the whole channel capacity. The remedies, in increasing order of cost: **burning in** a synthetic channel (lowering the DEM along the centreline by an assumed depth or a width–depth hydraulic-geometry relation); surveyed cross-sections interpolated into a bed; bathymetric lidar in clear shallow water ([Chapter 19](ch19-bathymetric-lidar.md)); sonar in navigable reaches ([Chapter 20](ch20-sonar.md)). Burned channels must be flagged: a 2 m channel burned into a DEM with 10 cm accuracy is an assumption, not a measurement, and should not survive into the archived terrain product. FEMA's riverine guidance requires surveyed channel geometry where the channel conveys a significant share of the flow for exactly this reason.

The **thalweg**—the line of deepest points along the channel—is a jurisdictional boundary on many rivers and the reference line for migration studies; derived from a lidar DTM it is the lowest line of the exposed bed or water surface, not the real bed, and should be labelled so. **Ice-covered rivers** at acquisition present a rough ice surface above open-water stage; winter lidar in cold regions must mask them.

## 34.6 Lakes, reservoirs, and wetlands

Large lakes have their own level datums. The Great Lakes use the **International Great Lakes Datum of 1985 (IGLD 85)**, a dynamic-height datum referenced to a point at Rimouski, Quebec, and periodically updated because glacial isostatic adjustment tilts the basins by tens of centimetres per century between the rising north shores and the stable south; a new IGLD realisation is in preparation. Lake levels are then reported as heights above the datum, and a DEM of a Great Lakes shoreline must state whether its zero is IGLD 85, NAVD88, or local water level on the day. Other large lakes and most reservoirs use a project datum defined by the operator, often tied to an old benchmark and offset from the national datum by unknown decimetres.

A **reservoir capacity curve**—storage volume as a function of elevation—is a DEM product, computed by integrating area below each level over bathymetry and exposed shore. Sedimentation reduces capacity by fractions of a per cent per year; repeat surveys at drawdown (lidar) and at pool (sonar), differenced, give the volume lost, with accuracy limited by the datum consistency across the topobathy seam of §34.8.

**Wetlands and marsh platforms** sit within centimetres of water and inherit the vegetation bias of [Chapter 32](ch32-dsm-to-dtm.md): lidar "ground" in a *Spartina* marsh is typically 10–30 cm above the sediment surface. Because marsh elevation relative to the tidal frame determines inundation frequency, zonation, and sea-level-rise vulnerability, a 15 cm bias is the difference between a marsh that keeps pace and one that drowns in the model. Correction models (LEAN and similar) regress lidar error against vegetation metrics using RTK truth; without correction, marsh DEMs should carry an explicit bias statement.

## 34.7 Hydro-conditioning for flow routing

Flow routing on a grid assigns each cell a flow direction toward a lower neighbour and accumulates upstream area along those directions; the stream network, catchments, and indices such as HAND fall out. The algorithm requires that every cell has a downslope path to the edge, which a measured DEM never satisfies: it has depressions and flats, some real, most artefacts.

**Depressions** in a lidar DTM arise from interpolation across voids, from noise, from vegetation removal, and—most consequentially—from road and railway embankments that cross streams on culverts the sensor cannot see; the embankment appears as a dam and the valley above it as a sink. **Flats** arise from hydro-flattening, from vertical quantisation, and from genuinely flat terrain. Two families of algorithm resolve them. **Filling** raises each depression to the elevation of its spill point, producing a surface with no sinks; the classic implementation is Jenson and Domingue (1988), and the efficient modern one is **Priority-Flood** (Barnes, Lehman, and Mulla, 2014), which processes cells from the edges inward with a priority queue and runs in $O(n \log n)$ time or $O(n)$ for integer data. **Breaching** instead cuts a channel from the depression's lowest cell through the barrier to the nearest lower cell, lowering the barrier rather than raising the basin; Lindsay (2016) formalised efficient breaching and hybrid breach-then-fill methods and showed that breaching modifies far fewer cells, by far smaller amounts, than filling on typical lidar DEMs, because the barriers are thin (an embankment) while the basins behind them are large. Breaching is physically closer to what a culvert does; filling is what happens when the culvert is blocked. Either way, the volume of change—cells modified, mean and maximum modification—should be reported, and large modifications inspected: a fill of 5 m over 2 km² is a dammed valley that needs a culvert cut, not a smoothing artefact.

Flats are resolved by imposing a small gradient toward the outlet (Garbrecht and Martz, 1997, or its priority-flood successors). Flow direction is then assigned by **D8** (O'Callaghan and Mark, 1984: flow to the steepest of eight neighbours) or **D∞** (Tarboton, 1997: flow split between the two neighbours bracketing the steepest triangular facet, giving dispersed accumulation on hillslopes). D8 produces parallel-line artefacts on planar slopes and under-represents divergent flow; D∞ is more realistic on hillslopes but spreads flow where it should concentrate. Channels, once defined by an accumulation threshold, should be routed with D8 regardless.

**HAND**—height above nearest drainage (Nobre et al., 2011)—reclassifies the DEM as elevation above the nearest stream cell along the flow path, giving a terrain-based flood susceptibility index that is used, with synthetic rating curves, in continental-scale flood forecasting. HAND inherits every conditioning decision: a mis-breached embankment changes which stream a cell drains to and therefore its HAND.

Not every depression is an artefact. **Karst** sinkholes, **prairie potholes**, **playas**, kettle lakes, and detention basins are real closed basins; filling them creates fictitious channels across divides. Distinguish them by size and depth (real basins are usually larger and deeper than interpolation pits), by independent knowledge (wetland inventories, geology), and by inspecting what the fill produced. The LBS requires hydro-flattening but explicitly does not require the base DEM to be conditioned; the depressions are the user's to interpret.

> **Try it.** Compare filling and breaching on a lidar DTM with WhiteboxTools and report how many cells each changed. Expected outcome: breaching modifies a small fraction of the cells that filling does; the difference raster shows filling pooling behind road embankments.
>
> ```bash
> whitebox_tools -r=FillDepressions -i=dtm.tif -o=dtm_fill.tif --fix_flats
> whitebox_tools -r=BreachDepressionsLeastCost -i=dtm.tif -o=dtm_breach.tif --dist=50 --fill
> gdal_calc.py -A dtm_fill.tif -B dtm.tif --outfile=fill_delta.tif --calc="A-B" --NoDataValue=-9999
> gdal_calc.py -A dtm_breach.tif -B dtm.tif --outfile=breach_delta.tif --calc="A-B" --NoDataValue=-9999
> for f in fill_delta.tif breach_delta.tif; do
>   gdalinfo -stats $f | grep -E "STATISTICS_(MEAN|MAXIMUM|MINIMUM)"
> done
> whitebox_tools -r=D8Pointer -i=dtm_breach.tif -o=d8.tif
> whitebox_tools -r=D8FlowAccumulation -i=d8.tif -o=facc.tif --pntr
> ```
>
> Keep `dtm.tif` unchanged; `dtm_breach.tif` is a modelling surface, not a product.

## 34.8 Topobathy stitching and the white ribbon

Along almost every coast there is a strip—from the low-water line out to the depth where survey vessels can safely work—in which neither topographic lidar (water absorbs it), nor multibeam (too shallow, too dangerous), nor charts (sparse old lead-line soundings) provides reliable elevations. Hydrographers call it the **white ribbon**. Bathymetric lidar fills it where water clarity allows ([Chapter 19](ch19-bathymetric-lidar.md)); satellite-derived bathymetry fills it coarsely where it does not ([Chapter 23](ch23-satellite-derived-bathymetry.md)); elsewhere it is interpolated across, with a seam.

Building a seamless topobathy DEM across the seam requires, first, a common vertical datum. Topography arrives in an orthometric datum (NAVD88), bathymetry in a chart datum (MLLW, LAT); the transformation between them is a spatially varying field (VDatum in the United States, similar models elsewhere) with its own uncertainty of 5–20 cm that is largest exactly in estuaries and over shallow flats where the seam lies. Second, a common horizontal datum and epoch. Third, a decision rule where the datasets overlap or conflict: Eakins and Grothe (2014) describe the NOAA practice—a priority order among sources, buffering and feathering at boundaries, consistency checks of the shoreline against both datasets, and a source raster that records which dataset supplied each cell. Fourth, the shoreline itself must be consistent: if the topographic data put MLLW at one position and the bathymetric data put zero depth 30 m seaward, the DEM has a step or a spurious terrace at the seam. [Chapter 48](ch48-compositing.md) treats compositing generally; the coastal case adds the datum field and the ribbon.

> **Case file.** Gesch (2009, 2018) examined the lidar-based sea-level-rise vulnerability maps that proliferated after 2005 and showed that many reported inundation for 1 m of rise without accounting for DEM vertical uncertainty or for the offset between the DEM's orthometric zero and local MHHW. With NAVD88 several decimetres from MHHW along much of the US coast and lidar RMSE of 10–20 cm, the smallest increment such a DEM could resolve at 95 % confidence was about 0.3–0.5 m. The resulting best practice—transform to a tidal datum with VDatum, report inundation with a confidence level, never map increments smaller than the DEM can resolve—is now standard in NOAA's Sea Level Rise Viewer and coastal flood guidance.

## Then & now

The shoreline was a surveyed line long before it was a datum intersection: the US Coast Survey's topographic sheets (T-sheets) from the 1830s onward recorded the high-water line by plane table, and the legal weight of that line was settled only in 1935 by *Borax*. Tide-coordinated aerial photography, flown within a window of predicted MHW or MLLW, replaced the plane table from the 1920s and remained NOAA's method into the 2000s; Shalowitz's volumes (1962, 1964) codified the doctrine. Lidar and VDatum made the tide-coordinated shoreline a computation rather than a flight-timing exercise, and CUSP (from the 2010s) turned the national shoreline into a continuously updated, source-attributed vector product.

Flow routing began with Peucker and Douglas's ridge-and-channel detection (1975) and O'Callaghan and Mark's D8 (1984), on coarse DEMs where depressions were mostly noise and "fill everything" was reasonable; Jenson and Domingue (1988) made filling standard in GIS. Lidar DTMs at 1 m, with real culverts, embankments, and potholes, broke that assumption: Priority-Flood (2014) and Lindsay's breaching (2016) are responses to DEMs in which filling does more damage than the artefacts it removes. Hydro-flattening as a specified product dates from the first USGS LBS (2012); Global Surface Water (2016) made "where is water, and how often" a lookup. The frontier is continental hydro-conditioning with culvert inventories and learned culvert detection, and ICESat-2 and SWOT measuring water-surface elevations directly, so that the water surface becomes an observed, time-stamped layer rather than a flattening assumption.

## Mathematics

**Slope amplification.** For a datum or DEM error $\Delta z$ and foreshore slope angle $\beta$, the horizontal displacement of a datum contour is $\Delta x = \Delta z / \tan\beta$. With independent errors in the DEM ($\sigma_{\text{DEM}}$) and the datum model ($\sigma_{\text{datum}}$), $\sigma_x = \sqrt{\sigma_{\text{DEM}}^2 + \sigma_{\text{datum}}^2}\,/\tan\beta$. For a change between two epochs, add the two $\sigma_x$ in quadrature.

**D8 flow direction.** For cell $c$ with neighbours $n_i$ at distance $d_i$ ($d$ for cardinal, $d\sqrt{2}$ for diagonal neighbours), the direction is $\arg\max_i\, (z_c - z_{n_i})/d_i$ over neighbours with positive drop. **D∞** (Tarboton, 1997) considers the eight triangular facets formed by the centre and pairs of adjacent neighbours, computes the steepest descent direction $\theta$ on each facet, takes the facet with the largest slope, and partitions flow between its two bounding cardinal/diagonal directions in proportion to the angular distance: $p_1 = (\pi/4 - \alpha)/(\pi/4)$, $p_2 = \alpha/(\pi/4)$, where $\alpha$ is the angle between $\theta$ and the nearer bounding direction.

**Priority-Flood.** Initialise a priority queue with all edge cells (elevation as priority) and mark them processed. Repeatedly pop the lowest cell $c$; for each unprocessed neighbour $n$, set $z_n \leftarrow \max(z_n, z_c)$ (filling) or, for flat resolution, $z_n \leftarrow \max(z_n, z_c + \epsilon)$, push $n$, mark it processed. Each cell is pushed and popped once, so the cost is $O(n \log n)$ with a binary heap, or $O(n)$ with a radix structure for integer elevations (Barnes, Lehman, and Mulla, 2014). Breaching (Lindsay, 2016) instead searches from each pit along a least-cost path to the nearest cell lower than the pit and lowers the cells on that path; the hybrid applies breaching up to a maximum length or depth and fills what remains.

**Fractal length.** For a coastline of fractal dimension $D$, the length measured with step $\epsilon$ scales as $L(\epsilon) = k\,\epsilon^{1-D}$. For the west coast of Britain, Mandelbrot (1967) quoted $D \approx 1.25$: halving the step multiplies the length by $2^{0.25} \approx 1.19$. A 1 m DEM shoreline is therefore of order $(30)^{0.25} \approx 2.3$ times longer than a 30 m one for the same coast.

## Validation & uncertainty

Three questions organise validation of water in a DEM: are the water cells correctly identified, are the elevations assigned to them defensible, and what did conditioning do to the land?

**Identification.** Compare the hydro-flattening breaklines and water masks against an independent source: orthoimagery of the same date, the GSW occurrence layer, or the national hydrography dataset. Report commission (land flattened as water—typically parking lots, flat roofs, and salt pans with lidar dropouts) and omission (water not flattened—narrow channels, shaded ponds) as areas and as a confusion matrix. For tidal flats, record the tide stage per flight line against the specified window; flights outside the window produce a different waterline and, for bathymetric lidar, a different land–water class boundary.

**Elevation.** For each flattened water body, report the elevation assigned, its source (lowest adjacent ground return, gauge reading, specified level), and the date. Where a gauge exists, the difference between the flattened elevation and the gauge stage on the acquisition date is a direct check; differences larger than the lidar's NVA indicate that the lowest-bank rule, not the water, set the level. For rivers, verify monotonicity along the breakline (no cell higher than the one upstream) with a scripted check, and verify that the water-surface slope lies within the range plausible for the reach. For shorelines, compute the positional uncertainty map from $\sigma_z/\tan\beta$ using the DEM's tested accuracy and the datum model's stated uncertainty, and check a sample of the DEM-derived datum line against RTK profiles or tide-staff observations: the mean offset tests the datum transformation, the scatter tests the DEM.

**Conditioning.** Archive the difference raster between the conditioned and the original DEM and summarise it: number and fraction of cells modified, mean and maximum modification, and the ten largest contiguous modified regions with their locations. Inspect those regions by hand: each is either a culvert that needs an enforcement cut, a real closed basin that should be preserved, or a data artefact to be fixed at source. Report which flow-direction algorithm was used and the accumulation threshold for channel initiation; compare the derived network to the mapped hydrography with a buffer-overlap metric (fraction of mapped stream length within 1–2 cells of a derived channel) and investigate the misses.

> **Uncertainty budget.** Horizontal position of a lidar-derived MHW shoreline on a sandy beach, 1σ, representative values:
>
> | Component | Vertical (m) | Horizontal at tanβ = 0.02 (m) |
> |---|---|---|
> | Lidar DTM vertical error (NVA) | 0.10 | 5.0 |
> | VDatum NAVD88→MHW transformation | 0.05–0.10 | 2.5–5.0 |
> | Residual vegetation/wrack bias at the datum line | 0.00–0.10 | 0–5 |
> | Tidal-datum epoch (if not matched between epochs) | 0.03–0.08 | 1.5–4.0 |
> | Beach change between lidar and reference date | — | 1–10 |
> | Combined (typical) | 0.13–0.17 | 7–10 |
>
> At 95 % the shoreline is known to roughly ±15–20 m on this slope; on a 1:200 flat, multiply the horizontal column by five.

## Software

**Open source:** WhiteboxTools (`FillDepressions`, `BreachDepressionsLeastCost`, `D8Pointer`, `DInfPointer`, `ElevationAboveStream` for HAND; the most complete open hydro-conditioning toolbox); TauDEM (Tarboton's D∞ suite, MPI-parallel for large grids); RichDEM (Barnes's Priority-Flood implementations, Python API); GRASS GIS (`r.watershed` routes without filling via least-cost search, `r.fill.dir`, `r.carve` for burning streams, `r.lake` for level-based inundation); SAGA (Wang & Liu fill, channel network tools); pysheds (lightweight Python D8/D∞ with conditioning); GDAL (`gdal_fillnodata`, `gdal_rasterize` for breaklines, `gdal_contour` for datum lines); Google Earth Engine (GSW access); NOAA VDatum (free, Java; the US datum-transformation field). Caveat: default "fill sinks" in every package fills real basins silently.

**Free but closed:** NOAA Sea Level Rise Viewer and CUSP downloads (data, not tools).

**Commercial:** ArcGIS Spatial Analyst Hydrology toolset and Arc Hydro (fill, D8, stream definition, HAND via extensions; D∞ absent in the core toolset); Global Mapper (hydro-flattening and watershed tools); Terrasolid TerraScan/TerraModeler (breakline-driven hydro-flattening in production). Caveat: production hydro-flattening is still largely a manual breakline task in any package.

## Standards & guides

- **USGS Lidar Base Specification** (v2.1, 2020, with later revisions). Hydro-flattening thresholds (2-acre water bodies, 100-ft rivers), breakline requirements, distinction from hydro-enforcement and hydro-conditioning.
- **NOAA NOS / NGS shoreline standards and CUSP documentation.** Tide-coordinated shoreline definition, MHW/MLLW compilation, attributes and sources for the national shoreline.
- **NOAA Special Publication NOS CO-OPS 1,** *Tidal Datums and Their Applications* (2000), and **NOAA Technical Report NOS CO-OPS,** tidal datum epoch policy. Definitions of MHW, MHHW, MLLW, MSL; epoch rules.
- **FEMA Guidelines and Standards for Flood Risk Analysis and Mapping** (current). Requirements for hydraulic terrain, channel bathymetry, and structure representation in flood studies.
- **IHO S-57 (ed. 3.1) and S-101** product specifications. Coastline (COALNE), land area, and depth-area features; sounding datum attributes.
- **United Nations Convention on the Law of the Sea (1982),** Articles 5, 7, 13. Normal baseline, straight baselines, low-tide elevations.
- **Shalowitz, A. L., *Shore and Sea Boundaries*** (1962, 1964) and Reed, M. W. (2000), vol. 3. The authoritative US treatment of tidal boundary doctrine.

## Pitfalls

- **Flattening a river to a horizontal plane.** The tool or the operator treats a river like a lake. Detect by checking the water-surface profile along the breakline for zero slope over long reaches; avoid by enforcing monotonic breaklines with bank-derived elevations.
- **Filling sinks that are real.** Default conditioning removes karst, potholes, playas, and detention basins. Detect by mapping the fill depth and inspecting the largest regions against wetland and geology layers; avoid by breaching first and whitelisting known closed basins.
- **"Shoreline" extracted from a DSM with riparian trees or marsh vegetation.** The datum contour runs through the canopy or the marsh surface, metres seaward of truth. Detect by comparing DSM and DTM contours; avoid by extracting only from a vegetation-corrected DTM.
- **Treating a reservoir at drawdown as terrain.** The exposed bed is flattened or interpreted as a permanent land surface. Detect by comparing acquisition-date level with the operator's record and GSW seasonality; avoid by recording the level and date in the metadata.
- **Comparing shorelines from different tidal epochs or datums as change.** Datum shifts of centimetres become apparent erosion of metres. Detect by checking the datum and epoch of each source; avoid by transforming both to the same datum and epoch first.
- **Burned-in channels surviving into the archived DEM.** A modelling assumption becomes "measured terrain." Detect by looking for channels of suspiciously uniform depth; avoid by keeping the burned surface as a separate, flagged product.
- **A culvert treated as a dam.** The embankment appears impermeable; filling floods the valley above it in the model. Detect by the fill-depth map along road networks; avoid by hydro-enforcing with a culvert inventory.
- **Mixing NAVD88 topography with MLLW bathymetry across the seam without VDatum.** A step of several decimetres appears at the shoreline. Detect by profiles across the seam; avoid by transforming both to one datum with the transformation's uncertainty recorded.
- **Flood-season or post-storm acquisition presented as terrain.** The DEM shows a water surface metres above the floodplain. Detect by comparing acquisition dates with gauge records; avoid by acquisition windows tied to stage.
- **Marsh "ground" biased by vegetation and used for SLR exposure.** A 15 cm positive bias halves the mapped inundation. Detect with RTK transects; avoid with a correction model and an explicit bias statement.

## Key takeaways

- Water is a surface with its own datum and its own date; a DEM records the water of the acquisition day, not a permanent elevation.
- Hydro-flattening (cartographic, DEM only), hydro-enforcement (terrain edited at structures), and hydro-conditioning (algorithmic sink removal for routing) are three operations; know which was done, keep the unmodified DEM, and archive the difference.
- The shoreline is a legal and tidal construct—MHW in most US states by *Borax*, the charted low-water line under UNCLOS Article 5—not a visible line; extract it as a datum contour from a DTM via VDatum and report its uncertainty as $\sigma_z/\tan\beta$.
- Shorelines move because sand moves, because water rises, and because datums and epochs are updated; a change study must separate the three.
- Rivers in lidar DTMs lack bathymetry; burn-in is an assumption, surveyed cross-sections or bathymetric sensors are measurements, and the two must be labelled differently.
- Breach before filling; inspect the largest modifications; real closed basins exist and must be preserved.
- The topobathy seam requires a common datum through a transformation field with its own uncertainty, a source raster, and a shoreline consistent with both sides.
- Use Global Surface Water occurrence to decide, reproducibly, whether a void is permanent water, seasonal water, or something else.

## References

- Barnes, R., Lehman, C., & Mulla, D. (2014). Priority-flood: An optimal depression-filling and watershed-labeling algorithm for digital elevation models. *Computers & Geosciences*, 62:117–127.
- Boak, E. H., & Turner, I. L. (2005). Shoreline definition and detection: A review. *Journal of Coastal Research*, 21(4):688–703.
- *Borax Consolidated, Ltd. v. City of Los Angeles*, 296 U.S. 10 (1935).
- Eakins, B. W., & Grothe, P. R. (2014). Challenges in building coastal digital elevation models. *Journal of Coastal Research*, 30(5):942–953.
- Garbrecht, J., & Martz, L. W. (1997). The assignment of drainage direction over flat surfaces in raster digital elevation models. *Journal of Hydrology*, 193(1–4):204–213.
- Gesch, D. B. (2009). Analysis of lidar elevation data for improved identification and delineation of lands vulnerable to sea-level rise. *Journal of Coastal Research*, SI 53:49–58.
- Gesch, D. B. (2018). Best practices for elevation-based assessments of sea-level rise and coastal flooding exposure. *Frontiers in Earth Science*, 6:230.
- Graham, D., Sault, M., & Bailey, C. J. (2003). National Ocean Service shoreline—Past, present, and future. *Journal of Coastal Research*, SI 38:14–32.
- Heidemann, H. K. (2020). *Lidar Base Specification*, version 2.1. U.S. Geological Survey Techniques and Methods 11-B4 (with subsequent online revisions).
- Jenson, S. K., & Domingue, J. O. (1988). Extracting topographic structure from digital elevation data for geographic information system analysis. *Photogrammetric Engineering & Remote Sensing*, 54(11):1593–1600.
- Li, R., Ma, R., & Di, K. (2002). Digital tide-coordinated shoreline. *Marine Geodesy*, 25(1–2):27–36.
- Lindsay, J. B. (2016). Efficient hybrid breaching-filling sink removal methods for flow path enforcement in digital elevation models. *Hydrological Processes*, 30(6):846–857.
- Mandelbrot, B. (1967). How long is the coast of Britain? Statistical self-similarity and fractional dimension. *Science*, 156(3775):636–638.
- Nobre, A. D., Cuartas, L. A., Hodnett, M., Rennó, C. D., Rodrigues, G., Silveira, A., Waterloo, M., & Saleska, S. (2011). Height Above the Nearest Drainage—a hydrologically relevant new terrain model. *Journal of Hydrology*, 404(1–2):13–29.
- O'Callaghan, J. F., & Mark, D. M. (1984). The extraction of drainage networks from digital elevation data. *Computer Vision, Graphics, and Image Processing*, 28(3):323–344.
- Pekel, J.-F., Cottam, A., Gorelick, N., & Belward, A. S. (2016). High-resolution mapping of global surface water and its long-term changes. *Nature*, 540:418–422.
- Poppenga, S. K., Worstell, B. B., Stoker, J. M., & Greenlee, S. K. (2010). *Using selective drainage methods to extract continuous surface flow from 1-meter lidar-derived digital elevation data.* U.S. Geological Survey Scientific Investigations Report 2010-5059.
- Shalowitz, A. L. (1962, 1964). *Shore and Sea Boundaries*, vols. 1–2. U.S. Coast and Geodetic Survey Publication 10-1. U.S. Government Printing Office. (Vol. 3 by Reed, M. W., 2000.)
- Tarboton, D. G. (1997). A new method for the determination of flow directions and upslope areas in grid digital elevation models. *Water Resources Research*, 33(2):309–319.
- United Nations (1982). *United Nations Convention on the Law of the Sea.* Articles 5, 7, 13.

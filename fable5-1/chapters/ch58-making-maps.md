# Chapter 58 — Making maps from elevation: topographic maps, charts, graticules, standard elements

> **Part XII — Visualization and cartography.** [Chapter 57](ch57-visualizing-dems.md) made terrain visible; this chapter turns a DEM or a bathymetric grid into a finished map or chart — generalized, symbolized, and framed by the marginalia that make it a verifiable claim rather than a picture.

**In this chapter.** A topographic map and a nautical chart are the two oldest products made from elevation data, and both have rules — some written into standards, some into two centuries of practice — about how the surface may be generalized, what the sheet must say about itself, and who is liable when it is wrong. This chapter covers map purpose and scale and the accuracy standards tied to them (NMAS 1947); the USGS quadrangle series, its successor US Topo, and their national counterparts; how to derive contours from a DEM without inventing detail the data cannot support; how soundings, isobaths, and depth tints are selected shoal-biased for a nautical chart and how CATZOC and S-101/S-102 carry quality into the ENC; the terrain and obstacle rules of aeronautical charts; the difference between a graticule and a grid and why the declination diagram carries a date; the standard marginalia and what web maps silently drop; and a QA routine for a finished map. You should finish able to read a legacy sheet correctly, produce a defensible contour map or chart overlay from a DEM, and recognize a map whose margins do not support its content.

## 58.1 Map purpose, scale, and accuracy standards

A map is a generalization of the world to a purpose, and the purpose determines the scale, the generalization rules, the contour interval, the symbols, and the accuracy the user may assume. Four purposes dominate elevation cartography. **Topographic maps** are general-purpose: they show relief, hydrography, transport, settlement, and boundaries for anyone who needs to know what is where. **Nautical charts** serve safety of navigation and are legally privileged for it; their rules are asymmetric because an error toward "deeper" can sink a ship and an error toward "shallower" merely costs a detour. **Aeronautical charts** depict terrain and obstacles for pilots, with their own asymmetric rounding rules. **Thematic maps** — slope, flood hazard, landslide susceptibility — show one derived variable and borrow the topographic base for context.

Scale drives generalization. At 1:24,000, 1 mm on paper is 24 m on the ground; at 1:250,000 it is 250 m. A 10 m wide stream is a double line at the first scale and a single line narrower than its true width at the second; a cluster of houses becomes a tinted built-up area; a contour is smoothed to the gullies that can be drawn apart. The **contour interval** follows from scale and relief: USGS 7.5′ quadrangles used 5, 10, 20, 40, or 80 ft depending on terrain; metric series commonly use 5, 10, or 20 m; 1:50,000 sheets in mountainous countries use 20 m (LINZ Topo50) or more. The interval is a promise about accuracy as well as a legibility choice, as the next paragraph makes explicit.

The **United States National Map Accuracy Standards (NMAS)**, issued by the Bureau of the Budget on 17 June 1947 ⟨H⟩, fixed the promise for two generations of maps. Horizontally, for maps at scales larger than 1:20,000, not more than 10 % of well-defined points tested may be in error by more than 1/30 inch at publication scale (0.85 mm, i.e. 20 m at 1:24,000); for 1:20,000 and smaller, the limit is 1/50 inch (0.5 mm, i.e. 127 m at 1:250,000). Vertically, not more than 10 % of elevations tested may be in error by more than one-half the contour interval, with the test points permitted to be shifted horizontally by the horizontal tolerance before the vertical comparison is made. A map meeting the standard could print "This map complies with National Map Accuracy Standards" in its margin; one that did not had to say nothing. NMAS is a 90 % criterion with no explicit statistical model; later standards (ASPRS 1990 and 2014; [Chapter 53](ch53-accuracy-assessment.md)) replaced it with RMSE-based classes, but NMAS still defines what a legacy contour means. The 90 %/half-interval rule implies, for Gaussian errors, an RMSE of about 0.3 times the interval: a 20 ft (6.1 m) contour sheet promises roughly 1.8 m RMSE at best, and nothing finer.

> **Definitions that bite.** *Scale* means three things. The **representative fraction** (1:24,000) is the nominal ratio of map distance to ground distance, valid exactly only where the projection's scale factor is 1. The **compilation scale** is the scale at which the map's content was generalized, which for a chart or a derived product may be much smaller than the display scale a screen allows — an ENC compiled at 1:80,000 zoomed to 1:5,000 shows no more information, only larger symbols, and ECDIS flags this as **overscale**. The **scale of the source data** — a 10 m DEM, 1:40,000 photography — bounds what either of the others can honestly claim. Confusing the three is how a 1:250,000-derived web layer ends up guiding a ground-level decision.

## 58.2 USGS topographic maps and other national series

### 58.2.1 The 7.5-minute series and the Historical Topographic Map Collection

The USGS began systematic topographic mapping of the United States in 1879 ⟨H⟩, first on 1:250,000 and 1:125,000 sheets, then on the 15-minute 1:62,500 series. The **7.5-minute quadrangle** at 1:24,000 (1:25,000 for some metric sheets, 1:63,360 for Alaska) became the primary series after the Second World War; production ran from 1947 to 1992, when the roughly 55,000 sheets covering the conterminous United States were complete. Each sheet covers 7.5′ × 7.5′ — about 13 by 17 km at mid-latitudes — and was compiled photogrammetrically, then field-checked: surveyors walked the ground to verify names, classify roads, and confirm what the stereo plotter could not see under trees.

The sheets are a time capsule, and reading one requires knowing its vintage. Horizontal positions are on **NAD27** ⟨H⟩ for most of the series, with later editions showing NAD83 tick marks offset in the margin; the NAD27→NAD83 shift is tens of metres in most of the conterminous United States and over 100 m in places ([Chapter 8](ch08-horizontal-datums.md)). Elevations and contours are on **NGVD29**, which differs from NAVD88 by roughly −0.4 to +1.5 m across the country ([Chapter 9](ch09-vertical-datums.md)) — meaning that a spot height on a 1950s sheet is not comparable to a modern DEM to better than a metre without conversion, which is in any case finer than the sheet's own accuracy. The **declination diagram** gives magnetic declination for the sheet centre at the date of the survey; the magnetic field has moved since. Contour intervals are in feet; coordinates in the margin include geographic ticks, a UTM grid (full or ticks), and State Plane ticks in feet.

The **Historical Topographic Map Collection (HTMC)** scanned every edition of every USGS topographic sheet published from 1884 to 2006 — more than 150,000 scans — and distributes them as georeferenced GeoPDF and GeoTIFF files through the National Map and topoView. The georeferencing is by the sheet's corner coordinates and must be treated as approximate (paper distortion, scanning, and the datum of the sheet all enter); a HTMC sheet overlaid on a modern DEM will show offsets of tens of metres that are datum shift, not change.

### 58.2.2 US Topo

In 2009 the USGS began publishing **US Topo**, a new 7.5-minute series produced not by field survey but by automated assembly of data from The National Map: 3DEP elevation ([Chapter 55](ch55-public-products.md)) for contours and shaded relief, NAIP orthoimagery as an optional layer, the National Hydrography Dataset, TIGER and other roads, structures, and boundaries, published as layered GeoPDF on a three-year refresh cycle (Moore 2011; USGS US Topo Product Standard). The gain is currency and complete coverage; the loss is everything field checking provided. Early US Topo editions lacked trails, many structures, some boundaries, and vegetation tint because no national database held them; several have since been added as sources appeared, and others remain absent. Contours are generated from the best available 3DEP DEM and smoothed for cartographic appearance, with the interval chosen per sheet; because the DEM may be 1 m lidar in one county and 10 m legacy data in the next, adjacent sheets can show contours of very different character and accuracy. The sheet's metadata states the elevation source. US Topo positions are on NAD83 and elevations on NAVD88, so a legacy sheet and its US Topo successor are on different datums horizontally and vertically — a difference that must be applied before any "then and now" comparison.

### 58.2.3 Other national series

Other mapping agencies made the same transition from field-compiled sheets to database-derived products, with differences in what they kept. Great Britain's **Ordnance Survey** publishes the 1:25,000 Explorer and 1:50,000 Landranger series from the OS MasterMap database, with contours (5 m and 10 m intervals) derived from OS Terrain data on the Ordnance Datum Newlyn vertical datum and the OSGB36 National Grid. France's **IGN** publishes the TOP 25 (1:25,000) on the Lambert-93 projection and RGF93 datum, heights in IGN69 (mainland). **swisstopo**'s national map at 1:25,000, redesigned from 2014 with a fully digital production chain, retains the relief shading tradition described by Imhof and uses the LV95 frame and LN02/LHN95 heights. Japan's **GSI** 1:25,000 series is the national base map. New Zealand's **LINZ Topo50** (1:50,000) has 20 m contours on NZGD2000 / NZTM2000 with heights in NZVD2016 for newer editions (verify which editions). Every one of these series has an edition date, a horizontal datum, a vertical datum, and a contour interval in its margin, and every one of them changed at least one of those during its life.

<!-- figure: Figure 58.1 — The same 7.5′ area on a 1958 USGS quadrangle (NAD27/NGVD29, 20 ft contours, field-checked) and a 2022 US Topo (NAD83/NAVD88, 10 m contours from 1 m lidar), with the datum offset between them shown by overlaying the two road networks. -->

## 58.3 Contours from DEMs

A contour is the intersection of the terrain with a horizontal plane, and in a DEM it is traced by **marching squares**: each grid cell is examined for edges whose endpoint elevations straddle the contour value, the crossing point on each such edge is found by linear interpolation, and the crossings are joined into line segments according to one of sixteen cases (with a saddle ambiguity in two of them that must be resolved consistently or contours will cross). `gdal_contour`, QGIS, GRASS `r.contour`, and GMT `grdcontour` all implement variants. The output is exact for the DEM — but the DEM is not the terrain, and a raw contour carries every grid artefact into a form readers trust more than a shaded image.

**Interval selection.** Use the NMAS logic in reverse: the interval should be at least about three times the DEM's vertical RMSE in the terrain concerned (so that 90 % of contour errors fall within half an interval), and large enough that contours remain separable at the publication scale on the steepest slopes you intend to show ([Chapter 57](ch57-visualizing-dems.md) §57.5). A 1 m lidar DTM with 0.1 m RMSE supports a 0.5 m interval in principle; at 1:10,000 that interval merges above about 11° slope and produces an unreadable black mass on any hillside, so 1 or 2 m with 0.5 m **supplementary contours** (dashed, drawn only on flat ground) is the usual compromise. Legacy 10 m or 30 m DEMs with several metres of RMSE do not support intervals below 10 m regardless of what the software will draw.

**Smoothing and generalization.** Contours from raw lidar grids are jagged at the cell scale and show the triangular facets of the interpolator, the circular pits of residual vegetation points, and the stair-steps of any DEM that was itself made from contours ([Chapter 59](ch59-vector-data.md) §59.3). Smooth the grid for the contour copy (a Gaussian of 1–3 cells, or a cartographic generalization such as the LIC-based method of Jenny, Jenny & Hurni 2011), then trace; this preserves topology. Simplify the lines afterwards with a tolerance well below the cell size (Douglas–Peucker at 0.2–0.5 cells), never above it, or the contour positional error exceeds the DEM's. Remove closed contours enclosing fewer than a few cells unless they mark a genuine feature.

**Depression contours and consistency.** Closed contours with lower ground inside need hachure ticks; the test is simple — compare the DEM elevation inside and outside the ring — and omitting it turns every sinkhole, quarry, and reservoir into a hill. Contours must agree with **spot heights** (a labelled summit of 1,234 m cannot sit inside the 1,240 m contour) and with **hydrography** (a stream must cross each contour once, at the apex of the V pointing upstream; a contour cannot cross a flattened lake). Where contours come from a DEM and hydrography from a separate vector dataset, they will disagree wherever the two were made at different dates or from different sources, and someone must decide which to move; on US Topo, hydro-flattened 3DEP DEMs ([Chapter 34](ch34-water-in-dems.md)) reduce but do not eliminate the problem.

**Staircase artefacts.** A DEM interpolated from contours (as many national 10–30 m DEMs were) has flat terraces at the source contour elevations and steps between them; contouring it at any interval that is not a multiple of the original produces wavy, bunched lines with a characteristic histogram spike at the original values. Check the DEM's elevation histogram before contouring: spikes at round numbers are the signature, and the only cure is a different DEM.

**Accuracy of the result.** A contour's positional accuracy is the DEM's vertical error divided by the local slope, plus the generalization displacement: $\sigma_{xy} \approx \sigma_z / \tan\beta \oplus \epsilon_{gen}$. On a 2° slope, 0.15 m of vertical error becomes 4.3 m of horizontal contour error; on a 30° slope, 0.26 m. This is why contours on flat ground are the least reliable lines on the map, and why supplementary contours on floodplains must be treated as indicative. Report contour accuracy as inherited from the DEM's assessed accuracy (NVA/VVA), not as a property of the lines.

> **Try it.** Generate smoothed, topologically clean contours with index and depression attributes from a lidar DTM. Expected result: a GeoPackage with 1 m contours, an `index` field true on every fifth line, and a `depression` field flagging closed lows; viewing the elevation histogram first tells you whether the DEM is contour-derived.
>
> ```bash
> # 0. Histogram check for stair-steps (spikes at round values => contour-derived DEM)
> gdalinfo -hist dtm.tif | tail -3
>
> # 1. Smooth a display copy (3x3 Gaussian-like kernel via gdal_calc, or use SAGA/Whitebox)
> whitebox_tools -r=GaussianFilter -i=dtm.tif -o=dtm_g1.tif --sigma=1.0
>
> # 2. Contours at 1 m, attribute 'elev'; 3D lines so Z is carried
> gdal_contour -a elev -i 1.0 -3d -f GPKG dtm_g1.tif contours.gpkg -nln contour
>
> # 3. Index contours and depressions (centre lower than the ring) with ogr2ogr/SQLite
> ogrinfo contours.gpkg -sql "ALTER TABLE contour ADD COLUMN idx INTEGER"
> ogrinfo contours.gpkg -sql "UPDATE contour SET idx = (CAST(elev AS INTEGER) % 5 = 0)"
> # Depression test: for closed rings, sample the DEM at the ring centroid (Python/rasterio)
> python - <<'EOF'
> import geopandas as gpd, rasterio
> from shapely.geometry import Polygon
> g = gpd.read_file("contours.gpkg", layer="contour"); src = rasterio.open("dtm_g1.tif")
> def depr(row):
>     ls = row.geometry
>     if not ls.is_ring: return 0
>     c = Polygon(ls.coords).representative_point()
>     z = next(src.sample([(c.x, c.y)]))[0]
>     return int(z < row.elev)
> g["depression"] = g.apply(depr, axis=1)
> g.to_file("contours.gpkg", layer="contour", driver="GPKG")
> print(g.depression.sum(), "depression contours of", len(g))
> EOF
> ```


## 58.4 Nautical charts from bathymetry

A nautical chart is the one map product whose generalization rules are written down as an international standard, because a mariner's life depends on them. IHO **S-4** (*Regulations of the IHO for International (INT) Charts and Chart Specifications of the IHO*) governs the paper and raster chart; **S-57** and its successor **S-101** govern the electronic navigational chart (ENC); **S-52** governs how an ECDIS displays it; **S-102** delivers a gridded bathymetric surface with uncertainty as an overlay. [Chapter 62](ch62-navigation-and-charting.md) treats navigation use; this section treats the compilation.

### 58.4.1 Soundings: shoal-biased selection

A modern multibeam survey yields millions of depths per square kilometre ([Chapter 20](ch20-sonar.md)); a chart at 1:20,000 can legibly show perhaps a few hundred. **Sounding selection** is the process of choosing which to print, and the governing rule is that the selection must be **shoal-biased**: within any neighbourhood, the shoalest sounding is retained before any other, so that a mariner reading the chart never sees a depth deeper than the least depth actually present nearby. Legibility then adds constraints — no overprinting, spacing that shows the trend of the bottom, denser coverage near dangers and channels. Zoraster and Bayer (1992) formulated this as a constrained optimization, and the approach underlies automated selection in CARIS, dKart, and similar systems; the hydrographer still reviews the result. Soundings are reduced to **chart datum** (LAT internationally, MLLW in the United States; [Chapter 9](ch09-vertical-datums.md)) and rounded *down* to the displayed precision (decimetres in shallow water, whole metres deeper), again so that the printed figure is never deeper than the measurement.

### 58.4.2 Depth contours, depth areas, and tints

**Depth contours** (isobaths) on a chart are generalized shoal-biased as described in [Chapter 57](ch57-visualizing-dems.md) §57.5: a smoothed or simplified isobath may move only toward deeper water. Between contours lie **depth areas**, polygons attributed with minimum and maximum depth, which in an ENC are what the ECDIS actually uses to colour the water and to compute whether the ship's safety contour is crossed. The chart's **depth tints** are flat colours assigned to depth areas; S-4 specifies the paper scheme and S-52 the ECDIS scheme, in which the mariner sets a **safety contour** (the shallowest ENC contour at or deeper than the ship's safety depth) and the display divides water into "safe" (white or very light) and "unsafe" (blue) with optional shallow and deep shades (the two- and four-shade modes). Because the ECDIS can only choose among contours present in the ENC, a chart with contours at 5, 10, and 20 m gives a vessel with a 7 m safety depth a 10 m safety contour — conservative, as intended — and a bathymetric grid with arbitrary contours would not improve the situation unless it is delivered as S-102.

### 58.4.3 CATZOC, source diagrams, and S-67

Charts have always indicated how much to trust them. The paper chart's **source diagram** divides the sheet into areas labelled by survey type and date ("leadline 1890", "multibeam 2015"). ENCs carry the **Category of Zone of Confidence (CATZOC)** attribute on each area as an M_QUAL object, with classes A1, A2, B, C, D, and U (unassessed). The classes bundle position and depth accuracy and seafloor coverage: A1 — position ±5 m + 5 % of depth, depth ±0.5 m + 1 % of depth, full seafloor search; A2 — ±20 m, ±1.0 m + 2 %, full search; B — ±50 m, ±1.0 m + 2 %, no full search (undetected features possible); C — ±500 m, ±2.0 m + 5 %; D — worse than C; U — not assessed (IHO S-57 Appendix A / S-4 B-297). On an ECDIS the classes display as a pattern of stars. Much of the world's charted water remains CATZOC C, D, or U — especially in polar, Pacific-island, and developing-nation waters — and the S-67 *Mariners' Guide to Accuracy of Depth Information in ENCs* (IHO 2020) explains to users what these classes mean for under-keel clearance. For the DEM practitioner, CATZOC is the chart world's per-area uncertainty layer and the model for how a product should carry its own confidence.

### 58.4.4 ENC, S-101, S-102, and overscale

The **S-57 ENC** (1990s–) is a vector dataset of objects (depth areas, soundings, contours, wrecks, buoys) with a fixed symbology defined by S-52. **S-101**, the S-100-based ENC product specification, replaces it; edition 1.0.0 was published in 2018 and the first operational edition, 2.0.0, in December 2024; the IMO performance standards (MSC.530(106), 2022) permit S-100-capable ECDIS from 1 January 2026, and S-101 ENCs can be issued alongside **S-102** bathymetric surface products (gridded depth plus uncertainty, derived from BAG; [Chapter 47](ch47-file-formats.md)), **S-104** water levels, and **S-111** surface currents. S-102 is the first time a hydrographic office delivers a DEM-like grid directly to the bridge, with its uncertainty, and S-102's own generalization rules (shoal-biased resampling to the product resolution) are the chart tradition applied to a raster. ECDIS raises an **overscale** indication when the display scale exceeds the ENC's compilation scale by a set factor, because the data were generalized for the smaller scale and the mariner must not read precision into enlarged symbols. The paper chart has the same limitation and no warning.

<!-- figure: Figure 58.2 — From multibeam grid to chart: (a) 1 m multibeam surface; (b) shoal-biased selected soundings at 1:20,000; (c) generalized isobaths with the 10 m contour displaced only seaward; (d) resulting depth areas with S-52 four-shade tints and CATZOC pattern overlay. -->

## 58.5 Aeronautical charts

Aeronautical charts depict terrain and obstacles so that pilots can keep above them; **ICAO Annex 4** (*Aeronautical Charts*) specifies the charts and **Annex 15** / PANS-AIM (Doc 10066) specifies the underlying **electronic terrain and obstacle data (eTOD)**. The elevation practitioner meets two things here: the rounding rules that make a chart elevation conservative, and the accuracy areas that eTOD divides the world into.

On US **sectional charts** (1:500,000), each 30′ × 30′ quadrangle carries a **Maximum Elevation Figure (MEF)**, printed as a large digit for thousands of feet and a small digit for hundreds. The FAA's rule (FAA *Aeronautical Chart Users' Guide*) is asymmetric by design: if the highest feature is a surveyed obstacle, the MEF is its elevation plus a 100 ft allowance for vertical error, rounded *up* to the next 100 ft; if the highest feature is terrain, the MEF is the terrain elevation plus 100 ft for source vertical error plus 200 ft for unsurveyed obstacles (natural or man-made below the obstacle-charting threshold), rounded up to the next 100 ft. A 4,850 ft summit therefore produces an MEF of 52 (5,200 ft). The MEF is not a safe altitude — it carries no clearance margin for flight — but it is a worked example of elevation-error allowances baked into a cartographic number. Charts depict terrain with hypsometric tints in feet, contours at scale-dependent intervals, and spot heights; obstacles above 200 ft AGL are symbolized with both MSL and AGL heights from the FAA **Digital Obstacle File** ([Chapter 59](ch59-vector-data.md) §59.5).

**eTOD** defines four areas around aerodromes with increasing accuracy demands. Approximately: Area 1 (the whole territory of a state) at 30 m vertical accuracy and 3″ post spacing; Area 2 (the terminal control area) at 3 m and 1″; Area 3 (the aerodrome movement area) at 0.5 m and 0.6″; and Area 4 (the Category II/III precision-approach area) at 1 m and 0.3″ (values per Annex 15 and PANS-AIM Doc 10066). These are among the few places where a national regulation prescribes DEM accuracy and post spacing directly, and they are the specification a terrain dataset must be validated against before it reaches a chart or a flight-management system. [Chapter 62](ch62-navigation-and-charting.md) and [Chapter 70](ch70-specifications-guided-tour.md) cover the surfaces and specifications in detail.

## 58.6 Graticule versus grid, and the three norths

A **graticule** is the network of meridians and parallels — lines of constant longitude and latitude — drawn on the map; its lines converge toward the poles and, on most projections, are curves. A **grid** is a rectangular network of lines of constant easting and northing in a projected coordinate system — UTM, MGRS squares derived from it, US State Plane, the British National Grid, Lambert-93 — and its lines are straight and perpendicular by construction. A topographic sheet usually shows both: a graticule (often only as corner coordinates and 2.5′ edge ticks on a 7.5′ sheet) and a full or ticked grid. A bearing measured against a grid line is a **grid bearing**, not a true bearing — a classic navigation error.

Three norths appear on the sheet. **True north** is the direction of the meridian. **Grid north** is the direction of the grid's northing axis, which equals true north only on the projection's central meridian; elsewhere they differ by the **grid convergence** $\gamma$, approximately $\gamma \approx \Delta\lambda \sin\varphi$ for a transverse Mercator zone, where $\Delta\lambda$ is the longitude difference from the central meridian. At the edge of a UTM zone (3° from the central meridian) at latitude 45°, $\gamma \approx 3° \times 0.707 \approx 2.1°$. **Magnetic north** is where the compass points; the **magnetic declination** between true and magnetic north varies from near zero along the agonic line to over 20° in parts of North America and changes by several minutes to a fraction of a degree per year. The **declination diagram** in the margin shows all three as rays from a point, states the angles, and states the *date* for which the declination is valid and usually its annual change. A sheet surveyed in 1965 with 17° E declination may be off by 2–4° today; a user who applies the printed value to a modern compass bearing will miss a target 1 km away by 35–70 m. Modern practice is to compute declination from the current World Magnetic Model (WMM, updated every five years, with an out-of-cycle update in early 2019) for the date of use.

**Neatlines, ticks, scale bars, and north arrows.** The neatline bounds the mapped area, usually along the graticule for topographic quadrangles (so it is not quite rectangular on the projection). Corner coordinates are printed in degrees–minutes–seconds; grid ticks carry abbreviated values (the principal digits, e.g. "⁴⁵12" for 4,512,000 m N) with the full value at one corner. A **scale bar** is more honest than a representative fraction because it survives photocopying and resizing, but on any projection it is exact only along certain lines; on Web Mercator the scale changes by $\sec\varphi$ and a scale bar drawn at one latitude is wrong at another on the same screen (at 60° N, by a factor of two). A north arrow should state which north it shows; on a conic or transverse projection true north rotates across the sheet and a single arrow is an approximation.

> **Worked example.** A field team uses a 1978 1:24,000 sheet in Oregon whose declination diagram reads 19° E (1978). The WMM for 2025 gives about 14.5° E at the same location (approximate). They measure a magnetic bearing of 062° to a ridge target 1.5 km away and plot it with the printed 1978 declination: true bearing = 062° + 19° = 081°. The correct conversion is 062° + 14.5° = 076.5°, so the plotted line is 4.5° in error, which at 1.5 km is 1,500 × tan 4.5° ≈ 118 m off the target. Had they also plotted against UTM grid lines without applying the sheet's grid convergence (a fraction of a degree to about 2° in UTM zone 10, depending on distance from the 123° W central meridian), the error would compound. Lesson: the declination diagram is dated information, and the grid–true difference is a separate correction.

## 58.7 Standard marginalia

Everything printed outside the neatline is evidence about the map inside it, and a map without it is an unsupported assertion. The standard set, present on every national-series topographic sheet and every chart:

| Element | What it tells the reader | Why it matters for elevation |
|---|---|---|
| Title, series, sheet number | Identity and position in the series | Links to the series specification and adjoining sheets |
| Edition, survey/compilation date(s), revision date | Epoch of the content | Terrain and shorelines change; contours have a date |
| Horizontal datum and projection/grid | How coordinates are defined | NAD27 vs NAD83: tens of metres of shift |
| **Vertical datum** | What zero means for every elevation shown | NGVD29 vs NAVD88; LAT vs MLLW: up to metres |
| Contour interval (and supplementary interval) | Vertical resolution and implied accuracy (NMAS) | Half the interval is the 90 % error bound |
| Declination diagram with date | True/grid/magnetic relationship at the time | Stale by degrees after decades |
| Scale (RF and bar) | Measurement ratio | Bars survive reproduction; RF does not |
| Sources / currency / reliability diagram | Where the content came from and how good it is | The map's own uncertainty map (source diagram, CATZOC) |
| Legend | Meaning of symbols | Depression ticks, supplementary contours, approximate contours |
| Adjoining-sheets index | Edge matching | Contour intervals can change across a sheet edge |
| Producer, copyright/licence, accuracy statement | Provenance and permitted use | "Complies with NMAS" is a legal-grade claim |

Two deserve emphasis. The **vertical datum** is the element most often missing from derived and thematic maps — and from nearly every web map — and the one that makes an elevation number mean something; a flood map labelled "2 m" without a datum cannot be compared to a gauge. The **reliability or currency diagram** admits that a map is a composite of sources of different ages and quality; charts have always had one, many topographic sheets had one, and database-derived products have largely replaced it with a "source" line in metadata that no reader sees. When you make a map from a DEM, put a source-and-accuracy panel in the margin: DEM name and version, acquisition date range, vertical datum and geoid model, assessed accuracy (NVA/VVA or RMSE with checkpoint count), and the contour interval's relationship to it.

## 58.8 Layout and generalization

Generalization is the cartographer's set of controlled lies — selection, simplification, smoothing, displacement, exaggeration, aggregation, typification — and each one trades positional truth for legibility. Monmonier (1996) is the standard account for readers; Robinson et al. (1995) and Kraak and Ormeling (2020) treat the craft. For elevation maps the specific decisions are these.

**Label placement.** Contour labels sit in the line (the line is broken for them), read uphill, and recur every 10–15 cm along index contours; spot heights are labelled to the right of the point; depth soundings *are* their labels and are positioned by the shoal-biased selection. Automated placement in QGIS or Mapnik handles 90 % of this; the remaining 10 % on steep slopes and in congested harbours is manual.

**Hydrography–contour consistency.** Streams must notch contours; lakes must be flat with a single shoreline contour; coastlines must coincide with the zero contour of the vertical datum used for land (which is *not* the chart datum used for depths — see the next paragraph). When the DEM is hydro-flattened to the same hydrography layer the map uses, these fall out automatically; otherwise, displace contours to the hydrography, not the reverse, because the hydrography is usually the better-surveyed line.

**Roads, buildings, spot heights.** At 1:24,000 roads are drawn at symbol width (0.5–1 mm, i.e. 12–24 m) and buildings as minimum-size squares; adjacent features are displaced to avoid overlap. Spot heights are selected for summits, passes, road junctions, and benchmarks, and their values must agree with the contours around them to within the interval; a DEM-derived spot height at a summit is a *maximum within the summit area*, not the DEM value at an arbitrary cell, and should be labelled with a precision no finer than the DEM justifies (whole metres for a 1 m lidar DTM).

**Relief integration.** Hypsometric tints and hillshade go under everything else at reduced contrast (hillshade opacity 30–50 %); contours go over the relief; labels get halos. The Swiss combination of shaded relief, rock drawing, and contours is the benchmark, and most of its effect comes from generalizing the relief itself ([Chapter 57](ch57-visualizing-dems.md) §57.2.6).

**The land–sea seam.** Coastal maps join a topographic DEM in orthometric height (e.g. NAVD88) to bathymetry in chart datum (MLLW), with a difference of a metre or more between the two zeros and a tidal zone that belongs to both. A single colormap across the seam is only honest if both datasets have been transformed to one datum (VDatum or equivalent; [Chapter 9](ch09-vertical-datums.md)); otherwise the map must show two legends and a visible seam, as charts do with the drying-height convention (heights above chart datum in the intertidal, underlined on the chart).

## 58.9 Web and dynamic maps

A web map's generalization changes with every zoom level, its legend is usually absent, and its margins are gone. The gain — one map that works at 1:500 and 1:50,000,000 — is real; so are the losses. **Zoom-dependent generalization** means the contours at zoom 12 are not the contours at zoom 16, and nothing tells the reader which were traced from which DEM at what interval; vector-tile schemas (OpenMapTiles, Mapbox Streets, Protomaps) include a contour layer with a `height` attribute, typically from SRTM or a national DEM, with the source and datum recorded only in the tileset metadata. **Legends vanish** because the stylesheet is the legend and nobody renders it; **datum and date** are in a JSON file no user opens. Terrain in web maps is delivered as RGB-encoded tiles with no datum ([Chapter 57](ch57-visualizing-dems.md) §57.6) or as 3D Tiles whose vertical reference is whatever the globe's is.

What to do about it: expose the metadata in the interface (a "data sources" panel with DEM name, date, datum, and accuracy, visible at one click); render a dynamic legend for any elevation or depth symbology; show the contour interval on screen whenever contours are visible; and make the **printable output** a real map — QGIS or MapLibre print plugins can emit a sheet with a neatline, scale bar valid at the print latitude, north arrow, and the marginalia of §58.7. A screenshot is not a map.

## 58.10 Map QA

A finished map should be checked as a product, independently of the DEM's accuracy assessment, by someone who did not make it. The checks group into four kinds.

**Topological.** Contours do not cross or touch; every contour either closes or ends at the neatline; depression contours enclose lower ground; isobaths move only seaward under generalization; depth areas tile the water without gaps or overlaps; each stream crosses each contour exactly once. PostGIS or GEOS validity checks and a line-intersection query find these in seconds ([Chapter 59](ch59-vector-data.md) §59.7).

**Consistency.** Spot heights agree with surrounding contours; summits labelled are local maxima of the DEM; rivers descend monotonically along their traced length (sample the DEM along each reach and flag positive gradients); the coastline coincides with the land vertical datum's zero; soundings are never deeper than the DEM minimum within their selection radius; the contour interval printed in the margin is the interval drawn; adjoining sheets match at the edge.

**Metadata.** Every item in the §58.7 table is present, correct, and consistent with the data's own metadata ([Chapter 49](ch49-metadata.md)): the datum stated is the datum of the DEM actually used (after any transformation), the date is the acquisition date rather than the publication date, and the declination is computed for the edition date.

**Accuracy statement and independent review.** The map's accuracy statement should trace to the DEM's assessment (checkpoints, NVA/VVA, date), with the contour-accuracy inference of §58.3 made explicit. Then a second cartographer or hydrographer reviews the sheet against a checklist ([Appendix G](../appendices/appendix-g-checklists.md)); charts undergo formal verification before release. For a one-off map from a DEM, a thirty-minute review by a colleague who tries to navigate with it finds more than any automated test.

> **Try it.** A fast consistency check that rivers descend. Expected result: a table of reaches whose sampled DEM elevation *rises* downstream by more than the DEM's vertical uncertainty; on a hydro-flattened lidar DTM with a current NHD, a few percent of reaches will flag, mostly at culverts, bridges, and misaligned digitizing — each is either a map error or a DEM error, and both belong in the QA log.
>
> ```python
> import geopandas as gpd, rasterio, numpy as np
>
> rivers = gpd.read_file("nhd_flowlines.gpkg").to_crs("EPSG:6339")  # UTM 10N, NAD83(2011)
> dem = rasterio.open("dtm_1m.tif")
> tol = 0.30  # ~2 x assessed NVA (m); below this, rises are noise
> bad = []
> for idx, row in rivers.iterrows():
>     line = row.geometry
>     d = np.arange(0, line.length, 10.0)                  # sample every 10 m
>     pts = [line.interpolate(s) for s in d]
>     z = np.array([v[0] for v in dem.sample([(p.x, p.y) for p in pts])])
>     rise = np.max(z[1:] - np.minimum.accumulate(z[:-1]))  # largest climb vs running min
>     if rise > tol:
>         bad.append((row["permanent_identifier"], round(float(rise), 2)))
> print(f"{len(bad)} of {len(rivers)} reaches climb > {tol} m downstream")
> print(sorted(bad, key=lambda t: -t[1])[:20])
> ```

<!-- figure: Figure 58.3 — Marginalia of a complete sheet annotated: title block, series and sheet number, edition and survey dates, horizontal and vertical datums, projection and grid, contour interval, declination diagram with date, scale bar, source and reliability diagrams, legend, adjoining-sheet index, producer and licence. -->

## Then & now

The national topographic survey is older than many nation-states. The **Cassini** family's map of France (1756–1815) was the first national triangulation-based survey ⟨H⟩; Britain's **Ordnance Survey** began in 1791 with the Principal Triangulation and published its first one-inch sheet (Kent) in 1801 ⟨H⟩. Relief on these sheets was hachured; contours came into general topographic use during the nineteenth century. The **USGS** began its topographic programme in 1879 ⟨H⟩, and the sheets of the next seventy years were plane-tabled in the field, with contours sketched by topographers reading the ground through an alidade.

**Photogrammetric compilation** displaced the plane table between the 1930s and the 1950s: stereo plotters (Multiplex, Kelsh, later analytical plotters) let an operator trace contours from aerial photography, with field checking reduced to names, classification, and the ground under trees. NMAS (1947) ⟨H⟩ was written for this process, and the 7.5′ series was completed under it. Nautical charts moved from lead-line fair sheets to echo-sounder and then multibeam surveys over the same decades, though much charted water still rests on the earlier work.

**DEM-derived cartography** arrived with national elevation databases. US Topo (2009–) draws its contours from 3DEP; OS, IGN, swisstopo, and LINZ moved to database-driven production in the 2000s–2010s; ENCs (S-57, 1990s–) replaced the paper chart as the legal carriage document on SOLAS vessels during the 2012–2018 ECDIS mandate, and S-101/S-102 (2020s) carry gridded bathymetry with uncertainty to the bridge. The map became a *view* of a database rather than an artefact, which is why edition dates, source diagrams, and datums — once printed on every sheet because the sheet was the only record — are now so easily lost in metadata nobody renders.

**Continuous, scale-less cartography** — vector tiles, S-101 on ECDIS, 3D globes — is the present. Its unsolved problem is exactly the one paper marginalia solved: how a reader knows what they are looking at, how old it is, what datum it is on, and how much to trust it, when the map is regenerated for every zoom level and no margin exists.

## Mathematics

**Marching squares.** For a cell with corner elevations $z_{00}, z_{10}, z_{01}, z_{11}$ and a contour level $c$, classify each corner as above or below $c$ to get one of 16 cases. On each edge whose endpoints straddle $c$, the crossing lies at the linear-interpolation fraction $t = (c - z_a)/(z_b - z_a)$ along the edge. The two saddle cases (corners alternately above and below) are ambiguous; the usual resolution compares the cell-centre mean $\bar z$ with $c$ and connects accordingly. Applying this rule consistently across the grid is what guarantees contours do not cross. The positional error of a contour vertex from DEM noise is, to first order, $\sigma_{xy} \approx \sigma_z / |\nabla z|$, so error is largest where slope is smallest (§58.3).

**Line generalization.** The **Douglas–Peucker** algorithm (1973) keeps the endpoint pair, finds the vertex farthest from their chord, and recurses on each side if that distance exceeds a tolerance $\epsilon$; every retained vertex lies within $\epsilon$ of the original line, so the positional error introduced is bounded by $\epsilon$ (but the algorithm can create self-intersections). **Visvalingam–Whyatt** (1993) iteratively removes the vertex whose *effective area* — the triangle formed with its two neighbours — is smallest, which preserves shape character better for the same vertex count and has a natural area-based tolerance. For contours, use $\epsilon \le 0.5\,\Delta x$ (half a cell), since the contour's own positional uncertainty is already about $\sigma_z/\tan\beta$; for isobaths, generalize and then enforce the shoal-bias constraint by moving the simplified line seaward of the original wherever it crossed inshore. [Chapter 59](ch59-vector-data.md) §59.9 treats generalization in detail.

**Grid convergence and scale factor.** For a transverse Mercator projection, the convergence angle (grid north minus true north) is to first order
$$\gamma \approx \Delta\lambda \,\sin\varphi \left(1 + \tfrac{1}{3}\Delta\lambda^2 \cos^2\varphi\,(1 + 3\eta^2)\right),$$
with $\Delta\lambda$ the longitude from the central meridian in radians and $\eta^2 = e'^2 \cos^2\varphi$; the leading term suffices for a declination diagram. The point scale factor is $k \approx k_0\,(1 + \tfrac{1}{2}\Delta\lambda^2 \cos^2\varphi)$, so with $k_0 = 0.9996$ a UTM zone's scale ranges from 0.9996 at the central meridian to about 1.0010 at its edges on the equator: a 10 km scale bar drawn at the edge is about 1.4 m longer than one at the centre — negligible on paper, significant in a GIS measurement.

**Maximum Elevation Figure.** With $h$ the highest feature in the quadrangle and allowance $a$ (100 ft for a surveyed obstacle; 100 ft of source error plus 200 ft for uncharted obstacles when the feature is terrain), the MEF in feet is $\mathrm{MEF} = 100 \lceil (h + a)/100 \rceil$. Note the ceiling, not rounding: the number may only err high.

**Sounding selection.** Let $S$ be the surveyed soundings with depths $d_i$ and positions $\mathbf{p}_i$, and let $r$ be the minimum legible separation at the compilation scale (for 1:20,000 and 2.5 mm label spacing, $r = 50$ m). Choose $T \subseteq S$ maximizing $|T|$ (or an information score weighting dangers and channels) subject to (i) legibility, $\|\mathbf{p}_i - \mathbf{p}_j\| \ge r$ for all $i \ne j \in T$, and (ii) shoal bias: for every omitted $s \in S \setminus T$ there exists $t \in T$ within radius $r$ with $d_t \le d_s$. The greedy solution — sort by depth ascending, accept each sounding whose disc of radius $r$ contains no accepted sounding, which satisfies (ii) automatically — is where most production systems start (Zoraster & Bayer 1992); the hydrographer's edit afterwards relaxes (i) near dangers and restores soundings that show the bottom trend.

## Validation & uncertainty

A map inherits the DEM's errors and adds its own. The error budget of a finished sheet has five components, and each is testable.

> **Uncertainty budget.** Contribution to the horizontal position of a 10 m contour on a 1:25,000 topographic sheet made from a 1 m lidar DTM (NVA 0.15 m at 95 %, i.e. σ_z ≈ 0.08 m), on a 3° slope.
>
> | Component | Mechanism | Magnitude (1σ, horizontal) |
> |---|---|---|
> | DEM vertical error | σ_z / tan β | 0.08 / 0.052 ≈ 1.5 m |
> | DEM horizontal error | lidar georeferencing | ≈ 0.3 m |
> | Smoothing before tracing | 2-cell Gaussian shifts the contour on asymmetric slopes | ≤ 1 m (test by differencing smoothed and raw contours) |
> | Line simplification | DP tolerance 0.5 m | ≤ 0.5 m (bounded) |
> | Cartographic displacement | moving the line clear of a road symbol | 0–0.3 mm at scale = 0–7.5 m, local and deliberate |
> | Total (RSS, excluding displacement) | | ≈ 1.9 m, i.e. 0.08 mm at scale |
>
> The same contour on a 10° slope has 0.45 m of DEM-induced error and the generalization terms dominate; on a 0.5° floodplain it has 9 m and nothing else matters. Displacement is not an error in the statistical sense but must be documented, because a user measuring from the sheet cannot distinguish it from one.

**Testing contours against checkpoints.** The NMAS vertical test is still the practical one: take the independent checkpoints used for the DEM's NVA/VVA ([Chapter 53](ch53-accuracy-assessment.md)), interpolate the map elevation at each from the *contours* (not the DEM), and count the fraction whose error exceeds half the interval; the standard permits shifting the checkpoint by the horizontal tolerance first. Report the result alongside the DEM's own NVA, because they can differ: a 2 m interval drawn from a DEM with 0.6 m RMSE in vegetation will fail the contour test even though the DEM "passed" at 95 % in open terrain. For charts, the test is the S-44 TVU on the source survey ([Chapter 70](ch70-specifications-guided-tour.md)) plus a specific check that no selected sounding or generalized isobath lies deeper than any omitted survey depth within the selection radius — a query, not a statistic, and one that must return zero.

**Testing generalization.** Difference the generalized and ungeneralized line sets: the Hausdorff distance per contour, the signed area between isobath versions (which must lie entirely on the seaward side), and the change in enclosed area of closed contours. Any contour whose Hausdorff distance exceeds the stated tolerance has been moved by something other than simplification — usually a label-avoidance or displacement rule — and should be reviewed.

**Testing the margins.** Three numbers in the margin are computable and therefore checkable: the declination (recompute from the current WMM or IGRF for the sheet centre and edition date; disagreement above about 0.5° means the diagram is stale or mislabelled), the grid convergence (recompute from the projection), and the scale-bar length (measure it in the layout against projected coordinates at the sheet centre). Datum statements are checked by comparison, not computation: overlay a feature of known coordinates (a survey monument from the national database) and confirm the sheet places it where its stated datum says.

> **Worked example.** A county publishes a 1:10,000 flood-information map with 0.5 m contours from a 2 m DEM whose metadata states NVA = 0.49 m (95 %), i.e. RMSE ≈ 0.25 m. The contour test requires 90 % of checkpoints within ±0.25 m; for Gaussian errors with σ = 0.25 m only about 68 % will be. The map fails NMAS logic before any field check. The minimum interval the data support is ≈ 3 × 0.25 = 0.75 m, so 1 m contours — with the 0.5 m lines dropped or restyled as "indicative" — is the honest product. The legend should read: "1 m contours derived from 2 m DEM (2019), NVA 0.49 m; contours on slopes below 1° are indicative only."

**What to report.** The map's own accuracy statement (contour-test result or NMAS-style compliance; for charts, CATZOC or equivalent), the DEM with its assessed accuracy and date, the generalization tolerances, the datums with any transformation applied, the declination date, and the name of the reviewer. A map that states these can be wrong in a known way; one that does not is wrong in an unknown way.

## Software

**Open source:** QGIS (print layouts with graticules, grids, scale bars, and expression-driven north arrows; contouring and label placement; atlas generation for sheet series); GDAL (`gdal_contour` with `-p` polygon output and `-amin/-amax` fields for depth areas; `gdaldem` for shading; S-57 vector driver for reading ENCs — read-only); GRASS GIS (`r.contour`; `v.generalize` with Douglas–Peucker, Visvalingam, and topology-preserving options; `ps.map`); SAGA; GMT (`grdcontour`, `coast`, `basemap` frames and graticules — the publication standard in geophysics); Mapnik and MapServer (tile/WMS rendering of contour and relief layers); OpenCPN (ENC and raster-chart display; useful for seeing what a mariner sees); NOAA `s100py` (read/write S-102, S-104, S-111 HDF5); `pyIGRF` and similar libraries for declination. **Free but closed:** NOAA's online ENC viewer; USGS topoView and The National Map viewers for HTMC and US Topo. **Commercial:** ArcGIS Pro with Production Mapping and Maritime extensions (sounding selection, S-57/S-101 production, cartographic displacement — complete but costly); CARIS HPD and S-57 Composer (hydrographic-office standard for ENC compilation; automated sounding selection still requires the hydrographer's review); dKart and SevenCs (ENC production and ECDIS kernels); Global Mapper (quick contours and layouts; limited cartographic control); Avenza MAPublisher with Adobe Illustrator (fine cartographic finishing; georeferencing is easily lost in editing).

## Standards & guides

- **US Bureau of the Budget, 1947.** *United States National Map Accuracy Standards* ⟨H⟩. The 90 %/half-interval and 1/30″–1/50″ rules that define legacy map accuracy.
- **USGS, 2017.** *Standard for the U.S. Geological Survey Topographic Map* (successor to the 2011 *US Topo Product Standard*), Techniques and Methods 11-B2. Content, sources, symbology, and marginalia.
- **USGS, 2015 (verify).** *Topographic Mapping* — general-interest publication on USGS topographic mapping history and methods.
- **ASPRS, 2014 (edition 2, 2023).** *Positional Accuracy Standards for Digital Geospatial Data*. Replaces NMAS for digital products; contour accuracy inferred from DEM NVA/VVA.
- **IHO S-4, edition 4.9.0 (2021).** Chart specifications: soundings, contours, tints, source diagrams, generalization.
- **IHO S-52, edition 6.1.1 (2015) with Presentation Library 4.0.x.** ECDIS presentation library; safety contour and depth shades.
- **IHO S-57, edition 3.1 (2000) with supplements; IHO S-101, edition 1.0.0 (2018) to 2.0.0 (December 2024).** ENC product specifications; CATZOC in S-57 Appendix A and its S-101 successor.
- **IHO S-102, edition 3.0.0 (2024).** Bathymetric Surface Product Specification; gridded depth and uncertainty for ECDIS overlay.
- **IHO S-67, edition 1.0.0 (2020).** Mariners' guide to accuracy of depth information in ENCs.
- **ICAO Annex 4** (*Aeronautical Charts*, 11th ed. 2009 with amendments) and **Annex 15 / PANS-AIM Doc 10066.** Chart content and eTOD area accuracy requirements.
- **FAA, current edition.** *Aeronautical Chart Users' Guide.* MEF rules and terrain/obstacle symbology.
- **FGDC-STD-011-2001** (*United States National Grid*) and **FGDC-STD-013-2006** (*Digital Cartographic Standard for Geologic Map Symbolization*).
- **Ordnance Survey and IGN cartographic specifications** (published legend sheets and symbol specifications for Explorer/Landranger and TOP 25).

## Pitfalls

- **Omitting the vertical datum from a map that shows elevations** → the producer assumed "elevation" is self-explanatory → every elevation map must state the vertical datum and realization (NAVD88 via GEOID18; LAT; MLLW with epoch); reject maps without it.
- **Stale declination** → the diagram was copied from a previous edition or computed for the survey date → recompute from WMM/IGRF for the edition date and print date and annual change.
- **Grid north treated as true north** → bearings measured against UTM lines → print the convergence angle in the declination diagram and label the grid; in software, compute bearings geodesically.
- **Contour interval finer than the DEM justifies** → the software will draw anything → apply the 3 × RMSE rule, run the NMAS contour test with independent checkpoints, and label supplementary contours as indicative.
- **Chart generalization that is not shoal-biased** → a generic smoothing or simplification algorithm was applied to isobaths or soundings → difference generalized and source lines and require the signed area to be entirely seaward; require zero omitted soundings shoaler than any selected neighbour.
- **Depth-area polygons that do not tile the water** → contours were converted to areas without snapping → run a coverage check (no gaps, no overlaps) before export; ECDIS behaviour in a gap is undefined.
- **Overscale use of a small-scale chart or map** → screens remove the physical scale cue → carry the compilation scale in metadata and display it; ECDIS warns, GIS does not.
- **Web maps with no edition date or source currency** → metadata is in the tileset JSON and never rendered → build a sources panel and a dynamic legend into the interface; treat absence as a defect.
- **Mixing feet contours with metric spot heights** → legacy contour layers combined with a modern DEM → one unit per map; convert, state the conversion, and check that labelled summits sit inside the correct contour.
- **Staircase DEM contoured at a new interval** → the DEM was itself made from contours → inspect the elevation histogram for spikes at round values and use a different source or the original contours.
- **Depression contours without hachures** → the closed-low test was not run → compare inside/outside elevations for every closed contour; sinkholes and pits drawn as hills are a classic QA failure.
- **Contours disagreeing with hydrography** → DEM and vector water from different dates or sources → sample the DEM along streams and shores; decide which dataset governs and record the decision.
- **A scale bar valid at one latitude on a Web Mercator layout** → the layout tool draws a bar for the centre → use a regional conformal or equal-area projection for print, or label the bar's latitude.
- **Datum mismatch across the land–sea seam** → topography on NAVD88, bathymetry on MLLW, one continuous colour ramp → transform both to one datum (VDatum) or show two legends and the seam explicitly.

## Key takeaways

- A map is a claim and its marginalia — datums, dates, projection, contour interval, sources, accuracy — are the evidence; a map without them is a picture.
- Scale is three things (representative fraction, compilation scale, source scale); the smallest bounds what the map may honestly assert.
- Contours inherit the DEM's vertical error divided by slope, plus generalization; choose an interval ≥ 3 × RMSE, test against independent checkpoints, and label indicative lines as such.
- At sea every generalization step is shoal-biased by rule — soundings, isobaths, rounding, S-102 resampling may only err toward shallower; verify with queries that must return zero.
- CATZOC, source diagrams, and the US Topo elevation-source statement are the map world's per-area uncertainty layers; carry them into derived products.
- Grid, true, and magnetic north differ by computable, dated angles; print the date and recompute for each edition.
- Database-driven cartography gains currency and loses field checking and visible margins; restore the margins in the interface.
- QA a map as a product: topology, consistency with the DEM, correct marginalia, an accuracy statement traceable to the DEM's assessment, and an independent reviewer who tries to use it.

## References

- Brewer, C. A. (2015). *Designing Better Maps: A Guide for GIS Users* (2nd ed.). Esri Press.
- Douglas, D. H., & Peucker, T. K. (1973). Algorithms for the reduction of the number of points required to represent a digitized line or its caricature. *The Canadian Cartographer*, 10(2), 112–122.
- Federal Aviation Administration (current edition). *Aeronautical Chart Users' Guide*. FAA Aeronautical Information Services.
- Federal Geographic Data Committee (2001). *United States National Grid*, FGDC-STD-011-2001.
- Federal Geographic Data Committee (2006). *Digital Cartographic Standard for Geologic Map Symbolization*, FGDC-STD-013-2006.
- Fishburn, K. A., Davis, L. R., & Allord, G. J. (2017). *Standard for the U.S. Geological Survey Topographic Map*. USGS Techniques and Methods 11-B2.
- Imhof, E. (1982). *Cartographic Relief Presentation* (H. J. Steward, Ed.). Walter de Gruyter. (Reissued Esri Press, 2007.)
- International Civil Aviation Organization (2009, with amendments). *Annex 4 — Aeronautical Charts* (11th ed.).
- International Hydrographic Organization (2000). *S-57: IHO Transfer Standard for Digital Hydrographic Data*, edition 3.1.
- International Hydrographic Organization (2020). *S-67: Mariners' Guide to Accuracy of Depth Information in an Electronic Navigational Chart*, edition 1.0.0.
- International Hydrographic Organization (2021). *S-4: Regulations of the IHO for International (INT) Charts and Chart Specifications of the IHO*, edition 4.9.0.
- Jenny, B., Jenny, H., & Hurni, L. (2011). Terrain generalization with multi-scale pyramids constrained by curvature. *Cartography and Geographic Information Science*, 38(1), 110–116.
- Kraak, M.-J., & Ormeling, F. (2020). *Cartography: Visualization of Geospatial Data* (4th ed.). CRC Press.
- Monmonier, M. (1996). *How to Lie with Maps* (2nd ed.). University of Chicago Press.
- Moore, L. (2011). US Topo — a new national map series. *Directions Magazine*, May 2011.
- Robinson, A. H., Morrison, J. L., Muehrcke, P. C., Kimerling, A. J., & Guptill, S. C. (1995). *Elements of Cartography* (6th ed.). Wiley.
- Snyder, J. P. (1987). *Map Projections — A Working Manual*. U.S. Geological Survey Professional Paper 1395. ⟨H⟩
- U.S. Bureau of the Budget (1947). *United States National Map Accuracy Standards*. Washington, DC.
- U.S. Geological Survey (2015). *Topographic Mapping*. USGS General Information Product. (verify)
- Visvalingam, M., & Whyatt, J. D. (1993). Line generalisation by repeated elimination of points. *The Cartographic Journal*, 30(1), 46–51.
- Zoraster, S., & Bayer, S. (1992). Automated cartographic sounding selection. *International Hydrographic Review*, 69(1), 57–61.

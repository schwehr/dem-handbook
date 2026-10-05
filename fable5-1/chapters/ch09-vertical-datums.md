# Chapter 9 — Vertical datums: orthometric, ellipsoidal, tidal, and home-made

> **Part III — Where is "here"? Geodesy, datums, projections.** With the geoid ([Chapter 7](ch07-shape-of-the-earth.md)) and the horizontal frames ([Chapter 8](ch08-horizontal-datums.md)) in place, this chapter deals with the zero of the height axis — the single most common source of gross error when elevation products are merged.

**In this chapter.** Every DEM has a zero, and the zeros disagree. National orthometric datums are offset and tilted relative to one another and to the geoid; tidal datums are 19-year averages at gauges that change with every epoch update; ellipsoidal heights are stable but unlike anything a user wants; and a surprising fraction of engineering, mining, and legacy data sits on datums someone made up on a Tuesday. After this chapter you will be able to name the realization and epoch of any vertical datum you meet, compute a tidal datum from gauge data, write the separation equation linking the ellipsoid to a chart datum, use VDatum-style transformation chains with their uncertainty, and recognize the failure modes of home-made datums before they cost you a merge, a change-detection study, or a lawsuit. The running theme is the coast, where three height systems meet within a few hundred metres and disagree by metres.

## 9.1 National orthometric datums

A **national vertical datum** is a realization of "height above the geoid" by a specific network of benchmarks, a specific adjustment, and a specific definition of zero. Each of those three choices leaves fingerprints.

**NGVD29 → NAVD88 → NAPGD2022 (United States).** The **Sea Level Datum of 1929** (renamed NGVD29 in 1973) adjusted about 100 000 km of levelling with 26 tide gauges (21 in the United States, 5 in Canada) held fixed at their local mean sea level. Because local MSL differs from the geoid by the mean dynamic topography ([Chapter 7](ch07-shape-of-the-earth.md), §7.7) — the Pacific coast sea level stands about 0.5–0.7 m higher than the Atlantic in geopotential terms — forcing all 26 to zero warped the network. **NAVD88** (Zilkoski, Richards & Young 1992) fixed a single point, Father Point/Rimouski on the St. Lawrence estuary, and adjusted about 625 000 km of levelling with observed-gravity Helmert orthometric corrections. The NGVD29→NAVD88 difference ranges from about −0.4 m on parts of the east coast to about +1.5 m in the Rocky Mountains; NGS's VERTCON grid models it to roughly 2 cm (1σ) where levelling is dense. NAVD88 in turn is now known — from GRAV-D-era geoids and GNSS — to be offset from the $W_0$ geoid by about 0.5 m at its origin and tilted by about a metre from the Pacific northwest to the southeast (NGS Blueprint Part 2 gives the maps; the figures are approximate). **NAPGD2022** replaces it with heights defined as $h - N_{GEOID2022}$ (Chapter 7, §7.4.1), eliminating the levelling-network definition; the NAVD88→NAPGD2022 change will be decimetres and spatially smooth, and NGS will publish a transformation grid with uncertainties.

**CGVD28 → CGVD2013 (Canada).** CGVD28 was a 1928 levelling adjustment with MSL fixed at several coastal gauges; CGVD2013 is defined as the equipotential surface $W_0 = 62\,636\,856.0$ m² s⁻² (the value then adopted, slightly different from the 2015 IAG value) realized by the gravimetric geoid CGG2013a (Véronneau & Huang 2016). The CGVD28→CGVD2013 differences are decimetres across the country, with the largest departures in the west and north where CGVD28 levelling was sparse or absent; NRCan publishes the difference grid.

**ODN (Great Britain).** Ordnance Datum Newlyn is MSL at Newlyn, Cornwall, over 1915–1921, carried by the geodetic levellings; the network's apparent south–north tilt of about 0.2 m has been debated — Penna et al. (2013) attribute most of it to levelling error rather than real sea slope. OSGM15 is fitted to ODN and reproduces it, tilt included.

**NAP (Netherlands) and TAW (Belgium).** Normaal Amsterdams Peil descends from the 1684 Amsterdam gauge zero, is the origin of EVRF, and has been re-adjusted (NAP 2005) and corrected for benchmark subsidence. Belgium's **TAW** zero is approximately mean low water at Ostend and lies about **2.3 m below NAP** — a step that runs straight through Zeeland-Flanders in any untransformed cross-border DEM.

**DHHN2016 (Germany), EVRF2019 (Europe).** The German DHHN2016 is a **normal-height** system based on the 2006–2012 re-levelling and the GCG2016 quasigeoid; EVRF2019 (the European Vertical Reference Frame realized through the United European Levelling Network) is likewise in normal heights, zero-tide, with the NAP origin, and is published in both zero-tide and mean-tide versions. The national-to-EVRF offsets range from centimetres (Netherlands) to over 0.5 m (Belgium, −2.3 m the other way; Scandinavia with land-uplift corrections), and BKG publishes the per-country offsets.

**AHD (Australia).** The Australian Height Datum (1971) held MSL at 30 tide gauges around the coast fixed at zero over 1966–1968. The result inherited the MDT difference around the continent — sea level is higher in the north — and is tilted by roughly 0.5–0.7 m from south to north, with additional distortions from the one-way third-order levelling that formed much of the network (Featherstone & Filmer 2012). AUSGeoid2020 is fitted to AHD and reproduces it; users needing a geoid rather than AHD use the gravimetric AGQG2017.

**NZVD2016 (New Zealand).** Replaced thirteen local MSL-based datums with a single quasigeoid-based datum (NZGeoid2016), offsets to the old datums ranging from about −0.1 to +0.5 m by region (LINZ publishes the per-datum offsets).

The pattern: levelling-based datums carry MDT-induced tilts of 0.2–1 m at continental scale plus local distortions of decimetres; geoid-based datums (CGVD2013, NZVD2016, NAPGD2022) remove the levelling errors but inherit the geoid model's error pattern ([Chapter 7](ch07-shape-of-the-earth.md)). Either way, the datum is a surface with structure, not a constant, and the transformation between any two is a grid, not a number.

<!-- figure: Figure 9.1 — Map of CONUS showing the NGVD29→NAVD88 difference (VERTCON) contoured from −0.4 m to +1.5 m, overlaid with the NAVD88→NAPGD2022 expected change pattern (schematic). -->

## 9.2 Ellipsoidal heights as a working datum

GNSS delivers ellipsoidal heights $h$ directly, repeatably, and without reference to any geoid or gauge. For a *survey*, as opposed to a *product*, that is a virtue: an **ellipsoidally referenced survey (ERS)** keeps every observation in $h$ throughout acquisition and processing, and only at the end reduces to the orthometric or tidal datum the user wants, via a separation model. Hydrographers formalized this (Dodd & Mills 2011; FIG Publication 62) because it removes the water-level observation from the sounding reduction chain: instead of depth = (observed depth) − (tide at the time, interpolated from a gauge), depth below chart datum = (ellipsoidal height of the seabed, from GNSS-positioned sonar) − (ellipsoid-to-chart-datum separation at that place), and the tide gauge is no longer needed in real time.

The cost of ERS is that the **separation model** becomes the critical dependency: its errors go straight into the product, and it must exist where you work. Offshore, beyond the coverage of a hybrid geoid or VDatum, that is not guaranteed; in estuaries the separation can vary by decimetres over a few kilometres.

> **Rule of thumb.** Store and archive ellipsoidal heights with frame and epoch; deliver whatever the user asks for; never archive *only* the reduced heights. A product in $h$ can be re-reduced to any future datum (NAPGD2022, the next tidal epoch, a revised chart datum) with a grid; a product in NAVD88 via GEOID12B cannot be improved without re-doing the reduction, and in ten years nobody will remember which grid version was used. This rule fails only when the GNSS trajectory itself is the weak link (poor PPK, [Chapter 12](ch12-gnss.md)), in which case neither $h$ nor $H$ is trustworthy.

## 9.3 Tidal datums

A **tidal datum** is a vertical reference defined by a statistic of observed water levels at a place. The common ones:

| Datum | Definition (NOAA usage) | Typical use |
|---|---|---|
| MSL | Arithmetic mean of hourly heights over the epoch | Reference for MDT, long-term sea-level; land datums historically |
| MTL | Mean of MHW and MLW | Legal in some jurisdictions |
| MHW | Mean of all high waters over the epoch | US shoreline (legal boundary in most states) |
| MHHW | Mean of the higher of the two daily highs | Upper tidal datum; inundation mapping |
| MLW | Mean of all low waters | Older US charts (Atlantic) |
| MLLW | Mean of the lower of the two daily lows | US chart datum since 1980 (all coasts) |
| MLWS | Mean low water springs | Older chart datum in UK/Commonwealth |
| LAT / HAT | Lowest/Highest astronomical tide: extreme predicted levels under average meteorological conditions over the nodal cycle | IHO-recommended chart datum (LAT); vertical clearance (HAT) |

Because tidal amplitudes are modulated by the 18.61-year regression of the lunar nodes (plus the 8.85-year perigee cycle), averages must span a full cycle: NOAA's **National Tidal Datum Epoch (NTDE)** is a 19-year period, **1983–2001** for the datums officially in use as of this writing; NOAA has analysed the **2002–2020** period and plans to adopt the next NTDE later in the decade (about 2029, per NOAA CO-OPS). The epoch change is not cosmetic: with relative sea-level rise of 2–4 mm/yr on most US coasts, the new MLLW is about 5–9 cm higher than the old one at a typical gauge, and more where subsidence is fast. For such places NOAA uses **modified epochs** — five-year averages adjusted to the NTDE — in the western Gulf of Mexico (Louisiana, Texas) and parts of Alaska, where land motion of 10 mm/yr or more would otherwise make a 19-year mean obsolete before it was published. A chart datum therefore has an epoch, and "MLLW" without one is as incomplete as "WGS84" without a realization.

### 9.3.1 Computation at gauges

At a **control station** with 19 years of hourly data, the datums are computed directly from the tabulated highs and lows. Nearly every other station is a **subordinate** with months to a few years of record, and its datums are computed by **simultaneous comparison** with a control station: for the simultaneous period, the mean difference in MSL and the ratios of mean ranges between the two stations are computed, and these are applied to the control's accepted 19-year values to obtain *equivalent* 19-year datums at the subordinate (NOAA 2003, *Computational Techniques for Tidal Datums Handbook*). The Mathematics section gives the formulas. The method's accuracy depends on the series length and the similarity of the two stations' tides: NOAA's guidance puts the uncertainty of datums from a one-month series at roughly 3–8 cm, from one year at 1–3 cm, and the method degrades badly if the control is in a different tidal regime (semidiurnal control for a mixed subordinate, for example).

### 9.3.2 Zoning across a survey

A survey covers an area; a gauge measures a point. Between gauges the datum and the instantaneous water level both vary — in range, in phase, and in the shape of the tidal curve — and the hydrographer must model the variation. Classical **discrete tidal zoning** divides the survey area into polygons, each with a time offset and range ratio relative to a gauge; its error is the step between zones, typically 5–15 cm. **TCARI** (Tidal Constituent And Residual Interpolation, Hess 2003) instead interpolates harmonic constituents, residuals, and datums spatially by solving Laplace's equation over the water body with gauges as boundary conditions, producing a continuous field; NOAA uses it for its own surveys and inside VDatum. Hydrodynamic models (ADCIRC, in VDatum) give the datum fields in areas with no gauges, at the cost of model error that NOAA quantifies regionally (§9.7).

<!-- figure: Figure 9.2 — Tidal datums at a mixed-tide gauge: one month of hourly water levels with MHHW, MHW, MSL, MLW, MLLW and LAT marked; inset showing the 18.6-year nodal modulation of range at the same gauge. -->

## 9.4 Chart and sounding datums

A **chart datum** (CD) is the surface below which depths on a nautical chart are measured and above which drying heights and some clearances are given. The IHO recommends (Technical Resolution A2.5) a datum "so low that the tide will seldom fall below it", and since 1997 recommends **LAT** specifically; most IHO member states use LAT or something close to it (the UK, Australia, much of Europe). The United States uses **MLLW** (since 1980 on all coasts; previously MLW on the Atlantic and Gulf), Canada uses **Lower Low Water Large Tide (LLWLT)**, and some states retain historical datums (Indian Spring Low Water, approximately LAT, in parts of Asia). The practical differences are not small: LAT is typically 0.1–0.5 m below MLLW in semidiurnal regimes, more where the range is large, and MLLW is below MLW by the diurnal inequality. In non-tidal waters (the Baltic, the Great Lakes, rivers) the chart datum is a fixed level (Baltic: a national height system; Great Lakes: **Low Water Datum** on IGLD 1985 per lake, e.g. 183.2 m for Lake Superior).

**Reduction of soundings.** Traditionally: $d_{CD} = d_{obs} - WL(t) + \text{(draft, squat, heave, sound-speed corrections)}$, where $WL(t)$ is the water level above CD at the sounding time and place. The water-level term can be **predicted** (from harmonic constants), **observed** at a gauge and zoned, or eliminated by **ERS** (§9.2). Predicted tides differ from observed by the **non-tidal residual** — wind setup, atmospheric pressure (about 1 cm per hPa), river discharge, seiches — which is routinely 0.1–0.3 m and exceeds 1 m during storm surges; the IHO S-44 budget ([Chapter 70](ch70-specifications-guided-tour.md)) requires an observed or modelled water level for Special Order and Exclusive Order work. **Dynamic draft** (squat and settlement, which depend on speed and depth under keel) can reach 0.1–0.3 m on a launch at survey speed and must be measured, not assumed; it is one of the larger systematic terms in a shallow-water TVU budget.

> **Definitions that bite.** "LAT" is a *predicted* extreme over a nodal cycle under average meteorological conditions, computed from the harmonic constants at a gauge; two agencies with different constituent sets or prediction periods get different LATs at the same gauge, by several centimetres. "MLLW" is an *observed* mean over a specific epoch. A product that says "depths relative to LAT" from a European source and one that says "MLLW" from a US source cannot be merged by assuming either is zero; the difference is a surface with decimetre variation. The IHO S-100/S-104 framework carries water-level and datum information explicitly for this reason.

## 9.5 Lake, river, and project datums

**IGLD 1985.** The International Great Lakes Datum uses **dynamic heights** ([Chapter 7](ch07-shape-of-the-earth.md), §7.3) with zero at Rimouski, because only dynamic heights make a level lake surface read as one number from end to end; the orthometric height of Lake Superior's surface varies by roughly 0.2 m over its length for a constant dynamic height (Coordinating Committee 1995; approximate). IGLD is re-realized roughly every 25–35 years because glacial isostatic adjustment tilts the basin: the northeast rises relative to the southwest by several millimetres per year, so gauge zeros drift relative to the water. IGLD 1955 → IGLD 1985 → the forthcoming IGLD 2020. Lake-level data, shoreline rules, and hydraulic structures are all specified in IGLD; anyone merging a terrestrial DEM in NAVD88 with lake bathymetry or shoreline elevations in IGLD 1985 must convert through the dynamic-height relation, and the difference ranges from a few centimetres to about 0.3 m across the basin.

**River gauges and stage.** A river gauge reports **stage**, the water level above the **gauge datum**, which is an arbitrary local zero chosen so that stage is never negative; the USGS publishes, for each gauge, the datum's elevation in NGVD29 or NAVD88 — when it is known. Many gauge datums were established by levelling from benchmarks that have since been destroyed, moved, or re-adjusted, and the published conversion can be in error by decimetres. Flood-inundation mapping that combines gauge stage with a lidar DEM depends entirely on that one number; checking it against a water-surface elevation extracted from the lidar on the survey date ([Chapter 34](ch34-water-in-dems.md)) is the single most valuable validation step in such a project.

**"Assumed elevation 100.00."** Construction, mining, and plant surveys commonly begin by assigning an arbitrary round elevation to a convenient monument so that all site elevations are positive and the design drawings are simple. Mine grids add an arbitrary horizontal origin and often a rotation and a scale factor of exactly 1 (a "ground" grid, [Chapter 10](ch10-projections-and-resampling.md)). These datums are perfectly fit for their purpose for the life of the project; they become a problem when the site's data must be merged with anything from outside — a regional DEM, a flood model, a neighbouring property, a reclamation bond survey decades later.

**RTK "site calibration" / "localization."** GNSS field software can fit a horizontal similarity transformation and a vertical plane (offset plus two tilts) between the GNSS frame and whatever coordinates the site's monuments have. This is how a crew makes modern GNSS agree with a 1970s mine grid in ten minutes. The danger is that the vertical plane absorbs *everything* — the geoid slope, the old datum's errors, a blundered benchmark — and extrapolates it linearly beyond the calibration points. A calibration from four marks on one side of a site can be wrong by decimetres on the other side, and the file that stores it is often not delivered with the data.

**Island, legacy, and "sea level" datums.** Islands and remote territories often have a vertical datum defined by one gauge over one short period (Guam, American Samoa, and the Hawaiian islands each had their own; many Pacific and Caribbean states still do): well defined at the gauge, undefined elsewhere except through local levelling, and connected to the ellipsoid only by GNSS on the gauge benchmark. A product "relative to sea level" without a gauge and epoch — the case for most pre-1990 topographic maps — is relative to something within about ±1 m of the geoid (MDT, [Chapter 7](ch07-shape-of-the-earth.md)) plus sea-level rise since the unnamed epoch; only historical research into the mapping agency's gauge and levelling line improves on that.

## 9.6 What happens when people create their own datums

People create datums because it is faster than connecting to the national network (a connection may require a day of GNSS observations or kilometres of levelling), because the nearest control is far away or destroyed, because the engineering or legal context requires a stable local system that will not change when the nation adjusts its datum, or simply from habit — every site has always had its own grid. All of these reasons are locally rational, and the costs arrive later, to other people:

- **Merging and change detection.** A project DEM on an assumed datum cannot be placed in a regional product without a transformation nobody computed; the usual recovery — estimating an offset from overlapping road surfaces or building pads — is good to decimetres and blind to tilt. A 2008 pre-mining survey on "assumed 100.00" and a 2024 reclamation survey on NAVD88 via GEOID18 can be compared only through monuments that survived sixteen years of earthmoving; if none did, a volume change that may be the basis of a bond release has an uncertainty dominated by a datum offset that may be metres.
- **Liability.** Floodplain elevation certificates, building permits, and boundary cases hinge on heights in a legally recognized datum; a structure certified against "assumed" or an unstated local datum has no defensible elevation.
- **Staff turnover.** The person who knew which monument was 100.00, and whether it was later disturbed, leaves. The datum then exists only as a number in a drawing title block.

Doing it safely costs little when done at the start and a great deal later:

1. **Tie to national control at two or more marks** (three or more if a tilt is to be controlled), with GNSS observations long enough for a few-centimetre ellipsoidal height (NGS-58/59 procedures or national equivalents), and keep the raw observations.
2. **Publish the transformation** — offset, and tilt if any — between the project datum and the national datum (horizontal and vertical, with frame, realization, geoid model, and epoch), in the project metadata and on the drawings.
3. **Keep ellipsoidal heights in parallel.** Deliver and archive the GNSS-derived $h$ for every control point and, where feasible, for the point cloud itself. Whatever happens to the project datum or the national one, $h$ in a stated frame and epoch can be recovered.
4. **Monument durably and describe.** The monuments carrying the project datum need witness descriptions and photographs; a datum that cannot be re-occupied cannot be re-connected.
5. **Date everything.** An epoch for the GNSS frame, the geoid model version, and the tidal epoch if any tidal datum is involved.

> **Case file.** Eakins & Grothe (2014) describe building coastal DEMs for tsunami inundation modelling from dozens of sources and list the vertical-datum problems encountered: bathymetry on MLLW or MLW of unknown epoch, topography on NGVD29 or NAVD88, lidar on ellipsoidal heights, and legacy soundings with no datum statement at all. Their examples include offsets of 1–2 m between adjacent datasets at the shoreline and shorelines that did not coincide with the zero contour of the merged DEM until each source was transformed through VDatum to a common datum. The paper's practical conclusion is that datum conversion, not interpolation, is the dominant task — and the dominant error — in coastal DEM compilation.

## 9.7 Vertical transformations

Converting between vertical datums means evaluating a **separation surface** between them at the point of interest. The surfaces come in three kinds: geoid or hybrid-geoid grids (ellipsoid ↔ orthometric; [Chapter 7](ch07-shape-of-the-earth.md)), datum-to-datum grids between orthometric realizations (VERTCON for NGVD29↔NAVD88; the CGVD28↔CGVD2013 grid; the NAVD88↔NAPGD2022 grid to come), and **ellipsoid-to-tidal** separation models.

**VDatum (United States).** NOAA's VDatum (Parker et al. 2003; current web and Java tools) chains the three: NAD83(2011) or ITRF ellipsoidal height ↔ NAVD88 via the current GEOID model, NAVD88 ↔ local MSL via a **topography-of-the-sea-surface (TSS)** grid built from gauges and hydrodynamic models, and MSL ↔ the tidal datums (MLLW, MLW, MTL, MHW, MHHW) via datum fields from TCARI and ADCIRC-based models. Coverage is the US coast out to roughly the 200 m isobath, the Great Lakes (with IGLD 1985), and the territories, by region. NOAA publishes an uncertainty table per region: typical **maximum cumulative uncertainty** for NAD83 → MLLW is on the order of 5–10 cm along open coasts and 10–20 cm in complex estuaries and bays (NOAA VDatum documentation; the per-region values should be read from the current tables rather than quoted from here).

**Separation (SEP) models in hydrographic software.** CARIS HIPS, QPS Qimera, Hypack, and Teledyne PDS consume a SEP grid — ellipsoid height of the chart datum — to reduce ERS soundings. Agencies build them from VDatum, VORF, AusCoastVDT, or in-house gauge-plus-geoid work; the SEP grid *is* the vertical datum of the survey and should be archived with it.

**VORF, AusCoastVDT, BLAST.** The UK's Vertical Offshore Reference Frames model (UKHO with UCL, 2008 onward) gives ETRS89-to-LAT, -MSL, and -ODN separations around the British Isles from a geoid, altimetric MDT, and tidal models, with quoted uncertainty of about 10 cm (1σ) offshore and more in estuaries (Iliffe et al. 2013). Australia's AusCoastVDT (CRC for Spatial Information, 2012; Geoscience Australia now maintains successor coastal vertical-datum tools) links AHD, the ellipsoid, MSL, and LAT with uncertainty maps. In Europe the Interreg BLAST project (2009–2012) built the North Sea LAT-to-ellipsoid surface that EMODnet Bathymetry uses to express its grid relative to LAT; national agencies maintain NAP/DHHN-to-LAT models for coastal engineering.

**Transformation uncertainty.** Every link in a VDatum-style chain adds uncertainty, and they add in quadrature only if independent — which the geoid and the TSS are not entirely, since the TSS was built using the geoid. Representative 1σ magnitudes (open coast / estuary): GNSS $h$, 2–3 / 2–3 cm; hybrid geoid, 2–5 / 2–5 cm; TSS (NAVD88→MSL), 3–5 / 5–15 cm; MSL→MLLW datum field, 2–4 / 5–15 cm. Root-sum-square totals of about 5–8 cm offshore and 10–20 cm in estuaries follow, which matches NOAA's published regional maxima. The estuary degradation is physical: the datums vary rapidly in space where the tide is distorted by shallow water and river flow, and gauges are sparse.

> **Try it.** Chain a vertical transformation with PROJ and inspect each step. This example converts a NAD83(2011) ellipsoidal height to NAVD88 using GEOID18, then applies a user-supplied MLLW separation grid (such as one exported from VDatum as a GeoTIFF of NAVD88-to-MLLW offsets):
>
> ```bash
> # Step 1: ellipsoidal (EPSG:6319, NAD83(2011) 3D) -> NAVD88 (compound EPSG:6349)
> echo "-122.4194 37.7749 -3.00" | cs2cs EPSG:6319 EPSG:6349 -d 3
> # San Francisco: GEOID18 N ≈ -32.6 m, so H ≈ -3.00 - (-32.6) ≈ +29.6 m
>
> # Step 2: NAVD88 -> MLLW with a local separation grid (values = MLLW - NAVD88, metres)
> echo "-122.4194 37.7749 29.60" | \
>   cct -d 3 +proj=pipeline \
>       +step +proj=vgridshift +grids=./sf_navd88_to_mllw.tif +multiplier=-1
> # Expect roughly 29.60 - (-0.06 .. +0.10) m: in SF Bay the NAVD88–MLLW
> # separation is a few centimetres to a decimetre; check VDatum for the exact local value.
> ```
>
> The point of the exercise is the `+multiplier` sign and the grid's definition (is the stored value CD−NAVD88 or NAVD88−CD?). Verify with one point from VDatum's web interface before running a million.

## 9.8 The land–water seam

At the coast three height systems meet: the land datum (NAVD88, ODN, NAP, AHD), the chart datum (MLLW, LAT), and the ellipsoid that both were measured against. Their zeros differ by metres, and the differences vary along the coast:

- **NAVD88 vs MLLW (United States).** MLLW lies below NAVD88 zero by an amount that is roughly the local MSL–NAVD88 offset plus half the diurnal range: about 0.1–0.5 m on much of the Atlantic, around 1 m in San Francisco Bay, 1–2 m in Puget Sound, and 3 m or more in Cook Inlet and the Bay of Fundy approaches (VDatum; approximate). A topobathymetric DEM that places land in NAVD88 and water in MLLW without transformation has a step at the shoreline of that size, and the shoreline itself (MHW, by US legal convention) will not fall on any consistent contour.
- **NAP vs TAW.** About 2.3 m across the Dutch–Belgian border (§9.1); the Scheldt estuary DEMs from the two countries disagree by that amount until one is transformed.
- **NGVD29 vs NAVD88.** Up to about 1.5 m; coastal engineering studies built on 1970s NGVD29 benchmark elevations and compared against modern NAVD88 lidar show "subsidence" or "accretion" of that size if the conversion is omitted.
- **Great Lakes.** IGLD 1985 Low Water Datum vs NAVD88 differences of up to ~0.3 m, and lake levels that vary seasonally and interannually by a metre or more, so that "the shoreline" in a DEM depends on the acquisition date ([Chapter 36](ch36-seasonal-variability.md)).

The seam is also where the *definition* of the surface changes: land lidar measures the ground (or the water surface, which it then flattens; [Chapter 34](ch34-water-in-dems.md)), bathymetric lidar and sonar measure the seabed, and in the intertidal zone both may be present at different times. [Chapter 19](ch19-bathymetric-lidar.md) and [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md) treat the acquisition side; here the point is that the datum transformation must be applied *before* the surfaces are merged, with the same separation model on both sides of the seam, and the merged product's metadata must state one vertical datum and the transformation applied to each source.

<!-- figure: Figure 9.3 — Cross-shore profile through a topobathymetric DEM showing the ellipsoid, geoid/NAVD88 zero, local MSL, MHW, MLLW/LAT, and the land and seabed surfaces, with the separations N, TSS, and (CD − MSL) labelled. -->

## 9.9 Vertical datums on ice and other planets

On the **ice sheets** there is no levelling network and the "ground" changes by metres per year in places; Antarctic and Greenland DEMs (REMA, ArcticDEM, BedMachine) are published in ellipsoidal heights with an EGM2008 grid supplied, and the surface epoch is part of the product's definition. The datum issue that bites is the permanent-tide convention: altimetry heights (ICESat-2, CryoSat-2) are tide-free ITRF, and comparisons with DEMs in another convention inherit a latitude-dependent decimetre offset ([Chapter 7](ch07-shape-of-the-earth.md), §7.8).

On **Mars** the vertical datum is the **areoid**, an equipotential surface of the Martian gravity field with mean equatorial radius 3 396.0 km; MOLA elevations are heights above it (Smith et al. 2001), and the older 6.1 mbar pressure-surface datum of the Viking era differs from it by a spatially variable amount, so pre-MOLA elevations must be re-referenced before comparison. On the **Moon**, LOLA and Kaguya elevations are referenced to a **sphere of radius 1 737.4 km** centred on the centre of mass; the selenoid departs from it by several hundred metres. Neither convention is wrong, and both are documented — the lesson for Earth-based workers is that a datum is always a convention ([Chapter 67](ch67-planetary-dems.md)).

## Then & now

- **Local MSL at one gauge → levelling networks held to many gauges → single-origin networks → geoid-defined datums.** NAP (1684) and the Amsterdam zero; Sea Level Datum of 1929 with 26 gauges; NAVD88 (1991) with one; CGVD2013 and NZVD2016 defined by a geopotential surface and a geoid model; NAPGD2022 the same for North America.
- **Chart datums from local custom → MLW/MLWS → MLLW (US 1980) → LAT (IHO recommendation 1997).** Shalowitz (1962, 1964) documents the US legal history; the shift to LAT internationally came with the IHO's push for a common low-water datum.
- **Tidal datum epochs.** NOAA's 19-year NTDE sequence (1941–1959, 1960–1978, 1983–2001, 2002–2020) and the introduction of modified epochs for fast-subsiding coasts in the 2000s; S-100/S-104 (2020s) carry datum and water-level metadata in the chart itself.
- **Water-level reduction: tide staffs and predicted tides → zoned observed tides → TCARI (2003) → ERS with SEP models (FIG 62, 2014) and GNSS-positioned soundings.** The tide gauge has moved from the critical path to a validation role.
- **Transformations: constant offsets on a chart note → VERTCON (1994) → VDatum (2003) → VORF (2008), AusCoastVDT (2012), BLAST (2012) → PROJ vertical grids as GeoTIFF (2019) → published per-cell uncertainties (AUSGeoid2020, VDatum).**
- **Project datums.** "Assumed 100.00" has not changed since the chain and level; what changed is that RTK localization made it possible to create one in minutes, and that regional lidar made its costs visible to everyone downstream.

## Mathematics

**Orthometric from ellipsoidal.** $H = h - N$, with the caveats of [Chapter 7](ch07-shape-of-the-earth.md): $N$ must be the separation between *this* ellipsoid/frame and *this* orthometric datum, so for a hybrid model $H_{NAVD88} = h_{NAD83(2011)} - N_{GEOID18}$ and for a gravimetric model $H_{geoid} = h_{ITRF} - N_{grav}$, and the two $H$ differ by the datum offset.

**Separation from ellipsoid to chart datum.** Writing all heights positive upward and measured along the normal at the point,

$$S \;=\; h_{CD} \;=\; N \;+\; (\mathrm{MSL} - \text{geoid}) \;+\; (\mathrm{CD} - \mathrm{MSL}),$$

where $N$ is the geoid (or datum) height above the ellipsoid, $(\mathrm{MSL} - \text{geoid})$ is the mean dynamic topography or, in VDatum's terms, the TSS between the land datum and local MSL, and $(\mathrm{CD} - \mathrm{MSL})$ is the (negative) tidal-datum offset — for MLLW, approximately minus the mean diurnal low-water inequality plus half the mean range. A depth from an ERS survey is then $d_{CD} = S - h_{seabed}$. With the land datum $D$ in the chain, $h_{CD} = N_{D} + (\mathrm{MSL} - D) + (\mathrm{CD} - \mathrm{MSL})$, and each bracket is a grid.

**Tidal datums by simultaneous comparison (NOAA standard method).** Let subscripts $c$ and $s$ denote control and subordinate stations and the overbar a mean over the simultaneous period. The equivalent 19-year MSL and MTL at the subordinate are

$$\mathrm{MSL}_s^{19} = \mathrm{MSL}_c^{19} + (\overline{\mathrm{MSL}}_s - \overline{\mathrm{MSL}}_c), \qquad \mathrm{MTL}_s^{19} = \mathrm{MTL}_c^{19} + (\overline{\mathrm{MTL}}_s - \overline{\mathrm{MTL}}_c).$$

The ranges are scaled by ratio (the **range-ratio method**):

$$\mathrm{Mn}_s^{19} = \mathrm{Mn}_c^{19}\,\frac{\overline{\mathrm{Mn}}_s}{\overline{\mathrm{Mn}}_c}, \qquad \mathrm{DLQ}_s^{19} = \mathrm{DLQ}_c^{19}\,\frac{\overline{\mathrm{DLQ}}_s}{\overline{\mathrm{DLQ}}_c},$$

where Mn is the mean range (MHW − MLW) and DLQ the mean diurnal low-water inequality (MLW − MLLW). Then

$$\mathrm{MLW}_s^{19} = \mathrm{MTL}_s^{19} - \tfrac{1}{2}\mathrm{Mn}_s^{19}, \qquad \mathrm{MLLW}_s^{19} = \mathrm{MLW}_s^{19} - \mathrm{DLQ}_s^{19},$$

and symmetrically for MHW and MHHW with the diurnal high-water inequality. For diurnal regimes NOAA uses the Modified-Range-Ratio or Direct methods instead; the handbook (NOAA 2003) specifies which applies.

> **Worked example.** A subordinate gauge records one year simultaneously with a control station. Control's accepted NTDE values (above station datum): MTL 2.000 m, Mn 1.600 m, DLQ 0.250 m, so MLW$_c$ = 1.200 m and MLLW$_c$ = 0.950 m. Over the simultaneous year: $\overline{\mathrm{MTL}}_c = 2.035$, $\overline{\mathrm{MTL}}_s = 1.512$ (sea level was 3.5 cm above its epoch mean that year at the control); $\overline{\mathrm{Mn}}_c = 1.590$, $\overline{\mathrm{Mn}}_s = 1.272$; $\overline{\mathrm{DLQ}}_c = 0.248$, $\overline{\mathrm{DLQ}}_s = 0.310$.
>
> MTL$_s^{19}$ = 2.000 + (1.512 − 2.035) = **1.477 m**.
> Mn$_s^{19}$ = 1.600 × (1.272/1.590) = 1.600 × 0.800 = **1.280 m**.
> DLQ$_s^{19}$ = 0.250 × (0.310/0.248) = 0.250 × 1.250 = **0.3125 m**.
> MLW$_s^{19}$ = 1.477 − 0.640 = **0.837 m**; MLLW$_s^{19}$ = 0.837 − 0.3125 = **0.5245 m** above the subordinate's station datum.
>
> Had the analyst simply averaged the subordinate's one year of lower low waters, the result would have been about 0.56 m (the year's +3.5 cm anomaly carried straight into the datum). The 3.5 cm difference is the size of error that simultaneous comparison exists to remove, and it is the same size as the entire epoch-to-epoch change on many coasts.

**TVU contribution of water-level reduction.** IHO S-44 expresses the allowable total vertical uncertainty as $\mathrm{TVU}_{max}(d) = \sqrt{a^2 + (b\,d)^2}$ at 95 %, with $a$ the depth-independent term (0.15 m Exclusive, 0.25 m Special Order, 0.5 m Order 1) and $b$ the depth-proportional one. The water-level term enters $a$. If the survey's water-level reduction has 1σ uncertainty $\sigma_{WL}$ and the remaining depth-independent terms (draft, heave, sonar) have $\sigma_{other}$, then at 95 % the budget requires $1.96\sqrt{\sigma_{WL}^2 + \sigma_{other}^2} \le a$. For Special Order with $\sigma_{other} = 0.08$ m, this leaves $\sigma_{WL} \le \sqrt{(0.25/1.96)^2 - 0.08^2} = \sqrt{0.01627 - 0.0064} = 0.099$ m. A zoned predicted tide with 0.15 m 1σ error fails this; observed tides with TCARI (0.05 m) or ERS with a 0.05–0.08 m SEP pass. The arithmetic shows why ERS and VDatum-class SEP models were adopted: the water level was the budget's largest single term.

**Datum offset in change detection.** If two surfaces are on datums differing by an unknown constant $\delta$ with prior uncertainty $\sigma_\delta$, the uncertainty of a volume change over area $A$ gains a term $A\,\sigma_\delta$ that does not shrink with the number of cells: for $A = 1$ km² and $\sigma_\delta = 0.1$ m, that is 100 000 m³, which is often larger than the geomorphic signal. Estimating $\delta$ from stable terrain in the overlap ([Chapter 41](ch41-change-detection.md)) replaces $\sigma_\delta$ with the standard error of that estimate — provided the stable terrain is truly on both datums without a tilt.

## Validation & uncertainty

Vertical-datum error is almost never random. It is a constant, a tilt, or a smooth field, and it is almost always *large* relative to the product's stated accuracy when it occurs at all. That makes it both easy to detect when you look and easy to miss when you do not — a 1 m step is invisible in a hillshade of rolling terrain and invisible in an RMSE computed against checkpoints that were transformed with the same wrong assumption.

### How errors arise

1. **Unstated or misstated datum.** The file says "NAVD88" and the heights are NGVD29 (up to 1.5 m), or ellipsoidal (−30 m in the eastern US, +50 m in parts of Europe — gross and obvious), or MLLW (metres at the coast), or a project datum (anything).
2. **Wrong realization or epoch of the right datum.** NAVD88 via GEOID12B versus GEOID18 (centimetres to a decimetre); MLLW of the 1960–1978 epoch versus 1983–2001 (5–15 cm on subsiding coasts); AHD "as published" versus AHD "via AUSGeoid09" (decimetres in places).
3. **Wrong separation model for the location.** A land hybrid geoid applied offshore; VDatum applied outside its region; a SEP grid from a neighbouring survey extrapolated across an estuary mouth.
4. **Unit and sign errors.** US survey feet vs metres on 1950s–1980s benchmarks and drawings; MLLW depths positive down merged with heights positive up; a separation grid applied with the wrong sign (the `+multiplier` trap).
5. **Localization/site calibration.** A vertical plane fitted to a few marks and extrapolated; the calibration file not delivered with the data.
6. **Datum change between acquisition and use.** Tidal epochs update; national datums are replaced (NAVD88 → NAPGD2022; AHD → AVWS); the product's heights do not change but their relationship to current control does.

### How errors propagate

A datum error is a bias $\delta$ (possibly with a tilt) added to every height. Slopes and local relief are unaffected by a constant; volumes gain $A\,\delta$; flood extents move by $\delta/\tan\beta$ horizontally — 100 m per 0.1 m on a 1:1000 floodplain; coastal inundation frequencies for the affected elevation band change by large factors when $\delta$ is comparable to the local tidal inequality; and change detection between products on different datums reports a uniform false change of $\delta$ that can exceed the real signal by an order of magnitude.

### How to test

- **Water-surface check.** Lidar returns from calm water bodies give the water-surface elevation on the survey date; compare with a gauge reading on that date reduced to the DEM's claimed datum. A disagreement of more than the lidar's accuracy (≈ 0.1 m) plus the gauge-datum uncertainty is a datum problem (or a gauge-datum problem — either is worth knowing). This is the cheapest and most powerful test for coastal and riverine DEMs ([Chapter 34](ch34-water-in-dems.md)).
- **Shoreline check.** For a topobathy DEM, intersect the surface with the MHW (or national legal shoreline) elevation and compare with the independently mapped shoreline; a systematic landward or seaward displacement of the contour is $\delta/\tan\beta_{beach}$.
- **Benchmark residuals.** Occupy published benchmarks with GNSS, reduce to the product's datum with the product's stated model, and compare with the published elevations; plot residuals against position to see tilts, and against benchmark epoch to see subsidence.
- **Overlap differencing.** Where two sources overlap on stable terrain, the mean difference after each has been transformed to the common datum should be within the RSS of their accuracies; a residual larger than that is a transformation (or metadata) error on one side.
- **Metadata audit.** Datum name, realization/epoch, geoid or separation model name and version, units, and the sign convention of depths. A missing entry is a finding, not a gap to fill by assumption.
- **Gauge-datum verification.** For any river gauge used in a project, check its published datum elevation against the lidar water surface at the time of the lidar; the USGS National Water Information System flags gauges whose datum has been re-levelled, but not all have.

> **Uncertainty budget.** Depth of one sounding reduced to MLLW in a US estuary by two methods. Values are indicative 1σ in metres; the third column is the ERS alternative.
>
> | Component | Zoned observed tide | ERS with VDatum SEP |
> |---|---|---|
> | Sonar range, sound speed, refraction (10 m depth) | 0.04 | 0.04 |
> | Heave / induced heave after motion compensation | 0.03 | 0.02 (GNSS height replaces heave) |
> | Static + dynamic draft, squat | 0.05 | — (absorbed in GNSS antenna–transducer lever arm, 0.02) |
> | Water-level observation at gauge | 0.02 | — |
> | Zoning error between gauge and sounding (estuary) | 0.08–0.15 | — |
> | GNSS ellipsoidal height, PPK | — | 0.03–0.05 |
> | SEP: geoid + TSS + MLLW field (estuary) | — | 0.08–0.15 |
> | **RSS total (1σ)** | **0.11–0.17** | **0.10–0.17** |
> | **At 95 % (×1.96)** | **0.22–0.33** | **0.20–0.33** |
>
> The two approaches arrive at similar totals in an estuary because both are dominated by the spatial variation of the tidal datum between gauges; ERS wins decisively offshore, where the SEP is smooth (total ≈ 0.07 m, 1σ) and zoning is poor. Both exceed the S-44 Special Order $a = 0.25$ m at 95 % at the upper end — which is why Special Order surveys in estuaries install additional temporary gauges to shrink the zoning/SEP term.

### What to report

Vertical datum (name, realization, epoch); geoid or separation model (name, version, date downloaded); units and sign convention; transformation operations applied to each source in a merged product and the residual at seams; the gauges used, their datum elevations and the epoch of those; for any project datum, the tie to national control (marks, dates, observations, resulting offset and tilt, with uncertainty); and, ideally, the ellipsoidal heights alongside the reduced ones.

## Software

**Open source.**
- **PROJ / pyproj** with PROJ-data: geoid grids, VERTCON (`us_noaa_vertconc.tif` etc.), national datum grids, and user-supplied separation grids via `+proj=vgridshift`; compound CRS support means `cs2cs EPSG:6319 EPSG:6349` applies GEOID18 automatically. Caveat: tidal datums are not in EPSG (except a few, e.g. EPSG:5866 "MLLW depth" as a generic datum), so MLLW/LAT separations must be supplied as grids and documented by you.
- **GDAL** (`gdalwarp` with compound CRSs, `gdal_calc.py` for applying separation rasters): the workhorse for transforming whole DEMs; caveat: `gdalwarp` will happily reproject a geoid grid as if it were imagery — apply separations in the DEM's native grid.
- **MB-System**: `mbprocess` applies tide files and SEP grids to sonar data; `mbgrid` outputs on any datum you supply. Caveat: the tide/SEP sign conventions are documented but easy to invert.
- **xdem**: vertical bias and tilt estimation between DEMs on stable terrain — the tool for *finding* a datum discrepancy empirically.

**Free but closed.**
- **NOAA VDatum** (web, API, Java application): the US authority for ellipsoid ↔ NAVD88 ↔ tidal datums with regional uncertainty tables; caveat: coverage ends near the 200 m isobath and in some back-bays, and the tool returns a null or flagged value there — check the flags.
- **NGS VERTCON 3.0 and GEOID18 tools; NCAT** for NGVD29/NAVD88 and ellipsoid/NAVD88.
- **VORF** (UKHO; licensed free to UK users under conditions) and **AusCoastVDT** (Geoscience Australia / CRCSI).
- **NOAA CO-OPS datum pages and the Tidal Datum computation tools**: accepted datums, epochs, and benchmark sheets for every US gauge.

**Commercial.**
- **CARIS HIPS and SIPS, QPS Qimera, Hypack, Teledyne PDS**: SEP-model reduction, tide zoning, and ERS workflows (caveat: SEP grid format and sign are software-specific). **Trimble Business Center, Leica Infinity, Topcon Magnet**: site calibration and geoid application (caveat: the localization lives in the project, not the data — export and archive it). **Esri ArcGIS Pro** and **Global Mapper**: vertical transformations via PROJ/EPSG grids and VDatum integration (caveat: the default when a vertical CRS is missing is *no* vertical transformation, silently).

## Standards & guides

- **NOAA Special Publication NOS CO-OPS 1**, *Tidal Datums and Their Applications* (Gill & Schultz, 2000) — definitions, epochs, legal uses.
- **NOAA Special Publication NOS CO-OPS 2**, *Computational Techniques for Tidal Datums Handbook* (2003) — the simultaneous-comparison and range-ratio procedures and their accuracy.
- **IOC Manuals and Guides No. 14**, *Manual on Sea Level Measurement and Interpretation*, Vols. I–V (1985–2016) — gauge installation, datum control, benchmark ties.
- **FIG Publication No. 62**, *Ellipsoidally Referenced Surveying for Hydrography* (Mills & Dodd, FIG Commission 4, 2014) — the ERS method and its SEP requirements.
- **NOAA Hydrographic Surveys Specifications and Deliverables (HSSD)**, annual editions — the water-levels chapter: gauge requirements, zoning, ERS, and the required uncertainty of water-level reduction.
- **NGS-58** (Zilkoski et al., 1997), *Guidelines for Establishing GPS-Derived Ellipsoid Heights (Standards: 2 cm and 5 cm)*, and **NGS-59** (Zilkoski et al., 2008), *Guidelines for Establishing GPS-Derived Orthometric Heights* — how to tie a project to national control with stated accuracy.
- **IHO S-44**, *Standards for Hydrographic Surveys*, Edition 6.1.0 (2022) — TVU budgets into which water-level and datum uncertainties must fit; **IHO Technical Resolution A2.5** on LAT as chart datum; **IHO S-104** (water level information for surface navigation).

## Pitfalls

- **"MSL" of unknown gauge and epoch used as a datum.** It happens because old maps say "above mean sea level." Detect by comparing with a modern datum: an offset of 0.2–1 m with no documentation. Avoid by treating "MSL" as ±1 m until the gauge and epoch are found.
- **Applying a land hybrid geoid offshore.** The hybrid model is unconstrained beyond the coast. Detect by decimetre steps or trends seaward of the shoreline; avoid with VDatum/VORF/AusCoastVDT or a purpose-built SEP.
- **Predicted tides when observed water levels differ by decimetres.** Surge, setup, and river discharge are not in the prediction. Detect by comparing predicted and observed at the nearest gauge for the survey dates; avoid by using observed/zoned or ERS reductions, as S-44 and HSSD require.
- **Mixing LAT and MLLW (or MLW and MLLW) within a compilation.** They differ by 0.1–0.5 m or more. Detect by shoreline-parallel steps at source boundaries; avoid by transforming every source to one chart datum through a stated model.
- **Feet vs metres on legacy benchmarks and drawings.** US survey feet persist on 1980s benchmark sheets and many state DOT drawings. Detect by residuals near a factor of 3.28 or a 0.3048 multiple; avoid by reading the unit on the datasheet and recording it.
- **Undocumented local datums.** "Assumed 100.00" with no tie. Detect by an elevation range that is implausible for the location (a coastal site at 100 m); avoid by tying to national control at the start and publishing the offset.
- **Forgetting that tidal datums and legal shorelines move with every epoch update.** The datum of a 2005 survey is the 1983–2001 epoch; a survey made after the next NTDE is adopted will be on 2002–2020. Detect by a uniform coastal offset of 5–15 cm between epochs; avoid by recording the epoch and converting with NOAA's published epoch-change values.
- **Site calibrations that leave with the crew.** The vertical plane fitted in the field is in the controller, not in the deliverable. Detect by heights that match the site's old control but not national control; avoid by delivering the calibration report and the raw GNSS heights.
- **Sign errors in separation grids, or constants where grids are needed.** CD−NAVD88 vs NAVD88−CD; depth positive down vs height up; a single offset applied where the transformation is a surface. Detect by a seam offset of exactly twice the expected separation, or a residual tilt; avoid by testing one point against VDatum before batch processing and always applying the grid.
- **Using a river gauge's published datum elevation without verification.** Gauge datums are frequently decades old and sometimes wrong by decimetres. Detect by comparing the lidar water surface on the acquisition date with the gauge stage plus datum; avoid by making that check part of every riverine project.

## Key takeaways

- Document the vertical datum, its realization and epoch, and the transformation (model name and version) used — or the product cannot be merged, compared, or trusted.
- Survey to the ellipsoid; reduce to whatever the user needs; archive the ellipsoidal heights with frame and epoch so the reduction can be redone.
- National orthometric datums are offset and tilted by 0.2–1 m at continental scale relative to the geoid and to each other; the transformation between any two is a grid, not a number.
- Tidal datums are 19-year statistics at gauges with a stated epoch; they move 5–15 cm per epoch on most coasts, and chart datums (MLLW, LAT) differ from one another by decimetres.
- Between gauges, datums vary spatially; zoning, TCARI, or hydrodynamic models supply the field, and the estuary is where every method's uncertainty is largest (10–20 cm) because the physics is.
- The coast is where three height systems meet; NAVD88, MLLW, and the ellipsoid differ by metres at the shoreline, and a topobathy DEM must transform every source to one datum *before* merging.
- Home-made datums are rational locally and expensive later; make them safe by tying to national control at ≥ 2 marks, publishing the offset and tilt, and keeping ellipsoidal heights in parallel.
- The cheapest validation of a coastal or riverine DEM's datum is the water surface: compare lidar water-surface elevations with gauge readings reduced to the claimed datum on the acquisition date.

## References

- Coordinating Committee on Great Lakes Basic Hydraulic and Hydrologic Data (1995). *Establishment of International Great Lakes Datum (1985)*. US Army Corps of Engineers / Environment Canada (datum implemented 1992; report published December 1995).
- Dodd, D., & Mills, J. (2011). Ellipsoidally referenced surveys: Issues and solutions. *International Hydrographic Review*, No. 5 (May 2011):19–29.
- Mills, J., & Dodd, D. (2014). *Ellipsoidally Referenced Surveying for Hydrography*. FIG Publication No. 62. International Federation of Surveyors, Copenhagen.
- Eakins, B. W., & Grothe, P. R. (2014). Challenges in building coastal digital elevation models. *Journal of Coastal Research*, 30(5):942–953. doi:10.2112/JCOASTRES-D-13-00192.1
- Featherstone, W. E., & Filmer, M. S. (2012). The north–south tilt in the Australian Height Datum is explained by the ocean's mean dynamic topography. *Journal of Geophysical Research: Oceans*, 117:C08035. doi:10.1029/2012JC007974
- Gill, S. K., & Schultz, J. R. (2000). *Tidal Datums and Their Applications*. NOAA Special Publication NOS CO-OPS 1. Silver Spring.
- Hess, K. W. (2003). Water level simulation in bays by spatial interpolation of tidal constituents, residual water levels, and datums. *Continental Shelf Research*, 23(5):395–414. doi:10.1016/S0278-4343(03)00005-0
- Iliffe, J. C., Ziebart, M. K., Turner, J. F., Talbot, A. J., & Lessnoff, A. P. (2013). Accuracy of vertical datum surfaces in coastal and offshore zones. *Survey Review*, 45(331):254–262.
- IHO (2022). *Standards for Hydrographic Surveys*, Special Publication S-44, Edition 6.1.0. International Hydrographic Organization, Monaco.
- NOAA (2003). *Computational Techniques for Tidal Datums Handbook*. NOAA Special Publication NOS CO-OPS 2. Silver Spring.
- National Geodetic Survey (2017). *Blueprint for 2022, Part 2: Geopotential Coordinates*. NOAA Technical Report NOS NGS 64.
- Parker, B., Milbert, D., Hess, K., & Gill, S. (2003). National VDatum — The implementation of a national vertical datum transformation database. *Sea Technology*, 44(9):10–15.
- Penna, N. T., Featherstone, W. E., Gazeaux, J., & Bingham, R. J. (2013). The apparent British sea slope is caused by systematic errors in the levelling-based vertical datum. *Geophysical Journal International*, 194(2):772–786. doi:10.1093/gji/ggt161
- Pugh, D., & Woodworth, P. (2014). *Sea-Level Science: Understanding Tides, Surges, Tsunamis and Mean Sea-Level Changes*. Cambridge University Press, Cambridge.
- Shalowitz, A. L. (1962, 1964). *Shore and Sea Boundaries*, Vols. 1–2. US Coast and Geodetic Survey Publication 10-1. US Government Printing Office, Washington.
- Smith, D. E., Zuber, M. T., Frey, H. V., Garvin, J. B., Head, J. W., et al. (2001). Mars Orbiter Laser Altimeter: Experiment summary after the first year of global mapping of Mars. *Journal of Geophysical Research: Planets*, 106(E10):23689–23722. doi:10.1029/2000JE001364
- Véronneau, M., & Huang, J. (2016). The Canadian Geodetic Vertical Datum of 2013 (CGVD2013). *Geomatica*, 70(1):9–19. doi:10.5623/cig2016-101
- Zilkoski, D. B., Richards, J. H., & Young, G. M. (1992). Results of the general adjustment of the North American Vertical Datum of 1988. *Surveying and Land Information Systems*, 52(3):133–149.

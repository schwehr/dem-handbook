# Chapter 4 — Names and definitions: DEM, DSM, DTM, and the words that bite

> **Part II — Vocabulary and the foundations of correctness.** This chapter fixes the vocabulary that every later chapter depends on, and catalogs the terms whose meanings silently differ between surveying, hydrography, remote sensing, photogrammetry, radar, and software communities.

**In this chapter.** You will learn to name an elevation product precisely enough that a stranger could reproduce your interpretation of it: which physical surface it represents (bare earth, canopy top, reflective surface, seafloor), what kind of height its numbers are (orthometric, normal, ellipsoidal, depth below chart datum), how its cells are registered (pixel-is-point versus pixel-is-area), what its several "resolutions" actually measure, and how its accuracy, precision, and uncertainty are distinguished. You will see a side-by-side table of how USGS, ASPRS, IHO, ICAO, INSPIRE, and ISO define the same words differently, learn the specialist vocabularies of lidar, photogrammetry, hydrography, and radar well enough to read their specifications, and understand the "community collisions" — *resolution*, *accuracy*, *control*, *calibration*, *validation*, *ground truth*, *model* — that cause real errors in real projects. The chapter closes with the handbook's own conventions and a plea for metadata that uses these words exactly.

## 4.1 DEM as umbrella; DSM, DTM, and their relatives

The first and most common vocabulary failure is treating *DEM*, *DSM*, and *DTM* as synonyms. In this handbook, and in the terminology survey of Guth et al. (2021) that the ISPRS and ASPRS communities have broadly adopted, a **digital elevation model (DEM)** is the generic, umbrella term for any digital representation of a continuous elevation surface, regardless of which surface it is. The two most important specific cases are:

- A **digital surface model (DSM)** represents the **reflective surface** — the first thing a sensor sees looking down: canopy tops, roofs, vehicles, bridge decks, power lines where sampled, and bare ground where nothing stands on it. Photogrammetric dense matching and single-pass InSAR produce DSMs natively; a lidar DSM is usually built from first returns or from the highest return in each cell.
- A **digital terrain model (DTM)** represents the **bare-earth** ground surface with vegetation and built structures removed. "Removed" conceals a chain of modeling decisions: are bridges terrain? Are road embankments? Is a landfill cap? Is a pier? The definitional problem is deep enough to deserve its own chapter ([Chapter 32](ch32-dsm-to-dtm.md)); here it is enough to know that two agencies' "bare earth" can differ by meters at a bridge.

Several derived and domain-specific models share the family name:

| Term | Surface represented | Typical source | Note |
|---|---|---|---|
| DSM | First reflective surface | Photogrammetry, InSAR, lidar first return | Includes buildings, canopy, cars |
| DTM | Bare earth | Classified lidar ground returns; manual photogrammetric editing | Definition of "bare earth" varies |
| DHM / nDSM | DSM − DTM (height above ground) | Difference of the two | Also "normalized DSM"; DHM = digital height model in German-language usage |
| CHM | Canopy height model (vegetation-specific nDSM) | Lidar, SfM over forest | Pit-filling and treetop definitions matter |
| DBM | Digital bathymetric model (seafloor) | Multibeam, lidar bathymetry, SDB | Sign and datum conventions differ from land |
| Topobathymetric model | Seamless land + seafloor | Merged lidar + sonar + topobathy lidar | Requires a single vertical datum across the shoreline |
| DTED | DEM in the DTED format (NGA) | Mixed | A format name, not a surface type ([Chapter 47](ch47-file-formats.md)) |

Older and regional usage differs. In parts of Europe, especially in German- and French-language practice, *DTM* (or *MNT*, *DGM*) is the generic term and *DEM* is less used; in the United Kingdom, Ordnance Survey historically sold "DTM" and "DSM" products under those names; in the United States the USGS used "DEM" both as the generic term and as the name of a specific 1970s–1990s product format (see Then & now). The lidar era made the DSM/DTM split operationally important because a single survey produces both, and the processing path from one to the other is where most of the interpretive decisions live.

Three more phrases carry hidden assumptions:

- **Bare earth** is a processing *target*, not a physical observation. Nothing measures bare earth under a dense building; it is interpolated. Metadata should say what was removed and how the holes were filled.
- **First return / last return** are per-pulse lidar concepts. A last return is not necessarily ground (it may be a roof or a dense shrub), and a first return is not necessarily canopy top (the pulse may have missed the highest twig). The surface built from last returns is sometimes mislabeled "DTM."
- **Reflective surface** is the photogrammetric and radar term for what a DSM represents. For radar it is subtle: at C- and X-band the radar phase center over forest sits partway *into* the canopy, so an SRTM or TanDEM-X "DSM" is neither canopy top nor ground ([Chapter 21](ch21-radar-sar-insar.md)).

> **Definitions that bite.** The USGS 3D Elevation Program (3DEP) distributes a product called the "1 m DEM" that is a bare-earth DTM; the Copernicus DEM (GLO-30) is explicitly a DSM derived from TanDEM-X; SRTM is a C-band radar reflective surface that behaves like a DSM over forest and like a DTM over open ground; ASTER GDEM is a photogrammetric DSM. All four are commonly labeled "DEM" in catalogs. Differencing a DSM from a DTM over forest produces tree heights, not change ([Chapter 41](ch41-change-detection.md)).

### 4.1.1 The same words in six documents

The disagreement is not between careless and careful users; it is between carefully written standards. The table paraphrases how six authorities use the core terms (consult the cited editions for exact wording).

| Authority / document | "DEM" | Bare-earth term | Surface term | Height / elevation reference | Accuracy vocabulary |
|---|---|---|---|---|---|
| **USGS** Lidar Base Specification (2024) | Means the **bare-earth** product specifically ("DEM" = bare-earth DEM) | DEM; "bare earth" with hydro-flattening rules | DSM (first-return surface, optional deliverable) | Orthometric, NAVD 88 via current NGS geoid | NVA/VVA RMSEz and 95 % by Quality Level |
| **ASPRS** Positional Accuracy Standards Ed. 2 (2023) | Generic umbrella for any gridded elevation | DTM (bare earth; in Ed. 1 implied mass points + breaklines) | DSM (top reflective surface) | As specified by project; vertical datum must be stated | NVA (non-vegetated), VVA (vegetated), reported as RMSEz only; Ed. 2 dropped Ed. 1's 1.96·RMSEz and 95th-percentile statistics and made VVA report-only (not pass/fail) |
| **IHO** S-44 Ed. 6.1.0 / S-32 / S-102 | Rarely used; "bathymetric model," "bathymetric surface" (S-102) | Seafloor; "depth" | Not applicable (water surface handled via tide) | Depth below **sounding/chart datum** (LAT, MLLW, …) | TVU/THU at 95 %, Orders, feature detection, CATZOC |
| **ICAO** Annex 15 / PANS-AIM | "Terrain data set" / "obstacle data set" | **Terrain**: Earth's surface incl. water, ice, snow, *excluding obstacles* | Obstacles (man-made or natural objects above terrain) handled as separate features | Elevation = from **MSL**; height = from specified datum; altitude = airborne | Accuracy, resolution, confidence level (90 %) and integrity by Area 1–4 |
| **INSPIRE** Elevation spec v3.0 (2013) | Generic for DTM and DSM; covers land elevation *and* bathymetry | DTM: bare earth excluding objects | DSM: incl. vegetation and man-made objects | Height or depth relative to a named vertical CRS (EVRS recommended) | Defers to ISO 19157 quality elements |
| **ISO** 19111 / 19157 / 5725 / GUM | Not defined | Not defined | Not defined | Vertical CRS; gravity-related vs ellipsoidal height; epoch | Positional accuracy elements (19157); trueness/precision (5725); uncertainty, coverage factor (GUM) |

Two consequences follow. First, a "DEM" delivered against a USGS specification is a DTM, while a "DEM" delivered against an ASPRS or INSPIRE specification could be either; the procurement document decides. Second, ICAO's "terrain" *includes* water surfaces and permanent ice while USGS's "bare earth" hydro-flattens water to a constant and INSPIRE's DTM excludes "objects" without naming ice — so the same lidar survey yields three slightly different "terrain" products depending on who is paying.

<!-- figure: Figure 4.1 — A single cross-section through a forested slope with a building and a bridge, showing the DSM (reflective surface), the DTM (bare earth), the nDSM/CHM as the difference, and the radar phase-center surface partway into the canopy. -->

## 4.2 Elevation, height, altitude, depth, and the height systems

Everyday English treats *elevation*, *height*, and *altitude* as synonyms; the standards do not. **Elevation** is the vertical distance of a point *on the ground or on a fixed object* above a reference surface. **Altitude** is the vertical distance of a point *in the air* (aircraft, balloon, drone) above a reference, and aviation further splits it into pressure altitude, density altitude, true altitude, and height above ground level (AGL). **Height** is the general term, and in geodesy it is always qualified by the reference surface:

- **Ellipsoidal height** $h$: distance along the ellipsoid normal from the reference ellipsoid (for example GRS80 or WGS 84) to the point. GNSS measures this directly. It has no physical meaning: water can flow "uphill" in $h$.
- **Orthometric height** $H$: distance along the curved plumb line from the geoid to the point. This is what "height above mean sea level" is trying to say. Because the plumb line curves and gravity varies along it, $H$ requires an assumption about the gravity inside the Earth (Helmert orthometric heights assume a particular model).
- **Normal height** $H^*$: the Molodensky alternative, measured from the quasigeoid, requiring only surface gravity. Used officially in much of Europe, Russia, and China; differs from $H$ by up to a few decimeters in high mountains, by millimeters in lowlands.
- **Dynamic height** $H^{dyn} = C/\gamma_{45}$: the geopotential number scaled by a constant normal gravity. Points with equal dynamic height lie on the same level surface, which is what hydraulics needs on large lakes (the International Great Lakes Datum is a dynamic-height datum).
- **Geopotential number** $C = W_0 - W_P$: the difference in gravity potential between the geoid and the point, in m²/s² (or "geopotential units," 10 m²/s²). It is the physically fundamental quantity; every gravity-related height is $C$ divided by some gravity value.

The quantity tying $h$ and $H$ together is the **geoid undulation** (geoid height) $N$, the separation of the geoid above the ellipsoid, with the handbook's standing relation

$$h = H + N,$$

exact only to the extent that the plumb line and ellipsoid normal coincide (the deflection of the vertical introduces sub-millimeter differences that can be ignored for elevation work; [Chapter 7](ch07-shape-of-the-earth.md) gives the full treatment). $N$ ranges from about −106 m (south of India) to about +85 m (New Guinea) globally; across a single US county it may vary by several meters.

On the water side the vocabulary inverts sign and changes reference. A **depth** is a vertical distance *below* a water surface or datum; a **sounding** is a single measured depth; a **reduced sounding** is a sounding corrected for the tide (and draft, squat, and sound speed) to the **sounding datum** or **chart datum** (§4.7). **Draft** is the depth of the transducer (or keel) below the water line, which must be added to a measured transducer-to-bottom range to get water depth. A bathymetric grid may store positive-down depths (hydrographic convention) or negative-up elevations (geodetic convention); both appear in BAG files, in GEBCO, and in NOAA products, and a sign error here is a classic blunder ([Chapter 47](ch47-file-formats.md)). A seamless topobathymetric model must store elevations relative to one vertical datum with one sign convention, and the metadata must say which.

> **Definitions that bite.** "Mean sea level" (MSL) is used to mean at least three things: (1) the geoid, loosely; (2) the local tidal datum computed by averaging hourly heights at a specific gauge over a specific **tidal datum epoch** (in the United States, the 19-year National Tidal Datum Epoch of 1983–2001); (3) the zero of a national vertical datum that was *originally* tied to MSL at one or more gauges (NGVD 29, NAVD 88, Ordnance Datum Newlyn). Local MSL differs from the geoid by the **mean dynamic topography**, roughly ±1–2 m globally and decimeters along most coasts ([Chapter 9](ch09-vertical-datums.md)). "Heights above MSL" in a dataset's metadata is therefore not a datum specification.

## 4.3 Grid, raster, cell, pixel, post, node — and where the value lives

A **grid** is a regular lattice of locations with a value at each; a **raster** is the array data structure that stores one, usually with an affine transform mapping array indices to coordinates. The words **cell** and **pixel** describe the same thing from two viewpoints — an area in the plane versus a picture element — while **post** (from the USGS and photogrammetric tradition) and **node** (from GMT and the gridding literature) describe the point location at which an elevation is defined. The distinction sounds pedantic until two datasets are overlaid and disagree by half a cell.

There are two valid conventions, and they must be stated:

- **Pixel-is-area** (GDAL `AREA_OR_POINT=Area`; GMT *pixel registration*; GeoTIFF `RasterPixelIsArea`): the cell value represents the whole cell, and the coordinate in the geotransform is the *outer corner* of the corner cell. A grid of 100 cells at 1 m spanning x = 0–100 m has cell centers at 0.5, 1.5, …, 99.5.
- **Pixel-is-point** (GDAL `AREA_OR_POINT=Point`; GMT *gridline registration*; GeoTIFF `RasterPixelIsPoint`): the value is an elevation *at the node*, and the nodes lie on the grid lines. A 1 m grid spanning x = 0–100 m has 101 nodes at 0, 1, …, 100.

Most DEMs are conceptually pixel-is-point — a post height is an estimate of the surface at a location — but are stored and consumed as pixel-is-area by image-processing software. SRTM and ASTER GDEM tiles are nominally pixel-is-point with the node at the integer degree; the Copernicus DEM is pixel-is-point; USGS 3DEP GeoTIFFs are written as pixel-is-area with the stated origin at the corner. The GeoTIFF specification handles `RasterPixelIsPoint` by shifting the tie point by half a pixel, and GDAL's handling of that shift changed between versions (GDAL ≥ 1.x applies it internally; the `GTIFF_POINT_GEO_IGNORE` configuration option exists precisely because data producers have been inconsistent). When metadata is missing, assume nothing and test: overlay a known feature, or compare edge coordinates of adjacent tiles — a half-cell overlap or gap is the signature of a registration mismatch ([Chapter 31](ch31-interpolation-and-gridding.md), [Chapter 10](ch10-projections-and-resampling.md)).

> **Rule of thumb.** A half-cell registration error on a 30 m grid is 15 m horizontally; on a 10 % slope that becomes a 1.5 m vertical error that looks like a systematic bias correlated with aspect. If a DEM difference map shows a hillshade-like pattern (positive on one aspect, negative on the opposite), suspect registration or co-registration before suspecting the terrain ([Chapter 41](ch41-change-detection.md)).

<!-- figure: Figure 4.2 — Pixel-is-area vs pixel-is-point: the same 4×4 set of values drawn as (a) area cells with the origin at the outer corner and (b) nodes on grid lines, with the half-cell shift and the GMT -r flag annotated. -->

## 4.4 Resolution, GSD, post spacing, point density, footprint, effective resolution

"Resolution" is the most overloaded word in the field. At least six distinct quantities hide behind it, and only one of them is what a user usually means — the size of the smallest terrain feature the data can faithfully represent.

| Term | What it measures | Units | Determined by |
|---|---|---|---|
| **Post spacing / cell size** | Distance between grid nodes | m (or arc seconds) | A choice made at gridding time; can be anything |
| **Ground sample distance (GSD)** | Ground distance between adjacent pixel centers of the *sensor* image | m | Pixel pitch × flying height / focal length (frame camera); range × IFOV (scanner) |
| **Point density** | Points per unit area in a point cloud | pts/m² | Pulse rate, speed, altitude, swath, overlap |
| **Point spacing (NPS)** | Typical distance between neighboring points ≈ $1/\sqrt{\text{density}}$ | m | Same |
| **Footprint** | Diameter of the area illuminated by one pulse/beam on the ground | m | Beam divergence × range (lidar); beamwidth × depth (sonar) |
| **Effective resolution** | Smallest feature actually resolved in the product | m | Footprint, density, processing filters, interpolation, and co-registration — the *largest* of these, not the smallest |

The relationships matter. A 1 m lidar DTM gridded from 2 pts/m² (NPS ≈ 0.7 m) has an effective resolution of perhaps 2–3 m after ground filtering and interpolation. A "30 m" SRTM cell was formed from a radar footprint and processing window substantially larger than 30 m, so its effective resolution is nearer 60–90 m (the 1-arc-second product resolves features somewhat better than the 3-arc-second one, but not three times better). A satellite stereo DSM at 0.5 m GSD matched with a 7×7 window has an effective resolution of several meters on textureless surfaces. Resampling a 30 m DEM to 10 m makes a 10 m *grid*, not a 10 m *DEM* — the mantra of [Chapter 3](ch03-fitness-for-use.md) and [Chapter 44](ch44-resolution-and-sampling.md): *a finer grid is not a finer survey*.

Effective resolution can be measured rather than asserted: by the response to a known step or edge, by the spatial frequency at which the DEM's power spectrum falls to the noise floor, or by the semivariogram's nugget-to-range behavior ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 44](ch44-resolution-and-sampling.md)). Hydrographic standards add **feature detection** as a resolution requirement expressed in object size (S-44 Exclusive Order: a 0.5 m cube) rather than grid spacing (§4.7).

## 4.5 Accuracy, precision, trueness, uncertainty, repeatability, reproducibility

The metrological vocabulary is set by two documents the whole handbook leans on: ISO 5725 (*Accuracy (trueness and precision) of measurement methods and results*) and JCGM 100:2008, the *Guide to the Expression of Uncertainty in Measurement* (GUM). Their definitions:

- **Accuracy** (ISO 5725): closeness of agreement between a measurement result and the true value. It combines two components and is a *qualitative* concept; what you quantify are its parts.
- **Trueness**: closeness of the *mean* of many measurements to the true value — the absence of **bias** (systematic error).
- **Precision**: closeness of agreement among repeated measurements — the absence of **random error**, measured by a standard deviation σ.
- **Repeatability**: precision under the *same* conditions (same instrument, operator, day, settings). **Reproducibility**: precision under *changed* conditions (different instrument, crew, season, software). For DEMs, overlap/crossline comparisons measure something close to repeatability; comparison of two independent surveys measures reproducibility.
- **Uncertainty** (GUM): a parameter characterizing the dispersion of values that could reasonably be attributed to the measurand — a statement about what we *do not know*, expressed as a standard uncertainty $u$ (1σ) or an expanded uncertainty $U = k\,u$ with coverage factor $k$. The GUM is explicit that uncertainty is not the same as error: error is a single (unknown) value, uncertainty is a distribution.

In DEM practice, "accuracy" is almost always reported as an RMSE or a 95 % value computed against checkpoints; the honest translation is "the precision plus bias of this product relative to a reference that itself has uncertainty." [Chapter 5](ch05-error-and-uncertainty.md) builds the full statistical toolkit; the vocabulary point here is that *precision is not accuracy*: a lidar strip can be internally consistent to 3 cm and biased by 30 cm because the GNSS base station coordinate was wrong.

<!-- figure: Figure 4.3 — Four target diagrams (high/low trueness × high/low precision) labeled with the ISO 5725 terms, and a fifth panel showing a DEM error histogram annotated with bias, σ, RMSE, and a 95 % interval. -->

## 4.6 Datum, reference frame, CRS, epoch, realization — and the six meanings of "WGS84"

A **datum** is, in the classical sense, a set of conventions that fixes the origin, orientation, and scale of a coordinate system relative to the Earth — historically a chosen ellipsoid plus a fundamental point (NAD 27 at Meades Ranch, Kansas). A **reference system** is the abstract definition (origin at the geocenter, axes aligned with the IERS pole and meridian, SI scale); a **reference frame** is its physical **realization** through a set of station coordinates and velocities at a stated **epoch** (ITRF2020 is a frame; ITRS is the system). A **coordinate reference system (CRS)**, in the ISO 19111 sense used by PROJ and EPSG, is a coordinate system (axes, units, order) plus a datum, and may be compound (horizontal + vertical) or projected. An **epoch** is the instant at which coordinates are valid; for points on moving plates, coordinates without an epoch are incomplete ([Chapter 6](ch06-time-as-coordinate.md), [Chapter 8](ch08-horizontal-datums.md)).

"WGS84" is where this vocabulary fails most often in practice. The label legitimately refers to at least six distinct things:

1. The **WGS 84 ellipsoid** (a = 6 378 137 m, 1/f = 298.257 223 563), which differs from GRS80 only in the eighth significant figure of flattening (≈ 0.1 mm in semi-minor axis).
2. The **WGS 84 reference system** as defined by the US National Geospatial-Intelligence Agency (NGA).
3. One of its successive **realizations**: the original (1987, Doppler-based, ~1–2 m), G730 (1994), G873 (1997), G1150 (2002), G1674 (2012), G1762 (2013), G2139 (2021), and G2296 (2024). Recent realizations agree with the contemporaneous ITRF at the centimeter level; the original differed from ITRF by about a meter.
4. The **EPSG:4326** CRS, which in the EPSG database is an *ensemble* datum spanning all realizations, with an explicitly stated ensemble accuracy of 2 m — meaning that a coordinate labeled EPSG:4326 cannot, by definition, be trusted better than that without further information.
5. The **EGM96 or EGM2008 geoid** that NGA associates with WGS 84 for orthometric heights ("WGS84 heights" in consumer GPS metadata usually means EGM96 orthometric, not ellipsoidal).
6. The **WGS 84 web-Mercator** projection (EPSG:3857), which uses a sphere for projection math but tags its coordinates as WGS84.

A dataset labeled "vertical datum: WGS84" might therefore hold ellipsoidal heights in any of several frames, or EGM96 orthometric heights. The only cure is metadata naming the realization, the epoch, and the height type explicitly — e.g., "ellipsoidal heights, WGS 84 (G1762), epoch 2015.5" or "orthometric heights, NAVD 88 via GEOID18." [Chapter 8](ch08-horizontal-datums.md) and [Chapter 9](ch09-vertical-datums.md) treat the transformations.

## 4.7 Hydrographic vocabulary

Hydrography evolved its own words, codified in the IHO *Hydrographic Dictionary* (S-32) and in the survey standard S-44 (edition 6.1.0, 2022). The ones that matter for elevation work:

- **Chart datum (CD)**: the reference surface to which charted depths and drying heights are reduced. The IHO recommends a low-water level that the tide "will seldom fall below," and most nations use **Lowest Astronomical Tide (LAT)**; the United States uses **Mean Lower Low Water (MLLW)** over the National Tidal Datum Epoch. CD is defined *locally* at tide gauges and varies by meters along a coast; it is not a level surface and is not the geoid. **Sounding datum** is the datum to which a survey's soundings are reduced, which is usually but not necessarily the chart datum.
- **Total propagated uncertainty (TPU)**: the combined 1σ uncertainty of a sounding's position and depth from all contributing sources (positioning, attitude, heave, sound speed, tide, draft, transducer offsets), propagated through the depth equation. Its vertical and horizontal components, expanded to 95 %, are the **total vertical uncertainty (TVU)** and **total horizontal uncertainty (THU)**. S-44 specifies the allowed TVU as $\sqrt{a^2 + (b\,d)^2}$ with order-dependent constants $a$ (fixed) and $b$ (depth-proportional), and depth $d$.
- **Order**: S-44 survey classes — Exclusive, Special, 1a, 1b, 2 — each pairing a TVU/THU allowance with a **feature detection** requirement (the smallest cubic feature that must be detected: 0.5 m for Exclusive, 1 m for Special, 2 m or 10 % of depth for 1a) and a **feature search** (coverage) requirement. Order 1b and Order 2 do not require full seafloor search.
- **CATZOC** (Category of Zone of Confidence): the S-57/S-101 attribute (A1, A2, B, C, D, U) by which charts tell mariners the quality of underlying surveys, combining position accuracy, depth accuracy, and seafloor coverage. Much of the world's charted seafloor is CATZOC C, D, or U — i.e., unassessed or from lead-line surveys ([Chapter 62](ch62-navigation-and-charting.md)).
- **Shoal-biased**: hydrographic gridding deliberately preserves the *shallowest* sounding in a cell rather than the mean, because the shoalest point governs safety of navigation. A shoal-biased grid is not an unbiased estimate of mean depth and must not be treated as one in volume or habitat work ([Chapter 2](ch02-uses-bathymetry.md), [Chapter 20](ch20-sonar.md)).

## 4.8 Lidar vocabulary

The USGS Lidar Base Specification (LBS) and the ASPRS LAS 1.4 format (revision 15) supply most of the terms:

- **Nominal pulse spacing (NPS)** and **nominal pulse density (NPD)**: the typical spacing and density of first-return pulses from a single swath, excluding overlap. **Aggregate NPD (ANPD)** counts all swaths together. The LBS Quality Levels are defined by ANPD and vertical accuracy: **QL0** (≥ 8 pts/m², RMSEz ≤ 5 cm), **QL1** (≥ 8 pts/m², RMSEz ≤ 10 cm), **QL2** (≥ 2 pts/m², RMSEz ≤ 10 cm), **QL3** (≥ 0.5 pts/m², RMSEz ≤ 20 cm); QL2 is the 3DEP baseline. Note that density is a *pulse* density, not a return density, and that it is required in *non-vegetated* areas — density under canopy is lower.
- **Swath / strip / flight line**: one pass of the scanner; the basic unit for internal consistency checks (strip-to-strip, [Chapter 18](ch18-topographic-lidar.md)).
- **ASPRS classification codes** (LAS 1.4 Table 17): 0 created/never classified, 1 unclassified, 2 ground, 3–5 low/medium/high vegetation, 6 building, 7 low point (noise), 9 water, 17 bridge deck, 18 high noise, and so on. Code 2 is the input to a DTM; what producers put in it is governed by their classification specification, not by the number.
- **Flags**: **withheld** (point should be ignored by processing — e.g., obvious noise — but is retained for lineage), **synthetic** (point was not measured by the sensor but created, e.g., from a breakline or hydro-flattening), **key-point** (point is a model key point retained by thinning), **overlap** (point lies in the overlap between swaths; LAS 1.4 moved this to a dedicated flag from class 12). A DTM built from a cloud without honoring the withheld and overlap flags will inherit noise and double-weighted seams.

## 4.9 Photogrammetry and computer-vision vocabulary

- **GSD**: §4.4. For a frame camera, $\text{GSD} = p \cdot H / f$ with pixel pitch $p$, flying height above ground $H$, and focal length $f$.
- **Base-to-height ratio (B/H)**: the stereo baseline divided by the flying height; it governs height precision, $\sigma_Z \approx \frac{H}{B}\cdot\frac{H}{f}\cdot\sigma_{p_x}$ for parallax measurement precision $\sigma_{p_x}$. Wide baselines give better heights and worse matching; aerial mapping typically uses B/H of 0.3–0.6 ([Chapter 22](ch22-photogrammetry-sfm.md)).
- **Ground control point (GCP)** versus **checkpoint**: a GCP is a surveyed point *used in* the adjustment (it constrains the solution); a checkpoint is a surveyed point *withheld from* the adjustment and used only to assess accuracy. A point cannot be both for the same product; reusing GCPs as checkpoints reports fit, not accuracy ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 52](ch52-ground-truth.md)).
- **Tie points**: image-to-image correspondences (automatically matched features in SfM) that connect photos but have no ground coordinates. **Bundle adjustment**: the simultaneous least-squares estimation of camera exterior orientations, interior orientation (if self-calibrating), and 3D tie-point coordinates, minimizing reprojection error. **Dense matching** (semi-global matching and its descendants, or multi-view stereo): the per-pixel correspondence step that produces the DSM after the bundle adjustment fixes geometry.
- **Structure from motion (SfM)**: the computer-vision name for self-calibrating bundle adjustment from unordered images with automatically detected features; the geometry is classical photogrammetry, but the defaults, error reporting, and vocabulary differ ("reprojection error" in pixels rather than σ₀ in micrometers; "alignment" rather than "orientation").

## 4.10 Radar vocabulary

Side-looking radar images in **slant range** (distance along the line of sight), and must be projected to **ground range**; the geometry produces the three classic terrain distortions: **foreshortening** (slopes facing the radar appear compressed), **layover** (steep facing slopes have their tops imaged *before* their bases, so the image is folded), and **shadow** (slopes facing away steeper than the incidence angle are not illuminated at all). InSAR adds **coherence** (the magnitude of the complex correlation between two acquisitions, 0–1; low coherence means the phase is noise), the **height of ambiguity** $h_a = \frac{\lambda R \sin\theta}{2 B_\perp}$ (the height change producing one 2π fringe for wavelength λ, range R, incidence θ, perpendicular baseline $B_\perp$; smaller $h_a$ means more height sensitivity and harder unwrapping), and **penetration depth** (the depth into vegetation, snow, or dry sand at which the backscatter effectively originates — centimeters at X-band in wet vegetation, meters in dry snow or sand at L- and P-band) ([Chapter 21](ch21-radar-sar-insar.md)). Radar DSM voids in layover and shadow are not "no data" in the ordinary sense; they are geometric blind spots that will recur in every acquisition from the same look direction.

## 4.11 Community collisions

The words below are used by several communities with meanings that differ enough to cause errors. The table pairs each with its colliding senses.

| Word | Sense A | Sense B | Where the collision hurts |
|---|---|---|---|
| **Resolution** | Grid cell size (GIS) | Smallest resolvable feature (optics, signal processing) | Resampled products advertised at the cell size |
| **Accuracy** | Closeness to truth, including bias (ISO 5725) | A reported RMSE or 95 % number against checkpoints (ASPRS, NSSDA) | The number reported omits bias, reference uncertainty, or land cover |
| **Control** | Surveyed points constraining an adjustment (geodesy, photogrammetry) | Any reference data, including checkpoints (casual GIS) | "Control" reused as "check" |
| **Calibration** | Determining instrument parameters (boresight, lever arms, range bias) | Adjusting a product to fit reference data (remote sensing, "calibrated DEM") | A "calibrated" DEM may simply have had a bias subtracted |
| **Validation** | Independent assessment that a product meets requirements | Any comparison with other data, including non-independent data | Validation against the data used to make the product |
| **Verification** | Checking that a product conforms to its specification (ISO 9000 sense: built right) | Synonym for validation (built the right thing) | Confusing spec conformance with fitness for use |
| **Ground truth** | Reference data of known, higher accuracy | Any field observation, or another DEM | "Truth" that is itself uncertain or biased |
| **Model** | A gridded surface (DEM) | A physical/statistical/ML model producing or using the surface | "The model is wrong" — which one? |
| **Depth** | Positive-down distance below datum (hydrography) | Negative elevation (geodesy/GIS) | Sign errors at the shoreline |
| **Point** | A lidar return | A node of a grid | "Point density" vs "post spacing" |
| **Vertical datum** | A geoid/tidal/levelling-based reference surface | Whatever the heights are relative to, including an ellipsoid | "Vertical datum: WGS84" |

The practical defense is not to legislate one meaning but to *qualify* the word every time it appears in a specification or metadata record: "resolution (post spacing)," "accuracy (RMSEz against 48 independent GNSS checkpoints in open terrain)," "calibration (boresight and lever-arm determination)," "validation (independent, against NGS benchmarks)." [Chapter 52](ch52-ground-truth.md) and [Chapter 53](ch53-accuracy-assessment.md) show what each looks like in practice.

> **Case file.** When Guth et al. (2021) surveyed usage across the literature and major agencies for the ISPRS/ASPRS terminology effort, they found "DEM," "DTM," and "DSM" used inconsistently even within single agency product lines, with the most frequent problem being distribution of DSMs under the generic "DEM" label. The authors proposed DEM as the umbrella term with DSM and DTM as the specific types — the convention this handbook adopts — and explicitly recommended that metadata state which surface is represented. The recommendation remains more honored in papers than in catalogs; a quick survey of any national or cloud-hosted DEM catalog will still turn up DSMs labeled "DEM" without qualification.

## 4.12 Style guide for this handbook — and a plea

To keep 73 chapters consistent, this book uses the following conventions throughout; they are also a reasonable template for project metadata.

- **DEM** is generic. **DSM** and **DTM** are used when the surface is known. A model whose surface type is unknown is called "a DEM of unspecified surface type," which is itself informative.
- Heights are **h** (ellipsoidal), **H** (orthometric or, where stated, normal), **N** (geoid undulation), related by $h = H + N$. Depths are stated as positive-down with the datum named, or as negative elevations when inside a topobathymetric product; the metadata states which.
- **Resolution** is never used bare. We write *post spacing*, *GSD*, *point density*, *footprint*, or *effective resolution*.
- **Accuracy** statements always carry: the statistic (RMSE, NMAD, LE95…), the sample size, the land-cover stratum, the reference data and its own uncertainty, the vertical datum and epoch of both datasets, and the date of each. [Chapter 5](ch05-error-and-uncertainty.md) gives the template.
- Datums are named with realization and epoch: NAD83(2011) epoch 2010.00; ITRF2020 at the observation epoch; WGS 84 (G2139). "WGS84" alone appears only inside quotation marks when discussing its misuse.
- Grid registration is stated as pixel-is-area or pixel-is-point, and the geotransform origin as corner or center.
- Time is UTC in ISO 8601 unless the source format dictates otherwise, in which case the conversion is documented ([Chapter 6](ch06-time-as-coordinate.md)).

The plea: metadata that uses these words precisely is the cheapest accuracy improvement available in the field. A well-labeled DSM is more useful than a mislabeled DTM, and a DEM whose cell registration, datum realization, and accuracy stratum are stated can be integrated with others at a fraction of the cost of one whose properties must be reverse-engineered ([Chapter 49](ch49-metadata.md), [Chapter 54](ch54-evaluating-others-data.md)).

> **Try it.** Interrogate what a DEM file actually claims about itself before trusting a catalog label. The GDAL output below shows the pixel registration, the CRS (including whether a vertical CRS is present), and the data type — three of the five qualifiers. Note that the surface type (DSM/DTM) is almost never stored in the file; it must come from external metadata.
>
> ```bash
> # Copernicus GLO-30 tile (a DSM) — check registration, CRS, type, nodata
> gdalinfo -json Copernicus_DSM_COG_10_N46_00_E007_00_DEM.tif \
>   | python3 -c "
> import json,sys
> j=json.load(sys.stdin)
> print('AREA_OR_POINT:', j['metadata'][''].get('AREA_OR_POINT'))
> print('type:', j['bands'][0]['type'], ' nodata:', j['bands'][0].get('noDataValue'))
> print('geotransform:', j['geoTransform'])
> print('CRS:', j['coordinateSystem']['wkt'].splitlines()[0])
> print('vertical CRS present:', 'VERT' in j['coordinateSystem']['wkt'])
> "
> ```
>
> Expected outcome for this product: `AREA_OR_POINT: Point`, `type: Float32`, a geotransform whose origin is offset by half a cell from the integer degree, a geographic CRS of WGS 84, and *no* vertical CRS — the EGM2008 orthometric height reference is documented only in the product handbook. Repeat with a USGS 3DEP 1 m tile and you should see `Area`, a projected UTM CRS, and (in recent tiles) a compound CRS naming NAVD88 height; and with an SRTM `.hgt` file you should see `Point`, `Int16`, and no vertical CRS.

## Then & now

The vocabulary is younger than it feels. **Digital terrain model** was coined at the MIT Photogrammetry Laboratory by Charles Miller and Robert LaFlamme (1958), who defined it as "a statistical representation of the continuous surface of the ground by a large number of selected points with known x, y, z coordinates" — a *point* representation intended for highway design, not a grid. The word **pixel** entered print in 1965 through Frederic Billingsley's papers on digital image processing at JPL ⟨H⟩, and "picture element" and "pel" competed with it for a decade. The US Geological Survey adopted **DEM** as a *product name* in the 1970s for its gridded elevation data derived from contour maps and from the Gestalt Photo Mapper, and Doyle (1978) described the digital terrain models of that era in *Photogrammetric Engineering and Remote Sensing* — the USGS "DEM" format with its 7.5-minute quadrangle tiling defined the generic term for a generation of GIS users and fixed the habit of calling every grid a DEM. Pike (2000) traced the resulting conceptual tangle in his review of geomorphometry's progress.

The **DSM/DTM split** became operationally necessary in the 1990s when airborne lidar began producing, from a single flight, both a first-return surface and a classified bare-earth surface; vendors and agencies needed two product names, and photogrammetric "DTM" (which had always been edited to bare earth by operators) was joined by the "DSM" that automated correlators produced. InSAR missions (SRTM in 2000, TanDEM-X from 2010) added a third kind of surface — the radar reflective surface — that is neither. **Guth et al. (2021)**, writing for the ISPRS and ASPRS communities, attempted to standardize the usage this chapter follows; the companion effort by Maune and Nayegandhi (2018) in the ASPRS *DEM Users Manual* (3rd ed.) consolidated US practice. Measurement vocabulary followed a parallel path: ISO 5725's trueness/precision decomposition dates from 1994, the GUM from 1993 (revised 2008), and the IHO's TPU/TVU/THU terminology entered S-44 with the 4th edition in 1998 and was reorganized in the 5th (2008) and 6th (2020/2022) editions. The US survey foot — 1200/3937 m — was formally deprecated at the end of 2022 in favor of the international foot (0.3048 m exactly); the 2 ppm difference is 0.6 m at a northing of 300 km, which is why legacy State Plane coordinates in feet remain a definitions hazard ([Chapter 10](ch10-projections-and-resampling.md)).

## Validation & uncertainty

Vocabulary errors are a *source* of elevation error, and they can be budgeted like any other. The mechanism is always the same: a word is interpreted under one community's definition when the data were produced under another's, and the result is a systematic offset — a bias, a tilt, or a shift — that no amount of random-error analysis will reveal. The table below lists the most common collisions with typical magnitudes so that they can be entered in an uncertainty budget *as hypotheses to test* rather than discovered after delivery.

> **Uncertainty budget.** Magnitudes of error introduced purely by definitional mismatch (order of magnitude; the exact value depends on site).
>
> | Mismatch | Typical magnitude | Signature in a difference map |
> |---|---|---|
> | DSM used as DTM over forest | 5–40 m (canopy height) | Positive blobs following vegetation |
> | DSM used as DTM in cities | 3–100 m (building height) | Building footprints |
> | Ellipsoidal vs orthometric height | ±(−106 … +85) m globally; 20–50 m in the conterminous US | Smooth, large-wavelength offset |
> | Local MSL vs geoid (mean dynamic topography) | 0.1–2 m | Near-constant offset per region |
> | Chart datum (MLLW/LAT) vs orthometric datum | 0.5–5 m, varies along coast | Offset changing along shoreline |
> | Realization/epoch of "WGS84" | 0.01–2 m horizontal; cm vertical | Shift; grows with age on fast plates |
> | NAD83 vs ITRF/WGS 84 (G1762+) | ~1–2 m horizontal, ~1 m vertical in CONUS | Constant shift plus small tilt |
> | Pixel-is-point vs pixel-is-area | ½ cell horizontally → ½ cell × slope vertically | Aspect-dependent (hillshade-like) pattern |
> | US survey foot vs international foot | 2 ppm of coordinate (0.6 m per 300 km) | Scale error from the projection origin |
> | Positive-down depth vs negative elevation | 2× the depth | Reflection about zero |
> | Shoal-biased vs mean-depth gridding | Decimeters to meters in rough seabed | One-sided (always shallower) bias |

How to test for them:

1. **Check the surface type before anything else.** Compute the difference between the candidate DEM and a known DTM (or compare against lidar ground points) stratified by land cover; if the mean difference in forest exceeds that in open ground by meters, the candidate is a DSM or a radar surface regardless of its label.
2. **Check the height type by magnitude.** The difference between ellipsoidal and orthometric heights at a site is simply $N$, which any geoid model will tell you to within decimeters; a near-constant offset equal to $N$ is diagnostic. Over a whole tile, the offset will vary slowly with the geoid gradient (a few centimeters per kilometer typically).
3. **Check registration by aspect.** Regress DEM differences against $\tan(\text{slope}) \cdot \sin(\text{aspect})$ and $\tan(\text{slope}) \cdot \cos(\text{aspect})$ (the Nuth and Kääb 2011 procedure of [Chapter 41](ch41-change-detection.md)); a significant fit indicates a horizontal shift, often exactly half a cell.
4. **Check the datum realization and epoch** by comparing against passive control whose coordinates are published in several frames (NGS datasheets give NAD83(2011) and ITRF2014 coordinates with epochs). An unexplained horizontal offset of ~1 m in North America is the NAD83–ITRF difference; one of a few decimeters on an actively deforming or fast plate may be an epoch mismatch ([Chapter 6](ch06-time-as-coordinate.md)).
5. **Check units and sign** by range: a DEM of a coastal plain whose values span 0–300 is probably in feet if the terrain is known to reach 90 m; a bathymetric grid with all-positive values stores depths.

What to report: every one of the five qualifiers in the Key takeaways, with the specific document that defines each term (e.g., "bare earth per USGS LBS 2024, classification of bridges as class 17 removed"). An accuracy statement that cannot name its vertical datum and surface type is not an accuracy statement.

> **Worked example.** A coastal county merges a lidar DTM (NAVD 88 orthometric heights via GEOID18, meters) with a NOAA bathymetric grid (depths positive-down relative to MLLW, meters) at a shoreline where published tidal datums give MLLW = −0.85 m NAVD 88. A pier deck surveyed at 2.40 m NAVD 88 appears in the lidar DTM only as the ground around it. The nearshore sounding of 1.20 m MLLW must become an elevation of $-(1.20) + (-0.85) = -2.05$ m NAVD 88 before merging. An analyst who forgets the sign flip stores +1.20; one who forgets the datum shift stores −1.20; one who uses the geoid height $N \approx -30$ m (because the sonar positions were recorded as "WGS84 heights") instead of the tidal datum stores −31.2 m. The three errors are 3.25 m, 0.85 m, and 29.15 m respectively — all pure vocabulary.

## Software

**Open source:** GDAL (`gdalinfo`, `gdalsrsinfo`) reports pixel registration, CRS/WKT including vertical CRS, data type, and units — but cannot tell you the surface type; PROJ (`projinfo`, `cs2cs`) resolves datum names, ensembles, and epochs, and warns when "WGS 84" is an ensemble with 2 m accuracy; PDAL (`pdal info --metadata`, `filters.info`) reports LAS classification histograms and flags, letting you verify what was classified as ground before trusting a "DTM"; GMT (`grdinfo`) distinguishes gridline from pixel registration explicitly; QGIS exposes all of the above and its Raster Layer Properties dialog shows `AREA_OR_POINT`. **Free but closed:** NOAA VDatum (vertical datum transformations among tidal, orthometric, and ellipsoidal datums in US waters; its uncertainty varies by region and is published); NGS NCAT/HTDP (horizontal datum and epoch transformations); the EPSG registry (datum definitions and ensemble accuracies). **Commercial:** Esri ArcGIS Pro (reads vertical CRS; its "Elevation" layer semantics default to DTM-like interpretation unless told otherwise); CARIS HIPS/BASE Editor and QPS Qimera (hydrographic vocabulary natively — TPU, shoal-biased surfaces, CATZOC); Blue Marble Global Mapper and Geographic Calculator (datum/epoch bookkeeping, including survey-foot variants).

## Standards & guides

- **Guth et al. 2021**, *Remote Sensing* 13(18):3581, "Digital Elevation Models: Terminology and Definitions" — the ISPRS/ASPRS terminology recommendation adopted here.
- **ISO 19157-1:2023**, *Geographic information — Data quality — Part 1* — defines quality elements (positional accuracy, completeness, logical consistency, temporal quality, thematic accuracy, usability) and the vocabulary of quality evaluation.
- **ISO 5725-1:2023** (and parts 2–6), *Accuracy (trueness and precision) of measurement methods and results* — trueness, precision, repeatability, reproducibility.
- **JCGM 100:2008**, *Evaluation of measurement data — Guide to the expression of uncertainty in measurement* (GUM) — uncertainty, Type A/B, coverage factor; with JCGM 200:2012 (VIM, 3rd ed.) for the metrological vocabulary itself.
- **IHO S-32**, *Hydrographic Dictionary* (online edition, continuously updated) — chart datum, sounding, reduced sounding, and the rest of the hydrographic lexicon.
- **IHO S-44 Edition 6.1.0 (2022)**, *Standards for Hydrographic Surveys* — TVU/THU, Orders, feature detection and search.
- **IHO S-57 / S-101** — CATZOC (S-57 Appendix A; S-101 Data Classification and Encoding Guide).
- **ASPRS LAS Specification 1.4 – R15 (2019)** — classification codes, point flags, GPS time encoding.
- **USGS Lidar Base Specification 2024 (online)** — NPS/NPD/ANPD, Quality Levels, bare-earth classification requirements, hydro-flattening vocabulary.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (Version 1.0, 2023; Version 2, June 2024)** — NVA/VVA, checkpoint vs control, accuracy-class vocabulary.
- **ICAO Annex 15 and PANS-AIM (Doc 10066)** — terrain and obstacle data vocabulary (Areas 1–4, "obstacle," data quality requirements) for aviation.
- **INSPIRE Data Specification on Elevation (D2.8.II.1, v3.0, 2013)** — defines "elevation," "DTM," "DSM," and the European product vocabulary; distinguishes land elevation from bathymetry.
- **ISO 19111:2019**, *Referencing by coordinates* — datum, reference frame, CRS, epoch, datum ensemble.
- **NIST / NOAA Federal Register notice (2019)** on the deprecation of the US survey foot effective 2023-01-01.

## Pitfalls

- **A catalog "DEM" that is a DSM** → catalogs inherit the generic label from legacy habits → difference the candidate against known ground points by land cover before use; canopy-height offsets in forest are diagnostic.
- **"WGS84" given as the vertical datum** → consumer GNSS and many software exports write "WGS84" for both the horizontal frame and (often) EGM96 heights → determine from magnitude whether the heights are ellipsoidal or orthometric (the offset equals $N$), and demand the realization and epoch in writing.
- **"MSL" used to mean the geoid** → the two were conflated when national datums were defined at tide gauges → treat MSL as a *local tidal* datum unless the metadata names a geoid model; expect decimeter-to-meter mean dynamic topography offsets.
- **Feet versus meters, and which foot** → legacy State Plane deliverables and some US county products remain in US survey feet after the 2022 retirement → check coordinate ranges against the projection's expected extents; a 2 ppm scale error from the origin is the signature of the wrong foot.
- **"Resolution" meaning the cell size of a resampled product** → resampling is cheap and the finer number sells → ask for point density, footprint, and processing window; measure effective resolution if it matters.
- **Half-cell registration error** → the pixel-is-point/pixel-is-area flag is missing, ignored, or mishandled by software → look for aspect-correlated residuals; check tile edges for half-cell gaps or overlaps.
- **Depth sign and datum errors at the shoreline** → hydrographic (positive-down, chart datum) and geodetic (negative-up, orthometric) conventions meet in topobathymetric merges → convert explicitly through published tidal datum relationships; verify at a feature visible in both datasets.
- **GCPs reused as checkpoints** → the same survey supplied both and nobody withheld a set → insist on independence; a fit statistic is not an accuracy statistic ([Chapter 52](ch52-ground-truth.md)).
- **"Calibrated" meaning bias-subtracted** → remote-sensing usage of "calibration" for product-level fitting → ask what parameters were estimated and from what data; a bias-shifted DEM retains all of its tilts and spatially correlated error.
- **Last-return surface labeled DTM** → "last" is assumed to mean "ground" → check classification statistics; a last return on a roof is still a roof.
- **Shoal-biased bathymetry used as mean depth** → navigation products are built shallow by design → use the mean or median surface (or the point data) for volumes and habitat; use the shoal surface for navigation only.
- **Confusing verification with validation** → both are "checking" → verification asks "does it meet the spec?"; validation asks "is it right for the use?" — report both separately.

## Key takeaways

- **DEM** is the umbrella; **DSM** and **DTM** are specific surfaces, and "bare earth" is a processing target defined differently by different producers.
- Every elevation number needs five qualifiers: **which surface**, **which datum (and realization and epoch)**, **which cell semantics** (point or area, corner or center origin), **which resolution** (nominal *and* effective), and **which uncertainty** (statistic, sample, stratum, reference).
- "Height" is meaningless without its reference surface: $h$ (ellipsoid), $H$ (geoid/orthometric), normal, dynamic, or chart datum — and $h = H + N$ is the bridge.
- "WGS84" names an ellipsoid, a system, eight realizations, an EPSG ensemble with 2 m accuracy, an associated geoid, and a projection; metadata must say which.
- "Resolution" is never a single number; post spacing, GSD, point density, footprint, and effective resolution are different quantities, and the effective one is the largest of them.
- Accuracy ≠ precision; trueness and precision are its components; uncertainty is a statement about a distribution, not about one error.
- Hydrography, lidar, photogrammetry, and radar each have a precise internal vocabulary; learn enough of each to read their specifications, and translate explicitly when crossing communities.
- Definitional mismatches are systematic errors with magnitudes from centimeters to tens of meters; budget them, test for them, and report the definitions you used.

## References

- ASPRS. 2019. *LAS Specification 1.4 – R15*. American Society for Photogrammetry and Remote Sensing.
- ASPRS. 2023. *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 1.0 (August 2023); Version 2 (June 2024). Bethesda, MD: American Society for Photogrammetry and Remote Sensing.
- Billingsley, F. C. 1965. Digital video processing at JPL. *Electronic Imaging Techniques I*, Proceedings of SPIE 3, pp. XV-1–19.
- Doyle, F. J. 1978. Digital terrain models: an overview. *Photogrammetric Engineering and Remote Sensing* 44(12):1481–1485.
- Guth, P. L., A. Van Niekerk, C. H. Grohmann, J.-P. Muller, L. Hawker, I. V. Florinsky, D. Gesch, H. I. Reuter, V. Herrera-Cruz, S. Riazanoff, C. López-Vázquez, C. C. Carabajal, C. Albinet, and P. Strobl. 2021. Digital Elevation Models: Terminology and Definitions. *Remote Sensing* 13(18):3581. doi:10.3390/rs13183581
- Heidemann, H. K. 2018 (rev. 2024). *Lidar Base Specification* (online edition). U.S. Geological Survey Techniques and Methods 11-B4 and successors.
- International Hydrographic Organization. 2022. *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. Monaco: IHO.
- International Hydrographic Organization. *S-32 Hydrographic Dictionary* (online). Monaco: IHO.
- ISO. 2019. *ISO 19111:2019 Geographic information — Referencing by coordinates*. Geneva: ISO.
- ISO. 2023. *ISO 19157-1:2023 Geographic information — Data quality — Part 1: General requirements*. Geneva: ISO.
- ISO. 2023. *ISO 5725-1:2023 Accuracy (trueness and precision) of measurement methods and results — Part 1: General principles and definitions*. Geneva: ISO.
- JCGM. 2008. *JCGM 100:2008 Evaluation of measurement data — Guide to the expression of uncertainty in measurement*. Sèvres: BIPM.
- JCGM. 2012. *JCGM 200:2012 International vocabulary of metrology — Basic and general concepts and associated terms (VIM)*, 3rd ed. Sèvres: BIPM.
- Maune, D. F., and A. Nayegandhi (eds.). 2018. *Digital Elevation Model Technologies and Applications: The DEM Users Manual*, 3rd ed. Bethesda, MD: ASPRS. Chapter 1.
- Miller, C. L., and R. A. Laflamme. 1958. The digital terrain model — theory and application. *Photogrammetric Engineering* 24(3):433–442.
- NGA. 2014. *Department of Defense World Geodetic System 1984: Its Definition and Relationships with Local Geodetic Systems*, NGA.STND.0036_1.0.0_WGS84 (with later addenda on G2139 and G2296).
- NIST and NOAA. 2019. Deprecation of the United States (U.S.) survey foot. *Federal Register* 84(199):55562–55565.
- Nuth, C., and A. Kääb. 2011. Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere* 5(1):271–290. doi:10.5194/tc-5-271-2011
- Pike, R. J. 2000. Geomorphometry — diversity in quantitative surface analysis. *Progress in Physical Geography* 24(1):1–20.
- European Commission INSPIRE Thematic Working Group Elevation. 2013. *D2.8.II.1 Data Specification on Elevation — Technical Guidelines*, v3.0.
- ICAO. 2018. *Annex 15 to the Convention on International Civil Aviation — Aeronautical Information Services*, 16th ed.; and *PANS-AIM, Doc 10066*.

# Chapter 8 — Horizontal datums and terrestrial reference frames

> **Part III — Where is "here"? Geodesy, datums, projections.** Having established the shape of the Earth in [Chapter 7](ch07-shape-of-the-earth.md), this chapter fixes the coordinate system on it: frames, their realizations, the epoch that every modern coordinate silently carries, and the transformations between them.

**In this chapter.** A latitude and longitude are meaningless until you know the datum they belong to, and in the GNSS era a datum is three things — a reference frame, a realization of it, and an epoch. After this chapter you will be able to read a CRS definition and know which of the three it specifies, which it leaves implicit, and what the consequences are at the sub-metre level. You will see why NAD27 and NAD83 differ by over 100 m, why WGS84 is a family of frames rather than one, why a coordinate in Australia drifts 7 cm a year, and how the Helmert, Molodensky–Badekas, and grid-shift transformations work, including their time-dependent versions and the errors that accumulate when transformations are chained. You will learn to encode all of this correctly in WKT2 and PROJJSON, to avoid the axis-order trap, and to test the horizontal accuracy of a DEM — which matters more than most users realize, because on a slope every horizontal error becomes a vertical one.

## 8.1 Classical datums to geocentric frames

A **geodetic datum** in the classical sense is a reference ellipsoid plus a rule for attaching it to the Earth. Before satellites the only way to attach it was at a point: choose an **origin station**, assign it latitude, longitude, and geoid height (usually zero — the ellipsoid was made tangent to the geoid there), and fix the orientation by an astronomical azimuth to a second station. The whole national triangulation (§8.6) then hung from that point. Because the geoid is not the ellipsoid, and because the astronomical latitude at the origin includes the deflection of the vertical ([Chapter 7](ch07-shape-of-the-earth.md)), each classical datum ended up with its ellipsoid displaced from the Earth's centre of mass by tens to hundreds of metres, in a direction and amount peculiar to that datum.

**NAD27** ⟨H⟩ (North American Datum of 1927) used the Clarke 1866 ellipsoid with origin at Meades Ranch, Kansas; **ED50** (European Datum 1950) used the International (Hayford) ellipsoid with the orientation effectively defined at Potsdam; the **Tokyo Datum** used Bessel 1841 with origin at the old Tokyo Astronomical Observatory. Each was internally consistent to roughly a part in 100 000 for its era and each is offset from the geocentre: ED50 by about 100–200 m relative to ETRS89, Tokyo by about 400–450 m relative to JGD2000, and NAD27 by amounts that vary across the continent.

The NAD27→NAD83 shift exceeds 100 m in places for three compounding reasons. First, the Clarke 1866 ellipsoid is about 70 m larger in $a$ than GRS80 and differently flattened, so even a perfectly centred Clarke datum would differ in latitude and longitude from a GRS80 one. Second, the Meades Ranch origin placed the Clarke ellipsoid about 200 m from the geocentre in three dimensions, which projects to horizontal shifts of several tens of metres that vary with position. Third, NAD27 accumulated **network distortion**: the triangulation was adjusted in pieces, scale and azimuth errors propagated for thousands of kilometres, and when NAD83 was computed (a simultaneous adjustment of about 250 000 stations including satellite Doppler and VLBI, completed in 1986), the distortions became visible as a spatially varying field. The net shift is around 10–40 m in the eastern United States, about 80–100 m in the Pacific Northwest, 200–300 m or more in Alaska relative to the Old Alaskan datums, and about 400 m in Hawaii relative to the Old Hawaiian datum (approximate; NADCON documentation gives the maps). Because the shift is not a smooth function, no 7-parameter transformation can model it to better than several metres; grid shifts (§8.4) were invented precisely for this.

**Geocentric datums** replaced the origin-station rule with satellite geodesy: the origin is the Earth's centre of mass as sensed by satellite orbits, the orientation is inherited from an earlier frame (ultimately the BIH 1984.0 orientation), and the scale comes from the speed of light and the adopted $GM$. NAD83 (1986), WGS84 (1987), and the first ITRF (1988) were all geocentric in intent; what has happened since is that each has been *re-realized* with better data, and the realizations differ from one another by amounts that matter — see the next section.

<!-- figure: Figure 8.1 — Schematic of a classical datum (ellipsoid tangent to the geoid at the origin station, offset from the geocentre) versus a geocentric frame (ellipsoid centred on the centre of mass), with the resulting coordinate shift at a distant station. -->

## 8.2 ITRS/ITRF, IGS frames, WGS84, and the regional plate-fixed frames

The **International Terrestrial Reference System (ITRS)** is the *system*: a set of conventions (geocentric origin including oceans and atmosphere, SI metre scale, orientation continuous with BIH 1984.0 and with no net rotation relative to the lithosphere over time, as laid down in the IERS Conventions). An **International Terrestrial Reference Frame (ITRF)** is a *realization*: a list of stations with coordinates at a reference epoch and velocities, computed by combining VLBI, SLR, GNSS, and DORIS solutions. Realizations so far: ITRF88, 89, 90, 91, 92, 93, 94, 96, 97, 2000, 2005, 2008, 2014, and 2020 (Altamimi et al. 2016, 2023). Successive ITRFs differ by millimetres to a few centimetres in origin and scale — ITRF2014→ITRF2020, for example, involves translations under 3 mm and a scale change of about −0.42 ppb at epoch 2015.0 (approximate; see the official transformation table). For almost all DEM work one ITRF is as good as another *provided the epoch is handled*; the difference between ITRFs is small, the difference between epochs is not.

The **IGS** (International GNSS Service) distributes its own realizations aligned to ITRF — IGS05, IGS08/IGb08, IGS14/IGb14, IGS20 — because satellite orbits and antenna calibrations have to be consistent with the frame; PPP solutions ([Chapter 12](ch12-gnss.md)) are in the IGS frame of the products used, at the epoch of observation.

**WGS84** is the US Department of Defense's frame, defined by the coordinates of the GPS tracking stations. Its realizations — the original Doppler-based WGS84 (1987), then **G730** (1994), **G873** (1997), **G1150** (2002), **G1674** (2012), **G1762** (2013), **G2139** (2021), and **G2296** (2024) — are aligned to the contemporary ITRF at the centimetre level or better (the "G" number is the GPS week of introduction). The original realization differed from ITRF by about 1–2 m; everything from G730 on agrees with ITRF to within a few centimetres and the recent ones to about a centimetre. Consequently "WGS84" in a file created with a geodetic receiver after 1994 means "ITRF-class coordinates at the epoch of observation, in a realization the author probably did not record". A file labelled EPSG:4326 therefore carries a hidden uncertainty of order 1 m from unknown realization and unknown epoch; this is why EPSG now treats WGS84 as an **ensemble** CRS (EPSG:4326 encompasses all realizations with a stated ensemble accuracy of 2 m) and offers per-realization codes (e.g., EPSG:9755 WGS 84 (G2139)).

Regional frames fall into two families. **Earth-fixed** frames move with the ITRS and require an epoch; **plate-fixed** frames are rotated with a tectonic plate so that coordinates of points on that plate stay nearly constant over time:

| Frame | Plate / alignment | Reference epoch | Relation to ITRF |
|---|---|---|---|
| NAD83(2011) epoch 2010.00 | North American plate | 2010.00 | ~1–2 m from ITRF2014; rotates with the plate |
| NAD83(CSRS) v8 | North American plate (Canada) | 2010.00 (v8) | same family as NAD83(2011), per-version differences at cm level |
| ETRS89 (ETRF2000, ETRF2014) | Eurasian plate, coincident with ITRS at 1989.0 | 1989.0 | diverging ~2.5 cm/yr; ≈ 0.8–0.9 m by the mid-2020s |
| GDA94 | ITRF92 at 1994.0, then plate-fixed | 1994.0 | ~1.8 m from ITRF2014 at 2020.0 |
| GDA2020 | ITRF2014 at 2020.0, plate-fixed | 2020.0 | 0 at 2020.0; ~7 cm/yr thereafter |
| JGD2011 | ITRF2008-aligned with post-Tohoku coordinates | 2011.4 (patched) | patch model; semi-dynamic corrections |
| SIRGAS2000 | ITRF2000 at 2000.4 | 2000.4 | South American plate ~1–2 cm/yr |
| NZGD2000 | ITRF96 at 2000.0, deformation model | 2000.0 | semi-dynamic; deformation model applied |

The practical rule is that a coordinate in a plate-fixed frame can be used without an epoch for most purposes (the residual intra-plate motion is millimetres per year, except near plate boundaries), while a coordinate in ITRF or WGS84 is incomplete without one.

> **Definitions that bite.** *Datum*, *reference system*, *reference frame*, and *realization* are used loosely and inconsistently. ISO 19111:2019 uses "datum" (or "reference frame") for the definition of how a CRS is tied to the Earth, and "realization" for a particular set of station coordinates implementing it; the IERS uses "system" for the conventions and "frame" for the realization. In practice: *ITRS* is a system; *ITRF2014* is a frame/realization; *NAD83* is a datum with realizations NAD83(1986), NAD83(HARN), NAD83(NSRS2007), NAD83(2011); *WGS84* is a datum with realizations G730…G2296. Software that offers only "NAD83" or "WGS84" has collapsed a family that spans 1–2 m into one name.

## 8.3 Epochs and velocities

Plates move at 1–10 cm per year. Over the 30 years between a 1994 survey and a 2024 one, that is 0.3–3 m — comparable to the entire error budget of a modern DEM and larger than the horizontal accuracy of lidar by an order of magnitude. Any coordinate in an Earth-fixed frame is therefore a four-dimensional quantity: $(x, y, z, t)$, and converting between epochs requires a **velocity**:

$$\mathbf{x}(t) = \mathbf{x}(t_0) + \dot{\mathbf{x}}\,(t - t_0) .$$

Where does $\dot{\mathbf{x}}$ come from? For a stable plate interior, from a **plate-motion model**: ITRF2014 came with a model giving Euler poles for 11 major plates fitted to the ITRF velocities (Altamimi et al. 2017), and ITRF2020 updated it. Horizontal velocities from such a model are good to about 1 mm/yr in plate interiors; vertical velocities are not included (vertical motion is treated in [Chapter 38](ch38-plate-motion-and-vlm.md)). Near plate boundaries, in deforming zones (the western United States, Japan, New Zealand, the Mediterranean), and after earthquakes, a plate model is wrong by centimetres per year and a **deformation model** is needed — a gridded velocity field, plus patches for coseismic and postseismic displacements.

The US tool for this is **HTDP** ⟨H⟩ (Horizontal Time-Dependent Positioning, first released 1992; Snay 1999; Pearson & Snay 2013), which combines a velocity model for the United States with a catalogue of earthquake displacement models and the frame transformations between ITRF, WGS84, and NAD83 realizations, allowing a coordinate to be moved between any two frames and any two epochs in one step. New Zealand's **NZGD2000** was designed from the outset (2000) as a **semi-dynamic datum**: coordinates are stored at epoch 2000.0, and the national deformation model (updated after the 2010–2011 Canterbury and 2016 Kaikōura earthquakes) is applied to convert observations at any epoch to and from the datum epoch. Japan's **semi-dynamic correction** (introduced by the Geospatial Information Authority in 2010) does the same for JGD2011, with annual parameter files. Australia's **GDA2020** is plate-fixed at 2020.0; alongside it the **Australian Terrestrial Reference Frame (ATRF)** is the Earth-fixed, time-dependent twin for users who need ITRF-compatible coordinates at the observation epoch.

The **modernized NSRS** in the United States replaces NAD83 with four plate-fixed frames — **NATRF2022** (North American), **PATRF2022** (Pacific), **CATRF2022** (Caribbean), and **MATRF2022** (Mariana) — each defined as a rotation of ITRF2020 about that plate's Euler pole. Coordinates will be published at a reference epoch (2020.00) together with an **intra-frame velocity model (IFVM)** so that users can move them to any epoch; the vertical component is in NAPGD2022 ([Chapter 7](ch07-shape-of-the-earth.md), [Chapter 9](ch09-vertical-datums.md)). The consequence for DEM producers is that "NAD83(2011) epoch 2010.00" products and "NATRF2022 epoch 2020.00" products will differ by roughly 1–2 m horizontally (the NAD83 offset from the geocentre) plus any motion between epochs, and must not be mosaicked without transformation.

> **Rule of thumb.** Plate velocities relative to ITRF: Australia ~7 cm/yr toward the NNE; India ~5 cm/yr; the stable interior of North America ~1.5–2 cm/yr to the WSW; Eurasia ~2.5 cm/yr to the NE; Pacific plate ~7–10 cm/yr to the NW. Coastal California moves at roughly 3–5 cm/yr relative to the North American interior across the San Andreas system. A decade therefore means 0.2–1 m of relative motion depending on where you are; if your work is at the half-metre level and spans a decade, epoch is not optional. The rule fails near plate boundaries and after earthquakes, where the only answer is a deformation model.

## 8.4 Transformations

### 8.4.1 Helmert (similarity) transformations

The **7-parameter Helmert transformation** maps Cartesian coordinates in one frame to another by a translation $\mathbf{T}$, a scale change $s$, and three small rotations:

$$\mathbf{x}' = \mathbf{T} + (1 + s)\,\mathbf{R}\,\mathbf{x}, \qquad \mathbf{R} \approx \begin{pmatrix} 1 & R_z & -R_y \\ -R_z & 1 & R_x \\ R_y & -R_x & 1 \end{pmatrix},$$

with rotations in radians (published in milliarcseconds, mas) and scale in parts per billion (ppb). This linearized form is accurate when the rotations are small (arc seconds), which is always the case between geocentric frames and usually between a geocentric frame and a classical datum. Two sign conventions coexist: the **position-vector** convention (ISO 19111, EPSG method 9606, IERS, most European usage) and the **coordinate-frame** convention (EPSG method 9607, US NGS and much US usage), which differ in the sign of all three rotations. Confusing them is harmless when the rotations are sub-mas and catastrophic when they are arc seconds: a 1″ rotation error moves a point at the Earth's surface by about 31 m.

Between ITRF and a plate-fixed frame the rotation rates are not negligible, so the **14-parameter** form adds a rate to each parameter:

$$p(t) = p(t_0) + \dot p\,(t - t_0), \qquad p \in \{T_x, T_y, T_z, s, R_x, R_y, R_z\}.$$

For example, the ITRF2014→NAD83(2011) transformation used by HTDP has translations of roughly (1.005, −1.909, −0.542) m, rotations of roughly (26.8, −0.4, 10.9) mas, scale near zero, and rotation rates of about (0.07, −0.76, −0.05) mas/yr at epoch 2010.0 (approximate — take the current values from HTDP or EPSG, and check the sign convention). The rotation rates are the plate motion expressed as an Euler rotation; applied over 14 years they move a point in Colorado by about 0.25 m.

A Helmert transformation fitted between a geocentric frame and a classical datum (ED50→ETRS89, Tokyo→JGD2000, AGD66→GDA94) is only as good as the classical network's internal consistency: residuals of 1–5 m are typical nationally, which is why IOGP's Guidance Note 7-2 publishes transformations with a stated accuracy and area of use, and why EPSG lists several alternative transformations for the same pair of datums.

### 8.4.2 Molodensky–Badekas and the abridged Molodensky

When a Helmert transformation is estimated from control points clustered in a small region, the translation and rotation parameters are highly correlated because rotations about the geocentre move the local points almost like translations. The **Molodensky–Badekas** form (EPSG method 9636) rotates about a chosen centroid $\mathbf{x}_0$ of the control points instead of the geocentre: $\mathbf{x}' = \mathbf{x}_0 + \mathbf{T} + (1+s)\mathbf{R}(\mathbf{x} - \mathbf{x}_0)$. It is mathematically equivalent to a Helmert transformation with different numerical parameters (and so cannot be inverted by simply changing signs). The **abridged Molodensky** formulas apply a 3-parameter translation directly in geodetic coordinates together with the ellipsoid change $\Delta a, \Delta f$; they are accurate to a few metres and survive in older software and some military standards. Neither is appropriate below the metre level.

### 8.4.3 Grid-shift transformations

When the difference between two datums is dominated by network distortion, the only accurate transformation is an empirical one: a **grid of shifts** interpolated bilinearly (or biquadratically) at the point of interest. **NADCON** (1990) did this for NAD27→NAD83 with latitude and longitude shift grids; **NTv2** (Canada, 1995) added nested sub-grids of different density and became the de-facto international format (used in Australia, Germany, Spain, Brazil, and elsewhere); **NADCON5** (NGS, 2016) extends the US grids to all historical NAD83 realizations and adds ellipsoidal-height shift grids with accompanying error grids (Dennis 2017). PROJ since version 7 stores grids as GeoTIFF with a documented layout, and PROJ-data hosts most national grids. A grid-shift transformation is as accurate as the control that built it — typically 0.1–0.5 m for NAD27→NAD83 in CONUS away from the grid's edges, versus several metres for the best Helmert fit.

### 8.4.4 Concatenation and "WGS84 to WGS84"

Most software cannot transform directly between arbitrary pairs of datums; it chains transformations through a **hub**, historically WGS84. The errors of each link add in quadrature at best and in bias at worst. Consider NAD27→NAD83(2011) via WGS84: NAD27→WGS84 is a 3-parameter transformation accurate to about 5 m (EPSG lists several); WGS84→NAD83 is often a *null* transformation (the two were coincident in 1986) accurate to about 1–2 m today. The result is good to 5 m, whereas the direct NADCON5 route is good to 0.2 m. **PROJ ≥ 6** with its EPSG-driven `proj_create_crs_to_crs` avoids the WGS84 hub when a direct path exists and reports the accuracy of each candidate operation (`projinfo -s EPSG:4267 -t EPSG:6318 --spatial-test intersects`); older GDAL/PROJ (≤ 5) always went through WGS84 with the `+towgs84` parameters, and files produced by that era carry the hub's errors.

The null transformation deserves its own warning. "WGS84 to WGS84" is an identity only if realization and epoch match. WGS84 (original, 1987) to WGS84 (G1762) is ~1–2 m. ITRF2014 at 2024.0 to ITRF2014 at 2010.0 is 1 m in Australia. NAD83(2011) treated as WGS84 (as thousands of shapefiles do) is ~1–2 m, with a direction that rotates across the continent. Each of these is a real, directional error that a software "null transformation" silently sets to zero.

<!-- figure: Figure 8.2 — Vector map of the NAD83(2011)–ITRF2014 (epoch 2020.0) horizontal difference across CONUS, with arrows of 1–2 m, illustrating that the "null" WGS84↔NAD83 transformation is not null and not uniform. -->

## 8.5 Encoding CRSs

A transformation is only as good as the description of its endpoints, and the history of CRS encoding is a history of descriptions that could not say enough.

**EPSG** ⟨H⟩. The European Petroleum Survey Group began compiling geodetic parameters in 1985 and released the first public version of its database in 1993; since 2005 it has been maintained by IOGP as the **EPSG Geodetic Parameter Dataset**. It assigns integer codes to ellipsoids, datums, CRSs, transformations, and units, and — importantly — records each transformation's accuracy, area of use, and source. The codes have become the lingua franca of GIS, with the side effect that users treat "EPSG:4326" as a complete specification when it is an ensemble spanning 2 m.

**WKT1 → WKT2.** The original **Well-Known Text** (OGC 01-009, 2001) encoded a CRS as nested keywords; its two dialects (OGC and Esri) disagreed on names and parameters, it could not express a datum realization, an epoch, a vertical CRS tied to a geoid model, or axis order unambiguously, and it embedded the WGS84 hub via `TOWGS84[...]`. **WKT2** (ISO 19162:2015, revised as ISO 19162:2019, "WKT2:2019") fixes these: it carries `DATUM`/`ENSEMBLE`, `DYNAMIC[FRAMEEPOCH[...]]`, explicit `AXIS` order, `USAGE`/`AREA`/`BBOX`, `BOUNDCRS` for a CRS packaged with a specific transformation, `COMPOUNDCRS` for horizontal plus vertical, and `COORDINATEMETADATA` with an epoch. A DEM's CRS should be written in WKT2:2019; GeoTIFF 1.1 (OGC 19-008r4, 2019) allows it in the GeoTIFF keys ([Chapter 10](ch10-projections-and-resampling.md), [Chapter 47](ch47-file-formats.md)).

**PROJJSON** is PROJ's JSON rendering of the same model (introduced in PROJ 6.2, 2019); it is lossless with WKT2 and easier to parse and validate in software. Both are preferable to a bare EPSG code in metadata, because the code can be looked up but a WKT2 string survives a change of registry version.

**The axis-order wars.** EPSG:4326 is defined with axis order latitude, longitude (north, east), following the geodetic convention and ISO 19111. Most software of the 1990s–2010s wrote and read it as longitude, latitude, because that is x, y. GDAL 3 / PROJ 6 (2019) switched to honouring the authority's axis order unless told otherwise (`OAMS_TRADITIONAL_GIS_ORDER`), and a great many pipelines broke. The failure mode is not subtle — points land in the ocean off Somalia or at the wrong pole — but the quiet version is: a WKT1 string that *claims* lon/lat order being handed to a WKT2-aware library that *assumes* the authority's lat/lon. Always set axis order explicitly in code (`pyproj.Transformer.from_crs(..., always_xy=True)`) and write it explicitly in WKT2.

**Bound and compound CRSs.** A **compound CRS** (EPSG:5498 = NAD83 + NAVD88 height; EPSG:9518 = WGS 84 + EGM2008 height; EPSG:7415 = Amersfoort/RD New + NAP height) is the correct way to state that a DEM's horizontal coordinates are in one CRS and its heights in a vertical CRS — and the only way to make a transformation engine apply the geoid grid automatically. A **bound CRS** packages a CRS with one specific transformation to a hub (the WKT2 successor of `TOWGS84`), which is useful for documenting exactly which transformation was applied but should not be the published CRS of a product. Shapefile `.prj` files are WKT1 and can express none of this; a lidar LAS 1.4 file can carry WKT (and should carry a compound CRS; [Chapter 47](ch47-file-formats.md)); a GeoTIFF can carry a compound CRS since GeoTIFF 1.1.

> **Try it.** Ask PROJ what it will actually do, and how well, before trusting any transformation:
>
> ```bash
> # Candidate operations NAD27 → NAD83(2011), with accuracies and grids
> projinfo -s EPSG:4267 -t EPSG:6318 --spatial-test intersects -o PROJ --summary
> # Expect several candidates: NADCON5 pipelines (~0.15–0.5 m) listed before
> # the 3-parameter Helmert via WGS84 (~5 m). If only the Helmert appears,
> # PROJ-data grids are missing or PROJ_NETWORK is off.
>
> # Time-dependent: ITRF2014 @2024.5 → NAD83(2011) @2010.0 (epoch given as 4th coord)
> echo "-105.0 40.0 1600.0 2024.5" | cs2cs EPSG:7912 EPSG:6319 -d 4
> # Horizontal shift ≈ 1.2–1.5 m in Colorado; height changes by ~0.6–1.0 m.
>
> # Compound CRS with a vertical grid: NAD83(2011)+NAVD88 → ITRF2014 ellipsoidal
> projinfo -s EPSG:6349 -t EPSG:7912 --summary
> ```
>
> Expected outcome: the summaries list operation names, accuracy in metres, and area of use. The exercise is to notice that the accuracy field is populated for grid shifts and Helmerts but is *unknown* for ensembles and null transformations — "unknown" means "assume metres".

## 8.6 Horizontal control

Datums are abstract; **control networks** are how they reach the ground. The classical method was **triangulation**: measure one or a few baselines precisely (with bars, tapes, or invar wires), measure all the angles of a chain of triangles with a theodolite, and propagate position and scale through the chain. The **Principal Triangulation of Great Britain** ⟨H⟩ ran from 1791 to 1853 under the Ordnance Survey (Roy's Hounslow Heath baseline of 1784 preceded it); the **Great Trigonometrical Survey of India** (1802–1871, Lambton then Everest) carried a meridian arc 2 400 km from Cape Comorin to the Himalaya and incidentally measured the height of Peak XV. Triangulation's weakness is scale: it is controlled only at the baselines, so scale error accumulates with distance from them, and that accumulation is one of the distortions buried in NAD27 and ED50. **Trilateration** (measuring sides with electronic distance measurement, from the 1950s) and **traverses** (measuring angles and distances along a line) filled the gaps; mid-century readjustments (NAD83, ED87) incorporated them.

Satellite methods began with **Doppler** tracking of the TRANSIT satellites (1960s–1980s, metre-level geocentric positions that first revealed the offsets of the classical datums) and matured with GPS. The modern network layer is the **continuously operating reference station** (CORS): a permanent GNSS receiver whose data are archived and whose coordinates and velocities are computed continuously. NGS established the US CORS network in 1994 (Snay & Soler 2008); the IGS network provides the global tie; most countries now operate national CORS networks (EUREF Permanent Network, GEONET in Japan with ~1 300 stations, AUSPOS/APREF in Australia, CACS in Canada, PositioNZ). The frame of a modern survey is, in practice, the frame and epoch of the CORS coordinates it was processed against, which is why "processed with OPUS in 2015" implies NAD83(2011) epoch 2010.00 and "processed with CSRS-PPP in 2015" implies ITRF2008 at the observation epoch unless the user asked for NAD83(CSRS).

The physical monuments of the older networks — brass disks in concrete, with published coordinates — remain in use as **passive control**; their published positions are in whatever realization was current when they were last adjusted, and unless the agency has recomputed them they drift away from the active network at the plate rate. Decade-old passive control in California can be 0.3 m from a modern CORS-based position in the same nominal datum. In the modernized NSRS, passive marks will no longer define the frame; they will have coordinates derived from and checked against the CORS network.

## 8.7 Horizontal accuracy of DEMs

Vertical accuracy gets the attention, but horizontal error is rarely innocuous, because it converts to vertical error through slope:

$$\Delta z \approx \Delta_{xy}\,\tan\beta ,$$

where $\Delta_{xy}$ is the horizontal displacement and $\beta$ the terrain slope. A 5 m horizontal shift on a 30° slope is 2.9 m of apparent vertical error; on a 5° slope it is 0.44 m. This is why SRTM "vertical error" assessed against GNSS checkpoints is dominated in mountains by SRTM's horizontal geolocation, why DEM-of-difference change detection must co-register the two surfaces before differencing ([Chapter 41](ch41-change-detection.md)), and why ASPRS accuracy standards require horizontal accuracy to be assessed and reported separately for lidar (where it is otherwise invisible, since there are no visible pixels to check).

**How it is tested.** Three families of method:

1. **Feature-based.** Identify well-defined features visible in the DEM or its derivatives (hillshade, slope, intensity): building corners, road intersections, culvert ends, surveyed targets. Compare their DEM coordinates with surveyed ones. This is the ASPRS method for orthoimagery and works for lidar via intensity images or planar-roof intersections; it needs ~20 or more checkpoints for a meaningful RMSE$_{xy}$ ([Chapter 53](ch53-accuracy-assessment.md)).
2. **Co-registration by surface matching.** Nuth & Kääb (2011) showed that a horizontal offset between two DEMs produces an elevation-difference field whose dependence on terrain aspect is sinusoidal, with amplitude proportional to the shift and slope; fitting $dh/\tan\beta = a\cos(b - \psi) + c$ over aspect $\psi$ recovers the shift vector $(a, b)$ and a vertical bias $c$ in a few iterations. **ICP** (iterative closest point) and least-squares surface matching do the same in 3D. **xdem** and **demcoreg** implement these; they are the standard for glacier and change studies and resolve shifts to a small fraction of a cell.
3. **Cross-correlation.** Normalized cross-correlation of hillshades, slope maps, or intensity between the DEM and a reference image recovers sub-pixel shifts in flat-featured areas where surface matching fails for lack of relief; it is the method behind many DEM mosaicking pipelines.

**Typical values.** SRTM's absolute horizontal accuracy was assessed at about 9 m CE90 globally against the 20 m specification (Rodríguez et al. 2006). The Copernicus DEM product handbook specifies absolute horizontal accuracy better than 6 m CE90 (Airbus 2020, and later revisions). Airborne lidar at 1–2 m point spacing routinely achieves 0.1–0.5 m RMSE$_{xy}$ when boresight and GNSS/INS are well calibrated, and the USGS Lidar Base Specification requires horizontal accuracy to be reported following ASPRS (2014/2023) procedures. Photogrammetric DSMs inherit the horizontal accuracy of their ground control or of their direct georeferencing, typically 0.5–2 GSD. Satellite stereo DEMs without ground control (ArcticDEM, REMA strips) can be offset by several metres before co-registration to altimetry, which is why those products ship with a registration step.

> **Worked example.** Two 2 m lidar DTMs of a hillside (mean slope 22°) are differenced to detect landslide movement. The raw DEM-of-difference has a mean of +0.03 m and a σ of 0.41 m. A Nuth–Kääb fit returns a horizontal shift of 0.62 m at azimuth 148° and a vertical bias of −0.02 m between the two epochs. Expected vertical signature of that shift on a 22° slope: $0.62\tan 22° = 0.25$ m, aspect-dependent. After applying the shift and re-differencing, σ drops to 0.19 m, and the residual pattern no longer correlates with aspect. The 0.62 m shift is less than a third of a cell; it was invisible by inspection, consistent with both DTMs meeting a 1 m horizontal specification, and responsible for over half the apparent change variance. [Chapter 41](ch41-change-detection.md) continues this example into minimum detectable change.

## Then & now

- **Origin-station datums → geocentric frames.** NAD27 ⟨H⟩ (1927), ED50 (1950), Tokyo, AGD66, and their contemporaries were anchored at a point and distorted by their triangulation; satellite Doppler (1960s–70s) measured their geocentric offsets; NAD83, WGS84, and ITRF (1986–1988) made the geocentre the origin.
- **One WGS84 → a family.** WGS84 (1987) was metre-level; G730 (1994) aligned it to ITRF at the decimetre level; G1150 (2002) onward at the centimetre level; EPSG's ensemble concept (2020) formalized the ambiguity of the name.
- **Static → dynamic.** ITRF has carried station velocities since ITRF91; HTDP ⟨H⟩ (1992) brought time dependence to practitioners; NZGD2000 (2000) was the first national semi-dynamic datum; Japan's semi-dynamic correction (2010), ATRF (2017), and the 2022 NSRS frames make epoch a mandatory coordinate.
- **Helmert → grids → time-dependent grids.** 7-parameter fits dominated through the 1980s; NADCON (1990) and NTv2 (1995) made distortion grids standard; NADCON5 (2016) added error grids; deformation-model grids (New Zealand, Japan, Australia's GDA2020 conformal + distortion grids) now carry time as well.
- **Encoding.** EPSG ⟨H⟩ (1985/1993) → WKT1 (2001) → WKT2 (2015/2019) and PROJJSON (2019); GeoTIFF 1.1 (2019) and LAS 1.4 (2011) can finally carry a compound CRS with realization and epoch.
- **Control.** Triangulation (GB 1791–1853 ⟨H⟩; India 1802–1871) → EDM traverses (1950s) → Doppler (1967–1990s) → GPS campaigns (1980s) → CORS (1994) → real-time networks and PPP (2000s–2020s). Passive marks went from *being* the datum to being checked against it.

## Mathematics

**Helmert transformation, exact and linearized.** With a rotation matrix $\mathbf{R} = \mathbf{R}_z(R_z)\mathbf{R}_y(R_y)\mathbf{R}_x(R_x)$ and scale factor $(1+s)$, the exact similarity transformation is $\mathbf{x}' = \mathbf{T} + (1+s)\mathbf{R}\mathbf{x}$. For small angles (position-vector convention),

$$\begin{pmatrix} X' \\ Y' \\ Z' \end{pmatrix} = \begin{pmatrix} T_x \\ T_y \\ T_z \end{pmatrix} + (1+s)\begin{pmatrix} 1 & -R_z & R_y \\ R_z & 1 & -R_x \\ -R_y & R_x & 1 \end{pmatrix}\begin{pmatrix} X \\ Y \\ Z \end{pmatrix},$$

and the coordinate-frame convention negates the three rotation angles. Units: $\mathbf{T}$ in metres, $s$ dimensionless (1 ppb = $10^{-9}$), rotations in radians ($1\ \text{mas} = 4.848\times10^{-9}$ rad). The approximate inverse is obtained by negating all seven parameters; the error of that approximation is of order $s^2$ and $R^2$, i.e. negligible for geocentric-to-geocentric but not for arc-second rotations. Effect of each parameter at the Earth's surface ($R_E \approx 6.37\times10^6$ m): 1 ppb of scale → 6.4 mm radially; 1 mas of rotation → 31 mm tangentially; 1 m of $T_z$ → up to 1 m in height at the poles and in latitude at the equator.

**Time-dependent (14-parameter) form.** Each parameter $p$ has a rate $\dot p$ referred to $t_0$; apply at the epoch $t$ of the coordinates: $p(t) = p(t_0) + \dot p (t - t_0)$. The full chain from frame A at epoch $t_A$ to frame B at epoch $t_B$ is: propagate $\mathbf{x}_A(t_A) \to \mathbf{x}_A(t)$ with the velocity in frame A; apply the Helmert transformation evaluated at $t$; propagate in frame B from $t$ to $t_B$ with the velocity in B. For a point moving with a rigid plate of Euler vector $\boldsymbol{\Omega}$ (rad/yr), the velocity is $\dot{\mathbf{x}} = \boldsymbol{\Omega}\times\mathbf{x}$; a plate-fixed frame is one in which $\boldsymbol{\Omega}_{plate}$ has been absorbed into the frame's rotation rates so that $\dot{\mathbf{x}} \approx 0$.

**Grid-shift interpolation.** A shift grid stores $(\Delta\varphi, \Delta\lambda)$ (NTv2: in arc seconds, with longitude positive *west* in the original specification — a classic sign trap) or $(\Delta X, \Delta Y, \Delta Z)$ at nodes. For a point at fractional grid position $(u, v)$ within a cell with corner values $f_{00}, f_{10}, f_{01}, f_{11}$, bilinear interpolation gives

$$f(u,v) = (1-u)(1-v)f_{00} + u(1-v)f_{10} + (1-u)v\,f_{01} + uv\,f_{11}.$$

The forward direction is exact at the nodes; the inverse (target→source) is solved iteratively, since the shift must be evaluated at the unknown source position; two or three iterations converge to sub-millimetre. NADCON5 ships $\sigma$ grids that should be interpolated the same way and carried into the uncertainty budget.

**Worked numbers: scale and rotation.** Suppose a transformation is applied with the scale sign reversed, $s = +0.37$ ppb instead of $-0.37$ ppb. The radial error is $2\times0.37\times10^{-9}\times6.37\times10^6 = 4.7$ mm — invisible. Now suppose the rotations of ITRF2014→NAD83(2011), $(26.8, -0.4, 10.9)$ mas, are applied with the wrong sign convention. The tangential error is twice the rotation: at $|\mathbf{R}| \approx 28.9$ mas, $2\times28.9\times4.848\times10^{-9}\times6.37\times10^6 = 1.78$ m. Translations are unaffected by the convention, so the result is a position that is wrong by nearly 2 m but looks plausible because the translation moved it the expected ~1.5 m. Only a check against a known point in the target frame catches this.

## Validation & uncertainty

### How errors arise

- **Unknown or wrong realization.** "NAD83" that is actually NAD83(1986) (HARN-era differences up to ~1 m in some states), "WGS84" that is actually NAD83(2011) (~1–2 m), ETRS89 that is actually ITRF at the observation epoch (0.8–0.9 m in 2025). These are biases with a regionally consistent direction.
- **Unknown or ignored epoch.** 1–10 cm/yr times the number of years. In Australia between GDA94 and GDA2020, 1.8 m; in Japan after Tohoku, up to 5.3 m horizontally near the Pacific coast (GSI).
- **Transformation chain through a hub.** Adds the accuracy of each link; the WGS84 hub with a null NAD83↔WGS84 link contributes 1–2 m.
- **Wrong sign convention or units** for Helmert rotations (metres of error for arc-second rotations), wrong longitude sign in NTv2 grids, degrees versus radians, feet versus metres in projected coordinates (US survey foot vs international foot: 2 ppm, which is 0.6 m at a false easting of 300 km… and a reason the US survey foot was deprecated in 2023).
- **Grid edges and extrapolation.** Shift grids are undefined or extrapolated beyond their extent; software may fall back silently to a Helmert transformation or to null at the edge, producing a step of metres along a straight line (visible in a mosaic as a shear).
- **Axis order.** Swapped coordinates, or — more insidiously — a grid or raster whose stated CRS has one axis order while its geotransform assumes another, producing data that look right in one tool and are transposed in another.

### How they propagate

Horizontal errors propagate to vertical via slope ($\Delta z \approx \Delta_{xy}\tan\beta$), to volumes via the area-weighted slope, to change detection as aspect-correlated artefacts, and to merged products as shears at boundaries. A 1 m frame error across a 50 m wide river channel in a hydrodynamic model moves the bank by two cells at 0.5 m resolution; in flat farmland the same error is harmless. The horizontal error that matters is therefore the one that is *inconsistent* between datasets being combined — a 1.5 m NAD83↔ITRF offset applied uniformly to a project is harmless until someone overlays data in the other frame.

### How to test

1. **Independent checkpoints** in a known frame and epoch (surveyed targets, photo-identifiable points), processed to the DEM's declared CRS with a documented transformation; compute RMSE$_x$, RMSE$_y$, RMSE$_r$, and the mean offset vector. A mean offset that is significant relative to the RMSE is a datum problem, not a noise problem.
2. **Co-registration against a trusted reference DEM** (Nuth–Kääb or ICP) over stable terrain; the recovered shift vector is the datum discrepancy plus any sensor geolocation error.
3. **Transformation round-trip test**: transform a set of coordinates A→B→A with the operations the software actually selected (`projinfo` lists them), and confirm the residual is at the millimetre level; large residuals mean a non-invertible chain or a hub.
4. **Epoch sensitivity**: transform the same coordinate with the epoch set to the survey date and to the datum's reference epoch; the difference is the correction you need to make or document.
5. **Metadata audit**: does the WKT state the realization and epoch? Is the vertical CRS part of a compound CRS? If not, the achievable accuracy is bounded by the ensemble accuracy (2 m for EPSG:4326).

> **Uncertainty budget.** Horizontal position of a lidar DEM cell, delivered in NAD83(2011) / UTM, assessed against GNSS checkpoints. Indicative 1σ values; see the cited sources for specifics.
>
> | Component | 1σ (m) | Character | Source |
> |---|---|---|---|
> | GNSS/INS trajectory and boresight, 1 500 m AGL | 0.10–0.25 | per-strip bias + noise | [Chapter 18](ch18-topographic-lidar.md) |
> | Checkpoint survey (RTK, NAD83(2011) via CORS) | 0.02–0.03 | random | [Chapter 12](ch12-gnss.md) |
> | NAD83(2011) realization vs frame truth | 0.01–0.02 | negligible | NGS |
> | Epoch (if ITRF data without epoch, CONUS interior) | 0.015–0.02 per year | bias, directional | plate motion model |
> | Epoch, coastal California, decade | 0.3–0.5 | bias, directional | HTDP |
> | "Null" NAD83↔WGS84 if applied | 1.0–2.0 | bias, directional | this chapter |
> | NADCON5 NAD27→NAD83 (if legacy control) | 0.15–0.5 | smooth field | Dennis 2017 |
> | **Total, consistent frame and epoch** | **~0.10–0.25** | — | RSS of rows 1–3 |
> | **Total, with one ignored null transformation** | **1–2** | dominated by bias | — |

### What to report

Realization and epoch of the horizontal CRS; the transformation operation(s) applied, by EPSG code or PROJ pipeline string, with the accuracy EPSG assigns to them; the frame and epoch of checkpoints; RMSE$_x$, RMSE$_y$, RMSE$_r$ and the mean offset vector; the co-registration shift if one was applied to any input. Write the CRS as WKT2:2019 or PROJJSON, not as a bare code.

## Software

**Open source.**
- **PROJ** (≥ 9 recommended) and **pyproj**: the reference implementation of EPSG operations, WKT2/PROJJSON, time-dependent Helmert (`+proj=helmert +t_epoch`), deformation models (`+proj=deformation`, `+proj=defmodel` for the GGXF-style NZ/AU/JP models), and grid shifts (`hgridshift`, `vgridshift`, `xyzgridshift`). Caveat: results depend on which grids are installed; `projinfo --summary` and `PROJ_DEBUG=2` tell you what was actually used, and a missing grid may silently degrade to a Helmert or null operation unless you use `proj_create_crs_to_crs` with `ONLY_BEST=YES` (PROJ ≥ 9.2).
- **GeographicLib**: exact geodesic, geocentric↔geodetic, and local Cartesian conversions used as the numerical backbone by many tools; `CartConvert` and `GeodSolve` are handy for checking a transformation's geometry independently of PROJ.
- **NGS NCAT** (web and API) and **HTDP** (Fortran, free source): authoritative for US frames and epochs, including earthquake displacement models; HTDP is the only tool that knows every historical NAD83 realization. Caveat: HTDP's velocity model is for horizontal motion; vertical velocities are separate and less certain.
- **GEOTRANS** (NGA, free source): military-standard datum transformations and projections; lineage of many of the 3-parameter transformations still in EPSG. Caveat: metre-class transformations by design.
- **GDAL** (`gdalwarp -s_srs/-t_srs`, `-ct` for an explicit PROJ pipeline): applies all of the above to rasters; use `-ct` when you must control which operation is applied rather than letting PROJ choose.
- **xdem**, **demcoreg**: Nuth–Kääb and ICP co-registration of DEMs, with the shift vector reported and optionally applied; essential for §8.7 testing.

**Free but closed.** NGS OPUS (positions in NAD83(2011) and ITRF2014 with epoch); NRCan CSRS-PPP; Geoscience Australia AUSPOS; LINZ's online coordinate converter with the NZGD2000 deformation model; GSI's semi-dynamic correction tool (Japan).

**Commercial.** Blue Marble Geographic Calculator (the broadest commercial transformation library, including proprietary national grids; caveat: parameter provenance is less transparent than EPSG's); Trimble Coordinate System Manager and Leica Infinity (bundled datum databases that may lag EPSG by a release; a project "site calibration" can mask a datum error entirely — [Chapter 9](ch09-vertical-datums.md)); Esri ArcGIS Pro and QGIS transformation pickers (both now driven by PROJ/EPSG; the picker's default is the operation EPSG ranks first *for the area of use you specified*, so specify it).

## Standards & guides

- **ISO 19111:2019** *Geographic information — Referencing by coordinates* — the conceptual model: datums, ensembles, dynamic reference frames, coordinate epochs, compound and bound CRSs.
- **ISO 19162:2019** *Well-known text representation of coordinate reference systems* (WKT2:2019) — the text encoding of the ISO 19111 model.
- **OGC 18-005r4** (the OGC publication of ISO 19111:2019) and **OGC 18-010r7** (WKT2:2019) — the openly accessible editions.
- **IOGP Geomatics Guidance Note 7-2 (373-07-2)** *Coordinate Conversions and Transformations including Formulas* — the formulas behind every EPSG method code (Helmert variants, Molodensky–Badekas, grid interpolation, projections); revised regularly, so cite the revision you used.
- **EPSG Geodetic Parameter Dataset** (IOGP), with its *Guidance Note 7-1* (Using the EPSG Dataset) — the registry; note each transformation's accuracy and area of use.
- **IERS Conventions (2010)**, IERS Technical Note 36 — ITRS definition, transformation parameters between ITRFs, station motion models.
- **NGS Blueprint for 2022, Part 1 (NOAA TR NOS NGS 62)** — definition of NATRF2022 and the sister frames, Euler pole approach, intra-frame velocity model.
- **ICSM GDA2020 Technical Manual** (Intergovernmental Committee on Surveying and Mapping, v1.8) — GDA94→GDA2020 conformal and distortion grids, ATRF, and uncertainty statements.
- **LINZ Standard LINZS25000** *Standard for New Zealand Geodetic Datum 2000*, which incorporates the NZGD2000 deformation model (published separately with versioned releases).
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data** (Edition 1, 2014; Edition 2, 2023) — horizontal accuracy classes, testing with checkpoints, and reporting of RMSE$_x$, RMSE$_y$, RMSE$_r$.

## Pitfalls

- **Ignoring epoch.** Treating ITRF/WGS84 coordinates from different years as the same frame → metres in Australia, decimetres per decade in California, centimetres per year everywhere. Detect by a uniform shift between datasets whose magnitude scales with their time separation; avoid by recording the observation epoch and propagating to a common one.
- **Accepting the default null WGS84↔NAD83 (or WGS84↔ETRS89) transformation.** Software offers it because the datums coincided once; today it is 1–2 m (NAD83) or ~0.9 m (ETRS89). Detect by comparing to CORS-based control; avoid by selecting the time-dependent Helmert or the NADCON5/ETRF path explicitly.
- **Applying a 2D transformation to 3D data.** A horizontal grid shift or 2D Helmert leaves ellipsoidal heights in the source frame; NAD83→ITRF height differences are 0.5–2 m. Detect through a systematic height offset that varies smoothly across the continent; avoid by transforming in 3D (geocentric) or with a transformation that includes a height grid.
- **Shapefile `.prj` as the CRS of record.** WKT1 cannot express realization, epoch, or vertical CRS; "GCS_North_American_1983" could be any of five realizations. Detect by asking; avoid by shipping WKT2/PROJJSON in metadata and in formats that support it (GeoPackage, GeoTIFF 1.1, LAS 1.4, COPC).
- **Copying an EPSG code without its axis order.** EPSG:4326 is lat/lon; most code assumes lon/lat. Detect by points landing in the wrong hemisphere or on a 180°-rotated Earth; avoid with `always_xy=True` and explicit AXIS in WKT2.
- **Wrong rotation sign convention.** Position-vector vs coordinate-frame Helmert conventions produce errors of $2\times$ the rotation (1.8 m for ITRF→NAD83). Detect by testing a known point; avoid by using the EPSG method code (9606 vs 9607), not just the numbers.
- **Chaining transformations through WGS84 when a direct one exists.** Each hub link adds its error. Detect with `projinfo`; avoid with PROJ ≥ 6 and installed grids.
- **Grid-shift edge effects.** Outside the grid, software may extrapolate, revert to Helmert, or do nothing. Detect by a linear discontinuity in a mosaic that coincides with the grid boundary; avoid by checking the grid's extent against the project and choosing a grid that covers it (NTv2 sub-grids, NADCON5 regional grids).
- **Mixing feet.** US survey foot vs international foot differ by 2 ppm; State Plane coordinates in the wrong foot are off by 0.3–1 m at typical false eastings. Detect by a uniform offset proportional to the coordinate value; avoid by reading the unit from the CRS definition, not from habit.
- **Passive control at the wrong epoch.** A benchmark's published NAD83(2011) coordinates are at epoch 2010.00; measuring to it in 2024 with ITRF-based RTK and treating the difference as an error leads to a false "calibration" of up to 0.3–0.5 m in deforming regions. Avoid by propagating published coordinates to the survey epoch with HTDP (or equivalent).
- **Assuming horizontal error does not matter for a DEM.** On slopes it converts to vertical error at $\tan\beta$; in change detection it produces aspect-correlated fake change. Detect with a Nuth–Kääb plot of $dh/\tan\beta$ against aspect; avoid by co-registering before differencing and reporting the shift.
- **Treating "WGS84 (G1762)" as different from ITRF2008/2014 for practical purposes.** The opposite mistake: they agree to ~1 cm, and inventing a transformation between them with parameters copied from a forum can insert decimetres. Use the EPSG null-with-stated-accuracy operation and record it.

## Key takeaways

- A horizontal datum is frame + realization + epoch; a coordinate missing any of the three has an uncertainty of order a metre (ensemble WGS84) or a growing one (missing epoch).
- NAD27→NAD83 and the other classical-to-geocentric shifts exceed 100 m and are not smooth; use grid shifts (NADCON5, NTv2) and expect 0.1–0.5 m accuracy, not Helmert fits at several metres.
- All WGS84 realizations since G730 (1994) agree with ITRF at the centimetre to decimetre level; NAD83, ETRS89, and GDA are plate-fixed frames offset from ITRF by about 1–2 m, 0.9 m, and (GDA2020 at 2020.0) zero but growing at 7 cm/yr.
- The plate beneath you moves about as fast as your fingernails grow; decade-old control shows it, and sub-metre work spanning years needs an explicit epoch and velocity or deformation model.
- Helmert transformations have two sign conventions; using the wrong one doubles the rotation error — nearly 2 m for ITRF→NAD83.
- "WGS84 to WGS84" and "NAD83 to WGS84 (null)" are not identity transformations; let PROJ choose the best available operation and read the accuracy it reports.
- Encode CRSs in WKT2:2019 or PROJJSON with explicit axis order, realization, epoch, and a compound vertical CRS; a shapefile `.prj` cannot carry what a modern DEM needs.
- Horizontal error becomes vertical error on slopes ($\Delta z \approx \Delta_{xy}\tan\beta$); test it with checkpoints, co-registration, or cross-correlation, and report RMSE$_r$ and the mean offset vector separately.

## References

- Airbus Defence and Space (2020). *Copernicus DEM — Copernicus Digital Elevation Model Product Handbook*, GEO.2018-1988-2, v1.0 (later revisions are published through the Copernicus Data Space Ecosystem).
- Altamimi, Z., Rebischung, P., Métivier, L., & Collilieux, X. (2016). ITRF2014: A new release of the International Terrestrial Reference Frame modeling nonlinear station motions. *Journal of Geophysical Research: Solid Earth*, 121(8):6109–6131. doi:10.1002/2016JB013098
- Altamimi, Z., Métivier, L., Rebischung, P., Rouby, H., & Collilieux, X. (2017). ITRF2014 plate motion model. *Geophysical Journal International*, 209(3):1906–1912. doi:10.1093/gji/ggx136
- Altamimi, Z., Rebischung, P., Collilieux, X., Métivier, L., & Chanard, K. (2023). ITRF2020: an augmented reference frame refining the modeling of nonlinear station motions. *Journal of Geodesy*, 97:47. doi:10.1007/s00190-023-01738-w
- ASPRS (2023). *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2. American Society for Photogrammetry and Remote Sensing. (Edition 1: *Photogrammetric Engineering & Remote Sensing* 81(3):A1–A26, 2015.)
- Blick, G., Crook, C., Grant, D., & Beavan, J. (2005). Implementation of a semi-dynamic datum for New Zealand. In: Sansò, F. (ed.), *A Window on the Future of Geodesy*, IAG Symposia 128, Springer, pp. 38–43.
- Craymer, M. R. (2006). The evolution of NAD83 in Canada. *Geomatica*, 60(2):151–164.
- Dennis, M. L. (2017). *NADCON 5.0: Geometric Transformation Tool for Points in the National Spatial Reference System*. NOAA Technical Report NOS NGS 63. NOAA, Silver Spring.
- ICSM (2023). *Geocentric Datum of Australia 2020 Technical Manual*, version 1.8. Intergovernmental Committee on Surveying and Mapping, Canberra.
- Iliffe, J., & Lott, R. (2008). *Datums and Map Projections for Remote Sensing, GIS and Surveying* (2nd ed.). Whittles Publishing, Dunbeath.
- IOGP. *Coordinate Conversions and Transformations including Formulas*. Geomatics Guidance Note 7, part 2 (373-07-2), revised regularly. International Association of Oil & Gas Producers.
- ISO (2019). *ISO 19111:2019 Geographic information — Referencing by coordinates*. International Organization for Standardization, Geneva.
- ISO (2019). *ISO 19162:2019 Geographic information — Well-known text representation of coordinate reference systems*. International Organization for Standardization, Geneva.
- Nuth, C., & Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5(1):271–290. doi:10.5194/tc-5-271-2011
- Pearson, C., & Snay, R. (2013). Introducing HTDP 3.1 to transform coordinates across time and spatial reference frames. *GPS Solutions*, 17(1):1–15. doi:10.1007/s10291-012-0255-y
- Petit, G., & Luzum, B. (eds.) (2010). *IERS Conventions (2010)*. IERS Technical Note 36. Verlag des Bundesamts für Kartographie und Geodäsie, Frankfurt am Main.
- Rodríguez, E., Morris, C. S., & Belz, J. E. (2006). A global assessment of the SRTM performance. *Photogrammetric Engineering & Remote Sensing*, 72(3):249–260.
- Schwarz, C. R. (ed.) (1989). *North American Datum of 1983*. NOAA Professional Paper NOS 2. National Geodetic Survey, Rockville.
- Snay, R. A. (1999). Using the HTDP software to transform spatial coordinates across time and between reference frames. *Surveying and Land Information Systems*, 59(1):15–25.
- Snay, R. A., & Soler, T. (2008). Continuously Operating Reference Station (CORS): History, applications, and future enhancements. *Journal of Surveying Engineering*, 134(4):95–104. doi:10.1061/(ASCE)0733-9453(2008)134:4(95)
- Soler, T., & Hothem, L. D. (1988). Coordinate systems used in geodesy: Basic definitions and concepts. *Journal of Surveying Engineering*, 114(2):84–97.
- Soler, T., & Snay, R. A. (2004). Transforming positions and velocities between the International Terrestrial Reference Frame of 2000 and North American Datum of 1983. *Journal of Surveying Engineering*, 130(2):49–55.
- National Geodetic Survey (2017, rev. 2021). *Blueprint for 2022, Part 1: Geometric Coordinates*. NOAA Technical Report NOS NGS 62.
- NIMA (2000). *Department of Defense World Geodetic System 1984: Its Definition and Relationships with Local Geodetic Systems*. Technical Report TR8350.2, 3rd ed. (and NGA.STND.0036_1.0.0_WGS84, 2014).

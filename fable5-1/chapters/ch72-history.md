# Chapter 72 — How we got here: a history of measuring the shape of the Earth

> **Part XVI — Standards, software, and history.** This chapter is the book's long view: how the ideas, instruments, institutions, and mistakes of twenty-three centuries produced the elevation data, datums, and habits you inherit today — and why knowing that history is a validation skill.

**In this chapter.** You will be able to place any elevation dataset in its technological era and infer from that era what its producers could and could not have known: whether heights are tied to a tide gauge, a geoid model, or an ellipsoid; whether positions carry a 1920s triangulation adjustment or a 1990s GPS solution; whether "depth" came from a lead line, a single-beam echo sounder with an assumed sound speed, or a multibeam system with a measured profile. The narrative runs from Eratosthenes and Snellius through the French geodesic missions, national triangulations and levelling networks, lead lines and *Challenger*, echo sounding and multibeam, photogrammetry, radar, lasers, GPS, SRTM, satellite lidar, and structure from motion, to the cloud-native and machine-learning present. It closes with the recurring patterns — every new sensor over-trusted, every datum change a decade of mixed data, every archive under-funded — and a then-vs-now table quantifying how accuracy, density, coverage, latency, and cost moved between 1900 and 2025. Dates are anchored to [Appendix C](../appendices/appendix-c-timeline.md); items tagged ⟨H⟩ come from the gis-history repository.

## 72.1 Antiquity to the Enlightenment

The problem of elevation is the problem of the Earth's shape, first posed quantitatively in the third century BCE. **Eratosthenes** of Cyrene reasoned (c. 240 BCE) that if the noon Sun stood overhead at Syene while casting a shadow of about 1/50 of a circle (7.2°) at Alexandria, and the cities lay roughly 5,000 stadia apart on a meridian, the Earth's circumference was about 250,000 stadia. The result was within perhaps 2–15 % of the modern value depending on which stadion he used — a range historians still argue about, which is itself a lesson in recording units. The method — an angle measured astronomically, a distance measured on the ground, and a ratio — is the method of every meridian-arc measurement for the next two thousand years.

**Ptolemy** (c. 150 CE) codified latitude and longitude in the *Geographia* with a circumference about one-sixth too small, an error that propagated into Columbus's estimate of the distance to Asia. **al-Biruni** (c. 1025) measured the Earth's radius from the dip of the horizon seen from a hill of known height — geometry replacing a long baseline. The modern survey begins with **triangulation**: Willebrord **Snellius** measured a baseline near Leiden and chained triangles between Alkmaar and Bergen op Zoom in 1615 (*Eratosthenes Batavus*, 1617). His degree was about 3.5 % short, but the method — one measured baseline, many measured angles, scale carried by trigonometry — remained the backbone of geodesy until electronic distance measurement in the 1950s and GPS in the 1980s. Jean **Picard** repeated it with telescopic sights between Paris and Amiens (1669–1670) to roughly 0.1 %, good enough for Newton to use in the *Principia* (1687).

Newton predicted an **oblate** Earth; the **Cassini** dynasty, extending Picard's arc through France, concluded the degree shortened northward — a **prolate** Earth. The Académie des Sciences settled the dispute by sending **Maupertuis** to Lapland (1736–1737) and **Bouguer**, **La Condamine**, and Godin to the Viceroyalty of Peru (1735–1744). The Lapland degree was longer; the Earth was oblate; and the Peru expedition's observations of the attraction of Chimborazo began the story of the geoid and isostasy. Modern flattening ($1/f \approx 298.257$) descends from that lineage.

The Enlightenment closed by making the meridian the unit of length. In 1791 the Académie defined the **metre** as one ten-millionth of the quarter meridian through Paris; Delambre and Méchain measured Dunkirk to Barcelona (1792–1798), a provisional metre was legislated in 1795, and the platinum *mètre des Archives* was deposited in 1799. ⟨H⟩ Méchain's concealed latitude discrepancy at Barcelona, reconstructed by Alder (2002), left the metre about 0.2 mm short of its definition. The unit survived because it was embodied in an artefact and in use. Two lessons recur throughout this handbook: hidden errors poison everything built on them, and a practical standard, once realized, outlives the theory that justified it.

<!-- figure: Figure 72.1 — Timeline strip from 240 BCE to 1800: Eratosthenes, Ptolemy, al-Biruni, Snellius, Picard, the Lapland and Peru missions, and the metre, with the implied Earth circumference or flattening estimate for each -->

## 72.2 National surveys and the figure of the Earth

The nineteenth century turned triangulation into state infrastructure. The **Ordnance Survey** traces its origin to the Principal Triangulation of Great Britain, begun in 1791 under fear of French invasion and completed in 1853. ⟨H⟩ The **US Coast Survey** was funded by Congress in 1807 and organized by Ferdinand Hassler, becoming the Coast and Geodetic Survey and eventually part of NOAA. ⟨H⟩ The most ambitious was the **Great Trigonometrical Survey of India**, begun by William Lambton in 1802 and carried north by George **Everest** (superintendent 1823–1843) along roughly 2,400 km of meridian. Its computers announced Peak XV in 1856 as 29,002 ft (8,840 m), within 9 m of today's 8,848.86 m, from observations more than 170 km away through an atmosphere whose refraction was the dominant and only partly modelled error (Keay 2000; see the Mathematics worked example). The GTS also documented the Himalayan deflections of the vertical that forced the invention of isostasy.

Two mathematical contributions underpin everything in [Chapter 5](ch05-error-and-uncertainty.md). Carl Friedrich **Gauss** published **least squares** in 1809 (Legendre had printed it in 1805) and applied it to his triangulation of Hanover. ⟨H⟩ Least squares turned redundancy from an embarrassment into a strength: the adjustment distributes misclosures by weight and yields, for the first time, an estimate of the precision of the result. Gauss also invented the heliotrope and the conformal mapping that became the transverse Mercator projection ([Chapter 10](ch10-projections-and-resampling.md)).

Arc measurements accumulated and were fitted to ellipsoids: **Airy** (1830) ⟨H⟩, **Bessel** (1841), **Clarke** (1858, 1866, 1880) ⟨H⟩, and **Hayford** (1909–1910, adopted as the International Ellipsoid of 1924). Each is still embedded in archive data; a 1950s map on Clarke 1880 and a 1970s chart on International 1924 differ from WGS 84 by hundreds of metres horizontally ([Chapter 8](ch08-horizontal-datums.md)).

Heights came from a different instrument. **Spirit levelling** — carrying height differences from a tide gauge inland with a horizontal telescope and graduated staff — was systematized in the nineteenth century. By 1929 the United States and Canada had about 100,000 km of first-order levelling, adjusted jointly while holding 26 tide gauges fixed at local mean sea level: the **Sea Level Datum of 1929**, renamed **NGVD29** in 1973. ⟨H⟩ Holding 26 gauges at zero forced real sea-surface topography — up to about 0.5 m between Pacific and Atlantic mean sea levels — into the network as distortion, which NAVD88 would undo in 1991 (§72.6). Levelling is precise but its errors accumulate along lines, and **vertical land motion** since the adjustment epoch now dominates its uncertainty ([Chapter 38](ch38-plate-motion-and-vlm.md)).

The theory of what levelled heights *mean* was built by Friedrich Robert **Helmert** (*Die mathematischen und physikalischen Theorieen der höheren Geodäsie*, 1880–1884). Listing had coined "**geoid**" in 1873 for the equipotential surface coinciding with undisturbed mean sea level; Helmert showed how levelled differences depend on gravity along the path and introduced the orthometric reduction that bears his name. **Pratt** and **Airy** (both 1855) had proposed rival forms of **isostasy** to explain the Himalayan deflections. The geoid, isostasy, and the distinction between $h$, $H$, and $N$ in $h = H + N$ ([Chapter 7](ch07-shape-of-the-earth.md)) are nineteenth-century results that still generate twenty-first-century errors whenever a GNSS height is reported as "elevation."

> **Definitions that bite.** In 1900 *datum* meant an origin station with assigned latitude, longitude, azimuth, and ellipsoid (Meades Ranch for NAD27), and heights were "above mean sea level" at whatever gauge the network began from. Neither is defined by the physical quantities (geocentric coordinates, geopotential) that define today's datums. Archive data carry the old meaning; [Chapter 9](ch09-vertical-datums.md) gives the conversions and their uncertainties.

## 72.3 Depth

For most of history depth was a weighted line and the fathoms of wetted rope: a point measurement at a dead-reckoned position, biased deep by line drift in currents. Matthew Fontaine **Maury** compiled such soundings into the first **bathymetric chart of the North Atlantic** (1853), contouring at 1,000-fathom intervals from about 200 deep soundings. ⟨H⟩ It was commissioned by the telegraph-cable interest — bathymetry has always been paid for by whoever needs the seafloor next. The **HMS *Challenger* expedition** (1872–1876) took 492 deep soundings on a 127,000 km circumnavigation, including 8,184 m in what became the Challenger Deep. ⟨H⟩ Its depths were tied to nothing but the instantaneous sea surface and its positions were celestial, with tens of kilometres of uncertainty — which matters when a modern compiler finds a *Challenger* sounding disagreeing with multibeam.

Acoustic depth arrived in the decade of *Titanic*. Behm filed the first echo-sounder patent in 1913 ⟨H⟩; **Fessenden** detected an iceberg and the seabed acoustically in April 1914; the German *Meteor* expedition (1925–1927) made about 67,000 echo soundings across the South Atlantic and revealed the Mid-Atlantic Ridge as continuous. Echo sounding introduced the error that still dominates sonar budgets: $d = c\,t/2$ with an *assumed* sound speed, so a 1 % error in $c$ is a 1 % error in depth ([Chapter 20](ch20-sonar.md)).

Marie **Tharp** and Bruce **Heezen** turned 1950s precision-depth-recorder profiles into **physiographic diagrams** — the 1952 drafting that revealed the rift valley, the 1957 North Atlantic diagram, and with Berann the 1977 *World Ocean Floor Panorama*. ⟨H⟩ Tharp filled the gaps between tracks with geologically plausible morphology; the maps were right about plate tectonics while being, as elevation data, mostly extrapolation. That distinction between a *picture* of the seafloor and a *measurement* of it is why GEBCO's Type Identifier grid ([Chapter 48](ch48-compositing.md)) exists.

**Multibeam** transformed density. Patented in 1962 ⟨H⟩ for the US Navy, it reached commerce as **SeaBeam** (1977; 16 beams, 45° swath) ⟨H⟩; second-generation systems (Hydrosweep DS, 1989 ⟨H⟩) widened swaths to 90–120°, and by the 2000s shallow-water systems produced hundreds of soundings per ping. The problem shifted from too few soundings to too many for a hydrographer to inspect — the motivation for **CUBE** (Calder & Mayer 2003) and the uncertainty-bearing **BAG** format (2006).

From orbit a radar altimeter cannot see the seafloor, but it can measure the sea-surface slope that seafloor gravity imposes. **Seasat** (1978) proved the principle in 105 days; **GEOSAT** (1985) ⟨H⟩ and ERS-1 (1991) provided dense tracks; and **Smith and Sandwell** (1997) combined altimetric gravity with ship soundings into a global predicted-bathymetry grid at about 2′. ⟨H⟩ That grid and its successors are the background in every global compilation and the reason most of the ocean floor in GEBCO is "predicted" rather than "measured" ([Chapter 23](ch23-satellite-derived-bathymetry.md)). **GEBCO** itself was initiated by Prince Albert I of Monaco in 1903 ⟨H⟩; its grid era began in the 1990s. The Nippon Foundation–GEBCO **Seabed 2030** project (2017) aims for a depth-dependent grid of the whole ocean (100 m cells shallower than 1,500 m, up to 800 m in the deepest water) by 2030. ⟨H⟩ About 6 % met that standard at launch; the project reported 26.1 % at the GEBCO_2024 release and 27.3 % at GEBCO_2025 (figure announced June 2025; grid released August 2025). The gap is a theme of [Chapter 73](ch73-open-problems.md).

> **Case file.** On 8 January 2005 the submarine USS *San Francisco* struck an uncharted seamount near the Caroline Islands at full speed, killing one sailor. ⟨H⟩ The chart in use showed no hazard; the altimetry-derived feature appeared in other sources. Every sounding on the chart dated from the lead-line and single-beam eras, and the seamount lay between tracks. The incident is the standard illustration of why source density and date — not the chart's edition — define its fitness for use ([Chapter 56](ch56-case-files.md), [Chapter 62](ch62-navigation-and-charting.md)).

<!-- figure: Figure 72.2 — Depth-measurement density through time: lead line (Maury 1853, Challenger 1876), single-beam (Meteor 1927), multibeam (SeaBeam 1977; modern shallow-water MBES), altimetry prediction (Smith & Sandwell 1997), as log soundings per square kilometre -->

## 72.4 Air and light

Photogrammetry's geometry predates the camera: Johann Heinrich **Lambert** worked out how to recover geometry from perspective drawings in the 1760s–1770s. ⟨H⟩ Within a decade of Niépce's first permanent photograph (1826) ⟨H⟩, Aimé **Laussedat** was using photographs for topographic survey (from 1849), and Nadar photographed Paris from a balloon in 1858 ⟨H⟩. Extracting heights by hand was laborious until the stereoplotter: Pulfrich's stereocomparator (1901), von Orel's stereoautograph (1908–1909), and the Zeiss, Wild, and Kern optical-mechanical plotters that drew most of the world's topographic contours between the 1930s and the 1980s. ⟨H⟩ The First World War made aerial photography routine for reconnaissance; the Second made it routine for mapping, and analytical aerotriangulation (Schmid, Brown, 1950s) put bundle adjustment ([Chapter 22](ch22-photogrammetry-sfm.md)) on a least-squares footing. The 1947 **US National Map Accuracy Standards** — 90 % of tested elevations within half a contour interval — were written for this era, and that is the accuracy of the quadrangle contours later digitized into the first national DEMs.

Radar began as detection (Hülsmeyer, 1904 ⟨H⟩), acquired the **synthetic aperture** in 1951 ⟨H⟩, and yielded interferometric topography from Seasat data (Zebker & Goldstein 1986). Radar **altimetry** — the same pulse timing pointed down — gave sea-surface and ice heights from Seasat (1978), GEOSAT (1985) ⟨H⟩, and **TOPEX/Poseidon** (1992) ⟨H⟩, whose ≈ 2 cm precision made global sea-level rise directly measurable ([Chapter 21](ch21-radar-sar-insar.md)).

The **laser** was first built in 1960 ⟨H⟩ and the first lidar followed within a year ⟨H⟩. Airborne laser *profiling* matured in the 1970s (NASA's Airborne Oceanographic Lidar, 1977, also demonstrated bathymetric returns), but a profile is not a map: without decimetre knowledge of where the aircraft was, the range was wasted. Two navigation technologies changed that. The first **GPS** satellite launched on 22 February 1978 ⟨H⟩; **full operational capability** came on 17 July 1995; Selective Availability was switched off on 2 May 2000 ⟨H⟩, improving civilian autonomous accuracy from roughly 100 m to roughly 10 m overnight, and kinematic carrier-phase processing (mid-1980s) gave centimetre trajectories. The strapdown **inertial navigation system** (first INS 1942 ⟨H⟩; ring-laser and fibre-optic gyros in the 1980s) supplied attitude and bridged gaps. Commercial scanning airborne lidar with GPS/IMU georeferencing appeared in the early 1990s (Optech ALTM, 1993; TopScan in Europe), and by the late 1990s national programmes — the Netherlands' AHN-1 (1996–2003) first — were replacing photogrammetric DTMs with lidar DTMs at about 1 point per 16 m², then 1 per m², then, by the 2010s, 8–20 per m² ([Chapter 18](ch18-topographic-lidar.md)). ⟨H⟩

The **Shuttle Radar Topography Mission** flew for eleven days in February 2000 and produced, by single-pass C-band interferometry with a 60 m mast, the first consistent near-global DEM: 80 % of land between 60° N and 56° S, released at 3″ (1″ globally from 2014). ⟨H⟩ Its specification was 16 m absolute vertical accuracy at 90 %; validation found roughly 5–9 m RMSE depending on terrain and cover (Farr et al. 2007; Rodríguez et al. 2006). Its voids, phase-unwrapping errors, vegetation bias, and many "void-filled" derivatives are a case study in [Chapter 55](ch55-public-products.md). SRTM also established the expectation that a global DEM should be free.

Space-based lidar followed: **ICESat** (2003) ⟨H⟩ profiled ice sheets until 2009; **ICESat-2** (2018) ⟨H⟩ and **GEDI** (launched December 2018, operating from 2019) ⟨H⟩ supply the sparse, accurately georeferenced heights now used to validate global DEMs ([Chapter 52](ch52-ground-truth.md)). **TanDEM-X** (2010) produced the first global 12 m InSAR DEM (2016) and, through the Copernicus DEM, the current default global product.

Finally the camera returned. **Structure from motion** — Tomasi–Kanade factorization (1992) ⟨H⟩, SIFT (1999–2004), bundle adjustment for unordered images (*Photo Tourism*, 2006), and dense multi-view stereo — met the consumer **drone** (DJI founded 2006 ⟨H⟩) and by about 2012 (Westoby et al. 2012) let a field scientist with a few thousand dollars of equipment make a centimetre-resolution DSM of a hillslope. Its accuracy depends on control, camera calibration, and geometry in ways photogrammetrists had known for a century and SfM users rediscovered one dome-shaped systematic error at a time.

<!-- figure: Figure 72.3 — Vertical accuracy (1σ, log scale) versus year for the dominant topographic method: stereoplotter contours, contour-derived DEMs, SRTM, airborne lidar, TanDEM-X, ICESat-2 — annotated with the enabling navigation technology -->

## 72.5 Computation and data

The DEM is a computing artefact, and its history tracks computing. The foundations came first: Fourier (1822) and Shannon's *A Mathematical Theory of Communication* (1948) ⟨H⟩, whose sampling theorem says a surface sampled at spacing $\Delta$ cannot represent wavelengths shorter than $2\Delta$ ([Chapter 44](ch44-resolution-and-sampling.md)); and Rudolf **Kálmán**'s recursive filter, developed 1958–1959 and published in 1960 ⟨H⟩, the engine of every GNSS/INS trajectory ([Chapter 13](ch13-imu-ins.md)).

The term **digital terrain model** was coined by Miller and Laflamme at MIT in 1958 for highway design: a grid of photogrammetrically sampled elevations from which a computer computed cut and fill. ⟨H⟩ Howard Fisher's **SYMAP** (1963–1964) printed isoline maps on a line printer, and the **Harvard Laboratory for Computer Graphics and Spatial Analysis** (1965) ⟨H⟩ trained the generation that built commercial GIS (Chrisman 2006). Tomlinson's **Canada Geographic Information System** (1963) ⟨H⟩ is conventionally the first GIS; "pixel" was written down by Billingsley at JPL in 1965 ⟨H⟩, where VICAR (1966) ⟨H⟩ was being built for planetary images — planetary and terrestrial elevation computing share a cradle ([Chapter 67](ch67-planetary-dems.md)).

The US Defense Mapping Agency's **DTED** format and Level 1 (3″) product date from the 1970s, created largely for terrain-following and terrain-contour-matching guidance; its 16-bit integer metres and latitude-dependent column spacing persist in archives ([Chapter 47](ch47-file-formats.md)). ⟨H⟩ The USGS began distributing DEMs digitized from contour maps in the mid-1970s; these, with their terracing and interpolation artefacts, were the national DEM until the National Elevation Dataset (1999) and 3DEP (2012–2013). Data structures appeared in the same decade: the **quadtree** (Finkel & Bentley 1974) ⟨H⟩ and the **TIN** of Peucker, Fowler, Little, and Mark (1978) ⟨H⟩, which argued that the terrain's own critical points and lines, not a regular grid, are the right sampling ([Chapter 46](ch46-data-models.md)).

The 1980s produced the software lineages still in use — **ARC/INFO** (1982) ⟨H⟩ and **GRASS** (1984) ⟨H⟩; Snyder's GCTP (1980) ⟨H⟩ and Evenden's code (1983) ⟨H⟩ leading to **PROJ** (1994) ⟨H⟩; **GMT** and **NetCDF** (1988) ⟨H⟩; **MB-System** (1993) ⟨H⟩; **ERDAS** (1979) ⟨H⟩. **GDAL**'s first release in 2000 ⟨H⟩ made it, with PROJ and GEOS (2002) ⟨H⟩, the substrate under nearly every raster tool in [Chapter 71](ch71-software-landscape.md); **PDAL** (2011) ⟨H⟩ did the same for point clouds. Formats encoded the data models: **GeoTIFF** (1995) ⟨H⟩; **LAS** (2003) ⟨H⟩ and LAZ (2011) ⟨H⟩; **BAG** (2006), the first widely used format with a mandatory uncertainty layer, fed by **CUBE** (2003). The **cloud-native** turn — COG (2016), **STAC** (2017; 1.0 in 2021) ⟨H⟩, Zarr (2015–2019) ⟨H⟩, **COPC** (2021) ⟨H⟩ — moved the unit of access from the file to the byte range, and **Earth Engine** (started 2009, public 2010) ⟨H⟩ moved computation to the data. The **machine-learning era** is usually dated from AlexNet (2012); for elevation, PointNet (2017), CoastalDEM (2018), FABDEM (2022), and foundation models from about 2023 mark the stages ([Chapter 43](ch43-traditional-vs-ml.md)).

> **Rule of thumb.** A DEM's *data structure* predicts its error structure. Contour-derived grids (pre-1995) show terracing at contour elevations and flat-topped hills; early lidar DTMs (1996–2005) show classification artefacts at forest edges; InSAR DEMs show void fills and unwrapping steps; SfM DSMs show doming. Check for the artefact the era predicts before trusting the accuracy statement.

## 72.6 Datums and frames

In North America: **NAD27** (1927) ⟨H⟩ — Clarke 1866, origin at Meades Ranch, a single adjustment of the continental triangulation — then **NAD83 (1986)**, geocentric by intent on GRS80 (1980) ⟨H⟩ with Doppler and VLBI ties, then successive GNSS realizations (HARN, CORS96, NAD83(2011)), each shifting coordinates by decimetres. NAD27-to-NAD83 shifts reach about 100 m in the west, which is why NADCON exists. Internationally, **ITRF88** through ITRF2020 are geocentric to the centimetre and time-dependent since ITRF91; **WGS 84** began in 1984 ⟨H⟩ as a Doppler frame about 1–2 m from ITRF and has been re-realized (G730 in 1994 through G2296 in 2024) to agree with ITRF at the centimetre level. "WGS 84" on a data sheet therefore spans two metres of meaning depending on the year ([Chapter 8](ch08-horizontal-datums.md)).

Vertically, NGVD29 gave way to **NAVD88** (1991), a minimum-constraint adjustment of 625,000 km of levelling held to a single gauge at Father Point/Rimouski. That removed the sea-surface-topography distortion but left NAVD88 tilted about 1 m across the conterminous United States relative to the best geoid, and vertical land motion since the 1980s levelling has made it worse; the hybrid geoid models GEOID90–GEOID18 are warped to fit it. The **NSRS modernization** replaces NAD83 and NAVD88 with four plate-fixed frames (NATRF2022 and its Pacific, Caribbean, and Mariana counterparts) and a geopotential datum, **NAPGD2022**, whose heights come from a gravimetric geoid rather than levelling; coordinates will be time-dependent, and as this was written NGS had announced a beta release for 2026, with formal adoption still pending. NAVD88-to-NAPGD2022 offsets are expected to be decimetres to about a metre, varying smoothly ([Chapter 9](ch09-vertical-datums.md), [Chapter 73](ch73-open-problems.md)).

Other regions ran the same course: Europe from ED50 to **ETRS89** (plate-fixed at epoch 1989.0); Australia from AGD66/84 through GDA94 to **GDA2020**, a jump of about 1.8 m from 26 years of plate motion; New Zealand's NZGD2000 with an embedded deformation model. The direction everywhere is from static regional datums to global, time-dependent frames and geopotential heights ([Chapter 38](ch38-plate-motion-and-vlm.md)).


| Transition | Years of overlap in practice (approx.) | Typical horizontal shift | Typical vertical shift |
|---|---|---|---|
| NAD27 → NAD83 (1986) | 1986 – c. 2000 | 10–100 m | n/a |
| NGVD29 → NAVD88 | 1991 – c. 2005 | n/a | −0.4 to +1.5 m (CONUS, regional) |
| ED50 → ETRS89 | 1990s – 2010s | 100–250 m | n/a |
| GDA94 → GDA2020 | 2017 – present | ≈ 1.8 m | ≈ 0.1 m |
| NAD83/NAVD88 → NATRF2022/NAPGD2022 | 2020s – 2030s | 1–2 m | dm to ≈ 1 m |

Shifts are order-of-magnitude ranges; use the official tools (NADCON/VERTCON, NCAT, GDA2020 grids, VDatum) for actual values.

> **Case file.** After Hurricane Katrina (2005) it became clear that many published NAVD88 bench-mark heights along the northern Gulf Coast were no longer true: NGS's analysis of repeated levelling and GPS (Shinkle & Dokka 2004, NOAA Technical Report NOS/NGS 50) had found subsidence of several millimetres per year across the lower Mississippi valley, so heights adjusted in 1991 from 1980s levelling were by the mid-2000s in error by decimetres in places. Flood-insurance maps, levee crest elevations, and lidar DEMs controlled to those marks inherited the error. A static vertical datum is an epoch-stamped snapshot; a DEM "on NAVD88" is only as current as the marks that controlled it ([Chapter 38](ch38-plate-motion-and-vlm.md), [Chapter 41](ch41-change-detection.md)).

## 72.7 Standards and institutions

The institutions that set the rules were founded in three waves, each answering a need to make measurements from different hands comparable. The first was international and scientific: the Mitteleuropäische Gradmessung (1862) that became the International Association of Geodesy, housed in the **IUGG** from 1919; **FIG** (1878); the International Society for Photogrammetry, now **ISPRS** (1910); and the **International Hydrographic Bureau** in Monaco (1921), renamed IHO in 1970. ⟨H⟩ Its first business was standardizing chart symbols and sounding units — fathoms versus metres still bites in archives. The first edition of **S-44** appeared in 1968 ⟨H⟩; its sixth (2020; 6.1.0 in 2022) is the reference for TVU/THU in [Chapter 70](ch70-specifications-guided-tour.md). The **ASPRS** was founded in 1934 ⟨H⟩, and its accuracy standards (1990; 2014; Edition 2, 2023) replaced NMAS for digital data; NOAA formed in 1970 ⟨H⟩.

The second wave concerned data rather than measurements. The US **FGDC** (1990) ⟨H⟩ issued the Content Standard for Digital Geospatial Metadata in 1994 ⟨H⟩ and the NSSDA in 1998, the first standard to require a tested RMSE and the 1.96 multiplier rather than a map-scale class. The **OGC** (1994) ⟨H⟩ and **ISO/TC 211** (1994) produced the interoperability and metadata standards (ISO 19115 in 2003 ⟨H⟩; ISO 19157 for quality) that **INSPIRE** (2007) ⟨H⟩ made mandatory in Europe; **OSGeo** (2006) ⟨H⟩ gave GDAL, GRASS, QGIS, PDAL, and PROJ an institutional home.

The third wave is the **open-data turn**: SRTM free in 2000; the Landsat archive opened in 2008; Copernicus (Sentinel-1 from 2014 ⟨H⟩, Sentinel-2 from 2015 ⟨H⟩) fully open; the USGS **3DEP** (2012–2013) committing to public-domain lidar for the whole United States. Open data changed validation — once anyone could download a product, anyone could test it, and the independent accuracy literature of [Chapter 55](ch55-public-products.md) exists because of it — and it defined what is *missing*: the lidar deserts of [Chapter 73](ch73-open-problems.md) are the countries that lacked budget or policy.

## 72.8 Recurring patterns

**Every new sensor was first over-trusted.** Echo-sounding depths were used for decades with an assumed sound speed; early airborne lidar was marketed at 15 cm before anyone had measured its performance under canopy; SRTM's 16 m specification was read as a typical error rather than a 90 % bound; SfM DSMs were published without control until the doming literature caught up. The first users of a sensor are its champions, the test sites are chosen where it works, and the previous generation's reference data are too poor to reveal its errors. The remedy is [Chapter 53](ch53-accuracy-assessment.md): independent, stratified checkpoints before the specification becomes folklore.

**Every datum change created a decade of mixed data.** Producers switched at different dates, metadata led or lagged the transformation, and compilations silently mixed both. NSRS modernization will repeat this. The remedy is machine-readable datum and epoch metadata and routine consistency tests ([Chapter 49](ch49-metadata.md), [Chapter 54](ch54-evaluating-others-data.md)).

**The archive was always under-funded.** *Challenger*'s sounding sheets survive; many 1960s–1980s analogue echograms and 1990s multibeam raw files do not, and much 1990s lidar exists only as grids because the point clouds were not kept. The budget line that pays for acquisition rarely pays for the archive ([Chapter 50](ch50-archiving-and-provenance.md)).

**The error budget was understood by few and documented by fewer.** Most datasets produced between 1950 and 2010 state a single accuracy number, if any, without saying how it was obtained; CUBE/BAG, S-102, and per-pixel uncertainty layers are the first products designed so the budget travels with the data.

**Standards followed disasters.** SOLAS (1914) followed *Titanic* ⟨H⟩; the *San Francisco* grounding ⟨H⟩ accelerated source-diagram and CATZOC adoption; Katrina drove Gulf Coast re-levelling and the move to a gravimetric geoid datum. Read [Chapter 56](ch56-case-files.md) as the demand side of [Chapter 70](ch70-specifications-guided-tour.md).

## 72.9 Then-vs-now

Typical best-practice capability at each date, order-of-magnitude; exceptional projects were better and much production work was worse.


| Capability | 1900 | 1950 | 1980 | 2000 | 2025 |
|---|---|---|---|---|---|
| Horizontal control | Triangulation; ≈ 1:50,000–1:100,000 proportional | Triangulation + invar baselines; ≈ 1:200,000 | EDM traverse; Doppler ≈ 1 m | GPS RTK cm relative; ≈ 10 m autonomous | GNSS RTK/PPP 1–3 cm, ITRF-tied |
| Height control | Levelling to local MSL | First-order levelling (NGVD29) | Levelling + early gravimetric geoids (dm) | GPS + GEOID99 (≈ 5 cm) | GNSS + gravimetric geoid (1–3 cm); geopotential datums |
| Topography (vertical, 1σ) | Plane-table contours; several m | Stereoplotter contours; NMAS ≈ ½ CI (1.5–3 m at 1:24k) | Contour-derived DEMs; 3–7 m RMSE | Airborne lidar 15–30 cm; SRTM 5–9 m | Lidar 5–10 cm NVA; global DEMs 2–4 m |
| Depth | Lead line; percent-level bias; hours per sounding | Single-beam; ≈ 1 % of depth | SeaBeam-class MBES (16 beams); ≈ 0.5 % | MBES 100+ beams; S-44 Order 1 | MBES 400+ beams, CUBE; Exclusive Order |
| Point density (land) | Spot heights ≈ 1/km² | Contours; effectively 1 per 10²–10³ m² | DEM posts 30–90 m | Lidar 0.1–1 pt/m² | Lidar 8–50 pt/m²; SfM 100+ pt/m² |
| Coverage | National; ocean floor < 0.1 % sounded | Continental; oceans along tracks | DTED-1 for parts of globe | SRTM 80 % of land; ocean ≈ 6 % at Seabed 2030 resolution | Copernicus 30 m global; lidar for much of N. America/Europe; ocean 26.1 % (GEBCO_2024) |
| Latency | Years to decades | Years | Months to years | Weeks to months | Days to weeks; satellites hours |
| Cost per km² (DEM) | Person-years | Person-months | Thousands USD (photogrammetry) | Hundreds USD (lidar, large area) | Tens USD (lidar QL2 at scale); ≈ 0 for global products |
| Uncertainty reporting | None | Map-scale class (NMAS) | Single RMSE in a report | NSSDA tested RMSE; CUBE/BAG begin | Per-pixel uncertainty; TVU/THU; NVA/VVA by land cover |

<!-- figure: Figure 72.4 — Log–log plot of vertical accuracy against areal coverage for each era in the table, showing the frontier moving down and right -->

## Then & now

A hydrographer in 1925 and one in 2025 would recognize each other's problems: sound speed, position, tide, and whether gaps between lines hide a hazard. The 1925 hydrographer measured one depth every few hundred metres with an assumed sound speed; the 2025 hydrographer measures hundreds per ping with a cast an hour old and a CUBE surface reporting uncertainty at every node — and must decide whether to trust it at a 65° swath edge. A topographer in 1950 judged where the ground lay under trees in a stereo model; in 2025 a classifier does so across billions of points and the operator audits the classifier.

What changed most is not accuracy but *density, coverage, and latency* — each by three or more orders of magnitude — and, latest of all, the expectation that uncertainty travels with the data. What changed least is the error budget's structure: position, orientation, range, refraction, datum, and the definition of the surface. The positioning thread — theodolite (1576) ⟨H⟩, Gunter's chain (1620) ⟨H⟩, H4 chronometer (1761) ⟨H⟩, Tellurometer (1957) ⟨H⟩, GPS (1978) ⟨H⟩ — is followed in [Chapter 11](ch11-history-of-positioning.md); the computing thread from ENIAC (1945) ⟨H⟩ to TensorFlow (2015) ⟨H⟩ is why a laptop now adjusts a lidar block that was a national project in 1980.

## Mathematics

**Eratosthenes.** With parallel sunlight and both sites on a meridian, the shadow angle $\theta$ equals the latitude difference, so $C = s \cdot 360^\circ/\theta$. For $\theta = 7.2^\circ$, $s = 5{,}000$ stadia: $C = 250{,}000$ stadia — 39,375 km if the stadion was 157.5 m (−1.6 % against 40,008 km), 46,250 km if 185 m (+15.6 %). The uncertainty is dominated by the unit of the baseline, not the angle, exactly as the scale of a modern network is its weakest observation.

**Least squares (Legendre 1805, Gauss 1809).** For $\mathbf{l} + \mathbf{v} = A\mathbf{x}$ with weights $P = \Sigma_l^{-1}$, minimizing $\mathbf{v}^{\mathsf T} P \mathbf{v}$ gives

$$ \hat{\mathbf{x}} = (A^{\mathsf T} P A)^{-1} A^{\mathsf T} P \mathbf{l}, \qquad \Sigma_{\hat x} = \hat\sigma_0^{2}(A^{\mathsf T} P A)^{-1}, \qquad \hat\sigma_0^{2} = \frac{\mathbf{v}^{\mathsf T} P \mathbf{v}}{n-u}. $$

Gauss's contribution beyond Legendre was the probabilistic justification and the a posteriori variance factor — the first routine estimate of the uncertainty of a result from the observations themselves ([Appendix B](../appendices/appendix-b-math-reference.md) §B.6).

**Flattening from two arcs.** To first order the meridional degree length is $L(\varphi) \approx \bar L\,(1 - 2f + 3f\sin^2\varphi)$, so two measured degrees give $f \approx (L_2 - L_1)/[3\bar L(\sin^2\varphi_2 - \sin^2\varphi_1)]$. Lapland (66.3° N, ≈ 111.5 km) against Peru (1.5° S, ≈ 110.57 km) yields $f \approx 1/300$; a 100 m error in a degree moves $1/f$ by about 25, which is why eighteenth-century results ranged from 1/178 to 1/330 (GRS80: 1/298.257).

**The geoid as an equipotential.** Level surfaces satisfy $W = V + \Phi = \text{const}$; the geoid is $W = W_0$ (conventional $W_0 = 62\,636\,853.4\ \mathrm{m^2 s^{-2}}$). The geopotential number $C = W_0 - W_P = \int g\,\mathrm{d}n$ is path-independent; the raw levelled sum $\sum \mathrm{d}n$ is not. $H = C/\bar g$ with $\bar g$ the mean gravity along the plumb line (Helmert: $\bar g \approx g + 0.0424\,H$ mGal, $H$ in m); $N = h - H$ ([Chapter 7](ch07-shape-of-the-earth.md)).

**Kalman (1960).** With $\mathbf{x}_k = F\mathbf{x}_{k-1} + \mathbf{w}$, $\mathbf{z}_k = H\mathbf{x}_k + \mathbf{v}$, $\mathbf{w}\sim\mathcal N(0,Q)$, $\mathbf{v}\sim\mathcal N(0,R)$: predict $\mathbf{x}^- = F\mathbf{x}$, $P^- = FPF^{\mathsf T} + Q$; update $K = P^-H^{\mathsf T}(HP^-H^{\mathsf T}+R)^{-1}$, $\mathbf{x} = \mathbf{x}^- + K(\mathbf{z} - H\mathbf{x}^-)$, $P = (I-KH)P^-$. It is sequential least squares with a dynamic model, arriving as Apollo navigation needed it.

> **Worked example.** How good was Everest's 1856 height? Peak XV was observed from six stations 174–190 km away at vertical angles of 1°–2°. Refraction lifts the apparent target by roughly $k s^2/(2R)$: at $s = 180$ km, $k = 0.13$ gives $0.13 \times (1.8\times10^5)^2/(2 \times 6.371\times10^6) \approx 330$ m; $k = 0.07$ gives ≈ 180 m. The whole gap between 8,840 m and 8,848.86 m is a few percent of the refraction correction, so the real 1856 uncertainty was of order ±50 m, dominated by $k$ — not by the angles (good to a few arc seconds, ≈ 2–3 m at that range) nor the baseline. Coming within 9 m was partly luck, which is the distinction to keep when judging whether an old measurement "was accurate."

## Validation & uncertainty

History is a validation tool because it bounds what a dataset *could* know. For legacy data without an error budget — the normal case before about 2005 — the era lets you reconstruct the budget's structure and tells you which tests to run.

**Reconstruct the budget from four questions.** (1) *How was position obtained?* Triangulation and plane table (pre-1950): metres to tens of metres, correlated over tens of kilometres, on a regional datum. Aerotriangulation to ground control (1950–1995): a fraction of a metre to a few metres, block-wise systematic. GPS (post-1995): sub-metre, on whatever datum realization the base used. (2) *How was height obtained, and to what?* Levelling to a tide gauge; stereo model to levelled control; GNSS to a geoid model — which one? (3) *What was the measurement primitive?* Contours are accurate at the line and interpolated between; single-beam depths are biased in proportion to depth by sound speed; lidar is biased under vegetation. (4) *What surface was intended?* Pre-lidar topography is an operator's judgement of the ground; early lidar DTMs often retain low vegetation; stereo-matched DSMs bleed buildings onto the ground.

> **Uncertainty budget.** Reconstructed vertical budget for a USGS 7.5′ DEM (c. 1985–1995) derived from 1950s–1970s photogrammetric contours at a 20 ft interval. Typical ranges, not a specification.
>
> | Component | Mechanism | Typical magnitude (1σ) |
> |---|---|---|
> | Source contours | NMAS: 90 % within ½ CI → σ ≈ 0.3 CI | ≈ 1.8 m |
> | Ground judgement under forest | Floating mark on canopy or shadow | +0.5 to +3 m bias |
> | Contour-to-grid interpolation | Terracing; flat ridges and valleys | 0.5–2 m, worst on low slopes |
> | Datum (NGVD29 → NAVD88) | Not applied, or VERTCON | 0.0–1.5 m, regionally smooth |
> | Horizontal error × slope | σ_xy ≈ 6–12 m at 1:24k | ≈ 1 m per 10 % slope per 10 m |
> | Vertical land motion since source | 40–60 yr of subsidence/uplift | 0–0.5 m; locally several m |
> | **Combined, open flat terrain** | root-sum-square | ≈ 2–3 m |
> | **Combined, forested 30 % slope** | includes biases | ≈ 4–7 m, biased high |
>
> The USGS specified its contour-derived 7.5′ Level 1 DEMs at a vertical RMSE of 7 m (15 m maximum) and Level 2 at half the source contour interval; published tests typically found a few metres RMSE, consistent with this reconstruction.

**Run the tests the era predicts.** For contour-derived grids, histogram elevations modulo the contour interval: a peak diagnoses terracing. For single-beam bathymetry, plot crossing-line discrepancies against depth: proportional means sound speed, constant means draft or tide. For 1990s lidar, difference against a modern DTM by land cover: positive bias confined to forest is residual vegetation. For any pre-2000 dataset, compare with GNSS heights at stable bench marks: a smooth regional residual is a datum or geoid-model difference, not random error.

**Report the era forward.** When compositing legacy data ([Chapter 48](ch48-compositing.md)), carry acquisition dates, positioning method, the original vertical reference, the transformation applied and its uncertainty, and the artefacts tested for; GEBCO's per-cell TID is the minimal form.

> **Try it.** Detect contour terracing in a legacy DEM.
>
> ```python
> import numpy as np, rasterio
> with rasterio.open("legacy_dem.tif") as src:
>     z = src.read(1, masked=True).compressed().astype(float)
> ci = 20 * 0.3048                      # 20 ft contour interval, metres
> r = np.mod(z, ci) / ci                # fractional position between contours
> hist, _ = np.histogram(r, bins=20, range=(0, 1))
> print(f"peak/mean bin ratio = {hist.max() / hist.mean():.2f}")
> # ~1.0–1.3 for lidar-derived DEMs; > 2 indicates the grid remembers its contours
> ```

## Software

**Open source:** GRASS GIS (1984 ⟨H⟩; `r.surf.contour` reproduces 1980s contour-to-grid production and its artefacts); GMT (1988 ⟨H⟩; `surface` and `grdtrack` were and are the tools of the Smith & Sandwell lineage); MB-System (1993 ⟨H⟩; reads legacy multibeam formats back to SeaBeam classic, making 1980s swath data recoverable); GDAL (2000 ⟨H⟩; reads DTED, USGS DEM, SDTS); PROJ (1994 ⟨H⟩; carries NADCON, NTv2, VERTCON, and HTDP-derived grids — check the grid files are installed, as default builds omit many). Caveat: reading an old format is not recovering its semantics (pixel-is-point versus area, integer units, implied datum).

**Free but closed:** NGS NCAT, VDatum, and HTDP for US transformations across datums and epochs; scanned primary sources such as the 1928 ⟨H⟩ and 1976 ⟨H⟩ *Hydrographic Manuals* for reconstructing procedures.

**Commercial:** ArcGIS Pro still reads the ARC/INFO coverage format; ERDAS IMAGINE (1979 ⟨H⟩ lineage) reads legacy `.img` and block files; CARIS HIPS (1979 ⟨H⟩) reads hydrographic projects back to the 1990s. SYMAP's algorithms are documented in Chrisman (2006); GRASS 4.x–5.x source is archived by OSGeo.

## Standards & guides

- **US Bureau of the Budget, National Map Accuracy Standards (1947).** Horizontal: 90 % of well-defined points within 1/30 in (≥ 1:20,000) or 1/50 in; vertical: 90 % within ½ contour interval. Governs every pre-digital US map and hence contour-derived DEMs; read against ASPRS (2023) to see the move from map-scale classes to tested RMSE.
- **IHO S-44, 1st edition (1968).** ⟨H⟩ International accuracy classes for soundings; compare Ed. 6.1.0 (2022), which replaced fixed tolerances with depth-dependent TVU and added feature detection and coverage requirements.
- **FGDC-STD-001 CSDGM (1994; rev. 1998).** ⟨H⟩ First mandatory US metadata standard; its data-quality section is the ancestor of ISO 19157.
- **FGDC-STD-007.3 NSSDA (1998).** Replaced NMAS with tested RMSE × 1.96 (vertical) / × 1.7308 (horizontal) at 95 %; ≥ 20 checkpoints.
- **USGS Standards for Digital Elevation Models (1980s–1998).** Level 1–3 classes and the 7 m / 15 m RMSE acceptance thresholds for legacy USGS DEMs.
- **NOAA/NOS *Hydrographic Manual*, Hawley (1928) ⟨H⟩ and 4th ed. (1976) ⟨H⟩.** Lead-line and echo-sounding procedures; the source for how a legacy survey handled sound speed, tide, and position.

## Pitfalls

- **Whiggish history** — assuming the current generation "finally got it right" → its errors are not yet documented → expect today's defaults (Copernicus DEM as reference, EGM2008 as "the" geoid) to look naive in 2050; write limitations sections accordingly.
- **Forgetting archive data carry their era's assumptions** → files are re-formatted without re-deriving budgets → reconstruct the budget from the era and test for the predicted artefacts before compositing.
- **Reading old accuracy statements in modern terms** → NMAS "90 % within ½ CI" is not RMSE; S-44 1st-edition classes are not TVU → convert explicitly (σ ≈ 0.3 CI) and label the conversion an estimate.
- **Assuming a stated datum was applied** → during transitions metadata led or lagged the data → test against modern heights at stable marks; a smooth residual is a datum problem.
- **Treating "WGS 84" or "NAD83" as one thing** → realizations differ by up to ≈ 2 m and decimetres respectively → record realization and epoch ([Chapter 8](ch08-horizontal-datums.md)).
- **Mistaking interpretive maps for measurement** → physiographic fill, hand contours, predicted bathymetry all look like data once gridded → check TID, source diagrams, lineage; treat unmeasured cells as such.
- **Over-trusting the newest sensor** → champions test where it works → demand independent, stratified checkpoints before adopting a specification as typical.
- **Assuming a datum change is complete when announced** → adoption takes a decade → plan for mixed inputs and build the datum test into intake.
- **Discarding raw data because the grid "is the deliverable"** → the archive is unfunded → keep raw observations with calibration; unkept 1990s point clouds cannot be re-classified.
- **Calling a famous number accurate because it was close** → Everest's 1856 height was within 9 m with ±50 m uncertainty → judge by uncertainty, not luck.

## Key takeaways

- Most present-day confusions — datum realizations, surface definitions, units, over-trust of new sensors — have identifiable historical roots that tell you which test to run.
- A dataset's era bounds what it could know: positioning method, height reference, measurement primitive, and intended surface follow from date and producer, and a plausible error budget follows from them.
- Accuracy improved one to two orders of magnitude between 1900 and 2025; density, coverage, and latency improved three or more; uncertainty reporting went from absent to per-pixel only in the last two decades.
- Every datum transition produced a decade of mixed data; NSRS modernization will too. Test datum and epoch at intake rather than trusting metadata.
- Interpretive products are indistinguishable from measurement after gridding; source-type layers are the only defence.
- Least squares (1809), the geoid as equipotential (1873–1884), and the Kalman filter (1960) are the field's mathematical spine and the parts least likely to be replaced.
- Raw data outlive products and theories; archive them with calibration so the next generation can reprocess rather than remeasure.
- Standards followed disasters; read case files as the demand side of specifications and anticipate the next one.

## References

- Alder, K. (2002). *The Measure of All Things: The Seven-Year Odyssey and Hidden Error That Transformed the World*. Free Press.
- Calder, B. R., & Mayer, L. A. (2003). Automatic processing of high-rate, high-density multibeam echosounder data. *Geochemistry, Geophysics, Geosystems*, 4(6):1048.
- Chrisman, N. (2006). *Charting the Unknown: How Computer Mapping at Harvard Became GIS*. ESRI Press.
- Deacon, M. (1971). *Scientists and the Sea, 1650–1900*. Academic Press.
- Dierssen, H. M., & Theberge, A. E. (2014). Bathymetry: History of seafloor mapping. In *Encyclopedia of Natural Resources: Water*. Boca Raton: Taylor & Francis/CRC Press.
- Farr, T. G., et al. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics*, 45(2):RG2004.
- Finkel, R. A., & Bentley, J. L. (1974). Quad trees: A data structure for retrieval on composite keys. *Acta Informatica*, 4(1):1–9.
- Foresman, T. W. (ed.) (1998). *The History of Geographic Information Systems: Perspectives from the Pioneers*. Prentice Hall.
- Gauss, C. F. (1809). *Theoria Motus Corporum Coelestium*. Perthes & Besser, Hamburg.
- Helmert, F. R. (1880, 1884). *Die mathematischen und physikalischen Theorieen der höheren Geodäsie*, 2 vols. Teubner.
- Kalman, R. E. (1960). A new approach to linear filtering and prediction problems. *Journal of Basic Engineering*, 82(1):35–45.
- Keay, J. (2000). *The Great Arc: The Dramatic Tale of How India Was Mapped and Everest Was Named*. HarperCollins.
- Mayer, L., et al. (2018). The Nippon Foundation—GEBCO Seabed 2030 Project. *Geosciences*, 8(2):63.
- Miller, C. L., & Laflamme, R. A. (1958). The digital terrain model — theory and application. *Photogrammetric Engineering*, 24(3):433–442.
- Parkinson, B. W., & Spilker, J. J. (eds.) (1996). *Global Positioning System: Theory and Applications*. AIAA.
- Peucker, T. K., Fowler, R. J., Little, J. J., & Mark, D. M. (1978). The triangulated irregular network. *Proc. Digital Terrain Models Symposium*, St. Louis, pp. 516–532.
- Rodríguez, E., Morris, C. S., & Belz, J. E. (2006). A global assessment of the SRTM performance. *Photogrammetric Engineering & Remote Sensing*, 72(3):249–260.
- Schwehr, K. (ongoing). *gis-history*. https://github.com/schwehr/gis-history (CC0).
- Shannon, C. E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27:379–423, 623–656.
- Shinkle, K. D., & Dokka, R. K. (2004). *Rates of Vertical Displacement at Benchmarks in the Lower Mississippi Valley and the Northern Gulf Coast*. NOAA Technical Report NOS/NGS 50.
- Smith, J. R. (1997). *Introduction to Geodesy: The History and Concepts of Modern Geodesy*. Wiley.
- Smith, W. H. F., & Sandwell, D. T. (1997). Global sea floor topography from satellite altimetry and ship depth soundings. *Science*, 277(5334):1956–1962.
- Theberge, A. E. (1989). *The Coast Survey 1807–1867* (History of the Commissioned Corps of NOAA, vol. 1). NOAA Central Library / NOAA History.
- Torge, W., & Müller, J. (2012). *Geodesy*, 4th ed. De Gruyter.
- Westoby, M. J., et al. (2012). 'Structure-from-Motion' photogrammetry: A low-cost, effective tool for geoscience applications. *Geomorphology*, 179:300–314.
- Zebker, H. A., & Goldstein, R. M. (1986). Topographic mapping from interferometric synthetic aperture radar observations. *Journal of Geophysical Research*, 91(B5):4993–4999.

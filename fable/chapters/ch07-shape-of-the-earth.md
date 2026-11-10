# Chapter 7 — The shape of the Earth: ellipsoid, geoid, gravity, heights

> **Part III — Where is "here"? Geodesy, datums, projections.** This chapter supplies the physical and geometric geodesy that every later chapter on datums, sensors, and validation silently assumes.

**In this chapter.** Every elevation is a distance from *something*, and the something is either a mathematical ellipsoid or a gravity-defined surface. After this chapter you will be able to state which one a given height refers to, convert between them with the right geoid model, and estimate how much that conversion can be wrong and in what spatial pattern. You will read ellipsoid parameters ($a$, $f$, $e^2$), compute normal gravity, explain why $h = H + N$ is an approximation, distinguish orthometric, normal, and dynamic heights, and understand what GRACE, GOCE, and GRAV-D actually measured. You will also see why mean sea level is not the geoid (by up to a metre or two), why the ground breathes by decimetres daily under tidal forcing, and how geoid models are validated by levelling lines hundreds of kilometres long. The chapter ends with a concrete uncertainty budget for GNSS-derived orthometric heights.

## 7.1 Sphere → ellipsoid

Eratosthenes (about 240 BCE) made the first checkable estimate of the Earth's circumference from a shadow angle at Alexandria, a vertical sun at Syene, and the distance between them; depending on the stadion assumed, he was within a few percent to about 15 % of the modern value. For eighteen centuries the sphere was good enough, because nobody could measure its departure from sphericity.

Newton (1687) argued from rotation that the Earth must be an **oblate** spheroid; the Cassinis' French arcs suggested the opposite. The French Academy settled it with two **arc measurements** — Maupertuis in Lapland (1736–1737) and Bouguer, La Condamine, and Godin in Peru (1735–1744) — each measuring the astronomical latitude at both ends of a triangulated line to get the local radius of curvature in the meridian. A degree is longer near the pole on an oblate body, and that is what they found; combining arcs at different latitudes gave the flattening.

Through the nineteenth century, national surveys produced a family of **reference ellipsoids**, each fitted to the arcs available to its author. The ones you will still meet in metadata are:

| Ellipsoid | Year | $a$ (m) | $1/f$ | Where it survives |
|---|---|---|---|---|
| Airy ⟨H⟩ | 1830 | 6 377 563.396 | 299.324 964 6 | Great Britain (OSGB36) |
| Bessel | 1841 | 6 377 397.155 | 299.152 812 8 | Germany, Japan (Tokyo datum), Indonesia, Switzerland |
| Clarke ⟨H⟩ | 1866 | 6 378 206.4 | 294.978 698 2 | NAD27, North America |
| Clarke | 1880 | 6 378 249.145 | 293.465 | Africa, France (modified), Middle East |
| Hayford / International | 1909 / 1924 | 6 378 388 | 297 | ED50, many mid-century datums |
| GRS80 ⟨H⟩ | 1980 | 6 378 137 | 298.257 222 101 | NAD83, ETRS89, GDA, ITRF |
| WGS84 ⟨H⟩ | 1984 | 6 378 137 | 298.257 223 563 | GPS broadcast frame |

Two things matter about this table for DEM work. First, the ellipsoids differ by hundreds of metres in semi-major axis, and a classical datum also *positions* its ellipsoid relative to the Earth's centre of mass by hundreds of metres ([Chapter 8](ch08-horizontal-datums.md)). Second, GRS80 and WGS84 share the same $a$ and differ in flattening only in the ninth significant figure; their semi-minor axes differ by about 0.1 mm. For any elevation purpose the two ellipsoids are identical; what differs between NAD83 and WGS84 is the datum (origin and orientation), not the ellipsoid.

GRS80 is a **geodetic reference system**, not just a shape: it is defined by four constants — $a$, the geocentric gravitational constant $GM$, the dynamic form factor $J_2$, and the angular velocity $\omega$ — from which the flattening and a **normal gravity** field (§7.2) are derived. It is the equipotential ellipsoid: its surface is a level surface of its own normal gravity field. That is what makes it the natural reference for both geometric and physical heights.

<!-- figure: Figure 7.1 — Meridian ellipse with semi-axes a and b, geodetic latitude φ versus geocentric latitude ψ, the normal through a surface point, and the radius of curvature in the prime vertical N(φ). -->

### 7.1.1 Ellipsoid geometry in two paragraphs

A meridian section is an ellipse with semi-major axis $a$ and semi-minor axis $b$. Flattening is $f = (a-b)/a$, the first eccentricity squared is $e^2 = (a^2 - b^2)/a^2 = 2f - f^2$. **Geodetic latitude** $\varphi$ is the angle between the equatorial plane and the *normal* to the ellipsoid at a point; it is not the angle to the centre (geocentric latitude $\psi$), and the two differ by up to about 11.5′ at mid-latitudes — a difference of roughly 21 km on the ground, which is why "latitude" in a file without a stated ellipsoid is not a coordinate.

The radius of curvature in the prime vertical, $N(\varphi) = a / \sqrt{1 - e^2\sin^2\varphi}$ (not to be confused with geoid undulation $N$; the symbol collision is unfortunate and universal), is the quantity that converts $(\varphi, \lambda, h)$ to Earth-centred Cartesian coordinates and back — the computation that every GNSS receiver performs and that the Mathematics section of this chapter lays out. Along a meridian the radius of curvature is $M(\varphi) = a(1-e^2)/(1 - e^2\sin^2\varphi)^{3/2}$; $M$ is about 6 335 km at the equator and 6 400 km at the poles, which is the modern echo of what Maupertuis measured.

## 7.2 Gravity and the geoid

The ellipsoid is a convenient fiction. Water does not care about it; water settles on an **equipotential surface** of the Earth's actual gravity field. The **geoid** is the particular equipotential surface that best fits global mean sea level — in modern practice the surface with potential $W_0 = 62\,636\,853.4\ \mathrm{m^2\,s^{-2}}$, the conventional value adopted by the IAG in 2015 (Sánchez et al. 2016). Its departure from the GRS80 ellipsoid, the **geoid undulation** or geoid height $N$, ranges from about −106 m south of India to about +85 m near New Guinea. The geoid is smooth compared with topography but not featureless: it has structure at every scale from the Indian Ocean low to metre-scale bumps over mountain ranges.

### 7.2.1 Gravity anomalies

Gravity measured at the surface, $g$, varies with latitude (centrifugal acceleration and the equatorial bulge), with height (the inverse-square law), and with the mass distribution beneath. The latitude and height dependence are predictable and are removed by comparing $g$ with **normal gravity** $\gamma$, the gravity of the GRS80 ellipsoid. On the ellipsoid, $\gamma$ follows Somigliana's closed formula (Mathematics section); for GRS80 it runs from 9.780 326 7715 m s⁻² at the equator to 9.832 186 3685 m s⁻² at the poles, a 0.5 % variation that corresponds to about 5.2 Gal, or 5 200 mGal (1 mGal = 10⁻⁵ m s⁻²).

Reducing an observation at height $H$ to the geoid uses the **free-air gradient**, about −0.3086 mGal per metre of elevation gain. The **free-air anomaly** is $\Delta g_F = g + 0.3086\,H - \gamma$. It still contains the attraction of the rock between the station and the geoid; subtracting the attraction of an infinite slab of density ρ (conventionally 2 670 kg m⁻³), $2\pi G\rho H \approx 0.1119\,H$ mGal, gives the **simple Bouguer anomaly**, and adding a terrain correction for the departure of the real topography from a slab gives the **complete Bouguer anomaly**. Free-air anomalies are what geoid computation needs (they refer to the mass as it is); Bouguer anomalies are what geologists need (they reveal density contrasts beneath the surface). Confusing the two produces geoid errors of tens of metres in mountains.

### 7.2.2 Stokes, Molodensky, and the quasigeoid

Stokes (1849) showed that if gravity anomalies were known everywhere on the geoid, and if there were no masses outside it, the undulation at any point would follow from a global integral of the anomalies weighted by a kernel depending only on the spherical distance (Mathematics section). The two "ifs" are the problem. There are masses above the geoid — the continents — and we measure gravity on the topography, not on the geoid. Classical practice removes the topographic masses computationally, computes a geoid for the mass-reduced Earth, and restores them (the **remove–compute–restore** approach that modern regional geoids still use).

Molodensky (1945, English edition 1962) reframed the problem to avoid hypotheses about the density of the crust: solve the boundary-value problem on the actual topographic surface instead of the geoid. The resulting height system uses **normal heights** $H^*$ measured from the **quasigeoid**, which is not an equipotential surface but coincides with the geoid over the oceans and departs from it on land by $N - \zeta \approx \Delta g_B H / \bar\gamma$, where $\Delta g_B$ is the Bouguer anomaly in the same units as $\bar\gamma$ (Hofmann-Wellenhof & Moritz 2006, §8.13). The difference is centimetres in lowlands and reaches a metre or more in high mountains: at 3 000 m elevation with a Bouguer anomaly of −200 mGal, $N - \zeta \approx -2\times 10^{-3}\times 3000 / 9.8 \approx -0.6$ m. Germany, Russia, China, and much of Europe use normal heights; North America, Australia, and the UK use orthometric heights. A European DEM in DHHN2016 (normal heights) merged with one in a Helmert-orthometric system differs by a few decimetres in the Alps for this reason alone.

### 7.2.3 Deflection of the vertical

The plumb line does not point along the ellipsoid normal. The angle between them, the **deflection of the vertical** (components ξ north–south, η east–west), is a few arc seconds in lowlands and 30–60″ near great mountain ranges or trenches. A 10″ deflection is a geoid slope of 4.8 cm per kilometre — the first hint of a pattern that recurs throughout this chapter: geoid errors are **tilts and long-wavelength bumps**, not white noise. Deflections also act on instruments: a level or an IMU aligned to gravity differs from the ellipsoidal normal by the deflection, and over a 10 km trigonometric line a 10″ error is 0.48 m of height.

## 7.3 Height systems

The word "height" without a qualifier is ambiguous in at least four ways. All four are in daily use.

**Ellipsoidal height** $h$ is the geometric distance along the ellipsoid normal from the ellipsoid to the point. It is what GNSS produces, it is purely geometric, and it is reproducible to the centimetre level anywhere on Earth with the appropriate equipment. Its only disadvantage is that water does not flow along it: two points with equal $h$ can differ in gravity potential by an amount equivalent to 100 m of head, so a canal design in ellipsoidal heights would flow uphill.

**Geopotential numbers** $C = W_0 - W_P$ are the physically meaningful quantity: the potential difference between the geoid and the point, in m² s⁻² (or geopotential units, 1 gpu = 10 m² s⁻², which makes the numbers resemble metres). Two points with the same $C$ are on the same level surface; water does not flow between them. Levelling, combined with gravity, measures $C$ directly: $C = \int g\,dn$ along the levelling route. Every gravity-related height is $C$ divided by some gravity value, and the choice of that value defines the system.

**Orthometric height** $H = C / \bar g$ divides by the mean gravity along the plumb line between the geoid and the point. That mean cannot be measured; it must be modelled from the surface gravity and a density assumption. **Helmert orthometric heights** use the Poincaré–Prey reduction with a crustal density of 2 670 kg m⁻³, $\bar g \approx g + 0.0424\,H$ (mGal, $H$ in metres); NAVD88 is a Helmert system. More rigorous variants (Niethammer, Mader, and the "rigorous orthometric heights" of Santos et al. 2006) differ from Helmert by centimetres to a few decimetres in high mountains.

**Normal height** $H^* = C / \bar\gamma$ divides by the mean *normal* gravity along the normal plumb line, which is computable exactly from the ellipsoid parameters. Normal heights need no density hypothesis, which is why Molodensky's school preferred them. The surface they are measured from is the quasigeoid.

**Dynamic height** $H^{dyn} = C / \gamma_{45}$ divides by a single constant, normal gravity at 45° latitude on GRS80, 9.806 199 203 m s⁻². Dynamic heights are scaled geopotential numbers: points on the same level surface have the same dynamic height everywhere, which makes them the correct heights for hydraulics over large distances and the basis of the International Great Lakes Datum ([Chapter 9](ch09-vertical-datums.md)). Their cost is that a dynamic metre is not a geometric metre; because gravity varies by about 0.5 % from equator to pole, the ratio $\gamma_{45}/\bar g$ departs from unity by up to about ±0.27 %.

### 7.3.1 $h = H + N$ and why it is not exact

The relation every GIS user knows, $h = H + N$, says that the ellipsoidal height is the orthometric height plus the geoid undulation. It is a very good approximation, but it is not an identity, for three reasons that are worth being able to name:

1. $h$ runs along the ellipsoid normal and $H$ along the curved plumb line; the deflection of the vertical θ between them changes the length by about $H\theta^2/2$ — 0.03 mm for $H = 3\,000$ m and $\theta = 30″$ — and plumb-line curvature adds sub-millimetre terms. Negligible.
2. The real issue is **which $H$ and which $N$**. If $H$ is a normal height, the relation is $h = H^* + \zeta$ with the quasigeoid height ζ, and mixing $N$ with $H^*$ introduces the $N - \zeta$ term of §7.2.2 — decimetres in mountains. If $H$ is Helmert orthometric and $N$ was computed with a different mass reduction, the mismatch is centimetres to decimetres. If $H$ is in a national datum (NAVD88) and $N$ from a global model (EGM2008), the mismatch includes the national datum's bias and tilt (§7.4, [Chapter 9](ch09-vertical-datums.md)) — half a metre across the conterminous United States.

So the honest statement is $h = H + N + \epsilon$, where $\epsilon$ is dominated not by geometry but by definitional mismatch between the height system and the geoid model. A **hybrid geoid** (§7.4) is built precisely to drive $\epsilon$ toward zero for one specific national datum.

> **Definitions that bite.** "Geoid height" in a product's metadata may mean (a) a gravimetric geoid undulation relative to GRS80, (b) a hybrid model's separation between the ellipsoid of a *specific* geodetic datum and a *specific* levelling datum (e.g., GEOID18: NAD83(2011) to NAVD88), (c) a quasigeoid height ζ, or (d) EGM96 undulations relative to WGS84 as broadcast in many GPS receivers' internal tables. These differ by decimetres to over a metre in the same place. Before applying any grid, write down which ellipsoid it is relative to, which vertical datum it realizes, and whether it is a geoid or a quasigeoid. If the file name is "geoid.tif" and nobody can answer, the heights it produces are unvalidated.

<!-- figure: Figure 7.2 — Cross-section showing topography, geoid, quasigeoid, and ellipsoid; the heights h, H, H*, N, and ζ at a mountain point; the plumb line versus the ellipsoid normal (deflection exaggerated). -->

## 7.4 Geoid models

A **global geopotential model** (GGM) is a set of spherical-harmonic coefficients $\bar C_{nm}, \bar S_{nm}$ for the Earth's gravitational potential (Mathematics section). From them one can evaluate the potential, gravity, gravity anomalies, deflections, and geoid undulations anywhere. The spatial resolution of a model truncated at degree $n_{max}$ is about half a wavelength, $\approx 20\,000\ \mathrm{km}/n_{max}$:

| Model | Year | $n_{max}$ | Half-wavelength | Data | Stated/assessed accuracy |
|---|---|---|---|---|---|
| EGM84 ⟨H⟩ | 1984 | 180 | ~110 km | Satellite tracking, surface gravity, altimetry | several metres (regionally worse) |
| EGM96 ⟨H⟩ | 1996 | 360 | ~55 km | + more surface gravity, altimetry | ~0.5–1 m globally; metres where data were sparse |
| EGM2008 ⟨H⟩ | 2008 | 2 159 (2 190) | ~9 km | GRACE, 5′ surface gravity, altimetry, SRTM/DTM2006 fill | ~0.1–0.15 m RMS vs GNSS/levelling in well-surveyed areas; decimetres to >1 m elsewhere (Pavlis et al. 2012) |
| XGM2019e | 2019 | 5 540 (2′) | ~4 km | GOCO06s, 15′ ground gravity, topography-derived short wavelengths | comparable to EGM2008 where data are good; improved where EGM2008 used fill (Zingerle et al. 2020) |

The jump from EGM96 to EGM2008 was driven by two things: GRACE's long-wavelength field and the release of 5′×5′ terrestrial gravity grids by many countries. Where no gravity was released (parts of Africa, South America, Antarctica, Southeast Asia), EGM2008 filled the short wavelengths from topography via an assumed density relation ("fill-in" areas), and its errors there are metres rather than decimetres. Users should check the EGM2008 data-source map before trusting the model to better than a metre in those regions.

### 7.4.1 Hybrid national geoids

A gravimetric geoid gives $N$ relative to GRS80 in a geocentric frame. National vertical datums were realized by levelling, and they contain their own biases, tilts, and distortions ([Chapter 9](ch09-vertical-datums.md)). To let a GNSS user obtain heights in the national datum directly, agencies build **hybrid geoids**: a gravimetric model warped with a smooth correction surface fitted to GNSS-on-benchmark observations ($h - H_{datum}$ at marks where both are known). The hybrid model therefore inherits the datum's defects on purpose; it is a *transformation surface*, not the geoid.

- **GEOID18** (NGS, 2019; superseded GEOID12B) converts NAD83(2011) ellipsoidal heights to NAVD88 and is fitted to about 32 000 GNSS-on-benchmark points in CONUS; NGS's own assessment puts its agreement with those marks at a few centimetres (2σ) in well-controlled regions (Ahlgren et al. 2020).
- **CGG2013a** (Natural Resources Canada) is a *pure gravimetric* geoid defining CGVD2013 — Canada abandoned levelling-based realization in 2013 and defined the datum as the $W_0$ equipotential surface (Véronneau & Huang 2016; Huang & Véronneau 2013).
- **AUSGeoid2020** (Geoscience Australia) is a hybrid for AHD, with an accompanying uncertainty grid — one of the first national models to ship per-cell uncertainties, which range from about 4 cm to over 10 cm (Brown et al. 2018).
- **OSGM15** (Ordnance Survey/OSi/LPS) transforms ETRS89 heights to ODN and the Irish datums; Ordnance Survey quotes an RMS fit of about 8 mm on the Great Britain mainland, with poorer figures (a few centimetres) on offshore islands such as the Isle of Man. The **xGEOID** series (NGS, 2014–2020) were experimental gravimetric models incorporating GRAV-D airborne gravity, culminating in **GEOID2022**, the model that defines the **North American–Pacific Geopotential Datum of 2022 (NAPGD2022)**: orthometric heights become $H = h - N_{GEOID2022}$ by definition, and levelling becomes a check rather than the definition (NGS Blueprint Part 2).

### 7.4.2 How geoid models are validated

Comparison with GNSS-on-benchmark data is the standard test, but it is circular for a hybrid model (which was fitted to those data) and confounded for a gravimetric model (the benchmarks carry the levelling datum's errors). NGS designed the **Geoid Slope Validation Surveys** to break the circularity: a dedicated line surveyed with first-order levelling, absolute and relative gravity, long-occupation GNSS, and astrogeodetic deflections, so that the *slope* of the geoid along the line is known independently of any model.

- **GSVS11**: 325 km across the flat Texas Gulf Coastal Plain, 218 marks; the independent geoid slopes agreed with the then-current gravimetric models at the 1–2 cm level over distances up to a few hundred kilometres, and the survey demonstrated that airborne GRAV-D data improved the models (Smith et al. 2013).
- **GSVS14**: Iowa, moderate relief and a known long-wavelength geoid feature; results confirmed centimetre-level differential accuracy (Wang et al. 2017).
- **GSVS17**: Colorado, 350 km through the Rocky Mountains with >3 km of relief — the hard case for topographic reductions; the survey anchored the international "Colorado geoid experiment" in which 14 groups computed geoids from identical data and were compared, with the spread among well-performing solutions at the 2–3 cm level in the mountains (Wang et al. 2021).

The headline from all three: a modern gravimetric geoid computed from good terrestrial plus airborne gravity has a differential accuracy of roughly 1–2 cm over tens of kilometres and 2–4 cm over hundreds of kilometres in temperate terrain, degrading to a few centimetres more in high mountains. Those are the numbers to carry into an uncertainty budget — remembering that they describe correlated, slowly varying error.

<!-- figure: Figure 7.3 — Map of CONUS showing the GSVS11 (Texas), GSVS14 (Iowa) and GSVS17 (Colorado) lines, with a profile of geoid height along GSVS17 and the residuals of two models against the independent survey. -->

## 7.5 Measuring gravity

Geoid models are only as good as the gravity that goes into them, so it helps to know where gravity numbers come from and how good they are.

**Instruments.** Pendulums (Kater's reversible pendulum, 1817, about 1 mGal; Vening Meinesz's submarine apparatus from 1923, which found the great negative anomalies over trenches) supplied gravity until the 1930s and still lurk in the databases behind EGM84/96. **Relative spring gravimeters** (LaCoste & Romberg, Scintrex) measure differences to 5–10 µGal and are the source of most of the 5′ terrestrial data in EGM2008 — data of inhomogeneous quality, with campaign datum offsets and pre-GNSS station heights known only to tens of metres (a 10 m height error is a 3 mGal free-air error). **Absolute gravimeters** (free-fall FG5-class, ~2 µGal; cold-atom **quantum gravimeters** since the 2010s at a similar level) fix the datum of gravity networks and track long-term change from groundwater and glacial isostatic adjustment.

**Airborne gravimetry** fills the gap between sparse ground points and satellite resolution. NGS's **GRAV-D** program (Gravity for the Redefinition of the American Vertical Datum), begun in 2007, flew a stabilized-platform gravimeter at roughly 6 km altitude along 10 km-spaced lines over the United States and its territories; the project's stated goal was a geoid accurate to 2 cm where possible and 1 cm in flat terrain, and the data are the backbone of GEOID2022 (NGS Blueprint Part 2). Airborne gravity is noisy per point (around 1–2 mGal after filtering) but spatially homogeneous and free of the campaign-to-campaign datum offsets of old terrestrial data; filtered along-track resolution is around 10–20 km.

**Satellite gravimetry** supplies the long wavelengths uniformly over the planet. **GRACE** (March 2002 – October 2017) measured the range between two satellites 220 km apart to micrometres, giving the static field to about degree 150–180 and monthly fields that track mass change at ~300 km scales (Tapley et al. 2004); **GOCE** (March 2009 – November 2013) flew a gradiometer at ~255 km altitude and delivered the static field to about degree 280–300 with centimetre geoid accuracy at 100 km resolution — the largest single improvement to global geoid knowledge since satellite altimetry; **GRACE Follow-On** (May 2018) continues the series. Combination models (GOCO, EIGEN, XGM2019e) stack these with terrestrial and altimetric gravity, so any geoid model published after about 2012 has a long-wavelength field reliable at the centimetre level everywhere; what varies by region is the short-wavelength content from ground data.

> **Rule of thumb.** Over the oceans and in countries that released dense gravity, EGM2008/XGM2019e-class models are good to about a decimetre; in GRAV-D-era national models with airborne gravity, 2–5 cm; in mountainous terrain, add a few centimetres; in fill-in regions of EGM2008 (check the data-source map), expect errors of 0.5–2 m. These are 1σ-ish figures for the *absolute* undulation; relative error between points a few kilometres apart is far smaller — typically a centimetre or two — because geoid errors are long-wavelength.

## 7.6 Levelling

**Spirit levelling** (differential levelling) is still the most precise way to transfer a height difference between two points a few kilometres apart. A levelled telescope reads graduated staffs held on the back and fore points; the difference of readings is the height difference along the local level surface. First-order levelling achieves random errors around 0.5–1 mm per kilometre of double run, so a 100 km line carries roughly 5–10 mm of random error. The systematic errors are the ones that hurt national datums: staff scale and temperature, refraction (sight lines bending in a temperature gradient, which produces errors that accumulate systematically up long slopes — the mechanism blamed for much of the NAVD88 and AHD tilts), unequal sight lengths with an imperfectly collimated instrument, settling of turning points, and magnetic effects on early compensator levels. Because levelling measures $\int g\,dn$ only when gravity is observed along the route, uncorrected levelled differences are *not* orthometric height differences; the **orthometric correction** can reach decimetres in mountains, and whether it was applied with observed or normal gravity is part of a datum's definition.

Raw levelled differences around a closed loop do not sum to zero, because the sum depends on the gravity field along the route; once converted to geopotential numbers a loop should close to within the random error, and **loop closures** are the primary internal quality test, with tolerances of $3\sqrt{D}$ mm (first-order class I) and $4\sqrt{D}$ mm (class II), $D$ in km, in the FGCC *Standards and Specifications for Geodetic Control Networks* (1984), which remain the FGCS standard. Closures reveal random error and blunders but are blind to errors that are consistent in both directions — refraction up a long one-way grade, for instance — which is why national adjustments can close beautifully and still be tilted by half a metre.

**GNSS levelling** is simply $H = h - N$: an ellipsoidal height from GNSS and a model $N$. Its accuracy is the sum of the GNSS height error (1–3 cm for long static occupations, 3–5 cm for RTK, [Chapter 12](ch12-gnss.md)) and the geoid model error (§7.4). It has replaced spirit levelling for all but the most demanding work, and in Canada and in the modernized US NSRS it *is* the datum realization. The costs are that its errors are spatially correlated through the geoid model and that it cannot be checked by loop closure — a GNSS-levelling "loop" closes trivially because every height comes from the same model. Validation must therefore come from independent levelling ties (§7.4.2) or from comparison with marks the model was not fitted to.

> **Try it.** Compute the geoid undulation and the three height types at a point with GeographicLib and PROJ. With `geographiclib-tools` and the EGM2008 grid installed (`geographiclib-get-geoids egm2008-1`):
>
> ```bash
> # EGM2008 undulation N at Mt. Whitney summit (approx. 36.5785 N, 118.2923 W)
> echo "36.5785 -118.2923" | GeoidEval -n egm2008-1
> # typical output: -29.9 (metres; EGM2008 N relative to WGS84 ellipsoid)
>
> # With PROJ ≥ 7 and PROJ-data: convert an ellipsoidal height to EGM2008 orthometric
> echo "-118.2923 36.5785 4388.0" | cs2cs EPSG:4979 EPSG:9518 -d 3
> # EPSG:9518 = WGS 84 + EGM2008 height; expect H ≈ 4388.0 - (-29.9) ≈ 4417.9
> ```
>
> Then repeat with a national hybrid grid (CONUS: `EPSG:5498`, NAD83 + NAVD88 via `us_noaa_g2018u0.tif`); the two orthometric heights differ by 0.5–1.5 m in the western US — the NAVD88 datum bias relative to a global geoid, not an error in either model.

## 7.7 Mean sea level is not the geoid

If the ocean were at rest and homogeneous, its surface would be the geoid. It is neither. Winds, density differences, and the Coriolis force maintain a permanent **mean dynamic topography** (MDT): the time-averaged sea surface stands above or below the geoid by amounts that are mapped from satellite altimetry minus a GOCE-class geoid, and that range globally over about ±1–2 m. The western boundary currents are the extremes: the sea surface rises by roughly 1 m across the Gulf Stream and the Kuroshio; the Antarctic Circumpolar Current separates a sea surface about 2 m lower around Antarctica from the subtropical gyres. Along a single coast the variation is smaller but not negligible — on the order of decimetres over 1 000 km.

This has two consequences for elevation data. First, **local mean sea level at a tide gauge is not the geoid**, so a vertical datum defined as "MSL at gauge X" is offset from the geoid by the MDT at X, which differs from the MDT at gauge Y. Classical datums defined by multiple gauges (NGVD29 held 26 gauges fixed to local MSL) were therefore *distorted* to force the MDT differences into the levelling network, and that is one reason NGVD29 differs from a geoid-based datum by up to about 1.5 m across the continent ([Chapter 9](ch09-vertical-datums.md)). Second, "sea level" is not a usable height reference for DEM production without specifying the gauge, the epoch, and the datum: the three can disagree by a metre.

## 7.8 Earth tides, ocean and atmospheric loading

The solid Earth is elastic. The same lunar and solar gravitational gradients that raise ocean tides deform the crust: the **solid Earth tide** moves the ground vertically with a range of a few decimetres (peak amplitudes around 20–30 cm at low latitudes, depending on the lunar and solar geometry; the horizontal component is a few centimetres). Every GNSS position and every lidar strip is collected on a surface that is at a different height than it was six hours earlier. Processing software removes the solid Earth tide with the IERS Conventions model, which is accurate to the millimetre; a product whose heights were not tide-corrected (some real-time RTK workflows, and some older photogrammetric blocks adjusted to uncorrected GNSS) carries a decimetre-scale error that varies smoothly over hours and therefore shows up as a strip-to-strip or block-to-block offset, not as noise.

**Ocean tide loading** — the elastic response to the weight of the ocean tide — reaches 5–10 cm vertically near coasts with large ranges (Bay of Fundy, Bristol Channel, Patagonia, northwest Australia) and is still a centimetre or two several hundred kilometres inland; it is modelled from an ocean tide model (FES2014, TPXO) convolved with Green's functions. **Atmospheric loading** contributes up to 1–2 cm, hydrological loading an annual centimetre or two in large basins, the pole tide a few millimetres.

There is also the **permanent tide**, the time-averaged part of the tidal potential, which raises the geoid at the equator and lowers it at the poles relative to a hypothetical tide-free Earth. Geodetic conventions differ: ITRF coordinates are **tide-free** (the permanent deformation removed using a model), while gravity and most geoid work use **zero-tide** (direct permanent tidal potential removed, indirect deformation kept) or **mean-tide** (nothing removed, the surface the real ocean sees). The geoid differs between the mean-tide and zero-tide conventions by about $0.099 - 0.296\sin^2\varphi$ m — roughly +10 cm at the equator and −20 cm at the poles — and between zero-tide and tide-free by about $k \approx 0.3$ times that (+3 cm to −6 cm) (Ekman 1989; approximate). Mixing conventions, for example combining tide-free GNSS heights with a mean-tide geoid, introduces an error of up to a decimetre that depends only on latitude and is therefore almost impossible to notice in a regional check. The modernized NSRS (NAPGD2022) adopts the zero-tide convention; EGM2008 was published tide-free with instructions for conversion; most national hybrid geoids are consistent with whatever their GNSS-on-benchmark data were (tide-free, in practice). [Chapter 6](ch06-time-as-coordinate.md) treats the clock side of these effects and [Chapter 38](ch38-plate-motion-and-vlm.md) the secular motions.

## Then & now

The ellipsoid has been settled since 1980; the geoid is the part that keeps moving.

- **Arc measurements to space geodesy.** From the Lapland and Peru arcs (1735–1744) to Hayford's 1909 ellipsoid, flattening came from meridian arcs and was uncertain at a part in a thousand; satellite tracking after Sputnik (1957) gave $J_2$ directly, and GRS80 ⟨H⟩ and WGS84 ⟨H⟩ fixed it to better than a part per million.
- **Geoid as a diagram to geoid as a product.** Hand-drawn astrogeodetic geoids (Heiskanen's Columbus Geoid, 1957) → first satellite harmonic models (1960s) → EGM84 ⟨H⟩ (degree 180), EGM96 ⟨H⟩ (360), EGM2008 ⟨H⟩ (2 190), XGM2019e (5 540).
- **Levelling as definition to geoid as definition.** NGVD29 and NAVD88 were levelling networks; CGVD2013 (2013) and NAPGD2022 define the datum as an equipotential surface and compute heights from GNSS plus a geoid. The GSVS campaigns (2011, 2014, 2017) exist because this shift makes the geoid model the single point of failure.
- **Tides from nuisance to model.** Solid Earth tides were a known correction in gravimetry from the 1930s; routine millimetre-level modelling of tidal and loading displacements in positioning arrived with the IERS Standards (1989, 1992) and Conventions (1996, 2003, 2010).

## Mathematics

**Ellipsoid.** With semi-major axis $a$ and flattening $f$:

$$b = a(1-f), \qquad e^2 = 2f - f^2 = \frac{a^2-b^2}{a^2}, \qquad e'^2 = \frac{a^2-b^2}{b^2} = \frac{e^2}{1-e^2}.$$

For GRS80: $a = 6\,378\,137$ m, $1/f = 298.257\,222\,101$, so $f = 3.352\,810\,681\times10^{-3}$, $e^2 = 6.694\,380\,023\times10^{-3}$, $b = 6\,356\,752.314\,1$ m. Radii of curvature at geodetic latitude $\varphi$:

$$N(\varphi) = \frac{a}{\sqrt{1-e^2\sin^2\varphi}}, \qquad M(\varphi) = \frac{a(1-e^2)}{(1-e^2\sin^2\varphi)^{3/2}}.$$

Geodetic to Cartesian: $X = (N+h)\cos\varphi\cos\lambda$, $Y = (N+h)\cos\varphi\sin\lambda$, $Z = (N(1-e^2)+h)\sin\varphi$; the inverse is closed-form or iterative, and PROJ's is accurate to nanometres. Geodetic and geocentric latitude are related by $\tan\psi = (1-e^2)\tan\varphi$ on the surface, with a maximum difference of about 11.5′ near 45°.

**Normal gravity (Somigliana).** On the GRS80 ellipsoid,

$$\gamma_0(\varphi) = \gamma_e\,\frac{1 + k\sin^2\varphi}{\sqrt{1-e^2\sin^2\varphi}}, \qquad k = \frac{b\gamma_p}{a\gamma_e} - 1,$$

with $\gamma_e = 9.780\,326\,7715$ m s⁻², $\gamma_p = 9.832\,186\,3685$ m s⁻², $k = 0.001\,931\,851\,353$. Above the ellipsoid, to second order in $h$,

$$\gamma(\varphi,h) = \gamma_0\left[1 - \frac{2}{a}\left(1 + f + m - 2f\sin^2\varphi\right)h + \frac{3}{a^2}h^2\right], \qquad m = \frac{\omega^2 a^2 b}{GM},$$

which gives the free-air gradient $\partial\gamma/\partial h \approx -0.3086$ mGal m⁻¹ (slightly latitude dependent: −0.3088 at the equator, −0.3083 at the poles, approximately).

**Spherical-harmonic expansion of the gravitational potential.** Outside the masses,

$$V(r,\theta,\lambda) = \frac{GM}{r}\left[1 + \sum_{n=2}^{n_{max}} \left(\frac{a}{r}\right)^n \sum_{m=0}^{n} \big(\bar C_{nm}\cos m\lambda + \bar S_{nm}\sin m\lambda\big)\bar P_{nm}(\cos\theta)\right],$$

with $\theta$ the geocentric colatitude and $\bar P_{nm}$ fully normalized associated Legendre functions. The gravity potential is $W = V + \tfrac{1}{2}\omega^2 r^2\sin^2\theta$. The **disturbing potential** $T = W - U$ ($U$ the normal potential of the reference ellipsoid) has the same form with the even zonal terms of $U$ removed. **Bruns' formula** links it to the geoid: $N = T/\gamma$ (on the ellipsoid, to first order), and the gravity anomaly is $\Delta g = -\partial T/\partial r - \tfrac{2}{r}T$ in spherical approximation. Degree $n$ corresponds to half-wavelength $\pi R/n \approx 20\,000\ \mathrm{km}/n$. In practice a GGM is evaluated with a stable recursion (Holmes & Featherstone 2002) — writing your own above degree ~1 000 is a numerical trap; use pyshtools, GeographicLib, or the ICGEM service.

**Stokes' integral (sketch).** With $\Delta g$ given on a sphere of radius $R$ and no masses outside it,

$$N(P) = \frac{R}{4\pi\gamma}\iint_\sigma \Delta g\, S(\psi)\, d\sigma, \qquad S(\psi) = \frac{1}{\sin(\psi/2)} - 6\sin\frac{\psi}{2} + 1 - 5\cos\psi - 3\cos\psi\,\ln\!\Big(\sin\frac{\psi}{2} + \sin^2\frac{\psi}{2}\Big),$$

where $\psi$ is the spherical distance between $P$ and the integration element. $S(\psi)$ diverges as $1/\psi$ near the computation point and decays slowly, which is why the integral needs global data: regional computations use a GGM for the far zone and integrate local gravity only within a cap (remove–compute–restore). The Molodensky counterpart replaces $\Delta g$ on the geoid with anomalies on the telluroid and $N$ with the height anomaly $\zeta$ (plus correction terms $G_1$ that depend on terrain slope).

**Geopotential numbers and heights.** With $W_0$ on the geoid and $W_P$ at the point,

$$C_P = W_0 - W_P = \int_0^P g\,dn \approx \sum_i \bar g_i\,\Delta n_i ,$$

summing levelled increments $\Delta n_i$ weighted by the local gravity. Then

$$H = \frac{C}{\bar g}, \qquad H^* = \frac{C}{\bar\gamma}, \qquad H^{dyn} = \frac{C}{\gamma_{45}}, \qquad \gamma_{45} = 9.806\,199\,203\ \mathrm{m\,s^{-2}}\ (\text{GRS80}),$$

with the Helmert approximation $\bar g \approx g_P + 0.0424\,H$ (mGal, $H$ in m) and $\bar\gamma$ evaluated from the normal gravity formula at height $H^*/2$ (iteratively). The relations to the ellipsoidal height are

$$h = H + N \quad (\text{orthometric}), \qquad h = H^* + \zeta \quad (\text{normal}), \qquad N - \zeta = H - H^* \approx \frac{\Delta g_B}{\bar\gamma}\,H.$$

Worked numbers: at a point with $g = 979\,650.0$ mGal and a levelled-plus-gravity geopotential number $C = 1\,225.50$ gpu (= 12 255.0 m² s⁻²), the Helmert mean gravity (using a provisional $H \approx 1\,250$ m) is $\bar g \approx 979\,650.0 + 0.0424\times1\,250 = 979\,703.0$ mGal $= 9.797\,030$ m s⁻², so $H = 12\,255.0 / 9.797\,030 = 1\,250.89$ m — the arithmetic shows why geopotential units were chosen to make $C$ numerically close to metres. The dynamic height is $H^{dyn} = 12\,255.0 / 9.806\,199 = 1\,249.72$ m, 1.17 m less than the orthometric height, purely because of the choice of divisor. Two lake gauges with equal $C$ have equal dynamic heights but orthometric heights that can differ by decimetres over the length of Lake Superior — hence IGLD 1985 ([Chapter 9](ch09-vertical-datums.md)).

## Validation & uncertainty

The subject of this chapter enters a DEM's error budget at exactly one place — the conversion between ellipsoidal and gravity-related heights — but it enters every DEM that was ever referenced to GNSS, which is nearly all of them since about 1995. The errors have a specific character that the standard accuracy statistics are poor at describing.

### How the errors arise

1. **Geoid model commission error.** The model's $N$ differs from the true separation between its stated ellipsoid and its stated vertical datum. For a modern gravimetric model in a well-surveyed temperate region this is 2–5 cm (1σ); for a hybrid model on its own fitted marks, a few centimetres; in mountains, fill-in regions, or offshore beyond the GNSS-on-benchmark data, decimetres. The error field is smooth, with correlation lengths of tens to hundreds of kilometres.
2. **Datum mismatch.** The model realizes a different vertical datum from the one the user wanted (EGM2008 undulations applied to produce "NAVD88" heights; a quasigeoid applied as a geoid; a tide-free model mixed with zero-tide heights). These are biases and tilts of 0.1–1.5 m that no amount of averaging reduces.
3. **Ellipsoid/frame mismatch.** The model was built for one geodetic frame (NAD83(2011), ITRF2014) and applied to heights in another. Frames differ in height by up to about 1–2 m (NAD83 vs ITRF, [Chapter 8](ch08-horizontal-datums.md)), and ignoring this is the single most common gross vertical error in merged North American products.
4. **Grid interpolation and temporal change.** Bilinear interpolation of a 1′ geoid grid errs at the millimetre level (up to a centimetre with 2.5′ grids in rugged terrain). Secular geoid change is sub-millimetre per year except in deglaciating regions (1–2 mm/yr); vertical land motion ([Chapter 38](ch38-plate-motion-and-vlm.md)) changes $h$ but not $N$, so a hybrid geoid fitted to benchmarks that have subsided since they were levelled encodes the subsidence as geoid error.

### How they propagate

Because geoid errors are spatially correlated, their effect depends on the scale of the quantity computed. **Absolute heights** inherit the full error. **Slopes and local relief** over distances shorter than the correlation length are almost unaffected (a 10 cm error with 100 km correlation length is a 1 µrad tilt). **Volumes and flood extents** over 10–100 km are affected by the regional tilt: a 5 cm tilt across a 20 km floodplain shifts a flood boundary on a 1:1000 slope by 50 m at one end. **Merged products** from sources that used different geoid models show steps along the seam equal to the model difference — typically 5–50 cm between a global and a national model, too small to be obvious and too large to ignore.

### How to test

- **Independent GNSS-on-benchmark residuals.** Compute $h_{GNSS} - H_{levelled} - N_{model}$ at marks the model was not fitted to. Report the mean (bias), the standard deviation, and — critically — a map or a plot against distance, because a tilt shows as a trend and a bias of zero can hide ±20 cm residuals at opposite ends of the area. NGS publishes the residual statistics for every GEOID release; Geoscience Australia ships the AUSGeoid2020 uncertainty grid; check them before accepting a model's quoted accuracy for your region.
- **Model-to-model difference maps.** `gdal_calc` between EGM2008 and the national hybrid over your project area shows the datum offset and its gradient. Where the difference has structure at your project's scale, you have a decision to make, not an error to average.
- **Semivariogram and latitude checks.** A variogram of the residuals gives the correlation length to use when propagating geoid error (and its nugget, the GNSS-plus-levelling noise floor); a latitude-dependent trend of order 10 cm per 30° with the sign of $-\sin^2\varphi$ points to a permanent-tide convention mismatch.
- **Closure around the seam.** For merged products, difference the two sources in the overlap and test the mean difference against the expected geoid-model difference. If they agree, the step is a datum artefact and should be removed by transformation, not by feathering ([Chapter 48](ch48-compositing.md)).

> **Uncertainty budget.** Orthometric height of a single GNSS-derived point, $H = h - N$, in CONUS using NAD83(2011)/GEOID18, temperate lowland, long static occupation. Values are indicative 1σ and the sources are the bodies cited in this chapter; adjust for your region.
>
> | Component | 1σ (cm) | Character | Source |
> |---|---|---|---|
> | GNSS ellipsoidal height, 4 h static, OPUS-class processing | 1.5–2.5 | random per point, some daily correlation | NGS OPUS statistics; [Chapter 12](ch12-gnss.md) |
> | GEOID18 vs NAVD88 at independent marks | 2–3 | correlated, 50–200 km | NGS GEOID18 technical details |
> | NAVD88 itself vs the geopotential surface it nominally realizes | 10–50 (tilt, not noise) | bias/tilt across continent | NGS Blueprint Part 2 |
> | Permanent-tide convention mismatch (if any) | 0–10 | latitude-dependent bias | Ekman 1989 |
> | Geoid grid interpolation | <0.5 | random | — |
> | Vertical land motion since benchmark levelling (local) | 0–5 (cm per decade in subsiding areas) | regional trend | [Chapter 38](ch38-plate-motion-and-vlm.md) |
> | **Total, consistent with NAVD88 (what GEOID18 is for)** | **~3–4** | — | root-sum-square of rows 1, 2, 5 |
> | **Total, if the question is "height above the true geoid"** | **10–50** | dominated by datum tilt | rows 1–5 |
>
> The two totals are the whole lesson: the same numbers answer two different questions with an order-of-magnitude different uncertainty, and only the second question is the one a flood model or a sea-level study is asking.

### What to report

For any product whose heights pass through a geoid model: the input frame and epoch, the geoid model's exact name and version, the vertical datum it realizes, the permanent-tide convention, and the model's assessed accuracy *in the project region* from the issuing agency. For merged products: the model used by each source and the residual step at seams after transformation.

## Software

**Open source.**
- **PROJ** (≥ 7) with **PROJ-data**: geoid and quasigeoid grids as Cloud-Optimized GeoTIFFs (`us_noaa_g2018u0.tif`, `au_ga_AUSGeoid2020`, `uk_os_OSGM15_GB.tif`, `us_nga_egm08_25.tif`, and so on), usable via `cs2cs`, `projinfo`, and the `+proj=vgridshift` pipeline step. Caveat: PROJ's network grid fetching defaults to off; a missing grid silently yields no vertical transformation unless you check `projinfo` output or set `PROJ_NETWORK=ON`.
- **GeographicLib** (`GeoidEval`, `Gravity`, `MagneticField`): evaluates EGM84/96/2008 undulations from its own grids and computes the full gravity field from GGM coefficients; the C++ and Python bindings are the most reliable way to get $N$, $\gamma$, and deflections in a script. Caveat: its EGM2008 grids are interpolated from the harmonic model and have small (mm-level) interpolation differences from NGA's official grids.
- **pyshtools**: spherical-harmonic analysis and synthesis in Python — evaluate a GGM to arbitrary degree, compute spectra, compare models by degree. **ICGEM calculation service** (GFZ): evaluates any published GGM on a grid or at points, with choice of tide system and ellipsoid (caveat: "height anomaly" and "geoid undulation" differ by $N-\zeta$).


**Free but closed.** NGA's EGM2008 synthesis program and grids; Geoscience Australia's AUSGeoid2020 tool; Ordnance Survey's Grid InQuest II.

**Commercial.** Trimble Business Center, Leica Infinity, and Topcon Magnet bundle geoid models (caveat: the bundled release may lag the agency's current one); CARIS and QPS Qimera handle hydrographic separation models ([Chapter 9](ch09-vertical-datums.md)); Esri ArcGIS Pro applies vertical transformations through PROJ/EPSG grids.

## Standards & guides

- **IERS Conventions (2010)**, Petit & Luzum (eds.), IERS Technical Note 36 — the authoritative models for solid Earth tides, ocean and atmospheric loading, permanent tide conventions, and the GRS80/ITRF constants used in positioning.
- **IAG Resolution 1 (2015)** — conventional value of $W_0 = 62\,636\,853.4$ m² s⁻² for the International Height Reference System (IHRS); Sánchez et al. 2016 describe the derivation.
- **NGS Blueprint for 2022, Part 1: Geometric Coordinates** (NOAA Technical Report NOS NGS 62, 2017, revised 2021); **Part 2: Geopotential Coordinates** (NOS NGS 64, 2017); **Part 3: Working in the Modernized NSRS** (NOS NGS 67, 2019) — how NAPGD2022 and GEOID2022 are defined and how heights will be computed.
- **Geodetic Reference System 1980**, Moritz 2000, *Journal of Geodesy* 74(1):128–162 — the definitive constants and derived quantities for GRS80.
- **NIMA TR8350.2 (3rd ed., 2000) / NGA.STND.0036 (2014)** — the WGS84 definition, including EGM96/EGM2008 as its geoid.

## Pitfalls

- **Subtracting EGM2008 (or the receiver's internal EGM96) from GNSS heights and calling the result NAVD88, AHD, or ODN.** It happens because the global model is the default in receivers and software. Detect by comparing with a few national benchmarks: a bias of 0.3–1.5 m with a regional trend is the signature. Avoid by using the national hybrid model for the national datum and recording which model was used.
- **Treating "mean sea level" as zero everywhere.** MDT varies by ±1–2 m globally and decimetres along a coast; datums tied to different gauges differ accordingly. Ask which gauge, which epoch, which datum ([Chapter 9](ch09-vertical-datums.md)).
- **Mixing orthometric and normal heights.** European products in DHHN2016, EVRF2019, or Russian/Chinese datums are normal heights; the difference from orthometric is $N-\zeta$, decimetres in mountains. Detect through mountain-only discrepancies that scale with elevation and Bouguer anomaly; avoid by transforming via the quasigeoid.
- **Ignoring dynamic heights on large lakes.** On the Great Lakes, IGLD 1985 dynamic heights differ from orthometric by up to decimetres over a lake's length; a shoreline "at 183.2 m" is only level in dynamic heights. Use IGLD for anything hydraulic and convert explicitly.
- **Treating geoid error as white noise in the uncertainty budget.** Geoid error is a tilt and long-wavelength bump; averaging many points does not reduce it, and it is invisible to slope-based checks. Report it separately, with its correlation length, and test with distance-dependent residual plots.
- **Applying a land hybrid geoid offshore.** Hybrid models are unconstrained beyond the coast and may be clipped, extrapolated, or blended to the gravimetric model; errors grow to decimetres a few tens of kilometres out. Use the separation model built for the purpose (VDatum, VORF, AusCoastVDT; [Chapter 9](ch09-vertical-datums.md)).
- **Mixing permanent-tide conventions.** Tide-free GNSS heights plus a mean-tide geoid gives a latitude-dependent error up to ~10–20 cm. Check the convention statement in the model documentation (EGM2008: tide-free; NAPGD2022: zero-tide) and convert.
- **Forgetting that GNSS levelling has no loop closure.** A network of GNSS-derived orthometric heights "closes" perfectly because all heights share the geoid model; the model's error is undetectable from within. Tie to independent levelled marks.

## Key takeaways

- GNSS gives ellipsoidal heights $h$; nearly every user wants a gravity-related height $H$ (or $H^*$); the geoid (or quasigeoid) model is the bridge, and $h = H + N$ is exact only when the model realizes precisely the datum you want.
- Orthometric, normal, and dynamic heights are the same geopotential number divided by different gravity values; the differences are centimetres in lowlands, decimetres to a metre in high mountains, and decimetres over the length of a large lake.
- Modern global models (EGM2008, XGM2019e) are good to about a decimetre where gravity data were dense and to metres where they were not; national models with airborne gravity reach 2–5 cm; differential accuracy over a few kilometres is a centimetre or two in all of them.
- Geoid-model errors are spatially correlated tilts and bumps with correlation lengths of tens to hundreds of kilometres: they do not average out, they do not show in slope, and they create steps at seams between products that used different models.
- Mean sea level departs from the geoid by up to ±1–2 m (mean dynamic topography); "sea level" without a gauge, epoch, and datum is not a height reference.
- Validate geoid use with independent GNSS-on-benchmark residuals plotted against position and distance, not with a single RMSE; report the model name, version, realized datum, frame, and tide convention in every product.

## References

- Brown, N. J., McCubbine, J. C., Featherstone, W. E., Gowans, N., Woods, A., & Baran, I. (2018). AUSGeoid2020 combined gravimetric–geometric model: location-specific uncertainties and baseline-length-dependent error decorrelation. *Journal of Geodesy*, 92(12):1457–1465. doi:10.1007/s00190-018-1202-7
- Ekman, M. (1989). Impacts of geodynamic phenomena on systems for height and gravity. *Bulletin Géodésique*, 63(3):281–296.
- Heiskanen, W. A., & Moritz, H. (1967). *Physical Geodesy*. W. H. Freeman, San Francisco.
- Hirt, C., Claessens, S., Fecher, T., Kuhn, M., Pail, R., & Rexer, M. (2013). New ultrahigh-resolution picture of Earth's gravity field. *Geophysical Research Letters*, 40(16):4279–4283. doi:10.1002/grl.50838
- Hofmann-Wellenhof, B., & Moritz, H. (2006). *Physical Geodesy* (2nd ed.). Springer, Vienna.
- Holmes, S. A., & Featherstone, W. E. (2002). A unified approach to the Clenshaw summation and the recursive computation of very high degree and order normalised associated Legendre functions. *Journal of Geodesy*, 76(5):279–299. doi:10.1007/s00190-002-0216-2
- Huang, J., & Véronneau, M. (2013). Canadian gravimetric geoid model 2010. *Journal of Geodesy*, 87(8):771–790. doi:10.1007/s00190-013-0645-0
- Ahlgren, K., Scott, G., Zilkoski, D., Shaw, B., & Paudel, N. (2020). *GEOID18*. NOAA Technical Report NOS NGS 72. NOAA, Silver Spring.
- Jekeli, C. (2016). *Geometric Reference Systems in Geodesy* (August 2016 ed.). Lecture notes, Division of Geodetic Science, School of Earth Sciences, Ohio State University.
- Meyer, T. H. (2010). *Introduction to Geometrical and Physical Geodesy: Foundations of Geomatics*. Esri Press, Redlands.
- National Geodetic Survey (2017). *Blueprint for 2022, Part 1: Geometric Coordinates*. NOAA Technical Report NOS NGS 62 (revised 2021). NOAA, Silver Spring.
- National Geodetic Survey (2017). *Blueprint for 2022, Part 2: Geopotential Coordinates*. NOAA Technical Report NOS NGS 64. NOAA, Silver Spring.
- National Geodetic Survey (2019). *Blueprint for 2022, Part 3: Working in the Modernized NSRS*. NOAA Technical Report NOS NGS 67. NOAA, Silver Spring.
- Pavlis, N. K., Holmes, S. A., Kenyon, S. C., & Factor, J. K. (2012). The development and evaluation of the Earth Gravitational Model 2008 (EGM2008). *Journal of Geophysical Research: Solid Earth*, 117:B04406. doi:10.1029/2011JB008916
- Petit, G., & Luzum, B. (eds.) (2010). *IERS Conventions (2010)*. IERS Technical Note 36. Verlag des Bundesamts für Kartographie und Geodäsie, Frankfurt am Main.
- Sánchez, L., Čunderlík, R., Dayoub, N., Mikula, K., Minarechová, Z., Šíma, Z., Vatrt, V., & Vojtíšková, M. (2016). A conventional value for the geoid reference potential $W_0$. *Journal of Geodesy*, 90(9):815–835. doi:10.1007/s00190-016-0913-x
- Smith, D. A., Holmes, S. A., Li, X., Guillaume, S., Wang, Y. M., Bürki, B., Roman, D. R., & Damiani, T. M. (2013). Confirming regional 1 cm differential geoid accuracy from airborne gravimetry: the Geoid Slope Validation Survey of 2011. *Journal of Geodesy*, 87(10–12):885–907. doi:10.1007/s00190-013-0653-0
- Tapley, B. D., Bettadpur, S., Watkins, M., & Reigber, C. (2004). The gravity recovery and climate experiment: Mission overview and early results. *Geophysical Research Letters*, 31:L09607. doi:10.1029/2004GL019920
- Torge, W., & Müller, J. (2012). *Geodesy* (4th ed.). De Gruyter, Berlin.
- Vaníček, P., & Krakiwsky, E. J. (1986). *Geodesy: The Concepts* (2nd ed.). North-Holland, Amsterdam.
- Véronneau, M., & Huang, J. (2016). The Canadian Geodetic Vertical Datum of 2013 (CGVD2013). *Geomatica*, 70(1):9–19. doi:10.5623/cig2016-101
- Wang, Y. M., Sánchez, L., Ågren, J., Huang, J., Forsberg, R., Abd-Elmotaal, H. A., et al. (2021). Colorado geoid computation experiment: overview and summary. *Journal of Geodesy*, 95:127. doi:10.1007/s00190-021-01567-9
- Zingerle, P., Pail, R., Gruber, T., & Oikonomidou, X. (2020). The combined global gravity field model XGM2019e. *Journal of Geodesy*, 94:66. doi:10.1007/s00190-020-01398-0

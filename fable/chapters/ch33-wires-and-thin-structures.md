# Chapter 33 — Wires, power lines, antennas, and other thin or moving structures

> **Part VII — From sensor data to products.** The chapter about the objects that every surface model is most likely to miss and that a pilot, a drone, or a line crew most needs to know about: thin, tall, specular, and never quite still.

**In this chapter.** A conductor 3 cm across, strung 300 m between towers, is invisible to most of the instruments that build DEMs and lethal to most of the vehicles that use them. You will be able to explain, with numbers, why wires, guy lines, antennas, fences, turbine blades, and crane booms drop out of lidar clouds, photogrammetric meshes, and radar DSMs; how corridor surveys recover them with Hough and RANSAC line finding, PCA linearity, and catenary fitting into LAS wire classes 13–16; and why a wire's position is a function of conductor temperature, wind, ice, and age, so that a clearance measured on a cold morning says little about a hot afternoon. You will work a sag–temperature example in the IEEE 738 framework, compare DSMs with obstacle databases (FAA DOF, ICAO eTOD, NGA DVOF), decide by use whether a DSM should contain wires, recognise wires masquerading as ground or floating as SfM ghosts, and set up a NERC FAC-003 vegetation-clearance analysis.

## 33.1 Why they are missed

Everything about a wire works against the sampling assumptions behind a DEM. Start with geometry. A DEM is built from samples whose spacing is set by the **footprint** of the measurement and the **density** of the sampling pattern. A typical topographic lidar survey at 8–20 points m⁻² has a laser footprint of 20–50 cm on the ground and a nominal pulse spacing of 20–35 cm. A transmission conductor presents a cross-section of 1–4 cm; a distribution line or guy wire 0.5–1.5 cm; a fence wire 2–3 mm. The question is not whether the beam hits the wire—along a 300 m span, hundreds of pulses will—but whether the hit produces a *detectable return*. A pulse whose 30 cm footprint is cut by a 2 cm conductor returns at most a few per cent of its energy from the wire; the rest continues to the ground and produces a strong later return, and a discrete-return receiver with a threshold set to reject noise often registers only the ground. Whether the wire appears depends on the receiver's sensitivity to weak first returns, the pulse energy, the conductor's reflectance at the laser wavelength, and the angle at which the beam meets the wire.

Angle brings the second mechanism, **specularity**. A stranded conductor is approximately a bundle of cylinders, and a cylinder returns energy to the sensor only when the beam is nearly perpendicular to its axis. Scan patterns that cross a line at a shallow angle see fewer returns per metre than patterns crossing at right angles; corridor surveys are flown along the line precisely so that the across-track scan crosses conductors near 90°. A county-wide DTM survey with north–south flight lines meets an east–west corridor at whatever angle geography dictates and may capture it in one strip but not the next.

Photogrammetry fails for a third reason: **non-reconstruction**. Dense matching recovers a surface by finding the same texture patch in two or more images. A wire against sky or varied ground has no stable patch of its own; it is thinner than the matching window, its background changes with viewing geometry, and the matcher returns the background. The result is a DSM with no wire and no hole where the wire was. Multi-view stereo occasionally recovers a fragment of a thick bundle or a smeared ridge along a line seen against uniform ground, but no production photogrammetric DSM should be assumed to contain wires ([Chapter 22](ch22-photogrammetry-sfm.md)).

Radar is different again. The **radar cross-section** of a long thin conductor is strongly polarisation- and orientation-dependent: a wire parallel to the electric-field vector and perpendicular to the look direction can be a bright extended scatterer, while the same wire rotated 90° is almost invisible. SAR images of corridors show towers as bright points and sometimes a faint line between them, but an InSAR DSM at 10–30 m posting absorbs the wire's phase contribution into the resolution cell with the ground beneath it ([Chapter 21](ch21-radar-sar-insar.md)).

Towers and masts are a partial exception. A 40 m lattice tower has a footprint of several metres and plentiful returns; towers are routinely captured. A thin monopole, a guyed mast with a 0.5 m triangular section, or a rooftop whip antenna is different: the top few metres may yield a handful of returns or none, and a 1 m DSM records whichever return happened to be highest, with no guarantee it was the tip. Under-estimation or absence is the normal case, which is why obstacle databases are built from surveys that target obstacles explicitly rather than from general-purpose DSMs (§33.4).

<!-- figure: Figure 33.1 — Schematic cross-sections of a lidar footprint (30 cm) and a 2 cm conductor, with the fraction of pulse energy returned; next to it, a scan-geometry diagram showing why returns per metre of wire fall with the angle between scan direction and wire. -->

> **Rule of thumb.** For discrete-return topographic lidar, expect usable returns from transmission conductors (≥ 2 cm) at ≥ 10 points m⁻² when the scan crosses the line within ±30° of perpendicular and weak first returns are recorded; expect distribution lines and guy wires to be fragmentary below ~20 points m⁻² and fence wires to be absent except in dense terrestrial or low-altitude UAV data. Experience-based thresholds, not guarantees; receiver sensitivity and conductor condition move them by a factor of two.

## 33.2 Detection and modeling

Where wires are the target, the acquisition is designed for them: helicopter or fixed-wing flights along the corridor at low altitude (often 100–400 m above the line), high pulse rates, narrow fields of view, and 30–200 points m⁻² on the conductors. The processing problem is then to extract the few per cent of points on wires, insulators, and towers from a cloud dominated by ground and vegetation, and to fit physically meaningful curves to them.

The standard pipeline has four stages. **Candidate selection** removes ground and most vegetation with a height-above-ground threshold (conductors on a 110 kV line are rarely below 6 m at mid-span) and often an intensity filter. **Local geometry** classifies each remaining point by the shape of its neighbourhood: the covariance of the $k$ nearest neighbours has eigenvalues $\lambda_1 \ge \lambda_2 \ge \lambda_3$, and the **linearity** $L = (\lambda_1 - \lambda_2)/\lambda_1$ is near 1 on a wire and near 0 on a planar roof or in a volumetric crown. A neighbourhood radius of 1–3 m is typical; too small sees individual returns as isolated, too large merges adjacent conductors of a bundle. **Line extraction** groups high-linearity points into candidate lines, most commonly with a Hough transform in plan view (a span projects to a nearly straight line, so a 2D $(\rho, \theta)$ accumulator finds it robustly) or with RANSAC fitting of 3D segments. McLaughlin (2006) demonstrated the covariance-feature approach on airborne lidar; later work added supervised classifiers (random forests, JointBoost) on the same features and, recently, point-wise deep networks trained on labelled corridor data. **Model fitting** replaces point groups with curves. In the vertical plane of the span a conductor hangs as a **catenary**; fitting its parameter and attachment points gives a compact, physically interpretable model and lets gaps be bridged by the model rather than by interpolation. Jwa and Sohn (2012) formalised this as **piecewise catenary growing**: start from a seed segment, extend along the line while the fit holds, start a new piece where the geometry breaks at a tower. Where points are too few to constrain the catenary, a parabola is adequate (Mathematics section).

Towers are found separately, as vertical clusters with large height range and high density in a small plan footprint, or as the places where fitted catenaries terminate; tower positions then fix span lengths and attachment heights, which constrains the catenary fits.

The output goes into the LAS point classes that ASPRS added in LAS 1.4 for this purpose: class 13 **Wire – Guard (Shield)**, 14 **Wire – Conductor (Phase)**, 15 **Transmission Tower**, and 16 **Wire-structure Connector** (insulators). These are defined for point data record formats 6–10; a LAS 1.2 file with the older class table has no standard place for wires, and producers have used class 14 or project codes inconsistently. A dataset with wire classes populated is one that was processed to find wires; one without may still contain wires in the unclassified or high-vegetation bins. Beyond the points, utilities want a **vector model**: a catenary per conductor per span, with attachment heights, mid-span sag, conductor identifier, and ambient and conductor temperature at acquisition. That model, not the point cloud, is what clearance software consumes.

Corridor mapping programs institutionalise this. Many transmission operators fly their networks on a 1–5 year cycle, and in the United States the reliability requirements of §33.7 drove a wave of corridor lidar after 2007. Deliverables are typically a classified cloud with classes 13–16 populated, a vector line model importable to PLS-CADD, orthoimagery, a vegetation-encroachment report, and a weather-and-load record per flight.

> **Try it.** Find linear structures above the ground in a classified corridor tile with PDAL's covariance features. Expected outcome: a LAZ file in which points with high linearity above 6 m AGL are assigned class 14; opening it in CloudCompare and colouring by classification shows the conductors as continuous threads between towers, with tree crowns and roofs left in their original classes.
>
> ```json
> {
>   "pipeline": [
>     "corridor_tile.laz",
>     {"type": "filters.hag_nn", "count": 8},
>     {"type": "filters.range", "limits": "HeightAboveGround[6:]"},
>     {"type": "filters.covariancefeatures", "knn": 16,
>      "feature_set": "Linearity,Planarity,Verticality"},
>     {"type": "filters.assign",
>      "value": ["Classification = 14 WHERE Linearity > 0.9 && Planarity < 0.2"]},
>     {"type": "writers.las", "filename": "corridor_wires.laz",
>      "minor_version": 4, "dataformat_id": 6, "extra_dims": "all"}
>   ]
> }
> ```
>
> Run with `pdal pipeline wires.json`. The thresholds are starting points; lower `Linearity` to 0.8 if conductors fragment, and add a radius-outlier pass if lone branch tips survive.

## 33.3 Motion and time scales

A wire is not a fixed object with a position; it is a mechanical system with a state. Four processes move it, on four time scales.

**Conductor temperature** is the dominant term. Length depends on temperature through thermal expansion, and sag depends on length through the catenary geometry. IEEE Std 738 (current edition 2023; the 2012 edition is still widely cited) provides the heat-balance model relating current, solar heating, wind, and ambient temperature to conductor temperature: ohmic heating $I^2 R(T_c)$ plus solar gain $q_s$ balance convective loss $q_c$ and radiative loss $q_r$. The consequence for surveyors is that the same span can hang with 9 m of sag at 15 °C under light load and 12 m at 100 °C under heavy load (Mathematics section). Lines are designed to a **maximum operating temperature** (commonly 75–100 °C for conventional ACSR, higher for high-temperature low-sag conductors), and the clearance that matters legally is the clearance at that temperature, not at whatever temperature the conductor had when surveyed. Every corridor deliverable therefore records, per flight, ambient temperature, wind, solar conditions, and the line current from the utility's SCADA, so that the measured catenary can be **re-sagged** to the design temperature before any clearance is judged. Conductor temperature at survey time is usually estimated from these inputs with the IEEE 738 steady-state equations; line-mounted sensors used for dynamic line rating increasingly measure it directly.

**Wind** acts in seconds to minutes. Steady wind swings a span laterally into a **blow-out** angle whose tangent is the ratio of drag per unit length to weight per unit length—of order 15° and 2–3 m of mid-span displacement for a 3 cm conductor in a 15 m s⁻¹ wind (Mathematics section). Gusts superimpose oscillation. **Galloping**—low-frequency (0.1–1 Hz), high-amplitude (metres) vertical oscillation of iced or asymmetrically loaded conductors in moderate wind—can swing a conductor through an amplitude comparable to its sag; **aeolian vibration** (10–100 Hz, millimetres to centimetres) is invisible to a survey but matters for fatigue. Two scan passes a few minutes apart will not place the conductor in the same position; in moderate wind the across-track scatter of wire points within one pass is itself a measure of motion. Clearance surveys are flown in light wind and the wind is recorded.

**Ice** acts over hours to days. Radial ice of 10–25 mm can double or triple the weight per unit length and add metres of sag; it is a design load case, not a survey condition, but partial icing or wet snow in a winter survey will bias an epoch comparison.

**Creep** acts over years. Aluminium strands under tension elongate inelastically, mostly in the first years after stringing but continuing for the line's life; a span strung decades ago hangs lower at the same temperature than when new, typically by decimetres, until re-tensioning resets it. Between lidar epochs ten years apart, creep is a real signal that looks like subsidence of the wire.

The composite lesson is that a wire position is a measurement with a state vector attached. Comparing two epochs, or a survey against a design model, requires normalising both to a common conductor temperature and still air, or accepting an uncertainty of metres.

> **Case file.** The 14 August 2003 blackout in the northeastern United States and Ontario began, in its physical chain, with three 345 kV FirstEnergy lines in Ohio sagging into trees under heavy afternoon load and high ambient temperature; each contact tripped a line and shifted load and heat to the next. The U.S.–Canada Power System Outage Task Force (2004) named inadequate vegetation management—trees allowed into the clearance envelope at design sag—among the causes. The regulatory consequence was mandatory NERC FAC-003 and, with it, routine corridor lidar that re-sags measured conductors to maximum operating temperature before computing clearances.

## 33.4 Antennas, masts, guyed towers, cranes, turbines, cable cars, fences, railings

The wire problem generalises to a family of objects sharing thin cross-section, great height relative to footprint, motion, and safety significance. Each fails in a DSM in its own way.

**Antennas and masts** range from a 1 m rooftop whip to guyed lattice masts over 600 m tall. A wide lattice is captured; the top—a thin cylinder or lightning rod—rarely yields the highest return, and the guy wires, which can reach hundreds of metres from the base and are among the most dangerous objects in aviation, are almost never present in general-purpose lidar. The DSM shows a short spike a few metres under true height and nothing along the guys. **Cranes** rotate, relocate, and appear for days; they are among the most frequently reported obstacles near heliports and construction sites and the least likely to be in any published DSM ([Chapter 27](ch27-moving-and-transient-objects.md)); an obstacle layer has a workflow for temporary notices (NOTAMs) that a terrain product cannot imitate. **Wind turbines** have hubs at 80–160 m and tips at 150–250 m; the tower and usually the nacelle are captured, but the blades are thin, moving, and oriented to the wind, so the top of the swept volume is almost never sampled, and a 2.5D surface cannot represent a swept disc up to 170 m across in any case. **Cable cars, ski lifts, and zip lines** are catenary systems with the same detection properties as power lines, often in steep terrain with poor scan geometry; mountain lidar programs frequently miss them. **Fences, railings, and barriers** matter less for aviation than for ground vehicles, robots, and hydraulics: a chain-link fence is transparent to lidar at any practical density; a crash barrier is captured intermittently; a flood wall 0.5 m thick is captured as a line of points but may be erased by a 1 m DTM grid or by a ground filter that treats it as a thin object. For flood models the lost flood wall is the most consequential thin-structure error in this chapter, and breaklines or an explicit structure layer are the only reliable remedy ([Chapter 61](ch61-hydrology.md)).

Because DSMs are unreliable for these objects, aviation maintains **obstacle databases** surveyed to their own standards. The FAA's **Digital Obstacle File (DOF)** lists man-made obstacles at least 200 ft (61 m) above ground, or lower where they affect instrument procedures, each with position, height above ground, elevation above mean sea level, an accuracy code, a type, and a verification status; the FAA's **Airports GIS (AGIS)** program collects obstacle and airport surveys under Advisory Circular 150/5300-18 (currently revision B). ICAO's **Annex 15** and **PANS-AIM** (Doc 10066) define **electronic terrain and obstacle data (eTOD)** in four areas of decreasing extent and increasing stringency—Area 1 (state territory), Area 2 (terminal area), Area 3 (aerodrome movement area), Area 4 (precision-approach zone)—with numerical requirements for post spacing, accuracy, confidence level, and completeness listed in [Chapter 62](ch62-navigation-and-charting.md). RTCA **DO-276** and EUROCAE **ED-98** are the industry user requirements behind the ICAO provisions. NGA's **Digital Vertical Obstruction File (DVOF)** is the military counterpart.

The contrast with a DSM is instructive. An obstacle database is a feature collection: every record is a decision that an object exists, has a height, and matters, with a date and an accuracy attached. A DSM is a field: every cell has a value, and the value says nothing about whether any object was sought or found. An obstacle may be in the database and absent from the DSM (a guyed mast) or in the DSM and absent from the database (a tall tree, a new crane). Obstacle analysis uses both—the DSM for terrain and large structures, the database for the thin and tall—and a procedure for reconciling them.

| Source | Content model | Thin objects | Wires | Currency | Accuracy statement |
|---|---|---|---|---|---|
| General-purpose lidar DSM | Raster field | Often missed or under-height | Fragmentary or absent | Single epoch | Per-dataset vertical accuracy |
| Photogrammetric DSM | Raster field | Usually missed | Absent | Single epoch | Per-dataset |
| InSAR DSM (e.g., Copernicus) | Raster field | Missed | Absent | Multi-year composite | Per-tile HEM |
| Corridor lidar + classes 13–16 | Points + vector model | Towers yes | Yes, modelled | Per flight, with weather | Per-conductor |
| FAA DOF / NGA DVOF | Feature records | Yes (above threshold) | Transmission lines as spans in some records | Continuous updates | Per-record accuracy code |
| ICAO eTOD Area 2–4 | Features + terrain | Yes, per specification | Yes, where penetrating surfaces | Per survey cycle | Per-area numerical requirement |

<!-- figure: Figure 33.2 — The same guyed broadcast mast as seen in (a) a 1 m lidar DSM (short spike, no guys), (b) a corridor-style lidar classified cloud (mast and guys), (c) an obstacle-database record (point with height AGL and AMSL). -->

## 33.5 Should a DSM include wires?

There is no universal answer; the decision is by use, and a specification that does not ask the question will be wrong for half its users.

For **aviation obstacle analysis** and **low-altitude drone route planning** the answer is yes—in a layer the user cannot accidentally omit. A drone planner that computes clearance against a DSM from which wires were removed as noise will route through the wire. The pattern the aviation standards adopt is a DSM *plus* an obstacle layer with its own completeness statement. For **urban wind and dispersion modelling** the answer is yes for masts, cranes, and turbines, which shed wakes, and no for conductors. For **hydrology and hydraulics** the answer is emphatically no: a wire that survives into a DTM as a line of elevated cells becomes a dam across the flow network, and hydro-conditioning will breach it or route around it, both wrongly ([Chapter 34](ch34-water-in-dems.md)). For **orthorectification**, wires in a DSM produce streaks; using a DTM or smoothed DSM removes them intentionally. For **viewsheds** wires are irrelevant but masts are not. For **canopy height models**, wires above forest become spurious trees of the conductor's height above ground; remove classes 13–16 before computing the nDSM.

The practical resolution is **separate layers with explicit semantics**: a DTM with no above-ground objects; a DSM whose definition states which classes were included; a vector obstacle or wire layer with per-feature attributes; and the classified point cloud, so that a user with a different need can rebuild the surface under a different rule. The USGS Lidar Base Specification, for example, requires wire classification where present at the project's density but builds its bare-earth DEM from ground points only. The error to avoid is a single DSM with an undocumented rule.

## 33.6 Wires as artefacts

Wires that are not recognised do not vanish; they corrupt. Three patterns recur.

**False ground.** Ground filters that grow a surface from the lowest points in a neighbourhood are safe where a span crosses a valley far above the terrain, but on a ridge or near a tower on a summit, conductor points can fall within the filter's tolerance of the local ground and be adopted. The result is a thin ridge in the DTM along the line, a few decimetres high and a few metres wide, invisible in a regional hillshade and glaring in a slope map. The inverse also occurs: a filter with a maximum-slope constraint sees a wire descending toward a tower and rejects the real ground beneath it.

**Floating points.** In a first-return DSM, fragmentary wire returns produce isolated cells 10–30 m above their neighbours. A median filter removes them—and the tips of masts and lightning rods with them. Isolated-point removal tuned for birds is reasonably safe for fragmentary conductors but deletes the only evidence of a guy wire. Put these points in class 7/18 or in classes 13–16 rather than deleting them, so the decision is reviewable.

**SfM ghosts.** Multi-view stereo, confronted with a wire matched in some pairs and not others, produces a diffuse cloud around the true position—a "ghost" tube a metre or more across—or a wire reconstructed at the wrong depth because the matcher locked onto the background. A density filter removes the ghost and the DSM then shows nothing. Where SfM is used near wires, state in the metadata that thin linear structures are not reconstructed and supplement with lidar or a survey of the attachments.

> **Definitions that bite.** "Wire" in LAS 1.4 means classes 13 and 14 (guard and conductor), with 16 for connectors and 15 for the tower; many utilities and older specifications use "wire" or "powerline" for all four, put every wire in class 14, or use a project code in the 64–255 range. "Obstacle" in ICAO usage is any fixed or mobile object penetrating an obstacle limitation surface, including terrain and trees; in the FAA DOF it is a man-made structure above a height threshold. A DSM that "includes obstacles" may mean either. Read the data dictionary, not the label.

## 33.7 Vegetation encroachment and clearance analysis

The most mature application of wire modelling is **transmission vegetation management**. In North America, NERC Reliability Standard FAC-003 (FAC-003-4, superseded by FAC-003-5 effective 1 April 2024) requires transmission owners to maintain minimum vegetation clearance distances from conductors on lines at 200 kV and above (and on lower-voltage lines designated as elements of an Interconnection Reliability Operating Limit), with the clearance evaluated at the conductor's position under maximum designed sag and blow-out. The standard sets voltage-dependent minimum distances derived from flashover physics (the Table 2 minimum vegetation clearance distance for 345 kV at sea level is 4.3 ft, about 1.3 m, rising with voltage and with altitude; the tables in the standard govern, and utilities typically manage to a much larger working buffer) and requires annual inspection and a documented management program.

A lidar clearance analysis implements this as follows. Classify the corridor cloud into ground, vegetation, structures, and wire classes; fit each span as a catenary and record the conditions at acquisition; import conductors, towers, and attachment geometry into a line-design package such as PLS-CADD, which re-computes the catenary at the design states—maximum operating temperature, maximum blow-out, ice—from the conductor's mechanical and thermal properties. For each state, compute the 3D distance from the conductor to every vegetation point and flag those within the minimum clearance as encroachments, with location, tree height, and the state in which the violation occurs. Growth models project encroachments forward to plan the next cycle; "grow-in" (growth under the line) and "fall-in" (trees outside the right-of-way tall enough to strike the line if they fall) are analysed separately, the latter as a geometric test of tree height against distance to conductor.

The uncertainty budget is dominated not by the lidar but by the state. A 15 cm lidar vertical error is small next to a 2–3 m change in sag between survey and design temperature; a 0.5 m horizontal error is small next to a 3 m blow-out. If the conductor was assumed to be at ambient when it was actually 20 K warmer, the re-sag over-estimates the additional sag accordingly. Programs therefore fly in cool, calm, low-load conditions (early morning) so that the survey state is well defined, and log line current at the minute of overflight.

> **Worked example.** A 345 kV span of 320 m is surveyed at 06:30 with ambient 12 °C, wind 1 m s⁻¹, and line current at 15 % of rating; IEEE 738 puts the conductor at about 14 °C. The fitted catenary gives 9.2 m of mid-span sag and 11.4 m of vertical gap to a tree crown 20 m from mid-span. Re-sagging to the 100 °C design temperature adds about 2.7 m (Mathematics section), reducing the gap to roughly 8.7 m; design blow-out moves the conductor 2.5 m laterally, which barely changes the distance to a tree directly below but can halve it for a tree at the edge of the right-of-way. With a 3 m working clearance (well above the ~1.3 m regulatory minimum) and 0.5 m yr⁻¹ growth, the tree passes this cycle, and the report records its projected year of encroachment rather than merely "pass."

## Then & now

Until the 1990s a clearance survey was a ground job: a crew with a theodolite or total station measured attachment heights and a few mid-span points, a thermometer and the utility's load log supplied the state, and a sag–tension chart converted the measurement to the design condition. Coverage was sparse by necessity; vegetation was assessed on foot or by helicopter patrol. Aerial photogrammetry gave tower positions and ground profiles but not reliable conductor geometry.

Helicopter lidar changed the economics in the late 1990s and the practice after the 2003 blackout: every span of a line at decimetre accuracy in a day of flying. Automatic extraction followed—McLaughlin's covariance features (2006), Hough and RANSAC methods, Jwa and Sohn's catenary growing (2012)—and by Matikainen et al.'s 2016 review the pipeline of §33.2 was standard in commercial software. ASPRS formalised the wire classes in LAS 1.4 (2011), replacing project-specific codes that had made corridor data non-portable. On the aviation side, obstacle data moved from paper charts and national obstruction lists to ICAO's eTOD requirements (Annex 15 in the 2000s, PANS-AIM in 2018) with stated numerical quality; the FAA DOF is now updated on a 56-day cycle in step with the charting calendar.

The present frontier is dense, frequent, and automated: UAV corridor inspection at centimetre resolution, deep-learning classification of wires and insulators, line-mounted sensors feeding dynamic line rating and therefore real-time conductor temperature, and digital-twin models in which the lidar catenary is one observation of a continuously updated state. The physics has not changed; the state vector is now sometimes measured rather than assumed.

## Mathematics

**The catenary.** A uniform flexible cable of weight per unit length $w$ hanging under its own weight between two supports, with horizontal tension $H$, takes the shape

$$ y(x) = a \cosh\!\left(\frac{x}{a}\right), \qquad a = \frac{H}{w}, $$

with the origin below the lowest point. For a level span of length $S$ the **sag** is $D = a\,[\cosh(S/2a) - 1]$ and the arc length is $L = 2a \sinh(S/2a)$. When $D \ll S$ (the usual case, $D/S$ of 2–5 %), the series expansions give the **parabolic approximations**

$$ D \approx \frac{w S^2}{8 H}, \qquad L \approx S + \frac{8 D^2}{3 S}. $$

The parabola is accurate to better than 0.5 % in sag for $D/S < 0.05$; for long or slack spans (river crossings, cable cars) use the exact catenary. Fitting to lidar points proceeds in the vertical plane of the span: project the wire points onto the plane defined by the two attachment points, then solve for $a$ and the horizontal offset of the low point by nonlinear least squares, or, in the parabolic regime, by linear least squares on $y = c_0 + c_1 x + c_2 x^2$ with $H/w = 1/(2c_2)$.

**Thermal elongation.** A conductor of length $L$ and coefficient of linear expansion $\alpha$ changes length by

$$ \Delta L = \alpha\, L\, \Delta T . $$

For aluminium $\alpha \approx 23 \times 10^{-6}\ \text{K}^{-1}$; for steel about $11.5 \times 10^{-6}$; for a composite ACSR conductor the effective value lies between, around $19 \times 10^{-6}\ \text{K}^{-1}$ for common stranding ratios (the conductor data sheet gives the exact figure).

**From length to sag.** Inverting $L \approx S + 8D^2/(3S)$,

$$ D \approx \sqrt{\frac{3 S\,(L - S)}{8}}, \qquad \frac{dD}{dL} = \frac{3 S}{16 D}. $$

The sensitivity is large because $L - S$ is small: for $S$ = 320 m and $D$ = 9.2 m, $dD/dL = 960/147 \approx 6.5$, so every centimetre of extra conductor length adds 6.5 cm of sag.

**Elastic coupling.** As the conductor lengthens and sags, its tension falls, and the lower tension shortens it elastically by $\Delta L_e = \Delta H \cdot L / (E A)$ with $E A$ the conductor's axial stiffness. This partly offsets the thermal growth and is why a full sag–tension calculation iterates between the two. For a rough hand estimate the correction is 5–15 % of the thermal term.

> **Worked example.** Span $S$ = 320 m, surveyed sag $D_0$ = 9.2 m at conductor temperature 14 °C; design temperature 100 °C, $\Delta T$ = 86 K; $\alpha = 19.3 \times 10^{-6}\ \text{K}^{-1}$; $w$ = 15 N m⁻¹; $EA \approx 36$ MN (a Drake-class ACSR, approximate).
>
> Initial length: $L_0 = 320 + 8(9.2)^2/(3 \times 320) = 320 + 0.705 = 320.705$ m.
> Thermal growth: $\Delta L_t = 19.3 \times 10^{-6} \times 320.7 \times 86 = 0.532$ m.
> First-pass sag: $D_1 = \sqrt{3 \times 320 \times 1.237/8} = \sqrt{148.5} = 12.19$ m.
> Tension before and after (parabolic): $H_0 = wS^2/(8D_0) = 15 \times 102\,400/73.6 = 20\,870$ N; $H_1 = 15 \times 102\,400/97.5 = 15\,750$ N; $\Delta H = -5\,120$ N.
> Elastic shortening: $\Delta L_e = -5\,120 \times 320.7 / 36 \times 10^{6} = -0.046$ m.
> Net: $L - S = 0.705 + 0.532 - 0.046 = 1.191$ m; $D = \sqrt{960 \times 1.191/8} = \sqrt{142.9} = 11.95$ m.
> One more iteration moves the answer by a few centimetres. **Sag increases by about 2.7 m**, from 9.2 to roughly 11.9 m. The vertical clearance to anything beneath mid-span shrinks by that amount—an order of magnitude more than the lidar's vertical error.

**Wind displacement.** Drag per unit length $f = \tfrac{1}{2}\rho_a C_d d v^2$ with air density $\rho_a \approx 1.2\ \text{kg m}^{-3}$, drag coefficient $C_d \approx 1.0$ for a stranded conductor at moderate Reynolds number, diameter $d$, and wind speed $v$ normal to the span. The swing angle from vertical is $\phi = \arctan(f/w)$ and the mid-span lateral displacement is approximately $D \sin\phi$ (the sag swings as a rigid plane). With $d$ = 0.028 m, $v$ = 15 m s⁻¹, $w$ = 15 N m⁻¹: $f \approx 3.8$ N m⁻¹, $\phi \approx 14°$, displacement $\approx 12 \times 0.24 \approx 2.9$ m for a 12 m sag. Doubling the wind speed quadruples the force.

**IEEE 738 heat balance.** At steady state the conductor temperature $T_c$ satisfies $q_c(T_c) + q_r(T_c) = I^2 R(T_c) + q_s$, with convection depending on wind speed and direction and radiation on emissivity and $T_c^4 - T_a^4$; the standard supplies the correlations. A conductor at low current in still air and shade is within a few kelvin of ambient; at full rating in sun and light wind it may be 60–80 K above ambient.

## Validation & uncertainty

Validating a wire product means validating two different things: the geometry of what was captured, and the completeness of the capture. The second is the one usually missing.

**Geometric accuracy.** Lidar points on a conductor carry the usual trajectory, boresight, and ranging errors plus two specific terms. Beam divergence matters more because a thin target intercepts only part of the footprint; the height is unbiased for a horizontal wire, but the horizontal position is uncertain by up to half the footprint across the wire. Motion matters because the wire moved during the pass; the dispersion of points about the fitted catenary is an estimate of motion plus noise. Report per span: the RMS residual about the catenary (commonly 2–5 cm in calm conditions for well-captured transmission conductors; larger values signal wind or a bad fit), the point count, and the conductor temperature estimate with its inputs. Check attachment heights against surveyed insulator positions where the utility has them, and tower positions against the structure inventory.

**Completeness.** "Did we capture every wire?" cannot be answered from the data alone, because a missed wire leaves no hole. The reference is the utility's or aviation authority's asset inventory: every inventory span should have a modelled conductor, every modelled conductor should map to a span, and discrepancies must be resolved as survey misses, inventory errors, or real change. Report the fraction of spans fully modelled, partially modelled (with gap length), and absent, separately for guard wires and distribution under-build, which are thinner and missed more often. ICAO's eTOD specification additionally demands a stated **confidence level** (commonly 90 % for Area 2) that surveyed values lie within the stated accuracy, delivered through independent check surveys of a sample of obstacles.

**Temporal state.** A deliverable without ambient temperature, wind, line current, and derived conductor temperature cannot be transported to any other condition. Record their uncertainty too: a conductor temperature estimated with assumed emissivity and wind from a station 20 km away may be uncertain by ±10 K, which at the worked example's sensitivity of about 3 cm of sag per kelvin is ±0.3 m of sag.

**Epoch comparison.** Comparing two corridor surveys requires re-sagging both to the same state. The residual between the re-sagged catenaries, after lidar error, is creep plus re-tensioning plus modelling error; if it exceeds a few decimetres, suspect a state error before suspecting the line.

> **Uncertainty budget.** Vertical position of a transmission conductor at mid-span, as used in a clearance analysis for a 320 m span, representative magnitudes (1σ unless stated):
>
> | Component | Magnitude | Notes |
> |---|---|---|
> | Lidar point vertical error | 0.05–0.15 m | Trajectory, boresight, range; as for any lidar point |
> | Catenary fit residual | 0.02–0.05 m | Calm conditions, ≥ 50 points per span |
> | Wire motion during pass | 0.05–0.5 m | Light to moderate wind; vertical component |
> | Conductor temperature at survey | ±5–10 K → ±0.15–0.3 m | From IEEE 738 with assumed inputs |
> | Re-sag to design temperature | ±0.2–0.5 m | Conductor property uncertainties, creep state |
> | Blow-out at design wind (lateral) | 2–4 m, ±0.5 m | Enters 3D clearance, not vertical |
> | Creep since survey | 0.01–0.05 m yr⁻¹ | Conductor-dependent; resets at re-tensioning |
>
> The measurement terms sum to about 0.1–0.2 m; the state and transport terms to 0.3–0.6 m. The clearance decision is dominated by the physics, not by the survey.

**Wires as artefacts, tested.** For a DTM, overlay the known transmission network (OpenStreetMap power lines are a usable first source; the utility's inventory is better) and inspect slope and curvature maps along the corridors; a thin ridge or trough following a line is diagnostic. For a DSM, compute the fraction of corridor cells more than 5 m above ground outside tower footprints: near zero means the wires are absent, regular along-line gaps mean they are fragmentary, and either way the DSM must not be sold as an obstacle surface.

## Software

**Open source:** PDAL (`filters.covariancefeatures`, `filters.hag_nn`; Hough and catenary fitting need custom stages); CloudCompare (RANSAC shape detection, manual segmentation, cross-sections of spans); lidR in R (eigenvalue metrics via `point_metrics`); Open3D, scikit-learn, and `scipy.optimize` in Python for PCA, DBSCAN clustering, and least-squares catenary fits; QGIS for overlaying obstacle databases and corridor inventories. Caveat: no open tool is a turnkey corridor product; expect to write the span segmentation and catenary logic.

**Free but closed:** The FAA DOF and NGA DVOF data themselves are freely downloadable; viewers are generic GIS.

**Commercial:** PLS-CADD (Power Line Systems) is the de facto standard for line design, lidar import, re-sagging to design states, and clearance reporting; TerraScan (Terrasolid) has mature powerline classification and catenary-fitting tools and writes LAS classes 13–16; Global Mapper and LP360 offer powerline classification modules; several vendors (e.g., corridor-survey specialists) supply end-to-end services. Caveat: PLS-CADD's results depend on conductor property files and on the state inputs you supply; it will re-sag confidently from a wrong survey temperature.

## Standards & guides

- **ASPRS, LAS Specification 1.4 (R15, 2019).** Defines point classes 13 (wire – guard), 14 (wire – conductor), 15 (transmission tower), 16 (wire-structure connector) for point data record formats 6–10.
- **IEEE Std 738-2023** (superseding 738-2012), *Standard for Calculating the Current-Temperature Relationship of Bare Overhead Conductors.* The heat-balance model used to estimate conductor temperature from current and weather, and hence to re-sag a surveyed catenary.
- **NERC Reliability Standard FAC-003-4 / FAC-003-5,** *Transmission Vegetation Management.* (FAC-003-5 effective April 2024.) Minimum vegetation clearance distances evaluated at maximum sag and blow-out; annual inspection; the regulatory driver for corridor lidar in North America.
- **FAA Advisory Circular 150/5300-18B,** *General Guidance and Specifications for Submission of Aeronautical Surveys to NGS.* Obstacle survey requirements for U.S. airports (AGIS); together with the **Digital Obstacle File (DOF)** documentation (record structure, accuracy codes, 56-day cycle).
- **ICAO Annex 15,** *Aeronautical Information Services,* and **PANS-AIM (Doc 10066).** eTOD Areas 1–4 with numerical requirements for terrain and obstacle data.
- **RTCA DO-276C / EUROCAE ED-98C,** *User Requirements for Terrain and Obstacle Data.* Industry requirements underpinning the ICAO provisions (C revisions, 2015, current).
- **NGA Digital Vertical Obstruction File (DVOF)** specification. Military obstacle database format and content.
- **USGS Lidar Base Specification** (current revision). Requires wire classification where present at project density; bare-earth DEM excludes wires.

## Pitfalls

- **A clearance survey flown on a cold morning used to judge summer sag.** The surveyed catenary is a snapshot at one conductor temperature; the design condition can add metres of sag. Detect by checking whether the deliverable records ambient, wind, and current and whether the analysis re-sagged to design temperature; avoid by making the re-sag step explicit in the workflow.
- **Antennas and guy wires absent from a DSM used for obstacle analysis.** DSMs under-sample thin tall objects by nature. Detect by overlaying the obstacle database and listing database obstacles that do not appear as DSM spikes; avoid by never using a DSM alone for obstacle clearance.
- **Wires removed as noise, then the dataset used for drone route planning.** Isolated-point filters delete fragmentary wire returns. Detect by comparing the class-7/18 population along known corridors; avoid by classifying to 13–16 before any noise filter, or by flagging rather than deleting.
- **Wind turbines recorded at the blade position of the moment.** The DSM height is wherever the blades were; the obstacle height is the tip at top dead centre. Detect by comparing DSM maxima at turbine locations with hub height plus rotor radius; avoid by using the turbine register.
- **A thin ridge in the DTM along a transmission corridor.** Low conductor points adopted as ground near towers and ridges. Detect in slope maps along the network; avoid with corridor-aware ground filtering and a height-above-ground sanity check.
- **Wires above forest counted as canopy in an nDSM.** A wire 15 m above ground becomes a 15 m "tree" in the canopy height model. Detect by linear features in the CHM; avoid by removing classes 13–16 before gridding.
- **Comparing two corridor epochs without re-sagging either.** Metres of apparent conductor movement that is temperature. Detect by correlating the differences with the temperature difference; avoid by normalising to a common state.
- **Treating a utility GIS centreline as the conductor's horizontal position.** Centrelines are tower-to-tower straight lines; the conductor blows out metres to either side. Detect by comparing with lidar wire points; avoid by using the modelled conductor.
- **A flood wall or crash barrier lost to a 1 m grid or a ground filter.** Thin structures of hydraulic consequence vanish for the same reasons wires do. Detect by comparing DTM profiles across known structures; avoid with breaklines or a structure layer.

## Key takeaways

- Thin structures fail every DEM sampling assumption at once—small cross-section, specular reflection, non-reconstruction in matching, orientation-dependent radar return. Expect them to be missing.
- Dedicated corridor lidar with along-line geometry and high density captures conductors reliably; the pipeline is height threshold → PCA linearity → Hough/RANSAC → catenary fit → LAS classes 13–16 plus a vector span model.
- A wire has a state, not a position: conductor temperature changes sag by metres (about 2.7 m in the worked example), wind moves it metres sideways in seconds, ice adds metres over hours, creep lowers it decimetres over decades.
- Every wire deliverable needs ambient temperature, wind, line current, and derived conductor temperature at acquisition; without them the geometry cannot be transported to the design condition that clearance rules require.
- Obstacle databases are feature collections with per-record accuracy and currency; DSMs are fields with no completeness guarantee for thin objects. Use both, reconcile them, never substitute one for the other.
- Whether a DSM should contain wires depends on the use: yes for obstacles and drone routing (in a separable layer), no for hydrology and orthorectification. Document the inclusion rule.
- Unrecognised wires corrupt products as false-ground ridges, floating cells, spurious canopy, and SfM ghosts; flag rather than delete so the decision can be reviewed.
- In clearance analysis the uncertainty is dominated by the physical state and its transport, not by the lidar; fly cool, calm, and low-load, and log the conditions.

## References

- ASPRS (2019). *LAS Specification 1.4 – R15.* American Society for Photogrammetry and Remote Sensing.
- Federal Aviation Administration (2009, with changes). *Advisory Circular 150/5300-18B: General Guidance and Specifications for Submission of Aeronautical Surveys to NGS: Field Data Collection and Geographic Information System (GIS) Standards.* U.S. Department of Transportation.
- Guo, B., Li, Q., Huang, X., & Wang, C. (2016). An improved method for power-line reconstruction from point cloud data. *Remote Sensing*, 8(1):36. doi:10.3390/rs8010036
- IEEE (2023). *IEEE Std 738-2023: IEEE Standard for Calculating the Current-Temperature Relationship of Bare Overhead Conductors.* Institute of Electrical and Electronics Engineers. (Earlier edition: IEEE Std 738-2012.)
- International Civil Aviation Organization (2018). *Annex 15 to the Convention on International Civil Aviation: Aeronautical Information Services,* 16th ed.; and *Procedures for Air Navigation Services — Aeronautical Information Management (PANS-AIM), Doc 10066,* 1st ed.
- Jwa, Y., & Sohn, G. (2012). A piecewise catenary curve model growing for 3D power line reconstruction. *Photogrammetric Engineering & Remote Sensing*, 78(12):1227–1240.
- Jwa, Y., Sohn, G., & Kim, H. B. (2009). Automatic 3D powerline reconstruction using airborne lidar data. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, 38(3/W8):105–110.
- Kim, H. B., & Sohn, G. (2013). Point-based classification of power line corridor scene using random forests. *Photogrammetric Engineering & Remote Sensing*, 79(9):821–833.
- Matikainen, L., Lehtomäki, M., Ahokas, E., Hyyppä, J., Karjalainen, M., Jaakkola, A., Kukko, A., & Heinonen, T. (2016). Remote sensing methods for power line corridor surveys. *ISPRS Journal of Photogrammetry and Remote Sensing*, 119:10–31.
- McLaughlin, R. A. (2006). Extracting transmission lines from airborne LIDAR data. *IEEE Geoscience and Remote Sensing Letters*, 3(2):222–226.
- Melzer, T., & Briese, C. (2004). Extraction and modeling of power lines from ALS point clouds. *Proceedings of the 28th Workshop of the Austrian Association for Pattern Recognition (ÖAGM)*, Hagenberg, 47–54.
- North American Electric Reliability Corporation (2016). *Reliability Standard FAC-003-4: Transmission Vegetation Management.*
- RTCA (2015). *DO-276C: User Requirements for Terrain and Obstacle Data.* RTCA, Inc. (EUROCAE ED-98C equivalent.)
- Sohn, G., Jwa, Y., & Kim, H. B. (2012). Automatic powerline scene classification and reconstruction using airborne lidar data. *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, I-3:167–172.
- U.S.–Canada Power System Outage Task Force (2004). *Final Report on the August 14, 2003 Blackout in the United States and Canada: Causes and Recommendations.* U.S. Department of Energy and Natural Resources Canada.
- U.S. Geological Survey (2020, with later revisions). *Lidar Base Specification,* version 2.1 and successors. National Geospatial Program.
- Zhu, L., & Hyyppä, J. (2014). Fully-automated power line extraction from airborne laser scanning point clouds in forest areas. *Remote Sensing*, 6(11):11267–11282.

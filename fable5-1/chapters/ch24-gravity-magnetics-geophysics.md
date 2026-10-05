# Chapter 24 — Gravity, magnetics, and other geophysics as mapping aids

> **Part V — Sensors and platforms.** The last sensor chapter leaves the surface: potential fields and seismic, electrical, and electromagnetic methods do not image topography directly but constrain it, correct it, and extend it to places — under ice, under sediment, inside the crust — where ranging and parallax cannot go. It closes the loop opened in [Chapter 7](ch07-shape-of-the-earth.md), where gravity defined the geoid that gives orthometric heights their meaning.

**In this chapter.** Gravity is woven into elevation at every level: it defines the geoid and therefore $H = h - N$; its measurement requires terrain corrections computed from a DEM; its inversion predicts bathymetry under oceans and ice sheets where no sounder has been; and its long-wavelength behaviour (isostasy, flexure) tells you what topography is plausible. Magnetics supplies the declination your compass heading depends on and the seafloor age that sets regional ocean depth; seismics and electromagnetics map buried interfaces — bedrock, water table, permafrost base, sediment horizons — that are themselves surfaces worth gridding. You will be able to compute Bouguer and terrain corrections and recognise the DEM circularity in geoid modelling; apply Parker's formula and the admittance to predict topography from gravity and to test whether a DEM is consistent with gravity; obtain declination from WMM/IGRF for the correct epoch; use seafloor age as a depth prior and know where it fails; read sub-bottom and refraction sections as buried DEMs; and fuse geophysical constraints into void filling and plausibility checks without laundering an inference into a measurement.

## 24.1 Gravity

### 24.1.1 From gravity to orthometric heights

The orthometric height $H$ of a point is its distance above the geoid along the plumb line, and the geoid is an equipotential surface of Earth's gravity field. Ellipsoidal heights $h$ from GNSS are converted by $H = h - N$, where the **geoid undulation** $N$ comes from a gravity-field model — a global spherical-harmonic model (EGM2008 to degree 2190, roughly 9 km half-wavelength; XGM2019e; the GRACE/GOCE-based satellite-only models to degree 200–300) refined regionally by terrestrial, airborne, and marine gravity in a national geoid model (GEOID18 and, from the modernised NSRS, NAPGD2022 in the United States; the Canadian CGG2013a; AUSGeoid2020; OSGM15 in Britain). [Chapter 7](ch07-shape-of-the-earth.md) and [Chapter 9](ch09-vertical-datums.md) describe the heights; here the question is how the gravity data and the DEM interact.

Gravity observed on the ground must be **reduced** to isolate the signal of the geoid. The **free-air correction** accounts for the observation height above the reference ellipsoid (0.3086 mGal m$^{-1}$); the **Bouguer correction** removes the attraction of the rock slab between the station and the datum ($2\pi G\rho\,h = 0.1119$ mGal m$^{-1}$ for $\rho = 2{,}670$ kg m$^{-3}$); and the **terrain correction** accounts for the fact that the surface is not a flat slab — hills above the station pull upward and valleys below it are missing mass, both of which make the slab correction too large, so the terrain correction is always positive. Hammer (1939) tabulated it for concentric zones read from a topographic map by hand; today it is computed from a DEM by summing the attraction of **prisms** (Nagy 1966; Nagy, Papp & Benedek 2000 for the closed-form prism and its singularities) or, more efficiently, by FFT methods (Forsberg 1985) out to 167 km (Hayford–Bowie zone O) with inner-zone refinement from a fine DEM. In mountainous terrain the terrain correction reaches tens of milligals and its error, dominated by the DEM's error and resolution within the first kilometre, can be milligals; since 1 mGal of systematic gravity error over 100 km corresponds to roughly 1–2 cm of geoid, the DEM quality matters at the level modern geoid models aim for (1–2 cm). The **residual terrain model (RTM)** technique (Forsberg 1984) uses the high-frequency part of the DEM — the difference between the detailed DEM and a smoothed reference surface — to compute the short-wavelength gravity and geoid signal that global models omit, which is what GGMplus (Hirt et al. 2013) did to extend EGM2008 to about 200 m resolution worldwide using SRTM.

### 24.1.2 The circularity

Here is the loop. A DEM is used to compute terrain corrections and RTM effects; these feed a geoid model; the geoid converts GNSS ellipsoidal heights to orthometric heights; those orthometric heights become the control and the content of the next DEM; which is used to compute the next geoid. For most purposes the loop is benign because the DEM's influence on the geoid is through its integrated mass at wavelengths of kilometres, while the DEM's own errors are mostly at shorter wavelengths and average out. It becomes malignant when (a) the DEM has a systematic height bias over a large area (forest canopy in SRTM-derived DEMs — [Chapter 21](ch21-radar-sar-insar.md)), which the geoid computation reads as excess mass; (b) a density assumed in the terrain correction is wrong regionally (ice sheets, sedimentary basins, volcanic islands), so that the DEM is "right" but the mass model is not; or (c) a user validates a new lidar DTM against GNSS-on-benchmark orthometric heights that were themselves computed with a geoid built from the previous DEM, and reports agreement as independent confirmation. Track which DEM went into which geoid (national geoid reports state this), prefer validation with ellipsoidal heights where possible, and treat sub-decimetre agreement between a DEM and a geoid-dependent height as partly inherited.

### 24.1.3 Airborne and satellite gravity

Surface gravimetry is sparse and inconsistent across borders and absent over oceans, ice, and jungle. **Satellite gravimetry** — CHAMP (2000), GRACE (2002–2017), GOCE (2009–2013), GRACE-FO (2018–) — determines the long and medium wavelengths (down to roughly 80–100 km) homogeneously, and GRACE's time-variable field tracks ice-mass loss and groundwater depletion ([Chapter 38](ch38-plate-motion-and-vlm.md)). **Airborne gravimetry** fills the gap between satellite and surface: the US **GRAV-D** program (2007–) flew the entire United States and territories at about 6 km altitude and 10 km line spacing with the explicit goal of a 1–2 cm geoid for the 2022 modernised vertical datum, and similar campaigns underlie Greenland and Antarctic gravity grids. Airborne gravity requires sub-centimetre-per-second-squared separation of the aircraft's accelerations from gravity, which depends on kinematic GNSS of the aircraft and, again, on a DEM-free free-air reduction to flight altitude. Over ice sheets and polar margins the same airborne gravity (Operation IceBridge, OMG, ICECAP) is inverted for **sub-ice bathymetry**: where radar sounding fails (warm ice, water-filled troughs, fjords with floating ice), the gravity low over a deep trough constrains its depth to perhaps ± 50–100 m given assumptions about rock density and sediment, and this is how the cavities under Thwaites and Totten and the fjords of Greenland entered BedMachine (Tinto & Bell 2011; Greenbaum et al. 2015; An et al. 2019). Over oceans, the altimeter-derived gravity and its inversion to bathymetry were covered in [Chapter 21](ch21-radar-sar-insar.md) and [Chapter 23](ch23-satellite-derived-bathymetry.md).

### 24.1.4 Isostasy, flexure, and what topography is plausible

Mountains do not sit on a rigid Earth; they are supported by buoyancy (Airy and Pratt isostasy) and by the strength of the lithosphere (flexure). The practical consequence for DEM work is that gravity and topography are correlated in a wavelength-dependent way described by the **admittance** $Z(k)$ — the ratio of gravity to topography spectra — and the **coherence** $\gamma^2(k)$ between them (Dorman & Lewis 1970; Forsyth 1985; Watts 2001). At short wavelengths (< 50 km) topography is uncompensated and gravity follows it with the Bouguer-slab admittance; at long wavelengths (> 300 km) topography is compensated and the free-air gravity is nearly zero; the transition wavelength depends on the **effective elastic thickness** $T_e$ of the lithosphere (a few kilometres under young oceanic crust and hot continental regions, 50–100 km under old cratons). Two uses follow. First, a DEM can be checked against gravity: compute the predicted gravity from the DEM through the admittance and compare with observed gravity; residuals that correlate with a DEM's tiles, seams, or land-cover classes indicate DEM error rather than geology. Second, a bathymetric prediction from gravity needs the admittance *with* its compensation, which is why Smith & Sandwell band-pass to 15–160 km (above the flexural roll-off) and calibrate the scale factor regionally.

<!-- figure: Figure 24.1 — Gravity–topography admittance versus wavelength for Te = 5, 20, and 60 km, showing the short-wavelength Bouguer plateau, the flexural roll-off, and the long-wavelength isostatic zero; the Smith–Sandwell 15–160 km band is shaded. -->

## 24.2 Magnetics

### 24.2.1 Declination

Every survey heading taken from a magnetic compass — on a boat, a drone, a handheld instrument, or a legacy survey record — must be corrected for **declination**, the angle between magnetic and true north, which ranges from near zero to tens of degrees and changes by up to 0.2–0.5° per year in places (secular variation). The reference models are the **International Geomagnetic Reference Field (IGRF)**, revised every five years by IAGA (IGRF-13, Alken et al. 2021; IGRF-14 released November 2024, valid to 2030), and the **World Magnetic Model (WMM)**, produced by NOAA NCEI and the British Geological Survey for the US and UK defence departments (WMM2020; WMM2025 released December 2024). Both are spherical-harmonic models of the core field with linear secular variation over their five-year window; both are evaluated for a specific date — a declination from the wrong epoch is an error of degrees in some regions, and historical survey headings must be corrected with the declination of *their* date, which IGRF provides back to 1900 (`GeographicLib MagneticField` evaluates IGRF and WMM for any date). Neither model includes the crustal field, which near ore bodies, volcanic rocks, and steel structures can deflect a compass by several degrees; nor the external field during magnetic storms. For DEM work, the error enters as a rotation of any dead-reckoned or compass-oriented track — a 2° heading error over 1 km is 35 m of position error at the end of the line.

### 24.2.2 Marine magnetic anomalies, seafloor age, and depth

The stripes of alternating magnetic polarity recorded in oceanic crust, explained by Vine & Matthews (1963) and independently by Morley (the Vine–Matthews–Morley hypothesis), give the age of the seafloor when correlated with the geomagnetic polarity timescale (Cande & Kent 1992 ⟨H⟩, 1995; Ogg 2020 for the current scale). Global **seafloor age grids** (Müller et al. 2008, 2019; the latter at 0.1° with uncertainty estimates) combine ship-track magnetic picks with plate reconstructions. Age is a depth predictor through thermal subsidence — the Parsons & Sclater (1977) relation of [Chapter 23](ch23-satellite-derived-bathymetry.md) — and the age grid is what supplies the long-wavelength depth where neither ship soundings nor gravity constrain it in SRTM15+ and GEBCO. The prior fails where the lithosphere is not simply cooling: near hotspot swells (Hawaii, Iceland, the Cape Verdes), on oceanic plateaus and aseismic ridges, in back-arc basins, near continental margins where sediment loading dominates, and in the oldest crust, where the relation flattens and its calibration is debated (Stein & Stein 1992). Treat a depth-from-age value as a regional expectation with 300–500 m scatter, and as nothing at all within a few hundred kilometres of a hotspot or margin.

### 24.2.3 Magnetometer surveys and EMAG2

Towed or drone-borne magnetometers find ferrous objects: pipelines, cables, unexploded ordnance (UXO), wrecks, and buried infrastructure, which matter for DEM work as **features to be flagged** — a wreck on a multibeam surface and the same wreck's magnetic signature should coincide, and a magnetic anomaly without a bathymetric expression is a buried object that a dredging or construction DEM must respect ([Chapter 65](ch65-mining-landfills-earthworks.md)). Aeromagnetic surveys map crustal structure, and the global compilation **EMAG2v3** (Meyer, Saltus & Chulliat 2017; 2 arc-minute grid at 4 km altitude) is the magnetic analogue of the marine gravity grid, used for tectonic interpretation and as a secondary constraint on seafloor age. Neither gives depth directly; both give context.

## 24.3 Seismics: buried surfaces

Seismic methods image interfaces of acoustic-impedance contrast. Marine **sub-bottom profilers** (chirp, boomer, sparker — [Chapter 20](ch20-sonar.md)) and **reflection seismics** produce sections in two-way travel time; each continuous reflector — the seabed, the base of recent sediment, a buried channel, bedrock — can be picked along every line and gridded into a **buried DEM**, a surface with its own elevation, slope, and error, after conversion from time to depth with a velocity model whose uncertainty (typically 5–10 % in unconsolidated sediment) is a direct depth uncertainty. Offshore wind, cable, and pipeline projects routinely deliver "depth to bedrock" and "thickness of unit X" grids; archaeological and palaeolandscape studies grid buried river valleys from the last glacial lowstand (the Doggerland surveys of the North Sea are DEMs of a landscape under 30 m of water and tens of metres of sediment). On land, **refraction seismics** gives depth to bedrock or to the water table from the travel-time curve's crossover distance, and **passive seismic** methods (HVSR, ambient-noise) estimate sediment thickness cheaply at a point. At crustal scale, **receiver functions** (Langston 1979; the H-κ stacking of Zhu & Kanamori 2000) give the depth to the Mohorovičić discontinuity under each seismometer, and compilations (CRUST1.0, Laske et al. 2013; regional Moho maps) are gridded Moho "DEMs" with uncertainties of 2–5 km — surfaces that enter flexural and isostatic modelling of the topography above them.

All these buried surfaces share the characteristics of radio-echo-sounded ice beds ([Chapter 21](ch21-radar-sar-insar.md)): sparse lines, interpolation between them, a depth conversion that depends on an assumed velocity, and a picking step whose consistency between lines and operators limits the product. They should be delivered with the line coverage, the velocity model, and a distance-to-nearest-data layer, exactly as a bathymetric grid should carry its source and density.

## 24.4 Electrical, electromagnetic, and GPR

**Electrical resistivity tomography (ERT)** and **electromagnetic (EM) methods** — frequency- and time-domain, ground and airborne — map subsurface conductivity, which contrasts strongly between dry and saturated sediment, between sediment and crystalline bedrock, between fresh and saline groundwater, and between frozen and unfrozen ground. **Airborne EM** (SkyTEM, VTEM, RESOLVE) flown at 30–60 m altitude maps the top 100–300 m along lines 100–250 m apart; Denmark mapped most of its groundwater aquifers this way, and the products include **depth-to-bedrock**, **water-table**, and **permafrost-base** grids — Earth layers as DEMs, each with a horizontal resolution of the line spacing and a vertical uncertainty from the inversion's non-uniqueness (layered-earth inversions trade thickness against conductivity; depth errors of 10–20 % are typical). **Ground-penetrating radar** ([Chapter 21](ch21-radar-sar-insar.md)) adds the metre-scale detail: snow depth over a glacier, the active-layer base in permafrost, the water table in sand, pavement layers, and archaeological features, each a surface at a depth set by the two-way time and an assumed velocity.

The connection to surface DEMs is twofold. A **depth-to-interface** grid is meaningless without the surface DEM from which depth is measured — "bedrock at 12 m depth" is an elevation only once you know the ground elevation at that point and its epoch — and the surface DEM's error propagates straight into the buried surface's elevation. Conversely, the surface DEM is often the *only* spatially dense constraint, and buried-surface interpolation methods use surface morphology (valley axes, terrace edges) as covariates. Documenting which surface DEM was used, with its datum and date, is part of delivering a subsurface model.

<!-- figure: Figure 24.2 — Stacked "Earth layers as DEMs": land surface (lidar), water table (AEM), base of permafrost (AEM/borehole), top of bedrock (seismic refraction and AEM), Moho (receiver functions), each with its characteristic horizontal resolution and vertical uncertainty annotated. -->

## 24.5 Fusing geophysics with topography

Three modes of fusion are legitimate; a fourth is not.

**Constraint in void filling.** Where a bathymetric or sub-ice DEM has no direct measurement, gravity (through the admittance), seafloor age (through depth–age), and mass conservation (through ice flux) supply a physically motivated interpolant that is better than kriging across a gap, and the resulting cells are labelled as such (GEBCO's TID; BedMachine's source mask). The uncertainty of these cells is the uncertainty of the physics plus the uncertainty of the regional calibration, and it is large: hundreds of metres for gravity-predicted ocean depth, tens to hundreds for mass-conservation ice beds, 300–500 m for depth-from-age.

**Joint inversion.** Where two or more geophysical datasets constrain the same interface — gravity and radar sounding for an ice bed, gravity and seismic refraction for a sediment basin, EM and borehole logs for bedrock — a joint inversion with a shared geometry and separate physics (or structural coupling such as cross-gradient constraints) gives a better interface than either alone, and its posterior covariance is the honest uncertainty. Fatiando a Terra's Harmonica and SimPEG are the open frameworks; the result is still a model, and its label should say so.

**Plausibility checks.** A DEM can be tested for consistency with gravity: forward-model the gravity from the DEM (Parker's formula, or prism summation) and compare with observed free-air or Bouguer gravity; large residuals at short wavelengths point to DEM error (tile seams, void fill, penetration bias over forest, a misplaced coastline), while long-wavelength residuals are geology. Likewise, a bathymetric compilation whose depth–age residuals show a stripe along a cruise track has a datum or sound-speed error on that cruise ([Chapter 54](ch54-evaluating-others-data.md)). These are cheap tests and underused.

**What not to do** is to blend a predicted surface with measured surfaces so that the distinction is lost, or to report the accuracy of the measured cells as the accuracy of the grid. [Chapter 48](ch48-compositing.md) gives the rules; the one that matters here is that geophysical inference is always a *source type*, carried as an attribute, never silently merged.

> **Case file.** The Southern Ocean south of Australia contains seafloor cells in global grids whose only constraint was gravity and depth–age. When the search for Malaysia Airlines flight MH370 began in 2014, the pre-search bathymetry in the priority area was predominantly satellite-predicted, with reported local errors of hundreds of metres and features such as a 1,400 m-high seamount and 1,000 m-deep fault valleys absent or mislocated. The Geoscience Australia bathymetric survey (2014–2017) mapped about 279,000 km² with multibeam before the sonar search could proceed, and the differences between the predicted and measured grids were published as a direct illustration of what "predicted bathymetry" means (Picard, Brooke & Coffin 2017; feature dimensions as reported there (verify)).

## Then & now

- **1735–1749.** Bouguer's measurements in Peru (the Chimborazo plumb-line deflection) found the Andes attract less than their visible mass implies — the first hint of isostasy.
- **1849.** Stokes's formula relates gravity anomalies to the geoid.
- **1855.** Pratt and Airy publish rival isostatic models to explain the Himalayan deflection anomaly measured by the Great Trigonometrical Survey.
- **1939.** Hammer's terrain-correction zone chart becomes standard practice for the next half century.
- **1963.** Vine & Matthews explain marine magnetic stripes by seafloor spreading; Morley's parallel paper is rejected.
- **1966.** Nagy publishes the right rectangular prism gravity formula, the basis of DEM-based terrain corrections.
- **1973.** Parker's FFT forward formula makes gravity computation from gridded topography fast.
- **1977 ⟨H⟩.** Parsons & Sclater depth–age relation.
- **1992 ⟨H⟩.** Cande & Kent geomagnetic polarity timescale; 1995 revision.
- **2000–2013.** CHAMP, GRACE (2002), GOCE (2009) transform the long-wavelength gravity field; EGM2008 (2008).
- **2007.** NGS begins GRAV-D airborne gravity for the modernised US vertical datum; Müller et al. (2008) global age grid.
- **2013–2017.** GGMplus (2013); EMAG2v3 (2017); BedMachine Greenland (2017) uses gravity-derived fjord bathymetry; MH370 search survey (2014–2017).
- **2020–2026.** WMM2020 and WMM2025; IGRF-13 (2020) and IGRF-14 (2024); NAPGD2022 and the modernised NSRS released by NGS as beta products in 2026, with NAVD 88 still official pending adoption (verify current status).

The through-line is that gravity has moved from the explanation of a surveying anomaly to the definition of the height system itself, and the DEM has moved from a map read by hand for terrain corrections to a dataset whose errors propagate into the geoid.

## Mathematics

**Free-air and Bouguer.** Free-air anomaly: $\Delta g_{FA} = g_{\mathrm{obs}} - \gamma_0 + 0.3086\,h$ (mGal, $h$ in m). Simple Bouguer anomaly: $\Delta g_{B} = \Delta g_{FA} - 2\pi G\rho\,h = \Delta g_{FA} - 0.04193\,\rho\,h$ with $\rho$ in g cm$^{-3}$ (0.1119 mGal m$^{-1}$ at 2.67). Complete Bouguer: add the terrain correction $\delta g_T \ge 0$ and, for distant zones, the curvature (Bullard B) correction (LaFehr 1991; Hinze et al. 2005 for modern standards).

**Nagy prism.** The vertical attraction at the origin of a right rectangular prism of density $\rho$ occupying $[x_1, x_2] \times [y_1, y_2] \times [z_1, z_2]$ is

$$g_z = G\rho \,\Big|\Big|\Big|\; x\ln(y + r) + y\ln(x + r) - z\arctan\frac{xy}{zr} \;\Big|_{x_1}^{x_2}\Big|_{y_1}^{y_2}\Big|_{z_1}^{z_2},$$

with $r = \sqrt{x^2 + y^2 + z^2}$ (Nagy 1966; Nagy, Papp & Benedek 2000 give the singular cases). A terrain correction sums this over DEM cells (as prisms from the station height to the cell's surface height) within the inner zone, and uses faster approximations (line masses, FFT) beyond a few kilometres.

**Parker's forward formula.** For a density interface $h(\mathbf{x})$ (positive up) at mean depth $d$ below the observation plane,

$$\mathcal{F}\{\Delta g\}(\mathbf{k}) = 2\pi G\Delta\rho\, e^{-|\mathbf{k}| d}\sum_{n=1}^{\infty}\frac{|\mathbf{k}|^{n-1}}{n!}\,\mathcal{F}\{h^n\}(\mathbf{k}).$$

Truncating at $n = 1$ gives the linear admittance $Z(k) = 2\pi G\Delta\rho\,e^{-kd}$; the series converges when $|h|_{\max} < d$, and in practice three to five terms suffice for ocean bathymetry.

**Flexural isostasy.** A load $\rho_c g h$ on an elastic plate of flexural rigidity $D = E T_e^3/[12(1-\nu^2)]$ over a fluid mantle of density $\rho_m$ deflects the Moho by $w(\mathbf{k}) = -\Phi_e(k)\,\dfrac{\rho_c}{\rho_m - \rho_c}\,h(\mathbf{k})$ with $\Phi_e(k) = \big[1 + Dk^4/((\rho_m - \rho_c)g)\big]^{-1}$. The free-air admittance for surface loading is then

$$Z(k) = 2\pi G\rho_c\,e^{-kd}\Big(1 - \Phi_e(k)\,e^{-k t_c}\Big),$$

where $t_c$ is the crustal thickness; it tends to the Bouguer value at short wavelengths and to zero at long wavelengths. **Coherence** between Bouguer gravity and topography, $\gamma^2(k) = |\langle G^* H\rangle|^2 / (\langle G^* G\rangle\langle H^* H\rangle)$, distinguishes surface from subsurface loading and is used to estimate $T_e$ (Forsyth 1985).

**Geoid from gravity.** Stokes: $N = \dfrac{R}{4\pi\gamma}\iint_\sigma \Delta g\, S(\psi)\, d\sigma$, with the Stokes kernel $S(\psi)$; the terrain contributes through $\Delta g$ (the reduction) and through the **indirect effect** of moving masses in the reduction, both of which depend on the DEM. The RTM geoid effect at a point from the residual topography $h - h_{\mathrm{ref}}$ is of order $2\pi G\rho\,(h - h_{\mathrm{ref}})^2/\gamma$ for the local term — centimetres for 100 m residual relief.

> **Worked example.** *Terrain-correction error from DEM error.* A gravity station sits in a valley; within the 500 m inner zone the mean terrain stands 150 m above the station, with density 2,670 kg m$^{-3}$. Approximating the inner zone as a ring of height $h$, inner radius $r_1 = 20$ m and outer radius $r_2 = 500$ m, the terrain correction is $\delta g_T = 2\pi G\rho\,\big[(r_2 - r_1) - \sqrt{r_2^2 + h^2} + \sqrt{r_1^2 + h^2}\big]$ $= 0.1119\;\mathrm{mGal\,m^{-1}} \times [480 - 522.0 + 151.3] = 0.1119 \times 109.3 = 12.2$ mGal. If the DEM overstates the ring height by 10 m (a forest canopy in an SRTM-derived DEM), $h = 160$ m gives $[480 - 524.98 + 161.25] = 116.3$ m and $\delta g_T = 13.0$ mGal: a 0.8 mGal error from a 10 m canopy bias — the size of the total error budget of a modern gravity station. Over a forested region such a correlated error of ~1 mGal at 10–50 km wavelength maps into roughly 1 cm of geoid, which is at the target accuracy of modern national geoids.

> **Try it.** Forward-model the gravity of a DEM with Harmonica (Fatiando a Terra) prisms and compare with a gravity grid to find DEM-correlated residuals. Expected outcome: short-wavelength residuals of a few mGal that follow DEM tile boundaries or forest/non-forest edges indicate DEM problems; smooth residuals are geology.
>
> ```python
> import numpy as np, xarray as xr, harmonica as hm, verde as vd
>
> dem = xr.open_dataarray("dem_utm_90m.nc")            # metres, projected grid
> east, north = np.meshgrid(dem.easting.values, dem.northing.values)
> # Prisms from sea level (0) up to the DEM surface, density 2670 kg/m3 (negative for below-zero cells)
> prisms = hm.prism_layer((dem.easting.values, dem.northing.values),
>                         surface=dem.values, reference=0.0,
>                         properties={"density": np.where(dem.values >= 0, 2670.0, -1640.0)})
> # Observation points: on a plane 100 m above the highest terrain, same grid, 1 km spacing
> coords = vd.grid_coordinates(region=vd.get_region((east, north)), spacing=1000,
>                              extra_coords=float(dem.max()) + 100)
> g_dem = prisms.prism_layer.gravity(coords, field="g_z")        # mGal
> g_obs = xr.open_dataarray("free_air_1km_upward_continued.nc").values
> resid = g_obs - g_dem
> print("residual RMS (mGal):", np.sqrt(np.nanmean((resid - np.nanmean(resid))**2)))
> # Save the residual grid; inspect in QGIS against DEM tile edges and a forest mask.
> vd.make_xarray_grid(coords, resid, data_names="resid").to_netcdf("gravity_residual.nc")
> ```

## Validation & uncertainty

Geophysical surfaces and corrections carry three kinds of uncertainty that must be reported separately.

**Measurement and reduction uncertainty.** Modern relative gravimeters measure to 0.01–0.05 mGal; the reduction (free-air, Bouguer, terrain) adds 0.1–1 mGal depending on the DEM and the density assumption, and the station elevation itself (0.3 mGal per metre of height error in the free-air term) is often the dominant term for historical stations positioned from maps. Report the DEM used for terrain correction (name, resolution, version) and the density; where the density is assumed, state it, and where it is known to differ (ice: 917 kg m$^{-3}$; water; sediments 1,800–2,200), apply the appropriate value.

**Inversion uncertainty.** Gravity inversion for an interface is non-unique: a shallow low-contrast body and a deep high-contrast body produce similar anomalies. Report the assumed density contrast and the sensitivity of the depth to it ($\partial d/\partial\Delta\rho$), the regularisation used, and — where the inversion was calibrated against direct measurements (ship soundings, boreholes, radar picks) — the residuals at withheld calibration points by distance from the nearest constraint. For gravity-derived sub-ice or seafloor depths, typical uncertainties are 50–100 m near constraints and several hundred metres far from them; a published grid without such a layer should be assumed to be at the worse end.

**Model-epoch and reference uncertainty.** Magnetic declination must be evaluated for the observation date with the model valid for that date, and the model's own uncertainty stated (the WMM technical report quotes a global RMS declination error of a few tenths of a degree, larger near the poles (verify)). Geoid models have a stated accuracy (GEOID18: about 1–2 cm relative over short distances, several centimetres absolute (verify)) and an epoch; using a geoid of one realisation with GNSS heights in another frame introduces decimetre errors ([Chapter 9](ch09-vertical-datums.md)).

**Tests.** (1) Forward-model gravity from the DEM and compare with observed gravity (Try it); residual maps that show DEM structure are DEM problems. (2) For any gravity- or age-predicted bathymetry, withhold whole cruises and report RMS by distance to constraint. (3) For buried-surface grids, cross-plot the picked depth at line intersections (mis-ties) and report the RMS mis-tie; a mis-tie larger than the claimed vertical accuracy means the claim is wrong. (4) For declination, check the model value against a known true bearing (a surveyed baseline) once per campaign. (5) For any product that passed through a geoid, record the geoid model and the DEM it used, and avoid validating that DEM with heights that depend on it.

> **Uncertainty budget.** Depth to a buried interface from gravity inversion, far from direct constraints (illustrative, 1σ).
>
> | Component | Magnitude | Comment |
> |---|---|---|
> | Gravity observation + reduction | 1–2 mGal | includes DEM-based terrain correction |
> | Regional field removal | 2–5 mGal | long-wavelength ambiguity |
> | Density contrast assumption (± 100 kg m⁻³ on 1,700) | ≈ 6 % of relief | scales interface amplitude |
> | Non-uniqueness / regularisation | 50–200 m | depends on depth and wavelength |
> | Upward-continuation loss (short wavelengths) | features < 2–3 × depth unresolved | resolution, not error |
> | Combined, 10–20 km from nearest sounding | ≈ 100–300 m | consistent with GEBCO/SRTM15+ assessments |

## Software

**Open source.** **GMT** (`grdfft`, `gravfft`, `grdgravmag3d`, `gravprisms`): spectral admittance/coherence, Parker forward and inverse modelling, prism gravity from grids. **Fatiando a Terra — Harmonica, Verde, Boule**: prism and tesseroid forward modelling, equivalent sources, gridding, and normal gravity in Python. **SimPEG**: joint and regularised inversion of gravity, magnetics, EM, and resistivity. **pyshtools** (Wieczorek & Meschede 2018): spherical-harmonic gravity and topography analysis, localized admittance on planets and Earth. **GeographicLib `MagneticField`** and the **`pyIGRF` / `wmm2020` / `ppigrf` packages**: declination for any date. **ICGEM** calculation service (GFZ; web): geoid and gravity functionals from any global model. **ObsPy** and **RfPy**: receiver-function processing. **ResIPy**, **pyGIMLi**: ERT/EM inversion.

**Free but closed.** **NGS GEOID18 / xGEOID / NAPGD2022 tools** and **GRAV-D data**; **NOAA NCEI WMM calculators**; **CRUST1.0**.

**Commercial.** **Seequent Oasis montaj**: the industry standard for potential-field processing, terrain correction, and inversion (VOXI); caveat — proprietary formats. **Petrel** (SLB) and **Kingdom** (S&P Global): seismic interpretation and horizon gridding. **Aarhus Workbench**: airborne EM inversion and hydrogeophysical layer models.

## Standards & guides

- **Hinze et al. (2005), "New standards for reducing gravity data: The North American gravity database"**, *Geophysics* 70(4): the modern reduction conventions (ellipsoidal heights, Bullard B, atmospheric correction).
- **IAG / IGFS gravity standards** and the **International Gravity Reference System (IGRS 2020)**: absolute gravity reference.
- **NGS GRAV-D Project Plan and Technical Reports** (2007–): airborne gravity specifications for the modernised NSRS.
- **IAGA IGRF release notes** (IGRF-13, 2020; IGRF-14, November 2024) and the **WMM Technical Report** (WMM2025, NOAA NCEI/BGS): model validity, epoch, and error statements.
- **GEBCO Cook Book (IHO-IOC B-11)**: chapters on gravity-predicted bathymetry and source identification.
- **SEG / EAGE recommended practices** for seismic horizon picking and time–depth conversion (project-specific (verify)).
- **ASTM D6429 (standard guide for selecting surface geophysical methods)** and **ASTM D6431 / D6432** (resistivity, GPR): procedures for near-surface surveys.

## Pitfalls

- **Correcting gravity with a DEM, building a geoid from it, and validating the same DEM with geoid-dependent heights.** The agreement is partly inherited. Record the DEM in the geoid lineage and validate with ellipsoidal heights where possible.
- **Assuming the depth–age relation near hotspots, plateaus, back-arc basins, and margins.** Residuals of a kilometre are normal there. Mask these regions or inflate the prior's uncertainty.
- **Declination from the wrong epoch or the wrong model.** Secular variation moves declination by degrees per decade in places. Evaluate IGRF/WMM at the observation date; for historical headings use IGRF for that year.
- **Terrain corrections with a canopy-biased DEM.** Forest height becomes rock mass; the error is correlated over tens of kilometres and enters the geoid. Use a DTM, or correct the DSM, for terrain corrections.
- **Wrong density in the terrain correction over ice, water, or sediment.** A 2,670 kg m$^{-3}$ slab over an ice sheet is three times too heavy. Use the material's density and say so.
- **Treating a gravity-predicted interface as measured.** Non-uniqueness and the density assumption give hundreds of metres of uncertainty. Label predicted cells and report residuals at withheld constraints.
- **Delivering a buried-surface grid without the surface DEM it is referenced to.** "Depth below ground" has no elevation until the ground is specified, with its datum and epoch.
- **Ignoring seismic velocity uncertainty in time-to-depth conversion.** A 10 % velocity error is a 10 % depth error. Report the velocity model and its basis (boreholes, refraction, stacking velocities).
- **Blending predicted and measured depths into one grid without a source attribute.** Users cannot tell them apart. Carry a TID or equivalent in every compilation.
- **Reading magnetic compasses near steel, ore, or basalt as if the core-field model applied.** Crustal anomalies of several degrees are common. Check against a true bearing on site.
- **Forgetting that the free-air term makes station height the dominant gravity error.** A 1 m height error is 0.3 mGal. Position gravity stations with GNSS or levelling, not from a map.

## Key takeaways

- Gravity defines the geoid, so every orthometric height is a gravity product; the DEM used for terrain corrections is part of that product's lineage.
- Terrain and RTM corrections need a DTM of the right density; canopy bias and ice density errors propagate into the geoid at the centimetre level over regional scales.
- Parker's formula and the flexural admittance connect topography to gravity in a wavelength-dependent way; use them to predict bathymetry where there is nothing better and to test DEMs for consistency.
- Gravity-predicted depths carry uncertainties of hundreds of metres and 6–12 km resolution; they are a source type, carried as an attribute, never merged silently.
- Declination comes from WMM/IGRF evaluated at the observation date; the wrong epoch is an error of degrees.
- Seafloor age is a regional depth prior with 300–500 m scatter that fails near hotspots and margins.
- Seismic, EM, and GPR interfaces are buried DEMs with sparse-line interpolation, velocity-dependent depths, and a dependence on the surface DEM they are measured from — report all three.
- Forward-modelling gravity from a DEM and plotting the residual is a cheap, underused plausibility check for DEM seams, void fill, and systematic bias.

## References

- Alken, P., Thébault, E., Beggan, C. D., Amit, H., Aubert, J., Baerenzung, J., et al. (2021). International Geomagnetic Reference Field: the thirteenth generation. *Earth, Planets and Space*, 73:49.
- An, L., Rignot, E., Chauche, N., Holland, D. M., Holland, D., Jakobsson, M., et al. (2019). Bathymetry of southeast Greenland from Oceans Melting Greenland (OMG) data. *Geophysical Research Letters*, 46(20):11197–11205.
- Cande, S. C., & Kent, D. V. (1992). A new geomagnetic polarity time scale for the Late Cretaceous and Cenozoic. *Journal of Geophysical Research*, 97(B10):13917–13951.
- Cande, S. C., & Kent, D. V. (1995). Revised calibration of the geomagnetic polarity timescale for the Late Cretaceous and Cenozoic. *Journal of Geophysical Research*, 100(B4):6093–6095.
- Dorman, L. M., & Lewis, B. T. R. (1970). Experimental isostasy: 1. Theory of the determination of the Earth's isostatic response to a concentrated load. *Journal of Geophysical Research*, 75(17):3357–3365.
- Forsberg, R. (1984). *A Study of Terrain Reductions, Density Anomalies and Geophysical Inversion Methods in Gravity Field Modelling*. Report 355, Department of Geodetic Science and Surveying, Ohio State University.
- Forsberg, R. (1985). Gravity field terrain effect computations by FFT. *Bulletin Géodésique*, 59(4):342–360.
- Forsyth, D. W. (1985). Subsurface loading and estimates of the flexural rigidity of continental lithosphere. *Journal of Geophysical Research*, 90(B14):12623–12632.
- Greenbaum, J. S., Blankenship, D. D., Young, D. A., Richter, T. G., Roberts, J. L., Aitken, A. R. A., et al. (2015). Ocean access to a cavity beneath Totten Glacier in East Antarctica. *Nature Geoscience*, 8:294–298.
- Hammer, S. (1939). Terrain corrections for gravimeter stations. *Geophysics*, 4(3):184–194.
- Hinze, W. J., Aiken, C., Brozena, J., Coakley, B., Dater, D., Flanagan, G., et al. (2005). New standards for reducing gravity data: The North American gravity database. *Geophysics*, 70(4):J25–J32.
- Hirt, C., Claessens, S., Fecher, T., Kuhn, M., Pail, R., & Rexer, M. (2013). New ultrahigh-resolution picture of Earth's gravity field. *Geophysical Research Letters*, 40(16):4279–4283.
- LaFehr, T. R. (1991). An exact solution for the gravity curvature (Bullard B) correction. *Geophysics*, 56(8):1179–1184.
- Langston, C. A. (1979). Structure under Mount Rainier, Washington, inferred from teleseismic body waves. *Journal of Geophysical Research*, 84(B9):4749–4762.
- Laske, G., Masters, G., Ma, Z., & Pasyanos, M. (2013). Update on CRUST1.0 — A 1-degree global model of Earth's crust. *Geophysical Research Abstracts*, 15, EGU2013-2658.
- Meyer, B., Saltus, R., & Chulliat, A. (2017). *EMAG2v3: Earth Magnetic Anomaly Grid (2-arc-minute resolution), Version 3*. NOAA National Centers for Environmental Information.
- Morlighem, M., Williams, C. N., Rignot, E., An, L., Arndt, J. E., Bamber, J. L., et al. (2017). BedMachine v3: Complete bed topography and ocean bathymetry mapping of Greenland from multibeam echo sounding combined with mass conservation. *Geophysical Research Letters*, 44(21):11051–11061.
- Morlighem, M., Rignot, E., Binder, T., Blankenship, D., Drews, R., Eagles, G., et al. (2020). Deep glacial troughs and stabilizing ridges unveiled beneath the margins of the Antarctic ice sheet. *Nature Geoscience*, 13:132–137.
- Müller, R. D., Sdrolias, M., Gaina, C., & Roest, W. R. (2008). Age, spreading rates, and spreading asymmetry of the world's ocean crust. *Geochemistry, Geophysics, Geosystems*, 9:Q04006.
- Müller, R. D., Zahirovic, S., Williams, S. E., Cannon, J., Seton, M., Bower, D. J., et al. (2019). A global plate model including lithospheric deformation along major rifts and orogens since the Triassic. *Tectonics*, 38(6):1884–1907.
- Nagy, D. (1966). The gravitational attraction of a right rectangular prism. *Geophysics*, 31(2):362–371.
- Nagy, D., Papp, G., & Benedek, J. (2000). The gravitational potential and its derivatives for the prism. *Journal of Geodesy*, 74(7–8):552–560.
- Parker, R. L. (1973). The rapid calculation of potential anomalies. *Geophysical Journal of the Royal Astronomical Society*, 31(4):447–455.
- Parsons, B., & Sclater, J. G. (1977). An analysis of the variation of ocean floor bathymetry and heat flow with age. *Journal of Geophysical Research*, 82(5):803–827.
- Pavlis, N. K., Holmes, S. A., Kenyon, S. C., & Factor, J. K. (2012). The development and evaluation of the Earth Gravitational Model 2008 (EGM2008). *Journal of Geophysical Research: Solid Earth*, 117:B04406.
- Picard, K., Brooke, B., & Coffin, M. F. (2017). Geological insights from Malaysia Airlines flight MH370 search. *Eos*, 98. doi:10.1029/2017EO069015
- Stein, C. A., & Stein, S. (1992). A model for the global variation in oceanic depth and heat flow with lithospheric age. *Nature*, 359:123–129.
- Tinto, K. J., & Bell, R. E. (2011). Progressive unpinning of Thwaites Glacier from newly identified offshore ridge: Constraints from aerogravity. *Geophysical Research Letters*, 38:L20503.
- Vine, F. J., & Matthews, D. H. (1963). Magnetic anomalies over oceanic ridges. *Nature*, 199:947–949.
- Watts, A. B. (2001). *Isostasy and Flexure of the Lithosphere*. Cambridge University Press.
- Wieczorek, M. A., & Meschede, M. (2018). SHTools: Tools for working with spherical harmonics. *Geochemistry, Geophysics, Geosystems*, 19(8):2574–2592.
- Zhu, L., & Kanamori, H. (2000). Moho depth variation in southern California from teleseismic receiver functions. *Journal of Geophysical Research*, 105(B2):2969–2980.

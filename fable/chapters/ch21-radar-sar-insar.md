# Chapter 21 — Radar, SAR, InSAR, radar altimetry, and ice-penetrating radar

> **Part V — Sensors and platforms.** After the laser and acoustic ranging sensors of [Chapter 18](ch18-topographic-lidar.md) to [Chapter 20](ch20-sonar.md), this chapter covers the microwave family: imaging radar and its interferometric and stereo derivatives, nadir-looking altimeters, and the long-wavelength radars that see through ice and soil to surfaces no other sensor reaches.

**In this chapter.** Radar is the only elevation sensor that works through cloud, at night, and in some cases through the surface itself — both its gift and its trap, because a radar DEM maps the *radar* scattering centre, which is the ground only for bare rock and soil. You will be able to draw the side-looking geometry and predict foreshortening, layover, and shadow; derive the phase-to-height relation and the height of ambiguity for repeat-pass and single-pass (bistatic) systems; decompose coherence into its loss terms and convert it into an expected height error; explain why repeat-pass DEMs inherit atmospheric artefacts that single-pass DEMs do not; estimate wavelength-dependent penetration bias in forest, snow, firn, and sand; read the height-error and coherence layers of SRTM, TanDEM-X, and Copernicus DEM; follow the chain from altimeter sea-surface heights to marine gravity to predicted bathymetry; and interpret radio-echo-sounding bed DEMs such as Bedmap and BedMachine. The Validation section gives a height-error budget and a checklist for testing an InSAR DEM against lidar or ICESat-2.

## 21.1 Radar basics and SAR imaging geometry

A **radar** transmits a microwave pulse and records the echo against two-way delay. Three architectures matter for elevation: the side-looking **imaging radar**, resolving range and along-track; the nadir **altimeter**, resolving range only; and the **sounder**, resolving interfaces within ice, snow, or soil. All share the ranging physics of [Chapter 17](ch17-measurement-physics.md): $R = c\,\Delta t/2$, slant-range resolution $\rho_r = c/(2 B_w)$ for chirp bandwidth $B_w$ (100 MHz → 1.5 m; 300 MHz → 0.5 m), and a wavelength $\lambda$ that decides what the wave interacts with. The bands and their approximate wavelengths: Ka (≈ 0.8 cm; SWOT), Ku (≈ 2.2 cm; ocean altimeters, CryoSat-2), X (≈ 3.1 cm; TerraSAR-X/TanDEM-X, COSMO-SkyMed, SRTM X-SAR), C (≈ 5.6 cm; ERS, Envisat, Radarsat, Sentinel-1, SRTM C-band), S (≈ 9.4 cm; NISAR, NovaSAR), L (≈ 24 cm; ALOS-2, SAOCOM, NISAR), P (≈ 69 cm; ESA Biomass), and VHF/UHF (1–6 m; ice sounders). Wavelength is destiny: a surface is "smooth" when its height variation is well below $\lambda/8$ (Rayleigh criterion), and a medium is transparent when its loss tangent is small at that frequency — which is why X-band stops at the top of a forest and P-band reaches the ground beneath it.

### 21.1.1 Synthetic aperture

A real antenna of length $L$ has an along-track beamwidth of about $\lambda/L$ — roughly 4 km on the ground for a 10 m C-band antenna at 700 km. **Synthetic aperture radar (SAR)** records each scatterer's phase history as the platform passes and compresses it coherently to an **azimuth** resolution of about $L/2$ regardless of range (Cumming & Wong 2005). Side-looking geometry follows, since a nadir imager cannot separate left from right at equal delay; SAR therefore images in **slant range** and azimuth, a coordinate system neither map-like nor height-free.

### 21.1.2 Foreshortening, layover, and shadow

Because the radar measures range, terrain facing the sensor is compressed and terrain facing away is stretched. Let $\theta$ be the local **incidence angle** (between the radar line of sight and the local vertical, roughly 20–45° for most spaceborne SARs) and $\alpha$ the terrain slope in the range direction, positive when facing the radar. A ground-range length $\Delta g$ on that slope projects to a slant-range length

$$\Delta r = \Delta g\,\sin(\theta - \alpha).$$

When $0 < \alpha < \theta$ the slope is **foreshortened** — compressed into fewer range cells and bright because many scatterers share each cell. When $\alpha \ge \theta$ the summit is closer to the radar than the foot and the range ordering inverts: **layover**, with summit and foot superposed in the same cells and inseparable. When the back-slope exceeds $90° - \theta$ the terrain is not illuminated: **radar shadow**. At 30° incidence, layover affects radar-facing slopes steeper than 30° and shadow away-facing slopes steeper than 60°; at 45° both thresholds are 45°. Steep incidence reduces shadow and increases layover; shallow incidence does the reverse, and no angle frees a mountain range of both — which is why global InSAR DEMs combine ascending and descending passes and why their layover/shadow masks are essential metadata (Section 21.10).

<!-- figure: Figure 21.1 — Side-looking geometry showing a ridge imaged at incidence angle θ: foreshortening of the facing slope, layover where slope exceeds θ, shadow on the far slope where back-slope exceeds 90° − θ, with the slant-range axis annotated to show the inverted ordering of summit and foot in layover. -->

### 21.1.3 Speckle

Each resolution cell contains many scatterers whose echoes add with random phases, so amplitude fluctuates from cell to cell even over a uniform surface. This **speckle** is deterministic for a given scene and geometry but behaves like multiplicative noise with standard deviation equal to the mean for single-look intensity; averaging $N$ independent looks reduces it by $\sqrt{N}$ at the cost of resolution. It sets the noise floor of radargrammetric matching (Section 21.5), and the same multi-looking that suppresses it yields usable interferometric phase and coherence estimates (Section 21.2; Mathematics).

## 21.2 InSAR DEM generation

**Interferometric SAR (InSAR)** compares the phase of two SAR images of the same scene acquired from slightly different positions. For a scatterer at slant ranges $R_1$ and $R_2$ from the two antennas, the interferometric phase is

$$\phi = -\frac{2\pi p}{\lambda}\,(R_2 - R_1),$$

where $p = 2$ for a **monostatic** system in which each antenna transmits and receives (repeat-pass InSAR; TanDEM-X "ping-pong" mode) and $p = 1$ when one antenna transmits and both receive (SRTM; standard TanDEM-X bistatic mode; SWOT KaRIn). The range difference depends on the baseline $B$ and its component $B_\perp$ perpendicular to the line of sight; after subtracting the **flat-Earth** phase of a reference surface, the residual is proportional to height above it. The Mathematics section derives the result; its practical summary is the **height of ambiguity**

$$h_{\mathrm{amb}} = \frac{\lambda\,R\,\sin\theta}{p\,B_\perp},$$

the height change that produces one full fringe of $2\pi$. Longer perpendicular baselines give smaller $h_{\mathrm{amb}}$ and therefore finer height sensitivity, until geometric decorrelation (below) destroys the signal.

### 21.2.1 The processing chain

Every step of the chain can inject error (Rosen et al. 2000; Hanssen 2001): (1) focusing to single-look complex images; (2) coregistering the secondary to ≈ 0.1 pixel (≈ 0.001 pixel in azimuth for Sentinel-1 TOPS); (3) interferogram formation and multi-looking; (4) removing flat-Earth and reference-DEM phase with precise orbits; (5) filtering (Goldstein & Werner 1998), which aids unwrapping at the cost of smoothing; (6) unwrapping; (7) phase-to-height conversion and geocoding; (8) calibrating absolute height and tilt against ground control (ICESat/ICESat-2, GNSS, lidar), since the phase has an unknown constant and the baseline is never perfectly known; (9) mosaicking passes weighted by expected height error, with masks for layover, shadow, and low coherence.

### 21.2.2 Phase unwrapping

The interferogram records phase modulo $2\pi$; unwrapping adds the integer cycles that make the field consistent, which is possible only where the true phase changes by less than $\pi$ between neighbouring pixels (range slope below $h_{\mathrm{amb}}/(2\,\Delta g)$ per pixel) and noise does not create spurious discontinuities. **Branch-cut** methods (Goldstein, Zebker & Werner 1988) find **residues** — points where the wrapped gradient integrated around a 2 × 2 loop is non-zero — connect them with cuts, and integrate around them; fast, but leaving islands unwrapped. **Minimum-cost-flow** methods (Costantini 1998) minimise the weighted number of cycle discontinuities as a network-flow problem. **SNAPHU** (Chen & Zebker 2001) adds a statistical cost model from local intensity and coherence and solves for the maximum-a-posteriori field; it is the default in ISCE, GMTSAR, and most research pipelines. All three fail in the same places — steep terrain near layover, low-coherence patches, narrow corridors between them — and in the same way: a region offset by an integer number of $h_{\mathrm{amb}}$ with a sharp step at its boundary, a terrace or cliff in the DEM (Pitfalls).

### 21.2.3 Coherence and decorrelation

**Coherence** $\gamma$ is the magnitude of the complex correlation between the two images, estimated over a window of pixels, from 0 (pure noise) to 1 (identical echoes). It is modelled as a product of independent loss factors (Zebker & Villasenor 1992):

$$\gamma = \gamma_{\mathrm{thermal}}\;\gamma_{\mathrm{geom}}\;\gamma_{\mathrm{vol}}\;\gamma_{\mathrm{temporal}}\;\gamma_{\mathrm{proc}}.$$

**Thermal** decorrelation is set by signal-to-noise ratio, $\gamma_{\mathrm{thermal}} = 1/(1 + \mathrm{SNR}^{-1})$: 0.91 at 10 dB, 0.5 at 0 dB, so calm water, smooth sand, and some snow decorrelate because they return almost nothing. **Geometric** decorrelation arises because the two antennas see the ground-range spectrum shifted relative to each other; the shift grows with $B_\perp$ until the spectra no longer overlap at the **critical baseline** $B_{\perp,\mathrm{crit}} = \lambda R \tan\theta / (p\,\rho_r)$ — about 1.1 km for ERS/Envisat-class C-band at 23°, roughly 5 km for Sentinel-1 IW, several kilometres for TanDEM-X, whose 100–500 m baselines are well within limits. **Volume** decorrelation occurs when scatterers are distributed in depth (canopy, snow, firn, dry sand); it is itself a measurement of the volume (the basis of PolInSAR forest height) and the mechanism behind the penetration bias of Section 21.3. **Temporal** decorrelation is change in the scatterers between acquisitions — moving leaves, soil moisture, snowfall, waves — and is zero by construction in single-pass systems; it is why SRTM and TanDEM-X could produce global DEMs and repeat-pass Sentinel-1 cannot outside deserts and cities, since over vegetation C-band coherence falls below usable levels within days to weeks and X-band within one orbit cycle. **Processing** decorrelation comes from coregistration and interpolation.

### 21.2.4 Atmospheric phase screen

Microwaves are delayed by the troposphere (water vapour, pressure, temperature) and the ionosphere (electron content, scaling as $\lambda^2$, so 20 times worse at L-band than C-band). In a repeat-pass interferogram the two acquisitions sample different atmospheres, and the difference — the **atmospheric phase screen (APS)** — is indistinguishable from topography or deformation. Tropospheric delay differences of 1–3 cm over tens of kilometres are routine, 10 cm in convective weather, and the height conversion is severe because phase is scaled by $h_{\mathrm{amb}}$: a one-way delay difference $\delta L$ gives $\delta h = p\,h_{\mathrm{amb}}\,\delta L/\lambda$, which for $p = 2$, $h_{\mathrm{amb}} = 50$ m, $\lambda = 5.6$ cm, $\delta L = 1$ cm is 18 m. Single-pass systems see one atmosphere at one instant, so the APS cancels — the second reason, after temporal decorrelation, that global InSAR DEMs come from single-pass missions. Repeat-pass producers mitigate the APS by stacking many interferograms (atmosphere is random pass to pass, topography is not) and by weather-model corrections (ERA5-based services such as GACOS).

### 21.2.5 Single-pass versus repeat-pass

**SRTM** (February 2000) carried C- and X-band antenna pairs on the Shuttle, the second antennas on a 60 m mast, and mapped 80 % of the land between 60° N and 56° S in eleven days (Farr et al. 2007). The mast flexed, so the baseline was tracked continuously and residual tilts calibrated against ocean and kinematic-GNSS control; absolute vertical accuracy is 16 m LE90 by specification and about 6–9 m LE90 as assessed (Rodríguez, Morris & Belz 2006). **TanDEM-X** (2010–present) flies two X-band satellites in a helix 120–500 m apart, acquiring bistatic interferograms with neither temporal decorrelation nor APS; its global DEM from 2010–2015 acquisitions, with repeat coverage of difficult terrain at different heights of ambiguity, is specified at 10 m absolute and 2 m relative (slopes < 20 %) at 90 % confidence (Krieger et al. 2007; Rizzoli et al. 2017). **Repeat-pass** DEMs — ERS-1/2 tandem, Envisat, ALOS PALSAR, Sentinel-1 — remain useful where coherence holds (deserts, cities, winter bare ice) and for topographic *change*, but a single repeat-pass interferogram should never become an absolute DEM without independent control and an atmospheric budget.

> **Definitions that bite.** *Height of ambiguity* is quoted with and without the factor $p$: a TanDEM-X note giving "$h_{\mathrm{amb}} = 45$ m" for a bistatic acquisition corresponds to 22.5 m if the same baseline were flown monostatically; check the convention when comparing missions. *Coherence* is reported either raw (biased high at low values, because the magnitude of a noisy complex mean is positive) or bias-corrected; a 5 × 5 window overestimates zero coherence by about 0.2.

## 21.3 Penetration and the measured surface

A radar DEM is the surface of **scattering phase centres**, not of the first physical interface. For a volume scatterer the phase centre lies inside the volume at a depth set by the extinction coefficient at the radar's wavelength, so the InSAR height is biased *below* the top of the volume by an amount that also depends on the interferometric geometry (Dall 2007).

**Vegetation.** At X-band the phase centre sits within the top few metres of a closed canopy, so TanDEM-X and Copernicus DEM heights over forest are close to a DSM. At C-band the SRTM phase centre lies roughly in the upper third to half of the canopy; Carabajal & Harding (2006) quantified this against ICESat as a positive SRTM bias growing with tree cover and canopy height — several metres in temperate forest, more than 10 m in dense tropical forest — with agreement to a few metres over bare, flat terrain. At L-band the phase centre drops toward the lower canopy and trunks, and at P-band much of the return is ground and trunk–ground double bounce, which is why ESA's **Biomass** (launched April 2025; 435 MHz, ≈ 69 cm) can weigh forests tomographically and, as a secondary product, map sub-canopy terrain (Quegan et al. 2019). None of these is a DTM in the lidar sense; an X-band DEM over forest is "canopy top minus a wavelength- and density-dependent penetration of a few metres".

**Snow, firn, and ice.** Dry snow and firn are nearly transparent at X- and C-band, and the phase centre can lie several metres down. Over the dry-snow zones of Greenland and Antarctica, TanDEM-X elevations are biased low by roughly 3–10 m relative to laser altimetry, varying with firn density, grain size, and height of ambiguity (Rizzoli et al. 2017; Abdullahi et al. 2019); Hoen & Zebker (2000) inferred C-band penetration of order 10–20 m from volume decorrelation over Greenland. Wet snow is opaque and the phase centre is near the surface, so one DEM can carry a spatially varying bias of metres depending on where the melt line lay; blue ice and bare glacier ice behave as surfaces. The rule for cryospheric differencing ([Chapter 41](ch41-change-detection.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)): never difference a radar DEM against lidar or optical over firn without a penetration correction, nor two radar DEMs of different bands or seasons as if penetration cancelled.

**Dry sand and soil.** Hyper-arid sand with volumetric moisture below a few percent is transparent at L-band to depths of metres — the Shuttle Imaging Radar-A discovery of buried Saharan palaeo-drainage in 1981 (McCauley et al. 1982). At C- and X-band the effect is decimetres at most; for DEMs it means a small negative bias over dune fields at L-band rather than a large height error.

**Water and wet surfaces.** Calm water is a specular mirror at all bands and returns nothing to a side-looking antenna, so lakes and calm rivers are dark, decorrelated, and void in InSAR DEMs; they are then "filled" by editing (Copernicus DEM flattens them to a constant height) — an editorial decision, not a measurement ([Chapter 34](ch34-water-in-dems.md)).

<!-- figure: Figure 21.2 — Schematic vertical profiles of scattering phase centre depth for X, C, L, and P band over (a) closed forest canopy, (b) dry firn, (c) wet snow, (d) hyper-arid sand, with approximate depth scales and the resulting sign of the DEM bias relative to the physical surface. -->

## 21.4 Differential InSAR and time series

Removing the topographic phase with an existing DEM leaves, in a repeat-pass interferogram, the change in line-of-sight range between acquisitions — **differential InSAR (DInSAR)** — at one fringe per $\lambda/2$ (2.8 cm at C-band) and, after unwrapping and averaging, millimetre-per-year rates (Massonnet & Feigl 1998; Bürgmann, Rosen & Fielding 2000). DInSAR belongs to Part VIII ([Chapter 38](ch38-plate-motion-and-vlm.md), [Chapter 39](ch39-earthquakes-volcanoes-landslides.md)); two connections to DEMs matter here.

First, DInSAR inherits the DEM's errors: a reference-DEM error $\delta h$ leaves a residual phase $\delta\phi = 2\pi\,\delta h/h_{\mathrm{amb}}$ in every interferogram, scaling with $B_\perp$. With a 10 m error and $h_{\mathrm{amb}} = 100$ m the residual is 0.1 cycle, or 2.8 mm of apparent displacement at C-band — negligible for an earthquake, fatal for a 2 mm/yr subsidence trend if baselines correlate with time. Time-series methods remove this term because it scales with baseline while deformation scales with time.

Second, those methods are themselves DEM refinement. **Persistent scatterer interferometry (PSI)** (Ferretti, Prati & Rocca 2001) identifies pixels dominated by one stable scatterer — building corners, outcrops, corner reflectors — and solves jointly for displacement history and a height correction relative to the reference DEM, at sub-metre precision for good scatterers. **Small-baseline subset (SBAS)** methods (Berardino et al. 2002) invert many short-baseline, short-interval interferograms of distributed scatterers for displacement time series, estimating the DEM-error term in the same inversion; **StaMPS** (Hooper et al. 2004) extended PSI to natural terrain, and MintPy, LiCSBAS, and PyRate make SBAS routine on Sentinel-1 stacks. Results that feed back into elevation work include subsidence over aquifers and mines (which moves the vertical datum under benchmarks — [Chapter 9](ch09-vertical-datums.md)), co-seismic displacement fields that force re-survey of control ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md)), and slow landslides, where a DInSAR velocity map tells a lidar campaign where to look.

> **Rule of thumb.** In a repeat-pass stack, any signal that correlates with $B_\perp$ is topography (or DEM error); any signal common to all interferograms sharing one date is that date's atmosphere; what grows with time is deformation. The separation works only when the stack is large (tens of acquisitions) and baselines are not themselves correlated with time.

## 21.5 Radargrammetry, SAR stereo, and offset tracking

Interferometry uses phase; **radargrammetry** uses amplitude and geometry. Two SAR images from different incidence angles image each point at ranges that differ with its height, as optical stereo parallax does ([Chapter 22](ch22-photogrammetry-sfm.md)); matching the amplitude images gives a range disparity, and intersecting the two range–Doppler loci gives a 3D point (Leberl 1990; Toutin & Gray 2000). The ground-range height sensitivity is $\partial h / \partial \Delta g = 1/(\cot\theta_1 - \cot\theta_2)$ — about 0.9 for a pair at 25° and 45°, so a 1 pixel matching error at 3 m resolution is roughly 3 m of height. Radargrammetry needs no coherence, so it works across years and vegetation change where InSAR fails, with no unwrapping ambiguity; its costs are matching noise (speckle forces heavy averaging, so effective resolutions of 30–100 m from 3 m imagery are typical), a reduced but present penetration bias, and doubled layover/shadow because both images must see the point. Radarsat-2 and TerraSAR-X stereo pairs reach 5–10 m RMSE in moderate terrain, and Canada used radargrammetry in the Arctic where cloud defeated optical stereo (Toutin 2010).

**Offset tracking** cross-correlates small windows of two amplitude images for sub-pixel shifts (Strozzi et al. 2002): two orders of magnitude less precise than DInSAR (1/10–1/30 pixel) but able to measure multi-metre displacements over decorrelated glaciers, landslides, and fault zones ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)). For DEM work it is diagnostic: azimuth offsets that correlate with topography reveal orbit or timing errors that would otherwise appear as a tilt in the InSAR height.

## 21.6 Geocoding, terrain correction, and the circularity problem

A SAR image in slant-range/azimuth coordinates cannot be placed on a map without the height of every pixel, since the ground position of a range cell depends on where the range sphere meets the terrain. **Geocoding** therefore requires a DEM, as does **radiometric terrain correction (RTC)**, which normalises backscatter for the local illuminated area (Small 2011). Every geocoded or RTC product carries its DEM's error projected through the geometry: a height error $\delta h$ displaces the pixel horizontally by $\delta h / \tan\theta$ — about 17 m for 10 m at 30° — and distorts the RTC area term in proportion to the DEM's slope error.

This is circular whenever the DEM under evaluation was itself SAR-derived. Geocoding Sentinel-1 with Copernicus DEM (TanDEM-X lineage) inherits its forest penetration bias and water editing, and "validating" Copernicus DEM with that geocoded product succeeds trivially. The CEOS Analysis Ready Data specification requires the geocoding/RTC DEM to be named in metadata so that this inheritance can be traced; apply the same discipline to any DEM you make from geocoded SAR. InSAR DEM generation likewise flattens the interferogram with a reference DEM, and the new DEM's long-wavelength tilt and absolute level are only as good as the subsequent calibration against independent control (Section 21.2.1, step 8).

## 21.7 Radar altimetry

A **radar altimeter** points at nadir, transmits a Ku-band (sometimes Ka- or C-band) chirp, and measures two-way delay to the surface to 1–3 cm over the open ocean. The pulse-limited echo integrates an expanding annulus; its **waveform** is fitted (the Brown model over oceans) for range, significant wave height, and backscatter over an effective footprint of 2–10 km depending on wave height (Fu & Cazenave 2001; Chelton et al. 2001). Range, corrected for ionosphere, dry and wet troposphere, sea-state bias, and tides, is subtracted from the precise orbit to give **sea-surface height (SSH)** above the ellipsoid. **TOPEX/Poseidon** (1992–2006) first achieved a sub-decimetre SSH budget; **Jason-1/2/3** and **Sentinel-6 Michael Freilich** (November 2020) continue its 10-day, 66° reference orbit in a thirty-year sea-level record. **CryoSat-2** (April 2010) adds a delay-Doppler (SAR) mode that sharpens the along-track footprint to about 300 m and a **SARIn** mode whose two antennas 1.17 m apart resolve the across-track angle of the first return — essential over ice-sheet margins and mountain glaciers, where the first echo rarely comes from nadir (Wingham et al. 2006). **Sentinel-3A/B** (2016, 2018) run SAR mode globally, and **SWOT** (December 2022) carries **KaRIn**, a Ka-band single-pass interferometer on a 10 m boom mapping water-surface height in two 50 km swaths at 2 km (ocean) and roughly 100 m (inland) posting, with centimetre-level precision after averaging (Fu et al. 2024).

### 21.7.1 Sea-surface height to marine gravity to bathymetry

Time-averaged SSH is the marine geoid plus about ± 1 m of dynamic topography, and the geoid reflects the seafloor because a seamount's excess mass pulls the sea surface up by metres over tens of kilometres. The chain: along-track SSH → along-track slope (differencing removes orbit error and long-wavelength dynamic topography) → deflection of the vertical (1 µrad ≈ 1 mGal, since $g \approx 9.8$ m s$^{-2}$) → gridded gravity anomaly → predicted bathymetry by downward continuation and an empirically calibrated admittance in the 15–160 km band (Smith & Sandwell 1994, 1997). Resolution is limited by along-track noise, footprint, and track spacing, which is why the dense non-repeating geodetic orbits of Geosat (1985–86), ERS-1 (1994–95), CryoSat-2, Jason-1 (2012–13), and SARAL/AltiKa were so valuable: Sandwell et al. (2014) reached about 2 mGal accuracy and roughly 6 km half-wavelength resolution, revealing thousands of unknown seamounts. The resulting bathymetry, its uncertainty of hundreds of metres, and its role in SRTM15+ and GEBCO are treated in [Chapter 23](ch23-satellite-derived-bathymetry.md) and [Chapter 24](ch24-gravity-magnetics-geophysics.md).

### 21.7.2 Ice sheets and inland water

Over ice sheets, CryoSat-2 SARIn with ICESat (2003–2009) and ICESat-2 (2018–) underpins the mass-balance record. Radar-specific caveats are firn penetration (the Ku-band phase centre can lie metres down and move with melt events; Section 21.3), slope-induced error (the first return comes from the nearest point, possibly kilometres from nadir; SARIn resolves this, conventional altimeters need a DEM-based slope correction — another inheritance), and footprint smoothing. Over rivers and lakes, nadir altimeters give stage at crossings (Hydroweb, DAHITI, G-REALM) and SWOT gives water-surface elevation and slope over whole reaches at decimetre precision — observations [Chapter 34](ch34-water-in-dems.md) uses to check hydro-flattened DEMs and [Chapter 61](ch61-hydrology.md) uses as boundary conditions.

<!-- figure: Figure 21.3 — The altimetry-to-bathymetry chain: along-track SSH profile over a seamount, derived slope and gravity anomaly, gridded gravity, and predicted depth, with annotation of the wavelength band in which the admittance is used and the shipboard soundings used for calibration. -->

## 21.8 Ice-penetrating and ground-penetrating radar

At VHF and UHF (roughly 1–1,000 MHz) cold ice is among the most transparent natural materials, attenuating 5–30 dB per kilometre depending on temperature and impurities, so a downward-looking radar receives echoes from the surface, internal isochrones, and the bed up to 4 km below. **Radio-echo sounding (RES)** has flown since the 1960s (Evans & Robin's 35 MHz system at the Scott Polar Research Institute; the SPRI–NSF–TUD campaigns of 1967–1979) and today uses systems such as CReSIS MCoRDS (near 195 MHz, multi-channel arrays for clutter suppression), BAS PASIN (150 MHz), AWI's UWB radar, and NASA's Operation IceBridge suite (2009–2019). Depth is $d = c\,t/(2 n_{\mathrm{ice}})$ with $n_{\mathrm{ice}} \approx 1.78$ (about 168–169 m µs$^{-1}$) plus a **firn correction** of roughly 5–15 m for faster propagation through low-density firn; bed elevation is surface elevation (laser altimetry on the same aircraft, or a surface DEM) minus thickness. Thickness precision on a well-focused bed echo is of order 10 m; the dominant errors are bed picking under clutter, the firn correction, and above all track spacing of tens of kilometres across much of the interior.

Bed DEMs are therefore interpolation products with highly non-stationary error. **Bedmap2** (Fretwell et al. 2013) gridded roughly 25 million thickness measurements at 1 km with per-cell uncertainty from about 60 m near data to about 1,000 m in the largest gaps; **Bedmap3** (Pritchard et al. 2025) adds some 50 million points and a 500 m grid, yet gaps of hundreds of kilometres remain. **BedMachine** (Morlighem et al. 2017 for Greenland; 2020 for Antarctica) replaces interpolation in fast-flowing outlet glaciers with **mass conservation**: given surface velocity, mass balance, and thinning, the thickness field must satisfy continuity, which constrains the bed far more tightly than kriging and revealed deep fjords under Greenland's outlet glaciers that interpolation had smoothed away. Its error layer is correspondingly structured — tens of metres where mass conservation applies, hundreds in the slow interior. A bed DEM's smoothness is a property of the interpolator, not of the bed; read the error layers.

At higher frequencies and shorter ranges, **ground-penetrating radar (GPR)** (25 MHz–2 GHz) profiles snow depth on glaciers and sea ice, the permafrost active layer, the water table in sand, and buried utilities. Snow depth from two-way time needs the snow's permittivity, which depends on density (for dry snow the Kovacs relation $\varepsilon_r \approx (1 + 0.845\rho)^2$ with $\rho$ in g cm$^{-3}$; wet snow needs a liquid-water term), so an unmeasured density is a direct depth error — 10 % in density is about 4 % in depth. [Chapter 24](ch24-gravity-magnetics-geophysics.md) places GPR among the other "Earth layers as DEMs" sensors.

## 21.9 Ground-based radar interferometers

A **ground-based SAR (GB-SAR)** moves a Ku- or X-band antenna along a 1–3 m rail (or scans a real-aperture dish) and images a slope, dam, or pit wall every few minutes from a fixed position (Monserrat, Crosetto & Luzi 2014). With no motion between acquisitions there is no baseline and no topographic phase; the interferometric phase is line-of-sight displacement plus atmosphere, at sub-millimetre precision over a few kilometres; mine and dam operators run these systems (IDS IBIS, GroundProbe SSR, Reutech MSR) as alarmed deformation monitors. Topography enters as the geocoding DEM: projecting the range–azimuth displacement map onto the wall requires a DEM — typically TLS or drone photogrammetry — whose errors displace the alarm polygons. A rail system relocated between campaigns acquires a baseline, and the problem becomes repeat-pass InSAR with a small $h_{\mathrm{amb}}$ that must be handled explicitly (Noferini et al. 2005).

## 21.10 Products and missions

The table summarises the InSAR DEM products most readers will meet; [Chapter 55](ch55-public-products.md) and [Appendix E](../appendices/appendix-e-public-products-tables.md) compare them with optical and lidar products.

| Product | Source | Acquired | Posting | Stated vertical accuracy | Notes |
|---|---|---|---|---|---|
| SRTM (v3 / SRTMGL1) | Shuttle C-band single-pass | 2000-02 | 1″ (≈ 30 m); 3″ | 16 m LE90 spec; ≈ 6–9 m LE90 assessed | 60° N–56° S; voids in steep terrain filled from other sources in v3 |
| NASADEM | SRTM reprocessed with ICESat control | 2000-02 (data) / 2020 (release) | 1″ | Improved unwrapping and void reduction over SRTM v3 | Same penetration behaviour as SRTM |
| TanDEM-X DEM | TerraSAR-X/TanDEM-X bistatic | 2010-12 to 2015-01 | 0.4″ (12 m); 1″; 3″ | 10 m abs. / 2 m rel. LE90 spec; ≈ 3.5 m LE90 abs. assessed globally against ICESat | HEM, COM, COV, AMP layers; 90 m version free |
| TanDEM-X 30 m EDEM | Edited TanDEM-X | 2010–2020 (incl. later acquisitions) | 1″ | As above | Edited/hydro-flattened; free for research |
| Copernicus DEM GLO-30 / GLO-90 / EEA-10 | Edited TanDEM-X (WorldDEM lineage) | 2011–2015 | 1″ / 3″ / 10 m (Europe) | < 4 m abs. LE90, < 2 m rel. (stated) | Edited water, coastlines, airports; infill from other DEMs flagged in EDM/FLM layers |

Three missions set what repeat-pass InSAR can now offer. **Sentinel-1** (1A launched April 2014; 1B April 2016, failed December 2021; 1C December 2024; 1D November 2025) gives C-band IW coverage of all land every 6–12 days with free data and standardised processing (ASF HyP3, ESA SNAP), making DInSAR time series routine but DEM-quality coherence available only in arid and urban areas. **NISAR** (NASA–ISRO; launched July 2025) carries L- and S-band SweepSAR with a 240 km swath and 12-day repeat; L-band's slower decorrelation gives usable repeat-pass coherence over vegetation, though its systematic plan targets deformation and biomass rather than DEM production. **TanDEM-X** continues a second global coverage (the 30 m EDEM and change-DEM products) and remains the only operational single-pass spaceborne InSAR system; L-band successors (Tandem-L, ESA Harmony-class concepts) have been studied but not flown (verify current status).

> **Case file.** The SRTM canopy bias of Section 21.3 (Carabajal & Harding 2006) is not random noise: hydrologic models that treated it as such produced spurious ridges along forest–field boundaries and reversed drainage in low-relief floodplains — one reason MERIT DEM (Yamazaki et al. 2017) explicitly removed tree-height bias, speckle, and stripe noise from SRTM before conditioning.

## Then & now

- **1951–1960s.** Carl Wiley's Doppler beam-sharpening patent (filed 1954) and the Willow Run airborne programs establish synthetic-aperture imaging; radio-echo sounding of ice sheets begins at the Scott Polar Research Institute, and the SPRI–NSF–TUD campaigns (1967–1979) map Antarctic ice thickness at continental scale.
- **1974–1986.** Graham demonstrates airborne InSAR topography (1974); Seasat flies the first civilian spaceborne SAR and precise altimeter (1978); SIR-A reveals buried Saharan drainage at L-band (1981); Zebker & Goldstein (1986) demonstrate single-pass airborne InSAR DEMs.
- **1985–1997.** Geosat and ERS-1 geodetic altimeter missions; Smith & Sandwell predicted bathymetry (1994, 1997).
- **1991–1993.** ERS-1 launches; Massonnet et al. (1993) map the Landers earthquake with DInSAR, the founding image of the method; TOPEX/Poseidon begins the precision altimetry record (1992).
- **2000 ⟨H⟩.** SRTM flies on STS-99 (11–22 February), producing the first near-global, consistent DEM from a single instrument in eleven days.
- **2001–2002.** Persistent scatterer interferometry (Ferretti, Prati & Rocca) and SBAS (Berardino et al.) formalised.
- **2007–2010.** TerraSAR-X (2007), TanDEM-X and CryoSat-2 (2010) launch.
- **2014–2016.** Sentinel-1A begins free systematic C-band coverage; CryoSat-2/Jason-1 marine gravity (Sandwell et al. 2014); TanDEM-X global DEM completed (2016), Copernicus DEM released from 2020.
- **2022–2025.** SWOT (2022) brings single-pass Ka-band interferometry to water surfaces; Sentinel-1C (December 2024), Biomass (April 2025), NISAR (July 2025), and Sentinel-1D (November 2025) extend the band coverage from X to P.

The arc runs from a classified imaging technique to a free, systematic, multi-band observing system; what has not changed is where the phase centre sits.

## Mathematics

**Interferometric geometry.** Let antenna 1 be at height $H$ above a reference plane, looking at a point at slant range $R$, look angle $\theta$, and height $h$ above the plane; let antenna 2 be displaced by a baseline $B$ at angle $\alpha$ from horizontal. By the law of cosines,

$$R_2^2 = R^2 + B^2 - 2 R B \sin(\theta - \alpha),$$

and for $B \ll R$ the range difference is $\Delta R \approx -B\sin(\theta - \alpha) = -B_\parallel$, the component of the baseline parallel to the line of sight. The interferometric phase is $\phi = -(2\pi p/\lambda)\Delta R = (2\pi p/\lambda) B\sin(\theta - \alpha)$. Terrain height enters through $\theta$: $h = H - R\cos\theta$, so $\partial\theta/\partial h = 1/(R\sin\theta)$ and

$$\frac{\partial\phi}{\partial h} = \frac{2\pi p}{\lambda}\,B\cos(\theta - \alpha)\,\frac{1}{R\sin\theta} = \frac{2\pi p\,B_\perp}{\lambda R\sin\theta},$$

with $B_\perp = B\cos(\theta - \alpha)$ the perpendicular baseline. One fringe ($\Delta\phi = 2\pi$) therefore corresponds to the height of ambiguity

$$h_{\mathrm{amb}} = \frac{\lambda R \sin\theta}{p\,B_\perp}, \qquad p = \begin{cases} 2 & \text{monostatic (repeat-pass, ping-pong)} \\ 1 & \text{single-pass standard / bistatic} \end{cases}$$

and a phase error $\sigma_\phi$ gives $\sigma_h = h_{\mathrm{amb}}\,\sigma_\phi/(2\pi)$. The flat-Earth phase is $\phi$ at $h = 0$ as a function of range, removed before unwrapping; its range rate $\partial\phi/\partial R|_{h=0} = (2\pi p B_\perp)/(\lambda R \tan\theta)$ sets the critical baseline, beyond which the two images no longer share a range spectrum: $B_{\perp,\mathrm{crit}} = \lambda R \tan\theta / (p\,\rho_r)$.

**Phase statistics from coherence.** For $N$ independent looks and coherence $\gamma$, the Cramér–Rao bound on the interferometric phase standard deviation is

$$\sigma_\phi \ge \frac{1}{\sqrt{2N}}\,\frac{\sqrt{1 - \gamma^2}}{\gamma},$$

which is accurate for $N \gtrsim 4$ and $\gamma \gtrsim 0.3$ (Rodríguez & Martin 1992). Combined with the previous expression, the expected height error of an InSAR DEM is

$$\sigma_h = \frac{h_{\mathrm{amb}}}{2\pi}\,\frac{1}{\sqrt{2N}}\,\frac{\sqrt{1-\gamma^2}}{\gamma}.$$

This is the formula behind the TanDEM-X **height error map (HEM)** layer.

**Decorrelation terms.** Thermal: $\gamma_{\mathrm{thermal}} = (1 + \mathrm{SNR}^{-1})^{-1}$. Geometric (for a rectangular range spectrum): $\gamma_{\mathrm{geom}} = 1 - B_\perp/B_{\perp,\mathrm{crit}}$ for $B_\perp < B_{\perp,\mathrm{crit}}$, zero beyond. Volume, for an exponential vertical scattering profile of extinction $\kappa$ in a layer of thickness $d$ (the random-volume model): $\gamma_{\mathrm{vol}} = \left|\int_0^d e^{2\kappa z/\cos\theta} e^{j k_z z}\,dz\right| \big/ \int_0^d e^{2\kappa z/\cos\theta}\,dz$ with vertical wavenumber $k_z = 2\pi/h_{\mathrm{amb}}$; the phase of the same integral gives the phase-centre height and therefore the penetration bias, which shrinks as $h_{\mathrm{amb}}$ grows (Dall 2007).

**Layover and shadow conditions.** With incidence $\theta$ and range-direction slope $\alpha$ (positive toward the sensor), the ground-to-slant factor is $\sin(\theta - \alpha)$; layover when $\alpha \ge \theta$, shadow when $-\alpha \ge 90° - \theta$. Projecting a prior DEM into radar geometry (`isce2` `topo`, GAMMA `gc_map`) yields these masks.

**Atmosphere to height.** A differential one-way path delay $\delta L$ between passes enters the phase as $\delta\phi = 2\pi p\,\delta L/\lambda$ and the height as $\delta h = h_{\mathrm{amb}}\,\delta\phi/(2\pi) = p\,h_{\mathrm{amb}}\,\delta L/\lambda$.

> **Worked example.** *Height sensitivity and error for two systems.*
> (a) A TanDEM-X bistatic acquisition ($p = 1$, $\lambda = 3.1$ cm) at slant range $R = 620$ km and incidence $\theta = 35°$ with $B_\perp = 250$ m: $h_{\mathrm{amb}} = 0.031 \times 620{,}000 \times 0.574 / 250 = 44$ m. With $\gamma = 0.8$ and $N = 10$ looks, $\sigma_\phi = (1/\sqrt{20})(\sqrt{1 - 0.64}/0.8) = 0.224 \times 0.75 = 0.168$ rad, so $\sigma_h = 44 \times 0.168 / 6.283 = 1.2$ m. At $\gamma = 0.5$ the same geometry gives $\sigma_\phi = 0.387$ rad and $\sigma_h = 2.7$ m; at $\gamma = 0.3$, $\sigma_h = 5.0$ m.
> (b) A Sentinel-1 repeat-pass pair ($p = 2$, $\lambda = 5.55$ cm) at $R = 850$ km, $\theta = 39°$, $B_\perp = 120$ m: $h_{\mathrm{amb}} = 0.0555 \times 850{,}000 \times 0.629 / (2 \times 120) = 124$ m. A 1.5 cm tropospheric delay difference across the scene maps to $\delta h = 2 \times 124 \times 0.015 / 0.0555 = 67$ m — larger than the entire SRTM error budget, and the reason this pair would be used for deformation, not for a DEM.

## Validation & uncertainty

An InSAR DEM's error has four distinct components with different spatial structure, and a validation that reports a single RMSE conflates them.

**Random (phase-noise) error** follows the coherence formula, varies pixel to pixel, and is largest over water, wet snow, dense vegetation at short wavelengths, and foreshortened slopes. It is the only component the height-error layer describes; averaging reduces it at the cost of resolution.

**Unwrapping error** is integer multiples of $h_{\mathrm{amb}}$ over connected regions: blocky, bimodal in a residual histogram (clusters at zero and at ± $h_{\mathrm{amb}}$), and invisible to the height-error layer. Detect it by differencing against an independent DEM, checking histograms for secondary modes at the quoted $h_{\mathrm{amb}}$, and inspecting hillshades for terraces of constant step height. TanDEM-X mitigated it with dual-baseline acquisitions; NASADEM with better unwrapping and ICESat control.

**Penetration bias** is a systematic negative offset over volume scatterers, correlated with land cover, firn facies and, for repeat-pass, season. Detect it by stratifying residuals by land cover and canopy height (GEDI, lidar, ICESat-2 ATL08; [Chapter 25](ch25-calibration-infrastructure.md), [Chapter 52](ch52-ground-truth.md)).

**Long-wavelength calibration error** — tilt, offset, bowing from baseline, orbit, and (repeat-pass) atmosphere — varies over tens to hundreds of kilometres. Detect it by fitting a low-order surface to residuals against widely distributed control and by checking overlapping passes for consistency.

> **Uncertainty budget.** Illustrative budget for a 30 m posting single-pass X-band DEM over mixed terrain, in metres (1σ unless noted). Values are representative magnitudes from the TanDEM-X assessment literature (Rizzoli et al. 2017; Wessel et al. 2018) and should be re-derived for any specific product.
>
> | Component | Flat bare ground | Moderate slopes, open forest | Steep terrain / dense forest / firn |
> |---|---|---|---|
> | Phase noise (from HEM) | 0.5–1 | 1–2 | 2–6 |
> | Unwrapping residuals | ≈ 0 | rare, ± h_amb | localised, ± h_amb |
> | Penetration bias (mean, sign −) | 0 | 1–4 (canopy-dependent) | 3–10 (firn); canopy-top minus several m |
> | Calibration (tilt/offset) | 0.3–1 | 0.3–1 | 0.3–1 |
> | Horizontal-error-induced vertical error (σ_xy ≈ 3–6 m × slope) | ≈ 0 | 0.5–2 | 2–10 |
> | Combined RMSE (excluding unwrapping) | ≈ 1–1.5 | ≈ 2–4 | ≈ 5–15 |

**Procedure for testing an InSAR DEM.** (1) Obtain independent checkpoints — lidar, ICESat-2 ATL06/ATL08, GNSS profiles, a photogrammetric DEM — never a product derived from the same radar data. (2) Co-register horizontally on stable terrain (Nuth & Kääb 2011, implemented in `xdem`); offsets of 3–6 m are typical for 30 m InSAR products and produce large apparent vertical errors on slopes. (3) Apply the product's own masks (layover, shadow, water, infill, low coherence) *and* report the masked fraction. (4) Report mean, median, σ, NMAD, RMSE, and LE90/LE95 per land-cover and slope class ([Chapter 53](ch53-accuracy-assessment.md)). (5) Look for secondary histogram modes at ± $h_{\mathrm{amb}}$. (6) Compare empirical σ per class with the HEM; a ratio far from 1 means the HEM is miscalibrated or a non-random error dominates. (7) Report penetration bias separately from accuracy: it cancels when differencing two epochs of the same product, not when comparing to lidar.

> **Try it.** Compare Copernicus DEM GLO-30 against ICESat-2 ATL06 heights over a tile, stratified by slope. Expect, over bare flat terrain, a median within about ± 1 m and an NMAD of 1–2 m; over forest the median goes positive (DEM above ICESat-2 ground) by several metres.
>
> ```python
> import numpy as np, rasterio, geopandas as gpd
> from rasterio.transform import rowcol
>
> dem = rasterio.open("Copernicus_DSM_COG_10_N46_00_E007_00_DEM.tif")
> z = dem.read(1).astype(float)
> pts = gpd.read_file("atl06_subset.gpkg").to_crs(dem.crs)   # columns: h_li (ellipsoidal, WGS84)
> r, c = rowcol(dem.transform, pts.geometry.x, pts.geometry.y)
> ok = (r >= 0) & (r < z.shape[0]) & (c >= 0) & (c < z.shape[1])
> dem_h = z[r[ok], c[ok]]
> # Copernicus DEM is EGM2008 orthometric; convert ICESat-2 ellipsoidal to EGM2008 first,
> # e.g. with pyproj Transformer to EPSG:9518 (WGS84 + EGM2008), or pre-convert in SlideRule.
> res = dem_h - pts.loc[ok, "h_li_egm08"].to_numpy()
> gy, gx = np.gradient(z, dem.res[1], dem.res[0])
> slope = np.degrees(np.arctan(np.hypot(gx, gy)))[r[ok], c[ok]]
> for lo, hi in [(0, 5), (5, 15), (15, 30), (30, 90)]:
>     m = (slope >= lo) & (slope < hi)
>     d = res[m]
>     nmad = 1.4826 * np.median(np.abs(d - np.median(d)))
>     print(f"slope {lo:2d}-{hi:2d}°  n={m.sum():6d}  median={np.median(d):6.2f}  "
>           f"NMAD={nmad:5.2f}  RMSE={np.sqrt(np.mean(d**2)):5.2f}  "
>           f"LE90={np.percentile(np.abs(d), 90):5.2f}")
> ```

**What to report** for any radar-derived DEM: band and mission; single- or repeat-pass; acquisition dates; $h_{\mathrm{amb}}$ (with the $p$ convention) and $B_\perp$; unwrapping method; reference DEM used for flattening and geocoding; coherence and height-error layers; masks for layover, shadow, water, and infill with the infill source; calibration control and its datum; validation statistics by slope and land cover; and which surface the heights represent over forest, snow, and firn.

## Software

**Open source.** **ISCE2/ISCE3** (NASA JPL): full InSAR processing for most sensors including Sentinel-1 TOPS and NISAR. **GMTSAR**: InSAR on GMT, good for batch work and teaching. **ESA SNAP** (S1TBX): graphical InSAR and DEM generation. **SNAPHU**: the standard statistical-cost unwrapper. **MintPy**, **LiCSBAS**, **PyRate**: SBAS inversion, each estimating the DEM-error term. **StaMPS** (MATLAB): PSI for natural terrain. **ASF HyP3**: on-demand Sentinel-1 RTC and InSAR with the DEM named in metadata. **xdem**: co-registration and differencing for validation. **GMT**: altimetry and gravity grids (`grdfft`, `gravfft`). **OpenPolarRadar** (CReSIS toolbox lineage): radio-echo-sounding processing and picking.

**Commercial.** **GAMMA** (GAMMA Remote Sensing): the reference implementation for operational InSAR, used for TanDEM-X and many national DEM productions; command-line, modular. **SARscape** (NV5/L3Harris): integrated InSAR, PSI/SBAS, and radargrammetry in ENVI. **SARPROZ**: PSI with a graphical workflow. **IDS IBIS Guardian**, **GroundProbe SSR-Viewer**: ground-based radar monitoring with alarms.

## Standards & guides

- **TanDEM-X DEM Product Specification** (DLR, TD-GS-PS-0021, issue 3.x (verify)): DEM, HEM, COM, COV, AMP, and WAM layers, accuracy requirements, tiling.
- **Copernicus DEM Product Handbook** (Airbus / ESA, current issue (verify)): GLO-30/GLO-90/EEA-10 editing rules, auxiliary layers (EDM, FLM, HEM, WBM), accuracy statements.
- **SRTM / NASADEM user guides** (NASA JPL and LP DAAC, 2003–2020): format, void handling, known artefacts, geoid reference (EGM96).
- **CEOS Analysis Ready Data for Land — Normalised Radar Backscatter and Polarimetric Radar (CARD4L NRB/POL), v5.5 (2022), and the CEOS-ARD framework (2023–)**: metadata requirements including the geocoding/RTC DEM and per-pixel masks.
- **ESA Sentinel-1 Product Specification and SAR User Guide**: acquisition modes, TOPS geometry, orbit products.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)**: the vocabulary (NVA/VVA, RMSE, 95 %) for reporting InSAR DEM accuracy.
- **ISO 19157-1:2023 Geographic information — Data quality**: quality elements for reporting.

## Pitfalls

- **Reading an X- or C-band InSAR height over forest or snow as the ground.** The phase centre sits inside the canopy or firn; the DEM is DSM-minus-penetration. Detect by stratifying residuals against lidar or ICESat-2 by land cover; label the surface and apply a documented penetration correction, or use a lidar DTM where one exists.
- **Treating filled layover, shadow, and water voids as measurements.** Editing fills them from other sources or interpolation and the result looks continuous. Check the mask layers, report the filled fraction, and never derive slope or hydrology inside filled areas without saying so.
- **Mistaking 2π unwrapping errors for terraces or cliffs.** They are sharp steps of constant height $h_{\mathrm{amb}}$. Look for secondary residual modes at ± $h_{\mathrm{amb}}$ and for repeating step heights.
- **Converting a single repeat-pass interferogram to an absolute DEM.** The atmosphere adds tens of metres through the $h_{\mathrm{amb}}/\lambda$ scaling. Use single-pass products or many-interferogram stacks with independent control; otherwise call it a relative height map.
- **Reading tropospheric or ionospheric phase as deformation (or topography).** The APS mimics both. Test for correlation with elevation (stratified troposphere), with time of day and solar activity (ionosphere, especially L-band), and across independent pairs.
- **Geocoding SAR with a DEM derived from the same SAR, then "validating" the DEM with that product.** The agreement is circular. Record the geocoding DEM in metadata (CEOS-ARD requires it) and validate only against independent sources.
- **Comparing heights in the wrong vertical reference.** SRTM is EGM96, Copernicus DEM is EGM2008, TanDEM-X raw DEM and ICESat-2 are WGS84 ellipsoidal. Metre-level "errors" are often just the geoid model ([Chapter 9](ch09-vertical-datums.md)).
- **Trusting the height-error layer as a total uncertainty.** It describes phase noise only, not unwrapping, penetration, or calibration error. Compare it with empirical residuals before using it to weight a composite.
- **Using sub-ice bed DEMs without their error grids.** Bedmap and BedMachine interpolate across hundreds of kilometres in places; the smoothness is the interpolator's. Read the uncertainty and source-distance layers and the data-coverage maps.
- **Differencing radar DEMs of different bands or seasons over firn or forest as if penetration cancelled.** It does not; the bias depends on wavelength, $h_{\mathrm{amb}}$, and snow state. Difference like against like, or correct explicitly.

## Key takeaways

- Radar works through cloud and darkness and measures a wavelength-dependent scattering surface: canopy top at X-band, mid-canopy at C-band, near-ground at L/P-band; metres below the surface in dry firn and sand.
- Side-looking geometry guarantees foreshortening, layover, and shadow in steep terrain; global products mask these and fill them, and the masks are part of the product.
- The height of ambiguity $h_{\mathrm{amb}} = \lambda R\sin\theta/(p B_\perp)$ scales every phase error into height; state the $p$ convention and the baseline when quoting it.
- Coherence sets the random height error through $\sigma_h = (h_{\mathrm{amb}}/2\pi)\,\sigma_\phi(\gamma, N)$; unwrapping, penetration, and calibration errors are additional and are not in the height-error layer.
- Single-pass systems (SRTM, TanDEM-X, SWOT) have no temporal decorrelation and no atmospheric phase screen; repeat-pass systems do, and a single repeat-pass interferogram is not a DEM.
- DInSAR time series both depend on a DEM and refine it; residual DEM error appears as a baseline-proportional phase that PSI and SBAS estimate.
- Geocoding and radiometric terrain correction need a DEM, and products inherit its errors; track the lineage to avoid circular validation.
- Radar altimetry gives centimetre sea-surface heights whose slopes become marine gravity and then predicted bathymetry with kilometres of resolution and hundreds of metres of local uncertainty.
- Radio-echo-sounding bed DEMs are sparse-track interpolations (or mass-conservation inversions) with per-cell uncertainties from tens to a thousand metres; read the error layer.
- Validate radar DEMs against independent lidar, ICESat-2, or GNSS, stratified by slope and land cover, after horizontal co-registration and with the product's own masks applied and reported.

## References

- Abdullahi, S., Wessel, B., Huber, M., Wendleder, A., Roth, A., & Kuenzer, C. (2019). Estimating penetration-related X-band InSAR elevation bias: A study over the Greenland Ice Sheet. *Remote Sensing*, 11(24):2903.
- Bamler, R., & Hartl, P. (1998). Synthetic aperture radar interferometry. *Inverse Problems*, 14(4):R1–R54.
- Berardino, P., Fornaro, G., Lanari, R., & Sansosti, E. (2002). A new algorithm for surface deformation monitoring based on small baseline differential SAR interferograms. *IEEE Transactions on Geoscience and Remote Sensing*, 40(11):2375–2383.
- Bürgmann, R., Rosen, P. A., & Fielding, E. J. (2000). Synthetic aperture radar interferometry to measure Earth's surface topography and its deformation. *Annual Review of Earth and Planetary Sciences*, 28:169–209.
- Carabajal, C. C., & Harding, D. J. (2006). SRTM C-band and ICESat laser altimetry elevation comparisons as a function of tree cover and relief. *Photogrammetric Engineering & Remote Sensing*, 72(3):287–298.
- Chelton, D. B., Ries, J. C., Haines, B. J., Fu, L.-L., & Callahan, P. S. (2001). Satellite altimetry. In Fu, L.-L., & Cazenave, A. (eds.), *Satellite Altimetry and Earth Sciences*, Academic Press, pp. 1–131.
- Chen, C. W., & Zebker, H. A. (2001). Two-dimensional phase unwrapping with use of statistical models for cost functions in nonlinear optimization. *Journal of the Optical Society of America A*, 18(2):338–351.
- Costantini, M. (1998). A novel phase unwrapping method based on network programming. *IEEE Transactions on Geoscience and Remote Sensing*, 36(3):813–821.
- Cumming, I. G., & Wong, F. H. (2005). *Digital Processing of Synthetic Aperture Radar Data: Algorithms and Implementation*. Artech House.
- Dall, J. (2007). InSAR elevation bias caused by penetration into uniform volumes. *IEEE Transactions on Geoscience and Remote Sensing*, 45(7):2319–2324.
- Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., et al. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics*, 45:RG2004.
- Ferretti, A., Prati, C., & Rocca, F. (2001). Permanent scatterers in SAR interferometry. *IEEE Transactions on Geoscience and Remote Sensing*, 39(1):8–20.
- Fretwell, P., Pritchard, H. D., Vaughan, D. G., Bamber, J. L., Barrand, N. E., Bell, R., et al. (2013). Bedmap2: improved ice bed, surface and thickness datasets for Antarctica. *The Cryosphere*, 7:375–393.
- Fu, L.-L., & Cazenave, A. (eds.) (2001). *Satellite Altimetry and Earth Sciences: A Handbook of Techniques and Applications*. Academic Press.
- Fu, L.-L., Pavelsky, T., Cretaux, J.-F., Morrow, R., Farrar, J. T., Vaze, P., et al. (2024). The Surface Water and Ocean Topography Mission: A breakthrough in radar remote sensing of the ocean and land surface water. *Geophysical Research Letters*, 51:e2023GL107652.
- Goldstein, R. M., & Werner, C. L. (1998). Radar interferogram filtering for geophysical applications. *Geophysical Research Letters*, 25(21):4035–4038.
- Goldstein, R. M., Zebker, H. A., & Werner, C. L. (1988). Satellite radar interferometry: Two-dimensional phase unwrapping. *Radio Science*, 23(4):713–720.
- Hanssen, R. F. (2001). *Radar Interferometry: Data Interpretation and Error Analysis*. Kluwer Academic Publishers.
- Hoen, E. W., & Zebker, H. A. (2000). Penetration depths inferred from interferometric volume decorrelation observed over the Greenland Ice Sheet. *IEEE Transactions on Geoscience and Remote Sensing*, 38(6):2571–2583.
- Hooper, A., Zebker, H., Segall, P., & Kampes, B. (2004). A new method for measuring deformation on volcanoes and other natural terrains using InSAR persistent scatterers. *Geophysical Research Letters*, 31:L23611.
- Krieger, G., Moreira, A., Fiedler, H., Hajnsek, I., Werner, M., Younis, M., & Zink, M. (2007). TanDEM-X: A satellite formation for high-resolution SAR interferometry. *IEEE Transactions on Geoscience and Remote Sensing*, 45(11):3317–3341.
- Leberl, F. W. (1990). *Radargrammetric Image Processing*. Artech House.
- Massonnet, D., & Feigl, K. L. (1998). Radar interferometry and its application to changes in the Earth's surface. *Reviews of Geophysics*, 36(4):441–500.
- Massonnet, D., Rossi, M., Carmona, C., Adragna, F., Peltzer, G., Feigl, K., & Rabaute, T. (1993). The displacement field of the Landers earthquake mapped by radar interferometry. *Nature*, 364:138–142.
- McCauley, J. F., Schaber, G. G., Breed, C. S., Grolier, M. J., Haynes, C. V., Issawi, B., Elachi, C., & Blom, R. (1982). Subsurface valleys and geoarcheology of the eastern Sahara revealed by Shuttle radar. *Science*, 218(4576):1004–1020.
- Monserrat, O., Crosetto, M., & Luzi, G. (2014). A review of ground-based SAR interferometry for deformation measurement. *ISPRS Journal of Photogrammetry and Remote Sensing*, 93:40–48.
- Moreira, A., Prats-Iraola, P., Younis, M., Krieger, G., Hajnsek, I., & Papathanassiou, K. P. (2013). A tutorial on synthetic aperture radar. *IEEE Geoscience and Remote Sensing Magazine*, 1(1):6–43.
- Morlighem, M., Williams, C. N., Rignot, E., An, L., Arndt, J. E., Bamber, J. L., et al. (2017). BedMachine v3: Complete bed topography and ocean bathymetry mapping of Greenland from multibeam echo sounding combined with mass conservation. *Geophysical Research Letters*, 44(21):11,051–11,061.
- Morlighem, M., Rignot, E., Binder, T., Blankenship, D., Drews, R., Eagles, G., et al. (2020). Deep glacial troughs and stabilizing ridges unveiled beneath the margins of the Antarctic ice sheet. *Nature Geoscience*, 13:132–137.
- Noferini, L., Pieraccini, M., Mecatti, D., Luzi, G., Atzeni, C., Tamburini, A., & Broccolato, M. (2005). Permanent scatterers analysis for atmospheric correction in ground-based SAR interferometry. *IEEE Transactions on Geoscience and Remote Sensing*, 43(7):1459–1471.
- Nuth, C., & Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5:271–290.
- Pritchard, H. D., Fretwell, P. T., Fremand, A. C., Bodart, J. A., Kirkham, J. D., Aitken, A., et al. (2025). Bedmap3 updated ice bed, surface and thickness gridded datasets for Antarctica. *Scientific Data*, 12:414.
- Quegan, S., Le Toan, T., Chave, J., Dall, J., Exbrayat, J.-F., Ho Tong Minh, D., et al. (2019). The European Space Agency BIOMASS mission: Measuring forest above-ground biomass from space. *Remote Sensing of Environment*, 227:44–60.
- Rizzoli, P., Martone, M., Gonzalez, C., Wecklich, C., Borla Tridon, D., Bräutigam, B., et al. (2017). Generation and performance assessment of the global TanDEM-X digital elevation model. *ISPRS Journal of Photogrammetry and Remote Sensing*, 132:119–139.
- Rodríguez, E., & Martin, J. M. (1992). Theory and design of interferometric synthetic aperture radars. *IEE Proceedings F — Radar and Signal Processing*, 139(2):147–159.
- Rodríguez, E., Morris, C. S., & Belz, J. E. (2006). A global assessment of the SRTM performance. *Photogrammetric Engineering & Remote Sensing*, 72(3):249–260.
- Rosen, P. A., Hensley, S., Joughin, I. R., Li, F. K., Madsen, S. N., Rodríguez, E., & Goldstein, R. M. (2000). Synthetic aperture radar interferometry. *Proceedings of the IEEE*, 88(3):333–382.
- Sandwell, D. T., Müller, R. D., Smith, W. H. F., Garcia, E., & Francis, R. (2014). New global marine gravity model from CryoSat-2 and Jason-1 reveals buried tectonic structure. *Science*, 346(6205):65–67.
- Small, D. (2011). Flattening gamma: Radiometric terrain correction for SAR imagery. *IEEE Transactions on Geoscience and Remote Sensing*, 49(8):3081–3093.
- Smith, W. H. F., & Sandwell, D. T. (1994). Bathymetric prediction from dense satellite altimetry and sparse shipboard bathymetry. *Journal of Geophysical Research*, 99(B11):21803–21824.
- Smith, W. H. F., & Sandwell, D. T. (1997). Global sea floor topography from satellite altimetry and ship depth soundings. *Science*, 277(5334):1956–1962.
- Strozzi, T., Luckman, A., Murray, T., Wegmüller, U., & Werner, C. L. (2002). Glacier motion estimation using SAR offset-tracking procedures. *IEEE Transactions on Geoscience and Remote Sensing*, 40(11):2384–2391.
- Toutin, T. (2010). Impact of Radarsat-2 SAR ultrafine-mode parameters on stereo-radargrammetric DEMs. *IEEE Transactions on Geoscience and Remote Sensing*, 48(10):3816–3823.
- Toutin, T., & Gray, L. (2000). State-of-the-art of elevation extraction from satellite SAR data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 55(1):13–33.
- Wessel, B., Huber, M., Wohlfart, C., Marschalk, U., Kosmann, D., & Roth, A. (2018). Accuracy assessment of the global TanDEM-X Digital Elevation Model with GPS data. *ISPRS Journal of Photogrammetry and Remote Sensing*, 139:171–182.
- Wingham, D. J., Francis, C. R., Baker, S., Bouzinac, C., Brockley, D., Cullen, R., et al. (2006). CryoSat: A mission to determine the fluctuations in Earth's land and marine ice fields. *Advances in Space Research*, 37(4):841–871.
- Yamazaki, D., Ikeshima, D., Tawatari, R., Yamaguchi, T., O'Loughlin, F., Neal, J. C., Sampson, C. C., Kanae, S., & Bates, P. D. (2017). A high-accuracy map of global terrain elevations. *Geophysical Research Letters*, 44(11):5844–5853.
- Zebker, H. A., & Goldstein, R. M. (1986). Topographic mapping from interferometric synthetic aperture radar observations. *Journal of Geophysical Research*, 91(B5):4993–4999.
- Zebker, H. A., & Villasenor, J. (1992). Decorrelation in interferometric radar echoes. *IEEE Transactions on Geoscience and Remote Sensing*, 30(5):950–959.

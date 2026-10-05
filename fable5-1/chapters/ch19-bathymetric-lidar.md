# Chapter 19 — Bathymetric lidar and the land–water transition

> **Part V — Sensors and platforms.** Between the topographic lidar of [Chapter 18](ch18-topographic-lidar.md) and the sonar of [Chapter 20](ch20-sonar.md) lies the shallow, often turbulent strip that neither measures well; this chapter covers the green-laser systems built for it and the spaceborne photons that now reach it.

**In this chapter.** Airborne laser bathymetry (ALB) sends a green (532 nm) pulse through the air–water interface and into the water column, and recovers depth from the time between the surface and bottom echoes after correcting for the change in speed and direction at the surface. You will be able to explain why green works and near-infrared does not, how Secchi depth and the diffuse attenuation coefficient $K_d$ bound the achievable depth (roughly 1.5–3 Secchi depths depending on the system), what a water-surface model is and why its error becomes a depth error, how to apply the refraction correction and propagate its uncertainty into a depth-dependent TVU, and how turbidity, sea state, surf, and bottom albedo produce gaps and biases. You will be able to place the operational systems (CZMIL, Chiroptera/HawkEye, Riegl VQ-880-G and VQ-840-G, RAMMS, EAARL, UAV systems) and ICESat-2's photon-counting bathymetry in that framework, compare bathymetric with topographic lidar and with sonar on depth range, coverage rate, cost, and environment, and understand the "white ribbon" — the nearshore gap between hydrographic and topographic surveys — that these systems exist to close.

## 19.1 Physics: green light in water

Pure water's absorption is lowest in the blue (about 0.005 m⁻¹ near 420 nm) and still small at 532 nm (about 0.045 m⁻¹; Pope & Fry 1997), then rises steeply into the red and near-infrared, exceeding 10 m⁻¹ at 1,064 nm ([Chapter 17](ch17-measurement-physics.md)); doubled, frequency-stabilised Nd:YAG lasers at 532 nm therefore sit near the transmission window, and the same laser can supply a 1,064 nm channel for topography. In natural waters the attenuation is dominated not by pure-water absorption but by dissolved organic matter, phytoplankton, and suspended sediment, all of which absorb and scatter. The quantity that governs lidar performance is the **diffuse attenuation coefficient** $K_d$ (m⁻¹), the exponential decay rate of downwelling irradiance with depth, which ranges from about 0.03–0.1 m⁻¹ in clear oceanic water, 0.1–0.5 m⁻¹ in coastal water, to more than 1 m⁻¹ in turbid estuaries. The **Secchi depth** $Z_{sd}$ — the depth at which a white disk disappears — is the field proxy; empirically $K_d \approx 1.4$–$1.7 / Z_{sd}$ for the green band, with considerable scatter.

A lidar pulse entering the water is attenuated on the way down and on the way back, so the bottom-return power falls roughly as $\exp(-2\,k_{\text{sys}}\,z)$, where the **system attenuation coefficient** $k_{\text{sys}}$ lies between the beam attenuation coefficient $c$ (for narrow receiver fields of view that reject scattered light) and $K_d$ (for wide fields that collect it); bathymetric receivers use wide fields of view precisely to collect the forward-scattered light and approach $K_d$. The maximum detectable depth is where the bottom return falls to the detection threshold against the noise from the water-column backscatter, the surface return, and daylight; the achievable **maximum depth** is conventionally quoted as a multiple of Secchi depth — roughly 1–1.5 $Z_{sd}$ for compact, high-PRF "topobathy" systems with microjoule-class pulses, and 2–3 $Z_{sd}$ for high-energy (millijoule-class), lower-PRF "deep" channels — or equivalently about $(10$–$15)/K_d$ for the latter (Guenther 1985; Guenther et al. 2000; Mandlburger 2022). In 10 m Secchi water that is 10–15 m for a topobathy sensor and 20–30 m for a deep channel; in the clearest reef and lake waters (Secchi 25–40 m) deep channels reach 50–70 m; in a turbid estuary with 1 m Secchi, nothing below 1.5–3 m.

<!-- figure: Figure 19.1 — A bathymetric lidar waveform annotated: surface return (specular plus volume), exponentially decaying water-column backscatter, bottom return, and noise floor; a second panel shows how the bottom peak sinks into the column backscatter as depth increases toward the Secchi-depth limit, for Kd = 0.1 and 0.3 m⁻¹. -->

**Water-surface detection** is the first measurement and the one that controls everything downstream. The surface return comes from two sources: specular (Fresnel) reflection, strong near nadir and weak at 15–20° off nadir, and volume backscatter from the top decimetres of water and the air–water interface, including foam. Because the green surface return is weak and biased downward by the volume contribution, systems with a co-aligned **near-infrared channel** (1,064 nm, which returns from the surface and does not penetrate) use it to locate the surface, and some add a red channel or a Raman channel (the 532 nm beam excites water Raman scattering at about 645 nm, a signature that arises only within the water) for the same purpose. Waves complicate matters: the instantaneous local surface is tilted and displaced by the wave field, and a **water-surface model** — a smooth surface fitted to many surface returns over a patch of tens of metres, or the per-pulse surface where it is reliable — is what the refraction correction uses. Error in that model propagates directly into depth (Section 19.3).

**Refraction** changes both the speed and the direction of the pulse at the surface. With $n_w \approx 1.34$ for seawater at 532 nm (temperature- and salinity-dependent at the third decimal; Quan & Fry 1995), the in-water speed is $c/n_w$, so the slant distance below the surface is $s = c\,\tau_w / (2 n_w)$ for in-water two-way time $\tau_w$, and the ray bends toward the vertical by Snell's law. The depth is $z = s\cos\theta_w$ and the horizontal displacement of the bottom point from the surface entry point is $s\sin\theta_w$ along the scan direction. Neglecting refraction overstates depth by about 30 % and misplaces the bottom point by decimetres to metres ([Chapter 17](ch17-measurement-physics.md); full formulas in the Mathematics section). Most systems scan at a fixed off-nadir angle of about 15–20° (circular, elliptical, or Palmer patterns) to avoid the blinding specular return at nadir and to keep the geometry constant across the swath.

**Bottom-return detection, turbidity, sea state, and albedo** determine whether a depth is obtained and how good it is. The bottom return is the convolution of the pulse (stretched by its passage through a scattering medium) with the bottom within a footprint that has grown by scattering to a metre or more; it sits on the exponentially decaying water-column backscatter and must be extracted by waveform processing (Gaussian or exponential-plus-Gaussian decomposition, deconvolution, or matched filtering). Three failure modes follow. In **turbid water** the column backscatter is strong and the bottom weak: beyond the attenuation limit no bottom is found, and — more dangerously — a strong scattering layer, a thermocline of particles, or dense seagrass can be detected as a false bottom above the true one. In the **surf zone** entrained air scatters the pulse before it reaches the bottom and the surface is foam, so the strip of breaking waves is typically a gap in every ALB dataset. **Bottom albedo** at 532 nm ranges from about 5 % for dark mud or basalt to 40–60 % for coral sand, a factor of ten in return power, equivalent to roughly one Secchi depth of range: a system reaching 25 m over sand may reach 15 m over seagrass beside it. Sea state raises the surface-model error, increases foam, and — at the wavelength-scale roughness of capillary waves — scatters the beam entering the water.

## 19.2 Systems

ALB has a sixty-year history (see Then & now); the operational systems of the 2020s fall into a few families.

| System (manufacturer) | Channels | Bathy PRF | Nominal depth capability | Typical altitude / swath | Notes |
|---|---|---|---|---|---|
| CZMIL SuperNova (Teledyne Optech) | 532 nm deep + shallow, 1,064 nm topo, RGB/hyperspectral camera | 10 kHz (deep) / higher shallow segments | ≈ 3 Secchi (deep channel); shallow channel ~1.5–2 | 400–600 m / ~300 m circular 20° | USACE NCMP workhorse; large deep-channel footprint (≈ 2 m) |
| Leica Chiroptera 4X / 5 | 532 nm bathy + 1,064 nm topo | ≈ 140 kHz bathy | ≈ 1.5 Secchi | 400–600 m / elliptical scan | topobathy class; HawkEye adds a deep channel |
| Leica HawkEye 4X / 5 | Chiroptera + 532 nm deep channel | 10 kHz deep | ≈ 3 Secchi (deep) | 400–600 m | dual-mode system |
| Riegl VQ-880-G / -GII | 532 nm bathy, optional 1,064 nm | 200–700 kHz | ≈ 1.5 Secchi | 400–600 m / circular 20° | high density, shallow water and rivers |
| Riegl VQ-840-G / -GL | 532 nm compact | 50–200 kHz | ≈ 1.7–2.0 Secchi (rate-dependent) | 50–150 m (UAV) to 600 m | UAV- and helicopter-capable |
| Fugro RAMMS | 532 nm push-broom with multiple beams | — | ≈ 3 Secchi (claimed) | ~400 m | compact, 2017 onward; operational details proprietary |
| ASTRALiTe edge | 532 nm polarimetric | — | very shallow (< ~5 m) | UAV, < 100 m | surface/bottom separation by polarisation |
| EAARL / EAARL-B (NASA/USGS) | 532 nm small-footprint full waveform | 3–5 kHz raster | ≈ 1.5 Secchi; also sub-canopy topo | 300 m | research system 2001–2014 (Nayegandhi et al. 2009) |

Nominal depth capabilities are manufacturers' statements under stated conditions and should be treated as such (verify against current product specifications). The structural distinction is between **topobathy** systems — a single green channel at high PRF with small footprint and low pulse energy, giving dense (5–20 pts/m²) coverage of the beach, the intertidal, and water to 1–2 Secchi depths, plus a NIR channel for land and surface — and **bathy-only or deep-channel** systems that fire millijoule pulses at 10 kHz through a wide-field receiver to reach 2–3 Secchi depths at 1–2 pts/m² with 2 m footprints. Dual-mode systems (CZMIL, HawkEye) combine both. Multi-wavelength topographic scanners with a green channel (Teledyne Optech Titan, with 532/1,064/1,550 nm) demonstrated simultaneous terrain and shallow bathymetry (Fernandez-Diaz et al. 2014) and sit at the shallow end. **UAV bathymetric lidar** (Riegl VQ-840-G, ASTRALiTe, YellowScan Navigator) brings the technique to rivers, lakes, and short coastal reaches at 50–150 m altitude with swaths of tens of metres, where its advantages are density and access rather than depth.

> **Definitions that bite.** "Depth" in an ALB deliverable may be referenced to the instantaneous water surface (the raw measurement), to the ellipsoid (what the trajectory gives), to an orthometric datum via a geoid, or to a tidal datum via a separation model — and a topobathy LAS commonly mixes land points in NAVD88 with bathy points that someone has reduced to MLLW. The S-44 TVU applies to the reduced depth and includes the water-level and datum terms; a TVU quoted for ellipsoidal bottom elevations is a different and smaller number. Make the deliverable state one vertical reference for all points and carry the separation model as metadata ([Chapter 9](ch09-vertical-datums.md)).

## 19.3 Total propagated uncertainty for bathymetric lidar

The airborne-lidar error budget of [Chapter 18](ch18-topographic-lidar.md) — trajectory, attitude × range, boresight, lever arm, range — applies to every ALB point down to the water surface. Below the surface four additional terms appear, and they dominate in all but the shallowest water.

**Water-surface model error.** The refraction correction is applied at the modelled surface, so an error $\delta z_s$ in the surface height enters the depth twice with opposite signs of effect on the bottom elevation: the bottom's ellipsoidal height depends on where the ray was bent and slowed. For near-nadir geometry the bottom-height error is approximately $(1 - 1/n_w)\,\delta z_s \approx 0.25\,\delta z_s$ — a 0.4 m surface error (a wave) becomes a 0.1 m bottom error — while the *depth* (bottom relative to surface) error is close to $\delta z_s$ itself if the instantaneous surface is used as the depth reference. A surface *slope* error $\delta\alpha$ (wave tilt) changes the refracted angle and displaces the bottom point horizontally by about $z\,\delta\alpha\,(1 - 1/n_w)$ and vertically by a second-order amount; at 20° incidence and a 5° wave slope the horizontal shift in 20 m of water is of the order of 0.4 m. Surface models that average over a wave-scale patch suppress the random part at the cost of a small bias in long swell (Westfeld et al. 2017).

**Refraction-model error.** With the surface known, the remaining uncertainty is in $n_w$ (± 0.002 between fresh and sea water and over temperature, i.e. ± 0.15 % of depth) and in the incidence angle (attitude error, ~0.005° → negligible). A system that assumes seawater over a freshwater lake biases depths by about 0.5 %.

**Pulse-stretching and bottom-detection bias.** Scattering in the column lengthens the pulse and the footprint, so the detected bottom time is biased toward the near (shallow) edge of the footprint and the detection point on a stretched waveform depends on the algorithm; the bias grows with depth and turbidity and is of the order of 0.1–0.3 m at the depth limit. Bottom slope within the footprint adds a term $D\tan\alpha/2$ as in topographic lidar, with $D$ now 1–3 m. Dense vegetation or a fluid-mud layer adds a "which bottom" ambiguity of decimetres ([Chapter 17](ch17-measurement-physics.md)).

**Water level and datum.** If the deliverable is a reduced depth or a chart-datum elevation, the water-level observation or model and the ellipsoid–datum separation enter exactly as for sonar ([Chapter 20](ch20-sonar.md), [Chapter 9](ch09-vertical-datums.md)); ALB's advantage is that the trajectory gives ellipsoidal heights for both surface and bottom directly, so an **ellipsoidally referenced** product avoids the tide term entirely and defers the datum choice to the user.

> **Uncertainty budget.** Vertical uncertainty of an ALB bottom elevation (1σ, m) for a topobathy system at 500 m AGL, 20° incidence, in moderate conditions. The depth-dependent terms are given at 5 m and 20 m.
>
> | Component | 5 m depth | 20 m depth | Nature |
> |---|---|---|---|
> | Trajectory + attitude × range + boresight (as topo lidar) | 0.06 | 0.06 | additive |
> | Water-surface model (0.2 m wave residual → × 0.25) | 0.05 | 0.05 | additive; sea-state dependent |
> | Refractive index (± 0.15 % of depth) | 0.01 | 0.03 | scale |
> | Pulse stretching / detection bias | 0.03 | 0.12 | grows with depth × turbidity |
> | Bottom slope within footprint (D = 1.5 m, 10° slope) | 0.07 | 0.09 | footprint grows with depth |
> | Combined (ellipsoidal bottom height) | ≈ 0.11 | ≈ 0.17 | |
> | Water level + datum separation (if reduced to chart datum) | 0.05–0.10 | 0.05–0.10 | systematic per area |
> | Combined (reduced depth) | ≈ 0.12–0.15 | ≈ 0.18–0.20 | compare S-44 Order 1a TVU: 0.50 m at 5 m, 0.56 m at 20 m |
>
> Both columns are comfortably inside S-44 Order 1a and often inside Special Order (0.26 m at 5 m, 0.29 m at 20 m) in clear water; in turbid or rough conditions the surface and detection terms double or triple, and the budget — not the specification — should decide whether a point is delivered.

## 19.4 Processing and deliverables

The ALB processing chain runs: trajectory (PPK/PPP + IMU, [Chapter 12](ch12-gnss.md), [Chapter 13](ch13-imu-ins.md)) → calibration (boresight on land features as for topographic lidar, plus a range/refraction check over a surveyed flat bottom) → **waveform decomposition** of every green pulse into surface, column, bottom, and noise components (vendor algorithms; Gaussian mixtures or exponentially modified Gaussians; deconvolution for shallow water where surface and bottom returns merge below ~1 m) → **surface/bottom classification**, assigning each return to water surface, bottom, land, submerged object, or noise, with the NIR channel and the surface model as arbiters → **water-surface modelling** per patch → **refraction correction** of each bottom return through the model → **TPU** per point from the budget of Section 19.3 → **cleaning** (manual and statistical removal of false bottoms, fish, column noise, surf) → products.

Shallow water below about 1–1.5 m is the hard case in the other direction: the surface and bottom returns overlap in time and the pulse's length (1–2 ns, 0.2–0.3 m in water) limits separation; deconvolution and high-PRF small-footprint systems have pushed the minimum depth to 0.2–0.5 m, and the NIR channel measures the exposed beach to the waterline, so the intertidal zone is covered by the two channels together if the tide is right. A gap between the last NIR land return and the first resolved green bottom is common and must be declared, not interpolated.

**Deliverables** follow the LAS 1.4 **Topo-Bathy Lidar Domain Profile** (ASPRS 2013): bathymetric bottom = class 40, water surface = 41, derived water surface = 42, submerged object = 43, IHO S-57 object = 44, no-bottom-found-at = 45, with the refraction-corrected coordinates stored and the uncorrected ones recoverable from extra bytes; a DEM (land + bottom) in GeoTIFF/COG; a **BAG** with its uncertainty layer where the product feeds hydrographic use ([Chapter 47](ch47-file-formats.md)); the water-surface model; per-point TPU; and the project report with Secchi/turbidity observations, sea state, tide, and the depth-capability actually achieved. Class 45 ("no bottom found at") is the honest record of where the laser penetrated to a known depth without finding the bottom — it tells the user that the water is *at least* that deep there, which is more information than a void and much more than an interpolated surface.

> **Try it.** Apply a first-order refraction correction to a bathymetric point cloud whose bottom returns were computed as if in air (a common state of raw exports), using PDAL with a Python filter. The input carries an estimated water-surface height per point (`WaterSurface`), the scan angle, and class 40 bottom points.
>
> ```python
> # refract.py — used by: pdal translate in.laz out.laz python --filters.python.script=refract.py \
> #   --filters.python.function=refract --filters.python.module=refract
> import numpy as np
> N_W = 1.34
> def refract(ins, outs):
>     cls = ins["Classification"]; sa = np.deg2rad(np.abs(ins["ScanAngleRank"].astype(float)))
>     z = ins["Z"].astype(float); zs = ins["WaterSurface"].astype(float)
>     bottom = (cls == 40) & (z < zs)
>     s_air = (zs[bottom] - z[bottom]) / np.cos(sa[bottom])     # slant distance computed as if in air
>     th_w = np.arcsin(np.sin(sa[bottom]) / N_W)
>     s_w = s_air / N_W                                         # true in-water slant distance
>     dz = s_w * np.cos(th_w)                                   # true depth below surface
>     dh = s_air * np.sin(sa[bottom]) - s_w * np.sin(th_w)      # horizontal pull-back toward nadir
>     z[bottom] = zs[bottom] - dz
>     # horizontal correction applied along the scan direction (cross-track unit vector assumed +Y here)
>     y = ins["Y"].astype(float); y[bottom] -= np.sign(ins["ScanAngleRank"][bottom]) * dh
>     outs["Z"] = z; outs["Y"] = y
>     return True
> ```
>
> Expected: for a point at 20° scan angle and 10.0 m apparent depth, the corrected depth is 7.68 m and the horizontal shift about 1.6 m toward nadir. (The real correction uses the per-pulse ray direction and the local surface normal; this script shows the magnitude and sign.)

## 19.5 Spaceborne photon-counting bathymetry

ICESat-2's ATLAS fires 532 nm — the bathymetric wavelength — and its single-photon detectors register the few photons that return from a shallow seabed. Parrish et al. (2019) showed that ATL03 photon clouds over clear water contain a resolvable bottom to depths approaching 40 m (Secchi-limited, nearly one Secchi depth in their analysis), and that after a refraction correction (the photons' geolocation assumes propagation in air) and comparison with airborne bathymetric lidar the agreement is 0.43–0.60 m RMSE across their sites. The correction is the same Snell geometry as airborne ALB with the difference that ICESat-2 looks within about 0.5° of nadir, so the depth correction is nearly a pure scale factor, $z \approx z_{\text{apparent}}/n_w$, plus a small horizontal term; the water-surface height is taken from the dense surface photons in the same track; and the sea-surface and bottom photons must be separated from noise by density-based classification, since there is no waveform. Tools for this — SlideRule, `icepyx`, OpenAltimetry for discovery, and open bathymetry-specific classifiers — have matured since 2019.

The product is sparse: six profiles per pass, each a line of bottom photons with along-track spacing of decimetres, repeating every 91 days on the reference tracks (with off-pointing campaigns adding more). Its value lies in three uses. First, as **independent truth** for satellite-derived bathymetry ([Chapter 23](ch23-satellite-derived-bathymetry.md)) — ICESat-2 depths calibrate and validate the band-ratio inversion over reefs and shelves where no ship or ALB survey exists, and this combination has become the standard way to map remote shallow seas. Second, as a **check on charted depths** in poorly surveyed regions, where metre-level ICESat-2 depths reveal charts off by much more. Third, as a **reconnaissance of water clarity**: whether a bottom appears, and how deep, measures the local Secchi depth before an ALB campaign is mobilised. ICESat-2 does not replace ALB; it finds where ALB will work and tells you what to expect from it.

## 19.6 Bathymetric lidar versus topographic lidar versus sonar

The three sensors overlap only at the shoreline, and the comparison explains why coastal mapping needs all of them.

| Property | Topographic lidar (1,064/1,550 nm) | Bathymetric lidar (532 nm) | Multibeam / single-beam sonar |
|---|---|---|---|
| Medium | air only; water is a void | air and water to ~1.5–3 Secchi depths | water only; cannot work in < ~1–2 m or in surf |
| Pulse energy / PRF | µJ; 0.5–2+ MHz | µJ (topobathy) to mJ (deep); 10–700 kHz | — |
| Footprint | 0.2–0.5 m | 0.5–3 m (scattering-widened) | 0.5–2 % of depth |
| Vertical accuracy (open/clear) | 5–10 cm | 10–30 cm, depth- and clarity-dependent | 10–30 cm shallow; 0.2–0.5 % of depth deep |
| Coverage rate | 200–1,000 km²/day | 100–300 km²/day (slower, lower altitude, overlap) | 5–50 km²/day shallow launch; swath ~3–5 × depth |
| Cost per km² (indicative, mid-2020s) | lowest | 2–5 × topo lidar | 10–100 × bathy lidar in shallow water; cheaper in deep water per km² |
| Environment | any dry land; leaf-off for DTM | clear water, calm sea, no surf; reefs, rivers, lakes, sandy shelves | any water deep enough to float the vessel; turbid water fine; surf and reef flats not |
| Depth limit | 0 | ~1.5–3 Secchi (practically 0.5–50 m) | unlimited |
| Hazard detection | n/a | footprint-limited; small objects < 1 m may be missed | full ensonification feasible (S-44 feature detection) |
| Sub-bottom / fluid mud | n/a | reads top of mud/vegetation | dual-frequency reads top and consolidated bottom |

The **white ribbon** is the strip the table exposes: hydrographic sonar surveys stop where the launch cannot safely go (roughly the 5–10 m contour, farther offshore on reef and surf coasts), topographic lidar stops at the waterline, and between them lies a 0–10 m deep, 50–500 m wide zone that is both the most dynamic part of the coast and the most dangerous for navigation and for storm-surge modelling. Bathymetric lidar was built to fill it, and it does so wherever the water is clear and the sea is calm enough; it does not fill it in turbid estuaries, in persistent surf, or over dark bottoms at depth, and in those places the ribbon remains white — or is filled by interpolation that must be labelled as such. Integrating topobathy lidar with topographic lidar and sonar requires co-registration on shared surfaces (the dry beach for topo–bathy, overlapping depths for bathy–sonar), reconciliation of surface definitions (top of seagrass versus acoustic bottom), and a single vertical datum; Quadros et al. (2008) and the national programs below describe the practical steps ([Chapter 48](ch48-compositing.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).

<!-- figure: Figure 19.2 — Cross-shore profile from dune to 30 m depth showing the coverage envelopes of topographic lidar (to the waterline), topobathy lidar (to ~1.5 Secchi), deep-channel ALB (to ~3 Secchi), launch multibeam (seaward of the surf zone), and the surf-zone gap; a turbid-estuary variant shows the ALB envelope collapsing and the white ribbon widening. -->

## 19.7 Program context

The US Army Corps of Engineers' **JALBTCX** (Joint Airborne Lidar Bathymetry Technical Center of Expertise, with the Navy, NOAA, and USGS) has run the **National Coastal Mapping Program** since the early 2000s, flying SHOALS and then CZMIL systems along the US coasts on a recurring cycle, with post-storm response flights; its data (via NOAA's Digital Coast) are the largest public ALB archive. **NOAA's National Geodetic Survey** flies topobathy lidar for the national shoreline and for charting support, and the Office of Coast Survey accepts ALB for chart updates under the HSSD's lidar provisions. France's **Litto3D** (SHOM and IGN) produced a seamless topobathymetric model of the French coast from ALB and sonar from the mid-2000s onward; Australia, Denmark, Sweden, Finland, the Netherlands, and others run national or regional ALB programs; and the USGS's topobathymetric elevation models (CoNED) integrate ALB with topographic lidar and sonar into seamless coastal DEMs ([Chapter 55](ch55-public-products.md)). The programs share a lesson: ALB is scheduled around water clarity (seasonal plankton blooms, river discharge), sea state, and tide, and the fraction of a coast that is mappable in a given year is a property of the environment, not of the contractor.

## Then & now

The first airborne laser bathymetry experiments were flown in the late 1960s and 1970s — Hickman and Hogg's 1969 demonstration and NASA's Airborne Oceanographic Lidar in the mid-1970s in the US, Australia's WRELADS program from the late 1970s, and Canada's Larsen 500 in 1985 — proving that a green pulse could return a bottom from tens of metres. Guenther's 1985 NOAA Professional Paper laid out the system-design and error physics that still governs the field. Operational systems arrived in the 1990s: Australia's LADS (1993), the USACE/Optech **SHOALS** (1994), and Sweden's Hawk Eye, each a mJ-class 532 nm system at a few hundred hertz to a few kilohertz. The 2010s brought the dual-mode and topobathy generation — CZMIL (2011), Chiroptera and HawkEye III (2012–2013), Riegl VQ-820-G and VQ-880-G (2012–2014) — raising PRFs by two orders of magnitude and adding dense NIR topography, so that the beach and the seabed came from one flight. Since 2018 the field has widened at both ends: ICESat-2 photon-counting bathymetry from orbit and compact green scanners on UAVs; waveform processing has moved from vendor black boxes toward open research pipelines; and ellipsoidally referenced, uncertainty-attributed deliverables (BAG, LAS topobathy profile) have replaced tide-reduced soundings as the archival form.

## Mathematics

**Refraction correction.** Let the pulse meet the water surface at point $\mathbf{P}_s$ with unit direction $\hat{\mathbf{u}}_a$ (from the georeferencing equation of [Chapter 18](ch18-topographic-lidar.md)) and let $\hat{\mathbf{n}}$ be the local upward surface normal from the water-surface model. The incidence angle is $\cos\theta_a = -\hat{\mathbf{u}}_a\cdot\hat{\mathbf{n}}$. Snell's law gives $\sin\theta_w = \sin\theta_a / n_w$, and the refracted unit direction (vector form) is

$$\hat{\mathbf{u}}_w = \frac{1}{n_w}\hat{\mathbf{u}}_a + \left(\frac{\cos\theta_a}{n_w} - \cos\theta_w\right)\hat{\mathbf{n}}.$$

If the raw processing placed the bottom at $\mathbf{P}_b' = \mathbf{P}_s + s_a\hat{\mathbf{u}}_a$ using the in-air speed, the in-water slant distance is $s_w = s_a / n_w$ (the two-way time is the same; only the speed changes) and the corrected bottom point is

$$\mathbf{P}_b = \mathbf{P}_s + \frac{s_a}{n_w}\,\hat{\mathbf{u}}_w.$$

For a horizontal surface, the depth is $z = s_w\cos\theta_w$ and the horizontal offset from the entry point is $s_w\sin\theta_w$; the uncorrected point lies deeper by $s_a\cos\theta_a - s_w\cos\theta_w$ and farther from nadir by $s_a\sin\theta_a - s_w\sin\theta_w$. With $\theta_a = 20°$, $n_w = 1.34$, $s_a = 13.4$ m (apparent depth $12.59$ m): $\theta_w = 14.79°$, $s_w = 10.0$ m, $z = 9.67$ m, horizontal offset $2.55$ m versus $4.58$ m uncorrected — a correction of 2.92 m vertically and 2.03 m horizontally.

**Sensitivity to the surface.** Differentiating with respect to the surface height $z_s$ (horizontal surface, fixed two-way time measured from the aircraft): raising the modelled surface by $\delta z_s$ shortens the air path and lengthens the water path by the same geometric length along the ray, so the bottom's height changes by $\delta z_b = \delta z_s\,(1 - \cos\theta_w / (n_w \cos\theta_a))\approx \delta z_s\,(1 - 1/n_w)$ near nadir — about $0.25\,\delta z_s$ to $0.23\,\delta z_s$ at 20°. For the *depth* $z = z_s - z_b$, $\delta z = \delta z_s\,(1 - 0.25) = 0.75\,\delta z_s$ if the depth is quoted relative to the erroneous surface. A surface tilt $\delta\alpha$ about the cross-track axis changes the incidence angle by $\delta\alpha$ and rotates the normal to which the refracted angle is referred by the same $\delta\alpha$, so the refracted ray's direction relative to the vertical changes by $(\mathrm{d}\theta_w/\mathrm{d}\theta_a - 1)\,\delta\alpha = \big(\cos\theta_a/(n_w\cos\theta_w) - 1\big)\,\delta\alpha$; the horizontal displacement of the bottom is therefore $z\,\big(1 - \cos\theta_a/(n_w\cos\theta_w)\big)\,\delta\alpha \approx z\,(1 - 1/n_w)\,\delta\alpha$ — for $z = 20$ m and $\delta\alpha = 5° = 0.087$ rad about 0.5 m, before the surface-model averaging reduces the effective tilt error to a fraction of a degree.

**Depth-dependent TVU.** Collecting the terms of Section 19.3 into the S-44 form,

$$\sigma_z^2(z) = a^2 + (b\,z)^2, \qquad a^2 = \sigma^2_{\text{traj}} + \sigma^2_{\text{surf}} + \sigma^2_{\text{det},0} + \sigma^2_{\text{wl}},\quad b^2 = \left(\frac{\sigma_{n}}{n_w}\right)^2 + \beta^2_{\text{det}} + \left(\frac{\gamma\tan\alpha}{2}\right)^2,$$

where $\sigma_n/n_w \approx 0.0015$ is the relative index uncertainty, $\beta_{\text{det}}$ (≈ 0.003–0.008) the depth-proportional growth of the detection bias with turbidity, and $\gamma\tan\alpha/2$ the footprint-slope term with scattering-widened divergence $\gamma$ (e.g. 0.05 rad effective) on bottom slope $\alpha$. Numerically, with $a = 0.10$ m and $b = 0.006$, $\sigma_z(20\,\text{m}) = \sqrt{0.10^2 + 0.12^2} = 0.16$ m, consistent with the budget table; the 95 % TVU is $1.96\,\sigma_z = 0.31$ m against the S-44 Order 1a allowance of $\sqrt{0.5^2 + (0.013\times20)^2} = 0.56$ m.

**Attenuation and the depth limit.** The bottom-return power is approximately

$$P_b(z) = P_0\,\frac{\rho_b\,A_r\,\eta}{\pi\,(n_w H + z)^2}\,T_s^2\,e^{-2 k_{\text{sys}} z},$$

with $\rho_b$ the bottom reflectance, $A_r$ the receiver area, $\eta$ the optical efficiency, $H$ the altitude, $T_s$ the surface transmittance, and $k_{\text{sys}}$ the system attenuation coefficient. Setting $P_b$ equal to the detection threshold $P_{\min}$ and solving for $z$ gives the depth limit $z_{\max} \approx \frac{1}{2k_{\text{sys}}}\ln\frac{P_0\,\rho_b\,A_r\,\eta\,T_s^2}{\pi (n_w H)^2 P_{\min}}$; the logarithm's argument is the system's "dynamic range," and because the dependence is logarithmic, doubling pulse energy adds only $\ln 2/(2k_{\text{sys}})$ — 1.7 m at $k_{\text{sys}} = 0.2$ m⁻¹ — while halving $k_{\text{sys}}$ doubles $z_{\max}$. Water clarity, not laser power, is the lever; this is the quantitative content of "1.5–3 Secchi depths."

## Validation & uncertainty

ALB validation inherits the topographic lidar checks (overlap statistics, land checkpoints, calibration report; [Chapter 18](ch18-topographic-lidar.md)) and adds the water-specific ones.

**Land-side tie.** The NIR and green channels both return from the dry beach; their agreement (mean and RMS of green-minus-NIR heights on the beach, typically within 5 cm) checks the green channel's range calibration and boresight before any water is involved. Land checkpoints on the beach and hard surfaces give the NVA as usual.

**Submerged reference surfaces.** The absolute check in water is a **reference surface** surveyed independently — a multibeam survey of a flat, hard, stable patch at several depths (boat ramps, dredged channel floors, sandy flats), reduced to the same ellipsoidal reference, or a set of GNSS-surveyed points on wading-depth bottoms — against which ALB bottom points are compared, stratified by depth and bottom type. Report bias and RMS per depth bin; a bias that grows with depth indicates a refraction, index, or detection problem, a constant bias a surface-model or datum problem. Where MBES overlap exists, difference the two surfaces over the whole overlap, not just a patch, and look at the pattern: a bias on seagrass but not on sand is a surface-definition difference, not an error.

**Crosslines and overlap.** Fly crosslines over the bathymetric swaths and compute swath-to-swath differences on flat bottoms as in topographic lidar; the statistics should be comparable to the land overlaps after allowing for the detection-noise growth with depth. A cross-track pattern in the water that is absent on land points to the surface model or the refraction geometry.

**Depth-capability and gap reporting.** Validation of ALB is as much about *where it did not measure* as where it did: deliver a map of achieved maximum depth (from class 40 bottoms and class 45 "no bottom found" points), the Secchi/turbidity observations, and the surf-zone and foam gaps, so that users can distinguish "no bottom because it is deep" from "no bottom because it is turbid" from "shallow but not surveyed." Interpolated surfaces across any of these must carry the interpolation flag in the uncertainty layer.

**Feature detection.** Hydrographic use additionally requires evidence that objects of a stated size are detected; ALB's scattering-widened footprint and sparse deep-channel density make small-object detection weaker than a full-ensonification multibeam, and S-44's feature-detection requirements may not be met at depth. State the detection capability demonstrated (e.g. on known wrecks or placed targets) rather than inferring it from point spacing.

> **Worked example.** A topobathy survey over a reef flat delivers bottom points at 3–18 m depth with per-point TPU from the model $\sigma_z^2 = 0.10^2 + (0.006 z)^2$. A multibeam reference surface in 12 m of water (its own σ ≈ 0.08 m) is compared: 4,120 ALB points, mean difference (ALB − MBES) = +0.11 m, standard deviation 0.17 m. The expected standard deviation of the differences is $\sqrt{0.10^2 + (0.006\times12)^2 + 0.08^2} = 0.15$ m, so the scatter is consistent with the model. The bias of +0.11 m (ALB shallower) exceeds its standard error ($0.17/\sqrt{4120} = 0.003$ m, though the effective sample is much smaller given spatial correlation — say 50 independent patches, giving 0.024 m) and is significant. Checks: the same bias on the dry beach between green and NIR? No (−0.01 m). The same bias on a sand patch at 5 m? +0.03 m. So the bias grows with depth and is not a datum offset; the suspects are the refractive index (a 0.11 m change at 12 m would need a 0.9 % index error — too large), the detection algorithm's bias toward the near edge of the stretched pulse (plausible: 0.1 m at 12 m in moderate turbidity), or the top of algal turf being detected by the lidar and the harder substrate by the sonar (plausible on a reef flat). The report states the bias, the two hypotheses, and the evidence, and the deliverable's uncertainty layer carries an added 0.1 m systematic term at depth until a sand-bottom reference resolves it.

## Software

**Open source:** PDAL (Python filters for refraction correction as above; classification, gridding); CloudCompare (comparison of ALB and MBES surfaces, M3C2); SlideRule, `icepyx`, and OpenAltimetry for ICESat-2 ATL03 access and processing; open ICESat-2 bathymetry classifiers published with recent papers; MB-System and GMT for the sonar side of the comparison; `pyproj`/PROJ with VDatum-derived grids for datum work. Caveat: open waveform-decomposition code for commercial ALB systems is scarce; most users receive discrete points from vendor software.

**Free but closed:** NOAA Digital Coast tools and the Data Access Viewer for public ALB data; VDatum for separation models; vendor viewers.

**Commercial:** Leica Lidar Survey Studio (LSS) for Chiroptera/HawkEye waveform processing and refraction; Teledyne Optech HydroFusion for CZMIL; Riegl RiHYDRO/RiPROCESS for the VQ-8x0-G series; Fugro's in-house RAMMS processing; CARIS HIPS & SIPS and QPS Qimera for cleaning, TPU, and BAG production; TerraSolid for topobathy point classification. Caveat: each vendor's surface model and refraction implementation is different and seldom documented in enough detail to reproduce; archive the raw waveforms and the surface model with the product.

## Standards & guides

- **IHO S-44**, Edition 6.1.0 (2022) — TVU/THU and feature-detection requirements by survey order; the standard that ALB products for charting must meet, including the depth-dependent $b$ term.
- **NOAA Hydrographic Surveys Specifications and Deliverables** (annual; lidar bathymetry provisions) — requirements for ALB surveys submitted for charting, including TPU, datum, and deliverable formats.
- **USACE EM 1110-2-1003, Hydrographic Surveying** (2013, with changes) — Corps requirements for ALB in navigation projects.
- **USGS Lidar Base Specification** topobathymetric guidance/addendum — classification and product conventions for topobathy deliveries in US federal programs. (verify)
- **ASPRS LAS 1.4 Topo-Bathy Lidar Domain Profile** (2013) — classes 40–45 and extra bytes for bathymetric points.
- **IHO S-102 Bathymetric Surface** / **ONS BAG Format Specification** — gridded product with uncertainty layer for ALB-derived surfaces.
- **JALBTCX / NCMP data standards and NOAA Digital Coast metadata profiles** — practical conventions for ALB archive deliveries.

## Pitfalls

- **Surface-model errors doubling as depth errors** → a wave-biased or NIR-glint-biased surface shifts every bottom point beneath it → detect by comparing green and NIR surface heights and by swath-overlap patterns in water absent on land; avoid by reporting the surface model and its residuals.
- **Data gaps in the surf zone sold as "no features"** → foam and aerated water produce voids that interpolation fills with a smooth bar → detect by overlaying the breaking-wave zone from imagery; deliver class 45 and void polygons.
- **Turbidity-limited depth presented as the seabed** → the deepest returns in a turbid area are the last detectable bottoms, not the deepest water; a surface drawn through them is a false shoal/plateau → detect with the achieved-depth map and ICESat-2 or sonar; label the limit.
- **False bottoms from scattering layers, seagrass canopy, or thermoclines** → a strong return above the true bottom → detect by waveform inspection and by sonar comparison; classify as submerged object or vegetation, not bottom.
- **Mixing tidal and orthometric datums in one topobathy LAS** → land in NAVD88, water points reduced to MLLW, a 0.5–1.5 m step at the shoreline → detect by profiling across the waterline; deliver everything on one reference with the separation model as metadata.
- **Assuming seawater index over fresh water (or vice versa)** → 0.5 % depth scale error → detect by reference-surface bias growing with depth; set $n_w$ per project.
- **Quoting the manufacturer's Secchi multiple as achieved depth** → capability depends on bottom albedo, sea state, and sun; a 3-Secchi system reaches 2 over dark bottoms → report achieved depth from the data.
- **Treating ICESat-2 bathymetry as a survey** → six sparse profiles with 0.4–0.6 m agreement and no feature detection → use for calibration, validation, and reconnaissance; never for charting alone.
- **Ignoring the minimum-depth gap** → the 0–1 m zone where surface and bottom returns merge is left as a hole or bridged → fly at low tide, use NIR for the exposed flat, and declare the gap.
- **Flying ALB in the wrong season** → plankton blooms, river plumes, and swell halve the depth capability → schedule by clarity climatology and in-situ Secchi readings; budget for re-flights.
- **Comparing ALB to sonar without reconciling surface definitions** → seagrass top versus acoustic bottom, fluid mud, rubble → stratify comparisons by bottom type before calling a difference an error.

## Key takeaways

- Bathymetric lidar works because water is nearly transparent at 532 nm and nearly opaque at 1,064 nm; its depth limit is set by water clarity — roughly 1.5 Secchi depths for topobathy systems and up to 3 for high-energy deep channels — not by laser power, which enters only logarithmically.
- The uncertainty is dominated by the water-surface model and the refraction geometry in shallow water and by pulse stretching and bottom detection at depth; publish the surface model, the index used, and the per-point TPU with the data.
- Refraction correction is a 30 % effect on depth and a metre-scale effect on position; apply it with the per-pulse ray and the local surface normal, and verify it against a submerged reference surface stratified by depth.
- ALB fills the white ribbon between topographic lidar and sonar wherever the water is clear and calm; where it is turbid or breaking, the ribbon stays white, and the deliverable must say so with class 45 points, void polygons, and achieved-depth maps.
- Ellipsoidally referenced bottom heights sidestep the tide term and defer the datum choice; a reduced-depth product must include water-level and separation uncertainty in its TVU.
- ICESat-2 photon bathymetry is sparse, independent, 0.4–0.6 m-class truth to ~40 m in clear water: use it to calibrate SDB, to check charts, and to scout clarity before an ALB campaign.
- Compare ALB with topographic lidar on the dry beach and with sonar in overlapping depths, reconciling surface definitions first; the three sensors together, on one datum, make the coastal DEM.

## References

- Guenther, G. C. (1985). *Airborne Laser Hydrography: System Design and Performance Factors*. NOAA Professional Paper Series, National Ocean Service 1. NOAA, Rockville, MD.
- Guenther, G. C., Cunningham, A. G., LaRocque, P. E., & Reid, D. J. (2000). Meeting the accuracy challenge in airborne lidar bathymetry. *Proceedings of EARSeL-SIG-Workshop LIDAR*, Dresden, 16–17 June 2000.
- Philpot, W. (ed.) (2019). *Airborne Laser Hydrography II*. Cornell University eCommons.
- Mandlburger, G. (2022). A review of active and passive optical methods in hydrography. *The International Hydrographic Review*, 28:8–52.
- Fernandez-Diaz, J. C., Glennie, C. L., Carter, W. E., Shrestha, R. L., Sartori, M. P., Singhania, A., Legleiter, C. J., & Overstreet, B. T. (2014). Early results of simultaneous terrain and shallow water bathymetry mapping using a single-wavelength airborne LiDAR sensor. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*, 7(2):623–635.
- Nayegandhi, A., Brock, J. C., & Wright, C. W. (2009). Small-footprint, waveform-resolving lidar estimation of submerged and sub-canopy topography in coastal environments. *International Journal of Remote Sensing*, 30(4):861–878.
- Parrish, C. E., Magruder, L. A., Neuenschwander, A. L., Forfinski-Sarkozi, N., Alonzo, M., & Jasinski, M. (2019). Validation of ICESat-2 ATLAS bathymetry and analysis of ATLAS's bathymetric mapping performance. *Remote Sensing*, 11(14):1634.
- Quadros, N. D., Collier, P. A., & Fraser, C. S. (2008). Integration of bathymetric and topographic LiDAR: a preliminary investigation. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, 37(B8):1299–1304.
- Westfeld, P., Maas, H.-G., Richter, K., & Weiß, R. (2017). Analysis and correction of ocean wave pattern induced systematic coordinate errors in airborne LiDAR bathymetry. *ISPRS Journal of Photogrammetry and Remote Sensing*, 128:314–325.
- Mandlburger, G., & Jutzi, B. (2019). On the feasibility of water surface mapping with single photon LiDAR. *ISPRS International Journal of Geo-Information*, 8(4):188.
- Quan, X., & Fry, E. S. (1995). Empirical equation for the index of refraction of seawater. *Applied Optics*, 34(18):3477–3480.
- Pope, R. M., & Fry, E. S. (1997). Absorption spectrum (380–700 nm) of pure water. II. Integrating cavity measurements. *Applied Optics*, 36(33):8710–8723.
- Irish, J. L., & Lillycrop, W. J. (1999). Scanning laser mapping of the coastal zone: the SHOALS system. *ISPRS Journal of Photogrammetry and Remote Sensing*, 54(2–3):123–129.
- Hickman, G. D., & Hogg, J. E. (1969). Application of an airborne pulsed laser for near shore bathymetric measurements. *Remote Sensing of Environment*, 1(1):47–58.
- Pe'eri, S., & Philpot, W. (2007). Increasing the existence of very shallow-water LIDAR measurements using the red-channel waveforms. *IEEE Transactions on Geoscience and Remote Sensing*, 45(5):1217–1223.
- Tuell, G., Barbor, K., & Wozencraft, J. (2010). Overview of the coastal zone mapping and imaging lidar (CZMIL): a new multisensor airborne mapping system for the U.S. Army Corps of Engineers. *Proceedings of SPIE*, 7695:76950R.
- Wozencraft, J., & Millar, D. (2005). Airborne lidar and integrated technologies for coastal mapping and nautical charting. *Marine Technology Society Journal*, 39(3):27–35.
- Mandlburger, G., Pfennigbauer, M., Schwarz, R., Flöry, S., & Nussbaumer, L. (2020). Concept and performance evaluation of a novel UAV-borne topo-bathymetric LiDAR sensor. *Remote Sensing*, 12(6):986.
- Kinzel, P. J., Legleiter, C. J., & Nelson, J. M. (2013). Mapping river bathymetry with a small footprint green LiDAR: applications and challenges. *Journal of the American Water Resources Association*, 49(1):183–204.
- Babbel, B. J., Parrish, C. E., & Magruder, L. A. (2021). ICESat-2 elevation retrievals in support of satellite-derived bathymetry for global science applications. *Geophysical Research Letters*, 48(5):e2020GL090629.
- Thomas, N., Pertiwi, A. P., Traganos, D., Lagomasino, D., Poursanidis, D., Moreno, S., & Fatoyinbo, L. (2021). Space-borne cloud-native satellite-derived bathymetry (SDB) models using ICESat-2 and Sentinel-2. *Geophysical Research Letters*, 48(6):e2020GL092170.
- International Hydrographic Organization (2022). *S-44 IHO Standards for Hydrographic Surveys*, Edition 6.1.0. IHO, Monaco.
- ASPRS (2013). *LAS Domain Profile Description: Topo-Bathy Lidar*, Version 1.0. ASPRS. (verify)
- Eren, F., Jung, J., Parrish, C. E., Sarkozi-Forfinski, N., & Calder, B. R. (2019). Total vertical uncertainty (TVU) modeling for topo-bathymetric LIDAR systems. *Photogrammetric Engineering & Remote Sensing*, 85(8):585–596.

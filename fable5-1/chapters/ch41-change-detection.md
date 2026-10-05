# Chapter 41 — Change detection methods and the minimum detectable change

> **Part VIII — The dynamic Earth.** The Part's closing chapter is the methods toolbox: how to compare elevation data across time (and across sources) with grids, point clouds, radar phase, and images, and the statistics that determine what can honestly be claimed — and, just as important, what cannot.

**In this chapter.** You will learn to co-register two elevation datasets before comparing them — the Nuth & Kääb aspect-slope fit, ICP, feature matching, and bias correction over stable terrain — and to recognize the half-pixel misregistration that produces aspect-dependent false change. You will apply grid-based differencing with spatially variable uncertainty, and point-cloud methods (C2C, C2M, M3C2 and its error-propagating variant, 4D objects-by-change) that measure change along the surface normal and give every distance its own level of detection. You will see InSAR time series as millimetre-scale change detection with specific failure modes, optical correlation for horizontal motion, and repeat multibeam for the seabed. You will separate semantic from geometric change, define the minimum detectable change formally, perform a power analysis to design a survey that can see a specified change, and build a checklist for the confounds — season, moving objects, datum events, reprocessed baselines, DSM-versus-DTM — that generate most published "change." A py4dgeo example computes M3C2 distances with per-point LoD.

## 41.1 Co-registration before comparison

Two elevation datasets never share a coordinate frame exactly. Each has its own georeferencing error — GNSS/IMU trajectory for lidar, bundle adjustment and GCPs for photogrammetry, orbit and baseline for radar, datum transformation and resampling for any archived product — and the difference between the two is a small rigid (or nearly rigid) misalignment: a horizontal shift of a fraction of a pixel to several pixels, a vertical offset, often a tilt, occasionally a scale. Differencing without removing it produces a DoD whose dominant signal is the misalignment projected onto the terrain.

The signature is specific. A horizontal shift $\delta$ at azimuth $\psi_0$ produces an apparent elevation change

$$
\Delta z \approx \delta\,\tan\alpha\,\cos(\psi - \psi_0)
$$

on terrain of slope α and aspect ψ: zero on flat ground, maximal on slopes facing along the shift, reversing sign on slopes facing the opposite way. This is the **aspect-dependent bias** that Nuth & Kääb (2011) turned into a co-registration method: normalize the DoD by $\tan\alpha$, bin by aspect, fit $a\cos(b - \psi) + c$, and read off the shift magnitude $a$, direction $b$, and the residual vertical offset $c\,\overline{\tan\alpha}$; shift, re-difference, and iterate until the shift is below a threshold (typically 0.1 pixel or 1 cm). The method is robust, needs only the DoD and a stable-terrain mask, and converges in a few iterations; it is the default in xdem and demcoreg and the standard for satellite-DEM glacier work. Its assumptions are that the misalignment is a translation (add a tilt or a low-order polynomial correction afterward if the stable-terrain residuals show a ramp), that there is enough slope and aspect diversity in the stable terrain to constrain the fit (flat floodplains do not constrain horizontal shift at all), and that the stable terrain really is stable.

**ICP** (Besl & McKay 1992) solves the same problem for point clouds or meshes and recovers rotation as well as translation; its point-to-plane variant (using local normals) converges faster and is less sensitive to point density differences. It requires an initial alignment within the convergence basin (metres), is biased by outliers and by unmatched surfaces (vegetation present in one epoch), and — like Nuth & Kääb — needs geometric texture in all three directions; a flat plane constrains only one translation and two rotations. **Feature-based matching** (building corners, road intersections, distinctive terrain points detected by SIFT-like operators on hillshades or by keypoint detectors on point clouds) gives a sparse set of correspondences for a robust initial estimate, especially across sensors. **Bias correction over stable terrain** removes whatever structured residual remains — a constant, a plane, a function of elevation (common between radar and optical DEMs), or along-track/cross-track trends in satellite DEMs (ASTER's "jitter" at ~several-km wavelength, corrected by Girod et al. 2017) — by fitting and subtracting it on the stable mask.

The **half-pixel registration problem** ([Chapter 31](ch31-interpolation-and-gridding.md)) is the same error introduced by convention rather than by measurement: one dataset uses pixel-is-area (coordinates refer to cell centres) and the other pixel-is-point (coordinates refer to corners), or the two grids are offset by half a cell after reprojection. The resulting aspect-dependent pattern is identical to a georeferencing shift and is removed by the same methods — but it is better to catch it in the metadata first, because its magnitude (half a cell diagonally, 0.71 cell) is exactly predictable.

> **Definitions that bite.** "Stable terrain" means terrain whose elevation did not change between epochs *at the level of the comparison's precision*. Bedrock and paved surfaces qualify on land for decades; forests never do (growth, season, penetration); agricultural fields do not within a year (tillage, crops); roads in a subsiding basin do not for absolute work. Glacier-free terrain used to co-register glacier DEMs excludes periglacial slopes (creep, thaw). Under water, "stable" seabed is bedrock or armoured substrate, and even that is suspect at the decimetre level because of the tide and sound-speed reductions. State the mask's definition and area; show its residual statistics.

<!-- figure: Figure 41.1 — Nuth & Kääb diagnostic: (a) DoD before co-registration showing the aspect-dependent pattern on hillslopes; (b) dh/tan(slope) plotted against aspect with the fitted cosine (amplitude = shift magnitude, phase = direction); (c) DoD after shift correction with the pattern gone; (d) stable-terrain histogram before and after (NMAD reduction). -->

## 41.2 Grid-based change detection

Once co-registered, grid differencing is the simplest and most widely used method, and [Chapter 40](ch40-erosion-and-geomorphic-change.md) developed its statistics for geomorphic change. The points to add here concern what the grid cannot see.

**Vertical versus normal-direction change.** A DoD measures the vertical difference at a fixed horizontal position. On a slope, a surface that retreats by a distance $d$ along its normal appears as a vertical change $d/\cos\alpha$ — 1 m of normal retreat on a 60° cliff face is 2 m of vertical change — and on a vertical or overhanging face the vertical difference is undefined ([Chapter 35](ch35-voids-and-overhangs.md)). Conversely, horizontal translation of a slope appears as vertical change (§41.1). For steep terrain, cliffs, structures, and anything with overhangs, the quantity of interest is the distance along the local normal, which requires point-cloud methods (§41.3) or a reprojection of the grid into a local reference frame (a cliff-face "DEM" with the horizontal axis as elevation).

**Slope-dependent error** is now standard practice to model (per-cell σ as a function of slope and curvature), but its *causes* are worth distinguishing because they imply different remedies: horizontal position error of the measurement (σ_xy tan α) is reduced by better georeferencing; interpolation error on rough, high-curvature terrain is reduced by denser sampling; footprint averaging across a slope (a 30 cm lidar footprint or a 10 m SAR resolution cell on a 30° slope spans decimetres to metres of elevation) is intrinsic to the sensor. **Curvature effects** are subtler: a smoothing sensor or interpolator biases ridges low and valleys high, so a DoD between a smooth and a sharp DEM of the same terrain shows false erosion on ridges and false deposition in channels — a pattern easily mistaken for diffusive hillslope process. The remedy is to compare at matched effective resolution (degrade the sharper DEM with the same kernel; [Chapter 44](ch44-resolution-and-sampling.md)) and to check the DoD against curvature on stable terrain.

**Time series rather than pairs.** With more than two epochs, per-pixel regression (linear or with seasonal terms) against time replaces pairwise differencing: it uses all data, is robust to any single bad epoch (with robust regression — Theil–Sen or weighted least squares with outlier rejection), yields a rate with an uncertainty, and is the method of Hugonnet et al. (2021) for glaciers and of most Landsat/Sentinel surface-change products. Its assumption is a model of the temporal behaviour; a landslide that moved once is poorly described by a linear rate and better by a step detector ([Chapter 37](ch37-time-scales-of-change.md), Mathematics).

## 41.3 Point-cloud-based methods

Point clouds preserve the 3D geometry that grids discard, at the cost of irregular sampling and no natural "same location" to difference at. Four families of methods exist (Qin, Tian & Reinartz 2016 and Okyay et al. 2019 review them).

**Cloud-to-cloud (C2C)** computes, for each point in the second cloud, the distance to the nearest point in the first. It is fast and needs no surface model, but the nearest-point distance is biased by point spacing (it cannot be smaller than roughly half the spacing even for identical surfaces), is unsigned (no erosion/deposition distinction), and is sensitive to roughness and outliers. It is a screening tool, not a measurement.

**Cloud-to-mesh (C2M)** meshes the reference cloud and measures signed distances from the compared cloud's points to the mesh along the mesh normal. It gives signed, spacing-independent distances but inherits meshing errors — holes, bridging across occlusions, smoothing — and in natural, rough terrain the mesh is often the largest error source.

**M3C2** (Multiscale Model to Model Cloud Comparison; Lague, Brodu & Leroux 2013) avoids meshing. At each **core point** (a subsample of the reference cloud), a normal is estimated from the neighbourhood within a radius $D$ (the normal scale, chosen large enough to average over roughness — the "multiscale" refers to selecting $D$ per point where the surface is most planar); a cylinder of radius $d/2$ (the projection scale) is projected along that normal through both clouds; the mean position of each cloud's points within the cylinder is computed, and the signed distance between the two means along the normal is the M3C2 distance. Crucially, each distance carries its own **level of detection**: with $n_1, n_2$ points in the cylinder and local standard deviations (roughness) $\sigma_1, \sigma_2$ along the normal,

$$
\text{LoD}_{95} = 1.96\left(\sqrt{\frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}} + \text{reg}\right),
$$

where reg is the registration error between the clouds (a scalar, estimated from stable areas). Change is declared significant where $|d_{\text{M3C2}}| > \text{LoD}_{95}$. The method handles steep, overhanging, and rough surfaces, measures in the physically meaningful direction, and separates measurement precision from registration error — which is why it has become the standard for TLS and UAV change detection on cliffs, river banks, landslides, and structures. Its parameters matter: too small a $D$ and the normals follow roughness (noisy distances, inflated LoD); too large and the normal is wrong on curved surfaces; too small a $d$ and the cylinders contain too few points. Lague et al. recommend $D$ ≈ 20–25 times the roughness scale and $d$ comparable to the point spacing times a factor giving ≥ 20–30 points.

**M3C2-EP** (Winiwarter, Anders & Höfle 2021) replaces the scalar reg with full error propagation: each point's 3D covariance (from the scanner's range and angular precision and the registration's covariance matrix) is propagated through the M3C2 geometry to a per-point LoD that varies with range, incidence angle, and position relative to the registration targets. The result is a spatially variable LoD that is smaller than the global M3C2 LoD near the scanner and on well-constrained surfaces and larger at range and at the edges of the registered volume — in the authors' rock-glacier case, detecting significant change over substantially more area than classic M3C2 at the same confidence.

**4D methods.** Permanent laser scanning — a TLS installed on a cliff, a beach, or a glacier forefield, scanning hourly for months to years (Vos et al. 2017 at Kijkduin beach; Williams et al. 2018 on the North Yorkshire cliffs) — produces thousands of epochs, and pairwise differencing becomes both impractical and wasteful. **4D objects-by-change** (Anders et al. 2020, 2021) treats the data as a time series per core point, detects changes as departures from the local temporal baseline, and segments space–time regions of similar change history into objects with a start time, an end time, a magnitude, and a spatial extent — a rockfall, a sand-bar migration, a snow-drift — so that the result is a catalog of events rather than a stack of maps. py4dgeo implements both M3C2 (with EP) and 4D-OBC.

> **Try it.** Compute M3C2 distances and per-point LoD₉₅ between two epochs of a TLS cliff survey with py4dgeo, and report the fraction of the surface with significant change.
>
> ```python
> import numpy as np, py4dgeo
> epoch1, epoch2 = py4dgeo.read_from_las("cliff_2022-03.laz", "cliff_2023-03.laz")
> # Core points: subsample of epoch1 (every 20th point), or a regular grid on the face
> core = epoch1.cloud[::20]
> m3c2 = py4dgeo.M3C2(epochs=(epoch1, epoch2), corepoints=core,
>                     normal_radii=(0.5, 1.0, 2.0),   # multiscale normal estimation (m)
>                     cyl_radius=0.5,                  # projection radius d/2 (m)
>                     max_distance=5.0,
>                     registration_error=0.012)        # from stable-area residuals (m)
> dist, unc = m3c2.run()
> lod = unc["lodetection"]
> sig = np.abs(dist) > lod
> print(f"median LoD95 = {np.nanmedian(lod):.3f} m; significant change on {sig.mean()*100:.1f} % of core points")
> print(f"significant retreat (dist<0) volume proxy: {np.nansum(dist[sig & (dist<0)]):.1f} m·pts")
> ```
>
> Expected outcome: median LoD₉₅ of roughly 2–4 cm for a well-registered TLS pair at tens of metres range; significant change concentrated in rockfall scars (negative distances of decimetres to metres) and talus accumulation (positive), with the rest of the face below LoD. Raising `registration_error` to 0.05 m should visibly shrink the significant area — a direct demonstration that registration, not scanner noise, usually sets the detection floor.

## 41.4 InSAR time series

Interferometric SAR measures change in the radar line-of-sight (LOS) distance between acquisitions as a phase difference, with a sensitivity of a fraction of the wavelength — millimetres for C-band (5.6 cm) and X-band (3.1 cm), roughly a centimetre for L-band (24 cm) — over scenes of 100–250 km ([Chapter 21](ch21-radar-sar-insar.md)). As a change-detection method it occupies a different region of the amplitude–period map from everything else in this chapter: it sees millimetres per year of slow deformation (subsidence, landslide creep, interseismic strain, volcanic inflation) that no DEM pair can, and it cannot see a metre of erosion at all, because such change decorrelates the phase.

**Persistent scatterer** (PS) methods (Ferretti, Prati & Rocca 2001) select pixels whose phase is dominated by a single stable scatterer (buildings, rock outcrops, poles) and that remain coherent across the whole stack; they achieve the highest precision (~1 mm/yr on rates over several years) but only on built or rocky surfaces. **Small-baseline subset** (SBAS) methods (Berardino et al. 2002) use many interferograms with short temporal and spatial baselines, average over distributed scatterers, and invert for the time series by least squares; they cover vegetated and natural terrain at lower resolution and precision. Modern processors (MintPy, LiCSBAS, StaMPS, GAMMA, SARscape) combine both.

The limits are intrinsic and should be listed in every product. **Decorrelation**: temporal (vegetation growth, snow, tillage, moisture change), geometric (large perpendicular baselines), and volumetric (canopy) — the phase becomes noise, and the area is simply missing from the result; L-band (ALOS-2, NISAR, SAOCOM) penetrates vegetation better and stays coherent longer. **Atmosphere**: tropospheric water-vapour delay produces phase patterns of centimetres over tens of kilometres that correlate with topography and vary between acquisitions; stacking, weather-model corrections (GACOS), and elevation-dependent fits reduce it, but a residual of 1–2 mm/yr over 50 km is typical and is indistinguishable from broad tectonic or GIA signals. **Unwrapping errors**: phase is measured modulo 2π, and wherever the gradient exceeds π per pixel or coherence is lost, the unwrapper can add integer cycles (2.8 cm per cycle at C-band) to entire regions; such errors appear as sharp steps in the velocity field with no physical boundary. **LOS geometry**: a single track measures one projection of the 3D displacement; vertical and east components are separable with ascending and descending tracks, north is almost invisible (polar orbits look east–west), and users who assume "InSAR displacement is vertical" misattribute horizontal motion. **Reference**: every InSAR velocity is relative to a reference pixel or area assumed stable; tie to GNSS for absolute rates ([Chapter 38](ch38-plate-motion-and-vlm.md)). And **the DEM dependence**: topographic phase is removed using a reference DEM, and DEM error maps into the result in proportion to the perpendicular baseline — one more reason the quality and epoch of the DEM matter.

## 41.5 Image-based methods

Where change is horizontal and large — glaciers flowing at metres per day, dunes migrating, landslides creeping, coseismic offsets — sub-pixel **optical image correlation** between two orthorectified images gives the horizontal displacement field directly. COSI-Corr (Leprince et al. 2007), MicMac's MM2DPosSism, and autoRIFT (Gardner et al. 2018; the engine behind the ITS_LIVE global ice-velocity product) all cross-correlate small windows (16–64 pixels) in the frequency or spatial domain and locate the correlation peak to ~0.05–0.1 pixel; with Sentinel-2 (10 m) that is ~1 m, with Pléiades (0.5 m) a few centimetres. The method's error budget is dominated by orthorectification (DEM errors and sensor-model errors produce apparent displacement that correlates with topography and with the stereo geometry — the reason COSI-Corr's first step is a rigorous resampling), by illumination and shadow differences between dates, by surface-texture loss (snow, cloud, water), and by attitude jitter of pushbroom sensors (periodic along-track stripes of decimetres). **Feature tracking** on ice uses the same machinery with crevasse patterns as texture and now runs operationally on Landsat 8/9 and Sentinel-2 archives; on dunes it tracks slip faces and ripples. For elevation work, image-based methods supply the horizontal component that grid DoD lacks, and combining them with vertical change gives full 3D displacement from imagery alone.

## 41.6 Bathymetric change

Repeat multibeam surveys detect seabed change for navigation safety, dredge monitoring, habitat and sediment studies, and infrastructure risk ([Chapter 20](ch20-sonar.md)). The methods are those of §41.2 — grid DoD with LoD — but the error budget is different in kind: it is dominated not by the sonar but by the reductions. Tide (or ellipsoid-referenced vertical positioning) contributes 5–20 cm of correlated error over a survey area in coastal waters; sound-speed error produces depth-dependent and swath-angle-dependent bias ("smiles" and "frowns") of 0.1–0.5 % of depth; vessel motion residuals (heave, pitch/roll timing, lever arms) produce along- and across-track artefacts at the decimetre level; and total vertical uncertainty (TVU) under S-44 Order 1a — $\sqrt{0.5^2 + (0.013\,d)^2}$ m at 95 % — is 0.52 m at 10 m depth and 0.72 m at 40 m, which sets the LoD for a DoD between two such surveys at ~0.9 m unless both surveys are demonstrably better than specification (Special Order or Exclusive Order surveys, or ellipsoid-referenced surveys with careful calibration, reach 0.1–0.2 m). The practical consequence is that most bathymetric change studies can see decimetres at best; **dredge monitoring**, which needs to confirm that a channel was deepened by 0.5 m and that the spoil ground rose by the corresponding volume, is at the edge of what pre- and post-dredge surveys resolve, and contractual volumes are disputed accordingly ([Chapter 65](ch65-mining-landfills-earthworks.md)).

**Bedform tracking** — measuring sandwave and megaripple migration by cross-correlating repeat bathymetric grids, or by tracking crest lines — is the bathymetric analogue of optical correlation and is less sensitive to vertical reductions because it measures horizontal displacement of a shape. Sandwaves in the southern North Sea migrate at 1–20 m/yr; the burial depth of a cable or pipeline, and the risk of its exposure and free-spanning, depend on the trough depths that will pass over it during its lifetime, so repeat surveys and migration models are part of route engineering (Knaapen 2005; [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)). Submarine landslides, scour around offshore structures, and post-storm nearshore change are the other main applications; in each case the first analysis step is the same as on land — difference the two surveys over seabed believed stable and verify that the result is zero within the reductions' uncertainty.

## 41.7 Semantic versus geometric change

A DoD reports that the surface at a location is 12 m higher than before. Whether that means a building was constructed, a tree grew, a stockpile was raised, a container was parked, or a cloud contaminated the stereo match is a question of **semantics**, and the appropriate response — update the city model, ignore, invoice, flag, reprocess — depends entirely on the answer ([Chapter 42](ch42-object-detection-semantics.md)). **Classification-aware differencing** classifies both epochs (ground, building, vegetation, water, vehicle, bridge, noise) and compares class *and* height: a ground-to-building transition with a height increase is construction; building-to-ground with a decrease is demolition; vegetation-to-vegetation with an increase is growth and is usually excluded from geomorphic budgets; ground-to-ground with a change is terrain change and goes into the DoD; a vehicle class in either epoch is masked ([Chapter 27](ch27-moving-and-transient-objects.md)). Qin, Tian & Reinartz (2016) frame 3D change detection as exactly this joint problem, and the practical gain is large: in urban and vegetated areas, 80–95 % of above-LoD cells in a raw DSM difference are vegetation, vehicles, or construction, and the geomorphic signal is only visible after they are removed.

Two cautions. Classification errors become change: a point labelled ground in one epoch and low vegetation in the other produces a DTM step that is purely a label difference, and ground filters tuned differently between epochs produce systematic false change on slopes and under canopy ([Chapter 30](ch30-point-cloud-classification.md)). And semantic change has its own definition problem: "building" includes temporary structures in one scheme and excludes them in another; a pile of gravel is ground to a DTM producer and an object to a city modeller ([Chapter 32](ch32-dsm-to-dtm.md)). The honest product is a change map with class transitions, heights, and the LoD, from which users apply their own definitions.

## 41.8 Minimum detectable change

The **minimum detectable change (MDC)** is the smallest true change that a given comparison will detect with specified probabilities of false alarm (α, Type I) and missed detection (β, Type II). It is a design quantity, fixed before the data are examined; the LoD is a decision threshold applied to the data. The two are related but not identical, and the distinction is the source of much confusion.

For a single cell (or core point) with difference uncertainty $\sigma_{\Delta}$, a two-sided test at level α declares change when $|\Delta z| > z_{1-\alpha/2}\sigma_\Delta$ — the LoD. A true change $\delta$ is detected with probability (power) $1 - \beta$, where

$$
1 - \beta = 1 - \Phi\!\left(z_{1-\alpha/2} - \frac{\delta}{\sigma_\Delta}\right) + \Phi\!\left(-z_{1-\alpha/2} - \frac{\delta}{\sigma_\Delta}\right)
\;\approx\; 1 - \Phi\!\left(z_{1-\alpha/2} - \frac{\delta}{\sigma_\Delta}\right).
$$

Setting the power to a target (conventionally 0.8 or 0.9) and solving for δ gives the MDC:

$$
\text{MDC} = \left(z_{1-\alpha/2} + z_{1-\beta}\right)\sigma_\Delta \quad\Rightarrow\quad \text{MDC}_{\alpha=0.05,\ \beta=0.2} = (1.96 + 0.84)\,\sigma_\Delta = 2.80\,\sigma_\Delta .
$$

That is, to detect a change reliably (80 % power) at 95 % confidence, the change must be 2.8σ, not the 1.96σ of the LoD — cells with true change exactly at the LoD are detected only half the time. For a *mean* change over a region (a volume, a glacier-wide thinning), $\sigma_\Delta$ is replaced by $\sigma_\Delta/\sqrt{n_{\text{eff}}}$ and the MDC falls accordingly, but only as fast as the effective sample size allows.

The design use of MDC is **power analysis**: given the change one needs to see (δ), the per-epoch uncertainty achievable with each candidate survey method, and the correlation structure, compute the MDC and choose the method, the cadence, and the number of epochs that bring MDC below δ at acceptable cost. The trade-offs are explicit: TLS at 1 cm σ detects 3–4 cm but covers a hillside; UAV SfM at 3–5 cm detects ~10–15 cm and covers square kilometres; airborne lidar at 7–10 cm detects 20–30 cm and covers counties; satellite stereo at 1–3 m detects 3–8 m and covers continents; InSAR detects millimetres per year but only on coherent surfaces and only in LOS. A **confidence map** — the per-cell probability that the observed change is real, or equivalently the per-cell LoD alongside the DoD — is the product that lets a user apply their own α; a change map published without one has made the decision for the user, silently.

> **Worked example.** *Power analysis for a landslide-creep monitoring program.* A slow-moving earthflow creeps at an estimated 5 cm/yr vertically. Options: (A) annual airborne lidar, per-epoch σ = 8 cm after co-registration; (B) annual UAV SfM with GCPs, σ = 3 cm; (C) quarterly UAV SfM, same σ; (D) Sentinel-1 InSAR, LOS rate σ ≈ 3 mm/yr, but the slope is vegetated and coherence is marginal.
> For a two-epoch comparison, $\sigma_\Delta = \sqrt{2}\sigma$: (A) 11.3 cm → MDC = 2.8 × 11.3 = 32 cm, i.e. 6 years of motion before a single cell is reliably detected; (B) 4.2 cm → MDC = 12 cm, 2.4 years; (C) with 8 quarterly epochs over 2 years and a linear-rate fit, $\sigma_{\hat r} \approx \sigma\sqrt{12/(N S^2)} = 3\sqrt{12/(8 \times 4)}$ = 1.8 cm/yr, so MDC on the rate = 2.8 × 1.8 ≈ 5.1 cm/yr — the target, barely, after 2 years; (D) if coherent, 3 mm/yr → MDC ≈ 1 cm/yr in LOS, detectable within a year, but only on the ~30 % of the slope that is coherent, and the LOS projection of a downslope vector on a north-facing slope captures mostly the vertical component. Averaging over the earthflow's area (0.1 km², correlation range 50 m → $n_{\text{eff}}$ ≈ 13) improves every option's *mean* rate by $\sqrt{13}$ ≈ 3.6, so (B) detects the mean creep in a single year. The design answer: annual UAV SfM for the spatial pattern of mean motion, InSAR where coherent for early warning of acceleration, and a declared MDC per cell of 12 cm so that nobody reads the first-year map as "no motion."

## 41.9 Separating signal from confounds

Most published "change" that later proves spurious comes from a short list of confounds, and the list is a checklist.

| Confound | Signature in the DoD | Test | Chapter |
|---|---|---|---|
| Season / vegetation state | Change follows land cover; positive in growing season | Stratify residuals by land cover and date; compare bare ground only | [36](ch36-seasonal-variability.md) |
| Snow, water level, tide | Uniform offsets on snow/water-covered areas; shoreline steps | Mask by date-specific snow/water extent | [34](ch34-water-in-dems.md), [36](ch36-seasonal-variability.md) |
| Moving/transient objects | Blobs of vehicle/ship size on roads, lots, harbours | Classification-aware masking | [27](ch27-moving-and-transient-objects.md) |
| Coseismic / VLM / datum events | Regional ramps, steps at patch boundaries, uniform offsets | Stable far-field test; apply deformation model; check event catalog | [38](ch38-plate-motion-and-vlm.md), [39](ch39-earthquakes-volcanoes-landslides.md) |
| Tidal datum or geoid model change | Uniform vertical offset in one product version | Compare metadata; difference against a third dataset | [9](ch09-vertical-datums.md) |
| Co-registration residual | Aspect-dependent pattern on slopes; ramp | Nuth–Kääb test; stable-terrain statistics | §41.1 |
| Half-pixel / pixel-is-area convention | Same as a 0.5–0.7 cell shift | Metadata check; Nuth–Kääb | [31](ch31-interpolation-and-gridding.md) |
| Resolution / smoothing mismatch | Ridges "eroded," valleys "filled" | Plot DoD against curvature on stable terrain | [44](ch44-resolution-and-sampling.md) |
| Reprocessed baseline | Change with sharp tile or project boundaries; version date differs from acquisition date | Lineage; compare both versions of the baseline | [50](ch50-archiving-and-provenance.md) |
| DSM vs DTM, different ground filters | Positive "change" = canopy/buildings; slope-dependent steps | Confirm surface type of both epochs; recompute from point clouds with one filter | [32](ch32-dsm-to-dtm.md), [30](ch30-point-cloud-classification.md) |
| Radar penetration | Negative bias on firn, dry snow, forest | Avoid cross-sensor differences there, or model penetration | [21](ch21-radar-sar-insar.md), [40](ch40-erosion-and-geomorphic-change.md) |
| Void fill in one epoch | Smooth areas of change coincident with fill masks | Use the fill/source mask; exclude | [35](ch35-voids-and-overhangs.md) |

"Comparing a DSM to a DTM equals trees" deserves its own line because it is the most common error in casual change studies with public data: a 2010 national DTM differenced against a 2020 commercial DSM shows every forest as 20 m of "deposition" and every building as construction. The reverse comparison shows deforestation everywhere. Neither is change. The test is trivial — check the product type — but the metadata is often missing or wrong, and a DSM/DTM mismatch on *part* of a mosaic (one tile delivered as DSM) produces a convincing patch of false change with a straight edge.

<!-- figure: Figure 41.2 — Gallery of confound signatures in DoD maps: (a) aspect-dependent co-registration pattern; (b) land-cover-correlated seasonal change; (c) regional ramp from a datum event; (d) straight-edged tile from a reprocessed baseline; (e) curvature-correlated smoothing mismatch; (f) DSM-vs-DTM forest "deposition." -->

## Then & now

Change detection began as visual comparison: two editions of a topographic map side by side, repeat photographs from the same station, a surveyor's note that the bank had moved. Digital elevation data made subtraction possible, and the first DoDs appeared in GIS in the late 1980s and 1990s as soon as two DEMs of the same place existed — usually without any error treatment, so that the maps showed change everywhere and were read selectively. The 2000s brought statistical thresholding (Brasington et al. 2003; Lane et al. 2003; Wheaton et al. 2010) and co-registration as a formal step (Nuth & Kääb 2011), driven by fluvial geomorphology and glaciology, where the signals were small relative to the errors and over-interpretation was costly. The 2010s brought point-cloud methods with per-point uncertainty (M3C2, 2013; M3C2-EP, 2021), satellite-scale time series (ASTER/ArcticDEM glacier stacks; Sentinel-1 InSAR from 2014 with free, systematic coverage), and the first permanent laser scanners streaming epochs by the hour (Kijkduin 2016–17). The current decade's direction is continuous monitoring and change *catalogs* rather than change *maps* — 4D objects-by-change, InSAR ground-motion services at national and continental scale (EGMS from 2022), repeat UAV programs, and the OpenTopography differencing service that lets any user difference two public lidar collections with co-registration and uncertainty applied by default. The arc runs from "the map changed" to "this event, here, of this magnitude, at this confidence, between these dates."

## Mathematics

**Nuth & Kääb co-registration.** For stable-terrain cells with elevation difference $dh$, slope α, and aspect ψ,

$$
\frac{dh}{\tan\alpha} = a\cos(b - \psi) + c,
$$

fitted by least squares (or robustly, by binning in aspect and fitting the bin medians). The horizontal shift has magnitude $a$ and direction $b$; the vertical offset is $c\cdot\overline{\tan\alpha}$. Apply the shift (resample the moving DEM by $-a$ at azimuth $b$), recompute $dh$, and iterate until $a$ < tolerance; typically 2–5 iterations. Add a tilt or elevation-dependent correction afterward if the residual on stable terrain shows a plane or a trend with elevation.

**M3C2 distance and LoD.** With normal $\hat{\mathbf n}$ at core point $\mathbf{c}$, cylinder radius $d/2$, and the sets $P_1, P_2$ of points from each cloud within the cylinder, let $\bar{p}_k = \frac{1}{n_k}\sum_{\mathbf{p}\in P_k} (\mathbf{p} - \mathbf{c})\cdot\hat{\mathbf n}$ and $\sigma_k$ the standard deviation of the same projections. Then $d_{\text{M3C2}} = \bar p_2 - \bar p_1$ and $\text{LoD}_{95} = 1.96\left(\sqrt{\sigma_1^2/n_1 + \sigma_2^2/n_2} + \text{reg}\right)$. In M3C2-EP, reg is replaced by $\hat{\mathbf n}^\top \mathbf{C}\,\hat{\mathbf n}$ terms where $\mathbf{C}$ is the propagated 3D covariance of each mean position, including the registration transformation's covariance.

**ICP.** Minimize $E(\mathbf R, \mathbf t) = \sum_i w_i\,\big[(\mathbf R\mathbf p_i + \mathbf t - \mathbf q_{c(i)})\cdot \hat{\mathbf n}_{c(i)}\big]^2$ (point-to-plane) by alternating correspondence search and a linearized least-squares solve for the six rigid parameters; convergence is to a local minimum, so the initial alignment must be within the basin.

**Hypothesis testing framing.** Per cell, $H_0$: no change. Test statistic $T = \Delta z/\sigma_\Delta$. Reject $H_0$ when $|T| > z_{1-\alpha/2}$ (Type I rate α). Power against alternative δ: $1 - \beta(\delta) = P(|T| > z_{1-\alpha/2} \mid \delta)$ as in §41.8. Across $n$ cells, the expected number of false positives under $H_0$ is $\alpha n$ — 5 % of a million cells is 50 000 cells of false change, spatially clustered where σ is under-estimated — which is why spatial-coherence filters and false-discovery-rate control (Benjamini–Hochberg) are used on change maps.

**Variogram-based effective sample size.** For a region of area $A$ and a variogram with nested ranges $L_k$ and partial sills $s_k$ (fractions of the total variance), $\sigma^2_{\bar\Delta} = \sigma_\Delta^2 \sum_k s_k / n_{\text{eff},k}$ with $n_{\text{eff},k} \approx A / (\kappa L_k^2)$ for $A \gg L_k^2$ and $n_{\text{eff},k} \to 1$ as $A \ll L_k^2$; Hugonnet et al. (2022) give the exact double-integral form and a numerical implementation (xdem `number_effective_samples`). The MDC for a mean change over the region is then $(z_{1-\alpha/2} + z_{1-\beta})\,\sigma_{\bar\Delta}$.

**Rate from a time series with steps.** For epochs $t_i$ and heights $z_i$, the model $z_i = z_0 + r t_i + \sum_k s_k \mathcal{H}(t_i - \tau_k) + \varepsilon_i$ with known step times $\tau_k$ is linear and solved by weighted least squares; unknown step times are found by a change-point search (e.g. PELT) or avoided by MIDAS-style median-of-pairwise-slopes estimators that are insensitive to isolated steps.

## Validation & uncertainty

The validation of a change product has two layers: validating each input surface, which the rest of the book covers, and validating the *difference*, which has its own tests.

**Stable-terrain validation** is the primary tool. After co-registration, the difference over the stable mask should have (i) mean within the LoD of zero; (ii) NMAD consistent with the propagated $\sigma_\Delta$; (iii) no significant dependence on slope, aspect, elevation, curvature, land cover, or position (test each by binning and by a regression); (iv) a variogram whose short-range sill matches the sensor noise and whose long-range structure is understood (flight lines, tiles, control). Any failure diagnoses a specific problem — aspect dependence is residual shift, elevation dependence is scale or atmosphere, position dependence is tiling or trajectory.

**Independent change validation** uses observations of change made by other means at points or small areas: GNSS or total-station re-survey of marked points, erosion pins, scour chains, TLS over a sub-area within an airborne or UAV study, or the Hugonnet-style approach of using ICESat/ICESat-2 altimetry as a sparse, high-precision check on DEM-derived change over ice. The comparison yields a bias and an RMS for the change product at the scale of the check, which is usually finer than the product; aggregate both to a common scale before comparing.

**Registration-error estimation** is required for every point-cloud method: compute the residual between the two epochs on stable patches *after* registration, as a distribution (not just an RMS), and use its spread as reg or, better, propagate the registration covariance (M3C2-EP). Reporting the registration residual as "0.4 cm RMS on targets" when the targets are near the scanner and the change area is 200 m away understates the error at range by a factor of several.

**What to report** for any change product: epochs (dates, seasons, tide stage where relevant); surface definitions of both inputs; co-registration method, mask, and residual statistics; the error model (global σ, binned, propagated) with its calibration; LoD and α; MDC at a stated power, per cell and for the aggregated quantity; a confidence or LoD layer alongside the change layer; the confound checklist of §41.9 with each item explicitly dismissed or addressed; and for volumes or means, the correlation model and $n_{\text{eff}}$.

> **Uncertainty budget.** UAV SfM change detection on a 500 m coastal cliff, two epochs one year apart, 2 cm GSD, 12 GCPs.
>
> | Component | Magnitude | Enters as |
> |---|---|---|
> | SfM surface noise (per epoch, bare rock) | 1.5 cm | $\sigma_k$ in M3C2 |
> | SfM systematic dome/tilt (per epoch, after GCPs) | 1–3 cm over 500 m | Long-range correlated; partly removed by stable-terrain plane fit |
> | Registration between epochs (GCP re-occupation + ICP on stable rock) | 1.2 cm | reg (scalar) or covariance (EP) |
> | Vegetation on cliff top and ledges | 5–50 cm | Masked by classification |
> | Normal estimation error on rough faces (D = 1 m) | adds ~0.5 cm equivalent | Inflates $\sigma_k$ |
> | **Typical LoD₉₅ (M3C2)** | **≈ 4–5 cm** | 1.96 (√(σ₁²/n₁+σ₂²/n₂) + reg) with n ≈ 30 |
> | **MDC (80 % power)** | **≈ 6–7 cm** | 2.8 × σ |
>
> Rockfalls of 10 cm and above are reliably detected; the 1–3 cm/yr weathering retreat of the face is not, cell by cell, and becomes detectable as a mean only after several years or by averaging over many square metres of face.

## Software

**Open source:** **xdem** (Nuth & Kääb, ICP, tilt/bias corrections, heteroscedastic error, variograms, $n_{\text{eff}}$; the reference implementation of Hugonnet et al. 2022); **py4dgeo** (M3C2, M3C2-EP, 4D-OBC, correspondence-driven plane-based M3C2; caveat: API still evolving); **CloudCompare** (C2C, C2M, M3C2 plugin, ICP; GUI-friendly, scriptable via command line; caveat: global ICP only without scripting); **GCD** (Riverscapes; thresholded DoD and budgets); **demcoreg** (Shean et al.; Nuth & Kääb and ICP for satellite DEMs with glacier/stable masks); **autoRIFT** and **ITS_LIVE** tools (feature tracking); **MicMac** (correlation and photogrammetry); **MintPy**, **LiCSBAS**, **StaMPS** (InSAR time series; caveat: reference-point and atmospheric-correction choices change results at the mm/yr level); **OpenTopography differencing service** (on-demand vertical and 3D differencing of public lidar collections with co-registration; caveat: parameters are fixed by the service); **PDAL** (point-cloud preparation, filtering, classification pipelines); **GDAL/GRASS/R `terra`** (grid DoD).

**Free but closed:** **COSI-Corr** (optical correlation); **EGMS Explorer** and national ground-motion portals (InSAR products, not software).

**Commercial:** **TerraScan/TerraModeler** (production change detection in lidar workflows); **Trimble RealWorks**, **Leica Cyclone 3DR** (point-cloud inspection and surface comparison for engineering; caveat: uncertainty reporting is limited); **Global Mapper** (grid differencing); **Esri ArcGIS Pro** (Change Detection Wizard, raster differencing; caveat: no built-in LoD/correlation treatment); **GAMMA**, **SARscape** (InSAR).

## Standards & guides

- **USGS 3DEP / Lidar Base Specification** (current ed.) — collection and product specifications that determine comparability between repeat collections (density, accuracy, classification, DTM definition); and USGS guidance on comparing 3DEP collections across time.
- **IHO S-44** (ed. 6.1.0, 2022) — TVU/THU orders that set the achievable LoD for repeat bathymetric surveys; requirements for re-survey after change.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data** (ed. 2, 2023) — RMSE_V/RMSE_H reporting and checkpoint requirements that make epoch accuracies comparable (the NVA/VVA terms of ed. 1 persist in the USGS Lidar Base Specification).
- **ISO 19157-1:2023** *Geographic information — Data quality* — quality elements and reporting applicable to change products (positional accuracy, temporal quality).
- **Riverscapes GCD documentation** — thresholding and error-surface practice.
- **OGC / community conventions for time-series data** (CF conventions for NetCDF time axes; STAC datetime fields) — recording epochs in change products.

## Pitfalls

- **Skipping co-registration** → "both DEMs are in the same CRS" → run the Nuth–Kääb diagnostic regardless; a half-pixel shift is invisible in metadata.
- **Using one global σ for slope-dependent errors** → simplicity → bin stable-terrain residuals by slope/curvature; use a per-cell σ.
- **Detecting "change" that is a reprocessed baseline** → the new version has the same name → check lineage and processing dates; difference the two baseline versions.
- **Mixing surface definitions** → DSM vs DTM, different ground filters, leaf-on/off → confirm product type for every tile; recompute from point clouds with one filter where possible.
- **Declaring the MDC after seeing the data** → the threshold drifts toward what shows the result → fix α, β, and the error model before differencing; document them.
- **Publishing change maps without a confidence layer** → maps look authoritative → ship the LoD or probability layer with the change layer, always.
- **Treating M3C2 reg as a target-RMS number** → it should reflect the change area, not the targets → estimate reg on stable surfaces at the range and geometry of the change; prefer M3C2-EP.
- **Reading InSAR LOS as vertical** → convention → decompose with ascending/descending or state the LOS vector; never report "subsidence" from a single track without a horizontal-motion argument.
- **Ignoring Type II error** → the LoD is a false-alarm control → report power and MDC; say what you cannot detect.
- **Interpreting a two-epoch DoD as a rate** → convenience → report a difference with its interval; fit rates only to ≥ 3 epochs.
- **Comparing DEMs of different effective resolution** → ridges "erode," valleys "fill" → match resolution; test against curvature.
- **Stable mask contaminated by slow change** → biased co-registration and budgets → test residuals vs land cover and distance from the active area.
- **Over-trusting C2C** → it is fast → use C2C only to screen; measure with M3C2 or a DoD.

## Key takeaways

- Register, estimate uncertainty spatially, threshold, then interpret — in that order, every time.
- The aspect-dependent pattern in a DoD is a shift until proven otherwise; the Nuth & Kääb fit removes it and tells you how big it was.
- Grids measure vertical change at fixed positions; M3C2 measures change along the surface normal with a per-point LoD; choose by terrain and by the question.
- The LoD controls false alarms; the MDC (≈ 2.8σ for 95 %/80 %) tells you what you can reliably see. Report both, and report what you cannot detect as clearly as what you can.
- Volume and mean-change uncertainties are governed by spatial correlation; $n_{\text{eff}}$ from a variogram, not the cell count.
- InSAR sees millimetres per year on coherent ground in LOS; nothing else sees that, and InSAR sees nothing else.
- Most spurious change is a confound from a short list: season, moving objects, datum events, reprocessed baselines, DSM-vs-DTM; run the checklist.
- The best change detector is a survey designed for change: same sensor, same season, same processing, fixed phase, and an MDC computed before the first flight.

## References

- Anders, K., Winiwarter, L., Lindenbergh, R., Williams, J. G., Vos, S. E. & Höfle, B. (2020). 4D objects-by-change: Spatiotemporal segmentation of geomorphic surface change from LiDAR time series. *ISPRS Journal of Photogrammetry and Remote Sensing*, 159:352–363. doi:10.1016/j.isprsjprs.2019.11.025
- Anders, K., Winiwarter, L., Mara, H., Lindenbergh, R., Vos, S. E. & Höfle, B. (2021). Fully automatic spatiotemporal segmentation of 3D LiDAR time series for the extraction of natural surface changes. *ISPRS Journal of Photogrammetry and Remote Sensing*, 173:297–308.
- Berardino, P., Fornaro, G., Lanari, R. & Sansosti, E. (2002). A new algorithm for surface deformation monitoring based on small baseline differential SAR interferograms. *IEEE Transactions on Geoscience and Remote Sensing*, 40(11):2375–2383. doi:10.1109/TGRS.2002.803792
- Besl, P. J. & McKay, N. D. (1992). A method for registration of 3-D shapes. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 14(2):239–256.
- Brasington, J., Langham, J. & Rumsby, B. (2003). Methodological sensitivity of morphometric estimates of coarse fluvial sediment transport. *Geomorphology*, 53(3–4):299–316.
- Ferretti, A., Prati, C. & Rocca, F. (2001). Permanent scatterers in SAR interferometry. *IEEE Transactions on Geoscience and Remote Sensing*, 39(1):8–20. doi:10.1109/36.898661
- Gardner, A. S., Moholdt, G., Scambos, T., Fahnestock, M., Ligtenberg, S., van den Broeke, M. & Nilsson, J. (2018). Increased West Antarctic and unchanged East Antarctic ice discharge over the last 7 years. *The Cryosphere*, 12:521–547.
- Girod, L., Nuth, C., Kääb, A., McNabb, R. & Galland, O. (2017). MMASTER: Improved ASTER DEMs for elevation change monitoring. *Remote Sensing*, 9(7):704.
- Hugonnet, R., McNabb, R., Berthier, E., Menounos, B., Nuth, C., Girod, L., Farinotti, D., Huss, M., Dussaillant, I., Brun, F. & Kääb, A. (2021). Accelerated global glacier mass loss in the early twenty-first century. *Nature*, 592:726–731.
- Hugonnet, R., Brun, F., Berthier, E., Dehecq, A., Mannerfelt, E. S., Eckert, N. & Farinotti, D. (2022). Uncertainty analysis of digital elevation models by spatial inference from stable terrain. *IEEE JSTARS*, 15:6456–6472. doi:10.1109/JSTARS.2022.3188922
- James, L. A., Hodgson, M. E., Ghoshal, S. & Latiolais, M. M. (2012). Geomorphic change detection using historic maps and DEM differencing. *Geomorphology*, 137(1):181–198.
- Knaapen, M. A. F. (2005). Sandwave migration predictor based on shape information. *Journal of Geophysical Research: Earth Surface*, 110:F04S11.
- Lague, D., Brodu, N. & Leroux, J. (2013). Accurate 3D comparison of complex topography with terrestrial laser scanner: Application to the Rangitikei canyon (N-Z). *ISPRS Journal of Photogrammetry and Remote Sensing*, 82:10–26. doi:10.1016/j.isprsjprs.2013.04.009
- Lane, S. N., Westaway, R. M. & Hicks, D. M. (2003). Estimation of erosion and deposition volumes in a large, gravel-bed, braided river using synoptic remote sensing. *Earth Surface Processes and Landforms*, 28(3):249–271.
- Leprince, S., Barbot, S., Ayoub, F. & Avouac, J.-P. (2007). Automatic and precise orthorectification, coregistration, and subpixel correlation of satellite images. *IEEE Transactions on Geoscience and Remote Sensing*, 45(6):1529–1558.
- Nuth, C. & Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5:271–290. doi:10.5194/tc-5-271-2011
- Okyay, U., Telling, J., Glennie, C. L. & Dietrich, W. E. (2019). Airborne lidar change detection: An overview of Earth sciences applications. *Earth-Science Reviews*, 198:102929. doi:10.1016/j.earscirev.2019.102929
- Qin, R., Tian, J. & Reinartz, P. (2016). 3D change detection — Approaches and applications. *ISPRS Journal of Photogrammetry and Remote Sensing*, 122:41–56. doi:10.1016/j.isprsjprs.2016.09.013
- Shean, D. E., Alexandrov, O., Moratto, Z. M., Smith, B. E., Joughin, I. R., Porter, C. & Morin, P. (2016). An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very-high-resolution commercial stereo satellite imagery. *ISPRS Journal of Photogrammetry and Remote Sensing*, 116:101–117.
- Vos, S., Lindenbergh, R. & de Vries, S. (2017). CoastScan: Continuous monitoring of coastal change using terrestrial laser scanning. *Proceedings of Coastal Dynamics 2017*, Helsingør, pp. 1518–1528.
- Wheaton, J. M., Brasington, J., Darby, S. E. & Sear, D. A. (2010). Accounting for uncertainty in DEMs from repeat topographic surveys: improved sediment budgets. *Earth Surface Processes and Landforms*, 35(2):136–156.
- Williams, J. G., Rosser, N. J., Hardy, R. J., Brain, M. J. & Afana, A. A. (2018). Optimising 4-D surface change detection: an approach for capturing rockfall magnitude–frequency. *Earth Surface Dynamics*, 6:101–119. doi:10.5194/esurf-6-101-2018
- Winiwarter, L., Anders, K. & Höfle, B. (2021). M3C2-EP: Pushing the limits of 3D topographic point cloud change detection by error propagation. *ISPRS Journal of Photogrammetry and Remote Sensing*, 178:240–258. doi:10.1016/j.isprsjprs.2021.06.011

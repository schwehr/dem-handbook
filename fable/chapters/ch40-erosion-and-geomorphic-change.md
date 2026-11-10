# Chapter 40 — Erosion, deposition, and geomorphic change

> **Part VIII — The dynamic Earth.** This chapter covers the reshaping of the surface by water, wind, ice, gravity, and people — the processes whose signature is the DEM of difference — and the statistics required to say, honestly, where the surface changed and by how much.

**In this chapter.** You will learn the rates at which geomorphic processes move material — hillslope creep at millimetres per year, cliff retreat at metres per year, glaciers thinning at a metre per year, humans moving more sediment than all the world's rivers — and how to decide whether a given pair of surveys can see them. You will master the geomorphic change detection (GCD) workflow: co-register, difference, estimate spatially variable error, threshold by a level of detection, and sum volumes with uncertainty that respects spatial correlation. You will see why net change hides gross change, how shoreline-change analysis (DSAS) and beach volume studies handle a moving boundary, what repeat bathymetry reveals about rivers, inlets, and reservoirs, how geodetic glacier mass balance is computed from DEMs and corrected for radar penetration, and why every morphometric index — slope, curvature, drainage density, hypsometry — depends on the resolution it was computed at. A runnable xdem example produces a thresholded DoD and a volume with a confidence interval.

## 40.1 Processes and rates

Geomorphic change is the movement of mass across the surface, and each process has a characteristic rate, scale, and style (Table 40.1). The rates span seven orders of magnitude, from the 10⁻³ m/yr of soil creep to the 10³ m/yr of a migrating braid bar, and the spatial scales from the centimetre relief of bioturbation to the hundreds of kilometres of a delta. Whether a process is observable in a DEM pair depends on where it falls relative to the pair's level of detection (§40.2) and sampling interval ([Chapter 37](ch37-time-scales-of-change.md)).

| Process | Typical vertical rate | Spatial scale | Style | Observable with |
|---|---|---|---|---|
| Soil creep, hillslope diffusion | 0.1–10 mm/yr | Hillslope (10–500 m) | Secular, diffuse | Decadal lidar; cosmogenic nuclides |
| Bioturbation (burrowing, treethrow) | mm/yr, cm-scale relief | 0.1–10 m | Stochastic | TLS; rarely isolated in DoD |
| Fluvial incision (bedrock) | 0.01–10 mm/yr | Channel | Secular, episodic | Dated terraces; not DoD |
| Fluvial aggradation/scour (alluvial) | 0.1–5 m per flood | Reach (10²–10⁴ m) | Episodic | Repeat lidar, MBES, SfM |
| Bank erosion | 0.1–10 m/yr lateral | Reach | Episodic | Repeat lidar, orthoimages |
| Braided-river bar migration | 1–100 m/yr lateral | Reach | Episodic | Repeat lidar/SfM, imagery |
| Gullying | 0.1–1 m/yr headcut retreat | 10–10³ m | Episodic | UAV SfM, lidar |
| Coastal cliff retreat | 0.01–2 m/yr (soft rock ≫ hard) | km of coast | Episodic | Repeat lidar, TLS, imagery |
| Beach/dune volume change | ±1–5 m per storm | 10²–10⁴ m | Episodic, seasonal | Repeat lidar, GNSS profiles |
| Aeolian dune migration | 1–50 m/yr lateral | 10–10³ m | Secular | Imagery correlation, lidar |
| Glacial scour (bedrock) | 0.1–10 mm/yr | Valley | Secular | Not DoD |
| Glacier thinning (ice surface) | 0.1–3 m/yr | km² | Secular + seasonal | DEM differencing, altimetry |
| Permafrost thermokarst | 1–100 cm/yr | 10–10³ m | Secular/episodic | Lidar, InSAR |
| Anthropogenic earth moving | 1–100 m per project | Site to region | Episodic | Any; semantic context needed |

Three facts about rates deserve emphasis. First, most geomorphic work is done by rare events: a river moves more sediment in a single large flood than in decades of base flow, a coast retreats more in one storm cluster than in the intervening years (Wolman & Miller 1960). A change study with two epochs measures the sum of whatever events occurred between them, and the rate it reports is a function of the interval's event history, not a property of the landscape. Second, the vertical rates of slow processes (creep, incision, scour) are below the level of detection of any DEM pair separated by less than decades; these are measured by dating, not differencing, and a DoD that appears to show them is almost always showing error. Third, humans are now the dominant geomorphic agent: Hooke (2000) estimated that deliberate earth moving — construction, mining, agriculture — shifts around 30–35 Gt/yr, more than the ~24 Gt/yr carried to the sea by rivers, and Wilkinson & McElroy (2007) estimated that agriculturally accelerated soil erosion (~75 Gt/yr) exceeds all natural denudation by an order of magnitude. On most inhabited land the largest signals in a DoD are quarries, cut-and-fill, landfills, and ploughing ([Chapter 65](ch65-mining-landfills-earthworks.md)).

<!-- figure: Figure 40.1 — Process-rate chart: vertical rate (mm/yr to m/event, log) against spatial scale (m to 100 km, log) for the processes in Table 40.1, with overlaid detection envelopes for TLS (1 cm), UAV SfM (3–5 cm), airborne lidar (10–15 cm), and satellite stereo (1–3 m) at 1-year and 10-year intervals. -->

## 40.2 Geomorphic change detection

**Geomorphic change detection (GCD)** is the differencing of two surfaces with an explicit error model. The core steps, formalized by Brasington et al. (2003), Lane et al. (2003), and Wheaton et al. (2010), are:

1. **Co-register** the two surfaces over terrain assumed stable, removing translation (horizontal and vertical), and if necessary rotation and scale, so that the difference over stable ground has zero mean and no slope- or aspect-dependent structure ([Chapter 41](ch41-change-detection.md)).
2. **Difference**: $\Delta z = z_2 - z_1$ cell by cell (the **DEM of Difference, DoD**), with a consistent sign convention (new minus old: positive is deposition).
3. **Estimate the uncertainty** of each surface, $\sigma_1$ and $\sigma_2$, either as a single value per survey (from checkpoints or stable-terrain statistics) or as a **spatially variable error surface** that depends on slope, roughness, point density, vegetation, interpolation distance, and sensor geometry; propagate to $\sigma_{\Delta z} = \sqrt{\sigma_1^2 + \sigma_2^2}$ (independent errors).
4. **Threshold** by a **level of detection**: $\text{LoD} = t\,\sigma_{\Delta z}$, with $t$ = 1.96 for 95 % confidence (or $t$ = 1 for a permissive 68 % threshold); cells with $|\Delta z| < \text{LoD}$ are treated as "no detectable change." Variants include **probabilistic thresholding** (retain each cell weighted by its probability of real change), **spatially coherent** thresholding (retain sub-LoD cells that are contiguous with above-LoD change, since real erosion patches are spatially coherent while noise is not), and Bayesian updating with a coherence prior (Wheaton et al. 2010).
5. **Sum** the thresholded DoD into volumes of erosion, deposition, and net change, each with a propagated uncertainty (Mathematics), and present a **volumetric budget** with intervals.

The choice of error model is the crux. A single σ for the whole survey is simple and usually wrong: lidar error on a flat gravel bar is 3–5 cm; on a 35° vegetated bank it is 20–50 cm; in a wetted channel it is undefined if the laser did not reach the bed. Wheaton et al. (2010) introduced **fuzzy inference systems** that combine slope, point density, and roughness into a per-cell σ with expert-defined membership functions; Hugonnet et al. (2022) replaced the expert rules with empirical modelling of the error as a function of terrain variables fitted on stable terrain, plus variogram-based spatial correlation. Either way, the output is a per-cell σ surface, and the LoD varies accordingly: a 10 cm change on a flat bar is detected, the same change on a steep bank is not — which is correct.

> **Rule of thumb.** For a DoD from two airborne lidar surveys with 10 pt/m² and good co-registration, expect $\sigma_{\Delta z}$ ≈ 5–8 cm on flat, bare ground; ≈ 10–20 cm on slopes of 20–30° or under low vegetation; ≥ 30 cm on steep, forested, or rough terrain. The 95 % LoD is twice these values. For UAV SfM with good GCPs, halve them on bare ground but expect worse under any vegetation; for TLS over short ranges, divide by five. The rule fails where either survey has a systematic error (flight-line misalignment, GCP bias) because such errors do not enter $\sigma_{\Delta z}$ as random noise.

> **Try it.** Co-register two DEMs, estimate slope-dependent uncertainty from stable terrain, threshold at a 95 % LoD, and compute a volume with a correlation-aware confidence interval using xdem (≥ 0.1).
>
> ```python
> import numpy as np, xdem, geoutils as gu
> ref = xdem.DEM("dem_2015.tif")               # reference epoch
> tba = xdem.DEM("dem_2021.tif").reproject(ref)  # to be aligned
> aoi = gu.Vector("active_area.gpkg")           # eroding reach; exclude from stable mask
> stable = ~aoi.create_mask(ref)
> # 1. Co-register (Nuth & Kääb horizontal + vertical shift, then tilt) on stable terrain
> coreg = xdem.coreg.NuthKaab() + xdem.coreg.Tilt()
> aligned = coreg.fit_and_apply(ref, tba, inlier_mask=stable)
> dh = aligned - ref                            # DoD, new minus old
> # 2. Heteroscedastic error model: sigma_dh as a function of slope and curvature
> slope, maxc = xdem.terrain.get_terrain_attribute(ref, ["slope", "maximum_curvature"])
> err = xdem.spatialstats.infer_heteroscedasticity_from_stable(
>     dvalues=dh, list_var=[slope, maxc], stable_mask=stable)
> sig = err[0]                                  # raster of per-cell sigma_dh
> # 3. Threshold at 95 % LoD
> lod = 1.96 * sig
> dh_thr = dh.copy(); dh_thr.data[np.abs(dh.data) < lod.data] = np.nan
> # 4. Volume in the AOI, with spatial-correlation-aware uncertainty of the mean
> inside = aoi.create_mask(ref)
> cell_area = ref.res[0] * ref.res[1]
> vol_net = np.nansum(dh_thr.data[inside.data]) * cell_area
> _, params, _ = xdem.spatialstats.infer_spatial_correlation_from_stable(
>     dvalues=dh, list_models=["Gaussian", "Spherical"], stable_mask=stable)
> n_eff = xdem.spatialstats.number_effective_samples(area=inside.data.sum()*cell_area,
>                                                     params_variogram_model=params)
> sig_mean = float(np.nanmean(sig.data[inside.data])) / np.sqrt(n_eff)
> print(f"net volume {vol_net:,.0f} m³ ± {1.96*sig_mean*inside.data.sum()*cell_area:,.0f} m³ (95 %)")
> print(f"n_eff = {n_eff:.0f} of {inside.data.sum():,} cells")
> ```
>
> Expected outcome: stable-terrain residuals centred at 0 with slope-dependent σ (a few cm on flat ground, tens of cm on steep slopes); the thresholded DoD retains coherent erosion/deposition patches and discards speckle; the 95 % interval on the volume is typically 5–20 % of the volume for a well-controlled reach, and $n_{\text{eff}}$ is two to four orders of magnitude smaller than the cell count. (Function signatures follow xdem's spatialstats module; check the version's API.)

## 40.3 Sediment budgets and the net-versus-gross problem

A **sediment budget** is a mass-balance statement: input − output = Δstorage. For a reach, the DoD gives Δstorage (as volume, converted to mass with a bulk density that itself has 10–20 % uncertainty), and if one of input or output is known the other follows. The practical difficulties are three.

**Net hides gross.** A reach that eroded 50 000 m³ from one bank and deposited 48 000 m³ on the opposite bar has a net change of −2 000 m³ — a number dominated by the uncertainty of each gross term. Report erosion, deposition, and net separately, each with its interval; a net change smaller than its uncertainty is not evidence of equilibrium, only of insufficient precision. Within a single cell the same problem occurs at smaller scale: a bar that was scoured by 0.5 m during the flood peak and re-filled by 0.4 m on the falling limb records −0.1 m in the DoD, and the 0.9 m of gross activity is invisible. Only continuous monitoring (scour chains, repeat surveys within the event, or acoustic bed-level sensors) resolves it.

**Compensating errors.** Co-registration removes the mean difference over stable terrain; if the stable-terrain mask inadvertently includes slowly aggrading or degrading surfaces, the correction shifts the whole DoD and erosion and deposition volumes change in opposite directions while the net stays similar — a plausible-looking budget with both gross terms wrong. Check the mask by plotting stable-terrain residuals against distance from the channel and against land cover.

**Boundary and density conversions.** The budget depends on where the reach boundaries are drawn, on how the wetted channel (where lidar has no data and SfM has refraction errors) is treated, and on the bulk density used (1.6–2.0 t/m³ for sand and gravel; 1.0–1.4 for fresh fine deposits; much less for organic). State all three; the volumes are only comparable across studies if they are.

<!-- figure: Figure 40.2 — Gravel-bed river reach: (a) DoD 2015–2021 unthresholded; (b) per-cell σ surface from slope/density/roughness; (c) DoD thresholded at 95 % LoD showing coherent bank erosion and bar deposition; (d) elevation-change distribution histogram with erosion, deposition, net, and uncertainty bars; inset table of volumes ± 95 % intervals. -->

## 40.4 Coastal change

The coast is where geomorphic change meets the largest number of people and the most datums. Three measurement traditions coexist.

**Shoreline change** treats the coast as a line and measures its horizontal migration. The USGS **Digital Shoreline Analysis System (DSAS)** (Himmelstoss et al. 2021) casts transects perpendicular to a baseline, intersects them with shorelines from different dates, and computes rates — end-point rate, linear regression rate with its confidence interval, net shoreline movement — per transect. The method's statistical machinery is sound; its weakness is the **shoreline proxy**. A shoreline can be the high-water line interpreted from aerial photographs (the wet/dry sand boundary, which moves with wave run-up and tide stage by tens of metres on a flat beach), the vegetation line, the cliff toe or top, or a datum-based contour (e.g. MHW) extracted from a lidar DEM. Proxies differ systematically — the photo-interpreted HWL lies seaward of the MHW contour by an amount that depends on beach slope and wave conditions (Ruggiero & List 2009 give a correction) — and a time series that switches proxy mid-way records the switch as change. The FGDC shoreline metadata profile requires that the proxy, tide stage, and datum be recorded for each shoreline for exactly this reason.

**Beach and dune volume** uses DoD, typically from repeat airborne lidar (the USGS/NASA/USACE EAARL and later programs flown before and after storms since the late 1990s) or from repeat GNSS profiles. Storm response is episodic: a single hurricane lowers dunes by metres and moves 10⁵–10⁶ m³ of sand per kilometre of coast offshore or inland (overwash), and the subsequent recovery over months to years returns part of it. The sampling problem of [Chapter 37](ch37-time-scales-of-change.md) is acute — the seasonal cycle (winter erosion, summer accretion) has an amplitude of 1–2 m of beach elevation on energetic coasts, so epochs must be matched by season or the signal is the season. Cliff retreat is measured by TLS or airborne lidar DoD and by repeat orthoimagery of the cliff top; soft-rock coasts retreat at 0.5–2 m/yr (the Holderness coast of England averages ~1.5–2 m/yr), hard-rock coasts at millimetres, and in both cases the long-term mean is made of discrete failures.

**Nearshore and inlet bathymetric change** requires repeat bathymetric surveys — single-beam profiles historically, multibeam and bathymetric lidar now ([Chapter 19](ch19-bathymetric-lidar.md), [Chapter 20](ch20-sonar.md)). Tidal inlets and ebb-tidal deltas move 10⁵–10⁶ m³/yr; nearshore bars migrate seasonally by tens of metres; dredged channels infill at rates that determine maintenance budgets. The error budget is dominated by tide and vertical-datum reduction (a 10 cm tidal datum error over a 1 km² inlet is 10⁵ m³), by sound-speed and heave in shallow, stratified water, and by the land–water seam where topographic and bathymetric surveys of different dates, datums, and surface definitions (the lidar sees the water surface, the sonar sees the bed) meet ([Chapter 34](ch34-water-in-dems.md)). Relative sea-level rise adds a secular term: on a coast with 4 mm/yr of relative rise, the shoreline on a 1:50 beach slope would retreat ~0.2 m/yr with no sediment loss at all (the Bruun rule's geometric part, which is a lower bound and widely disputed in its details).

> **Case file.** *The proxy-datum bias.* The USGS National Assessment of Shoreline Change combines historical T-sheet and photo-interpreted high-water-line (HWL) shorelines with lidar-derived MHW shorelines from the 2000s onward. Ruggiero & List (2009) showed that the HWL lies seaward of the MHW contour by an amount that depends on beach slope and wave run-up — typically several metres to ~20 m on low-slope, energetic beaches of the U.S. Pacific Northwest — so that an uncorrected HWL-to-MHW time series carries a spurious landward (erosional) step at the switch. They derived a proxy-datum bias correction and its uncertainty per transect; applying it is now standard in the national assessment (Morton & Miller 2005 and successors). The lesson generalizes: whenever a change series switches measurement proxy, sensor, or surface definition, the first candidate explanation for a step is the switch.

## 40.5 Rivers

River change is measured along three axes: the bed (vertical), the banks (lateral), and the planform (pattern). Repeat lidar, SfM, and bathymetric surveys now resolve all three at reach scale.

**Bedforms and bed-level change.** Dunes in sand-bed rivers migrate at metres per day during floods; repeat multibeam at hourly to daily intervals tracks their celerity and height, from which bedload transport is estimated (the dune-tracking method). Gravel-bed rivers change by bar growth, chute cutoff, and scour at bends; lidar DoD at annual intervals resolves bar-scale change (0.2–2 m) but not the sub-LoD winnowing and fining that matter ecologically. Bank erosion is the lateral term and is measured well by DoD on exposed banks (TLS at centimetres, airborne lidar at decimetres); it is the dominant sediment source on many lowland rivers.

**Braided rivers** (New Zealand's Waimakariri, Alaska's Tanana, the Himalayan Brahmaputra tributaries) rework their entire active bed over years to decades; Lane et al. (2003) and Brasington et al. (2003) established DoD-based budgets on the Waimakariri and the Feshie as the GCD method's proving ground, and repeat SfM from UAVs now resolves braid-bar dynamics at sub-metre resolution over kilometres ([Chapter 22](ch22-photogrammetry-sfm.md)). The wetted channel remains the gap: optical SfM sees the water surface (or a refracted bed, correctable to ~0.1 depth for clear water), lidar sees the surface, and only bathymetric lidar or sonar sees the bed, so most braided-river DoDs carry a "wet" mask where change is unknown.

**Dams** change rivers in both directions. Downstream, sediment starvation causes incision (metres over decades below large dams — the Missouri below Gavins Point, the Colorado below Glen Canyon) and bed armouring; upstream, the reservoir traps sediment and loses capacity. **Reservoir sedimentation surveys** — repeat bathymetry on the original pre-impoundment topography (often the 1930s–1960s contour maps, digitized) — quantify the loss: global reservoir capacity declines by roughly 0.5–1 % per year from sedimentation, and individual reservoirs in high-yield catchments (Loess Plateau, Himalaya, parts of the U.S. Southwest) have lost most of their capacity in decades. USACE EM 1110-2-4000 sets out the survey and computation practice (range-line and contour methods, now multibeam DoD against the pre-impoundment surface); the dominant uncertainty is the pre-impoundment surface itself, whose contour-map accuracy (±half a contour interval, i.e. ±0.75–1.5 m) over a reservoir of tens of km² dwarfs the modern survey's error, and whose datum (often a local project datum or NGVD 29) must be reconciled with the new survey's.

**Post-fire debris flows** convert a hillslope into a sediment source within one storm. After the 2017 Thomas Fire, the January 2018 Montecito debris flows mobilized ~10⁶ m³ from the burned catchments; pre- and post-event lidar quantified channel scour (several metres) and fan deposition, and such pairs now inform the USGS debris-flow hazard models used for post-fire warning. The pre-fire lidar's date relative to the fire and the post-event lidar's date relative to subsequent storms are the critical metadata.

## 40.6 Glaciers and ice

Glacier mass change is the clearest success of DEM differencing at global scale. The **geodetic mass balance** is the volume change from two DEMs, converted to mass with a density assumption (850 ± 60 kg/m³ for multi-year changes integrating firn and ice, Huss 2013), divided by area and time. Hugonnet et al. (2021) applied it to all ~220 000 glaciers on Earth using ASTER stereo DEMs (2000–2019) with ArcticDEM/REMA where available, found a global loss of 267 ± 16 Gt/yr with thinning accelerating from 0.36 m/yr (2000–04) to 0.69 m/yr (2015–19), and — critically for this book — propagated uncertainty with a full spatial-correlation model (nested variograms with ranges from hundreds of metres to hundreds of kilometres) so that regional and global totals carried honest intervals (Hugonnet et al. 2022 describe the method). The ingredients are those of §40.2 at scale: co-registration on stable terrain (Nuth & Kääb 2011), per-pixel error from terrain variables, temporal regression per pixel across dozens of DEMs rather than a two-epoch DoD, and correlation-aware aggregation.

Two glaciological error sources have no analogue on land. **Radar penetration**: X-band (TanDEM-X) and C-band (SRTM) signals penetrate dry snow and firn by metres before the effective scattering surface — up to ~10 m on cold Antarctic and Greenland firn, 1–5 m on temperate accumulation zones in winter, near zero on bare ice and wet snow — so a radar DEM of a glacier is biased *low* by a spatially and seasonally variable amount, and a radar-minus-optical or radar-minus-lidar difference reports false thinning in the accumulation zone unless corrected (Dehecq et al. 2016; Berthier et al. 2023 review). **Seasonality and density**: a DEM pair spanning different seasons includes the snow accumulation cycle (metres), and the density of what was gained or lost (fresh snow 100–300, firn 500–800, ice 917 kg/m³) is not observable from the DEMs.

Ice sheets are monitored primarily by **satellite altimetry** — ICESat (2003–09), ICESat-2 (2018–; photon-counting laser, ~0.1 m precision on flat ice, repeat ground tracks), CryoSat-2 (2010–; Ku-band radar with interferometric SARIn mode for margins) — whose sparse along-track sampling is the opposite of a DEM but whose precision and repeat are unmatched; DEMs from ArcticDEM/REMA strips fill in the spatial pattern and resolve outlet-glacier dynamics ([Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)). **Glacial lake outburst floods** (GLOFs) are an end-member geomorphic event — a moraine-dammed lake drains in hours, scouring the valley by metres and depositing fans downstream — and repeat DEMs of lake basins, dams, and downstream channels are the basis of hazard assessment; the Chamoli (2021) rock-ice avalanche in India was reconstructed from pre- and post-event DEMs within weeks (Shugar et al. 2021).

## 40.7 Morphometrics and their resolution dependence

DEMs are used not only to measure change but to infer process from form: **slope–area** relationships separate hillslopes (slope increasing with area) from channels (slope decreasing with area) and identify the channel head; **hypsometry** (the area–elevation distribution) indexes basin maturity; **roughness** (standard deviation of elevation, slope, or curvature in a window) discriminates landslide deposits, lava flows of different ages, and bedform fields; **drainage density** reflects lithology, climate, and vegetation; **knickpoints** (convexities in the longitudinal profile, found by the χ or slope–area method) record base-level fall or lithologic contrasts and are mapped systematically with tools such as TopoToolbox and LSDTopoTools (Schwanghart & Scherler 2014; Mudd et al. 2014).

Every one of these indices depends on the grid resolution at which it is computed — not as a nuisance but fundamentally, because the land surface is rough at all scales and a derivative of a sampled surface is a derivative of the sampling. Zhang & Montgomery (1994) showed that mean slope decreases and the slope–area relationship shifts as cell size coarsens from 2 m to 90 m; drainage density depends on the area threshold used to define channels, which depends on resolution; roughness in a fixed window changes by factors of several between 1 m lidar and 30 m SRTM; hypsometry is the most robust but still shifts at the peaks and valley floors. Passalacqua et al. (2015) review the opportunities and the traps of high-resolution topography for geomorphology, and the operative rules are: compute morphometrics at a stated resolution appropriate to the process scale (Chapter 44 develops the sampling theory); compare across sites only at the same resolution and with the same algorithm (slope by Horn, Zevenbergen–Thorne, or least-squares plane differ by degrees on rough terrain; [Chapter 44](ch44-resolution-and-sampling.md)); and never compare an index computed from 1 m lidar with the same index from 30 m SRTM and attribute the difference to the landscape.

<!-- figure: Figure 40.3 — Same catchment at 1 m, 5 m, 10 m, and 30 m: slope maps, slope–area plots, extracted channel networks at a fixed area threshold, and a table of mean slope, drainage density, and roughness showing systematic drift with resolution. -->

## 40.8 Anthropogenic change

On most inhabited land the largest terms in a DoD are human. Agricultural terraces (built and abandoned over millennia, now mapped from lidar across Mediterranean Europe and Asia), levelled fields (laser-levelled rice paddies move 10²–10³ m³/ha), quarries and open-pit mines (10⁶–10⁹ m³; the largest excavations on Earth), landfills (rising at metres per year during operation, settling at decimetres per year for decades after), land reclamation (Singapore has added ~25 % to its land area since 1965; the Netherlands, Dubai, and the Chinese coast on similar scales), and dredging and dumping (channels deepened by metres, spoil grounds raised by metres — [Chapter 65](ch65-mining-landfills-earthworks.md)) are all unambiguous in a thresholded DoD, usually with sharp edges that natural processes do not produce. The difficulties are semantic rather than statistical: the ground definition changes when a surface is paved or built on ([Chapter 32](ch32-dsm-to-dtm.md)); stockpiles are terrain to the earthwork surveyor and objects to the DTM producer; a landfill cap is "ground" that settles and must be monitored against a permit's final grade; and reclaimed land subsides for decades as the fill consolidates, so that its "as-built" DEM decays like a benchmark in a delta ([Chapter 38](ch38-plate-motion-and-vlm.md)). For change studies, the operational rule is to classify anthropogenic change explicitly — by semantic context ([Chapter 42](ch42-object-detection-semantics.md)), by edge sharpness, by permit and cadastral records — and to report it separately from the natural budget; otherwise a river reach's sediment budget includes the gravel pit on its floodplain.

## Then & now

Quantitative geomorphology began with repeat measurement at points and lines: erosion pins hammered into banks and read with a ruler, painted pebbles traced after floods, cross-sections re-levelled each season, the repeat photography of Gilbert and later workers in the American West. These methods gave rates at the places chosen and nothing between, so the first budgets (Leopold, Wolman, and Miller's *Fluvial Processes in Geomorphology*, 1964) were built from sparse samples and strong assumptions. Total stations in the 1980s and kinematic GNSS in the 1990s made dense surveys of small reaches feasible (thousands of points per day), and the first true DoDs were interpolated from such surveys (Lane, Chandler & Richards 1994 on a glacial outwash reach). Airborne lidar at the end of the 1990s and SfM photogrammetry after about 2010 (Westoby et al. 2012; James & Robson 2012) changed the question from "did it change at the sections?" to "where did it change, by how much, and with what confidence?" — and the statistical apparatus of §40.2 (Brasington et al. 2003; Lane et al. 2003; Wheaton et al. 2010) was developed precisely because the new data made it possible to over-interpret noise at scale. Repeat multibeam did the same underwater a decade later, and satellite stereo (ASTER, then Maxar/Pléiades strips) extended the method to every glacier on Earth (Hugonnet et al. 2021). The present frontier is continuous monitoring — permanent terrestrial scanners on cliffs and beaches logging hourly, Sentinel-1 and -2 at weekly cadence — where the data model is a 4D time series and the challenge is detecting change *when* it happens rather than between two arbitrary dates ([Chapter 41](ch41-change-detection.md)).

## Mathematics

**DoD and its uncertainty.** For co-registered surfaces $z_1$ (old) and $z_2$ (new), $\Delta z = z_2 - z_1$. With independent per-cell errors, $\sigma_{\Delta z} = \sqrt{\sigma_1^2 + \sigma_2^2}$; if the two surfaces share a correlated error component $\sigma_c$ (same control, same geoid, same interpolation of the same breaklines), the shared part cancels in the difference and $\sigma_{\Delta z} = \sqrt{\sigma_{1,\text{ind}}^2 + \sigma_{2,\text{ind}}^2}$ is *smaller* than the naive sum — one reason repeat surveys with identical methods detect change better than their absolute accuracies suggest. Conversely, a bias $b$ between surveys that is not removed by co-registration enters $\Delta z$ in full.

**Level of detection.** $\text{LoD}_{1-\alpha} = z_{1-\alpha/2}\,\sigma_{\Delta z}$, with $z_{0.975}$ = 1.96. The probability that a cell with true change $\delta$ exceeds the LoD is $P = 1 - \Phi\!\big((\text{LoD} - \delta)/\sigma_{\Delta z}\big) + \Phi\!\big((-\text{LoD} - \delta)/\sigma_{\Delta z}\big)$; for $\delta = \text{LoD}$ this is only ~50 %, i.e. half of the cells with true change equal to the LoD are missed (Type II error). The LoD is a false-positive control, not a detection guarantee ([Chapter 41](ch41-change-detection.md) on power).

**Probabilistic thresholding** (Wheaton et al. 2010). Each cell's $t$-score $t_i = |\Delta z_i| / \sigma_{\Delta z,i}$ gives a probability $p_i = 1 - 2(1 - \Phi(t_i))$ (two-sided) that the change is real; cells are retained if $p_i > p_{\min}$, or volumes are computed as $\sum p_i \Delta z_i a$. Spatial coherence is incorporated by Bayes' rule with a prior from the fraction of above-threshold neighbours in a window.

**Volume and its uncertainty.** $V = a \sum_{i=1}^{n} \Delta z_i$. Independent errors give $\sigma_V = a\,\sigma_{\Delta z}\sqrt{n}$, which for a $\sigma_{\Delta z}$ of 0.1 m and $n$ = 10⁶ cells of 1 m² is 100 m³ — far too small, because DEM errors are spatially correlated. With correlation function $\rho(h)$,

$$
\sigma_V^2 = a^2 \sum_i \sum_j \sigma_i \sigma_j\, \rho(h_{ij}) \;\approx\; a^2 \sigma_{\Delta z}^2\, n^2 / n_{\text{eff}},
\qquad
n_{\text{eff}} = \frac{n^2}{\sum_i\sum_j \rho(h_{ij})}.
$$

For a spherical variogram with range $L$ and area $A \gg L^2$, $n_{\text{eff}} \approx A / (\kappa L^2)$ with $\kappa$ ≈ 0.2–0.5 depending on the model (Rolstad et al. 2009 give $\kappa = \pi/5$ for a spherical model in the form $A_{\text{corr}} = \pi L^2/5$); the uncertainty of the *mean* change is $\sigma_{\Delta z}/\sqrt{n_{\text{eff}}}$ and $\sigma_V = A\,\sigma_{\Delta z}/\sqrt{n_{\text{eff}}}$. Multiple correlation ranges (short-range sensor noise, medium-range interpolation and flight-line effects, long-range control and atmospheric errors) are summed: $\sigma_V^2 = A^2 \sum_k \sigma_k^2 / n_{\text{eff},k}$ (Hugonnet et al. 2022). A fully correlated bias $b$ adds $bA$ to $V$ directly and should be carried as a separate systematic term.

**Fuzzy-inference error surfaces.** Inputs (slope, point density, roughness, interpolation distance) are mapped to linguistic classes (low/medium/high) by membership functions; rules of the form "IF slope is high AND density is low THEN error is high" are evaluated with min/max operators; the output fuzzy set is defuzzified (centroid) to a numeric σ per cell. The scheme is transparent and tunable but its membership functions must be calibrated against checkpoints or stable-terrain residuals in each new setting; the empirical alternative (binning stable-terrain residuals by terrain variables, then fitting a smooth function) achieves the same end with fewer assumptions.

**Geodetic mass balance.** $\dot{B} = \dfrac{\rho_{\Delta V}}{\rho_w}\cdot\dfrac{\sum_i \Delta z_i\, a}{\bar A\,\Delta t}$ in metres water equivalent per year, with $\rho_{\Delta V}$ = 850 ± 60 kg/m³ for multi-year periods and $\bar A$ the mean glacier area over the interval; uncertainty combines $\sigma_V$ (above), the density uncertainty (~7 %), area uncertainty, and any unfilled voids (filled by hypsometric interpolation with its own error term).

## Validation & uncertainty

**Where DoD errors come from.** (1) Each surface's own error — sensor noise, georeferencing, interpolation, ground-classification errors — which is heteroscedastic (slope, vegetation, density) and spatially correlated. (2) Co-registration residuals — a horizontal misalignment $\delta$ produces apparent change $\delta\tan\alpha$ correlated with aspect; a vertical offset produces a uniform bias; a tilt produces a ramp. (3) Surface-definition differences — leaf-on vs leaf-off, grass height, snow, water level, the DSM/DTM distinction, different ground filters — which are systematic by land cover and the most common source of false change in mixed-sensor comparisons. (4) Temporal mixing within a survey (a multi-day flight across a flood). (5) Processing-version differences in the baseline ([Chapter 41](ch41-change-detection.md)).

**How to test.** *Stable-terrain statistics*: after co-registration, the DoD over a stable mask should have mean ≈ 0, no trend with slope, aspect, elevation, or position, and a distribution whose spread (use the NMAD, robust to outliers) defines $\sigma_{\Delta z}$ as a function of terrain attributes. *Aspect test*: plot $\Delta z / \tan\alpha$ against aspect; a cosine is residual horizontal shift (Nuth & Kääb 2011). *Variogram*: compute the empirical variogram of stable-terrain residuals out to several kilometres; fit nested models; derive $n_{\text{eff}}$ for the area of interest. *Independent checks*: GNSS or TLS at a few locations within the active area, surveyed at both epochs, give a direct validation of $\Delta z$ at points; scour chains or sediment traps validate gross vs net. *Closure*: for a confined slide or an excavation of known volume (haul records), compare the DoD volume with the independent figure.

**What to report.** Epoch dates and seasons; sensors, densities, and ground-filter methods for both surfaces; co-registration method, stable mask definition, and residual statistics; the error model (global, binned, or fuzzy) and its calibration; LoD and confidence level; variogram parameters and $n_{\text{eff}}$; erosion, deposition, and net volumes each with intervals; bulk density if converting to mass; treatment of wetted or void areas; and anthropogenic change classified separately.

> **Uncertainty budget.** Volumetric budget for a 2 km gravel-bed reach (active area 0.8 km²), airborne lidar 2015 and 2021, 8 pt/m².
>
> | Term | Value | Basis |
> |---|---|---|
> | σ₁, σ₂ (bare, flat) | 0.05 m each | Stable-terrain NMAD |
> | σ₁, σ₂ (banks > 20°, vegetated) | 0.18 m each | Binned residuals |
> | σ_Δz (flat / banks) | 0.07 / 0.25 m | RSS |
> | LoD₉₅ (flat / banks) | 0.14 / 0.50 m | 1.96 σ |
> | Co-registration residual (post Nuth–Kääb) | 0.01 m vertical, 0.15 m horizontal | Stable terrain |
> | Correlation range (nested) | 40 m (sensor); 600 m (flight lines/control) | Variogram |
> | n_eff for 0.8 km² | ≈ 800 (short) ; ≈ 3 (long) | A/(κL²), κ ≈ π/5 |
> | Erosion (thresholded) | 61 000 m³ ± 7 000 (95 %) | Sum + correlation |
> | Deposition (thresholded) | 47 000 m³ ± 6 000 | |
> | Net | −14 000 m³ ± 10 000 | 95 % interval −4 000 to −24 000 m³ |
> | Wetted channel (no data) | 12 % of active area | Unknown; stated |
>
> The long-range correlation term, with $n_{\text{eff}}$ ≈ 3, dominates the net volume uncertainty (0.01 m/√3 × 0.8 km² ≈ 4 600 m³ at 1σ, ≈ 9 000 m³ at 95 %); the short-range term alone would give only ≈ ±4 000 m³ and the conclusion would be falsely precise.

## Software

**Open source:** **GCD** (Geomorphic Change Detection; Riverscapes Consortium — the reference implementation of Wheaton et al. 2010 with fuzzy-inference error surfaces, probabilistic thresholding, and budget segregation; standalone and ArcGIS add-in; caveat: the standalone version lags the add-in); **xdem** (co-registration, heteroscedastic error, variograms, $n_{\text{eff}}$; the Hugonnet et al. method); **py4dgeo** and **CloudCompare** (M3C2 for point clouds; [Chapter 41](ch41-change-detection.md)); **LSDTopoTools**, **TopoToolbox** (MATLAB), **Landlab** (Python), **WhiteboxTools** (morphometrics, channel extraction, knickpoint analysis; caveat: each uses its own slope/flow algorithms — state which); **GRASS GIS** (`r.slope.aspect`, `r.watershed`, `r.series` for time stacks); **GDAL** (`gdal_calc.py`, `gdaldem`); **R** packages `terra`, `whitebox`, `rgee` for scripted DoD and morphometrics.

**Free but closed:** **DSAS** (USGS; ArcGIS Pro add-in, v5.1+, for shoreline-change rates with regression statistics; caveat: requires an ArcGIS licence); **Coastal Toolkits** from various agencies.

**Commercial:** **ArcGIS Pro** (Cut Fill, raster calculator, Surface Difference; caveat: no built-in LoD or correlation-aware uncertainty); **Global Mapper** (volume between surfaces; same caveat); **Trimble Business Center** and **Leica Infinity** earthwork modules (volumes for construction; uncertainty is not reported); **TerraSolid TerraModeler** (surface differencing at production scale).

## Standards & guides

- **USGS DSAS v5.1 User Guide** (Himmelstoss et al. 2021, OFR 2021-1091) — transect casting, rate statistics, uncertainty of shoreline positions.
- **USACE EM 1110-2-4000**, *Sedimentation Investigations of Rivers and Reservoirs* (1989; check for current revision) — reservoir survey methods and capacity computation.
- **Riverscapes Consortium GCD documentation** (current) — error-surface construction, thresholding options, budget segregation.
- **FGDC Shoreline Metadata Profile** (FGDC-STD-001.2-2001) — required attributes for shoreline proxies, tide stage, datum.
- **USGS Lidar Base Specification** (current ed.) — defines the DTM products most repeat-lidar DoDs are built from; relevant to surface-definition consistency.
- **IHO S-44** (ed. 6.1.0) — uncertainty requirements for the bathymetric surveys used in nearshore and reservoir change.
- **WGMS Guidelines for geodetic mass-balance reporting** (Zemp et al. 2013 and WGMS practice) — density conversion, uncertainty components.

## Pitfalls

- **Reporting change below the LoD** → the DoD looks like a map and every pixel has a value → threshold; show the unthresholded map only alongside the σ surface.
- **Summing volumes with independent-cell statistics** → $\sqrt{n}$ is seductive → compute $n_{\text{eff}}$ from the variogram; report nested ranges.
- **Comparing DEMs with different ground definitions** → DSM vs DTM, leaf-on vs leaf-off, grass, snow, water → match surface definitions and seasons; mask what cannot be matched.
- **Mistaking co-registration shift for erosion on slopes** → aspect-dependent bias → Nuth–Kääb test before any interpretation.
- **Comparing morphometrics across resolutions** → slope, roughness, drainage density all drift with cell size → fix the resolution and the algorithm.
- **Reading a two-epoch rate as a landscape property** → rates are event histories → report the interval's known events; prefer multi-epoch.
- **Stable mask that is not stable** → includes slowly changing surfaces → test residuals vs distance from the active area and land cover.
- **Ignoring the wetted channel** → no data is not zero change → mask it and state the fraction.
- **Shoreline proxies switched mid-series** → HWL vs MHW vs vegetation line → record the proxy per shoreline; apply the proxy-datum bias correction.
- **Radar DEM over firn used as a surface** → penetration of metres → correct or avoid; never difference radar against lidar in accumulation zones without a penetration model.
- **Reservoir capacity loss computed against an unreconciled pre-impoundment map** → old datum, half-contour accuracy → reconcile datums; carry the old map's uncertainty.
- **Including the gravel pit in the river budget** → anthropogenic change not classified → segregate by semantic context and edge sharpness.

## Key takeaways

- Change is a difference of two uncertain surfaces; co-register first, estimate σ spatially, threshold by LoD, and only then interpret.
- Volume uncertainty is governed by spatial correlation, not cell count; $n_{\text{eff}}$ from a variogram is mandatory, and long-range terms usually dominate net budgets.
- Report erosion, deposition, and net separately with intervals; net hides gross, and a net smaller than its interval is not equilibrium.
- Most geomorphic work is done by rare events; a two-epoch rate is the interval's event history.
- Surface definition (season, vegetation, water, DSM/DTM, radar penetration) is the most common source of false change in mixed-sensor comparisons.
- Many "erosion" signals are datum, registration, or proxy artefacts until proven otherwise.
- Morphometrics are resolution-dependent by nature; compare like with like.
- Humans move more sediment than rivers; classify anthropogenic change and keep it out of the natural budget.

## References

- Berthier, E., Floricioiu, D., Gardner, A. S., Gourmelen, N., Jakob, L., Paul, F., Treichler, D., Wouters, B., Belart, J. M. C., Dehecq, A., Dussaillant, I., Hugonnet, R., Kääb, A., Krieger, L., Pálsson, F. & Zemp, M. (2023). Measuring glacier mass changes from space — a review. *Reports on Progress in Physics*, 86:036801. doi:10.1088/1361-6633/acaf8e
- Brasington, J., Langham, J. & Rumsby, B. (2003). Methodological sensitivity of morphometric estimates of coarse fluvial sediment transport. *Geomorphology*, 53(3–4):299–316. doi:10.1016/S0169-555X(02)00320-3
- Dehecq, A., Millan, R., Berthier, E., Gourmelen, N., Trouvé, E. & Vionnet, V. (2016). Elevation changes inferred from TanDEM-X data over the Mont-Blanc area: Impact of the X-band interferometric bias. *IEEE JSTARS*, 9(8):3870–3882.
- Himmelstoss, E. A., Henderson, R. E., Kratzmann, M. G. & Farris, A. S. (2021). *Digital Shoreline Analysis System (DSAS) version 5.1 user guide*. USGS Open-File Report 2021-1091. doi:10.3133/ofr20211091
- Hooke, R. LeB. (2000). On the history of humans as geomorphic agents. *Geology*, 28(9):843–846.
- Hugonnet, R., McNabb, R., Berthier, E., Menounos, B., Nuth, C., Girod, L., Farinotti, D., Huss, M., Dussaillant, I., Brun, F. & Kääb, A. (2021). Accelerated global glacier mass loss in the early twenty-first century. *Nature*, 592:726–731. doi:10.1038/s41586-021-03436-z
- Hugonnet, R., Brun, F., Berthier, E., Dehecq, A., Mannerfelt, E. S., Eckert, N. & Farinotti, D. (2022). Uncertainty analysis of digital elevation models by spatial inference from stable terrain. *IEEE JSTARS*, 15:6456–6472. doi:10.1109/JSTARS.2022.3188922
- Huss, M. (2013). Density assumptions for converting geodetic glacier volume change to mass change. *The Cryosphere*, 7:877–887. doi:10.5194/tc-7-877-2013
- James, L. A., Hodgson, M. E., Ghoshal, S. & Latiolais, M. M. (2012). Geomorphic change detection using historic maps and DEM differencing: The temporal dimension of geospatial analysis. *Geomorphology*, 137(1):181–198. doi:10.1016/j.geomorph.2010.10.039
- James, M. R. & Robson, S. (2012). Straightforward reconstruction of 3D surfaces and topography with a camera: Accuracy and geoscience application. *Journal of Geophysical Research: Earth Surface*, 117:F03017.
- Lane, S. N., Chandler, J. H. & Richards, K. S. (1994). Developments in monitoring and modelling small-scale river bed topography. *Earth Surface Processes and Landforms*, 19(4):349–368.
- Lane, S. N., Westaway, R. M. & Hicks, D. M. (2003). Estimation of erosion and deposition volumes in a large, gravel-bed, braided river using synoptic remote sensing. *Earth Surface Processes and Landforms*, 28(3):249–271. doi:10.1002/esp.483
- Morton, R. A. & Miller, T. L. (2005). *National assessment of shoreline change: Part 2, Historical shoreline changes and associated coastal land loss along the U.S. Southeast Atlantic Coast*. USGS Open-File Report 2005-1401.
- Mudd, S. M., Attal, M., Milodowski, D. T., Grieve, S. W. D. & Valters, D. A. (2014). A statistical framework to quantify spatial variation in channel gradients using the integral method of channel profile analysis. *Journal of Geophysical Research: Earth Surface*, 119(2):138–152.
- Nuth, C. & Kääb, A. (2011). Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere*, 5:271–290. doi:10.5194/tc-5-271-2011
- Passalacqua, P., Belmont, P., Staley, D. M., Simley, J. D., Arrowsmith, J. R., Bode, C. A., Crosby, C., DeLong, S. B., Glenn, N. F., Kelly, S. A., Lague, D., Sangireddy, H., Schaffrath, K., Tarboton, D. G., Wasklewicz, T. & Wheaton, J. M. (2015). Analyzing high resolution topography for advancing the understanding of mass and energy transfer through landscapes: A review. *Earth-Science Reviews*, 148:174–193. doi:10.1016/j.earscirev.2015.05.012
- Rolstad, C., Haug, T. & Denby, B. (2009). Spatially integrated geodetic glacier mass balance and its uncertainty based on geostatistical analysis: application to the western Svartisen ice cap, Norway. *Journal of Glaciology*, 55(192):666–680.
- Ruggiero, P. & List, J. H. (2009). Improving accuracy and statistical reliability of shoreline position and change rate estimates. *Journal of Coastal Research*, 25(5):1069–1081.
- Schwanghart, W. & Scherler, D. (2014). TopoToolbox 2 — MATLAB-based software for topographic analysis and modeling in Earth surface sciences. *Earth Surface Dynamics*, 2:1–7.
- Shugar, D. H., Jacquemart, M., Shean, D., et al. (2021). A massive rock and ice avalanche caused the 2021 disaster at Chamoli, Indian Himalaya. *Science*, 373(6552):300–306. doi:10.1126/science.abh4455
- Westoby, M. J., Brasington, J., Glasser, N. F., Hambrey, M. J. & Reynolds, J. M. (2012). 'Structure-from-Motion' photogrammetry: A low-cost, effective tool for geoscience applications. *Geomorphology*, 179:300–314.
- Wheaton, J. M., Brasington, J., Darby, S. E. & Sear, D. A. (2010). Accounting for uncertainty in DEMs from repeat topographic surveys: improved sediment budgets. *Earth Surface Processes and Landforms*, 35(2):136–156. doi:10.1002/esp.1886
- Wilkinson, B. H. & McElroy, B. J. (2007). The impact of humans on continental erosion and sedimentation. *GSA Bulletin*, 119(1–2):140–156. doi:10.1130/B25899.1
- Wolman, M. G. & Miller, J. P. (1960). Magnitude and frequency of forces in geomorphic processes. *Journal of Geology*, 68(1):54–74.
- Zemp, M., Thibert, E., Huss, M., Stumm, D., Rolstad Denby, C., Nuth, C., Nussbaumer, S. U., Moholdt, G., Mercer, A., Mayer, C., Joerg, P. C., Jansson, P., Hynek, B., Fischer, A., Escher-Vetter, H., Elvehøy, H. & Andreassen, L. M. (2013). Reanalysing glacier mass balance measurement series. *The Cryosphere*, 7:1227–1245. doi:10.5194/tc-7-1227-2013
- Zhang, W. & Montgomery, D. R. (1994). Digital elevation model grid size, landscape representation, and hydrologic simulations. *Water Resources Research*, 30(4):1019–1028.

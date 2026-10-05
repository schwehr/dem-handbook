# Chapter 65 — Mining, landfills, construction, and engineered earthworks

> **Part XIV — Domain deep dives.** The chapter where a cubic metre has a price, a signature, and sometimes a court date: how volumes are computed from surfaces, why the base surface dominates the error budget, and how the industries that move earth survey, certify, and monitor it.

**In this chapter.** Mines, landfills, quarries, and construction sites are the most intensively re-surveyed terrain on Earth, and the quantities derived from those surveys—stockpile tonnages, pay-item cut and fill, remaining landfill airspace, resource depletion—are legal and financial numbers. You will be able to compute a volume between two surfaces by prism, end-area, and TIN methods; recognize that the *base surface* and the *material density*, not top-surface noise, usually dominate volumetric uncertainty; and propagate spatially correlated elevation error into a defensible volume interval. The chapter covers the survey methods and cadences used in practice (UAV structure-from-motion and its doming failure mode, terrestrial and mobile scanners, machine-control as-builts, satellite stereo, InSAR for tailings dams), the standards and licensure rules that make a volume admissible, and the peculiar surface semantics of these sites—trucks on piles, vertical highwalls, fluid tailings, steam, and dust—so that you can specify, check, and defend a volume to a stated uncertainty, and know when continuous monitoring rather than periodic survey is the only responsible choice.

## 65.1 Volume computation

### 65.1.1 Prisms, end areas, and TINs

Every earthwork volume is the integral of the difference between two surfaces over a footprint:

$$V = \iint_{\Omega} \left[ z_{\text{top}}(x,y) - z_{\text{base}}(x,y) \right] \, dA .$$

Three discretizations of this integral are in daily use.

The **grid prism method** evaluates both surfaces on a common raster and sums $V = \sum_i A_i (z_{\text{top},i} - z_{\text{base},i})$, with $A_i$ the cell area. It is a **DEM of Difference (DoD)** multiplied by cell area ([Chapter 41](ch41-change-detection.md)) and is exact for the piecewise-constant surfaces it assumes. Its errors are those of resampling—both surfaces must be on the *same* grid with the *same* registration ([Chapter 31](ch31-interpolation-and-gridding.md))—and of boundary quantization to whole cells, which matters for small piles on coarse grids (a 1 m grid on a 30 m × 30 m stockpile has roughly 120 edge cells out of 900).

The **TIN prism method** builds a *merged* TIN containing the breaklines and vertices of both surfaces so that each triangle has a planar top and base; each prism contributes $A_t \cdot \bar{d}_t$, with $\bar{d}_t$ the mean of the three vertex differences. It honors breaklines (toes, crests, berm edges) exactly, which is why licensed surveyors' quantities are almost always TIN-based; its weakness is that triangulation is not unique, and two packages given the same points can differ by a fraction of a percent on steep features.

The **average end-area method** is the classical highway and pipeline method: cross-sections at stations $L$ apart, cut and fill areas $A_1, A_2$ measured on each, and $V = L (A_1 + A_2)/2$ between sections. It overestimates a tapering (pyramid- or cone-shaped) feature by up to 50 % in the limit; the **prismoidal formula** $V = L (A_1 + 4A_m + A_2)/6$, with $A_m$ the mid-station area, is exact for second-order surfaces. Many construction contracts still specify end-area quantities, so you must be able to reproduce end-area numbers from a DEM to resolve a dispute even when the DEM-based number is better.

| Method | Honors breaklines | Needs common grid | Typical use | Characteristic error |
|---|---|---|---|---|
| Grid prism (DoD) | No (unless burned in) | Yes | Change detection, mine-wide budgets | Edge quantization, resampling |
| TIN prism | Yes | No | Stamped stockpile/cut-fill quantities | Triangulation ambiguity on steep faces |
| Average end area | Via section lines | No | Linear works, legacy contracts | Up to tens of % on tapering features if sections sparse |
| Prismoidal | Via section lines | No | Precise linear works | Small if sections capture curvature |

### 65.1.2 The base surface: the biggest uncertainty

Suppliers of volume software advertise the precision of the top surface; the quantity that actually decides whether a stockpile is 48,000 or 52,000 m³ is the **base surface**—the ground the material sits on. There are four ways to define it, in descending order of defensibility.

A **pre-placement survey** of the bare pad, tied to the same control as the later surveys, is the gold standard; archive it with the control report, because the pad will not be visible again while the pile exists. A **design pad surface** from drawings is acceptable only if an as-built confirms the pad was built to it—pads settle, are regraded by loaders, and accumulate "floor" material that is never reclaimed. A **toe-line interpolation**—digitizing the visible edge of the pile and interpolating a surface (planar, TIN, or minimum-curvature) across the footprint—is what most UAV volume tools do by default; it is adequate on a flat, hard pad and badly wrong on sloping or irregular ground, because it assumes the ground under the pile continues smoothly from the ground around it. A **constant base elevation** (lowest toe point, or one plane) is a last resort to be disclosed as such.

The sensitivity of the volume to a base-surface bias $\delta_b$ is exactly the footprint area: $\partial V / \partial \delta_b = -A$. For a 50,000 m³ pile on an 8,000 m² footprint, a 10 cm base error is 800 m³ (1.6 %)—more than the entire random error of a well-executed UAV survey. Floor material (product mixed with pad material that the loader cannot recover) is usually 0.1–0.3 m and is the commonest cause of inventory write-downs when a pile is finally cleared ("book-to-physical" reconciliation). On a sloping pad the toe itself is ambiguous: material spills downslope, and the low-side toe may be metres from where the product actually rests.

> **Definitions that bite.** *Toe line* in a stockpile survey is the polygon where the pile meets the base surface, inside which the volume is computed; in a geotechnical report it is the bottom edge of a slope face, and in a dump design the bottom of the final lift. A toe digitized from an orthomosaic generally lies *outside* the true contact because of spillage and fines; one picked by a slope-break algorithm on the DSM lies *inside* it. Two surveyors can draw toes differing by 1–2 m in plan, which on a 6 m-high pile edge of 350 m perimeter is 2,000–4,000 m³. State how the toe was defined, by whom, and from what data.

### 65.1.3 Stockpile delineation and surface semantics

Within the footprint the top surface must be the *material*, not what sits on it. Loaders, trucks, conveyors, and stacker booms inflate volumes—a 40 t haul truck occupies roughly 60–80 m³ of DSM; ponded water in a depression is counted as material by any surface method; adjacent piles that have slumped together need a dividing line that is partly judgment; vegetated long-term dumps need DTM extraction with all the problems of [Chapter 32](ch32-dsm-to-dtm.md); dust and steam produce noise or voids ([Section 65.9](#659-pitfalls-particular-to-engineered-surfaces)). Every stockpile survey therefore needs a surface-classification step, however light, and a record of what was removed.

### 65.1.4 Correlated error and volume uncertainty

The honest uncertainty of a DoD volume is treated in [Chapter 40](ch40-erosion-and-geomorphic-change.md) and [Chapter 41](ch41-change-detection.md); here the application is condensed. If per-cell differences had independent standard deviation $\sigma_d$, the volume uncertainty over $n$ cells of area $a$ would be $\sigma_V = a \sigma_d \sqrt{n}$—negligible for any realistic survey (1 m grid, $\sigma_d$ = 5 cm, 8,000 cells: 4.5 m³). That number is wrong because elevation errors are spatially correlated: a base-station height error, an SfM dome, a lever-arm or boresight error moves whole regions together. With an error correlation length $L$ (the semivariogram range), the effective number of independent samples over footprint area $A$ is roughly $n_{\text{eff}} \approx A / (\pi L^2)$, and

$$\sigma_V \approx A \, \sigma_d \, \sqrt{\frac{1 + (n-1)\bar\rho}{n}} \;\approx\; A\,\sigma_d \big/ \sqrt{n_{\text{eff}}} ,$$

where $\bar\rho$ is the mean pairwise correlation across the footprint. For a fully correlated error ($L \gg$ footprint) this reduces to $\sigma_V = A \sigma_d$—the whole footprint moves together, exactly as a base-surface bias does. Rolstad et al. (2009) and Anderson (2019) give the derivation; the practical message is that volume uncertainty is set by the *long-wavelength* error, which a single survey cannot see about itself and only independent control reveals.

> **Worked example.** *Uncertainty of a 50,000 m³ stockpile volume from a UAV SfM survey.* Footprint area $A$ = 8,000 m², mean thickness 6.25 m. Check points on the pad give an RMSE$_z$ of 0.05 m for the top surface against RTK GNSS, with a residual semivariogram range of about 10 m (typical of SfM texture noise plus local tie-point density). Independent components:
>
> 1. Random/short-correlation surface error: $n_{\text{eff}} \approx 8000 / (\pi \cdot 10^2) \approx 25$; $\sigma_{V,1} \approx 8000 \times 0.05 / \sqrt{25}$ = **80 m³** (0.16 %).
> 2. Long-wavelength SfM error (residual dome after GCP adjustment): from the check-point residual *trend*, estimated as a 0.04 m systematic offset over the pile: $\sigma_{V,2} = 8000 \times 0.04$ = **320 m³** (0.64 %).
> 3. Base surface: the pad was surveyed before placement with RTK (σ = 0.02 m), but floor material of 0.05 ± 0.05 m is suspected: bias −400 m³, $\sigma_{V,3} = 8000 \times \sqrt{0.02^2 + 0.05^2}$ ≈ **430 m³** (0.86 %).
> 4. Toe delineation: ±1 m in plan along a 350 m perimeter at a 2 m mean edge height: $\sigma_{V,4} \approx 350 \times 1 \times 2 \times 0.5$ ≈ **350 m³** (0.7 %) (the 0.5 reflects the triangular edge profile).
> 5. Excluded objects: one loader (70 m³) removed; residual **20 m³**.
>
> Combined (root-sum-square, assuming independence): $\sigma_V \approx \sqrt{80^2 + 320^2 + 430^2 + 350^2 + 20^2}$ ≈ **650 m³**, i.e., 1.3 % at 1σ, about 2.6 % at 95 %. Converting to tonnes with a bulk density of 1.60 ± 0.08 t/m³ (5 % at 1σ—a *modest* figure for a moist, partly compacted aggregate): $M$ = 80,000 t with $\sigma_M / M = \sqrt{0.013^2 + 0.05^2}$ ≈ 5.2 %. The density term dominates by a factor of four; the top-surface precision that the software reported (0.05 m) contributes almost nothing. Report: $V$ = 49,600 m³ (after floor correction) ± 1,300 m³ (95 %); $M$ = 79,000 ± 8,000 t (95 %); base surface = pre-placement RTK survey of 2024-03-11; toe digitized on orthomosaic by J. Doe; density from 12 sand-cone tests on 2024-06-02.

### 65.1.5 Density and tonnage

Volumes are measured; tonnes are paid for. The conversion $M = \rho_b V$ uses a **bulk density** that varies with material, moisture, compaction, and height within the pile. In-place densities (sand-cone ASTM D1556, nuclear gauge ASTM D6938, or weighed trucks over a known volume) typically scatter by 3–10 % within one pile. **Swell** and **shrink** factors convert bank (in situ), loose (hauled), and compacted (placed) volumes—a bank cubic metre of common earth is roughly 1.2–1.3 loose and 0.9–0.95 compacted, with wide variation—and the contract must state which state is the pay quantity. Hygroscopic products (coal fines, some ores, fertilizer) change height and density with the weather, so a survey after a storm can differ by several percent in tonnes with no material moved ([Section 65.9](#659-pitfalls-particular-to-engineered-surfaces)).

<!-- figure: Figure 65.1 — Cross-section of a stockpile showing the four candidate base surfaces (pre-placement survey, design pad, toe-line interpolation, constant plane), the floor-material layer, spillage beyond the true contact, and the resulting volume differences for each choice. -->

## 65.2 Survey methods and cadence

### 65.2.1 UAV structure-from-motion

Since about 2013, when consumer multirotors with stabilized cameras met commodity SfM software, UAV photogrammetry has been the default stockpile and site-survey method ([Chapter 22](ch22-photogrammetry-sfm.md)). A 15–30 minute flight at 60–120 m above ground yields a 2–4 cm ground sample distance (GSD), a dense point cloud, a DSM, and an orthomosaic for 20–80 ha; weekly or daily flights are routine at large sites, some from docked autonomous drones.

Georeferencing is by **ground control points (GCPs)** surveyed with RTK/static GNSS or total station, or by **direct georeferencing** with onboard RTK/PPK GNSS tagging each exposure. Direct georeferencing removes the target labor but moves the control problem into the camera–antenna lever arm, exposure synchronization, and interior orientation; because camera-model errors map almost entirely into the vertical, a PPK-only block still needs check points to prove its height. Precision maps (James, Robson, and Smith 2017) show that PPK nadir blocks are weakest in height at the edges and corners and that one or two GCPs, or oblique imagery, suffice to constrain the datum shift and tilt the GNSS cannot.

**Doming** is the characteristic systematic error of self-calibrated SfM blocks. When radial lens distortion is poorly determined—typical of a nadir-only, parallel-strip block over a flat site—the bundle adjustment trades distortion against a smooth deformation of the surface, which bows into a dome or bowl across the block. James and Robson (2014) demonstrated the mechanism and showed that convergent (10–20° off-nadir) images, or a second flight at a different altitude or heading, break the correlation and remove most of the dome; GCPs spread over the block and on the pile do the rest. A 0.1–0.3 m dome over a 300 m block is not unusual in uncorrected nadir blocks and adds 800–2,400 m³ (1.6–4.8 %) to the worked example's pile—the largest error a UAV survey can make while looking perfect. Detect it by check-point residuals that trend with distance from the block center, by a DoD against a previous survey that shows a smooth bowl over unchanged haul roads and pads, and by a repeat flight with crossed grid and obliques that disagrees with the nadir block.

> **Try it.** Compute a stockpile volume and its sensitivity to the base surface with open-source tools. Start from a classified point cloud (`site.laz`) from WebODM or MicMac, with GCP control, and a toe polygon (`toe.gpkg`). PDAL grids the top surface; GDAL and NumPy do the volume on two candidate bases.
>
> ```bash
> # 1. Ground-only DSM of the pile top at 0.25 m (class 2 = ground incl. pile; 
> #    vehicles/noise already classified out).
> pdal pipeline - <<'EOF'
> {
>   "pipeline": [
>     "site.laz",
>     {"type":"filters.range","limits":"Classification[2:2]"},
>     {"type":"writers.gdal","filename":"top.tif","resolution":0.25,
>      "output_type":"idw","window_size":3,"gdaldriver":"GTiff"}
>   ]
> }
> EOF
> # 2. Clip to the toe polygon; same grid for base surfaces.
> gdalwarp -cutline toe.gpkg -crop_to_cutline -dstnodata -9999 top.tif top_clip.tif
> gdalwarp -cutline toe.gpkg -crop_to_cutline -dstnodata -9999 \
>          -te_srs EPSG:32610 pad_preplacement.tif base_pad.tif
> ```
>
> ```python
> import numpy as np, rasterio
> from scipy.interpolate import griddata
> with rasterio.open("top_clip.tif") as t, rasterio.open("base_pad.tif") as b:
>     top = t.read(1, masked=True); a = abs(t.res[0]*t.res[1])
>     base_pad = b.read(1, masked=True)
> # Candidate 2: toe-line interpolation from the top surface's own edge cells.
> edge = np.ma.getmaskarray(top) ^ np.roll(np.ma.getmaskarray(top), 1, 0)  # crude ring
> yy, xx = np.nonzero(edge & ~np.ma.getmaskarray(top))
> base_toe = griddata((yy, xx), top[yy, xx], tuple(np.indices(top.shape)), method="linear")
> for name, base in [("pre-placement pad", base_pad), ("toe interpolation", base_toe)]:
>     d = np.ma.masked_invalid(top - base)
>     V = float((d.filled(0) * a).sum()); A = float((~d.mask).sum() * a)
>     print(f"{name:20s} V = {V:9.0f} m3   A = {A:7.0f} m2   dV/dz_base = {-A:.0f} m3 per m")
> ```
>
> Expected outcome: two volumes that differ by hundreds to thousands of cubic metres for a typical pile on an imperfect pad, and a printed sensitivity equal to the footprint area—so a 0.1 m base uncertainty maps directly to 0.1 × A m³. Replace the crude edge ring with the surveyed toe points for production work.

### 65.2.2 Terrestrial and mobile scanners

**Terrestrial laser scanners (TLS)** give millimetre-to-centimetre range precision at 100–1,000 m and remain the reference method for pit walls, highwalls, and stockpiles in sheds or under conveyors ([Chapter 18](ch18-topographic-lidar.md)). Their weaknesses are occlusion—the far side of a pile is invisible from one setup—and registration between setups, which accumulates error along a long pit unless tied to control. Permanently mounted scanners on pit rims or stockyard gantries acquire the same scene every few minutes and underpin several "continuous inventory" systems. **Mobile mapping systems** on haul trucks or light vehicles ([Chapter 16](ch16-platforms.md)) survey roads and benches during normal operation with the accuracy of their trajectory, which in a deep pit with GNSS masked above 30–40° elevation degrades rapidly without ground control or scan-to-scan registration ([Chapter 13](ch13-imu-ins.md)).

### 65.2.3 Machine control and as-built surfaces

Dozers, graders, excavators, and drills carry **machine-control** GNSS (RTK from a site base, dual antennas for heading, blade sensors for cutting-edge position) and record blade or bucket position continuously. The resulting **as-built surface**—the envelope of blade positions—has centimetre precision relative to the site base, is available in near real time, and is biased in specific ways: it records where the *blade* was, not where the ground *settled*; it misses material tipped by uncontrolled trucks until a controlled machine passes over it; and it inherits the site **calibration** (the localization from the RTK base to the project system) wholesale. A localization error—a wrong geoid model, an old benchmark, a combined-scale-factor mistake ([Section 65.3](#653-standards-and-legal))—moves every machine-control surface by the same amount, invisibly to any internal comparison. Models are exchanged as **LandXML** TINs or proprietary files; design, as-built, and independent check survey must be reduced to one datum before any quantity is computed.

### 65.2.4 Satellite stereo and InSAR

For remote mines and long-term dump growth, **satellite stereo** (WorldView, Pléiades, SPOT; [Chapter 22](ch22-photogrammetry-sfm.md)) gives DSMs at 0.5–2 m posting with 1–3 m vertical accuracy without GCPs—adequate for mine-wide reconciliation at the percent level and for detecting undisclosed waste expansion, not for stamped inventories. **InSAR** ([Chapter 21](ch21-radar-sar-insar.md)) measures not volume but line-of-sight displacement at millimetres per year, which makes it the tool for **subsidence** over underground workings, **dewatering** compaction, and **tailings dam** deformation; persistent-scatterer and small-baseline time series from Sentinel-1 (6–12-day revisit, C-band) and X-band commercial sensors (TerraSAR-X, COSMO-SkyMed, ICEYE) are now the standard screening method for dam movement.

> **Case file.** *Brumadinho, Brazil, 25 January 2019.* Dam I of Vale's Córrego do Feijão iron mine, an upstream-raised tailings dam inactive since 2016, liquefied and failed, releasing on the order of 10 million m³ of tailings and killing roughly 270 people. Post-event analyses of Sentinel-1 time series (Gama et al. 2020, SBAS and PSI) and of combined Sentinel-1/TerraSAR-X data (Grebby et al. 2021) found deformation on the dam face in the preceding months, accelerating toward the end—millimetres to a few centimetres per year, small in absolute terms but anomalous for a supposedly static structure. Ground-based radar and inclinometers were installed, but the monitoring and its interpretation did not trigger evacuation. The lessons ([Chapter 56](ch56-case-files.md)) are that an inactive dam is not a static one; that displacement, not elevation, is the right observable for dam safety; that InSAR screening of every upstream dam is cheap relative to the consequence; and that a monitoring system is only as good as the decision rule attached to it. The GISTM (2020) followed the next year ([Section 65.7](#657-tailings-and-dams)).

### 65.2.5 Choosing a cadence

Cadence should follow the rate of change and the cost of being wrong. Month-end quarry inventories are UAV flights with GCPs; daily progress on a large earthworks job is machine control plus a weekly UAV check; a pit wall with a known instability is watched by slope radar at minutes-scale cadence; a tailings dam by piezometers, GNSS, and InSAR at days-to-weeks cadence with a quarterly survey. Keep the *reference* survey—the one everything is differenced against—at the highest standard and re-observe it on a fixed schedule rather than letting the datum drift through a chain of relative surveys.

<!-- figure: Figure 65.2 — Illustration of SfM doming: cross-section of a flat haul road reconstructed from a nadir-only parallel-strip block (bowed by ~0.2 m) versus the same block with added oblique images and GCPs (flat), with the check-point residual-versus-distance plot that reveals the dome. -->

## 65.3 Standards and legal

### 65.3.1 Licensure and the stamped volume

In most jurisdictions a volume used to settle a contract, support a financial statement, or satisfy a regulator must be certified by a **licensed (registered, chartered) surveyor** or professional engineer who takes personal legal responsibility for it. Several US state boards have ruled that producing volumetric quantities from UAV data for a fee is the practice of land surveying; details vary by state, and the drone operator, the SfM processor, and the signer are often three people. The signature attaches to the *method*: the control (datum, epoch, benchmarks or CORS held fixed), the instrument and its calibration (ISO 17123 field procedures), the surface definitions (top, base, toe), the computation method, and—increasingly—an uncertainty statement. A volume without those is an estimate, whatever software produced it.

### 65.3.2 Mineral resource reporting

Public mining companies report resources and reserves under the **JORC Code** (2012 edition; Australasia), Canada's **NI 43-101** with the CIM Definition Standards (2014), South Africa's SAMREC, and the CRIRSCO template that aligns them. Topography enters twice. The **pit surface** at the reporting date defines what has been mined and depletes the resource model; an out-of-date or mis-registered topography overstates remaining tonnes. **Stockpile inventories** are reported in their own right, with survey volume, density, and grade each carrying stated confidence. The Competent/Qualified Person must discuss the "quality and adequacy of topographic control" (JORC Table 1), so the surveyor's report becomes an appendix to a securities filing.

### 65.3.3 Landfill airspace and capacity reports

A landfill's commercial value is its remaining permitted **airspace**: the volume between the current waste surface and the permitted final-contour surface (in cubic yards in the US). Operators report consumed and remaining airspace to regulators (RCRA Subtitle D, 40 CFR Part 258, and state rules that typically require an annual topographic survey and capacity certification) and to finance, where airspace is amortized against tonnage. The **airspace utilization factor (AUF)**—tonnes received per cubic metre consumed—is the key efficiency metric; its numerator comes from scale tickets and its denominator from the difference between two surveys, so a 2 % volume error in a cell receiving 500,000 t/yr shifts the apparent AUF by 2 % and the projected site life by months. Because the final-contour surface is a *permit* surface in the permit's datum—sometimes decades old—airspace is a frequent site of datum error: a permit on NGVD 29 against a survey on NAVD 88 is off by the local shift (tens of centimetres in much of the US) over the whole footprint, i.e., hundreds of thousands of cubic metres on a 40 ha cell.

### 65.3.4 Construction pay quantities

Earthwork contracts pay by the cubic metre (or yard) of excavation, embankment, or borrow, measured by survey, and disputes over pay quantities are among the commonest construction claims. Three details recur.

**Grid versus ground.** Projected coordinates carry a **grid scale factor** $k$ and, with ellipsoidal height $h$, an **elevation factor** $\approx R/(R+h)$; their product is the **combined scale factor (CSF)**, roughly 0.9997 (≈ 300 ppm) at 1,500 m elevation on a State Plane zone. Areas scale by CSF² (≈ 600 ppm) and so, since heights are not scaled, do volumes computed in grid coordinates: 0.06 %, a few hundred cubic metres per 500,000 m³. Many sites therefore use a **low-distortion projection** or a "ground" system (grid coordinates divided by the CSF and offset by a constant), and the standard failure is mixing design files in ground coordinates with survey files in grid, which produces both the scale error and a positional offset growing with distance from the projection origin—metres across a large site. [Chapter 10](ch10-projections-and-resampling.md) treats the geometry; contractually, the specification must name the system and the surveyor must state which one the quantity was computed in.

**Units and rounding.** US contracts use cubic yards (1 yd³ = 0.764555 m³) and frequently specify "neat-line" quantities (to design lines, regardless of over-excavation) rather than measured ones. Rounding rules—to the nearest 10 yd³ per section, or per station—can accumulate systematically if applied before summation.

**Independent surveys and dispute resolution.** The defense against a quantity dispute is a *jointly witnessed* pre-work survey with monumented, documented control and an agreed method statement. When disputes arise, an independent surveyor re-computes from the archived raw data—so the deliverable must include the point cloud or images and the control report, not just the TIN and the number. The commonest findings of such re-computations are an undisclosed change of base surface, a datum or scale-factor mismatch, and sections cut at different stations by the two parties.

### 65.3.5 Reclamation bonds

Mine operators post **reclamation bonds** sized to the cost of regrading, covering, and revegetating the disturbed area; in the US, the Surface Mining Control and Reclamation Act (SMCRA, 1977) requires coal sites to be returned to "approximate original contour" (AOC). Bond release depends on surveys showing the as-built landform meets the approved plan within tolerance, and the bond amount depends on the volume to be moved, so the pre-mining topography—often a 1970s–1990s photogrammetric map at 5-foot contour interval—is a legal reference surface of poor, undocumented accuracy. Where it is all that exists, its uncertainty (several metres vertically in steep, vegetated terrain) belongs in the bond calculation rather than assumed away.

## 65.4 Landfills and dumps

A landfill is designed to change continuously, settle for decades, generate gas, catch fire, and be worked on every hour. The **working face** advances by metres per day; **daily** and **intermediate cover** add 15–30 cm layers of soil, not waste, that must be separated in AUF accounting; the **final cover** (geomembrane, drainage, vegetative soil) is an engineered structure of its own.

**Settlement** is the distinguishing process. Municipal waste compacts and decomposes, and the surface subsides by 10–30 % of waste thickness over 20–30 years, fastest in the first years (Sowers' model separates primary mechanical settlement over months from secondary, biodegradation-driven settlement over decades). A DoD between annual surveys therefore measures airspace consumed by new waste *minus* airspace recovered by settlement of old waste; separating them needs a settlement model or markers (plates, GNSS monuments) on closed areas. Operators must also maintain final-cover grades for drainage and gas control—a settled depression ponds water and increases leachate—and lidar or UAV DTMs of closed cells every one to two years, compared with the design cover surface, are the standard compliance evidence.

**Gas and fires.** Landfill gas escapes at cracks and settlement features; subsurface fires produce localized subsidence of metres, thermal hot spots, and steam and smoke that corrupt SfM reconstructions ([Chapter 27](ch27-moving-and-transient-objects.md)). InSAR measures landfill settlement where coherence holds (closed, covered cells) and fails over active faces.

**Transient objects** are extreme at landfills: compactors, dozers, trucks, tipping loads, litter fences, and—at open dumps in much of the world—people and animals scavenging. Loose waste at the working face has roughly half the bulk density of compacted waste, so a survey that catches a day's tipping before compaction overstates airspace consumption. **Illegal dumping** is detected by DoD at the scale of a few truckloads (tens of cubic metres), which demands repeat surveys with vertical precision of a few centimetres over weeds, debris, and standing water; UAV SfM with permanent GCPs works and has been used in environmental enforcement. Tucci et al. (2019) give the full UAV workflow for a waste-stockpile volume, with photogrammetric–TLS comparison and error analysis.

> **Rule of thumb.** Count on compacted municipal waste at roughly 0.7–1.0 t/m³ in place (operator targets are often quoted as 1,200–1,500 lb/yd³) and on long-term settlement of 10–30 % of thickness; so a survey-derived AUF that is stable year to year across cells of very different ages is suspect, because the older cells should be giving airspace back. The rule breaks for inert-waste and construction-debris fills, which settle little, and for bioreactor landfills, which are designed to settle faster.

## 65.5 Construction sites

A construction site is a sequence of design surfaces realized in order—stripping, bulk earthworks, subgrade, pavement layers—each with a tolerance (typically ±15–30 mm for subgrade, ±5–10 mm for pavement layers, looser for bulk fill) checked by survey before the next is placed. Quantities are computed between successive as-builts and against design; the **earthwork balance** (cut equals fill within haul distance) is designed from the pre-construction DTM, and a 10 cm DTM error over a 50 ha site is 50,000 m³ of unbalanced material—several thousand truckloads.

**Design surfaces** arrive as LandXML TINs, IFC (Industry Foundation Classes) models in a BIM workflow, or proprietary machine-control files. **BIM-to-field** alignment is the recurrent problem: a building model in a local, un-projected system with origin at a grid intersection and "elevation 0" at finished floor must be placed in the site's projected system and vertical datum. IFC carries georeferencing (IfcMapConversion, since IFC4), but it is often empty or defaulted by the architect's software, and the misplacement is found only when the as-built does not fit. Every site should have one documented **site calibration**—the transformation from the GNSS frame to the project system—carried by every machine, rover, and scanner.

**Transients** on a construction site—cranes, scaffolding, formwork, laydown, cabins—appear as structures in a DSM and as change in a DoD; a tower crane's jib sweeps hundreds of square metres and sits in a different position in every survey. Scaffold around a rising building can make a photogrammetric DSM meaningless for progress, which is why progress measurement increasingly compares the point cloud with the BIM element by element (**scan-vs-BIM**). Slab flatness and levelness are checked by TLS at millimetre precision; [Chapter 63](ch63-buildings-cities-innerspace.md) covers the building side.

## 65.6 Open pits, quarries, underground

**Pit wall monitoring** is a safety function. **Slope stability radar** (ground-based real- or synthetic-aperture radar, commercial since the early 2000s) measures sub-millimetre line-of-sight displacement of a highwall every few minutes over a kilometre-scale face, with velocity and inverse-velocity alarms giving hours to days of warning; it is standard at large open pits. TLS adds geometry (bench and berm width, catch-bench integrity) and change in the radar's shadow. Highwalls are near-vertical or overhanging, so a 2.5D DEM represents them poorly ([Section 65.9](#659-pitfalls-particular-to-engineered-surfaces); [Chapter 35](ch35-voids-and-overhangs.md)); the right products are the point cloud, a mesh, or a projection onto a wall-parallel plane.

**Pit volumes** are differences between successive pit-surface models, typically monthly from UAV flights, reconciled against truck counts and the block model's depleted tonnes; the three rarely agree within a few percent, and the reconciliation report is where survey, truck-factor, and density errors are apportioned. **Dewatering** lowers the water table over kilometres and causes compaction subsidence of centimetres to decimetres, detectable by InSAR and levelling; in karst it causes sinkholes.

**Underground**, there is no GNSS and the survey is a traverse from surface control transferred down a shaft (plumb wires, gyro-theodolite, optical plummet), so uncertainty grows with distance from the shaft. **Cavity monitoring systems** (boom-mounted scanners lowered into a stope through a drill hole) measure **stope volumes** to compute dilution and overbreak against design—10,000–100,000 m³ with uncertainties of a few percent dominated by occlusion. Handheld **SLAM** scanners ([Chapter 15](ch15-slam.md)) map drives at walking speed with centimetre-to-decimetre drift per hundred metres unless closed on control; the same technology serves **cave surveys**, where loop closure against compass-and-tape stations is the only check available.

<!-- figure: Figure 65.3 — An open-pit cross-section with the quantities a monthly survey must separate: in-situ ore and waste mined (block model depletion), haul-road and ramp changes, highwall failure debris, ponded water at the sump, and the slope-radar and TLS fields of view on the highwall. -->

## 65.7 Tailings and dams

**Tailings storage facilities (TSFs)** are among the largest engineered structures on Earth and fail at a rate—Mount Polley (Canada, 2014), Fundão/Mariana (Brazil, 2015), and Brumadinho (2019) among several significant failures per decade—that no other civil structure would be allowed. Three geometric quantities are monitored. The **crest elevation**, surveyed by GNSS on monuments and by UAV/lidar surfaces, must stay above design and be re-surveyed after each raise. The **freeboard**—pond level to the *lowest* point of the crest—must exceed a design minimum (commonly 1–2 m plus wave run-up, site-specific) through the design storm, which requires pond level and minimum crest in the same datum. And **deformation** of embankment and foundation is monitored by piezometers, inclinometers, prisms, continuous GNSS, ground-based radar, and satellite InSAR; geometric surveys find settlement and bulging, InSAR finds slow movement over the whole face.

The **beach** (exposed tailings between embankment and pond) and the **pond** are neither land nor water in this book's senses: beaches are soft and saturated, their slope and the pond's extent change with deposition and decant operations, and a UAV DSM of a wet beach is a surface of specular water, drying crust, and slurry whose "elevation" has little geotechnical meaning. Stored tailings volumes are computed between the beach/pond surface and the pre-deposition ground or last survey, with the pond's volume from a separate bathymetric survey (a small USV or drone-dropped sounder).

The **Global Industry Standard on Tailings Management** (GISTM, August 2020; ICMM, UN Environment Programme, and the Principles for Responsible Investment) requires an engineer of record, a monitoring program with performance indicators and trigger levels, independent review, and public disclosure, and has driven a surge in InSAR screening, continuous GNSS, and routine UAV surveys of TSFs. Water-retaining dams follow the same geometry (crest, freeboard, deformation) under ICOLD guidance and national regulators, with a long tradition of precise levelling and geodetic networks that mining adopted late.

## 65.8 Reclamation and post-mining landscapes

Mine closure converts a pit, a dump, and a TSF into a landform that must be stable, drain without erosion, and support vegetation for centuries. The traditional **engineered landform**—terraced benches, uniform slopes, armored channels—is easy to survey against but concentrates runoff and gullies at bench edges. **Geomorphic reclamation** (the GeoFluv method, Bugosh; implemented in the Natural Regrade software) designs a drainage network and hillslopes with the geometry of stable natural landforms in the same climate, producing a complex curved surface that is harder to build and to check: tolerance is statistical (slope distributions, drainage density, sinuosity) rather than a vertical offset from a plane.

Post-closure **erosion monitoring** is a long-term DoD problem ([Chapter 40](ch40-erosion-and-geomorphic-change.md)): rills and gullies growing centimetres per year over hundreds of hectares, detectable by lidar or UAV at multi-year intervals if—and only if—the control network survives closure (monuments are routinely buried, graded over, or displaced by settlement). AOC compliance under SMCRA is assessed against the pre-mining topography, with the legacy-surface problems of [Section 65.3.5](#6535-reclamation-bonds). Subsidence over backfilled or abandoned workings continues for decades and is a known InSAR application.

## 65.9 Pitfalls particular to engineered surfaces

Engineered sites concentrate the surface-semantics problems that the rest of the book treats one at a time.

**Vertical walls and overhangs** (highwalls, quarry faces, bins, retaining walls, undercut faces at reclaimers) are not functions of $(x, y)$. A 2.5D DEM turns a vertical 20 m face into a one- or two-cell slope, mislocating crest and toe and understating face area, and a DoD across the face attributes horizontal retreat to vertical change of the cells it crosses. Use point clouds or meshes ([Chapter 35](ch35-voids-and-overhangs.md); [Chapter 46](ch46-data-models.md)) and compute retreat as cloud-to-cloud or cloud-to-mesh distance along the face normal.

**Vehicles and equipment on stockpiles** inflate volumes, as noted; the subtler problem is their *tracks*—compaction ruts and the pushed-up ridges beside them—which are real surface change of no inventory meaning.

**Wet versus dry material.** Fine-grained and hygroscopic materials (coal, fertilizer, some concentrates, fly ash) change height by settlement and swelling with moisture, and density more so; a coal yard surveyed after heavy rain and converted with a dry density can misstate inventory by several percent with no coal moved. State the moisture condition and, where tonnes matter, pair the survey with moisture sampling.

**Dust, steam, and smoke** from blasting, crushers, hot slag, autoclave vents, and landfill or stockpile fires scatter lidar (points in the air, voids beneath) and defeat image matching (holes or hallucinated surfaces in SfM). Fly in still, clear conditions, and treat voids over a pile as unknowns, not zero change ([Chapter 27](ch27-moving-and-transient-objects.md)).

**Dynamic water in pits.** The sump, the TSF pond, and a flooded quarry rise and fall by metres, and a DSM renders each as a flat surface at whatever level it happened to be; the rock below has not changed, and the volume between two pit surfaces at different water levels is not mined material. Mask water before computing volumes and sound the sump if its storage matters ([Chapter 34](ch34-water-in-dems.md)).

**Datum drift across a long record.** Mines survey the same pit for decades while control is re-adjusted, benchmarks are destroyed, geoid models are updated, and national datums modernized; a 1998 pit surface on a local datum and a 2024 GNSS-derived orthometric surface can differ by decimetres everywhere. Tie every survey to current control and, when control changes, publish the transformation and re-reduce the archive ([Chapter 9](ch09-vertical-datums.md); [Chapter 50](ch50-archiving-and-provenance.md)).

## Then & now

Earthwork measurement is older than most of geodesy. Nineteenth-century railway and canal engineers measured **cross-sections by chain and level** at fixed stations, computed areas with a **planimeter**, and applied the average end-area formula—a method so embedded in contract law that it survives in specifications today. Mine surveyors ran underground traverses with theodolite and steel tape; stockpile volumes were estimated by pacing the toe and taking a few staff readings. The **total station** (1970s) and **RTK GNSS** (1990s) made a few hundred points per hour on a pile routine, with TIN volumes computed in CAD. **Terrestrial laser scanning** and slope-stability radar arrived in mining in the early 2000s and gave millions of points per setup. The **UAV photogrammetry revolution** from about 2013—consumer multirotors, cheap cameras, commodity SfM—brought monthly, weekly, then daily site surfaces at centimetre GSD, and with them the doming problem and the licensure debate. The present phase is **continuous monitoring**: fixed scanners and radars every few minutes, machine-control as-builts streaming from every blade, InSAR time series over every tailings dam, autonomous docked drones on schedule. The surveyor's role has shifted from making the measurement to controlling, validating, and signing it.

## Mathematics

**Prism volume.** For two surfaces on a common grid of cell area $a$,

$$V = a \sum_{i \in \Omega} \left( z^{\text{top}}_i - z^{\text{base}}_i \right), \qquad \frac{\partial V}{\partial z^{\text{base}}_i} = -a, \qquad \frac{\partial V}{\partial \delta_b} = -A ,$$

where a uniform base-surface bias $\delta_b$ over footprint area $A$ maps one-to-one into volume. For a TIN, each triangle $t$ with vertex differences $d_1, d_2, d_3$ and plan area $A_t$ contributes $A_t (d_1 + d_2 + d_3)/3$ exactly when both surfaces are planar over $t$.

**End-area and prismoidal formulas.** For sections $A_1, A_2$ a distance $L$ apart, the average end-area volume is $V_{\text{EA}} = L(A_1 + A_2)/2$; with the mid-section area $A_m$, the prismoidal volume is $V_{\text{P}} = L(A_1 + 4A_m + A_2)/6$. For a frustum tapering linearly in both dimensions, $A_m \ne (A_1 + A_2)/2$ and the end-area method overestimates by the **prismoidal correction** $V_{\text{EA}} - V_{\text{P}} = L\,(w_1 - w_2)(d_1 - d_2)/6$ for sections of width $w$ and depth $d$.

**Volume uncertainty with spatially correlated error.** Let the per-cell difference error $\epsilon_i$ have variance $\sigma_d^2$ and correlation $\rho(\mathbf{x}_i - \mathbf{x}_j)$. Then

$$\sigma_V^2 = a^2 \sum_i \sum_j \sigma_d^2 \, \rho_{ij} = a^2 \sigma_d^2 \left[ n + \sum_{i \ne j} \rho_{ij} \right] .$$

For an isotropic exponential correlation with range $L$ on a footprint large compared with $L$, $\sum_{i \ne j}\rho_{ij} \approx n \cdot (2\pi L^2 / a)$ to leading order, giving $\sigma_V \approx \sigma_d \sqrt{A \cdot 2\pi L^2}$; the commonly quoted $n_{\text{eff}} = A/(\pi L^2)$ (Rolstad et al. 2009) differs by a factor near 2 in the definition of $L$ and is adequate for budgeting. A fully correlated (bias) component $\sigma_b$ adds $A^2\sigma_b^2$ directly. Because $\sigma_{V,\text{random}} \propto \sqrt{A}$ while the bias term $\propto A$, bias dominates for any footprint larger than a few correlation lengths—which is every real stockpile.

**Tonnage uncertainty.** With $M = \rho_b V$ and independent relative uncertainties,

$$\left(\frac{\sigma_M}{M}\right)^2 = \left(\frac{\sigma_V}{V}\right)^2 + \left(\frac{\sigma_{\rho_b}}{\rho_b}\right)^2 ,$$

and because $\sigma_{\rho_b}/\rho_b$ is typically 3–10 % while a good survey achieves $\sigma_V/V$ of 1–2 %, density controls the tonnage.

**SfM doming.** James and Robson (2014) model the dome as the surface deformation that compensates an error $\Delta k_1$ in the first radial distortion coefficient of a camera at height $H$: the vertical error grows approximately quadratically with distance $r$ from the block center, $\delta z(r) \approx c \, \Delta k_1 \, H \, r^2 / f^2$ ($f$ the focal length, $c$ a geometry-dependent constant), so the amplitude scales with block size squared and flying height, and is removed by convergent image geometry that decorrelates $k_1$ from the surface rather than by more GCPs alone. Fit a quadratic in $x, y$ to check-point residuals: a significant quadratic term is the dome.

## Validation & uncertainty

Validation of an engineered-surface survey has one purpose: to convert a number produced by software into a number a professional can sign. The procedure below is the minimum.

**1. Control, independently verified.** Establish site control (≥ 3 monuments, preferably 5+, around and *on* the feature) by static GNSS or levelling to a named datum and epoch; re-observe at least annually and after any earthwork near a monument; keep a *check* subset never used in processing. For a UAV block, place GCPs around the perimeter and at least one on the pile; with PPK/RTK direct georeferencing, still place 3–5 check points.

**2. Check-point statistics, with their spatial pattern.** Compute RMSE$_z$, mean error (bias), and the 95 % value ([Chapter 53](ch53-accuracy-assessment.md)) against the check points, *and plot residual versus distance from block center and versus x, y*. A bias above ~1 cm per 100 m of block, or a significant quadratic trend, indicates a datum shift, tilt, or dome to be corrected in the adjustment, not in the deliverable.

**3. Stable-area DoD.** Difference the new surface against the previous survey over unchanged areas—haul roads, pads, concrete, bedrock. The mean is the inter-survey bias (< 2–3 cm for UAV with GCPs, < 1 cm for TLS on control); the standard deviation and semivariogram give $\sigma_d$ and $L$ for the uncertainty formula; the spatial pattern reveals doming and tilts. This is the most informative check available and costs nothing.

**4. Repeat-survey consistency.** For high-value inventories, fly twice (different headings or altitudes) and compare volumes; a disagreement larger than the stated uncertainty means the uncertainty is wrong.

**5. Base-surface audit.** Document the base surface's source, date, and uncertainty; compute the volume on at least one alternative base to show sensitivity. When a pile is cleared, survey the pad and reconcile the floor material against the assumed value—this closes the loop most inventory programs leave open.

**6. Density and moisture.** Record the density source, the number of tests, their scatter, and the moisture condition at the survey time.

**7. Semantics.** Record what was removed from the surface (vehicles, water, dust artefacts) and how (manual, classification), and show the mask in the report.

**8. Report.** Volume (and tonnes) with a 95 % uncertainty interval and its components; datum, epoch, projection and scale factor; control report; method; surfaces; software and version; raw data archived with a hash.

> **Uncertainty budget.** Typical 1σ components for a monthly UAV stockpile inventory of a single 50,000 m³, 8,000 m² pile, well executed (GCPs, obliques, pre-placement base). Values are illustrative orders of magnitude from the literature and practice; measure your own.
>
> | Component | Typical magnitude | Volume effect | Detectable by |
> |---|---|---|---|
> | Short-wavelength surface noise (SfM texture, lidar range) | 2–5 cm, L ≈ 5–15 m | 50–150 m³ | Check points; stable-area DoD σ |
> | Residual dome / tilt after adjustment | 2–5 cm over pile | 160–400 m³ | Residual-vs-distance trend; stable-area DoD pattern |
> | Datum / control bias (base station height, geoid) | 1–3 cm (common to all surveys; cancels in DoD, not in absolute) | 80–240 m³ | Independent control re-observation |
> | Base surface (pad survey + floor material) | 3–10 cm | 240–800 m³ | Pad re-survey when cleared |
> | Toe delineation | 0.5–2 m in plan | 150–700 m³ | Two independent digitizations |
> | Transient objects, water, dust | 0–100 m³ | 0–100 m³ | Classification mask review |
> | Bulk density | 3–10 % | 1,500–5,000 m³-equivalent | Density tests; truck-scale reconciliation |
>
> Root-sum-square of the geometric components is roughly 400–1,200 m³ (0.8–2.4 %); including density, the tonnage uncertainty is 3–10 %. The two largest terms are the two the software does not see.

A DoD-based *change* volume (airspace consumed, cut moved) is easier to defend than an absolute inventory: the base is the previous survey on the same control, the common datum bias cancels, and the dominant remaining term—the inter-survey bias over stable areas—is directly observable.

## Software

**Open source:** **CloudCompare** (volume between a cloud and a reference plane or between two clouds via the 2.5D Volume tool; M3C2 distances for walls) — caveat: the grid and base are user choices, so document both. **QGIS** ("Raster surface volume" processing tool; profiles) and **GRASS GIS** (`r.volume`, `r.mapcalc` for DoD) — caveat: `r.volume` needs the base subtracted first. **WhiteboxTools** (DoD, gully metrics for reclamation monitoring). **OpenDroneMap / WebODM** (SfM with GCP support and web volume measurement) — caveat: self-calibration defaults can dome on nadir-only blocks; add obliques. **MicMac** (rigorous photogrammetric SfM with explicit camera-calibration control). **PDAL** and **GDAL** (classification, gridding, differencing, common grids), **xdem** (co-registration and spatially correlated DoD uncertainty), **R `gstat`/`lidR`** (semivariograms, ground classification). **SNAP / MintPy / ISCE2** (InSAR time series for subsidence and dam monitoring).

**Free but closed:** vendor viewers and free tiers (Trimble Connect, Propeller and Pix4D web viewers, Leica TruView) for measuring on deliverables — caveat: they do not expose the grid, base, and toe behind a displayed volume, so they are review tools, not audit tools.

**Commercial:** **Propeller** (UAV site surveys with AeroPoints GCPs and web volume tools), **Pix4Dmapper/Pix4Dmatic** and **Agisoft Metashape** (SfM with GCP/PPK and volume tools), **DJI Terra**, **Trimble Business Center** and **SiteVision/WorksManager** (survey office and machine-control integration; grid/ground handling), **Carlson Civil/Mining and Natural Regrade** (TIN volumes, end-area reports, GeoFluv design), **Maptek PointStudio and Vulcan** (pit and stockpile scanning, mine design), **Leica Cyclone/Cyclone 3DR** (TLS registration and volumes), **Bentley OpenRoads/MicroStation** (design surfaces, quantities), **GroundProbe SSR / IDS GeoRadar IBIS** (slope stability radar). Common caveat: default "lowest-point" or "triangulated-toe" base surfaces are conveniences, not surveys, and volume reports rarely state uncertainty unless configured to.

## Standards & guides

- **JORC Code (2012 edition)** — Joint Ore Reserves Committee (Australasia): public reporting of exploration results, resources, and reserves; Table 1 requires discussion of survey and topographic control quality.
- **NI 43-101 (2011) with CIM Definition Standards (2014)** — Canadian Securities Administrators / CIM: technical reports for mineral projects, Qualified Person responsibility.
- **US EPA, 40 CFR Part 258** — Criteria for municipal solid waste landfills (RCRA Subtitle D); state programs built on it require annual topographic surveys and capacity certification.
- **SMCRA (1977) and 30 CFR Chapter VII** — US Office of Surface Mining: approximate original contour, reclamation bonding and release.
- **GISTM (2020)** — ICMM/UNEP/PRI Global Industry Standard on Tailings Management: monitoring, trigger levels, engineer of record, disclosure.
- **ICOLD Bulletin 158, *Dam Surveillance Guide* (2018)** — monitoring of embankment dams.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023)** — accuracy classes and reporting (NVA/VVA) for the DEMs and orthos UAV surveys produce.
- **USACE EM 1110-1-1000, Photogrammetric and LiDAR Mapping (2015)** — mapping standards for Corps projects, including earthwork quantities.
- **USACE EM 1110-2-1003, Hydrographic Surveying (2013)** — dredging payment surveys, the aquatic analogue of this chapter ([Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).
- **ISO 17123 series** — field procedures for testing geodetic and surveying instruments (levels, total stations, GNSS RTK, terrestrial laser scanners (Part 9).
- **ASTM D1556 / D6938** — in-place density by sand-cone and nuclear methods; **ASTM E57** standards for 3D imaging systems.
- **State surveyor licensing statutes and board rulings** — define when volumetric work is the practice of surveying; consult the state board before offering UAV volume services.
- **LandXML 1.2 / IFC4 and IFC 4.3 (ISO 16739-1:2018, revised 2024)** — exchange of design TINs and georeferenced BIM.

## Pitfalls

- **Reporting a volume without base-surface uncertainty** → the software reports top-surface precision and the base is taken as given → always compute the volume on at least two bases and state the pre-placement survey date, or declare the base an assumption.
- **Grid-versus-ground confusion** → design in ground coordinates, survey in grid (or vice versa), changing quantities by 0.01–0.1 % and positions by metres → name the coordinate system and combined scale factor in the method statement; check a known ground distance against the file.
- **Counting a loader, truck, or conveyor as stockpile** → unclassified DSM used directly → review the classification mask over every pile; a 40 t truck is 60–80 m³.
- **SfM dome inflating a pile by several percent** → nadir-only, parallel-strip block, self-calibrated, few or perimeter-only GCPs → add obliques and a GCP on the pile; plot check residuals against distance from block center; difference against a stable-area surface.
- **Comparing surfaces in different vertical datums** → legacy permit surface on NGVD 29 or a local datum, new survey on NAVD 88/GNSS geoid → convert explicitly ([Chapter 9](ch09-vertical-datums.md)) and verify on a monument common to both epochs.
- **Wet-day survey of hygroscopic material** → height and density both change with moisture → record moisture state; pair tonnage surveys with density/moisture sampling.
- **Trusting machine-control as-builts as independent** → they share the site calibration with the design → check with an independent survey on independent control at least at project start and end.
- **Toe digitized from the orthomosaic without site inspection** → spillage and fines extend the apparent toe outward → walk or scan the toe; compare two digitizations; state the method.
- **Pit sump or TSF pond at different levels between surveys** → water surface counted as rock or tailings → mask water bodies; sound the sump if its volume matters.
- **Highwall change computed on a 2.5D DoD** → vertical faces collapse to one or two cells → use cloud-to-cloud (M3C2) distances along the face normal, or a wall-parallel projection.
- **Settlement credited as capacity** → DoD of a landfill cell mixes new waste with settlement of old → separate with settlement monuments or a settlement model before computing AUF.
- **Inactive tailings dam assumed static** → no routine deformation monitoring → InSAR screening and GNSS on every dam, with written trigger levels (GISTM).
- **End-area quantities reproduced from a DEM at the wrong stations** → sections cut at the contractor's stations differ from the engineer's → agree station list and section orientation before computing; archive the cross-sections.
- **Losing control monuments at closure** → regraded, buried, or settled → set deep monuments outside the disturbed area before reclamation; re-observe every campaign.

## Key takeaways

- An engineered volume is a legal and financial number: document datum, epoch, projection and scale factor, control, method, top and base surface definitions, toe, density source, and a 95 % uncertainty.
- The base surface and the bulk density dominate volumetric and tonnage uncertainty; the top-surface precision quoted by software is usually the smallest term.
- Spatially correlated error, not per-cell noise, controls volume uncertainty; estimate it from check-point trends and stable-area DoDs, and propagate it as a bias over the footprint area.
- UAV SfM is the workhorse; defeat doming with convergent imagery and on-pile control, and prove the result with independent check points and a stable-area comparison.
- Machine-control, scanner, and UAV surfaces that share a site calibration are not independent; keep an independent control check in the program.
- Change volumes (DoD) are easier to defend than absolute inventories because the base is itself a survey and datum bias cancels; close the loop by surveying the pad when a pile is cleared.
- Vertical walls, vehicles, water, dust, steam, and moisture are the characteristic semantic failures of engineered surfaces; classify, mask, and record.
- Where failure is catastrophic—tailings dams, pit walls—periodic survey is insufficient; monitor displacement continuously (radar, GNSS, InSAR) with written trigger levels.

## References

- Anderson, S. W. 2019. Uncertainty in quantitative analyses of topographic change: error propagation and the role of thresholding. *Earth Surface Processes and Landforms* 44(5):1015–1033. doi:10.1002/esp.4551
- Bemis, S. P., S. Micklethwaite, D. Turner, M. R. James, S. Akciz, S. T. Thiele, and H. A. Bangash. 2014. Ground-based and UAV-based photogrammetry: a multi-scale, high-resolution mapping tool for structural geology and paleoseismology. *Journal of Structural Geology* 69:163–178. doi:10.1016/j.jsg.2014.10.007
- Bugosh, N., and E. Epp. 2019. Evaluating sediment production from native and fluvial geomorphic-reclamation watersheds at La Plata Mine. *Catena* 174:383–398.
- Carrivick, J. L., M. W. Smith, and D. J. Quincey. 2016. *Structure from Motion in the Geosciences*. Wiley-Blackwell, Chichester.
- CIM. 2014. *CIM Definition Standards for Mineral Resources and Mineral Reserves*. Canadian Institute of Mining, Metallurgy and Petroleum.
- Esposito, G., R. Salvini, F. Matano, M. Sacchi, M. Danzi, R. Somma, and C. Troise. 2017. Multitemporal monitoring of a coastal landslide through SfM-derived point cloud comparison. *The Photogrammetric Record* 32(160):459–479.
- Esposito, G., G. Mastrorocco, R. Salvini, M. Oliveti, and P. Starita. 2017. Application of UAV photogrammetry for the multi-temporal estimation of surface extent and volumetric excavation in the Sa Pigada Bianca open-pit mine, Sardinia, Italy. *Environmental Earth Sciences* 76:103. doi:10.1007/s12665-017-6409-z
- Gama, F. F., J. C. Mura, W. R. Paradella, and C. G. de Oliveira. 2020. Deformations prior to the Brumadinho dam collapse revealed by Sentinel-1 InSAR data using SBAS and PSI techniques. *Remote Sensing of Environment* 246:111859. doi:10.1016/j.rse.2020.111859
- Grebby, S., A. Sowter, J. Gluyas, D. Toll, D. Gee, A. Athab, and R. Girindran. 2021. Advanced analysis of satellite data reveals ground deformation precursors to the Brumadinho Tailings Dam collapse. *Communications Earth & Environment* 2:2. doi:10.1038/s43247-020-00079-2
- Hugenholtz, C. H., J. Walker, O. Brown, and S. Myshak. 2015. Earthwork volumetrics with an unmanned aerial vehicle and softcopy photogrammetry. *Journal of Surveying Engineering* 141(1):06014003. doi:10.1061/(ASCE)SU.1943-5428.0000138
- ICMM, UNEP, and PRI. 2020. *Global Industry Standard on Tailings Management*. August 2020.
- James, M. R., and S. Robson. 2014. Mitigating systematic error in topographic models derived from UAV and ground-based image networks. *Earth Surface Processes and Landforms* 39(10):1413–1420. doi:10.1002/esp.3609
- James, M. R., S. Robson, and M. W. Smith. 2017. 3-D uncertainty-based topographic change detection with structure-from-motion photogrammetry: precision maps for ground control and directly georeferenced surveys. *Earth Surface Processes and Landforms* 42(12):1769–1788. doi:10.1002/esp.4125
- JORC. 2012. *Australasian Code for Reporting of Exploration Results, Mineral Resources and Ore Reserves (The JORC Code)*, 2012 edition. Joint Ore Reserves Committee of the AusIMM, AIG and MCA.
- Rolstad, C., T. Haug, and B. Denby. 2009. Spatially integrated geodetic glacier mass balance and its uncertainty based on geostatistical analysis: application to the western Svartisen ice cap, Norway. *Journal of Glaciology* 55(192):666–680. doi:10.3189/002214309789470950
- Sowers, G. F. 1973. Settlement of waste disposal fills. *Proceedings of the 8th International Conference on Soil Mechanics and Foundation Engineering*, Moscow, 2:207–210.
- Tucci, G., A. Gebbia, A. Conti, L. Fiorini, and C. Lubello. 2019. Monitoring and computation of the volumes of stockpiles of bulk material by means of UAV photogrammetric surveying. *Remote Sensing* 11(12):1471. doi:10.3390/rs11121471
- US Army Corps of Engineers. 2015. *Photogrammetric and LiDAR Mapping*, EM 1110-1-1000. Washington, DC.
- US Army Corps of Engineers. 2013. *Hydrographic Surveying*, EM 1110-2-1003. Washington, DC.
- US Environmental Protection Agency. 40 CFR Part 258 — Criteria for Municipal Solid Waste Landfills. *Code of Federal Regulations*.
- Wheaton, J. M., J. Brasington, S. E. Darby, and D. A. Sear. 2010. Accounting for uncertainty in DEMs from repeat topographic surveys: improved sediment budgets. *Earth Surface Processes and Landforms* 35(2):136–156. doi:10.1002/esp.1886
- Robertson, P. K., L. de Melo, D. J. Williams, and G. W. Wilson. 2019. *Report of the Expert Panel on the Technical Causes of the Failure of Feijão Dam I*. Prepared for Vale S.A.
- Morgenstern, N. R., S. G. Vick, C. B. Viotti, and B. D. Watts. 2016. *Fundão Tailings Dam Review Panel: Report on the Immediate Causes of the Failure of the Fundão Dam*. Cleary Gottlieb Steen & Hamilton LLP.

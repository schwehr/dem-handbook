# Chapter 61 — Hydrologic and hydraulic modeling constraints

> **Part XIV — Domain deep dives.** The first of the domain chapters: what flood, drainage, and watershed models demand from an elevation model, and the small artefacts that produce large wrong answers.

**In this chapter.** Water finds the lowest path, so a water model inherits every error in its elevation model and amplifies the ones on that path. You will be able to match model families (1D and 2D hydraulics, lumped and distributed hydrology, terrain proxies such as HAND) to the DEM resolution and accuracy they can exploit; explain why a DSM, a hydro-flattened DTM, and a hydro-enforced DTM give three different floods from the same rain; choose between filling, breaching, and burning, and predict how D8, D∞, and multiple-flow-direction routing respond to grid spacing; recognize that lidar stops at the water surface and the channel beneath must come from elsewhere; propagate vertical uncertainty into inundation extent with a correlated Monte Carlo experiment rather than a single deterministic edge; read FEMA's Guidelines and Standards and the EU Floods Directive as testable specifications; and list the data gaps—culverts, levee crests, channel bathymetry, tidal boundary datums—that matter more than any pixel statistic.

## 61.1 Model families and their DEM sweet spots

Every water model carries a terrain model inside it, but what "terrain" means differs by model type, and so does the accuracy that pays off. Three families are worth separating.

**Hydraulic models** solve for water depth and velocity on a domain whose lower boundary is the bed or ground. **One-dimensional (1D)** models (HEC-RAS 1D, MIKE 11, Flood Modeller) represent a river as a sequence of **cross-sections**—station–elevation profiles cut perpendicular to flow—and interpolate conveyance between them; the DEM supplies the overbank portions and, if nothing better exists, the channel too. **Two-dimensional (2D)** models (HEC-RAS 2D, LISFLOOD-FP, TUFLOW, MIKE 21/MIKE+, Delft3D FM, SFINCS, ANUGA) solve the depth-averaged **shallow-water equations** (SWE) or a simplification (diffusive-wave, local-inertial) on a grid or mesh whose cell elevations *are* the DEM, sometimes with **sub-grid** treatment that keeps finer bed detail inside coarser computational cells. **Coupled 1D–2D** models route the channel in 1D and the floodplain in 2D; urban models add a 1D pipe network beneath the 2D surface.

For these models the DEM is not a parameter; it is the geometry of the problem, and errors in it are structural. Horritt and Bates (2001, 2002) established the central empirical result: beyond a modest resolution, finer grids do not improve predicted inundation unless they bring in features that control flow—a bank, an embankment, a road—whereas small *vertical* errors at those controls change extents substantially. 2D flood models therefore reward a DTM that is topologically faithful (barriers continuous, openings open) with decimeter vertical accuracy, and punish a smoother, finer-looking DTM that has quietly bridged a culvert. The sweet spot for a lowland 2D model is a 1–5 m DTM from QL2-or-better lidar (RMSE$_z$ ≤ 10 cm in open terrain; [Chapter 53](ch53-accuracy-assessment.md)), hydro-enforced at structures, run at 5–30 m with sub-grid bathymetry where the code supports it.

**Hydrologic models** ask how much water arrives and when, and use the DEM for watershed delineation, slope, and flow length. Lumped and semi-distributed models (HEC-HMS, SWAT) need a DEM only to define subbasins and a few indices; 30 m data are often adequate. Distributed models (WRF-Hydro, MIKE SHE, GSSHA) route flow on a 30–250 m grid and are more sensitive to grid artefacts. Here absolute vertical accuracy barely matters; *drainage topology* matters enormously—a basin that leaks into its neighbor through a spurious saddle has the wrong area and the wrong peak flow however precise its elevations.

**Terrain-only proxies** use the DEM without a solver. **HAND** (Height Above Nearest Drainage; Nobre et al. 2011) assigns each cell its vertical distance above the channel cell it drains to; thresholding HAND at a stage gives an inundation map in seconds, and the US National Water Model's flood-inundation mapping used HAND with synthetic rating curves at reach scale. Proxies are only as good as the DEM's drainage network and are blind to hydraulic controls (backwater, levees, bridges): they overpredict in confined reaches and underpredict behind embankments.

| Family | Representative codes | DEM role | Resolution that pays | Accuracy that pays | Fatal artefact |
|---|---|---|---|---|---|
| 1D hydraulics | HEC-RAS 1D, MIKE 11, Flood Modeller | Cross-section overbanks | 1–5 m for sections | Decimeter at banks | Section cut through a bridge deck |
| 2D hydraulics | HEC-RAS 2D, LISFLOOD-FP, TUFLOW, SFINCS, Delft3D FM | Cell/mesh elevations | 1–10 m source; 5–30 m compute | ≤ 10–15 cm RMSE$_z$ | Missing culvert; levee gap |
| Coupled 1D–2D / urban | InfoWorks ICM, MIKE+, TUFLOW, HEC-RAS | Surface + network inverts | 0.5–2 m | Centimeter at curbs | Inlet–surface mismatch |
| Lumped/semi-distributed hydrology | HEC-HMS, SWAT | Delineation, indices | 10–30 m | Topology, not σ$_z$ | Basin leak across false saddle |
| Distributed hydrology | WRF-Hydro, MIKE SHE | Routing grid | 30–250 m | Topology | Flat-area routing noise |
| Terrain proxies | HAND, GeoFlood | Drainage distance | 1–30 m | Relative to channel | Hydro-flattened channel at bank height |

The "fatal artefact" column is the point of this chapter: a model's sensitivity to the DEM is concentrated along the lines that control where water can and cannot go.

<!-- figure: Figure 61.1 — Schematic of the three model families (1D cross-sections, 2D grid/mesh with sub-grid bathymetry, HAND terrain proxy) applied to the same floodplain, annotated with where the DEM enters each. -->

## 61.2 DTM, not DSM — and the thin features that must survive

The first and most expensive mistake in flood modeling is to run on a surface that contains vegetation and buildings. A DSM ([Chapter 4](ch04-names-and-definitions.md)) presents a riparian forest as a 20 m wall and a row of houses as a dam; the modelled flood piles up behind them, deeper and narrower than reality. Global products made the mistake easy: SRTM and the Copernicus DEM are surface models in which forests and cities stand several meters proud of the ground, and a decade of global flood models inherited those biases until bare-earth corrections appeared (MERIT DEM statistically; FABDEM, Hawker et al. 2022, by machine-learned forest and building removal from the Copernicus 30 m DEM). Even corrected, residual errors are meters in dense forest and cities, which is why §61.5 insists on propagating them.

A lidar DTM solves the vegetation problem but forces the modeler to decide how to put buildings back in. **Block-out** removes building cells from the domain (or raises them to roof height) so water flows around them—right for solid masonry, wrong for buildings with open ground floors. **Porosity** methods reduce a coarser cell's storage and conveyance by its building fraction, which is better behaved at 10–30 m. **Roughness** methods leave the ground alone and assign a very high Manning's $n$ (0.1–1.0 or more) to footprints, slowing water rather than blocking it. Whatever the choice, the DTM must be *consistently* bare earth under buildings ([Chapter 32](ch32-dsm-to-dtm.md) discusses what "ground under a building" means) and the footprints must be from the same epoch.

The thin features are harder. A **levee** 3 m high and 4 m wide at the crest is well resolved in a 1 m DTM, a one-cell ridge in a 5 m DTM, and gone in a 10 m DTM—its crest averaged with the floodplain into a 1 m bump that water crosses at the first opportunity. **Floodwalls** (0.3 m wide, 2 m high) vanish at any spacing above about 0.5 m, and **road and railway embankments** behave as unintended levees with the same sensitivity. The remedy is not finer grids everywhere but **breaklines** ([Chapter 59](ch59-vector-data.md)): 3D polylines along crests and wall tops enforced in the mesh so that cell elevations take the crest height rather than the cell mean. The USGS Lidar Base Specification requires breaklines for hydro-flattening but not for levee crests; FEMA studies typically require surveyed crest profiles, and the US National Levee Database holds profiles for federally managed levees that can be checked against the DTM.

The complementary error is the feature that should *not* be a barrier. A **bridge deck** kept as ground closes the river beneath it; a **culvert** under a road embankment is never seen from above, so the embankment is continuous in every DTM and the ditch behind it ponds. Roads become dams. **Hydro-enforcement**—cutting the DTM at known culverts and bridge openings—corrects this and depends on a structure inventory that no DEM contains. Poppenga and Worstell (2016) showed for a lidar DTM in the US Midwest that without enforcing drainage structures the delineated network and flow paths were wrong across large areas of an embankment-dominated landscape. Inventories come from transportation agencies, field surveys, and increasingly from automated detection of embankment–channel intersections followed by field confirmation.

> **Definitions that bite.** *Hydro-flattening*, *hydro-enforcement*, and *hydro-conditioning* are three operations with three purposes, routinely conflated. Flattening makes water bodies flat and monotonic for product reasons and *does not* make the surface drain; enforcement cuts the DTM at real structures so flow passes where it does in reality; conditioning alters the surface (fill, breach, burn) so that a routing algorithm runs to completion, whether or not the result corresponds to reality ([Chapter 34](ch34-water-in-dems.md)). A deliverable called "hydro-enforced" should come with the list of structures enforced; one called "hydro-conditioned" has been altered in ways you must ask about before using its elevations for anything but routing.

## 61.3 Conditioning the surface: filling, breaching, burning, routing

A flow-direction algorithm needs every cell to have a downslope neighbor or be an outlet; real DTMs do not comply. **Depressions** arise from real closed basins (karst, prairie potholes, detention ponds, quarries), from noise, from interpolation across bridges and culverts, and from narrow channels straddled by grid cells. **Flats** arise from hydro-flattening, vertical quantization, and genuinely flat terrain. Conditioning removes them; the algorithms differ in what else they damage.

**Filling** raises each depression cell to its spill elevation. The **priority-flood** algorithm (Barnes, Lehman, and Mulla 2014) processes cells from the edges inward with a priority queue keyed on elevation, fills every depression in one pass in $O(n \log n)$ time, and is what WhiteboxTools, RichDEM, and TauDEM use. Filling is robust but destroys information: a prairie pothole becomes a flat surface at spill height; a detention basin disappears; a channel under a road embankment is not opened—the whole upstream reach is raised to the crest and the resulting flat needs a tie-breaking rule to route across.

**Breaching** carves a path from the depression bottom to the nearest cell below spill height. Lindsay (2016) showed that on lidar DTMs, where most artificial depressions come from embankments over culverts and bridges, breaching modifies far fewer cells than filling, and that a hybrid—breach short, shallow obstructions, fill the rest—balances best. Breaching is right at culverts and wrong at real closed basins; the length and depth thresholds that separate them must be set and reported.

**Stream burning** lowers the DTM along a mapped stream network (by 5–20 m, say) so that routing follows the vector hydrography. It guarantees agreement with the map and imports every error in the map (misregistered or outdated streams; 1:24,000 positional accuracy of ± 12 m applied to a 1 m DTM). Burning suits coarse DEMs whose hydrography is more accurate than the terrain; on a lidar DTM it usually degrades the result, and enforcement at structures only is preferable.

Once conditioned, the surface is routed. **D8** (O'Callaghan and Mark 1984) sends all of a cell's flow to the steepest of its eight neighbors; it produces parallel flow-line artefacts on planar slopes and cannot represent divergence, but yields clean channel networks and is what most hydrologic models expect. **D∞** (Tarboton 1997) computes the steepest descent on triangular facets and splits flow between the two bracketing neighbors, removing the eight-direction quantization. **Multiple flow direction (MFD)** methods distribute flow to all downslope neighbors weighted by slope—best for specific catchment area on hillslopes, worst for channel delineation. The usual compromise is D∞ or MFD for terrain indices (§61.7) and D8 for networks and basins.

All of these are **resolution-sensitive**. On a coarse grid the steepest-descent direction is averaged over a long baseline and follows the valley; on a 1 m lidar grid it follows wheel ruts, furrows, and the camber of every road unless the DTM is smoothed or the accumulation threshold raised. **Channel initiation** is set by a **flow accumulation threshold** $A_c$; a 1 km² threshold on a 30 m DEM and on a 1 m DEM do not produce the same network, because the fine DEM contains thousands of divides the coarse one averaged away. Calibrate the threshold against mapped channel heads or a slope–area relationship and report it with the network.

> **Try it.** Condition and route a lidar DTM with WhiteboxTools from Python, comparing filling and breaching.
>
> ```python
> import whitebox
> wbt = whitebox.WhiteboxTools()
> wbt.set_working_dir("/data/floodplain")
>
> # Hybrid breach-then-fill (Lindsay 2016); thresholds are a modelling decision.
> wbt.breach_depressions_least_cost("dtm_1m.tif", "dtm_breached.tif",
>                                   dist=50, max_cost=2.0, fill=True)
> wbt.fill_depressions("dtm_1m.tif", "dtm_filled.tif")  # for comparison
>
> # Change rasters
> wbt.subtract("dtm_breached.tif", "dtm_1m.tif", "delta_breach.tif")
> wbt.subtract("dtm_filled.tif",   "dtm_1m.tif", "delta_fill.tif")
>
> # D8 network at a 0.5 km² threshold
> wbt.d8_pointer("dtm_breached.tif", "d8.tif")
> wbt.d8_flow_accumulation("dtm_breached.tif", "facc.tif", out_type="catchment area")
> wbt.extract_streams("facc.tif", "streams.tif", threshold=500000)
>
> # D-infinity specific catchment area for TWI
> wbt.d_inf_flow_accumulation("dtm_breached.tif", "sca_dinf.tif",
>                             out_type="specific contributing area")
> ```
>
> Expected outcome: `delta_fill.tif` shows large positive patches upstream of every road crossing (fields raised to embankment height); `delta_breach.tif` shows narrow cuts through the embankments and little else. The networks agree in the main valleys and disagree behind embankments; overlay them on the hillshade and the culvert inventory to decide which is right where.

pysheds offers a lighter pure-Python path (`fill_depressions`, `resolve_flats`, `flowdir`, `accumulation`) for notebooks; TauDEM scales to continental extents with MPI; GRASS `r.watershed` routes by least cost without explicit filling.

## 61.4 The bathymetry under the water

Topographic lidar stops at the water surface ([Chapter 34](ch34-water-in-dems.md)), so the delivered DTM shows every river as a flat ribbon at the water level on the day of flight, with the channel's cross-section—the part that carries low and moderate flows—absent. A 2D model on such a surface has no channel conveyance: the first increment of discharge spills over the banks because the "channel" is already full of virtual terrain, and the model overpredicts inundation for all but the largest events. The error is not subtle: a 40 m wide, 3 m deep channel is roughly 120 m² of section, about 180 m³/s of conveyance at 1.5 m/s that the hydro-flattened DTM does not have.

Four remedies exist. **Measured bathymetry** is best: single- or multibeam sonar from a small boat ([Chapter 20](ch20-sonar.md)), ADCP transects (depth as a by-product of velocity profiling), RTK-GNSS wading surveys in small streams, and topobathymetric green lidar in clear water ([Chapter 19](ch19-bathymetric-lidar.md)); the surveyed channel is merged below the water-surface breakline into a **topobathymetric DEM** whose bathymetric part carries its own, usually larger, uncertainty. **Synthetic channels** are the usual fallback: a trapezoidal or parabolic geometry generated from hydraulic-geometry relations ($w \propto Q^{b}$, $d \propto Q^{f}$), from a conveyance requirement (carry bankfull discharge at the DTM's bank elevations), or from interpolated surveyed sections, burned in below the water surface. They are honest when labelled and dangerous when distributed as measured topobathy. **1D channels** with surveyed cross-sections coupled to a 2D floodplain sidestep the issue, and **sub-grid channel** schemes (LISFLOOD-FP, SFINCS) carry width and depth as cell attributes without resolving the channel on the grid.

Reservoirs raise a distinct need. A **storage curve** (elevation–area–capacity) is the heart of reservoir routing and dam-safety analysis and requires the bathymetry below the current pool, which sedimentation has changed since construction (globally on the order of 0.5–1 % of capacity per year, approximately; regional estimates vary). Repeat bathymetric surveys differenced against pre-impoundment topography give the current curve and the sedimentation rate; volume uncertainty follows [Chapter 65](ch65-mining-landfills-earthworks.md).

## 61.5 Vertical accuracy becomes horizontal inundation error

Flood extent is where a water surface intersects the ground; where the ground is flat, a small vertical error moves that intersection a long way. For a planar floodplain of slope $\tan\beta$, a vertical error $\delta z$ shifts the flood edge by

$$\delta x = \frac{\delta z}{\tan \beta}.$$

At a slope of 1:1000, typical of deltaic and coastal plains, $\delta z = 0.5$ m moves the edge 500 m; at 1:100, 50 m; at 1:10, 5 m. This is the shoreline slope amplification of [Chapter 34](ch34-water-in-dems.md), and it is why a 1 m RMSE$_z$ DEM is not "a bit worse" than a 10 cm DEM on flat terrain but categorically unfit for parcel-level results.

The DEM is only one term: water-surface uncertainty from discharge, roughness, and boundary conditions adds its own $\delta z$, perhaps 0.2–0.5 m for a design event on a well-calibrated gauged river, and the DEM should be at least as good—the implicit logic behind decimeter-class lidar requirements in regulatory programs.

A single flood edge from a DEM with non-negligible σ$_z$ is a point estimate without a confidence statement. The honest product is a **probability of inundation** map, obtained by **Monte Carlo propagation**: generate many DEM realizations consistent with the error model, run the model (or a fast proxy) on each, and tally the fraction of realizations in which each cell is wet. The subtlety is **spatial correlation**. DEM errors are correlated over tens to hundreds of meters by strip geometry, vegetation, and interpolation ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 53](ch53-accuracy-assessment.md)). Independent white noise per cell creates a spuriously rough surface that blocks flow with false ridges and *under*-estimates extent uncertainty, because independent errors average out over any area larger than a cell. Correlated error fields—white noise filtered with a kernel matched to the error semivariogram, or sequential Gaussian simulation conditioned on check points—move whole areas of floodplain together, as real errors do (Wechsler 2007).

> **Worked example.** *Probabilistic flood extent from a DEM with correlated error.* A 2D model of a 12 km lowland reach uses a 2 m lidar DTM with NVA RMSE$_z$ = 0.08 m and VVA 95th percentile 0.25 m; the floodplain is 60 % pasture, 40 % riparian woodland. Check-point residuals give an error semivariogram with range ≈ 150 m and nugget 0.03 m². The design event's modelled water surface has σ ≈ 0.20 m from discharge and roughness uncertainty.
>
> 1. Error model: σ$_z$ = 0.08 m on open ground, 0.13 m (≈ 0.25/1.96) under woodland; exponential correlation, range 150 m; nugget 0.17 m as independent noise.
> 2. Generate $N$ = 200 correlated error fields $\epsilon_i(x,y)$ by convolving Gaussian white noise with a kernel matched to the semivariogram, scaling by the land-cover σ map, and adding the nugget; DEM$_i$ = DTM + $\epsilon_i$.
> 3. Draw a water-surface perturbation $\eta_i \sim \mathcal{N}(0, 0.20^2)$ per realization (perfectly correlated along the reach—conservative).
> 4. Run the model on each DEM$_i$ with boundary stage + $\eta_i$; record the wet mask $W_i$.
> 5. Inundation probability $P(x,y) = \frac{1}{N}\sum_i W_i(x,y)$.
>
> Result (illustrative numbers): deterministic extent 9.4 km²; area with $P \ge 0.5$, 9.6 km²; area with $0.05 < P < 0.95$—where the outcome is genuinely undecided—2.1 km², about 22 % of the deterministic extent, concentrated on the floodplain back-slope at 1:800. There the combined σ$_z$ of $\sqrt{0.08^2 + 0.20^2} = 0.215$ m predicts an edge σ of $0.215 \times 800 \approx 170$ m, consistent with the band's width. With independent per-cell noise instead, the same 200 realizations give an uncertain band of only 0.6 km² and spurious ponding in 3 % of cells—both artefacts of the wrong error model.

The global picture follows the same arithmetic. Sampson et al. (2015) built the first ~90 m global flood hazard model on SRTM-derived terrain and found the DEM to be the dominant error source in flat, vegetated, and urban regions; Hawker et al. (2018) and Schumann and Bates (2018) argued that a high-accuracy open global DEM would be the community's most valuable investment; FABDEM (Hawker et al. 2022) reduced modelled extent error substantially relative to the uncorrected Copernicus DEM in forested and built-up floodplains while remaining far from lidar quality. For **coastal sea-level-rise exposure**, Kulp and Strauss (2019) replaced SRTM with the neural-network-corrected CoastalDEM and roughly tripled the global population estimated below projected high-tide lines—a change driven entirely by DEM bias. Gesch (2018) formalized a **minimum increment** rule: the smallest sea-level increment that can be mapped with 95 % confidence is about twice the DEM's LE95, so a DEM with LE95 of 0.3 m cannot responsibly separate a 0.5 m from a 0.7 m scenario, and the DEM's accuracy should be stated with every exposure number.

<!-- figure: Figure 61.2 — Deterministic flood edge versus probability-of-inundation map from 200 correlated DEM realizations; inset shows the same experiment with independent per-cell noise to illustrate the underestimated uncertainty band and spurious ponding. -->

## 61.6 Regulatory uses: what the rules require and how they are tested

Flood maps carry legal weight—insurance premiums, building permits, levee accreditation, dam-safety classifications—so the elevation data behind them are specified, and the specifications are testable.

In the United States, the **National Flood Insurance Program (NFIP)** produces **Flood Insurance Rate Maps (FIRMs)** showing the Special Flood Hazard Area (the 1 %-annual-chance floodplain) and, where studied in detail, the **Base Flood Elevation (BFE)**, that flood's water-surface elevation. FEMA's **Guidelines and Standards for Flood Risk Analysis and Mapping** (a living set of standards and guidance; the *Elevation Guidance* document is the relevant one) require that new elevation data acquired for Flood Risk Projects meet the USGS Lidar Base Specification at Quality Level 2 or better—RMSE$_z$ ≤ 10 cm in non-vegetated terrain, equivalently NVA ≤ 19.6 cm at 95 %, with VVA reported—in NAVD 88 with the geoid model documented, and that existing data be evaluated for currency and accuracy before reuse. Testing follows ASPRS practice ([Chapter 53](ch53-accuracy-assessment.md)): independent check points by land-cover class, RMSE and 95th-percentile statistics, and a report that enters the study's Technical Support Data Notebook. The BFE is printed to 0.1 ft (≈ 3 cm), a regulatory convention rather than a measurement claim; structure-specific Elevation Certificates are field-surveyed, and a DEM is not accepted for that purpose.

**Levee accreditation** under 44 CFR 65.10 requires demonstrated freeboard (typically 3 ft, ≈ 0.9 m, above the BFE) from a surveyed crest profile; a crest read from a lidar DTM without ground survey is generally not accepted. USACE's **EM 1110-2-1619** (*Risk-Based Analysis for Flood Damage Reduction Studies*, 1996) replaced fixed freeboard in federal project evaluation with distributions on discharge, stage, and geotechnical performance, into which crest survey uncertainty enters explicitly. **Dam safety** programs require breach-inundation maps whose downstream extents are DEM-limited and whose storage curves depend on reservoir bathymetry (§61.4).

In the **European Union**, the **Floods Directive (2007/60/EC)** obliges member states to produce flood hazard maps (extent, depth, and where appropriate velocity for low-, medium-, and high-probability events) and risk maps on a six-year cycle (the third began in 2022). It prescribes no DEM accuracy; national practice does. The UK Environment Agency's lidar guidance and national 1 m DTM, and the Netherlands' AHN (used for statutory dike assessments where crest heights are legally consequential), set a de facto standard of decimeter-class, hydro-enforced lidar for detailed modeling. Rules thus specify the *input* DEM's tested accuracy and datum, not the map's accuracy, and none yet requires the probabilistic extents of §61.5. A modeler who reports a deterministic edge from a compliant DEM has met the rule; one who also reports the uncertain band has met the science.

## 61.7 Terrain indices and their resolution dependence

Hydrologic models and landscape analyses lean on derived indices whose values depend as much on the grid as on the land.

The **Topographic Wetness Index** (Beven and Kirkby 1979),

$$\mathrm{TWI} = \ln\!\left(\frac{a}{\tan\beta}\right),$$

where $a$ is the specific catchment area (upslope area per unit contour length, m) and $\beta$ the local slope, indexes a cell's tendency to saturate. Both terms are resolution-dependent: $a$ grows with cell size as coarse grids lose divides, and $\tan\beta$ shrinks as slopes are averaged over longer baselines, so TWI distributions shift upward and compress as resolution coarsens; the same threshold does not identify the same wet areas on a 5 m and a 30 m DEM. Flow-direction choice matters too: D8 streaks TWI along flow lines, D∞ and MFD smooth it. An unsmoothed 1 m lidar TWI is dominated by micro-topographic noise and usually less useful than the same index from a DTM smoothed to 5–10 m.

The **stream power index** $\mathrm{SPI} = a \tan\beta$ and the USLE/RUSLE **slope-length (LS) factor** inherit the same dependence, with 30 m grids systematically underestimating slope and overestimating length relative to 10 m; **HAND** depends on which cells are designated channel (the accumulation threshold of §61.3), and raising that threshold raises HAND everywhere. A workable heuristic: compute slope-dependent indices on a DTM smoothed or aggregated to 5–10 m (so that vertical noise of ~0.1 m over a 2 % slope does not dominate the gradient), but extract networks and barriers from the full-resolution surface; the heuristic fails in steep terrain and in flat terrain with important micro-relief.

**Catchment delineation** across DEMs is a sobering exercise. The same pour point on SRTM 30 m, Copernicus 30 m, a national 10 m DEM, and a 1 m lidar DTM typically agrees to within a few percent of basin area in mountainous terrain and disagrees by tens of percent in flat terrain, where a 1 m change in a divide's elevation moves the boundary kilometers; in agricultural lowlands, ditches and road embankments route water in ways no unenforced DEM reproduces. The test is simple and should be routine: delineate the basin on two independent DEMs and difference the polygons; where they disagree, look.

## 61.8 Urban drainage: when 2.5D is not enough

Pluvial (surface-water) flooding in cities is controlled by features no regional DTM resolves: curbs 10–15 cm high that confine shallow flow to the street; **inlets** connecting the surface to the pipe network at tens of liters per second each; building thresholds a step above the sidewalk; underpasses and basement ramps that collect water from blocks around them. The appropriate framework is a **coupled 1D sewer–2D surface** model (InfoWorks ICM, MIKE+, SWMM with a 2D engine, TUFLOW, HEC-RAS 2D with pipe networks) in which water enters at inlets, surcharges back when pipes are full, and flows over a DTM between buildings.

The DTM requirements are at the limit of airborne lidar. A 0.15 m curb needs cell spacing of 0.5 m or smaller *and* vertical noise well under 0.1 m, or **breaklines** along curb lines so the mesh follows them; QL1 lidar (8 pulses/m², RMSE$_z$ ≤ 10 cm) is marginal, and leading practitioners use centimeter-accurate mobile lidar along streets for curbs, inlets, and thresholds, fused with airborne lidar for roofs and yards. **Sub-grid** methods—storing within each computational cell a curb-aware storage–volume relationship—let a 2–5 m mesh carry the effect of curbs without resolving them.

Underpasses are multi-valued surfaces ([Chapter 35](ch35-voids-and-overhangs.md), [Chapter 63](ch63-buildings-cities-innerspace.md)): a road passing under a railway has two elevations at one $(x,y)$. A 2.5D DTM must choose, and the right choice for drainage is the lower surface with the overpass removed, so that the underpass—the site that actually floods—can pond. Beyond the DTM, an urban model needs pipe inverts (often in local or arbitrary datums), inlet locations and capacities, building thresholds, and roughness; each has its own epoch and uncertainty, and the DTM is frequently the best-documented of them.

## 61.9 The data gaps that matter most

Pixel statistics—RMSE$_z$, NVA, VVA—describe a DEM on average. Floods are controlled by extremes and connectivity, so the gaps that matter are the ones no pixel statistic reveals.

1. **Culverts and bridges.** Invisible from above, controlling in the model. A structure inventory with invert elevations and openings is the most valuable non-DEM dataset for a lowland hydraulic model; where none exists, automated detection of embankment–channel crossings produces candidates for field verification.
2. **Levee and embankment crests.** A crest 0.3 m lower than the DTM shows changes overtopping from zero to catastrophic. Survey crests; enforce as breaklines; check against the National Levee Database or equivalent; note the epoch, since embankments settle.
3. **Channel bathymetry.** §61.4. Measure it where in-channel conveyance matters; label synthetic channels as such.
4. **Tidal and coastal boundary datums.** The downstream boundary is a water level in a tidal datum (MLLW, MHHW, LAT; [Chapter 9](ch09-vertical-datums.md)); the DTM is orthometric (NAVD 88, ODN, NAP). The conversion (VDatum in the US) carries 5–20 cm of uncertainty that is rarely included; a boundary applied in the wrong datum biases every result by the full offset, often 0.5–1.5 m.
5. **Floodplain vegetation roughness.** Manning's $n$ is usually assigned from land-cover classes, but the same lidar that produced the DTM measures vegetation height and density; lidar-derived roughness maps ([Chapter 64](ch64-agriculture-forests-wetlands.md)) are more defensible and share the DTM's epoch.
6. **Epoch.** A 2015 DTM does not contain the 2019 subdivision or the new flood wall; a currency check against recent imagery is cheaper than a wrong map.

## Then & now

Through the 1980s and 1990s floodplain studies rested on **1D steady-state models (HEC-2, then HEC-RAS)** fed by field or photogrammetric cross-sections; DEMs, where used, were interpolated from contours (USGS 30 m DEMs from 10- or 20-ft contours) and inherited terracing artefacts that routing algorithms then had to fill. **Raster 2D codes** became practical in the late 1990s (Bates and De Roo 2000 introduced LISFLOOD-FP for the newly available DEMs), and systematic studies of DEM resolution effects followed (Horritt and Bates 2001, 2002).

The **SRTM** release (2000 acquisition; 90 m public from 2003, 30 m globally from 2014–15) made global flood modeling possible and its DEM-limited nature obvious; the 2010s brought global hazard models (Sampson et al. 2015), corrected derivatives (MERIT DEM 2017), and the argument for a better open DEM (Hawker et al. 2018; Schumann and Bates 2018). **Airborne lidar** reached national coverage in the Netherlands (AHN-1, begun 1996 ⟨H⟩), England (Environment Agency surveys from 1998; the National LiDAR Programme flew the country at 1 m between 2017 and early 2023), the Nordic countries, and much of the US under 3DEP (operational from 2013 ⟨H⟩), making decimeter DTMs the regulatory default where they exist and moving the frontier from "what is the ground elevation" to "what is under the embankment and under the water."

The 2020s added **FABDEM-class** corrections to global DSMs (Hawker et al. 2022), reduced-complexity codes fast enough for Monte Carlo (SFINCS; GPU LISFLOOD-FP), **probabilistic national flood maps** (the UK's Risk of Flooding from Rivers and Sea), and operational continental inundation mapping from HAND and synthetic rating curves (US National Water Model). The next step, under way, is a public global DTM of lidar-like accuracy and routine reporting of inundation probability rather than extent.

## Mathematics

**Shallow-water equations.** Depth-averaged conservation of mass and momentum on a bed of elevation $z_b(x,y)$, with depth $h$, velocity $(u,v)$, and free surface $\eta = z_b + h$:

$$\frac{\partial h}{\partial t} + \frac{\partial (hu)}{\partial x} + \frac{\partial (hv)}{\partial y} = 0,$$

$$\frac{\partial (hu)}{\partial t} + \frac{\partial}{\partial x}\!\left(hu^2 + \tfrac{1}{2} g h^2\right) + \frac{\partial (huv)}{\partial y} = -g h \frac{\partial z_b}{\partial x} - \frac{g n^2 u \sqrt{u^2+v^2}}{h^{1/3}},$$

and symmetrically for $v$. The bed enters through the slope source term $-gh\,\partial z_b/\partial x$ and through the depth $h = \eta - z_b$ in the friction term; a DEM error $\delta z_b$ therefore perturbs both the driving force (through its gradient—so *noise* in the DEM matters, not only bias) and the conveyance (through $h^{5/3}$ in Manning's law). The diffusive-wave simplification drops the inertial terms and makes flow a function of the free-surface gradient alone; the local-inertial scheme (Bates et al. 2010) keeps the local acceleration term and is what LISFLOOD-FP and HEC-RAS 2D's diffusion-wave option use.

**D8 and D∞.** For cell $(i,j)$ with neighbors $k = 1..8$ at distances $d_k$ ($\Delta$ cardinal, $\Delta\sqrt{2}$ diagonal), D8 assigns all flow to $\arg\max_k (z_{ij} - z_k)/d_k$. D∞ (Tarboton 1997) computes the steepest-descent direction on each of eight triangular facets around the cell, takes the steepest facet, and splits flow between its two bounding neighbors in proportion to the angular distance of the descent direction from each. Specific catchment area is $a = A/\ell$ with $\ell$ the contour length (grid spacing for a cell).

**Priority-flood** (Barnes, Lehman, and Mulla 2014). Push all edge cells onto a priority queue ordered by elevation; repeatedly pop the lowest cell $c$; for each unvisited neighbor $n$, set $z_n \leftarrow \max(z_n, z_c)$, mark it visited, and push it. Each cell is pushed and popped once, so the cost is $O(n \log n)$; with $z_n \leftarrow \max(z_n, z_c + \epsilon)$ the filled flats acquire a gradient for routing. Breaching instead walks from the depression bottom along the least-cost path to the first lower cell and lowers the cells along it.

**Inundation-extent error with correlated DEM error.** On a transect of slope $\tan\beta$ with DEM error $\epsilon$ of variance $\sigma_z^2$ and water-surface error $\delta\eta$, the edge error is $\delta x \approx (\epsilon - \delta\eta)/\tan\beta$, so $\sigma_x^2 \approx (\sigma_z^2 + \sigma_\eta^2)/\tan^2\beta$ *locally*. The flood's *area* uncertainty depends on the number of independent edge segments: for edge length $L$ and correlation range $r$, about $L/r$ segments, giving $\sigma_A \approx \sigma_x \sqrt{L\, r}$ for correlated error versus $\sigma_x \sqrt{L\,\Delta}$ for independent per-cell error—larger by $\sqrt{r/\Delta}$, a factor of about 9 for $r$ = 150 m and $\Delta$ = 2 m. This is why independent-noise Monte Carlo underestimates extent uncertainty.

## Validation & uncertainty

A flood model is validated against observed floods, but most of what goes wrong traces to the DEM and can be tested before any hydraulics run.

**Pre-model DEM checks.** (1) Confirm the surface is a DTM: difference it against a DSM or canopy-height product; inspect hillshades along riparian corridors. (2) Confirm the datum against benchmarks and against the boundary-condition datum; a geoid or tidal offset's sign and magnitude are the first things to get wrong. (3) Test accuracy by land cover with independent check points (NVA, VVA; [Chapter 53](ch53-accuracy-assessment.md)); VVA in floodplain woodland and marsh is the relevant number and is routinely 2–4× the NVA. (4) Walk the structure list: confirm each culvert and bridge is enforced; difference each levee crest against its surveyed profile. (5) Audit depressions deeper than ~0.3 m: real (keep), structure artefact (breach), noise (fill). (6) Check currency against recent imagery.

**Propagating DEM uncertainty.** Run the correlated Monte Carlo of §61.5 with an error model from the check-point residuals (variance by land cover, semivariogram range); report inundation probability, the area of the uncertain band, and the sensitivity of key outcomes (number of buildings in the $P \ge 0.5$ extent; depth at critical facilities) to the DEM term alone. Where a full-model Monte Carlo is too costly, use a reduced-complexity code or a HAND proxy for the ensemble and the full model for the deterministic run, and say so.

**Post-model validation.** Compare predicted extents against observed outlines (post-event imagery, wrack lines, surveyed high-water marks) with the critical success index $F = A_{\text{hit}}/(A_{\text{hit}} + A_{\text{miss}} + A_{\text{false}})$, and predicted water surfaces against high-water marks (RMSE). Then ask whether residuals cluster at structures (enforcement), along forest edges (VVA), or along the whole reach (discharge or roughness, not the DEM). A model that matches high-water marks to 0.15 m but misses the extent behind an embankment has a DEM-topology problem.

> **Uncertainty budget.** Illustrative error sources for a lowland lidar-based 2D flood model (measure your own).
>
> | Component | Typical σ or bias | Enters as | Controlled by |
> |---|---|---|---|
> | DTM, open ground (NVA) | 0.05–0.10 m RMSE$_z$ | Bed elevation, correlated 50–300 m | Lidar QL, check points |
> | DTM, floodplain woodland/marsh (VVA) | 0.15–0.30 m (95th pct), positive bias | Bed elevation, correlated with land cover | Leaf-off acquisition, classification |
> | Channel bathymetry (measured) | 0.1–0.3 m | Conveyance | Survey method, datum tie |
> | Channel bathymetry (synthetic) | 0.5–1.5 m | Conveyance | Hydraulic geometry assumptions |
> | Levee crest (DTM vs survey) | 0.1–0.3 m; local gaps | Overtopping threshold | Breaklines, crest survey |
> | Structure enforcement | Binary (open/closed) | Connectivity | Inventory completeness |
> | Tidal datum conversion at boundary | 0.05–0.20 m | Boundary stage | VDatum/national model |
> | Roughness (Manning's $n$) | ± 30–50 % of $n$ | Stage via $h^{5/3}$ | Calibration, lidar-derived roughness |
>
> On a 1:1000 floodplain each 0.1 m of combined water-surface uncertainty is 100 m of edge uncertainty; the DTM is rarely the largest single term in a calibrated model but is the one term that is cheap to characterize and expensive to ignore.

## Software

**Open source:** **LISFLOOD-FP** (Bristol; raster 2D with sub-grid channels, well-documented resolution behavior). **SFINCS** (Deltares; reduced-complexity compound flooding built for ensembles). **ANUGA** (Geoscience Australia; unstructured SWE). **TauDEM** (Utah State; D∞, priority-flood, MPI). **WhiteboxTools** (breaching, filling, hundreds of terrain tools). **RichDEM** (Barnes's algorithms as a library). **pysheds** (pure Python). **GRASS GIS** `r.watershed`/`r.stream.*` (least-cost routing without explicit filling). **SAGA GIS** (TWI, LS, many flow algorithms). **GeoFlood** (HAND and synthetic rating curves). **QGIS** as the front end to all of these.

**Free but closed:** **HEC-RAS** and **HEC-HMS** (USACE; the de facto regulatory codes in the US—RAS Mapper handles terrain, breaklines, and structures directly); **VDatum** (NOAA; tidal–orthometric transformations with published uncertainties). **SWMM** (US EPA) is public-domain software whose engine source is published on GitHub (USEPA/Stormwater-Management-Model); it belongs with the open tools above in practice.

**Commercial:** **TUFLOW** (BMT; quadtree/sub-grid 2D, strong in urban work). **MIKE+ / MIKE 21 / MIKE SHE** (DHI). **InfoWorks ICM** (Autodesk; dominant urban 1D–2D code in the UK). **Flood Modeller** (Jacobs). **Delft3D FM** (Deltares; open core, commercial support). **ArcHydro** (Esri; delineation and conditioning).

## Standards & guides

- **FEMA, *Guidelines and Standards for Flood Risk Analysis and Mapping*** (living document; *Elevation Guidance*, current edition). Elevation requirements for NFIP studies: USGS LBS QL2 or better, NAVD 88, accuracy testing and reporting.
- **USGS, *Lidar Base Specification*** (online, versioned; 2022 revision and later). QL definitions, NVA/VVA, hydro-flattening and breakline requirements.
- **ASPRS, *Positional Accuracy Standards for Digital Geospatial Data*, Ed. 2 (2023).** Accuracy classes and testing procedures for the DTM.
- **USACE, EM 1110-2-1619 *Risk-Based Analysis for Flood Damage Reduction Studies* (1996)** and **EM 1110-2-1913 *Design and Construction of Levees* (2000)**; **44 CFR 65.10** for NFIP levee accreditation.
- **European Union, Directive 2007/60/EC on the assessment and management of flood risks** and the associated CIS guidance documents on flood hazard and risk mapping.
- **Environment Agency (UK), National LiDAR Programme specification and lidar-for-flood-modeling guidance** (verify current edition).

## Pitfalls

- **Running a flood model on a DSM, or on a global "DEM" assumed to be bare earth** → SRTM, ASTER GDEM, AW3D30, and the Copernicus DEM are surface models labelled "DEM" → difference against a canopy-height map or lidar DTM; expect meters of positive bias in forest and cities; use FABDEM or a national DTM and still propagate the residual.
- **Filling depressions that were real detention basins, potholes, or quarries** → priority-flood fills indiscriminately → audit the fill-depth raster; keep real basins; breach at structures; document thresholds.
- **A bridge deck or culvert embankment blocking the channel** → classifiers keep decks; embankments are continuous from above → walk the structure inventory; enforce; look for flow accumulation terminating at roads.
- **Levee or floodwall lost at coarse resolution** → crest narrower than the cell averages away → enforce crests as breaklines; compare DTM crests with surveyed profiles; never average-downsample across a levee.
- **Hydro-flattened river treated as having a channel** → the ribbon is at water level, not bed level → add measured or synthetic bathymetry and label which.
- **Tidal boundary in the wrong vertical datum** → levels published in MLLW/LAT, DTM in NAVD 88/ODN → transform with VDatum or national tools; carry the transformation uncertainty; check that mean sea level sits where it should on the DTM.
- **Deterministic flood edge from a DEM with σ$_z$ of 0.5–1 m on flat terrain** → the edge is uncertain by hundreds of meters → report probability of inundation; apply Gesch's minimum-threshold rule.
- **Monte Carlo with independent per-cell noise** → easy to code, wrong physics → use correlated error fields with the check-point semivariogram's range; confirm realizations do not pond spuriously.
- **Comparing TWI, slope, or catchment area across resolutions** → all are resolution-dependent by construction → recalibrate thresholds per resolution; state grid spacing with every index.
- **Leaf-on lidar DTM in floodplain forest and marsh** → VVA degrades to decimeters with positive bias → prefer leaf-off, low-water acquisitions; report VVA by class ([Chapter 64](ch64-agriculture-forests-wetlands.md)).
- **Urban model without curbs and inlets** → a 1–2 m airborne DTM does not resolve a 0.15 m curb → mobile lidar or breaklines along curbs; sub-grid storage; field-verify inlets.

## Key takeaways

- Hydraulics needs a bare-earth, hydro-enforced, thin-feature-preserving DTM with reported uncertainty; a finer DTM that bridges a culvert is worse than a coarser one that does not.
- DEM sensitivity concentrates on controls—levee crests, embankments, bridge openings, channel beds; validate those individually, not only with pixel statistics.
- Condition by cause: breach at structures, fill noise, keep real basins, enforce rather than burn on lidar DTMs; report thresholds.
- Routing and terrain indices are resolution-dependent: D8 for networks, D∞/MFD for indices, smooth before slope-based indices on fine grids.
- Lidar does not see the channel; add bathymetry (measured if the question is in-channel; synthetic and labelled if not) and survey reservoir storage curves.
- Propagate vertical error with spatially correlated realizations; on a 1:1000 floodplain every 0.1 m of elevation uncertainty is 100 m of edge uncertainty.
- Regulations specify the input DTM's tested accuracy and datum (FEMA: USGS QL2, NAVD 88), not the map's accuracy—meet the rule, then report the uncertain band anyway.
- The most consequential errors—boundary datum mismatches and missing structures—are invisible in RMSE and findable before the model runs.

## References

- Barnes, R., Lehman, C., and Mulla, D. (2014). Priority-flood: An optimal depression-filling and watershed-labeling algorithm for digital elevation models. *Computers & Geosciences*, 62:117–127.
- Bates, P. D., and De Roo, A. P. J. (2000). A simple raster-based model for flood inundation simulation. *Journal of Hydrology*, 236(1–2):54–77.
- Bates, P. D., Horritt, M. S., and Fewtrell, T. J. (2010). A simple inertial formulation of the shallow water equations for efficient two-dimensional flood inundation modelling. *Journal of Hydrology*, 387(1–2):33–45.
- Beven, K. J., and Kirkby, M. J. (1979). A physically based, variable contributing area model of basin hydrology. *Hydrological Sciences Bulletin*, 24(1):43–69.
- Gesch, D. B. (2018). Best practices for elevation-based assessments of sea-level rise and coastal flooding exposure. *Frontiers in Earth Science*, 6:230.
- Hawker, L., Bates, P., Neal, J., and Rougier, J. (2018). Perspectives on digital elevation model (DEM) simulation for flood modeling in the absence of a high-accuracy open access global DEM. *Frontiers in Earth Science*, 6:233.
- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., and Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters*, 17(2):024016.
- Horritt, M. S., and Bates, P. D. (2001). Effects of spatial resolution on a raster based model of flood flow. *Journal of Hydrology*, 253(1–4):239–249.
- Horritt, M. S., and Bates, P. D. (2002). Evaluation of 1D and 2D numerical models for predicting river flood inundation. *Journal of Hydrology*, 268(1–4):87–99.
- Kulp, S. A., and Strauss, B. H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications*, 10:4844.
- Lindsay, J. B. (2016). Efficient hybrid breaching-filling sink removal methods for flow path enforcement in digital elevation models. *Hydrological Processes*, 30(6):846–857.
- Nobre, A. D., Cuartas, L. A., Hodnett, M., Rennó, C. D., Rodrigues, G., Silveira, A., Waterloo, M., and Saleska, S. (2011). Height Above the Nearest Drainage – a hydrologically relevant new terrain model. *Journal of Hydrology*, 404(1–2):13–29.
- O'Callaghan, J. F., and Mark, D. M. (1984). The extraction of drainage networks from digital elevation data. *Computer Vision, Graphics, and Image Processing*, 28(3):323–344.
- Poppenga, S. K., and Worstell, B. B. (2016). Hydrologic connectivity: Quantitative assessments of hydrologic-enabled drainage structures in an elevation model. *Journal of the American Water Resources Association*, 52(3):578–599.
- Sampson, C. C., Smith, A. M., Bates, P. D., Neal, J. C., Alfieri, L., and Freer, J. E. (2015). A high-resolution global flood hazard model. *Water Resources Research*, 51(9):7358–7381.
- Schumann, G. J.-P., and Bates, P. D. (2018). The need for a high-accuracy, open-access global DEM. *Frontiers in Earth Science*, 6:225.
- Tarboton, D. G. (1997). A new method for the determination of flow directions and upslope areas in grid digital elevation models. *Water Resources Research*, 33(2):309–319.
- Wechsler, S. P. (2007). Uncertainties associated with digital elevation models for hydrologic applications: a review. *Hydrology and Earth System Sciences*, 11(4):1481–1500.
- FEMA (current). *Guidelines and Standards for Flood Risk Analysis and Mapping: Elevation Guidance*. Federal Emergency Management Agency.
- USACE (1996). *Risk-Based Analysis for Flood Damage Reduction Studies*, EM 1110-2-1619. US Army Corps of Engineers.
- European Parliament and Council (2007). Directive 2007/60/EC on the assessment and management of flood risks. *Official Journal of the European Union*, L 288:27–34.

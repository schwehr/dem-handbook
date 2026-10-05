# Chapter 55 — Public DEM and bathymetry products: catalog and comparison

> **Part XI — Validation, quality, and judging data.** Having learned how to test any elevation dataset ([Chapter 53](ch53-accuracy-assessment.md)) and how to judge one delivered with thin metadata ([Chapter 54](ch54-evaluating-others-data.md)), this chapter applies those skills to the products most readers will actually download: the global, national, and commercial DEMs and bathymetric grids.

**In this chapter.** Twenty-five years ago there was one global DEM worth having; today there are a dozen on land, half a dozen for the seafloor, spaceborne-altimetry point products that behave like truth, and a growing commercial tier — each from a different sensor and date, in a different vertical datum, with a different notion of "surface" and a different licence. This chapter catalogues them: how each was made, when, in what datum, with what nominal and effective resolution, what accuracy its makers report and independent assessments found, and what voids, masks, artefacts, and licence terms it carries. It then gives a DEMIX-style comparison framework, a fitness-by-use table, and the errata that bite practitioners repeatedly, so that you can choose a product for a given use, defend the choice, and know which local test to run before trusting it. Standardized comparison tables are in [Appendix E](../appendices/appendix-e-public-products-tables.md).

## 55.1 Global and near-global land DEMs

The global land DEMs fall into three generations. The first (GTOPO30, GMTED2010) compiled existing cartography. The second measured the Earth from orbit — SRTM with C-band interferometry, ASTER and ALOS PRISM with optical stereo, TanDEM-X with X-band bistatic interferometry — and produced **DSMs** that include canopy and buildings. The third measures nothing new: it edits, fuses, and machine-learns its way from second-generation DSMs toward **DTMs** (MERIT, FABDEM, CoastalDEM, DeltaDTM, DiluviumDEM, GEDTM30), increasingly calibrated against spaceborne lidar. A third-generation product inherits the voids, dates, and datum of its parents plus whatever its correction model introduces.

### 55.1.1 SRTM and NASADEM

The **Shuttle Radar Topography Mission** flew on *Endeavour* for eleven days in February 2000 and mapped land between 60° N and 56° S with a C-band (5.6 cm) single-pass interferometer on a 60 m mast (Farr et al. 2007). C-band scatters from within the upper canopy, so in dense forest the phase centre sits several to more than ten metres above the ground. The specification was 16 m absolute vertical (LE90) and 20 m horizontal (CE90); global validation found continental absolute vertical errors of about 6–9 m LE90 (Rodríguez et al. 2006). Heights are orthometric (EGM96), integer metres, on a 1″ grid released outside the United States only in 2014–2015. Voids from layover, shadow, and low coherence concentrate in the Himalaya, Andes, and deserts; SRTM v3 (SRTMGL1) filled them from ASTER GDEM and other sources. **NASADEM** (2020) reprocessed the raw signal data with improved unwrapping, fewer voids, and a vertical adjustment to ICESat GLAS that removed much of the long-wavelength bias (Crippen et al. 2016); it remains a February-2000 C-band DSM in EGM96 with metre-level along-track striping visible in slope maps. Licence: public domain. Use it for the 2000 epoch and legacy continuity; for new work Copernicus DEM is usually better.

### 55.1.2 ASTER GDEM v3

The **ASTER Global DEM** stacks all cloud-free along-track stereo pairs from Terra (2000–2013 for v3) and averages the resulting DEMs cell by cell (Abrams, Crippen & Fujisada 2020), covering 83° N–83° S at 1″ in EGM96. Version 3 (2019) added about 360,000 scenes, reducing voids, pits, and bumps; reported accuracy is 8–12 m RMSE depending on terrain and stack depth (supplied as the NUM layer). Independent assessments consistently rank it the noisiest 1″ product (Uuemaa et al. 2020; Guth & Geoffroy 2021; Bielski et al. 2024): its effective resolution is much coarser than 30 m, and scene-boundary "mole runs" and residual cloud artefacts survive editing. Licence: free with attribution (NASA/METI). Use it only above 60° N where Copernicus is unavailable, or as a third opinion when two radar DEMs disagree.

### 55.1.3 ALOS World 3D — AW3D30

JAXA's **AW3D30** is the free 1″ downsample of the commercial 5 m AW3D DSM from ALOS PRISM triplet stereo acquired 2006–2011 (Tadono et al. 2014; Takaku et al. 2020). Being optical it sits on canopy tops and roofs with essentially no penetration — the cleanest DSM definition among the global products — and has no layover, but cloud and snow failures were filled from SRTM, GDEM, and other sources. Heights are orthometric (EGM96). Version 3.x (2019–2021) fixed coastline and void issues; v4.1 (April 2024) re-filled voids and corrected anomalies in 19,051 tiles (JAXA 2024). JAXA reports about 5 m RMSE for the 5 m source against GNSS control; independent evaluations place the 1″ product at 2.5–5 m RMSE in open terrain. Licence: free for commercial and non-commercial use with registration. Use it as an optical DSM to pair with a radar DSM for forest-height reasoning, or where X-band products show urban layover or ice penetration.

### 55.1.4 TanDEM-X DEMs

**TanDEM-X** flew two X-band (3.1 cm) SAR satellites in close formation from 2010, acquiring at least two global coverages in 2011–2013 plus difficult-terrain repeats to 2015, and produced the first homogeneous global DEM at 12 m (0.4″) posting (Rizzoli et al. 2017; Zink et al. 2021). The specification was 10 m absolute LE90 and 2 m relative LE90 (4 m on slopes over 20 %); validation against ICESat found about 3.5 m absolute LE90. Heights are **ellipsoidal (WGS 84 G1150)** — the most common trap. Each cell has a **height error map (HEM)** value derived from interferometric coherence, one of the few per-pixel uncertainty layers among global DEMs. X-band penetrates vegetation less than C-band but still enters sparse canopy and penetrates dry snow and firn by metres. Tiers: the 12 m DEM (scientific proposal or commercial licence through Airbus as **WorldDEM**), the free **TanDEM-X 30 m Edited DEM** (2023; voids filled and water edited; free for scientific use after registration under a DLR licence), and the 90 m DEM (free since 2018). Known artefacts: residual unwrapping errors in steep terrain, urban layover and multipath spikes, and acquisition-date differences between adjacent tiles.

### 55.1.5 Copernicus DEM (GLO-30, GLO-90, EEA-10)

The **Copernicus DEM** is the European Commission's edited derivative of WorldDEM: TanDEM-X data from 2011–2015 with voids filled, water bodies flattened, coastlines edited, "implausible terrain structures" removed, and airports flattened (Airbus 2022, Product Handbook Issue 5.0). It is a DSM; editing does not remove buildings or trees. Heights were converted to orthometric relative to **EGM2008** — unlike SRTM and AW3D30's EGM96, a difference of up to several metres regionally. GLO-90 (3″) is free worldwide, GLO-30 (1″) free except for a few tiles over Armenia and Azerbaijan, and EEA-10 (10 m) restricted to European institutions. Each tile ships with editing (EDM), water-body (WBM), filling (FLM), and height-error (HEM) masks that say which cells were measured and which invented. Independent assessments agree GLO-30 is the best general-purpose 1″ DSM: Guth & Geoffroy (2021) found it closest to lidar and ICESat-2, Purinton & Bookhagen (2021) found the best inter-pixel consistency in the arid Andes, and DEMIX (Bielski et al. 2024) ranked it first of six. Open-terrain RMSE is typically 1–3 m; forests and cities carry the DSM bias. Annual re-releases (2021_1 through 2024_1 and later) correct tiles and masks; record the release. Licence: free with attribution under the Copernicus DEM licence, whose text must accompany redistributed GLO-30.

### 55.1.6 MERIT DEM and MERIT Hydro

**MERIT DEM** (Yamazaki et al. 2017) was the first widely used "error-removed" global DEM: starting from SRTM v2.1 and AW3D30 (above 60° N), it removed absolute bias (with ICESat), stripe noise (2-D filter), speckle, and tree-height bias (canopy model plus per-biome relation) to make a 3″ product whose fraction of land with error under 2 m rose from 39 % to 58 % by the authors' assessment. It is closer to a DTM than its parents but keeps residual canopy bias in dense forest and residual stripes. **MERIT Hydro** (Yamazaki et al. 2019) adds flow direction, upstream area, and hydrologically adjusted elevations. Both are EGM96. Licence: CC BY-NC 4.0 or ODbL 1.0 at the user's choice — the ODbL path allows commercial use with share-alike. Use MERIT for 90 m continental hydrology; FABDEM and GEDTM30 are its 30 m successors.

### 55.1.7 FABDEM

**FABDEM** ("Forest And Buildings removed Copernicus DEM"; Hawker et al. 2022) applies random-forest regressions trained on reference lidar to strip canopy and building heights from GLO-30, giving a 1″ product in EGM2008. The authors report mean absolute error falling from 2.0 m to 1.1 m in built-up areas and from 5.2 m to 2.9 m in forest on their test set; DEMIX ranked it second behind its parent on DSM-rewarding criteria and ahead on DTM-like ones. Version 1-2 (2023) corrected artefacts in v1-0/v1-1. Characteristic failures are **terracing** (1–2 m steps where the correction switches land-cover class), over-correction on cliffs, and ghosts of large buildings. Licence: **CC BY-NC-SA 4.0**; commercial use requires a Fathom licence — and a consultancy delivering a flood study to a paying client is not making non-commercial use.

### 55.1.8 CoastalDEM, DeltaDTM, DiluviumDEM

Three products target the low-elevation coastal zone, where a few metres of DSM bias reclassify tens of millions of people above or below a flood level. **CoastalDEM** (Kulp & Strauss 2018; v2.1, 2021) corrects SRTM/NASADEM with a neural network trained on US lidar; it is free for non-commercial use under Climate Central's licence and underpinned the widely reported tripling of global sea-level-rise exposure (Kulp & Strauss 2019; [Chapter 56](ch56-case-files.md)). **DeltaDTM** (Pronk et al. 2024) is a 1″ coastal DTM below about 10 m built from GLO-30 corrected with ICESat-2 and GEDI, with reported mean absolute error near 0.45 m against lidar in its validation areas; CC BY 4.0. **DiluviumDEM** (Dusseau, Zobel & Schuldt 2023) likewise corrects Copernicus with an ICESat-2-trained gradient-boosted model, with RMSE under 1 m on its coastal test set; CC BY 4.0 (verify). All three are estimates, not measurements, least certain in mangrove, dense urban, and reclaimed land, and all inherit their parents' dates.

### 55.1.9 GEDTM30 and the ensemble generation

**GEDTM30** (Ho et al. 2025) is OpenGeoHub's 1″ "global ensemble DTM": a two-stage random-forest fusion of GLO-30, AW3D30, and other covariates against roughly 30 billion ICESat-2 and GEDI ground points, published with a per-pixel uncertainty layer (the spread of the forest's trees) and derived terrain parameters at six scales. The authors report gains over MERIT, FABDEM, and FathomDEM in built-up and forested areas; independent evaluations are so far few. Licence CC BY 4.0. The ensemble approach — DTM-like surface, uncertainty layer, permissive licence — inherits its reference's limits: ICESat-2 and GEDI ground returns are sparse, biased on slopes, and unreliable under the densest canopy, so the learned surface is smoothest where least constrained. Treat the uncertainty layer as model disagreement, not validated 1σ.

### 55.1.10 Legacy and coarse products

**GTOPO30** ⟨H⟩ (USGS EROS, 1996) compiled DTED, Digital Chart of the World contours, and national sources into a 30″ grid and was the global DEM for a decade. **GMTED2010** (Danielson & Gesch 2011) replaced it at 30″, 15″, and 7.5″ with mean, median, minimum, maximum, and breakline-emphasis variants. **ETOPO1** (Amante & Eakins 2009) and **ETOPO 2022** (NOAA NCEI 2022) merge topography and bathymetry at 1′ and 15″ in "ice surface" and "bedrock" versions, for visualization and planetary-scale modelling only.

### 55.1.11 Behaviour by land cover

Sensor physics makes the three main 1″ DSMs differ systematically by land cover. On bare flat ground all are unbiased to within a metre after datum reconciliation, Copernicus least noisy. In forest, AW3D30 sits at the canopy top, Copernicus/TanDEM-X a few metres below it, NASADEM deeper still. In cities both record roofs, but radar adds layover streaks and spikes beside tall buildings while optical blurs edges; on dry snow X-band penetrates metres and optical stereo fails for lack of texture. "DSM" is a spectrum (Uuemaa et al. 2020; Guth & Geoffroy 2021), and the land-cover-stratified error table is the one to read.

<!-- figure: Figure 55.1 — Schematic cross-section through forest, city, and glacier showing where the SRTM (C-band), TanDEM-X/Copernicus (X-band), AW3D30 (optical stereo), and ICESat-2 ground surfaces sit relative to true ground, with typical offsets in metres -->

> **Definitions that bite.** "Copernicus DEM" is a DSM with water, coastlines, and airports edited; it is not a DTM, and its handbook says so. Yet it is routinely fed to flood models as bare earth, and the resulting 2–5 m canopy and building bias exceeds the product's own vertical accuracy. If a model needs terrain, start from FABDEM, DeltaDTM, GEDTM30, or national lidar — and check the licence.

## 55.2 Regional and national high-resolution DEMs

Where a national lidar programme exists, nothing in §55.1 should be used except for change detection against the past or for areas the programme has not reached. Programmes differ in point density, surface products, vertical datum, update cadence, and licence; [Appendix E](../appendices/appendix-e-public-products-tables.md) tabulates them, and this section sketches the landscape.

### 55.2.1 United States: 3DEP, CoNED, CUDEM

The USGS **3D Elevation Program** (Sugarbaker et al. 2014) coordinates lidar acquisition to the **Lidar Base Specification** at QL2 (≥ 2 pulses/m², ≤ 10 cm RMSE$_z$ non-vegetated) or QL1 (≥ 8 pulses/m²) across the conterminous United States, with IfSAR at QL5 in Alaska. Deliverables are classified LAZ point clouds (increasingly COPC), 1 m DEMs, and seamless 1/3″ and 1″ DEMs, in NAD83(2011) and NAVD88 realized through whichever hybrid geoid (GEOID12B, GEOID18) was current for each project — so the "seamless" layer contains geoid-model seams of a few centimetres between projects. First national coverage was completed in the mid-2020s, with a next-generation plan (the 3D National Topography Model) integrating hydrography. NOAA NCEI's **CUDEM** tiles (1/9″ ≈ 3 m, 1/3″ ≈ 10 m) merge 3DEP lidar, topobathymetric lidar, and bathymetric surveys into seamless topobathymetric DEMs in NAVD88 along the coasts with a documented source hierarchy; **CoNED** products are their predecessors. Licence: public domain.

### 55.2.2 Europe

The **Netherlands' AHN** is the longest national lidar time series anywhere — AHN1 (1997–2003, ~1 point per 16 m²), AHN2 (2007–2012, 6–10 points/m²), AHN3 (2014–2019), AHN4 (2020–2022), AHN5 (2023–) — all in NAP and CC0, and invaluable for subsidence studies ([Chapter 38](ch38-plate-motion-and-vlm.md)). **England's Environment Agency** publishes 1 m composite DTM/DSM from the National LiDAR Programme (2016–2023) in ODN via OSGM15 under the Open Government Licence. **Denmark** (DHM, ≥ 4 points/m², 0.4 m grids, DVR90), **Finland** (2 m national model 2008–2019; 5 points/m² recollection from 2020), **Norway** (Høydedata, 1 m, NN2000), **Sweden** (1 m national lidar DEM, second campaign underway), **Switzerland** (swissALTI3D 0.5 m DTM on a six-year cycle and swissSURFACE3D, free since 2021), **Spain** (PNOA-LiDAR: two national covers at 0.5 and 1–2 points/m², third in progress, CC BY 4.0), **France** (LiDAR HD at ≥ 10 points/m², 2021–2026, following RGE ALTI, whose metadata layer shows which cells were lidar, radar, or photogrammetry), **Poland** (ISOK, 4–12 points/m²), **Estonia** (annual rotating lidar since 2008), **Slovenia** (national lidar 2011–2015), **Austria** (provincial 1 m lidar aggregated to a 10 m national model), and **Italy** (10 m TINITALY plus coastal and riverine lidar patchworks) complete the picture. Licences are converging on CC BY 4.0 or national open licences under the EU open-data directive, but check each.

### 55.2.3 Americas, Asia, and Oceania

**Canada's HRDEM** publishes 1–2 m lidar DTM/DSM in the south and 5 m ArcticDEM-derived products in the north, in CGVD2013, under the Open Government Licence – Canada. **Mexico's INEGI** offers the 15 m CEM nationally and 5 m lidar for selected areas. **Japan's GSI** distributes 5 m DEMs (5A lidar, 5B photogrammetry — different accuracies) and 1 m lidar DEMs in JGD2011 heights. **Australia's ELVIS** portal serves the 1″ SRTM-derived DEM-S/DEM-H, 5 m lidar and photogrammetric DEMs, and raw lidar; **New Zealand's LINZ** programme (2018–) serves 1 m DTM/DSM through the LINZ Data Service and OpenTopography. **Brazil** has state and city programmes but no national lidar; **Argentina's IGN MDE-Ar** is a corrected 30 m SRTM-based national model (verify current version).

### 55.2.4 ArcticDEM and REMA

The Polar Geospatial Center's **ArcticDEM** (Porter et al. 2018; v4.1, 2023) and **REMA** (Howat et al. 2019; v2, 2022) are 2 m DSMs built by the SETSM algorithm from Maxar WorldView and GeoEye stereo pairs over all land above 60° N and Antarctica. **Strips** are individual stereo-pair DEMs with an acquisition date and, where possible, an ICESat/ICESat-2 registration offset (applied or merely reported — the metadata says which); **mosaics** (2 m to 1 km) assemble the best strips with feathering and can mix dates by years across a tile, so a glacier front may appear twice. Heights are **ellipsoidal (WGS 84)**. Strip-level biases of metres remain without altimetry control, and matching blunders (spikes and pits of tens of metres) are flagged but not all removed; read the mask layers. Licence: CC BY 4.0 with acknowledgement of the Maxar imagery licence. They are the only sub-10 m public DEMs across much of the Arctic and all of Antarctica, and their dated strips make them a glaciological instrument rather than merely a map.

<!-- figure: Figure 55.2 — Map of national lidar coverage and point density by country circa 2025, with ArcticDEM/REMA extents, showing the "lidar deserts" of the Global South discussed in Chapter 56 -->

## 55.3 Global and regional bathymetry

Bathymetric compilations differ from land DEMs in one fundamental way: most of their cells are not measurements. Global ocean grids have direct soundings in roughly a quarter of their cells and predict the rest from satellite gravity, so a grid without its source or type-identifier layer is uninterpretable, and the first question to ask is "which cells are real?" [Chapter 20](ch20-sonar.md) covers soundings, [Chapter 23](ch23-satellite-derived-bathymetry.md) altimetric prediction, and [Chapter 48](ch48-compositing.md) the compositing itself.

### 55.3.1 GEBCO

The **GEBCO grid** (GEBCO Compilation Group 2024, 2025) is a 15″ global terrain model of ocean and land released annually since 2019 under the Nippon Foundation–GEBCO **Seabed 2030** project. Its base is SRTM15+ (below), overlaid with compilations from the four Seabed 2030 regional centres and the IBCAO/IBCSO polar grids, with land topography inherited from the base. Every release ships a **Type Identifier (TID) grid** distinguishing direct measurements (multibeam, single-beam, seismic, lidar, isolated soundings) from indirect ones (gravity prediction, interpolation, contours, pre-generated grids) — the grid's single most important companion. GEBCO_2024 appeared in July 2024 and GEBCO_2025 in August 2025; Seabed 2030 reported 27.3 % of the seafloor mapped to its resolution standard as of June 2025, up from about 6 % in 2017. GEBCO heights are relative to approximate mean sea level with no formal vertical datum and no per-cell uncertainty, and the product carries an explicit **"not to be used for navigation"** statement; coastal cells are routinely wrong by tens of metres because gravity is blind in shallow water and chart soundings are sparse. Licence: public domain. Use it for basin-scale context, ocean modelling, and visualization, never for the depth of a specific place.

### 55.3.2 SRTM15+, ETOPO 2022, GMRT

**SRTM15+** (Tozer et al. 2019; V2.x) is Scripps' 15″ grid of edited shipboard soundings plus depths predicted from altimetric gravity, with a source-identification grid; predicted depths are accurate to roughly 100–200 m in the deep ocean, worse on sedimented or rugged seafloor. Licence: free (verify terms for the current version). **ETOPO 2022** (NOAA NCEI 2022) merges GEBCO, regional compilations, and land DEMs at 15″ and 30″ in "ice surface" and "bedrock" variants referenced to approximate MSL/EGM2008; it is a visualization and modelling product. **GMRT** (Ryan et al. 2009) is Lamont-Doherty's synthesis of cleaned shipboard multibeam at native resolution (~100 m where surveyed) over a GEBCO/SRTM15+ base; its mask layer is the best quick look at which parts of the deep ocean are actually mapped.

### 55.3.3 Regional compilations: EMODnet, IBCAO, IBCSO

**EMODnet Bathymetry** publishes a DTM of European seas at 1/16′ (~115 m) from surveys contributed by national hydrographic offices and institutes, with a per-cell source reference and quality index, in LAT-referenced depths over most of the shelf; the 2022/2024 releases are CC BY 4.0. **IBCAO v4** (Jakobsson et al. 2020; 200 m, polar stereographic, with TID) was superseded by **IBCAO v5** (2024; 100 m), and **IBCSO v2** (Dorschel et al. 2022) is the 500 m Southern Ocean counterpart, also with a TID. Both feed GEBCO, both mix multibeam, single-beam, and seismic data of very different vintage, and their TIDs show where icebreakers have been.

### 55.3.4 United States: NBS/BlueTopo and CUDEM

NOAA's **National Bathymetric Source (NBS)** and its public product **BlueTopo** compile the best available surveys, charted soundings, and other sources into tiled GeoTIFFs with three bands — elevation, **per-cell uncertainty**, and a **contributor** band keyed to a raster attribute table naming the source survey, its date, and its qualification. Resolution varies by tile (2–16 m typical nearshore), the vertical reference is MLLW (ellipsoid-referenced versions in development), and coverage has expanded coast by coast since 2022. It is "not for navigation" because it may contain unqualified data, but it is the model for what every public bathymetric compilation should ship: depth, uncertainty, and source per cell. **CUDEM** (§55.2.1) is NCEI's topobathymetric counterpart.

### 55.3.5 National portals and crowdsourced bathymetry

The **UKHO ADMIRALTY Marine Data Portal** (survey grids to 1–4 m under the Open Government Licence), **AusSeabed**, **LINZ**, **CHS NONNA** (Canadian 10 m and 100 m "non-navigational" bathymetry), and the Japanese hydrographic services all serve "not for navigation" derivatives of navigational surveys — a contractual rather than physical statement: the data are often the best that exist, but no one certifies them for your use. **Crowdsourced bathymetry (CSB)** collected under IHO B-12 and archived at the IHO **DCDB** at NCEI supplies single-beam tracks of uncertain draft and tide correction, useful for reconnaissance and change detection; GEBCO ingests it under a distinct TID.

### 55.3.6 Sub-ice: BedMachine and Bedmap3

**BedMachine Greenland** (Morlighem et al. 2017; v5) and **BedMachine Antarctica** (Morlighem et al. 2020; v3) combine radar ice-thickness measurements with mass conservation (ice velocity and surface mass balance constrain thickness between flight lines) into 150 m and 500 m bed grids with per-cell error estimates and source masks; **Bedmap3** (Pritchard et al. 2025) adds 84 aero-geophysical surveys to Bedmap2 at 500 m. Where data are absent the two Antarctic products disagree by hundreds of metres, and both publish uncertainty grids that say so.

<!-- figure: Figure 55.3 — GEBCO_2025 TID grid for a shelf-to-abyss transect, colour-coded by type identifier, with the fraction of directly measured cells annotated and a BlueTopo tile's uncertainty band shown as inset -->

> **Case file.** When the US Navy fast-attack submarine *San Francisco* struck a seamount at speed in January 2005, the chart in use showed more than 1,800 m of water; the seamount was absent because the chart's source soundings were sparse and old, although a later review found discoloured water visible in satellite imagery and a shoaling shown on another chart ([Chapter 56](ch56-case-files.md), §56.1). Today, a GEBCO TID layer for that area would show the surrounding cells as altimetry-predicted. The product did not lie; the absence of measurement was the information, and it was not on the chart.

## 55.4 Spaceborne altimetry as products

Satellite altimeters are sparse profiles, not DEMs, but their point products are the de facto global reference for validating every grid in §55.1 and §55.3, with their own versions, datums, and quirks ([Chapter 52](ch52-ground-truth.md) covers their use as truth).

**ICESat-2** (2018–) carries ATLAS, a 532 nm photon-counting lidar with six beams in three pairs, ~11–17 m footprints, and 0.7 m along-track sampling. **ATL03** gives geolocated photons, **ATL06** land-ice heights on 40 m segments posted every 20 m, **ATL08** terrain and canopy height on 100 m land segments with a photon classification, and **ATL13** inland-water heights. Heights are ellipsoidal (WGS 84/ITRF2014) with geoid values supplied as a field; terrain precision on flat open ground is better than 0.2 m, degrading with slope and canopy, and on steep slopes the 100 m ATL08 segment should be replaced by photon-level fits. **GEDI** (2019–, stowed on the ISS in 2023–2024 and then resumed) is a full-waveform 1064 nm lidar with 25 m footprints between 51.6° N and S: **L2A** ground elevation and relative-height metrics, **L2B** canopy cover and profiles, **L3** gridded 1 km means, **L4A/L4B** biomass. GEDI ground elevation is 1–3 m RMSE in favourable terrain and worse on slopes; filter by quality, sensitivity, and degrade flags. **CryoSat-2** (2010–) SIRAL radar altimetry serves ice sheets, sea ice, and, in SARIn mode, coastal and inland water. **SWOT** (2022–) KaRIn products — pixel clouds (L2_HR_PIXC), RiverSP and LakeSP vectors, and Raster grids — give water-surface elevation and slope for rivers wider than about 100 m and lakes above about 0.06 km²; they are heights of water, not terrain, but they anchor hydro-flattening ([Chapter 34](ch34-water-in-dems.md)). **Sentinel-3** SRAL and **Sentinel-6 Michael Freilich** (2020–) Poseidon-4 add inland-water and coastal altimetry at ~300 m along-track resolution in SAR mode.

## 55.5 Commercial products

The commercial tier buys resolution, currency, or a contract — rarely different physics. **Maxar Precision3D** (formerly Vricon) is a 50 cm DSM/DTM from photogrammetric fusion of the Maxar stereo archive, specified at 3 m LE90/CE90 absolute and 1 m relative; it underlies many defence simulation terrains. **Airbus WorldDEM Neo** (2021–) is a 5 m X-band DSM from continued TanDEM-X acquisitions, specified at better than 1.4 m LE90 absolute vertical, with its parent's penetration behaviour; the 12 m **WorldDEM** and edited **WorldDEM4Ortho** remain available. **Intermap NEXTMap** products (NEXTMap One at 1 m; NEXTMap 5/10) descend from airborne X-band IfSAR flown over the US, Western Europe, and parts of Asia in the 2000s and updated by fusion — the age of the underlying IfSAR is the quantity to check. **Fugro, NV5 Geospatial (formerly Quantum Spatial), Hexagon's HxGN Content Program, Woolpert, and Dewberry** fly and license airborne lidar and imagery, often as the contractors behind national programmes, and sell off-the-shelf tiles; several firms also synthesize 3D surfaces from imagery with ML for simulation. **Elevation-as-a-service** APIs — Google Maps Elevation API, Mapbox Terrain-DEM tiles, AWS Terrain Tiles, OpenTopography's API, open-elevation — return heights from thinly documented composites of the public products above; they are convenient and should never be used for engineering, because source, date, datum, and resampling of a returned value are not stated.

## 55.6 A comparison framework

**DEMIX** — the Digital Elevation Model Intercomparison eXercise of the IEEE GRSS and ISPRS — formalized what careful users had done ad hoc: compare candidate DEMs against high-resolution reference DEMs in many 10 km tiles, on many criteria (elevation, slope, roughness differences), with a randomized complete block design and Friedman tests that separate product effects from terrain effects (Guth et al. 2021; Bielski et al. 2024). For a user who must choose, the framework reduces to the checklist below; each row has a column in [Appendix E](../appendices/appendix-e-public-products-tables.md).

| Dimension | Question to answer | Why it matters |
|---|---|---|
| Surface type | DSM, DTM, or hybrid/edited? What was removed, and how? | A 3 m canopy bias dwarfs most accuracy figures |
| Nominal vs effective resolution | Grid posting vs the smallest feature actually resolved | "30 m" ranges from ~30 m (lidar downsample) to ~100 m (ASTER) in effective terms |
| Acquisition dates | Single epoch or multi-year composite? Per-tile dates available? | Change detection, glaciers, coasts, cities |
| Vertical datum | EGM96, EGM2008, ellipsoid, national geoid, MSL/LAT? | Offsets of up to several metres between products |
| Horizontal datum / realization | WGS 84 (which realization?), ITRF epoch, NAD83 | Sub-metre to ~1 m shifts between frames and epochs |
| Reported accuracy | Metric (RMSE, LE90, MAE), stratified by land cover and slope? | Unstratified global numbers hide where it fails |
| Independent accuracy | Who tested it, against what, where? | Maker's figures are usually optimistic for your site |
| Voids and fills | What fraction? Filled from what? Is there a fill mask? | Filled cells carry the error of the filler |
| Artefacts | Stripes, terraces, penetration, tile seams, spikes | Visible in slope/curvature, invisible in hillshade at full extent |
| Uncertainty layers | Per-cell error map or quality flag? | The only way to weight cells correctly |
| Licence | Public domain, CC BY, CC BY-NC(-SA), custom | Determines whether your deliverable is legal |
| Formats and tiling | GeoTIFF/COG, DGED, NetCDF; tile scheme; nodata; pixel-is-area/point | Half-pixel shifts and nodata misreads |
| Update cadence | Annual releases, versioned? | Reproducibility and errata |

*Table 55.1 — Dimensions of the comparison framework. Each row is a question whose answer must be recorded in the fitness-for-use memo ([Chapter 54](ch54-evaluating-others-data.md)).*

Three rows are the ones most often skipped. **Datum:** SRTM, NASADEM, ASTER, AW3D30, and MERIT are in EGM96; Copernicus, FABDEM, DeltaDTM, and DiluviumDEM in EGM2008; TanDEM-X, ArcticDEM, REMA, and ICESat-2 ellipsoidal. EGM96 and EGM2008 differ by decimetres almost everywhere and by 2–3 m in places, so an unconverted Copernicus-minus-NASADEM difference is mostly geoid-model difference. **Effective resolution:** Purinton & Bookhagen (2021) and Guth & Geoffroy (2021) show the 1″ products differ by a factor of two or more in the spatial frequency at which their spectra fall into noise, so slope, curvature, and drainage derivatives at the nominal 30 m are not comparable across products even where elevations agree. **Licence:** FABDEM, CoastalDEM, and MERIT (CC BY-NC path) cannot enter commercial deliverables without a separate agreement; Copernicus, AW3D30, GEDTM30, DeltaDTM, and the national programmes generally can.

> **Try it.** Compare three 1″ global DSMs against ICESat-2 ATL08 terrain heights for a small area, after bringing all four to the same vertical datum. Expected outcome: a table of mean bias, σ, RMSE, and NMAD per product for open and forested cells, with Copernicus typically showing the smallest spread on open ground and all three biased high under canopy.
>
> ```bash
> # 1. Get the DEMs via OpenTopography's global DEM API (needs a free API key)
> for d in COP30 NASADEM AW3D30; do
>   curl -s "https://portal.opentopography.org/API/globaldem?demtype=$d&south=47.55&north=47.65&west=-122.35&east=-122.20&outputFormat=GTiff&API_Key=$OT_KEY" -o $d.tif
> done
> # 2. Convert everything to EGM2008 orthometric heights on a common grid.
> #    Copernicus is already EGM2008; NASADEM and AW3D30 are EGM96.
> for d in NASADEM AW3D30; do
>   gdalwarp -s_srs "EPSG:4326+5773" -t_srs "EPSG:4326+3855" -r bilinear \
>     -te -122.35 47.55 -122.20 47.65 -tr 0.000277778 0.000277778 $d.tif ${d}_egm08.tif
> done
> gdalwarp -te -122.35 47.55 -122.20 47.65 -tr 0.000277778 0.000277778 COP30.tif COP30_egm08.tif
> ```
>
> ```python
> # 3. Pull ATL08 terrain heights with icepyx or SlideRule, convert h -> H (EGM2008), sample, and summarize.
> import numpy as np, rasterio, pandas as pd
> from sliderule import sliderule, icesat2
> sliderule.init("slideruleearth.io")
> region = sliderule.toregion({"type":"Polygon","coordinates":[[[-122.35,47.55],[-122.20,47.55],
>            [-122.20,47.65],[-122.35,47.65],[-122.35,47.55]]]})
> atl08 = icesat2.atl08p({"poly": region["poly"], "srt": 0, "len": 100, "res": 100})
> # SlideRule's ATL08 (PhoREAL) output gives h_te_median (ellipsoidal); request or compute
> # the EGM2008 undulation N for each point (field names vary by SlideRule version), then H = h - N
> atl08["H"] = atl08["h_te_median"] - atl08["geoid"]
> rows = []
> for name in ["COP30_egm08", "NASADEM_egm08", "AW3D30_egm08"]:
>     with rasterio.open(f"{name}.tif") as src:
>         z = np.array([v[0] for v in src.sample(zip(atl08.geometry.x, atl08.geometry.y))])
>     d = z - atl08["H"].values
>     d = d[np.isfinite(d)]
>     rows.append(dict(product=name, n=len(d), bias=d.mean(), sigma=d.std(),
>                      rmse=np.sqrt((d**2).mean()), nmad=1.4826*np.median(np.abs(d-np.median(d)))))
> print(pd.DataFrame(rows).round(2))
> ```

## 55.7 Fitness by use

The question is never "which DEM is best" but "which DEM is adequate for this decision, here." [Chapter 3](ch03-fitness-for-use.md) built the requirement side; the table below pairs common uses with products that can serve them and products that should be refused.

| Use | What dominates fitness | Use | Avoid |
|---|---|---|---|
| Fluvial/pluvial flood modelling | Bare-earth surface; vertical accuracy; hydro-conditioning ([Chapter 61](ch61-hydrology.md)) | National lidar DTM; FABDEM (non-commercial); GEDTM30; MERIT Hydro at 90 m | Any DSM (Copernicus, SRTM, AW3D30) as terrain; ASTER |
| Coastal sea-level-rise exposure | Vertical accuracy in the 0–10 m band; datum (MSL vs geoid vs ellipsoid); tidal datum conversion | National lidar; DeltaDTM; CoastalDEM (non-commercial); CUDEM topobathy | SRTM/NASADEM unmodified; any product without a tidal-datum link |
| Geomorphometry, landform mapping | Effective resolution; inter-pixel consistency; artefacts in slope/curvature | Lidar; Copernicus GLO-30; TanDEM-X 12 m; ArcticDEM/REMA | ASTER; SRTM 3″; ML-corrected DTMs where terracing matters |
| Aviation obstacle/terrain (eTOD) | Certification; integrity; DSM including obstacles | Certified eTOD datasets per ICAO Annex 15 / DO-276 only | Every product in this chapter unless certified |
| Hydrographic charting, navigation | Qualified surveys with uncertainty; CATZOC | Official charts and S-102 from the HO | GEBCO, SRTM15+, ETOPO, GMRT, EMODnet, BlueTopo, CSB |
| Telecommunications line-of-sight, RF planning | DSM including buildings and trees; currency | AW3D30/AW3D 5 m; Copernicus; Precision3D; WorldDEM Neo; national lidar DSM | DTMs; MERIT; FABDEM |
| Glaciology, mass balance | Time stamp; penetration bias; ellipsoidal heights | ArcticDEM/REMA strips; TanDEM-X with HEM and penetration correction; ICESat-2 ATL06 | Mosaics without dates; C-/X-band without penetration treatment |
| Viewshed, solar, visualization | Modest accuracy; completeness; appearance | Copernicus; AW3D30; national lidar | Nothing is dangerous here, but label the surface type |
| Change detection (decades) | Co-registration; comparable surface types | SRTM/NASADEM (2000) vs Copernicus (2011–2015) vs lidar, after Nuth–Kääb alignment ([Chapter 41](ch41-change-detection.md)) | Comparing DSM to DTM; comparing across geoids without conversion |
| Ocean circulation / tsunami modelling | Shelf depths; coastline; smoothness | GEBCO with TID weighting; regional compilations; CUDEM nearshore | Any single global grid near the coast without local checks |

*Table 55.2 — Fitness by use. "Avoid" means the product cannot meet the use's dominant requirement regardless of how it is processed.*

> **Rule of thumb.** For flood and coastal work, a DEM's surface type matters more than its resolution and its datum matters more than its accuracy statistic. A 30 m bare-earth product in the right datum beats a 2 m DSM in the wrong one. The rule fails only when the terrain is so steep that resolution controls the hydraulics — mountain torrents, urban canyons — where neither 30 m product is adequate anyway.

## 55.8 Known errata and quirks

These are not errors so much as behaviours that surprise users who have not read the handbooks; the list is the one that has cost the most time.

- **SRTM tile edges and EGM96.** 1″ tiles are 3601 × 3601 cells with the edge row and column shared between neighbours (pixel-is-point, origin on the integer degree). Treating them as pixel-is-area shifts everything by half a pixel (15 m); naive mosaicking duplicates a row. The EGM96 conversion used a 15′ interpolated geoid, so re-converting with a full-degree EGM96 leaves decimetre residuals.
- **Copernicus DEM editing.** Water bodies are set to one height per body, rivers forced monotonic, coastlines set to 0 m or a local value, all inherited from the 12 m WorldDEM edit. Lakes therefore look perfect and are not measurements; shorelines may sit tens of metres from the acquisition-date shoreline; some real "implausible structures" (quarries, pits, new dams) were edited away. Read the EDM and WBM masks and cite the release year.
- **AW3D30 fills and stripes.** The MSK layer flags cells filled from SRTM, GDEM, or other sources (with cloud and snow codes) and STK gives stack depth; SRTM-filled cells carry C-band bias and a 2000 epoch inside an "optical 2006–2011" product. Faint along-track stripes from the triplet geometry show in slope maps.
- **ASTER GDEM stacking artefacts.** "Mole runs" (linear ridges and troughs where scene boundaries meet), cloud-top bumps, and pits over dark water survive in v3; down-weight cells with a low NUM count.
- **TanDEM-X penetration and the HEM.** The X-band phase centre sits 2–10 m below the canopy top in forest and metres below the surface on firn; dense cities add layover streaks and multipath spikes. The HEM is a coherence-derived *random* error and excludes these systematic biases — a cell can have HEM = 0.5 m and be 5 m too low.
- **MERIT residuals.** About 1 m of SRTM striping survives the filter in flat terrain, and several metres of tree bias remain in dense tropical forest because the canopy model was coarse.
- **FABDEM terraces and trenches.** The correction switches between land-cover classes, leaving 1–2 m steps that act as spurious drainage barriers, and may over-correct cliffs into negative trenches; v1-2 reduced but did not remove these.
- **GEBCO TID semantics.** The code names the *dominant* source type of a 15″ cell, not the fraction measured — "multibeam" may be one track clipping a corner. Codes 40 and above (indirect) cover most of the ocean; cross-check code 0 (land) against your own coastline.
- **ArcticDEM/REMA.** Heights are WGS 84 ellipsoidal; strips may or may not have their altimetry-derived offset applied (metadata says which); mosaics mix dates; matching blunders of tens of metres persist over featureless snow, water, and shadow; 2 m mosaics show feathering seams in curvature.
- **Nodata and quantization.** SRTM uses −32768, AW3D30 −9999, Copernicus NaN or a large negative value depending on format; SRTM, ASTER, and early AW3D30 store integer metres, which produce 1 m terraces in slope maps of flat terrain that are not in the terrain ([Chapter 54](ch54-evaluating-others-data.md)).

## Then & now

**GTOPO30** (1996) ⟨H⟩ compiled national and military cartography into the first downloadable global DEM, inheriting the errors of the paper maps beneath it. **SRTM** (February 2000) measured the Earth directly in eleven days; its 3″ public release (2003–2005) made quantitative global terrain analysis possible, while the 1″ data stayed restricted outside the United States until 2014–2015. **ASTER GDEM** (2009) extended coverage to 83° at the cost of noise; **TanDEM-X** (2010–2015) delivered the first homogeneous 12 m global DSM, which through Airbus's WorldDEM became the **Copernicus DEM** (2019–2021); **AW3D30** (2016) added an optical DSM. **MERIT** (2017), **CoastalDEM** (2018), **FABDEM** (2022), **DeltaDTM** and **DiluviumDEM** (2023–2024), and **GEDTM30** (2025) then turned machine learning and spaceborne lidar on those DSMs to approximate terrain. Under water, the **GEBCO TID era** (2019–) and **Seabed 2030** moved global bathymetry from a smooth gravity-predicted picture to a product that states per cell whether anyone has been there, and NOAA's **BlueTopo** (2022–) added per-cell uncertainty and source on the US shelf. The user's problem changed from "take what exists" to "choose, and justify the choice" — which is why this book's validation chapters exist.

## Validation & uncertainty

Three questions decide how much of this chapter's accuracy information applies to your site.

**Whose numbers.** Maker-reported accuracies are global aggregates against a chosen reference (ICESat GLAS for SRTM, NASADEM, TanDEM-X; GNSS control for AW3D30; lidar for FABDEM, DeltaDTM, GEDTM30) that exclude the hardest cells by construction. Independent assessments (Hawker et al. 2018, 2019; Uuemaa et al. 2020; Purinton & Bookhagen 2021; Guth & Geoffroy 2021; Bielski et al. 2024) find RMSEs 1.5–3 times the headline once forest, slope, and cities are included, and rank the products in the same order on every continent: Copernicus and derivatives, then AW3D30 and NASADEM, then SRTM v3, then ASTER. Treat the maker's figure as a floor and an independent, stratified figure as the estimate.

**On what terrain.** Vertical error grows with slope through horizontal geolocation error ($\sigma_z \approx \sigma_{xy} \tan\beta$: 10 m horizontal on a 30° slope is 5.8 m apparent vertical), with canopy through penetration, and with building density through layover and smoothing; use the error for *your* land cover and slope class, which the stratified tables in [Appendix E](../appendices/appendix-e-public-products-tables.md) provide.

**In what datum.** An EGM96 product tested against EGM2008 or national-geoid reference shows a smooth "bias" of decimetres to metres that is not DEM error; ellipsoidal TanDEM-X/ArcticDEM heights against orthometric reference show the full geoid undulation and are the most frequent "the DEM is broken" report. Convert first, then test.

> **Uncertainty budget.** A representative budget for using Copernicus GLO-30 as terrain in a mixed-cover temperate catchment (values are typical ranges from the independent assessments cited, 1σ unless stated):
>
> | Component | Magnitude | Note |
> |---|---|---|
> | Measurement noise (open flat ground) | 0.5–1.5 m | HEM gives a per-cell estimate |
> | Absolute bias after EGM2008 conversion | ±0.5 m | Regional; test against ICESat-2 |
> | Slope-induced error at 20° (σ_xy ≈ 3–5 m) | 1–2 m | Grows as tan β |
> | Canopy bias (mixed forest, X-band) | +2 to +8 m | Systematic; not in HEM |
> | Building bias (suburban) | +2 to +5 m | Systematic; not in HEM |
> | Edited/filled cells | unknown; treat as ≥ 5 m | Read EDM/FLM masks |
> | Datum mismatch if EGM96 assumed | up to ±2 m | Avoidable |
> | Epoch (2011–2015 vs today) | site-dependent | Mining, cities, glaciers |
>
> The random components combine in quadrature (≈ 1.5–2.5 m on open slopes); the systematic ones add and dominate in forest and city. A flood model requiring 0.5 m terrain accuracy cannot be served by this product anywhere with canopy or buildings, no matter how it is processed.

**How to test locally.** Before using any product here for a decision: (1) pull ICESat-2 ATL08 (ATL06 on ice) over the area, convert datums, and compute bias, σ, NMAD, and the 95th percentile of absolute error by land cover and slope — a few thousand segments usually exist for any area above 1,000 km²; (2) if any open lidar exists nearby, difference against it after Nuth–Kääb co-registration ([Chapter 41](ch41-change-detection.md)) and note the horizontal shift, typically 0.3–1 pixel for global products; (3) inspect slope and curvature, not the hillshade, for stripes, terraces, seams, and spikes; (4) tabulate the fraction of the area that the mask layers call edited, filled, or low-quality; (5) record all of it in a fitness-for-use memo ([Chapter 54](ch54-evaluating-others-data.md), §54.8). For bathymetric compilations, replace step 1 with the TID or source layer — fraction directly measured, survey vintage, and the distribution of per-cell uncertainty where one exists (BlueTopo, EMODnet quality index, BedMachine); where none exists, assume the compilation's regional error (hundreds of metres in altimetry-predicted deep ocean, tens of metres for sparse chart soundings on shelves).

> **Worked example.** A consultant must decide whether Copernicus GLO-30 or FABDEM is adequate for a 1-in-100-year pluvial flood screening in a 400 km² peri-urban catchment with 30 % tree cover, where the client requires terrain accuracy of 1 m RMSE and the deliverable is commercial. ICESat-2 ATL08 provides 2,840 terrain segments across the catchment. After converting to EGM2008 and removing segments flagged as low quality or on slopes over 15°, the comparison yields, for open ground, Copernicus bias +0.3 m and σ 0.9 m, FABDEM bias +0.1 m and σ 0.9 m; for tree-covered segments, Copernicus bias +4.6 m and σ 3.1 m, FABDEM bias +0.8 m and σ 1.9 m; for built-up segments, Copernicus bias +2.9 m and σ 2.4 m, FABDEM bias +0.4 m and σ 1.6 m. Area-weighted RMSE is $\sqrt{0.5(0.3^2+0.9^2) + 0.3(4.6^2+3.1^2) + 0.2(2.9^2+2.4^2)} \approx 3.4$ m for Copernicus and $\sqrt{0.5(0.1^2+0.9^2) + 0.3(0.8^2+1.9^2) + 0.2(0.4^2+1.6^2)} \approx 1.4$ m for FABDEM. Neither meets 1 m RMSE; FABDEM is close but is CC BY-NC-SA and cannot be used in the commercial deliverable without a Fathom licence. The honest memo recommends either licensing FABDEM/FathomDEM, using GEDTM30 or DeltaDTM if the catchment is coastal (and testing them the same way), or commissioning lidar — and states that a screening done on Copernicus alone will systematically under-predict flood extent under trees and in the suburbs.

## Software

**Open source:** **MICRODEM** (Guth; free, Windows) implements the DEMIX criteria and reads every product here. **xdem** (co-registration, differencing, spatial-statistics uncertainty) and **demcoreg** (co-registration to ICESat/ICESat-2 and other DEMs). **GDAL**/**PROJ** (`gdalwarp` with vertical CRS codes and CDN geoid grids for EGM96/EGM2008/ellipsoid conversion; `gdaldem` for slope and curvature; `gdalinfo` for nodata and AREA_OR_POINT). **SlideRule** and **icepyx** for ICESat-2; **GEDI Subsetter** and **NASA Earthdata** for GEDI. **QGIS** for masks, TIDs, and HEMs; **GMT** for GEBCO, SRTM15+, and ETOPO. **OpenTopography**, **Microsoft Planetary Computer**, and **Google Earth Engine** host most global DEMs as analysis-ready tiles. Caveat: cloud catalogues sometimes re-tile, resample, or reproject silently; verify registration and version against the primary source.

**Free but closed:** vendor viewers and portals (Airbus OneAtlas for WorldDEM previews, Maxar's Precision3D samples, Intermap's viewer) show coverage and allow sample ordering but not independent testing. The NOAA **nowCOAST** viewer serves BlueTopo elevation, uncertainty, and contributor layers via WMTS.

**Commercial:** **Global Mapper**, **ArcGIS Pro**, **ENVI**, **ERDAS IMAGINE**, **CARIS HIPS/BASE Editor**, and **QPS Fledermaus** read and compare the products; none substitutes for a documented independent test against altimetry or lidar.

## Standards & guides

- **Copernicus DEM Product Handbook**, Airbus Defence and Space for ESA, GEO1988-CopernicusDEM-SPE-002, Issue 5.0 (2022), and release-specific "updated tiles" notes — grid, masks (EDM, WBM, FLM, HEM), editing rules, EGM2008 conversion, licence.
- **NASADEM Technical Guide / User Guide**, NASA JPL (2020), and **SRTM User Guide** (SRTM v3, NASA JPL 2015) — processing, void filling, tile registration, EGM96 handling.
- **ASTER GDEM Version 3 User Guide**, NASA/METI (2019) — NUM layer, known anomalies.
- **ALOS World 3D-30m (AW3D30) Product Description**, JAXA EORC, v4.1 (2024) — MSK/STK layers, version history, terms of use.
- **TanDEM-X Ground Segment DEM Products Specification Document**, DLR (TD-GS-PS-0021, issue 3.x) — HEM, consistency masks, accuracy requirements.
- **ArcticDEM and REMA Release Notes and Strip/Mosaic Metadata**, Polar Geospatial Center (v4.1, 2023; v2, 2022) — ellipsoidal heights, registration offsets, mask bands.
- **USGS Lidar Base Specification** (2024 revision) and **3DEP product standards** — QL definitions, DEM derivation, hydro-flattening.
- **GEBCO Cook Book** (IHO B-11) and **GEBCO Grid Type Identifier (TID) definitions** — compilation methods and TID code table.
- **NOAA National Bathymetric Source / BlueTopo Specification** — tile scheme, uncertainty and contributor bands, RAT fields.
- **IHO B-12 Guidance on Crowdsourced Bathymetry**, Ed. 3.0.0 (2023) — CSB collection and metadata.
- **ICESat-2 ATL06/ATL08/ATL13 Algorithm Theoretical Basis Documents** (NASA GSFC) and **GEDI L2A/L2B/L4A ATBDs** (NASA/UMD) — product definitions, quality flags, geoid fields.
- **ICAO Annex 15 / PANS-AIM and RTCA DO-276 / EUROCAE ED-98** — why none of the products above is eTOD.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data**, Edition 2 (2023) — the metrics (NVA/VVA) in which independent tests should be reported.

## Pitfalls

- **Calling Copernicus DEM a DTM** → the handbook says DSM, but the water flattening and editing make it *look* terrain-like → check canopy and building bias against ICESat-2 before any hydraulic use; prefer FABDEM/GEDTM30/lidar for terrain.
- **Using FABDEM, CoastalDEM, or MERIT (CC BY-NC) in a commercial deliverable** → the licence text is one click away and no one clicks → record the licence in the project metadata at download time; obtain a commercial licence or choose CC BY/public-domain alternatives.
- **Mixing EGM96 and EGM2008 (or ellipsoidal) products** → the difference is smooth and invisible in a hillshade → always declare the vertical CRS (EPSG:5773, 3855, or ellipsoidal) on every file and convert with PROJ grids before differencing.
- **Treating SRTM's February 2000 as "current"** → it is the DEM everyone learned on → check what has changed (urban growth, mining, glaciers, river migration) against recent imagery; use Copernicus (2011–2015) or lidar where currency matters.
- **Using GEBCO, SRTM15+, ETOPO, or GMRT for anything navigational or site-specific** → they look continuous and detailed at basin scale → read the TID; in coastal waters most cells are predicted or interpolated, with errors of tens of metres.
- **Using ArcticDEM/REMA strips with unresolved vertical bias** → strips without altimetry registration carry metre-level offsets → read the strip metadata's registration fields; co-register to ICESat-2 yourself before differencing.
- **Believing "30 m" is comparable across products** → the posting is the same, the effective resolution differs by 2–3× → compute slope/curvature or spectra and compare feature detail; use DEMIX-style criteria rather than elevation RMSE alone.
- **Ignoring mask and quality layers** → they are separate files and often not downloaded → treat EDM/WBM/FLM/HEM, MSK/STK, NUM, TID, and contributor bands as part of the product; tabulate them for your area.
- **Reading elevation API values as data** → the API hides source, date, datum, and interpolation → use them for sketches only; for anything that matters, download the source product.
- **Half-pixel registration errors when mosaicking SRTM-style tiles with pixel-is-area products** → shared edge rows and AREA_OR_POINT metadata are easy to miss → check `gdalinfo` for AREA_OR_POINT and tile origins; see [Chapter 10](ch10-projections-and-resampling.md).
- **Assuming the uncertainty layer is validated** → HEM, GEDTM30's spread, and BlueTopo's uncertainty each measure different things → read what the layer is (coherence-derived random error, model disagreement, propagated survey TVU) and test it against independent data where possible.
- **Trusting a new ML-corrected DTM because its paper reports better numbers** → the test set is where training data existed → look for terraces at land-cover boundaries, trenches at cliffs, and smoothing of small features before adopting it.

## Key takeaways

- No product is best everywhere; choose by surface type, land cover, slope, datum, date, effective resolution, and licence — and write down why.
- Among free 1″ global DSMs, Copernicus GLO-30 is the current default; among terrain approximations, FABDEM (non-commercial), GEDTM30, and DeltaDTM lead, with national lidar superseding all of them wherever it exists.
- Vertical datum is the first thing to check: EGM96 (SRTM, NASADEM, ASTER, AW3D30, MERIT), EGM2008 (Copernicus, FABDEM, DeltaDTM), ellipsoid (TanDEM-X, ArcticDEM, REMA, ICESat-2).
- Maker-reported accuracies are floors; independent, land-cover-stratified assessments are the numbers to plan with.
- The mask, quality, TID, and uncertainty layers are part of the product; a cell's provenance matters as much as its value.
- Global bathymetric grids tell you where measurements exist; treat every other cell as a hypothesis with errors of tens to hundreds of metres, and never use them for navigation.
- Spaceborne lidar (ICESat-2, GEDI) makes a local independent test of any product cheap; run it before trusting anything, and report bias, σ, NMAD, and the 95th percentile by land cover.
- Licences are technical constraints: CC BY-NC products cannot go into commercial deliverables; record the licence with the data.

## References

- Abrams, M., Crippen, R., & Fujisada, H. (2020). ASTER Global Digital Elevation Model (GDEM) and ASTER Global Water Body Dataset (ASTWBD). *Remote Sensing*, 12(7):1156.
- Airbus Defence and Space (2022). *Copernicus DEM — Copernicus Digital Elevation Model Product Handbook*, GEO1988-CopernicusDEM-SPE-002, Issue 5.0. ESA.
- Amante, C., & Eakins, B. W. (2009). *ETOPO1 1 Arc-Minute Global Relief Model: Procedures, Data Sources and Analysis*. NOAA Technical Memorandum NESDIS NGDC-24.
- Bielski, C., López-Vázquez, C., Grohmann, C. H., Guth, P. L., Hawker, L., Gesch, D., Trevisani, S., Herrera-Cruz, V., Riazanoff, S., Corseaux, A., Reuter, H. I., & Strobl, P. (2024). Novel approach for ranking DEMs: Copernicus DEM improves one arc second open global topography. *IEEE Transactions on Geoscience and Remote Sensing*, 62:4503922.
- Crippen, R., Buckley, S., Agram, P., Belz, E., Gurrola, E., Hensley, S., Kobrick, M., Lavalle, M., Martin, J., Neumann, M., Nguyen, Q., Rosen, P., Shimada, J., Simard, M., & Tung, W. (2016). NASADEM global elevation model: methods and progress. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, XLI-B4:125–128.
- Danielson, J. J., & Gesch, D. B. (2011). *Global Multi-resolution Terrain Elevation Data 2010 (GMTED2010)*. USGS Open-File Report 2011-1073.
- Dorschel, B., Hehemann, L., Viquerat, S., et al. (2022). The International Bathymetric Chart of the Southern Ocean Version 2. *Scientific Data*, 9:275.
- Dusseau, D., Zobel, Z., & Schuldt, D. (2023). DiluviumDEM: Enhanced accuracy in global coastal digital elevation models. *Remote Sensing of Environment*, 298:113812.
- Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., Kobrick, M., Paller, M., Rodriguez, E., Roth, L., Seal, D., Shaffer, S., Shimada, J., Umland, J., Werner, M., Oskin, M., Burbank, D., & Alsdorf, D. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics*, 45:RG2004.
- GEBCO Compilation Group (2024). *GEBCO 2024 Grid*. doi:10.5285/1c44ce99-0a0d-5f4f-e063-7086abc0ea0f.
- GEBCO Compilation Group (2025). *GEBCO 2025 Grid*. NERC EDS British Oceanographic Data Centre. (verify)
- Guth, P. L., & Geoffroy, T. M. (2021). LiDAR point cloud and ICESat-2 evaluation of 1 second global digital elevation models: Copernicus wins. *Transactions in GIS*, 25(5):2245–2261.
- Guth, P. L., Van Niekerk, A., Grohmann, C. H., Muller, J.-P., Hawker, L., Florinsky, I. V., Gesch, D., Reuter, H. I., Herrera-Cruz, V., Riazanoff, S., López-Vázquez, C., Carabajal, C. C., Albinet, C., & Strobl, P. (2021). Digital Elevation Models: terminology and definitions. *Remote Sensing*, 13(18):3581.
- Hawker, L., Bates, P., Neal, J., & Rougier, J. (2018). Perspectives on digital elevation model (DEM) simulation for flood modeling in the absence of a high-accuracy open access global DEM. *Frontiers in Earth Science*, 6:233.
- Hawker, L., Neal, J., & Bates, P. (2019). Accuracy assessment of the TanDEM-X 90 Digital Elevation Model for selected floodplain sites. *Remote Sensing of Environment*, 232:111319.
- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., & Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters*, 17(2):024016.
- Ho, Y.-F., Grohmann, C. H., Lindsay, J., Reuter, H. I., Parente, L., Witjes, M., & Hengl, T. (2025). Global ensemble digital terrain modeling and parametrization at 30 m resolution (GEDTM30): a data fusion approach based on ICESat-2, GEDI and multisource data. *PeerJ*, 13:e19673.
- Howat, I. M., Porter, C., Smith, B. E., Noh, M.-J., & Morin, P. (2019). The Reference Elevation Model of Antarctica. *The Cryosphere*, 13:665–674.
- Jakobsson, M., Mayer, L. A., Bringensparr, C., et al. (2020). The International Bathymetric Chart of the Arctic Ocean Version 4.0. *Scientific Data*, 7:176.
- Jakobsson, M., Mayer, L. A., et al. (2024). The International Bathymetric Chart of the Arctic Ocean Version 5.0. *Scientific Data*, 11. (verify article number)
- JAXA EORC (2024). *ALOS Global Digital Surface Model "ALOS World 3D – 30m (AW3D30)" Product Description*, version 4.1.
- Kulp, S. A., & Strauss, B. H. (2018). CoastalDEM: A global coastal digital elevation model improved from SRTM using a neural network. *Remote Sensing of Environment*, 206:231–239.
- Kulp, S. A., & Strauss, B. H. (2019). New elevation data triple estimates of global vulnerability to sea-level rise and coastal flooding. *Nature Communications*, 10:4844.
- Morlighem, M., Williams, C. N., Rignot, E., et al. (2017). BedMachine v3: Complete bed topography and ocean bathymetry mapping of Greenland from multibeam echo sounding combined with mass conservation. *Geophysical Research Letters*, 44(21):11051–11061.
- Morlighem, M., Rignot, E., Binder, T., et al. (2020). Deep glacial troughs and stabilizing ridges unveiled beneath the margins of the Antarctic ice sheet. *Nature Geoscience*, 13:132–137.
- NOAA National Centers for Environmental Information (2022). *ETOPO 2022 15 Arc-Second Global Relief Model*. NOAA NCEI.
- Porter, C., Morin, P., Howat, I., et al. (2018). *ArcticDEM*. Harvard Dataverse, V1 (and v4.1 release notes, Polar Geospatial Center, 2023).
- Pritchard, H. D., Fretwell, P. T., Fremand, A. C., et al. (2025). Bedmap3 updated ice bed, surface and thickness gridded datasets for Antarctica. *Scientific Data*, 12:414.
- Pronk, M., Hooijer, A., Eilander, D., Haag, A., de Jong, T., Vousdoukas, M., Vernimmen, R., Ledoux, H., & Eleveld, M. (2024). DeltaDTM: A global coastal digital terrain model. *Scientific Data*, 11:273.
- Purinton, B., & Bookhagen, B. (2021). Beyond vertical point accuracy: assessing inter-pixel consistency in 30 m global DEMs for the arid Central Andes. *Frontiers in Earth Science*, 9:758606.
- Rizzoli, P., Martone, M., Gonzalez, C., Wecklich, C., Borla Tridon, D., Bräutigam, B., Bachmann, M., Schulze, D., Fritz, T., Huber, M., Wessel, B., Krieger, G., Zink, M., & Moreira, A. (2017). Generation and performance assessment of the global TanDEM-X digital elevation model. *ISPRS Journal of Photogrammetry and Remote Sensing*, 132:119–139.
- Rodríguez, E., Morris, C. S., & Belz, J. E. (2006). A global assessment of the SRTM performance. *Photogrammetric Engineering & Remote Sensing*, 72(3):249–260.
- Ryan, W. B. F., Carbotte, S. M., Coplan, J. O., et al. (2009). Global Multi-Resolution Topography synthesis. *Geochemistry, Geophysics, Geosystems*, 10:Q03014.
- Sugarbaker, L. J., Constance, E. W., Heidemann, H. K., Jason, A. L., Lukas, V., Saghy, D. L., & Stoker, J. M. (2014). *The 3D Elevation Program Initiative — A Call for Action*. USGS Circular 1399.
- Tadono, T., Ishida, H., Oda, F., Naito, S., Minakawa, K., & Iwamoto, H. (2014). Precise global DEM generation by ALOS PRISM. *ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, II-4:71–76.
- Takaku, J., Tadono, T., Doutsu, M., Ohgushi, F., & Kai, H. (2020). Updates of "AW3D30" ALOS global digital surface model with other open access datasets. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, XLIII-B4-2020:183–189.
- Tozer, B., Sandwell, D. T., Smith, W. H. F., Olson, C., Beale, J. R., & Wessel, P. (2019). Global bathymetry and topography at 15 arc sec: SRTM15+. *Earth and Space Science*, 6(10):1847–1864.
- Uuemaa, E., Ahi, S., Montibeller, B., Muru, M., & Kmoch, A. (2020). Vertical accuracy of freely available global digital elevation models (ASTER, AW3D30, MERIT, TanDEM-X, SRTM, and NASADEM). *Remote Sensing*, 12(21):3482.
- Yamazaki, D., Ikeshima, D., Tawatari, R., Yamaguchi, T., O'Loughlin, F., Neal, J. C., Sampson, C. C., Kanae, S., & Bates, P. D. (2017). A high-accuracy map of global terrain elevations. *Geophysical Research Letters*, 44(11):5844–5853.
- Yamazaki, D., Ikeshima, D., Sosa, J., Bates, P. D., Allen, G. H., & Pavelsky, T. M. (2019). MERIT Hydro: A high-resolution global hydrography map based on latest topography dataset. *Water Resources Research*, 55(6):5053–5073.
- Zink, M., Moreira, A., Hajnsek, I., Rizzoli, P., Bachmann, M., Kahle, R., Fritz, T., Huber, M., Krieger, G., Lachaise, M., Martone, M., Maurer, E., & Wessel, B. (2021). TanDEM-X: 10 years of formation flying bistatic SAR interferometry. *IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing*, 14:3546–3565.

# Chapter 51 — Finding the right data: catalogs, STAC, and search

> **Part X — Representing, storing, finding, and keeping elevation data.** This chapter closes Part X by turning the metadata of [Chapter 49](ch49-metadata.md) and the archives of [Chapter 50](ch50-archiving-and-provenance.md) into a practical question: for a given place, time, and purpose, what elevation data exist, how good are they, and how do you get them?

**In this chapter.** More elevation data exist for most places than any one person knows about, and the best dataset for your purpose is rarely the first one a search engine returns. This chapter gives you the discovery questions to ask before searching—where, when, what surface, what resolution and accuracy, what datum, what licence, what format, what cost—and a tour of where the answers live: USGS 3DEP and The National Map, NOAA Digital Coast and NCEI, OpenTopography, NASA Earthdata, the Copernicus Data Space, JAXA and DLR, the national mapping portals of a dozen countries, the marine compilations (EMODnet, GEBCO, DCDB, GMRT), and the cloud catalogs (AWS Open Data, Planetary Computer, Earth Engine, Source Cooperative). You will learn how STAC Items, Collections, and the STAC API work, run a search with pystac-client, and understand why quality-first search—by checkpoint accuracy, density, or datum—is still mostly impossible and what would fix it. The chapter covers crowd and commercial sources and the hidden provenance of elevation APIs, cloud-native access patterns (COG, COPC, Zarr range reads), how to evaluate a dataset before downloading it, and what to do when nothing fits.

## 51.1 The discovery questions

Searching for elevation data without a requirement is how people end up with a 30 m DSM for a drainage design. [Chapter 3](ch03-fitness-for-use.md) derives requirements from use; this section turns them into search terms. Write the answers down before opening a browser, because every portal will tempt you with the highest resolution it has.

**Where.** The area of interest as a polygon, not a name, with a buffer for edge effects (at least a few hundred metres for hydrology, more for viewsheds). Note the CRS you will work in; portals index by WGS 84 longitude–latitude but deliver in national grids.

**When.** The epoch you need, and the tolerance. A pre-event surface for change detection must predate the event; a baseline for an engineering design should postdate the last construction; a vegetation study needs leaf-on or leaf-off. "Most recent" is not always right—a 2012 lidar may be better than a 2023 photogrammetric DSM for a bare-earth question ([Chapter 37](ch37-time-scales-of-change.md)).

**What surface.** DTM, DSM, bathymetric surface, or topobathymetric; and the inclusions and exclusions that matter to you (bridges removed? water flattened? buildings present?). This single question eliminates most candidates.

**What resolution and accuracy.** State the required effective resolution and vertical accuracy as numbers with a statistic (for example, "features of 5 m resolved; RMSE$_z$ ≤ 0.25 m on open ground; ≤ 0.5 m under canopy"), derived from the use ([Chapter 3](ch03-fitness-for-use.md), [Chapter 44](ch44-resolution-and-sampling.md)). Resolution finer than you need costs storage and processing time and buys nothing.

**What datum.** The vertical datum and realization your other data use, so that you can estimate the conversion effort and its uncertainty ([Chapter 9](ch09-vertical-datums.md)). A 10 cm product in a tidal datum you cannot convert is a 1 m product.

**What licence.** Whether you need commercial use, redistribution, or derivative publication; whether attribution and share-alike are acceptable; whether the data may leave a jurisdiction ([Chapter 68](ch68-legal-issues.md)).

**What format and access pattern.** Whether you can work from cloud-native files by range request, need bulk download, or need an API; whether your tools read COPC, BAG, Zarr.

**What cost.** Including egress, API fees, licence fees, and your own time converting datums and formats.

The result is a specification against which each candidate is scored—and the score is use-dependent. For a flood model the datum and hydro-conditioning dominate; for a viewshed the DSM/DTM distinction and currency dominate; for a landslide inventory the effective resolution and epoch dominate. "Best" without "for what" is not a property a dataset can have.

> **Definitions that bite.** *Available.* On portals the word covers at least four states: *listed* (a record exists), *downloadable* (files can be obtained, perhaps after registration or payment), *licensed for your use*, and *fit for your purpose*. The first three are catalog facts; the fourth is yours to establish. A dataset that is "available" on a national portal under a non-commercial licence is not available to a consulting engineer.

## 51.2 Catalogs and portals

No single catalog covers elevation data. The practical search order is: the national mapping and hydrographic agencies for the territory; the thematic aggregators (OpenTopography, Digital Coast, EMODnet); the global products ([Chapter 55](ch55-public-products.md)); then the cloud catalogs, which increasingly mirror the first three with better access. Table 51.1 lists the portals a practitioner should know. Details change yearly; the descriptions are current as of this writing and should be checked.

| Portal | Operator | Holds | Access notes |
|---|---|---|---|
| The National Map / 3DEP downloader, LidarExplorer | USGS | 3DEP lidar point clouds (LAZ), 1 m and 1/3″ seamless DEMs, project metadata and reports | TNM API; 3DEP lidar also on AWS as EPT/COPC and on Planetary Computer; project boundaries with dates |
| Digital Coast Data Access Viewer | NOAA OCM | Coastal topographic and topobathymetric lidar, imagery, land cover | Custom extraction with datum and format options; bulk via S3 |
| NCEI Bathymetric Data Viewer; Multibeam and Trackline viewers | NOAA NCEI | Multibeam and single-beam surveys, NOS hydrographic surveys (BAG, smooth sheets), DEMs (CUDEM, CoNED) | Raw multibeam downloadable per cruise; DEM tiles via THREDDS/HTTPS |
| National Bathymetric Source / BlueTopo | NOAA OCS | Compiled US bathymetry tiles with elevation, uncertainty, and contributor layers | AWS public bucket; GeoTIFF with VRT; supersession documented |
| OpenTopography | NSF/SDSC | Academic and agency lidar (point clouds, DEMs), global DEM subsetting (SRTM, Copernicus, ALOS, NASADEM, GEBCO) | REST API with key; on-demand DEM generation; DOIs per dataset |
| Earthdata Search / CMR | NASA | SRTM, NASADEM, ASTER GDEM, ICESat-2 (ATL03/06/08), GEDI, IceBridge, ArcticDEM/REMA mirrors | Earthdata login; CMR API; lineage from the GCMD ⟨H⟩ |
| Copernicus Data Space Ecosystem | ESA/EC | Copernicus DEM (GLO-30, GLO-90; EEA-10 for Europe), Sentinel-1/2 | STAC API; also on AWS Open Data |
| ALOS World 3D (AW3D30) | JAXA | 30 m DSM from PRISM stereo | Registration; free; commercial 5 m/2.5 m versions via partners |
| TanDEM-X DEM and EDEM | DLR | 12 m (science proposal), 30 m and 90 m editions | 90 m free; 30 m Edited DEM free for scientific use after registration (EOC Geoservice licence); 12 m by proposal |
| UK: Environment Agency LiDAR via DEFRA Data Services Platform | EA/DEFRA | National 1 m DTM/DSM composites, time series, point clouds | Open Government Licence |
| Netherlands: AHN | Rijkswaterstaat/waterschappen | AHN1–AHN5 point clouds and 0.5 m grids | CC0; also on cloud mirrors |
| Switzerland: swissALTI3D, swissSURFACE3D | swisstopo | 0.5 m DTM, point clouds | Free since 2021 |
| New Zealand: LINZ Data Service | LINZ | Regional lidar DEM/DSM, point clouds, bathymetry | CC BY 4.0; API and bulk |
| Australia: ELVIS | Geoscience Australia / states | National and state lidar, DEMs | Free; state licences vary |
| Canada: HRDEM / Open Maps | NRCan | 1–2 m lidar DEMs, CDEM, bathymetry via CHS NONNA | Open Government Licence – Canada |
| Spain: PNOA-LiDAR via CNIG | IGN Spain | National lidar coverages, MDT05/MDT02 | CC BY 4.0 |
| France: LiDAR HD, RGE ALTI | IGN France | National 10 pts/m² lidar (in progress), 1 m DTM | Licence Ouverte |
| Denmark: DHM via Dataforsyningen | SDFI | 0.4 m DTM/DSM, point clouds | Open |
| Finland: NLS laser scanning, 2 m DEM | NLS Finland | National lidar (5 pts/m² programme), 2 m DEM | CC BY 4.0 |
| Norway: Høydedata | Kartverket | National detailed elevation model, point clouds | Open (NLOD) |
| Japan: GSI Maps / Basic Map Information | GSI | 5 m and 10 m DEMs, lidar in places | Terms of use require attribution |
| EMODnet Bathymetry | European Commission | European DTM (~115 m), source references and CDI metadata | Open; WMS/WCS and tiles |
| GEBCO and IHO DCDB | GEBCO/IHO/NCEI | Global grid with TID; archived soundings and CSB | Open; grid, TID, and source identifier grids |
| GMRT | Lamont-Doherty | Multi-resolution multibeam synthesis with global base | Open; web services |
| AWS Open Data Registry | Amazon | Mirrors: 3DEP, Copernicus DEM, BlueTopo, ArcticDEM/REMA, NASADEM, others | Requester or provider pays; STAC for many |
| Microsoft Planetary Computer | Microsoft | 3DEP lidar (COPC) and DEMs, Copernicus DEM, NASADEM, ALOS, others | STAC API; free tier with tokens |
| Google Earth Engine Data Catalog ⟨H⟩ | Google | SRTM, NASADEM, Copernicus DEM, ALOS, 3DEP 1 m and 10 m, GEBCO, ETOPO, many national DEMs | Earth Engine API; free for non-commercial |
| Source Cooperative | Radiant Earth | Community-published cloud-native datasets | STAC and HTTP |

*Table 51.1 — Elevation data portals a practitioner should know (details subject to change).*

Three observations apply across the table. First, **the agency portal and the cloud mirror are not always the same data**: mirrors lag releases, sometimes omit companion layers, and occasionally re-tile or re-compress. Record which you used ([Chapter 50](ch50-archiving-and-provenance.md)). Second, **project boundaries matter more than seamless products for quality**: USGS 3DEP's seamless 1 m DEM is stitched from projects with different years, sensors, and accuracies, and the project footprints with their dates—available from the 3DEP work-unit index—are the layer that tells you what you actually have at a point ([Chapter 48](ch48-compositing.md)). Third, **the marine portals index by survey, not by area**, so finding bathymetry for a location means finding the surveys whose footprints cover it and then judging each; GEBCO's source-identifier grid and NBS's contributor layer are the shortcuts.

<!-- figure: Figure 51.1 — A single coastal study area overlaid with the footprints returned by six portals (3DEP projects with years, Digital Coast lidar, NOS hydrographic surveys, BlueTopo tiles, Copernicus DEM, GEBCO TID), illustrating that "what exists here" is a dozen datasets of different epochs and surface types rather than one. -->

## 51.3 STAC and the catalog APIs

### 51.3.1 Items, Collections, Catalogs

[Chapter 49](ch49-metadata.md) introduced STAC as a metadata encoding; here it is a search mechanism. A **static catalog** is a tree of JSON files on a web server or object store—a root Catalog linking Collections linking Items—that a crawler can walk without a database. A **dynamic catalog** exposes the same objects through the **STAC API**, which adds a `/search` endpoint accepting a bounding box or GeoJSON intersects geometry, a datetime or interval, a list of collections, and—with the *filter* extension—CQL2 expressions over Item properties (`proj:code = 'EPSG:6350' AND pc:density > 4`). Results are paged GeoJSON FeatureCollections of Items, each pointing at its assets with media types and roles, so a client can go from a query to byte-range reads of a COG or COPC file without a download step. The *sort*, *fields*, and *aggregation* extensions make it possible to rank by date, return only the properties you need, and count Items per year or per CRS.

The lineage of this design runs through NASA's **Global Change Master Directory** (GCMD, from the early 1990s ⟨H⟩), whose Directory Interchange Format records and controlled keyword vocabularies were the first widely used machine-readable Earth-science dataset catalog, and its successor the **Common Metadata Repository** (CMR), which indexes every NASA DAAC granule with a spatial–temporal search API that STAC API deliberately resembles; CMR now also serves STAC. The OGC **Catalogue Service for the Web** (CSW, 2.0.2, 2007) was the standards-track equivalent for ISO records and is still what INSPIRE discovery services and many national geoportals speak; **OGC API – Records** is its web-API replacement and shares its query patterns with STAC API, while **OGC API – Features** is the general feature-access API from which STAC API borrows its structure. In practice, for elevation data in 2025: use STAC API where a provider offers it (Planetary Computer, Copernicus Data Space, Earth Search on AWS, many national agencies), CMR for NASA products, and CSW or vendor APIs for the rest.

> **Try it.** Find 3DEP lidar point-cloud Items and the 3DEP seamless DEM for an area of interest on the Planetary Computer STAC API, then open one asset by range request without downloading it.
>
> ```python
> import pystac_client, planetary_computer as pc, rasterio, json
> cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",
>                                 modifier=pc.sign_inplace)
> aoi = {"type": "Polygon", "coordinates": [[[-122.52,37.70],[-122.35,37.70],
>         [-122.35,37.83],[-122.52,37.83],[-122.52,37.70]]]}
> # Point clouds: one Item per 3DEP project tile; properties carry the pointcloud extension.
> pcs = cat.search(collections=["3dep-lidar-copc"], intersects=aoi,
>                  datetime="2015-01-01/2024-12-31").item_collection()
> for it in pcs[:5]:
>     p = it.properties
>     print(it.id, p.get("start_datetime","")[:10], p.get("3dep:usgs_id"),
>           p.get("pc:count"), p.get("pc:density"), p.get("proj:epsg"))
> # Seamless DEM (1 m where available): a raster Item per tile.
> dems = cat.search(collections=["3dep-seamless"], intersects=aoi,
>                   query={"gsd": {"eq": 1}}).item_collection()
> href = dems[0].assets["data"].href
> with rasterio.open(href) as src:          # HTTP range reads; only the needed blocks move
>     print(src.crs, src.res, src.nodata, src.tags().get("TIFFTAG_DATETIME"))
>     window = src.window(*src.bounds)      # replace with your AOI bounds in src.crs
>     print(src.read(1, window=window, out_shape=(1, 256, 256)).mean())
> ```
>
> Expected outcome: a list of COPC Items with their project identifiers, acquisition dates, point counts, densities, and EPSG codes—note that neighbouring Items can come from different projects and years—and a 1 m DEM tile opened over HTTP from which a 256 × 256 overview window is read in under a second. The `3dep:usgs_id` is the key for retrieving the project's reports and checkpoint tables from USGS; the Item itself carries no accuracy field.

### 51.3.2 What STAC search cannot (yet) answer

The example exposes the gap: you can filter by place, time, CRS, density, and format, but not by *vertical accuracy*, *surface type*, or *vertical datum realization*, because there is no agreed extension for them and most Items do not carry them. The pointcloud extension gives density, which is a proxy for effective resolution; the projection extension can carry a compound CRS with a vertical component, but most providers populate only the horizontal; and the acquisition date is frequently the processing date. The practical consequence is a two-stage search: STAC to enumerate candidates, then per-project metadata forensics ([Chapter 49](ch49-metadata.md), [Chapter 54](ch54-evaluating-others-data.md)) to rank them.

## 51.4 Search by quality

A quality-first catalog would let you ask: "point clouds within this polygon, acquired leaf-off since 2018, ground density ≥ 2 pts/m², NVA ≤ 10 cm RMSE$_z$ tested with ≥ 30 checkpoints, NAVD88 via GEOID18 or convertible, hydro-flattened, CC0." Every element of that query exists in some project's report; almost none is queryable anywhere. Three developments point toward fixing this.

**Structured accuracy metadata.** A STAC extension for positional accuracy—statistic, value, confidence level, method, checkpoint count, strata, reference—would be small to specify and would be populated automatically by any producer following the LBS or ASPRS reporting language. ISO 19157's `DQ_AbsoluteExternalPositionalAccuracy` already carries these fields in national catalogs; the missing step is exposing them through the API filters. Until then, a project-local convention (as in the [Chapter 49](ch49-metadata.md) example) at least makes the facts searchable within one catalog.

**Tile-level rankings.** The **DEMIX** initiative (Guth et al., 2021; Bielski et al., 2024) ranks global DEMs against reference lidar on a standard 10 km tile grid using a suite of criteria (elevation, slope, roughness differences; LE90; artefact scores), producing per-tile scores that say which of Copernicus DEM, ALOS AW3D30, NASADEM, SRTM, ASTER GDEM, or FABDEM is best *here*, and by how much. Published as a per-tile table, this is a discovery aid: before choosing a global DEM for a region, read its DEMIX ranking. The same approach could rank national lidar projects where reference data overlap, and the per-tile output format is exactly what a catalog could serve as a quality property.

**Companion-layer search.** Products that publish uncertainty, source, and date rasters ([Chapter 48](ch48-compositing.md)) make quality queries possible after the fact: fetch the uncertainty layer over the AOI by range read and compute its statistics before fetching the elevations. NBS/BlueTopo, GEBCO (TID), Copernicus DEM (height error mask), and TanDEM-X (HEM) support this today; most national lidar DEMs do not.

> **Rule of thumb.** Until quality fields are searchable, rank candidate datasets by (1) surface type match, (2) epoch match, (3) source density or stated resolution relative to the requirement, (4) existence of a checkpoint table or uncertainty layer, (5) datum convertibility, (6) licence—in that order, and never by nominal resolution alone. The order changes for navigation products, where (4) and the shoal-bias convention come first.

## 51.5 Crowd and commercial sources

**OpenStreetMap** holds no elevation surface, but it holds elevation-adjacent vectors—`ele` tags on peaks and passes, building footprints and heights, road and rail centrelines, waterways, coastlines, embankments and cliffs—that serve as breaklines, masks, and sanity checks for DEM work ([Chapter 59](ch59-vector-data.md)); its `ele` values have unknown provenance and should be treated as approximate. **Crowdsourced bathymetry** through the IHO DCDB (CSB) is growing rapidly: depth-and-position logs from fishing vessels, ferries, and recreational craft, contributed via trusted nodes, with transducer offsets and tide corrections often unknown. The DCDB serves CSB with its contribution metadata; it is valuable for detecting change and filling gaps, and unreliable at the metre level without processing ([Chapter 20](ch20-sonar.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)).

**Commercial DEMs** fill gaps in coverage, currency, and resolution. **Maxar Precision3D** (formerly Vricon) offers 0.5 m DSM/DTM from satellite stereo at global scale with stated accuracies; **Airbus WorldDEM** (12 m, from TanDEM-X) and **WorldDEM Neo** (5 m) provide global InSAR DSMs with the TanDEM-X height-error mask; **Intermap NEXTMap** provides airborne IFSAR DSM/DTM at 5 m over large regions with higher-resolution editions; **Fugro**, **NV5 Geospatial**, and other survey firms sell lidar and bathymetry from their own programmes or on commission; **Hexagon's HxGN Content Program** sells wide-area aerial imagery with derived DSMs. Commercial products usually come with accuracy statements and sample data; insist on the checkpoint methodology, the surface definition (many "DTMs" from stereo are edited DSMs), the vertical datum, and the licence's redistribution terms before purchase, and run your own check over a sample tile ([Chapter 54](ch54-evaluating-others-data.md)).

**Elevation APIs** return a height for a coordinate. **Google Maps Platform's Elevation API**, **Mapbox Terrain** services, **Open-Elevation**, **Open Topo Data**, and national equivalents (for example the USGS Elevation Point Query Service, which does state that it samples the 3DEP seamless DEM) differ in one crucial respect: whether they tell you which DEM answered. Most commercial APIs do not disclose the source DEM, its resolution, its epoch, or its vertical datum beyond "metres above sea level," and may blend sources that change without notice. For a casual lookup this does not matter; for anything that will be measured, modelled, or litigated it disqualifies the API, because the result cannot be reproduced or assigned an uncertainty. Open-source services (Open Topo Data, Open-Elevation) at least name their datasets—typically SRTM, ASTER, or national DEMs you could have used directly—which raises the question of why not use the dataset itself.

> **Case file.** Several published studies and many engineering memos have cited "Google Earth elevations" as ground truth or as the DEM of record. Google Earth's terrain layer is a composite of undisclosed sources at undisclosed resolutions that is updated without versioning; studies that compared it to GNSS checkpoints have found vertical errors ranging from a few metres in flat open terrain to tens of metres in mountains and built-up areas, consistent with a blend of SRTM-class data and higher-resolution patches. The lesson is not that the layer is bad for visualization—it is excellent—but that an elevation whose provenance cannot be stated cannot carry an uncertainty, and an elevation without an uncertainty cannot be used as a measurement.

<!-- figure: Figure 51.2 — The same transect queried through three elevation APIs and against a 3DEP lidar DTM: the APIs disagree with each other by metres where the source DEM evidently changes, and none reports which product answered. -->

## 51.6 Access patterns

How you fetch data determines what you can afford to look at. Four patterns coexist.

**Bulk download** of tiles or whole projects (HTTPS, FTP's successor; S3 sync; `aria2c` for parallel segmented downloads) is right when you need everything, when you will process many times, or when you must archive your own copy. Its costs are storage and the latency before you learn whether the data are any good.

**Cloud-native range reads** exploit formats designed for partial access: **COG** (internal tiling and overviews, so a viewer reads only the tiles and zoom level it needs), **COPC** (an octree of LAZ chunks in one file, so a reader fetches only the spatial and level-of-detail subset), **EPT** (the same idea as a directory tree), and **Zarr** (chunked arrays with separate metadata). GDAL's `/vsicurl/` and `/vsis3/`, rasterio, PDAL's COPC and EPT readers, `odc-stac` and `stackstac` (which assemble STAC Items into lazy xarray data cubes), and QGIS all read these directly. The pattern makes "look before you download" free and makes continental-scale analyses feasible without a continental download ([Chapter 47](ch47-file-formats.md)).

**Tiles and services** (XYZ terrain tiles, WMS/WMTS hillshades, WCS coverage requests, OGC API – Coverages) serve visualization and lightweight analysis; be careful that terrain tiles (Mapbox Terrain-RGB, Cesium quantized-mesh, and similar) are encoded with quantization steps—0.1 m for Terrain-RGB—and may be resampled and blended from undisclosed sources.

**APIs** (OpenTopography's global DEM endpoint, point-query services, on-demand processing) trade control for convenience; record the request parameters and the response headers, which often include a version.

Practicalities: most portals require **authentication** (Earthdata login; API keys for OpenTopography, Planetary Computer tokens; registration for JAXA and some national portals), and cloud mirrors may be **requester-pays**, so budget **egress**—typically on the order of US$0.05–0.10 per GB out of major clouds, which for a 2 TB lidar project is real money and an argument for computing where the data live. Keep a **local manifest** of everything you fetch: source URL or STAC Item URL, Collection and Item identifiers, dataset version, file checksums, fetch date, and the licence text—a small CSV or a saved STAC ItemCollection JSON. When a result is questioned two years later, the manifest is what lets you say exactly which bytes you used ([Chapter 50](ch50-archiving-and-provenance.md)).

> **Try it.** Read a COPC point cloud over the web by bounding box and resolution, and a BlueTopo tile's uncertainty band, without downloading either file.
>
> ```bash
> # PDAL: fetch only the octree nodes covering a 500 m box at ~1 m resolution.
> pdal translate \
>   "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CA_SanFrancisco_2020/ept.json" \
>   subset.laz \
>   --readers.ept.bounds="([-13631000,-13630500],[4545000,4545500])" \
>   --readers.ept.resolution=1.0
> pdal info --summary subset.laz | jq '.summary.num_points'
>
> # GDAL: statistics of the uncertainty band of a BlueTopo tile by range read.
> gdalinfo -stats -json "/vsis3/noaa-ocs-nationalbathymetry-pds/BlueTopo/BH4SX59B/BlueTopo_BH4SX59B_20240101.tiff" \
>   --config AWS_NO_SIGN_REQUEST YES | jq '.bands[1].metadata[""] , .bands[1].description'
> ```
>
> Expected outcome: a small LAZ containing only the points inside the box at the requested density, and the uncertainty-band statistics of one BlueTopo tile (band 2 is uncertainty; band 3 is the contributor index), both obtained in seconds with a few megabytes transferred. Dataset paths and tile names change; take them from the STAC or the bucket listing rather than from this page.

## 51.7 Evaluating before downloading

The cheapest validation is the one you do before committing. With range reads, five checks take minutes.

**Previews and hillshade quicklooks.** Render a hillshade of the AOI at native resolution (GDAL `gdaldem hillshade` on a `/vsicurl/` path, or the portal's own preview). Look for stitching seams, terracing from integer quantization, smoothing that erases drainage, striping from flight lines, "melted" buildings in a supposed DTM, and interpolation fans in voids ([Chapter 57](ch57-visualizing-dems.md)). Most fitness failures are visible in a hillshade.

**Metadata forensics.** Read the record as [Chapter 49](ch49-metadata.md) §49.8 and [Chapter 54](ch54-evaluating-others-data.md) describe: is the vertical CRS complete; is there a checkpoint table; does the acquisition date differ from the publication date; is the surface definition explicit; what does the licence actually say.

**Coverage and void maps.** Fetch the nodata mask, the density raster, or the source/TID layer for the AOI and compute the fraction of cells that are measured versus filled. For point clouds, PDAL's `info --boundary` and a quick density grid show where the ground returns thin out.

**Epoch check.** Compare the acquisition dates—from the project index, not the file timestamp—against the events that matter to you (construction, storms, fires, earthquakes).

**Spot check against something you trust.** Sample the DEM at a handful of locations with known heights—survey benchmarks from the NGS datasheets or a national equivalent, ICESat-2 ATL08 ground photons in open terrain, a prior survey—after converting datums. Ten points will not give you an RMSE, but they will catch a datum error of 0.3 m or a sign error of 2 × depth before you download 500 GB.

> **Worked example.** A 1 m DTM is listed for a watershed. Range-reading the project index shows three 3DEP projects: 2014 (QL2, 2 pts/m²), 2019 (QL1, 8 pts/m²), and 2022 (QL1, 8 pts/m²), with the 2014 project covering the headwaters. The seamless 1 m product therefore has an effective resolution of perhaps 2–3 m in the headwaters and about 1 m elsewhere ([Chapter 44](ch44-resolution-and-sampling.md)), and an epoch spread of eight years across a seam. The 2014 project's report states NVA 9.2 cm RMSE$_z$ from 35 checkpoints and VVA 28 cm; the 2019 and 2022 reports state 5–6 cm and 15–18 cm. A spot check of six NGS benchmarks (all in the 2019 area) gives a mean difference of +0.04 m, σ 0.06 m—consistent with the report. The decision: use the seamless DTM for the channel network, but mask the 2014 area in any slope-stability analysis requiring sub-2 m features, and do not use the composite for change detection across the seam. Nothing was downloaded to reach it.

## 51.8 When nothing fits

Sometimes the search ends with no candidate that meets the specification. Three paths remain, and the choice is an economic and scientific one ([Chapter 28](ch28-reducing-cost.md)).

**Commission a survey** ([Chapter 26](ch26-survey-planning.md)) when the requirement is firm, the area is bounded, and the budget allows: drone lidar or SfM for hectares to a few square kilometres; crewed airborne lidar for tens to thousands of square kilometres; multibeam or bathymetric lidar for water. Specify the deliverables of [Chapter 49](ch49-metadata.md) and the retention of [Chapter 50](ch50-archiving-and-provenance.md) in the contract.

**Enhance what exists** ([Chapter 45](ch45-super-resolution.md)) when the gap is modest: fuse a coarse DEM with higher-resolution partial coverage, apply bias corrections against ICESat-2, remove vegetation bias with a canopy model (as FABDEM does for Copernicus DEM), or super-resolve with a learned model—while recognizing that enhancement cannot create information that was not measured, and that its uncertainty must be validated independently, not assumed from the source's.

**Live with the uncertainty**, explicitly. Propagate the available product's stated or estimated uncertainty through the analysis ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 53](ch53-accuracy-assessment.md)), report the sensitivity of the result to it, and state that the data were the limiting factor. A flood extent with a ±0.5 m band is an honest product; the same extent drawn as a line from a 30 m DSM is not.

## Then & now

Finding elevation data was once a matter of knowing which drawer to open. Map libraries held topographic sheets by series and index; hydrographic offices kept survey indexes by sheet number; agencies published paper catalogs of DEM tiles. The 1990s brought **FTP sites** and the first **clearinghouses**: the US National Spatial Data Infrastructure, established by Executive Order 12906 in 1994 ⟨H⟩, mandated FGDC metadata and a distributed clearinghouse searchable with the Z39.50 library protocol; NASA's **Global Change Master Directory** ⟨H⟩ did the same for Earth-science datasets with controlled keywords. Searching required knowing the vocabulary, and obtaining data required knowing the FTP path.

The 2000s brought **web portals**: the USGS Seamless Data Distribution System and later The National Map, NOAA's Digital Coast, the Geospatial One-Stop (Goodchild, Fu, and Rich, 2007), and OGC's CSW standard for catalog interoperability. Portals made browsing easy and bulk access awkward; each had its own viewer, its own extraction tool, and its own notion of "download."

The 2010s inverted the relationship between data and compute. **Google Earth Engine** (public from 2010; Gorelick et al., 2017) ⟨H⟩ placed a curated catalog—SRTM, then NASADEM, ALOS, Copernicus DEM, 3DEP, GEBCO—next to a planetary-scale compute service, so that the data were found and used without ever being downloaded. **AWS Open Data** (from 2008, with 3DEP lidar as EPT from 2018) and **Microsoft Planetary Computer** (2021) made cloud-native copies public. **STAC** (2017–2021) ⟨H⟩ gave these catalogs a common, machine-first index, and STAC API gave them a common search. **OpenTopography** (2009–) showed that a community repository could combine curation, DOIs, APIs, and on-demand processing. The present state is "API-first catalogs plus cloud-native direct access": a query returns Items, Items point to COGs and COPCs, and analysis begins with a range read. What has not changed is that the quality facts—accuracy, surface definition, datum realization—still live in reports that neither the clearinghouse of 1994 nor the STAC API of 2025 can filter on.

## Validation & uncertainty

Discovery introduces its own errors, upstream of any measurement error, and they are among the most consequential in the book because they are invisible in the result.

**Wrong-surface errors.** A DSM used as a DTM (or a shoal-biased navigation surface used for volume) produces systematic errors of the height of whatever covers the ground—metres to tens of metres. Detect by hillshade inspection and by reading the surface definition; quantify by differencing against a known-surface-type dataset over a sample.

**Wrong-epoch errors.** A pre-event surface mistaken for post-event, or a composite whose seam crosses the study area with years between sides, converts geomorphic change into artefact or hides it. Detect from the project-date layer; quantify by the expected change rate over the epoch gap ([Chapter 37](ch37-time-scales-of-change.md)).

**Resampled-resolution errors.** A "1 m DEM" resampled from 10 m data carries 10 m effective resolution and smooth artefacts; slope and curvature derivatives are biased low. Detect by comparing stated resolution to source density and by the power spectrum or the variogram of the DEM ([Chapter 44](ch44-resolution-and-sampling.md)).

**Datum and provenance errors from APIs and mirrors.** An elevation obtained from an API with undisclosed provenance cannot be assigned an uncertainty; a mirror that re-tiled or re-compressed may differ from the original. Detect by spot checks against benchmarks and by checksum comparison with the authoritative source.

**Selection bias.** Choosing the dataset that "looks best" in the area you happen to inspect, or the one with the finest nominal resolution, biases toward products that are smoothest or newest rather than most accurate. Mitigate by scoring candidates against the written specification of §51.1 and by spot-checking all candidates at the same points.

> **Uncertainty budget.** Error introduced at the discovery stage, before any measurement error, with typical magnitudes (approximate; terrain- and site-dependent):
>
> | Discovery error | Typical vertical consequence | How detected before download |
> |---|---|---|
> | DSM taken for DTM in forest or city | 5–30 m systematic | Hillshade; surface-definition metadata |
> | Epoch mismatch across a composite seam | 0–several m where terrain changed | Project-date layer; difference across seam |
> | Nominal 1 m from 10 m source | derivative bias; features < ~20 m lost | Source density in metadata; variogram |
> | API with undisclosed source | unknown; metres typical for SRTM-class blends | Cannot be detected—avoid for measurement |
> | Tidal datum assumed equal to orthometric | 0.3–3 m systematic | Vertical CRS in metadata; spot check at gauge |
> | Mirror re-compressed with lossy quantization | 0.1–1 m terracing | Histogram of values; compare to source checksum |
> | Licence incompatible with use | not a height error; a project error | Licence field before download |

Report, for any dataset you chose: the specification you searched against, the candidates considered and why they were rejected, the source and version actually obtained (with checksums and fetch date), the results of the pre-download checks (hillshade findings, coverage fraction, spot-check statistics), and the datum conversions applied with their uncertainty. This paragraph in a methods section is what makes the subsequent analysis reproducible and is routinely omitted ([Chapter 53](ch53-accuracy-assessment.md)).

## Software

**Open source:** **pystac-client** (Python client for STAC API search, paging, and ItemCollections); **stac-browser** (browse any STAC catalog in a web page); **stac-fastapi** and **pgstac** (serve your own STAC API over PostgreSQL); **odc-stac** and **stackstac** (assemble STAC Items into lazy xarray cubes for analysis without download); **rasterio** and **GDAL** (`/vsicurl/`, `/vsis3/`, `/vsiaz/` for range reads; `gdaldem` for quicklooks; `gdal_translate -projwin` for subsetting over HTTP); **PDAL** (`readers.ept`, `readers.copc`, `readers.stac` for remote point clouds); **QGIS** with the STAC API Browser plugin and native COPC/COG support; **OpenTopography API** clients and the `opentopo` notebooks; **icepyx** and **SlideRule** (ICESat-2 subsetting for spot checks); **earthaccess** (NASA CMR search and Earthdata authentication); **openeo** and **sentinelhub** clients for the Copernicus Data Space; **aria2c** and `aws s3 sync` (parallel bulk download); **pyproj**/PROJ with PROJ-data (datum conversion of candidates). Caveat shared by all STAC clients: they return what providers populated, and most providers populate no quality fields.

**Free but closed:** **Google Earth Engine** Python and JavaScript APIs (free for non-commercial use; a very large curated elevation catalog with the caveat that export and reproducibility outside the platform require care); **Microsoft Planetary Computer** Hub (free tier; availability of hosted compute has changed over time); commercial cloud consoles for browsing public buckets.

**Commercial:** **Esri ArcGIS Living Atlas** (curated elevation services, including the World Elevation layers, which blend many sources—read the item descriptions for source and resolution per area); **Planet** and **Maxar** discovery APIs for stereo imagery and derived DEMs; **Airbus OneAtlas** for WorldDEM products; **Intermap** and other vendor portals; **Safe Software FME** for building ingestion pipelines against portals.

## Standards & guides

- **STAC 1.0.0 (2021) / 1.1.0 (2024)**, *SpatioTemporal Asset Catalog specification*; **STAC API 1.0.0 (2023)** with the filter (CQL2), sort, fields, query, and aggregation extensions — catalog records and search.
- **STAC extensions:** projection, raster, pointcloud, processing, file, scientific, version, classification — the elevation-relevant properties.
- **OGC API – Records – Part 1: Core**; **OGC API – Features – Part 1 (2019)** — web-API catalog and feature access on which STAC API builds.
- **OGC Catalogue Service for the Web 2.0.2 (2007)** — legacy catalog protocol still used by INSPIRE and national geoportals.
- **ISO 19115-1:2014** and **ISO 19157-1:2023** — the record content that quality-first search would filter.
- **W3C DCAT 3 (2024)** and **GeoDCAT-AP** — dataset catalog vocabularies used by open-data portals and the European data portal.
- **INSPIRE Discovery Services Technical Guidance** — CSW-based discovery for European spatial data.
- **NASA CMR API documentation** and **GCMD Keywords** — search of NASA DAAC holdings; keyword vocabularies.
- **Cloud-Optimized GeoTIFF specification (OGC 21-026, 2023)**; **COPC 1.0 (2021)**; **Zarr v3** — the formats that make range-read evaluation possible.
- **USGS 3DEP product and metadata documentation** and **Lidar Base Specification 2024** — what the project reports contain and how to find them from a work-unit identifier.
- **NOAA Digital Coast and NCEI data access documentation**; **NBS/BlueTopo product description** — coastal and bathymetric portals.
- **Nebert, D. (ed.) (2004), *The SDI Cookbook*, GSDI** — the spatial data infrastructure reference of the clearinghouse era.

## Pitfalls

- **Using an elevation API without knowing which DEM answered** → convenience → results irreproducible and unassignable an uncertainty; use a named dataset directly.
- **Downloading a "1 m DEM" that is a resampled 10 m** → the portal lists cell size, not source → compare source density or GSD with cell size; inspect a hillshade for smoothness.
- **Mixing tiles from two 3DEP (or any) projects of different years without noticing** → seamless products hide project boundaries → fetch the project-footprint layer with dates and overlay it on the AOI.
- **Assuming the portal's "accuracy" field was independently tested** → the field is often the specification or the sensor nominal → look for a checkpoint table and the "tested to meet" sentence.
- **Licence surprises after delivery (NC, share-alike, no redistribution)** → licence read last → read the licence first; record the text with the manifest.
- **Searching by nominal resolution alone** → it is the only sortable field → score against the written specification; rank by surface type, epoch, density, evidence of accuracy, datum, licence.
- **Treating the cloud mirror as identical to the agency release** → it usually is, until it is not → compare checksums or at least versions; note which you used.
- **Fetching the whole project before looking at it** → habit from the download era → range-read a hillshade, the coverage mask, and the uncertainty layer first.
- **Ignoring the vertical datum of marine data until the merge** → it is a different community's default → check MLLW/LAT/MSL and the sign convention at discovery time.
- **Trusting "latest" over "best"** → newest looks safest → a 2012 lidar DTM often beats a 2023 stereo DSM for bare earth; match surface and accuracy to the use.
- **No manifest of what was fetched** → nobody asked until the audit → write source, Item ID, version, checksum, date, and licence into a CSV as you download.

## Key takeaways

- Write the specification first—where, when, what surface, resolution and accuracy, datum, licence, format, cost—and score candidates against it; "best" is use-dependent and never equals finest nominal resolution.
- Search the national agency and hydrographic office first, then the aggregators (OpenTopography, Digital Coast, EMODnet, GEBCO/DCDB), then the global products, then the cloud catalogs that mirror them with better access.
- STAC API answers where, when, which CRS, which density, and which file; it does not yet answer how accurate, which surface, or which geoid—expect a second stage of metadata forensics.
- Project boundaries with dates are the most important layer in any seamless product; fetch them before the elevations.
- Prefer cloud-native range reads for evaluation: hillshade, coverage mask, uncertainty layer, and a spot check against benchmarks or ICESat-2 cost minutes and prevent most fitness failures.
- Elevation APIs and blended terrain layers with undisclosed provenance are for visualization, not measurement.
- Record exactly what you obtained—source, identifiers, version, checksums, fetch date, licence—because the reproducibility of everything downstream depends on it.
- When nothing fits, choose deliberately between commissioning, enhancing, and living with stated uncertainty; do not quietly use what does not fit.

## References

- Bielski, C., López-Vázquez, C., Grohmann, C. H., Guth, P. L., Hawker, L., Gesch, D., Trevisani, S., Herrera-Cruz, V., Riazanoff, S., Corseaux, A., Reuter, H. I., and Strobl, P. (2024). Novel approach for ranking DEMs: Copernicus DEM improves one arc second open global topography. *IEEE Transactions on Geoscience and Remote Sensing* 62:4503922. doi:10.1109/TGRS.2024.3368015.
- Crosby, C. J., Arrowsmith, J. R., and Nandigam, V. (2020). Zero to a trillion: advancing Earth surface process studies with open access to high-resolution topography. In Tarolli, P. and Mudd, S. M. (eds.), *Remote Sensing of Geomorphology*, Developments in Earth Surface Processes 23, pp. 317–338. Amsterdam: Elsevier.
- Goodchild, M. F., Fu, P., and Rich, P. (2007). Sharing geographic information: an assessment of the Geospatial One-Stop. *Annals of the Association of American Geographers* 97(2):250–266.
- Gorelick, N., Hancher, M., Dixon, M., Ilyushchenko, S., Thau, D., and Moore, R. (2017). Google Earth Engine: planetary-scale geospatial analysis for everyone. *Remote Sensing of Environment* 202:18–27. doi:10.1016/j.rse.2017.06.031.
- Guth, P. L., Van Niekerk, A., Grohmann, C. H., Muller, J.-P., Hawker, L., Florinsky, I. V., Gesch, D., Reuter, H. I., Herrera-Cruz, V., Riazanoff, S., López-Vázquez, C., Carabajal, C. C., Albinet, C., and Strobl, P. (2021). Digital elevation models: terminology and definitions. *Remote Sensing* 13(18):3581. doi:10.3390/rs13183581.
- Hawker, L., Uhe, P., Paulo, L., Sosa, J., Savage, J., Sampson, C., and Neal, J. (2022). A 30 m global map of elevation with forests and buildings removed. *Environmental Research Letters* 17(2):024016. doi:10.1088/1748-9326/ac4d4f.
- STAC Contributors (2021). *SpatioTemporal Asset Catalog (STAC) Specification*, version 1.0.0; and *STAC API Specification*, version 1.0.0 (2023). Community-authored; stacspec.org.
- Nebert, D. D. (ed.) (2004). *Developing Spatial Data Infrastructures: The SDI Cookbook*, Version 2.0. Global Spatial Data Infrastructure Association.
- Neumann, T. A., Martino, A. J., Markus, T., et al. (2019). The Ice, Cloud, and Land Elevation Satellite-2 mission: a global geolocated photon product derived from the Advanced Topographic Laser Altimeter System. *Remote Sensing of Environment* 233:111325. doi:10.1016/j.rse.2019.111325.
- Open Geospatial Consortium (2007). *OpenGIS Catalogue Services Specification 2.0.2*, OGC 07-006r1.
- Open Geospatial Consortium (2023). *Cloud Optimized GeoTIFF Standard*, OGC 21-026.
- Stoker, J. and Miller, B. (2022). The accuracy and consistency of 3D Elevation Program data: a systematic analysis. *Remote Sensing* 14(4):940. doi:10.3390/rs14040940.
- Sugarbaker, L. J., Constance, E. W., Heidemann, H. K., Jason, A. L., Lukas, V., Saghy, D. L., and Stoker, J. M. (2014). *The 3D Elevation Program initiative—A call for action*. USGS Circular 1399. doi:10.3133/cir1399.
- Weatherall, P., Marks, K. M., Jakobsson, M., et al. (2015). A new digital bathymetric model of the world's oceans. *Earth and Space Science* 2(8):331–345. doi:10.1002/2015EA000107.
- Wessel, B., Huber, M., Wohlfart, C., Marschalk, U., Kosmann, D., and Roth, A. (2018). Accuracy assessment of the global TanDEM-X Digital Elevation Model with GPS data. *ISPRS Journal of Photogrammetry and Remote Sensing* 139:171–182. doi:10.1016/j.isprsjprs.2018.02.017.

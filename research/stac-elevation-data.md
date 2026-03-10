Prompt: 

How are Digital Elevations Models (DEMs) represented in SpatioTemporal
Asset Catalogs: STAC?  Are there extensions that can or should be used for DEMs?
Are there other elevation data types that have special considerations for STAC,
for example LIDAR, SAR, or other types.

Mar 10, 2026 Gemini Deep Research

# **The Representation of Digital Elevation Models and 3D Topographic Data in SpatioTemporal Asset Catalogs (STAC)**

## **1\. Introduction to Cloud-Native Geospatial Indexing and the STAC Specification**

The proliferation of high-resolution Earth observation technologies over the past two decades has generated an unprecedented volume of three-dimensional spatial data. From global satellite-derived topographic grids and interferometric radar surface models to hyper-dense terrestrial laser scanning point clouds and acoustic bathymetric arrays, the sheer mass of elevation data necessitates highly efficient, standardized mechanisms for discovery, querying, and retrieval. In the era of cloud-native computing, traditional file-based architectures and proprietary metadata silos are increasingly obsolete. Consequently, the SpatioTemporal Asset Catalog (STAC) specification has emerged as the definitive, globally adopted standard for structuring and querying geospatial asset metadata in cloud environments.1

At its core, a "spatiotemporal asset" is defined as any file representing information about the Earth at a specific place and time.1 While STAC initially gained traction as a standard designed primarily for indexing two-dimensional optical satellite imagery, its intentionally minimal core and highly flexible extension mechanism have enabled it to support a vastly broader array of phenomenologies.1 Today, the STAC specification is extensively utilized by governmental space agencies, commercial satellite operators, and academic institutions to index Digital Elevation Models (DEMs), Light Detection and Ranging (LiDAR) point clouds, Synthetic Aperture Radar (SAR) products, and complex subaqueous bathymetric grids.1

The fundamental architecture of STAC relies on three primary JSON-based components that work in concert to organize data hierarchically: Catalogs, Collections, and Items.4

* **STAC Catalog:** A Catalog provides a flexible, overarching structure to link various STAC entities together. It functions essentially as a directory tree, allowing web crawlers or APIs to traverse the links to discover underlying data.5  
* **STAC Collection:** A Collection extends the Catalog specification by adding comprehensive dataset-level information. This includes overarching spatial and temporal extents, licensing details, keywords, and provider metadata that apply to all items contained within the collection.5  
* **STAC Item:** The STAC Item is the atomic, indispensable unit of the specification. It represents a single spatiotemporal asset (or a bundle of inseparable assets, like multiple spectral bands of a single scene) as a standard GeoJSON Feature. The Item is augmented with foreign members relevant to a STAC object, including fields identifying the time range and specific link relations to the actual physical assets stored in the cloud (e.g., Cloud Optimized GeoTIFFs or LAZ files).5

By standardizing the metadata layer using JavaScript Object Notation (JSON), STAC enables end-users to employ existing libraries and tools to access diverse elevation datasets without writing bespoke code to interact with each individual data provider's proprietary APIs.1 Furthermore, STAC aligns seamlessly with modern web standards, particularly the Open Geospatial Consortium (OGC) API \- Features specification, ensuring high interoperability across GIS software and programmatic data science workflows.7

This report provides an exhaustive, multi-disciplinary analysis of how digital elevation models and complex 3D topographic data are represented within the STAC specification. It details the specific extensions, metadata schemas, and cataloging best practices required to accurately capture the physical nuances of raster topography, discrete point clouds, interferometric radar derivations, and subaqueous bathymetry.

## **2\. Core Mechanisms for Raster Elevation Representation in STAC**

A Digital Elevation Model (DEM) is broadly defined as a digital representation of the elevations or heights of a topographic surface in the form of a geo-rectified, area-based grid covering the Earth.9 Because DEMs are fundamentally matrices of numerical values corresponding to physical measurements rather than visual color spectra, their representation in STAC relies heavily on extensions specifically designed for rasterized data and complex geospatial projections.

### **2.1 The Raster Extension (raster)**

When indexing DEMs, the fundamental data structure is a continuous grid of numbers. To describe the physical characteristics of this structure, STAC employs the Raster Extension (raster). This extension allows data providers to describe assets at the band level, detailing critical information required by Geographic Information System (GIS) software and data science libraries to correctly parse and interpret the numerical arrays.10

The Raster Extension introduces several key properties that are indispensable for accurately indexing DEMs:

* **raster:data\_type**: Specifies the data type of the pixels. Elevation data is frequently stored as Float32 to accommodate precise decimal values without rounding errors, or as Int16 (often scaled) to significantly reduce file sizes for global datasets. Providing the data type is critical for memory allocation when loading assets via STAC APIs.10  
* **raster:nodata**: Defines the specific pixel value used to represent data voids or areas outside the survey boundary. In elevation models, values such as \-9999 or \-32768 are commonly designated as nodata to ensure that valid zero values (representing mean sea level) or legitimate negative values (representing sub-sea-level terrestrial depressions like the Dead Sea or Death Valley) are not erroneously discarded as missing data.10  
* **raster:spatial\_resolution**: Indicates the average spatial resolution, or Ground Sample Distance (GSD), of the pixels in meters. This metric allows users to immediately ascertain the granularity of the elevation model (e.g., 1-meter, 10-meter, or 30-meter grids) before downloading the asset.10  
* **raster:unit**: Specifies the unit denomination of the pixel values. For DEMs, this is almost exclusively "meters" or "feet." Explicitly defining the unit in the metadata prevents severe analytical errors in subsequent workflows, such as hydrological flow modeling or volumetric cut-and-fill calculations.11  
* **raster:sampling**: A string indicating whether a pixel value should be assumed to represent a sampling over the entire region of the pixel (area) or a single point sample at the center of the pixel (point). This is a crucial distinction in physical geodesy and grid alignment.10  
* **raster:scale and raster:offset**: In remote sensing, raw pixel values are often stored as optimized Digital Numbers (DN) to compress storage footprints. The actual physical measurement is derived by applying a multiplicator factor (scale) and adding a constant (offset) to the raw pixel value. While less common in high-precision Float32 DEMs, this approach is highly relevant for optimizing massive global elevation datasets stored as scaled integers.10

When integrating these fields, the STAC specification recommends utilizing the raster:bands array within the Asset object to delineate multiple bands or to encapsulate the properties of a single-band DEM raster cleanly.13

![][image1]

## **3\. Spatial Anchoring: The Projection Extension and Vertical Datums**

A core requirement for any spatial data is an accurate Coordinate Reference System (CRS). Without a defined projection, an elevation matrix is merely a floating mathematical array. The STAC Projection Extension (proj) provides the necessary framework to anchor DEMs to the Earth's surface accurately, enabling spatial intersection queries.14

The standard practice in STAC is to specify projection information at the Asset level rather than globally at the Item level. This is because different assets within the same STAC Item (e.g., the primary high-resolution DEM data, a derived hillshade mask, and an unprojected thumbnail image) may possess different coordinate systems, spatial shapes, or transforms.14

The primary fields of the Projection Extension include:

* **proj:code**: This string field replaces the deprecated proj:epsg field from older STAC versions. It provides the authority and specific code of the data source (e.g., EPSG:32659). This acts as the primary key for standard horizontal map projections.14  
* **proj:wkt2 or proj:projjson**: For proprietary, localized, or highly complex coordinate systems that lack a standard EPSG code, these fields provide the complete Well-Known Text (WKT2) string or the PROJJSON object defining the CRS.14  
* **proj:shape and proj:transform**: The proj:shape array defines the exact number of pixels in the Y and X directions for the raster grid. The proj:transform array provides the affine transformation coefficients required to map the local pixel coordinates directly to real-world geospatial coordinates without opening the underlying file.14  
* **proj:geometry and proj:bbox**: These fields define the footprint and bounding box of the item explicitly in the native asset CRS, distinct from the core STAC GeoJSON geometry which mandates WGS84 (EPSG:4326).14

### **3.1 The Challenge of Vertical Coordinate Reference Systems**

While horizontal map projections (like Universal Transverse Mercator or Web Mercator) manipulate X and Y coordinates to project a spherical Earth onto a flat plane, they do not inherently alter or define vertical data.16 The vertical coordinates of a DEM rely entirely on a Vertical Coordinate Reference System, also known as a vertical datum.16

A vertical datum identifies the specific origin point or surface to which all 'Z' coordinates are referenced.16 These can be gravity-related orthometric heights referenced to a geoid surface (such as the North American Vertical Datum of 1988, the Earth Gravitational Model 1996 \[EGM96\], or the Canadian Geodetic Vertical Datum of 2013).16 Alternatively, they may be ellipsoidal heights referenced strictly to the underlying geometric ellipsoid used by the geographic CRS (e.g., WGS84).16

STAC itself does not perform coordinate transformations; it relies on the metadata specification to declare the system in use accurately. If a compound EPSG code—one that explicitly defines both the horizontal and vertical datums—is available, it should be supplied in the proj:code field. In cases where the vertical transformation is complex or relies on localized geoid models, the proj:wkt2 string provides a robust mechanism to explicitly declare the vertical datum parameters to the end-user.14

### **3.2 Bounding Boxes and the Z-Axis Convention**

Furthermore, the core STAC specification dictates specific geometric conventions for representing the Z-axis in spatial queries. When using 3D geometries, the Item bounding box (bbox) must be provided as an array of six numbers. The convention mandates the format: \[minimum longitude, minimum latitude, minimum elevation, maximum longitude, maximum latitude, maximum elevation\].6

Crucially, STAC requires that elevation values be represented such that the elevation of the southwesterly-most extent is strictly the minimum value, and the northeasterly-most extent is the maximum value, formatted relative to WGS84.6 This standardized approach to the Z-axis enables naive database clients and STAC APIs to execute multi-dimensional intersection operations efficiently.

## **4\. Taxonomic Clarity: Distinguishing DSM, DTM, and DEM**

In standard GIS nomenclature and informal discourse, the term "DEM" (Digital Elevation Model) is frequently utilized as a generic umbrella term encompassing all forms of gridded 3D topographic data.9 However, precision in remote sensing and Earth sciences demands clear differentiation between a Digital Terrain Model (DTM) and a Digital Surface Model (DSM). Each represents a fundamentally different physical reality and requires distinct processing workflows.

### **4.1 Defining the Phenomenologies**

* **Digital Surface Model (DSM):** A DSM encapsulates the complete, first-return topography of the Earth. It captures both the natural terrain and all anthropogenic features extruding from the Earth's surface.22 This includes the upper canopy of vegetation, buildings, residential structures, power lines, and bridges.23 DSMs are heavily utilized in specific operational contexts: in aviation for runway approach zone encroachment analysis, in telecommunications for line-of-sight signal propagation modeling, and in urban planning for viewshed obstruction analysis.23  
* **Digital Terrain Model (DTM):** A DTM (often used synonymously with the term "bare-earth DEM") represents the bare ground topographic surface of the Earth, mathematically excluding trees, buildings, and all other surface objects.9 DTMs are generated by applying complex filtering algorithms to raw survey data (such as LiDAR point clouds) to strip away non-ground points.23 DTMs are critical for hydrological modeling, soil science, physical geodesy, floodplain mapping, and terrain analysis where surface structures would erroneously disrupt fluid flow models or volumetric analyses.24

The mathematical difference between a DSM and a DTM is often utilized to create a Canopy Height Model (CHM), which isolates the height of vegetation and structures above the ground level.28

### **4.2 Resolving Nomenclature in STAC Metadata**

The STAC specification is fundamentally un-opinionated regarding the highly specific scientific definitions of raster grids. It does not enforce a strict structural or schema difference between a DSM and a DTM; both are represented equally well using the combination of the raster and proj extensions.29 To resolve this ambiguity and ensure end-users download the correct topographic product, data providers rely on established STAC conventions, asset roles, and collection segregation.

| Model Type | Target Surface | Typical Data Sources | Common STAC Asset Roles | Primary Scientific Use Cases |
| :---- | :---- | :---- | :---- | :---- |
| **DSM** | Canopy, Buildings, Infrastructure | Optical Stereo, SAR Interferometry (InSAR), First-return LiDAR | \["data", "dsm", "surface-model"\] | Urban planning, line-of-sight modeling, aviation encroachment |
| **DTM** | Bare Earth, Ground Level | Filtered LiDAR, Ground Survey, Filtered Photogrammetry | \["data", "dtm", "elevation-model"\] | Hydrological routing, flood modeling, civil engineering, gravimetry |

Table 1: Differentiation of elevation models and their corresponding representation strategies within STAC asset roles.22

**Strategies for Differentiation in STAC:**

1. **Asset Roles:** The roles array within a STAC Asset provides critical semantic context. A provider will typically assign an array such as \["data", "dsm"\] or \["data", "dtm"\] to explicitly state the phenomenology of the grid without altering the core schema.13  
2. **Collection Separation:** In massive, multi-modal national datasets, DSMs and DTMs are often separated entirely into distinct STAC Collections. For example, within the AWS Registry of Open Data and Microsoft's Planetary Computer, the USGS 3D Elevation Program (3DEP) exposes its bare-earth products in collections like 3dep-seamless and 3dep-lidar-dtm, while digital surface models are sequestered in 3dep-lidar-dsm.34  
3. **Title and Description Metadata:** Providers heavily rely on the Common Metadata fields title and description to document the algorithmic lineage of the product. For instance, a dataset might be explicitly described as "Forest and Buildings removed Copernicus 30m DEM," signaling to the user that algorithmic filtering has been applied to convert a raw DSM into a usable DTM.36

![][image2]

## **5\. Quantifying Topographic Uncertainty: The Accuracy Extension**

Topographic data inherently contains measurement error stemming from a multitude of sources: active sensor noise, orbital inaccuracies in satellite trajectories, atmospheric phase delays (in SAR), or interpolation artifacts introduced during grid generation.38 Inaccuracies in topographic data represent a significant source of error for downstream scientific analysis, particularly in hydrologic flow routing, atmospheric-land exchange simulations, and climate change sea-level rise modeling.39

To address this critical requirement for scientific rigor, the STAC community introduced the Accuracy Extension (accuracy). This extension allows data providers to quantitatively express the geometric and measurement uncertainties of their datasets directly within the STAC Item or Collection metadata, removing the need for users to hunt down separate PDF validation reports.31

### **5.1 Representing Vertical and Horizontal Error**

The accuracy of an elevation model is typically evaluated by comparing the generated DEM surface against highly accurate Ground Control Points (GCPs) surveyed via Global Navigation Satellite Systems (GNSS) or high-precision spaceborne laser altimetry instruments, such as NASA's ICESat-2.9

The accuracy extension provides specific, standardized fields to log these statistical error distributions:

* **accuracy:geometric\_z\_stddev and accuracy:geometric\_z\_bias**: These fields capture the standard deviation of the vertical error (often analogous to Root Mean Square Error, RMSEz) and the mean error (bias) of the elevation values relative to the control data.9  
* **accuracy:geometric\_x\_stddev and accuracy:geometric\_y\_stddev**: These capture horizontal displacement errors in the X and Y axes.31  
* **Linear Error (LE90) and Circular Error (CE90)**: The American Society for Photogrammetry and Remote Sensing (ASPRS) Positional Accuracy Standards mandate the reporting of accuracy at specific confidence intervals rather than just standard deviations.42 LE90 represents the 90th percentile linear error, meaning 90 percent of all vertical errors fall within the stated value (e.g., an LE90 of 2 meters).43 Horizontal accuracy is similarly expressed as CE90 (Circular Error at 90% confidence).43

While LE90 and CE90 are not explicitly coded as base string fields in the minimalist STAC accuracy extension, these values are frequently encoded into custom provider properties alongside the standard bias and standard deviation metrics to adhere to governmental data procurement mandates.42

Additionally, STAC link relation types (rel) are utilized to connect an asset directly to the documentation outlining the geometric correction algorithms used. This provides deep, transparent provenance regarding exactly how the geometric accuracy was achieved and validated.31

## **6\. Volumetric Topography: LiDAR and Point Cloud Data Representation**

While gridded DEMs provide a continuous, lightweight raster surface for rapid analysis, the primary source data for modern, high-resolution topography is often a three-dimensional point cloud. Point clouds, typically generated by aerial Light Detection and Ranging (LiDAR) or Structure from Motion (SfM) photogrammetry, are hyper-dense collections of individual vertices plotted in a three-dimensional coordinate system.23

Point clouds are structurally distinct from rasters. They do not consist of a regular, continuous grid of pixels; instead, they are essentially massive lists of discrete points, often numbering in the billions per file, containing precise spatial coordinates (![][image3]) alongside rich per-point metadata attributes.47 Because the standard GeoJSON footprint and core STAC specifications are wholly insufficient to describe this level of internal file complexity, the STAC Point Cloud Extension (pointcloud or pc) was developed.46

### **6.1 The Point Cloud Extension (pc)**

The pointcloud extension enables a STAC Catalog to thoroughly describe the phenomenological and architectural traits of massive point cloud datasets.48 By implementing this extension, API clients and data catalogs can parse the structure of large binary files—such as standard LAS or LAZ formats—without needing to execute an expensive HTTP GET request to download or crack open the file headers.46

Key metadata properties implemented at the Item level under this extension include:

* **pc:type**: A mandatory string that declares the physical phenomenology of the sensor used to capture the data. Valid values include lidar (active laser scanning), eopc (electro-optical point cloud, usually derived from stereo photogrammetry), radar, and sonar (acoustic multibeam bathymetry).49  
* **pc:count**: An integer defining the total number of points contained within the asset, useful for allocating memory prior to download.49  
* **pc:encoding**: Specifies the format of the data (e.g., laszip, ascii, binary), which is critical for determining the necessary parsing libraries (like PDAL or LAStools) required by the client.50  
* **pc:density**: A floating-point number representing the average number of points per square unit area. This enables users to filter massive datasets based on the point density required for their specific algorithms (e.g., filtering for \>10 points per square meter to extract detailed building footprints).49

### **6.2 Defining Dimensional Schemas (pc:schemas and pc:statistics)**

The most technically complex and powerful feature of the Point Cloud extension is the pc:schemas object. A LiDAR point cloud contains much more information than simple elevation coordinates. A single pulse of laser light emitted from an aircraft can penetrate a forest canopy and return multiple times as it hits branches, leaves, and finally the bare earth.23 Consequently, modern LiDAR data formats (like ASPRS LAS version 1.4) record a multitude of discrete dimensions for every single point.46

The pc:schemas field is a sequential array of items that precisely defines the dimensions present in the file, their data types (floating, unsigned, or signed), and their size in full bytes.49

A standard topographic LiDAR asset will define a complex schema that includes:

* **Coordinates:** X, Y, Z (typically stored as floating-point or highly compressed scaled integers).  
* **Intensity:** The amplitude of the return laser pulse, indicating the physical reflectivity of the surface material.54  
* **Return Number & Number of Returns:** Vital attributes for filtering algorithms aiming to separate canopy hits from true bare-earth hits.  
* **Classification:** Standardized integer codes defined by ASPRS (e.g., Class 2 for Ground, 5 for High Vegetation, 6 for Building, 9 for Water).55

Complementing the schema array is the pc:statistics object. This object maps directly to the schema array and provides pre-calculated per-channel summary statistics (including minimum, maximum, average, variance, and standard deviation).49 This powerful feature allows a user to query a STAC API to find only those specific point cloud tiles where the maximum intensity exceeds a certain threshold, or where specific ASPRS classifications (like buildings or bridges) are guaranteed to exist within the tile.55

### **6.3 Cloud-Optimized Point Clouds (COPC)**

The modernization of STAC's point cloud capabilities is closely tied to the emergence of the Cloud Optimized Point Cloud (COPC) format. Similar in philosophy to the Cloud Optimized GeoTIFF (COG) used for rasters, a COPC file organizes the point data in a clustered, hierarchical octree structure within a standard LAZ-compressed file. STAC Items index these COPC files, allowing clients to stream only the specific spatial subsets and resolutions they need directly from cloud storage via HTTP Range Requests. This drastically reduces data egress costs and processing time compared to downloading monolithic LAZ files.55

## **7\. Synthetic Aperture Radar (SAR) and InSAR Elevation Derivation**

While aerial LiDAR provides unmatched localized resolution for municipal and regional mapping, the vast majority of consistent, global-scale elevation models—such as the Shuttle Radar Topography Mission (SRTM) and the highly accurate Copernicus DEM (derived from the TanDEM-X mission)—are generated using active spaceborne radar systems.59

Synthetic Aperture Radar (SAR) systems provide day-and-night, all-weather imaging capabilities by emitting microwave pulses and recording the backscatter returning to the sensor.61 When multiple SAR images are acquired over the exact same area from slightly different spatial vantage points, the phase differences between the returning microwave signals can be exploited mathematically. This technique, known as Interferometric Synthetic Aperture Radar (InSAR), can be utilized to generate highly accurate digital elevation models or to measure millimeter-scale surface deformation over time.39

### **7.1 The SAR Extension (sar)**

When cataloging raw radar data (such as Single Look Complex (SLC) files) that may be used downstream for elevation derivation, STAC utilizes the SAR Extension (sar). Because radar geometry is oblique and side-looking, the physical properties of the acquisition heavily influence the accuracy of any derived DEM.64

The sar extension requires data providers to explicitly document parameters such as:

* **sar:instrument\_mode and sar:polarizations**: Defines the operational imaging mode (e.g., StripMap, Spotlight, Interferometric Wide) and the polarization combinations of the emitted and received waves (e.g., VV, HH, VH).66  
* **sar:observation\_direction**: Indicates whether the radar antenna was pointing left or right relative to the flight trajectory of the satellite.68  
* **sar:pixel\_spacing\_range and sar:pixel\_spacing\_azimuth**: Details the spatial resolution in both the parallel (azimuth) and perpendicular (range/slant) flight paths.68

### **7.2 The InSAR Extension (insar) and Height of Ambiguity**

To explicitly describe topographic or deformation products generated via interferometry, the STAC community developed the InSAR Extension (insar). This extension is crucial for establishing the provenance, quality, and physical validity of SAR-derived DEMs.68

The accuracy of an InSAR DEM is heavily dependent on the spatial baseline between the two radar acquisitions used to create the interferogram.39 The insar extension captures this geometry through specific quantitative fields:

* **insar:perpendicular\_baseline**: The absolute distance between the two satellite acquisition spots perpendicular to the viewing direction. The length of this baseline dictates the sensitivity of the interferogram to topographic height.68  
* **insar:temporal\_baseline**: The time elapsed between the reference and secondary acquisitions (e.g., 6 days for Sentinel-1). Shorter temporal baselines are required for DEM generation to limit phase decorrelation caused by environmental changes on the ground (e.g., vegetation growth, snowmelt, or soil moisture changes).39  
* **insar:height\_of\_ambiguity**: This is arguably the most critical physical parameter in the extension. It represents the specific altitude difference that generates a full ![][image4] change in the interferometric phase cycle, scaled by the perpendicular baseline.68 A smaller height of ambiguity means the interferogram is highly sensitive to fine topography, reducing the influence of atmospheric phase delay or instrument noise during the complex phase unwrapping process.39

Furthermore, SAR backscatter must often be radiometrically terrain-corrected (flattened) to account for radiometric distortions (layover and foreshortening) caused by undulating terrain.65 The insar:processing\_dem field explicitly documents the string identifier of the specific reference DEM (e.g., COP-DEM\_GLO30 or SRTM30) that was utilized during the geocoding and terrain-correction pipelines.67

## **8\. Bathymetry: Special Considerations for Subaqueous Elevation**

Bathymetry is the measurement of the depth of water in oceans, seas, or lakes.69 While bathymetry is conceptually similar to terrestrial topography—in that it maps a physical surface—indexing subaqueous elevation data within STAC introduces a host of complex challenges regarding vertical coordinate geometry, tidal datums, and legacy measurement paradigms.70

### **8.1 The Z-Axis Paradigm Conflict: Depth vs. Elevation**

In standard terrestrial topographic mapping, the Z-axis represents elevation, defined mathematically as positive values extending upward away from the center of the Earth's mass.71 Conversely, the hydrographic surveying community traditionally utilizes a "positive down" convention, where larger positive numbers represent deeper depths, and negative numbers represent terrestrial features extending above the water datum.71

This paradigm conflict poses a structural challenge for interoperable global data catalogs. To maintain spatial indexing consistency and prevent query logic failures, STAC rigidly enforces a "positive up" convention for its metadata.71 When defining 3D bounding boxes in STAC Items (\`\`), the minZ must represent the lowest elevation.6 Therefore, for bathymetric STAC Items, the deepest ocean trench must be represented as a negative number (e.g., \-10984 meters), ensuring that spatial queries intersect correctly across seamless terrestrial and marine datasets.6

It is important to note that while STAC enforces this negative-value structure at the metadata indexing level, the individual physical raster assets (like a Bathymetric Attributed Grid, or BAG file) may internally store depths as positive values to conform to hydrographic standards. This requires data engineers and end-users to explicitly transform or invert the data matrix upon ingestion for seamless visualization.70

### **8.2 Vertical Datums and Tidal Interpolation**

Coastal topobathymetric models (TBDEMs)—seamless elevation grids that merge land topography with adjacent water depth—are particularly complex to catalog because the constituent datasets are measured against fundamentally different vertical datums.74 Terrestrial elevation is typically referenced to an orthometric datum based on a geoid model (e.g., NAVD88 in North America), while nearshore bathymetry collected by sonar or LiDAR is referenced to dynamically shifting tidal datums, such as Mean Lower Low Water (MLLW) or Mean Sea Level (MSL).69

STAC metadata handles these discrepancies via the projection extension's proj:wkt2 field, which can embed the complex transformation matrices necessary to mathematically align the disparate vertical surfaces.14 Due to localized land subsidence and the spatial interpolation required between sparse tidal gauge benchmarks, rigorous datum conversion algorithms (like NOAA's VDATUM tool) are often documented within the processing:lineage field of the STAC Item. This provides transparency to the user regarding how the seamless elevation surface was synthesized and what transformation errors may exist.75

### **8.3 Modalities of Subaqueous Data: Sonar, LiDAR, and SDB**

Bathymetric data indexed in STAC catalogs generally originates from three distinct phenomenologies, each requiring slightly different metadata treatments:

1. **Acoustic (Sonar):** Multibeam and single-beam echosounders mounted on vessels produce hyper-accurate soundings of the seafloor. These are often processed into Bathymetric Attributed Grids (BAG), a non-proprietary format that preserves both the depth estimation and a co-registered uncertainty array.71 STAC indexes these using the raster extension.  
2. **Topobathymetric LiDAR:** Airborne LiDAR systems utilizing green-wavelength lasers can penetrate the water column to rapidly map shallow nearshore environments.77 These are indexed using the STAC pointcloud extension, utilizing specific ASPRS domain classifications within the pc:schemas to separate the water surface returns from the submerged benthic (seafloor) returns.77  
3. **Satellite-Derived Bathymetry (SDB):** An emerging technique that utilizes multispectral optical satellite imagery (such as Copernicus Sentinel-2 or USGS Landsat 8\) to map shallow coastal zones without deploying vessels.80 By employing physics-based radiative transfer equations or empirical band-ratio models (comparing the attenuation of blue and green light in the water column), algorithms can infer relative depth up to the optical extinction limit of the water.80 SDB STAC Items heavily utilize the Electro-Optical (eo) extension alongside the raster extension to explicitly define the specific radiometric inputs and center wavelengths used for the bathymetric derivation.77

## **9\. Cataloging Best Practices and Operational Architectures**

The deployment of massive, continent-scale or global elevation datasets requires strict adherence to cataloging best practices to ensure broad interoperability and highly performant search capabilities.

### **9.1 Static vs. Dynamic Catalogs**

The STAC architecture supports two primary deployment models: static and dynamic.33

* **Static Catalogs:** A Static Catalog is simply a network of raw JSON files hosted on basic, highly scalable cloud storage (like Amazon S3 or Azure Blob Storage). The JSON files link to one another hierarchically, allowing web crawlers to traverse the directory tree.1 This method does not respond to dynamic queries but is highly cost-effective and robust for publishing massive, immutable historical elevation datasets.33  
* **Dynamic Catalogs (STAC API):** A Dynamic Catalog involves a web server (such as an API compliant with OGC API \- Features) backed by a powerful geospatial indexing database like Elasticsearch or PostGIS.7 Dynamic APIs are essential for high-performance programmatic querying, allowing users to instantly retrieve all DEM strips intersecting a specific geographic polygon within a given date range.33

In modern enterprise and scientific deployments, the accepted best practice is a hybrid approach: host a static STAC catalog on cloud storage adjacent to the physical assets (e.g., COGs or COPCs) to serve as a durable source of truth, and then ingest that static structure into a dynamic STAC API endpoint to facilitate complex spatial searches for end-users.33

### **9.2 Real-World Implementations of Elevation Catalogs**

Major scientific organizations and commercial cloud providers have wholly adopted STAC as the default metadata infrastructure for distributing foundational elevation datasets.83

**The USGS 3D Elevation Program (3DEP):** The United States Geological Survey (USGS) utilizes STAC to catalog the massive 3DEP dataset, which aims to provide seamless, high-resolution topographic coverage of the nation.35 The architecture intelligently segregates data into distinct collections based on resolution and phenomenology.18 For instance, the 3dep-seamless collection contains the continuous bare-earth DTM grids at various resolutions (e.g., 10-meter, 30-meter), while raw point clouds are indexed in entirely separate collections utilizing Cloud Optimized Point Clouds (COPC) and the STAC pointcloud extension.35

**The Copernicus DEM:** Funded by the European Space Agency and derived from the TanDEM-X SAR mission, the Copernicus DEM provides a highly accurate global Digital Surface Model.86 It is distributed via STAC collections separated by spatial resolution (e.g., the cop-dem-glo-30 collection for 30-meter resolution and cop-dem-glo-90 for 90-meter resolution).87 Hosted on platforms like the Microsoft Planetary Computer and AWS Earth Search, these collections utilize the STAC raster and proj extensions, delivering data in Cloud Optimized GeoTIFF (COG) formats. This enables analysts to perform direct, chunk-based read access without initiating full, monolithic file downloads.86

**Polar Geospatial Center (PGC) ArcticDEM and REMA:** The PGC generates continent-scale, 2-meter resolution elevation models for the polar regions using stereoscopic auto-correlation of overlapping high-resolution optical satellite images.89 PGC provides a dynamic STAC API that exposes both individual time-stamped "strip" DEMs (highly useful for temporal change detection, such as measuring glacial retreat over seasons) and seamless "mosaic" tiles.89 Because these models are photogrammetrically derived from optical imagery, the metadata catalogs often integrate STAC attributes relating to sun elevation, cloud cover, and off-nadir viewing angles sourced from the original optical stereopairs.90

![][image5]

## **10\. Emerging Paradigms and Future Extensions**

As cloud computing capabilities expand and the volume of Earth observation data grows, the geospatial community continues to push the boundaries of how STAC represents three-dimensional and algorithmically derived data.

### **10.1 3D City Models (city3d)**

Urban planning, smart city infrastructure, and digital twin applications require spatial data that goes beyond 2.5D surface rasters to represent true 3D vector geometries (e.g., buildings with complex overhangs or internal structures). The proposed city3d extension aims to integrate sophisticated 3D city models directly into STAC.40 Operating alongside the standard file extension (which catalogs checksums, file sizes, and data types), the city3d extension will allow users to query localized datasets of complex architectural structures, effectively bringing Building Information Modeling (BIM) principles into the broader remote sensing catalog.91

### **10.2 Reproducible Pipelines and Data Lineage (STACD)**

A critical limitation of current geospatial cataloging is the difficulty of tracking data provenance.92 A DEM is rarely a raw sensor product; it is almost always the culmination of complex, multi-stage algorithmic pipelines involving noise filtering, reprojection, datum transformations, and mosaic stitching.74 If an underlying source image or processing algorithm is updated, determining which downstream DEMs must be recomputed is computationally arduous.92

To address this, the STAC Extension with DAGs (STACD) has been proposed to add vital workflow awareness to the standard.92 By formally representing geospatial processing pipelines as Directed Acyclic Graphs (DAGs) embedded directly within the STAC metadata, STACD facilitates complete lineage tracking.92 This ensures that an end-user querying a DEM can inspect not only the physical parameters of the final product but the entire, unbroken chain of algorithms, sensor inputs, and parameters utilized to generate it, thereby drastically improving the scientific reproducibility and auditability of topographic analysis.93

## **11\. Conclusion**

The representation of Digital Elevation Models and complex 3D topographic data within the SpatioTemporal Asset Catalog specification marks a significant and necessary evolution in global geospatial architecture. By shifting away from rigid, monolithic data silos and proprietary query interfaces toward a flexible, JSON-based indexing standard, STAC enables unprecedented interoperability across the Earth sciences.

Through the judicious and standardized application of specific extensions—namely raster, proj, pointcloud, accuracy, and insar—data providers can accurately capture the nuanced phenomenological differences between a bare-earth LiDAR dataset, an interferometric radar surface model, and an acoustic bathymetric grid. As the global archive of topographic data continues to expand at an exponential rate, adherence to STAC formatting and cataloging best practices will remain the cornerstone of efficient, cloud-native Earth observation science. This standardization ensures that researchers, engineers, and automated algorithms can rapidly discover, filter, and deploy the three-dimensional data necessary to map, monitor, and model a continuously changing planet.

#### **Works cited**

1. OGC looks to adopt STAC as Community Standard; Seeking Public Comment before moving to vote, accessed March 10, 2026, [https://www.ogc.org/requests/ogc-looks-to-adopt-stac-as-community-standard-seeking-public-comment-before-moving-to-vote/](https://www.ogc.org/requests/ogc-looks-to-adopt-stac-as-community-standard-seeking-public-comment-before-moving-to-vote/)  
2. SpatioTemporal Asset Catalog (STAC) \- Open Geospatial Consortium \- OGC, accessed March 10, 2026, [https://www.ogc.org/standards/stac/](https://www.ogc.org/standards/stac/)  
3. radiantearth/stac-spec: SpatioTemporal Asset Catalog specification \- making geospatial assets openly searchable and crawlable \- GitHub, accessed March 10, 2026, [https://github.com/radiantearth/stac-spec](https://github.com/radiantearth/stac-spec)  
4. WGISS-53 STAC primer \- CEOS, accessed March 10, 2026, [https://ceos.org/document\_management/Working\_Groups/WGISS/Meetings/WGISS-53/1.Tuesday/2022.03.22\_11.15\_STAC%20Primer.pdf](https://ceos.org/document_management/Working_Groups/WGISS/Meetings/WGISS-53/1.Tuesday/2022.03.22_11.15_STAC%20Primer.pdf)  
5. SpatioTemporal Asset Catalogs: STAC, accessed March 10, 2026, [https://stacspec.org/](https://stacspec.org/)  
6. stac-spec/item-spec/item-spec.md at master · radiantearth/stac-spec \- GitHub, accessed March 10, 2026, [https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md](https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md)  
7. Working With STAC \- TiTiler \- Development Seed, accessed March 10, 2026, [https://developmentseed.org/titiler/examples/notebooks/Working\_with\_STAC\_simple/](https://developmentseed.org/titiler/examples/notebooks/Working_with_STAC_simple/)  
8. Introduction to the SpatioTemporal Asset Catalog (STAC)—ArcGIS Pro | Documentation, accessed March 10, 2026, [https://pro.arcgis.com/en/pro-app/latest/help/data/imagery/introduction-to-stac.htm](https://pro.arcgis.com/en/pro-app/latest/help/data/imagery/introduction-to-stac.htm)  
9. Global Digital Elevation Model Comparison Criteria: An Evident Need to Consider Their Application \- MDPI, accessed March 10, 2026, [https://www.mdpi.com/2220-9964/12/8/337](https://www.mdpi.com/2220-9964/12/8/337)  
10. stac-extensions/raster: Describes raster assets at band level (one or multiple) with specific information such as data type, unit, number of bits used, nodata. \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/raster](https://github.com/stac-extensions/raster)  
11. pystac.extensions.raster, accessed March 10, 2026, [https://pystac.readthedocs.io/en/stable/api/extensions/raster.html](https://pystac.readthedocs.io/en/stable/api/extensions/raster.html)  
12. Suitable raster format for elevation data with sub-meter accuracy? \- GIS StackExchange, accessed March 10, 2026, [https://gis.stackexchange.com/questions/158544/suitable-raster-format-for-elevation-data-with-sub-meter-accuracy](https://gis.stackexchange.com/questions/158544/suitable-raster-format-for-elevation-data-with-sub-meter-accuracy)  
13. stac-spec/best-practices.md at master \- GitHub, accessed March 10, 2026, [https://github.com/radiantearth/stac-spec/blob/master/best-practices.md](https://github.com/radiantearth/stac-spec/blob/master/best-practices.md)  
14. stac-extensions/projection: Provides a way to describe Items whose assets are in a geospatial projection. \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/projection](https://github.com/stac-extensions/projection)  
15. Best Practices — odc-stac 0.5.2 documentation, accessed March 10, 2026, [https://odc-stac.readthedocs.io/en/latest/stac-best-practice.html](https://odc-stac.readthedocs.io/en/latest/stac-best-practice.html)  
16. Vertical Datum and Projection \- Geographic Information Systems Stack Exchange, accessed March 10, 2026, [https://gis.stackexchange.com/questions/221258/vertical-datum-and-projection](https://gis.stackexchange.com/questions/221258/vertical-datum-and-projection)  
17. High Resolution Digital Elevation Model Mosaic (HRDEM Mosaic) \- CanElevation Series \- Open Government Portal, accessed March 10, 2026, [https://open.canada.ca/data/en/dataset/0fe65119-e96e-4a57-8bfe-9d9245fba06b](https://open.canada.ca/data/en/dataset/0fe65119-e96e-4a57-8bfe-9d9245fba06b)  
18. 1 meter Digital Elevation Models (DEMs) \- USGS National Map 3DEP Downloadable Data Collection, accessed March 10, 2026, [https://data.usgs.gov/datacatalog/data/USGS:77ae0551-c61e-4979-aedd-d797abdcde0e](https://data.usgs.gov/datacatalog/data/USGS:77ae0551-c61e-4979-aedd-d797abdcde0e)  
19. stac-server API documentation \- LandsatLook \- USGS.gov, accessed March 10, 2026, [https://landsatlook.usgs.gov/stac-server/api.html](https://landsatlook.usgs.gov/stac-server/api.html)  
20. Collect STAC Metadata \- Introduction, accessed March 10, 2026, [https://docs.canopy.umbra.space/docs/collect-metadata](https://docs.canopy.umbra.space/docs/collect-metadata)  
21. Differences between DEM, DSM and DTM? \- GIS StackExchange, accessed March 10, 2026, [https://gis.stackexchange.com/questions/5701/differences-between-dem-dsm-and-dtm](https://gis.stackexchange.com/questions/5701/differences-between-dem-dsm-and-dtm)  
22. Elevation Models: The Difference Between DEM, DSM, and DTM \- JOUAV, accessed March 10, 2026, [https://www.jouav.com/blog/elevation-models-dem-dsm-dtm.html](https://www.jouav.com/blog/elevation-models-dem-dsm-dtm.html)  
23. DEM, DSM & DTM: Elevation Models in GIS, accessed March 10, 2026, [https://gisgeography.com/dem-dsm-dtm-differences/](https://gisgeography.com/dem-dsm-dtm-differences/)  
24. DEM, DSM & DTM: Digital Elevation Model \- Why It's Important \- AEVEX Geodetics, accessed March 10, 2026, [https://geodetics.com/dem-dsm-dtm-digital-elevation-models/](https://geodetics.com/dem-dsm-dtm-digital-elevation-models/)  
25. What is a digital elevation model (DEM)? | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/faqs/what-a-digital-elevation-model-dem](https://www.usgs.gov/faqs/what-a-digital-elevation-model-dem)  
26. DEM, DSM, DTM: Understanding the Key Differences for Better Mapping \- GIS Navigator, accessed March 10, 2026, [https://gisnavigator.co.uk/dem-dsm-dtm-understanding-the-key-differences-for-better-mapping/](https://gisnavigator.co.uk/dem-dsm-dtm-understanding-the-key-differences-for-better-mapping/)  
27. Digital elevation models · docs.up42.com, accessed March 10, 2026, [https://docs.up42.com/data/elevation-models](https://docs.up42.com/data/elevation-models)  
28. What is a CHM, DSM and DTM? About Gridded, Raster LiDAR Data | NSF NEON, accessed March 10, 2026, [https://www.neonscience.org/resources/learning-hub/tutorials/chm-dsm-dtm](https://www.neonscience.org/resources/learning-hub/tutorials/chm-dsm-dtm)  
29. Intro to STAC: an Overview of the Specification | STAC Tutorials \- SpatioTemporal Asset Catalogs, accessed March 10, 2026, [https://stacspec.org/en/tutorials/intro-to-stac/](https://stacspec.org/en/tutorials/intro-to-stac/)  
30. The STAC Specification \- SpatioTemporal Asset Catalogs, accessed March 10, 2026, [https://stacspec.org/en/about/stac-spec/](https://stacspec.org/en/about/stac-spec/)  
31. stac-extensions/accuracy: Fields to provide estimates of accuracy, both geometric and measurement (e.g., radiometric) accuracy. \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/accuracy](https://github.com/stac-extensions/accuracy)  
32. GIS Dictionary \- Esri Support, accessed March 10, 2026, [https://support.esri.com/en-us/gis-dictionary](https://support.esri.com/en-us/gis-dictionary)  
33. stac-api-spec/stac-spec/best-practices.md at release/v1.0.0 \- GitHub, accessed March 10, 2026, [https://github.com/radiantearth/stac-api-spec/blob/release/v1.0.0/stac-spec/best-practices.md](https://github.com/radiantearth/stac-api-spec/blob/release/v1.0.0/stac-spec/best-practices.md)  
34. RasterCollection—ArcGIS Pro | Documentation, accessed March 10, 2026, [https://pro.arcgis.com/en/pro-app/3.4/arcpy/image-analyst/rastercollection-class.htm](https://pro.arcgis.com/en/pro-app/3.4/arcpy/image-analyst/rastercollection-class.htm)  
35. Datasets tagged dem in Earth Engine \- Google for Developers, accessed March 10, 2026, [https://developers.google.com/earth-engine/datasets/tags/dem](https://developers.google.com/earth-engine/datasets/tags/dem)  
36. Catalog assets lists \- awesome-gee-community-catalog, accessed March 10, 2026, [https://gee-community-catalog.org/startup/catalog-assets/](https://gee-community-catalog.org/startup/catalog-assets/)  
37. Copernicus DEM GLO-30 \- terrabyte STAC API, accessed March 10, 2026, [https://stac.terrabyte.lrz.de/browser/collections/cop-dem-glo-30](https://stac.terrabyte.lrz.de/browser/collections/cop-dem-glo-30)  
38. Beyond Vertical Point Accuracy: Assessing Inter-pixel Consistency in 30 m Global DEMs for the Arid Central Andes \- Frontiers, accessed March 10, 2026, [https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.758606/full](https://www.frontiersin.org/journals/earth-science/articles/10.3389/feart.2021.758606/full)  
39. Comparison and Validation of Digital Elevation Models Derived from InSAR for a Flat Inland Delta in the High Latitudes of Northern Canada | Request PDF \- ResearchGate, accessed March 10, 2026, [https://www.researchgate.net/publication/313021253\_Comparison\_and\_Validation\_of\_Digital\_Elevation\_Models\_Derived\_from\_InSAR\_for\_a\_Flat\_Inland\_Delta\_in\_the\_High\_Latitudes\_of\_Northern\_Canada](https://www.researchgate.net/publication/313021253_Comparison_and_Validation_of_Digital_Elevation_Models_Derived_from_InSAR_for_a_Flat_Inland_Delta_in_the_High_Latitudes_of_Northern_Canada)  
40. STAC Extensions | Overview of STAC Extensions, with advice on creating new extensions, accessed March 10, 2026, [https://stac-extensions.github.io/](https://stac-extensions.github.io/)  
41. COMPARATIVE ACCURACY EVALUATION OF FINE-SCALE GLOBAL AND LOCAL DIGITAL SURFACE MODELS, accessed March 10, 2026, [https://d-nb.info/1143840399/34](https://d-nb.info/1143840399/34)  
42. Adopt updated accuracy standards | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/adopt-updated-accuracy-standards](https://www.usgs.gov/ngp-standards-and-specifications/adopt-updated-accuracy-standards)  
43. The TanDEM-X 30m Edited Digital Elevation Model (EDEM) and DEM Change Maps (DCM) \- EOC Geoservice Data Guide, accessed March 10, 2026, [https://geoservice.dlr.de/web/dataguide/tdm30/](https://geoservice.dlr.de/web/dataguide/tdm30/)  
44. ACCURACY OF WORLDVIEW PRODUCTS \- AWS, accessed March 10, 2026, [https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/38/DG\_ACCURACY\_WP\_V3.pdf](https://dg-cms-uploads-production.s3.amazonaws.com/uploads/document/file/38/DG_ACCURACY_WP_V3.pdf)  
45. Data structure—Imagery Workflows | Documentation \- ArcGIS Online, accessed March 10, 2026, [https://doc.arcgis.com/en/imagery/workflows/best-practices/data-structure.htm](https://doc.arcgis.com/en/imagery/workflows/best-practices/data-structure.htm)  
46. A Review of Options for Storage and Access of Point Cloud Data in the Cloud \- NASA Earthdata, accessed March 10, 2026, [https://www.earthdata.nasa.gov/s3fs-public/2022-06/ESCO-PUB-003.pdf](https://www.earthdata.nasa.gov/s3fs-public/2022-06/ESCO-PUB-003.pdf)  
47. Lidar Point Cloud \- USGS National Map 3DEP Downloadable Data Collection, accessed March 10, 2026, [https://data.usgs.gov/datacatalog/data/USGS:b7e353d2-325f-4fc6-8d95-01254705638a](https://data.usgs.gov/datacatalog/data/USGS:b7e353d2-325f-4fc6-8d95-01254705638a)  
48. stac-extensions/pointcloud: Provides a way to describe point cloud datasets. The point clouds can come from either active or passive sensors, and data is frequently acquired using tools such as LiDAR or coincidence-matched imagery. \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/pointcloud](https://github.com/stac-extensions/pointcloud)  
49. README.md \- stac-extensions/pointcloud \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/pointcloud/blob/main/README.md](https://github.com/stac-extensions/pointcloud/blob/main/README.md)  
50. Source code for pystac.extensions.pointcloud, accessed March 10, 2026, [https://pystac.readthedocs.io/en/v1.14.2/\_modules/pystac/extensions/pointcloud.html](https://pystac.readthedocs.io/en/v1.14.2/_modules/pystac/extensions/pointcloud.html)  
51. API Reference — pystac 0.5.6 documentation, accessed March 10, 2026, [https://pystac.readthedocs.io/en/0.5/api.html](https://pystac.readthedocs.io/en/0.5/api.html)  
52. pointcloud/examples/pdal-to-stac.py at main \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/pointcloud/blob/main/examples/pdal-to-stac.py](https://github.com/stac-extensions/pointcloud/blob/main/examples/pdal-to-stac.py)  
53. How to Calculate Point Cloud Density | Creating a Custom Transformer, accessed March 10, 2026, [https://support.safe.com/hc/en-us/articles/25407761998349-How-to-Calculate-Point-Cloud-Density-Creating-a-Custom-Transformer](https://support.safe.com/hc/en-us/articles/25407761998349-How-to-Calculate-Point-Cloud-Density-Creating-a-Custom-Transformer)  
54. Lidar Base Specification: Collection Requirements | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-collection-requirements](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-collection-requirements)  
55. USGS 3DEP Lidar Classification | Planetary Computer \- Microsoft, accessed March 10, 2026, [https://planetarycomputer.microsoft.com/dataset/3dep-lidar-classification](https://planetarycomputer.microsoft.com/dataset/3dep-lidar-classification)  
56. Point Cloud Extension \#157 \- radiantearth/stac-spec \- GitHub, accessed March 10, 2026, [https://github.com/radiantearth/stac-spec/issues/157](https://github.com/radiantearth/stac-spec/issues/157)  
57. STAC Extensions and 0.6.2 Release | by Chris Holmes | Radiant Earth Insights | Medium, accessed March 10, 2026, [https://medium.com/radiant-earth-insights/stac-extensions-and-0-6-2-release-b0cf34272ed7](https://medium.com/radiant-earth-insights/stac-extensions-and-0-6-2-release-b0cf34272ed7)  
58. USGS 3DEP LiDAR Point Clouds \- Registry of Open Data on AWS, accessed March 10, 2026, [https://registry.opendata.aws/usgs-lidar/](https://registry.opendata.aws/usgs-lidar/)  
59. eo-examples/datasets/CopernicusDEM.ipynb at main \- GitHub, accessed March 10, 2026, [https://github.com/DLR-terrabyte/eo-examples/blob/main/datasets/CopernicusDEM.ipynb](https://github.com/DLR-terrabyte/eo-examples/blob/main/datasets/CopernicusDEM.ipynb)  
60. Global and Complementary (Non-authoritative) Geospatial Data for SDGs: Role and Utilisation \- UN-GGIM, accessed March 10, 2026, [https://ggim.un.org/documents/Report\_Global\_and\_Complementary\_Geospatial\_Data\_for\_SDGs.pdf](https://ggim.un.org/documents/Report_Global_and_Complementary_Geospatial_Data_for_SDGs.pdf)  
61. 1377\_VALIDATION OF DEMs DERIVED FROM HIGH RESOLUTION SAR DATA, accessed March 10, 2026, [https://isprs-annals.copernicus.org/articles/I-7/49/2012/isprsannals-I-7-49-2012.pdf](https://isprs-annals.copernicus.org/articles/I-7/49/2012/isprsannals-I-7-49-2012.pdf)  
62. Interferometric synthetic-aperture radar \- Wikipedia, accessed March 10, 2026, [https://en.wikipedia.org/wiki/Interferometric\_synthetic-aperture\_radar](https://en.wikipedia.org/wiki/Interferometric_synthetic-aperture_radar)  
63. Geocoding Error Correction for InSAR Point Clouds \- MDPI, accessed March 10, 2026, [https://www.mdpi.com/2072-4292/10/10/1523](https://www.mdpi.com/2072-4292/10/10/1523)  
64. Elevation generation from single SAR images: Urban topography estimated via deep learning \- ESA Earth Online, accessed March 10, 2026, [https://earth.esa.int/eogateway/documents/d/earth-online/vh-roda-2023\_maniar](https://earth.esa.int/eogateway/documents/d/earth-online/vh-roda-2023_maniar)  
65. Radiometric Terrain Flattening of Geocoded Stacks of SAR Imagery \- MDPI, accessed March 10, 2026, [https://www.mdpi.com/2072-4292/15/7/1932](https://www.mdpi.com/2072-4292/15/7/1932)  
66. STAC extension for Planet data \- GitHub, accessed March 10, 2026, [https://github.com/planetlabs/stac-extension](https://github.com/planetlabs/stac-extension)  
67. insar/examples/item.json at main · stac-extensions/insar \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/insar/blob/main/examples/item.json](https://github.com/stac-extensions/insar/blob/main/examples/item.json)  
68. stac-extensions/insar \- GitHub, accessed March 10, 2026, [https://github.com/stac-extensions/insar](https://github.com/stac-extensions/insar)  
69. Bathymetry and Elevation \- Coastal and Marine Geoscience Data System \- USGS.gov, accessed March 10, 2026, [https://cmgds.marine.usgs.gov/catalog/science.php?thcode=23\&term=22](https://cmgds.marine.usgs.gov/catalog/science.php?thcode=23&term=22)  
70. Creating a Bathymetric Database & Datum Conversion \- Army, accessed March 10, 2026, [https://cirp.usace.army.mil/techtransfer/webinars/FY19/Basic/Day1/2-Datums%20and%20Surveys\_final.pdf](https://cirp.usace.army.mil/techtransfer/webinars/FY19/Basic/Day1/2-Datums%20and%20Surveys_final.pdf)  
71. Format Specification Document Description of Bathymetric Attributed Grid Object (BAG) Version 1.0.0 Document Version RELEASE 1\. \- NOAA, accessed March 10, 2026, [https://www.ngdc.noaa.gov/mgg/bathymetry/noshdb/ons\_fsd.pdf](https://www.ngdc.noaa.gov/mgg/bathymetry/noshdb/ons_fsd.pdf)  
72. Define Bathymetry \- ArcMap Resources for ArcGIS Desktop, accessed March 10, 2026, [https://desktop.arcgis.com/en/arcmap/latest/tools/bathymetry-toolbox/define-bathymetry.htm](https://desktop.arcgis.com/en/arcmap/latest/tools/bathymetry-toolbox/define-bathymetry.htm)  
73. SpatioTemporal Asset Catalog (STAC) Community Standard \- OGC, accessed March 10, 2026, [https://docs.ogc.org/cs/25-004/25-004.html](https://docs.ogc.org/cs/25-004/25-004.html)  
74. Topobathymetric Elevation Model Development using a New Methodology: Coastal National Elevation Database \- BioOne Complete, accessed March 10, 2026, [https://bioone.org/journals/journal-of-coastal-research/volume-76/issue-sp1/SI76-008/Topobathymetric-Elevation-Model-Development-using-a-New-Methodology--Coastal/10.2112/SI76-008.full](https://bioone.org/journals/journal-of-coastal-research/volume-76/issue-sp1/SI76-008/Topobathymetric-Elevation-Model-Development-using-a-New-Methodology--Coastal/10.2112/SI76-008.full)  
75. Topographic and BaThymeTric daTa consideraTions \- NOAA Office for Coastal Management, accessed March 10, 2026, [https://coast.noaa.gov/data/digitalcoast/pdf/topo-bathy-data-considerations.pdf](https://coast.noaa.gov/data/digitalcoast/pdf/topo-bathy-data-considerations.pdf)  
76. Is Satellite-Derived Bathymetry Vertical Accuracy Dependent on Satellite Mission and Processing Method? \- MDPI, accessed March 10, 2026, [https://www.mdpi.com/2072-4292/18/2/195](https://www.mdpi.com/2072-4292/18/2/195)  
77. SaTSeaD: Satellite Triangulated Sea Depth Open-Source Bathymetry Module for NASA Ames Stereo Pipeline \- MDPI, accessed March 10, 2026, [https://www.mdpi.com/2072-4292/15/16/3950](https://www.mdpi.com/2072-4292/15/16/3950)  
78. Guidelines for Bathymetric Mapping and Orthoimage Generation Using sUAS and SfM \- the NOAA Institutional Repository, accessed March 10, 2026, [https://repository.library.noaa.gov/view/noaa/22923/noaa\_22923\_DS1.pdf](https://repository.library.noaa.gov/view/noaa/22923/noaa_22923_DS1.pdf)  
79. U.S. Coastal Lidar Elevation Data \- Including The Great Lakes And Territories, 1996 \- Present \- NOAA Fisheries, accessed March 10, 2026, [https://www.fisheries.noaa.gov/inport/item/48242](https://www.fisheries.noaa.gov/inport/item/48242)  
80. Is satellite-derived bathymetry vertical accuracy dependent on satellite mission and processing method? \- USGS Publications Warehouse, accessed March 10, 2026, [https://pubs.usgs.gov/publication/70273442](https://pubs.usgs.gov/publication/70273442)  
81. NOAA's SatBathy Tool Beta v2.1.6, accessed March 10, 2026, [https://geodesy.noaa.gov/web/science\_edu/presentations\_library/files/noaa-satbathy-tool.pdf](https://geodesy.noaa.gov/web/science_edu/presentations_library/files/noaa-satbathy-tool.pdf)  
82. PGC STAC Access – Static and Dynamic API, accessed March 10, 2026, [https://www.pgc.umn.edu/guides/stereo-derived-elevation-models/stac-access-static-and-dynamic-api/?print=pdf](https://www.pgc.umn.edu/guides/stereo-derived-elevation-models/stac-access-static-and-dynamic-api/?print=pdf)  
83. About STAC Datasets, accessed March 10, 2026, [https://stacspec.org/en/about/datasets/](https://stacspec.org/en/about/datasets/)  
84. 1 Arc-second Digital Elevation Models (DEMs) \- USGS National Map 3DEP Downloadable Data Collection, accessed March 10, 2026, [https://data.usgs.gov/datacatalog/data/USGS:35f9c4d4-b113-4c8d-8691-47c428c29a5b](https://data.usgs.gov/datacatalog/data/USGS:35f9c4d4-b113-4c8d-8691-47c428c29a5b)  
85. USGS 3DEP Lidar Collection | Planetary Computer \- Microsoft, accessed March 10, 2026, [https://planetarycomputer.microsoft.com/dataset/group/3dep-lidar](https://planetarycomputer.microsoft.com/dataset/group/3dep-lidar)  
86. Copernicus DEM GLO-30 | Planetary Computer \- Microsoft, accessed March 10, 2026, [https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30](https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30)  
87. Copernicus Digital Elevation Model (DEM) \- Registry of Open Data on AWS, accessed March 10, 2026, [https://registry.opendata.aws/copernicus-dem/](https://registry.opendata.aws/copernicus-dem/)  
88. README.md \- Earth Search STAC API \- GitHub, accessed March 10, 2026, [https://github.com/Element84/earth-search/blob/main/README.md](https://github.com/Element84/earth-search/blob/main/README.md)  
89. PGC Dynamic STAC API Tutorial \- GitHub Pages, accessed March 10, 2026, [https://polargeospatialcenter.github.io/pgc-code-tutorials/dynamic\_stac\_api/web\_files/stac\_api\_demo\_workflow.html](https://polargeospatialcenter.github.io/pgc-code-tutorials/dynamic_stac_api/web_files/stac_api_demo_workflow.html)  
90. ArcticDEM \- Polar Geospatial Center, accessed March 10, 2026, [https://www.pgc.umn.edu/data/arcticdem/](https://www.pgc.umn.edu/data/arcticdem/)  
91. cityjson/stac-city3d: STAC extension for 3D city models \- GitHub, accessed March 10, 2026, [https://github.com/cityjson/stac-city3d](https://github.com/cityjson/stac-city3d)  
92. Building Reproducible Geospatial Pipelines: A STAC Extension with DAG's | Spatialnode, accessed March 10, 2026, [https://www.spatialnode.net/articles/building-reproducible-geospatial-pipelines-a-stac-extension-with-dags25119d](https://www.spatialnode.net/articles/building-reproducible-geospatial-pipelines-a-stac-extension-with-dags25119d)  
93. Building Reproducible Geospatial Pipelines: A STAC Extension with DAG's \- CoRE Stack, accessed March 10, 2026, [https://core-stack.org/building-reproducible-geospatial-pipelines-a-stac-extension-with-dags/](https://core-stack.org/building-reproducible-geospatial-pipelines-a-stac-extension-with-dags/)

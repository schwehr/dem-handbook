Prompt: What metadata standards are there for Digital Elevation Models (DEMs) and elevation data in general?

Mar 10, 2026 Gemini Deep Research

# **Comprehensive Analysis of Metadata Standards for Digital Elevation Models and Topographic Data**

Digital Elevation Models (DEMs), Digital Surface Models (DSMs), Digital Terrain Models (DTMs), and their foundational source data—such as Light Detection and Ranging (LiDAR) point clouds and Interferometric Synthetic Aperture Radar (IfSAR)—form the critical infrastructure of modern geospatial analysis and earth sciences. Because elevation data directly dictates outcomes in floodplain mapping, infrastructure engineering, aviation safety, precision agriculture, and climate modeling, the semantic and structural descriptions of this data—its metadata—must be exhaustively detailed. Without precise metadata, a DEM is merely an arbitrary grid of floating-point numbers devoid of spatial reality. Metadata establishes the geodetic reference frame, the sensor acquisition parameters, the vertical datum, the processing lineage, and the statistical accuracy of the elevation values.1

The ecosystem of metadata standards for elevation data is notoriously complex, characterized by a historical dichotomy between descriptive catalog-level metadata, which is used primarily for data discovery and archiving, and structural file-level metadata, which is embedded directly within the data files themselves to instruct rendering and analytical software. Furthermore, the global geospatial landscape is currently undergoing a prolonged transition from localized, national legacy standards to highly interoperable, object-oriented international frameworks. This report provides an exhaustive technical analysis of the metadata standards governing DEMs and elevation data. It spans the International Organization for Standardization (ISO) protocols, the Open Geospatial Consortium (OGC) service architectures, legacy federal frameworks, embedded file-level specifications, and the rigorous positional accuracy reporting standards required by professional photogrammetric organizations.

## **1\. The Legacy Federal Framework: FGDC CSDGM**

In the United States, the historical baseline for geospatial metadata is the Federal Geographic Data Committee's Content Standard for Digital Geospatial Metadata (FGDC CSDGM), officially designated as FGDC-STD-001-1998.4 Mandated by Executive Order 12906 in the 1990s, the FGDC CSDGM dictated metadata practices for all federal agencies, establishing a uniform approach to describing geographic data. Though the FGDC officially endorsed the transition to international ISO standards in September 2010, the sheer volume of legacy elevation data, coupled with deeply entrenched institutional workflows, means the CSDGM remains highly prevalent in contemporary data distribution.7

### **1.1 Structural Organization of the CSDGM**

The CSDGM was developed by the Metadata Ad Hoc Working Group of the FGDC to define the information required by a prospective user to determine the availability of a set of geospatial data, its fitness for an intended use, the means of accessing it, and the mechanism for successfully transferring it.4 The standard is organized into a rigid hierarchy of eleven main sections, of which several are heavily utilized to describe elevation data.4

| CSDGM Section | Title | Primary Function for Elevation Data |
| :---- | :---- | :---- |
| **0** | Metadata | Defines the metadata document itself, its language, and the standard version used. |
| **1** | Identification Information | Contains the basic narrative description, abstract, spatial bounding coordinates, purpose, and thematic keywords. For DEMs, the abstract typically details the origin of the data (e.g., derived from airborne LiDAR) and the general geographic scope.4 |
| **2** | Data Quality Information | Houses the positional accuracy elements and the lineage record, detailing processing steps, source media, and scale.12 |
| **3** | Spatial Data Organization | Describes the mechanism used to represent spatial information, such as vector or raster models. For DEMs, this confirms the grid structure. |
| **4** | Spatial Reference Information | Explicitly defines the horizontal and vertical coordinate systems, map projections, datums, and ellipsoids used to position the data.4 |
| **5** | Entity and Attribute Information | Details the data dictionary. For a raster DEM, this section describes the pixel values, establishing that the floating-point or integer grid values correspond to physical elevation rather than another phenomenon like spectral reflectance.4 |
| **6** | Distribution Information | Provides information about the distributor, the formats available for transfer, and the process for obtaining the data. |
| **7** | Metadata Reference Information | Details the currentness of the metadata document and the responsible party for its maintenance. |
| **8** | Citation Information | A reusable compound element providing standardized bibliographic information about the dataset. |
| **9** | Time Period Information | A reusable compound element detailing the temporal validity or acquisition dates of the elevation data. |
| **10** | Contact Information | A reusable compound element identifying personnel or organizations associated with the data. |

### **1.2 Critical CSDGM Elements for Elevation Data**

Within the CSDGM, Section 2 (Data Quality Information) is critical for determining a DEM's fitness for use. It contains the posacc (Positional Accuracy) element, which is split into horizpa (Horizontal Positional Accuracy) and vertacc (Vertical Positional Accuracy).12 This is where the statistical error bounds of the elevation model are explicitly stated. Furthermore, the lineage element is utilized to narrate the sequence of events that produced the data.12 For modern elevation models, the lineage section is often exhaustive, detailing the specific filtering algorithms used to remove vegetation and buildings from the point cloud to create a bare-earth terrain model, as well as the hydro-flattening processes applied to lakes and wide rivers.

Section 4 (Spatial Reference Information) is equally vital. For US-based elevation data, this section typically dictates the horizontal datum, such as the North American Datum of 1983 (NAD 83), the vertical datum, almost universally the North American Vertical Datum of 1988 (NAVD 88\) for the contiguous United States, and the associated units of measure, specifying whether elevations are recorded in meters, international feet, or US Survey Feet.2 The reliance on text strings rather than standardized codes in this legacy standard often requires careful parsing to ensure correct georeferencing.

## **2\. The International Descriptive Framework: The ISO 19100 Series**

Recognizing the limitations of nationalized, flat-text metadata standards in an increasingly globalized and interoperable digital environment, the International Organization for Standardization (ISO) Technical Committee 211 (TC 211\) developed a suite of interconnected standards. For elevation data, this suite dictates how metadata is structured, encoded, and evaluated. The shift toward ISO standards represents a profound evolution from linear profiles to highly relational, object-oriented, and hierarchical models.16

### **2.1 ISO 19115-1: Metadata Fundamentals**

ISO 19115-1:2014, which superseded the original ISO 19115:2003 edition, defines the core schema required for describing geographic information and services.17 It establishes the fundamental packages and elements required to assess the dataset. In the context of elevation data, ISO 19115-1 provides foundational modules that handle spatial representation and reference systems through formalized codelists rather than free text.

The Identification Information package (MD\_DataIdentification) captures the spatial resolution, temporal extent, and basic thematic descriptors of the terrain data. The Spatial Representation package (MD\_SpatialRepresentation) is crucial for DEMs, as it defines the underlying grid topology. The MD\_CellGeometryCode code list specifically dictates how the elevation values map to the physical world, offering precise values. For instance, the point value indicates the elevation represents a specific node, area indicates the elevation represents the mathematical average of the entire grid cell, and voxel denotes a volumetric measurement on a regular grid in three-dimensional space.19

The Reference System package (MD\_ReferenceSystem) identifies the Coordinate Reference System (CRS). Unlike the FGDC CSDGM, which requires manual entry of projection parameters, ISO 19115-1 utilizes standardized identifiers, such as European Petroleum Survey Group (EPSG) codes, to definitively declare both the horizontal and vertical datums.5 This object-oriented approach significantly reduces ambiguity and data entry errors.

### **2.2 ISO 19115-2: Extensions for Imagery and Gridded Data**

Because the base ISO 19115-1 standard was primarily designed for discrete vector data and traditional maps, ISO 19115-2:2009 was developed to address the unique complexities of remotely sensed data, imagery, and continuous gridded surfaces like DEMs.16

The ISO 19115-2 extension introduces the MI\_Metadata root entity, which encompasses standard spatial metadata (MD\_Metadata) while appending critical packages for acquisition (instruments, platforms) and gridded lineage. This hierarchical and relational structure wraps both standard descriptive elements and gridded/acquisition extensions, making it the premier model for DEMs. This structural expansion fundamentally alters the metadata to capture the physical realities of sensor-based data acquisition and algorithmic processing.16

For elevation data derived from LiDAR, IfSAR, or aerial photogrammetry, ISO 19115-2 provides the Acquisition Information (gmi:acquisitionInformation) package. This allows data producers to systematically document the sensor type (e.g., an airborne laser scanner), the specific platform carrying the sensor (e.g., a fixed-wing aircraft or uncrewed aerial system), the flight line trajectories, and the operational conditions during the survey.16 Furthermore, ISO 19115-2 introduces robust lineage tracking (LI\_Lineage). While the FGDC CSDGM provided a single text block for lineage, ISO 19115-2 allows the metadata to algorithmically map the exact processing steps taken to transform raw point clouds into a bare-earth DEM, documenting the relationships between source datasets and the final derived grid.16

### **2.3 ISO 19157: Data Quality Encoding**

Elevation data is inherently statistical; every pixel contains an error margin relative to true ground. ISO 19157:2013, alongside its XML implementation ISO 19157-2, establishes the framework for describing geospatial data quality.18 Within this standard, the DQ\_QuantitativeResult class is paramount for the rigorous documentation of DEM accuracy.21

When a DEM undergoes a vertical accuracy assessment against survey-grade ground control points, the resulting statistical variance, typically expressed as Root Mean Square Error (![][image1]), is documented within the metadata using the DQ\_QuantitativeResult element. The XML path structure typically encapsulates the value type, the specific unit of measure (e.g., meters or feet), and the statistical method used to derive the error statistic.21 This granular structure allows automated parsing systems and web services to query the exact vertical and horizontal positional accuracy of a DEM programmatically, bypassing the need to read unstructured text reports to determine if a dataset is suitable for a specific engineering tolerance.

### **2.4 XML Implementation: ISO 19139**

While ISO 19115 and ISO 19157 define the conceptual data dictionaries and Unified Modeling Language (UML) models, ISO 19139:2007 provides the standardized Extensible Markup Language (XML) schema implementation required for software parsing.18 It defines the specific XML tags, namespaces, and nesting rules required to create a machine-readable document that validates against the standard.

The namespaces used in ISO 19139 clearly delineate the metadata components. For instance, gmd handles core geographic metadata, gco handles geographic common elements like character strings and integers, and gmi handles the specific extensions for imagery and gridded elevation data.16 Validating an elevation dataset's metadata involves running the XML document against the official ISO 19139 XSD schemas to ensure all mandatory elements, complex codelists, and conditional dependencies are satisfied, ensuring robust interoperability across different geographic information systems.16

## **3\. Crosswalking from FGDC CSDGM to ISO Standards**

The architectural philosophies of the legacy FGDC CSDGM and the modern ISO 19115 series are fundamentally different. The CSDGM is a monolithic, hierarchical document structure designed primarily for flat files and human readability. In stark contrast, ISO 19115 is highly object-oriented, heavily utilizing reusable elements, strict codelists, and definitive links to external registries.5 Organizations managing vast archives of elevation data face the significant operational challenge of crosswalking legacy metadata to the new standard.

For example, to define a spatial reference system in the FGDC CSDGM, a user must manually input the projection parameters, false eastings, false northings, and datum names as free text.13 In ISO 19115, the spatial reference is ideally linked via a single EPSG code using the MD\_ReferenceSystem element, shifting the burden of parameter definition to an authoritative external database maintained by the International Association of Oil & Gas Producers.5

Federal agencies, such as the Environmental Protection Agency (EPA) and the National Oceanic and Atmospheric Administration (NOAA), have developed extensive Extensible Stylesheet Language Transformations (XSLT) to crosswalk CSDGM XML files into ISO 19139-compliant XML.5 However, direct one-to-one mappings are often impossible due to the expanded granularity and strict relational rules of the ISO standards. The CSDGM, for instance, allows multiple disparate data formats to be grouped under a single distributor with loose associations, whereas ISO enforces strict, logical relationships between specific digital transfer options and specific file formats.8

![][image2]

## **4\. Operational Implementation: The USGS 3D Elevation Program**

The U.S. Geological Survey's (USGS) 3D Elevation Program (3DEP) is the most prominent domestic producer of high-resolution elevation data, tasked with maintaining a continuously updated, seamless topographic model of the nation. Despite the broad federal push toward ISO standards, 3DEP standard products are currently still documented primarily using the legacy FGDC CSDGM standard to maintain compatibility with decades of existing archives.4 Textual metadata is delivered in strict XML format, bundled alongside every downloadable DEM and source LiDAR dataset.4

However, recognizing the inherent limitations of searching and parsing millions of individual file-by-file XML metadata records, the USGS has innovated by delivering comprehensive "Spatial Metadata" alongside its gridded products.4

### **4.1 Work Unit Extent Spatial Metadata (WESM)**

The Work Unit Extent Spatial Metadata (WESM) is a transformative approach to metadata distribution, delivered as an OGC GeoPackage.27 The WESM acts as an index-level metadata database, containing explicit geospatial polygons that represent the exact footprints of elevation data collection projects. Rather than relying on text-based bounding boxes, users can interact with the metadata geographically. These polygons contain rigorous attribute schemas detailing the specific parameters of the source elevation data.

| WESM Attribute | Description regarding Elevation Data |
| :---- | :---- |
| workunit\_id | A unique identifier for the specific geographic collection block. |
| project\_id | The overarching identifier linking multiple work units to a single acquisition contract. |
| ql | The LiDAR Quality Level (e.g., QL0, QL1, QL2), dictating pulse density and vertical accuracy expectations. |
| p\_method | The precise processing method utilized to derive the terrain models. |
| horiz\_crs | The horizontal coordinate reference system applied to the specific work unit. |
| vert\_crs | The vertical coordinate reference system applied. |
| geoid | The specific geoid model used to convert theoretical ellipsoid heights into physical orthometric heights (e.g., GEOID12B, GEOID18).28 |

This spatial metadata approach bridges the critical gap between high-level catalog discovery and deep file-level assessment. It allows civil engineers, hydrologists, and GIS professionals to query elevation metadata geospatially within a GIS interface, instantly determining the acquisition dates, resolutions, and exact geoid models covering a specific watershed, rather than manually parsing thousands of individual XML files.27

## **5\. Embedded File-Level Metadata Specifications**

While catalog-level XML metadata, whether ISO or FGDC, is highly detailed, it is easily separated from the physical data file during transfer or processing. To ensure elevation data remains fundamentally self-describing, critical spatial metadata parameters must be embedded directly within the binary file headers of the data formats themselves.

### **5.1 GeoTIFF and Cloud Optimized GeoTIFF (COG) Metadata**

The most ubiquitous format for sharing raster DEMs is the GeoTIFF, which cleverly embeds geographic metadata into the highly established Tagged Image File Format (TIFF) architecture without breaking standard image viewers.29 Recognizing its global utility, the OGC formally standardized GeoTIFF in version 1.1.29

A DEM stored as a GeoTIFF utilizes a specific subset of reserved TIFF tags to geolocate the otherwise abstract array of elevation pixels to the surface of the Earth 32:

* **ModelPixelScaleTag**: Specifies the exact ground resolution of the DEM pixels in the chosen map units. For a high-resolution DEM, this might state that each pixel represents precisely 1 meter in the X dimension and 1 meter in the Y dimension.32  
* **ModelTiepointTag**: Anchors the raster matrix to the physical world, typically by mapping a specific pixel coordinate (usually the top-left pixel at 0,0) to a specific Easting and Northing coordinate in the projected space.32  
* **GeoKeyDirectoryTag**: This is the metadata nerve center of the GeoTIFF format. It contains an array of specialized "GeoKeys" that define the Coordinate Reference System (CRS). It systematically dictates the geographic or projected coordinate system, the mathematical ellipsoid, the geodetic datum, and the specific units of measurement for the elevation values.32

In recent years, the USGS 3DEP and NASA Earth Science Data Systems have migrated their standard DEM products to the Cloud Optimized GeoTIFF (COG) format.29 A COG is fundamentally a standard, backward-compatible GeoTIFF, but its internal metadata headers and image tiles are structurally rearranged. This structural optimization allows for HTTP range requests.29 Consequently, cloud computing environments can read the GeoTIFF metadata headers instantly over the internet and stream only the exact spatial subsets of elevation data required for an analysis, entirely bypassing the need to download massive regional DEMs in their multi-gigabyte entirety.29

### **5.2 The LAS and LAZ 1.4 Specifications for Point Clouds**

The LAS format, alongside its highly efficient compressed counterpart, LAZ, is the definitive industry-standard binary format for the exchange of three-dimensional point cloud data generated by LiDAR.36 Because point clouds serve as the foundational source material from which nearly all modern high-resolution DEMs are derived, their metadata standards are rigorously maintained by the American Society for Photogrammetry and Remote Sensing (ASPRS). The LAS 1.4 specification represents a massive structural leap in how elevation and sensor metadata is stored and managed.39

The LAS 1.4 binary file is structurally divided into four distinct payload areas, each serving a specific metadata or data storage function:

1. **Public Header Block**: This mandatory block contains the fundamental metadata required to parse the file. It includes the file signature (LASF), the system identifier, the generating software, the crucial scale factors (X, Y, and Z multipliers used to convert compressed integer point coordinates back into precise floating-point elevations), spatial offsets, and the overall spatial bounding box defined by the absolute minimum and maximum X, Y, and Z values.39  
2. **Variable Length Records (VLRs)**: Immediately following the header, VLRs are utilized to store variable types of metadata, including detailed projection information and user-defined application data. However, a significant limitation of standard VLRs is their strict maximum payload constraint of 65,535 bytes.40  
3. **Point Data Records**: This represents the core massive array of LiDAR points. LAS 1.4 supports complex Point Data Record Formats (PDRF) ranging from 0 through 10, with newer formats supporting extended classifications and near-infrared channels.39  
4. **Extended Variable Length Records (EVLRs)**: A critical architectural addition introduced in LAS 1.4, EVLRs are strategically placed at the *end* of the file. This allows them to accommodate a massive metadata payload that easily exceeds the 64-kilobyte limit of standard VLRs.39 EVLRs were primarily introduced to store massive waveform data packets alongside the discrete elevation points, ensuring the rawest form of sensor data travels seamlessly with the file without corrupting the standard parsing architecture.39

#### **The Critical Shift in CRS Encoding: From GeoTIFF to OGC WKT**

Perhaps the most significant metadata paradigm shift within the LAS 1.4 specification involves the encoding of the Coordinate Reference System (CRS).39

In legacy LAS versions (1.0 through 1.3), the CRS was encoded within the VLRs using the exact same GeoKeyDirectoryTag logic found in GeoTIFFs.41 While highly functional for simple 2D maps, GeoTIFF keys are occasionally ambiguous and struggle to fully and consistently represent complex, three-dimensional compound coordinate systems—systems that must simultaneously define a horizontal datum, a vertical datum, and a specific geoid model.

To resolve this ambiguity, LAS 1.4 introduced a mandate to use OGC Well-Known Text (WKT) to represent the CRS for all new Point Data Record Formats (PDRFs 6–10).39 WKT is an explicit, human-readable, and machine-parseable string format that definitively describes spatial reference systems without relying on obscure key registries. To maintain backwards compatibility while enforcing this new standard, a "WKT" bit was added to the Global Encoding flag in the Public Header Block. When this bit is set to true, modern parsing software ignores any legacy GeoTIFF VLRs that might be present and relies entirely on the WKT string for precise georeferencing.39

The USGS Lidar Base Specification enforces exceptionally strict metadata rules regarding this WKT implementation. The CRS must be declared as a COMPD\_CS (Compound Coordinate System), which explicitly wraps both the horizontal CRS (e.g., NAD83) and the vertical CRS.44 Furthermore, the specific geoid model used to convert theoretical ellipsoid heights into practical orthometric heights (e.g., GEOID18) must be explicitly appended to the VERT\_CS name field. This ensures absolute, zero-ambiguity vertical positioning across multi-state datasets.44

![][image3]

## **6\. OGC Service Standards for Dynamic Elevation Coverage**

While the ISO and FGDC standards primarily describe static datasets resting on physical disks, the Open Geospatial Consortium (OGC) defines the complex metadata and structural standards required to serve dynamic, multidimensional elevation data over the web. Elevation data, conceptually, is categorized as a "coverage"—a formal mathematical mapping of a spatial domain (a grid) to a range of values (elevations).46

### **6.1 Web Coverage Service (WCS) and Earth Observation Profile**

The OGC Web Coverage Service (WCS) 2.0 Interface Standard offers multi-dimensional coverage data for robust access over the Internet.47 Unlike a Web Map Service (WMS), which merely serves rendered, static images (essentially pictures of data), a WCS serves the actual raw elevation values, allowing the remote client software to perform complex spatial analysis on the terrain models without downloading the entire dataset.48

For global elevation data, the WCS 2.0 standard is frequently augmented by the Earth Observation Application Profile (EO-WCS).50 EO-WCS mandates highly specific metadata structures and service capabilities:

* **EO Metadata Set**: Each EO Coverage must contain a definitive metadata record describing the coverage at a high semantic level, including a mandatory WGS84 bounding box and a strict temporal validity extent, allowing for time-series terrain analysis.50  
* **Mandatory Extensions**: An elevation-focused WCS must support specific processing extensions. The *Range Subsetting Extension* allows users to request only the elevation band from a complex multi-band scientific coverage. The *Scaling Extension* enables real-time downsampling of DEM resolution over the web to save bandwidth, and the *CRS Service Model Extension* permits dynamically reprojecting the elevation data from the server's native CRS to the client's requested CRS.50

### **6.2 Coverage Implementation Schema (CIS)**

The Coverage Implementation Schema (CIS) 1.1 provides the concrete structural and metadata definitions for coverages served by WCS protocols.46 CIS 1.1 fundamentally advances the metadata encoding of elevation data by intelligently partitioning the coverage into distinct, manageable components: the Domain Set (which defines the spatial grid geometry), the Range Type (which contains metadata about the elevation values themselves, heavily leveraging the Sensor Web Enablement (SWE) Common DataRecord standard), and the Range Set (which contains the actual massive binary data values).46

This partitioning represents a sophisticated approach to metadata. It allows the relatively lightweight metadata components (Domain Set and Range Type) to be encoded in easily parseable, text-based formats like JSON or GML. Simultaneously, the heavy, multi-gigabyte elevation grid (Range Set) remains encoded in highly compressed binary formats like GeoTIFF or NetCDF.46 Furthermore, CIS 1.1 introduces comprehensive metadata handling for irregular grids and complex 3D/4D voxel models. This ensures that complicated structures, such as ungridded point clouds or time-series elevation arrays representing shifting sand dunes, can be accurately modeled, mathematically defined, and efficiently queried over the internet.

## **7\. NetCDF and Climate and Forecast (CF) Conventions**

While GeoTIFF and LAS heavily dominate the terrestrial mapping and engineering industries, the oceanographic, meteorological, and climate science communities overwhelmingly utilize the Network Common Data Form (NetCDF) for storing multidimensional elevation data, deep-ocean bathymetry, and complex geophysical models.29

NetCDF files achieve widespread interoperability through the rigorous, systematic application of the Climate and Forecast (CF) Metadata Conventions.52 The CF conventions dictate precisely how the attributes within the NetCDF file must be named and structured so that any compliant analysis software can instantly understand the spatial and physical dimensions of the data array, regardless of its origin.54

For elevation data, the CF conventions rely heavily on the standardized application of the standard\_name attribute.56 To unequivocally identify a grid of values as representing topographic elevation rather than atmospheric pressure or temperature, the variable must be tagged with standard\_name="surface\_altitude".57 Furthermore, the units attribute must be populated with a physically equivalent string recognizable by the Udunits software package (e.g., "m" for meters) to allow automated unit conversion during analysis.57

Crucially, the CF conventions explicitly address the immense mathematical complexities of vertical coordinate systems—an area where other formats often falter. The conventions systematically delineate between:

* **Dimensional Vertical Coordinates**: Where the vertical axis is defined by explicit, real-world physical units (e.g., meters above the geoid or feet below sea level).59  
* **Dimensionless Vertical Coordinates**: These are heavily used in complex ocean or atmospheric modeling (e.g., ocean sigma coordinates). Here, the vertical position of a grid cell is not static but is calculated dynamically based on a mathematical formula involving the underlying bathymetry or surface topography.55 The metadata explicitly stores the formula\_terms—the algebraic variables pointing to other data grids in the file—required to calculate the exact physical elevation at runtime.60

In modern CF implementations, complex spatial reference information is mapped using the grid\_mapping attribute. This attribute points to a specialized container variable holding detailed projection parameters, which is increasingly aligning with the OGC CRS WKT standard through the use of the crs\_wkt attribute, bridging the gap between atmospheric science formats and traditional GIS standards.57

## **8\. Positional Accuracy Reporting: The ASPRS Standards**

The most robust XML schema or cleanly formatted binary header is meaningless if the data it describes is fundamentally inaccurate. Metadata describing a DEM is functionally incomplete without a rigorous, standardized statistical statement of its positional accuracy. A user must definitively know the expected margin of error for any given elevation pixel to determine the dataset's fitness for use in critical life-safety applications, such as flood risk modeling, autonomous vehicle navigation, or aviation route planning. In North America, the definitive metadata guidelines for accuracy reporting are authored and maintained by the American Society for Photogrammetry and Remote Sensing (ASPRS).61

### **8.1 The Paradigm Shift from Edition 1 (2014) to Edition 2 (2023)**

For nearly a decade, the geospatial industry relied entirely on the *ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 1 (2014)*. However, as LiDAR technology rapidly evolved—yielding massive exponential increases in pulse density and intrinsic inertial measurement system accuracy—the 2014 standard became misaligned with operational realities in the field.64 In late 2023, ASPRS published Edition 2, which instituted sweeping, fundamental changes to how accuracy metadata is calculated, statistically evaluated, and ultimately reported.62

**Elimination of the 95% Confidence Level** The most critical and visible change in Edition 2 was the complete elimination of the 95% confidence level as a primary reporting metric.62 Previously, elevation metadata reports often included both the Root Mean Square Error (![][image1]) and a 95% confidence value. Because the 95% confidence metric is directly derived from the ![][image1] by applying a simple mathematical multiplier (assuming a normal, Gaussian error distribution), presenting both numbers generated widespread confusion among end-users. Non-expert users frequently misinterpreted them as independent accuracy tests, leading to flawed engineering assumptions.65

Under the 2023 standard, ![][image4] (Root Mean Square Error in the vertical dimension) is established as the sole, authoritative statistical term to express vertical accuracy in metadata reports, significantly simplifying the interpretation of error bounds.65

**Accuracy Classes and Checkpoint Requirements**

The accuracy of a DEM is empirically established by comparing the raster elevation values against a set of highly precise, independently surveyed ground control checkpoints. The 2023 standard fundamentally altered the physical and statistical requirements for these checkpoints:

1. **Increased Minimum Quantity**: The minimum number of checkpoints required to statistically validate a dataset was increased from 20 to 30\. This ensures a more robust statistical sample, mitigating the impact of a single anomalous survey point on the overall dataset evaluation.62  
2. **Relaxed Survey Accuracy Requirements**: Historically, field checkpoints had to be three to four times more accurate than the intended final DEM product. However, as DEM accuracies rapidly approached the 1-to-2 centimeter range, achieving checkpoints that were mathematically "three times better" using standard Real-Time Kinematic (RTK) GPS equipment became physically impossible and financially cost-prohibitive. Edition 2 relaxes this restrictive rule, but mandates that the inherent error of the survey checkpoints must now be mathematically integrated when computing the overall product accuracy (![][image5]). This ensures transparency regarding the limitations of the ground-truthing equipment itself.62

### **8.2 NVA, VVA, and Metadata Compliance Statements**

When evaluating elevation data, ASPRS standards require data producers to distinguish between two distinct vertical accuracy metrics, both of which must be thoroughly documented in the dataset's metadata:

1. **Non-vegetated Vertical Accuracy (NVA)**: This is evaluated in open terrain (e.g., bare soil, pavement, short grass) where LiDAR pulses easily and directly reach the ground. NVA represents the fundamental, best-case accuracy of the sensor and the processing workflow. The dataset *must pass* the defined NVA threshold to be deemed compliant.2  
2. **Vegetated Vertical Accuracy (VVA)**: This is evaluated in areas with obscuring land cover (e.g., tall brush, dense forests). VVA errors are typically much higher and more erratic than NVA because far fewer laser pulses successfully penetrate the canopy to strike the true ground surface. A critical methodological change in the 2023 standard is the removal of a strict "pass/fail" requirement for VVA. Instead, VVA is strictly evaluated and *reported* in the metadata as an informational metric. This acknowledges that dense vegetation causes highly variable error rates that should not outright fail an otherwise highly accurate sensor survey.2

To legally comply with the standard, a DEM's metadata—whether encoded in an ISO 19115 DQ\_DescriptiveResult text field or a legacy FGDC vertacc field—must include a highly specific, verbatim compliance statement. For example, the metadata must explicitly state: *"This data set was produced to meet ASPRS Positional Accuracy Standards for Digital Geospatial Data, Edition 2 (2023) for a \_\_(cm) ![][image4] vertical positional accuracy class."* 66

Furthermore, the ASPRS standard outlines explicit methodologies for calculating true 3D accuracy, which is highly relevant for raw point clouds and complex digital twins. The three-dimensional positional accuracy (![][image6]) is derived from combining the horizontal (![][image7]) and vertical (![][image8]) error components according to the mathematical formula 62:

![][image9]  
This specific metric provides a holistic, single-number assessment of volumetric spatial accuracy, which is increasingly required in metadata for smart-city modeling, autonomous vehicle simulation, and advanced infrastructure design where vertical and horizontal precision are equally critical.62

## **9\. Conclusion**

The thorough documentation of Digital Elevation Models and topographic data relies on an immensely complex, multi-tiered architecture of metadata standards. At the descriptive catalog level, the global geospatial community is irrevocably moving toward the object-oriented, hierarchical structures of ISO 19115-1, ISO 19115-2, and ISO 19157\. These frameworks provide the rigorous vocabularies and XML schemas necessary for international interoperability. However, massive institutional inertia—particularly within US Federal agencies maintaining historical archives—means the legacy FGDC CSDGM standard remains heavily embedded in existing data pipelines, necessitating complex XML crosswalk operations to bridge the modern interoperability gap.

Simultaneously, at the file level, structural metadata standards have rapidly modernized to support cloud-native computing paradigms and massively dense datasets. The transition of the LAS 1.4 specification to rely on OGC Well-Known Text (WKT) instead of legacy GeoTIFF tags ensures robust, unambiguous encoding of complex 3D coordinate systems. Concurrently, the CF Conventions provide rigorous semantic tagging mechanisms for advanced NetCDF arrays used in climate science. Finally, the modernization of ASPRS positional accuracy reporting—specifically the deprecation of confusing 95% confidence intervals in favor of precise ![][image4] reporting—ensures that the statistical reliability of elevation data is communicated clearly and effectively to end-users.

As the sheer volume of global elevation data explodes—fueled by national LiDAR mapping initiatives, drone proliferation, and high-resolution satellite arrays—the strict adherence to these harmonized metadata standards will dictate the successful automated discovery, processing, and application of topographic data on a global scale. Only through rigorous metadata standardization can a simple grid of numbers be confidently transformed into actionable intelligence.

#### **Works cited**

1. Accuracy Assessment of Digital Elevation Models (DEMs): A Critical Review of Practices of the Past Three Decades \- MDPI, accessed March 10, 2026, [https://www.mdpi.com/2072-4292/12/16/2630](https://www.mdpi.com/2072-4292/12/16/2630)  
2. 1-Meter Digital Elevation Model Specification \- USGS Publications Warehouse, accessed March 10, 2026, [https://pubs.usgs.gov/tm/11/b07/tm11-b7.pdf](https://pubs.usgs.gov/tm/11/b07/tm11-b7.pdf)  
3. Core Spatial Data Theme 'Elevation' Recommendation for Content \- UN-GGIM Europe, accessed March 10, 2026, [https://un-ggim-europe.org/wp-content/uploads/2019/09/UN-GGIM-Europe\_WGA\_Recommandation\_Content\_Theme\_EL\_v1.0.pdf](https://un-ggim-europe.org/wp-content/uploads/2019/09/UN-GGIM-Europe_WGA_Recommandation_Content_Theme_EL_v1.0.pdf)  
4. 3DEP Product Metadata | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/3dep-product-metadata](https://www.usgs.gov/ngp-standards-and-specifications/3dep-product-metadata)  
5. EPA Metadata Technical Specification | US EPA, accessed March 10, 2026, [https://www.epa.gov/geospatial/epa-metadata-technical-specification](https://www.epa.gov/geospatial/epa-metadata-technical-specification)  
6. Commonly Used Metadata Standards \- University of Idaho Library, accessed March 10, 2026, [https://www.lib.uidaho.edu/services/data/data-management/guide/documenting/standards/](https://www.lib.uidaho.edu/services/data/data-management/guide/documenting/standards/)  
7. FGDC/CSDGM (Federal Geographic Data Committee Content Standard for Digital Geospatial Metadata), accessed March 10, 2026, [https://rdamsc.bath.ac.uk/msc/m17](https://rdamsc.bath.ac.uk/msc/m17)  
8. Differences between ArcGIS metadata and FGDC metadata—ArcMap | Documentation, accessed March 10, 2026, [https://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/differences-between-arcgis-metadata-and-fgdc-metadata.htm](https://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/differences-between-arcgis-metadata-and-fgdc-metadata.htm)  
9. FGDC/CSDGM (Federal Geographic Data Committee Content Standard for Digital Geospatial Metadata), accessed March 10, 2026, [https://rd-alliance.github.io/metadata-directory/standards/fgdccsdgm-federal-geographic-data-committee-content-standard-digital-ge.html](https://rd-alliance.github.io/metadata-directory/standards/fgdccsdgm-federal-geographic-data-committee-content-standard-digital-ge.html)  
10. Illustrated guide to complete FGDC metadata \- ArcMap Resources for ArcGIS Desktop, accessed March 10, 2026, [https://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/illustrated-guide-to-complete-fgdc-metadata.htm](https://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/illustrated-guide-to-complete-fgdc-metadata.htm)  
11. Guidance for using the FGDC-CSDGM to Create System-level Metadata Records \- AWS, accessed March 10, 2026, [https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/BestPractices\_Systems-Level\_FGDC\_Metadata\_November2015\_508%20compliant.pdf](https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/BestPractices_Systems-Level_FGDC_Metadata_November2015_508%20compliant.pdf)  
12. Geospatial Metadata \- EDM \- ITRC, accessed March 10, 2026, [https://edm-1.itrcweb.org/geospatial-metadata/](https://edm-1.itrcweb.org/geospatial-metadata/)  
13. FGDC CSDGM Misinterpreted Elements and some helpful hints \- Forms & Applications, accessed March 10, 2026, [https://programs.iowadnr.gov/nrgislibx/metadata/FGDC\_CSDGM\_HelpfulHints.pdf](https://programs.iowadnr.gov/nrgislibx/metadata/FGDC_CSDGM_HelpfulHints.pdf)  
14. Geospatial Metadata Technical Specification Version 1.0 \- US EPA, accessed March 10, 2026, [https://19january2021snapshot.epa.gov/sites/static/files/2014-08/documents/epa\_geospatial\_metadata\_technical\_specification\_v1\_11\_2\_2007.pdf](https://19january2021snapshot.epa.gov/sites/static/files/2014-08/documents/epa_geospatial_metadata_technical_specification_v1_11_2_2007.pdf)  
15. 1/3rd arc-second Digital Elevation Models (DEMs) \- USGS National Map 3DEP Downloadable Data Collection, accessed March 10, 2026, [https://data.usgs.gov/datacatalog/data/USGS:3a81321b-c153-416f-98b7-cc8e5f0e17c3](https://data.usgs.gov/datacatalog/data/USGS:3a81321b-c153-416f-98b7-cc8e5f0e17c3)  
16. ISO 19115 Geographic information – Metadata Workbook, accessed March 10, 2026, [https://www.ncei.noaa.gov/sites/default/files/2020-04/ISO%2019115-2%20Workbook\_Part%20II%20Extentions%20for%20imagery%20and%20Gridded%20Data.pdf](https://www.ncei.noaa.gov/sites/default/files/2020-04/ISO%2019115-2%20Workbook_Part%20II%20Extentions%20for%20imagery%20and%20Gridded%20Data.pdf)  
17. ISO 19115 | DCC, accessed March 10, 2026, [https://www.dcc.ac.uk/resources/metadata-standards/iso-19115](https://www.dcc.ac.uk/resources/metadata-standards/iso-19115)  
18. Support for ISO metadata standards in ArcGIS Desktop—ArcMap | Documentation, accessed March 10, 2026, [https://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/support-for-iso-metadata-standards.htm](https://desktop.arcgis.com/en/arcmap/latest/manage-data/metadata/support-for-iso-metadata-standards.htm)  
19. ISO 19115 and 19115-2 CodeList Dictionaries \- ESIP Wiki, accessed March 10, 2026, [https://wiki.esipfed.org/ISO\_19115\_and\_19115-2\_CodeList\_Dictionaries](https://wiki.esipfed.org/ISO_19115_and_19115-2_CodeList_Dictionaries)  
20. 6.5 Metadata Requirements \- Caribbean Disaster Emergency Management Agency (CDEMA), accessed March 10, 2026, [https://www.cdema.org/virtuallibrary/index.php/charim-hbook/data-management-book/6-managing-geospatial-data/6-5-metadata-requirements](https://www.cdema.org/virtuallibrary/index.php/charim-hbook/data-management-book/6-managing-geospatial-data/6-5-metadata-requirements)  
21. Documenting In-Situ Data Using ISO 19115-2 \- AIXM.aero, accessed March 10, 2026, [https://aixm.aero/sites/default/files/imce/library/AIXM\_WXXM\_Conf\_2010/26\_day\_2\_-\_wx\_-\_06\_documenting\_in-situ\_data\_using\_iso\_19115.pdf](https://aixm.aero/sites/default/files/imce/library/AIXM_WXXM_Conf_2010/26_day_2_-_wx_-_06_documenting_in-situ_data_using_iso_19115.pdf)  
22. ISO 19115 Geographic Metadata Information | NASA Earthdata, accessed March 10, 2026, [https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/iso-19115-geographic-metadata-information](https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/iso-19115-geographic-metadata-information)  
23. Technical Guidance for the implementation of INSPIRE dataset and service metadata based on ISO/TS 19139:2007 \- GitHub Pages, accessed March 10, 2026, [https://inspire-mif.github.io/technical-guidelines/metadata/metadata-iso19139/metadata-iso19139.html](https://inspire-mif.github.io/technical-guidelines/metadata/metadata-iso19139/metadata-iso19139.html)  
24. ISO Data Quality \- Earth Science Information Partners (ESIP), accessed March 10, 2026, [https://wiki.esipfed.org/ISO\_Data\_Quality](https://wiki.esipfed.org/ISO_Data_Quality)  
25. 103 Digital Geographic Information Exchange Standard (DIGEST) Metadata Profile of ISO 19115 and ISO 19139 \- DGIWG Portal, accessed March 10, 2026, [https://portal.dgiwg.org/files/5441](https://portal.dgiwg.org/files/5441)  
26. 3D Elevation Program Standards and Specifications | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/3d-elevation-program-standards-and-specifications](https://www.usgs.gov/ngp-standards-and-specifications/3d-elevation-program-standards-and-specifications)  
27. 3DEP Spatial Metadata | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/3d-elevation-program/3dep-spatial-metadata](https://www.usgs.gov/3d-elevation-program/3dep-spatial-metadata)  
28. WESM Data Dictionary | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/wesm-data-dictionary](https://www.usgs.gov/ngp-standards-and-specifications/wesm-data-dictionary)  
29. GeoTIFF \- NASA Earthdata, accessed March 10, 2026, [https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/geotiff](https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/geotiff)  
30. The Ultimate List of GIS Formats and Geospatial File Extensions, accessed March 10, 2026, [https://gisgeography.com/gis-formats/](https://gisgeography.com/gis-formats/)  
31. DGIWG 907 Imagery & Gridded Data Roadmap, accessed March 10, 2026, [https://portal.dgiwg.org/files/73255](https://portal.dgiwg.org/files/73255)  
32. GeoTIFF for Beginners: Format, Features & Benefits, accessed March 10, 2026, [https://www.lizardtech.com/post/geotiff-for-beginners-format-features-benefits](https://www.lizardtech.com/post/geotiff-for-beginners-format-features-benefits)  
33. 2.7.2 GeoTIFF GeoKeys for Geocoding, accessed March 10, 2026, [http://geotiff.maptools.org/spec/geotiff2.7.html](http://geotiff.maptools.org/spec/geotiff2.7.html)  
34. OGC GeoTIFF Standard, accessed March 10, 2026, [https://docs.ogc.org/is/19-008r4/19-008r4.html](https://docs.ogc.org/is/19-008r4/19-008r4.html)  
35. Elevation GeoTIFF Part 1 – Shaded Relief \- GitHub Pages, accessed March 10, 2026, [https://gwlucastrig.github.io/GridfourDocs/notes/ElevationGeoTiff1.html](https://gwlucastrig.github.io/GridfourDocs/notes/ElevationGeoTiff1.html)  
36. What types of elevation datasets are available, what formats do they come in, and where can I download them? | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/faqs/what-types-elevation-datasets-are-available-what-formats-do-they-come-and-where-can-i-download](https://www.usgs.gov/faqs/what-types-elevation-datasets-are-available-what-formats-do-they-come-and-where-can-i-download)  
37. accessed December 31, 1969, [https://www.asprs.org/wp-content/uploads/2019/03/LAS\_1\_4\_r14.pdf](https://www.asprs.org/wp-content/uploads/2019/03/LAS_1_4_r14.pdf)  
38. LAZ Specification 1.4 \- rapidlasso GmbH, accessed March 10, 2026, [https://downloads.rapidlasso.de/doc/LAZ\_Specification\_1.4\_R1.pdf](https://downloads.rapidlasso.de/doc/LAZ_Specification_1.4_R1.pdf)  
39. Open Geospatial Consortium LAS Specification 1.4 OGC Community Standard, accessed March 10, 2026, [https://portal.ogc.org/files/?artifact\_id=74523](https://portal.ogc.org/files/?artifact_id=74523)  
40. LAS (LASer) File Format, Version 1.4 \- The Library of Congress, accessed March 10, 2026, [https://www.loc.gov/preservation/digital/formats/fdd/fdd000418.shtml](https://www.loc.gov/preservation/digital/formats/fdd/fdd000418.shtml)  
41. Understand the LAS coordinate system—ArcGIS Pro | Documentation, accessed March 10, 2026, [https://pro.arcgis.com/en/pro-app/latest/help/analysis/3d-analyst/understand-las-coordinate-system.htm](https://pro.arcgis.com/en/pro-app/latest/help/analysis/3d-analyst/understand-las-coordinate-system.htm)  
42. LAS Specification 1.4 \- R15 \- Paul Bourke, accessed March 10, 2026, [https://paulbourke.net/dataformats/laz/LAS\_1\_4\_r15.pdf](https://paulbourke.net/dataformats/laz/LAS_1_4_r15.pdf)  
43. \[solved\] Georeferencing LAS file for ION \- Cesium Community, accessed March 10, 2026, [https://community.cesium.com/t/solved-georeferencing-las-file-for-ion/14402](https://community.cesium.com/t/solved-georeferencing-las-file-for-ion/14402)  
44. Lidar Base Specification 2025 rev. A \- AWS, accessed March 10, 2026, [https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/Lidar-Base-Specification-2025-rev-A.docx](https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/files/Lidar-Base-Specification-2025-rev-A.docx)  
45. Lidar Base Specification: Data Processing and Handling Requirements \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-data-processing-and-handling-requirements](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-data-processing-and-handling-requirements)  
46. OGC® Coverage Implementation Schema, accessed March 10, 2026, [https://docs.ogc.org/is/09-146r6/09-146r6.html](https://docs.ogc.org/is/09-146r6/09-146r6.html)  
47. OGC WCS Standard | Web Coverage Service Specification, accessed March 10, 2026, [https://www.ogc.org/standards/wcs/](https://www.ogc.org/standards/wcs/)  
48. WCS \-- OGC Web Coverage Service — GDAL documentation, accessed March 10, 2026, [https://gdal.org/en/stable/drivers/raster/wcs.html](https://gdal.org/en/stable/drivers/raster/wcs.html)  
49. WCS Server — MapServer 8.6.0 documentation, accessed March 10, 2026, [https://mapserver.org/ogc/wcs\_server.html](https://mapserver.org/ogc/wcs_server.html)  
50. Open Geospatial Consortium \- the OGC Portal, accessed March 10, 2026, [https://portal.ogc.org/files/42722](https://portal.ogc.org/files/42722)  
51. GTiff \-- GeoTIFF File Format — GDAL documentation, accessed March 10, 2026, [https://gdal.org/en/stable/drivers/raster/gtiff.html](https://gdal.org/en/stable/drivers/raster/gtiff.html)  
52. Climate and Forecast Metadata Conventions \- NASA Earthdata, accessed March 10, 2026, [https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/climate-forecast-metadata-conventions](https://www.earthdata.nasa.gov/about/esdis/esco/standards-practices/climate-forecast-metadata-conventions)  
53. NetCDF and CF \- The Basics | Unidata Python Training, accessed March 10, 2026, [https://unidata.github.io/python-training/workshop/CF%20Conventions/netcdf-and-cf-the-basics/](https://unidata.github.io/python-training/workshop/CF%20Conventions/netcdf-and-cf-the-basics/)  
54. NetCDF Climate and Forecast (CF) Metadata Conventions, accessed March 10, 2026, [https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9/cf-conventions.html](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.9/cf-conventions.html)  
55. NetCDF Climate and Forecast (CF) Metadata Conventions, accessed March 10, 2026, [https://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html](https://cfconventions.org/cf-conventions/v1.6.0/cf-conventions.html)  
56. The CF Metadata Convention \- Centre for Environmental Analysis (CEDA) Help Docs Site, accessed March 10, 2026, [https://help.ceda.ac.uk/article/4507-the-cf-metadata-convention](https://help.ceda.ac.uk/article/4507-the-cf-metadata-convention)  
57. NetCDF Climate and Forecast (CF) Metadata Conventions, accessed March 10, 2026, [https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.pdf](https://cfconventions.org/Data/cf-conventions/cf-conventions-1.13/cf-conventions.pdf)  
58. CF Standard Name Table \- CF Conventions, accessed March 10, 2026, [https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html](https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html)  
59. NetCDF Climate and Forecast (CF) Metadata Conventions, accessed March 10, 2026, [https://cfconventions.org/cf-conventions/cf-conventions.html](https://cfconventions.org/cf-conventions/cf-conventions.html)  
60. Standard Vertical Transforms \- NSF Unidata Software Documentation, accessed March 10, 2026, [https://docs.unidata.ucar.edu/netcdf-java/4.6/userguide/reference/StandardVerticalTransforms.html](https://docs.unidata.ucar.edu/netcdf-java/4.6/userguide/reference/StandardVerticalTransforms.html)  
61. Consolidated Standardized Survey-Grade Checkpoints 3DEP 2004 to 2025 (ver. 2.0, December 2025\) | USGS Science Data Catalog \- USGS.gov, accessed March 10, 2026, [https://data.usgs.gov/datacatalog/data/USGS:67075e6bd34e969edc59c3e7](https://data.usgs.gov/datacatalog/data/USGS:67075e6bd34e969edc59c3e7)  
62. The ASPRS Positional Accuracy Standards, Edition 2: The Geospatial Mapping Industry Guide to Best Practices, accessed March 10, 2026, [https://my.asprs.org/Common/Uploaded%20files/PERS/HLA/HLA%202023-10-1.pdf](https://my.asprs.org/Common/Uploaded%20files/PERS/HLA/HLA%202023-10-1.pdf)  
63. Positional Accuracy Standards \- ASPRS, accessed March 10, 2026, [https://asprs.org/Main/Main/Standards/Positional-Accuracy-Standards.aspx](https://asprs.org/Main/Main/Standards/Positional-Accuracy-Standards.aspx)  
64. ASPRS Positional Accuracy Standards for Digital Geospatial Data CONTENTS \- AAGS, accessed March 10, 2026, [https://aagsmo.org/wp-content/uploads/2023/03/ASPRS\_PosAcc\_Edition2\_MainBody.pdf](https://aagsmo.org/wp-content/uploads/2023/03/ASPRS_PosAcc_Edition2_MainBody.pdf)  
65. Dr. Riadh Munjy \- sopac, accessed March 10, 2026, [http://sopac-csrc.ucsd.edu/wp-content/uploads/2024/02/ASPRS-Accuracy-Standards-2023\_munjy.pdf](http://sopac-csrc.ucsd.edu/wp-content/uploads/2024/02/ASPRS-Accuracy-Standards-2023_munjy.pdf)  
66. Adopt updated accuracy standards | U.S. Geological Survey \- USGS.gov, accessed March 10, 2026, [https://www.usgs.gov/ngp-standards-and-specifications/adopt-updated-accuracy-standards](https://www.usgs.gov/ngp-standards-and-specifications/adopt-updated-accuracy-standards)  
67. ASPRS Positional Accuracy Standards for Digital Geospatial Data, accessed March 10, 2026, [https://my.asprs.org/Common/Uploaded%20files/PERS/HLA/HLA%202023-10-2.pdf](https://my.asprs.org/Common/Uploaded%20files/PERS/HLA/HLA%202023-10-2.pdf)

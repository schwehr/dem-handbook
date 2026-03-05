Outline from Gemini

# Prompt

Create an outline of a DEM handbook. Cover everything from Geodesy, Projections, GNSS, the many ways of measuring the shape of the earth (including levelling lines, sonar, radar / SAR, lidar, lead lines, computer vision, interferometric, occlusion, seismology, predicted bathymetry, satellite image bathymetry, etc; how opaque or transparent each technique is to various materials) and where the sensor is (underwater, on the sea surface, underground, in the air, or in space), measuring gravity, measuring time, vertical and tidal datums, ways to store the data (points, full waveform, tins, DEMs, polygons, gaussian splats, etc.), DTMs versus DSMs, how the shape of the earth changes over time and the range of time scales (plate motion models, earthquake deformation), how we track changes over time, how to we understand the error in DEMs, how are multiple types of elevation products integrated together, how do we calibrate and check DEMs (CORS stations, Tide Gauges, bench marks, etc.).

# Response:

This is a massive and fascinating scope for a handbook\! You are touching on everything from the deep physics of the Earth to cutting-edge computer graphics techniques.

Here is a comprehensive, logically structured outline for your Digital Elevation Model (DEM) Handbook, organized to take a reader from the fundamental physics of the Earth, through data collection and storage, to analysis and quality control.

---

## **The Comprehensive DEM Handbook: From Gravity to Gaussian Splats**

### **Part 0: Introduction&&

* **0.1 What is a Digital Elevation Model (DEM)?**
* **0.2 The major uses of DEMs**

### **Part 1: The Foundations of Earth Measurement**

Before we can model the Earth's surface, we must understand its underlying physical properties and how we define space and time.

* **1.1 Geodesy & The Shape of the Earth**
  * The true shape of the Earth: Sphere, Ellipsoid, and Geoid.
  * Measuring Gravity: Gravimeters, satellite gravity missions (GRACE, GOCE), and how gravity anomalies define the Geoid.
  * Measuring Time: Atomic clocks, relativistic effects, and why precise timekeeping is the bedrock of spatial measurement.
* **1.2 Global Navigation Satellite Systems (GNSS)**
  * How GNSS works: Constellations (GPS, GLONASS, Galileo), signals, and trilateration.
  * Positioning techniques: PPP, RTK, PPK, and network adjustments.
  * Encoding systems: NMEA, Rinex, Binex.
  * GNSS Receiver hardware: Options and tradeoffs.
  * Continuously Operating Reference Station (CORS) Network
  * Other location systems: Radio beacons, Wifi, Bluetooth, Celltowers, LORAN, etc.
  * Intertial Navigation Systems (INS): Dead reckoning and improving other systems.
* **1.3 Coordinate Reference Systems & Projections**
  * Geographic vs. Projected coordinate systems.
  * Distortion in projections (conformal, equal-area, equidistant) and choosing the right one for your DEM.
* **1.4 Understanding Datums**
  * Horizontal Datums: NAD83, WGS84, ITRF.
  * Vertical Datums: Orthometric heights (NAVD88) vs. Ellipsoidal heights. EGM96 versus EGM2008.
  * Tidal Datums: MLLW, MSL, HAT, and the complexity of the coastal transition zone.
  * Datum transformations and Geoid models.

---

### **Part 2: Sensors and Data Acquisition**

This section covers *where* the sensors are placed and *how* they interact with the physical world.

* **2.1 Sensor Platforms (The "Where")**
  * **Spaceborne:** Satellites (global coverage, lower resolution).
  * **Airborne:** Fixed-wing, helicopters, UAVs/drones.
  * **Surface (Land & Sea):** Survey vehicles, tripods, ships, uncrewed surface vessels (USVs).
  * **Underwater:** Submarines, ROVs, AUVs.
  * **Underground:** Borehole sensors, subterranean mapping robots.
* **2.2 Measurement Techniques (The "How")**
  * **Physical & Mechanical:**
    * Traditional Levelling Lines and Theodolites.
    * Lead Lines (historical and shallow bathymetry).
  * **Acoustic (Sounding):**
    * Sonar: Singlebeam vs. Multibeam echo sounders.
    * Seismology: Using seismic waves to map deep underground strata and the seafloor.
  * **Optical & Laser:**
    * Lidar (Light Detection and Ranging): Topographic (near-infrared) and Bathymetric (green laser).
    * Computer Vision: Photogrammetry, Structure from Motion (SfM), and stereo imagery.
  * **Radar & Microwave:**
    * SAR (Synthetic Aperture Radar) and Radar Altimetry.
    * Interferometric SAR (InSAR): Using phase differences for ultra-precise elevation.
  * **Derived, Modeled & Passive:**
    * Predicted Bathymetry: Deriving seafloor shape from satellite gravity anomalies.
    * Satellite-Derived Bathymetry (SDB): Using multispectral imagery to estimate depth based on light attenuation.
    * Shape from Occlusion/Shadows: Deriving height from shadow length in imagery.
* **2.3 Sensor-Material Interaction Matrix**
  * *How opaque or transparent each technique is to its environment.*

| Sensor Type | Earth/Rock | Vegetation | Water (Clear) | Water (Turbid) | Clouds/Weather |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **Topo Lidar (NIR)** | Opaque (Hits surface) | Semi-transparent | Opaque (Absorbed) | Opaque | Opaque |
| **Bathy Lidar (Green)** | Opaque | Semi-transparent | Transparent | Semi-transparent | Opaque |
| **Photogrammetry** | Opaque | Opaque (Models canopy) | Semi-transparent | Opaque | Opaque |
| **Radar/InSAR** | Opaque | Semi-transparent (Band-dependent) | Opaque (Reflects) | Opaque (Reflects) | Transparent |
| **Sonar** | Opaque | N/A | Transparent | Transparent | N/A |

---

### **Part 3: Data Representation and Storage**

Once we measure the Earth, how do we digitally reconstruct and store it?

* **3.1 Core Elevation Concepts**
  * **DTM (Digital Terrain Model):** Bare earth.
  * **DSM (Digital Surface Model):** Includes buildings, canopy, and features.
  * **CHM (Canopy Height Model):** DSM minus DTM.
* **3.2 Data Structures and Storage Formats**
  * **Point Clouds:** LAS/LAZ files, spatial indexing (Octrees).
  * **Full Waveform Data:** Storing the entire returning light/sound pulse for complex structural analysis.
  * **TINs (Triangulated Irregular Networks):** Variable resolution vector models.
  * **Rasters / Gridded DEMs:** GeoTIFFs, Cloud Optimized GeoTIFFs (COGs), NetCDF.
  * **Polygons & Contours:** Traditional vector representations (Shapefiles, GeoJSON).
  * **Emerging Tech:** 3D Gaussian Splatting and Neural Radiance Fields (NeRFs) for high-fidelity, view-dependent surface reconstruction.

---

### **Part 4: The Dynamic Earth (Temporal Changes)**

The Earth's surface is not static. This section covers how we model and track an ever-changing landscape.

* **4.1 Time Scales of Deformation**
  * **Geological & Tectonic:** Plate motion models (e.g., tectonic drift, glacial isostatic adjustment).
  * **Episodic & Catastrophic:** Earthquake deformation, volcanic inflation/deflation, landslides.
  * **Anthropogenic & Environmental:** Subsidence (groundwater extraction), coastal erosion, sea-level rise, open-pit mining.
* **4.2 Tracking and Modeling Change**
  * 4D mapping (Time as the 4th dimension).
  * DEM of Difference (DoD): Subtracting temporally distinct DEMs to calculate volumetric change (cut/fill).
  * Time-series InSAR for millimeter-level subsidence tracking.

---

### **Part 5: Quality, Calibration, and Integration**

A DEM is only as good as its measurable accuracy and its interoperability with other data.

* **5.1 Calibration and Ground Truth**
  * **CORS Stations:** Continuously Operating Reference Stations for GNSS correction.
  * **Tide Gauges:** Anchoring bathymetric surveys to real-world water levels.
  * **Benchmarks & Geodetic Control Networks:** Physical monuments used for vertical tying and levelling.
* **5.2 Understanding DEM Error**
  * Types of error: Systematic (bias), Random (noise), and Blunders.
  * Metrics of uncertainty: RMSE (Root Mean Square Error), CE90 (Circular Error 90%), LE90 (Linear Error 90%).
  * Spatially variable uncertainty: How slope, land cover, and sensor geometry affect local accuracy.
* **5.3 Integration and Conflation**
  * Stitching DEMs together: Mosaicking, feathering, and edge-matching.
  * Fusing diverse modalities (e.g., merging near-shore bathymetric Lidar with deep-water Sonar and terrestrial photogrammetry).
  * Datum harmonization: seamless translation across the land-sea boundary (using tools like VDatum).

### **Glossary**

### Topics to merge in.

What are the open source packages related to DEMs?
 * Chapter on contours
 * What can I take from the cat a book?
 * Gravity and gravity anomalies
 * Bathymetry
   * Single beam
   * Multi beam
   * Interferometric
   * Bathy-lidar
   * The water column and ray casting
   * Survey to ellipsoid or survey to a tidal datum
 * Drone surveys
 * Built strictures
 * Definitions of building representations. And building heights
 * Issues
 * Techniques
 * Antennas, wires/power lines, and other thin structures
 * Bridges
 * These things move. Wind. Sagging lines from heat
 * What gets included or excluded from a DSM
 * The elevation of vegetation
 * Local verses regional versus global DEMs- how does that impact things?
 * The history of USGS DEM and Topo products.
 * How do neighboring representations align or not?
 * Metadata - How to keep track of collection and processing?
 * Car / streetview style collection especially in urban canyons
 * Key algorithms that need to be worked in
   * Ransac
 * References
   * What are the key reference about DEMs?
   * Background / context
     * https://github.com/schwehr/gis-history
 * Legal issues and concerns with DEMs?
 * Mining
   * Surface
   * Underground
 * Earth layers as DEMs
 * Process that change the shape of the surface
   * Plate tectonics
   * Permafrost thaw
   * Earthquakes
   * Ground water
   * Ice motion
   * Landslides and slumps
   * Humans
   * Wildlife
   * Ice
 * Sea and water surface w.r.t. DEMs
 

# Chapter 47 — File formats: LAS/LAZ/COPC, GeoTIFF/COG, BAG/S-102, NetCDF/Zarr, DTED, and the rest

> **Part X — Representing, storing, finding, and keeping elevation data.** The chapter about the bytes: how the data models of [Chapter 46](ch46-data-models.md) are actually encoded, which semantics each encoding can and cannot carry, and the errors that formats themselves introduce.

**In this chapter.** A file format is a link in the measurement chain, and a weak one: it can quantize, truncate, drop the vertical datum, shift the grid by half a cell, or redefine what a number means on the way out the door. You will be able to read the LAS 1.4 header and know what the point data record format, scale/offset, and VLRs imply about precision and georeferencing; explain what LAZ, COPC, and EPT add; read GeoTIFF GeoKeys for horizontal and vertical CRS and pixel convention and decide whether a file is a valid COG; interpret the integer encodings of DTED and SRTM and the compound encodings of BAG and S-102, including what each uncertainty layer means; choose chunking for NetCDF and Zarr; and recognize the formats that carry no CRS at all. You will compute format-induced errors—quantization at $q/\sqrt{12}$, float32 precision at large coordinates, LERC and Terrain-RGB bounds—and run the validators (`pdal info`, `lasvalidate`, `gdalinfo`, `rio cogeo validate`) that should gate every receipt and delivery.

## 47.1 Point formats

### 47.1.1 ASPRS LAS 1.0–1.4

**LAS** is the exchange format for lidar point clouds, maintained by ASPRS since 1.0 (2003). A LAS file is a public header block, a sequence of **variable-length records** (VLRs), the point records, and (since 1.4) **extended VLRs** (EVLRs) after the points. The header declares the version, the **point data record format** (PDRF), the record length, point counts (64-bit in 1.4; the legacy 32-bit fields must be zero when counts exceed them), the per-axis **scale factors and offsets**, and the bounding box.

Coordinates are stored as signed 32-bit integers and reconstructed as $X = x_{\text{rec}} \cdot s_x + o_x$. The scale is the quantization step: 0.01 m is conventional, 0.001 m is common for terrestrial scans, and the 1 m scale that occasionally appears from careless export destroys the data. The offset exists so that the integer range ($\pm 2.1\times10^9$) covers the coordinates; with scale 0.001 the span is only ±2 147 km, which fails for geographic coordinates in degrees (scale 10⁻⁷ degrees is the usual choice there, about 1 cm) and for projected coordinates without an offset.

The PDRFs define what each point record contains:

| PDRF | Added in | Contents beyond XYZ, intensity, returns, class, scan angle, user data, source ID |
|---|---|---|
| 0 | 1.0 | Base record; 8-bit scan angle; 5-bit class + 3 flag bits |
| 1 | 1.0 | + GPS time (double) |
| 2 / 3 | 1.2 | + RGB / + GPS time and RGB |
| 4 / 5 | 1.3 | PDRF 1 / 3 + waveform packet descriptor fields |
| 6 | 1.4 | Redesigned base: 16-bit scan angle (0.006° units), 8-bit class (256 values), 4-bit return counts, scanner channel (2 bits), overlap flag, GPS time mandatory |
| 7 / 8 | 1.4 | PDRF 6 + RGB / + RGB and NIR |
| 9 / 10 | 1.4 | PDRF 6 / 8 + waveform packets |

The 1.4 **classification flags** (synthetic, key-point, withheld, overlap) are distinct from the class value, and "withheld" is the mechanism by which noise is retained but excluded—software that ignores the flag resurrects every bird. The **global encoding** bits declare whether GPS time is GPS week seconds or **adjusted standard GPS time** (GPS seconds minus 10⁹); mixing the two produces timestamps that are off by decades and strip adjustment that silently fails ([Chapter 6](ch06-time-as-coordinate.md)). The CRS lives in VLRs: GeoTIFF keys (user ID `LASF_Projection`, records 34735–34737) for PDRFs 0–5, and **OGC WKT** (record 2112) mandatory for PDRFs 6–10. Nothing forces the vertical CRS to be present or correct in either; most LAS files carry a horizontal CRS and an implied, undeclared vertical one. **Extra bytes** (record ID 4) describe additional per-point fields with name, type, scale, offset, and nodata—the mechanism for per-point uncertainty, water-surface height, and the topo-bathy domain profile's attributes ([Chapter 19](ch19-bathymetric-lidar.md)).

### 47.1.2 LAZ

**LAZ** (Isenburg 2013) is lossless compression of LAS: points are grouped into chunks (50 000 by default), each compressed with arithmetic coding of predicted residuals—coordinates predicted from the previous point, GPS time from a running delta, and so on. Typical ratios are 5–10× for airborne data. Because chunks are independently decodable, LAZ supports random access at chunk granularity, which is what COPC exploits. LAZ is bit-exact with the source LAS; decompressed values are identical. The only loss paths are tools that re-scale on write. Esri's closed `.zLAS` should be avoided for exchange.

### 47.1.3 COPC and EPT

**Entwine Point Tiles** (EPT) organizes a cloud into an octree of LAZ (or binary/Zstandard) files in a directory with a JSON hierarchy. **COPC** (Cloud Optimized Point Cloud, 2021) places the same octree inside a single LAZ 1.4 file: PDRF 6–8 only, a `copc` info VLR giving the root cube and spacing, each octree node as one LAZ chunk, and a hierarchy EVLR listing node keys $(\text{level}, x, y, z)$ with byte offsets and point counts. A client fetches the header and hierarchy with two HTTP range requests and then only the nodes its view needs. Both subsample points into coarse nodes, so a partial traversal is a thinned cloud ([Chapter 46](ch46-data-models.md)); both are lossless when traversed fully. COPC is now the preferred lidar format for cloud archives (USGS 3DEP on AWS).

### 47.1.4 E57, PLY/PCD/PTX, and ASCII

**E57** (ASTM E2807-11) targets terrestrial and mobile scanning: multiple scans per file, each with its pose, optional structured (row/column) layout, images, and per-scan metadata, in an XML-plus-binary container with CRC-protected pages. It preserves the organization that LAS discards. **PLY** and **OBJ** are mesh/point formats with arbitrary attributes and no CRS field; **PCD** (Point Cloud Library) and **PTX** (Leica) are similar, PTX with a scanner pose matrix. **ASCII XYZ**—space- or comma-delimited text—is the format of last resort: no CRS, no declared units, no attribute schema, decimal precision at the whim of the writer (a printf with `%.2f` is 1 cm quantization; `%g` is six significant figures, which is 1 m precision at 7-digit northings), and file sizes 3–5× LAS. Every ASCII delivery needs a sidecar stating CRS, units, column order, and precision; most do not have one.

> **Worked example.** *The scale that ate the survey.* A terrestrial scan with 0.5 mm ranging precision is exported to LAS with the default scale of 0.01 m. The quantization error is uniform on ±5 mm with $\sigma = 0.01/\sqrt{12} = 2.9$ mm—six times the instrument precision, applied independently to each axis. The same cloud exported to ASCII with `%.3f` keeps 0.29 mm; re-imported and written with scale 0.01, it is back to 2.9 mm. Set scale to 0.001 m (or finer) for terrestrial work and verify with `pdal info --metadata` that it survived every hop.

## 47.2 Raster formats

### 47.2.1 GeoTIFF 1.1 and its keys

**GeoTIFF** embeds georeferencing in TIFF tags: `ModelPixelScale` and `ModelTiepoint` (or `ModelTransformation`) for the affine, and a `GeoKeyDirectory` of **GeoKeys** for the CRS. Version 1.0 (Ritter and Ruth 1995, 1997) was a community specification; **OGC GeoTIFF 1.1** (19-008r4, 2019) formalized it and clarified the vertical keys. The keys that matter for elevation:

- `GTModelTypeGeoKey` (1024): projected, geographic, or geocentric.
- `GTRasterTypeGeoKey` (1025): **RasterPixelIsArea** (1) or **RasterPixelIsPoint** (2). Under PixelIsArea the tiepoint refers to the outer corner of the cell; under PixelIsPoint, to its centre. GDAL honours the key and reports the corner-based extent either way, which is correct but confuses people comparing extents.
- `ProjectedCRSGeoKey` (3072) / `GeodeticCRSGeoKey` (2048): EPSG codes, or 32767 (user-defined) with citation and parameter keys.
- `VerticalGeoKey` (4096), `VerticalCitationGeoKey` (4097), `VerticalDatumGeoKey` (4098), `VerticalUnitsGeoKey` (4099): the vertical CRS, for example EPSG 5703 (NAVD88 height). GeoTIFF 1.1 permits them; nothing requires them, and most DEMs omit them. A vertical key names the datum but not the **geoid model** used to realize it—GEOID12B and GEOID18 differ by centimetres over most of the conterminous United States, and locally by more—so even a complete GeoTIFF needs metadata text for the realization ([Chapter 9](ch09-vertical-datums.md)).

Nodata is a GDAL tag (`GDAL_NODATA`, 42113), not a GeoTIFF key, and other software may ignore it. Internal tiling and overviews are TIFF features that GeoTIFF inherits.

### 47.2.2 Cloud Optimized GeoTIFF

A **COG** (OGC 21-026, 2023) is a GeoTIFF whose layout permits efficient HTTP range reads: internally tiled, with overviews, and with the image file directories (IFDs) and tile offsets at the start so a client can read the header once and then fetch only the tiles it needs. A COG is a valid GeoTIFF; a GeoTIFF is not necessarily a COG. Overviews in a COG are the overviews of [Chapter 46](ch46-data-models.md), with all their kernel semantics, and the kernel is recorded only in GDAL's metadata tag.

### 47.2.3 Compression

**DEFLATE**, **LZW**, and **ZSTD** are lossless; with a horizontal predictor (`PREDICTOR=2` for integers, `3` for floats) they typically shrink a float32 DEM by 2–4×. **LERC** (Limerick Error-bounded Raster Compression, Esri; open since 2016) is *lossy with a bound*: the writer specifies a **maximum absolute error** and the codec quantizes each block to that tolerance, so `MAX_Z_ERROR=0.001` guarantees that no cell deviates from the source by more than 1 mm while achieving ratios well beyond lossless. `MAX_Z_ERROR=0` is lossless. The error is per cell and uniform within the bound, so its standard deviation is at most $\text{maxerr}/\sqrt{3}$; it is not an RMS. **JPEG2000** can be lossless or lossy; the lossy mode's wavelet quantization produces smooth-looking errors of decimetres on DEMs that pass visual inspection, and the lossless mode is rarely the default.

### 47.2.4 Terrain-RGB and Terrarium

Web terrain tiles encode elevation in the three 8-bit channels of a PNG. **Mapbox Terrain-RGB**: $h = -10\,000 + (256^2 R + 256 G + B)\times 0.1$, a 0.1 m step over a range of roughly −10 000 m to about +1 668 km. **Terrarium** (Mapzen/AWS): $h = 256 R + G + B/256 - 32\,768$, a step of $1/256$ m ≈ 3.9 mm. Decoding Terrarium with the Terrain-RGB formula produces elevations off by tens of kilometres; decoding either from a tile that was resampled with bilinear interpolation (as web tile servers do for overzoom) averages the *channels*, not the elevations, and produces garbage wherever a channel wraps. The quantization errors are $0.1/\sqrt{12} = 0.029$ m and $0.0039/\sqrt{12} = 0.0011$ m respectively—but the source DEM's resampling into Web Mercator tiles usually dominates.

### 47.2.5 Esri ASCII, .flt/.hdr, and SRTM .hgt ⟨H⟩

**Esri ASCII Grid** (`.asc`) has a six-line header (`ncols`, `nrows`, `xllcorner` *or* `xllcenter`, `yllcorner`/`yllcenter`, `cellsize`, `NODATA_value`) and space-delimited values; the corner/centre keyword is the only registration information and is frequently wrong. It carries no CRS; a `.prj` sidecar may. **.flt/.hdr** is its binary float32 sibling with a `byteorder` field. **SRTM .hgt** tiles are raw big-endian int16 arrays named by their south-west corner (`N37W122.hgt`), 3601×3601 samples for 1″ and 1201×1201 for 3″, PixelIsPoint, void = −32768, no header at all—the dimensions are inferred from file size. Adjacent tiles share their edge rows and columns, so a naive mosaic that treats cells as areas double-counts the edge or shifts tiles by one sample. SRTM heights are EGM96 orthometric integers; the integer quantization is 0.29 m σ on top of the measurement error.

### 47.2.6 USGS DEM, SDTS, and the contour ghost

The **USGS DEM** format (1970s–1990s) is fixed-width ASCII in 1 024-byte records with A/B/C logical records holding header, profiles, and accuracy; the **SDTS** transfer (FIPS 173, 1992) wrapped the same content in ISO 8211 modules. Both are read by GDAL and both are legacy. The data inside, not the container, is the hazard: many 7.5′ DEMs were interpolated from digitized contours, and their histograms spike at the contour interval while their slope maps show terraces—the **contour ghost** or stair-step artefact. Level 1 DEMs (from photogrammetric profiling) show along-profile striping instead. The artefacts persist in any DEM with that lineage; detect them with an elevation histogram and a low-sun hillshade ([Chapter 54](ch54-evaluating-others-data.md)).

### 47.2.7 DTED

**DTED** (MIL-PRF-89020B, 2000) is the NATO/NGA terrain format. Levels 0, 1, and 2 have nominal post spacings of 30″, 3″, and 1″ (about 900, 90, and 30 m at the equator). Longitude spacing is **latitude-dependent** to keep posts roughly square: for Level 1, 3″ below 50°, 6″ from 50° to 70°, 9″ to 75°, 12″ to 80°, and 18″ above 80° (the same multipliers apply to the other levels). Elevations are integer metres in **signed-magnitude** 16-bit big-endian (not two's complement; readers that assume two's complement decode every depression below sea level as a huge positive), void is −32767, data are stored column-major from the south-west corner northward, and the vertical datum is MSL realized by **EGM96** (earlier files may use EGM84 or a local datum; read each file's header) on WGS 84 horizontal. The user header and accuracy records declare absolute and relative horizontal and vertical accuracy at 90 % (CE90/LE90) as integers in metres—often filled with "NA." The integer encoding adds 0.29 m σ; it is not a statement that the data are accurate to 1 m.

### 47.2.8 NITF, JPEG2000, IMG, GRIB

**NITF** (MIL-STD-2500C) is a defence imagery container in which DEMs appear as image segments, often JPEG2000-compressed, with georeferencing in TREs that GDAL maps with varying fidelity. **Erdas IMG** (HFA) is widely supported, with internal pyramids; its pre-WKT CRS encoding occasionally loses datum parameters. **GRIB2** carries numerical-weather-model **orography**, a spectrally truncated surface on a grid of tens of kilometres—useful for atmospheric correction, useless as a DEM.

<!-- figure: Figure 47.1 — Anatomy of a LAS 1.4 file (header, VLRs incl. WKT and extra bytes, point records, EVLRs) side by side with a COG (IFDs, tile offsets, overviews, tiles), annotated with what each structure does and does not carry about CRS, vertical datum, nodata, and uncertainty. -->

## 47.3 Hydrographic formats

### 47.3.1 BAG

The **Bathymetric Attributed Grid** (Open Navigation Surface Working Group; 1.0 in 2006, 2.0.x current) is an HDF5 container holding, at minimum, an **elevation** layer (positive up, metres, nodata 1 000 000), an **uncertainty** layer of the same shape, ISO 19115-based XML **metadata**, and a **tracking list** of manually edited nodes with their original and replacement values. Optional layers include nominal elevation (shoal-biased for charting), hypothesis count and strength, number of soundings, standard deviation, and the **variable-resolution** refinement layers of [Chapter 46](ch46-data-models.md). The metadata declares the horizontal and vertical CRS and the **uncertainty type**—the enumeration that says whether the uncertainty layer is a raw standard deviation, a CUBE hypothesis σ, a product 95 % uncertainty, or something else. The file is digitally signable. GDAL reads BAG (including VR, via resampling or sub-datasets) and writes single-resolution BAG; the ONS C++/Python library is the reference. The semantic hazard is that GDAL exposes BAG as a two-band raster, and a `gdal_translate` to GeoTIFF produces bands named "elevation" and "uncertainty" with the type, tracking list, and most of the metadata gone.

### 47.3.2 S-102

**S-102** is the IHO product specification for bathymetric surfaces in the S-100 framework, encoded in HDF5 following S-100 Part 10c. **Edition 3.0.0** (December 2024) is the first operational edition. A dataset holds a `BathymetryCoverage` with **depth** (positive down—the opposite sign convention from BAG) and **uncertainty** arrays at a single resolution, and a `QualityOfBathymetryCoverage` whose cells reference rows of a feature attribute table carrying survey date range, horizontal and vertical uncertainty, feature-detection size, and similar per-region quality metadata (GDAL exposes this as a raster attribute table). Multi-resolution is achieved by issuing tiles of different resolutions; the tiling scheme and dataset size limits are set by the specification and by producer guidance, and change between editions. S-100 **Part 15** defines encryption and digital signatures for distribution, so an S-102 file in the wild may be unreadable without a permit. **Edition 3.1.0** is in development at the time of writing. S-102 is a navigation product, and its depths may be shoal-biased by the producer's compilation rules.

### 47.3.3 S-57/S-101 soundings and depth areas

Charts carry bathymetry as vector features: **SOUNDG** point clusters (3D coordinates, depth as the third ordinate) and **DEPARE** depth-area polygons with `DRVAL1`/`DRVAL2` minimum and maximum depth. These are generalized, shoal-biased selections from source surveys, in the chart datum, at chart scale; a DEM built from them is a safety surface, not a seafloor model.

### 47.3.4 GSF and vendor raw formats

**GSF** (Generic Sensor Format, originally SAIC/Leidos; 3.x current) is a sensor-neutral binary for processed multibeam pings—per-beam depth, across/along-track, travel time, backscatter, quality flags, plus navigation, attitude, sound-velocity profiles, and processing parameters. It is MB-System's preferred processed format and the archive format of several agencies. Vendor raw formats are the real raw: Kongsberg **.all** (legacy datagrams) and **.kmall** (current, self-describing), Teledyne Reson/Odom **.s7k** (record-based, water column capable), **.xtf** (Triton eXtended Triton Format, a sidescan/bathy wrapper of varying fidelity), EdgeTech **.jsf**, R2Sonic packets (typically captured inside Hypack or QINSy logs). Each embeds the ping-level data needed to recompute TPU; none is a product format. **SBET** (Applanix POSPac Smoothed Best Estimate of Trajectory) is a headerless binary of 17 double-precision fields per epoch—GPS seconds of week, latitude and longitude in radians, ellipsoidal height, velocities, attitude, accelerations—with a companion RMS file; the GPS week is not stored ([Chapter 13](ch13-imu-ins.md)). Hypack (.HSX/.RAW) and QINSy (.db) project formats are readable mainly by their own software; archive GSF or vendor raw plus SBET.

### 47.3.5 Compilations: GEBCO, ETOPO, CSAR

**GEBCO** grids ship as NetCDF (15″ since 2019; elevation as int16 metres with a companion **TID** grid of source-type codes) and as GeoTIFF and Esri ASCII. **ETOPO 2022** (NCEI) ships 15″ and 30″ NetCDF and GeoTIFF in ice-surface and bedrock versions. Both are PixelIsArea on a geographic grid; both are compilations ([Chapter 48](ch48-compositing.md)) whose cell values can come from anything between multibeam and satellite-gravity prediction, which the TID tells you and the elevation does not. **CSAR** is CARIS's proprietary surface container (grid or point cloud, with band metadata); export to BAG for exchange.

## 47.4 Multidimensional and cloud-native formats

### 47.4.1 NetCDF-4/HDF5 with CF conventions

**NetCDF-4** is an HDF5 profile with named dimensions, variables, and attributes. The **CF conventions** (1.11, 2023) make it geospatial: `standard_name` (`height`, `altitude`, `sea_floor_depth_below_geoid`, `sea_floor_depth_below_mean_sea_level` are the elevation-relevant ones), `units`, `_FillValue`, `positive = "up"|"down"`, a `grid_mapping` variable carrying the horizontal CRS as CF parameters (and, since CF 1.7, optionally `crs_wkt`), coordinate variables with `bounds` that settle the area-versus-point question explicitly, and `cell_methods` that state the aggregation (`area: mean`, `area: minimum`). CF is the only mainstream raster convention with a slot for the aggregation rule. The vertical datum is expressible only through the standard name and free-text attributes or a WKT compound CRS; readers rarely parse it. Check `positive` and the latitude ordering (north-up versus south-up) on every file.

### 47.4.2 Zarr, GeoZarr, Icechunk ⟨H⟩, and Kerchunk

**Zarr** stores an N-dimensional array as a directory (or object-store prefix) of compressed **chunks** plus JSON metadata; v2 (2018) is ubiquitous, **v3** (specification finalized 2024) adds sharding (many chunks in one object) and extension points. **GeoZarr** is the OGC-track convention for encoding CF-style geospatial metadata, CRS, and multiscale (overview) groups in Zarr; it is still maturing at the time of writing, and interoperability between writers is imperfect. **Icechunk** (Earthmover, open-sourced October 2024) adds transactional, versioned commits over Zarr chunks—git-like snapshots of an array store—so a composite DEM can be updated and its earlier states retained and cited ([Chapter 50](ch50-archiving-and-provenance.md)). **Kerchunk** indexes the byte ranges of existing NetCDF/HDF5/GRIB files so they can be read through the Zarr interface without conversion.

**Chunking** is the design decision. For a 2D DEM read by map viewers, square chunks of 512–2 048 cells per side match tile access; for a stack of DEM epochs read as time series at points, a chunk should span all epochs at a small spatial footprint; the two are incompatible, and the usual answer is two copies. Chunks below about 1 MB waste requests; above about 50 MB they waste bandwidth.

### 47.4.3 Tiled web formats

**XYZ raster tiles** carry elevation only as Terrain-RGB or Terrarium (§47.2.4). **quantized-mesh** and **3D Tiles** carry terrain and meshes with per-tile geometric error ([Chapter 46](ch46-data-models.md)). **PMTiles** packs an entire tile pyramid into one file with a Hilbert-ordered directory for HTTP range access. All are display formats: resampled to Web Mercator, LoD-simplified, and quantized; none should be the source for analysis.

## 47.5 Vector and 3D exchange formats

**CityGML** (OGC 3.0, GML encoding) and **CityJSON** (2.0, the compact JSON encoding) carry semantic 3D city models with LoDs and a CRS declared at the file level; terrain appears as a `ReliefFeature` (TIN, mass points, breaklines, or raster). **IFC** (ISO 16739-1; IFC 4.3 adds infrastructure alignment) describes BIM elements in a project coordinate system; georeferencing is through `IfcMapConversion` and `IfcProjectedCRS`, which are frequently absent, so an IFC's "elevation" is usually relative to a project datum ([Chapter 63](ch63-buildings-cities-innerspace.md)). **LandXML** (1.2, 2008) is the civil-engineering exchange for surfaces (TINs with breaklines), alignments, and points; it has a `CoordinateSystem` element that is optional and often empty. **DXF/DWG** have no CRS concept at all; survey drawings in DXF are typically in a **local ground coordinate system** scaled from a projected grid by a combined factor (of order 1.0001–1.0005), and treating ground coordinates as grid coordinates mislocates a 10 km site by metres ([Chapter 10](ch10-projections-and-resampling.md)). **OBJ**, **glTF**, and **USD** are graphics formats; glTF is Y-up by default, so a terrain mesh exported without the axis swap arrives on its side. **GeoPackage** (OGC 1.4, 2024) is a SQLite container for vectors and for tiled rasters, including the gridded-coverage extension for elevation (integer or float tiles with scale/offset); **GeoParquet** (1.1, 2024) stores vector geometries in columnar Parquet with CRS in metadata and is becoming the format for large point datasets (soundings, checkpoints). **Shapefile** `.prj` files use a WKT1-ESRI dialect with no vertical CRS; use GeoPackage for contours and breaklines.

## 47.6 Format-induced error catalog

Formats add errors that have nothing to do with the sensor. The catalog below gives each mechanism, its magnitude, and the test.

**Integer and fixed-point quantization.** Rounding to a step $q$ adds an error uniform on $[-q/2, q/2]$ with $\sigma = q/\sqrt{12} \approx 0.289\,q$ and zero mean (when the data are not already quantized at a coarser step). LAS at scale 0.01 m: 2.9 mm per axis. DTED and SRTM integer metres: 0.29 m. GEBCO int16 metres: 0.29 m. Terrain-RGB at 0.1 m: 0.029 m. quantized-mesh with a tile height range of 2 000 m over 15 bits: $q = 0.061$ m, $\sigma = 0.018$ m. Quantization errors are independent between products, so differencing two integer-metre DEMs of identical terrain has $\sigma = 0.41$ m from quantization alone ([Chapter 41](ch41-change-detection.md)).

**float32 precision at large coordinates.** IEEE float32 has a 24-bit significand, so the spacing between representable values (the **ulp**) at magnitude $m$ is $2^{\lfloor \log_2 m\rfloor - 23}$: 0.0078 m at 10⁵ m, 0.0625 m at 10⁶ m, 0.5 m at 5×10⁶ m. UTM northings in mid-latitudes are 4–6×10⁶ m, so a northing stored as float32 is quantized at 0.5 m—a tool that converts LAS coordinates to float32 (as many visualizers, and some exporters, do) destroys horizontal precision while leaving heights, which are small numbers, intact. Elevations are safe in float32 (ulp 0.0005 m at 8 000 m); the hazard is specific to coordinates, including ECEF (6.4×10⁶ m, ulp 0.5 m). Store coordinates as float64 or as scaled integers with an offset.

**Lossy compression.** LERC at `MAX_Z_ERROR = e` bounds each cell by $e$ (σ ≤ $e/\sqrt{3}$); JPEG2000 lossy at a bitrate gives no per-cell bound and errors that correlate spatially, producing smooth artefacts that look like terrain. Test by decompressing and differencing against the source; report the maximum, not the RMS.

**Nodata collisions.** −9999 is a valid depth in the Mariana Trench's neighbourhood only in the sense that −10 920 m exists; it is a valid elevation nowhere, which is why it was chosen—but −32768 is int16's minimum and appears as a legitimate value when a float grid is cast to int16 without range checking; 0 collides with sea level; NaN cannot be stored in integer bands; BAG's 1 000 000 becomes an elevation when written to a format that does not carry the nodata tag. Test with a histogram and by confirming that the nodata tag survived every conversion.

**Vertical CRS lost on export.** GeoTIFF→Esri ASCII, LAS→XYZ, BAG→GeoTIFF (sometimes), NetCDF→anything through tools that ignore `grid_mapping`: the horizontal CRS may survive and the vertical does not. The result is a file that is "in NAVD88" by oral tradition. Test every output with `gdalinfo`/`pdal info` and require a compound CRS or an explicit metadata statement.

**Half-cell shifts.** Converting PixelIsPoint to PixelIsArea (or reading one as the other) shifts the grid by half a cell: 15 m for SRTM, 0.5 m for a 1 m lidar DEM. On a slope $s$ the induced vertical error is $0.5\,\Delta\,s$. Test by differencing against an independent product and looking for a slope-correlated residual with alternating sign on opposite aspects ([Chapter 44](ch44-resolution-and-sampling.md)).

**Tile seams.** Independently gridded tiles disagree at edges; SRTM's shared edge rows and DTED's shared edge columns are double-counted by naive mosaics; edge-of-tile interpolation with no neighbour data produces a one-cell nodata or extrapolated fringe. Test with a gradient magnitude raster: seams appear as straight lines.

**Byte order and encoding legacies.** SRTM .hgt and DTED are big-endian; .flt is declared in its header; GSF and SBET are little-endian doubles; DTED is signed-magnitude. A wrong assumption produces values of ±10⁴ m or a map of noise, which is at least obvious—unless only the sub-sea-level cells are affected.

> **Uncertainty budget.** Format-induced vertical error, 1σ unless noted, for common encodings.
>
> | Mechanism | Magnitude | Note |
> |---|---|---|
> | LAS scale 0.01 m | 0.003 m per axis | Zero mean |
> | LAS scale 1 m (misconfigured) | 0.29 m | Catastrophic for lidar |
> | DTED / SRTM / GEBCO int16 metres | 0.29 m | Adds to measurement error in quadrature |
> | Terrain-RGB 0.1 m step | 0.029 m | Plus Web Mercator resampling |
> | quantized-mesh, 2 000 m tile range | 0.018 m | Depends on tile relief |
> | LERC MAX_Z_ERROR 0.01 m | ≤ 0.01 m max; ≈ 0.006 m σ | Bounded |
> | float32 northing at 5×10⁶ m | 0.5 m horizontal | Becomes vertical on slopes |
> | Half-cell convention error, 1 m DEM on 20° slope | 0.18 m systematic | Sign depends on aspect |
> | Half-cell convention error, SRTM on 20° slope | 5.5 m systematic | Same |

## 47.7 Choosing a format by role

A single dataset passes through several roles, and no format serves all of them. **Acquisition raw** (vendor sonar datagrams, lidar waveform and range files, raw GNSS/IMU observations, SBET): keep forever in the native format plus a documented converter, because it is the only level from which errors discovered later can be corrected ([Chapter 29](ch29-processing-pipelines.md), [Chapter 50](ch50-archiving-and-provenance.md)). **Working** formats are whatever the toolchain reads fastest—LAZ/COPC, tiled GeoTIFF, Zarr, GSF—and carry full precision. **Delivery** formats are dictated by the specification: LAS 1.4 PDRF 6+ in the USGS LBS, BAG for NOAA hydrographic surveys, S-102 for navigation products, GeoTIFF/COG for most DEM contracts; the contract usually also fixes CRS, nodata, and tiling. **Archive** formats favour openness, self-description, and stability: LAZ/COPC with WKT, COG with full GeoKeys and metadata, NetCDF-CF, BAG; avoid proprietary containers and lossy compression. **Web** formats (COPC, COG, PMTiles, 3D Tiles, Terrain-RGB) are derived, lossy or resampled, and should link back to the archive object they were made from.

## 47.8 Validation tools for files

- `pdal info --metadata file.laz` prints the header (version, PDRF, scale/offset, counts, bounds, global encoding), the VLRs including WKT, and the extra-bytes schema; `pdal info --stats` gives per-dimension ranges (a Z range of −9999 to 4 000 reveals a nodata leak; a classification histogram reveals a missing ground class). `pdal info --boundary` draws the footprint for footprint–bounds mismatch.
- `lasinfo` (LAStools; open-source portion) prints the same and `-repair` fixes header bounds; `lasvalidate` (ASPRS/rapidlasso, open source) checks conformance to the specification—legal PDRF/version combinations, header consistency, return numbering, GPS time encoding—and emits an XML report.
- `gdalinfo -stats -checksum file.tif` reports CRS (look for both a horizontal and a `VERT_CS`/compound), `AREA_OR_POINT`, nodata, data type, block size, overviews with their resampling tag, and value range; `gdalinfo -json` makes it machine-checkable.
- `rio cogeo validate file.tif` (rio-cogeo) and `cogger` or GDAL's `validate_cloud_optimized_geotiff.py` check COG layout (tiling, IFD order, overviews); they do not check CRS or meaning.
- BAG: the ONS library's validation (XML schema and layer consistency), GDAL `gdalinfo` for layers and metadata, and NOAA's HydrOffice QC Tools for hydrographic checks (holes, uncertainty-to-depth ratios, tracking list review).
- S-100/S-102: the IHO **S-158** validation check suites (S-158:102 *Bathymetric Surface Validation Checks*, Ed. 1.0.0, December 2025, released for implementation and testing) define machine-checkable rules; `s100py` (NOAA) reads and writes the HDF5 structure; GDAL reads S-102 and exposes the quality table.
- NetCDF/Zarr: `ncdump -h`, the CF Checker (`cfchecks`), `xarray.open_dataset(...).rio.crs` to confirm that the CRS survived.

> **Try it.** A receipt check for a lidar delivery and a DEM.
> ```bash
> # Point cloud: version, PDRF, scale/offset, CRS, class and Z ranges
> pdal info --metadata tile.laz | jq '.metadata | {major_version, minor_version,
>   dataformat_id, scale_x, scale_z, offset_x, srs: .srs.compoundwkt}'
> pdal info --stats --dimensions Z,Classification tile.laz | jq '.stats.statistic[]|{name,minimum,maximum}'
> lasvalidate -i tile.laz -o tile_validate.xml
> # Raster: compound CRS, pixel convention, nodata, overviews, COG layout
> gdalinfo -json dem.tif | jq '{crs: .coordinateSystem.wkt, aop: .metadata[""].AREA_OR_POINT,
>   nodata: .bands[0].noDataValue, ovr: .bands[0].overviews, type: .bands[0].type}'
> rio cogeo validate dem.tif
> ```
> Expected outcome: a passing delivery shows LAS 1.4 with PDRF 6–8, scale ≤ 0.01 m, a compound WKT naming both horizontal and vertical CRS, Z within the project's elevation range, and `lasvalidate` reporting "pass"; the raster shows a compound CRS, an explicit `AREA_OR_POINT`, a declared nodata, overviews, and "is a valid cloud optimized GeoTIFF".

<!-- figure: Figure 47.2 — Decision chart for format by role (raw / working / delivery / archive / web) across point, raster, hydrographic, and 3D data, with the semantic fields (horizontal CRS, vertical CRS, nodata, pixel convention, uncertainty, lineage) each format can carry marked present/absent. -->

## Then & now

Early elevation files were vendor binaries and ASCII dumps whose meaning lived in a README, if anywhere. The USGS DEM format and its SDTS wrapper (1990s) standardized public rasters but inherited contour-derived content. **GeoTIFF** (1995) put the CRS inside the raster, and nothing since has been as consequential. **LAS 1.0** (2003) ⟨H⟩ did the same for lidar points; 1.4 (2011; R15 in 2019) added 64-bit counts, WKT, and the redesigned PDRFs. **BAG 1.0** (2006) was the first mainstream elevation format to make uncertainty a mandatory layer. **LAZ** (2011) made lossless compression the default and, by being open, displaced closed alternatives. **COG** (2016 onward; OGC standard 2023) and **COPC** (2021) rearranged existing formats for HTTP range reads rather than inventing new ones—the cloud-native pattern. **Zarr** (v2 2018; v3 2024), **GeoZarr**, and **Icechunk** (2024) ⟨H⟩ moved large multidimensional stores to chunked object storage with versioning. **S-102 Ed. 3.0** (2024) made gridded bathymetry an official navigation product. The direction is clear—self-describing containers, network range access, uncertainty and lineage inside the file, versioned stores—and the persistent gap is the vertical CRS, which every modern format *can* carry and most files still do not.

## Mathematics

**Uniform quantization.** Rounding to step $q$ yields an error $e \sim U(-q/2, q/2)$ with $E[e]=0$ and $\mathrm{Var}[e] = \frac{1}{q}\int_{-q/2}^{q/2} e^2\,de = q^2/12$, so $\sigma_q = q/\sqrt{12}$. Truncation instead of rounding adds a bias of $q/2$. Two independently quantized products differ with variance $q_1^2/12 + q_2^2/12$. The model holds when the signal varies by more than $q$ between samples; for a flat surface quantized at 1 m, the error is a constant, not a random variable.

**float32 precision.** A binary32 value is $(-1)^s \cdot 1.f \cdot 2^{E}$ with a 23-bit fraction $f$, so the unit in the last place at magnitude $m$ is $\mathrm{ulp}(m) = 2^{\lfloor \log_2 m \rfloor - 23}$ and the rounding error is uniform within $\pm\,\mathrm{ulp}/2$: $\sigma = \mathrm{ulp}/\sqrt{12}$. At $10^5$ m, $\lfloor\log_2 10^5\rfloor = 16$, ulp $= 2^{-7} = 0.0078$ m. At $10^6$ m, $\lfloor\log_2\rfloor = 19$, ulp $= 2^{-4} = 0.0625$ m. At $5\times10^6$ m, $\lfloor\log_2\rfloor = 22$, ulp $= 2^{-1} = 0.5$ m. Subtracting an offset of $5\times10^6$ before storage brings a 100 km survey back to magnitude $10^5$ and ulp 0.0078 m, which is why LAS uses offsets and why "store as float32 after subtracting a tile origin" is the correct pattern for meshes and tiles. **Double** (binary64) has a 52-bit fraction: ulp at $5\times10^6$ m is $2^{-30} \approx 10^{-9}$ m.

**LERC max-error semantics.** For each block, LERC chooses a quantization step $q_b \le 2e$ such that every reconstructed value $\hat z$ satisfies $|\hat z - z| \le e$; blocks that cannot meet the bound more cheaply than lossless are stored losslessly. Hence the per-cell error is bounded (not merely bounded in RMS), uniform within a block with $\sigma_b \le e/\sqrt{3}$, and spatially blocky in its statistics—differences between adjacent blocks can show faint seams at the $e$ level.

**COPC octree addressing.** A node key is $(\ell, x, y, z)$ with $0 \le x,y,z < 2^\ell$; its cube has side $S/2^\ell$ within the root cube of side $S$, and its children are $(\ell+1, 2x+i, 2y+j, 2z+k)$ for $i,j,k \in \{0,1\}$. The hierarchy EVLR lists, per node, the byte offset and length of its LAZ chunk and its point count (or a pointer to a sub-hierarchy page); nodes are typically written in a depth-first or Hilbert-sorted order so that spatially adjacent nodes are adjacent in the file, which reduces the number of range requests for a view.

## Validation & uncertainty

Format errors are systematic, reproducible, and invisible to the checkpoint test if the checkpoints are processed through the same format chain. The validation plan therefore has two parts: structural checks on the file, and *differential* checks that isolate what the format did to the values.

**Structural checks (every file, automated).** Version and PDRF legal; scale factors appropriate to the sensor (≤ 0.01 m airborne, ≤ 0.001 m terrestrial); offsets present when coordinates exceed about 10⁶ m at the chosen scale; GPS time encoding flag consistent with the time values; horizontal *and* vertical CRS present and in agreement with the project specification; `AREA_OR_POINT` explicit; nodata declared and absent from the valid range; data type adequate (float32 for heights, never for projected coordinates); compression lossless or with a declared bound; overviews present with a recorded kernel; for BAG, uncertainty type declared and tracking list present; for S-102, quality table populated. The Try-it in §47.8 is the minimum script.

**Differential checks (per conversion step).** Keep the richest file and difference every derivative against it. Points: `pdal diff` or a join on GPS time and return number, checking that X, Y, Z residuals are exactly zero (lossless) or bounded by half the scale. Rasters: `gdal_calc.py` difference between source and exported grid on the same cell lattice; the expected result for lossless paths is identically zero, for LERC is bounded by `MAX_Z_ERROR`, and for anything else is a finding. Pay attention to the *extent and transform* as well as the values—a half-cell shift leaves the values identical and the georeferencing wrong—by comparing `gdalinfo` origins to the cell size.

**Quantization and precision budgets.** Add format-induced terms to the product's uncertainty budget in quadrature, explicitly: $\sigma_{\text{total}}^2 = \sigma_{\text{meas}}^2 + \sigma_{q}^2 + \sigma_{\text{float}}^2 + \ldots$. For a DTED Level 2 cell with 2 m measurement uncertainty the integer quantization (0.29 m) adds 1 %; for a 0.05 m lidar DEM written as int16 metres it adds 500 %.

> **Worked example.** *float32 coordinates in UTM.* A lidar tile in UTM zone 10 N has northings near 4 180 000 m. An exporter writes XYZ as float32. $\lfloor\log_2 4.18\times10^6\rfloor = 21$, so ulp $= 2^{21-23} = 0.25$ m, and northings are rounded to a 0.25 m lattice ($\sigma = 0.072$ m). Eastings near 550 000 m ($\lfloor\log_2\rfloor = 19$) land on a 0.0625 m lattice ($\sigma = 0.018$ m). On a 25° slope the northing error alone induces a vertical error of $0.072 \times \tan 25° = 0.034$ m 1σ with a 0.058 m worst case—comparable to the whole vertical accuracy budget of a USGS QL1 product (RMSEz 0.10 m). The symptom is a cloud that lies on visible lines when viewed from above; the test is a histogram of fractional coordinate parts, uniform for healthy data and concentrated on multiples of 0.25 here; the fix is float64 or scaled integers with offsets.

**Nodata and range checks.** Histogram every band for spikes at −9999, −32768, 0, 1 000 000, 3.4×10³⁸, and the contour interval; confirm the declared nodata is outside the valid range and, for int16 casts, that the source range fit and the rounding mode was stated.

**Semantic checks for hydrographic formats.** For BAG, read the uncertainty type and compare the uncertainty-to-depth ratio distribution against the S-44 order claimed in metadata; a product-uncertainty layer should exceed the TVU formula's value at the cell's depth, and a raw-σ layer need not. For S-102, confirm depth sign (positive down), compare the quality table's uncertainty against the coverage's uncertainty array, and verify tile edges against neighbouring tiles.

**What to report.** The format and version of every delivered and archived file; scale/offset or data type and the implied quantization; compression and bound; CRS (horizontal, vertical, geoid realization) as encoded in the file and as stated in the metadata; pixel convention; nodata; validator outputs with versions; and the differential-check results per conversion step, with maximum absolute deviation.

<!-- figure: Figure 47.3 — Histogram of the fractional parts of northings from a float32-exported point cloud showing spikes at multiples of 0.25 m, beside the uniform histogram from the LAS source; inset of the point cloud viewed from above showing the lattice. -->

## Software

**Open source:** PDAL (`info`, `translate`, `diff`, `tindex`; reads/writes LAS/LAZ/COPC/EPT/E57/PLY/text, GDAL rasters, BAG via GDAL; caveat—default writer scale is 0.01 m); laspy (Python LAS/LAZ/COPC with lazrs); LASzip/laz-perf (compression libraries); `lasvalidate` and the open portion of LAStools (`lasinfo`, `las2las`); GDAL/rasterio (every raster format here, COG driver, BAG, S-102, NetCDF, Zarr, GeoPackage; caveat—CF and BAG semantics are mapped, not preserved, on export); rio-cogeo and `cogger` (COG creation and validation); MB-System (GSF, .all/.kmall, .s7k, .xtf, many legacy formats; `mbinfo`, `mbgrid`); HDF5/h5py, netCDF4-python, xarray/rioxarray, Zarr-Python, Icechunk, Kerchunk; ONS BAG library (C++/Python); NOAA `s100py`; CF Checker; GeoPandas/pyogrio; cjio (CityJSON); IfcOpenShell (IFC).

**Free but closed:** Esri's zLAS tooling; vendor format libraries (Kongsberg, Teledyne) are documented but not open.

**Commercial:** LAStools (licensed tools: `lasground`, `lastile`, `las2dem`); CARIS (CSAR, BAG, S-102 production); QPS Qimera/Fledermaus (vendor raw, GSF, BAG); Hypack and QINSy (acquisition formats); Global Mapper and FME (broad format conversion; caveat—both silently apply defaults for scale, nodata, and pixel convention); ArcGIS (LAS datasets, zLAS, mosaic datasets); TerraSolid.

## Standards & guides

- ASPRS, *LAS Specification 1.4 – R15* (2019); ASPRS Lidar Division, *LAS Domain Profile Description: Topo-Bathy Lidar* (version 1.0, 2013).
- Hobu Inc./USGS, *COPC Specification 1.0* (2021); Entwine Point Tile specification.
- ASTM E2807-11 (2019), *Standard Specification for 3D Imaging Data Exchange, Version 1.0* (E57).
- OGC, *GeoTIFF Standard 1.1* (19-008r4, 2019); OGC, *Cloud Optimized GeoTIFF Standard 1.0* (21-026, 2023).
- Esri, *LERC specification* (open source, 2016–).
- NGA, *MIL-PRF-89020B Performance Specification: Digital Terrain Elevation Data* (2000).
- Open Navigation Surface WG, *BAG Format Specification Document* 2.0.x (2.0.1 released 2022; current documentation at bag.readthedocs.io).
- IHO, *S-100 Universal Hydrographic Data Model* Ed. 5.x (Parts 10c, 15); *S-102* Ed. 3.0.0 (2024), Ed. 3.1.0 in development; *S-158:102 Bathymetric Surface Validation Checks* Ed. 1.0.0 (2025, for implementation and testing).
- CF Conventions 1.11 (2023); Unidata NetCDF-4 and HDF5 documentation.
- Zarr v3 core specification (2024); GeoZarr specification (OGC, in development); Icechunk specification (2024).
- OGC, *GeoPackage Encoding Standard 1.4* (2024) with gridded coverage extension; *GeoParquet 1.1* (2024).
- OGC, *CityGML 3.0* (2021); *CityJSON 2.0* (2023); ISO 16739-1:2024 (IFC 4.3); LandXML 1.2 (2008).
- USGS, *Lidar Base Specification* 2024 rev. A, or current revision (delivery format clauses); NOAA OCS *Hydrographic Surveys Specifications and Deliverables* (BAG and raw-data retention clauses).

## Pitfalls

- **LAS with no CRS VLR and "it's probably State Plane feet"** → exporters that skip the VLR, and US projects where feet and metres coexist → reject on receipt; if forced, test both hypotheses against a known feature and record the inference as an assumption.
- **GeoTIFF with horizontal CRS and no vertical CRS** → GeoKeys for vertical are optional and most writers omit them → require EPSG vertical keys or compound WKT plus the geoid realization in metadata; without them, orthometric versus ellipsoidal is a guess worth tens of metres.
- **BAG uncertainty exported to GeoTIFF loses its meaning** → GDAL exposes BAG as two bands → carry the uncertainty type and tracking list in sidecar metadata, or deliver BAG.
- **Terrain-RGB decoded with the wrong base or interval** → two incompatible encodings share a tile format → check a known elevation (sea level should decode to ≈ 0) before using any tile source.
- **DTED edges and integer metres read as 1 m accuracy** → the format's precision is mistaken for the product's accuracy → use the accuracy records and the source lineage; add 0.29 m σ quantization to the budget.
- **A JP2 DEM with "lossless-looking" 0.5 m errors** → lossy wavelet compression is the default in many exporters → difference against the source; require lossless or LERC with a stated bound.
- **float32 projected coordinates** → visualizers and some exporters promote integers to float → histogram fractional coordinates; store float64 or scaled integers with offsets.
- **Half-cell shift from PixelIsPoint/PixelIsArea confusion** → readers that ignore the raster-type key or ASCII headers with the wrong keyword → compare origins against cell size; look for aspect-dependent residuals.
- **Nodata that becomes data** → casts and format hops drop the nodata tag → histogram for spikes at the usual sentinel values; verify the tag after every conversion.
- **DXF/LandXML surfaces assumed to be in grid coordinates** → the formats carry no CRS and engineers work in ground coordinates → check for a scale factor against a known grid point before merging with a DEM.

## Key takeaways

- The format is part of the measurement chain: it can quantize, truncate, shift, and strip meaning. Budget for it.
- Carry horizontal and vertical CRS (with geoid realization), nodata, pixel convention, uncertainty, and lineage *inside* the file; sidecars get lost.
- Scale/offset and data type are precision decisions: 0.01 m LAS scale is 3 mm σ; float32 projected coordinates are 0.25–0.5 m lattices; int16 metres is 0.29 m σ.
- Lossless by default; LERC with a declared bound when size matters; never lossy JPEG2000 or JPEG for elevation.
- BAG and S-102 encode uncertainty with declared semantics; exporting them to generic rasters discards the semantics unless you carry them explicitly.
- Cloud-native formats (COG, COPC, Zarr) rearrange bytes for range access; their overviews and coarse nodes are subsamples, not data.
- Keep raw forever, work in full precision, deliver what the specification says, archive open and self-describing, and treat web formats as derivatives.
- Validate automatically on receipt and before delivery; a missing vertical CRS is a rejection.

## References

- American Society for Photogrammetry and Remote Sensing (2019). *LAS Specification 1.4 – R15*. ASPRS, Bethesda, MD.
- ASTM International (2019). *E2807-11: Standard Specification for 3D Imaging Data Exchange, Version 1.0*. ASTM, West Conshohocken, PA.
- Eaton, B., Gregory, J., Drach, B., Taylor, K., Hankin, S., et al. (2023). *NetCDF Climate and Forecast (CF) Metadata Conventions*, version 1.11. https://cfconventions.org
- Hobu Inc. (2021). *Cloud Optimized Point Cloud (COPC) Specification 1.0*. https://copc.io
- International Hydrographic Organization (2024). *S-102 Bathymetric Surface Product Specification*, Edition 3.0.0. IHO, Monaco.
- International Hydrographic Organization (2022). *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. IHO, Monaco.
- Isenburg, M. (2013). LASzip: Lossless compression of lidar data. *Photogrammetric Engineering & Remote Sensing*, 79(2), 209–217.
- National Geospatial-Intelligence Agency (2000). *MIL-PRF-89020B: Performance Specification, Digital Terrain Elevation Data (DTED)*. NGA.
- Open Geospatial Consortium (2019). *OGC GeoTIFF Standard*, version 1.1, OGC 19-008r4.
- Open Geospatial Consortium (2023). *OGC Cloud Optimized GeoTIFF Standard*, version 1.0, OGC 21-026.
- Open Geospatial Consortium (2024). *OGC GeoPackage Encoding Standard*, version 1.4.0, OGC 12-128r19.
- Open Navigation Surface Working Group (2024). *Bathymetric Attributed Grid (BAG) Format Specification Document*, version 2.0.x. https://bag.readthedocs.io (code: https://github.com/OpenNavigationSurface/BAG)
- Ritter, N., and Ruth, M. (1997). The GeoTIFF data interchange standard for raster geographic images. *International Journal of Remote Sensing*, 18(7), 1637–1647.
- Farr, T. G., et al. (2007). The Shuttle Radar Topography Mission. *Reviews of Geophysics*, 45, RG2004. doi:10.1029/2005RG000183
- Ledoux, H., Arroyo Ohori, K., Kumar, K., Dukai, B., Labetski, A., and Vitalis, S. (2019). CityJSON: A compact and easy-to-use encoding of the CityGML data model. *Open Geospatial Data, Software and Standards*, 4, 4.
- U.S. Geological Survey (2024). *Lidar Base Specification*, 2024 rev. A. USGS National Geospatial Program. https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-online
- Earthmover (2024). *Icechunk: Open-source, cloud-native transactional tensor storage engine* (specification and software, released 15 October 2024). https://icechunk.io

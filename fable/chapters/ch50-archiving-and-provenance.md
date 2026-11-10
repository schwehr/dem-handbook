# Chapter 50 — Archiving, versioning, and provenance

> **Part X — Representing, storing, finding, and keeping elevation data.** Having described how elevation data are modelled ([Chapter 46](ch46-data-models.md)), encoded ([Chapter 47](ch47-file-formats.md)), merged ([Chapter 48](ch48-compositing.md)), and described ([Chapter 49](ch49-metadata.md)), this chapter is about keeping them usable, trustworthy, and traceable for decades.

**In this chapter.** A survey is expensive and unrepeatable: the terrain, the seafloor, the forest, and the glacier of the acquisition date will never exist again. This chapter treats the archive as the second-most-important product of any elevation project, after the measurements themselves. You will learn what to keep (the rawest data you can, with calibration, trajectories, intermediates, software, and parameters), which formats survive (open, documented, self-describing, with fixity), how the OAIS reference model and trusted-repository certification structure an archive, and where national and community repositories fit. The chapter then covers versioning—semantic versions, per-tile change logs, supersession records modelled on NOAA's National Bathymetric Source, content-addressed stores such as Icechunk and LakeFS, and versioned DOIs—and provenance, from W3C PROV and ISO lineage to STAC processing metadata and pipeline manifests. It closes with the problems that make elevation archives different from generic data archives: reference frames and geoid grids that must be archived with the heights, legal retention and sovereignty, cost tiers and compression, and the rescue of historical smooth sheets, lead-line soundings, film, and tapes with honest uncertainty assigned.

## 50.1 What to keep

The question "what should we archive?" is usually asked when storage is being budgeted, and the answer given is usually "the deliverables." That answer loses the project. The deliverables—a DTM, a bathymetric grid, a classified point cloud—are the output of a particular processing chain run with particular parameters, geoid, filters, and software bugs on a particular date. Every one of those will be improved within a decade. The raw observations will not.

**Raw sensor data.** For lidar: the full waveforms or, for photon-counting systems, the raw photon events; the discrete returns as the sensor wrote them (vendor raw, before any filtering); the intensity and range calibration tables. For sonar: the raw datagrams (Kongsberg `.all`/`.kmall`, Reson `.s7k`, and so on) including water-column data where recorded, the sound-speed profiles, the raw tide or water-level observations, the vessel configuration file. For photogrammetry and SfM: the original images at full radiometric depth, not the JPEGs; the camera calibration; the image-event log. For InSAR: the single-look complex scenes and orbit files. For GNSS/IMU: the raw observables (RINEX or receiver-native), the IMU record, the base-station data, and the processed trajectory (SBET or equivalent) with its covariances. These are what let a future analyst re-derive the ground with a better classifier, a new geoid, a corrected boresight, or a machine-learning model that did not exist when the survey was flown ([Chapter 29](ch29-processing-pipelines.md), [Chapter 43](ch43-traditional-vs-ml.md)).

**Calibration and control records.** Boresight and lever-arm solutions with dates; patch-test results; camera certificates; checkpoint and control-point coordinates with their own survey records; the reference-surface measurements. Without these the raw data can be reprocessed but not re-validated ([Chapter 25](ch25-calibration-infrastructure.md), [Chapter 52](ch52-ground-truth.md)).

**Intermediate products.** Strip-adjusted but unclassified clouds; the classification before manual editing; the gridded surface before hydro-flattening; the composite's per-source inputs. Intermediates are where a reprocessing can restart without repeating the expensive steps, and where an audit can locate the step that introduced an artefact.

**Final products and their companions.** The published surfaces together with their uncertainty, source, date, and mask layers ([Chapter 48](ch48-compositing.md)), the checkpoint tables, and the metadata records ([Chapter 49](ch49-metadata.md)).

**Software, versions, scripts, and parameters.** The pipeline definitions (PDAL JSON, GMT scripts, workflow files), the exact software versions, the container images or environment locks, and the parameter files. A product is reproducible only if these are kept; §50.5 treats them as provenance.

The SRTM mission of February 2000 ([Chapter 21](ch21-radar-sar-insar.md)) produced its first public DEM in 2003–2004 at 3″ outside the United States; the raw interferometric data were reprocessed with ICESat-controlled void filling and improved phase unwrapping to produce the 1″ global release in 2014–2015 and NASADEM in 2020—better products from the same observations, two decades later. ICESat-2 and GEDI are reprocessed into new release versions every year or two as calibration and geolocation improve, each time from the raw photon and waveform data ([Chapter 52](ch52-ground-truth.md)). After earthquakes and landslides, pre-event raw lidar is the only basis for a reanalysis of what the ground was before ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md)); a pre-event DTM alone cannot answer "was the slope already moving?" because the classification choices are frozen in it. In hydrography, raw multibeam archived at NCEI is routinely re-gridded and reprocessed with modern sound-speed and uncertainty models; a 1990s grid at 50 m is of little use, the 1990s datagrams are.

> **Rule of thumb.** If a byte was measured rather than computed, archive it. If it was computed, archive it when recomputing it would cost more than a week of compute or when it embeds manual judgement (editing, classification review). The rule fails for sensors whose raw output is enormous relative to its information content—water-column sonar at full rate, video-rate photogrammetry—where a documented, lossless-where-possible reduction is the practical compromise; state what was discarded.

## 50.2 Formats for the long term

An archival format must be readable without the organization that wrote it, the software that wrote it, or the machine that wrote it. That translates to four properties: **open** (the specification is public and freely implementable), **documented** (every field is defined), **self-describing** (the file carries its own structure and metadata), and **widely implemented** (more than one independent reader exists, preferably one of them open source). The Library of Congress's *Sustainability of Digital Formats* pages assess geospatial formats on exactly these criteria and are a reasonable external authority when you must justify a choice.

| Content | Preferred archival format | Notes |
|---|---|---|
| Point clouds | LAS 1.4 / LAZ (LASzip) / COPC | Open ASPRS specification; LAZ is lossless; COPC adds spatial indexing in the same container |
| Full waveforms | PulseWaves, or vendor raw plus its specification | No dominant open standard; archive the vendor documentation with the data |
| Multibeam raw | Vendor datagram formats plus the format specification document and an MB-System-readable copy | Kongsberg, Reson, R2Sonic formats are documented but proprietary; MB-System's reader is the de facto preservation path |
| Gridded elevation | GeoTIFF / Cloud-Optimized GeoTIFF; NetCDF-4/HDF5 with CF conventions; Zarr | All open; COG and Zarr are cloud-friendly; BAG for navigation bathymetry with uncertainty |
| Imagery | TIFF (lossless), JPEG 2000 (lossless mode), original RAW plus a DNG or TIFF conversion | Keep the camera's raw if the converter is documented |
| GNSS/IMU | RINEX 3/4 for GNSS; receiver-native alongside; trajectory as documented ASCII or SBET with the vendor's record layout | Receiver-native often carries fields RINEX drops |
| Documents | PDF/A; plain text; CSV with a data dictionary | PDF/A is the archival PDF profile (ISO 19005) |

*Table 50.1 — Archival format choices for elevation data.*

Vendor raw formats are the hard case. The raw sonar datagram is the most valuable file in a hydrographic archive and it is proprietary. The practical policy is to archive the vendor file *and* its format specification document *and* a conversion to an open form (MB-System's processing formats, or an HDF5 or Parquet representation with a documented schema) *and* a note of which fields the conversion drops. Plan a **migration review** every five to ten years: if no maintained open reader exists for the vendor format, convert while one still does. The same applies to lidar vendor formats (RIEGL `.rxp`, Leica `.sdf`, Teledyne Optech `.range`) and to proprietary trajectory files.

**Fixity** is the archival term for evidence that a file has not changed. Compute a cryptographic digest—SHA-256 is the current default; MD5 is acceptable only as a legacy check—at ingest, store it in the metadata (STAC's `file:checksum`, a PREMIS fixity event, or a BagIt manifest), and re-verify on a schedule and on every copy. **BagIt** (RFC 8493, 2018) is the simplest packaging convention: a directory with a `data/` payload, a `manifest-sha256.txt` listing every file and its digest, and a `bag-info.txt` of key–value metadata; it is understood by every major repository and can be created with a few lines of Python. **PREMIS** (the Library of Congress's preservation metadata dictionary, version 3) records the events—ingest, fixity check, migration, virus scan—and the agents responsible, which is what an auditor asks for.

> **Try it.** Package a lidar delivery as a BagIt bag with SHA-256 fixity and verify it.
>
> ```bash
> pip install bagit
> # Convert vendor LAS to LAZ (lossless) first; keep both if storage allows.
> pdal translate strip_017.las strip_017.laz --writers.las.compression=true \
>     --writers.las.minor_version=4 --writers.las.dataformat_id=6
> # Create a bag around the delivery directory (in place).
> python3 -m bagit --sha256 --contact-name "Survey Archive" \
>     --external-description "Project X lidar: swaths, SBET, calibration, checkpoints, reports" \
>     project_x_delivery/
> # Later, or after a copy: verify payload fixity.
> python3 -m bagit --validate project_x_delivery/
> ```
>
> Expected outcome: `project_x_delivery/` now contains `bagit.txt`, `bag-info.txt`, `manifest-sha256.txt`, and `data/` holding the original files; validation prints nothing on success and lists any file whose digest differs. Keep `manifest-sha256.txt` in a second location; it is the smallest possible description of a multi-terabyte delivery that can prove whether the delivery is intact.

## 50.3 OAIS and trusted repositories

The **Open Archival Information System** reference model (CCSDS 650.0-M-3, December 2024; adopted as ISO 14721:2025, replacing the 2012 edition) is the vocabulary and functional model every serious archive uses, and it is worth learning because it names the things that go wrong. Data arrive as a **Submission Information Package** (SIP), are transformed into an **Archival Information Package** (AIP) with **Preservation Description Information**—provenance, context, reference (identifiers), fixity, and access rights—and are served as **Dissemination Information Packages** (DIPs). The model's functional entities are ingest, archival storage, data management, administration, preservation planning, and access; its central requirement is that content be **independently understandable** by its **designated community** without the producer's help. For an elevation archive, that requirement is exactly the minimum metadata set of [Chapter 49](ch49-metadata.md) plus the format documentation and the geoid grids (§50.6). The 2024 edition adds explicit *preservation objectives* and *preservation watch*—monitoring formats, software, and community expectations for the moment a migration becomes necessary—which formalizes the migration review recommended above.

**Trusted repository certification** makes the model auditable. **ISO 16363:2012** (*Audit and certification of trustworthy digital repositories*) is the full audit standard; **CoreTrustSeal** is the lighter, widely adopted certification (sixteen requirements covering organizational infrastructure, digital object management, and technology), renewed every three years. Certification does not guarantee that a repository's elevation data are good; it guarantees that the repository has a succession plan, verifies fixity, documents provenance, and will not vanish when a grant ends.

**National archives.** In the United States, **NOAA NCEI** archives bathymetry (multibeam, single-beam, lidar, the DCDB, and the historical smooth sheets), with NOAA Administrative Order 212-15 requiring that NOAA environmental data be archived; **USGS EROS** archives Landsat, aerial film, and the 3DEP lidar and DEMs; **NASA's DAACs** archive mission data—LP DAAC for SRTM, ASTER, and NASADEM, NSIDC DAAC for ICESat and ICESat-2, ORNL DAAC for GEDI—with a mandated level of reprocessing support; the **Planetary Data System** archives planetary DEMs ([Chapter 67](ch67-planetary-dems.md)). Elsewhere, **LINZ** (New Zealand), the **UK Environment Agency** (national lidar), **Geoscience Australia**, **NRCan**, **swisstopo**, and national hydrographic offices perform the same role with varying degrees of OAIS formality. **ESA** and **DLR** archive Copernicus and TanDEM-X raw and products.

**Community repositories.** **OpenTopography** (NSF-funded; Crosby, Arrowsmith, and Nandigam, 2020) archives and serves high-resolution topography from academic and agency sources, assigns DOIs, and provides on-demand processing; **Zenodo** (CERN) and **PANGAEA** (AWI/MARUM) take arbitrary research datasets with DOIs, with PANGAEA curating geoscience metadata; the **IHO DCDB** is the global archive for crowdsourced bathymetry and the deposit point for Seabed 2030 contributions. Where you have a choice of repository, prefer the one whose designated community will still want the data in thirty years.

<!-- figure: Figure 50.1 — The OAIS functional model drawn for an elevation survey: SIP (vendor delivery: raw sonar/lidar, trajectories, calibration, reports) → ingest (format validation, fixity, metadata extraction) → AIP (open-format copies, vendor originals, PDI, geoid grids) → DIP (COG/COPC/BAG with STAC records), with preservation planning watching formats and reference frames. -->

## 50.4 Versioning

A dataset that changes under a fixed name is not a dataset; it is a rumour. Versioning is the discipline of making every change visible, citable, and reversible.

### 50.4.1 Semantic versions for products

Borrow **semantic versioning** from software, with the meaning adapted: a **major** version changes when values change in a way that invalidates prior analyses (new vertical datum, new geoid, reprocessing with a different classifier, retraction of a source); a **minor** version adds coverage or companion layers without altering existing cells; a **patch** fixes metadata, nodata handling, or packaging without changing any elevation value. Publish the rule with the product. Copernicus DEM's release numbering (2019_1, 2021_1, 2022_1 and later), GEBCO's annual grids (GEBCO_2019 through GEBCO_2025), and ICESat-2's release numbers (R005, R006) are all workable schemes; what matters is that a user can state which version they used in one token and that the differences between versions are documented. [Chapter 55](ch55-public-products.md) lists versions for the major public products.

### 50.4.2 Per-tile change logs and supersession

Large products are updated tile by tile, and a global version number hides which tiles changed. Keep a **per-tile change log**: tile identifier, version, date, what changed (new source, re-edit, datum fix), and the checksum before and after. **Supersession** is the specific case where a newer dataset replaces an older one over an area; the record should name the superseded and superseding datasets, the area, the reason, and the date. NOAA's **National Bathymetric Source** (NBS), published as **BlueTopo**, is the model: every tile carries a *Contributor* layer identifying the source survey of each cell, each source has a documented rank, and the supersession decisions—why survey H13245 (2021) overrides H11890 (2008) here but not there—are recorded so that a cell's value can be traced to a survey and a rule ([Chapter 48](ch48-compositing.md)). Publish a "what changed since version *x*" raster alongside each release: the difference grid is cheap to compute and is the single most useful artefact for users doing change detection, who otherwise cannot distinguish geomorphic change from a reprocessing step ([Chapter 41](ch41-change-detection.md)).

### 50.4.3 Reproducible builds and content-addressed storage

A product is **reproducibly built** if running the archived pipeline on the archived inputs yields the archived output, byte for byte or within a declared tolerance. Achieving this requires pinned software versions (container image digests or lock files), fixed random seeds where algorithms are stochastic, deterministic parallelism, and recorded parameters. It is rarely achieved in full for elevation products—floating-point reductions differ between CPU counts, and some vendor software is not deterministic—so state the tolerance you did achieve (for example, "re-gridding reproduces cell values to within 1 mm").

**Content-addressed storage** names each object by the hash of its contents, so that identical data are stored once, any change produces a new address, and a version is simply a manifest of addresses. **Git LFS** and **DVC** bring this model to files alongside code; **LakeFS** applies it to object stores with git-like branches and commits; **Icechunk** (Earthmover, released October 2024 ⟨H⟩; version 1.0 in July 2025) applies it to Zarr arrays with atomic commits, so that a multi-terabyte DEM mosaic can be updated tile by tile and every past state remains readable by commit identifier. The Zarr v3 specification on which Icechunk builds separates array metadata from chunk storage in a way that makes such transactional layers possible. These tools solve the "silent reprocessing under the same name" problem structurally rather than by policy; the cost is a dependency on the tool's own format, which must itself be archived.

### 50.4.4 Dataset DOIs with versions

A **DOI** is a persistent identifier with a resolution service; it is not a guarantee that the bytes behind it are fixed. The DataCite schema supports versions explicitly: mint a DOI per version, link versions with `IsNewVersionOf`/`IsPreviousVersionOf`, and optionally register a **concept DOI** that resolves to the latest version. Zenodo does this automatically; OpenTopography and the NASA DAACs assign version-specific DOIs. The practice to avoid is a single DOI whose landing page's files are replaced in place—users who downloaded in 2022 and 2024 then have different data under the same citation and no way to know it. Record the version, the DOI, and the checksum together in every citation and every pipeline manifest.

## 50.5 Provenance

**Provenance** is the record of what produced a thing: which inputs, which processes, which agents, when. Lineage in [Chapter 29](ch29-processing-pipelines.md) is provenance seen from inside a pipeline; this section is about recording it so that a stranger can audit it.

### 50.5.1 W3C PROV and ISO lineage

The **W3C PROV** family (PROV-DM data model and PROV-O ontology, Recommendations of April 2013) is the general standard. Its three core classes are **Entity** (a dataset, a file, a parameter set), **Activity** (a processing step with a start and end time), and **Agent** (a person, organization, or software), connected by relations such as `wasGeneratedBy`, `used`, `wasDerivedFrom`, `wasAttributedTo`, and `wasAssociatedWith`. A DEM's provenance graph says: *DTM v2.1* `wasGeneratedBy` *gridding run 2024-03-02* which `used` *classified cloud v2.0* and *parameters.json* and `wasAssociatedWith` *PDAL 2.6.0*; *classified cloud v2.0* `wasDerivedFrom` *strip-adjusted cloud v1* by *classification run* `wasAttributedTo` *analyst J.*; and so on back to the raw swaths. PROV is serializable as JSON-LD or Turtle and can be queried, which an ISO lineage section cannot. ISO 19115's `LI_Lineage`—a statement plus ordered `LI_ProcessStep` elements each with a description, date, processor, and `LI_Source` references—captures the same facts in catalog-friendly form; generate it from the PROV graph rather than typing it.

### 50.5.2 STAC processing metadata and pipeline manifests

The STAC **processing** extension records `processing:lineage` (free text), `processing:software` (a map of name to version), `processing:level`, `processing:facility`, and `processing:datetime` on an Item; combined with `derived_from` links to the Items of the inputs, it gives a lightweight provenance graph across a catalog. The pipeline itself is the most precise provenance document: a **PDAL pipeline JSON** names every stage, its parameters, and the filenames; a **Snakemake** or **Nextflow** workflow names the rules, their inputs and outputs, and the environment per rule; a **GMT** or shell script does the same less formally. Archive the manifest with the output, together with the **container image** (by digest, not tag) or the **environment lock** (conda-lock, `requirements.txt` with hashes, `renv.lock`) that pins every library. A manifest without its environment is a recipe without the oven temperature.

> **Try it.** Capture provenance from a PDAL run automatically and emit a minimal PROV-JSON record.
>
> ```python
> import json, subprocess, hashlib, datetime as dt, platform
> def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
> pipe = json.load(open("make_dtm.json"))            # PDAL pipeline: readers.las -> filters -> writers.gdal
> t0 = dt.datetime.now(dt.timezone.utc).isoformat()
> subprocess.run(["pdal", "pipeline", "make_dtm.json", "--metadata", "run_meta.json"], check=True)
> t1 = dt.datetime.now(dt.timezone.utc).isoformat()
> inp = pipe["pipeline"][0]["filename"]; out = pipe["pipeline"][-1]["filename"]
> prov = {"prefix": {"ex": "https://example.org/prov/"},
>   "entity": {f"ex:{inp}": {"ex:sha256": sha(inp)},
>              f"ex:{out}": {"ex:sha256": sha(out)},
>              "ex:make_dtm.json": {"ex:sha256": sha("make_dtm.json")}},
>   "activity": {"ex:run1": {"prov:startTime": t0, "prov:endTime": t1,
>                "ex:host": platform.node(),
>                "ex:pdal_version": subprocess.run(["pdal","--version"],capture_output=True,text=True).stdout.strip()}},
>   "agent": {"ex:pdal": {"prov:type": "prov:SoftwareAgent"}},
>   "used": {"_:u1": {"prov:activity": "ex:run1", "prov:entity": f"ex:{inp}"},
>            "_:u2": {"prov:activity": "ex:run1", "prov:entity": "ex:make_dtm.json"}},
>   "wasGeneratedBy": {"_:g1": {"prov:entity": f"ex:{out}", "prov:activity": "ex:run1"}},
>   "wasDerivedFrom": {"_:d1": {"prov:generatedEntity": f"ex:{out}", "prov:usedEntity": f"ex:{inp}"}},
>   "wasAssociatedWith": {"_:a1": {"prov:activity": "ex:run1", "prov:agent": "ex:pdal"}}}
> json.dump(prov, open(out + ".prov.json", "w"), indent=2)
> ```
>
> Expected outcome: a `*.prov.json` next to the DTM that names the input, the pipeline file, the output, their SHA-256 digests, the PDAL version, host, and run interval, in a form that PROV tooling (for example the `prov` Python package) can load and that a human can read. The `run_meta.json` PDAL writes alongside holds every stage's resolved parameters; archive both.

### 50.5.3 Audit trails for chart products

Navigation products carry the strictest provenance requirements because they are legal documents. **S-100 exchange sets** package S-101 ENCs and S-102 bathymetric surfaces with an exchange catalogue (S-100 Part 17) listing every dataset, its edition and update number, issue date, and producer, and with digital signatures under the S-100 data protection scheme (Part 15) so that a receiving system can verify both integrity and origin. Each S-102 cell's `QualityOfBathymetryCoverage` record ([Chapter 49](ch49-metadata.md)) points to the source survey; the hydrographic office's own records trace the survey to its Descriptive Report and raw data. The chain from a displayed depth on a bridge to a sonar ping on a given date is, in principle, complete; it is what a court will ask for after a grounding ([Chapter 62](ch62-navigation-and-charting.md)).

## 50.6 Coordinate reference frames over time

Elevation archives have a problem generic archives do not: the numbers are only meaningful relative to reference surfaces and frames that are themselves versioned, and those versions are often not archived with the data.

A height labelled "NAVD88, GEOID12A" can be converted to any later realization *only if GEOID12A is still available*. NGS keeps its models online, but regional geoids, national hybrid models from smaller agencies, and the one-off local transformations that consulting projects use ("the client's site datum, defined by three benchmarks") are routinely lost. The rule is to **archive the transformation grids and parameters used** inside the AIP: the geoid or hydroid grid file (GTX, GGXF, or the agency's native format), the horizontal transformation grid (NTv2, NADCON, or the PROJ-data distribution's version), the VDatum or vyperdatum version and its model files for tidal conversions, and the PROJ or software version that applied them—with their own checksums. The **GGXF** (Gridded Geodetic data eXchange Format, OGC, 2024) and the PROJ-data repository versioned by release make this tractable for public models; for private ones, the grid is the only record.

Record **epochs** explicitly: the epoch of the horizontal coordinates in a dynamic frame (ITRF2020 at 2023.6; NAD83(2011) epoch 2010.0), the tidal datum epoch (the US National Tidal Datum Epoch 1983–2001, and its successor when adopted), and the geoid model's reference epoch where it has one. [Chapter 38](ch38-plate-motion-and-vlm.md) quantifies what epoch confusion costs: centimetres per year horizontally in many regions, millimetres to centimetres per year vertically in subsiding or rebounding ones, which over an archive's life accumulates to decimetres.

**Re-reduction of historical soundings** is the archival payoff of keeping reductions separate from observations. A nineteenth-century lead-line sounding was reduced to a chart datum defined by a local tide staff and a datum epoch long since superseded; if the archive holds the raw sounding, the time, the tide observations, and the staff-to-benchmark levelling, the sounding can be re-reduced to a modern datum with a quantified uncertainty ([Chapter 72](ch72-history.md)). If the archive holds only the reduced depth, the datum offset is an educated guess. Hare, Eakins, and Amante (2011) give the framework used by NOAA to assign vertical and horizontal uncertainty to legacy soundings by era and technology; applying it is possible only when the era and technology are known, which again is a metadata question.

## 50.7 Legal retention, evidence, and sovereignty

Elevation records are often **legal records**. Hydrographic surveys underlie charts that carry liability for groundings; a hydrographic office must be able to produce the survey, its Descriptive Report, and its processing history decades later. Lidar and photogrammetric surveys underlie floodplain maps, property boundaries, construction as-builts, and mining volumes, all of which are litigated. Retention schedules therefore come from law and policy as well as science. In the United States, federal records fall under the Federal Records Act and the National Archives' General Records Schedules and agency-specific schedules; NOAA's hydrographic survey records are scheduled as permanent, and NOAA's data management directive (NAO 212-15) requires archiving of environmental data at a NOAA data centre. National hydrographic offices under IHO conventions keep survey records indefinitely; IHO publication **C-55** (*Status of Hydrographic Surveying and Charting Worldwide*) depends on member states knowing what surveys they hold and when they were made. Contracts for commercial surveys should specify retention explicitly—who keeps the raw data, for how long, in what format, and who may access it—because the default is that the contractor's disk is reused.

**Data sovereignty** constrains where bits may live. Some states classify high-resolution bathymetry or terrain over sensitive areas and restrict export; the European Union's GDPR affects imagery and point clouds that can identify persons or private property; Indigenous data governance frameworks (the CARE principles; [Chapter 69](ch69-security-sovereignty-privacy-ethics.md)) assert collective rights over data about Indigenous lands and waters. An archive design must therefore record, per dataset, the jurisdiction of the data, the access constraints, and the storage regions permitted, and a cloud archive must be able to pin objects to a region. Sovereignty constraints are also a preservation risk: data that may be held only by one agency in one country are one budget cut from loss, and the mitigation—escrowed copies under access control—must be negotiated, not assumed.

## 50.8 Cost: tiers, compression, and what never to downsample

Storage is cheap relative to surveys and expensive relative to attention. The arithmetic matters because it determines what gets kept.

**Storage classes.** Cloud object stores offer tiers from "hot" (immediate access, roughly US$0.02 per GB-month in 2024 list prices for major providers) through infrequent-access and archive tiers to "deep archive" (retrieval in hours, roughly US$0.001 per GB-month, with minimum retention periods and retrieval fees). On-premises tape (LTO-9, 18 TB native per cartridge) remains the lowest cost per byte for cold data at scale and is what national archives use for their deep copies. The archival pattern is: raw and intermediates in deep archive with a hot copy of the manifests and metadata; products in a hot or infrequent tier for access; at least two geographically separated copies of everything (the Library of Congress and the Digital Preservation Coalition both recommend three, one on different media or with a different provider).

**Compression.** **LAZ** (LASzip; Isenburg, 2013) is lossless and typically reduces LAS files by a factor of roughly five to ten depending on point format and attribute entropy; there is no reason to archive uncompressed LAS. **COPC** is LAZ with a spatial index and costs almost nothing extra. For grids, lossless **DEFLATE** or **ZSTD** on floating-point elevations achieves modest ratios (often 1.5–3×) because the low-order mantissa bits are noise; the floating-point predictor (`PREDICTOR=3` in GDAL) helps. **LERC** (Limited Error Raster Compression; Esri, open-sourced 2016; in GDAL as `LERC`, `LERC_DEFLATE`, `LERC_ZSTD`) quantizes to a declared maximum error (`MAX_Z_ERROR`) and then compresses losslessly; with `MAX_Z_ERROR` set to a value small relative to the data's uncertainty (1 mm for a 10 cm product) it is effectively lossless for every analytical purpose and compresses two to five times better than DEFLATE. Declare the error in the metadata. Lossy image compression is acceptable for quicklooks and never for archival imagery that may be re-matched photogrammetrically.

**What to downsample versus never.** Downsample derived visualizations, overviews, and tiles freely; they are recomputable. Never downsample raw observations, trajectories, calibration records, or checkpoint tables. Full-waveform and water-column data are the hard case: their volume can exceed the point data by one to two orders of magnitude. The defensible policy is to keep them for a defined fraction of the survey (calibration lines, areas of interest, a random sample of strips) in full, and to keep documented reductions (decimated waveforms, water-column detections) for the rest, stating the rule.

**Energy.** Storage has a carbon cost that is small per byte and large in aggregate; deep-archive tiers and tape use far less energy per stored byte than hot disk, so the energy and cost arguments point the same way—cold raw, hot products.

> **Worked example.** A lidar project yields 1.0 × 10⁹ points. In LAS 1.4 point data record format 6 (30 bytes per point) that is 30 GB; in LAZ at a typical 6× it is about 5 GB. Stored hot for ten years at US$0.023 per GB-month: 30 GB × 0.023 × 120 ≈ US$83 uncompressed, ≈ US$14 compressed. Stored in deep archive at US$0.00099 per GB-month: 5 GB × 0.00099 × 120 ≈ US$0.59. Add the full waveforms at ~10× the point volume (≈ 50 GB compressed): ≈ US$6 for ten years in deep archive. Re-flying the project costs on the order of 10⁴–10⁵ times these figures. The economics never favour discarding raw data; the only real costs are organizational—someone must own the archive. (Prices are approximate 2024 list prices for major US-region object stores and will change; the ratios are the point.)

## 50.9 Rescue of historical data

Much of the elevation record is in formats and media that are failing. **Smooth sheets**—the final plotted sheets of NOS/Coast Survey hydrographic surveys from the 1830s onward—survive as paper and film and have been scanned by NCEI; their soundings were digitized for the NOS Hydrographic Survey database and remain, for most US coastal waters, the only bathymetry away from shipping channels ([Chapter 72](ch72-history.md)). **Lead-line and early echo-sounder soundings** in field books and on sheets elsewhere in the world have been digitized unevenly; GEBCO's TID 13 and 14 cells rest on them. **Aerial film** from the 1930s onward is held by USGS EROS, national mapping agencies, and military archives, and scanned at 14–25 µm by programs that will take decades at current funding; the film is the only pre-satellite record of the surface and is deteriorating (vinegar syndrome in acetate bases). **Magnetic tapes** hold early satellite and airborne data; the SRTM raw data were recorded on high-density tapes aboard the shuttle (roughly 12 TB) and were safely transcribed, but many 1970s–1990s airborne lidar and profiler datasets exist only on media no drive can read. **Early lidar** (1990s–2000s) often survives only as ASCII XYZ without trajectories or timestamps.

Rescue has three stages. **Capture**: scan the sheet or film at a resolution that resolves the smallest pen stroke or film grain (typically 400–800 dpi for sheets, 14–21 µm for film), read the tape with a working drive while one exists, and store the capture losslessly with fixity. **Georeference**: identify the sheet's projection, datum, and scale from its title block; measure the graticule and control-point ticks; fit a transformation and record its residuals; convert the historical datum to a modern one using the published or reconstructed shift, and record the uncertainty of that step separately. **Assign uncertainty**: following Hare, Eakins, and Amante (2011), assign horizontal and vertical uncertainties by era and technology—sextant three-point fixes versus Decca versus Loran-C versus GPS; lead line versus early echo-sounder versus corrected echo-sounder; staff-tide versus predicted-tide reduction—and attach them to every point as attributes so that compilers can weight the data honestly ([Chapter 48](ch48-compositing.md)). Jakobsson et al. (2012) describe doing exactly this for IBCAO version 3, where soundings from nineteenth-century expeditions, Soviet-era charts, and submarine transits were given source-dependent uncertainties and tracked in a provenance database.

> **Case file.** The Lunar Orbiter Image Recovery Project (2008–) recovered high-resolution Lunar Orbiter imagery of 1966–1967 from original analogue tapes that had been stored for decades, using refurbished Ampex FR-900 tape drives—the last working units—and digitizing at far higher fidelity than the 1960s photographic prints from which all intervening lunar maps had been made. The recovered frames supported new photogrammetric terrain models of the Moon ([Chapter 67](ch67-planetary-dems.md)). The lesson for terrestrial elevation archives is literal: the data were never lost, but the ability to read them very nearly was, and the recovery depended on hardware that no longer existed commercially. Migrate while the drives still spin.

<!-- figure: Figure 50.2 — A rescued 1930s smooth sheet: scanned image with graticule ticks marked, the digitized lead-line soundings colour-coded by assigned vertical uncertainty (1–3 m), and the same area in a modern multibeam survey, showing both the agreement in the channel and the systematic datum offset diagnosed from the title block. -->

## Then & now

The pattern across two centuries is that data are lost at every transition of medium, and that what survives is what someone chose to keep in a form that could be read without them. Paper **smooth sheets** and field books in the NOS archives survived because they were legal records of a chart; many of the field books that would allow re-reduction did not. **Magnetic tape** carried Landsat (from 1972), early airborne profilers, and SRTM (2000); the Landsat Global Archive Consolidation effort (from 2010) recovered millions of scenes from international ground stations' tapes before the drives disappeared, and the Lunar Orbiter recovery above shows how close such efforts run. The **digital archives** of NCEI and EROS (institutionalized through the 1990s) made fixity, metadata, and public access routine, and the DAAC system gave NASA missions mandated reprocessing. **Cloud object stores** (2010s–) changed the economics—deep-archive tiers made keeping raw data cheaper than deciding what to discard—and **content-addressed, versioned formats** (Zarr v3; Icechunk 2024 ⟨H⟩; LakeFS; COPC for point clouds) are making "which version did you use?" answerable by construction rather than by policy. Each transition also created a new failure mode—proprietary vendor raw, then dependence on a provider's survival—and the remedy has not changed: open formats, multiple copies, documented provenance, an institution that owns the archive.

## Validation & uncertainty

An archive can fail in ways that corrupt every analysis built on it, and the failures are testable.

**Fixity failures** (bit rot, truncated transfers, silently altered files). Test by re-verifying digests on a schedule and after every copy; the BagIt validation above is the minimal form. The expected rate of undetected corruption on modern object stores is very low, but transfers and local disks are where files break; verify at the destination, not the source.

**Format failures** (a vendor raw no reader can open; an HDF5 written with a compression filter nobody installs). Test by **periodic read-back**: open a sample of every format in the archive with an open-source reader each year and record the result in PREMIS events. A format that fails read-back triggers migration while the last proprietary reader still runs.

**Provenance gaps** (a product whose inputs or parameters cannot be identified). Test by **reproduction**: rebuild a sample of products from their archived inputs and manifests and compare—cell-by-cell for grids, point-by-point for clouds—reporting the maximum and RMS difference. A clean reproduction validates the manifest; a failed one locates the undocumented step.

**Reference-frame losses** (a geoid grid or local datum definition missing). Test by attempting the archived product's datum transformation with only archived resources; if it requires downloading a model from a live server, the archive is incomplete.

> **Uncertainty budget.** Vertical uncertainty added by archival shortcomings when a legacy dataset is reused (approximate; the first three rows follow the era-based approach of Hare, Eakins, and Amante, 2011):
>
> | Shortcoming | Typical added vertical uncertainty (1σ) |
> |---|---|
> | Lead-line sounding, era and reduction known | 0.3–1 m plus ~1–2 % of depth |
> | Lead-line sounding, reduction datum unknown | add 0.5–2 m (tidal datum ambiguity) |
> | Early echo-sounder, sound speed uncorrected | ~1–3 % of depth |
> | Lidar DTM, geoid model used but not archived | 0.05–0.3 m (model-to-model differences) |
> | Legacy DEM, horizontal georeferencing from scanned sheet | slope × horizontal residual (e.g., 10 % slope × 20 m = 2 m) |
> | Product reprocessed under the same name, version unknown | unbounded without a difference grid |
>
> Each row is a cost of a missing record, not of a bad measurement; the archive determines whether the measurement's own uncertainty is recoverable at all.

Report, for an archive: the fixity verification date and result; the formats held and the date each was last read back; for each product, the inputs, manifest, environment, and reproduction tolerance; the reference-frame resources held; and the retention and access constraints. Report, for a rescued dataset: the capture resolution, the georeferencing residuals, the datum conversion and its uncertainty, and the era-based uncertainty assigned to each observation.

## Software

**Open source:** **bagit-python** and the Library of Congress **Bagger** (BagIt packaging and validation); **DVC** and **Git LFS** (versioned data alongside code); **LakeFS** (git-like branching over object stores); **Icechunk** (transactional, versioned Zarr; caveat: a young format whose own specification must be archived); **Zarr** and **xarray** (chunked arrays with versioned specifications); **Entwine** and **PDAL** (COPC/EPT generation; `pdal translate` for lossless LAZ; `pdal info --metadata` for header provenance); **GDAL** (COG, LERC, ZSTD, GGXF, PROJ-data transformation grids); **MB-System** (reads most raw multibeam formats—the de facto preservation path for proprietary datagrams); **PROV Python** (`prov` package) and **ProvToolbox** (PROV serialization and visualization); **Snakemake** and **Nextflow** (workflow manifests with per-rule environments); **Zenodo**, **PANGAEA**, and **OpenTopography** deposit workflows (DOI minting with versions); **Archivematica** (OAIS-oriented ingest with PREMIS; heavyweight for small teams).

**Free but closed:** cloud providers' archive tiers and lifecycle policies (lock-in through retrieval fees and minimum retention), NOAA and NASA DAAC submission tools.

**Commercial:** **CARIS Bathy DataBASE** (versioned bathymetric source management with supersession rules); enterprise digital-asset-management and backup systems; Esri **ArcGIS** mosaic datasets (source tracking without content addressing).

## Standards & guides

- **CCSDS 650.0-M-3 (2024) / ISO 14721:2025**, *Reference Model for an Open Archival Information System (OAIS)* — archive functions, information packages, preservation planning.
- **ISO 16363:2012**, *Audit and certification of trustworthy digital repositories*; **CoreTrustSeal Requirements** (current 2023–2025 cycle) — repository certification.
- **W3C PROV-DM / PROV-O (2013)** — provenance data model and ontology.
- **STAC processing, file, and version extensions** — provenance, fixity, and supersession in STAC.
- **RFC 8493 (2018)**, *The BagIt File Packaging Format* — manifests and fixity.
- **PREMIS Data Dictionary for Preservation Metadata, v3** (Library of Congress) — preservation events and agents.
- **DataCite Metadata Schema 4** — versioned DOIs and related identifiers.
- **FAIR Guiding Principles** (Wilkinson et al., 2016) and **CARE Principles** (Carroll et al., 2020) — findability/reuse and Indigenous data governance.
- **NOAA Administrative Order 212-15** and NOAA data management directives — archiving of NOAA environmental data; **NARA General Records Schedules** — US federal retention.
- **IHO C-55** — status of surveying and charting; **IHO B-12** — DCDB crowdsourced bathymetry contribution.
- **IHO S-100 Part 15 (data protection) and Part 17 (exchange catalogue)** — signed, versioned chart product exchange.
- **OGC GGXF 1.0 (OGC 22-051r7, approved 2024)** — gridded geodetic data exchange for archiving geoid and transformation grids.
- **Library of Congress, *Sustainability of Digital Formats*** — assessments of LAS/LAZ, GeoTIFF, BAG, HDF5, NetCDF as archival formats.

## Pitfalls

- **Keeping only the final DEM** → storage budgeted on deliverables → reprocessing with a better geoid or classifier becomes impossible; test by asking whether the raw swaths, trajectories, and calibration can be located.
- **Vendor raw with no reader in ten years** → the format was convenient at acquisition → schedule read-back tests and migrate while an open reader exists.
- **A DOI whose files changed in place** → a bug fix uploaded over the original → checksum mismatch between downloads; mint a new version DOI.
- **Silent reprocessing under the same name** → operational convenience → users cannot distinguish geomorphic change from reprocessing; publish per-tile change logs and difference grids.
- **Geoid or local datum definition not archived** → it was "available online" → the product's heights become irreproducible; include the grid in the AIP.
- **Provenance as prose only** → lineage written after the fact → cannot be verified or queried; emit PROV or STAC processing metadata from the pipeline.
- **Single copy on one provider or one disk** → cost → fixity cannot be recovered after loss; keep three copies, two media or providers.
- **Full waveforms or water column discarded without a stated rule** → volume → irrecoverable; keep a defined sample and document the reduction.
- **Legacy data digitized without era-based uncertainty** → the compiler needed numbers → old soundings weighted like modern ones; assign uncertainties per Hare et al. (2011).
- **Retention left to the contractor by default** → contract silent on data custody → raw data gone when the project closes; specify custody, format, and duration.

## Key takeaways

- Archive the rawest data you can—observations, trajectories, calibration, control—in open, documented formats, with SHA-256 fixity and at least three copies; the deliverables are the least durable part of a project.
- Treat vendor raw formats as a migration liability: keep the specification with the data, keep an open-format conversion, and test read-back yearly.
- Use the OAIS vocabulary and a certified repository where one exists; "independently understandable" means the metadata of [Chapter 49](ch49-metadata.md) plus the format documentation plus the geoid grids.
- Version explicitly—semantic versions, per-tile change logs, supersession records on the NBS model, versioned DOIs—and publish difference grids between versions.
- Record provenance from the pipeline (PROV, STAC processing, manifests, pinned environments), not from memory; reproducibility within a stated tolerance is the test.
- Archive the reference-frame resources—geoid and transformation grids, epochs, tidal datum definitions—with the heights; without them the heights are not reproducible.
- Storage is cheap: deep-archive tiers and lossless compression make keeping everything cost a tiny fraction of re-surveying. The real cost is institutional ownership.
- Rescue historical data while media and drives survive, georeference it with recorded residuals, and assign era-based uncertainty so it can be used honestly.

## References

- Carroll, S. R., Garba, I., Figueroa-Rodríguez, O. L., et al. (2020). The CARE Principles for Indigenous Data Governance. *Data Science Journal* 19(1):43. doi:10.5334/dsj-2020-043.
- Consultative Committee for Space Data Systems (2024). *Reference Model for an Open Archival Information System (OAIS)*, Recommended Practice CCSDS 650.0-M-3. Washington, DC: CCSDS. (Adopted as ISO 14721:2025.)
- Crosby, C. J., Arrowsmith, J. R., and Nandigam, V. (2020). Zero to a trillion: advancing Earth surface process studies with open access to high-resolution topography. In Tarolli, P. and Mudd, S. M. (eds.), *Remote Sensing of Geomorphology*, Developments in Earth Surface Processes 23, pp. 317–338. Amsterdam: Elsevier.
- Hare, R., Eakins, B., and Amante, C. (2011). Modelling bathymetric uncertainty. *International Hydrographic Review* 6 (November 2011):31–42.
- Isenburg, M. (2013). LASzip: lossless compression of lidar data. *Photogrammetric Engineering & Remote Sensing* 79(2):209–217.
- Jakobsson, M., Mayer, L., Coakley, B., et al. (2012). The International Bathymetric Chart of the Arctic Ocean (IBCAO) Version 3.0. *Geophysical Research Letters* 39:L12609. doi:10.1029/2012GL052219.
- Kunze, J., Littman, J., Madden, E., Scancella, J., and Adams, C. (2018). *The BagIt File Packaging Format (V1.0)*, RFC 8493. IETF.
- Library of Congress (2015). *PREMIS Data Dictionary for Preservation Metadata*, Version 3.0. Washington, DC: Library of Congress.
- Moreau, L. and Groth, P. (2013). *Provenance: An Introduction to PROV*. Synthesis Lectures on the Semantic Web. San Rafael, CA: Morgan & Claypool.
- Moreau, L., Missier, P., et al. (2013). *PROV-DM: The PROV Data Model*. W3C Recommendation, 30 April 2013.
- ISO (2012). *ISO 16363:2012 Space data and information transfer systems — Audit and certification of trustworthy digital repositories*. Geneva: ISO.
- Wilkinson, M. D., Dumontier, M., Aalbersberg, I. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data* 3:160018. doi:10.1038/sdata.2016.18.
- Wulder, M. A., White, J. C., Loveland, T. R., et al. (2016). The global Landsat archive: status, consolidation, and direction. *Remote Sensing of Environment* 185:271–283. doi:10.1016/j.rse.2015.11.032.
- Earthmover (2024–2025). *Icechunk: transactional storage engine for Zarr*. Specification and documentation, icechunk.io (first release October 2024; version 1.0 with a stability commitment July 2025).
- Zarr Development Team (2023). *Zarr core specification version 3* (accepted via ZEP 1, May 2023). zarr-specs.readthedocs.io.
- NOAA Office of Coast Survey. *National Bathymetric Source and BlueTopo: product description and supersession rules*. Silver Spring, MD: NOAA. (verify)

# Chapter 42 — Object detection and semantic labelling of the surface

> **Part IX — Semantics, learning, and enhancement.** The first chapter of the semantics part: how meaning (ground, building, tree, wire, water, car, ship, pile) is attached to points, pixels, and cells, and why every DTM, obstacle database, and change interpretation downstream inherits the error rate of that labelling.

**In this chapter.** A point cloud or DSM is geometry without meaning; nearly every product described earlier—a DTM, a hydro-flattened surface, an obstacle file, a building model, a change map—needs a label on each point or cell first. You will be able to read and apply the main label schemes (ASPRS LAS classes including wires 13–16 and bridge deck 17, CityGML LoD classes, OSM tags, S-57/S-101 chart objects) and explain why they disagree; compute the geometric features (height above ground, normals, covariance eigenfeatures) that classical and learned classifiers both consume; choose between rule-based filters, random forests, and point-cloud or raster deep networks on the basis of density, sensor, and transfer risk; read the public benchmarks critically; and evaluate labels by their geometric consequences, because a roof point mislabelled "ground" is not a 1 % confusion-matrix entry but a 10 m bump in the DTM. The chapter closes with human-in-the-loop editing, QA/QC sampling with confidence intervals, and the economics of labelling.

## 42.1 Label schemes and why they disagree

A **label scheme** is a finite vocabulary of classes plus the rules for assigning them. Elevation work uses at least five families of schemes that were designed by different communities for different purposes, and most real projects must translate between two or three of them. The translations are where errors enter.

### 42.1.1 ASPRS LAS classification codes

The LAS specification (ASPRS, version 1.4, revision 15, 2019) defines the per-point classification field used by almost all airborne and many mobile lidar deliverables. In point data record formats 6–10 the field is a full 8 bits (0–255), with 0–63 reserved for the standard and 64–255 user-definable; legacy formats 0–5 carry a 5-bit class (0–31) with flag bits packed alongside. The classes that matter for DEM production:

| Code | Class | Notes for elevation products |
|---|---|---|
| 0 / 1 | Created, never classified / Unclassified | 0 means "not yet looked at"; 1 is often the catch-all for vegetation in sparse specs |
| 2 | Ground | The DTM class; the single most consequential label in the file |
| 3 / 4 / 5 | Low / medium / high vegetation | Height bands vary by project (e.g., 0–0.5 / 0.5–2 / > 2 m) |
| 6 | Building | Roofs and walls; rarely the ground-level footprint |
| 7 / 18 | Low point (noise) / High noise | Must be excluded from gridding |
| 8 / 12 | Reserved | Were Model key-point and Overlap in 1.1–1.3; overlap is now a flag bit |
| 9 | Water | Interacts with hydro-flattening ([Chapter 34](ch34-water-in-dems.md)) |
| 10 / 11 | Rail / Road surface | Whether ballast and pavement are "ground" is a spec decision |
| 13 | Wire – guard (shield) | Static/earth wire atop a transmission structure |
| 14 | Wire – conductor (phase) | Energised conductors; the class obstacle users care about |
| 15 | Transmission tower | Lattice towers and poles |
| 16 | Wire-structure connector | Insulators and hardware |
| 17 | Bridge deck | The deck only; abutments and piers are other classes |
| 19 | Overhead structure | Conveyors, canopies, mining equipment (R15) |
| 20 | Ignored ground | Ground near breaklines excluded from DTM gridding (R15) |
| 21 / 22 | Snow / Temporal exclusion | Snow cover; features present only at acquisition time (R15) |

Three features of the scheme bite. The **flags** (synthetic, key-point, withheld, overlap) are separate from the class; a point can be class 2 and withheld, and a gridder that ignores the bit will use it. The wire classes 13–16 and bridge deck 17 exist because the DTM, obstacle, and asset communities needed to say *different* things about the same points ([Chapter 33](ch33-wires-and-thin-structures.md), [Chapter 32](ch32-dsm-to-dtm.md)). And the standard says nothing about *how* to classify: two vendors delivering LAS 1.4 to the same specification can legitimately disagree about whether a stone retaining wall is ground or building, whether a culvert headwall is ground, and whether a parked car on a bridge is class 17.

### 42.1.2 CityGML, OSM, land cover, hydrography, and chart objects

**CityGML** (OGC, version 3.0, 2021) describes *objects*, not points: a building has a footprint, wall and roof surfaces, and installations, with geometric detail expressed through **levels of detail** (LoD0 footprint, LoD1 block, LoD2 roof shapes, LoD3 façades and openings). Converting LAS class 6 points to CityGML LoD2 is a reconstruction task (§42.5), and converting back loses the instance identity CityGML carried. **OpenStreetMap** tags (`building=*`, `highway=*`, `natural=water`, `power=line`) are a crowd-sourced open vocabulary with no formal geometric definition; they are useful priors and weak labels but not truth—a `building=yes` polygon may be a carport, a ruin, or ten years stale.

**Land-cover** schemes (CORINE, NLCD, ESA WorldCover) classify the *dominant cover of an area*, not the object at a point: a 10 m "built-up" pixel can be mostly road, lawn, and parked cars, while the lidar under it has ground, building, vegetation, and vehicle points. Mixing object and land-cover vocabularies is the commonest cause of nonsensical agreement statistics. **Hydrographic feature classes** (e.g., USGS NHD/3DHP flowlines and waterbodies) define what hydro-flattening must honour, and the **IHO S-57** object catalogue and its successor **S-101** define chart objects—`WRECKS`, `OBSTRN`, `UWTROC`, `SBDARE`, `DEPARE`—whose detection from multibeam data is the bathymetric equivalent of building extraction, governed by IHO S-44 feature-detection requirements ([Chapter 20](ch20-sonar.md), [Chapter 62](ch62-navigation-and-charting.md)).

> **Definitions that bite.** "Bridge" means at least four things across these schemes: in LAS 1.4, class 17 is the deck only; in a 3DEP-style DTM specification, bridges are removed and the terrain beneath interpolated; in CityGML, a `Bridge` is one object including piers; in S-101 a bridge over navigable water is a feature whose vertical clearance is an attribute. A classifier trained on one definition and scored against another reports "errors" that are translations, and a DTM built from a model that labelled piers as class 17 has holes where the piers stood. [Chapter 32](ch32-dsm-to-dtm.md) treats the definitions problem in full; the lesson here is that the scheme must be fixed in the specification *before* training data are made.

Schemes disagree because they answer different questions: what belongs in the bare-earth surface (DTM specs), what the object is and how it is modelled (CityGML), what covers the area (land cover), and what a navigator must avoid (S-101). A project that needs more than one should carry a documented mapping table with its many-to-one and one-to-many cases.

## 42.2 Features from geometry and imagery

Whatever the classifier, it operates on **features**: numbers per point, pixel, or neighbourhood that make classes separable. Deep networks learn their own, but the hand-crafted features remain the best way to understand what any classifier can and cannot see, and they still dominate production pipelines for ground, building, and wire extraction.

### 42.2.1 Height above ground and return attributes

The most informative feature for most classes is **height above ground** (HAG): the point's elevation minus a provisional ground surface, which is why most pipelines run a ground filter ([Chapter 30](ch30-point-cloud-classification.md)) before any other classification and refine ground afterwards. HAG separates low vegetation from canopy and roofs from pavements but cannot separate a 4 m hedge from a 4 m shed. **Return number**, **number of returns**, and **return ratio** help: vegetation yields multiple returns per pulse, roofs and pavements single returns, wires first returns with ground far below. **Intensity** (range- and incidence-corrected) distinguishes asphalt from concrete from grass, and water from almost everything near nadir. **Scan angle** matters because walls and trunks appear only off-nadir and because intensity and footprint vary with it.

### 42.2.2 Covariance eigenfeatures

For a point with a neighbourhood of $k$ points (or all points within radius $r$), compute the $3\times3$ covariance matrix of the neighbour coordinates and its eigenvalues $\lambda_1 \ge \lambda_2 \ge \lambda_3 \ge 0$. Their ratios describe the local shape: a wire or edge is one-dimensional ($\lambda_1 \gg \lambda_2 \approx \lambda_3$), a roof or pavement two-dimensional ($\lambda_1 \approx \lambda_2 \gg \lambda_3$), foliage three-dimensional. The standard dimensionless features (Weinmann et al. 2015; formulas in the Mathematics section) are **linearity**, **planarity**, **sphericity**, **omnivariance**, **anisotropy**, **eigenentropy**, **change of curvature**, and **verticality**. The eigenvector of $\lambda_3$ is the local **normal**; its deviation from vertical separates roofs from walls, and the dispersion of normals over a larger neighbourhood is a **roughness** measure separating mown grass from scrub.

Two design choices dominate. The **neighbourhood scale** must match the object: at $r = 0.5$ m a roof tile and a hedge both look planar; at $r = 5$ m the roof is planar and the hedge spherical. Weinmann et al. (2015) showed that a per-point optimal neighbourhood (minimum eigenentropy) beats any fixed scale, and most systems compute features at three to five scales and let the classifier combine them. The **density dependence** is the hidden trap: $k$-nearest-neighbour neighbourhoods shrink physically as density rises, so a model trained at 8 pts/m² sees different features at 2 pts/m² for the same roof. Fixed-radius neighbourhoods transfer better but become unstable at low density; this is why §42.7 insists on cross-density evaluation.

### 42.2.3 Raster and image features

Point features are complemented by raster features on a provisional DSM and DTM: slope and curvature, the **normalised DSM** (nDSM = DSM − DTM, the raster analogue of HAG), top-hat residuals, local relief, and texture statistics. Where co-registered imagery exists, spectral features add what geometry cannot: **NDVI** $=(\mathrm{NIR}-\mathrm{Red})/(\mathrm{NIR}+\mathrm{Red})$ separates a green roof from a tree of the same height and planarity; **NDWI** separates shallow water from wet sand. The caveat is registration: a 1 m misalignment between orthophoto and point cloud mislabels the first metre of every building edge. Sample image features from a **true orthophoto** (built on the DSM, not the DTM) or building edges are displaced by their height times the view angle ([Chapter 22](ch22-photogrammetry-sfm.md)).

> **Try it.** Compute covariance eigenfeatures, normals, and HAG for a LAZ tile with PDAL, then inspect the planarity/linearity histograms per class. Expected outcome: ground and building points cluster near planarity ≈ 1; high-vegetation points spread toward sphericity; wire points (if present) have linearity > 0.9 and HAG of tens of metres.
>
> ```json
> {
>   "pipeline": [
>     "tile.laz",
>     {"type": "filters.smrf", "slope": 0.2, "window": 16.0, "threshold": 0.45, "cell": 1.0},
>     {"type": "filters.hag_nn", "count": 6},
>     {"type": "filters.normal", "knn": 16},
>     {"type": "filters.covariancefeatures", "knn": 16, "threads": 4,
>      "feature_set": "Dimensionality,Verticality,Omnivariance,Eigenentropy"},
>     {"type": "writers.las", "filename": "tile_features.laz",
>      "minor_version": 4, "dataformat_id": 6,
>      "extra_dims": "all"}
>   ]
> }
> ```
>
> Then group the output by `Classification` and plot `Planarity` and `Linearity`. If building and ground overlap completely in every feature, no classifier—learned or not—will separate them from geometry alone, and you need imagery or context.

## 42.3 Classical pipelines

The classical approach assembles explicit rules and estimators whose behaviour can be reasoned about, tuned per terrain, and documented. Its weakness is brittleness; its strength is that when it fails you can usually say why.

**Rule-based classification** thresholds the features above: HAG > 2 m with planarity > 0.8 and a near-vertical normal becomes a building candidate; HAG > 0.5 m with low planarity becomes vegetation; HAG < 0.2 m becomes ground. Rules are fast and transparent—the backbone of TerraScan macros and PDAL `filters.assign`/`filters.range` chains—but encode one terrain's thresholds and fail on the next; terraced slopes, flat industrial roofs abutting pavement, and dense low scrub are the usual casualties.

**Morphological ground filters** (PMF, SMRF, CSF) and Axelsson's (2000) **progressive TIN densification**, which underlies TerraScan's ground routine, are covered in [Chapter 30](ch30-point-cloud-classification.md). They remain the dominant approach to the single most important label. Their parameters (maximum window, slope tolerance, iteration angle and distance) are explicit terrain assumptions, which makes failures diagnosable: a 60 m roof survives a 50 m maximum window; a 40° slope exceeds a 30° tolerance and loses its ground points.

**Region growing** seeds a segment and adds neighbours while a smoothness criterion holds, converting points into planar segments that are classified as a unit; **RANSAC plane fitting** repeatedly samples three points, fits a plane, counts inliers within a tolerance, and keeps the best—robust to the 50 % outliers a cluttered roof contains, but prone to spurious planes through vegetation when the tolerance is loose. Both are the standard entry to building reconstruction (§42.5).

**Statistical learning on hand-crafted features** was the state of the art from roughly 2005 to 2017 and is still the most cost-effective choice for many production tasks. A **random forest** (Breiman 2001) or gradient-boosted trees trained on 20–60 eigen-, height-, return-, and spectral features at several scales reach overall accuracies in the high 80s to low 90s per cent on urban ALS benchmarks (Niemeyer, Rottensteiner & Soergel 2014; Weinmann et al. 2015), train in minutes, expose auditable feature importances, and degrade gracefully across sensors if features are density-normalised. Per-point predictions are noisy, so they are smoothed with a **conditional random field** (CRF) or graph cut penalising label changes between neighbours (Niemeyer et al. 2014); the smoothing term is a prior that erases small objects, and its weight must be tuned against the smallest object the specification requires.

## 42.4 Deep learning on point clouds and rasters

Deep networks replace hand-crafted features with learned ones and, given enough labelled data, outperform forests on every public benchmark. What they do not automatically provide is transferability, interpretability, or calibrated confidence.

### 42.4.1 Point-cloud architectures

**PointNet** (Qi et al. 2017a) was the first network to consume unordered point sets directly—a shared multilayer perceptron per point and a symmetric max-pool for permutation invariance—but had no notion of local neighbourhood; **PointNet++** (Qi et al. 2017b) added hierarchical sampling and grouping and became the baseline for airborne lidar segmentation. **KPConv** (Thomas et al. 2019) defines a convolution on points with kernel points in Euclidean space and has been the strongest or near-strongest performer on ALS benchmarks such as DALES and OpenGF. **RandLA-Net** (Hu et al. 2020) uses random sampling and local feature aggregation to process on the order of $10^6$ points per pass—whole tiles rather than small cubes—at slightly lower accuracy. **Point Transformer** (Zhao et al. 2021) and its successors apply self-attention within local neighbourhoods and lead most current leaderboards. **Sparse voxel CNNs** (MinkowskiEngine, SPVCNN) discretise points into a sparse voxel grid for efficient 3D convolution and dominate autonomous-driving perception, transferring well to dense mobile mapping.

All of these depend on the density and extent of the training data: a network trained on 10 pts/m² ALS over a European city learns neighbourhoods of a particular physical size and sees a differently shaped world in 2 pts/m² or 500 pts/m² data. Resampling to a common density before inference is a partial fix; fine-tuning on target-density data is the reliable one.

### 42.4.2 Raster architectures and 2D–3D fusion

For DSMs, nDSMs, orthophotos, and SAR backscatter the problem is image segmentation, and the **U-Net** family with modern encoders, **DeepLabv3+**, and transformer segmenters such as **SegFormer** are the workhorses. Rasterising a point cloud into channels (max and min height, intensity, return count, nDSM) and segmenting in 2D is often competitive with 3D networks on airborne data at a fraction of the compute, because airborne clouds are nearly 2.5-D; it fails where the surface is multi-valued (bridges, overhangs, façades; [Chapter 35](ch35-voids-and-overhangs.md)). **Fused 2D–3D** designs project image features onto points or lift point features into image space and have won several ISPRS and IEEE GRSS Data Fusion contests; their cost is the registration requirement of §42.2.3.

### 42.4.3 Foundation models and their failure modes on elevation data

The **Segment Anything Model** (SAM; Kirillov et al. 2023) produces class-agnostic masks from prompts on ordinary images, and `segment-geospatial` applies it to orthophotos and to hillshaded or colour-mapped DSMs. **Prithvi** (NASA–IBM, 2023) and **Clay** (2024) are Earth-observation foundation models pretrained on multispectral imagery for fine-tuning. Their appeal is zero- or few-shot labelling without a training campaign. Their failure modes on elevation data are specific: SAM segments *appearance* and cuts a roof along a colour change or merges a flat roof with the adjacent car park; applied to a hillshade it segments the shading, so masks shift with azimuth; neither Prithvi nor Clay was pretrained on elevation channels, so a DSM fed as an extra band is out of distribution; none produces calibrated confidence; and all are too large for behaviour on an unusual landscape (karst, mangrove, informal settlement) to be predicted from the paper. They are excellent *proposal* generators for human-in-the-loop labelling (§42.8) and poor replacements for a validated classifier.

<!-- figure: Figure 42.1 — The same urban ALS tile labelled by (a) SMRF + rule-based classification, (b) random forest on multi-scale eigenfeatures with CRF smoothing, (c) KPConv trained on DALES, (d) SAM masks on the true orthophoto projected to points; with a difference panel highlighting where the four disagree (roof edges, low walls, hedges, bridge deck). -->


## 42.5 Object detection and instance segmentation

Semantic labelling says *what* each point is; **object detection** and **instance segmentation** say *which* object it belongs to, which is what asset registers, obstacle databases, and change interpretation need.

**Buildings.** The footprint-first route segments building pixels in imagery or an nDSM and regularises the mask into a polygon; the roof-first route segments class 6 points into planes by region growing or RANSAC, intersects adjacent planes to find ridges, and projects the outline to the ground to obtain LoD2 geometry. Global footprint products—Google's **Open Buildings** (Sirko et al. 2021; version 3, 2023, reports approximately 1.8 billion detections across Africa, South and Southeast Asia, Latin America, and the Caribbean) and the **Microsoft Building Footprints** (over a billion polygons, released by region from 2018)—came from segmentation networks on high-resolution satellite imagery. They are invaluable priors and poor truth: both report uncalibrated confidence scores, both are offset where off-nadir imagery was orthorectified without a DSM, and both carry the epoch of their imagery, not yours. A DTM pipeline that masks "buildings" from an external footprint layer leaves ghost roofs where the layer is stale and digs holes where it is over-complete.

**Trees.** Individual tree crown (ITC) delineation uses a canopy height model (CHM = DSM − DTM) with local-maximum detection and watershed or region growing (`lidR` implements the Dalponte, Silva, and Li algorithms), or direct 3D clustering. Dominant conifers in open stands are found at > 90 %; suppressed and clustered deciduous crowns are under-counted by 30–50 % in many comparisons, and the CHM smoothing kernel alone changes counts by tens of per cent ([Chapter 64](ch64-agriculture-forests-wetlands.md)).

**Vehicles, ships, and other transients.** Cars appear in ALS as 1.5 m planar blobs on class 11, are routinely misclassified as low vegetation or building, bias pavement cells upward by ~0.1–0.3 m, and are the clearest candidates for *temporal exclusion* (class 22). Ships are detected in SAR by constant-false-alarm-rate (CFAR) detectors and CNNs; fusion with **AIS** resolves identity and flags "dark" vessels ([Chapter 27](ch27-moving-and-transient-objects.md)).

**Power infrastructure, solar panels, antennas.** Wires are the canonical linear feature (linearity → 1, HAG tens of metres), extracted by eigenfeature thresholds and catenary fitting per span; towers are vertical clusters at span ends. Solar panels are planar, tilted, regular, and dark in the near infrared—easy to detect, definitionally awkward in a DTM. Masts are thin verticals that ALS records with few returns, so obstacle surveys specify density by target size ([Chapter 33](ch33-wires-and-thin-structures.md), [Chapter 62](ch62-navigation-and-charting.md)).

**Piles, sinkholes, and bathymetric objects.** On mine sites the objects *are* terrain, and whether a stockpile is "ground" depends on whether the product is a volume survey or a base DTM; use a site class in the 64–255 range and a toe-line per pile ([Chapter 65](ch65-mining-landfills-earthworks.md)). Closed depressions are found by sink filling with area and depth thresholds; false positives are noise pits and quarries, false negatives are depressions whose steep walls the ground filter removed—label error and geomorphic detection are the same thing. On multibeam data, wrecks, boulders, and debris are detected by residual-from-trend tests on the grid and texture classifiers on backscatter; the S-44 feature-detection requirement (1 m or 2 m cubes) turns this into a sampling-density question rather than a classifier question ([Chapter 20](ch20-sonar.md)).

<!-- figure: Figure 42.2 — Instance segmentation outputs on one scene: building polygons from footprint-first and roof-first methods overlaid on a true orthophoto, individual tree crowns from CHM watershed, catenary fits to wire points, and a pile toe-line; each with a count of instances and the disagreement between methods. -->

## 42.6 Benchmarks and datasets

Public benchmarks are how methods are compared, and their composition is why published accuracies do not transfer ([Appendix H](../appendices/appendix-h-datasets.md) gives access details).

| Dataset | Year | Sensor / scene | Size (approx.) | Classes | What it tests |
|---|---|---|---|---|---|
| ISPRS Vaihingen 3D | 2012–14 | ALS, German town, ~4–8 pts/m² | ~1.2 M pts | 9 | Urban ALS semantic labelling; small, heavily studied |
| Semantic3D | 2017 | TLS, Swiss urban/rural | ~4 billion pts | 8 | Dense terrestrial scenes |
| DALES | 2020 | ALS, Dayton, Ohio, ~50 pts/m² | ~505 M pts, 10 km² | 8 | Large-area airborne labelling incl. power lines and poles |
| OpenGF | 2021 | ALS, 9 terrain types, 4 countries | ~542 M pts, > 47 km² | 2 (ground / non-ground) | Ground filtering across terrain and density |
| SensatUrban | 2021 | UAV photogrammetry, 3 UK cities | ~3 billion pts, 7.6 km² | 13 | City-scale photogrammetric clouds |
| H3D (Hessigheim 3D) | 2021 | UAV lidar + mesh, German village, multi-epoch | ~ hundreds of M pts | 11 | Dense UAV lidar, mesh labelling, change |
| US3D / DFC2019 | 2019 | WorldView-3 stereo + ALS, Jacksonville & Omaha | ~100 km² | 5 (+ height) | Satellite stereo semantics and DSM estimation |
| STPLS3D | 2022 | Synthetic + real UAV photogrammetry | ~16 km² synthetic + real | up to 20 | Synthetic-to-real transfer |

Sources: Niemeyer et al. 2014; Varney, Asari & Graehling 2020; Qin et al. 2021; Hu et al. 2021; Kölle et al. 2021; Le Saux et al. 2019; the Semantic3D and STPLS3D papers. Point counts are approximate; check current releases.

Read these with three facts in mind. **Geography**: the sets are overwhelmingly European and North American temperate towns; 95 % on DALES says little about informal settlements, mangrove coasts, karst, or tundra. **Density and sensor**: DALES at ~50 pts/m² and Vaihingen at ~5 pts/m² are different worlds, and no public set covers the 0.5–2 pts/m² regime most national programmes delivered before 2015. **Leakage**: several sets split train and test as adjacent tiles of one city, so a model learns the local roofing material and tree species; a held-out tile is not a held-out *domain*. OpenGF is the welcome exception for ground filtering, spanning nine terrain types in four countries; it showed KPConv and RandLA-Net beating the classical filters on average but with large terrain-dependent variance (Qin et al. 2021).

Bathymetric object-detection sets lag far behind: labelled wrecks, boulders, and seabed classes exist in national archives but rarely as public benchmarks, and most published detectors are trained on a few hundred targets from one sonar on one shelf. Treat any published bathymetric detection accuracy as a single-survey result until shown otherwise.

## 42.7 Evaluation: metrics, geometric consequences, and transfer

### 42.7.1 Per-class metrics

The confusion matrix $C_{ij}$ (true class $i$, predicted $j$) yields per-class **precision** $C_{ii}/\sum_i C_{ij}$, **recall** $C_{ii}/\sum_j C_{ij}$, their harmonic mean **F1**, and **intersection over union** $\mathrm{IoU}_i = C_{ii}/(\sum_j C_{ij} + \sum_i C_{ij} - C_{ii})$. Overall accuracy is dominated by ground and vegetation (typically 80–90 % of points) and hides a 40 % IoU on wires; always report **mean IoU** and the per-class table. **Cohen's κ** corrects agreement for chance and is still common, though the land-cover community now prefers per-class quantities. **Boundary metrics**—F-score within a buffer of the true boundary, or mean distance between predicted and true outlines—matter because label errors concentrate at edges, and an outline displaced by 0.5 m costs nothing in IoU for a large building and everything for a footprint area or an eave height.

### 42.7.2 The geometric consequence of label error

The metric that matters for a DTM is not the IoU of the ground class but the elevation error that mislabelling induces, and the asymmetry is severe. A ground point mislabelled as non-ground (**omission**) removes a sample; if neighbouring ground remains, the interpolated surface barely changes, and if a whole region is removed (a terraced slope, a dune crest) the surface is smoothed over, costing perhaps 0.5–3 m locally. A non-ground point mislabelled as ground (**commission**) *adds* a false sample: one roof point adopted into class 2 on a 1 m grid creates a bump as high as the roof—5–10 m for a house, 30 m for a warehouse—spread over the interpolation footprint. Evaluation must therefore weight commission and omission differently, compute the **DTM difference** between DTMs built from predicted and from reference labels (RMSE, 95th percentile of |Δz|, count of cells exceeding 1 m), and check bias by stratum (slope class, land cover, distance to buildings).

> **Worked example.** A 1 km² urban tile has 8 × 10⁶ points, 25 % of them building (2 × 10⁶). A classifier reports 99.5 % recall for buildings, i.e., 0.5 % of building points (10,000) fall into other classes; suppose one in ten of those becomes class 2 (1,000 false ground points). Gridding at 1 m with a TIN-linear interpolator, each false ground point at roof height $h_r \approx 8$ m lifts the surface over roughly the area of the triangles touching it—call it 4–10 cells—by an amount decaying from $h_r$ at the point to 0 at the neighbours; the mean lift over 6 cells is about $h_r/3 \approx 2.7$ m. The DTM therefore carries ~6,000 cells (0.6 % of the tile) with mean error 2.7 m and peaks near 8 m, contributing $\sqrt{0.006 \times 2.7^2} \approx 0.21$ m to the tile-wide RMSE even if every other cell were perfect. A 1 m-DTM specification with RMSE$_z$ ≤ 0.10 m is already violated by a classifier whose building recall is "99.5 %". The remedy is a second-pass ground filter and a spike detector on the DTM (residual from a 5 × 5 median > 1 m), not a better confusion matrix.

### 42.7.3 Transfer across regions, sensors, and densities

A classifier's accuracy is a property of the (model, training domain, test domain) triple. Report at least: in-domain held-out tiles; **cross-region** (train city A, test city B); **cross-sensor** (linear-mode vs single-photon lidar, lidar vs photogrammetry); and **cross-density** (train at 8 pts/m², test at 2 and 50 pts/m², resampled and native). Degradations of 5–20 percentage points in mean IoU under domain shift are typical, with thin classes (wires, poles, fences) and ambiguous ones (low vegetation vs ground, bridge vs road) suffering most. Density normalisation, test-time augmentation, and fine-tuning on a few hundred local labelled points recover much of the loss cheaply; the point is to measure it rather than assume it away. [Chapter 43](ch43-traditional-vs-ml.md) treats spatial cross-validation and area of applicability in general.

## 42.8 Human-in-the-loop editing, QA/QC sampling, and labelling cost

No automated labeller meets a stringent DTM specification unaided; production pairs automation with human review. **Review-everything** passes every tile to an editor who inspects profiles and hillshades and reclassifies by hand—the historical norm for national programmes, costing hours per square kilometre in complex terrain (the figure is vendor- and market-dependent). **Flag-and-review** sends only regions flagged by low classifier confidence, by disagreement between two classifiers, or by a DTM spike detector; it cuts human effort by 70–90 % in reported deployments but depends on flagging being well calibrated, which §43.6 explains it rarely is by default. **Active learning** feeds editors' corrections back as training data, prioritising the points that would most reduce model uncertainty; it is the most data-efficient and needs an MLOps loop few survey firms have built.

Acceptance requires **QA/QC sampling with confidence intervals**. The standard design (Olofsson et al. 2014, written for land cover and directly applicable) is stratified random sampling by predicted class, independent reference labelling by an analyst who does not see the prediction, and per-class accuracy estimates with standard errors that respect the stratification. The sample needed to bound a class accuracy $p$ with half-width $E$ at 95 % confidence is $n \approx 1.96^2\,p(1-p)/E^2$; to show that ground commission is below 1 % with $E = 0.5$ % requires $n \approx 1.96^2 \times 0.01 \times 0.99 / 0.005^2 \approx 1{,}520$ sampled non-ground points. Sampling only where the editor happened to look is not QA.

**Labelling cost** is the hidden budget line. Reference labels of benchmark quality cost minutes to tens of minutes per thousand points in dense multi-class scenes (Kölle et al. 2021 and Hu et al. 2021 report effort for H3D and SensatUrban), which is why benchmarks are small and weak labels (OSM, footprint products, automated pre-labels) are tempting. The rule is that reference data for *evaluation* must be independently and carefully produced even when training data are weak; a model evaluated against the labels it learned from looks better than it is.

> **Case file.** The 2019 IEEE GRSS Data Fusion Contest (US3D) asked teams to produce semantic labels and a DSM from WorldView-3 stereo over Jacksonville and Omaha, scored against airborne lidar. The semantic winners reached mean IoU in the high 70s to low 80s per cent; the DSM track showed the same models' *height* errors concentrated at building edges and tree canopies—the classes with the best labels—because the label was right while the stereo-matched height under it was not (Le Saux et al. 2019). Label accuracy and geometric accuracy are different quantities; measure both.


## Then & now

- **Manual stereoplotter compilation ⟨H⟩.** From the 1930s to the 1990s an operator at an analogue or analytical stereoplotter set the floating mark on the ground between trees and traced contours and breaklines by eye; semantics were applied by a trained human at every point, and labelling cost was the whole cost of mapping.
- **Morphological and TIN filters (1990s–2000s).** With airborne lidar, ground extraction became an algorithm: slope-based and morphological filters, Axelsson's progressive TIN densification (2000), then PMF (2003), SMRF (2013), and CSF (2016). The ISPRS filter test (Sithole & Vosselman 2004) was the first public benchmark and already showed the terrain-dependent failures that persist today.
- **Statistical learning on eigenfeatures (c. 2005–2017).** Random forests and boosted trees on multi-scale covariance features with CRF smoothing (Niemeyer et al. 2014; Weinmann et al. 2015) made full-scene multi-class labelling routine.
- **Point-cloud deep learning (2017–).** PointNet (2017), PointNet++, KPConv (2019), RandLA-Net (2020), and Point Transformer (2021), with large labelled sets (DALES 2020, OpenGF 2021, SensatUrban 2021) making airborne benchmarks meaningful.
- **Foundation models (2023–).** SAM, Prithvi, and Clay offer prompt-based or fine-tuned labelling with little local training data; promising for proposal generation, unvalidated for production on elevation data.
- **The LAS class list grew to say what the DTM needed said.** LAS 1.0 (2003) had classes 0–12; LAS 1.4 (2011) added wires 13–16, bridge deck 17, and high noise 18; revision 15 (2019) added 19–22. Each addition records a definitional dispute production had to resolve.

## Mathematics

**Covariance eigenfeatures.** For a neighbourhood $\mathcal{N}$ of $k$ points with centroid $\bar{\mathbf{p}}$, the covariance matrix is
$$\Sigma = \frac{1}{k}\sum_{\mathbf{p}_i \in \mathcal{N}} (\mathbf{p}_i - \bar{\mathbf{p}})(\mathbf{p}_i - \bar{\mathbf{p}})^\mathsf{T},$$
with eigenvalues $\lambda_1 \ge \lambda_2 \ge \lambda_3 \ge 0$ and eigenvectors $\mathbf{e}_1, \mathbf{e}_2, \mathbf{e}_3$. The dimensionless features of Weinmann et al. (2015), using normalised eigenvalues $e_i = \lambda_i / (\lambda_1 + \lambda_2 + \lambda_3)$ where indicated, are

$$
\begin{aligned}
\text{linearity } L_\lambda &= \frac{\lambda_1 - \lambda_2}{\lambda_1}, &
\text{planarity } P_\lambda &= \frac{\lambda_2 - \lambda_3}{\lambda_1}, &
\text{sphericity } S_\lambda &= \frac{\lambda_3}{\lambda_1}, \\
\text{omnivariance } O_\lambda &= (\lambda_1 \lambda_2 \lambda_3)^{1/3}, &
\text{anisotropy } A_\lambda &= \frac{\lambda_1 - \lambda_3}{\lambda_1}, &
\text{eigenentropy } E_\lambda &= -\sum_{i=1}^{3} e_i \ln e_i, \\
\text{change of curvature } C_\lambda &= \frac{\lambda_3}{\lambda_1 + \lambda_2 + \lambda_3}, &
\text{verticality } V &= 1 - |\langle \mathbf{e}_3, \hat{\mathbf{z}} \rangle|, &
L_\lambda + P_\lambda + S_\lambda &= 1 .
\end{aligned}
$$

The optimal neighbourhood size $k^*$ of Weinmann et al. is the $k$ (searched over, e.g., 10–100) that minimises $E_\lambda$, favouring the scale at which the local structure is most clearly one-, two-, or three-dimensional.

**Confusion matrix to IoU and κ.** With $C_{ij}$ the count of points of true class $i$ predicted as $j$, $N = \sum_{ij} C_{ij}$, $r_i = \sum_j C_{ij}$, $c_j = \sum_i C_{ij}$:
$$\mathrm{OA} = \frac{\sum_i C_{ii}}{N}, \qquad \mathrm{IoU}_i = \frac{C_{ii}}{r_i + c_i - C_{ii}}, \qquad \kappa = \frac{\mathrm{OA} - p_e}{1 - p_e}, \quad p_e = \frac{\sum_i r_i c_i}{N^2}.$$

**CRF smoothing.** A pairwise conditional random field assigns labels $\mathbf{y}$ by minimising
$$E(\mathbf{y}) = \sum_i \psi_u(y_i) + \mu \sum_{(i,j) \in \mathcal{E}} \psi_p(y_i, y_j),$$
where $\psi_u(y_i) = -\ln P(y_i \mid \mathbf{x}_i)$ is the classifier's negative log-probability, $\psi_p = [y_i \ne y_j]\exp(-\|\mathbf{x}_i - \mathbf{x}_j\|^2 / 2\sigma^2)$ penalises differing labels on similar neighbours, and $\mu$ trades evidence against coherence. Larger $\mu$ removes isolated errors and isolated true objects alike.

**Sampling-based accuracy with confidence intervals.** For stratified random sampling with strata $h$ (predicted classes), stratum weights $W_h = N_h/N$, and sample proportions $\hat{p}_h$ of correctly labelled points in stratum $h$ from $n_h$ samples, overall accuracy and its standard error are
$$\hat{\mathrm{OA}} = \sum_h W_h \hat{p}_h, \qquad \mathrm{SE}(\hat{\mathrm{OA}}) = \sqrt{\sum_h W_h^2 \frac{\hat{p}_h(1-\hat{p}_h)}{n_h - 1}},$$
and a 95 % interval is $\hat{\mathrm{OA}} \pm 1.96\,\mathrm{SE}$ (Olofsson et al. 2014 give the user's and producer's accuracy estimators and area-adjusted error matrices).

## Validation & uncertainty

Errors in semantic labelling arise from five sources, and a validation plan should test each.

1. **Definitional error.** Training labels encode one definition (bridge = deck; ballast = ground) and the specification requires another. Detect it by a confusion matrix whose "errors" concentrate in definitionally ambiguous classes; avoid it by writing the §42.1 mapping table first.
2. **Feature error.** Misregistered imagery, density-dependent neighbourhoods, uncorrected intensity, and a bad provisional ground corrupt features before any classifier sees them. Detect by per-class feature histograms across tiles of different density; a planarity distribution that shifts with density is a transfer failure waiting to happen.
3. **Model error.** Imperfect generalisation even in-domain. Measure on held-out tiles with per-class IoU, boundary F-score, and the DTM-difference statistics of §42.7.2.
4. **Domain shift.** Deployment differs from training in geography, sensor, density, season, or epoch. Measure by cross-region and cross-sensor tests; estimate exposure by comparing deployment and training feature distributions (the dissimilarity index of [Chapter 43](ch43-traditional-vs-ml.md)).
5. **Reference error.** The "truth" has its own error rate—a few per cent at boundaries, far more for ambiguous classes—and a model cannot be shown to exceed its reference. Estimate by double-labelling a subset and reporting inter-annotator agreement.

**What to report.** The scheme and mapping table; the training domain (locations, sensors, densities, epochs); per-class precision/recall/IoU with sample-based confidence intervals; boundary metrics for buildings; DTM-difference statistics (RMSE, 95th percentile, cells > 1 m) between predicted-label and reference-label DTMs; results stratified by slope and land cover; cross-domain results if the model was not trained locally; and the QA/QC sampling design with $n_h$ per stratum.

> **Uncertainty budget.** Indicative contributions to error in a 1 m urban/suburban lidar DTM traceable to labelling (your project's values come from the procedure in §42.7.2):
>
> | Source | Typical magnitude | Spatial pattern |
> |---|---|---|
> | Building commission into ground (false ground) | 2–10 m local spikes; 0.1–0.3 m tile RMSE contribution | Isolated, near roof edges and low buildings |
> | Low vegetation / scrub commission into ground | +0.1 to +0.5 m bias | Patchy, follows cover |
> | Ground omission on steep or terraced slopes | 0.5–3 m smoothing error | Linear, follows breaks |
> | Bridge/culvert definitional mismatch | 2–15 m over the feature | Along transport corridors |
> | Vehicles averaged into pavement | +0.05 to +0.3 m | Car parks, roads at acquisition hour |
> | Water misclassified as ground (noisy returns) | ±0.2 to ±1 m | Within water bodies, remedied by hydro-flattening |
>
> The first row dominates RMSE, the third and fourth the maximum error, the second the bias. Checkpoint RMSE on open flat ground ([Chapter 53](ch53-accuracy-assessment.md)) sees none of them—which is why the NVA/VVA split exists and why semantic validation is still needed on top of it.

> **Rule of thumb.** For DTM purposes, weight a ground-commission error roughly ten times a ground-omission error when choosing an operating point: it is almost always better to drop a true ground point than to admit a false one, because the interpolator recovers from gaps far better than from spikes. The rule fails on sparse data (< 1 pt/m²) and on narrow features (levee crests, road cuts) where omission removes the only samples that define the feature.

## Software

**Open source:** PDAL (`filters.smrf`/`pmf`/`csf`, `filters.covariancefeatures`, `filters.hag_*`, `filters.assign`; the production backbone for classical pipelines; no built-in learned classifier—pair with scikit-learn or a point-cloud network). lidR (R; ground, CHM, ITC delineation; memory-bound on large catalogues without chunking). CloudCompare (CANUPO dimensionality classifier, CSF plugin, interactive editing; scripting is limited). Open3D-ML, torch-points3d, Pointcept (PyTorch frameworks with KPConv, RandLA-Net, Point Transformer and benchmark loaders; fast-moving APIs, GPU required). segment-geospatial (SAM on rasters; appearance-based masks need geometric checks). Raster Vision and TorchGeo (raster segmentation pipelines). scikit-learn, XGBoost, LightGBM (forests and boosted trees on hand-crafted features; still the best cost–accuracy trade-off for many tasks).

**Free but closed:** Esri's downloadable deep-learning packages for point-cloud classification (tied to ArcGIS licences; training domain usually undocumented).

**Commercial:** TerraScan (Terrasolid; macro-based classification plus a learned classifier; the de facto airborne production standard). LP360 AI (GeoCue). Esri ArcGIS Pro 3D Analyst and 3D Basemaps. Trimble eCognition (object-based image analysis). Bentley Orbit 3DM and Leica Cyclone 3DR (mobile and terrestrial). Global Mapper Pro (low-cost classification; fewer tuning parameters).

## Standards & guides

- **ASPRS, LAS Specification 1.4 – R15 (2019).** Classification codes (incl. 13–16 wires, 17 bridge deck, 19–22 added in R15), flag bits, and the 8-bit class field of formats 6–10.
- **USGS, Lidar Base Specification (2024 rev. A, or current revision).** Minimum class set for 3DEP deliverables, classification accuracy and consistency requirements, handling of bridges, water, and overlap in the DTM.
- **OGC CityGML 3.0 Conceptual Model (2021).** Building, bridge, tunnel, vegetation, water, and transportation classes and the LoD concept.
- **IHO S-57 (ed. 3.1) and S-101 (ed. 1.x) feature catalogues; IHO S-44 Ed. 6.1.0 (2022).** Chart object classes that bathymetric detection must populate, and the feature-detection requirements that govern it.
- **ISPRS benchmark protocols** (Vaihingen/Toronto; Sithole & Vosselman 2004 filter test) and IEEE GRSS Data Fusion Contest rules: the de facto evaluation protocols, with known limits on domain coverage.
- **Olofsson et al. (2014) good-practice recommendations** for sample-based accuracy assessment.

## Pitfalls

- **Training on one density and deploying on another** → $k$-NN neighbourhoods change physical size, so features and learned filters see a different world → test on resampled and native data at the deployment density; prefer fixed-radius, multi-scale features; fine-tune locally.
- **Trusting benchmark numbers from European and North American towns** → the public sets under-represent most of the world's terrain and building styles → run a cross-region test on your own scene before accepting a model; budget for local labels.
- **Labelling "bridge" (or "ballast", "retaining wall") differently from the DTM specification** → the training instructions and the product specification were written by different people → write the class mapping table first, and check the confusion matrix for errors concentrated in definitionally ambiguous classes.
- **Evaluating labels but never the DTM** → confusion matrices are easy to produce and DTM differencing requires a reference DTM → always build DTMs from predicted and reference labels and report their difference statistics and spike counts.
- **Data leakage between train and test tiles of one scene** → adjacent tiles share roofing materials, tree species, sensor, and epoch → hold out whole scenes, and report cross-scene results separately.
- **Treating OSM or footprint products as truth** → they are convenient and look authoritative → use them as weak training labels or priors only; evaluate against independently produced reference labels of your own epoch.
- **Smoothing (CRF, morphological closing) with a weight tuned for appearance** → it removes the small objects the specification requires (poles, small sheds, culvert headwalls) → set the smoothing strength against the minimum object size and test recall on small instances specifically.
- **Accepting a vendor's QA where the sample was "points the editor looked at"** → convenience sampling is not a probability sample → require stratified random sampling with documented strata sizes and independent reference labelling.

## Key takeaways

- Labels are hypotheses with error rates; write the scheme and the mapping between schemes into the specification before any data are labelled.
- Height above ground, return attributes, and multi-scale covariance eigenfeatures explain most of what any classifier can see; understand them even if you deploy a network.
- Classical filters and random forests remain cost-effective and diagnosable; deep networks win in-domain and must be shown to transfer across region, sensor, and density.
- Evaluate semantics by geometric consequence: build the DTM from predicted and from reference labels and report the difference, the spike count, and the stratified bias.
- A roof point admitted into ground costs metres; a ground point dropped costs centimetres—set operating points asymmetrically.
- Hold out whole scenes and other sensors, not adjacent tiles; report cross-domain results.
- QA/QC is stratified random sampling with confidence intervals and independent reference labelling, sized to the error rate you need to demonstrate.

## References

- American Society for Photogrammetry and Remote Sensing (2019). *LAS Specification 1.4 – R15*. ASPRS, Bethesda, MD.
- Axelsson, P. (2000). DEM generation from laser scanner data using adaptive TIN models. *International Archives of Photogrammetry and Remote Sensing* 33(B4/1):110–117.
- Bosch, M., Foster, K., Christie, G., Wang, S., Hager, G. D. & Brown, M. (2019). Semantic stereo for incidental satellite images. *IEEE Winter Conference on Applications of Computer Vision (WACV)*, 1524–1532.
- Breiman, L. (2001). Random forests. *Machine Learning* 45(1):5–32.
- Hu, Q., Yang, B., Xie, L., Rosa, S., Guo, Y., Wang, Z., Trigoni, N. & Markham, A. (2020). RandLA-Net: Efficient semantic segmentation of large-scale point clouds. *IEEE/CVF CVPR*, 11108–11117.
- Hu, Q., Yang, B., Khalid, S., Xiao, W., Trigoni, N. & Markham, A. (2021). Towards semantic segmentation of urban-scale 3D point clouds: A dataset, benchmarks and challenges. *IEEE/CVF CVPR*, 4977–4987. (SensatUrban)
- Kirillov, A., Mintun, E., Ravi, N., Mao, H., Rolland, C., Gustafson, L., Xiao, T., Whitehead, S., Berg, A. C., Lo, W.-Y., Dollár, P. & Girshick, R. (2023). Segment Anything. *IEEE/CVF ICCV*, 4015–4026.
- Kölle, M., Laupheimer, D., Schmohl, S., Haala, N., Rottensteiner, F., Wegner, J. D. & Ledoux, H. (2021). The Hessigheim 3D (H3D) benchmark on semantic segmentation of high-resolution 3D point clouds and textured meshes from UAV LiDAR and multi-view-stereo. *ISPRS Open Journal of Photogrammetry and Remote Sensing* 1:100001.
- Le Saux, B., Yokoya, N., Hänsch, R., Brown, M. & Hager, G. (2019). 2019 Data Fusion Contest [Technical Committees]. *IEEE Geoscience and Remote Sensing Magazine* 7(1):103–105.
- Niemeyer, J., Rottensteiner, F. & Soergel, U. (2014). Contextual classification of lidar data and building object detection in urban areas. *ISPRS Journal of Photogrammetry and Remote Sensing* 87:152–165.
- Olofsson, P., Foody, G. M., Herold, M., Stehman, S. V., Woodcock, C. E. & Wulder, M. A. (2014). Good practices for estimating area and assessing accuracy of land change. *Remote Sensing of Environment* 148:42–57.
- Open Geospatial Consortium (2021). *OGC City Geography Markup Language (CityGML) Part 1: Conceptual Model Standard*, version 3.0. OGC 20-010.
- Qi, C. R., Su, H., Mo, K. & Guibas, L. J. (2017a). PointNet: Deep learning on point sets for 3D classification and segmentation. *IEEE CVPR*, 652–660.
- Qi, C. R., Yi, L., Su, H. & Guibas, L. J. (2017b). PointNet++: Deep hierarchical feature learning on point sets in a metric space. *Advances in Neural Information Processing Systems* 30.
- Qin, N., Tan, W., Ma, L., Zhang, D. & Li, J. (2021). OpenGF: An ultra-large-scale ground filtering dataset built upon open ALS point clouds around the world. *IEEE/CVF CVPR Workshops*, 1082–1091.
- Sirko, W., Kashubin, S., Ritter, M., Annkah, A., Bouchareb, Y. S. E., Dauphin, Y., Keysers, D., Neumann, M., Cisse, M. & Quinn, J. (2021). Continental-scale building detection from high resolution satellite imagery. arXiv:2107.12283.
- Sithole, G. & Vosselman, G. (2004). Experimental comparison of filter algorithms for bare-Earth extraction from airborne laser scanning point clouds. *ISPRS Journal of Photogrammetry and Remote Sensing* 59(1–2):85–101.
- Thomas, H., Qi, C. R., Deschaud, J.-E., Marcotegui, B., Goulette, F. & Guibas, L. J. (2019). KPConv: Flexible and deformable convolution for point clouds. *IEEE/CVF ICCV*, 6411–6420.
- Varney, N., Asari, V. K. & Graehling, Q. (2020). DALES: A large-scale aerial LiDAR data set for semantic segmentation. *IEEE/CVF CVPR Workshops*, 186–187.
- Weinmann, M., Jutzi, B., Hinz, S. & Mallet, C. (2015). Semantic point cloud interpretation based on optimal neighborhoods, relevant features and efficient classifiers. *ISPRS Journal of Photogrammetry and Remote Sensing* 105:286–304.
- Zhao, H., Jiang, L., Jia, J., Torr, P. & Koltun, V. (2021). Point Transformer. *IEEE/CVF ICCV*, 16259–16268.

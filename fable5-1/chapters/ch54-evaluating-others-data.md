# Chapter 54 — Evaluating other people's data when you lack the full story

> **Part XI — Validation, quality, and judging data.** [Chapter 52](ch52-ground-truth.md) described reference data and [Chapter 53](ch53-accuracy-assessment.md) the formal assessment; this chapter is for the common case where you have neither a checkpoint table nor a trustworthy report—only a file and a deadline.

**In this chapter.** Most elevation data you will use was made by someone else, for some other purpose, and arrives with metadata ranging from thin to wrong. This chapter is a forensic manual for that situation. You will learn to triage a DEM, point cloud, or bathymetric grid from the file alone (CRS and vertical-reference clues, units, quantization, nodata, pixel convention, tiling, compression, header dates and software signatures); to run hillshade and derivative sweeps that expose interpolation ghosts, contour terraces, stripes, tile seams, smearing, boresight sawtooth, refraction smiles, and heave; to test internal consistency on lakes, runways, roads, and bridges and to estimate effective resolution from the spectrum; to cross-check against ICESat-2, benchmarks, other DEMs after co-registration, OpenStreetMap, imagery, and water-level records; to infer provenance from texture; to judge accuracy claims and read a survey report between the lines; to apply the contractual lens of acceptance testing; and to write a fitness-for-use memo that says what you tested, what you found, what you could not test, and how much to inflate the uncertainty for the use at hand. The stance throughout: every delivered dataset is a hypothesis.

## 54.1 Triage from the file alone

Spend thirty minutes with `gdalinfo`, `pdal info`, or the BAG/NetCDF header first; most fatal problems are visible there.

**Coordinate reference system and vertical reference.** Read the horizontal CRS and check it against the extent: a file claiming UTM zone 17N whose coordinates would place it in the Atlantic has the wrong zone or hemisphere flag; geographic coordinates with longitudes 0–360 instead of ±180 are common in ocean products. The vertical CRS is more often missing than wrong. The first test is the sea: if the data include coastline, open water should sit near zero in an orthometric or tidal datum. If the sea surface sits at a constant non-zero value that matches the local geoid undulation $N$ (−30 m along the US east coast, +45 m in parts of the Alps, +60–75 m near New Guinea; look it up with any geoid model), the heights are ellipsoidal and nobody said so ([Chapter 9](ch09-vertical-datums.md)). Inland, compare a few spot heights against a known benchmark or a second DEM: a smooth, slowly varying offset of tens of metres is a geoid; a constant offset of a few decimetres is a datum realization or tidal datum difference; an offset that varies with terrain is not a datum problem at all.

**Units.** A DEM in feet looks like a DEM in metres with the relief exaggerated by 3.28. Check the maximum against known summits, or the elevation of a known lake; US county and state products in US survey feet are common, and some mix feet vertically with metres horizontally, which a `gdalinfo` unit tag may or may not reveal ([Chapter 4](ch04-names-and-definitions.md)). Depths may be positive down or negative up; S-102 and BAG are heights positive up (depths negative), many legacy grids are the reverse, and a sign error inverts the seafloor.

**Quantization and data type.** An integer data type (Int16 in SRTM, DTED, and many national products) quantizes to 1 m; a histogram of values with only integer bins, or a Float32 file whose values are all multiples of 0.01 or 0.1, tells you the precision at which the data were stored or originally produced, regardless of the current type. A Float32 file with integer-valued cells was produced as integers and later converted; its vertical precision is 1 m whatever the metadata claims. Quantization also produces terracing on gentle slopes visible in the hillshade (§54.2).

**Nodata.** Check that the declared nodata value is actually used, that it does not collide with real data (a nodata of 0 destroys sea level and lake surfaces; −9999 is safe on Earth, 3.4 × 10³⁸ is a sign of unset Float32), and that voids have not been silently filled; a void filled with a plane or a smooth interpolation has a distinctive texture (§54.2) and a void filled from another source has a different noise character inside a sharp boundary ([Chapter 35](ch35-voids-and-overhangs.md)).

**Pixel convention.** GeoTIFF's `GTRasterTypeGeoKey` distinguishes `PixelIsArea` (the coordinate is the cell's upper-left corner) from `PixelIsPoint` (the coordinate is the cell centre); SRTM and many 1″ products are point-registered, lidar DEMs are usually area-registered, and GDAL applies a half-pixel shift when it reads a `PixelIsPoint` file. A file whose tag is wrong, or whose producer ignored the convention when resampling, is misregistered by half a cell—15 m for a 1″ product—which appears as an aspect-dependent elevation difference against any other dataset ([Chapter 10](ch10-projections-and-resampling.md), [Chapter 44](ch44-resolution-and-sampling.md)).

**Tiling, seams, and compression.** Note the tile scheme; seams between separately processed tiles show as lines in the hillshade and steps across the boundary. Lossy compression (JPEG-in-TIFF for elevation is rare but happens; aggressive lossy LAZ-like schemes; low-bit-depth web tiles) leaves blockiness at 8 × 8 or 16 × 16 cell periods detectable in a high-pass filter. Nearest-neighbour overviews look noisy when zoomed out and are not evidence of noise in the base data.

**Dates and software signatures.** TIFF tags (`TIFFTAG_DATETIME`, `TIFFTAG_SOFTWARE`), GDAL metadata domains, LAS header fields (`System Identifier`, `Generating Software`, file creation day/year, point data record format, global encoding bits for GPS time type), BAG XML metadata, and NetCDF `history` attributes tell you what wrote the file and sometimes when the data were acquired. A LAS file with `Generating Software = TerraScan` and GPS week time (not adjusted standard GPS time) is older or poorly configured; one with point format 6–10 and a WKT CRS is LAS 1.4 and post-2011; a GeoTIFF with `Software = ArcGIS 10.2` was last touched around 2014. None of this is proof, but it dates the processing; a 2024 file date on a 2008 acquisition is a flag to find the real acquisition date ([Chapter 49](ch49-metadata.md), [Chapter 47](ch47-file-formats.md)).

> **Try it.** A five-minute triage of a GeoTIFF DEM with GDAL: CRS, pixel convention, type, nodata, and a value histogram.
>
> ```bash
> gdalinfo -stats -hist -mm dem.tif | sed -n '1,60p'     # CRS, GeoKeys, AREA_OR_POINT, type, nodata, min/max, histogram
> gdalinfo -json dem.tif | python3 -c "import json,sys; j=json.load(sys.stdin); print(j['metadata'].get('', {}).get('AREA_OR_POINT'), j['bands'][0].get('noDataValue'), j['bands'][0]['type'])"
> # fraction of cells with integer values (quantization check)
> python3 - <<'EOF'
> import rasterio, numpy as np
> with rasterio.open("dem.tif") as src:
>     a = src.read(1, masked=True).compressed()
> print("integer-valued fraction:", np.mean(np.isclose(a, np.round(a))).round(3),
>       "  multiples of 0.01:", np.mean(np.isclose(a*100, np.round(a*100), atol=1e-3)).round(3))
> EOF
> ```
>
> Expected: `AREA_OR_POINT=Point` on 1″ global products and `Area` on most lidar DEMs; an integer-valued fraction near 1.0 reveals metre quantization regardless of the Float32 type.

## 54.2 Hillshade and derivative sweeps

The eye is the best artefact detector available, provided it is shown the right picture. A single hillshade at the default azimuth of 315° hides everything aligned north-west; a **multi-azimuth sweep** (hillshades at 0°, 45°, 90°, 135°, and a low sun angle of 15–25°) and a **multi-directional composite** reveal linear features in any orientation. Then look at **slope**, which turns small steps into bright lines; **curvature** or a high-pass residual (DEM minus its 5 × 5 or 9 × 9 mean), which removes relief and leaves only the texture; and **aspect** on flat ground, which turns metre-scale noise into a random colour field and a tilt into a uniform one. Examine each at native resolution over several terrain types, not only at full extent.

What the sweep reveals, by signature ([Chapter 57](ch57-visualizing-dems.md) covers the rendering):

- **Interpolation ghosts**: triangular facets (TIN interpolation of sparse points), star or spoke patterns around isolated points (inverse-distance weighting), bull's-eyes (spline overshoot), and a "melted" look where a void was filled smoothly.
- **Contour terraces**: flat treads and steep risers at regular elevation intervals, with slope histograms peaked at zero and at a few discrete values; the product was interpolated from contours (Wise 2000) or quantized to integers and then smoothed.
- **Stripes**: regular linear banding at the strip spacing of a lidar or photogrammetric block (roll or range bias between swaths), at the along-track spacing of a satellite sensor (ASTER, SPOT), or at the ascending/descending crossing geometry of InSAR; stripes in SRTM at ~800 m period from mast oscillation were partly corrected in later versions.
- **Tile edges**: straight-line steps at round-number coordinates; the processing was per-tile with different parameters or sources.
- **Smearing and over-smoothing**: ML-corrected or heavily filtered DEMs lose ridge crests, round valley floors, and leave building-sized plateaus where structures were partly removed; the high-pass residual is nearly empty while the texture of a real DTM at the same resolution is not ([Chapter 45](ch45-super-resolution.md)).
- **Resampling blur**: features softened in one axis only (anisotropic resampling), or a Moiré pattern where a grid was resampled near its own resolution.
- **Surface type**: buildings and tree crowns present means DSM; building footprints flattened to ground means DTM with building removal; buildings present but trees removed (or vice versa) means a hybrid that needs a name ([Chapter 32](ch32-dsm-to-dtm.md)).
- **Lidar boresight sawtooth**: at swath edges in overlap, a periodic up-down pattern aligned with the flight direction (roll or scan-angle error); in the across-track direction, a difference growing linearly toward the swath edge.
- **Sonar refraction smiles and frowns**: in multibeam grids, the across-track profile curls up (smile) or down (frown) at the outer beams, so adjacent lines show a ribbed pattern at the line spacing; a sound-speed error ([Chapter 20](ch20-sonar.md)).
- **Heave and motion residuals**: along-track undulations of a few decimetres at wave period (heave filter or latency), or a corrugation at the ping rate; in airborne data, a long-wavelength along-track sag from GNSS trajectory error.
- **Water surface noise and false bottoms**: speckle on lakes in a DSM from lidar (specular dropouts interpolated), or in SDB a cloud-shadow or sunglint texture that follows the image, not the seabed ([Chapter 23](ch23-satellite-derived-bathymetry.md)).

<!-- figure: Figure 54.1 — Gallery of six hillshade/high-pass panels, each with its artefact labelled: TIN facets, contour terraces, swath stripes, tile seam, refraction smile in MBES, ML smearing over buildings. -->

## 54.3 Internal consistency

Having looked, measure; these tests need no external data.

**Flat-surface tests.** Select lakes, reservoirs, runways, large parking lots, and salt flats with polygons from OpenStreetMap or by hand. On each, compute the mean, standard deviation, slope of a fitted plane, and the NMAD of residuals from that plane. A lidar DTM on a runway should show σ of a few centimetres and a plane slope under 1 %; a 1″ global DEM on a large lake should show σ under 1 m for TanDEM-X-derived products and 1–3 m for SRTM; a tilt across a lake of more than its length × 10⁻⁴ (10 cm per km) in a lidar product is a trajectory or datum problem; and a lake with a non-zero plane slope in a hydro-flattened product means the flattening was done per tile. The histogram of residuals on the flat is the noise distribution of the product in its best case.

**Lake-level consistency across tiles.** A lake that spans a tile boundary must have the same elevation on both sides; it often does not, by the amount of the tiles' independent adjustment. Record it.

**Road crowns and bridges.** Profile along a highway: the crown should be continuous, with grades within design limits (typically ≤ 6–8 % on major roads) and no steps at tile or strip edges. Where a road crosses a river on a bridge, note what the product does—bridge deck retained (DSM behaviour), removed with the channel continuous (hydro-enforced DTM), or removed and interpolated as a ramp (common and wrong)—and whether it does the same thing everywhere ([Chapter 32](ch32-dsm-to-dtm.md), [Chapter 34](ch34-water-in-dems.md)).

**Water edges.** The DEM elevation at the shoreline polygon should equal the water-surface elevation within the noise; a systematic offset means the shoreline and DEM are from different dates or datums, or the DEM was flattened at the wrong level.

**Histogram of elevations.** A histogram at fine bin width exposes quantization (spikes at integer values), preferred values from contour interpolation (spikes at contour elevations), and a wall at the nodata or clipping value. A slope histogram with a spike at zero and holes is contour-derived or terraced.

**Spectral analysis for effective resolution.** The posting of a grid is not its resolution ([Chapter 44](ch44-resolution-and-sampling.md)). Compute the radially averaged power spectrum of a detrended, windowed block (a few hundred cells square) of the DEM. Natural topography follows an approximate power law $P(k) \propto k^{-\beta}$ with $\beta$ typically between 2 and 3 (Perron, Kirchner & Dietrich 2008); the **effective resolution** is roughly the wavelength at which the spectrum departs from that law—rolling off faster (the product was smoothed or interpolated at a coarser scale than its posting) or flattening into a white-noise floor (the posting is finer than the information). A 30 m product whose spectrum rolls off at a 90 m wavelength has an effective resolution near 90 m, which is the honest number to use for slope and drainage work; a "2 m" DEM resampled from 10 m data shows a knee at 10 m. Comparing the spectrum with that of a known-good product over the same area (lidar at the same posting) makes the reading unambiguous.

> **Worked example.** *Flat-surface test on a reservoir.* A 1 m DTM is clipped to a 2.1 km × 0.8 km reservoir polygon buffered inward by 30 m (n = 1.4 × 10⁶ cells). Results: mean 312.44 m; σ 0.09 m; fitted plane slope 0.00018 (0.18 m per km) toward the north-east; NMAD about the plane 0.04 m; 0.3 % of cells deviate by more than 0.5 m, clustered along the eastern shore. Reading: the σ of 9 cm includes the tilt; the NMAD of 4 cm is the product's noise on a specular surface, consistent with a QL2 lidar; the 18 cm/km tilt is too large for a hydro-flattened product and too small for a geoid artefact—it matches a strip-to-strip bias between two flight lines that cross the reservoir, confirmed by the sweep. The eastern-shore outliers are emergent vegetation. Conclusion for the memo: noise ≈ 4 cm, relative tilt ≈ 0.2 m/km in this block, hydro-flattening claimed in metadata but not applied here.

## 54.4 External cross-checks

One independent external source exposes what internal tests cannot: a datum offset, a scale error, a wrong epoch ([Chapter 52](ch52-ground-truth.md)).

**ICESat-2 and GEDI.** For any land DEM coarser than a few metres, pull ATL06/ATL08 segments over the extent, filter (strong beam, night, high confidence, low slope, low canopy), convert the ellipsoidal heights with a named geoid, and compute median, NMAD, and the slope/aspect dependence of the differences. A median offset that matches the geoid is a datum finding; one of a few decimetres is a realization or epoch finding; an NMAD far above the claimed accuracy is a noise finding. On an open, flat subset, ICESat-2 bounds the product's absolute bias to a decimetre or two with a few hundred segments, which is better than most vendor checkpoint sets. GEDI is the fallback for latitudes within ±51.6° where ICESat-2 tracks are sparse over the area of interest, with metre-level expectations.

**Benchmarks.** NGS datasheets and their national equivalents give published orthometric heights at marks whose descriptions say whether the disc is flush with the ground. A dozen flush marks on stable ground give a few-centimetre bias check, not a noise estimate; read their datum realization, do not assume it ([Chapter 52](ch52-ground-truth.md) §52.5).

**Other DEMs over stable terrain with co-registration.** Difference the product against the best available independent DEM (national lidar, Copernicus GLO-30, a previous survey) over terrain that has not changed. Before interpreting the difference, **co-register** with the Nuth & Kääb (2011) method: regress $\Delta h / \tan\theta$ on aspect $\psi$ to recover the horizontal shift $(a, b)$ and vertical offset $c$, apply it, iterate until the shift is below a tenth of a cell, and then examine what remains: a residual trend with elevation is a scale or atmospheric error (common in satellite stereo and InSAR); a tile-shaped pattern is processing; a land-cover-shaped pattern is penetration or filtering; a strip-shaped pattern is calibration. xdem and demcoreg do this in a few lines (Shean et al. 2016; Hugonnet et al. 2022); a half-cell shift found this way usually settles the pixel-convention question.

**OpenStreetMap and imagery.** Roads, buildings, water polygons, and runways from OSM supply the flat surfaces of §54.3 and a test of horizontal registration (road centrelines should follow the crown line in the slope map). Dated imagery shows whether a quarry, subdivision, or reservoir existed when the DEM was made, dating the acquisition when the metadata does not ([Chapter 37](ch37-time-scales-of-change.md)).

**Tide gauges and water levels for bathymetry.** For a bathymetric grid, compare the depth at a tide gauge location or at a surveyed pier with the gauge's datum relationships (MLLW–MSL–NAVD88 offsets published by NOAA CO-OPS and equivalents) to confirm the sounding datum; compare overlapping older surveys in NCEI or EMODnet archives; and check a few charted depths from the ENC against the grid, remembering that charted depths are shoal-biased and generalized, so a grid that is uniformly *deeper* than the chart by a few decimetres may be correct ([Chapter 62](ch62-navigation-and-charting.md)).

> **Case file.** Sandy Island, a 24 km feature charted in the Coral Sea since the nineteenth century and present in GEBCO, several coastline datasets, and web maps, was found not to exist when RV *Southern Surveyor* crossed its charted position in November 2012 and recorded depths near 1,400 m (Seton et al. 2013). It had propagated from an 1876 whaling report through chart compilations into digital products, each inheriting the last without a source check. Any compiled grid carries features whose only provenance is a prior compilation, and the external check that would have caught this—one independent sounding, one satellite image—was cheap.

## 54.5 Inferring provenance from texture

When the metadata does not say where a DEM came from, the DEM usually does. Each production method leaves a signature at native resolution (see also [Chapter 55](ch55-public-products.md)).

| Source | Posting | Texture and tell-tales |
|---|---|---|
| SRTM (v3/NASADEM) | 1″/3″ | C-band DSM; speckle-like noise of 1–3 m on flat ground; voids (filled in v3) in steep terrain and over water; integer metres; residual ~800 m striping in older versions; February 2000 snapshot (vegetation and buildings present, pre-2000 features absent) |
| ASTER GDEM v2/v3 | 1″ | Optical stereo DSM; strongest noise of the global DEMs (σ several metres on flat ground); pits and bumps; scene-boundary steps; cloud-related anomalies; stacking of many dates |
| ALOS AW3D30 | 1″ | PRISM stereo DSM; crisper than SRTM; buildings and tree canopies visible; cloud masks filled from other sources; 2006–2011 |
| TanDEM-X / Copernicus GLO-30/90 | 0.4″–3″ | X-band InSAR DSM; low noise (< 1 m) on open ground; phase-noise speckle in low-coherence areas (dense forest edges, water); edited water bodies flattened; 2011–2015; editing of implausible structures and flattening of water bodies and airports in the Copernicus edition (Copernicus DEM Product Handbook, GEO1988-CopernicusDEM-SPE-002, Issue 5.0) |
| Airborne lidar DTM | 0.5–2 m | Smooth, buildings removed, cm-level noise; TIN facets in low-density areas (under dense canopy, over water); strip edges; bridge handling varies |
| Airborne lidar DSM | 0.5–2 m | Buildings and trees present with sharp edges; intensity-independent; no occlusion smearing |
| UAS SfM | 2–20 cm | Very fine texture; vegetation as blobs; doming over the block; melted or bulging edges; moving objects as ghosts |
| Satellite stereo (WorldView, Pléiades) | 0.5–2 m | DSM with building lean artefacts, matching failures (holes) on homogeneous surfaces and in shadow; smooth fills |
| Contour-derived | Any | Terraces; slope histogram with spikes; "ghost" contours visible in curvature; flat hilltops and valley floors between contours |
| Chart-derived bathymetry | 50 m–1 km | Contour terraces; smooth interpolation between sparse soundings; shoal bias; survey-boundary steps; features present only at charted soundings |
| MBES grid | 0.5–50 m | Across-track ribbing at line spacing if refraction is uncorrected; nadir stripe; detail scaling with depth (beam footprint) |
| Altimetry-predicted bathymetry (e.g., SRTM15+, GEBCO away from ship tracks) | 15″–1′ | Smooth, long-wavelength texture (≥ 10–15 km) with "ship track" ribbons of real detail where soundings exist |
| Satellite-derived bathymetry | 2–30 m | Follows image texture: cloud shadows, sunglint, turbidity plumes; depth capped at a few times Secchi depth; smooth seaward of the limit |
| ML-corrected (FABDEM, CoastalDEM, DeltaDTM) | 1″–3″ | Parent product's texture with vegetation and buildings subtracted; over-smooth in cities, residual blocks, tile-pattern differences; parent artefacts inherited |

*Table 54.1 — Texture signatures by provenance. Build your own gallery over a familiar area.*

The GEBCO Type Identifier grid lets you check a compilation's own account of provenance against the texture ([Chapter 48](ch48-compositing.md)): a region labelled "multibeam" with 15 km-smooth texture has been downsampled or mislabelled.

<!-- figure: Figure 54.2 — Same 10 km × 10 km area rendered as hillshades from SRTM, ASTER GDEM, AW3D30, Copernicus GLO-30, lidar DTM, and FABDEM, with the high-pass residual beneath each, illustrating the signatures of Table 54.1. -->

## 54.6 Judging claims

Decompose each accuracy claim into statistic, reference, sample, strata, and independence ([Chapter 53](ch53-accuracy-assessment.md)); what is missing is usually what matters.

**"Accuracy 10 cm" without a test** is a specification or a datasheet, not a result; ask for the checkpoint table. **Vendor QC versus independent QA**: a producer's check against its own control, base station, and geoid tests only part of the budget ([Chapter 52](ch52-ground-truth.md)); ask who collected the reference, tied to what. **Sample size**: 8 points, 12 points, "selected checkpoints"—apply the chi-square interval and translate the claim into "consistent with 7–19 cm." **Extrapolation from roads**: an NVA on pavement says nothing about forest, marsh, or steep terrain; look for the VVA and for any residual map. **Reading between the lines** of a survey report: which flights were reflown and why; which strips were "adjusted to fit"; whether the calibration report predates or postdates the acquisition; whether the tide model was verified by a gauge; whether crosslines met the requirement or were waived; whether "hydro-flattened" is stated as a procedure or as an aspiration; and whether the accuracy statement quotes a standard by edition.

A red-flags list, in rough order of seriousness:

- No vertical datum, or "WGS 84" as the only vertical statement.
- Accuracy quoted without a statistic, a sample size, or a reference source.
- Checkpoints that were also control, or collected by the producer with shared infrastructure.
- Acquisition date absent or given as a year; a file date much later than the apparent surface date.
- A DSM described as a DTM or "bare earth" with buildings still present (or a DTM with bridges interpolated as ramps).
- Internal tests failing where they should pass: tilted lakes, stepped tile edges, terraces, strip stripes.
- Metadata copied from another project (wrong county, wrong sensor, wrong year).
- A product claimed to be "corrected" or "enhanced" by a method with no validation outside the training region ([Chapter 43](ch43-traditional-vs-ml.md)).
- A bathymetric grid with no sounding datum, no survey dates, and no uncertainty layer.

None is disqualifying alone; the flags direct the tests, they do not replace them.

## 54.7 The legal and contractual lens

When the dataset was procured, there is a specification, and the evaluation becomes **acceptance testing** against it ([Chapter 68](ch68-legal-issues.md), [Chapter 70](ch70-specifications-guided-tour.md)). The USGS Lidar Base Specification defines deliverables (swaths, classified point cloud, DEM, breaklines, metadata, checkpoint survey report, accuracy report), acceptance criteria by quality level (NVA, VVA reported, relative accuracy, density, classification accuracy, hydro-flattening rules), and the roles: the producer performs QC and the USGS or its contractor performs independent QA with its own tests before acceptance into 3DEP. NOAA's HSSD sets the hydrographic equivalents—TPU compliance with the required order, crossline percentages, feature verification, Descriptive Report content—with field QC, Processing Branch QA, and a formal survey acceptance process. S-44 orders are the language of international hydrographic contracts, and the contract should name the order *and* the feature-detection and search requirements, which are often forgotten.

The practical checklist for a reviewer with contractual authority: (1) obtain the specification and the edition named in the contract; (2) map every deliverable to a file and every acceptance criterion to a test; (3) run the independent tests of this chapter and [Chapter 53](ch53-accuracy-assessment.md) rather than re-reading the producer's report; (4) classify each finding as *non-conformance* (fails a stated criterion), *deviation* (meets the letter but not the intent, or a criterion the contract failed to state), or *observation*; (5) decide on acceptance, conditional acceptance with cure, or rejection, in writing, with the evidence; (6) keep the test data and scripts with the record ([Chapter 50](ch50-archiving-and-provenance.md)). Aim for an **ISO/IEC 17025** mindset—traceable references, documented methods, recorded uncertainties, producer separated from tester—even without accreditation. Rejection is rare and expensive; a documented deviation with inflated uncertainty is the usual, legitimate outcome if the use can tolerate it.

## 54.8 Writing a fitness-for-use memo

The output is a short document a non-specialist can act on—not an accuracy report, not a rejection letter, but a statement of what the dataset is, what it is not, what you tested, what you found, what you could not test, and whether it is fit for a named use. Two to four pages with figures is right.

```markdown
# Fitness-for-use memo — <dataset name / identifier / version>

**Prepared by / date / for:** <reviewer>, <ISO date>, <requesting party and intended use>

**1. What it is (as determined, not as claimed)**
- Surface type: <DSM / DTM / bathymetric surface; bridges, buildings, water treatment as observed>
- Source and method (inferred/declared): <e.g., airborne lidar, ~2 pls/m², leaf-off; declared in metadata; texture consistent>
- Acquisition date(s): <declared; corroborated by imagery/features?>
- Horizontal CRS / vertical reference: <as read from file; sea-level and benchmark tests; geoid model; epoch>
- Posting and effective resolution: <posting; spectral/visual estimate>
- Extent, voids, fills, nodata handling

**2. What it is not**
- <e.g., not hydro-flattened despite metadata; not bare earth under dense canopy; not a navigation product>

**3. Tests performed and results**
| Test | Where | Result | Interpretation |
|---|---|---|---|
| File triage | whole | <CRS, units, quantization, pixel convention> | <finding> |
| Hillshade/derivative sweep | <tiles> | <artefacts found> | <cause> |
| Flat-surface tests | <lakes, runways> | σ, tilt, NMAD | <noise, strip bias> |
| External check: ICESat-2 / benchmarks / reference DEM | <n segments/points> | median, NMAD, slope dependence | <datum, bias, noise> |
| Co-registration shift | <stable terrain> | <dx, dy, dz> | <pixel convention / registration> |
| Claims review | report/metadata | <what is supported> | <red flags> |

**4. What could not be tested**
- <e.g., accuracy under canopy; horizontal accuracy; dates of individual tiles; sounding datum>

**5. Assessed uncertainty for the intended use**
- Vertical: bias <value ± value>; random (1σ) <value> on open ground; <value or 'unknown, assume ≥ X'> in <stratum>
- Horizontal: <value or bound>
- Inflation applied for unknowns: <factor and rationale>
- Spatial structure: <correlation length / strip or tile pattern>

**6. Verdict for use <X>**
- Fit / fit with conditions / not fit — <conditions, e.g., apply +0.31 m datum shift; exclude tiles N; do not use for freeboard decisions>
- What would be needed to upgrade the verdict: <e.g., 30 independent checkpoints in forest; producer's calibration report>

**7. Attachments**
- Figures (sweeps, residual maps, spectra), scripts, test data, versions
```

Two rules govern the uncertainty section. First, **inflate when you cannot test**: if the open-ground noise is 0.10 m and nothing is known about forest, do not write 0.10 m for the project; write the open-ground value for open ground and a defended bound for the rest (for example, published results for the same sensor class under similar canopy, times a safety factor of 1.5–2, with the source cited). Second, **separate bias from noise and say which you corrected**: a 0.31 m datum offset found against ICESat-2 can be applied, and the memo must say that the delivered file does *not* include it. A memo ending "fit for hydraulic modelling of the reach with the 0.31 m shift applied and the two tilted tiles excluded; not fit for levee freeboard certification without an independent checkpoint survey" has done its job ([Chapter 3](ch03-fitness-for-use.md)).

<!-- figure: Figure 54.3 — One-page layout of a completed fitness-for-use memo for a county lidar DTM, with the test table filled in, an inset residual map against ICESat-2, and the verdict box highlighted. -->

## Then & now

For most of the twentieth century a map's authority was its publisher. The 1947 US National Map Accuracy Standards ⟨H⟩ made the stamp explicit, but compliance was asserted by the producer and almost never re-tested by users who had no better instrument than the surveyor's. The NSSDA (1998) changed the verb to "tested to meet" with independent checkpoints and a reported statistic; survey-grade GNSS made the test affordable; ASPRS 2014 and Edition 2 (2023) specified who may test, how many points, and in which strata; and USGS 3DEP made independent QA a routine stage before publication.

The 2010s made forensic evaluation possible without a field crew: spaceborne laser altimetry (ICESat 2003–2009, ICESat-2 2018–, GEDI 2019–) put a decimetre-class reference almost anywhere on land, and open national lidar supplied reference surfaces against which global products could be dissected. Third-party intercomparisons followed—SRTM against NED (Guth 2006), global DEMs against lidar across continents (Uuemaa et al. 2020), floodplain assessments (Hawker et al. 2018), and from 2020 DEMIX, a tile-based protocol built so that evaluations by different groups are comparable (Guth et al. 2021; Bielski et al. 2024). In bathymetry the shift is from trusting the chart to reading CATZOC and the per-node uncertainty delivered in BAG and S-102. The asymmetry remains: the producer knows more than the file reveals, and the user must reconstruct enough of the story to decide.

## Mathematics

**Flat-surface statistics.** For $n$ cells inside a flat polygon, fit $z = ax + by + c$ by least squares; tilt is $\sqrt{a^2+b^2}$ (× 1,000 for m/km) and noise is the σ or, robustly, the NMAD of the residuals $r_i$:

$$\mathrm{NMAD} = 1.4826 \cdot \operatorname{median}_i \left| r_i - \operatorname{median}_j r_j \right| .$$

Adjacent cells are correlated, so $\sigma_r/\sqrt{n}$ is *not* the uncertainty of the mean; use $n_{\text{eff}} \approx n (\Delta x / L)^2$ with $L$ the correlation length from a residual variogram ([Chapter 53](ch53-accuracy-assessment.md) §53.5).

**Spectral slope and effective resolution.** Detrend and Hann-window an $N \times N$ block, take the 2-D FFT, and average power in annuli of wavenumber $k$. Natural topography gives $\log P \approx \log A - \beta \log k$ with $\beta \approx 2$–3 (Perron et al. 2008). Fit over the trusted long-wavelength range; the **effective resolution** is $\lambda_{\text{eff}} = 1/k^*$ where the observed spectrum falls below the fit by a stated factor (3 dB is a reasonable convention) or flattens into a white-noise floor $P_0$, whose integral gives an independent noise variance to compare with the flat-surface NMAD.

**Registration shift.** With $\Delta h = h_{\text{test}} - h_{\text{ref}}$ on stable terrain of slope $\theta$ and aspect $\psi$ (Nuth & Kääb 2011):

$$\frac{\Delta h}{\tan\theta} = a \cos(b - \psi) + c ,$$

where $a$ is the shift magnitude, $b$ its direction, and $c\,\overline{\tan\theta}$ the vertical offset; solve on aspect bins, apply, iterate until $a < 0.1$ cell. A shift of half a cell on both axes with small standard error is the signature of a pixel-convention mismatch.

**What a small check can tell you.** For $n$ independent, roughly Gaussian residuals with sample RMSE $s$,

$$ s\sqrt{\frac{n}{\chi^2_{1-\alpha/2,\,n}}} \le \sigma \le s\sqrt{\frac{n}{\chi^2_{\alpha/2,\,n}}} ,$$

so $n = 8$, $s = 0.10$ m gives a 95 % interval of about 0.07–0.20 m; $n = 30$ gives 0.08–0.13 m. For a pass/fail question with zero failures in $n$ trials, the 95 % upper bound on the failure rate is about $3/n$: 20 clean checkpoints show the gross-error rate is probably below 15 %, nothing more. Report both numbers next to every small test.

## Validation & uncertainty

An evaluation is itself a measurement with an error budget. "Bias +0.31 m against ICESat-2" depends on the geoid used, the filtering, the interpolation to the footprint, and the terrain under the segments; "noise 4 cm from a reservoir" measures the best case of the product on a specular surface in one block. Budget the tests as you would a survey.

> **Uncertainty budget.** *Forensic bias estimate from ICESat-2 ATL06/ATL08 over a 1″ land DEM, open mid-latitude terrain; approximate 1σ.*
>
> | Component | Typical 1σ | Notes |
> |---|---|---|
> | ICESat-2 segment height, open flat ground | 0.1–0.3 m | ATL08 terrain in sparse vegetation (Neuenschwander et al. 2020) |
> | Geoid model (h → H) | 0.02–0.1 m regionally; ≥ 0.3 m in poorly surveyed regions | State the model; check one benchmark |
> | DEM interpolation to footprint | ≈ posting × tan θ / 2 (30 m, 5° ⇒ ≈ 1.3 m) | Restrict to slopes < 3–5°, interpolate bilinearly |
> | Unknown horizontal shift $d$ | $d \tan\theta$ | Co-register first |
> | Temporal change (crops, snow, subsidence) | 0 on bedrock; decimetres elsewhere | Filter by land cover and season |
> | Sampling (median of $n_{\text{eff}}$) | $1.25\,\sigma/\sqrt{n_{\text{eff}}}$ | Count tracks, not segments |
>
> For 400 segments on 6 tracks over open ground with slopes < 3°, write "+0.31 ± 0.08 m (1σ)", not "+0.31 m".

**How evaluation errors arise**, in decreasing frequency: comparing in different vertical references (the reviewer's own datum error); testing where the product is best and extrapolating; mis-attributing an artefact (a geoid difference read as strip tilt, crop growth read as bias); treating a reference whose error rivals the product's as truth ([Chapter 52](ch52-ground-truth.md) §52.5); quoting intervals from correlated samples; and over-reading texture—Table 54.1 generates hypotheses, not verdicts.

**How to test the evaluation.** Close the loop with two independent references: if ICESat-2 says +0.31 m and three NGS benchmarks agree within a few centimetres, the datum finding is robust; if they say −0.02 m, you have a question, not a conclusion. Repeat each internal test in two places of different character and report the spread. And run your scripts on a dataset you know—a reference lidar DTM should return cm-level noise, zero tilt, and no shift; if not, the problem is your pipeline.

**Propagation to the use.** For a threshold decision the user needs bias with its uncertainty, random error at the relevant scale, and correlation length ([Chapter 53](ch53-accuracy-assessment.md) §53.8). For derivatives, spatial structure matters more than magnitude: a 0.2 m/km strip tilt is harmless to floodplain extent and fatal to drainage direction on a 1 m/km plain ([Chapter 61](ch61-hydrology.md)).

> **Worked example.** *Combining tests into an assessed uncertainty.* A county 1 m DTM arrives with "RMSEz 9.25 cm (NVA)", no checkpoint table, no VVA. Tests: (a) three flats: NMAD 0.04, 0.05, 0.11 m, the third tilted 0.2 m/km (strip bias); (b) ICESat-2 ATL08, 212 open-ground segments on 5 tracks: median −0.02 m, NMAD 0.18 m; (c) 7 NGS flush benchmarks: mean −0.01 m, σ 0.06 m; (d) co-registration against six-year-older state lidar on bedrock: shift 0.3 m E, 0.1 m N, dz 0.00 m; (e) the same differencing in forest: median −0.12 m, NMAD 0.35 m—better penetration or over-aggressive filtering, undetermined. Assessed: open ground bias 0.00 ± 0.04 m, random 1σ 0.05 m, rising to 0.10 m plus a mapped 0.2 m/km tilt in the affected strips; forest bias −0.12 ± 0.10 m relative to the older lidar (true sign unknown), random 1σ ≥ 0.30 m, inflated ×1.5 to 0.45 m because neither reference is truth under canopy. The quoted 9.25 cm is consistent with open ground and silent on the rest. Verdict: fit for a 1-D hydraulic model of the main channel with the tilted strips excluded from floodplain geometry; not fit for forest-slope stability mapping without a canopy checkpoint survey.


## Software

**Open source.** **GDAL** (`gdalinfo`, `gdaldem`, `gdalwarp`) for triage, sweeps, and common grids—caveat: low-sun single-azimuth shades find more linear artefacts than `-multidirectional`. **QGIS** for interactive sweeps, histograms, profiles, and OSM/imagery overlays. **xdem** and **demcoreg** for Nuth–Kääb/ICP co-registration, residual variograms, and error models—caveat: you supply the stable-terrain mask. **CloudCompare** for cloud distances and plane fits. **PDAL** (`pdal info --metadata --stats`) and **lasinfo/lasvalidate** for LAS header forensics—caveat: a valid header is not a correct one. **SlideRule**/**icepyx** for ICESat-2; **earthaccess** for GEDI. **NOAA HydrOffice QC Tools** for BAG/grid QA; **MB-System** for crosslines when raw MBES exists. **GMT** (`grdfft`, `grdgradient`, `grdtrend`) for spectra and plane removal. **Python** (rasterio, numpy, scipy) and **R** (terra, gstat) for the scripts.

**Free but closed.** NGS datasheets and OPUS Shared; Copernicus and OpenTopography portals (open services, varied licences); Google Earth historical imagery for dating features.

**Commercial.** **Global Mapper** and **ArcGIS Pro** (sweeps, profiles, variograms—caveat: silent on-the-fly datum transformations can hide the problem under test); **TerraMatch** (strip reports when swaths exist); **CARIS HIPS/BASE Editor**, **QPS Qimera** (bathymetric QA, CUBE, uncertainty layers); **LP360** (lidar QA against ASPRS/LBS criteria).

## Standards & guides

- **ASPRS Positional Accuracy Standards, Ed. 2 (2023)** — independent testing, checkpoint independence and counts, NVA/VVA; the yardstick for a complete accuracy statement.
- **USGS Lidar Base Specification 2024** — deliverables, quality levels, acceptance criteria, QA/QC role separation for 3DEP.
- **NOAA HSSD and FPM (current editions)** — crossline requirements, TPU compliance, Descriptive Report content, QC/QA roles.
- **IHO S-44 Ed. 6.1.0 (2022)** — survey orders named in hydrographic contracts; **IHO S-67 Ed. 1.0.0 (2020)** and **S-57/S-101 CATZOC/ZOC** — how to read the quality of charted depths before using them as a check.
- **ISO 19157-1:2023** — quality elements, evaluation methods, and reporting vocabulary for the memo's test table; **ISO/IEC 17025:2017** — the traceability and impartiality mindset for independent QA.
- **OGC GeoTIFF 1.1 (2019)**, **ASPRS LAS 1.4 R15**, **BAG 2.x / IHO S-102** — the pixel-convention, header, and uncertainty-layer semantics that triage depends on.

## Pitfalls

- **Accepting a DEM because it "looks fine" at full extent** → screen resolution hides everything under 50 m → inspect at native resolution with low-sun multi-azimuth shades and a high-pass residual.
- **Judging a DTM by a DSM's standards, or the reverse** → the surface type is not what the filename says → determine it from buildings, trees, and bridges first; test against a reference of the same type.
- **Testing only where it is easy** → roads and lakes are every product's best case → label open-ground results as such; test the hard strata or inflate and say so.
- **Assuming newer = better** → a 2023 ML-corrected global product can be worse than 2010 lidar locally → test the candidate, not its date.
- **Dismissing a good dataset for a sloppy metadata template** → copied county names and wrong sensor fields are common in sound data → let flags direct tests; let tests decide.
- **Using your own wrong datum as the reference** → converting ICESat-2 with EGM2008 against a DEM on a national geoid produces a phantom bias → state the geoid and realization for every reference; check a benchmark.
- **Reading a seasonal or epoch difference as a bias** → crops, snow, reservoir level, subsidence → compare on stable bare or built surfaces; record dates ([Chapter 36](ch36-seasonal-variability.md)).
- **Interpreting difference maps before co-registration** → a half-cell shift masquerades as aspect-dependent bias of $d\tan\theta$ → run Nuth–Kääb first and report the shift as a finding.
- **Treating "accuracy 10 cm" as a tested result** → usually a specification or datasheet → ask for the checkpoint table, reference source, and independence statement.
- **Letting the contract's missing clause become your acceptance** → no crosslines or VVA were required, so none came → record a deviation with inflated uncertainty, not conformance; fix the next contract.
- **Writing a memo that only lists problems** → the user needs a verdict for a use → end with fit / fit-with-conditions / not-fit, the corrections to apply, and what would upgrade the verdict.

## Key takeaways

- Treat every delivered dataset as a hypothesis; find the cheapest test that could falsify it.
- Thirty minutes with the header—CRS, vertical reference, units, type, nodata, pixel convention, dates, software—catches most fatal problems.
- A low-sun multi-azimuth sweep plus a high-pass residual at native resolution is the most productive hour of evaluation; learn the signatures.
- Flat surfaces give noise, tilt, and tile consistency without external data; the spectrum gives effective resolution, which is rarely the posting.
- One independent external source exposes datum, bias, and scale problems that internal tests cannot; two make a finding robust.
- Decompose every accuracy claim into statistic, reference, sample size, strata, and independence; what is missing is what matters.
- Under a contract, map every criterion to a test you ran yourself and decide in writing: non-conformance, deviation, or observation.
- Your evaluation has an error budget; report findings with uncertainties and the places you could not look.
- Write the memo: what it is, what it is not, what you tested, what you could not, assessed uncertainty with inflation for unknowns, and the verdict for the named use.

## References

- ASPRS. 2023. *ASPRS Positional Accuracy Standards for Digital Geospatial Data*, Edition 2, Version 2.0. Baton Rouge, LA: ASPRS.
- Bielski, C., López-Vázquez, C., Grohmann, C. H., Guth, P. L., Hawker, L., Gesch, D., Trevisani, S., Herrera-Cruz, V., Riazanoff, S., Corseaux, A., Reuter, H. I., Strobl, P., and the TMSG DEMIX Working Group. 2024. Novel approach for ranking DEMs: Copernicus DEM improves one arc second open global topography. *IEEE Transactions on Geoscience and Remote Sensing* 62:4503922.
- FGDC. 1998. *Geospatial Positioning Accuracy Standards, Part 3: National Standard for Spatial Data Accuracy* (FGDC-STD-007.3-1998). Reston, VA: FGDC.
- Guth, P. L. 2006. Geomorphometry from SRTM: Comparison to NED. *Photogrammetric Engineering & Remote Sensing* 72(3):269–277.
- Guth, P. L., Van Niekerk, A., Grohmann, C. H., et al. 2021. Digital Elevation Models: Terminology and definitions. *Remote Sensing* 13(18):3581.
- Hare, R., Eakins, B., and Amante, C. 2011. Modelling bathymetric uncertainty. *International Hydrographic Review* (6):31–42.
- Hawker, L., Bates, P., Neal, J., and Rougier, J. 2018. Perspectives on digital elevation model (DEM) simulation for flood modeling in the absence of a high-accuracy open access global DEM. *Frontiers in Earth Science* 6:233.
- Hirt, C. 2018. Artefact detection in global digital elevation models (DEMs): The Maximum Slope Approach and its application for complete screening of the SRTM v4.1 and MERIT DEMs. *Remote Sensing of Environment* 207:27–41.
- Höhle, J., and Höhle, M. 2009. Accuracy assessment of digital elevation models by means of robust statistical methods. *ISPRS Journal of Photogrammetry and Remote Sensing* 64(4):398–406.
- Hugonnet, R., Brun, F., Berthier, E., Dehecq, A., Mannerfelt, E. S., Eckert, N., and Farinotti, D. 2022. Uncertainty analysis of digital elevation models by spatial inference from stable terrain. *IEEE JSTARS* 15:6456–6472.
- IHO. 2022. *S-44 Standards for Hydrographic Surveys*, Edition 6.1.0. Monaco: IHO.
- IHO. 2020. *S-67 Mariners' Guide to Accuracy of Depth Information in Electronic Navigational Charts (ENC)*, Edition 1.0.0. Monaco: IHO.
- ISO. 2023. *ISO 19157-1:2023 Geographic information — Data quality — Part 1: General requirements*. Geneva: ISO.
- Mesa-Mingorance, J. L., and Ariza-López, F. J. 2020. Accuracy assessment of digital elevation models (DEMs): A critical review of practices of the past three decades. *Remote Sensing* 12(16):2630.
- Neuenschwander, A., Guenther, E., White, J. C., Duncanson, L., and Montesano, P. 2020. Validation of ICESat-2 terrain and canopy heights in boreal forests. *Remote Sensing of Environment* 251:112110.
- Nuth, C., and Kääb, A. 2011. Co-registration and bias corrections of satellite elevation data sets for quantifying glacier thickness change. *The Cryosphere* 5(1):271–290.
- Oksanen, J., and Sarjakoski, T. 2005. Error propagation of DEM-based surface derivatives. *Computers & Geosciences* 31(8):1015–1027.
- Perron, J. T., Kirchner, J. W., and Dietrich, W. E. 2008. Spectral signatures of characteristic spatial scales and nonfractal structure in landscapes. *Journal of Geophysical Research: Earth Surface* 113:F04003.
- Polidori, L., and El Hage, M. 2020. Digital elevation model quality assessment methods: A critical review. *Remote Sensing* 12(21):3522.
- Seton, M., Williams, S., Zahirovic, S., and Micklethwaite, S. 2013. Obituary: Sandy Island (1876–2012). *Eos, Transactions AGU* 94(15):141–142.
- Shean, D. E., Alexandrov, O., Moratto, Z. M., Smith, B. E., Joughin, I. R., Porter, C., and Morin, P. 2016. An automated, open-source pipeline for mass production of digital elevation models (DEMs) from very-high-resolution commercial stereo satellite imagery. *ISPRS Journal of Photogrammetry and Remote Sensing* 116:101–117.
- USGS. 2024. *Lidar Base Specification 2024, Rev. A*. National Geospatial Program, Reston, VA (online, revised periodically).
- Uuemaa, E., Ahi, S., Montibeller, B., Muru, M., and Kmoch, A. 2020. Vertical accuracy of freely available global digital elevation models (ASTER, AW3D30, MERIT, TanDEM-X, SRTM, and NASADEM). *Remote Sensing* 12(21):3482.
- Wise, S. 2000. Assessing the quality for hydrological applications of digital elevation models derived from contours. *Hydrological Processes* 14(11–12):1909–1929.

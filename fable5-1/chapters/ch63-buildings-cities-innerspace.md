# Chapter 63 — Buildings, cities, and innerspace

> **Part XIV — Domain deep dives.** The built environment, where "the surface" is a stack of surfaces, where the definition of a building decides its height, and where the most valuable spaces—under roads, inside buildings, below the street—are invisible to every sensor that looks down.

**In this chapter.** Cities break the assumptions that make a DEM simple: one elevation per location, a clear line between ground and object, and a surface that stays put between surveys. You will be able to state what a building is for a given product—footprint rule, minimum size, attached structures, and above all which height reference (eave, ridge, mean roof, a percentile) the model reports—and why two correct models of the same city differ by meters; read CityGML and CityJSON levels of detail as specifications with known volume errors; explain how national programs such as the Dutch 3D BAG generate LoD1 and LoD2 models from lidar and footprints at scale; decide what "ground under a building" means for a city DTM; represent roads that pass under buildings and over other roads without forcing them into one surface; relate indoor models (IndoorGML, IFC/BIM) and underground utilities (ASCE 38-22 quality levels) to outdoor DEMs through registration you can test; and validate a city model per building, per LoD, and per epoch with tools such as val3dity.

## 63.1 What is a building?

Every building dataset embodies a definition, and the definitions differ in ways that change heights, counts, and areas. Three footprint conventions exist. The **roof outline** is what an aerial image or a DSM shows: the projection of the roof's outer edge, including eaves that overhang the walls by 0.3–1 m. The **wall base** (or ground-contact outline) is what a ground survey or a cadastral map records and is smaller than the roof outline by the eave overhang on every side; for a 10 m × 10 m house with 0.5 m eaves the roof-outline area is 121 m² and the wall-base area 100 m², a 21 % difference in "building area" from the definition alone. The **cadastral footprint** may follow legal rather than physical boundaries—a terrace of row houses split along party walls, or a footprint that includes an attached garage the imagery shows as a separate roof. National specifications choose one and state tolerances: the Dutch BAG registers wall-base outlines from the cadastre; OpenStreetMap buildings are usually roof outlines traced from imagery; the USGS Lidar Base Specification's building class (class 6) is a point-cloud class, not a footprint, and footprints derived from it are roof outlines.

**Minimum size** rules (typically 10–25 m² in national mapping; OSM has none) decide whether sheds, kiosks, and bus shelters are buildings. **Attached and ambiguous structures**—carports, canopies, greenhouses, covered walkways, ruins, buildings under construction, mobile homes, storage tanks—are included or excluded differently by every specification, and the differences show up directly as commission and omission errors when two datasets are compared ([Chapter 42](ch42-object-detection-semantics.md)). A rule such as "roofed, walled on at least three sides, permanent, ≥ 15 m² footprint" is typical, and the dataset's documentation should say so.

**Height references** are where the definitions bite hardest. Biljecki, Ledoux, and Stoter (2016) catalogued the choices in common use for the single height of an LoD1 block model and showed how far they diverge: height to the **eave** (lowest roof edge), to the **ridge** (highest point), to the **mean roof** height, to the **median** or a **percentile** (e.g., the 50th or 70th percentile of roof lidar points), or to the roof's centroid; and the base can be the lowest ground point around the footprint, the highest, the mean, or the elevation at the main entrance. For a gabled house with a 4 m eave-to-ridge difference, the "building height" ranges over 4 m depending on the pair of choices, the LoD1 block's volume over roughly ± 30 %, and any application that consumes volume—energy demand, population estimates, noise barriers—inherits that spread. There is no right reference; there are documented and undocumented ones. The CityGML 3.0 `Height` property carries both a `highReference` and a `lowReference` attribute precisely so that the choice is explicit, and the 3D BAG delivers several heights per building (ground level as a percentile, roof heights at the 50th, 70th, max, and min percentiles) so the user can pick.

**Roof shapes** (flat, gabled, hipped, mansard, shed, complex) matter for LoD2 modeling and for the applications that use roof planes (solar, drainage), and their classification from lidar depends on point density: at 2 points/m² a 6 m × 8 m gable roof has about 100 points, enough to fit two planes; a dormer has ten, not enough.

> **Definitions that bite.** *Building height* in a national statistics table, an LoD1 city model, a tax assessment, a planning code, and an aviation obstacle database are five different numbers for the same structure: respectively perhaps the number of storeys × 3 m, the 70th-percentile roof height above the 5th-percentile ground, the eave height above the main entrance, the parapet height above the average grade, and the top of the rooftop antenna above mean sea level. Compare heights across datasets only after translating both to one reference, and expect residual differences of 1–3 m from the translation itself.

<!-- figure: Figure 63.1 — One gabled building with an attached garage and rooftop equipment, annotated with roof-outline vs wall-base footprints, eave/ridge/mean/percentile heights, three candidate ground references, and the LoD0–LoD3 representations of the same building. -->

## 63.2 City models: LoDs, national programs, and meshes

**CityGML**, the OGC standard for semantic 3D city models (Gröger and Plümer 2012; version 3.0 adopted in 2021), defines **levels of detail**: **LoD0** is a footprint or roof-edge polygon, possibly with a height attribute (2.5D); **LoD1** a prismatic block extruded from the footprint to a single height; **LoD2** a block with a generalized roof shape and optional roof overhangs and semantic surfaces (RoofSurface, WallSurface, GroundSurface); **LoD3** a detailed exterior with openings (windows, doors) and architectural features; CityGML 2.0's LoD4 interior was folded into a separate interior concept in 3.0. Biljecki, Ledoux, and Stoter (2016) refined these into sixteen sub-levels (LoD0.0–LoD3.3) by separating the footprint, height, roof, and overhang choices that the coarse levels left implicit, so that two "LoD2" datasets can be compared on what they actually contain. **CityJSON** (version 2.0, 2023) encodes the CityGML 3.0 conceptual model in compact JSON and is now the practical interchange format for most open city models; `cjio` validates, converts, and subsets it.

National and municipal programs now produce LoD1/LoD2 models at scale. The Netherlands' **3D BAG** (Peters et al. 2022) reconstructs LoD1.2, LoD1.3, and LoD2.2 models for all ~10 million buildings in the country from the AHN national lidar and the BAG cadastral footprints, fully automatically, with per-building quality attributes (point density, reconstruction error, height percentiles) and periodic re-runs as new AHN data arrive; the pipeline (`geoflow`, successor to `3dfier`; Ledoux et al. 2021) is open source. Germany's state surveying agencies (AdV) deliver nationwide LoD1 and LoD2 CityGML; Switzerland's **swissBUILDINGS3D 2.0/3.0** provides LoD2 with roof overhangs; many cities (Berlin, Helsinki, New York, Singapore) publish their own. These semantic models coexist with **photogrammetric meshes**—the textured triangle meshes behind Google Earth's and Apple Maps' 3D views and the many municipal "digital twins" made with ContextCapture/iTwin or Metashape—which look better, carry no semantics, and have no notion of a building as an object; a mesh can be measured but not queried, and converting a mesh to LoD2 semantics is itself a reconstruction problem (Haala and Kada 2010 remain the reference review of building reconstruction approaches). **OpenStreetMap** carries `building:levels`, `height`, and `roof:shape` tags with no accuracy specification; `building:levels × ~3 m` is a usable LoD1 height prior with ± 1 storey uncertainty where nothing better exists.

Generating LoD1/LoD2 from lidar and footprints is now routine: for each footprint, select roof points, compute height percentiles (LoD1), segment roof planes by RANSAC or region growing, intersect planes with each other and with the footprint walls, and enforce a watertight solid (LoD2). The failure modes are footprints that disagree with the lidar epoch (demolished or new buildings), low point density on steep or dark roofs, vegetation overhanging roofs, and footprints that merge or split buildings differently from the roof structure.

## 63.3 DSM → DTM in cities: what is ground under a building?

[Chapter 32](ch32-dsm-to-dtm.md) treats object removal in general; cities add cases that specifications handle inconsistently and that users must check. A ground filter removes buildings and interpolates the terrain beneath from surrounding ground points, which works for a detached house on level ground and fails in characteristic ways elsewhere.

**Courtyards** inside building blocks are often unseen by airborne lidar at the ground (shadowed by walls) and are interpolated from the surrounding streets; a sunken courtyard or a raised interior podium is lost. **Terraces and retaining walls** are real ground discontinuities that filters either smooth (losing a 3 m wall) or classify as building (removing the upper terrace). **Sunken roads** and **cuttings** with vertical retaining walls are kept if the filter sees enough ground points in the cutting, and bridged if it does not. **Elevated roads and rail** on viaducts are not ground, and most specifications remove them (USGS LBS classifies bridge decks as class 17 and excludes them from the DTM), leaving a DTM in which the ground under the viaduct is interpolated—correct for hydrology, wrong for anyone who wanted the road's elevation. **Podiums**—multi-storey bases carrying towers, common in Asian cities—are buildings, but a DTM that removes a podium occupying a whole block interpolates the ground across 200 m from the surrounding streets, and the resulting "ground" under the towers may be meters from the slab.

The question **what is ground under a building** has at least three answers: the **natural ground** that existed before construction (unknowable from lidar; sometimes in old survey records), the **slab or ground-floor level** (what a flood model wants, since that is where water enters; measured at thresholds), and the **basement floor** (what a geotechnical or utility model wants). Specifications almost universally mean "an interpolated surface consistent with the surrounding ground," which is none of the three and is usually within a meter of the slab on level sites. A DTM user in a city should read the specification's sentence on buildings and then test it: difference the DTM against surveyed threshold heights for a sample of buildings and report the residual by building type and terrain slope.

> **Rule of thumb.** In a city DTM derived from airborne lidar, expect the interpolated ground under buildings to be within ± 0.3 m of the true ground-floor threshold for detached buildings on slopes below 5 %, within ± 1 m for row houses and small blocks, and unreliable (several meters) under podiums, large-footprint buildings on slopes, and anything over a cutting or embankment. The rule fails on terraced hillsides (retaining walls make the "surrounding ground" ambiguous) and in cities built on fill or over covered rivers.

## 63.4 Roads under buildings, buildings over roads: multi-valued surfaces

A 2.5D surface stores one elevation per $(x, y)$; a city has many. A road passing beneath a building (an air-rights development over a highway, a railway under a station concourse, a covered market street, a parking structure with five decks) has at least two surfaces at the same location, and a DSM/DTM pair represents neither correctly: the DSM shows the building roof, the DTM shows an interpolated ground, and the road—the navigable surface a vehicle or a flood model needs—vanishes from both. Multi-level intersections (stacked interchanges with four levels), tunnels, and underpasses are the same problem at the network scale. [Chapter 35](ch35-voids-and-overhangs.md) treats multi-valued surfaces generically; the urban solutions are three.

**Network Z-levels.** Road and rail networks carry elevation as attributes of links and nodes rather than as a surface: OSM's `layer=*` tag (ordinal stacking, not elevation), `bridge`/`tunnel` tags, and `level=*` for indoor floors; commercial road networks carry a Z-level per link end that defines connectivity at grade separations. The network knows which road is above which without knowing their elevations in meters, which is enough for routing and not enough for drainage or line of sight.

**3D road models.** HD maps ([Chapter 62](ch62-navigation-and-charting.md)) and some national topographic databases (e.g., the Dutch TOP10NL/3D Basisvoorziening, swissTLM3D) carry road centerlines and edges as 3D polylines with measured elevations, which represent stacked roads exactly where a surface cannot. From these a **navigable-surface** raster can be generated per level where needed.

**Layered surfaces.** Keep separate rasters for distinct surfaces—DTM, DSM, a "road surface" layer in which bridges and viaducts are kept at deck elevation and buildings over roads are removed, a "below-ground" layer for tunnels—each with its own definition, and do not attempt to merge them. The USGS LBS building, bridge-deck, and ground classes make such layers derivable from one point cloud; the deliverable is then not a DEM but a set of surfaces with a legend.

The failure to do any of these shows up as a flood model in which an underpass cannot flood ([Chapter 61](ch61-hydrology.md)), a line-of-sight analysis in which a tunnel portal has a view, a drone geofence that treats a covered road as a building, and a vehicle energy model whose grade profile jumps 8 m at every overpass because the DSM sampled the deck and then the road beneath.

<!-- figure: Figure 63.2 — Cross-section through a city block with an air-rights building over a highway, a railway in a cutting, a parking structure, and a basement; shows what a DSM, a DTM, a "navigable road surface" layer, a network Z-level graph, and an IndoorGML cell graph each represent of the same geometry. -->

## 63.5 Innerspace: indoor, underground, and the registration problem

Indoors, there is no DEM in the usual sense—floors are the "terrain," stacked, connected by stairs, ramps, and elevators—and the data models are different. **IndoorGML** (OGC; Kang and Li 2017; version 2.0 Part 1, the conceptual model, published in August 2025, with implementation schemas to follow in Part 2) models indoor space as **cells** (rooms, corridors) with geometry, a **node–relation graph** (dual graph) encoding adjacency and connectivity for navigation, and multiple **layered spaces** (topographic, sensor-coverage, security) over the same geometry. **IFC** (ISO 16739, the Industry Foundation Classes behind BIM) models a building as its components—walls, slabs, doors, ducts—with construction semantics and a local engineering coordinate system; converting IFC to CityGML/IndoorGML is a well-studied and lossy operation because the two models answer different questions (what is this made of vs. where can one go). **Floor and level semantics** (ground floor numbered 0 or 1; mezzanines; split levels; basements) are a persistent source of error in multi-source integration, and a level's floor elevation is rarely stored in a datum outside the building.

Indoor geometry is acquired by **SLAM** with handheld, backpack, and trolley mobile mappers ([Chapter 15](ch15-slam.md)), by terrestrial laser scanning, and from CAD/BIM. Zlatanova et al. (2013) laid out the indoor mapping problems that remain: GNSS denial, clutter and furniture, dynamic occupants, glass and mirrors, and the absence of an absolute reference. **Indoor–outdoor registration** is the elevation-relevant one: a SLAM map is internally consistent to centimeters but floats in position, orientation, scale (for visual SLAM), and datum until tied to something known. The practical ties are **door thresholds** and entrances surveyed from outside with GNSS/total station and matched to the indoor map; **façade features** visible to both the indoor scan (through windows or at entrances) and an outdoor mobile or airborne scan; and **control points** carried inside by traverse. Without a tie, the indoor model's floor elevations cannot be compared with the outdoor DTM, the flood model cannot know whether the basement is below the street, and the emergency-response map cannot say which outdoor door leads to which floor. A tie to one entrance fixes the vertical offset but not the orientation; three well-separated ties are the minimum for a rigid registration with a residual check.

**Underground utilities** are mapped under **ASCE 38-22** (*Standard Guideline for Investigating and Documenting Existing Utilities*), which defines four **quality levels**: **QL-D** (records research only; position unverified), **QL-C** (surface features surveyed and correlated with records), **QL-B** (geophysical designation—EM locators, GPR—giving horizontal position; depth, if given, is approximate), and **QL-A** (test holes or vacuum excavation exposing the utility, with surveyed horizontal and vertical position, typically to ± 15 mm). Depth below ground is the attribute that matters for excavation, and only QL-A provides it reliably; a utility record showing "1.2 m cover" from a 1970s as-built, over a street regraded twice since, is QL-D and should be treated as a rumor. The DTM enters because utility depth is stored relative to a ground surface that changes; QL-A records should carry invert elevations in a stated datum, not depths. **Mines and caves** ([Chapter 65](ch65-mining-landfills-earthworks.md), [Chapter 66](ch66-coastal-marine-polar-lakes-rivers.md)) and geological **subsurface voxel models** (city-scale 3D geology from boreholes, as in the Netherlands' GeoTOP) extend innerspace downward with their own, usually much larger, uncertainties.

## 63.6 Urban dynamics: what changed, and does it count?

Cities change faster than national lidar cycles. **Construction and demolition detection** by DSM differencing ([Chapter 41](ch41-change-detection.md)) finds new buildings reliably where the height change exceeds the minimum detectable change (typically 0.5–1 m for lidar pairs; several meters for satellite stereo) and the footprint exceeds a few cells; it also finds every **crane**, **scaffold**, and **construction hoarding** ([Chapter 27](ch27-moving-and-transient-objects.md)), which the specification must say whether to keep. Temporary structures—**markets**, **festival tents**, **stadium stands**, **seasonal terraces**—are in the DSM on the day of flight and not the next week.

**Rooftop equipment** is a definitional issue with large consequences for change detection and for height statistics. **Solar panels** add 0.1–0.5 m to a flat roof and change its lidar reflectance; a national programme that installs panels on 10 % of roofs in five years produces a systematic "height change" that is real but not what a building-height time series wants to count. HVAC units, water tanks, elevator overruns, **green roofs** (whose vegetation grows and is seasonal), parapets, and **antennas** ([Chapter 33](ch33-wires-and-thin-structures.md)) all raise the same question: is the building height the structural roof, the roof including fixed equipment, or the highest point including masts? The answer differs by application—aviation wants the highest point, energy modeling the structural envelope, solar potential the unobstructed roof plane—and a city model that stores several roof heights (3D BAG's approach) or classifies rooftop equipment separately (USGS LBS has no such class; some municipal specifications do) serves more applications than one that picks one.

## 63.7 Applications and the surface each needs

Urban applications of elevation data (Biljecki et al. 2015 reviewed about thirty) each require a specific surface, and much wasted effort comes from using the wrong one.

| Application | Surface needed | Objects included | Typical accuracy need | Common wrong choice |
|---|---|---|---|---|
| Rooftop solar potential | DSM of roof planes + obstructions (trees, equipment) | Trees yes, panels existing yes | 0.2 m roof height; roof slope/aspect | LoD1 blocks (no slope) |
| Wind / CFD, pedestrian comfort | DSM or LoD1/2 + roughness | Buildings yes, trees as porous | 1 m building height | DTM |
| Noise mapping (e.g., CNOSSOS-EU) | DTM + buildings as barriers + height | Buildings yes, trees no (or absorptive) | 0.5–1 m barrier height | DSM with trees as walls |
| 5G / RF planning | DSM + clutter classes | Everything | 1–2 m | DTM + building heights only |
| Shadow and sunlight rights | DSM or LoD2 with roof shape | Buildings, trees seasonal | 0.5 m | LoD1 (flat roofs cast wrong shadows) |
| Pluvial flood ([Chapter 61](ch61-hydrology.md)) | DTM + building blocks + curbs | Buildings as blocks | 0.1 m ground | DSM |
| Viewshed, skyline protection | DSM or LoD2 | Buildings, trees (seasonal) | 1 m | DTM |
| Population / floor-space estimation | LoD1 volume ÷ storey height | Buildings only | Height reference consistency | Mixed height references |
| Urban heat / sky-view factor | DSM | Everything | 1 m | DTM |

Two patterns recur. First, trees are an object class whose inclusion flips by application (obstruction for solar and viewshed, porous for wind, absent for noise barriers, seasonal for shadow), so a city product should keep vegetation separable rather than baked into one DSM. Second, the height reference problem of §63.1 propagates: a population estimate from LoD1 volumes made with ridge heights overestimates floor space in gabled neighbourhoods by 20–40 % relative to one made with eave heights, and the discrepancy is invisible unless the reference is documented.

## 63.8 Privacy, security, and licensing of city models

A detailed city model is a map of private property at a resolution that raises concerns a 10 m DEM does not. **Façade detail** at LoD3 and in street-level meshes shows windows, balconies, and the interiors visible through them; **interiors** in IndoorGML/BIM reveal layouts of homes and secure facilities; **sensitive sites** (prisons, military, critical infrastructure) are blurred, flattened, or removed in many published models, with the removal itself a detectable signal. [Chapter 69](ch69-security-sovereignty-privacy-ethics.md) treats the policy questions. The practical points for a producer are that national 3D models are increasingly open (3D BAG under CC BY; German LoD2 under open licenses in most states since 2023; swissBUILDINGS3D free), that their terms frequently differ from the licensing of the lidar and footprints they were made from, and that building-level attributes (height, volume, roof type) joined to address registers become personal data under GDPR-style regimes when they describe a single dwelling.

## 63.9 Validating a city model

A city model is validated at three levels: geometry, semantics/topology, and currency.

**Per-building height accuracy** is tested against independent measurements—surveyed roof points, total-station heights of eaves and ridges, or a higher-density lidar—using the *same height reference*; a typical national LoD2 product achieves RMSE of 0.2–0.5 m on roof heights where point density exceeds 4 points/m², degrading on small and complex roofs. Report by roof type and footprint size, not one number. **Footprint completeness and commission** are tested against a reference set (field survey or newer imagery) as per-object recall and precision with an IoU threshold (commonly 0.5), and the definitional differences of §63.1 must be reconciled first or they dominate the result.

**LoD compliance and 3D validity** are tested with **val3dity** (Ledoux 2018), which checks each solid against ISO 19107 rules: rings closed and non-self-intersecting, surfaces planar within tolerance, shells closed and orientable, no overlapping or dangling faces, solids not self-intersecting. A model that fails these cannot have its volume computed reliably and will break downstream CFD meshing and solar simulation; in practice, automatically reconstructed national models pass at rates above 99 % after post-processing while converted CAD/BIM models fail frequently. **Temporal currency** is tested by comparing the model against a newer DSM: buildings in the model but not in the DSM (demolished), in the DSM but not the model (new), and height changes above the minimum detectable change (modified); report the fraction of buildings with a verified epoch.

> **Try it.** Validate a CityJSON tile and compute per-building LoD1 volumes under two height references.
>
> ```bash
> # 1. Geometric validity (ISO 19107 rules) for every building
> val3dity tile.city.json --report report.json
> python3 -c "import json; r=json.load(open('report.json')); \
>   print('invalid features:', sum(1 for f in r['features'] if not f['validity']))"
>
> # 2. Inspect and subset with cjio
> cjio tile.city.json info
> cjio tile.city.json subset --exclude --cotype Bridge save tile_buildings.city.json
> ```
>
> ```python
> import json, numpy as np
> cm = json.load(open("tile_buildings.city.json"))
> V = np.array(cm["vertices"]) * cm["transform"]["scale"] + cm["transform"]["translate"]
> vol = {}
> for bid, b in cm["CityObjects"].items():
>     if b["type"] != "Building": continue
>     a = b.get("attributes", {})
>     # 3D BAG-style attributes: ground height (b3_h_maaiveld) and roof percentiles
>     h_ground = a.get("b3_h_maaiveld"); h50 = a.get("b3_h_dak_50p"); hmax = a.get("b3_h_dak_max")
>     area = a.get("b3_opp_grond")
>     if None in (h_ground, h50, hmax, area): continue
>     vol[bid] = (area * (h50 - h_ground), area * (hmax - h_ground))
> v50 = np.array([v[0] for v in vol.values()]); vmax = np.array([v[1] for v in vol.values()])
> print(f"buildings: {len(vol)}; median volume ratio max/p50 = {np.median(vmax / v50):.2f}")
> ```
>
> Expected outcome: `val3dity` reports zero or very few invalid solids for a 3D BAG tile; the volume ratio between max-roof-height and 50th-percentile LoD1 blocks is typically 1.1–1.4 in neighbourhoods of pitched roofs and ~1.0 for flat roofs—the height-reference sensitivity of §63.1 made visible. (Attribute names follow 3D BAG's current schema; check them against the tile's metadata.)

## Then & now

Building outlines began as an insurance and tax instrument: the **Sanborn fire-insurance maps** (from 1867) recorded footprints, storeys, construction material, and roof type at 1:600 for North American cities—an LoD1 attribute set on paper. Cadastral surveys supplied wall-base footprints; photogrammetry supplied roof outlines and, from stereo plotters, eave and ridge heights. The first **photogrammetric 3D city models** of the 1990s (manually plotted roofs in CAD for Berlin, Stuttgart, and others) were followed by **airborne lidar reconstruction** research from the late 1990s (reviewed by Haala and Kada 2010), the **CityGML** standard (OGC adoption 2008; 2.0 in 2012; 3.0 in 2021), and the national LoD1/LoD2 programmes of the 2010s. **Photogrammetric meshes** became ubiquitous when Apple (2012) and Google (2012) launched automatically generated 3D city views from oblique aerial imagery, and municipal "digital twins" followed in the 2020s with meshes, semantic models, and IoT feeds combined. Indoor mapping went from CAD floor plans to **SLAM** mobile mappers (commercial handheld systems from about 2013) and from building-specific coordinates to IndoorGML (OGC 1.0 in 2014) and IFC-based BIM-GIS integration. The height-reference problem is as old as the first building-height table and was only formalised in the LoD literature of the 2010s.

## Mathematics

**Roof-plane fitting with RANSAC.** For roof points $\{\mathbf{p}_i\}$ within a footprint, repeatedly sample three points, fit the plane $\mathbf{n}\cdot\mathbf{p} = d$, count inliers with $|\mathbf{n}\cdot\mathbf{p}_i - d| < \tau$ (τ ≈ 0.1–0.2 m for airborne lidar), keep the plane with the most inliers, refine by least squares on the inliers, remove them, and repeat until fewer than $k_{\min}$ points remain. The number of iterations for confidence $p$ with inlier fraction $w$ is $N = \ln(1-p)/\ln(1-w^3)$; for $w$ = 0.3 and $p$ = 0.99, $N \approx 168$. Plane adjacency and intersection lines give ridges and valleys; intersecting the planes with the vertical walls at the footprint gives the LoD2 solid.

**Height percentiles and block volume.** With roof points' heights $z_{(1)} \le \dots \le z_{(n)}$, the $q$-th percentile roof height is $z_{(\lceil qn \rceil)}$; with ground height $z_g$ (itself a percentile of ground points in a buffer around the footprint) and footprint area $A$, the LoD1 volume is $V_q = A\,(z_{(q)} - z_g)$. Its sensitivity to the reference is $\partial V / \partial z = A$, so a 1 m difference in reference on a 100 m² footprint is 100 m³, and for a gabled roof of eave-to-ridge difference $\Delta$ the ratio $V_{\text{ridge}}/V_{\text{eave}} = 1 + \Delta/(z_{\text{eave}} - z_g)$—for a two-storey house ($z_{\text{eave}} - z_g$ = 6 m, Δ = 4 m) a factor of 1.67. The true volume of the gabled roof is halfway, which is why a percentile near 50 is a sensible single-height choice for volume.

**3D validity.** val3dity implements ISO 19107's rules as tests: for a `Solid`, each `Shell` must be a closed 2-manifold (every edge shared by exactly two faces), orientable with outward normals, faces planar within a distance tolerance (default 0.01 m) and an angular tolerance, rings simple and non-overlapping, and the exterior shell must contain the interior shells without intersection. Volume by the divergence theorem, $V = \frac{1}{3}\sum_f \mathbf{c}_f \cdot \mathbf{n}_f A_f$, is only meaningful when these hold.

**Layered grids for multi-valued surfaces.** Represent the city as $K$ rasters $z_k(x,y)$, $k = 1..K$, with a label raster $\ell_k(x,y) \in \{\text{ground, road deck, roof, tunnel floor, nodata}\}$, ordered so that $z_1 \le z_2 \le \dots$ where defined; a query for "the navigable surface for vehicles at $(x,y)$ near elevation $z_0$" returns $\arg\min_k |z_k - z_0|$ among layers labelled road; a flood model takes the lowest layer labelled ground or road deck that is open to the sky. This is a 2.5D stack, not a full 3D model, but it preserves what a single surface destroys.

## Validation & uncertainty

Errors in city models arise from four sources that should be reported separately, because they have different fixes.

**Definitional error** is the largest and least recognized: footprint convention (roof outline vs wall base, ± 0.5 m per side), height reference (eave vs ridge vs percentile, up to several meters), inclusion rules for attached structures and rooftop equipment. It is not reduced by better sensors; it is reduced by documentation and by translating all datasets to one convention before comparison. Test for it by comparing two "correct" datasets of the same city and attributing the differences: if the height residual histogram is bimodal with a mode near the typical eave-to-ridge difference, the references differ.

**Measurement error** is the lidar or photogrammetric height error on roofs (small: 0.05–0.15 m for lidar on planar roofs) and the much larger error on the *ground* reference under and around buildings (§63.3), which dominates height-above-ground uncertainty on slopes. Test with surveyed thresholds and roof points; report RMSE and the 95th percentile by terrain slope class.

**Reconstruction error** is the simplification of LoD1/LoD2: a block or a few planes replacing a complex roof. Biljecki and colleagues' LoD specification work quantified the effect on applications; a practical measure is the volume between the reconstructed solid and the DSM over the footprint (the "reconstruction residual"), delivered per building by 3D BAG as an RMSE of lidar points from the model surfaces, typically 0.1–0.5 m. Buildings with large residuals are candidates for manual review or a different roof model.

**Temporal error** is the difference between the model's epoch and the use date; in a growing city 1–3 % of buildings change per year, so a five-year-old model is wrong for 5–15 % of buildings. Test against a newer DSM or imagery; report the verified-epoch fraction.

For **indoor and underground** data the uncertainty structure is different: SLAM maps have small relative and unknown absolute error until registered; registration residuals at three or more tie points should be reported, and a registration done at one entrance should be flagged as a vertical tie only. Utility positions carry ASCE 38 quality levels; an uncertainty number attached to a QL-D record is a fiction, and the deliverable should carry the quality level, not an invented σ.

> **Uncertainty budget.** Height above ground of a two-storey gabled house in a national LoD2 product (illustrative).
>
> | Component | Magnitude | Note |
> |---|---|---|
> | Lidar roof-point height error | 0.05–0.10 m (1σ) | Planar roof, 4+ points/m² |
> | Roof-plane fit / percentile sampling | 0.05–0.20 m | Depends on density, dormers |
> | Ground reference (interpolated under building) | 0.1–0.3 m level site; 0.5–2 m on slope | Dominant on hillsides |
> | Height-reference convention | 0 (if documented) to 4 m (if not) | Eave vs ridge |
> | Epoch mismatch (renovation, new storey) | 0 or ≥ 3 m | Per-building, binary |
>
> The two largest terms are not measurement errors at all; they are definitional and temporal, and both are removed by metadata, not by better lidar.

## Software

**Open source:** **3dfier / geoflow** (3D BAG pipeline; LoD1/LoD2 reconstruction from lidar and footprints). **City3D** (LoD2 reconstruction from point clouds, polygonal roofs). **cjio** (CityJSON validation, conversion, subsetting, upgrade). **val3dity** (ISO 19107 validity of 3D primitives; CLI and web). **citygml4j / citygml-tools** (CityGML ↔ CityJSON, 3.0 support). **PDAL** (building classification filters, `filters.hag_*` for height above ground) and **lidR** (`lasroofs`-style segmentation via community packages). **QGIS 3D** and **Blender-GIS** (visualization; Blender's BlenderGIS imports DEMs and buildings). **OSM tooling** (`osmium`, `osm2pgsql` with `building:levels`). **IndoorGML tools** (the OGC reference implementations and `InFactory`). **IfcOpenShell** (IFC parsing and conversion). **3D Tiles / py3dtiles** (streaming meshes and city models).

**Free but closed:** **Google Earth** and **Apple Maps** 3D (viewing meshes, no export). **Esri CityEngine** trial / **ArcGIS Online 3D basemaps** (viewing). **Autodesk Viewer** for IFC.

**Commercial:** **Esri ArcGIS Pro 3D / CityEngine** (procedural LoD models; 3D basemaps). **Bentley ContextCapture / iTwin** and **Agisoft Metashape** (photogrammetric meshes). **Trimble SketchUp**, **eCognition** (object extraction). **virtualcitySYSTEMS / VC Map**, **Cyclomedia** (street-level 3D). **NavVis**, **Leica BLK2GO**, **GeoSLAM/FARO** (indoor mobile mapping). **Bentley OpenCities** (city-scale CityGML management).

## Standards & guides

- **OGC CityGML 3.0 (2021)** conceptual model and **CityGML 2.0 (2012)** encoding; **OGC CityJSON 2.0 (2023)** community standard — LoDs, semantic surfaces, height references.
- **OGC IndoorGML 1.1 (2020)** and **IndoorGML 2.0 Part 1 (2025)** — indoor cells, dual graph, layered spaces.
- **ISO 16739-1:2024 (IFC 4.3)** — BIM data model; IFC–CityGML conversion guidance from buildingSMART/OGC.
- **ASCE 38-22** *Standard Guideline for Investigating and Documenting Existing Utilities* — quality levels A–D; companion **ASCE 75-22** for recording utility data.
- **ISO 19107:2019** Spatial schema — the geometric validity rules val3dity implements; **ISO 19152 (LADM)** for 3D cadastre.
- **AdV (Germany) LoD1/LoD2 product specification** and **Kadaster/3D BAG documentation (NL)**; **swisstopo swissBUILDINGS3D 3.0** specification — national height references and footprint rules.
- **USGS Lidar Base Specification** (building class 6, bridge deck 17) — point-cloud classification feeding footprints and DTMs.
- **GDPR** and national open-data licenses for building-level attributes ([Chapter 68](ch68-legal-issues.md), [Chapter 69](ch69-security-sovereignty-privacy-ethics.md)).

## Pitfalls

- **Comparing building heights with different reference points** → eave, ridge, mean, and percentile heights differ by meters → read both specifications; translate to one reference; check the residual histogram for bimodality.
- **A "DTM" that keeps podium or terrace levels, or interpolates meters off under large buildings** → ground filters see no ground inside big footprints → test against threshold surveys; flag footprints wider than the interpolation distance.
- **Roads under buildings vanishing from both DTM and DSM** → 2.5D surfaces cannot hold two elevations → keep a navigable-surface layer or network Z-levels; never route or flood-model from the DSM/DTM pair alone.
- **Bridge decks and viaducts removed from the DTM, then used for road grade** → the DTM is right for hydrology and wrong for the road → derive grade from the 3D road network or a road-surface layer.
- **Indoor maps with no vertical datum tie** → SLAM maps float; one-entrance ties fix offset only → survey at least three tie points; report registration residuals; store floor elevations in an outdoor datum.
- **Counting rooftop PV, HVAC, or green-roof growth as building height change** → DSM differencing is blind to semantics → classify rooftop equipment; store several roof heights; apply a minimum change area and height.
- **LoD1 volumes used for energy or population models with ± 30 % error** → height reference and roof shape ignored → use percentile heights near the median, document the reference, or use LoD2 volumes.
- **Footprints and lidar from different epochs** → reconstruction produces buildings with no points or points with no buildings → check footprint–point agreement per building before reconstruction; reconcile epochs.
- **Treating OSM `building:levels` × 3 m as measured height** → levels are crowd-sourced and floor heights vary 2.7–4.5 m → use as a prior with ± 1 storey; prefer lidar where available.
- **Utility depth from records treated as surveyed** → QL-D records refer to a ground surface that no longer exists → carry the ASCE 38 quality level; convert depths to invert elevations in a datum when exposed.
- **Flattened or removed sensitive sites mistaken for real terrain** → published models edit security-sensitive areas → check the provider's statement of edits; cross-check with imagery.
- **Mesh digital twin used as if it were a semantic model** → meshes have no building objects → reconstruct semantics or restrict use to measurement and visualization.

## Key takeaways

- Define "building" and "ground" per product—footprint convention, minimum size, attached structures, height reference, ground reference—and translate before comparing; the definitional error is usually larger than the measurement error.
- CityGML/CityJSON LoDs and the Biljecki sub-levels make the content of a model explicit; LoD1 volume is sensitive to height reference by tens of percent, and the 3D BAG practice of delivering several heights per building is the right answer.
- Cities are multi-valued: keep separate DTM, DSM, road-surface, and below-ground layers or a 3D network rather than forcing one surface; the road under the building is the case that breaks everything.
- "Ground under a building" in a DTM is an interpolation; test it against surveyed thresholds, and expect meters of error under podiums and on slopes.
- Indoor and underground data need an explicit registration to the outdoor datum (three or more ties) and an explicit quality level (ASCE 38); otherwise their elevations are not comparable with anything outside.
- Decide in advance whether rooftop equipment, cranes, and temporary structures count; store the decision as a class or attribute, not as an unexplained height.
- Validate per building (height against the stated reference, footprint IoU, val3dity validity) and per epoch (fraction verified against a newer DSM); report by roof type, size, and slope.
- Choose the surface by application—solar, wind, noise, RF, flood, and viewshed each need a different combination of ground, buildings, and vegetation—and keep vegetation separable.

## References

- Biljecki, F., Ledoux, H., and Stoter, J. (2016). An improved LOD specification for 3D building models. *Computers, Environment and Urban Systems*, 59:25–37.
- Biljecki, F., Ledoux, H., and Stoter, J. (2014). Height references of CityGML LOD1 buildings and their influence on applications. In *Proceedings of the 9th 3DGeoInfo Conference*, Dubai, UAE.
- Biljecki, F., Stoter, J., Ledoux, H., Zlatanova, S., and Çöltekin, A. (2015). Applications of 3D city models: State of the art review. *ISPRS International Journal of Geo-Information*, 4(4):2842–2889.
- Gröger, G., and Plümer, L. (2012). CityGML – Interoperable semantic 3D city models. *ISPRS Journal of Photogrammetry and Remote Sensing*, 71:12–33.
- Haala, N., and Kada, M. (2010). An update on automatic 3D building reconstruction. *ISPRS Journal of Photogrammetry and Remote Sensing*, 65(6):570–580.
- Kang, H.-K., and Li, K.-J. (2017). A standard indoor spatial data model—OGC IndoorGML and implementation approaches. *ISPRS International Journal of Geo-Information*, 6(4):116.
- Ledoux, H. (2018). val3dity: validation of 3D GIS primitives according to the international standards. *Open Geospatial Data, Software and Standards*, 3:1.
- Ledoux, H., Biljecki, F., Dukai, B., Kumar, K., Peters, R., Stoter, J., and Commandeur, T. (2021). 3dfier: automatic reconstruction of 3D city models. *Journal of Open Source Software*, 6(57):2866.
- Ledoux, H., Ohori, K. A., Kumar, K., Dukai, B., Labetski, A., and Vitalis, S. (2019). CityJSON: a compact and easy-to-use encoding of the CityGML data model. *Open Geospatial Data, Software and Standards*, 4:4.
- Peters, R., Dukai, B., Vitalis, S., van Liempt, J., and Stoter, J. (2022). Automated 3D reconstruction of LoD2 and LoD1 models for all 10 million buildings of the Netherlands. *Photogrammetric Engineering & Remote Sensing*, 88(3):165–170.
- Zlatanova, S., Sithole, G., Nakagawa, M., and Zhu, Q. (2013). Problems in indoor mapping and modelling. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, XL-4/W4:63–68.
- Kolbe, T. H., Kutzner, T., Smyth, C. S., Nagel, C., Roensdorf, C., and Heazel, C. (eds.) (2021). *OGC City Geography Markup Language (CityGML) Part 1: Conceptual Model Standard*, Version 3.0. OGC 20-010.
- American Society of Civil Engineers (2022). *Standard Guideline for Investigating and Documenting Existing Utilities*, ASCE/UESI/CI 38-22. ASCE, Reston, VA.
- Huang, J., Stoter, J., Peters, R., and Nan, L. (2022). City3D: Large-scale building reconstruction from airborne LiDAR point clouds. *Remote Sensing*, 14(9):2254.
- Rottensteiner, F., Sohn, G., Gerke, M., Wegner, J. D., Breitkopf, U., and Jung, J. (2014). Results of the ISPRS benchmark on urban object detection and 3D building reconstruction. *ISPRS Journal of Photogrammetry and Remote Sensing*, 93:256–271.

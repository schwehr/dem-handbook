# Chapter 57 — Visualizing DEMs: shading, colormaps, filtering, rendering, point clouds, splats

> **Part XII — Visualization and cartography.** Having built, stored, and validated elevation data in Parts VII–XI, the book now turns to making it visible: this chapter treats rendering as an analysis step with parameters that must be chosen and recorded, and [Chapter 58](ch58-making-maps.md) turns the rendered terrain into finished maps and charts.

**In this chapter.** A DEM is a table of numbers; everything you "see" in it is the product of a rendering decision. This chapter explains those decisions from first principles so that you can make terrain visible without lying about it. You will learn the Lambertian hillshade from Horn's 3 × 3 gradient to the azimuth and altitude conventions that make relief appear inverted; the multidirectional, sky-view-factor, openness, local-relief, and red-relief techniques that archaeologists and geomorphologists use to expose metre-scale features; why perceptually uniform colormaps (viridis, batlow, cmocean) are a correctness issue rather than a matter of taste and why the rainbow invents terraces that do not exist; how smoothing for display differs from smoothing for analysis; how to choose contour intervals; how 3D web terrain, point-cloud viewers with eye-dome lighting, and Gaussian-splat renderers work and what each one hides; and how to visualize uncertainty and time rather than only elevation. Every technique comes with the question this book keeps asking: what could this picture make me believe that the data do not support?

## 57.1 Purposes: exploration, analysis, communication

Three different jobs hide behind the word "visualization," and the choices that serve one actively harm another.

**Exploration and quality control** aims to reveal what is wrong. The ideal QC rendering is deliberately ugly: a slope map saturating at 2°, a hillshade lit from 10° altitude, a high-pass "detail" layer exposing the 5 cm flight-line steps a normal hillshade hides, a curvature map that turns every interpolation triangle into a visible facet. These renderings exaggerate noise on purpose, because noise is what you are looking for; legibility to outsiders is irrelevant and reproducibility is everything, so the rendering parameters belong in the QC log alongside the statistics of [Chapter 53](ch53-accuracy-assessment.md).

**Analysis** aims to let a trained eye perceive landform — slope breaks, convexity, drainage continuity — across scales from a few cells to the whole scene. The enemies are the single light source, which hides every slope that happens to face it, and the single technique, which privileges one feature class over others; blended multi-technique renderings (§57.4) exist for this purpose.

**Communication** aims to tell the truth attractively to someone who did not make the data — a planning board, a journal reader, the public. Legibility, convention, and restraint dominate: a colour-blind-readable colormap, a declared vertical exaggeration, a legend with units, a stated datum, and a visible indication of where the data are uncertain or absent. Communication renderings are the ones most likely to be reused out of context, so they must carry their own metadata.

Keep the three purposes separate in your workflow. The commonest failure in practice is to produce one rendering — usually a 315°/45° hillshade under a rainbow — and use it for all three jobs, where it reveals too little to the analyst, too much noise to the public, and misleads everyone about where the ridges are.

<!-- figure: Figure 57.1 — The same 1 m lidar DTM of a hillslope rendered four ways: (a) default 315°/45° hillshade; (b) low-altitude 15° hillshade exposing flight-line steps; (c) slope map saturating at 3° exposing interpolation facets; (d) multidirectional hillshade under a batlow hypsometric tint for communication. -->

## 57.2 Relief shading

### 57.2.1 The Lambertian hillshade and Horn's gradients

The analytical **hillshade** models the terrain as a matte (Lambertian) surface lit by a distant point source. The brightness of each cell is the cosine of the angle between the surface normal $\mathbf{n}$ and the direction to the light $\mathbf{l}$: $I = \max(0, \mathbf{n}\cdot\mathbf{l})$. Everything therefore depends on the normal, and the normal depends on how you estimate the two partial derivatives of elevation from a grid.

Horn (1981) derived the estimator that nearly every GIS uses. For a 3 × 3 window with cells labelled

```
a b c
d e f
g h i
```

and cell spacing $\Delta x$, $\Delta y$, the gradients at the centre cell $e$ are

$$
p = \frac{\partial z}{\partial x} \approx \frac{(c + 2f + i) - (a + 2d + g)}{8\,\Delta x},\qquad
q = \frac{\partial z}{\partial y} \approx \frac{(g + 2h + i) - (a + 2b + c)}{8\,\Delta y}.
$$

The weights (1, 2, 1) make this a Sobel operator: a smoothed central difference that suppresses single-cell noise at the cost of blurring the normal over three cells. The alternative Zevenbergen–Thorne (1987) estimator uses only the four edge neighbours and is sharper but noisier; GDAL exposes both (`-alg Horn` and `-alg ZevenbergenThorne`). Slope is $\tan\beta = \sqrt{p^2 + q^2}$ and aspect is $\tan\alpha = q/p$ with the quadrant resolved by the signs; the normal is $\mathbf{n} = (-p, -q, 1)/\sqrt{1 + p^2 + q^2}$. With a light at azimuth $\phi$ (clockwise from north) and altitude $\theta$ above the horizon, the light vector is $\mathbf{l} = (\sin\theta_z \sin\phi,\ \sin\theta_z\cos\phi,\ \cos\theta_z)$ with zenith angle $\theta_z = 90° - \theta$, and the shaded value in the form most GIS documentation prints is

$$
I = \cos\theta_z \cos\beta + \sin\theta_z \sin\beta \cos(\phi - \alpha).
$$

Two things in this formula are conventions rather than physics. The first is the units of $z$ relative to $\Delta x$: a geographic-coordinate DEM with metres of elevation and degrees of spacing yields gradients roughly 111,000 times too large unless a scale factor is applied (GDAL's `-s 111120` for metres-per-degree at the equator, with the cosine-of-latitude correction that the flag does *not* apply — see [Chapter 10](ch10-projections-and-resampling.md)). The second is a **vertical exaggeration** factor $z_f$ multiplying $p$ and $q$ (GDAL `-z`). Exaggeration of 2–5 is routine for low-relief terrain and is harmless *as long as it is declared*; undeclared, it makes a 2° coastal plain look alpine and invites readers to misjudge slope, which is exactly what a hillshade is used to judge.

### 57.2.2 Azimuth, altitude, and the inverted-relief illusion

The default light in essentially every package is azimuth 315° (north-west) and altitude 45°. The north-west convention is not arbitrary: the human visual system assumes light comes from above and, by a weaker margin, from the left; when a hillshade is lit from the south-east, most viewers perceive valleys as ridges and ridges as valleys — the **relief inversion** illusion (Imhof 1982; Bernabé-Poveda & Çöltekin 2015). Satellite imagery of the northern hemisphere is sun-lit from the south, so a Landsat scene beside a 315° hillshade of the same mountains shows opposite shading, and readers of raw imagery routinely see craters as domes. If you must light from the south (to match imagery, say), state it in the caption and consider adding a hypsometric tint, whose lightness gradient restores the correct reading.

Altitude controls contrast. At 45°, slopes facing away from the light go black at 45° steepness, and low-relief terrain shows almost no variation. Lower the light (15–25°) to see micro-relief; raise it (60–70°) to keep steep terrain legible. The "right" altitude depends on the scene's slope distribution, which is why a single default fails across a continent.

### 57.2.3 Multidirectional shading, shadows, and ambient occlusion

A single light hides all slopes parallel to it and renders those facing it uniformly bright. Mark (1992) proposed the **multidirectional oblique-weighted (MDOW)** hillshade: compute four hillshades from azimuths 225°, 270°, 315°, and 360° and combine them with per-cell weights proportional to $\sin^2(\alpha - \phi_i)$, so that each cell is lit mainly by the lights most oblique to its aspect. GDAL implements this as `gdaldem hillshade -multidirectional`; Esri's "multidirectional hillshade" in ArcGIS Pro follows the same idea with six lights. The result keeps relief legible in every aspect while remaining a shaded-relief image a reader intuitively understands. A simpler alternative, GDAL's `-combined`, multiplies a hillshade by a slope-shading term so that flat areas are bright regardless of aspect and steep ones darker — useful for QC but not a physical illumination.

**Cast shadows** (ray-traced occlusion of the light by intervening terrain) add realism and depth cues in mountain scenes but destroy information in the shadowed areas; most analytical shading omits them. **Ambient occlusion** and **sky-view factor** (next subsection) replace the point light with a hemisphere of diffuse sky, which produces the soft, shadowless shading of an overcast day and, crucially, does not depend on azimuth. Kennelly and Stewart (2014) treat general sky models for terrain.

### 57.2.4 Sky-view factor, openness, and the local relief model

The **sky-view factor (SVF)** of a cell is the fraction of the sky hemisphere visible from it. Zakšek, Oštir, and Kokalj (2011) introduced it as a relief visualization: for each of $n$ azimuth directions (typically 8–32), find the maximum horizon elevation angle $\gamma_i$ within a search radius $R$, and compute

$$
\mathrm{SVF} = 1 - \frac{1}{n}\sum_{i=1}^{n}\sin\gamma_i .
$$

Pits, ditches, and valley floors see little sky and render dark; ridges and mounds see most of it and render bright; a flat plain renders uniformly bright. Because SVF depends only on terrain within $R$, that radius sets the scale of features emphasized — 5–10 cells for archaeological micro-relief, hundreds for valley systems — and must be reported with the image.

**Openness** (Yokoyama, Shirasawa & Pike 2002) is the older cousin. **Positive openness** is the mean, over eight directions, of the zenith angle to the horizon ($90° - \gamma_i$); **negative openness** is the mean nadir angle to the "underside horizon," which highlights concavities. Unlike SVF, positive openness can exceed 90° on convexities, so it separates ridges from flat ground more strongly. Doneus (2013) showed openness to be the most robust single technique for interpretive archaeological mapping because it is independent of illumination direction and, unlike SVF, does not saturate on flats.

The **local relief model (LRM)** (Hesse 2010) subtracts a low-pass (large-kernel mean or trend) surface from the DEM, leaving the small-scale residual, and then refines the low-pass surface through the zero-contours of the first residual to reduce ringing. The output is a metric quantity — local elevation above or below the surroundings, in metres — which makes it the one technique in this family that supports direct measurement of feature height. Simpler "difference from mean elevation" and **topographic position index (TPI)** rasters are single-pass approximations.

### 57.2.5 Slope and curvature shading; the Red Relief Image Map

A slope map rendered in greyscale (flat = white, steep = black) is a shaded-relief image without a light source, and Pingel and Clarke (2014) show that a perceptually scaled slope map reads nearly as well as a hillshade while remaining a quantitative layer. Curvature maps (profile, plan, or total) expose breaks of slope and are the most sensitive display of interpolation artefacts — triangular facets, stair-steps from contour-derived DEMs, and pixel-locked striping all appear as curvature texture long before they are visible in a hillshade.

Chiba, Kaneta, and Suzuki (2008) combined these ideas into the **Red Relief Image Map (RRIM)**: slope drives red saturation, and the difference between positive and negative openness (a "ridge–valley index") drives lightness. The result reads correctly from any orientation, has no shadow, and shows ridges bright, valleys dark, and steep slopes red; it is standard in Japanese geomorphological and hazard mapping. The method is patented by Asia Air Survey Co., which has limited its appearance under that name in some software, although the ingredients (slope and the two openness rasters) are available in RVT, SAGA, and WhiteboxTools and can be blended by hand.

### 57.2.6 Manual, learned, and atmospheric shading

The analytical techniques above compute shading cell by cell; a human relief artist does not. Imhof (1982) codified the Swiss manual tradition: light direction adjusted locally so that every ridge is lit from its best side, major landforms generalized and minor ones suppressed, tone lightened at high elevations ("aerial perspective") and in valley bottoms. Analytical imitations include Marston and Jenny's (2015) landform-adaptive light direction. Jenny et al. (2021) trained a convolutional network on swisstopo's manual relief to shade terrain the way a cartographer does; the technique ships in the closed-source application Eduard (2023–). Learned shading is a communication tool: it hides small-scale detail deliberately, so it is unsuitable for QC, and because it is trained on alpine relief it can hallucinate ridge structure on other terrain types. Treat it like any other model and check it against a plain hillshade.

> **Rule of thumb.** Report every relief rendering with at least five parameters: technique, azimuth(s), altitude, vertical exaggeration, and (for SVF/openness/LRM) the search radius or kernel size in cells and in metres. If those five are absent, the image cannot be reproduced and should not be used as evidence. The rule holds for QC logs, papers, and web maps alike; it does not apply to purely illustrative artwork, which should be labelled as such.

## 57.3 Colormaps

### 57.3.1 Perceptual uniformity

A colormap is a function from a data value to a colour. For a reader to recover the data from the colour, equal steps in data should produce equal perceptual steps in colour, and the perceived lightness should change monotonically so that the eye's dominant channel — luminance, which carries the spatial detail the visual system actually uses to see shape — tells the same story as the hue. Colormaps that satisfy this are **perceptually uniform**; the test is to plot CIELAB $L^*$ (or the lightness $J'$ of CAM16-UCS) against data value and look for a straight line. Kovesi (2015) gives a design method and a diagnostic: render a sinusoidal test pattern of constant amplitude on a ramp, and any colormap in which the ripples vanish or jump in visibility at some value is distorting the data at that value.

The standard families that pass this test are viridis and its relatives (designed by van der Walt and Smith in 2015 in CAM02-UCS space for matplotlib), cividis (Nuñez, Anderton & Renslow 2018, optimized for red–green colour-vision deficiency), Crameri's Scientific Colour Maps (batlow for sequential data, oleron for topography with a sea–land zero, vik and roma for diverging), and the cmocean suite (Thyng et al. 2016; `topo`, `deep`, `balance`). Each is perceptually ordered, colour-blind-readable, and prints to greyscale in the right order. Crameri, Shephard, and Heron (2020) found a large fraction of published scientific figures still using rainbow or jet; theirs is the citation to hand to a colleague who objects that colormap choice is cosmetic.

### 57.3.2 Why rainbow and jet are harmful

The rainbow (and matlab's jet) fails all three tests at once. Its lightness is non-monotonic — yellow is the brightest colour in the middle of the range, so the brightest band on a rainbow DEM is a mid-elevation contour, not the summit. Its perceptual step size is wildly uneven: the transition through cyan–green–yellow spans a narrow data range but a wide perceptual one, so **false boundaries** appear at those values and look like terraces, shorelines, or breaks of slope that do not exist; elsewhere (the long blue and the long red) large data differences are invisible. And it is unreadable to the roughly 8 % of men and 0.5 % of women with red–green colour-vision deficiency (approximate; prevalence varies by population), for whom green–yellow–red collapse to a single band. Borland and Taylor (2007) documented these problems for the visualization community; nothing in the subsequent two decades has rehabilitated the map. The one defensible use of a rainbow-like map is a cyclic quantity such as aspect, where a perceptually designed cyclic map (e.g., Crameri's romaO, cmocean `phase`) exists for the purpose.

### 57.3.3 Hypsometric tints and bathymetric conventions

**Hypsometric tints** colour elevation bands by convention: greens for lowlands, yellows and browns for uplands, greys and whites for high mountains. The nineteenth-century convention carries a well-known lie — green lowlands are not necessarily vegetated, and deserts at sea level look lush. Patterson and Jenny's (2011) **cross-blended hypsometric tints** vary the scheme with latitude and climate zone (arid lowlands tan, humid lowlands green, polar lowlands grey-white) so that the map matches the reader's expectation of land cover without pretending to map it; Natural Earth distributes them with its shaded relief.

Bathymetry has its own conventions. Nautical charts use a small number of flat **depth tints** (typically white beyond a safety contour, a light blue between it and a shallow contour, a darker blue in the shallowest band, and green or ochre for the drying zone), with the breaks placed at depths that matter for the vessel, not at equal intervals (IHO S-4; S-52 for ECDIS). This is **shoal-biased** colouring: the question a chart answers is "is it deep enough," so the colour boundaries sit at the depths that answer it, and a cell straddling a boundary is coloured as the shallower class. Scientific bathymetry, by contrast, usually uses a continuous sequential map (cmocean `deep`, GMT's `geo` or `bathy` CPTs) in which deeper is darker — the opposite lightness ordering from hypsometric tints — so that a combined land–sea colormap such as Crameri's oleron or cmocean `topo` has its lightest values at the coast and darkens in both directions. That shared bright coastline is intentional and legible, but it also means the zero of the colormap must sit exactly at the vertical datum of the data, which is rarely the datum a reader expects ([Chapter 9](ch09-vertical-datums.md)).

### 57.3.4 Diverging, discrete, and dual-encoded maps

Change maps — a DEM of difference (DoD) from [Chapter 41](ch41-change-detection.md) — need a **diverging** map with a neutral centre at zero (vik, balance, RdBu) and *symmetric limits*, so that +2 m and −2 m are equally saturated. Letting software autoscale a DoD to its asymmetric min/max is the most common way to publish a change map that visually exaggerates one sign. Mask the band within the minimum detectable change in grey or white so that noise is not read as change.

**Discrete** (classed) maps turn a continuous DEM into a handful of bands. They are legible and easy to legend, but every class boundary is a visual edge, and a reader will treat it as a feature; place the boundaries where they mean something (flood stage, a safety contour, a datum) and never at round numbers for their own sake. Continuous maps avoid false edges but make it impossible to read a value to better than about one part in twenty.

A hillshade carries shape; a colormap carries value. Combining them — **dual encoding** — is the standard terrain map, and the blend matters. Multiplying colour by hillshade preserves hue but darkens everything, which is why multiply-blended hypsometric maps look muddy unless the hillshade is lightened first. Replacing the lightness channel (HSV/HSL blending) with the hillshade is perceptually cleaner but means lightness no longer encodes elevation at all. The honest rule is that in a dual-encoded map the colormap should be chosen for hue and saturation discriminability, since relief will override its lightness; never encode a second quantitative variable in lightness on top of a hillshade.

> **Try it.** Build a reproducible hillshade–tint composite with GDAL and a perceptual colormap. The expected result is a GeoTIFF whose relief reads correctly from the north-west and whose tint is colour-blind-readable; swapping `-az 315` for `-az 135` should make the valleys look like ridges.
>
> ```bash
> # 1. Multidirectional hillshade (Mark 1992), vertical exaggeration 1, metres in and out
> gdaldem hillshade dtm.tif hs_multi.tif -multidirectional -alt 45 -z 1 -compute_edges -co COMPRESS=DEFLATE
>
> # 2. Colour relief with Crameri's batlow (10 anchor colours, min/max of your DEM)
> python - <<'EOF'
> import numpy as np
> from cmcrameri import cm            # pip install cmcrameri
> from osgeo import gdal
> ds = gdal.Open("dtm.tif"); b = ds.GetRasterBand(1)
> lo, hi = b.ComputeRasterMinMax(False)
> with open("batlow.txt", "w") as f:
>     for v in np.linspace(lo, hi, 10):
>         r, g, bb, _ = cm.batlow((v - lo) / (hi - lo))
>         f.write(f"{v:.2f} {int(r*255)} {int(g*255)} {int(bb*255)}\n")
>     f.write("nv 0 0 0 0\n")
> EOF
> gdaldem color-relief dtm.tif batlow.txt tint.tif -alpha -co COMPRESS=DEFLATE
>
> # 3. Multiply blend (hillshade scaled to 0.4–1.0 so colours are not crushed)
> gdal_calc.py -A tint.tif --A_band=1 -B hs_multi.tif --outfile=r.tif --calc="A*(0.4+0.6*B/255.0)" --type=Byte
> gdal_calc.py -A tint.tif --A_band=2 -B hs_multi.tif --outfile=g.tif --calc="A*(0.4+0.6*B/255.0)" --type=Byte
> gdal_calc.py -A tint.tif --A_band=3 -B hs_multi.tif --outfile=b.tif --calc="A*(0.4+0.6*B/255.0)" --type=Byte
> gdal_merge.py -separate -o composite.tif r.tif g.tif b.tif
> ```
>
> Record the command lines with the figure; they *are* the figure's metadata.

<!-- figure: Figure 57.2 — Lightness (CIELAB L*) versus data value for jet, viridis, batlow, cmocean topo, and a classic hypsometric scheme, with the Kovesi sinusoidal test strip under each; jet's L* peak at yellow and the resulting false terrace are annotated. -->


## 57.4 Filtering for display versus filtering for analysis

Every DEM you look at has been filtered — by the sensor footprint, the gridding interpolator, the overview pyramid at the current zoom — and most are filtered again before publication because raw lidar grids look "noisy." The distinction this section insists on is between filters applied to a *display copy*, which are legitimate rendering parameters, and filters applied to the *analysis grid*, which change the data and must be treated as a processing step with lineage ([Chapter 29](ch29-processing-pipelines.md)).

**Low-pass smoothing.** A Gaussian kernel of standard deviation $\sigma$ cells attenuates features smaller than roughly $2\sigma$–$3\sigma$ cells and reduces random per-cell noise by a factor approaching $2\sigma\sqrt{\pi}$ for white noise. It also lowers every peak and fills every pit, by an amount that grows with curvature: a 3 m wide, 1 m deep ditch in a 1 m grid loses most of its depth under a $\sigma = 2$ Gaussian. A **median** filter preserves step edges (terraces, kerbs) better than a Gaussian and removes isolated spikes entirely, which is why it is the usual choice for display of DSMs with residual noise; but it flattens narrow ridges and ditches just as thoroughly. **Feature-preserving** filters — bilateral, anisotropic diffusion, normal-based mesh denoising adapted to grids — smooth within homogeneous regions while preserving breaks of slope. They are excellent for display and dangerous for analysis because the "features" they preserve are defined by a gradient threshold, so they sharpen genuine edges and spurious ones alike: a feature-preserving filter will turn a soft 10 cm flight-line seam into a crisp step.

**High-pass and detail layers.** Subtracting a smoothed copy from the original (an unsharp mask, equivalent to a crude LRM) yields a residual layer that shows only small-scale relief. Added back with gain > 1 it "exaggerates micro-topography" — a display trick that is enormously effective for revealing ploughed-out earthworks, old field boundaries, and processing artefacts alike. The archaeological community formalized the practice in the **Relief Visualization Toolbox (RVT)** (Kokalj & Hesse 2017; first released 2011) with blends such as the **Visualization for Archaeological Topography (VAT)**, which overlays SVF, positive openness, slope, and hillshade with tuned opacities (Kokalj & Somrak 2019). These blends are meant to be *looked at*, not measured.

**De-striping.** Lidar and InSAR DEMs carry along-track or cross-track stripes at the few-centimetre to decimetre level from residual calibration or trajectory error ([Chapter 18](ch18-topographic-lidar.md), [Chapter 21](ch21-radar-sar-insar.md)). Fourier-domain notch filtering or directional median filtering can suppress them for display. Applying the same filter to the analysis grid removes the symptom while leaving the underlying positional error, and — because real linear features (roads, drains, dykes) share the stripe orientation in agricultural landscapes — it removes some of them too.

How display filters hide and invent features is worth stating plainly. Smoothing hides anything narrower than the kernel, which includes the drainage ditch a flood model needs ([Chapter 61](ch61-hydrology.md)) and the kerb that defines a sidewalk. Feature-preserving filters invent edges where noise crosses the gradient threshold. High-pass gain invents relief amplitude: a 5 cm residual shown with 10× gain looks like a 50 cm bank, and nothing in the image says otherwise. The protection is procedural: filter only a copy, name the copy's file after the filter (`dtm_1m_gauss_s2.tif`), and never let the display copy become the input to a slope, volume, or hydrological computation.

> **Worked example.** A 1 m lidar DTM has per-cell random noise σ = 0.04 m and contains a buried pipeline trench expressed as a 0.6 m wide, 0.08 m deep linear depression. A Gaussian of σ = 1.5 cells is applied for display. Noise after filtering is roughly 0.04 / (2 × 1.5 × √π) ≈ 0.04 / 5.3 ≈ 0.008 m — the surface looks beautifully clean. The trench, however, has a cross-section narrower than one cell; its depth after convolution with the kernel is at most 0.08 × (0.6 m / (√(2π) × 1.5 m)) ≈ 0.08 × 0.16 ≈ 0.013 m, now comparable to the residual noise and invisible. A low-altitude hillshade of the *unfiltered* grid shows the trench clearly despite the noise because the eye integrates along the line. Conclusion: for linear-feature QC, do not pre-smooth; choose the light instead.

## 57.5 Contours and labels

Contours are the oldest quantitative display of elevation and the only one most readers can interpret numerically without a legend. [Chapter 58](ch58-making-maps.md) treats contour cartography and [Chapter 59](ch59-vector-data.md) treats contours as vector data; here the concern is choosing and rendering them as a visualization.

**Interval.** The interval should be no finer than the DEM's vertical uncertainty justifies — the NMAS tradition requires 90 % of contours to lie within half an interval of truth, so a 1 m interval presumes roughly 0.3 m RMSE — and no finer than legibility allows on the steepest slopes at the display scale. If the minimum legible contour spacing on screen or paper is $s$ (about 0.25 mm on paper, ≈ 2 px on screen) at scale $1{:}M$, slopes steeper than $\tan\beta = \mathrm{CI}/(sM)$ will merge. For a 1:25,000 map with $s$ = 0.25 mm, a 10 m interval merges above about 58°; a 2 m interval merges above 18°, which is why fine intervals demand large scales or supplementary contours used only on flat ground.

**Smoothing and generalization.** Contours traced through raw 1 m lidar look like torn paper — every cell's noise becomes a wiggle. Smooth either the grid (a display copy, per §57.4) or the lines (Chaikin or Gaussian smoothing, or Douglas–Peucker simplification with a tolerance well under the cell size). Grid smoothing is preferable because it preserves topology; line smoothing can make adjacent contours cross on steep slopes. **Index contours** (every fourth or fifth, heavier and labelled) make counting possible. **Depression contours** carry hachure ticks on the downslope side; without them a sinkhole in a karst DEM is simply a small hill. Labels run along the line, reading uphill by convention; automated placement (QGIS, Mapnik) handles most of this but needs human review on steep ground.

**Isobaths** follow the same geometry with an added safety rule. Depth contours on charts are generalized **shoal-biased**: when a contour is smoothed or simplified, it may move only toward deeper water, so that the area enclosed on the shallow side never shrinks. A shoal that the generalized isobath "cuts off" is a grounding waiting to happen. The scientific-bathymetry equivalent — contours drawn through a smoothed multibeam grid — has no such rule and should never be used for navigation ([Chapter 62](ch62-navigation-and-charting.md)).

## 57.6 3D rendering

A perspective view adds the depth cue that plan-view shading only simulates, and it costs the reader the ability to measure anything. That trade governs all 3D terrain graphics.

**Perspective views and flyovers.** A static oblique view from a declared camera (position, look-at point, field of view) with a declared vertical exaggeration is a legitimate figure; a flyover is a communication device and nothing else. Both suffer from occlusion — the backs of ridges are invisible — and from perspective foreshortening, which compresses distant terrain. Vertical exaggeration in 3D is more seductive and more misleading than in 2D, because the eye has no reference for "true" relief; exaggerations of 2–3 are usual, and anything above 1 must appear in the frame or caption.

**Texture draping.** Draping an orthoimage or a hillshade–tint composite over the terrain mesh is how most 3D terrain is coloured. Note what happens at the seams: an orthoimage made from a DSM draped on a DTM shows buildings smeared flat onto the ground; a hillshade texture adds a second, baked-in light source that fights the renderer's own lighting, which is why 3D viewers usually drape a tint without hillshade and let the engine shade.

**Level-of-detail streaming.** Web 3D terrain works by streaming tiles at a resolution that depends on screen-space error: Cesium's **quantized-mesh** and **3D Tiles** (an OGC Community Standard since 2019, version 1.1 in 2023), deck.gl's `TerrainLayer`, and MapLibre GL JS's `raster-dem` terrain all request coarser tiles for distant terrain and finer ones near the camera. The elevation itself is usually delivered as an RGB-encoded PNG — Mapbox Terrain-RGB encodes $h = -10000 + 0.1\,(256^2 R + 256 G + B)$ and Mapzen Terrarium encodes $h = 256 R + G + B/256 - 32768$ — which gives decimetre quantization and strips every datum and unit statement from the data. Nothing in a Terrain-RGB tile says whether its heights are EGM96 or ellipsoidal; viewers assume whatever their globe assumes (Cesium's globe is WGS 84 ellipsoidal), so a 3D web map is an excellent place to introduce a 30 m vertical offset and never notice. WebGL remains the delivery substrate; WebGPU (shipping in major browsers since 2023–2024) is arriving for compute-heavy rendering such as splats.

**Lighting that lies.** Rendering engines light terrain with physically based shaders designed for games: specular highlights make a hydro-flattened lake look like glass, a glossy snow material makes a glacier look like plastic, and a sun position taken from the wall clock lights a northern-hemisphere scene from the south and inverts relief (§57.2.2). Turn specular off, light from the north-west (or use hemispheric ambient lighting), and label the vertical exaggeration.

## 57.7 Point clouds

For QC of lidar and sonar data, the point cloud is the primary object and the grid is a derivative; a visualization that goes straight to the grid hides the classification and the per-point attributes where most errors live ([Chapter 30](ch30-point-cloud-classification.md)).

**Eye-dome lighting (EDL)** (Boucheny 2009) is the shading technique that made dense point clouds legible. For each pixel it compares the depth of the rendered point with the depths of its screen-space neighbours and darkens pixels that are farther than their surroundings, producing a cheap screen-space ambient-occlusion effect that outlines every object and every depth discontinuity. EDL needs no normals, which raw point clouds lack, and it works in any viewing direction. It is the default in CloudCompare, Potree, and most modern viewers; its strength parameter and neighbourhood radius are rendering choices that affect how prominent small-scale noise appears.

**Point size and density.** Fixed-pixel point sizes make dense regions opaque and sparse regions see-through, which is a perfectly good density visualization and a poor surface one. Adaptive point sizes (by local density or by octree level) produce a continuous-looking surface at the cost of hiding density variation — and density variation is exactly what a QC reviewer needs to see in overlap zones and at swath edges ([Chapter 26](ch26-survey-planning.md)). Keep both modes.

**Colour.** Colour by classification (ASPRS codes) to check ground extraction; by intensity or backscatter for pavement markings and seafloor type; by height to read terrain; by return number to see canopy penetration; by GPS time or flight line to expose strip misalignment; and, when the data carry it, by per-point uncertainty (TVU/THU; [Chapter 20](ch20-sonar.md)). Colour by flight line with a categorical palette is the fastest way to find a strip offset: in a well-calibrated block the colours interleave randomly on the ground, and any coherent band is a problem.

**Cross-sections and profiles are the main QC tool.** A plan view, however shaded, cannot show that the ground points in one strip sit 12 cm above those in the next, that a bridge deck was classified as ground, or that a multibeam outer beam curls upward at the swath edge; a 1–2 m wide vertical slice viewed side-on shows all three immediately. Make it a reflex to look at a few dozen slices across strip overlaps, water edges, and steep terrain before accepting any dataset. A quantitative strip-difference raster complements the slices but does not replace them.

**Viewers.** **Potree** (Schütz 2016) renders billions of points in a browser from a multi-resolution octree; the **COPC** format ([Chapter 47](ch47-file-formats.md)) makes a single LAZ file streamable to Potree-style viewers (e.g. viewer.copc.io) with HTTP range requests. **CloudCompare** is the desktop workhorse for slicing, cloud-to-cloud distance, and EDL rendering. VR viewers help communicate complex 3D scenes (caves, forest structure); for QC they add little beyond a good slicing tool and cost in reproducibility.

<!-- figure: Figure 57.3 — A 2 m wide cross-section through overlapping lidar strips coloured by PointSourceId, showing a 0.11 m vertical offset between strips that is invisible in the hillshade shown above it; EDL-rendered plan view on the left for context. -->

## 57.8 Neural and splat rendering

Since 2020 two families of image-based renderers have made photorealistic 3D scenes from the same photographs that structure-from-motion ([Chapter 22](ch22-photogrammetry-sfm.md)) uses. **Neural radiance fields (NeRF)** (Mildenhall et al. 2020) train a small network to map a 3D position and viewing direction to colour and volume density, then render novel views by integrating along rays. **3D Gaussian splatting (3DGS)** (Kerbl et al. 2023) instead represents the scene as millions of anisotropic 3D Gaussians with colour and opacity, initialized from the SfM sparse cloud and optimized by rendering them ("splatting") into training views; it renders in real time and has largely displaced NeRF for interactive use. Open implementations include nerfstudio and gsplat; several photogrammetry packages now export splats.

What these renderers produce is spectacular and, for the purposes of this book, **non-metric by default**. A splat scene optimizes photometric reproduction of the training images, not geometric fidelity: Gaussians float in front of surfaces where that reproduces view-dependent appearance better, thin structures become translucent clouds, and regions seen from few angles are filled with plausible texture rather than left empty. Scale and orientation are inherited from the SfM solution, so if that was georeferenced with GCPs ([Chapter 59](ch59-vector-data.md) §59.6) the splats are too — but there is no per-splat uncertainty, no notion of a ground return, and no way to validate against checkpoints except by extracting a surface (depth rendering or mesh extraction), which brings back photogrammetry's error budget plus the splat's own. Research on metric splats is moving fast; as of this writing none of it has the validation literature that lidar and stereo photogrammetry have.

Use splats and NeRFs for what they are good at: public engagement, virtual site visits, visual context for a dataset that was *also* delivered as a validated point cloud or DEM, and rapid visual inspection of SfM coverage (holes in the splat scene map onto holes in the photo coverage). Do not use them for measurement, change detection, volumes, or anything that will be checked against ground truth, and do not deliver them without a statement that they are a visualization product. [Chapter 46](ch46-data-models.md) treats splats as a data model.

## 57.9 Visualizing uncertainty

A DEM rendered as a crisp surface tells the reader that the surface is known. Usually it is not known to better than a few decimetres, often not to a few metres, and in some cells it is interpolated across voids with no observations at all ([Chapter 35](ch35-voids-and-overhangs.md)). The uncertainty layers this book insists on producing ([Chapter 53](ch53-accuracy-assessment.md)) are worthless if they stay in a side file. MacEachren et al. (2005, 2012) reviewed and tested the visual-variable options; the practical repertoire for elevation is small.

**Transparency or fog** fading the terrain where uncertainty is high is intuitive and widely implemented, but it also fades the shape cues, so uncertain terrain looks *flatter*, which conflates "poorly known" with "featureless." **Noise texture** — overlaying grain whose amplitude scales with σ — keeps shape visible while signalling doubt, and it maps naturally to the idea of "fuzziness"; its failure mode is that it resembles data noise. **Bivariate colormaps** encode elevation in hue and uncertainty in saturation or lightness (a 3 × 3 or 4 × 4 legend); they are compact and work in print but demand a legend and a carefully designed palette. **Confidence hatching** on change maps — hatching or stippling cells where |Δh| is below the level-of-detection — is the most important single technique in this section, because a DoD without it will be read as showing change everywhere.

**Ensembles and animation.** When uncertainty is spatially correlated — and DEM error always is ([Chapter 5](ch05-error-and-uncertainty.md)) — a per-cell σ map understates it badly. Rendering several conditional realizations side by side, or as **hypothetical outcome plots** (animated "hops" between realizations), shows the reader how much a ridge line or a flood boundary actually moves; it is the only visualization that conveys correlated error honestly. **Contour bands** — the envelope swept by a contour across realizations, or the ±2σ offset of a single contour — serve the same purpose in print and are far more informative than a single confident line.

For bathymetry, the chart tradition already does this: the CATZOC/ZOC diagram ([Chapter 58](ch58-making-maps.md)) and the S-102 uncertainty band are uncertainty visualizations, and the forthcoming S-101/S-102 presentation rules carry them into ECDIS.

## 57.10 Visualizing time

Terrain changes ([Chapter 37](ch37-time-scales-of-change.md)), and two stills — "before" and "after" — are the standard way of showing it and the least informative. A **swipe** or **slider** between two co-registered renderings lets the reader locate change by motion, which the visual system detects with great sensitivity; a **DoD map** with a zero-centred diverging colormap and an LoD mask quantifies it; a **flicker** (rapid alternation) catches sub-pixel misregistration, which appears as apparent uniform movement of everything — and so doubles as a co-registration check ([Chapter 41](ch41-change-detection.md)). **4D point clouds** (colour by epoch) and multi-epoch animations are needed to show *process* — a dune migrating, a slope creeping, a river braiding — and to distinguish steady trends from the single event two stills imply. Two-epoch stills encode whatever happened between two arbitrary dates as the whole story: a seasonal snow difference becomes "ice loss," a tide-stage difference "coastal erosion." Put acquisition dates and times, not just years, on both panels, and use multi-epoch data when the question is about a rate.

## 57.11 Accessibility and reproducibility

**Colour-vision deficiency** affects enough readers that a map unreadable under simulated deuteranopia and protanopia is defective; viridis, cividis, batlow, and ColorBrewer's "colorblind safe" schemes pass, and simulators (Color Oracle, `colorspacious`, Coblis) check in seconds. Avoid red–green diverging maps for change; use blue–brown or purple–green. **WCAG 2.1** requires 4.5:1 contrast for text and 3:1 for meaningful graphics (criterion 1.4.11), which rules out light-grey labels over hillshade. **Screen readers** cannot read a map image; provide alt text stating what the map shows, source and date, and a numeric summary. **Tactile and 3D-printed terrain** is routine (QGIS DEMto3D to STL; 3–5× exaggeration at 1:10,000 is typical) — declare the exaggeration on the model.

**Reproducibility** is the link back to validation. A figure made by hand in a desktop GIS cannot be regenerated when the DEM is reprocessed. Script figures (GDAL/GMT/matplotlib/R, or a QGIS project plus the PyQGIS export call) and keep the script with the data. The caption or metadata should state the DEM (name, version, epoch, datum), the technique and the parameters of §57.2's rule of thumb, the colormap and its limits, and any mask applied — the visual analogue of a map sheet's accuracy statement.


## Then & now

Relief depiction predates the DEM by two centuries.

- **Hachures (Lehmann 1799) ⟨H⟩** — slope-proportional strokes, a slope map in ink; they survive only as depression ticks.
- **Hand-painted Swiss relief (Imhof, 1920s–1960s)** — locally adjusted light, aerial perspective, generalized landform; still the benchmark for analytical methods.
- **Analytical hillshade (Yoëli 1965)** — Lambertian shading computed from a terrain grid; Horn (1981) supplied the general gradient and reflectance-map theory.
- **GIS hillshade default (1980s–1990s)** — 315°/45° became the visual vernacular; Mark's (1992) multidirectional alternative took two decades to reach default menus.
- **Multi-technique archaeological visualization (RVT 2011)** — SVF, openness, and LRM bundled for light-independent prospection under forest; VAT blends became standard.
- **Web 3D terrain (2010s)** — Cesium, Mapbox/MapLibre, deck.gl streamed LOD terrain with RGB-encoded elevation, gaining reach and losing datum metadata.
- **Neural rendering (2020–)** — NeRF and 3D Gaussian splatting made photoreal rendering from photographs routine, a product that looks like survey data and is not.

Parameters moved from the artist's hand into explicit, recordable settings — and, with learned shading and splats, back into implicit network weights. The reproducibility discipline of §57.11 is how to keep the gain.

## Mathematics

**Error propagation into shading.** Horn's operator is a linear filter, so for independent cell errors of variance $\sigma_z^2$,

$$
\sigma_p^2 = \frac{\sigma_z^2}{(8\Delta x)^2}\,(1^2+2^2+1^2)\times 2 = \frac{12\,\sigma_z^2}{64\,\Delta x^2} = \frac{3\sigma_z^2}{16\,\Delta x^2},
$$

i.e. $\sigma_p \approx 0.43\,\sigma_z/\Delta x$. For a 1 m grid with $\sigma_z$ = 0.05 m, $\sigma_p \approx 0.022$, or about 1.2° of slope noise — visible as grain in a 15° hillshade of flat ground and invisible at 45°. Coarsening to 2 m halves it; the Zevenbergen–Thorne estimator gives $\sigma_p = \sigma_z/(\sqrt{2}\,\Delta x)$, about 1.6 times noisier.

**Multidirectional weights (Mark 1992).** With lights at azimuths $\phi_i \in \{225°, 270°, 315°, 360°\}$ and cell aspect $\alpha$, the weights are $w_i = \sin^2(\alpha - \phi_i)$ and the combined shade is $I = \sum_i w_i I_i / \sum_i w_i$; because $\sum_i \sin^2(\alpha-\phi_i) = 2$ for four lights spaced 45° apart, the denominator is constant.

**Sky-view factor and openness.** For $n$ azimuths and horizon elevation angles $\gamma_i$ within radius $R$, $\mathrm{SVF} = 1 - \frac{1}{n}\sum_i \sin\gamma_i$ (§57.2.4), which is the fraction of the projected hemisphere unobstructed under the assumption of an isotropic sky; the exact hemisphere fraction would weight by $\sin\gamma\cos\gamma$, and both forms are in use — check which one your software implements before comparing SVF values across tools. Positive openness is $\Phi_R = \frac{1}{8}\sum_{i=1}^{8}(90° - \gamma_i)$ and negative openness $\Psi_R = \frac{1}{8}\sum_i (90° - \delta_i)$ with $\delta_i$ the nadir-side angle computed on the inverted surface.

**Multiscale relief filters.** The LRM is $z - \mathcal{L}_R\{z\}$ for a low-pass operator $\mathcal{L}_R$ of radius $R$, which in the frequency domain is a high-pass filter $1 - \hat{L}_R(k)$; a Gaussian $\mathcal{L}$ with standard deviation $\sigma$ passes wavelengths longer than about $2\pi\sigma$ into the "regional" surface and leaves shorter ones in the LRM. Reported LRM amplitudes are therefore band-limited, and a feature's LRM height approaches its true height only when the feature width is well below $\sigma$ and its surroundings are flat over several $\sigma$.

**Perceptual colour spaces.** CIELAB defines lightness $L^* = 116 f(Y/Y_n) - 16$ with $f(t) = t^{1/3}$ for $t > (6/29)^3$ and a linear segment below; equal $\Delta E^*_{ab} = \sqrt{\Delta L^{*2} + \Delta a^{*2} + \Delta b^{*2}}$ is approximately equal perceived difference, with known failures in the blue region that CAM16-UCS corrects. A colormap $c(v)$ is perceptually uniform if $\|dc/dv\|$ in the UCS is constant and lightness-monotonic if $dL^*/dv$ does not change sign. The luminance channel carries the fine spatial detail (the visual system's contrast sensitivity to luminance extends to much higher spatial frequencies than to chrominance), which is why a colormap with non-monotonic lightness cannot be rescued by hue ordering.

## Validation & uncertainty

Visualization introduces error at three points: in what the rendering computes, in what the human perceives, and in what the rendering omits. Each can be tested.

**Computational checks.** A hillshade is a derivative product and inherits the grid's noise amplified by $1/\Delta x$ (Mathematics). Check the *scale* of your rendering first: push a synthetic cone or known-slope plane through the same pipeline and confirm the shade matches the analytic $\cos$ value; this catches unit mistakes (degrees vs metres), misapplied exaggeration, and edge handling (GDAL's `-compute_edges`). For SVF/openness/LRM, render a synthetic ditch of known width and depth and note the radius at which it disappears. For colour relief, read back the colour at a cell of known elevation and confirm the colormap limits are the declared ones, not the autoscaled min/max of a tile that happened to contain a spike.

**Perceptual checks.** Run the Kovesi test strip through your colormap; simulate deuteranopia and protanopia on the finished figure; show the hillshade to a colleague and ask which way the valleys run — if the answer is wrong, the light is wrong. For 3D views, add a scale cube or known-height feature; viewers misjudge slope in exaggerated perspective by roughly the exaggeration factor.

**Omission checks — the main one.** A plan-view rendering omits the vertical, so it cannot show vertical offsets, misclassified bridge decks, or the systematic swath-edge curl of multibeam outer beams. Cross-sections (§57.7) are the remedy and should be a required step in any QC, with their locations recorded. A smoothed display copy omits features narrower than the kernel; a splat omits uncertainty entirely; a Terrain-RGB tile omits the datum. Make the omissions explicit in the caption.

> **Uncertainty budget.** Illustrative magnitudes of visual misreading, for a 1 m lidar DTM with σ_z = 0.05 m displayed at 1:5,000 (approximate; from the relations above and the cited perceptual studies).
>
> | Source | Effect | Magnitude |
> |---|---|---|
> | Horn gradient noise | Grain in low-altitude hillshade | σ_slope ≈ 1.2° per cell |
> | Gaussian display smoothing, σ = 1.5 cells | Loss of linear features | Features < 2–3 m wide suppressed; depths reduced > 80 % |
> | Rainbow colormap | False terraces at cyan/yellow | Spurious edges at ≈ 25 % and ≈ 60 % of range |
> | Undeclared vertical exaggeration 3× | Slope misjudged | Reader estimates slope ≈ 3× too steep |
> | South-east light | Relief inversion | Majority of naïve viewers invert valleys/ridges |
> | Terrain-RGB encoding | Quantization and lost datum | 0.1 m steps; geoid–ellipsoid offset of tens of m unflagged |
> | DoD autoscaled, no LoD mask | Noise read as change | All |Δh| < LoD (often 0.1–0.3 m) presented as signal |

**What to report.** With any evidentiary rendering: data source, version, epoch, vertical datum; technique and the five parameters of §57.2's rule; colormap name and limits; filter applied to the display copy, if any; masks (voids, LoD); vertical exaggeration; and the script that generates it. With any QC: the cross-section locations and what they showed.

## Software

**Open source:** GDAL (`gdaldem hillshade/slope/aspect/color-relief/TRI/TPI/roughness`, multidirectional and combined modes; caveat: no SVF/openness). QGIS (hillshade and blending in the renderer, "Multidirectional" option, contour and label engine; caveat: layer blending modes are not colour-managed). Relief Visualization Toolbox — RVT (`rvt-py` Python package and QGIS plugin; SVF, openness, LRM, RRIM-style blends, VAT; caveat: memory-hungry at large radii). WhiteboxTools (hillshade, multidirectional, time-in-daylight, horizon angle; caveat: single-threaded on some tools). SAGA GIS (SVF, openness, analytical hillshading with shadows). GRASS GIS (`r.relief`, `r.shade`, `r.skyview`, `r.horizon`). Blender with the BlenderGIS add-on (ray-traced relief with real shadows and global illumination; caveat: a rendering tool, not an analysis one — record camera and light). Potree and the COPC viewer (web point clouds with EDL). CloudCompare (EDL, slicing, per-attribute colouring). CesiumJS (3D Tiles, quantized-mesh; open core with commercial ion service), deck.gl `TerrainLayer`, MapLibre GL JS terrain, three.js. matplotlib with `cmcrameri` and `cmocean`; R `terra`/`rayshader` (ray-traced hillshade with ambient occlusion). nerfstudio and gsplat for NeRF/3DGS (research-grade; non-metric).

**Closed source:** Eduard (macOS; neural relief shading; paid licence). Color Oracle (free; colour-vision simulation).

**Commercial:** ArcGIS Pro (multidirectional hillshade, raster functions, 3D scenes; caveat: default 315°/45° in many templates). Global Mapper (shader library, 3D viewer). Surfer (contour and surface plots). Fledermaus (4D visualization for bathymetry, uncertainty surfaces from CUBE). Terragen and Natural Scene Designer (photoreal landscape rendering; artistic). Adobe Photoshop workflows (Patterson's shaded-relief techniques; non-reproducible by construction).

## Standards & guides

- IHO **S-4** *Regulations of the IHO for International (INT) Charts and Chart Specifications of the IHO*, ed. 4.9.0 (2021) — depth-tint conventions, isobath generalization, symbology for paper charts.
- IHO **S-52** *Specifications for Chart Content and Display Aspects of ECDIS*, ed. 6.1.1 (2015) with Presentation Library 4.0.x — depth-area colouring (two- and four-shade schemes), safety-contour display, day/dusk/night palettes.
- IHO **S-102** *Bathymetric Surface Product Specification*, ed. 3.0.0 (2024) — gridded bathymetry with uncertainty for ECDIS overlay.
- USGS **Topographic Map Symbols** and *US Topo Product Standard* — contour, index, supplementary, and depression-contour conventions.
- **ColorBrewer** (Harrower & Brewer 2003) and the **Scientific Colour Maps** user guide (Crameri) — palette selection guidance including colour-blind safety.
- **W3C WCAG 2.1** (2018) / 2.2 (2023) — contrast and non-text content requirements for web maps.
- **OGC 3D Tiles 1.1** Community Standard (2023) — LOD streaming of terrain and point clouds.
- ASPRS **LAS 1.4** specification — classification codes and attributes used for point-cloud colouring.

## Pitfalls

- **Hillshade lit from the south → relief inversion.** Why: matching imagery, or a default changed to "sun position." Detect: ask a naïve viewer which way valleys run; avoid: light from 300–345° or use SVF/openness, and caption any exception.
- **Rainbow or jet colormap → false terraces and colour-blind failure.** Why: software default, habit. Detect: plot $L^*$ vs value; simulate deuteranopia. Avoid: viridis/batlow/cmocean; diverging maps only for signed data.
- **Undeclared vertical exaggeration.** Why: low-relief terrain "looks flat." Detect: compare measured slopes with visual impression. Avoid: declare $z_f$ in caption and frame.
- **Smoothing for display, then analysing the smoothed grid.** Why: the smoothed file is the one that looks right and gets reused. Detect: file lineage; slope histograms missing high values. Avoid: name display copies explicitly; never feed them to hydrology, volume, or slope analyses.
- **Splat or NeRF renderings mistaken for survey data.** Why: they look better than the point cloud. Detect: no uncertainty, no classification, no checkpoint residuals. Avoid: label as visualization; deliver a validated cloud/DEM alongside.
- **QC in plan view only.** Why: viewers open in 2D. Detect: strip offsets found later by the client. Avoid: mandatory cross-sections across overlaps, water edges, and bridges.
- **DoD autoscaled to its min/max with no LoD mask.** Why: default renderer. Detect: asymmetric colour bar; "change" everywhere. Avoid: symmetric limits, zero-centred diverging map, grey below LoD.
- **Colormap zero not at the data's vertical datum.** Why: land–sea colormaps assume 0 = coast. Detect: coastline rendered inland or offshore. Avoid: set the colormap pivot explicitly to the datum's zero after any datum transformation.
- **Terrain-RGB tiles with unknown datum.** Why: encoding carries no metadata. Detect: 20–40 m offset against GNSS near coasts. Avoid: document the datum in the tile service metadata; transform to the viewer's globe datum before encoding.
- **SVF/openness radius unreported.** Why: tools default to 10 cells. Detect: features of a given size appear or vanish between figures. Avoid: report radius in cells and metres.

## Key takeaways

- Visualization is an analysis step with parameters; record technique, azimuth, altitude, exaggeration, and radius with every evidentiary image, and script the figure.
- Use the Horn gradient knowingly: it is a 3 × 3 smoothing filter, and its noise scales as $\sigma_z/\Delta x$.
- Light from the north-west or use direction-independent techniques (SVF, openness, LRM, RRIM); check for relief inversion whenever you deviate.
- Choose perceptually uniform, lightness-monotonic, colour-blind-safe colormaps; never the rainbow for a scalar field; symmetric zero-centred diverging maps for change, with the sub-LoD band masked.
- Keep display filtering on a named copy; never analyse the smoothed grid.
- Cross-sections through point clouds are the primary QC view; plan-view renderings cannot show vertical offsets.
- Web 3D terrain and RGB-encoded tiles strip datum and units — restore them in metadata before anyone measures.
- Splats and NeRFs are visualization products: beautiful, non-metric, without uncertainty; use them for engagement, not measurement.
- Show uncertainty (hatching, bands, ensembles) and time (swipes, multi-epoch animation), not just a crisp surface.

## References

- Bernabé-Poveda, M. A., & Çöltekin, A. (2015). Prevalence of the terrain reversal effect in satellite imagery. *International Journal of Digital Earth*, 8(8), 640–655.
- Borland, D., & Taylor, R. M. (2007). Rainbow color map (still) considered harmful. *IEEE Computer Graphics and Applications*, 27(2), 14–17.
- Boucheny, C. (2009). *Visualisation scientifique de grands volumes de données: pour une approche perceptive*. PhD thesis, Université Joseph Fourier, Grenoble.
- Chiba, T., Kaneta, S., & Suzuki, Y. (2008). Red Relief Image Map: new visualization method for three dimensional data. *International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences*, XXXVII(B2), 1071–1076.
- Crameri, F., Shephard, G. E., & Heron, P. J. (2020). The misuse of colour in science communication. *Nature Communications*, 11, 5444. https://doi.org/10.1038/s41467-020-19160-7
- Doneus, M. (2013). Openness as visualization technique for interpretative mapping of airborne lidar derived digital terrain models. *Remote Sensing*, 5(12), 6427–6442.
- Harrower, M., & Brewer, C. A. (2003). ColorBrewer.org: an online tool for selecting colour schemes for maps. *The Cartographic Journal*, 40(1), 27–37.
- Hesse, R. (2010). LiDAR-derived Local Relief Models — a new tool for archaeological prospection. *Archaeological Prospection*, 17(2), 67–72.
- Horn, B. K. P. (1981). Hill shading and the reflectance map. *Proceedings of the IEEE*, 69(1), 14–47.
- Imhof, E. (1982). *Cartographic Relief Presentation* (H. J. Steward, Ed.). Berlin: Walter de Gruyter. (Original *Kartographische Geländedarstellung*, 1965.)
- Jenny, B., Heitzler, M., Singh, D., Farmakis-Serebryakova, M., Liu, J. C., & Hurni, L. (2021). Cartographic relief shading with neural networks. *IEEE Transactions on Visualization and Computer Graphics*, 27(2), 1151–1160.
- Kennelly, P. J., & Stewart, A. J. (2014). General sky models for illuminating terrains. *International Journal of Geographical Information Science*, 28(2), 383–406.
- Kerbl, B., Kopanas, G., Leimkühler, T., & Drettakis, G. (2023). 3D Gaussian Splatting for real-time radiance field rendering. *ACM Transactions on Graphics*, 42(4), article 139.
- Kokalj, Ž., & Hesse, R. (2017). *Airborne Laser Scanning Raster Data Visualization: A Guide to Good Practice*. Prostor, kraj, čas 14. Ljubljana: Založba ZRC.
- Kokalj, Ž., & Somrak, M. (2019). Why not a single image? Combining visualizations to facilitate fieldwork and on-screen mapping. *Remote Sensing*, 11(7), 747.
- Kovesi, P. (2015). Good colour maps: how to design them. arXiv:1509.03700.
- MacEachren, A. M., Robinson, A., Hopper, S., Gardner, S., Murray, R., Gahegan, M., & Hetzler, E. (2005). Visualizing geospatial information uncertainty: what we know and what we need to know. *Cartography and Geographic Information Science*, 32(3), 139–160.
- MacEachren, A. M., Roth, R. E., O'Brien, J., Li, B., Swingley, D., & Gahegan, M. (2012). Visual semiotics & uncertainty visualization: an empirical study. *IEEE Transactions on Visualization and Computer Graphics*, 18(12), 2496–2505.
- Mark, R. K. (1992). *Multidirectional, oblique-weighted, shaded-relief image of the Island of Hawaii*. USGS Open-File Report 92-422.
- Marston, B. E., & Jenny, B. (2015). Improving the representation of major landforms in analytical relief shading. *International Journal of Geographical Information Science*, 29(7), 1144–1165.
- Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R., & Ng, R. (2020). NeRF: representing scenes as neural radiance fields for view synthesis. *Proceedings of ECCV 2020*, LNCS 12346, 405–421.
- Nuñez, J. R., Anderton, C. R., & Renslow, R. S. (2018). Optimizing colormaps with consideration for color vision deficiency to enable accurate interpretation of scientific data. *PLoS ONE*, 13(7), e0199239.
- Patterson, T., & Jenny, B. (2011). The development and rationale of cross-blended hypsometric tints. *Cartographic Perspectives*, 69, 31–46.
- Pingel, T. J., & Clarke, K. C. (2014). Perceptually shaded slope maps for the visualization of digital surface models. *The Cartographic Journal*, 51(4), 281–293.
- Schütz, M. (2016). *Potree: Rendering Large Point Clouds in Web Browsers*. Diploma thesis, Technische Universität Wien.
- Thyng, K. M., Greene, C. A., Hetland, R. D., Zimmerle, H. M., & DiMarco, S. F. (2016). True colors of oceanography: guidelines for effective and accurate colormap selection. *Oceanography*, 29(3), 9–13.
- Yoëli, P. (1965). Analytical hill shading. *Surveying and Mapping*, 25(4), 573–579.
- Yokoyama, R., Shirasawa, M., & Pike, R. J. (2002). Visualizing topography by openness: a new application of image processing to digital elevation models. *Photogrammetric Engineering & Remote Sensing*, 68(3), 257–265.
- Zakšek, K., Oštir, K., & Kokalj, Ž. (2011). Sky-View Factor as a relief visualization technique. *Remote Sensing*, 3(2), 398–415. https://doi.org/10.3390/rs3020398
- Zevenbergen, L. W., & Thorne, C. R. (1987). Quantitative analysis of land surface topography. *Earth Surface Processes and Landforms*, 12(1), 47–56.

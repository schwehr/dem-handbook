# Chapter 17 — Measurement physics: a unified view (ranging, parallax, interferometry, inversion)

> **Part V — Sensors and platforms.** Having placed the sensors on their platforms in [Chapter 16](ch16-platforms.md), this chapter reduces every elevation instrument in the book to a handful of physical principles, so that the sensor-specific chapters that follow ([Chapter 18](ch18-topographic-lidar.md) to [Chapter 24](ch24-gravity-magnetics-geophysics.md)) can be read as variations on five themes.

**In this chapter.** Every elevation sensor does one of five things: it times a signal there and back, it triangulates from two viewpoints, it compares the phase of two signals, it inverts a brightness into a depth or a slope, or it inverts a potential field into a mass distribution. You will be able to derive the basic range, parallax, and interferometric height equations, state the propagation speed and the refraction law for light and sound in air and water, compute a sensor footprint from range and beamwidth and explain why that makes the sensor a low-pass filter, and — most importantly — say *which surface* each sensor measures: first or last return, phase centre, scattering centre within snow or canopy, water surface or bottom. You will be able to use the sensor–material interaction matrix to predict where a sensor returns nothing, returns the wrong surface, or returns the right surface with a bias, and you will understand noise and detection thresholds as the physical origin of the outliers that every later chapter has to clean.

## 17.1 Ranging

**Ranging** measures distance from the time a signal takes to travel to the surface and back. For a pulse emitted at $t_0$ and received at $t_1$,

$$R = \frac{v\,(t_1 - t_0)}{2},$$

where $v$ is the propagation speed in the medium. The factor of two is the two-way path; the "2" is also the first source of error, because it assumes the same speed out and back along the same path. Three implementations dominate.

**Pulsed time-of-flight** emits a short pulse (lidar: 1–10 ns, so 0.3–3 m long in air; sonar: 0.1–10 ms, so 0.15–15 m long in water) and detects the return by threshold, constant-fraction discrimination, or waveform fitting. Range precision is set by the pulse rise time, the signal-to-noise ratio, and the timing clock: a 1 ns timing error is 15 cm of range in air. Modern topographic lidars reach 1–2 cm range precision on hard targets by averaging over the pulse and by waveform processing; multibeam sonars reach a few centimetres at short range by phase detection (Section 17.3 and [Chapter 20](ch20-sonar.md)).

**Phase-shift ranging** modulates a continuous wave at frequency $f_m$ and measures the phase difference $\Delta\phi$ between emitted and received modulation: $R = \frac{v}{2}\left(\frac{\Delta\phi}{2\pi f_m} + \frac{k}{f_m}\right)$ for integer $k$. The range is ambiguous modulo $v/(2 f_m)$, so instruments use several modulation frequencies to resolve $k$ (total stations, phase-based terrestrial scanners). Phase scanners give millimetre precision at short range but produce "mixed pixel" artefacts at edges and have no multi-return capability.

**FMCW** (frequency-modulated continuous wave) sweeps the carrier linearly over bandwidth $B$ in time $T$ and mixes the return with the transmitted signal; the beat frequency $f_b = \frac{2R}{v}\frac{B}{T}$ gives range, and the range resolution is $\Delta R = v/(2B)$ — a 1 GHz sweep gives 15 cm in air. FMCW is the basis of radar altimeters, coherent "4D" automotive lidar, and chirp sonars and sub-bottom profilers (where pulse compression achieves the same resolution gain, [Chapter 20](ch20-sonar.md)).

The propagation speed differs by five orders of magnitude between media. Light in vacuum travels at $c = 299{,}792{,}458$ m/s exactly; in air the group refractive index at near-infrared wavelengths is about 1.00027–1.00030, so the range correction is roughly 0.3 mm per metre — negligible in airborne lidar at the 1 cm level but applied in geodetic laser ranging and over 1 km terrestrial ranges. In water the refractive index at 532 nm is approximately 1.34 (seawater; 1.33 for fresh water), so light travels 25 % slower and an uncorrected two-way time overstates depth by a third of the true depth. Sound in seawater travels at about 1,450–1,550 m/s (nominal 1,500 m/s) and depends on temperature (≈ +4 m/s per °C near 10 °C), salinity (≈ +1.3 m/s per PSU), and pressure (≈ +1.7 m/s per 100 m depth); a 1 % error in the assumed speed is a 1 % error in every depth, and the depth-dependent profile bends every oblique ray (Section 17.9 and the Mathematics section). The practical consequence is that a lidar's range error is dominated by timing and the target, while a sonar's range error is dominated by the medium.

**Refraction** enters whenever the ray crosses a gradient or an interface. The air–water interface bends a bathymetric lidar pulse by Snell's law, $n_a \sin\theta_a = n_w \sin\theta_w$, which at 20° incidence turns a 20° air angle into a 14.9° water angle; failing to apply it produces depth errors of several percent and horizontal displacements of decimetres to metres ([Chapter 19](ch19-bathymetric-lidar.md)). Sound-speed gradients bend sonar beams continuously, which is why multibeam processing traces rays through a measured profile rather than using a straight line ([Chapter 20](ch20-sonar.md)). The atmosphere bends terrestrial laser lines of sight by amounts that matter at kilometre ranges (the coefficient of refraction $k \approx 0.13$ in the classic levelling correction) and delays GNSS and radar signals by metres ([Chapter 12](ch12-gnss.md), [Chapter 21](ch21-radar-sar-insar.md)).

## 17.2 Parallax and triangulation

**Triangulation** measures the angle to a point from two ends of a known baseline and solves the triangle. In **stereo photogrammetry** the baseline is the distance $B$ between two camera stations, the angles are encoded as image coordinates, and for the normal case (parallel optical axes, focal length $f$) the depth is

$$Z = \frac{f\,B}{p},$$

where $p$ is the **parallax** (disparity) — the difference in image x-coordinate of the same point in the two images. Differentiating, $\sigma_Z = \frac{Z^2}{f B}\,\sigma_p = \frac{Z}{B}\cdot\frac{Z}{f}\,\sigma_p$: height precision degrades with the *square* of the distance and improves with the base-to-height ratio $B/Z$ and the matching precision $\sigma_p$ (typically 0.1–0.3 pixel for good texture). A drone block at $Z = 100$ m with $f = 8{,}000$ pixels (a 24 mm lens on a 3 µm pixel), $B = 30$ m, and $\sigma_p = 0.3$ px gives $\sigma_Z = (100^2 / (8000 \times 30)) \times 0.3 = 1.25$ cm; a satellite pair at 700 km with a 30° convergence angle and 0.5 m pixels gives metres. The surface measured is whatever both cameras can see and match: the top of the canopy, the roof, the water surface if it has texture (usually it does not), and nothing in shadow or in featureless snow.

**Structured light** replaces the second camera with a projector of known pattern, and **laser triangulation** (line scanners, underwater laser-line systems on ROVs) replaces it with a laser sheet; the geometry is the same, with the projector's pattern providing the correspondence that image matching would otherwise have to find. Both give sub-millimetre precision at ranges of centimetres to metres and fail beyond a few metres because the base-to-height ratio collapses. Depth cameras on phones and robots and underwater micro-bathymetry systems belong here. In all triangulation systems the measured quantity is an angle, so the error budget is dominated by the camera model (interior orientation, distortion) and by the baseline knowledge, not by any clock ([Chapter 22](ch22-photogrammetry-sfm.md)).

## 17.3 Interferometry

**Interferometry** compares the phase of a coherent signal received at two points (or at one point at two times) and converts the phase difference into a path-length difference and then into an angle or a height. The phase difference $\Delta\phi = \frac{2\pi}{\lambda}\,\Delta R$ is measured modulo $2\pi$, so the raw observable is ambiguous and must be **unwrapped** — the central difficulty of every interferometric system.

In **InSAR** two antennas separated by a baseline $B$ (on one platform, as in SRTM and TanDEM-X, or on two passes of one satellite) observe the same ground with slightly different look angles, and the interferometric phase, after removing the flat-Earth term, is proportional to terrain height. The sensitivity is expressed as the **height of ambiguity** $h_a$ — the height change that produces one full $2\pi$ fringe:

$$h_a = \frac{\lambda\,R\,\sin\theta}{p\,B_\perp},$$

with $R$ the slant range, $\theta$ the incidence angle, $B_\perp$ the baseline component perpendicular to the look direction, and $p = 1$ for single-pass (bistatic) and $p = 2$ for repeat-pass (monostatic) geometry. A small $h_a$ (long baseline) gives fine height sensitivity but dense fringes that are hard to unwrap and decorrelate on steep terrain; a large $h_a$ gives robust unwrapping but coarse heights. TanDEM-X acquired its global DEM with $h_a$ of roughly 30–50 m in the first coverage and smaller values later, so that phase noise of a few degrees translated into height noise of a metre or two ([Chapter 21](ch21-radar-sar-insar.md)). The surface measured is the **phase centre** of the scattering volume within the resolution cell — which in forest is somewhere inside the canopy and in dry snow is metres below the surface (Section 17.7).

**Phase-differencing (interferometric) sonar** applies the same principle across the swath instead of along the baseline: two or more receiver staves separated by $d$ measure the phase difference of the bottom echo, $\Delta\phi = \frac{2\pi d \sin\theta}{\lambda}$, which gives the arrival angle $\theta$ for each time sample and hence a depth profile ([Chapter 20](ch20-sonar.md)). Multibeam sonars also use phase in their outer beams: the **split-aperture** bottom detector finds the instant at which the phase difference between two half-arrays crosses zero, which is a far sharper time estimate than the amplitude peak of a long, smeared outer-beam echo.

<!-- figure: Figure 17.1 — Four panels on a common scale: (a) pulsed ranging with two-way time; (b) stereo parallax geometry showing Z = fB/p; (c) InSAR geometry with baseline, look angle, and the height-of-ambiguity fringe; (d) phase-differencing sonar with two staves and arrival angle from phase difference. -->

## 17.4 Radiometric inversion

The fourth family does not measure geometry at all; it measures **brightness** and inverts a physical model to get a depth or a slope. The inversions are only as good as the model and must be calibrated against geometric measurements.

**Satellite-derived bathymetry (SDB)** from passive optical imagery uses the fact that water attenuates light exponentially with depth and more strongly at red than at blue–green wavelengths. In the simplest single-band model (Lyzenga 1978) the bottom-reflected radiance above the water is $L = L_\infty + (L_b - L_\infty)\,e^{-2 K_d z}$, where $L_\infty$ is the deep-water radiance, $L_b$ the radiance over the bottom at zero depth, $K_d$ the diffuse attenuation coefficient, and $z$ the depth; taking logarithms linearises depth against $\ln(L - L_\infty)$. The band-ratio form (Stumpf et al. 2003) uses $\ln(nR_{\text{blue}})/\ln(nR_{\text{green}})$ to cancel much of the bottom-albedo dependence. Either way the inversion needs calibration depths, holds for one water type and one bottom type at a time, and degrades beyond about one Secchi depth or where the bottom is dark or the water turbid ([Chapter 23](ch23-satellite-derived-bathymetry.md)). The surface it measures is the bottom as weighted by the water-leaving radiance model — not a point, but a water-column-averaged, albedo-dependent estimate.

**Shape-from-shading and photoclinometry** invert the brightness of a surface under known illumination into its slope, using a reflectance model (Lambertian, Minnaert, Hapke), and then integrate slopes into heights. The method is a workhorse of planetary mapping where stereo coverage is sparse ([Chapter 67](ch67-planetary-dems.md)) and is sensitive to albedo variations (which masquerade as slopes), to the accuracy of the reflectance model, and to the integration constant (it gives relative, not absolute, heights). **Shadow-length heights** use the simplest inversion of all: an object casting a shadow of length $L$ under solar elevation $\alpha$ has height $h = L\tan\alpha$; the method dates to the earliest aerial-photo interpretation and still measures building heights, crater rims, and ice-cliff faces from single images, with errors dominated by locating the shadow tip and by the assumption of flat ground beneath the shadow.

> **Definitions that bite.** "Depth" from SDB, from a lidar bottom return, and from a multibeam sounding are three physically different quantities at the same location: a radiance-weighted estimate of the bottom under the water-type and albedo assumptions of the inversion; the refracted range to the strongest green-laser bottom return within a footprint of 1–3 m; and the acoustic arrival from the ensonified footprint, which may be the top of soft sediment or some centimetres into it depending on frequency. Differences of 0.2–0.5 m among them in 10 m of water are physics, not error, and should be discussed before being minimised.

## 17.5 Potential-field inversion

The fifth family measures a potential field — gravity, or less often magnetics — and infers topography from it. Satellite radar altimetry measures the sea-surface height, which closely follows the geoid; short-wavelength geoid undulations are produced by seafloor relief through the density contrast between rock (≈ 2,700 kg/m³) and water (≈ 1,030 kg/m³). Smith & Sandwell (1994, 1997) showed that in the band of about 15–160 km wavelength — neither attenuated by upward continuation through the water column nor cancelled by isostatic compensation — gravity and bathymetry are related by a nearly linear transfer function calibrated with ship soundings. The resulting **altimetry-predicted bathymetry** fills most of the GEBCO grid away from ship tracks at a horizontal resolution of roughly 6–12 km with depth errors of 100–200 m typical, worse in sedimented basins ([Chapter 23](ch23-satellite-derived-bathymetry.md), [Chapter 24](ch24-gravity-magnetics-geophysics.md)). Under ice sheets the same inversion, with airborne gravity and radar-sounded control, fills gaps between radar lines. The measured "surface" is a density interface smoothed by the upward-continuation operator — every seamount narrower than the resolution is absent by construction, which matters for anyone who takes a GEBCO grid as a seabed.

## 17.6 Footprint, beamwidth, divergence, and the sensor as a low-pass filter

No sensor measures a point. A laser beam diverges, an acoustic beam has an angular width, a camera pixel subtends a solid angle, and the measurement is an average over the patch where that cone meets the surface. For a beam of full angular width $\theta$ (laser divergence, or sonar beamwidth between the −3 dB points) at range $R$ along the beam axis, the **footprint** diameter is

$$D \approx R\,\theta \quad(\theta \text{ in radians, small-angle}),$$

growing to $D \approx R\,\theta / \cos\phi$ across the swath at incidence angle $\phi$ on a flat surface, and more on slopes facing away. An airborne lidar with 0.25 mrad divergence at 1,500 m has a 0.38 m footprint; ICESat-2 at 500 km altitude with a 17 µrad beam has about 11 m; a 1° multibeam at 4,000 m depth has 70 m at nadir and about 280 m across-track at 60° (where the across-track dimension grows as $1/\cos^2\phi$, [Chapter 20](ch20-sonar.md)); a 25 m GEDI footprint; a 30 m SRTM resolution cell. The returned signal is the convolution of the surface with the beam's energy pattern (roughly Gaussian for lasers, a $\text{sinc}^2$-like main lobe with sidelobes for sonar arrays), so **the sensor is a spatial low-pass filter** whose cutoff is set by the footprint — any relief at wavelengths shorter than about twice the footprint is attenuated, and the range reported for the footprint is a weighted average biased toward the nearest or the brightest part of the patch depending on the detector. Footprint, not point spacing, is therefore the physical **effective resolution** floor of a DEM; sampling more densely than the footprint oversamples a smoothed surface ([Chapter 44](ch44-resolution-and-sampling.md)). On a slope of gradient $s$ the footprint alone spreads the return over a range interval $D\,s$: a 70 m deep-water sonar footprint on a 10° slope has 12 m of relief inside it, which sets a hard floor on depth precision regardless of the electronics.

> **Rule of thumb.** Grid a DEM no finer than the footprint of the sensor that made it, and expect its effective resolution to be 2–3 times the footprint in the presence of noise. For a multibeam the footprint is about $d\,\theta$ at depth $d$ (1° ≈ 1.7 % of depth); for airborne lidar it is roughly 0.2–0.5 m from typical flying heights; for optical stereo it is 3–5 pixels because matching windows average over that many. The rule fails for interferometric and FMCW systems, where resolution comes from bandwidth and phase rather than beamwidth, and for SAS, where synthetic-aperture processing makes the along-track resolution independent of range.

## 17.7 Which surface did we measure?

The question that distinguishes a careful DEM user from a careless one is not "how accurate is this?" but "what surface is this?" Each sensor class answers differently.

**Lidar returns.** A laser pulse that is 1–3 m long in air can produce several returns from one footprint when it hits canopy, wires, or building edges. The **first return** is the highest object that reflected enough energy; the **last return** is the lowest — which is the ground only if a gap let the pulse through, and is otherwise a branch or the understorey. Full-waveform systems record the whole echo and can detect weaker, later returns than discrete systems; single-photon systems detect individual photons and need statistical processing to separate signal from noise. The "ground" in a lidar DTM is therefore a *classification* of last returns, not a measurement of the ground ([Chapter 18](ch18-topographic-lidar.md), [Chapter 30](ch30-point-cloud-classification.md)).

**Radar scattering centres by wavelength.** A radar wave penetrates a medium to a depth that scales with wavelength and inversely with the medium's loss. In vegetation, X-band (3 cm) scatters mostly from the upper canopy, C-band (5.6 cm) somewhat deeper, L-band (24 cm) from branches and trunks with significant ground contribution, and P-band (70 cm) largely from trunks and ground — so an X-band InSAR DEM of a forest is a near-canopy-top DSM, and a P-band one is closer to the ground. In **dry snow and firn** the penetration is dramatic: TanDEM-X X-band phase centres over the Greenland and Antarctic interiors sit several metres below the surface (Rizzoli et al. 2017 report elevation biases of several metres, up to about 10 m in the dry-snow zone) and C-band SRTM-era products show similar biases on glaciers, which matters enormously when two DEMs from different seasons or wavelengths are differenced to estimate mass change ([Chapter 21](ch21-radar-sar-insar.md), [Chapter 41](ch41-change-detection.md)). In **dry sand** L-band penetrates metres, as the Shuttle Imaging Radar discovery of buried palaeo-drainage in the Sahara showed (McCauley et al. 1982). In wet media penetration collapses to centimetres.

**Optical penetration of water.** Pure water's absorption coefficient is near its minimum (about 0.005 m⁻¹ at 420 nm; Pope & Fry 1997) in the blue–green around 420–530 nm — natural waters are 0.02–0.1 m⁻¹ or more — and rises by about three orders of magnitude by 1,064 nm (roughly 10 m⁻¹ and above). A 1,064 nm topographic lidar pulse therefore dies within centimetres of the water surface — most of the time it returns from the surface or not at all, producing the voids over water in every NIR lidar dataset — while a 532 nm bathymetric lidar pulse survives a two-way path of tens of metres in clear water ([Chapter 19](ch19-bathymetric-lidar.md)). Passive optical sensors see the bottom through the same window and lose it beyond about one Secchi depth.

**Bottom detection in sonar.** At 200–400 kHz the acoustic wavelength is 4–8 mm and the echo comes from the sediment–water interface or within the top few centimetres; at 12 kHz (12 cm wavelength) the first strong return may still be the interface but the footprint is tens of metres and the detection is a statistical centroid of a long echo. Dual-frequency single-beams (e.g. 38/200 kHz) exploit exactly this: the high frequency reads the top of fluid mud, the low frequency reads the consolidated bottom beneath it, and the two depths can differ by a metre in a dredged channel — a difference that is a definition of "bottom," not an error ([Chapter 20](ch20-sonar.md), [Chapter 4](ch04-names-and-definitions.md)).

**Stereo and SfM** measure the visible textured surface — canopy top, roof, snow surface where it has shadows — and nothing where it is uniform or under closed canopy. **Altimetry** over ice measures the surface or, for some radar altimeters in dry snow, a point within the top metres. When two DEMs disagree, the first hypothesis should be that they measured different surfaces, and the second that one is wrong.

## 17.8 The sensor–material interaction matrix

The following matrix summarises, for the main sensor classes, what each returns from each common material. "Surface" means the physical surface is measured; "bias" means a measurement is returned but systematically displaced; "void" means no usable measurement.

| Material | NIR lidar (1,064 nm) | Green lidar (532 nm) | X/C-band InSAR | L/P-band InSAR | Optical stereo / SfM | MBES (200–400 kHz) | MBES (12–30 kHz) |
|---|---|---|---|---|---|---|---|
| Bare rock, soil | surface | surface | surface | surface | surface | — | — |
| Dense vegetation | canopy + some ground (last returns) | canopy + some ground | canopy top (bias above ground 5–30 m) | partial penetration; bias of metres | canopy top; no ground | — | — |
| Clear shallow water | surface or void; no bottom | surface and bottom to ~1.5–3 Secchi depths | surface (specular → low return) | surface | bottom to ~1 Secchi (SDB) if textured | bottom (cm) | bottom (footprint-limited) |
| Turbid water | surface or void | surface; bottom to < 1 Secchi depth | surface | surface | surface/none | bottom (cm); fluid mud ambiguity | bottom beneath fluid mud |
| Dry snow / firn | surface | surface | bias: phase centre metres below surface | bias: deeper still | surface if textured; void on uniform snow | — | — |
| Wet snow / ice | surface | surface | near-surface | near-surface | surface | — | — |
| Clouds, fog | void (blocked) or false returns | void | transparent | transparent | void | — | — |
| Smoke, steam | partial; false returns, attenuation | partial | transparent | transparent | void or bias | — | — |
| Glass, water-smooth surfaces | specular → void or multi-path ghosts | same | specular → dark | specular → dark | reflections → false matches | — | — |
| Soft mud seabed | — | surface of mud at 532 nm (weak) | — | — | — | top of mud | within/below mud |

The matrix is a prediction tool. Before merging a lidar DTM with an InSAR DEM over a glacier, read the "dry snow" row and expect a multi-metre offset that is not an error of either product; before promising a bathymetric lidar survey of an estuary, read the "turbid water" column; before using SfM to monitor a snowfield, note the "void on uniform snow" cell ([Chapter 36](ch36-seasonal-variability.md), [Chapter 48](ch48-compositing.md)).

<!-- figure: Figure 17.2 — Vertical cross-section through forest, a lake, a snow-covered glacier, and a muddy estuary, with the "measured surface" of each sensor class drawn as a coloured line: NIR lidar first/last return, green lidar, X-band and L/P-band phase centres, optical stereo, 200 kHz and 12 kHz sonar bottom detections. -->

## 17.9 Noise, detection thresholds, and false alarms as the origin of outliers

Every ranging and interferometric sensor makes a **detection decision**: is this sample a return from the surface, or noise? The decision is a threshold on a signal in the presence of noise — photon shot noise and solar background for lidar, thermal and ambient noise and reverberation for sonar, speckle and thermal noise for radar — and it has two failure modes with fixed names. A **missed detection** occurs when a real return falls below threshold: dark asphalt, wet surfaces, or steep slopes for lidar; soft sediment or steep slopes at the outer beams for sonar. The result is a void or, worse, detection of a later, weaker echo (the understorey, a sidelobe) in place of the missing one. A **false alarm** occurs when noise crosses threshold: a solar photon in ICESat-2 data, a bubble or a fish in the water column, a sidelobe echo of a strong nadir return, a cloud or a bird for airborne lidar. False alarms produce the isolated high and low points — "fliers," "spikes" — that every cleaning workflow removes ([Chapter 30](ch30-point-cloud-classification.md)).

The Neyman–Pearson framework makes the trade-off explicit: lowering the threshold recovers weak real returns at the cost of more false alarms, and the operator or the designer chooses a false-alarm rate. Constant-false-alarm-rate (CFAR) detectors adapt the threshold to the local noise. Photon-counting lidars push this to the limit — ATLAS on ICESat-2 detects single photons with background rates of several MHz in daylight, and the ground is found by density-based filtering of the photon cloud (ATL03 → ATL08), not by a per-pulse threshold ([Chapter 18](ch18-topographic-lidar.md)). The statistical nature of detection is why the error distributions of DEMs have heavy tails: the Gaussian core comes from timing and trajectory noise, but the tails come from detection errors that are not Gaussian at all, and robust statistics (median, NMAD, percentiles) are needed to describe them ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 53](ch53-accuracy-assessment.md)). A validation report that states only an RMSE has assumed away the physics of this section.

## Then & now

The five principles are old; the instruments are new. Triangulation is Thales and Snellius; the stereo plotter is Pulfrich's 1901 stereocomparator and the analogue instruments of the 1920s. Ranging by sound began with Fessenden's oscillator after the 1912 Titanic sinking and the echo sounders of the 1920s ([Chapter 20](ch20-sonar.md)); ranging by light waited for the laser in 1960 and the first lidar experiments in 1961 ⟨H⟩, airborne profiling in the 1960s–1980s, and scanning systems in the mid-1990s. Radar interferometry for topography was demonstrated by Graham in 1974 and made routine by ERS-1 in the 1990s and SRTM in 2000; phase-differencing sonar arrived in the 1980s–1990s. Radiometric bathymetry from Landsat (Lyzenga 1978) and gravity-predicted bathymetry from Geosat (Smith & Sandwell 1994) made the inversion families operational in the same decades. What has changed since is less the physics than the detection: waveform digitisers, single-photon detectors, multi-sector FM multibeams, and bistatic satellite formations have pushed each principle to its noise floor, and the resulting error distributions are now understood to be heavy-tailed in ways the early Gaussian budgets did not allow.

## Mathematics

**Two-way travel time and its sensitivity.** From $R = v\,\tau/2$ with $\tau$ the round-trip time, the differential is $dR = \frac{\tau}{2}\,dv + \frac{v}{2}\,d\tau$, i.e. $\frac{dR}{R} = \frac{dv}{v} + \frac{d\tau}{\tau}$. The speed term is a *scale* error — proportional to range — while the timing term is an additive offset for a fixed clock error. For sonar in 100 m of water, a 5 m/s (0.33 %) error in the harmonic mean sound speed is 0.33 m; for lidar at 1,500 m a 1 ns timing error is 0.15 m regardless of range.

**Snell's law and the two refractions.** At a plane interface, $n_1 \sin\theta_1 = n_2 \sin\theta_2$. For air ($n_a \approx 1.000$) to seawater at 532 nm ($n_w \approx 1.34$; Quan & Fry 1995 give the dependence on temperature, salinity, and wavelength) and an air incidence angle of 20°, $\sin\theta_w = \sin 20°/1.34 = 0.2552$, $\theta_w = 14.79°$. Light in water travels at $c/n_w$, so a measured in-water two-way time $\tau_w$ corresponds to slant distance $s = c\,\tau_w/(2 n_w)$, and the depth below the surface is $z = s\cos\theta_w$, with horizontal offset $s\sin\theta_w$. Ignoring refraction entirely (using $n = 1$ and $\theta_a$) overstates the slant distance by 34 % and understates $\cos\theta$: for $z = 10$ m the uncorrected depth would be $1.34 \times 10 / \cos 14.79° \times \cos 20° = 13.02$ m, an error of 3 m ([Chapter 19](ch19-bathymetric-lidar.md) gives the full correction including surface slope).

For sound in a stratified ocean the same law applies continuously. Snell's constant along a ray is $\dfrac{\sin\theta(z)}{c(z)} = \text{const}$, so a ray launched at $\theta_0$ where the speed is $c_0$ has $\sin\theta(z) = \sin\theta_0\,c(z)/c_0$: it bends toward the horizontal where the speed increases and toward the vertical where it decreases. In a layer with constant gradient $g = dc/dz$ the ray is a circular arc of radius $\rho = c_0/(g\sin\theta_0)$; for $g = -0.05$ s⁻¹ (a thermocline), $c_0 = 1{,}500$ m/s, $\theta_0 = 60°$, $|\rho| = 34.6$ km — a gentle curve whose integrated effect over a 100 m path is a few decimetres of depth error at the outer beam if the gradient is not modelled ([Chapter 20](ch20-sonar.md) gives the layer-by-layer ray-trace equations).

**Beam footprint.** For a Gaussian laser beam with $1/e^2$ full divergence $\theta$ the footprint diameter at range $R$ is $D = R\theta$ (plus the exit aperture, negligible beyond a few hundred metres). For a line array of length $L$ at wavelength $\lambda$ the −3 dB beamwidth is $\theta_{-3\,\text{dB}} \approx 0.88\,\lambda/L$ radians (unshaded; wider with shading): a 0.5 m array at 300 kHz ($\lambda = 5$ mm) gives 0.5°. On a flat bottom at depth $d$ and beam angle $\phi$ the across-track footprint is $d\,\theta/\cos^2\phi$ and the along-track footprint $d\,\theta/\cos\phi$.

**InSAR height of ambiguity.** From the interferometric phase $\phi = -\frac{2\pi p}{\lambda}(R_1 - R_2)$ and the geometry $\partial\phi/\partial h = -\frac{2\pi p\,B_\perp}{\lambda R\sin\theta}$, one fringe ($2\pi$) corresponds to $h_a = \frac{\lambda R\sin\theta}{p\,B_\perp}$. For a TanDEM-X-like single-pass case ($p = 1$, $\lambda = 3.1$ cm, $R = 600$ km, $\theta = 35°$, $B_\perp = 250$ m), $h_a = 0.031 \times 600{,}000 \times 0.574 / 250 = 42.7$ m; a phase standard deviation of 10° then gives height noise of $42.7 \times 10/360 = 1.2$ m before multilooking. For a repeat-pass Sentinel-1 pair ($p = 2$, $\lambda = 5.55$ cm, $R = 850$ km, $\theta = 39°$, $B_\perp = 100$ m), $h_a = 0.0555 \times 850{,}000 \times 0.629 / 200 = 148$ m — which is why Sentinel-1 is a deformation instrument, not a DEM instrument ([Chapter 21](ch21-radar-sar-insar.md)).

**Nyquist preview.** A surface sampled at spacing $\Delta$ represents wavelengths no shorter than $2\Delta$, and a sensor with footprint $D$ attenuates wavelengths shorter than about $2D$: sampling at $\Delta < D/2$ gains nothing, and sampling at $\Delta > D$ aliases relief between $D$ and $2\Delta$ into the grid ([Chapter 44](ch44-resolution-and-sampling.md)).

## Validation & uncertainty

The unified view yields a short list of *physics-level* error sources that appear, under different names, in every sensor chapter, and a corresponding list of tests.

**Propagation-speed errors are scale errors.** Test for them by comparing depths or ranges at different distances: a sound-speed error grows linearly with depth and appears as a slope-dependent, depth-proportional residual on crosslines and as the characteristic "smile" or "frown" across a multibeam swath; a refractive-index error in bathymetric lidar grows with depth and incidence angle. The diagnostic is a residual that is proportional to range, not constant.

**Refraction errors are angle-dependent.** Test by stratifying residuals by incidence or beam angle: a flat-bottom swath that curves up or down at the edges has a refraction problem; a bathymetric lidar whose depth residuals correlate with scan angle has a surface-model or refraction problem. Report residual statistics by angle bin, not only in aggregate.

**Footprint errors are slope- and roughness-dependent.** Test by stratifying residuals by local slope and by comparing with a higher-resolution reference: the smoothing bias of a large footprint appears as systematically too-low summits and too-high valleys, and as a residual variance that grows with slope. The ASPRS and USGS practice of reporting NVA on flat open ground and VVA separately exists because this term is unavoidable on slopes and under vegetation.

**Surface-definition differences are not errors.** Before computing any accuracy statistic between two datasets, state the surface each one measures using Section 17.8. Where they differ (canopy top versus ground; snow surface versus X-band phase centre; top of fluid mud versus consolidated bottom), either restrict the comparison to materials where they agree (bare rock, hard ground, sand), or model the difference explicitly as a bias with its own uncertainty, or report the difference as a measured quantity (canopy height, penetration depth) rather than as error.

**Detection errors are heavy-tailed.** Test by looking at the distribution, not the RMSE: compute the median, the NMAD, the 68th and 95th percentiles of absolute residuals, and the fraction beyond 3σ. A Gaussian residual set has about 0.3 % beyond 3σ; lidar in vegetation or multibeam outer beams routinely show 1–5 %, and those points are detection errors that the RMSE both inflates and conceals ([Chapter 5](ch05-error-and-uncertainty.md), [Chapter 53](ch53-accuracy-assessment.md)).

> **Try it.** Compute the footprint and the refraction-uncorrected depth error for a few configurations with Python; the outcome shows how quickly footprint grows across a sonar swath and how large the raw bathymetric-lidar refraction error is.
>
> ```python
> import numpy as np
>
> def footprint(range_m, beamwidth_deg, incidence_deg=0.0):
>     th = np.deg2rad(beamwidth_deg); phi = np.deg2rad(incidence_deg)
>     along = range_m * th / np.cos(phi)          # along-track (sonar) or along-scan
>     across = range_m * th / np.cos(phi) ** 2    # across-track on a flat bottom
>     return along, across
>
> for d, bw in [(20, 1.0), (4000, 1.0), (1500, 0.0143)]:   # launch MBES, deep MBES, ALS 0.25 mrad
>     for inc in (0, 45, 60):
>         a, c = footprint(d / np.cos(np.deg2rad(inc)), bw, inc)
>         print(f"range {d:6.0f} m  beam {bw:6.4f}°  inc {inc:2d}°  footprint {a:7.2f} x {c:7.2f} m")
>
> n_w = 1.34
> for z in (2, 10, 30):
>     for inc in (0, 15, 20):
>         th_a = np.deg2rad(inc); th_w = np.arcsin(np.sin(th_a) / n_w)
>         s = z / np.cos(th_w)                      # true slant path in water
>         z_wrong = n_w * s * np.cos(th_a)          # treat as air, no angle refraction
>         print(f"z={z:4.1f} m inc={inc:2d}°  uncorrected depth {z_wrong:6.2f} m  error {z_wrong - z:+5.2f} m")
> ```
>
> Expected: the deep-water 1° footprint goes from 70 m at nadir to about 280 m across-track at 60°; the uncorrected lidar depth error is about +32 % at nadir and +30 % at 20°, i.e. 3 m in 10 m of water.

> **Uncertainty budget.** Physics-level contributions, with the sensor chapters that quantify them.
>
> | Source | Nature | Scales with | Typical magnitude | Where treated |
> |---|---|---|---|---|
> | Propagation speed | scale (multiplicative) | range | 0.1–1 % of depth (sonar); < 0.03 % (lidar in air) | Ch. 20, 18 |
> | Refraction | angle-dependent, systematic | incidence angle × range | dm at swath edge (sonar); 30 % raw (bathy lidar, corrected to cm–dm) | Ch. 20, 19 |
> | Footprint smoothing | systematic on slopes | footprint × slope | footprint × tan(slope) | Ch. 44 |
> | Surface definition | systematic bias | material, wavelength | 0–30 m (canopy); 0–10 m (dry snow, X-band) | this chapter; Ch. 21, 32 |
> | Detection errors | heavy-tailed outliers | SNR, threshold | 0.3–5 % of points beyond 3σ | Ch. 30, 53 |
> | Timing / clock | additive | — | 1 ns = 15 cm (light); 1 ms = 0.75 m (sound) | Ch. 6, 18, 20 |

## Software

**Open source:** PDAL (filters for refraction correction via Python, footprint-aware thinning); `xdem` and `demcoreg` for co-registration and residual statistics stratified by slope and land cover; SNAP (ESA) and ISCE2 for InSAR height of ambiguity and phase unwrapping; MB-System (`mbvelocitytool`, ray tracing through SVPs); GMT for geoid/gravity transfer-function work; Python `gsw` (TEOS-10 sound speed and seawater properties) and `arlpy` for acoustic ray tracing; `icepyx`/SlideRule for ICESat-2 photon-level data. Caveat: most tools apply one refraction or sound-speed model silently; read the default.

**Free but closed:** NOAA's Sound Speed Manager (HydrOffice; largely open) for SVP handling; Teledyne's and Kongsberg's free viewers for raw sonar data; ESA SNAP is free and open.

**Commercial:** CARIS HIPS & SIPS and QPS Qimera (sonar ray tracing, TPU); Leica LSS, Teledyne HydroFusion, Riegl RiHYDRO (bathymetric lidar refraction and waveform processing); GAMMA and SARscape (InSAR); Agisoft Metashape and Pix4D (stereo matching precision reports). Caveat: vendor TPU models encode specific assumptions about sound speed and surface models that are not always documented.

## Standards & guides

- **IHO S-44**, Edition 6.1.0 (2022) — specifies TVU/THU by survey order; the depth-proportional "b" term is the standardised acknowledgement of the scale errors in Section 17.1.
- **ASPRS Positional Accuracy Standards for Digital Geospatial Data**, Edition 2 (2023) — separates NVA (open terrain) from VVA (vegetated), the operational response to footprint and surface-definition effects.
- **USGS Lidar Base Specification** (2024 rev. A) — defines the measured surface for ALS deliverables through its classification scheme and the treatment of water (voids, hydro-flattening).
- **ISO/IEC Guide 98-3 (GUM)** — the framework for propagating the multiplicative, angle-dependent, and additive terms of this chapter into a combined uncertainty.
- **IHO C-13 Manual on Hydrography** (2005, with updates) — chapters on acoustic propagation, sound speed, and refraction for hydrographers.
- **CEOS Cal/Val and ESA InSAR guidelines** (e.g. the TanDEM-X DEM product specification, DLR 2016) — document height of ambiguity, penetration, and the resulting product definitions. (verify)

## Pitfalls

- **Assuming the measured surface is the ground** → X-band DEMs over dry snow sit metres below the surface, canopy-top DSMs sit tens of metres above it → detect by consulting Section 17.8 for every material in the scene; avoid by stating the surface definition in the product metadata.
- **Calling a definition difference an error** → two sensors with different "surfaces" are differenced and the result is reported as RMSE → detect by stratifying differences by land cover and by seeing whether they are systematic; avoid by restricting accuracy statistics to materials where the definitions coincide.
- **Ignoring refraction in bathymetric lidar** → 30 % depth errors and metre-scale horizontal displacements → detect through residuals that scale with depth and scan angle; avoid by applying the Snell correction with the actual water-surface model.
- **Treating sound speed as a constant** → depth-proportional errors and swath "smiles" → detect on crosslines and swath-edge residuals; avoid with frequent casts and surface sound-speed sensors ([Chapter 20](ch20-sonar.md)).
- **Reading point spacing as resolution** → a 1 m grid from a 70 m footprint → detect by computing the footprint from range and beamwidth; avoid by gridding at or coarser than the footprint ([Chapter 44](ch44-resolution-and-sampling.md)).
- **Choosing a short InSAR baseline for easy unwrapping and then quoting metre accuracy** → the height of ambiguity sets the noise floor → detect by computing $h_a$ and the phase noise; report height noise accordingly.
- **Gaussian statistics on heavy-tailed residuals** → RMSE dominated by a few detection errors, or outliers hidden inside a large σ → detect with percentile statistics and the fraction beyond 3σ; report NMAD and LE95 alongside RMSE.
- **Trusting a radiometric inversion outside its calibration domain** → SDB depths over a different bottom type or water mass → detect by withholding calibration depths across bottom types; avoid by mapping the applicable domain.
- **Expecting a potential-field product to show small features** → a seamount missing from a gravity-predicted grid is not evidence of its absence → detect by reading the source metadata (ship track vs. predicted); avoid by consulting the source-identification grid.

## Key takeaways

- Every elevation sensor is one of five things: a clock (ranging), a protractor (triangulation), a phase meter (interferometry), a radiometer with a model (radiometric inversion), or a gravimeter with a model (potential-field inversion). Its error budget follows from which one it is.
- Speed errors are scale errors, refraction errors are angle errors, footprint errors are slope errors, and detection errors are outliers; each has a distinct signature in residuals, and a validation plan should stratify residuals to see them.
- The footprint $D = R\theta$ makes every sensor a low-pass filter and sets the effective-resolution floor; grid no finer than the footprint.
- Each sensor measures a physically defined surface — first/last return, phase centre, scattering centre, radiance-weighted bottom, acoustic interface — and DEM comparison across sensors is a comparison of definitions first and of errors second.
- The sensor–material matrix (Section 17.8) predicts voids and biases before acquisition; use it in planning and again when interpreting differences.
- Detection is a statistical decision, so residual distributions are heavy-tailed; report robust statistics and the outlier fraction, not RMSE alone.
- Light in air is fast and well-behaved; sound in water is slow and bent; light in water is attenuated and refracted. These three facts organise the error budgets of Chapters 18–20.

## References

- Lurton, X. (2010). *An Introduction to Underwater Acoustics: Principles and Applications*, 2nd ed. Springer/Praxis.
- Shan, J., & Toth, C. K. (eds.) (2018). *Topographic Laser Ranging and Scanning: Principles and Processing*, 2nd ed. CRC Press.
- Hanssen, R. F. (2001). *Radar Interferometry: Data Interpretation and Error Analysis*. Kluwer.
- Jensen, J. R. (2007). *Remote Sensing of the Environment: An Earth Resource Perspective*, 2nd ed. Pearson Prentice Hall.
- Elachi, C., & van Zyl, J. (2006). *Introduction to the Physics and Techniques of Remote Sensing*, 2nd ed. Wiley.
- Medwin, H., & Clay, C. S. (1998). *Fundamentals of Acoustical Oceanography*. Academic Press.
- Urick, R. J. (1983). *Principles of Underwater Sound*, 3rd ed. McGraw-Hill.
- Baltsavias, E. P. (1999). Airborne laser scanning: basic relations and formulas. *ISPRS Journal of Photogrammetry and Remote Sensing*, 54(2–3):199–214.
- Wagner, W., Ullrich, A., Ducic, V., Melzer, T., & Studnicka, N. (2006). Gaussian decomposition and calibration of a novel small-footprint full-waveform digitising airborne laser scanner. *ISPRS Journal of Photogrammetry and Remote Sensing*, 60(2):100–112.
- Rosen, P. A., Hensley, S., Joughin, I. R., Li, F. K., Madsen, S. N., Rodriguez, E., & Goldstein, R. M. (2000). Synthetic aperture radar interferometry. *Proceedings of the IEEE*, 88(3):333–382.
- Bamler, R., & Hartl, P. (1998). Synthetic aperture radar interferometry. *Inverse Problems*, 14(4):R1–R54.
- Rizzoli, P., Martone, M., Rott, H., & Moreira, A. (2017). Characterization of snow facies on the Greenland Ice Sheet observed by TanDEM-X interferometric SAR data. *Remote Sensing*, 9(4):315.
- Dall, J. (2007). InSAR elevation bias caused by penetration into uniform volumes. *IEEE Transactions on Geoscience and Remote Sensing*, 45(7):2319–2324.
- McCauley, J. F., Schaber, G. G., Breed, C. S., Grolier, M. J., Haynes, C. V., Issawi, B., Elachi, C., & Blom, R. (1982). Subsurface valleys and geoarcheology of the eastern Sahara revealed by Shuttle Radar. *Science*, 218(4576):1004–1020.
- Pope, R. M., & Fry, E. S. (1997). Absorption spectrum (380–700 nm) of pure water. II. Integrating cavity measurements. *Applied Optics*, 36(33):8710–8723.
- Quan, X., & Fry, E. S. (1995). Empirical equation for the index of refraction of seawater. *Applied Optics*, 34(18):3477–3480.
- Lyzenga, D. R. (1978). Passive remote sensing techniques for mapping water depth and bottom features. *Applied Optics*, 17(3):379–383.
- Stumpf, R. P., Holderied, K., & Sinclair, M. (2003). Determination of water depth with high-resolution satellite imagery over variable bottom types. *Limnology and Oceanography*, 48(1, part 2):547–556.
- Smith, W. H. F., & Sandwell, D. T. (1994). Bathymetric prediction from dense satellite altimetry and sparse shipboard bathymetry. *Journal of Geophysical Research*, 99(B11):21803–21824.
- Smith, W. H. F., & Sandwell, D. T. (1997). Global sea floor topography from satellite altimetry and ship depth soundings. *Science*, 277(5334):1956–1962.
- Mackenzie, K. V. (1981). Nine-term equation for sound speed in the oceans. *Journal of the Acoustical Society of America*, 70(3):807–812.
- Hughes Clarke, J. E. (2018). The impact of acoustic imaging geometry on the fidelity of seabed bathymetric models. *Geosciences*, 8(4):109.
- Kay, S. M. (1998). *Fundamentals of Statistical Signal Processing, Volume II: Detection Theory*. Prentice Hall.
- Neumann, T. A., et al. (2019). The Ice, Cloud, and Land Elevation Satellite – 2 mission: A global geolocated photon product derived from the Advanced Topographic Laser Altimeter System. *Remote Sensing of Environment*, 233:111325.

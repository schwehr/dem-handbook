# Chapter 37 — Time scales of surface change

> **Part VIII — The dynamic Earth.** This short chapter opens the Part by giving every "the ground moved" problem a common frame — amplitude against period — so that the chapters on plate motion, sudden deformation, erosion, and change detection that follow can be read as special cases of one question: can this survey, at this cadence, see this process?

**In this chapter.** You will learn to place any surface change — a passing truck, a tide, a crop, a subsiding delta, an earthquake, a drifting continent — on a log–log map of amplitude versus period, and to read from that map whether a given survey can detect it, alias it, or must ignore it. You will distinguish reversible from irreversible, periodic from secular from episodic change, and see what a single-epoch DEM freezes and what it cannot represent. You will separate the three times attached to every elevation — when it was measured, the epoch its coordinates refer to, and the window for which it is valid — and learn how to record each in metadata (acquisition start/end, per-pixel date rasters, coordinate reference epoch, tidal datum epoch). You will apply a temporal Nyquist rule to survey cadence, see how seasonal signals alias into false trends when sampled annually at the wrong phase, and finish with a decision rule for declaring a DEM "out of date" for a specific use, with a worked example and a runnable snippet that fits a trend with correlated errors.

## 37.1 A log–log map of change

Every process that moves the surface can be summarized by two numbers: a characteristic **amplitude** (how far the surface moves, in metres) and a characteristic **period** or **duration** (how long the motion takes to happen, or to repeat). Plotting processes on log–log axes — amplitude from 10⁻³ m to 10⁴ m, time from seconds to millions of years — produces a map that is more useful than any list, because a survey also occupies a region of the same map: its vertical uncertainty σ sets a floor below which it cannot see, and its repeat interval sets the shortest period it can resolve. A process is detectable by a survey program only if it lies above the survey's noise floor *and* at a period the program samples adequately.

<!-- figure: Figure 37.1 — Log–log chart of amplitude (mm to km, vertical axis) against period or duration (seconds to Myr, horizontal axis). Process clouds: vehicles and ships (1–10 m, seconds–minutes), wire sway (0.1–5 m, seconds), ocean tides (0.1–15 m, 12 h), Earth tides and ocean loading (1–40 cm, 12 h), atmospheric loading (1 cm, days), crops (0.1–3 m, months), snow (0.1–10 m, months), groundwater seasonal (1–10 cm, annual), subsidence (1–40 cm/yr accumulating to metres, years–decades), GIA (1–13 mm/yr, millennia), plate motion (1–10 cm/yr, Myr), coseismic (0.1–10 m, seconds, episodic), volcanic flows (1–100 m, days–months), landslides (1–100 m, seconds–years), fluvial/coastal erosion (0.01–10 m/yr), sea-level rise (3–4 mm/yr, century). Overlaid: rectangles for survey types (TLS, UAV SfM, airborne lidar, SRTM-class, GNSS CORS, InSAR) by vertical σ and practical repeat interval. -->

Table 37.1 gives representative magnitudes. The numbers are typical ranges, not specifications; each is developed with sources in the chapter that owns the process.

| Process | Typical amplitude | Period / duration | Character | Owning chapter |
|---|---|---|---|---|
| Vehicles, ships, cranes | 1–15 m (object height) | Seconds–hours | Transient | [Ch. 27](ch27-moving-and-transient-objects.md) |
| Conductor sway and sag | 0.1–5 m | Seconds (sway); hours (thermal sag) | Periodic/transient | [Ch. 33](ch33-wires-and-thin-structures.md) |
| Ocean tide | 0.2–15 m | 12.42 h, 24 h, 14 d, 18.6 yr | Periodic | [Ch. 9](ch09-vertical-datums.md), [Ch. 34](ch34-water-in-dems.md) |
| Solid-Earth tide | up to ~40 cm vertical | 12 h / 24 h | Periodic | [Ch. 36](ch36-seasonal-variability.md) |
| Ocean tidal loading | 1–10 cm (coasts) | 12 h | Periodic | [Ch. 36](ch36-seasonal-variability.md) |
| Atmospheric / hydrological loading | 0.5–3 cm | Days–annual | Periodic | [Ch. 36](ch36-seasonal-variability.md) |
| Crops and grass | 0.1–3 m | Seasonal | Periodic, reversible | [Ch. 36](ch36-seasonal-variability.md) |
| Snowpack | 0.1–10 m | Seasonal | Periodic, reversible | [Ch. 36](ch36-seasonal-variability.md) |
| Seasonal groundwater | 1–10 cm (poroelastic) | Annual | Periodic, partly reversible | [Ch. 38](ch38-plate-motion-and-vlm.md) |
| Anthropogenic subsidence | 0.5–40 cm/yr; metres cumulative | Years–decades | Secular, irreversible | [Ch. 38](ch38-plate-motion-and-vlm.md) |
| Glacial isostatic adjustment | −2 to +13 mm/yr | Millennia | Secular | [Ch. 38](ch38-plate-motion-and-vlm.md) |
| Plate motion (horizontal) | 1–10 cm/yr | Myr | Secular | [Ch. 38](ch38-plate-motion-and-vlm.md) |
| Coseismic displacement | 0.01–10 m (locally > 20 m) | Seconds–minutes | Episodic, irreversible | [Ch. 39](ch39-earthquakes-volcanoes-landslides.md) |
| Post-seismic relaxation | 0.01–1 m | Months–decades | Decaying transient | [Ch. 39](ch39-earthquakes-volcanoes-landslides.md) |
| Volcanic inflation/deflation | 1 cm–1 m | Days–years | Episodic, partly reversible | [Ch. 39](ch39-earthquakes-volcanoes-landslides.md) |
| Lava flows, dome growth, collapse | 1–500 m | Hours–months | Episodic, irreversible | [Ch. 39](ch39-earthquakes-volcanoes-landslides.md) |
| Landslides | 1–100 m | Seconds (rock avalanche) to years (creep) | Episodic or slow secular | [Ch. 39](ch39-earthquakes-volcanoes-landslides.md) |
| Fluvial and coastal erosion/deposition | 0.01–10 m/yr | Event-driven, annual | Episodic with secular trend | [Ch. 40](ch40-erosion-and-geomorphic-change.md) |
| Glacier thinning | 0.1–3 m/yr | Annual, decadal | Secular with seasonal cycle | [Ch. 40](ch40-erosion-and-geomorphic-change.md) |
| Global mean sea-level rise | 3–4 mm/yr (recent decades) | Century | Secular | [Ch. 66](ch66-coastal-marine-polar-lakes-rivers.md) |

Three features of this map drive the rest of the Part. First, the fast transients (vehicles, tides, wires) are usually *larger* than the slow signals (subsidence, GIA, sea-level rise) by one to three orders of magnitude, so a single survey is dominated by nuisances it must remove before the signals of interest are even visible. Second, the slow signals accumulate: 5 mm/yr of subsidence is invisible between two lidar flights a year apart (σ ≈ 5–10 cm each) but is 25 cm after fifty years, larger than the vertical accuracy of most national DEMs and larger than the freeboard of many levees. Third, the episodic processes — earthquakes, eruptions, landslides — have *no* characteristic period; they are step functions in time whose timing is unknown in advance, and they cannot be sampled adequately by any fixed cadence. They can only be detected after the fact, which is why [Chapter 39](ch39-earthquakes-volcanoes-landslides.md) is about response rather than monitoring.

> **Rule of thumb.** A process with rate $r$ is detectable between two surveys separated by $\Delta t$ when $r\,\Delta t \gtrsim 2\,\sqrt{\sigma_1^2 + \sigma_2^2}$, where σ are the per-epoch vertical uncertainties *after* co-registration (see [Chapter 41](ch41-change-detection.md) for the level of detection). For airborne lidar with σ ≈ 7 cm per epoch, that is about 20 cm of accumulated change — four years of 5 cm/yr subsidence, forty years of 5 mm/yr. The rule fails when the errors are spatially correlated or share a systematic component (same control, same geoid model), in which case the difference may be far better than the rule predicts for *relative* change and far worse for *absolute* change.

## 37.2 Reversible, irreversible, periodic, secular, episodic

The map in Figure 37.1 is two-dimensional, but processes differ in a third way: their shape in time. Four shapes recur, and they demand different survey designs.

**Periodic** change (tides, Earth tides, seasons, diurnal thermal expansion of a bridge) returns to its starting state. It can be modelled and removed if its phase is known at the time of measurement — which is why tide-reduced bathymetry, Earth-tide-corrected GNSS heights, and leaf-off lidar exist — and it can be *averaged out* by sampling many phases, which is what the 19-year **National Tidal Datum Epoch** (NTDE) does for the 18.6-year lunar nodal cycle ([Chapter 9](ch09-vertical-datums.md)). The danger of periodic change is aliasing (§37.4): sampled once a year at a drifting phase, a seasonal cycle masquerades as a trend.

**Secular** change (plate motion, GIA, pumping-induced subsidence, sediment compaction, sea-level rise, glacier thinning under a warming climate) proceeds in one direction at a rate that is roughly constant over the time scale of interest. It is the easiest to model — a velocity — and the most dangerous to forget, because it is invisible within any one survey and only appears as a discrepancy between surveys or between a survey and old control. The test for secular change is always a comparison across epochs, and the correct representation is a coordinate plus a velocity plus a reference epoch ([Chapter 38](ch38-plate-motion-and-vlm.md)).

**Episodic** change (earthquakes, eruptions, landslides, floods, storms, dredging, construction) is a step or an impulse. It has a before and an after, and the "after" state is usually permanent. Episodic change is irreversible in the geometric sense even when it is small; it breaks the velocity model of secular change and must be represented as a displacement field attached to a date — which is what deformation-model "patches" are ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md)).

**Transient** change (vehicles, smoke, steam, water level during a flood, snow, a construction crane) is present at the moment of measurement and absent later, or vice versa, without any lasting effect on the ground. Transients are the subject of [Chapter 27](ch27-moving-and-transient-objects.md) and [Chapter 36](ch36-seasonal-variability.md); they matter here because a change-detection study that does not classify them will report them as change.

The reversible/irreversible axis cuts across these shapes. Poroelastic seasonal uplift of an aquifer system is periodic and reversible; the inelastic compaction of the clay interbeds that accompanies it is secular and irreversible, and the two superpose — a GNSS station over the Central Valley of California shows a sawtooth with a declining mean (Galloway and Burbey 2011; [Chapter 38](ch38-plate-motion-and-vlm.md)). Post-seismic relaxation is a decaying transient layered on a coseismic step; glacier thinning is a secular trend layered on a seasonal cycle of several metres. Separating the components requires sampling that resolves the fastest one, or a model that removes it.

What does a single-epoch DEM freeze? Everything. A DEM is the surface at the instants its cells were measured — different instants in different cells, often separated by hours within a flight block, by months within a national campaign, and by years within a global mosaic. It freezes the tide phase at the shoreline, the crop height in the fields, the cars on the highway, the snow in the mountains, the position of the plate, the subsidence accumulated to that date, and the post-seismic motion since the last earthquake. None of this is an error; it is the nature of a snapshot. The error arises when the user treats the snapshot as timeless: compares it with another snapshot without reconciling their instants, or uses it in 2030 as if it described 2030.

> **Definitions that bite.** "Current" in a data catalog can mean (a) the most recently published version, (b) the most recently *acquired* data, (c) the data whose coordinates are propagated to the present epoch, or (d) the data that still describes the ground. A national DEM republished in 2024 with coordinates transformed to a 2020-epoch datum may be built from 2011 lidar over a delta subsiding at 1 cm/yr; it is current in senses (a) and (c), 13 years old in sense (b), and 13 cm wrong in sense (d). Catalog metadata rarely distinguishes the four.

## 37.3 Three times: measured, referenced, valid

Every elevation carries, explicitly or by default, three distinct times, and most of the confusion in Part VIII comes from conflating them.

The **measurement time** (acquisition time, observation epoch) is when the sensor touched the surface. For a lidar point it is the GPS timestamp of the pulse ([Chapter 6](ch06-time-as-coordinate.md)); for a DEM cell it is a range (the flight lines that contributed) or, in a mosaic, a value that varies cell by cell. It is a fact about the data and cannot be changed by processing.

The **reference epoch** of the coordinates is the date at which the coordinate reference frame's positions are defined to be valid. A point surveyed in 2023 with GNSS and expressed in ITRF2020 "at epoch 2023.5" carries coordinates for where it was in mid-2023; the same point expressed in NAD83(2011) epoch 2010.00 carries coordinates for where it *would have been* on 1 January 2010 according to the datum's velocity model, even though it was measured in 2023 ([Chapter 8](ch08-horizontal-datums.md)). In a plate-fixed datum the two differ by less than the deformation relative to the plate (millimetres to centimetres per year within a stable plate interior; much more near plate boundaries); in a global frame they differ by the full plate velocity, 2–7 cm/yr. For heights the reference epoch is equally real but less often stated: a NAVD 88 height published for a benchmark is the height when the benchmark was levelled and adjusted, and in subsiding terrain it decays from the day of publication.

The **validity window** is the span of time over which the data describe the surface to within the user's tolerance. It depends on the use, not only on the data: a 2011 DEM may be valid for watershed delineation in 2040 and invalid for levee freeboard assessment in 2015. Validity is a judgment the producer can inform (by stating acquisition dates and known rates of change) but only the user can make (§37.7).

A fourth time belongs to tidal datums specifically: the **tidal datum epoch**. Mean sea level, mean lower low water, and the other tidal datums are 19-year averages, and the U.S. NTDE is updated roughly every 20–25 years (the 1983–2001 epoch is current at this writing; NOAA has announced its replacement with a 2002–2020 epoch and a move to more frequent updates in regions of rapid relative sea-level change). Depths reduced to MLLW of one epoch differ from depths reduced to MLLW of the next by the local relative sea-level change between the epochs — around 5–10 cm along much of the U.S. coast, 20 cm or more in subsiding Gulf Coast and Alaskan uplift areas. Two charts, two bathymetric DEMs, or a bathymetric DEM and a topographic DEM referenced to different tidal epochs disagree by that amount before any measurement error is considered ([Chapter 9](ch09-vertical-datums.md)).

<!-- figure: Figure 37.2 — Timeline for a single coastal point showing: measurement instants of three surveys (1979 levelling, 2011 lidar, 2023 GNSS); the reference epochs of the frames each used (NGVD 29, NAVD 88 at adjustment, NAD83(2011) epoch 2010.00, ITRF2020 at 2023.5); the tidal datum epochs in force at each date; and the actual height history of the point under 8 mm/yr subsidence, illustrating the growing gap between "published" and "true" height. -->

## 37.4 Matching survey cadence to process rate

A survey program is a sampling scheme in time, and the sampling theorem applies to it exactly as it applies to a waveform: a signal with period $T$ can only be reconstructed from samples taken at intervals $\Delta t \le T/2$, i.e. at a sampling frequency $f_s \ge 2 f_{\max}$. Sampled more slowly, the signal does not vanish — it **aliases**: it appears in the record at a false, lower frequency determined by the beat between the true period and the sampling interval. In elevation work the relevant signals are rarely sinusoidal, but the consequence is the same: a cadence longer than half the period of the fastest significant process produces a record that cannot be interpreted without a model of that process.

The classic case is the annual cycle sampled annually. Suppose a floodplain surface moves seasonally by ±5 cm (soil moisture swelling, vegetation litter, frost) and subsides secularly at 3 mm/yr. Surveys flown every 12 months at the same phase see only the secular 3 mm/yr, correctly. Surveys flown "about yearly" at drifting phases — March, then July, then October, then February — sample the 10 cm peak-to-peak seasonal cycle at four phases and produce apparent year-to-year changes of several centimetres with random sign, swamping the 3 mm/yr trend. Worse, a cadence of 13 or 14 months samples the annual cycle at a slowly advancing phase and aliases it into a false multi-year oscillation with period $1/|1/T - 1/\Delta t|$ — for $T$ = 12 months and $\Delta t$ = 13 months, a 13-year apparent cycle that is pure artefact. Two epochs in a seasonal environment do not constitute a trend; they constitute two samples of unknown phase.

The practical corollaries are these. Choose the repeat interval from the process you need to see, then check it against the processes you need to *not* see. For secular signals, hold the acquisition phase fixed (same month, same tide stage, leaf-off) so that the periodic components cancel in the difference; the design is then a matched-phase differencing, and the residual periodic error is the year-to-year variability of the cycle, not its amplitude. For periodic signals you want to measure (snow depth, tidal flats), sample at the extrema or at many phases. For episodic processes, cadence is irrelevant; what matters is the pre-event baseline being recent enough that the post-event difference is dominated by the event ([Chapter 39](ch39-earthquakes-volcanoes-landslides.md)).

Averaging helps only against random error. If each epoch has independent random vertical error σ, the mean of $N$ epochs has random error $\sigma/\sqrt{N}$, and a trend fitted to $N$ evenly spaced epochs over total span $S$ has rate uncertainty $\sigma_{\dot z} \approx \sigma\sqrt{12/(N\,S^2)}$ (for large $N$; see Mathematics). But systematic error — a geoid-model bias, a datum offset, a vegetation-penetration bias shared by every epoch — does not average away, and *correlated* error (the same control network, the same sensor calibration drift) averages away only in proportion to the number of independent realizations, not the number of epochs. A rate derived from ten epochs of lidar all tied to the same subsiding benchmark is precise and wrong.

> **Worked example.** A coastal county has airborne lidar from 2008, 2014, and 2021, each with a validated NVA of 9.8 cm at 95 % (σ ≈ 5 cm) relative to the same NAVD 88 control, and wants to know whether a marsh platform is keeping pace with sea-level rise (3.5 mm/yr locally). Expected accumulated change over 13 years: 4.6 cm if the marsh is static, 0 if it keeps pace. Per-epoch random σ ≈ 5 cm; difference of two epochs σ ≈ 7 cm; LoD at 95 % ≈ 14 cm. The expected signal (≤ 4.6 cm) is one third of the LoD: the question **cannot be answered** by these data, pixel by pixel. Averaging over the 20 000 cells of the marsh platform reduces the random component to millimetres, but the three epochs were flown in different seasons (October, March, July), the marsh grass is 30–60 cm tall, and the "ground" returned by each sensor depends on canopy density; the seasonal/penetration bias, perhaps 5–10 cm, is larger than the signal and does not average. Honest answer: the lidar constrains marsh elevation change to within roughly ±10 cm over 13 years, which is uninformative at the 3.5 mm/yr level; use surface-elevation tables (SETs) or RTK transects on fixed plots instead. The arithmetic is trivial; the point is to do it before designing the study.

## 37.5 Kinematic datums and time-dependent coordinates

Until the 1990s a datum was a set of fixed coordinates for fixed monuments, and a map was a fixed picture. GNSS broke this in two ways: it measured positions in a global frame in which every continent moves at centimetres per year, and it measured precisely enough that the motion was obvious within a single year. The response, developed in detail in [Chapter 38](ch38-plate-motion-and-vlm.md), has three tiers. A **plate-fixed datum** (NAD83, ETRS89, GDA2020, NZGD2000) rotates with its plate so that coordinates of points on the stable interior stay nearly constant; the price is a growing offset from the global frame (ETRS89 is now about 0.8 m from ITRF, growing ~2.5 cm/yr; NAD83 is 1–2 m from ITRF with drift of 1–2 cm/yr) and the inability to represent deformation within the plate. A **semi-dynamic** datum (NZGD2000, Japan's semi-dynamic correction, NAD83 with HTDP) keeps fixed reference-epoch coordinates but supplies a deformation model to move observations to and from that epoch. A fully **dynamic** (kinematic) datum (ITRF, the Australian Terrestrial Reference Frame ATRF, the modernized U.S. NSRS) gives every coordinate an epoch and expects users to propagate.

ISO 19111:2019 formalized the vocabulary — **dynamic datum**, **coordinate epoch** (a decimal year such as 2023.47), and **point-motion operation** (moving a coordinate between epochs within one frame, as distinct from a transformation between frames) — and PROJ implements all three; a transformation from ITRF2020 at 2023.5 to NAD83(2011) at 2010.00 is properly a point-motion operation followed by a 14-parameter Helmert transformation, with the order and the epochs mattering at the centimetre level ([Chapter 38](ch38-plate-motion-and-vlm.md)).

For DEMs the practical questions are narrower than for control surveys, because a DEM's vertical content is expressed in a height system whose epoch is usually implicit. Three cases arise. If a DEM's horizontal coordinates are in a plate-fixed datum and the vertical is an orthometric height on a geoid model, the DEM's position relative to the ground moves only with intraplate deformation — negligible for a decade in a plate interior, decimetres over a decade across a plate boundary like New Zealand or California. If the horizontal is in ITRF at a stated epoch, propagating the DEM forward in time means shifting the entire raster horizontally by the plate velocity times the elapsed time: 7 cm/yr × 10 yr = 0.7 m in Australia, which is a full cell of a 0.5 m DEM and generates slope-dependent apparent height changes of $0.7 \tan\alpha$ when differenced against a newer DEM — 12 cm on a 10° slope. If the vertical is an ellipsoidal height in ITRF, the DEM also inherits the vertical component of plate motion and GIA, which is a few millimetres per year almost everywhere but 10 mm/yr or more in Fennoscandia and Hudson Bay. These are the cases that [Chapter 38](ch38-plate-motion-and-vlm.md) quantifies and [Chapter 41](ch41-change-detection.md) tests for.

## 37.6 Expressing time in metadata

Metadata is where the three times of §37.3 either survive or disappear. The minimum set a DEM producer should record, and a user should look for, is the following.

**Acquisition start and end.** Dates (and, for tidal and diurnal processes, times with time zone) of the first and last observation contributing to the product. For a single flight block this is a day or a week; for a national program, years. ISO 19115 carries this as a temporal extent; STAC Items carry `start_datetime` and `end_datetime` ([Chapter 49](ch49-metadata.md), [Chapter 51](ch51-finding-data.md)). A single `datetime` for a multi-year mosaic is not acceptable; set it null and populate the range.

**Per-pixel date raster.** For any composite — SRTM (acquired 11–22 February 2000, a happy case of one epoch), the Copernicus DEM (TanDEM-X acquisitions 2011–2015, varying by tile and by pixel), ArcticDEM and REMA mosaics (strips from 2008 onward, with a date-of-acquisition raster distributed alongside), national lidar mosaics stitched from projects a decade apart — a companion raster giving the acquisition date (or the index into a date table) for each cell is the only honest representation. Without it, change detection against the mosaic produces a patchwork of apparent change at project seams that is in fact the difference in acquisition date multiplied by the local rate of change. The ArcticDEM/REMA mosaics ship such rasters; most national products do not, and the user must reconstruct dates from tile indices and project reports ([Chapter 48](ch48-compositing.md)).

**Coordinate reference epoch.** For data in a dynamic frame, mandatory; ISO 19111:2019 provides `coordinateEpoch`, and PROJ/WKT2 can express it (`EPOCH[2023.5]` in a `COORDINATEMETADATA` construct). For data in a plate-fixed or static datum, record the datum realization and its reference epoch (NAD83(2011) epoch 2010.00; GDA2020 is ITRF2014 at 2020.0; ETRS89 realizations ETRF2000, ETRF2014 at their respective epochs) so that a future user can transform correctly ([Chapter 8](ch08-horizontal-datums.md)).

**Vertical datum realization and, for heights derived from GNSS, the geoid model and its version** (GEOID12B, GEOID18, AUSGeoid2020, EGM2008), because the realization determines the epoch of the vertical reference. **Tidal datum epoch** for any product referenced to a tidal datum, and the tide station(s) used.

**Processing date and version**, separately from acquisition date, because a reprocessing (new geoid model, new classification, new void fill) changes the product without changing the surface it describes — a frequent source of false "change" ([Chapter 41](ch41-change-detection.md), [Chapter 50](ch50-archiving-and-provenance.md)).

> **Try it.** Build a per-pixel acquisition-date raster for a mosaic from its tile footprints, then difference two mosaics and express the result as a *rate* rather than a change, so that seams with different time spans are comparable.
>
> ```bash
> # Tile footprints with an 'acq_date' attribute (ISO date) -> decimal-year raster
> ogr2ogr -f GPKG tiles_dy.gpkg tiles.gpkg -dialect sqlite \
>   -sql "SELECT geom, CAST(strftime('%Y',acq_date) AS REAL) + \
>         (strftime('%j',acq_date)-1)/365.25 AS dy FROM tiles"
> gdal_rasterize -a dy -tr 1 1 -a_nodata -9999 -ot Float32 \
>   -te 500000 4100000 510000 4110000 tiles_dy.gpkg date_2014.tif
> # (repeat for the second mosaic -> date_2021.tif)
> # Rate raster in m/yr: (z2 - z1) / (t2 - t1); mask where span < 2 yr
> gdal_calc.py -A dem_2021.tif -B dem_2014.tif -C date_2021.tif -D date_2014.tif \
>   --calc="where((C-D)>=2.0, (A-B)/(C-D), -9999)" --NoDataValue=-9999 \
>   --outfile=rate_m_per_yr.tif --type=Float32
> gdalinfo -stats rate_m_per_yr.tif | grep -E "MIN|MAX|MEAN|STDDEV"
> ```
>
> Expected outcome: a rate raster whose statistics over stable terrain (parking lots, bedrock) are centred near 0 with σ of a few cm/yr; seams between tiles of different dates no longer appear as steps in the rate raster if the surface change is genuinely secular, and *do* appear if it is seasonal or episodic — which is itself diagnostic.

## 37.7 Decision rule: when is a DEM out of date?

A DEM is out of date for a use when the accumulated change since acquisition exceeds the vertical tolerance of that use. Written as a rule:

$$
\text{out of date if}\quad |\hat r|\,(t_{\text{use}} - t_{\text{acq}}) + k\,\sigma_r\,(t_{\text{use}} - t_{\text{acq}}) + \Delta_{\text{episodic}} > \tau_{\text{use}} - \text{LE}_{\text{DEM}},
$$

where $\hat r$ is the best estimate of the local rate of surface change (from CORS, InSAR, levelling, or geomorphic knowledge), $\sigma_r$ its uncertainty, $k$ a coverage factor (1.96 for 95 %), $\Delta_{\text{episodic}}$ the displacement of any known event since acquisition, $\tau_{\text{use}}$ the vertical tolerance of the application, and $\text{LE}_{\text{DEM}}$ the DEM's own vertical error at the same confidence. The rule says: the DEM's error budget is spent partly on measurement error and partly on age, and when age uses up what the application left over, the DEM is stale.

The rule yields very different lifetimes for the same data. Take a 2015 lidar DTM with LE95 = 15 cm.

| Use | τ (95 %) | Local rate | Lifetime from 2015 |
|---|---|---|---|
| Watershed delineation, 10 m grid | ~2 m | any | effectively unlimited absent episodic change |
| Flood-insurance base flood elevation, stable terrain | 30 cm | 1 ± 1 mm/yr | > 50 yr |
| Same, subsiding coastal plain | 30 cm | 10 ± 3 mm/yr | ~9 yr → stale by about 2024 |
| Levee freeboard check | 15 cm | 10 ± 3 mm/yr | 0 yr → never adequate; need better DEM and current control |
| Runway obstacle surface (ICAO Area 2) | 3 m vertical, but *any* new object | — | until the next construction; semantic currency dominates |
| Post-earthquake tsunami inundation model, Kaikōura coast | 30 cm | step of 1–6 m in 2016 | invalidated on 14 November 2016 |

Two further considerations modify the rule. **Semantic currency** — whether the objects on the surface are still there — is independent of geodetic currency and often expires faster: a DSM for line-of-sight analysis in a growing suburb is stale in two years regardless of any ground motion ([Chapter 42](ch42-object-detection-semantics.md)). And **relative** uses (slope, local drainage, volume between two surfaces measured the same way) tolerate uniform secular change that **absolute** uses (elevation against a flood level, clearance against a datum surface) do not; the same DEM may be simultaneously stale for one and fine for the other.

The rule also tells the producer what to publish: the acquisition date (so the user can compute the age), a pointer to the regional VLM rate (or the rate itself as a companion raster), and the known episodic events since acquisition. Gesch (2018) made the case for coastal sea-level-rise assessments specifically: a DEM's acquisition date and vertical accuracy must both be carried into the inundation analysis, and the analysis's own temporal horizon (2050, 2100) must be compared against the DEM's expected lifetime under local VLM. A DEM used for 2100 inundation mapping of a coast subsiding at 8 mm/yr will be, by 2100, 70 cm out of date relative to the terrain it was supposed to represent — comparable to the sea-level-rise scenario itself.

> **Case file.** After Hurricane Katrina (August 2005), the Interagency Performance Evaluation Task Force found that parts of the New Orleans hurricane-protection system stood well below design grade relative to contemporary sea level, in part because the structures had been built to benchmarks whose published heights had decayed under regional subsidence (Dixon et al. 2006 measured a 2002–2005 citywide average of about 5.6 mm/yr by InSAR, locally far more). The design heights were correct at their reference epoch; the use required a currency the control did not have. The re-levelling and the epoch-tagged NAVD 88 (2004.65) heights that followed are developed in [Chapter 38](ch38-plate-motion-and-vlm.md).

<!-- figure: Figure 37.3 — Decision chart: inputs (acquisition date, DEM LE95, application tolerance, local VLM rate and uncertainty, episodic events since acquisition) → computed age-induced error → comparison with remaining tolerance → verdict (valid / valid for relative uses only / stale / invalidated by event), with the levee, flood-map, and watershed rows of the table plotted as example trajectories. -->

## Then & now

The paper map assumed a static Earth because it had to: the surveys that fed it took decades, the printing cycle took years, and the measurement precision — a few decimetres in height by spirit levelling over long lines, metres in position by triangulation — was coarser than any slow process. Benchmarks were "permanent"; a published elevation was a property of the monument, not a reading at a date. The fixed terrestrial datums of the first half of the twentieth century (NAD27 ⟨H⟩, ED50, OSGB36) embodied this: coordinates without epochs, by construction.

Three developments made time unavoidable. First, space geodesy: VLBI and SLR in the 1970s–80s and GPS from the late 1980s measured intercontinental baselines to centimetres and showed plates moving at the rates geologists had inferred from magnetic anomalies; the International Terrestrial Reference Frame series (ITRF88 onward; ITRF2014, Altamimi et al. 2016; ITRF2020, Altamimi et al. 2023) gave every station a velocity, and NAD83's drift relative to ITRF (~1–2 cm/yr, direction varying across the continent) became a routine datum problem rather than a research result ([Chapter 8](ch08-horizontal-datums.md), [Chapter 11](ch11-history-of-positioning.md)). Second, repeat observation: airborne lidar from the late 1990s, with vertical σ of a decimetre and the ability to re-fly a county in a week, made geomorphic change measurable rather than inferable (Brasington et al. 2003; Wheaton et al. 2010; [Chapter 40](ch40-erosion-and-geomorphic-change.md)); InSAR from the 1992 Landers interferogram onward put coseismic and subsidence fields on a map at millimetre-to-centimetre precision ([Chapter 21](ch21-radar-sar-insar.md)). Third, the free, systematic missions — Sentinel-1 since 2014, ICESat-2 since 2018, repeat ArcticDEM/REMA stereo — turned change from a bespoke study into a time series anyone can download.

The result is a reversal of defaults. Where change used to be a nuisance to be averaged away so that a map could be published, in the current practice of geodesy, glaciology, hydrography of mobile seabeds, and urban monitoring, change *is* the product, and the single-epoch DEM is the intermediate. Eitel et al. (2016) framed this for ecosystem science as "4D" lidar — the surface as a function of time at the scale of the process; Anders et al. (2020) built the analysis tools for permanent-scanner time series in which thousands of epochs are the norm. The datums have followed: ISO 19111 acquired dynamic datums and coordinate epochs in 2019, Australia moved to a datum (GDA2020) explicitly defined as a snapshot of a dynamic frame, and the modernized U.S. National Spatial Reference System is designed around time-dependent coordinates and an intra-frame velocity model.

## Mathematics

**Sampling in time.** A process with highest significant frequency $f_{\max}$ (period $T_{\min} = 1/f_{\max}$) is recoverable from regular samples at interval $\Delta t$ only if $f_s = 1/\Delta t \ge 2 f_{\max}$. A periodic component at frequency $f > f_s/2$ appears at the alias frequency $f_a = |f - n f_s|$ for the integer $n$ that minimizes $f_a$. For an annual signal ($f$ = 1 yr⁻¹) sampled at 13-month intervals ($f_s$ = 12/13 yr⁻¹), $f_a = |1 - 12/13| = 1/13$ yr⁻¹: a spurious 13-year cycle. Sampling at exactly the annual period ($f_s = f$) aliases the signal to zero frequency — a constant offset — which is harmless for trend estimation but means the offset's sign depends on the phase chosen.

**Detectability of accumulated change.** For two epochs with independent vertical errors $\sigma_1, \sigma_2$, the difference has $\sigma_\Delta = \sqrt{\sigma_1^2 + \sigma_2^2}$, and a change $\Delta z$ is detected at confidence $1-\alpha$ when $|\Delta z| > z_{1-\alpha/2}\,\sigma_\Delta$ (the level of detection, [Chapter 41](ch41-change-detection.md)). For a secular rate $r$ the minimum span to detect it is $S_{\min} = z_{1-\alpha/2}\,\sigma_\Delta / |r|$.

**Rate from $N$ epochs.** For heights $z_i$ at times $t_i$, $i = 1\dots N$, with the linear model $z_i = z_0 + r\,(t_i - \bar t) + \varepsilon_i$ and independent, equal-variance errors, the least-squares rate is $\hat r = \sum (t_i - \bar t) z_i / \sum (t_i - \bar t)^2$ with variance $\sigma_{\hat r}^2 = \sigma^2 / \sum (t_i - \bar t)^2$. For $N$ evenly spaced epochs spanning $S$, $\sum (t_i - \bar t)^2 = S^2 N (N+1)/(12 (N-1)) \approx N S^2/12$, so $\sigma_{\hat r} \approx \sigma\sqrt{12/(N S^2)}$: doubling the span is four times as valuable as doubling the number of epochs.

**Correlated errors.** If the epoch errors share a common component (covariance matrix $\mathbf{C} = \sigma_w^2 \mathbf{I} + \sigma_c^2 \mathbf{1}\mathbf{1}^\top$ for a fully common bias $\sigma_c$), generalized least squares gives $\hat{\boldsymbol\beta} = (\mathbf{A}^\top \mathbf{C}^{-1} \mathbf{A})^{-1} \mathbf{A}^\top \mathbf{C}^{-1} \mathbf{z}$ with $\mathbf{A} = [\mathbf{1}, \mathbf{t} - \bar t]$. Because the common bias is orthogonal to the centred time column, it leaves $\hat r$ and $\sigma_{\hat r}$ unchanged and inflates only the intercept — which is the formal statement that a shared datum bias does not corrupt a rate but does corrupt an absolute height. Temporally correlated noise that is *not* common (e.g. a first-order autoregressive error with coefficient $\phi$ between consecutive epochs) does inflate the rate variance, approximately by $(1+\phi)/(1-\phi)$ for long series; GNSS time-series practice models this as flicker or random-walk noise, and MIDAS (Blewitt et al. 2016) sidesteps it with a median of pairwise slopes robust to steps and outliers.

> **Try it.** Fit a rate to a short elevation time series with and without a shared bias term and confirm that the rate estimate is insensitive to the common bias while its intercept is not.
>
> ```python
> import numpy as np
> t = np.array([2008.8, 2014.2, 2017.6, 2021.5])          # decimal years
> z = np.array([1.512, 1.478, 1.455, 1.431])              # m, mean over a stable plot
> sig_w, sig_c = 0.03, 0.05                               # per-epoch random, shared bias
> A = np.column_stack([np.ones_like(t), t - t.mean()])
> C = sig_w**2*np.eye(4) + sig_c**2*np.ones((4, 4))
> Ci = np.linalg.inv(C)
> N = A.T @ Ci @ A
> beta = np.linalg.solve(N, A.T @ Ci @ z)
> cov = np.linalg.inv(N)
> print(f"rate = {beta[1]*1000:.1f} ± {np.sqrt(cov[1,1])*1000:.1f} mm/yr")
> print(f"intercept σ = {np.sqrt(cov[0,0])*1000:.0f} mm (vs {sig_w/2*1000:.0f} mm if no shared bias)")
> ```
>
> Expected outcome: rate ≈ −6.4 ± 3.2 mm/yr, identical to the ordinary least-squares value, while the intercept uncertainty grows from ~15 mm to ~52 mm because of the shared 50 mm bias.

## Validation & uncertainty

The uncertainties specific to this chapter are uncertainties about *time*, and they propagate into elevation through rates.

**Errors in the measurement time.** A DEM whose acquisition date is recorded as the project year rather than the flight date carries a date uncertainty of up to ±6 months; multiplied by a seasonal amplitude of 10 cm this is the full seasonal cycle, and multiplied by a secular rate of 1 cm/yr it is ±5 mm — negligible for the second, dominant for the first. Validate by recovering per-flight-line dates from the point cloud (LAS GPS time, [Chapter 6](ch06-time-as-coordinate.md)) and from the survey report, and by checking that the mosaic's per-pixel date raster, if any, agrees with them.

**Errors in the reference epoch.** A coordinate propagated with the wrong epoch, or not propagated at all, is in error by the velocity times the epoch mistake: 7 cm/yr × 5 yr = 35 cm horizontally in Australia; 1–3 mm/yr vertically in a plate interior, 10 mm/yr in GIA centres, 10–100 mm/yr in subsiding cities. Validate by transforming a handful of CORS coordinates through the same pipeline as the data and comparing with the published time series; a residual that grows linearly with the date difference is an epoch error.

**Errors in the assumed rate.** The decision rule of §37.7 is only as good as $\hat r$ and $\sigma_r$. Published VLM rates from InSAR are relative to a reference area that may itself be moving; from CORS they are point values that may not represent the surrounding terrain (a station on a deep-piled building does not subside with the shallow sediment around it); from tide gauges they are the difference between relative and absolute sea-level trends with their own decadal variability. State the source and the spatial footprint of the rate used.

**Reporting.** For any multi-epoch product, report: acquisition date range per epoch; coordinate reference epoch per epoch; co-registration method and residuals over stable terrain; per-epoch vertical σ and its source; the LoD used; the phase (season, tide stage) of each epoch; and the rate uncertainty including the systematic component. For any single-epoch product offered for a use with a known tolerance, report the acquisition date and a pointer to regional VLM so the user can apply the decision rule.

> **Uncertainty budget.** Age-related vertical error of a 2011 coastal DTM used in 2026 (15 years), subsiding plain.
>
> | Component | Magnitude (1σ, 2026) | Source |
> |---|---|---|
> | DEM vertical error at acquisition | 7 cm | NVA report |
> | Secular subsidence 8 ± 2 mm/yr × 15 yr | 12 cm (systematic), ± 3 cm | InSAR/CORS |
> | Seasonal phase mismatch vs intended use | ± 3 cm | Soil moisture, vegetation |
> | Tidal datum epoch change since acquisition | 6 cm (systematic, local) | NOAA datum sheet |
> | Episodic (none known) | 0 | Event catalog |
> | **Total systematic offset** | **≈ 18 cm** (DEM now too high relative to current MSL) | |
> | **Total random (RSS)** | **≈ 8 cm** | |
>
> The systematic part dominates and is correctable — if the user knows the dates and rates. Uncorrected, this DEM overstates freeboard by about 18 cm.

## Software

**Open source:** **xdem** (Python; DEM co-registration, differencing, and spatial-statistics-based uncertainty — the reference implementation for Chapters 40–41); **py4dgeo** (Python/C++; M3C2, M3C2-EP, and 4D object-by-change analysis for point-cloud time series); **GMT** (`gmtregress`, `grdmath`, `velo` for velocity fields and time-series fits); **PROJ ≥ 7** (point-motion operations, deformation-model grids, `cct` with `t_epoch`; caveat: epoch handling depends on correctly specified `+t_epoch` and grid availability, and silently does nothing if the epoch is omitted); **pyproj** (Python bindings exposing the same, including `Transformer` with 4D coordinates); **MIDAS** and **Hector** (GNSS time-series rate estimation with robust or coloured-noise models); **GDAL** (`gdal_calc.py`, `gdal_rasterize` for per-pixel date rasters and rate grids).

**Free but closed:** **HTDP** (NGS; time-dependent positioning for the U.S. and its plates; the velocity model is open, the Fortran source is distributed, but the model is NGS's and is being superseded by IFVM); **Coulomb** and **COSI-Corr** are listed in [Chapter 39](ch39-earthquakes-volcanoes-landslides.md).

**Commercial:** **Trimble Business Center** and **Leica Infinity** (HTDP/NZGD2000/GDA2020 time-dependent transformations in survey workflows; caveat: the deformation-model version in use is often not surfaced in reports); **Esri ArcGIS Pro** (raster time-series tools, change detection; caveat: dynamic-datum epoch support arrived late and partially — verify how coordinate epochs are carried).

## Standards & guides

- **ISO 19111:2019** *Geographic information — Referencing by coordinates* (3rd ed.) — defines dynamic datums, coordinate epochs, and point-motion operations; the normative basis for time-dependent coordinates in metadata.
- **IERS Conventions (2010)**, IERS Technical Note 36 (Petit & Luzum, eds.) — models for solid-Earth tides, ocean and atmospheric loading, and the ITRF station-motion model used to define "when" a coordinate is valid.
- **NOAA/NOS CO-OPS tidal datum epoch policy** — NOAA Special Publication NOS CO-OPS 1 (*Tidal Datums and Their Applications*, 2000) and the NTDE update notices; governs the 19-year epoch and its regional exceptions.
- **ISO 19115-1:2014** *Metadata — Fundamentals* — temporal extent elements for acquisition start/end.
- **STAC specification** (1.0, 2021) — `datetime`, `start_datetime`, `end_datetime` conventions for assets with temporal extent.
- **IOGP Guidance Note 373-25** *Coordinate transformations with time-dependent parameters* — practitioner guidance on epochs in Helmert transformations (detailed in [Chapter 38](ch38-plate-motion-and-vlm.md)).

## Pitfalls

- **Treating a decades-old benchmark elevation as current in a subsiding area** → published heights have no expiry date printed on them → check the NGS datasheet's adjustment date and the regional VLM rate; multiply before you use.
- **Comparing DEMs across a tidal-epoch change and attributing the step to geomorphic change** → the datum shift is in the title block, not the data → identify the tidal epoch of each product and apply the published datum relationship.
- **Trend analysis on two epochs** → two points always define a line → with fewer than three epochs, report a difference with its LoD, not a rate with a confidence interval; with three or more, test for seasonality before fitting.
- **Mixing coordinates referenced to different epochs within one survey** → base-station coordinates from an old datasheet, rover in current ITRF via PPP → propagate everything to one epoch in one frame before adjustment; a residual proportional to date difference is the tell.
- **Taking the project year as the acquisition date** → metadata convenience → recover flight dates from GPS time in the point cloud.
- **Differencing mosaics without per-pixel dates** → the mosaic looks like one surface → build the date raster; express change as rate; expect seams.
- **Averaging epochs to beat down systematic error** → the $1/\sqrt{N}$ intuition → identify which error components are shared and exclude them from the averaging claim.
- **Choosing cadence from the budget cycle** → annual funding, annual flights → if the process is seasonal, fix the phase; if episodic, invest in baseline currency rather than cadence.
- **Assuming "static datum" means static ground** → the datum's convention is mistaken for a physical claim → read the datum definition; look up the deformation model that goes with it.
- **Confusing processing date with acquisition date** → reissued products carry new dates → read lineage; a "new" DEM may be old data on a new geoid.

## Key takeaways

- Every elevation has a time; every datum has an epoch; every use has a tolerance. The three together determine whether a DEM is valid.
- Place each process on the amplitude–period map before designing a survey; a survey is a detectable-range rectangle on the same map.
- Fast transients are large and must be removed; slow secular signals are small and accumulate; episodic signals cannot be scheduled.
- Sample at least twice per period of the fastest process you cannot model, or hold the phase fixed; two epochs are a difference, not a trend.
- Averaging reduces random error as $1/\sqrt{N}$ and systematic error not at all; doubling the span is worth four times doubling the epochs for a rate.
- Record acquisition start/end, per-pixel dates in composites, coordinate reference epoch, vertical realization, tidal epoch, and processing version — separately.
- Declare a DEM out of date when rate × age plus episodic displacement exhausts the tolerance left after measurement error; different uses give different lifetimes for the same file.
- Choose survey cadence from the process you need to see, not from budget cycles alone.

## References

- Altamimi, Z., Rebischung, P., Métivier, L. & Collilieux, X. (2016). ITRF2014: A new release of the International Terrestrial Reference Frame modeling nonlinear station motions. *Journal of Geophysical Research: Solid Earth*, 121(8):6109–6131. doi:10.1002/2016JB013098
- Altamimi, Z., Rebischung, P., Collilieux, X., Métivier, L. & Chanard, K. (2023). ITRF2020: an augmented reference frame refining the modeling of nonlinear station motions. *Journal of Geodesy*, 97:47. doi:10.1007/s00190-023-01738-w
- Anders, K., Winiwarter, L., Lindenbergh, R., Williams, J. G., Vos, S. E. & Höfle, B. (2020). 4D objects-by-change: Spatiotemporal segmentation of geomorphic surface change from LiDAR time series. *ISPRS Journal of Photogrammetry and Remote Sensing*, 159:352–363. doi:10.1016/j.isprsjprs.2019.11.025
- Blewitt, G., Kreemer, C., Hammond, W. C. & Gazeaux, J. (2016). MIDAS robust trend estimator for accurate GPS station velocities without step detection. *Journal of Geophysical Research: Solid Earth*, 121(3):2054–2068. doi:10.1002/2015JB012552
- Brasington, J., Langham, J. & Rumsby, B. (2003). Methodological sensitivity of morphometric estimates of coarse fluvial sediment transport. *Geomorphology*, 53(3–4):299–316.
- Dixon, T. H., Amelung, F., Ferretti, A., Novali, F., Rocca, F., Dokka, R., Sella, G., Kim, S.-W., Wdowinski, S. & Whitman, D. (2006). Subsidence and flooding in New Orleans. *Nature*, 441:587–588. doi:10.1038/441587a
- Eitel, J. U. H., Höfle, B., Vierling, L. A., Abellán, A., Asner, G. P., Deems, J. S., Glennie, C. L., Joerg, P. C., LeWinter, A. L., Magney, T. S., Mandlburger, G., Morton, D. C., Müller, J. & Vierling, K. T. (2016). Beyond 3-D: The new spectrum of lidar applications for earth and ecological sciences. *Remote Sensing of Environment*, 186:372–392. doi:10.1016/j.rse.2016.08.018
- Galloway, D. L. & Burbey, T. J. (2011). Review: Regional land subsidence accompanying groundwater extraction. *Hydrogeology Journal*, 19(8):1459–1486. doi:10.1007/s10040-011-0775-5
- Gesch, D. B. (2018). Best practices for elevation-based assessments of sea-level rise and coastal flooding exposure. *Frontiers in Earth Science*, 6:230. doi:10.3389/feart.2018.00230
- Interagency Performance Evaluation Task Force (IPET) (2009). *Performance Evaluation of the New Orleans and Southeast Louisiana Hurricane Protection System*, Final Report, Vol. II (Geodetic Vertical and Water Level Datums). U.S. Army Corps of Engineers.
- International Organization for Standardization (2019). *ISO 19111:2019 Geographic information — Referencing by coordinates*. Geneva: ISO.
- NOAA National Ocean Service (2000). *Tidal Datums and Their Applications*. NOAA Special Publication NOS CO-OPS 1. Silver Spring, MD.
- Petit, G. & Luzum, B. (eds.) (2010). *IERS Conventions (2010)*. IERS Technical Note No. 36. Frankfurt am Main: Verlag des Bundesamts für Kartographie und Geodäsie.
- Wheaton, J. M., Brasington, J., Darby, S. E. & Sear, D. A. (2010). Accounting for uncertainty in DEMs from repeat topographic surveys: improved sediment budgets. *Earth Surface Processes and Landforms*, 35(2):136–156. doi:10.1002/esp.1886

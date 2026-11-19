# UNOLS Research Cruise — Demobilization, Processing & Validation

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `unols-research-cruise` | **Platform / Vessel / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

This phase closes physical vessel stability records, **enforces a project raw-data custody handoff BEFORE any science party disembarks** (ensuring 100 % raw streams enter the operator's `R2R` ingestion pipeline), governs safe crane offload, off-hire restoration, permit closeouts, and directs reproducible shoreside `PPK/PPP ERS` and `CUBE` validation through `NCEI`/`DCDB` archival.

---

## 1. End-of-Cruise Closure & Mandatory Pre-Disembarkation Raw Custody Gate (Onboard)

- [ ] **[GATE]** **Record end-of-cruise static pier draft marks, ambient water density, and tank closure soundings:** Immediately upon securing alongside at the demobilization pier, read port/stbd forward, midships, and aft draft marks, sample pier water density (`kg/m^3`), and obtain final Chief Engineer fuel, freshwater, and ballast tank volumes to close total cruise buoyancy change $\Delta m / (\rho_w A_{\text{WP}}) + \Delta z_\rho$ against departure $t_0$. — *Threshold:* End-of-leg draft measurement precision `<= 0.02 m` (`1σ`); net cruise buoyancy/waterline trajectory closed within `<= 0.03 m` (`1σ`) across tank soundings vs mark delta. — *Evidence:* Co-signed Chief Mate + Mapping Lead Final Draft & Fuel Closure Log ([09-resources-and-templates.md](09-resources-and-templates.md)). — *Ref:* [sec-07-08.md](../../gemini4/book/ch-07/sec-07-08.md)
- [ ] **[COND]** **Execute an end-of-cruise crossline or calibration check (*Trigger:* Extended `> 14 d` cruise, suspected pole movement, or severe storm encounter):** Acquire a final orthogonal crossline tie across the initial day-1 box or pier-approach reference patch before terminating acoustic logging to bound total temporal roll/draft drift. — *Threshold:* End-of-cruise minus start-of-cruise mean vertical difference `<= 0.25 %` of depth (`bias <= 0.1 * TVU_max`). — *Evidence:* Start-vs-End Repeat Line Difference Stats. — *Ref:* [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md)
- [ ] **[GATE]** **Complete 100 % Raw Data, Metadata, `SVP` & Calibration Custody Handoff BEFORE Disembarking:** Transfer and verify `100 %` of raw datagrams (`.kmall`/`.all`/`.s7k`, `WCI`, `SBP`, `ADCP`, `EK80`), raw navigation/attitude (`.000`/`T04`), all `MVP`/`CTD`/`XBT`/`SVP` casts, vessel offset survey (`VSR`), `MAC` baseline, signed physical/digital watch + SVP + draft logs, and `sha256sum` manifests to both the Lead Marine Tech's operator distribution drive (feeding post-cruise **`R2R`** breakout & ingest) and the PI's two independent portable drives **BEFORE any member of the science mapping team steps off the gangway**. — *Threshold:* `100 %` raw file parity (`0` missing timestamps, `0` SHA-256 mismatches) attested by **dual-signed Project Raw Custody Receipt** before gangway departure. — *Evidence:* Dual-Signed Custody Receipt ([00-README-and-signoff.md](00-README-and-signoff.md)) + Operator/R2R Transfer Verification Log. — *Ref:* [ch50-archiving-and-provenance.md](../../fable/chapters/ch50-archiving-and-provenance.md)
- [ ] **[GATE]** **Submit UNOLS Post-Cruise Assessment Report (`PCAR`) in `MFP`:** Chief Scientist completes the `PCAR` evaluation of vessel facilities, Marine Tech support, `MBES`/`MVP` acoustic performance, and safety/incident compliance independently alongside the Ship Master and Lead Marine Tech `PCAR`s. — *Threshold:* Chief Scientist `PCAR` submitted in `mfp.us` within `<= 7–30 d` of disembarkation. — *Evidence:* `MFP` `PCAR` Confirmation PDF. — *Ref:* [09-resources-and-templates.md](09-resources-and-templates.md)

---

## 2. Crane Offload, Off-Hire Deck Inspection, Washdown, Customs & Permit Closeouts

- [ ] **[GATE]** **Execute RVSS Appendix B crane/rigging offload & signed Off-Hire Deck/Lab Condition Walkthrough:** Conduct crane/forklift van offload under Master/Marine Tech rigging plan (`RVSS 11th Ed.` `SWL` margins verified, taglines manned, exclusion zones roped off), plug all exposed `0.61 m` UNOLS deck bolt sockets, repair any science-caused deck paint/weld marks, sweep lab benches, and obtain Marine Superintendent off-hire sign-off before stopping the vessel charter clock. — *Threshold:* `0` rigging incidents; `100 %` off-hire restoration punch-list items signed cleared by Vessel Rep before crew release. — *Evidence:* Co-signed Port Off-Hire & Deck Condition Certificate. — *Ref:* [sec-07-04.md](../../gemini4/book/ch-07/sec-07-04.md)
- [ ] **[GATE]** **Complete washdown, `DGR 2026`/`IMDG` battery return, `ATA Carnet`, `LNM` cancellation & permit reports:** Freshwater-rinse portable over-side poles, `MVP` fish/winch, `SVS`, and `CTD` frames to purge biofouling/salt; pack return batteries under **`IATA DGR 67th Ed. (2026)`** (`UN 3480 PI965 CAO` & `UN 3481 PI966 <= 30 % SoC`, `UN 3090 CAO`), **`IMO IMDG Code`**, and `49 CFR 171–180` with `SDS` and `UN 38.3` packets; stamp **ATA Carnet** re-exportation vouchers; cancel any active **Local Notice to Mariners (`LNM`)** or temporary mooring/buoy notices; and file post-cruise **`MMPA`/`IHA` `90-day` MMO monitoring report** plus **`UNCLOS Art. 249` preliminary cruise report (`<= 30 d`)**. — *Threshold:* `100 %` Carnet serials stamped at exit customs, `100 %` `DGD`/`IMDG` packs certified, `LNM` cancellation logged, and `Art. 249`/`MMPA` reporting deadlines tracked. — *Evidence:* Stamped Carnet Sheet, Carrier `DGD`s, `LNM` Cancel Confirmation & Filed `Art. 249`/`IHA` Receipts. — *Ref:* [ch68-legal-issues.md](../../fable/chapters/ch68-legal-issues.md)

---

## 3. Shoreside Reprocessing: `SBET`, Delayed Heave vs `PPK/PPP ERS`, Ray-Tracing & `CUBE`

- [ ] **[GATE]** **Pin processing software versions, antenna models, and datum transformation grids:** Lock an immutable container or Conda environment (`MB-System`, `Kluster`, `Qimera`, `CARIS`, `POSPac`, `PROJ`, `GDAL`), pinned `igs20.atx` PCV/PCO table, and exact named geoid / `VDatum` / `GGXF` transformation grid hashes inside the provenance repository. — *Threshold:* Exact software versions, grid SHA-256 digests, and `PROJ` pipeline strings recorded so reprocessing is `100 %` reproducible. — *Evidence:* `environment.yml` / `manifest_env.txt` archived in processing repo. — *Ref:* [ch29-processing-pipelines.md](../../fable/chapters/ch29-processing-pipelines.md)
- [ ] **[GATE]** **Compute `PPK` / `PPP-AR` `SBET` and reconcile Non-Causal Delayed Heave vs Ellipsoidally Referenced (`ERS`) Vertical Reduction:** Process raw `.000`/`T04` files in `POSPac MMS` (exporting 17-double binary `SBET` with explicit `GPS week` since `SBET` omits week number!), evaluate **non-causal zero-phase `TrueHeave` / Delayed Heave** (eliminating `2–3 Tc` turn heave hooks) for conventional tide-reduced surveys vs **`PPP-AR` / `PPK` `ERS`** using `h = H + N = z_CD + SEP = SEP - d_CD` (`SEP = N + TSS + ΔZ_(LMSL->CD)`), enforcing `allow_ballpark=False` and auditing the `VDatum` inverted `TSS` sign (`TSS_VDatum = -TSS`). — *Threshold:* Forward–backward GNSS/INS trajectory separation `<= 0.05 m` vertical `1σ` (`PPK` shelf) / `<= 0.15 m` (`PPP-AR` blue water); `0` residual turn heave-hook artifacts `> 0.05 m` (`95 %` shelf) / `> 0.25 m` (deep). — *Evidence:* `POSPac` Forward–Backward Separation Plot + verified `pyproj` pipeline output. — *Ref:* [sec-03-02.md](../../gemini4/book/ch-03/sec-03-02.md)
- [ ] **[GATE]** **Re-apply full Circular-Arc `c(z)` Ray-Tracing, Tuck/Barrass Squat, and Fuel-Burn Waterline:** Recompute acoustic ray bending across quality-controlled `MVP`/`CTD`/`XBT` + `WOA`-spliced profiles (verifying `1/g_k` signed curvature convention across every layer), apply dynamic **Tuck/Barrass** squat and linearly interpolated cruise fuel-burn draft curves (`z_waterline(v,h,t)`), and verify outer-beam smile/frown reduction across swath overlaps. — *Threshold:* Reprocessed outer-beam (`55°–60°`) refraction curl `<= 0.20 %` of water depth (`<= 8 m` at `4,000 m`); zero uncompensated fuel-burn trend across cruise days `1..N`. — *Evidence:* Pre-vs-Post SVP Re-Raytrace Crossline Diff Report. — *Ref:* [sec-10-04.md](../../gemini4/book/ch-10/sec-10-04.md)
- [ ] **[GATE]** **Build `CUBE`/`CHRT` Uncertainty Grids (`float64` / shifted UTM) & pass `HydrOffice QC Tools`:** Generate depth-band `CUBE` hypotheses and designated soundings using `float64` coordinates or a shifted local UTM false origin (avoiding `float32` `0.25–0.5 m` ulp grid quantization stair-stepping on 7-digit UTM northings), and run **`HydrOffice QC Tools`** (flier finder, holiday finder, `IHO S-44 Ed. 6.2.0` [Oct 2024; core Table 1 `TVU`/`THU` `a`/`b` values unchanged from `Ed. 6.1.0`, adding `§3.8` seabed characteristics] / `HSSD` TVU compliance grid, grid QA). — *Threshold:* `0` unverified fliers, `0` unintended coverage holidays (`<= 1–2 %` cells allowed only in documented steep cliff shadows), and `>= 95 %` grid nodes passing governing `TVU_max`. — *Evidence:* `HydrOffice QC Tools` HTML/PDF Summary Report. — *Ref:* [ch47-file-formats.md](../../fable/chapters/ch47-file-formats.md)

Verify vertical datum transforms cleanly without runtime `ProjError`: use `EPSG:7912 -> EPSG:4326+3855` (`EGM2008` `+z up`) with `allow_ballpark=False` for open-ocean UNOLS surveys, and an explicit `+proj=pipeline` grid shift (`+step +proj=vgridshift`) or verified algebraic `SEP` conversion (`d_CD = SEP - h_ellip`) for coastal `MLLW` work:

```python
# Verified pyproj 3.7+ open-ocean EGM2008 transform + coastal VDatum pipeline/SEP check
import pyproj

# 1. Open-ocean UNOLS: ITRF2014 3D (EPSG:7912) -> WGS 84 + EGM2008 orthometric height (+z up, EPSG:4326+3855)
tf_ocean = pyproj.Transformer.from_crs(
    "EPSG:7912",
    "EPSG:4326+3855",
    always_xy=True,
    allow_ballpark=False,  # Hard fail if geoid grid is unavailable!
)
lon, lat, h_ellip = -124.5000, 44.6000, -18.420
x_out, y_out, h_egm08 = tf_ocean.transform(lon, lat, h_ellip)
print(f"Open-ocean EGM2008 height (+z up, m): {h_egm08:.3f}")

# 2. Coastal Charting (MLLW +d down): use explicit +proj=pipeline with local VDatum SEP grid:
#    pipeline = "+proj=pipeline +step +proj=vgridshift +grids=vdatum_sep_mllw.tif +step +proj=axisswap +order=1,2,-3"
#    tf_mllw = pyproj.Transformer.from_pipeline(pipeline)
# Algebraic sign check: z_CD = h_ellip - SEP = -d_CD  =>  d_CD (+d downward, m) = SEP - h_ellip
sep_m = -22.150  # Verified SEP = N + TSS + dZ_(LMSL->MLLW) from VDatum (watch TSS_VDatum = -TSS!)
d_mllw = sep_m - h_ellip
print(f"Coastal MLLW depth (+d down, m): {d_mllw:.3f}")
```

---

## 4. Terrain Co-Registration, Spectral/Hillshade Audit & Final Archival Deposit

- [ ] **[GATE]** **Execute `Nuth & Kääb (2011)` 3D co-registration, 4-azimuth hillshade/2D FFT audit & White-Ribbon overlap check:** Compute slope-aspect cosine co-registration fit $\Delta z / \tan\alpha = a\cos\psi + b\sin\psi + c\cot\alpha$ (`+z ↑` elevation convention, downslope azimuth $\psi = \operatorname{atan2}(-\partial z/\partial x, -\partial z/\partial y)$) against overlapping archive `MBES` or `BATHY` lidar, inspect `45°/135°/225°/315°` shaded relief plus `2D FFT` spectrum for periodic heave-hook or roll-wobble peaks, and verify coastal **White-Ribbon** tie across multi-modal platforms ([multimodal-white-ribbon.md](../_shared/multimodal-white-ribbon.md)). — *Threshold:* Horizontal co-registration shift `<= 0.5 * THU_95`; white-ribbon overlap `95 %` difference `<= sqrt(TVU_A^2 + TVU_B^2)`; `0` visible striping artifacts in `4-azimuth` hillshades. — *Evidence:* `4-Azimuth` Hillshade PNGs + `Nuth & Kääb` Fit Plot + White-Ribbon Tie Report. — *Ref:* [sec-14-05.md](../../gemini4/book/ch-14/sec-14-05.md)
- [ ] **[GATE]** **Export `BAG FSD 2.0.1` / `IHO S-102 Ed. 3.0.0` / `GSF` / `COG`, attach license/embargo, and deposit to `NCEI`/`DCDB`:** Package deliverables (`BAG FSD 2.0.1` `+z up` + `IHO S-102 Ed. 3.0.0` `+d down` passing `S-158:102` schema validation + `COG` + `STAC`), bundle **`BagIt` (`RFC 8493`) + `PREMIS v3` + `ISO 19115-2` / `W3C PROV`** metadata explicitly declaring **Data License (`CC0` / `CC-BY-4.0` / `NSF Open`)** and **Embargo Expiration Date**, apply any required `UNCLOS Art. 249` / naval sanitization / `CARE-OCAP®` escrow mask, and obtain final accession confirmation from **NOAA NCEI**, **IHO DCDB**, and **Seabed 2030**. — *Threshold:* `100 %` `BagIt` (`bagit.py --validate`) and `S-158:102` pass; explicit license/embargo tags embedded; formal `NCEI`/`DCDB` accession DOI issued `<= 90–180 d` post-cruise. — *Evidence:* `bagit.py --validate` pass log, `S-158:102` Report & `NCEI`/`DCDB` Accession Receipt. — *Ref:* [sec-19-01.md](../../gemini4/book/ch-19/sec-19-01.md)

---

## Phase 07 Sign-Off

| Gate Verification Item | Phase Lead Initials & UTC | Independent Verifier Initials & UTC |
| :--- | :--- | :--- |
| Final pier draft closure, **`100 %` Raw Custody BEFORE disembark**, `PCAR`, `LNM`/`Art. 249` & Off-Hire | `____________` | `____________` |
| Pinned `SBET`/delayed heave/`PPK ERS`, ray-trace, `CUBE`/`HydrOffice`, `Nuth & Kääb` & licensed `NCEI`/`DCDB` DOI | `____________` | `____________` |

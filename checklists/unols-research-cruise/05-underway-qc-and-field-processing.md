# UNOLS Research Cruise — Underway QC & Field Processing

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `unols-research-cruise` | **Platform / Vessel / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

This phase runs continuously `24/7` underway. Watchstanders prevent multi-day silent losses caused by surface sound-speed jumps, bubble sweepdown, GNSS jamming/spoofing, unverified backups, or undetected shoals by running quantitative live and nightly checks.

---

## 1. 24/7 Watchstanding, Bridge Handover & Live `SIS`/`Qinsy` Acquisition QC

- [ ] **[GATE]** **Execute strict 15-minute overlapped Watch Turnover and Bridge-to-Lab coordination:** Conduct structured shift handover (`00:00`/`08:00`/`16:00` or `4/8` schedule) inspecting active line number, current `SVS` vs latest `SVP` delta, disk space (`>= 25 %` free on acquisition RAID), `POS MV` `GAMS`/`1PPS` status, upcoming turns, and Bridge speed/heading/traffic advisories before relieving watch. — *Threshold:* `100 %` shift turnovers signed by outgoing and incoming watch leads in the Watch Log ([09-resources-and-templates.md](09-resources-and-templates.md)); zero unattended acquisition watches (`<= 5 min` continuous visual scan gap). — *Evidence:* Completed physical/digital Watchstander Shift Log. — *Ref:* [ch26-survey-planning.md](../../fable/chapters/ch26-survey-planning.md)
- [ ] **[GATE]** **Monitor real-time `SIS` / `Qinsy` TPU grid and slope-coupled uncertainty (`Green / Yellow / Red`):** Display live swath `TVU_95` and outer-beam cross-track `THU_95` compliance layers continuously in the Main Lab against [template-error-budget.md](../_shared/template-error-budget.md); treat any sustained `Red` band (`TVU_95 > TVU_max`) or `> 10 %` holiday coverage gap on mainscheme overlap as an immediate re-run or speed/angle adjustment trigger. — *Threshold:* Zero unflagged `Red` TPU swaths exceeding `5` consecutive minutes without corrective action (`SVP` cast, swath angle trim, or line mark for re-run). — *Evidence:* Hourly `SIS`/`Qinsy` live-TPU diagnostic snapshots archived in daily QC folder. — *Ref:* [sec-13-03.md](../../gemini4/book/ch-13/sec-13-03.md)
- [ ] **[GATE]** **Detect and mitigate bubble sweepdown, acoustic cavitation, and `WCI`/backscatter SNR degradation:** Watch live swath waterfall, backscatter mosaic, and `WCI` displays for missing nadir beams, streaks of aerated dropouts in head seas, or midwater kelp/fish/gas-plume false bottom locks; coordinate immediately with Bridge to reduce speed by `0.5–1.0 m/s (1–2 kn)`, adjust ballast trim, or alter line heading `15°–20°` off head sea. — *Threshold:* Acoustic outer-beam/nadir dropout rate `<= 15 %` of valid swath width over `10 min` rolling average; `>= 20 %` sustained bubble dropout triggers immediate heading/speed adjustment or weather standby logged in [template-cost-ledger.md](../_shared/template-cost-ledger.md). — *Evidence:* Timestamped Watch Log intervention entry + before/after swath waterfall screenshots. — *Ref:* [ch20-sonar.md](../../fable/chapters/ch20-sonar.md)
- [ ] **[COND]** **Enforce GNSS spoofing, jamming (`C/N0`, `AGC`), and `GAMS` dropout protocols underway (*Trigger:* Operating within `500 km` of EW advisories, high-latitude aurora `Kp >= 5`, or unexplained `POS MV` heading jumps):** Monitor dual-antenna `GAMS` status, receiver carrier-to-noise (`C/N0`), Automatic Gain Control (`AGC`), and `POS MV` vs ship gyrocompass heading delta (`> 1.0°` divergence alert); lock ship ECDIS to radar/gyro dead-reckoning and flag affected lines for raw observable post-processing if `C/N0` spikes or drops `> 10 dB-Hz`. — *Threshold:* Zero unlogged GNSS jumps (`> 0.5 m` position jump or `> 0.3°` `GAMS` gap `> 60 s`); affected survey timestamps tagged `EW_SUSPECT` immediately. — *Evidence:* `POS MV` health log + GNSS anomaly entry in Watch Log. — *Ref:* [ch56-case-files.md](../../fable/chapters/ch56-case-files.md)

---

## 2. Real-Time Sound-Velocity Trigger & Seabed 2030 Transit Logging

- [ ] **[GATE]** **Trigger an immediate `MVP`/`XBT`/`CTD` cast when surface `|c_SVS - c_cast(0)| > 1.5–2.0 m/s` or outer-beam refraction curls:** Monitor real-time difference between hull `SVS` and surface layer (`0–5 m`) of the active `SVP` table; deploy `MVP` or launch an `XBT` immediately whenever `|c_SVS - c_cast(0)| > 1.5–2.0 m/s`, outer-beam overlap exhibits systematic frown/smile bias `> 0.25 %` of water depth (`10 m` at `4,000 m`), or hull thermosalinograph crosses `> 1.0 °C` SST front. — *Threshold:* Elapsed time from trigger exceedance to new `.asvp`/`.svp` cast applied in `SIS`/`Qinsy` `<= 30 min` (`MVP`) or `<= 45 min` (`XBT` drop + apply). — *Evidence:* Timestamped Cast & SVS Cross-Check Log ([09-resources-and-templates.md](09-resources-and-templates.md)). — *Ref:* [sec-13-03.md](../../gemini4/book/ch-13/sec-13-03.md)
- [ ] **[REC]** **Maintain continuous Seabed 2030 & `R2R` transit-mapping logging outside primary boxes:** During `> 200 m` transit legs between port and primary survey sites, keep hull `MBES` (`12/30 kHz`), `K-Sync`, `SVS`, and `POS MV` logging continuously (subject to coastal-state `UNCLOS Part XIII` / `MMPA` boundaries) with regular `XBT`/`MVP` updates every `4–8 h` or frontal crossings. — *Threshold:* `>= 95 %` of permitted open-ocean transit distance (`> 200 m` water depth) logged cleanly with valid `SVP` and `GAMS` lock. — *Evidence:* Daily Transit Coverage Shapefile / Ping Count Tally. — *Ref:* [ch28-reducing-cost.md](../../fable/chapters/ch28-reducing-cost.md)

---

## 3. Nightly (`24 h`) Field Processing, Crossline QA & 24 h `DTON` Reporting

- [ ] **[GATE]** **Run nightly (`24 h`) shipboard surface build, crossline junction QA & artifact audit:** Every `24 h` UTC, ingest raw `.kmall`/`.all`/`.s7k` files into `Qimera`, `CARIS HIPS`, `Kluster`, or `MB-System`, load delayed heave (where logged), apply latest `SVP` and fuel-burn waterline table, grid daily lines + crosslines (`4–5 %` design coverage), and compute crossline minus mainscheme difference statistics + 4-azimuth shaded-relief inspection. — *Threshold:* Crossline vs mainscheme outer-beam `95 %` difference `<= TVU_max` (`<= 0.5–1.0 % d` deepwater, within `S-44 Order 1a` on shelf); systematic outer-beam bias `<= 0.25 % d`; zero uncorrected `2–3 Tc` heave hooks or roll stripes before releasing ship from survey box. — *Evidence:* Nightly Crossline Diff Histogram (`NMAD`, `median bias`, `P95`) + 4-Azimuth Hillshade PNG reviewed by Lead. — *Ref:* [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md)
- [ ] **[COND]** **Inspect and transmit Danger to Navigation (`DTON`) reports within `24 h` (*Trigger:* Shelf/coastal survey `< 100–200 m` revealing uncharted shoal shallower than charted depth by `>= 10 %` or endangering vessel UKC):** Flag verified shoal sounding in `Qimera`/`CARIS`/`SIS`, cross-check against raw waveform/`WCI` to rule out fish/kelp fliers, confirm datum/draft/tide correction, and submit formatted `DTON` packet to Master and the cognizant national hydrographic office / **NAVAREA Coordinator** (`NOAA OCS`, `UKHO`, or host coastal-state charting authority). — *Threshold:* Confirmed shoal DTON transmitted within `<= 24 h` of acquisition (`immediately` by VHF/bridge if `< 5 m` under-keel risk to own ship). — *Evidence:* Timestamped DTON Report + Bridge/Hydrographic Office confirmation receipt. — *Ref:* [sec-24-01.md](../../gemini4/book/ch-24/sec-24-01.md)

Verify nightly `MB-System` + `GMT` crossline junction differences directly on the shipboard Linux workstation using a shared bounding region (`-R$REGION`), NetCDF output (`-G3`), and Gaussian weighted mean (`-F1`—avoiding shoal-biased `-F5` minimum!) so `grdmath` grids align identically (adapted from [ch25-calibration-infrastructure.md](../../fable/chapters/ch25-calibration-infrastructure.md)):

```bash
# Nightly shipboard crossline vs. mainscheme junction QA (MB-System + GMT)
REGION="-125.5/-124.5/44.2/45.0"  # Lock identical W/E/S/N domain across both grids
mbdatalist -F-1 -Idatamain.mb-1 > main.datalist
mbdatalist -F-1 -Idatacx.mb-1   > cross.datalist
mbgrid -Imain.datalist  -Omain_dayN  -R"$REGION" -A2 -E100/100/meters! -F1 -G3 -N
mbgrid -Icross.datalist -Ocross_dayN -R"$REGION" -A2 -E100/100/meters! -F1 -G3 -N
gmt grdmath cross_dayN.grd main_dayN.grd SUB = diff_dayN.grd
gmt grdinfo -L2 diff_dayN.grd

# Quantitative robust threshold check (guarding against empty crossline overlap)
python3 - <<'PY'
import numpy as np, subprocess, sys
vals = subprocess.check_output(["gmt", "grd2xyz", "diff_dayN.grd", "-sa", "-Z"])
dz = np.fromstring(vals.decode(), sep="\n")
if dz.size == 0:
    print("WARNING: No overlapping crossline/mainscheme cells in diff_dayN.grd", file=sys.stderr)
    sys.exit(1)
med = np.median(dz)
nmad = 1.4826 * np.median(np.abs(dz - med))
p95 = np.percentile(np.abs(dz), 95)
print(f"Crossline diff (m): n={len(dz)}, median_bias={med:.3f}, NMAD={nmad:.3f}, P95={p95:.3f}")
PY
```

---

## 4. Raw Data Immutability & 3-2-1 SHA-256 Backups

- [ ] **[GATE]** **Enforce write-once Raw Immutability and automated `3-2-1` SHA-256 daily backup verification:** Store native acquisition streams (`.kmall`/`.all`/`.s7k`, `.wcd`, `.asvp`/`.svp`, `.000`, `K-Sync`, `CTD`/`ADCP`/`SBP` raw) on a read-only mount (`chmod -R a-w` after file close) NEVER overwritten by processing edits; synchronize every `<= 12–24 h` to **Copy 1** (Ship NAS RAID), **Copy 2** (portable NVMe/SSD array in separate watertight rack), and **Copy 3** (offline **LTO-9** tape or second vault drive in separate compartment) verified by `sha256sum` / `BagIt` (`RFC 8493`). — *Threshold:* `100 %` raw files present across `>= 3` physical copies on `>= 2` distinct media types with `0` `sha256sum` mismatches at `24 h` verification. — *Evidence:* Daily `sha256sum -c` pass log + physical LTO/NVMe Vault Sign-Off. — *Ref:* [ch50-archiving-and-provenance.md](../../fable/chapters/ch50-archiving-and-provenance.md)
- [ ] **[GATE]** **Log daily fuel/water burn and ballast transfers in the Draft Ledger without silent mid-line offset jumps:** Record daily fuel burn (`~15–30 t/day` on Global/Ocean vessels) and any ballast transfer (`> 5 t`) with Chief Engineer; keep real-time `SIS`/`Qinsy` `z_waterline` constant (or update only at explicit documented line breaks logged in [09-resources-and-templates.md](09-resources-and-templates.md)) so shoreside processing never double-corrects step changes. — *Threshold:* `100 %` ballast transfers (`> 0.01 m` draft change) and daily tank burns logged within `<= 24 h`; `0` undocumented mid-line waterline edits. — *Evidence:* Updated Daily Draft, Fuel Burn & Squat Ledger. — *Ref:* [sec-07-08.md](../../gemini4/book/ch-07/sec-07-08.md)
- [ ] **[REC]** **Audit real-time backscatter waterfalls and `WCI` midwater scatterers each watch:** Inspect live geocoded backscatter swath mosaics for sudden `>= 3 dB` sector/nadir jumps (`CW`/`FM` transition or transducer fouling) and annotate dense fish schools, kelp canopies, or deep scattering layers (`DSL`) in `WCI` that risk false bottom detections. — *Threshold:* `100 %` sustained `>= 3 dB` backscatter step shifts or dense midwater false-bottom anomalies flagged with line/ping timestamps in Watch Log. — *Evidence:* Annotated Backscatter/WCI Watch Screenshot. — *Ref:* [ch20-sonar.md](../../fable/chapters/ch20-sonar.md)
- [ ] **[REC]** **Validate `SVP` cast monotonicity, pressure units, and `WOA` deep-tail continuity before activating in `SIS`/`Qinsy`:** Visually inspect every `MVP`/`CTD`/`XBT` curve before ingestion to catch thermocline spikes, surface air-bubble outliers, inverted pressure rows (`p_i >= p_{i+1}`), or abrupt `> 0.5 m/s` `WOA` tail-splice discontinuities. — *Threshold:* `0` inverted depths or surface outlier spikes loaded into live ray-tracer; splice continuity `<= 0.5 m/s` verified on every cast. — *Evidence:* QC'd Sound-Speed Profile Plot saved per cast ID. — *Ref:* [sec-10-04.md](../../gemini4/book/ch-10/sec-10-04.md)
- [ ] **[GATE]** **Verify companion `SBP`, `ADCP`, and underway `TSG`/meteorological stream time-sync and file integrity each watch:** Inspect `3.5 kHz`/`Chirp` `SBP` (`SEG-Y`/`JSF`), `ADCP` (`.STA`/`.ENR`), and shipboard `SCS`/`met` underway feeds every watch to verify monotonic UTC clock parity (`< 10 ms` drift vs `POS MV` master) and clean non-zero file closes. — *Threshold:* `0` silent logging freezes `> 15 min` across companion acoustic/oceanographic streams on any watch. — *Evidence:* Companion Stream Status Check row in Watchstander Shift Log. — *Ref:* [sec-32-02.md](../../gemini4/book/ch-32/sec-32-02.md)

---

## Phase 05 Sign-Off

| Gate Verification Item | Phase Lead Initials & UTC | Independent Verifier Initials & UTC |
| :--- | :--- | :--- |
| Daily watch logs, live TPU/bubble/GNSS-EW monitoring & `|SVS - cast(0)| <= 1.5–2.0 m/s` gate | `____________` | `____________` |
| Nightly `24 h` crossline junction QA (`NMAD`/`P95` pass), DTON & `3-2-1` SHA-256 backup logs | `____________` | `____________` |

# Underwater AUV Bathymetric & Subsea Mapping — Phase 5: Underway QC & Field Processing

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `underwater-auv` | **Platform / Vessel / Hull #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

---

## 1. Pre-Dive Deck BIT & Tethered Surface Wet Checks

- [ ] **[GATE]** Complete full **deck Built-In Test (`BIT`), INS coarse/fine dock alignment, and recovery-beacon readiness check** prior to crane lift:
  - INS alignment converged (`heading sigma <= 0.05–0.10°`), DVL dry-ping healthy, MBES/SAS/SBP test logs writing cleanly with free NVMe/SSD space `>= 1.5x` mission estimate.
  - All external recovery aids powered, battery-tested, and physically confirmed: **Iridium SBD** message test passed, **Argos** PTT active, **VHF RF direction-finding beacon** tone heard on bridge handheld, **Xenon strobe** flashing cleanly, and **acoustic emergency pinger** audible on deck hydrophone test box.
  - Acoustic release/drop-weight safety pin removed (`REMOVE BEFORE FLIGHT` flag logged) only at the rail immediately prior to launch.
  - *Evidence:* Signed Pre-Launch BIT & Pin-Pull Tally Sheet. *Ref:* [ch13-imu-ins.md](../../fable/chapters/ch13-imu-ins.md) (INS alignment); vehicle BIT & beacons per OEM manual and [External Regulatory Basis Register](./09-resources-and-templates.md#external-regulatory--standards-basis-register-non-handbook-authorities).
- [ ] **[GATE]** Execute **free-floating / tethered surface wet check** immediately upon entering the water before releasing the dive command:
  - **GNSS fix locked:** Differential/RTK surface position recorded (`PDOP <= 2.5`, velocity `<= 0.05 m/s` relative to drift) to seed the Kalman filter prior to submersion.
  - **Surface sound-speed check:** AUV `SVS` matches ship bucket/CTD `5 m` bin within **`<= 0.5–1.5 m/s`** (`> 2.0 m/s` divergence stops the dive for sensor purge/SVP check).
  - **Acoustic telemetry & USBL handshake:** Support ship locks two-way USBL range/bearing (`SNR >= 10 dB`) and verifies stable telemetry packet exchange.
  - **Visual ballast trim check:** Vehicle floats level at nominal waterline; no unexpected air bubbles streaming from pressure hulls, oil compensators, or connector boots.
  - *Evidence:* Wet-Check Pass Timestamp (`UTC`) in Watch Log. *Ref:* [ch14-positioning-beyond-gnss.md](../../fable/chapters/ch14-positioning-beyond-gnss.md), [sec-13-02.md](../../gemini4/book/ch-13/sec-13-02.md).
- [ ] **[REC]** Confirm final **LARS crane/sea-state Go/No-Go and Protected Species (`PSO/MMO`) clearance** immediately prior to hoisting: significant wave height `Hs <= 2.5–3.0 m`, tag-line crew positioned clear of swing arc, and **`30 min` (`60 min` in depths `> 200 m`) visual/acoustic mammal pre-watch + `>= 20 min` soft-start ramp** logged. *Evidence:* Bridge Launch Clearance Timestamp & PSO Log Entry. *Ref:* [ch69-security-sovereignty-privacy-ethics.md](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md), [ch26-survey-planning.md](../../fable/chapters/ch26-survey-planning.md).

---

## 2. Underway Acoustic Tracking, Innovation Residuals & Abort Gates

- [ ] **[GATE]** Monitor live **USBL / iUSBL innovation residuals (`z_meas - z_pred`)**, descent drift trajectory, depth vs pressure ceiling, and acoustic health telegrams throughout every dive. *Threshold:* USBL innovation residuals remain within `2–3 sigma` (`e.g., <= 0.3 %` of slant range `1 sigma` envelope); update shipboard track/speed to remain within optimal acoustic cone (`<= 30–45°` off vertical from vessel USBL head, avoiding prop-wash cavitation blanks). *Evidence:* Continuous USBL Tracking Strip Chart & Watch Log entries every `15–30 min`. *Ref:* [ch14-positioning-beyond-gnss.md](../../fable/chapters/ch14-positioning-beyond-gnss.md), [sec-05-04.md](../../gemini4/book/ch-05/sec-05-04.md).
- [ ] **[REC]** Watch acoustic quality and quick-look sonar logs for **deep scattering layers (`DSL`), hydrothermal gas plumes, steep-wall sidelobes, and double-echo multiples** falsely capturing bottom trackers, adjusting bottom-tracking gate windows or frequency filters before multi-dive contamination accumulates. *Evidence:* Water-Column / Tracker Gate Log Note. *Ref:* [ch20-sonar.md](../../fable/chapters/ch20-sonar.md), [sec-10-06.md](../../gemini4/book/ch-10/sec-10-06.md).
- [ ] **[GATE]** Enforce non-negotiable **underway abort triggers** without hesitation (via acoustic abort command or onboard autonomous fault rules):
  1. **Water-leak sensor trip** inside any electronics, battery, or motor pressure housing (`0 s` delay — immediate emergency drop-weight / abort).
  2. **Battery `SoC <= 20–30 %`** reserve floor, critical cell-overtemp (`>= 55–60 °C`), or unexplained rapid voltage sag.
  3. **Sustained DVL bottom-lock dropout** (`> 5–10 min` un-aided over rugged terrain) or INS divergence exceeding geofence safety buffer (`>= 50 %` toward keep-out boundary).
  4. **Acoustic comms blackout** exceeding mission timeout (`e.g., > 30–45 min` total silence despite optimal ship geometry) or repeated OAS obstacle-avoidance faults (`>= 3` consecutive stalls).
  - *Evidence:* Watch Officer Abort Action Log + Acoustic Command Receipt. *Ref:* [ch16-platforms.md](../../fable/chapters/ch16-platforms.md), [sec-13-03.md](../../gemini4/book/ch-13/sec-13-03.md).
- [ ] **[COND]** Trigger an **unscheduled shipboard CTD / SVP cast** (*Trigger:* Vessel transits a distinct ocean thermal/salinity front, surface SVS jumps `> 1.5–2.0 m/s` from the active SVP surface bin, or elapsed dive time exceeds `4–6 h` in stratified upper waters). *Threshold:* Log exact cast timestamp and ingest into post-dive ray-tracing queue immediately. *Evidence:* Updated SVP Cast Log. *Ref:* [sec-13-02.md](../../gemini4/book/ch-13/sec-13-02.md), [ch20-sonar.md](../../fable/chapters/ch20-sonar.md).

---

## 3. Recovery Lockout & Station-Hold Quick-Grid QC (BEFORE Leaving Station)

- [ ] **[GATE]** Enforce the **Recovery Thruster-Lockout Safety Gate**: confirm positive visual sighting (strobe/flags) + surface VHF/Iridium lock, send acoustic/RF **`THRUSTER SAFE / INHIBIT`** command, and verify physical propeller stop **BEFORE** launching RHIB, entering small-boat grapple range, deploying swimmer, or hooking crane/LARS recovery line. *Evidence:* Bridge/Deck Verbal & Logged `THRUSTER LOCKED` timestamp prior to hook-up. *Ref:* [ch16-platforms.md](../../fable/chapters/ch16-platforms.md) (LARS recovery ops); thruster hardware inhibit per OEM manual & `UNOLS RVSS`.
- [ ] **[GATE]** Perform a **deck IR thermal scan (`< 45–50 °C`) and external pressure/vacuum relief indicator check BEFORE cracking any main hull or battery hatches** right after deck recovery (catching flooded Li-ion `H_2` overpressure or hot-cell hazards prior to unbolting end-caps). *Evidence:* Post-Recovery Thermal/Pressure Check Entry on Deck Log. *Ref:* Vehicle OEM deck-safety manual & Li-ion `SDS`.
- [ ] **[GATE]** Run the **Immediate Post-Dive Quick-Grid, Outer-Beam Smile Check & DVL/USBL/SLAM Loop-Closure QC BEFORE the support ship releases station (`<= 2–4 h` post-recovery)**:
  1. **Holiday & overlap audit:** Grid all dive lines (`mbgrid` / `Kluster` / `Qimera`) at nominal resolution and verify `0 %` unmasked holidays inside the **planned survey polygon mask** (`<= 3 x 3` cell rule per `HSSD` or zero unaccounted acoustic dropouts).
  2. **Outer-beam refraction check:** Inspect cross-track profiles over flat bottom (`[-65°, -45°]` and `[+45°, +65°]` outer beams) for sound-speed "smile/frown" curvature (`bias <= 0.5 %` depth and within S-44 `TVU_95%` corridor).
  3. **DVL/USBL/SLAM loop-closure check:** Measure crossline vs mainscheme and adjacent tie-line differences (`|Delta z|` mean `<= 0.15 m`, `1 sigma <= 0.25–0.40 m`; horizontal feature mismatch `<= 2.0–3.0 m` prior to final `mbnavadjust`).
  4. **Re-run trigger:** If any holiday, uncorrectable outer-beam blowup, or DVL-INS/sonar gap fails spec, hold vessel on station and queue re-fly lines on the next dive.
  - *Evidence:* Quick-Grid Hillshade PNG, Crossline Residual Report, and **Station-Release Go/Re-Fly Sign-Off** logged against [template-error-budget.md](../_shared/template-error-budget.md). *Ref:* [ch26-survey-planning.md](../../fable/chapters/ch26-survey-planning.md), [ch15-slam.md](../../fable/chapters/ch15-slam.md), [sec-13-03.md](../../gemini4/book/ch-13/sec-13-03.md).
- [ ] **[GATE]** Audit **navigation & auxiliary sensor continuity (`INS / DVL / Pressure / SVP`)** on deck prior to approving vessel departure from station: verify `>= 95 %` bottom-track DVL lock during survey lines, uninterrupted Digiquartz pressure & `P_atm` logs, and zero unexpected `1PPS` timing drops (`0` missing navigation epochs). *Evidence:* Dive Navigation Completeness & DVL Lock Report. *Ref:* [ch13-imu-ins.md](../../fable/chapters/ch13-imu-ins.md), [sec-05-04.md](../../gemini4/book/ch-05/sec-05-04.md).
- [ ] **[REC]** Compute and apply **initial patch-test boresight offsets (`Delta t`, `Delta theta`, `Delta phi`, `Delta psi`)** immediately following Dive 1 (`solve_multibeam_patch_test` / `Kluster` / `Qimera`) before launching multi-day production lines so persistent angular misalignments are corrected in real-time quick-grids. *Evidence:* Dive 1 Patch-Test Convergence Screenshot. *Ref:* [sec-10-06.md](../../gemini4/book/ch-10/sec-10-06.md), [ch20-sonar.md](../../fable/chapters/ch20-sonar.md).

```python
# Station-Hold Quick-QC Snippet (check crossline Delta-z & polygon-masked holiday fraction)
import numpy as np


def station_hold_qc(
    dz_cross: np.ndarray, valid_poly_mask: np.ndarray, tvu_95_limit: float
) -> dict:
  """Evaluate post-dive crossline vertical consistency and grid completeness inside planned polygon.

  Note: dz_cross is a two-pass difference (sigma_dz = sqrt(2) * sigma_single), so checking
  1.96 * rmse <= tvu_95_limit serves as an intentionally conservative sqrt(2) station-hold gate.
  """
  dz = dz_cross[np.isfinite(dz_cross)]
  n = int(dz.size)
  mask = np.asarray(valid_poly_mask, dtype=bool)
  holiday_pct = float(100.0 * (1.0 - np.mean(mask))) if mask.size else 100.0
  if n < 2:
    return {
        "n": n,
        "holiday_pct": round(holiday_pct, 3),
        "pass_station_gate": False,
    }
  bias = float(np.mean(dz))
  sigma = float(np.std(dz, ddof=1))
  rmse = float(np.sqrt(np.mean(dz**2)))
  nmad = float(1.4826 * np.median(np.abs(dz - np.median(dz))))
  p95 = float(np.percentile(np.abs(dz), 95))
  pass_tvu = (1.96 * rmse <= tvu_95_limit) and (holiday_pct <= 0.5)
  return {
      "n": n,
      "bias_m": round(bias, 4),
      "sigma_m": round(sigma, 4),
      "rmse_m": round(rmse, 4),
      "nmad_m": round(nmad, 4),
      "p95_abs_m": round(p95, 4),
      "holiday_pct": round(holiday_pct, 3),
      "pass_station_gate": bool(pass_tvu),
  }
```

---

## 4. Immutable Raw Ingest, SHA-256 Manifest & 3-2-1 Shipboard Backup

- [ ] **[GATE]** Immediately ingest **100 % of raw AUV datagrams** (`.kmall`/`.all`/`.s7k`/`.xtf`/`.jsf`/optical frames), **navigation logs** (INS, DVL, Paroscientific pressure, surface GNSS), **USBL/LBL topside logs**, and **SVP casts** onto shipboard storage, verify **SHA-256 checksums**, and complete a **3-2-1 backup** (`3` copies, `2` distinct media — e.g., primary NVMe NAS + off-hull RAID/LTO tape, `1` physically isolated/fireproof-safe copy) **BEFORE formatting or wiping AUV SSD cartridges for the next dive**. *Threshold:* Byte-count & SHA-256 digest verification `100 %` match between AUV cartridge and both backup targets (`0` truncated/corrupted datagrams). *Evidence:* Verified `sha256sum` Manifest & Dive Backup Sign-Off. *Ref:* [ch50-archiving-and-provenance.md](../../fable/chapters/ch50-archiving-and-provenance.md), [ch47-file-formats.md](../../fable/chapters/ch47-file-formats.md).
- [ ] **[REC]** Append structured daily logs before watch turnover: dive number, launch/recovery UTC coordinates, surface/bottom sound speed, max depth, `SoC` start/end, USBL dropouts, `DTON` hazards noticed, standby/cost burn updated in [template-cost-ledger.md](../_shared/template-cost-ledger.md), and raw disk IDs. *Evidence:* Daily Dive Operations & Anomaly Log. *Ref:* [ch26-survey-planning.md](../../fable/chapters/ch26-survey-planning.md).
- [ ] **[COND]** Issue an immediate **Danger to Navigation (`DTON`)** report within **`24 h`** (*Trigger:* AUV discovers any uncharted shoal, pinnacle, sunken wreck, or pipeline hazard posing a threat to surface navigation per NOAA `HSSD` / national Hydrographic Office routing, typically in depths `< 40 m` or designated fairways). *Evidence:* NOAA `MCD` / National Hydrographic Office `DTON` submission receipt. *Ref:* [sec-24-01.md](../../gemini4/book/ch-24/sec-24-01.md), [ch62-navigation-and-charting.md](../../fable/chapters/ch62-navigation-and-charting.md).

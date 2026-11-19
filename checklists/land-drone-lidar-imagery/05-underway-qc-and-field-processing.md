# On-Land Drone (UAS) LiDAR + Imagery — Underway QC & Field Processing

> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `land-drone-lidar-imagery` | **Platform / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier:** `__________________`

---

## 1. Per-Battery Turnaround & In-Flight Telemetry Gates

- [ ] **[GATE]** **Per-Sortie Telemetry & Battery Health Check:** Immediately after landing each battery sortie, inspect GCS/aircraft telemetry before arming the next pack: confirm zero prolonged `FLOAT`/`SINGLE` gaps (`PDOP <= 3.0`, `>= 10` SVs), continuous `1–10 Hz` raw PPK logging, executed pre/post figure-8 maneuvers, steady line roll/pitch `< 20–25°`, resting cell voltage **`>= 3.65–3.70 V/cell`** (`>= 20–25 %` reserve), cell delta `< 0.05 V`, case temperature `< 50–55 °C`, and zero swelling; wait `>= 15–20 min` (`< 35 °C`) before charging. — *Evidence:* Initialed battery cycle log ([09 Template A](09-resources-and-templates.md)) + GCS telemetry checkoff. | *Ref:* [Ch. 12](../../fable/chapters/ch12-gnss.md), [Ch. 16](../../fable/chapters/ch16-platforms.md), [Ch. 18](../../fable/chapters/ch18-topographic-lidar.md).
- [ ] **[GATE]** **Per-Battery Sample Image Blur, Exposure & Hot-Shoe Event Audit:** Spot-check `5–10` nadir and oblique frames from each sortie on the field laptop: confirm zero blown target highlights or crushed shadows, crisp target/edge sharpness with **motion smear `<= 0.5 GSD`** ($v_g t_{\text{exp}} \le 0.5\,\text{GSD}$), clean optics, and exact **1:1 count parity** between imagery frames and GNSS `EventIn` timestamps. — *Evidence:* Sample frame QC log + `exif`/`EventIn` parity count check. | *Ref:* [Ch. 16](../../fable/chapters/ch16-platforms.md), [`gemini4` §7.3](../../gemini4/book/ch-07/sec-07-03.md).
- [ ] **[REC]** **Real-Time LiDAR Return & Strip Density Monitor:** Confirm multi-return canopy yield (`1st` vs `last`/ground pulse count), nominal PRF/scan rate, zero thermal throttles, and unobstructed `360°` / full-FOV scanner capture across every sortie. — *Evidence:* Vendor LiDAR monitor screenshot or `lasinfo` pulse-count summary. | *Ref:* [Ch. 18](../../fable/chapters/ch18-topographic-lidar.md).

---

## 2. Pre-Departure In-Field PPK, Tie-Point & Swath-Overlap Verification (Mandatory Before Leaving Site)

Never strike the GNSS base station or release the field crew until all three pre-departure verification gates below pass on site ([Ch. 26](../../fable/chapters/ch26-survey-planning.md), [Appendix G §G.2](../../fable/appendices/appendix-g-checklists.md)).

- [ ] **[GATE]** **In-Field PPK Trajectory Fix Ratio (`>= 95 %`) & Forward/Backward Separation:** Process field PPK trajectories (`RTKLIB rnx2rtkp` or vendor INS/PPK software) against the local site base (`<= 15 km`) on the field workstation before leaving site. Require **`>= 95 %` fixed integer ambiguities (`Q = 1`)** along active mapping lines (no `> 10–15 s` `FLOAT` outages over control), forward-backward separation **`< 2–3 cm` (`1σ`)**, and peak excursion **`< 5 cm`**. — *Evidence:* Saved `field_ppk.pos` summary stats (`Q=1 %`, max `sdu`) & F/B separation plot. | *Ref:* [Ch. 12](../../fable/chapters/ch12-gnss.md), [Ch. 13](../../fable/chapters/ch13-imu-ins.md).
- [ ] **[GATE]** **In-Field Coarse SfM Tie, Coverage & Radial-Dome Check:** Run a low/medium-resolution alignment pass (`OpenDroneMap --fast-orthophoto` or `COLMAP`/`Metashape` `1/4` preview) verifying zero image dropouts (`>= 80/70 %` realized overlap), `10–20°` oblique tie linkage across blocks, coarse DSM agreement `<= 5–10 cm` against `gcps.csv` with zero parabolic edge bow, and zero water-surface false tie spikes. — *Evidence:* Field SfM report PDF showing camera connectivity & coarse GCP residuals. | *Ref:* [Ch. 22](../../fable/chapters/ch22-photogrammetry-sfm.md), [`gemini4` §8.2](../../gemini4/book/ch-08/sec-08-02.md).
- [ ] **[GATE]** **In-Field LiDAR Swath Overlap, Holiday & Raw Strip-Step Check:** Generate a coarse LAS/LAZ swath mosaic (`PDAL` / vendor utility) confirming **`0 %` coverage holidays**, **`>= 25–30 %` realized sidelap**, `100 %` cross-strip overlap, and raw inter-swath open-flat vertical step **`<= 5–8 cm` `RMSDz`** (`<= 10–15 cm` mid-grade solid-state units prior to strip adjustment). — *Evidence:* `field_anpd_1m.tif` gap check raster + strip-difference visual overlay. | *Ref:* [Ch. 18](../../fable/chapters/ch18-topographic-lidar.md), [Ch. 26](../../fable/chapters/ch26-survey-planning.md).
- [ ] **[REC]** **Cross-Strip Roof/Road Profile Slice Check:** Slice at least two perpendicular `1–2 m` wide profile cross-sections across hard gable roofs or paved roads in a field viewer (`CloudCompare` / `PDAL`) to confirm zero broken lever-arm jumps (`> 10 cm`) before tearing down control. — *Evidence:* Annotated cross-section PNG saved in field QC folder. | *Ref:* [Ch. 25](../../fable/chapters/ch25-calibration-infrastructure.md).
- [ ] **[COND]** **In-Field Water-Glint & Dynamic Interference Watch:** *Trigger:* Flight block includes water margins, beaches, or active haul roads/work zones. Spot-check coastal edge tiles and road segments for specular water-glint false clouds or moving machinery, logging affected frame timestamps. — *Evidence:* Daily interference/transient frame range notes in field log. | *Ref:* [Ch. 27](../../fable/chapters/ch27-moving-and-transient-objects.md), [Ch. 34](../../fable/chapters/ch34-water-in-dems.md).

### Runnable Field QC Snippet (`RTKLIB` `.pos` Column `$10` Check + `PDAL` Count Grid)

```bash
# 1. Field PPK check (RTKLIB CLI) — columns: $1=date $2=time $6=Q(1=fix) $8=sdn $9=sde $10=sdu
rnx2rtkp -k field_uas_ppk.conf -o field_ppk.pos rover.obs base.obs nav.nav
awk '!/^%/ {tot++; if($6==1) {fix++; if($10>max_sdu) max_sdu=$10}} END {
  if (tot==0) {print "ERROR: zero epochs in field_ppk.pos"; exit 1}
  printf "PPK Fix: %.2f%% (%d/%d), Max Fixed Up-Std (sdu): %.3f m\n", 100*fix/tot, fix, tot, max_sdu
}' field_ppk.pos

# 2. Quick PDAL swath-density & overlap check (verify zero gaps and ANPD margin)
pdal merge strip_*.laz field_merged.laz
pdal translate field_merged.laz field_anpd_1m.tif \
  --writers.gdal.resolution=1.0 --writers.gdal.binmode=true --writers.gdal.output_type="count"
```

---

## 3. Daily Environment Log, Raw Immutability & Dual-Copy SHA-256

- [ ] **[REC]** **Daily Wind, Cloud, Transient-Object & Space-Weather Log:** Log hourly anemometer wind/gusts, barometric pressure (`hPa`, confirming home-zero drift resets), sun elevation/cloud shadow percentage, moving vehicles/cranes/cattle/vessels, and `Kp` geomagnetic index (`Kp < 5`, noting GNSS cycle slips). — *Evidence:* Completed daily environmental & transient log sheet. | *Ref:* [Ch. 12](../../fable/chapters/ch12-gnss.md), [Ch. 27](../../fable/chapters/ch27-moving-and-transient-objects.md).
- [ ] **[COND]** **Real-Time RF / GNSS `C/N0` & Spoofing Monitor:** *Trigger:* Site lies near military/quarry/urban RF emitters or anomalous position jumps occur. Monitor controller `C/N0` and AGC telemetry; pause flights immediately if `C/N0` drops `> 6–10 dB-Hz` across constellations or clock/coordinate offsets jump. — *Evidence:* Saved `C/N0`/AGC telemetry snapshot or RF anomaly log entry. | *Ref:* [Ch. 56 Case 56.19](../../fable/chapters/ch56-case-files.md), [Ch. 69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md).
- [ ] **[GATE]** **Raw Media Read-Only Immutability & Dual-Copy `SD -> Dual SSD SHA-256` Verification:** Engage SD write-protect tabs / mount media read-only (`-o ro`). Copy raw imagery, GNSS base/rover observables, IMU binaries, LiDAR streams, event files, and field photos to **two independent rugged SSDs** (`SSD_A`, `SSD_B`), verify identical **`sha256sum`** manifests across source and both SSDs, and confirm offsite/cloud sync (`3-2-1` rule) **before formatting any flight SD card**. — *Evidence:* Matching `sha256sum` logs (`source`, `SSD_A`, `SSD_B`) initialed by Verifier. | *Ref:* [Ch. 47](../../fable/chapters/ch47-file-formats.md), [Appendix G §G.2](../../fable/appendices/appendix-g-checklists.md).
- [ ] **[REC]** **Physical Separation & Overnight Transit Custody:** Transport `SSD_A` and `SSD_B` in physically separate crew bags/vehicles during transit and verify remote/cloud upload checksum confirmation before crew check-out. — *Evidence:* Custody separation sign-off + offsite cloud hash log. | *Ref:* [Appendix G §G.2](../../fable/appendices/appendix-g-checklists.md).
- [ ] **[GATE]** **Pre-Agreed Field Re-Fly & Abandonment Execution:** Trigger immediate in-window re-flight for any threshold breach (`PPK fix < 95 %`, F/B `> 5 cm`, missing `10–20°` obliques, LiDAR gap `> 1–2 m²`, blur `> 1 GSD`, uncompensated strip step `> 15 cm`, or unmasked specular glint), OR execute weather-abandonment trigger if forecast breaches [the cost ledger](../_shared/template-cost-ledger.md) standby cap; sign Gate **G-05** in [00-README-and-signoff.md](00-README-and-signoff.md). — *Evidence:* Re-fly completion record (or signed abandonment decision) + G-05 sign-off. | *Ref:* [Cost Ledger](../_shared/template-cost-ledger.md), [Ch. 26](../../fable/chapters/ch26-survey-planning.md).

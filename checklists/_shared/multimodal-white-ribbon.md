# Shared Guide 0.8 — Multi-Modal Coastal "White Ribbon" Synchronization

> **Purpose:** Coordinate concurrent or sequential land, intertidal, and marine platforms across the coastal **white ribbon** (the shallow nearshore strip—typically $0\text{–}10\text{ m}$ depth / $50\text{–}500\text{ m}$ wide depending on beach slope, qualitative per [Chapter 34](../../fable/chapters/ch34-water-in-dems.md) §34.8—where vessels risk grounding and NIR lasers are absorbed by water) so the merged Topo-Bathymetric DEM (TBDEM) achieves a **100–500 m empirically cross-checked intertidal overlap belt** (project target) without vertical datum cliffs or marine/air safety conflicts. Grounded in [Chapter 19](../../fable/chapters/ch19-bathymetric-lidar.md), [Chapter 34](../../fable/chapters/ch34-water-in-dems.md), [Chapter 48](../../fable/chapters/ch48-compositing.md), [Chapter 9](../../fable/chapters/ch09-vertical-datums.md), and [Gemini4 Sec. 13.2](../../gemini4/book/ch-13/sec-13-02.md).

---

## 1. Multi-Modal Coastal Tier & Role Matrix

| Asset Tier / Modality | Coastal Zone & Depth Envelope | Optimal Environmental Window | Key Limiting Failure Mode | Cross-Link to Modality Suite |
|---|---|---|---|---|
| **Tier 1 Screening:** ICESat-2 (`ATL03`/`ATL24`) & Optical SDB (`IHO B-13`) | Clear water $0\text{–}25\text{ m}$ (up to $\sim 1\text{ }Z_{sd}$ ICESat-2); bare beach | Low cloud, calm wave glint, clear water ($K_d$ low) | Sparse tracks; optical turbidity/dark seagrass false shoals | [Satellite Elevation](../satellite-elevation/00-README-and-signoff.md) |
| **Dry Beach & Intertidal:** Drone SfM/Lidar & Crewed ALS (`1064/1550 nm`) | Dunes down to exposed low-water line | **Within $1.5\text{ h}$ of predicted spring low water** (project window); sun $>30^\circ$; wind $<8\text{–}10\text{ m/s}$ (UAS) | Water absorption at $1064\text{ nm}$; wet-sand glint; Part 107 / airspace conflicts | [Land Drone](../land-drone-lidar-imagery/00-README-and-signoff.md) · [Land Aircraft](../land-aircraft-lidar-imagery/00-README-and-signoff.md) |
| **Land–Water Bridge:** Coastal Bathylidar (`532 nm + 1064 nm`) | Dry beach out to $1.5\text{–}3\text{ }Z_{sd}$ ($0.5\text{–}50\text{ m}$ clear water) | **Predicted spring low water** + **strict $30^\circ\text{–}45^\circ$ solar elevation** + calm sea / low surf foam | Surf-zone aeration void; turbidity plumes; $n_p/n_g$ refraction; `0–1 m` pulse overlap | [Coastal Bathylidar](../coastal-bathylidar/00-README-and-signoff.md) |
| **Nearshore Acoustic:** ASV / USV & Shallow Launch MBES | Shallow flats up to $z_{\text{high}} - d_{\min}$ seaward to shelf | **Predicted spring high water** (for intertidal flats) + Beaufort $\le 3\text{–}4$; SVP casts | Minimum keel/draft depth; surf grounding; high angular chop; stale SVP smile | [Autonomous Surface Vessel](../autonomous-surface-vessel/00-README-and-signoff.md) |
| **Offshore Shelf / Deep Tie:** UNOLS / Crewed Vessel MBES & AUV | Shelf break ($>10\text{–}20\text{ m}$) to deep water | Matched seasonal epoch (pre-storm/post-storm separation) | Draft/squat shifts; outer-beam refraction; VDatum offshore boundary | [UNOLS Cruise](../unols-research-cruise/00-README-and-signoff.md) · [Underwater AUV](../underwater-auv/00-README-and-signoff.md) |

---

## 2. Intertidal Overlap Geometry & Tidal / Solar Window Math

To eliminate the coastal white ribbon without inventing an unmeasured beach ([Chapter 48](../../fable/chapters/ch48-compositing.md) §48.6, [Gemini4 Sec. 13.2.2](../../gemini4/book/ch-13/sec-13-02.md)):

1. **High-Tide Marine Excursion ($z_{\text{boat,max}}$):** Schedule shallow-draft ASV/launch MBES around spring high water $z_{\text{high}}$ (in common datum, e.g. MLLW or NAVD88). With safe under-keel + transducer immersion depth $d_{\min}$, the landward acoustic limit is:
   $$z_{\text{boat,max}} = z_{\text{high}} - d_{\min}$$
2. **Low-Tide Airborne / UAS Excursion ($z_{\text{low}}$):** Schedule topographic NIR lidar/UAS SfM and $532\text{ nm}$ bathylidar within $1.5\text{ hours}$ before/after predicted spring low water $z_{\text{low}}$ (project planning window) to expose tidal flats for direct subaerial scanning and maximize green laser bottom depth.
3. **Subaerial vs. Submerged ALB Overlap Geometry (Target 100–500 m Cross-Shore Belt):** With tidal range $\Delta H_{\text{tide}} = z_{\text{high}} - z_{\text{low}}$ and foreshore slope $\tan\beta$:
   $$\Delta z_{\text{overlap,subaerial}} = \Delta H_{\text{tide}} - d_{\min}, \qquad \Delta z_{\text{overlap,ALB}} = \Delta H_{\text{tide}} + d_{\text{ALB,max}} - d_{\min}, \qquad W_{\text{overlap}} = \frac{\Delta z_{\text{overlap}}}{\tan\beta}$$
   Subaerial NIR/SfM loses positive vertical overlap whenever $\Delta H_{\text{tide}} \le d_{\min}$ (creating a vertical gap, not merely narrow width); on micro-tidal coasts ($\Delta H_{\text{tide}} < d_{\min} + 1\text{ m}$), bridge the $1\text{–}5\text{ m}$ shallow zone using **$532\text{ nm}$ bathylidar** ($d_{\text{ALB,max}} \approx (1.5\text{–}3)\,Z_{\text{sd}}$ below $z_{\text{low}}$) or wading RTK / jet-ski SBES directly overlapped with high-tide USV/launch MBES.
4. **Solar Elevation Window ($30^\circ\text{–}45^\circ$) vs. Tide Phase Conflict Resolution:**
   - Optical photogrammetry and green bathylidar require **sun elevation strictly $30^\circ\text{–}45^\circ$**: $<30^\circ$ casts long terrain/dune shadows; $>45^\circ\text{–}50^\circ$ blinds detectors with specular water glint ([Gemini4 Sec. 13.2.4](../../gemini4/book/ch-13/sec-13-02.md)).
   - Check astronomical tide + solar ephemeris tables **months in advance**: spring low water only coincides with $30^\circ\text{–}45^\circ$ sun angles during specific semi-monthly tidal-phase windows. Schedule airborne mobilization to those joint windows first; treat high-tide ASV/launch sorties as phase-shifted by $\sim 6.2\text{ h}$ (or on adjacent days in calm weather before storm sediment transport reshapes the beach).

---

## 3. Unified Vertical Datum & VDatum / SEP Uncertainty Propagation

Every land–water campaign MUST enforce **one common horizontal frame/epoch, one vertical datum, and one sign convention** for merging (**TBDEM / BAG**: $+z\uparrow\text{ m}$, seabed $< 0\text{ m}$; **IHO S-102 chart export**: $+d\downarrow\text{ m}$, `EPSG verticalCS = 6498`, seabed $> 0\text{ m}$) prior to compositing ([Chapter 9](../../fable/chapters/ch09-vertical-datums.md) §9.8):

- **Transform via Ellipsoid First (ERS + Published SEP Grid):** Keep raw airborne and acoustic trajectories in ellipsoidal height $h$ (`ITRF2020` / `NAD83(2011)`), then transform to the project TBDEM datum (e.g., `NAVD88`, `NAPGD2022`, or `MLLW`/`LAT`) using a single named **VDatum / VORF / AusCoastVDT / `vyperdatum`** separation pipeline with checksummed grid versions.
- **Propagated Datum Separation & Seam Uncertainty:** Define datum separation model uncertainty cleanly as $\sigma_{\text{SEP}}^2 = \sigma_N^2 + \sigma_{\text{TSS}}^2 + \sigma_{\text{CD}\to\text{LMSL}}^2$ (without double-counting trajectory $\sigma_h^2$). When both platforms reduce from $h$ via the **same ERS + SEP grid**, static SEP bias cancels across the seam ($\sigma_{\text{step,ERS}} = \sqrt{\sigma_{z,1,\text{ellip}}^2 + \sigma_{z,2,\text{ellip}}^2}$); when comparing a tide-gauge-reduced marine survey against an ERS/orthometric airborne survey, include $\sigma_{\text{SEP}}$:
  $$\sigma_{\text{step}} = \sqrt{\sigma_{z,1}^2 + \sigma_{z,2}^2 + \sigma_{\text{SEP}}^2}, \qquad \sigma_{x,\text{shoreline}} = \frac{\sqrt{\sigma_{\text{DEM}}^2 + \sigma_{\text{SEP}}^2}}{\tan\beta}$$
  *(Typical coastal VDatum uncertainty is $0.05\text{–}0.10\text{ m}$ on open coasts and $0.10\text{–}0.20\text{ m}$ in complex estuaries; [Chapter 9](../../fable/chapters/ch09-vertical-datums.md) §9.7.)*
- **Seam & Surface-Definition Audit (`ch48` §48.2 & §48.8):**
  - Run **Nuth–Kääb 3D co-registration** and residual sampling across the intertidal overlap belt. Any seam step exceeding **$2\sigma_{\text{step}}$** ($2\sqrt{\sigma_{z,1}^2 + \sigma_{z,2}^2}$ for shared-ERS acquisitions; $2\sqrt{\sigma_{z,1}^2 + \sigma_{z,2}^2 + \sigma_{\text{SEP}}^2}$ when comparing gauge-reduced vs. ERS surveys) is a **datum, tide-zoning, draft, or refraction failure** — NEVER feather over a bias!
  - Stratify overlap residuals by substrate (`bare sand` vs. `seagrass/kelp` vs. `marsh`): green lidar/optical often measures the top of submerged seagrass or *Spartina* marsh while lower-frequency sonar penetrates further, creating a surface-ontology ledge rather than an instrument error.
  - **Mandatory Companion Layers & No-Invented-Beach Rule:** Deliver co-registered `source_id`, `acquisition_date`, `uncertainty` (inflated by VDatum and interpolation distance), `method/TID` flags, and LAS Class 45 (*no bottom found at*) polygons. **Never feather a navigation channel** and **never present interpolated surf-zone gaps as measured bathymetry**.

---

## 4. Multi-Asset Field Synchronization & Safety Deconfliction Checklist

Use this coordination sequence whenever two or more coastal survey platforms share an operating area:

- [ ] **[GATE]** **Joint Ops Lead & Single CRS/Epoch Lock:** Designate one White-Ribbon Joint Coordinator and execute a single [Project Geodetic Header](template-project-header.md) (shared base stations/CORS, shared VDatum/SEP grid hash, common UTC clock) signed by both air and marine leads before mobilization.
- [ ] **[GATE]** **Airspace & UAS–Aircraft Deconfliction:** Separate crewed bathylidar/ALS aircraft (`400–600 m` ALB; `1,000–2,500 m` ALS) from mapping UAS (`<= 120 m` EASA Open / `<= 122 m [400 ft]` FAA Part 107 AGL) via time-window staggering (e.g., UAS beach ops after ALB clears sector), mandatory VHF CTAF/air-to-air guard monitoring, NOTAMs, and positive two-way radio hold authority.
- [ ] **[GATE]** **532 nm Laser NOHD, FAA Notice & Surface-Crew Eye Safety:** Verify crewed bathylidar Nominal Ocular Hazard Distance (NOHD; and binocular `ENOHD` if `Class 1M`), **FAA `AC 70-1B` Form `7140-1` + Laser Clearinghouse (LCH)** clearances, automated laser shutter geofencing over populated beaches/vessels, and issue wavelength-matched `532 nm` laser safety eyewear (OD rated per LSO memo; prohibit `7x50` binoculars during active passes) or clear crews (`ANSI Z136.6`).
- [ ] **[GATE]** **Marine Traffic & Surf-Zone Wading Deconfliction:** Coordinate high-tide ASV/launch tracklines with shore RTK/wading teams and chase vessels via AIS + VHF working channel; maintain hard surf-zone depth/wave abort floors (`H_s`, minimum UKC) and physical e-stop/recall verification before entering shallow flats.
- [ ] **[REC]** **Contemporaneous Tide, Benchmark, Secchi & Storm Separation:** Run project tide gauge (leveled in closed loops to `>= 3` tidal benchmarks per NOAA CO-OPS / [Chapter 26](../../fable/chapters/ch26-survey-planning.md) §26.3, `>= 5` benchmarks recommended for primary datum transfers) + shore RTK base continuously across *both* high-tide marine and low-tide airborne windows; log in-situ Secchi depth / $K_d$ during ALB flights; if a storm (`H_s` spike / beach cut) occurs between low-tide and high-tide acquisitions, log an epoch break.
- [ ] **[GATE]** **Intertidal Overlap Quick-Check Before Demob:** Difference preliminary low-tide beach/ALB grids against high-tide ASV/launch grids in the `100–500 m` overlap belt *before releasing either vessel or aircraft* from station (`|median bias|` explained by VDatum/surface-definition within $2\sigma_{\text{step}}$).

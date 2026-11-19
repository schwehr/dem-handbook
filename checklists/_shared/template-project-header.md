# Shared Template 0.2 — Project Geodetic, Metadata & RACI Sign-Off Header

> **Purpose:** Establish a single unambiguous geodetic, ontological, sign-convention, and accountability contract **before** mobilizing platforms, deploying control, or ingesting raw sensor streams. Copy the Compact Checklist Header into every operational phase sheet (`01`–`08`) and archive the completed ISO/WKT2 record with the final deliverable ([Chapter 49](../../fable/chapters/ch49-metadata.md), [Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md), [Gemini4 Sec. 3.2](../../gemini4/book/ch-03/sec-03-02.md)).

---

## 1. Copy-Ready Compact Checklist Header (`PLAN.md` §2.1 Standard)

Paste this three-line blockquote directly under the `# <Modality Title> — <Phase Title>` H1 heading of every active project checklist file (`01`–`08`):

```markdown
> **Project / Cruise / Sortie ID:** `__________________` | **Modality:** `<slug>` | **Platform / Vessel / Tail #:** `__________________`  
> **Horizontal CRS / Epoch:** `__________________` | **Vertical Datum / Geoid or SEP:** `__________________` | **Governing Spec:** `__________________`  
> **Sign Convention:** `[ ] Elevation (+z ↑, m)` `[ ] Depth (+d ↓, m)` | **Phase Lead & Date (UTC):** `__________________` | **Independent Verifier & Date (UTC):** `__________________`
```

*Two-person rule:* `Horizontal CRS / Epoch` MUST declare a **specific realization** (e.g., `NAD83(2011)` or `ITRF2020`, never bare `WGS 84`), and an **Independent Verifier** distinct from the **Phase Lead** should co-sign high-consequence datum, lever-arm, SWL, and chain-of-custody entries (`PRD.md` §7.2). (The trailing `Platform / Vessel / Tail #`, `Governing Spec`, and `& Date (UTC)` tokens are standardized Phase 0 extensions beyond the core fields enforced by `check_checklists.py`; modality suites using role-adapted labels such as `Platform / Tail #`, `Platform / Vessel / Hull #`, `Constellation / Platform`, `Vessel / Hull Class & Governing Spec`, or documenting `Governing Spec` in Phase `00`/`01` tables remain compliant.)

---

## 2. ISO 19111 / ISO 19115 Geodetic & Coordinate Reference Specification

Every coordinate in a DEM is a four-dimensional quantity $(x, y, z, t)$ anchored to a named realization and epoch. Never enter bare `"WGS 84"`, `"NAD83"`, `"NAVD88"`, or `"MLLW"` without realization, geoid/separation model, epoch, and linear units ([Chapter 8](../../fable/chapters/ch08-horizontal-datums.md), [Chapter 9](../../fable/chapters/ch09-vertical-datums.md)).

| Field | ISO 19111 / 19115 / WKT2 Element | Project Specification (Fill Before Acquisition) | Guardrail / Verification Rule |
|---|---|---|---|
| **Project / Cruise / Sortie ID** | `MD_Identifier.code` | `____________________________` | Unique immutable slug + **Platform / Vessel / Tail #:** `____________` |
| **Acquisition Window (UTC)** | `EX_TemporalExtent` (`start`–`end`) | `____-__-__T__:__:__Z` to `____-__-__T__:__:__Z` | ISO 8601 UTC; include valid-until epoch / re-survey trigger |
| **Horizontal System & Realization** | `GeodeticCRS` / `REALIZATION` | `____________________________` | e.g., `ITRF2020`, `NAD83(2011)`, `WGS 84 (G2296)`; note `NATRF2022` beta Sept 2026 (NAD 83 still official pending ~2027 adoption); reject bare `EPSG:4326` for `< 2 m` work |
| **Reference Epoch & Obs Epoch** | `FRAMEEPOCH` / `COORDINATEMETADATA` | Ref `______.__` / Obs `______.__` | Decimal year; required for dynamic frames (`ITRF`, `WGS 84`) and plate boundaries |
| **Velocity / Deformation Model** | `PointMotionOperation` | `____________________________` | e.g., `NOAA HTDP v3.5+`, `ITRF2020 PMM`, `NATRF2022 IFVM`, `NZGD2000` |
| **Projected CRS & Authority Code** | `ProjectedCRS` / `EPSG` | `____________________________` | State projection, zone, scale factor $k_0$, and grid-vs.-ground `CSF` policy |
| **Linear Units** | `CS.Unit` (SI metre mandatory) | `[ ] Metre (m)` `[ ] International Foot (0.3048 m exact; secondary only)` | **US Survey Foot deprecated 2022-12-31** (84 FR 55562); verify legacy CAD/state law |
| **Vertical Height Type & Datum** | `VerticalCRS` ($h$, $H$, $H^*$, $H_{\text{dyn}}$, CD) | `____________________________` | e.g., `ITRF2020 h`, `NAVD88 (EPSG:5703)`, `NAPGD2022` (2026 beta / ~2027 adoption), `IGLD 1985`, `MLLW`, `LAT` |
| **Geoid / Quasigeoid / SEP Model** | `VerticalTransform` / GGXF | Model: `______________` SHA-256: `________` | e.g., `GEOID18`, `GEOID2022`, `EGM2008`, `NOAA VDatum v4.x` / `vyperdatum`, `VORF` |
| **Tidal Datum Epoch & Control Gauge** | `VerticalDatum` (`NTDE`) | Epoch: `________` Control ID: `________` | e.g., `NTDE 1983–2001` (or modified 5-yr Gulf/AK epoch); note ~5–9 cm shift in `2002–2020` at typical 2–4 mm/yr RSLR gauges, larger where subsidence is fast ([Chapter 9](../../fable/chapters/ch09-vertical-datums.md) §9.3) |
| **Compound CRS / WKT2:2019 String** | `COMPOUNDCRS` (ISO 19162:2019) | EPSG: `________` (WKT2 file attached: `[ ] Yes`) | Verify axis order (`E, N` vs. `Lat, Lon`); embed WKT2 inside GeoTIFF 1.1 / LAS 1.4 VLR |

---

## 3. Coordinate Frame, Lever-Arm & Sign Convention Contract

Mixing **ENU** and **NED** or flipping $+z\uparrow$ and $+d\downarrow$ is the most expensive single-bit error in elevation engineering ([Notation & Symbols](../../gemini4/book/00-front-matter/notation-and-symbols.md), [Chapter 13](../../fable/chapters/ch13-imu-ins.md)). Check one option per row and attach the signed photo-documented offset diagram:

| Convention Item | Declared Project Setting | Mandatory Mathematical Definition |
|---|---|---|
| **Product Vertical Sign** | `[ ] Elevation (+z ↑, m)` / `[ ] Depth (+d ↓, m)` | $z = -d$ on identical datum zero ($h = H + N = z_{\text{CD}} + \text{SEP} = \text{SEP} - d_{\text{CD}}$, [Gemini4 Sec. 3.2](../../gemini4/book/ch-03/sec-03-02.md)). **ONS BAG** (`FSD 2.0.1`) and **TBDEMs** use $+z\uparrow$ (seabed $< 0\text{ m}$); **IHO S-102 Ed. 3.0.0** uses positive-downward depth $+d\downarrow$ (`EPSG verticalCS = 6498`, seabed $> 0\text{ m}$; verify GDAL open options); **IHO S-44 TVU** and acoustic ray-tracing use $+d\downarrow > 0$. |
| **Local Mapping Frame (LTP)** | `[ ] ENU (+E, +N, +U↑)` / `[ ] NED (+N, +E, +D↓)` | Right-handed ($\hat{\mathbf{e}}_1 \times \hat{\mathbf{e}}_2 = \hat{\mathbf{e}}_3$). State explicit permutation matrix $\mathbf{P}_{\text{ENU}\leftrightarrow\text{NED}}$ if trajectory and product frames differ. |
| **Platform Body Frame ($b$-frame)** | `[ ] Aero/Marine FRD (+x fwd, +y stbd/right, +z down)` / `[ ] ENU-Airborne RFU (+x stbd/right, +y fwd, +z up)` / `[ ] Terrestrial FLU` | Origin at IMU reference center. State exact body axis triad (`FRD` vs. `RFU` vs. `FLU`; note `RFU`/`FRD` align with `ENU`/`NED` only at heading $\psi = 0^\circ$ North), plus right-hand positive roll $\phi$, pitch $\theta$, and yaw $\psi$. |
| **Lever-Arm Vector Sign ($\mathbf{l}_{\text{lever}}^b$)** | `IMU → GNSS ARP`: `( ___, ___, ___ ) m` · `IMU → Sensor`: `( ___, ___, ___ ) m` | Explicitly state direction (`From IMU to Sensor` vs. `From Sensor to IMU`) and reference point (GNSS ARP vs. L1 phase center; transducer acoustic center vs. face). |
| **Boresight Rotation Convention** | `[ ] Active / Position-Vector (frame/vector rotated)` / `[ ] Passive / Coordinate-Frame (axes rotated)` | Declare rotation sense (active vs. passive), Euler sequence (e.g., $Z$-$Y$-$X$: yaw–pitch–roll; intrinsic vs. extrinsic), and exact target software (`POSPac`, `CARIS`, `Qimera`, `TerraMatch`). *(Do not conflate boresight angles with 7-parameter Helmert datum methods.)* |

---

## 4. Governing Specification, Surface Ontology & Delivery Contract

| Parameter | Project Lock-In | Notes / Reference |
|---|---|---|
| **Governing Spec & Edition** | `________________________________________` | e.g., `IHO S-44 Ed. 6.2.0 (Oct 2024; retains Ed. 6.1.0 Table 1 TVU/THU a/b parameters + §3.8 seabed characteristics) Order 1a`, `IHO S-100 Ed. 5.2.0 / S-102 Ed. 3.0.0 (Dec 2024) / S-158:102 Ed. 1.0.0 (Dec 2025)`, `NOAA HSSD (2024 restructured ed.; check annual log)`, `USGS LBS 2024/2025 rev. A QL1`, `ASPRS Ed. 2 v2 (2024; Addenda I–VI, incl. Add. V UAS & VI Oblique)`, `ICAO PANS-AIM Area 2`, `IHO B-13 Ed. 1.0 (2024)` |
| **Target Accuracy Statement** | Statistic: `________` Threshold: `________` Strata: `________` | Never write unqualified `±X cm`. Specify `RMSE_V`, `TVU_95%`, `LE95`, `CE90`, `NMAD`, and confidence level ([Chapter 70](../../fable/chapters/ch70-specifications-guided-tour.md)). |
| **Surface Ontology** | `[ ] DSM` `[ ] Bare-Earth DTM` `[ ] DBM` `[ ] Seamless TBDEM` | Declare rules for bridges (LAS Class 17), culverts (cut vs. intact), open-pile piers, wires, solar arrays, fluid mud ($1{,}200\text{ kg/m}^3$), and snowpack ([Chapter 4](../../fable/chapters/ch04-names-and-definitions.md), [Chapter 32](../../fable/chapters/ch32-dsm-to-dtm.md)). |
| **Water Treatment** | `[ ] Hydro-flattened` `[ ] Hydro-enforced` `[ ] Hydro-conditioned` `[ ] Raw` | LBS baseline: flatten lakes $\ge 0.8\text{ ha}$ ($2\text{ acres}$) and rivers $\ge 30\text{ m}$ ($100\text{ ft}$) monotonically ([Chapter 34](../../fable/chapters/ch34-water-in-dems.md)). |
| **Grid Registration & NoData** | `[ ] Pixel-is-Area` `[ ] Pixel-is-Point` · NoData: `[ ] NaN` `[ ] -9999.0` | Explicitly verify GeoTIFF **`AREA_OR_POINT`** (`Area` vs. `Point`) tag; **never use `NoData = 0`** near coasts or lakes ([Chapter 47](../../fable/chapters/ch47-file-formats.md)). Declare native resolution vs. grid post. |
| **Deliverable Formats & Archive** | Formats: `__________________` · Repository: `__________________` | Archive **raw sensor logs + RINEX/IMU/SBET + calibration + geoid grids + checkpoints** in `BagIt` (`SHA-256`); deliver `COG`/`COPC`/`BAG`/`S-102`/`STAC` ([Chapter 50](../../fable/chapters/ch50-archiving-and-provenance.md)). |
| **Data Rights, Export & Licence** | SPDX: `__________` · Export/Sovereignty: `__________` · `CARE/OCAP®`: `[ ] N/A [ ] Signed` | Screen for EAR/ITAR, national thresholds, GDPR PII redaction, NHPA §106 / ARPA withholding ([Chapter 68](../../fable/chapters/ch68-legal-issues.md), [Chapter 69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md)). |

---

## 5. RACI Accountability & Phase Gate Sign-Off Matrix

Roles: **R** = Responsible (executes), **A** = Accountable (single final sign-off), **C** = Consulted, **I** = Informed. **Independent QA/QC MUST remain organizationally walled off from production.**

| Lifecycle Gate | PI / Chief Scientist / PM | Survey Lead / Hydrographer | Platform / Flight / Watch Lead | Data Processor | Independent QA/QC Reviewer | Gate Sign-Off & Date (UTC) |
|---|---|---|---|---|---|---|
| `01` Requirements & Datum Lock | **A** | **R** | **C** | **C** | **C** | `________________` |
| `02` Permits, Safety, COI & Budget | **A** | **C** | **R** | **I** | **I** | `________________` |
| `03` Platform, Calibration & Support | **I** | **A** | **R** | **C** | **C** | `________________` |
| `04` Mission Plan & *A Priori* TPU | **I** | **R / A** | **C** | **C** | **C** | `________________` |
| `05` Underway QC & Raw Checksums | **I** | **A** | **R** | **R** | **I** | `________________` |
| `06` Emergency / Incident Hold (if any) | **A** | **C** | **R** | **I** | **I** | `________________` |
| `07` De-Mob Custody & Final Validation | **C** | **C** | **R** (de-mob) | **R** (pipeline) | **A** (acceptance) | `________________` |
| `08` Reconciled Budget & AAR PR | **A** | **R** | **C** | **C** | **C** | `________________` |

**Project Geodetic & Sign-Off Authorization:**
- **Accountable PI / PM:** `________________________` Signature: `______________` Date (UTC): `____-__-__T__:__:__Z`
- **Lead Surveyor / Hydrographer:** `____________________` Credential (`PLS/PE/Cat A/CP`): `________` Date (UTC): `____-__-__T__:__:__Z`
- **Independent QA/QC Lead:** `_______________________` Signature: `______________` Date (UTC): `____-__-__T__:__:__Z`

# Shared Template 0.6 — Field-Printable Emergency Response & Accident Quick-Card

> **Print and laminate one copy for every bridge, ROC console, cockpit kneeboard, drone flight case, and field truck.** Do not rely on internet connectivity during an emergency. Aligns with [Chapter 56](../../fable/chapters/ch56-case-files.md), [Chapter 68](../../fable/chapters/ch68-legal-issues.md), [Chapter 69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md), [Appendix G](../../fable/appendices/appendix-g-checklists.md) §G.9, [Gemini4 Sec. 27.1](../../gemini4/book/ch-27/sec-27-01.md), and [Gemini4 Sec. 27.2](../../gemini4/book/ch-27/sec-27-02.md).

---

## 1. Emergency Contacts & Incident Command Header (Fill Before First Launch/Flight)

- **Project / Cruise / Sortie ID:** `____________________` · **Operating Area:** `____________________`
- **Local EMS / SAR / Coast Guard / ATC:** `911` / VHF Ch `16` (`156.8 MHz`) & Ch `70` (DSC) / ATC Guard `121.5 MHz` / MRCC Tel: `____________________`
- **Regulatory Operations Centers:** NTSB ROC `+1-844-373-9922` · NRC `+1-800-424-8802` · Local FSDO / USCG Sector: `____________________`
- **Host-Country Authorities & Embassy/Consular 24h (Int'l):** Civil Aviation / Maritime MRCC: `________________` · Embassy Duty: `________________`
- **PIC / Vessel Master / Dive Supervisor:** `____________________` Tel / Sat: `____________________`
- **Principal Investigator / Project Manager:** `____________________` Tel: `____________________`
- **Laser Safety Officer (LSO, if ALB/ALS):** `____________________` Tel: `____________________`
- **Aviation / Marine Insurance Claims 24h Hotline:** `____________________` Policy #: `____________________`
- **Cyber / DPO / Legal Counsel Contact:** `____________________` Tel: `____________________`

---

## 2. Step 1 — Immediate Preserve-Life & Scene Stabilization (ICS First 15 Minutes)

1. **Life Safety First:** Halt survey operations immediately. Execute **Man Overboard (MOB)**, **Mayday / Pan-Pan** (VHF Ch 16 / Ch 70 DSC / ATC `121.5 MHz`), forced-landing/ditching egress, bystander perimeter sweep, or roadside traffic isolation.
2. **Isolate Energy & Hazards:**
   - **Marine / AUV / USV:** Engage hardware e-stop / thruster lockout before diver or crane contact; suspend LARS crane lifts; clear downwind of Li-ion/LiPo venting or H2 off-gassing.
   - **Aviation / Laser:** De-energize `532 / 1064 / 1550 nm` laser master key/interlock; if suspected ocular exposure, send exposed person immediately for dilated ophthalmological / OCT exam (`ANSI Z136.1 / Z136.6`).
   - **Battery Fire / Thermal Runaway & Subsea Primary-Cell Venting (Chemistry-Specific per SDS):** For **`UN 3480/3481` Li-ion / LiPo**, evacuate enclosed cabin/truck and apply copious seawater/water deluge cooling or AVD (`Lith-EX`) per SDS (ABC dry chem/Halon/CO2 fails thermal runaway), moving the pack clear of flammables if safe. Reserve **Class D dry powder strictly for primary lithium-metal (`UN 3090/3091`) cells**—never apply Class D to Li-ion or water to burning metallic lithium, and treat flooded **`LiSOCl2` (`UN 3090/3091`)** subsea/beacon housings as a toxic **`SO2` / `HCl`** venting hazard (open only upwind with respiratory/eye PPE).
3. **Establish ICS & Time-Stamped Scribe:** Assign one Incident Commander and one dedicated logkeeper recording **every action, heading, weather state, and radio call in UTC**.

---

## 3. Step 2 — Acoustic, RF, Satellite Beacon & Platform Recovery Registry

Populate **prior to deployment** so SAR and recovery boats do not waste battery/pinger life searching for IDs:

| Platform / Asset | Serial / Tail / Hull ID | 406 MHz ELT / PLB Hex ID | Iridium IMEI / Argos ID | VHF Beacon (MHz) | Acoustic Pinger (kHz / Rate) | USBL / AIS MMSI | Last Known `(Lat, Lon, z/d, UTC)` |
|---|---|---|---|---|---|---|---|
| Primary Platform | `__________` | `____________` | `____________` | `________` | `________` | `________` | `________________________` |
| Recovery / Chase / Backup | `__________` | `____________` | `____________` | `________` | `________` | `________` | `________________________` |

---

## 4. Step 3 — Black-Box, GNSS-Spoofing & Chain-of-Custody Log Freeze

**CRITICAL: DO NOT power-cycle flight/vessel controllers, reformat SD cards, clear autopilot logs, or run "re-calibrations" after an incident.** Evidence destruction compromises both safety investigation and insurance coverage ([Chapter 68](../../fable/chapters/ch68-legal-issues.md) §68.6, [Chapter 69](../../fable/chapters/ch69-security-sovereignty-privacy-ethics.md) §69.1.4).

- [ ] **Write-Protect & Clone Raw Telemetry:** Extract autopilot/flight-controller black box, ROC command/link logs, LARS load-cell logs, sonar/lidar raw datagrams (`.kmall`/`.s7k`/`.rxp`), AIS/ADS-B logs, and video/bridge audio onto write-once/read-only media.
- [ ] **GNSS Jamming / Spoofing Forensics Freeze:** Preserve **raw GNSS observables** (RINEX + receiver binary `.ubx`/`.sbf`/`.t02`), $C/N_0$ and Automatic Gain Control (`AGC`) time series, IMU raw accelerations/rates, and base-station logs to prove interference vs. operator error.
- [ ] **Cryptographic Chain of Custody (`FRE 901 / 902(13)–(14)`) & Medical/PII Protection:** Compute `sha256sum` immediately on every frozen file/archive (authenticating electronic records per `FRE 901/902(13)–(14)`); seal physical drives in signed tamper-evident bags recording custodian name, UTC timestamp, drive serial, and hash; **segregate injured-person medical records (retinal OCT, SMI test results) and bystander PII under restricted access** during broker/client sharing.
- [ ] **Data Spill, Cyber & PII Breach Containment:** If ransomware, unencrypted PII/GDPR exposure, ITAR/EAR technical-data spill, or restricted archaeological/sovereign data leak occurs: isolate host/cloud bucket immediately (preserve volatile memory/logs, do not wipe), revoke credentials, log exposed records, notify DPO/CISO/Legal (noting **GDPR Art. 33 72-hour** supervisory notification clock where applicable).

---

## 5. Step 4 — Statutory & Contractual Reporting Clocks

**Do not miss statutory clocks; consult Legal/PM on wording and admit no fault or liability at the scene.** *(Outside the U.S., substitute coastal/flag-state and ICAO Annex 13 equivalents—e.g., EASA Reg. `(EU) 996/2010 & 376/2014` [`72 h` occurrence reporting], IMO Casualty Investigation Code, AAIB/MAIB/TSB—while preserving wreckage/data identically.)*

| Authority / Party | Governing Rule & Form | Trigger Criteria | Statutory Deadline | POC / Filing Portal |
|---|---|---|---|---|
| **FAA (Small UAS)** | **14 CFR § 107.9** (FAADroneZone / FSDO) | Serious injury to any person, loss of consciousness, or damage to any property *other than the small UA* exceeding **$500** (cost to repair or fair market value to replace, **whichever is lower**). | **Within 10 calendar days** | `faadronezone.faa.gov` / Local FSDO |
| **NTSB (Aviation & Certificated UAS)** | **49 CFR Part 830 (`§ 830.2, § 830.5, § 830.10, § 830.15`)** | Any crewed aircraft accident, fatal/serious injury, substantial damage, mid-air collision, overdue aircraft, `> $25,000` damage to property *other than the aircraft* (lower of repair/FMV, § 830.5(a)(6)), or qualifying UAS accident under amended **§ 830.2 (2022)** (death/serious injury OR substantial damage to a UA holding an airworthiness certificate/approval). **Preserve aircraft wreckage & flight records (`§ 830.10`).** | **Immediate** notification + **10-day written report** (`§ 830.15`, NTSB Form `6120.1/6120.2`) | NTSB Response Operations Center (`+1-844-373-9922`) |
| **USCG (Marine Casualties & Pollution)** | **46 CFR § 4.05-1 / § 4.05-10** (Form **CG-2692**), **46 CFR § 4.06** (SMI), **33 CFR § 153.203** (NRC) | U.S. vessels / U.S. navigable waters: grounding, collision/allision, loss of propulsion/steering affecting seaworthiness, injury requiring medical treatment beyond first aid/death, `> $75,000` property damage; **oil/hazmat discharge** (NRC immediate); **Serious Marine Incident (SMI)** alcohol/drug testing (**2 h** alcohol / **32 h** drug). | **Immediate** verbal VHF/USCG & NRC + **5-day** written CG-2692 + **2 h / 32 h** SMI tests | Nearest USCG Sector / COTP & NRC (`+1-800-424-8802`) |
| **UNOLS / NSF / Flag State** | UNOLS **RVSS** & MFP Incident Workflow | Any injury, MOB, crane/winch wire failure, subsea asset loss, or hazmat incident on UNOLS/academic cruise. | **Immediate** to Master/Marine Supt; formal NSF report per operator SOP | Ship Master / Operator / NSF Program Officer |
| **OSHA & Laser Safety Officer** | **29 CFR 1904.39** & **ANSI Z136.1 / Z136.6** | Where OSHA has jurisdiction (shore/ROC/airfield/uninspected craft; USCG preempts on USCG-inspected vessels): fatality (**8 h**); inpatient hospitalization, amputation, or **eye loss** (**24 h**); any suspected `532/1064/1550 nm` ocular exposure (**immediate** LSO + medical). | **Immediate** (LSO/EMS); **8 h / 24 h** (OSHA) | Institutional LSO / `osha.gov` |
| **Insurer & Client / Contracting Officer** | H&M, P&I, Aviation, Floater, E&O Policies | Any hull/equipment loss, third-party claim, salvage/wreck-removal activation, or DTON/data breach. | **Immediate / within 24–72 h** per policy notice clause | Broker / Underwriter Claims Desk |

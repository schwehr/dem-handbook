### Track Specification: GNSS Constellations, Signals, and Trilateration

#### **1. Overview**
This track involves authoring **Section 1.2.1: How GNSS Works** for the Digital Elevation Model (DEM) Handbook. The content will define the primary satellite constellations (GPS, GLONASS, Galileo), explain the nature of GNSS signals, and detail the geometric principle of trilateration.

#### **2. Functional Requirements**
- **Format:** Author the content in a single Markdown file (`.md`) using **MyST Markdown** syntax.
- **Core Content:**
    - **Constellations:** Define and compare GPS (U.S.), GLONASS (Russia), and Galileo (Europe).
    - **Signals:** Explain the transmission of radio frequency signals (L-band) and their role in distance calculation.
    - **Trilateration:** Describe the 3D geometric intersection process used to determine a receiver's position.
- **Visuals & Interactivity:**
    - Include **Mermaid diagrams** to illustrate the geometric intersection of satellite spheres (trilateration).
    - Include a placeholder or embedded Python code cell for an **interactive widget** (e.g., a simple coordinate solver) using MyST integration.
- **Technical Level:** Maintain a balanced tone that serves both undergraduate students (accessible narrative) and professionals (precise terminology).

#### **3. Non-Functional Requirements**
- **Consistency:** Align with the tone and formatting established in existing book sections.
- **Source Material:** Strictly adhere to the technical data provided in `@research/0002-gnss-for-digital-elevation-models.md`.

#### **4. Acceptance Criteria**
- [ ] Section 1.2.1 is authored and follows the MyST Markdown format.
- [ ] GPS, GLONASS, and Galileo are clearly distinguished.
- [ ] The principle of 3D trilateration is explained and visualized with at least one Mermaid diagram.
- [ ] An interactive widget or a clear placeholder for one is included in the document.
- [ ] Technical terms (e.g., L-band, ellipsoidal height, geodetic reference) are used accurately.

#### **5. Out of Scope**
- Detailed analysis of the GNSS error budget (ionospheric/tropospheric delays).
- Advanced kinematic positioning methodologies (RTK, PPK, PPP).
- Implementation of the full interactive book build (this track focuses on content creation).

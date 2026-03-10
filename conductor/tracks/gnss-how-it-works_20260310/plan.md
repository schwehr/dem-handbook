### Implementation Plan: GNSS Constellations, Signals, and Trilateration

#### **Phase 1: Research & Scaffolding**
- [ ] **Task: Review Research Material & Existing Structure**
    - [ ] Analyze `@research/0002-gnss-for-digital-elevation-models.md` for specific technical details on constellations and trilateration.
    - [ ] Review the existing book structure to determine the exact path for the new section.
- [ ] **Task: Create Section Scaffolding**
    - [ ] Create the new Markdown file `sections/1.2-gnss/1.2.1-how-gnss-works.md` (or equivalent path).
    - [ ] Add the MyST header and frontmatter.
- [ ] **Task: Conductor - User Manual Verification 'Phase 1: Research & Scaffolding' (Protocol in workflow.md)**

#### **Phase 2: Content Authoring**
- [ ] **Task: Draft Constellation & Signal Sections**
    - [ ] Author the introduction to GNSS.
    - [ ] Implement detailed descriptions for GPS, GLONASS, and Galileo.
    - [ ] Explain L-band signals and their role in measurement.
- [ ] **Task: Author Trilateration & Visuals**
    - [ ] Write the conceptual explanation of 3D trilateration.
    - [ ] **Implement Mermaid Diagrams:** Create at least one diagram showing satellite intersection spheres.
- [ ] **Task: Implement Interactive Elements**
    - [ ] Embed a Python-based interactive widget or a clear placeholder using MyST syntax.
- [ ] **Task: Conductor - User Manual Verification 'Phase 2: Content Authoring' (Protocol in workflow.md)**

#### **Phase 3: Quality Assurance & Integration**
- [ ] **Task: Technical Review & Formatting**
    - [ ] Verify all technical terms against the geodetic foundations in the research paper.
    - [ ] Ensure consistent use of MyST Markdown syntax.
    - [ ] Run formatting/linting tools (e.g., `mdformat`) on the new file.
- [ ] **Task: Cross-Reference & Linkage**
    - [ ] Update the table of contents or index to include the new subpart.
- [ ] **Task: Conductor - User Manual Verification 'Phase 3: Quality Assurance & Integration' (Protocol in workflow.md)**

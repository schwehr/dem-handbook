# Product Guidelines

1. This text must be a deep dive. Text in each section should start off with an overview, but then must cover both breadth and depth. Being long is better than short.
2. Use lots of figures. Prefer diagrams created with mermaid. When images are needed, give the prompt used to generate the image.
3. Show the math.
4. Give code examples for the Earth Engine Code Editor, Earth Engine Python in Colab, PROJ/GDAL/etc. command line (use the new `gdal` CLI tool, not the old gdal/ogr commands), and in Python using pyproj, shapely, fiona, rasterio, etc.
5. Code examples should always have tests and code should be written to the Google Style Guides when possible.
6. For each topic give ways that people can use Gemini LLM tools to continue their education. For example, give example prompts for Deep Research or Gemini image generation (Nano Banana) info graphics. 

## Core Principles
1. **Academic Rigor:** Maintain an objective, rigorous, and formal tone suitable for a university-level textbook and professional reference material. Ensure all claims, methodologies, and findings are well-substantiated.
2. **Theory-First Pedagogy:** Introduce and thoroughly explain the underlying mathematical, scientific, and engineering concepts before demonstrating their implementation in code. Establish a strong conceptual foundation for the reader.
3. **Visually Rich Design:** Rely heavily on complex, interactive data visualizations, maps, and diagrams to convey spatial and quantitative information effectively. Ensure that visuals complement and elevate the text, particularly for Earth Sciences and GIS topics.

## Content & Formatting
- **Hybrid Code Snippets:** Utilize a mix of runnable core examples (executable Jupyter cells) and conceptual theory blocks (pseudocode or high-level snippets). Clearly distinguish between code that the user is expected to run and code meant purely for illustrative purposes.
- **Consistent Terminology:** Use precise and consistent terminology across Data Science, Engineering, Social Sciences, and Earth Sciences to avoid ambiguity.
- **Clear Structuring:** Organize content logically, starting from theoretical foundations and moving toward practical GIS and data analysis applications.

## Prose Style and Tone
The primary tone of the TeachBook should be a blend of Academic and Action-Oriented.
* **Academic and Formal:** Maintain an objective tone, utilize rigorous terminology, and ensure a formal structure throughout the material.
* **Action-Oriented:** While formal, the content must also be direct and instructional, focusing primarily on "how-to" and actionable takeaways.

## UX/UI Principles
Design and layout decisions should prioritize interactivity and accessibility.
* **Highly Interactive:** Incorporate interactive widgets, automated feedback loops, and dynamic elements to keep learners engaged.
* **Accessible & Inclusive:** Ensure high contrast, screen-reader compatibility, and clear, intuitive navigation paths for all users.

## Instructional Design Strategy
The curriculum should be structured to guide learners from problem identification to solution execution.
* **Problem-Based Learning:** Introduce concepts by starting with challenges, leading the learner toward theoretical solutions.
* **Step-by-Step Tutorials:** Follow up on theoretical solutions with a linear progression from basic to advanced concepts.
* **Referencing System:** When material should have a reference, link to a comprehensive reference section at the end of the documentation.

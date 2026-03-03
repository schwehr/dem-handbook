# Self-Assessment Exercises

To consolidate your understanding of the introductory Google Earth Engine (GEE) concepts, please review the following exercises. These questions are designed to test both your theoretical knowledge and your practical grasp of the differences between the JavaScript and Python APIs.

## Exercise 1: Concept Comprehension

```{exercise} Earth Engine Architecture
:label: gee-architecture-ex
What is the primary architectural difference in how the JavaScript Code Editor and the Python API handle interactive map visualization?
```

```{solution} gee-architecture-ex
:class: dropdown
The JavaScript Code Editor provides a native, integrated map canvas (`Map.addLayer`) directly within its browser-based IDE. In contrast, the Python API does not possess native UI components; it delegates map rendering to third-party Python packages (such as `geemap` or `folium`), allowing for greater flexibility but requiring external dependencies for visual output.
```

## Exercise 2: Code Translation

```{exercise} API Equivalency
:label: gee-translation-ex
Consider the following JavaScript snippet that initializes a point geometry over London:

`var point = ee.Geometry.Point([-0.1276, 51.5072]);`

How would you express this identical initialization using the Python API?
```

```{solution} gee-translation-ex
:class: dropdown
The syntax is nearly identical, primarily omitting the `var` keyword in favor of standard Python assignment:

`point = ee.Geometry.Point([-0.1276, 51.5072])`
```

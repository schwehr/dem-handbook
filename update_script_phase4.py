import re

with open('book/ch1_geodetic_foundation/01-01-geodesy.md', 'r') as f:
    content = f.read()

python_code = """
### Interactive Example: Ellipsoid Parameters

Let's use Python to calculate some basic parameters of the WGS84 ellipsoid. The two defining parameters of WGS84 are the semi-major axis ($a$) and the flattening factor ($f$). We can calculate the semi-minor axis ($b$) and the eccentricity ($e$).

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# WGS84 Parameters
a = 6378137.0  # Semi-major axis in meters
f = 1 / 298.257223563  # Flattening factor

# Calculate semi-minor axis (b)
b = a * (1 - f)

# Calculate first eccentricity squared (e^2)
e2 = 1 - (b**2 / a**2)

print(f"WGS84 Semi-major axis (a): {a} m")
print(f"WGS84 Semi-minor axis (b): {b:.3f} m")
print(f"Flattening (f): {f:.10f}")
print(f"Difference (a - b): {a - b:.3f} m")
print(f"Eccentricity squared (e^2): {e2:.10f}")
```

### Visualizing the Ellipsoid

To better understand the flattening of the Earth, we can visualize it in 3D. Note that the actual flattening of the Earth is very small (about 1/298), so the Earth looks almost like a perfect sphere from space. For demonstration purposes, we will exaggerate the flattening factor.

```{code-cell} ipython3
# Exaggerated flattening for visualization
exaggerated_f = 0.2
exaggerated_b = a * (1 - exaggerated_f)

# Generate grid for the ellipsoid
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

x = a * np.outer(np.cos(u), np.sin(v))
y = a * np.outer(np.sin(u), np.sin(v))
z = exaggerated_b * np.outer(np.ones_like(u), np.cos(v))

# Plot the 3D exaggerated ellipsoid
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, rstride=4, cstride=4, color='c', alpha=0.6, edgecolor='k', linewidth=0.2)

# Set equal aspect ratio to visualize the flattening correctly
max_radius = a
ax.set_xlim([-max_radius, max_radius])
ax.set_ylim([-max_radius, max_radius])
ax.set_zlim([-max_radius, max_radius])
ax.set_box_aspect([1, 1, 1])

ax.set_title('Exaggerated Earth Ellipsoid (Flattening = 0.2)')
ax.set_xlabel('X (m)')
ax.set_ylabel('Y (m)')
ax.set_zlabel('Z (m)')

plt.show()
```
"""

# Find where to insert the code. "The Reference Ellipsoid" section is a good place.
# Let's append it right after the Reference Ellipsoid section
content = content.replace('World Geodetic System 1984 (WGS84). \n', 'World Geodetic System 1984 (WGS84).\n' + python_code + '\n')

with open('book/ch1_geodetic_foundation/01-01-geodesy.md', 'w') as f:
    f.write(content)


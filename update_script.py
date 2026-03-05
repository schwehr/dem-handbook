import re

with open('book/ch1_geodetic_foundation/01-01-geodesy.md', 'r') as f:
    content = f.read()

satellite_gravimetry_text = """## Satellite Gravimetry and Gravity Modeling

While terrestrial, marine, and airborne gravimetry provide excellent short-wavelength detail, they suffer from vast geographical data gaps. It is logistically and economically unfeasible to survey the entirety of the deep oceans, the polar ice caps, and inaccessible mountain ranges. To map the global geopotential accurately and uniformly, the geodetic community relies on dedicated low-Earth orbit (LEO) satellite gravimetry missions.

### GRACE (Gravity Recovery and Climate Experiment)

Launched in 2002 and succeeded by the GRACE Follow-On (GRACE-FO) mission, this revolutionary program utilized the measurement principle of Satellite-to-Satellite Tracking in the Low-Low mode (SST-LL). The configuration involved two identical LEO satellites placed in the exact same orbit, separated by several hundred kilometers. 

As the lead satellite passed over an area of mass inhomogeneity—such as an unusually dense geological structure or a massive mountain range—the localized increase in gravitational pull accelerated it away from the trailing satellite. The microscopic variations in the range distance between the two satellites were continuously measured with the highest possible accuracy using a high-accuracy K-band microwave link (and laser-ranging interferometry in the GRACE-FO mission). Precise onboard accelerometers were utilized to measure and filter out non-gravitational effects such as atmospheric drag and solar radiation pressure.

GRACE's primary breakthrough was not just spatial, but temporal. By producing monthly gravity field models, GRACE allowed geodesists, climatologists, and hydrologists to observe the time-varying gravity field of the Earth. It accurately monitored seasonal mass transport phenomena, effectively "weighing" the shifting mass of the Earth's water systems from space.

### GOCE (Gravity field and steady-state Ocean Circulation Explorer)

Operating from 2009 until it ran out of fuel in October 2013, the European Space Agency's GOCE mission was designed with a different objective: to determine the stationary, static gravitational field to an unprecedented degree of spatial resolution and accuracy.

Unlike GRACE's twin-satellite SST-LL method, GOCE utilized the principle of Satellite Gravity Gradiometry (SGG). The spacecraft's primary payload was the Electrostatic Gravity Gradiometer (EGG), which consisted of an ensemble of ultra-sensitive test masses (accelerometers) mounted precisely near the center of mass of the single satellite. By directly measuring acceleration differences in all three spatial dimensions within the satellite itself, the gradiometer captured signals representing the second derivatives of the gravitational potential. A massive advantage of this methodology is that non-gravitational accelerations are the same for all measurements inside the satellite and therefore vanish perfectly by mathematical differentiation, leaving a pure, unadulterated gravitational signal.

When combined with GRACE temporal data and terrestrial gravity anomalies, these satellite missions form the definitive backbone of modern high-resolution geopotential models.
"""

relativistic_timekeeping_text = """## Relativistic Timekeeping

In the realm of modern space geodesy, spatial positioning is inextricably linked to the highly precise measurement of time. Global Navigation Satellite Systems (GNSS) determine terrestrial coordinates by measuring the transit time of electromagnetic carrier signals propagating from a constellation of satellites to a ground receiver. Because electromagnetic signals travel at the speed of light, a timing error of just one nanosecond equates to a positional error of approximately 30 centimeters.

### Relativistic Adjustments in GNSS

GNSS atomic clocks experience both motional and gravitational frequency shifts that are so massive that, without carefully accounting for numerous relativistic effects, the entire navigation system would fail within hours. Because the satellites are moving rapidly relative to the Earth's surface and exist in a much weaker gravitational field at high altitudes, their local proper time diverges significantly from the coordinate time established by reference clocks resting on the Earth's surface.

The relativistic adjustments are governed primarily by two competing physical phenomena:

1. **Special Relativity (Time Dilation via Velocity):** GNSS satellites orbit the Earth at very high velocities (approximately 4 kilometers per second). According to the principles of special relativity, moving clocks tick slower relative to a stationary observer. This kinetic time dilation causes the satellite clock to lose approximately 7 microseconds per day relative to Earth.
2. **General Relativity (Gravitational Blueshift):** The satellites operate at high altitudes (roughly 20,184 km), where the Earth's gravitational potential is significantly weaker than at the surface. According to the equivalence principle of general relativity, clocks situated in a weaker gravitational field tick faster. This gravitational frequency shift induces a massive gain of approximately 45 microseconds per day.

The summation of these two competing forces results in a net gain of 38 microseconds per day. While seemingly minuscule in human terms, an uncorrected time drift would accumulate a massive positioning error of over 11 kilometers every single day. Under such conditions, the GNSS would be rendered entirely useless for global navigation within a matter of minutes.

### Relativistic Geodesy and Chronometric Leveling

The extreme sensitivity of the passage of time to gravitational potential has birthed an entirely new, highly experimental sub-discipline: relativistic geodesy. Historically, finding the precise difference in geopotential (i.e., true orthometric elevation) between two distant points required laborious classical optical leveling across the terrain, or complex regional gravimetric surveys. However, the development of next-generation optical atomic clocks has opened the door to a revolutionary concept known as "chronometric leveling".

Modern experimental optical atomic clocks provide extremely precise frequencies based on quantum energy transitions. At this extreme level of precision, comparing the tick rates of two optical clocks connected via a phase-stabilized optical fiber link directly reveals the gravitational redshift caused by the varying geopotential between their locations. Because general relativity dictates that this gravitational frequency shift is directly proportional to the geopotential difference, geodesists can calculate the exact difference in physical height between the two clock stations purely by measuring time.
"""

content = re.sub(r'## Satellite Gravimetry and Gravity Modeling\n', satellite_gravimetry_text, content)
content = re.sub(r'## Relativistic Timekeeping\n?', relativistic_timekeeping_text, content)

with open('book/ch1_geodetic_foundation/01-01-geodesy.md', 'w') as f:
    f.write(content)

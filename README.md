# Engineering Units

[![Tests](https://github.com/matuscvengros/engunits/actions/workflows/tests.yml/badge.svg)](https://github.com/matuscvengros/engunits/actions/workflows/tests.yml)
[![Docs](https://github.com/matuscvengros/engunits/actions/workflows/docs.yml/badge.svg)](https://github.com/matuscvengros/engunits/actions/workflows/docs.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/engunits)](https://pypi.org/project/engunits/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Typed engineering quantities with unit-preserving storage, built on [pint](https://pint.readthedocs.io/).

**engunits** wraps pint in a typed layer that gives every physical quantity its own Python class. You get IDE autocompletion, type-checked arithmetic, automatic cross-type resolution, and clean SI/Imperial conversions — without losing access to pint's full unit ecosystem.

## Install

```bash
pip install engunits
```

## Quick Start

### Creating quantities

Quantities preserve the units you give them. When no unit is specified, SI is assumed.

```python
from engunits import Mass, Force, Length, Velocity

m = Mass(1000, "lb")       # stored as 1000 lb
f = Force(100, "N")        # stored as 100 N
v = Velocity(60, "mph")    # stored as 60 mph
l = Length(5)               # stored as 5 m (SI default)
```

### Converting units

Convert on demand with callable syntax, `.to()`, or the `.si()` / `.imperial()` shortcuts.

```python
m = Mass(1000, "lb")

m("kg")              # Mass(453.592, 'kg')
m.to("kg")           # Mass(453.592, 'kg')  — same as above
m.si()               # Mass(453.592, 'kg')
m.imperial()         # Mass(1000, 'lb')

# Chain conversions
Force(100, "N")("lbf")("kN")  # Force(0.1, 'kN')
```

### Arithmetic

Same-type arithmetic preserves the left operand's units. Cross-type arithmetic automatically resolves to the correct quantity type.

```python
from engunits import Mass, Force, Acceleration, Velocity, Time, Power

# Same-type: preserves units
Mass(10, "lb") + Mass(5, "lb")     # Mass(15, 'lb')
Mass(30, "kg") / Mass(10, "kg")    # 3.0 (dimensionless float)

# Scalar multiplication/division
Mass(10, "kg") * 3                  # Mass(30, 'kg')
Force(30, "N") / 3                  # Force(10, 'N')

# Cross-type: automatic type resolution
Force(100, "N") / Mass(10, "kg")    # Acceleration(10, 'N / kg')
Mass(5, "kg") * Acceleration(10)    # Force(50, 'kg * m / s ** 2')
Velocity(10) * Time(5)              # Length(50, 'm / s * s')
Power(1000, "W") / Velocity(10)     # Force(100, 'W * s / m')

# Exponentiation
Length(3, "m") ** 2                  # Area(9, 'm ** 2')
Length(2, "m") ** 3                  # Volume(8, 'm ** 3')
```

### Cross-type results preserve computed units

The units from the computation are preserved — call `.si()` to normalize.

```python
result = Force(100, "lbf") / Mass(10, "lb")
print(result)           # 10 lbf / lb
print(result.si())      # 9.80665 m / s ** 2
```

### Aggregation with sum()

```python
from engunits import Mass
masses = [Mass(1, "kg"), Mass(2, "kg"), Mass(3, "kg")]
total = sum(masses)     # Mass(6, 'kg')
```

### Comparisons

```python
Mass(1, "kg") == Mass(1000, "g")   # True
Mass(1, "lb") < Mass(1, "kg")     # True
Force(10, "N") >= Force(5, "N")    # True
```

### NumPy array support

All quantities accept NumPy arrays as values.

```python
import numpy as np
from engunits import Force

f = Force(np.array([3.0, 4.0]), "N")
f.value       # array([3., 4.])
f.norm        # 5.0 (L2 norm)
f("lbf")      # Force(array([0.6744, 0.8992]), 'lbf')
```

### Properties

```python
m = Mass(10, "kg")
m.value       # 10.0 — raw numeric magnitude
m.magnitude   # 10.0 — alias for value (pint compatibility)
m.units       # 'kg'
m.norm        # 10.0 — float for scalars, L2 norm for arrays
m.quantity    # pint.Quantity(10, 'kg') — underlying pint object
float(m)      # 10.0
bool(m)       # True (False only for zero)
```

## Ambiguous Dimensionality Conversions

Some quantity types share the same physical dimensions in pint. Cross-type arithmetic producing these dimensionalities returns a raw pint `Quantity` since the intended type is ambiguous. Explicit conversion methods are provided for intentional casts.

### Frequency / Angular Velocity

Pint treats radians as dimensionless, so `rad/s` and `Hz` both reduce to `1/[time]`. The physical relationship `ω = 2πf` requires an explicit conversion.

```python
from engunits import Frequency, AngularVelocity

omega = AngularVelocity(60, "rpm")
f = omega.to_frequency()        # Frequency(1, 'Hz')

f = Frequency(50, "Hz")
omega = f.to_angular_velocity() # AngularVelocity(314.159, 'rad/s')

# Roundtrip
Frequency(10, "Hz").to_angular_velocity().to_frequency()  # Frequency(10, 'Hz')
```

### Energy / Moment

Energy (J) and torque (N\*m) share dimensionality `[mass]*[length]²/[time]²` but are physically distinct.

```python
from engunits import Energy, Moment

e = Energy(100, "J")
m = e.to_moment()       # Moment(100, 'N * m')

m = Moment(50, "lbf*ft")
e = m.to_energy()       # Energy(67.791, 'J')
```

### Charge / Capacity

Charge (C) and battery capacity (A\*h) share dimensionality `[current]*[time]`.

```python
from engunits import Charge, Capacity

q = Charge(3600, "C")
cap = q.to_capacity()   # Capacity(1, 'A * h')

cap = Capacity(2, "A*h")
q = cap.to_charge()     # Charge(7200, 'C')
```

## Supported Quantities (41)

### SI Base

| Class | SI Unit |
|---|---|
| `Mass` | kg |
| `Length` | m |
| `Time` | s |
| `Temperature` | K |
| `Current` | A |
| `AmountOfSubstance` | mol |
| `LuminousIntensity` | cd |

### Mechanics

| Class | SI Unit |
|---|---|
| `Velocity` | m/s |
| `Acceleration` | m/s^2 |
| `Force` | N |
| `Moment` | N\*m |
| `Energy` | J |
| `Power` | W |
| `Area` | m^2 |
| `Volume` | m^3 |
| `Density` | kg/m^3 |
| `Pressure` | Pa |
| `Frequency` | Hz |
| `Momentum` | kg\*m/s |
| `AngularVelocity` | rad/s |
| `AngularAcceleration` | rad/s^2 |
| `MomentOfInertia` | kg\*m^2 |
| `SurfaceTension` | N/m |

### Electromagnetism

| Class | SI Unit |
|---|---|
| `Voltage` | V |
| `Charge` | C |
| `Capacity` | A\*h |
| `Resistance` | ohm |
| `Capacitance` | F |
| `Inductance` | H |
| `MagneticFlux` | Wb |
| `MagneticFluxDensity` | T |
| `Conductance` | S |
| `ElectricField` | V/m |

### Fluid and Thermal

| Class | SI Unit |
|---|---|
| `DynamicViscosity` | Pa\*s |
| `KinematicViscosity` | m^2/s |
| `MassFlowRate` | kg/s |
| `VolumetricFlowRate` | m^3/s |
| `ThermalConductivity` | W/(m\*K) |
| `SpecificHeatCapacity` | J/(kg\*K) |
| `HeatFlux` | W/m^2 |

### Optics

| Class | SI Unit |
|---|---|
| `Illuminance` | lx |

## Accessing pint directly

Every quantity exposes its underlying pint object via `.quantity` for advanced use cases.

```python
from engunits import Mass

m = Mass(10, "kg")
pq = m.quantity          # pint.Quantity(10, 'kg')
pq.dimensionality       # {'[mass]': 1}
```

You can also use the shared registry directly:

```python
from engunits import Q_, ureg

q = Q_(9.81, "m/s**2")  # raw pint Quantity
```

## License

MIT

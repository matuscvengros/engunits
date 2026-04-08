# Engineering Units

[![Tests](https://github.com/matuscvengros/engunits/actions/workflows/tests.yml/badge.svg)](https://github.com/matuscvengros/engunits/actions/workflows/tests.yml)
[![Docs](https://github.com/matuscvengros/engunits/actions/workflows/docs.yml/badge.svg)](https://github.com/matuscvengros/engunits/actions/workflows/docs.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/engunits)](https://pypi.org/project/engunits/)

Typed engineering quantities with unit-preserving storage, built on [pint](https://pint.readthedocs.io/).

## Install

```bash
pip install engunits
```

## Quick start

```python
from engunits import Mass, Force, Velocity

# Create quantities -- input units are preserved, SI assumed when omitted
m = Mass(1000, "lb")       # stored as 1000 lb
f = Force(100, "N")

# Convert on demand
print(m("kg"))              # 453.592 kg
print(m.si())               # 453.592 kg
print(m.imperial())         # 1000 lb

# Cross-type arithmetic resolves automatically
a = f / Mass(10, "kg")      # -> Acceleration
print(a.si())                # 10 m / s ** 2

# Arithmetic preserves units
total = Mass(10, "lb") + Mass(5, "lb")   # 15 lb
ratio = Mass(30, "kg") / Mass(10, "kg")  # 3.0

# sum() works
sum([Mass(1, "kg"), Mass(2, "kg"), Mass(3, "kg")])  # Mass(6, 'kg')
```

## Supported quantities (41)

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

## License

MIT

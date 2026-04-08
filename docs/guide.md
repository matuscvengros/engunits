# User Guide

## Creating quantities

Every quantity takes a numeric value and an optional unit string.
When no unit is given, the SI default is used.

```python
from engunits import Mass, Length, Temperature

m = Mass(100, "kg")         # explicit unit
m_default = Mass(100)       # SI default: kg
m_imperial = Mass(220, "lb")

# NumPy arrays are supported
import numpy as np
forces = Force(np.array([10, 20, 30]), "N")
```

Construction validates that the unit is dimensionally compatible:

```python
Mass(10, "m")  # raises DimensionalityError -- meters are not mass
```

## Unit preservation

Units given at construction are preserved through all operations.
Conversion only happens when you ask for it.

```python
m = Mass(1000, "lb")
print(m.value)   # 1000.0
print(m.units)   # lb

doubled = m * 2
print(doubled)   # 2000 lb -- still in pounds

total = m + Mass(500, "lb")
print(total)     # 1500 lb
```

When adding quantities in different units, the **left operand's** units win:

```python
a = Mass(1, "lb") + Mass(1, "kg")
print(a)  # 3.20462 lb
```

## Conversion

Three equivalent ways to convert:

```python
m = Mass(100, "kg")

# .to() method
m.to("lb")        # Mass(220.462, 'lb')

# Callable syntax (sugar for .to)
m("lb")            # Mass(220.462, 'lb')

# System conversion
m.si()             # Mass(100, 'kg')
m.imperial()       # Mass(220.462, 'lb')
```

All conversions return a **new instance** -- the original is unchanged.

## SI and Imperial systems

Every quantity knows its SI and Imperial defaults:

```python
from engunits import Force, Pressure

f = Force(100, "N")
f.si()         # Force(100, 'N')
f.imperial()   # Force(22.4809, 'lbf')

p = Pressure(6895, "Pa")
p.imperial()   # Pressure(1.00007, 'psi')
```

Electromagnetic quantities use SI units in both systems (there is no
separate imperial EM system).

## Arithmetic

### Same-type operations

Addition and subtraction require matching types:

```python
Mass(10, "kg") + Mass(5, "kg")   # Mass(15, 'kg')
Mass(10, "kg") - Mass(3, "kg")   # Mass(7, 'kg')
Mass(10, "kg") + Length(5, "m")   # TypeError
```

Scalar multiplication and division preserve the type:

```python
Mass(10, "kg") * 3    # Mass(30, 'kg')
Mass(30, "kg") / 3    # Mass(10, 'kg')
```

Dividing same types gives a dimensionless float:

```python
Mass(30, "kg") / Mass(10, "kg")  # 3.0
```

### Cross-type operations

Multiplying or dividing different types produces a new typed quantity
when the result dimensionality uniquely identifies a type:

```python
from engunits import Force, Mass, Acceleration, Velocity, Time

Force(100, "N") / Mass(10, "kg")    # Acceleration(10, 'N / kg')
Mass(5, "kg") * Acceleration(10)     # Force(50, 'kg * m / s ** 2')
Velocity(10) * Time(5)               # Length(50, 'm * s / s')
Length(3, "m") ** 2                   # Area(9, 'm ** 2')
```

### Ambiguous results

When a dimensionality maps to multiple types, a raw `pint.Quantity`
is returned. Cast explicitly if needed:

```python
from engunits import Energy, Moment

# Force * Length = N*m, which could be Energy OR Moment
result = Force(10, "N") * Length(5, "m")
type(result)  # pint.Quantity

# Cast to the type you intend
energy = Energy(result)
moment = Moment(result)
```

Known ambiguous pairs:
- **Energy / Moment** -- both `[M L^2 T^-2]`
- **Frequency / AngularVelocity** -- both `[T^-1]` (pint treats rad as dimensionless)
- **Charge / Capacity** -- both `[I T]`

## Comparisons

Quantities of the same type can be compared across units:

```python
Mass(1, "kg") == Mass(1000, "g")   # True
Mass(1, "lb") < Mass(1, "kg")      # True

# Works in sets and dicts (hash is SI-normalized)
s = {Mass(1, "kg")}
Mass(1000, "g") in s  # True
```

Different types are never equal:

```python
Mass(1, "kg") == Length(1, "m")  # False
```

## Using sum()

Python's built-in `sum()` is supported:

```python
masses = [Mass(1, "kg"), Mass(2, "kg"), Mass(3, "kg")]
total = sum(masses)  # Mass(6, 'kg')
```

## Temperature

Temperature supports offset units (`degC`, `degF`) for construction
and conversion, but **arithmetic requires absolute units** (`K` or `degR`):

```python
from engunits import Temperature

t = Temperature(100, "degC")
print(t("K"))     # 373.15 K
print(t("degF"))  # 212 degF

# Arithmetic -- use kelvin
t1 = Temperature(300, "K")
t2 = Temperature(50, "K")
print(t1 + t2)    # 350 K

# This raises OffsetUnitCalculusError:
# Temperature(20, "degC") + Temperature(10, "degC")
```

## Accessing the raw pint Quantity

Every typed quantity wraps a `pint.Quantity` accessible via `.quantity`:

```python
m = Mass(10, "kg")
m.quantity          # <Quantity(10, 'kilogram')>
m.quantity.to("g")  # <Quantity(10000.0, 'gram')>
```

## Supported quantities

### SI Base (7)

| Class                | SI Unit | Imperial Unit |
|---------------------|---------|---------------|
| `Mass`              | kg      | lb            |
| `Length`            | m       | ft            |
| `Time`             | s       | s             |
| `Temperature`      | K       | degF          |
| `Current`          | A       | A             |
| `AmountOfSubstance`| mol     | mol           |
| `LuminousIntensity`| cd      | cd            |

### Mechanics (16)

| Class                  | SI Unit    | Imperial Unit  |
|-----------------------|------------|----------------|
| `Velocity`            | m/s        | ft/s           |
| `Acceleration`        | m/s^2      | ft/s^2         |
| `Force`               | N          | lbf            |
| `Moment`              | N\*m       | lbf\*ft        |
| `Energy`              | J          | BTU            |
| `Power`               | W          | hp             |
| `Area`                | m^2        | ft^2           |
| `Volume`              | m^3        | ft^3           |
| `Density`             | kg/m^3     | lb/ft^3        |
| `Pressure`            | Pa         | psi            |
| `Frequency`           | Hz         | Hz             |
| `Momentum`            | kg\*m/s    | lb\*ft/s       |
| `AngularVelocity`     | rad/s      | rpm            |
| `AngularAcceleration` | rad/s^2    | rad/s^2        |
| `MomentOfInertia`     | kg\*m^2    | lb\*ft^2       |
| `SurfaceTension`      | N/m        | lbf/ft         |

### Electromagnetism (10)

| Class                 | SI Unit |
|----------------------|---------|
| `Voltage`            | V       |
| `Charge`             | C       |
| `Capacity`           | A\*h    |
| `Resistance`         | ohm     |
| `Capacitance`        | F       |
| `Inductance`         | H       |
| `MagneticFlux`       | Wb      |
| `MagneticFluxDensity`| T       |
| `Conductance`        | S       |
| `ElectricField`      | V/m     |

### Fluid and Thermal (7)

| Class                   | SI Unit      | Imperial Unit      |
|------------------------|--------------|---------------------|
| `DynamicViscosity`     | Pa\*s        | lb/(ft\*s)         |
| `KinematicViscosity`   | m^2/s        | ft^2/s             |
| `MassFlowRate`         | kg/s         | lb/s               |
| `VolumetricFlowRate`   | m^3/s        | ft^3/s             |
| `ThermalConductivity`  | W/(m\*K)     | BTU/(h\*ft\*degR)  |
| `SpecificHeatCapacity` | J/(kg\*K)    | BTU/(lb\*degR)     |
| `HeatFlux`             | W/m^2        | BTU/(h\*ft^2)      |

### Optics (1)

| Class          | SI Unit |
|---------------|---------|
| `Illuminance` | lx      |

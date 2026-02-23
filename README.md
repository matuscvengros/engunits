# engunits

[![Tests](https://github.com/matuscvengros/engunits/actions/workflows/tests.yml/badge.svg)](https://github.com/matuscvengros/engunits/actions/workflows/tests.yml)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)

Typed engineering quantities with SI-default storage, built on [pint](https://pint.readthedocs.io/).

## Install

```bash
pip install engunits
```

## Quick start

```python
from engunits import Mass, Length, Velocity

# Create quantities — SI units by default
m = Mass(1000, "lb")       # stored internally as kg
l = Length(5, "ft")         # stored internally as m

# Convert on demand
print(m("kg"))              # 453.592 kg
print(l("m"))               # 1.524 m

# Callable syntax for conversion
v = Velocity(100, "m/s")
print(v("ft/s"))            # 328.084 ft/s

# Arithmetic
total = Mass(10, "kg") + Mass(5, "kg")
scaled = Length(3, "m") * 2
ratio = Mass(30, "kg") / Mass(10, "kg")  # returns float: 3.0
```

## Supported quantities

| Class             | SI Unit   |
|-------------------|-----------|
| `Mass`            | kg        |
| `Length`          | m         |
| `Time`           | s         |
| `Temperature`    | K         |
| `Velocity`       | m/s       |
| `Force`          | N         |
| `Moment`         | N·m       |
| `Power`          | W         |
| `Energy`         | J         |
| `Area`           | m²        |
| `Volume`         | m³        |
| `Density`        | kg/m³     |
| `Pressure`       | Pa        |
| `AngularVelocity`| rad/s     |
| `Voltage`        | V         |
| `Current`        | A         |
| `Capacity`       | A·h       |

## License

MIT

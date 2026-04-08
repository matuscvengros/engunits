# engunits

Typed engineering quantities with SI-default storage, built on [pint](https://pint.readthedocs.io/).

**engunits** provides 41 typed quantity classes that preserve input units, support
on-demand conversion, and automatically resolve cross-type arithmetic to the
correct physical type.

## Features

- **Type safety** -- `Mass`, `Length`, `Force` are distinct types; incompatible
  operations raise `TypeError`.
- **Unit preservation** -- `Mass(1000, "lb")` stays in pounds until you convert.
- **Automatic type resolution** -- `Force / Mass` returns `Acceleration`.
- **SI and Imperial** -- `quantity.si()` and `quantity.imperial()` for instant system conversion.
- **Built on pint** -- full access to pint's unit ecosystem when needed.

## Quick start

```python
from engunits import Mass, Force, Velocity

# Create -- units preserved, SI assumed when omitted
m = Mass(1000, "lb")
f = Force(100, "N")

# Convert on demand
print(m("kg"))          # 453.592 kg
print(m.si())           # 453.592 kg
print(m.imperial())     # 1000 lb

# Cross-type arithmetic resolves automatically
a = f / Mass(10, "kg")  # -> Acceleration(10, "N / kg")
print(a.si())            # 10 m / s ** 2

# sum() works naturally
total = sum([Mass(1, "kg"), Mass(2, "kg"), Mass(3, "kg")])
```

## Install

```bash
pip install engunits
```

```{toctree}
:maxdepth: 2

guide
api/index
```

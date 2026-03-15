"""Shared test fixtures."""

from __future__ import annotations

from engunits.quantities import (
    Acceleration,
    AngularVelocity,
    Area,
    Capacity,
    Current,
    Density,
    Energy,
    Force,
    Length,
    Mass,
    Moment,
    Power,
    Pressure,
    Temperature,
    Time,
    Velocity,
    Voltage,
    Volume,
)

#: All concrete quantity classes for parametrized tests.
QUANTITY_CLASSES = [
    Mass,
    Length,
    Time,
    Temperature,
    Velocity,
    Acceleration,
    Force,
    Moment,
    Power,
    Energy,
    Area,
    Volume,
    Density,
    Pressure,
    AngularVelocity,
    Voltage,
    Current,
    Capacity,
]

#: Alternate units for testing conversion on each type.
ALT_UNITS: dict[str, str] = {
    "mass": "lb",
    "length": "ft",
    "time": "min",
    "temperature": "degF",
    "velocity": "ft/s",
    "acceleration": "ft/s**2",
    "force": "lbf",
    "moment": "lbf*ft",
    "power": "hp",
    "energy": "kJ",
    "area": "ft**2",
    "volume": "L",
    "density": "lb/ft**3",
    "pressure": "psi",
    "angular_velocity": "rpm",
    "voltage": "mV",
    "current": "mA",
    "capacity": "mA*h",
}

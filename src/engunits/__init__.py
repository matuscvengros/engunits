"""Typed engineering quantities with SI-default storage, built on pint."""

from importlib.metadata import PackageNotFoundError, version

from engunits.base import BaseQuantity
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
from engunits.registry import Q_, ureg

__all__ = [
    "Q_",
    "Acceleration",
    "AngularVelocity",
    "Area",
    "BaseQuantity",
    "Capacity",
    "Current",
    "Density",
    "Energy",
    "Force",
    "Length",
    "Mass",
    "Moment",
    "Power",
    "Pressure",
    "Temperature",
    "Time",
    "Velocity",
    "Voltage",
    "Volume",
    "ureg",
]

try:
    __version__ = version("engunits")
except PackageNotFoundError:
    __version__ = "0.0.0"

"""Concrete quantity classes for all supported physical types."""

from __future__ import annotations

from engunits.base import BaseQuantity


class Mass(BaseQuantity):
    """A mass quantity, defaulting to kilograms."""

    _quantity_type = "mass"


class Length(BaseQuantity):
    """A length quantity, defaulting to meters."""

    _quantity_type = "length"


class Time(BaseQuantity):
    """A time quantity, defaulting to seconds."""

    _quantity_type = "time"


class Temperature(BaseQuantity):
    """A temperature quantity, defaulting to kelvins."""

    _quantity_type = "temperature"


class Velocity(BaseQuantity):
    """A velocity quantity, defaulting to meters per second."""

    _quantity_type = "velocity"


class Acceleration(BaseQuantity):
    """An acceleration quantity, defaulting to meters per second squared."""

    _quantity_type = "acceleration"


class Force(BaseQuantity):
    """A force quantity, defaulting to newtons."""

    _quantity_type = "force"


class Moment(BaseQuantity):
    """A moment (torque) quantity, defaulting to newton-meters."""

    _quantity_type = "moment"


class Power(BaseQuantity):
    """A power quantity, defaulting to watts."""

    _quantity_type = "power"


class Energy(BaseQuantity):
    """An energy quantity, defaulting to joules."""

    _quantity_type = "energy"


class Area(BaseQuantity):
    """An area quantity, defaulting to square meters."""

    _quantity_type = "area"


class Volume(BaseQuantity):
    """A volume quantity, defaulting to cubic meters."""

    _quantity_type = "volume"


class Density(BaseQuantity):
    """A density quantity, defaulting to kilograms per cubic meter."""

    _quantity_type = "density"


class Pressure(BaseQuantity):
    """A pressure quantity, defaulting to pascals."""

    _quantity_type = "pressure"


class AngularVelocity(BaseQuantity):
    """An angular velocity quantity, defaulting to radians per second."""

    _quantity_type = "angular_velocity"


class Voltage(BaseQuantity):
    """A voltage quantity, defaulting to volts."""

    _quantity_type = "voltage"


class Current(BaseQuantity):
    """An electric current quantity, defaulting to amperes."""

    _quantity_type = "current"


class Capacity(BaseQuantity):
    """An electric capacity quantity, defaulting to ampere-hours."""

    _quantity_type = "capacity"

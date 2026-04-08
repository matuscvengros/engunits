"""Concrete quantity classes for all supported physical types."""

from __future__ import annotations

import math

from engunits.base import BaseQuantity
from engunits.config import SI_DEFAULTS

# =============================================================================
# SI base quantities
# =============================================================================


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
    """A temperature quantity, defaulting to kelvins.

    Arithmetic (``+``, ``-``) requires absolute units (``K`` or ``degR``).
    Offset units (``degC``, ``degF``) raise ``OffsetUnitCalculusError``
    from pint when used in addition or subtraction. Convert to ``K`` first.
    """

    _quantity_type = "temperature"


class Current(BaseQuantity):
    """An electric current quantity, defaulting to amperes."""

    _quantity_type = "current"


class AmountOfSubstance(BaseQuantity):
    """An amount-of-substance quantity, defaulting to moles."""

    _quantity_type = "amount_of_substance"


class LuminousIntensity(BaseQuantity):
    """A luminous intensity quantity, defaulting to candelas."""

    _quantity_type = "luminous_intensity"


# =============================================================================
# Mechanics
# =============================================================================


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
    """A moment (torque) quantity, defaulting to newton-meters.

    Shares dimensionality with :class:`Energy`; cross-type arithmetic
    producing this dimensionality returns a raw pint Quantity.
    """

    _quantity_type = "moment"

    def to_energy(self) -> Energy:
        """Reinterpret this moment as energy (dimensional cast).

        Moment and energy share dimensionality ``[mass] * [length]² / [time]²``.
        Returns a new :class:`Energy` in SI units (joules).
        """
        converted = self._quantity.to(SI_DEFAULTS["energy"])
        return Energy(converted)


class Energy(BaseQuantity):
    """An energy quantity, defaulting to joules.

    Shares dimensionality with :class:`Moment`; cross-type arithmetic
    producing this dimensionality returns a raw pint Quantity.
    """

    _quantity_type = "energy"

    def to_moment(self) -> Moment:
        """Reinterpret this energy as moment/torque (dimensional cast).

        Energy and moment share dimensionality ``[mass] * [length]² / [time]²``.
        Returns a new :class:`Moment` in SI units (newton-meters).
        """
        converted = self._quantity.to(SI_DEFAULTS["moment"])
        return Moment(converted)


class Power(BaseQuantity):
    """A power quantity, defaulting to watts."""

    _quantity_type = "power"


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


class Frequency(BaseQuantity):
    """A frequency quantity, defaulting to hertz.

    Shares dimensionality with :class:`AngularVelocity` because pint treats
    radians as dimensionless; cross-type arithmetic producing ``[time]^-1``
    returns a raw pint Quantity.
    """

    _quantity_type = "frequency"

    def to_angular_velocity(self) -> AngularVelocity:
        """Convert frequency to angular velocity using ``ω = 2πf``.

        Pint treats radians as dimensionless, so it cannot account for the
        ``2π`` factor between cycles and radians. This method applies the
        correct physical relationship.

        Returns:
            New :class:`AngularVelocity` in rad/s.
        """
        hz = self._quantity.to("Hz").magnitude
        return AngularVelocity(hz * 2 * math.pi, "rad/s")


class Momentum(BaseQuantity):
    """A linear momentum quantity, defaulting to kilogram-meters per second."""

    _quantity_type = "momentum"


class AngularVelocity(BaseQuantity):
    """An angular velocity quantity, defaulting to radians per second.

    Shares dimensionality with :class:`Frequency`; cross-type arithmetic
    producing ``[time]^-1`` returns a raw pint Quantity.
    """

    _quantity_type = "angular_velocity"

    def to_frequency(self) -> Frequency:
        """Convert angular velocity to frequency using ``f = ω / 2π``.

        Pint treats radians as dimensionless, so it cannot account for the
        ``2π`` factor between cycles and radians. This method applies the
        correct physical relationship.

        Returns:
            New :class:`Frequency` in Hz.
        """
        rads = self._quantity.to("rad/s").magnitude
        return Frequency(rads / (2 * math.pi), "Hz")


class AngularAcceleration(BaseQuantity):
    """An angular acceleration quantity, defaulting to radians per second squared.

    Does not collide with :class:`Acceleration` (``m/s²``) because pint
    preserves the ``[length]`` dimension in linear acceleration.
    """

    _quantity_type = "angular_acceleration"


class MomentOfInertia(BaseQuantity):
    """A moment of inertia quantity, defaulting to kilogram-square meters."""

    _quantity_type = "moment_of_inertia"


class SurfaceTension(BaseQuantity):
    """A surface tension quantity, defaulting to newtons per meter."""

    _quantity_type = "surface_tension"


# =============================================================================
# Electromagnetism
# =============================================================================


class Voltage(BaseQuantity):
    """A voltage quantity, defaulting to volts."""

    _quantity_type = "voltage"


class Charge(BaseQuantity):
    """An electric charge quantity, defaulting to coulombs.

    Shares dimensionality with :class:`Capacity`; cross-type arithmetic
    producing ``[current] * [time]`` returns a raw pint Quantity.
    """

    _quantity_type = "charge"

    def to_capacity(self) -> Capacity:
        """Reinterpret this charge as battery capacity (dimensional cast).

        Charge and capacity share dimensionality ``[current] * [time]``.
        Returns a new :class:`Capacity` in ampere-hours.
        """
        converted = self._quantity.to(SI_DEFAULTS["capacity"])
        return Capacity(converted)


class Capacity(BaseQuantity):
    """An electric capacity quantity, defaulting to ampere-hours.

    Shares dimensionality with :class:`Charge`; cross-type arithmetic
    producing ``[current] * [time]`` returns a raw pint Quantity.
    """

    _quantity_type = "capacity"

    def to_charge(self) -> Charge:
        """Reinterpret this capacity as electric charge (dimensional cast).

        Capacity and charge share dimensionality ``[current] * [time]``.
        Returns a new :class:`Charge` in coulombs.
        """
        converted = self._quantity.to(SI_DEFAULTS["charge"])
        return Charge(converted)


class Resistance(BaseQuantity):
    """An electrical resistance quantity, defaulting to ohms."""

    _quantity_type = "resistance"


class Capacitance(BaseQuantity):
    """An electrical capacitance quantity, defaulting to farads."""

    _quantity_type = "capacitance"


class Inductance(BaseQuantity):
    """An inductance quantity, defaulting to henrys."""

    _quantity_type = "inductance"


class MagneticFlux(BaseQuantity):
    """A magnetic flux quantity, defaulting to webers."""

    _quantity_type = "magnetic_flux"


class MagneticFluxDensity(BaseQuantity):
    """A magnetic flux density quantity, defaulting to teslas."""

    _quantity_type = "magnetic_flux_density"


class Conductance(BaseQuantity):
    """An electrical conductance quantity, defaulting to siemens."""

    _quantity_type = "conductance"


class ElectricField(BaseQuantity):
    """An electric field strength quantity, defaulting to volts per meter."""

    _quantity_type = "electric_field"


# =============================================================================
# Fluid & Thermal
# =============================================================================


class DynamicViscosity(BaseQuantity):
    """A dynamic viscosity quantity, defaulting to pascal-seconds."""

    _quantity_type = "dynamic_viscosity"


class KinematicViscosity(BaseQuantity):
    """A kinematic viscosity quantity, defaulting to square meters per second."""

    _quantity_type = "kinematic_viscosity"


class MassFlowRate(BaseQuantity):
    """A mass flow rate quantity, defaulting to kilograms per second."""

    _quantity_type = "mass_flow_rate"


class VolumetricFlowRate(BaseQuantity):
    """A volumetric flow rate quantity, defaulting to cubic meters per second."""

    _quantity_type = "volumetric_flow_rate"


class ThermalConductivity(BaseQuantity):
    """A thermal conductivity quantity, defaulting to watts per meter-kelvin."""

    _quantity_type = "thermal_conductivity"


class SpecificHeatCapacity(BaseQuantity):
    """A specific heat capacity quantity, defaulting to joules per kilogram-kelvin."""

    _quantity_type = "specific_heat_capacity"


class HeatFlux(BaseQuantity):
    """A heat flux quantity, defaulting to watts per square meter."""

    _quantity_type = "heat_flux"


# =============================================================================
# Optics
# =============================================================================


class Illuminance(BaseQuantity):
    """An illuminance quantity, defaulting to lux."""

    _quantity_type = "illuminance"

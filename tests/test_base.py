"""Tests for BaseQuantity functionality using Mass as a concrete subclass.

BaseQuantity preserves input units; SI is only used as default when no unit is given.
"""

from __future__ import annotations

import numpy as np
import pytest
from pint import DimensionalityError
from pint import Quantity as PintQuantity

from engunits.base import BaseQuantity
from engunits.config import IMPERIAL_DEFAULTS, SI_DEFAULTS
from engunits.quantities import (
    Acceleration,
    Area,
    Current,
    Energy,
    Force,
    Length,
    Mass,
    Momentum,
    Power,
    Pressure,
    Time,
    Velocity,
    Volume,
)


class TestConstruction:
    """Tests for quantity construction and unit preservation."""

    def test_explicit_unit_preserved(self):
        m = Mass(1000, "lb")
        assert m.units == "lb"
        assert m.value == 1000.0

    def test_no_unit_assumes_si(self):
        m = Mass(500)
        assert m.value == 500.0
        assert m.units == "kg"

    def test_from_pint_quantity(self):
        from engunits.registry import Q_

        pq = Q_(100, "lb")
        m = Mass(pq)
        assert m.units == "lb"
        assert m.value == 100.0

    def test_si_unit_no_conversion(self):
        m = Mass(25, "kg")
        assert m.value == 25.0
        assert m.units == "kg"

    def test_dimensionality_mismatch_caught_at_construction(self):
        with pytest.raises(DimensionalityError):
            Mass(10, "m")

    def test_numpy_array_support(self):
        arr = np.array([1.0, 2.0, 3.0])
        m = Mass(arr, "kg")
        np.testing.assert_array_equal(m.value, arr)

    def test_numpy_array_with_explicit_unit(self):
        arr = np.array([1.0, 2.0, 3.0])
        m = Mass(arr, "lb")
        assert m.units == "lb"
        np.testing.assert_array_equal(m.value, arr)


class TestNorm:
    """Tests for .norm (L2 norm) property."""

    def test_scalar_returns_float(self):
        m = Mass(10, "kg")
        assert m.norm == 10.0
        assert isinstance(m.norm, float)

    def test_scalar_negative(self):
        m = Mass(-5, "kg")
        assert m.norm == -5.0

    def test_array_returns_l2_norm(self):
        f = Force(np.array([3.0, 4.0]), "N")
        assert pytest.approx(f.norm) == 5.0

    def test_array_3d(self):
        f = Force(np.array([1.0, 2.0, 2.0]), "N")
        assert pytest.approx(f.norm) == 3.0

    def test_array_single_element(self):
        m = Mass(np.array([7.0]), "kg")
        assert pytest.approx(m.norm) == 7.0

    def test_array_returns_float(self):
        f = Force(np.array([3.0, 4.0]), "N")
        assert isinstance(f.norm, float)


class TestValueAndConversion:
    """Tests for .value, __call__, and .to()."""

    def test_value_returns_stored_magnitude(self):
        m = Mass(1000, "lb")
        assert m.value == 1000.0

    def test_call_converts_correctly(self):
        m = Mass(1000, "lb")
        m_kg = m("kg")
        assert pytest.approx(m_kg.value, rel=1e-4) == 453.5924

    def test_call_result_value_returns_target_magnitude(self):
        m = Mass(100, "kg")
        assert pytest.approx(m("lb").value, rel=1e-3) == 220.462

    def test_call_returns_same_class(self):
        m = Mass(10, "kg")
        result = m("lb")
        assert isinstance(result, Mass)

    def test_to_method(self):
        m = Mass(100, "kg")
        m_lb = m.to("lb")
        assert isinstance(m_lb, Mass)
        assert pytest.approx(m_lb.value, rel=1e-3) == 220.462


class TestSIAndImperial:
    """Tests for si() and imperial() conversion methods."""

    def test_si_from_imperial(self):
        m = Mass(1, "lb")
        m_si = m.si()
        assert isinstance(m_si, Mass)
        assert m_si.units == "kg"
        assert pytest.approx(m_si.value, rel=1e-4) == 0.453592

    def test_si_already_si_is_noop(self):
        m = Mass(10, "kg")
        m_si = m.si()
        assert m_si.units == "kg"
        assert m_si.value == 10.0

    def test_imperial_from_si(self):
        m = Mass(1, "kg")
        m_imp = m.imperial()
        assert isinstance(m_imp, Mass)
        assert m_imp.units == "lb"
        assert pytest.approx(m_imp.value, rel=1e-3) == 2.20462

    def test_imperial_already_imperial_is_noop(self):
        m = Mass(10, "lb")
        m_imp = m.imperial()
        assert m_imp.units == "lb"
        assert m_imp.value == 10.0

    def test_si_returns_same_class(self):
        f = Force(100, "lbf")
        f_si = f.si()
        assert isinstance(f_si, Force)
        assert f_si.units == SI_DEFAULTS["force"]

    def test_imperial_returns_same_class(self):
        f = Force(100, "N")
        f_imp = f.imperial()
        assert isinstance(f_imp, Force)
        assert f_imp.units == IMPERIAL_DEFAULTS["force"]

    def test_si_velocity(self):
        v = Velocity(100, "ft/s")
        v_si = v.si()
        assert v_si.units == "m / s"
        assert pytest.approx(v_si.value, rel=1e-3) == 30.48

    def test_imperial_velocity(self):
        v = Velocity(10, "m/s")
        v_imp = v.imperial()
        assert v_imp.units == "ft / s"
        assert pytest.approx(v_imp.value, rel=1e-3) == 32.8084

    def test_si_on_cross_type_result(self):
        result = Force(100, "N") / Mass(10, "kg")
        assert isinstance(result, Acceleration)
        result_si = result.si()
        assert result_si.units == "m / s ** 2"
        assert pytest.approx(result_si.value) == 10.0


class TestArithmetic:
    """Tests for arithmetic operators."""

    def test_add_same_type_preserves_units(self):
        a = Mass(1000, "lb")
        b = Mass(500, "lb")
        result = a + b
        assert isinstance(result, Mass)
        assert result.units == "lb"
        assert pytest.approx(result.value, rel=1e-3) == 1500.0

    def test_add_cross_unit_preserves_left_units(self):
        a = Mass(1, "lb")
        b = Mass(1, "kg")
        result = a + b
        assert isinstance(result, Mass)
        assert result.units == "lb"
        assert pytest.approx(result.value, rel=1e-3) == 3.20462

    def test_sub_same_type(self):
        a = Mass(1000, "lb")
        b = Mass(300, "lb")
        result = a - b
        assert isinstance(result, Mass)
        assert result.units == "lb"
        assert pytest.approx(result.value, rel=1e-3) == 700.0

    def test_sub_cross_unit_preserves_left_units(self):
        a = Mass(5, "kg")
        b = Mass(1, "lb")
        result = a - b
        assert isinstance(result, Mass)
        assert result.units == "kg"
        assert pytest.approx(result.value, rel=1e-3) == 4.54608

    def test_mul_scalar(self):
        m = Mass(10, "kg")
        result = m * 3
        assert isinstance(result, Mass)
        assert result.value == 30.0

    def test_rmul_scalar(self):
        m = Mass(10, "kg")
        result = 3 * m
        assert isinstance(result, Mass)
        assert result.value == 30.0

    def test_div_scalar(self):
        m = Mass(30, "kg")
        result = m / 3
        assert isinstance(result, Mass)
        assert result.value == 10.0

    def test_div_same_type_returns_float(self):
        a = Mass(30, "kg")
        b = Mass(10, "kg")
        result = a / b
        assert isinstance(result, float)
        assert result == 3.0

    def test_cross_type_mul_returns_pint(self):
        m = Mass(10, "kg")
        length = Length(5, "m")
        result = m * length
        assert isinstance(result, PintQuantity)

    def test_cross_type_div_returns_typed(self):
        f = Force(100, "N")
        m = Mass(10, "kg")
        result = f / m
        assert isinstance(result, Acceleration)
        assert pytest.approx(result.value) == 10.0

    def test_neg(self):
        m = Mass(10, "kg")
        result = -m
        assert isinstance(result, Mass)
        assert result.value == -10.0

    def test_abs(self):
        m = Mass(-10, "kg")
        result = abs(m)
        assert isinstance(result, Mass)
        assert result.value == 10.0

    def test_pow_returns_typed(self):
        length = Length(3, "m")
        result = length**2
        assert isinstance(result, Area)
        assert pytest.approx(result.value) == 9.0

    def test_rtruediv(self):
        length = Length(2, "m")
        result = 10 / length
        assert isinstance(result, PintQuantity)

    def test_mul_scalar_preserves_imperial(self):
        m = Mass(10, "lb")
        result = m * 3
        assert result.units == "lb"
        assert result.value == 30.0

    def test_div_scalar_preserves_imperial(self):
        m = Mass(30, "lb")
        result = m / 3
        assert result.units == "lb"
        assert result.value == 10.0


class TestTypeMismatch:
    """Tests that operations between incompatible types are rejected."""

    def test_add_different_types_raises(self):
        with pytest.raises(TypeError):
            Mass(1, "kg") + Length(1, "m")

    def test_sub_different_types_raises(self):
        with pytest.raises(TypeError):
            Mass(1, "kg") - Length(1, "m")

    def test_eq_different_types_returns_false(self):
        assert Mass(1, "kg") != Length(1, "m")

    def test_lt_different_types_raises(self):
        with pytest.raises(TypeError):
            assert Mass(1, "kg") < Length(1, "m")


class TestComparisons:
    """Tests for comparison operators."""

    def test_eq_same_units(self):
        assert Mass(10, "kg") == Mass(10, "kg")

    def test_eq_different_units(self):
        m1 = Mass(1, "kg")
        m2 = Mass(1000, "g")
        assert m1 == m2

    def test_neq(self):
        assert Mass(10, "kg") != Mass(20, "kg")

    def test_lt(self):
        assert Mass(5, "kg") < Mass(10, "kg")

    def test_lt_cross_unit(self):
        assert Mass(1, "lb") < Mass(1, "kg")

    def test_le(self):
        assert Mass(5, "kg") <= Mass(5, "kg")
        assert Mass(4, "kg") <= Mass(5, "kg")

    def test_gt(self):
        assert Mass(10, "kg") > Mass(5, "kg")

    def test_ge(self):
        assert Mass(5, "kg") >= Mass(5, "kg")
        assert Mass(6, "kg") >= Mass(5, "kg")


class TestRepresentation:
    """Tests for __repr__, __str__, __float__, __format__."""

    def test_repr(self):
        m = Mass(10, "kg")
        assert repr(m) == "Mass(10, 'kg')"

    def test_str(self):
        m = Mass(10, "kg")
        assert str(m) == "10 kg"

    def test_float(self):
        m = Mass(10, "kg")
        assert float(m) == 10.0

    def test_float_from_non_si(self):
        m = Mass(10, "kg")
        m_lb = m("lb")
        assert pytest.approx(float(m_lb), rel=1e-3) == 22.0462

    def test_format(self):
        m = Mass(10, "kg")
        result = format(m, "~")
        assert "kg" in result

    def test_hash_equal_values(self):
        m1 = Mass(10, "kg")
        m2 = Mass(10, "kg")
        assert hash(m1) == hash(m2)

    def test_hash_eq_consistency_cross_unit(self):
        m1 = Mass(1, "kg")
        m2 = Mass(1000, "g")
        assert m1 == m2
        assert hash(m1) == hash(m2)

    def test_hash_set_membership_cross_unit(self):
        s = {Mass(1, "kg")}
        assert Mass(1000, "g") in s

    def test_quantity_property(self):
        m = Mass(10, "kg")
        assert isinstance(m.quantity, PintQuantity)


class TestInternalConsistency:
    """Tests that internal methods are independent and consistent."""

    def test_to_is_independent_of_call(self):
        """to() works without relying on __call__."""
        m = Mass(100, "kg")
        result = m.to("lb")
        assert isinstance(result, Mass)
        assert pytest.approx(result.value, rel=1e-3) == 220.462

    def test_call_delegates_to_to(self):
        """__call__ produces the same result as to()."""
        m = Mass(100, "kg")
        via_call = m("lb")
        via_to = m.to("lb")
        assert via_call.value == via_to.value
        assert via_call.units == via_to.units

    def test_float_scalar(self):
        """__float__ returns norm for scalar quantities."""
        m = Mass(10, "kg")
        assert float(m) == 10.0

    def test_float_array_raises(self):
        """__float__ raises TypeError for array quantities."""
        f = Force(np.array([3.0, 4.0]), "N")
        with pytest.raises(TypeError, match="cannot convert"):
            float(f)

    def test_hash_array(self):
        """__hash__ works for array quantities (not crash)."""
        f1 = Force(np.array([3.0, 4.0]), "N")
        f2 = Force(np.array([3.0, 4.0]), "N")
        assert hash(f1) == hash(f2)

    def test_norm_uses_value(self):
        """norm is derived from value, not raw _quantity access."""
        m = Mass(10, "kg")
        assert m.norm == float(m.value)

    def test_norm_array_uses_value(self):
        """norm computes L2 norm from value array."""
        f = Force(np.array([3.0, 4.0]), "N")
        np.testing.assert_array_equal(f.value, np.array([3.0, 4.0]))
        assert pytest.approx(f.norm) == 5.0

    def test_repr_uses_value(self):
        """repr reflects value property, not raw _quantity access."""
        m = Mass(10, "kg")
        assert str(m.value) in repr(m)

    def test_str_uses_value(self):
        """str reflects value property, not raw _quantity access."""
        m = Mass(10, "kg")
        assert str(m) == f"{m.value:.6g} {m.units}"

    def test_float_converted_unit(self):
        """__float__ on a converted quantity uses its current norm."""
        m = Mass(10, "kg")
        m_lb = m("lb")
        assert pytest.approx(float(m_lb), rel=1e-3) == m_lb.norm


class TestBool:
    """Tests for __bool__ (truthiness)."""

    def test_nonzero_is_truthy(self):
        assert bool(Mass(10, "kg")) is True

    def test_zero_is_falsy(self):
        assert bool(Mass(0, "kg")) is False

    def test_zero_float_is_falsy(self):
        assert bool(Mass(0.0, "kg")) is False

    def test_negative_is_truthy(self):
        assert bool(Mass(-5, "kg")) is True

    def test_zero_array_is_falsy(self):
        assert bool(Force(np.array([0.0, 0.0]), "N")) is False

    def test_nonzero_array_is_truthy(self):
        assert bool(Force(np.array([0.0, 1.0]), "N")) is True


class TestTypeResolution:
    """Tests for automatic type resolution on cross-type arithmetic."""

    def test_force_div_mass_returns_acceleration(self):
        result = Force(100, "N") / Mass(10, "kg")
        assert isinstance(result, Acceleration)
        assert pytest.approx(result.value) == 10.0

    def test_mass_mul_acceleration_returns_force(self):
        result = Mass(5, "kg") * Acceleration(10)
        assert isinstance(result, Force)
        assert pytest.approx(result.value) == 50.0

    def test_velocity_mul_time_returns_length(self):
        result = Velocity(10) * Time(5)
        assert isinstance(result, Length)
        assert pytest.approx(result.value) == 50.0

    def test_force_div_area_returns_pressure(self):
        result = Force(1000, "N") / Area(2)
        assert isinstance(result, Pressure)
        assert pytest.approx(result.value) == 500.0

    def test_length_squared_returns_area(self):
        result = Length(3, "m") ** 2
        assert isinstance(result, Area)
        assert pytest.approx(result.value) == 9.0

    def test_length_cubed_returns_volume(self):
        result = Length(2, "m") ** 3
        assert isinstance(result, Volume)
        assert pytest.approx(result.value) == 8.0

    def test_energy_div_time_returns_power(self):
        result = Energy(100) / Time(10)
        assert isinstance(result, Power)
        assert pytest.approx(result.value) == 10.0

    def test_ambiguous_moment_energy_returns_pint(self):
        result = Force(10, "N") * Length(5, "m")
        assert isinstance(result, PintQuantity)
        assert not isinstance(result, BaseQuantity)

    def test_ambiguous_frequency_angular_velocity_returns_pint(self):
        """Frequency and AngularVelocity share dimensionality [time]^-1."""
        result = 1 / Time(2, "s")
        assert isinstance(result, PintQuantity)
        assert not isinstance(result, BaseQuantity)

    def test_ambiguous_charge_capacity_returns_pint(self):
        """Charge and Capacity share dimensionality [current]*[time]."""
        result = Current(5, "A") * Time(10, "s")
        assert isinstance(result, PintQuantity)
        assert not isinstance(result, BaseQuantity)

    def test_no_match_returns_pint(self):
        result = Force(10, "N") * Area(2)
        assert isinstance(result, PintQuantity)
        assert not isinstance(result, BaseQuantity)

    def test_rtruediv_no_match_returns_pint(self):
        result = 1 / Mass(2)
        assert isinstance(result, PintQuantity)
        assert not isinstance(result, BaseQuantity)

    def test_cross_type_preserves_units(self):
        """Cross-type results preserve the units from computation."""
        result = Force(100, "N") / Mass(10, "kg")
        assert isinstance(result, Acceleration)
        # pint computes N/kg, not m/s**2
        assert result.units == "N / kg"
        assert pytest.approx(result.value) == 10.0

    def test_cross_type_imperial_preserves_units(self):
        """Imperial inputs produce imperial-style computed units."""
        result = Force(100, "lbf") / Mass(10, "lb")
        assert isinstance(result, Acceleration)
        assert result.units == "lbf / lb"
        assert pytest.approx(result.value) == 10.0

    def test_cross_type_result_si_converts(self):
        """si() on a cross-type result gives canonical SI units."""
        result = Force(100, "lbf") / Mass(10, "lb")
        result_si = result.si()
        assert result_si.units == "m / s ** 2"

    def test_power_div_velocity_returns_force(self):
        result = Power(1000, "W") / Velocity(10, "m/s")
        assert isinstance(result, Force)
        assert pytest.approx(result.value) == 100.0

    def test_momentum_type_resolution(self):
        """Mass * Velocity produces momentum dimensionality — unique resolution."""
        result = Mass(10, "kg") * Velocity(5, "m/s")
        assert isinstance(result, Momentum)
        assert pytest.approx(result.value) == 50.0


class TestAbstractness:
    """Test that BaseQuantity cannot be instantiated directly."""

    def test_cannot_instantiate_base(self):
        with pytest.raises((TypeError, AttributeError)):
            BaseQuantity(10, "kg")

"""Tests for BaseQuantity functionality using Mass as a concrete subclass."""

from __future__ import annotations

import numpy as np
import pytest
from pint import DimensionalityError
from pint import Quantity as PintQuantity

from engunits.base import BaseQuantity
from engunits.quantities import Force, Length, Mass


class TestConstruction:
    """Tests for quantity construction and SI normalization."""

    def test_explicit_unit_converts_to_si(self):
        m = Mass(1000, "lb")
        assert m.units == "kg"
        assert pytest.approx(m.value, rel=1e-4) == 453.5924

    def test_no_unit_assumes_si(self):
        m = Mass(500)
        assert m.value == 500.0
        assert m.units == "kg"

    def test_from_pint_quantity(self):
        from engunits.registry import Q_

        pq = Q_(100, "lb")
        m = Mass(pq)
        assert m.units == "kg"
        assert pytest.approx(m.value, rel=1e-4) == 45.3592

    def test_si_unit_no_conversion(self):
        m = Mass(25, "kg")
        assert m.value == 25.0
        assert m.units == "kg"

    def test_dimensionality_validation_rejects_wrong_units(self):
        with pytest.raises(DimensionalityError):
            Mass(10, "m")

    def test_numpy_array_support(self):
        arr = np.array([1.0, 2.0, 3.0])
        m = Mass(arr, "kg")
        np.testing.assert_array_equal(m.value, arr)

    def test_numpy_array_with_conversion(self):
        arr = np.array([1.0, 2.0, 3.0])
        m = Mass(arr, "lb")
        assert m.units == "kg"
        expected = arr * 0.45359237
        np.testing.assert_allclose(m.value, expected, rtol=1e-4)


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
    """Tests for .value, __call__, .to(), and .in_units_of()."""

    def test_value_returns_si_magnitude(self):
        m = Mass(1000, "lb")
        assert pytest.approx(m.value, rel=1e-4) == 453.5924

    def test_call_converts_correctly(self):
        m = Mass(1000, "lb")
        m_lb = m("lb")
        assert pytest.approx(m_lb.value, rel=1e-4) == 1000.0

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


class TestArithmetic:
    """Tests for arithmetic operators."""

    def test_add_same_type_returns_si(self):
        a = Mass(1000, "lb")
        b = Mass(500, "lb")
        result = a + b
        assert isinstance(result, Mass)
        assert result.units == "kg"
        assert pytest.approx(result("lb").value, rel=1e-3) == 1500.0

    def test_sub_same_type(self):
        a = Mass(1000, "lb")
        b = Mass(300, "lb")
        result = a - b
        assert isinstance(result, Mass)
        assert pytest.approx(result("lb").value, rel=1e-3) == 700.0

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

    def test_cross_type_div_returns_pint(self):
        f = Force(100, "N")
        m = Mass(10, "kg")
        result = f / m
        assert isinstance(result, PintQuantity)

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

    def test_pow_returns_pint(self):
        length = Length(3, "m")
        result = length**2
        assert isinstance(result, PintQuantity)

    def test_rtruediv(self):
        length = Length(2, "m")
        result = 10 / length
        assert isinstance(result, PintQuantity)


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
        # __float__ uses norm property (L2 norm / scalar value)
        assert pytest.approx(float(m_lb), rel=1e-3) == 22.0462

    def test_format(self):
        m = Mass(10, "kg")
        result = format(m, "~")
        assert "kg" in result

    def test_hash_equal_values(self):
        m1 = Mass(10, "kg")
        m2 = Mass(10, "kg")
        assert hash(m1) == hash(m2)

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


class TestAbstractness:
    """Test that BaseQuantity cannot be instantiated directly."""

    def test_cannot_instantiate_base(self):
        with pytest.raises((TypeError, AttributeError)):
            BaseQuantity(10, "kg")

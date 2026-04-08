"""Base quantity class with unit-preserving storage and on-demand conversion."""

from __future__ import annotations

from abc import ABC
from typing import ClassVar

import numpy as np
from pint import DimensionalityError
from pint import Quantity as PintQuantity

from engunits.config import IMPERIAL_DEFAULTS, SI_DEFAULTS
from engunits.registry import Q_


class BaseQuantity(ABC):
    """Abstract base for dimensioned quantities.

    Preserves the units given at construction. When no unit is specified, SI
    units are used as the default. Supports on-demand conversion via callable
    syntax: ``mass("lb")`` returns a new instance in pounds.

    Subclasses must define ``_quantity_type`` matching a key in ``SI_DEFAULTS``.
    """

    _quantity_type: str
    _dimensionality_registry: ClassVar[dict] = {}
    _ambiguous_dimensionalities: ClassVar[set] = set()

    def __init_subclass__(cls, **kwargs: object) -> None:
        """Register subclass dimensionality for automatic type resolution."""
        super().__init_subclass__(**kwargs)
        try:
            si_unit = SI_DEFAULTS[cls._quantity_type]
        except (AttributeError, KeyError):
            return
        dim = Q_(1, si_unit).dimensionality
        if dim in BaseQuantity._ambiguous_dimensionalities:
            return
        if dim in BaseQuantity._dimensionality_registry:
            del BaseQuantity._dimensionality_registry[dim]
            BaseQuantity._ambiguous_dimensionalities.add(dim)
        else:
            BaseQuantity._dimensionality_registry[dim] = cls

    @classmethod
    def _resolve_type(cls, pint_quantity: PintQuantity) -> BaseQuantity | PintQuantity:
        """Wrap a pint Quantity in the matching typed class, or return it raw.

        Preserves the units from the computation rather than converting to SI.
        Ambiguous dimensionalities (matching multiple types) return a raw pint
        Quantity — the caller can cast to a specific type if needed.
        """
        try:
            matched_cls = BaseQuantity._dimensionality_registry[pint_quantity.dimensionality]
        except KeyError:
            return pint_quantity
        instance = object.__new__(matched_cls)
        instance._quantity = pint_quantity
        return instance

    def __init__(self, value: float | np.ndarray | PintQuantity, unit: str | None = None) -> None:
        si_unit = SI_DEFAULTS[self._quantity_type]
        try:
            unit = unit or str(value.units)
        except AttributeError:
            unit = unit or si_unit
        self._quantity = Q_(value, unit)
        try:
            self._quantity.to(si_unit)
        except DimensionalityError:
            raise DimensionalityError(unit, si_unit) from None

    # -- Properties ----------------------------------------------------------

    @property
    def value(self) -> float | np.ndarray:
        """Raw numeric value in current units."""
        return self._quantity.magnitude

    @property
    def magnitude(self) -> float | np.ndarray:
        """Raw numeric value in current units. Alias for :attr:`value` for pint compatibility."""
        return self.value

    @property
    def norm(self) -> float:
        """Scalar magnitude as float, or L2 norm for array values."""
        mag = self._quantity.magnitude
        try:
            return float(mag)
        except TypeError:
            return float(np.linalg.norm(mag))

    @property
    def units(self) -> str:
        """Current unit string."""
        return str(self._quantity.units)

    @property
    def quantity(self) -> PintQuantity:
        """Underlying pint Quantity."""
        return self._quantity

    # -- Conversion ----------------------------------------------------------

    def to(self, unit: str) -> BaseQuantity:
        """Convert to a different unit. Returns a new instance.

        Args:
            unit: Target unit string.
        """
        converted = self._quantity.to(unit)
        instance = object.__new__(self.__class__)
        instance._quantity = converted
        return instance

    def __call__(self, unit: str) -> BaseQuantity:
        """Return new instance converted to the given unit.

        Syntactic sugar for :meth:`to`. Allows ``mass("lb")`` syntax.

        Args:
            unit: Target unit string (e.g. ``"lb"``, ``"ft/s"``).

        Returns:
            New instance of the same type with the converted value.
        """
        return self.to(unit)

    def si(self) -> BaseQuantity:
        """Return new instance converted to SI units.

        Returns:
            New instance of the same type in SI default units.
        """
        return self.to(SI_DEFAULTS[self._quantity_type])

    def imperial(self) -> BaseQuantity:
        """Return new instance converted to Imperial/US customary units.

        Returns:
            New instance of the same type in Imperial default units.
        """
        return self.to(IMPERIAL_DEFAULTS[self._quantity_type])

    # -- Arithmetic ----------------------------------------------------------

    def __add__(self, other: BaseQuantity) -> BaseQuantity:
        if type(self) is not type(other):
            return NotImplemented
        result = (self._quantity + other._quantity).to(self._quantity.units)
        instance = object.__new__(self.__class__)
        instance._quantity = result
        return instance

    def __radd__(self, other: int | BaseQuantity) -> BaseQuantity:
        if other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other: BaseQuantity) -> BaseQuantity:
        if type(self) is not type(other):
            return NotImplemented
        result = (self._quantity - other._quantity).to(self._quantity.units)
        instance = object.__new__(self.__class__)
        instance._quantity = result
        return instance

    def __rsub__(self, other: BaseQuantity) -> BaseQuantity:
        if type(self) is not type(other):
            return NotImplemented
        result = (other._quantity - self._quantity).to(other._quantity.units)
        instance = object.__new__(self.__class__)
        instance._quantity = result
        return instance

    def __mul__(self, other: float | int | np.ndarray) -> BaseQuantity | PintQuantity:
        try:
            return self._resolve_type(self._quantity * other._quantity)
        except AttributeError:
            try:
                return self.__class__(self._quantity * other)
            except TypeError:
                return NotImplemented

    def __rmul__(self, other: float | int | np.ndarray) -> BaseQuantity | PintQuantity:
        return self.__mul__(other)

    def __truediv__(
        self,
        other: float | int | np.ndarray | BaseQuantity,
    ) -> BaseQuantity | PintQuantity | float:
        try:
            result = self._quantity / other._quantity
        except AttributeError:
            try:
                return self.__class__(self._quantity / other)
            except TypeError:
                return NotImplemented
        else:
            if type(self) is type(other):
                return float(result.to("dimensionless").magnitude)
            return self._resolve_type(result)

    def __rtruediv__(self, other: float | int) -> PintQuantity:
        try:
            return self._resolve_type(other / self._quantity)
        except TypeError:
            return NotImplemented

    def __pow__(self, exponent: int | float) -> PintQuantity:
        return self._resolve_type(self._quantity**exponent)

    def __neg__(self) -> BaseQuantity:
        instance = object.__new__(self.__class__)
        instance._quantity = -self._quantity
        return instance

    def __abs__(self) -> BaseQuantity:
        instance = object.__new__(self.__class__)
        instance._quantity = abs(self._quantity)
        return instance

    # -- Comparisons ---------------------------------------------------------

    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return bool(self._quantity == other._quantity)

    def __lt__(self, other: BaseQuantity) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return bool(self._quantity < other._quantity)

    def __le__(self, other: BaseQuantity) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return bool(self._quantity <= other._quantity)

    def __gt__(self, other: BaseQuantity) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return bool(self._quantity > other._quantity)

    def __ge__(self, other: BaseQuantity) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return bool(self._quantity >= other._quantity)

    # -- Representation ------------------------------------------------------

    def __repr__(self) -> str:
        mag = self._quantity.magnitude
        units = str(self._quantity.units)
        try:
            return f"{self.__class__.__name__}({mag:.6g}, '{units}')"
        except TypeError:
            return f"{self.__class__.__name__}({mag!r}, '{units}')"

    def __str__(self) -> str:
        mag = self._quantity.magnitude
        units = str(self._quantity.units)
        try:
            return f"{mag:.6g} {units}"
        except TypeError:
            return f"{mag} {units}"

    def __format__(self, format_spec: str) -> str:
        return format(self._quantity, format_spec)

    def __float__(self) -> float:
        mag = self._quantity.magnitude
        try:
            return float(mag)
        except TypeError:
            msg = f"cannot convert {self.__class__.__name__} with array value to float"
            raise TypeError(msg) from None

    def __bool__(self) -> bool:
        """Return False only when the SI-normalized magnitude is zero."""
        si_unit = SI_DEFAULTS[self._quantity_type]
        mag = self._quantity.to(si_unit).magnitude
        try:
            return bool(mag != 0)
        except ValueError:
            return bool(np.any(mag != 0))

    def __hash__(self) -> int:
        si_unit = SI_DEFAULTS[self._quantity_type]
        mag = self._quantity.to(si_unit).magnitude
        try:
            return hash((self.__class__, float(mag)))
        except TypeError:
            return hash((self.__class__, float(np.linalg.norm(mag))))

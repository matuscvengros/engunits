"""Base quantity class with unit-preserving storage and on-demand conversion."""

from __future__ import annotations

from abc import ABC

import numpy as np
from pint import Quantity as PintQuantity

from engunits.config import SI_DEFAULTS
from engunits.registry import Q_


class BaseQuantity(ABC):
    """Abstract base for dimensioned quantities.

    Preserves the units given at construction. When no unit is specified, SI
    units are used as the default. Supports on-demand conversion via callable
    syntax: ``mass("lb")`` returns a new instance in pounds.

    Subclasses must define ``_quantity_type`` matching a key in ``SI_DEFAULTS``.
    """

    _quantity_type: str

    def __init__(self, value: float | np.ndarray | PintQuantity, unit: str | None = None) -> None:
        si_unit = SI_DEFAULTS[self._quantity_type]
        try:
            unit = unit or str(value.units)
        except AttributeError:
            unit = unit or si_unit
        self._quantity = Q_(value, unit)

    # -- Properties ----------------------------------------------------------

    @property
    def value(self) -> float | np.ndarray:
        """Raw numeric value in current units."""
        return self._quantity.magnitude

    @property
    def magnitude(self) -> float | np.ndarray:
        """Raw numeric value in current units. Alias for :attr:`value`."""
        return self._quantity.magnitude

    @property
    def norm(self) -> float:
        """Vector magnitude (L2 norm) of the quantity."""
        mag = self._quantity.magnitude
        try:
            _ = mag.shape
            return float(np.linalg.norm(mag))
        except AttributeError:
            return float(mag)

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

    # -- Arithmetic ----------------------------------------------------------

    def __add__(self, other: BaseQuantity) -> BaseQuantity:
        if type(self) is not type(other):
            return NotImplemented
        return self.__class__(self._quantity + other._quantity)

    def __radd__(self, other: BaseQuantity) -> BaseQuantity:
        return self.__add__(other)

    def __sub__(self, other: BaseQuantity) -> BaseQuantity:
        if type(self) is not type(other):
            return NotImplemented
        return self.__class__(self._quantity - other._quantity)

    def __rsub__(self, other: BaseQuantity) -> BaseQuantity:
        if type(self) is not type(other):
            return NotImplemented
        return self.__class__(other._quantity - self._quantity)

    def __mul__(self, other: float | int | np.ndarray) -> BaseQuantity | PintQuantity:
        try:
            return self._quantity * other._quantity
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
            return result

    def __rtruediv__(self, other: float | int) -> PintQuantity:
        try:
            return other / self._quantity
        except TypeError:
            return NotImplemented

    def __pow__(self, exponent: int | float) -> PintQuantity:
        return self._quantity**exponent

    def __neg__(self) -> BaseQuantity:
        return self.__class__(-self._quantity)

    def __abs__(self) -> BaseQuantity:
        return self.__class__(abs(self._quantity))

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
            _ = mag.shape
            return f"{self.__class__.__name__}({mag!r}, '{units}')"
        except AttributeError:
            return f"{self.__class__.__name__}({mag:.6g}, '{units}')"

    def __str__(self) -> str:
        mag = self._quantity.magnitude
        units = str(self._quantity.units)
        try:
            _ = mag.shape
            return f"{mag} {units}"
        except AttributeError:
            return f"{mag:.6g} {units}"

    def __format__(self, format_spec: str) -> str:
        return format(self._quantity, format_spec)

    def __float__(self) -> float:
        mag = self._quantity.magnitude
        try:
            _ = mag.shape
        except AttributeError:
            return float(mag)
        msg = f"cannot convert {self.__class__.__name__} with array value to float"
        raise TypeError(msg)

    def __hash__(self) -> int:
        mag = self._quantity.magnitude
        try:
            _ = mag.shape
            return hash((self.__class__, float(np.linalg.norm(mag))))
        except AttributeError:
            return hash((self.__class__, float(mag)))

"""Damage"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.units_and_measurements.measurements import _1839

_DAMAGE = python_net_import(
    "SMT.MastaAPI.Utility.UnitsAndMeasurements.Measurements", "Damage"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.units_and_measurements import _1797

    Self = TypeVar("Self", bound="Damage")
    CastSelf = TypeVar("CastSelf", bound="Damage._Cast_Damage")


__docformat__ = "restructuredtext en"
__all__ = ("Damage",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Damage:
    """Special nested class for casting Damage to subclasses."""

    __parent__: "Damage"

    @property
    def fraction_measurement_base(self: "CastSelf") -> "_1839.FractionMeasurementBase":
        return self.__parent__._cast(_1839.FractionMeasurementBase)

    @property
    def measurement_base(self: "CastSelf") -> "_1797.MeasurementBase":
        from mastapy._private.utility.units_and_measurements import _1797

        return self.__parent__._cast(_1797.MeasurementBase)

    @property
    def damage(self: "CastSelf") -> "Damage":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class Damage(_1839.FractionMeasurementBase):
    """Damage

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DAMAGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_Damage":
        """Cast to another type.

        Returns:
            _Cast_Damage
        """
        return _Cast_Damage(self)

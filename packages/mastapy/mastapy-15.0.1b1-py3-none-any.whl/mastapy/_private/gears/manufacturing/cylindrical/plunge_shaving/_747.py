"""GearPointCalculationError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _745

_GEAR_POINT_CALCULATION_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "GearPointCalculationError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearPointCalculationError")
    CastSelf = TypeVar(
        "CastSelf", bound="GearPointCalculationError._Cast_GearPointCalculationError"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearPointCalculationError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearPointCalculationError:
    """Special nested class for casting GearPointCalculationError to subclasses."""

    __parent__: "GearPointCalculationError"

    @property
    def calculation_error(self: "CastSelf") -> "_745.CalculationError":
        return self.__parent__._cast(_745.CalculationError)

    @property
    def gear_point_calculation_error(self: "CastSelf") -> "GearPointCalculationError":
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
class GearPointCalculationError(_745.CalculationError):
    """GearPointCalculationError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_POINT_CALCULATION_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearPointCalculationError":
        """Cast to another type.

        Returns:
            _Cast_GearPointCalculationError
        """
        return _Cast_GearPointCalculationError(self)

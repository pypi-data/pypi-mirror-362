"""ShaverPointCalculationError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.plunge_shaving import _745

_SHAVER_POINT_CALCULATION_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.PlungeShaving",
    "ShaverPointCalculationError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaverPointCalculationError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaverPointCalculationError._Cast_ShaverPointCalculationError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaverPointCalculationError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaverPointCalculationError:
    """Special nested class for casting ShaverPointCalculationError to subclasses."""

    __parent__: "ShaverPointCalculationError"

    @property
    def calculation_error(self: "CastSelf") -> "_745.CalculationError":
        return self.__parent__._cast(_745.CalculationError)

    @property
    def shaver_point_calculation_error(
        self: "CastSelf",
    ) -> "ShaverPointCalculationError":
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
class ShaverPointCalculationError(_745.CalculationError):
    """ShaverPointCalculationError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAVER_POINT_CALCULATION_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def achieved_shaver_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AchievedShaverRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def achieved_shaver_z_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AchievedShaverZPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaverRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaver_z_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaverZPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_error(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalError")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ShaverPointCalculationError":
        """Cast to another type.

        Returns:
            _Cast_ShaverPointCalculationError
        """
        return _Cast_ShaverPointCalculationError(self)

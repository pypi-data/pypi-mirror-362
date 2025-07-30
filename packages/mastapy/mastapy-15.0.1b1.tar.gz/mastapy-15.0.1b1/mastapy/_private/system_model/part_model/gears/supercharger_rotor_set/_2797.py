"""RotorSetMeasuredPoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ROTOR_SET_MEASURED_POINT = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears.SuperchargerRotorSet",
    "RotorSetMeasuredPoint",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RotorSetMeasuredPoint")
    CastSelf = TypeVar(
        "CastSelf", bound="RotorSetMeasuredPoint._Cast_RotorSetMeasuredPoint"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotorSetMeasuredPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorSetMeasuredPoint:
    """Special nested class for casting RotorSetMeasuredPoint to subclasses."""

    __parent__: "RotorSetMeasuredPoint"

    @property
    def rotor_set_measured_point(self: "CastSelf") -> "RotorSetMeasuredPoint":
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
class RotorSetMeasuredPoint(_0.APIBase):
    """RotorSetMeasuredPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_SET_MEASURED_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def boost_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoostPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def input_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rotor_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_RotorSetMeasuredPoint":
        """Cast to another type.

        Returns:
            _Cast_RotorSetMeasuredPoint
        """
        return _Cast_RotorSetMeasuredPoint(self)

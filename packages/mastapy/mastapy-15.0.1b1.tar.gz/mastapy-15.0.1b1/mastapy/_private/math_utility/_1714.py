"""SinCurve"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SIN_CURVE = python_net_import("SMT.MastaAPI.MathUtility", "SinCurve")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SinCurve")
    CastSelf = TypeVar("CastSelf", bound="SinCurve._Cast_SinCurve")


__docformat__ = "restructuredtext en"
__all__ = ("SinCurve",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SinCurve:
    """Special nested class for casting SinCurve to subclasses."""

    __parent__: "SinCurve"

    @property
    def sin_curve(self: "CastSelf") -> "SinCurve":
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
class SinCurve(_0.APIBase):
    """SinCurve

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SIN_CURVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_cycles(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCycles")

        if temp is None:
            return 0.0

        return temp

    @number_of_cycles.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycles(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfCycles", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def starting_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartingAngle")

        if temp is None:
            return 0.0

        return temp

    @starting_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def starting_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartingAngle", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SinCurve":
        """Cast to another type.

        Returns:
            _Cast_SinCurve
        """
        return _Cast_SinCurve(self)

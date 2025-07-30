"""SNCurvePoint"""

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

_SN_CURVE_POINT = python_net_import("SMT.MastaAPI.Materials", "SNCurvePoint")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SNCurvePoint")
    CastSelf = TypeVar("CastSelf", bound="SNCurvePoint._Cast_SNCurvePoint")


__docformat__ = "restructuredtext en"
__all__ = ("SNCurvePoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SNCurvePoint:
    """Special nested class for casting SNCurvePoint to subclasses."""

    __parent__: "SNCurvePoint"

    @property
    def sn_curve_point(self: "CastSelf") -> "SNCurvePoint":
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
class SNCurvePoint(_0.APIBase):
    """SNCurvePoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SN_CURVE_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SNCurvePoint":
        """Cast to another type.

        Returns:
            _Cast_SNCurvePoint
        """
        return _Cast_SNCurvePoint(self)

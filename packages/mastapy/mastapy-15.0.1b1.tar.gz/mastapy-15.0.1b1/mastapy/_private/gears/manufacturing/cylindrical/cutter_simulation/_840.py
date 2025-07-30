"""FinishStockPoint"""

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

_FINISH_STOCK_POINT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation", "FinishStockPoint"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FinishStockPoint")
    CastSelf = TypeVar("CastSelf", bound="FinishStockPoint._Cast_FinishStockPoint")


__docformat__ = "restructuredtext en"
__all__ = ("FinishStockPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FinishStockPoint:
    """Special nested class for casting FinishStockPoint to subclasses."""

    __parent__: "FinishStockPoint"

    @property
    def finish_stock_point(self: "CastSelf") -> "FinishStockPoint":
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
class FinishStockPoint(_0.APIBase):
    """FinishStockPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FINISH_STOCK_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def finish_stock_arc_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishStockArcLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def finish_stock_tangent_to_the_base_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FinishStockTangentToTheBaseCircle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def index(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Index")

        if temp is None:
            return ""

        return temp

    @index.setter
    @exception_bridge
    @enforce_parameter_types
    def index(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Index", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FinishStockPoint":
        """Cast to another type.

        Returns:
            _Cast_FinishStockPoint
        """
        return _Cast_FinishStockPoint(self)

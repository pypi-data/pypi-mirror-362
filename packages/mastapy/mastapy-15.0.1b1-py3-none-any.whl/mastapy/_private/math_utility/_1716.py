"""StressPoint"""

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

_STRESS_POINT = python_net_import("SMT.MastaAPI.MathUtility", "StressPoint")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _27

    Self = TypeVar("Self", bound="StressPoint")
    CastSelf = TypeVar("CastSelf", bound="StressPoint._Cast_StressPoint")


__docformat__ = "restructuredtext en"
__all__ = ("StressPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StressPoint:
    """Special nested class for casting StressPoint to subclasses."""

    __parent__: "StressPoint"

    @property
    def shaft_point_stress(self: "CastSelf") -> "_27.ShaftPointStress":
        from mastapy._private.shafts import _27

        return self.__parent__._cast(_27.ShaftPointStress)

    @property
    def stress_point(self: "CastSelf") -> "StressPoint":
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
class StressPoint(_0.APIBase):
    """StressPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRESS_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def x_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def y_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_StressPoint":
        """Cast to another type.

        Returns:
            _Cast_StressPoint
        """
        return _Cast_StressPoint(self)

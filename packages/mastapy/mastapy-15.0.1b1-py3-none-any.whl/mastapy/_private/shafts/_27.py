"""ShaftPointStress"""

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
from mastapy._private.math_utility import _1716

_SHAFT_POINT_STRESS = python_net_import("SMT.MastaAPI.Shafts", "ShaftPointStress")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftPointStress")
    CastSelf = TypeVar("CastSelf", bound="ShaftPointStress._Cast_ShaftPointStress")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftPointStress",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftPointStress:
    """Special nested class for casting ShaftPointStress to subclasses."""

    __parent__: "ShaftPointStress"

    @property
    def stress_point(self: "CastSelf") -> "_1716.StressPoint":
        return self.__parent__._cast(_1716.StressPoint)

    @property
    def shaft_point_stress(self: "CastSelf") -> "ShaftPointStress":
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
class ShaftPointStress(_1716.StressPoint):
    """ShaftPointStress

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_POINT_STRESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_of_max_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleOfMaxBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_principal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPrincipalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_principal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumPrincipalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def von_mises_stress_max(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VonMisesStressMax")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftPointStress":
        """Cast to another type.

        Returns:
            _Cast_ShaftPointStress
        """
        return _Cast_ShaftPointStress(self)

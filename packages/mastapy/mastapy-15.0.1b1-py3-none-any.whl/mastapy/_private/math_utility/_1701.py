"""InertiaTensor"""

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

_INERTIA_TENSOR = python_net_import("SMT.MastaAPI.MathUtility", "InertiaTensor")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InertiaTensor")
    CastSelf = TypeVar("CastSelf", bound="InertiaTensor._Cast_InertiaTensor")


__docformat__ = "restructuredtext en"
__all__ = ("InertiaTensor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_InertiaTensor:
    """Special nested class for casting InertiaTensor to subclasses."""

    __parent__: "InertiaTensor"

    @property
    def inertia_tensor(self: "CastSelf") -> "InertiaTensor":
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
class InertiaTensor(_0.APIBase):
    """InertiaTensor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INERTIA_TENSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def x_axis_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XAxisInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def xy_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XYInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def xz_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "XZInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def y_axis_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YAxisInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yz_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YZInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def z_axis_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZAxisInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_InertiaTensor":
        """Cast to another type.

        Returns:
            _Cast_InertiaTensor
        """
        return _Cast_InertiaTensor(self)

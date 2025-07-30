"""ShaftGroove"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.shafts import _21

_SHAFT_GROOVE = python_net_import("SMT.MastaAPI.Shafts", "ShaftGroove")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _45

    Self = TypeVar("Self", bound="ShaftGroove")
    CastSelf = TypeVar("CastSelf", bound="ShaftGroove._Cast_ShaftGroove")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftGroove",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftGroove:
    """Special nested class for casting ShaftGroove to subclasses."""

    __parent__: "ShaftGroove"

    @property
    def shaft_feature(self: "CastSelf") -> "_21.ShaftFeature":
        return self.__parent__._cast(_21.ShaftFeature)

    @property
    def shaft_groove(self: "CastSelf") -> "ShaftGroove":
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
class ShaftGroove(_21.ShaftFeature):
    """ShaftGroove

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_GROOVE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Depth")

        if temp is None:
            return 0.0

        return temp

    @depth.setter
    @exception_bridge
    @enforce_parameter_types
    def depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Depth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def fillet_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilletRadius")

        if temp is None:
            return 0.0

        return temp

    @fillet_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def fillet_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FilletRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def surface_roughness(self: "Self") -> "_45.ShaftSurfaceRoughness":
        """mastapy.shafts.ShaftSurfaceRoughness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceRoughness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def add_new_groove(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddNewGroove")

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftGroove":
        """Cast to another type.

        Returns:
            _Cast_ShaftGroove
        """
        return _Cast_ShaftGroove(self)

"""ShaftSurfaceFinishSection"""

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

_SHAFT_SURFACE_FINISH_SECTION = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftSurfaceFinishSection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _45

    Self = TypeVar("Self", bound="ShaftSurfaceFinishSection")
    CastSelf = TypeVar(
        "CastSelf", bound="ShaftSurfaceFinishSection._Cast_ShaftSurfaceFinishSection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSurfaceFinishSection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSurfaceFinishSection:
    """Special nested class for casting ShaftSurfaceFinishSection to subclasses."""

    __parent__: "ShaftSurfaceFinishSection"

    @property
    def shaft_feature(self: "CastSelf") -> "_21.ShaftFeature":
        return self.__parent__._cast(_21.ShaftFeature)

    @property
    def shaft_surface_finish_section(self: "CastSelf") -> "ShaftSurfaceFinishSection":
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
class ShaftSurfaceFinishSection(_21.ShaftFeature):
    """ShaftSurfaceFinishSection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SURFACE_FINISH_SECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
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
    def add_new_surface_finish_section(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddNewSurfaceFinishSection")

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftSurfaceFinishSection":
        """Cast to another type.

        Returns:
            _Cast_ShaftSurfaceFinishSection
        """
        return _Cast_ShaftSurfaceFinishSection(self)

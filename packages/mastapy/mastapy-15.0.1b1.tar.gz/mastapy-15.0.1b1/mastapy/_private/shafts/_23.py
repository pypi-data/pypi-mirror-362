"""ShaftKey"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.shafts import _21

_SHAFT_KEY = python_net_import("SMT.MastaAPI.Shafts", "ShaftKey")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.shafts import _48

    Self = TypeVar("Self", bound="ShaftKey")
    CastSelf = TypeVar("CastSelf", bound="ShaftKey._Cast_ShaftKey")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftKey",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftKey:
    """Special nested class for casting ShaftKey to subclasses."""

    __parent__: "ShaftKey"

    @property
    def shaft_feature(self: "CastSelf") -> "_21.ShaftFeature":
        return self.__parent__._cast(_21.ShaftFeature)

    @property
    def shaft_key(self: "CastSelf") -> "ShaftKey":
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
class ShaftKey(_21.ShaftFeature):
    """ShaftKey

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_KEY

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
    def number_of_keys(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfKeys")

        if temp is None:
            return 0

        return temp

    @number_of_keys.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_keys(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfKeys", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def surface_finish(self: "Self") -> "_48.SurfaceFinishes":
        """mastapy.shafts.SurfaceFinishes"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceFinish")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Shafts.SurfaceFinishes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.shafts._48", "SurfaceFinishes"
        )(value)

    @surface_finish.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_finish(self: "Self", value: "_48.SurfaceFinishes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Shafts.SurfaceFinishes")
        pythonnet_property_set(self.wrapped, "SurfaceFinish", value)

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ShaftKey":
        """Cast to another type.

        Returns:
            _Cast_ShaftKey
        """
        return _Cast_ShaftKey(self)

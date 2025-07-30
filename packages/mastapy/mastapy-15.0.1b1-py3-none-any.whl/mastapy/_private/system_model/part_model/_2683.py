"""GuideImage"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GUIDE_IMAGE = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "GuideImage")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GuideImage")
    CastSelf = TypeVar("CastSelf", bound="GuideImage._Cast_GuideImage")


__docformat__ = "restructuredtext en"
__all__ = ("GuideImage",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GuideImage:
    """Special nested class for casting GuideImage to subclasses."""

    __parent__: "GuideImage"

    @property
    def guide_image(self: "CastSelf") -> "GuideImage":
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
class GuideImage(_0.APIBase):
    """GuideImage

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GUIDE_IMAGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def distance_from_left_to_origin(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceFromLeftToOrigin")

        if temp is None:
            return 0.0

        return temp

    @distance_from_left_to_origin.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_from_left_to_origin(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceFromLeftToOrigin",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def distance_from_top_to_centre(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceFromTopToCentre")

        if temp is None:
            return 0.0

        return temp

    @distance_from_top_to_centre.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_from_top_to_centre(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceFromTopToCentre",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def image(self: "Self") -> "Image":
        """Image"""
        temp = pythonnet_property_get(self.wrapped, "Image")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @image.setter
    @exception_bridge
    @enforce_parameter_types
    def image(self: "Self", value: "Image") -> None:
        value = conversion.mp_to_pn_smt_bitmap(value)
        pythonnet_property_set(self.wrapped, "Image", value)

    @property
    @exception_bridge
    def image_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ImageHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def image_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ImageWidth")

        if temp is None:
            return 0.0

        return temp

    @image_width.setter
    @exception_bridge
    @enforce_parameter_types
    def image_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ImageWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def transparency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Transparency")

        if temp is None:
            return 0.0

        return temp

    @transparency.setter
    @exception_bridge
    @enforce_parameter_types
    def transparency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Transparency", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_GuideImage":
        """Cast to another type.

        Returns:
            _Cast_GuideImage
        """
        return _Cast_GuideImage(self)

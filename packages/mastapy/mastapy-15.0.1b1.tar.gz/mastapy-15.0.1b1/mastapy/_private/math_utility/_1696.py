"""FacetedSurface"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_FACETED_SURFACE = python_net_import("SMT.MastaAPI.MathUtility", "FacetedSurface")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="FacetedSurface")
    CastSelf = TypeVar("CastSelf", bound="FacetedSurface._Cast_FacetedSurface")


__docformat__ = "restructuredtext en"
__all__ = ("FacetedSurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FacetedSurface:
    """Special nested class for casting FacetedSurface to subclasses."""

    __parent__: "FacetedSurface"

    @property
    def faceted_surface(self: "CastSelf") -> "FacetedSurface":
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
class FacetedSurface(_0.APIBase):
    """FacetedSurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACETED_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def body_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BodyIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def facets(self: "Self") -> "List[List[int]]":
        """List[List[int]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Facets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, int)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def normals(self: "Self") -> "List[List[float]]":
        """List[List[float]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Normals")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def vertices(self: "Self") -> "List[List[float]]":
        """List[List[float]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Vertices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FacetedSurface":
        """Cast to another type.

        Returns:
            _Cast_FacetedSurface
        """
        return _Cast_FacetedSurface(self)

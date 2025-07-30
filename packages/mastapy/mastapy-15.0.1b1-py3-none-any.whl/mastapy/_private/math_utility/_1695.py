"""FacetedBody"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FACETED_BODY = python_net_import("SMT.MastaAPI.MathUtility", "FacetedBody")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1696

    Self = TypeVar("Self", bound="FacetedBody")
    CastSelf = TypeVar("CastSelf", bound="FacetedBody._Cast_FacetedBody")


__docformat__ = "restructuredtext en"
__all__ = ("FacetedBody",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FacetedBody:
    """Special nested class for casting FacetedBody to subclasses."""

    __parent__: "FacetedBody"

    @property
    def faceted_body(self: "CastSelf") -> "FacetedBody":
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
class FacetedBody(_0.APIBase):
    """FacetedBody

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACETED_BODY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def surfaces(self: "Self") -> "List[_1696.FacetedSurface]":
        """List[mastapy.math_utility.FacetedSurface]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Surfaces")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def add_surface(
        self: "Self",
        vertices: "List[List[float]]",
        normals: "List[List[float]]",
        facets: "List[List[int]]",
        body_index: "int",
    ) -> None:
        """Method does not return.

        Args:
            vertices (List[List[float]])
            normals (List[List[float]])
            facets (List[List[int]])
            body_index (int)
        """
        vertices = conversion.mp_to_pn_objects_in_list(vertices)
        normals = conversion.mp_to_pn_objects_in_list(normals)
        facets = conversion.mp_to_pn_objects_in_list(facets)
        body_index = int(body_index)
        pythonnet_method_call(
            self.wrapped,
            "AddSurface",
            vertices,
            normals,
            facets,
            body_index if body_index else 0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FacetedBody":
        """Cast to another type.

        Returns:
            _Cast_FacetedBody
        """
        return _Cast_FacetedBody(self)

"""CirclesOnAxis"""

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
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private._math.vector_3d import Vector3D

_DOUBLE = python_net_import("System", "Double")
_CIRCLES_ON_AXIS = python_net_import("SMT.MastaAPI.MathUtility", "CirclesOnAxis")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="CirclesOnAxis")
    CastSelf = TypeVar("CastSelf", bound="CirclesOnAxis._Cast_CirclesOnAxis")


__docformat__ = "restructuredtext en"
__all__ = ("CirclesOnAxis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CirclesOnAxis:
    """Special nested class for casting CirclesOnAxis to subclasses."""

    __parent__: "CirclesOnAxis"

    @property
    def circles_on_axis(self: "CastSelf") -> "CirclesOnAxis":
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
class CirclesOnAxis(_0.APIBase):
    """CirclesOnAxis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CIRCLES_ON_AXIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axis(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Axis")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @axis.setter
    @exception_bridge
    @enforce_parameter_types
    def axis(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Axis", value)

    @property
    @exception_bridge
    def coord_fillet_radii(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoordFilletRadii")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def coords(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Coords")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mouse_position(self: "Self") -> "Vector2D":
        """Vector2D"""
        temp = pythonnet_property_get(self.wrapped, "MousePosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @mouse_position.setter
    @exception_bridge
    @enforce_parameter_types
    def mouse_position(self: "Self", value: "Vector2D") -> None:
        value = conversion.mp_to_pn_vector2d(value)
        pythonnet_property_set(self.wrapped, "MousePosition", value)

    @property
    @exception_bridge
    def origin(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Origin")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @origin.setter
    @exception_bridge
    @enforce_parameter_types
    def origin(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Origin", value)

    @exception_bridge
    @enforce_parameter_types
    def add_coords_from_point_in_sketch_plane(
        self: "Self", point_in_sketch_plane: "Vector3D"
    ) -> None:
        """Method does not return.

        Args:
            point_in_sketch_plane (Vector3D)
        """
        point_in_sketch_plane = conversion.mp_to_pn_vector3d(point_in_sketch_plane)
        pythonnet_method_call_overload(
            self.wrapped, "AddCoords", [Vector3D], point_in_sketch_plane
        )

    @exception_bridge
    @enforce_parameter_types
    def add_coords_from_point_on_axis(
        self: "Self", point_on_axis: "Vector3D", radius: "float"
    ) -> None:
        """Method does not return.

        Args:
            point_on_axis (Vector3D)
            radius (float)
        """
        point_on_axis = conversion.mp_to_pn_vector3d(point_on_axis)
        radius = float(radius)
        pythonnet_method_call_overload(
            self.wrapped,
            "AddCoords",
            [Vector3D, _DOUBLE],
            point_on_axis,
            radius if radius else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_coords(self: "Self", offset: "float", radius: "float") -> None:
        """Method does not return.

        Args:
            offset (float)
            radius (float)
        """
        offset = float(offset)
        radius = float(radius)
        pythonnet_method_call_overload(
            self.wrapped,
            "AddCoords",
            [_DOUBLE, _DOUBLE],
            offset if offset else 0.0,
            radius if radius else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_fillet_point(
        self: "Self",
        point_a_in_sketch_plane: "Vector3D",
        point_b_in_sketch_plane: "Vector3D",
        guide_point: "Vector3D",
        radius: "float",
    ) -> None:
        """Method does not return.

        Args:
            point_a_in_sketch_plane (Vector3D)
            point_b_in_sketch_plane (Vector3D)
            guide_point (Vector3D)
            radius (float)
        """
        point_a_in_sketch_plane = conversion.mp_to_pn_vector3d(point_a_in_sketch_plane)
        point_b_in_sketch_plane = conversion.mp_to_pn_vector3d(point_b_in_sketch_plane)
        guide_point = conversion.mp_to_pn_vector3d(guide_point)
        radius = float(radius)
        pythonnet_method_call(
            self.wrapped,
            "AddFilletPoint",
            point_a_in_sketch_plane,
            point_b_in_sketch_plane,
            guide_point,
            radius if radius else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_mouse_position(self: "Self", point_in_sketch_plane: "Vector3D") -> None:
        """Method does not return.

        Args:
            point_in_sketch_plane (Vector3D)
        """
        point_in_sketch_plane = conversion.mp_to_pn_vector3d(point_in_sketch_plane)
        pythonnet_method_call(self.wrapped, "SetMousePosition", point_in_sketch_plane)

    @property
    def cast_to(self: "Self") -> "_Cast_CirclesOnAxis":
        """Cast to another type.

        Returns:
            _Cast_CirclesOnAxis
        """
        return _Cast_CirclesOnAxis(self)

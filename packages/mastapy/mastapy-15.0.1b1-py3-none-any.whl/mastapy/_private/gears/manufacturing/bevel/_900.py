"""HypoidAdvancedLibrary"""

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
from mastapy._private._math.vector_3d import Vector3D

_HYPOID_ADVANCED_LIBRARY = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "HypoidAdvancedLibrary"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HypoidAdvancedLibrary")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidAdvancedLibrary._Cast_HypoidAdvancedLibrary"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidAdvancedLibrary",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidAdvancedLibrary:
    """Special nested class for casting HypoidAdvancedLibrary to subclasses."""

    __parent__: "HypoidAdvancedLibrary"

    @property
    def hypoid_advanced_library(self: "CastSelf") -> "HypoidAdvancedLibrary":
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
class HypoidAdvancedLibrary(_0.APIBase):
    """HypoidAdvancedLibrary

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_ADVANCED_LIBRARY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_pinion_meshing_boundary_coast(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerPinionMeshingBoundaryCoast")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def inner_pinion_meshing_boundary_drive(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerPinionMeshingBoundaryDrive")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def outer_pinion_meshing_boundary_coast(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterPinionMeshingBoundaryCoast")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def outer_pinion_meshing_boundary_drive(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterPinionMeshingBoundaryDrive")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def wheel_inner_blade_angle_convex(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerBladeAngleConvex")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_outer_blade_angle_concave(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelOuterBladeAngleConcave")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidAdvancedLibrary":
        """Cast to another type.

        Returns:
            _Cast_HypoidAdvancedLibrary
        """
        return _Cast_HypoidAdvancedLibrary(self)

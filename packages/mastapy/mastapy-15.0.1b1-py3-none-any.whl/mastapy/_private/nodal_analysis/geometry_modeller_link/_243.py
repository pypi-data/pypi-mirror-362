"""ProfileFromImport"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D
from mastapy._private._math.vector_3d import Vector3D

_PROFILE_FROM_IMPORT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "ProfileFromImport"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.nodal_analysis.geometry_modeller_link import _240
    from mastapy._private.shafts import _31

    Self = TypeVar("Self", bound="ProfileFromImport")
    CastSelf = TypeVar("CastSelf", bound="ProfileFromImport._Cast_ProfileFromImport")


__docformat__ = "restructuredtext en"
__all__ = ("ProfileFromImport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileFromImport:
    """Special nested class for casting ProfileFromImport to subclasses."""

    __parent__: "ProfileFromImport"

    @property
    def shaft_profile_from_import(self: "CastSelf") -> "_31.ShaftProfileFromImport":
        from mastapy._private.shafts import _31

        return self.__parent__._cast(_31.ShaftProfileFromImport)

    @property
    def profile_from_import(self: "CastSelf") -> "ProfileFromImport":
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
class ProfileFromImport(_0.APIBase):
    """ProfileFromImport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_FROM_IMPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def direction_from_geometry_modeller(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "DirectionFromGeometryModeller")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @direction_from_geometry_modeller.setter
    @exception_bridge
    @enforce_parameter_types
    def direction_from_geometry_modeller(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "DirectionFromGeometryModeller", value)

    @property
    @exception_bridge
    def origin_from_geometry_modeller(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "OriginFromGeometryModeller")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @origin_from_geometry_modeller.setter
    @exception_bridge
    @enforce_parameter_types
    def origin_from_geometry_modeller(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "OriginFromGeometryModeller", value)

    @property
    @exception_bridge
    def orthogonal_direction_from_geometry_modeller(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(
            self.wrapped, "OrthogonalDirectionFromGeometryModeller"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @orthogonal_direction_from_geometry_modeller.setter
    @exception_bridge
    @enforce_parameter_types
    def orthogonal_direction_from_geometry_modeller(
        self: "Self", value: "Vector3D"
    ) -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(
            self.wrapped, "OrthogonalDirectionFromGeometryModeller", value
        )

    @exception_bridge
    @enforce_parameter_types
    def add_edge(
        self: "Self",
        edge_type: "_240.GeometryTypeForComponentImport",
        points: "List[Vector2D]",
    ) -> None:
        """Method does not return.

        Args:
            edge_type (mastapy.nodal_analysis.geometry_modeller_link.GeometryTypeForComponentImport)
            points (List[Vector2D])
        """
        edge_type = conversion.mp_to_pn_enum(
            edge_type,
            "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink.GeometryTypeForComponentImport",
        )
        points = conversion.mp_to_pn_objects_in_dotnet_list(points)
        pythonnet_method_call(self.wrapped, "AddEdge", edge_type, points)

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileFromImport":
        """Cast to another type.

        Returns:
            _Cast_ProfileFromImport
        """
        return _Cast_ProfileFromImport(self)

"""FaceGearMeshMicroGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.analysis import _1345

_FACE_GEAR_MESH_MICRO_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Face", "FaceGearMeshMicroGeometry"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336, _1342
    from mastapy._private.gears.gear_designs.face import _1095, _1097, _1100

    Self = TypeVar("Self", bound="FaceGearMeshMicroGeometry")
    CastSelf = TypeVar(
        "CastSelf", bound="FaceGearMeshMicroGeometry._Cast_FaceGearMeshMicroGeometry"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearMeshMicroGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearMeshMicroGeometry:
    """Special nested class for casting FaceGearMeshMicroGeometry to subclasses."""

    __parent__: "FaceGearMeshMicroGeometry"

    @property
    def gear_mesh_implementation_detail(
        self: "CastSelf",
    ) -> "_1345.GearMeshImplementationDetail":
        return self.__parent__._cast(_1345.GearMeshImplementationDetail)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def face_gear_mesh_micro_geometry(self: "CastSelf") -> "FaceGearMeshMicroGeometry":
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
class FaceGearMeshMicroGeometry(_1345.GearMeshImplementationDetail):
    """FaceGearMeshMicroGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_MESH_MICRO_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def face_gear_set_micro_geometry(self: "Self") -> "_1100.FaceGearSetMicroGeometry":
        """mastapy.gears.gear_designs.face.FaceGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearSetMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def face_mesh(self: "Self") -> "_1095.FaceGearMeshDesign":
        """mastapy.gears.gear_designs.face.FaceGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def face_gear_micro_geometries(self: "Self") -> "List[_1097.FaceGearMicroGeometry]":
        """List[mastapy.gears.gear_designs.face.FaceGearMicroGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearMicroGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearMeshMicroGeometry":
        """Cast to another type.

        Returns:
            _Cast_FaceGearMeshMicroGeometry
        """
        return _Cast_FaceGearMeshMicroGeometry(self)

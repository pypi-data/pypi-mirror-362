"""FaceGearMeshRating"""

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
from mastapy._private.gears.rating import _451

_FACE_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Face", "FaceGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _415
    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.gear_designs.face import _1095
    from mastapy._private.gears.load_case.face import _984
    from mastapy._private.gears.rating import _443
    from mastapy._private.gears.rating.cylindrical.iso6336 import _605
    from mastapy._private.gears.rating.face import _539, _541

    Self = TypeVar("Self", bound="FaceGearMeshRating")
    CastSelf = TypeVar("CastSelf", bound="FaceGearMeshRating._Cast_FaceGearMeshRating")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearMeshRating:
    """Special nested class for casting FaceGearMeshRating to subclasses."""

    __parent__: "FaceGearMeshRating"

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_451.GearMeshRating":
        return self.__parent__._cast(_451.GearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _443

        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def face_gear_mesh_rating(self: "CastSelf") -> "FaceGearMeshRating":
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
class FaceGearMeshRating(_451.GearMeshRating):
    """FaceGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_flank(self: "Self") -> "_415.GearFlanks":
        """mastapy.gears.GearFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.GearFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._415", "GearFlanks"
        )(value)

    @property
    @exception_bridge
    def face_gear_mesh(self: "Self") -> "_1095.FaceGearMeshDesign":
        """mastapy.gears.gear_designs.face.FaceGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_set_rating(self: "Self") -> "_541.FaceGearSetRating":
        """mastapy.gears.rating.face.FaceGearSetRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_load_case(self: "Self") -> "_984.FaceMeshLoadCase":
        """mastapy.gears.load_case.face.FaceMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mesh_single_flank_rating(
        self: "Self",
    ) -> "_605.ISO63362006MeshSingleFlankRating":
        """mastapy.gears.rating.cylindrical.iso6336.ISO63362006MeshSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshSingleFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def face_gear_ratings(self: "Self") -> "List[_539.FaceGearRating]":
        """List[mastapy.gears.rating.face.FaceGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_FaceGearMeshRating
        """
        return _Cast_FaceGearMeshRating(self)

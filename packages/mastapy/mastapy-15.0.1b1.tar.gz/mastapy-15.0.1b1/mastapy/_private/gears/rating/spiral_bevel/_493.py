"""SpiralBevelGearMeshRating"""

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
from mastapy._private.gears.rating.bevel import _645

_SPIRAL_BEVEL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.SpiralBevel", "SpiralBevelGearMeshRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.gear_designs.spiral_bevel import _1074
    from mastapy._private.gears.rating import _443, _451
    from mastapy._private.gears.rating.agma_gleason_conical import _656
    from mastapy._private.gears.rating.conical import _630
    from mastapy._private.gears.rating.spiral_bevel import _494

    Self = TypeVar("Self", bound="SpiralBevelGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelGearMeshRating._Cast_SpiralBevelGearMeshRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearMeshRating:
    """Special nested class for casting SpiralBevelGearMeshRating to subclasses."""

    __parent__: "SpiralBevelGearMeshRating"

    @property
    def bevel_gear_mesh_rating(self: "CastSelf") -> "_645.BevelGearMeshRating":
        return self.__parent__._cast(_645.BevelGearMeshRating)

    @property
    def agma_gleason_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_656.AGMAGleasonConicalGearMeshRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _656

        return self.__parent__._cast(_656.AGMAGleasonConicalGearMeshRating)

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_630.ConicalGearMeshRating":
        from mastapy._private.gears.rating.conical import _630

        return self.__parent__._cast(_630.ConicalGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_451.GearMeshRating":
        from mastapy._private.gears.rating import _451

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
    def spiral_bevel_gear_mesh_rating(self: "CastSelf") -> "SpiralBevelGearMeshRating":
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
class SpiralBevelGearMeshRating(_645.BevelGearMeshRating):
    """SpiralBevelGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def spiral_bevel_gear_mesh(self: "Self") -> "_1074.SpiralBevelGearMeshDesign":
        """mastapy.gears.gear_designs.spiral_bevel.SpiralBevelGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearMesh")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spiral_bevel_gear_ratings(self: "Self") -> "List[_494.SpiralBevelGearRating]":
        """List[mastapy.gears.rating.spiral_bevel.SpiralBevelGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpiralBevelGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearMeshRating
        """
        return _Cast_SpiralBevelGearMeshRating(self)

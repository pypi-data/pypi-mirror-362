"""ZerolBevelGearSetRating"""

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
from mastapy._private.gears.rating.bevel import _647

_ZEROL_BEVEL_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.ZerolBevel", "ZerolBevelGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.gear_designs.zerol_bevel import _1058
    from mastapy._private.gears.rating import _445, _454
    from mastapy._private.gears.rating.agma_gleason_conical import _658
    from mastapy._private.gears.rating.conical import _633
    from mastapy._private.gears.rating.zerol_bevel import _460, _461

    Self = TypeVar("Self", bound="ZerolBevelGearSetRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ZerolBevelGearSetRating._Cast_ZerolBevelGearSetRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ZerolBevelGearSetRating:
    """Special nested class for casting ZerolBevelGearSetRating to subclasses."""

    __parent__: "ZerolBevelGearSetRating"

    @property
    def bevel_gear_set_rating(self: "CastSelf") -> "_647.BevelGearSetRating":
        return self.__parent__._cast(_647.BevelGearSetRating)

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_658.AGMAGleasonConicalGearSetRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _658

        return self.__parent__._cast(_658.AGMAGleasonConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_633.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _633

        return self.__parent__._cast(_633.ConicalGearSetRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_454.GearSetRating":
        from mastapy._private.gears.rating import _454

        return self.__parent__._cast(_454.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_445.AbstractGearSetRating":
        from mastapy._private.gears.rating import _445

        return self.__parent__._cast(_445.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def zerol_bevel_gear_set_rating(self: "CastSelf") -> "ZerolBevelGearSetRating":
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
class ZerolBevelGearSetRating(_647.BevelGearSetRating):
    """ZerolBevelGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ZEROL_BEVEL_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def zerol_bevel_gear_set(self: "Self") -> "_1058.ZerolBevelGearSetDesign":
        """mastapy.gears.gear_designs.zerol_bevel.ZerolBevelGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def zerol_bevel_gear_ratings(self: "Self") -> "List[_461.ZerolBevelGearRating]":
        """List[mastapy.gears.rating.zerol_bevel.ZerolBevelGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def zerol_bevel_mesh_ratings(self: "Self") -> "List[_460.ZerolBevelGearMeshRating]":
        """List[mastapy.gears.rating.zerol_bevel.ZerolBevelGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZerolBevelMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ZerolBevelGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_ZerolBevelGearSetRating
        """
        return _Cast_ZerolBevelGearSetRating(self)

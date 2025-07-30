"""HypoidGearSetRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.agma_gleason_conical import _658

_HYPOID_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Hypoid", "HypoidGearSetRating"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.gear_designs.hypoid import _1091
    from mastapy._private.gears.rating import _445, _454
    from mastapy._private.gears.rating.conical import _633
    from mastapy._private.gears.rating.hypoid import _529, _530

    Self = TypeVar("Self", bound="HypoidGearSetRating")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidGearSetRating._Cast_HypoidGearSetRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearSetRating:
    """Special nested class for casting HypoidGearSetRating to subclasses."""

    __parent__: "HypoidGearSetRating"

    @property
    def agma_gleason_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_658.AGMAGleasonConicalGearSetRating":
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
    def hypoid_gear_set_rating(self: "CastSelf") -> "HypoidGearSetRating":
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
class HypoidGearSetRating(_658.AGMAGleasonConicalGearSetRating):
    """HypoidGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rating(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def size_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def size_factor_contact(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorContact")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def hypoid_gear_set(self: "Self") -> "_1091.HypoidGearSetDesign":
        """mastapy.gears.gear_designs.hypoid.HypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def hypoid_gear_ratings(self: "Self") -> "List[_530.HypoidGearRating]":
        """List[mastapy.gears.rating.hypoid.HypoidGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGearRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_mesh_ratings(self: "Self") -> "List[_529.HypoidGearMeshRating]":
        """List[mastapy.gears.rating.hypoid.HypoidGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidMeshRatings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearSetRating
        """
        return _Cast_HypoidGearSetRating(self)

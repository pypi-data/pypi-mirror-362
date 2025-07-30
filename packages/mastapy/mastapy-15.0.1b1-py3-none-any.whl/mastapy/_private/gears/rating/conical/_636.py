"""ConicalMeshedGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CONICAL_MESHED_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Conical", "ConicalMeshedGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.conical import _1272
    from mastapy._private.gears.rating.straight_bevel_diff import _492

    Self = TypeVar("Self", bound="ConicalMeshedGearRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalMeshedGearRating._Cast_ConicalMeshedGearRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshedGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshedGearRating:
    """Special nested class for casting ConicalMeshedGearRating to subclasses."""

    __parent__: "ConicalMeshedGearRating"

    @property
    def straight_bevel_diff_meshed_gear_rating(
        self: "CastSelf",
    ) -> "_492.StraightBevelDiffMeshedGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _492

        return self.__parent__._cast(_492.StraightBevelDiffMeshedGearRating)

    @property
    def conical_meshed_gear_rating(self: "CastSelf") -> "ConicalMeshedGearRating":
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
class ConicalMeshedGearRating(_0.APIBase):
    """ConicalMeshedGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESHED_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_flank(self: "Self") -> "_1272.ConicalFlanks":
        """mastapy.gears.gear_designs.conical.ConicalFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.ConicalFlanks"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1272", "ConicalFlanks"
        )(value)

    @property
    @exception_bridge
    def axial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_force_type(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AxialForceType")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def gleason_axial_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GleasonAxialFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gleason_separating_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GleasonSeparatingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def normal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_force_type(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialForceType")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def tangential_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshedGearRating":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshedGearRating
        """
        return _Cast_ConicalMeshedGearRating(self)

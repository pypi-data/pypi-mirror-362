"""CylindricalGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating import _452

_CYLINDRICAL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.gear_designs.cylindrical import _1122
    from mastapy._private.gears.rating import _444, _449
    from mastapy._private.gears.rating.cylindrical import _579

    Self = TypeVar("Self", bound="CylindricalGearRating")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearRating._Cast_CylindricalGearRating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearRating:
    """Special nested class for casting CylindricalGearRating to subclasses."""

    __parent__: "CylindricalGearRating"

    @property
    def gear_rating(self: "CastSelf") -> "_452.GearRating":
        return self.__parent__._cast(_452.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_444.AbstractGearRating":
        from mastapy._private.gears.rating import _444

        return self.__parent__._cast(_444.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "CylindricalGearRating":
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
class CylindricalGearRating(_452.GearRating):
    """CylindricalGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def damage_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def damage_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_crack_initiation_safety_factor_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstCrackInitiationSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_fatigue_fracture_safety_factor_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstFatigueFractureSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_permanent_deformation_safety_factor_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstPermanentDeformationSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cylindrical_gear(self: "Self") -> "_1122.CylindricalGearDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def left_flank_rating(self: "Self") -> "_449.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LeftFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def right_flank_rating(self: "Self") -> "_449.GearFlankRating":
        """mastapy.gears.rating.GearFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RightFlankRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def vdi2737_safety_factor(
        self: "Self",
    ) -> "_579.VDI2737SafetyFactorReportingObject":
        """mastapy.gears.rating.cylindrical.VDI2737SafetyFactorReportingObject

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VDI2737SafetyFactor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearRating
        """
        return _Cast_CylindricalGearRating(self)

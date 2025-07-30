"""ISO63362006GearSingleFlankRating"""

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
from mastapy._private.gears.rating.cylindrical.iso6336 import _610

_ISO63362006_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO63362006GearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.cylindrical import _556
    from mastapy._private.gears.rating.cylindrical.iso6336 import _599, _600, _606, _608

    Self = TypeVar("Self", bound="ISO63362006GearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO63362006GearSingleFlankRating._Cast_ISO63362006GearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO63362006GearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO63362006GearSingleFlankRating:
    """Special nested class for casting ISO63362006GearSingleFlankRating to subclasses."""

    __parent__: "ISO63362006GearSingleFlankRating"

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_610.ISO6336AbstractMetalGearSingleFlankRating":
        return self.__parent__._cast(_610.ISO6336AbstractMetalGearSingleFlankRating)

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_608.ISO6336AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _608

        return self.__parent__._cast(_608.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _556

        return self.__parent__._cast(_556.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def iso63362019_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_606.ISO63362019GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _606

        return self.__parent__._cast(_606.ISO63362019GearSingleFlankRating)

    @property
    def iso63362006_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO63362006GearSingleFlankRating":
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
class ISO63362006GearSingleFlankRating(_610.ISO6336AbstractMetalGearSingleFlankRating):
    """ISO63362006GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO63362006_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def nominal_tooth_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalToothRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rim_thickness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RimThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rim_thickness_over_whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RimThicknessOverWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def work_hardening_factor_for_reference_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorkHardeningFactorForReferenceContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def work_hardening_factor_for_static_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorkHardeningFactorForStaticContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_fatigue_fracture_results(
        self: "Self",
    ) -> "_599.CylindricalGearToothFatigueFractureResults":
        """mastapy.gears.rating.cylindrical.iso6336.CylindricalGearToothFatigueFractureResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFatigueFractureResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tooth_fatigue_fracture_results_according_to_french_proposal(
        self: "Self",
    ) -> "_600.CylindricalGearToothFatigueFractureResultsN1457":
        """mastapy.gears.rating.cylindrical.iso6336.CylindricalGearToothFatigueFractureResultsN1457

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothFatigueFractureResultsAccordingToFrenchProposal"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO63362006GearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO63362006GearSingleFlankRating
        """
        return _Cast_ISO63362006GearSingleFlankRating(self)

"""CylindricalMeshedGearFlank"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_CYLINDRICAL_MESHED_GEAR_FLANK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalMeshedGearFlank"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="CylindricalMeshedGearFlank")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalMeshedGearFlank._Cast_CylindricalMeshedGearFlank"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMeshedGearFlank",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalMeshedGearFlank:
    """Special nested class for casting CylindricalMeshedGearFlank to subclasses."""

    __parent__: "CylindricalMeshedGearFlank"

    @property
    def cylindrical_meshed_gear_flank(self: "CastSelf") -> "CylindricalMeshedGearFlank":
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
class CylindricalMeshedGearFlank(_0.APIBase):
    """CylindricalMeshedGearFlank

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_MESHED_GEAR_FLANK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def arc_of_approach(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ArcOfApproach")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_of_recess(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ArcOfRecess")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clearance_from_form_diameter_to_sap_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ClearanceFromFormDiameterToSAPDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum_path_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DedendumPathOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flank_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def form_over_dimension(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormOverDimension")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_addendum_path_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfAddendumPathOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_direction_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDirectionAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def partial_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartialContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_line_length_of_the_active_tooth_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileLineLengthOfTheActiveToothFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_factor_at_tooth_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingFactorAtToothTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specific_sliding_at_eap(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificSlidingAtEAP")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specific_sliding_at_sap(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificSlidingAtSAP")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specific_sliding_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificSlidingChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def end_of_active_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EndOfActiveProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def highest_point_of_fewest_tooth_contacts(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HighestPointOfFewestToothContacts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lowest_point_of_fewest_tooth_contacts(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LowestPointOfFewestToothContacts")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def start_of_active_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StartOfActiveProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def working_pitch(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingPitch")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalMeshedGearFlank":
        """Cast to another type.

        Returns:
            _Cast_CylindricalMeshedGearFlank
        """
        return _Cast_CylindricalMeshedGearFlank(self)

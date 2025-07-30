"""Usage"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1779

_USAGE = python_net_import("SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "Usage")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _435
    from mastapy._private.gears.gear_designs.cylindrical import _1188

    Self = TypeVar("Self", bound="Usage")
    CastSelf = TypeVar("CastSelf", bound="Usage._Cast_Usage")


__docformat__ = "restructuredtext en"
__all__ = ("Usage",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Usage:
    """Special nested class for casting Usage to subclasses."""

    __parent__: "Usage"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def usage(self: "CastSelf") -> "Usage":
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
class Usage(_1779.IndependentReportablePropertiesBase["Usage"]):
    """Usage

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _USAGE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gearing_is_runin(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "GearingIsRunin")

        if temp is None:
            return False

        return temp

    @gearing_is_runin.setter
    @exception_bridge
    @enforce_parameter_types
    def gearing_is_runin(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "GearingIsRunin", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def improved_gearing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ImprovedGearing")

        if temp is None:
            return False

        return temp

    @improved_gearing.setter
    @exception_bridge
    @enforce_parameter_types
    def improved_gearing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ImprovedGearing", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def leads_modified(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LeadsModified")

        if temp is None:
            return False

        return temp

    @leads_modified.setter
    @exception_bridge
    @enforce_parameter_types
    def leads_modified(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LeadsModified", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def safety_requirement(self: "Self") -> "_435.SafetyRequirementsAGMA":
        """mastapy.gears.SafetyRequirementsAGMA"""
        temp = pythonnet_property_get(self.wrapped, "SafetyRequirement")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.SafetyRequirementsAGMA"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._435", "SafetyRequirementsAGMA"
        )(value)

    @safety_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def safety_requirement(self: "Self", value: "_435.SafetyRequirementsAGMA") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.SafetyRequirementsAGMA"
        )
        pythonnet_property_set(self.wrapped, "SafetyRequirement", value)

    @property
    @exception_bridge
    def spur_gear_load_sharing_code(self: "Self") -> "_1188.SpurGearLoadSharingCodes":
        """mastapy.gears.gear_designs.cylindrical.SpurGearLoadSharingCodes"""
        temp = pythonnet_property_get(self.wrapped, "SpurGearLoadSharingCode")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.SpurGearLoadSharingCodes"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1188",
            "SpurGearLoadSharingCodes",
        )(value)

    @spur_gear_load_sharing_code.setter
    @exception_bridge
    @enforce_parameter_types
    def spur_gear_load_sharing_code(
        self: "Self", value: "_1188.SpurGearLoadSharingCodes"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.SpurGearLoadSharingCodes"
        )
        pythonnet_property_set(self.wrapped, "SpurGearLoadSharingCode", value)

    @property
    def cast_to(self: "Self") -> "_Cast_Usage":
        """Cast to another type.

        Returns:
            _Cast_Usage
        """
        return _Cast_Usage(self)

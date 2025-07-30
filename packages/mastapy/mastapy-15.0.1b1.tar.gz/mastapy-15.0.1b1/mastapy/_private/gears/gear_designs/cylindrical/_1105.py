"""CaseHardeningProperties"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CASE_HARDENING_PROPERTIES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CaseHardeningProperties"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1162, _1163

    Self = TypeVar("Self", bound="CaseHardeningProperties")
    CastSelf = TypeVar(
        "CastSelf", bound="CaseHardeningProperties._Cast_CaseHardeningProperties"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CaseHardeningProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CaseHardeningProperties:
    """Special nested class for casting CaseHardeningProperties to subclasses."""

    __parent__: "CaseHardeningProperties"

    @property
    def case_hardening_properties(self: "CastSelf") -> "CaseHardeningProperties":
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
class CaseHardeningProperties(_0.APIBase):
    """CaseHardeningProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CASE_HARDENING_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def depth_at_maximum_hardness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DepthAtMaximumHardness")

        if temp is None:
            return 0.0

        return temp

    @depth_at_maximum_hardness.setter
    @exception_bridge
    @enforce_parameter_types
    def depth_at_maximum_hardness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DepthAtMaximumHardness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def effective_case_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EffectiveCaseDepth")

        if temp is None:
            return 0.0

        return temp

    @effective_case_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def effective_case_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EffectiveCaseDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def hardness_profile_calculation_method(
        self: "Self",
    ) -> "_1162.HardnessProfileCalculationMethod":
        """mastapy.gears.gear_designs.cylindrical.HardnessProfileCalculationMethod"""
        temp = pythonnet_property_get(self.wrapped, "HardnessProfileCalculationMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.HardnessProfileCalculationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1162",
            "HardnessProfileCalculationMethod",
        )(value)

    @hardness_profile_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def hardness_profile_calculation_method(
        self: "Self", value: "_1162.HardnessProfileCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.HardnessProfileCalculationMethod",
        )
        pythonnet_property_set(self.wrapped, "HardnessProfileCalculationMethod", value)

    @property
    @exception_bridge
    def heat_treatment_type(self: "Self") -> "_1163.HeatTreatmentType":
        """mastapy.gears.gear_designs.cylindrical.HeatTreatmentType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatTreatmentType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.HeatTreatmentType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1163", "HeatTreatmentType"
        )(value)

    @property
    @exception_bridge
    def total_case_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TotalCaseDepth")

        if temp is None:
            return 0.0

        return temp

    @total_case_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def total_case_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TotalCaseDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def vickers_hardness_hv_at_effective_case_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "VickersHardnessHVAtEffectiveCaseDepth"
        )

        if temp is None:
            return 0.0

        return temp

    @vickers_hardness_hv_at_effective_case_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def vickers_hardness_hv_at_effective_case_depth(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "VickersHardnessHVAtEffectiveCaseDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CaseHardeningProperties":
        """Cast to another type.

        Returns:
            _Cast_CaseHardeningProperties
        """
        return _Cast_CaseHardeningProperties(self)

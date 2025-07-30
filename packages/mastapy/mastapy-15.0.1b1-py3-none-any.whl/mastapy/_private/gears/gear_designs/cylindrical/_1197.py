"""ToothFlankFractureAnalysisSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.cylindrical import _1181
from mastapy._private.utility import _1779

_TOOTH_FLANK_FRACTURE_ANALYSIS_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ToothFlankFractureAnalysisSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1174
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisSettings._Cast_ToothFlankFractureAnalysisSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisSettings:
    """Special nested class for casting ToothFlankFractureAnalysisSettings to subclasses."""

    __parent__: "ToothFlankFractureAnalysisSettings"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def tooth_flank_fracture_analysis_settings(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisSettings":
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
class ToothFlankFractureAnalysisSettings(
    _1779.IndependentReportablePropertiesBase["ToothFlankFractureAnalysisSettings"]
):
    """ToothFlankFractureAnalysisSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def include_analysis_according_to_the_french_proposal_n1457(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeAnalysisAccordingToTheFrenchProposalN1457"
        )

        if temp is None:
            return False

        return temp

    @include_analysis_according_to_the_french_proposal_n1457.setter
    @exception_bridge
    @enforce_parameter_types
    def include_analysis_according_to_the_french_proposal_n1457(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAnalysisAccordingToTheFrenchProposalN1457",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def measured_residual_stress_profile_property(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasuredResidualStressProfileProperty"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @measured_residual_stress_profile_property.setter
    @exception_bridge
    @enforce_parameter_types
    def measured_residual_stress_profile_property(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MeasuredResidualStressProfileProperty", value.wrapped
        )

    @property
    @exception_bridge
    def residual_stress_calculation_method(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_ResidualStressCalculationMethod"
    ):
        """EnumWithSelectedValue[mastapy.gears.gear_designs.cylindrical.ResidualStressCalculationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ResidualStressCalculationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ResidualStressCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @residual_stress_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_stress_calculation_method(
        self: "Self", value: "_1181.ResidualStressCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ResidualStressCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ResidualStressCalculationMethod", value)

    @property
    @exception_bridge
    def use_enhanced_calculation_with_residual_stress_sensitivity(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseEnhancedCalculationWithResidualStressSensitivity"
        )

        if temp is None:
            return False

        return temp

    @use_enhanced_calculation_with_residual_stress_sensitivity.setter
    @exception_bridge
    @enforce_parameter_types
    def use_enhanced_calculation_with_residual_stress_sensitivity(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseEnhancedCalculationWithResidualStressSensitivity",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def muller_residual_stress_calculator(
        self: "Self",
    ) -> "_1174.MullerResidualStressDefinition":
        """mastapy.gears.gear_designs.cylindrical.MullerResidualStressDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MullerResidualStressCalculator")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisSettings":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisSettings
        """
        return _Cast_ToothFlankFractureAnalysisSettings(self)

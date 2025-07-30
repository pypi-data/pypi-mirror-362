"""StiffnessOptionsForHarmonicAnalysis"""

from __future__ import annotations

from enum import Enum
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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7878
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6062
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_STIFFNESS_OPTIONS_FOR_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "StiffnessOptionsForHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1718
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="StiffnessOptionsForHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StiffnessOptionsForHarmonicAnalysis._Cast_StiffnessOptionsForHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StiffnessOptionsForHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StiffnessOptionsForHarmonicAnalysis:
    """Special nested class for casting StiffnessOptionsForHarmonicAnalysis to subclasses."""

    __parent__: "StiffnessOptionsForHarmonicAnalysis"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7878.AbstractAnalysisOptions":
        return self.__parent__._cast(_7878.AbstractAnalysisOptions)

    @property
    def stiffness_options_for_harmonic_analysis(
        self: "CastSelf",
    ) -> "StiffnessOptionsForHarmonicAnalysis":
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
class StiffnessOptionsForHarmonicAnalysis(
    _7878.AbstractAnalysisOptions[_7674.StaticLoadCase]
):
    """StiffnessOptionsForHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STIFFNESS_OPTIONS_FOR_HARMONIC_ANALYSIS

    class StepCreation(Enum):
        """StepCreation is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _STIFFNESS_OPTIONS_FOR_HARMONIC_ANALYSIS.StepCreation

        GENERATE_STEPS_DISTRIBUTED_IN_TORQUE = 0
        GENERATE_STEPS_DISTRIBUTED_IN_SPEED = 1
        USE_POINTS_OF_TORQUE_SPEED_CURVE = 2
        USERSPECIFIED_TORQUES = 3
        USERSPECIFIED_SPEEDS = 4

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    StepCreation.__setattr__ = __enum_setattr
    StepCreation.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def curve_with_stiffness_steps(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurveWithStiffnessSteps")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def number_of_stiffness_steps(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStiffnessSteps")

        if temp is None:
            return 0

        return temp

    @number_of_stiffness_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_stiffness_steps(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStiffnessSteps",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def step_creation_option(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.harmonic_analyses.StiffnessOptionsForHarmonicAnalysis.StepCreation]"""
        temp = pythonnet_property_get(self.wrapped, "StepCreationOption")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @step_creation_option.setter
    @exception_bridge
    @enforce_parameter_types
    def step_creation_option(
        self: "Self", value: "StiffnessOptionsForHarmonicAnalysis.StepCreation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StiffnessOptionsForHarmonicAnalysis_StepCreation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "StepCreationOption", value)

    @property
    @exception_bridge
    def torque_input_type(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisTorqueInputType"
    ):
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisTorqueInputType]"""
        temp = pythonnet_property_get(self.wrapped, "TorqueInputType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisTorqueInputType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @torque_input_type.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_input_type(
        self: "Self", value: "_6062.HarmonicAnalysisTorqueInputType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicAnalysisTorqueInputType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "TorqueInputType", value)

    @property
    @exception_bridge
    def torque_speed_curve(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "TorqueSpeedCurve")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @torque_speed_curve.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_speed_curve(self: "Self", value: "_1718.Vector2DListAccessor") -> None:
        pythonnet_property_set(self.wrapped, "TorqueSpeedCurve", value.wrapped)

    @exception_bridge
    def create_load_cases_from_steps(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateLoadCasesFromSteps")

    @property
    def cast_to(self: "Self") -> "_Cast_StiffnessOptionsForHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_StiffnessOptionsForHarmonicAnalysis
        """
        return _Cast_StiffnessOptionsForHarmonicAnalysis(self)

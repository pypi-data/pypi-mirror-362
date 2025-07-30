"""WhineWaterfallSettings"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1679, _1711
from mastapy._private.system_model.analyses_and_results.modal_analyses import (
    _4896,
    _4897,
)

_WHINE_WATERFALL_SETTINGS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "WhineWaterfallSettings",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1704, _1717
    from mastapy._private.math_utility.measured_data_scaling import _1753
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6043,
        _6058,
        _6107,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _6150,
        _6153,
        _6158,
        _6159,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import (
        _4879,
        _4932,
        _4934,
        _4980,
        _4981,
    )
    from mastapy._private.system_model.drawing.options import _2482, _2484
    from mastapy._private.utility.property import _2046

    Self = TypeVar("Self", bound="WhineWaterfallSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="WhineWaterfallSettings._Cast_WhineWaterfallSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WhineWaterfallSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WhineWaterfallSettings:
    """Special nested class for casting WhineWaterfallSettings to subclasses."""

    __parent__: "WhineWaterfallSettings"

    @property
    def whine_waterfall_settings(self: "CastSelf") -> "WhineWaterfallSettings":
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
class WhineWaterfallSettings(_0.APIBase):
    """WhineWaterfallSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WHINE_WATERFALL_SETTINGS

    class SpeedBoundaryHandling(Enum):
        """SpeedBoundaryHandling is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _WHINE_WATERFALL_SETTINGS.SpeedBoundaryHandling

        SHOW_DISCONTINUITY = 0
        SHOW_VERTICAL_LINE = 1
        TAKE_MAXIMUM = 2
        TAKE_AVERAGE = 3

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    SpeedBoundaryHandling.__setattr__ = __enum_setattr
    SpeedBoundaryHandling.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def boundary_handling(
        self: "Self",
    ) -> "WhineWaterfallSettings.SpeedBoundaryHandling":
        """mastapy.system_model.analyses_and_results.modal_analyses.WhineWaterfallSettings.SpeedBoundaryHandling"""
        temp = pythonnet_property_get(self.wrapped, "BoundaryHandling")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.WhineWaterfallSettings+SpeedBoundaryHandling",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.modal_analyses.WhineWaterfallSettings.WhineWaterfallSettings",
            "SpeedBoundaryHandling",
        )(value)

    @boundary_handling.setter
    @exception_bridge
    @enforce_parameter_types
    def boundary_handling(
        self: "Self", value: "WhineWaterfallSettings.SpeedBoundaryHandling"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.WhineWaterfallSettings+SpeedBoundaryHandling",
        )
        pythonnet_property_set(self.wrapped, "BoundaryHandling", value)

    @property
    @exception_bridge
    def chart_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DynamicsResponse3DChartType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponse3DChartType]"""
        temp = pythonnet_property_get(self.wrapped, "ChartType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponse3DChartType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @chart_type.setter
    @exception_bridge
    @enforce_parameter_types
    def chart_type(self: "Self", value: "_4896.DynamicsResponse3DChartType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponse3DChartType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ChartType", value)

    @property
    @exception_bridge
    def complex_component(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption":
        """EnumWithSelectedValue[mastapy.math_utility.ComplexPartDisplayOption]"""
        temp = pythonnet_property_get(self.wrapped, "ComplexComponent")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @complex_component.setter
    @exception_bridge
    @enforce_parameter_types
    def complex_component(
        self: "Self", value: "_1679.ComplexPartDisplayOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ComplexPartDisplayOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ComplexComponent", value)

    @property
    @exception_bridge
    def connected_component_type(self: "Self") -> "_6150.ConnectedComponentType":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ConnectedComponentType"""
        temp = pythonnet_property_get(self.wrapped, "ConnectedComponentType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ConnectedComponentType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses.results._6150",
            "ConnectedComponentType",
        )(value)

    @connected_component_type.setter
    @exception_bridge
    @enforce_parameter_types
    def connected_component_type(
        self: "Self", value: "_6150.ConnectedComponentType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results.ConnectedComponentType",
        )
        pythonnet_property_set(self.wrapped, "ConnectedComponentType", value)

    @property
    @exception_bridge
    def coordinate_system(self: "Self") -> "_4879.CoordinateSystemForWhine":
        """mastapy.system_model.analyses_and_results.modal_analyses.CoordinateSystemForWhine"""
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.CoordinateSystemForWhine",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.modal_analyses._4879",
            "CoordinateSystemForWhine",
        )(value)

    @coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def coordinate_system(
        self: "Self", value: "_4879.CoordinateSystemForWhine"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.CoordinateSystemForWhine",
        )
        pythonnet_property_set(self.wrapped, "CoordinateSystem", value)

    @property
    @exception_bridge
    def extend_torque_map_at_edges(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ExtendTorqueMapAtEdges")

        if temp is None:
            return False

        return temp

    @extend_torque_map_at_edges.setter
    @exception_bridge
    @enforce_parameter_types
    def extend_torque_map_at_edges(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExtendTorqueMapAtEdges",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def limit_to_max_under_torque_speed_curve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LimitToMaxUnderTorqueSpeedCurve")

        if temp is None:
            return False

        return temp

    @limit_to_max_under_torque_speed_curve.setter
    @exception_bridge
    @enforce_parameter_types
    def limit_to_max_under_torque_speed_curve(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LimitToMaxUnderTorqueSpeedCurve",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def max_harmonic(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaxHarmonic")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @max_harmonic.setter
    @exception_bridge
    @enforce_parameter_types
    def max_harmonic(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaxHarmonic", value)

    @property
    @exception_bridge
    def maximum_order(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumOrder")

        if temp is None:
            return 0.0

        return temp

    @maximum_order.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_order(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumOrder", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minimum_order(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumOrder")

        if temp is None:
            return 0.0

        return temp

    @minimum_order.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_order(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumOrder", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_additional_points_either_side_of_order_line(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfAdditionalPointsEitherSideOfOrderLine"
        )

        if temp is None:
            return 0

        return temp

    @number_of_additional_points_either_side_of_order_line.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_additional_points_either_side_of_order_line(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfAdditionalPointsEitherSideOfOrderLine",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_points_per_step(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPointsPerStep")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_points_per_step.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_per_step(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfPointsPerStep", value)

    @property
    @exception_bridge
    def overlay_torque_speed_curve(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OverlayTorqueSpeedCurve")

        if temp is None:
            return False

        return temp

    @overlay_torque_speed_curve.setter
    @exception_bridge
    @enforce_parameter_types
    def overlay_torque_speed_curve(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverlayTorqueSpeedCurve",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def reduce_number_of_result_points(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ReduceNumberOfResultPoints")

        if temp is None:
            return False

        return temp

    @reduce_number_of_result_points.setter
    @exception_bridge
    @enforce_parameter_types
    def reduce_number_of_result_points(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReduceNumberOfResultPoints",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def replace_speed_axis_with_frequency(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ReplaceSpeedAxisWithFrequency")

        if temp is None:
            return False

        return temp

    @replace_speed_axis_with_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def replace_speed_axis_with_frequency(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReplaceSpeedAxisWithFrequency",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def response_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponseType]"""
        temp = pythonnet_property_get(self.wrapped, "ResponseType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @response_type.setter
    @exception_bridge
    @enforce_parameter_types
    def response_type(self: "Self", value: "_4897.DynamicsResponseType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ResponseType", value)

    @property
    @exception_bridge
    def show_amplitudes_of_gear_excitations(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAmplitudesOfGearExcitations")

        if temp is None:
            return False

        return temp

    @show_amplitudes_of_gear_excitations.setter
    @exception_bridge
    @enforce_parameter_types
    def show_amplitudes_of_gear_excitations(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowAmplitudesOfGearExcitations",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_boundaries_of_stiffness_steps(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowBoundariesOfStiffnessSteps")

        if temp is None:
            return False

        return temp

    @show_boundaries_of_stiffness_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def show_boundaries_of_stiffness_steps(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowBoundariesOfStiffnessSteps",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_coupled_modes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowCoupledModes")

        if temp is None:
            return False

        return temp

    @show_coupled_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def show_coupled_modes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowCoupledModes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_torques_at_stiffness_steps(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowTorquesAtStiffnessSteps")

        if temp is None:
            return False

        return temp

    @show_torques_at_stiffness_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def show_torques_at_stiffness_steps(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowTorquesAtStiffnessSteps",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_total_response_for_multiple_excitations(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ShowTotalResponseForMultipleExcitations"
        )

        if temp is None:
            return False

        return temp

    @show_total_response_for_multiple_excitations.setter
    @exception_bridge
    @enforce_parameter_types
    def show_total_response_for_multiple_excitations(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowTotalResponseForMultipleExcitations",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_total_response_for_multiple_surfaces(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ShowTotalResponseForMultipleSurfaces"
        )

        if temp is None:
            return False

        return temp

    @show_total_response_for_multiple_surfaces.setter
    @exception_bridge
    @enforce_parameter_types
    def show_total_response_for_multiple_surfaces(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowTotalResponseForMultipleSurfaces",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def speed_range_for_combining_excitations(
        self: "Self",
    ) -> "_4932.MultipleExcitationsSpeedRangeOption":
        """mastapy.system_model.analyses_and_results.modal_analyses.MultipleExcitationsSpeedRangeOption"""
        temp = pythonnet_property_get(self.wrapped, "SpeedRangeForCombiningExcitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.MultipleExcitationsSpeedRangeOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.modal_analyses._4932",
            "MultipleExcitationsSpeedRangeOption",
        )(value)

    @speed_range_for_combining_excitations.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_range_for_combining_excitations(
        self: "Self", value: "_4932.MultipleExcitationsSpeedRangeOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.MultipleExcitationsSpeedRangeOption",
        )
        pythonnet_property_set(self.wrapped, "SpeedRangeForCombiningExcitations", value)

    @property
    @exception_bridge
    def translation_or_rotation(self: "Self") -> "_1717.TranslationRotation":
        """mastapy.math_utility.TranslationRotation"""
        temp = pythonnet_property_get(self.wrapped, "TranslationOrRotation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.TranslationRotation"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1717", "TranslationRotation"
        )(value)

    @translation_or_rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def translation_or_rotation(
        self: "Self", value: "_1717.TranslationRotation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.TranslationRotation"
        )
        pythonnet_property_set(self.wrapped, "TranslationOrRotation", value)

    @property
    @exception_bridge
    def vector_magnitude_method(self: "Self") -> "_1704.ComplexMagnitudeMethod":
        """mastapy.math_utility.ComplexMagnitudeMethod"""
        temp = pythonnet_property_get(self.wrapped, "VectorMagnitudeMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.ComplexMagnitudeMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1704", "ComplexMagnitudeMethod"
        )(value)

    @vector_magnitude_method.setter
    @exception_bridge
    @enforce_parameter_types
    def vector_magnitude_method(
        self: "Self", value: "_1704.ComplexMagnitudeMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.ComplexMagnitudeMethod"
        )
        pythonnet_property_set(self.wrapped, "VectorMagnitudeMethod", value)

    @property
    @exception_bridge
    def whine_waterfall_export_option(
        self: "Self",
    ) -> "_4981.WhineWaterfallExportOption":
        """mastapy.system_model.analyses_and_results.modal_analyses.WhineWaterfallExportOption"""
        temp = pythonnet_property_get(self.wrapped, "WhineWaterfallExportOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.WhineWaterfallExportOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.modal_analyses._4981",
            "WhineWaterfallExportOption",
        )(value)

    @whine_waterfall_export_option.setter
    @exception_bridge
    @enforce_parameter_types
    def whine_waterfall_export_option(
        self: "Self", value: "_4981.WhineWaterfallExportOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.WhineWaterfallExportOption",
        )
        pythonnet_property_set(self.wrapped, "WhineWaterfallExportOption", value)

    @property
    @exception_bridge
    def data_scaling(self: "Self") -> "_1753.DataScalingOptions":
        """mastapy.math_utility.measured_data_scaling.DataScalingOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DataScaling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def frequency_options(
        self: "Self",
    ) -> "_6043.FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def harmonic_analysis_options(self: "Self") -> "_6058.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def modal_contribution_view_options(
        self: "Self",
    ) -> "_2484.ModalContributionViewOptions":
        """mastapy.system_model.drawing.options.ModalContributionViewOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalContributionViewOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mode_view_options(
        self: "Self",
    ) -> "_2482.AdvancedTimeSteppingAnalysisForModulationModeViewOptions":
        """mastapy.system_model.drawing.options.AdvancedTimeSteppingAnalysisForModulationModeViewOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeViewOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def order_cuts_chart_settings(self: "Self") -> "_4934.OrderCutsChartSettings":
        """mastapy.system_model.analyses_and_results.modal_analyses.OrderCutsChartSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OrderCutsChartSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reference_speed_options(
        self: "Self",
    ) -> "_6107.SpeedOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.SpeedOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def result_location_selection_groups(
        self: "Self",
    ) -> "_6158.ResultLocationSelectionGroups":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ResultLocationSelectionGroups

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultLocationSelectionGroups")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_excitations(self: "Self") -> "_6153.ExcitationSourceSelectionGroup":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ExcitationSourceSelectionGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedExcitations")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def waterfall_chart_settings(self: "Self") -> "_4980.WaterfallChartSettings":
        """mastapy.system_model.analyses_and_results.modal_analyses.WaterfallChartSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WaterfallChartSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def active_result_locations(self: "Self") -> "List[_6159.ResultNodeSelection]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.results.ResultNodeSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveResultLocations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def degrees_of_freedom(
        self: "Self",
    ) -> "List[_2046.EnumWithBoolean[_1711.ResultOptionsFor3DVector]]":
        """List[mastapy.utility.property.EnumWithBoolean[mastapy.math_utility.ResultOptionsFor3DVector]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DegreesOfFreedom")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    def calculate_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CalculateResults")

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_WhineWaterfallSettings":
        """Cast to another type.

        Returns:
            _Cast_WhineWaterfallSettings
        """
        return _Cast_WhineWaterfallSettings(self)

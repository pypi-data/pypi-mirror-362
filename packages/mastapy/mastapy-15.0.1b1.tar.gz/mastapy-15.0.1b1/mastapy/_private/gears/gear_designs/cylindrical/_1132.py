"""CylindricalGearMicroGeometrySettingsItem"""

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
from mastapy._private.gears import _408
from mastapy._private.gears.micro_geometry import _664, _665, _666, _667
from mastapy._private.utility.databases import _2028

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_SETTINGS_ITEM = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CylindricalGearMicroGeometrySettingsItem",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import (
        _1155,
        _1171,
        _1172,
        _1182,
    )
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1237
    from mastapy._private.gears.micro_geometry import _662, _668, _669, _671, _672

    Self = TypeVar("Self", bound="CylindricalGearMicroGeometrySettingsItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroGeometrySettingsItem._Cast_CylindricalGearMicroGeometrySettingsItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroGeometrySettingsItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroGeometrySettingsItem:
    """Special nested class for casting CylindricalGearMicroGeometrySettingsItem to subclasses."""

    __parent__: "CylindricalGearMicroGeometrySettingsItem"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cylindrical_gear_micro_geometry_settings_item(
        self: "CastSelf",
    ) -> "CylindricalGearMicroGeometrySettingsItem":
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
class CylindricalGearMicroGeometrySettingsItem(_2028.NamedDatabaseItem):
    """CylindricalGearMicroGeometrySettingsItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_SETTINGS_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def add_flank_side_labels_to_micro_geometry_lead_tolerance_charts(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "AddFlankSideLabelsToMicroGeometryLeadToleranceCharts"
        )

        if temp is None:
            return False

        return temp

    @add_flank_side_labels_to_micro_geometry_lead_tolerance_charts.setter
    @exception_bridge
    @enforce_parameter_types
    def add_flank_side_labels_to_micro_geometry_lead_tolerance_charts(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AddFlankSideLabelsToMicroGeometryLeadToleranceCharts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def adjust_micro_geometry_for_analysis_by_default_when_including_pitch_errors(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "AdjustMicroGeometryForAnalysisByDefaultWhenIncludingPitchErrors",
        )

        if temp is None:
            return False

        return temp

    @adjust_micro_geometry_for_analysis_by_default_when_including_pitch_errors.setter
    @exception_bridge
    @enforce_parameter_types
    def adjust_micro_geometry_for_analysis_by_default_when_including_pitch_errors(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AdjustMicroGeometryForAnalysisByDefaultWhenIncludingPitchErrors",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def centre_tolerance_charts_at_maximum_fullness(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CentreToleranceChartsAtMaximumFullness"
        )

        if temp is None:
            return False

        return temp

    @centre_tolerance_charts_at_maximum_fullness.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_tolerance_charts_at_maximum_fullness(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentreToleranceChartsAtMaximumFullness",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def crop_face_width_axis_of_micro_geometry_lead_tolerance_charts(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CropFaceWidthAxisOfMicroGeometryLeadToleranceCharts"
        )

        if temp is None:
            return False

        return temp

    @crop_face_width_axis_of_micro_geometry_lead_tolerance_charts.setter
    @exception_bridge
    @enforce_parameter_types
    def crop_face_width_axis_of_micro_geometry_lead_tolerance_charts(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CropFaceWidthAxisOfMicroGeometryLeadToleranceCharts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def crop_profile_measurement_axis_of_micro_geometry_profile_tolerance_charts(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "CropProfileMeasurementAxisOfMicroGeometryProfileToleranceCharts",
        )

        if temp is None:
            return False

        return temp

    @crop_profile_measurement_axis_of_micro_geometry_profile_tolerance_charts.setter
    @exception_bridge
    @enforce_parameter_types
    def crop_profile_measurement_axis_of_micro_geometry_profile_tolerance_charts(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CropProfileMeasurementAxisOfMicroGeometryProfileToleranceCharts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def default_coefficient_of_friction_method_for_ltca(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod":
        """EnumWithSelectedValue[mastapy.gears.CoefficientOfFrictionCalculationMethod]"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultCoefficientOfFrictionMethodForLTCA"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_coefficient_of_friction_method_for_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def default_coefficient_of_friction_method_for_ltca(
        self: "Self", value: "_408.CoefficientOfFrictionCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CoefficientOfFrictionCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "DefaultCoefficientOfFrictionMethodForLTCA", value
        )

    @property
    @exception_bridge
    def default_flank_side_with_zero_face_width(self: "Self") -> "_662.FlankSide":
        """mastapy.gears.micro_geometry.FlankSide"""
        temp = pythonnet_property_get(self.wrapped, "DefaultFlankSideWithZeroFaceWidth")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.MicroGeometry.FlankSide"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._662", "FlankSide"
        )(value)

    @default_flank_side_with_zero_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def default_flank_side_with_zero_face_width(
        self: "Self", value: "_662.FlankSide"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.MicroGeometry.FlankSide"
        )
        pythonnet_property_set(self.wrapped, "DefaultFlankSideWithZeroFaceWidth", value)

    @property
    @exception_bridge
    def default_location_of_evaluation_lower_limit(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfEvaluationLowerLimit]"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultLocationOfEvaluationLowerLimit"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_location_of_evaluation_lower_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def default_location_of_evaluation_lower_limit(
        self: "Self", value: "_664.LocationOfEvaluationLowerLimit"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationLowerLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "DefaultLocationOfEvaluationLowerLimit", value
        )

    @property
    @exception_bridge
    def default_location_of_evaluation_upper_limit(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfEvaluationUpperLimit]"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultLocationOfEvaluationUpperLimit"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_location_of_evaluation_upper_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def default_location_of_evaluation_upper_limit(
        self: "Self", value: "_665.LocationOfEvaluationUpperLimit"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfEvaluationUpperLimit.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "DefaultLocationOfEvaluationUpperLimit", value
        )

    @property
    @exception_bridge
    def default_location_of_root_relief_evaluation(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfRootReliefEvaluation]"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultLocationOfRootReliefEvaluation"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_location_of_root_relief_evaluation.setter
    @exception_bridge
    @enforce_parameter_types
    def default_location_of_root_relief_evaluation(
        self: "Self", value: "_666.LocationOfRootReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "DefaultLocationOfRootReliefEvaluation", value
        )

    @property
    @exception_bridge
    def default_location_of_root_relief_start(
        self: "Self",
    ) -> (
        "enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation"
    ):
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfRootReliefEvaluation]"""
        temp = pythonnet_property_get(self.wrapped, "DefaultLocationOfRootReliefStart")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_location_of_root_relief_start.setter
    @exception_bridge
    @enforce_parameter_types
    def default_location_of_root_relief_start(
        self: "Self", value: "_666.LocationOfRootReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfRootReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DefaultLocationOfRootReliefStart", value)

    @property
    @exception_bridge
    def default_location_of_tip_relief_evaluation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation":
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfTipReliefEvaluation]"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultLocationOfTipReliefEvaluation"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_location_of_tip_relief_evaluation.setter
    @exception_bridge
    @enforce_parameter_types
    def default_location_of_tip_relief_evaluation(
        self: "Self", value: "_667.LocationOfTipReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "DefaultLocationOfTipReliefEvaluation", value
        )

    @property
    @exception_bridge
    def default_location_of_tip_relief_start(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation":
        """EnumWithSelectedValue[mastapy.gears.micro_geometry.LocationOfTipReliefEvaluation]"""
        temp = pythonnet_property_get(self.wrapped, "DefaultLocationOfTipReliefStart")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @default_location_of_tip_relief_start.setter
    @exception_bridge
    @enforce_parameter_types
    def default_location_of_tip_relief_start(
        self: "Self", value: "_667.LocationOfTipReliefEvaluation"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_LocationOfTipReliefEvaluation.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DefaultLocationOfTipReliefStart", value)

    @property
    @exception_bridge
    def default_micro_geometry_lead_tolerance_chart_view(
        self: "Self",
    ) -> "_1237.MicroGeometryLeadToleranceChartView":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.MicroGeometryLeadToleranceChartView"""
        temp = pythonnet_property_get(
            self.wrapped, "DefaultMicroGeometryLeadToleranceChartView"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.MicroGeometryLeadToleranceChartView",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1237",
            "MicroGeometryLeadToleranceChartView",
        )(value)

    @default_micro_geometry_lead_tolerance_chart_view.setter
    @exception_bridge
    @enforce_parameter_types
    def default_micro_geometry_lead_tolerance_chart_view(
        self: "Self", value: "_1237.MicroGeometryLeadToleranceChartView"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.MicroGeometryLeadToleranceChartView",
        )
        pythonnet_property_set(
            self.wrapped, "DefaultMicroGeometryLeadToleranceChartView", value
        )

    @property
    @exception_bridge
    def default_scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts(
        self: "Self",
    ) -> "_1155.DoubleAxisScaleAndRange":
        """mastapy.gears.gear_designs.cylindrical.DoubleAxisScaleAndRange"""
        temp = pythonnet_property_get(
            self.wrapped,
            "DefaultScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DoubleAxisScaleAndRange"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1155",
            "DoubleAxisScaleAndRange",
        )(value)

    @default_scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts.setter
    @exception_bridge
    @enforce_parameter_types
    def default_scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts(
        self: "Self", value: "_1155.DoubleAxisScaleAndRange"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DoubleAxisScaleAndRange"
        )
        pythonnet_property_set(
            self.wrapped,
            "DefaultScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts",
            value,
        )

    @property
    @exception_bridge
    def draw_micro_geometry_charts_with_face_width_axis_oriented_to_view_through_air(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "DrawMicroGeometryChartsWithFaceWidthAxisOrientedToViewThroughAir",
        )

        if temp is None:
            return False

        return temp

    @draw_micro_geometry_charts_with_face_width_axis_oriented_to_view_through_air.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_micro_geometry_charts_with_face_width_axis_oriented_to_view_through_air(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawMicroGeometryChartsWithFaceWidthAxisOrientedToViewThroughAir",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def draw_micro_geometry_profile_chart_with_relief_on_horizontal_axis(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "DrawMicroGeometryProfileChartWithReliefOnHorizontalAxis"
        )

        if temp is None:
            return False

        return temp

    @draw_micro_geometry_profile_chart_with_relief_on_horizontal_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_micro_geometry_profile_chart_with_relief_on_horizontal_axis(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawMicroGeometryProfileChartWithReliefOnHorizontalAxis",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def ltca_root_stress_surface_chart_option(
        self: "Self",
    ) -> "_1182.RootStressSurfaceChartOption":
        """mastapy.gears.gear_designs.cylindrical.RootStressSurfaceChartOption"""
        temp = pythonnet_property_get(self.wrapped, "LTCARootStressSurfaceChartOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.RootStressSurfaceChartOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1182",
            "RootStressSurfaceChartOption",
        )(value)

    @ltca_root_stress_surface_chart_option.setter
    @exception_bridge
    @enforce_parameter_types
    def ltca_root_stress_surface_chart_option(
        self: "Self", value: "_1182.RootStressSurfaceChartOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.RootStressSurfaceChartOption",
        )
        pythonnet_property_set(self.wrapped, "LTCARootStressSurfaceChartOption", value)

    @property
    @exception_bridge
    def main_profile_modification_ends_at_the_start_of_root_relief_by_default(
        self: "Self",
    ) -> "_668.MainProfileReliefEndsAtTheStartOfRootReliefOption":
        """mastapy.gears.micro_geometry.MainProfileReliefEndsAtTheStartOfRootReliefOption"""
        temp = pythonnet_property_get(
            self.wrapped, "MainProfileModificationEndsAtTheStartOfRootReliefByDefault"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfRootReliefOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._668",
            "MainProfileReliefEndsAtTheStartOfRootReliefOption",
        )(value)

    @main_profile_modification_ends_at_the_start_of_root_relief_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def main_profile_modification_ends_at_the_start_of_root_relief_by_default(
        self: "Self", value: "_668.MainProfileReliefEndsAtTheStartOfRootReliefOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfRootReliefOption",
        )
        pythonnet_property_set(
            self.wrapped,
            "MainProfileModificationEndsAtTheStartOfRootReliefByDefault",
            value,
        )

    @property
    @exception_bridge
    def main_profile_modification_ends_at_the_start_of_tip_relief_by_default(
        self: "Self",
    ) -> "_669.MainProfileReliefEndsAtTheStartOfTipReliefOption":
        """mastapy.gears.micro_geometry.MainProfileReliefEndsAtTheStartOfTipReliefOption"""
        temp = pythonnet_property_get(
            self.wrapped, "MainProfileModificationEndsAtTheStartOfTipReliefByDefault"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfTipReliefOption",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._669",
            "MainProfileReliefEndsAtTheStartOfTipReliefOption",
        )(value)

    @main_profile_modification_ends_at_the_start_of_tip_relief_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def main_profile_modification_ends_at_the_start_of_tip_relief_by_default(
        self: "Self", value: "_669.MainProfileReliefEndsAtTheStartOfTipReliefOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.MainProfileReliefEndsAtTheStartOfTipReliefOption",
        )
        pythonnet_property_set(
            self.wrapped,
            "MainProfileModificationEndsAtTheStartOfTipReliefByDefault",
            value,
        )

    @property
    @exception_bridge
    def measure_root_reliefs_from_extrapolated_linear_relief_by_default(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasureRootReliefsFromExtrapolatedLinearReliefByDefault"
        )

        if temp is None:
            return False

        return temp

    @measure_root_reliefs_from_extrapolated_linear_relief_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def measure_root_reliefs_from_extrapolated_linear_relief_by_default(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeasureRootReliefsFromExtrapolatedLinearReliefByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def measure_tip_reliefs_from_extrapolated_linear_relief_by_default(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "MeasureTipReliefsFromExtrapolatedLinearReliefByDefault"
        )

        if temp is None:
            return False

        return temp

    @measure_tip_reliefs_from_extrapolated_linear_relief_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def measure_tip_reliefs_from_extrapolated_linear_relief_by_default(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeasureTipReliefsFromExtrapolatedLinearReliefByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def micro_geometry_lead_relief_definition(
        self: "Self",
    ) -> "_1171.MicroGeometryConvention":
        """mastapy.gears.gear_designs.cylindrical.MicroGeometryConvention"""
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryLeadReliefDefinition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometryConvention"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1171",
            "MicroGeometryConvention",
        )(value)

    @micro_geometry_lead_relief_definition.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_lead_relief_definition(
        self: "Self", value: "_1171.MicroGeometryConvention"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometryConvention"
        )
        pythonnet_property_set(self.wrapped, "MicroGeometryLeadReliefDefinition", value)

    @property
    @exception_bridge
    def micro_geometry_profile_relief_definition(
        self: "Self",
    ) -> "_1172.MicroGeometryProfileConvention":
        """mastapy.gears.gear_designs.cylindrical.MicroGeometryProfileConvention"""
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryProfileReliefDefinition"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometryProfileConvention",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1172",
            "MicroGeometryProfileConvention",
        )(value)

    @micro_geometry_profile_relief_definition.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_profile_relief_definition(
        self: "Self", value: "_1172.MicroGeometryProfileConvention"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometryProfileConvention",
        )
        pythonnet_property_set(
            self.wrapped, "MicroGeometryProfileReliefDefinition", value
        )

    @property
    @exception_bridge
    def number_of_points_for_2d_micro_geometry_plots(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsFor2DMicroGeometryPlots"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_for_2d_micro_geometry_plots.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_for_2d_micro_geometry_plots(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsFor2DMicroGeometryPlots",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_steps_for_ltca_contact_surface(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStepsForLTCAContactSurface"
        )

        if temp is None:
            return 0

        return temp

    @number_of_steps_for_ltca_contact_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_steps_for_ltca_contact_surface(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStepsForLTCAContactSurface",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def parabolic_root_relief_starts_tangent_to_main_profile_relief_by_default(
        self: "Self",
    ) -> "_671.ParabolicRootReliefStartsTangentToMainProfileRelief":
        """mastapy.gears.micro_geometry.ParabolicRootReliefStartsTangentToMainProfileRelief"""
        temp = pythonnet_property_get(
            self.wrapped, "ParabolicRootReliefStartsTangentToMainProfileReliefByDefault"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicRootReliefStartsTangentToMainProfileRelief",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._671",
            "ParabolicRootReliefStartsTangentToMainProfileRelief",
        )(value)

    @parabolic_root_relief_starts_tangent_to_main_profile_relief_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def parabolic_root_relief_starts_tangent_to_main_profile_relief_by_default(
        self: "Self", value: "_671.ParabolicRootReliefStartsTangentToMainProfileRelief"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicRootReliefStartsTangentToMainProfileRelief",
        )
        pythonnet_property_set(
            self.wrapped,
            "ParabolicRootReliefStartsTangentToMainProfileReliefByDefault",
            value,
        )

    @property
    @exception_bridge
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief_by_default(
        self: "Self",
    ) -> "_672.ParabolicTipReliefStartsTangentToMainProfileRelief":
        """mastapy.gears.micro_geometry.ParabolicTipReliefStartsTangentToMainProfileRelief"""
        temp = pythonnet_property_get(
            self.wrapped, "ParabolicTipReliefStartsTangentToMainProfileReliefByDefault"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicTipReliefStartsTangentToMainProfileRelief",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._672",
            "ParabolicTipReliefStartsTangentToMainProfileRelief",
        )(value)

    @parabolic_tip_relief_starts_tangent_to_main_profile_relief_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def parabolic_tip_relief_starts_tangent_to_main_profile_relief_by_default(
        self: "Self", value: "_672.ParabolicTipReliefStartsTangentToMainProfileRelief"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.MicroGeometry.ParabolicTipReliefStartsTangentToMainProfileRelief",
        )
        pythonnet_property_set(
            self.wrapped,
            "ParabolicTipReliefStartsTangentToMainProfileReliefByDefault",
            value,
        )

    @property
    @exception_bridge
    def shift_micro_geometry_lead_and_profile_modification_to_have_zero_maximum(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "ShiftMicroGeometryLeadAndProfileModificationToHaveZeroMaximum",
        )

        if temp is None:
            return False

        return temp

    @shift_micro_geometry_lead_and_profile_modification_to_have_zero_maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def shift_micro_geometry_lead_and_profile_modification_to_have_zero_maximum(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShiftMicroGeometryLeadAndProfileModificationToHaveZeroMaximum",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_same_micro_geometry_on_both_flanks_by_default(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseSameMicroGeometryOnBothFlanksByDefault"
        )

        if temp is None:
            return False

        return temp

    @use_same_micro_geometry_on_both_flanks_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def use_same_micro_geometry_on_both_flanks_by_default(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSameMicroGeometryOnBothFlanksByDefault",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroGeometrySettingsItem":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroGeometrySettingsItem
        """
        return _Cast_CylindricalGearMicroGeometrySettingsItem(self)

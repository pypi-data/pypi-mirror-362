"""MBDAnalysisOptions"""

from __future__ import annotations

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
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
    _5670,
    _5722,
    _5770,
)
from mastapy._private.system_model.part_model import _2703

_MBD_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "MBDAnalysisOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis import _94
    from mastapy._private.system_model.analyses_and_results.mbd_analyses import (
        _5666,
        _5729,
        _5730,
        _5746,
        _5779,
    )
    from mastapy._private.system_model.analyses_and_results.mbd_analyses.external_interfaces import (
        _5816,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4904

    Self = TypeVar("Self", bound="MBDAnalysisOptions")
    CastSelf = TypeVar("CastSelf", bound="MBDAnalysisOptions._Cast_MBDAnalysisOptions")


__docformat__ = "restructuredtext en"
__all__ = ("MBDAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MBDAnalysisOptions:
    """Special nested class for casting MBDAnalysisOptions to subclasses."""

    __parent__: "MBDAnalysisOptions"

    @property
    def mbd_analysis_options(self: "CastSelf") -> "MBDAnalysisOptions":
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
class MBDAnalysisOptions(_0.APIBase):
    """MBDAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MBD_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_type(self: "Self") -> "_5666.AnalysisTypes":
        """mastapy.system_model.analyses_and_results.mbd_analyses.AnalysisTypes"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.AnalysisTypes",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5666",
            "AnalysisTypes",
        )(value)

    @analysis_type.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_type(self: "Self", value: "_5666.AnalysisTypes") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.AnalysisTypes",
        )
        pythonnet_property_set(self.wrapped, "AnalysisType", value)

    @property
    @exception_bridge
    def bearing_rayleigh_damping_beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BearingRayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @bearing_rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BearingRayleighDampingBeta", value)

    @property
    @exception_bridge
    def bearing_stiffness_model(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.mbd_analyses.BearingStiffnessModel]"""
        temp = pythonnet_property_get(self.wrapped, "BearingStiffnessModel")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @bearing_stiffness_model.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_stiffness_model(
        self: "Self", value: "_5670.BearingStiffnessModel"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BearingStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BearingStiffnessModel", value)

    @property
    @exception_bridge
    def belt_rayleigh_damping_beta(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "BeltRayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @belt_rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def belt_rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BeltRayleighDampingBeta", value)

    @property
    @exception_bridge
    def create_inertia_adjusted_static_load_cases(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CreateInertiaAdjustedStaticLoadCases"
        )

        if temp is None:
            return False

        return temp

    @create_inertia_adjusted_static_load_cases.setter
    @exception_bridge
    @enforce_parameter_types
    def create_inertia_adjusted_static_load_cases(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CreateInertiaAdjustedStaticLoadCases",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def filter_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FilterCutOff")

        if temp is None:
            return 0.0

        return temp

    @filter_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def filter_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FilterCutOff", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gear_mesh_rayleigh_damping_beta(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "GearMeshRayleighDampingBeta")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @gear_mesh_rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_mesh_rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "GearMeshRayleighDampingBeta", value)

    @property
    @exception_bridge
    def gear_mesh_stiffness_model(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.mbd_analyses.GearMeshStiffnessModel]"""
        temp = pythonnet_property_get(self.wrapped, "GearMeshStiffnessModel")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @gear_mesh_stiffness_model.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_mesh_stiffness_model(
        self: "Self", value: "_5722.GearMeshStiffnessModel"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_GearMeshStiffnessModel.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "GearMeshStiffnessModel", value)

    @property
    @exception_bridge
    def include_gear_backlash(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeGearBacklash")

        if temp is None:
            return False

        return temp

    @include_gear_backlash.setter
    @exception_bridge
    @enforce_parameter_types
    def include_gear_backlash(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeGearBacklash",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_microgeometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMicrogeometry")

        if temp is None:
            return False

        return temp

    @include_microgeometry.setter
    @exception_bridge
    @enforce_parameter_types
    def include_microgeometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeMicrogeometry",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_shaft_and_housing_flexibilities(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.mbd_analyses.ShaftAndHousingFlexibilityOption]"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeShaftAndHousingFlexibilities"
        )

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @include_shaft_and_housing_flexibilities.setter
    @exception_bridge
    @enforce_parameter_types
    def include_shaft_and_housing_flexibilities(
        self: "Self", value: "_5770.ShaftAndHousingFlexibilityOption"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ShaftAndHousingFlexibilityOption.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(
            self.wrapped, "IncludeShaftAndHousingFlexibilities", value
        )

    @property
    @exception_bridge
    def interference_fit_rayleigh_damping_beta(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "InterferenceFitRayleighDampingBeta"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @interference_fit_rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def interference_fit_rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "InterferenceFitRayleighDampingBeta", value
        )

    @property
    @exception_bridge
    def load_case_for_component_speed_ratios(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "LoadCaseForComponentSpeedRatios")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @load_case_for_component_speed_ratios.setter
    @exception_bridge
    @enforce_parameter_types
    def load_case_for_component_speed_ratios(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "LoadCaseForComponentSpeedRatios", value)

    @property
    @exception_bridge
    def load_case_for_linearised_bearing_stiffness(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(
            self.wrapped, "LoadCaseForLinearisedBearingStiffness"
        )

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @load_case_for_linearised_bearing_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def load_case_for_linearised_bearing_stiffness(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "LoadCaseForLinearisedBearingStiffness", value
        )

    @property
    @exception_bridge
    def maximum_angular_jerk(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumAngularJerk")

        if temp is None:
            return 0.0

        return temp

    @maximum_angular_jerk.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_angular_jerk(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumAngularJerk",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_frequency_in_signal(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumFrequencyInSignal")

        if temp is None:
            return 0.0

        return temp

    @maximum_frequency_in_signal.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_frequency_in_signal(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumFrequencyInSignal",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def method_to_define_period(
        self: "Self",
    ) -> "_5729.InertiaAdjustedLoadCasePeriodMethod":
        """mastapy.system_model.analyses_and_results.mbd_analyses.InertiaAdjustedLoadCasePeriodMethod"""
        temp = pythonnet_property_get(self.wrapped, "MethodToDefinePeriod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InertiaAdjustedLoadCasePeriodMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5729",
            "InertiaAdjustedLoadCasePeriodMethod",
        )(value)

    @method_to_define_period.setter
    @exception_bridge
    @enforce_parameter_types
    def method_to_define_period(
        self: "Self", value: "_5729.InertiaAdjustedLoadCasePeriodMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InertiaAdjustedLoadCasePeriodMethod",
        )
        pythonnet_property_set(self.wrapped, "MethodToDefinePeriod", value)

    @property
    @exception_bridge
    def number_of_static_load_cases(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStaticLoadCases")

        if temp is None:
            return 0

        return temp

    @number_of_static_load_cases.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_static_load_cases(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStaticLoadCases",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def power_load_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PowerLoadRotation")

        if temp is None:
            return 0.0

        return temp

    @power_load_rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def power_load_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PowerLoadRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def reference_power_load_to_define_period(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_PowerLoad":
        """ListWithSelectedItem[mastapy.system_model.part_model.PowerLoad]"""
        temp = pythonnet_property_get(self.wrapped, "ReferencePowerLoadToDefinePeriod")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_PowerLoad",
        )(temp)

    @reference_power_load_to_define_period.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_power_load_to_define_period(
        self: "Self", value: "_2703.PowerLoad"
    ) -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_PowerLoad.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ReferencePowerLoadToDefinePeriod", value)

    @property
    @exception_bridge
    def sample_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SampleLength")

        if temp is None:
            return 0.0

        return temp

    @sample_length.setter
    @exception_bridge
    @enforce_parameter_types
    def sample_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SampleLength", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shaft_and_housing_rayleigh_damping_beta(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "ShaftAndHousingRayleighDampingBeta"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @shaft_and_housing_rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_and_housing_rayleigh_damping_beta(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "ShaftAndHousingRayleighDampingBeta", value
        )

    @property
    @exception_bridge
    def start_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartTime")

        if temp is None:
            return 0.0

        return temp

    @start_time.setter
    @exception_bridge
    @enforce_parameter_types
    def start_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def start_at_zero_angle(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "StartAtZeroAngle")

        if temp is None:
            return False

        return temp

    @start_at_zero_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_at_zero_angle(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartAtZeroAngle",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def static_load_case_used_to_set_initial_speeds(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(
            self.wrapped, "StaticLoadCaseUsedToSetInitialSpeeds"
        )

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @static_load_case_used_to_set_initial_speeds.setter
    @exception_bridge
    @enforce_parameter_types
    def static_load_case_used_to_set_initial_speeds(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "StaticLoadCaseUsedToSetInitialSpeeds", value
        )

    @property
    @exception_bridge
    def static_load_cases_to_create(
        self: "Self",
    ) -> "_5730.InertiaAdjustedLoadCaseResultsToCreate":
        """mastapy.system_model.analyses_and_results.mbd_analyses.InertiaAdjustedLoadCaseResultsToCreate"""
        temp = pythonnet_property_get(self.wrapped, "StaticLoadCasesToCreate")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InertiaAdjustedLoadCaseResultsToCreate",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5730",
            "InertiaAdjustedLoadCaseResultsToCreate",
        )(value)

    @static_load_cases_to_create.setter
    @exception_bridge
    @enforce_parameter_types
    def static_load_cases_to_create(
        self: "Self", value: "_5730.InertiaAdjustedLoadCaseResultsToCreate"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InertiaAdjustedLoadCaseResultsToCreate",
        )
        pythonnet_property_set(self.wrapped, "StaticLoadCasesToCreate", value)

    @property
    @exception_bridge
    def use_load_sensitive_stiffness(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseLoadSensitiveStiffness")

        if temp is None:
            return False

        return temp

    @use_load_sensitive_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def use_load_sensitive_stiffness(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseLoadSensitiveStiffness",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_static_load_case_to_set_initial_speeds(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseStaticLoadCaseToSetInitialSpeeds"
        )

        if temp is None:
            return False

        return temp

    @use_static_load_case_to_set_initial_speeds.setter
    @exception_bridge
    @enforce_parameter_types
    def use_static_load_case_to_set_initial_speeds(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseStaticLoadCaseToSetInitialSpeeds",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_temperature_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseTemperatureModel")

        if temp is None:
            return False

        return temp

    @use_temperature_model.setter
    @exception_bridge
    @enforce_parameter_types
    def use_temperature_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseTemperatureModel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def external_interface_options(
        self: "Self",
    ) -> "_5816.DynamicExternalInterfaceOptions":
        """mastapy.system_model.analyses_and_results.mbd_analyses.external_interfaces.DynamicExternalInterfaceOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalInterfaceOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def frequency_response_options(
        self: "Self",
    ) -> "_4904.FrequencyResponseAnalysisOptions":
        """mastapy.system_model.analyses_and_results.modal_analyses.FrequencyResponseAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyResponseOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def run_up_analysis_options(self: "Self") -> "_5746.MBDRunUpAnalysisOptions":
        """mastapy.system_model.analyses_and_results.mbd_analyses.MBDRunUpAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunUpAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def spline_damping_options(self: "Self") -> "_5779.SplineDampingOptions":
        """mastapy.system_model.analyses_and_results.mbd_analyses.SplineDampingOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SplineDampingOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transient_solver_options(self: "Self") -> "_94.TransientSolverOptions":
        """mastapy.nodal_analysis.TransientSolverOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransientSolverOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_MBDAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_MBDAnalysisOptions
        """
        return _Cast_MBDAnalysisOptions(self)

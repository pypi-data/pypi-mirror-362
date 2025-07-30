"""GearSetConfiguration"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_method_call_overload,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ABSTRACT_STATIC_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "AbstractStaticLoadCaseGroup",
)
_GEAR_SET_MODES = python_net_import("SMT.MastaAPI.Gears", "GearSetModes")
_BOOLEAN = python_net_import("System", "Boolean")
_STATIC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "StaticLoadCase"
)
_GEAR_SET_CONFIGURATION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "GearSetConfiguration"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears import _417, _418
    from mastapy._private.gears.analysis import _1347
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5950,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7674
    from mastapy._private.system_model.part_model.gears import (
        _2761,
        _2763,
        _2774,
        _2790,
    )

    Self = TypeVar("Self", bound="GearSetConfiguration")
    CastSelf = TypeVar(
        "CastSelf", bound="GearSetConfiguration._Cast_GearSetConfiguration"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearSetConfiguration",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearSetConfiguration:
    """Special nested class for casting GearSetConfiguration to subclasses."""

    __parent__: "GearSetConfiguration"

    @property
    def gear_set_configuration(self: "CastSelf") -> "GearSetConfiguration":
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
class GearSetConfiguration(_0.APIBase):
    """GearSetConfiguration

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_SET_CONFIGURATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_set_design_group(self: "Self") -> "_417.GearSetDesignGroup":
        """mastapy.gears.GearSetDesignGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetDesignGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def conical_gear_sets(self: "Self") -> "List[_2761.ConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.ConicalGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gear_sets(self: "Self") -> "List[_2763.CylindricalGearSet]":
        """List[mastapy.system_model.part_model.gears.CylindricalGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_gear_sets(
        self: "Self",
    ) -> "List[_2774.KlingelnbergCycloPalloidConicalGearSet]":
        """List[mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergCycloPalloidGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_gear_sets(self: "Self") -> "List[_2790.WormGearSet]":
        """List[mastapy.system_model.part_model.gears.WormGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGearSets")

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
    @enforce_parameter_types
    def implementation_detail_results_for_group(
        self: "Self",
        analysis_case: "_5950.AbstractStaticLoadCaseGroup",
        gear_set_mode: "_418.GearSetModes",
        run_all_planetary_meshes: "bool",
    ) -> "_1347.GearSetGroupDutyCycle":
        """mastapy.gears.analysis.GearSetGroupDutyCycle

        Args:
            analysis_case (mastapy.system_model.analyses_and_results.load_case_groups.AbstractStaticLoadCaseGroup)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ImplementationDetailResultsFor",
            [_ABSTRACT_STATIC_LOAD_CASE_GROUP, _GEAR_SET_MODES, _BOOLEAN],
            analysis_case.wrapped if analysis_case else None,
            gear_set_mode,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def implementation_detail_results_for(
        self: "Self",
        analysis_case: "_7674.StaticLoadCase",
        gear_set_mode: "_418.GearSetModes",
        run_all_planetary_meshes: "bool",
    ) -> "_1347.GearSetGroupDutyCycle":
        """mastapy.gears.analysis.GearSetGroupDutyCycle

        Args:
            analysis_case (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "ImplementationDetailResultsFor",
            [_STATIC_LOAD_CASE, _GEAR_SET_MODES, _BOOLEAN],
            analysis_case.wrapped if analysis_case else None,
            gear_set_mode,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def perform_implementation_detail_analysis_group(
        self: "Self",
        static_load_case_group: "_5950.AbstractStaticLoadCaseGroup",
        gear_set_mode: "_418.GearSetModes",
        run_all_planetary_meshes: "bool" = True,
        perform_system_analysis_if_not_ready: "bool" = True,
    ) -> None:
        """Method does not return.

        Args:
            static_load_case_group (mastapy.system_model.analyses_and_results.load_case_groups.AbstractStaticLoadCaseGroup)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool, optional)
            perform_system_analysis_if_not_ready (bool, optional)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        perform_system_analysis_if_not_ready = bool(
            perform_system_analysis_if_not_ready
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformImplementationDetailAnalysis",
            [_ABSTRACT_STATIC_LOAD_CASE_GROUP, _GEAR_SET_MODES, _BOOLEAN, _BOOLEAN],
            static_load_case_group.wrapped if static_load_case_group else None,
            gear_set_mode,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
            perform_system_analysis_if_not_ready
            if perform_system_analysis_if_not_ready
            else False,
        )

    @exception_bridge
    @enforce_parameter_types
    def perform_implementation_detail_analysis(
        self: "Self",
        static_load: "_7674.StaticLoadCase",
        gear_set_mode: "_418.GearSetModes",
        run_all_planetary_meshes: "bool" = True,
        perform_system_analysis_if_not_ready: "bool" = True,
    ) -> None:
        """Method does not return.

        Args:
            static_load (mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase)
            gear_set_mode (mastapy.gears.GearSetModes)
            run_all_planetary_meshes (bool, optional)
            perform_system_analysis_if_not_ready (bool, optional)
        """
        gear_set_mode = conversion.mp_to_pn_enum(
            gear_set_mode, "SMT.MastaAPI.Gears.GearSetModes"
        )
        run_all_planetary_meshes = bool(run_all_planetary_meshes)
        perform_system_analysis_if_not_ready = bool(
            perform_system_analysis_if_not_ready
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "PerformImplementationDetailAnalysis",
            [_STATIC_LOAD_CASE, _GEAR_SET_MODES, _BOOLEAN, _BOOLEAN],
            static_load.wrapped if static_load else None,
            gear_set_mode,
            run_all_planetary_meshes if run_all_planetary_meshes else False,
            perform_system_analysis_if_not_ready
            if perform_system_analysis_if_not_ready
            else False,
        )

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
    def cast_to(self: "Self") -> "_Cast_GearSetConfiguration":
        """Cast to another type.

        Returns:
            _Cast_GearSetConfiguration
        """
        return _Cast_GearSetConfiguration(self)

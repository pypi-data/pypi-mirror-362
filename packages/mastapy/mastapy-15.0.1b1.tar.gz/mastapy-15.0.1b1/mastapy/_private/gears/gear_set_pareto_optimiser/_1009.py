"""DesignSpaceSearchBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_set_pareto_optimiser import _1006

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_DESIGN_SPACE_SEARCH_BASE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "DesignSpaceSearchBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.gear_set_pareto_optimiser import (
        _1007,
        _1008,
        _1011,
        _1015,
        _1016,
        _1018,
        _1019,
        _1023,
        _1026,
        _1041,
        _1042,
        _1043,
    )
    from mastapy._private.math_utility.optimisation import _1724, _1730, _1733

    Self = TypeVar("Self", bound="DesignSpaceSearchBase")
    CastSelf = TypeVar(
        "CastSelf", bound="DesignSpaceSearchBase._Cast_DesignSpaceSearchBase"
    )

TAnalysis = TypeVar("TAnalysis", bound="_1337.AbstractGearSetAnalysis")
TCandidate = TypeVar("TCandidate")

__docformat__ = "restructuredtext en"
__all__ = ("DesignSpaceSearchBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DesignSpaceSearchBase:
    """Special nested class for casting DesignSpaceSearchBase to subclasses."""

    __parent__: "DesignSpaceSearchBase"

    @property
    def cylindrical_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1008.CylindricalGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1008

        return self.__parent__._cast(_1008.CylindricalGearSetParetoOptimiser)

    @property
    def face_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1011.FaceGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1011

        return self.__parent__._cast(_1011.FaceGearSetParetoOptimiser)

    @property
    def gear_set_pareto_optimiser(self: "CastSelf") -> "_1015.GearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1015

        return self.__parent__._cast(_1015.GearSetParetoOptimiser)

    @property
    def hypoid_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1016.HypoidGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1016

        return self.__parent__._cast(_1016.HypoidGearSetParetoOptimiser)

    @property
    def micro_geometry_design_space_search(
        self: "CastSelf",
    ) -> "_1019.MicroGeometryDesignSpaceSearch":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1019

        return self.__parent__._cast(_1019.MicroGeometryDesignSpaceSearch)

    @property
    def micro_geometry_gear_set_design_space_search(
        self: "CastSelf",
    ) -> "_1023.MicroGeometryGearSetDesignSpaceSearch":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1023

        return self.__parent__._cast(_1023.MicroGeometryGearSetDesignSpaceSearch)

    @property
    def spiral_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1042.SpiralBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1042

        return self.__parent__._cast(_1042.SpiralBevelGearSetParetoOptimiser)

    @property
    def straight_bevel_gear_set_pareto_optimiser(
        self: "CastSelf",
    ) -> "_1043.StraightBevelGearSetParetoOptimiser":
        from mastapy._private.gears.gear_set_pareto_optimiser import _1043

        return self.__parent__._cast(_1043.StraightBevelGearSetParetoOptimiser)

    @property
    def design_space_search_base(self: "CastSelf") -> "DesignSpaceSearchBase":
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
class DesignSpaceSearchBase(_0.APIBase, Generic[TAnalysis, TCandidate]):
    """DesignSpaceSearchBase

    This is a mastapy class.

    Generic Types:
        TAnalysis
        TCandidate
    """

    TYPE: ClassVar["Type"] = _DESIGN_SPACE_SEARCH_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def design_space_search_strategy_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DesignSpaceSearchStrategyDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @design_space_search_strategy_database.setter
    @exception_bridge
    @enforce_parameter_types
    def design_space_search_strategy_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def design_space_search_strategy_database_duty_cycle(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDatabaseDutyCycle",
            "SelectedItemName",
        )

        if temp is None:
            return ""

        return temp

    @design_space_search_strategy_database_duty_cycle.setter
    @exception_bridge
    @enforce_parameter_types
    def design_space_search_strategy_database_duty_cycle(
        self: "Self", value: "str"
    ) -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DesignSpaceSearchStrategyDatabaseDutyCycle",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def display_candidates(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice":
        """EnumWithSelectedValue[mastapy.gears.gear_set_pareto_optimiser.CandidateDisplayChoice]"""
        temp = pythonnet_property_get(self.wrapped, "DisplayCandidates")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @display_candidates.setter
    @exception_bridge
    @enforce_parameter_types
    def display_candidates(self: "Self", value: "_1006.CandidateDisplayChoice") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CandidateDisplayChoice.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DisplayCandidates", value)

    @property
    @exception_bridge
    def maximum_number_of_candidates_to_display(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfCandidatesToDisplay"
        )

        if temp is None:
            return 0

        return temp

    @maximum_number_of_candidates_to_display.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_candidates_to_display(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfCandidatesToDisplay",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_candidates_after_filtering(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCandidatesAfterFiltering")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_dominant_candidates(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfDominantCandidates")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_feasible_candidates(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfFeasibleCandidates")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_unfiltered_candidates(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfUnfilteredCandidates")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_unrateable_designs(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfUnrateableDesigns")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def remove_candidates_with(self: "Self") -> "_1018.LargerOrSmaller":
        """mastapy.gears.gear_set_pareto_optimiser.LargerOrSmaller"""
        temp = pythonnet_property_get(self.wrapped, "RemoveCandidatesWith")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearSetParetoOptimiser.LargerOrSmaller"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_set_pareto_optimiser._1018", "LargerOrSmaller"
        )(value)

    @remove_candidates_with.setter
    @exception_bridge
    @enforce_parameter_types
    def remove_candidates_with(self: "Self", value: "_1018.LargerOrSmaller") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearSetParetoOptimiser.LargerOrSmaller"
        )
        pythonnet_property_set(self.wrapped, "RemoveCandidatesWith", value)

    @property
    @exception_bridge
    def reporting_string_for_too_many_candidates_to_be_evaluated(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReportingStringForTooManyCandidatesToBeEvaluated"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def total_number_of_candidates_to_be_evaluated(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalNumberOfCandidatesToBeEvaluated"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def viewing_candidates_selected_in_chart(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ViewingCandidatesSelectedInChart")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def load_case_duty_cycle(self: "Self") -> "TAnalysis":
        """TAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_candidate(self: "Self") -> "TAnalysis":
        """TAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedCandidate")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_design_space_search_strategy(
        self: "Self",
    ) -> "_1733.ParetoOptimisationStrategy":
        """mastapy.math_utility.optimisation.ParetoOptimisationStrategy

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedDesignSpaceSearchStrategy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def all_candidate_designs_including_original_design(
        self: "Self",
    ) -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllCandidateDesignsIncludingOriginalDesign"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_candidate_designs_to_display(self: "Self") -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllCandidateDesignsToDisplay")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_candidate_designs_to_display_without_original_design(
        self: "Self",
    ) -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllCandidateDesignsToDisplayWithoutOriginalDesign"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def candidate_designs_to_display(self: "Self") -> "List[TCandidate]":
        """List[TCandidate]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CandidateDesignsToDisplay")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def chart_details(
        self: "Self",
    ) -> "List[_1007.ChartInfoBase[TAnalysis, TCandidate]]":
        """List[mastapy.gears.gear_set_pareto_optimiser.ChartInfoBase[TAnalysis, TCandidate]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChartDetails")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def filters(self: "Self") -> "List[_1730.ParetoOptimisationFilter]":
        """List[mastapy.math_utility.optimisation.ParetoOptimisationFilter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Filters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def input_setters(self: "Self") -> "List[_1724.InputSetter[TAnalysis]]":
        """List[mastapy.math_utility.optimisation.InputSetter[TAnalysis]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InputSetters")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def optimisation_targets(
        self: "Self",
    ) -> "List[_1026.OptimisationTarget[TAnalysis]]":
        """List[mastapy.gears.gear_set_pareto_optimiser.OptimisationTarget[TAnalysis]]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OptimisationTargets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def reasons_for_invalid_candidates(
        self: "Self",
    ) -> "List[_1041.ReasonsForInvalidDesigns]":
        """List[mastapy.gears.gear_set_pareto_optimiser.ReasonsForInvalidDesigns]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReasonsForInvalidCandidates")

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
    def add_table_filter(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddTableFilter")

    @exception_bridge
    def find_dominant_candidates(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FindDominantCandidates")

    @exception_bridge
    def load_strategy(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LoadStrategy")

    @exception_bridge
    def save_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SaveResults")

    @exception_bridge
    def save_strategy(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SaveStrategy")

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
    def cast_to(self: "Self") -> "_Cast_DesignSpaceSearchBase":
        """Cast to another type.

        Returns:
            _Cast_DesignSpaceSearchBase
        """
        return _Cast_DesignSpaceSearchBase(self)

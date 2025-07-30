"""ML1MicroGeometryOptimiser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ML1_MICRO_GEOMETRY_OPTIMISER = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.MachineLearning", "ML1MicroGeometryOptimiser"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1221
    from mastapy._private.math_utility.bayesian_optimization import _1765, _1766, _1769
    from mastapy._private.system_model.optimization.machine_learning import (
        _2457,
        _2458,
        _2460,
    )
    from mastapy._private.utility_gui.charts import _2065

    Self = TypeVar("Self", bound="ML1MicroGeometryOptimiser")
    CastSelf = TypeVar(
        "CastSelf", bound="ML1MicroGeometryOptimiser._Cast_ML1MicroGeometryOptimiser"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ML1MicroGeometryOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ML1MicroGeometryOptimiser:
    """Special nested class for casting ML1MicroGeometryOptimiser to subclasses."""

    __parent__: "ML1MicroGeometryOptimiser"

    @property
    def ml1_micro_geometry_optimiser(self: "CastSelf") -> "ML1MicroGeometryOptimiser":
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
class ML1MicroGeometryOptimiser(_0.APIBase):
    """ML1MicroGeometryOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ML1_MICRO_GEOMETRY_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Analysis")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def editable_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "EditableName")

        if temp is None:
            return ""

        return temp

    @editable_name.setter
    @exception_bridge
    @enforce_parameter_types
    def editable_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "EditableName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def micro_geometry_used_for_optimisation(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometryUsedForOptimisation")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def number_of_iterations_completed(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfIterationsCompleted")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def scatter_chart(self: "Self") -> "_2065.ScatterChartDefinition":
        """mastapy.utility_gui.charts.ScatterChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ScatterChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stage(self: "Self") -> "_1769.OptimizationStage":
        """mastapy.math_utility.bayesian_optimization.OptimizationStage

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stage")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.MathUtility.BayesianOptimization.OptimizationStage"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility.bayesian_optimization._1769",
            "OptimizationStage",
        )(value)

    @property
    @exception_bridge
    def starting_micro_geometry(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "StartingMicroGeometry")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @starting_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def starting_micro_geometry(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "StartingMicroGeometry", value)

    @property
    @exception_bridge
    def selected_results(
        self: "Self",
    ) -> "_1221.CylindricalGearSetMicroGeometryDutyCycle":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometryDutyCycle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def settings(self: "Self") -> "_1766.ML1OptimizerSettings":
        """mastapy.math_utility.bayesian_optimization.ML1OptimizerSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Settings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def constraints(self: "Self") -> "List[_2458.LoadCaseConstraint]":
        """List[mastapy.system_model.optimization.machine_learning.LoadCaseConstraint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Constraints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def duty_cycle_results(
        self: "Self",
    ) -> "List[_1221.CylindricalGearSetMicroGeometryDutyCycle]":
        """List[mastapy.gears.gear_designs.cylindrical.micro_geometry.CylindricalGearSetMicroGeometryDutyCycle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DutyCycleResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def flank_parameter_selections(
        self: "Self",
    ) -> "List[_2457.GearFlankParameterSelection]":
        """List[mastapy.system_model.optimization.machine_learning.GearFlankParameterSelection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankParameterSelections")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def snapshots(self: "Self") -> "List[_1765.ML1OptimiserSnapshot]":
        """List[mastapy.math_utility.bayesian_optimization.ML1OptimiserSnapshot]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Snapshots")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def targets(self: "Self") -> "List[_2460.LoadCaseTarget]":
        """List[mastapy.system_model.optimization.machine_learning.LoadCaseTarget]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Targets")

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
    def add_constraint(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddConstraint")

    @exception_bridge
    def add_selected_micro_geometry(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddSelectedMicroGeometry")

    @exception_bridge
    def add_target(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddTarget")

    @exception_bridge
    def clear_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearResults")

    @exception_bridge
    def delete_optimiser(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteOptimiser")

    @exception_bridge
    def select_best_micro_geometry(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectBestMicroGeometry")

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
    def cast_to(self: "Self") -> "_Cast_ML1MicroGeometryOptimiser":
        """Cast to another type.

        Returns:
            _Cast_ML1MicroGeometryOptimiser
        """
        return _Cast_ML1MicroGeometryOptimiser(self)

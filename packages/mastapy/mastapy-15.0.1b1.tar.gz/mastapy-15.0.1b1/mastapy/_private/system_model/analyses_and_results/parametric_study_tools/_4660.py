"""ParametricStudyVariable"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.system_model.analyses_and_results import _2889

_PARAMETRIC_STUDY_VARIABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyVariable",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4613,
        _4647,
        _4652,
    )

    Self = TypeVar("Self", bound="ParametricStudyVariable")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyVariable._Cast_ParametricStudyVariable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyVariable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyVariable:
    """Special nested class for casting ParametricStudyVariable to subclasses."""

    __parent__: "ParametricStudyVariable"

    @property
    def analysis_case_variable(self: "CastSelf") -> "_2889.AnalysisCaseVariable":
        return self.__parent__._cast(_2889.AnalysisCaseVariable)

    @property
    def parametric_study_variable(self: "CastSelf") -> "ParametricStudyVariable":
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
class ParametricStudyVariable(_2889.AnalysisCaseVariable):
    """ParametricStudyVariable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_VARIABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def current_values(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentValues")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def dimension(self: "Self") -> "_4652.ParametricStudyDimension":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyDimension"""
        temp = pythonnet_property_get(self.wrapped, "Dimension")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.ParametricStudyDimension",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.parametric_study_tools._4652",
            "ParametricStudyDimension",
        )(value)

    @dimension.setter
    @exception_bridge
    @enforce_parameter_types
    def dimension(self: "Self", value: "_4652.ParametricStudyDimension") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.ParametricStudyDimension",
        )
        pythonnet_property_set(self.wrapped, "Dimension", value)

    @property
    @exception_bridge
    def distribution(self: "Self") -> "_4647.MonteCarloDistribution":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.MonteCarloDistribution"""
        temp = pythonnet_property_get(self.wrapped, "Distribution")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.MonteCarloDistribution",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.parametric_study_tools._4647",
            "MonteCarloDistribution",
        )(value)

    @distribution.setter
    @exception_bridge
    @enforce_parameter_types
    def distribution(self: "Self", value: "_4647.MonteCarloDistribution") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.MonteCarloDistribution",
        )
        pythonnet_property_set(self.wrapped, "Distribution", value)

    @property
    @exception_bridge
    def end_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndValue")

        if temp is None:
            return 0.0

        return temp

    @end_value.setter
    @exception_bridge
    @enforce_parameter_types
    def end_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EndValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def group(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Group")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @group.setter
    @exception_bridge
    @enforce_parameter_types
    def group(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Group", value)

    @property
    @exception_bridge
    def maximum_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumValue")

        if temp is None:
            return 0.0

        return temp

    @maximum_value.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mean_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanValue")

        if temp is None:
            return 0.0

        return temp

    @mean_value.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minimum_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumValue")

        if temp is None:
            return 0.0

        return temp

    @minimum_value.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def parameter_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def show_variable_on_axis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowVariableOnAxis")

        if temp is None:
            return False

        return temp

    @show_variable_on_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def show_variable_on_axis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowVariableOnAxis",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def standard_deviation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StandardDeviation")

        if temp is None:
            return 0.0

        return temp

    @standard_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def standard_deviation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StandardDeviation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartValue")

        if temp is None:
            return 0.0

        return temp

    @start_value.setter
    @exception_bridge
    @enforce_parameter_types
    def start_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StartValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def doe_variable_setter(self: "Self") -> "_4613.DesignOfExperimentsVariableSetter":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.DesignOfExperimentsVariableSetter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DOEVariableSetter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def end_value_in_si_units(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EndValueInSIUnits")

        if temp is None:
            return 0.0

        return temp

    @end_value_in_si_units.setter
    @exception_bridge
    @enforce_parameter_types
    def end_value_in_si_units(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EndValueInSIUnits",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_value_in_si_units(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanValueInSIUnits")

        if temp is None:
            return 0.0

        return temp

    @mean_value_in_si_units.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_value_in_si_units(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanValueInSIUnits",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def standard_deviation_in_si_units(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StandardDeviationInSIUnits")

        if temp is None:
            return 0.0

        return temp

    @standard_deviation_in_si_units.setter
    @exception_bridge
    @enforce_parameter_types
    def standard_deviation_in_si_units(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StandardDeviationInSIUnits",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_value_in_si_units(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartValueInSIUnits")

        if temp is None:
            return 0.0

        return temp

    @start_value_in_si_units.setter
    @exception_bridge
    @enforce_parameter_types
    def start_value_in_si_units(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartValueInSIUnits",
            float(value) if value is not None else 0.0,
        )

    @exception_bridge
    def add_to_new_group(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddToNewGroup")

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @exception_bridge
    def down(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Down")

    @exception_bridge
    def set_values(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetValues")

    @exception_bridge
    def up(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Up")

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyVariable":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyVariable
        """
        return _Cast_ParametricStudyVariable(self)

"""FlexiblePinAnalysisOptions"""

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5954
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_FLEXIBLE_PIN_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "FlexiblePinAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FlexiblePinAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="FlexiblePinAnalysisOptions._Cast_FlexiblePinAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FlexiblePinAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FlexiblePinAnalysisOptions:
    """Special nested class for casting FlexiblePinAnalysisOptions to subclasses."""

    __parent__: "FlexiblePinAnalysisOptions"

    @property
    def flexible_pin_analysis_options(self: "CastSelf") -> "FlexiblePinAnalysisOptions":
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
class FlexiblePinAnalysisOptions(_0.APIBase):
    """FlexiblePinAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FLEXIBLE_PIN_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def extreme_load_case(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCase")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @extreme_load_case.setter
    @exception_bridge
    @enforce_parameter_types
    def extreme_load_case(self: "Self", value: "_7674.StaticLoadCase") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ExtremeLoadCase", value)

    @property
    @exception_bridge
    def extreme_load_case_for_stop_start(self: "Self") -> "_7674.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase"""
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCaseForStopStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @extreme_load_case_for_stop_start.setter
    @exception_bridge
    @enforce_parameter_types
    def extreme_load_case_for_stop_start(
        self: "Self", value: "_7674.StaticLoadCase"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ExtremeLoadCaseForStopStart", value.wrapped
        )

    @property
    @exception_bridge
    def include_flexible_bearing_races(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFlexibleBearingRaces")

        if temp is None:
            return False

        return temp

    @include_flexible_bearing_races.setter
    @exception_bridge
    @enforce_parameter_types
    def include_flexible_bearing_races(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeFlexibleBearingRaces",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def ldd(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_DutyCycle":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle]"""
        temp = pythonnet_property_get(self.wrapped, "LDD")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DutyCycle",
        )(temp)

    @ldd.setter
    @exception_bridge
    @enforce_parameter_types
    def ldd(self: "Self", value: "_5954.DutyCycle") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "LDD", value)

    @property
    @exception_bridge
    def nominal_load_case(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCase")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @nominal_load_case.setter
    @exception_bridge
    @enforce_parameter_types
    def nominal_load_case(self: "Self", value: "_7674.StaticLoadCase") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "NominalLoadCase", value)

    @property
    @exception_bridge
    def nominal_load_case_for_stop_start(self: "Self") -> "_7674.StaticLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase"""
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCaseForStopStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @nominal_load_case_for_stop_start.setter
    @exception_bridge
    @enforce_parameter_types
    def nominal_load_case_for_stop_start(
        self: "Self", value: "_7674.StaticLoadCase"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "NominalLoadCaseForStopStart", value.wrapped
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FlexiblePinAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_FlexiblePinAnalysisOptions
        """
        return _Cast_FlexiblePinAnalysisOptions(self)

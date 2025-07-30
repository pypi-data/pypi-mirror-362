"""WindTurbineCertificationReport"""

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.flexible_pin_analyses import (
    _6580,
)
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5954
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_WIND_TURBINE_CERTIFICATION_REPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.FlexiblePinAnalyses",
    "WindTurbineCertificationReport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3043,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.compound import (
        _3191,
    )
    from mastapy._private.system_model.part_model import _2706

    Self = TypeVar("Self", bound="WindTurbineCertificationReport")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WindTurbineCertificationReport._Cast_WindTurbineCertificationReport",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WindTurbineCertificationReport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WindTurbineCertificationReport:
    """Special nested class for casting WindTurbineCertificationReport to subclasses."""

    __parent__: "WindTurbineCertificationReport"

    @property
    def combination_analysis(self: "CastSelf") -> "_6580.CombinationAnalysis":
        return self.__parent__._cast(_6580.CombinationAnalysis)

    @property
    def wind_turbine_certification_report(
        self: "CastSelf",
    ) -> "WindTurbineCertificationReport":
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
class WindTurbineCertificationReport(_6580.CombinationAnalysis):
    """WindTurbineCertificationReport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WIND_TURBINE_CERTIFICATION_REPORT

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
    def design(self: "Self") -> "_2706.RootAssembly":
        """mastapy.system_model.part_model.RootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def extreme_load_case_static_analysis(
        self: "Self",
    ) -> "_3043.RootAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtremeLoadCaseStaticAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ldd_static_analysis(
        self: "Self",
    ) -> "_3191.RootAssemblyCompoundSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.compound.RootAssemblyCompoundSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LDDStaticAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def nominal_load_case_static_analysis(
        self: "Self",
    ) -> "_3043.RootAssemblySystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.RootAssemblySystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalLoadCaseStaticAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_WindTurbineCertificationReport":
        """Cast to another type.

        Returns:
            _Cast_WindTurbineCertificationReport
        """
        return _Cast_WindTurbineCertificationReport(self)

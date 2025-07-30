"""SystemOptimiser"""

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
from mastapy._private.system_model.analyses_and_results.load_case_groups import _5954

_SYSTEM_OPTIMISER = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.SystemOptimiser", "SystemOptimiser"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.rating import _453
    from mastapy._private.system_model import _2411
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5958,
    )
    from mastapy._private.system_model.optimization.system_optimiser import (
        _2449,
        _2452,
        _2453,
    )
    from mastapy._private.system_model.part_model.gears import _2763, _2769
    from mastapy._private.utility.logging import _2005

    Self = TypeVar("Self", bound="SystemOptimiser")
    CastSelf = TypeVar("CastSelf", bound="SystemOptimiser._Cast_SystemOptimiser")


__docformat__ = "restructuredtext en"
__all__ = ("SystemOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SystemOptimiser:
    """Special nested class for casting SystemOptimiser to subclasses."""

    __parent__: "SystemOptimiser"

    @property
    def system_optimiser(self: "CastSelf") -> "SystemOptimiser":
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
class SystemOptimiser(_0.APIBase):
    """SystemOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYSTEM_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def selected_duty_cycle_for_system_optimiser(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_DutyCycle":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle]"""
        temp = pythonnet_property_get(
            self.wrapped, "SelectedDutyCycleForSystemOptimiser"
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_DutyCycle",
        )(temp)

    @selected_duty_cycle_for_system_optimiser.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_duty_cycle_for_system_optimiser(
        self: "Self", value: "_5954.DutyCycle"
    ) -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_DutyCycle.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "SelectedDutyCycleForSystemOptimiser", value
        )

    @property
    @exception_bridge
    def design(self: "Self") -> "_2411.Design":
        """mastapy.system_model.Design

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
    def details(self: "Self") -> "_2452.SystemOptimiserDetails":
        """mastapy.system_model.optimization.system_optimiser.SystemOptimiserDetails

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Details")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def log(self: "Self") -> "_2005.Logger":
        """mastapy.utility.logging.Logger

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Log")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def tooth_number_finder(self: "Self") -> "_2453.ToothNumberFinder":
        """mastapy.system_model.optimization.system_optimiser.ToothNumberFinder

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothNumberFinder")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def gear_set_ratings_fast_power_flow(
        self: "Self",
    ) -> "List[_453.GearSetDutyCycleRating]":
        """List[mastapy.gears.rating.GearSetDutyCycleRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSetRatingsFastPowerFlow")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_sets(self: "Self") -> "List[_2769.GearSet]":
        """List[mastapy.system_model.part_model.gears.GearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def system_optimisation_gear_sets(
        self: "Self",
    ) -> "List[_5958.SystemOptimisationGearSet]":
        """List[mastapy.system_model.analyses_and_results.load_case_groups.SystemOptimisationGearSet]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemOptimisationGearSets")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def target_ratios(self: "Self") -> "List[_2449.DesignStateTargetRatio]":
        """List[mastapy.system_model.optimization.system_optimiser.DesignStateTargetRatio]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TargetRatios")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def system_optimiser_duty_cycle(self: "Self") -> "_5954.DutyCycle":
        """mastapy.system_model.analyses_and_results.load_case_groups.DutyCycle"""
        temp = pythonnet_property_get(self.wrapped, "SystemOptimiserDutyCycle")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @system_optimiser_duty_cycle.setter
    @exception_bridge
    @enforce_parameter_types
    def system_optimiser_duty_cycle(self: "Self", value: "_5954.DutyCycle") -> None:
        pythonnet_property_set(self.wrapped, "SystemOptimiserDutyCycle", value.wrapped)

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
    def cast_to(self: "Self") -> "_Cast_SystemOptimiser":
        """Cast to another type.

        Returns:
            _Cast_SystemOptimiser
        """
        return _Cast_SystemOptimiser(self)

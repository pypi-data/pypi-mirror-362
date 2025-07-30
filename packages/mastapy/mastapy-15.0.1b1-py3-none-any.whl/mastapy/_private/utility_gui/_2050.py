"""ColumnInputOptions"""

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
from mastapy._private.utility.file_access_helpers import _2014
from mastapy._private.utility.units_and_measurements import _1802

_COLUMN_INPUT_OPTIONS = python_net_import(
    "SMT.MastaAPI.UtilityGUI", "ColumnInputOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7861,
        _7862,
        _7864,
        _7865,
        _7866,
        _7867,
        _7869,
        _7870,
        _7871,
        _7872,
        _7874,
        _7875,
    )
    from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
        _2793,
        _2794,
        _2795,
        _2798,
    )

    Self = TypeVar("Self", bound="ColumnInputOptions")
    CastSelf = TypeVar("CastSelf", bound="ColumnInputOptions._Cast_ColumnInputOptions")


__docformat__ = "restructuredtext en"
__all__ = ("ColumnInputOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ColumnInputOptions:
    """Special nested class for casting ColumnInputOptions to subclasses."""

    __parent__: "ColumnInputOptions"

    @property
    def boost_pressure_input_options(
        self: "CastSelf",
    ) -> "_2793.BoostPressureInputOptions":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2793,
        )

        return self.__parent__._cast(_2793.BoostPressureInputOptions)

    @property
    def input_power_input_options(self: "CastSelf") -> "_2794.InputPowerInputOptions":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2794,
        )

        return self.__parent__._cast(_2794.InputPowerInputOptions)

    @property
    def pressure_ratio_input_options(
        self: "CastSelf",
    ) -> "_2795.PressureRatioInputOptions":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2795,
        )

        return self.__parent__._cast(_2795.PressureRatioInputOptions)

    @property
    def rotor_speed_input_options(self: "CastSelf") -> "_2798.RotorSpeedInputOptions":
        from mastapy._private.system_model.part_model.gears.supercharger_rotor_set import (
            _2798,
        )

        return self.__parent__._cast(_2798.RotorSpeedInputOptions)

    @property
    def boost_pressure_load_case_input_options(
        self: "CastSelf",
    ) -> "_7861.BoostPressureLoadCaseInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7861,
        )

        return self.__parent__._cast(_7861.BoostPressureLoadCaseInputOptions)

    @property
    def design_state_options(self: "CastSelf") -> "_7862.DesignStateOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7862,
        )

        return self.__parent__._cast(_7862.DesignStateOptions)

    @property
    def force_input_options(self: "CastSelf") -> "_7864.ForceInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7864,
        )

        return self.__parent__._cast(_7864.ForceInputOptions)

    @property
    def gear_ratio_input_options(self: "CastSelf") -> "_7865.GearRatioInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7865,
        )

        return self.__parent__._cast(_7865.GearRatioInputOptions)

    @property
    def load_case_name_options(self: "CastSelf") -> "_7866.LoadCaseNameOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7866,
        )

        return self.__parent__._cast(_7866.LoadCaseNameOptions)

    @property
    def moment_input_options(self: "CastSelf") -> "_7867.MomentInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7867,
        )

        return self.__parent__._cast(_7867.MomentInputOptions)

    @property
    def point_load_input_options(self: "CastSelf") -> "_7869.PointLoadInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7869,
        )

        return self.__parent__._cast(_7869.PointLoadInputOptions)

    @property
    def power_load_input_options(self: "CastSelf") -> "_7870.PowerLoadInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7870,
        )

        return self.__parent__._cast(_7870.PowerLoadInputOptions)

    @property
    def ramp_or_steady_state_input_options(
        self: "CastSelf",
    ) -> "_7871.RampOrSteadyStateInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7871,
        )

        return self.__parent__._cast(_7871.RampOrSteadyStateInputOptions)

    @property
    def speed_input_options(self: "CastSelf") -> "_7872.SpeedInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7872,
        )

        return self.__parent__._cast(_7872.SpeedInputOptions)

    @property
    def time_step_input_options(self: "CastSelf") -> "_7874.TimeStepInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7874,
        )

        return self.__parent__._cast(_7874.TimeStepInputOptions)

    @property
    def torque_input_options(self: "CastSelf") -> "_7875.TorqueInputOptions":
        from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
            _7875,
        )

        return self.__parent__._cast(_7875.TorqueInputOptions)

    @property
    def column_input_options(self: "CastSelf") -> "ColumnInputOptions":
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
class ColumnInputOptions(_0.APIBase):
    """ColumnInputOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COLUMN_INPUT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def column(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_ColumnTitle":
        """ListWithSelectedItem[mastapy.utility.file_access_helpers.ColumnTitle]"""
        temp = pythonnet_property_get(self.wrapped, "Column")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_ColumnTitle",
        )(temp)

    @column.setter
    @exception_bridge
    @enforce_parameter_types
    def column(self: "Self", value: "_2014.ColumnTitle") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_ColumnTitle.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Column", value)

    @property
    @exception_bridge
    def unit(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @unit.setter
    @exception_bridge
    @enforce_parameter_types
    def unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Unit", value)

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
    def cast_to(self: "Self") -> "_Cast_ColumnInputOptions":
        """Cast to another type.

        Returns:
            _Cast_ColumnInputOptions
        """
        return _Cast_ColumnInputOptions(self)

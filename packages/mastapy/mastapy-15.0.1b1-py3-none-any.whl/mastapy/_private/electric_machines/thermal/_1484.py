"""ThermalEndWindingSurfaceCollection"""

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
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.thermal import _1466

_THERMAL_END_WINDING_SURFACE_COLLECTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalEndWindingSurfaceCollection"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.thermal import _1467, _1468
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _223

    Self = TypeVar("Self", bound="ThermalEndWindingSurfaceCollection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThermalEndWindingSurfaceCollection._Cast_ThermalEndWindingSurfaceCollection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalEndWindingSurfaceCollection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalEndWindingSurfaceCollection:
    """Special nested class for casting ThermalEndWindingSurfaceCollection to subclasses."""

    __parent__: "ThermalEndWindingSurfaceCollection"

    @property
    def thermal_end_winding_surface_collection(
        self: "CastSelf",
    ) -> "ThermalEndWindingSurfaceCollection":
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
class ThermalEndWindingSurfaceCollection(_0.APIBase):
    """ThermalEndWindingSurfaceCollection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_END_WINDING_SURFACE_COLLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cooling_source(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_EndWindingCoolingFlowSource":
        """EnumWithSelectedValue[mastapy.electric_machines.thermal.EndWindingCoolingFlowSource]"""
        temp = pythonnet_property_get(self.wrapped, "CoolingSource")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_EndWindingCoolingFlowSource.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @cooling_source.setter
    @exception_bridge
    @enforce_parameter_types
    def cooling_source(
        self: "Self", value: "_1466.EndWindingCoolingFlowSource"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_EndWindingCoolingFlowSource.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "CoolingSource", value)

    @property
    @exception_bridge
    def end_winding_length_source(self: "Self") -> "_1467.EndWindingLengthSource":
        """mastapy.electric_machines.thermal.EndWindingLengthSource"""
        temp = pythonnet_property_get(self.wrapped, "EndWindingLengthSource")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.Thermal.EndWindingLengthSource"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.thermal._1467", "EndWindingLengthSource"
        )(value)

    @end_winding_length_source.setter
    @exception_bridge
    @enforce_parameter_types
    def end_winding_length_source(
        self: "Self", value: "_1467.EndWindingLengthSource"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.Thermal.EndWindingLengthSource"
        )
        pythonnet_property_set(self.wrapped, "EndWindingLengthSource", value)

    @property
    @exception_bridge
    def weighted_flow_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WeightedFlowRatio")

        if temp is None:
            return 0.0

        return temp

    @weighted_flow_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def weighted_flow_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WeightedFlowRatio",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def user_defined_heat_transfer_coefficient(
        self: "Self",
    ) -> "_223.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "UserDefinedHeatTransferCoefficient"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def surfaces(self: "Self") -> "List[_1468.EndWindingThermalElement]":
        """List[mastapy.electric_machines.thermal.EndWindingThermalElement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Surfaces")

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
    def cast_to(self: "Self") -> "_Cast_ThermalEndWindingSurfaceCollection":
        """Cast to another type.

        Returns:
            _Cast_ThermalEndWindingSurfaceCollection
        """
        return _Cast_ThermalEndWindingSurfaceCollection(self)

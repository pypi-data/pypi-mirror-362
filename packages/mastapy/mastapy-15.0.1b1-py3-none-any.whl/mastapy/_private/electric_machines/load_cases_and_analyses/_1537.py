"""ElectricMachineBasicMechanicalLossSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELECTRIC_MACHINE_BASIC_MECHANICAL_LOSS_SETTINGS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses",
    "ElectricMachineBasicMechanicalLossSettings",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ElectricMachineBasicMechanicalLossSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineBasicMechanicalLossSettings._Cast_ElectricMachineBasicMechanicalLossSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineBasicMechanicalLossSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineBasicMechanicalLossSettings:
    """Special nested class for casting ElectricMachineBasicMechanicalLossSettings to subclasses."""

    __parent__: "ElectricMachineBasicMechanicalLossSettings"

    @property
    def electric_machine_basic_mechanical_loss_settings(
        self: "CastSelf",
    ) -> "ElectricMachineBasicMechanicalLossSettings":
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
class ElectricMachineBasicMechanicalLossSettings(_0.APIBase):
    """ElectricMachineBasicMechanicalLossSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_BASIC_MECHANICAL_LOSS_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def friction_loss_exponent(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FrictionLossExponent")

        if temp is None:
            return 0.0

        return temp

    @friction_loss_exponent.setter
    @exception_bridge
    @enforce_parameter_types
    def friction_loss_exponent(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FrictionLossExponent",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def friction_losses_at_reference_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FrictionLossesAtReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @friction_losses_at_reference_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def friction_losses_at_reference_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FrictionLossesAtReferenceSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_basic_mechanical_losses_calculation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeBasicMechanicalLossesCalculation"
        )

        if temp is None:
            return False

        return temp

    @include_basic_mechanical_losses_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def include_basic_mechanical_losses_calculation(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBasicMechanicalLossesCalculation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def reference_speed_for_mechanical_losses(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedForMechanicalLosses")

        if temp is None:
            return 0.0

        return temp

    @reference_speed_for_mechanical_losses.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_speed_for_mechanical_losses(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReferenceSpeedForMechanicalLosses",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def windage_loss_exponent(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WindageLossExponent")

        if temp is None:
            return 0.0

        return temp

    @windage_loss_exponent.setter
    @exception_bridge
    @enforce_parameter_types
    def windage_loss_exponent(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WindageLossExponent",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def windage_loss_at_reference_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WindageLossAtReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @windage_loss_at_reference_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def windage_loss_at_reference_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WindageLossAtReferenceSpeed",
            float(value) if value is not None else 0.0,
        )

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineBasicMechanicalLossSettings":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineBasicMechanicalLossSettings
        """
        return _Cast_ElectricMachineBasicMechanicalLossSettings(self)

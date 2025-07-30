"""ElectricMachineAnalysis"""

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
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ELECTRIC_MACHINE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "ElectricMachineAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1387, _1394
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1531,
        _1534,
        _1540,
        _1541,
        _1543,
        _1554,
        _1558,
    )

    Self = TypeVar("Self", bound="ElectricMachineAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineAnalysis._Cast_ElectricMachineAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineAnalysis:
    """Special nested class for casting ElectricMachineAnalysis to subclasses."""

    __parent__: "ElectricMachineAnalysis"

    @property
    def dynamic_force_analysis(self: "CastSelf") -> "_1531.DynamicForceAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1531

        return self.__parent__._cast(_1531.DynamicForceAnalysis)

    @property
    def efficiency_map_analysis(self: "CastSelf") -> "_1534.EfficiencyMapAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1534

        return self.__parent__._cast(_1534.EfficiencyMapAnalysis)

    @property
    def electric_machine_fe_analysis(
        self: "CastSelf",
    ) -> "_1540.ElectricMachineFEAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1540

        return self.__parent__._cast(_1540.ElectricMachineFEAnalysis)

    @property
    def electric_machine_fe_mechanical_analysis(
        self: "CastSelf",
    ) -> "_1541.ElectricMachineFEMechanicalAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1541

        return self.__parent__._cast(_1541.ElectricMachineFEMechanicalAnalysis)

    @property
    def single_operating_point_analysis(
        self: "CastSelf",
    ) -> "_1554.SingleOperatingPointAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1554

        return self.__parent__._cast(_1554.SingleOperatingPointAnalysis)

    @property
    def speed_torque_curve_analysis(
        self: "CastSelf",
    ) -> "_1558.SpeedTorqueCurveAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1558

        return self.__parent__._cast(_1558.SpeedTorqueCurveAnalysis)

    @property
    def electric_machine_analysis(self: "CastSelf") -> "ElectricMachineAnalysis":
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
class ElectricMachineAnalysis(_0.APIBase):
    """ElectricMachineAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FieldWindingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def magnet_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagnetTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def windings_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingsTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electric_machine_detail(self: "Self") -> "_1387.ElectricMachineDetail":
        """mastapy.electric_machines.ElectricMachineDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_1543.ElectricMachineLoadCaseBase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseBase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def setup(self: "Self") -> "_1394.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def results_ready(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsReady")

        if temp is None:
            return False

        return temp

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
    def perform_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformAnalysis")

    @exception_bridge
    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", token: "_7901.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            token (mastapy.TaskProgress)
        """
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysisWithProgress",
            token.wrapped if token else None,
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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineAnalysis
        """
        return _Cast_ElectricMachineAnalysis(self)

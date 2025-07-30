"""HarmonicLoadDataBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
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
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1566

_FOURIER_SERIES = python_net_import("SMT.MastaAPI.MathUtility", "FourierSeries")
_LIST = python_net_import("System.Collections.Generic", "List")
_DOUBLE = python_net_import("System", "Double")
_STRING = python_net_import("System", "String")
_MEASUREMENT_TYPE = python_net_import(
    "SMT.MastaAPIUtility.UnitsAndMeasurements", "MeasurementType"
)
_HARMONIC_LOAD_DATA_BASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "HarmonicLoadDataBase"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.harmonic_load_data import _1562, _1568
    from mastapy._private.electric_machines.results import _1505
    from mastapy._private.math_utility import _1697
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7716,
        _7733,
        _7740,
        _7741,
        _7742,
        _7743,
        _7744,
        _7745,
        _7746,
        _7763,
        _7808,
        _7851,
    )
    from mastapy._private.units_and_measurements import _7903

    Self = TypeVar("Self", bound="HarmonicLoadDataBase")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicLoadDataBase._Cast_HarmonicLoadDataBase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicLoadDataBase:
    """Special nested class for casting HarmonicLoadDataBase to subclasses."""

    __parent__: "HarmonicLoadDataBase"

    @property
    def dynamic_force_results(self: "CastSelf") -> "_1505.DynamicForceResults":
        from mastapy._private.electric_machines.results import _1505

        return self.__parent__._cast(_1505.DynamicForceResults)

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1562.ElectricMachineHarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1562

        return self.__parent__._cast(_1562.ElectricMachineHarmonicLoadDataBase)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1568.SpeedDependentHarmonicLoadData":
        from mastapy._private.electric_machines.harmonic_load_data import _1568

        return self.__parent__._cast(_1568.SpeedDependentHarmonicLoadData)

    @property
    def conical_gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7716.ConicalGearSetHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7716,
        )

        return self.__parent__._cast(_7716.ConicalGearSetHarmonicLoadData)

    @property
    def cylindrical_gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7733.CylindricalGearSetHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7733,
        )

        return self.__parent__._cast(_7733.CylindricalGearSetHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7740.ElectricMachineHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7740,
        )

        return self.__parent__._cast(_7740.ElectricMachineHarmonicLoadData)

    @property
    def electric_machine_harmonic_load_data_from_excel(
        self: "CastSelf",
    ) -> "_7741.ElectricMachineHarmonicLoadDataFromExcel":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7741,
        )

        return self.__parent__._cast(_7741.ElectricMachineHarmonicLoadDataFromExcel)

    @property
    def electric_machine_harmonic_load_data_from_flux(
        self: "CastSelf",
    ) -> "_7742.ElectricMachineHarmonicLoadDataFromFlux":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7742,
        )

        return self.__parent__._cast(_7742.ElectricMachineHarmonicLoadDataFromFlux)

    @property
    def electric_machine_harmonic_load_data_from_jmag(
        self: "CastSelf",
    ) -> "_7743.ElectricMachineHarmonicLoadDataFromJMAG":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7743,
        )

        return self.__parent__._cast(_7743.ElectricMachineHarmonicLoadDataFromJMAG)

    @property
    def electric_machine_harmonic_load_data_from_masta(
        self: "CastSelf",
    ) -> "_7744.ElectricMachineHarmonicLoadDataFromMASTA":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7744,
        )

        return self.__parent__._cast(_7744.ElectricMachineHarmonicLoadDataFromMASTA)

    @property
    def electric_machine_harmonic_load_data_from_motor_cad(
        self: "CastSelf",
    ) -> "_7745.ElectricMachineHarmonicLoadDataFromMotorCAD":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7745,
        )

        return self.__parent__._cast(_7745.ElectricMachineHarmonicLoadDataFromMotorCAD)

    @property
    def electric_machine_harmonic_load_data_from_motor_packages(
        self: "CastSelf",
    ) -> "_7746.ElectricMachineHarmonicLoadDataFromMotorPackages":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7746,
        )

        return self.__parent__._cast(
            _7746.ElectricMachineHarmonicLoadDataFromMotorPackages
        )

    @property
    def gear_set_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7763.GearSetHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7763,
        )

        return self.__parent__._cast(_7763.GearSetHarmonicLoadData)

    @property
    def point_load_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7808.PointLoadHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7808,
        )

        return self.__parent__._cast(_7808.PointLoadHarmonicLoadData)

    @property
    def unbalanced_mass_harmonic_load_data(
        self: "CastSelf",
    ) -> "_7851.UnbalancedMassHarmonicLoadData":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7851,
        )

        return self.__parent__._cast(_7851.UnbalancedMassHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "HarmonicLoadDataBase":
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
class HarmonicLoadDataBase(_0.APIBase):
    """HarmonicLoadDataBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_LOAD_DATA_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def data_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]"""
        temp = pythonnet_property_get(self.wrapped, "DataType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @data_type.setter
    @exception_bridge
    @enforce_parameter_types
    def data_type(self: "Self", value: "_1566.HarmonicLoadDataType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DataType", value)

    @property
    @exception_bridge
    def excitation_order_as_rotational_order_of_shaft(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ExcitationOrderAsRotationalOrderOfShaft"
        )

        if temp is None:
            return 0.0

        return temp

    @excitation_order_as_rotational_order_of_shaft.setter
    @exception_bridge
    @enforce_parameter_types
    def excitation_order_as_rotational_order_of_shaft(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcitationOrderAsRotationalOrderOfShaft",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_cycles_in_signal(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCyclesInSignal")

        if temp is None:
            return 0.0

        return temp

    @number_of_cycles_in_signal.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycles_in_signal(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCyclesInSignal",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_harmonics(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfHarmonics")

        if temp is None:
            return 0

        return temp

    @number_of_harmonics.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_harmonics(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfHarmonics", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_values(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfValues")

        if temp is None:
            return 0

        return temp

    @number_of_values.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_values(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfValues", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def excitations(self: "Self") -> "List[_1697.FourierSeries]":
        """List[mastapy.math_utility.FourierSeries]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Excitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def peak_to_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeak")

        if temp is None:
            return 0.0

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
    def clear_all_data(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearAllData")

    @exception_bridge
    def clear_selected_data(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearSelectedData")

    @exception_bridge
    @enforce_parameter_types
    def set_selected_harmonic_load_data_with_fourier_series(
        self: "Self", fourier_series: "_1697.FourierSeries"
    ) -> None:
        """Method does not return.

        Args:
            fourier_series (mastapy.math_utility.FourierSeries)
        """
        pythonnet_method_call_overload(
            self.wrapped,
            "SetSelectedHarmonicLoadData",
            [_FOURIER_SERIES],
            fourier_series.wrapped if fourier_series else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_selected_harmonic_load_data_extended(
        self: "Self",
        amplitudes: "List[float]",
        phases: "List[float]",
        mean_value: "float",
        fourier_series_name: "str",
        fourier_series_measurement_type: "_7903.MeasurementType",
    ) -> None:
        """Method does not return.

        Args:
            amplitudes (List[float])
            phases (List[float])
            mean_value (float)
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        amplitudes = conversion.mp_to_pn_list_float(amplitudes)
        phases = conversion.mp_to_pn_list_float(phases)
        mean_value = float(mean_value)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(
            fourier_series_measurement_type,
            "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType",
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "SetSelectedHarmonicLoadData",
            [_LIST[_DOUBLE], _LIST[_DOUBLE], _DOUBLE, _STRING, _MEASUREMENT_TYPE],
            amplitudes,
            phases,
            mean_value if mean_value else 0.0,
            fourier_series_name if fourier_series_name else "",
            fourier_series_measurement_type,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_selected_harmonic_load_data(
        self: "Self",
        fourier_series_values: "List[float]",
        fourier_series_name: "str",
        fourier_series_measurement_type: "_7903.MeasurementType",
    ) -> None:
        """Method does not return.

        Args:
            fourier_series_values (List[float])
            fourier_series_name (str)
            fourier_series_measurement_type (mastapy.units_and_measurements.MeasurementType)
        """
        fourier_series_values = conversion.mp_to_pn_list_float(fourier_series_values)
        fourier_series_name = str(fourier_series_name)
        fourier_series_measurement_type = conversion.mp_to_pn_enum(
            fourier_series_measurement_type,
            "SMT.MastaAPIUtility.UnitsAndMeasurements.MeasurementType",
        )
        pythonnet_method_call_overload(
            self.wrapped,
            "SetSelectedHarmonicLoadData",
            [_LIST[_DOUBLE], _STRING, _MEASUREMENT_TYPE],
            fourier_series_values,
            fourier_series_name if fourier_series_name else "",
            fourier_series_measurement_type,
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
    def cast_to(self: "Self") -> "_Cast_HarmonicLoadDataBase":
        """Cast to another type.

        Returns:
            _Cast_HarmonicLoadDataBase
        """
        return _Cast_HarmonicLoadDataBase(self)

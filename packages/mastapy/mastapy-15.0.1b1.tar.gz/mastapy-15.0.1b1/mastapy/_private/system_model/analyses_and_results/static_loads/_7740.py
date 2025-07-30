"""ElectricMachineHarmonicLoadData"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.harmonic_load_data import _1562, _1566
from mastapy._private.system_model.analyses_and_results.static_loads import _7848

_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineHarmonicLoadData",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.harmonic_load_data import _1564, _1568
    from mastapy._private.math_utility import _1697
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7741,
        _7742,
        _7743,
        _7744,
        _7745,
        _7746,
    )

    Self = TypeVar("Self", bound="ElectricMachineHarmonicLoadData")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineHarmonicLoadData._Cast_ElectricMachineHarmonicLoadData",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineHarmonicLoadData",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineHarmonicLoadData:
    """Special nested class for casting ElectricMachineHarmonicLoadData to subclasses."""

    __parent__: "ElectricMachineHarmonicLoadData"

    @property
    def electric_machine_harmonic_load_data_base(
        self: "CastSelf",
    ) -> "_1562.ElectricMachineHarmonicLoadDataBase":
        return self.__parent__._cast(_1562.ElectricMachineHarmonicLoadDataBase)

    @property
    def speed_dependent_harmonic_load_data(
        self: "CastSelf",
    ) -> "_1568.SpeedDependentHarmonicLoadData":
        from mastapy._private.electric_machines.harmonic_load_data import _1568

        return self.__parent__._cast(_1568.SpeedDependentHarmonicLoadData)

    @property
    def harmonic_load_data_base(self: "CastSelf") -> "_1564.HarmonicLoadDataBase":
        from mastapy._private.electric_machines.harmonic_load_data import _1564

        return self.__parent__._cast(_1564.HarmonicLoadDataBase)

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
    def electric_machine_harmonic_load_data(
        self: "CastSelf",
    ) -> "ElectricMachineHarmonicLoadData":
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
class ElectricMachineHarmonicLoadData(_1562.ElectricMachineHarmonicLoadDataBase):
    """ElectricMachineHarmonicLoadData

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_HARMONIC_LOAD_DATA

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def apply_to_all_data_types(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ApplyToAllDataTypes")

        if temp is None:
            return False

        return temp

    @apply_to_all_data_types.setter
    @exception_bridge
    @enforce_parameter_types
    def apply_to_all_data_types(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyToAllDataTypes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def apply_to_all_speeds_for_selected_data_type(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ApplyToAllSpeedsForSelectedDataType"
        )

        if temp is None:
            return False

        return temp

    @apply_to_all_speeds_for_selected_data_type.setter
    @exception_bridge
    @enforce_parameter_types
    def apply_to_all_speeds_for_selected_data_type(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ApplyToAllSpeedsForSelectedDataType",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def constant_torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConstantTorque")

        if temp is None:
            return 0.0

        return temp

    @constant_torque.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ConstantTorque", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def data_type_for_scaling(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType":
        """EnumWithSelectedValue[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]"""
        temp = pythonnet_property_get(self.wrapped, "DataTypeForScaling")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @data_type_for_scaling.setter
    @exception_bridge
    @enforce_parameter_types
    def data_type_for_scaling(
        self: "Self", value: "_1566.HarmonicLoadDataType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_HarmonicLoadDataType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DataTypeForScaling", value)

    @property
    @exception_bridge
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff"
        )

        if temp is None:
            return 0.0

        return temp

    @rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_moment_from_stator_teeth_axial_loads_amplitude_cut_off(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorMomentFromStatorTeethAxialLoadsAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rotor_z_force_amplitude_cut_off(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorZForceAmplitudeCutOff")

        if temp is None:
            return 0.0

        return temp

    @rotor_z_force_amplitude_cut_off.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_z_force_amplitude_cut_off(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorZForceAmplitudeCutOff",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def scale(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Scale")

        if temp is None:
            return 0.0

        return temp

    @scale.setter
    @exception_bridge
    @enforce_parameter_types
    def scale(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Scale", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def torque_ripple_input_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.TorqueRippleInputType]"""
        temp = pythonnet_property_get(self.wrapped, "TorqueRippleInputType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @torque_ripple_input_type.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_ripple_input_type(
        self: "Self", value: "_7848.TorqueRippleInputType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_TorqueRippleInputType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "TorqueRippleInputType", value)

    @property
    @exception_bridge
    def use_stator_radius_from_masta_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseStatorRadiusFromMASTAModel")

        if temp is None:
            return False

        return temp

    @use_stator_radius_from_masta_model.setter
    @exception_bridge
    @enforce_parameter_types
    def use_stator_radius_from_masta_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseStatorRadiusFromMASTAModel",
            bool(value) if value is not None else False,
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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineHarmonicLoadData":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineHarmonicLoadData
        """
        return _Cast_ElectricMachineHarmonicLoadData(self)

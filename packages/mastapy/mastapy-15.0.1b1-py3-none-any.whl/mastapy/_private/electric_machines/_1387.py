"""ElectricMachineDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines import _1386

_ELECTRIC_MACHINE_DETAIL = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineDetail"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import (
        _1365,
        _1368,
        _1381,
        _1394,
        _1397,
        _1410,
        _1421,
        _1424,
        _1428,
        _1429,
        _1439,
        _1441,
        _1458,
    )
    from mastapy._private.electric_machines.results import _1526, _1527
    from mastapy._private.utility import _1783

    Self = TypeVar("Self", bound="ElectricMachineDetail")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineDetail._Cast_ElectricMachineDetail"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineDetail:
    """Special nested class for casting ElectricMachineDetail to subclasses."""

    __parent__: "ElectricMachineDetail"

    @property
    def electric_machine_design_base(
        self: "CastSelf",
    ) -> "_1386.ElectricMachineDesignBase":
        return self.__parent__._cast(_1386.ElectricMachineDesignBase)

    @property
    def cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1368.CADElectricMachineDetail":
        from mastapy._private.electric_machines import _1368

        return self.__parent__._cast(_1368.CADElectricMachineDetail)

    @property
    def interior_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1410.InteriorPermanentMagnetMachine":
        from mastapy._private.electric_machines import _1410

        return self.__parent__._cast(_1410.InteriorPermanentMagnetMachine)

    @property
    def non_cad_electric_machine_detail(
        self: "CastSelf",
    ) -> "_1421.NonCADElectricMachineDetail":
        from mastapy._private.electric_machines import _1421

        return self.__parent__._cast(_1421.NonCADElectricMachineDetail)

    @property
    def permanent_magnet_assisted_synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "_1424.PermanentMagnetAssistedSynchronousReluctanceMachine":
        from mastapy._private.electric_machines import _1424

        return self.__parent__._cast(
            _1424.PermanentMagnetAssistedSynchronousReluctanceMachine
        )

    @property
    def surface_permanent_magnet_machine(
        self: "CastSelf",
    ) -> "_1439.SurfacePermanentMagnetMachine":
        from mastapy._private.electric_machines import _1439

        return self.__parent__._cast(_1439.SurfacePermanentMagnetMachine)

    @property
    def synchronous_reluctance_machine(
        self: "CastSelf",
    ) -> "_1441.SynchronousReluctanceMachine":
        from mastapy._private.electric_machines import _1441

        return self.__parent__._cast(_1441.SynchronousReluctanceMachine)

    @property
    def wound_field_synchronous_machine(
        self: "CastSelf",
    ) -> "_1458.WoundFieldSynchronousMachine":
        from mastapy._private.electric_machines import _1458

        return self.__parent__._cast(_1458.WoundFieldSynchronousMachine)

    @property
    def electric_machine_detail(self: "CastSelf") -> "ElectricMachineDetail":
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
class ElectricMachineDetail(_1386.ElectricMachineDesignBase):
    """ElectricMachineDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def core_loss_build_factor_specification_method(
        self: "Self",
    ) -> "_1381.CoreLossBuildFactorSpecificationMethod":
        """mastapy.electric_machines.CoreLossBuildFactorSpecificationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "CoreLossBuildFactorSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.CoreLossBuildFactorSpecificationMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1381",
            "CoreLossBuildFactorSpecificationMethod",
        )(value)

    @core_loss_build_factor_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def core_loss_build_factor_specification_method(
        self: "Self", value: "_1381.CoreLossBuildFactorSpecificationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.CoreLossBuildFactorSpecificationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "CoreLossBuildFactorSpecificationMethod", value
        )

    @property
    @exception_bridge
    def dc_bus_voltage(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DCBusVoltage")

        if temp is None:
            return 0.0

        return temp

    @dc_bus_voltage.setter
    @exception_bridge
    @enforce_parameter_types
    def dc_bus_voltage(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DCBusVoltage", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def eddy_current_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EddyCurrentCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @eddy_current_core_loss_build_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def eddy_current_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EddyCurrentCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def effective_machine_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveMachineLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electric_machine_type(self: "Self") -> "_1397.ElectricMachineType":
        """mastapy.electric_machines.ElectricMachineType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.ElectricMachineType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1397", "ElectricMachineType"
        )(value)

    @property
    @exception_bridge
    def enclosing_volume(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnclosingVolume")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def excess_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ExcessCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @excess_core_loss_build_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def excess_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcessCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def has_non_linear_dq_model(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasNonLinearDQModel")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def hysteresis_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HysteresisCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @hysteresis_core_loss_build_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def hysteresis_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HysteresisCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_shaft(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeShaft")

        if temp is None:
            return False

        return temp

    @include_shaft.setter
    @exception_bridge
    @enforce_parameter_types
    def include_shaft(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IncludeShaft", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def line_line_supply_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineLineSupplyVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def machine_drawing(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MachineDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def machine_periodicity_factor(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MachinePeriodicityFactor")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @machine_periodicity_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def machine_periodicity_factor(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MachinePeriodicityFactor", value)

    @property
    @exception_bridge
    def magnet_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MagnetLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @magnet_loss_build_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def magnet_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MagnetLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_phases(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPhases")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_slots_per_phase(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsPerPhase")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_slots_per_pole(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsPerPole")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_slots_per_pole_per_phase(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSlotsPerPolePerPhase")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_supply_voltage_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseSupplyVoltagePeak")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_supply_voltage_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseSupplyVoltageRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_air_gap(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialAirGap")

        if temp is None:
            return 0.0

        return temp

    @radial_air_gap.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_air_gap(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialAirGap", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rated_inverter_current_peak(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RatedInverterCurrentPeak")

        if temp is None:
            return 0.0

        return temp

    @rated_inverter_current_peak.setter
    @exception_bridge
    @enforce_parameter_types
    def rated_inverter_current_peak(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RatedInverterCurrentPeak",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rated_inverter_phase_current_peak(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatedInverterPhaseCurrentPeak")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rotor_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RotorCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @rotor_core_loss_build_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RotorCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftDiameter")

        if temp is None:
            return 0.0

        return temp

    @shaft_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stator_core_loss_build_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StatorCoreLossBuildFactor")

        if temp is None:
            return 0.0

        return temp

    @stator_core_loss_build_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def stator_core_loss_build_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StatorCoreLossBuildFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def non_linear_dq_model(self: "Self") -> "_1526.NonLinearDQModel":
        """mastapy.electric_machines.results.NonLinearDQModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonLinearDQModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def non_linear_dq_model_generator_settings(
        self: "Self",
    ) -> "_1527.NonLinearDQModelGeneratorSettings":
        """mastapy.electric_machines.results.NonLinearDQModelGeneratorSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NonLinearDQModelGeneratorSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def results_locations_specification(
        self: "Self",
    ) -> "_1428.ResultsLocationsSpecification":
        """mastapy.electric_machines.ResultsLocationsSpecification

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsLocationsSpecification")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor(self: "Self") -> "_1429.Rotor":
        """mastapy.electric_machines.Rotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def selected_setup(self: "Self") -> "_1394.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedSetup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator(self: "Self") -> "_1365.AbstractStator":
        """mastapy.electric_machines.AbstractStator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stator")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def setups(self: "Self") -> "List[_1394.ElectricMachineSetup]":
        """List[mastapy.electric_machines.ElectricMachineSetup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setups")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def generate_cad_geometry_model(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateCADGeometryModel")

    @exception_bridge
    def add_setup(self: "Self") -> "_1394.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup"""
        method_result = pythonnet_method_call(self.wrapped, "AddSetup")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def duplicate_setup(
        self: "Self", setup: "_1394.ElectricMachineSetup"
    ) -> "_1394.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "DuplicateSetup", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def export_to_smt_format(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call(self.wrapped, "ExportToSMTFormat", file_name)

    @exception_bridge
    def generate_design_without_non_linear_dq_model(
        self: "Self",
    ) -> "_1783.MethodOutcomeWithResult[ElectricMachineDetail]":
        """mastapy.utility.MethodOutcomeWithResult[mastapy.electric_machines.ElectricMachineDetail]"""
        method_result = pythonnet_method_call(
            self.wrapped, "GenerateDesignWithoutNonLinearDQModel"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def setup_named(self: "Self", name: "str") -> "_1394.ElectricMachineSetup":
        """mastapy.electric_machines.ElectricMachineSetup

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "SetupNamed", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def try_generate_non_linear_dq_model(
        self: "Self",
    ) -> "_1783.MethodOutcomeWithResult[ElectricMachineDetail]":
        """mastapy.utility.MethodOutcomeWithResult[mastapy.electric_machines.ElectricMachineDetail]"""
        method_result = pythonnet_method_call(
            self.wrapped, "TryGenerateNonLinearDQModel"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def try_generate_non_linear_dq_model_with_task_progress(
        self: "Self", progress: "_7901.TaskProgress"
    ) -> "_1783.MethodOutcomeWithResult[ElectricMachineDetail]":
        """mastapy.utility.MethodOutcomeWithResult[mastapy.electric_machines.ElectricMachineDetail]

        Args:
            progress (mastapy.TaskProgress)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "TryGenerateNonLinearDQModelWithTaskProgress",
            progress.wrapped if progress else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def write_dxf_to(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call(self.wrapped, "WriteDxfTo", file_name)

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineDetail":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineDetail
        """
        return _Cast_ElectricMachineDetail(self)

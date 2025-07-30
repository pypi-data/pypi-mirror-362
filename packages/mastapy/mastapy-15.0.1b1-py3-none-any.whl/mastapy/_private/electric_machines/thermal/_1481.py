"""ThermalElectricMachineSetup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
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
from mastapy._private.electric_machines import _1395

_THERMAL_ELECTRIC_MACHINE_SETUP = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalElectricMachineSetup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines import _1396
    from mastapy._private.electric_machines.thermal import _1460, _1470, _1478
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _225
    from mastapy._private.utility import _1782

    Self = TypeVar("Self", bound="ThermalElectricMachineSetup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThermalElectricMachineSetup._Cast_ThermalElectricMachineSetup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalElectricMachineSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalElectricMachineSetup:
    """Special nested class for casting ThermalElectricMachineSetup to subclasses."""

    __parent__: "ThermalElectricMachineSetup"

    @property
    def electric_machine_setup_base(
        self: "CastSelf",
    ) -> "_1395.ElectricMachineSetupBase":
        return self.__parent__._cast(_1395.ElectricMachineSetupBase)

    @property
    def thermal_electric_machine_setup(
        self: "CastSelf",
    ) -> "ThermalElectricMachineSetup":
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
class ThermalElectricMachineSetup(_1395.ElectricMachineSetupBase):
    """ThermalElectricMachineSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_ELECTRIC_MACHINE_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_additional_slices(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfAdditionalSlices")

        if temp is None:
            return 0

        return temp

    @number_of_additional_slices.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_additional_slices(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfAdditionalSlices",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_axial_slices(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfAxialSlices")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_element(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfElement")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_nodes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfNodes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def meshing_options(self: "Self") -> "_1396.ElectricMachineThermalMeshingOptions":
        """mastapy.electric_machines.ElectricMachineThermalMeshingOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshingOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def slice_length_information_reporter(
        self: "Self",
    ) -> "_1478.SliceLengthInformationReporter":
        """mastapy.electric_machines.thermal.SliceLengthInformationReporter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SliceLengthInformationReporter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def additional_slices(self: "Self") -> "List[_1460.AdditionalSliceSpecification]":
        """List[mastapy.electric_machines.thermal.AdditionalSliceSpecification]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalSlices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def housing_channel_modification_factors(
        self: "Self",
    ) -> "List[_1470.HousingChannelModificationFactors]":
        """List[mastapy.electric_machines.thermal.HousingChannelModificationFactors]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HousingChannelModificationFactors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def user_defined_nodes(self: "Self") -> "List[_225.UserDefinedNodeInformation]":
        """List[mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedNodeInformation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserDefinedNodes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def add_user_defined_node(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddUserDefinedNode")

    @exception_bridge
    def generate_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateMesh")

    @exception_bridge
    @enforce_parameter_types
    def try_copy_user_defined_nodes_to_other_setups(
        self: "Self", setups: "List[ThermalElectricMachineSetup]"
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome

        Args:
            setups (List[mastapy.electric_machines.thermal.ThermalElectricMachineSetup])
        """
        setups = conversion.mp_to_pn_objects_in_dotnet_list(setups)
        method_result = pythonnet_method_call(
            self.wrapped, "TryCopyUserDefinedNodesToOtherSetups", setups
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ThermalElectricMachineSetup":
        """Cast to another type.

        Returns:
            _Cast_ThermalElectricMachineSetup
        """
        return _Cast_ThermalElectricMachineSetup(self)

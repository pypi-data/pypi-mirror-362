"""ElectricMachineSetup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private.electric_machines import _1395

_ELECTRIC_MACHINE_SETUP = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "ElectricMachineSetup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1385, _1446, _1447

    Self = TypeVar("Self", bound="ElectricMachineSetup")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineSetup._Cast_ElectricMachineSetup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineSetup:
    """Special nested class for casting ElectricMachineSetup to subclasses."""

    __parent__: "ElectricMachineSetup"

    @property
    def electric_machine_setup_base(
        self: "CastSelf",
    ) -> "_1395.ElectricMachineSetupBase":
        return self.__parent__._cast(_1395.ElectricMachineSetupBase)

    @property
    def electric_machine_setup(self: "CastSelf") -> "ElectricMachineSetup":
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
class ElectricMachineSetup(_1395.ElectricMachineSetupBase):
    """ElectricMachineSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def estimated_material_cost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EstimatedMaterialCost")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_air_gap_elements(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfAirGapElements")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def two_d_fe_model_for_electromagnetic_analysis(
        self: "Self",
    ) -> "_1446.TwoDimensionalFEModelForElectromagneticAnalysis":
        """mastapy.electric_machines.TwoDimensionalFEModelForElectromagneticAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TwoDFEModelForElectromagneticAnalysis"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def two_d_fe_model_for_mechanical_analysis(
        self: "Self",
    ) -> "_1447.TwoDimensionalFEModelForMechanicalAnalysis":
        """mastapy.electric_machines.TwoDimensionalFEModelForMechanicalAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TwoDFEModelForMechanicalAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def eccentricity(self: "Self") -> "_1385.Eccentricity":
        """mastapy.electric_machines.Eccentricity

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Eccentricity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def generate_electromagnetic_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateElectromagneticMesh")

    @exception_bridge
    def generate_mechanical_mesh(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GenerateMechanicalMesh")

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineSetup":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineSetup
        """
        return _Cast_ElectricMachineSetup(self)

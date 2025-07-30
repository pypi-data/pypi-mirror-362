"""ElectricMachineFEMechanicalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.load_cases_and_analyses import _1536

_ELECTRIC_MACHINE_FE_MECHANICAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses",
    "ElectricMachineFEMechanicalAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import _1545
    from mastapy._private.electric_machines.results import _1508
    from mastapy._private.nodal_analysis.elmer import _254

    Self = TypeVar("Self", bound="ElectricMachineFEMechanicalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineFEMechanicalAnalysis._Cast_ElectricMachineFEMechanicalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineFEMechanicalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineFEMechanicalAnalysis:
    """Special nested class for casting ElectricMachineFEMechanicalAnalysis to subclasses."""

    __parent__: "ElectricMachineFEMechanicalAnalysis"

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1536.ElectricMachineAnalysis":
        return self.__parent__._cast(_1536.ElectricMachineAnalysis)

    @property
    def electric_machine_fe_mechanical_analysis(
        self: "CastSelf",
    ) -> "ElectricMachineFEMechanicalAnalysis":
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
class ElectricMachineFEMechanicalAnalysis(_1536.ElectricMachineAnalysis):
    """ElectricMachineFEMechanicalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_FE_MECHANICAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def electric_machine_mechanical_results(
        self: "Self",
    ) -> "_1508.ElectricMachineMechanicalResults":
        """mastapy.electric_machines.results.ElectricMachineMechanicalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineMechanicalResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_1545.ElectricMachineMechanicalLoadCase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineMechanicalLoadCase

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
    def viewable(self: "Self") -> "_254.ElmerResultsViewable":
        """mastapy.nodal_analysis.elmer.ElmerResultsViewable

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Viewable")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineFEMechanicalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineFEMechanicalAnalysis
        """
        return _Cast_ElectricMachineFEMechanicalAnalysis(self)

"""ElectricMachineFEAnalysis"""

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
from mastapy._private.electric_machines.load_cases_and_analyses import _1554
from mastapy._private.electric_machines.results import _1523

_ELECTRIC_MACHINE_FE_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "ElectricMachineFEAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.load_cases_and_analyses import _1536
    from mastapy._private.electric_machines.results import _1505
    from mastapy._private.nodal_analysis.elmer import _254

    Self = TypeVar("Self", bound="ElectricMachineFEAnalysis")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineFEAnalysis._Cast_ElectricMachineFEAnalysis"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineFEAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineFEAnalysis:
    """Special nested class for casting ElectricMachineFEAnalysis to subclasses."""

    __parent__: "ElectricMachineFEAnalysis"

    @property
    def single_operating_point_analysis(
        self: "CastSelf",
    ) -> "_1554.SingleOperatingPointAnalysis":
        return self.__parent__._cast(_1554.SingleOperatingPointAnalysis)

    @property
    def electric_machine_analysis(self: "CastSelf") -> "_1536.ElectricMachineAnalysis":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1536

        return self.__parent__._cast(_1536.ElectricMachineAnalysis)

    @property
    def electric_machine_fe_analysis(self: "CastSelf") -> "ElectricMachineFEAnalysis":
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
class ElectricMachineFEAnalysis(
    _1554.SingleOperatingPointAnalysis, _1523.IHaveDynamicForceResults
):
    """ElectricMachineFEAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_FE_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def electromagnetic_solver_analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectromagneticSolverAnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_force_results(self: "Self") -> "_1505.DynamicForceResults":
        """mastapy.electric_machines.results.DynamicForceResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicForceResults")

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineFEAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineFEAnalysis
        """
        return _Cast_ElectricMachineFEAnalysis(self)

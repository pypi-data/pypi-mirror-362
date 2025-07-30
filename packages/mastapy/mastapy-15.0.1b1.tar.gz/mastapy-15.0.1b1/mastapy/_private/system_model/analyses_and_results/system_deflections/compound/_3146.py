"""DutyCycleEfficiencyResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_DUTY_CYCLE_EFFICIENCY_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound",
    "DutyCycleEfficiencyResults",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3018,
    )

    Self = TypeVar("Self", bound="DutyCycleEfficiencyResults")
    CastSelf = TypeVar(
        "CastSelf", bound="DutyCycleEfficiencyResults._Cast_DutyCycleEfficiencyResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DutyCycleEfficiencyResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycleEfficiencyResults:
    """Special nested class for casting DutyCycleEfficiencyResults to subclasses."""

    __parent__: "DutyCycleEfficiencyResults"

    @property
    def duty_cycle_efficiency_results(self: "CastSelf") -> "DutyCycleEfficiencyResults":
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
class DutyCycleEfficiencyResults(_0.APIBase):
    """DutyCycleEfficiencyResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_EFFICIENCY_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def efficiency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Efficiency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_input(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyInput")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_lost(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyLost")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def energy_output(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EnergyOutput")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def load_case_overall_efficiency_result(
        self: "Self",
    ) -> "List[_3018.LoadCaseOverallEfficiencyResult]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.LoadCaseOverallEfficiencyResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseOverallEfficiencyResult")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_DutyCycleEfficiencyResults":
        """Cast to another type.

        Returns:
            _Cast_DutyCycleEfficiencyResults
        """
        return _Cast_DutyCycleEfficiencyResults(self)

"""EfficiencyMapLoadCase"""

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
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.load_cases_and_analyses import _1551

_EFFICIENCY_MAP_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "EfficiencyMapLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1394
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1534,
        _1539,
        _1543,
    )

    Self = TypeVar("Self", bound="EfficiencyMapLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="EfficiencyMapLoadCase._Cast_EfficiencyMapLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EfficiencyMapLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EfficiencyMapLoadCase:
    """Special nested class for casting EfficiencyMapLoadCase to subclasses."""

    __parent__: "EfficiencyMapLoadCase"

    @property
    def non_linear_dq_model_multiple_operating_points_load_case(
        self: "CastSelf",
    ) -> "_1551.NonLinearDQModelMultipleOperatingPointsLoadCase":
        return self.__parent__._cast(
            _1551.NonLinearDQModelMultipleOperatingPointsLoadCase
        )

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1543

        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def efficiency_map_load_case(self: "CastSelf") -> "EfficiencyMapLoadCase":
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
class EfficiencyMapLoadCase(_1551.NonLinearDQModelMultipleOperatingPointsLoadCase):
    """EfficiencyMapLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _EFFICIENCY_MAP_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def efficiency_map_settings(
        self: "Self",
    ) -> "_1539.ElectricMachineEfficiencyMapSettings":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineEfficiencyMapSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EfficiencyMapSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def analysis_for(
        self: "Self", setup: "_1394.ElectricMachineSetup"
    ) -> "_1534.EfficiencyMapAnalysis":
        """mastapy.electric_machines.load_cases_and_analyses.EfficiencyMapAnalysis

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "AnalysisFor", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_EfficiencyMapLoadCase":
        """Cast to another type.

        Returns:
            _Cast_EfficiencyMapLoadCase
        """
        return _Cast_EfficiencyMapLoadCase(self)

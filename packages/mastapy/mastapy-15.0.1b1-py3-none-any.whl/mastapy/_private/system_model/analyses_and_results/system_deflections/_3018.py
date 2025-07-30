"""LoadCaseOverallEfficiencyResult"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_LOAD_CASE_OVERALL_EFFICIENCY_RESULT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "LoadCaseOverallEfficiencyResult",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadCaseOverallEfficiencyResult")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadCaseOverallEfficiencyResult._Cast_LoadCaseOverallEfficiencyResult",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadCaseOverallEfficiencyResult",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadCaseOverallEfficiencyResult:
    """Special nested class for casting LoadCaseOverallEfficiencyResult to subclasses."""

    __parent__: "LoadCaseOverallEfficiencyResult"

    @property
    def load_case_overall_efficiency_result(
        self: "CastSelf",
    ) -> "LoadCaseOverallEfficiencyResult":
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
class LoadCaseOverallEfficiencyResult(_0.APIBase):
    """LoadCaseOverallEfficiencyResult

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_CASE_OVERALL_EFFICIENCY_RESULT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def duration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

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
    def cast_to(self: "Self") -> "_Cast_LoadCaseOverallEfficiencyResult":
        """Cast to another type.

        Returns:
            _Cast_LoadCaseOverallEfficiencyResult
        """
        return _Cast_LoadCaseOverallEfficiencyResult(self)

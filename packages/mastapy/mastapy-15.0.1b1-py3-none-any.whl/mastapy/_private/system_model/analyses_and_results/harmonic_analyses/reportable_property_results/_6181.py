"""ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic"""

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

_RESULTS_FOR_SINGLE_DEGREE_OF_FREEDOM_OF_RESPONSE_OF_NODE_IN_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar(
        "Self", bound="ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic._Cast_ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic:
    """Special nested class for casting ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic to subclasses."""

    __parent__: "ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic"

    @property
    def results_for_single_degree_of_freedom_of_response_of_node_in_harmonic(
        self: "CastSelf",
    ) -> "ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
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
class ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic(_0.APIBase):
    """ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _RESULTS_FOR_SINGLE_DEGREE_OF_FREEDOM_OF_RESPONSE_OF_NODE_IN_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def frequency_of_max(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfMax")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def integral_with_respect_to_frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntegralWithRespectToFrequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def integral_with_respect_to_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntegralWithRespectToSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Max")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_of_max(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedOfMax")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """Cast to another type.

        Returns:
            _Cast_ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic
        """
        return _Cast_ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic(self)

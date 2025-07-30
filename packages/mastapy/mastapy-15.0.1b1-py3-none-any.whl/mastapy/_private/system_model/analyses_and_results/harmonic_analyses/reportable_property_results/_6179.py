"""ResultsForResponseOfAComponentOrSurfaceInAHarmonic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_RESULTS_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_IN_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForResponseOfAComponentOrSurfaceInAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6161,
        _6181,
    )

    Self = TypeVar("Self", bound="ResultsForResponseOfAComponentOrSurfaceInAHarmonic")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForResponseOfAComponentOrSurfaceInAHarmonic._Cast_ResultsForResponseOfAComponentOrSurfaceInAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForResponseOfAComponentOrSurfaceInAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForResponseOfAComponentOrSurfaceInAHarmonic:
    """Special nested class for casting ResultsForResponseOfAComponentOrSurfaceInAHarmonic to subclasses."""

    __parent__: "ResultsForResponseOfAComponentOrSurfaceInAHarmonic"

    @property
    def results_for_response_of_a_component_or_surface_in_a_harmonic(
        self: "CastSelf",
    ) -> "ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
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
class ResultsForResponseOfAComponentOrSurfaceInAHarmonic(_0.APIBase):
    """ResultsForResponseOfAComponentOrSurfaceInAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _RESULTS_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_IN_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def magnitude(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Magnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def result_at_reference_speed(
        self: "Self",
    ) -> "_6161.DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultAtReferenceSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def data_points(
        self: "Self",
    ) -> "List[_6161.DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DataPoints")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_ResultsForResponseOfAComponentOrSurfaceInAHarmonic
        """
        return _Cast_ResultsForResponseOfAComponentOrSurfaceInAHarmonic(self)

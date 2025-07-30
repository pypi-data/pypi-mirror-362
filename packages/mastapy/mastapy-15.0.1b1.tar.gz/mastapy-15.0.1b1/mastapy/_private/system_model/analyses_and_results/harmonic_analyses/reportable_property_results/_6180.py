"""ResultsForResponseOfANodeOnAHarmonic"""

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

_RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForResponseOfANodeOnAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6162,
        _6181,
    )

    Self = TypeVar("Self", bound="ResultsForResponseOfANodeOnAHarmonic")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForResponseOfANodeOnAHarmonic._Cast_ResultsForResponseOfANodeOnAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForResponseOfANodeOnAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForResponseOfANodeOnAHarmonic:
    """Special nested class for casting ResultsForResponseOfANodeOnAHarmonic to subclasses."""

    __parent__: "ResultsForResponseOfANodeOnAHarmonic"

    @property
    def results_for_response_of_a_node_on_a_harmonic(
        self: "CastSelf",
    ) -> "ResultsForResponseOfANodeOnAHarmonic":
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
class ResultsForResponseOfANodeOnAHarmonic(_0.APIBase):
    """ResultsForResponseOfANodeOnAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_RESPONSE_OF_A_NODE_ON_A_HARMONIC

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_magnitude(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularMagnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_magnitude(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearMagnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_angular_magnitude(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialAngularMagnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def radial_magnitude(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialMagnitude")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def result_at_reference_speed(
        self: "Self",
    ) -> "_6162.DataPointForResponseOfANodeAtAFrequencyToAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.DataPointForResponseOfANodeAtAFrequencyToAHarmonic

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
    def theta_x(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThetaX")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def theta_y(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThetaY")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def theta_z(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThetaZ")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def x(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "X")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def y(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Y")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def z(
        self: "Self",
    ) -> "_6181.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForSingleDegreeOfFreedomOfResponseOfNodeInHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Z")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def data_points(
        self: "Self",
    ) -> "List[_6162.DataPointForResponseOfANodeAtAFrequencyToAHarmonic]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.DataPointForResponseOfANodeAtAFrequencyToAHarmonic]

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
    def cast_to(self: "Self") -> "_Cast_ResultsForResponseOfANodeOnAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_ResultsForResponseOfANodeOnAHarmonic
        """
        return _Cast_ResultsForResponseOfANodeOnAHarmonic(self)

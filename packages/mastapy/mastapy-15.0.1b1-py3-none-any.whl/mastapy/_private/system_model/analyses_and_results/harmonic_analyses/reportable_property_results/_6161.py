"""DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic"""

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

_DATA_POINT_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_AT_A_FREQUENCY_TO_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar(
        "Self", bound="DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic._Cast_DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic:
    """Special nested class for casting DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic to subclasses."""

    __parent__: "DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic"

    @property
    def data_point_for_response_of_a_component_or_surface_at_a_frequency_to_a_harmonic(
        self: "CastSelf",
    ) -> "DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic":
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
class DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic(_0.APIBase):
    """DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _DATA_POINT_FOR_RESPONSE_OF_A_COMPONENT_OR_SURFACE_AT_A_FREQUENCY_TO_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def frequency(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Frequency")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def response(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Response")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic
        """
        return _Cast_DataPointForResponseOfAComponentOrSurfaceAtAFrequencyToAHarmonic(
            self
        )

"""DataPointForResponseOfANodeAtAFrequencyToAHarmonic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.math_utility import _1704

_DATA_POINT_FOR_RESPONSE_OF_A_NODE_AT_A_FREQUENCY_TO_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "DataPointForResponseOfANodeAtAFrequencyToAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1689

    Self = TypeVar("Self", bound="DataPointForResponseOfANodeAtAFrequencyToAHarmonic")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DataPointForResponseOfANodeAtAFrequencyToAHarmonic._Cast_DataPointForResponseOfANodeAtAFrequencyToAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DataPointForResponseOfANodeAtAFrequencyToAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DataPointForResponseOfANodeAtAFrequencyToAHarmonic:
    """Special nested class for casting DataPointForResponseOfANodeAtAFrequencyToAHarmonic to subclasses."""

    __parent__: "DataPointForResponseOfANodeAtAFrequencyToAHarmonic"

    @property
    def data_point_for_response_of_a_node_at_a_frequency_to_a_harmonic(
        self: "CastSelf",
    ) -> "DataPointForResponseOfANodeAtAFrequencyToAHarmonic":
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
class DataPointForResponseOfANodeAtAFrequencyToAHarmonic(_0.APIBase):
    """DataPointForResponseOfANodeAtAFrequencyToAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _DATA_POINT_FOR_RESPONSE_OF_A_NODE_AT_A_FREQUENCY_TO_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularMagnitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angular_radial_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularRadialMagnitude")

        if temp is None:
            return 0.0

        return temp

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
    def linear_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearMagnitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialMagnitude")

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
    def theta_x(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThetaX")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def theta_y(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThetaY")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def theta_z(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThetaZ")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def x(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "X")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def y(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Y")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def z(self: "Self") -> "complex":
        """complex

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Z")

        if temp is None:
            return None

        value = conversion.pn_to_mp_complex(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def get_scalar_result(
        self: "Self",
        scalar_result: "_1689.DynamicsResponseScalarResult",
        complex_magnitude_method: "_1704.ComplexMagnitudeMethod" = _1704.ComplexMagnitudeMethod.PEAK_AMPLITUDE,
    ) -> "complex":
        """complex

        Args:
            scalar_result (mastapy.math_utility.DynamicsResponseScalarResult)
            complex_magnitude_method (mastapy.math_utility.ComplexMagnitudeMethod, optional)
        """
        scalar_result = conversion.mp_to_pn_enum(
            scalar_result, "SMT.MastaAPI.MathUtility.DynamicsResponseScalarResult"
        )
        complex_magnitude_method = conversion.mp_to_pn_enum(
            complex_magnitude_method, "SMT.MastaAPI.MathUtility.ComplexMagnitudeMethod"
        )
        return conversion.pn_to_mp_complex(
            pythonnet_method_call(
                self.wrapped, "GetScalarResult", scalar_result, complex_magnitude_method
            )
        )

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_DataPointForResponseOfANodeAtAFrequencyToAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_DataPointForResponseOfANodeAtAFrequencyToAHarmonic
        """
        return _Cast_DataPointForResponseOfANodeAtAFrequencyToAHarmonic(self)

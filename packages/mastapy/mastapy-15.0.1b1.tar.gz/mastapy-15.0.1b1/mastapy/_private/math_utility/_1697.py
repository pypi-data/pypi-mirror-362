"""FourierSeries"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FOURIER_SERIES = python_net_import("SMT.MastaAPI.MathUtility", "FourierSeries")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.math_utility import _1700

    Self = TypeVar("Self", bound="FourierSeries")
    CastSelf = TypeVar("CastSelf", bound="FourierSeries._Cast_FourierSeries")


__docformat__ = "restructuredtext en"
__all__ = ("FourierSeries",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FourierSeries:
    """Special nested class for casting FourierSeries to subclasses."""

    __parent__: "FourierSeries"

    @property
    def fourier_series(self: "CastSelf") -> "FourierSeries":
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
class FourierSeries(_0.APIBase):
    """FourierSeries

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FOURIER_SERIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def mean_value(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanValue")

        if temp is None:
            return 0.0

        return temp

    @mean_value.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_value(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanValue", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def values(self: "Self") -> "List[float]":
        """List[float]"""
        temp = pythonnet_property_get(self.wrapped, "Values")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @values.setter
    @exception_bridge
    @enforce_parameter_types
    def values(self: "Self", value: "List[float]") -> None:
        value = conversion.mp_to_pn_objects_in_list(value)
        pythonnet_property_set(self.wrapped, "Values", value)

    @exception_bridge
    @enforce_parameter_types
    def harmonic(self: "Self", index: "int") -> "_1700.HarmonicValue":
        """mastapy.math_utility.HarmonicValue

        Args:
            index (int)
        """
        index = int(index)
        method_result = pythonnet_method_call(
            self.wrapped, "Harmonic", index if index else 0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def harmonics_above_cut_off(self: "Self") -> "List[_1700.HarmonicValue]":
        """List[mastapy.math_utility.HarmonicValue]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "HarmonicsAboveCutOff")
        )

    @exception_bridge
    def harmonics_with_zeros_truncated(self: "Self") -> "List[_1700.HarmonicValue]":
        """List[mastapy.math_utility.HarmonicValue]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "HarmonicsWithZerosTruncated")
        )

    @exception_bridge
    def peak_to_peak(self: "Self") -> "float":
        """float"""
        method_result = pythonnet_method_call(self.wrapped, "PeakToPeak")
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def set_amplitude(self: "Self", harmonic: "int", amplitude: "float") -> None:
        """Method does not return.

        Args:
            harmonic (int)
            amplitude (float)
        """
        harmonic = int(harmonic)
        amplitude = float(amplitude)
        pythonnet_method_call(
            self.wrapped,
            "SetAmplitude",
            harmonic if harmonic else 0,
            amplitude if amplitude else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_amplitude_and_phase(
        self: "Self", harmonic: "int", complex_: "complex"
    ) -> None:
        """Method does not return.

        Args:
            harmonic (int)
            complex_ (complex)
        """
        harmonic = int(harmonic)
        complex_ = conversion.mp_to_pn_complex(complex_)
        pythonnet_method_call(
            self.wrapped, "SetAmplitudeAndPhase", harmonic if harmonic else 0, complex_
        )

    @exception_bridge
    @enforce_parameter_types
    def set_phase(self: "Self", harmonic: "int", phase: "float") -> None:
        """Method does not return.

        Args:
            harmonic (int)
            phase (float)
        """
        harmonic = int(harmonic)
        phase = float(phase)
        pythonnet_method_call(
            self.wrapped,
            "SetPhase",
            harmonic if harmonic else 0,
            phase if phase else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_FourierSeries":
        """Cast to another type.

        Returns:
            _Cast_FourierSeries
        """
        return _Cast_FourierSeries(self)

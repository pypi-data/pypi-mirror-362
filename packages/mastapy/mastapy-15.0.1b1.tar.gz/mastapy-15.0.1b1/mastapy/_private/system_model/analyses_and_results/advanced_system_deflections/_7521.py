"""TransmissionErrorToOtherPowerLoad"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TRANSMISSION_ERROR_TO_OTHER_POWER_LOAD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "TransmissionErrorToOtherPowerLoad",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1697

    Self = TypeVar("Self", bound="TransmissionErrorToOtherPowerLoad")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TransmissionErrorToOtherPowerLoad._Cast_TransmissionErrorToOtherPowerLoad",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransmissionErrorToOtherPowerLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransmissionErrorToOtherPowerLoad:
    """Special nested class for casting TransmissionErrorToOtherPowerLoad to subclasses."""

    __parent__: "TransmissionErrorToOtherPowerLoad"

    @property
    def transmission_error_to_other_power_load(
        self: "CastSelf",
    ) -> "TransmissionErrorToOtherPowerLoad":
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
class TransmissionErrorToOtherPowerLoad(_0.APIBase):
    """TransmissionErrorToOtherPowerLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSMISSION_ERROR_TO_OTHER_POWER_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mean_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanTE")

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
    def peak_to_peak_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fourier_series_of_te(self: "Self") -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FourierSeriesOfTE")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_TransmissionErrorToOtherPowerLoad":
        """Cast to another type.

        Returns:
            _Cast_TransmissionErrorToOtherPowerLoad
        """
        return _Cast_TransmissionErrorToOtherPowerLoad(self)

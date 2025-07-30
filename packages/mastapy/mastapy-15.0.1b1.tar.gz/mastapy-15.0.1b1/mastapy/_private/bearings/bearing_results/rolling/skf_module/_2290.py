"""Frequencies"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling.skf_module import _2305

_FREQUENCIES = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "Frequencies"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import (
        _2291,
        _2303,
    )

    Self = TypeVar("Self", bound="Frequencies")
    CastSelf = TypeVar("CastSelf", bound="Frequencies._Cast_Frequencies")


__docformat__ = "restructuredtext en"
__all__ = ("Frequencies",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Frequencies:
    """Special nested class for casting Frequencies to subclasses."""

    __parent__: "Frequencies"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def frequencies(self: "CastSelf") -> "Frequencies":
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
class Frequencies(_2305.SKFCalculationResult):
    """Frequencies

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FREQUENCIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def frequency_of_over_rolling(self: "Self") -> "_2291.FrequencyOfOverRolling":
        """mastapy.bearings.bearing_results.rolling.skf_module.FrequencyOfOverRolling

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOfOverRolling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotational_frequency(self: "Self") -> "_2303.RotationalFrequency":
        """mastapy.bearings.bearing_results.rolling.skf_module.RotationalFrequency

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotationalFrequency")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Frequencies":
        """Cast to another type.

        Returns:
            _Cast_Frequencies
        """
        return _Cast_Frequencies(self)

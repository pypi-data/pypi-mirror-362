"""AdjustedSpeed"""

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

_ADJUSTED_SPEED = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "AdjustedSpeed"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import _2286

    Self = TypeVar("Self", bound="AdjustedSpeed")
    CastSelf = TypeVar("CastSelf", bound="AdjustedSpeed._Cast_AdjustedSpeed")


__docformat__ = "restructuredtext en"
__all__ = ("AdjustedSpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdjustedSpeed:
    """Special nested class for casting AdjustedSpeed to subclasses."""

    __parent__: "AdjustedSpeed"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def adjusted_speed(self: "CastSelf") -> "AdjustedSpeed":
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
class AdjustedSpeed(_2305.SKFCalculationResult):
    """AdjustedSpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADJUSTED_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adjusted_reference_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def adjustment_factors(self: "Self") -> "_2286.AdjustmentFactors":
        """mastapy.bearings.bearing_results.rolling.skf_module.AdjustmentFactors

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustmentFactors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_AdjustedSpeed":
        """Cast to another type.

        Returns:
            _Cast_AdjustedSpeed
        """
        return _Cast_AdjustedSpeed(self)

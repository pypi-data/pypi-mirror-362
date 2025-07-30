"""OilSealLossCalculationParameters"""

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

_OIL_SEAL_LOSS_CALCULATION_PARAMETERS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "OilSealLossCalculationParameters"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import _7797

    Self = TypeVar("Self", bound="OilSealLossCalculationParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OilSealLossCalculationParameters._Cast_OilSealLossCalculationParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OilSealLossCalculationParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OilSealLossCalculationParameters:
    """Special nested class for casting OilSealLossCalculationParameters to subclasses."""

    __parent__: "OilSealLossCalculationParameters"

    @property
    def oil_seal_loss_calculation_parameters(
        self: "CastSelf",
    ) -> "OilSealLossCalculationParameters":
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
class OilSealLossCalculationParameters(_0.APIBase):
    """OilSealLossCalculationParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OIL_SEAL_LOSS_CALCULATION_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def oil_sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def signed_relative_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedRelativeSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_seal_load_case(self: "Self") -> "_7797.OilSealLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilSealLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_OilSealLossCalculationParameters":
        """Cast to another type.

        Returns:
            _Cast_OilSealLossCalculationParameters
        """
        return _Cast_OilSealLossCalculationParameters(self)

"""ClutchLossCalculationParameters"""

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

_CLUTCH_LOSS_CALCULATION_PARAMETERS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "ClutchLossCalculationParameters"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.static_loads import _7703
    from mastapy._private.system_model.part_model.couplings import _2818

    Self = TypeVar("Self", bound="ClutchLossCalculationParameters")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ClutchLossCalculationParameters._Cast_ClutchLossCalculationParameters",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ClutchLossCalculationParameters",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ClutchLossCalculationParameters:
    """Special nested class for casting ClutchLossCalculationParameters to subclasses."""

    __parent__: "ClutchLossCalculationParameters"

    @property
    def clutch_loss_calculation_parameters(
        self: "CastSelf",
    ) -> "ClutchLossCalculationParameters":
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
class ClutchLossCalculationParameters(_0.APIBase):
    """ClutchLossCalculationParameters

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CLUTCH_LOSS_CALCULATION_PARAMETERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def dynamic_viscosity_of_air_oil_mist(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosityOfAirOilMist")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_viscosity_of_oil(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosityOfOil")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def is_clutch_engaged(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsClutchEngaged")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def oil_density(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OilDensity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def signed_angular_speed_of_clutch_half_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedAngularSpeedOfClutchHalfA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def signed_angular_speed_of_clutch_half_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedAngularSpeedOfClutchHalfB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clutch_half_a(self: "Self") -> "_2818.ClutchHalf":
        """mastapy.system_model.part_model.couplings.ClutchHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchHalfA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def clutch_half_b(self: "Self") -> "_2818.ClutchHalf":
        """mastapy.system_model.part_model.couplings.ClutchHalf

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchHalfB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def clutch_load_case(self: "Self") -> "_7703.ClutchLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClutchLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ClutchLossCalculationParameters":
        """Cast to another type.

        Returns:
            _Cast_ClutchLossCalculationParameters
        """
        return _Cast_ClutchLossCalculationParameters(self)

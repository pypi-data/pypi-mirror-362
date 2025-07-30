"""GreaseLifeAndRelubricationInterval"""

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

_GREASE_LIFE_AND_RELUBRICATION_INTERVAL = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule",
    "GreaseLifeAndRelubricationInterval",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling.skf_module import (
        _2295,
        _2297,
        _2298,
    )

    Self = TypeVar("Self", bound="GreaseLifeAndRelubricationInterval")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GreaseLifeAndRelubricationInterval._Cast_GreaseLifeAndRelubricationInterval",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GreaseLifeAndRelubricationInterval",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GreaseLifeAndRelubricationInterval:
    """Special nested class for casting GreaseLifeAndRelubricationInterval to subclasses."""

    __parent__: "GreaseLifeAndRelubricationInterval"

    @property
    def skf_calculation_result(self: "CastSelf") -> "_2305.SKFCalculationResult":
        return self.__parent__._cast(_2305.SKFCalculationResult)

    @property
    def grease_life_and_relubrication_interval(
        self: "CastSelf",
    ) -> "GreaseLifeAndRelubricationInterval":
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
class GreaseLifeAndRelubricationInterval(_2305.SKFCalculationResult):
    """GreaseLifeAndRelubricationInterval

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GREASE_LIFE_AND_RELUBRICATION_INTERVAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def speed_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def grease(self: "Self") -> "_2295.Grease":
        """mastapy.bearings.bearing_results.rolling.skf_module.Grease

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Grease")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def grease_quantity(self: "Self") -> "_2297.GreaseQuantity":
        """mastapy.bearings.bearing_results.rolling.skf_module.GreaseQuantity

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GreaseQuantity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def initial_fill(self: "Self") -> "_2298.InitialFill":
        """mastapy.bearings.bearing_results.rolling.skf_module.InitialFill

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InitialFill")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GreaseLifeAndRelubricationInterval":
        """Cast to another type.

        Returns:
            _Cast_GreaseLifeAndRelubricationInterval
        """
        return _Cast_GreaseLifeAndRelubricationInterval(self)

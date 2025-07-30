"""PowerLoss"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_POWER_LOSS = python_net_import("SMT.MastaAPI.Materials.Efficiency", "PowerLoss")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials.efficiency import _384, _386

    Self = TypeVar("Self", bound="PowerLoss")
    CastSelf = TypeVar("CastSelf", bound="PowerLoss._Cast_PowerLoss")


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoss",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PowerLoss:
    """Special nested class for casting PowerLoss to subclasses."""

    __parent__: "PowerLoss"

    @property
    def independent_power_loss(self: "CastSelf") -> "_384.IndependentPowerLoss":
        from mastapy._private.materials.efficiency import _384

        return self.__parent__._cast(_384.IndependentPowerLoss)

    @property
    def load_and_speed_combined_power_loss(
        self: "CastSelf",
    ) -> "_386.LoadAndSpeedCombinedPowerLoss":
        from mastapy._private.materials.efficiency import _386

        return self.__parent__._cast(_386.LoadAndSpeedCombinedPowerLoss)

    @property
    def power_loss(self: "CastSelf") -> "PowerLoss":
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
class PowerLoss(_0.APIBase):
    """PowerLoss

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _POWER_LOSS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def power_loss_calculation_details(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossCalculationDetails")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def total_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PowerLoss":
        """Cast to another type.

        Returns:
            _Cast_PowerLoss
        """
        return _Cast_PowerLoss(self)

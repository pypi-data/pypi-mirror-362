"""LoadAndSpeedCombinedPowerLoss"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials.efficiency import _391

_LOAD_AND_SPEED_COMBINED_POWER_LOSS = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "LoadAndSpeedCombinedPowerLoss"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadAndSpeedCombinedPowerLoss")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadAndSpeedCombinedPowerLoss._Cast_LoadAndSpeedCombinedPowerLoss",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadAndSpeedCombinedPowerLoss",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadAndSpeedCombinedPowerLoss:
    """Special nested class for casting LoadAndSpeedCombinedPowerLoss to subclasses."""

    __parent__: "LoadAndSpeedCombinedPowerLoss"

    @property
    def power_loss(self: "CastSelf") -> "_391.PowerLoss":
        return self.__parent__._cast(_391.PowerLoss)

    @property
    def load_and_speed_combined_power_loss(
        self: "CastSelf",
    ) -> "LoadAndSpeedCombinedPowerLoss":
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
class LoadAndSpeedCombinedPowerLoss(_391.PowerLoss):
    """LoadAndSpeedCombinedPowerLoss

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOAD_AND_SPEED_COMBINED_POWER_LOSS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadAndSpeedCombinedPowerLoss":
        """Cast to another type.

        Returns:
            _Cast_LoadAndSpeedCombinedPowerLoss
        """
        return _Cast_LoadAndSpeedCombinedPowerLoss(self)

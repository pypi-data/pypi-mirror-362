"""IndependentPowerLoss"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.materials.efficiency import _391

_INDEPENDENT_POWER_LOSS = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "IndependentPowerLoss"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IndependentPowerLoss")
    CastSelf = TypeVar(
        "CastSelf", bound="IndependentPowerLoss._Cast_IndependentPowerLoss"
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndependentPowerLoss",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_IndependentPowerLoss:
    """Special nested class for casting IndependentPowerLoss to subclasses."""

    __parent__: "IndependentPowerLoss"

    @property
    def power_loss(self: "CastSelf") -> "_391.PowerLoss":
        return self.__parent__._cast(_391.PowerLoss)

    @property
    def independent_power_loss(self: "CastSelf") -> "IndependentPowerLoss":
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
class IndependentPowerLoss(_391.PowerLoss):
    """IndependentPowerLoss

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INDEPENDENT_POWER_LOSS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def load_dependent_power_loss(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LoadDependentPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @load_dependent_power_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def load_dependent_power_loss(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadDependentPowerLoss",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def speed_dependent_power_loss(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpeedDependentPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @speed_dependent_power_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_dependent_power_loss(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpeedDependentPowerLoss",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_IndependentPowerLoss":
        """Cast to another type.

        Returns:
            _Cast_IndependentPowerLoss
        """
        return _Cast_IndependentPowerLoss(self)

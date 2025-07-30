"""TorqueConverterSpeedRatio"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_TORQUE_CONVERTER_SPEED_RATIO = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "TorqueConverterSpeedRatio"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TorqueConverterSpeedRatio")
    CastSelf = TypeVar(
        "CastSelf", bound="TorqueConverterSpeedRatio._Cast_TorqueConverterSpeedRatio"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TorqueConverterSpeedRatio",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TorqueConverterSpeedRatio:
    """Special nested class for casting TorqueConverterSpeedRatio to subclasses."""

    __parent__: "TorqueConverterSpeedRatio"

    @property
    def torque_converter_speed_ratio(self: "CastSelf") -> "TorqueConverterSpeedRatio":
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
class TorqueConverterSpeedRatio(_0.APIBase):
    """TorqueConverterSpeedRatio

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TORQUE_CONVERTER_SPEED_RATIO

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inverse_k(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InverseK")

        if temp is None:
            return 0.0

        return temp

    @inverse_k.setter
    @exception_bridge
    @enforce_parameter_types
    def inverse_k(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InverseK", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def speed_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpeedRatio")

        if temp is None:
            return 0.0

        return temp

    @speed_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def speed_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SpeedRatio", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def torque_ratio(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorqueRatio")

        if temp is None:
            return 0.0

        return temp

    @torque_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_ratio(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TorqueRatio", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TorqueConverterSpeedRatio":
        """Cast to another type.

        Returns:
            _Cast_TorqueConverterSpeedRatio
        """
        return _Cast_TorqueConverterSpeedRatio(self)

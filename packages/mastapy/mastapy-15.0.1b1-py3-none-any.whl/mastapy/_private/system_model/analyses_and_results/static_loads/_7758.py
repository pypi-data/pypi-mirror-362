"""ForceAndTorqueScalingFactor"""

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

_FORCE_AND_TORQUE_SCALING_FACTOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ForceAndTorqueScalingFactor",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ForceAndTorqueScalingFactor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ForceAndTorqueScalingFactor._Cast_ForceAndTorqueScalingFactor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ForceAndTorqueScalingFactor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ForceAndTorqueScalingFactor:
    """Special nested class for casting ForceAndTorqueScalingFactor to subclasses."""

    __parent__: "ForceAndTorqueScalingFactor"

    @property
    def force_and_torque_scaling_factor(
        self: "CastSelf",
    ) -> "ForceAndTorqueScalingFactor":
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
class ForceAndTorqueScalingFactor(_0.APIBase):
    """ForceAndTorqueScalingFactor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FORCE_AND_TORQUE_SCALING_FACTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def force_scaling_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ForceScalingFactor")

        if temp is None:
            return 0.0

        return temp

    @force_scaling_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def force_scaling_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ForceScalingFactor",
            float(value) if value is not None else 0.0,
        )

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
    def speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_scaling_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TorqueScalingFactor")

        if temp is None:
            return 0.0

        return temp

    @torque_scaling_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def torque_scaling_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TorqueScalingFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ForceAndTorqueScalingFactor":
        """Cast to another type.

        Returns:
            _Cast_ForceAndTorqueScalingFactor
        """
        return _Cast_ForceAndTorqueScalingFactor(self)

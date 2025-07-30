"""EngineSpeed"""

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

_ENGINE_SPEED = python_net_import("SMT.MastaAPI.SystemModel.PartModel", "EngineSpeed")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EngineSpeed")
    CastSelf = TypeVar("CastSelf", bound="EngineSpeed._Cast_EngineSpeed")


__docformat__ = "restructuredtext en"
__all__ = ("EngineSpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EngineSpeed:
    """Special nested class for casting EngineSpeed to subclasses."""

    __parent__: "EngineSpeed"

    @property
    def engine_speed(self: "CastSelf") -> "EngineSpeed":
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
class EngineSpeed(_0.APIBase):
    """EngineSpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ENGINE_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def can_do_efficiency(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CanDoEfficiency")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def number_of_part_loads(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPartLoads")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_part_torques(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPartTorques")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def part_loads_dummy(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartLoadsDummy")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def torque(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Torque")

        if temp is None:
            return 0.0

        return temp

    @torque.setter
    @exception_bridge
    @enforce_parameter_types
    def torque(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Torque", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_EngineSpeed":
        """Cast to another type.

        Returns:
            _Cast_EngineSpeed
        """
        return _Cast_EngineSpeed(self)

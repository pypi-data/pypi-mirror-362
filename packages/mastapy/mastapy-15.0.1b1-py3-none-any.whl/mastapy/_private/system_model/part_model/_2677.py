"""EnginePartLoad"""

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

_ENGINE_PART_LOAD = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "EnginePartLoad"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="EnginePartLoad")
    CastSelf = TypeVar("CastSelf", bound="EnginePartLoad._Cast_EnginePartLoad")


__docformat__ = "restructuredtext en"
__all__ = ("EnginePartLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_EnginePartLoad:
    """Special nested class for casting EnginePartLoad to subclasses."""

    __parent__: "EnginePartLoad"

    @property
    def engine_part_load(self: "CastSelf") -> "EnginePartLoad":
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
class EnginePartLoad(_0.APIBase):
    """EnginePartLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ENGINE_PART_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def consumption(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Consumption")

        if temp is None:
            return 0.0

        return temp

    @consumption.setter
    @exception_bridge
    @enforce_parameter_types
    def consumption(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Consumption", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def throttle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Throttle")

        if temp is None:
            return 0.0

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
    def cast_to(self: "Self") -> "_Cast_EnginePartLoad":
        """Cast to another type.

        Returns:
            _Cast_EnginePartLoad
        """
        return _Cast_EnginePartLoad(self)

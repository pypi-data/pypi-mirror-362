"""Wheel"""

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

_WHEEL = python_net_import("SMT.MastaAPI.Gears.Manufacturing.Bevel", "Wheel")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.bevel.basic_machine_settings import _924
    from mastapy._private.gears.manufacturing.bevel.cutters import _918

    Self = TypeVar("Self", bound="Wheel")
    CastSelf = TypeVar("CastSelf", bound="Wheel._Cast_Wheel")


__docformat__ = "restructuredtext en"
__all__ = ("Wheel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Wheel:
    """Special nested class for casting Wheel to subclasses."""

    __parent__: "Wheel"

    @property
    def wheel(self: "CastSelf") -> "Wheel":
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
class Wheel(_0.APIBase):
    """Wheel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WHEEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def basic_conical_gear_machine_settings(
        self: "Self",
    ) -> "_924.BasicConicalGearMachineSettings":
        """mastapy.gears.manufacturing.bevel.basic_machine_settings.BasicConicalGearMachineSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicConicalGearMachineSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def wheel_finish_cutter(self: "Self") -> "_918.WheelFinishCutter":
        """mastapy.gears.manufacturing.bevel.cutters.WheelFinishCutter

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelFinishCutter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_Wheel":
        """Cast to another type.

        Returns:
            _Cast_Wheel
        """
        return _Cast_Wheel(self)

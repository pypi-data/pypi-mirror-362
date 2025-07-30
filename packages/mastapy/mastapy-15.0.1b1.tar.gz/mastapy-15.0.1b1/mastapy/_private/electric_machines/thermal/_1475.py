"""RotorSetup"""

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
from mastapy._private.electric_machines.thermal import _1462

_ROTOR_SETUP = python_net_import("SMT.MastaAPI.ElectricMachines.Thermal", "RotorSetup")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines.thermal import _1465

    Self = TypeVar("Self", bound="RotorSetup")
    CastSelf = TypeVar("CastSelf", bound="RotorSetup._Cast_RotorSetup")


__docformat__ = "restructuredtext en"
__all__ = ("RotorSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorSetup:
    """Special nested class for casting RotorSetup to subclasses."""

    __parent__: "RotorSetup"

    @property
    def component_setup(self: "CastSelf") -> "_1462.ComponentSetup":
        return self.__parent__._cast(_1462.ComponentSetup)

    @property
    def rotor_setup(self: "CastSelf") -> "RotorSetup":
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
class RotorSetup(_1462.ComponentSetup):
    """RotorSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def inner_boundary_edge_selector(self: "Self") -> "_1465.EdgeSelector":
        """mastapy.electric_machines.thermal.EdgeSelector

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerBoundaryEdgeSelector")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RotorSetup":
        """Cast to another type.

        Returns:
            _Cast_RotorSetup
        """
        return _Cast_RotorSetup(self)

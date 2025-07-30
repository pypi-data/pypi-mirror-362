"""MAAElectricMachineGroup"""

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

_MAA_ELECTRIC_MACHINE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel", "MAAElectricMachineGroup"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1390

    Self = TypeVar("Self", bound="MAAElectricMachineGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="MAAElectricMachineGroup._Cast_MAAElectricMachineGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MAAElectricMachineGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MAAElectricMachineGroup:
    """Special nested class for casting MAAElectricMachineGroup to subclasses."""

    __parent__: "MAAElectricMachineGroup"

    @property
    def maa_electric_machine_group(self: "CastSelf") -> "MAAElectricMachineGroup":
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
class MAAElectricMachineGroup(_0.APIBase):
    """MAAElectricMachineGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MAA_ELECTRIC_MACHINE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def electric_machine_group(self: "Self") -> "_1390.ElectricMachineGroup":
        """mastapy.electric_machines.ElectricMachineGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricMachineGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MAAElectricMachineGroup":
        """Cast to another type.

        Returns:
            _Cast_MAAElectricMachineGroup
        """
        return _Cast_MAAElectricMachineGroup(self)

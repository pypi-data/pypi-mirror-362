"""StatorSetup"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.electric_machines.thermal import _1462

_STATOR_SETUP = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "StatorSetup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.electric_machines.thermal import _1489

    Self = TypeVar("Self", bound="StatorSetup")
    CastSelf = TypeVar("CastSelf", bound="StatorSetup._Cast_StatorSetup")


__docformat__ = "restructuredtext en"
__all__ = ("StatorSetup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatorSetup:
    """Special nested class for casting StatorSetup to subclasses."""

    __parent__: "StatorSetup"

    @property
    def component_setup(self: "CastSelf") -> "_1462.ComponentSetup":
        return self.__parent__._cast(_1462.ComponentSetup)

    @property
    def stator_setup(self: "CastSelf") -> "StatorSetup":
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
class StatorSetup(_1462.ComponentSetup):
    """StatorSetup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATOR_SETUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def user_specified_edge_indices(
        self: "Self",
    ) -> "List[_1489.UserSpecifiedEdgeIndices]":
        """List[mastapy.electric_machines.thermal.UserSpecifiedEdgeIndices]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedEdgeIndices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_StatorSetup":
        """Cast to another type.

        Returns:
            _Cast_StatorSetup
        """
        return _Cast_StatorSetup(self)

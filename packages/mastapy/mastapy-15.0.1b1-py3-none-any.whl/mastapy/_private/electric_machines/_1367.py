"""CADConductor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.electric_machines import _1450

_CAD_CONDUCTOR = python_net_import("SMT.MastaAPI.ElectricMachines", "CADConductor")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CADConductor")
    CastSelf = TypeVar("CastSelf", bound="CADConductor._Cast_CADConductor")


__docformat__ = "restructuredtext en"
__all__ = ("CADConductor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CADConductor:
    """Special nested class for casting CADConductor to subclasses."""

    __parent__: "CADConductor"

    @property
    def winding_conductor(self: "CastSelf") -> "_1450.WindingConductor":
        return self.__parent__._cast(_1450.WindingConductor)

    @property
    def cad_conductor(self: "CastSelf") -> "CADConductor":
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
class CADConductor(_1450.WindingConductor):
    """CADConductor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CAD_CONDUCTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CADConductor":
        """Cast to another type.

        Returns:
            _Cast_CADConductor
        """
        return _Cast_CADConductor(self)

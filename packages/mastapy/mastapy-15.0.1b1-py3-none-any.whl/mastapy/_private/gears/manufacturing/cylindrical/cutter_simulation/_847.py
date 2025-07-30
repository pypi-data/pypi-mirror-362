"""RoughCutterSimulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation import _842

_ROUGH_CUTTER_SIMULATION = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.CutterSimulation",
    "RoughCutterSimulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RoughCutterSimulation")
    CastSelf = TypeVar(
        "CastSelf", bound="RoughCutterSimulation._Cast_RoughCutterSimulation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RoughCutterSimulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RoughCutterSimulation:
    """Special nested class for casting RoughCutterSimulation to subclasses."""

    __parent__: "RoughCutterSimulation"

    @property
    def gear_cutter_simulation(self: "CastSelf") -> "_842.GearCutterSimulation":
        return self.__parent__._cast(_842.GearCutterSimulation)

    @property
    def rough_cutter_simulation(self: "CastSelf") -> "RoughCutterSimulation":
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
class RoughCutterSimulation(_842.GearCutterSimulation):
    """RoughCutterSimulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROUGH_CUTTER_SIMULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RoughCutterSimulation":
        """Cast to another type.

        Returns:
            _Cast_RoughCutterSimulation
        """
        return _Cast_RoughCutterSimulation(self)

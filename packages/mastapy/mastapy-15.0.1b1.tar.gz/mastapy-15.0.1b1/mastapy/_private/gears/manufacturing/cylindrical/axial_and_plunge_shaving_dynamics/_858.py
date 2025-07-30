"""PlungeShaverDynamics"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _868,
)

_PLUNGE_SHAVER_DYNAMICS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "PlungeShaverDynamics",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlungeShaverDynamics")
    CastSelf = TypeVar(
        "CastSelf", bound="PlungeShaverDynamics._Cast_PlungeShaverDynamics"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShaverDynamics",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShaverDynamics:
    """Special nested class for casting PlungeShaverDynamics to subclasses."""

    __parent__: "PlungeShaverDynamics"

    @property
    def shaving_dynamics(self: "CastSelf") -> "_868.ShavingDynamics":
        return self.__parent__._cast(_868.ShavingDynamics)

    @property
    def plunge_shaver_dynamics(self: "CastSelf") -> "PlungeShaverDynamics":
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
class PlungeShaverDynamics(_868.ShavingDynamics):
    """PlungeShaverDynamics

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVER_DYNAMICS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def number_of_gear_teeth_passed_per_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfGearTeethPassedPerFlank")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PlungeShaverDynamics":
        """Cast to another type.

        Returns:
            _Cast_PlungeShaverDynamics
        """
        return _Cast_PlungeShaverDynamics(self)

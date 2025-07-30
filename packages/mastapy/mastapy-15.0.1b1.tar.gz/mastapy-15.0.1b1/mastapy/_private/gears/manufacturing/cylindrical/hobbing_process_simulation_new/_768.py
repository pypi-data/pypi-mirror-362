"""GearMountingError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _782,
)

_GEAR_MOUNTING_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "GearMountingError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMountingError")
    CastSelf = TypeVar("CastSelf", bound="GearMountingError._Cast_GearMountingError")


__docformat__ = "restructuredtext en"
__all__ = ("GearMountingError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMountingError:
    """Special nested class for casting GearMountingError to subclasses."""

    __parent__: "GearMountingError"

    @property
    def mounting_error(self: "CastSelf") -> "_782.MountingError":
        return self.__parent__._cast(_782.MountingError)

    @property
    def gear_mounting_error(self: "CastSelf") -> "GearMountingError":
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
class GearMountingError(_782.MountingError):
    """GearMountingError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MOUNTING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMountingError":
        """Cast to another type.

        Returns:
            _Cast_GearMountingError
        """
        return _Cast_GearMountingError(self)

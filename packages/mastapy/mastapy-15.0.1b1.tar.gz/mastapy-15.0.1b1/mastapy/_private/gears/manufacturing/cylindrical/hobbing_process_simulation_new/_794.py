"""WormGrinderManufactureError"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _792,
)

_WORM_GRINDER_MANUFACTURE_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "WormGrinderManufactureError",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WormGrinderManufactureError")
    CastSelf = TypeVar(
        "CastSelf",
        bound="WormGrinderManufactureError._Cast_WormGrinderManufactureError",
    )


__docformat__ = "restructuredtext en"
__all__ = ("WormGrinderManufactureError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGrinderManufactureError:
    """Special nested class for casting WormGrinderManufactureError to subclasses."""

    __parent__: "WormGrinderManufactureError"

    @property
    def rack_manufacture_error(self: "CastSelf") -> "_792.RackManufactureError":
        return self.__parent__._cast(_792.RackManufactureError)

    @property
    def worm_grinder_manufacture_error(
        self: "CastSelf",
    ) -> "WormGrinderManufactureError":
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
class WormGrinderManufactureError(_792.RackManufactureError):
    """WormGrinderManufactureError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GRINDER_MANUFACTURE_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_WormGrinderManufactureError":
        """Cast to another type.

        Returns:
            _Cast_WormGrinderManufactureError
        """
        return _Cast_WormGrinderManufactureError(self)

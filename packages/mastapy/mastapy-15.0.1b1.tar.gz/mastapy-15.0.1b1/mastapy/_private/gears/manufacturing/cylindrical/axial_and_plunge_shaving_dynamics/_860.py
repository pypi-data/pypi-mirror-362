"""PlungeShaverRedressing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _858,
    _867,
)

_PLUNGE_SHAVER_REDRESSING = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "PlungeShaverRedressing",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlungeShaverRedressing")
    CastSelf = TypeVar(
        "CastSelf", bound="PlungeShaverRedressing._Cast_PlungeShaverRedressing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShaverRedressing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShaverRedressing:
    """Special nested class for casting PlungeShaverRedressing to subclasses."""

    __parent__: "PlungeShaverRedressing"

    @property
    def shaver_redressing(self: "CastSelf") -> "_867.ShaverRedressing":
        return self.__parent__._cast(_867.ShaverRedressing)

    @property
    def plunge_shaver_redressing(self: "CastSelf") -> "PlungeShaverRedressing":
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
class PlungeShaverRedressing(_867.ShaverRedressing[_858.PlungeShaverDynamics]):
    """PlungeShaverRedressing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVER_REDRESSING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_PlungeShaverRedressing":
        """Cast to another type.

        Returns:
            _Cast_PlungeShaverRedressing
        """
        return _Cast_PlungeShaverRedressing(self)

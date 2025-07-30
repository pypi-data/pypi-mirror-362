"""AxialShaverRedressing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics import (
    _854,
    _867,
)

_AXIAL_SHAVER_REDRESSING = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "AxialShaverRedressing",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AxialShaverRedressing")
    CastSelf = TypeVar(
        "CastSelf", bound="AxialShaverRedressing._Cast_AxialShaverRedressing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AxialShaverRedressing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AxialShaverRedressing:
    """Special nested class for casting AxialShaverRedressing to subclasses."""

    __parent__: "AxialShaverRedressing"

    @property
    def shaver_redressing(self: "CastSelf") -> "_867.ShaverRedressing":
        return self.__parent__._cast(_867.ShaverRedressing)

    @property
    def axial_shaver_redressing(self: "CastSelf") -> "AxialShaverRedressing":
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
class AxialShaverRedressing(_867.ShaverRedressing[_854.ConventionalShavingDynamics]):
    """AxialShaverRedressing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AXIAL_SHAVER_REDRESSING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AxialShaverRedressing":
        """Cast to another type.

        Returns:
            _Cast_AxialShaverRedressing
        """
        return _Cast_AxialShaverRedressing(self)

"""FatigueSafetyFactorItemBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _369

_FATIGUE_SAFETY_FACTOR_ITEM_BASE = python_net_import(
    "SMT.MastaAPI.Materials", "FatigueSafetyFactorItemBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _337, _340

    Self = TypeVar("Self", bound="FatigueSafetyFactorItemBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FatigueSafetyFactorItemBase._Cast_FatigueSafetyFactorItemBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FatigueSafetyFactorItemBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FatigueSafetyFactorItemBase:
    """Special nested class for casting FatigueSafetyFactorItemBase to subclasses."""

    __parent__: "FatigueSafetyFactorItemBase"

    @property
    def safety_factor_item(self: "CastSelf") -> "_369.SafetyFactorItem":
        return self.__parent__._cast(_369.SafetyFactorItem)

    @property
    def composite_fatigue_safety_factor_item(
        self: "CastSelf",
    ) -> "_337.CompositeFatigueSafetyFactorItem":
        from mastapy._private.materials import _337

        return self.__parent__._cast(_337.CompositeFatigueSafetyFactorItem)

    @property
    def fatigue_safety_factor_item(self: "CastSelf") -> "_340.FatigueSafetyFactorItem":
        from mastapy._private.materials import _340

        return self.__parent__._cast(_340.FatigueSafetyFactorItem)

    @property
    def fatigue_safety_factor_item_base(
        self: "CastSelf",
    ) -> "FatigueSafetyFactorItemBase":
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
class FatigueSafetyFactorItemBase(_369.SafetyFactorItem):
    """FatigueSafetyFactorItemBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FATIGUE_SAFETY_FACTOR_ITEM_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FatigueSafetyFactorItemBase":
        """Cast to another type.

        Returns:
            _Cast_FatigueSafetyFactorItemBase
        """
        return _Cast_FatigueSafetyFactorItemBase(self)

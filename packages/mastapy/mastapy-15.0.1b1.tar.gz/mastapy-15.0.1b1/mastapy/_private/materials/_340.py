"""FatigueSafetyFactorItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _341

_FATIGUE_SAFETY_FACTOR_ITEM = python_net_import(
    "SMT.MastaAPI.Materials", "FatigueSafetyFactorItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.materials import _337, _369

    Self = TypeVar("Self", bound="FatigueSafetyFactorItem")
    CastSelf = TypeVar(
        "CastSelf", bound="FatigueSafetyFactorItem._Cast_FatigueSafetyFactorItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FatigueSafetyFactorItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FatigueSafetyFactorItem:
    """Special nested class for casting FatigueSafetyFactorItem to subclasses."""

    __parent__: "FatigueSafetyFactorItem"

    @property
    def fatigue_safety_factor_item_base(
        self: "CastSelf",
    ) -> "_341.FatigueSafetyFactorItemBase":
        return self.__parent__._cast(_341.FatigueSafetyFactorItemBase)

    @property
    def safety_factor_item(self: "CastSelf") -> "_369.SafetyFactorItem":
        from mastapy._private.materials import _369

        return self.__parent__._cast(_369.SafetyFactorItem)

    @property
    def composite_fatigue_safety_factor_item(
        self: "CastSelf",
    ) -> "_337.CompositeFatigueSafetyFactorItem":
        from mastapy._private.materials import _337

        return self.__parent__._cast(_337.CompositeFatigueSafetyFactorItem)

    @property
    def fatigue_safety_factor_item(self: "CastSelf") -> "FatigueSafetyFactorItem":
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
class FatigueSafetyFactorItem(_341.FatigueSafetyFactorItemBase):
    """FatigueSafetyFactorItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FATIGUE_SAFETY_FACTOR_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FatigueSafetyFactorItem":
        """Cast to another type.

        Returns:
            _Cast_FatigueSafetyFactorItem
        """
        return _Cast_FatigueSafetyFactorItem(self)

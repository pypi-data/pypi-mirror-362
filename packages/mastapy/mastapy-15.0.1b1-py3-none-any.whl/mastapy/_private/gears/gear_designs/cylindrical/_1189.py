"""StandardRack"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1118

_STANDARD_RACK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "StandardRack"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1116

    Self = TypeVar("Self", bound="StandardRack")
    CastSelf = TypeVar("CastSelf", bound="StandardRack._Cast_StandardRack")


__docformat__ = "restructuredtext en"
__all__ = ("StandardRack",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StandardRack:
    """Special nested class for casting StandardRack to subclasses."""

    __parent__: "StandardRack"

    @property
    def cylindrical_gear_basic_rack(
        self: "CastSelf",
    ) -> "_1118.CylindricalGearBasicRack":
        return self.__parent__._cast(_1118.CylindricalGearBasicRack)

    @property
    def cylindrical_gear_abstract_rack(
        self: "CastSelf",
    ) -> "_1116.CylindricalGearAbstractRack":
        from mastapy._private.gears.gear_designs.cylindrical import _1116

        return self.__parent__._cast(_1116.CylindricalGearAbstractRack)

    @property
    def standard_rack(self: "CastSelf") -> "StandardRack":
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
class StandardRack(_1118.CylindricalGearBasicRack):
    """StandardRack

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STANDARD_RACK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StandardRack":
        """Cast to another type.

        Returns:
            _Cast_StandardRack
        """
        return _Cast_StandardRack(self)

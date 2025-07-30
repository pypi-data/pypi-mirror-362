"""StandardRackFlank"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1119

_STANDARD_RACK_FLANK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "StandardRackFlank"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1117

    Self = TypeVar("Self", bound="StandardRackFlank")
    CastSelf = TypeVar("CastSelf", bound="StandardRackFlank._Cast_StandardRackFlank")


__docformat__ = "restructuredtext en"
__all__ = ("StandardRackFlank",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StandardRackFlank:
    """Special nested class for casting StandardRackFlank to subclasses."""

    __parent__: "StandardRackFlank"

    @property
    def cylindrical_gear_basic_rack_flank(
        self: "CastSelf",
    ) -> "_1119.CylindricalGearBasicRackFlank":
        return self.__parent__._cast(_1119.CylindricalGearBasicRackFlank)

    @property
    def cylindrical_gear_abstract_rack_flank(
        self: "CastSelf",
    ) -> "_1117.CylindricalGearAbstractRackFlank":
        from mastapy._private.gears.gear_designs.cylindrical import _1117

        return self.__parent__._cast(_1117.CylindricalGearAbstractRackFlank)

    @property
    def standard_rack_flank(self: "CastSelf") -> "StandardRackFlank":
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
class StandardRackFlank(_1119.CylindricalGearBasicRackFlank):
    """StandardRackFlank

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STANDARD_RACK_FLANK

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_StandardRackFlank":
        """Cast to another type.

        Returns:
            _Cast_StandardRackFlank
        """
        return _Cast_StandardRackFlank(self)

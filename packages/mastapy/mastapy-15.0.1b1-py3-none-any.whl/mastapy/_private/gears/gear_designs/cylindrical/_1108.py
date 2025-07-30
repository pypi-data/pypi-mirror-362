"""CrossedAxisCylindricalGearPairLineContact"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1107

_CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR_LINE_CONTACT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CrossedAxisCylindricalGearPairLineContact",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CrossedAxisCylindricalGearPairLineContact")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CrossedAxisCylindricalGearPairLineContact._Cast_CrossedAxisCylindricalGearPairLineContact",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CrossedAxisCylindricalGearPairLineContact",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CrossedAxisCylindricalGearPairLineContact:
    """Special nested class for casting CrossedAxisCylindricalGearPairLineContact to subclasses."""

    __parent__: "CrossedAxisCylindricalGearPairLineContact"

    @property
    def crossed_axis_cylindrical_gear_pair(
        self: "CastSelf",
    ) -> "_1107.CrossedAxisCylindricalGearPair":
        return self.__parent__._cast(_1107.CrossedAxisCylindricalGearPair)

    @property
    def crossed_axis_cylindrical_gear_pair_line_contact(
        self: "CastSelf",
    ) -> "CrossedAxisCylindricalGearPairLineContact":
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
class CrossedAxisCylindricalGearPairLineContact(_1107.CrossedAxisCylindricalGearPair):
    """CrossedAxisCylindricalGearPairLineContact

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR_LINE_CONTACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CrossedAxisCylindricalGearPairLineContact":
        """Cast to another type.

        Returns:
            _Cast_CrossedAxisCylindricalGearPairLineContact
        """
        return _Cast_CrossedAxisCylindricalGearPairLineContact(self)

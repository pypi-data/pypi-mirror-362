"""CrossedAxisCylindricalGearPairPointContact"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.gear_designs.cylindrical import _1107

_CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR_POINT_CONTACT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CrossedAxisCylindricalGearPairPointContact",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CrossedAxisCylindricalGearPairPointContact")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CrossedAxisCylindricalGearPairPointContact._Cast_CrossedAxisCylindricalGearPairPointContact",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CrossedAxisCylindricalGearPairPointContact",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CrossedAxisCylindricalGearPairPointContact:
    """Special nested class for casting CrossedAxisCylindricalGearPairPointContact to subclasses."""

    __parent__: "CrossedAxisCylindricalGearPairPointContact"

    @property
    def crossed_axis_cylindrical_gear_pair(
        self: "CastSelf",
    ) -> "_1107.CrossedAxisCylindricalGearPair":
        return self.__parent__._cast(_1107.CrossedAxisCylindricalGearPair)

    @property
    def crossed_axis_cylindrical_gear_pair_point_contact(
        self: "CastSelf",
    ) -> "CrossedAxisCylindricalGearPairPointContact":
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
class CrossedAxisCylindricalGearPairPointContact(_1107.CrossedAxisCylindricalGearPair):
    """CrossedAxisCylindricalGearPairPointContact

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CROSSED_AXIS_CYLINDRICAL_GEAR_PAIR_POINT_CONTACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CrossedAxisCylindricalGearPairPointContact":
        """Cast to another type.

        Returns:
            _Cast_CrossedAxisCylindricalGearPairPointContact
        """
        return _Cast_CrossedAxisCylindricalGearPairPointContact(self)

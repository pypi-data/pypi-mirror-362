"""ConicalGearProfileModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.micro_geometry import _673

_CONICAL_GEAR_PROFILE_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry",
    "ConicalGearProfileModification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.micro_geometry import _670

    Self = TypeVar("Self", bound="ConicalGearProfileModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearProfileModification._Cast_ConicalGearProfileModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearProfileModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearProfileModification:
    """Special nested class for casting ConicalGearProfileModification to subclasses."""

    __parent__: "ConicalGearProfileModification"

    @property
    def profile_modification(self: "CastSelf") -> "_673.ProfileModification":
        return self.__parent__._cast(_673.ProfileModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def conical_gear_profile_modification(
        self: "CastSelf",
    ) -> "ConicalGearProfileModification":
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
class ConicalGearProfileModification(_673.ProfileModification):
    """ConicalGearProfileModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_PROFILE_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearProfileModification":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearProfileModification
        """
        return _Cast_ConicalGearProfileModification(self)

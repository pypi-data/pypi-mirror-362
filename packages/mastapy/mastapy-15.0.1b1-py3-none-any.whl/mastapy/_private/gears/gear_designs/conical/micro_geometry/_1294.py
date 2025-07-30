"""ConicalGearLeadModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.micro_geometry import _663

_CONICAL_GEAR_LEAD_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical.MicroGeometry",
    "ConicalGearLeadModification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.micro_geometry import _670

    Self = TypeVar("Self", bound="ConicalGearLeadModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalGearLeadModification._Cast_ConicalGearLeadModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearLeadModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearLeadModification:
    """Special nested class for casting ConicalGearLeadModification to subclasses."""

    __parent__: "ConicalGearLeadModification"

    @property
    def lead_modification(self: "CastSelf") -> "_663.LeadModification":
        return self.__parent__._cast(_663.LeadModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def conical_gear_lead_modification(
        self: "CastSelf",
    ) -> "ConicalGearLeadModification":
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
class ConicalGearLeadModification(_663.LeadModification):
    """ConicalGearLeadModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_LEAD_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearLeadModification":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearLeadModification
        """
        return _Cast_ConicalGearLeadModification(self)

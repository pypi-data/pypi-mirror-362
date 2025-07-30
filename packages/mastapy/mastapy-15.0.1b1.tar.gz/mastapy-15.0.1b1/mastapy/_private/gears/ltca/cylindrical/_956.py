"""CylindricalGearContactStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.ltca import _938

_CYLINDRICAL_GEAR_CONTACT_STIFFNESS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA.Cylindrical", "CylindricalGearContactStiffness"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.ltca import _950
    from mastapy._private.nodal_analysis import _69

    Self = TypeVar("Self", bound="CylindricalGearContactStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearContactStiffness._Cast_CylindricalGearContactStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearContactStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearContactStiffness:
    """Special nested class for casting CylindricalGearContactStiffness to subclasses."""

    __parent__: "CylindricalGearContactStiffness"

    @property
    def gear_contact_stiffness(self: "CastSelf") -> "_938.GearContactStiffness":
        return self.__parent__._cast(_938.GearContactStiffness)

    @property
    def gear_stiffness(self: "CastSelf") -> "_950.GearStiffness":
        from mastapy._private.gears.ltca import _950

        return self.__parent__._cast(_950.GearStiffness)

    @property
    def fe_stiffness(self: "CastSelf") -> "_69.FEStiffness":
        from mastapy._private.nodal_analysis import _69

        return self.__parent__._cast(_69.FEStiffness)

    @property
    def cylindrical_gear_contact_stiffness(
        self: "CastSelf",
    ) -> "CylindricalGearContactStiffness":
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
class CylindricalGearContactStiffness(_938.GearContactStiffness):
    """CylindricalGearContactStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_CONTACT_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearContactStiffness":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearContactStiffness
        """
        return _Cast_CylindricalGearContactStiffness(self)

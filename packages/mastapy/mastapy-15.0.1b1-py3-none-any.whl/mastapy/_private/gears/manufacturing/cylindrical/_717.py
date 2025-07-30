"""CylindricalGearSpecifiedProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CYLINDRICAL_GEAR_SPECIFIED_PROFILE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "CylindricalGearSpecifiedProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearSpecifiedProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSpecifiedProfile._Cast_CylindricalGearSpecifiedProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSpecifiedProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSpecifiedProfile:
    """Special nested class for casting CylindricalGearSpecifiedProfile to subclasses."""

    __parent__: "CylindricalGearSpecifiedProfile"

    @property
    def cylindrical_gear_specified_profile(
        self: "CastSelf",
    ) -> "CylindricalGearSpecifiedProfile":
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
class CylindricalGearSpecifiedProfile(_0.APIBase):
    """CylindricalGearSpecifiedProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SPECIFIED_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def offset_at_minimum_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OffsetAtMinimumRollDistance")

        if temp is None:
            return 0.0

        return temp

    @offset_at_minimum_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def offset_at_minimum_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OffsetAtMinimumRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSpecifiedProfile":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSpecifiedProfile
        """
        return _Cast_CylindricalGearSpecifiedProfile(self)

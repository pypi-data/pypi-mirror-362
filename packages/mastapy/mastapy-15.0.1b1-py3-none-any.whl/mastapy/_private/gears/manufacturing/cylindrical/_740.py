"""ProfileModificationSegment"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.gears.manufacturing.cylindrical import _739

_PROFILE_MODIFICATION_SEGMENT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "ProfileModificationSegment"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ProfileModificationSegment")
    CastSelf = TypeVar(
        "CastSelf", bound="ProfileModificationSegment._Cast_ProfileModificationSegment"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProfileModificationSegment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProfileModificationSegment:
    """Special nested class for casting ProfileModificationSegment to subclasses."""

    __parent__: "ProfileModificationSegment"

    @property
    def modification_segment(self: "CastSelf") -> "_739.ModificationSegment":
        return self.__parent__._cast(_739.ModificationSegment)

    @property
    def profile_modification_segment(self: "CastSelf") -> "ProfileModificationSegment":
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
class ProfileModificationSegment(_739.ModificationSegment):
    """ProfileModificationSegment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROFILE_MODIFICATION_SEGMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Diameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollAngle")

        if temp is None:
            return 0.0

        return temp

    @roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RollAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollDistance")

        if temp is None:
            return 0.0

        return temp

    @roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RollDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def use_iso217712007_slope_sign_convention(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseISO217712007SlopeSignConvention"
        )

        if temp is None:
            return False

        return temp

    @use_iso217712007_slope_sign_convention.setter
    @exception_bridge
    @enforce_parameter_types
    def use_iso217712007_slope_sign_convention(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseISO217712007SlopeSignConvention",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ProfileModificationSegment":
        """Cast to another type.

        Returns:
            _Cast_ProfileModificationSegment
        """
        return _Cast_ProfileModificationSegment(self)

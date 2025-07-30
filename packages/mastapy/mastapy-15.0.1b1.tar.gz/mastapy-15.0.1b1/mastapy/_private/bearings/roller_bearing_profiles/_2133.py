"""RollerBearingConicalProfile"""

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
from mastapy._private.bearings.roller_bearing_profiles import _2141

_ROLLER_BEARING_CONICAL_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingConicalProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerBearingConicalProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingConicalProfile._Cast_RollerBearingConicalProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingConicalProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingConicalProfile:
    """Special nested class for casting RollerBearingConicalProfile to subclasses."""

    __parent__: "RollerBearingConicalProfile"

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_conical_profile(
        self: "CastSelf",
    ) -> "RollerBearingConicalProfile":
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
class RollerBearingConicalProfile(_2141.RollerBearingProfile):
    """RollerBearingConicalProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_CONICAL_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cone_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConeAngle")

        if temp is None:
            return 0.0

        return temp

    @cone_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def cone_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ConeAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def deviation_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeviationOffset")

        if temp is None:
            return 0.0

        return temp

    @deviation_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def deviation_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DeviationOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def deviation_at_end_of_component(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DeviationAtEndOfComponent")

        if temp is None:
            return 0.0

        return temp

    @deviation_at_end_of_component.setter
    @exception_bridge
    @enforce_parameter_types
    def deviation_at_end_of_component(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DeviationAtEndOfComponent",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingConicalProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingConicalProfile
        """
        return _Cast_RollerBearingConicalProfile(self)

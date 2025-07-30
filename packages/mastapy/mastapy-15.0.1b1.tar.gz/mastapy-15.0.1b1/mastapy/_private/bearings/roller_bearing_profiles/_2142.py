"""RollerBearingTangentialCrownedProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.roller_bearing_profiles import _2141

_ROLLER_BEARING_TANGENTIAL_CROWNED_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles",
    "RollerBearingTangentialCrownedProfile",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="RollerBearingTangentialCrownedProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingTangentialCrownedProfile._Cast_RollerBearingTangentialCrownedProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingTangentialCrownedProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingTangentialCrownedProfile:
    """Special nested class for casting RollerBearingTangentialCrownedProfile to subclasses."""

    __parent__: "RollerBearingTangentialCrownedProfile"

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_tangential_crowned_profile(
        self: "CastSelf",
    ) -> "RollerBearingTangentialCrownedProfile":
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
class RollerBearingTangentialCrownedProfile(_2141.RollerBearingProfile):
    """RollerBearingTangentialCrownedProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_TANGENTIAL_CROWNED_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def crown_end_drop(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CrownEndDrop")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @crown_end_drop.setter
    @exception_bridge
    @enforce_parameter_types
    def crown_end_drop(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CrownEndDrop", value)

    @property
    @exception_bridge
    def crown_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CrownRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @crown_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def crown_radius(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CrownRadius", value)

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @exception_bridge
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def parallel_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ParallelLength")

        if temp is None:
            return 0.0

        return temp

    @parallel_length.setter
    @exception_bridge
    @enforce_parameter_types
    def parallel_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ParallelLength", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingTangentialCrownedProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingTangentialCrownedProfile
        """
        return _Cast_RollerBearingTangentialCrownedProfile(self)

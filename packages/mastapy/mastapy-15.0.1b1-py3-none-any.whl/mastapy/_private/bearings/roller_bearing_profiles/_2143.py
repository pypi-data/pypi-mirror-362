"""RollerBearingUserSpecifiedProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.roller_bearing_profiles import _2141

_ROLLER_BEARING_USER_SPECIFIED_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingUserSpecifiedProfile"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.roller_bearing_profiles import _2130, _2132, _2145

    Self = TypeVar("Self", bound="RollerBearingUserSpecifiedProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingUserSpecifiedProfile._Cast_RollerBearingUserSpecifiedProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingUserSpecifiedProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingUserSpecifiedProfile:
    """Special nested class for casting RollerBearingUserSpecifiedProfile to subclasses."""

    __parent__: "RollerBearingUserSpecifiedProfile"

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_user_specified_profile(
        self: "CastSelf",
    ) -> "RollerBearingUserSpecifiedProfile":
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
class RollerBearingUserSpecifiedProfile(_2141.RollerBearingProfile):
    """RollerBearingUserSpecifiedProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_USER_SPECIFIED_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def data_to_use(self: "Self") -> "_2130.ProfileDataToUse":
        """mastapy.bearings.roller_bearing_profiles.ProfileDataToUse"""
        temp = pythonnet_property_get(self.wrapped, "DataToUse")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.RollerBearingProfiles.ProfileDataToUse"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.roller_bearing_profiles._2130",
            "ProfileDataToUse",
        )(value)

    @data_to_use.setter
    @exception_bridge
    @enforce_parameter_types
    def data_to_use(self: "Self", value: "_2130.ProfileDataToUse") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.RollerBearingProfiles.ProfileDataToUse"
        )
        pythonnet_property_set(self.wrapped, "DataToUse", value)

    @property
    @exception_bridge
    def number_of_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPoints")

        if temp is None:
            return 0

        return temp

    @number_of_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfPoints", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def profile_to_fit(self: "Self") -> "_2132.ProfileToFit":
        """mastapy.bearings.roller_bearing_profiles.ProfileToFit"""
        temp = pythonnet_property_get(self.wrapped, "ProfileToFit")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.RollerBearingProfiles.ProfileToFit"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.roller_bearing_profiles._2132", "ProfileToFit"
        )(value)

    @profile_to_fit.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_to_fit(self: "Self", value: "_2132.ProfileToFit") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.RollerBearingProfiles.ProfileToFit"
        )
        pythonnet_property_set(self.wrapped, "ProfileToFit", value)

    @property
    @exception_bridge
    def points(self: "Self") -> "List[_2145.UserSpecifiedProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.UserSpecifiedProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Points")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def set_to_full_range(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SetToFullRange")

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingUserSpecifiedProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingUserSpecifiedProfile
        """
        return _Cast_RollerBearingUserSpecifiedProfile(self)

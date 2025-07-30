"""RollerBearingJohnsGoharProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.roller_bearing_profiles import _2139

_ROLLER_BEARING_JOHNS_GOHAR_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingJohnsGoharProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.roller_bearing_profiles import _2141

    Self = TypeVar("Self", bound="RollerBearingJohnsGoharProfile")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RollerBearingJohnsGoharProfile._Cast_RollerBearingJohnsGoharProfile",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingJohnsGoharProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingJohnsGoharProfile:
    """Special nested class for casting RollerBearingJohnsGoharProfile to subclasses."""

    __parent__: "RollerBearingJohnsGoharProfile"

    @property
    def roller_bearing_load_dependent_profile(
        self: "CastSelf",
    ) -> "_2139.RollerBearingLoadDependentProfile":
        return self.__parent__._cast(_2139.RollerBearingLoadDependentProfile)

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        from mastapy._private.bearings.roller_bearing_profiles import _2141

        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_johns_gohar_profile(
        self: "CastSelf",
    ) -> "RollerBearingJohnsGoharProfile":
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
class RollerBearingJohnsGoharProfile(_2139.RollerBearingLoadDependentProfile):
    """RollerBearingJohnsGoharProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_JOHNS_GOHAR_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingJohnsGoharProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingJohnsGoharProfile
        """
        return _Cast_RollerBearingJohnsGoharProfile(self)

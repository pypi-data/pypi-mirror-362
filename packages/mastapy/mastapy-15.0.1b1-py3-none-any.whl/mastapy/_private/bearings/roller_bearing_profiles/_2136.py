"""RollerBearingFlatProfile"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.roller_bearing_profiles import _2141

_ROLLER_BEARING_FLAT_PROFILE = python_net_import(
    "SMT.MastaAPI.Bearings.RollerBearingProfiles", "RollerBearingFlatProfile"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerBearingFlatProfile")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerBearingFlatProfile._Cast_RollerBearingFlatProfile"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingFlatProfile",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearingFlatProfile:
    """Special nested class for casting RollerBearingFlatProfile to subclasses."""

    __parent__: "RollerBearingFlatProfile"

    @property
    def roller_bearing_profile(self: "CastSelf") -> "_2141.RollerBearingProfile":
        return self.__parent__._cast(_2141.RollerBearingProfile)

    @property
    def roller_bearing_flat_profile(self: "CastSelf") -> "RollerBearingFlatProfile":
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
class RollerBearingFlatProfile(_2141.RollerBearingProfile):
    """RollerBearingFlatProfile

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING_FLAT_PROFILE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearingFlatProfile":
        """Cast to another type.

        Returns:
            _Cast_RollerBearingFlatProfile
        """
        return _Cast_RollerBearingFlatProfile(self)

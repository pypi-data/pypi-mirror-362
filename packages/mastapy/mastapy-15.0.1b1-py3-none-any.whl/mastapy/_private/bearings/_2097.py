"""RollingBearingKey"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _2025

_ROLLING_BEARING_KEY = python_net_import("SMT.MastaAPI.Bearings", "RollingBearingKey")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollingBearingKey")
    CastSelf = TypeVar("CastSelf", bound="RollingBearingKey._Cast_RollingBearingKey")


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingKey",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearingKey:
    """Special nested class for casting RollingBearingKey to subclasses."""

    __parent__: "RollingBearingKey"

    @property
    def database_key(self: "CastSelf") -> "_2025.DatabaseKey":
        return self.__parent__._cast(_2025.DatabaseKey)

    @property
    def rolling_bearing_key(self: "CastSelf") -> "RollingBearingKey":
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
class RollingBearingKey(_2025.DatabaseKey):
    """RollingBearingKey

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING_KEY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearingKey":
        """Cast to another type.

        Returns:
            _Cast_RollingBearingKey
        """
        return _Cast_RollingBearingKey(self)

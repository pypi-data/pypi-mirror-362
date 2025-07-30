"""BevelHypoidGearDesignSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_BEVEL_HYPOID_GEAR_DESIGN_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears", "BevelHypoidGearDesignSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BevelHypoidGearDesignSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BevelHypoidGearDesignSettings._Cast_BevelHypoidGearDesignSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BevelHypoidGearDesignSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelHypoidGearDesignSettings:
    """Special nested class for casting BevelHypoidGearDesignSettings to subclasses."""

    __parent__: "BevelHypoidGearDesignSettings"

    @property
    def bevel_hypoid_gear_design_settings(
        self: "CastSelf",
    ) -> "BevelHypoidGearDesignSettings":
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
class BevelHypoidGearDesignSettings(_0.APIBase):
    """BevelHypoidGearDesignSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_HYPOID_GEAR_DESIGN_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_BevelHypoidGearDesignSettings":
        """Cast to another type.

        Returns:
            _Cast_BevelHypoidGearDesignSettings
        """
        return _Cast_BevelHypoidGearDesignSettings(self)

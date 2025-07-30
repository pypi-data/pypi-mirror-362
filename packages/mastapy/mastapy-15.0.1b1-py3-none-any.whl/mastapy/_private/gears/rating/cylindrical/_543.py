"""CylindricalGearDesignAndRatingSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_DESIGN_AND_RATING_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearDesignAndRatingSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearDesignAndRatingSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDesignAndRatingSettings._Cast_CylindricalGearDesignAndRatingSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesignAndRatingSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesignAndRatingSettings:
    """Special nested class for casting CylindricalGearDesignAndRatingSettings to subclasses."""

    __parent__: "CylindricalGearDesignAndRatingSettings"

    @property
    def cylindrical_gear_design_and_rating_settings(
        self: "CastSelf",
    ) -> "CylindricalGearDesignAndRatingSettings":
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
class CylindricalGearDesignAndRatingSettings(_0.APIBase):
    """CylindricalGearDesignAndRatingSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN_AND_RATING_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesignAndRatingSettings":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesignAndRatingSettings
        """
        return _Cast_CylindricalGearDesignAndRatingSettings(self)

"""CylindricalGearDesignAndRatingSettingsDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical import _545
from mastapy._private.utility.databases import _2027

_CYLINDRICAL_GEAR_DESIGN_AND_RATING_SETTINGS_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical",
    "CylindricalGearDesignAndRatingSettingsDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _2023, _2031

    Self = TypeVar("Self", bound="CylindricalGearDesignAndRatingSettingsDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDesignAndRatingSettingsDatabase._Cast_CylindricalGearDesignAndRatingSettingsDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesignAndRatingSettingsDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesignAndRatingSettingsDatabase:
    """Special nested class for casting CylindricalGearDesignAndRatingSettingsDatabase to subclasses."""

    __parent__: "CylindricalGearDesignAndRatingSettingsDatabase"

    @property
    def named_database(self: "CastSelf") -> "_2027.NamedDatabase":
        return self.__parent__._cast(_2027.NamedDatabase)

    @property
    def sql_database(self: "CastSelf") -> "_2031.SQLDatabase":
        pass

        from mastapy._private.utility.databases import _2031

        return self.__parent__._cast(_2031.SQLDatabase)

    @property
    def database(self: "CastSelf") -> "_2023.Database":
        pass

        from mastapy._private.utility.databases import _2023

        return self.__parent__._cast(_2023.Database)

    @property
    def cylindrical_gear_design_and_rating_settings_database(
        self: "CastSelf",
    ) -> "CylindricalGearDesignAndRatingSettingsDatabase":
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
class CylindricalGearDesignAndRatingSettingsDatabase(
    _2027.NamedDatabase[_545.CylindricalGearDesignAndRatingSettingsItem]
):
    """CylindricalGearDesignAndRatingSettingsDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN_AND_RATING_SETTINGS_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesignAndRatingSettingsDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesignAndRatingSettingsDatabase
        """
        return _Cast_CylindricalGearDesignAndRatingSettingsDatabase(self)

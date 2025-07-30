"""ISOTR1417912001CoefficientOfFrictionConstantsDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.materials import _698
from mastapy._private.utility.databases import _2027

_ISOTR1417912001_COEFFICIENT_OF_FRICTION_CONSTANTS_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials",
    "ISOTR1417912001CoefficientOfFrictionConstantsDatabase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _2023, _2031

    Self = TypeVar(
        "Self", bound="ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISOTR1417912001CoefficientOfFrictionConstantsDatabase._Cast_ISOTR1417912001CoefficientOfFrictionConstantsDatabase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISOTR1417912001CoefficientOfFrictionConstantsDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISOTR1417912001CoefficientOfFrictionConstantsDatabase:
    """Special nested class for casting ISOTR1417912001CoefficientOfFrictionConstantsDatabase to subclasses."""

    __parent__: "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"

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
    def isotr1417912001_coefficient_of_friction_constants_database(
        self: "CastSelf",
    ) -> "ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
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
class ISOTR1417912001CoefficientOfFrictionConstantsDatabase(
    _2027.NamedDatabase[_698.ISOTR1417912001CoefficientOfFrictionConstants]
):
    """ISOTR1417912001CoefficientOfFrictionConstantsDatabase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISOTR1417912001_COEFFICIENT_OF_FRICTION_CONSTANTS_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ISOTR1417912001CoefficientOfFrictionConstantsDatabase":
        """Cast to another type.

        Returns:
            _Cast_ISOTR1417912001CoefficientOfFrictionConstantsDatabase
        """
        return _Cast_ISOTR1417912001CoefficientOfFrictionConstantsDatabase(self)

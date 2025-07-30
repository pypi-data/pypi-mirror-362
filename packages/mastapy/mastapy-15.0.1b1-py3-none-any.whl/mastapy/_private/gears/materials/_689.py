"""GearMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.databases import _2027

_GEAR_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "GearMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.materials import _680, _688, _700
    from mastapy._private.utility.databases import _2023, _2031

    Self = TypeVar("Self", bound="GearMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMaterialDatabase._Cast_GearMaterialDatabase"
    )

T = TypeVar("T", bound="_688.GearMaterial")

__docformat__ = "restructuredtext en"
__all__ = ("GearMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMaterialDatabase:
    """Special nested class for casting GearMaterialDatabase to subclasses."""

    __parent__: "GearMaterialDatabase"

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
    def bevel_gear_material_database(
        self: "CastSelf",
    ) -> "_680.BevelGearMaterialDatabase":
        from mastapy._private.gears.materials import _680

        return self.__parent__._cast(_680.BevelGearMaterialDatabase)

    @property
    def klingelnberg_conical_gear_material_database(
        self: "CastSelf",
    ) -> "_700.KlingelnbergConicalGearMaterialDatabase":
        from mastapy._private.gears.materials import _700

        return self.__parent__._cast(_700.KlingelnbergConicalGearMaterialDatabase)

    @property
    def gear_material_database(self: "CastSelf") -> "GearMaterialDatabase":
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
class GearMaterialDatabase(_2027.NamedDatabase[T]):
    """GearMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _GEAR_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_GearMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_GearMaterialDatabase
        """
        return _Cast_GearMaterialDatabase(self)

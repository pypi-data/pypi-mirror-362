"""CylindricalGearMaterialDatabase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _359

_CYLINDRICAL_GEAR_MATERIAL_DATABASE = python_net_import(
    "SMT.MastaAPI.Gears.Materials", "CylindricalGearMaterialDatabase"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.materials import _682, _683, _684, _686
    from mastapy._private.utility.databases import _2023, _2027, _2031

    Self = TypeVar("Self", bound="CylindricalGearMaterialDatabase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMaterialDatabase._Cast_CylindricalGearMaterialDatabase",
    )

T = TypeVar("T", bound="_684.CylindricalGearMaterial")

__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMaterialDatabase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMaterialDatabase:
    """Special nested class for casting CylindricalGearMaterialDatabase to subclasses."""

    __parent__: "CylindricalGearMaterialDatabase"

    @property
    def material_database(self: "CastSelf") -> "_359.MaterialDatabase":
        return self.__parent__._cast(_359.MaterialDatabase)

    @property
    def named_database(self: "CastSelf") -> "_2027.NamedDatabase":
        from mastapy._private.utility.databases import _2027

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
    def cylindrical_gear_agma_material_database(
        self: "CastSelf",
    ) -> "_682.CylindricalGearAGMAMaterialDatabase":
        from mastapy._private.gears.materials import _682

        return self.__parent__._cast(_682.CylindricalGearAGMAMaterialDatabase)

    @property
    def cylindrical_gear_iso_material_database(
        self: "CastSelf",
    ) -> "_683.CylindricalGearISOMaterialDatabase":
        from mastapy._private.gears.materials import _683

        return self.__parent__._cast(_683.CylindricalGearISOMaterialDatabase)

    @property
    def cylindrical_gear_plastic_material_database(
        self: "CastSelf",
    ) -> "_686.CylindricalGearPlasticMaterialDatabase":
        from mastapy._private.gears.materials import _686

        return self.__parent__._cast(_686.CylindricalGearPlasticMaterialDatabase)

    @property
    def cylindrical_gear_material_database(
        self: "CastSelf",
    ) -> "CylindricalGearMaterialDatabase":
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
class CylindricalGearMaterialDatabase(_359.MaterialDatabase[T]):
    """CylindricalGearMaterialDatabase

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MATERIAL_DATABASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMaterialDatabase":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMaterialDatabase
        """
        return _Cast_CylindricalGearMaterialDatabase(self)

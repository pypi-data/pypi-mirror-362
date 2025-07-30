"""CycloidalDiscMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.materials import _358

_CYCLOIDAL_DISC_MATERIAL = python_net_import(
    "SMT.MastaAPI.Cycloidal", "CycloidalDiscMaterial"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.databases import _2028

    Self = TypeVar("Self", bound="CycloidalDiscMaterial")
    CastSelf = TypeVar(
        "CastSelf", bound="CycloidalDiscMaterial._Cast_CycloidalDiscMaterial"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscMaterial:
    """Special nested class for casting CycloidalDiscMaterial to subclasses."""

    __parent__: "CycloidalDiscMaterial"

    @property
    def material(self: "CastSelf") -> "_358.Material":
        return self.__parent__._cast(_358.Material)

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        from mastapy._private.utility.databases import _2028

        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def cycloidal_disc_material(self: "CastSelf") -> "CycloidalDiscMaterial":
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
class CycloidalDiscMaterial(_358.Material):
    """CycloidalDiscMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscMaterial":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscMaterial
        """
        return _Cast_CycloidalDiscMaterial(self)

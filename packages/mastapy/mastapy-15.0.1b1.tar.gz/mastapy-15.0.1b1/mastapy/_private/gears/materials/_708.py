"""RawMaterial"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.databases import _2028

_RAW_MATERIAL = python_net_import("SMT.MastaAPI.Gears.Materials", "RawMaterial")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RawMaterial")
    CastSelf = TypeVar("CastSelf", bound="RawMaterial._Cast_RawMaterial")


__docformat__ = "restructuredtext en"
__all__ = ("RawMaterial",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RawMaterial:
    """Special nested class for casting RawMaterial to subclasses."""

    __parent__: "RawMaterial"

    @property
    def named_database_item(self: "CastSelf") -> "_2028.NamedDatabaseItem":
        return self.__parent__._cast(_2028.NamedDatabaseItem)

    @property
    def raw_material(self: "CastSelf") -> "RawMaterial":
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
class RawMaterial(_2028.NamedDatabaseItem):
    """RawMaterial

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RAW_MATERIAL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cost_per_kilogram(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CostPerKilogram")

        if temp is None:
            return 0.0

        return temp

    @cost_per_kilogram.setter
    @exception_bridge
    @enforce_parameter_types
    def cost_per_kilogram(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CostPerKilogram", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_RawMaterial":
        """Cast to another type.

        Returns:
            _Cast_RawMaterial
        """
        return _Cast_RawMaterial(self)

"""NamedPlanetAssemblyIndex"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_NAMED_PLANET_ASSEMBLY_INDEX = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "NamedPlanetAssemblyIndex"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NamedPlanetAssemblyIndex")
    CastSelf = TypeVar(
        "CastSelf", bound="NamedPlanetAssemblyIndex._Cast_NamedPlanetAssemblyIndex"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NamedPlanetAssemblyIndex",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedPlanetAssemblyIndex:
    """Special nested class for casting NamedPlanetAssemblyIndex to subclasses."""

    __parent__: "NamedPlanetAssemblyIndex"

    @property
    def named_planet_assembly_index(self: "CastSelf") -> "NamedPlanetAssemblyIndex":
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
class NamedPlanetAssemblyIndex(_0.APIBase):
    """NamedPlanetAssemblyIndex

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NAMED_PLANET_ASSEMBLY_INDEX

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def planet_assembly_index(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PlanetAssemblyIndex")

        if temp is None:
            return 0.0

        return temp

    @planet_assembly_index.setter
    @exception_bridge
    @enforce_parameter_types
    def planet_assembly_index(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PlanetAssemblyIndex",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_NamedPlanetAssemblyIndex":
        """Cast to another type.

        Returns:
            _Cast_NamedPlanetAssemblyIndex
        """
        return _Cast_NamedPlanetAssemblyIndex(self)

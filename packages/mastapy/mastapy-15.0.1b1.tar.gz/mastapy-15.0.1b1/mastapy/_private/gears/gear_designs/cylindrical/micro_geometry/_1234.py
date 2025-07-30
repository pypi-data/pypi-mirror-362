"""MeshAlignment"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MESH_ALIGNMENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry", "MeshAlignment"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1226

    Self = TypeVar("Self", bound="MeshAlignment")
    CastSelf = TypeVar("CastSelf", bound="MeshAlignment._Cast_MeshAlignment")


__docformat__ = "restructuredtext en"
__all__ = ("MeshAlignment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MeshAlignment:
    """Special nested class for casting MeshAlignment to subclasses."""

    __parent__: "MeshAlignment"

    @property
    def mesh_alignment(self: "CastSelf") -> "MeshAlignment":
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
class MeshAlignment(_0.APIBase):
    """MeshAlignment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MESH_ALIGNMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_a_alignment(self: "Self") -> "_1226.GearAlignment":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.GearAlignment

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearAAlignment")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b_alignment(self: "Self") -> "_1226.GearAlignment":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.GearAlignment

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearBAlignment")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MeshAlignment":
        """Cast to another type.

        Returns:
            _Cast_MeshAlignment
        """
        return _Cast_MeshAlignment(self)

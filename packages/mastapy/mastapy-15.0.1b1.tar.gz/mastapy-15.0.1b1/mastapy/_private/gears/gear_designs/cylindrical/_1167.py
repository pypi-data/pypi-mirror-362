"""ISO6336GeometryManufactured"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical import _1165

_ISO6336_GEOMETRY_MANUFACTURED = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ISO6336GeometryManufactured"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISO6336GeometryManufactured")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336GeometryManufactured._Cast_ISO6336GeometryManufactured",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336GeometryManufactured",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336GeometryManufactured:
    """Special nested class for casting ISO6336GeometryManufactured to subclasses."""

    __parent__: "ISO6336GeometryManufactured"

    @property
    def iso6336_geometry_base(self: "CastSelf") -> "_1165.ISO6336GeometryBase":
        return self.__parent__._cast(_1165.ISO6336GeometryBase)

    @property
    def iso6336_geometry_manufactured(
        self: "CastSelf",
    ) -> "ISO6336GeometryManufactured":
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
class ISO6336GeometryManufactured(_1165.ISO6336GeometryBase):
    """ISO6336GeometryManufactured

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_GEOMETRY_MANUFACTURED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def iso6336_root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336RootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso6336_tooth_root_chord(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO6336ToothRootChord")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336GeometryManufactured":
        """Cast to another type.

        Returns:
            _Cast_ISO6336GeometryManufactured
        """
        return _Cast_ISO6336GeometryManufactured(self)

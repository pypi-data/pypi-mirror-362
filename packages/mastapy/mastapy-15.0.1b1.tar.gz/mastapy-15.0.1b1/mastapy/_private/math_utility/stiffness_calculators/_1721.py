"""SurfaceToSurfaceContact"""

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
)

_SURFACE_TO_SURFACE_CONTACT = python_net_import(
    "SMT.MastaAPI.MathUtility.StiffnessCalculators", "SurfaceToSurfaceContact"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SurfaceToSurfaceContact")
    CastSelf = TypeVar(
        "CastSelf", bound="SurfaceToSurfaceContact._Cast_SurfaceToSurfaceContact"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SurfaceToSurfaceContact",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SurfaceToSurfaceContact:
    """Special nested class for casting SurfaceToSurfaceContact to subclasses."""

    __parent__: "SurfaceToSurfaceContact"

    @property
    def surface_to_surface_contact(self: "CastSelf") -> "SurfaceToSurfaceContact":
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
class SurfaceToSurfaceContact(_0.APIBase):
    """SurfaceToSurfaceContact

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SURFACE_TO_SURFACE_CONTACT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def normal_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_penetration(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfacePenetration")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SurfaceToSurfaceContact":
        """Cast to another type.

        Returns:
            _Cast_SurfaceToSurfaceContact
        """
        return _Cast_SurfaceToSurfaceContact(self)

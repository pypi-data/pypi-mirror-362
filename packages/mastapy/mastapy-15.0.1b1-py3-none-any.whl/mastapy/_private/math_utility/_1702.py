"""MassProperties"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_3d import Vector3D

_MASS_PROPERTIES = python_net_import("SMT.MastaAPI.MathUtility", "MassProperties")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.math_utility import _1701

    Self = TypeVar("Self", bound="MassProperties")
    CastSelf = TypeVar("CastSelf", bound="MassProperties._Cast_MassProperties")


__docformat__ = "restructuredtext en"
__all__ = ("MassProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MassProperties:
    """Special nested class for casting MassProperties to subclasses."""

    __parent__: "MassProperties"

    @property
    def mass_properties(self: "CastSelf") -> "MassProperties":
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
class MassProperties(_0.APIBase):
    """MassProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASS_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def centre_of_mass(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentreOfMass")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def inertia_tensor_about_centre_of_mass(self: "Self") -> "_1701.InertiaTensor":
        """mastapy.math_utility.InertiaTensor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaTensorAboutCentreOfMass")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inertia_tensor_about_origin(self: "Self") -> "_1701.InertiaTensor":
        """mastapy.math_utility.InertiaTensor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaTensorAboutOrigin")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_MassProperties":
        """Cast to another type.

        Returns:
            _Cast_MassProperties
        """
        return _Cast_MassProperties(self)

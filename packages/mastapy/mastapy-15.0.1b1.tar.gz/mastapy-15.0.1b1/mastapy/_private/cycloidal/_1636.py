"""ContactSpecification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D

_CONTACT_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.Cycloidal", "ContactSpecification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ContactSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="ContactSpecification._Cast_ContactSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactSpecification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ContactSpecification:
    """Special nested class for casting ContactSpecification to subclasses."""

    __parent__: "ContactSpecification"

    @property
    def contact_specification(self: "CastSelf") -> "ContactSpecification":
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
class ContactSpecification(_0.APIBase):
    """ContactSpecification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONTACT_SPECIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def contact_line_direction(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLineDirection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_line_point_1(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLinePoint1")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_line_point_2(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactLinePoint2")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_point(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPoint")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def estimate_contact_point(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EstimateContactPoint")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ContactSpecification":
        """Cast to another type.

        Returns:
            _Cast_ContactSpecification
        """
        return _Cast_ContactSpecification(self)

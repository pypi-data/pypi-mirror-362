"""ScriptedPropertyNameAttribute"""

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

_SCRIPTED_PROPERTY_NAME_ATTRIBUTE = python_net_import(
    "SMT.MastaAPIUtility", "ScriptedPropertyNameAttribute"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ScriptedPropertyNameAttribute")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ScriptedPropertyNameAttribute._Cast_ScriptedPropertyNameAttribute",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ScriptedPropertyNameAttribute",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ScriptedPropertyNameAttribute:
    """Special nested class for casting ScriptedPropertyNameAttribute to subclasses."""

    __parent__: "ScriptedPropertyNameAttribute"

    @property
    def scripted_property_name_attribute(
        self: "CastSelf",
    ) -> "ScriptedPropertyNameAttribute":
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
class ScriptedPropertyNameAttribute:
    """ScriptedPropertyNameAttribute

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SCRIPTED_PROPERTY_NAME_ATTRIBUTE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def property_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PropertyName")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ScriptedPropertyNameAttribute":
        """Cast to another type.

        Returns:
            _Cast_ScriptedPropertyNameAttribute
        """
        return _Cast_ScriptedPropertyNameAttribute(self)

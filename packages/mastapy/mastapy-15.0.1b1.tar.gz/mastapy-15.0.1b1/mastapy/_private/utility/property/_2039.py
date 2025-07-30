"""DeletableCollectionMember"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)

_DELETABLE_COLLECTION_MEMBER = python_net_import(
    "SMT.MastaAPI.Utility.Property", "DeletableCollectionMember"
)

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="DeletableCollectionMember")
    CastSelf = TypeVar(
        "CastSelf", bound="DeletableCollectionMember._Cast_DeletableCollectionMember"
    )

T = TypeVar("T")

__docformat__ = "restructuredtext en"
__all__ = ("DeletableCollectionMember",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DeletableCollectionMember:
    """Special nested class for casting DeletableCollectionMember to subclasses."""

    __parent__: "DeletableCollectionMember"

    @property
    def deletable_collection_member(self: "CastSelf") -> "DeletableCollectionMember":
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
class DeletableCollectionMember(_0.APIBase, Generic[T]):
    """DeletableCollectionMember

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _DELETABLE_COLLECTION_MEMBER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def item(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

    @property
    def cast_to(self: "Self") -> "_Cast_DeletableCollectionMember":
        """Cast to another type.

        Returns:
            _Cast_DeletableCollectionMember
        """
        return _Cast_DeletableCollectionMember(self)

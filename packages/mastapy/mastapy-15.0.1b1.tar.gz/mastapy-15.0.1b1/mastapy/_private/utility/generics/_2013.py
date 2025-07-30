"""NamedTuple7"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_NAMED_TUPLE_7 = python_net_import("SMT.MastaAPI.Utility.Generics", "NamedTuple7")

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="NamedTuple7")
    CastSelf = TypeVar("CastSelf", bound="NamedTuple7._Cast_NamedTuple7")

T1 = TypeVar("T1")
T2 = TypeVar("T2")
T3 = TypeVar("T3")
T4 = TypeVar("T4")
T5 = TypeVar("T5")
T6 = TypeVar("T6")
T7 = TypeVar("T7")

__docformat__ = "restructuredtext en"
__all__ = ("NamedTuple7",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NamedTuple7:
    """Special nested class for casting NamedTuple7 to subclasses."""

    __parent__: "NamedTuple7"

    @property
    def named_tuple_7(self: "CastSelf") -> "NamedTuple7":
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
class NamedTuple7(_0.APIBase, Generic[T1, T2, T3, T4, T5, T6, T7]):
    """NamedTuple7

    This is a mastapy class.

    Generic Types:
        T1
        T2
        T3
        T4
        T5
        T6
        T7
    """

    TYPE: ClassVar["Type"] = _NAMED_TUPLE_7

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def item_1(self: "Self") -> "T1":
        """T1

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item1")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def item_2(self: "Self") -> "T2":
        """T2

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item2")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def item_3(self: "Self") -> "T3":
        """T3

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item3")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def item_4(self: "Self") -> "T4":
        """T4

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item4")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def item_5(self: "Self") -> "T5":
        """T5

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item5")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def item_6(self: "Self") -> "T6":
        """T6

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item6")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def item_7(self: "Self") -> "T7":
        """T7

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Item7")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_NamedTuple7":
        """Cast to another type.

        Returns:
            _Cast_NamedTuple7
        """
        return _Cast_NamedTuple7(self)

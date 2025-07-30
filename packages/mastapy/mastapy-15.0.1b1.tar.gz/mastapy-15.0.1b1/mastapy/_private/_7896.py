"""MarshalByRefObjects"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MARSHAL_BY_REF_OBJECTS = python_net_import(
    "SMT.MastaAPIUtility", "MarshalByRefObjects"
)

if TYPE_CHECKING:
    from typing import Any, NoReturn, Type


__docformat__ = "restructuredtext en"
__all__ = ("MarshalByRefObjects",)


class MarshalByRefObjects:
    """MarshalByRefObjects

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MARSHAL_BY_REF_OBJECTS

    def __new__(
        cls: "Type[MarshalByRefObjects]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[MarshalByRefObjects]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def add(item: "object") -> None:
        """Method does not return.

        Args:
            item (object)
        """
        pythonnet_method_call(MarshalByRefObjects.TYPE, "Add", item)

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def remove(item: "object") -> None:
        """Method does not return.

        Args:
            item (object)
        """
        pythonnet_method_call(MarshalByRefObjects.TYPE, "Remove", item)

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def disconnect(item: "object") -> None:
        """Method does not return.

        Args:
            item (object)
        """
        pythonnet_method_call(MarshalByRefObjects.TYPE, "Disconnect", item)

    @staticmethod
    @exception_bridge
    def clear() -> None:
        """Method does not return."""
        pythonnet_method_call(MarshalByRefObjects.TYPE, "Clear")

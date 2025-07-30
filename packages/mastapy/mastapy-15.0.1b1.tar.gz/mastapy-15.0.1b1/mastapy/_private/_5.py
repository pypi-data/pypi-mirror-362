"""Versioning"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.class_property import classproperty
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_VERSIONING = python_net_import("SMT.MastaAPI", "Versioning")

if TYPE_CHECKING:
    from typing import Any, NoReturn, Type


__docformat__ = "restructuredtext en"
__all__ = ("Versioning",)


class Versioning:
    """Versioning

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VERSIONING

    def __new__(cls: "Type[Versioning]", *args: "Any", **kwargs: "Any") -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[Versioning]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @classproperty
    @exception_bridge
    def api_release_version_string(cls) -> "str":
        """str"""
        temp = pythonnet_property_get(Versioning.TYPE, "APIReleaseVersionString")

        if temp is None:
            return ""

        return temp

    @classproperty
    @exception_bridge
    def masta_version_string(cls) -> "str":
        """str"""
        temp = pythonnet_property_get(Versioning.TYPE, "MastaVersionString")

        if temp is None:
            return ""

        return temp

    @classproperty
    @exception_bridge
    def is_backwards_compatible_case(cls) -> "bool":
        """bool"""
        temp = pythonnet_property_get(Versioning.TYPE, "IsBackwardsCompatibleCase")

        if temp is None:
            return False

        return temp

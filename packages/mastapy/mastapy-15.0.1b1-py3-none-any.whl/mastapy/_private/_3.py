"""PythonUtility"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.class_property import classproperty
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PYTHON_UTILITY = python_net_import("SMT.MastaAPI", "PythonUtility")

if TYPE_CHECKING:
    from typing import Any, NoReturn, Type


__docformat__ = "restructuredtext en"
__all__ = ("PythonUtility",)


class PythonUtility:
    """PythonUtility

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PYTHON_UTILITY

    def __new__(
        cls: "Type[PythonUtility]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[PythonUtility]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @classproperty
    @exception_bridge
    def python_install_directory(cls) -> "str":
        """str"""
        temp = pythonnet_property_get(PythonUtility.TYPE, "PythonInstallDirectory")

        if temp is None:
            return ""

        return temp

    @python_install_directory.setter
    @exception_bridge
    @enforce_parameter_types
    def python_install_directory(cls, value: "str") -> None:
        pythonnet_property_set(
            PythonUtility.TYPE,
            "PythonInstallDirectory",
            str(value) if value is not None else "",
        )

    @classproperty
    @exception_bridge
    def python_executable(cls) -> "str":
        """str"""
        temp = pythonnet_property_get(PythonUtility.TYPE, "PythonExecutable")

        if temp is None:
            return ""

        return temp

    @python_executable.setter
    @exception_bridge
    @enforce_parameter_types
    def python_executable(cls, value: "str") -> None:
        pythonnet_property_set(
            PythonUtility.TYPE,
            "PythonExecutable",
            str(value) if value is not None else "",
        )

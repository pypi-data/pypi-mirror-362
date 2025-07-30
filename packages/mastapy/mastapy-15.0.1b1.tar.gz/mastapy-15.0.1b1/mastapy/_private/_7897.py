"""EnvironmentVariableUtility"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_ENVIRONMENT_VARIABLE_UTILITY = python_net_import(
    "SMT.MastaAPIUtility", "EnvironmentVariableUtility"
)

if TYPE_CHECKING:
    from typing import Any, NoReturn, Type


__docformat__ = "restructuredtext en"
__all__ = ("EnvironmentVariableUtility",)


class EnvironmentVariableUtility:
    """EnvironmentVariableUtility

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ENVIRONMENT_VARIABLE_UTILITY

    def __new__(
        cls: "Type[EnvironmentVariableUtility]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[EnvironmentVariableUtility]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def add_to_path_if_necessary(directory: "str") -> None:
        """Method does not return.

        Args:
            directory (str)
        """
        directory = str(directory)
        pythonnet_method_call(
            EnvironmentVariableUtility.TYPE,
            "AddToPathIfNecessary",
            directory if directory else "",
        )

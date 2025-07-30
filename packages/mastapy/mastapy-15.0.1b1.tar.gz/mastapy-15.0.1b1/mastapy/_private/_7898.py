"""Remoting"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion
from mastapy._private._internal.class_property import classproperty
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_REMOTING = python_net_import("SMT.MastaAPIUtility", "Remoting")

if TYPE_CHECKING:
    from typing import Any, Iterable, NoReturn, Type


__docformat__ = "restructuredtext en"
__all__ = ("Remoting",)


class Remoting:
    """Remoting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REMOTING

    def __new__(cls: "Type[Remoting]", *args: "Any", **kwargs: "Any") -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[Remoting]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @classproperty
    @exception_bridge
    def masta_processes(cls) -> "Iterable[int]":
        """Iterable[int]"""
        temp = pythonnet_property_get(Remoting.TYPE, "MastaProcesses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_iterable(temp, int)

        if value is None:
            return None

        return value

    @classproperty
    @exception_bridge
    def remote_identifier(cls) -> "str":
        """str"""
        temp = pythonnet_property_get(Remoting.TYPE, "RemoteIdentifier")

        if temp is None:
            return ""

        return temp

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def initialise(process_id: "int") -> None:
        """Method does not return.

        Args:
            process_id (int)
        """
        process_id = int(process_id)
        pythonnet_method_call(
            Remoting.TYPE, "Initialise", process_id if process_id else 0
        )

    @staticmethod
    @exception_bridge
    def stop() -> None:
        """Method does not return."""
        pythonnet_method_call(Remoting.TYPE, "Stop")

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def url_for_process_id(process_id: "int") -> "str":
        """str

        Args:
            process_id (int)
        """
        process_id = int(process_id)
        method_result = pythonnet_method_call(
            Remoting.TYPE, "UrlForProcessId", process_id if process_id else 0
        )
        return method_result

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def is_remoting(process_id: "int" = 0) -> "bool":
        """bool

        Args:
            process_id (int, optional)
        """
        process_id = int(process_id)
        method_result = pythonnet_method_call(
            Remoting.TYPE, "IsRemoting", process_id if process_id else 0
        )
        return method_result

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def is_masta_or_runna_process(process_id: "int") -> "bool":
        """bool

        Args:
            process_id (int)
        """
        process_id = int(process_id)
        method_result = pythonnet_method_call(
            Remoting.TYPE, "IsMastaOrRunnaProcess", process_id if process_id else 0
        )
        return method_result

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def remoting_port_name(process_id: "int") -> "str":
        """str

        Args:
            process_id (int)
        """
        process_id = int(process_id)
        method_result = pythonnet_method_call(
            Remoting.TYPE, "RemotingPortName", process_id if process_id else 0
        )
        return method_result

    @staticmethod
    @exception_bridge
    def remoting_port_name_for_current_process() -> "str":
        """str"""
        method_result = pythonnet_method_call(
            Remoting.TYPE, "RemotingPortNameForCurrentProcess"
        )
        return method_result

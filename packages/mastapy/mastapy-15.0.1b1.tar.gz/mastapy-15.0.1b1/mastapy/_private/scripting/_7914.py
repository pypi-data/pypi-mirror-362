"""ApiVersioning"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_API_VERSIONING = python_net_import("SMT.MastaAPIUtility.Scripting", "ApiVersioning")

if TYPE_CHECKING:
    from typing import Any, Iterable, NoReturn, Type

    from mastapy._private.scripting import _7906


__docformat__ = "restructuredtext en"
__all__ = ("ApiVersioning",)


class ApiVersioning:
    """ApiVersioning

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _API_VERSIONING

    def __new__(
        cls: "Type[ApiVersioning]", *args: "Any", **kwargs: "Any"
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[ApiVersioning]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def get_available_api_versions(folder: "str") -> "Iterable[_7906.ApiVersion]":
        """Iterable[mastapy.scripting.ApiVersion]

        Args:
            folder (str)
        """
        folder = str(folder)
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(
                ApiVersioning.TYPE, "GetAvailableApiVersions", folder if folder else ""
            )
        )

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def get_available_api_utility_versions(
        folder: "str",
    ) -> "Iterable[_7906.ApiVersion]":
        """Iterable[mastapy.scripting.ApiVersion]

        Args:
            folder (str)
        """
        folder = str(folder)
        return conversion.pn_to_mp_objects_in_iterable(
            pythonnet_method_call(
                ApiVersioning.TYPE,
                "GetAvailableApiUtilityVersions",
                folder if folder else "",
            )
        )

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def get_api_version_for_assembly(
        api_library_search_folder: "str", assembly_path: "str"
    ) -> "_7906.ApiVersion":
        """mastapy.scripting.ApiVersion

        Args:
            api_library_search_folder (str)
            assembly_path (str)
        """
        api_library_search_folder = str(api_library_search_folder)
        assembly_path = str(assembly_path)
        method_result = pythonnet_method_call(
            ApiVersioning.TYPE,
            "GetApiVersionForAssembly",
            api_library_search_folder if api_library_search_folder else "",
            assembly_path if assembly_path else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

"""LegacyV2RuntimeActivationPolicyAttributeSetter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)

_LEGACY_V2_RUNTIME_ACTIVATION_POLICY_ATTRIBUTE_SETTER = python_net_import(
    "SMT.MastaAPI", "LegacyV2RuntimeActivationPolicyAttributeSetter"
)

if TYPE_CHECKING:
    from typing import Any, NoReturn, Type


__docformat__ = "restructuredtext en"
__all__ = ("LegacyV2RuntimeActivationPolicyAttributeSetter",)


class LegacyV2RuntimeActivationPolicyAttributeSetter:
    """LegacyV2RuntimeActivationPolicyAttributeSetter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LEGACY_V2_RUNTIME_ACTIVATION_POLICY_ATTRIBUTE_SETTER

    def __new__(
        cls: "Type[LegacyV2RuntimeActivationPolicyAttributeSetter]",
        *args: "Any",
        **kwargs: "Any",
    ) -> "NoReturn":
        """Override of the new magic method.

        Note:
            This class cannot be instantiated and this method will always throw an
            exception.

        Args:
            cls (Type[LegacyV2RuntimeActivationPolicyAttributeSetter]: The class to instantiate.
            *args (Any): Arguments.
            **kwargs (Any): Keyword arguments.

        Returns:
            NoReturn
        """
        raise TypeError("Class cannot be instantiated. Please use statically.")

    @staticmethod
    @exception_bridge
    def ensure_config_file_for_current_app_domain_permits_dot_net_2() -> None:
        """Method does not return."""
        pythonnet_method_call(
            LegacyV2RuntimeActivationPolicyAttributeSetter.TYPE,
            "EnsureConfigFileForCurrentAppDomainPermitsDotNet2",
        )

    @staticmethod
    @exception_bridge
    def get_config_file_path_for_setup_assembly() -> "str":
        """str"""
        method_result = pythonnet_method_call(
            LegacyV2RuntimeActivationPolicyAttributeSetter.TYPE,
            "GetConfigFilePathForSetupAssembly",
        )
        return method_result

"""Initialiser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_INITIALISER = python_net_import("SMT.MastaAPI", "Initialiser")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Initialiser")
    CastSelf = TypeVar("CastSelf", bound="Initialiser._Cast_Initialiser")


__docformat__ = "restructuredtext en"
__all__ = ("Initialiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Initialiser:
    """Special nested class for casting Initialiser to subclasses."""

    __parent__: "Initialiser"

    @property
    def initialiser(self: "CastSelf") -> "Initialiser":
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
class Initialiser:
    """Initialiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _INITIALISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @exception_bridge
    @enforce_parameter_types
    def initialise_api_access(self: "Self", installation_directory: "str") -> None:
        """Method does not return.

        Args:
            installation_directory (str)
        """
        installation_directory = str(installation_directory)
        pythonnet_method_call(
            self.wrapped,
            "InitialiseApiAccess",
            installation_directory if installation_directory else "",
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Initialiser":
        """Cast to another type.

        Returns:
            _Cast_Initialiser
        """
        return _Cast_Initialiser(self)

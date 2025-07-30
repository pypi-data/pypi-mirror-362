"""ModuleLicenceStatus"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_MODULE_LICENCE_STATUS = python_net_import(
    "SMT.MastaAPIUtility.Licensing", "ModuleLicenceStatus"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModuleLicenceStatus")
    CastSelf = TypeVar(
        "CastSelf", bound="ModuleLicenceStatus._Cast_ModuleLicenceStatus"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModuleLicenceStatus",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModuleLicenceStatus:
    """Special nested class for casting ModuleLicenceStatus to subclasses."""

    __parent__: "ModuleLicenceStatus"

    @property
    def module_licence_status(self: "CastSelf") -> "ModuleLicenceStatus":
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
class ModuleLicenceStatus:
    """ModuleLicenceStatus

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODULE_LICENCE_STATUS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def module_code(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModuleCode")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def module_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModuleName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def status(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Status")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def is_licensed(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsLicensed")

        if temp is None:
            return False

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ModuleLicenceStatus":
        """Cast to another type.

        Returns:
            _Cast_ModuleLicenceStatus
        """
        return _Cast_ModuleLicenceStatus(self)

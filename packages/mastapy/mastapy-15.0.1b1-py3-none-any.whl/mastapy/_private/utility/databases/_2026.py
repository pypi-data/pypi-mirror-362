"""DatabaseSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.utility import _1786

_DATABASE_SETTINGS = python_net_import(
    "SMT.MastaAPI.Utility.Databases", "DatabaseSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1787
    from mastapy._private.utility.databases import _2024

    Self = TypeVar("Self", bound="DatabaseSettings")
    CastSelf = TypeVar("CastSelf", bound="DatabaseSettings._Cast_DatabaseSettings")


__docformat__ = "restructuredtext en"
__all__ = ("DatabaseSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatabaseSettings:
    """Special nested class for casting DatabaseSettings to subclasses."""

    __parent__: "DatabaseSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def database_settings(self: "CastSelf") -> "DatabaseSettings":
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
class DatabaseSettings(_1786.PerMachineSettings):
    """DatabaseSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASE_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def connection_settings(self: "Self") -> "_2024.DatabaseConnectionSettings":
        """mastapy.utility.databases.DatabaseConnectionSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DatabaseSettings":
        """Cast to another type.

        Returns:
            _Cast_DatabaseSettings
        """
        return _Cast_DatabaseSettings(self)

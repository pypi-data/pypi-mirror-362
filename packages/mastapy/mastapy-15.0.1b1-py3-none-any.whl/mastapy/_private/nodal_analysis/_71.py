"""FEUserSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility import _1786

_FE_USER_SETTINGS = python_net_import("SMT.MastaAPI.NodalAnalysis", "FEUserSettings")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility import _1787

    Self = TypeVar("Self", bound="FEUserSettings")
    CastSelf = TypeVar("CastSelf", bound="FEUserSettings._Cast_FEUserSettings")


__docformat__ = "restructuredtext en"
__all__ = ("FEUserSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEUserSettings:
    """Special nested class for casting FEUserSettings to subclasses."""

    __parent__: "FEUserSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def fe_user_settings(self: "CastSelf") -> "FEUserSettings":
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
class FEUserSettings(_1786.PerMachineSettings):
    """FEUserSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_USER_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_FEUserSettings":
        """Cast to another type.

        Returns:
            _Cast_FEUserSettings
        """
        return _Cast_FEUserSettings(self)

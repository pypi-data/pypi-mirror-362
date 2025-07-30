"""DefaultExportSettings"""

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

_DEFAULT_EXPORT_SETTINGS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "DefaultExportSettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.part_model import _2699
    from mastapy._private.utility import _1787

    Self = TypeVar("Self", bound="DefaultExportSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="DefaultExportSettings._Cast_DefaultExportSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DefaultExportSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DefaultExportSettings:
    """Special nested class for casting DefaultExportSettings to subclasses."""

    __parent__: "DefaultExportSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def default_export_settings(self: "CastSelf") -> "DefaultExportSettings":
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
class DefaultExportSettings(_1786.PerMachineSettings):
    """DefaultExportSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DEFAULT_EXPORT_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def part_model_export_panel_options(
        self: "Self",
    ) -> "_2699.PartModelExportPanelOptions":
        """mastapy.system_model.part_model.PartModelExportPanelOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PartModelExportPanelOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DefaultExportSettings":
        """Cast to another type.

        Returns:
            _Cast_DefaultExportSettings
        """
        return _Cast_DefaultExportSettings(self)

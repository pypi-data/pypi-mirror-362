"""GeometryModellerSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1786

_GEOMETRY_MODELLER_SETTINGS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryModellerSettings"
)

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.utility import _1782, _1787

    Self = TypeVar("Self", bound="GeometryModellerSettings")
    CastSelf = TypeVar(
        "CastSelf", bound="GeometryModellerSettings._Cast_GeometryModellerSettings"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryModellerSettings:
    """Special nested class for casting GeometryModellerSettings to subclasses."""

    __parent__: "GeometryModellerSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def geometry_modeller_settings(self: "CastSelf") -> "GeometryModellerSettings":
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
class GeometryModellerSettings(_1786.PerMachineSettings):
    """GeometryModellerSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_MODELLER_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auto_detected_geometry_modeller_path(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "AutoDetectedGeometryModellerPath")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @auto_detected_geometry_modeller_path.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_detected_geometry_modeller_path(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "AutoDetectedGeometryModellerPath", value)

    @property
    @exception_bridge
    def disable_intel_mkl_internal_multithreading(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "DisableIntelMKLInternalMultithreading"
        )

        if temp is None:
            return False

        return temp

    @disable_intel_mkl_internal_multithreading.setter
    @exception_bridge
    @enforce_parameter_types
    def disable_intel_mkl_internal_multithreading(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DisableIntelMKLInternalMultithreading",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def folder_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FolderPath")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def geometry_modeller_arguments(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerArguments")

        if temp is None:
            return ""

        return temp

    @geometry_modeller_arguments.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_modeller_arguments(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeometryModellerArguments",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def hide_geometry_modeller_instead_of_closing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "HideGeometryModellerInsteadOfClosing"
        )

        if temp is None:
            return False

        return temp

    @hide_geometry_modeller_instead_of_closing.setter
    @exception_bridge
    @enforce_parameter_types
    def hide_geometry_modeller_instead_of_closing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HideGeometryModellerInsteadOfClosing",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def no_licence_for_geometry_modeller(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoLicenceForGeometryModeller")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def show_message_when_hiding_geometry_modeller(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ShowMessageWhenHidingGeometryModeller"
        )

        if temp is None:
            return False

        return temp

    @show_message_when_hiding_geometry_modeller.setter
    @exception_bridge
    @enforce_parameter_types
    def show_message_when_hiding_geometry_modeller(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowMessageWhenHidingGeometryModeller",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_auto_detected_geometry_modeller_path(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseAutoDetectedGeometryModellerPath"
        )

        if temp is None:
            return False

        return temp

    @use_auto_detected_geometry_modeller_path.setter
    @exception_bridge
    @enforce_parameter_types
    def use_auto_detected_geometry_modeller_path(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseAutoDetectedGeometryModellerPath",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_geometry_modeller_connected(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsGeometryModellerConnected")

        if temp is None:
            return False

        return temp

    @exception_bridge
    @enforce_parameter_types
    def launch_geometry_modeller(
        self: "Self", file_path: Optional["PathLike"] = None
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome

        Args:
            file_path (PathLike, optional)
        """
        file_path = str(file_path)
        method_result = pythonnet_method_call(
            self.wrapped, "LaunchGeometryModeller", file_path
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def select_folder_path(self: "Self", path: "str") -> None:
        """Method does not return.

        Args:
            path (str)
        """
        path = str(path)
        pythonnet_method_call(self.wrapped, "SelectFolderPath", path if path else "")

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryModellerSettings":
        """Cast to another type.

        Returns:
            _Cast_GeometryModellerSettings
        """
        return _Cast_GeometryModellerSettings(self)

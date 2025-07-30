"""ProgramSettings"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility import _1786

_PROGRAM_SETTINGS = python_net_import("SMT.MastaAPI.Utility", "ProgramSettings")

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.utility import _1787

    Self = TypeVar("Self", bound="ProgramSettings")
    CastSelf = TypeVar("CastSelf", bound="ProgramSettings._Cast_ProgramSettings")


__docformat__ = "restructuredtext en"
__all__ = ("ProgramSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProgramSettings:
    """Special nested class for casting ProgramSettings to subclasses."""

    __parent__: "ProgramSettings"

    @property
    def per_machine_settings(self: "CastSelf") -> "_1786.PerMachineSettings":
        return self.__parent__._cast(_1786.PerMachineSettings)

    @property
    def persistent_singleton(self: "CastSelf") -> "_1787.PersistentSingleton":
        from mastapy._private.utility import _1787

        return self.__parent__._cast(_1787.PersistentSingleton)

    @property
    def program_settings(self: "CastSelf") -> "ProgramSettings":
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
class ProgramSettings(_1786.PerMachineSettings):
    """ProgramSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROGRAM_SETTINGS

    class CheckForNewerVersionOption(Enum):
        """CheckForNewerVersionOption is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _PROGRAM_SETTINGS.CheckForNewerVersionOption

        ASK_ON_STARTUP = 0
        YES = 1
        NO = 2

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    CheckForNewerVersionOption.__setattr__ = __enum_setattr
    CheckForNewerVersionOption.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def two_dcad_guide_model_autosave_size_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TwoDCADGuideModelAutosaveSizeLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @two_dcad_guide_model_autosave_size_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def two_dcad_guide_model_autosave_size_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TwoDCADGuideModelAutosaveSizeLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def allow_multithreading(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AllowMultithreading")

        if temp is None:
            return False

        return temp

    @allow_multithreading.setter
    @exception_bridge
    @enforce_parameter_types
    def allow_multithreading(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowMultithreading",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def ask_for_part_names_in_the_2d_view(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AskForPartNamesInThe2DView")

        if temp is None:
            return False

        return temp

    @ask_for_part_names_in_the_2d_view.setter
    @exception_bridge
    @enforce_parameter_types
    def ask_for_part_names_in_the_2d_view(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AskForPartNamesInThe2DView",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def auto_return_licences_inactivity_interval_minutes(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "AutoReturnLicencesInactivityIntervalMinutes"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @auto_return_licences_inactivity_interval_minutes.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_return_licences_inactivity_interval_minutes(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AutoReturnLicencesInactivityIntervalMinutes", value
        )

    @property
    @exception_bridge
    def autosave_directory(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AutosaveDirectory")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def autosave_interval_minutes(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "AutosaveIntervalMinutes")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @autosave_interval_minutes.setter
    @exception_bridge
    @enforce_parameter_types
    def autosave_interval_minutes(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AutosaveIntervalMinutes", value)

    @property
    @exception_bridge
    def check_for_new_version_on_startup(
        self: "Self",
    ) -> "ProgramSettings.CheckForNewerVersionOption":
        """mastapy.utility.ProgramSettings.CheckForNewerVersionOption"""
        temp = pythonnet_property_get(self.wrapped, "CheckForNewVersionOnStartup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.ProgramSettings+CheckForNewerVersionOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.ProgramSettings.ProgramSettings",
            "CheckForNewerVersionOption",
        )(value)

    @check_for_new_version_on_startup.setter
    @exception_bridge
    @enforce_parameter_types
    def check_for_new_version_on_startup(
        self: "Self", value: "ProgramSettings.CheckForNewerVersionOption"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.ProgramSettings+CheckForNewerVersionOption"
        )
        pythonnet_property_set(self.wrapped, "CheckForNewVersionOnStartup", value)

    @property
    @exception_bridge
    def confirm_exit(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ConfirmExit")

        if temp is None:
            return False

        return temp

    @confirm_exit.setter
    @exception_bridge
    @enforce_parameter_types
    def confirm_exit(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ConfirmExit", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def font_size(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FontSize")

        if temp is None:
            return 0.0

        return temp

    @font_size.setter
    @exception_bridge
    @enforce_parameter_types
    def font_size(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FontSize", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def include_overridable_property_source_information(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeOverridablePropertySourceInformation"
        )

        if temp is None:
            return False

        return temp

    @include_overridable_property_source_information.setter
    @exception_bridge
    @enforce_parameter_types
    def include_overridable_property_source_information(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeOverridablePropertySourceInformation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_view_focus_linked_to_3d_by_default(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsViewFocusLinkedTo3DByDefault")

        if temp is None:
            return False

        return temp

    @is_view_focus_linked_to_3d_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def is_view_focus_linked_to_3d_by_default(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsViewFocusLinkedTo3DByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_saved_operation_mode_and_selection(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "LoadSavedOperationModeAndSelection"
        )

        if temp is None:
            return False

        return temp

    @load_saved_operation_mode_and_selection.setter
    @exception_bridge
    @enforce_parameter_types
    def load_saved_operation_mode_and_selection(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LoadSavedOperationModeAndSelection",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_number_of_files_to_store_in_history(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfFilesToStoreInHistory"
        )

        if temp is None:
            return 0

        return temp

    @maximum_number_of_files_to_store_in_history.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_files_to_store_in_history(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfFilesToStoreInHistory",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def maximum_number_of_threads_for_large_operations(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfThreadsForLargeOperations"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_threads_for_large_operations.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_threads_for_large_operations(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumNumberOfThreadsForLargeOperations", value
        )

    @property
    @exception_bridge
    def maximum_number_of_threads_for_mathematically_intensive_operations(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfThreadsForMathematicallyIntensiveOperations"
        )

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_threads_for_mathematically_intensive_operations.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_threads_for_mathematically_intensive_operations(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfThreadsForMathematicallyIntensiveOperations",
            value,
        )

    @property
    @exception_bridge
    def maximum_number_of_undo_items(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfUndoItems")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_undo_items.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_undo_items(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfUndoItems",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_cpu_cores(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCPUCores")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_cpu_threads(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfCPUThreads")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_connections_to_show_when_multi_selecting(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfConnectionsToShowWhenMultiSelecting"
        )

        if temp is None:
            return 0

        return temp

    @number_of_connections_to_show_when_multi_selecting.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_connections_to_show_when_multi_selecting(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfConnectionsToShowWhenMultiSelecting",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_days_of_advance_warning_for_expiring_features(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfDaysOfAdvanceWarningForExpiringFeatures"
        )

        if temp is None:
            return 0

        return temp

    @number_of_days_of_advance_warning_for_expiring_features.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_days_of_advance_warning_for_expiring_features(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfDaysOfAdvanceWarningForExpiringFeatures",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def override_font(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "OverrideFont")

        if temp is None:
            return ""

        return temp

    @override_font.setter
    @exception_bridge
    @enforce_parameter_types
    def override_font(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "OverrideFont", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def save_driva_results_by_default(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SaveDRIVAResultsByDefault")

        if temp is None:
            return False

        return temp

    @save_driva_results_by_default.setter
    @exception_bridge
    @enforce_parameter_types
    def save_driva_results_by_default(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SaveDRIVAResultsByDefault",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_drawing_numbers_in_tree_view(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowDrawingNumbersInTreeView")

        if temp is None:
            return False

        return temp

    @show_drawing_numbers_in_tree_view.setter
    @exception_bridge
    @enforce_parameter_types
    def show_drawing_numbers_in_tree_view(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowDrawingNumbersInTreeView",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_number_of_teeth_with_gear_set_names(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowNumberOfTeethWithGearSetNames")

        if temp is None:
            return False

        return temp

    @show_number_of_teeth_with_gear_set_names.setter
    @exception_bridge
    @enforce_parameter_types
    def show_number_of_teeth_with_gear_set_names(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowNumberOfTeethWithGearSetNames",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def show_user_interface_hints(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowUserInterfaceHints")

        if temp is None:
            return False

        return temp

    @show_user_interface_hints.setter
    @exception_bridge
    @enforce_parameter_types
    def show_user_interface_hints(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowUserInterfaceHints",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_background_saving(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseBackgroundSaving")

        if temp is None:
            return False

        return temp

    @use_background_saving.setter
    @exception_bridge
    @enforce_parameter_types
    def use_background_saving(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseBackgroundSaving",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_compression_for_masta_files(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCompressionForMASTAFiles")

        if temp is None:
            return False

        return temp

    @use_compression_for_masta_files.setter
    @exception_bridge
    @enforce_parameter_types
    def use_compression_for_masta_files(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCompressionForMASTAFiles",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_default_autosave_directory(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseDefaultAutosaveDirectory")

        if temp is None:
            return False

        return temp

    @use_default_autosave_directory.setter
    @exception_bridge
    @enforce_parameter_types
    def use_default_autosave_directory(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseDefaultAutosaveDirectory",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_standard_dialog_for_file_open(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseStandardDialogForFileOpen")

        if temp is None:
            return False

        return temp

    @use_standard_dialog_for_file_open.setter
    @exception_bridge
    @enforce_parameter_types
    def use_standard_dialog_for_file_open(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseStandardDialogForFileOpen",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_standard_dialog_for_file_save(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseStandardDialogForFileSave")

        if temp is None:
            return False

        return temp

    @use_standard_dialog_for_file_save.setter
    @exception_bridge
    @enforce_parameter_types
    def use_standard_dialog_for_file_save(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseStandardDialogForFileSave",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def user_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "UserName")

        if temp is None:
            return ""

        return temp

    @user_name.setter
    @exception_bridge
    @enforce_parameter_types
    def user_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "UserName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def user_defined_autosave_directory(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "UserDefinedAutosaveDirectory")

        if temp is None:
            return ""

        return temp

    @user_defined_autosave_directory.setter
    @exception_bridge
    @enforce_parameter_types
    def user_defined_autosave_directory(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserDefinedAutosaveDirectory",
            str(value) if value is not None else "",
        )

    @exception_bridge
    def clear_mru_entries(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ClearMRUEntries")

    @exception_bridge
    def select_autosave_directory(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "SelectAutosaveDirectory")

    @property
    def cast_to(self: "Self") -> "_Cast_ProgramSettings":
        """Cast to another type.

        Returns:
            _Cast_ProgramSettings
        """
        return _Cast_ProgramSettings(self)

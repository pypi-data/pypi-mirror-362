"""DynamicExternalInterfaceOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DYNAMIC_EXTERNAL_INTERFACE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.ExternalInterfaces",
    "DynamicExternalInterfaceOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.mbd_analyses import _5731

    Self = TypeVar("Self", bound="DynamicExternalInterfaceOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DynamicExternalInterfaceOptions._Cast_DynamicExternalInterfaceOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicExternalInterfaceOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicExternalInterfaceOptions:
    """Special nested class for casting DynamicExternalInterfaceOptions to subclasses."""

    __parent__: "DynamicExternalInterfaceOptions"

    @property
    def dynamic_external_interface_options(
        self: "CastSelf",
    ) -> "DynamicExternalInterfaceOptions":
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
class DynamicExternalInterfaceOptions(_0.APIBase):
    """DynamicExternalInterfaceOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_EXTERNAL_INTERFACE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def generate_load_case(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "GenerateLoadCase")

        if temp is None:
            return False

        return temp

    @generate_load_case.setter
    @exception_bridge
    @enforce_parameter_types
    def generate_load_case(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GenerateLoadCase",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def input_signal_filter_level(self: "Self") -> "_5731.InputSignalFilterLevel":
        """mastapy.system_model.analyses_and_results.mbd_analyses.InputSignalFilterLevel"""
        temp = pythonnet_property_get(self.wrapped, "InputSignalFilterLevel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InputSignalFilterLevel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.mbd_analyses._5731",
            "InputSignalFilterLevel",
        )(value)

    @input_signal_filter_level.setter
    @exception_bridge
    @enforce_parameter_types
    def input_signal_filter_level(
        self: "Self", value: "_5731.InputSignalFilterLevel"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.InputSignalFilterLevel",
        )
        pythonnet_property_set(self.wrapped, "InputSignalFilterLevel", value)

    @property
    @exception_bridge
    def path_of_saved_file(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "PathOfSavedFile")

        if temp is None:
            return ""

        return temp

    @path_of_saved_file.setter
    @exception_bridge
    @enforce_parameter_types
    def path_of_saved_file(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "PathOfSavedFile", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def sample_time(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SampleTime")

        if temp is None:
            return 0.0

        return temp

    @sample_time.setter
    @exception_bridge
    @enforce_parameter_types
    def sample_time(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SampleTime", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def save_results(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SaveResults")

        if temp is None:
            return False

        return temp

    @save_results.setter
    @exception_bridge
    @enforce_parameter_types
    def save_results(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SaveResults", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicExternalInterfaceOptions":
        """Cast to another type.

        Returns:
            _Cast_DynamicExternalInterfaceOptions
        """
        return _Cast_DynamicExternalInterfaceOptions(self)

"""CreateMicrophoneNormalToSurfaceOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
from mastapy._private.system_model.part_model import _2692

_CREATE_MICROPHONE_NORMAL_TO_SURFACE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "CreateMicrophoneNormalToSurfaceOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="CreateMicrophoneNormalToSurfaceOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CreateMicrophoneNormalToSurfaceOptions._Cast_CreateMicrophoneNormalToSurfaceOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CreateMicrophoneNormalToSurfaceOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CreateMicrophoneNormalToSurfaceOptions:
    """Special nested class for casting CreateMicrophoneNormalToSurfaceOptions to subclasses."""

    __parent__: "CreateMicrophoneNormalToSurfaceOptions"

    @property
    def create_microphone_normal_to_surface_options(
        self: "CastSelf",
    ) -> "CreateMicrophoneNormalToSurfaceOptions":
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
class CreateMicrophoneNormalToSurfaceOptions(_0.APIBase):
    """CreateMicrophoneNormalToSurfaceOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CREATE_MICROPHONE_NORMAL_TO_SURFACE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def distance_to_surface(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceToSurface")

        if temp is None:
            return 0.0

        return temp

    @distance_to_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_to_surface(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceToSurface",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def microphone_array_to_add_to(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_MicrophoneArray":
        """ListWithSelectedItem[mastapy.system_model.part_model.MicrophoneArray]"""
        temp = pythonnet_property_get(self.wrapped, "MicrophoneArrayToAddTo")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_MicrophoneArray",
        )(temp)

    @microphone_array_to_add_to.setter
    @exception_bridge
    @enforce_parameter_types
    def microphone_array_to_add_to(
        self: "Self", value: "_2692.MicrophoneArray"
    ) -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_MicrophoneArray.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "MicrophoneArrayToAddTo", value)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    def create_microphone(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateMicrophone")

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CreateMicrophoneNormalToSurfaceOptions":
        """Cast to another type.

        Returns:
            _Cast_CreateMicrophoneNormalToSurfaceOptions
        """
        return _Cast_CreateMicrophoneNormalToSurfaceOptions(self)

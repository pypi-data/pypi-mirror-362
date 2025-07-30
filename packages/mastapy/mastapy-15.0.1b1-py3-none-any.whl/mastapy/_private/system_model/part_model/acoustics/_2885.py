"""ResultSurfaceOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
)
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
from mastapy._private.system_model import _2415
from mastapy._private.system_model.part_model import _2670

_RESULT_SURFACE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "ResultSurfaceOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.part_model.acoustics import _2882, _2883

    Self = TypeVar("Self", bound="ResultSurfaceOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="ResultSurfaceOptions._Cast_ResultSurfaceOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultSurfaceOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultSurfaceOptions:
    """Special nested class for casting ResultSurfaceOptions to subclasses."""

    __parent__: "ResultSurfaceOptions"

    @property
    def result_plane_options(self: "CastSelf") -> "_2882.ResultPlaneOptions":
        from mastapy._private.system_model.part_model.acoustics import _2882

        return self.__parent__._cast(_2882.ResultPlaneOptions)

    @property
    def result_sphere_options(self: "CastSelf") -> "_2883.ResultSphereOptions":
        from mastapy._private.system_model.part_model.acoustics import _2883

        return self.__parent__._cast(_2883.ResultSphereOptions)

    @property
    def result_surface_options(self: "CastSelf") -> "ResultSurfaceOptions":
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
class ResultSurfaceOptions(_0.APIBase):
    """ResultSurfaceOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULT_SURFACE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def reference_component(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Component":
        """ListWithSelectedItem[mastapy.system_model.part_model.Component]"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceComponent")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Component",
        )(temp)

    @reference_component.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_component(self: "Self", value: "_2670.Component") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_Component.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ReferenceComponent", value)

    @property
    @exception_bridge
    def reference_component_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DesignEntityId":
        """EnumWithSelectedValue[mastapy.system_model.DesignEntityId]"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceComponentType")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_DesignEntityId.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @reference_component_type.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_component_type(self: "Self", value: "_2415.DesignEntityId") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DesignEntityId.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ReferenceComponentType", value)

    @property
    @exception_bridge
    def target_edge_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetEdgeLength")

        if temp is None:
            return 0.0

        return temp

    @target_edge_length.setter
    @exception_bridge
    @enforce_parameter_types
    def target_edge_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TargetEdgeLength", float(value) if value is not None else 0.0
        )

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
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

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
    def cast_to(self: "Self") -> "_Cast_ResultSurfaceOptions":
        """Cast to another type.

        Returns:
            _Cast_ResultSurfaceOptions
        """
        return _Cast_ResultSurfaceOptions(self)

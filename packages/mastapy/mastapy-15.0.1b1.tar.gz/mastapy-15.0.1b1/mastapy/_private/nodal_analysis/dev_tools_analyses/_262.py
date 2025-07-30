"""DrawStyleForFE"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item_and_image
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis import _62, _68
from mastapy._private.nodal_analysis.dev_tools_analyses import _275, _281, _282, _287

_DRAW_STYLE_FOR_FE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "DrawStyleForFE"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="DrawStyleForFE")
    CastSelf = TypeVar("CastSelf", bound="DrawStyleForFE._Cast_DrawStyleForFE")


__docformat__ = "restructuredtext en"
__all__ = ("DrawStyleForFE",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DrawStyleForFE:
    """Special nested class for casting DrawStyleForFE to subclasses."""

    __parent__: "DrawStyleForFE"

    @property
    def draw_style_for_fe(self: "CastSelf") -> "DrawStyleForFE":
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
class DrawStyleForFE(_0.APIBase):
    """DrawStyleForFE

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DRAW_STYLE_FOR_FE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def draw_condensation_node_connections(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.NoneSelectedAllOption]"""
        temp = pythonnet_property_get(self.wrapped, "DrawCondensationNodeConnections")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @draw_condensation_node_connections.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_condensation_node_connections(
        self: "Self", value: "_287.NoneSelectedAllOption"
    ) -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DrawCondensationNodeConnections", value)

    @property
    @exception_bridge
    def draw_nodes_connected_to_condensation_nodes(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.NoneSelectedAllOption]"""
        temp = pythonnet_property_get(
            self.wrapped, "DrawNodesConnectedToCondensationNodes"
        )

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @draw_nodes_connected_to_condensation_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_nodes_connected_to_condensation_nodes(
        self: "Self", value: "_287.NoneSelectedAllOption"
    ) -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "DrawNodesConnectedToCondensationNodes", value
        )

    @property
    @exception_bridge
    def draw_search_regions(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.NoneSelectedAllOption]"""
        temp = pythonnet_property_get(self.wrapped, "DrawSearchRegions")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @draw_search_regions.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_search_regions(self: "Self", value: "_287.NoneSelectedAllOption") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_NoneSelectedAllOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DrawSearchRegions", value)

    @property
    @exception_bridge
    def grounded_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "GroundedNodes")

        if temp is None:
            return False

        return temp

    @grounded_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def grounded_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "GroundedNodes", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def highlight_bad_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HighlightBadElements")

        if temp is None:
            return False

        return temp

    @highlight_bad_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def highlight_bad_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HighlightBadElements",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def line_option(self: "Self") -> "_62.FEMeshElementEntityOption":
        """mastapy.nodal_analysis.FEMeshElementEntityOption"""
        temp = pythonnet_property_get(self.wrapped, "LineOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.FEMeshElementEntityOption"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._62", "FEMeshElementEntityOption"
        )(value)

    @line_option.setter
    @exception_bridge
    @enforce_parameter_types
    def line_option(self: "Self", value: "_62.FEMeshElementEntityOption") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.FEMeshElementEntityOption"
        )
        pythonnet_property_set(self.wrapped, "LineOption", value)

    @property
    @exception_bridge
    def mesh(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEMeshElementEntityOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.FEMeshElementEntityOption]"""
        temp = pythonnet_property_get(self.wrapped, "Mesh")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEMeshElementEntityOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def mesh(self: "Self", value: "_62.FEMeshElementEntityOption") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEMeshElementEntityOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Mesh", value)

    @property
    @exception_bridge
    def model_setup_view_type(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEModelSetupViewType":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.FEModelSetupViewType]"""
        temp = pythonnet_property_get(self.wrapped, "ModelSetupViewType")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEModelSetupViewType.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @model_setup_view_type.setter
    @exception_bridge
    @enforce_parameter_types
    def model_setup_view_type(self: "Self", value: "_275.FEModelSetupViewType") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FEModelSetupViewType.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ModelSetupViewType", value)

    @property
    @exception_bridge
    def node_size(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NodeSize")

        if temp is None:
            return 0

        return temp

    @node_size.setter
    @exception_bridge
    @enforce_parameter_types
    def node_size(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NodeSize", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def nodes(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FENodeOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.FENodeOption]"""
        temp = pythonnet_property_get(self.wrapped, "Nodes")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FENodeOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def nodes(self: "Self", value: "_68.FENodeOption") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FENodeOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Nodes", value)

    @property
    @exception_bridge
    def rigid_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RigidElements")

        if temp is None:
            return False

        return temp

    @rigid_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def rigid_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "RigidElements", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def surface(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESurfaceDrawingOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.FESurfaceDrawingOption]"""
        temp = pythonnet_property_get(self.wrapped, "Surface")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESurfaceDrawingOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @surface.setter
    @exception_bridge
    @enforce_parameter_types
    def surface(self: "Self", value: "_282.FESurfaceDrawingOption") -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESurfaceDrawingOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Surface", value)

    @property
    @exception_bridge
    def surface_and_non_deformed_surface(
        self: "Self",
    ) -> "list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESurfaceAndNonDeformedDrawingOption":
        """ListWithSelectedItemAndImage[mastapy.nodal_analysis.dev_tools_analyses.FESurfaceAndNonDeformedDrawingOption]"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceAndNonDeformedSurface")

        if temp is None:
            return None

        value = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESurfaceAndNonDeformedDrawingOption.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @surface_and_non_deformed_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_and_non_deformed_surface(
        self: "Self", value: "_281.FESurfaceAndNonDeformedDrawingOption"
    ) -> None:
        generic_type = list_with_selected_item_and_image.ListWithSelectedItemAndImage_FESurfaceAndNonDeformedDrawingOption.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "SurfaceAndNonDeformedSurface", value)

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
    def cast_to(self: "Self") -> "_Cast_DrawStyleForFE":
        """Cast to another type.

        Returns:
            _Cast_DrawStyleForFE
        """
        return _Cast_DrawStyleForFE(self)

"""FESubstructureExportOptions"""

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
from mastapy._private.nodal_analysis.fe_export_utility import _247
from mastapy._private.utility.units_and_measurements import _1802

_FE_SUBSTRUCTURE_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "FESubstructureExportOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="FESubstructureExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FESubstructureExportOptions._Cast_FESubstructureExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FESubstructureExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FESubstructureExportOptions:
    """Special nested class for casting FESubstructureExportOptions to subclasses."""

    __parent__: "FESubstructureExportOptions"

    @property
    def fe_substructure_export_options(
        self: "CastSelf",
    ) -> "FESubstructureExportOptions":
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
class FESubstructureExportOptions(_0.APIBase):
    """FESubstructureExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_SUBSTRUCTURE_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fe_export_file_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FESubstructuringFileFormat":
        """EnumWithSelectedValue[mastapy.nodal_analysis.fe_export_utility.FESubstructuringFileFormat]"""
        temp = pythonnet_property_get(self.wrapped, "FEExportFileType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FESubstructuringFileFormat.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @fe_export_file_type.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_export_file_type(
        self: "Self", value: "_247.FESubstructuringFileFormat"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FESubstructuringFileFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FEExportFileType", value)

    @property
    @exception_bridge
    def force_unit(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "ForceUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @force_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def force_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ForceUnit", value)

    @property
    @exception_bridge
    def include_condensation_node_displacement_expansion(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeCondensationNodeDisplacementExpansion"
        )

        if temp is None:
            return False

        return temp

    @include_condensation_node_displacement_expansion.setter
    @exception_bridge
    @enforce_parameter_types
    def include_condensation_node_displacement_expansion(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeCondensationNodeDisplacementExpansion",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_fe_mesh_definition(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeFEMeshDefinition")

        if temp is None:
            return False

        return temp

    @include_fe_mesh_definition.setter
    @exception_bridge
    @enforce_parameter_types
    def include_fe_mesh_definition(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeFEMeshDefinition",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_reduced_gravity_load(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeReducedGravityLoad")

        if temp is None:
            return False

        return temp

    @include_reduced_gravity_load.setter
    @exception_bridge
    @enforce_parameter_types
    def include_reduced_gravity_load(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeReducedGravityLoad",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_reduced_thermal_expansion_force(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeReducedThermalExpansionForce"
        )

        if temp is None:
            return False

        return temp

    @include_reduced_thermal_expansion_force.setter
    @exception_bridge
    @enforce_parameter_types
    def include_reduced_thermal_expansion_force(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeReducedThermalExpansionForce",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_reduction_commands(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeReductionCommands")

        if temp is None:
            return False

        return temp

    @include_reduction_commands.setter
    @exception_bridge
    @enforce_parameter_types
    def include_reduction_commands(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeReductionCommands",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeRigidCouplingNodesAndConstraintsAddedByMASTA"
        )

        if temp is None:
            return False

        return temp

    @include_rigid_coupling_nodes_and_constraints_added_by_masta.setter
    @exception_bridge
    @enforce_parameter_types
    def include_rigid_coupling_nodes_and_constraints_added_by_masta(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeRigidCouplingNodesAndConstraintsAddedByMASTA",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def length_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "LengthUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @length_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def length_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "LengthUnit", value)

    @property
    @exception_bridge
    def warning_about_gear_teeth_for_export(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WarningAboutGearTeethForExport")

        if temp is None:
            return ""

        return temp

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
    def export_to_file(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "ExportToFile", file_path)

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
    def cast_to(self: "Self") -> "_Cast_FESubstructureExportOptions":
        """Cast to another type.

        Returns:
            _Cast_FESubstructureExportOptions
        """
        return _Cast_FESubstructureExportOptions(self)

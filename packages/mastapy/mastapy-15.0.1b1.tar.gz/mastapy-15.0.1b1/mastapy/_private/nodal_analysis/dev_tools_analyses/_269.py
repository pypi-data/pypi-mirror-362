"""FEModel"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_FE_MODEL = python_net_import("SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FEModel")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis.dev_tools_analyses import _274, _284
    from mastapy._private.nodal_analysis.dev_tools_analyses.full_fe_reporting import (
        _289,
        _290,
        _293,
        _294,
        _295,
        _296,
        _297,
        _298,
        _299,
        _300,
        _301,
        _303,
        _304,
    )

    Self = TypeVar("Self", bound="FEModel")
    CastSelf = TypeVar("CastSelf", bound="FEModel._Cast_FEModel")


__docformat__ = "restructuredtext en"
__all__ = ("FEModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEModel:
    """Special nested class for casting FEModel to subclasses."""

    __parent__: "FEModel"

    @property
    def fe_model(self: "CastSelf") -> "FEModel":
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
class FEModel(_0.APIBase):
    """FEModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def edge_angle_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeAngleTolerance")

        if temp is None:
            return 0.0

        return temp

    @edge_angle_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_angle_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EdgeAngleTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def exclude_nodes_connected_to_condensation_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "ExcludeNodesConnectedToCondensationNodes"
        )

        if temp is None:
            return False

        return temp

    @exclude_nodes_connected_to_condensation_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def exclude_nodes_connected_to_condensation_nodes(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExcludeNodesConnectedToCondensationNodes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def model_force_unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelForceUnit")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def model_length_unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelLengthUnit")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def model_splitting_method(self: "Self") -> "_284.ModelSplittingMethod":
        """mastapy.nodal_analysis.dev_tools_analyses.ModelSplittingMethod"""
        temp = pythonnet_property_get(self.wrapped, "ModelSplittingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.ModelSplittingMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.dev_tools_analyses._284",
            "ModelSplittingMethod",
        )(value)

    @model_splitting_method.setter
    @exception_bridge
    @enforce_parameter_types
    def model_splitting_method(
        self: "Self", value: "_284.ModelSplittingMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.ModelSplittingMethod"
        )
        pythonnet_property_set(self.wrapped, "ModelSplittingMethod", value)

    @property
    @exception_bridge
    def number_of_elements(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfElements")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_elements_with_negative_jacobian(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfElementsWithNegativeJacobian"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_elements_with_negative_size(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfElementsWithNegativeSize")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_nodes(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfNodes")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def original_file_path(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OriginalFilePath")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def use_contact_pairs_for_boundary(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseContactPairsForBoundary")

        if temp is None:
            return False

        return temp

    @use_contact_pairs_for_boundary.setter
    @exception_bridge
    @enforce_parameter_types
    def use_contact_pairs_for_boundary(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseContactPairsForBoundary",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_multipoint_constraints_for_boundary(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseMultipointConstraintsForBoundary"
        )

        if temp is None:
            return False

        return temp

    @use_multipoint_constraints_for_boundary.setter
    @exception_bridge
    @enforce_parameter_types
    def use_multipoint_constraints_for_boundary(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseMultipointConstraintsForBoundary",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_rigid_elements_for_boundary(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseRigidElementsForBoundary")

        if temp is None:
            return False

        return temp

    @use_rigid_elements_for_boundary.setter
    @exception_bridge
    @enforce_parameter_types
    def use_rigid_elements_for_boundary(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseRigidElementsForBoundary",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_simplified_normal_calculation_when_deformed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UseSimplifiedNormalCalculationWhenDeformed"
        )

        if temp is None:
            return False

        return temp

    @use_simplified_normal_calculation_when_deformed.setter
    @exception_bridge
    @enforce_parameter_types
    def use_simplified_normal_calculation_when_deformed(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseSimplifiedNormalCalculationWhenDeformed",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def beam_element_properties(self: "Self") -> "List[_295.ElementPropertiesBeam]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesBeam]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BeamElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_pairs(self: "Self") -> "List[_289.ContactPairReporting]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ContactPairReporting]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPairs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def coordinate_systems(self: "Self") -> "List[_290.CoordinateSystemReporting]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.CoordinateSystemReporting]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystems")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def interface_element_properties(
        self: "Self",
    ) -> "List[_296.ElementPropertiesInterface]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesInterface]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InterfaceElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mass_element_properties(self: "Self") -> "List[_297.ElementPropertiesMass]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesMass]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MassElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def materials(self: "Self") -> "List[_303.MaterialPropertiesReporting]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.MaterialPropertiesReporting]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Materials")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def model_parts(self: "Self") -> "List[_274.FEModelPart]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.FEModelPart]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModelParts")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def other_element_properties(self: "Self") -> "List[_294.ElementPropertiesBase]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesBase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OtherElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rigid_element_properties(self: "Self") -> "List[_298.ElementPropertiesRigid]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesRigid]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RigidElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shell_element_properties(self: "Self") -> "List[_299.ElementPropertiesShell]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesShell]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShellElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def solid_element_properties(self: "Self") -> "List[_300.ElementPropertiesSolid]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesSolid]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SolidElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def spring_dashpot_element_properties(
        self: "Self",
    ) -> "List[_301.ElementPropertiesSpringDashpot]":
        """List[mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementPropertiesSpringDashpot]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpringDashpotElementProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def add_new_material(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddNewMaterial")

    @exception_bridge
    def change_interpolation_constraints_to_distributing(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ChangeInterpolationConstraintsToDistributing"
        )

    @exception_bridge
    def delete_unused_element_properties(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteUnusedElementProperties")

    @exception_bridge
    def delete_unused_materials(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "DeleteUnusedMaterials")

    @exception_bridge
    def get_all_element_details(self: "Self") -> "_293.ElementDetailsForFEModel":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.ElementDetailsForFEModel"""
        method_result = pythonnet_method_call(self.wrapped, "GetAllElementDetails")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def get_all_node_details(self: "Self") -> "_304.NodeDetailsForFEModel":
        """mastapy.nodal_analysis.dev_tools_analyses.full_fe_reporting.NodeDetailsForFEModel"""
        method_result = pythonnet_method_call(self.wrapped, "GetAllNodeDetails")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

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
    def cast_to(self: "Self") -> "_Cast_FEModel":
        """Cast to another type.

        Returns:
            _Cast_FEModel
        """
        return _Cast_FEModel(self)

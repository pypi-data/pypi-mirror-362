"""MASTAGUI"""

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
from mastapy._private._math.color import Color
from mastapy._private._math.vector_3d import Vector3D
from mastapy._private.nodal_analysis.geometry_modeller_link import _234

_MASTAGUI = python_net_import("SMT.MastaAPI.SystemModelGUI", "MASTAGUI")

if TYPE_CHECKING:
    from typing import Any, Dict, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.geometry.two_d import _400
    from mastapy._private.math_utility import _1677, _1695
    from mastapy._private.nodal_analysis.geometry_modeller_link import (
        _230,
        _233,
        _241,
        _242,
    )
    from mastapy._private.shafts import _31
    from mastapy._private.system_model import _2411, _2414
    from mastapy._private.utility.operation_modes import _1985

    Self = TypeVar("Self", bound="MASTAGUI")
    CastSelf = TypeVar("CastSelf", bound="MASTAGUI._Cast_MASTAGUI")


__docformat__ = "restructuredtext en"
__all__ = ("MASTAGUI",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MASTAGUI:
    """Special nested class for casting MASTAGUI to subclasses."""

    __parent__: "MASTAGUI"

    @property
    def mastagui(self: "CastSelf") -> "MASTAGUI":
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
class MASTAGUI(_0.APIBase):
    """MASTAGUI

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MASTAGUI

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_initialised(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsInitialised")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def is_paused(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsPaused")

        if temp is None:
            return False

        return temp

    @is_paused.setter
    @exception_bridge
    @enforce_parameter_types
    def is_paused(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsPaused", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def is_remoting(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsRemoting")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def active_design(self: "Self") -> "_2411.Design":
        """mastapy.system_model.Design"""
        temp = pythonnet_property_get(self.wrapped, "ActiveDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @active_design.setter
    @exception_bridge
    @enforce_parameter_types
    def active_design(self: "Self", value: "_2411.Design") -> None:
        pythonnet_property_set(self.wrapped, "ActiveDesign", value.wrapped)

    @property
    @exception_bridge
    def can_use_auto_method_for_component_import(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CanUseAutoMethodForComponentImport"
        )

        if temp is None:
            return False

        return temp

    @can_use_auto_method_for_component_import.setter
    @exception_bridge
    @enforce_parameter_types
    def can_use_auto_method_for_component_import(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CanUseAutoMethodForComponentImport",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def clear_component_profile_lines(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ClearComponentProfileLines")

        if temp is None:
            return False

        return temp

    @clear_component_profile_lines.setter
    @exception_bridge
    @enforce_parameter_types
    def clear_component_profile_lines(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClearComponentProfileLines",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def clear_component_selection(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ClearComponentSelection")

        if temp is None:
            return False

        return temp

    @clear_component_selection.setter
    @exception_bridge
    @enforce_parameter_types
    def clear_component_selection(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ClearComponentSelection",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def color_of_new_problem_node_group(self: "Self") -> "Color":
        """Color"""
        temp = pythonnet_property_get(self.wrapped, "ColorOfNewProblemNodeGroup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_color(temp)

        if value is None:
            return None

        return value

    @color_of_new_problem_node_group.setter
    @exception_bridge
    @enforce_parameter_types
    def color_of_new_problem_node_group(self: "Self", value: "Color") -> None:
        value = conversion.mp_to_pn_color(value)
        pythonnet_property_set(self.wrapped, "ColorOfNewProblemNodeGroup", value)

    @property
    @exception_bridge
    def gear_tip_radius_clash_test_request(
        self: "Self",
    ) -> "_230.GearTipRadiusClashTest":
        """mastapy.nodal_analysis.geometry_modeller_link.GearTipRadiusClashTest"""
        temp = pythonnet_property_get(self.wrapped, "GearTipRadiusClashTestRequest")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @gear_tip_radius_clash_test_request.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_tip_radius_clash_test_request(
        self: "Self", value: "_230.GearTipRadiusClashTest"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "GearTipRadiusClashTestRequest", value.wrapped
        )

    @property
    @exception_bridge
    def geometry_modeller_file_path_to_open(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerFilePathToOpen")

        if temp is None:
            return ""

        return temp

    @geometry_modeller_file_path_to_open.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_modeller_file_path_to_open(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeometryModellerFilePathToOpen",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def geometry_modeller_process_id(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerProcessID")

        if temp is None:
            return 0

        return temp

    @geometry_modeller_process_id.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_modeller_process_id(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GeometryModellerProcessID",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def in_dxf_line_select_mode(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "InDxfLineSelectMode")

        if temp is None:
            return False

        return temp

    @in_dxf_line_select_mode.setter
    @exception_bridge
    @enforce_parameter_types
    def in_dxf_line_select_mode(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InDxfLineSelectMode",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_connected_to_geometry_modeller(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsConnectedToGeometryModeller")

        if temp is None:
            return False

        return temp

    @is_connected_to_geometry_modeller.setter
    @exception_bridge
    @enforce_parameter_types
    def is_connected_to_geometry_modeller(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsConnectedToGeometryModeller",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def name_of_new_problem_node_group(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "NameOfNewProblemNodeGroup")

        if temp is None:
            return ""

        return temp

    @name_of_new_problem_node_group.setter
    @exception_bridge
    @enforce_parameter_types
    def name_of_new_problem_node_group(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NameOfNewProblemNodeGroup",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def open_designs(self: "Self") -> "List[_2411.Design]":
        """List[mastapy.system_model.Design]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def operation_mode(self: "Self") -> "_1985.OperationMode":
        """mastapy.utility.operation_modes.OperationMode"""
        temp = pythonnet_property_get(self.wrapped, "OperationMode")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.OperationModes.OperationMode"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.operation_modes._1985", "OperationMode"
        )(value)

    @operation_mode.setter
    @exception_bridge
    @enforce_parameter_types
    def operation_mode(self: "Self", value: "_1985.OperationMode") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.OperationModes.OperationMode"
        )
        pythonnet_property_set(self.wrapped, "OperationMode", value)

    @property
    @exception_bridge
    def positions_of_problem_node_group(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionsOfProblemNodeGroup")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def process_id(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProcessId")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def profile_for_geometry_modeller(self: "Self") -> "_31.ShaftProfileFromImport":
        """mastapy.shafts.ShaftProfileFromImport"""
        temp = pythonnet_property_get(self.wrapped, "ProfileForGeometryModeller")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @profile_for_geometry_modeller.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_for_geometry_modeller(
        self: "Self", value: "_31.ShaftProfileFromImport"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "ProfileForGeometryModeller", value.wrapped
        )

    @property
    @exception_bridge
    def restart_geometry_modeller_flag(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RestartGeometryModellerFlag")

        if temp is None:
            return False

        return temp

    @restart_geometry_modeller_flag.setter
    @exception_bridge
    @enforce_parameter_types
    def restart_geometry_modeller_flag(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RestartGeometryModellerFlag",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def restart_geometry_modeller_save_file(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "RestartGeometryModellerSaveFile")

        if temp is None:
            return ""

        return temp

    @restart_geometry_modeller_save_file.setter
    @exception_bridge
    @enforce_parameter_types
    def restart_geometry_modeller_save_file(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RestartGeometryModellerSaveFile",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def selected_design_entity(self: "Self") -> "_2414.DesignEntity":
        """mastapy.system_model.DesignEntity"""
        temp = pythonnet_property_get(self.wrapped, "SelectedDesignEntity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @selected_design_entity.setter
    @exception_bridge
    @enforce_parameter_types
    def selected_design_entity(self: "Self", value: "_2414.DesignEntity") -> None:
        pythonnet_property_set(self.wrapped, "SelectedDesignEntity", value.wrapped)

    @property
    @exception_bridge
    def text_for_manual_component_import(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "TextForManualComponentImport")

        if temp is None:
            return ""

        return temp

    @text_for_manual_component_import.setter
    @exception_bridge
    @enforce_parameter_types
    def text_for_manual_component_import(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TextForManualComponentImport",
            str(value) if value is not None else "",
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

    @staticmethod
    @exception_bridge
    @enforce_parameter_types
    def get_mastagui(process_id: "int") -> "MASTAGUI":
        """mastapy.system_model_gui.MASTAGUI

        Args:
            process_id (int)
        """
        process_id = int(process_id)
        method_result = pythonnet_method_call(
            MASTAGUI.TYPE, "GetMASTAGUI", process_id if process_id else 0
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def pause(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Pause")

    @exception_bridge
    def resume(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Resume")

    @exception_bridge
    def start_remoting(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "StartRemoting")

    @exception_bridge
    def stop_remoting(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "StopRemoting")

    @exception_bridge
    def aborted(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Aborted")

    @exception_bridge
    @enforce_parameter_types
    def add_electric_machine_from_cad_face_group(
        self: "Self",
        cad_face_group: "_400.CADFaceGroup",
        geometry_modeller_design_information: "_233.GeometryModellerDesignInformation",
        dimensions: "Dict[str, _234.GeometryModellerDimension]",
    ) -> None:
        """Method does not return.

        Args:
            cad_face_group (mastapy.geometry.two_d.CADFaceGroup)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """
        pythonnet_method_call(
            self.wrapped,
            "AddElectricMachineFromCADFaceGroup",
            cad_face_group.wrapped if cad_face_group else None,
            geometry_modeller_design_information.wrapped
            if geometry_modeller_design_information
            else None,
            dimensions,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_fe_substructure_from_data(
        self: "Self",
        vertices_and_facets: "_1695.FacetedBody",
        geometry_modeller_design_information: "_233.GeometryModellerDesignInformation",
        dimensions: "Dict[str, _234.GeometryModellerDimension]",
        body_monikers: "List[str]",
    ) -> None:
        """Method does not return.

        Args:
            vertices_and_facets (mastapy.math_utility.FacetedBody)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
            body_monikers (List[str])
        """
        body_monikers = conversion.mp_to_pn_objects_in_dotnet_list(body_monikers)
        pythonnet_method_call(
            self.wrapped,
            "AddFESubstructureFromData",
            vertices_and_facets.wrapped if vertices_and_facets else None,
            geometry_modeller_design_information.wrapped
            if geometry_modeller_design_information
            else None,
            dimensions,
            body_monikers,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_fe_substructure_from_file(
        self: "Self",
        length_scale: "float",
        stl_file_name: "str",
        geometry_modeller_design_information: "_233.GeometryModellerDesignInformation",
        dimensions: "Dict[str, _234.GeometryModellerDimension]",
    ) -> None:
        """Method does not return.

        Args:
            length_scale (float)
            stl_file_name (str)
            geometry_modeller_design_information (mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation)
            dimensions (Dict[str, mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension])
        """
        length_scale = float(length_scale)
        stl_file_name = str(stl_file_name)
        pythonnet_method_call(
            self.wrapped,
            "AddFESubstructureFromFile",
            length_scale if length_scale else 0.0,
            stl_file_name if stl_file_name else "",
            geometry_modeller_design_information.wrapped
            if geometry_modeller_design_information
            else None,
            dimensions,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_line_from_geometry_modeller(
        self: "Self", circles_on_axis: "_1677.CirclesOnAxis"
    ) -> None:
        """Method does not return.

        Args:
            circles_on_axis (mastapy.math_utility.CirclesOnAxis)
        """
        pythonnet_method_call(
            self.wrapped,
            "AddLineFromGeometryModeller",
            circles_on_axis.wrapped if circles_on_axis else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def add_shaft_from_geometry_modeller(
        self: "Self",
        imported_profile_without_features: "_31.ShaftProfileFromImport",
        imported_profile_with_features: "_31.ShaftProfileFromImport",
    ) -> None:
        """Method does not return.

        Args:
            imported_profile_without_features (mastapy.shafts.ShaftProfileFromImport)
            imported_profile_with_features (mastapy.shafts.ShaftProfileFromImport)
        """
        pythonnet_method_call(
            self.wrapped,
            "AddShaftFromGeometryModeller",
            imported_profile_without_features.wrapped
            if imported_profile_without_features
            else None,
            imported_profile_with_features.wrapped
            if imported_profile_with_features
            else None,
        )

    @exception_bridge
    def are_new_input_available(self: "Self") -> "_241.MeshRequest":
        """mastapy.nodal_analysis.geometry_modeller_link.MeshRequest"""
        method_result = pythonnet_method_call(self.wrapped, "AreNewInputAvailable")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def circle_pairs_from_geometry_modeller(
        self: "Self",
        preselection_circles: "_1677.CirclesOnAxis",
        selected_circles: "List[_1677.CirclesOnAxis]",
    ) -> None:
        """Method does not return.

        Args:
            preselection_circles (mastapy.math_utility.CirclesOnAxis)
            selected_circles (List[mastapy.math_utility.CirclesOnAxis])
        """
        selected_circles = conversion.mp_to_pn_objects_in_list(selected_circles)
        pythonnet_method_call(
            self.wrapped,
            "CirclePairsFromGeometryModeller",
            preselection_circles.wrapped if preselection_circles else None,
            selected_circles,
        )

    @exception_bridge
    @enforce_parameter_types
    def create_geometry_modeller_design_information(
        self: "Self", file_name: "PathLike", main_part_moniker: "str", tab_name: "str"
    ) -> "_233.GeometryModellerDesignInformation":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation

        Args:
            file_name (PathLike)
            main_part_moniker (str)
            tab_name (str)
        """
        file_name = str(file_name)
        main_part_moniker = str(main_part_moniker)
        tab_name = str(tab_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "CreateGeometryModellerDesignInformation",
            file_name,
            main_part_moniker if main_part_moniker else "",
            tab_name if tab_name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_geometry_modeller_dimension(
        self: "Self",
    ) -> "_234.GeometryModellerDimension":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDimension"""
        method_result = pythonnet_method_call(
            self.wrapped, "CreateGeometryModellerDimension"
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_mesh_request_result(self: "Self") -> "_242.MeshRequestResult":
        """mastapy.nodal_analysis.geometry_modeller_link.MeshRequestResult"""
        method_result = pythonnet_method_call(self.wrapped, "CreateMeshRequestResult")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_new_cad_face_group(self: "Self") -> "_400.CADFaceGroup":
        """mastapy.geometry.two_d.CADFaceGroup"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewCADFaceGroup")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_new_circles_on_axis(self: "Self") -> "_1677.CirclesOnAxis":
        """mastapy.math_utility.CirclesOnAxis"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewCirclesOnAxis")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def create_new_faceted_body(self: "Self") -> "_1695.FacetedBody":
        """mastapy.math_utility.FacetedBody"""
        method_result = pythonnet_method_call(self.wrapped, "CreateNewFacetedBody")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def create_shaft_profile_from_import(
        self: "Self", moniker: "str", window_name: "str"
    ) -> "_31.ShaftProfileFromImport":
        """mastapy.shafts.ShaftProfileFromImport

        Args:
            moniker (str)
            window_name (str)
        """
        moniker = str(moniker)
        window_name = str(window_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "CreateShaftProfileFromImport",
            moniker if moniker else "",
            window_name if window_name else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def flag_message_received(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "FlagMessageReceived")

    @exception_bridge
    def geometry_modeller_document_loaded(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "GeometryModellerDocumentLoaded")

    @exception_bridge
    @enforce_parameter_types
    def move_selected_component(
        self: "Self", origin: "Vector3D", axis: "Vector3D"
    ) -> None:
        """Method does not return.

        Args:
            origin (Vector3D)
            axis (Vector3D)
        """
        origin = conversion.mp_to_pn_vector3d(origin)
        axis = conversion.mp_to_pn_vector3d(axis)
        pythonnet_method_call(self.wrapped, "MoveSelectedComponent", origin, axis)

    @exception_bridge
    @enforce_parameter_types
    def open_design_in_new_tab(self: "Self", design: "_2411.Design") -> None:
        """Method does not return.

        Args:
            design (mastapy.system_model.Design)
        """
        pythonnet_method_call(
            self.wrapped, "OpenDesignInNewTab", design.wrapped if design else None
        )

    @exception_bridge
    @enforce_parameter_types
    def run_command(self: "Self", command: "str") -> None:
        """Method does not return.

        Args:
            command (str)
        """
        command = str(command)
        pythonnet_method_call(self.wrapped, "RunCommand", command if command else "")

    @exception_bridge
    @enforce_parameter_types
    def save_active_report(self: "Self", file: "str") -> None:
        """Method does not return.

        Args:
            file (str)
        """
        file = str(file)
        pythonnet_method_call(self.wrapped, "SaveActiveReport", file if file else "")

    @exception_bridge
    @enforce_parameter_types
    def select_tab(self: "Self", tab_text: "str") -> None:
        """Method does not return.

        Args:
            tab_text (str)
        """
        tab_text = str(tab_text)
        pythonnet_method_call(self.wrapped, "SelectTab", tab_text if tab_text else "")

    @exception_bridge
    @enforce_parameter_types
    def set_error(self: "Self", error: "str") -> None:
        """Method does not return.

        Args:
            error (str)
        """
        error = str(error)
        pythonnet_method_call(self.wrapped, "SetError", error if error else "")

    @exception_bridge
    @enforce_parameter_types
    def set_gear_tip_diameter_clash_test_result(
        self: "Self", result: "_230.GearTipRadiusClashTest"
    ) -> None:
        """Method does not return.

        Args:
            result (mastapy.nodal_analysis.geometry_modeller_link.GearTipRadiusClashTest)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetGearTipDiameterClashTestResult",
            result.wrapped if result else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_mesh_request_result(
        self: "Self", mesh_request_result: "_242.MeshRequestResult"
    ) -> None:
        """Method does not return.

        Args:
            mesh_request_result (mastapy.nodal_analysis.geometry_modeller_link.MeshRequestResult)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetMeshRequestResult",
            mesh_request_result.wrapped if mesh_request_result else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def show_boxes(
        self: "Self",
        small_box_corners: "List[Vector3D]",
        big_box_corners: "List[Vector3D]",
    ) -> None:
        """Method does not return.

        Args:
            small_box_corners (List[Vector3D])
            big_box_corners (List[Vector3D])
        """
        small_box_corners = conversion.mp_to_pn_objects_in_list(small_box_corners)
        big_box_corners = conversion.mp_to_pn_objects_in_list(big_box_corners)
        pythonnet_method_call(
            self.wrapped, "ShowBoxes", small_box_corners, big_box_corners
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
    def cast_to(self: "Self") -> "_Cast_MASTAGUI":
        """Cast to another type.

        Returns:
            _Cast_MASTAGUI
        """
        return _Cast_MASTAGUI(self)

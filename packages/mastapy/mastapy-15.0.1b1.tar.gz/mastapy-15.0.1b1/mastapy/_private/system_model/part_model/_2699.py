"""PartModelExportPanelOptions"""

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
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model.gears import _2780
from mastapy._private.utility.cad_export import _2035

_PART_MODEL_EXPORT_PANEL_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "PartModelExportPanelOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="PartModelExportPanelOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PartModelExportPanelOptions._Cast_PartModelExportPanelOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PartModelExportPanelOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PartModelExportPanelOptions:
    """Special nested class for casting PartModelExportPanelOptions to subclasses."""

    __parent__: "PartModelExportPanelOptions"

    @property
    def part_model_export_panel_options(
        self: "CastSelf",
    ) -> "PartModelExportPanelOptions":
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
class PartModelExportPanelOptions(_0.APIBase):
    """PartModelExportPanelOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PART_MODEL_EXPORT_PANEL_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auto_cad_version_dxf_dwg(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DxfVersionWithName":
        """EnumWithSelectedValue[mastapy.utility.cad_export.DxfVersionWithName]"""
        temp = pythonnet_property_get(self.wrapped, "AutoCADVersionDxfDwg")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DxfVersionWithName.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @auto_cad_version_dxf_dwg.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_cad_version_dxf_dwg(
        self: "Self", value: "_2035.DxfVersionWithName"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DxfVersionWithName.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "AutoCADVersionDxfDwg", value)

    @property
    @exception_bridge
    def draw_gear_teeth(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawGearTeeth")

        if temp is None:
            return False

        return temp

    @draw_gear_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_gear_teeth(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawGearTeeth", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def export_single_tooth_surface(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ExportSingleToothSurface")

        if temp is None:
            return False

        return temp

    @export_single_tooth_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def export_single_tooth_surface(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExportSingleToothSurface",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def gear_export_mode_dxf_dwg(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ProfileToothDrawingMethod":
        """EnumWithSelectedValue[mastapy.system_model.part_model.gears.ProfileToothDrawingMethod]"""
        temp = pythonnet_property_get(self.wrapped, "GearExportModeDxfDwg")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ProfileToothDrawingMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @gear_export_mode_dxf_dwg.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_export_mode_dxf_dwg(
        self: "Self", value: "_2780.ProfileToothDrawingMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ProfileToothDrawingMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "GearExportModeDxfDwg", value)

    @property
    @exception_bridge
    def include_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMicroGeometry")

        if temp is None:
            return False

        return temp

    @include_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def include_micro_geometry(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeMicroGeometry",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_planetary_duplicates(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludePlanetaryDuplicates")

        if temp is None:
            return False

        return temp

    @include_planetary_duplicates.setter
    @exception_bridge
    @enforce_parameter_types
    def include_planetary_duplicates(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludePlanetaryDuplicates",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_shaft_fillets(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeShaftFillets")

        if temp is None:
            return False

        return temp

    @include_shaft_fillets.setter
    @exception_bridge
    @enforce_parameter_types
    def include_shaft_fillets(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeShaftFillets",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_virtual_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeVirtualComponents")

        if temp is None:
            return False

        return temp

    @include_virtual_components.setter
    @exception_bridge
    @enforce_parameter_types
    def include_virtual_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeVirtualComponents",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def nurbs_degree(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NURBSDegree")

        if temp is None:
            return 0

        return temp

    @nurbs_degree.setter
    @exception_bridge
    @enforce_parameter_types
    def nurbs_degree(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NURBSDegree", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_face_width_points(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfFaceWidthPoints")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_face_width_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_face_width_points(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfFaceWidthPoints", value)

    @property
    @exception_bridge
    def number_of_points_per_cycloidal_disc_half_lobe_profile(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsPerCycloidalDiscHalfLobeProfile"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_per_cycloidal_disc_half_lobe_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_per_cycloidal_disc_half_lobe_profile(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsPerCycloidalDiscHalfLobeProfile",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_profile_points(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfProfilePoints")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_profile_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_profile_points(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfProfilePoints", value)

    @property
    @exception_bridge
    def smooth_root_fillet_flank_boundary_with_micro_geometry(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SmoothRootFilletFlankBoundaryWithMicroGeometry"
        )

        if temp is None:
            return False

        return temp

    @smooth_root_fillet_flank_boundary_with_micro_geometry.setter
    @exception_bridge
    @enforce_parameter_types
    def smooth_root_fillet_flank_boundary_with_micro_geometry(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SmoothRootFilletFlankBoundaryWithMicroGeometry",
            bool(value) if value is not None else False,
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
    def cast_to(self: "Self") -> "_Cast_PartModelExportPanelOptions":
        """Cast to another type.

        Returns:
            _Cast_PartModelExportPanelOptions
        """
        return _Cast_PartModelExportPanelOptions(self)

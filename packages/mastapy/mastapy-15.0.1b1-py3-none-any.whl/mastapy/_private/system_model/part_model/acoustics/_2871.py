"""AcousticInputSurfaceOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_ACOUSTIC_INPUT_SURFACE_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "AcousticInputSurfaceOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.part_model.acoustics import _2873, _2875

    Self = TypeVar("Self", bound="AcousticInputSurfaceOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AcousticInputSurfaceOptions._Cast_AcousticInputSurfaceOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticInputSurfaceOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AcousticInputSurfaceOptions:
    """Special nested class for casting AcousticInputSurfaceOptions to subclasses."""

    __parent__: "AcousticInputSurfaceOptions"

    @property
    def acoustic_input_surface_options(
        self: "CastSelf",
    ) -> "AcousticInputSurfaceOptions":
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
class AcousticInputSurfaceOptions(_0.APIBase):
    """AcousticInputSurfaceOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ACOUSTIC_INPUT_SURFACE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_element_size(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageElementSize")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def check_for_closed_input_surface(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CheckForClosedInputSurface")

        if temp is None:
            return False

        return temp

    @check_for_closed_input_surface.setter
    @exception_bridge
    @enforce_parameter_types
    def check_for_closed_input_surface(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CheckForClosedInputSurface",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def display_hole_id_labels(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DisplayHoleIDLabels")

        if temp is None:
            return False

        return temp

    @display_hole_id_labels.setter
    @exception_bridge
    @enforce_parameter_types
    def display_hole_id_labels(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DisplayHoleIDLabels",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def element_size_for_holes(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSizeForHoles")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_size_for_holes.setter
    @exception_bridge
    @enforce_parameter_types
    def element_size_for_holes(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSizeForHoles", value)

    @property
    @exception_bridge
    def highlight_free_edges(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HighlightFreeEdges")

        if temp is None:
            return False

        return temp

    @highlight_free_edges.setter
    @exception_bridge
    @enforce_parameter_types
    def highlight_free_edges(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HighlightFreeEdges",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_midside_nodes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeMidsideNodes")

        if temp is None:
            return False

        return temp

    @include_midside_nodes.setter
    @exception_bridge
    @enforce_parameter_types
    def include_midside_nodes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeMidsideNodes",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def manually_select_holes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ManuallySelectHoles")

        if temp is None:
            return False

        return temp

    @manually_select_holes.setter
    @exception_bridge
    @enforce_parameter_types
    def manually_select_holes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ManuallySelectHoles",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_hole_diameter_to_fill(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumHoleDiameterToFill")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_hole_diameter_to_fill.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_hole_diameter_to_fill(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumHoleDiameterToFill", value)

    @property
    @exception_bridge
    def mesh_frequency_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshFrequencyLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_diameter_for_manual_hole_selection(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumDiameterForManualHoleSelection"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_diameter_for_manual_hole_selection.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_diameter_for_manual_hole_selection(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MinimumDiameterForManualHoleSelection", value
        )

    @property
    @exception_bridge
    def number_of_degrees_of_freedom(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfDegreesOfFreedom")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def fe_part_options(self: "Self") -> "List[_2873.FEPartInputSurfaceOptions]":
        """List[mastapy.system_model.part_model.acoustics.FEPartInputSurfaceOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEPartOptions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hole_meshes(self: "Self") -> "List[_2875.HoleInFaceGroup]":
        """List[mastapy.system_model.part_model.acoustics.HoleInFaceGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HoleMeshes")

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
    def exclude_all_hole_meshes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExcludeAllHoleMeshes")

    @exception_bridge
    def include_all_hole_meshes(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "IncludeAllHoleMeshes")

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
    def cast_to(self: "Self") -> "_Cast_AcousticInputSurfaceOptions":
        """Cast to another type.

        Returns:
            _Cast_AcousticInputSurfaceOptions
        """
        return _Cast_AcousticInputSurfaceOptions(self)

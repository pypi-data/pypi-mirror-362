"""GeometryExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
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

_GEOMETRY_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.ImportExport", "GeometryExportOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="GeometryExportOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="GeometryExportOptions._Cast_GeometryExportOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryExportOptions:
    """Special nested class for casting GeometryExportOptions to subclasses."""

    __parent__: "GeometryExportOptions"

    @property
    def geometry_export_options(self: "CastSelf") -> "GeometryExportOptions":
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
class GeometryExportOptions(_0.APIBase):
    """GeometryExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def create_solid(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CreateSolid")

        if temp is None:
            return False

        return temp

    @create_solid.setter
    @exception_bridge
    @enforce_parameter_types
    def create_solid(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CreateSolid", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def draw_fillets(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawFillets")

        if temp is None:
            return False

        return temp

    @draw_fillets.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_fillets(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "DrawFillets", bool(value) if value is not None else False
        )

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
    def draw_to_tip_diameter(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "DrawToTipDiameter")

        if temp is None:
            return False

        return temp

    @draw_to_tip_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def draw_to_tip_diameter(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawToTipDiameter",
            bool(value) if value is not None else False,
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
    def include_bearing_cage(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingCage")

        if temp is None:
            return False

        return temp

    @include_bearing_cage.setter
    @exception_bridge
    @enforce_parameter_types
    def include_bearing_cage(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingCage",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_bearing_elements(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingElements")

        if temp is None:
            return False

        return temp

    @include_bearing_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def include_bearing_elements(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingElements",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_bearing_inner_race(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingInnerRace")

        if temp is None:
            return False

        return temp

    @include_bearing_inner_race.setter
    @exception_bridge
    @enforce_parameter_types
    def include_bearing_inner_race(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingInnerRace",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_bearing_outer_race(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeBearingOuterRace")

        if temp is None:
            return False

        return temp

    @include_bearing_outer_race.setter
    @exception_bridge
    @enforce_parameter_types
    def include_bearing_outer_race(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeBearingOuterRace",
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
    def number_of_face_width_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfFaceWidthPoints")

        if temp is None:
            return 0

        return temp

    @number_of_face_width_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_face_width_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfFaceWidthPoints",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_points_per_cycloidal_disc_half_lobe(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPointsPerCycloidalDiscHalfLobe"
        )

        if temp is None:
            return 0

        return temp

    @number_of_points_per_cycloidal_disc_half_lobe.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_per_cycloidal_disc_half_lobe(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPointsPerCycloidalDiscHalfLobe",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_profile_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfProfilePoints")

        if temp is None:
            return 0

        return temp

    @number_of_profile_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_profile_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfProfilePoints",
            int(value) if value is not None else 0,
        )

    @exception_bridge
    @enforce_parameter_types
    def export_to_stl(
        self: "Self", file_name: "PathLike", progress: "_7901.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
            progress (mastapy.TaskProgress)
        """
        file_name = str(file_name)
        pythonnet_method_call(
            self.wrapped,
            "ExportToSTL",
            file_name,
            progress.wrapped if progress else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def export_to_stp(self: "Self", file_name: "PathLike") -> None:
        """Method does not return.

        Args:
            file_name (PathLike)
        """
        file_name = str(file_name)
        pythonnet_method_call(self.wrapped, "ExportToSTP", file_name)

    @exception_bridge
    @enforce_parameter_types
    def save_stl_to_separate_files(
        self: "Self", directory_path: "str", save_in_sub_folders: "bool"
    ) -> None:
        """Method does not return.

        Args:
            directory_path (str)
            save_in_sub_folders (bool)
        """
        directory_path = str(directory_path)
        save_in_sub_folders = bool(save_in_sub_folders)
        pythonnet_method_call(
            self.wrapped,
            "SaveStlToSeparateFiles",
            directory_path if directory_path else "",
            save_in_sub_folders if save_in_sub_folders else False,
        )

    @exception_bridge
    def to_stl_code(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(self.wrapped, "ToSTLCode")
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GeometryExportOptions":
        """Cast to another type.

        Returns:
            _Cast_GeometryExportOptions
        """
        return _Cast_GeometryExportOptions(self)

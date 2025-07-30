"""CycloidalDiscDesignExporter"""

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
from mastapy._private._math.vector_2d import Vector2D

_CYCLOIDAL_DISC_DESIGN_EXPORTER = python_net_import(
    "SMT.MastaAPI.Cycloidal", "CycloidalDiscDesignExporter"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.cycloidal import _1645

    Self = TypeVar("Self", bound="CycloidalDiscDesignExporter")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CycloidalDiscDesignExporter._Cast_CycloidalDiscDesignExporter",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CycloidalDiscDesignExporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CycloidalDiscDesignExporter:
    """Special nested class for casting CycloidalDiscDesignExporter to subclasses."""

    __parent__: "CycloidalDiscDesignExporter"

    @property
    def cycloidal_disc_design_exporter(
        self: "CastSelf",
    ) -> "CycloidalDiscDesignExporter":
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
class CycloidalDiscDesignExporter(_0.APIBase):
    """CycloidalDiscDesignExporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYCLOIDAL_DISC_DESIGN_EXPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def geometry_to_export(self: "Self") -> "_1645.GeometryToExport":
        """mastapy.cycloidal.GeometryToExport"""
        temp = pythonnet_property_get(self.wrapped, "GeometryToExport")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Cycloidal.GeometryToExport"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.cycloidal._1645", "GeometryToExport"
        )(value)

    @geometry_to_export.setter
    @exception_bridge
    @enforce_parameter_types
    def geometry_to_export(self: "Self", value: "_1645.GeometryToExport") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Cycloidal.GeometryToExport"
        )
        pythonnet_property_set(self.wrapped, "GeometryToExport", value)

    @property
    @exception_bridge
    def include_modifications(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeModifications")

        if temp is None:
            return False

        return temp

    @include_modifications.setter
    @exception_bridge
    @enforce_parameter_types
    def include_modifications(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeModifications",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def number_of_half_lobe_points_for_export(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfHalfLobePointsForExport")

        if temp is None:
            return 0

        return temp

    @number_of_half_lobe_points_for_export.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_half_lobe_points_for_export(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfHalfLobePointsForExport",
            int(value) if value is not None else 0,
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
    def profile_points(
        self: "Self",
        geometry_to_export: "_1645.GeometryToExport",
        include_modifications_in_export: "bool",
        number_of_half_lobe_points_for_export: "int",
    ) -> "List[Vector2D]":
        """List[Vector2D]

        Args:
            geometry_to_export (mastapy.cycloidal.GeometryToExport)
            include_modifications_in_export (bool)
            number_of_half_lobe_points_for_export (int)
        """
        geometry_to_export = conversion.mp_to_pn_enum(
            geometry_to_export, "SMT.MastaAPI.Cycloidal.GeometryToExport"
        )
        include_modifications_in_export = bool(include_modifications_in_export)
        number_of_half_lobe_points_for_export = int(
            number_of_half_lobe_points_for_export
        )
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "ProfilePoints",
                geometry_to_export,
                include_modifications_in_export
                if include_modifications_in_export
                else False,
                number_of_half_lobe_points_for_export
                if number_of_half_lobe_points_for_export
                else 0,
            ),
            Vector2D,
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
    def cast_to(self: "Self") -> "_Cast_CycloidalDiscDesignExporter":
        """Cast to another type.

        Returns:
            _Cast_CycloidalDiscDesignExporter
        """
        return _Cast_CycloidalDiscDesignExporter(self)

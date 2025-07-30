"""GeometryModellerDimensions"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_GEOMETRY_MODELLER_DIMENSIONS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "GeometryModellerDimensions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis.geometry_modeller_link import (
        _231,
        _232,
        _233,
        _237,
        _239,
    )

    Self = TypeVar("Self", bound="GeometryModellerDimensions")
    CastSelf = TypeVar(
        "CastSelf", bound="GeometryModellerDimensions._Cast_GeometryModellerDimensions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeometryModellerDimensions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeometryModellerDimensions:
    """Special nested class for casting GeometryModellerDimensions to subclasses."""

    __parent__: "GeometryModellerDimensions"

    @property
    def geometry_modeller_dimensions(self: "CastSelf") -> "GeometryModellerDimensions":
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
class GeometryModellerDimensions(_0.APIBase):
    """GeometryModellerDimensions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEOMETRY_MODELLER_DIMENSIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def geometry_modeller_design_information(
        self: "Self",
    ) -> "_233.GeometryModellerDesignInformation":
        """mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerDesignInformation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryModellerDesignInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def angle_dimensions(self: "Self") -> "List[_231.GeometryModellerAngleDimension]":
        """List[mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerAngleDimension]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleDimensions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def count_dimensions(self: "Self") -> "List[_232.GeometryModellerCountDimension]":
        """List[mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerCountDimension]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CountDimensions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def length_dimensions(self: "Self") -> "List[_237.GeometryModellerLengthDimension]":
        """List[mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerLengthDimension]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthDimensions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def unitless_dimensions(
        self: "Self",
    ) -> "List[_239.GeometryModellerUnitlessDimension]":
        """List[mastapy.nodal_analysis.geometry_modeller_link.GeometryModellerUnitlessDimension]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnitlessDimensions")

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
    def cast_to(self: "Self") -> "_Cast_GeometryModellerDimensions":
        """Cast to another type.

        Returns:
            _Cast_GeometryModellerDimensions
        """
        return _Cast_GeometryModellerDimensions(self)

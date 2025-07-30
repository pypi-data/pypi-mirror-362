"""NodalMatrixEditorWrapperConceptCouplingStiffness"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
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
from mastapy._private.nodal_analysis import _83

_NODAL_MATRIX_EDITOR_WRAPPER_CONCEPT_COUPLING_STIFFNESS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "NodalMatrixEditorWrapperConceptCouplingStiffness"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="NodalMatrixEditorWrapperConceptCouplingStiffness")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NodalMatrixEditorWrapperConceptCouplingStiffness._Cast_NodalMatrixEditorWrapperConceptCouplingStiffness",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NodalMatrixEditorWrapperConceptCouplingStiffness",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NodalMatrixEditorWrapperConceptCouplingStiffness:
    """Special nested class for casting NodalMatrixEditorWrapperConceptCouplingStiffness to subclasses."""

    __parent__: "NodalMatrixEditorWrapperConceptCouplingStiffness"

    @property
    def nodal_matrix_editor_wrapper(self: "CastSelf") -> "_83.NodalMatrixEditorWrapper":
        return self.__parent__._cast(_83.NodalMatrixEditorWrapper)

    @property
    def nodal_matrix_editor_wrapper_concept_coupling_stiffness(
        self: "CastSelf",
    ) -> "NodalMatrixEditorWrapperConceptCouplingStiffness":
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
class NodalMatrixEditorWrapperConceptCouplingStiffness(_83.NodalMatrixEditorWrapper):
    """NodalMatrixEditorWrapperConceptCouplingStiffness

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NODAL_MATRIX_EDITOR_WRAPPER_CONCEPT_COUPLING_STIFFNESS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "Axial")

        if temp is None:
            return None

        return temp

    @axial.setter
    @exception_bridge
    @enforce_parameter_types
    def axial(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "Axial", value)

    @property
    @exception_bridge
    def theta_y_theta_y(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThetaYThetaY")

        if temp is None:
            return None

        return temp

    @theta_y_theta_y.setter
    @exception_bridge
    @enforce_parameter_types
    def theta_y_theta_y(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "ThetaYThetaY", value)

    @property
    @exception_bridge
    def theta_y_theta_y_cross(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "ThetaYThetaYCross")

        if temp is None:
            return None

        return temp

    @theta_y_theta_y_cross.setter
    @exception_bridge
    @enforce_parameter_types
    def theta_y_theta_y_cross(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "ThetaYThetaYCross", value)

    @property
    @exception_bridge
    def torsional(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "Torsional")

        if temp is None:
            return None

        return temp

    @torsional.setter
    @exception_bridge
    @enforce_parameter_types
    def torsional(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "Torsional", value)

    @property
    @exception_bridge
    def x_theta_y(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "XThetaY")

        if temp is None:
            return None

        return temp

    @x_theta_y.setter
    @exception_bridge
    @enforce_parameter_types
    def x_theta_y(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "XThetaY", value)

    @property
    @exception_bridge
    def xx(self: "Self") -> "Optional[float]":
        """Optional[float]"""
        temp = pythonnet_property_get(self.wrapped, "XX")

        if temp is None:
            return None

        return temp

    @xx.setter
    @exception_bridge
    @enforce_parameter_types
    def xx(self: "Self", value: "Optional[float]") -> None:
        pythonnet_property_set(self.wrapped, "XX", value)

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_NodalMatrixEditorWrapperConceptCouplingStiffness":
        """Cast to another type.

        Returns:
            _Cast_NodalMatrixEditorWrapperConceptCouplingStiffness
        """
        return _Cast_NodalMatrixEditorWrapperConceptCouplingStiffness(self)

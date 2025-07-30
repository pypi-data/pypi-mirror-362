"""CMSOptions"""

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

_CMS_OPTIONS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "CMSOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.fe_tools.vfx_tools import _1359
    from mastapy._private.math_utility import _1687
    from mastapy._private.nodal_analysis.dev_tools_analyses import _263, _283

    Self = TypeVar("Self", bound="CMSOptions")
    CastSelf = TypeVar("CastSelf", bound="CMSOptions._Cast_CMSOptions")


__docformat__ = "restructuredtext en"
__all__ = ("CMSOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CMSOptions:
    """Special nested class for casting CMSOptions to subclasses."""

    __parent__: "CMSOptions"

    @property
    def cms_options(self: "CastSelf") -> "CMSOptions":
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
class CMSOptions(_0.APIBase):
    """CMSOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CMS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculate_reduced_gravity_load(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CalculateReducedGravityLoad")

        if temp is None:
            return False

        return temp

    @calculate_reduced_gravity_load.setter
    @exception_bridge
    @enforce_parameter_types
    def calculate_reduced_gravity_load(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateReducedGravityLoad",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def calculate_reduced_thermal_expansion_force(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CalculateReducedThermalExpansionForce"
        )

        if temp is None:
            return False

        return temp

    @calculate_reduced_thermal_expansion_force.setter
    @exception_bridge
    @enforce_parameter_types
    def calculate_reduced_thermal_expansion_force(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateReducedThermalExpansionForce",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mass_matrix_type(self: "Self") -> "_283.MassMatrixType":
        """mastapy.nodal_analysis.dev_tools_analyses.MassMatrixType"""
        temp = pythonnet_property_get(self.wrapped, "MassMatrixType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.MassMatrixType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.dev_tools_analyses._283", "MassMatrixType"
        )(value)

    @mass_matrix_type.setter
    @exception_bridge
    @enforce_parameter_types
    def mass_matrix_type(self: "Self", value: "_283.MassMatrixType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.MassMatrixType"
        )
        pythonnet_property_set(self.wrapped, "MassMatrixType", value)

    @property
    @exception_bridge
    def mode_options_description(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeOptionsDescription")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def precision_when_saving_expansion_vectors(self: "Self") -> "_1687.DataPrecision":
        """mastapy.math_utility.DataPrecision"""
        temp = pythonnet_property_get(
            self.wrapped, "PrecisionWhenSavingExpansionVectors"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.DataPrecision")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1687", "DataPrecision"
        )(value)

    @precision_when_saving_expansion_vectors.setter
    @exception_bridge
    @enforce_parameter_types
    def precision_when_saving_expansion_vectors(
        self: "Self", value: "_1687.DataPrecision"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.MathUtility.DataPrecision"
        )
        pythonnet_property_set(
            self.wrapped, "PrecisionWhenSavingExpansionVectors", value
        )

    @property
    @exception_bridge
    def store_condensation_node_displacement_expansion(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "StoreCondensationNodeDisplacementExpansion"
        )

        if temp is None:
            return False

        return temp

    @store_condensation_node_displacement_expansion.setter
    @exception_bridge
    @enforce_parameter_types
    def store_condensation_node_displacement_expansion(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "StoreCondensationNodeDisplacementExpansion",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def internal_mode_options(self: "Self") -> "_263.EigenvalueOptions":
        """mastapy.nodal_analysis.dev_tools_analyses.EigenvalueOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalModeOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def solver_options(self: "Self") -> "_1359.ProSolveOptions":
        """mastapy.fe_tools.vfx_tools.ProSolveOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SolverOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_CMSOptions":
        """Cast to another type.

        Returns:
            _Cast_CMSOptions
        """
        return _Cast_CMSOptions(self)

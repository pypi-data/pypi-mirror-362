"""CMSModel"""

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

_CMS_MODEL = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis", "CMSModel"
)

if TYPE_CHECKING:
    from typing import Any, List, Optional, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis.component_mode_synthesis import (
        _310,
        _314,
        _321,
    )
    from mastapy._private.nodal_analysis.dev_tools_analyses import _269
    from mastapy._private.utility import _1771

    Self = TypeVar("Self", bound="CMSModel")
    CastSelf = TypeVar("CastSelf", bound="CMSModel._Cast_CMSModel")


__docformat__ = "restructuredtext en"
__all__ = ("CMSModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CMSModel:
    """Special nested class for casting CMSModel to subclasses."""

    __parent__: "CMSModel"

    @property
    def cms_model(self: "CastSelf") -> "CMSModel":
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
class CMSModel(_0.APIBase):
    """CMSModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CMS_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def estimated_memory_required_for_displacement_expansion(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EstimatedMemoryRequiredForDisplacementExpansion"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def estimated_memory_required_for_stiffness_and_mass_matrices(
        self: "Self",
    ) -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EstimatedMemoryRequiredForStiffnessAndMassMatrices"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def estimated_total_memory_required_for_results(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EstimatedTotalMemoryRequiredForResults"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def has_condensation_result(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasCondensationResult")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def internal_modes_frequency_error(self: "Self") -> "Optional[float]":
        """Optional[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InternalModesFrequencyError")

        if temp is None:
            return None

        return temp

    @property
    @exception_bridge
    def memory_required_for_displacement_expansion(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MemoryRequiredForDisplacementExpansion"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def memory_required_for_stiffness_and_mass_matrices(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MemoryRequiredForStiffnessAndMassMatrices"
        )

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def software_used_for_reduction(
        self: "Self",
    ) -> "_321.SoftwareUsedForReductionType":
        """mastapy.nodal_analysis.component_mode_synthesis.SoftwareUsedForReductionType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoftwareUsedForReduction")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.NodalAnalysis.ComponentModeSynthesis.SoftwareUsedForReductionType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis.component_mode_synthesis._321",
            "SoftwareUsedForReductionType",
        )(value)

    @property
    @exception_bridge
    def total_memory_required_for_mesh(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMemoryRequiredForMesh")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def total_memory_required_for_results(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalMemoryRequiredForResults")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def fe_model(self: "Self") -> "_269.FEModel":
        """mastapy.nodal_analysis.dev_tools_analyses.FEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reduction_information(self: "Self") -> "_1771.AnalysisRunInformation":
        """mastapy.utility.AnalysisRunInformation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReductionInformation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reduction_options(self: "Self") -> "_314.CMSOptions":
        """mastapy.nodal_analysis.component_mode_synthesis.CMSOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReductionOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def element_face_groups(self: "Self") -> "List[_310.CMSElementFaceGroup]":
        """List[mastapy.nodal_analysis.component_mode_synthesis.CMSElementFaceGroup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementFaceGroups")

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
    def save_surface_mesh_as_stl(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "SaveSurfaceMeshAsStl", file_path)

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
    def cast_to(self: "Self") -> "_Cast_CMSModel":
        """Cast to another type.

        Returns:
            _Cast_CMSModel
        """
        return _Cast_CMSModel(self)

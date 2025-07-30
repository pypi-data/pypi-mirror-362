"""HarmonicAnalysisBarModelFEExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.fe_export_utility import _246
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4927

_HARMONIC_ANALYSIS_BAR_MODEL_FE_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisBarModelFEExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.nodal_analysis import _55

    Self = TypeVar("Self", bound="HarmonicAnalysisBarModelFEExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisBarModelFEExportOptions._Cast_HarmonicAnalysisBarModelFEExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisBarModelFEExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisBarModelFEExportOptions:
    """Special nested class for casting HarmonicAnalysisBarModelFEExportOptions to subclasses."""

    __parent__: "HarmonicAnalysisBarModelFEExportOptions"

    @property
    def modal_analysis_bar_model_base_fe_export_options(
        self: "CastSelf",
    ) -> "_4927.ModalAnalysisBarModelBaseFEExportOptions":
        return self.__parent__._cast(_4927.ModalAnalysisBarModelBaseFEExportOptions)

    @property
    def harmonic_analysis_bar_model_fe_export_options(
        self: "CastSelf",
    ) -> "HarmonicAnalysisBarModelFEExportOptions":
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
class HarmonicAnalysisBarModelFEExportOptions(
    _4927.ModalAnalysisBarModelBaseFEExportOptions
):
    """HarmonicAnalysisBarModelFEExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_BAR_MODEL_FE_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_type(self: "Self") -> "_55.BarModelAnalysisType":
        """mastapy.nodal_analysis.BarModelAnalysisType"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.BarModelAnalysisType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._55", "BarModelAnalysisType"
        )(value)

    @analysis_type.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_type(self: "Self", value: "_55.BarModelAnalysisType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.BarModelAnalysisType"
        )
        pythonnet_property_set(self.wrapped, "AnalysisType", value)

    @property
    @exception_bridge
    def fe_package(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FEExportFormat":
        """EnumWithSelectedValue[mastapy.nodal_analysis.fe_export_utility.FEExportFormat]"""
        temp = pythonnet_property_get(self.wrapped, "FEPackage")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @fe_package.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_package(self: "Self", value: "_246.FEExportFormat") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FEPackage", value)

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisBarModelFEExportOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisBarModelFEExportOptions
        """
        return _Cast_HarmonicAnalysisBarModelFEExportOptions(self)

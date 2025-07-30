"""HarmonicAnalysisRootAssemblyExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

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
from mastapy._private.system_model.analyses_and_results import _2896
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6059
from mastapy._private.system_model.part_model import _2706

_HARMONIC_ANALYSIS_ROOT_ASSEMBLY_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisRootAssemblyExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6053,
        _6055,
    )

    Self = TypeVar("Self", bound="HarmonicAnalysisRootAssemblyExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisRootAssemblyExportOptions._Cast_HarmonicAnalysisRootAssemblyExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisRootAssemblyExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisRootAssemblyExportOptions:
    """Special nested class for casting HarmonicAnalysisRootAssemblyExportOptions to subclasses."""

    __parent__: "HarmonicAnalysisRootAssemblyExportOptions"

    @property
    def harmonic_analysis_root_assembly_and_fe_shared_export_options(
        self: "CastSelf",
    ) -> "_6059.HarmonicAnalysisRootAssemblyAndFESharedExportOptions":
        return self.__parent__._cast(
            _6059.HarmonicAnalysisRootAssemblyAndFESharedExportOptions
        )

    @property
    def harmonic_analysis_export_options(
        self: "CastSelf",
    ) -> "_6055.HarmonicAnalysisExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6055,
        )

        return self.__parent__._cast(_6055.HarmonicAnalysisExportOptions)

    @property
    def harmonic_analysis_root_assembly_export_options(
        self: "CastSelf",
    ) -> "HarmonicAnalysisRootAssemblyExportOptions":
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
class HarmonicAnalysisRootAssemblyExportOptions(
    _6059.HarmonicAnalysisRootAssemblyAndFESharedExportOptions[
        _2896.IHaveRootHarmonicAnalysisResults, _2706.RootAssembly
    ]
):
    """HarmonicAnalysisRootAssemblyExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_ROOT_ASSEMBLY_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def export_bar_model_with_excitation_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ExportBarModelWithExcitationData")

        if temp is None:
            return False

        return temp

    @export_bar_model_with_excitation_data.setter
    @exception_bridge
    @enforce_parameter_types
    def export_bar_model_with_excitation_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExportBarModelWithExcitationData",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_all_fe_models(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAllFEModels")

        if temp is None:
            return False

        return temp

    @include_all_fe_models.setter
    @exception_bridge
    @enforce_parameter_types
    def include_all_fe_models(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAllFEModels",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_all_shafts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeAllShafts")

        if temp is None:
            return False

        return temp

    @include_all_shafts.setter
    @exception_bridge
    @enforce_parameter_types
    def include_all_shafts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeAllShafts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def status_message_for_export(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatusMessageForExport")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def bar_model_export_options(
        self: "Self",
    ) -> "_6053.HarmonicAnalysisBarModelFEExportOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisBarModelFEExportOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BarModelExportOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    def export_results_for_bar_model(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExportResultsForBarModel")

    @exception_bridge
    @enforce_parameter_types
    def export_to_folder(self: "Self", folder_path: "str") -> "List[str]":
        """List[str]

        Args:
            folder_path (str)
        """
        folder_path = str(folder_path)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ExportToFolder", folder_path if folder_path else ""
            ),
            str,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisRootAssemblyExportOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisRootAssemblyExportOptions
        """
        return _Cast_HarmonicAnalysisRootAssemblyExportOptions(self)

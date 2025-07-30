"""HarmonicAnalysisRootAssemblyAndFESharedExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6055

_HARMONIC_ANALYSIS_ROOT_ASSEMBLY_AND_FE_SHARED_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisRootAssemblyAndFESharedExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6043,
        _6056,
        _6060,
        _6107,
    )
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="HarmonicAnalysisRootAssemblyAndFESharedExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisRootAssemblyAndFESharedExportOptions._Cast_HarmonicAnalysisRootAssemblyAndFESharedExportOptions",
    )

TIHaveAnalysisResults = TypeVar("TIHaveAnalysisResults")
TPart = TypeVar("TPart", bound="_2698.Part")

__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisRootAssemblyAndFESharedExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisRootAssemblyAndFESharedExportOptions:
    """Special nested class for casting HarmonicAnalysisRootAssemblyAndFESharedExportOptions to subclasses."""

    __parent__: "HarmonicAnalysisRootAssemblyAndFESharedExportOptions"

    @property
    def harmonic_analysis_export_options(
        self: "CastSelf",
    ) -> "_6055.HarmonicAnalysisExportOptions":
        return self.__parent__._cast(_6055.HarmonicAnalysisExportOptions)

    @property
    def harmonic_analysis_fe_export_options(
        self: "CastSelf",
    ) -> "_6056.HarmonicAnalysisFEExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6056,
        )

        return self.__parent__._cast(_6056.HarmonicAnalysisFEExportOptions)

    @property
    def harmonic_analysis_root_assembly_export_options(
        self: "CastSelf",
    ) -> "_6060.HarmonicAnalysisRootAssemblyExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6060,
        )

        return self.__parent__._cast(_6060.HarmonicAnalysisRootAssemblyExportOptions)

    @property
    def harmonic_analysis_root_assembly_and_fe_shared_export_options(
        self: "CastSelf",
    ) -> "HarmonicAnalysisRootAssemblyAndFESharedExportOptions":
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
class HarmonicAnalysisRootAssemblyAndFESharedExportOptions(
    _6055.HarmonicAnalysisExportOptions[TIHaveAnalysisResults, TPart]
):
    """HarmonicAnalysisRootAssemblyAndFESharedExportOptions

    This is a mastapy class.

    Generic Types:
        TIHaveAnalysisResults
        TPart
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_ROOT_ASSEMBLY_AND_FE_SHARED_EXPORT_OPTIONS
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def combine_excitations_from_different_parts(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CombineExcitationsFromDifferentParts"
        )

        if temp is None:
            return False

        return temp

    @combine_excitations_from_different_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def combine_excitations_from_different_parts(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CombineExcitationsFromDifferentParts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def combine_excitations_of_same_order(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CombineExcitationsOfSameOrder")

        if temp is None:
            return False

        return temp

    @combine_excitations_of_same_order.setter
    @exception_bridge
    @enforce_parameter_types
    def combine_excitations_of_same_order(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CombineExcitationsOfSameOrder",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def reference_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @reference_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ReferenceSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def use_single_speed(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseSingleSpeed")

        if temp is None:
            return False

        return temp

    @use_single_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def use_single_speed(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseSingleSpeed", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def frequency_options(
        self: "Self",
    ) -> "_6043.FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reference_speed_options(
        self: "Self",
    ) -> "_6107.SpeedOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.SpeedOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisRootAssemblyAndFESharedExportOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisRootAssemblyAndFESharedExportOptions
        """
        return _Cast_HarmonicAnalysisRootAssemblyAndFESharedExportOptions(self)

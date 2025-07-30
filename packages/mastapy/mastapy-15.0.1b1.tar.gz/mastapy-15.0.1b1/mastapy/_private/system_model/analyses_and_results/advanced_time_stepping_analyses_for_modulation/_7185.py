"""FEPartAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results import _2895
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
    _7126,
)

_FE_PART_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "FEPartAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892, _2894, _2898
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7154,
        _7211,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7887,
        _7890,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6056,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6163,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7756
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2998,
    )
    from mastapy._private.system_model.part_model import _2680

    Self = TypeVar("Self", bound="FEPartAdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FEPartAdvancedTimeSteppingAnalysisForModulation._Cast_FEPartAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting FEPartAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "FEPartAdvancedTimeSteppingAnalysisForModulation"

    @property
    def abstract_shaft_or_housing_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7126.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7126.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def component_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7154.ComponentAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7154,
        )

        return self.__parent__._cast(
            _7154.ComponentAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7211.PartAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7211,
        )

        return self.__parent__._cast(
            _7211.PartAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7890.PartStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7890,
        )

        return self.__parent__._cast(_7890.PartStaticLoadAnalysisCase)

    @property
    def part_analysis_case(self: "CastSelf") -> "_7887.PartAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7887,
        )

        return self.__parent__._cast(_7887.PartAnalysisCase)

    @property
    def part_analysis(self: "CastSelf") -> "_2898.PartAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2898

        return self.__parent__._cast(_2898.PartAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def fe_part_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "FEPartAdvancedTimeSteppingAnalysisForModulation":
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
class FEPartAdvancedTimeSteppingAnalysisForModulation(
    _7126.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation,
    _2895.IHaveFEPartHarmonicAnalysisResults,
):
    """FEPartAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def export_accelerations(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExportAccelerations")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def export_displacements(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExportDisplacements")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def export_forces(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExportForces")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def export_velocities(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExportVelocities")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2680.FEPart":
        """mastapy.system_model.part_model.FEPart

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_load_case(self: "Self") -> "_7756.FEPartLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.FEPartLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def export(self: "Self") -> "_6056.HarmonicAnalysisFEExportOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisFEExportOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Export")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def results(self: "Self") -> "_6163.FEPartHarmonicAnalysisResultsPropertyAccessor":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.FEPartHarmonicAnalysisResultsPropertyAccessor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Results")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def system_deflection_results(self: "Self") -> "_2998.FEPartSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.FEPartSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SystemDeflectionResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def planetaries(
        self: "Self",
    ) -> "List[FEPartAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.FEPartAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_FEPartAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_FEPartAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_FEPartAdvancedTimeSteppingAnalysisForModulation(self)

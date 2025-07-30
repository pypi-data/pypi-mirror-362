"""CVTCompoundAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
    _7271,
)

_CVT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound",
    "CVTCompoundAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7169,
    )
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
        _7261,
        _7342,
        _7361,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )

    Self = TypeVar("Self", bound="CVTCompoundAdvancedTimeSteppingAnalysisForModulation")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CVTCompoundAdvancedTimeSteppingAnalysisForModulation._Cast_CVTCompoundAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CVTCompoundAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CVTCompoundAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting CVTCompoundAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "CVTCompoundAdvancedTimeSteppingAnalysisForModulation"

    @property
    def belt_drive_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7271.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation":
        return self.__parent__._cast(
            _7271.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def specialised_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7361.SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7361,
        )

        return self.__parent__._cast(
            _7361.SpecialisedAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def abstract_assembly_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7261.AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7261,
        )

        return self.__parent__._cast(
            _7261.AbstractAssemblyCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7342.PartCompoundAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import (
            _7342,
        )

        return self.__parent__._cast(
            _7342.PartCompoundAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def cvt_compound_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "CVTCompoundAdvancedTimeSteppingAnalysisForModulation":
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
class CVTCompoundAdvancedTimeSteppingAnalysisForModulation(
    _7271.BeltDriveCompoundAdvancedTimeSteppingAnalysisForModulation
):
    """CVTCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _CVT_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_7169.CVTAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.CVTAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_7169.CVTAdvancedTimeSteppingAnalysisForModulation]":
        """List[mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.CVTAdvancedTimeSteppingAnalysisForModulation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_CVTCompoundAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_CVTCompoundAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_CVTCompoundAdvancedTimeSteppingAnalysisForModulation(self)

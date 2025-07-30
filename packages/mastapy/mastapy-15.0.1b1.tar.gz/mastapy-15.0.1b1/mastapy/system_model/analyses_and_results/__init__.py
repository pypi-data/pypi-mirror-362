"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results._2888 import (
        CompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2889 import (
        AnalysisCaseVariable,
    )
    from mastapy._private.system_model.analyses_and_results._2890 import (
        ConnectionAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2891 import Context
    from mastapy._private.system_model.analyses_and_results._2892 import (
        DesignEntityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2893 import (
        DesignEntityGroupAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2894 import (
        DesignEntitySingleContextAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2898 import PartAnalysis
    from mastapy._private.system_model.analyses_and_results._2899 import (
        CompoundAdvancedSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results._2900 import (
        CompoundAdvancedSystemDeflectionSubAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2901 import (
        CompoundAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2902 import (
        CompoundCriticalSpeedAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2903 import (
        CompoundDynamicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2904 import (
        CompoundDynamicModelAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2905 import (
        CompoundDynamicModelForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2906 import (
        CompoundDynamicModelForModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2907 import (
        CompoundDynamicModelForStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2908 import (
        CompoundDynamicModelForSteadyStateSynchronousResponse,
    )
    from mastapy._private.system_model.analyses_and_results._2909 import (
        CompoundHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2910 import (
        CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation,
    )
    from mastapy._private.system_model.analyses_and_results._2911 import (
        CompoundHarmonicAnalysisOfSingleExcitation,
    )
    from mastapy._private.system_model.analyses_and_results._2912 import (
        CompoundModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2913 import (
        CompoundModalAnalysisAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2914 import (
        CompoundModalAnalysisAtAStiffness,
    )
    from mastapy._private.system_model.analyses_and_results._2915 import (
        CompoundModalAnalysisForHarmonicAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2916 import (
        CompoundMultibodyDynamicsAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2917 import (
        CompoundPowerFlow,
    )
    from mastapy._private.system_model.analyses_and_results._2918 import (
        CompoundStabilityAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results._2919 import (
        CompoundSteadyStateSynchronousResponse,
    )
    from mastapy._private.system_model.analyses_and_results._2920 import (
        CompoundSteadyStateSynchronousResponseAtASpeed,
    )
    from mastapy._private.system_model.analyses_and_results._2921 import (
        CompoundSteadyStateSynchronousResponseOnAShaft,
    )
    from mastapy._private.system_model.analyses_and_results._2922 import (
        CompoundSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results._2923 import (
        CompoundTorsionalSystemDeflection,
    )
    from mastapy._private.system_model.analyses_and_results._2924 import (
        TESetUpForDynamicAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results._2925 import TimeOptions
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results._2888": ["CompoundAnalysis"],
        "_private.system_model.analyses_and_results._2889": ["AnalysisCaseVariable"],
        "_private.system_model.analyses_and_results._2890": ["ConnectionAnalysis"],
        "_private.system_model.analyses_and_results._2891": ["Context"],
        "_private.system_model.analyses_and_results._2892": ["DesignEntityAnalysis"],
        "_private.system_model.analyses_and_results._2893": [
            "DesignEntityGroupAnalysis"
        ],
        "_private.system_model.analyses_and_results._2894": [
            "DesignEntitySingleContextAnalysis"
        ],
        "_private.system_model.analyses_and_results._2898": ["PartAnalysis"],
        "_private.system_model.analyses_and_results._2899": [
            "CompoundAdvancedSystemDeflection"
        ],
        "_private.system_model.analyses_and_results._2900": [
            "CompoundAdvancedSystemDeflectionSubAnalysis"
        ],
        "_private.system_model.analyses_and_results._2901": [
            "CompoundAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2902": [
            "CompoundCriticalSpeedAnalysis"
        ],
        "_private.system_model.analyses_and_results._2903": ["CompoundDynamicAnalysis"],
        "_private.system_model.analyses_and_results._2904": [
            "CompoundDynamicModelAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2905": [
            "CompoundDynamicModelForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2906": [
            "CompoundDynamicModelForModalAnalysis"
        ],
        "_private.system_model.analyses_and_results._2907": [
            "CompoundDynamicModelForStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2908": [
            "CompoundDynamicModelForSteadyStateSynchronousResponse"
        ],
        "_private.system_model.analyses_and_results._2909": [
            "CompoundHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2910": [
            "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
        ],
        "_private.system_model.analyses_and_results._2911": [
            "CompoundHarmonicAnalysisOfSingleExcitation"
        ],
        "_private.system_model.analyses_and_results._2912": ["CompoundModalAnalysis"],
        "_private.system_model.analyses_and_results._2913": [
            "CompoundModalAnalysisAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2914": [
            "CompoundModalAnalysisAtAStiffness"
        ],
        "_private.system_model.analyses_and_results._2915": [
            "CompoundModalAnalysisForHarmonicAnalysis"
        ],
        "_private.system_model.analyses_and_results._2916": [
            "CompoundMultibodyDynamicsAnalysis"
        ],
        "_private.system_model.analyses_and_results._2917": ["CompoundPowerFlow"],
        "_private.system_model.analyses_and_results._2918": [
            "CompoundStabilityAnalysis"
        ],
        "_private.system_model.analyses_and_results._2919": [
            "CompoundSteadyStateSynchronousResponse"
        ],
        "_private.system_model.analyses_and_results._2920": [
            "CompoundSteadyStateSynchronousResponseAtASpeed"
        ],
        "_private.system_model.analyses_and_results._2921": [
            "CompoundSteadyStateSynchronousResponseOnAShaft"
        ],
        "_private.system_model.analyses_and_results._2922": [
            "CompoundSystemDeflection"
        ],
        "_private.system_model.analyses_and_results._2923": [
            "CompoundTorsionalSystemDeflection"
        ],
        "_private.system_model.analyses_and_results._2924": [
            "TESetUpForDynamicAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results._2925": ["TimeOptions"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CompoundAnalysis",
    "AnalysisCaseVariable",
    "ConnectionAnalysis",
    "Context",
    "DesignEntityAnalysis",
    "DesignEntityGroupAnalysis",
    "DesignEntitySingleContextAnalysis",
    "PartAnalysis",
    "CompoundAdvancedSystemDeflection",
    "CompoundAdvancedSystemDeflectionSubAnalysis",
    "CompoundAdvancedTimeSteppingAnalysisForModulation",
    "CompoundCriticalSpeedAnalysis",
    "CompoundDynamicAnalysis",
    "CompoundDynamicModelAtAStiffness",
    "CompoundDynamicModelForHarmonicAnalysis",
    "CompoundDynamicModelForModalAnalysis",
    "CompoundDynamicModelForStabilityAnalysis",
    "CompoundDynamicModelForSteadyStateSynchronousResponse",
    "CompoundHarmonicAnalysis",
    "CompoundHarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    "CompoundHarmonicAnalysisOfSingleExcitation",
    "CompoundModalAnalysis",
    "CompoundModalAnalysisAtASpeed",
    "CompoundModalAnalysisAtAStiffness",
    "CompoundModalAnalysisForHarmonicAnalysis",
    "CompoundMultibodyDynamicsAnalysis",
    "CompoundPowerFlow",
    "CompoundStabilityAnalysis",
    "CompoundSteadyStateSynchronousResponse",
    "CompoundSteadyStateSynchronousResponseAtASpeed",
    "CompoundSteadyStateSynchronousResponseOnAShaft",
    "CompoundSystemDeflection",
    "CompoundTorsionalSystemDeflection",
    "TESetUpForDynamicAnalysisOptions",
    "TimeOptions",
)

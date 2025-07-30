"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7877 import (
        AnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7878 import (
        AbstractAnalysisOptions,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7879 import (
        CompoundAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7880 import (
        ConnectionAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7881 import (
        ConnectionCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7882 import (
        ConnectionFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7883 import (
        ConnectionStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7884 import (
        ConnectionTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7885 import (
        DesignEntityCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7886 import (
        FEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7887 import (
        PartAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7888 import (
        PartCompoundAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7889 import (
        PartFEAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7890 import (
        PartStaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7891 import (
        PartTimeSeriesLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7892 import (
        StaticLoadAnalysisCase,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases._7893 import (
        TimeSeriesLoadAnalysisCase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.analysis_cases._7877": [
            "AnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7878": [
            "AbstractAnalysisOptions"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7879": [
            "CompoundAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7880": [
            "ConnectionAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7881": [
            "ConnectionCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7882": [
            "ConnectionFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7883": [
            "ConnectionStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7884": [
            "ConnectionTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7885": [
            "DesignEntityCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7886": [
            "FEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7887": [
            "PartAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7888": [
            "PartCompoundAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7889": [
            "PartFEAnalysis"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7890": [
            "PartStaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7891": [
            "PartTimeSeriesLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7892": [
            "StaticLoadAnalysisCase"
        ],
        "_private.system_model.analyses_and_results.analysis_cases._7893": [
            "TimeSeriesLoadAnalysisCase"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AnalysisCase",
    "AbstractAnalysisOptions",
    "CompoundAnalysisCase",
    "ConnectionAnalysisCase",
    "ConnectionCompoundAnalysis",
    "ConnectionFEAnalysis",
    "ConnectionStaticLoadAnalysisCase",
    "ConnectionTimeSeriesLoadAnalysisCase",
    "DesignEntityCompoundAnalysis",
    "FEAnalysis",
    "PartAnalysisCase",
    "PartCompoundAnalysis",
    "PartFEAnalysis",
    "PartStaticLoadAnalysisCase",
    "PartTimeSeriesLoadAnalysisCase",
    "StaticLoadAnalysisCase",
    "TimeSeriesLoadAnalysisCase",
)

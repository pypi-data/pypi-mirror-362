"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4989 import (
        CalculateFullFEResultsForMode,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4990 import (
        CampbellDiagramReport,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4991 import (
        ComponentPerModeResult,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4992 import (
        DesignEntityModalAnalysisGroupResults,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4993 import (
        ModalCMSResultsForModeAndFE,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4994 import (
        PerModeResultsReport,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4995 import (
        RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4996 import (
        RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4997 import (
        RigidlyConnectedDesignEntityGroupModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4998 import (
        ShaftPerModeResult,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._4999 import (
        SingleExcitationResultsModalAnalysis,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting._5000 import (
        SingleModeResults,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4989": [
            "CalculateFullFEResultsForMode"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4990": [
            "CampbellDiagramReport"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4991": [
            "ComponentPerModeResult"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4992": [
            "DesignEntityModalAnalysisGroupResults"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4993": [
            "ModalCMSResultsForModeAndFE"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4994": [
            "PerModeResultsReport"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4995": [
            "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4996": [
            "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4997": [
            "RigidlyConnectedDesignEntityGroupModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4998": [
            "ShaftPerModeResult"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._4999": [
            "SingleExcitationResultsModalAnalysis"
        ],
        "_private.system_model.analyses_and_results.modal_analyses.reporting._5000": [
            "SingleModeResults"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CalculateFullFEResultsForMode",
    "CampbellDiagramReport",
    "ComponentPerModeResult",
    "DesignEntityModalAnalysisGroupResults",
    "ModalCMSResultsForModeAndFE",
    "PerModeResultsReport",
    "RigidlyConnectedDesignEntityGroupForSingleExcitationModalAnalysis",
    "RigidlyConnectedDesignEntityGroupForSingleModeModalAnalysis",
    "RigidlyConnectedDesignEntityGroupModalAnalysis",
    "ShaftPerModeResult",
    "SingleExcitationResultsModalAnalysis",
    "SingleModeResults",
)

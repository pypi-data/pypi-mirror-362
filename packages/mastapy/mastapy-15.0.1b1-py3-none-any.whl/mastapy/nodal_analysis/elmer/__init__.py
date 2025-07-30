"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.elmer._248 import ContactType
    from mastapy._private.nodal_analysis.elmer._249 import ElectricMachineAnalysisPeriod
    from mastapy._private.nodal_analysis.elmer._250 import ElmerResultEntityType
    from mastapy._private.nodal_analysis.elmer._251 import ElmerResults
    from mastapy._private.nodal_analysis.elmer._252 import (
        ElmerResultsFromElectromagneticAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._253 import (
        ElmerResultsFromMechanicalAnalysis,
    )
    from mastapy._private.nodal_analysis.elmer._254 import ElmerResultsViewable
    from mastapy._private.nodal_analysis.elmer._255 import ElmerResultType
    from mastapy._private.nodal_analysis.elmer._256 import (
        MechanicalContactSpecification,
    )
    from mastapy._private.nodal_analysis.elmer._257 import MechanicalSolverType
    from mastapy._private.nodal_analysis.elmer._258 import NodalAverageType
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.elmer._248": ["ContactType"],
        "_private.nodal_analysis.elmer._249": ["ElectricMachineAnalysisPeriod"],
        "_private.nodal_analysis.elmer._250": ["ElmerResultEntityType"],
        "_private.nodal_analysis.elmer._251": ["ElmerResults"],
        "_private.nodal_analysis.elmer._252": [
            "ElmerResultsFromElectromagneticAnalysis"
        ],
        "_private.nodal_analysis.elmer._253": ["ElmerResultsFromMechanicalAnalysis"],
        "_private.nodal_analysis.elmer._254": ["ElmerResultsViewable"],
        "_private.nodal_analysis.elmer._255": ["ElmerResultType"],
        "_private.nodal_analysis.elmer._256": ["MechanicalContactSpecification"],
        "_private.nodal_analysis.elmer._257": ["MechanicalSolverType"],
        "_private.nodal_analysis.elmer._258": ["NodalAverageType"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ContactType",
    "ElectricMachineAnalysisPeriod",
    "ElmerResultEntityType",
    "ElmerResults",
    "ElmerResultsFromElectromagneticAnalysis",
    "ElmerResultsFromMechanicalAnalysis",
    "ElmerResultsViewable",
    "ElmerResultType",
    "MechanicalContactSpecification",
    "MechanicalSolverType",
    "NodalAverageType",
)

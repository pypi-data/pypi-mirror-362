"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.analysis._1335 import AbstractGearAnalysis
    from mastapy._private.gears.analysis._1336 import AbstractGearMeshAnalysis
    from mastapy._private.gears.analysis._1337 import AbstractGearSetAnalysis
    from mastapy._private.gears.analysis._1338 import GearDesignAnalysis
    from mastapy._private.gears.analysis._1339 import GearImplementationAnalysis
    from mastapy._private.gears.analysis._1340 import (
        GearImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1341 import GearImplementationDetail
    from mastapy._private.gears.analysis._1342 import GearMeshDesignAnalysis
    from mastapy._private.gears.analysis._1343 import GearMeshImplementationAnalysis
    from mastapy._private.gears.analysis._1344 import (
        GearMeshImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1345 import GearMeshImplementationDetail
    from mastapy._private.gears.analysis._1346 import GearSetDesignAnalysis
    from mastapy._private.gears.analysis._1347 import GearSetGroupDutyCycle
    from mastapy._private.gears.analysis._1348 import GearSetImplementationAnalysis
    from mastapy._private.gears.analysis._1349 import (
        GearSetImplementationAnalysisAbstract,
    )
    from mastapy._private.gears.analysis._1350 import (
        GearSetImplementationAnalysisDutyCycle,
    )
    from mastapy._private.gears.analysis._1351 import GearSetImplementationDetail
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.analysis._1335": ["AbstractGearAnalysis"],
        "_private.gears.analysis._1336": ["AbstractGearMeshAnalysis"],
        "_private.gears.analysis._1337": ["AbstractGearSetAnalysis"],
        "_private.gears.analysis._1338": ["GearDesignAnalysis"],
        "_private.gears.analysis._1339": ["GearImplementationAnalysis"],
        "_private.gears.analysis._1340": ["GearImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1341": ["GearImplementationDetail"],
        "_private.gears.analysis._1342": ["GearMeshDesignAnalysis"],
        "_private.gears.analysis._1343": ["GearMeshImplementationAnalysis"],
        "_private.gears.analysis._1344": ["GearMeshImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1345": ["GearMeshImplementationDetail"],
        "_private.gears.analysis._1346": ["GearSetDesignAnalysis"],
        "_private.gears.analysis._1347": ["GearSetGroupDutyCycle"],
        "_private.gears.analysis._1348": ["GearSetImplementationAnalysis"],
        "_private.gears.analysis._1349": ["GearSetImplementationAnalysisAbstract"],
        "_private.gears.analysis._1350": ["GearSetImplementationAnalysisDutyCycle"],
        "_private.gears.analysis._1351": ["GearSetImplementationDetail"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractGearAnalysis",
    "AbstractGearMeshAnalysis",
    "AbstractGearSetAnalysis",
    "GearDesignAnalysis",
    "GearImplementationAnalysis",
    "GearImplementationAnalysisDutyCycle",
    "GearImplementationDetail",
    "GearMeshDesignAnalysis",
    "GearMeshImplementationAnalysis",
    "GearMeshImplementationAnalysisDutyCycle",
    "GearMeshImplementationDetail",
    "GearSetDesignAnalysis",
    "GearSetGroupDutyCycle",
    "GearSetImplementationAnalysis",
    "GearSetImplementationAnalysisAbstract",
    "GearSetImplementationAnalysisDutyCycle",
    "GearSetImplementationDetail",
)

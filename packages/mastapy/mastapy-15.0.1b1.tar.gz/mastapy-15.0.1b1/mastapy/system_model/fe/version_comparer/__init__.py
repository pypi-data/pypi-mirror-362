"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.fe.version_comparer._2637 import DesignResults
    from mastapy._private.system_model.fe.version_comparer._2638 import (
        FESubstructureResults,
    )
    from mastapy._private.system_model.fe.version_comparer._2639 import (
        FESubstructureVersionComparer,
    )
    from mastapy._private.system_model.fe.version_comparer._2640 import LoadCaseResults
    from mastapy._private.system_model.fe.version_comparer._2641 import LoadCasesToRun
    from mastapy._private.system_model.fe.version_comparer._2642 import (
        NodeComparisonResult,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.fe.version_comparer._2637": ["DesignResults"],
        "_private.system_model.fe.version_comparer._2638": ["FESubstructureResults"],
        "_private.system_model.fe.version_comparer._2639": [
            "FESubstructureVersionComparer"
        ],
        "_private.system_model.fe.version_comparer._2640": ["LoadCaseResults"],
        "_private.system_model.fe.version_comparer._2641": ["LoadCasesToRun"],
        "_private.system_model.fe.version_comparer._2642": ["NodeComparisonResult"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignResults",
    "FESubstructureResults",
    "FESubstructureVersionComparer",
    "LoadCaseResults",
    "LoadCasesToRun",
    "NodeComparisonResult",
)

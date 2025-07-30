"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines.tolerances_and_deviations._1606 import (
        FitAndTolerance,
    )
    from mastapy._private.detailed_rigid_connectors.splines.tolerances_and_deviations._1607 import (
        SAESplineTolerances,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines.tolerances_and_deviations._1606": [
            "FitAndTolerance"
        ],
        "_private.detailed_rigid_connectors.splines.tolerances_and_deviations._1607": [
            "SAESplineTolerances"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "FitAndTolerance",
    "SAESplineTolerances",
)

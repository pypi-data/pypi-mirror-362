"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization.system_optimiser._2449 import (
        DesignStateTargetRatio,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2450 import (
        PlanetGearOptions,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2451 import (
        SystemOptimiser,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2452 import (
        SystemOptimiserDetails,
    )
    from mastapy._private.system_model.optimization.system_optimiser._2453 import (
        ToothNumberFinder,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization.system_optimiser._2449": [
            "DesignStateTargetRatio"
        ],
        "_private.system_model.optimization.system_optimiser._2450": [
            "PlanetGearOptions"
        ],
        "_private.system_model.optimization.system_optimiser._2451": [
            "SystemOptimiser"
        ],
        "_private.system_model.optimization.system_optimiser._2452": [
            "SystemOptimiserDetails"
        ],
        "_private.system_model.optimization.system_optimiser._2453": [
            "ToothNumberFinder"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "DesignStateTargetRatio",
    "PlanetGearOptions",
    "SystemOptimiser",
    "SystemOptimiserDetails",
    "ToothNumberFinder",
)

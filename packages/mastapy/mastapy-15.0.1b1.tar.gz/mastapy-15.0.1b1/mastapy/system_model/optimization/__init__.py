"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization._2437 import (
        ConicalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2438 import (
        ConicalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2439 import (
        ConicalGearOptimizationStrategyDatabase,
    )
    from mastapy._private.system_model.optimization._2440 import (
        CylindricalGearOptimisationStrategy,
    )
    from mastapy._private.system_model.optimization._2441 import (
        CylindricalGearOptimizationStep,
    )
    from mastapy._private.system_model.optimization._2442 import (
        MeasuredAndFactorViewModel,
    )
    from mastapy._private.system_model.optimization._2443 import (
        MicroGeometryOptimisationTarget,
    )
    from mastapy._private.system_model.optimization._2444 import OptimizationParameter
    from mastapy._private.system_model.optimization._2445 import OptimizationStep
    from mastapy._private.system_model.optimization._2446 import OptimizationStrategy
    from mastapy._private.system_model.optimization._2447 import (
        OptimizationStrategyBase,
    )
    from mastapy._private.system_model.optimization._2448 import (
        OptimizationStrategyDatabase,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization._2437": ["ConicalGearOptimisationStrategy"],
        "_private.system_model.optimization._2438": ["ConicalGearOptimizationStep"],
        "_private.system_model.optimization._2439": [
            "ConicalGearOptimizationStrategyDatabase"
        ],
        "_private.system_model.optimization._2440": [
            "CylindricalGearOptimisationStrategy"
        ],
        "_private.system_model.optimization._2441": ["CylindricalGearOptimizationStep"],
        "_private.system_model.optimization._2442": ["MeasuredAndFactorViewModel"],
        "_private.system_model.optimization._2443": ["MicroGeometryOptimisationTarget"],
        "_private.system_model.optimization._2444": ["OptimizationParameter"],
        "_private.system_model.optimization._2445": ["OptimizationStep"],
        "_private.system_model.optimization._2446": ["OptimizationStrategy"],
        "_private.system_model.optimization._2447": ["OptimizationStrategyBase"],
        "_private.system_model.optimization._2448": ["OptimizationStrategyDatabase"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ConicalGearOptimisationStrategy",
    "ConicalGearOptimizationStep",
    "ConicalGearOptimizationStrategyDatabase",
    "CylindricalGearOptimisationStrategy",
    "CylindricalGearOptimizationStep",
    "MeasuredAndFactorViewModel",
    "MicroGeometryOptimisationTarget",
    "OptimizationParameter",
    "OptimizationStep",
    "OptimizationStrategy",
    "OptimizationStrategyBase",
    "OptimizationStrategyDatabase",
)

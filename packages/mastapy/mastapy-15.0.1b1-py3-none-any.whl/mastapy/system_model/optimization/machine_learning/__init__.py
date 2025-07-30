"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.system_model.optimization.machine_learning._2454 import (
        CylindricalGearFlankOptimisationParameter,
    )
    from mastapy._private.system_model.optimization.machine_learning._2455 import (
        CylindricalGearFlankOptimisationParameters,
    )
    from mastapy._private.system_model.optimization.machine_learning._2456 import (
        CylindricalGearFlankOptimisationParametersDatabase,
    )
    from mastapy._private.system_model.optimization.machine_learning._2457 import (
        GearFlankParameterSelection,
    )
    from mastapy._private.system_model.optimization.machine_learning._2458 import (
        LoadCaseConstraint,
    )
    from mastapy._private.system_model.optimization.machine_learning._2459 import (
        LoadCaseSettings,
    )
    from mastapy._private.system_model.optimization.machine_learning._2460 import (
        LoadCaseTarget,
    )
    from mastapy._private.system_model.optimization.machine_learning._2461 import (
        ML1MicroGeometryOptimiser,
    )
    from mastapy._private.system_model.optimization.machine_learning._2462 import (
        ML1MicroGeometryOptimiserGroup,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.system_model.optimization.machine_learning._2454": [
            "CylindricalGearFlankOptimisationParameter"
        ],
        "_private.system_model.optimization.machine_learning._2455": [
            "CylindricalGearFlankOptimisationParameters"
        ],
        "_private.system_model.optimization.machine_learning._2456": [
            "CylindricalGearFlankOptimisationParametersDatabase"
        ],
        "_private.system_model.optimization.machine_learning._2457": [
            "GearFlankParameterSelection"
        ],
        "_private.system_model.optimization.machine_learning._2458": [
            "LoadCaseConstraint"
        ],
        "_private.system_model.optimization.machine_learning._2459": [
            "LoadCaseSettings"
        ],
        "_private.system_model.optimization.machine_learning._2460": ["LoadCaseTarget"],
        "_private.system_model.optimization.machine_learning._2461": [
            "ML1MicroGeometryOptimiser"
        ],
        "_private.system_model.optimization.machine_learning._2462": [
            "ML1MicroGeometryOptimiserGroup"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearFlankOptimisationParameter",
    "CylindricalGearFlankOptimisationParameters",
    "CylindricalGearFlankOptimisationParametersDatabase",
    "GearFlankParameterSelection",
    "LoadCaseConstraint",
    "LoadCaseSettings",
    "LoadCaseTarget",
    "ML1MicroGeometryOptimiser",
    "ML1MicroGeometryOptimiserGroup",
)

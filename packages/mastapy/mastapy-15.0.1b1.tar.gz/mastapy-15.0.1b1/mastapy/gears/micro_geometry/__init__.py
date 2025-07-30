"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.micro_geometry._660 import BiasModification
    from mastapy._private.gears.micro_geometry._661 import FlankMicroGeometry
    from mastapy._private.gears.micro_geometry._662 import FlankSide
    from mastapy._private.gears.micro_geometry._663 import LeadModification
    from mastapy._private.gears.micro_geometry._664 import (
        LocationOfEvaluationLowerLimit,
    )
    from mastapy._private.gears.micro_geometry._665 import (
        LocationOfEvaluationUpperLimit,
    )
    from mastapy._private.gears.micro_geometry._666 import (
        LocationOfRootReliefEvaluation,
    )
    from mastapy._private.gears.micro_geometry._667 import LocationOfTipReliefEvaluation
    from mastapy._private.gears.micro_geometry._668 import (
        MainProfileReliefEndsAtTheStartOfRootReliefOption,
    )
    from mastapy._private.gears.micro_geometry._669 import (
        MainProfileReliefEndsAtTheStartOfTipReliefOption,
    )
    from mastapy._private.gears.micro_geometry._670 import Modification
    from mastapy._private.gears.micro_geometry._671 import (
        ParabolicRootReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._672 import (
        ParabolicTipReliefStartsTangentToMainProfileRelief,
    )
    from mastapy._private.gears.micro_geometry._673 import ProfileModification
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.micro_geometry._660": ["BiasModification"],
        "_private.gears.micro_geometry._661": ["FlankMicroGeometry"],
        "_private.gears.micro_geometry._662": ["FlankSide"],
        "_private.gears.micro_geometry._663": ["LeadModification"],
        "_private.gears.micro_geometry._664": ["LocationOfEvaluationLowerLimit"],
        "_private.gears.micro_geometry._665": ["LocationOfEvaluationUpperLimit"],
        "_private.gears.micro_geometry._666": ["LocationOfRootReliefEvaluation"],
        "_private.gears.micro_geometry._667": ["LocationOfTipReliefEvaluation"],
        "_private.gears.micro_geometry._668": [
            "MainProfileReliefEndsAtTheStartOfRootReliefOption"
        ],
        "_private.gears.micro_geometry._669": [
            "MainProfileReliefEndsAtTheStartOfTipReliefOption"
        ],
        "_private.gears.micro_geometry._670": ["Modification"],
        "_private.gears.micro_geometry._671": [
            "ParabolicRootReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._672": [
            "ParabolicTipReliefStartsTangentToMainProfileRelief"
        ],
        "_private.gears.micro_geometry._673": ["ProfileModification"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BiasModification",
    "FlankMicroGeometry",
    "FlankSide",
    "LeadModification",
    "LocationOfEvaluationLowerLimit",
    "LocationOfEvaluationUpperLimit",
    "LocationOfRootReliefEvaluation",
    "LocationOfTipReliefEvaluation",
    "MainProfileReliefEndsAtTheStartOfRootReliefOption",
    "MainProfileReliefEndsAtTheStartOfTipReliefOption",
    "Modification",
    "ParabolicRootReliefStartsTangentToMainProfileRelief",
    "ParabolicTipReliefStartsTangentToMainProfileRelief",
    "ProfileModification",
)

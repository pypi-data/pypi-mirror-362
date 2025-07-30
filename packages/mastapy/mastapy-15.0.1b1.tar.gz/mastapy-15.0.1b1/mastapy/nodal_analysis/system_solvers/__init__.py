"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.nodal_analysis.system_solvers._106 import (
        BackwardEulerTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._107 import DenseStiffnessSolver
    from mastapy._private.nodal_analysis.system_solvers._108 import DirkTransientSolver
    from mastapy._private.nodal_analysis.system_solvers._109 import DynamicSolver
    from mastapy._private.nodal_analysis.system_solvers._110 import (
        InternalTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._111 import (
        LobattoIIICTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._112 import (
        NewmarkTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._113 import (
        NewtonRaphsonAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._114 import (
        NewtonRaphsonDegreeOfFreedomError,
    )
    from mastapy._private.nodal_analysis.system_solvers._115 import (
        SimpleVelocityBasedStepHalvingTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._116 import (
        SingularDegreeOfFreedomAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._117 import (
        SingularValuesAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._118 import (
        SingularVectorAnalysis,
    )
    from mastapy._private.nodal_analysis.system_solvers._119 import Solver
    from mastapy._private.nodal_analysis.system_solvers._120 import (
        StepHalvingTransientSolver,
    )
    from mastapy._private.nodal_analysis.system_solvers._121 import StiffnessSolver
    from mastapy._private.nodal_analysis.system_solvers._122 import ThermalSolver
    from mastapy._private.nodal_analysis.system_solvers._123 import TransientSolver
    from mastapy._private.nodal_analysis.system_solvers._124 import (
        WilsonThetaTransientSolver,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.nodal_analysis.system_solvers._106": ["BackwardEulerTransientSolver"],
        "_private.nodal_analysis.system_solvers._107": ["DenseStiffnessSolver"],
        "_private.nodal_analysis.system_solvers._108": ["DirkTransientSolver"],
        "_private.nodal_analysis.system_solvers._109": ["DynamicSolver"],
        "_private.nodal_analysis.system_solvers._110": ["InternalTransientSolver"],
        "_private.nodal_analysis.system_solvers._111": ["LobattoIIICTransientSolver"],
        "_private.nodal_analysis.system_solvers._112": ["NewmarkTransientSolver"],
        "_private.nodal_analysis.system_solvers._113": ["NewtonRaphsonAnalysis"],
        "_private.nodal_analysis.system_solvers._114": [
            "NewtonRaphsonDegreeOfFreedomError"
        ],
        "_private.nodal_analysis.system_solvers._115": [
            "SimpleVelocityBasedStepHalvingTransientSolver"
        ],
        "_private.nodal_analysis.system_solvers._116": [
            "SingularDegreeOfFreedomAnalysis"
        ],
        "_private.nodal_analysis.system_solvers._117": ["SingularValuesAnalysis"],
        "_private.nodal_analysis.system_solvers._118": ["SingularVectorAnalysis"],
        "_private.nodal_analysis.system_solvers._119": ["Solver"],
        "_private.nodal_analysis.system_solvers._120": ["StepHalvingTransientSolver"],
        "_private.nodal_analysis.system_solvers._121": ["StiffnessSolver"],
        "_private.nodal_analysis.system_solvers._122": ["ThermalSolver"],
        "_private.nodal_analysis.system_solvers._123": ["TransientSolver"],
        "_private.nodal_analysis.system_solvers._124": ["WilsonThetaTransientSolver"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "BackwardEulerTransientSolver",
    "DenseStiffnessSolver",
    "DirkTransientSolver",
    "DynamicSolver",
    "InternalTransientSolver",
    "LobattoIIICTransientSolver",
    "NewmarkTransientSolver",
    "NewtonRaphsonAnalysis",
    "NewtonRaphsonDegreeOfFreedomError",
    "SimpleVelocityBasedStepHalvingTransientSolver",
    "SingularDegreeOfFreedomAnalysis",
    "SingularValuesAnalysis",
    "SingularVectorAnalysis",
    "Solver",
    "StepHalvingTransientSolver",
    "StiffnessSolver",
    "ThermalSolver",
    "TransientSolver",
    "WilsonThetaTransientSolver",
)

"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.interference_fits._1628 import (
        AssemblyMethods,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1629 import (
        CalculationMethods,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1630 import (
        InterferenceFitDesign,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1631 import (
        InterferenceFitHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1632 import (
        StressRegions,
    )
    from mastapy._private.detailed_rigid_connectors.interference_fits._1633 import (
        Table4JointInterfaceTypes,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.interference_fits._1628": [
            "AssemblyMethods"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1629": [
            "CalculationMethods"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1630": [
            "InterferenceFitDesign"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1631": [
            "InterferenceFitHalfDesign"
        ],
        "_private.detailed_rigid_connectors.interference_fits._1632": ["StressRegions"],
        "_private.detailed_rigid_connectors.interference_fits._1633": [
            "Table4JointInterfaceTypes"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AssemblyMethods",
    "CalculationMethods",
    "InterferenceFitDesign",
    "InterferenceFitHalfDesign",
    "StressRegions",
    "Table4JointInterfaceTypes",
)

"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.electric_machines.thermal.results._1490 import (
        ThermalResultAtLocation,
    )
    from mastapy._private.electric_machines.thermal.results._1491 import ThermalResults
    from mastapy._private.electric_machines.thermal.results._1492 import (
        ThermalResultsForFEComponent,
    )
    from mastapy._private.electric_machines.thermal.results._1493 import (
        ThermalResultsForFERegionOrBoundary,
    )
    from mastapy._private.electric_machines.thermal.results._1494 import (
        ThermalResultsForFESlice,
    )
    from mastapy._private.electric_machines.thermal.results._1495 import (
        ThermalResultsForLPTNNode,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.electric_machines.thermal.results._1490": ["ThermalResultAtLocation"],
        "_private.electric_machines.thermal.results._1491": ["ThermalResults"],
        "_private.electric_machines.thermal.results._1492": [
            "ThermalResultsForFEComponent"
        ],
        "_private.electric_machines.thermal.results._1493": [
            "ThermalResultsForFERegionOrBoundary"
        ],
        "_private.electric_machines.thermal.results._1494": [
            "ThermalResultsForFESlice"
        ],
        "_private.electric_machines.thermal.results._1495": [
            "ThermalResultsForLPTNNode"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "ThermalResultAtLocation",
    "ThermalResults",
    "ThermalResultsForFEComponent",
    "ThermalResultsForFERegionOrBoundary",
    "ThermalResultsForFESlice",
    "ThermalResultsForLPTNNode",
)

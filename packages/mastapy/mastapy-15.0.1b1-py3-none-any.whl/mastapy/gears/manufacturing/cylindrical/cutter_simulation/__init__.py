"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._834 import (
        CutterSimulationCalc,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._835 import (
        CylindricalCutterSimulatableGear,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._836 import (
        CylindricalGearSpecification,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._837 import (
        CylindricalManufacturedRealGearInMesh,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._838 import (
        CylindricalManufacturedVirtualGearInMesh,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._839 import (
        FinishCutterSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._840 import (
        FinishStockPoint,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._841 import (
        FormWheelGrindingSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._842 import (
        GearCutterSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._843 import (
        HobSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._844 import (
        ManufacturingOperationConstraints,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._845 import (
        ManufacturingProcessControls,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._846 import (
        RackSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._847 import (
        RoughCutterSimulation,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._848 import (
        ShaperSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._849 import (
        ShavingSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._850 import (
        VirtualSimulationCalculator,
    )
    from mastapy._private.gears.manufacturing.cylindrical.cutter_simulation._851 import (
        WormGrinderSimulationCalculator,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.manufacturing.cylindrical.cutter_simulation._834": [
            "CutterSimulationCalc"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._835": [
            "CylindricalCutterSimulatableGear"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._836": [
            "CylindricalGearSpecification"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._837": [
            "CylindricalManufacturedRealGearInMesh"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._838": [
            "CylindricalManufacturedVirtualGearInMesh"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._839": [
            "FinishCutterSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._840": [
            "FinishStockPoint"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._841": [
            "FormWheelGrindingSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._842": [
            "GearCutterSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._843": [
            "HobSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._844": [
            "ManufacturingOperationConstraints"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._845": [
            "ManufacturingProcessControls"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._846": [
            "RackSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._847": [
            "RoughCutterSimulation"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._848": [
            "ShaperSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._849": [
            "ShavingSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._850": [
            "VirtualSimulationCalculator"
        ],
        "_private.gears.manufacturing.cylindrical.cutter_simulation._851": [
            "WormGrinderSimulationCalculator"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CutterSimulationCalc",
    "CylindricalCutterSimulatableGear",
    "CylindricalGearSpecification",
    "CylindricalManufacturedRealGearInMesh",
    "CylindricalManufacturedVirtualGearInMesh",
    "FinishCutterSimulation",
    "FinishStockPoint",
    "FormWheelGrindingSimulationCalculator",
    "GearCutterSimulation",
    "HobSimulationCalculator",
    "ManufacturingOperationConstraints",
    "ManufacturingProcessControls",
    "RackSimulationCalculator",
    "RoughCutterSimulation",
    "ShaperSimulationCalculator",
    "ShavingSimulationCalculator",
    "VirtualSimulationCalculator",
    "WormGrinderSimulationCalculator",
)

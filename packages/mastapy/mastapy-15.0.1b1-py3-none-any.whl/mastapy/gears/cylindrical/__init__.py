"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.cylindrical._1328 import (
        CylindricalGearLTCAContactChartDataAsTextFile,
    )
    from mastapy._private.gears.cylindrical._1329 import (
        CylindricalGearLTCAContactCharts,
    )
    from mastapy._private.gears.cylindrical._1330 import (
        CylindricalGearWorstLTCAContactChartDataAsTextFile,
    )
    from mastapy._private.gears.cylindrical._1331 import (
        CylindricalGearWorstLTCAContactCharts,
    )
    from mastapy._private.gears.cylindrical._1332 import (
        GearLTCAContactChartDataAsTextFile,
    )
    from mastapy._private.gears.cylindrical._1333 import GearLTCAContactCharts
    from mastapy._private.gears.cylindrical._1334 import PointsWithWorstResults
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.cylindrical._1328": [
            "CylindricalGearLTCAContactChartDataAsTextFile"
        ],
        "_private.gears.cylindrical._1329": ["CylindricalGearLTCAContactCharts"],
        "_private.gears.cylindrical._1330": [
            "CylindricalGearWorstLTCAContactChartDataAsTextFile"
        ],
        "_private.gears.cylindrical._1331": ["CylindricalGearWorstLTCAContactCharts"],
        "_private.gears.cylindrical._1332": ["GearLTCAContactChartDataAsTextFile"],
        "_private.gears.cylindrical._1333": ["GearLTCAContactCharts"],
        "_private.gears.cylindrical._1334": ["PointsWithWorstResults"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearLTCAContactChartDataAsTextFile",
    "CylindricalGearLTCAContactCharts",
    "CylindricalGearWorstLTCAContactChartDataAsTextFile",
    "CylindricalGearWorstLTCAContactCharts",
    "GearLTCAContactChartDataAsTextFile",
    "GearLTCAContactCharts",
    "PointsWithWorstResults",
)

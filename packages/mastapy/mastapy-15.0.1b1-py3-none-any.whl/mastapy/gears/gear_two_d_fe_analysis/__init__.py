"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_two_d_fe_analysis._997 import (
        CylindricalGearMeshTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._998 import (
        CylindricalGearMeshTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._999 import (
        CylindricalGearSetTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._1000 import (
        CylindricalGearSetTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._1001 import (
        CylindricalGearTIFFAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._1002 import (
        CylindricalGearTIFFAnalysisDutyCycle,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._1003 import (
        CylindricalGearTwoDimensionalFEAnalysis,
    )
    from mastapy._private.gears.gear_two_d_fe_analysis._1004 import (
        FindleyCriticalPlaneAnalysis,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_two_d_fe_analysis._997": [
            "CylindricalGearMeshTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._998": [
            "CylindricalGearMeshTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._999": [
            "CylindricalGearSetTIFFAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._1000": [
            "CylindricalGearSetTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._1001": ["CylindricalGearTIFFAnalysis"],
        "_private.gears.gear_two_d_fe_analysis._1002": [
            "CylindricalGearTIFFAnalysisDutyCycle"
        ],
        "_private.gears.gear_two_d_fe_analysis._1003": [
            "CylindricalGearTwoDimensionalFEAnalysis"
        ],
        "_private.gears.gear_two_d_fe_analysis._1004": ["FindleyCriticalPlaneAnalysis"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearMeshTIFFAnalysis",
    "CylindricalGearMeshTIFFAnalysisDutyCycle",
    "CylindricalGearSetTIFFAnalysis",
    "CylindricalGearSetTIFFAnalysisDutyCycle",
    "CylindricalGearTIFFAnalysis",
    "CylindricalGearTIFFAnalysisDutyCycle",
    "CylindricalGearTwoDimensionalFEAnalysis",
    "FindleyCriticalPlaneAnalysis",
)

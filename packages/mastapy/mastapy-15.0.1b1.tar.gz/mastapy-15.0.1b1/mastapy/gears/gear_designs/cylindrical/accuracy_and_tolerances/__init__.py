"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1250 import (
        AGMA2000A88AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1251 import (
        AGMA20151A01AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1252 import (
        AGMA20151AccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1253 import (
        AGMAISO13281B14AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1254 import (
        Customer102AGMA2000AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1255 import (
        CylindricalAccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1256 import (
        CylindricalAccuracyGraderWithProfileFormAndSlope,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1257 import (
        CylindricalAccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1258 import (
        CylindricalGearAccuracyTolerances,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1259 import (
        DIN3967SystemOfGearFits,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1260 import (
        ISO132811995AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1261 import (
        ISO132812013AccuracyGrader,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1262 import (
        ISO1328AccuracyGraderCommon,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1263 import (
        ISO1328AccuracyGrades,
    )
    from mastapy._private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1264 import (
        OverridableTolerance,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1250": [
            "AGMA2000A88AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1251": [
            "AGMA20151A01AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1252": [
            "AGMA20151AccuracyGrades"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1253": [
            "AGMAISO13281B14AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1254": [
            "Customer102AGMA2000AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1255": [
            "CylindricalAccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1256": [
            "CylindricalAccuracyGraderWithProfileFormAndSlope"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1257": [
            "CylindricalAccuracyGrades"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1258": [
            "CylindricalGearAccuracyTolerances"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1259": [
            "DIN3967SystemOfGearFits"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1260": [
            "ISO132811995AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1261": [
            "ISO132812013AccuracyGrader"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1262": [
            "ISO1328AccuracyGraderCommon"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1263": [
            "ISO1328AccuracyGrades"
        ],
        "_private.gears.gear_designs.cylindrical.accuracy_and_tolerances._1264": [
            "OverridableTolerance"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMA2000A88AccuracyGrader",
    "AGMA20151A01AccuracyGrader",
    "AGMA20151AccuracyGrades",
    "AGMAISO13281B14AccuracyGrader",
    "Customer102AGMA2000AccuracyGrader",
    "CylindricalAccuracyGrader",
    "CylindricalAccuracyGraderWithProfileFormAndSlope",
    "CylindricalAccuracyGrades",
    "CylindricalGearAccuracyTolerances",
    "DIN3967SystemOfGearFits",
    "ISO132811995AccuracyGrader",
    "ISO132812013AccuracyGrader",
    "ISO1328AccuracyGraderCommon",
    "ISO1328AccuracyGrades",
    "OverridableTolerance",
)

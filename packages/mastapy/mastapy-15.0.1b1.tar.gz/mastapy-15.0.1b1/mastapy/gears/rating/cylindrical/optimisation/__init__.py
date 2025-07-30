"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical.optimisation._592 import (
        CylindricalGearSetRatingOptimisationHelper,
    )
    from mastapy._private.gears.rating.cylindrical.optimisation._593 import (
        OptimisationResultsPair,
    )
    from mastapy._private.gears.rating.cylindrical.optimisation._594 import (
        SafetyFactorOptimisationResults,
    )
    from mastapy._private.gears.rating.cylindrical.optimisation._595 import (
        SafetyFactorOptimisationStepResult,
    )
    from mastapy._private.gears.rating.cylindrical.optimisation._596 import (
        SafetyFactorOptimisationStepResultAngle,
    )
    from mastapy._private.gears.rating.cylindrical.optimisation._597 import (
        SafetyFactorOptimisationStepResultNumber,
    )
    from mastapy._private.gears.rating.cylindrical.optimisation._598 import (
        SafetyFactorOptimisationStepResultShortLength,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical.optimisation._592": [
            "CylindricalGearSetRatingOptimisationHelper"
        ],
        "_private.gears.rating.cylindrical.optimisation._593": [
            "OptimisationResultsPair"
        ],
        "_private.gears.rating.cylindrical.optimisation._594": [
            "SafetyFactorOptimisationResults"
        ],
        "_private.gears.rating.cylindrical.optimisation._595": [
            "SafetyFactorOptimisationStepResult"
        ],
        "_private.gears.rating.cylindrical.optimisation._596": [
            "SafetyFactorOptimisationStepResultAngle"
        ],
        "_private.gears.rating.cylindrical.optimisation._597": [
            "SafetyFactorOptimisationStepResultNumber"
        ],
        "_private.gears.rating.cylindrical.optimisation._598": [
            "SafetyFactorOptimisationStepResultShortLength"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CylindricalGearSetRatingOptimisationHelper",
    "OptimisationResultsPair",
    "SafetyFactorOptimisationResults",
    "SafetyFactorOptimisationStepResult",
    "SafetyFactorOptimisationStepResultAngle",
    "SafetyFactorOptimisationStepResultNumber",
    "SafetyFactorOptimisationStepResultShortLength",
)

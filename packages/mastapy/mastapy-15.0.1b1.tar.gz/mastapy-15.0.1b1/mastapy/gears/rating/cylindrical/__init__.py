"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.rating.cylindrical._542 import AGMAScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._543 import (
        CylindricalGearDesignAndRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._544 import (
        CylindricalGearDesignAndRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._545 import (
        CylindricalGearDesignAndRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._546 import (
        CylindricalGearDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._547 import (
        CylindricalGearFlankDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._548 import (
        CylindricalGearFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._549 import CylindricalGearMeshRating
    from mastapy._private.gears.rating.cylindrical._550 import (
        CylindricalGearMicroPittingResults,
    )
    from mastapy._private.gears.rating.cylindrical._551 import CylindricalGearRating
    from mastapy._private.gears.rating.cylindrical._552 import (
        CylindricalGearRatingGeometryDataSource,
    )
    from mastapy._private.gears.rating.cylindrical._553 import (
        CylindricalGearScuffingResults,
    )
    from mastapy._private.gears.rating.cylindrical._554 import (
        CylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._555 import CylindricalGearSetRating
    from mastapy._private.gears.rating.cylindrical._556 import (
        CylindricalGearSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._557 import (
        CylindricalMeshDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._558 import (
        CylindricalMeshSingleFlankRating,
    )
    from mastapy._private.gears.rating.cylindrical._559 import (
        CylindricalPlasticGearRatingSettings,
    )
    from mastapy._private.gears.rating.cylindrical._560 import (
        CylindricalPlasticGearRatingSettingsDatabase,
    )
    from mastapy._private.gears.rating.cylindrical._561 import (
        CylindricalPlasticGearRatingSettingsItem,
    )
    from mastapy._private.gears.rating.cylindrical._562 import CylindricalRateableMesh
    from mastapy._private.gears.rating.cylindrical._563 import DynamicFactorMethods
    from mastapy._private.gears.rating.cylindrical._564 import (
        GearBlankFactorCalculationOptions,
    )
    from mastapy._private.gears.rating.cylindrical._565 import ISOScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._566 import MeshRatingForReports
    from mastapy._private.gears.rating.cylindrical._567 import MicropittingRatingMethod
    from mastapy._private.gears.rating.cylindrical._568 import MicroPittingResultsRow
    from mastapy._private.gears.rating.cylindrical._569 import (
        MisalignmentContactPatternEnhancements,
    )
    from mastapy._private.gears.rating.cylindrical._570 import RatingMethod
    from mastapy._private.gears.rating.cylindrical._571 import (
        ReducedCylindricalGearSetDutyCycleRating,
    )
    from mastapy._private.gears.rating.cylindrical._572 import (
        ScuffingFlashTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._573 import (
        ScuffingIntegralTemperatureRatingMethod,
    )
    from mastapy._private.gears.rating.cylindrical._574 import ScuffingMethods
    from mastapy._private.gears.rating.cylindrical._575 import ScuffingResultsRow
    from mastapy._private.gears.rating.cylindrical._576 import ScuffingResultsRowGear
    from mastapy._private.gears.rating.cylindrical._577 import TipReliefScuffingOptions
    from mastapy._private.gears.rating.cylindrical._578 import ToothThicknesses
    from mastapy._private.gears.rating.cylindrical._579 import (
        VDI2737SafetyFactorReportingObject,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.rating.cylindrical._542": ["AGMAScuffingResultsRow"],
        "_private.gears.rating.cylindrical._543": [
            "CylindricalGearDesignAndRatingSettings"
        ],
        "_private.gears.rating.cylindrical._544": [
            "CylindricalGearDesignAndRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._545": [
            "CylindricalGearDesignAndRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._546": ["CylindricalGearDutyCycleRating"],
        "_private.gears.rating.cylindrical._547": [
            "CylindricalGearFlankDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._548": ["CylindricalGearFlankRating"],
        "_private.gears.rating.cylindrical._549": ["CylindricalGearMeshRating"],
        "_private.gears.rating.cylindrical._550": [
            "CylindricalGearMicroPittingResults"
        ],
        "_private.gears.rating.cylindrical._551": ["CylindricalGearRating"],
        "_private.gears.rating.cylindrical._552": [
            "CylindricalGearRatingGeometryDataSource"
        ],
        "_private.gears.rating.cylindrical._553": ["CylindricalGearScuffingResults"],
        "_private.gears.rating.cylindrical._554": ["CylindricalGearSetDutyCycleRating"],
        "_private.gears.rating.cylindrical._555": ["CylindricalGearSetRating"],
        "_private.gears.rating.cylindrical._556": ["CylindricalGearSingleFlankRating"],
        "_private.gears.rating.cylindrical._557": ["CylindricalMeshDutyCycleRating"],
        "_private.gears.rating.cylindrical._558": ["CylindricalMeshSingleFlankRating"],
        "_private.gears.rating.cylindrical._559": [
            "CylindricalPlasticGearRatingSettings"
        ],
        "_private.gears.rating.cylindrical._560": [
            "CylindricalPlasticGearRatingSettingsDatabase"
        ],
        "_private.gears.rating.cylindrical._561": [
            "CylindricalPlasticGearRatingSettingsItem"
        ],
        "_private.gears.rating.cylindrical._562": ["CylindricalRateableMesh"],
        "_private.gears.rating.cylindrical._563": ["DynamicFactorMethods"],
        "_private.gears.rating.cylindrical._564": ["GearBlankFactorCalculationOptions"],
        "_private.gears.rating.cylindrical._565": ["ISOScuffingResultsRow"],
        "_private.gears.rating.cylindrical._566": ["MeshRatingForReports"],
        "_private.gears.rating.cylindrical._567": ["MicropittingRatingMethod"],
        "_private.gears.rating.cylindrical._568": ["MicroPittingResultsRow"],
        "_private.gears.rating.cylindrical._569": [
            "MisalignmentContactPatternEnhancements"
        ],
        "_private.gears.rating.cylindrical._570": ["RatingMethod"],
        "_private.gears.rating.cylindrical._571": [
            "ReducedCylindricalGearSetDutyCycleRating"
        ],
        "_private.gears.rating.cylindrical._572": [
            "ScuffingFlashTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._573": [
            "ScuffingIntegralTemperatureRatingMethod"
        ],
        "_private.gears.rating.cylindrical._574": ["ScuffingMethods"],
        "_private.gears.rating.cylindrical._575": ["ScuffingResultsRow"],
        "_private.gears.rating.cylindrical._576": ["ScuffingResultsRowGear"],
        "_private.gears.rating.cylindrical._577": ["TipReliefScuffingOptions"],
        "_private.gears.rating.cylindrical._578": ["ToothThicknesses"],
        "_private.gears.rating.cylindrical._579": [
            "VDI2737SafetyFactorReportingObject"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAScuffingResultsRow",
    "CylindricalGearDesignAndRatingSettings",
    "CylindricalGearDesignAndRatingSettingsDatabase",
    "CylindricalGearDesignAndRatingSettingsItem",
    "CylindricalGearDutyCycleRating",
    "CylindricalGearFlankDutyCycleRating",
    "CylindricalGearFlankRating",
    "CylindricalGearMeshRating",
    "CylindricalGearMicroPittingResults",
    "CylindricalGearRating",
    "CylindricalGearRatingGeometryDataSource",
    "CylindricalGearScuffingResults",
    "CylindricalGearSetDutyCycleRating",
    "CylindricalGearSetRating",
    "CylindricalGearSingleFlankRating",
    "CylindricalMeshDutyCycleRating",
    "CylindricalMeshSingleFlankRating",
    "CylindricalPlasticGearRatingSettings",
    "CylindricalPlasticGearRatingSettingsDatabase",
    "CylindricalPlasticGearRatingSettingsItem",
    "CylindricalRateableMesh",
    "DynamicFactorMethods",
    "GearBlankFactorCalculationOptions",
    "ISOScuffingResultsRow",
    "MeshRatingForReports",
    "MicropittingRatingMethod",
    "MicroPittingResultsRow",
    "MisalignmentContactPatternEnhancements",
    "RatingMethod",
    "ReducedCylindricalGearSetDutyCycleRating",
    "ScuffingFlashTemperatureRatingMethod",
    "ScuffingIntegralTemperatureRatingMethod",
    "ScuffingMethods",
    "ScuffingResultsRow",
    "ScuffingResultsRowGear",
    "TipReliefScuffingOptions",
    "ToothThicknesses",
    "VDI2737SafetyFactorReportingObject",
)

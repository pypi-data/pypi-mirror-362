"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.bearings.bearing_designs.rolling._2345 import (
        AngularContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2346 import (
        AngularContactThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2347 import (
        AsymmetricSphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2348 import (
        AxialThrustCylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2349 import (
        AxialThrustNeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2350 import BallBearing
    from mastapy._private.bearings.bearing_designs.rolling._2351 import (
        BallBearingShoulderDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2352 import (
        BarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2353 import (
        BearingProtection,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2354 import (
        BearingProtectionDetailsModifier,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2355 import (
        BearingProtectionLevel,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2356 import (
        BearingTypeExtraInformation,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2357 import CageBridgeShape
    from mastapy._private.bearings.bearing_designs.rolling._2358 import (
        CrossedRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2359 import (
        CylindricalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2360 import (
        DeepGrooveBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2361 import DiameterSeries
    from mastapy._private.bearings.bearing_designs.rolling._2362 import (
        FatigueLoadLimitCalculationMethodEnum,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2363 import (
        FourPointContactAngleDefinition,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2364 import (
        FourPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2365 import (
        GeometricConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2366 import (
        GeometricConstantsForRollingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2367 import (
        GeometricConstantsForSlidingFrictionalMoments,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2368 import HeightSeries
    from mastapy._private.bearings.bearing_designs.rolling._2369 import (
        MultiPointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2370 import (
        NeedleRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2371 import (
        NonBarrelRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2372 import RollerBearing
    from mastapy._private.bearings.bearing_designs.rolling._2373 import RollerEndShape
    from mastapy._private.bearings.bearing_designs.rolling._2374 import RollerRibDetail
    from mastapy._private.bearings.bearing_designs.rolling._2375 import RollingBearing
    from mastapy._private.bearings.bearing_designs.rolling._2376 import (
        RollingBearingElement,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2377 import (
        SelfAligningBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2378 import (
        SKFSealFrictionalMomentConstants,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2379 import SleeveType
    from mastapy._private.bearings.bearing_designs.rolling._2380 import (
        SphericalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2381 import (
        SphericalRollerThrustBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2382 import (
        TaperRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2383 import (
        ThreePointContactBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2384 import (
        ThrustBallBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2385 import (
        ToroidalRollerBearing,
    )
    from mastapy._private.bearings.bearing_designs.rolling._2386 import WidthSeries
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.bearings.bearing_designs.rolling._2345": [
            "AngularContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2346": [
            "AngularContactThrustBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2347": [
            "AsymmetricSphericalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2348": [
            "AxialThrustCylindricalRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2349": [
            "AxialThrustNeedleRollerBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2350": ["BallBearing"],
        "_private.bearings.bearing_designs.rolling._2351": [
            "BallBearingShoulderDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2352": ["BarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2353": ["BearingProtection"],
        "_private.bearings.bearing_designs.rolling._2354": [
            "BearingProtectionDetailsModifier"
        ],
        "_private.bearings.bearing_designs.rolling._2355": ["BearingProtectionLevel"],
        "_private.bearings.bearing_designs.rolling._2356": [
            "BearingTypeExtraInformation"
        ],
        "_private.bearings.bearing_designs.rolling._2357": ["CageBridgeShape"],
        "_private.bearings.bearing_designs.rolling._2358": ["CrossedRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2359": ["CylindricalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2360": ["DeepGrooveBallBearing"],
        "_private.bearings.bearing_designs.rolling._2361": ["DiameterSeries"],
        "_private.bearings.bearing_designs.rolling._2362": [
            "FatigueLoadLimitCalculationMethodEnum"
        ],
        "_private.bearings.bearing_designs.rolling._2363": [
            "FourPointContactAngleDefinition"
        ],
        "_private.bearings.bearing_designs.rolling._2364": [
            "FourPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2365": ["GeometricConstants"],
        "_private.bearings.bearing_designs.rolling._2366": [
            "GeometricConstantsForRollingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2367": [
            "GeometricConstantsForSlidingFrictionalMoments"
        ],
        "_private.bearings.bearing_designs.rolling._2368": ["HeightSeries"],
        "_private.bearings.bearing_designs.rolling._2369": [
            "MultiPointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2370": ["NeedleRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2371": ["NonBarrelRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2372": ["RollerBearing"],
        "_private.bearings.bearing_designs.rolling._2373": ["RollerEndShape"],
        "_private.bearings.bearing_designs.rolling._2374": ["RollerRibDetail"],
        "_private.bearings.bearing_designs.rolling._2375": ["RollingBearing"],
        "_private.bearings.bearing_designs.rolling._2376": ["RollingBearingElement"],
        "_private.bearings.bearing_designs.rolling._2377": ["SelfAligningBallBearing"],
        "_private.bearings.bearing_designs.rolling._2378": [
            "SKFSealFrictionalMomentConstants"
        ],
        "_private.bearings.bearing_designs.rolling._2379": ["SleeveType"],
        "_private.bearings.bearing_designs.rolling._2380": ["SphericalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2381": [
            "SphericalRollerThrustBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2382": ["TaperRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2383": [
            "ThreePointContactBallBearing"
        ],
        "_private.bearings.bearing_designs.rolling._2384": ["ThrustBallBearing"],
        "_private.bearings.bearing_designs.rolling._2385": ["ToroidalRollerBearing"],
        "_private.bearings.bearing_designs.rolling._2386": ["WidthSeries"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AngularContactBallBearing",
    "AngularContactThrustBallBearing",
    "AsymmetricSphericalRollerBearing",
    "AxialThrustCylindricalRollerBearing",
    "AxialThrustNeedleRollerBearing",
    "BallBearing",
    "BallBearingShoulderDefinition",
    "BarrelRollerBearing",
    "BearingProtection",
    "BearingProtectionDetailsModifier",
    "BearingProtectionLevel",
    "BearingTypeExtraInformation",
    "CageBridgeShape",
    "CrossedRollerBearing",
    "CylindricalRollerBearing",
    "DeepGrooveBallBearing",
    "DiameterSeries",
    "FatigueLoadLimitCalculationMethodEnum",
    "FourPointContactAngleDefinition",
    "FourPointContactBallBearing",
    "GeometricConstants",
    "GeometricConstantsForRollingFrictionalMoments",
    "GeometricConstantsForSlidingFrictionalMoments",
    "HeightSeries",
    "MultiPointContactBallBearing",
    "NeedleRollerBearing",
    "NonBarrelRollerBearing",
    "RollerBearing",
    "RollerEndShape",
    "RollerRibDetail",
    "RollingBearing",
    "RollingBearingElement",
    "SelfAligningBallBearing",
    "SKFSealFrictionalMomentConstants",
    "SleeveType",
    "SphericalRollerBearing",
    "SphericalRollerThrustBearing",
    "TaperRollerBearing",
    "ThreePointContactBallBearing",
    "ThrustBallBearing",
    "ToroidalRollerBearing",
    "WidthSeries",
)

"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.gears.materials._674 import AGMACylindricalGearMaterial
    from mastapy._private.gears.materials._675 import (
        BenedictAndKelleyCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._676 import BevelGearAbstractMaterialDatabase
    from mastapy._private.gears.materials._677 import BevelGearISOMaterial
    from mastapy._private.gears.materials._678 import BevelGearISOMaterialDatabase
    from mastapy._private.gears.materials._679 import BevelGearMaterial
    from mastapy._private.gears.materials._680 import BevelGearMaterialDatabase
    from mastapy._private.gears.materials._681 import CoefficientOfFrictionCalculator
    from mastapy._private.gears.materials._682 import (
        CylindricalGearAGMAMaterialDatabase,
    )
    from mastapy._private.gears.materials._683 import CylindricalGearISOMaterialDatabase
    from mastapy._private.gears.materials._684 import CylindricalGearMaterial
    from mastapy._private.gears.materials._685 import CylindricalGearMaterialDatabase
    from mastapy._private.gears.materials._686 import (
        CylindricalGearPlasticMaterialDatabase,
    )
    from mastapy._private.gears.materials._687 import (
        DrozdovAndGavrikovCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._688 import GearMaterial
    from mastapy._private.gears.materials._689 import GearMaterialDatabase
    from mastapy._private.gears.materials._690 import (
        GearMaterialExpertSystemFactorSettings,
    )
    from mastapy._private.gears.materials._691 import (
        InstantaneousCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._692 import (
        ISO14179Part1CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._693 import (
        ISO14179Part2CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._694 import (
        ISO14179Part2CoefficientOfFrictionCalculatorBase,
    )
    from mastapy._private.gears.materials._695 import (
        ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification,
    )
    from mastapy._private.gears.materials._696 import ISOCylindricalGearMaterial
    from mastapy._private.gears.materials._697 import (
        ISOTC60CoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._698 import (
        ISOTR1417912001CoefficientOfFrictionConstants,
    )
    from mastapy._private.gears.materials._699 import (
        ISOTR1417912001CoefficientOfFrictionConstantsDatabase,
    )
    from mastapy._private.gears.materials._700 import (
        KlingelnbergConicalGearMaterialDatabase,
    )
    from mastapy._private.gears.materials._701 import (
        KlingelnbergCycloPalloidConicalGearMaterial,
    )
    from mastapy._private.gears.materials._702 import ManufactureRating
    from mastapy._private.gears.materials._703 import (
        MisharinCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._704 import (
        ODonoghueAndCameronCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._705 import PlasticCylindricalGearMaterial
    from mastapy._private.gears.materials._706 import PlasticSNCurve
    from mastapy._private.gears.materials._707 import RatingMethods
    from mastapy._private.gears.materials._708 import RawMaterial
    from mastapy._private.gears.materials._709 import RawMaterialDatabase
    from mastapy._private.gears.materials._710 import (
        ScriptCoefficientOfFrictionCalculator,
    )
    from mastapy._private.gears.materials._711 import SNCurveDefinition
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.gears.materials._674": ["AGMACylindricalGearMaterial"],
        "_private.gears.materials._675": [
            "BenedictAndKelleyCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._676": ["BevelGearAbstractMaterialDatabase"],
        "_private.gears.materials._677": ["BevelGearISOMaterial"],
        "_private.gears.materials._678": ["BevelGearISOMaterialDatabase"],
        "_private.gears.materials._679": ["BevelGearMaterial"],
        "_private.gears.materials._680": ["BevelGearMaterialDatabase"],
        "_private.gears.materials._681": ["CoefficientOfFrictionCalculator"],
        "_private.gears.materials._682": ["CylindricalGearAGMAMaterialDatabase"],
        "_private.gears.materials._683": ["CylindricalGearISOMaterialDatabase"],
        "_private.gears.materials._684": ["CylindricalGearMaterial"],
        "_private.gears.materials._685": ["CylindricalGearMaterialDatabase"],
        "_private.gears.materials._686": ["CylindricalGearPlasticMaterialDatabase"],
        "_private.gears.materials._687": [
            "DrozdovAndGavrikovCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._688": ["GearMaterial"],
        "_private.gears.materials._689": ["GearMaterialDatabase"],
        "_private.gears.materials._690": ["GearMaterialExpertSystemFactorSettings"],
        "_private.gears.materials._691": [
            "InstantaneousCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._692": [
            "ISO14179Part1CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._693": [
            "ISO14179Part2CoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._694": [
            "ISO14179Part2CoefficientOfFrictionCalculatorBase"
        ],
        "_private.gears.materials._695": [
            "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification"
        ],
        "_private.gears.materials._696": ["ISOCylindricalGearMaterial"],
        "_private.gears.materials._697": ["ISOTC60CoefficientOfFrictionCalculator"],
        "_private.gears.materials._698": [
            "ISOTR1417912001CoefficientOfFrictionConstants"
        ],
        "_private.gears.materials._699": [
            "ISOTR1417912001CoefficientOfFrictionConstantsDatabase"
        ],
        "_private.gears.materials._700": ["KlingelnbergConicalGearMaterialDatabase"],
        "_private.gears.materials._701": [
            "KlingelnbergCycloPalloidConicalGearMaterial"
        ],
        "_private.gears.materials._702": ["ManufactureRating"],
        "_private.gears.materials._703": ["MisharinCoefficientOfFrictionCalculator"],
        "_private.gears.materials._704": [
            "ODonoghueAndCameronCoefficientOfFrictionCalculator"
        ],
        "_private.gears.materials._705": ["PlasticCylindricalGearMaterial"],
        "_private.gears.materials._706": ["PlasticSNCurve"],
        "_private.gears.materials._707": ["RatingMethods"],
        "_private.gears.materials._708": ["RawMaterial"],
        "_private.gears.materials._709": ["RawMaterialDatabase"],
        "_private.gears.materials._710": ["ScriptCoefficientOfFrictionCalculator"],
        "_private.gears.materials._711": ["SNCurveDefinition"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMACylindricalGearMaterial",
    "BenedictAndKelleyCoefficientOfFrictionCalculator",
    "BevelGearAbstractMaterialDatabase",
    "BevelGearISOMaterial",
    "BevelGearISOMaterialDatabase",
    "BevelGearMaterial",
    "BevelGearMaterialDatabase",
    "CoefficientOfFrictionCalculator",
    "CylindricalGearAGMAMaterialDatabase",
    "CylindricalGearISOMaterialDatabase",
    "CylindricalGearMaterial",
    "CylindricalGearMaterialDatabase",
    "CylindricalGearPlasticMaterialDatabase",
    "DrozdovAndGavrikovCoefficientOfFrictionCalculator",
    "GearMaterial",
    "GearMaterialDatabase",
    "GearMaterialExpertSystemFactorSettings",
    "InstantaneousCoefficientOfFrictionCalculator",
    "ISO14179Part1CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculator",
    "ISO14179Part2CoefficientOfFrictionCalculatorBase",
    "ISO14179Part2CoefficientOfFrictionCalculatorWithMartinsModification",
    "ISOCylindricalGearMaterial",
    "ISOTC60CoefficientOfFrictionCalculator",
    "ISOTR1417912001CoefficientOfFrictionConstants",
    "ISOTR1417912001CoefficientOfFrictionConstantsDatabase",
    "KlingelnbergConicalGearMaterialDatabase",
    "KlingelnbergCycloPalloidConicalGearMaterial",
    "ManufactureRating",
    "MisharinCoefficientOfFrictionCalculator",
    "ODonoghueAndCameronCoefficientOfFrictionCalculator",
    "PlasticCylindricalGearMaterial",
    "PlasticSNCurve",
    "RatingMethods",
    "RawMaterial",
    "RawMaterialDatabase",
    "ScriptCoefficientOfFrictionCalculator",
    "SNCurveDefinition",
)

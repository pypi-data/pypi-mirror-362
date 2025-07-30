"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.materials._323 import (
        AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._324 import AcousticRadiationEfficiency
    from mastapy._private.materials._325 import AcousticRadiationEfficiencyInputType
    from mastapy._private.materials._326 import AGMALubricantType
    from mastapy._private.materials._327 import AGMAMaterialApplications
    from mastapy._private.materials._328 import AGMAMaterialClasses
    from mastapy._private.materials._329 import AGMAMaterialGrade
    from mastapy._private.materials._330 import AirProperties
    from mastapy._private.materials._331 import BearingLubricationCondition
    from mastapy._private.materials._332 import BearingMaterial
    from mastapy._private.materials._333 import BearingMaterialDatabase
    from mastapy._private.materials._334 import BHCurveExtrapolationMethod
    from mastapy._private.materials._335 import BHCurveSpecification
    from mastapy._private.materials._336 import ComponentMaterialDatabase
    from mastapy._private.materials._337 import CompositeFatigueSafetyFactorItem
    from mastapy._private.materials._338 import CylindricalGearRatingMethods
    from mastapy._private.materials._339 import DensitySpecificationMethod
    from mastapy._private.materials._340 import FatigueSafetyFactorItem
    from mastapy._private.materials._341 import FatigueSafetyFactorItemBase
    from mastapy._private.materials._342 import Fluid
    from mastapy._private.materials._343 import FluidDatabase
    from mastapy._private.materials._344 import GearingTypes
    from mastapy._private.materials._345 import GeneralTransmissionProperties
    from mastapy._private.materials._346 import GreaseContaminationOptions
    from mastapy._private.materials._347 import HardnessType
    from mastapy._private.materials._348 import ISO76StaticSafetyFactorLimits
    from mastapy._private.materials._349 import ISOLubricantType
    from mastapy._private.materials._350 import LubricantDefinition
    from mastapy._private.materials._351 import LubricantDelivery
    from mastapy._private.materials._352 import LubricantViscosityClassAGMA
    from mastapy._private.materials._353 import LubricantViscosityClassification
    from mastapy._private.materials._354 import LubricantViscosityClassISO
    from mastapy._private.materials._355 import LubricantViscosityClassSAE
    from mastapy._private.materials._356 import LubricationDetail
    from mastapy._private.materials._357 import LubricationDetailDatabase
    from mastapy._private.materials._358 import Material
    from mastapy._private.materials._359 import MaterialDatabase
    from mastapy._private.materials._360 import MaterialsSettings
    from mastapy._private.materials._361 import MaterialsSettingsDatabase
    from mastapy._private.materials._362 import MaterialsSettingsItem
    from mastapy._private.materials._363 import MaterialStandards
    from mastapy._private.materials._364 import MetalPlasticType
    from mastapy._private.materials._365 import OilFiltrationOptions
    from mastapy._private.materials._366 import PressureViscosityCoefficientMethod
    from mastapy._private.materials._367 import QualityGrade
    from mastapy._private.materials._368 import SafetyFactorGroup
    from mastapy._private.materials._369 import SafetyFactorItem
    from mastapy._private.materials._370 import SNCurve
    from mastapy._private.materials._371 import SNCurvePoint
    from mastapy._private.materials._372 import SoundPressureEnclosure
    from mastapy._private.materials._373 import SoundPressureEnclosureType
    from mastapy._private.materials._374 import (
        StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._375 import (
        StressCyclesDataForTheContactSNCurveOfAPlasticMaterial,
    )
    from mastapy._private.materials._376 import TemperatureDependentProperty
    from mastapy._private.materials._377 import TransmissionApplications
    from mastapy._private.materials._378 import VDI2736LubricantType
    from mastapy._private.materials._379 import VehicleDynamicsProperties
    from mastapy._private.materials._380 import WindTurbineStandards
    from mastapy._private.materials._381 import WorkingCharacteristics
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.materials._323": [
            "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._324": ["AcousticRadiationEfficiency"],
        "_private.materials._325": ["AcousticRadiationEfficiencyInputType"],
        "_private.materials._326": ["AGMALubricantType"],
        "_private.materials._327": ["AGMAMaterialApplications"],
        "_private.materials._328": ["AGMAMaterialClasses"],
        "_private.materials._329": ["AGMAMaterialGrade"],
        "_private.materials._330": ["AirProperties"],
        "_private.materials._331": ["BearingLubricationCondition"],
        "_private.materials._332": ["BearingMaterial"],
        "_private.materials._333": ["BearingMaterialDatabase"],
        "_private.materials._334": ["BHCurveExtrapolationMethod"],
        "_private.materials._335": ["BHCurveSpecification"],
        "_private.materials._336": ["ComponentMaterialDatabase"],
        "_private.materials._337": ["CompositeFatigueSafetyFactorItem"],
        "_private.materials._338": ["CylindricalGearRatingMethods"],
        "_private.materials._339": ["DensitySpecificationMethod"],
        "_private.materials._340": ["FatigueSafetyFactorItem"],
        "_private.materials._341": ["FatigueSafetyFactorItemBase"],
        "_private.materials._342": ["Fluid"],
        "_private.materials._343": ["FluidDatabase"],
        "_private.materials._344": ["GearingTypes"],
        "_private.materials._345": ["GeneralTransmissionProperties"],
        "_private.materials._346": ["GreaseContaminationOptions"],
        "_private.materials._347": ["HardnessType"],
        "_private.materials._348": ["ISO76StaticSafetyFactorLimits"],
        "_private.materials._349": ["ISOLubricantType"],
        "_private.materials._350": ["LubricantDefinition"],
        "_private.materials._351": ["LubricantDelivery"],
        "_private.materials._352": ["LubricantViscosityClassAGMA"],
        "_private.materials._353": ["LubricantViscosityClassification"],
        "_private.materials._354": ["LubricantViscosityClassISO"],
        "_private.materials._355": ["LubricantViscosityClassSAE"],
        "_private.materials._356": ["LubricationDetail"],
        "_private.materials._357": ["LubricationDetailDatabase"],
        "_private.materials._358": ["Material"],
        "_private.materials._359": ["MaterialDatabase"],
        "_private.materials._360": ["MaterialsSettings"],
        "_private.materials._361": ["MaterialsSettingsDatabase"],
        "_private.materials._362": ["MaterialsSettingsItem"],
        "_private.materials._363": ["MaterialStandards"],
        "_private.materials._364": ["MetalPlasticType"],
        "_private.materials._365": ["OilFiltrationOptions"],
        "_private.materials._366": ["PressureViscosityCoefficientMethod"],
        "_private.materials._367": ["QualityGrade"],
        "_private.materials._368": ["SafetyFactorGroup"],
        "_private.materials._369": ["SafetyFactorItem"],
        "_private.materials._370": ["SNCurve"],
        "_private.materials._371": ["SNCurvePoint"],
        "_private.materials._372": ["SoundPressureEnclosure"],
        "_private.materials._373": ["SoundPressureEnclosureType"],
        "_private.materials._374": [
            "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._375": [
            "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial"
        ],
        "_private.materials._376": ["TemperatureDependentProperty"],
        "_private.materials._377": ["TransmissionApplications"],
        "_private.materials._378": ["VDI2736LubricantType"],
        "_private.materials._379": ["VehicleDynamicsProperties"],
        "_private.materials._380": ["WindTurbineStandards"],
        "_private.materials._381": ["WorkingCharacteristics"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AbstractStressCyclesDataForAnSNCurveOfAPlasticMaterial",
    "AcousticRadiationEfficiency",
    "AcousticRadiationEfficiencyInputType",
    "AGMALubricantType",
    "AGMAMaterialApplications",
    "AGMAMaterialClasses",
    "AGMAMaterialGrade",
    "AirProperties",
    "BearingLubricationCondition",
    "BearingMaterial",
    "BearingMaterialDatabase",
    "BHCurveExtrapolationMethod",
    "BHCurveSpecification",
    "ComponentMaterialDatabase",
    "CompositeFatigueSafetyFactorItem",
    "CylindricalGearRatingMethods",
    "DensitySpecificationMethod",
    "FatigueSafetyFactorItem",
    "FatigueSafetyFactorItemBase",
    "Fluid",
    "FluidDatabase",
    "GearingTypes",
    "GeneralTransmissionProperties",
    "GreaseContaminationOptions",
    "HardnessType",
    "ISO76StaticSafetyFactorLimits",
    "ISOLubricantType",
    "LubricantDefinition",
    "LubricantDelivery",
    "LubricantViscosityClassAGMA",
    "LubricantViscosityClassification",
    "LubricantViscosityClassISO",
    "LubricantViscosityClassSAE",
    "LubricationDetail",
    "LubricationDetailDatabase",
    "Material",
    "MaterialDatabase",
    "MaterialsSettings",
    "MaterialsSettingsDatabase",
    "MaterialsSettingsItem",
    "MaterialStandards",
    "MetalPlasticType",
    "OilFiltrationOptions",
    "PressureViscosityCoefficientMethod",
    "QualityGrade",
    "SafetyFactorGroup",
    "SafetyFactorItem",
    "SNCurve",
    "SNCurvePoint",
    "SoundPressureEnclosure",
    "SoundPressureEnclosureType",
    "StressCyclesDataForTheBendingSNCurveOfAPlasticMaterial",
    "StressCyclesDataForTheContactSNCurveOfAPlasticMaterial",
    "TemperatureDependentProperty",
    "TransmissionApplications",
    "VDI2736LubricantType",
    "VehicleDynamicsProperties",
    "WindTurbineStandards",
    "WorkingCharacteristics",
)

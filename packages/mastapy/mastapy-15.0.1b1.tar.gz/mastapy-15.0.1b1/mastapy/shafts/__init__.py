"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.shafts._6 import AGMAHardeningType
    from mastapy._private.shafts._7 import CastingFactorCondition
    from mastapy._private.shafts._8 import ConsequenceOfFailure
    from mastapy._private.shafts._9 import DesignShaftSection
    from mastapy._private.shafts._10 import DesignShaftSectionEnd
    from mastapy._private.shafts._11 import FkmMaterialGroup
    from mastapy._private.shafts._12 import FkmSnCurveModel
    from mastapy._private.shafts._13 import FkmVersionOfMinersRule
    from mastapy._private.shafts._14 import GenericStressConcentrationFactor
    from mastapy._private.shafts._15 import ProfilePointFilletStressConcentrationFactors
    from mastapy._private.shafts._16 import ShaftAxialBendingTorsionalComponentValues
    from mastapy._private.shafts._17 import (
        ShaftAxialBendingXBendingYTorsionalComponentValues,
    )
    from mastapy._private.shafts._18 import ShaftAxialTorsionalComponentValues
    from mastapy._private.shafts._19 import ShaftDamageResults
    from mastapy._private.shafts._20 import ShaftDamageResultsTableAndChart
    from mastapy._private.shafts._21 import ShaftFeature
    from mastapy._private.shafts._22 import ShaftGroove
    from mastapy._private.shafts._23 import ShaftKey
    from mastapy._private.shafts._24 import ShaftMaterial
    from mastapy._private.shafts._25 import ShaftMaterialDatabase
    from mastapy._private.shafts._26 import ShaftMaterialForReports
    from mastapy._private.shafts._27 import ShaftPointStress
    from mastapy._private.shafts._28 import ShaftPointStressCycle
    from mastapy._private.shafts._29 import ShaftPointStressCycleReporting
    from mastapy._private.shafts._30 import ShaftProfile
    from mastapy._private.shafts._31 import ShaftProfileFromImport
    from mastapy._private.shafts._32 import ShaftProfileLoop
    from mastapy._private.shafts._33 import ShaftProfilePoint
    from mastapy._private.shafts._34 import ShaftProfilePointCopy
    from mastapy._private.shafts._35 import ShaftProfileType
    from mastapy._private.shafts._36 import ShaftRadialHole
    from mastapy._private.shafts._37 import ShaftRatingMethod
    from mastapy._private.shafts._38 import ShaftSafetyFactorSettings
    from mastapy._private.shafts._39 import ShaftSectionDamageResults
    from mastapy._private.shafts._40 import ShaftSectionEndDamageResults
    from mastapy._private.shafts._41 import ShaftSettings
    from mastapy._private.shafts._42 import ShaftSettingsDatabase
    from mastapy._private.shafts._43 import ShaftSettingsItem
    from mastapy._private.shafts._44 import ShaftSurfaceFinishSection
    from mastapy._private.shafts._45 import ShaftSurfaceRoughness
    from mastapy._private.shafts._46 import SimpleShaftDefinition
    from mastapy._private.shafts._47 import (
        StressMeasurementShaftAxialBendingTorsionalComponentValues,
    )
    from mastapy._private.shafts._48 import SurfaceFinishes
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.shafts._6": ["AGMAHardeningType"],
        "_private.shafts._7": ["CastingFactorCondition"],
        "_private.shafts._8": ["ConsequenceOfFailure"],
        "_private.shafts._9": ["DesignShaftSection"],
        "_private.shafts._10": ["DesignShaftSectionEnd"],
        "_private.shafts._11": ["FkmMaterialGroup"],
        "_private.shafts._12": ["FkmSnCurveModel"],
        "_private.shafts._13": ["FkmVersionOfMinersRule"],
        "_private.shafts._14": ["GenericStressConcentrationFactor"],
        "_private.shafts._15": ["ProfilePointFilletStressConcentrationFactors"],
        "_private.shafts._16": ["ShaftAxialBendingTorsionalComponentValues"],
        "_private.shafts._17": ["ShaftAxialBendingXBendingYTorsionalComponentValues"],
        "_private.shafts._18": ["ShaftAxialTorsionalComponentValues"],
        "_private.shafts._19": ["ShaftDamageResults"],
        "_private.shafts._20": ["ShaftDamageResultsTableAndChart"],
        "_private.shafts._21": ["ShaftFeature"],
        "_private.shafts._22": ["ShaftGroove"],
        "_private.shafts._23": ["ShaftKey"],
        "_private.shafts._24": ["ShaftMaterial"],
        "_private.shafts._25": ["ShaftMaterialDatabase"],
        "_private.shafts._26": ["ShaftMaterialForReports"],
        "_private.shafts._27": ["ShaftPointStress"],
        "_private.shafts._28": ["ShaftPointStressCycle"],
        "_private.shafts._29": ["ShaftPointStressCycleReporting"],
        "_private.shafts._30": ["ShaftProfile"],
        "_private.shafts._31": ["ShaftProfileFromImport"],
        "_private.shafts._32": ["ShaftProfileLoop"],
        "_private.shafts._33": ["ShaftProfilePoint"],
        "_private.shafts._34": ["ShaftProfilePointCopy"],
        "_private.shafts._35": ["ShaftProfileType"],
        "_private.shafts._36": ["ShaftRadialHole"],
        "_private.shafts._37": ["ShaftRatingMethod"],
        "_private.shafts._38": ["ShaftSafetyFactorSettings"],
        "_private.shafts._39": ["ShaftSectionDamageResults"],
        "_private.shafts._40": ["ShaftSectionEndDamageResults"],
        "_private.shafts._41": ["ShaftSettings"],
        "_private.shafts._42": ["ShaftSettingsDatabase"],
        "_private.shafts._43": ["ShaftSettingsItem"],
        "_private.shafts._44": ["ShaftSurfaceFinishSection"],
        "_private.shafts._45": ["ShaftSurfaceRoughness"],
        "_private.shafts._46": ["SimpleShaftDefinition"],
        "_private.shafts._47": [
            "StressMeasurementShaftAxialBendingTorsionalComponentValues"
        ],
        "_private.shafts._48": ["SurfaceFinishes"],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "AGMAHardeningType",
    "CastingFactorCondition",
    "ConsequenceOfFailure",
    "DesignShaftSection",
    "DesignShaftSectionEnd",
    "FkmMaterialGroup",
    "FkmSnCurveModel",
    "FkmVersionOfMinersRule",
    "GenericStressConcentrationFactor",
    "ProfilePointFilletStressConcentrationFactors",
    "ShaftAxialBendingTorsionalComponentValues",
    "ShaftAxialBendingXBendingYTorsionalComponentValues",
    "ShaftAxialTorsionalComponentValues",
    "ShaftDamageResults",
    "ShaftDamageResultsTableAndChart",
    "ShaftFeature",
    "ShaftGroove",
    "ShaftKey",
    "ShaftMaterial",
    "ShaftMaterialDatabase",
    "ShaftMaterialForReports",
    "ShaftPointStress",
    "ShaftPointStressCycle",
    "ShaftPointStressCycleReporting",
    "ShaftProfile",
    "ShaftProfileFromImport",
    "ShaftProfileLoop",
    "ShaftProfilePoint",
    "ShaftProfilePointCopy",
    "ShaftProfileType",
    "ShaftRadialHole",
    "ShaftRatingMethod",
    "ShaftSafetyFactorSettings",
    "ShaftSectionDamageResults",
    "ShaftSectionEndDamageResults",
    "ShaftSettings",
    "ShaftSettingsDatabase",
    "ShaftSettingsItem",
    "ShaftSurfaceFinishSection",
    "ShaftSurfaceRoughness",
    "SimpleShaftDefinition",
    "StressMeasurementShaftAxialBendingTorsionalComponentValues",
    "SurfaceFinishes",
)

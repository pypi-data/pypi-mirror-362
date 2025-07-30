"""Subpackage."""

from typing import TYPE_CHECKING as __tc

if __tc:
    from mastapy._private.detailed_rigid_connectors.splines._1574 import (
        CustomSplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1575 import (
        CustomSplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1576 import (
        DetailedSplineJointSettings,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1577 import (
        DIN5480SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1578 import (
        DIN5480SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1579 import (
        DudleyEffectiveLengthApproximationOption,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1580 import FitTypes
    from mastapy._private.detailed_rigid_connectors.splines._1581 import (
        GBT3478SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1582 import (
        GBT3478SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1583 import (
        HeatTreatmentTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1584 import (
        ISO4156SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1585 import (
        ISO4156SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1586 import (
        JISB1603SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1587 import (
        ManufacturingTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1588 import Modules
    from mastapy._private.detailed_rigid_connectors.splines._1589 import (
        PressureAngleTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1590 import RootTypes
    from mastapy._private.detailed_rigid_connectors.splines._1591 import (
        SAEFatigueLifeFactorTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1592 import (
        SAESplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1593 import (
        SAESplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1594 import SAETorqueCycles
    from mastapy._private.detailed_rigid_connectors.splines._1595 import (
        SplineDesignTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1596 import (
        FinishingMethods,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1597 import (
        SplineFitClassType,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1598 import (
        SplineFixtureTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1599 import (
        SplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1600 import (
        SplineJointDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1601 import SplineMaterial
    from mastapy._private.detailed_rigid_connectors.splines._1602 import (
        SplineRatingTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1603 import (
        SplineToleranceClassTypes,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1604 import (
        StandardSplineHalfDesign,
    )
    from mastapy._private.detailed_rigid_connectors.splines._1605 import (
        StandardSplineJointDesign,
    )
else:
    import sys as __sys

    from lazy_imports import LazyImporter as __LazyImporter

    __import_structure = {
        "_private.detailed_rigid_connectors.splines._1574": ["CustomSplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1575": ["CustomSplineJointDesign"],
        "_private.detailed_rigid_connectors.splines._1576": [
            "DetailedSplineJointSettings"
        ],
        "_private.detailed_rigid_connectors.splines._1577": ["DIN5480SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1578": [
            "DIN5480SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1579": [
            "DudleyEffectiveLengthApproximationOption"
        ],
        "_private.detailed_rigid_connectors.splines._1580": ["FitTypes"],
        "_private.detailed_rigid_connectors.splines._1581": ["GBT3478SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1582": [
            "GBT3478SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1583": ["HeatTreatmentTypes"],
        "_private.detailed_rigid_connectors.splines._1584": ["ISO4156SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1585": [
            "ISO4156SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1586": [
            "JISB1603SplineJointDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1587": ["ManufacturingTypes"],
        "_private.detailed_rigid_connectors.splines._1588": ["Modules"],
        "_private.detailed_rigid_connectors.splines._1589": ["PressureAngleTypes"],
        "_private.detailed_rigid_connectors.splines._1590": ["RootTypes"],
        "_private.detailed_rigid_connectors.splines._1591": [
            "SAEFatigueLifeFactorTypes"
        ],
        "_private.detailed_rigid_connectors.splines._1592": ["SAESplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1593": ["SAESplineJointDesign"],
        "_private.detailed_rigid_connectors.splines._1594": ["SAETorqueCycles"],
        "_private.detailed_rigid_connectors.splines._1595": ["SplineDesignTypes"],
        "_private.detailed_rigid_connectors.splines._1596": ["FinishingMethods"],
        "_private.detailed_rigid_connectors.splines._1597": ["SplineFitClassType"],
        "_private.detailed_rigid_connectors.splines._1598": ["SplineFixtureTypes"],
        "_private.detailed_rigid_connectors.splines._1599": ["SplineHalfDesign"],
        "_private.detailed_rigid_connectors.splines._1600": ["SplineJointDesign"],
        "_private.detailed_rigid_connectors.splines._1601": ["SplineMaterial"],
        "_private.detailed_rigid_connectors.splines._1602": ["SplineRatingTypes"],
        "_private.detailed_rigid_connectors.splines._1603": [
            "SplineToleranceClassTypes"
        ],
        "_private.detailed_rigid_connectors.splines._1604": [
            "StandardSplineHalfDesign"
        ],
        "_private.detailed_rigid_connectors.splines._1605": [
            "StandardSplineJointDesign"
        ],
    }

    __sys.modules[__name__] = __LazyImporter(
        "mastapy",
        globals()["__file__"],
        __import_structure,
    )

__all__ = (
    "CustomSplineHalfDesign",
    "CustomSplineJointDesign",
    "DetailedSplineJointSettings",
    "DIN5480SplineHalfDesign",
    "DIN5480SplineJointDesign",
    "DudleyEffectiveLengthApproximationOption",
    "FitTypes",
    "GBT3478SplineHalfDesign",
    "GBT3478SplineJointDesign",
    "HeatTreatmentTypes",
    "ISO4156SplineHalfDesign",
    "ISO4156SplineJointDesign",
    "JISB1603SplineJointDesign",
    "ManufacturingTypes",
    "Modules",
    "PressureAngleTypes",
    "RootTypes",
    "SAEFatigueLifeFactorTypes",
    "SAESplineHalfDesign",
    "SAESplineJointDesign",
    "SAETorqueCycles",
    "SplineDesignTypes",
    "FinishingMethods",
    "SplineFitClassType",
    "SplineFixtureTypes",
    "SplineHalfDesign",
    "SplineJointDesign",
    "SplineMaterial",
    "SplineRatingTypes",
    "SplineToleranceClassTypes",
    "StandardSplineHalfDesign",
    "StandardSplineJointDesign",
)
